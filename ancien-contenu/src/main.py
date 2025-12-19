from lecture_csv import BaseDeDonnees
import operation as op
from exporter_csv import exporter_table

# 1. Créer la base
bdd = BaseDeDonnees()

# 2. Ajouter un CSV (exemple)
bdd.ajouter_table("data_fitness", "data/data_doublons.csv")

# Récupérer la table
table = bdd.get_table("data_fitness")

# 3. Suppression
op.nettoyer_espaces(table)
op.supprimer_doublons(table, ignorer_colonnes=["id"])
op.supprimer_lignes_vides(table)
op.supprimer_colonnes_specifiques(table, ["gender"])
op.corriger_types(table)

# 4. Exporter la nouvelle table
exporter_table(table, prefixe="data_fitness_clean")