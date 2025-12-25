from datetime import datetime

def collect_all_pids(guild_members, treasury_ledger):
    pids = set()

    # guild_members: keys are PIDs
    for pid in guild_members.keys():
        pids.add(pid)

    # treasury_ledger: values contain PID field
    for row in treasury_ledger.values():
        if "PID" in row:
            pids.add(int(row["PID"]))

    return {pid: {} for pid in sorted(pids)}

from datetime import datetime

def aggregate_donations(treasury_ledger):
    """
    Expected columns inside each row:
    {
        "Time": "...",
        "PID": "12345",
        "Kind": "...",
        "Resource": "...",
        "Amount": "...",
        "Note": "..."
    }

    Returns:
        { pid: { "gold": ..., "gems": ..., "last_donation": datetime(...) } }
    """
    donations = {}

    for entry in treasury_ledger.values():
        time_str = entry["Time"]
        pid = int(entry["PID"])
        resource = entry["Resource"]
        amount_str = entry["Amount"]

        # Convert amount "500,000" → 500000
        amount = int(amount_str.replace(",", ""))

        # Parse timestamp
        ts = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")

        # Initialize PID entry
        if pid not in donations:
            donations[pid] = {
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

    return donations


def update_pid_dict(pids, new_data):
    """
    pids: master dictionary { pid: {...fields...} }
    new_data: dictionary { pid: {...new fields...} }

    Returns the updated pids dictionary.
    """
    for pid, fields in new_data.items():
        if pid not in pids:
            pids[pid] = {}

        # Add or overwrite fields
        for key, value in fields.items():
            pids[pid][key] = value

    return pids

