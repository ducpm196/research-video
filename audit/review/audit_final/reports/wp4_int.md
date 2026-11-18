# WP4 — nâng khoá INT (8 bài L00–L07) lên chuẩn AF2 — 2026-11-14

Phạm vi: chỉ INT (`lessons/int/L00..L07`, `curriculum/int.yaml`, `labs/INT/`, `audit/int/verify_int.py`, `tools/registry/symbols.INT.yaml`, sổ `audit/review/screen_code/INT.yaml`). Không chạm ACB/BNX. Không chạy build/tts/asr/audit_all/git/docker; không chạy `interview_sync_video.py` và `interview_gen_tables.py` ở chế độ ghi (chỉ `--check`).

Cách làm: INT không có bộ sinh nên sửa trực tiếp YAML (nạp YAML → sửa chuỗi → ghi lại bằng script nháp ở scratchpad, giữ `asr_reviewed` dạng flow thụt lề như cũ để khỏi vỡ `asr_review_dms.py`). Bản gốc 7 bài + sổ được chép vào scratchpad trước khi sửa.

## 1. Kết quả theo cổng (số thật; lint, render, verify, lab_gate, screen_code, curriculum, check_course_refs chạy sau lần sửa cuối; `check_curricula_graph` và `test_e52` chạy trước vài chỉnh lời đọc nhỏ cuối cùng, không đổi lộ trình hay sổ ký hiệu)

| Cổng | Kết quả |
|---|---|
| `tools/lv.py lint` từng bài | L00 35 PASS · L01 32 · L02 26 · L03 34 · L04 44 · L05 39 · L06 30 · L07 35; **0 FAIL, 0 WARN** ở cả 8 bài (gồm E51/E53 `covers` + `practice` + lab, E52 thuật ngữ, E55 chính tả) |
| `tools/lv.py render` từng bài | L00 102 khung · L01 89 · L02 88 · L03 82 · L04 98 · L05 83 · L06 83 · L07 87; **0 vấn đề** ở cả 8 bài (đã sửa tràn khung: bảng từ vựng L02, dòng mã quá dài L02/L03/L04, tiêu đề cảnh quá dài L04/L06, bảng hai nhóm L00) |
| `audit/int/verify_int.py` | **168 PASS, 0 FAIL**: 8 lab giấy bút tính lại độc lập bằng Fraction/math (mong_doi.txt = số tính lại, dòng có trong loi_giai.md và hiện trên màn hình); 13 chương trình trên màn hình ghép nguyên văn rồi CHẠY THẬT (11 Python, Java 21 `LuongAo` 10 000 luồng ảo, Java `TuGoi` mô phỏng proxy), so với khối kết quả hiện trên màn hình; số của các cảnh quy mô; luật trung thực (không 50 triệu gross/50M kể cả tiêu đề cảnh, UIT luôn kèm "dự kiến", hai nhóm vai trò ở L00 và L06, L07 có công thức tổng đãi ngộ, mục tiêu giáo án = mục tiêu đặc tả, lời đọc ≤ 2 300 từ) |
| `audit/review/lab_gate.py INT` | **8 PASS · 0 FAIL** (lời giải chạy qua `labs/cham.sh`/kiểm chữ, đối chứng âm, mỗi lab được một bài tham chiếu) |
| `audit/review/screen_code.py check --course INT` | 57 khối trong sổ + 22 nguồn; **PASS 79 · FAIL 0 · STALE 0 · MISSING 0 · ORPHAN 0 · WARN 0** (thêm 13 chương trình chạy thật + 8 khối đáp án lab; ghim lại 4 khối chỉ đổi chữ khoá→khoá; khối properties L01 đổi khoá `example 3 0` → `example 4 0`) |
| `tools/lv.py curriculum curriculum/int.yaml` | 8 bài, 8 có đặc tả, **0 lỗi** |
| `audit/check_curricula_graph.py` | 46 lộ trình, 728 bài, tham chiếu hỏng 0, chu trình 0, VER không PASS 0 |
| `python tests/test_e52.py` | 0 FAIL |
| `audit/review/check_legal.py` | 0 FAIL (87 lượt dẫn; NĐ 23/2025/NĐ-CP là CHUA_KIEM, đã ghi "cần kiểm lại hiệu lực khi dẫn") |
| `check_xref.py` | không có dòng nào của INT (chỉ BNX) |
| `check_meta.py` | 1 vấn đề, thuộc ACB L04, không phải INT |
| `check_next_refs.py` | 551 lời hẹn, 0 lệch dãy học |
| `arith_scan.py` | 240 phép tính, 0 FAIL |
| `check_course_refs.py` | chạy riêng cho INT (`check_course_refs.py int`): **0 vấn đề** (bản chạy toàn kho treo ở CPU cao, các tác tử khác cũng treo; đã dừng tiến trình của tôi) |
| `interview_sync_video.py --check` | 92 cặp trùng, 0 lệch (chế độ chỉ đọc) |
| Xem bằng mắt | Ghép 6 khung/bài thành 8 tấm (cảnh quy mô, mã chạy thật, bảng, Tự làm đề + đáp án + gợi ý, SVG ba vòng L07, bảng hai nhóm L00/L06): đã xem cả 8 tấm (48 khung); sheet chụp từ bản dựng khung trước vài chỉnh sửa lời đọc nhỏ, bản cuối đã `render` lại 0 vấn đề |


