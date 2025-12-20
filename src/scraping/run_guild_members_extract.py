from scraping.fetch_guild_members import fetch_guild_members
from storage.guild_members_csv import merge_members

def extract_guild_members(context):
    page = context.new_page()
    url = "https://demonicscans.org/guild_members.php"
    page.goto(url, wait_until="domcontentloaded")
    #page.wait_for_selector("table", timeout=30000)
    print("Wait 5 secondes")
    page.wait_for_timeout(5000)  # wait 5 seconds

    guild_members = fetch_guild_members(page)
    merge_members(guild_members)

    page.close()
