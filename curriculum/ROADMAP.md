# Chương trình nền tảng AI · Khoa học máy tính · Khoa học dữ liệu · Công nghệ thông tin — lộ trình và tầm nhìn

Cập nhật 2026-10-30. Tài liệu này mô tả **kiến trúc chương trình, lộ trình theo nghề, độ phủ so với chuẩn, cách bảo đảm chất lượng và kế hoạch dài hạn**.
Số liệu thay đổi hằng ngày nằm ở hai tệp **sinh tự động**, không sửa tay:
- [`STATUS.md`](STATUS.md): hiện trạng từng khoá: số bài, đặc tả, video hoàn thiện, phút, bộ kiểm độc lập.
  - Sinh bởi `audit/review/audit_all.py` rồi `audit/review/status_report.py`.
- [`TRACKS.md`](TRACKS.md): lộ trình theo nghề, liệt kê đúng từng bài cần học theo thứ tự thoả mọi tiên quyết.
  - Sinh bởi `audit/review/tracks.py` từ [`tracks.yaml`](tracks.yaml).

**Nhãn bằng chứng:**
- **OBSERVED:** đã chạy hoặc đọc trong phiên.
- **CITED:** có nguồn tra được, đã đọc nguyên văn.
- **INFERRED:** suy luận.
- **NOT_VERIFIED:** chưa kiểm.

## 1. Mục tiêu và nguyên tắc

**Người học:** người mới hoặc mất gốc, chỉ có video trong tay. **Đích đến:** nền đủ vững để tự học tiếp và làm việc như kỹ sư, nhà khoa học trong các mảng AI, khoa học máy tính, dữ liệu, hệ thống.

Sáu nguyên tắc không đổi:
1. **Chỉ dạy điều kiểm được.** Mỗi con số được máy tính lại ba lần:
   - mã VER trong giáo án (`audit/verify_plan_curricula.py`);
   - bộ kiểm độc lập của khoá (`audit/<khoá>/verify_<khoá>.py`), tính bằng một cách khác;
   - `checks` chạy cùng lint của từng bài.
2. **Không lặp lỗi của nguồn.** Mỗi bài trong lộ trình có trường `fix`, ghi phát biểu hay bị nói sai và cách nói đúng.
3. **Bài tự đủ.** Không nhắc “tài liệu”, “slide”. Nhắc bài trước thì nói lại nội dung. Bài sau chỉ nhắc ở mở đầu hoặc tổng kết.
4. **Kinh nghiệm chuyên gia.** Bài mở bằng tình huống thật có con số. Bài cuối mỗi khoá là bài tình huống chuyên gia. Khoá CAS phân tích sự cố có thật theo báo cáo điều tra gốc (§6).
5. **Một giọng mỗi bài, phát âm kiểm bằng máy nghe.** Giọng vi-VN-NamMinhNeural. Chỉ khi giọng gốc bị chặn mới đổi giọng dự phòng, và đổi cho cả bài. Mọi câu bị máy nghe gắn cờ đều được xem xét, có ghi lý do.
6. **Nhất quán.** Trong toàn chương trình:
   - một ký hiệu cho một khái niệm (sổ ký hiệu, lint E12–E14);
   - một cách viết cho một từ (lint E38);
   - một tên chuỗi, một giọng cho mỗi khoá (`check_meta.py`);
   - bản đồ khoá ở bài 0 liệt kê đủ mọi bài (lint E37).

## 2. Kiến trúc chương trình: 8 tầng, 38 khoá, 575 bài (OBSERVED, đếm từ `curriculum/*.yaml`)

| Tầng | Khoá (số bài) | Vai trò |
|---|---|---|
| **T0 · Toán nền** (82) | DMS Toán rời rạc (20) · CS115 Toán cho KHMT và học máy (45) · RBM Toán cho robot (17) | lôgic, chứng minh, đếm, đại số tuyến tính, giải tích, tối ưu, xác suất–thống kê, toán của chuyển động |
| **T1 · Khoa học máy tính lõi** (115) | CS112 Thuật toán (29) · TOC Lý thuyết tính toán (14) · PLC Ngôn ngữ lập trình (13) · CSA Hệ thống máy tính (16) · OSY Hệ điều hành (15) · NET Mạng (15) · **PAR Song song và GPU (13)** | máy tính chạy chương trình như thế nào, giới hạn của tính toán, hiệu năng |
| **T2 · Kỹ nghệ phần mềm** (83) | SWF Phần mềm đúng đắn (13) · SDP Kỹ thuật lập trình và mẫu thiết kế (17) · DVO DevOps (13) · SAR Kiến trúc hệ thống (13) · WEB Web và di động (15) · **HCI Tương tác người–máy (12)** | viết, kiểm, phát hành, thiết kế hệ thống và giao diện cho người dùng |
| **T3 · Dữ liệu** (97) | DBS Cơ sở dữ liệu (17) · DAN Phân tích dữ liệu (12) · DSC Khoa học dữ liệu (15) · DSY Hệ phân tán (15) · DEN Kỹ thuật dữ liệu (14) · EVT Hướng sự kiện và dữ liệu luồng (11) · **IRS Truy hồi và hệ gợi ý (13)** | lưu, truy vấn, phân tích, suy luận, xử lý dữ liệu lớn và luồng, tìm kiếm, gợi ý |
| **T4 · Trí tuệ nhân tạo** (79) | AIF Nền tảng AI (14) · LLM Mô hình ngôn ngữ lớn (14) · AGT AI agent (12) · MLO MLOps (14) · **RLN Học tăng cường (13)** · **CVI Thị giác máy tính (12)** | tìm kiếm và suy luận, học sâu cho ngôn ngữ và ảnh, tác tử, học tăng cường, đưa mô hình vào sản xuất |
| **T5 · Hạ tầng và an toàn** (55) | CLD Microservice và Kubernetes (16, gồm bài hành trình L15) · CLC Điện toán đám mây (12) · SEC An toàn thông tin (15) · BCH Blockchain (12) | chạy hệ thống ở quy mô lớn, bảo vệ nó |
| **T6 · Hệ vật lý và đồ hoạ** (41) | ESY Hệ nhúng và thời gian thực (15) · ROB Robot tự hành (13) · **GFX Đồ hoạ máy tính (13)** | phần mềm gặp thế giới vật lý: cảm biến, chuyển động, ánh sáng |
| **T7 · Nghề nghiệp và tình huống chuyên gia** (23) | **SEP Xã hội, đạo đức và nghề nghiệp (11)** · **CAS Tình huống chuyên gia: sự cố có thật (12)** | trách nhiệm, pháp lý dữ liệu, công bằng, rủi ro; đọc sự cố như người điều tra |

