from scraping.fetch_player_info import extract_player_info
from storage.player_info_csv import load_csv, save_csv, update_player_info_in_memory

def extract_all_players_info(browser):
    data = load_csv()
    player_ids = list(data.keys())

    ctx = browser.new_context(java_script_enabled=False)

    ctx.route("**/*", lambda route, request: (
        route.abort()
        if request.resource_type in ["image", "stylesheet", "font", "script"]
        else route.continue_()
    ))

    page = ctx.new_page()
    
    print(f"Connecting to {player_ids.len()} player pages")
    
    for pid in player_ids:
        url = f"https://demonicscans.org/player.php?pid={pid}"
        page.goto(url, wait_until="domcontentloaded")

        info = extract_player_info(page.content())
        update_player_info_in_memory(data, pid, info["name"], info["level"])

    save_csv(data)
    ctx.close()
