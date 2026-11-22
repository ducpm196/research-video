# Kiểm định độc lập Stage 10 — Khoá `PAR` (`L00–L13`: 14/14 bài)

> Lưu ý tệp hướng dẫn: `D:\research-video\audit\review\sample_f\ADDENDUM.md` không tồn tại; đã đọc `D:\research-video\audit\review\audit_final\ADDENDUM.md` cùng `BRIEF.md` và `BRIEF_R4.md`. Không đọc bất kỳ tệp nào trong `audit/review/audit_final/reports/`, không sửa tệp nào.

## Kết luận: **NO-GO**
- **Điểm mạnh (nền tảng chuyên môn & bản dựng)**: **0 lỗi sai kiến thức chuyên môn và 0 lỗi số học** trong cả 14 bài. Toàn bộ `lv.py lint` (14/14: 0 FAIL, 0 WARN), `verify_par.py` (96/96 PASS), `build_report.json` (`spec_sha256` & `tts_sha256` khớp 14/14), `L*.srt == say` (14/14), `asr_report.md` (0 thiếu audio, 0 chưa xem xét), `layout_PAR.tsv` (trống), chạy trực tiếp `labs/PAR/L*/loi_giai.py` bằng `.venv/Scripts/python.exe` (14/14 khớp `mong_doi.txt`), và 51 PNG kiểm tra trực tiếp đều hiển thị sạch đẹp.
- **Lý do NO-GO**: Xuất hiện các lỗi **`MUST` mang tính hệ thống trên cả 14/14 bài** ở phần thực hành (`practice` + `labs/PAR/L*/de.md`), ánh xạ `covers:`, thiếu chốt `Hai mức quy mô:` trong `recap`, và vi phạm chuẩn `P1` chặt (chủ yếu ở `practice.0`/`practice.1`/`de.md`, cộng một số ký hiệu/thuật ngữ ở thân bài).

---

## 1. Bảng tóm tắt chỉ số (14 bài `PAR/L00..L13`)

| Hạng mục kiểm | Kết quả | Chi tiết |
|---|---|---|
| Số bài đạt `MUST = 0` (toàn diện kể cả P1/P8/P9/`covers`) | **0 / 14** | Thân bài kiến thức thuần đạt **14/14** (0 lỗi toán/lý thuyết), nhưng **14/14** mắc `MUST` hệ thống ở `practice` (lộ lời giải trước `pause`), `de.md` (thiếu format stdout), `P1` mã thực hành, và `covers:` lệch |
| Số bài `P1 = 2` (theo chuẩn `BRIEF_R4.md` chặt cả thân + `practice` + `de.md`) | **0 / 14** | Nếu chỉ tính thân bài: L02, L04, L12 đạt hoặc sát 2; nhưng tính cả `practice` & `de.md`: 14/14 bài `P1 = 0` (bảng cách đọc không phủ mã `practice.1`) |
| Số bài `P8 = 2` | **0 / 14** | 14/14 bài `P8 = 1` (lộ `loi_giai.py` + `mong_doi.txt` trước `pause`; `de.md` thiếu stdout format; số liệu trùng ví dụ) |
| Số bài `P9 = 2` | **0 / 14** | 14/14 bài có SVG và ≥ 2 mức quy mô trong thân bài, nhưng **0/14** có `<p class="note"><b>Hai mức quy mô:</b> ...` trong `recap` (`P9 = 1`) |
| Số bài `spec_sha256` & `tts_sha256` khớp | **14 / 14** | 100% `build_report.json` khớp `lv.spec_digest` và `lv.tts_digest` |
| Số bài `SRT == say` khớp | **14 / 14** | 100% câu phụ đề trong `out/PAR/L*/L*.srt` khớp từng câu với `say` |
| Số bài `asr_report.md` sạch (`chưa xem xét = 0`, `thiếu audio = 0`) | **14 / 14** | Tổng 150 câu gắn cờ ở 14 bài đều đã có `asr_reviewed` (trạng thái `NOT_VERIFIED bằng tai người` — chỉ kiểm bằng ASR) |
| Số bài `lv.py lint` PASS & `verify_par.py` PASS | **14 / 14** & **96 / 96** | 0 FAIL, 0 WARN trên cả 14 bài |
| Số bài lab chạy trực tiếp khớp `mong_doi.txt` | **14 / 14** | Chạy `.venv/Scripts/python.exe labs/PAR/L*/loi_giai.py` khớp từng dòng `mong_doi.txt` |
| Số cảnh báo `SHOULD` / `INFO` | **15+ SHOULD / 4 INFO** | Chi tiết ở Mục 2 |

