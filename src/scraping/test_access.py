from playwright.sync_api import sync_playwright
from auth.login import login

URLS = [
    "https://demonicscans.org/game_dash.php",
    "https://demonicscans.org/battle_pass.php",
    "https://demonicscans.org/a_lizardmen_winter.php",
    "https://demonicscans.org/active_wave.php?event=4&wave=2",
    "https://demonicscans.org/inventory.php",
    "https://demonicscans.org/pets.php",
    "https://demonicscans.org/stats.php",
    "https://demonicscans.org/adventurers_guild.php",
    "https://demonicscans.org/guild_dash.php",
    "https://demonicscans.org/guild_members.php",
    "https://demonicscans.org/guild_treasury_log.php",
    "https://demonicscans.org/guild_dungeon_instance.php?id=1675",
    "https://demonicscans.org/weekly.php",
    "https://demonicscans.org/chat.php",
    "https://demonicscans.org/guild_chat.php?channel=general",
]

def main():
    with sync_playwright() as p:
        browser, context, page = login(p)

        for url in URLS:
            try:
                page.goto(url)
                page.wait_for_load_state("networkidle")

                html = page.content().lower()

                if "access denied" in html:
                    print(f"[DENIED] {url}")
                else:
                    print(f"[OK] {url}")

            except Exception as e:
                print(f"[FAIL] {url} → {e}")

        browser.close()

if __name__ == "__main__":
    main()
