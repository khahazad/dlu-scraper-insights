from scraping.fetch_guild_members import extract_guild_members as fetch_members
from storage.guild_members_csv import merge_members


def extract_guild_members(context):
    page = context.new_page()
    page.goto("https://demonicscans.org/guild_members.php", wait_until="domcontentloaded")

    members = fetch_members(page)   # ← plus de conflit de nom
    merge_members(members)

    page.close()
