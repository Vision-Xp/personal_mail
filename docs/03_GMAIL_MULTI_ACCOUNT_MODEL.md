# Modèle multi-comptes Gmail

## Vue d’ensemble

`personal_mail` gère **plusieurs comptes Gmail** en parallèle. Chaque compte est une entité distincte avec son autorisation OAuth, ses journaux et son profil de règles, tout en partageant des règles globales lorsque pertinent.

## Par compte

| Aspect | Description |
|--------|-------------|
| OAuth | Un flux d’autorisation par compte — pas de mot de passe en clair |
| Activation | Chaque compte peut être `enabled` / désactivé indépendamment |
| Règles globales | Scams, social > 30 jours, newsletters, promotions, documents |
| Règles spécifiques | Surcharge ou complément selon le profil du compte |
| Labels communs | Taxonomie partagée (ex. `BANQUE`, `ADMINISTRATIF`) |
| Exceptions | Booking musical, Dryard, alertes sécurité, etc. |
| Journaux | Actions tracées par `account_id` |
| Dernière analyse | Horodatage / curseur de sync pour reprise |

## Exemples de comptes (fictifs)

| Profil | Usage typique | Exemple id |
|--------|---------------|------------|
| Perso | Banque, assurance, administratif, santé, achats | `gmail_personal_1` |
| Musique / Dryard | Booking, opportunités, plateformes, promo musique | `gmail_music_1` |
| Services / outils | GitHub, OpenAI, Cursor, factures SaaS | `gmail_tools_1` |
| Autre | Compte dédié futur | `gmail_*` |

Voir [config/gmail_accounts.example.yaml](../config/gmail_accounts.example.yaml) — **aucune donnée réelle dans Git**.

## Règles globales (tous comptes)

- Détection scams / phishing patterns
- Réseaux sociaux : rétention 30 jours (avec exceptions)
- Newsletters : classement + audit périodique
- Promotions utiles vs inutiles
- Documents importants : extraction vers PersonalRadar
- Factures, contrats, garanties, abonnements (signaux communs)

## Règles spécifiques par profil

### Compte perso

- Banque (Crédit Agricole, Revolut, Fortuneo, Trade Republic)
- Assurance (auto, habitation, santé)
- Administratif (impôts, CPAM, CAF, employeur)
- Santé, rendez-vous, confirmations
- Achats, preuves, garanties

### Compte musique

- Booking et dates de concert
- Opportunités professionnelles
- Plateformes (SoundCloud, etc.)
- Promo musique utile
- Réseaux sociaux avec exceptions booking / Dryard / Uncloned

### Compte outils / dev

- GitHub, notifications CI
- OpenAI, Cursor, services IA
- Factures SaaS et abonnements outils

## Exigences d’audit

- Chaque compte **auditable indépendamment** (rapports filtrés par `account_id`).
- Aucune donnée réelle dans le dépôt Git.
- Désactivation d’un compte sans impact sur les autres (sauf règles globales désactivées explicitement).

## Documents liés

- [OAuth / API](04_GMAIL_OAUTH_IMAP_API_MODEL.md)
- [Classification](06_CLASSIFICATION_RULES.md)
- [Hermès](10_HERMES_OPERATING_PROTOCOL.md)
