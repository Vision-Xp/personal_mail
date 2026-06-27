# Modèle d’usage Windows et Android

## Windows

| Élément | Détail |
|---------|--------|
| Client | Thunderbird Desktop (candidat principal) ou client validé en Phase 1 |
| Comptes | Toutes les boîtes Gmail ajoutées via OAuth/IMAP |
| Organisation | Labels/dossiers **créés côté Gmail** par `personal_mail` — visibles après sync |
| Actions Damien | Lire, modifier, répondre, envoyer |
| Hermès | Peut préparer nouveau courrier ou brouillon (Windows) |
| Classement | `personal_mail` **ne dépend pas** de Thunderbird pour classer |

Thunderbird reflète Gmail ; il ne pilote pas la taxonomie.

## Android

| Élément | Détail |
|---------|--------|
| Client | Thunderbird Android (candidat principal) |
| Comptes | Mêmes boîtes Gmail |
| Organisation | Identique via synchronisation Gmail |
| Automatisation locale | **Aucune en V1** — pas de moteur Rust sur mobile |
| Objectif | Consultation propre et épurée |

## Expérience cible

Après organisation par `personal_mail` :

- Boîte moins bruyante
- Catégories propres et stables
- Mails importants (banque, admin, contrats) visibles rapidement
- Promotions utiles séparées des inutiles
- Scams supprimés ou en quarantaine
- Réseaux sociaux nettoyés (> 30 jours hors exceptions)
- Documents importants déjà extraits vers PersonalRadar

## Schéma

```
personal_mail (PC) ──► Gmail labels
                           │
           ┌───────────────┼───────────────┐
           ▼               ▼               ▼
    Thunderbird Win   Thunderbird Android   Gmail Web
           │               │
           └─────── Damien consulte / répond
```

## Documents liés

- [Choix client](02_CLIENT_MAIL_SELECTION.md)
- [Architecture](01_ARCHITECTURE_DECISIONS.md)
- [Compose](12_REPLY_AND_COMPOSE_WORKFLOW.md)
