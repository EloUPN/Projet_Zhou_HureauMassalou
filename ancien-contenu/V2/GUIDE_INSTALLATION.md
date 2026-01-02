# 🤖 Guide d'Installation - Agent de Nettoyage CSV avec Gemini Pro

## 📋 Prérequis

### 1. Python
Vérifiez si Python est installé :
```cmd
python --version
```

Si Python n'est pas installé, téléchargez-le depuis : https://www.python.org/downloads/
⚠️ **Important** : Cochez "Add Python to PATH" lors de l'installation !

### 2. Clé API Gemini
1. Allez sur : https://makersuite.google.com/app/apikey
2. Connectez-vous avec votre compte Google
3. Cliquez sur "Create API Key"
4. Copiez votre clé API (elle ressemble à : `AIzaSy...`)

## 🚀 Installation

### Étape 1 : Créer un dossier pour le projet
```cmd
cd C:\Users\VotreNom\Documents
mkdir csv-cleaner
cd csv-cleaner
```

### Étape 2 : Placer les fichiers
Copiez ces deux fichiers dans le dossier `csv-cleaner` :
- `csv_cleaner_agent.py`
- `requirements.txt`

### Étape 3 : Installer les dépendances
Ouvrez le terminal (cmd) dans le dossier et exécutez :
```cmd
pip install -r requirements.txt
```

### Étape 4 : Configurer la clé API
Remplacez `VOTRE_CLE_API` par votre vraie clé :
```cmd
set GEMINI_API_KEY=VOTRE_CLE_API
```

⚠️ **Note** : Cette commande est temporaire. Pour la rendre permanente :
1. Recherchez "Variables d'environnement" dans Windows
2. Cliquez sur "Modifier les variables d'environnement système"
3. Cliquez sur "Variables d'environnement"
4. Dans "Variables utilisateur", cliquez sur "Nouvelle"
5. Nom : `GEMINI_API_KEY`
6. Valeur : Votre clé API
7. OK, OK, OK

## 💡 Utilisation

### Utilisation basique
```cmd
python csv_cleaner_agent.py mon_fichier.csv
```

### Exemple complet
```cmd
cd C:\Users\VotreNom\Documents\csv-cleaner
python csv_cleaner_agent.py donnees.csv
```

L'agent va :
1. ✅ Analyser votre fichier CSV
2. ✅ Détecter les anomalies (doublons, valeurs manquantes, etc.)
3. ✅ Proposer des corrections
4. ✅ Demander votre confirmation
5. ✅ Créer un nouveau fichier `donnees_cleaned.csv`

## 📝 Exemples de fichiers CSV à tester

Créez un fichier `test.csv` avec des anomalies volontaires :
```csv
nom,age,email,date_inscription
Jean Dupont,25,jean@email.com,2023-01-15
Marie Martin,  30,marie@email.com,2023-02-20
Jean Dupont,25,jean@email.com,2023-01-15
Pierre,,pierre@email,15/03/2023
,28,test@test.com,2023-04-01
Sophie Durant,999,sophie@email.com,2023-05-10
```

Puis lancez :
```cmd
python csv_cleaner_agent.py test.csv
```

## 🐛 Dépannage

### Erreur : "Python n'est pas reconnu"
➡️ Python n'est pas dans le PATH. Réinstallez Python en cochant "Add to PATH"

### Erreur : "GEMINI_API_KEY n'est pas définie"
➡️ Exécutez : `set GEMINI_API_KEY=votre_cle`

### Erreur : "No module named 'pandas'"
➡️ Exécutez : `pip install -r requirements.txt`

### Erreur : "UnicodeDecodeError"
➡️ Le script essaie automatiquement plusieurs encodages (UTF-8, Latin-1)

### L'agent ne trouve pas d'anomalies
➡️ Votre CSV est peut-être déjà propre ! 🎉

## 🎯 Fonctionnalités

L'agent détecte automatiquement :
- ✅ Valeurs manquantes (cellules vides, NaN)
- ✅ Doublons (lignes identiques)
- ✅ Espaces inutiles en début/fin de cellules
- ✅ Formats de dates incohérents
- ✅ Valeurs aberrantes (ex: âge = 999)
- ✅ Problèmes d'encodage
- ✅ Types de données incorrects
- ✅ Colonnes mal nommées

L'agent peut appliquer :
- 🔧 Suppression des doublons
- 🔧 Remplissage des valeurs manquantes
- 🔧 Suppression des espaces
- 🔧 Conversion de types
- 🔧 Renommage de colonnes
- 🔧 Suppression des valeurs aberrantes
- 🔧 Standardisation des formats

## 📚 Ressources

- Documentation Gemini : https://ai.google.dev/docs
- Documentation Pandas : https://pandas.pydata.org/docs/
- Python pour débutants : https://docs.python.org/fr/3/tutorial/

## 💬 Conseils

1. **Testez d'abord** sur une copie de votre fichier important
2. **Vérifiez** le fichier `*_cleaned.csv` avant de supprimer l'original
3. **Lisez attentivement** les propositions de l'agent avant de confirmer
4. **L'agent n'est pas parfait** - vérifiez toujours les résultats

## 🎓 Pour aller plus loin

### Personnaliser l'agent
Vous pouvez modifier le fichier `csv_cleaner_agent.py` pour :
- Ajouter vos propres règles de nettoyage
- Changer le modèle Gemini utilisé
- Ajuster les seuils de détection d'anomalies
- Personnaliser le format de sortie

### Automatisation
Pour nettoyer plusieurs fichiers :
```cmd
for %f in (*.csv) do python csv_cleaner_agent.py %f
```

Bon nettoyage ! 🚀
