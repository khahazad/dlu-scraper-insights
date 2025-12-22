from scraping.fetch_weekly_leaderboard import fetch_weekly_leaderboard
#from storage.weekly_leaderboard_csv import merge_weekly_leaderboard

def extract_weekly_leaderboard(context):
    page = context.new_page()
    url = "https://demonicscans.org/weekly.php"

    page.goto(url, wait_until="domcontentloaded")

    print("Connected to :", page.url)
    
    weekly_leaderboard = fetch_weekly_leaderboard(page)

    page.close()
