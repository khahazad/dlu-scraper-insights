from datetime import datetime

def aggregate_donations(rows):
    """
    rows = list of lists from scrape_first_table
    Expected columns:
    [Time, PID, Kind, Resource, Amount, Note]
    """

    # Skip header
    header = rows[0]
    data = rows[1:]

    donations = {}

    for time_str, pid, kind, resource, amount_str, note in data:
        # Convert amount "500,000" → 500000
        amount = int(amount_str.replace(",", ""))

        # Parse timestamp
        ts = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")

        if pid not in donations:
            donations[pid] = {
                "pid": pid,
                "gold": 0,
                "gems": 0,
                "last_donation": ts,
            }

        # Sum by resource type
        if resource.lower() == "gold":
            donations[pid]["gold"] += amount
        elif resource.lower() == "gems":
            donations[pid]["gems"] += amount

        # Update last donation timestamp
        if ts > donations[pid]["last_donation"]:
            donations[pid]["last_donation"] = ts

    return list(donations.values())


def merge_members_and_donations(guild_members, donations_summary):
    """
    guild_members: table from scrape_first_table, with header:
        ['PID', 'Role', 'Joined', 'Contribution']
    donations_summary: list of dicts from aggregate_donations()

    Returns a list of dicts with:
        pid, role, joined, gold, gems, last_donation
    """

    # --- Convert guild members table into a dict by PID ---
    # Skip header row
    members = {}
    for row in guild_members[1:]:
        pid, role, joined, _ = row  # ignore Contribution
        members[pid] = {
            "pid": pid,
            "role": role,
            "joined": joined,
            "gold": 0,
            "gems": 0,
            "last_donation": None,
        }

    # --- Merge donations ---
    for d in donations_summary:
        pid = d["pid"]

        if pid not in members:
            # Donor is no longer a guild member
            members[pid] = {
                "pid": pid,
                "role": "Former",
                "joined": None,
                "gold": d["gold"],
                "gems": d["gems"],
                "last_donation": d["last_donation"],
            }
        else:
            # Update existing guild member
            members[pid]["gold"] = d["gold"]
            members[pid]["gems"] = d["gems"]
            members[pid]["last_donation"] = d["last_donation"]

    # Return as a list
    return list(members.values())

