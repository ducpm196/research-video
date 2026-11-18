# S01b PYT (vòng 2): đã đọc 14/14 bài

Người đọc độc lập; không mở báo cáo khác trong `reports/`, không mở `plan_*`, `handover_*`. Đọc TRỌN `say`/`show`/quiz/lab của 14 YAML, `curriculum/pyt.yaml`, `.srt`, `chapters.txt`, `_frames.txt`. Môi trường: Python 3.11.9 (hệ thống, và `labs/.venv-pyt` có numpy 2.4.6, pandas 3.1.1, matplotlib 3.11.2, pytest 9.2.0), Python 3.13.5 (`.venv`, chỉ mã thuần). Không sửa tệp nào trong kho; tệp tạm ở scratchpad.

Tình trạng video lúc đọc (so `spec_sha256` với `lv.spec_digest`): L00, L01, L02, L04, L05, L06, L07, L09, L10, L12, L13 = FRESH; **L03, L08, L11 = STALE** (đang dựng lại; YAML mới hơn video, `.srt` của ba bài này thiếu câu: L03 "là hai kiểu chứa dữ liệu cuối cùng của bài này"; L08 "ta gói các tệp liên quan vào một thư mục chung gọi là"; L11 "trên trục", "mỗi vạch cách nhau cùng một khoảng"). Ba bài đó tôi đọc theo YAML hiện tại và xem khung hình của video cũ. 11 bài còn lại: `say` khớp `.srt` từng từ (ratio 1.0000).

## 1. Kết luận theo ngưỡng

| Ngưỡng | Kết quả |
|---|---|
| MUST = 0 | **KHÔNG ĐẠT: 1 MUST** (L12) |
| P1 = 2 ở ≥ 90% bài | **KHÔNG ĐẠT: 8/14 = 57%** (P1=1 ở L00, L05, L06, L07, L12, L13; mỗi bài 1–2 từ, xem bảng) |
| P8 = 2 ở 100% bài | **ĐẠT: 14/14** (đề cụ thể + mong_doi; tôi tự làm cả 14 bài, chấm ĐÚNG) |
| "N B" bị đọc "chục byte" | Đạt: grep `.srt` không có "chục byte" ("chục" chỉ còn trong "vài chục phần trăm", "hàng chục lần", "hàng chục tỉ byte", "vài chục nghìn byte"); mọi kích thước đọc đầy đủ "triệu byte", "nghìn byte", "tỉ byte"; YAML không còn "N B" dạng viết tắt |
| Hành vi 3.11 vs 3.13 | Nói đúng (đã chạy lại, xem mục 6) |

## 2. Bảng chuẩn xác (chỉ lỗi có bằng chứng)

