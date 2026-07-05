#!/usr/bin/env python3
"""Refresh public GitHub metadata into a generated comparison CSV."""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.simulate_alternatives import DEFAULT_DATA, DEFAULT_RESULTS, write_csv  # noqa: E402

GITHUB_API = "https://api.github.com"


def github_date(value: str | None) -> str:
    if not value:
        return ""
    return datetime.fromisoformat(value.replace("Z", "+00:00")).date().isoformat()


def get_json(url: str, timeout: int) -> tuple[dict[str, Any] | None, str]:
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "sdlc-report-metadata-check",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8")), ""
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return None, "not_found"
        return None, f"http_{exc.code}"
    except urllib.error.URLError as exc:
        return None, str(exc.reason)


def metadata_rows(raw_data: dict[str, Any], timeout: int, sleep_seconds: float) -> list[dict[str, Any]]:
    rows = []
    for item in raw_data["alternatives"]:
        repo = item["repo"]
        repo_payload, repo_error = get_json(f"{GITHUB_API}/repos/{repo}", timeout)
        release_payload, release_error = get_json(f"{GITHUB_API}/repos/{repo}/releases/latest", timeout)
        if sleep_seconds:
            time.sleep(sleep_seconds)

        if repo_payload is None:
            rows.append({
                "alternative_id": item["id"],
                "alternative": item["name"],
                "repo": repo,
                "ok": False,
                "error": repo_error,
                "dataset_stars": item["stars"],
                "live_stars": "",
                "star_delta": "",
                "dataset_last_pushed_at": item["last_pushed_at"],
                "live_last_pushed_at": "",
                "dataset_license": item["license"],
                "live_license": "",
                "license_matches": "",
                "archived": "",
                "latest_release_tag": "",
                "latest_release_error": release_error,
            })
            continue

        live_license = (repo_payload.get("license") or {}).get("spdx_id") or ""
        live_stars = int(repo_payload.get("stargazers_count") or 0)
        latest_release_tag = ""
        if release_payload is not None:
            latest_release_tag = release_payload.get("tag_name") or ""
        rows.append({
            "alternative_id": item["id"],
            "alternative": item["name"],
            "repo": repo,
            "ok": True,
            "error": "",
            "dataset_stars": item["stars"],
            "live_stars": live_stars,
            "star_delta": live_stars - int(item["stars"]),
            "dataset_last_pushed_at": item["last_pushed_at"],
            "live_last_pushed_at": github_date(repo_payload.get("pushed_at")),
            "dataset_license": item["license"],
            "live_license": live_license,
            "license_matches": live_license == item["license"],
            "archived": bool(repo_payload.get("archived")),
            "latest_release_tag": latest_release_tag,
            "latest_release_error": release_error,
        })
    rows.sort(key=lambda row: row["alternative"].lower())
    return rows


def write_metadata_rows(rows: list[dict[str, Any]], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    write_csv(
        output_dir / "github_metadata_check.csv",
        rows,
        [
            "alternative_id",
            "alternative",
            "repo",
            "ok",
            "error",
            "dataset_stars",
            "live_stars",
            "star_delta",
            "dataset_last_pushed_at",
            "live_last_pushed_at",
            "dataset_license",
            "live_license",
            "license_matches",
            "archived",
            "latest_release_tag",
            "latest_release_error",
        ],
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_RESULTS)
    parser.add_argument("--timeout", type=int, default=20)
    parser.add_argument("--sleep", type=float, default=0.0)
    args = parser.parse_args()

    raw_data = json.loads(args.data.read_text(encoding="utf-8"))
    rows = metadata_rows(raw_data, timeout=args.timeout, sleep_seconds=args.sleep)
    write_metadata_rows(rows, args.output_dir)
    failed = [row for row in rows if not row["ok"]]
    mismatched = [
        row
        for row in rows
        if row["ok"] and row["license_matches"] is False
    ]
    print(f"checked {len(rows)} GitHub repos; failed={len(failed)} license_mismatches={len(mismatched)}")
    return 1 if failed or mismatched else 0


if __name__ == "__main__":
    raise SystemExit(main())
