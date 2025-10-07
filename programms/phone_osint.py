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

import phonenumbers
from phonenumbers import geocoder, carrier, timezone
import argparse

def main():
    parser = argparse.ArgumentParser(description="Phone Number OSINT Tool")
    parser.add_argument("--target", help="Phone number to lookup", required=False)
    args = parser.parse_args()
    
    phone_number = args.target if args.target else input("\nEnter phone number (with country code): ").strip()
    
    if not phone_number:
        print("No phone number provided!")
        return
    
    print(f"\n[*] Analyzing phone number: {phone_number}")
    print(f"[*] Retrieving information...\n")
    
    try:
        parsed_number = phonenumbers.parse(phone_number, None)
        if phonenumbers.is_valid_number(parsed_number):
            status = "Valid"
        else:
            status = "Invalid"
        
        if phone_number.startswith("+"):
            country_code = "+" + phone_number[1:3]
        else:
            country_code = "None"
        
        try:
            operator = carrier.name_for_number(parsed_number, "en")
        except:
            operator = "None"
        
        try:
            type_number = "Mobile" if phonenumbers.number_type(parsed_number) == phonenumbers.PhoneNumberType.MOBILE else "Fixe"
        except:
            type_number = "None"
        
        try:
            timezones = timezone.time_zones_for_number(parsed_number)
            timezone_info = timezones[0] if timezones else None
        except:
            timezone_info = "None"
        
        try:
            country = phonenumbers.region_code_for_number(parsed_number)
        except:
            country = "None"
        
        try:
            region = geocoder.description_for_number(parsed_number, "en")
        except:
            region = "None"
        
        try:
            formatted_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.NATIONAL)
        except:
            formatted_number = "None"
        
        print("=" * 120)
        print(f"[+] Phone         : {phone_number}")
        print(f"[+] Formatted     : {formatted_number}")
        print(f"[+] Status        : {status}")
        print(f"[+] Country Code  : {country_code}")
        print(f"[+] Country       : {country}")
        print(f"[+] Region        : {region}")
        print(f"[+] Timezone      : {timezone_info}")
        print(f"[+] Operator      : {operator}")
        print(f"[+] Type Number   : {type_number}")
        print("=" * 120)
    except Exception as e:
        print(f"[!] Invalid phone number format: {e}")

if __name__ == "__main__":
    main()
