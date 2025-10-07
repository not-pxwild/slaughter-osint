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
import json
import argparse
import time
from datetime import datetime
import os

def archive_social_media(username):
    print(f"\n[*] Archiving social media presence for: {username}")
    print("[*] This tool saves social media data for offline analysis\n")
    
    archive_data = {
        "username": username,
        "timestamp": datetime.now().isoformat(),
        "platforms": {},
        "summary": {}
    }
    
    platforms = {
        "Instagram": f"https://www.instagram.com/{username}/",
        "Twitter": f"https://twitter.com/{username}",
        "Facebook": f"https://www.facebook.com/{username}",
        "TikTok": f"https://www.tiktok.com/@{username}",
        "YouTube": f"https://www.youtube.com/{username}",
        "Reddit": f"https://www.reddit.com/user/{username}",
        "GitHub": f"https://github.com/{username}",
        "Twitch": f"https://www.twitch.tv/{username}",
        "Steam": f"https://steamcommunity.com/id/{username}",
        "LinkedIn": f"https://www.linkedin.com/in/{username}"
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    found_profiles = 0
    total_checked = 0
    
    for platform, url in platforms.items():
        total_checked += 1
        print(f"[*] Checking {platform}...", end=" ")
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            
            platform_data = {
                "url": url,
                "status_code": response.status_code,
                "accessible": response.status_code == 200,
                "response_time": response.elapsed.total_seconds(),
                "content_length": len(response.content),
                "headers": dict(response.headers),
                "timestamp": datetime.now().isoformat()
            }
            
            if response.status_code == 200:
                platform_data["title"] = extract_title(response.text)
                platform_data["description"] = extract_description(response.text)
                found_profiles += 1
                print("✓ FOUND")
            else:
                print("✗ NOT FOUND")
            
            archive_data["platforms"][platform] = platform_data
            
        except Exception as e:
            platform_data = {
                "url": url,
                "error": str(e),
                "accessible": False,
                "timestamp": datetime.now().isoformat()
            }
            archive_data["platforms"][platform] = platform_data
            print("✗ ERROR")
        
        time.sleep(1)  
    
    archive_data["summary"] = {
        "total_platforms_checked": total_checked,
        "profiles_found": found_profiles,
        "success_rate": f"{(found_profiles/total_checked)*100:.1f}%" if total_checked > 0 else "0%"
    }
    
    filename = f"social_archive_{username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(archive_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n[*] Archive saved to: {filename}")
    print(f"[*] Found {found_profiles} profiles out of {total_checked} platforms checked")
    print(f"[*] Success rate: {archive_data['summary']['success_rate']}")
    
    return archive_data

def extract_title(html):
    try:
        import re
        title_match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
        if title_match:
            return title_match.group(1).strip()
    except:
        pass
    return "No title found"

def extract_description(html):
    try:
        import re
        desc_match = re.search(r'<meta name="description" content="(.*?)"', html, re.IGNORECASE)
        if desc_match:
            return desc_match.group(1).strip()
    except:
        pass
    return "No description found"

def main():
    parser = argparse.ArgumentParser(description="Social Media Archiver")
    parser.add_argument("--target", help="Username to archive", required=False)
    args = parser.parse_args()
    
    username = args.target if args.target else input("\n[?] Enter username to archive: ").strip()
    
    if not username:
        print("[!] No username provided!")
        return
    
    archive_social_media(username)

if __name__ == "__main__":
    main()

