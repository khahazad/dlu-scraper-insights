from storage.treasury_csv import load_existing_rows, save_csv
from scraping.fetch_treasury_ledger import extract_treasury_ledger

def extract_treasury_log(context):
    page = context.new_page()

    page_number = 1
    new_rows = []

    while True:
        url = f"https://demonicscans.org/guild_treasury_log.php?p={page_number}&res=&kind=donation"
        page.goto(url, wait_until="domcontentloaded")

        rows = extract_treasury_ledger(page)
        if not rows:
            break

        stop = False
        for r in rows:
            key = (r["Time"], r["PlayerID"], r["Kind"], r["Resource"], r["Amount"])
            if key in existing_keys:
                stop = True
                break
            new_rows.append(r)
            existing_keys.add(key)

        if stop:
            break

        page_number += 1

    ctx.close()

    all_rows = new_rows + all_rows
    save_csv(all_rows)
