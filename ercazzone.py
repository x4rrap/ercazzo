import os
import subprocess
import requests
import socket
from bs4 import BeautifulSoup

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
        "nmap_debug_1": ["nmap", "-d1", ip],
        "nmap_debug_2": ["nmap", "-d2", ip],
        "nmap_full": ["nmap", "-A", ip],  # Scansione completa
        "nmap_tcp_scan": ["nmap", "-sS", ip]  # TCP SYN scan
    }
    
    for nome_scansione, comando in scansioni.items():
        print(f"\nEsecuzione {nome_scansione} su {ip}...")
        stdout, stderr = run_command(comando)
        success_percentage = calculate_success_percentage(stdout, stderr)
        if stdout:
            print(f"Risultati {nome_scansione}:\n", stdout)
            salva_su_desktop(f"{nome_scansione}_{ip}.txt", stdout)
        if stderr:
            print(f"Errori durante {nome_scansione}:\n", stderr)
        print(f"Percentuale di successo {nome_scansione}: {success_percentage:.2f}%")

def calculate_success_percentage(stdout, stderr):
    """Calcola la percentuale di successo basata sull'output."""
    total_lines = len(stdout.splitlines()) + len(stderr.splitlines())
    successful_lines = len(stdout.splitlines())
    return (successful_lines / total_lines * 100) if total_lines > 0 else 0

def esegui_openssl(dominio):
    """Visualizza i certificati SSL del dominio usando OpenSSL."""
    print(f"\nControllo dei certificati SSL per {dominio}...")
    comando = ["openssl", "s_client", "-connect", f"{dominio}:443"]
    stdout, stderr = run_command(comando)
    success_percentage = calculate_success_percentage(stdout, stderr)
    if stdout:
        print(f"Certificati SSL:\n", stdout)
        salva_su_desktop(f"certificati_ssl_{dominio}.txt", stdout)
    if stderr:
        print(f"Errori durante il controllo SSL:\n", stderr)
    print(f"Percentuale di successo controllo SSL: {success_percentage:.2f}%")

def esegui_whatweb(dominio):
    """Esegui whatweb per identificare le tecnologie del sito web."""
    comando = ["whatweb", dominio]
    print(f"\nEsecuzione whatweb su {dominio}...")
    stdout, stderr = run_command(comando)
    success_percentage = calculate_success_percentage(stdout, stderr)
    if stdout:
        print(f"Risultati whatweb:\n", stdout)
        salva_su_desktop(f"whatweb_{dominio}.txt", stdout)
    if stderr:
        print(f"Errori durante whatweb:\n", stderr)
    print(f"Percentuale di successo whatweb: {success_percentage:.2f}%")

def esegui_subfinder(dominio):
    """Esegui subfinder per trovare i sottodomini del sito."""
    comando = ["subfinder", "-d", dominio]
    print(f"\nEsecuzione subfinder su {dominio}...")
    stdout, stderr = run_command(comando)
    success_percentage = calculate_success_percentage(stdout, stderr)
    if stdout:
        print(f"Sottodomini trovati:\n", stdout)
        salva_su_desktop(f"subfinder_{dominio}.txt", stdout)
    if stderr:
        print(f"Errori durante subfinder:\n", stderr)
    print(f"Percentuale di successo subfinder: {success_percentage:.2f}%")

def esegui_uniscan(dominio):
    """Esegui uniscan per cercare directory e vulnerabilità comuni."""
    comando = ["uniscan", "-u", dominio, "-qweds"]
    print(f"\nEsecuzione uniscan su {dominio}...")
    stdout, stderr = run_command(comando)
    success_percentage = calculate_success_percentage(stdout, stderr)
    if stdout:
        print(f"Risultati uniscan:\n", stdout)
        salva_su_desktop(f"uniscan_{dominio}.txt", stdout)
    if stderr:
        print(f"Errori durante uniscan:\n", stderr)
    print(f"Percentuale di successo uniscan: {success_percentage:.2f}%")

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
                print(f"Percentuale di successo dork {dork}: 100.00%")
            else:
                print(f"Errore nella ricerca con Dork {dork}. Status code: {response.status_code}")
                print(f"Percentuale di successo dork {dork}: 0.00%")
        except Exception as e:
            print(f"Errore durante la ricerca con Dork {dork}: {e}")
            print(f"Percentuale di successo dork {dork}: 0.00%")

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
                print(f"Percentuale di successo dork {dork}: 100.00%")
            else:
                print(f"Errore nella ricerca delle pagine login/admin con Dork {dork}. Status code: {response.status_code}")
                print(f"Percentuale di successo dork {dork}: 0.00%")
        except Exception as e:
            print(f"Errore durante la ricerca delle pagine login/admin con Dork {dork}: {e}")
                        print(f"Errore durante la ricerca delle pagine login/admin con Dork {dork}: {e}")
            print(f"Percentuale di successo dork {dork}: 0.00%")

def esegui_ftpunch(ip):
    """Esegui FTPunch per attaccare il server FTP."""
    comando = ["python3", "FTPunch.py", ip]  # Assicurati che FTPunch.py sia nel tuo percorso
    print(f"\nEsecuzione FTPunch su {ip}...")
    stdout, stderr = run_command(comando)
    success_percentage = calculate_success_percentage(stdout, stderr)
    if stdout:
        print(f"Risultati FTPunch:\n", stdout)
        salva_su_desktop(f"ftpunch_{ip}.txt", stdout)
    if stderr:
        print(f"Errori durante FTPunch:\n", stderr)
    print(f"Percentuale di successo FTPunch: {success_percentage:.2f}%")

def esegui_androbugs(dominio):
    """Esegui AndroBugs per analizzare le vulnerabilità delle app Android."""
    comando = ["python3", "AndroBugs_Framework.py", dominio]  # Assicurati che AndroBugs_Framework.py sia nel tuo percorso
    print(f"\nEsecuzione AndroBugs su {dominio}...")
    stdout, stderr = run_command(comando)
    success_percentage = calculate_success_percentage(stdout, stderr)
    if stdout:
        print(f"Risultati AndroBugs:\n", stdout)
        salva_su_desktop(f"androbugs_{dominio}.txt", stdout)
    if stderr:
        print(f"Errori durante AndroBugs:\n", stderr)
    print(f"Percentuale di successo AndroBugs: {success_percentage:.2f}%")

def main():
    """Funzione principale per eseguire le scansioni."""
    dominio = input("Inserisci il dominio del sito web (es: example.com): ")
    dorks_file = '/mnt/data/google-dorks.txt'  # Caricamento del file di dorks caricato
    
    ip = risolvi_ip(dominio)
    
    if ip:
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

