from bs4 import BeautifulSoup
import re

def extract_guild_members(page):
    html = page.content()
    soup = BeautifulSoup(html, "html.parser")

    table = soup.find("table")
    if table is None:
        raise RuntimeError("Tableau des membres introuvable (page protégée ou modifiée).")

    rows = table.find_all("tr")[1:]

    members = []

    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 3:
            continue

        link = cols[0].find("a")
        if not link or "href" not in link.attrs:
            continue

        href = link["href"]
        match = re.search(r"id=(\d+)", href)
        if not match:
            continue

        pid = int(match.group(1))
        role = cols[1].get_text(strip=True)
        joined = cols[2].get_text(strip=True)

        members.append({
            "PlayerID": pid,
            "Role": role,
            "Joined": joined,
        })

    return members
