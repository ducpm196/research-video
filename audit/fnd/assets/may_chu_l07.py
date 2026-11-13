import sys
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

TRANG = {"/": "xin chao", "/so_du": "1500000", "/het_han": '{"loi": "het han"}'}


class Xu(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def tra(self, ma, ten, nd):
        nd = nd.encode()
        self.send_response_only(ma, ten)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(nd)))
        self.end_headers()
        self.wfile.write(nd)

    def do_GET(self):
        p = self.path
        if p in TRANG:
            self.tra(200, "OK", TRANG[p])
        elif p == "/chuyen":
            self.tra(405, "Method Not Allowed", "chi nhan POST")
        elif p == "/loi":
            self.tra(500, "Internal Server Error", "loi may chu")
        elif p == "/cham":
            time.sleep(3)
            self.tra(200, "OK", "xong")
        else:
            self.tra(404, "Not Found", "khong thay")

    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        nd = self.rfile.read(n).decode()
        if self.path == "/chuyen":
            self.tra(201, "Created", "da nhan: " + nd)
        else:
            self.tra(404, "Not Found", "khong thay")

    def log_message(self, *a):
        pass


HTTPServer(("127.0.0.1", int(sys.argv[1])), Xu).serve_forever()
