# Kiểm định độc lập Stage 10 khoá `SEP` (`L00–L11`, 12 bài) — KẾT LUẬN: **NO-GO**

## 1. Bảng tóm tắt
| Hạng mục | Kết quả | Chi tiết |
|---|---|---|
| Bài `MUST = 0` | **0/12** | Cả 12 bài đều dính lỗi `MUST` (lộ `loi_giai` trước `pause`, `de.md` thiếu format stdout, `P1` chặt, `covers:` lệch, thiếu `<p class="note"><b>Hai mức quy mô:</b>` ở `recap`; riêng L07/L08/L09/L11 thêm lỗi nội dung/logic lab) |
| Bài `P1 = 2` (chuẩn chặt gồm `practice#0` + `de.md`) | **0/12** | 12/12 bài `P1 = 0` (thân bài giảng nền tốt nhưng `practice#0` bỏ sót cú pháp Python ở `practice#1`, và `de.md` dùng thuật ngữ/lệnh chưa giảng) |
| Bài `P8 = 2` | **0/12** | 12/12 bài `P8 = 0` (lộ `loi_giai.py` ở `practice#1` và `mong_doi.txt` ở `practice#2` **trước** `pause: 30` ở `practice#3`; dùng lại y nguyên số ví dụ; `de.md` thiếu format stdout nên không tự đứng được) |
| `spec_sha256 == lv.spec_digest` | **12/12** | Khớp 100% ở `out/SEP/L00..L11/build_report.json` |
| `tts_sha256 == lv.tts_digest` | **12/12** | Khớp 100% ở `out/SEP/L00..L11/build_report.json` |
| `out/SEP/L*/L*.srt == say` | **12/12** | Khớp từng câu 100% (tổng 1.189 câu trên 12 bài) |
| `labs/SEP/L*/loi_giai.py == mong_doi.txt` | **12/12** | Chạy trực tiếp `.venv/Scripts/python.exe` trên cả 12 bài đều exit 0 và khớp `mong_doi.txt` |
| `lv.py lint` | **12/12** | 0 FAIL, 0 WARN trên cả 12 tệp YAML |
| `audit/sep/verify_sep.py` | **71/71 PASS** | Toàn bộ phép kiểm độc lập đều PASS |
| `out/SEP/L*/asr_report.md` | **12/12 sạch hàng đợi** | `thiếu audio: 0` và `chưa xem xét: 0` ở cả 12 bài (nhưng các câu gắn cờ trong `asr_reviewed` đều ghi `NOT_VERIFIED bằng tai người`) |
| `audit/layout_SEP.tsv` | **Trống (2 byte)** | Chỉ có `\r\n`, không có dòng cảnh báo layout |
| `audit/review/screen_code/SEP.yaml` | **36 khối** | `L00..L11` × `practice {1,2,4}` khớp hash hiện tại, xác nhận `practice#1/#2` đang in đúng `loi_giai.py` và `mong_doi.txt` trước `pause` |
| Ký hiệu toán thô trong `say` | **0/12** | Không phát hiện ký hiệu toán thô (`×, ÷, ≤, ≥, =, *, /...`) trong `say` |
| Câu `say` chứa `"càng "` | **3 câu** | `L00` (`check#1`), `L07` (`formula#1`), `L09` (`formula#1`) |
| `SHOULD` | **5 nhóm vấn đề** | `asr_reviewed` `NOT_VERIFIED bằng tai người`; `P9` thiếu biểu đồ SVG hai quy mô ở 10/12 bài và thiếu đa quy mô ở `L02/L03/L08`; một vài con số làm tròn trong `L11 stage2` |

---

## 2. Phát hiện chi tiết (`MUST` / `SHOULD` / `INFO`)

### MUST (Chặn phát hành)
1. **Cả 12 bài (`L00–L11`) — Lộ toàn bộ `loi_giai.py` và `mong_doi.txt` TRƯỚC `pause: 30` (`P8 = 0`, `CONFIRMED`)**
   - **Cảnh/step**: `practice#1` (`step[1]`, `pause=0`) và `practice#2` (`step[2]`, `pause=0`) đứng **trước** `practice#3` (`step[3]`, `pause: 30` — `"Hãy bấm tạm dừng và tự làm trước"`).
   - **Trích nguyên chữ**: Ví dụ `L00` `practice#1`: `Cài đặt kiểm chứng SEP:L00 bằng Python / users = 1_000_000 / affected = int(users * 0.01) / print(f"affected_1pct={affected}")`; `practice#2`: `Đầu ra chạy thật (1 dòng) / affected_1pct=10000`. Mô-típ y hệt lặp ở toàn bộ `L00–L11`.
   - **Đề xuất sửa**: Đưa bài tập tự làm (`de.md` + `pause`) lên trước khi hiện lời giải, hoặc tách lab thành đề bài độc lập có số liệu mới so với ví dụ trên lớp và chỉ hiện mã kiểm chứng sau `pause` (hoặc kiểm chứng cho ví dụ thân bài, còn lab dùng bộ số mới).

