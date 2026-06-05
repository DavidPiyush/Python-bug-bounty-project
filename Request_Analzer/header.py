import sys
import requests
from datetime import datetime
import pyfiglet
from termcolor import colored
import argparse  # optional, but cleaner for command-line args

# ------------------------------------------------------------
# 1. Big Title Function
# ------------------------------------------------------------
def print_big_title(text):
    """Print a large ASCII art title in cyan."""
    ascii_art = pyfiglet.figlet_format(text, font='slant')
    print(colored(ascii_art, 'cyan'))

# ------------------------------------------------------------
# 2. Input Handling (supports both command-line and interactive)
# ------------------------------------------------------------
def get_target_url():
    """
    Get URL from command line argument or interactive input.
    Returns a properly formatted URL (with https:// if missing).
    """
    if len(sys.argv) > 1:
        url = sys.argv[1].strip()
    else:
        url = input("Enter URL to analyze: ").strip()
        while not url:
            url = input("Please enter a URL: ").strip()

    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
        print(colored(f"→ Added https:// (URL now: {url})", 'yellow'))
    return url

# ------------------------------------------------------------
# 3. Security Header Check Function (returns structured data)
# ------------------------------------------------------------
def check_security_headers(url, timeout=10, user_agent="Mozilla/5.0 (Security Scanner)", follow_redirects=True):
    """
    Analyze security headers of a given URL.
    Returns a dictionary with all findings.
    """
    HEADERS_TO_CHECK = {
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

    result = {
        "url": url,
        "status_code": None,
        "headers": {},
        "security_report": [],
        "summary": {},
        "tech_fingerprint": [],
        "error": None
    }

    try:
        response = requests.get(
            url,
            timeout=timeout,
            allow_redirects=follow_redirects,
            headers={"User-Agent": user_agent}
        )
        result["status_code"] = response.status_code
        result["url"] = response.url  # final URL after redirects
        result["headers"] = dict(response.headers)

        # Technology fingerprint
        info_headers = ["Server", "X-Powered-By", "Via", "X-Generator"]
        for h in info_headers:
            if h in response.headers:
                result["tech_fingerprint"].append({h: response.headers[h]})

        # Security header analysis
        present = []
        missing = []
        for header, info in HEADERS_TO_CHECK.items():
            if header in response.headers:
                present.append(header)
                result["security_report"].append({
                    "header": header,
                    "present": True,
                    "value": response.headers[header][:200],  # truncate
                    "risk": None,
                    "why": None
                })
            else:
                missing.append((header, info))
                result["security_report"].append({
                    "header": header,
                    "present": False,
                    "value": None,
                    "risk": info["risk"],
                    "why": info["why"]
                })

        # Summary
        high_risk_missing = [h for h, i in missing if i["risk"] == "HIGH"]
        result["summary"] = {
            "total_checked": len(HEADERS_TO_CHECK),
            "present": len(present),
            "missing": len(missing),
            "high_risk_missing": high_risk_missing
        }

    except requests.exceptions.ConnectionError:
        result["error"] = f"Could not connect to {url}"
    except requests.exceptions.Timeout:
        result["error"] = f"Request timed out after {timeout} seconds"
    except Exception as e:
        result["error"] = str(e)

    return result

# ------------------------------------------------------------
# 4. Styled Console Output
# ------------------------------------------------------------
def print_styled_report(report):
    """Print the security report with colors and emojis."""
    if report["error"]:
        print(colored(f"\n❌ Error: {report['error']}", 'red'))
        return

    # Header section
    print(colored("\n" + "="*60, 'cyan'))
    print(colored("🔍 SECURITY HEADER CHECK", 'cyan', attrs=['bold']))
    print(colored(f"Target   : {report['url']}", 'white'))
    print(colored(f"Time     : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 'white'))
    print(colored("="*60 + "\n", 'cyan'))

    # Basic response info
    status_color = 'green' if report['status_code'] == 200 else 'yellow'
    print(colored(f"Status Code : ", 'white') + colored(report['status_code'], status_color))
    print(colored(f"Final URL   : {report['url']}", 'white'))

    # Technology fingerprint
    if report["tech_fingerprint"]:
        print(colored("\n--- 🖥️  Technology Fingerprint ---", 'magenta'))
        for item in report["tech_fingerprint"]:
            for k, v in item.items():
                print(colored(f"  {k}: {v}", 'yellow') + colored("  ← revealed!", 'red'))

    # Security headers analysis
    print(colored("\n--- 🛡️  Security Header Analysis ---\n", 'magenta'))
    for item in report["security_report"]:
        if item["present"]:
            print(colored(f"  ✅ {item['header']}", 'green'))
            # Print value in a slightly dimmer color
            print(colored(f"     Value: {item['value']}", 'white'))
        else:
            print(colored(f"  ❌ {item['header']} — MISSING", 'red'))
            risk_color = 'red' if item['risk'] == 'HIGH' else 'yellow' if item['risk'] == 'MEDIUM' else 'white'
            print(colored(f"     Risk : {item['risk']}", risk_color))
            print(colored(f"     Why  : {item['why']}", 'white'))
        print()

    # Summary
    summary = report["summary"]
    print(colored("--- 📊 Summary ---", 'magenta'))
    print(colored(f"  Headers Present : {summary['present']}/{summary['total_checked']}", 'green'))
    print(colored(f"  Headers Missing : {summary['missing']}/{summary['total_checked']}", 'red'))
    if summary["high_risk_missing"]:
        print(colored(f"\n  🚨 High Risk Missing: {', '.join(summary['high_risk_missing'])}", 'red', attrs=['bold']))
        print(colored(f"  → These are worth reporting in bug bounty programs", 'yellow'))
    print(colored("\n" + "="*60 + "\n", 'cyan'))

# ------------------------------------------------------------
# 5. Optional: Save to file (uncomment if needed)
# ------------------------------------------------------------
def save_report_to_file(report, filename="security_report.txt"):
    """Save the report in plain text format."""
    with open(filename, "w") as f:
        f.write(f"Security Header Check\n")
        f.write(f"Target   : {report['url']}\n")
        f.write(f"Time     : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("="*60 + "\n\n")
        if report["error"]:
            f.write(f"Error: {report['error']}\n")
            return
        f.write(f"Status Code : {report['status_code']}\n")
        f.write(f"Final URL   : {report['url']}\n")
        if report["tech_fingerprint"]:
            f.write("\n--- Technology Fingerprint ---\n")
            for item in report["tech_fingerprint"]:
                for k, v in item.items():
                    f.write(f"  {k}: {v}\n")
        f.write("\n--- Security Header Analysis ---\n\n")
        for item in report["security_report"]:
            if item["present"]:
                f.write(f"  ✅ {item['header']}\n")
                f.write(f"     Value: {item['value']}\n")
            else:
                f.write(f"  ❌ {item['header']} — MISSING\n")
                f.write(f"     Risk : {item['risk']}\n")
                f.write(f"     Why  : {item['why']}\n")
            f.write("\n")
        summary = report["summary"]
        f.write("--- Summary ---\n")
        f.write(f"  Headers Present : {summary['present']}/{summary['total_checked']}\n")
        f.write(f"  Headers Missing : {summary['missing']}/{summary['total_checked']}\n")
        if summary["high_risk_missing"]:
            f.write(f"\n  High Risk Missing: {', '.join(summary['high_risk_missing'])}\n")
        f.write("\n" + "="*60 + "\n")
    print(colored(f"✅ Report also saved to {filename}", 'green'))

# ------------------------------------------------------------
# 6. Main Execution
# ------------------------------------------------------------
def main():
    # Show big title
    print_big_title("HEADER ANALYZER")

    # Get URL
    url = get_target_url()
    print(colored(f"\n🔎 Analyzing {url} ...\n", 'cyan'))

    # Run security check
    report = check_security_headers(url)

    # Print styled report
    print_styled_report(report)

    # Optional: save to file (you can ask the user or always save)
    # save_report_to_file(report)

if __name__ == "__main__":
    main()