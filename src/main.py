import sys
from playwright.sync_api import sync_playwright
from auth.login import login
from scraping.scrape_page_table import scrape_first_table
from scraping.scrape_players_info import scrape_many_players_info
from aggregate_data import aggregate_donations
from aggregate_data import merge_members_and_donations
from aggregate_data import merge_with_player_info

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
                print({
                    "pid": ds["pid"],
                    "gold": ds["gold"],
                    "gems": ds["gems"],
                    "last_donation": ds["last_donation"].strftime("%Y-%m-%d %H:%M:%S")
                })

            # Merging guild members with donations
            print("Merging guild members with donations.")
            merged = merge_members_and_donations(guild_members, donations_summary)
            
            for m in merged[:10]:
                print({
                    "pid": m["pid"],
                    "role": m["role"],
                    "joined": m["joined"],
                    "gold": m["gold"],
                    "gems": m["gems"],
                    "last_donation": (
                        m["last_donation"].strftime("%Y-%m-%d %H:%M:%S")
                        if m["last_donation"] else None
                    )
                })

            
            # Scrape player info (lightweight context)
            print("Scraping player info.")
            pids = [d["pid"] for d in merged]
            players_info = scrape_many_players_info(browser, pids)
            for pi in players_info[:10]: 
                print(pi)


            print("Merging player info.")
            merged = merge_with_player_info(merged, players_info)
            
            for m in merged[:10]:
                print({
                    "pid": m["pid"],
                    "name": m["name"],
                    "level": m["level"],
                    "role": m["role"],
                    "joined": m["joined"],
                    "gold": m["gold"],
                    "gems": m["gems"],
                    "last_donation": (
                        m["last_donation"].strftime("%Y-%m-%d %H:%M:%S")
                        if m["last_donation"] else None
                    )
                })

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