2. **Cả 12 bài (`L00–L11`) — `labs/SEP/L*/de.md` thiếu format `stdout` và không tự đứng được (`P8 = 0`, `CONFIRMED`)**
   - **Tệp**: `labs/SEP/L00..L11/de.md`.
   - **Bằng chứng**: Không một `de.md` nào ghi định dạng dòng xuất (tên khoá `affected_1pct=...`, `combos=... prob_unique_10k=...`, `ppv_A=...`, `score=... pass=...`, số chữ số thập phân `:.1f/.2f/.3f/.0f`). Ngoài ra `L02, L03, L04, L08, L10` không nêu đầy đủ biến/danh sách đầu vào (vd `L04/de.md` không liệt kê `('lib1','MIT'), ('lib2','Apache-2.0'), ('lib3','GPL-3.0')`; `L08/de.md` không cho ma trận điểm `X, Y, Z`). Đồng thời cả 12 `loi_giai.py` đều dùng lại y hệt số của ví dụ chính và 4 bài (`L02, L03, L05, L10`) gán cứng cờ kết quả (`mismatch=1`, `pass=0`, `stop_catastrophic_A=1`, `pinned_lockfile_safe=1`).
   - **Đề xuất sửa**: Bổ sung vào mỗi `de.md` đầy đủ đầu vào, yêu cầu tính với bộ số mới khác ví dụ thân bài, và mục **Định dạng đầu ra (stdout)** khớp từng ký tự với `mong_doi.txt`.

3. **L08 (`practice#1,#2,#4`, `labs/SEP/L08/loi_giai.py`, `mong_doi.txt`) — Logic mã lab mâu thuẫn với nội dung bài giảng (`CONFIRMED`)**
   - **Trích nguyên chữ**: Trong thân bài `L08` (`example`), ba phương án là `X=[2,2,2,-2]`, `Y=[1,1,1,0]`, `Z=[0,1,1,1]`, hoà tổng 3 nên áp bước 3 ưu tiên bên yếu thế → chọn **`Z`**. Nhưng `practice#1` và `labs/SEP/L08/loi_giai.py` viết: `plans = {'X': [2,2,2,-2], 'Y': [1,1,1,0], 'Z': [-1,2,2,1]}` → `min_scores={'X': -2, 'Y': 0, 'Z': -1} fair_pick=Y`.
   - **Vì sao sai**: Tự ý đổi `Z` thành `[-1,2,2,1]` làm `Z` bị loại ngay ở bước 1 (`min < 0`), bỏ qua hoàn toàn bước 3 (ưu tiên bên yếu thế) là trọng tâm của `L08`, và gây mâu thuẫn trực tiếp với đáp án `Z` trong chính video bài 8.
   - **Đề xuất sửa**: Đưa `Z` về `[0, 1, 1, 1]` và khoá sắp xếp phải xét `(min(v) >= 0, sum(v), v[3])` để chọn đúng `Z` theo luật 3 bước của bài (hoặc cho dữ liệu riêng có ghi rõ trong `de.md`).

4. **L09 (`practice#1,#3`, `labs/SEP/L09/de.md`, `loi_giai.py`) — Dùng thuật ngữ & ký hiệu chưa giảng và trái `sources_L09.md` (`CONFIRMED`)**
   - **Trích nguyên chữ**: `L09/de.md` & `practice#3`: `# Lab SEP L09 — Ước lượng ba điểm PERT: (O + 4M + P)/6 cho (2, 4, 12 ngày)` và `loi_giai.py`: `o, m, p = 2.0, 4.0, 12.0 / pert = (o + 4*m + p) / 6.0`.
   - **Vì sao sai**: Toàn bộ thân bài `L09` dùng ký hiệu **`E = (O + 4M + B)/6`** (`B` = bi quan), hoàn toàn không có chữ `PERT` hay `P`; chính `audit/sep/sources_L09.md` mục *"Điều KHÔNG dạy"* ghi rõ: *"Không gán phương pháp ba điểm cho một chương trình hay năm cụ thể"*.
   - **Đề xuất sửa**: Đổi `de.md`, `practice#3` và biến trong `loi_giai.py` về đúng ký hiệu `(O + 4M + B)/6` (`E`, `B`) như thân bài.

5. **L07 (`labs/SEP/L07/de.md`, `practice#3`) — Diễn đạt sai bản chất chính sách 90+30 (`CONFIRMED`)**
   - **Trích nguyên chữ**: `L07/de.md` & `practice#3`: `Công bố lỗ hổng có phối hợp: hạn chót 90 ngày + gia hạn 14/30 ngày`.
   - **Vì sao sai**: Trong chính sách Project Zero (`L07 policy`), **14 ngày** là thời gian ân hạn ("grace period"), còn **30 ngày** KHÔNG phải là "gia hạn" hạn chót 90 ngày mà là thời gian chờ sau khi đã có bản vá trước khi công bố chi tiết (`v + 30`). Gộp thành `"gia hạn 14/30 ngày"` là sai kiến thức bài vừa dạy.
   - **Đề xuất sửa**: Sửa thành `"hạn vá 90 ngày (ân hạn 14 ngày), công bố 30 ngày sau bản vá"`.

