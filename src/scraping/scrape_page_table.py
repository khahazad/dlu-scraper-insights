from bs4 import BeautifulSoup

def scrape_first_table(context, url):
    page = context.new_page()
    page.goto(url, wait_until="domcontentloaded")

    soup = BeautifulSoup(page.content(), "html.parser")

    table = soup.find("table")
    if table is None:
        raise RuntimeError(f"No table found on page: {url}")

    rows = []
    for tr in table.find_all("tr"):
        cells = [td.get_text(strip=True) for td in tr.find_all(["td", "th"])]
        if cells:
            rows.append(cells)
          
    page.close()
    return rows
