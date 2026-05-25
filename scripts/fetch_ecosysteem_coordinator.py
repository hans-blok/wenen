#!/usr/bin/env python3
"""fetch_ecosysteem_coordinator.py - Copies ecosysteem-coordinator prompts, contracts and tasks
from entoli-agents into this workspace.

Source:
  artefacten/fnd/fnd.01.ecosysteem-coordinator/prompts/*.prompt.md
  artefacten/fnd/fnd.01.ecosysteem-coordinator/agent-contracten/*.agent.md
  artefacten/fnd/fnd.01.ecosysteem-coordinator/tasks/*.tasks.json

Destination:
  .github/prompts/
  .github/agents/
  .vscode/tasks.json

Usage:
    python scripts/fetch_ecosysteem_coordinator.py
    python scripts/fetch_ecosysteem_coordinator.py --source ../entoli-agents --target .
    python scripts/fetch_ecosysteem_coordinator.py --dry-run
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple, TextIO

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
SIBLING_AGENTS = REPO_ROOT.parent / "entoli-agents"

DEFAULT_SOURCE = (
    SIBLING_AGENTS.resolve()
    if (REPO_ROOT.name != "entoli-agents" and SIBLING_AGENTS.exists())
    else REPO_ROOT
)
DEFAULT_TARGET = REPO_ROOT


class TeeWriter:
    """Schrijf output naar zowel console als logbestand."""
    
    def __init__(self, console: TextIO, logfile: TextIO):
        self.console = console
        self.logfile = logfile
    
    def write(self, text: str):
        # Console: replace unicode characters that don't work on Windows cp1252
        try:
            self.console.write(text)
        except UnicodeEncodeError:
            # Fallback: replace problematic characters
            safe_text = text.replace('\u2717', 'x').replace('\u2713', 'v')
            self.console.write(safe_text)
        self.logfile.write(text)
        self.logfile.flush()
    
    def flush(self):
        self.console.flush()
        self.logfile.flush()


def collect_ecosysteem_files(artefacten_root: Path) -> Tuple[List[Tuple[Path, str]], List[Tuple[Path, str]], List[Path]]:
    """Find all prompt, agent and task files for fnd.01.ecosysteem-coordinator.

    Returns (prompts, contracts, task_files) as lists of (src_path, dest_name) and task_files.
    """
    base = artefacten_root / "fnd" / "fnd.01.ecosysteem-coordinator"
    if not base.is_dir():
        raise SystemExit(
            f"ERROR: Directory not found: {base}.\n"
            "Make sure your source points to the entoli-agents repository (with artefacten/fnd/...)."
        )

    prompts_dir = base / "prompts"
    contracts_dir = base / "agent-contracten"
    tasks_dir = base / "tasks"

    prompts: List[Tuple[Path, str]] = []
    contracts: List[Tuple[Path, str]] = []
    task_files: List[Path] = []

    if prompts_dir.is_dir():
        for f in sorted(prompts_dir.glob("*.prompt.md")):
            prompts.append((f, f.name))

    if contracts_dir.is_dir():
        for f in sorted(contracts_dir.glob("*.agent.md")):
            contracts.append((f, f.name))

    if tasks_dir.is_dir():
        for f in sorted(tasks_dir.glob("*.tasks.json")):
            task_files.append(f)

    return prompts, contracts, task_files


def copy_files(
    items: List[Tuple[Path, str]],
    target_dir: Path,
    dry_run: bool,
    label: str,
) -> int:
    """Copy files to target_dir; returns number of copied items."""
    if not items:
        print(f"{label}: (none)")
        return 0

    if not dry_run:
        target_dir.mkdir(parents=True, exist_ok=True)

    count = 0
    for src, name in items:
        dest = target_dir / name
        if dry_run:
            print(f"  [dry] {label}: {src} -> {dest}")
        else:
            shutil.copy2(src, dest)
            print(f"  OK {label}: {src.name} -> {dest}")
        count += 1

    return count


def clean_folder(folder_path: Path, pattern: str, dry_run: bool) -> int:
    """Remove all files in folder matching pattern."""
    if not folder_path.exists():
        return 0
    
    files = list(folder_path.glob(pattern))
    if not files:
        return 0
    
    for f in files:
        if dry_run:
            print(f"  [dry] Remove: {f.name}")
        else:
            f.unlink()
            print(f"  ✗ Removed: {f.name}")
    
    return len(files)


def merge_and_write_tasks(
    task_files: List[Path],
    target_file: Path,
    source_root: Path,
    target_root: Path,
    dry_run: bool,
) -> int:
    """Merge task files and write to tasks.json; returns number of tasks.
    
    Rewrites paths in args so they refer to the source repo relative to the target.
    """
    if not task_files:
        print("Tasks: (none)")
        return 0

    # Calculate relative path from target to source (e.g. ../entoli-agents)
    try:
        rel_source = Path("..") / source_root.name
    except Exception:
        rel_source = source_root

    merged: Dict[str, Any] = {
        "version": "2.0.0",
        "tasks": [],
        "inputs": [],
    }

    task_labels_seen: set = set()
    input_ids_seen: set = set()

    for task_file in task_files:
        try:
            with open(task_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"  ERROR: Invalid JSON in {task_file}: {e}")
            continue

        # Merge tasks
        for task in data.get("tasks", []):
            label = task.get("label", "")
            if label in task_labels_seen:
                print(f"  WARNING: Duplicate task label '{label}', overwritten")
            else:
                task_labels_seen.add(label)
            
            # Rewrite paths in args that start with 'artefacten/'
            if "args" in task:
                new_args = []
                for arg in task["args"]:
                    if isinstance(arg, str) and arg.startswith("artefacten/"):
                        # Add relative source path
                        new_args.append(str(rel_source / arg).replace("\\", "/"))
                    else:
                        new_args.append(arg)
                task["args"] = new_args
            
            # Remove existing task with same label and add new one
            merged["tasks"] = [t for t in merged["tasks"] if t.get("label") != label]
            merged["tasks"].append(task)

        # Merge inputs
        for inp in data.get("inputs", []):
            inp_id = inp.get("id", "")
            if inp_id in input_ids_seen:
                print(f"  WARNING: Duplicate input ID '{inp_id}', overwritten")
            else:
                input_ids_seen.add(inp_id)
            # Remove existing input with same id and add new one
            merged["inputs"] = [i for i in merged["inputs"] if i.get("id") != inp_id]
            merged["inputs"].append(inp)

        print(f"  OK task-source: {task_file.name}")

    if dry_run:
        print(f"  [dry] tasks.json: {len(merged['tasks'])} tasks, {len(merged['inputs'])} inputs -> {target_file}")
    else:
        target_file.parent.mkdir(parents=True, exist_ok=True)
        with open(target_file, "w", encoding="utf-8") as f:
            json.dump(merged, f, indent=2, ensure_ascii=False)
            f.write("\n")
        print(f"  OK tasks.json: {len(merged['tasks'])} tasks, {len(merged['inputs'])} inputs -> {target_file}")

    return len(merged["tasks"])


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Copy ecosysteem-coordinator prompts and contracts from entoli-agents."
    )
    parser.add_argument(
        "--source",
        type=Path,
        default=DEFAULT_SOURCE,
        help=f"Path to entoli-agents (default: {DEFAULT_SOURCE})",
    )
    parser.add_argument(
        "--target",
        type=Path,
        default=DEFAULT_TARGET,
        help=f"Target workspace (default: {DEFAULT_TARGET})",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be copied without writing",
    )
    args = parser.parse_args(argv)

    source_root = args.source.expanduser().resolve()
    target_root = args.target.expanduser().resolve()
    artefacten_root = source_root / "artefacten"

    if not artefacten_root.is_dir():
        parser.error(
            f"artefacten/ directory missing in {source_root}. "
            "Use --source to point to the entoli-agents repo."
        )

    # Setup logging naar /logs
    logs_dir = target_root / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    log_file = logs_dir / f"fetch-ecosysteem-coordinator-{timestamp}.log"
    
    with open(log_file, "w", encoding="utf-8") as logf:
        # Redirect stdout naar TeeWriter
        original_stdout = sys.stdout
        sys.stdout = TeeWriter(original_stdout, logf)
        
        try:
            return _execute_fetch(args, source_root, target_root, artefacten_root, log_file)
        finally:
            sys.stdout = original_stdout


def _execute_fetch(
    args: argparse.Namespace,
    source_root: Path,
    target_root: Path,
    artefacten_root: Path,
    log_file: Path,
) -> int:
    """Execute the actual fetch (with logging active)."""

    print(f"\nFetch ecosysteem-coordinator  |  source: {source_root}  ->  target: {target_root}\n")

    # 1. Clean up existing files
    prompts_dir = target_root / ".github" / "prompts"
    agents_dir = target_root / ".github" / "agents"
    tasks_file = target_root / ".vscode" / "tasks.json"

    print("Cleaning up existing files:")
    n_cleaned = clean_folder(prompts_dir, "*.prompt.md", args.dry_run)
    n_cleaned += clean_folder(agents_dir, "*.agent.md", args.dry_run)
    
    if tasks_file.exists():
        if args.dry_run:
            print(f"  [dry] Remove: {tasks_file}")
        else:
            tasks_file.unlink()
            print(f"  ✗ Removed: {tasks_file}")
        n_cleaned += 1
    
    if n_cleaned == 0:
        print("  (nothing to remove)")
    print()

    # 2. Collect new files
    prompts, contracts, task_files = collect_ecosysteem_files(artefacten_root)

    print(f"Prompts ({len(prompts)}):")
    n_prompts = copy_files(
        prompts, target_root / ".github" / "prompts", args.dry_run, "prompt"
    )

    print(f"\nAgent contracts ({len(contracts)}):")
    n_contracts = copy_files(
        contracts, target_root / ".github" / "agents", args.dry_run, "agent"
    )

    print(f"\nTasks ({len(task_files)} bronbestanden):")
    n_tasks = merge_and_write_tasks(
        task_files, target_root / ".vscode" / "tasks.json", source_root, target_root, args.dry_run
    )

    mode = "[DRY-RUN] " if args.dry_run else ""
    print(f"\n{'-'*60}")
    print(f"{mode}Done for ecosysteem-coordinator (fnd.01)")
    print(f"  Prompts copied  : {n_prompts}")
    print(f"  Agents copied   : {n_contracts}")
    print(f"  Tasks merged    : {n_tasks}")
    print(f"  Log: {log_file.relative_to(target_root)}")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
