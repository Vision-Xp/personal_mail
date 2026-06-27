# Roadmap d’implémentation

## Phase 0 — Specs repo ✅ (cette session)

- Créer specs Markdown complètes
- Config exemples YAML
- Décisions d’architecture documentées
- `.gitignore`, structure `reports/`
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
- [Décision log](16_DECISION_LOG.md)
