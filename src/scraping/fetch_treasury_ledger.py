from bs4 import BeautifulSoup
import re

def fetch_treasury_ledger(page):
    html = page.content()
    
    if "No entries." in html:
        return []
        
    soup = BeautifulSoup(html, "html.parser")

    
    table = soup.find("table")
    if table is None:
        raise RuntimeError("Treasury ledger table nor found")

    rows = table.find_all("tr")[1:]    

    for row in rows:
        cols = row.find_all("td")
        # 6 raws available raws
        if len(cols) != 6:
            raise RuntimeError("Unexpected table format")
        
        # Time
        time = cols[0].text.strip()
        # PlayerID
        link = cols[1].find("a")
        if not link or "href" not in link.attrs:
            raise RuntimeError("No link found")
        href = link["href"]
        match = re.search(r"id=(\d+)", href)
        if not match:
            raise RuntimeError("No match for PID")      
        pid = int(match.group(1))
        # Kind
        kind = cols[2].text.strip()
        # Resource
        resource = cols[3].text.strip()
        # Amount
        amount = cols[4].text.strip().replace(",", "")
        # Note
        note = cols[5].text.strip()

        treasury_ledger.append({
            "Time": time,
            "PlayerID": pid,
            "Kind": kind,
            "Resource": resource,
            "Amount": amount,
            "Note": note
        })

    return treasury_ledger
