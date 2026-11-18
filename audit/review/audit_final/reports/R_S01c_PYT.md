# S01c PYT: đã đọc 14/14 bài (L00–L13), video dựng lại 2026-11-14

Người đọc độc lập. Tiêu chí: BRIEF_READ_S01 + sample_f/BRIEF + ADDENDUM (P8, P9). Python dùng để chạy: `labs/.venv-pyt` (3.11.9, numpy 2.4.6, pandas 3.1.1, matplotlib 3.11.2, pytest 9.2.0) và `.venv` (3.13.5). Không sửa tệp nào trong kho; tệp tạm ở scratchpad.

Quy ước chấm P1 (nêu rõ để người sau tái lập): một mục chỉ trừ P1 khi (a) hiện trên màn hình hoặc được đọc, (b) người học cần nó để theo điểm đang giảng, (c) chưa được giảng trong bài này hoặc bài PYT đứng trước. Lệnh/ký hiệu phụ chỉ để sinh ra kết quả đã được lời đọc nói thành lời được ghi ở cột "Cần biết trước", không trừ điểm, trừ L08 (xem dưới).

## 1. Kiểm tra dựng lại (STALE, SRT, chương)
- `spec_sha256` trong `out/PYT/Lxx/build_report.json` so với `lv.spec_digest` (băm JSON của YAML bỏ `asr_reviewed`): **14/14 khớp, không bài nào STALE**. (sha256 thô của tệp YAML khác vì băm bỏ `asr_reviewed`; mtime YAML 22:51 muộn hơn bản dựng 16:13 nhưng chỉ khác phần ghi chú ASR.)
- SRT so với `say`: so TOÀN BỘ 14 bài (không chỉ 4): chuỗi từ giống 100% (2 057–2 296 từ mỗi bài, 0 chỗ lệch). Lưu ý: SRT sinh từ chính `say`, không phải ASR độc lập; `asr_report.md` ghi nhiều câu "NOT_VERIFIED bằng tai người" (ví dụ "byte" nghe thành "bay", "Đáp án" nghe thành "Đáp ản"), tôi không kiểm được bằng tai.
- `chapters.txt`: 12 chương mỗi bài, tiêu đề trùng tiêu đề cảnh 14/14. Một giọng `vi-VN-NamMinhNeural` ở cả 14 bài (không trộn giọng).
- Thời lượng: 17,9–23,9 phút/bài, trong đó 5–11 phút là đoạn dừng tĩnh (quiz 60 giây + bài tự làm 240–600 giây); lời nói thật cỡ 12–13 phút.
- `checks` trong YAML: 174/174 biểu thức đúng (chạy lại bằng Python 3.13).

## 2. Bảng chuẩn xác
MUST: **không phát hiện**. Lời đọc nói rõ số đo "trên máy kiểm / số minh hoạ / tuỳ máy" ở mọi bài có số đo (L00 không có số phụ thuộc máy).

