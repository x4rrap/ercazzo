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

def nmap_full_scan(ip):
    """Esegui una mappatura completa con Nmap e rileva vulnerabilità."""
    print(f"\nEsecuzione di una scansione completa Nmap su {ip}...")
    commands = [
        ["nmap", "-A", "-T4", ip],  # Scansione aggressiva con rilevazione OS
        ["nmap", "-p-", "--open", ip],  # Scansione completa delle porte aperte
        ["nmap", "--script", "vuln", ip],  # Scansione delle vulnerabilità
        ["nmap", "--script", "http-enum", ip]  # Enumera directory e risorse HTTP
    ]
    
    for i, command in enumerate(commands):
        stdout, stderr = run_command(command)
        if stdout:
            print(f"Risultati della scansione Nmap {i + 1}:\n", stdout)
            salva_su_desktop(f"nmap_scan_{i+1}_{ip}.txt", stdout)
        if stderr:
            print(f"Errori durante la scansione Nmap {i + 1}:\n", stderr)

def esegui_ssl(dominio):
    """Esegui SSLyze per controllare i certificati SSL."""
    comando = ["sslyze", f"--regular {dominio}:443"]
    print(f"\nControllo certificati SSL per {dominio}...")
    stdout, stderr = run_command(comando)
    if stdout:
        print(f"Risultati SSLyze:\n", stdout)
        salva_su_desktop(f"sslyze_{dominio}.txt", stdout)
    if stderr:
        print(f"Errori durante SSLyze:\n", stderr)

def esegui_gobuster(dominio):
    """Esegui GoBuster per individuare directory nascoste."""
    comando = ["gobuster", "dir", "-u", f"http://{dominio}", "-w", "/usr/share/wordlists/dirb/common.txt"]
    print(f"\nEsecuzione di GoBuster su {dominio}...")
    stdout, stderr = run_command(comando)
    if stdout:
        print(f"Risultati GoBuster:\n", stdout)
        salva_su_desktop(f"gobuster_{dominio}.txt", stdout)
    if stderr:
        print(f"Errori durante GoBuster:\n", stderr)

def esegui_sqlmap(dominio):
    """Esegui SQLMap per rilevare vulnerabilità SQL injection."""
    comando = ["sqlmap", "-u", f"http://{dominio}", "--batch", "--crawl=5", "--random-agent"]
    print(f"\nEsecuzione di SQLMap su {dominio}...")
    stdout, stderr = run_command(comando)
    if stdout:
        print(f"Risultati SQLMap:\n", stdout)
        salva_su_desktop(f"sqlmap_{dominio}.txt", stdout)
    if stderr:
        print(f"Errori durante SQLMap:\n", stderr)

def esegui_searchsploit(dominio):
    """Esegui Searchsploit per trovare exploit noti per il dominio."""
    comando = ["searchsploit", dominio]
    print(f"\nEsecuzione di Searchsploit per {dominio}...")
    stdout, stderr = run_command(comando)
    if stdout:
        print(f"Risultati Searchsploit:\n", stdout)
        salva_su_desktop(f"searchsploit_{dominio}.txt", stdout)
    if stderr:
        print(f"Errori durante Searchsploit:\n", stderr)

def main():
    """Funzione principale per eseguire le scansioni."""
    dominio = input("Inserisci il dominio del sito web (es: example.com): ")
    
    # Validazione del dominio
    if not re.match(r'^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', dominio):
        print("Dominio non valido.")
        return

    ip = risolvi_ip(dominio)
    
    if ip:
        # Esegui la scansione completa Nmap
        nmap_full_scan(ip)
        
        # Esegui controllo SSL con SSLyze
        esegui_ssl(dominio)

        # Esegui directory enumeration con GoBuster
        esegui_gobuster(dominio)

        # Esegui SQLMap per rilevare vulnerabilità SQL injection
        esegui_sqlmap(dominio)

        # Esegui Searchsploit per cercare exploit noti
        esegui_searchsploit(dominio)

    else:
        print("Impossibile proseguire senza l'IP del dominio.")

if __name__ == "__main__":
    main()
