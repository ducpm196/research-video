# Báo cáo Đọc Độc Lập AF5 — PRJ (`L00` – `L03`)

- Phạm vi: `PRJ L00..L03` (`lessons/prj/L00..L03*.yaml`, `labs/PRJ/L00..L03/`, `out/PRJ/L00..L03/`).
- Quy tắc đối chiếu: `audit/review/audit_final/BRIEF_AF5.md`, `audit/review/boiler_deny.txt`, `labs/CONTRACT.yaml`, `labs/PRJ/SPEC.md`, `curriculum/prj.yaml`.
- Ghi chú chung về hạ tầng kiểm tra:
  - Không có `out/PRJ/<Lxx>/meta.json` ở cả 4 bài; thông số dựng lấy từ `out/PRJ/<Lxx>/build_report.json` và `out/PRJ/<Lxx>/_frames.txt`.
  - Ở cả 4 bài, `spec_sha256` trong `build_report.json` khác SHA-256 của tệp YAML hiện tại (YAML đã được chỉnh/bổ sung `asr_reviewed` sau lần build trước).
  - Kiểm tra `boiler_deny.txt` và chữ chấm điểm giả (`-10đ`, `thang 100`, `được ... điểm`): **0 vi phạm** trên cả 4 YAML, `de.md`, `labs/PRJ/SPEC.md`.
  - Chạy `bash labs/cham.sh` trực tiếp trong WSL bị chặn quyền gọi `.venv/Scripts/python.exe` qua `\\wsl.localhost\...`, nhưng đã chạy kiểm thử độc lập trực tiếp `labs/PRJ/L00..L03/loi_giai.py` bằng `.venv/Scripts/python.exe` trên toàn bộ `du_lieu.txt` → `mong_doi.txt` và 100% `ca_an/*.in` → `ca_an/*.out`: **Đạt 100%**.

## Bảng tóm tắt tổng hợp

| Bài | `sha16` | Từ / Thời lượng (không pause) | `MUST` | `SHOULD` | `P1..P7` (Tổng) | `P8` | `P9` | `L1..L5` | `covers` | ASR (`chưa xem xét` / `NOT_VERIFIED`) | Frames | Kết luận |
|---|---|---:|---:|---:|---:|---:|---:|---|---|---|---:|---|
| `PRJ L00` | `e76bb678d08cdcf1` | 1 388 / 06:54 (6,90 phút) | 1 | 3 | 2,2,2,2,2,2,2 (14) | 2 | 2 | 1,2,2,2,2 | 3/3 | 0 / thiếu ở 1/1 mục | 5 PNG OK | CÓ LỖI CHẶN |
| `PRJ L01` | `efc47d42771b5ada` | 1 351 / 06:47 (6,78 phút) | 1 | 3 | 2,2,2,2,2,2,2 (14) | 2 | 2 | 1,2,2,2,2 | 3/3 | 0 / 0 cờ | 5 PNG OK | CÓ LỖI CHẶN |
| `PRJ L02` | `18204d50cceb0f5c` | 1 411 / 06:42 (6,69 phút) | 2 | 3 | 2,2,2,2,2,2,2 (14) | 2 | 2 | 1,1,2,2,2 | 2/3 | 0 / đủ 1/1 mục | 5 PNG OK | CÓ LỖI CHẶN |
| `PRJ L03` | `275fb737e25a9873` | 1 326 / 06:35 (6,58 phút) | 1 | 3 | 2,2,2,2,2,2,2 (14) | 2 | 2 | 1,2,2,2,2 | 2/3 | 0 / đủ 4/7, thiếu 3/7 | 5 PNG OK | CÓ LỖI CHẶN |

---

