# PERSONAL_MAIL — modèles de prompts (Hermès / Cursor)

Prompts **génériques** — aucune donnée réelle. Adapter les placeholders `[...]` en session.

---

## 1. Audit des specs

```
Tu travailles sur le projet personal_mail (repo specs, phase sans moteur Rust).
Objectif : auditer la cohérence entre docs/00–23, hermes_context/, et config/*.example.yaml.
Vérifie : architecture Gmail source de vérité, Thunderbird cockpit, sécurité by-design, pas de secrets.
Liste : incohérences, manques, liens cassés, décisions ouvertes.
Ne connecte pas Gmail. Ne crée pas de tokens.
```

---

## 2. Dry-run futur

```
Contexte : personal_mail — mode dry-run uniquement.
Objectif : simuler l’application de la règle [RULE_ID] sur le compte fictif [ACCOUNT_ID].
Produis un rapport listant : messages qui seraient affectés, labels proposés, confiance, actions qui NE seront PAS exécutées.
Aucune modification Gmail. Aucun fichier réel. Fixtures synthétiques uniquement.
```

---

## 3. Validation rapport dry-run

```
Voici un rapport dry-run fictif pour personal_mail (aucune donnée réelle).
Analyse : faux positifs probables, mails sensibles mal classés, risques de suppression.
Recommande : GO / GO limité / NO GO pour passage en apply-run.
Rappelle la règle canonique : doute → validation humaine, pas de suppression.
```

---

## 4. Extraction document prudente

```
Contexte personal_mail — extraction vers I:\Dev Applications\personal_radar\documents.
Message fictif : expéditeur [SENDER_EXAMPLE], PJ [EXT], catégorie [CATEGORY], confiance [SCORE].
Vérifie : extension sûre, cohérence expéditeur, pas de PJ dangereuse.
Si OK : décris renommage, hash, sidecar .meta.json, manifeste JSONL.
Si doute : SUSPICIEUX_A_VALIDER — pas d’écriture PR sans validation Damien.
```

---

## 5. Audit newsletters

```
Mode audit-run personal_mail (fictif).
Objectif : lister les expéditeurs newsletter détectés sur [ACCOUNT_ID_EXAMPLE].
Pour chaque : proposer garder / revoir / désabonner.
Rappel V1 : pas de désabonnement automatique sans validation humaine.
Rapport expurgé, aucune adresse réelle.
```

---

## 6. Préparation mail de résiliation

```
Hermès — compose-run personal_mail.
Contexte fictif : contrat [SERVICE_EXAMPLE], échéance [DATE], références [REF].
Rédige un brouillon de résiliation : poli, ferme, concis, juridiquement prudent.
Champs : destinataire, objet, corps. Pas d’envoi. Validation Damien obligatoire.
```

---

## 7. Préparation demande banquier

```
Hermès — compose-run personal_mail.
Contexte fictif : établissement [BANK_EXAMPLE], demande [TYPE: justificatif / contestation / info].
Rédige un brouillon adapté. Ne pas inclure d’IBAN ou données réelles.
Validation Damien avant envoi. Pas d’envoi automatique.
```

---

## 8. Vérification sécurité avant action

```
Avant toute action personal_mail sur [ACTION: classify / extract / trash / compose] :
Checklist : secret visible ? mail réel dans Git ? PJ dangereuse ? destination claire ?
compte Gmail univoque ? confiance suffisante ? dry-run fait si destructif ?
Si un point échoue : STOP — validation humaine. Citer docs/17 et règle canonique.
```

---

## 9. Rapport GO / GO limité / NO GO

```
Génère un rapport de validation personal_mail (template fictif).
Sections : périmètre, tests fonctionnels, tests sécurité S1–S12, risques résiduels.
Verdict : GO / GO limité / NO GO avec conditions.
Aucune PII. Référencer docs/14_TEST_AND_VALIDATION_PLAN.md.
```
