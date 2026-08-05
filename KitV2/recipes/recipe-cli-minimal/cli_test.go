package cli

import (
	"bytes"
	"errors"
	"flag"
	"io"
	"reflect"
	"testing"
)

func TestParse_defaults(t *testing.T) {
	c, err := ParseTo(nil, io.Discard)
	if err != nil {
		t.Fatalf("ParseTo(nil) error: %v", err)
	}
	want := Config{Host: "127.0.0.1", Port: 8080, Verbose: false}
	if !reflect.DeepEqual(c, want) {
		t.Fatalf("Config = %+v, want %+v", c, want)
	}
}

func TestParse_customValues(t *testing.T) {
	c, err := ParseTo([]string{"-host", "0.0.0.0", "-port", "9090", "-verbose"}, io.Discard)
	if err != nil {
		t.Fatalf("ParseTo error: %v", err)
	}
	want := Config{Host: "0.0.0.0", Port: 9090, Verbose: true}
	if !reflect.DeepEqual(c, want) {
		t.Fatalf("Config = %+v, want %+v", c, want)
	}
}

func TestParse_unknownFlagReturnsErrorAndUsage(t *testing.T) {
	var buf bytes.Buffer
	_, err := ParseTo([]string{"-bogus"}, &buf)
	if err == nil {
		t.Fatal("expected error for unknown flag, got nil")
	}
	// ContinueOnError prints usage to the FlagSet output before returning.
	if !bytes.Contains(buf.Bytes(), []byte("bogus")) && !bytes.Contains(buf.Bytes(), []byte("Usage")) {
		t.Fatalf("expected usage mentioning the bad flag, got: %q", buf.String())
	}
}

func TestParse_invalidIntReturnsError(t *testing.T) {
	_, err := ParseTo([]string{"-port", "not-a-number"}, io.Discard)
	if err == nil {
		t.Fatal("expected error for invalid int value, got nil")
	}
}

func TestParse_helpIsErrHelp(t *testing.T) {
	_, err := ParseTo([]string{"-h"}, io.Discard)
	if !errors.Is(err, flag.ErrHelp) {
		t.Fatalf("err = %v, want flag.ErrHelp", err)
	}
}

func TestParse_rejectsPositionalArguments(t *testing.T) {
	_, err := ParseTo([]string{"Ada"}, io.Discard)
	if err == nil {
		t.Fatal("ParseTo() error = nil, want positional-argument error")
	}
}

func TestParse_nilWriter(t *testing.T) {
	if _, err := ParseTo(nil, nil); err != nil {
		t.Fatalf("ParseTo(nil, nil) error = %v", err)
	}
}