# PRJ L00 — sha16: `e76bb678d08cdcf1`
- Trạng thái đọc: ĐÃ ĐỌC ĐỦ (YAML + lab + `ca_an/` + `build_report.json` + `asr_report.md` + 5 frames PNG)
- Thời lượng / từ lời đọc: `07:44` (`463,833 s` có `50 s` pause; `413,833 s` = `6,90 phút` không pause) / `1 388` từ
- `out/PRJ/L00/meta.json`: Không tồn tại; `build_report.json` ghi `spec_sha256: 37b567020d0dfa82...` (khác YAML hiện tại `e76bb678d08cdcf1...`).
- Trạng thái ASR: `câu: 69, thiếu audio: 0, gắn cờ: 1, chưa xem xét: 0`; mục `asr_reviewed` ở khung 9 (`0.821`) ghi lý do nhưng **chưa giữ chuỗi `"NOT_VERIFIED bằng tai người"`**.

## A. Chuẩn xác
| Mức | Cảnh/step | Trích nguyên chữ | Vì sao sai + bằng chứng (phép tính/lệnh) | Đề xuất sửa | Tin cậy |
|---|---|---|---|---|---|
| MUST | Toàn bài | (tổng thời lượng âm thanh) | `BRIEF_AF5.md` mục 2A.6 & 2D yêu cầu `≥ 9,0 phút không kể pause`. Từ `build_report.json` (`463,833 s`) và `_frames.txt` trừ `50 s` pause còn `413,833 s = 6,90 phút < 9,0 phút`. | Mở rộng giảng sâu ví dụ chạy thật/kiểm chứng và giải thích từng dòng mã hoặc thêm ví dụ biên để đạt ≥ 540 s không pause (~1 800+ từ ở tốc độ -5%). | Đã kiểm (`build_report.json` + `_frames.txt`) |
| SHOULD | `sym` step 0 (`say` vs `show`) | `say`: "Bốn nhóm tiêu chí nghiệm thu trên bảng dùng chuẩn Đạt hay Chưa đạt..." | Bảng `show` cùng bước chỉ có **3 hàng** (`Đúng chức năng & bất biến`, `Biên & lỗi đầu vào`, `Quy mô & tái lập tất định`), thiếu hàng thứ 4 (`Sạch & tất định` trong `labs/PRJ/SPEC.md`). | Bổ sung hàng thứ 4 vào bảng `show` hoặc sửa lời đọc thành "Ba nhóm tiêu chí trên bảng...". | Đã kiểm (`YAML` + `SPEC.md`) |
| SHOULD | `quymo` (`checks`) | `100_000 * 1 == 100_000` | Hằng đẳng thức `x * 1 == x` không kiểm chứng giá trị nghiệp vụ (vi phạm quy ước `checks` mục 2D). | Thay bằng kiểm chứng tính toán của bảng/bài (ví dụ `50_000 * 100 - 50_000 * 50 == 2_500_000` hoặc so sánh chi phí chèn lô). | Đã kiểm (đọc YAML) |
| SHOULD | `check` step 0 (`say`) | "Hàm kết hợp giá trị mặc định không bảo đảm kết quả vẫn là số nguyên..." | Cách diễn đạt `"giá trị mặc định không"` dễ nghe nhầm thành *"không bảo đảm"* thay vì *"giá trị mặc định bằng 0 bảo đảm"*. | Sửa thành *"Hàm kết hợp giá trị mặc định bằng không giúp bảo đảm kết quả vẫn là số nguyên..."*. | Đã kiểm (đọc YAML) |

## B. Độ sâu & Lab
- Điểm: `P1=2 P2=2 P3=2 P4=2 P5=2 P6=2 P7=2 (Tổng=14) | P8=2 P9=2` -> Mất gốc: **ĐỦ** (về nội dung; bị chặn MUST thời lượng `< 9,0` phút)
- Lab: `L1=1 L2=2 L3=2 L4=2 L5=2` (`L1=1` vì `practice` step 0 chỉ ghi mở `labs/PRJ/L00/de.md` và đọc CSV từ `stdin`, chưa chiếu dữ liệu CSV mẫu ngay trên màn hình step 0)
- `covers` đúng: `3/3` (`1 -> example`, `2 -> check`, `3 -> practice`)
- Số đã tính lại / mã đã chạy:
  - Tất cả `checks` (`alg.prj_csv_totals(...) == (2, 2, 1000)`, `4/5 == 0.8`, `50000*100 - 50000*50 == 2_500_000`, `2000-750 == 1250`, `8/10 == 0.8`): `True`.
  - Chạy thật các khối mã `example..step 2` (`valid=4 bad=1 pct=80.0% in=1500 out=500`), `check..step 1` (`match=True sql_net=1000 acc={'u1': 700, 'u2': 300}`), `check..step 3` (`n=100000 net=2500000 batch_ok=True`): khớp 100%.
  - Chạy `labs/PRJ/L00/loi_giai.py`: `du_lieu.txt` (0.073s), `01_bien_loi.in` (0.056s), `02_quy_mo_vua.in` (0.064s), `03_quy_mo_lon.in` (0.104s) đều khớp 100%.
