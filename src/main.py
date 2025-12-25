import sys
from playwright.sync_api import sync_playwright
from auth.login import login
from scraping.scrape_page_table import scrape_first_table
from scraping.scrape_players_info import scrape_many_players_info

def main():
    with sync_playwright() as pw:
        browser = None
        context = None

        try:
            # -----------------------------------------
            # 1. Login
            # -----------------------------------------
            browser, context = login(pw)

            if context is None or browser is None:
                print("Login failed. Aborting run.")
                return

            # -----------------------------------------
            # 2. Build your list of player IDs
            # -----------------------------------------
            player_ids = [
                90594,
                12345,
                67890,
                # ...
            ]
            url = "https://demonicscans.org/guild_members.php"
            guild_members = scrape_first_table(context, url, 0)
            for gm in guild_members:
                print(gm)

            page_number = 1
            url = f"https://demonicscans.org/guild_treasury_log.php?p={page_number}&res=&kind=donation"       
            treasury_ledger = scrape_first_table(context, url, 1)
            for tl in treasury_ledger:
                print(tl)
                
            # -----------------------------------------
            # 3. Scrape player info (lightweight context)
            # -----------------------------------------
            print("Scraping player info.")
            players = scrape_many_players_info(browser, player_ids)

            # -----------------------------------------
            # 4. Use or store results
            # -----------------------------------------
            for p in players:
                print(p)

        except RuntimeError as e:
            print(f"ERREUR SCRAPER : {e}")
            sys.exit(1)

        finally:
            # -----------------------------------------
            # 5. Clean shutdown
            # -----------------------------------------
            if context:
                context.close()
            if browser:
                browser.close()


if __name__ == "__main__":
    main()
