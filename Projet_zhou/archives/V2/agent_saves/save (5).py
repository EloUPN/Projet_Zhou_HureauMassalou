#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agent IA de Nettoyage CSV avec Mistral AI
L'agent détecte les anomalies et appelle les fonctions du module Operations
Usage: python agent_csv.py mon_fichier.csv
"""

import sys
import os
import pandas as pd
import requests
import json
from datetime import datetime
from Operations import Operations, lister_operations

class AgentCSV:
    def __init__(self, api_key):
        """Initialise l'agent avec la clé API Mistral"""
        self.api_key = api_key
        self.api_url = "https://api.mistral.ai/v1/chat/completions"
        self.model = "mistral-small-latest"
        self.operations = Operations()
        self.operations_disponibles = lister_operations()
        
    def _call_mistral(self, prompt):
        """Appelle l'API Mistral"""
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3,
            "max_tokens": 4000
        }
        
        try:
            response = requests.post(self.api_url, headers=headers, json=data, timeout=60)
            response.raise_for_status()
            result = response.json()
            return result['choices'][0]['message']['content']
        except requests.exceptions.RequestException as e:
            print(f"❌ Erreur API Mistral : {e}")
            return None
    
    def analyser_csv(self, filepath):
        """Analyse le fichier CSV et détecte les anomalies"""
        print(f"\n📂 Lecture du fichier : {filepath}")
        
        try:
            df = pd.read_csv(filepath, encoding='utf-8')
        except UnicodeDecodeError:
            try:
                df = pd.read_csv(filepath, encoding='latin-1')
            except:
                df = pd.read_csv(filepath, encoding='cp1252')
        
        print(f"✅ {len(df)} lignes, {len(df.columns)} colonnes chargées")
        
        # Créer le résumé pour l'IA
        resume = self._creer_resume(df)
        
        print("\n🔍 Analyse des anomalies avec Mistral AI...")
        
        # Créer la liste des opérations disponibles
        ops_desc = "\n".join([
            f"- {nom}: {info['description']} (paramètres: {', '.join(info['parametres']) if info['parametres'] else 'aucun'})"
            for nom, info in self.operations_disponibles.items()
        ])
        
        prompt = f"""Tu es un expert en nettoyage de données CSV. Analyse ce fichier et détecte TOUTES les anomalies.

RÉSUMÉ DU FICHIER :
{resume}

ÉCHANTILLON (10 premières lignes) :
{df.head(10).to_string()}

STATISTIQUES :
{df.describe(include='all').to_string()}

OPÉRATIONS DISPONIBLES :
{ops_desc}

RÈGLES IMPORTANTES ET ORDRE D'EXÉCUTION :
1. TOUJOURS EN PREMIER : forcer_type_texte pour code_postal, telephone, numero_employe
2. Normaliser les téléphones → normaliser_telephones
3. Valeurs aberrantes/invalides → remplacer par "n/a"
4. Emails invalides → remplacer par "n/a"
5. Doublons → supprimer
6. Espaces → nettoyer
7. Valeurs MANQUANTES → NE PAS TOUCHER

DÉTECTION OBLIGATOIRE - ORDRE STRICT :
1. Si colonnes code_postal, telephone, numero_employe existent → TOUJOURS proposer forcer_type_texte EN PREMIER
2. Si colonne telephone existe → TOUJOURS proposer normaliser_telephones APRÈS forcer_type_texte
3. Téléphones avec formats variés (espaces, points, tirets, +33) → normaliser_telephones
4. Emails sans @ ou sans extension → remplacer_emails_invalides
5. Âge : < 0 ou > 120 → remplacer_valeurs_invalides
6. Salaire : < 0 ou très élevé → remplacer_valeurs_invalides
7. Heures : < 0 ou > 70 → remplacer_valeurs_invalides
8. Codes postaux invalides (longueur) → remplacer_valeurs_invalides
9. Téléphones invalides (après normalisation) → déjà géré par normaliser_telephones

NE JAMAIS proposer remplir_valeurs_manquantes

ORDRE DE PRIORITÉ STRICT (RESPECTER CET ORDRE) :
1. forcer_type_texte (code_postal, telephone, numero_employe) - ID: 1
2. normaliser_telephones (si colonne telephone existe) - ID: 2
3. supprimer_doublons - ID: 3
4. nettoyer_espaces - ID: 4
5. remplacer_valeurs_invalides / remplacer_valeurs_aberrantes - ID: 5+
6. remplacer_emails_invalides - ID: ...
7. normaliser_noms_colonnes - ID: dernier

Ta tâche :
1. Identifier TOUTES les anomalies
2. Pour CHAQUE anomalie, proposer l'opération appropriée
3. RESPECTER L'ORDRE DE PRIORITÉ ci-dessus
4. Numéroter les IDs selon l'ordre d'exécution
5. TOUJOURS "n/a" pour remplacer valeurs problématiques

Réponds UNIQUEMENT avec un JSON valide (sans markdown, sans backticks) :
{{
    "anomalies": [
        {{
            "id": 1,
            "type": "colonnes_numeriques",
            "description": "Colonnes qui doivent rester en texte",
            "gravite": "haute",
            "colonnes_affectees": ["code_postal", "telephone", "numero_employe"],
            "operation": "forcer_type_texte",
            "parametres": {{
                "colonnes": ["code_postal", "telephone", "numero_employe"]
            }},
            "impact_estime": "3 colonnes forcées en texte"
        }},
        {{
            "id": 2,
            "type": "formats_telephones_varies",
            "description": "Formats de téléphone variés à normaliser",
            "gravite": "moyenne",
            "colonnes_affectees": ["telephone"],
            "operation": "normaliser_telephones",
            "parametres": {{
                "colonne": "telephone",
                "format_sortie": "0600000000"
            }},
            "impact_estime": "X téléphones normalisés"
        }}
    ]
}}

EXEMPLES CORRECTS (AVEC BON ORDRE) :
- ID 1 : {{"operation": "forcer_type_texte", "parametres": {{"colonnes": ["code_postal", "telephone"]}}}}
- ID 2 : {{"operation": "normaliser_telephones", "parametres": {{"colonne": "telephone", "format_sortie": "0600000000"}}}}
- ID 3 : {{"operation": "supprimer_doublons", "parametres": {{}}}}
- ID 4 : {{"operation": "remplacer_valeurs_invalides", "parametres": {{"colonne": "age", "valeur_remplacement": "n/a", "min_valeur": 0, "max_valeur": 120}}}}

IMPORTANT : 
- RESPECTER L'ORDRE : forcer_type_texte EN PREMIER, puis normaliser_telephones
- TOUJOURS détecter code_postal, telephone, numero_employe pour forcer_type_texte
- TOUJOURS proposer normaliser_telephones si colonne telephone existe
- NE JAMAIS toucher aux valeurs manquantes"""
        
        response = self._call_mistral(prompt)
        return self._parse_json(response), df
    
    def executer_avec_confirmation(self, df, anomalies_json):
        """Exécute les opérations une par une avec confirmation utilisateur"""
        df_courant = df.copy()
        operations_effectuees = []
        
        print("\n" + "=" * 70)
        print("🔧 CORRECTIONS PROPOSÉES")
        print("=" * 70)
        
        anomalies = anomalies_json.get('anomalies', [])
        
        if not anomalies:
            print("\n✨ Aucune anomalie détectée ! Votre CSV est propre.")
            return df_courant, operations_effectuees
        
        for i, anomalie in enumerate(anomalies, 1):
            print(f"\n{'='*70}")
            print(f"ANOMALIE {i}/{len(anomalies)}")
            print(f"{'='*70}")
            
            # Afficher les détails
            gravite_emoji = {"haute": "🔴", "moyenne": "🟡", "faible": "🟢"}
            emoji = gravite_emoji.get(anomalie.get('gravite', 'moyenne'), "🟡")
            
            print(f"\n{emoji} Type : {anomalie.get('type', 'N/A')}")
            print(f"📝 Description : {anomalie.get('description', 'N/A')}")
            if anomalie.get('colonnes_affectees'):
                print(f"📊 Colonnes : {', '.join(anomalie['colonnes_affectees'])}")
            print(f"⚡ Impact estimé : {anomalie.get('impact_estime', 'N/A')}")
            
            # Afficher l'opération proposée
            operation_nom = anomalie.get('operation')
            parametres = anomalie.get('parametres', {})
            
            print(f"\n🔧 Opération proposée : {operation_nom}")
            if parametres:
                print(f"⚙️  Paramètres :")
                for param, valeur in parametres.items():
                    print(f"   • {param} = {valeur}")
            
            # Demander confirmation
            print(f"\n{'─'*70}")
            reponse = input("❓ Appliquer cette correction ? (o=oui / n=non / q=quitter) : ").strip().lower()
            
            if reponse == 'q':
                print("\n⚠️  Opération interrompue par l'utilisateur.")
                break
            
            if reponse not in ['o', 'oui', 'y', 'yes']:
                print("⏭️  Correction ignorée.")
                continue
            
            # Exécuter l'opération
            print(f"\n⚙️  Exécution en cours...")
            
            try:
                resultat = self._executer_operation(df_courant, operation_nom, parametres)
                
                if resultat is not None:
                    df_courant, info = resultat
                    print(f"✅ Opération réussie : {info}")
                    operations_effectuees.append({
                        'anomalie': anomalie.get('type'),
                        'operation': operation_nom,
                        'resultat': info
                    })
                else:
                    print(f"❌ Opération échouée ou non reconnue : {operation_nom}")
            
            except Exception as e:
                print(f"❌ Erreur lors de l'exécution : {str(e)}")
        
        return df_courant, operations_effectuees
    
    def _executer_operation(self, df, operation_nom, parametres):
        """Exécute une opération du module Operations"""
        
        # Mapper les opérations aux méthodes
        if operation_nom == 'supprimer_doublons':
            colonnes = parametres.get('colonnes')
            return self.operations.supprimer_doublons(df, colonnes)
        
        elif operation_nom == 'supprimer_colonnes_vides':
            seuil = float(parametres.get('seuil', 1.0))
            return self.operations.supprimer_colonnes_vides(df, seuil)
        
        elif operation_nom == 'supprimer_lignes_vides':
            seuil = float(parametres.get('seuil', 1.0))
            return self.operations.supprimer_lignes_vides(df, seuil)
        
        elif operation_nom == 'nettoyer_espaces':
            colonnes = parametres.get('colonnes')
            return self.operations.nettoyer_espaces(df, colonnes)
        
        elif operation_nom == 'remplir_valeurs_manquantes':
            colonne = parametres.get('colonne')
            valeur = parametres.get('valeur', 'n/a')  # Par défaut n/a
            methode = parametres.get('methode', 'constant')
            return self.operations.remplir_valeurs_manquantes(df, colonne, valeur, methode)
        
        elif operation_nom == 'normaliser_noms_colonnes':
            return self.operations.normaliser_noms_colonnes(df)
        
        elif operation_nom == 'remplacer_valeurs_aberrantes':
            colonne = parametres.get('colonne')
            valeur_remplacement = parametres.get('valeur_remplacement', 'n/a')
            methode = parametres.get('methode', 'iqr')
            seuil = float(parametres.get('seuil', 1.5))
            return self.operations.remplacer_valeurs_aberrantes(df, colonne, valeur_remplacement, methode, seuil)
        
        elif operation_nom == 'convertir_type_colonne':
            colonne = parametres.get('colonne')
            nouveau_type = parametres.get('nouveau_type')
            return self.operations.convertir_type_colonne(df, colonne, nouveau_type)
        
        elif operation_nom == 'standardiser_format_date':
            colonne = parametres.get('colonne')
            format_sortie = parametres.get('format', '%Y-%m-%d')
            return self.operations.standardiser_format_date(df, colonne, format_sortie)
        
        elif operation_nom == 'remplacer_valeurs':
            colonne = parametres.get('colonne')
            ancien = parametres.get('ancien')
            nouveau = parametres.get('nouveau')
            return self.operations.remplacer_valeurs(df, colonne, ancien, nouveau)
        
        elif operation_nom == 'supprimer_colonne':
            colonne = parametres.get('colonne')
            return self.operations.supprimer_colonne(df, colonne)
        
        elif operation_nom == 'filtrer_lignes_condition':
            colonne = parametres.get('colonne')
            operateur = parametres.get('operateur')
            valeur = parametres.get('valeur')
            return self.operations.filtrer_lignes_condition(df, colonne, operateur, valeur)
        
        elif operation_nom == 'capitaliser_texte':
            colonne = parametres.get('colonne')
            mode = parametres.get('mode', 'title')
            return self.operations.capitaliser_texte(df, colonne, mode)
        
        elif operation_nom == 'remplacer_valeurs_invalides':
            colonne = parametres.get('colonne')
            valeur_remplacement = parametres.get('valeur_remplacement', 'n/a')
            min_valeur = parametres.get('min_valeur')
            max_valeur = parametres.get('max_valeur')
            # Convertir en float si ce sont des strings
            if min_valeur is not None:
                min_valeur = float(min_valeur)
            if max_valeur is not None:
                max_valeur = float(max_valeur)
            return self.operations.remplacer_valeurs_invalides(df, colonne, valeur_remplacement, min_valeur, max_valeur)
        
        elif operation_nom == 'remplacer_emails_invalides':
            colonne = parametres.get('colonne')
            valeur_remplacement = parametres.get('valeur_remplacement', 'n/a')
            return self.operations.remplacer_emails_invalides(df, colonne, valeur_remplacement)
        
        elif operation_nom == 'forcer_type_texte':
            colonnes = parametres.get('colonnes', [])
            if isinstance(colonnes, str):
                colonnes = [colonnes]
            return self.operations.forcer_type_texte(df, colonnes)
        
        elif operation_nom == 'normaliser_telephones':
            colonne = parametres.get('colonne')
            format_sortie = parametres.get('format_sortie', '0600000000')
            return self.operations.normaliser_telephones(df, colonne, format_sortie)
        
        else:
            return None
    
    def _creer_resume(self, df):
        """Crée un résumé du DataFrame"""
        resume = f"""
Nombre de lignes : {len(df)}
Nombre de colonnes : {len(df.columns)}
Colonnes : {', '.join(df.columns)}

Types de données :
{df.dtypes.to_string()}

Valeurs manquantes par colonne :
{df.isnull().sum().to_string()}

Doublons : {df.duplicated().sum()} lignes
"""
        return resume
    
    def _parse_json(self, text):
        """Parse la réponse JSON"""
        if not text:
            return None
        
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
            print(f"Réponse : {text[:300]}")
            return None


