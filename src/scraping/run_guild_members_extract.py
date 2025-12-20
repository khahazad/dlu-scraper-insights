from scraping.fetch_guild_members import extract_guild_members as fetch_members
from storage.guild_members_csv import merge_members
from utils.protection import assert_page_is_valid

def extract_guild_members(context):
    page = context.new_page()
    page.goto("https://demonicscans.org/guild_members.php", wait_until="domcontentloaded")

    # Détection anti-bot
    #assert_page_is_valid(page)

    members = fetch_members(page)
    merge_members(members)

    page.close()
