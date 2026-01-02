#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agent de nettoyage CSV avec Gemini Pro
Usage: python csv_cleaner_agent.py mon_fichier.csv
"""

import sys
import os
import pandas as pd
from google import genai
from google.genai import types
from pathlib import Path
import json

class CSVCleanerAgent:
    def __init__(self, api_key):
        """Initialise l'agent avec la clé API Gemini"""
        self.client = genai.Client(api_key=api_key)
        self.model = 'gemini-1.5-flash'  # Modèle le plus récent et gratuit
        
    def analyze_csv(self, filepath):
        """Analyse le fichier CSV et détecte les anomalies"""
        print(f"\n📂 Lecture du fichier : {filepath}")
        
        try:
            # Lire le CSV
            df = pd.read_csv(filepath, encoding='utf-8')
        except UnicodeDecodeError:
            # Essayer avec un autre encodage si UTF-8 échoue
            df = pd.read_csv(filepath, encoding='latin-1')
        
        # Préparer un résumé du dataset
        summary = self._create_dataset_summary(df)
        
        print("\n🔍 Analyse des anomalies en cours...")
        
        # Demander à Gemini d'analyser
        prompt = f"""Tu es un expert en nettoyage de données. Analyse ce fichier CSV et identifie TOUTES les anomalies possibles.

INFORMATIONS SUR LE DATASET :
{summary}

ÉCHANTILLON DES DONNÉES (premières lignes) :
{df.head(10).to_string()}

STATISTIQUES :
{df.describe(include='all').to_string()}

Identifie les problèmes suivants :
1. Valeurs manquantes (NaN, vides, "N/A", etc.)
2. Doublons (lignes identiques)
3. Formats incohérents (dates, nombres, etc.)
4. Valeurs aberrantes ou impossibles
5. Colonnes mal nommées ou avec des espaces
6. Encodage de caractères problématique
7. Types de données incorrects
8. Espaces inutiles en début/fin de cellules

Réponds UNIQUEMENT avec un JSON valide dans ce format :
{{
    "anomalies": [
        {{
            "type": "type_anomalie",
            "description": "description détaillée",
            "colonnes_affectees": ["colonne1", "colonne2"],
            "nombre_lignes_affectees": 10,
            "gravite": "haute|moyenne|faible"
        }}
    ],
    "resume": "résumé général des problèmes trouvés"
}}
"""
        
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt
        )
        return self._parse_json_response(response.text), df
    
    def propose_corrections(self, anomalies_json, df):
        """Propose des corrections pour les anomalies détectées"""
        print("\n💡 Génération des propositions de correction...")
        
        prompt = f"""Tu es un expert en nettoyage de données. Voici les anomalies détectées :

{json.dumps(anomalies_json, indent=2, ensure_ascii=False)}

COLONNES DU DATASET : {list(df.columns)}
NOMBRE DE LIGNES : {len(df)}

Propose des corrections CONCRÈTES et APPLICABLES pour chaque anomalie.

Réponds UNIQUEMENT avec un JSON valide dans ce format :
{{
    "corrections": [
        {{
            "anomalie_ciblee": "description de l'anomalie",
            "action": "description de l'action à effectuer",
            "methode": "nom_methode_python",
            "parametres": {{"param1": "valeur1"}},
            "risque": "description des risques potentiels",
            "impact": "nombre de lignes/colonnes affectées"
        }}
    ],
    "ordre_execution": [0, 1, 2],
    "avertissements": ["avertissement1", "avertissement2"]
}}

Méthodes disponibles :
- drop_duplicates: supprimer les doublons
- fillna: remplir les valeurs manquantes
- strip_whitespace: supprimer les espaces
- convert_type: convertir le type de colonne
- rename_columns: renommer les colonnes
- remove_outliers: supprimer les valeurs aberrantes
- standardize_format: standardiser le format (dates, etc.)
"""
        
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt
        )
        return self._parse_json_response(response.text)
    
    def apply_corrections(self, df, corrections_json):
        """Applique les corrections au dataframe"""
        df_cleaned = df.copy()
        
        ordre = corrections_json.get('ordre_execution', range(len(corrections_json['corrections'])))
        
        for idx in ordre:
            correction = corrections_json['corrections'][idx]
            methode = correction['methode']
            params = correction.get('parametres', {})
            
            print(f"\n⚙️  Application : {correction['action']}")
            
            try:
                if methode == 'drop_duplicates':
                    avant = len(df_cleaned)
                    df_cleaned = df_cleaned.drop_duplicates()
                    print(f"   ✓ {avant - len(df_cleaned)} doublons supprimés")
                
                elif methode == 'fillna':
                    colonne = params.get('colonne')
                    valeur = params.get('valeur', '')
                    if colonne:
                        df_cleaned[colonne].fillna(valeur, inplace=True)
                    else:
                        df_cleaned.fillna(valeur, inplace=True)
                    print(f"   ✓ Valeurs manquantes remplies")
                
                elif methode == 'strip_whitespace':
                    colonnes = params.get('colonnes', df_cleaned.select_dtypes(include=['object']).columns)
                    for col in colonnes:
                        if col in df_cleaned.columns:
                            df_cleaned[col] = df_cleaned[col].astype(str).str.strip()
                    print(f"   ✓ Espaces supprimés dans {len(colonnes)} colonnes")
                
                elif methode == 'convert_type':
                    colonne = params.get('colonne')
                    nouveau_type = params.get('type')
                    if colonne and nouveau_type:
                        df_cleaned[colonne] = df_cleaned[colonne].astype(nouveau_type)
                    print(f"   ✓ Type de {colonne} converti en {nouveau_type}")
                
                elif methode == 'rename_columns':
                    mapping = params.get('mapping', {})
                    df_cleaned.rename(columns=mapping, inplace=True)
                    print(f"   ✓ {len(mapping)} colonnes renommées")
                
                elif methode == 'remove_outliers':
                    colonne = params.get('colonne')
                    if colonne and colonne in df_cleaned.columns:
                        Q1 = df_cleaned[colonne].quantile(0.25)
                        Q3 = df_cleaned[colonne].quantile(0.75)
                        IQR = Q3 - Q1
                        avant = len(df_cleaned)
                        df_cleaned = df_cleaned[
                            (df_cleaned[colonne] >= Q1 - 1.5 * IQR) & 
                            (df_cleaned[colonne] <= Q3 + 1.5 * IQR)
                        ]
                        print(f"   ✓ {avant - len(df_cleaned)} valeurs aberrantes supprimées")
                
                elif methode == 'standardize_format':
                    colonne = params.get('colonne')
                    format_type = params.get('format', 'date')
                    if format_type == 'date' and colonne:
                        df_cleaned[colonne] = pd.to_datetime(df_cleaned[colonne], errors='coerce')
                    print(f"   ✓ Format standardisé pour {colonne}")
                
            except Exception as e:
                print(f"   ⚠️  Erreur : {str(e)}")
        
        return df_cleaned
    
    def _create_dataset_summary(self, df):
        """Crée un résumé du dataset"""
        summary = f"""
Nombre de lignes : {len(df)}
Nombre de colonnes : {len(df.columns)}
Colonnes : {', '.join(df.columns)}

Types de données :
{df.dtypes.to_string()}

Valeurs manquantes par colonne :
{df.isnull().sum().to_string()}

Mémoire utilisée : {df.memory_usage(deep=True).sum() / 1024:.2f} KB
"""
        return summary
    
    def _parse_json_response(self, text):
        """Parse la réponse JSON de Gemini"""
        # Nettoyer la réponse (enlever les balises markdown si présentes)
        text = text.strip()
        if text.startswith('```json'):
            text = text[7:]
        if text.startswith('```'):
            text = text[3:]
        if text.endswith('```'):
            text = text[:-3]
        text = text.strip()
        
        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            print(f"⚠️  Erreur de parsing JSON : {e}")
            print(f"Réponse brute : {text[:500]}")
            return None


