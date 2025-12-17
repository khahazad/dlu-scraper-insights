import os
from playwright.sync_api import sync_playwright

def login():
    email = os.getenv("APP_EMAIL")
    password = os.getenv("APP_PASSWORD")

    if not email or not password:
        raise ValueError("Les variables APP_EMAIL et APP_PASSWORD ne sont pas définies.")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()

        page = context.new_page()
        page.goto("https://demonicscans.org/signin.php")

        # Champs identifiés depuis la page ouverte dans Edge :
        # - Email address
        # - Password
        page.fill("input[type='email']", email)
        page.fill("input[type='password']", password)

        # Bouton "Sign in"
        page.click("button[type='submit']")

        # Attendre la fin des requêtes réseau
        page.wait_for_load_state("networkidle")

        # Vérification : si on est encore sur signin.php, la connexion a échoué
        if "signin" in page.url.lower():
            raise RuntimeError("Échec de la connexion : identifiants incorrects ou changement de page.")

        print("Connexion réussie :", page.url)

        # On retourne le contexte pour permettre le scraping ensuite
        return browser, context, page


if __name__ == "__main__":
    login()
