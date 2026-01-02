# 🚀 Guide de Démarrage Rapide

## Installation Express (5 minutes)

### 1️⃣ Vérifiez Python
Ouvrez le terminal (cmd) et tapez :
```cmd
python --version
```
✅ Si vous voyez "Python 3.x.x" → OK
❌ Si erreur → Installez Python depuis python.org

### 2️⃣ Obtenez votre clé API Gemini
1. Allez sur : https://makersuite.google.com/app/apikey
2. Connectez-vous avec Google
3. Cliquez "Create API Key"
4. Copiez la clé (format: AIzaSy...)

### 3️⃣ Installez les dépendances
Dans le dossier du projet :
```cmd
pip install -r requirements.txt
```

### 4️⃣ Configurez votre clé API
```cmd
set GEMINI_API_KEY=VOTRE_CLE_ICI
```

### 5️⃣ Testez !
```cmd
python csv_cleaner_agent.py exemple_test.csv
```

## Utilisation Quotidienne

### Méthode 1 : Ligne de commande
```cmd
python csv_cleaner_agent.py mon_fichier.csv
```

### Méthode 2 : Script batch (plus simple)
```cmd
nettoyer.bat mon_fichier.csv
```

### Méthode 3 : Glisser-déposer (Windows)
1. Créez un raccourci de `nettoyer.bat` sur le bureau
2. Glissez votre fichier CSV sur le raccourci
3. C'est tout ! 🎉

## Ce que fait l'agent

```
📂 Lecture du CSV
    ↓
🔍 Analyse des anomalies
    ↓
📋 Affichage des problèmes trouvés
    ↓
💡 Proposition de corrections
    ↓
❓ Demande de confirmation (VOUS décidez)
    ↓
🔧 Application des corrections
    ↓
✅ Création du fichier *_cleaned.csv
```

## Exemple de session

```
C:\Users\Vous\csv-cleaner> python csv_cleaner_agent.py donnees.csv

🤖 AGENT DE NETTOYAGE CSV AVEC GEMINI PRO
============================================================

📂 Lecture du fichier : donnees.csv
🔍 Analyse des anomalies en cours...

============================================================
📋 ANOMALIES DÉTECTÉES
============================================================

🔴 Anomalie 1 [HAUTE]
   Type : doublons
   Description : 2 lignes identiques détectées
   Colonnes : toutes
   Lignes affectées : 2

🟡 Anomalie 2 [MOYENNE]
   Type : valeurs_manquantes
   Description : Valeurs manquantes dans la colonne 'email'
   Colonnes : email
   Lignes affectées : 3

🟢 Anomalie 3 [FAIBLE]
   Type : espaces_inutiles
   Description : Espaces en début/fin de cellules
   Colonnes : nom, prenom
   Lignes affectées : 5

============================================================
🔧 CORRECTIONS PROPOSÉES
============================================================

✏️  Correction 1
   Cible : Doublons détectés
   Action : Supprimer les lignes en double
   Impact : 2 lignes seront supprimées

✏️  Correction 2
   Cible : Valeurs manquantes dans email
   Action : Remplir avec une chaîne vide
   Impact : 3 cellules affectées

✏️  Correction 3
   Cible : Espaces inutiles
   Action : Supprimer les espaces en début/fin
   Impact : 5 lignes affectées

============================================================

❓ Voulez-vous appliquer ces corrections ? (oui/non) : oui

============================================================
🚀 APPLICATION DES CORRECTIONS
============================================================

⚙️  Application : Supprimer les lignes en double
   ✓ 2 doublons supprimés

⚙️  Application : Remplir avec une chaîne vide
   ✓ Valeurs manquantes remplies

⚙️  Application : Supprimer les espaces en début/fin
   ✓ Espaces supprimés dans 2 colonnes

============================================================
✅ NETTOYAGE TERMINÉ
============================================================

📁 Fichier original : donnees.csv
📁 Fichier nettoyé : donnees_cleaned.csv

📊 Statistiques :
   Lignes avant : 14
   Lignes après : 12
   Différence : 2 lignes

✨ Le fichier nettoyé a été sauvegardé avec succès !
```

## Problèmes Fréquents

### "python n'est pas reconnu"
➡️ Ajoutez Python au PATH ou réinstallez Python

### "GEMINI_API_KEY n'est pas définie"
➡️ Exécutez : `set GEMINI_API_KEY=votre_cle`

### "No module named pandas"
➡️ Exécutez : `pip install pandas google-generativeai`

### L'agent ne détecte rien
➡️ Votre CSV est peut-être déjà propre ! Testez avec `exemple_test.csv`

## Astuces Pro

### 💾 Sauvegardez vos fichiers
Faites toujours une copie avant de nettoyer :
```cmd
copy donnees.csv donnees_backup.csv
```

### 🔄 Nettoyage par lot
Pour nettoyer tous les CSV d'un dossier :
```cmd
for %f in (*.csv) do python csv_cleaner_agent.py %f
```

### 📝 Vérifiez toujours
Ouvrez le fichier `*_cleaned.csv` dans Excel/LibreOffice avant de supprimer l'original

### 🎯 Personnalisez
Modifiez `csv_cleaner_agent.py` pour ajouter vos propres règles

## Vous êtes prêt ! 🎉

Commencez par tester avec `exemple_test.csv` fourni, puis utilisez vos vrais fichiers.

Bon nettoyage ! 🚀
