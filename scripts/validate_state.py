#!/usr/bin/env python3
"""Validate project governance state, references, and context bounds."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


VALID_STATUSES = {"PLANNED", "IN_PROGRESS", "BLOCKED", "VERIFYING", "DONE", "CANCELLED", "IDLE"}
STACK_TYPES = ("EPIC", "TASK", "SUBTASK", "PATCH", "INTERRUPT")
ADR_RE = re.compile(r"\bADR-\d+\b")


def section(text: str, heading: str) -> str | None:
    match = re.search(rf"(?ms)^## {re.escape(heading)}\s*\n(.*?)(?=^## |\Z)", text)
    return match.group(1).strip() if match else None


def field(text: str, name: str) -> str | None:
    match = re.search(rf"(?m)^{re.escape(name)}:\s*(.+?)\s*$", text)
    return match.group(1).strip() if match else None


def referenced_file(folder: Path, identifier: str) -> Path | None:
    matches = [path for path in folder.rglob("*.md") if path.stem == identifier or path.stem.startswith(identifier + "-")]
    return matches[0] if len(matches) == 1 else None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_root", type=Path)
    parser.add_argument("--full", action="store_true", help="Also audit cold task history.")
    args = parser.parse_args()
    root = args.project_root.resolve()
    ai = root / ".ai"
    errors: list[str] = []
    warnings: list[str] = []

    required = [root / "AGENTS.md", ai / "PROJECT.md", ai / "STATE.md", ai / "CHANGE_POLICY.md", ai / "tasks", ai / "decisions"]
    for path in required:
        if not path.exists():
            errors.append(f"missing required path: {path}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    state_path = ai / "STATE.md"
    state = state_path.read_text(encoding="utf-8")
    if len(state.encode("utf-8")) > 12 * 1024:
        errors.append("STATE exceeds the 12 KiB hot-context limit")
    if len(state.splitlines()) > 120:
        errors.append("STATE exceeds the 120-line hot-context limit")

    for heading in ("Project Direction", "Active Work Stack", "Active Task", "Status", "Current Focus", "Last Checkpoint", "Next Action", "Blockers", "Verification"):
        if not section(state, heading):
            errors.append(f"STATE missing or empty section: {heading}")

    status = section(state, "Status")
    if status and status not in VALID_STATUSES:
        errors.append(f"invalid STATE status: {status}")

    stack = section(state, "Active Work Stack") or ""
    stack_ids: list[str] = []
    for kind in STACK_TYPES:
        match = re.search(rf"(?m)^- {kind}:\s*(\S+)", stack)
        if not match:
            errors.append(f"STATE stack missing {kind} entry")
            continue
        value = match.group(1)
        if value != "NONE":
            stack_ids.append(value)
            if kind not in value:
                errors.append(f"stack value {value} does not match frame {kind}")

    active = section(state, "Active Task")
    if status == "IDLE" and active != "NONE":
        errors.append("IDLE state must have Active Task NONE")
    if status != "IDLE" and active == "NONE":
        errors.append("non-IDLE state must name an Active Task")
    if active and active != "NONE" and active not in stack_ids:
        errors.append(f"Active Task {active} is not present in the stack")

    task_files: dict[str, Path] = {}
    stack_entries: list[tuple[str, str]] = []
    for kind in STACK_TYPES:
        match = re.search(rf"(?m)^- {kind}:\s*(\S+)", stack)
        if match and match.group(1) != "NONE":
            stack_entries.append((kind, match.group(1)))

    expected_active = stack_entries[-1][1] if stack_entries else "NONE"
    if active and active != expected_active:
        errors.append(f"Active Task {active} is not the top stack frame {expected_active}")

    for kind, identifier in stack_entries:
        path = referenced_file(ai / "tasks", identifier)
        if not path:
            errors.append(f"stack references missing or ambiguous task: {identifier}")
        else:
            task_files[identifier] = path
            recorded_type = field(path.read_text(encoding="utf-8"), "Type")
            if recorded_type != kind:
                errors.append(f"{path.name} Type {recorded_type} differs from stack frame {kind}")

    if active in task_files:
        active_path = task_files[active]
        task_text = active_path.read_text(encoding="utf-8")
        task_status = field(task_text, "Status")
        if task_status != status:
            errors.append(f"STATE status {status} differs from {active} status {task_status}")
        if len(task_text.encode("utf-8")) > 32 * 1024 or len(task_text.splitlines()) > 300:
            warnings.append(f"active task {active_path.name} is large; compact routine history before the next handoff")

    paths_to_audit = set((ai / "tasks").rglob("*.md")) if args.full else set(task_files.values())
    for task_path in paths_to_audit:
        text = task_path.read_text(encoding="utf-8")
        task_status = field(text, "Status")
        if task_status not in VALID_STATUSES - {"IDLE"}:
            errors.append(f"{task_path.name} has invalid or missing Status")
        if task_status not in {"DONE", "CANCELLED"} and not section(text, "Next Action"):
            errors.append(f"{task_path.name} needs a Next Action")
        dod = section(text, "Definition of Done") or ""
        if task_status == "DONE" and re.search(r"(?m)^\s*- \[ \]", dod):
            errors.append(f"{task_path.name} is DONE with unchecked Definition of Done items")
        for adr in set(ADR_RE.findall(section(text, "Decisions") or "")):
            if not referenced_file(ai / "decisions", adr):
                errors.append(f"{task_path.name} references missing or ambiguous {adr}")

    if re.search(r"\{\{[^}]+\}\}", state):
        errors.append("STATE contains unresolved template markers")

    for warning in warnings:
        print(f"WARNING: {warning}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        print(f"Validation failed with {len(errors)} error(s).")
        return 1
    print(f"State validation passed: {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
