# 🚀 Guide de Démarrage Rapide

## Installation Express (5 minutes)

### 1️⃣ Vérifiez Python
Ouvrez le terminal (cmd) et tapez :
```cmd
python --version
```
✅ Si vous voyez "Python 3.x.x" → OK
❌ Si erreur → Installez Python depuis python.org

### 2️⃣ Obtenez votre clé API Mistral
1. Allez sur : https://console.mistral.ai/
2. Créez un compte (gratuit)
3. Cliquez sur "API Keys" → "Create new key"
4. Copiez la clé (format: xxx...)

### 3️⃣ Installez les dépendances
Dans le dossier du projet :
```cmd
pip install -r requirements.txt
```

### 4️⃣ Configurez votre clé API
```cmd
set MISTRAL_API_KEY=VOTRE_CLE_ICI
```

### 5️⃣ Organisez vos fichiers
Créez la structure suivante :
```
SmartData_Cleaner/
├── agent_csv.py
├── operations.py
├── requirements.txt
└── Raw/                    ← Placez vos fichiers CSV ici
    └── exemple_test.csv
```

### 6️⃣ Testez !
```cmd
python agent_csv.py exemple_test.csv
```

## Utilisation Quotidienne

### Méthode Simple (Recommandée)
```cmd
# 1. Placez votre fichier dans Raw/
Raw/mon_fichier.csv

# 2. Lancez avec juste le nom
python agent_csv.py mon_fichier.csv

# 3. Le fichier nettoyé sera dans Cleaned/
Cleaned/mon_fichier_cleaned_2026-01-02_14-30-00.csv
```

### Méthode Alternative (Chemin complet)
```cmd
python agent_csv.py C:/data/mon_fichier.csv
```

### Structure Automatique
L'agent crée automatiquement cette organisation :
```
votre-projet/
├── agent_csv.py
├── operations.py
├── Raw/                    ← Fichiers sources
│   ├── exemple_test.csv
│   └── clients.csv
└── Cleaned/                ← Fichiers nettoyés
    ├── exemple_test_cleaned_2026-01-02_14-30-00.csv
    └── clients_cleaned_2026-01-02_15-15-30.csv
```

## Ce que fait l'agent

```
📂 Lecture du CSV (depuis Raw/)
    ↓
🔍 Analyse intelligente avec Mistral AI
    ↓
📋 Détection de 13+ types d'anomalies
    ↓
💡 Proposition de 38+ opérations de nettoyage
    ↓
❓ Demande de confirmation (VOUS décidez)
    ↓
🔧 Application des corrections
    ↓
✅ Sauvegarde dans Cleaned/ avec timestamp
```

## Types d'Anomalies Détectées

### 🔴 Haute Priorité
- ✅ **Doublons** - Lignes identiques
- ✅ **Valeurs aberrantes** - Outliers statistiques (999, 999999)
- ✅ **Types incorrects** - Code postal en nombre
- ✅ **Emails invalides** - Sans @ ou extension
- ✅ **Codes postaux invalides** - Longueur ≠ 5 chiffres
- ✅ **Téléphones invalides** - Formats incorrects
- ✅ **IBAN étrangers** - Non français (DE, GB, etc.)
- ✅ **SIRET invalides** - Longueur ≠ 14 chiffres

### 🟡 Moyenne Priorité
- ✅ **Espaces inutiles** - Début/fin de cellules
- ✅ **Accents** - Caractères accentués (é, è, ü, etc.)
- ✅ **Dates incohérentes** - Futures ou < 1900
- ✅ **Formats de dates variés** - DD/MM/YYYY, YYYY-MM-DD
- ✅ **Téléphones variés** - Espaces, points, tirets, +33
- ✅ **Valeurs manquantes** - Cellules vides (optionnel)

### 🟢 Faible Priorité
- ✅ **Noms de colonnes** - Majuscules, espaces
- ✅ **Colonnes vides** - 100% vides

## Exemple de session