- Khung hình đã xem: `00017.png` (SVG 2 nhánh), `00022.png` (công thức LaTeX + hộp nổi bật), `00028.png` (mã Python), `00043.png` (bảng 3 cỡ tệp), `00058.png` (cảnh Tự làm + badge tạm dừng) — bố cục sạch, không chồng chữ, không cắt cụt.
- Chỗ người mất gốc có thể kẹt (nếu có): `practice` step 0 chưa chiếu 2–3 dòng CSV đầu vào mẫu nên học viên phải mở `de.md` mới thấy khuôn `<tai_khoan>,<loai>,<so_tien>`.

---

# PRJ L01 — sha16: `efc47d42771b5ada`
- Trạng thái đọc: ĐÃ ĐỌC ĐỦ (YAML + lab + `ca_an/` + `build_report.json` + `asr_report.md` + 5 frames PNG)
- Thời lượng / từ lời đọc: `07:37` (`456,867 s` có `50 s` pause; `406,867 s` = `6,78 phút` không pause) / `1 351` từ
- `out/PRJ/L01/meta.json`: Không tồn tại; `build_report.json` ghi `spec_sha256: 37f293838629b6fa...` (khác YAML hiện tại `efc47d42771b5ada...`).
- Trạng thái ASR: `câu: 67, thiếu audio: 0, gắn cờ: 0, chưa xem xét: 0`; `asr_reviewed: []`.

## A. Chuẩn xác
| Mức | Cảnh/step | Trích nguyên chữ | Vì sao sai + bằng chứng (phép tính/lệnh) | Đề xuất sửa | Tin cậy |
|---|---|---|---|---|---|
| MUST | Toàn bài | (tổng thời lượng âm thanh) | `456,867 s - 50 s = 406,867 s = 6,78 phút < 9,0 phút` không kể pause (vi phạm `BRIEF_AF5.md` 2A.6 & 2D). | Bổ sung ví dụ chạy thử có `threading` đồng thời hoặc giải thích từng nhánh trong `apply_tx`/`xfer` để đạt ≥ 9,0 phút không pause. | Đã kiểm (`build_report.json` + `_frames.txt`) |
| SHOULD | `quymo` (`checks`) | `500 * 1 == 500` | Hằng đẳng thức `x * 1 == x` không có giá trị kiểm chứng (vi phạm mục 2D). | Thay bằng kiểm chứng cân bằng sổ hoặc phép tính có nghĩa gắn với bảng quy mô. | Đã kiểm (đọc YAML) |
| SHOULD | `covers` mục tiêu 3 & `check` | `objective: 3` -> `scene: check` ("Kiểm chứng bằng kịch bản SQL/Python với cả giao dịch thành công và giao dịch từ chối thiếu số dư") | Cảnh `check` chỉ chạy Python kiểm biểu thức tĩnh trên `bal = {'A': 200, ...}` mà không chạy câu lệnh SQL nào; phần kịch bản SQLite có thành công + từ chối nằm ở `example`. | Hoặc bổ sung kiểm chứng SQL thật vào `check`, hoặc điều chỉnh `covers` mục tiêu 3 / nội dung `check`. | Đã kiểm (`YAML` + `curriculum/prj.yaml`) |
| SHOULD | `labs/PRJ/L01/de.md` dòng 12 | `cộng <phi> ở FEE (nếu FEE tồn tại và <phi> > 0)` | Hơi mơ hồ nếu `FEE` không tồn tại khi `<phi> > 0`: `loi_giai.py` từ chối giao dịch (`rf is None -> False`) để giữ `ledger_sum = 0`, trong khi lời văn dễ hiểu nhầm là vẫn cho phép giao dịch và bỏ qua phần phí. | Ghi rõ trong `de.md`: khi `<phi> > 0`, tài khoản `FEE` bắt buộc phải tồn tại (nếu thiếu thì từ chối giao dịch). | Đã kiểm (`de.md` + `loi_giai.py`) |

