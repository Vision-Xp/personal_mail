# Décisions d’architecture

## Principes fondateurs

### 1. Rust-first pour le moteur

Le cerveau `personal_mail` sera implémenté en Rust pour robustesse, performance, sécurité mémoire et maintenabilité à long terme. Hermès et les scripts d’exploitation s’appuient sur ce binaire/CLI.

### 2. Gmail comme source de vérité

Messages, threads, labels, lu/non lu, corbeille, spam, classement et quarantaine vivent **côté Gmail**. Toute action métier canonique passe par l’API Gmail (ou équivalent serveur), pas par une copie locale Thunderbird.

### 3. Thunderbird comme cockpit humain

Thunderbird Desktop (Windows) et Thunderbird Android servent à **consulter, lire, répondre et envoyer**. Thunderbird **n’est pas une base métier** : il affiche l’organisation créée sur Gmail via synchronisation IMAP/OAuth.

### 4. Hermès comme opérateur

Hermès configure, lance dry-run, lit rapports, propose règles, extrait documents, prépare brouillons et communique avec PersonalRadar via dépôt de fichiers — sans contourner la validation humaine pour les actions sensibles.

### 5. PersonalRadar via ajout documentaire

Les fichiers vont dans `personal_radar\documents`. PersonalRadar scanne ensuite. **Pas d’écriture directe** dans sa base, ses états internes ou ses rapports métier.

### 6. Multi-comptes Gmail natif

Chaque compte a son OAuth, ses journaux et peut combiner règles globales et spécifiques.

### 7. Labels Gmail comme organisation durable

Les dossiers/labels sont **créés et maintenus sur Gmail** pour être visibles sur tous les clients synchronisés.

### 8. Journaux obligatoires

Chaque action (compte, message id, confiance, mode dry-run/safe/apply) est journalisée pour audit et restauration.

### 9. Dry-run obligatoire avant règle destructive

Toute nouvelle règle de suppression produit d’abord un rapport sans effet.

### 10. Quarantaine pour l’ambigu

Cas incertains → label/quarantaine (`SUSPICIEUX_A_VALIDER`), pas de suppression aveugle.

### 11. Validation humaine pour actions sensibles

Envoi, désabonnement, suppression définitive future, règles destructives nouvelles, ambiguïté financière/administrative.

### 12. Security-by-design obligatoire

Le système manipule des données **SENSITIVE_PERSONAL** et **FINANCIAL_SENSITIVE** (mails, pièces jointes, documents PR). La sécurité n’est pas une couche ajoutée en fin de projet : elle structure OAuth, stockage, logs, extraction, tests et permissions dès la conception. Voir [17](17_SECURITY_THREAT_MODEL.md) à [21](21_ATTACHMENT_SECURITY.md).

| Exigence | V1 |
|----------|-----|
| Lecture seule par défaut au démarrage | `default_mode: dry-run` |
| Permissions progressives | read → labels → extract → trash contrôlé |
| Tokens protégés (keyring / DPAPI) | Pas de fichier plat en prod |
| Logs expurgés | Pas de corps mail ni token en clair |
| Suppression définitive automatique | **Interdite** |
| Envoi automatique sensible | **Interdit** |

## Schéma cible

```
Plusieurs boîtes Gmail
        ↓
personal_mail (Rust)
        ↓
Organisation côté Gmail :
  labels, classement, nettoyage, extraction, quarantaine, journaux
        ↓
Thunderbird Windows / Android
        ↓
Damien consulte, lit, répond, envoie
        │
        └── (parallèle) extraction → personal_radar\documents → PersonalRadar scan
```

Flux texte :

```
Gmail accounts → personal_mail Rust → Gmail labels/actions → Thunderbird → Damien
                                      ↓
                           personal_radar\documents
```

## Voie canonique unique

| Besoin | Voie canonique | À éviter |
|--------|----------------|----------|
| Classer un mail | Label Gmail via API | Déplacer uniquement dans Thunderbird |
| Marquer lu/non lu | Gmail | État local Thunderbird seul |
| Supprimer / corbeille | Gmail (après dry-run) | Suppression locale IMAP désynchronisée |
| Extraire document | Fichier → `personal_radar\documents` | Copie manuelle non journalisée |
| Préparer réponse | Brouillon Thunderbird / compose Hermès | Envoi API sans validation |

**Ne pas dupliquer les actions** entre Gmail et Thunderbird. Si plusieurs chemins existent, **un seul** est canonique (Gmail API pour le métier ; Thunderbird pour l’humain).

## Matrice avantages / risques

| Décision | Avantages | Risques | Mitigation |
|----------|-----------|---------|------------|
| Gmail source de vérité | Sync multi-appareils, labels unifiés | Dépendance Google API/quota | Retry, batch, journaux |
| Rust moteur | Perf, sûreté | Courbe initiale | Tests, CLI claire |
| Thunderbird cockpit | Gratuit, Win+Android, IMAP | Pas d’API compose riche | Hermès prépare brouillon ; tests Phase 1 |
| Extraction fichiers PR | Découplage, scan PR inchangé | Doublons chemins | Hash, manifeste JSONL |
| Dry-run systématique | Confiance avant delete | Lenteur adoption règles | Rapports clairs |
| Validation humaine V1 | Sécurité envoi/delete | Friction | UX rapports Hermès |

## Documents liés

- [Modèle multi-comptes](03_GMAIL_MULTI_ACCOUNT_MODEL.md)
- [OAuth / API Gmail](04_GMAIL_OAUTH_IMAP_API_MODEL.md)
- [Sécurité — porte d’entrée](13_SECURITY_PRIVACY_AND_HUMAN_VALIDATION.md)
- [Modèle de menace](17_SECURITY_THREAT_MODEL.md)
- [Décision log](16_DECISION_LOG.md)