**In đậm:** 8 khoá chốt thêm ngày 2026-10-30 (99 bài, đang ở mức giáo án kế hoạch, mọi ví dụ đã PASS mã VER). Vì sao chọn đúng 8 khoá này:
- GFX, HCI, SEP là ba lĩnh vực của CS2023 trước đó chưa có khoá (§5).
- PAR, RLN, CVI, IRS là bốn mảng mà chuyên gia AI và hệ thống cần, nhưng kho mới chạm thoáng qua:
  - PAR: mới có Amdahl ở CSA L13;
  - RLN: mới có một bài CS115 L39;
  - CVI: mới có CS115 L34 và ROB L11;
  - IRS: mới có DEN L07 và LLM L12.
- CAS đáp ứng yêu cầu “vận dụng tình huống kinh nghiệm cụ thể của các chuyên gia”.

Mã khoá đồ hoạ là **GFX** chứ không phải GIT (tên lĩnh vực trong CS2023), để người học không lẫn với công cụ Git của DVO.

## 3. Hiện trạng (OBSERVED — tóm tắt lúc 2026-10-31T01:25Z; chi tiết từng khoá ở [`STATUS.md`](STATUS.md))

| Tầng | Bài | Có đặc tả | Hoàn thiện | Phút hoàn thiện | Khoá đã hoàn thiện trọn |
|---|---|---|---|---|---|
| T0 · Toán nền | 82 | 82 | 82 | 571 | DMS, CS115, RBM |
| T1 · KHMT lõi | 115 | 102 | 102 | 556 | CS112, TOC, PLC, CSA, OSY, NET |
| T2 · Kỹ nghệ phần mềm | 83 | 71 | 71 | 268 | SWF, SDP, DVO, SAR, WEB |
| T3 · Dữ liệu | 97 | 84 | 84 | 342 | DBS, DAN, DSC, DSY, DEN, EVT |
| T4 · Trí tuệ nhân tạo | 79 | 54 | 54 | 228 | AIF, LLM, AGT, MLO |
| T5 · Hạ tầng và an toàn | 55 | 55 | 55 | 226 | CLD, CLC, SEC, BCH |
| T6 · Hệ vật lý và đồ hoạ | 41 | 28 | 28 | 121 | ESY, ROB |
| T7 · Nghề nghiệp và tình huống | 23 | 0 | 0 | 0 | — |
| **Tổng** | **575** | **476** | **476** | **2312** | |

Số phút mỗi tầng được làm tròn riêng, nên cộng các tầng có thể lệch tổng 1–2 phút; tổng lấy từ STATUS.md.

- **“Hoàn thiện”** nghĩa là đủ năm điều:
  - đã dựng;
  - lint 0 FAIL, 0 WARN theo bộ luật hiện hành;
  - video khớp dấu băm của đặc tả và lời đọc hiện tại;
  - đúng một giọng;
  - máy nghe không còn câu nào chưa xem xét.
- **Mọi bài đã có đặc tả đều hoàn thiện** (476/476, 30 khoá). 99 bài còn lại thuộc 8 khoá chốt ngày 2026-10-30, mới ở mức giáo án, chưa có đặc tả: PAR 13, HCI 12, IRS 13, RLN và CVI 25, GFX 13, SEP và CAS 23 (xem §8.1).
- **Hoàn thiện ≠ đủ sâu cho người mất gốc.** Rà sư phạm 2026-10-31 (`audit/review/PEDAGOGY_REVIEW.md`, `pedagogy_scan.py`): theo chuẩn
  độ sâu E39, toàn kho có 6 bài ĐỦ, 30 GẦN, 440 MỎNG; 19 khoá dựng đợt 2026-10-28…30 là bản nén (khoảng 4,5 phút, 1 step số, 0 hình).
  Kế hoạch nâng độ sâu ở §8.1 mục 2. Bài mẫu đạt chuẩn: LLM L05 (viết lại), CLD L15 (bài hành trình).
- **Kiểm cuối (2026-10-31T01:25Z):** `audit_all` 476 bài, 0 vấn đề; `tts_speed_scan` 22 338 câu, 0 câu nghi cụt; `tests/test_lint.py` 0 FAIL; mọi bài đúng một giọng (vi-VN-NamMinhNeural), chưa bài nào phải dùng giọng dự phòng.
- **Tốc độ dựng** (từ 2026-10-30, `audit/review/production_log.tsv`): trung vị khoảng 2–3 phút mỗi bài mới — máy nghe chạy GPU, edge-tts tự đọc lại câu hỏng trước khi báo chặn. Trước đó 10,7 phút (bình thường) đến 26 phút (edge-tts bị chặn).
- **Bộ kiểm của toàn bộ giáo án:**
  - `verify_plan_curricula.py`: 439/439 PASS;
  - `check_curricula_graph.py`: 38 lộ trình, 575 bài, không tham chiếu hỏng, không chu trình;
  - `tests/test_lint.py`: 0 FAIL, chứng minh lint bắt được từng lỗi E1–E40.

## 4. Lộ trình theo nghề (thứ tự từng bài: [`TRACKS.md`](TRACKS.md))

Mỗi nghề chỉ khai **mục tiêu** trong `tracks.yaml`. Máy tính bao đóng tiên quyết ở mức từng bài rồi sắp theo tô pô, nên mỗi lộ trình chỉ gồm đúng các bài nền mà mục tiêu cần, không thiếu, không thừa. Script kiểm lại từng cạnh tiên quyết sau khi sắp. Khi hai khoá không ràng buộc nhau, thứ tự theo tầng ở §2. Ví dụ: DMS (quy nạp, đồ thị) học trước CS112.

