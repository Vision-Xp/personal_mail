# Taxonomie des catégories

Les catégories se matérialisent comme **labels Gmail** (préfixe cohérent recommandé, ex. `PM/` ou nom stable documenté). Une catégorie = un label principal ; les sous-catégories = labels enfants ou convention `CATEGORIE/SousCat`.

## Catégories principales

| Label | Rôle |
|-------|------|
| `00_INBOX_REVIEW` | À classer manuellement ou confiance insuffisante |
| `ADMINISTRATIF` | Impôts, CAF, CPAM, employeur, etc. |
| `BANQUE` | Établissements bancaires et néobanques |
| `ASSURANCES` | Auto, habitation, santé |
| `ENERGIE` | Fournisseurs énergie |
| `REVENUS` | Salaire, remboursements, ventes |
| `SORTIES_ARGENT` | Factures, abonnements, achats, frais |
| `CONTRATS` | Contrats et avenants |
| `ACHATS_GARANTIES` | Preuves, factures achat, garanties, SAV |
| `ABONNEMENTS` | Abonnements récurrents |
| `PROMOTIONS_UTILES` | Offres à valeur réelle |
| `PROMOTIONS_INUTILES` | Bruit commercial |
| `NEWSLETTERS` | Flux newsletter |
| `RESEAUX_SOCIAUX` | Notifications sociales (rétention courte) |
| `SCAM_AVERE` | Phishing/scam confirmé |
| `SUSPICIEUX_A_VALIDER` | Incertitude — validation humaine |
| `DOCUMENTS_EXTRAITS` | Mail traité, document dans PersonalRadar |
| `A_REPONDRE` | Réponse attendue |
| `A_TRAITER_PERSONAL_RADAR` | En attente traitement documentaire |

## Sous-catégories

### ADMINISTRATIF

- Impôts
- CPAM
- CAF
- France Travail
- Employeur
- Santé
- Rendez-vous
- Confirmations

### BANQUE

- Crédit Agricole
- Revolut
- Fortuneo
- Trade Republic

### ASSURANCES

- Auto
- Habitation
- Santé

### ENERGIE

- ENGIE
- Primeo
- Autres

### REVENUS

- Salaire
- Remboursements
- Ventes
- Autres entrées

### SORTIES_ARGENT

- Factures
- Abonnements
- Achats
- Frais bancaires
- Paiements récurrents

### ACHATS_GARANTIES

- Preuves d’achat
- Factures
- Garanties
- Retours
- SAV

### NEWSLETTERS

- À garder
- À revoir
- Désabonnement proposé

## Règles anti-usine-à-gaz

1. **Une sous-catégorie** seulement si volume ou intérêt réel (ex. organisme bancaire fréquent).
2. **Organisme important** = sous-catégorie possible ; organisme rare = rester dans la catégorie parente.
3. **Catégorie stable** avant granularité excessive — mieux vaut `BANQUE` bien rempli que 40 labels vides.
4. **Labels techniques** préfixés clairement (`PM/`, `SYS/`) pour distinguer métier et technique.
5. **Ne pas multiplier les labels** pour un seul mail sauf utilité claire (ex. `BANQUE` + `A_REPONDRE` si les deux sont vrais).

## Documents liés

- [Classification](06_CLASSIFICATION_RULES.md)
- [Rétention](07_RETENTION_AND_DELETION_RULES.md)
- [config/category_rules.example.yaml](../config/category_rules.example.yaml)
