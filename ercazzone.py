import os
import subprocess
import requests
import socket
from bs4 import BeautifulSoup
from datetime import datetime

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
    """Esegui una scansione nmap di base su un IP."""
    print(f"\nEseguendo nmap su {ip}...")
    comando = ["nmap", "-d1", ip]
    stdout, stderr = run_command(comando)
    if stdout:
        print("Risultati nmap:\n", stdout)
        salva_su_desktop(f"nmap_scan_{ip}.txt", stdout)
    if stderr:
        print("Errori durante la scansione nmap:\n", stderr)

def ottieni_info_database(dominio):
    """Tenta di identificare il database e la tecnologia su cui si basa il sito."""
    try:
        url = f"http://{dominio}"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            server = response.headers.get('Server', 'Sconosciuto')
            powered_by = response.headers.get('X-Powered-By', 'Non specificato')
            print(f"Server: {server}")
            print(f"X-Powered-By: {powered_by}")
            salva_su_desktop(f"info_server_{dominio}.txt", f"Server: {server}\nX-Powered-By: {powered_by}")
            
            # Aggiunta di controllo per individuare il database tramite tecniche di fingerprinting HTTP
            if 'php' in powered_by.lower():
                print("Potrebbe essere usato MySQL o MariaDB.")
                salva_su_desktop(f"info_server_{dominio}.txt", "Database: MySQL/MariaDB (presunto)")
            elif 'asp' in powered_by.lower():
                print("Potrebbe essere usato Microsoft SQL Server.")
                salva_su_desktop(f"info_server_{dominio}.txt", "Database: Microsoft SQL Server (presunto)")
            elif 'java' in powered_by.lower() or 'spring' in powered_by.lower():
                print("Potrebbe essere usato PostgreSQL o Oracle.")
                salva_su_desktop(f"info_server_{dominio}.txt", "Database: PostgreSQL/Oracle (presunto)")
        else:
            print(f"Il sito {dominio} ha restituito uno status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"Errore durante l'accesso al sito {dominio}: {e}")

def esegui_nmap_servizi(ip):
    """Esegui una scansione nmap più dettagliata per determinare i servizi attivi."""
    print(f"\nEseguendo nmap per determinare i servizi attivi su {ip}...")
    comando = ["nmap", "-sV", ip]
    stdout, stderr = run_command(comando)
    if stdout:
        print("Risultati dei servizi nmap:\n", stdout)
        salva_su_desktop(f"nmap_servizi_{ip}.txt", stdout)
    if stderr:
        print("Errori durante la scansione dei servizi nmap:\n", stderr)

def esegui_banner_grabbing(ip):
    """Esegui il banner grabbing per identificare i servizi e le versioni software."""
    print(f"\nEseguendo il banner grabbing su {ip}...")
    comando = ["nmap", "--script", "banner", ip]
    stdout, stderr = run_command(comando)
    if stdout:
        print("Risultati del banner grabbing:\n", stdout)
        salva_su_desktop(f"banner_grabbing_{ip}.txt", stdout)
    if stderr:
        print("Errori durante il banner grabbing:\n", stderr)

def esegui_whois(dominio):
    """Esegui una ricerca WHOIS sul dominio."""
    print(f"\nEseguendo ricerca WHOIS per {dominio}...")
    comando = ["whois", dominio]
    stdout, stderr = run_command(comando)
    if stdout:
        print("Risultati WHOIS:\n", stdout)
        salva_su_desktop(f"whois_{dominio}.txt", stdout)
    if stderr:
        print("Errori durante la ricerca WHOIS:\n", stderr)

def main():
    """Funzione principale per eseguire le scansioni."""
    dominio = input("Inserisci il dominio del sito web (es: example.com): ")
    ip = risolvi_ip(dominio)
    
    if ip:
        # Esegui Nmap scansioni
        nmap_scan(ip)
        esegui_nmap_servizi(ip)
        esegui_banner_grabbing(ip)
        
        # Identifica informazioni del server e del database
        ottieni_info_database(dominio)
        
        # Esegui WHOIS
        esegui_whois(dominio)
    else:
        print("Impossibile proseguire senza l'IP del dominio.")

if __name__ == "__main__":
    main()