| Nghề | Mục tiêu chính (ngoài nền chung DMS → CS112 → CS115 L00–L21, L44) | Tình huống chuyên gia ở cuối |
|---|---|---|
| Kỹ sư AI / học máy | CS115 trọn, AIF, DSC, MLO, CVI, RLN, PAR (Amdahl, huấn luyện phân tán) | CVI L11 học lối tắt · RLN L12 đánh giá ngoại tuyến · PAR L12 8 GPU · CAS L10 Flu Trends |
| Kỹ sư LLM và AI agent | LLM, AGT, IRS L00–L05, RLN L10–L11, SEC L04, L06, MLO L06–L13 | AGT · IRS · CAS L00 hậu kiểm |
| Khoa học dữ liệu / phân tích | DBS L00–L03, DAN, DSC, MLO L08–L10 | DAN L11 · DSC · CAS L10 |
| Kỹ sư dữ liệu | DBS, DSY, DEN, EVT | EVT L10 · CAS L08 GitLab |
| Fullstack web và di động | SWF, SDP, DBS, WEB, HCI, DVO, SEC L00–L06 | HCI L11 cảnh báo khẩn · CAS L05 Knight, L07 Cloudflare |
| DevOps, SRE, đám mây, Kubernetes | OSY, NET, CLD, CLC, DVO, SAR | CAS L05–L08 |
| Kiến trúc sư hệ thống lớn | SAR, DSY, EVT, CLD, DEN, SEC L11–L14 | SAR L12 · CAS trọn |
| An toàn thông tin (phòng thủ) | SEC, NET, OSY, CSA L00–L04, WEB L09 | CAS L09 Heartbleed · SEP L07 công bố lỗ hổng |
| Hệ nhúng và robot | ESY, RBM, ROB, CVI L03, L05–L06 | CAS L01 Patriot, L02 Ariane 5, L03 MCO, L04 Pathfinder |
| Đồ hoạ và thị giác | GFX, CVI, PAR L06–L09 | GFX L12 độ sâu · CVI L11 |
| Khoa học máy tính lõi | CS112, TOC, PLC, CSA, OSY, NET, DSY, PAR | CS112 L27 bài tập lớn · PAR L12 |
| Blockchain | BCH, SEC L07–L10 | BCH |

Mọi nghề đều nên học SEP. Số bài của từng lộ trình cùng số bài đã có video: xem TRACKS.md.

## 5. Độ phủ so với chuẩn (INFERRED từ nội dung giáo án; chuẩn CITED)

**CS2023 (ACM/IEEE/AAAI): 17 lĩnh vực kiến thức.** Nguồn: “Introduction to Knowledge Model”, sha256 `c51b590a2a6e6d98`. Sau đợt bổ sung, lĩnh vực nào cũng có khoá riêng:

| Lĩnh vực | Khoá |
|---|---|
| AI | AIF, LLM, AGT, RLN, CVI; CS115 (học máy, học sâu) |
| AL Thuật toán | CS112; TOC L13 |
| AR Kiến trúc | CSA |
| DM Quản lý dữ liệu | DBS, DEN |
| FPL Nền tảng ngôn ngữ | PLC; TOC L06–L08 |
| GIT Đồ hoạ và kỹ thuật tương tác | **GFX**; CVI |
| HCI | **HCI**; WEB L11 |
| MSF Toán nền | DMS, CS115, RBM |
| NC Mạng | NET |
| OS Hệ điều hành | OSY |
| PDC Song song và phân tán | **PAR**, DSY, EVT |
| SDF Nền tảng phát triển phần mềm | CS112, SDP, SWF |
| SE Công nghệ phần mềm | SWF, SDP, DVO, SAR |
| SEC An toàn | SEC; CAS L09 |
| SEP Xã hội, đạo đức, nghề nghiệp | **SEP**, CAS |
| SF Nền tảng hệ thống | CSA, OSY, SAR |
| SPD Nền tảng chuyên biệt | WEB (web, di động), ESY (nhúng), ROB (robot), BCH, CLC |

**ACM Data Science Task Force (2021): 11 lĩnh vực.** Nguồn: `DSTF_Final_Report.pdf`, sha256 `eaa9929c6b74446c`.

| Lĩnh vực | Khoá |
|---|---|
| AP Phân tích và trình bày | DAN, DSC |
| AI | AIF, CS115 |
| BDS Hệ dữ liệu lớn | DSY, DEN, EVT |
| CCF Nền tảng máy tính | CSA, OSY, NET |
| DG Thu thập, quản lý, quản trị dữ liệu | DBS, DEN, SEP L01 |
| DM Khai phá dữ liệu | DSC, CS115 |
| DP Riêng tư và an toàn dữ liệu | SEC, SEP, DSC L13 |
| ML | CS115, MLO |
| PR Tính chuyên nghiệp | SEP, CAS |
| PDA Lập trình, cấu trúc dữ liệu, thuật toán | CS112, SDP |
| SDM Phát triển và bảo trì phần mềm | SWF, DVO, MLO |

Báo cáo DSTF còn đòi giải tích, cấu trúc rời rạc, xác suất, thống kê và đại số tuyến tính. Các phần này nằm ở DMS và CS115.

**Kiến trúc có hai nghĩa:**
- **Kiến trúc máy tính** (bộ nhớ đệm, đường ống lệnh) nằm ở CSA.
- **Kiến trúc hệ thống phần mềm** (thành phần, dữ liệu, đánh đổi) nằm ở SAR.

## 6. Bài tình huống chuyên gia

**Hai loại** (chi tiết ở `.claude/skills/lecture-video/references/case-lessons.md`):
- **Sự cố có thật.** Chỉ khẳng định điều báo cáo điều tra gốc ghi. Con số của báo cáo được tính lại bằng kiến thức đã học. Không nêu tên cá nhân. Nội dung an ninh chỉ ở mức phòng thủ.
- **Quyết định nghề nghiệp.** Tình huống tiêu biểu dựng từ cơ chế đã học, con số ghi “(số minh hoạ)”.

**Khoá CAS** gồm 12 bài. Nguồn đều đã đọc nguyên văn trong phiên 2026-10-30, trừ lệnh của SEC về Knight Capital: trang sec.gov chặn tải, nên lấy qua bản trích có dẫn đoạn.

