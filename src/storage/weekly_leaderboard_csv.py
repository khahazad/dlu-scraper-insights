import csv
import os

CSV_PATH = "data/processed/weekly_leaderboard.csv"


def load_leaderboard_rows():
    os.makedirs(os.path.dirname(CSV_PATH), exist_ok=True)
    if not os.path.exists(CSV_PATH):
        return set(), []

    rows = []
    keys = set()

    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            key = (r["PlayerID"], r["Rank"], r["Damage"])
            keys.add(key)
            rows.append(r)

    return keys, rows


def save_csv(rows):
    fieldnames = ["PlayerID", "Rank", "Damage"]

    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
