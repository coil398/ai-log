#!/usr/bin/env python3
"""Create or append today's daily work-log entry and commit only touched files."""

from __future__ import annotations

import argparse
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

JST = ZoneInfo("Asia/Tokyo")


def run(cmd: list[str], cwd: Path | None = None, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=cwd,
        check=check,
        text=True,
        capture_output=True,
    )


def git(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return run(["git", "-C", str(repo), *args], check=check)


def ensure_repo(repo: Path) -> None:
    if not repo.is_dir():
        raise SystemExit(f"data repo not found: {repo}")
    r = git(repo, "rev-parse", "--is-inside-work-tree", check=False)
    if r.returncode != 0 or r.stdout.strip() != "true":
        raise SystemExit(f"not a git repository: {repo}")


def pull_rebase(repo: Path) -> None:
    r = git(repo, "pull", "--rebase", check=False)
    if r.returncode != 0:
        msg = (r.stderr or r.stdout or "").strip()
        raise SystemExit(f"git pull --rebase failed:\n{msg}")


def build_section(now: datetime, title: str, body: str) -> str:
    heading = f"## {now.strftime('%H:%M')} JST {title}".rstrip()
    text = body.strip()
    if text:
        return f"{heading}\n\n{text}\n"
    return f"{heading}\n"


def write_entry(path: Path, date_str: str, agent: str, section: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        existing = path.read_text(encoding="utf-8")
        if not existing.endswith("\n"):
            existing += "\n"
        path.write_text(existing + "\n---\n\n" + section, encoding="utf-8")
        return
    front = (
        "---\n"
        f"date: {date_str}\n"
        f"agent: {agent}\n"
        "type: daily-work-log\n"
        "---\n\n"
    )
    path.write_text(front + section, encoding="utf-8")


def commit_and_push(
    repo: Path,
    rel_path: str,
    message: str,
    do_commit: bool,
    do_push: bool,
) -> None:
    if not do_commit:
        print(f"wrote {rel_path} (no commit)")
        return
    git(repo, "add", "--", rel_path)
    staged = git(repo, "diff", "--cached", "--name-only")
    names = [n for n in staged.stdout.splitlines() if n.strip()]
    if not names:
        print("nothing to commit")
        return
    if names != [rel_path]:
        git(repo, "reset", "HEAD", "--", *names, check=False)
        git(repo, "add", "--", rel_path)
        staged = git(repo, "diff", "--cached", "--name-only")
        names = [n for n in staged.stdout.splitlines() if n.strip()]
        if names != [rel_path]:
            raise SystemExit(f"refusing to commit unexpected paths: {names}")
    git(repo, "commit", "-m", message)
    print(f"committed: {message}")
    if do_push:
        r = git(repo, "push", check=False)
        if r.returncode != 0:
            msg = (r.stderr or r.stdout or "").strip()
            raise SystemExit(f"git push failed (local commit kept):\n{msg}")
        print("pushed")


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--repo", type=Path, default=Path.home() / "ai-log-data")
    p.add_argument("--agent", required=True, help="agent id, e.g. hermes")
    p.add_argument("--title", required=True)
    p.add_argument("--body", default="")
    p.add_argument("--message", default="", help="summary part of commit message")
    p.add_argument("--no-commit", action="store_true")
    p.add_argument("--no-push", action="store_true")
    p.add_argument("--skip-pull", action="store_true")
    args = p.parse_args()

    repo = args.repo.expanduser().resolve()
    ensure_repo(repo)
    if not args.skip_pull:
        pull_rebase(repo)

    now = datetime.now(JST)
    date_str = now.strftime("%Y-%m-%d")
    rel = f"daily/{date_str}/{args.agent}.md"
    path = repo / rel
    section = build_section(now, args.title, args.body)
    write_entry(path, date_str, args.agent, section)

    summary = args.message.strip() or args.title.strip()
    message = f"log: {date_str} {summary}"
    commit_and_push(
        repo,
        rel,
        message,
        do_commit=not args.no_commit,
        do_push=not args.no_commit and not args.no_push,
    )


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as e:
        err = (e.stderr or e.stdout or str(e)).strip()
        print(err, file=sys.stderr)
        sys.exit(e.returncode or 1)