| Bài | Sự cố | Con số được tính lại |
|---|---|---|
| L00 | phương pháp hậu kiểm không đổ lỗi | xác suất lọt qua nhiều lớp phòng vệ |
| L01 | Patriot, Dhahran 1991 (GAO/IMTEC-92-26) | 0,1 cắt còn 23 bit phần lẻ → sau 100 giờ lệch 0,3433 s, khớp bảng Phụ lục II của GAO |
| L02 | Ariane 5, chuyến bay 501 (báo cáo hội đồng điều tra 1996) | giới hạn số nguyên 16 bit có dấu |
| L03 | Mars Climate Orbiter 1999 (báo cáo MIB) | lệch hệ số 4,45; cận điểm 57 km |
| L04 | Mars Pathfinder 1997 | đảo ngược ưu tiên, mô phỏng |
| L05 | Knight Capital 2012 | 7 trên 8 máy chủ; trên 10 triệu USD mỗi phút |
| L06 | Amazon S3 2017 | từ 9:37 tới 13:54 là 4 giờ 17 phút |
| L07 | Cloudflare 2019 | số bước của bộ khớp quay lui tăng theo n³ |
| L08 | GitLab 2017 | khoảng mất dữ liệu 6 giờ thay vì 24 giờ |
| L09 | Heartbleed 2014 | trường độ dài 16 bit, tối đa 65 535 byte |
| L10 | Google Flu Trends 2013 (Lazer và cộng sự, 2014) | dự báo gấp đôi CDC |
| L11 | sự cố năm 2038 | 2³¹ − 1 giây sau mốc 1970 là 03:14:07 UTC ngày 19/1/2038 |

**Bài cuối của 8 khoá mới:**
- PAR L12: 8 GPU mà chỉ nhanh gấp 3.
- RLN L12: đánh giá chính sách từ nhật ký cũ.
- CVI L11: mô hình học lối tắt.
- GFX L12: cảnh ở xa bị nhấp nháy.
- IRS L12: hệ gợi ý hai tầng trong 100 ms.
- HCI L11: thiết kế lại giao diện cảnh báo khẩn, theo báo cáo FCC về Hawaii 2018.
- SEP L10: left-pad 2016.
- CAS: cả khoá.

**Các khoá đã có:**
- Đã có bài tổng hợp: SDP L16, SAR L12, AIF L13, CS112 L27–L28, CS115 L33.
- **Loại thứ ba — bài hành trình theo trục thời gian** (người dùng yêu cầu 2026-10-31; `--kind journey`, lint E40; case-lessons.md mục 5).
  Một hệ thống thật đi qua các chặng khai sinh → tăng trưởng → quy mô lớn → ổn định → tiếp tục phát triển. Ở mỗi chặng: quy mô có nguồn,
  điểm nghẽn, cách chuyên gia xử lý, thực hành tốt kèm điều kiện áp dụng, và một con số tính lại.
  Bài mẫu đã dựng: **CLD L15 — từ Borg tới Kubernetes** (11,6 phút; nguồn EuroSys 2015, ACM Queue 2016, blog Kubernetes 2024, câu trích ở
  `audit/cld/sources_L15.md`). Mỗi khoá còn lại sẽ có một bài như vậy (§8.1 mục 3).

## 7. Bảo đảm chất lượng: các cổng và công cụ

| Cổng | Kiểm gì | Công cụ |
|---|---|---|
| Giáo án | phạm vi theo chuẩn, không trùng khoá khác; mọi con số PASS mã VER; đồ thị tiên quyết không chu trình | `verify_plan_curricula.py`, `check_curricula_graph.py`, `lv.py curriculum` |
| Đặc tả bài | ký hiệu giới thiệu trước khi dùng; lý do cho từng bước; `checks` cho mọi con số; câu đọc được; “bài N” đúng; bản đồ khoá đủ (E37); chính tả thống nhất (E38) | `lv.py lint` (E1–E40), `tests/test_lint.py` |
| Kiểm độc lập | khẳng định của bài được tính lại bằng cách khác | `audit/<khoá>/verify_<khoá>.py` |
| Bố cục | không tràn, không đè, viền không chạm chữ | `render`, `audit/layout_scan.py` |
| Phát âm | hai mô hình máy nghe nghe mọi câu; câu gắn cờ phải có lý do dẫn bản chép; câu ngắn nghe sai thì viết lại | `lv.py asr`, `audit/review/asr_flags.py`, `audit/dms/asr_review_dms.py` |
| Toàn kho | video khớp dấu băm đặc tả và lời đọc; một giọng; tham chiếu; siêu dữ liệu | `audit/review/audit_all.py`, `check_course_refs.py`, `check_meta.py` |
| Báo cáo | hiện trạng và lộ trình sinh từ dữ liệu, không gõ tay | `status_report.py`, `tracks.py` |

