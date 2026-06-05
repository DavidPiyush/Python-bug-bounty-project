# import pyfiglet
# from termcolor import colored
import sys

# url = input("Enter a URL to analyze : ").strip()
# print(f"URL : {url}")

# def print_big_title(text):
#     ascii_art = pyfiglet.figlet_format(text,font='slant')
#     print(colored(ascii_art,'cyan'))



# print_big_title("HEADER ANALYZER")

# taking input from user
# if len(sys.argv) > 1:
#     url = sys.argv[1].strip()

# else:
#     url = input("Enter URL: ").strip()

# if not url.startswith(('http://','https://')):
#     url = 'https://' +url

# print(f"Analyzing: {url}")



import requests
from datetime import datetime

def check_security_headers(url):
    """
    Checks a URL for missing security headers.
    Returns a report of findings.
    """

    # Security headers we care about and why
    headers_to_check = {
        "Strict-Transport-Security": {
            "risk": "HIGH",
            "why": "Missing HSTS allows downgrade attacks from HTTPS to HTTP"
        },
        "Content-Security-Policy": {
            "risk": "HIGH", 
            "why": "Missing CSP makes XSS attacks significantly easier"
        },
        "X-Frame-Options": {
            "risk": "MEDIUM",
            "why": "Missing allows clickjacking — tricking users into clicks"
        },
        "X-Content-Type-Options": {
            "risk": "LOW",
            "why": "Missing allows MIME type sniffing attacks"
        },
        "Referrer-Policy": {
            "risk": "LOW",
            "why": "Missing leaks URL info to third parties"
        },
        "Permissions-Policy": {
            "risk": "LOW",
            "why": "Missing allows unrestricted access to browser features"
        },
    }

    print(f"\n{'='*60}")
    print(f"🔍 Security Header Check")
    print(f"Target : {url}")
    print(f"Time   : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")

    try:
        # Don't follow redirects — we want the actual response
        response = requests.get(
            url,
            timeout=10,
            allow_redirects=True,
            headers={"User-Agent": "Mozilla/5.0 (Security Scanner)"}
        )

        print(f"Status Code : {response.status_code}")
        print(f"Final URL   : {response.url}")

        # Show what technology is revealed
        print(f"\n--- 🖥️  Technology Fingerprint ---")
        for info_header in ["Server", "X-Powered-By", "Via", "X-Generator"]:
            if info_header in response.headers:
                print(f"  {info_header}: {response.headers[info_header]}  ← revealed!")

        # Check security headers
        print(f"\n--- 🛡️  Security Header Analysis ---\n")

        missing = []
        present = []

        for header, info in headers_to_check.items():
            if header in response.headers:
                present.append(header)
                print(f"  ✅ {header}")
                print(f"     Value: {response.headers[header][:80]}")
            else:
                missing.append((header, info))
                print(f"  ❌ {header} — MISSING")
                print(f"     Risk : {info['risk']}")
                print(f"     Why  : {info['why']}")
            print()

        # Summary
        print(f"--- 📊 Summary ---")
        print(f"  Headers Present : {len(present)}/{len(headers_to_check)}")
        print(f"  Headers Missing : {len(missing)}/{len(headers_to_check)}")

        if missing:
            high_risk = [h for h, i in missing if i["risk"] == "HIGH"]
            if high_risk:
                print(f"\n  🚨 High Risk Missing: {', '.join(high_risk)}")
                print(f"  → These are worth reporting in bug bounty programs")

        print(f"\n{'='*60}\n")

    except requests.exceptions.ConnectionError:
        print(f"❌ Could not connect to {url}")
    except requests.exceptions.Timeout:
        print(f"⏱️  Request timed out for {url}")
    except Exception as e:
        print(f"Error: {e}")


# Run it
if __name__ == "__main__":
    targets = [
        "https://httpbin.org",
        "https://example.com",
        # Add any website you want to check
    ]

    for target in targets:
        check_security_headers(target)
