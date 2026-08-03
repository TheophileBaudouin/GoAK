package offline

import "unicode/utf8"

const bytesPerToken = 4

func excerpt(data []byte, q Query) string {
	tokens := q.BudgetTokens
	maxTokens := 512
	if q.Full {
		maxTokens = 8000
	}
	if tokens <= 0 {
		tokens = defaultBudget
		if q.Full {
			tokens = 8000
		}
	}
	if tokens > maxTokens {
		tokens = maxTokens
	}
	return truncate(data, tokens*bytesPerToken)
}

func truncate(data []byte, max int) string {
	marker := "\n…[truncated]\n"
	if len(data) <= max {
		return string(data)
	}
	cut := max - len(marker)
	if cut < 0 {
		cut = 0
	}
	for cut > 0 && !utf8.Valid(data[:cut]) {
		cut--
	}
	return string(data[:cut]) + marker
}

func limitMatches(matches []Match, q Query) []Match {
	limit := q.Limit
	if limit <= 0 {
		limit = defaultLimit
	}
	if len(matches) > limit {
		matches = matches[:limit]
	}
	budget := q.BudgetTokens
	if budget <= 0 {
		budget = defaultBudget
		if q.Full {
			budget = 8000
		}
	}
	if q.Full && budget > 8000 {
		budget = 8000
	}
	max := budget * bytesPerToken
	used := 0
	out := matches[:0]
	for _, match := range matches {
		if used+len(match.Excerpt) > max {
			break
		}
		out = append(out, match)
		used += len(match.Excerpt)
	}
	return out
}
