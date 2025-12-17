import os
from playwright.sync_api import Playwright

def login(playwright: Playwright):
    email = os.getenv("APP_EMAIL")
    password = os.getenv("APP_PASSWORD")

    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    
    # 🚀 Bloquer images, CSS, fonts, scripts
    context.route("**/*", lambda route, request: (
        route.abort()
        if request.resource_type in ["image", "stylesheet", "font", "script"]
        else route.continue_()
    ))
    
    page = context.new_page()

    page.goto("https://demonicscans.org/signin.php")

    # Déjà connecté ?
    if not page.locator("input[type='email']").is_visible():
        print("Déjà connecté.")
        return browser, context, page

    page.fill("input[type='email']", email)
    page.fill("input[type='password']", password)
    page.get_by_role("button", name="Sign in").click()
    page.wait_for_load_state("networkidle")

    if "signin" in page.url.lower():
        raise RuntimeError("Échec de la connexion.")

    print("Connexion réussie :", page.url)
    return browser, context, page
