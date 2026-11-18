# fix3_S01_PYT: sửa khoá PYT vòng 3 theo `R_S01c_PYT.md` (một tác tử, cả khoá)

Nguồn sửa: `audit/pyt/src/lNN.py` → `gen.py` (không sửa YAML sinh ra bằng tay). Không chạy build/tts/asr/git/docker. Nền: MUST 0, P1 = 2 ở 13/14 (92,9%), P8 100%. Mục tiêu vòng này: nâng biên P1 (nay dự kiến 14/14) và sửa mọi SHOULD.

## 1. Bài đã đổi (cần dựng lại: mỗi bài đổi `spec_sha256` nên STALE)
L00, L03, L04, L05, L06, L07, L08, L10, L12, L13 (10 bài). Không đổi: L01, L02, L09, L11.

## 2. P1: lệnh/ký hiệu phụ nay được giảng tại chỗ
| Bài | Mục | Cách giảng |
|---|---|---|
| L08 | `grep`, `wc -l`, `find \| sort`, `mv`, `2>&1`, `python -m` | Bước `sym.1` mới (bảng "lệnh cửa sổ lệnh mà bài này dùng", 7 hàng + lời đọc): `ls`, `grep`, `wc -l`, `mv`, `lệnh1 \| lệnh2` (kèm `tail -n 1`, `cut -c1-58`), `2>&1`, `python -m tên`. Đơn giản hoá lệnh để giảm số thứ phải giảng: `find ngan_hang -name "*.py" \| sort` thành `ls ngan_hang`; `grep -E "^(numpy\|pandas)=="` thành `grep pandas requirements.txt`; `wc -l < tệp` thành `wc -l requirements.txt` (cả ba chạy thật trong Git Bash qua `verify_pyt`, đầu ra mới: `__init__.py  phi.py`, `pandas==3.1.1`, `17 requirements.txt`). `pyt_cut` chuyển sang step này; ghi chú `cut`/`tail` ở ví dụ trùng tên rút gọn |
| L00 | `echo $?`, Git Bash | prereq.0: thêm đoạn "Git Bash là cửa sổ lệnh của khoá: tải Git for Windows ở git-scm.com, cài, mở Git Bash; dấu `$` là dấu nhắc không gõ; `echo` in chữ ra màn hình; `$?` là mã thoát của lệnh vừa chạy"; lời đọc nói thành lời (không đọc tên Git/Bash vì lexicon FND ghi 3/8 nghe đúng) |
| L05 | `tail`, "luồng in" | pitfalls.2: "luồng in = chỗ chương trình in chữ ra màn hình (stdout)" ở lần đầu xuất hiện; pitfalls.3: `tail -n 1 loi.txt` (giữ dòng cuối của tệp, nơi có tên lỗi) và `\|` (chuyển kết quả sang lệnh sau), có trong chữ và lời đọc |
| L12 | `python -m` | sym.0: hàng lệnh giải `-m pytest` ("chạy mô-đun theo tên, như `python -m venv` ở bài 8"), lời đọc "ba cờ nhỏ, cờ chữ m chạy một mô-đun theo tên" |
| L08 de.md | `python -m venv`, `pip install` | thêm: tạo thư mục mới `.venv-hoc` trong thư mục đang đứng (xoá là xoá môi trường); `pip install` tải từ mạng (PyPI), mất vài phút, không mạng thì báo lỗi; giải thích `-m` |

## 3. SHOULD (8 mục báo cáo) đã sửa
| Mục | Cách sửa |
|---|---|
| L12 số dòng vết lỗi lệch tệp gõ (`:18`, `:5`) | Hai tệp kiểm trên màn hình đổi sang dạng gọn không dòng trống: `test_phi.py` 12 dòng (hai nửa 1-6 và 7-12, nối liền), `test_float.py` 5 dòng. Gõ đúng như màn hình thì `test_phi.py:12` và `test_float.py:3`; hai số này thay `:18`/`:5` ở màn hình, `verify` (`py(... out=...)` chạy pytest 9.2.0 thật trên đúng tệp) và đã đo lại. Thêm ghi chú ở bước đọc ca đỏ: "`:12` là dòng thứ mười hai của tệp bạn gõ (không có dòng trống); thêm dòng trống thì số này đổi" (chữ và lời đọc). Cổng `screen-files` dựng lại tệp từ khối màn hình và chạy thật: PASS (L12 14/14) |
| L04 "lũy thừa của độ dài" | "tăng theo hàm mũ: gấp đôi mỗi ký tự thêm vào" (chữ và lời đọc) |
| L10 `str`/`datetime64[us]` chỉ đúng pandas 3 | formula.1: "đo bằng pandas 3.1.1; bản 2.x hiện `object`"; ví dụ ngày: "đo bằng pandas 3.1.1; pandas 2.x hiện `datetime64[ns]` (phần tỉ giây): nội dung giống, chỉ tên kiểu khác"; lời đọc: "tên kiểu này là của bản thư viện ghim trong khoá, bản cũ hơn ghi tên khác" |
| L10 "thiếu tiền" | "ô tiền trống" (chữ và lời đọc; cả hai chỗ) |
| L03 `doc_lap` bị cắt chữ cuối chú thích đỏ | Chú thích tách hai dòng ở x=580 (trước dài ~770 px đè hộp `doc_lap` ở x=900); xem khung 00037: đủ chữ "… KHÔNG tạo danh sách mới" |
| L06 nút "Dừng video" đè "để chấm" | Đề practice.0 rút ngắn 2 dòng (gộp "rồi chạy đoạn thử" vào mục 3; đoạn "Đo" còn 2 dòng); xem khung 00126: dòng "… mở Git Bash tại đó để chấm." nằm trên nút, không đè |
| L07 formula.2/.4 đoạn giải thích nằm trên tiêu đề "Bước" | Đảo thứ tự: khối mã (có tiêu đề "Bước 2"/"Bước 3") đứng trước, đoạn "Vì…" đứng sau, như các bước khác |
| L13 `exec`/`sys.path.insert` không giảng; pause lab nặng | de.md: thêm hai mẫu mã nạp mô-đun từ thư mục tạm ("Cách 1" `sys.path.insert(0, str(thu_muc))` rồi `from phan_tich import tong_theo_loai`; "Cách 2" `ns = {}; exec(MODULE, ns)`), nhắc làm khi thư mục tạm còn tồn tại; hộp "Nếu kẹt" trên màn hình và lời đọc có một câu tương ứng; ghi thời gian dự kiến 45-60 phút, chia hai lượt. Pause: L13 practice 600 s thành 1200 s (cộng quiz 60 s: 21 phút); L12 practice 420 s thành 1200 s (21 phút). Lint không có trần cho `pause` |

