from lecture_csv import BaseDeDonnees
import operation as op
from exporter_csv import exporter_table

# 1. Créer la base
bdd = BaseDeDonnees()

# 2. Ajouter un CSV (exemple)
bdd.ajouter_table("data_fitness", "data/data_doublons.csv")

# 3. Supprimer doublons
new_table = op.supprimer_doublons(bdd.get_table("data_fitness"), ignorer_colonnes=["record_id"])

# 4. Exporter la nouvelle table
exporter_table(new_table)