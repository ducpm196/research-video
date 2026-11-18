# fix_S01_PYT_A: sửa nửa A khoá PYT (L00–L06), 2026-11-14

Nguồn: `reports/S01_PYT.md` phần A (L00–L03) và B (L04–L06) + `BRIEF_FIX_PYT.md`. Sửa NGUỒN `audit/pyt/src/l00.py … l06.py` rồi `gen`; không chạm `l07…l13`, `labs/PYT/L07…L13`, `lessons/pyt/` bằng tay. Không chạy `gen-pyt`, `screen_code check`, build/tts/asr/git.

## 1. Kết quả cổng (số thật, lần chạy cuối)
| Bài | verify (gồm screen) | lint | từ lời đọc | render | ghi chú |
|---|---|---|---|---|---|
| L00 | 23/23 | 0 FAIL 0 WARN | 2273 (trước 2387) | 0 vấn đề | |
| L01 | 19/19 | 0/0 | 2151 | 0 | |
| L02 | 14/14 | 0/0 | 2098 | 0 | đo lại `--remeasure` lúc máy rảnh hơn |
| L03 | 21/21 | 0/0 | 2246 | 0 | |
| L04 | 17/17 | 0/0 | 2224 | 0 | |
| L05 | 16/16 | 0/0 | 2011 | 0 | |
| L06 | 16/16 | 0/0 | 2291 (sát trần 2300) | 0 | |
- Một lần `verify_pyt.py L00 … L06` gộp: **126/126 PASS** (py, repl, sh, measure, screen). `lv.py curriculum curriculum/pyt.yaml`: 14 bài, 0 lỗi. `tests/test_e52.py`: 0 FAIL. `lab_gate.py PYT`: 14 PASS · 0 FAIL (76 lab được bài tham chiếu), chạy lần cuối sau mọi sửa.
- Đã xem khung PNG: L01 hook (00004) + quiz (00117); L02 demo đo (00066); L03 intuition (00029) + Bước 1b (00043); L04 Bước 4a (00069) + ghi chú phiên bản (00055); L05 Bước 2 (00040); L06 hook (00005), lớp đầy đủ (00054), getsizeof (00075).

## 2. Cổng mới: kiểm "khối trên màn hình = mã chạy thật" (gốc chung 1)
- `audit/pyt/screen_check.py` (mới) + hai chỗ nối trong `audit/pyt/verify_pyt.py` (giữ `SPECS[lid] = build()[1]`, gọi `screen_check.run(...)` trước dòng tổng). Đọc đặc tả do `build()` trả về (chạy được trước `gen`).
  - Khối phiên `>>>`: gõ lại nguyên văn từ trên xuống; các khối `>>>` của cùng một CẢNH nối tiếp trong một cửa sổ `code.InteractiveConsole`, mỗi cảnh một cửa sổ mới (3.11 và 3.13); từng câu phải ra đúng kết quả hiện ngay dưới (bắt biến chưa gán, thiếu `import`, kết quả dán nhầm).
  - Khối mã chương trình (khớp một đoạn liên tiếp của một `py(...)`) có khối kết quả liền sau trong cùng step: chạy ĐÚNG đoạn đó (cộng các đoạn trước của cùng chương trình đã hiện trong cùng cảnh) và so từng dòng với khối kết quả; khối đứng một mình: kiểm cú pháp; khối khớp một `measure(...)`: bỏ qua.
- Bằng chứng nó bắt đúng lỗi gốc: trước khi sửa, chạy trên L00–L06 cho FAIL ở L01 hook#1 (`IndentationError`), L02 hook#0 (màn hình hiện thêm 3 dòng không do mã in), L03 pitfalls#0 (hiện thêm 2 dòng), 4 + 3 + 7 + 8 + 3 + 10 câu `>>>` NameError (L00 formula#1, L02 formula#1/#3, L03 formula#0/#3/#4, L04 hook/formula, L05 JSON, L06 formula/pitfalls), và L06 example (lớp không hiện trọn). Sau sửa: 0 FAIL.
- Lưu ý với nửa B: `verify_pyt.py L07 … L13` giờ cũng chạy kiểm này; bài nào còn khối `>>>` dùng biến chưa gán trong cùng cảnh hoặc mã cụt sẽ FAIL ở dòng `Lxx screen`.

