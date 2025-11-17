#!/usr/bin/env python3
"""
Listens on all IPv6 interfaces and issues a 301 redirect to
http://x.marks.the.spot.ept/flag.txt for any incoming GET request.
"""
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import socket

PORT = 80
TARGET = "http://x.marks.the.spot.ept/flag.txt"

class RedirectHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # send 301 redirect to TARGET
        self.send_response(301)
        self.send_header("Location", TARGET)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(f"Moved permanently to {TARGET}\n".encode("utf-8"))

    def do_HEAD(self):
        self.send_response(301)
        self.send_header("Location", TARGET)
        self.end_headers()

    def log_message(self, fmt, *args):
        # simple logging to stdout
        print(f"{self.address_string()} - {fmt % args}")


def run():
    # Create server bound to IPv6 '::' on given port
    server_address = ("::", PORT)

    # ThreadingHTTPServer uses socket.DEFAULT_TIMEOUT etc; override address_family to AF_INET6
    class IPv6ThreadingHTTPServer(ThreadingHTTPServer):
        address_family = socket.AF_INET6

    httpd = IPv6ThreadingHTTPServer(server_address, RedirectHandler)
    httpd.allow_reuse_address = True

    print(f"Redirector listening on [::]:{PORT} -> redirects to {TARGET}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
        httpd.server_close()


if __name__ == "__main__":
    run()