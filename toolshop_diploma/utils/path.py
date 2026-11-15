from pathlib import Path


def abs_path_from_project(relative: str) -> str:
    """Repo root is two levels above utils/."""
    root = Path(__file__).resolve().parents[2]
    return str(root / relative)
