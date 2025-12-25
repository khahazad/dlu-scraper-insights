import re
from bs4 import BeautifulSoup

def scrape_first_table(context, url, pid_column=None, key="auto"):
    """
    Scrape the first table on the page.
    
    If pid_column is provided, replace that column's text with the extracted PID
    AND rename the header to 'PID'.
    
    key="pid"  → dictionary keyed by PID (requires pid_column)
    key="auto" → dictionary keyed by auto-generated row IDs
    """
    page = context.new_page()
    page.goto(url, wait_until="domcontentloaded")

    soup = BeautifulSoup(page.content(), "html.parser")
    table = soup.find("table")
    if table is None:
        raise RuntimeError(f"No table found on page: {url}")

    rows = []
    header_processed = False

    for tr in table.find_all("tr"):
        cols = tr.find_all(["td", "th"])
        if not cols:
            continue

        # HEADER
        if cols[0].name == "th" and not header_processed:
            header = [c.get_text(strip=True) for c in cols]

            if pid_column is not None:
                header[pid_column] = "PID"

            rows.append(header)
            header_processed = True
            continue

        # DATA ROW
        row = []
        for idx, col in enumerate(cols):
            if pid_column is not None and idx == pid_column:
                link = col.find("a")
                if not link or "href" not in link.attrs:
                    raise RuntimeError(f"No link found in PID column {pid_column} on page {url}")

                href = link["href"]
                match = re.search(r"id=(\d+)", href)
                if not match:
                    raise RuntimeError(f"No PID found in link: {href}")

                pid = int(match.group(1))
                row.append(pid)
            else:
                row.append(col.get_text(strip=True))

        rows.append(row)

    page.close()

    # ----------------------------------------------------
    # RETURN AS DICTIONARY
    # ----------------------------------------------------
    header = rows[0]
    data_rows = rows[1:]

    result = {}

    for i, row in enumerate(data_rows, start=1):

        # Determine key
        if key == "pid":
            if pid_column is None:
                raise RuntimeError("key='pid' requires pid_column")
            dict_key = row[pid_column]
        else:
            dict_key = f"row_{i}"

        # Build row dictionary
        entry = {}
        for col_index, value in enumerate(row):
            if key == "pid" and col_index == pid_column: 
                continue # skip PID column entirely 
            entry[header[col_index]] = value

        result[dict_key] = entry

    return result

def scrape_paginated_tables(context, url_template, pid_column=1, key="auto", max_pages=200):
    """
    Scrape multiple paginated tables until no table or empty table is found.

    Parameters:
        context: Playwright context
        url_template: string with {page} placeholder
        pid_column: column index for PID extraction (or None)
        key: "auto" or "pid"
        max_pages: safety limit

    Returns:
        A single dictionary containing all rows from all pages.
    """
    all_rows = {}
    page_number = 1

    while True:
        url = url_template.format(page=page_number)
        #print(f"  → Scraping page {page_number}")

        try:
            page_data = scrape_first_table(context, url, pid_column, key)
        except RuntimeError:
            print(f"Scraping page {page_number}: No table found. Stopping pagination.")
            break

        if not page_data:
            print(f"Scraping page {page_number}: Empty table. Stopping pagination.")
            break

        # Merge dictionaries
        all_rows.update(page_data)

        # Merge with unique keys 
        for i, (k, v) in enumerate(page_data.items(), start=1): 
            unique_key = f"p{page_number}_r{i}" 
            all_rows[unique_key] = v

        page_number += 1
        if page_number > max_pages:
            print("  Safety stop: too many pages.")
            break

    return all_rows