```
C:\projet> python agent_csv.py exemple_test.csv

======================================================================
🤖 AGENT IA DE NETTOYAGE CSV (avec Mistral AI + operations)
======================================================================

📂 Fichier trouvé dans : C:\projet\Raw
📂 Lecture du fichier : Raw\exemple_test.csv
✅ 25 lignes, 15 colonnes chargées

🔍 Analyse des anomalies avec Mistral AI...

======================================================================
🔧 CORRECTIONS PROPOSÉES
======================================================================

======================================================================
ANOMALIE 1/13
======================================================================

🔴 Type : colonnes_numeriques
📝 Description : Colonnes à forcer en texte
📊 Colonnes : code_postal, telephone, numero_employe
⚡ Impact estimé : 3 colonnes forcées en texte

🔧 Opération proposée : forcer_type_texte
⚙️  Paramètres :
   • colonnes = ['code_postal', 'telephone', 'numero_employe']

──────────────────────────────────────────────────────────────────────
❓ Appliquer cette correction ? (o=oui / n=non / q=quitter) : o

⚙️  Exécution en cours...
✅ Opération réussie : 3

======================================================================
ANOMALIE 2/13
======================================================================

🔴 Type : accents_caracteres_speciaux
📝 Description : Accents détectés dans nom, prenom, ville
📊 Colonnes : nom, prenom, ville
⚡ Impact estimé : 5 lignes affectées

🔧 Opération proposée : supprimer_accents
⚙️  Paramètres :
   • colonnes = ['nom', 'prenom', 'ville']

──────────────────────────────────────────────────────────────────────
❓ Appliquer cette correction ? (o=oui / n=non / q=quitter) : o

⚙️  Exécution en cours...
✅ Opération réussie : Lefèvre → Lefevre, Müller → Muller

[... autres anomalies ...]

======================================================================
📊 RÉSUMÉ FINAL
======================================================================

📈 Statistiques :
   • Lignes avant : 25
   • Lignes après : 25
   • Différence : 0 lignes
   • Colonnes avant : 15
   • Colonnes après : 15

🔧 Opérations effectuées : 13
   1. forcer_type_texte → 3 colonnes
   2. supprimer_accents → 5 valeurs
   3. valider_codes_postaux → 7 codes postaux
   4. normaliser_telephones → 9 téléphones
   5. detecter_incoherences_dates → 3 dates
   6. standardiser_format_date → 22 dates
   7. remplacer_emails_invalides → 6 emails
   8. verifier_format_iban → 6 IBAN
   9. verifier_format_siret → 4 SIRET
   10. remplacer_valeurs_invalides (age) → 8 valeurs
   11. remplacer_valeurs_invalides (heures) → 4 valeurs
   12. remplacer_valeurs_aberrantes (salaire) → 4 valeurs
   13. normaliser_noms_colonnes → OK

======================================================================
💾 Sauvegarder le fichier nettoyé ? (oui/non) : oui

🧹 Nettoyage final : remplacement de 'nan' par cellules vides...

======================================================================
✅ FICHIER SAUVEGARDÉ
======================================================================

📁 Fichier original : Raw\exemple_test.csv
📁 Fichier nettoyé : Cleaned\exemple_test_cleaned_2026-01-02_14-30-00.csv
📁 Dossier : C:\projet\Cleaned
🕐 Timestamp : 2026-01-02_14-30-00

✨ Nettoyage terminé avec succès !
```

## 38+ Opérations Disponibles

### Nettoyage de Base
1. `supprimer_doublons` - Supprime lignes identiques
2. `nettoyer_espaces` - Nettoie espaces début/fin
3. `supprimer_lignes_vides` - Supprime lignes vides
4. `supprimer_colonnes_vides` - Supprime colonnes vides

### Normalisation de Texte
5. `supprimer_accents` - Enlève é, è, ü, etc.
6. `capitaliser_texte` - Capitalise (Title, UPPER, lower)
7. `normaliser_noms_colonnes` - snake_case, minuscules

### Validation de Données
8. `valider_codes_postaux` - Vérifie 5 chiffres
9. `normaliser_telephones` - Format uniforme 06XXXXXXXX
10. `remplacer_emails_invalides` - Vérifie @ et extension
11. `verifier_format_iban` - Uniquement IBAN français
12. `verifier_format_siret` - 14 chiffres obligatoires

### Dates
13. `standardiser_format_date` - Format YYYY-MM-DD
14. `detecter_incoherences_dates` - Futures, < 1900

### Valeurs Numériques
15. `remplacer_valeurs_invalides` - Hors plage min/max
16. `remplacer_valeurs_aberrantes` - Outliers + codes (999)
17. `detecter_valeurs_negatives` - Valeurs < 0
18. `arrondir_decimales` - Précision décimale