## 2. Mỗi bài đã thêm gì

Mọi bài: `af2: true`; `covers` (mục tiêu giáo án viết lại đúng điều bài dạy, mục tiêu "LÀM" trỏ tới cảnh `example`/`practice`); cảnh `practice` (Tự làm) + lab giấy bút `labs/INT/Lxx/{de.md, mong_doi.txt, loi_giai.md}` (đề dạng "trả lời một câu phỏng vấn có số", số liệu khác ví dụ của bài); cảnh quy mô/thời gian chạy thật (Python hiện nguyên văn mã + kết quả, kèm bảng "điều gì gãy / cách người làm nghề xử lý / đánh đổi"); thuật ngữ giảng tại chỗ; chính tả chuẩn E55 (`khoá`, `tệp`); bỏ mọi `50 triệu gross` ở recap.

| Bài | Cảnh mới | Mã chạy thật trên màn hình | Lab (số liệu lab) |
|---|---|---|---|
| L00 lộ trình | `quymo` (Little ×1/×100/×10 000; phút ngừng theo số chín); bước "hai nhóm vai trò A/B" ở `concept`; công thức gói thu nhập `T = L × (13 + k)` với L = 40 (số minh hoạ) thay cho 50M | Python | 8 000 tps × 25 ms = 200; 99,95% = 262,8 phút; phân nhóm tin B |
| L01 CS/Java | `quymo` (cây B-Tree ×1/×1 000/×1 000 000); bước chạy 10 000 luồng ảo Java 21 | Python; Java 21 `LuongAo` | 80 triệu dòng, 500 nhánh → 3 tầng, 4 lần đọc; 2 000 MB so với 4 000 000 byte |
| L02 Spring/REST | `chaythat` (MÔ PHỎNG lớp vỏ bằng `java.lang.reflect.Proxy`: tự gọi nội bộ chỉ mở 1 giao dịch); `quymo` (bể kết nối 17 chỉ đỡ 850 tps) | Java `TuGoi`; Python | bể 34; trần 1 700 và 1 360 tps (REQUIRES_NEW giữ thêm kết nối) |
| L03 phân tán | `quymo` (2PC giữ khoá 40/400/4 000 ms → 400/4 000/40 000 s so với SAGA 40 s) | Python | 24 000 dòng, lô 2 000; 48 000 so với 24 lần đổi ngữ cảnh; trần 33 so với 333 tps |
| L04 nghiệp vụ | `chaythat` (bản đồ bit 3,4,11,37,52 và khối PIN); `quymo` (đối soát ×1/×10/×100: 2,5 giờ so với 0,21 giây … 25 000 giờ so với 27,3 giây); bỏ "Bước 3" ước lượng cũ (quymo thay thế) | Python ×2 | bitmap 2220000000800000; LTV 168; DTI 25%; thu từng phần 7,5 + thiếu 4,5 |
| L05 AI | `chaythat` (4400,0; 18,67; UCB1 1,21/1,77; cosine 0,992); `quymo` (nhân xử lý: nhẹ 1/10/100, nặng 40/400/4 000) | Python ×2 | 36 và 480 nhân; Z = 10; UCB1 1,13 và 1,93 → chọn B; cosine 0,707 |
| L06 100 câu | bước "hai nhóm vai trò" (bảng nhóm câu hỏi A/B) ở `prereq`; `quymo` (đề 10 000 tps: 120/1 200/12 000 yêu cầu dở; 1/3/24 máy +1; chuỗi 4 tầng 99,96% = 210,2 phút) | Python ×2 | 400 yêu cầu dở; 4 máy; 262,8 phút; chuỗi 3 tầng 99,85% và 788,0 phút; ngưỡng sinh trắc học |
| L07 đàm phán | Viết lại: hỏi khung lương, công thức `T = L × (13 + k) + 12 × P` (số minh hoạ), so hai offer, đòn ép giá số 3 tính bằng số (lương cứng thấp kéo cả thưởng xuống), `quymo` thời gian (mất 60 / 194,8 / 352 triệu sau 1/3/5 năm, giả định tăng 8%/năm), SVG ba vòng (E39) | Python | A 570, B 534, A hơn 36, B cần phụ cấp 5 triệu/tháng |