| Bài | Mức | Cảnh/step | Trích nguyên chữ | Vì sao sai + bằng chứng đã chạy | Đề xuất sửa | Tin cậy |
|---|---|---|---|---|---|---|
| L12 | **MUST** | hook / hook.1 (hiện lại ở khung hình giây 10) | Hàm `phi_chuyen (đúng)`: `phi = tien // 1000; if phi < 1100: return 1100; if phi > 11000: return 11000` rồi hết hàm | Hàm gắn nhãn "(đúng)" **thiếu dòng cuối `return phi`**: với `tien` từ 1 100 000 đến 11 000 000 hàm trả `None`. Bước đã chạy: chép đúng hàm trên màn hình vào `phi.py`, ghép `test_phi.py` từ formula.1 + formula.2 (2 ca + `parametrize` 5 cặp), `python -m pytest -q --tb=short` cho **3 failed, 4 passed**: `assert None == 1100` (tien=1100000), `None == 1101` (1101000), `None == 11000` (11000000). Thêm `return phi` thì **7 passed**; đổi `<` thành `<=` thì đúng "1 failed, 6 passed", `assert 0 == 1100`, khớp màn hình. Cả bài (hook.2, formula.3, formula.5, example, quiz) dựa vào hàm đầy đủ nhưng người học không bao giờ thấy hàm đầy đủ, cũng không thấy `phi.py`/`test_phi.py` trọn tệp | Thêm `return phi` ở cuối hàm trong hook.1; nên có một cảnh hiện trọn `phi.py` và `test_phi.py` | CONFIRMED |
| L12 | SHOULD | pitfalls.2, pitfalls.3 | chỉ hiện đầu ra `1 passed in 0.04s` kèm lời "Hàm vẫn sai (<=) nhưng ca xanh" | Không có mã ca kiểm nào trên màn hình (ca không có `assert`; ca lấy mong đợi từ chính công thức của mã): người học không gõ lại được. example.1 chỉ hiện đầu ra pytest, không hiện `test_float.py`. Tôi tự dựng `test_float.py` thì ra đúng "F." và dòng `test_float.py:5: in test_cong` | Hiện 3–6 dòng mã của từng ca | CONFIRMED |
| L13 | SHOULD | hook (tiêu đề cảnh), tiêu đề cảnh trên `chapters.txt` | "tệp giao dịch đã lớn vạn lần" | Bảng ngay dưới: 1 000 dòng thành 100 000 000 dòng = ×10^5 (một trăm nghìn lần), không phải "vạn" = 10^4. Phép tính 10^8 / 10^3 = 10^5 | Đổi "mười vạn lần" hoặc "một trăm nghìn lần" | CONFIRMED |
| L07 | SHOULD | scale.1 | "50% … bắt lỗi (try) ≈ 3 s", "kiểm tra trước (isdigit) ≈ 600 ms" | Không tái lập: 1 triệu chuỗi, 50% hỏng, tôi đo `try` = 0.52 s (3.11.9) và 0.60 s (3.13.5), biến thể có `replace(".", "")` 0.63 s; `isdigit` 0.18–0.24 s. Tỉ số try/isdigit ≈ 2.5–3.3 lần, màn hình ≈ 5 lần. Ở 0%: `try` 0.24 s, `isdigit` 0.32 s (màn hình 600/800 ms: cùng chiều). Máy tôi ở các bài khác chậm hơn máy kiểm khoảng 2 lần, nên "3 s" càng khó khớp. Kết luận ("đắt khi thường xuyên") vẫn đúng | Đo lại hoặc ghi "cỡ vài lần" | CONFIRMED |
| L09 | SHOULD | practice.1 (khung hình giây 671) | "In **năm khối**: 1. trung bình từng cột; 2. độ lệch chuẩn …; 2. mảng đã chuẩn hoá …; 4. kiểm …; 5. …" | HTML là `<ol>` hai `<li>`: mục thứ ba hiện nhãn tự động "2." (đã xem khung hình), mất số "3." | Tách thành năm `<li>` | CONFIRMED |
| L09 | SHOULD | scale.1 | "nhanh gấp ≈ 200 / ≈ 200 / ≈ 200" ở 10^4, 10^6, 10^7 | Tôi đo (venv-pyt, numpy 2.4.6) vòng lặp/`arr.sum()` = ×59 (10^4), ×177 (10^6), ×122 (10^7). Hệ số không hằng; ở 10^4 chỉ cỡ 60 lần. Bộ nhớ 8.0 MB / 40.0 MB khớp tuyệt đối | Ghi "hàng chục đến hàng trăm lần" | CONFIRMED |
| L08 | SHOULD | example.3, example.4, pitfalls.1 | `$ python -c "import khong_guard"` → `chay thu: 6`; `$ python chay.py 2>&1 | tail -n 1 | cut -c1-58` → `AttributeError: module 'csv' has no attribute 'DictReader'` | Nội dung `khong_guard.py`, `csv.py`, `chay.py` không hiện trên màn hình nên người học không dựng lại được cảnh. Tôi tự dựng (csv.py giả + chay.py `import csv; print(csv.DictReader)`): ra đúng dòng 58 ký tự; sau `mv csv.py csv_cua_toi.py` ra `<class 'csv.DictReader'>` | Hiện 2–3 dòng nội dung từng tệp | CONFIRMED |
| L10 | SHOULD (nhẹ) | scale.2 | "10 000 dòng … ≈ 5 ms / ≈ 3 ms / ≈ 1,7" | Tôi đo nhóm theo loại ở 10^4 dòng: vòng lặp 1.9 ms, `groupby` 2.4 ms (×0.8, `groupby` không nhanh hơn); ở 10^6 ×3.2 khớp "≈ 3,0". Bộ nhớ 1.39 MB / 139 MB, kiểu danh mục 0.25 MB / 19.06 MB (×5.5, ×7.3) khớp tuyệt đối | Bỏ cột tỉ số ở 10^4 hoặc ghi "chưa chắc nhanh hơn" | CONFIRMED |
| L01 | SHOULD (nhẹ) | formula.4 | "gần mười một năm rưỡi" | 139 tháng = 11,58 năm, hơi hơn 11,5 | "hơn mười một năm rưỡi" | CONFIRMED |
| L00, L05 | SHOULD | L00 example.1, L05 formula.4 | "gõ bằng trình soạn thảo, lưu cùng thư mục" | Không bài nào dạy cách tạo/lưu tệp `.py`, cài Python, kiểm `python --version`; chỉ có trong `de.md` (L00 `requires_ext: FND:L04, L05`). Người mất gốc chưa học FND có thể kẹt ở lab L00 | Một cảnh 20 giây ở L00: tạo tệp, đuôi `.py`, UTF-8, chạy | PLAUSIBLE |

