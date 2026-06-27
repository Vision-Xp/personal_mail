# Plan de tests et validation

## Tests sans vrais comptes (phase actuelle et CI future)

| Artefact | Usage |
|----------|--------|
| Fixtures mails synthétiques | JSON / structures message factices |
| Messages simulés | Expéditeurs, sujets, corps inventés |
| Attachments factices | PDF/texte générés, pas de données réelles |
| Comptes fictifs | `example.*@gmail.com` dans config exemple |
| Rapports fictifs | Templates sans PII |

## Tests fonctionnels cibles

| # | Scénario | Résultat attendu |
|---|----------|------------------|
| 1 | Classification banque (CA, Revolut, etc.) | Label `BANQUE` + sous-cat |
| 2 | Classification assurance | `ASSURANCES` |
| 3 | Classification énergie (ENGIE) | `ENERGIE` |
| 4 | Classification revenu | `REVENUS` |
| 5 | Classification sortie d’argent | `SORTIES_ARGENT` |
| 6 | Réseau social | `RESEAUX_SOCIAUX` |
| 7 | Réseau social > 30 jours | Candidat trash (dry-run) |
| 8 | Promo utile | `PROMOTIONS_UTILES` |
| 9 | Promo inutile | `PROMOTIONS_INUTILES` |
| 10 | Newsletter | `NEWSLETTERS` |
| 11 | Scam avéré | `SCAM_AVERE` |
| 12 | Suspicieux | `SUSPICIEUX_A_VALIDER` |
| 13 | Pièce jointe facture | Extraction + sidecar |
| 14 | Mail sans PJ important | Export `.eml` |
| 15 | Sidecar `.meta.json` | Champs complets |
| 16 | Manifeste PersonalRadar | Ligne JSONL valide |
| 17 | Dry-run suppression | Rapport sans mutation |
| 18 | Safe-run labels | Labels appliqués, pas de trash |
| 19 | Rapport final validation | GO / NO GO lisible |

## Tests sécurité

| # | Scénario | Résultat attendu |
|---|----------|------------------|
| S1 | Audit repo — aucun secret | `git grep` / scan : pas de token, `.env`, clé |
| S2 | Aucun vrai `.eml` versionné | `.gitignore` + working tree clean |
| S3 | Token absent des logs | Logs test sans pattern token OAuth |
| S4 | Dry-run avant suppression | Apply trash refusé sans dry-run préalable validé |
| S5 | PJ dangereuse (`.exe`, etc.) | Quarantaine `SUSPICIEUX_A_VALIDER`, pas d’extraction PR |
| S6 | Rapport redacted | Version partageable sans IBAN, token, corps mail |
| S7 | Compte Gmail test uniquement | Premier run réel ≠ boîte perso principale |
| S8 | Action ambiguë | Demande validation humaine, pas d’auto-apply |
| S9 | Fichier suspect vers PR | Bloqué ou validation requise |
| S10 | security_policy chargée | `default_mode: dry-run`, `allow_permanent_delete_v1: false` |
| S11 | Manifeste sans secrets | JSONL sans token ni credential |
| S12 | Hash extraction | SHA-256 présent dans sidecar et log |

## Validation réelle future (compte Gmail test)

Checklist :

- [ ] Compte Gmail test dédié (pas boîte perso principale en premier run)
- [ ] OAuth OK, scopes minimaux
- [ ] Labels créés via API visibles Gmail Web
- [ ] Thunderbird Windows voit les labels
- [ ] Thunderbird Android voit les labels
- [ ] Extraction document OK + hash
- [ ] Manifeste JSONL OK
- [ ] PersonalRadar scan OK sur fichier déposé
- [ ] Aucun secret dans Git
- [ ] Tests sécurité S1–S12 passés
- [ ] Rapport final : **GO** / **GO limité** / **NO GO**

## Critères GO

- Aucune action destructive non validée exécutée
- Labels visibles sur les clients cibles
- Extraction vérifiée (fichier + hash + sidecar)
- Rapports lisibles et reproductibles
- Aucune donnée sensible commitée
- Thunderbird reflète Gmail correctement (pas l’inverse)

## Critères NO GO

- Suppression ou envoi non validé
- Labels non synchronisés
- Extraction incomplète ou hash manquant
- Fuite de PII dans Git ou rapports versionnés
- Token ou secret détecté dans repo, logs ou rapport commité
- PJ dangereuse extraite vers PR sans validation

## Documents liés

- [Roadmap](15_IMPLEMENTATION_ROADMAP.md)
- [Modèle de menace](17_SECURITY_THREAT_MODEL.md)
- [reports/validation/](../reports/validation/)
