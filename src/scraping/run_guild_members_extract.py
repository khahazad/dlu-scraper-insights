from scraping.fetch_guild_members import fetch_guild_members
from storage.guild_members_csv import merge_members

def extract_guild_members(context):
    page = context.new_page()
    url = "https://demonicscans.org/guild_members.php"
    page.goto(url, wait_until="domcontentloaded")
    #page.wait_for_selector("table", timeout=30000)

    print("Connected to :", page.url)
    
    guild_members = fetch_guild_members(page)
    #merge_members(guild_members)

    page.close()
    return guild_members
