# Gmail — OAuth, IMAP et API

## Modèle Gmail (entités)

| Entité | Usage dans personal_mail |
|--------|--------------------------|
| Messages | Contenu, métadonnées, pièces jointes |
| Threads | Regroupement conversationnel |
| Labels | Organisation canonique (équivalent dossiers) |
| Read/unread | État de lecture (pas forcément modifié auto en V1) |
| Trash | Corbeille avant suppression définitive |
| Spam | Flux spam Gmail |
| Attachments | Extraction documentaire |
| Search queries | Dry-run, batch, règles de rétention |

## OAuth

| Principe | Détail |
|----------|--------|
| Pas de mot de passe en clair | Uniquement OAuth 2.0 par compte |
| Tokens protégés | Stockage local sécurisé à définir (Phase 3+) |
| Scopes minimaux | Lecture, labels, modification messages — pas plus que nécessaire |
| Révocation | Possible côté Google et localement |
| Séparation par compte | Un token store logique par `account_id` |
| Git | Tokens exclus (.gitignore) |

## IMAP

- **Utile pour Thunderbird** : synchronisation des labels et messages vers le client humain.
- **Utile éventuellement** pour compatibilité ou debug.
- **Pas la voie principale** pour l’automatisation `personal_mail` — préférer Gmail API pour batch, labels, recherche et journaux cohérents.

## Gmail API — voie préférée

| Cas d’usage | API |
|-------------|-----|
| Lecture métadonnées | `users.messages.get` (format metadata) |
| Recherche | `users.messages.list` + query |
| Labels | `users.labels` create/list, `users.messages.modify` |
| Classification | modify labels + rapports |
| Pièces jointes | `attachments.get` |
| Trash | `trash` / `modify` remove INBOX |
| Batch | `batch` pour perf multi-messages |
| Journaux d’action | Côté personal_mail (pas API Gmail native) |

## Actions destructives — échelle de prudence

```
1. dry-run     → rapport uniquement
2. quarantaine → label SUSPICIEUX / dossier dédié
3. trash       → corbeille Gmail
4. delete      → suppression définitive (hors V1 par défaut, validation explicite future)
```

- Nouvelle règle destructive : **toujours** dry-run d’abord.
- Suppression définitive : **pas en V1** sauf décision future explicitement validée.

## Documents liés

- [Rétention](07_RETENTION_AND_DELETION_RULES.md)
- [Sécurité](13_SECURITY_PRIVACY_AND_HUMAN_VALIDATION.md)
- [Tests](14_TEST_AND_VALIDATION_PLAN.md)
