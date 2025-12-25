import os
from playwright.sync_api import Playwright

def login(playwright: Playwright):
    print("login")

    email = os.getenv("APP_EMAIL")
    password = os.getenv("APP_PASSWORD")

    #browser = playwright.chromium.launch()
    browser = playwright.chromium.launch(headless=True)

    context = browser.new_context(
        java_script_enabled=True,
        user_agent=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        viewport={"width": 1280, "height": 800},
    )

    # Reduce bandwidth
    context.route("**/*", lambda route, request: (
        route.abort()
        if request.resource_type in ["image", "stylesheet"]
        else route.continue_()
    ))

    page = context.new_page()
    page.goto("https://demonicscans.org/signin.php", wait_until="domcontentloaded")

    # --- CASE 1: Already signed in ---
    if page.locator("text=You are already signed in").is_visible():
        print("Already signed in")
        return browser, context

    # --- CASE 2: Login form available ---
    if page.locator("text=Sign in to your account").is_visible():
        print("Signing in to your account")        
        page.fill("input[type='email']", email)
        page.fill("input[type='password']", password)
        page.get_by_role("button", name="Sign in").click()
        
        page.wait_for_load_state("networkidle")

        # If still on signin page → login failed 
        if "signin" in page.url.lower(): 
            print("Login failed") 
            context.close() 
            browser.close()
            return None, None, None
        else:
            print("Connected to:", page.url)
            return browser, context
    else:
        # --- ANY OTHER CASE: Cloudflare or unexpected page ---
        print("Login page not available — skipping run.")
        context.close()
        browser.close()
        return None, None
