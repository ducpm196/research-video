# Lab FND L07 — Hỏi một máy chủ cục bộ bằng curl

Tạo `http.sh`. **Chép nguyên khối đầu tiên dưới đây** (khoảng 55 dòng, trong đó 45 dòng Python tạo máy chủ nhỏ `may_chu.py`, rồi chạy nó ở nền cổng 18766, chờ nó sẵn sàng, đặt biến `U`): **chép đúng từng ký tự, chưa cần hiểu Python** — bài này chỉ cần biết nó trả lời các đường dẫn bên dưới. Tệp `may_chu.py` này **cũng chính là máy chủ của video** (video chạy nó ở cổng 18765), nên bạn có thể thử lại mọi phép `curl` của bài, như `/so_du`, `/chuyen`, `/het_han`, `/cham`, `/loi`:

```bash
cat > may_chu.py <<'EOF'
import sys
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

TRANG = {"/": "xin chao", "/so_du": "1500000", "/het_han": '{"loi": "het han"}', "/chao": "xin chao tu lab", "/tai_khoan/42": "so du 750000"}


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
        if self.path in ("/chuyen", "/nap"):
            self.tra(201, "Created", "da nhan: " + nd)
        else:
            self.tra(404, "Not Found", "khong thay")

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
