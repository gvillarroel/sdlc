#!/usr/bin/env python3
"""Generate lightweight SVG charts for the report."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
DEFAULT_OUTPUT = ROOT / "reports" / "assets"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def esc(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def write_rank_stability_chart(output_dir: Path) -> Path:
    rows = read_csv(RESULTS / "rank_stability.csv")[:10]
    width = 960
    row_height = 34
    margin_left = 250
    margin_right = 60
    margin_top = 54
    height = margin_top + len(rows) * row_height + 48
    bar_max = width - margin_left - margin_right

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        '<text x="24" y="32" font-family="Arial, sans-serif" font-size="20" font-weight="700" fill="#111827">Rank stability: mean Monte Carlo top-3 rate</text>',
        '<text x="24" y="52" font-family="Arial, sans-serif" font-size="12" fill="#4b5563">Higher is better. Top 10 candidates by cross-scenario stability.</text>'
    ]
    for index, row in enumerate(rows):
        y = margin_top + index * row_height
        value = float(row["mean_top3_rate"])
        bar_width = value * bar_max
        parts.extend([
            f'<text x="24" y="{y + 21}" font-family="Arial, sans-serif" font-size="13" fill="#111827">{esc(row["alternative"])}</text>',
            f'<rect x="{margin_left}" y="{y + 6}" width="{bar_max}" height="18" rx="3" fill="#e5e7eb"/>',
            f'<rect x="{margin_left}" y="{y + 6}" width="{bar_width:.1f}" height="18" rx="3" fill="#2563eb"/>',
            f'<text x="{margin_left + bar_max + 10}" y="{y + 21}" font-family="Arial, sans-serif" font-size="12" fill="#111827">{value:.2f}</text>'
        ])
    parts.append("</svg>")
    output_path = output_dir / "rank_stability.svg"
    output_path.write_text("\n".join(parts) + "\n", encoding="utf-8", newline="\n")
    return output_path


def write_scenario_regret_chart(output_dir: Path) -> Path:
    rows = [
        row
        for row in read_csv(RESULTS / "regret_analysis.csv")
        if int(row["deterministic_rank"]) <= 3
    ]
    scenarios = []
    for row in rows:
        if row["scenario"] not in scenarios:
            scenarios.append(row["scenario"])

    width = 1080
    row_height = 30
    scenario_gap = 18
    margin_left = 290
    margin_top = 56
    bar_max = 520
    height = margin_top + len(rows) * row_height + len(scenarios) * scenario_gap + 52
    max_regret = max(float(row["regret_vs_best"]) for row in rows) or 1.0

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        '<text x="24" y="32" font-family="Arial, sans-serif" font-size="20" font-weight="700" fill="#111827">Scenario top-3 regret versus winner</text>',
        '<text x="24" y="52" font-family="Arial, sans-serif" font-size="12" fill="#4b5563">Lower is better. Zero means the scenario winner.</text>'
    ]
    y = margin_top
    for scenario in scenarios:
        parts.append(f'<text x="24" y="{y + 18}" font-family="Arial, sans-serif" font-size="14" font-weight="700" fill="#111827">{esc(scenario)}</text>')
        y += scenario_gap
        for row in [r for r in rows if r["scenario"] == scenario]:
            regret = float(row["regret_vs_best"])
            bar_width = 2 if regret == 0 else max(2, regret / max_regret * bar_max)
            color = "#16a34a" if regret == 0 else "#f97316"
            label = f'{row["deterministic_rank"]}. {row["alternative"]}'
            parts.extend([
                f'<text x="44" y="{y + 20}" font-family="Arial, sans-serif" font-size="13" fill="#111827">{esc(label)}</text>',
                f'<rect x="{margin_left}" y="{y + 6}" width="{bar_max}" height="18" rx="3" fill="#f3f4f6"/>',
                f'<rect x="{margin_left}" y="{y + 6}" width="{bar_width:.1f}" height="18" rx="3" fill="{color}"/>',
                f'<text x="{margin_left + bar_max + 10}" y="{y + 20}" font-family="Arial, sans-serif" font-size="12" fill="#111827">{regret:.3f}</text>'
            ])
            y += row_height
    parts.append("</svg>")
    output_path = output_dir / "scenario_regret.svg"
    output_path.write_text("\n".join(parts) + "\n", encoding="utf-8", newline="\n")
    return output_path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    paths = [
        write_rank_stability_chart(args.output_dir),
        write_scenario_regret_chart(args.output_dir)
    ]
    for path in paths:
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