| Bài | Mức | Cảnh/step | Trích nguyên chữ | Vì sao + bằng chứng | Đề xuất | Tin cậy |
|---|---|---|---|---|---|---|
| L12 | SHOULD | formula.2 (hook.1, pitfalls.0) | `test_phi.py:18: in test_bien` ; `test_float.py:5: in test_cong` | Người học gõ đúng tệp hiện trên màn hình thì được `test_phi.py:12` và `test_float.py:3` (đã chạy pytest 9.2.0 với đúng nội dung màn hình). Số dòng trong vết lỗi khác tệp họ gõ; người mới có thể tưởng gõ sai. | bỏ số dòng khỏi vết lỗi hiển thị hoặc ghi chú "số dòng của bạn có thể khác" | CONFIRMED |
| L04 | SHOULD | scale.1 | "nên thời gian tăng theo **lũy thừa** của độ dài" | Tăng gấp đôi mỗi ký tự là hàm mũ (2^n), không phải luỹ thừa của độ dài (n^k) như nghĩa thông thường; cùng bài sau đó nói "gấp đôi mỗi ký tự" đúng. | "tăng theo hàm mũ (gấp đôi mỗi ký tự)" | PLAUSIBLE |
| L10 | SHOULD | formula.1, example.0 | `ngay  str` ; `datetime64[us]` | Đầu ra đúng với pandas 3.1.1 (đã chạy); pandas 2.x in `object` và `datetime64[ns]`. Màn hình không nói phụ thuộc phiên bản (L08 có dạy ghim phiên bản nhưng bài này không nhắc lại). | thêm một dòng: "pandas bản cũ hiện object / ns" | PLAUSIBLE (chưa chạy pandas 2) |
| L10 | SHOULD | formula.5 | "giao dịch rút thứ hai thiếu tiền nên không được đếm" | "thiếu tiền" dễ đọc thành "không đủ tiền"; ý đúng là ô số tiền để trống (lời đọc nói "thiếu số tiền"). | "để trống số tiền" | PLAUSIBLE |
| L01–L13 | thông tin | các bảng quy mô | số giây trong bảng | Đo lại: bộ nhớ khớp gần như tuyệt đối (L03 40,0/65,5 MB; L06 18,5/19,3 MB; L10 139/19,1 MB; L11 SVG 118 KB và 10,7 MB; L13 B 52 KB, C 9,3 MB); thời gian lệch 2–10 lần theo máy/phiên bản (ví dụ L04 mẫu viết kém 25 ký tự 1–9 giây tuỳ cách đo; L02 gọi hàm/viết thẳng 2,0 lần ở 3.11, 5,1/2,5 giây ở 3.13) nhưng bậc độ lớn, chiều so sánh và tỉ lệ đúng; bài đã nói "máy bạn khác". | không cần sửa | CONFIRMED |

Các bài còn lại: không phát hiện lỗi kiến thức.

## 3. Bảng độ sâu
Phút = độ dài video (gồm dừng). sha16 lúc đọc (không đổi đến lúc ghi báo cáo).

| Bài | sha16 | Phút | P1 | P2 | P3 | P4 | P5 | P6 | P7 | P8 | P9 | Tổng(P1–P7) | Mất gốc | Cần biết trước (dùng, không giảng tại chỗ) | Chỗ thiếu chính |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| L00 | 230caeb772c0e088 | 18,2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | `echo $?`, dấu nhắc `$`, Git Bash (chỉ ở de.md) | Git Bash không được cài/giảng ở đâu trong khoá |
| L01 | 2b0a1826de2251c4 | 18,5 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | `list(...)`, Ctrl+C (có nói) | không đáng kể |
| L02 | a441fa6372f4b17f | 18,4 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | định dạng `:.2f` (ví dụ đo giờ) | `:.2f` chưa giảng (L00 chỉ dạy `:,`) |
| L03 | 17a0fb2b5311926c | 18,6 | 2 | 2 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | đơn vị byte | intuition.1: chú thích đỏ "…KHÔNG tạo danh sách mới" bị hộp `doc_lap` cắt mất chữ "mới" |
| L04 | 5a21079d6b05ea80 | 18,8 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | không | sym.2 dồn 9 ký hiệu mẫu trong một bảng; "lũy thừa" dùng sai nghĩa (mục 2) |
| L05 | 5c435eca8783b7e7 | 17,9 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | `tail -n 1`, "luồng in" (stdout), KB/MB/GB | pitfalls.2 dùng lệnh shell nhiều tầng |
| L06 | 3173f2dea43538db | 18,7 | 2 | 2 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | `"A%07d" % i` (định dạng kiểu cũ) | practice.0: nút "Dừng video" đè lên chữ cuối "…để chấm" |
| L07 | d6a9aff386acb7b3 | 17,9 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | `%(levelname)s`, `sys.stdout` | formula.2/.4: đoạn giải thích nằm TRÊN tiêu đề "Bước", đảo thứ tự so với các bước khác |
| L08 | 0b901c1beace00d6 | 20,7 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | ĐỦ | `grep -E`, `wc -l <`, `find … \| sort`, `mv`, `2>&1`, `python -m` (nhiều lệnh shell không giảng) | 4–5 lệnh shell xuất hiện không giảng (P1=1); bước cài `pip` cần mạng, video không chạy |
| L09 | 4c53111dce0f576b | 17,9 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | "bit", `astype` (có nói "đổi sang kiểu 8 byte") | không đáng kể |
| L10 | d7adbec8b3c414b1 | 19,3 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | phụ thuộc pandas 3 (mục 2) | ghi chú phiên bản pandas |
| L11 | 8637e0cba4816d86 | 19,6 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | `default_rng().normal`, gỡ gói lồng `fig, (ax1, ax2) =`, `dem, bien, _ =` | thang lôgarit và ô lục giác không có hình thật (chỉ chữ/phác) |
| L12 | 8ce6a8c8966fd924 | 20,5 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | `python -m` | số dòng vết lỗi lệch tệp (mục 2); bài tự làm dùng `subprocess` mới (có giảng trong gợi ý) |
| L13 | 7836bc80fb84b47f | 23,9 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | ĐỦ | `sys.path.insert` / `exec(MODULE, ns)` để nạp mô-đun từ thư mục tạm (de.md gợi ý, không giảng); `importlib` trong hàm chấm chép sẵn | bài tự làm nặng nhất, dừng 10 phút ngắn so với việc thật |

