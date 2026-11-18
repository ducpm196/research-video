# fix2_S01_PYT: sửa khoá PYT vòng 2 theo `S01b_PYT.md` (một tác tử, cả khoá)

Nguồn sửa: `audit/pyt/src/lNN.py` (YAML sinh bằng `gen.py`), công cụ `audit/pyt/lib.py`, `audit/pyt/screen_check.py`, `audit/pyt/verify_pyt.py`, sổ `tools/registry/symbols.PYT.yaml`, số đo `audit/pyt/measured.json`. Không chạy build/tts/asr/audit_all/git/docker.

## 1. Bài đã đổi
Nội dung: **L00, L01, L02, L05, L06, L07, L08, L09, L10, L12, L13** (11 bài).
Chỉ đổi cảnh chấm lab (dòng "Lưu tệp ở thư mục gốc của bộ khoá…" ở step đề, dòng "Chấm (chạy từ thư mục gốc…)" ở `de.md`, không đổi lời đọc): **L03, L04, L11** (YAML sinh lại nên `spec_sha256` đổi, video phải dựng lại).

## 2. MUST (1) và SHOULD đã sửa
| Mục | Cách sửa | Kiểm |
|---|---|---|
| **MUST L12 hook.1** hàm "(đúng)" thiếu `return phi` | hook hiện `phi.py` trọn 9 dòng (có `return phi`); formula.2 hiện đủ `def test_bien` + `assert` (trước chỉ hiện decorator, thiếu thân hàm); `test_phi.py` hiện trọn tệp trong hai step liền nhau (nửa trên dòng 1–10, nửa dưới dòng 13–18, lời đọc dặn nối liền, lưu cạnh `phi.py`) | `screen_check.check_show_files` dựng lại `phi.py` và `test_phi.py` TỪ KHỐI TRÊN MÀN HÌNH rồi chạy pytest thật: `chay_ok` ra `7 passed`; `chay_loi` (áp đúng cặp thay `<`→`<=` hiện ở khối diff) ra `1 failed, 6 passed`, `assert 0 == 1100` |
| L12 pitfalls.2/.3, example.1 không có mã ca kiểm | hiện `test_rong.py`, `test_chep.py`, `test_float.py` trọn tệp (step mã riêng, step kết quả riêng, để khỏi tràn) | cùng cổng: dựng lại từ màn hình, chạy ra đúng đầu ra hiện |
| L13 "đã lớn vạn lần" | tiêu đề "đã lớn một trăm nghìn lần" (10^3 → 10^8 = ×10^5) | lint/render |
| L07 scale.1 "try ≈ 3 s" | đo lại (`--remeasure`), phép đo L07 đổi thành lấy lần nhanh nhất trong 5 lần mỗi ô; bảng và lời đọc dùng số mới; thêm "bắt lỗi chậm hơn kiểm tra trước cỡ vài lần, tỉ số đổi theo máy" | số mới ở `measured.json`; tỉ số đo được trên máy kiểm hiện ≈ 5 lần ở 50% (máy người đọc ≈ 3 lần), lời nói "cỡ vài lần" đúng cho cả hai |
| L09 "≈ 200" ở cả ba quy mô; practice.1 đánh số "2." hai lần | đo lại (nay ≈ 200, 300, 200 trên máy kiểm vì mỗi quy mô một số); tiêu đề hook, ô "Quyết định", recap, ghi chú bảng nói "hàng chục đến hàng trăm lần" và "khác giữa các quy mô và các máy"; practice.1 tách đủ **năm** `<li>` | lint/render (khung 118 cũ hết lỗi số) |
| L10 scale.2 tỉ số 1,7 ở 10^4 dòng | bỏ tỉ số ở 10^4, ô ghi "cùng cỡ; chưa chắc nhanh hơn", lời đọc: "hai cách cùng cỡ thời gian, có máy lệnh trên bảng còn chậm hơn, vì có chi phí cố định"; giữ tỉ số ở 10^6 (đo ≈ 3) | số đo lại ở `measured.json` |
| L08 `khong_guard.py`, `csv.py`, `chay.py` không hiện | step mới hiện nội dung từng tệp trước lệnh chạy (example.3 và example.4 tách hai step để khỏi tràn); khai `show_files` cho hai phiên `sh` | cổng `screen-files` PASS: tệp hiện trọn vẹn và đúng nội dung phiên đã chạy |
| L00, L05 không dạy tạo tệp `.py`/cài Python | L00: prereq giảng `python -c` (cờ `-c`), cài từ python.org + tích PATH + `python --version`; example.1 dạy "trình soạn thảo chữ thuần, lưu `lai.py` (đuôi `.py`) vào thư mục cửa sổ lệnh đang đứng"; `de.md` L00 dạy cài + cách tạo tệp + mở Git Bash tại thư mục gốc. L05 formula.3 nhắc cách tạo `gd.csv` (đuôi, UTF-8, cùng thư mục) | lint/render |
| E51 L02/L06/L13 không có việc tự đo | **L02**: step hiện mã "hai cách viết" (`tang/goi/thang`, đúng mã đã đo) + lab thêm dòng `Goi ham cham hon viet thang: CO`; **L06**: lab thêm hai dòng `getsizeof hai danh sach: bang nhau` và `tracemalloc hai danh sach: chuoi lon hon`; **L13**: lab thêm dòng `Bo nho khi dong tang 10 lan: gan nhu khong doi` (đỉnh `tracemalloc` ở 2 000 và 20 000 dòng). Cả ba chấm HÌNH DẠNG đầu ra (CO/bằng nhau/không đổi), không số tuyệt đối; đề trên màn hình, gợi ý, `de.md`, `mong_doi.txt`, `loi_giai.py` khớp nhau | `verify_pyt` chạy `lab_l02/l06/l13` thật: PASS; `lab_gate` 14/14 |
| L01 "gần mười một năm rưỡi" | "hơn mười một năm rưỡi" (139 tháng = 11,58 năm) | lint |
| Lab: `cham.sh` ghi đúng chỗ người học đứng | step đề của MỌI bài PYT có dòng "Lưu tệp ở thư mục gốc của bộ khoá (nơi có `labs`), mở Git Bash tại đó để chấm"; mọi `de.md` ghi "Chấm (chạy từ thư mục gốc của bộ khoá, nơi có thư mục `labs`; để tệp của bạn ở đó hoặc ghi đường dẫn tới tệp)" | lab_gate 14/14 |