Không phát hiện lỗi kiến thức hoặc số liệu ở các bài còn lại (xem mục 6).

## 3. Bảng độ sâu (một dòng mỗi bài)

Phút = `timeline_seconds` của `build_report.json`. P1…P7 theo rubric mẫu F; P8, P9 theo phụ lục. Tổng chỉ P1–P7.

| Bài | sha16 | Phút | P1 | P2 | P3 | P4 | P5 | P6 | P7 | P8 | P9 | Tổng | Mất gốc | Cần biết trước (dùng mà chưa giảng tại chỗ) | Chỗ thiếu chính |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| L00 | a4dea46459b585cd | 18,1 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | trình soạn thảo, tạo tệp `.py`, `python -c` (cờ `-c`), cài Python/PATH | tạo tệp `.py` (example.1) |
| L01 | 091298ab7ee7c0c6 | 18,5 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | không | nit "gần mười một năm rưỡi" |
| L02 | 5ff290ece6d1bc83 | 17,9 | 2 | 2 | 2 | 2 | 2 | 2 | 1 | 2 | 2 | 13 | ĐỦ | không | mục tiêu 9 "so hai cách viết": mã "viết thẳng" không hiện, lab không có bài đo |
| L03 | 43f6cf1cfd7b38d3 | 18,5 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | không (hook dùng "tập hợp", "danh sách" trước sym; nghe tiếp là hiểu) | video STALE |
| L04 | 7b2c73f3efacaa59 | 18,8 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | "byte" chưa định nghĩa trần (dựa FND) | không đáng kể |
| L05 | d2c4325ed379ef30 | 17,6 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | `repr()` (pitfalls.6), `rstrip` (quiz.2) | hai hàm trên |
| L06 | 12dc7eb0386b45b1 | 18,8 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | "con trỏ" (example.9), "cấp phát" (tiêu đề example.10), `__slots__` chỉ nêu tên | hai từ trên |
| L07 | ad5c5f8b818ad5db | 17,7 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | "ngoại lệ" (không định nghĩa trần), "nhả khoá", "luồng điều khiển" | định nghĩa "ngoại lệ"; số 3 s ở scale.1 |
| L08 | aed6466b5cfafeca | 20,8 | 2 | 2 | 2 | 1 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | `grep`, `wc`, `find`, `tail` (dựa FND) | không có tính tay (chỉ thao tác); tệp trong example.3/.4 không hiện; video STALE |
| L09 | 391fbe948f270b1a | 17,8 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | không | số thứ tự ở practice.1; "≈ 200" chung cho mọi quy mô |
| L10 | af0ee8e9b0006ac2 | 19,3 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | "cơ sở dữ liệu" (chỉ nêu hướng) | tỉ số 1,7 ở 10^4 |
| L11 | 0301e0349d7d3b2e | 19,5 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | tên định dạng PNG/SVG (khái niệm vector/điểm ảnh có giảng trong lời đọc) | video STALE |
| L12 | 64f953a71a1487eb | 19,6 | 1 | 2 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 12 | ĐỦ (sát ngưỡng) | `sys.executable`, `capture_output`/`text`, `--tb=short` (ở gợi ý lab) | MUST: hàm thiếu `return phi`; mã ca ở pitfalls.2/.3 không hiện |
| L13 | 7544d7470b3fa8d4 | 23,7 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | ký hiệu "∝" (SVG intuition, recap), "hằng số", "cơ sở dữ liệu" | không có việc người học tự đo ba cách đọc; "vạn lần" |

