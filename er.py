import os
import requests
from termcolor import colored
from bs4 import BeautifulSoup

# Import required libraries for OWASP ZAP
import subprocess
import zipfile
import time
import sys

def pulisci_schermo():
    """Pulisce lo schermo del terminale."""
    os.system('cls' if os.name == 'nt' else 'clear')

def disegna_ascii(position, sparando=False):
    """Genera un frame dell'arte ASCII in una data posizione."""
    proiettile = " |-->\n" if sparando else " |\n"
    arte = f"""
{position * " "} _,.-Y  |  |  Y-._
{position * " "}.{"-" * 4}   ||  |  |  |   {"-" * 3}.
{position * " "}I" ""=="|" !""! "|"[]""|     _____
{position * " "}L__  [] |..------|:   _[----I" .-{{"-.
{position * " "}I___|  ..| l______|l_ [__L]_[I_/r(}}=-P{proiettile}
{position * " "}[L______L_[________]______j~  '-=c_]/=-^
{position * " "} \\_I_j.--.\\==I|I==_/.--L_]
{position * " "}   [_((==)[`-----`](==)j
{position * " "}      I--I"~~"""~~"I--I
{position * " "}      |[]|         |[]|
{position * " "}      l__j         l__j
{position * " "}      |!!|         |!!|
{position * " "}      |..|         |..|
{position * " "}      ([])         ([])]
{position * " "}      ]--[         ]--[
{position * " "}      [_L]         [_L] -l'era di un nuovo mondo.
{position * " "}     /|..|\\       /|..|\\
{position * " "}    `=}--{{=`     `=}--{{=`
{position * " "}   .-^--r-^-.   .-^--r-^-.
"""
    return arte

def anima_ascii():
    """Anima l'arte ASCII spostandola attraverso lo schermo."""
    for i in range(20):
        pulisci_schermo()
        sparando = (i % 5 == 0)  # Spara ogni 5 frame
        print(disegna_ascii(i, sparando))
        time.sleep(0.1)

def ascii_art():
    """Anima e stampa l'arte ASCII di H4ggar"""
    anima_ascii()

def whois_lookup(url):
    """Esegue un Whois lookup per l'URL specificato"""
    try:
        response = requests.get(f"https://www.whois.com/whois/{url}", timeout=5)
        print("\nRisultati del Whois Lookup:")
        sys.stdout.write(response.text.strip())
    except Exception as e:
        print(f"Errore durante il recupero delle informazioni Whois: {e}")

def find_admin_page(url):
    """Trova la pagina admin del sito web"""
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(f"{url}/wp-admin/", headers=headers, timeout=5)
    if response.status_code == 200:
        print("\nPagina Admin Trovata!")
        print(f"URL: {response.url}")
        
        # Scarica la pagina admin in un file HTML
        html_file_path = os.path.join(os.path.expanduser("~"), "Desktop", f"{url}_admin.html")
        with open(html_file_path, "w") as f:
            f.write(response.text)
    else:
        print("Pagina Admin Non Trovata.")

def bypass_waf(url):
    """Tenta di bypassare il Web Application Firewall"""
    try:
        response = requests.get(f"{url}/waf_bypass", timeout=5)
        if response.status_code == 200:
            print("\nWAF Bypassato!")
            print(f"URL: {response.url}")
        else:
            print("WAF Non Bypassato.")
    except Exception as e:
        print(f"Errore durante il bypass del WAF: {e}")

def bypass_cloudflare(url):
    """Tenta di bypassare Cloudflare"""
    try:
        response = requests.get(f"https://{url}/cloudflare_bypass", timeout=5)
        if response.status_code == 200:
            print("\nCloudflare Bypassato!")
            print(f"URL: {response.url}")
        else:
            print("Cloudflare Non Bypassato.")
    except Exception as e:
        print(f"Errore durante il bypass di Cloudflare: {e}")

def sql_injection(url):
    """Esegue una SQL injection per l'URL specificato"""
    try:
        response = requests.get(f"{url}/sql injection", timeout=5)
        print("\nRisultati della SQL Injection:")
        sys.stdout.write(response.text.strip())
    except Exception as e:
        print(f"Errore durante l'esecuzione della SQL injection: {e}")

def scan_vulnerabilities(url):
    """Scansiona vulnerabilità sul sito web utilizzando OWASP ZAP"""
    # Scarica e installa il client API di OWASP ZAP
    owasp_zap_api_url = "https://github.com/zaproxy/zap-api-python/releases/download/v3.9.0/zapapi-3.9.0.jar"
    owasp_zap_api_path = os.path.join(os.path.expanduser("~"), "Desktop", "zapapi-3.9.0.jar")
    
    if not os.path.exists(owasp_zap_api_path):
        response = requests.get(owasp_zap_api_url, stream=True)
        with open(owasp_zap_api_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024): 
                if chunk: # filtra i chunk keep-alive
                    f.write(chunk)

    # Avvia OWASP ZAP
    zap_proxy = subprocess.Popen(["java", "-jar", owasp_zap_api_path, "run"])

    # Aggiungi l'URL target a OWASP ZAP
    os.system(f"echo 'target={url}' | {owasp_zap_api_path} api context")

    # Attendi che OWASP ZAP finisca di processare
    zap_proxy.wait()

    # Ottieni i risultati da OWASP ZAP
    html_content = subprocess.check_output([f"{owasp_zap_api_path} api core", "-k", "core:/v3/info/Alerts"]).decode("utf-8")
    soup = BeautifulSoup(html_content, "html.parser")
    vulnerability_results = str(soup.find_all("div", {"class": "alert alert-error"}))
    print("\nRisultati della Scansione di Vulnerabilità di OWASP ZAP:")
    sys.stdout.write(vulnerability_results)

def display_results(title, result):
    """Mostra i risultati in modo formattato"""
    print("\n")
    print("+" + "-" * len(result) + "+")
    print("| " + title + ":")
    print("| " + result)
    print("+" + "-" * len(result) + "+")

def main():
    url = input("Inserisci l'URL del sito web da analizzare (es. http://example.com, https://example.onion o http://example.gov): ")
    ascii_art()
    
    # Avvia Tor per il traffico anonimo
    os.system("tor")

    whois_lookup(url)
    find_admin_page(url)
    bypass_waf(url)
    bypass_cloudflare(url)
    sql_injection(url)
    scan_vulnerabilities(url)

if __name__ == "__main__":
    main()
