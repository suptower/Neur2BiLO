import os
import pickle as pkl
import time

import numpy as np

from blo.blo.watwa import Watwa
from blo.utils.watwa import get_path
from .data_manager import DataManager


class WatwaDataManager(DataManager):

    def __init__(self, cfg):
        """Constructor for WatwaOS bilevel problem."""
        self.cfg = cfg

        self.problem_path = get_path(self.cfg.data_path, self.cfg, "problem")
        self.ml_data_path = get_path(self.cfg.data_path, self.cfg, "ml_data")

        self.blo = Watwa()


    def initialize_problem(self):
        """
        Initialize the WatwaOS problem by running the optimizer on all
        program instances defined in cfg.program_dirs and storing the
        resulting scenario data.
        """
        print("Initializing WatwaOS problem...")

        self.prob = self._get_problem_data(self.cfg)

        print("Saving problem to:", self.problem_path)
        pkl.dump(self.prob, open(self.problem_path, 'wb'))


    def _solve_lower_level_mp(self, x, instance, inst_id, mp_time, mp_count, n_samples):
        """
        Obtain the follower objective for a given leader decision x.

        x is a ternary vector in {0,1,2}^s where s = number of switch points.
        The follower objective (energy) is looked up directly from the
        pre-computed WatwaOS scenario results.
        """
        time_ = time.time()

        # Solve follower for fixed x (lookup in pre-computed scenarios)
        solve_res = self.blo.solve_follower(instance, x)
        follower_obj = solve_res["follower_obj"]
        follower_sol = solve_res["follower_sol"]

        time_ = time.time() - time_

        results = {
            'x'            : x,
            'instance'     : instance,
            'inst_id'      : inst_id,
            'follower_obj' : follower_obj,
            'follower_sol' : follower_sol,
            'solve_res'    : solve_res,
        }

        self.update_mp_status(mp_count, mp_time, n_samples)

        return results


    def _sample_random_x(self, instance, X_hash=None):
        """
        Sample a random leader decision x ∈ {0,1,2}^s.

        s = instance['k'] = number of configuration switch points.
        Each position is independently sampled from {0, 1, 2}.

        Only samples scenarios that exist in the pre-computed results
        to avoid out-of-distribution decisions.
        """
        scenarios = instance["scenarios"]
        all_keys = list(scenarios.keys())

        # Sample a random scenario key from the pre-computed set
        while True:
            key = np.random.choice(all_keys)
            x = list(eval(key))   # e.g. "(2, 0)" -> [2, 0]
            x_str = str(x)

            if X_hash is None:
                break

            if x_str not in X_hash:
                X_hash.add(x_str)
                break

        return np.array(x)


    def _get_problem_data(self, cfg):
        """Store generic problem information from cfg."""
        prob = {}
        prob['program_dirs']       = cfg.program_dirs
        prob['n_samples_inst']     = cfg.n_samples_inst
        prob['n_samples_per_inst'] = cfg.n_samples_per_inst
        prob['n_samples']          = cfg.n_samples_inst * cfg.n_samples_per_inst
        prob['time_limit']         = cfg.time_limit
        prob['mip_gap']            = cfg.mip_gap
        prob['verbose']            = cfg.verbose
        prob['threads']            = cfg.threads
        prob['tr_split']           = cfg.tr_split
        prob['seed']               = cfg.seed
        prob['data_path']          = cfg.data_path

        return prob