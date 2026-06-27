# Configuration — exemples uniquement

Ce dossier contient **uniquement des fichiers d’exemple** pour la phase de spécification et les futurs tests.

## Règles

- **Aucun secret** : pas de tokens, pas de mots de passe, pas de clés API.
- **Aucun vrai compte** : les adresses `@gmail.com` sont fictives.
- Les **vrais fichiers de configuration** devront être locaux et **ignorés par Git** (voir `.gitignore` : `*.local.yaml`, `*real*.yaml`, `*private*.yaml`).
- Copier un fichier `.example.yaml` vers un nom local (ex. `gmail_accounts.local.yaml`) lors de l’implémentation future — ne jamais committer les copies locales.

## Fichiers exemples

| Fichier | Rôle |
|---------|------|
| [gmail_accounts.example.yaml](gmail_accounts.example.yaml) | Comptes Gmail fictifs, profils de règles |
| [category_rules.example.yaml](category_rules.example.yaml) | Règles de classification par expéditeur, domaine, etc. |
| [retention_rules.example.yaml](retention_rules.example.yaml) | Conservation, suppression, audits |
| [document_routes.example.yaml](document_routes.example.yaml) | Routage vers `personal_radar\documents` |
| [hermes_permissions.example.yaml](hermes_permissions.example.yaml) | Permissions et validations Hermès |
| [security_policy.example.yaml](security_policy.example.yaml) | Politique sécurité globale (dry-run, OAuth, logs, PJ, PR) |

Voir aussi [docs/10_HERMES_OPERATING_PROTOCOL.md](../docs/10_HERMES_OPERATING_PROTOCOL.md), [docs/13_SECURITY_PRIVACY_AND_HUMAN_VALIDATION.md](../docs/13_SECURITY_PRIVACY_AND_HUMAN_VALIDATION.md) et [docs/17_SECURITY_THREAT_MODEL.md](../docs/17_SECURITY_THREAT_MODEL.md).
