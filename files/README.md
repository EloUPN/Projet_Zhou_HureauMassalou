# 🎯 Guide Complet - Agent IA Modulaire avec Operations

## 🏗️ Architecture du Système

Le système est composé de **2 fichiers principaux** :

### 1. **Operations.py** 📦
Contient **13 fonctions** de nettoyage CSV :
- `supprimer_doublons()` - Supprime les lignes identiques
- `supprimer_colonnes_vides()` - Supprime les colonnes vides
- `supprimer_lignes_vides()` - Supprime les lignes vides
- `nettoyer_espaces()` - Nettoie les espaces en début/fin
- `remplir_valeurs_manquantes()` - Remplit les valeurs manquantes
- `normaliser_noms_colonnes()` - Normalise les noms de colonnes
- `supprimer_valeurs_aberrantes()` - Supprime les outliers
- `convertir_type_colonne()` - Convertit les types de données
- `standardiser_format_date()` - Standardise les dates
- `remplacer_valeurs()` - Remplace des valeurs
- `supprimer_colonne()` - Supprime une colonne
- `filtrer_lignes_condition()` - Filtre selon condition
- `capitaliser_texte()` - Capitalise le texte

### 2. **agent_csv.py** 🤖
L'agent intelligent qui :
1. Analyse le CSV avec Mistral AI
2. Détecte les anomalies
3. Choisit les bonnes fonctions d'Operations.py
4. **Demande confirmation pour CHAQUE correction**
5. Applique les modifications
6. Sauvegarde le résultat

---

## 🚀 Installation

### Étape 1 : Obtenir la clé Mistral (gratuit)
1. Allez sur : https://console.mistral.ai/
2. Créez un compte
3. Cliquez sur "API Keys" → "Create new key"
4. Copiez votre clé

### Étape 2 : Installer les dépendances
```cmd
python -m pip install pandas requests numpy
```

### Étape 3 : Configurer la clé API
```cmd
set MISTRAL_API_KEY=votre_cle_ici
```

### Étape 4 : Placer les fichiers
Mettez ces fichiers dans le même dossier :
- `agent_csv.py`
- `Operations.py`
- `exemple_test.csv` (votre fichier à nettoyer)

---

## 💻 Utilisation

### Commande de base
```cmd
python agent_csv.py mon_fichier.csv
```

### Exemple complet
```cmd
cd C:\Users\VotreNom\MesFichiers
set MISTRAL_API_KEY=votre_cle
python agent_csv.py donnees.csv
```

---

## 📋 Exemple de Session Interactive

```
C:\...\files> python agent_csv.py exemple_test.csv

======================================================================
🤖 AGENT IA DE NETTOYAGE CSV (avec Mistral AI + Operations)
======================================================================

📂 Lecture du fichier : exemple_test.csv
✅ 14 lignes, 7 colonnes chargées

🔍 Analyse des anomalies avec Mistral AI...

======================================================================
🔧 CORRECTIONS PROPOSÉES
======================================================================

======================================================================
ANOMALIE 1/5
======================================================================

🔴 Type : doublons
📝 Description : 2 lignes identiques détectées dans le fichier
📊 Colonnes : toutes
⚡ Impact estimé : 2 lignes seront supprimées

🔧 Opération proposée : supprimer_doublons
⚙️  Paramètres :
   • colonnes = None

──────────────────────────────────────────────────────────────────────
❓ Appliquer cette correction ? (o=oui / n=non / q=quitter) : o

⚙️  Exécution en cours...
✅ Opération réussie : 2

======================================================================
ANOMALIE 2/5
======================================================================

🟡 Type : espaces_inutiles
📝 Description : Espaces en début/fin détectés dans les colonnes nom, prenom
📊 Colonnes : nom, prenom
⚡ Impact estimé : 5 cellules seront modifiées

🔧 Opération proposée : nettoyer_espaces
⚙️  Paramètres :
   • colonnes = ['nom', 'prenom']

──────────────────────────────────────────────────────────────────────
❓ Appliquer cette correction ? (o=oui / n=non / q=quitter) : o

⚙️  Exécution en cours...
✅ Opération réussie : 5

======================================================================
ANOMALIE 3/5
======================================================================

🟡 Type : valeurs_manquantes
📝 Description : 1 valeur manquante dans la colonne prenom
📊 Colonnes : prenom
⚡ Impact estimé : 1 cellule sera remplie

🔧 Opération proposée : remplir_valeurs_manquantes
⚙️  Paramètres :
   • colonne = prenom
   • valeur = 
   • methode = constant

──────────────────────────────────────────────────────────────────────
❓ Appliquer cette correction ? (o=oui / n=non / q=quitter) : n
⏭️  Correction ignorée.

======================================================================
ANOMALIE 4/5
======================================================================

🔴 Type : valeurs_aberrantes
📝 Description : Valeur aberrante détectée dans age (999)
📊 Colonnes : age
⚡ Impact estimé : 1 ligne sera supprimée

🔧 Opération proposée : supprimer_valeurs_aberrantes
⚙️  Paramètres :
   • colonne = age
   • methode = iqr
   • seuil = 1.5

──────────────────────────────────────────────────────────────────────
❓ Appliquer cette correction ? (o=oui / n=non / q=quitter) : o

⚙️  Exécution en cours...
✅ Opération réussie : 1

======================================================================
ANOMALIE 5/5
======================================================================

🟢 Type : noms_colonnes
📝 Description : Les noms de colonnes contiennent des majuscules
📊 Colonnes : toutes
⚡ Impact estimé : Format standardisé

🔧 Opération proposée : normaliser_noms_colonnes

──────────────────────────────────────────────────────────────────────
❓ Appliquer cette correction ? (o=oui / n=non / q=quitter) : o

⚙️  Exécution en cours...
✅ Opération réussie : {'date_embauche': 'date_embauche'}

======================================================================
📊 RÉSUMÉ FINAL
======================================================================

📈 Statistiques :
   • Lignes avant : 14
   • Lignes après : 11
   • Différence : 3 lignes
   • Colonnes avant : 7
   • Colonnes après : 7

🔧 Opérations effectuées : 4
   1. supprimer_doublons → 2
   2. nettoyer_espaces → 5
   3. supprimer_valeurs_aberrantes → 1
   4. normaliser_noms_colonnes → {'date_embauche': 'date_embauche'}

======================================================================
💾 Sauvegarder le fichier nettoyé ? (oui/non) : oui

======================================================================
✅ FICHIER SAUVEGARDÉ
======================================================================

📁 Fichier original : exemple_test.csv
📁 Fichier nettoyé : exemple_test_cleaned.csv

✨ Nettoyage terminé avec succès !
```

