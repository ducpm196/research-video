# Bảng quyết định môi trường Thực hành & Lab Chặng 6–8 (`BN-08`)

Mỗi khoá trong Chặng 6, Chặng 7 và Chặng 8 (15 khoá = 231 bài + 3 dự án `PRJ L05–L07`) được phân loại rõ ràng giữa **thực thi thật trên công cụ hệ thống (PRODUCT/REAL)** và **mô phỏng định lượng có nhãn rõ ràng trên màn hình (SIM — ghi minh bạch `(mô phỏng định lượng)` hoặc `(trên Docker Linux cục bộ)`)** trước khi nâng cấp sang chuẩn AF2. Mọi bài đều chấm tự động qua `labs/cham.sh` bằng lời giải mẫu trong `labs/<KHOÁ>/<Lxx>/loi_giai.*`.

## Bảng xác nhận công cụ có sẵn trên máy trạm (đã đo kiểm trực tiếp)

| Công cụ | Đường dẫn / Phiên bản đã đo | Phục vụ khoá |
|---|---|---|
| Python `.venv` | `D:\research-video\.venv\Scripts\python.exe` (3.12) | `CSA`, `OSY`, `NET`, `SWF`, `SDP`, `SEC`, `DSY`, `EVT`, `DEN`, `CLD`, `CLC`, `SAR`, `PRJ` |
| GCC 16.2.0 | `C:\tools\w64devkit\bin\gcc.exe` (`-std=c11 -Wall -Wextra -Werror`) | `CPR`, `CSA`, `OSY` |
| SQLite CLI 3.46.0 | `C:\Program Files\NVIDIA Corporation\Nsight Systems 2025.1.3\host-windows-x64\sqlite3.exe` | `DBS`, `DEN`, `PRJ` |
| OpenJDK 21 LTS | `java` / `javac` Temurin `21.0.13` LTS | `SWF`, `SDP`, `JVA`, `JV2` |
| Node.js 25 | `node` `v25.8.0` | `WEB` |
| OpenSSL & Git Bash | `OpenSSL 3.5.5` + `C:\Program Files\Git\bin\bash.exe` | `SEC`, `LNX`, `DVO` |
| Docker Engine + Compose v2 | Ảnh cục bộ `postgres:17-alpine`, `redis:8.10.3`, `mongo:8`, `mysql:8.4`, `apache/kafka:3.9.0`, `prom/prometheus` | `LNX`, `DVO`, `DBS` (thử nghiệm Docker), `EVT` |

---

## Quyết định môi trường theo Chặng & Khoá

### Chặng 6 — Hệ thống cốt lõi (49 bài + `PRJ:L05`)
| Khoá | Số bài | Chế độ `cham.sh` & `screen_code` | Ranh giới Thực / Mô phỏng |
|---|---|---|---|
| `CSA` | 17 | **REAL C (`gcc`)** cho thao tác bit/endianness/cache-line stride (`L00–L05`) + **SIM Python** cho mô phỏng CPU pipeline / cache miss / ALU | Trên màn hình & đề lab ghi rõ `SIM` cho bộ mô phỏng pipeline/cache; bit-level dùng `gcc -std=c11` thật |
| `OSY` | 16 | **REAL C (`gcc`) / POSIX Bash** (`L00–L04` kích thước/ngăn xếp/tín hiệu) + **SIM Python** cho lập lịch RR/SJF, Banker deadlock, phân trang LRU/Clock | Mọi bộ lập lịch và thuật toán thay trang đánh dấu `(mô phỏng định lượng)` |
| `NET` | 16 | **REAL Python `socket` loopback / Docker `nc`** + **SIM Python** cho tính băng thông, TCP slow-start/AIMD, định tuyến bảng khoảng cách | Đóng khung TCP socket kiểm thật trên `127.0.0.1`; giao thức tổng thể là `SIM` định lượng |
| `PRJ:L05` | 1 | **REAL Python + C/Bash** — Dự án Chặng 6: Trình mô phỏng phân tích nhật ký khung & hàng đợi lập lịch đa nhân | Kết hợp đọc nhị phân + đo độ trễ thực thi |

