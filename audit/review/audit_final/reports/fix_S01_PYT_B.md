# fix_S01_PYT_B — sửa NỬA B khoá PYT (L07–L13), 2026-11-14

Nguồn: `reports/S01_PYT.md` (phần B, C, D) + `BRIEF_FIX_PYT.md`. Chỉ sửa NGUỒN `audit/pyt/src/l07.py … l13.py` rồi `gen.py` (YAML trong `lessons/pyt/` do máy sinh). Không chạm `l00–l06.py`, `labs/PYT/L00…L06`. Không chạy build/tts/asr/audit_all/git/gen-pyt/screen_code.

## Kết quả cổng (chạy THẬT, `bash audit/pyt/gates.sh Lxx`, lần chạy cuối)
| Bài | verify_pyt (py/repl/sh/measure/screen) | lint | render | lab_gate | lời đọc |
|---|---|---|---|---|---|
| L07 | 14/14 PASS | 0 FAIL, 0 WARN | 137 khung, 0 vấn đề | 14 PASS, 0 FAIL | 13,8 phút (2075 từ) |
| L08 | 12/12 PASS | 0 FAIL, 0 WARN | 152 khung, 0 vấn đề | 14 PASS, 0 FAIL | 15,1 phút (2261 từ) |
| L09 | 15/15 PASS | 0 FAIL, 0 WARN | 139 khung, 0 vấn đề | 14 PASS, 0 FAIL | 13,5 phút (2025 từ) |
| L10 | 18/18 PASS | 0 FAIL, 0 WARN | 145 khung, 0 vấn đề | 14 PASS, 0 FAIL | 14,1 phút (2108 từ) |
| L11 | 11/11 PASS | 0 FAIL, 0 WARN | 144 khung, 0 vấn đề | 14 PASS, 0 FAIL | 14,8 phút (2224 từ) |
| L12 | 9/9 PASS | 0 FAIL, 0 WARN | 135 khung, 0 vấn đề | 14 PASS, 0 FAIL | 13,4 phút (2007 từ) |
| L13 | 9/9 PASS | 0 FAIL, 0 WARN | 138 khung, 0 vấn đề | 14 PASS, 0 FAIL | 15,0 phút (2254 từ) |

Tất cả ≤ 16 phút và ≤ 2 300 từ. Thêm: `python -B tools/lv.py curriculum curriculum/pyt.yaml` = 14 bài, 0 lỗi; `python tests/test_e52.py` = 0 FAIL. `verify_pyt` được chạy riêng từng bài bên trong `gates.sh` (không chạy gộp một lệnh `verify_pyt L07…L13`). Đã xem bằng mắt khung PNG: L07 (hook), L08 (hình thứ tự tìm mô-đun, bảng số gói), L10 (gd.csv, bảng category), L11 (hook hai biểu đồ), L12 (hình trục số), L13 (Bước 0 cách đo, cách A).
Máy đo đang tải nặng nên lần chạy đầu của `l08_import` báo lệch ×8 so với số lưu; đã đo lại bằng `verify_pyt.py L08 --remeasure` (5 số mới, gồm `pytest`); các số thời gian trong bài là số minh hoạ cùng bậc, chậm hơn máy rảnh 2–5 lần.

