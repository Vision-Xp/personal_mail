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

1. Fichier présent sur disque
2. Taille non nulle
3. Hash calculé et enregistré
4. Lisibilité vérifiée si possible (PDF/texte)
5. Action journalisée
6. Entrée rapport d’extraction

## Documents liés

- [Intégration PersonalRadar](09_PERSONAL_RADAR_INTEGRATION.md)
- [Tests](14_TEST_AND_VALIDATION_PLAN.md)