### Transformation
19. `forcer_type_texte` - Préserve 0 initiaux
20. `convertir_type_colonne` - int, float, str, date
21. `remplacer_valeurs` - Remplace A par B
22. `remplir_valeurs_manquantes` - Constante, moyenne, médiane

### Analyse
23. `detecter_doublons_approximatifs` - Fuzzy matching
24. `calculer_statistiques` - Stats descriptives
25. `compter_valeurs_uniques` - Cardinalité

### Filtrage
26. `filtrer_lignes_condition` - Filtre selon règle
27. `supprimer_colonne` - Supprime une colonne

### Et 11+ autres opérations...

## Problèmes Fréquents

### "python n'est pas reconnu"
➡️ Ajoutez Python au PATH ou réinstallez Python avec "Add to PATH"

### "MISTRAL_API_KEY n'est pas définie"
➡️ Exécutez : `set MISTRAL_API_KEY=votre_cle`
➡️ Pour rendre permanent : Panneau de configuration → Variables d'environnement

### "No module named pandas"
➡️ Exécutez : `pip install -r requirements.txt`

### "No module named operations"
➡️ Vérifiez que `operations.py` est dans le même dossier que `agent_csv.py`

### L'agent ne détecte rien
➡️ Votre CSV est peut-être déjà propre ! Testez avec `exemple_test.csv`

### Erreur de parsing JSON
➡️ L'IA a mal formaté sa réponse, relancez (rare avec Mistral)

### Le dossier Raw/ n'existe pas
➡️ L'agent le crée automatiquement au premier lancement

## Astuces Pro

### 💾 Organisation Automatique
L'agent gère tout seul :
- Création de `Raw/` si inexistant
- Création de `Cleaned/` si inexistant
- Timestamps uniques (pas d'écrasement)

### 🔄 Nettoyage par Lot
Pour nettoyer tous les CSV du dossier Raw :
```cmd
cd Raw
for %f in (*.csv) do python ..\agent_csv.py %f
```

### 📝 Vérifiez Toujours
Comparez original et nettoyé dans Excel/LibreOffice :
```
Raw/clients.csv         ← Original (préservé)
Cleaned/clients_cleaned_xxx.csv  ← Nettoyé (à vérifier)
```

### 🎯 Score de Qualité
L'agent vise **90-96%** de qualité automatique :
- ✅ Accents : 100%
- ✅ Emails : 100%
- ✅ Âges : 100%
- ✅ Dates : 92%
- ✅ Téléphones : 78%
- ✅ Codes postaux : 86%

### 🔧 Personnalisation
Modifiez le prompt dans `agent_csv.py` (ligne 90+) pour :
- Ajouter vos propres règles métier
- Changer les seuils de détection
- Prioriser certaines anomalies

## Avantages de l'Organisation Raw/Cleaned

✅ **Clarté** - Sources séparées des résultats
✅ **Sécurité** - Originaux toujours préservés
✅ **Traçabilité** - Timestamps sur chaque nettoyage
✅ **Professionnalisme** - Structure standard
✅ **Simplicité** - Une seule commande

## Formats Supportés

### Encodages
- ✅ UTF-8 (priorité)
- ✅ Latin-1 (fallback)
- ✅ CP1252 (fallback Windows)

### Séparateurs
- ✅ Virgule (,) - Standard
- ✅ Point-virgule (;) - À configurer dans pandas

### Formats de Dates Reconnus
- ✅ DD/MM/YYYY (15/03/2020)
- ✅ DD-MM-YYYY (15-03-2020)
- ✅ YYYY-MM-DD (2020-03-15)
- ✅ YYYY/MM/DD (2020/03/15)

**Format de sortie :** Toujours `YYYY-MM-DD`

## Vous êtes prêt ! 🎉

### Premier Test
```cmd
# 1. Placez exemple_test.csv dans Raw/
# 2. Lancez
python agent_csv.py exemple_test.csv
# 3. Vérifiez le résultat dans Cleaned/
```

### Utilisation Réelle
```cmd
# 1. Copiez vos fichiers dans Raw/
copy C:\data\*.csv Raw\

# 2. Nettoyez-les un par un
python agent_csv.py clients.csv
python agent_csv.py factures.csv
python agent_csv.py stocks.csv

# 3. Tous les résultats dans Cleaned/ !
```

Bon nettoyage ! 🚀
