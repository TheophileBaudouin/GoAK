package main

import (
	"fmt"
	"io"
	"os"

	cli "go-agent-kit-v2/recipes/recipe-cli-minimal"
)

func main() {
	config, err := cli.ParseTo([]string{"-host", "127.0.0.1", "-port", "9090", "-verbose"}, io.Discard)
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	if config.Host != "127.0.0.1" || config.Port != 9090 || !config.Verbose {
		fmt.Fprintf(os.Stderr, "unexpected config: %+v\n", config)
		os.Exit(1)
	}
	fmt.Println("cli-minimal: PASS")
}
