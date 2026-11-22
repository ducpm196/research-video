# Báo cáo Kiểm định Độc lập Khóa `LLM` (L00–L14, 15 bài) — WP-AF4-5 Stage 9

## 1. Kết luận tổng thể: **`NO-GO`**
Khóa `LLM` đạt 100% các cổng kỹ thuật tự động (`lv.py lint`, `lv.py curriculum`, `verify_llm.py`, `arith_scan.py`, `spec_sha256`/`tts_sha256` STALE=0, `L*.srt == say` 15/15, `asr_report.md` `chưa xem xét: 0` 15/15, `audit/layout_LLM.tsv` 0 lỗi, SVG rõ nét), **nhưng KHÔNG ĐẠT chuẩn sư phạm AF2 (`NO-GO`)** do:
1. **3 lỗi `MUST` nghiêm trọng về tính đúng/nhất quán của Lab (`L01`, `L02`, `L14`)**: `L02` `loi_giai.py` cho kết quả gộp cặp **trái ngược** với bài giảng & `curriculum` & `verify_llm.py`; `L01` `de.md` thiếu ngữ cảnh nên `0.125` trong `loi_giai.py` không suy ra được từ đề; `L14` `de.md` thiếu hẳn yêu cầu thứ hai (`tokens_per_param=20`).
2. **Lỗi `MUST` hệ thống ở toàn bộ cảnh `practice` (`L00..L14`)**: `practice#1` (code) và `practice#2` (stdout) **lộ toàn bộ lời giải `loi_giai.py` và đáp án `mong_doi.txt` TRƯỚC bước `practice#3` (`pause: 30`)**; `de.md` ở cả 15 bài không nêu định dạng chuỗi đầu ra cần in; nhiều bài gán cứng số/đáp số (`L00`, `L01`, `L07`, `L12`) và lặp y nguyên số ví dụ trong thân bài.
3. **Lỗi `MUST`/`SHOULD` ở `covers:` (`14/15` bài)** và **thuật ngữ tiếng Anh chưa chú thích ở `practice#0/#3` + `de.md` (`P1`)** (đặc biệt `L06`, `L07`, `L13` ở mức yếu `0/2`: `loss`, `PPL`, `7B/140B tokens`, `Softmax`, `logits`, `token`, `attention`, `O(L^2)`, `KV cache`, `4k/32k`).

---

## 2. Kết quả cổng kỹ thuật & nhất quán toàn khóa
- **`tools/lv.py lint` (L00–L14)**: `15/15 PASS` (`0 FAIL, 0 WARN`).
- **`tools/lv.py curriculum curriculum/llm.yaml`**: `15 bài, 15 đã có đặc tả, 0 lỗi` (`PASS`).
- **`audit/llm/verify_llm.py`**: `18 PASS · 0 FAIL`.
- **`audit/review/arith_scan.py LLM`**: `13 phép tính kiểm được, 0 FAIL`.
- **`build_report.json` (`2026-11-19T23:42Z`..`2026-11-20T00:04Z`)**: `spec_sha256` & `tts_sha256` khớp **15/15** (`STALE = 0`), giọng duy nhất `vi-VN-NamMinhNeural`.
- **`L*.srt == say`**: khớp **15/15 (100%)**.
- **`out/LLM/L*/asr_report.md`**: **15/15** có `thiếu audio: 0`, `chưa xem xét: 0` (mọi câu gắn cờ đều đã ghi `asr_reviewed` kèm `NOT_VERIFIED bằng tai người`).
- **`audit/layout_LLM.tsv`**: rỗng (2 byte `\r\n`, 0 lỗi bố cục).
- **Chạy thực nghiệm 15 `labs/LLM/L*/loi_giai.py` & 15 khối mã `practice#1`** bằng `.venv/Scripts/python.exe -B`: **15/15** cho `stdout` khớp `mong_doi.txt` và `practice#2/#4`. *(Ghi chú môi trường: `audit/review/lab_gate.py LLM` trả `0 PASS · 15 FAIL` vì `C:\Program Files\Git\bin\bash.exe` trong shell này thoát mã `1` không đầu ra khi gọi `cham.sh`; `audit/review/screen_code/LLM.yaml` khớp 45/45 SHA nhưng gán toàn bộ sang `kind: other, lang: text` thay vì `run/python` & `output`.)*
- **Kiểm tra `"càng ..."` trong `say`/`show`**: Đã kiểm đủ 7 vị trí (`L01 sym#0`, `L07 prereq#0`, `L09 prereq#1`, `L12 prereq#0` có rào `"thường là"`, `L14 stage1#0/stage2#0/stage5#1`) — **0 lỗi** logic hay diễn đạt tiếng Việt.

