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
from prettytable import PrettyTable

def main():
    parser = argparse.ArgumentParser(description="Breach Database Lookup")
    parser.add_argument("--target", help="Email or username", required=False)
    args = parser.parse_args()
    
    email = args.target if args.target else input("\n[?] Enter email or username: ").strip()
    
    if not email:
        print("[!] No target provided!")
        return
    
    print(f"\n[*] Searching breached databases for: {email}")
    
    try:
        url = f"https://leakcheck.net/api/public?key=49535f49545f5245414c4c595f4150495f4b4559&check={email}"
        response = requests.get(url)
        data = response.json()
        
        if data.get('success'):
            table = PrettyTable()
            table.field_names = ["Breach Name", "Date"]
            
            sources = data.get('sources', [])
            for source in sources:
                table.add_row([source.get('name'), source.get('date')])
            
            print(f"\n[+] Found {data.get('found', 0)} breaches!")
            print(table)
        else:
            print(f"\n[-] No breaches found for {email}")
    except Exception as e:
        print(f"[!] Error: {e}")

if __name__ == "__main__":
    main()

