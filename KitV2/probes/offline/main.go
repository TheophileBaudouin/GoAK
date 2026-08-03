package main

import (
	"context"
	"fmt"
	"os"
	"strings"

	"go-agent-kit-v2/tools/offline"
)

func main() {
	root := "tools/offline/bundle"
	resolver, err := offline.Open(root)
	if err != nil {
		fail(err)
	}
	if err := resolver.Verify(); err != nil {
		fail(err)
	}
	checks := []offline.Query{
		{Source: "pkg-doc", Unit: "fmt"},
		{Source: "pkg-doc", Unit: "github.com/spf13/cobra"},
		{Source: "pkg-doc", Unit: "github.com/spf13/viper"},
		{Source: "pkg-doc", Unit: "github.com/knadh/koanf/v2"},
		{Source: "toolchain", Unit: "help:testflag"},
		{Source: "toolchain", Unit: "cmd:gofmt"},
	}
	for _, query := range checks {
		result := resolver.Resolve(context.Background(), query)
		if result.Status != offline.StatusHit || len(result.Matches) == 0 {
			fail(fmt.Errorf("%s/%s: unexpected result: %+v", query.Source, query.Unit, result))
		}
	}
	blocked := resolver.Resolve(context.Background(), offline.Query{Source: "pkg-doc", Unit: "not/a/real/package"})
	if blocked.Status != offline.StatusBlocked || !strings.Contains(blocked.Prerequisite, "cache") {
		fail(fmt.Errorf("blocked prerequisite missing: %+v", blocked))
	}
	fmt.Println("offline: PASS")
}

func fail(err error) {
	fmt.Fprintln(os.Stderr, "offline: FAIL:", err)
	os.Exit(1)
}
