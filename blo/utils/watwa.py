from pathlib import Path


def lst_to_str(lst):
    """Convert list to a string."""
    return "-".join(map(str, lst))


def get_path(data_path, cfg, ptype, suffix="pkl"):
    """Gets path for WatwaOS problem."""
    p = Path(data_path) / "watwa"
    p.mkdir(parents=True, exist_ok=True)

    p = p / (
        f"{ptype}_"
        f"nsi-{cfg.n_samples_inst}_"
        f"nspi-{cfg.n_samples_per_inst}_"
        f"s-{cfg.seed}"
        f".{suffix}"
    )

    return p