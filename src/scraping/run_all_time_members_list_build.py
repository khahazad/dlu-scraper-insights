from storage.save_or_update_csv import save_or_update_csv
from datetime import datetime

def build_all_time_members_list(guild_members, treasury_ledger):
    # 1. Indexation des membres actuels par PlayerID
    guild_index = {m["PlayerID"]: m for m in guild_members}

    # 2. Calcul des dons cumulés + dernière date vue
    donations = {}
    last_donation = {}

    for row in treasury_ledger:
        pid = row["PlayerID"]
        resource = row["Resource"]
        amount = int(row["Amount"])
        time_str = row["Time"]

        # Parse date (format du site : "YYYY-MM-DD HH:MM")
        try:
            time = datetime.strptime(time_str, "%Y-%m-%d %H:%M")
        except:
            # fallback si format différent
            time = time_str

        # Init structures
        if pid not in donations:
            donations[pid] = {"TotalGold": 0, "TotalGems": 0}

        # Cumuls
        if resource.lower() == "gold":
            donations[pid]["TotalGold"] += amount
        elif resource.lower() == "gems":
            donations[pid]["TotalGems"] += amount

        # LastDonation
        if pid not in last_donation or time > last_donation[pid]:
            last_donation[pid] = time

    # 3. Liste complète des PlayerID sans doublons
    all_player_ids = set(guild_index.keys()) | set(donations.keys())

    # 4. Construction du tableau final
    all_time_members_table = []
    for pid in sorted(all_player_ids):
        member_info = guild_index.get(pid, {})

        all_time_members_table.append({
            "PlayerID": pid,
            "Role": member_info.get("Role"),
            "Joined": member_info.get("Joined"),
            "LastDonation": last_donation.get(pid),  # None si jamais vu
            "TotalGold": donations.get(pid, {}).get("TotalGold", 0),
            "TotalGems": donations.get(pid, {}).get("TotalGems", 0)
        })
    
    save_or_update_csv(final_table, "data/processed/all_time_members.csv", key="PlayerID")
    return all_time_members_table