### Chặng 7 — Kỹ thuật Phần mềm & Dữ liệu (96 bài + `PRJ:L06`)
| Khoá | Số bài | Chế độ `cham.sh` & `screen_code` | Ranh giới Thực / Mô phỏng |
|---|---|---|---|
| `SWF` | 14 | **REAL Java (`javac`/`java`) hoặc Python (`unittest`)** — tái cấu trúc hàm thuần, bất biến mô-đun, đo bao phủ nhánh | Thực thi 100% mã thật không giả lập |
| `SDP` | 18 | **REAL Python / Java** — cài đặt trực tiếp các mẫu thiết kế (Factory, Strategy, Observer, State, Adapter) + kiểm thử hợp đồng | Thực thi 100% mã thật |
| `DBS` | 18 | **REAL SQLite CLI 3.46.0 (`*.sql`)** cho toàn bộ 18 bài (`EXPLAIN QUERY PLAN`, chỉ mục B-Tree, khoá ngoại, ACID `BEGIN/ROLLBACK`) | 100% SQL thật qua `sqlite3.exe`; các tính năng riêng Postgres/MVCC nâng cao chú thích đối chiếu khái niệm |
| `DVO` | 14 | **REAL Git Bash (`git`, shell script)** + **Docker Compose** (chạy thật trong `verify_dvo.py`; `cham.sh` dùng kiểm định cấu hình YAML/trạng thái) | Lệnh Git & Docker thật trên ảnh cục bộ; không gọi registry ngoài mạng |
| `WEB` | 16 | **REAL Node.js (`v25.8.0`) / Python HTTP loopback** (`cham.sh` bổ sung hỗ trợ `*.js` via `node`) — phân tích HTTP status, CORS header, rate-limit token bucket | Thực thi thật trên tiến trình HTTP nội bộ / Node |
| `SEC` | 16 | **REAL OpenSSL 3.5.5 (`openssl`) + Python `hmac`/`hashlib`** — băm SHA-256, chữ ký HMAC, chứng chỉ X.509 tự ký, kiểm lỗ hổng SQLi (parameterized vs nối chuỗi trên SQLite) | 100% mã mật mã và câu lệnh kiểm thử SQLite thật |
| `PRJ:L06` | 1 | **REAL Python + SQLite + OpenSSL** — Dự án Chặng 7: Dịch vụ ghi nhật ký có chữ ký HMAC, chỉ mục SQLite & kiểm soát tốc độ | Bảo đảm 100% tiêu chí 100 điểm `labs/PRJ/SPEC.md` |

### Chặng 8 — Phân tán, Dữ liệu lớn & Kiến trúc (86 bài + `PRJ:L07`)
| Khoá | Số bài | Chế độ `cham.sh` & `screen_code` | Ranh giới Thực / Mô phỏng |
|---|---|---|---|
| `DSY` | 16 | **SIM Python tất định** — mô phỏng đồng hồ Lamport/Vector, quorum `R + W > N`, Raft term/vote/commit, Consistent Hashing | Bắt buộc gắn nhãn rõ `[Mô phỏng phân tán]` trên màn hình và đầu đề lab |
| `EVT` | 12 | **SIM Python tất định** (+ đối chứng khái niệm Kafka `apache/kafka:3.9.0`) — hàng đợi phân vùng, consumer group offset, outbox, DLQ | Luồng event deterministic chấm được trong `< 2s` qua `cham.sh` |
| `DEN` | 15 | **REAL SQLite / Python ETL** — lọc bản ghi trễ (watermark), hợp nhất CDC (upsert), khử trùng cửa sổ, định dạng cột Parquet-layout định lượng | Biến đổi bảng & tổng hợp chạy thật trên SQLite/Python |
| `CLD` | 16 | **SIM Python định lượng** — tính chi phí lưu trữ/EBS/Egress 3 vùng, SLA multi-AZ (`1 - (1-a)^k`), autoscale ngưỡng CPU | Tính toán tất định bằng hàm thuần Python đối chiếu `checklib` |
| `CLC` | 13 | **SIM Python định lượng** — hàng đợi M/M/c xấp xỉ, backpressure, circuit breaker 3 trạng thái, cân bằng tải nhất quán | Mô hình toán tải thực chứng |
| `SAR` | 14 | **SIM Python định lượng** — đo ghép nối kiến trúc, CQRS đồng bộ độ trễ, tách ranh giới dịch vụ & ma trận đánh đổi | Kiểm định bảng phương án bằng Python |
| `PRJ:L07` | 1 | **REAL + SIM Python** — Dự án Chặng 8: Đường ống sự kiện có Outbox, Consistent Hashing và Circuit Breaker | Đạt 100 điểm tự động qua `cham.sh PRJ L07` |
