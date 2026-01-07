from collector import SystemCollector
from scanner import NetworkScanner
from report import ReportGenerator


def main():
    print("=" * 60)
    print("AUDIT INFORMATIQUE - Inventaire IT")
    print("=" * 60)
    print()

    # 1. Collecte infos poste local
    print("Collecte des infos système...")
    collector = SystemCollector()
    data = collector.collect_all()
    print("  Infos système collectées")
    print()

    # 2. Optionnel : Scan réseau
    print("Scan réseau (optionnel)...")
    network_range = input("  Entrez la plage réseau (ex: 192.168.1.0/24) ou appuyez sur Entrée pour ignorer: ").strip()
    
    if network_range:
        scanner = NetworkScanner(network_range)
        hosts = scanner.scan_network()
        data["network_hosts"] = hosts
        print(f"  {len(hosts)} poste(s) trouvé(s)")
    print()

    # 3. Génère rapports
    print("Génération des rapports...")
    report_gen = ReportGenerator(data)
    pdf_file = report_gen.generate_pdf()
    excel_file = report_gen.generate_excel()
    print()

    print("=" * 60)
    print("Audit terminé !")
    print(f"  - PDF: {pdf_file}")
    print(f"  - Excel: {excel_file}")
    print("=" * 60)

if __name__ == "__main__":
    main()