6. **L11 (`labs/SEP/L11/de.md`) — Phép tính thiếu thừa số và dùng từ chưa giảng (`CONFIRMED`)**
   - **Trích nguyên chữ**: `L11/de.md`: `Tính số tổ hợp 2 * 100000 (hoặc 2 * 5 zips * 365 * 100 = 365 000) so với 54 805 cử tri Cambridge.`
   - **Vì sao sai**: `2 * 100000` thiếu `× 365 × 100` (nếu tính đủ 100.000 mã bưu chính 5 số phải là `2 × 100 000 × 365 × 100 = 7,3 tỉ`, không thể đặt ngang hàng với `365 000`). Ngoài ra bài `L11` dùng `"mã bưu chính 5 số"` và `"một danh sách cử tri"`, không dùng `"zips"` hay `"Cambridge"`.
   - **Đề xuất sửa**: Sửa `de.md` thành `2 * 5 * 365 * 100 = 365 000 tổ hợp (2 giới tính × 5 mã bưu chính × 365 ngày × 100 năm) so với 54 805 cử tri`.

7. **Cả 12 bài (`L00–L11`) — `covers:` rập khuôn, trỏ sai cảnh dạy mục tiêu (`CONFIRMED`)**
   - **Bằng chứng**: Tất cả bài 4 mục tiêu (`L00–L05, L10`) đều gán cứng `[example, check, check, practice]`; tất cả bài 3 mục tiêu (`L06–L09`) đều gán cứng `[example, check, practice]`; `L11` gán `[stage1, stage2, stage3, practice]`. Hệ quả là hàng loạt mục tiêu trỏ vào cảnh không dạy nó:
     - `L00`: obj 1 (bên liên quan) → `example` (không nhắc bên liên quan; dạy ở `intuition`/`tool`); obj 3 (bộ quy tắc) → `check` (dạy ở `code`/`tool`); obj 4 (phát hành dần) → `practice` (dạy ở `tool`/`quiz`).
     - `L01`: obj 2 (xoá tên ≠ khử nhận dạng, mã hoá vẫn là DLCN) → `check` (không nhắc mã hoá; dạy ở `law`/`pitfalls`); obj 3 (thu tối thiểu, mục đích, thời hạn) → `check` (dạy ở `law`/`pitfalls`); obj 4 (chọn thuộc tính chia sẻ) → `practice` (dạy ở `example`/`quiz`).
     - `L02`: obj 2 → `check` (suy ra ở `formula`); obj 3 → `check` (dạy ở `criteria`/`formula`); obj 4 → `practice` (dạy ở `pitfalls#2`/`quiz`).
     - `L03`: obj 2 (thuộc tính đổi được) → `check` (dạy ở `pitfalls#1`/`quiz`); obj 3 (mô hình xấp xỉ sai) → `check` (dạy ở `pitfalls#0`); obj 4 (ghi nhật ký) → `practice` (dạy ở `log`/`pitfalls#2`).
     - `L04`: obj 2 (phụ thuộc gián tiếp) → `check` (dạy ở `prereq`/`formula`/`pitfalls#2`); obj 3 (không ghi giấy phép) → `check` (dạy ở `prereq`/`pitfalls#0`); obj 4 (thay/giữ/mở) → `practice` (dạy ở `example`/`quiz`).
     - `L05`: obj 2 → `check` (suy ra ở `formula`); obj 3 (không đảo ngược được) → `check` (dạy ở `stop`/`pitfalls#1`); obj 4 (khi nào dừng) → `practice` (dạy ở `code`/`stop`/`quiz`).
     - `L06`: obj 3 (huấn luyện vs phục vụ vòng đời) → `practice` (không nhắc phục vụ; dạy ở `serving`/`pitfalls#2`).
     - `L07`: obj 1 (quy trình báo riêng/chờ vá) → `example` (dạy ở `sym`/`policy`); obj 2 (năm nhuận & khai thác thật) → `check` (không có năm nhuận/khai thác; dạy ở `example`/`pitfalls#3`/`quiz`); obj 3 (cân hai rủi ro) → `practice` (dạy ở `pitfalls`/`quiz`/`recap`).
     - `L08`: obj 1 (lập bảng có khả năng lên tiếng & vắng mặt) → `example` (dạy ở `intuition`/`pitfalls#0`); obj 3 (tổng che tác hại) → `practice` (dạy ở `check#1`/`pitfalls#1`).
     - `L09`: obj 1 (nhiều việc) → `example` (nhiều việc ở `pitfalls#1`); obj 2 (cam kết theo khoảng) → `check` (dạy ở `concept`/`example`/`quiz`); obj 3 (nói "chưa được") → `practice` (dạy ở `say_no`/`pitfalls#2`).
     - `L10`: obj 3 (trách nhiệm 3 bên) → `check` (dạy ở `duty`); obj 4 (gỡ gói & giữ bản dựng) → `practice` (dạy ở `duty`/`pitfalls#3`/`quiz`).
     - `L11`: obj 1 (5 chặng) → `stage1` (dạy ở `intuition` + `stage1..5`); obj 2 (con số cả 5 chặng) → `stage2` (ở `stage1..5` + `check`); obj 3 (tra luật) → `stage3` (dạy ở `lookup`); obj 4 (chọn việc ở quy mô mình) → `practice` (dạy ở `quiz`).
   - **Đề xuất sửa**: Cập nhật `covers:` từng bài trỏ đúng cảnh (hoặc danh sách cảnh) thật sự giảng mục tiêu tương ứng.

