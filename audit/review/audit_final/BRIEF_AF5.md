# BRIEF_AF5 — Hướng dẫn đọc độc lập và viết/sửa bài chuẩn AF5

Người học mục tiêu: **mất gốc, chưa từng lập trình**, chỉ có video + thư mục `labs/` + `HOC_TAP.html`.

---

## 1. Quy tắc làm việc cho tác tử đọc độc lập (`D-13`)

1. Người đọc **CHỈ đọc**, không sửa bài học, không chạy `build`/`tts`/`asr`/`render`/`gen.py`/git.
2. Đường dẫn ghi báo cáo duy nhất được phép: tệp được giao trong `audit/review/read_af5/<KHOÁ>/<Lxx>.md` (hoặc tệp lô được chỉ định).
3. **Không đọc** báo cáo cũ (`sample_*`, `read_af5/` của bài khác, `handover_*`, `plan_*`).
4. Với mỗi bài được giao:
   - Ghi đúng `sha16` của tệp YAML lúc đọc.
   - Đọc **toàn bộ** tệp đặc tả `lessons/<khoá>/Lxx_*.yaml` + `labs/<KHOÁ>/<Lxx>/{de.md, mong_doi.txt, loi_giai.*, ca_an/}`.
   - Tự tính lại mọi con số quan trọng bằng phép tính độc lập hoặc chạy thử đoạn mã minh hoạ / lời giải lab trong thư mục tạm (nếu được cấp quyền đọc-chạy không sửa kho). Nếu không chạy được (ví dụ Docker/Oracle/mạng ngoài), ghi rõ `CHƯA KIỂM (lý do)` vào cột Tin cậy — tuyệt đối không bịa kết quả.
   - Xem ít nhất **3–5 khung hình** tiêu biểu (nếu có `out/<KHOÁ>/<Lxx>/frames/`) khi kiểm bố cục/SVG/công thức.
   - Đọc lời nói (`say`) song song màn hình (`show`): đối chiếu xem lời và hình có khớp thuật ngữ, số liệu, kí hiệu không; kiểm câu khuôn mẫu rỗng trong `audit/review/boiler_deny.txt`.

---

## 2. Tiêu chí đánh giá bài học

### A. Chuẩn xác (MUST vs SHOULD)

- **MUST (chặn chốt khoá — bắt buộc 0 lỗi):**
  1. Sai kiến thức, sai công thức, sai số liệu hoặc đầu ra chạy thật khác màn hình.
  2. Khẳng định tuyệt đối sai điều kiện hoặc bịa kết quả chưa chạy/không có nguồn.
  3. Mục tiêu (`objectives`) không được dạy ở cảnh khai báo trong `covers`, hoặc động từ **LÀM** mà cảnh chỉ nói suông/lệch nội dung.
  4. Dùng thuật ngữ / cú pháp / công cụ nâng cao trong ví dụ hoặc lab mà chưa giảng tại chỗ và chưa dạy ở bài tiên quyết (mất gốc kẹt).
  5. Cảnh **Tự làm** (`practice`) rỗng, chỉ "mở `de.md`", lộ toàn bộ đáp án `mong_doi.txt` trong `de.md`, chiếu nguyên `loi_giai.*` ngay trong video, hoặc lời giải không chạy ra `mong_doi.txt` / lọt qua `ca_an/` bằng hardcode.
  6. Lời đọc độn khuôn mẫu rỗng (`boiler_deny.txt`) hoặc lời đọc < 1 300 từ / < 9,0 phút không kể `pause`.
  7. Khối mã hoặc kết quả ở cảnh dạy không khớp nguồn thật / tự mâu thuẫn trong bài.
- **SHOULD (bắt buộc sửa cùng đợt):**
  - Lệch nhỏ giữa lời và màn hình (đọc thiếu mục bảng, khác đơn vị nhưng tương đương số).
  - Thiếu giả định/đánh đổi khi nêu ưu điểm.
  - Hình vẽ/SVG chữ quá nhỏ, chồng hộp, hoặc tên cảnh bị cắt cụt.
  - Không nhất quán ký hiệu/tên khoá giữa các cảnh.
  - Đề lab trùng đúng bộ số liệu của ví dụ trong bài.

### B. Thang độ sâu cho người mất gốc (`P1–P9`, mỗi mục 0 / 1 / 2)

