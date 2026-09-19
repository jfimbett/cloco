#!/usr/bin/env python3
"""
Merge BibTeX entries produced by the academic-librarian into the project's
central bibliography without creating duplicates.

Usage:
    python3 .claude/scripts/merge_bib.py SOURCE.bib [--target paper/references.bib]
                                         [--dry-run]

Rules
- An entry is a duplicate if its cite key already exists in the target, OR its
  DOI matches, OR (normalised title, first-author surname, year) match.
- Duplicates are reported and skipped; the target is never rewritten in place —
  new entries are appended under a dated comment block.
- --dry-run prints what would be added and changes nothing.

Note: paper/references.bib is protected from Write/Edit tool calls by
.claude/hooks/protect-files.py. This script is the sanctioned way to add
entries to it programmatically.
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path

ENTRY_RE = re.compile(r"@(\w+)\s*\{\s*([^,\s]+)\s*,", re.MULTILINE)


def split_entries(text: str) -> list[tuple[str, str, str]]:
    """Return list of (entry_type, key, raw_text) using brace matching."""
    entries = []
    for m in ENTRY_RE.finditer(text):
        start = m.start()
        depth = 0
        i = text.find("{", start)
        while i < len(text):
            ch = text[i]
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    break
            i += 1
        raw = text[start : i + 1]
        entries.append((m.group(1).lower(), m.group(2), raw))
    return entries


def field(raw: str, name: str) -> str:
    m = re.search(name + r"\s*=\s*[{\"]([^}\"]*)[}\"]", raw, re.IGNORECASE)
    return m.group(1).strip() if m else ""


def norm_title(t: str) -> str:
    return re.sub(r"[^a-z0-9]", "", t.lower())


def first_author(raw: str) -> str:
    a = field(raw, "author")
    if not a:
        return ""
    first = a.split(" and ")[0]
    surname = first.split(",")[0] if "," in first else first.split()[-1]
    return re.sub(r"[^a-z]", "", surname.lower())


def signature(raw: str) -> tuple[str, str, str]:
    return (norm_title(field(raw, "title")), first_author(raw), field(raw, "year"))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("source")
    ap.add_argument("--target", default="paper/references.bib")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    src = Path(args.source)
    tgt = Path(args.target)
    if not src.exists():
        sys.stderr.write(f"source not found: {src}\n")
        return 1
    tgt.parent.mkdir(parents=True, exist_ok=True)
    if not tgt.exists():
        tgt.write_text("% Central bibliography — managed by .claude/scripts/merge_bib.py\n\n", encoding="utf-8")

    target_text = tgt.read_text(encoding="utf-8", errors="replace")
    existing = split_entries(target_text)
    keys = {k for _, k, _ in existing}
    dois = {field(r, "doi").lower() for _, _, r in existing if field(r, "doi")}
    sigs = {signature(r) for _, _, r in existing}

    added, skipped = [], []
    for etype, key, raw in split_entries(src.read_text(encoding="utf-8", errors="replace")):
        doi = field(raw, "doi").lower()
        sig = signature(raw)
        if key in keys:
            skipped.append((key, "key exists"))
        elif doi and doi in dois:
            skipped.append((key, f"doi exists ({doi})"))
        elif sig[0] and sig in sigs:
            skipped.append((key, "title/author/year exists"))
        else:
            added.append((key, raw))
            keys.add(key)
            if doi:
                dois.add(doi)
            sigs.add(sig)

    for key, why in skipped:
        print(f"skip  {key:<40} {why}")
    for key, _ in added:
        print(f"add   {key}")
    print(f"\n{len(added)} to add, {len(skipped)} skipped, target now {len(existing) + len(added)} entries")

    if args.dry_run or not added:
        return 0

    block = [f"\n% ---- merged {datetime.now().strftime('%Y-%m-%d %H:%M')} from {src} ----\n"]
    block += [raw.rstrip() + "\n\n" for _, raw in added]
    with tgt.open("a", encoding="utf-8") as fh:
        fh.write("".join(block))
    print(f"appended to {tgt}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
