# Journal des décisions

## Décisions confirmées — 2026-06-27

| # | Décision |
|---|----------|
| 1 | Nom du projet : **personal_mail** |
| 2 | Toutes les boîtes mail ciblées sont **Gmail** |
| 3 | Moteur **Rust-first** |
| 4 | **Gmail** = source de vérité serveur (messages, threads, labels, états) |
| 5 | **Thunderbird** = cockpit humain Windows + Android |
| 6 | **Hermès** pilote personal_mail |
| 7 | personal_mail pilote **Gmail**, pas Thunderbird comme base métier |
| 8 | Les **labels** sont créés côté Gmail |
| 9 | Thunderbird récupère l’organisation par **synchronisation** |
| 10 | Documents extraits → `I:\Dev Applications\personal_radar\documents` |
| 11 | PersonalRadar reçoit les données via **scan documentaire normal** (pas d’écriture directe en base PR) |
| 12 | Suppressions autorisées (après validation) : promotions inutiles ; scams/fakes avérés ; réseaux sociaux > 30 jours |
| 13 | Mails suspicieux incertains → **validation humaine** (`SUSPICIEUX_A_VALIDER`) |
| 14 | Hermès **prépare** les mails, ne les envoie **pas** automatiquement (V1) |
| 15 | **Damien** garde la validation finale (envoi, règles destructives, désabonnements) |

### Sécurité — 2026-06-27 (session security-by-design)

| # | Décision |
|---|----------|
| 16 | **Security-by-design obligatoire** — exigence transversale, pas une option |
| 17 | Données mail classées **sensibles** (SENSITIVE_PERSONAL / FINANCIAL_SENSITIVE) |
| 18 | Tokens OAuth classés **SECRET** — keyring/DPAPI, jamais Git/logs/rapports |
| 19 | **Pas de suppression définitive automatique en V1** |
| 20 | **Pas d’envoi automatique sensible en V1** |
| 21 | Logs et rapports réels **non committables** — redaction par défaut |
| 22 | Pièces jointes suspectes → **quarantaine** — pas d’exécution ni extraction PR sans validation |
| 23 | PersonalRadar reçoit uniquement documents **validés ou non suspects** via protocole documentaire |
| 24 | **Lecture seule par défaut** (`dry-run`) et permissions progressives |
| 25 | **Règle canonique** : en cas de doute → validation humaine, pas d’action destructive |

## Décisions ouvertes

| Sujet | Notes |
|-------|-------|
| Client mail final | Après tests réels Thunderbird Desktop + Android (Phase 1) |
| Format exact mail sans PJ | Préférence `.eml` + `.meta.json` — à confirmer sur cas réels |
| Ouverture nouveau courrier Thunderbird Windows | Méthode technique pour Hermès (URI, automation, API) |
| Stockage sécurisé des tokens OAuth | Keyring OS, DPAPI — spec dans [19](19_SECRETS_AND_TOKEN_STORAGE.md) ; impl Phase 2 bis |
| Structure finale dossiers `personal_radar\documents` | Alignement avec conventions PR existantes |
| Niveau suppression définitive future | Hors trash Gmail — politique à définir |
| Fréquence scans automatiques | Cron, déclenchement Hermès, événementiel |

## Historique

| Date | Événement |
|------|-----------|
| 2026-06-27 | Fondation documentaire repo (phase specs) |
| 2026-06-27 | Couche security-by-design (docs 17–21, security_policy) |

## Documents liés

- [Architecture](01_ARCHITECTURE_DECISIONS.md)
- [Sécurité — porte d’entrée](13_SECURITY_PRIVACY_AND_HUMAN_VALIDATION.md)
- [Modèle de menace](17_SECURITY_THREAT_MODEL.md)
- [Roadmap](15_IMPLEMENTATION_ROADMAP.md)
