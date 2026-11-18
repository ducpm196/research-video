# S01 BNK (L00..L14): đã đọc 15/15 bài — 2026-11-14

Cách làm: bốn người đọc độc lập (A: L00–03, B: L04–07, C: L08–11, D: L12–14) đọc TRỌN YAML, mục `curriculum/bnk.yaml`, `.srt`, ≥ 5 khung hình/bài (8–11 khung ở hầu hết bài), tự làm lab trước khi mở `loi_giai.*`, chạy lại số và mã (JDK 21.0.13, Python 3.13, sqlite qua module Python). Máy KHÔNG có `sqlite3` CLI và KHÔNG có `audit/bnk/deps`, nên Spring/HikariCP/Kafka/Redis/Oracle thật không chạy được ("chỉ đọc"). Người điều phối ghép bốn phần (Phụ lục A–D, đủ 9 mục mỗi phần) và TỰ KIỂM LẠI các phát hiện MUST bằng Python/grep/Java (ghi "đã kiểm lại"). Không mở báo cáo/plan/handover nào của kho. mp4 và khung hình của cả 15 bài có đủ; srt khớp `say` 100% theo người đọc (sha16 trong bảng là lúc đọc).

## Kết luận theo ngưỡng chốt
| Ngưỡng | Kết quả | Đạt? |
|---|---|---|
| MUST = 0 | 6 (4 CONFIRMED + 2 ở mức biên) | KHÔNG |
| P1 = 2 ≥ 90% số bài | 1/15 (chỉ L01); L12 = 0, L13 = 0, 12 bài còn lại = 1 | KHÔNG (6,7%) |
| P8 = 2 = 100% | 15/15 | ĐẠT |
| P9 = 2 | 15/15 | không có ngưỡng |
| Lời đọc ≤ 16 phút | mp4 13:40–16:21 gồm dừng quiz/tự làm 175–205 s; lời đọc thuần 11–13 phút. L11 = 16:01, L13 = 16:21 vượt 16:00 khi tính cả dừng | đạt về lời đọc |
| Mất gốc | ĐỦ: L06, L07, L08, L09, L11 (L06/L08/L11 sát ngưỡng 12); GẦN: 10 bài; CHƯA: 0 | — |

## MUST (6)
| # | Bài | Tệp + bước | Trích | Bằng chứng đã chạy | Tin cậy |
|---|---|---|---|---|---|
| 1 | L06 | lessons/bnk/L06_redis_cache_khoa_phan_tan.yaml, `quy_mo` step 2 (hộp "Giải pháp cũ gãy ở đâu", dòng ~610) | "muốn xuống mười thì phải trúng 99,9%" | tải ×10 000 = 10^6 yêu cầu/s × 20 ms: trúng 99% → 200; trúng 99,9% → 10^6×0,001×0,02 = **20,0**; muốn 10 cần 99,95% (10,0). Đã kiểm lại bằng Python | CONFIRMED |
| 2 | L09 | L09_so_cai_but_toan_kep.yaml, `quy_mo` step 1: lời đọc (`say` dòng ~481, có trong `L09.srt`) khác màn hình (dòng 467) | lời: "mất khoảng bốn ngày rưỡi"; hình: "≈ 4,2 ngày" | 365 000 000 000 / 10^6 / 86 400 = **4,2245 ngày**. Đã kiểm lại bằng Python và grep srt | CONFIRMED |
| 3 | L13 | L13_bao_mat_thanh_toan_pin_hsm.yaml, `chay_that` step 2 (`say` dòng ~408) và `formula` bước 1 | "Bên nào có khoá và số thẻ thì XOR lại để lấy PIN. Người không có thì chỉ thấy dãy này." | `041225EEEEEEEEEE` là khối PIN RÕ (chưa mã hoá TPK). XOR lại với trường PAN `0000111111111111` ra `041234FFFFFFFFFF` ⇒ PIN 1234 chỉ cần SỐ THẺ, không cần khoá; bước mã hoá không hề tính/hiện. Người học hiểu nhầm dãy này là thứ che được PIN. Đã kiểm lại bằng Python | CONFIRMED |
| 4 | L05 | L05_plsql_khoa_hang_deadlock.yaml: `check` step 1 (dòng ~437) vs `chay_that` step 1 (dòng 342, 359) vs `curriculum/bnk.yaml` L05 `example` (dòng 98) | check: "cú pháp riêng của Oracle thì máy này không chạy được"; chay_that: "PL/SQL chạy thật trên Oracle 26ai Free (Docker)"; giáo án: "mô phỏng; Oracle không chạy trên máy" | ba nơi nói ba điều khác nhau về cùng khối PL/SQL (ví dụ tự mâu thuẫn); đã kiểm bằng grep. PL/SQL có chạy thật hay không: PLAUSIBLE (không được chạy docker) | CONFIRMED (mâu thuẫn) / PLAUSIBLE (chạy thật) |
| 5 | L08 | L08_saga_transactional_outbox.yaml `chay_that` step 3, `practice` step 3; labs/BNK/L08/de.md bước 2 | "INSERT … rồi COMMIT; (để kết thúc giao dịch ngầm của câu INSERT)" | đúng với driver Python (`labs/sqlrun.py`), nhưng engine sqlite ở chế độ tự chốt (như `sqlite3` CLI mà de.md cho phép dùng) báo "cannot commit - no transaction is active" (người đọc C đã chạy sqlite 3.49.1; tôi không chạy lại; hành vi `cham.sh` với CLI là PLAUSIBLE vì máy không có CLI). Hạ SHOULD nếu `sqlrun.py` là đường chạy duy nhất | MUST-biên; engine CONFIRMED, CLI PLAUSIBLE |
| 6 | L14 | L14_tinh_huong_tru_tien_hai_lan.yaml `check` step 1–2 | "4 dòng cũ (r7, r7b) + 2 dòng đảo = 6" | cảnh `chay_that` ngay trước dùng SQL một dòng/mã (đếm 2 rồi 3); `check` đột ngột chuyển sang sổ bút toán kép 6 dòng, không hiện sổ lên màn hình, không giảng "cân đối". Hạ SHOULD nếu coi là hai mô hình sổ | MUST-biên; chuyển mô hình CONFIRMED |

Ngoài danh sách (SHOULD mạnh, sát MUST): **L01 `chay_that` step 1–2**, màn hình "dung 2000000? false" là kết quả ngẫu nhiên. Tôi chạy MatCapNhat.java (đúng mã trên màn hình) 30 lần JDK 21.0.13: **9/30 lần in `true`** (người đọc A: 6/15). Người học chạy ra `true` sẽ nghĩ bài sai; nên chỉ nói "thường thiếu, đôi khi may mắn đủ" hoặc in số tổng. CONFIRMED.

## SHOULD (tóm tắt; tệp + bước + bằng chứng đầy đủ ở Phụ lục)
- L00: `chay_that` RoRi.java "sau khi xoa, heap >= 5 MB? false" chỉ đúng với G1/Parallel (Serial/ZGC/1 CPU ra true, người đọc A đã chạy); "1 MB = 1 048 576" ở `prereq` vs mã chia 1_000_000. L01: "ba việc" vs "hai việc" (với 3 việc/luồng có 20 cách, không phải 6); sáu dãy xen kẽ chỉ đếm, không liệt kê (mục tiêu 1). L02: "Spring thật dùng đúng cơ chế này" (Spring Boot mặc định CGLIB, không phải java.lang.reflect.Proxy); bảng T=5/500/50 000 không ghi "số minh hoạ". L03: "mỗi khoá in một dòng" vs mong đợi 4 dòng; MayChu.java chỉ hiện từng phần, không có trong labs.
- L04: hình cây 3 tầng vs lời 4 tầng; "5 lần đọc thay vì 10 000 000" so hai đơn vị khác nhau. L05: SVG đồ thị chờ mũi tên ngược/không khép vòng; PL/SQL thiếu CREATE TABLE/dữ liệu/SELECT cuối nên không tái hiện 1 500 000/700 000/800 000; xác suất mỗi cặp giữ nguyên khi T×10^4 không nêu điều kiện; "ORDER BY … FOR UPDATE" không nguồn (PLAUSIBLE). L06: "hộp"=hồ kết nối chưa giảng, ⑦⑧ trước ④⑤⑥. L07: "TK-1001 vào phân vùng 1" là crc32, murmur2 của Kafka thật cho phân vùng 2 (người đọc B tự cài murmur2 khớp 4 vector chuẩn), màn hình không ghi chú; "lũy đẳng" dùng 10 lần chưa giảng; mã L05–L07 thiếu import/class/`}`.
- L08: `hook` step 2 nhãn "kết quả mô phỏng ở cuối bài" nhưng 2/4 dòng không chạy ở đâu. L09: "(như bài trước)" trỏ nhầm L08 (khoá hàng ở L05); "cộng trừ trực tiếp … ghi đè nhau" thiếu điều kiện. L10: "Hỏi trạng thái trước thì mọi trường hợp đều đúng một lần" tuyệt đối, mâu thuẫn bước 3; không có bản tin OFS nào dù tiêu đề "T24: OFS". L11: quy tắc che số thẻ (PCI DSS) không nêu nguồn; quiz đáp án 1 hiện "0𝑥30" chữ nghiêng, không nhất quán "0x70".
- L12: "gãy trên một máy" cho 100 GB tuyệt đối. L13: sinh trắc học thiếu yếu tố thứ hai loại C/D và phạm vi; `source`/registry ghi tên TT 50/2024 là "an toàn hệ thống thanh toán" (tên thật: an toàn, bảo mật cho việc cung cấp dịch vụ trực tuyến trong ngành Ngân hàng) và PCI "3.3.1.2" có thể lệch (3.3.1.3) (metadata). L14: r7 = -500 000 vs +500 000 trái định nghĩa "khớp" của L12; `NOT IN` + NULL không cảnh báo (người đọc D chạy sqlite 3.49.1: có NULL thì trả rỗng, `NOT EXISTS` đúng); "từ chối r7b là trùng" dù mã mới.

## Pháp lý / sản phẩm (đối chiếu `audit/legal/registry.yaml`)
- TT 50/2024/TT-NHNN sửa đổi bởi TT 77/2025/TT-NHNN: registry khớp lời bài (50/2024 SUA_DOI, 77/2025 hiệu lực 01/3/2026, bản hợp nhất 25/VBHN-NHNN đã đọc bản gốc; 77/2025 basis SECONDARY, chưa mở Công báo). Ngưỡng cá nhân "trên 10 triệu/giao dịch, tổng ngày trên 20 triệu": khớp nguồn thứ cấp, PLAUSIBLE.
- Ngày: TT 50/2024 hiệu lực 01/01/2025; TT 77/2025 hiệu lực 01/03/2026 nhưng Điều 10 (thay Phụ lục) áp dụng 01/07/2026 cho cá nhân: PLAUSIBLE (nguồn thứ cấp), bài nên nói rõ mốc.
- TT 31/2024/TT-NHNN (phân loại nợ) và TT 64/2024/TT-NHNN (Open API): KHÔNG xuất hiện trong L12–L14 (không có mục tiêu pháp lý nào dùng chúng); registry có mục, trạng thái HIEU_LUC, ORIGINAL.
- Sản phẩm: Java 21 luồng ảo, Spring proxy/@Transactional, Redis, Kafka (partition/offset), ISO 8583 (bitmap, DE), PIN block ISO-0, Luhn, MAC: đối chiếu bằng kiến thức chuẩn và mã chạy lại; chỗ lệch ghi ở MUST/SHOULD trên.