**Lỗi thật mà các cổng đã bắt trong đợt này:**
- **Bản đồ khoá thiếu bài.** CS115 L00 ghi “bài 34–43: mở rộng”, bỏ sót bài 44 (thống kê). Đã sửa bài 0, bài 33 và bài 44, rồi thêm luật E37.
- **Chính tả không thống nhất.** Lẫn “luỹ/lũy”, “tùy/tuỳ”, “logarit/lôgarit”, “tỷ/tỉ”, “vectơ/vector”. Đã thống nhất và thêm luật E38.
- **Mã VER kiểm số đã sửa.** Mã EVT:L09 vẫn kiểm con số 6 ngày đã sửa thành 7,5 ngày.
- **Tính nhẩm sai.** nDCG đúng là 0,985 (đã ghi 0,986), bước SGD đúng là (1,025; 2,05) (đã ghi 1,05).
- **Phép kiểm luôn đúng.** DMS L00, L07 có phép kiểm luôn trả về đúng, nên không kiểm gì.
- **Hàm kiểm trùng tên.** Hàm của DAN che hàm cùng tên của DBS.
- **Tên bài lệch.** 15 tên bài trong lộ trình khác tên hiển thị trong video.
- **Báo cáo máy nghe cũ.** 31 `asr_report.md` (CSA, DBS, PLC, RBM) vẫn ghi “chưa xem xét” dù đặc tả đã có đủ lý do, vì báo cáo chưa sinh lại. Đã sinh lại cả 31, và `audit_all.py` nay báo loại lệch này.
- **Câu quá ngắn bị nghe sai.** SWF, DSY, DSC có 13 câu ngắn bị máy nghe chép sai, ví dụ “Một, mạng luôn tin cậy.” chỉ khớp 0,6. Đã viết dài ra rồi dựng lại; `asr_flags.py` đánh dấu sẵn loại câu này.
- **Âm thanh cụt đuôi lọt kiểm.** AIF L08, CSA L11, DBS L15 có câu cụt (0,16–0,19 giây/từ) mà ngưỡng cũ 0,15 không bắt; hai lý do HAND cũ còn quy nhầm cho máy nghe. Đã dựng lại, sửa lý do; câu ≥ 4 từ nay dùng ngưỡng 0,20, `audit_all` báo “âm thanh cụt”, `tts_speed_scan.py` quét toàn kho (22 185 câu, 0 câu nghi cụt).
- **Câu ngắn và câu đổi nghĩa ở đợt 2026-10-30/31.** Khoảng 40 câu ở 14 khoá (phần lớn dạng “Bảng …” 3–5 từ) bị máy nghe chép sai, có câu đổi nghĩa (“Bảng đếm số kênh” → “Bạn đếm…”, “7 chữ số” → “7 triệu số”). Đã viết lại rồi dựng lại từng bài.
- **Bộ nháp lý do HAND (`asr_hand_gen.py`) ghi sai khi chưa đọc lại.** Các lỗi đã gặp: “ghi” (từ Việt) bị coi là GB, “ích/xê” bị coi là chữ cái, “mê-ga” khớp trong “ô-mê-ga”. Đã sửa bộ sinh và một lý do sai đã ghi (DEN L10). Quy tắc: luôn đọc lại từng lý do trước khi ghi.

- **Bài đúng nhưng nén, chưa đủ cho người mất gốc** (rà 2026-10-31, `audit/review/PEDAGOGY_REVIEW.md`). 270 bài của 19 khoá dựng đợt
  2026-10-28…30 chỉ có 6 phân cảnh, 1 step làm bằng số, 0 hình, khoảng 4,5 phút. Toàn kho theo luật mới: 6 bài ĐỦ, 30 GẦN, 440 MỎNG. Đã thêm
  chuẩn độ sâu (pedagogy.md luật 22, lint **E39** khi bài khai `depth: full`), mẫu bài mới mặc định `depth: full`, và
  `audit/review/pedagogy_scan.py` để đo cả kho. Bài mẫu LLM L05 tăng từ 4,4 lên 9,7 phút.
- **Chữ đè nhau trong hình chưa từng được kiểm.** CLD L15 (nhãn dòng thời gian), CS115 L24 (“x + y = 10” đè “9”) và NET L10 (“ACK” đè
  chú thích) có lỗi. `player.html` nay đo khung thật của từng chữ trong `<svg>`, nên `render` FAIL khi chữ đè nhau. Đã quét mọi bài có
  hình, sửa 3 lỗi thật, và siết ngưỡng sau 2 lần báo nhầm (hai dòng nhãn xếp sát nhau).
- **Từ dễ nghe nhầm sang nghĩa khác.** “cắm” bị cả hai mô hình nghe thành “cấm”, ở CLD L15 bản đầu. Đã đổi cách nói thành “thay / giao
  diện chuẩn”.

**Khung cho chuyên ngành mới.**
- Lệnh `lv.py new-course <KHOÁ>` dựng sẵn lộ trình, lớp phủ ký hiệu, lớp phủ phát âm và bộ kiểm.
- Lệnh `lv.py new … --kind case` tạo bài tình huống sự cố, `--kind journey` tạo bài hành trình. Mẫu tự điền `course` và `series`;
  mẫu bài thường mặc định `depth: full`.
- Quy trình có cổng ở `references/new-domain.md`.

## 8. Tầm nhìn và kế hoạch dài hạn

