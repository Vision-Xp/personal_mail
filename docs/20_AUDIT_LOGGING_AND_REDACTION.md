# Journalisation, audit et redaction

## 1. Besoin

| Objectif | Description |
|----------|-------------|
| Auditabilité | Savoir qui/quoi/quand/compte pour chaque action |
| Classification | Comprendre pourquoi un mail a reçu un label |
| Extraction | Tracer fichier, hash, chemin PR |
| Restauration | Revenir en arrière après erreur |
| Anti-suppression silencieuse | Aucune delete/trash sans trace |

## 2. Logs internes — champs possibles

| Champ | Description | Redaction par défaut |
|-------|-------------|----------------------|
| `action_id` | UUID unique | Non |
| `timestamp` | UTC ISO 8601 | Non |
| `mode` | dry-run / safe-run / apply-run | Non |
| `account_id` | Identifiant compte | Pseudonyme OK en log partageable |
| `message_id` | Id Gmail | Non en local ; masquer partiel si export |
| `thread_id` | Id thread | Idem |
| `action` | classify, extract, trash, quarantine, … | Non |
| `category` | Label cible | Non |
| `confidence` | Score 0–1 | Non |
| `result` | ok / error / skipped | Non |
| `target_label` | Label appliqué | Non |
| `document_path` | Chemin relatif PR | Non en local |
| `hash` | SHA-256 fichier | Non |
| `error_code` | Code erreur structuré | Non |
| `sender` | Expéditeur | **Masquer** si rapport partageable |
| `subject` | Objet | **Tronquer / masquer** par défaut |
| `body` | Corps mail | **Jamais** par défaut |

Stockage local : `logs/` — ignoré par Git.

## 3. Redaction

| Donnée | Règle |
|--------|-------|
| Adresses mail | `damien@example.com` → `d***@example.com` si rapport partageable |
| Tokens | Toujours `[REDACTED]` |
| Liens sensibles | Tronquer query params |
| IBAN / RIB | Masquer tout sauf 4 derniers caractères |
| N° contrat | Masquer si rapport non local |
| Sujets mail | Tronquer à N caractères ou remplacer par catégorie |
| Corps mail | Ne jamais logger en entier par défaut |
| Montants | Masquer dans logs info ; OK en log debug local désactivé par défaut |

`allow_full_local_debug_logs: false` dans [security_policy.example.yaml](../config/security_policy.example.yaml).

## 4. Types de rapports

| Type | Contenu | Versionnable Git |
|------|---------|------------------|
| Rapport local complet | PII autorisée sur machine Damien | ❌ |
| Rapport partageable expurgé | Redaction appliquée | ❌ (sauf template fictif) |
| Rapport de validation | Checklist GO/NO GO | ❌ si données réelles |
| Rapport dry-run | Liste messages affectés | ❌ |
| Rapport erreurs | Stack, codes — pas de token | ❌ |

Templates fictifs sans PII : niveau PUBLIC_OR_DOCS_ONLY — possible en `docs/` ou fixtures.

## 5. Règles Git

- Aucun rapport réel commité
- Seuls exemples fictifs ou README dans `reports/`
- `.gitignore` exclut `reports/**/*.json`, `*.jsonl`, `*.csv`, `*.html`, `*.pdf`, `*.eml`, `*.txt`
- `logs/` et `*.log` exclus

## 6. Restauration

Chaque action destructive doit laisser une trace permettant le rollback :

| Action | Trace minimale | Rollback |
|--------|----------------|----------|
| Label appliqué | `action_id`, labels avant/après | Retirer label via API |
| Quarantaine | `message_id`, label quarantaine | Retirer label |
| Trash | `message_id`, compte, timestamp | `untrash` Gmail si dans délai |
| Extraction | `hash`, chemin, `action_log_id` | Supprimer fichier PR si erreur (manuel) |

Rapport de rollback à prévoir en implémentation (Phase 10) : liste des `action_id` réversibles.

## Documents liés

- [Modèle de menace](17_SECURITY_THREAT_MODEL.md)
- [Classification données](18_DATA_CLASSIFICATION_AND_RETENTION.md)
- [Porte d’entrée sécurité](13_SECURITY_PRIVACY_AND_HUMAN_VALIDATION.md)
