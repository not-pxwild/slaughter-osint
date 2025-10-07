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
from difflib import SequenceMatcher

import requests
from bs4 import BeautifulSoup
import phonenumbers
from phonenumbers import geocoder, carrier, timezone

def normalize_phone(num):
    try:
        parsed = phonenumbers.parse(num, None)
        if not phonenumbers.is_possible_number(parsed):
            return None, None
        e164 = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
        national = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL)
        return e164, parsed
    except Exception:
        return None, None

def fetch(url, timeout=12):
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        r = requests.get(url, headers=headers, timeout=timeout)
        if r.status_code == 200:
            return r.text
    except Exception:
        pass
    return ""

def parse_whitepages(html):
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(" ", strip=True)
    owner = None
    m = re.search(r"Owner(?: Name)?:\s*([A-Z][A-Za-z' -]+)", text)
    if m:
        owner = m.group(1)
    city = None
    c = re.search(r"(City|Location):\s*([A-Za-z .'-]+)", text)
    if c:
        city = c.group(2)
    return {"owner": owner, "location": city, "source": "Whitepages"}

def parse_anywho(html):
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(" ", strip=True)
    owner = None
    m = re.search(r"Name:\s*([A-Z][A-Za-z' -]+)", text)
    if m:
        owner = m.group(1)
    loc = None
    c = re.search(r"Address:\s*([A-Za-z0-9 .,'-]+)", text)
    if c:
        loc = c.group(1)
    return {"owner": owner, "location": loc, "source": "AnyWho"}

def score_profile(hints):
    name = hints.get("owner") or ""
    loc = hints.get("location") or ""
    score = 0
    if name:
        score += 2
    if loc:
        score += 1
    return score

def main():
    parser = argparse.ArgumentParser(description="Automated Phone Scraping & Owner Inference")
    parser.add_argument("--target", help="Phone number to validate", required=False)
    args = parser.parse_args()

    print("\n[*] Phone Validation & Owner Inference (no APIs)")
    print("[*] Example: +19087654321")

    numero = args.target if args.target else input("\n[?] Enter the phone number: ").strip()
    if not numero:
        print("[!] No phone number provided!")
        return

    e164, parsed = normalize_phone(numero)
    if not e164:
        print("[!] Invalid phone number format")
        return

    print(f"\n[*] Normalized: {e164}")
    try:
        operator = carrier.name_for_number(parsed, "en") or "Unknown"
    except Exception:
        operator = "Unknown"
    try:
        tzs = timezone.time_zones_for_number(parsed)
        tz = tzs[0] if tzs else "Unknown"
    except Exception:
        tz = "Unknown"
    try:
        region = geocoder.description_for_number(parsed, "en") or "Unknown"
    except Exception:
        region = "Unknown"

    print(f"[+] Carrier: {operator}")
    print(f"[+] Region: {region}")
    print(f"[+] Timezone: {tz}")

    hints = []
    wp = fetch(f"https://www.whitepages.com/phone/{e164}")
    if wp:
        hints.append(parse_whitepages(wp))
    time.sleep(0.5)
    aw = fetch(f"https://www.anywho.com/phone/{e164}")
    if aw:
        hints.append(parse_anywho(aw))

    hints = [h for h in hints if h.get("owner") or h.get("location")]
    for h in hints:
        h["score"] = score_profile(h)

    hints.sort(key=lambda x: x.get("score", 0), reverse=True)
    if hints:
        print("\n[+] Owner Inference:")
        for h in hints:
            print(f"  - {h.get('owner') or 'Unknown'} | {h.get('location') or 'Unknown'} | {h.get('source')} | score={h.get('score')}")
    else:
        print("\n[-] No owner hints found across scraped sources")

if __name__ == "__main__":
    main()

