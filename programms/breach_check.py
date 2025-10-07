# -----------------------------------------------------------------------------
# Copyright (c) 2025 pxwild. All Rights Reserved.
# pxwild PROPRIETARY AND CONFIDENTIAL — NOT FOR MODIFICATION OR REDISTRIBUTION.
#
# This software and its source code are proprietary to pxwild. Unauthorized
# copying, modification, distribution, decompilation, reverse engineering, or
# creation of derivative works is strictly prohibited without prior written
# permission from pxwild. Any attempt to modify or remove this notice is a
# material breach of the license and will be acted upon to the fullest extent
# permitted by law.
# -----------------------------------------------------------------------------

import argparse
import concurrent.futures
import json
import re
import time
from datetime import datetime

import requests
from bs4 import BeautifulSoup

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
]

def ua_headers():
    import random
    return {"User-Agent": random.choice(USER_AGENTS), "Accept-Language": "en-US,en;q=0.9"}

def get_session():
    s = requests.Session()
    s.headers.update(ua_headers())
    return s

def scrape_hibp(session, target):
    try:
        url = f"https://haveibeenpwned.com/account/{target}"
        r = session.get(url, timeout=15)
        if r.status_code not in (200, 404):
            return {"source": "HIBP", "status": r.status_code, "breaches": []}
        soup = BeautifulSoup(r.text, "html.parser")
        breaches = []
        for row in soup.select("table tr"):
            cols = [c.get_text(strip=True) for c in row.find_all(["td", "th"])]
            if len(cols) >= 2 and cols[0].lower() != "breach":
                name = cols[0]
                date_match = re.search(r"\d{4}-\d{2}-\d{2}", " ".join(cols))
                breaches.append({"name": name, "date": date_match.group(0) if date_match else None, "types": []})
        return {"source": "HIBP", "status": r.status_code, "breaches": breaches}
    except Exception as e:
        return {"source": "HIBP", "error": str(e), "breaches": []}

def scrape_leakcheck_public(session, target):
    try:
        url = f"https://leakcheck.io/search?q={target}"
        r = session.get(url, timeout=15)
        soup = BeautifulSoup(r.text, "html.parser")
        breaches = []
        text = soup.get_text(" ", strip=True)
        for m in re.finditer(r"Breach:?\s*([A-Za-z0-9 ._-]+).*?(\d{4}-\d{2}-\d{2})?", text):
            breaches.append({"name": m.group(1).strip(), "date": m.group(2) or None, "types": []})
        return {"source": "LeakCheck", "status": r.status_code, "breaches": breaches}
    except Exception as e:
        return {"source": "LeakCheck", "error": str(e), "breaches": []}

def scrape_firefox_monitor(session, target):
    try:
        url = f"https://monitor.firefox.com/breach-search?q={target}"
        r = session.get(url, timeout=15)
        soup = BeautifulSoup(r.text, "html.parser")
        breaches = []
        for card in soup.select(".breach-card, .breach-list-item"):
            name = card.get_text(" ", strip=True)[:80]
            date = None
            dm = re.search(r"\d{4}-\d{2}-\d{2}", name)
            if dm:
                date = dm.group(0)
            breaches.append({"name": name, "date": date, "types": []})
        return {"source": "FirefoxMonitor", "status": r.status_code, "breaches": breaches}
    except Exception as e:
        return {"source": "FirefoxMonitor", "error": str(e), "breaches": []}

def scrape_dehashed_public(session, target):
    try:
        url = f"https://www.dehashed.com/search?query={target}"
        r = session.get(url, timeout=15)
        soup = BeautifulSoup(r.text, "html.parser")
        breaches = []
        for row in soup.select("table tr"):
            txt = row.get_text(" ", strip=True)
            if txt and target.lower() in txt.lower():
                name = txt.split(" ")[0]
                breaches.append({"name": name, "date": None, "types": []})
        return {"source": "DeHashedPublic", "status": r.status_code, "breaches": breaches}
    except Exception as e:
        return {"source": "DeHashedPublic", "error": str(e), "breaches": []}

def enrich_breach_details(session, breach):
    return breach

def dedupe_and_sort(breaches):
    seen = {}
    for b in breaches:
        key = (b.get("name"), b.get("date"))
        if key not in seen:
            seen[key] = b
    items = list(seen.values())
    items.sort(key=lambda x: (x.get("date") or "9999-99-99", x.get("name") or ""))
    return items

def fuzzy_link_to_target(entries, target):
    import difflib
    for e in entries:
        e["score"] = difflib.SequenceMatcher(a=(e.get("name") or "").lower(), b=target.lower()).ratio()
    return entries

def run_scrapers(target):
    session = get_session()
    sites = [
        scrape_hibp,
        scrape_leakcheck_public,
        scrape_firefox_monitor,
        scrape_dehashed_public,
    ]
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as ex:
        futs = [ex.submit(site, session, target) for site in sites]
        for f in concurrent.futures.as_completed(futs):
            results.append(f.result())
            time.sleep(0.2)
    all_breaches = []
    for r in results:
        for b in r.get("breaches", []):
            all_breaches.append({"source": r.get("source"), **b})
    all_breaches = dedupe_and_sort(all_breaches)
    all_breaches = fuzzy_link_to_target(all_breaches, target)
    return {"target": target, "checked_at": datetime.utcnow().isoformat() + "Z", "sources": results, "breaches": all_breaches}

def main():
    parser = argparse.ArgumentParser(description="Automated Breach Scraper (no APIs)")
    parser.add_argument("--target", help="Email or username to check", required=False)
    args = parser.parse_args()

    target = args.target if args.target else input("\nEnter email or username: ").strip()
    if not target:
        print("No target provided!")
        return

    print(f"\n[*] Scraping public breach sources for: {target}")
    report = run_scrapers(target)
    hits = len(report.get("breaches", []))
    print(f"[+] Potential breaches found: {hits}")
    if hits:
        for b in report["breaches"]:
            print(f"  - {b.get('name')} ({b.get('date')}) [{b.get('source')}] score={b.get('score'):.2f}")

    out_file = f"breaches_{re.sub(r'[^A-Za-z0-9_@.-]+','_', target)}.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    print(f"\n[*] Saved report to: {out_file}")

if __name__ == "__main__":
    main()

