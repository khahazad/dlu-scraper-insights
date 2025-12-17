from playwright.sync_api import Page
from bs4 import BeautifulSoup
import re

def extract_guild_members(page: Page):
    """
    Extrait les membres de la guilde depuis la page guild_members.php.
    Retourne une liste de dicts :
    {
        "player_id": int,
        "role": str,
        "joined_at": str (ISO),
    }
    """

    html = page.content()
    soup = BeautifulSoup(html, "html.parser")

    table = soup.find("table")
    rows = table.find_all("tr")[1:]  # skip header

    members = []

    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 3:
            continue

        # Colonne 1 : lien vers le joueur → player_id
        link = cols[0].find("a")
        href = link["href"]
        match = re.search(r"id=(\d+)", href)
        player_id = int(match.group(1)) if match else None

        # Colonne 2 : rôle
        role = cols[1].get_text(strip=True)

        # Colonne 3 : date de join
        joined_at = cols[2].get_text(strip=True)

        members.append({
            "player_id": player_id,
            "role": role,
            "joined_at": joined_at,
        })

    return members
