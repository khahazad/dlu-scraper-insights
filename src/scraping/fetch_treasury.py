from bs4 import BeautifulSoup
import re

def extract_treasury_ledgers(page):
    html = page.content()
    soup = BeautifulSoup(html, "html.parser")
    
    table = soup.find("table")
    if table is None:
        raise RuntimeError("Treasury ledger table nor found")

    rows = table.find_all("tr")[1:]    
    ledgers = []

    for row in rows:
        cols = row.find_all("td")
        # 6 raws available raws
        if len(cols) != 6:
            raise RuntimeError("Unexpected table format")
            
        # PlayerID
        link = cols[1].find("a")
        if not link or "href" not in link.attrs:
            raise RuntimeError("No link found")
        href = link["href"]
        match = re.search(r"id=(\d+)", href)
        if not match:
            raise RuntimeError("No match for PID")      
        pid = int(match.group(1))
        # Time
        time = tds[0].text.strip()
        # Kind
        kind = tds[2].text.strip()
        # Resource
        resource = tds[3].text.strip()
        # Amount
        amount = tds[4].text.strip().replace(",", "")
        # Note
        note = tds[5].text.strip()

        rows.append({
            "Time": time,
            "PlayerID": pid,
            "Kind": kind,
            "Resource": resource,
            "Amount": amount,
            "Note": note
        })

    return rows
