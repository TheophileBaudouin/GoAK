# Rapport — Intégration bibliothèques auth (2026-08-05)

- **Plan :** `docs/plans/2026-08-05-auth-libraries.md`
- **Évidence brute :** `docs/evidence/2026-08-05/auth-libraries/gate.log`

## Décisions

| Candidat | Verdict | Justification (données 2026-08-05) |
| --- | --- | --- |
| golang-jwt/jwt v5.3.1 | **APPROUVÉ** (promotion legacy) | Actif (push 08-01), scorecard 7.8, pin ≥ 5.2.2 (GO-2025-3553) |
| x/oauth2 v0.36.0 | **POINTEUR stdlib** | Go team, actif, pin ≥ 0.27.0 (GO-2025-3488) |
| x/crypto v0.54.0 | **POINTEUR stdlib** | Go team, pin ≥ 0.52.0 (batch 2026), openpgp unsafe (GO-2026-5932) |
| alexedwards/scs v2.9.0 | **APPROUVÉ** (remplaçant gorilla/sessions) | Actif (push 2025-11-20), 0 advisory, MIT |
| gorilla/sessions | **REFUSÉ** | G5 : dormant 2024-08-20 (24 mois) |
| justinas/alice | **REFUSÉ** | G5 : dormant 2024-06-06 (26 mois), sans releases ; concept couvert (`pattern:http:middleware-chain`) |
| aarondl/authboss v3.5.3 | **REFUSÉ** | Framework opaque : anti-framework + responsabilité unique (maintenance OK) |
| gorilla/csrf v1.7.3 | **SURVEILLER** | ~15 mois dormants ; besoin couvert par anti-pattern CSRF stdlib |
| justinas/nosurf v1.2.0 | **SURVEILLER** | ~15 mois dormants |

## Fichiers créés (6)

- `catalogs/libraries/golang-jwt/SKILL.md` — fiche vétée (promotion ; le YAML
  legacy `golang-jwt.yaml` kind Source reste).
- `catalogs/libraries/scs/SKILL.md` — fiche vétée (nouvelle).
- `stdlib/x-crypto.yaml` (`source:go:x-crypto`) — bcrypt/argon2, openpgp.
- `stdlib/x-oauth2.yaml` (`source:go:x-oauth2`) — OAuth2/OIDC.
- `patterns/auth-session-vs-jwt.yaml` (`pattern:security:auth-session-vs-jwt`)
  — décision cookies vs JWT vs OAuth2 (aucune couverture existante).
- `anti-patterns/sec-missing-csrf.yaml` (`pattern:antipattern:sec-missing-csrf`)
  — OWASP, aucune couverture CSRF existante.

Minimal use compilés hors kit (jwt, scs, bcrypt, oauth2 : OK — voir session).

## Fichiers modifiés

- `validate-kitv2.py` : EXPECTED_PRODUCT_SKILLS 60 → 62.
- `capabilities.yaml` : product_skills 60 → 62 ; knowledge_catalogs 40 → 42.
- `router/` : régénéré (246 → 252 ressources).
- `.pi/memory/Gotchas.md` : 5 rejets loggés (règle admission).

## Gate (sorties dans gate.log)

kitv2 PASS (62 skills, router 252) · instructions PASS · gofmt OK · vet OK ·
lint 0 · tests -race 11 pkgs · gosec 0 · govulncheck 0 · probes 5/5 ·
router up to date.

## Points honnêtes

- **scs** n'était pas dans la liste demandée : c'est le remplaçant rigoureux de
  gorilla/sessions (refusé), substitution assumée et documentée.
- **authboss** : maintenance OK (push 2026-07-10) mais architecture rejetée
  (framework opaque) — cohérent avec « NE PAS : frameworks auth complets
  opaques ».
- **Scorecard scs Maintained:0** = cache périmé (contredit par push GitHub) —
  même anomalie que age, croiser avec GitHub.
- Aucune dépendance ajoutée au module kit.
- **Legacy `golang-jwt.yaml` supprimé** après promotion (convention des vagues
  précédentes cobra/koanf/viper) — aucune référence résiduelle ; router
  régénéré (251 ressources).

## Revue fresh-context

Verdict **APPROVE-WITH-NITS** (0 BLOCKER/MAJOR). Tous les claims sécurité
recroisés OSV/GitHub/Scorecard **exacts** : GO-2025-3553 fix 5.2.2,
GO-2025-3488 fix 0.27.0, batch x/crypto 0.52.0 (ssh/agent), openpgp
GO-2026-5932 non corrigé, scs 0 advisory, dormances gorilla/sessions/alice,
authboss actif mais rejeté architecture. Zéro duplication de question.

Nits corrigés (2026-08-05) :

- F1 : mention « org gorilla archivée en 2020 » retirée (claim périmé — repos
  relancés en 2022 ; le motif de rejet reste la dormance vérifiée).
- F2 : URL OWASP JWT 404 → `JSON_Web_Token_Cheat_Sheet.html`.
- F3 : classe « A01/Broken Access Control » retirée (CSRF hors Top 10) —
  citation cheat sheet OWASP conservée.
- F4 : x/crypto « no fix planned » → recommandation du fork maintenu
  ProtonMail/go-crypto.
- F6 : legacy `golang-jwt.yaml` supprimé (convention migration).

## Restants

- gorilla/csrf + nosurf à ré-évaluer à leur prochaine release (WATCH).
- Harmonisation des fiches préexistantes sans Security note (déjà notée).