## 3. Yêu cầu riêng từ JD mới

- **Hai nhóm vai trò** (backend microservices hiện đại so với hệ cũ/nghiệp vụ): L00 (`concept`, bảng A/B + chú giải hệ cũ, hỗ trợ mức 3, SLA; lab L00 có câu phân nhóm tin) và L06 (`prereq`, bảng "câu hay được hỏi về dữ liệu/nghiệp vụ/vận hành" theo nhóm + cách chọn trọng tâm ôn). Nguồn nêu là "một số tin tuyển dụng backend ngân hàng", không lấy tên ngân hàng làm nguồn sự thật; có dặn đối chiếu trang chính thức.
- **L07 không còn số lương không nguồn**: tiêu đề đặc tả + giáo án đổi thành "Chiến lược Đàm phán Lương: Hỏi Khung, Tính Tổng Đãi ngộ và Đối đáp Ba Vòng" (id và tên tệp giữ nguyên); mọi số tiền là "số minh hoạ" ghi ở đề, mã và lab; điều có nguồn duy nhất giữ lại là phúc lợi chính thức của tin ACB (lương ghi "Thương lượng", tháng 13 cố định, thưởng 1–4 tháng tuỳ xếp loại). Gỡ: 50M/700–850 triệu/42–46 triệu/số ngày thử việc "60" và dẫn Điều 25 BLLĐ (không có trong `audit/legal/registry.yaml`; thay bằng "luật lao động giới hạn thời gian thử việc, cần kiểm lại văn bản hiện hành"). Đã gỡ cả `50 triệu gross` ở recap L01–L06 và `50M` ở tiêu đề recap L07, nhờ `verify_int.py` bắt thêm một chỗ sót ở L00.
- Kiểm không bị vỡ: `interview_sync_video.py --check` → 92 cặp trùng, 0 lệch (không đụng `out/`); `interview_gen_tables.py` lấy tiêu đề từ đặc tả và cắt tiền tố `Chuyên đề N —` (tiền tố được giữ), tên tệp `07_salary_negotiation_50m_gross` không đổi nên không vỡ.
- Trung thực CV (theo bộ nhớ dự án): UIT luôn "dự kiến tốt nghiệp 11/2026", dự án AI chỉ là nguyên mẫu học thuật; không nói ACB dùng T24; số lương và sự cố không bịa (còn `[điền số thật theo bảng lương]` ở L07 như cũ); pháp lý: chỉ dẫn văn bản có trong registry, NĐ 23/2025/NĐ-CP (CHUA_KIEM) thêm "cần kiểm lại hiệu lực khi dẫn". `verify_int.py` có các cổng trung thực (không 50 triệu gross, UIT kèm "dự kiến", L07 không số ngày thử việc…). Toàn bộ nội dung về người dùng chỉ nằm trong kho.

