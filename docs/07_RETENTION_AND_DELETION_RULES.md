# Rétention et suppression

## Suppressions autorisées (après validation humaine de la règle)

| Type | Condition |
|------|-----------|
| Promotions inintéressantes | Catégorie `PROMOTIONS_INUTILES`, confiance élevée |
| Scams avérés | `SCAM_AVERE`, confiance ≥ 0.95, règle validée |
| Réseaux sociaux > 30 jours | Hors exceptions documentées |
| Doublons sans valeur | Après extraction documentaire validée et hash identique |

## Quarantaine (`SUSPICIEUX_A_VALIDER`)

Cas typiques :

- Suspicion phishing non certaine
- Fausse facture possible
- Pièce jointe douteuse
- Expéditeur ambigu (homographe)
- Domaine proche d’un organisme connu
- Urgence artificielle sans certitude

**Pas de suppression automatique** — revue humaine obligatoire.

## Conservation longue durée

Conserver (ne pas supprimer automatiquement) :

- Administratif, contrats, factures
- Preuves d’achat, garanties
- Paiements, revenus, remboursements
- Rendez-vous, échéances, confirmations
- Informations bancaires et assurance
- Santé, employeur

## Réseaux sociaux

| Règle | Détail |
|-------|--------|
| Durée max | 30 jours |
| Suppression auto | Au-delà de 30 jours **si** règle validée + dry-run passé |
| Exceptions | Booking musical, opportunité musicale/pro, Dryard/Uncloned, alerte sécurité compte, preuve utile |

## Newsletters

- **Audit** 1 à 2 fois par an
- Lister les organismes émetteurs
- Proposer : garder / revoir / désabonner
- **Pas de désabonnement automatique en V1** sans validation humaine

## Dry-run (obligatoire pour nouvelles règles destructives)

1. Exécuter la règle en mode simulation
2. Produire un rapport listant les messages qui **auraient** été supprimés/déplacés
3. Revue humaine
4. Passage en mode `apply` uniquement après validation explicite

Rapports dans [reports/cleanup/](../reports/cleanup/) — non versionnés si données perso.

## Documents liés

- [Classification](06_CLASSIFICATION_RULES.md)
- [Sécurité](13_SECURITY_PRIVACY_AND_HUMAN_VALIDATION.md)
- [config/retention_rules.example.yaml](../config/retention_rules.example.yaml)
