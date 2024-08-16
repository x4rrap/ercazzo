import os
import subprocess
import requests
import re
import time
import whois
from tqdm import tqdm
from bs4 import BeautifulSoup, Comment
from scapy.all import sr1, IP, ICMP
from socket import gethostbyname, gethostbyaddr
import json

def pulisci_schermo():
    """Pulisce lo schermo del terminale."""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_ascii_art():
    """Mostra il disegno ASCII all'inizio dell'esecuzione"""
    print("""
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⡀⠀⠀⠀⢀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣤⣶⣾⣿⡉⢤⣍⡓⢶⣶⣦⣤⣉⠒⠤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⣿⣿⣿⣿⣿⣷⡀⠙⣿⣷⣌⠻⣿⣿⣿⣶⣌⢳⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣄⠈⢿⣿⡆⠹⣿⣿⣿⣿⣷⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣄⠹⣿⡄⢻⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠿⣿⣿⣷⣽⣷⢸⣿⡿⣿⡿⠿⠿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠀⠐⠾⢭⣭⡼⠟⠃⣤⡆⠘⢟⢺⣦⡀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⡿⠁⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠻⢿⣿⣿⣿⡿⠁⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣯⡀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠋⠹⣆⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠿⠿⠿⣿⣿⣦⡀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⡀⠀⠉⠙⠒⠂⠀⠀⠀⠀⠀⣤⣤⣄⠀⠉⠛⠿⠁⠀⠀⠀⠀⠀
⠀⠀⠀⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣀⠀⠀⠀⠀⠀⠀⠀⢿⣿⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⠿⠿⠿⢶⣿⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠀⠀⠀⠀⠀⠀⠀⠀
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆⠀⠀⠀⠀⠀
⠉⠛⠛⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠛⠛⠛⠀⠀⠀⠀
                
by hagg4r""")