---

## 3. Tỷ lệ `P1`, `P8`, `P9` toàn khóa (15 bài)
- **`P1` (thuật ngữ / ký hiệu / viết tắt tại chỗ, gồm `practice#0/#3` và `de.md`)**:
  - Đạt (`2`): **2/15 (13.3%)** — `L10`, `L14`.
  - Vừa (`1`): **10/15 (66.7%)** — `L00, L01, L02, L03, L04, L05, L08, L09, L11, L12`.
  - Yếu (`0`): **3/15 (20.0%)** — `L06, L07, L13`.
- **`P8` (Thực nghiệm AF2 — đề tự làm khác ví dụ, không lộ lời giải, không gán cứng)**:
  - Đạt (`2`): **0/15 (0.0%)**.
  - Một phần (`1`): **12/15 (80.0%)** — có `loi_giai.py` khớp `mong_doi.txt`, nhưng lộ lời giải trước `pause`, trùng số ví dụ, thiếu format đầu ra trong `de.md`, hoặc gán cứng (`L00, L07, L12`).
  - Không đạt (`0`): **3/15 (20.0%)** — `L01, L02, L14` (lỗi đề/mâu thuẫn đáp án).
- **`P9` (Hai mức quy mô / thời gian ở thân bài & `recap`)**:
  - Đạt (`2`): **7/15 (46.7%)** — `L05, L06, L08, L10, L11, L13, L14` (trong đó `L08, L11` phần `recap` chưa nhấn mạnh lại 2 mức quy mô).
  - Một phần (`1`): **6/15 (40.0%)** — `L01, L02, L03, L04, L09, L12`.
  - Không có (`0`): **2/15 (13.3%)** — `L00, L07`.

---

## 4. Báo cáo chi tiết từng bài (`L00..L14`)

### **L00 — Mô hình ngôn ngữ: xác suất của một chuỗi và quy tắc chuỗi** (`sha16: 8b81f6c36bd983cb`)
- **Điểm**: `P1=1`, `P8=1`, `P9=0`.
- **`MUST`**:
  - `practice#1/#2` lộ toàn bộ `loi_giai.py` và `prob=4/9 float=0.4444` trước `practice#3` (`pause: 30`).
  - `labs/LLM/L00/loi_giai.py` **gán cứng** `Fraction(2, 3) * Fraction(1, 1) * Fraction(2, 3) * Fraction(1, 1)` thay vì đếm bigram từ 3 câu đề bài nêu (`de.md`), trùng số ví dụ trong bài, và `de.md` không ghi định dạng `prob=... float=...`.
  - `covers:` gán `objective: 3` (*"Hiểu mô hình ngôn ngữ dự đoán từ tố kế tiếp"*) → `practice`, trong khi `practice` chỉ nhân phân số.
- **`SHOULD`**:
  - `P1` ở `practice#0/#3` & `de.md`: dùng `Fraction` (`from fractions import Fraction`) nhưng `practice#0` không giảng `Fraction` (lại giải thích `import thu_vien` và `:.3f` dù `practice#1` dùng `from ... import ...` và `:.4f`).
  - `P9`: Thân bài và `recap` chưa có 2 mức quy mô tính số.
