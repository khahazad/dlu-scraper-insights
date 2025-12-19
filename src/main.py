from playwright.sync_api import sync_playwright
from auth.login import login
from scraping.run_guild_members_extract import extract_guild_members
from scraping.run_player_info_extract import extract_player_info_all
from scraping.run_treasury_extract import extract_treasury_log

def main():
    with sync_playwright() as p:
        try:
            browser, context, page = login(p)

            print("=== Étape 1 : Extraction des membres de la guilde ===")
            extract_guild_members(context)

            print("=== Étape 2 : Extraction des noms + levels ===")
            extract_player_info_all(browser)

            print("=== Étape 3 : Extraction des dons ===")
            extract_treasury_log(browser)

        except RuntimeError as e:
            print(f"ERREUR SCRAPER : {e}")
            exit(1)

        finally:
            browser.close()

if __name__ == "__main__":
    main()
