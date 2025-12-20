from bs4 import BeautifulSoup
import re

def extract_weekly_leaderboard(page):
    html = page.content()
    soup = BeautifulSoup(html, "html.parser")

    table = soup.find("table")
    if table is None:
        raise RuntimeError("Weekly Leaderboard table nor found")

    rows = table.find_all("tr")[1:]
    weekly_leaderboard = []

    for row in rows:
        cols = row.find_all("td")
        # 3 raws vailable
        if len(cols) != 3:
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
        # Rank
        rank = cols[1].get_text(strip=True)        
        # Damage
        damage = cols[2].get_text(strip=True)
        
        weekly_leaderboard.append({
            "PlayerID": pid,
            "Rank": rank,
            "Damage": damage
        })

    return weekly_leaderboard
