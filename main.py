from collector import SystemCollector
import logger
from scanner import NetworkScanner
from report import ReportGenerator
from logger import SimpleLogger

def main():
    logger = SimpleLogger()
    logger.log("Demarrage d'un nouvel audit informatique")
    try:
        print("=" * 60)
        print("AUDIT INFORMATIQUE - Inventaire IT")
        print("=" * 60)
        print()

        # 1. Collecte infos poste local
        print("Collecte des infos systeme...")
        collector = SystemCollector()
        data = collector.collect_all()
        print("  Infos systeme collectees")
        print()
        logger.log("Infos systeme collecte pour {}".format(data["basic"]["hostname"]))

        # 2. Optionnel : Scan reseau
        print("Scan reseau (optionnel)...")
        network_range = input("  Entrez la plage reseau (ex: 192.168.1.0/24) ou appuyez sur Entrée pour ignorer: ").strip()
        if network_range:
            scanner = NetworkScanner(network_range)
            hosts = scanner.scan_network()
            data["network_hosts"] = hosts
            logger.log("Scan reseau effectue sur {} ({} hote(s) UP)".format(network_range, len(hosts)))
        # 3. Genere rapports
        print("Generation des rapports...")
        report_gen = ReportGenerator(data)
        pdf_file = report_gen.generate_pdf()
        excel_file = report_gen.generate_excel()
        logger.log("Rapports generes: {}, {}".format(pdf_file, excel_file))
        
        print("=" * 60)
        print("Audit termine !")
        print(f"  - PDF: {pdf_file}")
        print(f"  - Excel: {excel_file}")
        print("=" * 60)
    except Exception as e:
        logger.log("Erreur pendant l'audit: {}".format(e))
        print("Une erreur est survenue:", e)

if __name__ == "__main__":
    main()
