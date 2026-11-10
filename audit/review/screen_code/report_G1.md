# SC1 nhóm 1 — PLC, SWF, DMS, CAS, TOC, MLO, CVI: 60 khối

> Người điều phối ghi tệp này, nguyên văn từ câu trả lời cuối của tác tử nhóm 1 (công cụ không cho tác tử ghi tệp báo cáo).
> Các số và cổng được người điều phối chạy lại; kết quả ở `report_SC1.md`.

| Khoá | khối | run | syntax | fragment | output | pseudo | other | unverified_claims |
|---|---|---|---|---|---|---|---|---|
| PLC | 35 | 30 | 0 | 0 | 0 | 4 | 1 | 10 |
| SWF | 12 | 10 | 0 | 2 | 0 | 0 | 0 | 1 |
| DMS | 7 | 4 | 0 | 3 | 0 | 0 | 0 | 4 |
| CAS | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 2 |
| TOC | 2 | 1 | 0 | 0 | 0 | 1 | 0 | 2 |
| MLO | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| CVI | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |

## Cách kiểm
- Khối là biểu thức: `post` đọc lại đúng các dòng của khối từ tệp chạy rồi tính, không chép tay.
- Giá trị trung gian (SWF L01 quiz, L02 Euclid, L05 độ phủ): ghi vết bằng `sys.settrace` khi chạy lại nguyên văn.
- TOC L10: số bước = số lần tra bảng chuyển.
- SWF L09: đếm trạng thái bế tắc bằng duyệt mọi trạng thái, từ thứ tự thao tác thật của khối.
- Kiểm cổng có bắt lỗi không:
  - đổi kỳ vọng ở 5 mục (PLC L02 code, SWF L09, TOC L10, SWF L02, DMS L02) → cả 5 FAIL;
  - nạp lại bản cũ của PLC L12 và CVI L00 → FAIL NameError.

## Lỗi đã sửa (4 MUST, 0 SHOULD)
| Khối | Mức | Cũ | Vì sao sai + bằng chứng | Sửa thành | lint/render/verify |
|---|---|---|---|---|---|
| PLC L11 example 3 0 | MUST | `DEBUG = False / if DEBUG: ghi_nhat_ky(...) / return x / x = x + 1` | `python -I` → SyntaxError: 'return' outside function | thêm `def f(x):` và thụt lề; say "đoạn mã này" → "hàm f này"; thêm checks; sync_tpl --write | lint 0/0; render 68 khung 0 vấn đề; verify_plc 72/72 |
| PLC L12 example 0 0 | MUST | `tong  = reduce(...)` không có dòng nhập | NameError: name 'reduce' is not defined | thêm `from functools import reduce`; say "Dòng đầu nạp hàm gộp từ thư viện chuẩn, còn ba dòng sau…" | lint 0/0; render 82 khung 0 vấn đề; verify_plc 72/72 |
| PLC L12 pitfalls 3 0 | MUST | `@lru_cache` không có dòng nhập | NameError: name 'lru_cache' is not defined | thêm `from functools import lru_cache` | như dòng trên |
| CVI L00 check 1 0 | MUST | `khung = np.zeros(...)`; cả bài không nhập np | NameError: name 'np' is not defined | thêm `import numpy as np` | lint 0/0; render 102 khung 0 vấn đề; verify_cvi 112/112 |

## Đã xét nhưng không sửa
- SWF L02 prereq 1 0 (`while b != 0:` / `# thân vòng`) là khung có chỗ giữ thân vòng → fragment, không within.
- Biến bài nói ra nhưng không hiện thành mã được cấp bằng `prelude` kèm `prelude_reason`: k, h, a, s, n, ten, db. Cách này cũng áp cho các hàm mà màn hình hoặc lời đọc tả bằng chữ: term/atom/peek/eat (PLC L02), hai mô hình đồ chơi (MLO L03), lay/nha (SWF L09).

## unverified_claims (19)
- **PLC (10)**:
  - 4 khối mã giả (L02 prereq, L03 prereq, L03 example, L10 gen) kiểm bằng bản Python đối chiếu (độ trung thực INFERRED).
  - Phạm vi động (L04 hook, L04 quiz): Python không có.
  - "Kiểm tĩnh báo lỗi trước khi chạy" (L05 tradeoff, L06 prereq): không có trình kiểm tĩnh.
  - Suy luận kiểu OCaml (L06 hook): máy không có OCaml.
  - Bản sửa `acc=None` (L09): chỉ hiện nội dòng.
- **SWF (1)**: L01 hook "đúng với mọi n" là chứng minh quy nạp; máy chỉ chạy n = 1…10.
- **DMS (4)**: mã kiểu C chạy bằng node; nghĩa trong C là INFERRED vì không có trình biên dịch C.
- **CAS (2)**:
  - L03: phần "tệp ghi trường đơn vị, bên đọc từ chối tệp thiếu trường" không có mã để chạy.
  - L03: hệ số 4,448222 dẫn NIST SP 811 theo hiểu biết, chưa mở lại nguồn.
- **TOC (2)**:
  - L12 Q1 in A: kiểm bằng bản đối chiếu, độ trung thực INFERRED.
  - L12 "P2 chạy mãi": chỉ kiểm được 10 000 vòng chưa dừng.

## Dòng cuối của cổng (tác tử chạy)
- PLC: 35 khối, PASS 40 · FAIL 0 · STALE 0 · MISSING 0 · ORPHAN 0 · WARN 0
- SWF: 12 khối, PASS 12, các cột lỗi đều 0
- DMS: 7 khối, PASS 9, các cột lỗi đều 0
- CAS: 2 khối, PASS 2, các cột lỗi đều 0
- TOC: 2 khối, PASS 3, các cột lỗi đều 0
- MLO: 1 khối, PASS 1, các cột lỗi đều 0
- CVI: 1 khối, PASS 1, các cột lỗi đều 0

Bộ kiểm khác:
- verify_plc 72/72; verify_cvi 112/112
- sync_tpl PLC 0 mẫu lệch
- scan_ctrl 8 lượt, đều là JVA cố ý
- lv.py curriculum plc/cvi 0 lỗi

Bài cần dựng lại: `lessons/plc/L11_toi_uu.yaml`, `lessons/plc/L12_lap_trinh_ham.yaml`, `lessons/cvi/L00_anh_so.yaml`.

## Đề xuất cho cổng (tác tử)
1. Thêm `-X utf8` khi chạy python. **Đã làm** (người điều phối, 11:45Z).
2. Cho phép nhiều `expect_stderr_contains` trong một mục.
3. Thêm hàm sẵn để chạy lại văn bản của khối.
4. `stub`/`check` đọc mọi sổ nên lỗi khi nhóm khác đang ghi dở.
