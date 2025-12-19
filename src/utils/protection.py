from playwright.sync_api import Page

# Signatures HTML typiques des protections anti-bot
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

def assert_page_is_valid(page: Page, expected_selector: str | None = None):
    """
    Vérifie que la page n'est pas protégée (Cloudflare, captcha, challenge JS)
    et que la structure HTML attendue est présente.
    """

    html = page.content().lower()

    # 1. Détection Cloudflare / captcha / anti-bot
    if any(sig in html for sig in PROTECTION_SIGNATURES):
        raise RuntimeError("Protection anti-bot détectée (Cloudflare / captcha / challenge JS).")

    # 2. Détection challenge JS Cloudflare
    if page.locator("div#cf-spinner, #challenge-running").count() > 0:
        raise RuntimeError("Challenge JavaScript Cloudflare détecté.")

    # 3. Vérification structure HTML attendue
    if expected_selector and page.locator(expected_selector).count() == 0:
        raise RuntimeError(f"Structure HTML inattendue : {expected_selector} introuvable.")
