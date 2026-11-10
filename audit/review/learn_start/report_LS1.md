# report_LS1: hai lộ trình đã sẵn sàng để bắt đầu học (2026-11-10/11)

**Kết luận: `DONE`** cho phạm vi đã cam kết ở `plan_LS1_20261110T1420Z.md`: 119 bài của hai lộ trình người dùng chọn. Đồ thị chứng cứ: `knowledge-graph_LS1_20261110T1420Z.md` (LS-01…LS-12).

## 1. Bắt đầu học ở đâu
- Mở **`HOC_TAP.html`** ở gốc kho bằng trình duyệt; không cần mạng. Bản chữ: `HOC_TAP.md`.
- **Lộ trình phỏng vấn backend ngân hàng**: 45 bài, 6,1 giờ video. JVA L00 → L12 → BNK L00 → L14 → INT L00 → L07 → ACB L00 → L08. Người chưa từng lập trình bắt đầu ở **JVA L00**.
- **Lộ trình nền tảng khoa học máy tính**: 74 bài, 12,9 giờ video. DMS L00 → L18 → CS112 L00 → L29 → CS115 L00 → L13 → DMS L19 → L20 → CS115 L14 → L21 → CS115 L44. Đây là thứ tự máy tính theo mọi tiên quyết: DMS L19 cần CS115 L13.
- Mỗi bài có trang **`out/<KHOÁ>/<Lxx>/xem.html`** gồm:
  - video, mục lục bấm để nhảy tới đoạn cần xem, chỉnh tốc độ 0,75–1,5×;
  - mục tiêu bài lấy từ giáo án;
  - nút sang bài trước và bài sau.
- Phụ đề đã in sẵn trên hình. Dấu "đã học" lưu trong trình duyệt.

## 2. Đã làm gì
1. **Kiểm máy từng tệp** (`pack.py check --decode`): mp4 giải mã trọn, h264 1920×1080 kèm tiếng aac, độ dài khớp timeline, srt và mục lục hợp lệ, đặc tả khớp dấu băm của bản dựng.
   - Lỗ hổng tìm thấy: `preview.html` thiếu hẳn ở JVA (13/13), INT (7/8), ACB (5/9), CS112 L29. Các bản còn lại cũ hơn đặc tả, tức hiện nội dung trước khi sửa.
   - Đã sinh lại; nay `pack.py` so từng byte với bản sinh từ đặc tả hiện tại.
2. **Đọc trọn 119 bài**: 9 người đọc độc lập, chỉ đọc (brief `BRIEF_LS1.md`).
   - Họ tự tính lại mọi con số, chạy thử mã và xem khung hình thật.
   - Họ chấm theo hai mặt: chuẩn xác, và người mất gốc có theo được không (thuật ngữ chưa giảng, bước nhảy cóc, quiz dùng điều chưa dạy).
3. **Sửa**:
   - CS115 do người điều phối tự sửa; 7 khoá khác do chính người đọc sửa theo `BRIEF_FIX_LS1.md`.
   - Người điều phối kiểm diff mọi mục MUST.
   - Sửa đúng nguồn: `audit/jva/src`, `audit/bnk/src`, mẫu `.tpl`, `lp_svg.py`.
4. **Dựng lại 97 bài** bằng 3 luồng (`rebuild_ls1.sh`), một giọng NamMinh. Máy nghe báo 0 câu chưa xem xét; có 6 lý do viết tay, đều trích nguyên bản chép.
5. **Đồng bộ**:
   - video phỏng vấn (92/92 trùng byte), bảng mục lục phỏng vấn;
   - tài liệu `interview/04`, `06`, `MASTER_CURRICULUM_INDEX`, `HANDOVER_INTERVIEW` (nhóm nợ);
   - trang học.

### Phát hiện và xử lý (chi tiết: `findings_LS1.md`)
| Khoá | Bài đọc | MUST | Mục đã sửa | Bài dựng lại |
|---|---:|---:|---:|---:|
| JVA | 13 | 3 | 24 | 10 |
| BNK | 15 | 2 | 28 (1 giữ, xem §4) | 14 |
| INT | 8 | 6 | 36 | 8 |
| ACB | 9 | 4 | 31 | 9 |
| DMS | 21 | 0 | 37 | 18 |
| CS112 | 30 | 1 | 47 | 22 |
| CS115 | 23 | 1 | 27 | 16 |
| **Tổng** | **119** | **17** | | **97** |