---

## 2. Phát hiện chi tiết (phân tách `MUST` / `SHOULD` / `INFO`)

### A. Lỗi `MUST` (chặn `GO`)

| Bài | Mức | Cảnh/step | Trích nguyên chữ | Vì sao sai + bằng chứng | Đề xuất sửa | Tin cậy |
|---|---|---|---|---|---|---|
| L00–L13 | **MUST** | `practice.1`, `practice.2` (trước `practice.3 pause: 30`) | `practice.1`: in toàn bộ code `loi_giai.py`; `practice.2`: `Đầu ra chạy thật (1 dòng)` in nguyên `mong_doi.txt`; tới `practice.3` mới đặt `pause: 30` (`Hãy bấm tạm dừng và tự làm trước`) | **Lộ lời giải và đầu ra mong đợi TRƯỚC `pause`** ở 14/14 bài (`pauses=[3], first_exp=2`). Người học nhìn thấy đáp án trước khi dừng video tự làm (`P8`). | Chuyển step hiện code mẫu và `Đầu ra chạy thật` ra **sau** `pause: 30` (chỉ giữ bảng giải thích + đề bài trước `pause`), đồng thời dùng tham số khác ví dụ chính. | CONFIRMED |
| L00–L13 | **MUST** | `labs/PAR/L00..L13/de.md` | VD L00 `de.md`: `Tính tăng tốc Amdahl 1 / ((1-p) + p/N) ở N=16 và trần khi N -> inf.` (tương tự ở cả 14 tệp `de.md`) | **14/14 tệp `de.md` thiếu định dạng `stdout` và không tự đứng được**: không ghi tên khoá/định dạng chuỗi phải in (`amdahl_16=6.40x max_limit=10.0x`, `gustafson_16=14.50x`, v.v.). Người học chỉ đọc `de.md` sẽ bị `cham.sh` chấm trượt 100% vì không biết format cần in. L04 `de.md` còn thiếu điều kiện sắp giảm dần danh sách trong `loi_giai.py` (`for j in jobs:` không gọi `sorted(..., reverse=True)`). | Bổ sung mục **Định dạng đầu ra (`stdout`)** đầy đủ + số chữ số làm tròn vào từng `de.md`, bổ sung đủ tham số (vd L08 nêu rõ 32 luồng), và đổi số bài lab khác với ví dụ bài giảng. | CONFIRMED |
| L00–L13 | **MUST** | `practice.0`, `practice.1`, `de.md` | `practice.0` của 13/14 bài (trừ L04, L07 chỉ thêm 2 dòng) chỉ có: `f"{val:.3f}"` và `print(...)`; trong khi `practice.1` dùng `=`, `//`, `%`, `**`, `;`, `#`, `[:4]`, `[4:]`, `l[0]`, `+=`, `0 if ... else 1`, `10e12`, `:.0f`, `:.1f`, `:.2f` | **P1 chặt FAIL hệ thống (bảng cách đọc không phủ)**: (1) Bảng `practice.0` giảng `:.3f` nhưng code `practice.1` dùng `:.2f`, `:.1f`, `:.0f` hoặc không dùng `:.3f` (L03–06, L09, L13); (2) Hầu hết cú pháp Python trong `practice.1` và lệnh `bash labs/cham.sh ... .py` ở `practice.3` chưa từng được giảng trong khoá PAR (`requires_ext` cũng không đòi khoá Python nào); (3) Nhiều `de.md` dùng từ Anh/ký hiệu chưa giảng trong bài (`Work-Span` L02, `makespan`/`LPT` L04, `False Sharing`/`cache line` L05, `SIMD`/`float32` L06, `TF/s`/`TB/s`/`FLOP/byte`/`arithmetic intensity` L07, `pipeline` L12). | Sửa bảng `practice.0` của từng bài để khớp đúng 100% cú pháp, định dạng `:.0f/.1f/.2f` và toán tử (`//`, `%`, `**`, `;`, `[:4]`, `if..else`, `10e12`) mà bài đó dùng; bỏ từ Anh chưa giảng khỏi `de.md`. | CONFIRMED |
| L00–L13 | **MUST** | `covers:` cuối mỗi tệp YAML | L00 `O2 -> check`, `O3 -> practice`; L01 `O2 -> check`, `O3 -> practice`; L02 `O2 -> check`, `O3 -> practice`; L03 `O2 -> check`, `O3 -> practice`; L04 `O3 -> practice`; L05 `O3 -> practice`; L06 `O3 -> practice`; L07 `O2,O3 -> check`, `O4 -> practice`; L08 `O1 -> example`, `O2 -> check`, `O4 -> practice`; L09 `O3 -> check`, `O4 -> practice`; L10 `O1 -> example`, `O2,O3 -> check`, `O4 -> practice`; L11 `O3 -> check`, `O4 -> practice`; L12 `O3 -> check`, `O4 -> practice`; L13 `O1 -> stage1`, `O2 -> stage2`, `O3 -> practice` | **`covers:` trỏ sai cảnh dạy thực tế ở 14/14 bài** (dường như áp mẫu cứng `example/check/practice`): VD L00 `O2` (đo ngược $p$) nằm ở `measure` chứ không phải `check`; L00 `O3` (chọn thuê lõi hay sửa tuần tự) nằm ở `quiz` chứ không phải `practice`; L01 `O3` (đổi cách đo $q \leftrightarrow 1-p$) nằm ở `formula`/`check` chứ không phải `practice`; L03 `O3` (số thực + tái lập) nằm ở `example`/`pitfalls`/`quiz`, `practice` chỉ mô phỏng số nguyên `c=2`; L07 `O3` (điểm gãy $F/B$) nằm ở `formula`/`roof`/`example`/`quiz`, `check` không tính điểm gãy; L08 `O1` (lưới/khối/thứ tự bất kỳ) nằm ở `sym`/`intuition`, không phải `example`; L10 `O1` (mô phỏng tay 3 máy) nằm ở `check`, `O2` nằm ở `formula`, `O3` nằm ở `example`; L11 `O3` nằm ở `formula`/`pitfalls`; L12 `O3` nằm ở `example`/`quiz`; L13 `O1,O2` trải `timeline` + `stage1..5`, `O3` ở `quiz`. | Sửa `covers:` cho từng mục tiêu trỏ đúng cảnh thực sự giảng/thực hành mục tiêu đó (cho phép trỏ danh sách hoặc đúng cảnh cốt lõi như `measure`, `formula`, `example`, `quiz`). | CONFIRMED |

