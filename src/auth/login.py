import os
from playwright.sync_api import Playwright, sync_playwright

def login(playwright: Playwright):
    email = os.getenv("APP_EMAIL")
    password = os.getenv("APP_PASSWORD")

    if not email or not password:
        raise ValueError("Les variables APP_EMAIL et APP_PASSWORD ne sont pas définies.")

    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://demonicscans.org/signin.php")

    # Déjà connecté ?
    if not page.locator("input[type='email']").is_visible():
        print("Déjà connecté.")
        return browser, context, page

    # Login normal
    page.fill("input[type='email']", email)
    page.fill("input[type='password']", password)

    page.get_by_role("button", name="Sign in").click()
    page.wait_for_load_state("networkidle")

    if "signin" in page.url.lower():
        raise RuntimeError("Échec de la connexion.")

    print("Connexion réussie :", page.url)
    return browser, context, page