def main():
    """Fonction principale"""
    print("=" * 70)
    print("🤖 AGENT IA DE NETTOYAGE CSV (avec Mistral AI + Operations)")
    print("=" * 70)
    
    # Vérifier les arguments
    if len(sys.argv) < 2:
        print("\n❌ Usage : python agent_csv.py fichier.csv")
        sys.exit(1)
    
    csv_file = sys.argv[1]
    
    if not os.path.exists(csv_file):
        print(f"\n❌ Erreur : Le fichier '{csv_file}' n'existe pas.")
        sys.exit(1)
    
    # Vérifier la clé API
    api_key = os.getenv('MISTRAL_API_KEY')
    if not api_key:
        print("\n❌ Erreur : Variable MISTRAL_API_KEY non définie.")
        print("💡 Exécutez : set MISTRAL_API_KEY=votre_cle")
        print("💡 Obtenez une clé sur : https://console.mistral.ai/")
        sys.exit(1)
    
    # Créer l'agent
    agent = AgentCSV(api_key)
    
    # Analyser le CSV
    anomalies, df = agent.analyser_csv(csv_file)
    
    if not anomalies:
        print("\n❌ Impossible d'analyser le fichier.")
        sys.exit(1)
    
    # Exécuter avec confirmation
    df_clean, operations = agent.executer_avec_confirmation(df, anomalies)
    
    # Résumé final
    print("\n" + "=" * 70)
    print("📊 RÉSUMÉ FINAL")
    print("=" * 70)
    
    print(f"\n📈 Statistiques :")
    print(f"   • Lignes avant : {len(df)}")
    print(f"   • Lignes après : {len(df_clean)}")
    print(f"   • Différence : {len(df) - len(df_clean)} lignes")
    print(f"   • Colonnes avant : {len(df.columns)}")
    print(f"   • Colonnes après : {len(df_clean.columns)}")
    
    print(f"\n🔧 Opérations effectuées : {len(operations)}")
    for i, op in enumerate(operations, 1):
        print(f"   {i}. {op['operation']} → {op['resultat']}")
    
    # Demander si on sauvegarde
    if len(operations) > 0:
        print("\n" + "=" * 70)
        reponse = input("💾 Sauvegarder le fichier nettoyé ? (oui/non) : ").strip().lower()
        
        if reponse in ['oui', 'o', 'yes', 'y']:
            # Créer le dossier Cleaned s'il n'existe pas
            cleaned_dir = os.path.join(os.path.dirname(os.path.abspath(csv_file)), 'Cleaned')
            os.makedirs(cleaned_dir, exist_ok=True)
            
            # Générer le timestamp
            timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            
            # Créer le nom du fichier avec timestamp
            base_name = os.path.splitext(os.path.basename(csv_file))[0]
            output_file = os.path.join(cleaned_dir, f"{base_name}_cleaned_{timestamp}.csv")
            
            # Sauvegarder
            df_clean.to_csv(output_file, index=False, encoding='utf-8')
            
            print("\n" + "=" * 70)
            print("✅ FICHIER SAUVEGARDÉ")
            print("=" * 70)
            print(f"\n📁 Fichier original : {csv_file}")
            print(f"📁 Fichier nettoyé : {output_file}")
            print(f"📁 Dossier : {cleaned_dir}")
            print(f"🕐 Timestamp : {timestamp}")
            print("\n✨ Nettoyage terminé avec succès !")
        else:
            print("\n⚠️  Fichier non sauvegardé.")
    else:
        print("\n✨ Aucune modification effectuée.")


if __name__ == "__main__":
    main()
