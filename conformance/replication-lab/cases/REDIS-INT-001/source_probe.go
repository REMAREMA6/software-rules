package main

import (
	"context"
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"errors"
	"fmt"
	"os"
	"path/filepath"
	"time"

	"github.com/redis/go-redis/v9"
)

type scenario struct {
	Label string `json:"label"`
	Request map[string]string `json:"request"`
	Outcome string `json:"outcome"`
	Value any `json:"value"`
}

func digest(file string) string {
	data, err := os.ReadFile(file)
	if err != nil { panic(err) }
	sum := sha256.Sum256(data)
	return hex.EncodeToString(sum[:])
}

func main() {
	root := os.Getenv("REDIS_SOURCE_ROOT")
	addr := os.Getenv("REDIS_ADDR")
	if root == "" || addr == "" { panic("REDIS_SOURCE_ROOT and REDIS_ADDR are required") }
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()
	client := redis.NewClient(&redis.Options{Addr: addr})
	defer client.Close()
	scenarios := make([]scenario, 0, 7)
	add := func(label, operation, logicalKey, outcome string, value any) {
		request := map[string]string{"operation": operation}
		if logicalKey != "" { request["logicalKey"] = logicalKey }
		scenarios = append(scenarios, scenario{label, request, outcome, value})
	}

	pong, err := client.Ping(ctx).Result()
	if err != nil { panic(err) }
	add("ping", "PING", "", "success", pong)

	prefix := "software-rules:go:"
	_ = client.Del(ctx, prefix+"primary", prefix+"ttl", prefix+"list").Err()
	if err := client.Set(ctx, prefix+"primary", "world", 0).Err(); err != nil { panic(err) }
	value, err := client.Get(ctx, prefix+"primary").Result()
	if err != nil { panic(err) }
	add("set-get", "SET/GET", "primary", "success", value)

	missing, err := client.Get(ctx, prefix+"missing").Result()
	if errors.Is(err, redis.Nil) {
		add("missing-get", "GET", "missing", "missing", nil)
	} else if err != nil { panic(err) } else { add("missing-get", "GET", "missing", "success", missing) }

	exists, err := client.Exists(ctx, prefix+"primary").Result()
	if err != nil { panic(err) }
	add("exists", "EXISTS", "primary", "success", exists)

	if err := client.Set(ctx, prefix+"ttl", "expires", time.Minute).Err(); err != nil { panic(err) }
	ttl, err := client.PTTL(ctx, prefix+"ttl").Result()
	if err != nil { panic(err) }
	ttlValue := "non-positive"
	if ttl > 0 { ttlValue = "positive" }
	add("ttl", "PTTL", "ttl", "success", ttlValue)

	if err := client.LPush(ctx, prefix+"list", "item").Err(); err != nil { panic(err) }
	_, err = client.Get(ctx, prefix+"list").Result()
	if err == nil { add("wrongtype", "GET", "list", "success", "success") } else if err.Error() != "" {
		add("wrongtype", "GET", "list", "failure", "wrongtype")
	}

	unavailable := redis.NewClient(&redis.Options{Addr: "127.0.0.1:1", DialTimeout: 300*time.Millisecond, ReadTimeout: 300*time.Millisecond, WriteTimeout: 300*time.Millisecond})
	_, err = unavailable.Ping(ctx).Result()
	_ = unavailable.Close()
	if err != nil { add("connection-failure", "PING", "unavailable", "failure", "connection-error") } else { add("connection-failure", "PING", "unavailable", "success", "success") }

	output := map[string]any{
		"capturedAt": time.Now().UTC().Format(time.RFC3339Nano),
		"source": "redis/go-redis pinned Go runtime",
		"sourceCommit": os.Getenv("REDIS_SOURCE_COMMIT"),
		"runtime": "Go",
		"sourceFiles": map[string]string{
			"go.mod": digest(filepath.Join(root, "go.mod")),
			"LICENSE": digest(filepath.Join(root, "LICENSE")),
		},
		"scenarios": scenarios,
	}
	encoded, err := json.MarshalIndent(output, "", "  ")
	if err != nil { panic(err) }
	fmt.Println(string(encoded))
}
