# Protocole d’exploitation Hermès

## Rôle d’Hermès

Hermès est l’**opérateur** qui pilote `personal_mail` et coordonne validation humaine, rapports et intégration documentaire.

### Hermès doit pouvoir

| Capacité | Description |
|----------|-------------|
| Installer prérequis | Rust toolchain (futur), dépendances, structure config locale |
| Configurer le projet | Copier `*.example.yaml` → `*.local.yaml` (non commité) |
| Demander autorisations | OAuth par compte — jamais mot de passe clair |
| Lancer dry-run | Simulations sans mutation destructive |
| Lire rapports | Classification, cleanup, extraction, erreurs |
| Proposer règles | Suggérer ajouts à `category_rules` / `retention_rules` |
| Appliquer règles validées | Mode apply après validation Damien |
| Extraire documents | Vers `personal_radar\documents` |
| Lancer audits | Newsletters, stockage, règles obsolètes |
| Préparer mails | Brouillons complets — pas d’envoi auto sensible |
| Produire rapports validation | GO / GO limité / NO GO |
| Communiquer avec PR | Via fichiers + manifeste JSONL |

## Informations qu’Hermès peut demander

- Liste des comptes Gmail à connecter
- Autorisation OAuth (navigateur / device flow)
- Choix ou confirmation client mail (post Phase 1)
- Validation des règles destructives et exceptions
- Chemins locaux (documents, rapports)
- Confirmation avant commit/push si opération Git
- Confirmation avant toute suppression définitive future

## Interdictions

- Ne **pas** demander de mot de passe Gmail en clair
- Ne **pas** envoyer de mail sans validation humaine
- Ne **pas** supprimer définitivement hors règles validées
- Ne **pas** modifier PersonalRadar hors protocole documentaire
- Ne **pas** committer secrets, tokens, mails réels
- Ne **pas** ouvrir automatiquement pièces jointes dangereuses

## Modes opératoires

| Mode | Effet |
|------|--------|
| `dry-run` | Analyse uniquement — rapports |
| `safe-run` | Labels + extraction non destructive |
| `apply-run` | Actions validées (trash, etc.) |
| `audit-run` | Newsletters, règles, stockage Gmail |
| `compose-run` | Préparation brouillons — pas d’envoi |

Voir [config/hermes_permissions.example.yaml](../config/hermes_permissions.example.yaml).

## Types de rapports

| Rapport | Contenu typique |
|---------|-----------------|
| Scan | Volume, comptes, curseurs |
| Classification | Catégories, scores |
| Suppression potentielle | Dry-run delete/trash |
| Extraction | Fichiers, hash, erreurs |
| Validation | Checklist humaine |
| Newsletter | Émetteurs, recommandations |
| Erreurs | API, OAuth, I/O |

Stockage : [reports/](../reports/) — fichiers sensibles non versionnés.

## Documents liés

- [Sécurité](13_SECURITY_PRIVACY_AND_HUMAN_VALIDATION.md)
- [Compose workflow](12_REPLY_AND_COMPOSE_WORKFLOW.md)
- [Tests](14_TEST_AND_VALIDATION_PLAN.md)