- **`INFO`**: SVG `00016.png` nhánh dưới `bạn → thích` không ghi nhãn `1` (khác nhánh trên `tôi → thích`), không đè chữ.
- **PNG đã xem**: `out/LLM/L00/frames/00016.png`, `00051.png`, `00052.png`.

### **L01 — Mô hình n-gram, làm trơn và độ hỗn loạn** (`sha16: bf4e347c277ff0a5`)
- **Điểm**: `P1=1`, `P8=0`, `P9=1`.
- **`MUST`**:
  - `labs/LLM/L01/de.md` chỉ ghi *"Tính perplexity `(4/9)^(-1/4)` và xác suất sau làm trơn cộng 1 của cặp chưa gặp (`V=6`)"* mà **không nêu ngữ cảnh nào** (đếm ngữ cảnh bằng `2`), trong khi `loi_giai.py` gán cứng `(0 + 1) / (2 + 6) = 0.125` (khác cả 2 cặp chưa gặp trong ví dụ bài là `1/9` và `1/7`).
  - `practice#1/#2` lộ code và `perplexity=1.225 add1_unseen=0.125` trước `practice#3` (`pause`).
  - `covers:` gán `objective: 3` (*"So sánh mô hình đúng cách"*) → `practice` (thực chất nằm ở `pitfalls`).
- **`SHOULD`**:
  - `P1` ở `practice#3` & `de.md`: dùng `Perplexity` và `Laplace` chưa chú thích trong thân bài (bài dùng `"độ hỗn loạn"`, `"làm trơn cộng một"`).
  - `P9`: `pitfalls#2` nêu `V = 50 000` nhưng chưa tính cụ thể xác suất bị chia đi bao nhiêu và `recap` chưa nêu quy mô.
- **`INFO`**: `"càng nhỏ càng tốt"` (`sym#0`) chính xác trong điều kiện cùng bộ tách & tập kiểm tra (`pitfalls#0/#1`).
- **PNG đã xem**: `out/LLM/L01/frames/00022.png`, `00058.png`, `00059.png`.

### **L02 — Tách từ tố: mã hoá cặp byte (BPE)** (`sha16: 3655fdf79b59fc08`)
- **Điểm**: `P1=1`, `P8=0`, `P9=1`.
- **`MUST`**:
  - **Mâu thuẫn kiến thức/đáp án**: `curriculum/llm.yaml` L02, thân bài `L02` (`example#1`: *"hoà thì lấy cặp gặp trước"* → `e+s (9)`, `es+t (9)`, `est+</w> (9)`), và `verify_llm.py` L02a đều ra `e+s`, `es+t`; **nhưng** `labs/LLM/L02/loi_giai.py` (và `practice#1`) viết `best = max(pairs, key=lambda k: (pairs[k], k))` — ưu tiên cặp có thứ tự từ điển lớn nhất → `mong_doi.txt` (`practice#2/#4`) ra `merge1=t+</w> freq=9` và `merge2=s+t</w> freq=9`! `de.md` cũng không nêu luật phân xử hoà.
  - `practice#1/#2` lộ toàn bộ code và đầu ra trước `practice#3` (`pause`).
  - `covers:` gán `objective: 3` (*"Hiểu vì sao số từ tố khác nhau giữa các ngôn ngữ"*) → `practice` (`pitfalls#1` mới dạy).
- **`SHOULD`**:
  - `P1` ở `practice#3`, `de.md`, `practice#0`: thân bài dùng `"mã hoá cặp byte"`, không giải thích cụm `Byte-Pair Encoding` hay tên `Sennrich 2016` (chỉ nằm trong `source:`); `practice#0` giải thích `:.3f` (không dùng) mà thiếu `Counter`, `zip`, `max`, `.split()`, `.items()`, `.replace()`.
  - `P9`: Mới so sánh 2 ngôn ngữ (16 byte vs 11 byte), chưa có 2 mức quy mô dữ liệu/từ vựng.
