#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module Operations - Fonctions de nettoyage CSV
Contient toutes les opérations disponibles pour nettoyer les fichiers CSV
"""

import pandas as pd
import numpy as np
from datetime import datetime

class Operations:
    """Classe contenant toutes les opérations de nettoyage CSV"""
    
    @staticmethod
    def supprimer_doublons(df, colonnes=None):
        """
        Supprime les lignes en double
        
        Args:
            df: DataFrame pandas
            colonnes: Liste des colonnes à considérer (None = toutes)
        
        Returns:
            DataFrame nettoyé, nombre de lignes supprimées
        """
        avant = len(df)
        df_clean = df.drop_duplicates(subset=colonnes, keep='first')
        apres = len(df_clean)
        return df_clean, avant - apres
    
    @staticmethod
    def supprimer_colonnes_vides(df, seuil=1.0):
        """
        Supprime les colonnes complètement vides ou presque vides
        
        Args:
            df: DataFrame pandas
            seuil: Proportion de valeurs manquantes (1.0 = 100% vides)
        
        Returns:
            DataFrame nettoyé, liste des colonnes supprimées
        """
        colonnes_avant = list(df.columns)
        seuil_lignes = len(df) * seuil
        
        colonnes_a_garder = []
        for col in df.columns:
            if df[col].isnull().sum() < seuil_lignes:
                colonnes_a_garder.append(col)
        
        df_clean = df[colonnes_a_garder]
        colonnes_supprimees = [col for col in colonnes_avant if col not in colonnes_a_garder]
        
        return df_clean, colonnes_supprimees
    
    @staticmethod
    def supprimer_lignes_vides(df, seuil=1.0):
        """
        Supprime les lignes complètement vides ou presque vides
        
        Args:
            df: DataFrame pandas
            seuil: Proportion de valeurs manquantes (1.0 = 100% vides)
        
        Returns:
            DataFrame nettoyé, nombre de lignes supprimées
        """
        avant = len(df)
        seuil_colonnes = len(df.columns) * seuil
        
        # Compter les valeurs manquantes par ligne
        valeurs_manquantes_par_ligne = df.isnull().sum(axis=1)
        df_clean = df[valeurs_manquantes_par_ligne < seuil_colonnes]
        
        apres = len(df_clean)
        return df_clean, avant - apres
    
    @staticmethod
    def nettoyer_espaces(df, colonnes=None):
        """
        Supprime les espaces en début et fin de cellules
        
        Args:
            df: DataFrame pandas
            colonnes: Liste des colonnes à nettoyer (None = toutes les colonnes texte)
        
        Returns:
            DataFrame nettoyé, nombre de cellules modifiées
        """
        df_clean = df.copy()
        modifications = 0
        
        if colonnes is None:
            colonnes = df_clean.select_dtypes(include=['object']).columns
        
        for col in colonnes:
            if col in df_clean.columns:
                avant = df_clean[col].astype(str)
                apres = avant.str.strip()
                modifications += (avant != apres).sum()
                df_clean[col] = apres
        
        return df_clean, modifications
    
    @staticmethod
    def remplir_valeurs_manquantes(df, colonne, valeur='n/a', methode='constant'):
        """
        Remplit les valeurs manquantes dans une colonne
        
        Args:
            df: DataFrame pandas
            colonne: Nom de la colonne
            valeur: Valeur de remplacement (pour methode='constant')
            methode: 'constant' (par défaut avec 'n/a'), 'moyenne', 'mediane', 'mode', 'forward', 'backward'
        
        Returns:
            DataFrame nettoyé, nombre de valeurs remplies
        """
        df_clean = df.copy()
        nb_manquantes = df_clean[colonne].isnull().sum()
        
        if methode == 'constant':
            df_clean[colonne].fillna(valeur, inplace=True)
        elif methode == 'moyenne':
            df_clean[colonne].fillna(df_clean[colonne].mean(), inplace=True)
        elif methode == 'mediane':
            df_clean[colonne].fillna(df_clean[colonne].median(), inplace=True)
        elif methode == 'mode':
            mode_val = df_clean[colonne].mode()
            if len(mode_val) > 0:
                df_clean[colonne].fillna(mode_val[0], inplace=True)
        elif methode == 'forward':
            df_clean[colonne].fillna(method='ffill', inplace=True)
        elif methode == 'backward':
            df_clean[colonne].fillna(method='bfill', inplace=True)
        
        return df_clean, nb_manquantes
    
    @staticmethod
    def normaliser_noms_colonnes(df):
        """
        Normalise les noms de colonnes (minuscules, sans espaces, sans caractères spéciaux)
        
        Args:
            df: DataFrame pandas
        
        Returns:
            DataFrame nettoyé, dictionnaire {ancien_nom: nouveau_nom}
        """
        df_clean = df.copy()
        mapping = {}
        
        nouveaux_noms = []
        for col in df_clean.columns:
            # Convertir en minuscules
            nouveau = str(col).lower()
            # Remplacer espaces et caractères spéciaux par underscore
            nouveau = nouveau.replace(' ', '_').replace('-', '_')
            # Supprimer les caractères spéciaux
            nouveau = ''.join(c if c.isalnum() or c == '_' else '_' for c in nouveau)
            # Supprimer les underscores multiples
            while '__' in nouveau:
                nouveau = nouveau.replace('__', '_')
            nouveau = nouveau.strip('_')
            
            nouveaux_noms.append(nouveau)
            if nouveau != col:
                mapping[col] = nouveau
        
        df_clean.columns = nouveaux_noms
        return df_clean, mapping
    
    @staticmethod
    def remplacer_valeurs_aberrantes(df, colonne, valeur_remplacement='n/a', methode='iqr', seuil=1.5):
        """
        Remplace les valeurs aberrantes (outliers) par 'n/a' au lieu de les supprimer
        
        Args:
            df: DataFrame pandas
            colonne: Nom de la colonne
            valeur_remplacement: Valeur pour remplacer les outliers (par défaut 'n/a')
            methode: 'iqr' (interquartile) ou 'zscore'
            seuil: Seuil pour la méthode (1.5 pour IQR, 3 pour z-score)
        
        Returns:
            DataFrame nettoyé, nombre de valeurs remplacées
        """
        df_clean = df.copy()
        
        # Sauvegarder la colonne originale
        colonne_originale = df_clean[colonne].copy()
        
        # Convertir en numérique pour calculer les outliers
        colonne_numerique = pd.to_numeric(df_clean[colonne], errors='coerce')
        
        # Identifier les outliers
        masque_outliers = pd.Series([False] * len(df_clean), index=df_clean.index)
        
        if methode == 'iqr':
            # Calculer IQR sur les valeurs non-NaN
            valeurs_valides = colonne_numerique.dropna()
            if len(valeurs_valides) > 0:
                Q1 = valeurs_valides.quantile(0.25)
                Q3 = valeurs_valides.quantile(0.75)
                IQR = Q3 - Q1
                limite_inf = Q1 - seuil * IQR
                limite_sup = Q3 + seuil * IQR
                masque_outliers = (colonne_numerique < limite_inf) | (colonne_numerique > limite_sup)
        
        elif methode == 'zscore':
            valeurs_valides = colonne_numerique.dropna()
            if len(valeurs_valides) > 0:
                moyenne = valeurs_valides.mean()
                std = valeurs_valides.std()
                if std > 0:
                    masque_outliers = np.abs((colonne_numerique - moyenne) / std) > seuil
        
        # Compter les outliers
        nb_outliers = masque_outliers.sum()
        
        # IMPORTANT : Convertir la colonne en type object (string) pour pouvoir y mettre 'n/a'
        df_clean[colonne] = df_clean[colonne].astype(str)
        
        # Remplacer par 'n/a'
        df_clean.loc[masque_outliers, colonne] = valeur_remplacement
        
        return df_clean, nb_outliers
    
    @staticmethod
    def convertir_type_colonne(df, colonne, nouveau_type):
        """
        Convertit le type de données d'une colonne
        
        Args:
            df: DataFrame pandas
            colonne: Nom de la colonne
            nouveau_type: 'int', 'float', 'str', 'date', 'bool'
        
        Returns:
            DataFrame nettoyé, nombre de conversions réussies
        """
        df_clean = df.copy()
        conversions = 0
        
        try:
            if nouveau_type == 'int':
                df_clean[colonne] = pd.to_numeric(df_clean[colonne], errors='coerce').astype('Int64')
            elif nouveau_type == 'float':
                df_clean[colonne] = pd.to_numeric(df_clean[colonne], errors='coerce')
            elif nouveau_type == 'str':
                df_clean[colonne] = df_clean[colonne].astype(str)
            elif nouveau_type == 'date':
                df_clean[colonne] = pd.to_datetime(df_clean[colonne], errors='coerce')
            elif nouveau_type == 'bool':
                df_clean[colonne] = df_clean[colonne].astype(bool)
            
            conversions = len(df_clean)
        except Exception as e:
            print(f"Erreur lors de la conversion : {e}")
        
        return df_clean, conversions
    
    @staticmethod
    def standardiser_format_date(df, colonne, format_sortie='%Y-%m-%d'):
        """
        Standardise le format des dates en essayant plusieurs formats sources.
        """
        df_clean = df.copy()
        
        # 1. Traduction du format de sortie (Sécurité IA)
        mapping_formats = {
            'YYYY-MM-DD': '%Y-%m-%d',
            'DD/MM/YYYY': '%d/%m/%Y',
            'DD-MM-YYYY': '%d-%m-%Y',
            'YYYY/MM/DD': '%Y/%m/%d'
        }
        format_python = mapping_formats.get(format_sortie, format_sortie)
        if '%' not in format_python:
            format_python = '%Y-%m-%d'

        # 2. Liste des formats sources à tester (du plus probable au moins probable)
        formats_a_tester = [None, '%d/%m/%Y', '%Y-%m-%d', '%d-%m-%Y', '%d.%m.%Y']
        
        dates_converties = pd.Series([pd.NaT] * len(df_clean), index=df_clean.index)
        
        # On essaie chaque format jusqu'à ce que la colonne soit convertie
        for fmt in formats_a_tester:
            masque_manquant = dates_converties.isna()
            if not masque_manquant.any():
                break
                
            try:
                temp_conv = pd.to_datetime(
                    df_clean.loc[masque_manquant, colonne], 
                    format=fmt, 
                    errors='coerce', 
                    dayfirst=True if fmt is None else None
                )
                dates_converties.update(temp_conv)
            except:
                continue

        # 3. Application du résultat et nettoyage des erreurs (ex: 99/99/9999)
        conversions = dates_converties.notna().sum()
        
        # On initialise tout à 'n/a' par défaut pour remplacer les dates invalides
        resultat = pd.Series('n/a', index=df_clean.index)
        
        # On ne remplit que les dates qu'on a réussi à formater
        masque_valides = dates_converties.notna()
        if masque_valides.any():
            resultat[masque_valides] = dates_converties[masque_valides].dt.strftime(format_python)
        
        # On préserve les cellules qui étaient déjà vides à l'origine (nan ou vide)
        masque_vide_origine = (
            df_clean[colonne].isna() | 
            (df_clean[colonne].astype(str).str.lower() == 'nan') | 
            (df_clean[colonne].astype(str).str.strip() == '')
        )
        resultat[masque_vide_origine] = ''
        
        # --- LIGNE CORRECTRICE : Assigner les changements au DataFrame ---
        df_clean[colonne] = resultat
        
        return df_clean, conversions
    
    
    
    @staticmethod
    def remplacer_valeurs(df, colonne, ancien, nouveau):
        """
        Remplace toutes les occurrences d'une valeur par une autre
        
        Args:
            df: DataFrame pandas
            colonne: Nom de la colonne
            ancien: Valeur à remplacer
            nouveau: Nouvelle valeur
        
        Returns:
            DataFrame nettoyé, nombre de remplacements
        """
        df_clean = df.copy()
        remplacements = (df_clean[colonne] == ancien).sum()
        df_clean[colonne] = df_clean[colonne].replace(ancien, nouveau)
        
        return df_clean, remplacements
    
    @staticmethod
    def supprimer_colonne(df, colonne):
        """
        Supprime une colonne
        
        Args:
            df: DataFrame pandas
            colonne: Nom de la colonne à supprimer
        
        Returns:
            DataFrame nettoyé, nom de la colonne supprimée
        """
        df_clean = df.copy()
        if colonne in df_clean.columns:
            df_clean = df_clean.drop(columns=[colonne])
            return df_clean, colonne
        return df_clean, None
    
    @staticmethod
    def filtrer_lignes_condition(df, colonne, operateur, valeur):
        """
        Filtre les lignes selon une condition
        
        Args:
            df: DataFrame pandas
            colonne: Nom de la colonne
            operateur: '==', '!=', '>', '<', '>=', '<='
            valeur: Valeur de comparaison
        
        Returns:
            DataFrame filtré, nombre de lignes supprimées
        """
        avant = len(df)
        
        if operateur == '==':
            df_clean = df[df[colonne] == valeur]
        elif operateur == '!=':
            df_clean = df[df[colonne] != valeur]
        elif operateur == '>':
            df_clean = df[df[colonne] > valeur]
        elif operateur == '<':
            df_clean = df[df[colonne] < valeur]
        elif operateur == '>=':
            df_clean = df[df[colonne] >= valeur]
        elif operateur == '<=':
            df_clean = df[df[colonne] <= valeur]
        else:
            df_clean = df
        
        apres = len(df_clean)
        return df_clean, avant - apres
    
    @staticmethod
    def remplacer_valeurs_invalides(df, colonne, valeur_remplacement='n/a', min_valeur=None, max_valeur=None):
        """
        Remplace les valeurs en dehors d'une plage acceptable par 'n/a'
        
        Args:
            df: DataFrame pandas
            colonne: Nom de la colonne
            valeur_remplacement: Valeur de remplacement (par défaut 'n/a')
            min_valeur: Valeur minimale acceptable (None = pas de limite)
            max_valeur: Valeur maximale acceptable (None = pas de limite)
        
        Returns:
            DataFrame nettoyé, nombre de valeurs remplacées
        """
        df_clean = df.copy()
        
        # Sauvegarder les valeurs originales
        colonne_originale = df_clean[colonne].copy()
        
        # Convertir en numérique pour tester les conditions
        colonne_numerique = pd.to_numeric(df_clean[colonne], errors='coerce')
        
        # Identifier les valeurs invalides
        masque_invalides = pd.Series([False] * len(df_clean), index=df_clean.index)
        
        # Valeurs en dehors de la plage
        if min_valeur is not None:
            masque_invalides |= (colonne_numerique < min_valeur)
        if max_valeur is not None:
            masque_invalides |= (colonne_numerique > max_valeur)
        
        # Valeurs qui n'ont pas pu être converties (sauf si déjà vides)
        masque_invalides |= (colonne_numerique.isna() & colonne_originale.notna())
        
        # Compter les invalides
        nb_invalides = masque_invalides.sum()
        
        # IMPORTANT : Convertir la colonne en type object (string) pour pouvoir y mettre 'n/a'
        df_clean[colonne] = df_clean[colonne].astype(str)
        
        # Remplacer par 'n/a'
        df_clean.loc[masque_invalides, colonne] = valeur_remplacement
        
        return df_clean, nb_invalides
    
    @staticmethod
    def normaliser_telephones(df, colonne, format_sortie='0600000000'):
        """
        Normalise les numéros de téléphone français vers un format standard
        
        Args:
            df: DataFrame pandas
            colonne: Nom de la colonne contenant les téléphones
            format_sortie: Format de sortie ('0600000000' ou '06 00 00 00 00')
        
        Returns:
            DataFrame nettoyé, nombre de téléphones normalisés
        """
        df_clean = df.copy()
        
        # Convertir en string
        df_clean[colonne] = df_clean[colonne].astype(str)
        
        import re
        nb_normalises = 0
        
        for idx in df_clean.index:
            tel = str(df_clean.loc[idx, colonne])
            
            # Ignorer les valeurs vides ou 'nan'
            if tel in ['', 'nan', 'n/a']:
                continue
            
            # Nettoyer : enlever tous les caractères non numériques
            tel_clean = re.sub(r'[^0-9]', '', tel)
            
            # Si commence par 33, remplacer par 0
            if tel_clean.startswith('33') and len(tel_clean) == 11:
                tel_clean = '0' + tel_clean[2:]
            
            # Vérifier que c'est un numéro français valide (10 chiffres, commence par 0)
            if len(tel_clean) == 10 and tel_clean[0] == '0':
                # Vérifier que c'est un mobile (06, 07) ou fixe valide (01-05, 09)
                deuxieme_chiffre = tel_clean[1]
                if deuxieme_chiffre in ['1', '2', '3', '4', '5', '6', '7', '9']:
                    # Formater selon le format demandé
                    if format_sortie == '06 00 00 00 00':
                        tel_formate = f"{tel_clean[0:2]} {tel_clean[2:4]} {tel_clean[4:6]} {tel_clean[6:8]} {tel_clean[8:10]}"
                    else:  # Format par défaut : 0600000000
                        tel_formate = tel_clean
                    
                    if tel_formate != df_clean.loc[idx, colonne]:
                        df_clean.loc[idx, colonne] = tel_formate
                        nb_normalises += 1
                else:
                    # Deuxième chiffre invalide (0, 8) → invalide
                    df_clean.loc[idx, colonne] = 'n/a'
                    nb_normalises += 1
            else:
                # Numéro invalide (longueur incorrecte ou ne commence pas par 0)
                df_clean.loc[idx, colonne] = 'n/a'
                nb_normalises += 1
        
        return df_clean, nb_normalises
    
    @staticmethod
    def forcer_type_texte(df, colonnes):
        """
        Force des colonnes à être de type texte (pour éviter conversion en numérique)
        Utile pour codes postaux, numéros de téléphone, etc.
        
        Args:
            df: DataFrame pandas
            colonnes: Liste des colonnes à convertir en texte
        
        Returns:
            DataFrame nettoyé, nombre de colonnes converties
        """
        df_clean = df.copy()
        nb_converties = 0
        
        for col in colonnes:
            if col in df_clean.columns:
                # Convertir en string et préserver les valeurs
                df_clean[col] = df_clean[col].astype(str)
                
                # Remplacer 'nan' par chaîne vide pour les valeurs manquantes
                df_clean.loc[df_clean[col] == 'nan', col] = ''
                
                # Pour les codes postaux, supprimer les .0 qui peuvent apparaître
                if 'code' in col.lower() or 'postal' in col.lower():
                    df_clean[col] = df_clean[col].str.replace('.0', '', regex=False)
                    # Ajouter le 0 devant si nécessaire (codes postaux à 4 chiffres)
                    df_clean.loc[(df_clean[col] != '') & (df_clean[col].str.len() == 4), col] = '0' + df_clean[col]
                
                nb_converties += 1
        
        return df_clean, nb_converties
    
    @staticmethod
    def valider_codes_postaux(df, colonne, valeur_remplacement='n/a'):
        """
        Valide les codes postaux français (5 chiffres)
        
        Args:
            df: DataFrame pandas
            colonne: Nom de la colonne
            valeur_remplacement: Valeur pour codes invalides
        
        Returns:
            DataFrame nettoyé, nombre de codes invalides
        """
        import re
        df_clean = df.copy()
        df_clean[colonne] = df_clean[colonne].astype(str)
        
        # Code postal français = 5 chiffres
        pattern = r'^[0-9]{5}$'
        
        invalides = ~df_clean[colonne].str.match(pattern, na=False)
        invalides &= (df_clean[colonne] != '') & (df_clean[colonne] != 'nan')
        
        nb_invalides = invalides.sum()
        df_clean.loc[invalides, colonne] = valeur_remplacement
        
        return df_clean, nb_invalides
    
    @staticmethod
    def remplacer_emails_invalides(df, colonne, valeur_remplacement='n/a'):
        """
        Remplace les emails invalides par 'n/a'
        
        Args:
            df: DataFrame pandas
            colonne: Nom de la colonne contenant les emails
            valeur_remplacement: Valeur de remplacement (par défaut 'n/a')
        
        Returns:
            DataFrame nettoyé, nombre d'emails invalides remplacés
        """
        df_clean = df.copy()
        
        # Convertir en string
        df_clean[colonne] = df_clean[colonne].astype(str)
        
        # Pattern simple pour email valide : contient @ et un point après le @
        import re
        pattern = r'^[^@]+@[^@]+\.[^@]+$'
        
        # Identifier les emails invalides (ceux qui ne matchent pas le pattern)
        masque_invalides = ~df_clean[colonne].str.match(pattern, na=False)
        
        # Ne pas compter les valeurs déjà vides comme invalides
        masque_invalides &= (df_clean[colonne] != '') & (df_clean[colonne] != 'nan')
        
        nb_invalides = masque_invalides.sum()
        
        # Remplacer par 'n/a'
        df_clean.loc[masque_invalides, colonne] = valeur_remplacement
        
        return df_clean, nb_invalides
    
    @staticmethod
    def capitaliser_texte(df, colonne, mode='title'):
        """
        Capitalise le texte d'une colonne
        
        Args:
            df: DataFrame pandas
            colonne: Nom de la colonne
            mode: 'title' (Première Lettre), 'upper' (MAJUSCULES), 'lower' (minuscules)
        
        Returns:
            DataFrame nettoyé, nombre de modifications
        """
        df_clean = df.copy()
        avant = df_clean[colonne].astype(str)
        
        if mode == 'title':
            apres = avant.str.title()
        elif mode == 'upper':
            apres = avant.str.upper()
        elif mode == 'lower':
            apres = avant.str.lower()
        else:
            apres = avant
        
        modifications = (avant != apres).sum()
        df_clean[colonne] = apres
        
        return df_clean, modifications
    
    # ===== NOUVELLES OPÉRATIONS COMPLÈTES =====
    
    # 1. NETTOYAGE STRUCTUREL
    
    @staticmethod
    def supprimer_accents(df, colonnes=None):
        """
        Supprime les accents des colonnes textuelles
        
        Args:
            df: DataFrame pandas
            colonnes: Liste des colonnes (None = toutes les colonnes texte)
        
        Returns:
            DataFrame nettoyé, nombre de modifications
        """
        import unicodedata
        df_clean = df.copy()
        nb_modifs = 0
        
        if colonnes is None:
            colonnes = df_clean.select_dtypes(include=['object']).columns
        
        for col in colonnes:
            if col in df_clean.columns:
                df_clean[col] = df_clean[col].astype(str).apply(
                    lambda x: ''.join(c for c in unicodedata.normalize('NFD', x) 
                                    if unicodedata.category(c) != 'Mn')
                    if x != 'nan' else x
                )
                nb_modifs += 1
        
        return df_clean, nb_modifs
    
    @staticmethod
    def uniformiser_categories(df, colonne, mapping):
        """
        Uniformise les variations de catégories (ex: "F"/"Femme"/"f" → "F")
        
        Args:
            df: DataFrame pandas
            colonne: Nom de la colonne
            mapping: Dictionnaire de mapping {valeur_ancienne: valeur_nouvelle}
        
        Returns:
            DataFrame nettoyé, nombre de remplacements
        """
        df_clean = df.copy()
        nb_remplacements = 0
        
        for ancien, nouveau in mapping.items():
            mask = df_clean[colonne] == ancien
            nb_remplacements += mask.sum()
            df_clean.loc[mask, colonne] = nouveau
        
        return df_clean, nb_remplacements
    
    @staticmethod
    def detecter_anomalies_type(df):
        """
        Détecte les colonnes avec des types de données incohérents
        
        Args:
            df: DataFrame pandas
        
        Returns:
            DataFrame propre, dict des anomalies détectées
        """
        anomalies = {}
        
        for col in df.columns:
            # Tenter conversion numérique
            essai_numeric = pd.to_numeric(df[col], errors='coerce')
            nb_non_numeric = essai_numeric.isna().sum() - df[col].isna().sum()
            
            if nb_non_numeric > 0 and nb_non_numeric < len(df) * 0.1:
                # Moins de 10% de valeurs non-numériques dans une colonne majoritairement numérique
                anomalies[col] = {
                    'type': 'mixte_numerique',
                    'nb_anomalies': nb_non_numeric,
                    'exemples': df[col][essai_numeric.isna() & df[col].notna()].head(3).tolist()
                }
        
        return df, anomalies
    
    @staticmethod
    def fusionner_colonnes_similaires(df, colonnes, nouveau_nom, separateur=' '):
        """
        Fusionne plusieurs colonnes en une seule
        
        Args:
            df: DataFrame pandas
            colonnes: Liste des colonnes à fusionner
            nouveau_nom: Nom de la nouvelle colonne
            separateur: Séparateur entre les valeurs
        
        Returns:
            DataFrame avec colonne fusionnée, nombre de colonnes supprimées
        """
        df_clean = df.copy()
        
        # Créer la nouvelle colonne
        df_clean[nouveau_nom] = df_clean[colonnes].astype(str).agg(separateur.join, axis=1)
        
        # Nettoyer les 'nan'
        df_clean[nouveau_nom] = df_clean[nouveau_nom].str.replace('nan', '').str.strip()
        
        # Supprimer les anciennes colonnes
        df_clean = df_clean.drop(columns=colonnes)
        
        return df_clean, len(colonnes)
    
    # 2. NETTOYAGE SÉMANTIQUE
    
    @staticmethod
    def verifier_format_iban(df, colonne, valeur_remplacement='n/a'):
        """
        Vérifie et nettoie les IBAN
        
        Args:
            df: DataFrame pandas
            colonne: Nom de la colonne
            valeur_remplacement: Valeur pour les IBAN invalides
        
        Returns:
            DataFrame nettoyé, nombre d'IBAN invalides
        """
        import re
        df_clean = df.copy()
        df_clean[colonne] = df_clean[colonne].astype(str)
        
        # Pattern simplifié IBAN (commence par 2 lettres puis chiffres)
        pattern = r'^[A-Z]{2}[0-9]{2}[A-Z0-9]+$'
        
        invalides = ~df_clean[colonne].str.match(pattern, na=False)
        invalides &= (df_clean[colonne] != '') & (df_clean[colonne] != 'nan')
        
        nb_invalides = invalides.sum()
        df_clean.loc[invalides, colonne] = valeur_remplacement
        
        return df_clean, nb_invalides
    
    @staticmethod
    def verifier_format_siret(df, colonne, valeur_remplacement='n/a'):
        """
        Vérifie les numéros SIRET (14 chiffres)
        
        Args:
            df: DataFrame pandas
            colonne: Nom de la colonne
            valeur_remplacement: Valeur pour les SIRET invalides
        
        Returns:
            DataFrame nettoyé, nombre de SIRET invalides
        """
        import re
        df_clean = df.copy()
        df_clean[colonne] = df_clean[colonne].astype(str)
        
        # SIRET = 14 chiffres
        pattern = r'^[0-9]{14}$'
        
        invalides = ~df_clean[colonne].str.match(pattern, na=False)
        invalides &= (df_clean[colonne] != '') & (df_clean[colonne] != 'nan')
        
        nb_invalides = invalides.sum()
        df_clean.loc[invalides, colonne] = valeur_remplacement
        
        return df_clean, nb_invalides
    
    @staticmethod
    def detecter_incoherences_dates(df, colonne_date, valeur_remplacement='n/a'):
        """
        Détecte les dates futures ou trop anciennes
        
        Args:
            df: DataFrame pandas
            colonne_date: Nom de la colonne de date
            valeur_remplacement: Valeur pour dates invalides
        
        Returns:
            DataFrame nettoyé, nombre de dates invalides
        """
        from datetime import datetime
        df_clean = df.copy()
        
        # Convertir en datetime
        dates = pd.to_datetime(df_clean[colonne_date], errors='coerce')
        aujourd_hui = pd.Timestamp.now()
        
        # Dates dans le futur
        futures = dates > aujourd_hui
        
        # Dates trop anciennes (avant 1900)
        anciennes = dates < pd.Timestamp('1900-01-01')
        
        invalides = futures | anciennes
        nb_invalides = invalides.sum()
        
        df_clean.loc[invalides, colonne_date] = valeur_remplacement
        
        return df_clean, nb_invalides
    
    @staticmethod
    def detecter_doublons_approximatifs(df, colonne, seuil_similarite=0.8):
        """
        Détecte les doublons approximatifs (fuzzy matching)
        
        Args:
            df: DataFrame pandas
            colonne: Nom de la colonne
            seuil_similarite: Seuil de similarité (0-1)
        
        Returns:
            DataFrame, liste des groupes de doublons
        """
        from difflib import SequenceMatcher
        
        valeurs = df[colonne].dropna().unique()
        groupes_doublons = []
        
        for i, val1 in enumerate(valeurs):
            groupe = [val1]
            for val2 in valeurs[i+1:]:
                similarite = SequenceMatcher(None, str(val1).lower(), str(val2).lower()).ratio()
                if similarite >= seuil_similarite:
                    groupe.append(val2)
            
            if len(groupe) > 1:
                groupes_doublons.append(groupe)
        
        return df, groupes_doublons
    
    @staticmethod
    def normaliser_devises(df, colonne, devise_cible='EUR', taux_change=None):
        """
        Normalise les montants vers une devise unique
        
        Args:
            df: DataFrame pandas
            colonne: Nom de la colonne
            devise_cible: Devise de sortie
            taux_change: Dict {devise: taux} ou None pour auto
        
        Returns:
            DataFrame normalisé, nombre de conversions
        """
        df_clean = df.copy()
        
        # Taux par défaut (approximatifs)
        if taux_change is None:
            taux_change = {
                'USD': 0.92,  # USD vers EUR
                'GBP': 1.17,  # GBP vers EUR
                'CHF': 0.96,  # CHF vers EUR
                'EUR': 1.0
            }
        
        # Détection automatique de devise dans la colonne (simplifiée)
        # Pour l'instant, retourne juste le df
        # Une vraie implémentation nécessiterait parsing des montants
        
        return df_clean, 0
    
    # 3. NORMALISATION ET STANDARDISATION
    
    @staticmethod
    def normaliser_unites(df, colonne, unite_cible, facteur_conversion):
        """
        Convertit les unités de mesure
        
        Args:
            df: DataFrame pandas
            colonne: Nom de la colonne
            unite_cible: Unité de sortie
            facteur_conversion: Facteur multiplicatif
        
        Returns:
            DataFrame normalisé, nombre de conversions
        """
        df_clean = df.copy()
        
        # Convertir en numérique et appliquer le facteur
        valeurs_num = pd.to_numeric(df_clean[colonne], errors='coerce')
        df_clean[colonne] = valeurs_num * facteur_conversion
        
        nb_conversions = valeurs_num.notna().sum()
        
        return df_clean, nb_conversions
    
    @staticmethod
    def arrondir_numerique(df, colonne, decimales=2):
        """
        Arrondit les valeurs numériques
        
        Args:
            df: DataFrame pandas
            colonne: Nom de la colonne
            decimales: Nombre de décimales
        
        Returns:
            DataFrame arrondi, nombre de valeurs arrondies
        """
        df_clean = df.copy()
        
        valeurs_num = pd.to_numeric(df_clean[colonne], errors='coerce')
        df_clean[colonne] = valeurs_num.round(decimales)
        
        nb_arrondis = valeurs_num.notna().sum()
        
        return df_clean, nb_arrondis
    
    @staticmethod
    def encoder_categories_onehot(df, colonne):
        """
        Encode une colonne catégorielle en One-Hot
        
        Args:
            df: DataFrame pandas
            colonne: Nom de la colonne à encoder
        
        Returns:
            DataFrame avec colonnes encodées, nombre de colonnes créées
        """
        df_clean = df.copy()
        
        # One-hot encoding
        dummies = pd.get_dummies(df_clean[colonne], prefix=colonne)
        
        # Supprimer la colonne originale et ajouter les dummies
        df_clean = df_clean.drop(columns=[colonne])
        df_clean = pd.concat([df_clean, dummies], axis=1)
        
        return df_clean, len(dummies.columns)
    
    @staticmethod
    def encoder_categories_label(df, colonne):
        """
        Encode une colonne catégorielle en numérique (Label Encoding)
        
        Args:
            df: DataFrame pandas
            colonne: Nom de la colonne
        
        Returns:
            DataFrame encodé, dict de mapping
        """
        df_clean = df.copy()
        
        # Créer le mapping
        categories = df_clean[colonne].dropna().unique()
        mapping = {cat: idx for idx, cat in enumerate(categories)}
        
        # Appliquer l'encodage
        df_clean[colonne] = df_clean[colonne].map(mapping)
        
        return df_clean, mapping
    
    @staticmethod
    def normaliser_variations_orthographe(df, colonne, mapping_corrections):
        """
        Corrige les variations orthographiques
        
        Args:
            df: DataFrame pandas
            colonne: Nom de la colonne
            mapping_corrections: Dict {erreur: correction}
        
        Returns:
            DataFrame corrigé, nombre de corrections
        """
        df_clean = df.copy()
        nb_corrections = 0
        
        for erreur, correction in mapping_corrections.items():
            mask = df_clean[colonne].str.contains(erreur, case=False, na=False)
            nb_corrections += mask.sum()
            df_clean.loc[mask, colonne] = df_clean.loc[mask, colonne].str.replace(
                erreur, correction, case=False, regex=False
            )
        
        return df_clean, nb_corrections
    
    # 4. QUALITÉ ET VALIDATION
    
    @staticmethod
    def generer_rapport_qualite(df):
        """
        Génère un rapport de qualité des données
        
        Args:
            df: DataFrame pandas
        
        Returns:
            DataFrame original, dict rapport qualité
        """
        rapport = {
            'nb_lignes': len(df),
            'nb_colonnes': len(df.columns),
            'valeurs_manquantes': df.isnull().sum().to_dict(),
            'taux_completude': (1 - df.isnull().sum() / len(df)).to_dict(),
            'doublons': df.duplicated().sum(),
            'types': df.dtypes.to_dict(),
            'memoire_mb': df.memory_usage(deep=True).sum() / 1024**2
        }
        
        return df, rapport
    
    @staticmethod
    def detecter_outliers_statistiques(df, colonne, methode='iqr', seuil=1.5):
        """
        Détecte les valeurs aberrantes sans les modifier (pour inspection)
        
        Args:
            df: DataFrame pandas
            colonne: Nom de la colonne
            methode: 'iqr' ou 'zscore'
            seuil: Seuil de détection
        
        Returns:
            DataFrame original, indices des outliers
        """
        valeurs_num = pd.to_numeric(df[colonne], errors='coerce')
        
        if methode == 'iqr':
            Q1 = valeurs_num.quantile(0.25)
            Q3 = valeurs_num.quantile(0.75)
            IQR = Q3 - Q1
            outliers = ((valeurs_num < Q1 - seuil * IQR) | 
                       (valeurs_num > Q3 + seuil * IQR))
        else:  # zscore
            mean = valeurs_num.mean()
            std = valeurs_num.std()
            outliers = np.abs((valeurs_num - mean) / std) > seuil
        
        indices_outliers = df[outliers].index.tolist()
        
        return df, indices_outliers
    
    @staticmethod
    def valider_schema(df, schema_attendu):
        """
        Valide que le DataFrame correspond au schéma attendu
        
        Args:
            df: DataFrame pandas
            schema_attendu: Dict {colonne: type_attendu}
        
        Returns:
            DataFrame original, dict des erreurs de validation
        """
        erreurs = {}
        
        # Vérifier les colonnes manquantes
        colonnes_manquantes = set(schema_attendu.keys()) - set(df.columns)
        if colonnes_manquantes:
            erreurs['colonnes_manquantes'] = list(colonnes_manquantes)
        
        # Vérifier les types
        for col, type_attendu in schema_attendu.items():
            if col in df.columns:
                type_actuel = df[col].dtype
                if str(type_actuel) != type_attendu:
                    erreurs[f'type_{col}'] = {
                        'attendu': type_attendu,
                        'actuel': str(type_actuel)
                    }
        
        return df, erreurs


def lister_operations():
    """Retourne la liste de toutes les opérations disponibles avec leur description"""
    operations = {
        'supprimer_doublons': {
            'description': 'Supprime les lignes en double',
            'parametres': ['colonnes (optionnel)']
        },
        'supprimer_colonnes_vides': {
            'description': 'Supprime les colonnes vides ou presque vides',
            'parametres': ['seuil (0.0-1.0)']
        },
        'supprimer_lignes_vides': {
            'description': 'Supprime les lignes vides ou presque vides',
            'parametres': ['seuil (0.0-1.0)']
        },
        'nettoyer_espaces': {
            'description': 'Supprime les espaces en début/fin de cellules',
            'parametres': ['colonnes (optionnel)']
        },
        'remplir_valeurs_manquantes': {
            'description': 'Remplit les valeurs manquantes avec n/a',
            'parametres': ['colonne', 'valeur (défaut: n/a)', 'methode']
        },
        'normaliser_noms_colonnes': {
            'description': 'Normalise les noms de colonnes',
            'parametres': []
        },
        'remplacer_valeurs_aberrantes': {
            'description': 'Remplace les valeurs aberrantes (outliers) par n/a',
            'parametres': ['colonne', 'valeur_remplacement', 'methode', 'seuil']
        },
        'convertir_type_colonne': {
            'description': 'Convertit le type de données',
            'parametres': ['colonne', 'nouveau_type']
        },
        'standardiser_format_date': {
            'description': 'Standardise le format des dates',
            'parametres': ['colonne', 'format']
        },
        'remplacer_valeurs': {
            'description': 'Remplace des valeurs spécifiques',
            'parametres': ['colonne', 'ancien', 'nouveau']
        },
        'supprimer_colonne': {
            'description': 'Supprime une colonne',
            'parametres': ['colonne']
        },
        'filtrer_lignes_condition': {
            'description': 'Filtre les lignes selon une condition',
            'parametres': ['colonne', 'operateur', 'valeur']
        },
        'capitaliser_texte': {
            'description': 'Capitalise le texte',
            'parametres': ['colonne', 'mode']
        },
        'remplacer_valeurs_invalides': {
            'description': 'Remplace les valeurs en dehors d\'une plage acceptable par n/a',
            'parametres': ['colonne', 'valeur_remplacement', 'min_valeur', 'max_valeur']
        },
        'remplacer_emails_invalides': {
            'description': 'Remplace les emails invalides (sans @ ou sans extension) par n/a',
            'parametres': ['colonne', 'valeur_remplacement']
        },
        'forcer_type_texte': {
            'description': 'Force des colonnes à rester en texte (codes postaux, téléphones, etc.)',
            'parametres': ['colonnes']
        },
        'valider_codes_postaux': {
            'description': 'Valide les codes postaux français (5 chiffres)',
            'parametres': ['colonne', 'valeur_remplacement']
        },
        'normaliser_telephones': {
            'description': 'Normalise les téléphones français vers format standard (0600000000)',
            'parametres': ['colonne', 'format_sortie']
        },
        
        # === NETTOYAGE STRUCTUREL ===
        'supprimer_accents': {
            'description': 'Supprime les accents des colonnes textuelles',
            'parametres': ['colonnes']
        },
        'uniformiser_categories': {
            'description': 'Uniformise les variations de catégories (ex: F/Femme/f → F)',
            'parametres': ['colonne', 'mapping']
        },
        'detecter_anomalies_type': {
            'description': 'Détecte les colonnes avec types incohérents',
            'parametres': []
        },
        'fusionner_colonnes_similaires': {
            'description': 'Fusionne plusieurs colonnes en une',
            'parametres': ['colonnes', 'nouveau_nom', 'separateur']
        },
        
        # === NETTOYAGE SÉMANTIQUE ===
        'verifier_format_iban': {
            'description': 'Vérifie et nettoie les IBAN',
            'parametres': ['colonne', 'valeur_remplacement']
        },
        'verifier_format_siret': {
            'description': 'Vérifie les numéros SIRET (14 chiffres)',
            'parametres': ['colonne', 'valeur_remplacement']
        },
        'detecter_incoherences_dates': {
            'description': 'Détecte les dates futures ou trop anciennes',
            'parametres': ['colonne_date', 'valeur_remplacement']
        },
        'detecter_doublons_approximatifs': {
            'description': 'Détecte les doublons approximatifs (fuzzy matching)',
            'parametres': ['colonne', 'seuil_similarite']
        },
        'normaliser_devises': {
            'description': 'Normalise les montants vers une devise unique',
            'parametres': ['colonne', 'devise_cible', 'taux_change']
        },
        
        # === NORMALISATION ET STANDARDISATION ===
        'normaliser_unites': {
            'description': 'Convertit les unités de mesure',
            'parametres': ['colonne', 'unite_cible', 'facteur_conversion']
        },
        'arrondir_numerique': {
            'description': 'Arrondit les valeurs numériques',
            'parametres': ['colonne', 'decimales']
        },
        'encoder_categories_onehot': {
            'description': 'Encode une colonne catégorielle en One-Hot',
            'parametres': ['colonne']
        },
        'encoder_categories_label': {
            'description': 'Encode une colonne catégorielle en numérique',
            'parametres': ['colonne']
        },
        'normaliser_variations_orthographe': {
            'description': 'Corrige les variations orthographiques',
            'parametres': ['colonne', 'mapping_corrections']
        },
        
        # === QUALITÉ ET VALIDATION ===
        'generer_rapport_qualite': {
            'description': 'Génère un rapport de qualité des données',
            'parametres': []
        },
        'detecter_outliers_statistiques': {
            'description': 'Détecte les outliers sans les modifier',
            'parametres': ['colonne', 'methode', 'seuil']
        },
        'valider_schema': {
            'description': 'Valide que le DataFrame correspond au schéma attendu',
            'parametres': ['schema_attendu']
        }
    }
    return operations


if __name__ == "__main__":
    # Test des opérations
    print("=" * 60)
    print("MODULE OPERATIONS - FONCTIONS DISPONIBLES")
    print("=" * 60)
    
    operations = lister_operations()
    for nom, info in operations.items():
        print(f"\n📌 {nom}")
        print(f"   Description: {info['description']}")
        print(f"   Paramètres: {', '.join(info['parametres']) if info['parametres'] else 'aucun'}")