Ghi chú điểm: L02 P7=1 và L06/L13 giữ 2 vì E51 như sau.

### E51: mục tiêu giáo án "đo thời gian và bộ nhớ" ↔ video

| Bài | Mục tiêu giáo án | Video có dạy trên màn hình? | Người học có việc tự đo? |
|---|---|---|---|
| L02 | "Đo thời gian chạy … bằng `time.perf_counter` và so hai cách viết" | Có mã đo (example.3) và lời "chạy nhiều lần, lấy lần nhanh nhất" (example.4); so sánh gọi hàm / viết thẳng chỉ có số trong bảng scale.2, mã "viết thẳng" không hiện | Không (lab chỉ ba hàm phí) |
| L06 | "Đo bộ nhớ … `sys.getsizeof` và `tracemalloc`, hai cách khác nhau ở đâu" | Đủ: example.9 (28 / 56 / 8056 byte, "không tính những gì ô trỏ tới"), example.10 (`tracemalloc`, 18.5 MB), example.11 | Không (lab = lớp `TaiKhoan`) |
| L13 | "Đo thời gian và bộ nhớ của ba cách đọc ở hai quy mô" | Đủ: formula.1 mã đo, formula.2/.3 bảng 10^3 và 10^6 | Không (lab = dự án nhỏ tự chấm) |

Khuyến nghị: thêm một bài tập đo nhỏ ở lab L02/L06 (mong đợi dạng "cùng bậc độ lớn"), vì hiện mục tiêu được dạy nhưng chưa được thực hành.

## 4. Lab: tự làm như người học (không xem `loi_giai.*` trước)

Tự viết lời giải ở scratchpad, chấm `bash labs/cham.sh PYT <Lxx> <tệp>`. Thời gian = ước lượng cho người đã học FND (không tính chờ pip). Sau đó chấm `loi_giai.py` của cả 14 bài: 14/14 ĐÚNG.

| Bài | Tự làm được | Thời gian | Kẹt ở đâu | `mong_doi` khớp màn hình |
|---|---|---|---|---|
| L00 | Có | 5 phút | không (`type(lai).__name__` có gợi ý, cần biết cách tạo tệp) | Khớp; 3.11 và 3.13 đều ĐÚNG |
| L01 | Có | 5 | không | Khớp; 3.11 + 3.13 |
| L02 | Có | 5 | không | Khớp; 3.11 + 3.13 |
| L03 | Có | 6 | không (`dict.get`, `sorted(key=lambda)` đã giảng) | Khớp; 3.11 + 3.13 |
| L04 | Có | 6 | không (hai mẫu `re` đã gợi ý) | Khớp; 3.11 + 3.13 |
| L05 | Có | 8 | không (`newline=""`, `sort_keys` có gợi ý) | Khớp; 3.11 + 3.13 |
| L06 | Có | 8 | không | Khớp; 3.11 + 3.13 |
| L07 | Có | 7 | không (`repr` có gợi ý ở practice.3) | Khớp; 3.11 + 3.13 |
| L08 | Có (cài thật) | 10 + chờ pip | Tạo `.venv-hoc` rồi `pip install -r labs/requirements-py.txt` thật trên mạng: `rc=0`, `pip freeze` ra đúng 17 dòng trùng `requirements-py.txt` (khác CRLF); trong venv đã kích hoạt `python in_phien_ban.py` rồi `cham.sh` ĐÚNG | Khớp |
| L09 | Có | 8 | không (cần venv; `np.allclose` có giải thích) | Khớp (venv-pyt) |
| L10 | Có | 10 | không (`idxmax`, `int(...)` có gợi ý) | Khớp (venv-pyt) |
| L11 | Có | 10 | không (đọc `ax.patches`, `get_ylim` có gợi ý) | Khớp (venv-pyt) |
| L12 | Có | 15 | `subprocess.run([sys.executable, …], capture_output=True, text=True)` chép được từ gợi ý nhưng không giảng; `cham.sh` mỗi lần ~25 s vì pytest khởi động chậm trên Windows | Khớp (venv-pyt) |
| L13 | Có | 20 | Lần đầu tôi vấp đúng bẫy `\n` trong chuỗi ba nháy thường (ghi `\n` thật vào tệp thì pytest lỗi thu thập, "Ba ca kiem qua: CHUA", 8/10); `de.md` và practice.3 có cảnh báo `\\n`/`r'''`; sửa là ra 10/10 | Khớp (venv-pyt) |

