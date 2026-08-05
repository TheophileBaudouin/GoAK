// Package restchi shows a minimal idiomatic REST API with the chi router:
// composable middleware, a route group, path parameters, and JSON in/out.
//
// chi is 100% net/http-compatible, so handlers and middleware are plain
// http.HandlerFunc / func(http.Handler) http.Handler — no framework-specific
// signatures, and any net/http middleware in the ecosystem just works.
package restchi

import (
	"encoding/json"
	"io"
	"log/slog"
	"net/http"
	"sort"
	"strconv"
	"strings"
	"sync"

	"github.com/go-chi/chi/v5"
	"github.com/go-chi/chi/v5/middleware"
)

const maxRequestBodyBytes = 8 << 10

// Item is the API resource.
type Item struct {
	ID   int    `json:"id"`
	Name string `json:"name"`
}

// Store is a tiny thread-safe in-memory backing store for the example.
// Its logger is supplied at construction so applications retain ownership of
// log configuration and redaction policy.
type Store struct {
	mu     sync.RWMutex
	nextID int
	items  map[int]Item
	log    *slog.Logger
}

// NewStore returns an empty Store ready to serve using slog.Default().
func NewStore() *Store {
	return NewStoreWithLogger(slog.Default())
}

// NewStoreWithLogger returns an empty Store using logger. A nil logger is
// replaced with slog.Default so request handling remains safe for callers that
// have not configured logging yet.
func NewStoreWithLogger(logger *slog.Logger) *Store {
	if logger == nil {
		logger = slog.Default()
	}
	return &Store{nextID: 1, items: make(map[int]Item), log: logger}
}

// Router builds the chi router with a canonical base middleware stack and the
// /items resource mounted. Returning http.Handler keeps the handler decoupled
// from chi internals — callers just http.ListenAndServe(":3333", s.Router()).
func (s *Store) Router() http.Handler {
	r := chi.NewRouter()
	// Access logging belongs to the observability recipe. Do not install chi's
	// generic logger here: request URLs and bodies can contain client data.
	r.Use(middleware.RequestID, middleware.Recoverer)

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
	r.Body = http.MaxBytesReader(w, r.Body, maxRequestBodyBytes)
	decoder := json.NewDecoder(r.Body)
	decoder.DisallowUnknownFields()
	if err := decoder.Decode(&in); err != nil {
		writeJSON(w, http.StatusBadRequest, errResp("invalid JSON body"))
		return
	}
	var extra any
	if err := decoder.Decode(&extra); err != io.EOF {
		writeJSON(w, http.StatusBadRequest, errResp("invalid JSON body"))
		return
	}
	in.Name = strings.TrimSpace(in.Name)
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

	// ID is server-generated. Do not log request bodies or client-supplied names.
	s.log.Info("item created", "item_id", id)
	writeJSON(w, http.StatusCreated, item)
}

func (s *Store) listItems(w http.ResponseWriter, _ *http.Request) {
	s.mu.RLock()
	out := make([]Item, 0, len(s.items))
	for _, it := range s.items {
		out = append(out, it)
	}
	s.mu.RUnlock()
	sort.Slice(out, func(i, j int) bool { return out[i].ID < out[j].ID })
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
		writeJSON(w, http.StatusNotFound, errResp("item not found"))
		return
	}
	writeJSON(w, http.StatusOK, item)
}

// writeJSON serialises v as JSON with the given status. A write error is
// ignored: per net/http contract there is no useful recovery once the headers
// are sent.
func writeJSON(w http.ResponseWriter, status int, v any) {
	w.Header().Set("Content-Type", "application/json; charset=utf-8")
	w.WriteHeader(status)
	_ = json.NewEncoder(w).Encode(v)
}

func errResp(msg string) errorResponse {
	return errorResponse{Error: msg}
}

type errorResponse struct {
	Error string `json:"error"`
}
