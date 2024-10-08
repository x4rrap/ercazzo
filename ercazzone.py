import os
import subprocess
import requests
import re
import time
from bs4 import BeautifulSoup
import random
import sys
import sqlite3

# Pulizia schermo (utile durante esecuzioni lunghe)
def pulisci_schermo():
    os.system('cls' if os.name == 'nt' else 'clear')

# Effetto Matrix per estetica del terminale
def display_matrix_effect(duration=5):
    columns = 80  
    rows = 24     
    chars = "ercazoercazzoercazzoerc4azzoercazzo3rc4zzoercazzonesucanegrodimerda1233909"
    
    end_time = time.time() + duration
    while time.time() < end_time:
        grid = [[' ' for _ in range(columns)] for _ in range(rows)]
        for y in range(rows):
            for x in range(columns):
                if random.random() < 0.1:
                    grid[y][x] = random.choice(chars)

        for row in grid:
            print('\033[92m' + ''.join(row) + '\033[0m')  # Stile Matrix verde
        sys.stdout.flush()
        time.sleep(0.1)
        pulisci_schermo()

# Avviare Tor (se necessario per anonimato)
def start_tor():
    print("Tor in avvio...")
    try:
        subprocess.Popen(['tor'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(10)  
        print("Tor avviato correttamente.")
    except Exception as e:
        print(f"Errore durante l'avvio di Tor: {e}")

# Funzione per installare tool di pentesting necessari
def install_tool(tool_name, install_command):
    try:
        subprocess.run([tool_name, '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"{tool_name} è già installato.")
        return True
    except FileNotFoundError:
        print(f"{tool_name} non trovato. Installazione in corso...")
        try:
            subprocess.run(install_command, shell=True, check=True)
            print(f"{tool_name} installato correttamente.")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Errore durante l'installazione di {tool_name}: {e}")
            return False

# Installa strumenti principali per scansioni
def install_required_tools():
    install_tool('hydra', 'sudo apt-get install -y hydra')
    install_tool('git', 'sudo apt-get install -y git')
    install_tool('nmap', 'sudo apt-get install -y nmap')
    install_tool('nikto', 'sudo apt-get install -y nikto')
    install_tool('sqlmap', 'sudo apt-get install -y sqlmap')

    if not os.path.exists('HostHunter'):
        print("Clonazione di HostHunter da GitHub...")
        try:
            subprocess.run('git clone https://github.com/SpiderLabs/HostHunter.git', shell=True, check=True)
            print("HostHunter installato correttamente.")
        except subprocess.CalledProcessError as e:
            print(f"Errore durante la clonazione di HostHunter: {e}")
    else:
        print("HostHunter è già presente.")

# Funzione per effettuare scanning su vulnerabilità comuni
def scan_vulnerabilities(url):
    try:
        print(f"\nInizio scansione delle vulnerabilità per {url}...")

        # Scan XSS con regex di base (comando esterno potrebbe essere aggiunto)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        scripts = soup.find_all('script')

        if scripts:
            print(f"\nPossibili punti di XSS rilevati nel sito: {url}")
            for script in scripts:
                print(script)

        # Scansione SQL Injection con SQLMap (necessita di autorizzazione)
        print("\nEsecuzione SQLMap (SQL Injection Check)...")
        sqlmap_command = f"sqlmap -u {url} --batch"
        subprocess.run(sqlmap_command, shell=True)

        # Open Redirect Check
        check_open_redirect(url)

        print("Scansione completata.")

    except Exception as e:
        print(f"Errore durante la scansione delle vulnerabilità: {e}")

# Funzione per rilevare Honeypot analizzando le risposte e configurazioni sospette
def honeypot_detection(url):
    try:
        print(f"\nInizio rilevamento honeypot per {url}...")
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        
        # Segnali comuni di honeypot
        if "X-HoneyPot" in response.headers:
            print(f"\nHoneypot rilevato: {url}")
        elif response.status_code == 418:  # Codice HTTP I'm a teapot spesso usato per honeypot
            print(f"\nPossibile Honeypot (HTTP 418) rilevato su {url}")
        else:
            print("\nNessun honeypot rilevato.")
    
    except Exception as e:
        print(f"Errore durante il rilevamento di honeypot: {e}")

# Controllo Open Redirect
def check_open_redirect(url):
    try:
        print(f"\nControllo Open Redirect per {url}...")
        redirect_test = f"{url}?next=https://evil.com"
        response = requests.get(redirect_test, allow_redirects=False)
        if response.status_code == 302 and "evil.com" in response.headers.get('Location', ''):
            print(f"Vulnerabilità Open Redirect trovata su {url}")
        else:
            print("Nessun Open Redirect trovato.")
    except Exception as e:
        print(f"Errore durante il controllo Open Redirect: {e}")

# Cheatsheet per comandi utili durante il pentesting
def show_ctf_cheatsheet():
    cheatsheet = """
    Comandi utili per CTF e Pentesting:
    
    1. SQL Injection: sqlmap -u <url> --dbs
    2. XSS: Usa payload comuni di XSS per testare form.
    3. Brute Force Login: hydra -l admin -P passwords.txt <url> http-post-form "/login.php:username=^USER^&password=^PASS^:F=failed"
    4. Scansione Nmap: nmap -sC -sV -oA output <url>
    5. Nikto Scan: nikto -h <url>
    """
    print(cheatsheet)

# Funzione principale per eseguire scansioni e rilevamenti
if __name__ == "__main__":
    pulisci_schermo()
    display_matrix_effect()
    install_required_tools()
    
    # Esegui scansioni su un URL di test
    target_url = "http://example.com"
    scan_vulnerabilities(target_url)
    honeypot_detection(target_url)
    show_ctf_cheatsheet()
