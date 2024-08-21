import nmap
import requests

# Fonction pour scanner les ports et les services
def scan_ports(ip):
    nm = nmap.PortScanner()
    nm.scan(ip, arguments='-T4 -F')  # Arguments : -T4 pour vitesse, -F pour scan rapide des ports
    print("Scan results:")
    print(nm.csv())

# Fonction pour effectuer du fuzzing sur les entrées de formulaires
def fuzz_form(url, form_data):
    response = requests.post(url, data=form_data)
    print(f"Testing with data: {form_data}")
    print(f"Response code: {response.status_code}")
    if response.status_code == 200:
        print("Response Content:")
        print(response.text[:500])  # Print the first 500 characters of the response for review

# Exemple de scan des ports pour une adresse IP
target_ip = '192.168.8.135'
print(f"Scanning ports on {target_ip}...")
scan_ports(target_ip)

# Exemple de fuzzing des formulaires pour BWAPP et WordPress
def fuzzing_example(url):
    form_data = {
        'username': 'test',
        'password': 'test'
    }
    print(f"\nFuzzing {url} with example data...")
    fuzz_form(url, form_data)

# Effectuer du fuzzing sur les URLs de BWAPP et WordPress
bwapp_url = 'http://192.168.8.135/bWAPP/portal.php'
wordpress_url = 'http://192.168.8.135/wordpress/'

fuzzing_example(bwapp_url)
fuzzing_example(wordpress_url)