8. **Cả 12 bài (`L00–L11`) — Thiếu `<p class="note"><b>Hai mức quy mô:</b> ...` trong `recap` (`P9`, `CONFIRMED`)**
   - **Bằng chứng**: Kiểm tra toàn bộ `scenes[id=recap]` của cả 12 bài: **0/12 bài** có thẻ `<p class="note"><b>Hai mức quy mô:</b> ...`.
   - **Đề xuất sửa**: Bổ sung ở `recap` mỗi bài dòng `<p class="note"><b>Hai mức quy mô:</b> ...` tóm tắt sự thay đổi ở hai mức quy mô/thời gian và đánh đổi kèm theo (riêng `L02, L03, L08` cần bổ sung thêm so sánh quy mô vào thân bài + SVG).

9. **Cả 12 bài (`L00–L11`) — Không đạt chuẩn `P1` chặt (`0/12`, `CONFIRMED`)**
   - Xem chi tiết từng mục ở Mục 3 bên dưới. Nguyên nhân chính là bảng `practice#0` dùng mẫu chung sơ sài (thừa `f"{val:.3f}"` ở 10/12 bài không dùng `.3f`, nhưng lại thiếu hàng loạt cú pháp Python xuất hiện ngay ở `practice#1`), cộng với các lệnh/từ chưa giảng trong `labs/SEP/L*/de.md`.

### SHOULD (Nên sửa / kiểm tra thêm)
1. **Kiểm thính ASR bằng tai người (`L00, L01, L03, L04, L05, L06, L08, L09`)**: Tuy `asr_report.md` ghi `chưa xem xét: 0`, toàn bộ 15 câu bị gắn cờ (vd `L00` `"tắc dùng"→"tác dụng"`, `"rủi ro tuỳ"→"đuổi do tuy"`; `L01` `"ghi rõ, gộp, ngày"→"di trỏ, gục, ngay"`, `"c"→"sẽ"`; `L05` `"chia e"→"GE"`; `L06` `"c"→"sẽ"`; `L08` `"X, Z, D"→"ít, Jack, Vê"`; `L09` `"e... gộp"→"gục"`) đều ghi `NOT_VERIFIED bằng tai người`. Nên nghe kiểm âm thanh thật hoặc đặt tên chữ cái/cụm từ dễ nghe hơn.
2. **Câu chứa `"càng "` (`L00, L07, L09`)**:
   - `L00 check#1`: `"Lỗi càng hiếm thì 1 trừ p càng gần 1, nên thử ít người gần như chắc chắn không thấy gì, nhưng n nhân p vẫn lớn khi số người dùng lớn."`
   - `L07 formula#1`: `"Nhận xét, vá càng muộn thì ngày công bố càng muộn."` (cần điều kiện `v ≤ 90`; nếu không vá kịp thì công bố ngay ngày 90 — sớm hơn `83+30=113`!).
   - `L09 formula#1`: `"Vì khoảng từ lạc quan tới bi quan càng rộng thì ước lượng càng kém chắc, cách ước lượng này lấy một phần sáu khoảng đó, s bằng B trừ O, chia 6."`
3. **`L02, L03, L08` thiếu so sánh hai mức quy mô hệ thống & đánh đổi trong thân bài/SVG (`P9`)**: `L02` cố định 100 người/nhóm (chỉ nhắc nhóm 20 người thoáng qua ở Lỗi 4), `L03` chỉ xét 1 hồ sơ đơn lẻ, `L08` chỉ thêm 1 cột ở Lỗi 1. Ngoài ra chỉ `L05` và `L11` có SVG thể hiện trục quy mô/thời gian; 10 bài còn lại SVG chưa vẽ 2 mức quy mô.
4. **`L11 stage2#1` làm tròn trung gian**: `(1 - 1/8000)**4999 = 0.53533... ≈ 0.54`, màn hình ghi `≈ 0,54 — khoảng 2677 người` (`5000 × 0,53533 ≈ 2677`, nếu nhân từ số làm tròn `0,54` sẽ ra `2700` — dễ khiến người học bấm máy ra khác 23 người nếu không nói lấy giá trị chưa làm tròn).
5. **`L01 quiz#2`**: Dùng từ `"nghị định"` (`"tra toàn văn luật và nghị định hiện hành"`) khi chưa giảng khái niệm nghị định ở `L01` (tới `L11` mới giảng).

