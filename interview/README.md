# CHƯƠNG TRÌNH LUYỆN PHỎNG VẤN SENIOR INTEGRATION ENGINEER — NGÂN HÀNG ACB

> **Đối tượng**: người mới bắt đầu hoặc mất gốc, đến kỹ sư backend chuẩn bị phỏng vấn vị trí tích hợp ngân hàng.
> **Mục tiêu**: hiểu chắc các chủ đề trong JD ACB (`resources/job/JD.md`) và trong CV của ứng viên, trả lời được khi bị hỏi sâu, và đề xuất mức **50,000,000 VND gross/tháng** có căn cứ. Thu nhập năm nếu đạt mức này: **700 – 850 triệu VND** = 50 triệu × (13 tháng cố định + 1–4 tháng thưởng tùy xếp loại, theo tin tuyển dụng ACB). Không tài liệu nào ở đây bảo đảm kết quả phỏng vấn hay mức lương.
> **Mục lục và số đo video (nguồn duy nhất)**: [`MASTER_CURRICULUM_INDEX.md`](file:///D:/research-video/interview/MASTER_CURRICULUM_INDEX.md).
> **Bản đồ toàn bộ thư viện video (`out/`)**: [`SOURCE_CODE_VIDEO_MAP.md`](file:///D:/research-video/interview/SOURCE_CODE_VIDEO_MAP.md).
> **Trạng thái, bằng chứng kiểm chứng và việc còn mở**: [`HANDOVER_INTERVIEW.md`](file:///D:/research-video/interview/HANDOVER_INTERVIEW.md) Mục 7–10.

---

## 1. XEM VIDEO CÓ ĐỦ KHÔNG?

**Không, nếu chỉ xem 9 video ACB (khoảng 50 phút).** Video ACB và INT là bản tóm tắt cho người đã có nền. Người **chưa từng lập trình** học khóa **JVA** (13 bài, `out/JVA/`, mọi chương trình trong bài đã được biên dịch và chạy thật) trước, rồi khóa **BNK** (15 bài, `out/BNK/`), tự làm phần "Đến lượt bạn" ra giấy, rồi mới sang INT/ACB và ngân hàng 100 câu hỏi.

Những điều *chưa có nguồn* đã bị gỡ khỏi tài liệu (rà soát 2026-11-08): thành phần hội đồng phỏng vấn ACB, quy tắc "dưới X năm BHXH thì hạ lương", và việc ACB dùng Temenos T24 (JD không nêu hệ thống lõi của ACB).

## 2. THỨ TỰ HỌC ĐỀ XUẤT

| Bước | Học gì | Ở đâu | Cách tự kiểm |
|:---:|:---|:---|:---|
| 0 | Khóa **JVA** L00 → L12: chương trình đầu tiên, biến và kiểu, toán tử, rẽ nhánh, vòng lặp, mảng, hàm, lớp và đối tượng, chuỗi, danh sách và bản đồ, ngoại lệ, giao diện/bản ghi/kiểu liệt kê, sổ chuyển khoản nhỏ | [`out/JVA/`](file:///D:/research-video/out/JVA/) | Cài JDK 21+, gõ lại và chạy từng chương trình; làm phần "Bây giờ tới phần bạn tự làm" trước khi xem đáp án |
| 1 | Khóa **BNK** L00 → L14: Java/GC, đa luồng, Spring, REST và khoá lũy đẳng, SQL/chỉ mục, PL/SQL và ORA-00060, Redis, Kafka, SAGA/Outbox, sổ cái, T24/OFS/IBM MQ, ISO 8583, đối soát, khối PIN/HSM/QĐ 2345, tình huống giả định | [`out/BNK/`](file:///D:/research-video/out/BNK/) | Làm câu "Đến lượt bạn"; trả lời các câu hỏi ghi ở `HANDOVER_INTERVIEW.md` Mục 4D mà không nhìn đáp án |
| 2 | Nền còn hổng (chỉ khi cần): DBS, OSY, NET, DSY, EVT, CLD, SEC | [`out/`](file:///D:/research-video/out/) theo `MASTER_CURRICULUM_INDEX.md` Mục 1–3 | Câu hỏi cuối mỗi bài |
| 3 | Khóa **INT** L00 → L07 cùng giáo án `00_…md` → `07_…md` | [`interview/video/`](file:///D:/research-video/interview/video/) | Đọc giáo án sau khi xem video |
| 4 | Khóa **ACB** L00 → L08 | [`interview/video/`](file:///D:/research-video/interview/video/) `L00.mp4`… | Giải thích lại mỗi bài trong 2 phút |
| 5 | Ngân hàng 100 câu | [`06_interview_qa_bank_100.md`](file:///D:/research-video/interview/06_interview_qa_bank_100.md) | Tự trả lời trước, rồi so; câu nào vướng thì ghi lại |
| 6 | Chuẩn bị phần cá nhân: sự cố thật (Câu 93), lương hiện tại thật, bằng chứng dự án AI, xin phép người tham chiếu | [`07_salary_negotiation_50m_gross.md`](file:///D:/research-video/interview/07_salary_negotiation_50m_gross.md), `HANDOVER_INTERVIEW.md` Mục 7.4 | Tập nói to theo khung STAR |

## 3. QUY TẮC TRUNG THỰC KHI DÙNG TÀI LIỆU NÀY

1. Số liệu trong bài giảng là **ví dụ minh họa** hoặc **mục tiêu thiết kế** trừ khi ghi nguồn. Không nói chúng là kết quả của mình.
2. Tách rõ việc **mình trực tiếp làm** (luồng Squad Lending: thấu chi cầm cố sổ tiết kiệm, thấu chi lương, Cloud CA + QĐ 2345, CIC B2B, khóa Redis chống giải ngân kép, trích nợ từng phần, xử lý ORA-00060) với việc **phối hợp** (adapter T24/IBM MQ, cổng NAPAS và HSM của đội Switch, cụm Kafka của đội Nền tảng Dữ liệu). Xem `HANDOVER_INTERVIEW.md` Mục 2.3.
3. Bằng Cử nhân AI UIT: **dự kiến tốt nghiệp 11/2026**; không nói "đã tốt nghiệp".
4. Dự án Isolation Forest/ONNX là **dự án học thuật UIT**, không phải hệ thống production.
5. Không nói thay người tham chiếu; chỉ nêu đúng quan hệ.
6. Lương hiện tại: nói số thật (hoặc lịch sự từ chối nêu), không khai sai; mốc thời gian công tác phải khớp hợp đồng và sổ BHXH.

## 4. TỆP TRONG THƯ MỤC NÀY

| Tệp | Nội dung |
|:---|:---|
| `00_overview_roadmap.md` | Khung năng lực 5 tầng và thứ tự học |
| `01_foundation_cs_java.md` | Nền CS, Java 17/21, JVM, đa luồng, luồng ảo |
| `02_backend_microservices.md` | Spring Boot 3, REST (RFC 9457), Redis, container |
| `03_distributed_systems_senior.md` | SAGA, Outbox, Kafka, khóa phân tán, Oracle 19c |
| `04_banking_domain_t24_napas.md` | T24/OFS/IBM MQ, NAPAS 247/ISO 8583, HSM, tín dụng, đối soát |
| `05_uit_ai_banking_multiplier.md` | Cách trình bày bằng AI UIT trung thực |
| `06_interview_qa_bank_100.md` | 100 câu hỏi và đáp án |
| `07_salary_negotiation_50m_gross.md` | Kịch bản đàm phán, những điều không được khẳng định |
| `video/` | 8 video INT (hai tên trùng byte: `0x_*.mp4` và `INT_L0x.mp4`) và 9 video ACB (`L00.mp4`…`L08.mp4`), kèm `.srt` và chapters |
