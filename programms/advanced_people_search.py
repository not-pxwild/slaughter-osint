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
import webbrowser
import argparse
import time
import json
from datetime import datetime

def advanced_people_search():
    print("\n[*] Advanced People Search - Multi-Platform OSINT")
    print("[*] This tool searches across multiple platforms simultaneously\n")
    
    print("Search Options:")
    print("[1] Name Search (First + Last Name)")
    print("[2] Username Search")
    print("[3) Email Search")
    print("[4] Phone Number Search")
    print("[5] Address Search")
    
    search_type = input("\n[?] Select search type (1-5): ").strip()
    
    if search_type == "1":
        first_name = input("[?] First Name: ").strip()
        last_name = input("[?] Last Name: ").strip()
        search_term = f"{first_name} {last_name}"
        search_people_by_name(first_name, last_name)
        
    elif search_type == "2":
        username = input("[?] Username: ").strip()
        search_term = username
        search_people_by_username(username)
        
    elif search_type == "3":
        email = input("[?] Email Address: ").strip()
        search_term = email
        search_people_by_email(email)
        
    elif search_type == "4":
        phone = input("[?] Phone Number: ").strip()
        search_term = phone
        search_people_by_phone(phone)
        
    elif search_type == "5":
        address = input("[?] Address: ").strip()
        search_term = address
        search_people_by_address(address)
        
    else:
        print("[!] Invalid option!")
        return
    
    log_search(search_term, search_type)

def search_people_by_name(first_name, last_name):
    print(f"\n[*] Searching for: {first_name} {last_name}")
    print("[*] Opening multiple search platforms...\n")
    
    search_urls = [
        f"https://www.facebook.com/search/top/?init=quick&q={first_name}%20{last_name}",
        f"https://twitter.com/search?f=users&vertical=default&q={first_name}%20{last_name}",
        f"https://www.linkedin.com/search/results/people/?keywords={first_name}%20{last_name}",
        f"https://www.youtube.com/results?search_query={first_name}+{last_name}",
        f"https://www.tiktok.com/search?q={first_name}%20{last_name}",
        f"https://www.peekyou.com/{last_name}_{first_name}",
        f"https://www.spokeo.com/{last_name}-{first_name}",
        f"https://www.beenverified.com/lp/e030ee/1/loading?fn={first_name}&ln={last_name}",
        f"https://www.peoplelooker.com/lp/5ee6b8/1/loading?fn={first_name}&ln={last_name}",
        f"https://www.whitepages.com/name/{last_name}/{first_name}"
    ]
    
    for i, url in enumerate(search_urls, 1):
        print(f"[{i}] Opening: {url.split('/')[2]}")
        webbrowser.open(url)
        time.sleep(1)

def search_people_by_username(username):
    print(f"\n[*] Searching for username: {username}")
    print("[*] Opening social media platforms...\n")
    
    search_urls = [
        f"https://www.instagram.com/{username}/",
        f"https://twitter.com/{username}",
        f"https://www.facebook.com/{username}",
        f"https://www.tiktok.com/@{username}",
        f"https://www.youtube.com/{username}",
        f"https://www.reddit.com/user/{username}",
        f"https://github.com/{username}",
        f"https://www.twitch.tv/{username}",
        f"https://steamcommunity.com/id/{username}",
        f"https://www.linkedin.com/in/{username}"
    ]
    
    for i, url in enumerate(search_urls, 1):
        print(f"[{i}] Opening: {url.split('/')[2]}")
        webbrowser.open(url)
        time.sleep(1)

def search_people_by_email(email):
    print(f"\n[*] Searching for email: {email}")
    print("[*] Opening email search platforms...\n")
    
    search_urls = [
        f"https://www.facebook.com/search/top/?init=quick&q={email}",
        f"https://twitter.com/search?f=users&vertical=default&q={email}",
        f"https://www.linkedin.com/search/results/people/?keywords={email}",
        f"https://www.google.com/search?q={email}",
        f"https://www.bing.com/search?q={email}",
        f"https://haveibeenpwned.com/unifiedsearch/{email}",
        f"https://leakcheck.net/search?q={email}"
    ]
    
    for i, url in enumerate(search_urls, 1):
        print(f"[{i}] Opening: {url.split('/')[2]}")
        webbrowser.open(url)
        time.sleep(1)

def search_people_by_phone(phone):
    print(f"\n[*] Searching for phone: {phone}")
    print("[*] Opening phone search platforms...\n")
    
    search_urls = [
        f"https://www.facebook.com/search/top/?init=quick&q={phone}",
        f"https://www.whitepages.com/phone/{phone}",
        f"https://www.anywho.com/phone/{phone}",
        f"https://www.spokeo.com/phone/{phone}",
        f"https://www.beenverified.com/phone/{phone}",
        f"https://www.peoplelooker.com/phone/{phone}",
        f"https://www.google.com/search?q={phone}"
    ]
    
    for i, url in enumerate(search_urls, 1):
        print(f"[{i}] Opening: {url.split('/')[2]}")
        webbrowser.open(url)
        time.sleep(1)

def search_people_by_address(address):
    print(f"\n[*] Searching for address: {address}")
    print("[*] Opening address search platforms...\n")
    
    search_urls = [
        f"https://www.facebook.com/search/top/?init=quick&q={address}",
        f"https://www.whitepages.com/address/{address}",
        f"https://www.spokeo.com/address/{address}",
        f"https://www.beenverified.com/address/{address}",
        f"https://www.peoplelooker.com/address/{address}",
        f"https://www.google.com/search?q={address}",
        f"https://www.google.com/maps/search/{address}"
    ]
    
    for i, url in enumerate(search_urls, 1):
        print(f"[{i}] Opening: {url.split('/')[2]}")
        webbrowser.open(url)
        time.sleep(1)

def log_search(search_term, search_type):
    log_entry = {
        "search_term": search_term,
        "search_type": search_type,
        "timestamp": datetime.now().isoformat(),
        "platforms_opened": "Multiple"
    }
    
    try:
        with open("people_search_log.json", "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry) + "\n")
    except:
        pass

def main():
    parser = argparse.ArgumentParser(description="Advanced People Search")
    parser.add_argument("--target", help="Search term", required=False)
    args = parser.parse_args()
    
    if args.target:
        print(f"[*] Searching for: {args.target}")
        search_people_by_username(args.target)
    else:
        advanced_people_search()

if __name__ == "__main__":
    main()

