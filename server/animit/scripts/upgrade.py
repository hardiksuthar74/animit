"""Run alembic upgrade.

Usage:
  uv-upgrade             # upgrades to heads
  uv-upgrade target      # upgrades to given target (e.g. 'heads' or a revision id)
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]

    parser = argparse.ArgumentParser(
        prog="uv-upgrade", description="Run alembic upgrade"
    )
    parser.add_argument(
        "target", nargs="?", default="heads", help="Upgrade target (default: heads)"
    )
    args = parser.parse_args(argv)

    target = args.target

    project_root = Path(__file__).resolve().parents[2]
    alembic_ini = project_root / "alembic.ini"

    if not alembic_ini.exists():
        print(
            f"alembic.ini not found at {alembic_ini}. Running from current working directory."
        )
        cwd = None
    else:
        cwd = str(project_root)

    env = os.environ.copy()

    try:
        print(f"Running: alembic upgrade {target} (cwd={cwd or os.getcwd()})")
        subprocess.run(
            [
                sys.executable,
                "-m",
                "alembic",
                "upgrade",
                target,
            ],
            check=True,
            cwd=cwd,
            env=env,
        )

    except subprocess.CalledProcessError as exc:
        print("Command failed:", exc)
        return 2

    print("Upgrade complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
