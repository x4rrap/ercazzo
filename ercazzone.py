import os
import requests
from bs4 import BeautifulSoup
from termcolor import colored

def pulisci_schermo():
    """Pulisce lo schermo del terminale."""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_ascii_art():
    """Mostra il disegno ASCII all'inizio dell'esecuzione"""
    print(f"                       .-.
                      |_:_|
                     /(_Y_)\
.                   ( \/M\/ )
 '.               _.'-/'-'\-'._
   ':           _/.--'[[[[]'--.\_
     ':        /_'  : |::"| :  '.\
       ':     //   ./ |oUU| \.'  :\
         ':  _:'..' \_|___|_/ :   :|
           ':.  .'  |_[___]_|  :.':\
            [::\ |  :  | |  :   ; : \
             '-'   \/'.| |.' \  .;.' |
             |\_    \  '-'   :       |
             |  \    \ .:    :   |   |
             |   \    | '.   :    \  |
             /       \   :. .;       |
            /     |   |  :__/     :  \\
           |  |   |    \:   | \   |   ||
          /    \  : :  |:   /  |__|   /|
          |     : : :_/_|  /'._\  '--|_\
          /___.-/_|-'   \  \
                         '-'
                
by hagg4r")

def find_admin_page(url):
    """Trova la pagina admin del sito web"""
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(f"{url}/wp-admin/", headers=headers, timeout=5)
    if response.status_code == 200:
        print("\nPagina Admin Trovata!")
        print(f"URL: {response.url}")
        
        # Scarica la pagina admin in un file HTML
        html_file_path = os.path.join(os.path.expanduser("~"), "Desktop", f"{url}_admin.html")
        with open(html_file_path, "w") as f:
            f.write(response.text)
    else:
        print("Pagina Admin Non Trovata.")

def bypass_waf(url):
    """Tenta di bypassare il Web Application Firewall"""
    try:
        response = requests.get(f"{url}/waf_bypass", timeout=5)
        if response.status_code == 200:
            print("\nWAF Bypassato!")
            print(f"URL: {response.url}")
        else:
            print("WAF Non Bypassato.")
    except Exception as e:
        print(f"Errore durante il bypass del WAF: {e}")

def bypass_cloudflare(url):
    """Tenta di bypassare Cloudflare"""
    try:
        response = requests.get(f"https://{url}/cloudflare_bypass", timeout=5)
        if response.status_code == 200:
            print("\nCloudflare Bypassato!")
            print(f"URL: {response.url}")
        else:
            print("Cloudflare Non Bypassato.")
    except Exception as e:
        print(f"Errore durante il bypass di Cloudflare: {e}")

def sql_injection(url):
    """Esegue una SQL injection per l'URL specificato"""
    try:
        response = requests.get(f"{url}/sql injection", timeout=5)
        print("\nRisultati della SQL Injection:")
        sys.stdout.write(response.text.strip())
    except Exception as e:
        print(f"Errore durante l'esecuzione della SQL injection: {e}")

def scan_vulnerabilities(url):
    """Scansiona vulnerabilità sul sito web utilizzando OWASP ZAP"""
    # Scarica e installa il client API di OWASP ZAP
    owasp_zap_api_url = "https://github.com/zaproxy/zap-api-python/releases/download/v3.9.0/zapapi-3.9.0.jar"
    owasp_zap_api_path = os.path.join(os.path.expanduser("~"), "Desktop", "zapapi-3.9.0.jar")
    
    if not os.path.exists(owasp_zap_api_path):
        response = requests.get(owasp_zap_api_url, stream=True)
        with open(owasp_zap_api_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024): 
                if chunk: # filtra i chunk keep-alive
                    f.write(chunk)

    # Avvia OWASP ZAP
    zap_proxy = subprocess.Popen(["java", "-jar", owasp_zap_api_path, "run"])

    # Aggiungi l'URL target a OWASP ZAP
    os.system(f"echo 'target={url}' | {owasp_zap_api_path} api context")

    # Attendi che OWASP ZAP finisca di processare
    zap_proxy.wait()

    # Ottieni i risultati da OWASP ZAP
    html_content = subprocess.check_output([f"{owasp_zap_api_path} api core", "-k", "core:/v3/info/Alerts"]).decode("utf-8")
    soup = BeautifulSoup(html_content, "html.parser")
    vulnerability_results = str(soup.find_all("div", {"class": "alert alert-error"}))
    print("\nRisultati della Scansione di Vulnerabilità di OWASP ZAP:")
    sys.stdout.write(vulnerability_results)

def display_results(title, result):
    """Mostra i risultati in modo formattato"""
    print("\n")
    print(colored("+" + "-" * len(result) + "+", 'yellow'))
    print("| " + colored(title, 'blue') + ":")
    print("| " + colored(result, 'green'))
    print(colored("+" + "-" * len(result) + "+", 'yellow'))

def check_honey_pot(url):
    """Controlla se il sito è un honey pot"""
    try:
        response = requests.get(f"{url}/honey_pot", timeout=5)
        if response.status_code == 403 or response.status_code == 500:
            print("\nSito Honey Pot!")
            return True
        else:
            return False
    except Exception as e:
        print(f"Errore durante il controllo del sito honey pot: {e}")
        return None

def find_mail_admin(url):
    """Trova l'indirizzo email dell'amministratore del sito web"""
    try:
        response = requests.get(f"{url}/robots.txt", timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")
        admin_email = soup.find("mailto").text
        print("\nIndirizzo Email Amministratore Trovato:")
        print(admin_email)
    except Exception as e:
        print(f"Errore durante la ricerca dell'indirizzo email amministratore: {e}")

def find_admin_name(url):
    """Trova il nome dell'amministratore del sito web"""
    try:
        response = requests.get(f"{url}/about.html", timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")
        admin_name = soup.find("h2").text
        print("\nNome Amministratore Trovato:")
        print(admin_name)
    except Exception as e:
        print(f"Errore durante la ricerca del nome amministratore: {e}")

def bypass_admin_page(url):
    """Bypassa la pagina admin utilizzando command injection"""
    try:
        command = 'echo "Admin Page Bypassed!"'
        headers = {"User-Agent": "Mozilla/5.0", "X-Forwarded-For": command}
        response = requests.get(f"{url}/wp-admin/", headers=headers, timeout=5)
        if response.status_code == 200:
            print("\nPagina Admin Bypassata!")
            print(f"URL: {response.url}")
        else:
            print("Pagina Admin Non Bypassata.")
    except Exception as e:
        print(f"Errore durante il bypass della pagina admin: {e}")

def scan_site(url):
    """Scanna il sito web"""
    print(f"\nScansione in corso su {url}...")
    
    # Attiva Tor e configura la connessione anonima
    os.system("tor")

    find_mail_admin(url)
    find_admin_name(url)

    if not check_honey_pot(url):  # Se non è un honey pot
        bypass_waf(url)
        bypass_cloudflare(url)
        sql_injection(url)
        scan_vulnerabilities(url)

        bypass_admin_page(url)

        # Estrae informazioni dal sito
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")
        info = soup.find_all("meta")
        for i in info:
            print(f"\nInformazione trovata: {i['name']} - {i['content']}")
        
        # Avvisa se la pagina admin è stata trovata e fornisce il link
        find_admin_page(url)
    else:
        print("\nSito honey pot, scan abbandonato.")

if __name__ == "__main__":
    url = input("Inserisci l'URL del sito web da analizzare (es. http://example.com, https://example.onion o http://example.gov): ")
    
    # Pulizia dello schermo
    pulisci_schermo()
    
    # Mostra il disegno ASCII all'inizio dell'esecuzione
    display_ascii_art()

    # Scansione del sito
    scan_site(url)