### 8.1 Sản xuất (theo thứ tự giá trị)
1. ~~Hoàn tất hàng đợi các khoá đã có đặc tả~~ — XONG 2026-10-30 (475/475). Quy trình mỗi khoá giữ nguyên cho các khoá sau: kiểm giọng, `asr_flags` → viết lại câu ⚠ NGẮN / xử lý ⚠ THIẾU → lý do HAND (đọc lại từng dòng) → `tts_speed_scan` → `audit_all` → sinh lại STATUS.
2. **Nâng độ sâu cho người mới — viết lại theo `depth: full`** (lint E39; khung bài mẫu LLM L05; đo bằng `pedagogy_scan.py`).
   Không đổi số bài, không đổi mục tiêu. Giữ các con số và `checks` đã kiểm; chỉ thêm phần dựng kiến thức: ôn nền, hình cơ chế, suy ra
   từng bước, ví dụ từng phép tính, tự kiểm bằng đường khác, lỗi của người đã đi làm, quiz quyết định giải từng bước.
   - **Đợt A** — 19 khoá nén, khoảng 270 bài, theo số nghề dùng tới: (1) AIF, LLM, SWF, SDP, DBS, SEC; (2) CLD, CLC, DVO, SAR, DSY, EVT, DEN;
     (3) DSC, DAN, MLO, AGT, WEB, BCH, PLC, ESY, ROB.
     Tiến độ 2026-10-31: **đặc tả đợt A XONG — 23 khoá, 325 bài, `pedagogy_scan` 100% ĐỦ** (lint 0/0, render 0 vấn đề, mẫu khớp bài,
     0 ký tự điều khiển). Dựng lại theo hàng đợi (`audit/review/batch*.log`, tới batch17 = ROB). Quy trình chuẩn: pedagogy.md luật 24.
     Rà lại khi tách bước đã bắt 9 lỗi nội dung cũ (SWF L07, SDP L04, DBS L07/L12, SEC L05/L08/L10, CLD L03, SDP L00) — mỗi lỗi có `checks` mới.
   - **Đợt B** — 8 khoá dày hơn (CS115, CS112, DMS, RBM, NET, TOC, OSY, CSA): chỉ bổ sung theo từng bài. Thêm hình cơ chế, thêm bước ôn
     nền (6 khoá chưa có), tách đáp án quiz thành từng bước.
     Tiến độ 2026-11-01: **đặc tả đợt B XONG — 8 khoá, 171 bài, `depth: full`** (lint 0/0, render 0 vấn đề, mẫu khớp bài; công cụ
     đồng bộ mẫu nay khớp cả mẫu tên ngắn hơn bài). Sửa nội dung cũ: NET ×4, CSA ×2, OSY L09 (căn 4 MiB → 12 hay 16 KiB),
     DMS L01 (p → q và q → p trùng 2 dòng, không phải 3), TOC L06/L09/L11, CS112 L06 (chèn đầu danh sách), CS115 L29 (62 cách gán
     nhãn = 2 × 31 cách chia). Dựng lại theo hàng đợi tới batch26 = CS115.
     Tiến độ 2026-11-02: **dựng đợt A + B XONG** — batch10–34 đều PASS, 0 FAIL; ASR 0 câu chưa xem xét ở mọi khoá trừ AIF L11
     (1 câu chờ tai người). Câu ngắn/thấp viết lại rồi dựng lại: CSA L01/L06/L14, DMS L08/L15/L18, CS112 L22/L23 (cùng các câu đợt A).
     Kiểm toàn kho: tests 0 FAIL; audit_all 476/476 đã dựng, 1 vấn đề (AIF L11 nói trên); tts_speed_scan 35 622 câu, 0 câu cụt;
     STATUS 475/575 bài, 3740 phút. Còn: bài hành trình (mục 3), các khoá GFX/HCI/IRS/PAR/RLN/SEP chưa soạn.
     Tiến độ 2026-11-03: **đợt C XONG — 29 bài hành trình** (bảng mục 3, mỗi dòng ✅ ghi nguồn đã đọc), dựng batch35–45 đều PASS, ASR 0 chưa
     xem xét. Sửa nội dung cũ khi soạn: ESY L10 hook (cơ chế Pathfinder: tác vụ cao chờ khoá do tác vụ thấp giữ), câu “bài cuối” ở bài áp chót
     (CSA L14, OSY L13, DMS L18). Khoá mới: SEP 12 bài và CAS 12 bài đã có đặc tả (dựng batch46–47); PAR, RLN đang soạn; còn IRS, CVI, HCI, GFX.
   - Mỗi khoá xong thì đi đủ các cổng §7 rồi sinh lại STATUS. Thời gian máy đo được: dựng và chạy ASR một bài 10 phút mất khoảng 7–10 phút.
