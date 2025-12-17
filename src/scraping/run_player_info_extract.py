from playwright.sync_api import sync_playwright
from auth.login import login
from scraping.fetch_player_info import extract_player_info
from storage.player_info_csv import update_player_info
import csv

def main():
    with sync_playwright() as p:
        # Connexion (JS activé)
        browser, context, page = login(p)

        # Charger la liste des PlayerID depuis le CSV
        with open("data/processed/guild_members.csv", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            player_ids = [int(row["PlayerID"]) for row in reader]

        # Contexte optimisé pour les pages joueur (JS désactivé)
        player_context = browser.new_context(java_script_enabled=False)

        # Bloquer images, CSS, fonts, scripts
        player_context.route("**/*", lambda route, request: (
            route.abort()
            if request.resource_type in ["image", "stylesheet", "font", "script"]
            else route.continue_()
        ))

        player_page = player_context.new_page()

        # Boucle sur chaque joueur
        for pid in player_ids:
            url = f"https://demonicscans.org/player.php?pid={pid}"

            # Chargement ultra rapide (document-only)
            player_page.goto(url, wait_until="domcontentloaded")

            # Extraction nom + niveau
            info = extract_player_info(player_page.content())

            # Mise à jour du CSV
            update_player_info(pid, info["name"], info["level"])

        browser.close()

if __name__ == "__main__":
    main()
