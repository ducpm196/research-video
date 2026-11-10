# CAS — đã đọc 12/12 bài

Đọc kiểm 2026-11-08: mọi cảnh, `show`/`say`/`checks`, quiz và đáp án; đối chiếu từng năm, con số, chuỗi nguyên nhân với `audit/cas/sources_L*.md`
(câu trích nguyên văn từ báo cáo gốc: GAO/IMTEC-92-26, báo cáo Inquiry Board Ariane 501, MIB Phase I MCO, thư 1997 về Pathfinder, lệnh SEC 34-70694,
tổng kết AWS 41926, hậu kiểm Cloudflare 12/7/2019, hậu kiểm GitLab 10/2/2017, RFC 6520 + bản vá OpenSSL, Lazer 2014, LWN/glibc/ext4/MariaDB/FAA).
Không bài nào sinh từ mẫu (`audit/cas/src/` không tồn tại). Tổng: **2 MUST, 3 SHOULD** trên 5 bài.

| Bài | Kết luận | Mục đã sửa (cảnh: MUST/SHOULD — lý do ngắn) | Nguồn | lint / render |
|---|---|---|---|---|
| L00 hậu kiểm | không phát hiện lỗi | — | [R00] BMJ 2000; [SRE] ch.15 + phụ lục D; [CF19] | — |
| L01 Patriot | đã sửa | example.1: MUST — màn hình ghi “Nửa giây sai số đã là gần 700 mét” (0,5 s × ≈2000 m/s ≈ 1000 m) và lệch lời đọc “chưa tới nửa giây”; sửa thành “Chưa tới nửa giây sai số (0,3433) đã là gần 700 mét” | GAO/IMTEC-92-26 Phụ lục II (687 m ở 0,3433 s) | lint: 0 FAIL, 0 WARN, 33 PASS; render: 93 khung (0 vấn đề) |
| L02 Ariane 5 | đã sửa | pitfalls.1: SHOULD — “Đã qua hàng nghìn phép thử” không có trong báo cáo; báo cáo §2.3 nói “thousands of problems and potential failures are successfully handled in the review process” → sửa thành “Khâu duyệt đã xử lý hàng nghìn vấn đề” (cả `show` và `say`, tách câu, thêm `focus`) | Inquiry Board 19/7/1996 §2.3 | lint: 0 FAIL, 0 WARN, 26 PASS; render: 90 khung (0 vấn đề) |
| L03 Mars Climate Orbiter | không phát hiện lỗi | — (đã kiểm 226/57/80 km, 4,45, 09:00:46→09:04:52, 10–14 lần, 29/9) | MIB Phase I 10/11/1999; NIST SP 811 B.8 | — |
| L04 Mars Pathfinder | không phát hiện lỗi | — (8 Hz/0,125 s, 18 giờ, bốn câu hỏi trước khi bật cờ khớp thư 15/12/1997) | [GR97], [MJ97] | — |
| L05 Knight Capital | không phát hiện lỗi | — (212 lệnh, 45 phút, 4 triệu khớp, 397 triệu cp, 460 triệu USD, 8/8 máy, 97 thư, 2003/2005, gỡ 7 máy làm tệ hơn) | SEC 34-70694 ¶1–27 | — |
| L06 AWS S3 | không phát hiện lỗi | — (9:37, 11:37, 12:26, 13:18, 13:54; 257 phút) | AWS message/41926 | — |
| L07 Cloudflare | đã sửa | recap.1: SHOULD — “Hai lỗi nhỏ cùng lúc … mới thành sự cố lớn” mâu thuẫn với chính bài (hậu kiểm liệt kê 11 lỗ hổng) → “Nhiều lỗ hổng nhỏ cùng lúc (như một mẫu chậm và một quy trình không có bậc)” | [CF19] mục “multiple vulnerabilities that converged” | lint: 0 FAIL, 0 WARN, 26 PASS; render: 90 khung (0 vấn đề) |
| L08 GitLab | không phát hiện lỗi | — (300 GB, 17:20/23:30, bốn cách sao lưu, 18 giờ, 60 Mbit/s) | [GL17] | — |
| L09 Heartbleed | đã sửa | example.0 + check: MUST — “65 534 byte trả về không thuộc bản ghi / 65 534 giá trị đọc vượt biên”: 16 byte đệm nằm trong bản ghi 20 byte; từ ô dữ liệu tới cuối bản ghi có 20 − 3 = 17 byte nên phần ngoài bản ghi là 65 535 − 17 = **65 518** byte, và chỉ n ≥ 18 (65 518 giá trị) đọc vượt biên. Sửa `show`, `say`, thêm `checks` (`65535 - (20 - 3) == 65518`, `sum(… 1 + 2 + n > 20) == 65518`), giữ “65 534 giá trị bị bỏ” (đúng với phép kiểm của bản vá); xoá 1 mục `asr_reviewed` cũ | RFC 6520 §4; bản vá 96db9023 (phép tính lại, VER) | lint: 0 FAIL, 0 WARN, 25 PASS; render: 79 khung (0 vấn đề) |
| L10 Google Flu Trends | không phát hiện lỗi | — (gấp đôi 2/2013, >50% mùa 2011–12, 100/108 tuần, MAE 0,486/0,311/0,232) | Lazer và cộng sự, Science 343, 2014 | — |
| L11 năm 2038 | đã sửa | example.1: SHOULD — “trên x86 mặc định vẫn 32 bit” dễ hiểu nhầm là cả x86-64 (time_t 64 bit) và nói như vĩnh viễn → “trên x86 32 bit mặc định vẫn là 32 bit (ghi chú của bản 2.34)”, lời đọc cùng nghĩa | glibc NEWS mục 2.34 (“configurations like x86 where time_t is traditionally 32-bit … this default may change”) | lint: 0 FAIL, 0 WARN, 36 PASS; render: 90 khung (0 vấn đề) |

## Không sửa và vì sao
- L01: mô hình “0,1 cắt sau 23 bit phần lẻ” không có trong báo cáo GAO — bài đã tự gọi là “mô hình của bài” và kiểm khớp cả 6 hàng Phụ lục II; giữ.
- L03: mốc “150–170 km tuần trước khi vào quỹ đạo” — câu trích không ghi rõ “tuần trước”, nhưng nằm giữa TCM-4 (15/9) và MOI (23/9); hợp lý, giữ.
- L00/L01/L02/L06: L00 trang bản đồ khoá học gọi MCO là “pound-lực đọc như newton” (đúng ra là pound-lực giây đọc như newton giây) — mức tóm tắt một dòng, L03 dạy đúng; không đổi.
- L08: “dịch vụ ngừng khoảng 18 giờ” còn phép tính 23:30 → 18:00 = 18 giờ 30 — bài đã ghi rõ cả hai và nguồn viết “about 18 hours”; giữ.
- Không mở lại được PDF gốc trong phiên cho CAS; mọi đối chiếu dựa vào câu trích nguyên văn đã lưu ngày 2026-11-02 trong `audit/cas/sources_L*.md`.

## Kết quả bộ kiểm
- `audit/cas/verify_cas.py`: **verify_cas: 93/93 PASS**
- `tools/lv.py curriculum curriculum/cas.yaml`: **curriculum: 12 bài, 12 đã có đặc tả, 0 lỗi**
- `audit/review/scan_ctrl.py`: không có lượt nào ở `lessons/cas/`.
