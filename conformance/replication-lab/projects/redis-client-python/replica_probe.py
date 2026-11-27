import json
import os
import redis


def capture(mutations=None):
    mutations = mutations or {}
    host = os.getenv("REDIS_HOST", "127.0.0.1")
    port = int(os.getenv("REDIS_PORT", "6379"))
    client = redis.Redis(host=host, port=port, db=15, decode_responses=True,
                         socket_connect_timeout=2, socket_timeout=2)
    prefix = "software-rules:python:"
    scenarios = []

    def add(label, request, outcome, value=None):
        scenarios.append({"label": label, "request": request, "outcome": outcome, "value": value})

    try:
        add("ping", {"operation": "PING"}, "success" if client.ping() else "failure", "PONG")
        client.delete(prefix + "primary", prefix + "ttl", prefix + "list")
        client.set(prefix + "primary", "world")
        value = client.get(prefix + "primary")
        add("set-get", {"operation": "SET/GET", "logicalKey": "primary"},
            "success", "mutated" if mutations.get("skip_set") else value)
        missing = client.get(prefix + "missing")
        add("missing-get", {"operation": "GET", "logicalKey": "missing"},
            "success" if mutations.get("missing_as_value") else ("success" if missing is not None else "missing"),
            "world" if mutations.get("missing_as_value") else missing)
        add("exists", {"operation": "EXISTS", "logicalKey": "primary"},
            "success", 0 if mutations.get("skip_set") else int(client.exists(prefix + "primary")))
        client.set(prefix + "ttl", "expires", ex=60)
        ttl = int(client.pttl(prefix + "ttl"))
        add("ttl", {"operation": "PTTL", "logicalKey": "ttl"},
            "success", 0 if mutations.get("ttl_as_zero") else ("positive" if ttl > 0 else "non-positive"))
        client.delete(prefix + "list")
        client.lpush(prefix + "list", "item")
        try:
            client.get(prefix + "list")
            wrong_type = "success"
        except redis.ResponseError as error:
            wrong_type = "wrongtype" if "WRONGTYPE" in str(error).upper() else "other-error"
        add("wrongtype", {"operation": "GET", "logicalKey": "list"},
            "success" if mutations.get("wrongtype_as_success") else "failure",
            "success" if mutations.get("wrongtype_as_success") else wrong_type)
    finally:
        client.close()

    unavailable = redis.Redis(host="127.0.0.1", port=1, db=15,
                              socket_connect_timeout=0.2, socket_timeout=0.2)
    try:
        unavailable.ping()
        connection_outcome = "success"
    except redis.exceptions.ConnectionError:
        connection_outcome = "connection-error"
    except redis.exceptions.RedisError:
        connection_outcome = "other-error"
    finally:
        unavailable.close()
    if mutations.get("connection_as_success"):
        connection_outcome = "success"
    add("connection-failure", {"operation": "PING", "endpoint": "unavailable"},
        "failure" if connection_outcome != "success" else "success", connection_outcome)
    return {"implementation": "Independent Python 3.12 redis-py client", "scenarios": scenarios}


if __name__ == "__main__":
    print(json.dumps(capture(), indent=2))
