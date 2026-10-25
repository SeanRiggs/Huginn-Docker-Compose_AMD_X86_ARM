# Make your homelab a little smarter

Contributions are welcome. Good changes make this deployment easier to understand, easier to recover, or easier to verify.

- Keep the official-image setup reproducible on AMD64 and ARM64.
- Explain changes to image versions, environment variables, or storage; include an upgrade path if data could be affected.
- Run `python3 -m unittest discover -s tests -v` and `bash -n scripts/backup.sh`.
- For deployment changes, use a disposable project and run the workflow's smoke checks. Its volume deletion is strictly for disposable test data.
- Include your OS, CPU architecture, Docker/Compose versions, and exact reproduction steps in a pull request.
- Never commit `.env`, database dumps, real credentials, or personal event data.
- Scenario contributions need setup requirements, credential placeholders, example events, notification destinations, and the date/version tested. Disable schedules and notifications until users configure their own destinations.

The historical scenarios are learning examples. Improve or replace them with tested examples rather than promising their old external services still work. Preserve credits and the existing license.
