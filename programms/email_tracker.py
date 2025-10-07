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
from bs4 import BeautifulSoup
import random

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
]

def get_user_agent():
    return random.choice(USER_AGENTS)

def Instagram(email):
    try:
        session = requests.Session()
        headers = {
            'User-Agent': get_user_agent(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Origin': 'https://www.instagram.com',
            'Connection': 'keep-alive',
            'Referer': 'https://www.instagram.com/'
        }
        data = {"email": email}
        response = session.get("https://www.instagram.com/accounts/emailsignup/", headers=headers)
        if response.status_code != 200:
            return False
        token = session.cookies.get('csrftoken')
        if not token:
            return False
        headers["x-csrftoken"] = token
        headers["Referer"] = "https://www.instagram.com/accounts/emailsignup/"
        response = session.post(
            url="https://www.instagram.com/api/v1/web/accounts/web_create_ajax/attempt/",
            headers=headers,
            data=data
        )
        if response.status_code == 200:
            if "Another account is using the same email." in response.text or "email_is_taken" in response.text:
                return True
            return False
        return False
    except:
        return False

def Twitter(email):
    try:
        session = requests.Session()
        response = session.get(
            url="https://api.twitter.com/i/users/email_available.json",
            params={"email": email}
        )
        if response.status_code == 200:
            return response.json()["taken"]
        return False
    except:
        return False

def Pinterest(email):
    try:
        session = requests.Session()
        response = session.get(
            "https://www.pinterest.com/_ngjs/resource/EmailExistsResource/get/",
            params={"source_url": "/", "data": '{"options": {"email": "' + email + '"}, "context": {}}'}
        )
        if response.status_code == 200:
            data = response.json()["resource_response"]
            if data["message"] == "Invalid email.":
                return False
            return data["data"] is not False
        return False
    except:
        return False

def Imgur(email):
    try:
        session = requests.Session()
        headers = {
            'User-Agent': get_user_agent(),
            'Accept': '*/*',
            'Accept-Language': 'en,en-US;q=0.5',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'https://imgur.com',
            'DNT': '1',
            'Connection': 'keep-alive',
            'TE': 'Trailers',
        }
        r = session.get("https://imgur.com/register?redirect=%2Fuser", headers=headers)
        headers["X-Requested-With"] = "XMLHttpRequest"
        data = {'email': email}
        response = session.post('https://imgur.com/signin/ajax_email_available', headers=headers, data=data)
        if response.status_code == 200:
            data = response.json()['data']
            if data["available"]:
                return False
            if "Invalid email domain" in response.text:
                return False
            return True
        return False
    except:
        return False

def Patreon(email):
    try:
        session = requests.Session()
        headers = {
            'User-Agent': get_user_agent(),
            'Accept': '*/*',
            'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Origin': 'https://www.plurk.com',
            'DNT': '1',
            'Connection': 'keep-alive',
        }
        data = {'email': email}
        response = session.post('https://www.plurk.com/Users/isEmailFound', headers=headers, data=data)
        if response.status_code == 200:
            return "True" in response.text
        return False
    except:
        return False

def Spotify(email):
    try:
        session = requests.Session()
        headers = {
            'User-Agent': get_user_agent(),
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.5',
            'DNT': '1',
            'Connection': 'keep-alive',
        }
        params = {'validate': '1', 'email': email}
        response = session.get('https://spclient.wg.spotify.com/signup/public/v1/account',
                headers=headers,
                params=params)
        if response.status_code == 200:
            status = response.json()["status"]
            return status == 20
        return False
    except:
        return False

def FireFox(email):
    try:
        session = requests.Session()
        data = {"email": email}
        response = session.post("https://api.accounts.firefox.com/v1/account/status", data=data)
        if response.status_code == 200:
            return "false" not in response.text
        return False
    except:
        return False

def LastPass(email):
    try:
        session = requests.Session()
        headers = {
            'User-Agent': get_user_agent(),
            'Accept': '*/*',
            'Accept-Language': 'en,en-US;q=0.5',
            'Referer': 'https://lastpass.com/',
            'X-Requested-With': 'XMLHttpRequest',
            'DNT': '1',
            'Connection': 'keep-alive',
            'TE': 'Trailers',
        }
        params = {
            'check': 'avail',
            'skipcontent': '1',
            'mistype': '1',
            'username': email,
        }
        response = session.get(
            'https://lastpass.com/create_account.php?check=avail&skipcontent=1&mistype=1&username='+str(email).replace("@", "%40"),       
            params=params,
            headers=headers)
        if response.status_code == 200:
            if "no" in response.text:
                return True
            return False
        return False
    except:
        return False

def Archive(email):
    try:
        session = requests.Session()
        headers = {
            'User-Agent': get_user_agent(),
            'Accept': '*/*',
            'Accept-Language': 'en,en-US;q=0.5',
            'Content-Type': 'multipart/form-data; boundary=---------------------------',
            'Origin': 'https://archive.org',
            'Connection': 'keep-alive',
            'Referer': 'https://archive.org/account/signup',
            'Sec-GPC': '1',
            'TE': 'Trailers',
        }
        data = '-----------------------------\r\nContent-Disposition: form-data; name="input_name"\r\n\r\nusername\r\n-----------------------------\r\nContent-Disposition: form-data; name="input_value"\r\n\r\n' + email + \
            '\r\n-----------------------------\r\nContent-Disposition: form-data; name="input_validator"\r\n\r\ntrue\r\n-----------------------------\r\nContent-Disposition: form-data; name="submit_by_js"\r\n\r\ntrue\r\n-------------------------------\r\n'
        response = session.post('https://archive.org/account/signup', headers=headers, data=data)
        if response.status_code == 200:
            return "is already taken." in response.text
        return False
    except:
        return False

def PornHub(email):
    try:
        session = requests.Session()
        headers = {
            'User-Agent': get_user_agent(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en,en-US;q=0.5',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        response = session.get("https://www.pornhub.com/signup", headers=headers)
        if response.status_code == 200:
            token = BeautifulSoup(response.content, features="html.parser").find(attrs={"name": "token"})
            if token is None:
                return False
            token = token.get("value")
        else:
            return False
        params = {'token': token}
        data = {'check_what': 'email', 'email': email}
        response = session.post('https://www.pornhub.com/user/create_account_check', headers=headers, params=params, data=data) 
        if response.status_code == 200:
            if response.json()["error_message"] == "Email has been taken.":
                return True
            return False
        return False
    except:
        return False

def Xnxx(email):
    try:
        session = requests.Session()
        headers = {
            'User-Agent': get_user_agent(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-en',
            'Host': 'www.xnxx.com',
            'Referer': 'https://www.google.com/',
            'Connection': 'keep-alive'
        }
        cookie = session.get('https://www.xnxx.com', headers=headers)
        if cookie.status_code != 200:
            return False
        headers['Referer'] = 'https://www.xnxx.com/video-holehe/palenath_fucks_xnxx_with_holehe'
        headers['X-Requested-With'] = 'XMLHttpRequest'
        email = email.replace('@', '%40')
        response = session.get(f'https://www.xnxx.com/account/checkemail?email={email}', headers=headers, cookies=cookie.cookies)
        if response.status_code == 200:
            try:
                if response.json()['message'] == "This email is already in use or its owner has excluded it from our website.":
                    return True
                elif response.json()['message'] == "Invalid email address.": 
                    return False
            except:
                pass    
            if response.json()['result'] == "false":
                return True
            elif response.json()['code'] == 1:
                return True
            elif response.json()['result'] == "true":
                return False
            elif response.json()['code'] == 0:
                return False  
            else:
                return False
        return False
    except:
        return False

def Xvideo(email):
    try:
        session = requests.Session()
        headers = {
            'User-Agent': get_user_agent(),
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'keep-alive',
            'Referer': 'https://www.xvideos.com/',
        }
        params = {'email': email}
        response = session.get('https://www.xvideos.com/account/checkemail', headers=headers, params=params)
        if response.status_code == 200:
            try:
                if response.json()['message'] == "This email is already in use or its owner has excluded it from our website.": 
                    return True
                elif response.json()['message'] == "Invalid email address.": 
                    return False
            except: 
                pass    
            if response.json()['result'] == "false":
                return True
            elif response.json()['code'] == 1:
                return True
            elif response.json()['result'] == "true":
                return False
            elif response.json()['code'] == 0:
                return False  
            else:
                return False
        return False
    except:
        return False

def main():
    parser = argparse.ArgumentParser(description="Email Tracker OSINT Tool")
    parser.add_argument("--target", help="Email to track", required=False)
    args = parser.parse_args()
    
    email = args.target if args.target else input("Enter email address: ").strip()
    
    if not email:
        print("No email provided!")
        return
    
    print(f"\n[*] Checking email: {email}")
    print(f"[*] User-Agent: {get_user_agent()}")
    print(f"[*] Scanning across 12 platforms...\n")
    
    sites = [
        ("Instagram", Instagram),
        ("Twitter", Twitter),
        ("Pinterest", Pinterest),
        ("Imgur", Imgur),
        ("Patreon", Patreon),
        ("Spotify", Spotify),
        ("FireFox", FireFox),
        ("LastPass", LastPass),
        ("Archive", Archive),
        ("PornHub", PornHub),
        ("Xnxx", Xnxx),
        ("Xvideo", Xvideo)
    ]
    
    site_founds = []
    found = 0
    not_found = 0
    
    for name, func in sites:
        result = func(email)
        if result:
            print(f"[+] {name}: Found")
            site_founds.append(name)
            found += 1
        else:
            print(f"[-] {name}: Not Found")
            not_found += 1
    
    if found:
        print(f"\n[*] Total Found ({found}): {', '.join(site_founds)}")
    print(f"[*] Not Found: {not_found}")

if __name__ == "__main__":
    main()

