import os
import subprocess
import socket
import requests
from datetime import datetime

def run_command(command):
    """Esegui un comando di sistema e restituisci l'output, gestendo eventuali errori."""
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Errore nell'esecuzione del comando: {e}")
        return None

def salva_su_desktop(file_name, data):
    """Salva i dati in un file sul Desktop."""
    try:
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        if not os.path.exists(desktop_path):
            os.makedirs(desktop_path)
        
        file_path = os.path.join(desktop_path, file_name)
        with open(file_path, 'a') as file:
            file.write(data + '\n')
        print(f"Risultati salvati in: {file_path}")
    except Exception as e:
        print(f"Errore nel salvataggio del file {file_name}: {e}")

def risolvi_ip(dominio):
    """Risolvi l'indirizzo IP reale del dominio."""
    try:
        ip = socket.gethostbyname(dominio)
        print(f"IP di {dominio}: {ip}")
        return ip
    except socket.gaierror as e:
        print(f"Errore nel risolvere l'IP per il dominio {dominio}: {e}")
        return None

def esegui_nmap(dominio):
    """Esegui una scansione Nmap completa sul dominio."""
    print(f"\nEsecuzione Nmap su {dominio}...")
    comando = ["nmap", "-sV", "-p-", "--script=vuln", dominio]
    stdout = run_command(comando)
    
    if stdout:
        print(f"Risultati Nmap:\n{stdout}")
        salva_su_desktop(f"nmap_{dominio}.txt", stdout)

def esegui_sslscan(dominio):
    """Esegui l'analisi del certificato SSL con SSLyze."""
    print(f"\nAnalisi del certificato SSL per {dominio}...")
    comando = ["sslyze", "--regular", dominio]
    stdout = run_command(comando)
    
    if stdout:
        print(f"Risultati SSLyze:\n{stdout}")
        salva_su_desktop(f"ssl_{dominio}.txt", stdout)

def esegui_gobuster(dominio):
    """Esegui Gobuster per il brute forcing delle directory nascoste."""
    print(f"\nEsecuzione Gobuster su {dominio}...")
    wordlist = "/usr/share/wordlists/dirb/common.txt"  # Cambiare con il percorso della propria wordlist
    comando = ["gobuster", "dir", "-u", f"http://{dominio}", "-w", wordlist]
    stdout = run_command(comando)
    
    if stdout:
        print(f"Risultati Gobuster:\n{stdout}")
        salva_su_desktop(f"gobuster_{dominio}.txt", stdout)

def esegui_nikto(dominio):
    """Esegui Nikto per la scansione delle vulnerabilità web."""
    print(f"\nEsecuzione Nikto su {dominio}...")
    comando = ["nikto", "-host", dominio]
    stdout = run_command(comando)
    
    if stdout:
        print(f"Risultati Nikto:\n{stdout}")
        salva_su_desktop(f"nikto_{dominio}.txt", stdout)

def esegui_subfinder(dominio):
    """Esegui Subfinder per trovare sottodomini."""
    print(f"\nEsecuzione Subfinder per la scoperta di sottodomini su {dominio}...")
    comando = ["subfinder", "-d", dominio]
    stdout = run_command(comando)
    
    if stdout:
        print(f"Sottodomini trovati:\n{stdout}")
        salva_su_desktop(f"subfinder_{dominio}.txt", stdout)

def esegui_searchsploit(software):
    """Esegui Searchsploit per cercare vulnerabilità note nel software identificato."""
    print(f"\nCerca exploit per {software} con Searchsploit...")
    comando = ["searchsploit", software]
    stdout = run_command(comando)
    
    if stdout:
        print(f"Exploit trovati per {software}:\n{stdout}")
        salva_su_desktop(f"searchsploit_{software}.txt", stdout)

def main():
    """Funzione principale per eseguire le scansioni."""
    dominio = input("Inserisci il dominio del sito web (es: example.com): ")
    
    ip = risolvi_ip(dominio)
    
    if ip:
        print(f"\nInizio scansioni per {dominio} ({ip}) alle {datetime.now()}\n")
        
        # Esegui le varie scansioni
        esegui_nmap(dominio)
        esegui_sslscan(dominio)
        esegui_gobuster(dominio)
        esegui_nikto(dominio)
        esegui_subfinder(dominio)
        
        # Cerca exploit per software noti
        software = input("Inserisci il nome del software da cercare su Searchsploit (oppure premi invio per saltare): ")
        if software:
            esegui_searchsploit(software)
        
        print(f"\nScansioni completate per {dominio} alle {datetime.now()}")
    else:
        print("Impossibile proseguire senza l'IP del dominio.")

if __name__ == "__main__":
    main()