## 3. MUST (9 mục của nửa A) — đã sửa hết
| # | Chỗ | Cách sửa |
|---|---|---|
| 1 | L01 hook#1 mã cụt | Hiện đủ 9 dòng `tong.py` + kết quả (screen_check xác nhận chạy ra đúng 2 dòng). |
| 2 | L01 quiz#0/#2 | Đề hiện mã ngay trong khung; đổi `P_DAO` thành đổi chỗ THẬT hai nhánh đầu (`< 20000000` rồi `< 1000000`) với `tien = 500000` → `vua` (đúng bài học "thứ tự nhánh"), lời đáp án và `checks` khớp. |
| 3 | L02 hook#0 | Hiện cả chương trình `ham.py` (đủ 3 `print`) thay cho `lines=(1, 6)`. |
| 4 | L02 formula#3 | Hiện trọn `def tang`, `tang(5)`, `f = tang`, `f(5)`, `type(tang)`, lambda; formula#1 hiện `def tong_tien` trước khi gọi. |
| 5 | L02 scale#1 | Đo lại TRONG MỘT HÀM, lấy lần nhanh nhất của 3 lần; hiển thị 2 chữ số có nghĩa (`pyt_a.t2`), tỉ lệ tính từ chính hai số hiện ra (`val2`), nêu rõ phạm vi (Python 3.11, vòng lặp trong hàm, hàm chỉ một phép cộng ⇒ cận trên, hàm làm việc thật nhỏ hơn nhiều). Số đo cuối: ở 10^7 lần gọi, gọi hàm ≈ 2,0 s so với viết thẳng ≈ 1,2 s (≈ 1,7×; ở 10^6: 2,3×), ghi "số minh hoạ"; bảng và lời đọc cùng một con số. |
| 6 | L03 formula#0/#3/#4 | Hiện phép gán (`gd = …`, `xs = …`) trước khi hỏi; sort/comp hiện từ bước 0. |
| 7 | L03 pitfalls#0 | Chương trình mới `bi_danh_is` (5 dòng, in 2 dòng: danh sách và `goc is ban_sao`) và khối kết quả đúng 2 dòng. |
| 8 | L03 mục tiêu 1 "sửa" | Thêm step "Bước 1b": `gd[0] = 500000` (danh sách sửa được) và `tk[0] = 500000` → `TypeError` (bộ không sửa được); `covers` giữ nguyên (formula). |
| 9 | L06 hook | "một trăm chín mươi byte mỗi đối tượng, đã tính cả chuỗi và số bên trong" (190 B/đối tượng đã gồm dữ liệu: tracemalloc 193,4 MB cho 10^6). Quét `audit/pyt/src/l00…l06.py` và `lessons/pyt/L00…L06`: không còn "chục byte" hay số + " B" trong `say`/`srt` ở nửa A (L06.yaml/srt cũ còn cho tới khi gen/dựng lại). |

