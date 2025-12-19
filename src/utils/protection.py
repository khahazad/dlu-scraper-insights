from playwright.sync_api import Page

PROTECTION_SIGNATURES = [
    "cf-challenge",
    "cloudflare",
    "attention required",
    "verify you are human",
    "captcha",
    "robot",
    "blocked",
    "challenge-running"
]

def assert_page_is_valid(page: Page):
    """
    Vérifie que la page n'est pas protégée (Cloudflare / captcha / JS challenge).
    """
    html = page.content().lower()

    # Signatures Cloudflare / captcha
    if any(sig in html for sig in PROTECTION_SIGNATURES):
        raise RuntimeError("Protection anti-bot détectée (Cloudflare / captcha).")

    # Challenge JS Cloudflare
    if page.locator("div#cf-spinner, #challenge-running").count() > 0:
        raise RuntimeError("Challenge JavaScript Cloudflare détecté.")
