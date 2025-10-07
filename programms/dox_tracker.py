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

def main():
    parser = argparse.ArgumentParser(description="DoxTracker OSINT Tool")
    parser.add_argument("--target", help="Target to search", required=False)
    args = parser.parse_args()
    
    print("\n[*] DoxTracker - People Search Tool")
    print("[0] Back")
    print("[1] Username")
    print("[2] LastName, FirstName")
    print("[3] Other")
    
    search_type = input("\n[?] Search Type -> ").strip()
    
    if search_type in ['00', '0']:
        return
    
    if search_type in ['01', '1']:
        search = input("[?] Username -> ").strip()
    elif search_type in ['02', '2']:
        name = input("[?] LastName -> ").strip()
        first_name = input("[?] FirstName -> ").strip()
    elif search_type in ['03', '3']:
        search = input("[?] Search -> ").strip()
    else:
        print("[!] Invalid choice!")
        return
    
    if search_type in ['1', '01','2','02','3','03']:
        print("\n[0] Back")
        print("[1] Facebook.com")
        print("[2] Youtube.com")
        print("[3] Twitter.com")
        print("[4] Tiktok.com")
        print("[5] Peekyou.com")
        print("[6] Tumblr.com")
        print("[7] PagesJaunes.fr")
        
        while True:
            choice = input("\n[?] Site -> ").strip()
            
            if choice in ['0', '00']:
                break
            
            elif choice in ['01', '1']:
                if search_type in ['01', '1', '3', '03']:
                    webbrowser.open(f"https://www.facebook.com/search/top/?init=quick&q={search}")
                elif search_type in ['02', '2']:
                    webbrowser.open(f"https://www.facebook.com/search/top/?init=quick&q={name}%20{first_name}")
            
            elif choice in ['02', '2']:
                if search_type in ['01', '1', '3', '03']:
                    webbrowser.open(f"https://www.youtube.com/results?search_query={search}")
                elif search_type in ['02', '2']:
                    webbrowser.open(f"https://www.youtube.com/results?search_query={name}+{first_name}")
            
            elif choice in ['03', '3']:
                if search_type in ['01', '1', '3', '03']:
                    webbrowser.open(f"https://twitter.com/search?f=users&vertical=default&q={search}")
                elif search_type in ['02', '2']:
                    webbrowser.open(f"https://twitter.com/search?f=users&vertical=default&q={name}%20{first_name}")
            
            elif choice in ['04', '4']:
                if search_type in ['01', '1', '3', '03']:
                    webbrowser.open(f"https://www.tiktok.com/search?q={search}")
                elif search_type in ['02', '2']:
                    webbrowser.open(f"https://www.tiktok.com/search?q={name}%20{first_name}")
            
            elif choice in ['05', '5']:
                if search_type in ['01', '1', '3', '03']:
                    webbrowser.open(f"https://www.peekyou.com/{search}")
                elif search_type in ['02', '2']:
                    webbrowser.open(f"https://www.peekyou.com/{name}_{first_name}")
            
            elif choice in ['06', '6']:
                if search_type in ['01', '1', '3', '03']:
                    webbrowser.open(f"https://www.tumblr.com/search/{search}")
                elif search_type in ['02', '2']:
                    webbrowser.open(f"https://www.tumblr.com/search/{name}%20{first_name}")
            
            elif choice in ['07', '7']:
                if search_type in ['01', '1', '3', '03']:
                    webbrowser.open(f"https://www.pagesjaunes.fr/pagesblanches/recherche?quoiqui={search}")
                elif search_type in ['02', '2']:
                    webbrowser.open(f"https://www.pagesjaunes.fr/pagesblanches/recherche?quoiqui={name}%20{first_name}")

if __name__ == "__main__":
    main()

