# 📋 Liste des Anomalies dans exemple_test_complet.csv

## 🎯 Fichier de Test Complet

Ce fichier contient **25 lignes** avec de **nombreuses anomalies** pour tester tous les aspects de l'agent.

---

## 🔴 ANOMALIES CRITIQUES (Haute priorité)

### Doublons
- **Ligne 1 et 3** : Dupont Jean - doublon complet (même numéro employé EMP001)
- **Ligne 2 et 11** : Martin Sophie - doublon complet (même numéro employé EMP002)

### Âges invalides
- **Ligne 5** : age = `999` (Petit Marie)
- **Ligne 8** : age = `-5` (Moreau Thomas)
- **Ligne 15** : age = `150` (Blanc Pierre)
- **Ligne 19** : age = `-1` (Lemoine Marc)

### Salaires invalides
- **Ligne 15** : salaire = `-5000` (Blanc Pierre) - salaire négatif
- **Ligne 21** : salaire = `999999` (Faure Thomas) - salaire aberrant (presque 1 million)

### Heures de travail aberrantes
- **Ligne 15** : heures_semaine = `999` (Blanc Pierre)
- **Ligne 19** : heures_semaine = `0` (Lemoine Marc)
- **Ligne 21** : heures_semaine = `80` (Faure Thomas) - trop élevé
- **Ligne 25** : heures_semaine = `-10` (Girard Paul) - négatif

---

## 🟡 ANOMALIES MOYENNES

### Codes postaux invalides
- **Ligne 6** : code_postal = `6000` (Nice) - devrait être `06000`
- **Ligne 17** : code_postal = `750` (Paris) - incomplet
- **Ligne 18** : code_postal = `69999999` (Lyon) - trop long

### Téléphones invalides
- **Ligne 13** : telephone = `1234567890` (Fournier) - pas au bon format
- **Ligne 16** : telephone = `06` (Noir Sophie) - incomplet
- **Ligne 19** : telephone = `9999999999` (Lemoine Marc) - format invalide

### Formats de dates incohérents
- **Ligne 4** : date = `15/06/2020` (format jour/mois/année)
- **Ligne 9** : date = `01-04-2022` (format jour-mois-année avec tirets)
- **Ligne 24** : date = `99/99/9999` (Chevalier Emma) - date invalide

### Numéro employé manquant
- **Ligne 16** : numero_employe vide (Noir Sophie)

---

## ⚪ VALEURS MANQUANTES (Doivent rester vides)

### Colonnes avec valeurs manquantes
- **Ligne 4** : prenom vide (Bernard)
- **Ligne 5** : salaire vide (Petit Marie)
- **Ligne 6** : nom vide (Lucas)
- **Ligne 7** : ville vide (Rousseau Emma)
- **Ligne 20** : telephone vide (Robert Julie)
- **Ligne 22** : email vide (Lefebvre Marie)
- **Ligne 23** : code_postal vide (Garnier Luc)

---

## 🟢 ANOMALIES MINEURES (Faible priorité)

### Espaces inutiles
- **Ligne 2 et 11** : prenom = `"  Sophie  "` (espaces avant/après)

### Formats de téléphone variés (tous valides mais incohérents)
- `0612345678` (standard)
- `06 87 65 43 21` (avec espaces)
- `+33 6 12 34 56 78` (international avec espaces)
- `06.11.22.33.44` (avec points)
- `06-12-34-56-78` (avec tirets)
- `+33612345678` (international sans espaces)

---

## 📊 Résumé des Anomalies

| Type | Nombre | Colonnes affectées |
|------|--------|-------------------|
| **Doublons** | 2 lignes | Toutes |
| **Âges invalides** | 4 | age |
| **Salaires invalides** | 2 | salaire |
| **Heures aberrantes** | 4 | heures_semaine |
| **Codes postaux** | 3 | code_postal |
| **Téléphones** | 3 | telephone |
| **Dates invalides** | 3 | date_embauche |
| **Espaces** | 2 | prenom |
| **Valeurs manquantes** | 7 | Diverses |

**Total : ~30 anomalies**

---

## 🎯 Ce que l'agent devrait proposer

### À REMPLACER par "n/a"
- ✅ age = 999, -5, 150, -1
- ✅ salaire = -5000, 999999
- ✅ heures_semaine = 999, 0, 80, -10
- ✅ code_postal = 6000, 750, 69999999
- ✅ telephone = 06, 1234567890, 9999999999
- ✅ date = 99/99/9999

### À SUPPRIMER
- ✅ Lignes 1 et 3 (doublon)
- ✅ Lignes 2 et 11 (doublon)

### À NETTOYER
- ✅ Espaces autour de "Sophie"

### À NE PAS TOUCHER
- ❌ Valeurs manquantes (prenom, salaire, ville, telephone, email, code_postal vides)

---

## 🚀 Utilisation

```cmd
python agent_csv.py exemple_test_complet.csv
```

L'agent devrait :
1. Détecter toutes ces anomalies
2. Proposer des corrections appropriées
3. Demander confirmation pour chaque type
4. Créer un fichier nettoyé dans `Cleaned/`

---

## ✨ Résultat Attendu

- **23 lignes** (2 doublons supprimés)
- **~20 valeurs remplacées par "n/a"**
- **Espaces nettoyés**
- **Valeurs manquantes préservées**

**Testez et voyez si l'agent détecte tout ! 🎉**