## B. Độ sâu & Lab
- Điểm: `P1=2 P2=2 P3=2 P4=2 P5=2 P6=2 P7=2 (Tổng=14) | P8=2 P9=2` -> Mất gốc: **ĐỦ** (về nội dung; bị chặn MUST thời lượng `< 9,0` phút)
- Lab: `L1=1 L2=2 L3=2 L4=2 L5=2` (`L1=1` vì `practice` step 0 chưa chiếu ví dụ dòng lệnh `ACC ...` / `TX ...` mẫu ngay trên màn hình)
- `covers` đúng: `3/3` (có ghi chú SHOULD về `check` chỉ chạy Python tĩnh cho mục tiêu 3)
- Số đã tính lại / mã đã chạy:
  - `checks`: `alg.prj_double_entry_sum(...) == 0`, `200+545+300+5 == 500+400+150` (`1050 == 1050`), `95+10 > 100`, `-155+150+5 == 0`: `True`.
  - Chạy thật `example..step 5` (`res=True,False,True order1=['A', 'B'] lsum=0`) và `check..step 1` (`self=False fee_ok=False total=1050`): khớp 100%.
  - Chạy `labs/PRJ/L01/loi_giai.py`: `du_lieu.txt` (0.072s), `01_bien_tu_choi.in` (0.060s), `02_quy_mo_lon.in` (0.071s) đều khớp 100%.
- Khung hình đã xem: `00012.png` (SVG khoá tăng dần), `00016.png` (công thức bất biến), `00027.png` (mã `apply_tx`), `00040.png` (bảng 3 quy mô), `00056.png` (cảnh Tự làm) — rõ nét, không lỗi hiển thị.
- Chỗ người mất gốc có thể kẹt (nếu có): `practice` step 0 chưa chiếu ví dụ `ACC`/`TX` mẫu; `example` đặt `for k in order: locks[k].acquire()` trên bài chạy đơn luồng nên học viên chưa thấy tận mắt 2 luồng chạy song song.

---

# PRJ L02 — sha16: `18204d50cceb0f5c`
- Trạng thái đọc: ĐÃ ĐỌC ĐỦ (YAML + lab + `ca_an/` + `build_report.json` + `asr_report.md` + 5 frames PNG)
- Thời lượng / từ lời đọc: `07:32` (`451,567 s` có `50 s` pause; `401,567 s` = `6,69 phút` không pause) / `1 411` từ
- `out/PRJ/L02/meta.json`: Không tồn tại; `build_report.json` ghi `spec_sha256: 4cd651b92b34fbf8...` (khác YAML hiện tại `18204d50cceb0f5c...`).
- Trạng thái ASR: `câu: 61, thiếu audio: 0, gắn cờ: 1, chưa xem xét: 0`; mục `asr_reviewed` ở khung 4 (`0.897`) **đã giữ đúng `"NOT_VERIFIED bằng tai người"`**.

