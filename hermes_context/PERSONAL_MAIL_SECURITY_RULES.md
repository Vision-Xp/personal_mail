# PERSONAL_MAIL — règles sécurité (rappel Hermès)

## Classification rapide

| Donnée | Niveau |
|--------|--------|
| Mails, corps, PJ | **Sensible** (SENSITIVE_PERSONAL / FINANCIAL_SENSITIVE) |
| Tokens OAuth | **SECRET** |
| Documents admin / financiers | **Sensible** |
| Ce pack `hermes_context/` | PUBLIC_OR_DOCS_ONLY — générique uniquement |

## Git et dépôt

- **Aucun secret** dans Git
- **Aucun vrai `.eml`** dans Git
- **Aucun rapport PII** dans Git
- Config réelle : `*.local.yaml` — local uniquement

## Authentification

- **OAuth uniquement** — jamais mot de passe Gmail
- **Scopes minimaux**
- Tokens dans **keyring / DPAPI** (implémentation future) — pas de fichier plat
- Jamais token dans logs, rapports, chat, ou ce dossier

## Opérations

- **Logs redacted** par défaut (pas de corps mail, pas de token)
- PJ suspectes → **quarantaine** (`SUSPICIEUX_A_VALIDER`)
- **Trash / quarantaine** avant toute suppression
- **Suppression définitive interdite** en V1
- **Envoi automatique interdit** en V1

## Extensions dangereuses — ne jamais exécuter / ouvrir auto

`.exe`, `.bat`, `.cmd`, `.ps1`, `.vbs`, `.js`, `.scr`, `.msi`, `.jar`, `.lnk`

**Archives suspectes** (`.zip`, `.rar`, `.7z`) si origine inconnue.

Documents Office avec **macros** si expéditeur suspect.

## Règle canonique

Doute → validation humaine. Voir `PERSONAL_MAIL_OPERATING_RULES.md`.

## Détail complet

`docs/13`, `docs/17`–`21`, `config/security_policy.example.yaml`
