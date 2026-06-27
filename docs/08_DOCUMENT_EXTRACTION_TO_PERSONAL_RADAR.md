# Extraction documentaire vers PersonalRadar

## Destination

```
I:\Dev Applications\personal_radar\documents
```

`personal_mail` **dépose des fichiers** dans cette arborescence. PersonalRadar les traite via son scan habituel. **Ne pas modifier** le dépôt `personal_radar` hors ajout de fichiers documentés.

## Routage par nature / contenu

| Domaine | Dossier cible (exemple) |
|---------|-------------------------|
| Banque | `Banque/` |
| Assurance | `Assurance/` |
| Énergie | `Energie/` |
| Achats | `Achats/` |
| Garanties | `Garanties/` |
| Contrats | `Contrats/` |
| Administratif | `Administratif/` |
| Santé | `Sante/` |
| Emploi | `Emploi/` |
| Abonnements | `Abonnements/` |
| Revenus | `Revenus/` |
| Sorties d’argent | `Sorties_Argent/` |

Voir [config/document_routes.example.yaml](../config/document_routes.example.yaml).

## Vérifications sécurité avant extraction

Avant tout dépôt vers PersonalRadar :

| Étape | Action |
|-------|--------|
| 1 | Vérifier extension / type MIME — voir [21](21_ATTACHMENT_SECURITY.md) |
| 2 | Vérifier cohérence expéditeur / catégorie attendue |
| 3 | Refuser ou mettre en quarantaine si fichier suspect |
| 4 | **Ne pas envoyer à PersonalRadar** un fichier dangereux ou non validé |
| 5 | Télécharger comme fichier **inerte** — jamais exécuter |
| 6 | Calculer hash SHA-256 avant écriture finale |
| 7 | Écrire sidecar `.meta.json` avec `action_log_id` |
| 8 | Journaliser en mode dry-run si simulation |

Si doute → `SUSPICIEUX_A_VALIDER` + alerte Hermès — pas d’extraction PR.

## Cas avec pièce jointe

Si la pièce jointe contient **toutes** les informations utiles et le corps du mail est redondant :

1. Extraire la pièce jointe
2. Renommer proprement (voir convention ci-dessous)
3. Classer dans le dossier cible
4. Créer métadonnées sidecar
5. Classer le mail côté Gmail (`DOCUMENTS_EXTRAITS` + catégorie métier)
6. **Ne pas** passer le mail en lu automatiquement en V1 — Damien le fait manuellement si souhaité

## Cas sans pièce jointe

Si le **corps** contient l’information importante :

1. Exporter le mail en format standard durable
2. Classer l’export dans `personal_radar\documents`
3. Classer le mail côté Gmail
4. Laisser Damien marquer lu manuellement

## Comparaison des formats

| Format | Avantages | Inconvénients |
|--------|-----------|---------------|
| `.eml` | Source brute standard, headers complets | Moins lisible humainement |
| `.html` | Lisible | Moins « preuve » que .eml |
| `.pdf` | Lecture figée pratique | Moins idéal comme source brute |
| `.md` + source | Bon résumé / index | Insuffisant seul si valeur juridique |
| `.meta.json` | Sidecar métadonnées | Complément, pas remplacement |

### Préférence provisoire

- **`.eml`** : source brute pour mail important sans pièce jointe
- **`.meta.json`** : sidecar obligatoire
- **`.md`** : résumé optionnel
- **`.pdf`** : seulement si besoin lecture humaine figée

## Convention de renommage

```
YYYY-MM-DD__organisme__type_document__montant_si_disponible__source.ext
```

Exemple fictif : `2026-06-27__ENGIE__facture__89-50EUR__gmail_personal_1.pdf`

## Métadonnées sidecar (`.meta.json`)

| Champ | Description |
|-------|-------------|
| `source_account_id` | Id compte Gmail |
| `gmail_message_id` | Id message |
| `gmail_thread_id` | Id thread |
| `received_at` | Date réception |
| `sender` | Expéditeur |
| `subject` | Objet |
| `detected_category` | Catégorie |
| `confidence` | Score |
| `extraction_type` | `attachment` \| `eml_export` \| etc. |
| `target_path` | Chemin final |
| `file_hash` | SHA-256 du fichier |
| `action_log_id` | Lien journal |

## Validation extraction

1. Contrôles sécurité (extension, expéditeur, suspicion) — voir ci-dessus
2. Fichier présent sur disque
3. Taille non nulle
4. Hash calculé et enregistré (intégrité + anti-doublon)
5. Lisibilité vérifiée si possible (PDF/texte) — sans exécuter le fichier
6. Métadonnées sidecar complètes
7. Action journalisée (`action_id`, mode, compte)
8. Entrée rapport d’extraction (local, non commité)

## Documents liés

- [Intégration PersonalRadar](09_PERSONAL_RADAR_INTEGRATION.md)
- [Sécurité pièces jointes](21_ATTACHMENT_SECURITY.md)
- [Logs et redaction](20_AUDIT_LOGGING_AND_REDACTION.md)
- [Tests](14_TEST_AND_VALIDATION_PLAN.md)
