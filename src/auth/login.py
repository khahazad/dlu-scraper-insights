import os
from playwright.sync_api import Playwright
from bs4 import BeautifulSoup

def login(playwright: Playwright):      
    print("login")
    email = os.getenv("APP_EMAIL")
    password = os.getenv("APP_PASSWORD")

    browser = playwright.chromium.launch()
    context = browser.new_context(java_script_enabled=True)

    context = browser.new_context(
        java_script_enabled=True,
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
       "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        viewport={"width": 1280, "height": 800}
        )
    
    # Block images and CSS to save bandwidth, but DO NOT block scripts and font
    context.route("**/*", lambda route, request: (
        route.abort()
        if request.resource_type in ["image", "stylesheet"]
        else route.continue_()
    ))
    
    page = context.new_page()

    # Aller à la page de login
    page.goto("https://demonicscans.org/signin.php", wait_until="domcontentloaded")
    
    html = page.content()
    print("-----------page preview-----------")
    print(html)
    print("----------------------------------")

    if "cf-browser-verification" in page.content().lower():
        print("Cloudflare challenge detected, waiting…")
        page.wait_for_timeout(8000)

    html = page.content()
    text = BeautifulSoup(html, "html.parser").get_text()
    
    if "You are already signed in" in text:
        print("Already signed in")
        return browser, context, page
    elif "Sign in to your account" in text:
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
        
    else:
        raise RuntimeError("Unable to sign in")
