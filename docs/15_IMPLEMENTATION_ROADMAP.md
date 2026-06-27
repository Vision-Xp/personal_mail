# Roadmap d’implémentation

## Phase 0 — Specs repo ✅

- Créer specs Markdown complètes
- Config exemples YAML
- Décisions d’architecture documentées
- `.gitignore`, structure `reports/`
- Couche security-by-design (docs 17–21, security_policy)
- Commit / push

## Phase 1 — Choix client mail et preuve Thunderbird/Gmail

- Tester Thunderbird Desktop (Windows)
- Tester Thunderbird Android
- Vérifier visibilité labels Gmail créés manuellement ou via API test
- Vérifier multi-comptes
- Valider Thunderbird comme cockpit humain
- Clôturer décision [02_CLIENT_MAIL_SELECTION](02_CLIENT_MAIL_SELECTION.md)

## Phase 2 — Rust CLI skeleton

- Structure projet Cargo
- Chargement config (exemples → local)
- Logs structurés
- Mode dry-run global
- Gestion erreurs
- Tests unitaires de base

## Phase 2 bis — Sécurité transversale (parallèle Phases 2–6)

- Implémenter modèle de menace en code (modes, permissions)
- Stockage tokens keyring / DPAPI Windows
- Moteur de redaction logs et rapports
- Tests sécurité S1–S12 ([14](14_TEST_AND_VALIDATION_PLAN.md))
- Permissions progressives (read → labels → extract → trash)
- Audit Git secrets (pre-commit ou CI : détection token/`.eml`)
- Chargement `security_policy.local.yaml`

## Phase 3 — Gmail OAuth proof

- OAuth compte **test** uniquement
- Scopes minimaux
- Lecture messages test
- Création / liste labels test

## Phase 4 — Classification non destructive

- Scan messages
- Application labels
- Scores de confiance
- Rapports classification
- **Pas de suppression**

## Phase 5 — Extraction documentaire

- Téléchargement pièces jointes
- Export `.eml` + `.meta.json`
- Routage `personal_radar\documents`
- Manifeste `_incoming_mail_manifest.jsonl`

## Phase 6 — Rétention et nettoyage

- Réseaux sociaux > 30 jours (dry-run puis apply)
- Promotions inutiles
- Scams avérés
- Quarantaine
- Validation humaine avant apply

## Phase 7 — Hermès ops

- Pack contexte Hermès (`hermes_context/`) — source canonique versionnée ✅ specs
- Documentation sync : [22](22_HERMES_SKILL_AND_CONTEXT_PACK.md), [23](23_HERMES_CONTEXT_SYNC_AND_INSTALL.md)
- Synchronisation future vers dossier Hermès local (`AppData\Local\hermes`)
- Script futur : `scripts/sync_hermes_context.ps1` (à créer — pas en phase specs)
- Validation de relecture Hermès après sync (checklist GO/NO GO)
- Scripts / prompts d’exploitation
- Rapports standardisés
- Protocole validation Damien

## Phase 8 — Compose workflow

- Génération contenu réponses
- Ouverture brouillon Thunderbird Windows (méthode à trouver)
- Validation humaine avant envoi

## Phase 9 — Audits périodiques

- Newsletters (semestriel)
- Revue catégories / labels obsolètes
- Stockage Gmail
- Règles devenues inutiles

## Phase 10 — Durcissement

- Logs robustes, rotation
- Restauration depuis trash/quarantaine
- Suite de tests élargie
- Sécurité tokens (keyring OS)
- Packaging binaire Windows

## Documents liés

- [Vision](00_PRODUCT_VISION.md)
- [Tests](14_TEST_AND_VALIDATION_PLAN.md)
- [Sécurité](13_SECURITY_PRIVACY_AND_HUMAN_VALIDATION.md)
- [Décision log](16_DECISION_LOG.md)
- [Hermès context pack](22_HERMES_SKILL_AND_CONTEXT_PACK.md)
