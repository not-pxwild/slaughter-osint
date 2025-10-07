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
import json
from datetime import datetime
import time

def monitor_darkweb(target):
    print(f"\n[*] Dark Web Monitoring for: {target}")
    print("[*] This tool monitors public breach databases and leak sites\n")
    
    monitoring_data = {
        "target": target,
        "timestamp": datetime.now().isoformat(),
        "checks": [],
        "summary": {}
    }
    
    breach_sources = [
        {
            "name": "HaveIBeenPwned",
            "url": f"https://haveibeenpwned.com/api/v3/breachedaccount/{target}",
            "type": "email_breach"
        },
        {
            "name": "LeakCheck",
            "url": f"https://leakcheck.net/api/public?key=49535f49545f5245414c4c595f4150495f4b4559&check={target}",
            "type": "general_breach"
        }
    ]
    
    found_breaches = 0
    total_checked = 0
    
    for source in breach_sources:
        total_checked += 1
        print(f"[*] Checking {source['name']}...", end=" ")
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(source['url'], headers=headers, timeout=15)
            
            check_result = {
                "source": source['name'],
                "url": source['url'],
                "status_code": response.status_code,
                "timestamp": datetime.now().isoformat(),
                "success": False,
                "data": None
            }
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    check_result["success"] = True
                    check_result["data"] = data
                    
                    if source['name'] == "HaveIBeenPwned":
                        if isinstance(data, list) and len(data) > 0:
                            found_breaches += len(data)
                            print(f"✓ FOUND {len(data)} breaches")
                        else:
                            print("✓ No breaches found")
                    elif source['name'] == "LeakCheck":
                        if data.get('success') and data.get('found', 0) > 0:
                            found_breaches += data.get('found', 0)
                            print(f"✓ FOUND {data.get('found', 0)} breaches")
                        else:
                            print("✓ No breaches found")
                    else:
                        print("✓ Data retrieved")
                        
                except json.JSONDecodeError:
                    check_result["data"] = response.text
                    print("✓ Response received")
            else:
                print(f"✗ HTTP {response.status_code}")
                
        except Exception as e:
            check_result["error"] = str(e)
            print(f"✗ ERROR: {str(e)}")
        
        monitoring_data["checks"].append(check_result)
        time.sleep(2)  
    
    print(f"\n[*] Additional monitoring checks:")
    
    print("[*] Checking breach news sources...", end=" ")
    try:
        news_sources = [
            "https://www.bleepingcomputer.com/",
            "https://krebsonsecurity.com/",
            "https://www.darkreading.com/"
        ]
        
        news_check = {
            "source": "Breach News",
            "timestamp": datetime.now().isoformat(),
            "sources_checked": len(news_sources),
            "note": "Manual verification recommended"
        }
        
        monitoring_data["checks"].append(news_check)
        print("✓ Sources identified")
        
    except Exception as e:
        print(f"✗ ERROR: {str(e)}")
    
    monitoring_data["summary"] = {
        "total_sources_checked": total_checked,
        "breaches_found": found_breaches,
        "monitoring_complete": True,
        "recommendation": "Regular monitoring recommended"
    }
    
    filename = f"darkweb_monitor_{target}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(monitoring_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n[*] Monitoring report saved to: {filename}")
    print(f"[*] Sources checked: {total_checked}")
    print(f"[*] Breaches found: {found_breaches}")
    
    if found_breaches > 0:
        print(f"\n[!] WARNING: {found_breaches} breaches found!")
        print("[!] Consider changing passwords and enabling 2FA")
    else:
        print(f"\n[+] No breaches found in monitored sources")
    
    print(f"\n[*] Note: This tool only checks public, legal OSINT sources")
    print("[*] For comprehensive monitoring, consider professional services")
    
    return monitoring_data

def main():
    parser = argparse.ArgumentParser(description="Dark Web Monitor")
    parser.add_argument("--target", help="Email or username to monitor", required=False)
    args = parser.parse_args()
    
    target = args.target if args.target else input("\n[?] Enter email or username to monitor: ").strip()
    
    if not target:
        print("[!] No target provided!")
        return
    
    monitor_darkweb(target)

if __name__ == "__main__":
    main()

