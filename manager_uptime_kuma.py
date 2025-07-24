import subprocess
import yaml
import sys
import os

def run_kubectl_command(command, capture_output=False):
    """
    Executes a kubectl command.
    If capture_output is True, returns stdout, otherwise prints it directly.
    """
    try:
        if capture_output:
            result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
            return result.stdout.strip()
        else:
            result = subprocess.run(command, shell=True, check=True, text=True)
            print(result.stdout)
            if result.stderr:
                print(f"Error output:\n{result.stderr}")
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        print(f"Command output (stdout):\n{e.stdout}")
        print(f"Command error (stderr):\n{e.stderr}")
        sys.exit(1) # Exit if kubectl command fails
    return "" # Return empty string for non-captured output

def start_kuma(config_file):
    """Applies Kubernetes configurations."""
    print("\n--- 🚀 Demarrage de Uptime Kuma 🚀 ---")
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)

    files_to_apply = config.get('kubernetes_files', [])
    if not files_to_apply:
        print("No Kubernetes files specified in config.yaml for starting.")
        return

    for file in files_to_apply:
        if os.path.exists(file):
            print(f"🪄 Applying {file}...  ✨ ")
            run_kubectl_command(f"kubectl apply -f {file}")
        else:
            print(f"Warning: File not found: {file}. Skipping.")
    print("\n ✅ Le processus de démarrage d'Uptime Kuma est terminé. Le démarrage des pods peut prendre quelques instants. ✅")
    check_pod_status(config) # Automatically check status after starting

def stop_kuma(config_file):
    """Deletes Kubernetes configurations."""
    print("\n--- ⚠️ Arrêt de de toutes les ressources Uptime Kuma ⚠️---")
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)

    # We typically delete in reverse order of creation.
    files_to_delete = reversed(config.get('kubernetes_files', []))
    if not files_to_delete:
        print("No Kubernetes files specified in config.yaml for stopping.")
        return

    for file in files_to_delete:
        if os.path.exists(file):
            print(f" 🗑️ Deleting {file}... ❌ ")
            run_kubectl_command(f"kubectl delete -f {file}")
        else:
            print(f"Warning: File not found: {file}. Skipping deletion.")
    print("\n ✅ Le processus d'arrêt est terminé. ✅")

def check_pod_status(config):
    """Checks the status of pods, optionally filtering by namespace if defined."""
    print("\n --- 📊 Vérification de l'état de fonctionnement du Kuma Pod 📊 ---")
    namespace = config.get('namespace') # Get namespace from config

    if namespace:
        print(f" 🔍 Recherche de pods dans le Namespace : {namespace}")
        command = f"kubectl get pods -n {namespace} -l app=uptime-kuma"
    else:
        print("No specific namespace configured. Checking pods across all namespaces (may be verbose).")
        command = "kubectl get pods -l app=uptime-kuma --all-namespaces"

    output = run_kubectl_command(command, capture_output=True)

    if output:
        print("\n" + output)
    else:
        print("No Uptime Kuma pods found or unable to retrieve status.")
    print("\n --- ✅ Vérification de l'état du pod terminée ✅ ---")


def main():
    if len(sys.argv) < 2:
        print("Usage: python manage_kuma.py [start|stop|status]")
        sys.exit(1)

    action = sys.argv[1].lower()
    config_file = 'config.yaml' # Assuming config.yaml is in the same directory

    # Load config once to pass to status function
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)

    if action == 'start':
        start_kuma(config_file)
    elif action == 'stop':
        stop_kuma(config_file)
    elif action == 'status':
        check_pod_status(config)
    else:
        print(f"Invalid action: {action}. Please use 'start', 'stop', or 'status'.")
        sys.exit(1)

if __name__ == "__main__":
    main()