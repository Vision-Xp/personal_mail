# PERSONAL_MAIL — modes d’action

## dry-run (défaut)

| Aspect | Comportement |
|--------|--------------|
| Gmail | Aucune modification |
| Documents | Aucun écrit vers PR (sauf rapport local/fictif de simulation) |
| But | Analyse + rapport de ce qui **serait** fait |
| Hermès | Toujours privilégier ce mode pour nouvelle règle |

## safe-run

| Aspect | Comportement |
|--------|--------------|
| Labels | Application labels **non destructifs** |
| Extraction | Documents **non suspects** uniquement |
| Suppression | **Non** |
| Envoi | **Non** |

## apply-run

| Aspect | Comportement |
|--------|--------------|
| Prérequis | Règle validée par Damien après dry-run |
| Actions | Trash / quarantaine selon politique |
| Delete définitif | **Jamais** en V1 |
| Hermès | Ne lancer qu’après validation explicite |

## audit-run

| Aspect | Comportement |
|--------|--------------|
| Cibles | Newsletters, catégories, stockage Gmail, règles obsolètes |
| Sortie | Rapports **expurgés** si partage |
| Destructif | Non par défaut |

## compose-run

| Aspect | Comportement |
|--------|--------------|
| Action | Préparation mail / brouillon |
| Validation | **Damien obligatoire** avant envoi |
| Envoi auto | **Interdit** en V1 |

## Alignement config

`config/hermes_permissions.example.yaml`, `config/security_policy.example.yaml` — `default_mode: dry-run`.
