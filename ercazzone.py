import os
import subprocess
import requests
import socket
from bs4 import BeautifulSoup
import re

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

def nmap_scan(ip):
    """Esegui diverse scansioni nmap sull'IP del dominio."""
    scansioni = {
        "nmap_servizi": ["nmap", "-sV", ip],
        "nmap_os_detection": ["nmap", "-O", ip],
        "nmap_vuln_scan": ["nmap", "--script", "vuln", ip],
        "nmap_debug1": ["nmap", "-d1", ip],
        "nmap_debug2": ["nmap", "-d2", ip],
        "nmap_full_scan": ["nmap", "-A", ip],
        "nmap_syn_scan": ["nmap", "-sS", ip],
    }
    
    for nome_scansione, comando in scansioni.items():
        print(f"\nEsecuzione {nome_scansione} su {ip}...")
        stdout, stderr = run_command(comando)
        if stdout:
            print(f"Risultati {nome_scansione}:\n", stdout)
            salva_su_desktop(f"{nome_scansione}_{ip}.txt", stdout)
        if stderr:
            print(f"Errori durante {nome_scansione}:\n", stderr)

def esegui_openssl(dominio):
    """Controlla i certificati SSL del dominio."""
    comando = ["openssl", "s_client", "-connect", f"{dominio}:443"]
    print(f"\nControllo certificati SSL per {dominio}...")
    stdout, stderr = run_command(comando)
    if stdout:
        print(f"Certificati SSL trovati:\n", stdout)
        salva_su_desktop(f"openssl_{dominio}.txt", stdout)
    if stderr:
        print(f"Errori durante il controllo dei certificati SSL:\n", stderr)

def esegui_whatweb(dominio):
    """Esegui whatweb per identificare le tecnologie del sito web."""
    comando = ["whatweb", dominio]
    print(f"\nEsecuzione whatweb su {dominio}...")
    stdout, stderr = run_command(comando)
    if stdout:
        print(f"Risultati whatweb:\n", stdout)
        salva_su_desktop(f"whatweb_{dominio}.txt", stdout)
    if stderr:
        print(f"Errori durante whatweb:\n", stderr)

def esegui_subfinder(dominio):
    """Esegui subfinder per trovare i sottodomini del sito."""
    comando = ["subfinder", "-d", dominio]
    print(f"\nEsecuzione subfinder su {dominio}...")
    stdout, stderr = run_command(comando)
    if stdout:
        print(f"Sottodomini trovati:\n", stdout)
        salva_su_desktop(f"subfinder_{dominio}.txt", stdout)
    if stderr:
        print(f"Errori durante subfinder:\n", stderr)

def esegui_uniscan(dominio):
    """Esegui uniscan per cercare directory e vulnerabilità comuni."""
    comando = ["uniscan", "-u", dominio, "-qweds"]
    print(f"\nEsecuzione uniscan su {dominio}...")
    stdout, stderr = run_command(comando)
    if stdout:
        print(f"Risultati uniscan:\n", stdout)
        salva_su_desktop(f"uniscan_{dominio}.txt", stdout)
    if stderr:
        print(f"Errori durante uniscan:\n", stderr)

def esegui_dorks(dominio, dorks_file):
    """Esegui le Google Dorks per trovare pagine sensibili sul sito."""
    with open(dorks_file, 'r') as file:
        dorks = [line.strip() for line in file.readlines()]
    
    print(f"\nEsecuzione delle Google Dorks su {dominio}...\n")
    for dork in dorks:
        url_dork = f"https://www.google.com/search?q={dork}+site:{dominio}"
        try:
            response = requests.get(url_dork)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                links = [a['href'] for a in soup.find_all('a', href=True)]
                for link in links:
                    print(f"Dork: {dork}\nLink: {link}")
                    salva_su_desktop(f"google_dorks_{dominio}.txt", f"Dork: {dork}\nLink: {link}")
            else:
                print(f"Errore nella ricerca con Dork {dork}. Status code: {response.status_code}")
        except Exception as e:
            print(f"Errore durante la ricerca con Dork {dork}: {e}")

