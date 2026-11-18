# WP4 nhánh A — BNX L00–L03 lên chuẩn AF2 (2026-11-14)

Tiến độ: L00, L01, L02, L03 đã xong nguồn + lab + sổ screen_code + cổng riêng từng bài (lint 0/0, render 0 vấn đề, verify PASS, screen_fast PASS). Chưa chạy build/tts/asr/git (theo brief).

## Bài đã đổi (nguồn `audit/bnx/src/lNN.py` → `gen.py`)
| Bài | Lời đọc (từ) | Cảnh mới | Lab (`labs/BNX/Lxx`) | Số đo thật (cảnh quy mô, id `quymo`, loại `example`) |
|---|---|---|---|---|
| L00 Git | 2 299 | `quymo`, `practice`, bản đồ khoá (2 bảng ở `recap`, forward_ref) | `loi_giai.sh`: hai nhánh sửa cùng dòng lãi suất, 5 commit, 2 cha | N nhánh cùng sửa một dòng, gộp lần lượt vào main bằng git thật: N = 2 → 1, 10 → 9, 50 → 49 xung đột (= N − 1); biến thể mỗi người một tệp → 0 xung đột |
| L01 OpenAPI | 2 299 | `quymo`, `practice` | `loi_giai.py`: kiểm yêu cầu rút tiền ATM theo lược đồ (5 yêu cầu thử) | lô yêu cầu có tỉ lệ sai cố định: 1 000 → 30 bị chặn, 100 000 → 3 000 (hàm `kiem` của bài, chạy nguyên văn); 5/50/500 đối tác cũ vs hợp đồng đòi `purpose` → 5/50/500 yêu cầu 400 |
| L02 Protobuf | 2 297 | `quymo`, `practice` | `loi_giai.py`: mã hoá tay 3 trường (08 14 30 f0 a2 04 3a 05 41 54 4d 30 31, 13 byte) | tổng byte n bản tin: 1 000 → 21 857 (nhị phân) vs 62 786 (JSON); 100 000 → 2 381 377 vs 6 677 790; đối chiếu bằng `google.protobuf` thật |
| L03 JWT | 2 293 | `quymo`, `practice` | `loi_giai.py`: ký và kiểm JWT HS256, khoá khoa-lab-l03 (5 dòng đầu ra) | hạn 300 s vs 3 600 s, mã lộ ở giây 60: kẻ gian dùng được 240 vs 3 540 lần (gọi `kiem` mỗi giây); mã mới mỗi giờ 12 000 vs 1 000 (1 000 người), 12 000 000 vs 1 000 000 (1 triệu, số minh hoạ) |

Mọi bài: `af2: true` + `covers` (6 mục tiêu, E51), thêm hai mục tiêu (quy mô, tự làm) vào bài và `curriculum/bnx.yaml`; mục tiêu cũ "Giải thích …" đổi thành "Nêu …" (E51 coi "giải" là động từ LÀM) ở L00, L01, L02.

## Cổng thật đã chạy
- `verify_bnx.py`: L00 19/19, L01 20/20, L02 20/20, L03 21/21 PASS (không SKIP).
- `lv.py lint`: 0 FAIL, 0 WARN cả bốn bài; `lv.py render`: 0 vấn đề (112/110/103/103 khung); đã xem khung PNG: L00 quymo/practice/bản đồ, L01 quymo ×2 + practice, L02 quymo + sym, L03 quymo ×2 + practice.
- `screen_fast.py L00 L01 L02 L03`: 57 khối, PASS 61 (gồm nguồn lab), FAIL/STALE/MISSING/ORPHAN 0.
- `lv.py curriculum curriculum/bnx.yaml`: 37 bài, 0 lỗi. `tests/test_e52.py`: 0 FAIL. `check_course_refs.py bnx`: 0 vấn đề (bản đồ L00 phủ đủ Bài 1–36; câu "bài cuối" đổi thành "bài ba mươi sáu" vì R4).
- `check_curricula_graph.py`: không chu trình, tham chiếu hỏng 0; một dòng FAIL của WEB:L04 (VER), ngoài phạm vi.
- `lab_gate.py BNX`: xem dòng cuối mục "Lab gate" bên dưới.

