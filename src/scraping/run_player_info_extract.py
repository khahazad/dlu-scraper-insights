from playwright.sync_api import sync_playwright
from auth.login import login
from scraping.fetch_player_info import extract_player_info
from storage.player_info_csv import load_csv, save_csv, update_player_info_in_memory
import csv


def main():
    with sync_playwright() as p:
        # Connexion (JS activé)
        browser, context, page = login(p)

        # Charger le CSV une seule fois
        data = load_csv()
        
        # LOG : colonnes date AVANT mise à jour
        before = count_date_columns(data)
        print(f"[INFO] Colonnes date AVANT mise à jour : {before}")
        
        # Charger la liste des PlayerID
        player_ids = list(data.keys())

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

            # Chargement rapide (document-only)
            player_page.goto(url, wait_until="domcontentloaded")

            # Extraction nom + level
            info = extract_player_info(player_page.content())

            # Mise à jour en mémoire
            update_player_info_in_memory(data, pid, info["name"], info["level"])

        # LOG : colonnes date APRÈS mise à jour
        after = count_date_columns(data)
        print(f"[INFO] Colonnes date APRÈS mise à jour : {after}")

        # Sauvegarde finale du CSV
        save_csv(data)

        browser.close()


if __name__ == "__main__":
    main()
