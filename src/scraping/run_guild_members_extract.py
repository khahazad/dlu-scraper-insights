from playwright.sync_api import sync_playwright
from auth.login import login
from scraping.fetch_guild_members import extract_guild_members
from storage.guild_members_csv import merge_members

def main():
    with sync_playwright() as p:
        # Connexion (JS activé)
        browser, context, page = login(p)

        # Bloquer images, CSS, fonts, scripts pour la page guilde
        context.route("**/*", lambda route, request: (
            route.abort()
            if request.resource_type in ["image", "stylesheet", "font", "script"]
            else route.continue_()
        ))

        # Chargement rapide de la page guilde
        page.goto("https://demonicscans.org/guild_members.php", wait_until="domcontentloaded")

        # Extraction
        members = extract_guild_members(page)

        # Mise à jour du CSV
        merge_members(members)

        browser.close()

if __name__ == "__main__":
    main()
