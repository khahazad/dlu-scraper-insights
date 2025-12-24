import csv
import os

def save_or_update_csv(rows, filename, key="PlayerID"):
    """
    Sauvegarde un tableau dans un CSV.
    Si le CSV existe déjà, il est mis à jour en fusionnant les données
    selon la clé unique (par défaut PlayerID).
    """

    # 1. Charger l'existant si le fichier existe
    existing = {}
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if key in row:
                    existing[row[key]] = row

    # 2. Fusionner avec les nouvelles données
    for row in rows:
        row_key = row[key]
        if row_key in existing:
            # Mise à jour des champs existants
            existing[row_key].update(row)
        else:
            # Nouveau joueur
            existing[row_key] = row

    # 3. Déterminer toutes les colonnes (union des clés)
    fieldnames = set()
    for row in existing.values():
        fieldnames.update(row.keys())
    fieldnames = list(fieldnames)

    # 4. Sauvegarde finale
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(existing.values())

    print(f"CSV mis à jour : {filename}")
