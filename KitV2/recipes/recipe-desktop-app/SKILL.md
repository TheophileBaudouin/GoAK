---
name: recipe-desktop-app
description: "Service Go testable pour application Desktop Wails v3 sans dépendance runtime directe. Méthodes liées typées et isolées du Webview. Utiliser pour concevoir la logique métier Go d'une application Desktop Wails."
category: recipe
tags: [desktop, wails, gui, bindings, frontend, Go]
last-verified: 2026-08-05
---

# recipe-desktop-app — Adaptateur de service Go pour Wails v3

## Objectif et cas d'utilisation

Concevoir la couche de services métier en Go d'une application Desktop Wails v3 de sorte que les méthodes exposées au frontend web soient 100% testables en Go pur, sans nécessiter la compilation CGO du webview ni le runtime Wails dans la suite de tests.

Utiliser cette recette pour créer des applications de bureau hybrides (Go + HTML/TS frontend) tout en maintenant les tests unitaires Go portables et rapides.

## Prérequis et architecture

- Go 1.25+
- Wails v3 (Beta-to-GA transition) — documenté pour l'application cliente, non importé dans ce package Go.
- Architecture testable :
  - L'objet `App` contient l'état applicatif et la synchronisation (`sync.Mutex`).
  - Les méthodes publiques (`AddNote`, `Notes`, `DeleteNote`) prennent et retournent des types Go typés avec des tags JSON (`json:"id"`).
  - Ne contenir aucun import vers `github.com/wailsapp/wails/v3/pkg/application` dans le package de service métier, pour éviter de tirer la dépendance CGO/GTK/Webview2 dans la gate Go.

## Composants et choix

- Struct métier Go pur avec Mutex — garantit la sécurité d'accès concurrent entre le thread principal Go et les appels JS asynchrones du frontend.
- Contrat d'interface transparent — les méthodes exportées sont automatiquement exposées au frontend par les générateurs de bindings Wails (`wails3 generate bindings`).

## Alternatives rejetées

- Importer directement le package `application` de Wails dans le package de service : impose la présence de bibliothèques système CGO/GUI (WebKitGTK sur Linux, Webview2 sur Windows), brisant les tests unitaires croisés sur CI sans GUI.
- Tauri (Rust) : framework alternatif majeur, mais rédigé en Rust et non en Go.
- Fyne / Gio : frameworks GUI purement Go sans webview (autre paradigme d'architecture).

## Exemple complet

```go
package desktop

import (
	"errors"
	"sync"
	"time"
)

type Note struct {
	ID        int       `json:"id"`
	Text      string    `json:"text"`
	CreatedAt time.Time `json:"created_at"`
}

type App struct {
	mu     sync.Mutex
	nextID int
	notes  map[int]Note
}

func NewApp() *App {
	return &App{nextID: 1, notes: make(map[int]Note)}
}

var errEmptyNote = errors.New("note text must not be empty")

func (a *App) AddNote(text string) (Note, error) {
	if text == "" {
		return Note{}, errEmptyNote
	}
	a.mu.Lock()
	defer a.mu.Unlock()

	n := Note{ID: a.nextID, Text: text, CreatedAt: time.Now().UTC()}
	a.notes[n.ID] = n
	a.nextID++
	return n, nil
}

func (a *App) Notes() []Note {
	a.mu.Lock()
	defer a.mu.Unlock()

	out := make([]Note, 0, len(a.notes))
	for i := 1; i < a.nextID; i++ {
		if n, ok := a.notes[i]; ok {
			out = append(out, n)
		}
	}
	return out
}

func (a *App) DeleteNote(id int) bool {
	a.mu.Lock()
	defer a.mu.Unlock()
	_, ok := a.notes[id]
	delete(a.notes, id)
	return ok
}
```

## Bonnes pratiques et pièges

- Protéger tout état partagé avec `sync.Mutex` : le frontend Wails peut exécuter des appels de méthodes en parallèle.
- Valider systématiquement les arguments côté Go : Go est la frontière de confiance, le frontend peut transmettre des entrées invalides.
- Noter que Wails v3 est actuellement en statut Beta-to-GA : vérifier le suivi d'issues avant la mise en production.

## Limites et extensions

Cette recette couvre l'adaptateur Go testable. Le câblage `main.go` Wails avec la fenêtre webview et l'embarquement d'actifs statiques (`embed.FS`) vit dans le binaire d'application client final.

## Scénario observable et vérification

```sh
go test ./recipes/recipe-desktop-app/...
go run ./probes/desktop-app
```

La probe instancie `NewApp()`, ajoute une note, la liste, la supprime et vérifie le résultat, puis affiche `desktop-app: PASS`.

## Sources primaires

- [Wails Documentation](https://wails.io/) — site officiel et documentation Wails v2 / v3.
- [Wails v3 Beta Repository](https://github.com/wailsapp/wails) — dépôt officiel Wails.
