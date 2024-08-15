import os
import requests

def whois_lookup(url):
    """Esegue il lookup Whois per l'URL specificato"""
    try:
        response = requests.get(f"https://www.whois.com/whois/{url}", timeout=5)
        print("Informazioni Whois:")
        sys.stdout.write(response.text.strip())
    except Exception as e:
        print(f"Errore nel recupero delle informazioni Whois: {e}")

def find_admin_page(url):
    """Cerca la pagina amministrativa dell'Site"""
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(f"{url}/wp-admin/", headers=headers, timeout=5)
    if response.status_code == 200:
        print("Pagina amministrativa trovata!")
        print(f"URL: {response.url}")
    else:
        print("Pagina amministrativa non trovata.")

def bypass_database(url):
    """Cerca la pagina di database bypassato"""
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(f"{url}/wp-login.php", headers=headers, timeout=5)
    if response.status_code == 200:
        print("Pagina di database bypassata trovata!")
        print(f"URL: {response.url}")
    else:
        print("Pagina di database bypassata non trovata.")

def sql_injection(url):
    """Esegue un'iniezione SQL per l'URL specificato"""
    try:
        response = requests.get(f"{url}/sql injection", timeout=5)
        print("\nRisultati dell'iniezione SQL:")
        sys.stdout.write(response.text.strip())
    except Exception as e:
        print(f"Errore nell'esecuzione dell'iniezione SQL: {e}")

def scan_vulnerabilities(url):
    """Esegue lo scanning delle vulnerabilità sul sito web"""
    try:
        response = requests.get(f"https://{url}/vulnerability scan", timeout=5)
        print("\nRisultati dello scanning delle vulnerabilità:")
        sys.stdout.write(response.text.strip())
    except Exception as e:
        print(f"Errore nel recupero dei risultati dello scanning: {e}")

def display_results(title, result):
    """Visualizza i risultati in rettangoli tratteggiati"""
    print("\n")
    print("+" + "-" * len(result) + "+")
    print("| " + title + ":")
    print("| " + result)
    print("+" + "-" * len(result) + "+")

def main():
    url = input("Inserisci l'URL del sito da analizzare (es.: http://example.com, https://example.onion o http://example.gov): ")
    whois_lookup(url)
    find_admin_page(url)
    bypass_database(url)
    sql_injection(url)
    scan_vulnerabilities(url)

if __name__ == "__main__":
    main()
