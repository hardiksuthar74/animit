"""Create an alembic revision with a message (defaults to a UUID).

Usage:
  uv-revision            # creates revision with random uuid message
  uv-revision -m "msg"   # creates revision with provided message
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
        prog="uv-revision", description="Create alembic revision"
    )
    parser.add_argument(
        "-m", "--message", help="Revision message (defaults to random UUID)"
    )
    args = parser.parse_args(argv)

    msg = args.message or str(uuid.uuid4())

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

    except subprocess.CalledProcessError as exc:
        print("Command failed:", exc)
        return 2

    print("Revision created.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
