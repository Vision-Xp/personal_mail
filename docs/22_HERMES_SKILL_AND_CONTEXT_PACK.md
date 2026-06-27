# Hermès skill et context pack

## Pourquoi le repo contient un pack Hermès

Le dossier Hermès local (`C:\Users\SMAD Inc\AppData\Local\hermes` ou équivalent) peut héberger des règles opérationnelles au quotidien. Le dépôt **`personal_mail` reste la source canonique versionnée** : toute règle critique doit pouvoir être retrouvée, revue et restaurée via Git.

Le dossier `hermes_context/` contient une **copie opérationnelle courte** — pas un doublon des specs complètes de `docs/`.

## Principes

| Principe | Détail |
|----------|--------|
| Source canonique | `personal_mail` (repo Git) |
| Copie opérationnelle | Dossier Hermès local — généré/copié depuis le repo |
| Règles critiques | Ne vivent **pas** uniquement hors Git |
| Évolutions importantes | Toujours commitées dans le repo |
| `hermes_context/` | Fichiers courts, opérationnels, lisibles par Hermès |
| `docs/` | Specs complètes, architecture, sécurité, tests |

## Rôles — ce qu’Hermès doit pouvoir faire

- Lire les specs et le context pack
- Préparer l’installation et la configuration future
- Demander les autorisations nécessaires (OAuth — jamais mot de passe)
- Lancer les futurs dry-runs
- Analyser les rapports (classification, cleanup, extraction)
- Appliquer **uniquement** les règles validées par Damien
- Extraire les documents vers `I:\Dev Applications\personal_radar\documents` (quand implémenté)
- Préparer des mails / brouillons avec validation humaine
- **Refuser ou suspendre** une action en cas de doute

## Rôles — ce qu’Hermès ne doit pas faire

- Demander un mot de passe Gmail en clair
- Afficher ou stocker des tokens (chat, logs, fichiers versionnés)
- Envoyer un mail sensible sans validation humaine
- Supprimer définitivement en V1
- Ouvrir automatiquement une pièce jointe suspecte
- Modifier PersonalRadar hors protocole documentaire
- Committer des données réelles (mails, rapports PII, secrets)
- Confondre Thunderbird et Gmail comme sources métier

## Contenu du pack

| Fichier | Rôle |
|---------|------|
| [hermes_context/README.md](../hermes_context/README.md) | Présentation du dossier |
| [PERSONAL_MAIL_CORE_CONTEXT.md](../hermes_context/PERSONAL_MAIL_CORE_CONTEXT.md) | Résumé dense architecture et V1 |
| [PERSONAL_MAIL_OPERATING_RULES.md](../hermes_context/PERSONAL_MAIL_OPERATING_RULES.md) | Règles opérationnelles Hermès |
| [PERSONAL_MAIL_SECURITY_RULES.md](../hermes_context/PERSONAL_MAIL_SECURITY_RULES.md) | Rappel sécurité court |
| [PERSONAL_MAIL_ACTION_MODES.md](../hermes_context/PERSONAL_MAIL_ACTION_MODES.md) | Modes dry-run, safe-run, etc. |
| [PERSONAL_MAIL_PROMPT_TEMPLATES.md](../hermes_context/PERSONAL_MAIL_PROMPT_TEMPLATES.md) | Prompts modèles génériques |
| [PERSONAL_MAIL_VALIDATION_CHECKLISTS.md](../hermes_context/PERSONAL_MAIL_VALIDATION_CHECKLISTS.md) | Checklists avant action |

## Pourquoi ne pas se contenter du dossier Hermès ?

Le dossier Hermès local est **opérationnel** mais **non idéal comme source unique** :

- Pas de versioning structuré ni d’historique de revue
- Risque de dérive silencieuse (règles modifiées localement sans trace)
- Difficile à partager entre Cursor, Hermès, ChatGPT et futures automations

Le **repo** apporte :

- Versioning, revue, rollback, synchronisation GitHub
- Source unique pour Cursor, Hermès et assistants
- Alignement avec specs `docs/`, config `config/`, sécurité `docs/17–21`

**Flux correct** : modifier `hermes_context/` dans le repo → commit → sync contrôlé vers Hermès local (voir [23](23_HERMES_CONTEXT_SYNC_AND_INSTALL.md)).

**Flux incorrect** : inventer des règles uniquement dans le dossier Hermès sans les reporter dans le repo.

## Documents liés

- [Sync et installation](23_HERMES_CONTEXT_SYNC_AND_INSTALL.md)
- [Protocole Hermès](10_HERMES_OPERATING_PROTOCOL.md)
- [Sécurité](13_SECURITY_PRIVACY_AND_HUMAN_VALIDATION.md)
