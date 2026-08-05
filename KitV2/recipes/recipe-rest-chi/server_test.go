package restchi

import (
	"bytes"
	"encoding/json"
	"log/slog"
	"net/http"
	"net/http/httptest"
	"strings"
	"sync"
	"testing"
)

func do(s *Store, method, target string, body any) *httptest.ResponseRecorder {
	var r *http.Request
	if body != nil {
		b, _ := json.Marshal(body)
		r = httptest.NewRequest(method, target, bytes.NewReader(b))
		r.Header.Set("Content-Type", "application/json")
	} else {
		r = httptest.NewRequest(method, target, nil)
	}
	w := httptest.NewRecorder()
	s.Router().ServeHTTP(w, r)
	return w
}

func TestCreateItem_success(t *testing.T) {
	s := NewStore()
	w := do(s, http.MethodPost, "/items", map[string]string{"name": "alpha"})

	if w.Code != http.StatusCreated {
		t.Fatalf("status = %d, want %d", w.Code, http.StatusCreated)
	}
	var got Item
	if err := json.NewDecoder(w.Body).Decode(&got); err != nil {
		t.Fatalf("decode body: %v", err)
	}
	if got.ID != 1 || got.Name != "alpha" {
		t.Fatalf("item = %+v, want {ID:1 Name:alpha}", got)
	}
	if ct := w.Header().Get("Content-Type"); ct != "application/json; charset=utf-8" {
		t.Fatalf("Content-Type = %q, want JSON content type", ct)
	}
}

func TestCreateItem_validation(t *testing.T) {
	cases := []struct {
		name string
		body any
		want int
	}{
		{"empty name", map[string]string{"name": ""}, http.StatusBadRequest},
		{"invalid json", nil, http.StatusBadRequest}, // nil → "null" body, fails decode
	}
	for _, tc := range cases {
		t.Run(tc.name, func(t *testing.T) {
			s := NewStore()
			w := do(s, http.MethodPost, "/items", tc.body)
			if w.Code != tc.want {
				t.Fatalf("status = %d, want %d", w.Code, tc.want)
			}
		})
	}
}

func TestCreateItem_rejectsUnknownTrailingAndOversizedJSON(t *testing.T) {
	for _, body := range []string{
		`{"name":"alpha","unexpected":true}`,
		`{"name":"alpha"} {}`,
		`{"name":"` + strings.Repeat("x", maxRequestBodyBytes) + `"}`,
	} {
		s := NewStore()
		r := httptest.NewRequest(http.MethodPost, "/items/", strings.NewReader(body))
		w := httptest.NewRecorder()
		s.Router().ServeHTTP(w, r)
		if w.Code != http.StatusBadRequest {
			t.Fatalf("body length %d: status = %d, want %d", len(body), w.Code, http.StatusBadRequest)
		}
	}
}

func TestListItems(t *testing.T) {
	s := NewStore()
	do(s, http.MethodPost, "/items", map[string]string{"name": "a"})
	do(s, http.MethodPost, "/items", map[string]string{"name": "b"})

	w := do(s, http.MethodGet, "/items", nil)
	if w.Code != http.StatusOK {
		t.Fatalf("status = %d, want %d", w.Code, http.StatusOK)
	}
	var got []Item
	if err := json.NewDecoder(w.Body).Decode(&got); err != nil {
		t.Fatalf("decode body: %v", err)
	}
	if len(got) != 2 {
		t.Fatalf("len(items) = %d, want 2", len(got))
	}
	if got[0].ID != 1 || got[1].ID != 2 {
		t.Fatalf("items = %+v, want ID order", got)
	}
}

func TestStore_concurrentCreateAndNoClientDataInLogs(t *testing.T) {
	var logs bytes.Buffer
	s := NewStoreWithLogger(slog.New(slog.NewJSONHandler(&logs, nil)))
	const requests = 20
	var group sync.WaitGroup
	for i := 0; i < requests; i++ {
		group.Add(1)
		go func() {
			defer group.Done()
			w := do(s, http.MethodPost, "/items", map[string]string{"name": "client-secret"})
			if w.Code != http.StatusCreated {
				t.Errorf("status = %d, want %d", w.Code, http.StatusCreated)
			}
		}()
	}
	group.Wait()
	if strings.Contains(logs.String(), "client-secret") {
		t.Fatalf("logs contain client data: %s", logs.String())
	}
	w := do(s, http.MethodGet, "/items", nil)
	var items []Item
	if err := json.NewDecoder(w.Body).Decode(&items); err != nil {
		t.Fatalf("decode list: %v", err)
	}
	if len(items) != requests {
		t.Fatalf("len(items) = %d, want %d", len(items), requests)
	}
}

func TestGetItem_foundAndNotFound(t *testing.T) {
	s := NewStore()
	do(s, http.MethodPost, "/items", map[string]string{"name": "alpha"}) // ID 1

	w := do(s, http.MethodGet, "/items/1", nil)
	if w.Code != http.StatusOK {
		t.Fatalf("GET /items/1: status = %d, want %d", w.Code, http.StatusOK)
	}

	w = do(s, http.MethodGet, "/items/999", nil)
	if w.Code != http.StatusNotFound {
		t.Fatalf("GET /items/999: status = %d, want %d", w.Code, http.StatusNotFound)
	}

	w = do(s, http.MethodGet, "/items/notanint", nil)
	if w.Code != http.StatusBadRequest {
		t.Fatalf("GET /items/notanint: status = %d, want %d", w.Code, http.StatusBadRequest)
	}
}
