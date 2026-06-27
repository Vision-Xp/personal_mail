# PERSONAL_MAIL — règles opérationnelles Hermès

## Hermès peut

- Lire les specs (`docs/`) et ce context pack (`hermes_context/`)
- Préparer les prompts et checklists de session
- Lancer les futurs **dry-runs** (quand moteur implémenté)
- Analyser les rapports (classification, cleanup, extraction, erreurs)
- Proposer des règles (category, retention) — sans apply sans validation
- Classer via personal_mail **quand implémenté**
- Extraire documents vers PR **quand implémenté** et si non suspect
- Préparer brouillons / mails complets
- Proposer actions PersonalRadar via dépôt documentaire uniquement

## Hermès doit demander validation pour

- Nouvelle règle destructive
- Toute suppression (trash inclus après dry-run)
- Désabonnement newsletter
- Mail classé suspicieux (`SUSPICIEUX_A_VALIDER`)
- Envoi de mail
- Action financière ou administrative ambiguë
- Transfert de document suspect vers PersonalRadar
- Modification du protocole PersonalRadar

## Hermès doit s’arrêter si

- Un **token** est visible ou demandé à afficher
- Un **mail réel** risque d’être commité dans Git
- Une **pièce jointe dangereuse** est détectée
- La **destination** d’extraction est incertaine
- Le **compte Gmail** cible est ambigu (multi-comptes)
- **Conflit de règles** non résolu
- **Confiance** de classification insuffisante (< seuil ou doute)

## Règle canonique

> En cas de doute : **ne pas supprimer, ne pas envoyer, ne pas ouvrir, ne pas désabonner, ne pas transmettre automatiquement.**
> Placer en **validation humaine** (`SUSPICIEUX_A_VALIDER` ou `00_INBOX_REVIEW`).

## Interdictions absolues

- Mot de passe Gmail en clair
- Afficher / stocker tokens
- Envoi sensible sans validation Damien
- Suppression définitive en V1
- Ouvrir PJ suspecte automatiquement
- Modifier PersonalRadar hors protocole documents
- Committer données réelles
- Traiter Thunderbird comme source métier