Python 3.13: chạy L00–L07 pass (mã thuần); L08–L13 cần thư viện ngoài, `.venv` không có pandas nên không chạy 3.13.

## 5. Người học kẹt ở đâu (chỉ xem video + các bài đứng trước)

| Bài | Chỗ đầu tiên không theo được |
|---|---|
| L00 | example.1 "Tệp lai.py (gõ bằng trình soạn thảo, lưu cùng thư mục)": chưa biết tạo/lưu tệp `.py` (dựa FND) |
| L01 | không kẹt |
| L02 | không kẹt |
| L03 | không kẹt |
| L04 | intuition.1 "bộ nhớ lưu byte": byte chưa được định nghĩa trần (dựa FND) |
| L05 | pitfalls.6 `print(repr(open("kq.txt", encoding="utf-8").read()))`: `repr` chưa giảng, thấy `''` mà không hiểu vì sao có nháy |
| L06 | example.9 "mỗi ô chỉ là một con trỏ 8 byte": "con trỏ" chưa giảng |
| L07 | intuition.1 "Hàm chia ném một ngoại lệ": "ngoại lệ" chưa định nghĩa trần (đang dùng thay "lỗi") |
| L08 | example.3 `$ python -c "import khong_guard"` → `chay thu: 6`: tệp `khong_guard.py` không hiện, số 6 từ đâu |
| L09 | không kẹt (practice.1 đánh số sai "2." hai lần) |
| L10 | không kẹt |
| L11 | không kẹt |
| L12 | hook.1: chép hàm `phi_chuyen` "(đúng)" thì chạy ra None; formula.3 `7 passed` không tái lập được; pitfalls.2/.3 không có mã |
| L13 | intuition.1 "bộ nhớ ∝ số dòng": ký hiệu ∝ chưa giảng (lời đọc nói "tỉ lệ với") |

## 6. Số đã tính lại / mã đã chạy

