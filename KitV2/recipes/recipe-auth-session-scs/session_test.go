package authsessionscs

import (
	"bytes"
	"context"
	"encoding/json"
	"net/http"
	"net/http/cookiejar"
	"net/http/httptest"
	"testing"
)

func TestSessionLoginCSRFAndLogout(t *testing.T) {
	t.Parallel()

	server := newTestServer(t, func(_ context.Context, email, password string) (string, error) {
		if email != "person@example.test" || password != "correct" {
			return "", ErrInvalidCredentials
		}
		return "user-42", nil
	})
	defer server.Close()

	client := tlsClient(t, server)
	csrfBefore := getCSRF(t, client, server.URL)
	response := postJSON(t, client, server.URL+"/login", csrfBefore, `{"email":"person@example.test","password":"correct"}`)
	if response.StatusCode != http.StatusOK {
		t.Fatalf("login status = %d, want %d", response.StatusCode, http.StatusOK)
	}
	var login map[string]string
	if err := json.NewDecoder(response.Body).Decode(&login); err != nil {
		t.Fatalf("decode login response: %v", err)
	}
	if login["csrf_token"] == "" || login["csrf_token"] == csrfBefore {
		t.Fatalf("login csrf token = %q, want fresh token", login["csrf_token"])
	}
	closeResponseBody(t, response)

	protected, err := client.Get(server.URL + "/protected")
	if err != nil {
		t.Fatalf("GET protected: %v", err)
	}
	if protected.StatusCode != http.StatusOK {
		t.Fatalf("protected status = %d, want %d", protected.StatusCode, http.StatusOK)
	}
	closeResponseBody(t, protected)

	logout := postJSON(t, client, server.URL+"/logout", login["csrf_token"], "")
	if logout.StatusCode != http.StatusNoContent {
		t.Fatalf("logout status = %d, want %d", logout.StatusCode, http.StatusNoContent)
	}
	closeResponseBody(t, logout)

	protected, err = client.Get(server.URL + "/protected")
	if err != nil {
		t.Fatalf("GET protected after logout: %v", err)
	}
	defer closeResponseBody(t, protected)
	if protected.StatusCode != http.StatusUnauthorized {
		t.Fatalf("protected after logout = %d, want %d", protected.StatusCode, http.StatusUnauthorized)
	}
}

func TestLoginRejectsMissingOrWrongCSRFBeforeVerification(t *testing.T) {
	t.Parallel()

	called := false
	server := newTestServer(t, func(context.Context, string, string) (string, error) {
		called = true
		return "user-42", nil
	})
	defer server.Close()
	client := tlsClient(t, server)
	_ = getCSRF(t, client, server.URL)

	response := postJSON(t, client, server.URL+"/login", "wrong", `{"email":"person@example.test","password":"secret"}`)
	defer closeResponseBody(t, response)
	if response.StatusCode != http.StatusForbidden {
		t.Fatalf("login status = %d, want %d", response.StatusCode, http.StatusForbidden)
	}
	if called {
		t.Fatal("verifier called before CSRF validation")
	}
}

func TestLoginRejectsInvalidCredentials(t *testing.T) {
	t.Parallel()

	server := newTestServer(t, func(context.Context, string, string) (string, error) {
		return "", ErrInvalidCredentials
	})
	defer server.Close()
	client := tlsClient(t, server)
	csrf := getCSRF(t, client, server.URL)

	response := postJSON(t, client, server.URL+"/login", csrf, `{"email":"person@example.test","password":"wrong"}`)
	defer closeResponseBody(t, response)
	if response.StatusCode != http.StatusUnauthorized {
		t.Fatalf("login status = %d, want %d", response.StatusCode, http.StatusUnauthorized)
	}
}

func TestNewRejectsMissingDependencies(t *testing.T) {
	t.Parallel()
	if _, err := New(nil, func(context.Context, string, string) (string, error) { return "", nil }); err == nil {
		t.Fatal("New accepted nil session manager")
	}
	if _, err := New(NewSessionManager(), nil); err == nil {
		t.Fatal("New accepted nil verifier")
	}
}

func newTestServer(t *testing.T, verify VerifyFunc) *httptest.Server {
	t.Helper()
	app, err := New(NewSessionManager(), verify)
	if err != nil {
		t.Fatalf("New: %v", err)
	}
	return httptest.NewTLSServer(app.Router())
}

func tlsClient(t *testing.T, server *httptest.Server) *http.Client {
	t.Helper()
	jar, err := cookiejar.New(nil)
	if err != nil {
		t.Fatalf("new cookie jar: %v", err)
	}
	client := server.Client()
	client.Jar = jar
	return client
}

func getCSRF(t *testing.T, client *http.Client, baseURL string) string {
	t.Helper()
	response, err := client.Get(baseURL + "/csrf")
	if err != nil {
		t.Fatalf("GET /csrf: %v", err)
	}
	defer closeResponseBody(t, response)
	if response.StatusCode != http.StatusOK {
		t.Fatalf("csrf status = %d, want %d", response.StatusCode, http.StatusOK)
	}
	var payload map[string]string
	if err := json.NewDecoder(response.Body).Decode(&payload); err != nil {
		t.Fatalf("decode csrf response: %v", err)
	}
	return payload["csrf_token"]
}

func postJSON(t *testing.T, client *http.Client, url, csrf, body string) *http.Response {
	t.Helper()
	request, err := http.NewRequest(http.MethodPost, url, bytes.NewBufferString(body))
	if err != nil {
		t.Fatalf("new POST request: %v", err)
	}
	request.Header.Set("Content-Type", "application/json")
	if csrf != "" {
		request.Header.Set("X-CSRF-Token", csrf)
	}
	response, err := client.Do(request)
	if err != nil {
		t.Fatalf("POST %s: %v", url, err)
	}
	return response
}

func closeResponseBody(t *testing.T, response *http.Response) {
	t.Helper()
	if err := response.Body.Close(); err != nil {
		t.Errorf("close response body: %v", err)
	}
}
