// Package restchi shows a minimal idiomatic REST API with the chi router:
// composable middleware, a route group, path parameters, and JSON in/out.
//
// chi is 100% net/http-compatible, so handlers and middleware are plain
// http.HandlerFunc / func(http.Handler) http.Handler — no framework-specific
// signatures, and any net/http middleware in the ecosystem just works.
package restchi

import (
	"encoding/json"
	"log/slog"
	"net/http"
	"strconv"
	"sync"

	"github.com/go-chi/chi/v5"
	"github.com/go-chi/chi/v5/middleware"
)

// Item is the API resource.
type Item struct {
	ID   int    `json:"id"`
	Name string `json:"name"`
}

// Store is a tiny thread-safe in-memory backing store for the example.
// The logger is injected (see rules/registry/logging): slog is the kit default,
// never fmt.Println. chi's middleware.Logger below is access-level; s.log
// carries the structured business signal.
type Store struct {
	mu     sync.RWMutex
	nextID int
	items  map[int]Item
	log    *slog.Logger
}

// NewStore returns an empty Store ready to serve. It wires slog.Default() as
// the logger; a constructor taking an explicit *slog.Logger keeps the logger
// testable in real services (see rules/registry/logging).
func NewStore() *Store {
	return &Store{nextID: 1, items: make(map[int]Item), log: slog.Default()}
}

// Router builds the chi router with a canonical base middleware stack and the
// /items resource mounted. Returning http.Handler keeps the handler decoupled
// from chi internals — callers just http.ListenAndServe(":3333", s.Router()).
func (s *Store) Router() http.Handler {
	r := chi.NewRouter()
	r.Use(middleware.RequestID, middleware.Logger, middleware.Recoverer)

	r.Route("/items", func(r chi.Router) {
		r.Get("/", s.listItems)   // GET    /items
		r.Post("/", s.createItem) // POST   /items
		r.Get("/{id}", s.getItem) // GET    /items/{id}
	})
	return r
}

func (s *Store) createItem(w http.ResponseWriter, r *http.Request) {
	var in struct {
		Name string `json:"name"`
	}
	if err := json.NewDecoder(r.Body).Decode(&in); err != nil {
		writeJSON(w, http.StatusBadRequest, errResp("invalid JSON body"))
		return
	}
	if in.Name == "" {
		writeJSON(w, http.StatusBadRequest, errResp("name is required"))
		return
	}

	s.mu.Lock()
	id := s.nextID
	s.nextID++
	item := Item{ID: id, Name: in.Name}
	s.items[id] = item
	s.mu.Unlock()

	s.log.Info("item created", "id", id, "name", in.Name)
	writeJSON(w, http.StatusCreated, item)
}

func (s *Store) listItems(w http.ResponseWriter, _ *http.Request) {
	s.mu.RLock()
	out := make([]Item, 0, len(s.items))
	for _, it := range s.items {
		out = append(out, it)
	}
	s.mu.RUnlock()
	writeJSON(w, http.StatusOK, out)
}

func (s *Store) getItem(w http.ResponseWriter, r *http.Request) {
	id, err := strconv.Atoi(chi.URLParam(r, "id"))
	if err != nil {
		writeJSON(w, http.StatusBadRequest, errResp("id must be an integer"))
		return
	}

	s.mu.RLock()
	item, ok := s.items[id]
	s.mu.RUnlock()
	if !ok {
		s.log.Warn("item not found", "id", id)
		writeJSON(w, http.StatusNotFound, errResp("item not found"))
		return
	}
	writeJSON(w, http.StatusOK, item)
}

// writeJSON serialises v as JSON with the given status. A write error is
// ignored: per net/http contract there is no useful recovery once the headers
// are sent.
func writeJSON(w http.ResponseWriter, status int, v any) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	_ = json.NewEncoder(w).Encode(v)
}

func errResp(msg string) map[string]string {
	return map[string]string{"error": msg}
}
