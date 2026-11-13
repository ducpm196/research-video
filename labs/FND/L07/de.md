# Lab FND L07 — Hỏi một máy chủ cục bộ bằng curl

Tạo `http.sh`. **Dòng đầu chép nguyên** (tạo máy chủ nhỏ `may_chu.py`, chạy ở nền cổng 18766, chờ nó sẵn sàng, đặt biến `U`):

```bash
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
```

Rồi viết bốn lệnh `curl -s …` (mỗi lệnh in một dòng) và cuối cùng `kill $SV`:
1. **mã trạng thái** của `GET $U/chao`;
2. **mã trạng thái** của `GET $U/khong_co`;
3. **nội dung** của `GET $U/tai_khoan/42` (thêm `echo` để xuống dòng);
4. **mã trạng thái** của `POST $U/nap` với nội dung `so_tien=100000`.

Gợi ý lấy mã: `curl -s -o /dev/null -w "%{http_code}\n" URL`. Chạy `bash http.sh`; chấm: `bash labs/cham.sh FND L07 http.sh`. Cần Python và curl (có sẵn trong Git Bash). Cổng 18766 phải trống.
