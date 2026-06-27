# Intégration PersonalRadar

## Principe

```
personal_mail  →  fichiers dans personal_radar\documents  →  scan PersonalRadar normal
```

`personal_mail` **n’écrit pas** directement dans :

- La base de données PersonalRadar
- Les états internes ou caches PR
- Les rapports métier existants de PR
- Tout fichier métier non documenté de PR

PersonalRadar reste maître de son interprétation après scan.

## Sécurité de l’échange

| Règle | Détail |
|-------|--------|
| Protocole documentaire uniquement | Fichiers + manifeste optionnel — pas d’API interne PR |
| Interdiction écriture états internes | Base PR, caches, rapports métier PR — **interdit** en V1 |
| Manifeste sans secrets | Pas de token, mot de passe, ni refresh dans JSONL |
| Protection PII | Manifeste = PERSONAL_METADATA — fichier local, ignoré Git si réel |
| Fichiers validés uniquement | Pas de PJ suspecte / non validée vers PR — voir [21](21_ATTACHMENT_SECURITY.md) |
| Hash et traçabilité | Chaque document importé lié à `action_log_id` et `file_hash` |

Les documents extraits restent classés **FINANCIAL_SENSITIVE** ou **SENSITIVE_PERSONAL** — jamais dans le repo `personal_mail`.

## Données transmissibles (via documents + manifeste)

- Facture, échéance, contrat, abonnement
- Revenu, remboursement
- Preuve d’achat, garantie
- Promotion utile (archivage)
- Changement tarifaire, résiliation
- Confirmation de souscription ou de rendez-vous

## Manifeste entrant (optionnel)

Chemin proposé :

```
I:\Dev Applications\personal_radar\documents\_incoming_mail_manifest.jsonl
```

Chaque ligne JSONL (exemple de champs) :

```json
{
  "event_id": "uuid-example",
  "created_at": "2026-06-27T12:00:00Z",
  "source_project": "personal_mail",
  "source_account_id": "gmail_personal_1",
  "gmail_message_id": "msg_fictif",
  "sender": "example@engie.fr",
  "subject": "Example subject",
  "document_path": "Energie/2026-06-27__ENGIE__facture__example.pdf",
  "document_type": "invoice",
  "category": "ENERGIE",
  "confidence": 0.91,
  "recommended_personal_radar_action": "detect_due_date"
}
```

Le manifeste est un **hint** pour PR ou pour audits Hermès — pas un contrat d’API interne PR tant que PR n’est pas modifié. **Ne jamais y inclure de secrets** (tokens, credentials).

## Alertes possibles (côté PR après scan)

- Nouvelle facture ou échéance
- Renouvellement contrat / abonnement
- Hausse tarifaire
- Opportunité d’économie (promo utile archivée)
- Document manquant attendu
- Réponse recommandée
- Garantie à conserver

## Limites V1

- Pas de callback PR → personal_mail
- Pas de modification des règles PR
- Structure fine des sous-dossiers `documents/` : décision ouverte (voir [16_DECISION_LOG](16_DECISION_LOG.md))

## Documents liés

- [Extraction](08_DOCUMENT_EXTRACTION_TO_PERSONAL_RADAR.md)
- [Architecture](01_ARCHITECTURE_DECISIONS.md)
- [Classification données](18_DATA_CLASSIFICATION_AND_RETENTION.md)
- [config/document_routes.example.yaml](../config/document_routes.example.yaml)
- [config/security_policy.example.yaml](../config/security_policy.example.yaml)