- **`INFO`**: SVG `00016.png` hiển thị rõ nét, không tràn/đè chữ.
- **PNG đã xem**: `out/LLM/L02/frames/00016.png`, `00050.png`, `00051.png`, `00053.png`.

### **L03 — Vector nhúng và độ tương tự cosin** (`sha16: 38f6ecd1bd421423`)
- **Điểm**: `P1=1`, `P8=1`, `P9=1`.
- **`MUST`**:
  - `practice#1/#2` lộ `loi_giai.py` và `cos_sim=0.956 cos_orth=0.0` trước `practice#3` (`pause`); `de.md` trùng số ví dụ bài và thiếu định dạng in ra.
  - `covers:` gán `objective: 3` (*"Biết giới hạn của độ tương tự giữa vector nhúng"*) → `practice` (`pitfalls` mới dạy).
- **`SHOULD`**:
  - `P1`: `practice#3` & `de.md` dùng `trực giao` (thân bài chỉ dùng `vuông góc`); `practice#0` thiếu `math.hypot`, `zip`, `sum`.
  - `P9`: Mới nêu 12 288 chiều của mô hình 175 tỉ (tĩnh) và nhân 10 lần vector (`pitfalls#1`), chưa có 2 mức quy mô trong thân & `recap`.
- **`INFO`**: `asr_report.md` 0 câu gắn cờ.
- **PNG đã xem**: `out/LLM/L03/frames/00018.png`, `00052.png`.

### **L04 — Transformer giải mã: mặt nạ nhân quả và vị trí** (`sha16: d50c4bd430da4798`)
- **Điểm**: `P1=1`, `P8=1`, `P9=1`.
- **`MUST`**:
  - `practice#1/#2` lộ code và `n=4 allowed=10/16 / n=8 allowed=36/64` trước `practice#3` (`pause`); `de.md` thiếu định dạng output.
  - `covers:` gán `objective: 3` (*"Giải thích vì sao cần thông tin vị trí"*) → `practice` (`sym` và `pitfalls#1` mới dạy).
- **`SHOULD`**:
  - `P1`: `practice#3` & `de.md` dùng `tam giác dưới` (thân bài chưa gọi tên này); `practice#0` thiếu phép `//` và ghi thừa `f"{val:.3f}"`.
  - `P9`: Chưa phân tích bùng nổ $O(n^2)$ ở 2 mức quy mô ngữ cảnh (để sang L13) và `recap` chưa nêu quy mô.
- **`INFO`**: SVG `00023.png` mũi tên tự trỏ xanh ở hộp `trời` chạm nhẹ vào đầu cung nét đứt đỏ, chữ hoàn toàn rõ không bị đè.
- **PNG đã xem**: `out/LLM/L04/frames/00023.png`, `00056.png`, `00057.png`.

### **L05 — Chi phí tính toán: tham số, phép tính và bộ nhớ đệm khoá–giá trị** (`sha16: 495b5152ef1197e4`)
- **Điểm**: `P1=1`, `P8=1`, `P9=2`.
- **`MUST`**:
  - `practice#1/#2` lộ code và `kv_bytes=2147483648 kv_GiB=2.0` trước `practice#3` (`pause`); trùng số ví dụ `example#2`; `de.md` thiếu định dạng output.
  - `covers:` gán `objective: 4` (*"Quyết định một thẻ tính toán phục vụ được bao nhiêu chuỗi cùng lúc"*) → `practice` (`quiz` mới dạy bài toán thẻ 80 GB!).
- **`SHOULD`**:
  - `P1`: `practice#3` & `de.md` dùng **`KV cache`** và `de.md` dùng thêm **`fp16`**, cả hai thuật ngữ/viết tắt tiếng Anh này **không hề được chú thích trong thân bài** (thân bài chỉ viết `"bộ nhớ đệm khoá–giá trị"` và `"dạng nửa độ chính xác"`). `practice#0` ghi `:.3f` trong khi `practice#1` dùng `:.1f` và `**`.
