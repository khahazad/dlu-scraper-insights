import os
from playwright.sync_api import Playwright
from bs4 import BeautifulSoup

def login(playwright: Playwright):      
    print("login")
    email = os.getenv("APP_EMAIL")
    password = os.getenv("APP_PASSWORD")

    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context(java_script_enabled=True)

    # Block images, CSS and fonts to save bandwidth, but DO NOT block scripts
    context.route("**/*", lambda route, request: (
        route.abort()
        if request.resource_type in ["image", "stylesheet", "font"]
        else route.continue_()
    ))
    
    page = context.new_page()

    # Aller à la page de login
    page.goto("https://demonicscans.org/signin.php", wait_until="domcontentloaded")
    
    html = page.content()
    text = BeautifulSoup(html, "html.parser").get_text()
    print("-----------page preview-----------")
    print(text)
    print("----------------------------------")

    if text.contains("You are already signed in"):
        print("Already signed in")
        return browser, context, page
    elif text.contains("Sign in to your account"):
        print("Signing in to your account")
        # Formulaire
        page.fill("input[type='email']", email)
        page.fill("input[type='password']", password)
        page.get_by_role("button", name="Sign in").click()
        page.wait_for_load_state("networkidle")        
        
        # Vérification login OK
        if "signin" in page.url.lower():
            raise RuntimeError("Login failed")
            
        print("Connected to :", page.url)
        return browser, context, page
        
    else raise RuntimeError("Unable to sign in")