### B. Lỗi `SHOULD` (nên sửa để hoàn thiện chuẩn Stage 10)

| Bài | Mức | Cảnh/step | Trích nguyên chữ | Vì sao cần sửa + bằng chứng | Đề xuất sửa | Tin cậy |
|---|---|---|---|---|---|---|
| L00–L13 | **SHOULD** | `recap` (tất cả 14 bài) | Không có `<p class="note"><b>Hai mức quy mô:</b> ...` trong `recap` | **P9 thiếu chốt quy mô ở `recap` (0/14 bài)**: dù thân bài đều có SVG và ≥ 2 mức quy mô, `recap` của cả 14 bài không tóm tắt 2 mức quy mô và điểm đổi hành vi/đánh đổi bằng mẫu `<p class="note"><b>Hai mức quy mô:</b> ...`. | Thêm 1 thẻ `<p class="note"><b>Hai mức quy mô:</b> ...</p>` vào `recap` của mỗi bài (nêu rõ số liệu 2 mức quy mô + đánh đổi). | CONFIRMED |
| L00, L01 | **SHOULD** | `intuition.0`, `pitfalls.1`, `measure.0` | `10 s`, `100 s`, `15,6 s`, `20,4 s`, `1450 s` | **P1 thân bài**: ký hiệu `s` (giây) xuất hiện trên màn hình từ L00 mà chưa có dòng chú thích `s = giây` trên màn hình (dù lời đọc nói "giây"). | Ghi rõ `giây` hoặc chú thích `s = giây` ở lần đầu trong L00. | CONFIRMED |
| L02 | **SHOULD** | `formula.1` | `Lemma 2 của Brent (1974)` | **P1 / lệch màn hình vs lời đọc**: màn hình dùng từ Anh `Lemma 2` (lời đọc nói `bài báo năm 1974`), người mất gốc không biết `Lemma` là bổ đề. | Đổi trên màn hình thành `Bổ đề 2 của Brent (1974)`. | CONFIRMED |
| L03, L10, L11 | **SHOULD** | L03 `quiz.2`, L10 `pitfalls.3`, L11 `pitfalls.3` | `từng bit` | **P1 thân bài**: thuật ngữ `bit` được dùng ở L03, trước khi được giảng ở L06 `prereq.0` (`8 bit là 1 byte`). | Giải thích ngắn `bit (chữ số nhị phân 0 hoặc 1)` ở L03 hoặc dùng `từng chữ số nhị phân`. | CONFIRMED |
| L04 | **SHOULD** | `pitfalls.0` | `1000 việc 1 mi li giây` | **P1 thân bài**: `mi li giây` xuất hiện ở L04 trước khi được giải thích `0,001 giây` ở L07 `prereq.0`. | Mở ngoặc `(một phần nghìn giây)` ở L04 `pitfalls.0`. | CONFIRMED |
| L05 | **SHOULD** | `hook.0`, `prereq.0`, `pitfalls.3` | `8 byte`, `64 byte`, `8 MB, đệm 64 MB` | **P1 thân bài**: `byte` dùng suốt L05 trước khi được giảng ở L06 `prereq.0`; chữ viết tắt `MB` dùng ở `pitfalls.3` chưa được giải thích (triệu byte). | Giảng ngắn `byte (đơn vị bộ nhớ, bằng 8 bit)` và `MB (triệu byte)` tại L05. | CONFIRMED |
| L06, L09, L10 | **SHOULD** | L06 `pitfalls.2`, L09 `hook.0`, L10 `hook.0` | `20 GB/s`, `119,9 GB/s`, `10 GB/s` | **P1 thân bài**: chữ viết tắt `GB/s` (và `GB`) xuất hiện trên màn hình ở L06, L09, L10 trước khi có giải thích `GB = tỉ byte` ở `L11 check.1` (lời đọc có nói "tỉ byte mỗi giây" ở L06, L09, nhưng L10 đọc nguyên "GB"). | Chú thích `GB = tỉ byte; GB/s = tỉ byte mỗi giây` ở lần đầu xuất hiện (L06 hoặc L10). | CONFIRMED |
| L07–L10 | **SHOULD** | L07 `check.0`, L08 `hook.0`, L10 `pitfalls.0` | `0,1 ms`, `12 ms`, `1 ms`, `2 ms`, `0,05 ms` | **P1 thân bài**: chữ viết tắt `ms` xuất hiện trên màn hình từ L07 mà không có chú thích `ms = mi li giây` trên màn hình (chỉ người nghe `say` mới đoán được `ms` ứng với `mi li giây`). | Thêm chú thích `(ms = mi li giây)` ở lần đầu `ms` xuất hiện (L07 `check.0`, L08 `hook.0`). | CONFIRMED |
| L12 | **SHOULD** | `labs/PAR/L12/de.md`, `practice.1` | Bài học `example.1`: sửa còn `2%` (7,02×); lab `de.md`: sửa xuống `5%` (`after_fix_5pct=5.93x`) | Con số mục tiêu trong lab (`5%`) lệch với con số minh hoạ trong bài giảng (`2%`), dễ gây nhầm nếu `practice.3` chỉ nói "chẩn đoán 25% nạp dữ liệu tuần tự". | Đồng nhất hoặc ghi rõ trong `practice` là thí nghiệm tham số mới `5%` (thay cho `2%` trong bài). | CONFIRMED |
| L13 | **SHOULD** | `stage5.1` | `(NCCL)`, `(Tensor Fusion)` | **P1 thân bài**: đưa tên riêng/thuật ngữ tiếng Anh `NCCL`, `Tensor Fusion` lên màn hình nhưng chưa giải thích trực tiếp `NCCL` là viết tắt gì / `Tensor Fusion` nghĩa là gì. | Bỏ `(NCCL)` hoặc ghi rõ `thư viện truyền thông tập thể NCCL của hãng`; ghi rõ `(gộp tensor — Tensor Fusion)`. | CONFIRMED |

