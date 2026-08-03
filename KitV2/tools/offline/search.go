package offline

import (
	"sort"
	"strings"
)

func search(records []indexRecord, query string, mode Mode) []indexRecord {
	matches := make([]indexRecord, 0, len(records))
	for _, record := range records {
		matched := record.unit == query
		switch mode {
		case ModePrefix:
			matched = strings.HasPrefix(record.unit, query)
		case ModeContains:
			matched = strings.Contains(record.unit, query)
		}
		if matched {
			matches = append(matches, record)
		}
	}
	sort.SliceStable(matches, func(i, j int) bool {
		ri := rank(matches[i].unit, query)
		rj := rank(matches[j].unit, query)
		if ri != rj {
			return ri < rj
		}
		return matches[i].unit < matches[j].unit
	})
	return matches
}

func rank(unit, query string) int {
	if unit == query {
		return 0
	}
	if strings.HasPrefix(unit, query) {
		return 1
	}
	return 2
}