Ghi chú điểm:
- P3=1 ở L03 và L06 vì lỗi hiển thị thật (chữ bị cắt/đè). Ở L08 intuition.1, chú thích đỏ "hai bản numpy không ở chung được" tràn mép hộp nhưng đọc được: giữ P3=2.
- P1 sát ngưỡng ở L08 (đã trừ). Nếu người chấm khác cũng trừ L05, L00 hoặc L12 (mỗi nơi một lệnh phụ), tỉ lệ P1=2 xuống dưới 90%: nên giảng một dòng cho `tail`, `echo $?`, `-m`.
- P8=2 ở cả 14 bài (mỗi bài có tệp tự viết, `de.md` có số khác ví dụ, `mong_doi.txt`, `cham.sh`). P9=2 ở cả 14 bài (bảng ≥ 2 quy mô/mốc thời gian + đánh đổi).

## 4. Lab (làm như người học: chỉ đọc `de.md`, tự viết trong scratchpad, chấm bằng `bash labs/cham.sh PYT Lxx <tệp>`, sau đó mới so `loi_giai`)
Thời gian là ƯỚC LƯỢNG cho người mất gốc (tôi viết mỗi bài trong 2–5 phút nhưng đã xem bài giảng); không đo được thời gian người thật.

| Bài | Tự làm được | Thời gian ước | Kẹt ở đâu | mong_doi khớp màn hình |
|---|---|---|---|---|
| L00 | có | 10–15 phút | tạo tệp bằng trình soạn thảo, mở Git Bash tại thư mục gốc | khớp (cham: ĐÚNG) |
| L01 | có | 15 phút | không | khớp (ĐÚNG) |
| L02 | có | 20–25 phút | phần đo `perf_counter` (có đủ trong bài) | khớp (ĐÚNG; dòng cuối CO phụ thuộc máy nhưng ổn định) |
| L03 | có | 15 phút | không | khớp (ĐÚNG) |
| L04 | có | 15–20 phút | viết hai mẫu `\d`/`[\d.]` | khớp (ĐÚNG) |
| L05 | có | 20 phút | ghi `gd.csv` trước khi đọc | khớp (ĐÚNG) |
| L06 | có | 25–30 phút | điều kiện rút với thấu chi; hai kiểu đo bộ nhớ | khớp (ĐÚNG) |
| L07 | có | 15–20 phút | thứ tự except, `repr` | khớp (ĐÚNG) |
| L08 | phần | 20–30 phút | `pip install` cần mạng; phần in phiên bản làm được ngay; tôi chấm bằng môi trường có sẵn, không chạy `pip install` | khớp (ĐÚNG) |
| L09 | có | 15–20 phút | `std` mặc định chia n (de.md đã nêu) | khớp (ĐÚNG) |
| L10 | có | 20–25 phút | `dt.day`, `idxmax` (có trong gợi ý) | khớp (ĐÚNG) |
| L11 | có | 20–25 phút | đọc lại từ `ax.patches`, `get_ylim` | khớp (ĐÚNG) |
| L12 | có | 30–40 phút | `subprocess.run` + `sys.executable`; lấy dòng cuối `stdout` | khớp (ĐÚNG) |
| L13 | phần | 45–60+ phút | nạp `phan_tich` từ thư mục tạm cho phần đo (cần `sys.path.insert`/`exec`, chỉ nêu tên trong de.md); chuỗi mã lồng và `\\n` | khớp (ĐÚNG) |

`mong_doi.txt` so với khối "Kết quả mong đợi" trên màn hình (practice.1): **14/14 trùng từng dòng**. `cham.sh` ra ĐÚNG 14/14 với lời giải tôi tự viết.

