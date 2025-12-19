import os
from datetime import datetime

def exporter_table(table, dossier_sortie="results", prefixe="table"):
    """
    Exporte les données d'un objet Table dans un fichier CSV.
    Le fichier est nommé avec un timestamp (date + heure).
    
    Exemple de sortie :
    results/table_2025-01-15_14-32-10.csv
    """

    # Vérifier qu'une table valide est donnée
    if table.data is None:
        print("Aucune donnée à exporter.")
        return

    # Créer le dossier results si nécessaire
    os.makedirs(dossier_sortie, exist_ok=True)

    # Générer un timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Construire le chemin du fichier
    nom_fichier = f"{prefixe}_{timestamp}.csv"
    chemin_complet = os.path.join(dossier_sortie, nom_fichier)

    # Exporter
    table.data.to_csv(chemin_complet, index=False)

    print(f"Fichier exporté : {chemin_complet}")

    return chemin_complet