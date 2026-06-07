from __future__ import annotations

import argparse
import json
from collections.abc import Iterable
from pathlib import Path
from typing import Any

import pandas as pd
import requests


BASE_URL = "https://api.jolpi.ca/ergast/f1"
DEFAULT_YEARS = range(2020, 2025 + 1)
RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")
RESULTS_COLUMNS = [
    "season",
    "round",
    "race_name",
    "event_date",
    "country",
    "location",
    "circuit",
    "driver_id",
    "driver_code",
    "driver_number",
    "driver",
    "constructor",
    "grid",
    "finish_position",
    "classified_position",
    "status",
    "points",
    "podium",
    "points_finish",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download Formula 1 race results into data/raw and data/processed.",
    )
    parser.add_argument(
        "--years",
        type=int,
        nargs="+",
        default=list(DEFAULT_YEARS),
        help="Season years to download.",
    )
    parser.add_argument(
        "--raw-dir",
        type=Path,
        default=RAW_DIR,
        help="Directory for per-season raw JSON and CSV files.",
    )
    parser.add_argument(
        "--processed-dir",
        type=Path,
        default=PROCESSED_DIR,
        help="Directory for the combined processed CSV file.",
    )
    parser.add_argument(
        "--output",
        default="results.csv",
        help="Processed output filename.",
    )
    return parser.parse_args()


def get_json(url: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    return response.json()


def season_payloads(year: int) -> list[dict[str, Any]]:
    url = f"{BASE_URL}/{year}/results.json"
    offset = 0
    payloads: list[dict[str, Any]] = []

    while True:
        payload = get_json(url, {"limit": 100, "offset": offset})
        payloads.append(payload)

        metadata = payload["MRData"]
        offset += int(metadata["limit"])
        if offset >= int(metadata["total"]):
            return payloads


def driver_name(driver: dict[str, Any]) -> str:
    given_name = driver.get("givenName", "")
    family_name = driver.get("familyName", "")
    return f"{given_name} {family_name}".strip()


def int_or_none(value: Any) -> int | None:
    if value in (None, ""):
        return None
    try:
        return int(value)
    except ValueError:
        return None


def float_or_zero(value: Any) -> float:
    if value in (None, ""):
        return 0.0
    return float(value)


def parse_payloads(year: int, payloads: list[dict[str, Any]]) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []

    for payload in payloads:
        races = payload["MRData"]["RaceTable"].get("Races", [])

        for race in races:
            circuit = race.get("Circuit", {})
            circuit_location = circuit.get("Location", {})
            round_number = int(race["round"])

            for result in race.get("Results", []):
                driver = result.get("Driver", {})
                constructor = result.get("Constructor", {})
                finish_position = int_or_none(result.get("position"))
                points = float_or_zero(result.get("points"))

                rows.append(
                    {
                        "season": year,
                        "round": round_number,
                        "race_name": race.get("raceName"),
                        "event_date": race.get("date"),
                        "country": circuit_location.get("country"),
                        "location": circuit_location.get("locality"),
                        "circuit": circuit.get("circuitName"),
                        "driver_id": driver.get("driverId"),
                        "driver_code": driver.get("code"),
                        "driver_number": int_or_none(result.get("number")),
                        "driver": driver_name(driver),
                        "constructor": constructor.get("name"),
                        "grid": int_or_none(result.get("grid")),
                        "finish_position": finish_position,
                        "classified_position": result.get("positionText"),
                        "status": result.get("status"),
                        "points": points,
                        "podium": int(
                            finish_position is not None and finish_position <= 3
                        ),
                        "points_finish": int(points > 0),
                    }
                )

    return pd.DataFrame(rows, columns=RESULTS_COLUMNS)


def write_raw_payloads(
    year: int, payloads: list[dict[str, Any]], raw_dir: Path
) -> None:
    raw_dir.mkdir(parents=True, exist_ok=True)
    output_path = raw_dir / f"results_{year}.json"
    output_path.write_text(json.dumps(payloads, indent=2), encoding="utf-8")


def write_raw_results(year: int, frame: pd.DataFrame, raw_dir: Path) -> None:
    raw_dir.mkdir(parents=True, exist_ok=True)
    output_path = raw_dir / f"results_{year}.csv"
    frame.to_csv(output_path, index=False)
    print(f"Wrote {len(frame)} rows to {output_path}")


def download_years(years: Iterable[int], raw_dir: Path) -> list[pd.DataFrame]:
    frames: list[pd.DataFrame] = []

    for year in years:
        print(f"Loading {year} race results")
        payloads = season_payloads(year)
        frame = parse_payloads(year, payloads)
        write_raw_payloads(year, payloads, raw_dir)
        write_raw_results(year, frame, raw_dir)
        frames.append(frame)

    return frames


def write_processed_results(frames: list[pd.DataFrame], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if frames:
        results = pd.concat(frames, ignore_index=True)
    else:
        results = pd.DataFrame(columns=RESULTS_COLUMNS)

    results = results.sort_values(["season", "round", "finish_position", "driver"])
    results.to_csv(output_path, index=False)
    print(f"Wrote {len(results)} rows to {output_path}")


def main() -> None:
    args = parse_args()
    frames = download_years(args.years, args.raw_dir)
    write_processed_results(frames, args.processed_dir / args.output)


if __name__ == "__main__":
    main()
