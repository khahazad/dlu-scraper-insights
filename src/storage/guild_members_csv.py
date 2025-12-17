import csv
import os
from datetime import datetime

CSV_PATH = "data/processed/guild_members.csv"

def load_existing():
    if not os.path.exists(CSV_PATH):
        return {}

    data = {}
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            data[int(row["player_id"])] = row
    return data


def save_csv(data):
    all_columns = set(["player_id", "role", "joined", "left"])
    for row in data.values():
        all_columns.update(row.keys())

    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(all_columns))
        writer.writeheader()
        for row in data.values():
            writer.writerow(row)


def merge_members(new_members):
    existing = load_existing()
    now = datetime.utcnow().isoformat()

    new_ids = {m["player_id"] for m in new_members}

    for m in new_members:
        pid = m["player_id"]

        if pid not in existing:
            existing[pid] = {
                "player_id": pid,
                "role": m["role"],
                "joined": m["joined"],
                "left": "",
            }
        else:
            existing[pid]["role"] = m["role"]
            if existing[pid]["left"]:
                existing[pid]["left"] = ""

    for pid, row in existing.items():
        if pid not in new_ids and not row["left"]:
            row["left"] = now
            row["role"] = ""

    save_csv(existing)
