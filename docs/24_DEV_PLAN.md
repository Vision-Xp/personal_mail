# Plan de développement — personal_mail

Source : docs/00 à docs/23, config examples, hermes_context/.
Périmètre : phase 0 livrée (specs). Plan couvre phases 0 à 10.

## 0. Objectif du plan

- Livrer un moteur Rust pilotable par Hermès via CLI.
- Organiser Gmail en source de vérité.
- Afficher l’organisation dans Thunderbird (Win + Android) sans dupliquer l’état métier.
- Extraire documents sensibles vers I:\Dev Applications\personal_radar\documents par protocole documentaire.
- Respecter sécurité-by-design : dry-run, quarantaine, validation humaine, keyring/DPAPI, logs expurgés.

## 1. Phases, livrables et critères GO

### Phase 0 — Specs repo
Statut : livré.
Livrables : docs 00–23, config exemples, .gitignore, hermes_context/, reports/README.
Qualité : sécurité-by-design couverte (docs security + security_policy.example.yaml).

### Phase 1 — Choix client mail et preuve Thunderbird/Gmail
Objectif : valider l’hypothèse client humain avant d’écrire du code Rust.

Sous-tâches
1. Installer/configurer Thunderbird Desktop (Windows) avec OAuth2 Gmail multi-comptes.
2. Créer via API Gmail test la taxonomie labels (05) et vérifier affichage Desktop.
3. Installer/configurer Thunderbird Android, même validation visibilité labels.
4. Valider multi-comptes (labels distincts / règles par compte).
5. Documenter la checklist GO/NO GO (client stable, labels synchronisés).

Critères GO
- Labels créés API visibles Desktop + Android (10 min max latency).
- Pas de duplicate local IMAP comme source de vérité.
- Compte test uniquement.

Risques : quota API, latence sync Android.
Mitigation : retry/backoff, mesure explicit.

### Phase 2 — Rust CLI skeleton
Objectif : base exécutable, config, logs, erreurs, dry-run global.

