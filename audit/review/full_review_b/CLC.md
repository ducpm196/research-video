# CLC — đã đọc 13/13 bài

Đọc toàn bộ `show`, `say`, `checks`, chữ trong hình SVG, quiz và đáp án của từng bài (2026-11-08). Khoá không có mẫu `audit/clc/src/*.tpl.yaml` → không chạy `sync_tpl_from_lesson.py`. Tổng: 6 bài đã sửa, 1 mục MUST, 9 mục SHOULD.

| Bài | Kết luận | Mục đã sửa (cảnh: MUST/SHOULD — lý do ngắn) | Nguồn | lint / render |
|---|---|---|---|---|
| L00 | đã sửa | Lỗi 1: SHOULD — “Phần lớn sự cố dữ liệu trên đám mây đến từ cấu hình của khách” là con số thực tế không nguồn → “Rất nhiều sự cố …” (màn hình + lời đọc) | NIST SP 800-145 (5 đặc tính, kiểm lại đúng); không có nguồn số liệu cho “phần lớn” | lint: 0 FAIL, 0 WARN, 14 PASS · render: 55 khung (0 vấn đề) |
| L01 | không phát hiện lỗi | — (99,9975%, 13,1 phút, 4,6 giờ ≈ 21 lần, 99,9899% đều đúng) | — | — |
| L02 | đã sửa | sym + recap: SHOULD — “mạng con nằm trong **một** vùng sẵn sàng” nói như quy luật chung; đúng với nhà cung cấp trong ví dụ, sai với nhà cung cấp có mạng con theo vùng → “ở nhà cung cấp trong ví dụ …; có nhà cung cấp cho mạng con trải cả vùng” | AWS VPC docs “Subnets for your VPC” (“Each subnet must reside entirely within one Availability Zone”); Google Cloud VPC docs “Subnets are regional resources” (truy cập 2026-11-08, no revision given) | lint: 0 FAIL, 0 WARN, 17 PASS · render: 59 khung (0 vấn đề) |
| L03 | đã sửa | Lỗi 1: SHOULD — “nguyên nhân rò rỉ hàng đầu” là xếp hạng không nguồn → “một kiểu rò rỉ rất hay gặp” (bài + `curriculum/clc.yaml` L03 `fix`). Lỗi 3: SHOULD — “Tài khoản gốc vượt qua mọi chính sách” tuyệt đối (chính sách cấp tổ chức vẫn giới hạn được gốc của tài khoản thành viên) → “Chính sách quyền thông thường không giới hạn được tài khoản gốc” | AWS IAM User Guide “Root user” và AWS Organizations “Service control policies” (SCP áp lên root user của tài khoản thành viên) (truy cập 2026-11-08, no revision given) | lint: 0 FAIL, 0 WARN, 14 PASS · render: 52 khung (0 vấn đề) |
| L04 | đã sửa | sym: SHOULD — “ổ khối gắn vào **một** máy ảo” tuyệt đối (có ổ gắn nhiều máy) → “thường gắn vào một máy ảo”. Lỗi 2: SHOULD — “thêm một dòng vào tệp nhật ký 1 GB là phải ghi lại cả 1 GB” không đúng mọi kho (có loại đối tượng cho ghi nối) → “Với đối tượng thông thường, …”; xoá 1 mục `asr_reviewed` cũ | Amazon EBS docs “Multi-Attach”; Azure Blob docs “Append blobs” (truy cập 2026-11-08, no revision given) | lint: 0 FAIL, 0 WARN, 15 PASS · render: 51 khung (0 vấn đề) |
| L05 | không phát hiện lỗi | — (hoà vốn 5000 h = 57,1%, 5500 h = 62,8%; 876/264/1000 đô la đúng) | — | — |
| L06 | không phát hiện lỗi | — (100 000 GB-giây → 1,87; hoà vốn ≈ 19,6 triệu lần; 93,33 đô la) | — | — |
| L07 | không phát hiện lỗi | — (RPO 5 phút/24 giờ/1 phút/6 giờ; 2500 s, 2000 s đúng; khôi phục về 15:06 khả thi vì nhật ký sau đó vẫn được đẩy) | ISO/IEC 27031:2011 | — |
| L08 | không phát hiện lỗi | — (4608, 737,28 đô la; 0,03 → 0,025; +10% mỗi đơn) | — | — |
| L09 | không phát hiện lỗi | — (320 000 byte; 3 125 000 lần; 1,6 MB) | NIST SP 800-57 Pt 1 Rev 5 | — |
| L10 | không phát hiện lỗi | — (1/(n − f): 100%, 50%, 33%; tổng ×2, ×1,5, ×1,33; bốn chiến lược khớp whitepaper) | AWS whitepaper Disaster Recovery of Workloads on AWS (2021) | — |
| L11 | đã sửa | hook + intuition + example: MUST — ví dụ tự mâu thuẫn: hook và hình nói 3 máy là 3 vai (ứng dụng, cơ sở dữ liệu, xử lý ảnh) = 438 đô la, nhưng bước 2–4 coi 438 là “3 máy ứng dụng” rồi so với riêng tầng ứng dụng sau (1 máy nền + 2 máy cao điểm = 216,4) để ra “tiết kiệm 50,6%” → hook “riêng phần ứng dụng là ba máy ảo … 438, chưa kể máy cơ sở dữ liệu và máy xử lý ảnh”; hình “trước: mọi máy chạy suốt”, ô “3 máy ứng dụng”; lời đọc hình nêu đủ năm máy; bước 4 “tiết kiệm trên tiền máy ứng dụng”; tách câu hook dài (lint) | tính lại: 3·730·0,20 = 438; 730·0,20 + 2·176·0,20 = 216,4; 1 − 216,4/438 ≈ 50,6% (`verify_clc.py` L11 PASS) | lint: 0 FAIL, 0 WARN, 15 PASS · render: 60 khung (0 vấn đề) |
| L12 | đã sửa | stage2 lời đọc: SHOULD — “Phần lớn, nhưng chưa phải tất cả” — nguồn chỉ ghi “refactor parts of the service”, màn hình không có → “Nhưng chưa phải tất cả”. stage3: SHOULD — “chia hệ con chỉ mục thành ô ngay / làm ngay” trong khi nguồn ghi đã lên kế hoạch chia tiếp và “reprioritizing that work to begin immediately” → “bắt đầu ngay việc chia tiếp”. stage4: SHOULD — “trước 2020 kho chỉ nhất quán cuối cùng”, “14 năm chỉ nhất quán cuối cùng” nói quá (ghi đối tượng mới đã có đọc sau ghi trước 2020; chưa tải lại được bản tài liệu cũ) → “chưa bảo đảm nhất quán mạnh cho mọi thao tác; Amazon gọi đó là nhất quán cuối cùng”; tách câu dài (lint). Đã ghi bổ sung vào `audit/clc/sources_L12.md` | [S17] aws.amazon.com/message/41926 (WebFetch 2026-11-08: “debugging an issue causing the S3 billing system …”, “had planned further partitioning of the index subsystem later this year … begin immediately”); [W20], [B20] | lint: 0 FAIL, 0 WARN, 36 PASS · render: 133 khung (0 vấn đề) |

