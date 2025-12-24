from playwright.sync_api import sync_playwright
from auth.login import login
from scraping.run_guild_members_extract import extract_guild_members
from scraping.run_weekly_leaderboard_extract import extract_weekly_leaderboard
from scraping.run_treasury_ledger_extract import extract_treasury_ledger
from scraping.run_all_players_info_extract import extract_all_players_info
from scraping.run_all_time_members_list_build import build_all_time_members_list

def main():
    with sync_playwright() as p:
        try:
            browser, context, page = login(p)

            print("=== Step 1 : Guild members extraction ===")
            guild_members = []
            guild_members = extract_guild_members(context)

            print("=== Step 2 : Treasury ledger extraction ===")
            treasury_ledger = []
            treasury_ledger = extract_treasury_ledger(context)

            print("=== Step 3 : Build all time member list")
            all_time_members_table = build_all_time_members_list(guild_members, treasury_ledger)
            save_or_update_csv(final_table, "storage/all_time_members.csv", key="PlayerID")
            
            print("=== Step 4 : Players info extraction (name + levels) ===")
            extract_all_players_info(browser)
            
            print("=== Step 5 : Weekly leaderboard extraction ===")
            weekly_leaderboard = []
            weekly_leaderboard = extract_weekly_leaderboard(context)
            
        except RuntimeError as e:
            print(f"ERREUR SCRAPER : {e}")
            exit(1)

        finally:
            browser.close()

if __name__ == "__main__":
    main()
