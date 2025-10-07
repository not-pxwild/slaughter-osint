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
import dns.resolver
import socket
import argparse
import json
from datetime import datetime
import ssl

def analyze_domain(domain):
    print(f"\n[*] Analyzing domain: {domain}")
    print("[*] Performing comprehensive domain analysis...\n")
    
    analysis = {
        "domain": domain,
        "timestamp": datetime.now().isoformat(),
        "dns_records": {},
        "ssl_info": {},
        "whois_info": {},
        "subdomains": [],
        "security_headers": {},
        "summary": {}
    }
    
    print("[*] DNS Records Analysis:")
    dns_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'CNAME', 'SOA']
    
    for record_type in dns_types:
        try:
            answers = dns.resolver.resolve(domain, record_type)
            records = [str(answer) for answer in answers]
            analysis["dns_records"][record_type] = records
            print(f"    {record_type}: {', '.join(records)}")
        except Exception as e:
            analysis["dns_records"][record_type] = f"Error: {str(e)}"
            print(f"    {record_type}: Error - {str(e)}")
    
    print(f"\n[*] SSL Certificate Analysis:")
    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                analysis["ssl_info"] = {
                    "subject": dict(x[0] for x in cert['subject']),
                    "issuer": dict(x[0] for x in cert['issuer']),
                    "version": cert['version'],
                    "serial_number": cert['serialNumber'],
                    "not_before": cert['notBefore'],
                    "not_after": cert['notAfter'],
                    "valid": True
                }
                print(f"    Subject: {analysis['ssl_info']['subject']}")
                print(f"    Issuer: {analysis['ssl_info']['issuer']}")
                print(f"    Valid Until: {analysis['ssl_info']['not_after']}")
    except Exception as e:
        analysis["ssl_info"] = {"error": str(e), "valid": False}
        print(f"    SSL Error: {str(e)}")
    
    print(f"\n[*] Security Headers Analysis:")
    try:
        response = requests.get(f"https://{domain}", timeout=10)
        security_headers = [
            'Strict-Transport-Security',
            'Content-Security-Policy',
            'X-Frame-Options',
            'X-Content-Type-Options',
            'X-XSS-Protection',
            'Referrer-Policy',
            'Permissions-Policy'
        ]
        
        for header in security_headers:
            if header in response.headers:
                analysis["security_headers"][header] = response.headers[header]
                print(f"    {header}: {response.headers[header]}")
            else:
                analysis["security_headers"][header] = "Not present"
                print(f"    {header}: Not present")
    except Exception as e:
        analysis["security_headers"] = {"error": str(e)}
        print(f"    Headers Error: {str(e)}")
    
    print(f"\n[*] Subdomain Discovery:")
    common_subdomains = [
        'www', 'mail', 'ftp', 'admin', 'blog', 'shop', 'api', 'dev', 'test',
        'staging', 'app', 'cdn', 'static', 'img', 'images', 'js', 'css'
    ]
    
    found_subdomains = []
    for subdomain in common_subdomains:
        try:
            full_domain = f"{subdomain}.{domain}"
            socket.gethostbyname(full_domain)
            found_subdomains.append(full_domain)
            print(f"    Found: {full_domain}")
        except:
            pass
    
    analysis["subdomains"] = found_subdomains
    
    print(f"\n[*] WHOIS Information:")
    try:
        import whois
        w = whois.whois(domain)
        analysis["whois_info"] = {
            "registrar": str(w.registrar) if w.registrar else "Unknown",
            "creation_date": str(w.creation_date) if w.creation_date else "Unknown",
            "expiration_date": str(w.expiration_date) if w.expiration_date else "Unknown",
            "name_servers": list(w.name_servers) if w.name_servers else [],
            "status": list(w.status) if w.status else []
        }
        print(f"    Registrar: {analysis['whois_info']['registrar']}")
        print(f"    Created: {analysis['whois_info']['creation_date']}")
        print(f"    Expires: {analysis['whois_info']['expiration_date']}")
    except Exception as e:
        analysis["whois_info"] = {"error": str(e)}
        print(f"    WHOIS Error: {str(e)}")
    
    analysis["summary"] = {
        "dns_records_found": len([r for r in analysis["dns_records"].values() if not str(r).startswith("Error")]),
        "ssl_valid": analysis["ssl_info"].get("valid", False),
        "security_headers_count": len([h for h in analysis["security_headers"].values() if h != "Not present"]),
        "subdomains_found": len(found_subdomains),
        "analysis_complete": True
    }
    
    filename = f"domain_analysis_{domain}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(analysis, f, indent=2, ensure_ascii=False)
    
    print(f"\n[*] Analysis saved to: {filename}")
    print(f"[*] DNS Records: {analysis['summary']['dns_records_found']}")
    print(f"[*] SSL Valid: {analysis['summary']['ssl_valid']}")
    print(f"[*] Security Headers: {analysis['summary']['security_headers_count']}")
    print(f"[*] Subdomains Found: {analysis['summary']['subdomains_found']}")
    
    return analysis

def main():
    parser = argparse.ArgumentParser(description="Domain Analyzer")
    parser.add_argument("--target", help="Domain to analyze", required=False)
    args = parser.parse_args()
    
    domain = args.target if args.target else input("\n[?] Enter domain to analyze: ").strip()
    
    if not domain:
        print("[!] No domain provided!")
        return
    
    domain = domain.replace('https://', '').replace('http://', '').replace('www.', '')
    
    analyze_domain(domain)

if __name__ == "__main__":
    main()