- **`INFO`**: `P9` mạnh (1 vs 16 chuỗi, 4096 vs 32768 từ tố, GQA 1/4, thẻ 80 GB 8 vs 9 chuỗi, `recap` nêu đủ biến chi phối); mọi phép tính trong bài chính xác (`verify_llm.py` L05a PASS).
- **PNG đã xem**: `out/LLM/L05/frames/00021.png`, `00025.png`, `00082.png`, `00085.png`.

### **L06 — Huấn luyện trước: mất mát entropy chéo và quy luật mở rộng** (`sha16: e95ea05f5121a85e`)
- **Điểm**: `P1=0`, `P8=1`, `P9=2`.
- **`MUST`**:
  - `practice#1/#2` lộ code và `ppl=7.39 flops=5.88e+21` trước `practice#3` (`pause`); trùng y nguyên số `example#1/#2`; `de.md` thiếu định dạng output.
  - `covers:` gán `objective: 3` (*"Hiểu tỉ lệ dữ liệu trên tham số là điểm tối ưu, không phải luật"*) → `practice` (`pitfalls#1` mới dạy).
  - **`P1=0`**: `practice#3` & `de.md` dùng **`loss`**, **`PPL`**, **`7B`**, **`140B tokens`**, **`exp(2.0)`** hoàn toàn chưa giảng trong thân bài (bài dùng `"mất mát"`, `"$PP$"`, `"tỉ"`, `"từ tố"`).
- **`SHOULD`**: `practice#0` ghi `:.3f` nhưng `practice#1` dùng `:.2f` và `:.2e`.
- **`INFO`**: `P9` đạt 2 (7B vs 70B tăng 100× tính toán; Chinchilla 2022 20 tok/param vs LLaMA-7B 2023 ~143 tok/param); khớp `sources_L06_L09.md`.
- **PNG đã xem**: `out/LLM/L06/frames/00034.png`, `00067.png`, `00068.png`.

### **L07 — Sinh văn bản: tham lam, nhiệt độ, top-k, top-p** (`sha16: aeeccae97da632cd`)
- **Điểm**: `P1=0`, `P8=1`, `P9=0`.
- **`MUST`**:
  - `practice#1/#2` lộ code và đầu ra trước `practice#3` (`pause`); `loi_giai.py` **gán cứng** `sum(p1[:2])` thay vì lọc động theo tổng tích luỹ `>= 0.9` (và cộng trên mảng đã `round(..., 3)` thay vì chưa làm tròn như `quiz#2` nhắc); trùng số `(2, 1, 0)` của `example`; `de.md` thiếu định dạng output.
  - `covers:` gán `objective: 3` (*"Chọn cách sinh theo mục đích"*) → `practice` (`pitfalls#0` & `recap#0` mới dạy).
  - **`P1=0`**: `practice#3` & `de.md` dùng **`Softmax`**, **`logits`**, **`token`** chưa từng được chú thích trong thân bài (bài dùng `"hàm chuẩn hoá mũ"`, `"điểm"`, `"từ tố"`).
- **`SHOULD`**: `practice#0` thiếu `round`, `sum`, `math.exp`; `P9=0` (chỉ có 3 mức nhiệt độ T, chưa có 2 mức quy mô/độ dài văn bản có số liệu).
- **`INFO`**: `"điểm càng cao thì càng hợp"` (`prereq#0`) chính xác; `asr_report.md` 0 gắn cờ.
- **PNG đã xem**: `out/LLM/L07/frames/00015.png`, `00049.png`.

### **L08 — Tinh chỉnh: toàn bộ tham số và hạng thấp (LoRA)** (`sha16: 1fd0cbd0592aaad8`)
- **Điểm**: `P1=1`, `P8=1`, `P9=2`.
- **`MUST`**:
  - `practice#1/#2` lộ code và `full=16777216 lora=65536 ratio=0.39%` trước `practice#3` (`pause`); trùng số `example#0/#1`; `de.md` thiếu định dạng output.
  - `covers:` gán `objective: 3` (*"Biết khi nào nên tinh chỉnh, khi nào chỉ cần lời nhắc hay truy xuất"*) → `practice` (`pitfalls` mới dạy).
