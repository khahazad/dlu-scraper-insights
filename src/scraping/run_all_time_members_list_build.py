def build_all_time_members_list(guild_members, treasury_ledger):
    # 1. Indexation des membres actuels par PlayerID
    guild_index = {m["PlayerID"]: m for m in guild_members}

    # 2. Calcul des dons cumulés par PlayerID
    donations = {}
    for row in treasury_ledger:
        pid = row["PlayerID"]
        resource = row["Resource"]
        amount = int(row["Amount"])

        if pid not in donations:
            donations[pid] = {"TotalGold": 0, "TotalGems": 0}

        if resource.lower() == "gold":
            donations[pid]["TotalGold"] += amount
        elif resource.lower() == "gems":
            donations[pid]["TotalGems"] += amount

    # 3. Liste complète des PlayerID sans doublons
    all_player_ids = set(guild_index.keys()) | set(donations.keys())

    # 4. Construction du tableau final
    final_table = []
    for pid in sorted(all_player_ids):
        member_info = guild_index.get(pid, {})

        final_table.append({
            "PlayerID": pid,
            "Role": member_info.get("Role"),
            "Joined": member_info.get("Joined"),
            "TotalGold": donations.get(pid, {}).get("TotalGold", 0),
            "TotalGems": donations.get(pid, {}).get("TotalGems", 0),
        })

    return final_table
