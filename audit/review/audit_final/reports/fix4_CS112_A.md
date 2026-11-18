# fix4 CS112 phần A (L00–L14): sửa theo báo cáo người đọc R2_CS112_A.md

Ngày 2026-11-15. Phạm vi: `lessons/cs112/L00–L14`, `audit/cs112/src/*.tpl.yaml` (L05, L07, L14; L06 chỉ sinh lại), `tools/registry/symbols.CS112.yaml` (thêm mục riêng CS112), `audit/cs112/ledger_specs_a.yaml`, `audit/cs112/verify_cs112_fix4.py` (mới). KHÔNG chạy build/tts/asr/git/docker.

## Tiến độ
15/15 bài đã xử lý (đủ). Bài ĐỔI → CẦN DỰNG LẠI (build): **L00, L03, L04, L05, L07, L08, L09, L11, L12, L13, L14**. Bài đổi chỉ siêu dữ liệu (không đổi tiếng/hình): L06 (sinh lại từ mẫu: nạp `asr_reviewed` hai câu "Bảng băm thì khác." và "Chèn và lấy lớn nhất…" đã có sẵn trong mẫu), L10 (chỉ `assumes`). L01, L02: không đổi (người đọc không nêu mục sửa).

## Việc đã làm theo bài
| Bài | Sửa |
|---|---|
| L00 | hook hiện hai chương trình A (vòng for cộng dần) và B (n(n+1)/2) (SHOULD); tách step "2y − n + 1" (kèm ví dụ n = 4, y = 3) khỏi step "y ≥ ⌈n/2⌉" (giảng chuyển vế, làm tròn lên, ví dụ n = 5 → y nhỏ nhất 3); nói rõ từ đây biến vòng ngoài đổi tên i → y; nói `int m` kiểu C; cảnh `scale`: một câu lời thường cho khai báo hàm, dãy `range` bỏ số cuối, tăng biến đếm. Cắt chỗ khác giữ 2295 từ. Hook thêm `clear` ở step 2 cho khỏi tràn. |
| L03 | thêm step `class Nut` trong cảnh `linked` (lớp = khuôn, hàm tạo, tham số đầu là chính nút, con trỏ mặc định rỗng, dựng 7→3→9), `introduces: cs112_class_nut`; sửa "list Python = mảng động như vậy": nói rõ chỉ xin thêm ~1/8 sức chứa, không gấp đôi, ghi chú trên màn hình với số đo `sys.getsizeof` thật (Python 3.13: 4, 8, 16, 24, 32, 40, 52, 64, …). |
| L04 | `try/except` giảng bằng lời ("khối thử bắt lỗi"); hàm C `int fact(int n) {` giảng (kiểu số nguyên ghi trước tên, ngoặc nhọn); lab: nói `HangDoiVong` là một lớp, khung cho sẵn ở `de.md`; hàng "deque" giới thiệu (`introduces: cs112_deque`). |
| L05 | (mẫu) `avl`: thêm step thử số N(h) = 1, 2, 4, 7, 12, 20, … N(10) = 232; N(h) ≥ 2N(h−2) ⇒ n ≥ 2^(h/2) ⇒ h ≤ 2 log2 n; AVL dưới 232 nút cao tối đa 9. `assumes` thêm `cdot`. |
| L06 | sinh lại từ mẫu; hai câu ASR đã ghi `asr_reviewed` (cơ chế hiện có) — không đổi lời đọc. |
| L07 | (mẫu) cảnh `scale`: giảng một câu cho `deque` (nhắc bài 4), `popleft`, biến `d`/`hang`, vòng nhìn bốn ô, và `print(c * c, *bfs(c))` (dấu sao rải ba kết quả). `assumes` thêm `cs112_deque`. |
| L08 | giảng "công thức đóng" lần đầu ở `backsub` bước cuối (khung + lời, ví dụ T(10) = 1023), `introduces: cs112_cong_thuc_dong`; giảng `dem[0]` (danh sách một ô làm bộ đếm chung), `introduces: cs112_dem0`. |
| L09 | nhắc lại "công thức đóng" ở `partial` + `assumes`; `scale`: n = 53 đúng, **n = 54 là chỗ sai đầu tiên** (lời, mã chạy `(10, 53, 54, 60)`, bảng thêm hàng 54, mục tiêu "sai từ n = 54"); giảng "chữ số nhị phân/bit" (5 = 101; 2^53−1 đủ 53 chữ số 1, 2^54−1 cần 54), giải thích `int(2.0 ** n − 1)`. `introduces: cs112_bit`. |
| L10 | `assumes` thêm `cs112_dem0`. |
| L11 | `scale`: thêm cột "số tầng khi lấy căn = log2 log2 n" (4, 5, 6, 10) để lời hiện trên màn hình; một câu giảng lệnh lấy căn nguyên (isqrt) ; `assumes` thêm `cs112_cong_thuc_dong`. |
| L12 | tách khung định lý thợ: khung 1 trường hợp 1–2 + định nghĩa ε; khung 2 trường hợp 3 + điều kiện đều đặn (giải bằng lời + ví dụ f = n², a = b = 2 ⇒ c = 1/2); `scale`: giảng cắt lát, `pop(0)`, "nếu … ngược lại" một dòng. `assumes` thêm `cs112_dem0`. Cắt chỗ khác giữ 2291 từ. |
| L13 | `scale` hàng "1 000 000 (công thức)" đủ 5 ô ("chưa chạy" ở hai cột đo, 499 999 500 000 và 999 999 ở hai cột công thức); lời nói rõ hàng này không chạy máy. |
| L14 | (mẫu) giả mã kiểu C giảng (dấu `!` là phủ định, ngoặc nhọn, vị trí đếm từ 1); `practice`: thống nhất "x[i] ≠ i + 1, vị trí đếm từ 0, bỏ j = i + 1" như `de.md`; nhắc hàm đệ quy viết trong hàm chính và mẹo kiểm bằng một dòng; `assumes` thêm `cs112_dem0`. |