## MUST (6/6 đã sửa; mỗi cái kiểm lại bằng cách chạy thật trước khi sửa — báo cáo gốc đúng cả 6)
| Bài | MUST | Cách sửa |
|---|---|---|
| L09 | hook/scale/quiz "nhanh gấp ≈ 30" mâu thuẫn "hàng trăm" | Phép đo cũ (`3*a+1` rồi `.sum()` so với vòng `3*i+1`) khác việc hook nói ("cộng một triệu số"); đổi phép đo thành khóa mới `l09_sum`: vòng `for x in xs: s += x` trên danh sách có sẵn so với `a.sum()` (min của 3 lần). Đo: 1e4 = 191×, 1e6 = 247×, 1e7 = 268×. Tỉ số "nhanh gấp" tính từ chính các số đã làm tròn hiện trên màn hình; tiêu đề, quiz, recap dùng cụm "hàng trăm"/"hàng chục" tự suy ra từ tỉ số đo (hôm nay "hàng trăm"). |
| L09 | formula#3 `x.mean()`/`x.std()` dùng `x` chưa định nghĩa | Bước 4 hiện trọn `import numpy as np` + `x = np.array([2, 4, 4, 4, 5, 5, 7, 9])` rồi các dòng sau (R_STD 0:7); lời đọc đọc tám số. Cả công thức bước 1–3 cũng hiện `import` + dựng `so_tien` (trước đây `so_tien` chỉ hiện ở ví dụ, sau ba bước dùng nó). |
| L10 | hook "một trăm bốn mươi chục byte mỗi dòng" | Lời đọc: "…cỡ một trăm bốn mươi byte mỗi dòng" (đo 139 B); hook nêu rõ bốn cột (mã, loại, tài khoản, số tiền). |
| L13 | formula#0 "chín mươi bốn chục byte" | "cỡ chín mươi bốn byte mỗi dòng" (đo 94,25 B/dòng trong `measured.json`); không còn "chục byte" ở bất kỳ nguồn nào (đã quét `audit/pyt/src` và `say` của 14 YAML: 0 mẫu "chục byte", 0 mẫu "N B"/"N KB/MB/GB" trong lời). |
| L13 | quiz#1 câu 1 "A cần cỡ 5 GB nên sát giới hạn" | Sửa lời và màn hình: bộ nhớ ≈ 5 lần dung lượng tệp (đo 4,99×) ⇒ tệp 5 GB cần ≈ 25 GB, nhiều hơn 8 GB nên CHẮC CHẮN hết bộ nhớ; thêm kiểm `5 * 5 * 10 ** 9 > 8 * 10 ** 9`. |
| L13 | mục tiêu 1 "Đo thời gian và bộ nhớ" không được dạy | Giữ mục tiêu, thêm Bước 0 trong cảnh `formula`: chương trình `cach_do` (thật, verify 3.11/3.13) đọc `time.perf_counter()` hai lần và `tracemalloc.get_traced_memory()[1]`; nhắc lại cách đo ở cảnh `scale`; `assumes: [pyt_perf_counter, pyt_tracemalloc]` (nửa A dạy ở L02/L06; `lv.py curriculum` chấp nhận, nghĩa là nửa A đã `introduces` hai id này). |

