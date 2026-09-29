#!/usr/bin/env python3
"""Scan deliverable filenames and supported text files for rejected design terms.

Usage:
  python check_terms.py -t "LegacyAuth,trial-component" design.md
  python check_terms.py -f terms.txt design.md docs/
  python check_terms.py -t "LegacyAuth" --root . docs/

Requires Python 3.10+.

Exit codes:
  0: all requested supported text content was scanned with no matches
  1: a match or incomplete scan (missing path, unreadable file, oversized file,
     or no supported text files in the requested scope)
  2: invalid arguments or an unreadable terms file

This is an exact text check, not a semantic or synonym detector.
"""

from __future__ import annotations

import argparse
import codecs
import re
import sys
import unicodedata
from pathlib import Path

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

MAX_FILE_BYTES = 16 * 1024 * 1024
SKIP_DIRS = {
    ".git",
    ".venv",
    "__pycache__",
    ".idea",
    ".vscode",
    "build",
    "dist",
    "node_modules",
}
TEXT_SUFFIXES = frozenset(
    {
        ".adoc",
        ".asciidoc",
        ".bat",
        ".c",
        ".cc",
        ".cpp",
        ".cs",
        ".css",
        ".csv",
        ".drawio",
        ".go",
        ".h",
        ".hpp",
        ".htm",
        ".html",
        ".ini",
        ".java",
        ".js",
        ".json",
        ".jsx",
        ".kt",
        ".kts",
        ".less",
        ".md",
        ".mdx",
        ".mermaid",
        ".mmd",
        ".php",
        ".properties",
        ".ps1",
        ".py",
        ".rb",
        ".rs",
        ".rst",
        ".scss",
        ".sh",
        ".sql",
        ".svg",
        ".tex",
        ".toml",
        ".ts",
        ".tsx",
        ".txt",
        ".xml",
        ".yaml",
        ".yml",
    }
)


def normalize(value: str) -> str:
    return unicodedata.normalize("NFKC", value).casefold()


def load_terms(args: argparse.Namespace) -> list[str]:
    terms: list[str] = []
    if args.terms:
        terms.extend(term.strip() for term in re.split(r"[,，]", args.terms) if term.strip())
    if args.terms_file:
        path = Path(args.terms_file)
        try:
            terms.extend(
                line.strip()
                for line in path.read_text(encoding="utf-8-sig").splitlines()
                if line.strip()
            )
        except (OSError, UnicodeError) as exc:
            print(f"Error: cannot read terms file {path}: {exc}", file=sys.stderr)
            raise SystemExit(2) from exc

    prepared: list[str] = []
    seen: set[str] = set()
    for term in terms:
        normalized = normalize(term)
        if normalized and normalized not in seen:
            seen.add(normalized)
            prepared.append(normalized)
    return prepared


def iter_files(paths: list[str], issues: list[str]):
    for raw_path in paths:
        path = Path(raw_path)
        try:
            if path.is_file():
                yield path.resolve()
                continue
            if not path.is_dir():
                issues.append(f"Path does not exist or is not readable: {path}")
                continue

            for sub in sorted(path.rglob("*")):
                try:
                    if sub.is_file() and not any(
                        part.casefold() in SKIP_DIRS for part in sub.parts
                    ):
                        yield sub.resolve()
                except OSError as exc:
                    issues.append(f"Cannot inspect path {sub}: {exc}")
        except OSError as exc:
            issues.append(f"Cannot access path {path}: {exc}")


def display_path(path: Path, root: Path | None) -> Path:
    if root is not None:
        try:
            return path.relative_to(root)
        except ValueError:
            pass
    return path


def decode_text(data: bytes) -> str:
    if data.startswith((codecs.BOM_UTF32_LE, codecs.BOM_UTF32_BE)):
        return data.decode("utf-32")
    if data.startswith((codecs.BOM_UTF16_LE, codecs.BOM_UTF16_BE)):
        return data.decode("utf-16")
    return data.decode("utf-8-sig")


def check_file(
    path: Path,
    terms: list[str],
    root: Path | None,
    issues: list[str],
) -> tuple[list[str], bool]:
    hits: list[str] = []
    display = display_path(path, root)

    name_norm = normalize(str(display))
    for term in terms:
        if term in name_norm:
            hits.append(f"Filename match [{term}] {display}")

    if path.suffix.casefold() not in TEXT_SUFFIXES:
        return hits, False

    try:
        size = path.stat().st_size
        if size > MAX_FILE_BYTES:
            issues.append(
                f"Skipped oversized file {display} (>{MAX_FILE_BYTES // 1024 // 1024} MiB)"
            )
            return hits, False
        text = decode_text(path.read_bytes())
    except (OSError, UnicodeError) as exc:
        issues.append(f"Could not read text completely {display}: {exc}")
        return hits, False

    for line_no, line in enumerate(text.splitlines(), 1):
        line_norm = normalize(line)
        for term in terms:
            if term in line_norm:
                snippet = line.strip()
                if len(snippet) > 80:
                    snippet = snippet[:77] + "..."
                hits.append(f"{display}:{line_no} [{term}] {snippet}")
    return hits, True


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Scan supported text deliverables for exact rejected-term matches."
    )
    parser.add_argument("-t", "--terms", help="comma-separated terms")
    parser.add_argument("-f", "--terms-file", help="UTF-8 terms file, one term per line")
    parser.add_argument("paths", nargs="+", help="files or directories to scan")
    parser.add_argument("--root", help="root used to display relative paths and scan names")
    args = parser.parse_args()

    terms = load_terms(args)
    if not terms:
        print("Error: provide terms with -t or -f.", file=sys.stderr)
        return 2

    root: Path | None = None
    if args.root:
        root = Path(args.root)
        if not root.is_dir():
            print(f"Error: root is not a readable directory: {root}", file=sys.stderr)
            return 2
        root = root.resolve()

    issues: list[str] = []
    total_hits = 0
    files_seen = 0
    text_files_scanned = 0

    for file_path in iter_files(args.paths, issues):
        files_seen += 1
        hits, content_scanned = check_file(file_path, terms, root, issues)
        total_hits += len(hits)
        text_files_scanned += int(content_scanned)
        for hit in hits:
            print(hit)

    for issue in issues:
        print(f"Incomplete scan: {issue}", file=sys.stderr)

    if total_hits:
        print(f"{total_hits} match(es) found; review each one (substring matches may be false positives).")
    if total_hits or issues:
        return 1
    if files_seen == 0:
        print("Incomplete scan: no files were found in the requested paths.", file=sys.stderr)
        return 1
    if text_files_scanned == 0:
        print("Incomplete scan: no supported text files were scanned.", file=sys.stderr)
        return 1

    print(
        f"Clean: no exact matches for {len(terms)} term(s) in "
        f"{text_files_scanned} text file(s) "
        "(semantic rewrites still require manual review)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
