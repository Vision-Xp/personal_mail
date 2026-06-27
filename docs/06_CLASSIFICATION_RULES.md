# Règles de classification

## Signaux utilisés

| Signal | Exemples |
|--------|----------|
| Expéditeur | `noreply@revolut.com` |
| Domaine | `credit-agricole.fr` |
| Sujet | « Votre facture », « Rappel échéance » |
| Corps | Montants, IBAN, références contrat |
| Pièces jointes | PDF facture, image preuve achat |
| Mots-clés | facture, échéance, garantie, résiliation |
| Montants | `123,45 EUR`, `$`, patterns devise |
| Dates | échéance, rendez-vous |
| IBAN / RIB | FR76… |
| Numéro de contrat | patterns par organisme |
| Commande | n° commande, tracking |
| Facture | n° facture, TVA |
| Preuve d’achat | reçu, ticket |
| Confirmation | RDV, réservation |
| Lien suspect | domaine typosquatté, URL raccourcie inconnue |
| Pièce jointe suspecte | `.exe`, macro, archive inattendue |

## Niveaux de confiance

| Confiance | Comportement |
|-----------|--------------|
| **≥ 0.95** | Action auto possible si non sensible **ou** règle déjà validée humainement |
| **0.80 – 0.95** | Classement auto OK ; **pas** de suppression définitive |
| **0.60 – 0.80** | `00_INBOX_REVIEW` ou `SUSPICIEUX_A_VALIDER` selon risque |
| **< 0.60** | Non classé — revue humaine |

## Cas typiques

| Cas | Catégorie cible | Notes |
|-----|-----------------|-------|
| Crédit Agricole | BANQUE / Crédit Agricole | Relevés, virements |
| Revolut | BANQUE / Revolut | Transactions |
| Fortuneo | BANQUE / Fortuneo | |
| Trade Republic | BANQUE / Trade Republic | |
| ENGIE | ENERGIE / ENGIE | Factures |
| Assurance auto | ASSURANCES / Auto | |
| Assurance habitation | ASSURANCES / Habitation | |
| Achats e-commerce | ACHATS_GARANTIES | Extraction PDF |
| Confirmation RDV | ADMINISTRATIF / Rendez-vous | |
| Newsletter | NEWSLETTERS | Sous-type à revoir |
| Réseau social | RESEAUX_SOCIAUX | Rétention 30j |
| Promo utile | PROMOTIONS_UTILES | Critères ci-dessous |
| Promo inutile | PROMOTIONS_INUTILES | Delete après validation |
| Scam avéré | SCAM_AVERE | Quarantaine ou trash validé |
| Mail suspicieux | SUSPICIEUX_A_VALIDER | Jamais delete auto |

## Promotions utiles vs inutiles

### Promotion **utile** si liée à

- Économie réelle ou opportunité concrète
- Situation financière ou administrative actuelle
- Banque, assurance, énergie, télécom
- Outils IA, musique, matériel utile
- Abonnement **existant** (renégociation, résiliation)
- Résiliation ou renégociation possible

### Promotion **inutile** si

- Hors sujet ou marque jamais utilisée
- Répétitive / générique (« -70% sur tout »)
- Aucun rapport avec la situation actuelle
- Incitation sans valeur / spam commercial évident

## Documents liés

- [Taxonomie](05_CATEGORY_TAXONOMY.md)
- [Rétention](07_RETENTION_AND_DELETION_RULES.md)
- [config/category_rules.example.yaml](../config/category_rules.example.yaml)
