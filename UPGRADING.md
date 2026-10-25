# Upgrading and protecting existing data

## Read this before using the refreshed Compose file

The original setup and the refreshed setup have different database configuration and storage. **Do not replace the old YAML and run `up` expecting an automatic migration.** The generator deliberately refuses to run beside old data directories.

The previous file is retained at [`legacy/docker-compose.yaml`](legacy/docker-compose.yaml) for comparison only. It includes public default passwords and outdated assumptions; do not use it for new installations.

### Why existing installations need inspection

The old file declared a separate MySQL container but did not explicitly supply Huginn with the full external database configuration. It also mounted `./data` at `/var/lib/MySQL` (different casing from `/var/lib/mysql`) and mounted `./huginn` under `/app/huginn`. Depending on the image and Docker behavior, data may be in the external database, an image-created volume, or the application container's own database storage.

**Do not assume `./database` is your active Huginn database.** Inspect the running containers and mounts, the effective database host/name, and the existing service/image versions. Keep inspection output private: expanded configuration can contain credentials.

## Migrating from the old repository version

1. Record the existing Compose project name, YAML, image IDs/tags, mount locations, and environment files. Do not remove containers or volumes yet.
2. Identify which database Huginn actually uses. Export a logical database dump from that database using the matching tools for its current engine/version. A copy of an unrelated directory is not a verified backup.
3. Preserve `APP_SECRET_TOKEN`, credentials, any agent-created files, and a protected copy of the old configuration. Scenario exports alone do not preserve all users, events, credentials, or settings.
4. Follow [Huginn's upgrade guide](https://github.com/huginn/huginn/blob/master/UPGRADING.md) and [Docker database upgrade notes](https://github.com/huginn/huginn/tree/master/docker/multi-process). MySQL 5.7 data directories cannot be attached directly to 8.4; upstream requires an intermediate 8.0 upgrade for that in-place route. MariaDB data directories are not interchangeable with MySQL data directories.
5. Create the refreshed stack in a **different directory and Compose project**, with a different host port, leaving the original installation available for rollback. Generate a new `.env` there, then deliberately align the restored database credentials and original application secret as needed.
6. Test a version-compatible logical restore into the new isolated database. Stop the new Huginn service during the restore. Validate users, credentials, agents, events, schedules, and any external integrations before switching traffic. Application migrations can change restored data; preserve the pre-migration dump.
7. Stop the old deployment only after verifying the new one. Keep its backups and compatible images for rollback. Never run an older database binary against a data directory upgraded by a newer version.

This repository does not automate migration of unidentified old installations. That needs a plan based on the actual running database and versions, not just the contents of this GitHub repository.

## Updating an installation created with the refreshed setup

1. Read upstream release notes, including database and scenario compatibility changes.
2. Run `bash scripts/backup.sh`, and make a separate protected copy of `.env` and any files written by agents.
3. Test the backup and proposed image versions on a separate deployment. For a coordinated application snapshot, stop Huginn while dumping MySQL; also preserve any external files consistently.
4. Update image settings deliberately in `.env`. The Huginn release is pinned. `mysql:8.4` follows patch releases in that LTS series; it must not be changed to a new major version without a database upgrade plan.
5. Run `docker compose pull` and `docker compose up -d --wait --wait-timeout 600` in the same project directory/name. Confirm service health, login, and your important agents.

Changing `MYSQL_PASSWORD`, `MYSQL_USER`, or `MYSQL_DATABASE` in `.env` does not reconfigure an already-initialized database. Change database accounts with a deliberate database procedure and update the app configuration together.

## Restore a refreshed-stack logical backup

The following is for a **separate recovery deployment with an initialized database**, compatible images, and matching `.env` settings. Restoring replaces tables in the target database. Stop and verify the target project before doing this; do not experiment on your only working copy.

```bash
docker compose stop huginn
gzip -dc /path/to/your/backup.sql.gz | docker compose exec -T mysql sh -c \
  'MYSQL_PWD="$MYSQL_PASSWORD" exec mysql -u"$MYSQL_USER" "$MYSQL_DATABASE"'
docker compose up -d --wait --wait-timeout 600
```

Preserve the original application secret when recovering the deployment. Check the restore command's exit status and validate the recovered application before relying on it. The backup script contains the database, not `.env`, Docker images, agent output files, or any external storage.

The CI workflow exercises fresh initialization, login, a stored agent/event, container recreation, and a logical backup/restore on disposable AMD64 and ARM64 deployments. It does not certify migrations from arbitrary historic MySQL/MariaDB versions.
