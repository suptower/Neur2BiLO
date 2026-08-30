"""
Bilevel problem wrapper for the WatwaOS energy optimization benchmark.
"""

import ast
import json
import os
import subprocess

import numpy as np

from .blo import BLO


class Watwa(BLO):
    """
    Bilevel problem wrapper for the WatwaOS optimizer.
    The leader selects frequency switch-point decisions, and the follower
    evaluates corresponding system execution energy.
    """

    def __init__(self):
        super().__init__()

    # ------------------------------------------------------------------
    # Instance Handling
    # ------------------------------------------------------------------

    def sample_instance(self, cfg, scale=True):
        """Samples a random program instance directory from the configuration pool."""
        program_dir = np.random.choice(cfg.program_dirs)
        return self.read_instance(cfg, program_dir, scale=scale)

    def read_instance(self, cfg, program_dir, scale=True):
        """
        Reads program instance metadata and precomputed scenario solutions.

        Returns
        -------
        dict
            Contains program path, scenario solutions, ideal energy/scenario,
            worst-case energy, and number of switch points (k).
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

        # Parse switch-point count from first scenario key e.g. "(2, 0)" -> k=2
        first_key = next(iter(scenarios))
        k = len(ast.literal_eval(first_key))

        # Scale energy values relative to the worst-case scenario
        worst_energy = max(s["energy"] for s in scenarios.values()) if scenarios else 1.0

        for s in scenarios.values():
            if scale and worst_energy > 0:
                s["energy_scaled"] = s["energy"] / worst_energy
            else:
                s["energy_scaled"] = s["energy"]

        if not scale:
            worst_energy = 1.0

        return {
            "program_dir": program_dir,
            "scenarios": scenarios,
            "ideal_energy": ideal_energy,
            "ideal_scenario": ideal_scenario,
            "worst_energy": worst_energy,
            "k": k,
        }

    # ------------------------------------------------------------------
    # Follower Evaluation
    # ------------------------------------------------------------------

    def solve_follower(self, instance, x):
        """Evaluates follower energy objective for a given leader decision vector x."""
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

    # ------------------------------------------------------------------
    # Pipeline Execution & Formatting Helpers
    # ------------------------------------------------------------------

    def _run_watwa(self, program_dir):
        """Runs the WatwaOS compile and optimization pipeline in online mode."""
        result_path = os.path.join(program_dir, "build", "optimize-result.json")

        self._make(program_dir, "clean")
        self._make(program_dir, "build")
        self._make(program_dir, "optimize")

        if not os.path.exists(result_path):
            raise FileNotFoundError(f"optimize-result.json not found at {result_path}")

        with open(result_path) as f:
            return json.load(f)

    def _make(self, program_dir, target):
        """Executes a Makefile target in the specified program directory."""
        result = subprocess.run(
            ["make", target],
            cwd=program_dir,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            raise RuntimeError(f"make {target} failed in {program_dir}:\n{result.stderr}")

    def _x_to_scenario_key(self, x):
        """Converts an integer decision vector to a scenario key string, e.g. [2, 0] -> '(2, 0)'."""
        return str(tuple(int(v) for v in x))