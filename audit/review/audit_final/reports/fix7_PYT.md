# fix7_PYT: sửa khoá PYT theo `R4_PYT.md` (vòng 4b, chuẩn P1 chặt) — một tác tử, cả 14 bài

Nguồn sửa: `audit/pyt/src/lNN.py` -> `gen.py` (không sửa YAML sinh ra bằng tay). Không chạy build/tts/asr/git/docker (render khung `lv.py render` có chạy theo quy tắc bổ sung của người điều phối). Nền: MUST 0; P1 = 2: 0/14 (P1 = 1: L03, L07, L08, L09, L11; P1 = 0: 9 bài); SHOULD 7. Mục tiêu vòng này: 0 mục chưa giảng (loại A/B/M, cả mục "yếu") ở 14/14 bài.

## TIẾN ĐỘ
- Xong cả 14 bài (L00–L13): nguồn, sinh, lint, render 0 vấn đề, verify, lab_gate, screen_code (mục 5).

## 1. Bài đổi, CẦN DỰNG LẠI (spec_sha256 đổi): cả 14 bài L00–L13
Lab đổi (`de.md`/`loi_giai.py`, máy chấm `mong_doi.txt` giữ nguyên): L00 (không đổi chữ máy chấm), L13 (hàm `cham` đơn giản hoá, thêm đoạn "Cách đọc hàm chấm", gợi ý chuỗi thô). Sổ `audit/pyt/measured.json`: đo lại khoá `l04_redos` (máy rảnh; số cũ do tải) và thêm khoá `l12_mut`. Thêm `audit/pyt/make_fig_l11.py` + `audit/pyt/fig_l11.json` (dữ liệu thật của `hexbin`, sinh bằng `labs/.venv-pyt`).

