package main

import (
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"time"

	"github.com/casbin/casbin/v3"
)

type request struct {
	Subject  string `json:"subject"`
	Resource string `json:"resource"`
	Action   string `json:"action"`
}

type scenario struct {
	Label    string  `json:"label"`
	Request  request `json:"request"`
	Decision string  `json:"decision"`
}

func digest(file string) string {
	data, err := os.ReadFile(file)
	if err != nil { panic(err) }
	sum := sha256.Sum256(data)
	return hex.EncodeToString(sum[:])
}

func main() {
	root := os.Getenv("CASBIN_SOURCE_ROOT")
	if root == "" { panic("CASBIN_SOURCE_ROOT is required") }
	model := filepath.Join(root, "examples", "rbac_model.conf")
	policy := filepath.Join(root, "examples", "rbac_policy.csv")
	enforcer, err := casbin.NewEnforcer(model, policy)
	if err != nil { panic(err) }

	requests := []struct {
		label string
		value request
	}{
		{"alice-data1-read", request{"alice", "data1", "read"}},
		{"alice-data1-write", request{"alice", "data1", "write"}},
		{"alice-data2-read-via-role", request{"alice", "data2", "read"}},
		{"alice-data2-write-via-role", request{"alice", "data2", "write"}},
		{"alice-data3-read", request{"alice", "data3", "read"}},
		{"bob-data2-write", request{"bob", "data2", "write"}},
		{"bob-data2-read", request{"bob", "data2", "read"}},
		{"bob-data1-read", request{"bob", "data1", "read"}},
		{"unknown-data1-read", request{"unknown", "data1", "read"}},
		{"alice-data2-delete", request{"alice", "data2", "delete"}},
	}

	scenarios := make([]scenario, 0, len(requests))
	for _, item := range requests {
		allowed, err := enforcer.Enforce(item.value.Subject, item.value.Resource, item.value.Action)
		if err != nil { panic(err) }
		decision := "deny"
		if allowed { decision = "permit" }
		scenarios = append(scenarios, scenario{item.label, item.value, decision})
	}

	output := map[string]any{
		"capturedAt": time.Now().UTC().Format(time.RFC3339Nano),
		"source": "Apache Casbin pinned Go runtime",
		"sourceCommit": os.Getenv("CASBIN_SOURCE_COMMIT"),
		"runtime": "Go",
		"sourceFiles": map[string]string{
			"model": digest(model),
			"policy": digest(policy),
		},
		"scenarios": scenarios,
	}
	encoded, err := json.MarshalIndent(output, "", "  ")
	if err != nil { panic(err) }
	fmt.Println(string(encoded))
}
