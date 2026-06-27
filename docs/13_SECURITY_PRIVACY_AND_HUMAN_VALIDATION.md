# Sécurité, confidentialité et validation humaine

**Porte d’entrée sécurité** — `personal_mail` est un système **security-by-design** : il traitera des mails et documents classés **SENSITIVE_PERSONAL** et **FINANCIAL_SENSITIVE** (administratif, bancaire, contrats, factures, santé, emploi, identité). Les tokens OAuth sont **SECRET**.

Documentation détaillée :

| Document | Contenu |
|----------|---------|
| [17 — Modèle de menace](17_SECURITY_THREAT_MODEL.md) | Actifs, menaces, matrice risque, règle canonique |
| [18 — Classification des données](18_DATA_CLASSIFICATION_AND_RETENTION.md) | Niveaux PUBLIC → SECRET, Git, logs, rétention |
| [19 — Secrets et tokens](19_SECRETS_AND_TOKEN_STORAGE.md) | OAuth, keyring Windows, checklist activation |
| [20 — Logs et redaction](20_AUDIT_LOGGING_AND_REDACTION.md) | Audit, rapports expurgés, restauration |
| [21 — Sécurité pièces jointes](21_ATTACHMENT_SECURITY.md) | Extensions dangereuses, PDF, quarantaine |
| [config/security_policy.example.yaml](../config/security_policy.example.yaml) | Politique globale (exemple) |

## Règle canonique

> En cas de doute : **ne pas supprimer, envoyer, ouvrir ni désabonner.** Classer en validation humaine (`SUSPICIEUX_A_VALIDER` ou `00_INBOX_REVIEW`).

## Résumé des exigences

### Secrets et authentification

- **OAuth uniquement** — jamais de mot de passe Gmail en clair
- Tokens dans **keyring / DPAPI** — pas de fichier plat en production
- Tokens **jamais** dans Git, logs, rapports, exemples YAML, ni chat Hermès
- Révocation et rotation documentées — [19](19_SECRETS_AND_TOKEN_STORAGE.md)

### Git et dépôt

- `.gitignore` strict — voir racine du projet
- Pas de vrais comptes, mails, `.eml`, rapports PII, logs sensibles
- Config réelle : `*.local.yaml` uniquement en local
- Fixtures de test : synthétiques uniquement ([18](18_DATA_CLASSIFICATION_AND_RETENTION.md))

### Actions sensibles (validation humaine obligatoire)

- Suppression définitive (**interdite en V1** par défaut)
- Envoi de mail (**pas d’auto-send sensible en V1**)
- Désabonnement newsletter
- Nouvelle règle destructive (après dry-run)
- Ambiguïté financière / administrative
- Extraction vers PR d’un fichier suspect

### Opérations sécurisées

| Mécanisme | Rôle |
|-----------|------|
| Dry-run par défaut | `default_mode: dry-run` |
| Quarantaine | Avant toute suppression |
| Trash | Avant delete définitif (hors V1) |
| Permissions progressives | read → labels → extract → trash |
| Hash documents | Intégrité extraction |
| Logs redacted | Pas de corps mail ni token par défaut |

### Pièces jointes

Ne **jamais** exécuter ni ouvrir automatiquement les fichiers à risque. Détail : [21](21_ATTACHMENT_SECURITY.md).

### PersonalRadar

- Dépôt documentaire uniquement — `personal_radar\documents`
- Pas d’écriture dans états internes PR
- Documents validés ou non suspects uniquement

### Hermès

- Ne jamais demander mot de passe ni afficher token
- Rapports redacted si partage ; s’arrêter en cas de doute — [10](10_HERMES_OPERATING_PROTOCOL.md)

## Journalisation (résumé)

Chaque action trace : `action_id`, timestamp, mode, `account_id`, `message_id`, action, résultat, confiance, chemin document si extraction. Détail et redaction : [20](20_AUDIT_LOGGING_AND_REDACTION.md).

## Documents liés

- [Architecture](01_ARCHITECTURE_DECISIONS.md) — décision security-by-design
- [OAuth](04_GMAIL_OAUTH_IMAP_API_MODEL.md)
- [Rétention](07_RETENTION_AND_DELETION_RULES.md)
- [Extraction](08_DOCUMENT_EXTRACTION_TO_PERSONAL_RADAR.md)
- [Hermès](10_HERMES_OPERATING_PROTOCOL.md)
- [Tests sécurité](14_TEST_AND_VALIDATION_PLAN.md)
