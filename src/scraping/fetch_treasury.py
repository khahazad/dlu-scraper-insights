from bs4 import BeautifulSoup


def extract_page_rows(html):
    soup = BeautifulSoup(html, "html.parser")
    
    print("HTML de ma page guild_treasury : ")
    print(html[:500])
    
    table = soup.find("table")
    if not table:
        return []

    rows = []

    for tr in table.find_all("tr")[1:]:  # skip header
        tds = tr.find_all("td")
        if len(tds) < 5:
            continue

        time = tds[0].text.strip()

        # PlayerID depuis le lien
        link = tds[1].find("a")
        if link and "pid=" in link.get("href", ""):
            pid = link["href"].split("pid=")[1]
        else:
            pid = "0"

        kind = tds[2].text.strip()
        resource = tds[3].text.strip()
        amount = tds[4].text.strip().replace(",", "")

        rows.append({
            "Time": time,
            "PlayerID": pid,
            "Kind": kind,
            "Resource": resource,
            "Amount": amount
        })

    return rows
