# Phụ thuộc của bài BNX L20 (Go cho backend: luồng nhẹ, kênh, dịch vụ HTTP, Fiber)

Chỉ MỘT thư viện ngoài chính: **Fiber v2.52.16** (`github.com/gofiber/fiber/v2`), đặt ở `audit/bnx/deps/l20/fiber/` (module `bnxl20fiber`, `go 1.25.5`).
Các chương trình Go khác của bài chỉ dùng thư viện chuẩn của Go (`fmt`, `errors`, `sync`, `sync/atomic`, `net/http`, `net`, `io`, `strconv`, `runtime`, `time`, `strings`).

Máy chạy thật: `go version go1.25.5 windows/amd64`; `-race` cần cgo: `CGO_ENABLED=1`, trình biên dịch C `gcc` của w64devkit (`C:\tools\w64devkit\bin\gcc`) có trong PATH.
Thiếu `go` hoặc thiếu gcc (cho `-race`): bộ kiểm `audit/bnx/ver/l20.py` trả SKIP (cổng FAIL có nhãn NOT_VERIFIED).

| Tệp | sha256 | Ghi chú |
|---|---|---|
| `fiber/go.mod` | `01a2aa78f9711a184ed2b0e29bd19afcc661c1c010fe70807179664413aec433` | yêu cầu `github.com/gofiber/fiber/v2 v2.52.16` |
| `fiber/go.sum` | `7565b879f87b8a075982fcc5b1e9fbf731ea7f7498491933cb57c0d28bd5267a` | các băm `h1:` do Go tính (cơ sở dữ liệu tổng kiểm của Go) |
| `fiber/main.go` | `de8f50c4fb712c9256784a78680b07598fbb8c0d1b74ecd0f40e7cae9dd48a28` | chương trình hiện trên màn hình (hằng `G_FIBER` ở `audit/bnx/src/l20.py`; `ver/l20.py` so nguyên văn) |

Tệp zip của mô-đun trong bộ nhớ đệm mô-đun Go (`go env GOMODCACHE`, thư mục `cache/download/…/@v/`), sha256 tính 2026-11-12:

| Mô-đun | Phiên bản | sha256 của tệp .zip | Byte |
|---|---|---|---|
| github.com/gofiber/fiber/v2 | v2.52.16 (thẻ git, hash `9407e6ec419fc1bd26c9297ba9e32ddeaafc27e5`) | `19c1e1e7282933368d1a23dcf8ebeeb0fcf78534c07dcb661c8fb680cd19aaca` | 1023734 |
| github.com/valyala/fasthttp | v1.51.0 | `137680b8144e4da9ac9d49687187380bdba1b688cbc56c630a0709ebcffcf03c` | 305473 |
| github.com/andybalholm/brotli | v1.1.0 | `61bc9b753662e2101c63bfc9562f660e9ceca9866010948f1aaccb05cf9e263a` | 1882316 |
| github.com/google/uuid | v1.6.0 | `d0f02f377217f42702e259684e06441edbf5140dddcc34ba9bea56038b38a6ed` | 31981 |
| github.com/klauspost/compress | v1.17.9 | `a009d53eecbdb9d6b789e9a0662fa41c87a85ab280291b2b5a5d9664bb1c5e8f` | 38853521 |
| github.com/mattn/go-colorable | v0.1.13 | `08be322dcc584a9fcfde5caf0cf878b4e11cd98f252e32bc704e92c5a4ba9d15` | 13909 |
| github.com/mattn/go-isatty | v0.0.20 | `f2d5f89ca451577e17464b9bb596dc0d0ecececb5eaa63622c41b57cd0b7b8cc` | 8936 |
| github.com/mattn/go-runewidth | v0.0.16 | `179d2d900c76ee3560fbeda60d0237a3be6acb734d0cb7423b55e5ccb0cedbca` | 22002 |
| github.com/rivo/uniseg | v0.2.0 | `3199d94be50284142220662ca3b00e19ddd1debe4e80ddc745ff4203ecb601c0` | 45731 |
| github.com/valyala/bytebufferpool | v1.0.0 | `7f59f32c568539afee9a21a665a4156962b019beaac8404e26ba37af056b4f1e` | 7534 |
| github.com/valyala/tcplisten | v1.0.0 | `79dff3ed1114b89bb396b73d54dfd3999a74181859d02b261c31861c021cc1e8` | 7515 |
| golang.org/x/sys | v0.28.0 | `0ed47a83fe7d7a7e743e815172bc10c1ac0ed0d31ebb095e75717428e09aa895` | 1983555 |

Thư mục `fiber/vendor/` do `go mod vendor` sinh (đã nằm trong `.gitignore`: `audit/bnx/deps/**/vendor/`); có nó thì `go run .` chạy không cần mạng.
Dựng lại: `cd audit/bnx/deps/l20/fiber && go mod vendor` (cần mạng hoặc bộ nhớ đệm mô-đun), hoặc cứ `go run .` khi có mạng (Go tải theo `go.sum`).

Cách dùng: `audit/bnx/ver/l20.py` và khối bash trong `audit/bnx/screen/l20.yaml` chạy `go run .` trong `audit/bnx/deps/l20/fiber/`; máy chủ chỉ nghe `127.0.0.1` cổng do hệ điều hành chọn (`:0`), tự tắt (`app.Shutdown()`); không Docker, không chạm cổng khác.
