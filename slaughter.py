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

import sys
import subprocess
import os
import getpass
from colorama import Fore, Style, init
from pystyle import Colors, Colorate, Write

init(autoreset=True)

red, green, yellow, blue, cyan, magenta, white, reset = Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.CYAN, Fore.MAGENTA, Fore.WHITE, Fore.RESET

BANNER_COLOR = Colors.cyan_to_blue
MENU_COLOR = Colors.cyan_to_blue
PROMPT_COLOR = Colors.cyan_to_blue
ERROR_COLOR = Colors.cyan_to_blue
INFO_COLOR = Colors.cyan_to_blue
EXIT_COLOR = Colors.cyan_to_blue

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def print_banner():
    clear_screen()
    
    banner = """
                           ▄▄▄▄▄   █    ██     ▄     ▄▀   ▄  █    ▄▄▄▄▀ ▄███▄   █▄▄▄▄ 
                          █     ▀▄ █    █ █     █  ▄▀    █   █ ▀▀▀ █    █▀   ▀  █  ▄▀ 
                        ▄  ▀▀▀▀▄   █    █▄▄█ █   █ █ ▀▄  ██▀▀█     █    ██▄▄    █▀▀▌  
                         ▀▄▄▄▄▀    ███▄ █  █ █   █ █   █ █   █    █     █▄   ▄▀ █  █  
                                       ▀   █ █▄ ▄█  ███     █    ▀      ▀███▀     █   
                                          █   ▀▀▀          ▀                     ▀    
                                         ▀                                            
    """
    
    print(Colorate.Horizontal(BANNER_COLOR, banner))

MAIN_MENU = f""" ┌─ OSINT 
 ├─ SLAUGHTER ┌─────────────────┐                        ┌───────────┐                        ┌────────────┐            
 └─┬──────────┤   OSINT Tools   ├─────────┬──────────────┤   Email   ├────────────┬───────────┤   Social   ├──────│
   |          └─────────────────┘         |              └───────────┘            |           └────────────┘
   ├─ 1)  IP Lookup                       ├─ 12) Email Tracker                   ├─ 17) DoxTracker Search
   ├─ 2)  Phone OSINT                     ├─ 13) Email Lookup                    ├─ 18) Social Media Scanner
   ├─ 3)  Phone Validation                ├─ 14) Email Intelligence              ├─ 19) Username Search
   ├─ 4)  Roblox Info                     ├─ 15) Email Breach Check              ├─ 20) Social Archiver
   ├─ 5)  People Tracker                  ├─ 16) Breach Database                  └─
   ├─ 6)  Link Scanner                    └─
   ├─ 7)  Image EXIF Analysis                                                     
   ├─ 8)  Domain Analyzer                                                          
   ├─ 9)  Advanced People Search                                                   
   ├─ 10) Darkweb Monitor                                                          
   ├─ 11) Metadata Analyzer                                                        
   ├─ 0)  EXIT                                                                     
   └─                                                                              
"""

def run_script(script_name, target_value=None, output_file=None):
    try:
        if target_value:
            cmd = [sys.executable, os.path.join("programms", script_name), "--target", target_value]
        else:
            cmd = [sys.executable, os.path.join("programms", script_name)]
        if output_file:
            cmd.extend(["--out", output_file])
        subprocess.run(cmd)
    except Exception as e:
        print(Colorate.Horizontal(ERROR_COLOR, f"Error running {script_name}: {e}"))
    input(Colorate.Horizontal(INFO_COLOR, "\nPress [Enter] to return to the menu..."))

def main_menu():
    username = getpass.getuser()
    while True:
        print_banner()
        print(Colorate.Horizontal(MENU_COLOR, MAIN_MENU))
        
        choice = input(Colorate.Horizontal(PROMPT_COLOR, f"┌───({username}@slaughter)-[~/Main Menu]\n└─$ ")).strip()
        
        if choice == "0":
            print(Colorate.Horizontal(EXIT_COLOR, "\nGoodbye! Stay safe in your OSINT journey!"))
            break
        elif choice == "1":
            run_script("ip_lookup.py")
        elif choice == "2":
            run_script("phone_osint.py")
        elif choice == "3":
            run_script("phone_validation.py")
        elif choice == "4":
            run_script("roblox_info.py")
        elif choice == "5":
            run_script("people_tracker.py")
        elif choice == "6":
            run_script("link_scanner.py")
        elif choice == "7":
            run_script("image_exif.py")
        elif choice == "8":
            run_script("domain_analyzer.py")
        elif choice == "9":
            run_script("advanced_people_search.py")
        elif choice == "10":
            run_script("darkweb_monitor.py")
        elif choice == "11":
            run_script("metadata_analyzer.py")
        elif choice == "12":
            run_script("email_tracker.py")
        elif choice == "13":
            run_script("email_lookup.py")
        elif choice == "14":
            run_script("email_intelligence.py")
        elif choice == "15":
            run_script("breach_check.py")
        elif choice == "16":
            run_script("breach_database.py")
        elif choice == "17":
            run_script("dox_tracker.py")
        elif choice == "18":
            run_script("social_scanner.py")
        elif choice == "19":
            run_script("username_search.py")
        elif choice == "20":
            run_script("social_archiver.py")
        else:
            print(Colorate.Horizontal(ERROR_COLOR, "Invalid option. Please try again."))
            input(Colorate.Horizontal(INFO_COLOR, "Press Enter to continue..."))

def main():
    main_menu()

if __name__ == "__main__":
    main()