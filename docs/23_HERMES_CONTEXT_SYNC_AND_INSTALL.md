# Synchronisation et installation du contexte Hermès

> **Phase actuelle** : documentation uniquement. Aucun script n’est créé ni exécuté dans cette session. Aucun fichier n’est copié vers le dossier Hermès local.

## Objectif

Permettre plus tard de **régénérer proprement** le contexte opérationnel Hermès depuis le repo `personal_mail`, sans dupliquer toute la documentation `docs/`.

## Chemins

| Rôle | Chemin |
|------|--------|
| **Source canonique** | `I:\Dev Applications\personal_mail\hermes_context\` |
| **Destination probable** | `C:\Users\SMAD Inc\AppData\Local\hermes\` (ou sous-dossier dédié `personal_mail\`) |

La structure exacte côté Hermès sera confirmée lors de l’implémentation Phase 7.

## Flux futur (documenté, non exécuté)

```
1. Modifier les fichiers dans personal_mail/hermes_context/
2. Commit dans Git (personal_mail)
3. Lancer un script de sync contrôlé (futur)
4. Le script sauvegarde les anciens fichiers Hermès (timestamp)
5. Le script copie les nouveaux fichiers depuis hermes_context/
6. Hermès relit son contexte au prochain démarrage / session
7. Rapport de validation (fichiers copiés, backup path, erreurs)
```

## Script futur (roadmap uniquement)

Nom proposé : `scripts/sync_hermes_context.ps1`

**Non créé en phase specs.** Responsabilités prévues :

| Étape | Action |
|-------|--------|
| Pré-vol | Vérifier que la source `hermes_context/` existe |
| Pré-vol | Vérifier que la destination Hermès existe (ou demander création) |
| Backup | Copier l’ancien contexte vers `hermes_backup_YYYYMMDD_HHMMSS/` |
| Sync | Copier uniquement les fichiers Markdown du pack (liste blanche) |
| Sécurité | Refuser de copier secrets, tokens, `.eml`, rapports, configs locales |
| Rapport | Lister fichiers copiés, ignorés, erreurs |
| Post | Afficher rappel : relire contexte Hermès, valider GO/NO GO |

Paramètres envisagés :

```powershell
# Exemple futur — NE PAS EXÉCUTER MAINTENANT
# .\scripts\sync_hermes_context.ps1 -Source "I:\Dev Applications\personal_mail\hermes_context" `
#   -Destination "C:\Users\SMAD Inc\AppData\Local\hermes\personal_mail" -WhatIf
```

## Validations obligatoires (futur script)

- [ ] Répertoire source existe et contient les fichiers attendus
- [ ] Répertoire destination existe ou est créé explicitement
- [ ] Backup effectué avant tout écrasement
- [ ] Aucun fichier hors liste blanche copié
- [ ] Aucun secret, token, mail réel, rapport PII, document extrait
- [ ] Rapport généré (local, non commité si contient chemins machine)
- [ ] Liste des fichiers copiés affichée à l’utilisateur

## Règle de contenu

**Aucun** des éléments suivants ne doit entrer dans le contexte Hermès synchronisé :

- Secrets, tokens OAuth, credentials
- Mails réels, `.eml`, pièces jointes
- Rapports contenant des PII
- Documents extraits vers PersonalRadar
- Fichiers `config/*.local.yaml`
- Contenu de `logs/`, `reports/`, `tokens/`

Seuls les fichiers **PUBLIC_OR_DOCS_ONLY** de `hermes_context/` sont éligibles.

## Installation initiale (futur)

1. Cloner / mettre à jour le repo `personal_mail`
2. Lire `docs/22` et `hermes_context/README.md`
3. Exécuter le script de sync (quand disponible) ou copie manuelle contrôlée
4. Valider avec [PERSONAL_MAIL_VALIDATION_CHECKLISTS.md](../hermes_context/PERSONAL_MAIL_VALIDATION_CHECKLISTS.md)
5. Ne pas connecter Gmail avant Phase 3 checklist complète

## Documents liés

- [Hermès skill et context pack](22_HERMES_SKILL_AND_CONTEXT_PACK.md)
- [Roadmap Phase 7](15_IMPLEMENTATION_ROADMAP.md)
- [Décision log](16_DECISION_LOG.md)
