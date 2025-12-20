from bs4 import BeautifulSoup
import re

def fetch_guild_members(page):
    html = page.content()
    soup = BeautifulSoup(html, "html.parser")

    table = soup.find("table")
    if table is None:
        raise RuntimeError("Members table nor found")

    rows = table.find_all("tr")[1:]
    members = []

    for row in rows:
        cols = row.find_all("td")
        # 4 raws vailable
        if len(cols) != 4:
            raise RuntimeError("Unexpected table format")

        # PlayerID
        link = cols[0].find("a")
        if not link or "href" not in link.attrs:
            raise RuntimeError("No link found")
        href = link["href"]
        match = re.search(r"id=(\d+)", href)
        if not match:
            raise RuntimeError("No match for PID") 
        pid = int(match.group(1))       
        # Role
        role = cols[1].get_text(strip=True)        
        # Joined
        joined = cols[2].get_text(strip=True)
        # Contribution
        contribution = cols[3].get_text(strip=True)
        
        members.append({
            "PlayerID": pid,
            "Role": role,
            "Joined": joined,
            "Contribution": contribution
        })

    return members
