# KitV2 URL Correction Research — 2026-08-05

5 dead URLs found in KitV2 product files, each verified and replaced.

---

## 1. `knowledge/anti-patterns/arch-god-object.yaml`

**Dead URL:** `https://refactoring.guru/refactoring/smells/large-class` (HTTP 404)

**Replacement URL:** `https://refactoring.guru/smells/large-class`

**HTTP check:** `curl -L -s -o /dev/null -w '%{http_code}'` → `200`

**Source:** Refactoring.Guru — "Large Class" code smell page, canonical refactoring reference.

**Justification:** The original URL had an extra `/refactoring/` path segment that no longer exists on the site. The correct path is `/smells/large-class`. The site was fetched and confirmed to serve the "Large Class" content (code smell: a class with many fields/methods/lines of code). This is the same resource, just at the correct URL.

**Date of consultation:** 2026-08-05

---

## 2. `knowledge/anti-patterns/msg-offset-commit-misorder.yaml`

**Dead URL:** `https://docs.axonops.com/data-platforms/kafka/application-development/anti-patterns/` (DNS resolution failure: `getaddrinfo ENOTFOUND`)

**Replacement URL:** `https://docs.confluent.io/platform/current/clients/consumer.html`

**HTTP check:** `curl -L -s -o /dev/null -w '%{http_code}'` → `200`

**Source:** Confluent Documentation — "Kafka Consumer for Confluent Platform", official Kafka client configuration reference.

**Justification:** The Axonops page (a Kafka anti-patterns guide) is no longer reachable. Confluent's official consumer documentation covers offset commit semantics, auto-commit vs manual commit, delivery semantics (at-most-once, at-least-once), and consumer group coordination — directly addressing the anti-pattern described in the YAML (offset commit misordering, auto-commit with async processing, commit-before-processing data loss). This is the most authoritative Kafka consumer reference available.

**Date of consultation:** 2026-08-05

---

## 3. `knowledge/anti-patterns/test-over-mocking.yaml`

**Dead URL:** `http://xunitpatterns.com/MockObject.html` (HTTP 404)

**Replacement URL:** `http://xunitpatterns.com/Mock%20Object.html`

**HTTP check:** `curl -L -s -o /dev/null -w '%{http_code}'` → `200`

**Source:** XUnitPatterns.com — "Mock Object" pattern page, by Gerard Meszaros (author of xUnit Test Patterns book).

**Justification:** The original URL used `MockObject.html` (no space) but the actual page is at `Mock%20Object.html` (with a space). The page was fetched and confirmed to serve the Mock Object pattern content — behavior verification, test doubles, and the distinction between mockist and classicist testing styles. This is the same resource at the correct URL.

**Date of consultation:** 2026-08-05

---

## 4. `knowledge/anti-patterns/test-sleep-based.yaml`

**Dead URL:** `http://xunitpatterns.com/Sleepy%20Test.html` (HTTP 404)

**Replacement URL:** `http://xunitpatterns.com/Slow%20Tests.html`

**HTTP check:** `curl -L -s -o /dev/null -w '%{http_code}'` → `200`

**Source:** XUnitPatterns.com — "Slow Tests" pattern page, by Gerard Meszaros.

**Justification:** The "Sleepy Test" page does not exist on xunitpatterns.com. The site's equivalent anti-pattern for time-based test delays is "Slow Tests" (`/Slow%20Tests.html`), which covers tests that take too long to run, cause developers to skip running them, and degrade trust in the test suite — the same category of problem as sleep-based tests. The page was fetched and confirmed to serve the "Slow Tests" content.

**Date of consultation:** 2026-08-05

---

## 5. `knowledge/catalogs/libraries/modernc-sqlite/SKILL.md`

**Dead URL:** `https://gitlab.com/cznic/sqlite/-/issues` (HTTP 404)

**Replacement URL:** `https://gitlab.com/cznic/sqlite/-/work_items`

**HTTP check:** `curl -L -s -o /dev/null -w '%{http_code}'` → `200`

**Source:** GitLab — cznic/sqlite project Work Items page (issue tracker).

**Justification:** GitLab has migrated the issue tracking system from "issues" to "work items" for this project. The `/issues` endpoint now 404s, while `/work_items` serves the same issue tracker interface. The page was fetched and confirmed to show the work items list for cznic/sqlite, including known issues about VFS, transaction behavior, platform support, and other limitations relevant to the SKILL.md's "Pièges connus" section.

**Date of consultation:** 2026-08-05

---

## Summary

| File | Dead URL | Replacement | HTTP |
|---|---|---|---|
| `arch-god-object.yaml` | `refactoring.guru/refactoring/smells/large-class` | `refactoring.guru/smells/large-class` | 200 |
| `msg-offset-commit-misorder.yaml` | `docs.axonops.com/.../anti-patterns/` | `docs.confluent.io/platform/current/clients/consumer.html` | 200 |
| `test-over-mocking.yaml` | `xunitpatterns.com/MockObject.html` | `xunitpatterns.com/Mock%20Object.html` | 200 |
| `test-sleep-based.yaml` | `xunitpatterns.com/Sleepy%20Test.html` | `xunitpatterns.com/Slow%20Tests.html` | 200 |
| `modernc-sqlite/SKILL.md` | `gitlab.com/cznic/sqlite/-/issues` | `gitlab.com/cznic/sqlite/-/work_items` | 200 |
