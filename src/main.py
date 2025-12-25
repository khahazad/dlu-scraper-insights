import sys
from playwright.sync_api import sync_playwright
from auth.login import login
from scraping.scrape_page_table import scrape_first_table
from scraping.scrape_players_info import scrape_many_players_info
from aggregate_data import aggregate_donations

def main():
    with sync_playwright() as pw:
        browser = None
        context = None

        try:
            # Login            
            print("Login.")
            browser, context = login(pw)
            if context is None or browser is None:
                print("Login failed. Aborting run.")
                return
                
            # Scraping guild members info
            print("Scraping guild members info.")
            url = "https://demonicscans.org/guild_members.php"
            guild_members = scrape_first_table(context, url, 0)
            for gm in guild_members[:10]:
                print(gm)

            # Scraping treasury ledger info
            print("Scraping treasury ledger info.")
            page_number = 1
            url = f"https://demonicscans.org/guild_treasury_log.php?p={page_number}&res=&kind=donation"       
            treasury_ledger = scrape_first_table(context, url, 1)
            for tl in treasury_ledger[:10]: 
                print(tl)

            # Aggregating donations
            print("Aggregating donations.")
            donations_summary = aggregate_donations(treasury_ledger)
            for ds in donations_summary[:10]: 
                print(ds)

            # Scrape player info (lightweight context)
            print("Scraping player info.")
            pids = [d["pid"] for d in donations_summary]
            players_info = scrape_many_players_info(browser, pids)
            for pi in players_info[:10]: 
                print(pi)

        except RuntimeError as e:
            print(f"ERREUR SCRAPER : {e}")
            sys.exit(1)

        finally:
            # -----------------------------------------
            # Clean shutdown
            # -----------------------------------------
            if context:
                context.close()
            if browser:
                browser.close()


if __name__ == "__main__":
    main()
