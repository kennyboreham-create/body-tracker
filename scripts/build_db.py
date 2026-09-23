#!/usr/bin/env python3
"""Rebuild data/app.db from foods.json, workouts.json, and workouttooltip.json."""
from __future__ import annotations

import json
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "data" / "app.db"


def load_json(name: str):
    with open(ROOT / name, encoding="utf-8") as f:
        return json.load(f)


def main() -> None:
    foods = load_json("foods.json")
    workouts = load_json("workouts.json")
    tooltips = load_json("workouttooltip.json")

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    if DB_PATH.exists():
        DB_PATH.unlink()

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript(
        """
        CREATE TABLE foods (
            category TEXT NOT NULL,
            id TEXT NOT NULL,
            name TEXT,
            portion TEXT,
            calories REAL,
            protein REAL,
            PRIMARY KEY (category, id)
        );
        CREATE TABLE workout_days (
            day_key TEXT PRIMARY KEY,
            title TEXT
        );
        CREATE TABLE workout_exercises (
            day_key TEXT NOT NULL,
            id TEXT NOT NULL,
            name TEXT,
            sets TEXT,
            est_burn REAL,
            sort_order INTEGER,
            PRIMARY KEY (day_key, id)
        );
        CREATE TABLE workout_tooltips (
            id TEXT PRIMARY KEY,
            name TEXT,
            how_to TEXT,
            sets TEXT,
            est_burn REAL,
            section_key TEXT,
            extra_json TEXT
        );
        """
    )

    food_rows = []
    for category, items in foods.items():
        if not isinstance(items, list):
            continue
        for item in items:
            food_rows.append(
                (
                    category,
                    item.get("id"),
                    item.get("name"),
                    item.get("portion"),
                    item.get("calories"),
                    item.get("protein"),
                )
            )
    cur.executemany(
        "INSERT INTO foods(category, id, name, portion, calories, protein) VALUES (?,?,?,?,?,?)",
        food_rows,
    )

    for day_key, day in workouts.items():
        cur.execute(
            "INSERT INTO workout_days(day_key, title) VALUES (?, ?)",
            (day_key, day.get("title")),
        )
        for sort_order, ex in enumerate(day.get("exercises") or []):
            cur.execute(
                """
                INSERT INTO workout_exercises(day_key, id, name, sets, est_burn, sort_order)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    day_key,
                    ex.get("id"),
                    ex.get("name"),
                    ex.get("sets"),
                    ex.get("estBurn"),
                    sort_order,
                ),
            )

    # workouttooltip.json is nested under section keys (e.g. "Descriptons")
    for section_key, section in tooltips.items():
        if not isinstance(section, dict):
            continue
        for ex in section.get("exercises") or []:
            known = {"id", "name", "How To", "how_to", "howTo", "sets", "estBurn"}
            extra = {k: v for k, v in ex.items() if k not in known}
            how_to = ex.get("How To") or ex.get("how_to") or ex.get("howTo")
            cur.execute(
                """
                INSERT OR REPLACE INTO workout_tooltips
                    (id, name, how_to, sets, est_burn, section_key, extra_json)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    ex.get("id"),
                    ex.get("name"),
                    how_to,
                    ex.get("sets"),
                    ex.get("estBurn"),
                    section_key,
                    json.dumps(extra) if extra else None,
                ),
            )

    conn.commit()

    counts = {
        "foods": cur.execute("SELECT COUNT(*) FROM foods").fetchone()[0],
        "workout_days": cur.execute("SELECT COUNT(*) FROM workout_days").fetchone()[0],
        "workout_exercises": cur.execute("SELECT COUNT(*) FROM workout_exercises").fetchone()[0],
        "workout_tooltips": cur.execute("SELECT COUNT(*) FROM workout_tooltips").fetchone()[0],
    }
    conn.close()
    print(f"Wrote {DB_PATH}")
    for k, v in counts.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
