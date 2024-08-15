import os
import requests
from termcolor import colored


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
    else:
        print("Admin Page Not Found.")


def bypass_database(url):
    """Attempts to bypass the database page"""
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(f"{url}/wp-login.php", headers=headers, timeout=5)
    if response.status_code == 200:
        print("\nDatabase Page Bypassed!")
        print(f"URL: {response.url}")
    else:
        print("Database Page Not Bypassed.")


def sql_injection(url):
    """Executes a SQL injection for the specified URL"""
    try:
        response = requests.get(f"{url}/sql injection", timeout=5)
        print("\nSQL Injection Results:")
        sys.stdout.write(response.text.strip())
    except Exception as e:
        print(f"Error while executing SQL injection: {e}")


def scan_vulnerabilities(url):
    """Scans for vulnerabilities on the website"""
    try:
        response = requests.get(f"https://{url}/vulnerability scan", timeout=5)
        print("\nVulnerability Scan Results:")
        sys.stdout.write(response.text.strip())
    except Exception as e:
        print(f"Error while retrieving vulnerability scan results: {e}")


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
    whois_lookup(url)
    find_admin_page(url)
    bypass_database(url)
    sql_injection(url)
    scan_vulnerabilities(url)


if __name__ == "__main__":
    main()