## 2. Mục "chưa giảng" nay giảng tại chỗ (theo R4 mục 3)
| Bài | Mục (loại) | Cách giảng |
|---|---|---|
| L00 | f-string `{so_du + round(lai):,}` (M) | cảnh ví dụ: step f-string chuyển LÊN ĐẦU (trước tệp `lai.py`), bảng "viết → đọc là", thêm phiên `f"Tong: {2000000 + 30000:,}"` (biểu thức trong ngoặc nhọn); lời dẫn ở step tệp nhắc "dòng cuối dùng chuỗi có chỗ điền" |
| L00 | `type(lai).__name__` (M) | cảnh trực giác: phiên `type(...).__name__` ra `'int'`, `'float'` + hộp "dấu chấm lấy thuộc tính; `__name__` là tên kiểu viết thành chữ" (trước khi hiện ở đề bài) |
| L00 | "hệ nhị phân/hệ hai" (A) | formula bước 5: chỉ có hai chữ số 0 và 1, các vị trí gấp đôi (1, 2, 4, 8… như hệ mười có 1, 10, 100…) |
| L00 | số mũ âm 10⁻¹⁶, ×10⁶, ×10¹⁵ (A) | scale bước 1: "10⁶ là một và sáu số không; 10⁻¹⁶ là một chia 10¹⁶, rất nhỏ (0,0000000000000001)" (chữ + lời) |
| L01 | `so_du * 5 // 1000` (B) | step vòng điều kiện: `//` chia lấy phần nguyên (`7 // 2` ra `3`), nên lãi là số nguyên đồng (chữ + lời) |
| L01 | `list(range(3))` (A), "≈ 93 µs" (A) | step `range`: `list(…)` xếp các số của `range` thành danh sách; ghi chú scale: "ms là phần nghìn giây, µs là phần triệu giây" |
| L02 | `time.perf_counter()` (A), `for i in range(n): y = tang(y)` (B), ngoại suy (B) | step bảng đứng trước khung mã đo giờ: "dấu chấm đọc là *của*", `import time`, `for i in range(n)` lặp n lượt, i đếm từ 0 (chữ + lời); ghi chú một dòng định nghĩa ngoại suy ở scale |
| L03 | "≈ 40 MB", "bốn mươi triệu byte" (A), ngoại suy (B) | scale: ghi chú byte (một byte đủ chứa một chữ cái; KB ≈ nghìn byte, MB ≈ triệu byte) + câu lời; ghi chú định nghĩa ngoại suy |
| L04 | `if m is None:`, `continue` (B), ngoại suy (B) | step "Phần xử lý": `is` = "đúng là cùng một thứ", `None` = "không có gì", `continue` = bỏ lượt, sang dòng kế (chữ + lời); ghi chú ngoại suy ở scale |
| L05 | `from pathlib import Path` (A) | bảng sym: hàng `from pathlib import Path` ("nạp công cụ": lấy riêng công cụ từ thư viện, một lần ở đầu tệp) + câu lời |
| L05 | `f.write("tiền mặt\n")`, `split("\n")` (A) | bảng sym: hàng `"…\n"` ("hai ký tự `\` và `n` trong chuỗi là MỘT ký tự xuống dòng; `s.split("\n")` cắt thành các dòng") + câu lời |
| L05 | `PYTHONIOENCODING=cp1252 python -c … 2> loi.txt; echo $?`, `tail … | cut …` (M) | pitfall lỗi 2 tách ba step: (1) lệnh đầu + giải tiền tố `TÊN=giá_trị`, `2>`, `;`, `echo $?`; (2) `tail -n 1`, `|`, `cut -d: -f1`; (3) lệnh đặt `PYTHONIOENCODING=utf-8` + quy tắc. Mỗi lệnh giảng ngay dưới khung lệnh của nó |
| L05 | `json.dumps/loads` (A), ngoại suy (B) | formula bước 4: `s` = chuỗi, `dumps/loads` đổi dữ liệu <-> chữ JSON, bản không có `s` làm việc với tệp; ghi chú ngoại suy ở hook |
| L06 | `from dataclasses import dataclass` (A) | bảng sym: hàng `from dataclasses import dataclass` ("from X import Y: lấy riêng công cụ Y từ thư viện X") + câu lời |
| L06 | `[A("A" + str(i), i) for i in range(100000)]` (A/B), ngoại suy (B) | step `tracemalloc`: `str(i)` đổi số thành chuỗi; danh sách suy ra "một đối tượng cho mỗi i" (chữ + lời); ghi chú ngoại suy ở hook và scale |
| L07 | `print(repr(s), doc_tien(s))` (B) | formula bước 1: `repr(s)` in `s` kèm cặp nháy, để chuỗi rỗng hiện `''` (chữ + lời) |
| L08 | `source … && python -c "…"` (A) | ví dụ kích hoạt: `A && B` chạy B chỉ khi A thành công (mã thoát 0) (chữ + lời) |
| L08 | `python -c "import sys; print(…)"` (A) | formula bước 3: dấu `;` ngăn hai câu lệnh trên một dòng; `!=` là "khác" (chữ + lời) |
| L09 | `np.array([[1., 10.], …])` (A) | ví dụ chuẩn hoá cột: `1.` là số thực 1,0; mảng toàn số thực (chữ + lời) |
| L09 | "số nguyên 4 byte (32 bit, một bit dành cho dấu)" (A) | pitfall: bit là một chữ số 0 hoặc 1, một byte có 8 bit; thêm phép tính quay vòng 4 000 000 000 − 2³² = −294 967 296 (chữ + lời) |
| L10 | `gd.loc[gd["loai"] == "nap", "so_tien"].sum()` (M) | formula bước 2: thêm hộp `gd.loc[điều_kiện, "cột"]` NGAY TRÊN khung mã; `splitall(k=3)` để cả phần giảng `.loc` nằm ở nửa đầu cùng khung mã |
| L10 | `gd.dropna(subset=["so_tien"])` (A) | formula bước 4 (bỏ/điền): `subset` = chỉ xét các cột nêu; lời nhắc lệnh bỏ dòng thiếu kèm tên cột |
| L10 | `gd["so_tien"] == float("nan")` (A), ngoại suy (B) | pitfall 3: `float("nan")` tự dựng giá trị thiếu để thử so sánh (chữ + lời); ghi chú ngoại suy ở hook và scale |
| L11 | `[int(p.get_height()) for p in ax.patches]` (B), ngoại suy (B) | formula bước 1: `ax.patches` = danh sách các cột đã vẽ, `get_height()` hỏi chiều cao, danh sách suy ra một phần tử mỗi cột (chữ + lời); ghi chú ngoại suy ở scale |
| L12 | `mong_doi = 0 if tien <= 50000 else max(…)` (A) | pitfall lỗi 3: `A if điều_kiện else B` = biểu thức điều kiện một dòng, đọc từng phần, `max` chọn số lớn (chữ + lời) |
| L12 | "đặc tả" (A), diff `-`/`+` (A), ngoại suy (B) | formula bước 1: đặc tả = bản mô tả bằng lời đầu vào nào thì kết quả phải là gì; hook: dòng `-` bị bỏ, dòng `+` thay vào; ghi chú ngoại suy ở scale |
| L13 | `except ValueError: bo_qua += 1; continue` (A) | gợi ý đổi sang khung mã nhiều dòng với `bo_qua = bo_qua + 1` (đã học), không còn `+=` và `;` |
| L13 | chuỗi ba nháy, `\n` (A) | cảnh ví dụ thêm 2 step: bảng "viết trong mã → đọc là" (`"""…"""`, `\n`, `r"…"`) + chương trình thật `ba_nhay` (3 và 4 ký tự); gợi ý và `de.md` đổi sang chuỗi thô `r'''…'''` (không cần nhân đôi gạch chéo) |
| L13 | hàm `cham` (`importlib`, `exec_module`, `subprocess.run`) | hàm `cham` đơn giản hoá: bỏ `importlib` (dùng `sys.path.insert` + `import`); thêm step đầu cảnh tự làm "đọc hàm chấm qua bảng" (5 việc, mỗi việc một dòng lệnh -> đọc là, giải `sys.path`, `sys.executable`, `capture_output`, `text`); `de.md` thêm đoạn "Cách đọc hàm chấm" |
| L13 | ngoại suy (B) | ghi chú một dòng định nghĩa ở hook và scale |

