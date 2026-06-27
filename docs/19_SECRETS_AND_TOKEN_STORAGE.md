# Secrets et stockage des tokens

## 1. Interdictions absolues

| Interdit | Raison |
|--------|--------|
| Mot de passe Gmail en clair | Contournement OAuth, fuite catastrophique |
| Token dans Git | Historique irréversible |
| Token dans logs | Exposition opérationnelle |
| Token dans rapports | Partage / commit accidentel |
| Token dans exemples YAML | Mauvais réflexe copy-paste |
| Credentials dans captures ou docs | Fuite hors dépôt |

Les fichiers `*.example.yaml` utilisent uniquement des **placeholders** (`local_secure_store`, `system_keyring_or_dpapi`) — jamais de valeurs réelles.

## 2. OAuth Gmail

| Aspect | Politique |
|--------|-----------|
| Autorisation | Un flux OAuth **par compte** Gmail |
| Scopes | Minimaux — voir [04](04_GMAIL_OAUTH_IMAP_API_MODEL.md) |
| Révocation | Possible sur [Google Account](https://myaccount.google.com/permissions) + purge locale |
| Séparation | Un enregistrement token par `account_id` |
| Rotation | Réautorisation documentée si compromission suspectée ou expiration refresh |
| Refresh token | Traité comme SECRET — même protection que access token |

### Scopes cibles (à affiner à l’implémentation)

- Lecture messages et métadonnées
- Modification labels
- Téléchargement pièces jointes
- Trash (phase apply validée)
- **Pas** d’envoi mail via API en V1 sans validation explicite future

## 3. Stockage local cible (Windows)

| Option | Statut |
|--------|--------|
| Windows Credential Manager | **Candidat principal** |
| DPAPI (chiffrement utilisateur Windows) | Via crate `keyring` ou équivalent Rust |
| Fichiers tokens plats | **Interdits** en production |
| Fichier dev temporaire | Autorisé **uniquement** si : dossier ignoré Git (`tokens/`, `secrets/`), chiffrement ou durée courte, jamais commité |

Structure logique (implémentation future) :

```
Service: personal_mail
  Account: gmail_personal_1  → refresh + access (chiffré OS)
  Account: gmail_music_1     → refresh + access (chiffré OS)
```

Chemins `tokens/`, `oauth/`, `credentials/`, `keyring/` sont dans `.gitignore`.

## 4. Permissions progressives

| Phase | Capacités activées |
|-------|-------------------|
| 1 — Lecture seule | List, get metadata, dry-run classification |
| 2 — Labels | create/modify labels, safe-run |
| 3 — Extraction | attachments.get, écriture PR documents |
| 4 — Trash contrôlé | trash après dry-run + validation |
| — | **Jamais** suppression définitive auto en V1 |
| — | **Jamais** envoi automatique sensible en V1 |

Aligné avec [config/security_policy.example.yaml](../config/security_policy.example.yaml) et [hermes_permissions.example.yaml](../config/hermes_permissions.example.yaml).

## 5. Checklist avant activation d’un compte réel

- [ ] `.gitignore` vérifié et à jour
- [ ] Aucun secret dans le working tree (`git status` propre)
- [ ] `security_policy.local.yaml` revu (copie locale de l’exemple)
- [ ] Dry-run exécuté avec succès sur compte **test** d’abord
- [ ] Scopes OAuth compris et minimaux
- [ ] Compte test validé (Phase 3 roadmap)
- [ ] Procédure restauration comprise (trash, quarantaine)
- [ ] Stockage token = keyring/DPAPI — pas de fichier plat
- [ ] Hermès configuré : pas d’affichage token dans chat/logs

## Documents liés

- [OAuth / API Gmail](04_GMAIL_OAUTH_IMAP_API_MODEL.md)
- [Classification données](18_DATA_CLASSIFICATION_AND_RETENTION.md)
- [Modèle de menace](17_SECURITY_THREAT_MODEL.md)
