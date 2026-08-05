# Re-vérification des URLs pkg.go.dev initialement rate-limitées — 2026-08-05

## Résultat

Les 18 URLs initialement observées en HTTP 429 ont été re-vérifiées par le
sous-agent de recherche le 2026-08-05 avec `fetch_content`, séquentiellement.
La méthode n'a pas permis d'imposer un délai de 4 secondes ni de fournir un
User-Agent curl navigateur ; cette limite est conservée explicitement.

Résultat sous-agent : **18 vivantes / 0 mortes / 0 toujours 429**, chacune en
HTTP 200 à la première tentative de son outil.

Un contrôle indépendant du correcteur avec `curl -L -s -o /dev/null -w
'%{http_code}'`, User-Agent navigateur et délai de 3 secondes a confirmé 3
URLs représentatives en HTTP 200 : `x/sync/errgroup`, `log/slog`, et
`vuln/GO-2024-3098`.

| URL | Résultat sous-agent | Tentatives | Statut | Vérification indépendante |
|---|---:|---:|---|---:|
| <https://pkg.go.dev/golang.org/x/crypto/ssh> | 200 | 1 | vivant | non re-testée indépendamment |
| <https://pkg.go.dev/golang.org/x/oauth2> | 200 | 1 | vivant | non re-testée indépendamment |
| <https://pkg.go.dev/golang.org/x/sync/errgroup> | 200 | 1 | vivant | 200 curl |
| <https://pkg.go.dev/golang.org/x/sync/singleflight> | 200 | 1 | vivant | non re-testée indépendamment |
| <https://pkg.go.dev/golang.org/x/tools/go/analysis/passes/shadow> | 200 | 1 | vivant | non re-testée indépendamment |
| <https://pkg.go.dev/google.golang.org/adk/v2> | 200 | 1 | vivant | non re-testée indépendamment |
| <https://pkg.go.dev/html/template> | 200 | 1 | vivant | non re-testée indépendamment |
| <https://pkg.go.dev/log/slog> | 200 | 1 | vivant | 200 curl |
| <https://pkg.go.dev/modernc.org/sqlite> | 200 | 1 | vivant | non re-testée indépendamment |
| <https://pkg.go.dev/net/http> | 200 | 1 | vivant | non re-testée indépendamment |
| <https://pkg.go.dev/net/http/httptest> | 200 | 1 | vivant | non re-testée indépendamment |
| <https://pkg.go.dev/strings> | 200 | 1 | vivant | non re-testée indépendamment |
| <https://pkg.go.dev/sync> | 200 | 1 | vivant | non re-testée indépendamment |
| <https://pkg.go.dev/testing> | 200 | 1 | vivant | non re-testée indépendamment |
| <https://pkg.go.dev/text/template> | 200 | 1 | vivant | non re-testée indépendamment |
| <https://pkg.go.dev/vuln/> | 200 | 1 | vivant | non re-testée indépendamment |
| <https://pkg.go.dev/vuln/GO-2024-3098> | 200 | 1 | vivant | 200 curl |
| <https://pkg.go.dev/vuln/GO-2026-5320> | 200 | 1 | vivant | non re-testée indépendamment |

## Conclusion

Aucune URL pkg.go.dev ne doit être remplacée. Le statut initial « À VÉRIFIER »
est levé avec confiance élevée pour les résultats du sous-agent et confiance
indépendante complémentaire sur l'échantillon curl. Consultation :
2026-08-05.
