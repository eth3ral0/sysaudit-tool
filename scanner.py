import ping3
import ipaddress
from concurrent.futures import ThreadPoolExecutor, as_completed

class NetworkScanner:
    """Scanne les postes disponibles sur un réseau"""

    def __init__(self, network_range):
        """
        network_range : ex. "192.168.1.0/24"
        """
        self.network_range = network_range
        self.available_hosts = []

    def ping_host(self, ip):
        """Ping un seul host"""
        try:
            response = ping3.ping(str(ip), timeout=2)
            if response:
                return {"ip": str(ip), "status": "UP", "response_time": response}
            else:
                return {"ip": str(ip), "status": "DOWN"}
        except Exception:
            return {"ip": str(ip), "status": "UNREACHABLE"}

    def scan_network(self, max_workers=10):
        """Scanne tout le réseau en parallèle"""
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
                        print(f"  ✓ {result['ip']} is UP")

            return sorted(results, key=lambda x: x["ip"])
        except Exception as e:
            print(f"Erreur scan réseau: {e}")
            return []
