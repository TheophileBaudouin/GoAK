package snippet

import "fmt"

// WrapBoundary adds context at an error boundary.
func WrapBoundary(err error) error {
	if err == nil {
		return nil
	}
	return fmt.Errorf("load record: %w", err)
}