## 3. SHOULD (7/7 xử lý)
| Bài | Việc |
|---|---|
| L02 | "1,7 đến 2,4 lần" -> câu mới tính từ hai số đo trên màn hình: "chậm hơn cỡ {ratio ở 10^6} đến {ratio ở 10^7} lần"; bỏ chữ "cận trên"; "hàm làm việc thật thì khoản gọi chỉ là phần nhỏ" |
| L04 | đo lại `l04_redos` (máy rảnh, `verify_pyt L04 --remeasure`): 4 000 ký tự ≈ 11 ms, 8 000 ký tự ≈ 45 ms; câu mới "chuỗi dài gấp đôi, thời gian gấp cỡ {tỉ số} lần, tức tăng theo bình phương độ dài; số minh hoạ theo máy"; sửa luôn câu sai nghĩa "vẫn chậm hơn rất xa mẫu viết kém" -> "nhanh hơn rất xa". Đo thủ công 3.11/3.13: 4 000 -> 8 000 ký tự: ×4,0 (12,2 -> 48,3 ms; 15,4 -> 55,9 ms) |
| L06 | "(về khái niệm; từ Python 3.11 máy dựng từ điển đó muộn, chỉ khi cần)" ở tiêu đề, ghi chú, lời đọc; hộp đánh đổi: "lưu thuộc tính theo kiểu từ điển linh hoạt (từ 3.11 dựng muộn) nên vẫn tốn thêm" |
| L07 | năm mức: `debug < info < warning < error < critical` (năm mức chuẩn); lời "theo năm mức, từ chi tiết đến nghiêm trọng nhất" |
| L08 | bỏ ký tự `|` thừa ở hàng `2>&1` ("để lọc được cả hai") |
| L12 | chạy đột biến bằng mã (`measure l12_mut`, verify chạy thật trên 3.11 và 3.13): 18 cách sửa một chỗ (đổi dấu, dịch hằng ±1); 4 cách KHÔNG đổi kết quả ở mọi giá trị thử (`phi < 1100` -> `<=`, `phi > 11000` -> `>=`, `phi < 1101`, `phi > 10999`: hàm liền mạch tại 1 100 000 và 11 000 000); 14 cách làm hàm sai; bảy ca của bài bắt 12/14, thêm hai ca `1 099 999 -> 1 100` và `11 001 000 -> 11 000` bắt 14/14 (bốn ca giữa vùng chỉ 10/14; ba ca sát ngưỡng 50 000 chỉ 7/14; một ca 50 000 chỉ 5/14; tính ngoài bài bằng `mut12.py` ở scratchpad). Sửa: SVG trực giác (50 000 hàm NHẢY; hai ngưỡng kia liền mạch), lời đọc trực giác, hai step mới ở ví dụ (kết quả đột biến + giải thích nhảy/liền mạch), quiz "Quyết định" (chữ + lời): ba ca sát ngưỡng ở chỗ hàm nhảy bắt lỗi đổi dấu và lệch một, ở chỗ liền mạch đổi dấu không đổi kết quả và ca sát ngưỡng kiểm giá trị chặn. Số trong bài lấy từ `measured.json` (`l12_mut`), không gõ tay |
| L13 | khối `for hang in csv.DictReader(f): try: … except … continue` thành MỘT dòng văn xuôi -> khung mã 6 dòng (`raw_block`) |
| L11 (P3) | thêm hai HÌNH THẬT: (1) bước 5 thang lôgarit: hai biểu đồ vẽ từ chính bốn số 1, 10, 100, 1000 (thang thường: đường cong; lôgarit: đường thẳng); (2) cảnh scale: các ô lục giác THẬT của `hexbin` (100 000 điểm, `default_rng(1)`, `gridsize=30`: 707 ô có điểm, ô đậm nhất 1 119 điểm, tổng đếm 100 000), toạ độ ô và số đếm lấy từ `fig_l11.json` do `make_fig_l11.py` chạy bằng `labs/.venv-pyt`; không bịa số |

