# Mẫu H — đọc độc lập 40 bài (đợt AF5, 2026-11-22, hạt giống `20261122`)

Chọn mẫu: `sample_h.py` → `sample_h.json` (loại 214 bài đã vào Mẫu C–G). Chuẩn chấm: `BRIEF.md`. Báo cáo gốc của 4 người đọc (chỉ đọc, không được xem báo cáo cũ): `part_1.md` … `part_4.md`. Tổng hợp bằng máy: `tally.py` → `tally.out`. Người điều phối tự kiểm lại 14 phát hiện trọng yếu bằng `audit/review/audit_final/logs/af5/verify_h_claims.py`: 14/14 đúng như báo (13 khớp chuỗi tự động, 1 — LNX L03 — khớp bằng grep tay).

## 1. Kết quả (từ `tally.out`)

| Nhóm | Bài | Có MUST | Wilson 95% | MUST | SHOULD | Mất gốc ĐỦ / GẦN / CHƯA |
|---|---|---|---|---|---|---|
| Lớp A — bài soạn tay chặng 1–5 (FND, JVA, JV2, PYT, BNK, BNX, INT, ACB, DMS, CS112) | 14 | 2 (14%) | 4,0–39,9% | 4 | 46 | 14 / 0 / 0 |
| Lớp B+C — 4 khoá mới + bài nâng AF2 hàng loạt | 26 | 24 (92%) | 75,9–97,9% | 58 | 115 | 13 / 4 / 9 |
| — trong đó tầng NEW (CPR, LNX, MLP, PRJ) | 12 | 12 (100%) | 75,7–100% | 33 | 66 | 0 / 3 / 9 |
| — trong đó tầng MASS (13 khoá chặng 6–11) | 13 | 11 (85%) | 57,8–95,7% | 22 | 45 | 12 / 1 / 0 |
| Toàn mẫu | 40 | 26 (65%) | 49,5–77,9% | 62 | 161 | 27 / 4 / 9 |

Bài có MUST: AIF L10, BNK L08, CLC L05, CLD L15, CPR L04, CPR L06, CPR L08, CS115 L43, CSA L00, DBS L01, JVA L04, LLM L10, LNX L03, LNX L05, LNX L06, MLP L04, MLP L08, MLP L12, NET L11, OSY L02, PLC L03, PRJ L04, PRJ L05, PRJ L07, RLN L13, TOC L10.
Bài không MUST: ACB L03, BNK L12, BNX L09, BNX L26, BNX L28, BNX L36, CS112 L08, DMS L18, FND L10, GFX L11, INT L08, JV2 L09, PYT L04, ROB L05.

Điều đáng tin nhất của mẫu: **không tìm thấy `mong_doi.txt` nào sai** (40/40 lời giải lab chạy lại hoặc dò tay đều khớp), và ở lớp A mọi đầu ra mã chạy lại đều khớp. Lỗi nằm ở tầng sư phạm và ở phần được máy chèn thêm.

## 2. Năm lỗi hệ thống (mỗi lỗi lặp ở nhiều bài; số lan toàn kho đo bằng `mech_scan.py`, `verify_h_claims.py`)

1. **Cảnh "Tự làm" khuôn mẫu không phải bài tự làm.** Video chỉ ghi "mở `de.md`" rồi chiếu đáp án (581/777 bài; bản đầu ghi 542 vì script đo sót 39 bài của CPR, LNX, MLP, PRJ — đính chính 2026-11-22T20:35Z); 375 bài còn chiếu nguyên lời giải sau 30 giây dừng; 209 đề lab chép sẵn mọi dòng đáp án; `labs/cham.sh` chỉ so đầu ra nên vài lệnh in là "ĐÚNG". Nhiều lab trùng số liệu ví dụ trong bài, hoặc không luyện mục tiêu chính (PLC L03 không dựng cây, GFX L11 một phép nhân).
2. **Lab đòi ngôn ngữ/công cụ chưa dạy.** CSA L00 đòi C khi khoá chưa có dòng C nào; DBS L01 đòi SQL trước bài SQL (L02); OSY/CLC/GFX/PLC/CLD đòi Python trong khoá không dạy Python; LNX L05 đòi `socket` Python. `labs/ENV.md` và `check_env.sh` không nhắc `gcc` (17 lab C) và Node (16 lab WEB).
3. **`covers` gán theo vị trí, không theo nội dung.** Sai ở 14/40 bài mẫu; toàn kho 158 bài có đúng dãy `example > check > practice`, 183 bài có mục tiêu trỏ vào cảnh "mở de.md" (cảnh không dạy gì). Kèm theo là mục tiêu không được dạy (LNX L03, LNX L06, MLP L04, MLP L12, PRJ L05, PRJ L07, AIF L10, BNK L08).
4. **Lời/bảng chèn thêm để qua cổng gây sai.** Recap độn 65–129 giây trên màn hình tĩnh (AIF L10, LLM L10, PLC L03, CS115 L43, CLC L05); ghi chú "Hai mức quy mô" (380 tệp) có số sai/không nguồn (AIF 10^150, PLC "độ sâu", TOC O(t²), CLD "hàng chục nghìn tổ chức"); bảng "viết trong mã" dán chung có dòng sai với mã (215 tệp dòng `round`, 60 tệp dòng `math`); câu rỗng ở MLP; điểm trừ "(-30đ)" không có thang (25 tệp MLP + PRJ); `checks` vô nghĩa "1 + 1 == 2" (15 tệp).
5. **Bốn khoá mới CPR, LNX, MLP, PRJ quá mỏng.** 45/45 bài dài 5,3–6,5 phút, 905–1 175 từ (chuẩn 9–16 phút, 1 300–2 300 từ); mã 8–13 dòng chỉ được nói trong 2–4 câu; điều tên bài hứa không được chạy (LNX L05 gọi từ ngoài container, MLP L12 đo độ trễ, LNX L06 khoá SSH); PRJ tuyên bố "chấm tự động 100 điểm" không tồn tại.

## 3. Đối chứng tích cực
Lớp A đạt chuẩn "Tự làm" thật: đề hiện trên video, số liệu khác ví dụ, có bước "Nếu kẹt", phải chạy mới ra đáp án (BNX L09, L26, L28, L36; BNK L08, L12; JV2 L09; JVA L04; ACB L03; DMS L18; CS112 L08; PYT L04; FND L10; INT L08). Hai bài lớp A có MUST: BNK L08 (lời đếm dòng nhật ký lệch màn hình; mục tiêu "chọn điều phối hay phối hợp khi tải tăng" không được dạy; `covers` mục tiêu 2 lệch cảnh) và JVA L04 (một dòng `covers` lệch).

## 4. Giới hạn của mẫu
- Không nghe âm thanh, không xem tệp mp4 (chỉ khung hình và phụ đề); 179 khung đã mở, không thấy chữ tràn/đè.
- Chưa chạy Docker/Maven/Kafka/ksqlDB thật; mốc phiên bản sản phẩm và văn bản pháp lý chỉ đối chiếu với nguồn trong kho.
- 40 bài trên 777: khoảng Wilson rộng; với lớp A cận trên vẫn là 40%, nên chưa thể nói "không lỗi" cho 182 bài lớp A chưa vào mẫu.
- Các dòng PLAUSIBLE trong báo cáo gốc chưa được kiểm bằng nguồn ngoài.
