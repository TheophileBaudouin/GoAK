package main

import (
	"bytes"
	"context"
	"errors"
	"fmt"
	"net/http"
	"net/http/httptest"
	"os"

	"github.com/getkin/kin-openapi/openapi3filter"

	openapivalidation "go-agent-kit-v2/recipes/recipe-openapi-validation"
)

func main() {
	validator, err := openapivalidation.New(context.Background(), openapivalidation.Config{
		Spec: openapivalidation.ExampleSpec, MaxBodyBytes: 1024,
		AuthenticationFunc: func(_ context.Context, input *openapi3filter.AuthenticationInput) error {
			if input.RequestValidationInput.Request.Header.Get("Authorization") != "Bearer probe" {
				return errors.New("invalid probe authentication")
			}
			return nil
		},
	})
	if err != nil {
		fail(err)
	}
	handler := validator.Middleware(http.HandlerFunc(func(w http.ResponseWriter, _ *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusCreated)
		_, _ = w.Write([]byte(`{"id":1}`))
	}))
	request := httptest.NewRequest(http.MethodPost, "/widgets", bytes.NewBufferString(`{"name":"probe"}`))
	request.Header.Set("Content-Type", "application/json")
	request.Header.Set("Authorization", "Bearer probe")
	response := httptest.NewRecorder()
	handler.ServeHTTP(response, request)
	if response.Code != http.StatusCreated || response.Body.String() != `{"id":1}` {
		fail(fmt.Errorf("validated response is %d %q", response.Code, response.Body.String()))
	}
	fmt.Println("openapi-validation: PASS")
}

func fail(err error) {
	fmt.Fprintln(os.Stderr, "openapi-validation:", err)
	os.Exit(1)
}
