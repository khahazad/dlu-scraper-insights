import sys
from playwright.sync_api import sync_playwright
from auth.login import login
from scraping.scrape_page_table import scrape_first_table
from scraping.scrape_page_table import scrape_paginated_tables
from scraping.scrape_players_info import scrape_players_info
from aggregate_data import collect_all_pids
from aggregate_data import aggregate_donations
from aggregate_data import update_pid_dict
from aggregate_data import serialize_for_json


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
            print(f"### dico size {len(guild_members)}")
            for pid, data in list(guild_members.items())[:5]:
                print(pid, data)

            # Scraping treasury ledger
            print("Scraping treasury ledger info.")
            url_template = "https://demonicscans.org/guild_treasury_log.php?p={page}&res=&kind=donation"
            treasury_ledger = scrape_paginated_tables(context, url_template, 1, "auto")
            # Clean Rank values: remove leading '#'
            for pid, fields in weekly_leaderboard.items():
                if "Rank" in fields and isinstance(fields["Rank"], str):
                    fields["Rank"] = fields["Rank"].lstrip("#")
            print(f"### dico size {len(treasury_ledger)}")
            for key, data in list(treasury_ledger.items())[:5]:
                print(key, data)

            # Scraping weekly leaderboard
            print("Scraping weekly_leaderboard info.")
            url = "https://demonicscans.org/weekly.php"
            weekly_leaderboard = scrape_first_table(context, url, 1, "pid")
            print(f"### dico size {len(weekly_leaderboard)}")
            for pid, data in list(weekly_leaderboard.items())[:5]:
                print(pid, data)
                
            # Collect all PIDs in the main dictionary
            print("Collect all PIDs.")
            delulu_dictionary = collect_all_pids(guild_members,treasury_ledger)
            print(f"### dico size {len(delulu_dictionary)}")
            for pid, data in list(delulu_dictionary.items())[:5]:
                print(pid, data)
            
            # Scrape players names and levels
            print("Scraping players info.")
            pids = list(delulu_dictionary.keys())
            players_info = scrape_players_info(browser, pids)
            print(f"### dico size {len(players_info)}")
            for pid, data in list(players_info.items())[:5]:
                print(pid, data)
            
            # Merging players info with pids_dictionary
            delulu_dictionary = update_pid_dict(delulu_dictionary, players_info)
            
            # Merging guild members with pids_dictionary
            print("Merging guild members with pids_dictionary.")
            delulu_dictionary = update_pid_dict(delulu_dictionary, guild_members, fields=["Role", "Joined"])
            
            # Aggregating donations
            print("Aggregating donations.")
            donations_summary = aggregate_donations(treasury_ledger)
            print(f"### dico size {len(donations_summary)}")
            for pid, data in list(donations_summary.items())[:5]:
                print(pid, data)
            
            # Merging donations with pids
            print("Merging donations with pids_dictionary.")
            delulu_dictionary = update_pid_dict(delulu_dictionary, donations_summary)

            # Merging weekly leaderboard with pids
            print("Merging weekly leaderboard with pids_dictionary.")
            delulu_dictionary = update_pid_dict(delulu_dictionary, weekly_leaderboard, fields=["Rank"])

            
            # Convert datetimes → ISO strings
            clean_data = serialize_for_json(delulu_dictionary)
            
            # Display result
            print("display final delulu_dictionary.")
            print(f"### dico size {len(clean_data)}")
            for pid, data in list(clean_data.items())[:10]:
                print(pid, data)

            # Save to docs/delulu_data.json
            import json
            with open("docs/delulu_data.json", "w", encoding="utf-8") as f:
                json.dump(clean_data, f, indent=2, ensure_ascii=False)
            
            print("Saved JSON to docs/delulu_data.json")

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
