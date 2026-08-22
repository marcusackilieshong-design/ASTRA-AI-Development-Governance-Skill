#!/usr/bin/env python3
"""Check bidirectional traceability between Git commits and task records."""

from __future__ import annotations

import argparse
import re
import subprocess
from pathlib import Path


TASK_ID_RE = re.compile(r"\b(?:[A-Z][A-Z0-9]*-)?(?:EPIC|TASK|SUBTASK|PATCH|INTERRUPT)-\d+(?:\.\d+)?\b")
HASH_RE = re.compile(r"\b[0-9a-fA-F]{7,40}\b")


def git(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", "-C", str(root), *args], text=True, capture_output=True, check=False)


def find_task(tasks: Path, identifier: str) -> Path | None:
    matches = [path for path in tasks.rglob("*.md") if path.stem == identifier or path.stem.startswith(identifier + "-")]
    return matches[0] if len(matches) == 1 else None


def commit_touches_product(root: Path, commit: str) -> bool:
    result = git(root, "diff-tree", "--root", "--no-commit-id", "--name-only", "-r", commit)
    names = [line for line in result.stdout.splitlines() if line]
    return any(not (name == "AGENTS.md" or name.startswith(".ai/")) for name in names)


def trace_section(text: str) -> str | None:
    match = re.search(r"(?ms)^## Git Traceability\s*\n(.*?)(?=^## |\Z)", text)
    return match.group(1).strip() if match else None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_root", type=Path)
    parser.add_argument("--range", dest="revision_range", help="Git revision range; overrides TRACEABILITY_BASELINE")
    parser.add_argument("--include-governance-only", action="store_true")
    parser.add_argument("--full", action="store_true", help="Also audit every cold task record.")
    args = parser.parse_args()
    root = args.project_root.resolve()
    tasks = root / ".ai" / "tasks"
    baseline_file = root / ".ai" / "TRACEABILITY_BASELINE"
    errors: list[str] = []
    audit_paths: set[Path] = set()

    if git(root, "rev-parse", "--is-inside-work-tree").returncode != 0:
        print("SKIP: project is not a Git work tree")
        return 0
    if not tasks.is_dir():
        print("ERROR: missing .ai/tasks")
        return 1

    if args.revision_range:
        revision = args.revision_range
    else:
        baseline = baseline_file.read_text(encoding="utf-8").strip() if baseline_file.exists() else "UNAVAILABLE"
        revision = f"{baseline}..HEAD" if baseline not in {"", "UNAVAILABLE"} else "HEAD"

    log = git(root, "log", "--format=%H%x09%s", revision)
    commits: list[tuple[str, str]] = []
    if log.returncode != 0:
        errors.append(f"cannot inspect Git range {revision}: {log.stderr.strip()}")
    else:
        for line in log.stdout.splitlines():
            if "\t" in line:
                commit, subject = line.split("\t", 1)
                commits.append((commit, subject))

    for commit, subject in commits:
        if not args.include_governance_only and not commit_touches_product(root, commit):
            continue
        identifiers = TASK_ID_RE.findall(subject)
        if not identifiers:
            errors.append(f"commit {commit[:12]} lacks a task ID: {subject}")
            continue
        for identifier in identifiers:
            task_path = find_task(tasks, identifier)
            if not task_path:
                errors.append(f"commit {commit[:12]} references missing task {identifier}")
                continue
            audit_paths.add(task_path)
            recorded = HASH_RE.findall(trace_section(task_path.read_text(encoding="utf-8")) or "")
            if not any(commit.startswith(value.lower()) for value in (item.lower() for item in recorded)):
                errors.append(f"{task_path.name} does not link back to commit {commit[:12]}")

    state_path = root / ".ai" / "STATE.md"
    state_text = state_path.read_text(encoding="utf-8") if state_path.exists() else ""
    active = re.search(r"(?ms)^## Active Task\s*\n\s*(\S+)", state_text)
    if active and active.group(1) != "NONE":
        active_path = find_task(tasks, active.group(1))
        if active_path:
            audit_paths.add(active_path)

    paths_to_audit = set(tasks.rglob("*.md")) if args.full else audit_paths
    for task_path in paths_to_audit:
        text = task_path.read_text(encoding="utf-8")
        heading = re.search(r"(?m)^#\s+([^\s]+)", text)
        if not heading:
            errors.append(f"{task_path.name} has no task ID heading")
            continue
        task_id = heading.group(1)
        trace = trace_section(text)
        if trace is None:
            errors.append(f"{task_path.name} lacks Git Traceability section")
            continue
        for commit_hash in HASH_RE.findall(trace):
            shown = git(root, "show", "-s", "--format=%s", commit_hash)
            if shown.returncode != 0:
                errors.append(f"{task_path.name} references unknown commit {commit_hash}")
            elif task_id not in shown.stdout:
                errors.append(f"commit {commit_hash[:12]} does not reference owning task {task_id}")

    status = git(root, "status", "--porcelain")
    product_changes = []
    for line in status.stdout.splitlines():
        path = line[3:].split(" -> ")[-1]
        if path != "AGENTS.md" and not path.startswith(".ai/"):
            product_changes.append(path)
    if product_changes:
        if not active or active.group(1) == "NONE" or not find_task(tasks, active.group(1)):
            errors.append("working tree has product changes without a valid Active Task")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        print(f"Traceability check failed with {len(errors)} error(s).")
        return 1
    print(f"Traceability check passed for {revision}: {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