## 4. P1 (thuật ngữ tại chỗ) và E52

Thêm 9 mục `term:` vào `tools/registry/symbols.INT.yaml` (gross, lũy đẳng, nguyên tử, bể kết nối, HikariCP, OFS, ISO 8583, lớp vỏ ủy quyền, bean) với `introduces` đúng step giảng và `assumes` ở bài sau; lint E52 PASS. Giảng thêm tại chỗ: hệ cũ/mức 3/SLA (L00, L06), CPU/RAM/`finally` (L01), HTTP/hàm tạo/CGLIB/JSON/hàm băm (L02), Oracle/PL/SQL (L03), dòng nóng (L03, nói trong lời đọc và de.md), nhân xử lý/số minh hoạ (L04, L05), BATNA/BHXH/công thức tổng đãi ngộ (L07). Tách "bean" khỏi hook L02 (dùng trước khi giảng). Chưa có người đọc độc lập; P1 dự kiến = 2 ở các bài còn lại là TỰ ĐÁNH GIÁ, NOT_VERIFIED.

## 5. Mục không làm / còn mở (kèm lý do)

1. Mã Spring, Redis, Kafka, PL/SQL, ONNX, OFS vẫn là `syntax`/`other` trong sổ như SC1 (máy không có các sản phẩm đó; không bịa đầu ra); `unverified_claims` giữ nguyên 37 mục. Phần chạy thật là mô phỏng/tính toán bằng Python và Java 21, ghi rõ "MÔ PHỎNG" ở L02.
2. Không dựng lại video, không TTS, không ASR: các câu mới/đổi cần ASR và nghe lại sau khi dựng (người điều phối); các mục `asr_reviewed` của câu không còn trong bài đã gỡ (E30).
3. Tài liệu ngoài phạm vi vẫn còn "50M gross", cần người điều phối đồng bộ sau: `interview/00_overview_roadmap.md`, `interview/06_interview_qa_bank_100.md`, `interview/07_salary_negotiation_50m_gross.md` (và `MASTER_CURRICULUM_INDEX.md` các dòng viết tay), `interview/HANDOVER_INTERVIEW.md`, `interview/SOURCE_CODE_VIDEO_MAP.md`, `HOC_TAP.md/.html`, `state/knowledge-graph.md`; CV md/pdf (`resources/job/`) không đụng.
4. `check_meta.py` còn 1 vấn đề nhưng thuộc ACB L04 (đặc tả "Khoá" so với lộ trình "Khóa"), không phải INT.
5. Số ngày thử việc/Điều 25 BLLĐ 2019 đã gỡ; nếu cần dạy lại số ngày, trước tiên thêm văn bản (45/2019/QH14) vào `audit/legal/registry.yaml`.

## 6. Đề xuất tách bài

- **L04** (2 296 từ, sát trần 2 300, sau khi đã cắt 3 đoạn và thay "Bước 3" bằng cảnh quy mô): nên tách thành hai bài, "OFS + IBM MQ + ISO 8583 + khối PIN/HSM + mã 68" và "tín dụng bán lẻ (LTV, DTI, CIC, trích nợ từng phần, thấu chi cầm cố) + đối soát EOD". Chưa tự tách/đánh số lại.
- L00, L01, L03, L02 ở khoảng 2 000–2 200 từ; còn dư địa dưới trần.

## 7. Tệp đã đổi hoặc tạo

`lessons/int/L00..L07*.yaml`; `curriculum/int.yaml` (tiêu đề L00, L07; mục tiêu chép từ đặc tả; `fix`/`example` của L07); `tools/registry/symbols.INT.yaml`; `audit/review/screen_code/INT.yaml`; `audit/int/verify_int.py`; `labs/INT/L00..L07/{de.md, mong_doi.txt, loi_giai.md}`; báo cáo này. `out/INT/*/frames` bị `lv.py render` ghi lại (không phải sản phẩm dựng; `out/INT/*/L0x.mp4` và `interview/video/` không đổi).