MUST tiêu biểu (lỗi người học sẽ học sai):
- **CS112 L07**: ghi chú tổng kết nói A, C, D, E, F, B "không phải thứ tự đi sâu". Sai: đó là một thứ tự đi sâu hợp lệ (vét cạn mọi thứ tự xét láng giềng).
- **INT L03, L04**: tự bồi hoàn hoặc mở phong toả khi đối tác chỉ "lỗi mạng". Trái nguyên lý chính của khoá: hết giờ chờ là chưa biết kết quả, phải hỏi lại trước.
- **Nhóm nợ 2** (INT L04, ACB L08, tài liệu phỏng vấn): ghi "10–89 ngày", lệch một ngày. Đúng là 10–90 ngày (LS-04).
- **BNK L00**: nhãn hình "xám: không ai trỏ tới → rác" mâu thuẫn với chính hình vẽ. **BNK L04**: phép chứng minh "bọc hàm làm mất chỉ mục" dùng sai ví dụ (sqlite cho SCAN cả khi không bọc hàm).
- **JVA L03**: đoạn mã trên màn hình thiếu lệnh in mà vẫn hiện kết quả; phần mở đầu nói "sai một ký tự" trong khi chương trình sai hai chỗ. **JVA L04**: giáo án hứa điều bài không dạy.
- **ACB L00**: mục tiêu P99 100 ms mâu thuẫn với ví dụ 155 ms. **L06**: tiêu đề hứa "Ngân hàng Mở" nhưng không dạy. **L08**: mục tiêu hứa giải ngân luỹ đẳng nhưng không dạy.
- **CS115 L03**: giáo án hứa tính chất tuyến tính nhưng bài không nêu.

Các mục BLOCK (người mất gốc kẹt) đã sửa, ví dụ:
- quy tắc đạo hàm xⁿ (L07, L08 dùng mà L06 không dạy);
- quy tắc diện tích dưới xᵏ (L14, L17);
- "tuyến tính", SGD, cross-entropy, trung bình điều hoà, phân phối t;
- số nguyên tố, căn, hệ số, biến cố, bảng băm (DMS);
- cú pháp `for`/hàm/`int` (CS112 L00, L04);
- Survivor, TLS, TCP, máy trạng thái (INT);
- mã Go, Kafka Streams (ACB).

## 3. Cổng cuối (OBSERVED, log ở `logs/`)
| Cổng | Kết quả |
|---|---|
| `pack.py check --decode` (119 bài) | 0 vấn đề; giải mã trọn 119; 1136,7 phút |
| Dựng lại | 97/97 PASS; máy nghe chưa xem xét 0 |
| `audit_all.py` toàn kho | 656 bài, 656 đã dựng, **0 bài có vấn đề** (gồm lint, dấu băm, giọng, ASR, cổng mã màn hình từng khoá) |
| verify_jva / verify_bnk | 110/110 · 21/21 |
| verify_cs112 / verify_cs112_p2 / verify_plan_curricula | FAIL 0 · 37/0 · 545/0 |
| check_xref / check_meta / check_course_refs / scan_ctrl | 0 / 0 / 0 / 8 (JVA cố ý) |
| Mẫu `.tpl` (CS112, DMS, CS115) | 0 lệch |
| Video phỏng vấn | 92/92 trùng byte; 365,61 phút |
| Trang học | 0 liên kết chết (357 + 710 + 120) |

## 4. Còn mở (không chặn việc bắt đầu học; ghi rõ, không gọi là đã kiểm)
- **BNK L13, QĐ 2345/QĐ-NHNN**: chưa kiểm được điều kiện "khách hàng cá nhân", cũng chưa kiểm được việc nội dung này nay nằm ở TT 50/2024/TT-NHNN. Bài giữ câu cũ; nên đối chiếu văn bản gốc.
- **TT 31/2024**: mới kiểm qua hai nguồn thứ cấp; nguyên văn Điều 10 chưa đọc được (thuvienphapluat trả 403).
- **Phát âm**: chỉ máy nghe kiểm; chưa có tai người nghe lại.
- **Hiệu quả với người học thật**: chưa đo.
- **537 bài ngoài hai lộ trình**: không được đọc lại trong đợt này. Theo mẫu E, khoảng 5% bài có MUST.
- **Hệ thống ngoài** (Redis, Oracle, Kafka, T24, NAPAS) và **mã C**: không chạy được trên máy (CB-2, CB-5 của SC1).
