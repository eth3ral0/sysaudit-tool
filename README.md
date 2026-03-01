# sysaudit-tool : outil d'audit système et réseau

![image](https://github.com/eth3ral0/sysaudit-tool/blob/main/banner.png)

Outil d'audit informatique en Python permettant de collecter les informations d'un poste (CPU, mémoire, disques, OS, réseau) et de générer automatiquement un rapport PDF et Excel pour le suivi du parc.  

## Fonctionnalités

- Collecte des informations système : nom de machine, OS, version, date du scan.
- Récupération des caractéristiques CPU (cœurs physiques/logiques, fréquence).
- Mesure de l'utilisation de la mémoire (total, utilisé, pourcentage).
- Inventaire des disques (taille totale, utilisé, libre, pourcentage utilisé).
- Scan réseau optionnel d'une plage IP pour détecter les hôtes actifs.
- Génération d'un rapport **PDF** avec synthèse de l'état du poste.
- Génération d'un rapport **Excel** avec mise en forme et code couleur sur l'utilisation des disques (vert / orange / rouge).
- Journalisation basique des actions dans un fichier de log.

## Prérequis

- Python 3.x
- Bibliothèques Python :
  - `psutil`
  - `reportlab`
  - `openpyxl`

Installation des dépendances :

```bash
pip install -r requirements.txt
```

## Cas d'usage

- Préparer un inventaire de parc avant une migration, un renouvellement de matériel ou un audit interne.

- Aider une équipe support / helpdesk à identifier rapidement les postes à risque (disques presque pleins, mémoire très sollicitée).

- Générer des rapports PDF/Excel partageables avec un tuteur, un responsable IT ou une équipe projet.

- Servir de base pour des scripts d’automatisation plus avancés autour de la supervision et de la maintenance préventive.

## Exemple de sortie :

```bash
$ python main.py
============================================================
AUDIT INFORMATIQUE - Inventaire IT
============================================================

Collecte des infos systeme...
  Infos systeme collectees

Scan reseau (optionnel)...
  Entrez la plage reseau (ex: 192.168.1.0/24) ou appuyez sur Entree pour ignorer: 192.168.1.0/24
  Scan en cours...
  5 hote(s) UP detectes

Generation des rapports...
✓ PDF genere: reports/audit_it_20260107_210501.pdf
✓ Excel genere: reports/audit_it_20260107_210501.xlsx
============================================================
Audit termine !
  - PDF: reports/audit_it_20260107_210501.pdf
  - Excel: reports/audit_it_20260107_210501.xlsx
============================================================
```

## Améliorations futures 

- Ajouter un export JSON/CSV des données collectées pour intégration dans d’autres outils (SIEM, CMDB, etc.).
​
- Enrichir le scan réseau (détection des ports ouverts de base, résolution des noms d’hôtes).

- Ajouter une Interface GUI pour les utilisateurs non techniques.

- Implémenter un système d’alertes (e-mail, fichier récapitulatif) lorsque certains seuils sont dépassés (disque > 90%, mémoire > 85%, aucun antivirus détecté, etc.).

- Internationaliser l’outil (FR/EN) et rendre la génération de rapports configurable (choix des sections, activation/désactivation du scan réseau).

