# Phụ thuộc của bài BNX L19 (Redis nâng cao)

Bài không tải tệp thư viện nào; chỉ dùng **ảnh Docker chính thức của Redis** (Docker Hub, kho `library/redis`).

| Thứ | Thẻ | Mã băm (docker image inspect, 2026-11-11) | Ghi chú |
|---|---|---|---|
| Ảnh Docker `redis` | `redis:8.10.3` (cùng mã băm với `redis:8` lúc kéo) | `redis@sha256:1f88291b4c57bdf249f02eb085a8669889b2d2954e91d4de5118a5da6b78dd53` | `redis-server --version` in: `Redis server v=8.10.3 sha=00000000:1 malloc=jemalloc-5.3.0 bits=64 build=fa199f3d245589d0`; kích thước 55 618 749 byte |

Kéo lại: `docker pull redis:8.10.3` (ghim băm: `docker pull redis@sha256:1f88291b4c57bdf249f02eb085a8669889b2d2954e91d4de5118a5da6b78dd53`).

Cách dùng: `audit/bnx/ver/l19.py` và các khối bash trong `audit/bnx/screen/l19.yaml` tự dựng container **`bnx-l19-redis`**
(ba tiến trình `redis-server` ở cổng 7000, 7001, 7002 trong MỘT container, bật `cluster-enabled`, tạo cụm bằng
`redis-cli --cluster create … --cluster-yes`) rồi tự gỡ bằng `docker rm -f bnx-l19-redis`. Không mở cổng ra máy chủ, không chạm `bnx-ora`, `bnx-mss`.
Thiếu Docker hoặc thiếu ảnh: bộ kiểm trả SKIP (cổng FAIL, NOT_VERIFIED). Lệnh `DELEX … IFEQ` cần Redis ≥ 8.4.