## 4. SHOULD (21 mục) — đã sửa hết, không bỏ mục nào
- L00 (3): "bảy phép toán" thống nhất ở tên cảnh, lời đọc, mục tiêu (cả `curriculum/pyt.yaml`); `prereq#1` hiện lỗi thật (bỏ `2> loi.txt`; `sh` đặt `only311=True`, ghi chú 3.13 chen dòng mã/`^`, cách đọc vẫn đúng; không còn "dòng ngay trên"); `round` về số chẵn: thêm step với `round(0.5)=0`, `round(1.5)=2`, `round(2.5)=2` và cách tự viết "làm tròn nửa lên" bằng số nguyên.
- L01 (1): scale#1 dùng 2 chữ số có nghĩa (≈ 140 ms, ≈ 1,5 s), nói rõ "mỗi lần nhân 10 số lượt, thời gian tăng khoảng 10 lần, lệch vài chục %".
- L02 (2): REPL formula#1 hiện `def` trước khi gọi; check#0 "nên ta tin hàm hơn, dù một lần thử chưa phải là chứng minh".
- L03 (4): "luôn bằng" thêm điều kiện "khi chỉ số cuối không vượt quá độ dài"; tỉ lệ và "mười hai phút" tính từ số hiện ra (≈ 54, 73 000, ≈ 12 phút); "bộ chứa toàn giá trị không sửa được" làm khoá; SVG ô rộng 160, chữ "12 000 000" không chạm mép.
- L04 (3): ghi chú 3.13 sửa đúng (hiển thị lỗi khác nhau giữa 3.11 và 3.13 ở cả cửa sổ `>>>` lẫn chạy tệp, dòng cuối giống nhau); "a+b tăng tuyến tính" thay bằng số đo (4 000 ký tự ≈ 30 ms, 8 000 ký tự ≈ 250 ms: tăng nhanh hơn tỉ lệ nhưng không bùng nổ; bài nêu hai số đo và "gấp đôi chuỗi mà thời gian gấp nhiều lần", không nêu hệ số vì số đo trên máy tải nhảy từ ×4 đến ×8); mọi khối `>>>` đủ `s = …`, `dong = …`, `import re` (Bước 1–4, hook, pitfalls).
- L05 (4): "hầu hết các máy" → "nhiều máy cá nhân", tiêu đề "có thể hết bộ nhớ", nhãn "rồi tách thành dòng"; 31 byte ghi là của NỘI DUNG, tệp trên đĩa Windows 33 byte (CRLF); thêm step hiện nội dung `gd.csv` trước khi đọc.
- L06 (4): hiện trọn lớp `TaiKhoan` (13 dòng) trước khi dùng; "mọi thay đổi đều đi qua cửa này" → quy ước, Python không ép (ghi cả ở recap/Tư duy); `__dict__` "thường là" (trừ `__slots__`); `curriculum/pyt.yaml` + `gen_curriculum.py` đổi "gấp nhiều lần" thành "khoảng 190 MB so với 160 MB, hơn khoảng 20%".
- Thêm: nhãn "dựng" ở SVG L06 không còn bị gạch đè.

## 5. Dạy đo thời gian và bộ nhớ (E51, mục tiêu "đo thời gian và bộ nhớ" của khoá)
- L02 (example, mục tiêu 9 mới, `covers (9, "example")`): `time.perf_counter()` — đọc đồng hồ trước/sau, hiệu là thời gian chạy, chạy nhiều lần lấy lần nhanh nhất; chương trình hiện nguyên văn (`measure l02_demo` chạy đúng mã đó).
- L06 (example, mục tiêu 10 mới, `covers (10, "example")`): `sys.getsizeof` (chương trình `kich_thuoc`: 28, 56, 8056 byte, chạy thật trên 3.11 và 3.13; chỉ tính phần của riêng giá trị) và `tracemalloc` (chương trình hiện nguyên văn, `measure l06_demo`; đếm mọi byte cấp phát). Bảng quy mô L06 đo đúng bằng `tracemalloc`.
- Cả hai thêm vào `curriculum/pyt.yaml` (mục tiêu mới). L07–L13 (nửa B) chỉ cần nhắc lại ngắn khi dùng và khai `assumes`.

