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
import argparse

def main():
    parser = argparse.ArgumentParser(description="IP Lookup OSINT Tool")
    parser.add_argument("--target", help="IP address to lookup", required=False)
    args = parser.parse_args()
    
    ip = args.target if args.target else input("Enter IP address: ").strip()
    
    if not ip:
        print("No IP provided!")
        return
    
    print(f"\n[*] Looking up IP: {ip}")
    print(f"[*] Searching for information...\n")
    
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        api = response.json()
        
        status = "Valid" if api.get('status') == "success" else "Invalid"
        country = api.get('country', "None")
        country_code = api.get('countryCode', "None")
        region = api.get('regionName', "None")
        region_code = api.get('region', "None")
        zip_code = api.get('zip', "None")
        city = api.get('city', "None")
        latitude = api.get('lat', "None")
        longitude = api.get('lon', "None")
        timezone = api.get('timezone', "None")
        isp = api.get('isp', "None")
        org = api.get('org', "None")
        as_host = api.get('as', "None")
        
        print("=" * 120)
        print(f"[+] Status    : {status}")
        print(f"[+] Country   : {country} ({country_code})")
        print(f"[+] Region    : {region} ({region_code})")
        print(f"[+] Zip       : {zip_code}")
        print(f"[+] City      : {city}")
        print(f"[+] Latitude  : {latitude}")
        print(f"[+] Longitude : {longitude}")
        print(f"[+] Timezone  : {timezone}")
        print(f"[+] ISP       : {isp}")
        print(f"[+] Org       : {org}")
        print(f"[+] AS        : {as_host}")
        print("=" * 120)
    except Exception as e:
        print(f"[!] Error: {e}")

if __name__ == "__main__":
    main()

