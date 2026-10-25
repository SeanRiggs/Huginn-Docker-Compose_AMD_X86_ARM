# Huginn, ready for your homelab

[![Compose tests](https://github.com/SeanRiggs/Huginn-Docker-Compose_AMD_X86_ARM/actions/workflows/compose-test.yml/badge.svg)](https://github.com/SeanRiggs/Huginn-Docker-Compose_AMD_X86_ARM/actions/workflows/compose-test.yml)

**Give your server something useful to keep an eye on.** Watch a feed, spot a change, filter the noise, and send yourself the update that matters. This project makes Huginn easier to start with Docker Compose: an official Huginn image, a separate MySQL database, persistent storage, and credentials generated for your own installation.

> **Existing installation? Start with [UPGRADING.md](UPGRADING.md).** The refreshed configuration uses different storage and explicit database settings. It is not a drop-in upgrade for the original Compose file. Never attach a newer database image to old data without an upgrade plan and a verified backup.

## What changed in this refresh?

- Official Huginn image pinned to **v2026.10.24**, with MySQL on the **8.4 LTS series**.
- One Compose configuration for **AMD64 and ARM64**; Docker chooses the image for your host.
- An explicit app-to-database connection, with database readiness checks before Huginn starts.
- Unique generated database passwords, an initial administrator password, an invitation code, and a persistent application secret.
- A named database volume; no host mount hiding the application code.
- Localhost-only access by default, bounded container logs, and no published MySQL port.
- Configuration tests and real deployment smoke tests in GitHub Actions, including sign-in, container recreation, and database backup/restore.

This is a community deployment starter, not the Huginn application source or a managed hosting service. [Upstream Huginn](https://github.com/huginn/huginn) supplies the application and images.

## Supported hosts

| Platform | Status |
| --- | --- |
| `linux/amd64` (Intel/AMD 64-bit) | Included in native CI smoke tests. |
| `linux/arm64` (64-bit ARM, including a Pi with a 64-bit OS) | Included in native CI smoke tests. |
| `linux/arm/v7` / 32-bit Raspberry Pi OS | Not supported by this refreshed setup. Use a supported 64-bit OS where the hardware permits it. |

The old repository name is retained so existing links keep working. x86-64 and AMD64 refer to the same architecture; a 64-bit-capable Pi still needs a 64-bit operating system. On Windows/macOS, use Docker Desktop with Linux containers; those desktop environments are not covered by this repository's native Linux tests.

## Fresh install

Requirements: Git, Python 3, Docker Engine or Docker Desktop, and the **Docker Compose v2** plugin (`docker compose version`). Use an always-on host with room for the database and backups. Check the workflow badge for the most recent test results.

```bash
git clone https://github.com/SeanRiggs/Huginn-Docker-Compose_AMD_X86_ARM.git
cd Huginn-Docker-Compose_AMD_X86_ARM
python3 scripts/setup.py
```

The setup script creates `.env` with random credentials and owner-only file permissions on POSIX systems. It refuses to overwrite an existing `.env` or proceed when it finds the old `data/`, `database/`, or `huginn/` directories. On Windows, protect the file with your normal account/file permissions.

Open `.env` in your editor. Review `TIMEZONE`, `SEED_EMAIL`, and any network changes you need. Your initial login is the `SEED_USERNAME` and `SEED_PASSWORD` recorded there. The default email is a placeholder; set a real address and configure SMTP separately if you want working password-reset mail.

```bash
docker compose config --quiet
docker compose pull
docker compose up -d --wait --wait-timeout 600
docker compose ps
```

Open **http://localhost:3000**. First startup initializes the database and can take several minutes. If Docker runs on another computer, `localhost` means that computer, not your laptop; see access options below.

Keep `.env` private and backed up. Moving passwords into `.env` prevents accidental hardcoding in the Compose file; it does not encrypt them or hide them from host/Docker administrators. Do not post expanded `docker compose config` output or share `.env` in bug reports.

## Access from another computer

The default port binding is `127.0.0.1:3000`, so the web interface is reachable only on the Docker host. For remote administration, an SSH tunnel keeps that default intact:

```bash
ssh -L 3000:127.0.0.1:3000 your-user@your-server
```

Then open http://localhost:3000 on your computer.

For a trusted LAN, set `HUGINN_BIND_ADDRESS` to your server's LAN IP and set `DOMAIN` to the address users will visit, including the port. Recreate Huginn after editing `.env`. Binding `0.0.0.0` exposes the port on all host interfaces, so account for the host's network and firewall rules. For Internet access, put an HTTPS reverse proxy in front and review [upstream deployment configuration](https://github.com/huginn/huginn/blob/master/.env.example); this starter does not provide TLS or a reverse proxy.

## Configuration

Edit `.env`, then run `docker compose up -d`. `.env.example` documents the available settings.

| Setting | Purpose |
| --- | --- |
| `HUGINN_IMAGE` | Tested upstream release tag. Change deliberately after reading upstream release notes. |
| `MYSQL_IMAGE` | MySQL LTS series; currently `mysql:8.4`. Patch updates are allowed within that series. |
| `MYSQL_DATABASE`, `MYSQL_USER` | Database created during first initialization. |
| `MYSQL_PASSWORD`, `MYSQL_ROOT_PASSWORD` | Generated application and database administrator passwords. |
| `APP_SECRET_TOKEN` | Generated Rails secret. Preserve it across container replacements and restores. |
| `SEED_USERNAME`, `SEED_EMAIL`, `SEED_PASSWORD` | Initial administrator account; changing these does not reset an existing account. |
| `INVITATION_CODE` | Generated signup invitation code. Keep it private. |
| `HUGINN_BIND_ADDRESS`, `HUGINN_PORT`, `DOMAIN` | Host port binding and browser-facing address. |
| `TIMEZONE` | Huginn time zone; defaults to UTC. |
| `FORCE_SSL` | Defaults to false for the local HTTP setup. Enable only with a correctly configured HTTPS deployment. |
| `ENABLE_SMOKESCREEN` | Defaults to false for trusted-user homelabs. See below. |

For a shared installation where untrusted users can create agents, set `ENABLE_SMOKESCREEN=true` and review [Huginn's outbound-request controls](https://github.com/huginn/huginn/blob/master/doc/manual/outbound-requests.md). This restricts HTTP(S) access to internal addresses and can affect agents intended to monitor your LAN; it does not cover every protocol. Review the upstream guidance before changing it.

Email agents need SMTP configuration. Add the upstream `SMTP_*` settings you require to the Huginn service's `environment` section, referencing values in your private `.env`. Merely adding an unused setting to `.env` does not pass it to the container.

## Everyday commands

```bash
docker compose ps                  # Service status
docker compose logs --tail=100 huginn
docker compose stop               # Stop, keep containers and data
docker compose start              # Start existing containers
docker compose down               # Remove containers/network, retain the database volume
```

**Do not use `docker compose down --volumes` on an installation you want to keep.** It deletes the named database volume. Keep the same Compose project name/directory when recreating the deployment; a different project name uses a different named volume.

## Backups and restores

```bash
bash scripts/backup.sh
```

This creates a compressed logical database dump in `backups/` with restrictive permissions. It uses the new configuration's MySQL service and does not support the old bundled-database layout. It does not back up `.env`, host files written by agents, or other external services. Keep separate protected copies of those and test restores on an isolated deployment. Restore instructions and upgrade cautions are in [UPGRADING.md](UPGRADING.md).

## Scenario ideas

The files in [`JSON Files/`](JSON%20Files/) are **historical examples**, not a tested current scenario pack. They can help explain weather alerts, RSS filtering, email digests, and earthquake monitoring. Some upstream services and agent types have changed or disappeared. Review [the scenario notes](JSON%20Files/README.txt) before importing; configure credentials, locations, and recipients for your own installation.

## Huginn or n8n?

Huginn remains a useful choice for agents that watch feeds, scrape changes, filter events, and send alerts. n8n is another option for building workflows between applications. Pick the tool for the job; this repository focuses on making Huginn understandable and reproducible rather than competing with every automation platform.

## Help make it better

Useful contributions include tested scenario examples, clearer upgrade instructions, deployment fixes, and reproducible bug reports. Keep changes focused and include your CPU architecture, Docker/Compose versions, and the checks you ran. Never include credentials, private event data, or unredacted logs. See [CONTRIBUTING.md](CONTRIBUTING.md) and [FAQ.md](FAQ.md).

Local configuration tests:

```bash
python3 -m unittest discover -s tests -v
bash -n scripts/backup.sh
```

The CI workflow also creates a disposable deployment on AMD64 and ARM64, checks HTTP login, creates an agent/event, recreates containers, and restores a database backup into a clean test volume. **Do not run the CI volume-removal steps against your own installation.** Passing these checks is not a guarantee that every external scenario or hardware configuration works.

## Upstream and license

- [Huginn source and documentation](https://github.com/huginn/huginn)
- [Upstream releases](https://github.com/huginn/huginn/releases)
- [Upstream Docker documentation](https://github.com/huginn/huginn/tree/master/docker/multi-process)

This repository's deployment files use the [MIT license](LICENSE.md). Huginn and third-party images retain their own licenses and credits.
