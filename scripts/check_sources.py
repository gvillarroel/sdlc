#!/usr/bin/env python3
"""Check external source URLs used by the evaluation artifacts."""

from __future__ import annotations

import argparse
import csv
import json
import re
import time
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA = ROOT / "data" / "alternatives.json"
DEFAULT_REPORT = ROOT / "reports" / "ai_orchestrator_frameworks_report.md"
DEFAULT_SOURCE_MATRIX = ROOT / "results" / "market_maintenance_source_matrix.csv"
DEFAULT_OUTPUT = ROOT / "results" / "source_check.csv"
URL_RE = re.compile(r"https?://[^\s)>\]]+")


def collect_urls(
    data_path: Path = DEFAULT_DATA,
    report_path: Path = DEFAULT_REPORT,
    source_matrix_path: Path = DEFAULT_SOURCE_MATRIX,
) -> list[str]:
    urls: set[str] = set()
    raw = json.loads(data_path.read_text(encoding="utf-8"))
    for item in raw["alternatives"]:
        for key in ("url", "homepage"):
            value = item.get(key)
            if value:
                urls.add(value)
        urls.update(item.get("evidence_urls", []))
    for match in URL_RE.findall(report_path.read_text(encoding="utf-8")):
        urls.add(match.rstrip(".,"))
    if source_matrix_path.exists():
        with source_matrix_path.open("r", encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle):
                url = row.get("url", "").strip()
                if url:
                    urls.add(url)
    return sorted(urls)


def check_url(url: str, timeout: float) -> dict[str, Any]:
    started = time.perf_counter()
    request = Request(
        url,
        headers={
            "User-Agent": "sdlc-report-source-check/1.0"
        }
    )
    try:
        with urlopen(request, timeout=timeout) as response:
            response.read(512)
            status = getattr(response, "status", 200)
            final_url = response.geturl()
            error = ""
    except HTTPError as exc:
        status = exc.code
        final_url = exc.geturl()
        error = str(exc.reason)
    except URLError as exc:
        status = ""
        final_url = ""
        error = str(exc.reason)
    except TimeoutError:
        status = ""
        final_url = ""
        error = "timeout"
    elapsed_ms = round((time.perf_counter() - started) * 1000, 1)
    ok = isinstance(status, int) and 200 <= status < 400
    return {
        "url": url,
        "ok": ok,
        "status": status,
        "elapsed_ms": elapsed_ms,
        "final_url": final_url,
        "error": error
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["url", "ok", "status", "elapsed_ms", "final_url", "error"],
            lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--source-matrix", type=Path, default=DEFAULT_SOURCE_MATRIX)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--timeout", type=float, default=15.0)
    args = parser.parse_args()

    rows = [
        check_url(url, args.timeout)
        for url in collect_urls(args.data, args.report, args.source_matrix)
    ]
    write_csv(args.output, rows)
    ok_count = sum(1 for row in rows if row["ok"])
    print(f"checked={len(rows)} ok={ok_count} failed={len(rows) - ok_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
