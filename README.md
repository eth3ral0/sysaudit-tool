# sysaudit-tool — outil d'audit système et réseau

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

