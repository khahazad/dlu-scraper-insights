import csv
import os
import re
from datetime import datetime

CSV_PATH = "data/processed/guild_members.csv"

def load_existing():
    if not os.path.exists(CSV_PATH):
        return {}

    data = {}
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            data[int(row["PlayerID"])] = row
    return data


def save_csv(data):
    fixed_columns = [
        "PlayerID",
        "PlayerName",
        "PreviousNames",
        "Role",
        "Joined",
        "Left",
    ]

    dynamic_columns = sorted(
        col for row in data.values() for col in row.keys()
        if re.match(r"\d{4}-\d{2}-\d{2}", col)
    )

    all_columns = fixed_columns + dynamic_columns

    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=all_columns)
        writer.writeheader()
        for row in data.values():
            writer.writerow(row)


def merge_members(new_members):
    existing = load_existing()
    now = datetime.utcnow().isoformat()

    new_ids = {m["PlayerID"] for m in new_members}

    for m in new_members:
        pid = m["PlayerID"]

        if pid not in existing:
            existing[pid] = {
                "PlayerID": pid,
                "PlayerName": "",
                "PreviousNames": "",
                "Role": m["role"],
                "Joined": m["joined"],
                "Left": "",
            }
        else:
            existing[pid]["Role"] = m["role"]
            if existing[pid]["Left"]:
                existing[pid]["Left"] = ""

    for pid, row in existing.items():
        if pid not in new_ids and not row["Left"]:
            row["Left"] = now
            row["Role"] = ""

    save_csv(existing)