## Thuật ngữ (E52) và canon (E55)
Id mới trong `tools/registry/symbols.BNX.yaml` (mục `term:`):
- `bnx_thap_luc_phan` (thập lục phân) — giảng ở L00 prereq; L02 `assumes`.
- `bnx_vung_cho` (vùng chờ) — L00 sym. `bnx_gop_ba_chieu` (gộp ba chiều) — L00 formula.
- `bnx_base64url` (base64…) và `bnx_hmac` (HMAC) — giảng ở L03 prereq. **Nhánh B (L04, L05): nếu dùng "base64"/"HMAC" phải `assumes: [bnx_base64url, bnx_hmac]`.**
- `bnx_ma_bam` (đã có, của L26): L00 giảng ("hàm băm, mã băm") `introduces`; L03 `assumes: [bnx_ma_bam]` (dùng "SHA256"). Bài sau L00 dùng "mã băm"/"sha256" thì `assumes`.
Không đăng ký "commit", "xung đột", "HEAD", "bản sao kho", "khoá lũy đẳng", "lược đồ", "OpenAPI", "JWT" (đã có bài L24+ af2 dùng nghĩa khác hoặc bài khác chưa giảng); lint E52 không báo gì ở L00–L03 (E55 sạch).
Sửa P1 tại chỗ: L01 giảng "API", "máy khách" (prereq ①), thay "Jackson" trong lời đọc; L00 hook bỏ "mã băm" trước khi giảng; L01 recap bỏ "ngoại lệ" (đụng `bnx_ngoai_le`).

## Cách làm và quyết định
- Không đổi khối mã cũ: sổ cũ (`audit/bnx/screen/l0N.yaml`, kiểu viết tay) giữ nguyên, nối thêm mục cho khối mới (`quymo` mã + đầu ra, `practice` đầu ra mong đợi, nguồn `LAB_Lxx`) bằng kiểu `run` + `prelude_keys` (dùng lại hàm của cảnh trước, như L03 cũ).
- Bộ kiểm (`audit/bnx/ver/lNN.py`) thêm: chạy lại nguyên văn khối đo; đếm bằng đường khác (L00: biến thể tệp riêng; L01: vòng đếm + công thức sàn; L02: `google.protobuf` thật; L03: mô phỏng từng giây bằng HMAC tự dựng RFC 2104); chạy lời giải lab so với mong_doi và với công cụ độc lập. `tools/checklib_bnx/l0N.py` thêm `bnx_l00_conflicts/minutes`, `bnx_l01_blocked`, `bnx_l02_sizes`, `bnx_l03_exposed/refresh_per_hour`.
- Lời đọc dùng `_merge_short` (từ `l03.py`) ghép câu < 8 từ.
- Lab Git (L00) chạy bash + git thật qua `cham.sh`; yêu cầu Git Bash, danh tính người viết đặt bằng biến môi trường (4 dòng đầu cho sẵn).

## Không làm / hạn chế
- Không nghe ASR/tai người (không chạy `asr`); từ "HMAC", "SHA256", "API", "Python" trong lời đọc dựa trên luật đọc cũ của lexicon BNX (cảnh L03 cũ đã dùng).
- Cổng `screen_code check --course BNX` toàn khoá không chạy (Oracle/SQL Server/Kafka của bài khác); chỉ `screen_fast` cho L00–L03.
- Lời đọc mỗi bài sát trần 2 300 từ (≈ 15–16 phút). Đề xuất nếu cần thêm nội dung sau này: tách bản đồ khoá khỏi L00 thành bài mở đầu riêng (không đánh số lại bây giờ); L02 có thể tách "hạn chót" thành bài riêng.
- Sự cố nhỏ: một tệp `p_l00.py` trong thư mục scratchpad dùng chung đã bị xoá nhầm (tệp cặp thay thế cũ không phải của tôi); không ảnh hưởng kho.

## Lab gate
`audit/review/lab_gate.py BNX`: 37 PASS · 0 FAIL (gồm lab L00–L03 của nhánh này và L24–L36).
