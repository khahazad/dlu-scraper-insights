from bs4 import BeautifulSoup
import re

def extract_player_info(html):
    soup = BeautifulSoup(html, "html.parser")

    # Nom du joueur dans le <h1>
    h1 = soup.find("h1")    
    if h1 is None:
        raise RuntimeError("Nom du joueur introuvable (page protégée ou modifiée).")
    name = h1.get_text(strip=True) if h1 else None

    # Niveau du joueur : "Level 1,234"
    match = re.search(r"Level\s+([\d,]+)", html)
    level = int(match.group(1).replace(",", "")) if match else None

    return {
        "name": name,
        "level": level,
    }
