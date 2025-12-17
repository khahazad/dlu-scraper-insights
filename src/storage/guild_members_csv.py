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
            player_id = int(row["player_id"])
            data[player_id] = row
    return data


def save_csv(data):
    os.makedirs("data/processed", exist_ok=True)

    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "player_id",
            "role",
            "joined_at",
            "left_at",
        ])
        writer.writeheader()
        for row in data.values():
            writer.writerow(row)


def merge_members(new_members):
    """
    new_members : liste de dicts venant du scraping
    """

    existing = load_existing()
    now = datetime.utcnow().isoformat()

    new_ids = {m["player_id"] for m in new_members}

    # 1. Mettre à jour ou ajouter les membres actuels
    for m in new_members:
        pid = m["player_id"]

        if pid not in existing:
            # Nouveau membre
            existing[pid] = {
                "player_id": pid,
                "role": m["role"],
                "joined_at": m["joined_at"],
                "left_at": "",
            }
        else:
            # Membre existant → mise à jour du rôle
            existing[pid]["role"] = m["role"]

            # Si le membre était parti → il revient
            if existing[pid]["left_at"]:
                existing[pid]["left_at"] = ""

    # 2. Détecter les départs
    for pid, row in existing.items():
        if pid not in new_ids and not row["left_at"]:
            row["left_at"] = now

    save_csv(existing)
