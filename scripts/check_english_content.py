#!/usr/bin/env python3
"""Detect likely Spanish prose in repository-authored text files.

The check is intentionally conservative. It looks for multiple Spanish language
markers on a prose line or a small set of high-confidence phrases. URLs and
technical identifiers are sanitized, while lockfiles, vendored trees, and
non-text artifacts (including generated binary assets) are excluded.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import os
from pathlib import Path
import re
import subprocess
import unicodedata


ROOT = Path(__file__).resolve().parents[1]

TEXT_SUFFIXES = {
    ".adoc",
    ".bash",
    ".cfg",
    ".cjs",
    ".conf",
    ".css",
    ".csv",
    ".htm",
    ".html",
    ".ini",
    ".js",
    ".json",
    ".jsonl",
    ".jsx",
    ".md",
    ".mjs",
    ".mmd",
    ".ps1",
    ".py",
    ".rst",
    ".scss",
    ".sh",
    ".toml",
    ".ts",
    ".tsv",
    ".tsx",
    ".txt",
    ".yaml",
    ".yml",
    ".zsh",
}

TEXT_FILENAMES = {
    ".editorconfig",
    ".gitattributes",
    ".gitignore",
    "copying",
    "dockerfile",
    "license",
    "makefile",
    "notice",
}

EXCLUDED_DIRECTORY_NAMES = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "__pycache__",
    "build",
    "coverage",
    "dist",
    "node_modules",
    "third_party",
    "vendor",
    "venv",
}

EXCLUDED_FILENAMES = {
    "bun.lock",
    "bun.lockb",
    "composer.lock",
    "package-lock.json",
    "pipfile.lock",
    "pnpm-lock.yaml",
    "poetry.lock",
    "yarn.lock",
}

def decode_words(hex_value: str) -> frozenset[str]:
    """Decode detector data while keeping non-English tokens out of source prose."""
    return frozenset(bytes.fromhex(hex_value).decode("ascii").split())


SPANISH_FUNCTION_WORDS = decode_words(
    "616c20616e7465732061756e717565206361646120636f6d6f20636f6e206375616e646f206465626520"
    "646562656e2064656c2064656e74726f206465736465206465737075657320646f6e646520656c20657374"
    "612065737461732065737465206573746f73206861737461206c61206c6173206c6f73206d69656e747261"
    "73206e696e67756e206e696e67756e612070617261207065726f20706f7271756520706f72207075656465"
    "2070756564656e207175652073696e2074616d6269656e20746f64617320746f646f7320756e20756e6120"
    "756e617320756e6f20756e6f73"
)

SPANISH_CONTENT_WORDS = decode_words(
    "61637475616c697a61206167656e7465206167656e74657320616e7469677561732061706c69636163696f"
    "6e2061706c69636163696f6e6573206172636869766f206172636869766f7320617369676e612063616465"
    "6e6120636f6469676f20636f6d7061726163696f6e20636f6e66696775726163696f6e20636f6e66696775"
    "726163696f6e657320636f6e636c7573696f6e20636f6e6669616e7a612063726561206372656172206465"
    "6d7565737472612064696e616d69636f2064696e616d69636f73206469726563746f72696f206469726563"
    "746f72696f7320646973656e6120656e746f726e6f20656e746f726e6f7320657363726974757261206573"
    "63726974757261732065737472756374757261206576616c756163696f6e206576616c756163696f6e6573"
    "2065766964656e63696120656a656375746120656a65637563696f6e20657874656e73696f6e6573206675"
    "656e7465206675656e7465732067656e6572612068657272616d69656e74612068657272616d69656e7461"
    "7320696e666f726d6520696e666f726d657320696e7465726e6f20696e7465726e6120696e7465726e6f73"
    "20696e7465726e617320696e766f636163696f6e206c656374757261206c65637475726173206d65746f64"
    "6f6c6f676961206d6f64656c6f206d6f64656c6f73206e6f6d627265206e6f6d62726573206f626a6574"
    "69766f206f66696369616c6573206f7267616e697a6163696f6e206f7267616e697a6163696f6e65732070"
    "61736f207061736f73207065726d69736f207065726d69736f732070726163746963612070727565626120"
    "70727565626173207265636f6d656e646163696f6e207265706f727465207265706f727465732072657175"
    "697369746f2072657175697369746f7320726573756c7461646f20726573756c7461646f73207265766973"
    "696f6e2072696573676f2072696573676f7320727574612072757461732073656775726964616420736567"
    "75726f2073656c656363696f6e20746172656120746172656173207573756172696f207573756172696f73"
    "207574696c2076616c69646163696f6e207665726966696361207669737461"
)

SPANISH_MARKERS = SPANISH_FUNCTION_WORDS | SPANISH_CONTENT_WORDS

def compile_phrase(hex_value: str) -> re.Pattern[str]:
    words = bytes.fromhex(hex_value).decode("ascii").split()
    return re.compile(r"\b" + r"\s+".join(re.escape(word) for word in words) + r"\b")


HIGH_CONFIDENCE_PHRASES = tuple(
    compile_phrase(value)
    for value in (
        "7265706f7274652066696e616c",
        "7265706f7274652066696e616c20676c6f62616c",
        "766973746120676c6f62616c",
        "7175652064656d756573747261",
        "6c656374757261207072696f72697461726961",
        "7265636f6d656e646163696f6e207072616374696361",
    )
)

URL_RE = re.compile(r"(?:https?|ftp)://[^\s<>\])}]+|\bwww\.[^\s<>\])}]+", re.IGNORECASE)
EMAIL_RE = re.compile(r"\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b")
INLINE_CODE_RE = re.compile(r"`+[^`]*`+")
HTML_TAG_RE = re.compile(r"<[^>]+>")
QUOTED_IDENTIFIER_RE = re.compile(r"([\"'])(?:[A-Za-z][A-Za-z0-9_.:/-]{0,60})\1")
TECHNICAL_IDENTIFIER_RE = re.compile(
    r"(?<![\w])[@$]?[A-Za-z][A-Za-z0-9]*"
    r"(?:[_.:/\\-][A-Za-z0-9][A-Za-z0-9_.:/\\-]*)+(?![\w])"
)
CLI_OPTION_RE = re.compile(r"(?<!\w)--?[A-Za-z][A-Za-z0-9-]*")
HASH_RE = re.compile(r"\b(?:[0-9a-f]{16,}|[A-Za-z0-9+/]{40,}={0,2})\b", re.IGNORECASE)
TOKEN_RE = re.compile(r"[^\W\d_]+", re.UNICODE)
MARKDOWN_HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s+")
HTML_HEADING_RE = re.compile(r"^\s*<h[1-6]\b", re.IGNORECASE)


@dataclass(frozen=True)
class Finding:
    path: Path
    line_number: int
    reason: str
    markers: tuple[str, ...]
    excerpt: str


@dataclass(frozen=True)
class ScanResult:
    scanned_files: int
    skipped_files: int
    findings: tuple[Finding, ...]


def normalize_for_matching(value: str) -> str:
    decomposed = unicodedata.normalize("NFKD", value.casefold())
    return "".join(character for character in decomposed if not unicodedata.combining(character))


def sanitize_line(line: str) -> str:
    sanitized = URL_RE.sub(" ", line)
    sanitized = EMAIL_RE.sub(" ", sanitized)
    sanitized = INLINE_CODE_RE.sub(" ", sanitized)
    sanitized = HTML_TAG_RE.sub(" ", sanitized)
    sanitized = QUOTED_IDENTIFIER_RE.sub(" ", sanitized)
    sanitized = TECHNICAL_IDENTIFIER_RE.sub(" ", sanitized)
    sanitized = CLI_OPTION_RE.sub(" ", sanitized)
    return HASH_RE.sub(" ", sanitized)


def analyze_line(path: Path, line_number: int, line: str) -> Finding | None:
    is_heading = bool(MARKDOWN_HEADING_RE.match(line) or HTML_HEADING_RE.match(line))
    sanitized = sanitize_line(line)
    normalized = normalize_for_matching(sanitized)

    for phrase in HIGH_CONFIDENCE_PHRASES:
        if phrase.search(normalized):
            return Finding(
                path=path,
                line_number=line_number,
                reason="high-confidence Spanish phrase",
                markers=tuple(phrase.findall(normalized)),
                excerpt=line.strip()[:200],
            )

    tokens = TOKEN_RE.findall(normalized)
    if not tokens:
        return None

    markers = [token for token in tokens if token in SPANISH_MARKERS]
    strong_markers = [token for token in markers if token in SPANISH_CONTENT_WORDS]
    unique_markers = tuple(sorted(set(markers)))
    marker_density = len(markers) / len(tokens)

    if "\u00bf" in line or "\u00a1" in line:
        reason = "Spanish sentence punctuation"
    elif is_heading and strong_markers:
        reason = "Spanish heading marker"
    elif len(tokens) <= 6 and len(strong_markers) >= 2 and marker_density >= 0.33:
        reason = "multiple Spanish content markers"
    elif len(markers) >= 3 and strong_markers and marker_density >= 0.16:
        reason = "Spanish prose marker density"
    elif len(markers) >= 4 and marker_density >= 0.20:
        reason = "Spanish function-word density"
    else:
        return None

    return Finding(
        path=path,
        line_number=line_number,
        reason=reason,
        markers=unique_markers,
        excerpt=line.strip()[:200],
    )


def is_repository_text_path(path: Path) -> bool:
    lowered_parts = {part.casefold() for part in path.parts}
    if lowered_parts.intersection(EXCLUDED_DIRECTORY_NAMES):
        return False

    name = path.name.casefold()
    if name in EXCLUDED_FILENAMES:
        return False
    if name.endswith((".min.js", ".min.css")):
        return False
    return path.suffix.casefold() in TEXT_SUFFIXES or name in TEXT_FILENAMES


def repository_files(root: Path = ROOT) -> list[Path]:
    completed = subprocess.run(
        [
            "git",
            "-C",
            str(root),
            "ls-files",
            "--cached",
            "--others",
            "--exclude-standard",
            "-z",
        ],
        check=True,
        capture_output=True,
    )
    relative_paths = [os.fsdecode(item) for item in completed.stdout.split(b"\0") if item]
    return [root / relative for relative in relative_paths if (root / relative).is_file()]


def scan_file(path: Path, display_path: Path | None = None) -> tuple[list[Finding], bool]:
    if not is_repository_text_path(display_path or path):
        return [], False

    raw = path.read_bytes()
    if b"\0" in raw:
        return [], False
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        return [], False

    findings = []
    finding_path = display_path or path
    for line_number, line in enumerate(text.splitlines(), start=1):
        finding = analyze_line(finding_path, line_number, line)
        if finding is not None:
            findings.append(finding)
    return findings, True


def scan_paths(paths: list[Path], root: Path = ROOT) -> ScanResult:
    findings: list[Finding] = []
    scanned_files = 0
    skipped_files = 0

    for path in paths:
        resolved = path if path.is_absolute() else root / path
        try:
            display_path = resolved.relative_to(root)
        except ValueError:
            display_path = resolved
        file_findings, scanned = scan_file(resolved, display_path)
        if scanned:
            scanned_files += 1
            findings.extend(file_findings)
        else:
            skipped_files += 1

    findings.sort(key=lambda item: (item.path.as_posix(), item.line_number))
    return ScanResult(scanned_files, skipped_files, tuple(findings))


def expand_explicit_paths(paths: list[Path], root: Path) -> list[Path]:
    expanded: list[Path] = []
    for path in paths:
        resolved = path if path.is_absolute() else root / path
        if resolved.is_dir():
            expanded.extend(candidate for candidate in resolved.rglob("*") if candidate.is_file())
        else:
            expanded.append(resolved)
    return sorted(set(expanded), key=lambda item: item.as_posix())


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check repository-authored tracked text for likely Spanish prose."
    )
    parser.add_argument("paths", nargs="*", type=Path, help="Optional files or directories to scan.")
    parser.add_argument("--root", type=Path, default=ROOT, help="Repository root.")
    parser.add_argument("--max-findings", type=int, default=50, help="Maximum findings to print.")
    args = parser.parse_args()

    root = args.root.resolve()
    paths = expand_explicit_paths(args.paths, root) if args.paths else repository_files(root)
    result = scan_paths(paths, root)

    if result.findings:
        print(
            f"English-content check failed: {len(result.findings)} suspicious line(s) "
            f"in {result.scanned_files} scanned text file(s)."
        )
        for finding in result.findings[: args.max_findings]:
            marker_text = ", ".join(finding.markers) or "punctuation"
            print(
                f"{finding.path.as_posix()}:{finding.line_number}: {finding.reason} "
                f"[{marker_text}]"
            )
            print(f"  {finding.excerpt}")
        hidden = len(result.findings) - args.max_findings
        if hidden > 0:
            print(f"... {hidden} additional finding(s) omitted")
        return 1

    print(
        f"English-content check passed: {result.scanned_files} text file(s) scanned; "
        f"{result.skipped_files} non-text or excluded file(s) skipped."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
