package offline

import (
	"fmt"
	"strings"
)

type indexRecord struct {
	unit string
	ref  string
	sha  string
}

func (r *Resolver) loadIndex(s source) ([]indexRecord, error) {
	path, err := safeJoin(r.root, s.Index)
	if err != nil {
		return nil, fmt.Errorf("source %q index: %w", s.ID, err)
	}
	data, err := readFile(path)
	if err != nil {
		return nil, fmt.Errorf("read index %q: %w", s.ID, err)
	}
	if len(data) > maxIndexBytes {
		return nil, fmt.Errorf("index %q exceeds %d bytes", s.ID, maxIndexBytes)
	}
	if digest(data) != s.IndexSHA256 {
		return nil, fmt.Errorf("index %q checksum mismatch", s.ID)
	}
	trimmed := strings.TrimSuffix(string(data), "\n")
	if trimmed == "" {
		return nil, fmt.Errorf("index %q is empty", s.ID)
	}
	records := make([]indexRecord, 0)
	previous := ""
	for _, line := range strings.Split(trimmed, "\n") {
		fields := strings.Split(line, "\t")
		if len(fields) != 3 || fields[0] == "" || fields[1] == "" || fields[2] == "" {
			return nil, fmt.Errorf("index %q has malformed record", s.ID)
		}
		if previous != "" && fields[0] <= previous {
			return nil, fmt.Errorf("index %q is not strictly sorted", s.ID)
		}
		rel, err := safeJoin(r.root, fields[1])
		if err != nil {
			return nil, fmt.Errorf("index %q blob %q: %w", s.ID, fields[1], err)
		}
		if rel == r.root {
			return nil, fmt.Errorf("index %q blob path is empty", s.ID)
		}
		records = append(records, indexRecord{unit: fields[0], ref: fields[1], sha: fields[2]})
		previous = fields[0]
	}
	return records, nil
}
