import requests
import time
import sys
import pyfiglet
from termcolor import colored

def fuzz(base_url, wordlist_path):
    found = []
    total = 0

    with open(wordlist_path, "r") as f:
        words = f.read().splitlines()  # load all at once, cleaner

    print(colored(f"\n[*] Starting fuzz on: {base_url}", "yellow"))
    print(colored(f"[*] Wordlist size: {len(words)} words\n", "yellow"))

    for word in words:
        if not word.strip():   # skip empty lines
            continue

        url = f"{base_url.rstrip('/')}/{word.strip()}"
        total += 1

        try:
            response = requests.get(
                url,
                timeout=5,
                allow_redirects=False,  # don't follow redirects
                headers={"User-Agent": "Mozilla/5.0"}
            )

            # Color code by status
            if response.status_code == 200:
                print(colored(f"  [200] ✅ {url}", "green"))
                found.append(url)

            elif response.status_code == 403:
                print(colored(f"  [403] 🔒 {url} — Forbidden (exists!)", "yellow"))
                found.append(url)

            elif response.status_code == 301 or response.status_code == 302:
                print(colored(f"  [{response.status_code}] ➡️  {url} — Redirect", "cyan"))
                found.append(url)

            elif response.status_code == 500:
                print(colored(f"  [500] 💥 {url} — Server Error!", "red"))
                found.append(url)

            # 404 = silently skip, no output

            time.sleep(0.3)   # polite delay

        except requests.exceptions.ConnectionError:
            print(colored(f"  [ERR] Could not connect to {url}", "red"))
        except requests.exceptions.Timeout:
            print(colored(f"  [TMO] Timeout on {url}", "red"))

    # Summary
    print(colored(f"\n{'='*50}", "cyan"))
    print(colored(f"  Scan complete!", "cyan"))
    print(colored(f"  Checked : {total}", "cyan"))
    print(colored(f"  Found   : {len(found)} interesting paths", "green"))
    if found:
        print(colored(f"\n  Results:", "green"))
        for url in found:
            print(colored(f"    → {url}", "green"))
    print(colored(f"{'='*50}\n", "cyan"))


def get_print():
    ascii_art = pyfiglet.figlet_format("FUZZER", font='slant')
    print(colored(ascii_art, 'cyan'))


def get_input():
    get_print()   # ← print banner first, then ask for input

    if len(sys.argv) > 2:
        url = sys.argv[1].strip()
        wordlist = sys.argv[2].strip()
    else:
        url = input("Enter URL    : ").strip()
        wordlist = input("Enter Wordlist: ").strip()

    if not url.startswith(('http://', 'https://')):
        url = "https://" + url

    fuzz(url, wordlist)


get_input()