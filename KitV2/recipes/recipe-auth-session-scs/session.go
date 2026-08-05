// Package authsessionscs demonstrates browser sessions with scs and an
// explicit CSRF synchronizer-token boundary.
package authsessionscs

import (
	"context"
	"crypto/rand"
	"crypto/subtle"
	"encoding/base64"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"net/http"
	"strings"

	"github.com/alexedwards/scs/v2"
)

const (
	csrfKey   = "csrf"
	userIDKey = "user_id"
)

var (
	// ErrInvalidCredentials lets a verifier identify an expected login failure.
	ErrInvalidCredentials = errors.New("invalid credentials")
	errCSRF               = errors.New("csrf token mismatch")
)

// VerifyFunc verifies submitted credentials and returns the authenticated
// subject. Implementations must not log passwords or return them in errors.
type VerifyFunc func(ctx context.Context, email, password string) (subject string, err error)

// Server owns the small HTTP boundary. Session state is deliberately explicit
// so a consumer can attach an admitted persistent store when it needs one.
type Server struct {
	sessions *scs.SessionManager
	verify   VerifyFunc
}

// NewSessionManager returns the secure browser-cookie defaults for this recipe.
// scs uses in-memory storage by default; it is appropriate only for tests or a
// single process and must be replaced explicitly for a multi-replica service.
func NewSessionManager() *scs.SessionManager {
	sessions := scs.New()
	sessions.Cookie.Name = "session"
	sessions.Cookie.Secure = true
	sessions.Cookie.HttpOnly = true
	sessions.Cookie.SameSite = http.SameSiteStrictMode
	return sessions
}

// New validates the injected dependencies and returns a handler factory.
func New(sessions *scs.SessionManager, verify VerifyFunc) (*Server, error) {
	if sessions == nil {
		return nil, errors.New("session manager is required")
	}
	if verify == nil {
		return nil, errors.New("credential verifier is required")
	}

	// The security attributes are invariants of this browser recipe even when
	// callers construct the manager themselves.
	sessions.Cookie.Secure = true
	sessions.Cookie.HttpOnly = true
	sessions.Cookie.SameSite = http.SameSiteStrictMode

	return &Server{sessions: sessions, verify: verify}, nil
}

// Router returns the complete session route set wrapped in scs.LoadAndSave.
func (s *Server) Router() http.Handler {
	mux := http.NewServeMux()
	mux.HandleFunc("GET /csrf", s.csrf)
	mux.HandleFunc("POST /login", s.login)
	mux.HandleFunc("POST /logout", s.logout)
	mux.Handle("GET /protected", s.requireUser(http.HandlerFunc(s.protected)))
	return s.sessions.LoadAndSave(mux)
}

func (s *Server) csrf(w http.ResponseWriter, r *http.Request) {
	token, err := newToken()
	if err != nil {
		writeError(w, http.StatusInternalServerError, "internal server error")
		return
	}
	s.sessions.Put(r.Context(), csrfKey, token)
	writeJSON(w, http.StatusOK, map[string]string{"csrf_token": token})
}

func (s *Server) login(w http.ResponseWriter, r *http.Request) {
	if err := s.validateCSRF(r); err != nil {
		writeError(w, http.StatusForbidden, "csrf validation failed")
		return
	}

	var input struct {
		Email    string `json:"email"`
		Password string `json:"password"`
	}
	decoder := json.NewDecoder(http.MaxBytesReader(w, r.Body, 8<<10))
	decoder.DisallowUnknownFields()
	if err := decoder.Decode(&input); err != nil || strings.TrimSpace(input.Email) == "" || input.Password == "" {
		writeError(w, http.StatusBadRequest, "invalid login request")
		return
	}
	if err := decoder.Decode(&struct{}{}); !errors.Is(err, io.EOF) {
		writeError(w, http.StatusBadRequest, "invalid login request")
		return
	}

	subject, err := s.verify(r.Context(), input.Email, input.Password)
	if err != nil || strings.TrimSpace(subject) == "" {
		// Do not disclose whether the account exists or why verification failed.
		writeError(w, http.StatusUnauthorized, "invalid credentials")
		return
	}

	if err := s.sessions.RenewToken(r.Context()); err != nil {
		writeError(w, http.StatusInternalServerError, "internal server error")
		return
	}
	csrfToken, err := newToken()
	if err != nil {
		writeError(w, http.StatusInternalServerError, "internal server error")
		return
	}
	s.sessions.Put(r.Context(), userIDKey, subject)
	s.sessions.Put(r.Context(), csrfKey, csrfToken)
	writeJSON(w, http.StatusOK, map[string]string{"csrf_token": csrfToken})
}

func (s *Server) logout(w http.ResponseWriter, r *http.Request) {
	if err := s.validateCSRF(r); err != nil {
		writeError(w, http.StatusForbidden, "csrf validation failed")
		return
	}
	if s.sessions.GetString(r.Context(), userIDKey) == "" {
		writeError(w, http.StatusUnauthorized, "authentication required")
		return
	}
	if err := s.sessions.Destroy(r.Context()); err != nil {
		writeError(w, http.StatusInternalServerError, "internal server error")
		return
	}
	w.WriteHeader(http.StatusNoContent)
}

func (s *Server) protected(w http.ResponseWriter, r *http.Request) {
	writeJSON(w, http.StatusOK, map[string]string{"subject": s.sessions.GetString(r.Context(), userIDKey)})
}

func (s *Server) requireUser(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if s.sessions.GetString(r.Context(), userIDKey) == "" {
			writeError(w, http.StatusUnauthorized, "authentication required")
			return
		}
		next.ServeHTTP(w, r)
	})
}

func (s *Server) validateCSRF(r *http.Request) error {
	expected := s.sessions.GetString(r.Context(), csrfKey)
	provided := r.Header.Get("X-CSRF-Token")
	if expected == "" || provided == "" || subtle.ConstantTimeCompare([]byte(expected), []byte(provided)) != 1 {
		return errCSRF
	}
	return nil
}

func newToken() (string, error) {
	bytes := make([]byte, 32)
	if _, err := rand.Read(bytes); err != nil {
		return "", fmt.Errorf("generate csrf token: %w", err)
	}
	return base64.RawURLEncoding.EncodeToString(bytes), nil
}

func writeJSON(w http.ResponseWriter, status int, value any) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	if err := json.NewEncoder(w).Encode(value); err != nil {
		return
	}
}

func writeError(w http.ResponseWriter, status int, message string) {
	writeJSON(w, status, map[string]string{"error": message})
}
