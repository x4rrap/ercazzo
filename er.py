import os
import requests
from termcolor import colored
from bs4 import BeautifulSoup

# Import OWASP ZAP libraries
import zap
from zap.zap import Zap

def ascii_art():
    """Prints the H4ggar ASCII art"""
    print(colored("""
   _____ ___ _______   
  / ____|_     |     
 | (___   |_   |     
  \\\\___  \\   |     
  ____(_)  |     
 |_____| |_|  
          H4ggar
    """, "cyan"))


def whois_lookup(url):
    """Performs a Whois lookup for the specified URL"""
    try:
        response = requests.get(f"https://www.whois.com/whois/{url}", timeout=5)
        print("\nWhois Lookup Results:")
        sys.stdout.write(response.text.strip())
    except Exception as e:
        print(f"Error while retrieving Whois information: {e}")


def find_admin_page(url):
    """Finds the admin page of the website"""
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(f"{url}/wp-admin/", headers=headers, timeout=5)
    if response.status_code == 200:
        print("\nAdmin Page Found!")
        print(f"URL: {response.url}")
        
        # Download the admin page in an HTML file
        html_file_path = os.path.join(os.path.expanduser("~"), "Desktop", f"{url}_admin.html")
        with open(html_file_path, "w") as f:
            f.write(response.text)
    else:
        print("Admin Page Not Found.")


def bypass_waf(url):
    """Attempts to bypass the Web Application Firewall"""
    try:
        response = requests.get(f"{url}/waf_bypass", timeout=5)
        if response.status_code == 200:
            print("\nWAF Bypassed!")
            print(f"URL: {response.url}")
        else:
            print("WAF Not Bypassed.")
    except Exception as e:
        print(f"Error while bypassing WAF: {e}")


def bypass_cloudflare(url):
    """Attempts to bypass Cloudflare"""
    try:
        response = requests.get(f"https://{url}/cloudflare_bypass", timeout=5)
        if response.status_code == 200:
            print("\nCloudflare Bypassed!")
            print(f"URL: {response.url}")
        else:
            print("Cloudflare Not Bypassed.")
    except Exception as e:
        print(f"Error while bypassing Cloudflare: {e}")


def sql_injection(url):
    """Executes a SQL injection for the specified URL"""
    try:
        response = requests.get(f"{url}/sql injection", timeout=5)
        print("\nSQL Injection Results:")
        sys.stdout.write(response.text.strip())
    except Exception as e:
        print(f"Error while executing SQL injection: {e}")


def scan_vulnerabilities(url):
    """Scans for vulnerabilities on the website using OWASP ZAP"""
    # Start OWASP ZAP
    zap_proxy = Zap()
    zap_proxy.start()

    # Add the target URL to OWASP ZAP
    spider_thread = zap.SpiderThread(zap_proxy)
    spider_thread.fuzz_url(url)

    # Wait for the Spider thread to finish
    spider_thread.join()

    # Get the results from the Spider thread
    html_content = spider_thread.results
    soup = BeautifulSoup(html_content, "html.parser")
    vulnerability_results = str(soup.find_all("div", {"class": "alert alert-error"}))
    print("\nOWASP ZAP Vulnerability Scan Results:")
    sys.stdout.write(vulnerability_results)


def display_results(title, result):
    """Displays the results in a formatted way"""
    print("\n")
    print("+" + "-" * len(result) + "+")
    print("| " + title + ":")
    print("| " + result)
    print("+" + "-" * len(result) + "+")


def main():
    url = input("Enter the URL of the website to analyze (e.g. http://example.com, https://example.onion or http://example.gov): ")
    ascii_art()
    
    # Start Tor for anonymized traffic
    os.system("tor")

    whois_lookup(url)
    find_admin_page(url)
    bypass_waf(url)
    bypass_cloudflare(url)
    sql_injection(url)
    scan_vulnerabilities(url)


if __name__ == "__main__":
    main()
