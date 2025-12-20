from scraping.fetch_guild_members import fetch_guild_members
from storage.guild_members_csv import merge_members

def extract_guild_members(context):
    page = context.new_page()
    url = "https://demonicscans.org/guild_members.php"
    page.goto(url, wait_until="domcontentloaded")

    members = fetch_guild_members(page)
    merge_members(members)

    page.close()
