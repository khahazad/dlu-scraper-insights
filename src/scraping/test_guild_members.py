from playwright.sync_api import sync_playwright
from auth.login import login

URL = "https://demonicscans.org/guild_members.php"

def main():
    with sync_playwright() as p:
        browser, context, page = login(p)

        print("Accès à la page :", URL)
        page.goto(URL)
        page.wait_for_load_state("networkidle")

        html = page.content().lower()

        if "access denied" in html:
            print("[DENIED] La page renvoie 'access denied'.")
            browser.close()
            return

        print("[OK] Page accessible.")

        # Récupération du tableau
        # On cherche un <table> dans la page
        table_html = page.locator("table").first.inner_html()

        print("\n===== CONTENU DU TABLEAU =====\n")
        print(table_html)
        print("\n===== FIN DU TABLEAU =====\n")

        browser.close()

if __name__ == "__main__":
    main()
