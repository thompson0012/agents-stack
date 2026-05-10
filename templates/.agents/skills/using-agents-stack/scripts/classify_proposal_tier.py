#!/usr/bin/env python3
"""Standalone CLI for deterministic proposal tier classification.

LLM workers invoke this script to get a mechanical tier classification,
eliminating the non-determinism of manual pattern re-implementation.

Usage:
    python classify_proposal_tier.py .harness/WORKSTREAM-001/sprint_proposal.md
    python classify_proposal_tier.py --symbols '["ValidateToken","HashPassword"]' --hints '["auth/","middleware/"]' --ac-text 'authentication required'
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

# --- Tier signal patterns (synchronized with dispatch_phase.py) -------------
# T3 = critical (schema, migration, auth, encryption, payment, security)
# T1 = light (styles, docs, config, markdown only)

TIER3_SYMBOL_PATTERNS: list[str] = [
    "schema", "migration", "migrate", "backfill",
    "auth", "authenticate", "token", "session", "credential",
    "password", "encrypt", "decrypt", "secret",
    "permission", "authorize", "rbac", "acl",
    "payment", "billing", "invoice", "transaction",
    "oauth", "sso", "certificate", "ssl", "tls", "crypto",
    "csrf", "xss", "sanitize",
    "webhook", "callback",
    "bcrypt", "argon2", "scrypt", "pbkdf2",
]

TIER3_PATH_PATTERNS: list[str] = [
    "prisma/", "migrations/", "migration/",
    "auth/", "middleware/", "guard/",
    "schema/", "database/", "db/",
    "payment/", "billing/",
    "security/", "audit/", "compliance/",
]

TIER3_AC_PATTERNS: list[str] = [
    "data integrity", "authentication", "authorization",
    "api contract", "breaking change", "migration",
    "encryption", "rate limit",
]

TIER1_PATH_PATTERNS: list[str] = [
    "styles/", "css/", "docs/", "public/",
    ".md", ".css", ".json", ".yaml", ".yml", ".toml",
    ".config.", "README",
]

# False-positive guards: these symbols are common data-structure names that
# should NOT trigger T3 even if they contain a T3 pattern substring.
# Guard check: if a symbol name matches BOTH a T3 pattern AND one of these
# broader contexts, it's demoted.
TIER3_GUARD_TERMS: set[str] = {
    "hash",       # too broad: HashTable, HashMap, hashCode
    "role",       # too broad: roleplay, controller, parole
    "token",      # too broad: tokenizeString, tokenizer
    "secret",     # too broad: secretSanta
    "session",    # moderately broad: sessionStorage, sessionId (but keep for auth context)
}


def _is_guarded_match(symbol_name: str, pattern: str) -> bool:
    """Return True if the match is a known false-positive pattern."""
    name_lower = symbol_name.lower()
    if pattern not in TIER3_GUARD_TERMS:
        return False
    if pattern != name_lower and f"_{pattern}" not in name_lower and f"{pattern}_" not in name_lower:
        # Pattern appears as a substring inside a larger word that's not
        # separated by underscores. E.g., "hash" in "HashTable" or "rehash".
        # But "hash" in "password_hash" or "hash_password" is fine.
        return True
    return False


def classify_proposal_tier(
    symbols: list[dict[str, str]] | None = None,
    file_hints: list[str] | None = None,
    acceptance_criteria_text: str = "",
) -> dict[str, Any]:
    """Return tier classification with signal breakdown.

    Returns {"tier": "T1"|"T2"|"T3", "t3_signals": [...], "t1_signals": [...]}
    """
    symbols = symbols or []
    file_hints = file_hints or []
    t3_signals: list[str] = []
    t1_signals: list[str] = []

    # --- Check T3 signals ---
    for sym in symbols:
        name = sym.get("name", "").lower()
        kind = sym.get("kind", "")
        for pattern in TIER3_SYMBOL_PATTERNS:
            if pattern in name:
                if _is_guarded_match(name, pattern):
                    continue
                t3_signals.append(f"symbol:{pattern} in {name} ({kind})")
                break  # one signal per symbol max

    for hint in file_hints:
        hint_lower = hint.lower()
        for pattern in TIER3_PATH_PATTERNS:
            if pattern in hint_lower:
                t3_signals.append(f"path:{pattern} in {hint}")
                break

    ac_lower = acceptance_criteria_text.lower()
    for pattern in TIER3_AC_PATTERNS:
        if pattern in ac_lower:
            t3_signals.append(f"ac:{pattern}")
            break

    # --- Check T1 signals (all files must match light patterns) ---
    all_light = False
    if file_hints:
        all_light = True
        for hint in file_hints:
            hint_lower = hint.lower()
            if not any(p in hint_lower for p in TIER1_PATH_PATTERNS):
                all_light = False
                break
    if all_light:
        t1_signals.append("all_file_hints_match_light_patterns")

    # --- Determine tier ---
    if t3_signals:
        tier = "T3"
    elif all_light and not t3_signals:
        tier = "T1"
    else:
        tier = "T2"

    return {
        "tier": tier,
        "t3_signal_count": len(t3_signals),
        "t3_signals": t3_signals,
        "t1_signals": t1_signals,
        "all_light": all_light,
    }


def extract_from_proposal(proposal_path: Path) -> dict[str, Any]:
    """Extract symbols, file hints, and AC text from a sprint_proposal.md."""
    if not proposal_path.exists():
        return {"error": f"proposal not found: {proposal_path}"}

    text = proposal_path.read_text(encoding="utf-8")

    # Extract task decomposition JSON
    symbols: list[dict[str, str]] = []
    file_hints: list[str] = []
    ac_text = ""

    # Find the Task Decomposition fenced JSON block
    td_match = re.search(
        r'## Task Decomposition\s*\n\s*```(?:json)?\s*\n(.*?)\n\s*```',
        text, re.DOTALL | re.IGNORECASE
    )
    if td_match:
        try:
            td = json.loads(td_match.group(1))
            for task in td.get("tasks", []):
                for sym in task.get("symbols", []):
                    symbols.append({
                        "name": sym.get("name", ""),
                        "kind": sym.get("kind", ""),
                        "signature": sym.get("signature", ""),
                        "file_hint": sym.get("file_hint", ""),
                    })
                for dep in task.get("depends_on", []):
                    pass  # dependencies don't affect tier
        except json.JSONDecodeError:
            pass

    # Extract file hints from task symbols
    for sym in symbols:
        fh = sym.get("file_hint", "")
        if fh:
            file_hints.append(fh)

    # Also look for explicit allowed-files section
    af_match = re.search(
        r'## Allowed Files\s*\n(.*?)(?=\n## |\Z)',
        text, re.DOTALL | re.IGNORECASE
    )
    if af_match:
        for line in af_match.group(1).strip().split("\n"):
            line = line.strip().lstrip("- ").strip()
            if line and not line.startswith("#"):
                file_hints.append(line)

    # Extract acceptance criteria text
    ac_match = re.search(
        r'## Acceptance Criteria\s*\n(.*?)(?=\n## |\Z)',
        text, re.DOTALL | re.IGNORECASE
    )
    if ac_match:
        ac_text = ac_match.group(1)

    return {
        "proposal_path": str(proposal_path),
        "symbols": symbols,
        "file_hints": list(dict.fromkeys(file_hints)),  # deduplicate
        "acceptance_criteria_text": ac_text,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Deterministic proposal tier classification for LLM workers.",
    )
    parser.add_argument(
        "proposal_path",
        nargs="?",
        help="Path to sprint_proposal.md",
    )
    parser.add_argument(
        "--symbols",
        help='JSON array of symbol dicts, e.g. \'[{"name":"Auth"}])\'',
    )
    parser.add_argument(
        "--hints",
        help='JSON array of file hint strings, e.g. \'["auth/","db/"]\'',
    )
    parser.add_argument(
        "--ac-text",
        default="",
        help="Acceptance criteria text as a string",
    )
    parser.add_argument(
        "--json-output",
        action="store_true",
        default=True,
        help="Output JSON (default)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.proposal_path:
        proposal_path = Path(args.proposal_path)
        extracted = extract_from_proposal(proposal_path)
        if "error" in extracted:
            print(json.dumps(extracted, indent=2), file=sys.stderr)
            return 1
        result = classify_proposal_tier(
            symbols=extracted["symbols"],
            file_hints=extracted["file_hints"],
            acceptance_criteria_text=extracted["acceptance_criteria_text"],
        )
        result["proposal_path"] = extracted["proposal_path"]
        result["symbol_count"] = len(extracted["symbols"])
        result["file_hint_count"] = len(extracted["file_hints"])
    elif args.symbols or args.hints:
        symbols = json.loads(args.symbols) if args.symbols else []
        file_hints = json.loads(args.hints) if args.hints else []
        result = classify_proposal_tier(
            symbols=symbols,
            file_hints=file_hints,
            acceptance_criteria_text=args.ac_text,
        )
    else:
        print("Error: provide either proposal_path or --symbols/--hints", file=sys.stderr)
        return 1

    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
