import re
from bs4 import BeautifulSoup

# ---------------------------------------------------------
# Extract player info with pid using a lightweight context
# ---------------------------------------------------------
def scrape_player_info(ctx, pid):
    url = f"https://demonicscans.org/player.php?pid={pid}"
    page = ctx.new_page()

    try:
        page.goto(url, wait_until="domcontentloaded", timeout=5000)
        html = page.content()
        soup = BeautifulSoup(html, "html.parser")

        # Player name in <h1>
        h1 = soup.find("h1")
        if h1 is None:
            raise RuntimeError(f"Player name not found for pid {pid}.")
        name = h1.get_text(strip=True)

        # Level pattern: "Level 1,234"
        match = re.search(r"Level\s+([\d,]+)", html)
        if not match:
            raise RuntimeError(f"Player level not found for pid {pid}.")

        level = int(match.group(1).replace(",", ""))

        return {
            "pid": pid,
            "name": name,
            "level": level,
        }

    finally:
        page.close()


# ---------------------------------------------------------
# Scrape many players info using their IDs
# ---------------------------------------------------------
def scrape_players_info(browser, player_ids):
    results = {}
    
    ctx = browser.new_context(
      java_script_enabled=False,
      bypass_csp=True,
      ignore_https_errors=True,
      user_agent=(
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
          "AppleWebKit/537.36 (KHTML, like Gecko) "
          "Chrome/120.0.0.0 Safari/537.36"
      )
    )

    ctx.route("**/*", lambda route, request: (
        route.abort()
        if request.resource_type in ["image", "stylesheet", "font", "script"]
        else route.continue_()
    ))

    try:
        for pid in player_ids:
            info = scrape_player_info(ctx, pid)
            results[pid] = { "Player": info["name"], "Level": info["level"], }

        return results

    finally:
        ctx.close()
