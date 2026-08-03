package cobracli

import (
	"bytes"
	"strings"
	"testing"
)

func TestNewCommandGreets(t *testing.T) {
	var output bytes.Buffer
	command := NewCommand(&output)
	command.SetArgs([]string{"greet", "Ada", "--name", "Ada"})
	if _, err := command.ExecuteC(); err != nil {
		t.Fatalf("ExecuteC() error = %v", err)
	}
	if got := output.String(); got != "hello Ada\n" {
		t.Fatalf("output = %q, want %q", got, "hello Ada\n")
	}
}

func TestNewCommandRejectsMissingName(t *testing.T) {
	command := NewCommand(&bytes.Buffer{})
	command.SetArgs([]string{"greet", "Ada"})
	_, err := command.ExecuteC()
	if err == nil || !strings.Contains(err.Error(), "name must not be empty") {
		t.Fatalf("ExecuteC() error = %v, want validation error", err)
	}
}