### INFO
- `curriculum/sep.yaml` khớp 100% `title` và `objectives` với cả 12 đặc tả `lessons/sep/L*.yaml`.
- Dữ kiện lịch sử và pháp lý trong `L00–L11` đều đối chiếu nguyên văn với `audit/sep/sources_L00..L11.md`; mọi số tự dựng đều ghi rõ `"số minh hoạ"`.
- Hình ảnh render trên toàn bộ **37 khung PNG** đã mở đọc trực tiếp đều sắc nét, không đè chữ, không tràn viền, không cắt khung, công thức KaTeX sạch (chỉ lưu ý rất nhỏ ở `L03/00030.png`: nhãn `"số năm: 0 → 10"` nằm sát mép trên vùng vẽ nhưng không bị cắt).

---

## 3. Chấm chặt `P1` — Liệt kê từng mục chưa giảng

| Bài | Cảnh / step / tệp | Trích chữ chưa giảng | Bảng cách đọc có phủ không? | Ghi chú |
|---|---|---|---|---|
| **L00** | `practice#1` | `1_000_000`, `int(...)`, `=`, `*`, `f"...{affected}"` (không có `:.3f`) | **Không** | `practice#0` chỉ có `f"{val:.3f}"` và `print(...)`; dùng thừa `.3f` |
| **L00** | `labs/SEP/L00/de.md` | `bash labs/cham.sh SEP L00 duong_dan/bai_cua_ban.py` | **Không** | Chưa giảng `bash` / đường dẫn lệnh chấm trong thân bài |
| **L01** | `quiz#2` | `nghị định` (`tra toàn văn luật và nghị định hiện hành`) | — | Thuật ngữ pháp lý chưa giảng ở L01 (tới L11 mới giảng) |
| **L01** | `practice#1` | `=`, `*`, `/`, `f"...{combos}..."` (chèn nhiều biến, biến nguyên không `:.3f`) | **Không** | `practice#0` có `import`, `math.exp`, `:.3f`, `print`, thiếu `=`, `*`, `/` |
| **L01** | `labs/SEP/L01/de.md` | `(365 * 80 * 2)`, `bash labs/cham.sh ...` | **Không** | Toán tử `*` trong mã & lệnh `bash` chưa giảng |
| **L02** | `practice#1` | `ppv = ...` (gán hàm), `ppv(0.5)` (gọi hàm), `*`, `/` | **Không** | `practice#0` có `lambda x: ...` nhưng không giảng gán tên hàm & gọi hàm |
| **L02** | `labs/SEP/L02/de.md` | `bash labs/cham.sh ...` | **Không** | Lệnh `bash` chưa giảng; còn `TPR, FPR, PPV` đã giảng ở `L02 sym` |
| **L03** | `practice#1` | `=`, `*`, `/`, `:.1f` (làm tròn 1 chữ số) | **Không** | `practice#0` chỉ ghi `f"{val:.3f}"`, không phủ `:.1f`, `=`, `*`, `/` |
| **L03** | `labs/SEP/L03/de.md` | `score = 0.5*income + 2*years`, `bash labs/cham.sh ...` | **Không** | Từ tiếng Anh `score, income, years`, dấu `*` trong mã & `bash` chưa giảng |
| **L04** | `practice#1` | `[('lib1', 'MIT'), ...]` (tuple `(...)`, chuỗi `'...'`), `for n, lic in deps if lic.startswith('GPL')` (gỡ 2 biến, `if`, `.startswith`) | **Không** | `practice#0` chỉ ghi `[f(x) for x in xs]`, không phủ tuple, `if`, `.startswith`, biến chuỗi |
| **L04** | `labs/SEP/L04/de.md` | `bash labs/cham.sh ...` | **Không** | Lệnh `bash` chưa giảng |
| **L05** | `practice#1` | `1_000_000`, `1_000`, `:.0f`, `=`, `*` | **Không** | `practice#0` chỉ ghi `f"{val:.3f}"` (thừa) và `print(...)` |
| **L05** | `labs/SEP/L05/de.md` | `bash labs/cham.sh ...` | **Không** | Lệnh `bash` chưa giảng |
| **L06** | `practice#1` | `:.1f`, `=`, `*` | **Không** | `practice#0` chỉ ghi `f"{val:.3f}"` (thừa) và `print(...)` |
| **L06** | `labs/SEP/L06/de.md` | `CO2`, `CO2/kWh`, `bash labs/cham.sh ...` | **Không** | `L06` dùng `CO₂`, chưa giảng ký hiệu `CO2/kWh` dạng ASCII & `bash` |
| **L07** | `practice#1` | `import datetime as dt` (`as`), `dt.date(...)`, `dt.timedelta(days=90)`, `{d0}` | **Không** | `practice#0` chỉ ghi `import thu_vien` và `:.3f` (thừa), thiếu `as`, `date`, `timedelta` |
| **L07** | `labs/SEP/L07/de.md` | `datetime.date`, `gia hạn 14/30 ngày`, `bash labs/cham.sh ...` | **Không** | `datetime.date` và `bash` chưa giảng; `"gia hạn 14/30 ngày"` sai nghĩa |
| **L08** | `practice#1` | `{'X': [...]}` (dict `{}`), `plans[k]`, `key=lambda ...`, `(min(...), sum(...))`, `{k:min(v) for k,v in plans.items()}` | **Không** | `practice#0` thiếu dict, truy cập khoá, `key=`, `.items()`, dict comprehension |
| **L08** | `labs/SEP/L08/de.md` | `bash labs/cham.sh ...` | **Không** | Lệnh `bash` chưa giảng |
| **L09** | `practice#1` | `o, m, p = 2.0, 4.0, 12.0` (gán nhiều biến, biến `p`), `:.1f`, `:.2f`, `*`, `/` | **Không** | `practice#0` chỉ ghi `f"{val:.3f}"` (thừa) và `print(...)` |
| **L09** | `labs/SEP/L09/de.md` | `PERT`, `(O + 4M + P)/6`, `bash labs/cham.sh ...` | **Không** | `PERT` và `P` không tồn tại trong bài giảng `L09` (chỉ có `E` và `B`) |
| **L10** | `practice#1` | `=`, `+`, `{removed}` (không `.3f`) | **Không** | `practice#0` chỉ ghi `f"{val:.3f}"` (thừa) và `print(...)` |
| **L10** | `labs/SEP/L10/de.md` | `băm`, `lockfile`, `bash labs/cham.sh ...` | **Không** | Bài `L10` gọi là `"tệp khoá phiên bản"`, không hề giảng `"băm"` hay `"lockfile"` |
| **L11** | `stage5#0` | `Điều 21`, `khoản 2 Điều 33` | — | Chỉ nêu số điều không giải thích nội dung (tuy `sources_L11.md` ghi chú giữ nguyên văn) |
| **L11** | `practice#1` | `54_805`, `:.2f`, `=`, `*`, `/` | **Không** | `practice#0` chỉ ghi `f"{val:.3f}"` (thừa) và `print(...)` |
| **L11** | `labs/SEP/L11/de.md` | `zips`, `Cambridge`, `bash labs/cham.sh ...` | **Không** | Bài `L11` không dùng từ `"zips"` hay tên `"Cambridge"` |

