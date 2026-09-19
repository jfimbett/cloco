"""
Path helpers backed by data/registry.json. Import from any script under code/:

    import sys; sys.path.insert(0, "code")          # if not running from repo root
    from utils.data_paths import data_path, out_path, project_root

    df = pd.read_parquet(data_path("crsp_msf_2000_2023"))
    df.to_parquet(out_path("panel_clean", stage="processed", depends_on=["crsp_msf_2000_2023"]))

Never write literal Dropbox / home-directory paths in analysis code.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_ROOT / ".claude" / "scripts"))
from data_registry import load_env, load_registry, resolve  # noqa: E402


def project_root() -> Path:
    return _ROOT


def data_path(name: str, must_exist: bool = True) -> Path:
    """Absolute path of a registered dataset on this machine."""
    reg = load_registry()["datasets"]
    if name not in reg:
        raise KeyError(f"'{name}' is not in data/registry.json — register it with /data-registry add")
    p, missing = resolve(reg[name]["path"], load_env())
    if missing:
        raise EnvironmentError(f"{missing} not set in .env (see .env.example)")
    if must_exist and not p.exists():
        raise FileNotFoundError(f"{name} is registered at {p} but the file is not on this machine")
    return p


def out_path(name: str, stage: str = "processed", fmt: str = "parquet", root: str = "${PROJECT_ROOT}",
             depends_on: list[str] | None = None, source: str | None = None, register: bool = True) -> Path:
    """Path to write a derived dataset to; registers it (idempotently) so downstream code can data_path() it."""
    template = f"{root}/data/{stage}/{name}.{fmt}" if root == "${PROJECT_ROOT}" else f"{root}/{name}.{fmt}"
    p, missing = resolve(template, load_env())
    if missing:
        raise EnvironmentError(f"{missing} not set in .env")
    p.parent.mkdir(parents=True, exist_ok=True)
    if register:
        cmd = [sys.executable, str(_ROOT / ".claude/scripts/data_registry.py"), "add", name, "--path", template,
               "--stage", stage, "--source", source or f"produced by {Path(sys.argv[0]).name}", "--format", fmt, "--force",
               "--script", str(Path(sys.argv[0]).resolve().relative_to(_ROOT)) if Path(sys.argv[0]).resolve().is_relative_to(_ROOT) else Path(sys.argv[0]).name]
        if depends_on:
            cmd += ["--depends", *depends_on]
        subprocess.run(cmd, check=False, capture_output=True)
    return p
