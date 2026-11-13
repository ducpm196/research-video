cat > may_chu.py <<'EOF'
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer


class Xu(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def tra(self, ma, nd):
        nd = nd.encode()
        self.send_response_only(ma)
        self.send_header("Content-Length", str(len(nd)))
        self.end_headers()
        self.wfile.write(nd)

    def do_GET(self):
        if self.path == "/chao":
            self.tra(200, "xin chao tu lab")
        elif self.path == "/tai_khoan/42":
            self.tra(200, "so du 750000")
        else:
            self.tra(404, "khong thay")

    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        self.rfile.read(n)
        self.tra(201 if self.path == "/nap" else 404, "da nhan")

    def log_message(self, *a):
        pass


HTTPServer(("127.0.0.1", int(sys.argv[1])), Xu).serve_forever()
EOF
python may_chu.py 18766 > /dev/null 2>&1 &
SV=$!
for i in 1 2 3 4 5 6 7 8 9 10; do
  curl -s -o /dev/null http://127.0.0.1:18766/ && break
  sleep 0.3
done
U=http://127.0.0.1:18766
curl -s -o /dev/null -w "%{http_code}\n" $U/chao
curl -s -o /dev/null -w "%{http_code}\n" $U/khong_co
curl -s $U/tai_khoan/42; echo
curl -s -o /dev/null -w "%{http_code}\n" -X POST -d so_tien=100000 $U/nap
kill $SV
