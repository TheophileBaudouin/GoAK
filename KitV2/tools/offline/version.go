package offline

import (
	"strconv"
	"strings"
)

func compatibleVersion(declared, requested string) bool {
	if requested == "" || declared == "" {
		return true
	}
	declared = strings.TrimPrefix(declared, "go")
	requested = strings.TrimPrefix(requested, "go")
	declaredParts, declaredOK := versionParts(strings.TrimSuffix(declared, "+"))
	requestedParts, requestedOK := versionParts(requested)
	if !declaredOK || !requestedOK {
		return false
	}
	if strings.HasSuffix(declared, "+") {
		for i := range declaredParts {
			if requestedParts[i] != declaredParts[i] {
				return requestedParts[i] > declaredParts[i]
			}
		}
		return true
	}
	return declaredParts == requestedParts
}

func versionParts(value string) ([3]int, bool) {
	var parts [3]int
	fields := strings.Split(value, ".")
	if len(fields) > len(parts) {
		return parts, false
	}
	for i, field := range fields {
		parsed, err := strconv.Atoi(field)
		if err != nil || parsed < 0 {
			return parts, false
		}
		parts[i] = parsed
	}
	return parts, true
}
