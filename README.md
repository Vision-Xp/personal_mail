# personal_mail

**SPECIFICATION PHASE — NO REAL MAIL ACTION YET**

`personal_mail` est le cerveau mail intelligent de l’écosystème Damien : un moteur Rust (à implémenter) qui organise plusieurs boîtes Gmail, supprime le bruit, isole les risques, extrait les documents importants vers PersonalRadar, et laisse Damien consulter ses boîtes proprement organisées depuis Thunderbird sur Windows et Android.

Hermès pilote `personal_mail`. `personal_mail` pilote Gmail. Thunderbird affiche l’organisation et sert à lire, modifier, répondre et envoyer.

## Séparation des rôles

| Composant | Rôle |
|-----------|------|
| **Gmail** | Source de vérité serveur (messages, threads, labels, états, corbeille, spam, classement, quarantaine) |
| **personal_mail** (Rust) | Cerveau : classification, règles, extraction, journaux, orchestration |
| **Hermès** | Opérateur / orchestrateur : configuration, dry-run, validation, rapports, préparation de brouillons |
| **Thunderbird** (Desktop + Android) | Cockpit humain de consultation et rédaction — **pas une base métier** |
| **PersonalRadar** | Destination documentaire et analyse via scan normal des documents déposés |

Les labels et l’organisation sont **écrits côté Gmail** pour être visibles partout (Thunderbird Desktop, Thunderbird Android, Gmail Web). Thunderbird ne décide pas du classement ; il affiche l’organisation déjà créée côté Gmail.

## Documentation

| Document | Description |
|----------|-------------|
| [00 — Vision produit](docs/00_PRODUCT_VISION.md) | Problèmes, objectifs, non-objectifs V1 |
| [01 — Décisions d’architecture](docs/01_ARCHITECTURE_DECISIONS.md) | Rust-first, Gmail source de vérité, schéma cible |
| [02 — Choix client mail](docs/02_CLIENT_MAIL_SELECTION.md) | Comparaison clients, recommandation Thunderbird |
| [03 — Modèle multi-comptes Gmail](docs/03_GMAIL_MULTI_ACCOUNT_MODEL.md) | Comptes, règles globales et spécifiques |
| [04 — OAuth, IMAP et API Gmail](docs/04_GMAIL_OAUTH_IMAP_API_MODEL.md) | Authentification, voies d’accès, actions destructives |
| [05 — Taxonomie des catégories](docs/05_CATEGORY_TAXONOMY.md) | Labels, sous-catégories, règles anti-usine-à-gaz |
| [06 — Règles de classification](docs/06_CLASSIFICATION_RULES.md) | Signaux, confiance, cas typiques |
| [07 — Rétention et suppression](docs/07_RETENTION_AND_DELETION_RULES.md) | Conservation, quarantaine, dry-run |
| [08 — Extraction vers PersonalRadar](docs/08_DOCUMENT_EXTRACTION_TO_PERSONAL_RADAR.md) | Formats, renommage, métadonnées |
| [09 — Intégration PersonalRadar](docs/09_PERSONAL_RADAR_INTEGRATION.md) | Manifeste, alertes, limites |
| [10 — Protocole Hermès](docs/10_HERMES_OPERATING_PROTOCOL.md) | Modes opératoires, rapports, interdictions |
| [11 — Usage Windows / Android](docs/11_WINDOWS_ANDROID_USAGE_MODEL.md) | Thunderbird comme cockpit synchronisé |
| [12 — Réponses et composition](docs/12_REPLY_AND_COMPOSE_WORKFLOW.md) | Workflow Hermès → Damien → envoi |
| [13 — Sécurité et validation humaine](docs/13_SECURITY_PRIVACY_AND_HUMAN_VALIDATION.md) | Secrets, Git, actions sensibles |
| [14 — Plan de tests](docs/14_TEST_AND_VALIDATION_PLAN.md) | Fixtures synthétiques, critères GO/NO GO |
| [15 — Roadmap d’implémentation](docs/15_IMPLEMENTATION_ROADMAP.md) | Phases 0 à 10 |
| [16 — Journal des décisions](docs/16_DECISION_LOG.md) | Décisions confirmées et ouvertes |
| [17 — Modèle de menace](docs/17_SECURITY_THREAT_MODEL.md) | Actifs, menaces, mitigations, matrice risque |
| [18 — Classification des données](docs/18_DATA_CLASSIFICATION_AND_RETENTION.md) | Niveaux PUBLIC → SECRET, règles Git/logs |
| [19 — Secrets et tokens](docs/19_SECRETS_AND_TOKEN_STORAGE.md) | OAuth, keyring Windows, permissions progressives |
| [20 — Logs et redaction](docs/20_AUDIT_LOGGING_AND_REDACTION.md) | Audit, rapports expurgés, restauration |
| [21 — Sécurité pièces jointes](docs/21_ATTACHMENT_SECURITY.md) | Extensions dangereuses, PDF/factures, quarantaine |
| [22 — Hermès skill / context pack](docs/22_HERMES_SKILL_AND_CONTEXT_PACK.md) | Source canonique du contexte Hermès |
| [23 — Sync contexte Hermès](docs/23_HERMES_CONTEXT_SYNC_AND_INSTALL.md) | Installation et sync future vers dossier local |

