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

import requests
import threading
from queue import Queue
import argparse
import time
import random

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
]

PLATFORMS = {
    "Instagram": {
        "url": "https://www.instagram.com/{}/",
        "available_codes": [404],
        "unavailable_codes": [200],
        "body_must_include": ["og:url", "profilePage"],
        "body_must_exclude": ["Page Not Found", "The link you followed may be broken"],
    },
    "Twitter": {
        "url": "https://twitter.com/{}",
        "available_codes": [404],
        "unavailable_codes": [200, 301, 302],
        "body_must_include": ["@{}"],
        "body_must_exclude": ["This account doesn’t exist", "Try searching for another"],
    },
    "Facebook": {
        "url": "https://www.facebook.com/{}",
        "available_codes": [404],
        "unavailable_codes": [200, 301, 302],
        "body_must_exclude": ["This Content Isn't Available"],
    },
    "TikTok": {
        "url": "https://www.tiktok.com/@{}",
        "available_codes": [404],
        "unavailable_codes": [200, 301, 302],
        "body_must_exclude": ["Couldn't find this account", "hasn't posted any videos"],
    },
    "YouTube": {
        "url": "https://www.youtube.com/@{}",
        "available_codes": [404],
        "unavailable_codes": [200, 301, 302],
        "body_must_include": ["@{}"],
    },
    "Reddit": {
        "url": "https://www.reddit.com/user/{}",
        "available_codes": [404],
        "unavailable_codes": [200, 302],
        "body_must_exclude": ["page not found", "u/{} doesn’t exist"],
    },
    "GitHub": {
        "url": "https://github.com/{}",
        "available_codes": [404],
        "unavailable_codes": [200, 301, 302],
        "body_must_include": ["followers", "following"],
    },
    "Twitch": {
        "url": "https://www.twitch.tv/{}",
        "available_codes": [404],
        "unavailable_codes": [200, 301, 302],
    },
    "Steam": {
        "url": "https://steamcommunity.com/id/{}",
        "available_codes": [404],
        "unavailable_codes": [200, 301, 302],
        "body_must_exclude": ["The specified profile could not be found"],
    },
    "Discord": {
        "url": "https://discord.com/users/{}",
        "available_codes": [404],
        "unavailable_codes": [200, 302],
    }
}

found_accounts = []
lock = threading.Lock()
queue = Queue()

def get_user_agent():
    return random.choice(USER_AGENTS)

def request_with_retries(url, headers, method="GET", max_retries=2, timeout=10):
    for attempt in range(max_retries + 1):
        try:
            if method == "HEAD":
                return requests.head(url, headers=headers, timeout=timeout, allow_redirects=False)
            return requests.get(url, headers=headers, timeout=timeout, allow_redirects=False)
        except requests.exceptions.RequestException:
            if attempt == max_retries:
                raise
            time.sleep(0.5 * (attempt + 1))

def body_matches(text, patterns, username):
    if not patterns:
        return False
    resolved = []
    for p in patterns:
        resolved.append(p.format(username))
    joined = "\n".join(resolved)
    for token in joined.split("\n"):
        if token and token.lower() in text.lower():
            return True
    return False

def check_username_availability(platform_name, platform_data, username):
    url = platform_data["url"].format(username)
    try:
        headers = {
            'User-Agent': get_user_agent(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        resp = request_with_retries(url, headers, method="HEAD")
        if resp.status_code == 405:
            resp = request_with_retries(url, headers, method="GET")
        status_code = resp.status_code
        if status_code in platform_data.get("available_codes", []):
            with lock:
                found_accounts.append((platform_name, url, "AVAILABLE"))
            return
        if status_code in platform_data.get("unavailable_codes", []):
            body = ""
            if status_code == 200:
                try:
                    body = request_with_retries(url, headers, method="GET").text
                except Exception:
                    body = ""
            inc = body_matches(body, platform_data.get("body_must_include"), username)
            exc = body_matches(body, platform_data.get("body_must_exclude"), username)
            if inc and not exc:
                with lock:
                    found_accounts.append((platform_name, url, "TAKEN"))
            elif exc and not inc:
                with lock:
                    found_accounts.append((platform_name, url, "AVAILABLE"))
            else:
                with lock:
                    found_accounts.append((platform_name, url, "TAKEN"))
            return
        with lock:
            found_accounts.append((platform_name, url, "UNKNOWN"))
    except requests.exceptions.RequestException:
        with lock:
            found_accounts.append((platform_name, url, "ERROR"))
    except Exception:
        with lock:
            found_accounts.append((platform_name, url, "ERROR"))

def worker():
    while True:
        item = queue.get()
        if item is None:
            break
        platform_name, platform_data, username = item
        check_username_availability(platform_name, platform_data, username)
        queue.task_done()

def scan_username(username, thread_count=5):
    print(f"\n[*] Scanning username '{username}' across {len(PLATFORMS)} platforms...")
    print(f"[*] Using {thread_count} threads for faster scanning\n")
    
    threads = []
    for _ in range(thread_count):
        t = threading.Thread(target=worker)
        t.start()
        threads.append(t)
    
    for platform_name, platform_data in PLATFORMS.items():
        queue.put((platform_name, platform_data, username))
    
    queue.join()
    
    for _ in range(thread_count):
        queue.put(None)
    for t in threads:
        t.join()
    
    return found_accounts

def print_results(results):
    if not results:
        print("\n[-] No results found!")
        return
    
    available = []
    taken = []
    unknown = []
    errors = []
    
    for platform, url, status in results:
        if status == "AVAILABLE":
            available.append((platform, url))
        elif status == "TAKEN":
            taken.append((platform, url))
        elif status == "UNKNOWN":
            unknown.append((platform, url))
        else:
            errors.append((platform, url))
    
    print("\n" + "="*80)
    print("                    USERNAME AVAILABILITY RESULTS")
    print("="*80)
    
    if available:
        print(f"\n[+] AVAILABLE ({len(available)}):")
        for platform, url in available:
            print(f"    ✓ {platform}: {url}")
    
    if taken:
        print(f"\n[-] TAKEN ({len(taken)}):")
        for platform, url in taken:
            print(f"    ✗ {platform}: {url}")
    
    if unknown:
        print(f"\n[?] UNKNOWN ({len(unknown)}):")
        for platform, url in unknown:
            print(f"    ? {platform}: {url}")
    
    if errors:
        print(f"\n[!] ERRORS ({len(errors)}):")
        for platform, url in errors:
            print(f"    ! {platform}: {url}")
    
    print("\n" + "="*80)
    print(f"SUMMARY: {len(available)} available, {len(taken)} taken, {len(unknown)} unknown, {len(errors)} errors")
    print("="*80)

def main():
    parser = argparse.ArgumentParser(description="Advanced Username Search Tool")
    parser.add_argument("--target", help="Username to search", required=False)
    args = parser.parse_args()
    
    username = args.target if args.target else input("\n[?] Enter username to search: ").strip()
    
    if not username:
        print("[!] No username provided!")
        return
    
    if len(username) < 3:
        print("[!] Username too short! Minimum 3 characters.")
        return
    
    start_time = time.time()
    results = scan_username(username)
    elapsed_time = time.time() - start_time
    
    print_results(results)
    print(f"\n[*] Scan completed in {elapsed_time:.2f} seconds")

if __name__ == "__main__":
    main()
