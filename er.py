import os
import requests
from termcolor import colored
from bs4 import BeautifulSoup

# Import required libraries for OWASP ZAP
import subprocess
import zipfile

def ascii_art():
    """Prints the H4ggar ASCII art"""
    print(colored("""
           _,.-Y  |  |  Y-._
      .-~"   ||  |  |  |   "-.
      I" ""=="|" !""! "|"[]""|     _____
      L__  [] |..------|:   _[----I" .-{"-.
     I___|  ..| l______|l_ [__L]_[I_/r(=}=-P
    [L______L_[________]______j~  '-=c_]/=-^
     \_I_j.--.\==I|I==_/.--L_]
       [_((==)[`-----"](==)j
          I--I"~~"""~~"I--I
          |[]|         |[]|
          l__j         l__j
          |!!|         |!!|
          |..|         |..|
          ([])         ([])
          ]--[         ]--[
          [_L]         [_L] -l'era di un nuovo mondo.
         /|..|\       /|..|\
        `=}--{='     `=}--{='
       .-^--r-^-.   .-^--r-^-.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
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
    # Download and install the OWASP ZAP API client
    owasp_zap_api_url = "https://github.com/zaproxy/zap-api-python/releases/download/v3.9.0/zapapi-3.9.0.jar"
    owasp_zap_api_path = os.path.join(os.path.expanduser("~"), "Desktop", "zapapi-3.9.0.jar")
    
    if not os.path.exists(owasp_zap_api_path):
        response = requests.get(owasp_zap_api_url, stream=True)
        with open(owasp_zap_api_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024): 
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)

    # Start OWASP ZAP
    zap_proxy = subprocess.Popen(["java", "-jar", owasp_zap_api_path, "run"])

    # Add the target URL to OWASP ZAP
    os.system(f"echo 'target={url}' | {owasp_zap_api_path} api context")

    # Wait for OWASP ZAP to finish processing
    zap_proxy.wait()

    # Get the results from OWASP ZAP
    html_content = subprocess.check_output([f"{owasp_zap_api_path} api core", "-k", "core:/v3/info/Alerts"]).decode("utf-8")
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
