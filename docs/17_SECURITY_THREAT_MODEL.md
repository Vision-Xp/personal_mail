# Modèle de menace — personal_mail

`personal_mail` manipule des informations personnelles, administratives, financières, contractuelles, bancaires et des documents sensibles issus de plusieurs boîtes Gmail. Ce document décrit les actifs, menaces, mitigations et la règle canonique en cas de doute.

## 1. Actifs à protéger

| Actif | Sensibilité | Notes |
|-------|-------------|-------|
| Tokens OAuth Gmail | SECRET | Accès complet aux comptes |
| Comptes Gmail | FINANCIAL_SENSITIVE / SENSITIVE_PERSONAL | Identité, volume, historique |
| Mails (corps, headers) | SENSITIVE_PERSONAL à FINANCIAL_SENSITIVE | Selon contenu |
| Pièces jointes | SENSITIVE_PERSONAL à FINANCIAL_SENSITIVE | Factures, contrats, malware potentiel |
| Documents extraits | FINANCIAL_SENSITIVE | Fichiers dans `personal_radar\documents` |
| Manifestes PersonalRadar | PERSONAL_METADATA | Pas de secrets, mais PII |
| Rapports | PERSONAL_METADATA à SENSITIVE_PERSONAL | Selon niveau de redaction |
| Logs | PERSONAL_METADATA | Doivent être expurgés par défaut |
| Règles de classification | INTERNAL_CONFIG | Révèlent priorités et organismes |
| Brouillons préparés | SENSITIVE_PERSONAL | Contenu avant envoi |
| Chemins locaux | INTERNAL_CONFIG | Structure disque Windows |
| Métadonnées (ids, labels) | PERSONAL_METADATA | Traçabilité |

Voir [18 — Classification des données](18_DATA_CLASSIFICATION_AND_RETENTION.md).

## 2. Menaces principales

| # | Menace | Description |
|---|--------|-------------|
| T1 | Fuite de tokens | Exposition OAuth → accès compte Gmail |
| T2 | Commit accidentel de secrets | Token, `.eml`, rapport PII dans Git |
| T3 | Suppression erronée de mails | Règle trop agressive ou bug |
| T4 | Extraction au mauvais endroit | Document sensible hors arborescence PR |
| T5 | Classification erronée | Mail financier/admin traité comme bruit |
| T6 | Phishing/scam non détecté | Utilisateur exposé à fraude |
| T7 | PJ dangereuse ouverte auto | Malware, macro, script |
| T8 | Logs avec données personnelles | Fuite via fichiers log |
| T9 | Rapport avec infos sensibles | Partage ou commit involontaire |
| T10 | Accès local non autorisé au PC | Lecture tokens, exports, cache |
| T11 | Bug règle destructive | Apply sans dry-run ou mauvais filtre |
| T12 | Confusion multi-comptes | Action sur le mauvais `account_id` |
| T13 | Usurpation d’expéditeur | Fausse facture, domaine typosquatté |
| T14 | Dépendance compromise | Crate Rust, lib tierce |
| T15 | Mauvaise sync Thunderbird/Gmail | État local cru à tort pour vérité |
| T16 | Écriture incontrôlée dans PersonalRadar | Corruption états internes PR |

## 3. Principes de mitigation

| Principe | Application |
|----------|-------------|
| Moindre privilège | Scopes OAuth minimaux ; permissions Hermès progressives |
| Scopes OAuth minimaux | Lecture/labels/modify — pas send sauf phase dédiée validée |
| Stockage sécurisé des tokens | Windows Credential Manager / DPAPI / keyring — voir [19](19_SECRETS_AND_TOKEN_STORAGE.md) |
| Dry-run obligatoire | Toute règle destructive nouvelle |
| Quarantaine avant suppression | `SUSPICIEUX_A_VALIDER`, label dédié |
| Trash avant suppression définitive | Jamais delete direct en V1 |
| Validation humaine | Envoi, delete, désabonnement, ambiguïté |
| Logs redacted | Pas de corps mail, tokens, IBAN en clair par défaut |
| Pas de vrais mails dans Git | Fixtures synthétiques uniquement |
| Hash des documents extraits | Intégrité et détection doublons |
| Journalisation des actions | `action_id`, mode, compte, message_id |
| Séparation compte par compte | Token store et journaux par `account_id` |
| Lecture seule par défaut au démarrage | `default_mode: dry-run` |
| Activation progressive des permissions | read → labels → extract → trash contrôlé |

Voir [config/security_policy.example.yaml](../config/security_policy.example.yaml).

## 4. Matrice risque

| Menace | Impact | Probabilité | Mitigation | Statut V1 |
|--------|--------|-------------|------------|-----------|
| T1 Fuite tokens | Critique | Moyenne | Keyring, .gitignore, pas de log token | Spec + impl Phase 3 |
| T2 Commit secrets | Critique | Moyenne | .gitignore, audit Git, exemples fictifs | Spec ✅ |
| T3 Suppression erronée | Élevé | Moyenne | Dry-run, quarantaine, trash, pas delete V1 | Spec ✅ |
| T4 Mauvais chemin extraction | Élevé | Faible | Routes YAML, validation chemin, hash | Spec ✅ |
| T5 Mauvaise classification | Élevé | Moyenne | Scores confiance, review, inbox review | Spec ✅ |
| T6 Phishing non détecté | Élevé | Moyenne | Règles + SUSPICIEUX_A_VALIDER | Spec ✅ |
| T7 PJ dangereuse | Critique | Faible | Jamais exécuter, quarantaine — [21](21_ATTACHMENT_SECURITY.md) | Spec ✅ |
| T8 Logs PII | Élevé | Moyenne | Redaction — [20](20_AUDIT_LOGGING_AND_REDACTION.md) | Spec ✅ |
| T9 Rapport sensible | Moyen | Moyenne | Rapports locaux vs partageables, .gitignore | Spec ✅ |
| T10 Accès PC local | Critique | Faible | DPAPI, permissions Windows (hors scope app) | Partiel |
| T11 Bug règle destructive | Élevé | Faible | Tests, dry-run, mode par défaut | Spec + tests |
| T12 Confusion comptes | Moyen | Moyenne | `account_id` explicite partout | Spec ✅ |
| T13 Usurpation expéditeur | Élevé | Moyenne | Domaine, contexte, SUSPICIEUX | Spec ✅ |
| T14 Dépendance compromise | Variable | Faible | Cargo.lock, audit deps (Phase 10) | Ouvert |
| T15 Sync TB/Gmail | Moyen | Moyenne | Gmail = vérité, pas Thunderbird | Spec ✅ |
| T16 Écriture PR interne | Élevé | Faible | Protocole documents uniquement | Spec ✅ |

## 5. Règle canonique

> **En cas de doute : ne pas supprimer, ne pas envoyer, ne pas ouvrir, ne pas désabonner.**
> **Classer en validation humaine** (`SUSPICIEUX_A_VALIDER` ou `00_INBOX_REVIEW`).

Cette règle prime sur toute optimisation de volume ou de automatisation.

## Documents liés

- [Porte d’entrée sécurité](13_SECURITY_PRIVACY_AND_HUMAN_VALIDATION.md)
- [Classification données](18_DATA_CLASSIFICATION_AND_RETENTION.md)
- [Secrets et tokens](19_SECRETS_AND_TOKEN_STORAGE.md)
- [Logs et redaction](20_AUDIT_LOGGING_AND_REDACTION.md)
- [Sécurité pièces jointes](21_ATTACHMENT_SECURITY.md)
