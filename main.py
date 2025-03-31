import requests
import socket
import re
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

def get_subdomains_crtsh(domain, retries=3):
    print("[+] Buscando subdomínios no crt.sh...")
    url = f"https://crt.sh/?q=%25.{domain}&output=json"
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                subdomains = sorted(set(entry["name_value"] for entry in data))
                if subdomains:
                    return subdomains
        except Exception:
            pass
        print(f"[!] Falha na busca pelo crt.sh, tentativa {attempt + 1} de {retries}...")
        time.sleep(2)
    return []

def get_subdomains_rapiddns(domain, retries=3):
    print("[+] Buscando subdomínios no RapidDNS...")
    url = f"https://rapiddns.io/s/{domain}?full=1"
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                subdomains = list(set(re.findall(r"[a-zA-Z0-9.-]+\." + re.escape(domain), response.text)))
                if subdomains:
                    return subdomains
        except Exception:
            pass
        print(f"[!] Falha na busca pelo RapidDNS, tentativa {attempt + 1} de {retries}...")
        time.sleep(2)
    return []

def resolve_ip(subdomain):
    try:
        return subdomain, socket.gethostbyname(subdomain)
    except socket.gaierror:
        return subdomain, "Não resolvido"

def check_subdomain_status(subdomain):
    try:
        response = requests.get(f"http://{subdomain}", timeout=3)
        return subdomain, response.status_code
    except requests.RequestException:
        return subdomain, "Não responde"

def is_email(domain):
    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", domain))

def save_results(domain, resolved_subs, subdomain_status):
    valid_subdomains = {
        sub: ip for sub, ip in resolved_subs.items()
        if subdomain_status.get(sub) == 200 and not is_email(sub) and ip != "Não resolvido"
    }

    filename = os.path.abspath(f"{domain}_subdomains_ativos_{len(valid_subdomains)}.txt")
    with open(filename, "w") as file:
        file.write(f"Resultados para {domain}\n")
        file.write(f"Total de subdomínios encontrados: {len(resolved_subs)}\n")
        file.write(f"Subdomínios ativos (código 200): {len(valid_subdomains)}\n\n")
        file.write("Subdomínios ativos:\n")
        for sub, ip in valid_subdomains.items():
            file.write(f"{sub} -> {ip}\n")
    
    print(f"[✔] Resultados salvos em: {filename}")
    print(f"[✔] Subdomínios ativos (código 200) salvos: {len(valid_subdomains)}")

def main(domain):
    print(f"[+] Iniciando busca de subdomínios para {domain}...")
    subdomains = set(get_subdomains_crtsh(domain))
    subdomains.update(get_subdomains_rapiddns(domain))
    subdomains = sorted(subdomains)
    
    if not subdomains:
        print("[!] Nenhum subdomínio encontrado. Tente novamente mais tarde.")
        return
    
    print(f"[+] Foram encontrados {len(subdomains)} subdomínios. Resolvendo IPs...")
    
    resolved_subs = {}
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(resolve_ip, sub): sub for sub in subdomains}
        for future in as_completed(futures):
            sub, ip = future.result()
            resolved_subs[sub] = ip
            print(f"[>] Resolvendo: {sub} -> {ip}")
    
    print("[+] Verificando status HTTP...")
    subdomain_status = {}
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(check_subdomain_status, sub): sub for sub in subdomains}
        for future in as_completed(futures):
            sub, status = future.result()
            subdomain_status[sub] = status
            print(f"[>] Checando: {sub} -> Status {status}")
    
    save_results(domain, resolved_subs, subdomain_status)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python script.py dominio.com")
    else:
        main(sys.argv[1])
