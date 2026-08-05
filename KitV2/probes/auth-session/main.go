package main

import (
	"bytes"
	"context"
	"crypto/tls"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"net/http/cookiejar"
	"net/http/httptest"
	"os"

	authsessionscs "go-agent-kit-v2/recipes/recipe-auth-session-scs"
)

func main() {
	app, err := authsessionscs.New(authsessionscs.NewSessionManager(), func(_ context.Context, email, password string) (string, error) {
		if email == "probe@example.test" && password == "correct" {
			return "probe-user", nil
		}
		return "", authsessionscs.ErrInvalidCredentials
	})
	if err != nil {
		fail(err)
	}
	server := httptest.NewTLSServer(app.Router())
	defer server.Close()

	jar, err := cookiejar.New(nil)
	if err != nil {
		fail(err)
	}
	client := &http.Client{Jar: jar, Transport: &http.Transport{TLSClientConfig: &tls.Config{InsecureSkipVerify: true}}} // #nosec G402 -- httptest TLS server only.
	csrf := fetchCSRF(client, server.URL)
	request, err := http.NewRequest(http.MethodPost, server.URL+"/login", bytes.NewBufferString(`{"email":"probe@example.test","password":"correct"}`))
	if err != nil {
		fail(err)
	}
	request.Header.Set("Content-Type", "application/json")
	request.Header.Set("X-CSRF-Token", csrf)
	response, err := client.Do(request)
	if err != nil {
		fail(err)
	}
	if response.StatusCode != http.StatusOK {
		closeBody(response.Body)
		fail(fmt.Errorf("login status = %d", response.StatusCode))
	}
	var login map[string]string
	if err := json.NewDecoder(response.Body).Decode(&login); err != nil {
		closeBody(response.Body)
		fail(err)
	}
	closeBody(response.Body)
	if login["csrf_token"] == "" || login["csrf_token"] == csrf {
		fail(fmt.Errorf("login did not rotate CSRF token"))
	}

	protected, err := client.Get(server.URL + "/protected")
	if err != nil {
		fail(err)
	}
	if protected.StatusCode != http.StatusOK {
		closeBody(protected.Body)
		fail(fmt.Errorf("protected status = %d", protected.StatusCode))
	}
	closeBody(protected.Body)

	logout, err := http.NewRequest(http.MethodPost, server.URL+"/logout", nil)
	if err != nil {
		fail(err)
	}
	logout.Header.Set("X-CSRF-Token", login["csrf_token"])
	response, err = client.Do(logout)
	if err != nil {
		fail(err)
	}
	if response.StatusCode != http.StatusNoContent {
		closeBody(response.Body)
		fail(fmt.Errorf("logout status = %d", response.StatusCode))
	}
	closeBody(response.Body)

	fmt.Println("auth-session: PASS")
}

func fetchCSRF(client *http.Client, url string) string {
	response, err := client.Get(url + "/csrf")
	if err != nil {
		fail(err)
	}
	defer closeBody(response.Body)
	if response.StatusCode != http.StatusOK {
		fail(fmt.Errorf("csrf status = %d", response.StatusCode))
	}
	var payload map[string]string
	if err := json.NewDecoder(response.Body).Decode(&payload); err != nil {
		fail(err)
	}
	if payload["csrf_token"] == "" {
		fail(fmt.Errorf("missing csrf token"))
	}
	return payload["csrf_token"]
}

func closeBody(body io.Closer) {
	if err := body.Close(); err != nil {
		fail(err)
	}
}

func fail(err error) {
	fmt.Fprintln(os.Stderr, "auth-session:", err)
	os.Exit(1)
}
