from bs4 import BeautifulSoup
import re

def extract_player_info(html):
    soup = BeautifulSoup(html, "html.parser")

    # --- Nom du joueur ---
    # Le nom apparaît seul, juste avant "Level X"
    name_tag = soup.find(string=re.compile(r"Level"))
    player_name = None
    if name_tag:
        # Le nom est juste avant ce texte
        prev = name_tag.find_previous(string=True)
        if prev:
            player_name = prev.strip()

    # --- Niveau du joueur ---
    # Plusieurs formats possibles : "LV 29" ou "Level 1"
    level = None

    # Format "LV 29"
    lv_tag = soup.find(string=re.compile(r"LV\s+\d+"))
    if lv_tag:
        level = int(re.search(r"LV\s+(\d+)", lv_tag).group(1))

    # Format "Level 1"
    if level is None:
        lvl_tag = soup.find(string=re.compile(r"Level\s+\d+"))
        if lvl_tag:
            level = int(re.search(r"Level\s+(\d+)", lvl_tag).group(1))

    return {
        "name": player_name,
        "level": level,
    }
