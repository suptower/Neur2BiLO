import json
import subprocess
import numpy as np

from .blo import BLO


class Watwa(BLO):
    """
    Bilevel problem wrapper for the WatwaOS optimizer.

    Leader:   selects a subset of cc_alt_vars (configuration switch candidates)
              x ∈ {0,1}^m  with  ||x||_0 = 2k
              (m = 6k, k = number of IO configuration switch points)

    Follower: WatwaOS ILP solver finds the optimal energy configuration
              for the program under the leader's constraints.
              Returns total energy consumption as the objective value.
    """

    def __init__(self, watwa_bin, config_path):
        """
        Parameters
        ----------
        watwa_bin   : str  path to the WatwaOS optimizer binary/script
        config_path : str  path to the instruction cost configuration file
        """
        self.watwa_bin = watwa_bin
        self.config_path = config_path


    # ------------------------------------------------------------------
    # Instance handling
    # ------------------------------------------------------------------

    def sample_instance(self, cfg, scale=True):
        """
        Sample a random program instance.

        For now this reads a program from a pre-generated pool.
        Later: generate synthetic C programs on the fly.
        """
        # TODO: implement random program selection from a pool
        # Placeholder: pick a random program path from cfg
        program_path = np.random.choice(cfg.program_paths)
        instance = self.read_instance(cfg, program_path, scale=scale)
        return instance


    def read_instance(self, cfg, program_path, scale=True):
        """
        Read a program instance and run WatwaOS to get all scenario results.

        Returns a dict with:
          - program_path : path to the C program
          - scenarios    : dict mapping scenario-tuple to {time, energy}
          - cc_alt_vars  : list of cc_alt_var names (in order)
          - ideal_energy : optimal energy found by WatwaOS
          - m            : total number of cc_alt_vars
          - k            : number of IO switch points (m = 6k)
        """
        # Run WatwaOS optimizer
        result = self._run_watwa(program_path)

        # Parse scenario results
        scenarios = result["solutions"]
        ideal_energy = result["ideal_energy"]

        # Extract cc_alt_vars structure from .lp files
        # (parsed separately, see utils/watwa.py)
        # TODO: parse cc_alt_vars from generated .lp files
        cc_alt_vars = self._parse_cc_alt_vars(program_path)
        m = len(cc_alt_vars)
        k = m // 6   # m = 6k by empirical observation

        if scale:
            # Normalize energy by worst-case (all-high-freq) energy
            worst_energy = max(s["energy"] for s in scenarios.values())
            for s in scenarios.values():
                s["energy_scaled"] = s["energy"] / worst_energy if worst_energy > 0 else 0
        else:
            worst_energy = 1
            for s in scenarios.values():
                s["energy_scaled"] = s["energy"]

        instance = {
            "program_path" : program_path,
            "scenarios"    : scenarios,
            "cc_alt_vars"  : cc_alt_vars,
            "ideal_energy" : ideal_energy,
            "worst_energy" : worst_energy,
            "m"            : m,
            "k"            : k,
        }

        return instance


    # ------------------------------------------------------------------
    # Follower
    # ------------------------------------------------------------------

    def solve_follower(self, instance, x):
        """
        Solve the follower problem for a given leader decision x.

        x is a binary vector of length m = 6k indicating which
        cc_alt_vars are active (1) or blocked (0).

        Since WatwaOS pre-computes all scenarios, we can look up
        the result directly from the cached scenario dict.

        Parameters
        ----------
        instance : dict  output of read_instance()
        x        : list/array of 0/1 of length m

        Returns
        -------
        dict with follower_obj, follower_sol, leader_obj, leader_sol
        """
        # Convert x to scenario key (tuple of active cc_alt_vars indices)
        scenario_key = self._x_to_scenario_key(x, instance["cc_alt_vars"])

        scenarios = instance["scenarios"]

        if scenario_key in scenarios:
            energy = scenarios[scenario_key]["energy_scaled"]
        else:
            # Scenario not pre-computed: run WatwaOS for this specific x
            # TODO: implement targeted single-scenario WatwaOS call
            energy = self._run_single_scenario(instance["program_path"], x)

        res = {
            "follower_obj" : energy,      # energy to minimize (leader obj)
            "follower_sol" : x,           # cc_alt_vars assignment
            "leader_obj"   : energy,
            "leader_sol"   : x,
        }

        return res


    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _run_watwa(self, program_path):
        """
        Call WatwaOS optimizer and return parsed JSON result.
        """
        cmd = [self.watwa_bin, program_path, self.config_path]
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            raise RuntimeError(
                f"WatwaOS failed for {program_path}:\n{result.stderr}"
            )

        # WatwaOS writes JSON to stdout or a fixed output path
        # TODO: adjust based on actual WatwaOS output location
        output = json.loads(result.stdout)
        return output


    def _parse_cc_alt_vars(self, program_path):
        """
        Parse cc_alt_vars from the generated .lp files.

        WatwaOS generates gurobi-model-*.lp files alongside the JSON.
        Each .lp file contains the cc_alt_vars for that batch of scenarios.

        Returns ordered list of cc_alt_var names.
        """
        import re
        import os

        lp_dir = os.path.dirname(program_path)
        lp_files = sorted(f for f in os.listdir(lp_dir) if f.startswith("gurobi-model"))

        if not lp_files:
            raise FileNotFoundError(f"No .lp files found in {lp_dir}")

        # All .lp files have the same cc_alt_vars – read from first file
        with open(os.path.join(lp_dir, lp_files[0])) as f:
            content = f.read()

        # Extract cc_alt_vars from the base model (before first Scenario block)
        base = content.split("Scenario")[0]
        vars_found = sorted(set(re.findall(r'cc_alt_vars_\d+', base)),
                            key=lambda v: int(v.split("_")[-1]))

        return vars_found


    def _x_to_scenario_key(self, x, cc_alt_vars):
        """
        Convert binary vector x to a scenario lookup key.

        The scenario keys in the JSON are tuples like "(2, 0)" representing
        the active configuration indices. This mapping needs to be aligned
        with how WatwaOS generates scenario keys.

        TODO: clarify exact scenario key format from WatwaOS JSON output.
        """
        active_indices = [i for i, val in enumerate(x) if val == 1]
        return str(tuple(active_indices))


    def _run_single_scenario(self, program_path, x):
        """
        Run WatwaOS for a single specific cc_alt_vars configuration.

        Used when the requested scenario was not pre-computed.
        TODO: implement once WatwaOS supports targeted scenario runs.
        """
        raise NotImplementedError(
            "Single-scenario WatwaOS calls not yet implemented. "
            "Use pre-computed scenarios only."
        )