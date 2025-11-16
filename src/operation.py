from lecture_csv import Table

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