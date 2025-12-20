from scraping.fetch_weekly_leaderboard import fetch_weekly_leaderboard
#from storage.guild_members_csv import merge_members

def extract_guild_members(context):
    page = context.new_page()
    url = "https://demonicscans.org/weekly.php"
    page.goto(url, wait_until="domcontentloaded")

    guild_members = fetch_weekly_leaderboard(page)

    page.close()
