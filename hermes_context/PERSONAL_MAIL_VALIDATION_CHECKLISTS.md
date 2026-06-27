# PERSONAL_MAIL — checklists de validation

## Checklist avant compte Gmail réel

- [ ] Repo propre (`git status` sans fichiers sensibles)
- [ ] Aucun secret dans le working tree
- [ ] OAuth compris — scopes minimaux documentés
- [ ] Compte **test** validé avant compte principal
- [ ] Dry-run OK sur compte test
- [ ] Thunderbird Desktop voit les labels Gmail créés
- [ ] Thunderbird Android voit les mêmes labels
- [ ] Stratégie tokens (keyring/DPAPI) décidée — voir docs/19
- [ ] `security_policy.local.yaml` en place (copie locale)
- [ ] Hermès context pack à jour (sync future)

## Checklist avant règle destructive

- [ ] Dry-run exécuté sur la règle
- [ ] Rapport dry-run lu intégralement
- [ ] Faux positifs vérifiés (mails sensibles dans la liste)
- [ ] Catégorie cible confirmée non sensible ou exceptions documentées
- [ ] Validation **Damien** explicite
- [ ] Rollback possible (trash/quarantaine, pas delete V1)
- [ ] Action journalisée (`action_id`, mode, compte)

## Checklist avant extraction PersonalRadar

- [ ] Document **non suspect** (extension, expéditeur, contexte)
- [ ] Classification confiance suffisante ou validation humaine
- [ ] Destination claire (`document_routes` / sous-dossier PR)
- [ ] Hash SHA-256 calculé et enregistré
- [ ] Sidecar `.meta.json` prévu
- [ ] Manifeste JSONL prévu si politique active
- [ ] Mail source traçable (`gmail_message_id`, `account_id`)
- [ ] Pas d’écriture si PJ dangereuse ou `SUSPICIEUX_A_VALIDER`

## Checklist avant préparation mail (compose-run)

- [ ] Destinataire vérifié (pas de phishing, domaine cohérent)
- [ ] Contexte vérifié (mail source, docs PR si pertinent)
- [ ] Pièces jointes vérifiées (pas de fichier dangereux)
- [ ] Ton adapté (poli, concis, juridiquement prudent)
- [ ] Validation **Damien** avant envoi
- [ ] **Pas d’envoi automatique** en V1
- [ ] Brouillon journalisé si possible (sans corps complet sensible en log)

## Checklist avant commit Git

- [ ] Pas de secret (token, `.env`, credentials)
- [ ] Pas de vraie donnée personnelle (mails, montants, noms réels)
- [ ] Pas de `.eml` réel
- [ ] Pas de rapport PII dans `reports/`
- [ ] `personal_radar` non modifié (si session touche l’écosystème)
- [ ] `git status` vérifié
- [ ] `hermes_context/` reste générique (pas de données opérationnelles réelles)

## Checklist avant sync Hermès (futur)

- [ ] Modifications commitées dans `personal_mail`
- [ ] Aucun secret dans `hermes_context/`
- [ ] Backup destination Hermès prévu (script futur)
- [ ] Rapport post-sync à valider

Voir [docs/23_HERMES_CONTEXT_SYNC_AND_INSTALL.md](../docs/23_HERMES_CONTEXT_SYNC_AND_INSTALL.md).