def start_tor():
    """Avvia Tor in background e nasconde l'output."""
    print("Tor in avvio...")
    try:
        subprocess.Popen(['tor'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(10)  # Attende che Tor sia avviato
        print("Tor avviato correttamente.")
    except Exception as e:
        print(f"Errore durante l'avvio di Tor: {e}")

def find_admin_page(url):
    """Trova la pagina admin del sito web"""
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(f"http://{url}/wp-admin/", headers=headers, timeout=5)
        if response.status_code == 200:
            print("\nPagina Admin trovata!")
            print(f"URL: {response.url}")

            # Estrae le email e altre informazioni utili dalla pagina
            soup = BeautifulSoup(response.text, 'html.parser')
            emails = set(re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', response.text))
            print("\nEmail trovate:")
            for email in emails:
                print(email)

            # Scarica la pagina admin in un file HTML
            html_file_path = os.path.join(os.path.expanduser("~"), "Desktop", f"{url.replace('/', '')}_admin.html")
            with open(html_file_path, 'w') as file:
                file.write(response.text)
            print(f"Pagina admin salvata in {html_file_path}")

            # Simula il salvataggio del database in un file di testo
            save_database_to_txt(url)
        else:
            print("Pagina Admin non trovata.")
    except Exception as e:
        print(f"Errore durante la ricerca della pagina admin: {e}")

def save_database_to_txt(url):
    """Simula il salvataggio del database in un file di testo"""
    database_content = "Simulazione dei dati del database estratti."
    try:
        txt_file_path = os.path.join(os.path.expanduser("~"), "Desktop", f"{url.replace('/', '')}_database.txt")
        with open(txt_file_path, 'w') as file:
            file.write(database_content)
        print(f"\nDatabase salvato in {txt_file_path}")

        # Mostra il peso del file
        file_size = os.path.getsize(txt_file_path)
        print(f"Peso del file: {file_size} bytes")
    except Exception as e:
        print(f"Errore durante il salvataggio del database: {e}")

def scan_for_errors(url):
    """Scansiona il sito per errori comuni e debolezze di sicurezza"""
    error_patterns = [
        "404 Not Found", "500 Internal Server Error", "403 Forbidden",
        "SQL syntax", "Error establishing a database connection", "PHP Warning"
    ]
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(f"http://{url}", headers=headers, timeout=10)
        page_content = response.text

        print("\nScansione errori:")
        for pattern in error_patterns:
            if pattern in page_content:
                print(f"Trovato errore: {pattern}")
    except Exception as e:
        print(f"Errore durante la scansione degli errori: {e}")

def bypass_waf_cloudflare(url):
    """Cerca di bypassare WAF e Cloudflare per accedere alla pagina admin"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    try:
        # Tentativi di accesso diretto alla pagina admin
        possible_paths = [
            "/admin", "/admin.php", "/administrator", "/wp-login.php", "/wp-admin"
        ]
        for path in possible_paths:
            full_url = f"http://{url}{path}"
            response = requests.get(full_url, headers=headers, timeout=10)
            if response.status_code == 200:
                print(f"Accesso riuscito alla pagina admin: {full_url}")
                return full_url
        print("Nessun accesso riuscito.")
        return None
    except Exception as e:
        print(f"Errore durante il bypass di WAF/Cloudflare: {e}")
        return None

def whois_scan(url):
    """Esegue una scansione WHOIS per ottenere informazioni sul dominio"""
    try:
        domain_info = whois.whois(url)
        print("\nInformazioni WHOIS:")
        print(json.dumps(domain_info, indent=4))
    except Exception as e:
        print(f"Errore durante la scansione WHOIS: {e}")

def find_servers(url):
    """Trova i server collegati al sito e fornisce informazioni sulla posizione"""
    try:
        ip = gethostbyname(url)
        print(f"\nIndirizzo IP per {url}: {ip}")
        
        # Aggiunge informazioni sui server
        hostname, _, _ = gethostbyaddr(ip)
        print(f"Nome host per {ip}: {hostname}")
        
        # Ping per verificare la raggiungibilità del server
        response = sr1(IP(dst=ip)/ICMP(), timeout=2, verbose=False)
        if response:
            print(f"Il server {ip} è raggiungibile.")
        else:
            print(f"Il server {ip} non è raggiungibile.")
    except Exception as e:
        print(f"Errore durante la ricerca dei server: {e}")

def check_honeypot(url):
    """Verifica se il sito è un honeypot"""
    honeypot_patterns = [
        "honeypot", "capture", "suspicious", "test", "fake", "demo", "security", "bot"
    ]
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(f"http://{url}", headers=headers, timeout=10)
        page_content = response.text

        print("\nVerifica honeypot:")
        for pattern in honeypot_patterns:
            if pattern in page_content.lower():
                print(f"Sito potenzialmente un honeypot: trovato '{pattern}'")
                return
        print("Sito non sembra essere un honeypot.")
    except Exception as e:
        print(f"Errore durante la verifica del honeypot: {e}")

def main():
    pulisci_schermo()
    display_ascii_art()
    start_tor()

    url = input("Inserisci l'URL del sito (senza 'http://'): ")
    
    print("\nRicerca della pagina admin...")
    find_admin_page(url)
    
    print("\nScansione del sito per errori...")
    scan_for_errors(url)
    
    print("\nTentativo di bypass di WAF/Cloudflare...")
    admin_url = bypass_waf_cloudflare(url)
    if admin_url:
        print(f"Pagina admin accessibile a: {admin_url}")
    else:
        print("Non è stato possibile bypassare WAF/Cloudflare.")
    
    print("\nEsecuzione scansione WHOIS...")
    whois_scan(url)
    
    print("\nRicerca dei server collegati...")
    find_servers(url)
    
    print("\nVerifica se il sito è un honeypot...")
    check_honeypot(url)
    
if __name__ == "__main__":
    main()
