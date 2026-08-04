# Plan — Intégration bibliothèques auth (2026-08-05)

- **Demande :** évaluer 6 candidats auth (gorilla/sessions, golang-jwt, x/oauth2,
  x/crypto bcrypt, alice, authboss) contre les gates ; intégrer les passants.
- **Méthode :** données dures GitHub/OSV/Scorecard/proxy.golang + audit de
  couverture + pipeline Z2 §9 / A1 / N1 §4 / C2 / Z11.

## Décisions (gate par gate)

| Candidat | Verdict | Gate échouée / pin |
| --- | --- | --- |
| golang-jwt/jwt v5.3.1 | **APPROUVER** (promotion legacy YAML → fiche) | pin ≥ 5.2.2 (GO-2025-3553) |
| x/oauth2 v0.36.0 | **POINTEUR stdlib** | pin ≥ 0.27.0 (GO-2025-3488) |
| x/crypto v0.54.0 | **POINTEUR stdlib** | pin ≥ 0.52.0 (batch 2026) ; openpgp unsafe (GO-2026-5932, non corrigé) |
| alexedwards/scs v2.9.0 | **APPROUVER** (remplaçant gorilla/sessions) | 0 advisory ; actif |
| gorilla/sessions v1.4.0 | **REFUSER** | G5 maintenance : dormant depuis 2024-08-20 (24 mois) |
| justinas/alice | **REFUSER** | G5 maintenance : dormant depuis 2024-06-06 ; concept couvert (`pattern:http:middleware-chain`) |
| aarondl/authboss v3.5.3 | **REFUSER** | Framework opaque : viole anti-framework (décision order) + responsabilité unique ; maintenance OK |
| gorilla/csrf v1.7.3 | **SURVEILLER** | ~15 mois dormants ; besoin couvert par anti-pattern CSRF stdlib |
| justinas/nosurf v1.2.0 | **SURVEILLER** | ~15 mois dormants |

## Fichiers à créer

1. `knowledge/catalogs/libraries/golang-jwt/SKILL.md` (promotion ; le YAML legacy
   `golang-jwt.yaml` reste, kind Source).
2. `knowledge/catalogs/libraries/scs/SKILL.md` (nouveau).
3. `knowledge/stdlib/x-crypto.yaml` — `source:go:x-crypto` (bcrypt/argon2, openpgp).
4. `knowledge/stdlib/x-oauth2.yaml` — `source:go:x-oauth2` (OAuth2/OIDC).
5. `knowledge/patterns/auth-session-vs-jwt.yaml` — `pattern:security:auth-session-vs-jwt`
   (décision cookies vs JWT vs OAuth2 — question centrale, aucune couverture existante).
6. `knowledge/anti-patterns/sec-missing-csrf.yaml` — `pattern:antipattern:sec-missing-csrf`
   (OWASP ; aucune couverture CSRF existante).

## Fichiers à modifier

- `tools/validators/validate-kitv2.py` : EXPECTED_PRODUCT_SKILLS 60 → 62.
- `capabilities.yaml` : product_skills 60 → 62 ; knowledge_catalogs 40 → 42.
- Router régénéré (246 → +8 ressources).
- `.pi/memory/Gotchas.md` : section rejets (gorilla/sessions, alice, authboss,
  gorilla/csrf, nosurf) avec critère et évidence.

## Validation

Gate complète + compile minimal use (déjà faits : jwt/scs/bcrypt/oauth2 OK) +
évidence `docs/evidence/2026-08-05/auth-libraries/` + revue fresh-context.
