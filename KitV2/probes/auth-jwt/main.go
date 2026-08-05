package main

import (
	"fmt"
	"net/http"
	"net/http/httptest"
	"os"
	"strings"
	"time"

	authjwt "go-agent-kit-v2/recipes/recipe-auth-jwt"
)

func main() {
	auth, err := authjwt.New(authjwt.Config{
		Key: []byte(strings.Repeat("p", 32)), Issuer: "kit-probe", Audience: "probe-api", TTL: time.Minute,
	})
	if err != nil {
		fail(err)
	}
	token, err := auth.Issue("probe-user")
	if err != nil {
		fail(err)
	}
	handler := auth.Middleware(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if subject, ok := authjwt.Subject(r.Context()); !ok || subject != "probe-user" {
			fail(fmt.Errorf("validated subject missing"))
		}
		w.WriteHeader(http.StatusNoContent)
	}))
	request := httptest.NewRequest(http.MethodGet, "/private", nil)
	request.Header.Set("Authorization", "Bearer "+token)
	response := httptest.NewRecorder()
	handler.ServeHTTP(response, request)
	if response.Code != http.StatusNoContent {
		fail(fmt.Errorf("protected status = %d", response.Code))
	}
	fmt.Println("auth-jwt: PASS")
}

func fail(err error) {
	fmt.Fprintln(os.Stderr, "auth-jwt:", err)
	os.Exit(1)
}
