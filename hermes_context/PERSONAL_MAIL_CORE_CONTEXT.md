# PERSONAL_MAIL — contexte cœur (Hermès)

## Projet

**personal_mail** — cerveau mail intelligent Rust-first, pilotable par Hermès.

## But

Organiser plusieurs boîtes Gmail, réduire le bruit, isoler les risques, extraire les documents importants, alimenter PersonalRadar et préparer des mails — **toujours avec validation humaine pour le sensible**.

## Architecture canonique

| Composant | Rôle |
|-----------|------|
| **Gmail** | Source de vérité serveur (messages, threads, labels, états) |
| **personal_mail** | Cerveau Rust (classification, règles, extraction, journaux) |
| **Hermès** | Opérateur / orchestrateur |
| **Thunderbird** (Windows + Android) | Cockpit humain — lecture, réponse, envoi |
| **PersonalRadar** | Destination documentaire + analyse via scan normal |

## Règle essentielle

**personal_mail pilote Gmail**, pas Thunderbird comme base métier.

Thunderbird **affiche** l’organisation synchronisée depuis Gmail. Ne jamais classer ou supprimer en ne modifiant que Thunderbird.

## Destination documents

```
I:\Dev Applications\personal_radar\documents
```

Dépôt fichier uniquement — pas d’écriture directe dans la base interne PersonalRadar.

## Mode V1

| Règle | Valeur |
|-------|--------|
| Mode par défaut | **dry-run** (analyse seulement) |
| Suppression définitive | **Interdite** |
| Envoi automatique sensible | **Interdit** |
| Ambigu / sensible | **Validation humaine** (Damien) |

## Phase actuelle

**SPECIFICATION PHASE — NO REAL MAIL ACTION YET**

Pas de moteur Rust, pas de Gmail réel, pas de tokens.

## Références repo

- Specs : `docs/00` à `docs/23`
- Sécurité : `docs/13`, `docs/17`–`21`
- Config exemples : `config/*.example.yaml`
