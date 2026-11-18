# WP4 — nhánh B: BNX L20–L23 lên chuẩn AF2 (2026-11-14)

## Tiến độ
- L21 (cho vay số): XONG phần bài — gen + lint 0/0 + render 0 + verify 32/32 PASS + screen_fast PASS.
- L22 (AEM, mô phỏng): XONG phần bài — gen + lint 0/0 + render 0 + verify 33/33 PASS + screen_fast PASS.
- L23 (scikit-learn/ONNX): XONG phần bài — gen + lint 0/0 + render 0 + verify 47/47 PASS + screen_fast PASS.
- L20 (Go): XONG — gen + lint 0/0 + render 0 + verify 33/33 PASS + screen_fast PASS (30 khối, 52 mục) + labs/cham.sh ĐÚNG.

## Số từ lời đọc (đếm theo khoảng trắng của `say` trong YAML sinh ra)
| bài | trước | sau |
|---|---|---|
| L20 | 3 590 | ~2 253 |
| L21 | 2 952 | ~2 130 |
| L22 | 3 352 | ~2 276 |
| L23 | 3 989 | ~2 273 |

Các bài đều thêm cảnh `quymo` + `practice` và `af2: true` + `covers`; phần nội dung cũ bị cắt (gộp step, bỏ bảng hỏi ở hook, bỏ ví dụ thừa) nhưng không bỏ mục tiêu nào.

## Thay đổi theo bài
Chung: `from lib import *` → `lib2` (+ `spoken_b._spoken` ghép câu < 8 từ: tệp mới `audit/bnx/src/spoken_b.py`, sao từ l16 để không phụ thuộc bài của nhánh A); hai mục tiêu mới thêm vào `curriculum/bnx.yaml` (quy mô + lab) và vào bài; thêm mục `term:`/`introduces` (E52) vào `tools/registry/symbols.BNX.yaml` dưới các tiêu đề `# ── L20/L21/L22/L23 (nhánh B …) ──`.

- **L21**: cảnh `quymo` đo thật luật dấu vân tay thiết bị “từ 3 giấy tờ khác nhau trên một mã thì gắn cờ” ở 5, 500, 50 000 hồ sơ (24 kiểu máy): 0 / 500 / 50 000 hồ sơ bị gắn cờ → cần 0 / 13 / 1 250 người xét (40 hồ sơ mỗi người, số minh hoạ) — luật chỉ có nghĩa khi quần thể nhỏ. Lab `labs/BNX/L21` (Python: DTI, điểm, quyết định, băm SHA-256, đếm vị trí khác; số liệu khác ví dụ). Checklib: `bnx_l21_scale`, `bnx_l21_fp_of`, `bnx_l21_reviewers`. `introduces` bnx_ma_bam (mã băm: sổ L26 đã có `term`), bnx_thap_luc_phan (đã có từ L00).
- **L22** (vẫn là MÔ PHỎNG, ghi rõ trên màn hình và trong lời đọc): `quymo` đo thật tìm theo thuộc tính không chỉ mục / có chỉ mục ở 10, 1 000, 100 000 trang: duyệt 14 / 1 004 / 100 004 nút, khớp 1 / 10 / 1 000; tra một đường dẫn luôn 4 bước. Lab `labs/BNX/L22` (kho nhỏ + chọn tệp dựng). Checklib `bnx_l22_scale`. Bảng sym tách hai step (tràn khung).
- **L23**: `quymo` huấn luyện lại IsolationForest (sklearn 1.9.1 trong `audit/bnx/deps/l23/venv`) ở 1 010, 10 100, 101 000 điểm: nhãn −1 = 11 / 101 / 1 005 (quy tắc đếm cho 1 010; lệch ≤ 5 vì điểm trùng điểm), bắt đủ điểm lạ, tổng số nút của rừng ≈ 11 400 không đổi bậc, người xét cần 1 / 3 / 26. Lab `labs/BNX/L23` (Python thuần: c(n), điểm, nhãn, số điểm bị gắn). Checklib `bnx_l23_reviewers`. Câu “Bài sau (Bài 24): JPA/Hibernate và Spring Data” thay nội dung cuối (R4: L23 không còn là bài cuối; bài cũ không có chữ “bài cuối” nhưng chưa có cảnh forward_ref tới L24).
- **L20** (Go): viết lại toàn bộ mã Go thành các chương trình gọn ≤ 24 dòng, hiện đủ `package`/`import`, chia ≤ 2 khung ≤ 12 dòng, đầu ra ASCII; mọi chương trình là `prog(kind=other)` + chương trình bash `go run` đi kèm (sổ sinh bằng `lib2.py gen-screen L20`, không còn mục viết tay). `main.go` của Fiber ở `audit/bnx/deps/l20/fiber/` được viết lại lúc import `l20.py` (README: sha mới). `quymo` đo thật ngăn xếp của 1 000, 10 000, 100 000 luồng nhẹ cùng chờ: 7 / 70 / 703 MiB (≈ 7–8 nghìn byte mỗi luồng, Go 1.25.5 Windows — ghi rõ số đo theo máy). Lab `labs/BNX/L20/loi_giai.sh` (tạo `main.go` bằng heredoc rồi `go run`; cần Go: `cham.sh` không có đuôi `.go`). Checklib `bnx_l20_mb`.

