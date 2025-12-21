from scraping.fetch_weekly_leaderboard import fetch_weekly_leaderboard
#from storage.weekly_leaderboard_csv import merge_weekly_leaderboard

def extract_weekly_leaderboard(context):
    page = context.new_page()
    url = "https://demonicscans.org/weekly.php"
    print(url)
    page.goto(url, wait_until="domcontentloaded")

    weekly_leaderboard = fetch_weekly_leaderboard(page)

    page.close()
