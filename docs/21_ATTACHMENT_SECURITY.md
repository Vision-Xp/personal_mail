# Sécurité des pièces jointes

Une pièce jointe **n’est jamais fiable** uniquement parce qu’elle est jointe à un mail. Même un PDF « facture » peut être frauduleux ou piégé.

## 1. Risques

| Risque | Description |
|--------|-------------|
| Malware | Exécutable déguisé |
| Macro | Document Office malveillant |
| Script | `.js`, `.vbs`, `.ps1` |
| Archive piégée | `.zip` avec double extension ou exploit |
| Faux PDF | Phishing visuel, lien embarqué |
| Lien phishing | URL dans PDF/HTML |
| Facture frauduleuse | Usurpation organisme, IBAN tiers |
| Document usurpé | Logo banque, domaine expéditeur incohérent |

## 2. Extensions dangereuses — ne jamais exécuter / ne pas ouvrir auto

| Type | Extensions |
|------|------------|
| Exécutables | `.exe`, `.bat`, `.cmd`, `.ps1`, `.vbs`, `.js`, `.scr`, `.msi`, `.jar`, `.lnk` |
| Archives suspectes | `.zip`, `.rar`, `.7z` si origine inconnue ou expéditeur non attendu |
| Office macros | `.docm`, `.xlsm`, `.pptm` — et parfois `.doc`/`.xls` si expéditeur suspect |

Liste configurable dans [security_policy.example.yaml](../config/security_policy.example.yaml) (`quarantine_dangerous_extensions`).

## 3. Règles opérationnelles

| # | Règle |
|---|-------|
| 1 | Ne **jamais exécuter** une pièce jointe depuis `personal_mail` |
| 2 | Ne **pas ouvrir automatiquement** les fichiers à risque |
| 3 | Extraire uniquement comme **fichier inerte** sur disque |
| 4 | Calculer **hash SHA-256** avant et après écriture |
| 5 | En cas de doute → `SUSPICIEUX_A_VALIDER` — pas d’extraction vers PR |
| 6 | Ne **pas transmettre à PersonalRadar** un fichier dangereux ou non validé |
| 7 | Produire une **alerte Hermès** pour PJ suspecte |
| 8 | Journaliser extension, hash, décision — pas le contenu binaire |

## 4. PDF et factures

Avant extraction vers PR, vérifier :

| Contrôle | Action si échec |
|----------|-----------------|
| Cohérence expéditeur / domaine | `SUSPICIEUX_A_VALIDER` |
| Sujet et contexte (organisme attendu) | Review humaine |
| Organisme connu vs inconnu | Label + confiance réduite |
| Incohérence (ex. « ENGIE » depuis domaine inconnu) | Quarantaine |

Extraction PDF autorisée seulement si :

- Extension non dangereuse
- Expéditeur / règle de confiance ≥ seuil **ou** validation humaine
- Hash enregistré
- Pas de signal malware (taille anormale, type MIME incohérent — à implémenter)

## 5. Flux sécurisé d’extraction

```
PJ détectée
    ↓
Extension / MIME check ──danger──► SUSPICIEUX_A_VALIDER + alerte Hermès
    ↓ safe
Contexte expéditeur / règle ──doute──► validation humaine
    ↓ OK
Téléchargement binaire (pas d'exécution)
    ↓
Hash + écriture fichier inerte → personal_radar\documents
    ↓
Sidecar .meta.json + journal action_id
```

## Documents liés

- [Extraction PR](08_DOCUMENT_EXTRACTION_TO_PERSONAL_RADAR.md)
- [Modèle de menace](17_SECURITY_THREAT_MODEL.md)
- [Classification](06_CLASSIFICATION_RULES.md)
