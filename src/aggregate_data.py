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
        {
            pid: {
                "gold": int,
                "gems": int,
                "last_donation": "YYYY-MM-DDTHH:MM:SS"
            }
        }
    """
    donations = {}

    for entry in treasury_ledger.values():
        time_str = entry["Time"]
        pid = int(entry["PID"])
        resource = entry["Resource"]
        amount_str = entry["Amount"]

        # Convert amount "500,000" → 500000
        amount = int(amount_str.replace(",", ""))

        # Parse timestamp from website format
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

    # Convert datetime → "YYYY-MM-DD HH:MM:SS"
    for pid in donations:
        donations[pid]["last_donation"] = donations[pid]["last_donation"].strftime("%Y-%m-%d %H:%M:%S")

    return donations


def update_pid_dict(pids, new_data, fields=None):
    """
    pids: master dictionary { pid: {...fields...} }
    new_data: dictionary { pid: {...new fields...} }
    fields: list of field names to import (None = import all)

    Only updates PIDs that already exist in pids.
    """
    for pid, data_fields in new_data.items():

        # Skip PIDs that are not already in the master dictionary
        if pid not in pids:
            continue

        # Import ALL fields
        if fields is None:
            for key, value in data_fields.items():
                pids[pid][key] = value

        # Import ONLY selected fields
        else:
            for key in fields:
                if key in data_fields:
                    pids[pid][key] = data_fields[key]

    return pids


def serialize_for_json(data):
    """
    Convert all datetime values inside the dictionary to ISO strings.
    Keeps everything else unchanged.
    """
    out = {}

    for pid, fields in data.items():
        out[pid] = {}
        for key, value in fields.items():
            if isinstance(value, datetime):
                out[pid][key] = value.isoformat()
            else:
                out[pid][key] = value

    return out