## 5. Người học kẹt ở đâu (người mất gốc, chỉ xem video này và các bài PYT trước)
- L00: không kẹt cứng. Chỗ đầu tiên chưa rõ: prereq.0 `$ echo $?` (không nói `echo` làm gì); khi làm lab: "mở Git Bash tại đó" (khoá không cài/giảng Git Bash).
- L01: không kẹt.
- L02: không kẹt; ví dụ đo ở example.2 dùng `:.2f` chưa giảng.
- L03: không kẹt; hình intuition.1 mất chữ cuối ở chú thích đỏ.
- L04: sym.2 (bảng ký hiệu mẫu: chín ký hiệu `\d \w . + * ? [\d.] (…) r"…"` trong một bước) là chỗ dễ rối đầu tiên.
- L05: pitfalls.2 `PYTHONIOENCODING=cp1252 python -c "print('tiền')" 2> loi.txt; echo $?` rồi `tail -n 1 | cut -d: -f1` (`tail` không giảng; "luồng in" chưa định nghĩa).
- L06: example.9 `"A%07d" % i` (dấu `%` dùng khác L00, không giảng); không chặn việc hiểu.
- L07: không kẹt.
- L08: sym.1/formula.3–5 các lệnh `find … | sort`, `grep -E "^(numpy|pandas)=="`, `wc -l < …`, `mv` (không giảng); bài tự làm cần mạng.
- L09: không kẹt; lan truyền (3,) với (3,1) giảng chậm, đủ.
- L10: không kẹt; nếu cài pandas 2 thì đầu ra `object` khác màn hình.
- L11: formula.3 `dem, bien, _ = ax.hist(...)` và formula.7 `fig, (ax1, ax2) = plt.subplots(1, 2)` (gỡ gói lồng/dấu `_` chưa giảng); example hexbin dùng `rng.normal`.
- L12: sym.0 `python -m pytest` (`-m` không giảng); gõ lại tệp kiểm thì số dòng trong vết lỗi khác màn hình; bài tự làm: `subprocess` (có giảng trong gợi ý).
- L13: practice (bước 4 phần đo): nạp `phan_tich` từ thư mục tạm; de.md đưa hai cách (`exec(MODULE, ns)`, `sys.path.insert(0, thu_muc)`) nhưng bài không giảng cách nào.

## 6. Số đã tính lại / mã đã chạy
- Khối `>>>` trên màn hình (259 khối, đủ các bài): chạy trong console có trạng thái theo từng cảnh, trên 3.11.9 và 3.13.5: **259/259 khớp** (riêng các vết lỗi: so dòng cuối và tên lỗi; `<stdin>` so với `<console>` bỏ qua).
- Chương trình `.py` hiện trên màn hình kèm khối "kết quả" (95 cặp mã/kết quả): chạy tự động từng khối riêng, 59/95 khớp ngay; 36 khối còn lại cần ngữ cảnh (tệp CSV, lớp/hàm định nghĩa ở khối trước, `ngan_hang`, `csv.py`) hoặc là số đo thời gian (L02 `0.24 giay` so với 0,37 giây trên máy này). Các khối đó tôi dựng lại thủ công từ chính nội dung màn hình và chạy: L05 (gd.csv, ghi/đọc, JSON, 33 byte trên Windows, repr rỗng, lệnh shell `PYTHONIOENCODING`), L06 (lớp, dataclass, kế thừa, `__repr__`, `getsizeof`), L07 (try/except/finally, lỗi riêng, logging), L08 (mô-đun, gói, `__name__`, `venv`, csv.py che bộ có sẵn, requirements 17 dòng), L10/L13 (pandas, nhóm, chunksize, bẫy ghi đè), L12 (pytest, 7 ca, mã sai `<=`): khớp trừ số dòng pytest (mục 2). Không chạy được: khối diff `-`/`+` ở hook L12 (chỉ đọc).
- `breakpoint()`: 3.11 dừng ở dòng kế, 3.13 dừng ngay dòng gọi: đúng như bài nói (L07).
- Số đo bộ nhớ lấy lại: khớp (mục 2). Số đo thời gian: cùng bậc, khác hệ số (đã nêu).
- Phép tính tay trên màn hình (tổng nhóm, tỉ lệ nhìn thấy 4,0 và 1,03, nghịch lý Simpson 90 / 33,3 / 39 và 88,9 / 20 / 82, trung vị 3 và 3,5, 25 GB = 5 × 5 GB, mốc ngoại suy 3,4 phút / 2,6 phút / 12 phút / 20 giờ): đúng. Một số làm tròn của bảng ngoại suy (L04 "≈ 20 giờ" so với 18,2 giờ tính từ 1 giây × 2^16) là làm tròn sát mức "≈" đã ghi.

