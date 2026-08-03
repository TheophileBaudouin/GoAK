package main

import "testing"

func TestScaffold(t *testing.T) {
	if "go-template-grpc" == "" {
		t.Fatal("template name must not be empty")
	}
}
