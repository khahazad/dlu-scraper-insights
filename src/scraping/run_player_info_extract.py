from playwright.sync_api import sync_playwright
from auth.login import login
from scraping.fetch_player_info import extract_player_info
from storage.player_info_csv import update_player_info
import csv

def main():
    with sync_playwright() as p:
        browser, context, page = login(p)

        with open("data/processed/guild_members.csv", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            player_ids = [int(row["player_id"]) for row in reader]

        for pid in player_ids:
            url = f"https://demonicscans.org/player.php?pid={pid}"
            page.goto(url)
            page.wait_for_load_state("networkidle")

            info = extract_player_info(page.content())
            update_player_info(pid, info["name"], info["level"])

        browser.close()

if __name__ == "__main__":
    main()