def main():
    """Fonction principale"""
    print("=" * 60)
    print("🤖 AGENT DE NETTOYAGE CSV AVEC GEMINI PRO")
    print("=" * 60)
    
    # Vérifier les arguments
    if len(sys.argv) < 2:
        print("\n❌ Usage : python csv_cleaner_agent.py fichier.csv")
        sys.exit(1)
    
    csv_file = sys.argv[1]
    
    # Vérifier que le fichier existe
    if not os.path.exists(csv_file):
        print(f"\n❌ Erreur : Le fichier '{csv_file}' n'existe pas.")
        sys.exit(1)
    
    # Récupérer la clé API
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("\n❌ Erreur : La variable d'environnement GEMINI_API_KEY n'est pas définie.")
        print("💡 Exécutez : set GEMINI_API_KEY=votre_cle_api")
        sys.exit(1)
    
    # Créer l'agent
    agent = CSVCleanerAgent(api_key)
    
    # Étape 1 : Analyser le CSV
    anomalies, df = agent.analyze_csv(csv_file)
    
    if not anomalies:
        print("\n❌ Impossible d'analyser le fichier.")
        sys.exit(1)
    
    # Afficher les anomalies
    print("\n" + "=" * 60)
    print("📋 ANOMALIES DÉTECTÉES")
    print("=" * 60)
    
    if 'resume' in anomalies:
        print(f"\n📝 Résumé : {anomalies['resume']}\n")
    
    for i, anomalie in enumerate(anomalies.get('anomalies', []), 1):
        gravite_emoji = {"haute": "🔴", "moyenne": "🟡", "faible": "🟢"}
        emoji = gravite_emoji.get(anomalie.get('gravite', 'moyenne'), "🟡")
        
        print(f"{emoji} Anomalie {i} [{anomalie.get('gravite', 'N/A').upper()}]")
        print(f"   Type : {anomalie.get('type', 'N/A')}")
        print(f"   Description : {anomalie.get('description', 'N/A')}")
        if anomalie.get('colonnes_affectees'):
            print(f"   Colonnes : {', '.join(anomalie['colonnes_affectees'])}")
        print(f"   Lignes affectées : {anomalie.get('nombre_lignes_affectees', 'N/A')}")
        print()
    
    # Étape 2 : Proposer des corrections
    corrections = agent.propose_corrections(anomalies, df)
    
    if not corrections:
        print("\n❌ Impossible de générer des corrections.")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("🔧 CORRECTIONS PROPOSÉES")
    print("=" * 60)
    
    if corrections.get('avertissements'):
        print("\n⚠️  AVERTISSEMENTS :")
        for warning in corrections['avertissements']:
            print(f"   • {warning}")
        print()
    
    for i, correction in enumerate(corrections.get('corrections', []), 1):
        print(f"\n✏️  Correction {i}")
        print(f"   Cible : {correction.get('anomalie_ciblee', 'N/A')}")
        print(f"   Action : {correction.get('action', 'N/A')}")
        print(f"   Impact : {correction.get('impact', 'N/A')}")
        if correction.get('risque'):
            print(f"   ⚠️  Risque : {correction['risque']}")
    
    # Étape 3 : Demander confirmation
    print("\n" + "=" * 60)
    reponse = input("\n❓ Voulez-vous appliquer ces corrections ? (oui/non) : ").strip().lower()
    
    if reponse not in ['oui', 'o', 'yes', 'y']:
        print("\n❌ Opération annulée.")
        sys.exit(0)
    
    # Étape 4 : Appliquer les corrections
    print("\n" + "=" * 60)
    print("🚀 APPLICATION DES CORRECTIONS")
    print("=" * 60)
    
    df_cleaned = agent.apply_corrections(df, corrections)
    
    # Sauvegarder le fichier nettoyé
    output_file = csv_file.replace('.csv', '_cleaned.csv')
    df_cleaned.to_csv(output_file, index=False, encoding='utf-8')
    
    print("\n" + "=" * 60)
    print("✅ NETTOYAGE TERMINÉ")
    print("=" * 60)
    print(f"\n📁 Fichier original : {csv_file}")
    print(f"📁 Fichier nettoyé : {output_file}")
    print(f"\n📊 Statistiques :")
    print(f"   Lignes avant : {len(df)}")
    print(f"   Lignes après : {len(df_cleaned)}")
    print(f"   Différence : {len(df) - len(df_cleaned)} lignes")
    print(f"\n✨ Le fichier nettoyé a été sauvegardé avec succès !")


if __name__ == "__main__":
    main()