Sous-tâches
1. Initialiser Cargo workspace (binaire CLI).
2. Charger config depuis config/*.example.yaml vers local copies (*.local.yaml) non commitées.
3. Logs structurés JSON, rotation locale.
4. Dry-run global (default_mode: dry-run).
5. Gestion erreurs + codes retour stables.
6. CLI help + modes (dry-run, safe-run, apply-run, audit-run, compose-run).

Livrable
- Binaire personal-mail CLI opérationnel en --help.
- Exemple personal_mail.local.yaml avec valeurs safe.

Critères GO
- cargo build --release OK.
- personal-mail --help fonctionne.
- Lancement dry-run sans erreur sans compte configuré.

### Phase 2 bis — Sécurité transversale (parallèle Phases 2–6)
Objectif : implémenter modèle de menace, stockage sécurisé, redaction, tests sécurité.

Sous-tâches
1. Intégrer crate keyring/DPAPI pour tokens OAuth (19, 04).
2. Implémenter scanner secrets (git grep + CI future).
3. Moteur redaction logs/rapports (20).
4. Permissions progressives par mode (19).
5. Security policy loader (security_policy.local.yaml).
6. Tests S1–S12 (14).

Livrable
- Module security/ + intégration CLI.

### Phase 3 — Gmail OAuth proof
Objectif : preuve bout-en-bout sur compte test, sans mutation métier.

Sous-tâches
1. Flux OAuth 2.0 par compte, scopes minimaux (lecture/labels/attachments).
2. Stockage token keyring séparé par account_id.
3. Lecture métadonnées messages (list/get metadata).
4. Création/liste labels test.
5. Vérifier visibilité labels dans Thunderbird Desktop + Android.

Critères GO
- Auth réussie sans mot de passe clair.
- Labels test visibles partout.
- Aucun secret exposé (S1–S3 passent).

### Phase 4 — Classification non destructive
Objectif : appliquer labels Gmail selon règles métier, sans suppression.

Sous-tâches
1. Charger taxonomie labels (05) + règles catégories (06).
2. Implémenter moteur scoring (confiance, signaux).
3. Modes dry-run + safe-run labels-only.
4. Rapports classification par compte (14).
5. Quarantaine ambigu (SUSPICIEUX_A_VALIDER).
6. Validation humaine pour règles nouvelles ou cas limites.

Critères GO
- Scénarios tests 1–12 passent (fixtures synthétiques).
- Rapports lisibles.
- Aucun delete; labels synchronisés.

### Phase 5 — Extraction documentaire vers PersonalRadar
Objectif : exporter pièces jointes / .eml vers I:\Dev Applications\personal_radar\documents.

Sous-tâches
1. Routing docs par catégorie config (08).
2. Sécurité PJ (21) : extensions, MIME, quarantaine.
3. Renommage conventionnel (08).
4. Sidecar .meta.json (08).
5. Hash SHA-256 + traçabilité action_log_id.
6. Manifeste JSONL optionnel (09).
7. Journal extraction dry-run / safe-run.
8. Tests 13–16 passent.

Exclusions
- Pas d’écriture base/rapports PersonalRadar (protocole documentaire uniquement).

### Phase 6 — Rétention et nettoyage
Objectif : nettoyage contrôlé (dry-run puis apply) avec quarantaine.

Sous-tâches
1. Règles rétention (07) configurées par catégorie.
2. Moteur dry-run trash + rapport diff.
3. Validation humaine obligatoire avant apply.
4. Réseaux > 30j, promotions inutiles, scams avérés (06, 07).
5. Procédure rollback trash listée (20).
6. Tests 17–18 passent.

Critères GO
- dry-run sans mutation, apply seulement post-validation.
- Aucune suppression définitive V1.

### Phase 7 — Hermès ops
Objectif : fournir pack d’exploitation à Hermès et templates prêts à l’emploi.

Sous-tâches
1. Pack hermes_context/ cohérent docs/22–23.
2. Prompts Cursor + skill Hermès dédié (22).
3. Scripts : setup config, dry-run, validation Damien (23).
4. Rapports standardisés (20).
5. Checklist GO/NO GO post-sync contexte.

Livrable
- scripts/setup_personal_mail.ps1 + docs d’usage.

### Phase 8 — Compose workflow
Objectif : préparer brouillons sans envoyer.

Sous-tâches
1. Extraction contexte mail vers template brouillon (12).
2. Ouverture brouillon Thunderbird Windows (méthode à valider Phase 1).
3. Validation humaine avant envoi.
4. Interdiction envoyer avant validation explicite (security_policy).

### Phase 9 — Audits périodiques
Objectif : maintenir la base propre et économique.

Sous-tâches
1. Scanner newsletters inutiles (semestriel).
2. Revue labels/catégories obsolètes.
3. Revue stockage Gmail.
4. Désactivation règles inutiles.

### Phase 10 — Durcissement
Objectif : production-ready.

Sous-tâches
1. Tests sécurité élargis, rotation secrets.
2. Audit dépendances Cargo (T14).
3. Logs robustes, rotation, purge PII.
4. Restauration depuis trash/quarantaine documentée.
5. Packaging binaire Windows (installer/scoop candidate).
6. CI privée (tests + secrets scan).

## 2. Transversale : règles communes à toutes phases

- Sécurité : lire security_policy.example.yaml, ne jamais committer secrets.
- Données sensibles : mails/tokens/docs extraits = SENSITIVE_PERSONAL / FINANCIAL_SENSIBLE.
- Validations humaines : toute action destructrice/ambiguë nécessite GO Damien.
- Logs : expurgés par défaut (pas corps mail / token).
- Git : workflow feature branch, PR review, merge main.
- Tests : fixtures synthétiques, pas de données réelles en CI.

## 3. Frontières d’implémentation

- Thunderbird = cockpit humain, pas base métier.
- Gmail API = voie canonique pour labels, recherche, trash.
- PersonalRadar = ajout fichiers + manifeste JSONL uniquement.
- Rust moteur CLI ; Hermès opère par CLI/rapports.
- IMAP = secours affichage uniquement, pas logique métier.

## 4. Points ouverts à confirmer (décisions 16)

- Structure fine sous-dossiers documents/ PR (fixe ou dynamique).
- Méthode compose Thunderbird Windows (API/URL?).
- Rythme CI privée (GitHub vs Git local).
- Lissage quotas Gmail API multi-comptes.

## 5. Prochaine action immédiate

Démarrer Phase 2 (Rust CLI skeleton) en parallèle d’un POC Phase 1 léger (labels API test + Thunderbird) pour valider hypothèse avant implémentation Rust avancée.