---

## 4. Bảng độ sâu (`L00–L11`)

| Bài | sha16 lúc đọc | Phút | P1 | P2 | P3 | P4 | P5 | P6 | P7 | Tổng | Mất gốc | P8 | P9 | Chỗ thiếu chính | Cần biết trước |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| L00 | `76d835e664de8f60` | 11.6 | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | GẦN (do P1=0) | 0 | 1 | `P1`: `practice#0` sót `1_000_000, int, =, *`, `de.md` có `bash`; `P7`: `covers:` trỏ sai; `P8`: lộ code trước `pause`, thiếu format stdout; `P9`: thiếu note recap & SVG 2 quy mô | Cú pháp Python cơ bản (`=`, `*`, `int`, `1_000_000`), lệnh `bash` |
| L01 | `b4cf5e192f1e044d` | 11.6 | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | GẦN (do P1=0) | 0 | 1 | `P1`: `quiz#2` `"nghị định"`, `practice#0` sót `=, *, /`, `de.md` có `*, bash`; `P7`: `covers:` trỏ sai; `P8`: lộ code trước `pause`, thiếu format stdout; `P9`: thiếu note recap & SVG 2 quy mô | Python cơ bản (`=`, `*`, `/`), `"nghị định"`, `bash` |
| L02 | `649cec730756fcf3` | 11.7 | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | GẦN (do P1=0) | 0 | 1 | `P1`: `practice#0` không giảng gán/gọi hàm `ppv(0.5)`, `de.md` có `bash`; `P7`: `covers:` trỏ sai; `P8`: lộ code trước `pause`, thiếu input & format stdout; `P9`: thân bài cố định 100 người, thiếu note recap | Gán/gọi hàm Python, `bash` |
| L03 | `2fb32bb6e0b6da07` | 10.8 | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | GẦN (do P1=0) | 0 | 0 | `P1`: `practice#0` thiếu `:.1f, =, *, /`, `de.md` có `score/income/years, bash`; `P7`: `covers:` trỏ sai; `P8`: lộ code, thiếu format stdout; `P9`: chỉ xét 1 hồ sơ, không có 2 quy mô, thiếu note recap | Tiếng Anh `score/income/years`, Python `:.1f, =, *, /`, `bash` |
| L04 | `5daa43fcb6e26062` | 11.5 | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | GẦN (do P1=0) | 0 | 1 | `P1`: `practice#0` thiếu tuple, `if`, `.startswith`, `de.md` có `bash`; `P7`: `covers:` trỏ sai; `P8`: lộ code, `de.md` thiếu danh sách `deps` & format stdout; `P9`: thiếu note recap & SVG 2 quy mô | Tuple, chuỗi, `.startswith()` trong Python, `bash` |
| L05 | `67146a3c082e8392` | 11.0 | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | GẦN (do P1=0) | 0 | 1 | `P1`: `practice#0` thiếu `1_000_000, :.0f, =, *`, `de.md` có `bash`; `P7`: `covers:` trỏ sai; `P8`: lộ code, gán cứng `stop_catastrophic_A=1`, thiếu format stdout; `P9`: thân bài & SVG tốt nhưng thiếu note recap | Python `1_000_000, :.0f, =, *`, `bash` |
| L06 | `e655e017886eeaa0` | 11.5 | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | GẦN (do P1=0) | 0 | 1 | `P1`: `practice#0` thiếu `:.1f, =, *`, `de.md` có `CO2/kWh, bash`; `P7`: `covers:` obj 3 trỏ `practice`; `P8`: lộ code, thiếu format stdout; `P9`: thiếu note recap & SVG 2 quy mô | Python `:.1f, =, *`, `CO2/kWh`, `bash` |
| L07 | `f964f4cc5898fe8f` | 10.7 | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | GẦN (do P1=0) | 0 | 1 | `P1`: `practice#0` thiếu `as, dt.date, dt.timedelta`, `de.md` có `datetime.date, bash`; `P7`: `covers:` trỏ sai; `P8`: lộ code, `de.md` sai `"gia hạn 14/30 ngày"`, thiếu format stdout; `P9`: thiếu note recap | `datetime.date`, `timedelta`, `as` trong Python, `bash` |
| L08 | `4ec3b6e712cbb98b` | 9.5 | 0 | 2 | 2 | 2 | 2 | 2 | 0 | 10 | GẦN (do P1=0) | 0 | 1 | `P1`: `practice#0` thiếu `dict {}, [k], key=, .items()`; `P7`: `covers:` trỏ sai & `practice` mâu thuẫn thân bài (`Y` vs `Z`); `P8`: lộ code, đổi `Z` thành `[-1,2,2,1]`, thiếu ma trận & format stdout; `P9`: thiếu đa quy mô & note recap | `dict`, `.items()`, `key=lambda`, dict comprehension, `bash` |
| L09 | `2e23f12aa47ff471` | 11.2 | 0 | 2 | 2 | 2 | 2 | 2 | 0 | 10 | GẦN (do P1=0) | 0 | 1 | `P1`: `practice#0` thiếu đa biến `o,m,p`, `:.1f, :.2f`, `de.md` có `PERT, P`; `P7`: `covers:` trỏ sai & `de.md` sai ký hiệu `PERT/P` so với `E/B` của bài; `P8`: lộ code, thiếu format stdout; `P9`: thiếu note recap & SVG 2 quy mô | Gán nhiều biến Python, `:.1f/.2f`, `PERT`, `P`, `bash` |
| L10 | `0c5b50af22c2f1f7` | 11.1 | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | GẦN (do P1=0) | 0 | 1 | `P1`: `practice#0` thiếu `=, +`, `de.md` có `băm lockfile, bash`; `P7`: `covers:` trỏ sai; `P8`: lộ code, gán cứng `pinned_lockfile_safe=1`, thiếu dữ kiện & format stdout; `P9`: thiếu note recap & SVG 2 quy mô | Python `=, +`, `"băm"`, `"lockfile"`, `bash` |
| L11 | `af84608cbdbea123` | 16.9 | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | GẦN (do P1=0) | 0 | 1 | `P1`: `practice#0` thiếu `54_805, :.2f, =, *, /`, `de.md` có `zips, Cambridge, bash`; `P7`: `covers:` trỏ sai; `P8`: lộ code, `de.md` ghi sai `2 * 100000`, thiếu format stdout; `P9`: thân bài & SVG 5 chặng tốt nhưng thiếu note recap | Python `54_805, :.2f, =, *, /`, `zips`, `Cambridge`, `bash` |