### C. Thông tin (`INFO`)

1. **`curriculum/par.yaml` dòng 12**: vẫn ghi `status: planned` dù cả 14 bài L00–L13 đã có spec và video hoàn chỉnh.
2. **Tiền tố tiêu đề**: 14/14 bài trong `lessons/par/L*.yaml` thêm tiền tố `Bài X — ` trước `title` so với `curriculum/par.yaml` (nội dung phần sau và `objectives` khớp 100%).
3. **ASR (`asr_reviewed`)**: tất cả các câu gắn cờ ở L00–L13 (tổng 150 câu, phần lớn do từ `byte`, `ms`, `Amdahl`, `GB`, `KB`, chữ cái đơn) đều đã đánh dấu `NOT_VERIFIED bằng tai người` (chỉ đối chiếu bằng 2 mô hình ASR, chưa có người thật nghe lại).
4. **Kiểm tra `"càng "` trong `say`**: chỉ có 1 câu ở `L09 pitfalls.0` (`"Lỗi thứ nhất là nghĩ khối càng lớn càng tốt."`), đây là trích dẫn lỗi thường gặp có giải thích phản bác ngay sau đó, không phải lỗi phát âm hay khẳng định tuyệt đối sai. Từ `video` trong `L* quiz.0` nằm trong `foreign_ok` của `lexicon_vi.yaml` chung.