## SHOULD (36/36 xử lý; 2 chỗ chỉ sửa một phần, lý do ở mục cuối)
- **L07 (4)**: bỏ hàng 1% (try/isdigit ở 1% đổi chiều theo máy/phiên bản), chỉ giữ 0% và 50% + chú thích; "hai cách cho cùng tổng" chỉ khi chuỗi toàn chữ số/chữ cái, thêm `"1.250.000".isdigit()` → `False` (hiện trong cửa sổ `>>>`); `breakpoint()`: ghi rõ 3.11 dừng ở dòng kế, 3.13 dừng ngay dòng đó (bảng + lời); ghi chú traceback 3.13 (`<python-input-N>`, dòng mã, `~^`) ở ví dụ 0 và ví dụ 1; hook hiện trọn mã (trước chỉ dòng 4–8, thiếu `chia`).
- **L08 (7)**: bảng số gói tính bằng `importlib.metadata` trong venv (phép đo `l08_pkgs`): 1 / 4 / 12 / 17 (cộng dồn), thêm dòng thư viện kiểm thử; cột thời gian ghi rõ "nạp RIÊNG", bỏ dấu "+", thêm đo `pytest`; tiêu đề cảnh cụt sửa lại; `__init__.py`: nói đúng (từ 3.3 thiếu vẫn nạp được, nên có); "che" chỉ đúng với mô-đun viết bằng Python (sys/time/math không bị che); `cut -c1-58` được giảng + ghi chú 3.13 dài thêm gợi ý đổi tên tệp; hiện mã `giao_dich.py`, `chay.py`, `ngan_hang/phi.py`, `chay_goi.py`; `covers` mục tiêu 1 → `formula`; chữ chạm viền ô hình `intuition` (nới ô); mục tiêu 6 sửa cho khớp bảng.
- **L09 (3)**: dựng `so_tien` trước khi dùng; hình broadcast dùng đúng ba hàng dữ liệu; "biên dịch" giảng tại chỗ.
- **L10 (6)**: lời đọc khớp màn hình ở nhóm theo loại / theo tài khoản (tách hai màn hình, giải thích từng tổng); bảng tốc độ nêu rõ "vòng lặp trên danh sách" và hiện tỉ số tính từ số đã hiện (đo lại: 3 loại/cột số), có câu về chi phí cố định ở bảng nhỏ; category: đổi cấu hình đo (3 loại, 1 000 tài khoản ở cả hai quy mô, khóa `l10_mem2`) ⇒ tiết kiệm 5,5× / 7,3× và lời nói rõ "không đổi theo số dòng"; "bốn cột" liệt kê; hiện `gd.csv` (8 dòng) và `tk.csv` trước khi đọc; quiz đổi sang bảng nhỏ mới (không còn lặp đáp án đã hiện); `.loc` giảng; lab: `de.md` + màn hình + gợi ý ghi rõ `int(...)` và `idxmax()`; nhãn "bảng gốc (6 dòng có số tiền)".
- **L11 (6)**: mọi chương trình vẽ hiện trọn (3 dòng nạp thư viện + thân; không còn "lines=" cắt mất import); ô mã rỗng ở pitfalls#0 hết (dùng `truc_cat_don`); nhãn giá trị cột nằm trong cột khi chạm viền, chú thích dời xuống khỏi nhãn trục; "cột nhóm" → "biểu đồ tần suất (histogram)" (cả mục tiêu); `covers` mục tiêu 3 → `example` + ví dụ đọc mẫu biểu đồ B theo thứ tự tiêu đề/đơn vị/trục/thang + câu 3 trong quiz; thêm chương trình `gop_luc_giac` (`hexbin`, in 100000 điểm trong các ô) cho cột "ô lục giác".
- **L12 (4)**: hiện `phi_chuyen` (8 dòng) + dòng đổi `<` → `<=` ở hook và bước 3; đặc tả "tiền chia 1000 làm tròn xuống" nêu trong hình, bước 1, bảng ca biên; "máy gần như không đổi" → "tăng chậm hơn rất nhiều, từ vài giây tới vài phút"; thời gian chạy tay hiện 2 chữ số (3,5 ngày, 35 ngày); hình trục số có đủ ba vạch ngưỡng và nhãn đúng chỗ.
- **L13 (6)**: "≈ 4 phút" → ngoại suy tính từ số ĐÃ làm tròn hiện ra (2 s × 100 = ≈ 3 phút); bỏ "verify_pyt" khỏi màn hình (thay bằng cách đo thật); hiện `gd.csv` 8 dòng và mã cách A (`ca_tep`); `trung vị` giảng + phản ví dụ bằng số ([1,2,9] và [3,4,5]: 3 ≠ 3,5), `xếp trên đĩa` giảng; ở 10^3 "cả ba cách chỉ vài phần nghìn giây, chênh lệch không có ý nghĩa"; lab: hàm chấm in dòng `Ly do` cho từng tiêu chí CHUA (và `--tb=line` cho pytest), `de.md` + gợi ý nói rõ `\\n`/chuỗi thô, `tempfile` giảng.

