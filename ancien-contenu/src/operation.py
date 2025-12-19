from lecture_csv import Table
import pandas as pd
import re

def supprimer_doublons(table, ignorer_colonnes=None):
    """
    Supprime les doublons d'un objet Table.
    ignorer_colonnes : liste de colonnes à ignorer dans la détection de doublons.
    """

    if table.data is None:
        print("Aucune donnée à nettoyer.")
        return

    # Colonnes à utiliser pour détecter les doublons
    if ignorer_colonnes is None:
        colonnes = table.data.columns
    else:
        colonnes = [col for col in table.data.columns if col not in ignorer_colonnes]

    nb_avant = len(table.data)

    table.data = table.data.drop_duplicates(subset=colonnes)

    nb_apres = len(table.data)
    nb_supprimes = nb_avant - nb_apres

    print(f"{nb_supprimes} doublons supprimés sur les colonnes suivantes : {colonnes}")
    return table

def supprimer_lignes_vides(table):
    """
    Supprime les lignes où toutes les valeurs sont manquantes.
    """
    if table.data is None:
        print("Aucune donnée à nettoyer.")
        return

    nb_avant = len(table.data)
    table.data = table.data.dropna(how="all")
    nb_apres = len(table.data)

    print(f"{nb_avant - nb_apres} lignes entièrement vides supprimées.")
    return table.data


def supprimer_colonnes_vides(table):
    """
    Supprime les colonnes entièrement vides.
    """
    if table.data is None:
        print("Aucune donnée à nettoyer.")
        return

    colonnes_avant = table.data.shape[1]
    table.data = table.data.dropna(axis=1, how="all")
    colonnes_apres = table.data.shape[1]

    print(f"{colonnes_avant - colonnes_apres} colonnes entièrement vides supprimées.")
    return table.data


def supprimer_colonnes_trop_vides(table, seuil=0.5):
    """
    Supprime les colonnes dont plus de `seuil` % des valeurs sont manquantes.
    Exemple : seuil = 0.5 -> supprime les colonnes avec plus de 50% de NaN.
    """
    if table.data is None:
        print("Aucune donnée à nettoyer.")
        return

    nb_lignes = len(table.data)
    colonnes_a_supprimer = []

    for col in table.data.columns:
        nb_nan = table.data[col].isna().sum()
        if nb_nan / nb_lignes >= seuil:
            colonnes_a_supprimer.append(col)

    table.data = table.data.drop(columns=colonnes_a_supprimer)

    print(f"Colonnes supprimées (trop de valeurs manquantes): {colonnes_a_supprimer}")
    return table.data


def supprimer_colonnes_specifiques(table, colonnes):
    """
    Supprime des colonnes par leur nom.
    """
    if table.data is None:
        print("Aucune donnée à nettoyer.")
        return

    table.data = table.data.drop(columns=[c for c in colonnes if c in table.data.columns])
    print(f"Colonnes supprimées : {colonnes}")
    return table.data

def nettoyer_espaces(table):
    """
    Nettoie toutes les colonnes de la table :
    - supprime les espaces en début/fin
    - supprime les espaces multiples
    - supprime les caractères invisibles (Unicode)
    """

    if table.data is None:
        print("Aucune donnée à nettoyer.")
        return

    def clean_value(val):
        # convertir en string si nécessaire
        if pd.isna(val):
            return val
        val = str(val)

        # supprimer caractères invisibles unicode (contrôles, non imprimables)
        val = re.sub(r"[\u200B-\u200F\u202A-\u202E\u2060-\u206F]+", "", val)

        # supprimer tabulations et retours à la ligne
        val = val.replace("\n", "").replace("\r", "").replace("\t", " ")

        # retirer espaces début/fin
        val = val.strip()

        # remplacer espaces multiples par un seul
        val = re.sub(r"\s+", " ", val)

        return val

    # Application colonne par colonne
    for col in table.data.columns:
        table.data[col] = table.data[col].apply(clean_value)

    print("Espaces et caractères invisibles nettoyés.")
    return table.data


def corriger_types(table):
    """
    Corrige les types :
    - convertit en nombres quand possible
    - convertit en dates quand possible
    """

    if table.data is None:
        print("Aucune donnée à nettoyer.")
        return

    df = table.data.copy()

    for col in df.columns:

        # Nettoyage préliminaire : enlever espaces invisibles + tab + retour ligne
        df[col] = df[col].apply(
            lambda x: re.sub(r"[\u200B-\u200F\u202A-\u202E\u2060-\u206F]+", "", str(x))
            if not pd.isna(x) else x
        )

        # Enlever les espaces internes pour les nombres (ex : "5 200" -> "5200")
        df[col] = df[col].apply(
            lambda x: x.replace(" ", "") if isinstance(x, str) else x
        )

        # Remplacer virgules par points
        df[col] = df[col].apply(
            lambda x: x.replace(",", ".") if isinstance(x, str) else x
        )

        # Conversion numérique
        df[col] = pd.to_numeric(df[col], errors='ignore')

        # Conversion date
        if df[col].dtype == object:
            try:
                df[col] = pd.to_datetime(df[col], errors='raise')
            except:
                pass

    table.data = df
    print("Types corrigés (version robuste).")
    return table.data
