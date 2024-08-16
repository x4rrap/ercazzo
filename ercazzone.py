import os
import subprocess
import requests
import time
from tqdm import tqdm  # Per mostrare la barra di progresso
from bs4 import BeautifulSoup, Comment

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
⠀⠀⠀⠀⠀⠀⠀⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⠹⣿⡄⢻⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠿⣿⣿⣷⣽⣷⢸⣿⡿⣿⡿⠿⠿⣆⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠀⠐⠾⢭⣭⡼⠟⠃⣤⡆⠘⢟⢺⣦⡀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⡿⠁⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⡿⢛⣥⣶⠾⠿⠛⠳⠶⢬⡁⠀⠀⠘⣃⠤⠤⠤⢍⠻⡄⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⡿⣫⣾⡿⢋⣥⣶⣿⠿⢿⣿⣿⣿⠩⠭⢽⣷⡾⢿⣿⣦⢱⡹⡀⠀⠀
⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⡟⠈⠛⠏⠰⢿⣿⣿⣧⣤⣼⣿⣿⣿⡏⠩⠽⣿⣀⣼⣿⣿⢻⣷⢡⠀⠀
⠀⠀⠀⠀⠀⢰⣿⣿⣿⣿⣿⣿⢁⣿⣷⣦⡀⠀⠉⠙⠛⠛⠛⠋⠁⠙⢻⡆⠀⢌⣉⠉⠉⠀⠸⣿⣇⠆⠀
⠀⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⡇⢸⣿⣿⣿⣿⠷⣄⢠⣶⣾⣿⣿⣿⣿⣿⠁⠀⠀⢿⣿⣿⣷⠈⣿⠸⡀⠀
⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⠀⣌⡛⠿⣿⣿⠀⠈⢧⢿⣿⡿⠟⠋⠉⣠⣤⣤⣤⣄⠙⢿⣿⠏⣰⣿⡇⢇⠀
⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⠁⣾⣟⣛⠛⠛⠿⠿⠶⠬⠔⠀⣠⡶⠋⠿⠈⠷⠸⠇⠻⠏⣀⢿⣿⣿⡄⢇
⠀⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⣴⠀⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠏⠉⠰⠆⠠⣠⣿⣿⣿⣿⠿⠋⠁
⢀⣿⣿⠿⠋⣡⣤⣶⣾⣿⣿⣿⡟⠁⠀⣠⣤⣴⣶⣶⣾⣿⣿⣷⡈⢿⣿⣿⣿⣿⠿⠛⠡⣴⣿⣿⣿⣿⠟⠁
⣼⠋⢁⣴⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣎⠻⠟⠋⣠⣴⣿⣿⣿⣿⠿⠋⠁⠀⠀
⢿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⣴⠀⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣠⣾⣿⠿⠿⠟⠋⠁⠀⠀⠀⠀⠀
⠀⠉⠛⠛⠿⠿⠿⢿⣿⣿⣿⣵⣾⣿⣧⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠉⠉⠉⠉⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                
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

            # Scarica la pagina admin in un file HTML
            html_file_path = os.path.join(os.path.expanduser("~"), "Desktop", f"{url.replace('/', '')}_admin.html")
            with open(html_file_path, "w", encoding="utf-8") as file:
                file.write(response.text)

            print(f"La pagina admin è stata scaricata come HTML in: {html_file_path}")
        else:
            print("\nPagina Admin non trovata.")
    except requests.RequestException as e:
        print(f"\nErrore durante la richiesta alla pagina admin: {e}")

def check_robots_txt(url):
    """Controlla se il sito web ha un file robots.txt"""
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(f"http://{url}/robots.txt", headers=headers, timeout=5)
        if response.status_code == 200:
            print("\nrobots.txt trovato!")
            print(response.text)
        else:
            print("\nrobots.txt non trovato.")
    except requests.RequestException as e:
        print(f"\nErrore durante la richiesta a robots.txt: {e}")

def extract_html_comments(url):
    """Estrae i commenti HTML dalla homepage del sito web"""
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(f"http://{url}", headers=headers, timeout=5)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            comments = soup.find_all(string=lambda text: isinstance(text, Comment))
            if comments:
                print("\nCommenti HTML trovati:")
                for comment in comments:
                    print(comment)
            else:
                print("\nNessun commento HTML trovato.")
        else:
            print("\nImpossibile accedere alla homepage del sito.")
    except requests.RequestException as e:
        print(f"\nErrore durante la richiesta alla homepage: {e}")

def run_uniscan_scan(url):
    """Esegue una scansione Uniscan sul sito web"""
    print("\nEsecuzione della scansione Uniscan...")
    uniscan_command = ["uniscan", "-u", f"http://{url}", "-qweds"]
    result = subprocess.run(uniscan_command, capture_output=True, text=True)
    print(result.stdout)

def run_nmap_scan(url):
    """Esegue una scansione Nmap sul sito web"""
    print("\nEsecuzione della scansione Nmap...")
    nmap_command = ["nmap", "-sS", "-sV", url]
    result = subprocess.run(nmap_command, capture_output=True, text=True)
    print(result.stdout)

def run_sqli_detector(url):
    """Esegue SQLiDetector per trovare vulnerabilità di SQL Injection"""
    print("\nEsecuzione di SQLiDetector...")
    sqli_command = ["python3", "SQLiDetector/sqlidetector.py", "-u", f"http://{url}"]
    result = subprocess.run(sqli_command, capture_output=True, text=True)
    print(result.stdout)

def upload_to_github():
    """Carica i risultati su GitHub (Brahmastra repository)"""
    print("\nCaricamento dei risultati su GitHub...")
    try:
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", "'Aggiunta automatica dei risultati'"], check=True)
        subprocess.run(["git", "push"], check=True)
        print("Caricamento completato con successo.")
    except subprocess.CalledProcessError as e:
        print(f"Errore durante il caricamento su GitHub: {e}")

def main():
    pulisci_schermo()
    display_ascii_art()

    start_tor()

    domain = input("Inserisci il dominio del sito web da testare (ad esempio example.com): ").strip()

    url = f"http://{domain}"

    # Barra di avanzamento
    tasks = [
        ("Ricerca pagina Admin", find_admin_page),
        ("Controllo file robots.txt", check_robots_txt),
        ("Estrazione commenti HTML", extract_html_comments),
        ("Scansione Uniscan", run_uniscan_scan),
        ("Scansione Nmap", run_nmap_scan),
        ("SQL Injection Detection", run_sqli_detector)
    ]

    for task_name, task_function in tqdm(tasks, desc="Progress", ncols=100):
        print(f"\nInizio: {task_name}")
        task_function(domain)

    upload_to_github()

if __name__ == "__main__":
    main()
