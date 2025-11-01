from lecture_csv import BaseDeDonnees

# 1. Créer la base
bdd = BaseDeDonnees()

# 2. Ajouter un CSV (exemple)
bdd.ajouter_table("data_fitness", "data/random_fitness_dataset.csv")

# 3. Lister les tables
bdd.lister_tables()

# 4. Consulter un aperçu
table_fr = bdd.get_table("data_fitness")
print(table_fr.get_sample(10))