*(Ghi chú: ở thân bài lý thuyết/trực giác/ví dụ/tự kiểm của cả 12 bài, chất lượng giảng P2–P6 rất tốt [đạt 2/2]; điểm mất gốc rơi xuống `GẦN` hoàn toàn do `P1 = 0` khi chấm chặt cả `practice#0`, `practice#1`, `de.md`, cùng lỗi `covers:`/`practice`/`de.md`/`recap` ở `P7, P8, P9`.)*

---

## 5. Khung hình PNG đã xem (37 khung)
- `L00`: `00030.png`, `00044.png`, `00088.png`
- `L01`: `00033.png`, `00047.png`, `00090.png`
- `L02`: `00028.png`, `00036.png`, `00087.png`
- `L03`: `00030.png`, `00045.png`, `00086.png`
- `L04`: `00030.png`, `00045.png`, `00083.png`
- `L05`: `00021.png`, `00035.png`, `00080.png`
- `L06`: `00021.png`, `00036.png`, `00082.png`
- `L07`: `00026.png`, `00044.png`, `00077.png`
- `L08`: `00021.png`, `00033.png`, `00073.png`
- `L09`: `00026.png`, `00040.png`, `00097.png`
- `L10`: `00020.png`, `00031.png`, `00080.png`
- `L11`: `00017.png`, `00107.png`, `00117.png`, `00128.png`