## Công cụ sửa
`audit/bnx/screen_keep.py` (của người điều phối): thêm remap `prelude_keys` (ngoài `of`) khi khoá khối đổi vị trí.

## Cổng cuối (chạy 2026-11-14)
| cổng | kết quả |
|---|---|
| lint L20 / L21 / L22 / L23 | 0 FAIL 0 WARN (53 / 59 / 62 / 45 PASS) |
| render | 0 vấn đề cả bốn bài (xem khung quymo, practice và một khung ví dụ/pitfall mỗi bài) |
| verify_bnx | L20 33/33, L21 32/32, L22 33/33, L23 47/47 PASS (không SKIP) |
| screen_fast | L20 PASS 52 · L21 PASS 24 · L22 PASS 28 · L23 PASS 37 (FAIL/STALE/MISSING/ORPHAN đều 0) |
| lab_gate BNX | 37 PASS · 0 FAIL (gồm lab L20–L23) |
| `lv.py curriculum curriculum/bnx.yaml` | 37 bài, 0 lỗi |
| `check_curricula_graph.py` | tham chiếu hỏng 0, chu trình 0 |
| `tests/test_e52.py` | 0 FAIL |
| `check_next_refs.py` | 0 lệch dãy học |
| `check_course_refs.py` | chỉ báo R4 ở BNX L00 recap.3 (“bài cuối là phỏng vấn thiết kế hệ thống”, bài của nửa L00–L11, ngoài phạm vi); không có lỗi ở L20–L23 |
| `check_xref.py` | BNX 14 lượt ở 2 tệp (không thuộc L20–L23) |

## P1 dự kiến
Mỗi bài giảng tại chỗ các thuật ngữ mới (E52 `introduces`: L20 luồng nhẹ/nhóm chờ/khoá/tranh chấp/Fiber/nguyên tử; L21 LOS/LMS/DTI/thẻ điểm/OTP/ECM/OFS/mã băm/thập lục phân; L22 AEM/JCR/Sling/HTL/OSGi; L23 độ lệch chuẩn/phân phối chuẩn/tỉ lệ nhiễm/ONNX) → dự kiến P1 = 2 ở cả 4 bài; rủi ro còn lại: cú pháp Go/Python lạ (`select … default`, `setdefault`) chỉ giảng một câu.

## Điều không làm / lưu ý
- L22 vẫn là mô phỏng (không có máy chủ AEM) — ghi rõ trên màn hình và lời đọc; HTL/Java/MANIFEST chỉ đọc đối chiếu.
- Số đo bộ nhớ L20 phụ thuộc phiên bản Go/hệ điều hành: đầu ra làm tròn xuống nghìn byte (8, 7, 7) để tất định; bản trước in MiB bị lệch 1 đơn vị khi máy tải nặng nên đã bỏ.
- `Roiri` (L20) dùng `time.Sleep(200ms)`: máy quá tải có thể làm số luồng còn sống lệch (chưa gặp).
- Bộ đếm không khoá L20: hook nói “có lần thấp hơn 1000, không lần nào chắc chắn đúng” (đo 200 lần: 95/200 thấp hơn; trên máy khác tỉ lệ khác).
- Dòng Go dài tới ≤ 90 ký tự (ver nới từ 70 lên 90; khung 1920 px không tràn).
- Đề xuất tách bài: không cần; cả bốn bài ≤ 2 300 từ.
- Mã Go dùng dấu chấm phẩy trên một dòng (`import ("fmt"; "sync")`) cho vừa khung: hợp lệ nhưng không phải gofmt.
