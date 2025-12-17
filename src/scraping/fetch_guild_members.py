from bs4 import BeautifulSoup
import re

def extract_guild_members(page):
    html = page.content()
    soup = BeautifulSoup(html, "html.parser")

    table = soup.find("table")
    rows = table.find_all("tr")[1:]

    members = []

    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 3:
            continue

        link = cols[0].find("a")
        href = link["href"]
        pid = int(re.search(r"id=(\d+)", href).group(1))

        role = cols[1].get_text(strip=True)
        joined = cols[2].get_text(strip=True)

        members.append({
            "player_id": pid,
            "role": role,
            "joined": joined,
        })

    return members
