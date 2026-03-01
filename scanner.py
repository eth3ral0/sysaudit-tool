import subprocess
import platform
import ipaddress
from concurrent.futures import ThreadPoolExecutor, as_completed

class NetworkScanner:
    """Scanne les postes disponibles sur un reseau"""

    def __init__(self, network_range):
        """
        network_range : ex. "192.168.1.0/24"
        """
        self.network_range = network_range
        self.available_hosts = []

    def ping_host(self, ip):
        """Ping un seul host avec subprocess"""
        try:
            # Detecter l'OS pour adapter la commande ping
            param = "-n" if platform.system().lower() == "windows" else "-c"
            # -n 1 ou -c 1 = 1 seul paquet, -W 2 ou -w 2000 = timeout 2 secondes
            timeout_param = "-w" if platform.system().lower() == "windows" else "-W"
            timeout_value = "2000" if platform.system().lower() == "windows" else "2"
            
            command = ["ping", param, "1", timeout_param, timeout_value, str(ip)]
            result = subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            if result.returncode == 0:
                return {"ip": str(ip), "status": "UP"}
            else:
                return {"ip": str(ip), "status": "DOWN"}
        except Exception:
            return {"ip": str(ip), "status": "UNREACHABLE"}

    def scan_network(self, max_workers=10):
        """Scanne tout le reseau en parallele"""
        try:
            network = ipaddress.ip_network(self.network_range, strict=False)
            ips = list(network.hosts())

            print(f"Scanning {len(ips)} hosts in {self.network_range}...")

            results = []
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = {executor.submit(self.ping_host, ip): ip for ip in ips}
                for future in as_completed(futures):
                    result = future.result()
                    if result["status"] == "UP":
                        results.append(result)
                        print(f"  OK {result['ip']} is UP")

            return sorted(results, key=lambda x: x["ip"])
        except Exception as e:
            print(f"Erreur scan reseau: {e}")
            return []