3. **Bài hành trình cho mỗi khoá** (`--kind journey`). Đánh số tiếp sau bài cuối, sửa câu nối của bài cuối cũ, rồi dựng lại bài đó.
   Nguồn dưới đây đều là **ứng viên NOT_VERIFIED**: phải đọc nguyên văn và ghi câu trích vào `audit/<khoá>/sources_<id>.md` trước khi soạn,
   như CLD L15. Ưu tiên nguồn do chính đội làm ra hệ thống viết (bài báo, bài hậu kiểm, blog kỹ thuật).

   | Khoá | Hành trình | Nguồn gốc cần đọc |
   |---|---|---|
   | CLD | ✅ Borg → Omega → Kubernetes (L15, đã dựng) | EuroSys 2015; ACM Queue 2016; blog Kubernetes 2024 |
   | NET | ✅ sụp đổ tắc nghẽn 1986 → Jacobson 1988 → BBR 2017 → QUIC 2021 và BBR bản IETF (L15) | Jacobson & Karels 1988; blog Google Cloud 2017; RFC 9000/9002; draft-ietf-ccwg-bbr — audit/net/sources_L15.md (ACM Queue 2016 bị chặn 403, không dạy) |
   | DBS | ✅ thêm cột khi bảng có hàng triệu dòng: bảng bóng (pt-osc) → gh-ost 2016 → ghi kép Stripe 2017 → thêm cột tức thì 2018 → 2022 (L17) | tài liệu pt-online-schema-change; blog GitHub 2016; blog Stripe 2017; MySQL 8.0.12/8.0.29; PostgreSQL 11 — audit/dbs/sources_L17.md |
   | DSY | ✅ Bigtable 2006 → Spanner 2012 → Spanner thành hệ SQL 2017 (L15) | OSDI 2006; OSDI 2012; SIGMOD 2017 — audit/dsy/sources_L15.md |
   | DEN | ✅ MapReduce 2004 → Spark 2012 → Dataflow 2015 → Spark một bộ máy chung 2016 (L14) | OSDI 2004; NSDI 2012; PVLDB 2015; CACM 2016 — audit/den/sources_L14.md |
   | EVT | ✅ Kafka 2011 → LinkedIn 2015 → KIP-500 2019 → KRaft 2.8–3.x → 4.0 (2025) bỏ ZooKeeper (L11) | NetDB 2011; PVLDB 2015; blog LinkedIn 2015; KIP-500; bài phát hành Kafka — audit/evt/sources_L11.md |
   | SAR | ✅ Twitter 2006 → 2014: nguyên khối Ruby → dịch vụ JVM (L13) | slide “Scaling Twitter with Open Source”; QCon London 2014; “Your Server as a Function” 2013 — audit/sar/sources_L13.md (blog Twitter 2013 bị chặn 403/429, không dạy) |
   | SDP | ✅ Shopify 2006 → 2024: nguyên khối mô-đun hoá, Packwerk và bài nhìn lại (L17) | Shopify Engineering 2019, 2020, 2020, 2024 — audit/sdp/sources_L17.md |
   | SWF | ✅ Google 2010 → 2020: một kho mã chung cho hàng chục nghìn kỹ sư (L13) | Google Engineering Tools/Testing blog 2011, 2016; ICSM 2013; ICSE-SEIP 2017; Software Engineering at Google 2020 — audit/swf/sources_L13.md (CACM 2016 bị chặn 403/429, không dạy) |
   | DVO | ✅ đo năng lực phân phối 2014 → 2024 (L13; có kiểm lệch số “440 lần” năm 2017 → tính lại 449) | báo cáo State of DevOps 2014–2019, 2021, 2023; dora.dev — audit/dvo/sources_L13.md |
   | CLC | ✅ S3 2006 → 2013 → sự cố 2017 → nhất quán mạnh 2020 → 2022 (L12) | thông cáo 2006; blog AWS 2013, 2020, 2021, 2022; bài tổng kết sự cố 2017 — audit/clc/sources_L12.md |
   | SEC | ✅ Heartbleed 2014 → Let’s Encrypt 2015 → HTTPS phổ biến 2019 → vòng đời chứng chỉ 45 ngày 2025–2028 (L15) | cảnh báo OpenSSL 2014; IMC 2014; CCS 2019; blog Let’s Encrypt 2015, 2025 — audit/sec/sources_L15.md |
   | BCH | ✅ nâng cấp một chuỗi khối đang chạy: Bitcoin 2008 → SegWit 2016–17 → Hợp nhất 2022 → sau 2022 (L12) | sách trắng Bitcoin; BIP 141, 9, 91; bitcoincore.org; ethereum.org — audit/bch/sources_L12.md |
   | WEB | ✅ HTTP/1.0 1996 → 1.1 1999 → 2 2015 → 3 và bộ RFC 2022 (L15) | RFC 1945, 2616, 9112, 7540, 7541, 9113, 9114, 9110 — audit/web/sources_L15.md |
   | PLC | ✅ an toàn bộ nhớ 2019 → 2025: ~70% lỗ hổng là lỗi bộ nhớ → Android giảm dưới 20% (L13) | blog MSRC 2019; Chromium rule-of-2; blog bảo mật Google 2019–2025 — audit/plc/sources_L13.md |
   | OSY | ✅ bộ lập lịch Linux: O(1) 2002 → CFS 2007 → nhóm 2008 → EEVDF 2023 → 2024 (L15) | tài liệu nhân, Kernel Newbies, LWN — audit/osy/sources_L15.md |
   | CSA | ✅ 2 GHz 2001 → hết bữa trưa miễn phí 2005 → đa nhân → Spectre 2018 → giảm thiểu (L16) | Sutter 2005; Kocher và cộng sự 2019 (bản tác giả); docs.kernel.org — audit/csa/sources_L16.md |
   | TOC | ✅ Thompson 1968 → quay lui bùng nổ 2007 → 2010 → sự cố Cloudflare 2019 → RE2 2025 (L14) | Thompson 1968 (bản quét); Cox 2007, 2010; hậu kiểm Cloudflare 2019; README RE2 — audit/toc/sources_L14.md |
   | CS112 | ✅ Timsort 2002 → Java 2011 → lỗi tìm bằng kiểm chứng hình thức 2015 → Powersort 2021 → 2025 (L29) | listsort.txt; JDK 7; CAV 2015 (bản tác giả); CPython #23515, bpo-34561, gh-135551; JDK-8072909 — audit/cs112/sources_L29.md |
   | CS115 | ✅ Adam 2015 → lỗi hội tụ 2018 → AdamW 2019 → thư viện (L45) | arXiv 1412.6980, 1904.09237, 1711.05101; ghi chú PyTorch — audit/cs115/sources_L45.md |
   | DMS | ✅ hàm băm: MD5 → va chạm SHA-1 2017 → NIST rút SHA-1 2022 → Git chuyển hàm băm (L20) | RFC 6151; ePrint 2017/190; blog Google 2017; NIST; tài liệu Git — audit/dms/sources_L20.md |
   | RBM | ✅ lọc Kalman 1960 → Apollo 1961–1972 → công nghiệp 1973–1985 (L17) | McGee & Schmidt, NASA TM-86847 (1985) — audit/rbm/sources_L17.md |
   | AIF | ✅ chip cờ 1988 → Deep Blue 1997 → AlphaGo 2016 → AlphaGo Zero 2017 → AlphaZero 2018 (L14) | AI 2002 (bản chép cs.oswego.edu); Nature 2016, 2017; arXiv 1712.01815; bản truy cập mở Science 2018 — audit/aif/sources_L14.md |
   | LLM | ✅ Transformer 2017 → luật mở rộng 2020 → GPT-3 2020 → Chinchilla 2022 (L14) | arXiv 1706.03762, 2001.08361, 2005.14165, 2203.15556 — audit/llm/sources_L14.md |
   | MLO | ✅ nền tảng đầu 2007 → nợ kỹ thuật 2015 → TFX 2017 → mã nguồn mở và quy mô 2019–2020 (L14) | NeurIPS 2015; KDD 2017; arXiv 2010.02013 — audit/mlo/sources_L14.md |
   | DSC | ✅ Netflix Prize 2006 → 2007 → 2009 → không triển khai cả bộ ghép 2012 (L15) | KDD Cup 2007; bài các đội 2009; Statistical Science 2012; SIGKDD Explorations 2012 — audit/dsc/sources_L15.md (blog Netflix 2012 bị chặn, không dạy) |
   | DAN | ✅ thử nghiệm A/B 2007 → 2019 ở Microsoft: bài học lạ, quy mô lớn, giảm phương sai, lệch tỉ lệ chia nhóm (L12) | KDD 2007, 2012, 2013, 2019; WSDM 2013; SIGKDD Explorations 2019 — audit/dan/sources_L12.md |
   | AGT | ✅ ReAct 2022 → Toolformer 2023 → SWE-bench 2023 → SWE-agent 2024 → bộ Verified 2025 (L12) | ICLR 2023; arXiv 2023; ICLR 2024; NeurIPS 2024; swebench.com — audit/agt/sources_L12.md |
   | ROB | ✅ DARPA 2004 → Stanley 2005 → báo cáo an toàn Waymo 2020–2025 (L13) | JFR 2006; arXiv 2011.00038, 2011.00054, 2312.12675, 2505.01515 — audit/rob/sources_L13.md |
   | ESY | ✅ Pathfinder 1997 → Spirit 2004 → Opportunity 2014–2015 → khung F´ 2017– (L15) | thư Reeves 1997 (bản chép); IEEE Aerospace 2005 (bản tác giả); tin JPL; F´ — audit/esy/sources_L15.md |
   Các sự cố từng ghi là ứng viên cuối khoá (Facebook 4/10/2021, Equifax 2017 theo GAO-18-559, The DAO 2016, Therac-25 theo Leveson &
   Turner 1993, CrowdStrike 19/7/2024, Zillow Offers 2021, chèn lời nhắc gián tiếp theo Greshake 2023) được giữ làm chặng trong bài hành
   trình tương ứng hoặc làm bài của khoá CAS. Chúng vẫn NOT_VERIFIED.
