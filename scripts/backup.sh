#!/usr/bin/env bash
# Run from the repository directory. A database-only logical backup.
set -euo pipefail
umask 077
mkdir -p backups
backup="backups/huginn-$(date -u +%Y%m%dT%H%M%SZ)-${RANDOM}.sql.gz"
partial="${backup}.partial"
trap 'rm -f "$partial"' EXIT
# Credentials expand inside the container and are never printed.
docker compose exec -T mysql sh -c \
  'MYSQL_PWD="$MYSQL_PASSWORD" exec mysqldump --user="$MYSQL_USER" --single-transaction --no-tablespaces --skip-lock-tables "$MYSQL_DATABASE"' \
  | gzip > "$partial"
gzip -t "$partial"
mv "$partial" "$backup"
printf 'Database backup saved: %s\nKeep your .env separately; it is NOT included.\n' "$backup"
