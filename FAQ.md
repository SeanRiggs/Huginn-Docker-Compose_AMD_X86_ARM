# Huginn deployment FAQ

## Is Huginn still maintained?

Yes. The refreshed setup targets upstream release v2026.10.24. Check [upstream releases](https://github.com/huginn/huginn/releases) for current changes. This repository maintains a deployment example, not Huginn itself.

## Do I need a different Compose file for ARM?

No. Docker selects the native image for AMD64 or ARM64. Check the operating system architecture with `uname -m`: `x86_64` and `aarch64` are supported. Old ARMv7/armhf instructions and third-party images are historical and are not supported by this refresh.

## Why does setup refuse to continue?

It will not overwrite `.env` or initialize beside legacy data directories. If you already have an installation, follow [UPGRADING.md](UPGRADING.md). A generated secret must not change just because you rerun setup.

## Why is port 3000 unavailable from my laptop?

By default it is bound to localhost on the Docker host. Use the SSH tunnel described in the README, or deliberately configure a LAN binding and the `DOMAIN` setting. MySQL is not published to the host.

## How do I find the initial login?

Read `SEED_USERNAME` and `SEED_PASSWORD` in your local `.env`. Do not paste them into an issue. Changing the seed password after the database is initialized does not change the existing user's password; use Huginn's account controls or upstream recovery instructions.

## Can I copy only the YAML with wget or curl?

Use the full repository for this version: the setup script, template, backup tool, and migration instructions are part of the deployment. GitHub `/blob/` URLs download HTML pages, not raw YAML. For manual downloads, use the file's Raw link, and get all required companion files. Do not download an old Compose file from a tutorial and mix it with this configuration.

## Docker says permission denied or cannot connect to the daemon.

Confirm Docker is running and that your account can run `docker info`. Use your operating system's Docker installation instructions. On Linux, membership in the Docker group grants powerful host access; do not change socket permissions to world-writable as a workaround.

## The application is starting slowly or is unhealthy.

First startup creates schema and assets. Run `docker compose ps` and inspect `docker compose logs --tail=100 huginn` and `docker compose logs --tail=100 mysql` locally. Database credentials must match the initialized database, and the host needs enough resources. Redact private information before sharing logs. A failed health check does not mean the database should be deleted.

## I changed MYSQL_PASSWORD in .env and login stopped working.

MySQL initialization variables apply to a new, empty database volume. Editing `.env` does not change an existing database user's password. Restore the previous configuration or follow the database's credential-change procedure; do not discard the volume.

## Where did the static IP addresses and links go?

Compose gives the services a private network and DNS service names. Huginn connects to `mysql:3306`; fixed container IPs and legacy `links` are unnecessary. The app can still make outbound requests unless you enable an outbound proxy.

## Is .env a secret manager?

No. It is a private local configuration file. Keep it out of version control and backups intended for public sharing. Host administrators and users with Docker access can inspect container configuration.

## Will the old JSON scenarios still work?

Not necessarily. They are historical examples with service-specific assumptions, locations, and notification targets. TwitterStreamAgent is retired upstream. Review each scenario before importing and before enabling scheduled runs or notifications.

## Should I use n8n instead?

Either can be useful. Huginn is well suited to monitoring and event-processing agents. If your main goal is connecting business apps with a visual workflow editor, evaluate n8n as well. There is no need to retire a working Huginn deployment solely because another tool is popular.
