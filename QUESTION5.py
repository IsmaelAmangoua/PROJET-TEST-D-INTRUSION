from jinja2 import Environment, FileSystemLoader
import datetime
import matplotlib.pyplot as plt
import os

# Exemple de données de vulnérabilités
report_data = {
    'application': 'BWAPP et WordPress',
    'vulnerabilities': {
        'XSS': [
            {'url': 'http://192.168.8.135/bWAPP/portal.php', 'payload': '<script>alert(1)</script>', 'status': 'Vulnérable'},
            {'url': 'http://192.168.8.135/wordpress/', 'payload': '"><img src="x" onerror="alert(1)">', 'status': 'Vulnérable'}
        ],
        'SQL Injection': [
            {'url': 'http://192.168.8.135/bWAPP/portal.php', 'payload': "' OR '1'='1", 'status': 'Vulnérable'},
            {'url': 'http://192.168.8.135/wordpress/', 'payload': '" OR "1"="1', 'status': 'Vulnérable'}
        ]
    },
    'system_info': {
        'CPU Usage': '20%',
        'Memory Usage': '50%',
        'Disk Usage': '30%',
        'Processes Running': 150
    }
}

# Définir le chemin absolu du dossier contenant le template
template_dir = os.path.join(os.getcwd(), 'templates')

# Contexte à passer au template
context = {
    'application': report_data['application'],
    'vulnerabilities': report_data['vulnerabilities'],
    'system_info': report_data['system_info'],
    'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
}

# Extraire les données pour le graphique
def extract_vulnerability_data(vulnerabilities):
    severity_counts = {'XSS': len(vulnerabilities.get('XSS', [])),
                       'SQL Injection': len(vulnerabilities.get('SQL Injection', []))}
    return severity_counts

# Créer le graphique
def generate_vulnerability_chart(severity_counts):
    labels = list(severity_counts.keys())
    counts = list(severity_counts.values())

    fig, ax = plt.subplots()
    ax.bar(labels, counts, color=['blue', 'green'])
    ax.set_xlabel('Type de Vulnérabilité')
    ax.set_ylabel('Nombre')
    ax.set_title('Répartition des Vulnérabilités')

    # Sauvegarder le graphique
    chart_path = 'vulnerability_chart.png'
    plt.savefig(chart_path)
    plt.close()
    return chart_path

# Générer le rapport HTML avec Jinja2
def generate_html_report(context):
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template('report_template.html')

    # Générer le rendu HTML
    html_output = template.render(context)

    # Sauvegarder le rapport
    with open('report.html', 'w') as file:
        file.write(html_output)

# Exemple d'utilisation
if __name__ == "__main__":
    # Extraire les données pour le graphique
    severity_counts = extract_vulnerability_data(report_data['vulnerabilities'])

    # Générer le graphique
    chart_path = generate_vulnerability_chart(severity_counts)
    
    # Ajouter le chemin du graphique au contexte
    context['chart_path'] = chart_path

    # Générer le rapport HTML
    generate_html_report(context)
    
    print("Rapport généré avec succès : report.html")
    print(f"Graphique sauvegardé sous : {chart_path}")
