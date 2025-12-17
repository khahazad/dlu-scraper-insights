from bs4 import BeautifulSoup
import re

def extract_player_info(html):
    soup = BeautifulSoup(html, "html.parser")

    # Nom du joueur
    level_tag = soup.find(string=re.compile(r"Level\s+[\d,]+"))
    name = None
    if level_tag:
        prev = level_tag.find_previous(string=True)
        if prev:
            name = prev.strip()

    # Niveau du joueur
    match = re.search(r"Level\s+([\d,]+)", html)
    level = int(match.group(1).replace(",", "")) if match else None

    return {"name": name, "level": level}