## 3. P1: giảng tại chỗ (dự kiến 14/14 bài P1 = 2)
| Bài | Từ | Cách giảng |
|---|---|---|
| L00 | trình soạn thảo, tạo tệp `.py`, `python -c`, cài Python/PATH | như mục 2 |
| L05 | `repr`, `rstrip` | pitfalls.5: "lệnh in giá trị kèm cặp nháy: chuỗi rỗng hiện `''`" (`introduces: pyt_repr`); quiz.1: "`rstrip("\n")` cắt dấu xuống dòng ở cuối chuỗi" (`introduces: pyt_rstrip`) |
| L06 | "con trỏ", "cấp phát", `__slots__` | example.8: "con trỏ = số 8 byte ghi chỗ chứa giá trị thật"; "cấp phát" thay bằng "đã xin thêm"; scale.1 hiện cách viết dòng `__slots__ = (…)` ngay dưới `class` |
| L07 | "ngoại lệ", "nhả khoá", "luồng điều khiển" | hook.1 định nghĩa "ngoại lệ = lỗi được báo ra, có tên loại và lý do" (`introduces: pyt_ngoai_le`); "nhả khoá" → "đóng kết nối"; "luồng điều khiển" → "việc rẽ nhánh thông thường" |
| L12 | `sys.executable`, `capture_output`, `text`, `--tb=short` | hàng lệnh bảng sym giải `-q`, `--tb=short`; gợi ý lab giải `sys.executable`, `capture_output=True`, `text=True`, `--tb=no`, `-p no:cacheprovider` (`introduces: pyt_sys_executable, pyt_capture_output`) |
| L13 | "∝", "hằng số", "cơ sở dữ liệu" | bỏ ký hiệu và chữ "hằng số" (viết "tăng theo số dòng", "gần như không đổi"); "cơ sở dữ liệu" có chú giải ở scale.1 (bảng và lời đọc) |

Sổ `symbols.PYT.yaml` thêm 5 mục `term:` (không ghi đè tệp): `pyt_sys_executable`, `pyt_capture_output`, `pyt_ngoai_le`, `pyt_repr`, `pyt_rstrip`; `assumes` thêm: L06/L07 `pyt_repr`; L12/L13 `pyt_ngoai_le`. Bài L06 trước đây nhắc "ngoại lệ" ở câu báo bài sau: đổi thành "bắt lỗi và gỡ lỗi" để E52 sạch.