---

## 6. Mã đã chạy & số đã tính lại
- `D:\research-video\.venv\Scripts\python.exe -B D:\research-video\tools\lv.py lint <L00..L11>`: **12/12 PASS** (0 FAIL, 0 WARN; tổng 350 PASS).
- `D:\research-video\.venv\Scripts\python.exe -B D:\research-video\audit\sep\verify_sep.py`: **71/71 PASS** (kiểm độc lập lại toàn bộ phép tính, mô phỏng Monte Carlo, beta-PERT, lịch thật).
- `D:\research-video\.venv\Scripts\python.exe -B labs/SEP/L00..L11/loi_giai.py` đối chiếu `mong_doi.txt`: **12/12 exit 0, khớp 100%**.
- Số lượng phép kiểm `checks:` trong YAML đã chạy qua `lint`: L00 (21), L01 (20), L02 (20), L03 (19), L04 (11), L05 (19), L06 (19), L07 (16), L08 (14), L09 (16), L10 (13), L11 (28) — **216/216 phép khớp**.

---

## 7. Người học kẹt ở đâu
- **L00**: `practice#1` (`users = 1_000_000 / affected = int(users * 0.01)`) — người mất gốc chưa từng thấy Python không hiểu dấu `_` trong số, `int(...)`, `=`, `*` và khi mở `de.md` không biết phải in dòng `affected_1pct=10000`.
- **L01**: `quiz#2` (`tra toàn văn luật và nghị định hiện hành`) nhắc `"nghị định"` chưa giải thích; sang `practice#1` & `de.md` không hiểu cú pháp `=`, `*`, `/`, cách gọi `bash labs/cham.sh`, và không có format `combos=... prob_unique_10k=...` trong `de.md`.
- **L02**: `practice#1` (`ppv = lambda b: ...` rồi `ppv(0.5)`) không giải thích cách gọi biến hàm, và `de.md` thiếu định dạng `ppv_A=... ppv_B=... mismatch=1`.
- **L03**: `practice#1` (`:.1f`) & `de.md` (`score = 0.5*income + 2*years`, thiếu format stdout `score=... pass=0 need_extra_years=...`) — người mất gốc kẹt ở từ tiếng Anh và định dạng xuất.
- **L04**: `practice#1` (`deps = [('lib1', 'MIT'), ...]` và `[n for n, lic in deps if lic.startswith('GPL')]`) dùng tuple, unpack 2 biến, `if`, `.startswith()` chưa giảng ở `practice#0`; `de.md` không cho luôn danh sách `deps` và format xuất.
- **L05**: `practice#1` (`1_000_000`, `:.0f`) chưa giảng ở `practice#0`, và `de.md` không nói cách xuất cờ cứng `stop_catastrophic_A=1`.
- **L06**: `practice#1` (`:.1f`, `=`, `*`) chưa giảng ở `practice#0`, và `de.md` không nêu format `kwh=... co2_kg=...`.
- **L07**: `practice#1` (`import datetime as dt`, `dt.date`, `dt.timedelta(days=90)`) hoàn toàn không có trong `practice#0`; `de.md` còn viết `"gia hạn 14/30 ngày"` gây hiểu nhầm quy tắc 90+30 vừa học.
- **L08**: `practice#1` (`plans = {'X': ...}`, `key=lambda`, dict comprehension) không được giảng ở `practice#0`, lại tự đổi `Z` thành `[-1,2,2,1]` ra `fair_pick=Y` khiến người học hoang mang vì thân bài vừa chọn `Z`.
- **L09**: `practice#1` & `de.md` bất ngờ đổi thành `PERT` và `(O + 4M + P)/6` khi toàn bài dùng `E` và `B`, lại không nêu format `pert_days=... sd=...`.
- **L10**: `de.md` dùng thuật ngữ `"khoá băm lockfile"` mà cả bài không hề nhắc tới `"băm"` hay `"lockfile"`, và `de.md` thiếu format `removed_pkgs=273 pinned_lockfile_safe=1`.
- **L11**: `de.md` ghi `"2 * 100000 (hoặc 2 * 5 zips * 365 * 100 = 365 000) so với 54 805 cử tri Cambridge"` khiến người học kẹt ở phép tính thiếu `365 * 100` và từ `"zips"`, `"Cambridge"` không xuất hiện trong bài, cộng thêm `practice#1` thiếu giải thích `54_805` và `:.2f`.
