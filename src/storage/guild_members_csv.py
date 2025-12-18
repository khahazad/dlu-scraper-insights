import csv
import os

CSV_PATH = "data/processed/guild_members.csv"

def merge_members(members):
    os.makedirs(os.path.dirname(CSV_PATH), exist_ok=True)
    if not os.path.exists(CSV_PATH):
        with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=members[0].keys())
            writer.writeheader()
            writer.writerows(members)
        return

    existing = {}
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            existing[int(row["PlayerID"])] = row

    for m in members:
        pid = int(m["PlayerID"])
        existing[pid] = m

    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=members[0].keys())
        writer.writeheader()
        writer.writerows(existing.values())
