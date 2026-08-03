package main

import (
	"bytes"
	"fmt"
	"io"
	"net/http"
	"net/http/httptest"
	"os"

	restchi "go-agent-kit-v2/recipes/recipe-rest-chi"
)

func main() {
	server := httptest.NewServer(restchi.NewStore().Router())
	defer server.Close()

	request, err := http.NewRequest(http.MethodPost, server.URL+"/items", bytes.NewBufferString(`{"name":"probe"}`))
	if err != nil {
		fail(err)
	}
	request.Header.Set("Content-Type", "application/json")
	response, err := http.DefaultClient.Do(request)
	if err != nil {
		fail(err)
	}
	defer func() { _ = response.Body.Close() }()
	body, err := io.ReadAll(response.Body)
	if err != nil {
		fail(err)
	}
	if response.StatusCode != http.StatusCreated || string(body) != "{\"id\":1,\"name\":\"probe\"}\n" {
		fail(fmt.Errorf("unexpected response: status=%d body=%q", response.StatusCode, body))
	}
	fmt.Println("rest-chi: PASS")
}

func fail(err error) {
	fmt.Fprintln(os.Stderr, err)
	os.Exit(1)
}
