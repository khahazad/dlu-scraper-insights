import csv
import os

CSV_PATH = "data/processed/guild_members.csv"


def load_csv():
    os.makedirs(os.path.dirname(CSV_PATH), exist_ok=True)
    if not os.path.exists(CSV_PATH):
        return {}

    data = {}
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cleaned = {k.strip().replace("\ufeff", ""): v for k, v in row.items()}
            pid = int(cleaned["PlayerID"])
            data[pid] = cleaned
    return data


def save_csv(data):
    columns = [
        "PlayerID",
        "PlayerName",
        "PreviousNames",
        "Role",
        "Joined",
        "Left",
        "PlayerLevel",
    ]

    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        for row in data.values():
            writer.writerow(row)


def update_player_info_in_memory(data, pid, name, level):
    if pid not in data:
        return

    row = data[pid]

    old_name = row.get("PlayerName", "")
    if old_name and old_name != name:
        prev = row.get("PreviousNames", "")
        if old_name not in prev:
            row["PreviousNames"] = (prev + "," + old_name).strip(",")

    row["PlayerName"] = name
    row["PlayerLevel"] = level

    data[pid] = row
