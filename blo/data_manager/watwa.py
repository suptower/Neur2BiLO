"""
Bilevel problem wrapper for WatwaOS energy optimization.
"""

import ast
import json
import os
import subprocess

import numpy as np

from .blo import BLO


class Watwa(BLO):
    """
    Bilevel problem interface for WatwaOS.
    The leader selects discrete frequency choices per switch point,
    and the follower evaluates the corresponding energy consumption.
    """

    def sample_instance(self, cfg, scale=True):
        """Samples a random program instance directory from the configuration pool."""
        program_dir = np.random.choice(cfg.program_dirs)
        return self.read_instance(cfg, program_dir, scale=scale)

    def read_instance(self, cfg, program_dir, scale=True):
        """
        Loads program instance metadata and precomputed scenario solutions.

        Returns a dictionary containing:
            program_dir: Path to the program directory.
            scenarios: Mapping from scenario keys to energy metrics.
            ideal_energy: Minimum energy value from exhaustive search.
            ideal_scenario: Key of the optimal scenario tuple (e.g. '(2, 0)').
            worst_energy: Maximum energy across all evaluated scenarios.
            k: Number of switch points.
        """
        result_path = os.path.join(program_dir, "build", "optimize-result.json")
        pml_path = os.path.join(program_dir, "build", "app.c.pml")

        if os.path.exists(result_path) and os.path.exists(pml_path):
            with open(result_path) as f:
                result = json.load(f)
        else:
            result = self._run_watwa(program_dir)

        scenarios = result["solutions"]
        ideal_energy = result["ideal_energy"]
        ideal_scenario = result["ideal_scenario"]

        first_key = next(iter(scenarios))
        k = len(ast.literal_eval(first_key))

        worst_energy = max((s["energy"] for s in scenarios.values()), default=1.0)
        for s in scenarios.values():
            s["energy_scaled"] = (
                s["energy"] / worst_energy if scale and worst_energy > 0 else s["energy"]
            )

        return {
            "program_dir": program_dir,
            "scenarios": scenarios,
            "ideal_energy": ideal_energy,
            "ideal_scenario": ideal_scenario,
            "worst_energy": worst_energy if scale else 1.0,
            "k": k,
        }

    def solve_follower(self, instance, x):
        """Looks up the follower energy objective for leader decision vector x."""
        scenario_key = self._x_to_scenario_key(x)
        scenarios = instance["scenarios"]

        if scenario_key not in scenarios:
            raise KeyError(f"Scenario {scenario_key} not found in precomputed results.")

        energy = scenarios[scenario_key]["energy_scaled"]
        return {
            "follower_obj": energy,
            "follower_sol": list(x),
            "leader_obj": energy,
            "leader_sol": list(x),
        }

    def _run_watwa(self, program_dir):
        """Runs the WatwaOS compile and optimization pipeline."""
        result_path = os.path.join(program_dir, "build", "optimize-result.json")

        self._make(program_dir, "clean")
        self._make(program_dir, "build")
        self._make(program_dir, "optimize")

        if not os.path.exists(result_path):
            raise FileNotFoundError(f"optimize-result.json not found at {result_path}")

        with open(result_path) as f:
            return json.load(f)

    def _make(self, program_dir, target):
        """Executes a Makefile target within the given program directory."""
        result = subprocess.run(
            ["make", target],
            cwd=program_dir,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            raise RuntimeError(f"make {target} failed in {program_dir}:\n{result.stderr}")

    def _x_to_scenario_key(self, x):
        """Converts an integer decision vector to a scenario string key, e.g. [2, 0] -> '(2, 0)'."""
        return str(tuple(int(v) for v in x))