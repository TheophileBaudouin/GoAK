package main

import "testing"

func TestScaffold(t *testing.T) {
	if "go-template-monolith" == "" {
		t.Fatal("template name must not be empty")
	}
}