## A. Chuẩn xác
| Mức | Cảnh/step | Trích nguyên chữ | Vì sao sai + bằng chứng (phép tính/lệnh) | Đề xuất sửa | Tin cậy |
|---|---|---|---|---|---|
| MUST | `covers` mục tiêu 2 & `check` | `covers: - objective: 2 / scene: check` (mục tiêu 2: "Cài đặt bảng khử trùng theo Idempotency-Key bảo đảm gửi lại 10 lần chỉ trừ tiền 1 lần") | Cảnh `check` (`Đối chứng kết quả phân trang con trỏ với OFFSET truyền thống`) **chỉ dạy và kiểm chứng phân trang con trỏ vs OFFSET**, hoàn toàn không chứa nội dung `Idempotency-Key` (nội dung này nằm ở `formula` và `example` step 2–3). Vi phạm `BRIEF_AF5.md` 2A.3. | Chuyển `covers` mục tiêu 2 sang `example` (hoặc tách/bổ sung cảnh kiểm thử `Idempotency-Key` gửi lại 10 lần vào `check` để khớp `covers`). | Đã kiểm (`YAML` + `curriculum/prj.yaml`) |
| MUST | Toàn bài | (tổng thời lượng âm thanh) | `451,567 s - 50 s = 401,567 s = 6,69 phút < 9,0 phút` không kể pause (vi phạm `BRIEF_AF5.md` 2A.6 & 2D). | Bổ sung đoạn chạy đo thật 100 000 dòng `OFFSET` vs `Keyset` trong `quymo`/`check` và giảng sâu cấu trúc JWT + bẫy timing attack để đạt ≥ 9,0 phút. | Đã kiểm (`build_report.json` + `_frames.txt`) |
| SHOULD | `labs/PRJ/L02/du_lieu.txt` vs video | `REQ k1 400 ...`, `REQ k2 500 ...`, `REQ k1 400 ...`, `REQ k3 300 ...`, `REQ k2 500 ...`, `IDS 1000`, `CURSOR 990 3` | Bộ dữ liệu `du_lieu.txt` (và đầu ra `executed=3 total_amount=1200`, `cursor_page=991,992,993`) **trùng hoàn toàn** với ví dụ trong video (`hook`, `formula`, `example`, `check`, `quiz`). Vi phạm `BRIEF_AF5.md` 2A SHOULD & giảm `L2=1`. | Đổi `du_lieu.txt` (và `mong_doi.txt`, `practice` step 1) sang bộ số liệu mới khác hẳn ví dụ video (ví dụ 6 yêu cầu có 1 thẻ sai/hết hạn, tổng tiền mới, `IDS 1200`, `CURSOR 1185 4`). | Đã kiểm (`du_lieu.txt`, `mong_doi.txt`, YAML) |
| SHOULD | `quymo` (`covers` mục tiêu 3: "Đo chi phí phân trang...") | `(~0,1 ms)`, `(~50 ms+)`, `(~0,2 ms)` | Bảng `quymo` chỉ nêu số ước lượng bằng lời mà không có mã đo thật trên 100 000 dòng như `L00 check` đã làm với `time.perf_counter()`. | Thêm bước chạy đo `time.perf_counter()` thật trên bảng 100 000 dòng (so `OFFSET 99980` và `id > 99980`). | Đã kiểm (đọc YAML) |
| SHOULD | `formula` step 0 (`say` vs `show`) & `practice` step 0 | `show`: `OFFSET 99 980 quét bỏ 99 980 dòng thừa`; `say`: `"bỏ qua chín mươi chín nghìn dòng"` | Lời đọc làm tròn `99 980` xuống `99 000` (lệch nhẹ so với màn hình); đồng thời `practice` step 0 chỉ nêu mẫu tên trường chứ chưa có ví dụ dòng dữ liệu cụ thể (`L1=1`). | Đọc chính xác `"chín mươi chín nghìn chín trăm tám mươi dòng"` và thêm 1 ví dụ input mẫu ngắn vào `practice` step 0. | Đã kiểm (đọc YAML) |

