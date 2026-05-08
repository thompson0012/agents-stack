#!/usr/bin/env python3
"""List and prune docs/records/ files. Read-only by default; --prune requires --confirm."""

from __future__ import annotations

import argparse
import re
from datetime import datetime, timezone
from pathlib import Path

RECORDS_DIR = Path("docs/records")
VALID_STATUSES = {"informative", "promoted", "superseded", "expired"}
REQUIRED_META = ("workstream_id", "scope", "status")


def resolve_repo_root(raw: str) -> Path:
    return Path(raw).expanduser().resolve()


def extract_metadata(content: str) -> dict[str, str]:
    """Extract metadata fields from the first 500 chars of a record file."""
    meta: dict[str, str] = {}
    for line in content[:500].splitlines():
        for field in ("workstream_id", "scope", "status", "superseded_by"):
            m = re.match(rf"^[-*]\s+{field}:\s*(.*)", line.strip())
            if m:
                meta[field] = m.group(1).strip()
    return meta


def list_records(records_root: Path, repo_root: Path) -> list[dict[str, str]]:
    """Return all records with their metadata, sorted by path."""
    results: list[dict[str, str]] = []
    if not records_root.exists():
        return results
    for file_path in sorted(records_root.rglob("*")):
        if file_path.is_dir() or file_path.name == "README.md":
            continue
        rel = file_path.relative_to(repo_root)
        meta = {"path": str(rel)}
        if file_path.suffix == ".md":
            try:
                meta.update(extract_metadata(file_path.read_text(encoding="utf-8")))
            except Exception:
                pass
        results.append(meta)
    return results


def cmd_list(repo_root: Path) -> int:
    records_root = repo_root / RECORDS_DIR
    records = list_records(records_root, repo_root)
    if not records:
        print("No records found.")
        return 0
    # Column widths
    col_path = max(len(r["path"]) for r in records)
    col_status = max(
        max((len(r.get("status", "-")), len(r.get("scope", "-"))))
        for r in records
    )
    print(f"{'PATH':<{col_path}}  {'STATUS':<12}  {'SCOPE':<{col_status}}  SUPERSEDED_BY")
    print("-" * (col_path + col_status + 50))
    for r in records:
        path = r["path"]
        status = r.get("status", "-")
        scope = r.get("scope", "-")
        sup = r.get("superseded_by", "")
        # Flag issues
        flags = ""
        if status not in VALID_STATUSES:
            flags = " [!INVALID_STATUS]"
        missing = [f for f in REQUIRED_META if f not in r]
        if missing:
            flags = f" [!MISSING:{','.join(missing)}]"
        print(f"{path:<{col_path}}  {status:<12}  {scope:<{col_status}}  {sup}{flags}")
    return 0


def cmd_prune(repo_root: Path, dry_run: bool = True, older_than_days: int = 30) -> int:
    records_root = repo_root / RECORDS_DIR
    records = list_records(records_root, repo_root)
    candidates = [
        r for r in records
        if r.get("status") in ("superseded", "expired")
    ]

    # Filter by age if --older-than-days specified
    if older_than_days > 0:
        cutoff = datetime.now(timezone.utc).timestamp() - (older_than_days * 86400)
        candidates = [
            r for r in candidates
            if not (repo_root / r["path"]).exists()
            or (repo_root / r["path"]).stat().st_mtime < cutoff
        ]

    if not candidates:
        print("No superseded or expired records to prune.")
        return 0

    print(f"Found {len(candidates)} candidate(s) for pruning:\n")
    for r in candidates:
        file_path = repo_root / r["path"]
        age = "unknown"
        if file_path.exists():
            mtime = datetime.fromtimestamp(file_path.stat().st_mtime, tz=timezone.utc)
            age_days = (datetime.now(timezone.utc) - mtime).days
            age = f"{age_days}d ago"
        print(f"  {r['path']}  [{r.get('status')}]  scope={r.get('scope','-')}  mtime={age}")

    if dry_run:
        print(f"\nDry run. Run with --confirm to delete these {len(candidates)} files.")
        return 0

    confirm = input(f"\nDelete {len(candidates)} file(s)? Type 'yes' to confirm: ")
    if confirm.strip().lower() != "yes":
        print("Aborted.")
        return 0

    deleted = 0
    for r in candidates:
        file_path = repo_root / r["path"]
        if file_path.exists():
            file_path.unlink()
            print(f"  Deleted: {r['path']}")
            deleted += 1
    print(f"\nPruned {deleted} record(s).")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Manage docs/records/ lifecycle.")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("list", help="List all records with metadata")

    prune_parser = sub.add_parser("prune", help="Remove superseded/expired records")
    prune_parser.add_argument("--confirm", action="store_true", help="Actually delete (default: dry-run)")
    prune_parser.add_argument(
        "--older-than-days", type=int, default=30,
        help="Only prune records older than N days (default: 30)"
    )

    parser.add_argument(
        "--repo-root", default=".",
        help="Repository root (default: current directory)"
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = resolve_repo_root(args.repo_root)
    if args.command == "list":
        return cmd_list(repo_root)
    elif args.command == "prune":
        return cmd_prune(repo_root, dry_run=not args.confirm, older_than_days=args.older_than_days)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
