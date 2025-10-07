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

import webbrowser
import argparse
import time

def main():
    parser = argparse.ArgumentParser(description="People Tracker")
    parser.add_argument("--target", help="Name to search", required=False)
    args = parser.parse_args()
    
    print("\n[*] People Tracker - Search across multiple platforms")
    print("[1] Name")
    print("[2] Phone number")
    print("[3] Dead")
    print("[4] IP")
    
    opt = input("\n[?] Select option: ").strip()
    
    if opt == "1":
        name = input("[?] LastName: ").strip()
        first_name = input("[?] FirstName: ").strip()
        
        print("\n[*] Opening search results in browser...")
        webbrowser.open(f"https://www.facebook.com/search/top/?init=quick&q={name} {first_name}")
        time.sleep(1)
        webbrowser.open(f"https://twitter.com/search?f=users&vertical=default&q={name} {first_name}")
        time.sleep(1)
        webbrowser.open(f"https://www.peekyou.com/{name}_{first_name}")
        
    elif opt == "2":
        num = input("[?] Phone Number: ").strip()
        print("\n[*] Opening search results in browser...")
        webbrowser.open(f"https://www.facebook.com/search/top/?init=quick&q={num}")
        
    elif opt == "4":
        ip = input("[?] IP Address: ").strip()
        print("\n[*] Opening IP lookup...")
        webbrowser.open(f"http://whatismyipaddress.com/ip/{ip}")

if __name__ == "__main__":
    main()