## B. Độ sâu & Lab
- Điểm: `P1=2 P2=2 P3=2 P4=2 P5=2 P6=2 P7=2 (Tổng=14) | P8=2 P9=2` -> Mất gốc: **ĐỦ** (về cấu trúc; bị chặn 2 lỗi MUST ở trên)
- Lab: `L1=1 L2=1 L3=2 L4=2 L5=2` (`L1=1` vì chưa có giá trị mẫu cụ thể trên `practice` step 0; `L2=1` vì `du_lieu.txt` trùng bộ số liệu ví dụ trong bài)
- `covers` đúng: `2/3` (`2 -> check` sai cảnh)
- Số đã tính lại / mã đã chạy:
  - `checks`: `alg.prj_idem_dedup(...) == (3, 1200)`, `400+500+300 == 1200`, `991+992+993 == 2976`, `100_000 // 20 == 5000`, `2000-1200 == 800`: `True`.
  - Chạy thật `example..step 3` (`valid=5 bad=1 executed=3 total=1200`) và `check..step 1` (`same=True ids=[991, 992, 993] empty=[]`): khớp 100%.
  - Chạy `labs/PRJ/L02/loi_giai.py`: `du_lieu.txt` (0.076s), `01_expired_tampered.in` (0.063s), `02_scale_100k.in` (0.147s) đều khớp 100%.
- Khung hình đã xem: `00013.png` (SVG 3 chốt), `00017.png` (công thức khử trùng & phân trang), `00024.png` (hàm `ok`/`sign`), `00035.png` (bảng so sánh OFFSET vs Keyset), `00051.png` (cảnh Tự làm) — bố cục sạch, chữ rõ, không tràn khung.
- Chỗ người mất gốc có thể kẹt (nếu có): Hàm `ok(tok)` trong `example` không kiểm `p[0]` rỗng (`sub` rỗng), trong khi `loi_giai.py` có `if not sub`.

---

# PRJ L03 — sha16: `275fb737e25a9873`
- Trạng thái đọc: ĐÃ ĐỌC ĐỦ (YAML + lab + `ca_an/` + `build_report.json` + `asr_report.md` + 5 frames PNG)
- Thời lượng / từ lời đọc: `07:25` (`445,000 s` có `50 s` pause; `395,000 s` = `6,58 phút` không pause) / `1 326` từ
- `out/PRJ/L03/meta.json`: Không tồn tại; `build_report.json` ghi `spec_sha256: c933d9dccd41d3f1...` (khác YAML hiện tại `275fb737e25a9873...`).
- Trạng thái ASR: `câu: 63, thiếu audio: 0, gắn cờ: 7, chưa xem xét: 0`; trong `asr_reviewed`, **4/7** mục (khung 42, 19, 37, 18) giữ đúng `"NOT_VERIFIED bằng tai người"`, còn **3/7** mục (khung 46, 1, 49) **chưa có chuỗi `"NOT_VERIFIED bằng tai người"`**.

