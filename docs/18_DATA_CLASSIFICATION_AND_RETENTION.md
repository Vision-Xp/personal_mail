# Classification des données et rétention

Toutes les données traitées par `personal_mail` sont classées par niveau de sensibilité. Les règles ci-dessous s’appliquent au dépôt Git, aux logs, aux rapports, au chiffrement local et à la durée de conservation.

## Niveaux de classification

### PUBLIC_OR_DOCS_ONLY

**Exemples** : specs Markdown versionnées, README, exemples YAML fictifs, fixtures synthétiques sans PII.

| Règle | Valeur |
|-------|--------|
| Commit Git | ✅ Autorisé |
| Loggé en clair | ✅ Oui |
| Redaction | Non requise |
| Chiffrement local | Non requis |
| Conservation | Durée vie du repo |
| Export | Libre |
| Suppression | N/A (versionné) |

### INTERNAL_CONFIG

**Exemples** : règles locales (`*.local.yaml`), taxonomie active, profils de classification sans données réelles embarquées.

| Règle | Valeur |
|-------|--------|
| Commit Git | ❌ Fichiers locaux — `.gitignore` |
| Loggé en clair | ⚠️ Partiel (pas de PII embarquée) |
| Redaction | Si partage rapport |
| Chiffrement local | Recommandé si chemins réels |
| Conservation | Tant que compte actif |
| Export | Local uniquement |
| Suppression | À la désactivation compte |

### PERSONAL_METADATA

**Exemples** : expéditeur, sujet, date, compte, label, `message_id`, chemin local, hash fichier.

| Règle | Valeur |
|-------|--------|
| Commit Git | ❌ Interdit (rapports, logs réels) |
| Loggé en clair | ⚠️ Logs locaux complets ; masquer si rapport partageable |
| Redaction | Adresses mail partielles (`d***@domain`) si export |
| Chiffrement local | Recommandé sur disque sensible |
| Conservation | Journaux : rotation définie (ex. 90 j–1 an) |
| Export | Rapport local complet uniquement |
| Suppression | Après rotation log |

### SENSITIVE_PERSONAL

**Exemples** : corps de mail personnel, documents administratifs, contrats, preuves d’achat, emploi, rendez-vous, santé (hors financier pur).

| Règle | Valeur |
|-------|--------|
| Commit Git | ❌ Strictement interdit |
| Loggé en clair | ❌ Corps mail jamais par défaut |
| Redaction | Sujets limités ; pas de corps dans rapports partageables |
| Chiffrement local | Recommandé (BitLocker / dossier protégé) |
| Conservation | Selon règles métier Gmail + extraction PR |
| Export | `.eml` / fichiers vers PR uniquement |
| Suppression | Trash Gmail après validation — pas delete V1 |

### FINANCIAL_SENSITIVE

**Exemples** : banque, assurances, factures, échéanciers, revenus, abonnements, remboursements, données de paiement.

| Règle | Valeur |
|-------|--------|
| Commit Git | ❌ Strictement interdit |
| Loggé en clair | ❌ Montants, IBAN masqués par défaut |
| Redaction | IBAN/RIB, montants, n° contrat si rapport non local |
| Chiffrement local | Fortement recommandé |
| Conservation | Longue durée — alignée obligations légales |
| Export | PR `documents/` + sidecar `.meta.json` |
| Suppression | Quarantaine + validation humaine |

### SECRET

**Exemples** : tokens OAuth, refresh tokens, credentials, clés API, secrets client OAuth.

| Règle | Valeur |
|-------|--------|
| Commit Git | ❌ **Jamais** |
| Loggé en clair | ❌ **Jamais** |
| Redaction | Toujours `[REDACTED]` |
| Chiffrement local | **Obligatoire** (keyring / DPAPI) |
| Conservation | Jusqu’à révocation ou rotation |
| Export | ❌ Interdit |
| Suppression | Révocation Google + purge locale |

## Règles transversales

| Règle | Détail |
|-------|--------|
| Aucune donnée réelle dans Git | Comptes, mails, montants, noms réels |
| Aucun vrai `.eml` dans Git | `.gitignore` `*.eml` |
| Aucun rapport PII dans Git | `reports/**/*.json`, etc. |
| Logs masquent PII si nécessaire | Adresses, sujets sensibles, montants |
| Tokens toujours SECRET | Voir [19](19_SECRETS_AND_TOKEN_STORAGE.md) |
| Documents extraits hors repo | Uniquement dans `personal_radar\documents` |
| Fixtures de test | Niveau PUBLIC_OR_DOCS_ONLY — synthétiques uniquement |
| Séparation fixtures / réel | Dossiers distincts : `real_mail_samples/` ignoré Git |

## Séparation données réelles vs test

```
personal_mail repo (Git)     → specs, exemples, fixtures synthétiques
config/*.local.yaml (local)  → règles réelles, ignoré Git
logs/, reports/ (local)      → opérationnel, ignoré Git
personal_radar\documents     → documents extraits réels, hors repo PM
```

## Documents liés

- [Modèle de menace](17_SECURITY_THREAT_MODEL.md)
- [Secrets et tokens](19_SECRETS_AND_TOKEN_STORAGE.md)
- [Logs et redaction](20_AUDIT_LOGGING_AND_REDACTION.md)
- [Rétention métier](07_RETENTION_AND_DELETION_RULES.md)