---

## 3. Liệt kê TỪNG mục chưa giảng (`P1` chặt theo `BRIEF_R4.md`)

*(Bao gồm thân bài, `practice.0`/`practice.1`/`practice.3` và `labs/PAR/L*/de.md`)*

| Bài | Cảnh / tệp | Trích chữ chưa giảng | Bảng cách đọc có phủ không |
|---|---|---|---|
| L00 | `intuition.0`, `pitfalls.1`; `practice.1`, `practice.3` | `10 s` (`s`); mã Python `p = 0.90`, `/`, `:.2f`, `:.1f`, lệnh `bash labs/cham.sh ... .py` | **Không** (bảng chỉ ghi `f"{val:.3f}"`, `print(...)`) |
| L01 | `intuition.0`, `measure.0`; `practice.1`, `practice.3` | `100 s` (`s`); mã `s, N = 0.10, 16`, `*`, `:.2f`, lệnh `bash ... .py` | **Không** (bảng chỉ ghi `f"{val:.3f}"`, `print(...)`) |
| L02 | `formula.1`; `practice.1`, `practice.3`; `de.md` | `Lemma 2`; mã `T1, Tinf, P = ...`, `/`, `:.2f`; `de.md`: `Work-Span`, `T_inf`, `T1/P` | **Không** |
| L03 | `quiz.2`; `practice.1`, `practice.3` | `bit`; mã `c = 0`, `;`, `#`, `+`, lệnh `bash ... .py` | **Không** |
| L04 | `pitfalls.0`; `practice.1`, `practice.3`; `de.md` | `mi li giây`; mã `jobs = [...]`, `jobs[:4]`, `jobs[4:]`, `l[0]`, `<=`, `if..else`, `+=`; `de.md`: `makespan`, `LPT` | **Không** (`practice.0` chỉ có `for`, `sum/len/max/min`, `:.3f`, `print`) |
| L05 | `hook.0`, `pitfalls.3`; `practice.1`, `practice.3`; `de.md` | `byte`, `MB`; mã `//`, `*`, `=`; `de.md`: `False Sharing`, `cache line 64B` | **Không** |
| L06 | `pitfalls.2`; `practice.1`, `practice.3`; `de.md` | `20 GB/s`; mã `//`, `%`, `=`; `de.md`: `SIMD`, `float32` | **Không** |
| L07 | `check.0`; `practice.1`, `practice.3`; `de.md` | `ms`; mã `10e12`, `1e12`, `:.1f`, `=`; `de.md`: `10 TF/s`, `1 TB/s`, `FLOP/byte`, `arithmetic intensity` | **Không** |
| L08 | `hook.0`; `practice.1`, `practice.3`; `de.md` | `ms`; mã `;`, `:.0f`, `/`, `*`; `de.md`: `Warp` | **Không** |
| L09 | `hook.0`; `practice.1`, `practice.3`; `de.md` | `GB/s`; mã `**`, `//`, `=`; `de.md`: `^`, `vs` | **Không** |
| L10 | `hook.0`, `pitfalls.0,3`; `practice.1`, `practice.3` | `GB`, `GB/s`, `ms`, `bit`; mã `=`, `*`, `/`, `:.2f` | **Không** |
| L11 | `pitfalls.3`; `practice.1`, `practice.3`; `de.md` | `bit`; mã `=`, `/`, `*`, `:.1f` | **Không** |
| L12 | `practice.1`, `practice.3`; `de.md` | mã `=`, `/`, `+`, `:.2f`; `de.md`: `pipeline nạp` | **Không** |
| L13 | `stage5.1`; `practice.1`, `practice.3` | `(NCCL)`, `(Tensor Fusion)`; mã `=`, `/`, `*`, `:.2f` | **Không** |

