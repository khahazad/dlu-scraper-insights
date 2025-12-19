from playwright.sync_api import Page

def assert_page_is_valid(page: Page, expected_selector: str):
    # Vérifier la réponse HTTP
    response = page.wait_for_load_state("domcontentloaded")
    html = page.content().lower()

    # Signatures Cloudflare / anti-bot
    signatures = [
        "cf-challenge", "cloudflare", "attention required",
        "verify you are human", "captcha", "robot", "blocked"
    ]
    if any(sig in html for sig in signatures):
        raise RuntimeError("Protection anti-bot détectée (Cloudflare ou captcha).")

    # Challenge JS
    if page.locator("div#cf-spinner, #challenge-running").count() > 0:
        raise RuntimeError("Challenge JavaScript détecté (Cloudflare).")

    # Vérifier que l’élément attendu existe
    if page.locator(expected_selector).count() == 0:
        raise RuntimeError(f"Structure HTML inattendue : {expected_selector} introuvable.")
