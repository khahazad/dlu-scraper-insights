import csv
import os
import re
from datetime import datetime

CSV_PATH = "data/processed/guild_members.csv"

def load_csv():
    if not os.path.exists(CSV_PATH):
        return {}

    data = {}
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            data[int(row["PlayerID"])] = row
    return data


def save_csv(data):
    os.makedirs(os.path.dirname(CSV_PATH), exist_ok=True)
    
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
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", col)
    )

    all_columns = fixed_columns + dynamic_columns

    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=all_columns)
        writer.writeheader()
        for row in data.values():
            writer.writerow(row)

def update_player_info(pid, name, level):
    data = load_csv()
    today = datetime.utcnow().strftime("%Y-%m-%d")

    if pid not in data:
        return

    row = data[pid]

    # Mise à jour du nom
    old_name = row.get("PlayerName", "")
    if old_name and old_name != name:
        prev = row.get("PreviousNames", "")
        if old_name not in prev:
            row["PreviousNames"] = (prev + "," + old_name).strip(",")

    row["PlayerName"] = name

    # Mise à jour du level du jour (pas de nouvelle colonne)
    row[today] = level

    data[pid] = row
    save_csv(data)

