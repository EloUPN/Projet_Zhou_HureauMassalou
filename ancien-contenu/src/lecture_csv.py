import pandas as pd

class Table:
    """
    Représente une table (CSV) chargée en mémoire.
    Fournit des méthodes pour accéder aux colonnes, lignes et informations.
    """

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.data = None
        self.load_csv()

    def load_csv(self):
        """Charge le CSV dans un DataFrame pandas."""
        try:
            self.data = pd.read_csv(self.file_path, sep=",")
            print(f"Fichier chargé : {self.file_path}")
            print(f"{len(self.data)} lignes, {len(self.data.columns)} colonnes")
        except FileNotFoundError:
            print(f"Erreur : fichier introuvable {self.file_path}")
        except Exception as e:
            print(f"Erreur lors du chargement : {e}")

    def get_columns(self):
        """Retourne la liste des colonnes."""
        return list(self.data.columns) if self.data is not None else []

    def get_sample(self, n=5):
        """Retourne un aperçu des premières lignes."""
        return self.data.head(n) if self.data is not None else None

    def info(self):
        """Affiche les informations générales sur la table."""
        if self.data is not None:
            print("Informations sur la table :")
            print(self.data.info())
        else:
            print("Aucune donnée chargée.")


class BaseDeDonnees:
    """
    Représente un ensemble de tables (plusieurs CSV, par exemple France / Allemagne).
    """

    def __init__(self):
        self.tables = {}

    def ajouter_table(self, nom: str, file_path: str):
        """Ajoute une table à partir d’un fichier CSV."""
        table = Table(file_path)
        self.tables[nom] = table
        print(f"Table '{nom}' ajoutee ({file_path})")

    def lister_tables(self):
        """Liste les tables actuellement chargées."""
        print("Tables disponibles :")
        for nom, table in self.tables.items():
            nb_lignes = len(table.data) if table.data is not None else 0
            print(f"- {nom} ({nb_lignes} lignes)")

    def get_table(self, nom: str):
        """Retourne la table demandée."""
        return self.tables.get(nom, None)
