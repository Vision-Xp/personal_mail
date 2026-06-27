# Vision produit — personal_mail

## Résumé

`personal_mail` vise à transformer plusieurs boîtes Gmail bruyantes en un système mail propre, sûr et exploitable : organisation automatique côté Gmail, consultation unifiée via Thunderbird, documents importants rangés dans PersonalRadar, et aide à la rédaction pilotée par Hermès.

## Problèmes adressés

### Surcharge mail

Des dizaines ou centaines de messages non lus mélangent l’important (banque, impôts, contrats) et le bruit (promotions, notifications sociales). La charge mentale pour « retrouver le bon mail » devient élevée.

### Promotions inutiles

Les offres commerciales génériques encombrent la boîte sans valeur réelle, masquant les promotions réellement utiles (économie, renégociation, abonnements existants).

### Scams et phishing

Les tentatives de fraude et les faux expéditeurs créent un risque sécurité et une anxiété. Les cas incertains doivent être isolés sans action aveugle.

### Documents importants dispersés

Factures, garanties, preuves d’achat et courriers administratifs restent noyés dans le fil mail au lieu d’être archivés de façon durable et analysables.

### Informations financières perdues

Revenus, sorties d’argent, échéances et changements tarifaires ne sont pas systématiquement reliés au reste de l’écosystème documentaire (PersonalRadar).

### Répondre plus facilement

Les réponses administratives, relances, résiliations et demandes bancaires demandent du temps et du contexte — Hermès doit pouvoir préparer un brouillon complet que Damien valide avant envoi.

## Objectifs

| Objectif | Description |
|----------|-------------|
| Organiser toutes les boîtes Gmail | Labels cohérents, multi-comptes |
| Supprimer le bruit | Promotions inutiles, doublons, social > 30 jours (après validation) |
| Isoler les risques | Quarantaine, `SUSPICIEUX_A_VALIDER`, scams avérés traités |
| Extraire les documents importants | Pièces jointes et mails exportés vers PersonalRadar |
| Alimenter PersonalRadar | Scan documentaire normal, pas d’écriture directe en base |
| Faciliter la rédaction | Hermès prépare, Damien modifie et envoie |
| Consulter proprement | Thunderbird Windows + Android synchronisés sur Gmail |

## Réduction de la charge mentale

L’utilisateur ne doit plus « trier manuellement » chaque flux : le cerveau Rust applique des règles validées, journalise, et laisse une boîte lisible avec des catégories stables. Les actions sensibles restent sous contrôle humain.

## Connexion au flux PersonalRadar

Les documents extraits alimentent `I:\Dev Applications\personal_radar\documents`. PersonalRadar les indexe via sa toolchain habituelle — échéances, contrats et alertes deviennent exploitables sans dupliquer la logique métier de PersonalRadar dans `personal_mail`.

## Non-objectifs V1

- Pas d’envoi automatique de mails sensibles.
- Pas de suppression définitive non journalisée.
- Pas de stockage de mots de passe en clair.
- Pas de remplacement complet de Gmail (Gmail reste la source serveur).
- Pas de manipulation de vrais comptes pendant la phase specs.
- Pas d’écriture directe dans les données internes PersonalRadar.

## Documents liés

- [Architecture](01_ARCHITECTURE_DECISIONS.md)
- [Taxonomie](05_CATEGORY_TAXONOMY.md)
- [Roadmap](15_IMPLEMENTATION_ROADMAP.md)
- [Journal des décisions](16_DECISION_LOG.md)
