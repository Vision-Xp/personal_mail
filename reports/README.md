# Rapports

Ce dossier accueillera les rapports produits par `personal_mail` et Hermès lors de l’implémentation.

## Versionnement Git

- Les **rapports réels ne doivent pas être commités** s’ils contiennent des données personnelles (adresses, sujets, corps de mails, pièces jointes, montants, etc.).
- Seuls les **README** (et éventuellement `.gitkeep`) sont versionnés dans ce dépôt.
- Les patterns `reports/**/*.json`, `*.jsonl`, `*.csv`, `*.html`, `*.pdf`, `*.eml`, `*.txt` sont ignorés par [`.gitignore`](../.gitignore).

## Types de rapports

| Type | Dossier | Description |
|------|---------|-------------|
| Validation | [validation/](validation/) | Rapports GO / GO limité / NO GO, revues humaines |
| Audits newsletters | [newsletter_audits/](newsletter_audits/) | Listes garder / revoir / désabonner |
| Nettoyage | [cleanup/](cleanup/) | Dry-run et apply des suppressions validées |
| Dry-run | (racine ou sous-dossiers) | Simulations sans action destructive |
| Extraction | (racine ou sous-dossiers) | Fichiers extraits, hash, erreurs |
| Classification | (racine ou sous-dossiers) | Scores de confiance, catégories proposées |
| Erreurs | (racine ou sous-dossiers) | Échecs API, OAuth, I/O |

Voir [docs/10_HERMES_OPERATING_PROTOCOL.md](../docs/10_HERMES_OPERATING_PROTOCOL.md) et [docs/14_TEST_AND_VALIDATION_PLAN.md](../docs/14_TEST_AND_VALIDATION_PLAN.md).