Configuration exemple (non sensible) : voir [config/README.md](config/README.md).

Rapports générés (non versionnés si données perso) : voir [reports/README.md](reports/README.md).

## Statut actuel

- **Phase** : spécification uniquement — aucun moteur Rust, aucun compte Gmail réel, aucune action mail.
- **Contenu versionné** : documentation Markdown, fichiers YAML d’exemple, structure `reports/` avec README.
- **Prochaine étape** : Phase 1 — validation Thunderbird Desktop/Android avec labels Gmail (voir [roadmap](docs/15_IMPLEMENTATION_ROADMAP.md)).

## Security-by-design

`personal_mail` est conçu comme un **système sécurisé dès le départ**. Il traitera des mails personnels, données administratives et financières, contrats, factures, échéanciers, preuves d’achat, garanties, pièces jointes sensibles et documents destinés à `personal_radar\documents`. **Mails, documents extraits et tokens OAuth sont des données sensibles** — pas du contenu public.

La sécurité est une **exigence transversale** : architecture, config, Hermès, extraction, tests et roadmap y sont alignés.

| Principe | Référence |
|----------|-----------|
| Moindre privilège, OAuth, tokens protégés | [docs/19](docs/19_SECRETS_AND_TOKEN_STORAGE.md) |
| Aucun secret dans Git | [.gitignore](.gitignore), [docs/18](docs/18_DATA_CLASSIFICATION_AND_RETENTION.md) |
| Logs et rapports expurgés | [docs/20](docs/20_AUDIT_LOGGING_AND_REDACTION.md) |
| Dry-run, quarantaine, validation humaine | [docs/17](docs/17_SECURITY_THREAT_MODEL.md) |
| Pièces jointes : ne jamais exécuter | [docs/21](docs/21_ATTACHMENT_SECURITY.md) |
| Politique globale (exemple) | [config/security_policy.example.yaml](config/security_policy.example.yaml) |

**Règle canonique** : en cas de doute — ne pas supprimer, envoyer, ouvrir ni désabonner ; classer en validation humaine.

Voir [docs/13_SECURITY_PRIVACY_AND_HUMAN_VALIDATION.md](docs/13_SECURITY_PRIVACY_AND_HUMAN_VALIDATION.md) — porte d’entrée sécurité.

## Hermès context pack

Le dossier [`hermes_context/`](hermes_context/README.md) est la **source canonique versionnée** du contexte opérationnel Hermès pour `personal_mail`. Il contient des résumés courts (règles, sécurité, modes, prompts, checklists) destinés à être **copiés/synchronisés plus tard** vers le dossier Hermès local — sans dupliquer toute la documentation `docs/`.

| Ressource | Description |
|-----------|-------------|
| [hermes_context/README.md](hermes_context/README.md) | Présentation du pack |
| [docs/22 — Hermès skill](docs/22_HERMES_SKILL_AND_CONTEXT_PACK.md) | Pourquoi le pack vit dans le repo |
| [docs/23 — Sync et install](docs/23_HERMES_CONTEXT_SYNC_AND_INSTALL.md) | Stratégie de sync future (script non créé) |

**Règle** : évolutions importantes → commit dans `personal_mail` ; le dossier Hermès local est une **copie opérationnelle**, pas la source unique.