---

## 4. Bảng độ sâu & điểm thành phần (14 bài `PAR/L00..L13`)

| Bài | sha16 lúc đọc | Phút | P1 | P2 | P3 | P4 | P5 | P6 | P7 | Tổng | Mất gốc | Chỗ thiếu chính | P8 | P9 | Cần biết trước |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|---|
| L00 | `f617dd1033490282` | 12.95 | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | GẦN | P1: `practice.1`+`de.md`, `s`; P7: `covers` lệch `O2,O3`; P8: lộ code; P9: thiếu `recap` | 1 | 1 | Python cơ bản (`=`, `/`, `:.2f`), `bash`, cộng/chia số thập phân |
| L01 | `90517ed792e37502` | 11.26 | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | GẦN | P1: `practice.1`+`de.md`, `s`; P7: `covers` lệch `O2,O3`; P8: lộ code; P9: thiếu `recap` | 1 | 1 | Python cơ bản (`s, N = ...`, `:.2f`), `bash`, nhân/chia số thập phân |
| L02 | `bc334c3258222bc8` | 10.93 | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | GẦN | P1: `practice.1`+`de.md`, `Lemma`; P7: `covers` lệch `O2,O3`; P8: lộ code; P9: thiếu `recap` | 1 | 1 | Python cơ bản, `bash`, luỹ thừa 2 |
| L03 | `b4c4d49cc160331a` | 11.42 | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | GẦN | P1: `practice.1`+`de.md`, `bit`; P7: `covers` lệch `O2,O3`; P8: lộ code; P9: thiếu `recap` | 1 | 1 | Python (`;`, `#`, `=`), `bash`, nhị phân |
| L04 | `e74f386c14c05e20` | 10.73 | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | GẦN | P1: `practice.1`+`de.md`, `ms`; P7: `covers` lệch `O3`; P8: lộ code; P9: thiếu `recap` | 1 | 1 | Python (`[:4]`, `if..else`, `+=`), `bash` |
| L05 | `e0b7d15779efc283` | 10.47 | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | GẦN | P1: `practice.1`+`de.md`, `byte/MB`; P7: `covers` lệch `O3`; P8: lộ code; P9: thiếu `recap` | 1 | 1 | Python (`//`, `*`), `bash`, khái niệm `byte`/`MB` |
| L06 | `8b91bbaddc36962d` | 10.26 | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | GẦN | P1: `practice.1`+`de.md`, `GB/s`; P7: `covers` lệch `O3`; P8: lộ code; P9: thiếu `recap` | 1 | 1 | Python (`//`, `%`), `bash`, `GB/s` |
| L07 | `d136077ef3264b5e` | 12.17 | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | GẦN | P1: `practice.1`+`de.md`, `ms`; P7: `covers` lệch `O2–4`; P8: lộ code; P9: thiếu `recap` | 1 | 1 | Python (`10e12`, `:.1f`), `bash`, `TF/s`, `TB/s` |
| L08 | `b68fe8381950f156` | 11.79 | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | GẦN | P1: `practice.1`+`de.md`, `ms`; P7: `covers` lệch `O1,2,4`; P8: lộ code; P9: thiếu `recap` | 1 | 1 | Python (`;`, `:.0f`), `bash`, `ms` |
| L09 | `5e3c76fdccd04f23` | 12.17 | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | GẦN | P1: `practice.1`+`de.md`, `GB/s`; P7: `covers` lệch `O3,O4`; P8: lộ code; P9: thiếu `recap` | 1 | 1 | Python (`**`, `//`), `bash`, `GB/s` |
| L10 | `ebf05f922c0ce7aa` | 12.53 | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | GẦN | P1: `practice.1`+`de.md`, `GB/ms/bit`; P7: `covers` lệch `O1–4`; P8: lộ code; P9: thiếu `recap` | 1 | 1 | Python (`:.2f`), `bash`, `GB`, `ms` |
| L11 | `ee9f28342d1d73b3` | 11.66 | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | GẦN | P1: `practice.1`+`de.md`, `bit`; P7: `covers` lệch `O3,O4`; P8: lộ code; P9: thiếu `recap` | 1 | 1 | Python (`:.1f`), `bash` |
| L12 | `c72518597ef63df7` | 9.32 | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | GẦN | P1: `practice.1`+`de.md`; P7: `covers` lệch `O3,O4`; P8: lộ code; P9: thiếu `recap` | 1 | 1 | Python (`:.2f`), `bash`, `pipeline` |
| L13 | `ff12fae972e33561` | 17.18 | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | GẦN | P1: `practice.1`+`de.md`, `NCCL/Tensor Fusion`; P7: `covers` lệch `O1–3`; P8: lộ code; P9: thiếu `recap` | 1 | 1 | Python (`:.2f`), `bash`, `NCCL` |

