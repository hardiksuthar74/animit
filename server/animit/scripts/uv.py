"""Console script to create an alembic revision with a random UUID message
and then run `alembic upgrade heads`.

Install the package (editable) to get the `uv` console script:

    pip install -e .

Then run:

    uv

You can also pass an explicit message with `--message` / `-m`.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import uuid
from pathlib import Path


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]

    parser = argparse.ArgumentParser(
        prog="uv", description="Create alembic revision and upgrade heads"
    )
    parser.add_argument(
        "-m", "--message", help="Revision message (defaults to random UUID)"
    )
    args = parser.parse_args(argv)

    msg = args.message or str(uuid.uuid4())

    # Compute project root (two levels up from this file -> server folder)
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
        print(
            f"Running: alembic revision --message '{msg}' --autogenerate (cwd={cwd or os.getcwd()})"
        )
        subprocess.run(
            [
                sys.executable,
                "-m",
                "alembic",
                "revision",
                "--message",
                msg,
                "--autogenerate",
            ],
            check=True,
            cwd=cwd,
            env=env,
        )

        print("Running: alembic upgrade heads")
        subprocess.run(
            [
                sys.executable,
                "-m",
                "alembic",
                "upgrade",
                "heads",
            ],
            check=True,
            cwd=cwd,
            env=env,
        )

    except subprocess.CalledProcessError as exc:
        print("Command failed:", exc)
        return 2

    print("Migration created and upgraded to heads.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