- **P1 (Ôn nền & dạy tại chỗ):** Không nhảy bước; khái niệm/cú pháp mới đều giảng ngay.
- **P2 (Hook thực tế):** Mở bài từ tình huống thật có con số cụ thể.
- **P3 (Hình cơ chế):** Hình/SVG/bảng thể hiện đúng luồng hoạt động (không chỉ chữ).
- **P4 (Ví dụ từng bước):** Làm tay ≥ 4 bước số, có giá trị trung gian rõ ràng.
- **P5 (Kiểm chứng độc lập):** Đối chiếu kết quả bằng đường khác / mô phỏng / chạy thật.
- **P6 (Bẫy hay gặp):** Nêu bẫy cụ thể của người mới hoặc kỹ sư thực tế kèm ví dụ sai.
- **P7 (Quiz kiểm hiểu):** Câu hỏi buộc suy luận + đáp án giải từng bước.
- **P8 (Thực nghiệm thật):** Mã/lệnh chạy thật cho ra đúng kết quả trên màn hình.
- **P9 (Quy mô & đánh đổi):** Có ít nhất hai mức quy mô có số liệu + đánh đổi rõ ràng (không gắn note "Hai mức quy mô:" rỗng vào `recap`).

Quy ước **Mất gốc ĐỦ**: tổng `P1..P7 >= 12` và **không** có mục nào = 0; `P1 = 2`, `P8 = 2`, `P9 >= 1`.

### C. Thang lab `L1–L5` (mỗi mục 0 / 1 / 2)

- **L1 (Đề & dữ liệu rõ trong video):** Bước 1 của `practice` nêu rõ nhiệm vụ và dữ liệu vào mẫu ngay trên màn hình (không chỉ ghi "mở `de.md`"); có `pause`, bước kết quả mong đợi, và bước gợi ý (tổng ≥ 3 bước).
- **L2 (Số liệu mới, đúng nội dung vừa học):** Lab dùng dữ liệu khác ví dụ trong video; không dùng công cụ/thư viện chưa dạy; luyện đúng kỹ năng khó nhất trong `objectives`.
- **L3 (Không lộ đáp án & không chiếu lời giải):** `de.md` không chép nguyên văn mọi dòng giá trị đáp án từ `mong_doi.txt`; video không chiếu toàn bộ `loi_giai.*`.
- **L4 (Chấm thật & chạy lại khớp):** Lời giải mẫu chạy thật qua `labs/cham.sh` cho khớp `mong_doi.txt` và toàn bộ `ca_an/` (hoặc `kiem/` với `du_an`).
- **L5 (Chống in cứng — `ca_them: bat_buoc`):** Lab bắt buộc có `ca_an/` (`ham.json` cho Python, `in_k.txt`/`args_k.txt`→`out_k.txt` cho Java/C/JS/Bash, `seed_k.sql`→`out_k.txt` cho SQL) hoặc `kiem/` (cho `du_an`); lời giải chỉ `print(...)` cứng đáp án công khai **phải FAIL** khi chấm.

### D. Hợp đồng viết/sửa bài & `CONTRACT.yaml`

- Lời đọc mỗi bài thông thường: **1 300 – 2 300 từ**, ≥ 9,0 phút không kể `pause` (riêng `case: journey` có thể vượt 2 300 từ nếu mật độ nội dung sạch).
- Tổng `pause` hợp lý (≤ 300 s).
- `checks` trong bài phải tham chiếu giá trị/tham số thật của bài — cấm hằng đẳng thức vô nghĩa (`1 + 1 == 2`, `1e-12 < 1e-9`).
- Cấm chữ chấm điểm giả (`(-10đ)`, `thang 100 điểm`, `được ... điểm`) trong cảnh Tự làm, `de.md` và `labs/PRJ/SPEC.md`.
- Nếu trong bài có bảng đối chiếu "viết trong mã" thì mọi mục bên trái phải xuất hiện thật trong đoạn mã cùng cảnh.
- Nếu bài nằm trong khoá có `audit/<khoá>/src/*.tpl.yaml`, sau khi sửa YAML bài nhớ chạy `sync_tpl_from_lesson.py <khoá> --write` (và tuyệt đối không chạy bất kỳ generator bị khoá nào).

---

## 3. Mẫu báo cáo chuẩn cho mỗi bài (`audit/review/read_af5/<KHOÁ>/<Lxx>.md`)

```markdown
# <KHOÁ> <Lxx> — sha16: `<16_hex>`
- Trạng thái đọc: ĐÃ ĐỌC ĐỦ (YAML + lab + frames)
- Thời lượng / từ lời đọc: <mm:ss> (<m_no_pause> phút không pause) / <N> từ

## A. Chuẩn xác
| Mức | Cảnh/step | Trích nguyên chữ | Vì sao sai + bằng chứng (phép tính/lệnh) | Đề xuất sửa | Tin cậy |
|---|---|---|---|---|---|
(nếu 0 lỗi ghi: "Không phát hiện lỗi MUST/SHOULD.")

## B. Độ sâu & Lab
- Điểm: P1=.. P2=.. P3=.. P4=.. P5=.. P6=.. P7=.. (Tổng=..) | P8=.. P9=.. -> Mất gốc: <ĐỦ/GẦN/CHƯA>
- Lab: L1=.. L2=.. L3=.. L4=.. L5=..
- covers đúng: <k/n>
- Số đã tính lại / mã đã chạy: ...
- Khung hình đã xem: ...
- Chỗ người mất gốc có thể kẹt (nếu có): ...
```