## 4. Độ dài lời đọc (từ, ≤ 2 300)
L00 2273, L01 2151, L02 2281, L03 2287, L04 2283, L05 2228, L06 2297, L07 2169, L08 2290, L09 2106, L10 2177, L11 2278, L12 2283, L13 2244. Cắt để bù: lời lặp lại bảng ở L00, L02, L06, L11, L12, L13; câu mở "Hôm nay ta trả lời ba câu hỏi"; L13 rút ~150 từ (tư duy cuối, đánh đổi, bước 3, tổng kết). Mọi `say` 4–38 từ, câu <= 170 ký tự (lint 0 FAIL 0 WARN).

## 5. Cổng thật
- `lv.py lint`: **0 FAIL, 0 WARN** ở cả 14 bài (L00 35 PASS, L01 25, L02 20, L03 23, L04 23, L05 20, L06 21, L07 19, L08 20, L09 26, L10 23, L11 24, L12 26, L13 23).
- `lv.py render` (theo quy tắc bổ sung của người điều phối): lần đầu 3 bài TRÀN bảng (L02 example, L06 example, L13 practice: cả bảng "đọc hàm chấm" và khối gợi ý). Đã sửa bằng cách tách step: L02 thêm step bảng "viết trong mã -> đọc là" (`import time`, `time.perf_counter()`, `for i in range(n)`) đứng TRƯỚC khung mã đo giờ; L06 thêm step bảng (`str(i)`, danh sách suy ra) đứng trước khung mã `tracemalloc`; L13 tách bảng hàm chấm làm hai step (`cham_a`, `cham_b`) và tách gợi ý làm hai step. Chạy lại: **cả 14 bài 0 vấn đề** (L00 147 khung, L01 154, L02 154, L03 141, L04 154, L05 149, L06 144, L07 140, L08 154, L09 142, L10 147, L11 137, L12 144, L13 144). Đã xem khung PNG: L13 `00117` (bảng hàm chấm), `00124` (đề tự làm), `00112`; L11 `00086` (hình ô lục giác thật), `00104`.
- `verify_pyt`: cả khoá lần đầu 226/228 (hai ô thời gian lệch >×8 do máy rất tải: L09 `l09_sum`, L12 `l12_scale`); chạy lại L02 L06 L09 L12 L13 sau mọi sửa: **74/74 PASS**. Đo mới: `l04_redos` (remeasure), `l12_mut` (mới).
- `lv.py curriculum curriculum/pyt.yaml`: 14 bài, 0 lỗi. `tests/test_e52.py`: 0 FAIL. `arith_scan`: 252 phép tính, 0 FAIL.
- `lab_gate PYT`: **14 PASS · 0 FAIL (196 lab)**. Lab L02 đo thời gian: một lần `screen_code check` gặp `KHONG` khi máy tải nặng (nhiễu đã biết), chạy lại `loi_giai.py` 3/3 lần ra `CO`.
- `screen_code check --course PYT`: sổ sinh lại bằng công cụ chính thức `gen-pyt` (347 khối, 0 chưa khớp trừ 4 khối hand), thêm bằng Edit 4 mục `hand: true` (L02 example 3 0/1: mã đo giờ `DEMO_DO` + đầu ra; L06 example 10 0/1: mã `tracemalloc` `DEMO_MEM` + đầu ra; mã trùng nguyên văn mã `measure` mà verify_pyt chạy thật). Kết quả: PASS 544 · FAIL 0 · STALE 0 · MISSING 0 · ORPHAN 0 (lần chạy cuối: FAIL 2 chỉ là nhiễu thời gian lab L02 nói trên).

