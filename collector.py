import platform
import socket
from datetime import datetime
import psutil
class SystemCollector:
    """Collecte les informations systeme du poste local"""

    def __init__(self):
        self.hostname = socket.gethostname()
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def get_basic_info(self):
        """Infos generales du poste"""
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
            except (PermissionError, SystemError, OSError):
                pass
        return disks

    def get_network_info(self):
        """Infos reseau (adresses IP, MAC)"""
        networks = []
        for iface, addresses in psutil.net_if_addrs().items():
            for addr in addresses:
                networks.append({
                    "interface": iface,
                    "address": addr.address,
                                        "family": "IPv4" if addr.family.name == "AF_INET" else ("IPv6" if addr.family.name == "AF_INET6" else addr.family.name),
                })
        return networks

    def get_installed_software(self):
        """Placeholder pour logiciels installes"""
        return "Liste des logiciels - fonctionnalite a venir"

    def compute_health_summary(self, data):
        """Analyse rapide de l'etat du poste"""
        summary = []
        # CPU
        cpu = data.get("cpu", {})
        cpu_percent = cpu.get("cpu_percent", 0) if cpu else 0
        if cpu_percent > 90:
            summary.append(f"CPU a {cpu_percent}% - fortement sollicite")
        elif cpu_percent > 0:
            summary.append(f"CPU a {cpu_percent}% - normal")
        # RAM
        mem = data.get("memory", {})
        mem_percent = mem.get("memory_percent", 0) if mem else 0
        if mem_percent > 85:
            summary.append(f"RAM a {mem_percent}% - risque de saturation")
        elif mem_percent > 0:
            summary.append(f"RAM a {mem_percent}% - normal")
        # Disques
        for d in data.get("disk", []):
            disk_percent = d.get("percent", 0)
            device = d.get("device", "inconnu")
            if disk_percent > 90:
                summary.append(f"Disque {device} a {disk_percent}% - presque plein")
        return " | ".join(summary) if summary else "Aucune information disponible"


    def collect_all(self):
        """Collecte toutes les informations et retourne un dictionnaire complet"""
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
