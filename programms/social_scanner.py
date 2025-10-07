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

PLATFORMS = {
    "Facebook": "https://www.facebook.com/{}",
    "Twitter": "https://twitter.com/{}",
    "Instagram": "https://www.instagram.com/{}",
    "LinkedIn": "https://www.linkedin.com/in/{}",
    "YouTube": "https://www.youtube.com/{}",
    "Reddit": "https://www.reddit.com/user/{}",
    "Pinterest": "https://www.pinterest.com/{}",
    "Tumblr": "https://{}.tumblr.com",
    "GitHub": "https://github.com/{}",
    "TikTok": "https://www.tiktok.com/@{}",
}

found_accounts = []
lock = threading.Lock()
queue = Queue()

def check_url(platform, url, username):
    full_url = url.format(username)
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        try:
            head = requests.head(full_url, headers=headers, timeout=4, allow_redirects=False)
        except Exception:
            head = None
        if head and head.status_code in [200, 301, 302, 403]:
            with lock:
                found_accounts.append((platform, full_url))
            return
        response = requests.get(full_url, headers=headers, timeout=7, allow_redirects=False)
        if response.status_code == 200:
            with lock:
                found_accounts.append((platform, full_url))
        elif response.status_code in [301, 302, 403]:
            with lock:
                found_accounts.append((platform, full_url))
    except:
        pass

def worker():
    while True:
        item = queue.get()
        if item is None:
            break
        platform, url, username = item
        check_url(platform, url, username)
        queue.task_done()

def check_username(username, thread_count=10):
    print(f"\n[*] Checking username '{username}' across {len(PLATFORMS)} platforms...\n")
    
    threads = []
    for _ in range(thread_count):
        t = threading.Thread(target=worker)
        t.start()
        threads.append(t)
    
    for platform, url in PLATFORMS.items():
        queue.put((platform, url, username))
    
    queue.join()
    
    for _ in range(thread_count):
        queue.put(None)
    for t in threads:
        t.join()
    
    return found_accounts

def main():
    parser = argparse.ArgumentParser(description="Social Media Scanner")
    parser.add_argument("--target", help="Username to search", required=False)
    args = parser.parse_args()
    
    username = args.target if args.target else input("Enter username to search: ").strip()
    
    if not username:
        print("[!] No username provided!")
        return
    
    found = check_username(username)
    
    if found:
        print("\n[+] Found accounts:")
        for platform, url in sorted(found, key=lambda x: x[0]):
            print(f"  [+] {platform}: {url}")
    else:
        print("\n[-] No accounts found with this username.")

if __name__ == "__main__":
    main()

