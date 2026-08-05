package cobracli

import (
	"bytes"
	"errors"
	"io"
	"strings"
	"testing"
)

func TestNewCommandGreets(t *testing.T) {
	var output bytes.Buffer
	command := NewCommand(&output)
	command.SetArgs([]string{"greet", "--name", "Ada"})
	if _, err := command.ExecuteC(); err != nil {
		t.Fatalf("ExecuteC() error = %v", err)
	}
	if got := output.String(); got != "hello Ada\n" {
		t.Fatalf("output = %q, want %q", got, "hello Ada\n")
	}
}

func TestNewCommandRejectsMissingName(t *testing.T) {
	command := NewCommand(&bytes.Buffer{})
	command.SetArgs([]string{"greet"})
	_, err := command.ExecuteC()
	if err == nil || !strings.Contains(err.Error(), "name must not be empty") {
		t.Fatalf("ExecuteC() error = %v, want validation error", err)
	}
}

func TestNewCommandRejectsPositionalArgument(t *testing.T) {
	command := NewCommand(&bytes.Buffer{})
	command.SetArgs([]string{"greet", "Ada", "--name", "Ada"})
	if _, err := command.ExecuteC(); err == nil {
		t.Fatal("ExecuteC() error = nil, want argument error")
	}
}

func TestNewCommandPropagatesWriteError(t *testing.T) {
	command := NewCommand(errorWriter{})
	command.SetArgs([]string{"greet", "--name", "Ada"})
	_, err := command.ExecuteC()
	if !errors.Is(err, errWrite) {
		t.Fatalf("ExecuteC() error = %v, want writer error", err)
	}
}

var errWrite = errors.New("write failed")

type errorWriter struct{}

func (errorWriter) Write([]byte) (int, error) { return 0, errWrite }

var _ io.Writer = errorWriter{}
