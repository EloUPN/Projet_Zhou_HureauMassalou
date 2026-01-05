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
        Standardise le format des dates dans une colonne
        
        Args:
            df: DataFrame pandas
            colonne: Nom de la colonne
            format_sortie: Format de sortie souhaité (ou None pour garder datetime)
        
        Returns:
            DataFrame nettoyé, nombre de dates converties
        """
        df_clean = df.copy()
        
        # Convertir en datetime
        df_clean[colonne] = pd.to_datetime(df_clean[colonne], errors='coerce')
        
        # Compter les conversions réussies
        conversions = df_clean[colonne].notna().sum()
        
        # NE PAS formater en string, garder le type datetime
        # (Le CSV affichera automatiquement les dates correctement)
        
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
