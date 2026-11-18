# fix6 BNX_A nhánh A1 (L00–L03) — 2026-11-16

## TIẾN ĐỘ
- [x] L00 xong  - [x] L01 xong  - [x] L02 xong  - [x] L03 xong (cổng từng bài + test_e52 đã chạy)

Nguồn sửa: `audit/bnx/src/l00..l03.py` (sinh bằng `gen.py`), `audit/bnx/ver/l00.py` (thêm kiểm). `tools/registry/symbols.BNX.yaml` KHÔNG sửa (không thêm `term:`: "blob", "mã làm mới" … dùng nghĩa riêng của bài, giảng tại chỗ bằng `introduces` không cần; không có ký hiệu sổ nào bị dùng sớm). Không động tới sổ chung `audit/review/screen_code/BNX.yaml` (chỉ `audit/bnx/screen/l00..l03.yaml` sinh lại bằng `screen_keep.py`). Không docker/build/tts/asr/git.

## Bảng từng bài
| Bài | Mục R4 → xử lý | Từ lời đọc (trước → sau) | lint | render | verify_bnx | screen_keep/fast | mục chưa giảng ước còn lại | asr_reviewed |
|---|---|---|---|---|---|---|---|---|
| L00 | `blob a9b66cb`/`f"blob {…}"`: nhãn `tree`/`blob` trên hình + câu say "khối nội dung" + hàng bảng check ("chữ đầu chuỗi là loại đối tượng"). `git diff --cached --check`: giải nghĩa `git diff --cached` + `--check` (hộp ghi chú + say). `%h`, `git switch -c thu 18bdd9f`, `.env`: bảng 4 hàng mới đứng TRƯỚC khối mã lỗi 2 (+ hộp giải `.env`), khối mã tách step riêng. `git switch -q -c n$i main`, `;`: bảng quymo tách hai step (4+4 hàng) có hàng `lệnh_a ; lệnh_b` và `git switch -q -c n$i main`. | 2297 → 2286 | 0/0 (36 PASS) | 0 vấn đề (113 khung) | 20/20 (thêm 1 kiểm) | 14 khối: PASS 15, FAIL/STALE/MISSING/ORPHAN 0 | 0 | 5 → 4 |
| L01 | `application/json`: ghi chú "kiểu nội dung" ở step Bước 2 + say. "bản nháp IETF": ghi chú trên màn hình (IETF soạn chuẩn Internet, bản nháp = chưa chính thức) + say; GIỮ nhãn "bản 08". `for f in (…):`, `if v is not None and not (…)`, `CAN = (…)` (tuple), `#`, `return loi + …`: thêm bảng 4 hàng đứng trước khối mã `kiem` (cắt bảng cũ thành 2 bảng). `A, B = "…", "…"`: hàng mới ở bảng check.3. `req["amount"] = 0`: gộp vào hàng `del req[...]` của bảng quymo. | 2294 → 2295 | 0/0 (42) | 0 vấn đề (118) | 20/20 | 13 khối: PASS 14, 0 lỗi | 0 | 8 → 8 |
| L02 | `json.dumps({"id": 150}…)` + từ điển: hàng `{"id": 150}` ở bảng đứng trước. `out = {}`, `out[num], i = …`, `i, out = 0, {}`: bảng 3 hàng mới đứng trước khối `decode`. `n = shift = 0`, `return n, i`: hàng mới ở bảng check.5. `#`: thêm vào hàng `def varint` (check.1). `//` .proto: hộp ghi chú dưới khối mã lỗi 2 + say. "MB": ghi chú trên màn hình (MB = mê-ga-byte, một triệu byte; lời đọc đã nói "triệu byte"). | 2298 → 2296 | 0/0 (46) | 0 vấn đề (119) | 20/20 | 17 khối: PASS 18, 0 lỗi | 0 | 29 → 23 |
| L03 | "mã làm mới" (A chắc): định nghĩa tại chỗ ở Bước 5 (hộp ghi chú "mã làm mới (refresh token): mã thứ hai chỉ dùng để xin mã mới khi mã đang dùng hết hạn; nơi cấp mã thu hồi được" + say) — trước formula Bước 6/quiz/recap. `json.loads(unb64u(t))`, `from datetime import datetime, timezone`, `ma.split(".")[1]`, `datetime.fromtimestamp`, `time.time()`: bảng 4 hàng mới đứng trước khối "Đọc phần thân" (có `time.time()` cho khối "Năm ca thử" sau đó). `openssl base64 -A`, `date '+%F %T'`: sửa hai hàng của bảng lệnh check.1. `typ`: thêm vào hàng "phần đầu" của bảng sym. | 2292 → 2298 | 0/0 (59) | 0 vấn đề (110) | 21/21 | 13 khối: PASS 14, 0 lỗi | 0 | 11 → 8 |

(asr_reviewed giảm vì câu đổi chữ, không phải lỗi; gen.py giữ nguyên các câu không đổi.)

Khung PNG đã xem: L00 00033 (hình blob/tree), 00069 (bảng quymo), 00085 (bảng lỗi 2); L01 00061 (bảng mới), 00065 (khối mã); L02 00059, 00069; L03 00031 (mã làm mới), 00049 (bảng datetime). Tất cả gọn, không tràn.

## SHOULD
- L00 quiz câu 2: đề thêm "nhánh X rẽ từ commit gốc … main cũng đã có commit mà X chưa có"; đáp án giữ 7 commit/2 cha, thêm ghi chú trên màn hình + lời đọc "nếu main không có commit mới thì tua nhanh: 6 commit, không commit gộp". Tự kiểm git thật: `ver/l00.py` gộp X vào main khi `main` không là tổ tiên của X → 7 commit, 2 cha; và ca tua nhanh (X rẽ từ ngọn main) → 6 commit, 1 cha. Chạy PASS.
- L00 example.7 (`*   0eac7e6` / `|\` mất khoảng trắng đầu dòng): không sửa (chỉ lệch định dạng, nằm ngoài mục 2 của việc giao).
- Các SHOULD khác của R4 thuộc A2/A3 (L04, L06, L11).

## Mục không làm / lưu ý
- Mục "B" và "yếu" khác của L00–L03 trong R4 mục 3 đều đã xử lý ở bảng trên; không bỏ mục nào.
- Lab `de.md` L00 dùng `$(…)`, `git rev-list --count`, `grep -c` không giải thích: reader ghi là ngoài đường chính, không sửa.
- Phụ thuộc Docker/DB: không có ở L00–L03; tất cả cổng chạy thật.
- `screen_try.py --merge` KHÔNG chạy (tác tử chính gộp một lần). `shacheck.py` khớp sha 14/13/17/13 khối.
- Công cụ dùng chung scratchpad: nhánh khác ghi đè `fidx.py`/`rep.py` cùng tên trong scratchpad; nhánh A1 dùng `a1_*`/`rep2.py`.

## Bài đổi → requeue
L00, L01, L02, L03 (lời đọc và bảng đổi ở cả 4).
