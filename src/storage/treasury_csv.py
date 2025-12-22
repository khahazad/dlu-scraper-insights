import csv
import os

CSV_PATH = "data/processed/guild_treasury_log.csv"


def load_treasury_rows():
    os.makedirs(os.path.dirname(CSV_PATH), exist_ok=True)
    if not os.path.exists(CSV_PATH):
        return set(), []

    rows = []
    keys = set()

    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            key = (r["Time"], r["PlayerID"], r["Kind"], r["Resource"], r["Amount"], r["Note"])
            keys.add(key)
            rows.append(r)

    return keys, rows


def save_csv(rows):
    fieldnames = ["Time", "PlayerID", "Kind", "Resource", "Amount", "Note"]

    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
