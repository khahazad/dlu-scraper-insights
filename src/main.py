import sys
from playwright.sync_api import sync_playwright
from auth.login import login
from scraping.scrape_page_table import scrape_first_table
from scraping.scrape_players_info import scrape_players_info
from aggregate_data import aggregate_donations
from aggregate_data import update_pid_dict

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
                
            # Scraping guild members
            print("Scraping guild members info.")
            url = "https://demonicscans.org/guild_members.php"
            guild_members = scrape_first_table(context, url, 0, "pid")
            for pid, data in list(guild_members.items())[:5]:
                print(pid, data)

            # Scraping treasury ledger
            print("Scraping treasury ledger info.")
            page_number = 1
            url = f"https://demonicscans.org/guild_treasury_log.php?p={page_number}&res=&kind=donation"       
            treasury_ledger = scrape_first_table(context, url, 1, "auto")
            for pid, data in list(treasury_ledger.items())[:5]:
                print(pid, data)

            # Scraping weekly leaderboard
            print("Scraping weekly_leaderboard info.")
            url = "https://demonicscans.org/weekly.php"
            weekly_leaderboard = scrape_first_table(context, url, 0, "pid")
            for pid, data in list(weekly_leaderboard.items())[:5]:
                print(pid, data)
                
            # Collect all PIDs in the main dictionary
            print("Collect all PIDs.")
            delulu_dictionary = collect_all_pids(guild_members,treasury_ledger)
            
            # Scrape players names and levels
            print("Scraping players info.")
            pids = list(delulu_dictionary.keys())
            players_info = scrape_players_info(browser, pids)
            
            # Merging players info with pids_dictionary
            delulu_dictionary = update_pid_dict(delulu_dictionary, players_info)
            
            # Merging guild members with pids_dictionary
            print("Merging guild members with pids_dictionary.")
            delulu_dictionary = update_pid_dict(delulu_dictionary, guild_members)
            
            # Aggregating donations
            print("Aggregating donations.")
            donations_summary = aggregate_donations(treasury_ledger)
            
            # Merging donations with pids
            print("Merging donations with pids_dictionary.")
            delulu_dictionary = update_pid_dict(delulu_dictionary, donations_summary)

            # Merging weekly leaderboard with pids
            print("Merging weekly leaderboard with pids_dictionary.")
            delulu_dictionary = update_pid_dict(delulu_dictionary, weekly_leaderboard)
            
            # Display 10 first rows in log with dates formated
            for pd in delulu_dictionary[:10]:
                #  print({ ??? })

        
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