## A. Chuẩn xác
| Mức | Cảnh/step | Trích nguyên chữ | Vì sao sai + bằng chứng (phép tính/lệnh) | Đề xuất sửa | Tin cậy |
|---|---|---|---|---|---|
| MUST | Toàn bài | (tổng thời lượng âm thanh) | `445,000 s - 50 s = 395,000 s = 6,58 phút < 9,0 phút` không kể pause (vi phạm `BRIEF_AF5.md` 2A.6 & 2D). | Bổ sung bước giải thích chi tiết từng trường hợp thiếu một/hai chiều (`miss_bank`, `miss_napas`, `miss_partner`, `extra_napas`, `one_side`) và kịch bản trả lời phỏng vấn 3 bước để đạt ≥ 9,0 phút. | Đã kiểm (`build_report.json` + `_frames.txt`) |
| SHOULD | `covers` mục tiêu 3 & `pitfalls` | `covers: - objective: 3 / scene: pitfalls` ("Trình bày ngắn gọn đánh đổi O(n log n) và bảng phương án khi phỏng vấn") | Bảng phương án phỏng vấn qua 3 quy mô nằm ở cảnh `quymo` và công thức đánh đổi nằm ở `formula`; `pitfalls` chỉ nêu 3 lỗi sai và nhắc miệng ngắn ở câu cuối lời đọc. | Sửa `covers` mục tiêu 3 trỏ tới `quymo` (hoặc bổ sung khung trình bày phỏng vấn hoàn chỉnh). | Đã kiểm (`YAML` + `curriculum/prj.yaml`) |
| SHOULD | `check` step 0 (`say` vs mã) | `for tid, src, amt, st in heapq.merge(sB, sN, sP): by_id.setdefault(tid, {})[src] = (amt, st)` | `say` nói *"giữ bộ nhớ ổn định vì chỉ cần gom theo từng mã liền kề"*, nhưng mã giả lập vẫn nạp tất cả vào `by_id` trong RAM thay vì xử lý tuần tự theo nhóm `tid` (`itertools.groupby` hoặc biến `cur_id`). | Đổi đoạn giả lập sang gom theo `cur_id` hiện tại (hoặc `itertools.groupby`) để phản ánh đúng bộ nhớ O(1) khi trộn ngoài đĩa. | Đã kiểm (đọc YAML + chạy thử) |
| SHOULD | `hook` (`checks`) & `practice` step 0 | `hook checks`: `alg.prj_reconcile_3way(['t1','t2','t3','t4'],['t1','t2','t3','t5'],['t1','t2','t3','t4']) == (3, 2)` | Trong `hook` `show` và `formula` `checks`, `t4` thiếu ở đối tác (`partner` chỉ có `['t1','t2','t3']`), còn trong `hook` `checks` lại để `'t4'` có mặt ở `partner` (thiếu ở `napas`); ngoài ra `practice` step 0 chưa chiếu ví dụ 4 cột mẫu trên màn hình (`L1=1`). | Đồng bộ `partner` thành `['t1','t2','t3']` ở `hook` `checks` và chiếu ví dụ 1–2 dòng input mẫu 4 cột ở `practice` step 0. | Đã kiểm (đọc YAML) |

## B. Độ sâu & Lab
- Điểm: `P1=2 P2=2 P3=2 P4=2 P5=2 P6=2 P7=2 (Tổng=14) | P8=2 P9=2` -> Mất gốc: **ĐỦ** (về nội dung; bị chặn MUST thời lượng `< 9,0` phút)
- Lab: `L1=1 L2=2 L3=2 L4=2 L5=2` (`L1=1` vì `practice` step 0 chưa chiếu khuôn/ví dụ đầu vào mẫu 4 cột ngay trên màn hình)
- `covers` đúng: `2/3` (mục tiêu 3 trỏ `pitfalls` thay vì `quymo`)
- Số đã tính lại / mã đã chạy:
  - `checks`: `alg.prj_reconcile_3way(...) == (3, 2)`, `2/5 == 0.4`, `len(['t1','t3','t4']) == 3`, `2/4 == 0.5`, `500_000_000 // 100_000 == 5000`, `3/5 == 0.6`: `True`.
  - Chạy thật `example..step 3` (`matched=2/5 pct=40.0% state=['t3'] one_side=['t4', 't5']`) và `check..step 2` (`merge_classify={'t1': 'match', 't2': 'state', 't4': 'one_side'}`): khớp 100%.
  - Chạy `labs/PRJ/L03/loi_giai.py`: `du_lieu.txt` (0.048s), `01_bien_lech.in` (0.044s), `02_quy_mo_lon.in` (0.052s) đều khớp 100%.
- Khung hình đã xem: `00013.png` (SVG 3 nguồn đối soát), `00017.png` (công thức O(n) vs O(n log n)), `00024.png` (mã nạp 3 nguồn), `00036.png` (bảng phương án phỏng vấn 3 quy mô), `00052.png` (cảnh Tự làm) — sạch, không chồng chữ, không cắt cụt.
- Chỗ người mất gốc có thể kẹt (nếu có): `practice` step 0 chưa liệt kê 5 nhãn thiếu chiều (`miss_partner`, `extra_napas`, `miss_bank`, `miss_napas`, `one_side`) hay ví dụ dòng `<nguon> <ma_gd> <so_tien> <trang_thai>`, học viên buộc phải mở `de.md` để biết tên nhãn chính xác.
