"""Exercise a disposable Compose deployment; never point this at an existing install."""
import http.cookiejar
from html.parser import HTMLParser
from pathlib import Path
import subprocess
import sys
import urllib.parse
import urllib.request


class LoginForm(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hidden = {}

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "input" and attrs.get("type") == "hidden" and attrs.get("name"):
            self.hidden[attrs["name"]] = attrs.get("value", "")


def rails(code):
    subprocess.run(["docker", "compose", "exec", "-T", "huginn", "bundle", "exec",
                    "rails", "runner", code], check=True, timeout=180)


def login():
    config = dict(line.split("=", 1) for line in Path(".env").read_text().splitlines()
                  if line and not line.startswith("#"))
    base = "http://127.0.0.1:" + config.get("HUGINN_PORT", "3000")
    session = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
    with session.open(base + "/users/sign_in", timeout=30) as response:
        form = LoginForm()
        form.feed(response.read().decode())
    if not form.hidden.get("authenticity_token"):
        raise RuntimeError("Sign-in form did not contain a CSRF token")
    values = dict(form.hidden, **{"user[login]": config["SEED_USERNAME"],
                                 "user[password]": config["SEED_PASSWORD"]})
    with session.open(base + "/users/sign_in", urllib.parse.urlencode(values).encode(), timeout=30) as response:
        html = response.read().decode()
        if "/users/sign_out" not in html:
            raise RuntimeError("Admin sign-in did not reach an authenticated page")
    print("Admin HTTP sign-in passed.")


if sys.argv[1] == "prepare":
    login()
    rails('u = User.find_by!(username: ENV.fetch("SEED_USERNAME")); '
          'a = Agents::ManualEventAgent.create!(user: u, name: "Compose persistence check", options: {payload: {}}); '
          'a.create_event(payload: {"compose_refresh" => "retained"}); '
          'puts "Created persistence marker."')
elif sys.argv[1] == "verify":
    login()
    rails('u = User.find_by!(username: ENV.fetch("SEED_USERNAME")); '
          'a = u.agents.find_by!(name: "Compose persistence check"); '
          'abort "Event missing" unless a.events.any? { |e| e.payload["compose_refresh"] == "retained" }; '
          'abort "Wrong database" unless ActiveRecord::Base.connection.current_database == ENV.fetch("DATABASE_NAME"); '
          'puts "User, agent, and event persisted in the external database."')
else:
    raise SystemExit("Use prepare or verify")