*(Ghi chú: Thân bài giảng `hook..quiz` của cả 14 bài rất sâu, trực quan và chuẩn xác — `P2, P3, P4, P5, P6` đều đạt `2/2`. Điểm mất tập trung chủ yếu ở `P1` mã thực hành + `de.md`, `P7` `covers:` lệch, `P8` lộ code trước `pause`, `P9` thiếu dòng `Hai mức quy mô:` ở `recap`.)*

---

## 5. Khung hình PNG đã xem trực tiếp (51 khung hình) & Kiểm chứng mã / số

### Khung hình PNG đã xem bằng `read_file` (đều sạch, không đè chữ, không tràn khung, KaTeX rõ nét)
- **L00** (5): `out/PAR/L00/frames/00000.png`, `00026.png`, `00033.png`, `00091.png`, `00097.png`
- **L01** (4): `out/PAR/L01/frames/00016.png`, `00021.png`, `00063.png`, `00076.png`
- **L02** (3): `out/PAR/L02/frames/00014.png`, `00021.png`, `00071.png`
- **L03** (3): `out/PAR/L03/frames/00025.png`, `00029.png`, `00085.png`
- **L04** (3): `out/PAR/L04/frames/00016.png`, `00020.png`, `00079.png`
- **L05** (3): `out/PAR/L05/frames/00021.png`, `00061.png`, `00075.png`
- **L06** (4): `out/PAR/L06/frames/00016.png`, `00020.png`, `00053.png`, `00066.png`
- **L07** (4): `out/PAR/L07/frames/00021.png`, `00031.png`, `00039.png`, `00089.png`
- **L08** (4): `out/PAR/L08/frames/00021.png`, `00025.png`, `00029.png`, `00086.png`
- **L09** (3): `out/PAR/L09/frames/00023.png`, `00027.png`, `00087.png`
- **L10** (4): `out/PAR/L10/frames/00024.png`, `00033.png`, `00074.png`, `00089.png`
- **L11** (3): `out/PAR/L11/frames/00019.png`, `00026.png`, `00082.png`
- **L12** (3): `out/PAR/L12/frames/00019.png`, `00048.png`, `00064.png`
- **L13** (5): `out/PAR/L13/frames/00017.png`, `00024.png`, `00102.png`, `00118.png`, `00124.png`

### Mã đã chạy / số đã tính lại
- `lv.py lint` cho 14 tệp `lessons/par/L*.yaml`: **14/14 PASS** (chạy mọi `checks:` trong 14 bài bằng SymPy/NumPy/`checklib`, 0 FAIL, 0 WARN).
- `audit/par/verify_par.py`: **96/96 PASS** (kiểm độc lập mô phỏng từng bước, vét cạn hoán vị/xen kẽ, phân số chính xác, `numpy` đối chứng).
- `labs/PAR/L00..L13/loi_giai.py`: **14/14 chạy thật** qua `D:\research-video\.venv\Scripts\python.exe` và đối chiếu khớp 100% từng ký tự với `mong_doi.txt` (không dùng `bash.exe`/`cham.sh`).