- **`SHOULD`**:
  - `P1`: Viết tắt **`LoRA`** chỉ nằm ở `title` bài và `source:`, **không hề xuất hiện hay giải thích trong thân bài** (`sym#0` chỉ nói `"Tinh chỉnh hạng thấp"`), nhưng `practice#3` & `de.md` dùng trực tiếp `LoRA`. `practice#0` ghi `:.3f` nhưng `practice#1` dùng `:.2f`.
  - `P9`: Thân bài có 2 mức quy mô tốt (1 ma trận 0.39% vs 128 ma trận / 32 tầng 0.13%, 16.8 MB vs 12.9 GB / 103 GB Adam), nhưng `recap` chưa tóm lại so sánh 2 mức quy mô.
- **`INFO`**: Khớp số liệu trong `verify_llm.py` L08a và ZeRO 16 byte/tham số.
- **PNG đã xem**: `out/LLM/L08/frames/00022.png`, `00054.png`, `00055.png`.

### **L09 — Học theo chỉ dẫn và căn chỉnh theo đánh giá của con người** (`sha16: 355c8c54e72e5363`)
- **Điểm**: `P1=1`, `P8=1`, `P9=1`.
- **`MUST`**:
  - `practice#1/#2` lộ code và `bt_prob=0.731 bt_loss=0.313` trước `practice#3` (`pause`); trùng số `example#1`; `de.md` thiếu định dạng output.
  - `covers:` gán `objective: 3` (*"Nhận ra khai thác lỗ hổng phần thưởng"*) → `practice` (`pitfalls#0` & `quiz#2` mới dạy).
- **`SHOULD`**:
  - `P1`: `practice#3` & `de.md` dùng **`sigmoid`** trong khi thân bài chỉ gọi là `"Hàm xích-ma"` (`$\sigma(x)$`), chưa chú thích tên `sigmoid`.
  - `P9`: Có diễn tiến 3 giai đoạn (`RLHF 2022 → DPO 2023`) và ví dụ minh hoạ độ dài câu (40/200/400 từ), chưa có 2 mức quy mô hệ thống thực tế trong thân & `recap`.
- **`INFO`**: `"Xác suất càng gần 1 thì âm lôgarit của nó càng gần 0..."` (`prereq#1`) chính xác; đồng thuận người chấm 73% khớp `sources_L06_L09.md`.
- **PNG đã xem**: `out/LLM/L09/frames/00018.png`, `00053.png`.

### **L10 — Đánh giá mô hình ngôn ngữ: bộ kiểm tra, nhiễm dữ liệu, khoảng tin cậy** (`sha16: 5e982bd0a516612e`)
- **Điểm**: `P1=2`, `P8=1`, `P9=2`.
- **`MUST`**:
  - `practice#1/#2` lộ code và `acc=82.0% margin_pp=3.37` trước `practice#3` (`pause`); trùng số `example#0`; `de.md` thiếu định dạng output.
  - `covers:` gán `objective: 3` (*"Nhận ra nhiễm dữ liệu kiểm tra"*) → `practice` (`pitfalls#1` mới dạy).
- **`SHOULD`**: `practice#0` ghi `:.3f` nhưng `practice#1` dùng `:.1f` và `:.2f`.
- **`INFO`**: `P1=2` sạch thuật ngữ; `P9=2` tốt (`n=100` vs `400`, `500` vs `2000`, `1537` vs `6147`).
- **PNG đã xem**: `out/LLM/L10/frames/00023.png`, `00057.png`, `00058.png`.

### **L11 — Ảo giác, hiệu chuẩn và tự nhất quán** (`sha16: 11f0ae8045592a8b`)
- **Điểm**: `P1=1`, `P8=1`, `P9=2`.
- **`MUST`**:
  - `practice#1/#2` lộ code và `single=0.600 maj5_indep=0.683` trước `practice#3` (`pause`); trùng số `example#2/#3`; `de.md` thiếu định dạng output.
