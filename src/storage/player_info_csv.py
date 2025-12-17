import csv
import os
from datetime import datetime

CSV_PATH = "data/processed/guild_members.csv"

def load_csv():
    if not os.path.exists(CSV_PATH):
        return {}

    data = {}
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            data[int(row["player_id"])] = row
    return data


def save_csv(data):
    all_columns = set(["player_id", "PlayerName", "PreviousNames", "joined", "left"])
    for row in data.values():
        all_columns.update(row.keys())

    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(all_columns))
        writer.writeheader()
        for row in data.values():
            writer.writerow(row)


def update_player_info(player_id, name, level):
    data = load_csv()
    today = datetime.utcnow().strftime("%Y-%m-%d")

    if player_id not in data:
        return

    row = data[player_id]

    old_name = row.get("PlayerName", "")
    if old_name and old_name != name:
        prev = row.get("PreviousNames", "")
        if name not in prev:
            row["PreviousNames"] = (prev + "," + old_name).strip(",")

    row["PlayerName"] = name
    row[today] = level

    data[player_id] = row
    save_csv(data)