## 6. P1 (thuật ngữ tại chỗ) và sổ E52
Đã giảng tại chỗ ở lần đầu trong bài (một câu + ví dụ nhỏ): L00 `type(x).__name__` (dấu chấm = thuộc tính); L01 `in` ("nằm trong") và bộ; L02 chữ viết tắt thuế, trạng thái cửa sổ gõ, `perf_counter`; L03 `x in tập hợp`, phương thức bằng dấu chấm, `is`/đối tượng, `d.get`; L04 byte hệ 16, `b'…'`, `.encode/.decode`, `.group()`, `ms/µs/ns`; L05 `newline=""`, `.stat().st_size`, `type(x).__name__`, `-c`, `2>`, `$?`, `cut -d`, "đỉnh"; L06 `isinstance`, `pass`, thấu chi, hai cột đầu hook, `getsizeof`, `tracemalloc`. Dự kiến P1 = 2 ở 7/7 bài nửa A (cần người đọc độc lập xác nhận).
`tools/registry/symbols.PYT.yaml` (thêm bằng Edit nhỏ, cùng tệp với nửa B): `pyt_perf_counter` (L02 `introduces`), `pyt_getsizeof`, `pyt_tracemalloc`, `pyt_isinstance`, `pyt_pass` (L06 `introduces`). Nửa B đã thêm `pyt_ngoai_suy` (thuật ngữ này xuất hiện đầu tiên ở L01): L01 `introduces: [pyt_ngoai_suy]` ở step bảng quy mô; L02–L06 `assumes: [pyt_ngoai_suy]`.
**Việc cho nửa B / điều phối**: bài L07–L13 dùng `ngoại suy` phải khai `assumes: [pyt_ngoai_suy]`; L07 dùng `isinstance`/`pass` ⇒ `assumes: [pyt_isinstance, pyt_pass]`; L13 (và bài nào dùng) `tracemalloc`/`perf_counter`/`getsizeof` ⇒ `assumes` tương ứng (cổng E52 sẽ báo đúng chỗ).

## 7. Cách viết số trong `say` (gốc chung 2)
Nửa A: không còn mẫu "N chục byte" hay số + " B" (grep `src` và YAML). Lời đọc ghi "byte" đầy đủ và số bằng chữ. Lần quét cuối `lessons/pyt/L00…L13_*.yaml`: 0 chỗ "chục byte".

## 8. Không sửa / còn mở (có lý do)
- L04: hình cơ chế "thử mọi cách chia chuỗi" của `(a+)+b` (P3 trong bảng độ sâu, không nằm trong MUST/SHOULD): không thêm, vì cần một cảnh vẽ mới và bài đã chạm trần thời lượng (2224 từ).
- Số đo thời gian (L01, L02, L04) lấy khi máy kiểm đang tải nặng (nhiều tác tử); số tuyệt đối lệch cả 2×; bài đều ghi "số minh hoạ". L02: tỉ lệ gọi hàm/viết thẳng có thể lệch giữa hai hàng của bảng (cùng bậc, cùng chiều); nên chạy lại `verify_pyt.py L02 --remeasure` khi máy rảnh rồi `gen`.
- L06 sát trần 2300 từ (2291): thêm câu giảng phải cắt chỗ khác. L00 giảm 114 từ để vừa chỗ thêm `round`/`prereq`.
- Video/srt của L00–L06 cũ hơn YAML mới: cần dựng lại (người điều phối). Sổ `screen_code` của PYT cần `stub` rồi điền (khối mã đổi nhiều).
- Ghi chú 3.13: L07 `breakpoint()` (nửa B). Ở nửa A đã nói rõ ở L00 (prereq), L03 (Bước 1b) và L04.

## 9. Tệp đổi
`audit/pyt/src/l00.py … l06.py`, `audit/pyt/src/pyt_a.py` (mới, `t2`/`val2`), `audit/pyt/screen_check.py` (mới), `audit/pyt/verify_pyt.py` (2 chỗ nối), `audit/pyt/gen_curriculum.py` (1 chuỗi), `curriculum/pyt.yaml` (mục tiêu L00, L02, L06 + ví dụ L06), `tools/registry/symbols.PYT.yaml` (5 mục), `audit/pyt/measured.json` (đo mới `l02_call`, `l02_demo`, `l04_redos` thêm `t_lin_*`, `l06_demo`), `lessons/pyt/L00…L06_*.yaml` và `labs/PYT/L00…L06/de.md` (sinh bởi gen).
