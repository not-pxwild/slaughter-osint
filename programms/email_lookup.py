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

import dns.resolver
import requests
import re
import argparse

def GetEmailInfo(email):
    info = {}
    try:
        domain_all = email.split('@')[-1]
    except:
        domain_all = None
    try:
        name = email.split('@')[0]
    except:
        name = None
    try:
        domain = re.search(r"@([^@.]+)\.", email).group(1)
    except:
        domain = None
    try:
        tld = f".{email.split('.')[-1]}"
    except:
        tld = None
    
    try:
        mx_records = dns.resolver.resolve(domain_all, 'MX')
        mx_servers = [str(record.exchange) for record in mx_records]
        info["mx_servers"] = mx_servers
    except dns.resolver.NoAnswer:
        info["mx_servers"] = None
    except dns.resolver.NXDOMAIN:
        info["mx_servers"] = None
    
    try:
        spf_records = dns.resolver.resolve(domain_all, 'TXT')
        info["spf_records"] = [str(record) for record in spf_records]
    except dns.resolver.NoAnswer:
        info["spf_records"] = None
    except dns.resolver.NXDOMAIN:
        info["spf_records"] = None
    
    try:
        dmarc_records = dns.resolver.resolve(f'_dmarc.{domain_all}', 'TXT')
        info["dmarc_records"] = [str(record) for record in dmarc_records]
    except dns.resolver.NoAnswer:
        info["dmarc_records"] = None
    except dns.resolver.NXDOMAIN:
        info["dmarc_records"] = None
    
    if info.get("mx_servers"):
        for server in info["mx_servers"]:
            if "google.com" in server:
                info["google_workspace"] = True
            elif "outlook.com" in server:
                info["microsoft_365"] = True
    
    return info, domain_all, domain, tld, name

def main():
    parser = argparse.ArgumentParser(description="Email Lookup OSINT Tool")
    parser.add_argument("--target", help="Email to lookup", required=False)
    args = parser.parse_args()
    
    email = args.target if args.target else input("\nEnter email address: ").strip()
    
    if not email:
        print("No email provided!")
        return
    
    print(f"\n[*] Looking up email: {email}")
    print(f"[*] Retrieving information...\n")
    
    info, domain_all, domain, tld, name = GetEmailInfo(email)
    
    try:
        mx_servers = info["mx_servers"]
        mx_servers = ' / '.join(mx_servers) if mx_servers else None
    except:
        mx_servers = None
    
    try:
        spf_records = info["spf_records"]
    except:
        spf_records = None
    
    try:
        dmarc_records = info["dmarc_records"]
        dmarc_records = ' / '.join(dmarc_records) if dmarc_records else None
    except:
        dmarc_records = None
    
    try:
        google_workspace = info["google_workspace"]
    except:
        google_workspace = None
    
    try:
        mailgun_validation = info["mailgun_validation"]
        mailgun_validation = ' / '.join(mailgun_validation) if mailgun_validation else None
    except:
        mailgun_validation = None
    
    print("=" * 120)
    print(f"[+] Email         : {email}")
    print(f"[+] Name          : {name}")
    print(f"[+] Domain        : {domain}")
    print(f"[+] TLD           : {tld}")
    print(f"[+] Domain All    : {domain_all}")
    print(f"[+] MX Servers    : {mx_servers}")
    print(f"[+] SPF           : {spf_records}")
    print(f"[+] DMARC         : {dmarc_records}")
    print(f"[+] Workspace     : {google_workspace}")
    print(f"[+] Mailgun       : {mailgun_validation}")
    print("=" * 120)

if __name__ == "__main__":
    main()