4. **Các khoá mới.** Soạn đặc tả cho 8 khoá theo thứ tự: CAS và SEP, rồi PAR và RLN, rồi IRS và CVI, cuối cùng HCI và GFX.
   Bài viết theo `depth: full` ngay từ đầu.
5. **Thực hành đi kèm video.** Video dạy khái niệm và cách nghĩ, nhưng không thay được việc tự viết mã. Mỗi khoá nên có bộ bài thực hành nhỏ, tự chấm bằng chính các hàm kiểm của checklib, và một dự án cuối khoá.

### 8.2 Đo hiệu quả với người học thật (hiện NOT_VERIFIED)
- Bài kiểm trước và sau mỗi khoá, dựng từ quiz đã có.
- Đo tỉ lệ xem hết, và các bài người học dừng hoặc tua lại nhiều.
- Người nghe kiểm mẫu phát âm theo từng khoá: mỗi khoá 10 câu bị máy nghe gắn cờ nhiều nhất.
- Kết quả đo quay lại sửa đặc tả. Mọi thay đổi vẫn qua đủ các cổng ở §7.

### 8.3 Giữ giá trị lâu dài
- **Dạy nguyên lý, không dạy thao tác của một công cụ.** Tên sản phẩm chỉ hiện trên màn hình; ví dụ tính được bằng tay hoặc bằng máy.
- **Rà lại định kỳ mỗi năm** những gì có thể đổi:
  - Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15 (hiệu lực 1/1/2026) và Nghị định 356/2025/NĐ-CP;
  - tài liệu sản phẩm theo phiên bản (Kubernetes, giao thức, WCAG);
  - bản cuối của CS2023.
- **Không sửa tay STATUS.md và TRACKS.md.** Sinh lại sau mỗi đợt, để tài liệu luôn khớp hiện trạng.

### 8.4 Mở rộng sang chuyên ngành khác: hồ sơ chuyên ngành (2026-10-31)
Người dùng yêu cầu: dùng lại xưởng cho ngoại ngữ, kỹ năng mềm, kiến thức xã hội đời sống, triết học, phim ảnh, video tiếp thị liên kết.
Đường ống chung không đổi (đặc tả → khung hình → giọng → máy nghe → MP4); khác biệt nằm trong **hồ sơ** `tools/profiles/<tên>.yaml`
(phân cảnh và nhãn, phân cảnh bắt buộc, chuẩn độ sâu, chính sách bằng chứng, luật riêng). Hướng dẫn: `references/profiles.md`;
kiến trúc mã: `tools/README.md`.

| Hồ sơ | Bằng chứng thay cho `checks` số | Luật riêng | Bài mẫu (`examples/profiles/`) |
|---|---|---|---|
| `stem` (mặc định, 476 bài hiện có) | mọi con số chạy `checks` | E1–E40 | — (khung hình giữ nguyên từng byte) |
| `language` | từ điển / giáo trình chuẩn | E50: giọng bản ngữ chỉ ở step câu mẫu, không lẫn chữ Việt | **đã dựng**: verify PASS, ASR 42 câu, 0 cờ |
| `softskill` | mô hình có nguồn + mức bằng chứng | E46: không hứa kết quả | phản hồi SBI |
| `humanities` | `quotes` (tác giả, tác phẩm, năm) | E47: trích dẫn có nguồn | con thuyền Theseus (Plutarch, Hobbes) |
| `film` | dữ kiện có nguồn; nhận định ghi rõ | E48: ảnh có giấy phép; E49: báo trước tiết lộ nội dung | hiệu ứng Kuleshov + các nghiên cứu lặp lại 1992, 2016 |
| `affiliate` | `claims` có nguồn + ngày xem | E41 công bố liên kết trước; E42 từ tuyệt đối; E43 lời khen bịa; E44 khẳng định không ngày; E45 nói ai không nên mua | sạc dự phòng: mAh → Wh, giới hạn 100 Wh của IATA |

Lĩnh vực có rủi ro gây hại (y tế, tài chính, pháp lý) cần thêm luật riêng trước khi mở (mẫu: E41–E45), mỗi luật có ca thử trong
`tests/test_lint.py`. Vẫn giữ hai điều kiện mở khoá: có chuẩn hay nguồn gốc để làm căn cứ phạm vi, và khẳng định kiểm được (bằng máy,
hoặc bằng nguồn đọc nguyên văn). Ứng viên STEM tiếp theo: phương pháp số, thống kê Bayes và suy luận nhân quả, vận trù học.

## 9. NOT_VERIFIED và rủi ro
- **Hiệu quả sư phạm** với người học thật chưa đo (§8.2).
- **Phát âm** mới được kiểm bằng máy nghe (hai mô hình), chưa có người nghe. Tên riêng đạt dưới 7/8 lần thử chỉ hiện trên màn hình.
- **Số giờ lõi CS2023** lấy từ bản “Introduction to Knowledge Model” (2024), chưa đối chiếu báo cáo cuối.
- **Tên từng nguyên tắc** trong ACM Code of Ethics 2018 chưa đối chiếu nguyên văn, vì trang acm.org chặn tải. SEP phải đối chiếu trước khi dựng video.
- **Lệnh của SEC về Knight Capital** (34-70694) chỉ đọc qua bản trích có dẫn số đoạn. Đọc bản gốc trước khi dựng CAS L05.
- **Các kết quả kinh điển** (Lamport 1978, Raft 2014, Liu & Layland 1973…) ghi theo kiến thức chuẩn. Mọi **con số** liên quan đã được máy tính lại.
- **Ngưỡng kinh nghiệm** (PSI 0,2; 31% vấn đề phát hiện được mỗi người thử; điểm SUS trung bình 68) là quy ước của ngành, không phải định lý. Giáo án ghi rõ điều này.