## 4. Cổng thật (máy đang bận nên đã chạy từng bài một)
- `bash audit/pyt/gates.sh Lxx` cho 10 bài đổi: lint **0 FAIL, 0 WARN** ở cả 10; render **0 vấn đề** ở cả 10; `lab_gate PYT`: **14 PASS · 0 FAIL (195 lab)** ở cả 10 lần.
- `verify_pyt`: L00 23/23, L04 17/17, L05 16/16, L06 16/16, L07 14/14, L08 14/14, L12 14/14, L13 9/9. **L03 và L10 có ô `measure` thời gian lệch ×8 so số lưu khi máy tải** (VS Code, docker và các tác tử khác đang chạy): chạy lại riêng khi máy bớt tải: **L03 21/21, L10 18/18 PASS**. Bài và số đo không đổi (không phải lỗi bài).
- Số từ lời đọc (≤ 2 300): L00 2293, L03 2257, L04 2229, L05 2097, L06 2264, L07 2125, L08 2291, L10 2135, L12 2207, L13 2295 (thêm ở đâu thì cắt ở chỗ khác: L08 cắt câu "Hôm nay ta thấy ý tương tự…" ở prereq, câu về dấu nhắc môi trường ở ví dụ, câu "Chi phí chỉ là một ít dung lượng đĩa"; L00 cắt câu "Tóm lại, số thực sai nhiều hơn…" và câu bản 3.13 ở prereq.1 — nội dung này vẫn nằm trong chữ trên màn hình; L13 cắt câu về dòng ghim).
- `lv.py curriculum curriculum/pyt.yaml`: 14 bài, **0 lỗi**; `tests/test_e52.py`: **0 FAIL**; `check_curricula_graph.py`: tham chiếu hỏng 0, chu trình 0, VER không PASS 0; `arith_scan.py`: 243 phép tính, **0 FAIL**.
- `screen_code.py check --course PYT` trước tái sinh: STALE 7 (L08 formula 3/5, L12 hook/formula/example/pitfalls, đúng các khối đã đổi); sau `gen-pyt` (334 khối, ghi 334, chưa khớp 0): `check --course PYT` **PASS 526 · FAIL 0 · STALE 0 · MISSING 0 · ORPHAN 0 · WARN 0**.

## 5. P1 dự kiến
Mọi mục "Cần biết trước" còn lại của báo cáo đã xử lý: L00 (`echo $?`, Git Bash), L05 (`tail`, luồng in), L08 (`grep -E`, `wc -l`, `find|sort`, `mv`, `2>&1`, `python -m`), L12 (`python -m`), L13 (nạp mô-đun từ thư mục tạm; mẫu mã ở de.md và gợi ý trên màn hình). Dự kiến P1 = 2 ở 14/14 bài.

## 6. Mục không sửa / còn hở
- **Không có cách kiểm tai người** (giọng, ngắt nghỉ, cách đọc "byte", "JSON"; các câu `say` mới/đổi ở L00, L05, L08, L12, L13, L10, L04 là câu TTS mới): chỉ kiểm được ≥ 8 từ mỗi step, 4-38 từ mỗi câu (lint WARN 0).
- **`ls ngan_hang`**: hiện `__init__.py  phi.py` trên một dòng (đúng với cửa sổ Git Bash tương tác); khi chuyển vào ống thì mỗi tên một dòng. Màn hình chỉ chạy dạng tương tác nên khớp.
- **Số dòng vết lỗi L12**: dạng gọn không dòng trống trái PEP 8 (hai dòng trống giữa các hàm); đã chọn để số dòng gõ-đúng-màn-hình xác định được; ghi chú trên màn hình nói thêm dòng trống thì số đổi.
- **Thời gian dừng L12/L13 là dừng tĩnh trong video** (người học vẫn làm 30-60 phút thật); không có cách "nới" hơn trong khuôn khổ khoá.
- **Số đo thời gian dễ lệch ×8 khi máy tải** (`verify_pyt` ô `measure` của L03, L10 bài không đổi số): nên chạy `verify_pyt` toàn khoá khi máy rảnh.
- Video của cả 10 bài STALE, cần dựng lại (build/tts/asr do người điều phối).
