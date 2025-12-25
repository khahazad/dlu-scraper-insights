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
