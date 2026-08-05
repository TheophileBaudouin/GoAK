package authjwt

import (
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"
	"time"

	"github.com/golang-jwt/jwt/v5"
)

var fixedNow = time.Date(2026, 8, 5, 12, 0, 0, 0, time.UTC)

func TestIssueAndMiddleware(t *testing.T) {
	t.Parallel()
	auth := newTestAuthenticator(t)
	token := mustIssue(t, auth, "user-42")
	handler := auth.Middleware(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		subject, ok := Subject(r.Context())
		if !ok || subject != "user-42" {
			t.Fatalf("Subject = %q, %t", subject, ok)
		}
		w.WriteHeader(http.StatusNoContent)
	}))

	request := httptest.NewRequest(http.MethodGet, "/private", nil)
	request.Header.Set("Authorization", "Bearer "+token)
	response := httptest.NewRecorder()
	handler.ServeHTTP(response, request)
	if response.Code != http.StatusNoContent {
		t.Fatalf("status = %d, want %d", response.Code, http.StatusNoContent)
	}
}

func TestMiddlewareRejectsInvalidTokens(t *testing.T) {
	t.Parallel()
	auth := newTestAuthenticator(t)
	valid := mustIssue(t, auth, "user-42")
	expired := mustSign(t, jwt.RegisteredClaims{
		Issuer:    "kit-test",
		Subject:   "user-42",
		Audience:  jwt.ClaimStrings{"kit-api"},
		ExpiresAt: jwt.NewNumericDate(fixedNow.Add(-time.Second)),
	})
	wrongIssuer := mustSign(t, jwt.RegisteredClaims{
		Issuer:    "other",
		Subject:   "user-42",
		Audience:  jwt.ClaimStrings{"kit-api"},
		ExpiresAt: jwt.NewNumericDate(fixedNow.Add(time.Minute)),
	})
	wrongAudience := mustSign(t, jwt.RegisteredClaims{
		Issuer:    "kit-test",
		Subject:   "user-42",
		Audience:  jwt.ClaimStrings{"other-api"},
		ExpiresAt: jwt.NewNumericDate(fixedNow.Add(time.Minute)),
	})
	missingSubject := mustSign(t, jwt.RegisteredClaims{
		Issuer:    "kit-test",
		Audience:  jwt.ClaimStrings{"kit-api"},
		ExpiresAt: jwt.NewNumericDate(fixedNow.Add(time.Minute)),
	})
	wrongMethod := mustSignMethod(t, jwt.SigningMethodHS384, jwt.RegisteredClaims{
		Issuer:    "kit-test",
		Subject:   "user-42",
		Audience:  jwt.ClaimStrings{"kit-api"},
		ExpiresAt: jwt.NewNumericDate(fixedNow.Add(time.Minute)),
	})

	for name, header := range map[string]string{
		"missing":          "",
		"not bearer":       "Basic " + valid,
		"malformed bearer": "Bearer ",
		"expired":          "Bearer " + expired,
		"wrong issuer":     "Bearer " + wrongIssuer,
		"wrong audience":   "Bearer " + wrongAudience,
		"missing subject":  "Bearer " + missingSubject,
		"wrong method":     "Bearer " + wrongMethod,
	} {
		t.Run(name, func(t *testing.T) {
			response := httptest.NewRecorder()
			request := httptest.NewRequest(http.MethodGet, "/private", nil)
			if header != "" {
				request.Header.Set("Authorization", header)
			}
			auth.Middleware(http.HandlerFunc(func(http.ResponseWriter, *http.Request) {
				t.Fatal("next handler ran for invalid token")
			})).ServeHTTP(response, request)
			if response.Code != http.StatusUnauthorized {
				t.Fatalf("status = %d, want %d", response.Code, http.StatusUnauthorized)
			}
		})
	}
}

func TestNewAndIssueValidateInputs(t *testing.T) {
	t.Parallel()
	for name, config := range map[string]Config{
		"short key": {Key: []byte("short"), Issuer: "issuer", Audience: "aud", TTL: time.Minute},
		"issuer":    {Key: []byte(strings.Repeat("k", 32)), Audience: "aud", TTL: time.Minute},
		"audience":  {Key: []byte(strings.Repeat("k", 32)), Issuer: "issuer", TTL: time.Minute},
		"ttl":       {Key: []byte(strings.Repeat("k", 32)), Issuer: "issuer", Audience: "aud"},
	} {
		t.Run(name, func(t *testing.T) {
			if _, err := New(config); err == nil {
				t.Fatal("New accepted invalid config")
			}
		})
	}
	auth := newTestAuthenticator(t)
	if _, err := auth.Issue(" "); err == nil {
		t.Fatal("Issue accepted empty subject")
	}
}

func newTestAuthenticator(t *testing.T) *Authenticator {
	t.Helper()
	auth, err := New(Config{
		Key:      []byte(strings.Repeat("k", 32)),
		Issuer:   "kit-test",
		Audience: "kit-api",
		TTL:      time.Minute,
		Now:      func() time.Time { return fixedNow },
	})
	if err != nil {
		t.Fatalf("New: %v", err)
	}
	return auth
}

func mustIssue(t *testing.T, auth *Authenticator, subject string) string {
	t.Helper()
	token, err := auth.Issue(subject)
	if err != nil {
		t.Fatalf("Issue: %v", err)
	}
	return token
}

func mustSign(t *testing.T, claims jwt.Claims) string {
	t.Helper()
	return mustSignMethod(t, jwt.SigningMethodHS256, claims)
}

func mustSignMethod(t *testing.T, method jwt.SigningMethod, claims jwt.Claims) string {
	t.Helper()
	token, err := jwt.NewWithClaims(method, claims).SignedString([]byte(strings.Repeat("k", 32)))
	if err != nil {
		t.Fatalf("sign token: %v", err)
	}
	return token
}