## Bảng độ sâu gộp (đủ cột "Cần biết trước", "Chỗ thiếu chính" ở Phụ lục)
| Bài | sha16 | Phút mp4 | P1 | P2 | P3 | P4 | P5 | P6 | P7 | Tổng | P8 | P9 | Mất gốc |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| L00 | 70768ec2957e6594 | 14:52 | 1 | 1 | 1 | 2 | 2 | 2 | 1 | 10 | 2 | 2 | GẦN |
| L01 | b8624f515c6f6d0a | 14:25 | 2 | 1 | 1 | 2 | 2 | 2 | 1 | 11 | 2 | 2 | GẦN |
| L02 | 8f2400acf8b826d9 | 14:12 | 1 | 1 | 2 | 2 | 2 | 2 | 1 | 11 | 2 | 2 | GẦN |
| L03 | e317ae8f221b6d2d | 14:13 | 1 | 2 | 1 | 2 | 2 | 2 | 1 | 11 | 2 | 2 | GẦN |
| L04 | 6a8aabf4ed0668ce | 13:40 | 1 | 1 | 1 | 2 | 2 | 2 | 1 | 10 | 2 | 2 | GẦN |
| L05 | 8ebacd73f6b5afcc | 14:36 | 1 | 1 | 1 | 2 | 2 | 2 | 1 | 10 | 2 | 2 | GẦN |
| L06 | edcd65d9d32a6b86 | 14:53 | 1 | 2 | 1 | 2 | 2 | 2 | 2 | 12 | 2 | 2 | ĐỦ (còn MUST #1) |
| L07 | 16d0b3507ced62bd | 14:42 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | 2 | 2 | ĐỦ |
| L08 | 51f9038cf6675d94 | 13:57 | 1 | 2 | 1 | 2 | 2 | 2 | 2 | 12 | 2 | 2 | ĐỦ (sát ngưỡng) |
| L09 | 300d554ba2d0a67f | 14:02 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | 2 | 2 | ĐỦ (còn MUST #2) |
| L10 | b04095b92d4c796b | 14:35 | 1 | 1 | 1 | 2 | 2 | 1 | 1 | 9 | 2 | 2 | GẦN |
| L11 | 503cdaf2d5dbe32a | 16:01 | 1 | 2 | 2 | 2 | 2 | 2 | 1 | 12 | 2 | 2 | ĐỦ (sát ngưỡng) |
| L12 | 02c72c0d89ca5104 | 14:34 | 0 | 2 | 2 | 2 | 2 | 1 | 1 | 10 | 2 | 2 | GẦN |
| L13 | 5c594e84d7cccf08 | 16:21 | 0 | 1 | 2 | 2 | 1 | 1 | 2 | 9 | 2 | 2 | GẦN (còn MUST #3) |
| L14 | f1838cdc47d56c33 | 15:30 | 1 | 1 | 2 | 2 | 2 | 1 | 2 | 11 | 2 | 2 | GẦN |

## Lab
15/15 tự làm được (L03 chỉ "phần": lab không đo máy chủ + curl) và `cham.sh` ra ĐÚNG cả ở lời giải tự viết lẫn `loi_giai.*`; `mong_doi.txt` khớp màn hình cả 15. Nhỏ: L10 `cham.sh` đòi `public class` mà de.md không nhắc; L08 video không nói cách chạy tệp .sql; lab L04 không bắt EXPLAIN, lab L05 không tái tạo bế tắc.

## "Chạy thật" có thật không, số tính lại, khung hình
- Chạy lại được và khớp: Java thuần (L00, L01, L02 mô phỏng proxy, L03 MayChu+curl, L04–L07 mô phỏng), sqlite (L04, L08 outbox, L09, L14), Python (L11, L12, L13). Số tính lại ≈ 285; sai 2 (L06, L09 lời đọc), còn lại khớp.
- Không chạy được trong kho này: Oracle (L05), Spring/HikariCP, Kafka/Redis/IBM MQ/T24/HSM/NAPAS. Các bài ghi rõ là mô phỏng/minh hoạ; ngoại lệ mâu thuẫn L05 (MUST #4) và nhãn `hook` L08. Không chỗ nào khiến người học tưởng đã chạy Kafka/Oracle/MQ/T24 thật, trừ L05 `chay_that` "chạy thật trên Oracle".
- Khung hình: lỗi nhẹ, nhãn bị mũi tên/nét gạch cắt ngang (L00 00023, L01 00027, L03 00033, L05 00027, L06 00034/00042, L08 00023, L10 00027); L11 quiz 00109 chữ "0𝑥30". Không chữ tràn nặng; L12–L14 nửa dưới khung hơi trống.

## Nhận xét chung
- Chính xác khá cao; lỗi MUST tập trung ở câu "quy mô" viết thêm (L06, L09) và ở câu giảng an ninh (L13).
- P1 là điểm yếu hệ thống: "đối soát", "lũy đẳng", "cô lập", "kỳ vọng", "lõi", "hạch toán", "sinh trắc học", "khoá phiên", "thu gom rác" dùng chưa giảng tại chỗ. Ngưỡng P1 trượt nặng (1/15).
- P8, P9 đồng đều 15/15 nhờ lab có `mong_doi.txt` và bảng ×1/×100/×10 000.
- Nhiều đoạn mã trên màn hình thiếu import/khung lớp, chép ra không biên dịch; lab thay cho phần đó.
- Mô phỏng ghi rõ, trừ mâu thuẫn L05 và nhãn `hook` L08; mốc ngày pháp lý L13 nên tách "hiệu lực" và "áp dụng".

---
# PHỤ LỤC (kết quả nguyên văn của bốn người đọc; tiêu đề hạ một cấp)

## Phụ lục A
#### Phần A — BNK L00, L01, L02, L03: đã đọc 4/4 bài (YAML trọn, srt, 8–10 khung hình mỗi bài, lab tự làm + chạy lại mã)

JDK dùng để chạy: openjdk 21.0.13 (Windows, 12 CPU). YAML sha16 lúc đọc: L00 `70768ec2957e6594`, L01 `b8624f515c6f6d0a`, L02 `8f2400acf8b826d9`, L03 `e317ae8f221b6d2d`.
Số MUST = 0. Số SHOULD = 9 (L00: 2, L01: 3, L02: 2, L03: 2). Một SHOULD sát ranh giới MUST (L01-a: kết quả "false" của MatCapNhat không ổn định).

### 1. Chuẩn xác

| Bài | Mức | Cảnh/step | Trích nguyên chữ | Vì sao sai + bằng chứng đã chạy | Đề xuất sửa | Tin cậy |
|---|---|---|---|---|---|---|
| L00-a | SHOULD | `chay_that` step 3–4 (tệp RoRi.java), lời đọc step 4 | Màn hình: "giu 5 doi tuong, heap >= 5 MB? true / sau khi xoa, heap >= 5 MB? false". Lời: "Xoá bản đồ rồi, năm mảng thành rác và bị dọn, nên heap không còn tới năm mê ga byte." | Dòng 2 phụ thuộc bộ GC/số CPU nhưng trình bày như tuyệt đối (chỉ GiuThamChieu ở step 2 có câu "ở cách chạy mặc định ... trên máy này"). Chạy mã đúng như `audit/bnk/src/l00.py`: G1 mặc định, ParallelGC, `-Xmx32m` cho `true/false` (khớp màn hình); nhưng `-XX:+UseSerialGC`, `-XX:+UseSerialGC -Xmx1g`, `-XX:+UseZGC` và `-XX:ActiveProcessorCount=1` (JVM tự chọn SerialGC) đều cho `true/true`. Bản in giá trị (RoRi2): Serial baseline 6 215 656 B > 5 000 000 nên ngưỡng "≥ 5" không thể ra false; sau `clear()` Serial vẫn 5 622 552 B ở lần `System.gc()` đầu. Máy 1 CPU / VM nhỏ / container 1 vCPU là chuyện thường của người học. | Thêm câu "đúng với G1, mặc định trên máy nhiều lõi; máy 1 lõi có thể khác"; hoặc đổi phép đo sang hiệu "sau trừ trước" thay vì ngưỡng tuyệt đối 5. | CONFIRMED |
| L00-b | SHOULD | `prereq` step 4 so với `chay_that` step 3 | Step 4 prereq: "1 MB = 1024 · 1024 = 1 048 576 byte". Mã RoRi: `return (rt.totalMemory() - rt.freeMemory()) / 1_000_000;   // heap đang dùng, đơn vị MB` | Cùng bài dùng hai nghĩa "MB" (2^20 và 10^6) mà không báo. 5 mảng × 1 000 000 B = 5 000 000 B = 4,77 MiB. Nguồn của YAML ghi IEC 80000-13 (KiB = 1024) nhưng bài vẫn viết "KB/MB". | Ghi chú `// MB ở đây = 10^6 byte` hoặc chia `1024*1024`; hoặc dùng KiB/MiB cả bài. | CONFIRMED |
| L01-a | SHOULD (sát ranh giới MUST) | `chay_that` step 1–2 (MatCapNhat.java) | Màn hình: "Kết quả chạy thật: dung 2000000? false". Lời: "Chạy thật in ra không đúng. ... Con số mất cụ thể thay đổi từng lần chạy, nên ta chỉ in đúng hay sai." | Không ổn định, bài trình bày như xác định. Chạy 15 lần mã y như màn hình: 9 `false`, 6 `true`. Bản in giá trị (Mat2) 20 lần: 4 lần dem = 2 000 000, còn lại 1 293 002 đến 1 993 622; `-XX:ActiveProcessorCount=1`: 2/6 lần ra 2 000 000. Người học gõ lại có 20–40% thấy `true`, đảo ngược điều vừa nói. Nếu cổng coi "mã cho kết quả khác điều bài nói" là MUST thì nâng mức. | In giá trị `dem`, tăng vòng lặp lên 10 triệu, hoặc nói "thường ra false, đôi khi true; chạy vài lần". | CONFIRMED |
| L01-b | SHOULD | `formula` step 3 + mục tiêu 1 giáo án | "Bước 3. Chạy thử cả sáu cách: hai cách cho 180, hai cách cho 130, hai cách cho 150." Mục tiêu: "Liệt kê mọi cách xen kẽ của hai luồng" | Số đúng: vét cạn 6 dãy → {180: 2, 130: 2, 150: 2} (Python, khớp). Nhưng sáu dãy không được liệt kê trên màn hình, chỉ đếm (4·3/(2·1)) và nêu tally; người học không tự kiểm được. Mục tiêu viết "liệt kê", video chỉ "đếm". | Thêm bảng 6 hàng (RA WA RB WB → 180; RA RB WA WB → 130; ...). | CONFIRMED |
| L01-c | SHOULD (nhẹ) | `pitfalls` Lỗi 1 so với `formula` Bước 1 | Lỗi 1: "Thực ra nó là đọc, cộng, ghi: ba việc". Bước 1: "mỗi luồng gồm hai việc nhỏ, đọc rồi ghi". | Hai mô hình (2 hay 3 việc) trong cùng bài; 6 cách chỉ đúng với 2 việc/luồng; với 3 việc/luồng là 6!/(3!3!) = 20. Không sai kiến thức nhưng dễ gây hỏi "6 hay 20 cách?". | Ở Lỗi 1 ghi "đọc, (cộng), ghi: ta gộp cộng vào bước ghi". | CONFIRMED (tính lại) |
| L02-a | SHOULD | `chay_that` step 1, lời đọc | "Ta mô phỏng cơ chế proxy bằng thư viện chuẩn của Java, vì Spring thật dùng đúng cơ chế này." | Spring Boot (tiêu đề bài) mặc định proxy theo lớp bằng CGLIB (`spring.aop.proxy-target-class=true` từ Boot 2.0), không phải `java.lang.reflect.Proxy` theo giao diện. Ý chính (gọi từ ngoài qua proxy, `this.ghiVet()` không qua proxy) vẫn đúng cho cả hai; chỉ câu "đúng cơ chế này" quá tay. `source` YAML ghi đúng "JDK dynamic proxy hoặc CGLIB" nhưng lời đọc/màn hình không nói. Spring thật không chạy (không có thư viện). | "Spring thật dùng cùng ý tưởng: JDK proxy hoặc lớp con CGLIB". | CONFIRMED (kiến thức vững, chưa chạy) |
| L02-b | SHOULD (nhẹ) | `quy_mo` step 1 | Bảng "×1: T = 5; ×100: 500; ×10 000: 50 000 ... thiếu, và vượt giới hạn của cơ sở dữ liệu" | Ba bài kia đều gắn "(số minh hoạ)", bảng này không; "vượt giới hạn của cơ sở dữ liệu" không nguồn. T·(C−1)+1 = 6, 501, 50 001 đã chạy lại: đúng; công thức khớp HikariCP wiki "About Pool Sizing"; mặc định pool 10 và connectionTimeout 30 000 ms khớp README HikariCP. | Thêm "(số minh hoạ)"; nêu mốc cụ thể (ví dụ PostgreSQL max_connections mặc định 100) hoặc đổi "thường vượt". | CONFIRMED (công thức, mặc định) / PLAUSIBLE (mốc giới hạn CSDL) |
| L03-a | SHOULD | `practice` step 1 + lời đọc, so với step 2 và `de.md` | Màn hình: "mỗi khoá in một dòng `k1 -> 2300000`". Lời: "Mỗi khoá in một dòng, gồm khoá, mũi tên, và phản hồi." Step 2 mong đợi 4 dòng (k1, k1, k2, k1). | "Mỗi khoá" gợi 2 dòng nhưng đáp án 4 dòng, k1 lặp 3 lần; `de.md` viết "Với từng khoá trong dãy" (cũng mơ hồ). Người học in 2 dòng sẽ nhận `cham.sh` KHÁC. Đã chạy: bản in 4 dòng thì ĐÚNG. | Đổi thành "mỗi yêu cầu in một dòng". | CONFIRMED |
| L03-b | SHOULD (nhẹ) | `chay_that` step 1–3 | "Cửa sổ lệnh thứ hai (máy chủ chạy ở cửa sổ thứ nhất bằng java MayChu.java)" | Mã chỉ hiện "(phần 1)", "Phần 2", thiếu `import com.sun.net.httpserver.*`, `IOException`, `InetSocketAddress`, `java.util.*`, lớp `MayChu`, `main ... throws Exception`; `labs/BNK/L03/` chỉ có de.md, loi_giai.java, mong_doi.txt, không có MayChu.java. Người học không tái hiện được máy chủ để chạy `curl`; mục tiêu 5 giáo án chỉ được xem, không được làm. Tôi ghép tệp đầy đủ từ `audit/bnk/src/l03.py` và chạy thật (java MayChu.java + 6 lệnh curl): đúng 6 dòng như màn hình. | Đưa MayChu.java đầy đủ vào `labs/BNK/L03/` hoặc hiện đủ import + khung lớp. | CONFIRMED |

Đã kiểm và không có bằng chứng sai: JEP 444/491 (ghim ở Java 21, bỏ ở Java 24, native vẫn ghim); rollback mặc định RuntimeException + Error; RFC 9110 bảng an toàn/lũy đẳng (GET, PUT, DELETE, POST); G1 mặc định từ JDK 9; BigDecimal(double) mang sai lệch (Decimal(0.1) = 0.1000000000000000055511151231257827...); sqlite `INSERT OR IGNORE` + PRIMARY KEY cho COUNT = 1 và dòng đầu.

### 2. Độ sâu

P1–P7 chấm nghiêm theo BRIEF. "Phút (lời đọc/thật)": lời đọc = thời lượng mp4 trừ tổng `pause` trong YAML; thật = `ffprobe` mp4.

| Bài | sha16 | Phút (lời đọc/thật) | P1 | P2 | P3 | P4 | P5 | P6 | P7 | Tổng | P8 | P9 | Mất gốc | Cần biết trước | Chỗ thiếu chính |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| L00 | 70768ec2957e6594 | ≈13,0 / 14,87 | 1 | 1 | 1 | 2 | 2 | 2 | 1 | 10 | 2 | 2 | GẦN | máy ảo Java (JVM), kiểu `int/long/double`, `final`, generic `<Integer, byte[]>`, `javac/java`, GB, "đối soát" | P1: "đối soát cuối ngày" (pitfalls Lỗi 3) và "máy ảo Java" (`chay_that` step 2) không giảng; "heap" xuất hiện ở `sym` (01:52, "trên vùng nhớ heap") trước khi `intuition` giảng (02:18). P2: "số thực nhị phân không biểu diễn đúng 0,1" (`check` step 2) nói mà không cho thấy vì sao (0,1 nhị phân lặp vô hạn). P3: khung 00023, nhãn "tham chiếu" bị mũi tên cắt ngang. P7: mục tiêu 1 (stack vs heap) không câu quiz/lab nào đo. |
| L01 | b8624f515c6f6d0a | ≈12,0 / 14,41 | 2 | 1 | 1 | 2 | 2 | 2 | 1 | 11 | 2 | 2 | GẦN | hệ điều hành, lõi CPU, TB/GB, `static`, `ExecutorService` + try-with-resources, `AtomicInteger`, `Thread.sleep`, lambda trả giá trị | P2: `formula` step 3 khẳng định kết quả sáu cách mà không liệt kê sáu dãy (L01-b). P3: khung 00027, chỉ có mũi tên A đọc→A ghi, thiếu mũi tên B, không trục thời gian; mũi tên xuất phát dưới đáy hộp "A đọc". P7: mục tiêu 1 "Liệt kê" chỉ được đếm. P1: "lõi bộ xử lý", "TB" dùng không giảng (nhẹ, không trừ). |
| L02 | 8f2400acf8b826d9 | ≈11,8 / 14,20 | 1 | 1 | 2 | 2 | 2 | 2 | 1 | 11 | 2 | 2 | GẦN | lambda `(p, m, a) ->` và `m.invoke`, `interface ... implements`, bảng/SQL, "ghi vết" = audit log | P1: "hộp kết nối" (connection pool) dùng ở `quy_mo` mà không định nghĩa (chỉ định nghĩa "kết nối"); "HikariCP" chỉ hiện trên màn hình; "đường nóng" (`quy_mo` step 2) không giảng. P2: công thức T·(C−1)+1 nêu, không suy ra "vì sao +1". P7: mục tiêu 1 "Nêu cách Spring tạo bean" chỉ nói ở `sym`/`intuition`, không câu đo; Spring thật không chạy. |
| L03 | e317ae8f221b6d2d | ≈11,8 / 14,22 | 1 | 2 | 1 | 2 | 2 | 2 | 1 | 11 | 2 | 2 | GẦN | giao thức, lambda `ex ->`, `HttpExchange`, `a -= 500_000` có tác dụng phụ trong biểu thức, SQL cơ bản, "đối soát" | P1: "đối soát" (`quy_mo` step 2) không giảng ở bất kỳ bài L00–L03. P3: khung 00033, nhãn "ghi" bị mũi tên cắt ngang. P7: mục tiêu 5 (chạy máy chủ nhỏ + curl) chỉ xem, không có MayChu.java đầy đủ (L03-b); `practice` đo mục tiêu 7 không phải 5. |

P8 = 2 cả 4 bài (có đề, đầu vào, kết quả mong đợi, lệnh chấm; số khác ví dụ). Chỗ yếu P8: phần máy chủ + curl ở L03 chỉ xem; các tệp GiuThamChieu, RoRi, MatCapNhat, LuongAo không có trong `labs/`.
P9 = 2 cả 4 bài: L00 4,9 ngày / 70 phút / 42 giây; L01 5 s / 8,3 phút / 13,9 giờ và 10 GB/1 TB/100 TB vs 10 MB/1 GB/100 GB; L02 6/501/50 001 kết nối; L03 5×10^7 / 5×10^9 / 5×10^11 đồng, 6,4 MB / 640 MB / 64 GB; cả bốn đều có "giải pháp cũ gãy" + đánh đổi.
P1 = 2 chỉ ở L01 (1/4 bài).

### 3. Lab

Lời giải tự viết trong `scratchpad\labA\` (chưa mở `loi_giai.*`); `bash labs/cham.sh BNK Lxx <tệp>` trả ĐÚNG cả 4 bài ngay lần đầu. `cham.sh` trên `loi_giai.java` của kho: ĐÚNG cả 4.

| Bài | tự làm được | thời gian | kẹt ở đâu | mong_doi khớp màn hình | ghi chú |
|---|---|---|---|---|---|
| L00 | có | ≈8 phút | không kẹt; đề đủ (ba dòng in, tên biến) | khớp (3 dòng giống step "Kết quả mong đợi") | Cần biết `long`, `double`, `println`; `long` chỉ được gọi bằng lời "số nguyên dài". |
| L01 | có | ≈12 phút | không kẹt; đề liệt kê `static long tong`, `KHOA`, `synchronized`, `start/join` nên gần như điền chỗ trống | khớp (`tong = 600000`) | Thay `synchronized` bằng `AtomicLong` cũng ĐÚNG; đề không cấm (không ảnh hưởng mục tiêu). |
| L02 | có | ≈8 phút (khung có sẵn, điền 2 TODO) | không kẹt; dự đoán 1/2/3 cần hiểu `this` không qua proxy (dạy ở `chay_that`) | khớp (3 dòng) | Đề tự chứa, không cần Spring; là mô phỏng (bài có nói). |
| L03 | có (phần) | ≈12 phút | "mỗi khoá in một dòng" (video) gợi 2 dòng, mong đợi 4 dòng (L03-a); gợi ý `computeIfAbsent` trong `de.md` giúp qua | khớp (4 dòng k1/k1/k2/k1) | "Phần": lab chỉ đo hàm chặn trùng trong bộ nhớ (mục tiêu 7); không có lab máy chủ + curl (mục tiêu 5) hay UNIQUE trong CSDL (mục tiêu 3 chỉ xem). |

### 4. Người học kẹt ở đâu

- L00: không kẹt ở chữ; kẹt nhẹ ở `chay_that` step 1 (≈05:18): "Tệp GiuThamChieu.java (phần chính)" thiếu `import java.lang.ref.WeakReference` và lớp bọc, `labs/` không có tệp để chạy lại; thêm `check` step 2 "Kiểu số thực nhị phân không biểu diễn đúng số không phẩy một" nói mà không giải thích.
- L01: `chay_that` step 5 (LuongAo.java, ≈06:00): "Bộ phân việc này tạo mỗi việc một luồng ảo ... tăng một biến đếm an toàn khi nhiều luồng cùng tăng" (`Executors.newVirtualThreadPerTaskExecutor`, try-with-resources, `Thread.sleep` trong lambda trả giá trị, `AtomicInteger` chỉ gọi bằng lời); trước đó `formula` step 3 "Chạy thử cả sáu cách" không liệt kê.
- L02: `chay_that` step 2 (≈06:10): "Proxy.newProxyInstance(...) (p, m, a) -> { ... m.invoke(that, a); }" — lời chỉ nói "Đoạn có mũi tên là việc proxy làm", không giảng lambda ba tham số và `m.invoke`; sau đó `quy_mo` "hộp kết nối cần ít nhất T·(C−1)+1" không định nghĩa hộp kết nối và không suy ra công thức.
- L03: `chay_that` step 2 (≈04:45): `sv.createContext("/chuyen", ex -> tra(ex, "so du " + (a -= 500_000)))` và `daXuLy.computeIfAbsent(ex.getRequestHeaders().getFirst("Idempotency-Key"), k -> ... (b -= 500_000))` — lời kể mục đích nhưng không giảng `HttpExchange`, lambda `ex ->`, tác dụng phụ `a -= 500_000` trong biểu thức; thêm `quy_mo` step 2 "Nhân viên đối soát" không giảng.

### 5. Số đã tính lại / mã đã chạy

- Số tính lại bằng Python: 39 phép kiểm (≈70 số), khớp 39/39. L00: 0,1×10 = 0.9999999999999999, 0,3×20 = 5.999999999999998 (≠ 6,0), 1024², 4·1024³, 419 430 s = 4,9 ngày, 4 194 s = 70 phút, 42 s, 10 240 / 1 024 000 / 102 400 000 B, 10 000 mục = 10 240 000 B, 4096 MB, 6−3 = 3, 5 rác = 500 B, quiz 4−2 = 2 và 2·50 = 100, `Decimal(0.1)` ≠ `Decimal('0.1')`. L01: vét cạn 6 dãy = {180: 2, 130: 2, 150: 2}, 90 cách cho 3 luồng (6!/8), 5 s, 8 s, 2000 req/s, 500 s = 8,3 phút, 50 000 s = 13,9 giờ, 10 GB/1 TB/100 TB, 10 MB/1 GB/100 GB. L02: 6/501/50 001. L03: 3×500 000, 500 000 còn lại, 1 000 000 oan, quiz 0 và 800 000, 100/10 000/1 000 000 lệnh trùng, 5·10^7/5·10^9/5·10^11 đồng, 6,4 MB/640 MB/64 GB, lab 2 300 000 và 1 600 000.
- Mã chạy thật (JDK 21.0.13) và khớp màn hình: L00: GiuThamChieu, RoRi (true/false trên G1; true/true trên SerialGC/ZGC, L00-a), CongTien (`0.9999999999999999 | 1.0 | 10 phan muoi`), SoSanh, PhiLech. L01: CoKhoa, LuongAo (0,77–0,90 s), TongBaLuong, MatCapNhat (không ổn định, L01-a). L02: ProxyGiaoDich (6 dòng khớp), ChuyenKhoanProxy (1/2/3). L03: MayChu + 6 lệnh curl (6 dòng khớp), XuLyTrung, sqlite KhoaLuyDang bằng Python `sqlite3` (COUNT = 1, `so du 1500000`). Tổng 14 chương trình + 4 lab tự viết + 4 loi_giai qua cham.sh.
- Mã chỉ đọc: không có. Spring thật chưa chạy (không có thư viện); khẳng định về Spring/HikariCP dựa vào tài liệu và kiến thức vững.
- Cảnh "chạy thật": L00 và L01 là JVM thật (`Thread.sleep(100)` ở L01 được ghi rõ "giả làm đang chờ đối tác"); L02 là mô phỏng bằng `java.lang.reflect.Proxy`, câu đầu nói rõ "Ta mô phỏng cơ chế proxy" (xem L02-a); L03 là máy chủ `com.sun.net.httpserver` + curl + sqlite thật (không phải framework REST; có ghi "cách bỏ qua nếu trùng là riêng của cơ sở dữ liệu này"). Không bài nào dễ hiểu nhầm thành Redis/Kafka/Oracle thật.
- Đo thời gian: L01 LuongAo có ghi "đúng khi máy không quá tải"; L00 RoRi không có ghi chú (L00-a); L01 MatCapNhat trình bày như xác định (L01-a).

### 6. Khung hình đã xem

- L00 (10): 00000 (hook, 0 s), 00023 (stack/heap, 138 s; nhãn "tham chiếu" bị mũi tên cắt ngang), 00030 (đồ thị gốc→A→B→C, D→E, F, 171 s; sạch), 00056 (mã GiuThamChieu, 319 s), 00070 (kết quả RoRi, 389 s), 00080 (so ba cách lưu tiền, 433 s), 00107 (quiz, 571 s), 00122 (quy mô heap, 651 s; công thức + bảng đọc được), 00134 (đề tự làm, 713 s), 00148 (tổng kết, 876 s).
- L01 (8): 00000 (hook), 00027 (xen kẽ xấu, 142 s: mũi tên xuất phát dưới hộp "A đọc", không có mũi tên B), 00038 (200 luồng nền vs luồng ảo, 183 s; sạch), 00063 (mã CoKhoa, 334 s), 00097 (đáp án quiz câu 1, 539 s), 00106 (bảng quy mô, 584 s; cột "×10 000" ngắt dòng "×10 / 000", không che chữ), 00112 (giải pháp cũ gãy, 620 s), 00123 (kết quả mong đợi lab, 801 s).
- L02 (8): 00000 (hook), 00033 (Controller→Proxy→TransferService, 187 s), 00042 (this.ghiVet không qua proxy, 225 s), 00064 (mã ProxyGiaoDich phần 1, 347 s), 00073 (kết quả chạy proxy, 396 s), 00092 (quiz, 498 s), 00104 (bảng T·(C−1)+1, 576 s), 00110 (vì sao kẹt, 613 s; "HikariCP" chỉ trên màn hình, lời nói "thư viện kết nối phổ biến").
- L03 (8): 00000 (hook), 00028 (phản hồi mất, 134 s), 00033 (khoá chặn trùng, 154 s; nhãn "ghi" bị mũi tên cắt ngang), 00058 (mã MayChu phần 2, 287 s), 00066 (kết quả 6 dòng curl, 326 s), 00097 (quiz, 482 s), 00110 (bảng thiệt hại + bảng khoá, 572 s), 00139 (tổng kết, 842 s).
- Không thấy chữ tràn/đè/cắt nặng; ba lỗi hiển thị nhẹ như trên. mp4 ≤ 16 phút cả 4 bài (14:12 đến 14:52, đã gồm 110–145 s dừng). SRT khớp `say` 100% (152/137/133/142 câu, 0 câu thiếu).

### 7. E51 giáo án ↔ video

- L00 (5 mục tiêu): 1 stack vs heap → `intuition` step 1 dạy, không câu đo (lệch nhỏ); 2 đồ thị tham chiếu → `formula` + `example` + quiz Q1/Q2 (đo được); 3 rò rỉ static + chạy thật → `chay_that` + `pitfalls` Lỗi 2 (kết quả RoRi phụ thuộc GC, L00-a); 4 ×100/×10 000 → `quy_mo`; 5 kiểu dữ liệu cho tiền → `check` + quiz Q3 + `practice`. Ví dụ giáo án khớp `example` và `hook`.
- L01 (5): 1 "Liệt kê mọi cách xen kẽ" → `formula`/`example` (chỉ đếm + tally, L01-b); 2 khoá làm chạy lần lượt → `intuition` step 2 + `chay_that` CoKhoa; 3 thời gian theo lô vs luồng ảo → `check` + quiz Q2; 4 chọn luồng nền/luồng ảo ×100/×10 000 → `quy_mo` (ghi cả giới hạn của luồng ảo); 5 viết mã dùng khoá → `practice`. Ví dụ giáo án khớp.
- L02 (6): 1 "Nêu cách Spring tạo bean và trao proxy" → `sym` + `intuition` (dạy, không câu đo); 2 dự đoán số giao dịch → `example` + quiz; 3 lỗi gọi cùng lớp → `pitfalls` Lỗi 2 + `chay_that`; 4 chỗ đặt hàm ghi vết → quiz Q3; 5 kết nối tối thiểu ×100/×10 000 → `quy_mo` (công thức không suy); 6 viết phần đếm proxy → `practice`. Ví dụ giáo án khớp `hook` + `example`.
- L03 (7): 1 vì sao thử lại bình thường → `intuition` step 1 + `formula` Bước 1; 2 tiền trừ oan → `example` ①–⑤ + quiz Q1/Q2; 3 bảng khoá chặn trùng → `check` (sqlite chạy thật), không có lab; 4 phương thức an toàn/lũy đẳng → `sym` + bảng ở `check` (đúng RFC 9110); 5 chạy máy chủ nhỏ + curl → `chay_that` (chỉ xem, thiếu tệp đủ, L03-b); 6 thiệt hại và dung lượng bảng khoá → `quy_mo`; 7 viết hàm chặn trùng → `practice`. Ví dụ giáo án khớp.

### 8. Pháp lý/sản phẩm

`audit/legal/registry.yaml` không có mục nào cho L00–L03 (bài không dẫn văn bản pháp luật Việt Nam; chỉ dẫn chuẩn kỹ thuật).

| Dữ kiện | Kết quả |
|---|---|
| JEP 444 (JDK 21): luồng ảo ghim khi chờ trong `synchronized` hoặc native | CONFIRMED |
| JEP 491 (JDK 24): `synchronized` không còn ghim; native/foreign vẫn ghim | CONFIRMED |
| JEP 248: G1 mặc định từ JDK 9 trên máy server-class; evacuation | CONFIRMED; máy 1 CPU/ít RAM chọn SerialGC (đã chạy, ảnh hưởng L00-a) |
| `System.gc()` chỉ là gợi ý (`-XX:+DisableExplicitGC` làm `sau khi bo: true`, đã chạy) | CONFIRMED |
| `WeakReference`, `BigDecimal(String)` vs `BigDecimal(double)`, double 0,1×10 | CONFIRMED (đã chạy) |
| Ngăn xếp luồng nền mặc định thường 1 MB (tuỳ hệ điều hành) | CONFIRMED |
| Spring: self-invocation bỏ qua `@Transactional` ở chế độ proxy; REQUIRES_NEW giữ thêm kết nối; rollback mặc định RuntimeException/Error, checked vẫn commit | CONFIRMED (kiến thức + Spring Reference trong `source`); chưa chạy Spring |
| Spring Boot proxy mặc định là CGLIB (L02-a) | CONFIRMED |
| HikariCP: `maximumPoolSize` = 10, `connectionTimeout` = 30 000 ms; công thức Tn × (Cm − 1) + 1 | CONFIRMED |
| RFC 9110: GET an toàn + lũy đẳng; PUT, DELETE lũy đẳng không an toàn; POST không lũy đẳng | CONFIRMED |
| `Idempotency-Key` làm tiêu đề (dự thảo IETF, chưa phải RFC); "phải từ chối khi cùng khoá khác nội dung" | PLAUSIBLE (thực hành Stripe/IETF draft; bài không dẫn nguồn) |
| sqlite `INSERT OR IGNORE` + PRIMARY KEY | CONFIRMED (đã chạy bằng Python sqlite3) |
| "vượt giới hạn của cơ sở dữ liệu" ở 50 001 kết nối (L02 `quy_mo`) | PLAUSIBLE |

### 9. Nhận xét

- Nội dung kỹ thuật chính xác, phép tính khớp, SRT khớp `say` 100%, 0 MUST; lỗi thật nằm ở mã "Chạy thật" trình bày như xác định (MatCapNhat, RoRi) và vài chỗ nền chưa giảng.
- Điểm yếu chung: P1 (chỉ L01 đạt 2) và P7 (mỗi bài có một mục tiêu giáo án chỉ được xem, không được đo/làm); P8 và P9 đạt 2 cả bốn bài.
- L01 mạnh nhất về lab và quy mô (nêu cả giới hạn của luồng ảo); L02 mô phỏng proxy sạch nhưng nền Spring (container, tiêm phụ thuộc, hộp kết nối) mỏng và không có Spring thật; L03 thiếu MayChu.java đầy đủ để người học tự chạy.
- Mã `chay_that` ở L00/L01/L03 hiện "phần chính" không có import/lớp bọc và không có trong `labs/`: người học làm được các lab nhỏ nhưng không tái hiện được các cảnh minh hoạ chính.
- Thứ tự sửa đề xuất: L01-a, L00-a/b, L03-a, L03-b, L02-a, L01-b, rồi các chỗ P1 ("đối soát", "hộp kết nối", "đường nóng").

## Phụ lục B
#### Phần B — BNK L04, L05, L06, L07: đã đọc 4/4 bài (YAML đọc trọn, srt so với `say`, 33 khung hình, lab tự làm)

Điều kiện đọc: chỉ đọc kho `D:/research-video`; mọi tệp tạm ở `scratchpad\labB\`. Không chạy docker/build/tts/asr/render/gen/git; không mở các tệp bị cấm. Không nghe được âm thanh (chỉ đọc `say`, `.srt`, `asr_report.md` của bản dựng).
Thời lượng lấy từ `ffprobe` mp4 và tổng `duration` trong `_frames.txt`. `.srt` của cả 4 bài khớp `say` từng từ (difflib: 1883/2143/2142/2087 từ, tỉ lệ 1,0000).

### 1. Chuẩn xác

| Bài | Mức | Cảnh/step | Trích nguyên chữ | Vì sao sai + bằng chứng đã chạy | Đề xuất sửa | Tin cậy |
|---|---|---|---|---|---|---|
| L04 | SHOULD | `intuition` step 1, SVG (khung `frames/00033.png`) | nhãn "tầng 1 (nút gốc): 100 lối rẽ", "tầng 2: 100 lối rẽ", "tầng 3 (lá)" (chỉ 3 tầng, mỗi nút 2 mũi tên) | Hình dựng 3 tầng/2 nhánh, trong khi bài khẳng định 10 000 000 dòng cần **4** tầng (`100**4 ≥ 10**7`, tính lại: 4). Không ghi "hình rút gọn". | Thêm nhãn "rút gọn: thật là 100 nhánh/nút" hoặc vẽ tầng 4 | CONFIRMED |
| L04 | SHOULD | `formula` step 3, `example` ⑤ | "$4 + 1 = 5$ lần đọc thay vì $10\,000\,000$" | Hai vế khác đơn vị: 5 là số nút/khối chỉ mục, 10 000 000 là số dòng; quét thật đọc theo khối. Chênh vẫn lớn nhưng không ghi chú. Không có số sai (21/21 khớp). | Ghi chú đơn vị | PLAUSIBLE |
| L05 | **MUST** | `check` step 1 `say` đối chiếu `chay_that` step 1 `show` và `curriculum/bnk.yaml` L05 `example` | check: "Mô phỏng chỉ kiểm logic thứ tự khoá, còn cú pháp riêng của Oracle thì máy này không chạy được." — chay_that: "PL/SQL chạy thật trên Oracle 26ai Free (Docker)" — giáo án: "(mô phỏng; Oracle không chạy trên máy)" | Ba chỗ nói ngược nhau. `audit/bnk/src/l05.py` khai `lang="oracle"`, `audit/review/screen_code.py` (~dòng 614) chạy oracle qua Docker và trả NOT_VERIFIED nếu không có container ⇒ nhiều khả năng PL/SQL đã chạy thật, câu "máy này không chạy được" và ghi chú giáo án là bản cũ. Tôi KHÔNG chạy Docker (bị cấm) nên không tự kiểm đầu ra Oracle. L04 cũng nói "Máy này không có Oracle". | Sửa câu ở `check` và `example` giáo án cho thống nhất | CONFIRMED (mâu thuẫn); PLAUSIBLE (đã chạy thật) |
| L05 | SHOULD | `intuition` step 1, SVG (`frames/00027.png`) | mũi tên xám "A đang do phiên 1 giữ" từ Phiên 1 sang Phiên 2; "muốn B", "muốn A" nằm đè lên nét đứt | `sym` định nghĩa đồ thị chờ: "mũi tên từ phiên đang chờ tới phiên đang giữ khoá"; hình vẽ ngược chiều (từ phiên giữ) và chỉ MỘT mũi tên, vòng tròn không được khép; nhãn bị gạch ngang. | Vẽ hai mũi tên chờ khép vòng, dời nhãn | CONFIRMED |
| L05 | SHOULD | `chay_that` step 1–2 | khối `DECLARE … END;` rồi "xong, tong truoc = 1500000 / 2 700000 / 5 800000" | Màn hình không có `CREATE TABLE bnk_tk`, hai dòng khởi tạo (id 2 = 1 000 000; id 5 = 500 000) và câu SELECT cuối sinh hai dòng kết quả (có trong `src/l05.py`). Người học không tái hiện/không suy ra được các số. | Hiện đủ phần dựng bảng và SELECT | CONFIRMED |
| L05 | SHOULD | `quy_mo` step 1–2 | "mỗi cặp có xác suất 0,0001 khoá ngược thứ tự nhau … ≈ 500 000", "ở ×10 000 liên tục" | Số học đúng (45; 499 500; 4 999 950 000; 0,0045; 49,95; 499 995). Nhưng giả định xác suất mỗi cặp không đổi khi T tăng ×10⁴ là điều kiện then chốt, không nói; 100 000 phiên đồng thời tranh hai hàng là phi thực tế. | Ghi giả định "số hàng nóng giữ nguyên" | PLAUSIBLE |
| L05 | SHOULD | `pitfalls` step 2 | "đừng tin `ORDER BY … FOR UPDATE` khoá theo thứ tự ORDER BY" | Hành vi Oracle; nguồn trong `source`. Không chạy được Oracle để tái hiện. | Dẫn nguồn cụ thể | PLAUSIBLE |
| L06 | **MUST** | `quy_mo` step 2, hộp "Giải pháp cũ gãy ở đâu" (`frames/00114.png`) | "Tăng tỉ lệ trúng lên 99% còn 200; muốn xuống mười thì phải trúng 99,9%" | 1 000 000 × (1 − 0,999) × 0,02 = **20** kết nối, không phải 10; muốn 10 cần h = 1 − 10/20 000 = **99,95%** (`labB\run\nums.py`: DIFF 20 vs 10). Chỉ nằm trên màn hình; `verify_bnk.py` dòng 310 không kiểm câu này. | "…phải trúng 99,95%" | CONFIRMED |
| L06 | SHOULD | `quy_mo` step 2; `prereq` đánh số | "(cần 20 kết nối, hộp vài chục là đủ)"; ⑦⑧ hiện trước ④⑤⑥ | "hộp" là từ lạ (ý hồ/pool kết nối, chưa giảng pool); số thứ tự nhảy. Không sai kiến thức. | Sửa từ, sắp lại số | CONFIRMED |
| L06 | SHOULD | `prereq` ④, `sym`, `intuition` step 3, MaChan | ④ "khoá phân tán … đặt ở một nơi lưu chung như Redis"; sau đó "Nơi lưu nhớ mã chặn lớn nhất = 2" | Cùng nhãn "nơi lưu" chỉ hai thứ: Redis (giữ khoá) và tài nguyên được ghi (CSDL); theo Kleppmann phía tài nguyên kiểm mã chặn. Dễ hiểu nhầm Redis từ chối. Chưa nói ai cấp bộ đếm. | Đổi nhãn thành "kho dữ liệu được ghi" | PLAUSIBLE |
| L07 | SHOULD | `formula` step 1 "Làm thử", `say` | "khoá TK-1001 hai lần đều vào phân vùng 1" | "1" = `crc32('TK-1001') % 6` (chạy lại: 1; `tools/checklib.py` dòng 6925 ghi "Kafka thật dùng murmur2"). Tôi cài murmur2 (seed 0x9747b28c), kiểm khớp 4 vector Kafka UtilsTest (`"21"→-973932308`, `"foobar"→-790332482`, `"a-little-bit-long-string"→-985981536`, `"abc"→479470107`) rồi tính: Kafka thật cho phân vùng **2**. Ghi chú crc32 chỉ nằm ở `source`, không hiện/không đọc. | Ghi "băm minh hoạ, Kafka thật dùng murmur2 nên ra số khác" | CONFIRMED |
| L07 | SHOULD | `formula` step 3; `check`; `pitfalls` 2–3; `quiz`; `recap` (10 lần) | "làm việc xử lý lũy đẳng", "khoá lũy đẳng" | Kết luận của bài nhưng không giảng ở L07 (chỉ L03 dạy). Cơ chế (tập mã đã xử lý) có ở `check` nhưng không gắn với từ. | Định nghĩa ở lần đầu | CONFIRMED |
| L05·L06·L07 | SHOULD | các khối mã `chay_that` | "(phần 1)", "(phần chính)" | Mã hiện là mảnh: thiếu `import`, `public class`, và `}` đóng `main`/lớp (BeTac, MaChan, GhiNho). Tôi phải thêm vỏ mới biên dịch (đã chạy, khớp màn hình). | Ghi "chỉ phần chính" hoặc đưa mã đủ vào lab | CONFIRMED |

Không phát hiện sai kiến thức ở: ORA-00060 (chỉ câu lệnh bị huỷ), SELECT thường không khoá hàng, khoá ngoại không chỉ mục/ITL, SQLite plan, Redis SET NX PX, Redlock không cấp fencing token, Kafka rebalance/offset/commit, EOS chỉ trong Kafka.

### 2. Độ sâu

| Bài | sha16 | Phút (lời đọc ≈ / thật) | P1 | P2 | P3 | P4 | P5 | P6 | P7 | Tổng | P8 | P9 | Mất gốc | Cần biết trước | Chỗ thiếu chính |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| L04 | 6a8aabf4ed0668ce | ≈10,8 (1883 từ) / 13:40,5 | 1 | 1 | 1 | 2 | 2 | 2 | 1 | **10** | 2 | 2 | GẦN | "lối rẽ", "chỉ mục nhiều cột (account_id, created)", byte/MB/GB, bộ nhớ vs đĩa | P1: "lối rẽ" (hook dùng trước `intuition`), "chỉ mục nhiều cột" chưa giảng. P2: `prereq` ④ dạy tìm nhị phân nhưng cây 100 lối rẽ không nối với nó. P3: hình 3 tầng vs 4 (00033). P7: mục tiêu 2–3 không có quiz/lab đo. P6 thiếu: độ chọn lọc thấp/thống kê cũ khiến tối ưu vẫn quét. |
| L05 | 8ebacd73f6b5afcc | ≈12,2 (2143 từ) / 14:36,3 | 1 | 1 | 1 | 2 | 2 | 2 | 1 | **10** | 2 | 2 | GẦN | INITRANS (chỉ hiện trên màn hình), "Docker"; `Lock`/`tryLock`/luồng Java | P1: INITRANS, Docker. P2: T(T−1)/2 chỉ nêu, không suy. P3: vòng chờ không khép, mũi tên ngược định nghĩa, nhãn bị gạch (00027). P7: giáo án `example` ≠ bài; mục tiêu 4 (xử lý ORA-00060) không có phép đo. Lab chỉ sắp thứ tự, không tái tạo bế tắc. |
| L06 | edcd65d9d32a6b86 | ≈12,0 (2142 từ) / 14:53,3 | 1 | 2 | 1 | 2 | 2 | 2 | 2 | **12** | 2 | 2 | ĐỦ (sát ngưỡng; còn 1 MUST) | "thu gom rác" (L00), "luồng", định luật Little chỉ phát biểu, hồ kết nối | P1: "thu gom rác". P3: mũi tên gạch "20 ms" và nhãn (00034), nhãn "1 < 2 → từ chối" bị gạch (00042). Số sai "99,9% → 10". Chưa nói: eviction, vô hiệu bộ đệm. |
| L07 | 16d0b3507ced62bd | ≈11,8 (2087 từ) / 14:41,6 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | **13** | 2 | 2 | ĐỦ | "lũy đẳng" (10 lần), "giao dịch cơ sở dữ liệu", "tệp mở", `Arrays.toString`/`StringBuilder` | P1: lũy đẳng, giao dịch CSDL. Chưa nói phía gửi (acks, idempotent producer), khoá lệch gây phân vùng nóng, lag, cooperative rebalance. |

P1 = 2: 0/4 bài (ngưỡng ≥ 90% KHÔNG đạt). P8 = 2: 4/4 theo thang, nhưng L04 không bắt chạy EXPLAIN, L05 không tái tạo bế tắc. MUST: 2 (L05 mâu thuẫn Oracle; L06 99,9%). Lời đọc ≈ = thời lượng thật trừ 2 lần dừng (25 s + 150 s hoặc 120 s).

### 3. Lab

Không có `sqlite3` CLI → `cham.sh` dùng `labs/sqlrun.py` (Python 3.11, sqlite 3.49.1). JDK 21. Lời giải TỰ viết trước khi mở `loi_giai.*`; tệp ở `scratchpad\labB\`.

| Bài | tự làm được | thời gian | kẹt ở đâu | mong_doi khớp màn hình | ghi chú |
|---|---|---|---|---|---|
| L04 | có | ≈ 8 phút | không kẹt (bài không dạy INSERT nhiều dòng một lệnh; tôi dùng 7 INSERT riêng, vẫn đúng) | khớp (7 dòng `1\|900000 … 13\|300000`) | tự viết **ĐÚNG**; `loi_giai.sql` **ĐÚNG**. Không đo mục tiêu 2–3. |
| L05 | có | ≈ 5 phút | không kẹt ("Nếu kẹt" gần như là lời giải) | khớp (4 dòng) | tự viết **ĐÚNG**; `loi_giai.java` **ĐÚNG**. Không chạm tới bế tắc. |
| L06 | có | ≈ 8 phút | không kẹt (cần biết `import java.util.*`, màn hình không hiện) | khớp `trung 36/40, trung binh 5.0 ms` (4×32 + 36×2 = 200; /40 = 5,0) | tự viết **ĐÚNG**; `loi_giai.java` **ĐÚNG**. Không đụng mã chặn. |
| L07 | có | ≈ 8 phút | không kẹt (ví dụ + "Nếu kẹt" cho sẵn công thức) | khớp (10 dòng) | tự viết **ĐÚNG**; `loi_giai.java` **ĐÚNG**. Số khác ví dụ nhưng không có phần thí nghiệm. |

### 4. Người học kẹt ở đâu

- L04: `formula` step 1 (03:08) "Cây L tầng chứa được tối đa f mũ L dòng" — hình trước chỉ 2 nhánh/nút, chưa nối từ tìm nhị phân sang "100 lối rẽ"; kẹt rõ ở `check`/`pitfalls` Lỗi 3 (05:42–07:15) "chỉ mục (account_id, created)".
- L05: `chay_that` step 1 (≈05:02) "SELECT so_du INTO v_nho FROM bnk_tk WHERE id = 2 FOR UPDATE" — bảng `bnk_tk`, `INTO`, `DBMS_OUTPUT` chưa dựng/giảng; sau đó `quy_mo` (10:03) "T·(T−1)/2" không suy.
- L06: `intuition` step 2 (≈03:20) "A tạm dừng… (ví dụ thu gom rác)" chưa giảng; rồi "Nơi lưu nhớ mã chặn lớn nhất" không rõ Redis hay CSDL.
- L07: `formula` step 3 (≈03:45) "và làm việc xử lý lũy đẳng" — chưa giảng, lặp 10 lần tới `recap`.

### 5. Số đã tính lại / mã đã chạy

- **L04**: tính lại 21 (số tầng 3/4/5/3, 100², 100³, 100⁴, 4+1, 3+1, quét 0,1/10/1000 s, 16,7 phút, chỉ mục 1,6 MB/160 MB/16 GB, tìm nhị phân tối đa 11 lần trên 1024 (vét cạn), 2¹⁰, 5000/500 = 10, tỉ lệ ×100/×10 000), khớp 21/21. Mã chạy: SQLite 3.49.1 dựng `tx` 5000 dòng, `COUNT = 5000`, ba `EXPLAIN QUERY PLAN` ra đúng `2|0|216|SCAN tx`, `2|0|56|SEARCH tx USING COVERING INDEX i_tk (tk=?)`, `2|0|216|SCAN tx`; bảng `check` (5 điều kiện × 2 = 10 ô) khớp. "Chạy thật" là SQLite thật, ghi rõ, nêu tên Oracle tương đương.
- **L05**: tính lại 13 (2×2, 3!, T(T−1)/2 ở 10/1000/100 000, kỳ vọng 0,0045/49,95/499 995, tỉ lệ, 1 500 000, 700 000 + 800 000, 2 cặp ngược), khớp 13/13. Chạy: `BeTac.java` (thêm vỏ) → "be tac" / "xong" khớp. Chỉ đọc: PL/SQL `KhoaTheoThuTu` (cần Oracle/Docker, bị cấm; phép tính 700 000/800 000 khớp). "Chạy thật": PL/SQL khai chạy thật trên Oracle (chưa tự xác nhận, xem MUST); Java ghi rõ "mô phỏng".
- **L06**: tính lại 21 (T = 3/11/1,2; 6,7; 1,8; 16,7; quiz 8 và 3,75; 12−10; 300/100; 9 ô kết nối 0,2…20 000; lab 5,0; "99,9% → 10"), khớp 20/21, **1 sai**. Chạy: `BoDem.java` ("trung 90/100, trung binh 3.0 ms") và `MaChan.java` (true/false/B) khớp. Là mô phỏng bằng `HashMap`, ghi rõ ("Redis thật cần cài riêng", tiêu đề "mô phỏng"). Không có Redis thật.
- **L07**: tính lại 17 (13 = 2×6+1, 6/3, 6/2, 8−6, [3,3,2,2], 12−10, 5/500/50 000, 3 600 000/1 785 600 000/179 985 600 000, tổng 6 và 4, lab 7/9), khớp 17/17. Chạy: `ChiaPhanVung.java`, `GhiNho.java` ([1,1,0,1,1] / [1,1,2,1,1]) khớp. Thêm murmur2 tự cài (kiểm 4 vector Kafka) → `TK-1001` phân vùng 2. Tiêu đề ghi "(mô phỏng bằng Java)".
- Tổng: 72 phép số, 71 khớp, 1 sai (L06). Chạy 5 chương trình Java, 2 kịch bản SQLite, 4 lab tự viết + 4 lời giải mẫu: tất cả khớp. Chỉ đọc: PL/SQL Oracle (L05); cú pháp Redis và Kafka thật không có trong bài/không có thư viện.

### 6. Khung hình đã xem (33 khung; thời điểm = cộng dồn `duration`)

- **L04** (9): 00001 (0:10), 00033 (2:50), 00062 (5:35), 00066 (5:55), 00086 (8:00), 00098 (8:50), 00102 (9:15), 00111 (10:05), 00121 (13:20). Không đè/cắt chữ; chỉ sai nội dung ở 00033 (3 tầng vs 4).
- **L05** (8): 00001 (0:08), 00027 (2:10), 00055 (4:30), 00064 (5:22), 00068 (5:45), 00073 (6:12), 00082 (7:00), 00115 (10:20). Lỗi: 00027 nhãn "muốn B/A" bị nét đứt gạch, vòng chờ không khép; 00068 chú thích `// xin hàng thứ hai, chờ tối đa 0,5 giây` tràn ra ngoài khung mã; 00073 mã không có `}` đóng.
- **L06** (8): 00034 (2:55), 00038 (3:20), 00042 (3:35), 00063 (5:45), 00070 (6:25), 00093 (8:20), 00107 (9:50), 00114 (10:25). Lỗi: 00034 mũi tên xuyên chữ "20 ms", nhãn "2. trượt → hỏi tiếp" bị gạch, mũi tên "trúng → trả" đứt khỏi ô Redis; 00042 nhãn "1 < 2 → từ chối" bị gạch; 00070 chú thích sát mép phải, thiếu `}`; 00114 có "99,9%" sai và "hộp".
- **L07** (8): 00029 (2:25), 00031 (2:35), 00033 (2:45), 00052 (4:35), 00060 (5:20), 00070 (6:20), 00083 (7:30), 00107 (10:00), 00132 (14:30). Không thấy lỗi hiển thị.

### 7. E51 giáo án ↔ video

- **L04**: (1) số tầng → `formula`, `example`, quiz Q1–Q2 ✓. (2) đọc kế hoạch → `chay_that`, `check` ✓ — **không có phép đo**. (3) điều kiện vô hiệu → `chay_that` (`tk + 0`), `check`, `pitfalls` ✓ — **không có phép đo**. (4) lợi hại → `pitfalls` Lỗi 1, quiz Q3 ✓. (5) quy mô → `quy_mo` ✓. (6) viết SQL → `practice` + lab ✓. Ví dụ giáo án khớp video.
- **L05**: (1) vòng chờ → `intuition` (hình lệch định nghĩa) ✓; (2) đếm cặp → `formula`, `check` ✓; (3) quy tắc id tăng → `example`, quiz Q2, lab ✓; (4) xử lý ORA-00060 → `pitfalls` Lỗi 3, `recap` ✓ (chỉ nói); (5) chạy PL/SQL + mô phỏng → `chay_that` ✓ nhưng giáo án `example` nói "Oracle không chạy trên máy" — **lệch**; (6) quy mô → `quy_mo` ✓.
- **L06**: (1) `formula`, `example`, quiz ✓; (2) `intuition`, `formula` ✓; (3) `intuition`, `chay_that` ✓; (4) quiz Q3, `pitfalls` Lỗi 3 ✓; (5) `chay_that` ✓; (6) `quy_mo` ✓ (kèm số sai); (7) `practice` + lab ✓. Ví dụ giáo án khớp.
- **L07**: (1) `example`, `chay_that`, lab ✓; (2) `formula` step 1 ✓; (3) `example` ④⑤, `chay_that` ✓; (4) `check`, quiz Q3 ✓; (5) `chay_that` ✓; (6) `quy_mo` ✓; (7) `practice` + lab ✓. Ví dụ giáo án khớp.

### 8. Pháp lý/sản phẩm

`audit/legal/registry.yaml` không có mục nào cho L04–L07 (không có văn bản pháp lý trong 4 bài). Dữ kiện sản phẩm:
- SQLite `EXPLAIN QUERY PLAN`: `SCAN tx` (≥ 3.36), `SEARCH … USING COVERING INDEX`, bọc cột mất chỉ mục, chỉ mục (account_id, created) không dùng cho điều kiện chỉ có `created` (không ANALYZE) — CONFIRMED (chạy lại 3.49.1).
- Oracle TABLE ACCESS FULL / INDEX RANGE SCAN / INDEX SKIP SCAN là tên tương đương; B-tree hàng trăm lối rẽ/khối — CONFIRMED.
- Oracle ORA-00060: chỉ câu lệnh bị roll back, khoá cũ còn, phải rollback giao dịch rồi thử lại; SELECT thường không khoá hàng — CONFIRMED.
- Khoá ngoại không chỉ mục khoá bảng con khi xoá/sửa khoá chính bảng cha (từ 9i chỉ trong thời gian câu lệnh); ITL/INITRANS có thể dẫn tới ORA-00060 — CONFIRMED (diễn đạt rút gọn). `ORDER BY … FOR UPDATE` không bảo đảm thứ tự khoá — PLAUSIBLE.
- Redis `SET key value NX PX`; nhả khoá nguyên tử bằng script; Redlock không cấp fencing token; khoá có hạn bị hai người giữ khi tạm dừng (GC); định luật Little — CONFIRMED.
- Kafka: mỗi phân vùng một bộ đọc trong nhóm; số phân vùng chỉ tăng; đổi số phân vùng đổi ánh xạ khoá; chia đoạn liền kiểu Range (10/4 → 3,3,2,2); xử lý rồi commit ⇒ ít nhất một lần, commit rồi xử lý ⇒ nhiều nhất một lần; heartbeat luồng riêng, `max.poll.interval.ms`; EOS chỉ trong Kafka — CONFIRMED. Băm khoá thật là murmur2 (TK-1001 → phân vùng 2, không phải 1) — CONFIRMED bằng tính lại.

### 9. Nhận xét

- Số liệu và mã nhìn chung chắc (71/72 phép tính, 100% mã chạy khớp màn hình, srt trùng `say`); lỗi thật chỉ có: "99,9% → 10" (L06) và mâu thuẫn Oracle chạy thật hay không (L05, kèm giáo án).
- P1 chưa đạt ngưỡng ở cả 4 bài (mỗi bài còn 1–2 từ); đáng tiếc nhất là "lũy đẳng" (L07) dùng 10 lần mà không giảng.
- Hình cơ chế có lỗi nhỏ ở L04, L05 (đồ thị chờ không khép vòng, nhãn bị gạch), L06 (mũi tên gạch chữ); L07 sạch.
- Lab chạy đúng, chấm ĐÚNG cả 8 lần, nhưng đều là "đổi số rồi chép lại ví dụ": không lab nào bắt tái tạo hiện tượng chính (EXPLAIN, bế tắc, mã chặn, thứ tự ghi nhớ), gợi ý "Nếu kẹt" gần như trao lời giải.
- Hướng tới "senior": thiếu độ chọn lọc/thống kê (L04), NOWAIT/SKIP LOCKED (L05), eviction/vô hiệu bộ đệm (L06), phía gửi/khoá lệch/lag (L07); P9 đạt cả 4 bài.

## Phụ lục C
#### Phần C — BNK L08, L09, L10, L11 (đã đọc TRỌN 4/4 bài; YAML + curriculum + srt + 8–11 khung hình mỗi bài + lab tự làm + chạy lại số/mã)

Ghi chú nền: tệp `part_C.md` cũ (báo cáo PYT từ 05:02 cùng ngày) đã được sao lưu sang `part_C_PYT_stale_backup.md` trước khi ghi đè. YAML có mtime 2026-11-13 09:02, mp4 dựng 07:34–08:23 cùng ngày. Đã đối chiếu: toàn văn `say` trong YAML = toàn văn srt (L08 1952 từ, L09 1942, L10 2028, L11 2319, khớp 100%), và chữ `show` có mặt trong `_capture.html` (chỉ LaTeX không so được) → video khớp YAML hiện tại. Giọng đồng nhất vi-VN-NamMinhNeural (3 câu mỗi bài ghi "edge?" ở build_report, không lẫn giọng).

### 1. Chuẩn xác

| Bài | Mức | Cảnh/step | Trích nguyên chữ | Vì sao sai + bằng chứng đã chạy | Đề xuất sửa | Tin cậy |
|---|---|---|---|---|---|---|
| L09 | **MUST** | `quy_mo` step 1 (lời đọc; srt cùng chữ) | say: "Tải tăng mười nghìn lần, mất khoảng bốn ngày rưỡi." ; màn hình cùng bước: "≈ 4,2 ngày" | Tính lại: 365 000 000 000 dòng / 10^6 dòng/giây = 365 000 giây = 4,22 ngày (labC/t_nums.py). "Bốn ngày rưỡi" = 4,5 ngày, lệch màn hình và lệch phép tính (step 2 nói "bốn ngày", màn hình 4,2). Màn hình khác lời đọc ở một con số. | Sửa lời đọc: "khoảng bốn phẩy hai ngày" (hoặc "hơn bốn ngày") | CONFIRMED |
| L08 | **MUST** (hạ xuống SHOULD nếu coi `labs/sqlrun.py` là đường chạy duy nhất) | `chay_that` step 3 + `practice` step 3 + `labs/BNK/L08/de.md` mục 2 | say: "Lệnh chốt đầu tiên chỉ để kết thúc phần dựng bảng." ; de.md: "`COMMIT;` (để kết thúc giao dịch ngầm của câu `INSERT`)" ; Nếu kẹt: "Đừng quên `COMMIT;` ngay sau `INSERT INTO sodu`" | `COMMIT` ngay sau `INSERT` chỉ cần ở trình điều khiển Python (`sqlrun.py`, chế độ giao dịch ngầm). Ở engine sqlite autocommit (tương đương `sqlite3` CLI) câu `COMMIT;` đó LỖI: đã chạy `sqlite3.connect(isolation_level=None)` (sqlite 3.49.1): `COMMIT` → "cannot commit - no transaction is active"; chạy cả `outbox.sql` bằng `executescript` cũng lỗi y hệt. Ngược lại nếu bỏ COMMIT ở chế độ Python thì `BEGIN` lỗi "cannot start a transaction within a transaction". `de.md` tự gợi ý "`sqlite3 :memory: < outbox.sql` nếu máy có sqlite3" và `cham.sh` coi mã thoát khác 0 là "LỖI khi chạy" → người học dùng CLI sẽ thấy lời giải mẫu `loi_giai.sql` báo LỖI (mã thoát khác 0 của CLI khi có lỗi: PLAUSIBLE, máy này không có CLI để thử). Lời giải thích "giao dịch ngầm của INSERT" là hành vi của driver Python, không phải của SQLite. | Nói rõ: "chỉ cần khi chạy bằng sqlrun.py/Python; trong sqlite3 CLI bỏ dòng này", hoặc bỏ gợi ý CLI trong de.md và chỉ dùng sqlrun | CONFIRMED (lỗi engine); PLAUSIBLE (mã thoát CLI) |
| L08 | SHOULD | `hook` step 2 | say: "Bảng này là kết quả mô phỏng ở cuối bài. Ghi có lỗi mà không bù thì tiền mất dấu... Lưu xong rồi sập trước khi báo thì không có sự kiện nào được phát" | Video chỉ chạy: (a) nhật ký SAGA có bù; (b) Outbox chốt/huỷ (sqlite). Hai dòng của bảng ("ghi có lỗi, không bù → tiền mất dấu", "không Outbox → 0 sự kiện") KHÔNG có lần chạy nào ở cuối bài (chỉ có phát biểu ở ví dụ ⑤ và trong `checks`). Nhãn "kết quả mô phỏng ở cuối bài" nói quá. | Bỏ cụm "kết quả mô phỏng ở cuối bài" hoặc thêm một lần chạy "không Outbox" (ghi DB, sập, đếm sự kiện = 0) | CONFIRMED |
| L09 | SHOULD | `quy_mo` step 2 (+ lời đọc) | "Nhưng một dòng số dư mà mọi giao dịch cùng sửa sẽ thành **điểm nghẽn khoá** (như bài trước)" | Bài trước của L09 là L08 (SAGA/Outbox): không nói khoá/điểm nghẽn (grep L00–L08: "nghẽn khoá" 0 chỗ; khoá hàng ở L05). Tham chiếu sai, khái niệm không giảng tại chỗ. | Giảng một câu tại chỗ (mọi giao dịch xếp hàng chờ khoá dòng) hoặc ghi đúng "bài 5" | CONFIRMED |
| L09 | SHOULD | `pitfalls` step 1 | "Lưu số dư là một cột rồi **cộng trừ trực tiếp**. Hai giao dịch cùng lúc có thể ghi đè nhau" | Thiếu điều kiện: ghi đè (lost update) chỉ xảy ra khi đọc-rồi-ghi ở ứng dụng (SELECT rồi UPDATE giá trị tính sẵn). Câu `UPDATE ... SET so_du = so_du - x` (đúng dạng L08 dùng) được khoá dòng, không ghi đè nhau ở Oracle/PostgreSQL/SQLite. Người học có thể hiểu ngược. | Ghi rõ "đọc ra, tính ở ứng dụng, rồi ghi lại" | CONFIRMED (hành vi khoá dòng chuẩn); PLAUSIBLE về ý tác giả |
| L10 | SHOULD | `chay_that` step 4 (lời đọc) | "Hỏi trạng thái trước thì mọi trường hợp đều đúng một lần." | Tuyệt đối; mô phỏng `soLanGhiNo` không mô hình hoá việc lệnh gốc còn nằm trong hàng đợi (đã chạy lại HetGio.java: 2,1,1,1 — đúng nhưng chỉ vì mô hình bỏ qua đua). Chính bước 3 và bảng tình huống C/D của bài nói "chưa thấy chưa chắc chắn… phải dùng cùng mã tham chiếu hoặc Expiry". Hai chỗ mâu thuẫn nhẹ. | Thêm "…nếu gửi lại cùng mã tham chiếu" vào câu | CONFIRMED |
| L11 | SHOULD | `pitfalls` step 2, quiz đáp án 3, `quy_mo` step 2 | "ghi nguyên số thẻ… nhật ký phải che, ví dụ 6 số đầu và 4 số cuối" ; "vi phạm quy tắc che số thẻ" | Nội dung đúng (PCI DSS cho hiển thị tối đa BIN 6 + 4 cuối; PAN không được đọc được khi lưu) nhưng bài không nêu nguồn ("quy tắc che số thẻ" của ai?); `source` YAML cũng không liệt kê PCI DSS. | Nêu "PCI DSS" tại chỗ một lần | CONFIRMED (nội dung); thiếu nguồn |
| L11 | SHOULD (hiển thị) | `quiz` đáp án 1, khung 00109 | màn hình hiện "0𝑥30", "0𝑥20" (chữ x nghiêng kiểu toán) | Cảnh `formula` (khung 00053) in "0x70", "0x20" thẳng. Không sai nghĩa nhưng không nhất quán, có thể làm kẹt người mới ("0x" là dấu báo hex). | Dùng `\mathtt{0x30}` | CONFIRMED |

Không phát hiện thêm lỗi kiến thức ở: L08 (2i+1, thứ tự bù, điều phối/phối hợp, Outbox at-least-once + khử trùng, SAGA không cô lập), L10 (MessageID/CorrelationID của IBM MQ/JMS, OFS = Open Financial Service, Expiry, 44/120, kỳ vọng điểm cố định = 1), L11 (MTI 0200/0210, bit 1 = bản đồ thứ hai, DE 2/3/4/11/37/39, LLVAR tối đa 19, bản đồ 0x70/0x20, ISO 4217: VND 0, USD 2). Mọi số trên màn hình/lời đọc khác đã tính lại khớp (mục 5).

### 2. Độ sâu

Thời lượng thật (ffprobe): L08 836,97 giây = 13:57; L09 842,10 = 14:02; L10 874,97 = 14:35; L11 961,13 = 16:01 (vượt mục tiêu 16:00 khoảng 1 giây). Gồm tạm dừng 150 giây (Tự làm) + 25 giây (quiz). Lời đọc thuần ≈ thật − 175 giây.

| Bài | sha16 | Phút (lời đọc/thật) | P1 | P2 | P3 | P4 | P5 | P6 | P7 | Tổng(P1–P7) | P8 | P9 | Mất gốc | Cần biết trước | Chỗ thiếu chính |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| L08 | 51f9038cf6675d94 | 11,0 / 13,95 | 1 | 2 | 1 | 2 | 2 | 2 | 2 | 12 | 2 | 2 | ĐỦ (sát ngưỡng) | khoá lũy đẳng (L03: dùng ở "khoá lũy đẳng"/"bước bù không lũy đẳng", không định nghĩa lại); "tính cô lập" (ACID, L04–L05); Kafka (L07); SQL BEGIN/COMMIT/ROLLBACK, PRIMARY KEY/DEFAULT (L04); cách chạy tệp .sql (chỉ có trong de.md) | P1: "lũy đẳng"/"khoá lũy đẳng" (formula step 3 "khử trùng (khoá lũy đẳng)", pitfalls Lỗi 2) và "tính cô lập" không giảng tại chỗ. P3: nhãn "lỗi → quay lui" bị mũi tên cắt ngang (khung 00023, intuition step 1). SAGA "chạy thật" chỉ là chuỗi ghi log tự dựng, kết quả lặp lại công thức (vòng tròn); relay/Kafka không chạy, chỉ vẽ |
| L09 | 300d554ba2d0a67f | 11,1 / 14,03 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 13 | 2 | 2 | ĐỦ | khoá hàng/điểm nghẽn khoá (L05; "như bài trước" trỏ nhầm L08); ISO 4217 (chỉ nêu tên) | P1: "điểm nghẽn khoá", "tài khoản nóng" (quy_mo) không giảng. Quy ước nợ–có chỉ nhắc một câu (đúng, có lưu ý): "bút toán kép" ở đây là số có dấu. Một slide prereq gói ≥ 7 từ SQL (nghe nhanh). MUST lời đọc 4,5 ngày |
| L10 | b04095b92d4c796b | 11,7 / 14,58 | 1 | 1 | 1 | 2 | 2 | 1 | 1 | 9 | 2 | 2 | GẦN | khoá lũy đẳng (L03); kỳ vọng (expected value); Java HashMap/substring (JVA); "nhiều bản dịch vụ" = nhiều instance; Expiry (có giảng một câu tại chỗ) | P1: "kỳ vọng" (quy_mo), "nhiều bản dịch vụ", "phản hồi đang bay". P2: "kỳ vọng bằng 1 bất kể n" không chứng minh; "44 thứ tự" nói là vét cạn nhưng không hiện cách đếm, người học không tự làm tay được. P3: nhãn "tương quan = M7" và "M7" bị mũi tên cắt (khung 00027). P6/P7: tiêu đề "T24: OFS" nhưng không có bản tin OFS nào, không có chi tiết MQ thật (MsgId tự sinh, get theo CorrelId, syncpoint); mục tiêu 2 ("xác suất bằng vét cạn") chỉ đo bằng con số cho sẵn, lab không đo |
| L11 | 503cdaf2d5dbe32a | 13,1 / 16,02 | 1 | 2 | 2 | 2 | 2 | 2 | 1 | 12 | 2 | 2 | ĐỦ (sát ngưỡng) | PAN (nhãn trên hình/bảng, không giảng); bảng mã ký tự (ASCII/EBCDIC) ở Lỗi 3; xoay vòng nhật ký, băng thông; PCI DSS (quy tắc che số thẻ) | P1: "PAN", "bảng mã ký tự", "xoay vòng nhật ký". P7: mục tiêu 4 "Che số thẻ khi ghi nhật ký" chỉ là câu quy tắc, không có ví dụ che (411111******1111) và lab không đo; không có ví dụ số LLLVAR/bản đồ thứ hai. Prereq slide 2 gói 7 ký hiệu Python trong một khung. Tổng thời lượng 16:01 |

Mất gốc: ĐỦ = tổng ≥ 12 và không mục nào 0. Cả 4 bài P1 = 1, nghĩa là với ngưỡng cả khoá (P1 = 2 ≥ 90% số bài) 4/4 bài trượt; P8 = 2 cả 4 bài (đạt); P9 = 2 cả 4 bài.

### 3. Lab

Tự viết lời giải trước khi mở `loi_giai.*`; chấm bằng `bash labs/cham.sh BNK <Lxx> <tệp>` (máy này không có `sqlite3` nên cham.sh dùng `sqlrun.py`).

| Bài | tự làm được | thời gian | kẹt ở đâu | mong_doi khớp màn hình | ghi chú |
|---|---|---|---|---|---|
| L08 | có (nhờ de.md) | 10–15 phút | (1) video không nói cách chạy tệp `.sql`, chỉ de.md nói (`python labs/sqlrun.py` hoặc `sqlite3`); (2) quy tắc `COMMIT;` sau `INSERT` — lỗi với người dùng sqlite3 CLI (xem MUST thứ hai) | khớp (`2300000` / `lenh 77 da tru 700000\|0`; màn hình = mong_doi.txt) | lời giải tự viết: ĐÚNG; `loi_giai.sql`: ĐÚNG (bản tôi viết trùng 0 byte) |
| L09 | có | 8–12 phút | không kẹt; `HAVING SUM(tien) <> 0` và `GROUP BY ... ORDER BY tk` đều có trong bài (check + "Nếu kẹt"); thứ tự `C, D, phi` do ORDER BY nhị phân (chữ hoa trước chữ thường) — bài không giải thích nhưng đúng | khớp (`2` / `C\|-1256600` / `D\|1240000` / `phi\|6600`) | tự viết: ĐÚNG; `loi_giai.sql`: ĐÚNG (0 byte khác) |
| L10 | có | 15–20 phút | cham.sh bắt buộc `public class GhepPhanHoi` (viết `class GhepPhanHoi` không `public` → "không thấy 'public class Tên'", đã thử), de.md không nhắc; định dạng dòng in phải đúng từng ký tự | khớp (7 dòng, `1/6`) | tự viết: ĐÚNG; `loi_giai.java`: ĐÚNG (chỉ khác bố cục mã) |
| L11 | có | 8–12 phút | không kẹt; đề cho sẵn công thức `1 << (64 - số trường)`. Điểm mới so với ví dụ: trường 39 rơi vào byte thứ 5 (0x02), bài chỉ làm tay bit 3, 4, 11 | khớp (`3020000002000000` / `46`) | tự viết: ĐÚNG; `loi_giai.py`: ĐÚNG |

Đề đủ để tự làm từ kiến thức bài: có cả 4 (lab = ví dụ đổi số/đổi trường). Không lab nào có "thí nghiệm đổi tham số rồi quan sát"; P8 = 2 theo mức "bài tập có số khác ví dụ + kết quả mong đợi".

### 4. Người học kẹt ở đâu

- **L08**: `formula` step 3, "người nhận phải khử trùng (khoá lũy đẳng)" — "khoá lũy đẳng" không giảng (ở L03); kế đó `pitfalls` Lỗi 1 "tính cô lập". Khi làm lab: không biết chạy `.sql` thế nào nếu chỉ xem video.
- **L09**: `quy_mo` step 2, "điểm nghẽn khoá (như bài trước)" — không hiểu "khoá" là gì, bài trước (L08) không có. (Trước đó prereq step 2 nhồi 7 mệnh đề SQL trong một khung, có thể phải tua lại.)
- **L10**: `quy_mo` step 1, "có kỳ vọng bằng 1, bất kể n lớn thế nào" — "kỳ vọng" không giảng, không chứng minh; trước đó `check` step 1 "vét cạn một trăm hai mươi thứ tự… bốn mươi bốn" — không tự đếm được bằng tay.
- **L11**: `prereq` step 2 (slide ⑤⑥⑦: phép dịch bit, từ điển, cắt chuỗi, `"%016X"` trong một khung ~1 phút) rồi `intuition` step 1 "DE 2 (PAN)" — PAN không giảng. Phần còn lại theo được.

### 5. Số đã tính lại / mã đã chạy

(Script: `labC/t_nums.py`, `labC/t_sqlite.py`, `labC/j/*.java`, `labC/cmp_srt.py`, `labC/cmp_show.py`.)

- **L08**: tính lại 11 số (100/10 000/1 000 000 lệnh bù; 20 MB/2 GB/200 GB; 1,2/116/11 574 sự kiện/giây; 12 bộ chuyển tiếp; 2i+1 cho i = 0..3 → 1,3,5,7), khớp 11/11 (kể cả "hai trăm nghìn mê ga byte" = 200 GB thập phân). Mã đã chạy: `Saga.java` (javac + java, JDK 21): 3 dòng khớp từng chữ với màn hình; 2 đoạn SQL Outbox (chốt: `1500000` / `lenh 42 da tru 500000|0`; huỷ: `2000000` / `0`) bằng Python sqlite3 3.49.1 chế độ như `sqlrun.py` — khớp; 2 lần thử autocommit/executescript cho thấy lỗi `COMMIT` (xem MUST). Cảnh "Chạy thật": Saga.java là **mô phỏng** (chuỗi log tự dựng, không gọi dịch vụ), lời đọc nói rõ "Ta mô phỏng SAGA bằng Java"; Outbox chạy thật trên sqlite (tiêu đề ghi "(sqlite)", lời đọc chỉ nói "cơ sở dữ liệu nhỏ"). Không chỗ nào nói đã chạy Kafka/Oracle thật: Kafka chỉ là hộp trong hình. Đối chiếu `audit/bnk/src/l08.py`: mã/kết quả trên màn hình trùng nguyên văn.
- **L09**: tính lại 14 số (505 500; 2 011 000; 300 000/30 000 000/3 000 000 000 dòng; 36 500 000/3,65 tỉ/365 tỉ dòng thu phí; 36,5 giây/3650 giây = 1,01 giờ/365 000 giây = 4,22 ngày), khớp 13/14; lệch duy nhất là lời đọc "bốn ngày rưỡi" (màn hình 4,2). Mã đã chạy: 4 câu SQL "Chạy thật" (`1|0`; 3 dòng số dư; sau đảo 0,0,0 và `6`) và câu `HAVING SUM(amt) <> 0` (`[1]`), khớp. Sqlite thật, có ghi "(sqlite)". Đối chiếu `l09.py`: trùng.
- **L10**: tính lại 9 số (44 hoán vị không điểm cố định trong 120, 44/120 = 36,7% ≈ 37%; kỳ vọng điểm cố định n = 6 bằng vét cạn 720 hoán vị = 1,0; 0/5 và 5/5; quiz 3/5; lab 1/6; 4/499/49 999; 100/10 000/1 000 000), khớp 9/9. Mã đã chạy: `TuongQuan.java` (0/5, 5/5) và `HetGio.java` (2,1,1,1) — khớp; hai tệp là **mô phỏng** logic (tiêu đề cảnh ghi "mô phỏng bằng Java", lời đọc nói "T24 và IBM MQ không chạy trên máy này") nên không gây hiểu nhầm. Không có mã chỉ đọc.
- **L11**: tính lại 20 số (bản đồ 7020000000000000; 3020000000000000; 3020000002000000; độ dài 62, 44, 46; 108 byte; 10,8 KB/s, 1,08 MB/s, 108 MB/s; 933 MB, 93,3 GB, 9,33 TB; nửa nhị phân), khớp 20/20. Mã đã chạy: `IsoDung` (3 dòng: bản đồ, bản tin, 62) và `IsoDoc` (`[2, 3, 4, 11]`, `4111111111111111`) bằng Python 3.13 — khớp từng chữ với màn hình và `l11.py`. Cảnh "Chạy thật" là chạy thật bằng Python (không phải kết nối mạng); không có kết nối NAPAS/HSM nào bị nói là có.
- Tổng: ≈ 54 số tính lại (53 khớp, 1 lệch: L09 "bốn ngày rưỡi"); 9 đoạn mã/SQL chạy lại (9 khớp; 2 đoạn SQL L08 báo lỗi `COMMIT` ở engine autocommit).

### 6. Khung hình đã xem

- **L08** (126 khung, 837 giây): 00000 (0 giây, hook), 00023 (123 giây, hình bù ngược — nhãn "lỗi → quay lui" bị mũi tên cắt ngang), 00053 (288 giây, Saga.java), 00072 (390 giây, kiểm bằng bảng), 00087 (458 giây, quiz), 00099 (539 giây, bảng quy mô), 00107 (597 giây, đề lab), 00124 (827 giây, tổng kết). Lỗi hiển thị: chỉ nhãn bị mũi tên cắt; chữ code không tràn.
- **L09** (133 khung, 842 giây): 00000 (hook), 00036 (173 giây, sổ cái chỉ thêm), 00041 (212 giây, bước 2), 00062 (325 giây, kết quả chạy thật), 00089 (462 giây, đề quiz), 00096 (514 giây, đáp án quiz), 00105 (559 giây, bảng quy mô), 00112 (598 giây, "giải pháp cũ gãy"). Không lỗi hiển thị.
- **L10** (139 khung, 875 giây): 00001 (5 giây), 00027 (134 giây, hình hai hàng đợi — nhãn "tương quan = M7" bị mũi tên cắt), 00039 (198 giây, formula bước 3), 00056 (288 giây, ví dụ ①–⑤), 00069 (350 giây, HetGio.java), 00096 (493 giây, quiz có nút "Dừng video"), 00109 (572 giây, bảng quy mô), 00115 (598 giây, gãy ở đâu). Không đè chữ khác.
- **L11** (147 khung, 961 giây): 00000, 00014 (79 giây, prereq), 00034 (188 giây, MTI→bản đồ), 00039 (210 giây, hình 16 bit đúng 0x70/0x20), 00053 (297 giây, bước 1–3), 00073 (397 giây, mã dựng bản đồ), 00092 (478 giây, lỗi 1), 00109 (574 giây, quiz đáp án 1 — "0𝑥30" nghiêng), 00118 (657 giây, bảng quy mô), 00126 (698 giây, gãy ở đâu), 00143 (945 giây, tổng kết). Không tràn chữ; cỡ chữ SVG DE 4 (18 px) nhỏ nhưng đọc được.

### 7. E51 giáo án ↔ video

- **L08**: (1) đếm dòng/thứ tự bù → `example` ①–④, `check`, quiz Q1–Q2 ✓. (2) vì sao ghi kép mất sự kiện → `formula` step 3, `pitfalls` Lỗi 3, `example` ⑤ ✓ (không có lần chạy "không Outbox", xem SHOULD). (3) Outbox gộp một giao dịch → `intuition` step 2, `chay_that` ✓. (4) điều phối vs phối hợp → quiz Q3 + `quy_mo` step 2 ✓ (định nghĩa ở `sym`). (5) chạy mô phỏng → `chay_that` ✓. (6) số lệnh bù/hộp thư/bộ chuyển tiếp ×100, ×10 000 → `quy_mo` ✓. (7) SQL chốt + huỷ → `practice` + lab ✓. `fix` giáo án ("bước bù phải lũy đẳng") có ở Lỗi 2. Ví dụ giáo án khớp video. Lệch: không.
- **L09**: (1) giao dịch có phí cân đối → `example` ①–③ ✓. (2) số dư = tổng → `formula` bước 2 + hình ✓. (3) bút toán đảo → `formula` bước 3, `example` ④⑤, chạy thật ✓. (4) truy vấn tổng nhóm tìm lệch → `check` ✓. (5) chạy SQL → `chay_that` ✓. (6) dòng sổ cái + thời gian cộng lại ×100, ×10 000 → `quy_mo` ✓ (kèm lệch lời đọc 4,5/4,2). (7) lab ✓. Ví dụ giáo án (500 000, phí 5 500, 6 dòng) khớp. Lệch: không.
- **L10**: (1) ghép theo mã → `intuition`, `example` ③, `chay_that` ✓. (2) xác suất bằng vét cạn → `check` step 1: nêu kết quả 44/120 nhưng phép vét cạn không hiện, không đo (lệch nhỏ). (3) xử lý hết giờ chờ → `formula` b3, `chay_that` HetGio ✓. (4) nhiều bản dịch vụ lấy nhầm → chỉ `pitfalls` Lỗi 3 + một dòng `quy_mo` (phát biểu, không chạy/đo) — đo yếu. (5) chạy mô phỏng ✓. (6) số ghép sai và lệnh hết giờ chờ ×100, ×10 000 → `quy_mo` ✓. (7) lab ✓. Lệch: tiêu đề "OFS" không có nội dung OFS ngoài định nghĩa.
- **L11**: (1) dựng bản đồ bit → `formula`, `example` ①, `chay_that` ✓. (2) độ dài với LLVAR → `example` ②–④ ✓. (3) đọc ngược → `formula` b3, `example` ⑤, `chay_that` ✓. (4) che số thẻ → chỉ `pitfalls` Lỗi 2 + quiz Q3 (quyết định), không có ví dụ che, không đo — lệch nhỏ. (5) chạy dựng/đọc ✓. (6) băng thông/nhật ký ×100, ×10 000 → `quy_mo` ✓. (7) lab 0210 ✓. Ví dụ giáo án (bản đồ 7020000000000000, 62 ký tự) khớp.

### 8. Pháp lý/sản phẩm

(`audit/legal/registry.yaml` không có mục nào cho L08–L11; các dữ kiện sau tự đối chiếu.)

- SAGA không cô lập (không có tính I của ACID), bước bù lũy đẳng, pivot → thử lại, Outbox + bộ chuyển tiếp at-least-once nên người nhận phải khử trùng, chia khoá cho nhiều relay giữ thứ tự theo tài khoản — CONFIRMED (Garcia-Molina & Salem 1987; Richardson, Microservices Patterns).
- sqlite: `COMMIT` khi không có giao dịch → lỗi; Python sqlite3 mở giao dịch ngầm trước INSERT/UPDATE — CONFIRMED (đã chạy 3.49.1). Mã thoát khác 0 của CLI khi có lỗi — PLAUSIBLE.
- VND exponent 0, USD exponent 2 (ISO 4217) — CONFIRMED.
- IBM MQ/JMS: JMSMessageID/JMSCorrelationID; trả lời đặt CorrelationID = MessageID của yêu cầu; thuộc tính Expiry — CONFIRMED (khái niệm chung); OFS = Open Financial Service của Temenos T24 — CONFIRMED; cú pháp OFS/MQ thật không có trong bài (đúng như `source`: chỉ minh hoạ) — PLAUSIBLE rằng người học chưa ghép được với T24 thật.
- ISO 8583:1987: MTI 0200/0210; bit 1 báo bản đồ thứ hai; DE 2 LLVAR tối đa 19; DE 3 mã xử lý 6 chữ số (00 = mua hàng/dịch vụ); DE 4 12 chữ số; DE 11 STAN 6; DE 37 RRN 12; DE 39 mã phản hồi 2 ký tự (00 = chấp nhận) — CONFIRMED. NAPAS có đặc tả riêng (bài nêu đúng "có thể khác"); cách NAPAS mã hoá DE 4 cho VND — không kiểm được (PLAUSIBLE rằng một số kết nối nội địa dùng 2 chữ số lẻ ngầm; bài đã rào "mỗi mạng có đặc tả riêng").
- Che số thẻ 6 đầu + 4 cuối, không ghi PAN nguyên vào nhật ký — CONFIRMED theo PCI DSS (bài không nêu nguồn).
- Không có điều luật Việt Nam được trích trong 4 bài này.

### 9. Nhận xét

- Nội dung cốt lõi 4 bài chuẩn và tự chạy lại được; số tính lại khớp trừ một lời đọc (L09 "bốn ngày rưỡi" vs 4,2); mã "chạy thật" trùng `audit/bnk/src`. Lỗi đáng sửa nhất: lab L08 gắn `COMMIT;` theo hành vi driver Python và giải thích sai nguyên nhân.
- P1 nghiêm: cả 4 bài còn 1–3 từ chưa giảng tại chỗ (lũy đẳng, cô lập, điểm nghẽn khoá, kỳ vọng, PAN, bảng mã ký tự); các bài kéo kiến thức từ L03/L05 mà không trỏ đúng bài (L09 trỏ nhầm "bài trước").
- L10 yếu nhất (tổng 9, GẦN): tiêu đề hứa OFS/IBM MQ nhưng bài chỉ là mô phỏng ghép mã tương quan; "kỳ vọng = 1" và "44 thứ tự" không có cách tự làm tay.
- P8, P9 đạt cả 4 bài (bảng 3 mức quy mô, "giải pháp cũ gãy ở đâu", đánh đổi; lab có đáp án mong đợi tự chấm); lab chạy ĐÚNG 4/4 cả lời giải tự viết lẫn lời giải mẫu.
- Hình: hai hình cơ chế (L08 bù ngược, L10 hai hàng đợi) bị mũi tên cắt nhãn; L11 in "0𝑥30" kiểu nghiêng; L11 dài 16:01 (hơi vượt mục tiêu 16 phút).

## Phụ lục D
#### Phần D — BNK L12, L13, L14 (đọc trọn 3/3 bài)

Ngày đọc: 2026-11-14. Tệp tạm: `...\scratchpad\labD\` (doi_soat.py, luhn_lab.py, sua_sai.sql, verify.py, fr.py, cmp.py).
sha16 lúc đọc: L12 `02c72c0d89ca5104`; L13 `5c594e84d7cccf08`; L14 `f1838cdc47d56c33`.

### 1. Chuẩn xác

| Bài | Mức | Cảnh/step | Trích nguyên chữ | Vì sao sai + bằng chứng đã chạy | Đề xuất sửa | Tin cậy |
|---|---|---|---|---|---|---|
| L12 | SHOULD | `quy_mo` step 2 (show + say) | "ở ×10 000 cần cỡ 100 GB bộ nhớ nên cũng gãy trên một máy" / "nên cũng gãy trên một máy" | Khẳng định tuyệt đối thiếu điều kiện: máy chủ 128 GB–vài TB RAM là thường; 100 GB (= 10^9 mục × 100 byte, tính lại đúng) chỉ "gãy" với cấu hình cụ thể. Bảng quy mô tính đúng (verify.py: 100 s; 11,57 ngày; 316,9 năm; 0,01/1/100 s; 10 MB/1 GB/100 GB), chỉ câu kết luận quá tay. Thêm: dict Python tốn nhiều hơn 100 byte/mục (chuỗi + số + bảng băm). | Đổi thành "ở ×10 000 cần cỡ 100 GB: vượt bộ nhớ của máy thường, phải chia phần hoặc dùng hợp nhất theo thứ tự"; nêu rõ 100 byte/mục là giả định. | PLAUSIBLE |
| L12 | — | còn lại | — | Không có MUST. Đã tính lại mọi số (5+5−4=6; 3+1+1+1; 1500/1650/150; 50+600−500; quiz a1..a4; lab −500) và chạy lại chương trình "Chạy thật": in `3 1 1 1` / `150` khớp màn hình. RRN 12 ký tự, STAN 6 số, MTI 0200/0210: khớp ISO 8583 (CONFIRMED từ kiến thức). | | |
| L13 | MUST (biên) | `chay_that` step 2, và `formula` step 1 | "Khi chạy thật, khối PIN là không bốn một hai hai năm rồi các chữ E, đúng như phép tính tay. Bên nào có khoá và số thẻ thì XOR lại để lấy PIN. Người không có thì chỉ thấy dãy này." / "Vì XOR hai lần trả về ban đầu, bên có khoá và số thẻ khôi phục được PIN." | `041225EEEEEEEEEE` là khối PIN RÕ (mới XOR với PAN, chưa mã hoá bằng khoá nào). Chạy: `041225EEEEEEEEEE` XOR `0000111111111111` = `041234FFFFFFFFFF` → lấy lại PIN 1234 chỉ cần số thẻ, KHÔNG cần khoá. Khoá chỉ cần để giải khối đã MÃ HOÁ (TDES/AES), bước này bài không hiển thị hay tính. Người học dễ hiểu "XOR với số thẻ là che được PIN". PAN lại nằm trong nhật ký/thẻ nên không bí mật. Cảnh `intuition` có nói "mã hoá ngay" nhưng không nối với khối vừa tính. | Thêm một câu/hình: "đây là khối rõ; thiết bị đầu cuối mã hoá tiếp bằng TPK (TDES/AES) rồi mới gửi; khối rõ không được rời thiết bị an toàn"; sửa "bên nào có khoá và số thẻ..." thành "ai giải được khối đã mã hoá và biết số thẻ mới lấy được PIN; khối rõ thì chỉ cần số thẻ". | CONFIRMED (đã chạy) |
| L13 | SHOULD | `formula` step 3 + `hook` bảng (+ say) | "chuyển tiền trực tuyến của cá nhân trên 10 triệu đồng một giao dịch, hoặc khi tổng trong ngày vượt 20 triệu đồng, phải xác thực sinh trắc học (Phụ lục 01). Tổng cộng dồn tính lại từ 0 sau mỗi lần xác thực." | Bản dịch văn bản (english.luatvietnam.vn, Phụ lục 01 nhóm I.3, Ghi chú) cho thấy: (a) ngưỡng 10 triệu/20 triệu thuộc nhóm chuyển tiền cho chủ tài khoản khác và nạp/rút ví, còn thanh toán hàng hoá dịch vụ (nhóm I.2) dùng ngưỡng khác (5 triệu, 100 triệu, 1,5 tỷ); (b) giao dịch loại C/D yêu cầu sinh trắc học KẾT HỢP OTP/Soft OTP/token/chữ ký số (Phụ lục 02), không phải chỉ sinh trắc học; (c) Tksth chỉ cộng giao dịch loại A, B (bản 77/2025: thêm C2) đã phát sinh, về 0 đầu ngày hoặc ngay sau giao dịch dùng hình thức xác nhận loại C (hoặc C/D ở bản gốc), không phải "mỗi lần xác thực" bất kỳ. Ngưỡng và phép cộng của bài (ví dụ ⑤, quiz câu 2: 6+7=13, 13+9=22>20) khớp công thức G + Tksth > 20 triệu. Đã chạy lại 8 ca ngưỡng, khớp. | Thêm "(chuyển tiền giữa hai chủ tài khoản; xác thực gồm sinh trắc học cùng một yếu tố nữa)" và "tổng tính từ đầu ngày, về 0 sau giao dịch đã xác thực loại C/D". | PLAUSIBLE (bản dịch/tóm tắt thứ cấp; chưa mở bản Công báo) |
| L13 | SHOULD | `formula` step 3, say; `hook` bảng | "Bản sửa đổi có hiệu lực từ ngày một tháng ba năm hai nghìn không trăm hai mươi sáu" (show: "hiệu lực 01/03/2026") | TT 50/2024: ký 31/10/2024, hiệu lực 01/01/2025. TT 77/2025: ký 31/12/2025, hiệu lực 01/03/2026 nhưng Điều 3 và Điều 10 áp dụng từ 01/07/2026 với đơn vị phục vụ cá nhân (Điều 12); mà Điều 10 chính là điều THAY Phụ lục 01, 02, 04 (nguồn: luatvietnam.vn trang TT 77/2025). Phụ lục 01 (chứa ngưỡng) bản mới chỉ có hiệu lực từ 01/07/2026; ngưỡng 10/20 triệu của cá nhân vẫn giữ nguyên ở cả hai bản. Màn hình dễ làm người học tưởng quy tắc ngưỡng chỉ bắt đầu từ 01/03/2026. | Ghi "TT 50/2024 hiệu lực từ 01/01/2025; Phụ lục 01 thay bởi TT 77/2025, áp dụng từ 01/07/2026 (cá nhân)". | PLAUSIBLE (nguồn thứ cấp) |
| L13 | SHOULD | trường `source` (tệp YAML) | "Thông tư 50/2024/TT-NHNN về an toàn hệ thống thanh toán, sinh trắc học" ; "PCI DSS v4.0.1 Req. 3.3.1.2 (không lưu PIN / khối PIN sau cấp phép)" | (1) Tên thật của TT 50/2024: quy định về an toàn, bảo mật cho việc cung cấp dịch vụ trực tuyến trong ngành Ngân hàng (nhiều nguồn: english.luatvietnam.vn, thoibaotaichinhvietnam.vn); `audit/legal/registry.yaml` ghi cùng tên sai "an toàn hệ thống thanh toán". (2) PCI DSS v4.x: 3.3.1.1 = track data, 3.3.1.2 = mã xác minh thẻ (CVV), 3.3.1.3 = PIN và khối PIN. Số điều ghi trong `source` lệch một mục. Cả hai chỉ nằm ở metadata, không hiện trên màn hình. | Sửa tên TT 50 trong `source` và registry; PIN = Req. 3.3.1.3. | (1) CONFIRMED; (2) CONFIRMED từ kiến thức (chưa mở lại PDF PCI) |
| L13 | SHOULD | `chay_that` step 1 (mã) | `pin, pan = "1234", "4111111111111111"` rồi `a = "041234FFFFFFFFFF"` | Biến `pin` không dùng; PIN đã đệm gõ cứng nên chương trình không "tính" phần đệm như tiêu đề "Tính khối PIN định dạng 0 từ PIN thử" (chỉ tính phần XOR). Đã chạy: ra đúng `041225EEEEEEEEEE`. Có thể gây hiểu nhầm nhỏ. | `a = ("0%d%s" % (len(pin), pin)).ljust(16, "F")`. | CONFIRMED |
| L14 | MUST (biên: có thể hạ SHOULD nếu coi là hai mô hình sổ) | `check` step 1–2 (bảng + say) so với `chay_that` | "số dòng sau khi đảo: 4 dòng cũ (r7, r7b) + 2 dòng đảo = 6, không dòng nào bị xoá" / say: "Số dòng bằng bốn dòng cũ của r bảy và r bảy b, cộng hai dòng đảo, là sáu dòng" | Cảnh `chay_that` (SQL chạy thật) có bảng `ngan_hang` MỘT dòng mỗi mã: sau khi đảo có 3 dòng (đã chạy: `count(*)` = 3; trước đó r7, r7b = 2 dòng). Cảnh `check` bất ngờ chuyển sang sổ bút toán kép (mỗi giao dịch 2 dòng, thêm tài khoản "nhận", "chờ thanh toán chuyển mạch") không hề hiện sổ 6 dòng lên màn hình; khái niệm "cân đối (tổng 0)" cũng chưa giảng trong bài. Người học thấy 2→3 dòng ở cảnh trước, 4→6 dòng ở cảnh sau, không có cầu nối. Phần `checks` YAML (6 dòng, `bnk_ledger_unbalanced`) đúng, nhưng chỉ nằm trong mã kiểm, không lên màn hình. | Hiện bảng 6 dòng (id, tài khoản, số tiền, tổng 0) trước khi nêu số dòng; hoặc đổi câu thành "3 dòng: r7, r7b, dao-r7b". Thêm một câu giảng "bút toán kép: mỗi giao dịch có hai dòng, tổng 0 = cân đối". | CONFIRMED |
| L14 | SHOULD | `chay_that` step 1 vs `formula` step 2 và bài L12 | `INSERT ... VALUES ('r7','A',-500000), ('r7b','A',-500000)` và `INSERT INTO chuyen_mach VALUES ('r7', 500000)`; step 2: "r7 có ở cả hai sổ và khớp" | Theo định nghĩa L12 ("khớp: cả hai có, tiền bằng"), -500000 ≠ +500000 nên r7 trong dữ liệu SQL sẽ bị chương trình L12 xếp "lệch tiền", chứ không "khớp". Quy ước dấu (ngân hàng ghi âm, chuyển mạch ghi dương) không được nói; ở `formula`/`check` YAML dùng cả hai số dương. | Nói rõ "so theo giá trị tuyệt đối/ngược dấu" hoặc ghi cùng dấu trong dữ liệu mẫu. | CONFIRMED |
| L14 | SHOULD | `chay_that` step 2, `practice` (lab), "Nếu kẹt" | `WHERE ma NOT IN (SELECT ma FROM chuyen_mach)` / "Điều kiện mã thừa là mã không nằm trong sổ chuyển mạch" | `NOT IN` trả RỖNG nếu cột của truy vấn con có một giá trị NULL. Đã chạy sqlite 3.49.1: thêm `(NULL, 1)` vào `chuyen_mach` → truy vấn trả `[]` (mã r7b biến mất), còn `NOT EXISTS` vẫn trả `[('r7b',)]`. Bài dạy `NOT IN` làm phép đối soát cho "người làm nghề" mà không cảnh báo; đúng với dữ liệu sạch của bài. Ngoài ra chạy lại cùng điều kiện sau khi đảo sẽ liệt kê cả `dao-r7b` (đã chạy: `[r7b, dao-r7b]`) và đảo lần hai nếu chạy lặp. | Thêm một câu cảnh báo NULL (hoặc dùng `NOT EXISTS`), và nêu cách loại dòng đã đảo (ví dụ cột `da_dao`). | CONFIRMED |
| L14 | SHOULD | `intuition` step 1 (hình + say) | "chuyển mạch từ chối r7b là trùng, chỉ ghi r7; ngân hàng không tự hoàn ghi nợ r7b" | Lệnh thứ hai mang mã mới r7b nên "trùng" ở chuyển mạch phải dựa vào nội dung, không dựa vào mã: chưa giải thích; thực tế bản thử lại không khoá thường mang mã mới và chuyển mạch nhận tiếp (bài có nói thoáng "nếu chuyển mạch nhận cả hai"). Hơn nữa nhận bản từ chối mà ngân hàng không tự hoàn là một lỗi thứ hai (thiếu xử lý phản hồi từ chối), nhưng 3 biện pháp "sửa 1–3" không nêu "tự hoàn khi bị từ chối". Không sai kiến thức lõi (khoá lũy đẳng, truy vấn trước khi thử lại), nhưng nguyên nhân gốc trình bày chưa đủ. | Thêm một nguyên nhân/biện pháp: "xử lý phản hồi từ chối bằng bút toán đảo tự động có duyệt"; hoặc đơn giản hoá kịch bản. | PLAUSIBLE |

Ghi chú: TT 31/2024/TT-NHNN và TT 64/2024/TT-NHNN KHÔNG được dẫn trong L12, L13, L14 (grep). Registry: 31/2024 = phân loại nợ/trích lập dự phòng; 64/2024 = Open API ngân hàng — không liên quan nội dung sinh trắc học của L13 và không có chỗ dẫn sai. Các mục 50/2024, 77/2025, 25/VBHN-NHNN có trong registry (SUA_DOI/HIEU_LUC); bài ghi chú rõ "sửa đổi bởi 77/2025" ở cả bảng hook lẫn bước 3, nên thoả cổng "cần kiểm lại" ở mức chuỗi chữ; còn thiếu cụm "kiểm lại văn bản hiện hành" mà `fix` của giáo án L13 hứa ("ranh giới ngưỡng theo văn bản hiện hành").

### 2. Độ sâu

Phút: tổng mp4 (ffprobe) = lời đọc + thời gian dừng (quiz 25 s + thực hành 150–180 s). Lời đọc ước = tổng − dừng. SRT khớp tuyệt đối với `say` (cmp.py: 0 câu thiếu, 1993/2234/2041 từ, bằng nhau từng từ).

| Bài | sha16 | Phút (lời đọc/thật) | P1 | P2 | P3 | P4 | P5 | P6 | P7 | Tổng | P8 | P9 | Mất gốc | Cần biết trước | Chỗ thiếu chính |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| L12 | 02c72c0d89ca5104 | 11:39 / 14:34 | 0 | 2 | 2 | 2 | 2 | 1 | 1 | 10 | 2 | 2 | GẦN | hạch toán, ghi nợ (L09); "lõi" (L10); mã băm (JV2/giải thuật); thuật ngữ bản tin ISO 8583 (L11) | P1: "hạch toán" (sym bản tin huỷ; quiz đáp án 3), "ghi nợ" (quiz), "lõi + cổng" (hình `intuition`), "mã băm" (`quy_mo` đánh đổi) đều chưa giảng tại chỗ (4 từ). P6: không có thanh toán bù trừ/phiên/chu kỳ đối soát, không nói tổng tiền có thể triệt tiêu nhau (kiểm bằng tổng không bắt được hai lệch bù nhau), dict che mất mã trùng; "NAPAS 24/7" chỉ nhắc, chi tiết hoãn cho "đặc tả của họ". P7: tên tệp `napas_247` nhưng bài là mô hình chung; `covers` gán mục tiêu 4 cho cảnh `example` trong khi dạy ở `formula` bước 3 và quiz câu 3. |
| L13 | 5c594e84d7cccf08 | 12:56 / 16:21 | 0 | 1 | 2 | 2 | 1 | 1 | 2 | 9 | 2 | 2 | GẦN | sinh trắc học (khái niệm), khoá gốc/khoá phiên, gom lô, xoay vòng khoá (quy_mo, pitfalls); TDES/AES (không được nêu tên); Python hmac/hashlib (có chú giải ngắn) | P1: "sinh trắc học" chưa giảng; "khoá gốc", "khoá phiên", "gom lô" (hộp đánh đổi), "xoay vòng" (lỗi 2), "ngân hàng thanh toán" chỉ nói không có trong hình (≥5 từ). P2: từ khối PIN rõ → "dịch khối PIN từ TPK sang ZPK" nhảy cóc, bước mã hoá không bao giờ hiện bằng số; mã `chay_that` gõ cứng phần đệm. P5: quiz chỉ kiểm sinh trắc học và che thẻ, không có câu nào về khối PIN, MAC, Luhn (3 mục tiêu); dừng 25 s cho 3 câu. P6: sai ngụ ý "chỉ cần khoá + số thẻ" (mục 1), sinh trắc học thiếu yếu tố thứ hai, không nêu khuôn dạng 4/AES. Thời lượng thật 16:21 > mục tiêu 16 phút (gồm dừng 3:25). |
| L14 | f1838cdc47d56c33 | 12:00 / 15:30 | 1 | 1 | 2 | 2 | 2 | 1 | 2 | 11 | 2 | 2 | GẦN | bút toán kép, "cân đối" (L09); lõi ngân hàng (L10); giám sát, nhật ký kiểm toán; CREATE TABLE/INSERT cơ bản (L04) | P1: "lõi ngân hàng" (prereq), "cân đối", sổ nhiều dòng (check), "giám sát/nhật ký kiểm toán" (quy_mo, pitfalls) chưa giảng; 2 từ then chốt chính (cân đối, sổ nhiều dòng). P2: nhảy mô hình sổ ở `check` (xem MUST L14). P6: khoá lũy đẳng chỉ dạy ở mức khái niệm — thiếu ràng buộc UNIQUE lưu khoá, hai yêu cầu đồng thời cùng khoá, cùng khoá khác nội dung, thời hạn lưu khoá; `NOT IN`+NULL. |

Chi tiết điểm 0/1:
- L12 P1=0 (4 từ, đếm ở cột chỗ thiếu); nếu tính "lõi" và "mã băm" là nhãn phụ thì còn 2 từ → 1. P6=1 và P7=1: nêu trên.
- L13 P1=0, P2=1, P5=1, P6=1: xem cột chỗ thiếu.
- L14 P1=1 (cân đối, sổ nhiều dòng, lõi), P2=1 (check), P6=1.
- P8=2 cả ba: có việc cụ thể + kết quả mong đợi (cham.sh); số khác ví dụ (a1..a8; thẻ 5500005555555559; r8/r8b/r8c, 800 000). P9=2 cả ba: ba mức ×1/×100/×10 000, "giải pháp cũ gãy ở đâu", đánh đổi; số tính lại đúng (mục 5).

### 3. Lab

| Bài | tự làm được | thời gian | kẹt ở đâu | mong_doi khớp màn hình | ghi chú |
|---|---|---|---|---|---|
| L12 | CÓ (cham.sh: ĐÚNG; lời giải mẫu `loi_giai.py` cũng ĐÚNG) | ~10 phút | không kẹt: đề cho sẵn hai từ điển, định dạng in chính xác, video đã dạy bốn danh sách lọc | KHỚP: `khop 3 - lech tien 1 - chi ngan hang 2 - chi chuyen mach 2` / `chenh tien: -500` giống màn hình `practice` step 2 | Lời giải tự viết gần như trùng mẫu (dạy 1:1 từ cảnh `chay_that`). Bài tập đủ 3 yếu tố (số khác, kết quả cụ thể). Đề cần thêm: không. Chỉ "đổi tham số" chưa có (ví dụ thêm một mã trùng). |
| L13 | CÓ (cham.sh: ĐÚNG; mẫu ĐÚNG) | ~15 phút | Phần Luhn: video không hiện mã Luhn, chỉ tính tay; đề tả đủ luật (vị trí 1,3,5 từ phải) và cảnh "Nếu kẹt" gợi `enumerate(reversed(so))`, `i % 2 == 1` nên làm được. `enumerate` chưa giảng trước nhưng được giải một dòng ở "Nếu kẹt". Thẻ thử 5500005555555559: Luhn tổng 40 → True; đổi số cuối thành 8 → 39 → False (đã tính). | KHỚP: `True`/`False`/`550000******5559` | Đề không yêu cầu lab cho khối PIN, MAC (2 trong 4 ý của bài) — mục tiêu 1, 2 chỉ có xem, không có việc tự làm. "Hàm che số thẻ" là in trực tiếp, không phải hàm (mục tiêu 7 ghi "hàm che"). |
| L14 | CÓ (cham.sh: ĐÚNG; mẫu ĐÚNG; máy này không có `sqlite3` CLI nên cham.sh tự dùng `labs/sqlrun.py`) | ~12 phút | không kẹt; `INSERT ... SELECT 'dao-' || ma, tk, -tien` nằm sẵn trong video, đề nhắc dùng lại `NOT IN` ở bước 2 | KHỚP: `r8b`/`r8c`/`600000`/`2200000` | `ORDER BY ma` có trong de.md nhưng KHÔNG có trên màn hình `practice` (video chỉ nói "chi tiết ở de.md"). Màn hình chỉ nhắc cham.sh, không nhắc cách chạy SQL khi thiếu sqlite3 (cham.sh xử lý tự động). Quiz câu 3 (STAR) không có đáp án mong đợi (chủ đích). |

### 4. Người học kẹt ở đâu

- L12: nhẹ, ở `sym` 02:08–02:42 "bản tin huỷ (reversal): bản tin đảo một giao dịch đã hạch toán" và hình `intuition` "Ngân hàng gửi — lõi + cổng": "hạch toán", "lõi" chưa giảng (người đã học L09/L10 không kẹt); còn lại theo được.
- L13: ở cảnh `intuition` step 1 (02:48–03:57) "HSM chặng giữa dịch TPK/ZPK → ZPK" và "PIN rõ không ra khỏi HSM": "dịch" (giải mã bằng khoá chặng trước, mã hoá lại bằng khoá chặng sau) chưa từng được tính hay minh hoạ bằng số; kế đến ở `chay_that` (06:23) "Người không có thì chỉ thấy dãy này" dễ hiểu sai khối rõ là đã được che.
- L14: ở `check` step 1–2 (06:53–07:36) "4 dòng cũ (r7, r7b) + 2 dòng đảo = 6" — sau khi ở `chay_that` bảng chỉ có 2 rồi 3 dòng; "cân đối (tổng 0)" chưa giảng.

### 5. Số đã tính lại / mã đã chạy

- L12: số tính lại 31, khớp 31 (6=5+5−4; 3+1+1+1; 1500, 1650, 150; 50+600−500; quiz 1/1/1/1 và 4; lab 3/1/2/2/−500 và 8 mã khác nhau; quy mô 3 mức: so từng cặp 100 s / 1,0×10^6 s = 11,57 ngày / 10^10 s = 316,9 năm; bảng tra 0,01/1/100 s; bộ nhớ 10 MB/1 GB/100 GB = 100 000 MB). Mã đã chạy 2 (chương trình `chay_that`, lab `doi_soat.py`), cả hai khớp màn hình/mong_doi. Mã chỉ đọc: không. Cảnh "chạy thật": THẬT (Python thuần, đối chiếu `audit/bnk/src/l12.py` có cùng mã và đầu ra `3 1 1 1`/`150`). Mô phỏng NAPAS: không có; bài ghi rõ "số minh hoạ" và "mô hình chung", không để hiểu nhầm đã kết nối NAPAS.
- L13: số tính lại 34, khớp 34 (PAN đệm `0000111111111111`; 04, 12, 25 (0x34^0x11), EE (0xFF^0x11) ×5; khối `041225EEEEEEEEEE` dài 16; 0111^0101=0010; Luhn 8+14+8=30 chia hết 10; 5500005555555559 tổng 40; đổi số cuối 8 → 39; mặt nạ `411111******1111` và `550000******5559`; HMAC-SHA256 khoá `k`: `7625fd27947ee367` (amt=500000), `7958d294fb89b6dc` (amt=900000), so sánh False; ngưỡng sinh trắc học 8 ca (15 triệu/0 cần; 5/0 không; 8,8,8 → ca 3 cần; 12/0 cần; 6,7,9 → ca 3 cần; 22>20); HSM 100→200→1, 10 000→20 000→20, 1 000 000→2 000 000→2 000). Mã đã chạy 3 (khối PIN, mặt nạ+MAC, lab `luhn_lab.py`) khớp. Thử nghiệm thêm: khối rõ XOR PAN đệm lấy lại `041234FFFFFFFFFF` (xem MUST L13). Mã chỉ đọc: không (hmac/hashlib có sẵn). Cảnh "chạy thật": THẬT cho Python; HSM và MAC chuẩn thẻ KHÔNG chạy — bài ghi rõ "minh hoạ, chuẩn thẻ dùng thuật toán MAC riêng" và "thông lượng HSM là số minh hoạ"; riêng khối PIN rõ không ghi là khối chưa mã hoá.
- L14: số tính lại 24, khớp 24 (2×500 000; 2 000 000−1 000 000=1 000 000; 1 500 000−1 000 000=500 000; 1 000 000+500 000=1 500 000; −500 000−500 000+500 000; quiz (3−1)×400 000=800 000 và 3−2=1; lab 3 000 000−2 400 000=600 000 và 2 200 000; quy mô: 10/1 000/100 000 vụ, 100 phút/166,7 giờ/16 666,7 giờ, 0,208/20,83/2 083 người). Mã đã chạy 3 (4 câu SQL `chay_that` trên sqlite 3.49.1 ra `r7b`/`1000000`/`1500000` khớp; lab `sua_sai.sql`; thử NULL và đếm dòng). Cảnh "chạy thật": THẬT trên sqlite (ghi rõ "(sqlite)" ở tiêu đề); Oracle/T24 không liên quan.

### 6. Khung hình đã xem (≥ 5/bài)

- L12 (tổng 873,6 s): `00032.png` (170 s, hình đường đi), `00037.png` (200 s, hai sổ), `00063.png` (345 s, mã chạy thật), `00094.png` (480 s, quiz), `00112.png` (580 s, bảng quy mô), `00127.png` (700 s, đề tự làm). Lỗi hiển thị: không có chữ tràn/đè/cắt; nội dung chỉ chiếm nửa trên khung (nửa dưới trống ở cả 6 khung); hình đường đi không gắn nhãn 0200/0210 trên từng mũi tên (chú giải ở bên phải), nhưng khớp lời đọc.
- L13 (981,4 s): `00034.png` (175 s), `00040.png` (215 s), `00048.png` (255 s), `00071.png` (390 s), `00076.png` (420 s), `00077.png` (425 s), `00086.png` (470 s), `00116.png` (650 s). Lỗi: không tràn/đè; nửa dưới khung trống; chữ chú giải TPK/ZPK/ZMK/LMK nhỏ nhưng đọc được; lời đọc nêu "ngân hàng thanh toán" không có ô trong hình; khung 00076 hiện phụ đề "Người không có thì chỉ thấy dãy này." cùng khối rõ (xem MUST).
- L14 (930,0 s): `00037.png` (180 s), `00040.png` (200 s, cùng hình dòng thời gian), `00045.png` (220 s), `00081.png` (400 s), `00118.png` (620 s). Lỗi: không tràn/đè; tiêu đề cảnh ở `00045` vẫn là "dòng thời gian của sự cố giả định" nhưng hình là bảng nguyên nhân–biện pháp (nhãn tiêu đề lệch nhẹ); nửa dưới khung trống.

### 7. E51 giáo án ↔ video

- L12: (1) đường đi và chỗ mất dấu → `intuition` step 1 ✓; (2) phân loại bốn loại → `formula` bước 2 + `example` ✓; (3) kiểm bằng đếm bù trừ và tổng tiền → `prereq` ③, `formula` bước 1–2, `check` ✓ (khớp `covers`); (4) hành động đầu tiên cho từng loại lệch → dạy ở `formula` bước 3 (khớp: xong; chỉ một bên: tra soát; lệch tiền: điều tra) và quiz câu 3 (chỉ "chỉ ngân hàng có"); `covers` ghi `example` là sai cảnh; chưa có câu đo cho "lệch tiền"/"chỉ chuyển mạch"; (5) chạy chương trình → `chay_that` ✓; (6) thời gian và bộ nhớ ×100, ×10 000 → `quy_mo` ✓; (7) viết chương trình → `practice` + lab ✓. Ví dụ giáo án (3/1/1/1, 6 mã khác nhau) khớp video. `fix` ✓ (pitfall 1 và 3).
- L13: (1) khối PIN định dạng 0 → `example` ①–④ ✓ nhưng không tới khối đã mã hoá; (2) vì sao sửa bản tin làm MAC không khớp → `formula` bước 2 + `check` bảng ✓ ("bên nhận tính lại MAC" nằm ở lời đọc `check`); (3) quy tắc sinh trắc học + cộng dồn → `formula` bước 3, `example` ⑤, quiz ✓ (xem SHOULD pháp lý); (4) che số thẻ và không ghi PIN vào nhật ký → `check` (b), `pitfalls` 1, quiz câu 3 (`covers` ghi `check` — chỉ nửa đầu); (5) chạy chương trình → `chay_that` ✓; (6) số HSM ×100, ×10 000 → `quy_mo` ✓; (7) hàm Luhn và hàm che số thẻ → `practice` (lab chỉ Luhn là hàm; che thẻ là lệnh in). Ví dụ giáo án (041225EEEEEEEEEE, MAC đổi, Luhn thẻ thử) khớp video. `fix` về "ranh giới ngưỡng theo văn bản hiện hành" mới đạt ở mức ghi "sửa đổi bởi 77/2025".
- L14: (1) triệu chứng → nguyên nhân, bằng chứng, sửa, ngăn → `formula` bước 1–4 + `intuition` ✓; (2) số tiền trừ dư và đối soát → `example` ①–③ ✓; (3) bút toán đảo → `example` ④ + `chay_that` ✓; (4) kể sự cố thật theo STAR → dạy ở `sym`, đo ở quiz câu 3 và `pitfalls` (`covers` chỉ `pitfalls`); không chấm được (có chủ ý); (5) chạy SQL → `chay_that` ✓; (6) quy mô ×100, ×10 000 → `quy_mo` ✓; (7) viết SQL → `practice` ✓. Ví dụ giáo án (trừ dư 500 000, 1 mã chỉ ngân hàng, đảo) khớp.

### 8. Pháp lý/sản phẩm

Pháp lý (L13), đối chiếu `audit/legal/registry.yaml` + nguồn web (thứ cấp, không mở được Công báo):
- TT 50/2024/TT-NHNN: có trong registry (SUA_DOI, đọc "CITED LF2"). Ký 31/10/2024, hiệu lực 01/01/2025 (english.luatvietnam.vn; thoibaotaichinhvietnam.vn). Tên trong registry/`source` ("an toàn hệ thống thanh toán, sinh trắc học") KHÔNG khớp tên thật (an toàn, bảo mật cho việc cung cấp dịch vụ trực tuyến trong ngành Ngân hàng): CONFIRMED lệch. Phụ lục 01 chứa ngưỡng: CONFIRMED (bản dịch).
- TT 77/2025/TT-NHNN sửa TT 50/2024: CONFIRMED (nhiều nguồn). Ký 31/12/2025, hiệu lực 01/03/2026; Điều 3 và 10 áp dụng từ 01/07/2026 (phục vụ cá nhân) và 01/10/2026 (chỉ tổ chức); Điều 10 thay Phụ lục 01, 02, 04: PLAUSIBLE (luatvietnam.vn, một nguồn). Registry ghi "basis SECONDARY, chưa mở bản gốc" khớp tình trạng này.
- Ngưỡng cá nhân "trên 10 triệu/giao dịch" và "tổng ngày vượt 20 triệu" (G ≤ 10 triệu; G + Tksth ≤ 20 triệu) có ở cả bản gốc lẫn Phụ lục 01 thay thế, nhóm I.3: CONFIRMED (bản dịch) / PLAUSIBLE (chưa đối chiếu nguyên văn). Ngưỡng 50 triệu/100 triệu là của khách hàng tổ chức (từ 01/07/2026): bài không nhắc, đúng phạm vi "của cá nhân".
- "Tổng cộng dồn tính lại từ 0 sau mỗi lần xác thực": gần đúng; đúng ra: 0 đầu ngày hoặc ngay sau giao dịch xác nhận loại C (bản gốc: C hoặc D): PLAUSIBLE.
- QĐ 2345/QĐ-NHNN (nguồn gốc lịch sử của ngưỡng 10/20 triệu, hiệu lực 01/07/2024): bài không nhắc; registry CHUA_KIEM; không ảnh hưởng.
- TT 31/2024 (phân loại nợ) và TT 64/2024 (Open API): không xuất hiện trong L12–L14.
- PCI DSS: Req. 3.4.1 (che PAN khi hiển thị, tối đa BIN và 4 số cuối): CONFIRMED từ kiến thức; PIN/khối PIN không lưu sau cấp phép là 3.3.1.3 (bài ghi 3.3.1.2): CONFIRMED từ kiến thức.

Sản phẩm/giao thức:
- Khối PIN ISO 9564 định dạng 0 (0 | độ dài | PIN | F, PAN đệm 0000 + 12 số phải nhất trừ số kiểm; XOR): CONFIRMED (đã chạy, khớp). Giải thích TPK/ZPK/ZMK/LMK theo Thales payShield: CONFIRMED (khớp hành vi chung). Khối rõ so với khối mã hoá: SAI NGỤ Ý (xem MUST).
- Luhn (ISO/IEC 7812-1), mặt nạ 6+4: CONFIRMED.
- MAC tổng quát: bài ghi rõ HMAC-SHA256 chỉ là minh hoạ, chuẩn thẻ dùng MAC riêng (ISO 9797-1/X9.19 hoặc CMAC): CONFIRMED.
- ISO 8583 MTI 0200/0210, RRN 12 ký tự (DE37), STAN 6 số (DE11): CONFIRMED. Khoá ghép duy nhất RRN+STAN+ngày giờ truyền+mã ngân hàng: PLAUSIBLE (theo đặc tả từng mạng, bài đã rào).
- Khoá lũy đẳng phải sinh ở màn hình xác nhận và dùng lại khi bấm lại: CONFIRMED; thiếu lưu khoá với UNIQUE/đồng thời: xem P6.
- SQL: `NOT IN` với NULL: đã chạy, CONFIRMED; sqlite `INSERT ... SELECT` từ chính bảng đó: chạy đúng (3 dòng).

### 9. Nhận xét

- Cả ba bài tự tính số đúng 100% (L12 31/31, L13 34/34, L14 24/24), mã "chạy thật" đều thật, đầu ra khớp màn hình và `mong_doi`; SRT trùng `say` từng từ.
- Lỗi lớn nhất là ngụ ý sai ở L13 (`chay_that` bước 2): khối PIN rõ mà nói cần khoá mới lấy được PIN, cộng với bước mã hoá và "dịch khoá" không bao giờ được tính bằng số; rồi L14 `check` nhảy từ sổ 1 dòng/mã sang sổ bút toán kép 2 dòng/mã (6 dòng) không cầu nối.
- Pháp lý L13: ngưỡng 10/20 triệu cá nhân đúng; chỗ lệch là ngày (Phụ lục 01 bản mới áp dụng từ 01/07/2026, TT 50 từ 01/01/2025), thiếu yếu tố xác thực thứ hai (OTP/token) của loại C/D, tên và số điều PCI trong metadata sai (3.3.1.2 → 3.3.1.3; tên TT 50 trong `source` và registry).
- P1 yếu cả ba bài (L12 0, L13 0, L14 1) vì từ nghiệp vụ dùng lại từ L09/L10 (hạch toán, ghi nợ, lõi, cân đối) và từ mới ở hộp đánh đổi (khoá gốc, khoá phiên, gom lô, mã băm) không giảng tại chỗ; P8 = 2 và P9 = 2 cả ba (lab 3/3 tự làm được, cham.sh ĐÚNG ở cả lời giải tự viết lẫn mẫu).
- L13 là bài dài nhất: 16:21 thật (12:56 lời đọc + 3:25 dừng), vượt mục tiêu 16 phút 21 giây; L12 14:34, L14 15:30.
