# Sécurité, confidentialité et validation humaine

## Secrets et authentification

| Règle | Implémentation |
|-------|----------------|
| OAuth uniquement | Pas de mot de passe Gmail en clair |
| Tokens protégés | Stockage local sécurisé (à définir Phase 3) |
| Exclusion Git | `.gitignore` : tokens, secrets, oauth/, credentials/ |
| Révocation | Procédure par compte documentée à l’implémentation |

## Git et dépôt

- `.gitignore` strict (voir racine du projet)
- Pas de vrais comptes, mails, `.eml` réels
- Pas de rapports avec données personnelles versionnés
- Pas de logs sensibles commités
- Config réelle : `*.local.yaml` uniquement en local

## Actions sensibles (validation humaine obligatoire)

- Suppression définitive (hors scope V1 par défaut)
- Envoi de mail
- Désabonnement newsletter
- Changement filtre serveur Gmail non documenté
- Extraction massive (seuil à définir)
- Suppression de pièces jointes côté serveur
- Modification directe de PersonalRadar (interdit)

## Validation humaine — cas métier

- Mails `SUSPICIEUX_A_VALIDER`
- Ambiguïté financière ou administrative
- Nouvelle règle destructive (après dry-run)
- Désabonnement newsletter
- Envoi tout courrier préparé par Hermès

## Journalisation

Chaque entrée de journal devrait inclure :

| Champ | Description |
|-------|-------------|
| `action` | Type d’opération |
| `timestamp` | Date/heure UTC |
| `account_id` | Compte Gmail |
| `message_id` | Id Gmail si applicable |
| `result` | succès / échec / skipped |
| `confidence` | Si classification |
| `mode` | dry-run / safe-run / apply-run |
| `document_path` | Si extraction |

## Restauration

1. Privilégier **quarantaine** / label avant trash
2. **Trash** Gmail avant suppression définitive
3. **Pas de delete définitif en V1** par défaut

## Pièces jointes dangereuses

Ne **jamais** ouvrir automatiquement :

- Exécutables : `.exe`, `.bat`, `.cmd`, `.ps1`, `.js`, `.vbs`, `.scr`
- Archives suspectes (double extension, expéditeur inconnu)
- Documents macro suspects (Office avec macros non attendues)

En cas de doute → `SUSPICIEUX_A_VALIDER`, pas d’extraction du binaire.

## Documents liés

- [OAuth](04_GMAIL_OAUTH_IMAP_API_MODEL.md)
- [Rétention](07_RETENTION_AND_DELETION_RULES.md)
- [Hermès](10_HERMES_OPERATING_PROTOCOL.md)
- [Tests](14_TEST_AND_VALIDATION_PLAN.md)