---

## 🎮 Contrôles pendant l'exécution

Pour chaque anomalie détectée, vous pouvez :

- **`o` ou `oui`** → Appliquer la correction
- **`n` ou `non`** → Ignorer cette correction
- **`q` ou `quitter`** → Arrêter le processus

---

## 🔧 Ajouter vos propres opérations

### Dans Operations.py, ajoutez :

```python
@staticmethod
def ma_nouvelle_operation(df, param1, param2):
    """
    Description de l'opération
    
    Args:
        df: DataFrame pandas
        param1: Description param1
        param2: Description param2
    
    Returns:
        DataFrame modifié, info sur les modifications
    """
    df_clean = df.copy()
    
    # Votre code ici
    
    return df_clean, "info sur ce qui a été fait"
```

### Dans lister_operations(), ajoutez :

```python
'ma_nouvelle_operation': {
    'description': 'Ce que fait l\'opération',
    'parametres': ['param1', 'param2']
}
```

### Dans agent_csv.py, dans _executer_operation(), ajoutez :

```python
elif operation_nom == 'ma_nouvelle_operation':
    param1 = parametres.get('param1')
    param2 = parametres.get('param2')
    return self.operations.ma_nouvelle_operation(df, param1, param2)
```

L'IA utilisera automatiquement votre nouvelle opération ! 🎉

---

## 📊 Fonctionnalités avancées

### 1. Tester une opération manuellement

```python
from Operations import Operations

ops = Operations()
df_clean, resultat = ops.supprimer_doublons(df)
print(f"Doublons supprimés : {resultat}")
```

### 2. Lister toutes les opérations

```cmd
python Operations.py
```

### 3. Mode debug

Modifiez `temperature` dans agent_csv.py pour ajuster la créativité de l'IA :
```python
"temperature": 0.1,  # Plus conservateur (0.0-1.0)
```

---

## 🐛 Dépannage

### Erreur : "MISTRAL_API_KEY non définie"
```cmd
set MISTRAL_API_KEY=votre_cle
```

### Erreur : "No module named 'Operations'"
➡️ Vérifiez que `Operations.py` est dans le même dossier que `agent_csv.py`

### Erreur : "No module named 'pandas'"
```cmd
python -m pip install pandas numpy
```

### L'IA propose des opérations incorrectes
➡️ Réduisez la température ou précisez mieux les descriptions dans `lister_operations()`

### Erreur de parsing JSON
➡️ L'IA a mal formaté sa réponse, relancez le script

---

## 💡 Avantages de ce système

✅ **Modulaire** - Facile d'ajouter de nouvelles opérations
✅ **Contrôle total** - Vous validez chaque correction
✅ **Intelligent** - L'IA comprend le contexte de vos données
✅ **Extensible** - Ajoutez vos propres règles métier
✅ **Traçable** - Voir exactement ce qui a été fait
✅ **Réversible** - Le fichier original est conservé

---

## 🎓 Cas d'usage

### Nettoyage de données RH
```python
# Dans Operations.py, ajoutez :
@staticmethod
def anonymiser_donnees(df, colonnes):
    """Anonymise les données sensibles"""
    # Votre code
```

### Validation de données comptables
```python
@staticmethod
def valider_montants(df, colonne, min_val, max_val):
    """Vérifie que les montants sont dans une plage"""
    # Votre code
```

### Enrichissement de données
```python
@staticmethod
def calculer_colonne(df, nouvelle_col, formule):
    """Ajoute une colonne calculée"""
    # Votre code
```

---

## 📚 Ressources

- **Mistral AI** : https://docs.mistral.ai/
- **Pandas** : https://pandas.pydata.org/docs/
- **Python** : https://docs.python.org/fr/3/

---

**Profitez de votre agent IA modulaire ! 🚀**
