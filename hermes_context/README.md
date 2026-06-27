# hermes_context — pack opérationnel Hermès

Ce dossier contient le **contexte opérationnel court** pour Hermès sur le projet `personal_mail`.

## Règles

- **Ne remplace pas** les specs complètes dans `docs/` — les consulter pour le détail.
- **Source canonique versionnée** : modifications importantes → commit dans `personal_mail`, puis sync future vers le dossier Hermès local.
- **Aucun secret** : pas de tokens, mots de passe, clés API.
- **Aucune donnée réelle** : pas de mails, adresses perso, montants, noms réels.
- **Aucune config OAuth réelle**.
- **Aucune pièce jointe** ni mail réel.

## Fichiers

| Fichier | Rôle |
|---------|------|
| [PERSONAL_MAIL_CORE_CONTEXT.md](PERSONAL_MAIL_CORE_CONTEXT.md) | Résumé projet, architecture, V1 |
| [PERSONAL_MAIL_OPERATING_RULES.md](PERSONAL_MAIL_OPERATING_RULES.md) | Ce qu’Hermès peut / doit / ne doit pas faire |
| [PERSONAL_MAIL_SECURITY_RULES.md](PERSONAL_MAIL_SECURITY_RULES.md) | Rappel sécurité condensé |
| [PERSONAL_MAIL_ACTION_MODES.md](PERSONAL_MAIL_ACTION_MODES.md) | dry-run, safe-run, apply-run, audit-run, compose-run |
| [PERSONAL_MAIL_PROMPT_TEMPLATES.md](PERSONAL_MAIL_PROMPT_TEMPLATES.md) | Prompts modèles pour sessions Hermès/Cursor |
| [PERSONAL_MAIL_VALIDATION_CHECKLISTS.md](PERSONAL_MAIL_VALIDATION_CHECKLISTS.md) | Checklists avant compte, règle, extraction, mail, commit |

## Sync future

Voir [docs/23_HERMES_CONTEXT_SYNC_AND_INSTALL.md](../docs/23_HERMES_CONTEXT_SYNC_AND_INSTALL.md).

Destination probable : `C:\Users\SMAD Inc\AppData\Local\hermes` — **non modifiée dans la phase specs**.