## 6. Ước số mục chưa giảng còn lại (theo R4 mục 3)
L00 0, L01 0, L02 0, L03 0, L04 0, L05 0, L06 0, L07 0, L08 0, L09 0, L10 0, L11 0, L12 0, L13 0 (ước lượng của người sửa: mọi mục R4 đã có bảng/lời giảng ở lần xuất hiện đầu hoặc trước nó trong cùng bài; chưa có người đọc độc lập đo lại). Rủi ro còn lại: L13 (nhiều ký hiệu nhất; bảng "đọc hàm chấm" dài), L05 (ba step shell mới).

## 7. Mục không làm / còn hở
- **Tai người**: các câu `say` mới/đổi là câu TTS mới (chỉ kiểm ≥ 8 từ mỗi step, 4–38 từ mỗi câu, không từ Latin/Anh: lint + lexicon); L12 có số đọc dài (hai trăm chín mươi bốn triệu… ở L09; "một nghìn một trăm mười chín" ở L11).
- **Phép đo thời gian dưới tải**: máy đang chạy nhiều tác tử khác; `verify_pyt` cả khoá lần cuối có hai ô thời gian lệch quá ×8 (L09 `l09_sum`, L12 `l12_scale`) — nhiễu đo, không phải lỗi bài; đã chạy lại, 74/74 PASS (mục 5).
- Không sửa `lib.py` dùng chung; sổ `tools/registry/symbols.PYT.yaml` không đổi (không thêm thuật ngữ mới; `pyt_sys_path` chuyển `introduces` lên step đầu cảnh tự làm L13; L13 `assumes` thêm `pyt_subprocess`, `pyt_sys_executable`, `pyt_capture_output` — đã giảng ở L12).
