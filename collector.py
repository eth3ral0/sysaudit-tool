import psutil
import platform
import socket
from datetime import datetime

class SystemCollector:
    """Collecte les informations système du poste local"""

    def __init__(self):
        self.hostname = socket.gethostname()
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def get_basic_info(self):
        """Infos générales du poste"""
        return {
            "hostname": self.hostname,
            "os": platform.system(),
            "os_version": platform.version(),
            "architecture": platform.architecture()[0],
            "scan_date": self.timestamp,
        }

    def get_cpu_info(self):
        """Infos CPU"""
        return {
            "cpu_count_physical": psutil.cpu_count(logical=False),
            "cpu_count_logical": psutil.cpu_count(logical=True),
            "cpu_percent": psutil.cpu_percent(interval=1),
            "cpu_freq_mhz": psutil.cpu_freq().current if psutil.cpu_freq() else "N/A",
        }

    def get_memory_info(self):
        """Infos RAM"""
        mem = psutil.virtual_memory()
        return {
            "memory_total_gb": round(mem.total / (1024**3), 2),
            "memory_used_gb": round(mem.used / (1024**3), 2),
            "memory_percent": mem.percent,
        }

    def get_disk_info(self):
        """Infos disque(s)"""
        disks = []
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disks.append({
                    "device": partition.device,
                    "mountpoint": partition.mountpoint,
                    "total_gb": round(usage.total / (1024**3), 2),
                    "used_gb": round(usage.used / (1024**3), 2),
                    "free_gb": round(usage.free / (1024**3), 2),
                    "percent": usage.percent,
                })
            except PermissionError:
                pass
        return disks

    def get_network_info(self):
        """Infos réseau (adresses IP, MAC)"""
        networks = []
        for iface, addresses in psutil.net_if_addrs().items():
            for addr in addresses:
                networks.append({
                    "interface": iface,
                    "address": addr.address,
                    "family": str(addr.family),
                })
        return networks

    def get_installed_software(self):
        """Placeholder pour logiciels installes"""
        return "Liste des logiciels : fonctionnalite a venir"

    def compute_health_summary(self, data):
        """Analyse rapide de l'etat du poste"""
        issues = []
        mem = data.get("memory", {})
        if mem and mem.get("memory_percent", 0) > 85:
            issues.append("RAM fortement sollicitee (>85%).")
        for d in data.get("disk", []):
            if d.get("percent", 0) > 90:
                issues.append(f"Disque {d.get('device')} presque plein (>90%).")
        if not issues:
            return "Aucun probleme majeur detecte."
        return " / ".join(issues)

    def collect_all(self):
        data = {
            "basic": self.get_basic_info(),
            "cpu": self.get_cpu_info(),
            "memory": self.get_memory_info(),
            "disk": self.get_disk_info(),
            "network": self.get_network_info(),
            "software": self.get_installed_software(),
        }
        # ajouter la synthese de sante
        data["health_summary"] = self.compute_health_summary(data)
        return data