Sổ thuật ngữ CS112 (chỉ thêm mục riêng, không sửa sổ chung): `cs112_class_nut`, `cs112_cong_thuc_dong`, `cs112_dem0`, `cs112_bit`, `cs112_deque` (`term:`). Mỗi mục chỉ khớp ở bài L00–L14 (đã kiểm: lint 0 FAIL ở cả 30 bài CS112, kể cả L15–L29).

P1 dự kiến: L08, L09 lên 2 ⇒ 15/15 = 100% (người đọc nêu: "công thức đóng", "chữ số nhị phân" là nguyên nhân duy nhất làm hụt).

## Số liệu cổng thật
| Cổng | Kết quả |
|---|---|
| lint L00–L29 CS112 | 0 FAIL, 0 WARN ở cả 30 bài |
| lời đọc (từ) | L00 2295, L03 2000, L04 ~1740, L05 2218, L06 2111, L07 1959, L08 ~1760, L09 1684, L10 2074, L11 ~1700, L12 2291, L13 ~1810, L14 1732 (đều ≤ 2300) |
| render (khung 1920×1080) | L00, L03, L04, L05, L07, L08, L09, L11, L12, L13, L14: 0 vấn đề; đã xem khung L00 hook, L07 scale, L09 scale ×2, L12 master |
| `audit/cs112/verify_cs112_fix4.py` (mới, mã thật) | 30 PASS · 0 FAIL |
| `audit/cs112/verify_cs112_a.py` (chạy thật mã `scale` + 15 lab) | 30 PASS · 0 FAIL |
| `lv.py curriculum curriculum/cs112.yaml` | 30 bài, 0 lỗi |
| `tests/test_e52.py` | 0 FAIL |
| `check_curricula_graph.py` | tham chiếu hỏng 0, chu trình 0 |
| `screen_code.py check --course CS112` | 97 khối — PASS 144 · FAIL 0 · STALE 0 · MISSING 0 · ORPHAN 0 (trước khi cập nhật sổ: STALE 2 = L09 scale, MISSING 3 = L00 hook ×2, L03 linked; đã thêm spec vào `audit/cs112/ledger_specs_a.yaml` và chạy `ledger_a.py`) |
| `audit/review/lab_gate.py CS112` | 30 PASS · 0 FAIL (195 lab được bài tham chiếu) |
| `audit/review/arith_scan.py` | 245 phép tính, 0 FAIL |

## Không sửa / lưu ý
- L01 ("bậc", "hữu hạn"), L03 ("rò rỉ bộ nhớ"), L13 ("tìm tuần tự"), `enumerate` (L14), `dict.get`/`max(o.values())` (L06): người đọc ghi là mục biên không trừ điểm; không đổi để khỏi tăng lời đọc.
- Lab phần "đề ghi sẵn công thức đóng" (SHOULD nhẹ của vòng 1): ngoài danh sách nhiệm vụ lần này, không đổi.
- Âm thanh chưa nghe bằng tai người (không chạy tts/asr).
- Sửa SHOULD L03 getsizeof: số đo ở Python 3.13.5 của kho; bản khác có thể khác (bài ghi "hệ số tăng tuỳ phiên bản").
