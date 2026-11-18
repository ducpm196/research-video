# fix6 BNX_B nhánh B2 (L19–L21) — 2026-11-16

## TIẾN ĐỘ
- [x] L19 xong  - [x] L20 xong  - [x] L21 xong

Khuôn: `audit/bnx/libj.py` (`jstep`, `nowrap`; không sửa). Nguồn sửa: `audit/bnx/src/l19.py, l20.py, l21.py`, sinh bằng `gen.py`; không sửa YAML sinh ra; sổ chỉ qua `screen_keep.py`. Không docker/build/tts/asr/git.

## L19 (Redis, cụm khe băm)
- Mục chưa giảng → 0: `def`/`return`, `for x in b`, `for _ in range(8)`, `A if đk else B` (dòng `c = (c << 1) ^ 0x1021 if c & 0x8000 else c << 1`), `b"foo"`, `hex()`, `print(a, b)`, danh sách sinh sẵn `[(a, a + n - 1) for a, n in …]` (hai bảng đứng TRƯỚC `PY_CRC`); `khoa.find("{")`, `khoa[a + 1:b]`, `next(i for i, (x, y) in enumerate(dai) if x <= k <= y)` (bảng trước PhanBo 1/2); `for n in (3000, 300000)`, `f"dedup:{{tx}}:{i}"`, `dem[nut(…)] += 1` (bảng trước PhanBo 2/2).
- SHOULD: ô "(×N)" bọc `nowrap()` (3 ô); ghi chú màn hình sau khối dựng cụm: "Redis 8.10.3 là ảnh dùng lúc ghi hình; chưa đối chiếu độc lập với trang phát hành (NOT_VERIFIED); `DELEX … IFEQ` có từ Redis 8.4 (cũng NOT_VERIFIED độc lập)". Không bịa nguồn.
- Không đổi văn bản bất kỳ khối mã nào (giữ sha). Lời đọc 2294 → 2292 (thêm ~255 từ bảng, cắt ~257 ở câu không có `asr_reviewed`). `asr_reviewed` 22 → 22.
- Cổng: lint 0/0; render 120 khung, 0 vấn đề (đã xem khung 36, 73); `screen_keep.py L19`: 18 khối, chưa khớp 0; sha-only (`shachk`) MISSING 0, STALE 0, ORPHAN 0; KHÔNG chạy `screen_fast` (docker). `verify_bnx.py L19` với PATH bỏ thư mục Docker: 21/22 PASS, 1 SKIP (phần docker/Redis).
- Mục chưa giảng ước còn lại: 0.

## L20 (Go)
- Mục chưa giảng → 0: `func rut(tk TaiKhoan, tien int) (TaiKhoan, error) {`, `tk := TaiKhoan{So: "001", SoDu: 500}`, `tk.SoDu -= tien`, `dem++` (bảng ba hàng trước `main.go` đầu tiên); `for i := 0; i < 1000; i++ {` (bảng trước khối đếm có khoá); dấu nháy ngược `fmt.Fprint(w, `{"trang_thai":"ok"}`)` (hàng mới ở bảng trước dịch vụ HTTP); `close(ch)`, `for v := range ch { tong += v }` (bảng trước khối kiểm nguyên tử/kênh); `time.Sleep(200 * time.Millisecond)`, `runtime.NumGoroutine()` (bảng trước khối rò rỉ).
- SHOULD: "(×N)" bảng quy mô bọc `nowrap()`.
- Lời đọc 2296 → 2288. `asr_reviewed` 6 → 4 (đổi câu để bù từ; cần ASR lại 2 câu khi dựng).
- Cổng: lint 0/0; render 119 khung 0 vấn đề (xem khung 40, 89); `screen_keep` 30 khối chưa khớp 0; `screen_fast.py L20`: PASS 52, FAIL/STALE/MISSING/ORPHAN 0 (Go 1.25.5 chạy thật); `verify_bnx.py L20` 33/33 PASS.
- Mục chưa giảng ước còn lại: 0.

## L21 (cho vay số)
- Mục chưa giảng → 0: `(35 if thu_nhap >= 15_000_000 else 20)`, `15_000_000`, `return a, b, c` (bảng trước `DECIDE_PY`); `hashlib.sha256(…).hexdigest()`, `import hashlib`, `a[:16]`, `len`, `replace` (bảng trước `HASH_PY`); hai hàng mới ở bảng trước dấu vân tay: `for ma, giay_to, may in ho_so:`, `[:12]`; `ofs.split(",")[4:]`, `setdefault(…)[(…)] = …`, `len({mv for mv, sv in …})` (bảng trước `OFS_PY` đầy đủ); `int(…hexdigest(), 16)`, `HE[h % 4]`, `h // 4 % 6` (bảng trước QuyMo). "(×N)" bọc `nowrap()`.
- Lời đọc 2297 → 2290. `asr_reviewed` 6 → 3 (đổi câu để bù từ; cần ASR lại khi dựng).
- Cổng: lint 0/0; render 116 khung 0 vấn đề (xem khung 32, 59); `screen_keep` 21 khối chưa khớp 0 + một Edit tay: `within` của mục `BNX L21 formula 15 0` từ `formula 14 0` sang `formula 17 0` (khối OFS đầy đủ bị đẩy xuống hai chỗ vì thêm bảng; `screen_keep` không dịch lại khoá `within`; bằng chứng: `screen_fast` FAIL "không phải dãy dòng liên tiếp" trước, PASS sau); `screen_fast.py L21`: PASS 24, FAIL 0; `verify_bnx.py L21` 32/32 PASS.
- Mục chưa giảng ước còn lại: 0.

## Tổng
Bài đổi (requeue): L19, L20, L21. Lời đọc 2292 / 2288 / 2290. Chưa dùng đến libj.JROW (dùng bộ ba tự khai, lời đọc ngắn); không sửa libj/lib/lib2. Lưu ý cho tác tử khác: `screen_keep.py` KHÔNG dịch lại khoá trong trường `within` khi step chèn thêm — nên chạy `screen_fast`/kiểm `within` sau khi chèn bảng trước khối "trích" (fragment).