- **`SHOULD`**:
  - `P1`: `de.md` dùng `"phân phối nhị thức"` chưa gọi tên trong thân bài; `practice#0` thiếu `math.comb` và `range` dùng ở `practice#1`.
  - `covers:` trỏ `objective: 3` (*"Tính lợi ích và điều kiện của biểu quyết đa số"*) → `practice` (chỉ tính phần lợi ích độc lập, phần *điều kiện* nằm ở `pitfalls#0/#1`).
  - `P9`: Thân bài có 3 mức k-vote (`1` vs `5` vs `25` lần + `p=0.4` + tương quan), `recap` nhắc điều kiện nhưng chưa nhắc 2 mức k.
- **`INFO`**: `asr_report.md` 0 gắn cờ.
- **PNG đã xem**: `out/LLM/L11/frames/00020.png`, `00057.png`, `00058.png`.

### **L12 — Sinh có truy xuất (RAG): chỉ mục, tìm kiếm, ghép ngữ cảnh** (`sha16: f3e3232a04e0c8dc`)
- **Điểm**: `P1=1`, `P8=1`, `P9=1`.
- **`MUST`**:
  - `practice#1/#2` lộ code và `top1=docA cos=0.956 recall_at_1=1.0` trước `practice#3` (`pause`); `loi_giai.py` **gán cứng** chuỗi `recall_at_1=1.0` trong `print(...)` mà không tính từ nhãn đúng; `de.md` thiếu định dạng output.
  - `covers:` gán `objective: 3` (*"Biết các lỗi thường gặp của truy xuất"*) → `practice` (`pitfalls` mới dạy).
- **`SHOULD`**:
  - `P1`: `practice#0` thiếu `math.hypot`, `max(..., key=...)`, `zip`; `practice#3` & `de.md` dùng `top-1` (thân bài chỉ viết `k đoạn`, chưa gọi tên `top-1`).
  - `P9`: Mới có danh sách 3–6 đoạn đồ chơi, chưa có 2 mức quy mô kho tài liệu/chỉ mục.
- **`INFO`**: `"Cô-sin càng gần 1 thì hai vector càng cùng hướng, thường là càng gần nghĩa"` (`prereq#0`) chính xác.
- **PNG đã xem**: `out/LLM/L12/frames/00019.png`, `00059.png`, `00060.png`.

### **L13 — Ngữ cảnh dài và suy luận hiệu quả** (`sha16: d4714b0e499f286c`)
- **Điểm**: `P1=0`, `P8=1`, `P9=2`.
- **`MUST`**:
  - `practice#1/#2` lộ code và `kv_mult=8x attn_flops_mult=64x` trước `practice#3` (`pause`); trùng số `hook`/`example#2`; `de.md` thiếu định dạng output.
  - `covers:` gán `objective: 3` (*"Biết vì sao ngữ cảnh dài không có nghĩa là dùng tốt mọi phần"*) → `practice` (`pitfalls#0` mới dạy).
  - **`P1=0`**: `practice#3` & `de.md` dùng **`attention`**, **`O(L^2)`** (trùng ký hiệu `L` số tầng ở L05 trong khi thân bài L13 dùng `n`!), **`KV cache`**, **`4k -> 32k`** — đều chưa chú thích trong thân bài (bài dùng `"chú ý"`, `"cỡ n bình phương"`, `"bộ nhớ đệm khoá–giá trị"`, `"4 nghìn"`, `"32 nghìn"`).
- **`SHOULD`**: `practice#0` liệt kê `f"{val:.3f}"` dù `practice#1` không định dạng số thực, và thiếu `//`, `**`.
- **`INFO`**: `P9=2` tốt (`4k→32k` 8×/64×, `8k→128k` 16×/256×, lượng tử hoá 2→1→0.5 byte, `α=0.8` vs `0.6`, `recap` phản ánh đủ).
- **PNG đã xem**: `out/LLM/L13/frames/00019.png`, `00054.png`.

