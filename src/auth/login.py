import os
from playwright.sync_api import Playwright
from utils.protection import assert_page_is_valid

def login(playwright: Playwright):
    email = os.getenv("APP_EMAIL")
    password = os.getenv("APP_PASSWORD")

    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    
    # Bloquer images, CSS, fonts, scripts
    context.route("**/*", lambda route, request: (
        route.abort()
        if request.resource_type in ["image", "stylesheet", "font", "script"]
        else route.continue_()
    ))
    
    page = context.new_page()

    # Aller à la page de login
    page.goto("https://demonicscans.org/signin.php", wait_until="domcontentloaded")

    # Détection anti-bot sur la page de login
    assert_page_is_valid(page, "input[type='email']")

    # Déjà connecté ?
    if not page.locator("input[type='email']").is_visible():
        print("Déjà connecté.")
        return browser, context, page

    # Formulaire
    page.fill("input[type='email']", email)
    page.fill("input[type='password']", password)
    page.get_by_role("button", name="Sign in").click()
    page.wait_for_load_state("networkidle")

    # Détection anti-bot après login
    assert_page_is_valid(page)

    # Vérification login OK
    if "signin" in page.url.lower():
        raise RuntimeError("Échec de la connexion (mauvais identifiants ou protection).")

    print("Connexion réussie :", page.url)
    return browser, context, page
