#!/usr/bin/env python3
"""Initialize repository-centered AI governance without silent overwrites."""

from __future__ import annotations

import argparse
import datetime as dt
import re
import shutil
import subprocess
import sys
from pathlib import Path


TASK_ID_RE = re.compile(r"^(?:[A-Z][A-Z0-9]*-)?TASK-\d+$")


def git_head(root: Path) -> str:
    result = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "HEAD"],
        text=True,
        capture_output=True,
        check=False,
    )
    return result.stdout.strip() if result.returncode == 0 else "UNAVAILABLE"


def render(source: Path, replacements: dict[str, str]) -> str:
    text = source.read_text(encoding="utf-8")
    for marker, value in replacements.items():
        text = text.replace("{{" + marker + "}}", value)
    return text


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_root", type=Path)
    parser.add_argument("--project-name")
    parser.add_argument("--purpose", default="UNKNOWN — define the durable project purpose.")
    parser.add_argument("--task-id", default="TASK-001")
    parser.add_argument("--force", action="store_true", help="Overwrite governance files; requires explicit authorization.")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    root = args.project_root.resolve()
    if not TASK_ID_RE.fullmatch(args.task_id):
        parser.error("--task-id must look like TASK-001 or PREFIX-TASK-001")

    skill_root = Path(__file__).resolve().parent.parent
    templates = skill_root / "templates"
    mappings = {
        templates / "AGENTS.template.md": root / "AGENTS.md",
        templates / "PROJECT.template.md": root / ".ai" / "PROJECT.md",
        templates / "STATE.template.md": root / ".ai" / "STATE.md",
        templates / "TASK.template.md": root / ".ai" / "tasks" / f"{args.task_id}.md",
    }
    change_source = skill_root / "references" / "change-policy.md"
    change_target = root / ".ai" / "CHANGE_POLICY.md"
    baseline_target = root / ".ai" / "TRACEABILITY_BASELINE"
    conflicts = [path for path in [*mappings.values(), change_target, baseline_target] if path.exists()]
    if conflicts and not args.force:
        print("Refusing to overwrite existing files:", file=sys.stderr)
        for path in conflicts:
            print(f"  {path}", file=sys.stderr)
        print("Merge deliberately, or use --force only with explicit authorization.", file=sys.stderr)
        return 2

    replacements = {
        "PROJECT_NAME": args.project_name or root.name,
        "PROJECT_PURPOSE": args.purpose,
        "INITIAL_TASK_ID": args.task_id,
        "DATE": dt.date.today().isoformat(),
    }

    print(f"Initialize governance in {root}")
    for source, target in mappings.items():
        print(f"  write {target}")
        if not args.dry_run:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(render(source, replacements), encoding="utf-8")
    print(f"  copy  {change_target}")
    print(f"  write {baseline_target}")
    if not args.dry_run:
        change_target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(change_source, change_target)
        (root / ".ai" / "decisions").mkdir(parents=True, exist_ok=True)
        (root / ".ai" / "tasks" / "archive").mkdir(parents=True, exist_ok=True)
        baseline_target.write_text(git_head(root) + "\n", encoding="utf-8")
    print("Initialization complete. Tailor UNKNOWN fields, then run validate_state.py.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