def mostra_pagine_login(dominio):
    """Mostra le pagine di login e admin tramite Dorks."""
    dorks_login = [
        'inurl:admin',
        'inurl:login',
        'inurl:wp-login',
        'intitle:login',
        'intitle:admin',
        'inurl:signin',
        'inurl:auth',
        'inurl:dashboard',
        'inurl:cpanel'
    ]
    
    print(f"\nRicerca delle pagine di login e admin per {dominio}...\n")
    for dork in dorks_login:
        url_dork = f"https://www.google.com/search?q={dork}+site:{dominio}"
        try:
            response = requests.get(url_dork)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                links = [a['href'] for a in soup.find_all('a', href=True)]
                for link in links:
                    print(f"Pagine admin/login trovate:\nDork: {dork}\nLink: {link}")
                    salva_su_desktop(f"pagine_login_{dominio}.txt", f"Dork: {dork}\nLink: {link}")
            else:
                print(f"Errore nella ricerca delle pagine login/admin con Dork {dork}. Status code: {response.status_code}")
        except Exception as e:
            print(f"Errore durante la ricerca delle pagine login/admin con Dork {dork}: {e}")

def verifica_honeypot(dominio):
    """Verifica se il sito è un honeypot."""
    honeypot_keywords = ["honeypot", "trap", "bait", "honeypots"]
    try:
        response = requests.get(f"http://{dominio}")
        if response.status_code == 200:
            content = response.text.lower()
            for keyword in honeypot_keywords:
                if keyword in content:
                    print(f"Il sito {dominio} sembra essere un honeypot. Messaggio: sucate merde.")
                    return True
    except Exception as e:
        print(f"Errore durante la verifica dell'honeypot per {dominio}: {e}")
    return False

def esegui_ftpunch(ip):
    """Esegui FTPunch per attaccare il server FTP."""
    comando = ["python3", "FTPunch.py", ip]  # Assicurati che FTPunch.py sia nel tuo percorso
    print(f"\nEsecuzione FTPunch su {ip}...")
    stdout, stderr = run_command(comando)
    if stdout:
        print(f"Risultati FTPunch:\n", stdout)
        salva_su_desktop(f"ftpunch_{ip}.txt", stdout)
    if stderr:
        print(f"Errori durante FTPunch:\n", stderr)

def esegui_androbugs(dominio):
    """Esegui AndroBugs per analizzare le vulnerabilità delle app Android."""
    comando = ["python3", "AndroBugs_Framework.py", dominio]  # Assicurati che AndroBugs_Framework.py sia nel tuo percorso
    print(f"\nEsecuzione AndroBugs su {dominio}...")
    stdout, stderr = run_command(comando)
    if stdout:
        print(f"Risultati AndroBugs:\n", stdout)
        salva_su_desktop(f"androbugs_{dominio}.txt", stdout)
    if stderr:
        print(f"Errori durante AndroBugs:\n", stderr)

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
        if verifica_honeypot(dominio):
            print("Operazione annullata poiché il sito è un honeypot.")
            return
        
        # Esecuzione delle scansioni Nmap
        nmap_scan(ip)
        
        # Visualizza i certificati SSL del dominio
        esegui_openssl(dominio)

        # Esecuzione di WhatWeb per raccogliere informazioni sul server
        esegui_whatweb(dominio)
        
        # Esecuzione di subfinder per individuare sottodomini
        esegui_subfinder(dominio)
        
        # Scansione con Uniscan
        esegui_uniscan(dominio)
        
        # Esecuzione delle Google Dorks per trovare pagine sensibili
        esegui_dorks(dominio, dorks_file)
        
        # Mostra pagine admin e login
        mostra_pagine_login(dominio)

        # Esecuzione di FTPunch
        esegui_ftpunch(ip)

        # Esecuzione di AndroBugs
        esegui_androbugs(dominio)

    else:
        print("Impossibile proseguire senza l'IP del dominio.")

if __name__ == "__main__":
    main()
