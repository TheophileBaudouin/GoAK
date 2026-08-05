package snippet

import (
	"encoding/json"
	"net/http"
)

// ExampleWriteJSON encodes a JSON response with an explicit status.
func ExampleWriteJSON(w http.ResponseWriter, status int, value any) error {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	return json.NewEncoder(w).Encode(value) // pi-lens-ignore: go-bare-error
}