### **L14 — Tình huống chuyên gia theo dòng thời gian: từ kiến trúc chú ý tới huấn luyện tối ưu tính toán** (`sha16: 1830c4aa6c6a8af3`)
- **Điểm**: `P1=2`, `P8=0`, `P9=2`.
- **`MUST`**:
  - `labs/LLM/L14/de.md` chỉ yêu cầu *"Đổi `C = 6 * 174.6e9 * 3e11` phép tính sang PF-ngày (`10^15 * 86400`)"*, **hoàn toàn thiếu yêu cầu thứ hai** (`tokens_per_param=20` từ Chinchilla `1.4e12 / 70e9`) có trong `loi_giai.py` và `mong_doi.txt`!
  - `practice#1/#2` lộ code và `gpt3_pf_days=3637 tokens_per_param=20` trước `practice#3` (`pause`); trùng số `stage3`/`stage4`; `de.md` thiếu định dạng output.
  - `covers:` gán `objective: 3` (*"Chia một ngân sách tính toán cho kích thước mô hình và dữ liệu ở quy mô của mình, kèm điều kiện đổi lựa chọn"*) → `practice` (`quiz` mới dạy mục tiêu này!).
- **`SHOULD`**: `practice#0` ghi `:.3f` trong khi `practice#1` dùng `:.0f`.
- **`INFO`**: Toàn bộ số liệu lịch sử/tính lại trong `L14` (`11.1 giờ`, `3.47 ngày`, `2.3e19`, `174 tỉ`, `3.14e23`, `3637 PF-ngày`, `5.88e23`, `20 tok/param`, `120` vs `30` ngày) khớp hoàn toàn `audit/llm/sources_L14.md` và `verify_llm.py`; 3 câu `"càng ..."` chính xác.
- **PNG đã xem**: `out/LLM/L14/frames/00019.png`, `00024.png`, `00117.png`, `00118.png`, `00121.png`.

---

## 5. Đề xuất hành động ưu tiên trước khi `GO`
1. **Sửa `L02` `loi_giai.py` + `de.md` + `mong_doi.txt`** theo đúng quy tắc bài giảng (`hoà thì lấy cặp gặp trước` → `e+s`, `es+t`) và dùng dữ liệu lab mới tách biệt khỏi ví dụ bài.
2. **Sửa `L01` `de.md` + `loi_giai.py`** (nêu rõ kho/ngữ cảnh cần tính, không gán cứng `2 + 6`) và **bổ sung yêu cầu Chinchilla vào `L14` `de.md`** (hoặc tách số liệu lab mới cho tất cả 15 bài, không gán cứng ở `L00, L07, L12`, ghi rõ format output trong `de.md`).
3. **Đảo lại luồng cảnh `practice` ở cả 15 bài**: không hiện code `loi_giai.py` và kết quả trước `pause`; giữ đúng `practice#0` (giải thích đúng cú pháp bài dùng) → đề + `pause` → gợi ý / đối chiếu `mong_doi.txt`; đồng thời cập nhật `screen_code/LLM.yaml` sang `kind: run, lang: python`.
4. **Khắc phục `P1` ở `practice#3` & `de.md`** (nhất quán dùng thuật ngữ tiếng Việt đã giảng hoặc chú thích rõ `KV cache`, `fp16`, `loss`, `PPL`, `Softmax`, `logits`, `attention`, `O(n^2)`, `LoRA`, `sigmoid`, `Perplexity`, `Laplace`, `Fraction`) và **sửa `covers:` ở 14/15 bài** trỏ đúng cảnh dạy từng mục tiêu; bổ sung **"Hai mức quy mô"** cho thân bài & `recap` các bài còn thiếu (`L00–L04, L07, L09, L12`).
5. Dựng lại các bài đã sửa (`render` + `build` + `asr`).