- Khối mã/REPL gõ lại từ màn hình, chạy bằng harness tự viết (`InteractiveConsole` cho khối `>>>`, chạy tệp cho khối mã, so từng dòng; traceback chỉ so loại lỗi): L00 68/68, L01 44/44, L02 33/33, L03 48/48, L04 49/49, L05 25/25, L06 42/42, L07 28/28, L09 53/53, L10 32/32, L11 20/20, L13 14/14 khớp; tổng 456 khối tự động khớp, 0 lệch thật. Các khối đầu ra của lab, các cảnh dùng nhiều tệp (L08, L12, một phần L05, L10, L13) và 3 khối "lệch" đầu tiên của L08 là do harness thiếu tệp, đã dựng tay lại từng cảnh: L08 `giao_dich.py`/`chay.py`/`ngan_hang/phi.py`/`csv.py`, L10 `gd.csv`+`tk.csv` (`merge`, `groupby`), L12 `phi.py`/`test_phi.py`/`test_float.py`, L04 example, L05 shell (`PYTHONIOENCODING=cp1252` → rc 1, `UnicodeEncodeError`): đều khớp, trừ MUST L12 ở mục 2.
- Python 3.13.5: L00–L07 chạy lại toàn bộ khối: 0 lệch. Khác biệt 3.11/3.13 mà bài nói: dòng mã và `~^` trong traceback (L00, L04, L07, L08: đúng); `breakpoint()` dừng ở dòng kế (3.11) so với dòng đó (3.13): **đã chạy, đúng** (L07 sym.2); thông báo `AttributeError` dài thêm gợi ý đổi tên tệp (3.13): **đúng** (L08, cắt đúng 58 ký tự).
- Số đo (máy tôi chậm hơn máy kiểm khoảng 2 lần ở vòng lặp thuần; so bậc độ lớn và thứ tự): L01 vòng cộng 10^6/10^7 = 0.29/3.3 s (màn hình 0.14/1.5 s); L02 hàm vs viết thẳng ×1.9–2.1 (màn hình ×1.7); L03 danh sách 1e6 tìm không thấy 8.1 ms vs tập hợp 68 ns, bộ nhớ 40.0 / 65.5 MB (khớp 40 / 66); L04 `(a+)+b` 17/21/25 ký tự = 8 ms/0.19 s/3.0 s (màn hình 3 ms/50 ms/1 s), `a+b` 4000→8000 ký tự 17→89 ms (gấp 5, khớp "gấp nhiều lần"); L05 bộ nhớ đọc cả tệp 96.5 MB (110), từng dòng 26.0 KB (26 KB, khớp tuyệt đối), 10^4 dòng 1.0 MB (1,1), thời gian hai cách 0.47 vs 0.46 s (khớp "cùng cỡ"); L06 `__dict__` lớp thường 18.5/185 MB, `__slots__` 14.5/145, bộ ba 16.1/161 (màn hình 19/190, 15/150, 16/160), 3.13 thấp hơn ~4%; `getsizeof` 28/56/8056 khớp; L08 import riêng từng thư viện (venv-pyt, tốt nhất 3 lần) sys 0.09 s, numpy 1.04 s, pandas 3.25 s, matplotlib.pyplot 5.06 s, pytest 2.24 s (màn hình 0.2/0.9/3/2/2 s); `requirements-py.txt` 17 dòng = 4 thư viện + 13 phụ thuộc; L09 mảng 8.0 MB / danh sách 40.0 MB khớp tuyệt đối, tốc độ xem mục 2; L10 bộ nhớ khớp tuyệt đối; L11 scatter+PNG 1e3/1e5/1e6 = 0.09/0.28/2.3 s (màn hình 90 ms/200 ms/1 s), SVG 0.12/10.8 MB (khớp 120 KB / 11 MB), hexbin 0.06–0.20 s (khớp 100–200 ms); L12 pytest 100/1000/10000 ca = 0.10/0.99/27 s (màn hình 0.8/2/10 s, cùng bậc); L13 bộ nhớ A/B/C ở 10^3 = 99.2/43.5/296.9 KB và ở 10^6 = 95.5 MB/43.5 KB/9.3 MB (khớp 98/42/300 KB và 94 MB/43 KB/9,3 MB), thứ tự thời gian C < A < B khớp (máy tôi chậm 5–10 lần ở B).
- Số học ngoại suy kiểm lại: L00 `0.1+0.2`, `12000000*0.072 = 863999.9999999999`, `10**15+0.1-10**15 = 0.125`, `2**53+1`; L01 139 tháng; L02 18,3% và 86,7% (`1-0.98**10`, `1-0.98**100`); L05 24 ký tự / 31 byte, 33 byte trên Windows; L11 chuỗi 90,0/33,3/39,0 so 88,9/20,0/82,0 và tần suất [5,5,0,0,1]; L13 5 400 000 = 1 450 000 + 3 400 000 + 550 000, trung vị 3 so 3,5, 10^5 so "vạn": đúng, trừ "vạn lần" ở L13.
- Giáo án ↔ video (P7): 14/14 bài có đủ cảnh cho từng mục tiêu theo `covers`; không bài nào hứa điều không dạy; điểm lệch duy nhất là thực hành đo (E51, mục 3).
- spec_sha256: xem đầu báo cáo.

## 7. Khung hình đã xem

