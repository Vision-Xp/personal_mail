# Workflow réponses et composition

## Flux général

```
1. Hermès détecte ou reçoit une demande
2. Hermès analyse le contexte (mail source, docs PR, situation, destinataire, objectif)
3. Hermès propose une intention
4. Hermès rédige un mail complet
5. Hermès prépare brouillon / nouveau courrier (Windows, Thunderbird si possible)
6. Damien modifie
7. Damien envoie
```

**V1** : pas d’envoi automatique pour mails sensibles. Validation humaine obligatoire.

## Cas documentés

| Cas | Objectif typique |
|-----|------------------|
| Résiliation contrat | Fin abonnement / service |
| Demande au banquier | Opération, justificatif, contestation |
| Courrier avant échéance | Rappel paiement ou renégociation |
| Demande de justificatif | Pièce manquante admin/banque |
| Demande de remboursement | SAV, trop-perçu |
| Contestation | Facture, prélèvement, erreur |
| Relance | Sans réponse d’un organisme |
| Prise de rendez-vous | Admin, médical, pro |
| Confirmation | RDV, réception documents |
| Réponse administrative | CPAM, impôts, employeur |
| Réponse professionnelle | Booking, partenaires |
| Demande d’information | Clarification contrat ou facture |

## Champs du brouillon

- Destinataire (`To`)
- Copie (`Cc`)
- Copie cachée (`Bcc`) si pertinent
- Objet
- Corps (texte + mise en forme si supportée)
- Pièces jointes (chemins PR ou fichiers locaux)
- Références utiles (n° dossier, facture, date échéance)

## Ton

- Clair, poli, ferme si nécessaire
- Adapté au destinataire (banque vs admin vs pro)
- Concis — pas de remplissage
- Sans agressivité inutile
- Juridiquement prudent (pas d’aveu ou engagement non voulu)

## Sécurité

| Règle | Détail |
|-------|--------|
| Validation humaine | Obligatoire avant envoi |
| Pas d’envoi auto sensible V1 | Hermès s’arrête au brouillon |
| Journalisation | Brouillons préparés tracés si possible (sans corps complet en log si sensible) |
| Contexte PR | Hermès peut s’appuyer sur documents indexés — pas de fuite de secrets dans le dépôt Git |

## Documents liés

- [Hermès](10_HERMES_OPERATING_PROTOCOL.md)
- [Sécurité](13_SECURITY_PRIVACY_AND_HUMAN_VALIDATION.md)
- [Décision log](16_DECISION_LOG.md) — méthode exacte Thunderbird compose : ouverte
