from playwright.sync_api import sync_playwright
from auth.login import login
from scraping.run_guild_members_extract import extract_guild_members
from scraping.run_weekly_leaderboard_extract import extract_weekly_leaderboard
from scraping.run_treasury_extract import extract_treasury_ledger
from scraping.run_players_info_extract import extract_players_info

def main():
    with sync_playwright() as p:
        try:
            browser, context, page = login(p)

            print("=== Step 1 : Guild members extraction ===")
            extract_guild_members(context)

            print("=== Step 2 : Weekly leaderboard extraction ===")
            extract_weekly_leaderboard(context)
            
            print("=== Step 3 : Treasury ledger extraction ===")
            extract_treasury_ledger(context)
            
            print("=== Étape 2 : Players info extraction (name + levels) ===")
            extract_players_info(context)

        except RuntimeError as e:
            print(f"ERREUR SCRAPER : {e}")
            exit(1)

        finally:
            browser.close()

if __name__ == "__main__":
    main()