## Giáo án L11: con số chưa có bản ghi kiểm (VER) — cho người điều phối
`curriculum/clc.yaml` L11 `example`: “ứng dụng **3** thành phần: cơ sở dữ liệu chuyển sang dịch vụ được quản lý, máy chủ ứng dụng chuyển nguyên sang máy ảo trước, tác vụ xử lý ảnh viết lại thành hàm theo sự kiện”.
- Khớp bài: bảng bước 1 của cảnh `example` và hình `intuition` có đúng 3 thành phần (cơ sở dữ liệu → chuyển có chỉnh; máy chủ ứng dụng → chuyển nguyên rồi co giãn; xử lý ảnh → viết lại thành hàm). Cách tính: đếm `len(["cơ sở dữ liệu", "máy chủ ứng dụng", "xử lý ảnh"]) == 3`.
- Gợi ý bản ghi (kèm số chính của bài, đã có ở `verify_clc.py` L11): `rec("CLC:L11", len(["cơ sở dữ liệu", "máy chủ ứng dụng", "xử lý ảnh"]) == 3 and round(3 * 730 * 0.20) == 438 and round(730 * 0.20 + 2 * 8 * 22 * 0.20, 1) == 216.4 and round((1 - 216.4 / 438) * 100, 1) == 50.6, "3 thành phần; tầng ứng dụng 438 → 216,4 đô la (−50,6%)")`. Tôi không sửa `verify_plan_curricula.py` (theo brief).

## Không sửa và vì sao
- L06, L08: đơn giá (0,0000166667 đô la/GB-giây, 0,20 đô la/triệu lần; 0,09 đô la/GB truyền ra, tính phẳng không bậc) mang tính thời điểm, nhưng bài đã ghi “số minh hoạ”, không trình bày như giá hiện hành.
- L09: bài mô tả xoay khoá chính = mã hoá lại mọi khoá dữ liệu (320 000 byte). Có dịch vụ quản lý khoá xoay tự động bằng cách giữ vật liệu khoá cũ, không bọc lại khoá dữ liệu; mô hình của bài vẫn đúng như cận trên khi muốn bỏ hẳn khoá cũ, nên giữ.
- L05 hook: “đặt trước rẻ hơn tới 40%” là lời “ai đó đọc” trong tình huống; số của bài (500 so với 876 đô la ≈ 43%) nhất quán, không phải khẳng định về giá thật.
- L10 hook: sự cố cả vùng không nêu tên, nêu ở mức “hiếm, nhưng đã xảy ra” — không kiểm theo sự kiện cụ thể, không có năm/số để sai.
- L01: “vùng sẵn sàng cách nhau đủ xa … độ trễ vài mi li giây”, “cách nhau vài chục km” — mô tả định tính khớp tài liệu nhà cung cấp, giữ.

## Kết quả cuối
- `audit/clc/verify_clc.py`: `verify_clc: 13/13 PASS`
- `tools/lv.py curriculum curriculum/clc.yaml`: `curriculum: 13 bài, 13 đã có đặc tả, 0 lỗi`
- `audit/review/scan_ctrl.py`: 8 lượt, tất cả ở `lessons/jva` (khoá khác), 0 ở CLC.
- `audit/review/prune_stale_asr.py lessons/clc/*.yaml`: xoá 1 mục ở L04, các bài khác 0.
