package snippet

import (
	"net/http/httptest"
	"strings"
	"testing"
)

func TestExampleWriteJSON(t *testing.T) {
	recorder := httptest.NewRecorder()
	if err := ExampleWriteJSON(recorder, 201, map[string]string{"name": "probe"}); err != nil {
		t.Fatalf("ExampleWriteJSON() error = %v", err)
	}
	if recorder.Code != 201 {
		t.Fatalf("status = %d, want 201", recorder.Code)
	}
	if got := recorder.Header().Get("Content-Type"); got != "application/json" {
		t.Fatalf("Content-Type = %q, want application/json", got)
	}
	if !strings.Contains(recorder.Body.String(), `"name":"probe"`) {
		t.Fatalf("body = %q, want encoded name", recorder.Body.String())
	}
}
