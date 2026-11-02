#!/usr/bin/env python3
"""Check whether a URL is up, with optional scheduled repeats."""
import argparse
import http.server
import socket
import threading
import time
import urllib.error
import urllib.request

def check(url: str, timeout: float = 5.0):
    """Return (ok, status, elapsed_ms, note)."""
    start = time.monotonic()
    request = urllib.request.Request(url, headers={"User-Agent": "site-checker/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            status = response.getcode()
            return 200 <= status < 400, status, (time.monotonic() - start) * 1000, "ok"
    except urllib.error.HTTPError as exc:
        return False, exc.code, (time.monotonic() - start) * 1000, "http error"
    except (urllib.error.URLError, socket.timeout, OSError) as exc:
        return False, None, (time.monotonic() - start) * 1000, str(exc)

def demo() -> None:
    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"ok")
        def log_message(self, *args):
            pass

    server = http.server.HTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    closed = socket.socket(); closed.bind(("127.0.0.1", 0)); dead_port = closed.getsockname()[1]; closed.close()
    try:
        ok, status, ms, note = check(f"http://127.0.0.1:{server.server_address[1]}/")
        print(f"up   status={status} {ms:.1f} ms ({note})")
        ok, status, ms, note = check(f"http://127.0.0.1:{dead_port}/", timeout=1)
        print(f"down status={status} {ms:.1f} ms ({note[:60]})")
    finally:
        server.shutdown(); server.server_close()

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url", nargs="?")
    parser.add_argument("--interval", type=float, default=0, help="minutes between checks")
    parser.add_argument("--count", type=int, default=1)
    parser.add_argument("--timeout", type=float, default=5.0)
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()

    if args.demo:
        demo()
        return
    url = args.url or input("URL: ").strip()
    for index in range(args.count):
        ok, status, ms, note = check(url, args.timeout)
        stamp = time.strftime("%Y-%m-%d %H:%M:%S")
        state = "UP  " if ok else "DOWN"
        print(f"{stamp} {state} status={status} {ms:.1f} ms {note}")
        if index + 1 < args.count:
            time.sleep(max(0.0, args.interval * 60))

if __name__ == "__main__":
    main()
