from storage.treasury_csv import load_treasury_rows, save_csv
from scraping.fetch_treasury_ledger import fetch_treasury_ledger

def extract_treasury_log(context):
    page = context.new_page()

    page_number = 1
    all_rows = []
        
    while True:
        url = f"https://demonicscans.org/guild_treasury_log.php?p={page_number}&res=&kind=donation"
        page.goto(url, wait_until="domcontentloaded")

        rows = fetch_treasury_ledger(page)
        if not rows:
            break

        for r in rows:
            key = (r["Time"], r["PlayerID"], r["Kind"], r["Resource"], r["Amount"])
            all_rows.append(r)
            existing_keys.add(key)
        page_number += 1

    context.close()

    save_csv(all_rows)
