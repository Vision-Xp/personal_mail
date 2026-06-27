# Choix du client mail

## Contexte

Damien doit consulter **toutes** ses boîtes Gmail sur **Windows** et **Android**, avec une organisation **déjà créée côté Gmail** par `personal_mail`. Le client est le cockpit humain — pas le moteur de classement.

## Candidats comparés

| Critère | Thunderbird D.+A. | Gmail Web/App | Outlook | eM Client free | Mailbird free |
|---------|-------------------|---------------|---------|----------------|---------------|
| Gratuité réelle | Oui (Mozilla) | Oui | Freemium / M365 | Limité | Très limité |
| Windows | Oui | Web/app | Oui | Oui | Oui |
| Android | Oui (dédié) | Oui | Oui | Non | Non |
| Multi-comptes | Oui | Oui | Oui | Oui | Oui |
| Gmail OAuth | Oui | Natif | Oui | Oui | Variable |
| IMAP | Oui | N/A | Oui | Oui | Oui |
| Labels/dossiers Gmail | Sync labels | Natif | Partiel | Partiel | Partiel |
| Robustesse | Bonne | Excellente | Bonne | Correcte | Correcte |
| Pérennité | Fondation Mozilla | Google | Microsoft | Éditeur commercial | Éditeur commercial |
| Open-source | Oui (desktop) | Non | Non | Non | Non |
| Confidentialité | Local + sync serveur | Cloud Google | Cloud MS | Local | Local |
| Automatisation compose | Limitée (OS/URI) | N/A pour Hermès | Limitée | Limitée | Limitée |
| Export standard | Oui (.eml, etc.) | Oui | Oui | Oui | Oui |
| Affiche orga Gmail créée ailleurs | Oui (si labels sync) | Oui | À tester | À tester | À tester |

### Autres options notées

- **FairEmail** (Android, open-source) : fort sur confidentialité, mais pas de pendant Windows unifié avec le même produit.
- **K-9 Mail** : fusionné dans Thunderbird Android — aligné avec la piste Thunderbird.

## Critères décisifs pour personal_mail

1. **Windows + Android** avec expérience cohérente.
2. **Gratuit** sans plafond agressif sur multi-comptes.
3. **Synchronisation des labels Gmail** créés par l’API.
4. **Ne pas devenir la base métier** — le client doit refléter Gmail, pas l’inverse.
5. **Pérennité** et communauté active.

## Recommandation provisoire

**Thunderbird Desktop + Thunderbird Android** comme candidat principal :

- Gratuit, open-source (desktop), présent sur les deux plateformes cibles.
- Multi-comptes Gmail via OAuth/IMAP.
- Aligné avec la décision « Gmail = source de vérité » : Thunderbird affiche les labels existants.
- Hermès peut viser la préparation de brouillons côté Windows (méthode exacte à valider en Phase 1).

## Précisions importantes

- Thunderbird est le **cockpit humain** — lecture, modification, envoi.
- Gmail reste la **source de vérité** — `personal_mail` écrit les labels sur Gmail.
- La **décision finale** doit être validée par **test réel** : labels créés via API visibles sur Thunderbird Desktop et Android (Phase 1 roadmap).

## Documents liés

- [Architecture](01_ARCHITECTURE_DECISIONS.md)
- [Usage Windows/Android](11_WINDOWS_ANDROID_USAGE_MODEL.md)
- [Roadmap Phase 1](15_IMPLEMENTATION_ROADMAP.md)
- [Décision log](16_DECISION_LOG.md)