## Gốc chung của brief (phần nửa B)
1. **Mã cụt / REPL biến chưa gán**: mọi khối `>>>` và khối chương trình trong L07–L13 hiện trọn (import, gán biến, thân vòng lặp, `print`); khối chương trình dài được tách step (code | kết quả + ghi chú). `verify_pyt.py` đã có `screen_check` (do người điều phối thêm): L07–L13 qua cả cổng này.
2. **"N chục byte"**: quét `audit/pyt/src/*.py` và `lessons/pyt/*.yaml`: 0 mẫu "chục byte" còn lại, 0 mẫu số + "B/KB/MB/GB" trong `say`.
3. **P1**: giảng tại chỗ + `introduces`/`assumes` (E52). Đã THÊM 19 mục `term:` vào `tools/registry/symbols.PYT.yaml` (Edit nhỏ, cạnh 5 mục của nửa A): `pyt_ngoai_suy`, `pyt_pip`, `pyt_site_packages`, `pyt_sys_prefix`, `pyt_cut`, `pyt_bien_dich`, `pyt_loc`, `pyt_datetime64`, `pyt_idxmax`, `pyt_assert`, `pyt_decorator`, `pyt_subprocess`, `pyt_ham_thuan`, `pyt_chunksize`, `pyt_trung_vi`, `pyt_tempfile`, `pyt_diem_anh`, `pyt_luc_giac`, `pyt_get_offsets`; L07 dùng `pyt_pass` (nửa A đã khai); L10–L13 `assumes` `pyt_ngoai_suy`, `pyt_bien_dich` (L09 giới thiệu), L13 thêm `pyt_perf_counter`, `pyt_tracemalloc` (nửa A). P1 dự kiến: 7/7 bài nửa B = 2 (P1 chưa chấm lại bằng người đọc; đây là dự kiến theo danh sách "Cần biết trước" của từng bài đã xử lý hết).
4. **E51 mục tiêu ↔ video**: L08 (covers + mục tiêu 6), L11 (covers mục tiêu 3 → ví dụ đọc mẫu; mục tiêu 1 đổi chữ), L13 (mục tiêu 1 có Bước 0 dạy đo) đã đồng bộ ở `curriculum/pyt.yaml` + `audit/pyt/gen_curriculum.py` (META `example` của L08, L10, L12). `lv.py curriculum curriculum/pyt.yaml`: 0 lỗi.
5. **Python 3.13**: L07 `breakpoint()` + traceback `<python-input-N>`; L08 thông báo csv dài hơn ở 3.13; nội dung lỗi giống nhau nhưng dạng hiển thị khác (đã nói).
6. **Mọi SHOULD**: xem trên; hai mục chỉ sửa một phần ở mục dưới.

## Mục không sửa hoặc sửa một phần, và lý do
- **L11 hình ô lục giác**: thêm chương trình `gop_luc_giac` chạy thật (in 100000 điểm đếm trong các ô) nhưng KHÔNG vẽ SVG minh hoạ các ô sáu cạnh: hình không mang số liệu kiểm được; mã + kết quả đủ để người học lặp lại.
- **L08 `pip freeze` chạy trên màn hình**: không chạy (trong venv trống cho đầu ra rỗng; ví dụ có nghĩa cần cài ~17 gói qua mạng). Bài nêu đúng vai trò (sinh tệp ghim) ở Bước 4 + pitfalls, bước cài/freeze thật nằm ở lab.
- **L07 `breakpoint()` không có bước demo**: cần cửa sổ tương tác (`p x`, `n`, `c`); bài nêu rõ khác biệt vị trí dừng 3.11/3.13 và lệnh trong bảng.
- **L08 `labs/pyt` vs `labs/PYT`**: trên kho này chỉ có thư mục `labs/PYT` (báo cáo gốc thấy hai tên do hệ tệp Windows không phân biệt hoa thường); `de.md` đã gọi đúng `PYT`.

## Việc người điều phối cần chạy một lần sau khi cả hai nửa xong
`gen-pyt` / `screen_code check --course PYT` (tái sinh sổ), và `python audit/pyt/gen_curriculum.py` nếu nửa A đổi mục tiêu (META của L08/L10/L12 đã sửa; `curriculum/pyt.yaml` đã được vá tay cho khớp).
Tệp phụ: `audit/pyt/measured.json` có khóa mới `l08_pkgs`, `l09_sum`, `l10_mem2` và `t_import_pytest` (số đo do verify_pyt ghi; máy đang tải nặng nên số tuyệt đối chậm hơn máy rảnh 2–5 lần, chỉ so bậc và chiều).