## 4. Cổng thật (kết quả cuối)
- `gates` từng bài (verify → gen → lint → render): 14 bài lint **0 FAIL, 0 WARN**, render **0 vấn đề**; `lab_gate PYT`: **14 PASS · 0 FAIL (120 lab)**.
- Lời đọc (từ, ≤ 2 300): L00 2289, L01 2151, L02 2189, L03 2257, L04 2224, L05 2063, L06 2264, L07 2125, L08 2248, L09 2057, L10 2116, L11 2233, L12 2185, L13 2290 (thêm ở đâu thì cắt ở chỗ khác, không bỏ `covers`).
- `lv.py curriculum curriculum/pyt.yaml`: 14 bài, **0 lỗi**; `tests/test_e52.py`: **0 FAIL**.
- `screen_code.py gen-pyt`: 334 khối, ghi 334, chưa khớp 0; `check --course PYT`: **PASS 526 · FAIL 0 · STALE 0 · MISSING 0 · ORPHAN 0 · WARN 0**.
- `verify_pyt` toàn khoá: 220/222 PASS; 2 FAIL là ô đo thời gian lệch quá ×8 do máy tải (mục 6), từng bài chạy lại riêng đều PASS (L03 21/21, L04 17/17).

## 5. Công cụ mới
- `lib.py`: `py(..., show_files={tên: [(cũ, mới)…]})` và `sh(..., show_files=…)`: tệp đó PHẢI hiện trọn trên màn hình (một khối, hoặc nhiều khối liền nhau tách step, chỉ cách nhau dòng trống).
- `screen_check.check_show_files` (gọi từ `verify_pyt`): dựng lại tệp từ khối trên màn hình (áp cặp thay chữ), với `py(...)` chạy lại chương trình bằng Python/pytest thật và so từng dòng với kết quả hiện; với `sh(...)` kiểm văn bản hiện = tệp của phiên đã chạy. Đã gắn cho L12 (5 chương trình) và L08 (2 phiên): 7 cổng `screen-files` PASS.
- `lib.pr_steps`: thêm dòng nói chỗ chạy `cham.sh`.

## 6. Mục không sửa / còn hở, kèm lý do
- **L07 scale.1**: số tuyệt đối trên bảng vẫn là số đo trên "máy kiểm" (đang bị các tác tử khác làm tải nặng, best-of-5): hiện try ≈ 2 s so với isdigit ≈ 0,5 s ở 50%, máy người đọc ra ≈ 0,5 s so với 0,2 s. Không có số đo "chuẩn" duy nhất; bảng ghi rõ "số minh hoạ" và lời nói "cỡ vài lần, đổi theo máy" đúng ở cả hai máy. Nên đo lại một lần khi máy rảnh nếu muốn số đẹp hơn (`verify_pyt.py L07 --remeasure`).
- **L09 bảng ≈ 200/300/200**: là số đo trên máy kiểm (người đọc ra ×59/×177/×122): đã bỏ cách nói "≈ 200 cho mọi quy mô", mọi chỗ khái quát nay nói "hàng chục đến hàng trăm lần".
- **Phép đo thời gian bất ổn khi máy tải (không phải lỗi bài)**: máy dùng chung với các tác tử dựng khác nên hai lần `verify_pyt` toàn khoá có ô đo lệch quá ×8 so số đã lưu, mỗi lần một ô khác nhau và đều thuộc bài tôi KHÔNG đổi số đo: lần 1 `L03 t_set_1e3`, `L10 t_groupby_1e6`; lần 2 `L03 t_set_1e3` (lưu 1,1e-7 s, đo 1,3e-6 s), `L04 t_bad_20/24` (lưu 0,05/1,07 s, đo 0,63/8,7 s). Chạy lại riêng từng bài khi máy rảnh: `verify_pyt.py L03` 21/21 PASS, `L04` 17/17 PASS, `L10` PASS (18/18, lần chạy đơn); các lần chạy toàn khoá còn lại: 219/221 và 220/222, mọi FAIL đều là ô `measure` kiểu này. Kiểm mã/đầu ra/`screen`/`screen-files` của cả khoá PASS ở mọi lần. Đề xuất người điều phối chạy lại toàn khoá khi máy rảnh.
- **Lỗi có sẵn ở `lib.split_note`** (không phải do vòng này, không sửa để khỏi đổi lời đọc của mọi bài dùng nó): hai biểu thức `re.search(r"\x08(vì|nên|do|theo|thay|nghĩa là)\x08", …)` dùng nhầm ký tự lùi `\x08` thay cho `\b`, nên bộ sinh luôn chèn câu đệm "Nghĩa là mỗi kết luận…"/"Vì vậy ta đọc kết quả thật…" (L12 đã bỏ bằng `nofill`). Đề xuất người điều phối quyết định sửa trước đợt TTS tới.
- **Ba video STALE (L03, L08, L11)** vốn đang dựng lại; vòng này L03/L04/L11 đổi thêm một dòng ghi chú lab, L08 đổi nội dung: cả 11 + 3 bài trên cần dựng lại.
- Không chạy tai người/TTS: các câu `say` mới/đổi (L00, L02, L05, L06, L07, L08, L12, L13, L09, L10) đều ≥ 8 từ mỗi step, từng câu 4–38 từ (lint WARN 0) nhưng chưa nghe.
