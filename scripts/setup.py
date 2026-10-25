#!/usr/bin/env python3
"""Create fresh-install configuration without printing or overwriting secrets."""
import os
from pathlib import Path
import secrets
import sys


def main():
    root = Path.cwd()
    if not (root / "docker-compose.yaml").is_file():
        raise SystemExit("Run this script from the repository directory.")
    if (root / ".env").exists():
        raise SystemExit(".env already exists; it was not changed. See UPGRADING.md.")
    if any((root / name).exists() for name in ("data", "database", "huginn")):
        raise SystemExit("Legacy data directories found. Read UPGRADING.md; no files changed.")
    template = (root / ".env.example").read_text()
    generated = {key: secrets.token_hex(length) for key, length in (
        ("MYSQL_ROOT_PASSWORD", 32), ("MYSQL_PASSWORD", 32),
        ("APP_SECRET_TOKEN", 64), ("SEED_PASSWORD", 24), ("INVITATION_CODE", 32)
    )}
    lines = []
    for line in template.splitlines():
        key = line.split("=", 1)[0]
        lines.append(key + "=" + generated[key] if key in generated else line)
    # O_EXCL protects against overwriting an existing file, including symlinks.
    fd = os.open(root / ".env", os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "w") as target:
        target.write("\n".join(lines) + "\n")
    print("Created .env with unique credentials (owner read/write on POSIX).")
    print("Review .env, then run: docker compose config --quiet")
    print("Your initial admin username and password are SEED_USERNAME and SEED_PASSWORD in .env.")


if __name__ == "__main__":
    try:
        main()
    except OSError as error:
        sys.exit("Could not create configuration: " + str(error))
