import json
import threading
import socket
from datetime import datetime, timezone
from http.client import HTTPConnection
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit


def make_handler(case_sensitive=False, strict_routing=False, suppress_head_body=True, options_includes_head=True, explicit_options_override=True, query_in_path=False):
    def route_matches(path):
        pathname = path if query_in_path else urlsplit(path).path
        expected = "/widgets"
        actual = pathname
        if not strict_routing:
            actual = actual.rstrip("/") or "/"
            expected = expected.rstrip("/") or "/"
        if not case_sensitive:
            actual = actual.casefold()
            expected = expected.casefold()
        return actual == expected

    class Handler(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"

        def log_message(self, *_args):
            pass

        def send_result(self, status, body, allow=None, suppress_body=False):
            encoded = body.encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(encoded)))
            if allow is not None:
                self.send_header("Allow", allow)
            self.send_header("Connection", "close")
            self.end_headers()
            if not suppress_body:
                self.wfile.write(encoded)
            self.close_connection = True

        def do_GET(self):
            if route_matches(self.path):
                self.send_result(200, "get")
            else:
                self.send_result(404, "not found")

        def do_HEAD(self):
            if route_matches(self.path):
                self.send_result(200, "get", suppress_body=suppress_head_body)
            else:
                self.send_result(404, "not found", suppress_body=True)

        def do_PUT(self):
            if route_matches(self.path):
                self.send_result(200, "put")
            else:
                self.send_result(404, "not found")

        def do_OPTIONS(self):
            pathname = urlsplit(self.path).path
            if pathname == "/override" and explicit_options_override:
                self.send_result(200, "GET", allow="GET")
            elif route_matches(self.path):
                methods = "GET, HEAD, PUT" if options_includes_head else "GET, PUT"
                self.send_result(200, methods, allow=methods)
            else:
                self.send_result(404, "not found")

    return Handler


def raw_head_body_bytes(host, port):
    chunks = []
    with socket.create_connection((host, port), timeout=5) as client:
        client.sendall(b"HEAD /widgets HTTP/1.1\r\nHost: 127.0.0.1\r\nConnection: close\r\n\r\n")
        while True:
            chunk = client.recv(4096)
            if not chunk:
                break
            chunks.append(chunk)
    raw = b"".join(chunks)
    separator = raw.find(b"\r\n\r\n")
    return 0 if separator < 0 else len(raw) - separator - 4


def capture(case_sensitive=False, strict_routing=False, suppress_head_body=True, options_includes_head=True, explicit_options_override=True, query_in_path=False):
    server = ThreadingHTTPServer(
        ("127.0.0.1", 0),
        make_handler(case_sensitive, strict_routing, suppress_head_body, options_includes_head, explicit_options_override, query_in_path),
    )
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    host, port = server.server_address
    requests = [
        ("get-base", "GET", "/widgets"),
        ("head-fallback", "HEAD", "/widgets"),
        ("options-auto", "OPTIONS", "/widgets"),
        ("options-missing", "OPTIONS", "/missing"),
        ("options-explicit", "OPTIONS", "/override"),
        ("case-and-trailing-slash", "GET", "/WIDGETS/"),
        ("query-ignored", "GET", "/widgets?color=blue"),
    ]
    scenarios = []
    try:
        for label, method, path in requests:
            connection = HTTPConnection(host, port, timeout=5)
            connection.request(method, path, headers={"Connection": "close"})
            response = connection.getresponse()
            body = response.read().decode("utf-8")
            headers = {
                "content-type": response.getheader("Content-Type"),
                "content-length": response.getheader("Content-Length"),
                "allow": response.getheader("Allow"),
            }
            scenarios.append({
                "label": label,
                "request": {"method": method, "path": path},
                "response": {
                    "status": response.status,
                    "headers": headers,
                    "body": body,
                },
            })
            connection.close()
        scenarios[1]["response"]["wireBodyBytes"] = raw_head_body_bytes(host, port)
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)

    return {
        "capturedAt": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "completedAt": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "implementation": "Independent Python 3.12 standard-library HTTP server",
        "configuration": {
            "caseSensitiveRouting": case_sensitive,
            "strictRouting": strict_routing,
        },
        "scenarios": scenarios,
    }


if __name__ == "__main__":
    print(json.dumps(capture(), indent=2))