## 7. Khung hình đã xem
Mỗi bài 11 khung ghép thành 2 tấm (6 + 5; cỡ 960×540 mỗi khung): mở đầu, 2 khung cơ chế/công thức, ví dụ, bảng quy mô/đánh đổi, lỗi thường gặp, quiz (đề và quyết định), bài tự làm (đề và kết quả mong đợi), tổng kết. Tổng 154 khung. Xem thêm nguyên độ phân giải: L03 `00037.png`, L06 `00126.png`, L07 `00041.png` và `00046.png`.
Lỗi hiển thị:
- L03 `00037.png` (intuition.1): chú thích đỏ "ban_sao = goc: dán thêm nhãn, KHÔNG tạo danh sách mới" bị hộp `doc_lap` đè mất chữ cuối.
- L06 `00126.png` (practice.0): nút "Dừng video, tự làm rồi xem tiếp" đè lên "để chấm" của dòng lưu ý.
- L07 formula.2 và formula.4: đoạn "Vì…" nằm trên tiêu đề "Bước 2/3" (thứ tự khác các bước khác).
- L08 intuition.1: chú thích đỏ tràn mép hộp (vẫn đọc được).
- Toàn khoá: nội dung chiếm khoảng nửa trên khung 1920×1080, nửa dưới trống; mã cỡ chữ ≈ 24 px: đọc được trên máy tính, nhỏ trên điện thoại. Không có chữ tràn/cắt nào khác trong số khung đã xem.
- Công thức LaTeX hiển thị đúng (số nhóm bằng dấu cách mảnh trên màn hình); lời đọc không có chữ số nào (mọi số đã đọc thành chữ), có chữ Latin tối thiểu: "Python", "JSON", "byte", "bit", tên tệp đọc qua "chấm py/xê ét vê".
- Lời đọc: câu ≤ 4 từ có 3–9 câu/bài (tín hiệu kiểu "Đáp án như sau.", "Bước ba, nhóm."; ASR có nghe sai "Đáp án" thành "Đáp ản" ở một bài); không có câu ngắn gây hiểu sai.

## 8. Nhận xét chung
- Kết quả theo ngưỡng chốt: MUST 0; P1=2 ở 13/14 bài (92,9%, ≥ 90%); P8=2 ở 14/14 (100%). Có thể đạt "bắt đầu học" cho PYT.
- Điểm mạnh nhất: mọi con số hiện trên màn hình đều chạy lại được và khớp; mỗi bài có đúng mô hình (hook số liệu, hình cơ chế, ví dụ tay, đường kiểm thứ hai, bảng quy mô, 3 lỗi, quiz có dừng, lab có mong_doi).
- Rủi ro P1 tập trung ở lệnh shell không giảng (L08 rõ nhất; L05, L00, L12 mỗi nơi một lệnh): sửa bằng một câu mỗi chỗ hoặc một bảng "lệnh shell dùng trong khoá" ở L00.
- L13 và L12 là hai lab nặng nhất; L13 đòi nạp mô-đun từ thư mục tạm (`sys.path.insert`/`exec`) mà bài không giảng, dừng 10 phút ngắn. Nên thêm một dòng gợi ý có mã mẫu hoặc nới thời gian.
- Số dòng trong vết pytest (L12), phụ thuộc phiên bản pandas (L10), và hai lỗi hiển thị (L03, L06) là các mục SHOULD cụ thể đáng sửa.
- Không đánh giá được bằng tai người (giọng, ngắt nghỉ, cách đọc "byte", "JSON"): `asr_report` ghi NOT_VERIFIED.
- Chưa chạy `pip install` (cần mạng, sẽ tạo `.venv-hoc` trong kho); môi trường kiểm có đúng 17 gói ghim, khớp requirements 17 dòng.
