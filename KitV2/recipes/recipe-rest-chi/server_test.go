package restchi

import (
	"bytes"
	"encoding/json"
	"net/http"
	"net/http/httptest"
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
	if ct := w.Header().Get("Content-Type"); ct != "application/json" {
		t.Fatalf("Content-Type = %q, want application/json", ct)
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
