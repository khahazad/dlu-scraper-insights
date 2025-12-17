from playwright.sync_api import sync_playwright
from auth.login import login
from scraping.fetch_guild_members import extract_guild_members
from storage.guild_members_csv import merge_members

def main():
    with sync_playwright() as p:
        browser, context, page = login(p)

        page.goto("https://demonicscans.org/guild_members.php")
        page.wait_for_load_state("networkidle")

        members = extract_guild_members(page)
        merge_members(members)

        browser.close()

if __name__ == "__main__":
    main()