---

## 6. Người học kẹt ở đâu (nếu mất gốc, chỉ xem video + bài trước trong `PAR`)

- **L00**: Thân bài không kẹt (chỉ chú thích nhỏ `s` = giây ở `intuition.0`); tới `practice.1` (`p = 0.90 ... :.2f`) và `labs/PAR/L00/de.md` bị kẹt vì không biết cú pháp Python, format `stdout` (`amdahl_16=...`), và lệnh `bash`.
- **L01**: Thân bài không kẹt (chỉ `s` ở `intuition.0`); kẹt tại `practice.1` (`s, N = 0.10, 16`) và `de.md` thiếu format `gustafson_16=14.50x`.
- **L02**: Thân bài kẹt nhẹ ở `formula.1` (`Lemma 2 của Brent` chưa dịch "Bổ đề"); kẹt nặng ở `practice.1` (`T1, Tinf, P = ...`) và `de.md` (`Work-Span`, `T_inf`, thiếu format `work=...`).
- **L03**: Thân bài kẹt nhẹ ở `quiz.2` (từ `từng bit` chưa giảng); kẹt nặng ở `practice.1` (`r1 = c; r2 = c # ...`) và `de.md` thiếu format `racy_final=...`.
- **L04**: Thân bài kẹt nhẹ ở `pitfalls.0` (`mi li giây` chưa giải thích); kẹt nặng ở `practice.1` (`jobs[:4]`, `0 if l[0] <= l[1] else 1`, `+=`) và `de.md` (`makespan`, `LPT`, thiếu format `static_makespan=...`).
- **L05**: Thân bài kẹt ở `hook.0`/`prereq.0` (chưa giảng `byte`) và `pitfalls.3` (`8 MB`); kẹt nặng ở `practice.1` (`64 // 8`) và `de.md` (`False Sharing`, `cache line 64B`, thiếu format).
- **L06**: Thân bài kẹt ở `pitfalls.2` (`20 GB/s`); kẹt nặng ở `practice.1` (`n // lanes`, `n % lanes`) và `de.md` (`SIMD`, `float32`, thiếu format).
- **L07**: Thân bài kẹt ở `check.0` (`ms` trên bảng không ghi = mi li giây); kẹt nặng ở `practice.1` (`10e12`, `:.1f`) và `de.md` (`TF/s`, `TB/s`, `FLOP/byte`, `arithmetic intensity`, thiếu format).
- **L08**: Thân bài kẹt ở `hook.0` (`ms` trên bảng); kẹt nặng ở `practice.1` (`;`, `:.0f`) và `de.md` (`Warp`, thiếu số 32 luồng và format `warp_eff_diverged=...`).
- **L09**: Thân bài kẹt ở `hook.0` (`GB/s` trên bảng); kẹt nặng ở `practice.1` (`n**3`, `//`) và `de.md` (`^`, `vs`, thiếu format).
- **L10**: Thân bài kẹt ở `hook.0` (`GB`, `GB/s`) và `pitfalls.0` (`ms`); kẹt nặng ở `practice.1` (`:.2f`) và `de.md` thiếu format `ring_allreduce_sent_GB=...`.
- **L11**: Thân bài không kẹt ở thân bài (ngoại trừ nhắc `bit` ở `pitfalls.3`); kẹt ở `practice.1` (`:.1f`) và `de.md` thiếu format `seq_eff=...`.
- **L12**: Thân bài không kẹt; kẹt ở `practice.1` (`:.2f`), `de.md` (`pipeline nạp`, thiếu format `speedup_25pct_serial=...`) và con số `5%` khác `2%` của ví dụ.
- **L13**: Thân bài kẹt nhẹ ở `stage5.1` (`(NCCL)`, `(Tensor Fusion)`); kẹt ở `practice.1` (`:.2f`) và `de.md` thiếu format `gpu_vs_cpu_2005=...`.