Mỗi bài 8 khung hình (hook, intuition, formula, example hoặc scale, pitfalls, quiz, practice hoặc recap), ghép 2×2 mỗi ảnh (hai ảnh mỗi bài), tổng 112 khung. Thời điểm = chương + 10 giây, tính từ `_frames.txt` và `chapters.txt`.

- L00: 00001, 00035, 00054, 00093, 00105, 00119, 00132, 00148. L01: 00001, 00040, 00078, 00092, 00104, 00118, 00133, 00145. L02: 00001, 00029, 00039, 00059, 00082, 00096, 00110, 00125. L03: 00001, 00030, 00040, 00067, 00085, 00096, 00108, 00121. L04: 00001, 00041, 00052, 00077, 00096, 00104, 00115, 00143. L05: 00001, 00027, 00037, 00058, 00078, 00089, 00106, 00119. L06: 00001, 00029, 00038, 00055, 00087, 00096, 00112, 00139. L07: 00001, 00027, 00032, 00055, 00082, 00090, 00101, 00114. L08: 00002, 00028, 00038, 00068, 00091, 00105, 00116, 00129. L09: 00001, 00027, 00037, 00057, 00079, 00091, 00104, 00118. L10: 00001, 00030, 00039, 00067, 00084, 00096, 00107, 00120. L11: 00001, 00032, 00039, 00062, 00083, 00099, 00109, 00123. L12: 00001, 00025, 00039, 00061, 00079, 00090, 00100, 00114. L13: 00001, 00026, 00030, 00050, 00070, 00085, 00098, 00111.
- Lỗi hiển thị: không thấy chữ tràn, đè, bị cắt; cỡ chữ đọc được; hình khớp lời đọc ở mọi khung. Lỗi duy nhất: L09 practice.1 đánh số "2." hai lần (khung 00118). Nhận xét bố cục: nửa dưới khung thường để trống (code ngắn), không phải lỗi. L12 khung 00001 cho thấy hàm `phi_chuyen` kết thúc ở `return 11000` (nguồn của MUST). L03, L08, L11 là khung hình video cũ.

## 8. Nhận xét chung

- Nội dung kiến thức của khoá chính xác và nhất quán: 456 khối mã tự chạy khớp, mọi số đo tái lập được đúng bậc độ lớn, bộ nhớ khớp gần như tuyệt đối ở L03, L05, L06, L09, L10, L13; hành vi 3.11/3.13 nói đúng (đã chạy `breakpoint()` và thông báo `AttributeError`).
- Chỉ còn một lỗi chặn: hàm `phi_chuyen` thiếu `return phi` ở hook L12; sửa một dòng và nên hiện trọn `phi.py`, `test_phi.py`.
- P1 chưa đạt 90%: 6 bài còn 1–2 từ chưa giảng tại chỗ (L00 tạo tệp `.py`; L05 `repr`, `rstrip`; L06 "con trỏ", "cấp phát"; L07 "ngoại lệ"; L12 `sys.executable`, `capture_output`; L13 "∝", "hằng số"); mỗi chỗ sửa bằng một câu.
- P8 đạt 100%: lab cụ thể có `mong_doi`, `cham.sh` hoạt động, L08 cài thật qua mạng thành công (17 gói trùng danh sách ghim); L13 có bẫy `\n` được đề bài cảnh báo trước.
- P9 = 2 ở cả 14 bài (số liệu ở 2–3 quy mô + ngoại suy + đánh đổi); E51: đo thời gian/bộ nhớ được dạy bằng mã trên màn hình ở L02/L06/L13, thiếu bài tập đo cho người học.
- Ba video STALE (L03, L08, L11) đang dựng lại: sau khi dựng nên chạy lại `spec_sha256` và so `.srt`; YAML hiện tại của ba bài không có lỗi MUST.
- Các lỗi SHOULD là số đo minh hoạ lệch (L07 "3 s", L09 "≈ 200", L10 "1,7"), cảnh dựng thiếu mã tệp phụ (L08, L12), tiêu đề "vạn lần" (L13), đánh số (L09).
- Độ dài 17,6–23,7 phút mỗi bài (L13 dài nhất, L08 20,8): vừa phải cho người học mất gốc nếu dừng video làm lab.
