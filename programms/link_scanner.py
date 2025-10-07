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
import re
import time
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

def extract_links(html, base_url):
    soup = BeautifulSoup(html, "html.parser")
    urls = set()
    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        if href.startswith("mailto:"):
            continue
        full = urljoin(base_url, href)
        urls.add(full)
    return urls

def relevance_score(text, target):
    score = 0
    lowered = text.lower()
    for token in [target.lower(), "profile", "about", "bio", "contact", "user", "posts", "followers"]:
        if token in lowered:
            score += 1
    return score

def fetch(url, timeout=10):
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        r = requests.get(url, headers=headers, timeout=timeout)
        if r.status_code == 200 and r.text:
            return r.text
    except Exception:
        pass
    return ""

def google_dorks(target):
    seeds = []
    dorks = [
        f"https://www.google.com/search?q=site:reddit.com+%22{target}%22",
        f"https://www.google.com/search?q=site:twitter.com+%22{target}%22",
        f"https://www.google.com/search?q=site:github.com+%22{target}%22",
    ]
    for d in dorks:
        html = fetch(d)
        urls = re.findall(r"/url\?q=(https?://[^&]+)&", html)
        seeds.extend(urls)
        time.sleep(0.5)
    return list(dict.fromkeys(seeds))

def build_seeds(target):
    seeds = [
        f"https://twitter.com/{target}",
        f"https://www.instagram.com/{target}/",
        f"https://github.com/{target}",
        f"https://www.reddit.com/user/{target}",
        f"https://www.facebook.com/{target}",
    ]
    seeds.extend(google_dorks(target))
    return list(dict.fromkeys(seeds))

def crawl(target, depth=2, limit=120):
    visited = set()
    queue = []
    results = []
    seeds = build_seeds(target)
    for s in seeds:
        queue.append((s, 0))
    while queue and len(visited) < limit:
        url, d = queue.pop(0)
        if url in visited or d > depth:
            continue
        visited.add(url)
        html = fetch(url)
        if not html:
            continue
        text_snippet = BeautifulSoup(html, "html.parser").get_text(" ", strip=True)[:240]
        score = relevance_score(text_snippet, target)
        results.append({"url": url, "domain": urlparse(url).netloc, "snippet": text_snippet, "score": score})
        if d < depth:
            for link in extract_links(html, url):
                if urlparse(link).netloc and link not in visited:
                    queue.append((link, d + 1))
        time.sleep(0.2)
    return results

def save_csv(rows, out_file):
    import csv
    with open(out_file, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["URL", "Domain", "Snippet", "RelevanceScore"])
        for r in rows:
            w.writerow([r["url"], r["domain"], r["snippet"], r["score"]])

def main():
    parser = argparse.ArgumentParser(description="Automated Link Extraction & Network Mapping")
    parser.add_argument("--target", help="Username or email to pivot from", required=False)
    args = parser.parse_args()

    target = args.target if args.target else input("\n[?] Enter username/email: ").strip()
    if not target:
        print("[!] No target provided!")
        return

    print(f"\n[*] Crawling links for: {target}")
    rows = crawl(target)
    rows.sort(key=lambda r: r["score"], reverse=True)
    out_file = f"links_{re.sub(r'[^A-Za-z0-9_@.-]+','_', target)}.csv"
    save_csv(rows, out_file)
    print(f"[+] Saved {len(rows)} links to {out_file}")

if __name__ == "__main__":
    main()

