# fix_R_BNX_L00_11 — sửa BNX L00–L11 theo báo cáo người đọc độc lập (2026-11-14)

Chi tiết từng nhóm: `fix_R_BNX_L00_11_F1.md` (L06, L37), `_F2.md` (L07, L38), `_F3.md` (L08–L11). Tệp này ghi phần điều phối (L00, L01, L04, L05, L36, L00 bản đồ, pack.py) và số cổng cuối.

## Bài đã đổi
| Bài | Việc | Từ (trước → sau) |
|---|---|---|
| L00 | P1: bảng giảng tại chỗ `export`, `` `mktemp -d` ``, `git switch -c`, `git commit -am`, `cat-file -p`, `rev-parse HEAD:…`, `log --graph --oneline` (2 step ở cảnh sym) và `for/seq`, `\|\|`, `$(( ))`, `>/dev/null` (step đầu cảnh quymo); cột "mỗi người sửa tệp riêng: 0/0/0" ở bảng quy mô + `checklib bnx_l00_conflicts_split` + `ver` chạy git thật N=2,10,50; bản đồ khoá thêm bài 37–38 | 2301 → 2375 (≈ 15 phút) |
| L01 | 2015 trao cho tổ chức chuẩn mở (31/12/2015, `sources.md`), sau đó đổi tên | không đổi đáng kể |
| L04 | quiz câu 2 thành "chọn luồng" (ứng dụng điện thoại → mã ủy quyền + PKCE; dịch vụ ban đêm → thông tin máy khách), phủ mục tiêu 2 | 2306 → 2348 |
| L05 | nêu OpenSSL ≥ 3.4 (cờ `-not_before`), trên màn hình và lời đọc | 2346 → 2360 |
| L06 | F1: cắt còn Oracle | 3054 → 2254 |
| L07 | F2: còn phân vùng + JSON | 3049 → 2299 |
| L08–L11 | F3 | 2284 / 2293 / 2300 / 2296 |
| L36 | thêm `forward_ref` "bài sau" (quay lại cơ sở dữ liệu: L37) | 2293 → ~2320 |
| L37 (mới) | F1: T-SQL, XACT_ABORT, chống chèn mã, JDBC, kết nối an toàn | 2276 |
| L38 (mới) | F2: hàng đợi AQ, bộ nhớ cột, phân mảnh | 2290 |

Việc chung: `curriculum/bnx.yaml` có L37, L38 ở cuối; `audit/verify_plan_curricula.py` có dòng VER; `pack.py` JD_MAP: "Stored Procedure Oracle và MS SQL" + L37; "Oracle: SQL, chỉ mục, …" + L06, L07; "Tính năng Oracle mới" + L38; "MongoDB, MySQL, PostgreSQL bên cạnh Oracle và SQL Server" + L37. L06 recap sửa "bài cuối khoá" → "bài ba mươi bảy" (R4); L37 hẹn "bài sau" (L38).

## Cổng (số thật)
- lint 0 FAIL 0 WARN và render 0 vấn đề: L00, L01, L04, L05, L06, L07, L08, L09, L10, L11, L36, L37, L38.
- `verify_bnx`: L00 L01 L04 L05 L36 = 106/106 PASS; các nhóm khác theo báo cáo F1/F2/F3 (không SKIP, trừ nguồn JDBC L37 thoát 97 khi thiếu ojdbc).
- `screen_fast`: 0 FAIL/STALE/MISSING/ORPHAN cho mọi bài đã đổi.
- `check_course_refs.py BNX`: 0 vấn đề. `check_curricula_graph`: 0 tham chiếu hỏng, 0 chu trình, VER 0 lỗi. `tests/test_e52.py`: 0 FAIL. `check_next_refs`: 551 lời hẹn, 0 lệch.
- `lab_gate.py BNX`: 39 PASS 0 FAIL (F1/F2/F3).
- `lv.py curriculum curriculum/bnx.yaml`: 39 bài, **1 lỗi ngoài phạm vi**: `L17 assumes ['bnx_base64url']` — L17 chỉ đi theo chuỗi L16→…→L08→L01→L00, không qua L03 (nơi `bnx_base64url` được giới thiệu). L17 do nhóm L12–L23 sửa; cần thêm `requires: L03` hoặc `assumes_external`/bỏ `assumes` ở L17.

## Mục không làm / lưu ý
- L00 (2375), L04 (2348), L05 (2360) vẫn trên 2 300 từ nhưng < 16 phút (L05 đo 14:49 ở 2346 từ); đã giữ lượng thêm ở mức tối thiểu cho P1.
- RabbitMQ L10 (queue/binding/ack): F3 không làm vì L10 đã đúng 2 300 từ.
- Sổ screen chung `audit/review/screen_code/BNX.yaml` chưa gộp: người điều phối chạy `python -B audit/bnx/screen_try.py --merge`. `lib2.py gen-screen L06/L37` sẽ xoá phần Oracle/SQL Server gộp tay (xem F1).
- ojdbc jar L37 chép từ phiên trước (sha1 khớp Maven Central đã ghi); Docker hostname `461d1255632f` nằm trong `expect_stdout` các khối SQL Server L37.
- Video: L04, L06–L11, L36–L38 cần dựng lại (lời đọc thay đổi); chưa dò ASR câu `say` mới.
