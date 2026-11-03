# L00 — Bức tranh lớn: AI học như thế nào — 2026-10-24

Lý do làm bài: người dùng phát hiện giáo án có L00 nhưng không có bài. Đã kiểm lúc 11:11Z (OBSERVED): `curriculum/cs115.yaml` có `L00` nhưng không có `spec`, thư mục `lessons/` không có file L00, `out/` không có L00. Lệnh `curriculum` khi đó vẫn báo 0 lỗi. Cách chặn tái phát xem `audit/CURRICULUM_RENUMBER.md` §5.
Nhãn: OBSERVED = chạy trong phiên này; INFERRED = suy luận, chưa kiểm.

## 1. Thiết kế

- **Vị trí**: bài đầu tiên, trước mọi bài khác. Bài chỉ dùng số học phổ thông (cộng, trừ, nhân, bình phương, số thập phân) và chỉ giới thiệu 2 ký hiệu mới: `·` và `ŷ`. Bài không dùng vector in đậm, chỉ số dưới hay hàm f(x), vì các ký hiệu này được dạy ở bài 1 và bài 5.
- **Nguồn**: tex dòng 105–119 (sơ đồ tư duy 4 bước).
- **Sửa A7**: tex dòng 116 viết sai số “giảm dần về 0”. Bài này chỉ ra bằng số rằng điều đó không đúng khi có nhiều dữ liệu. Với hai nhà A (6, 2, 4; giá 20) và B (5, 1, 2; giá 17), không có w nào đoán đúng cả hai: nhà A cần w = 10/3, nhà B cần w = 17/5. Sai số tổng nhỏ nhất là 4/61 ≈ 0,066, đạt tại w = 205/61 ≈ 3,36. Mọi con số này được tính lại bằng sympy trong `checks`.
- **Luật 17**: nhắc bài sau chỉ ở hook, `in_ai_map` và recap (3 step `forward_ref: true`), luôn kèm giải thích bằng lời thường. Bảng bản đồ khoá học đã được đối chiếu với `title` của từng bài trong lộ trình. Bản nháp đầu ghi sai bài 11 (“xác suất”, thực ra là hàm mũ & logarit) và bài 15 (thực ra là nén dữ liệu, thuộc bước biểu diễn); cả hai đã được sửa.
- **Cùng ví dụ với L01**: ngôi nhà 6, 2, 4 (diện tích tính theo chục m²). Hai bài nối tiếp nhau mà không phải đổi ví dụ.

## 2. Kết quả (OBSERVED)

| Hạng mục | Kết quả | checked_at |
|---|---|---|
| lint | 0 FAIL, 0 WARN, 32 PASS; 25 phép kiểm sympy; 12 scene; 1740 từ | 12:43Z |
| build + verify | `out/L00/L00.mp4` 646,4 s (10,8 phút), 123 khung, verify PASS; `L00.srt`, `chapters.txt` (12 chương) | 12:30Z, 12:43Z |
| render | 0 vấn đề. Lần render đầu tràn bảng ở 5 khung (scene learn) → đã thêm `clear: true` | 11:17:12Z |
| ASR | 123 câu, độ khớp TB 0,980, **gắn cờ 0, chưa xem xét 0** | 12:32:01Z |

ASR trước khi sửa (12:28Z) gắn cờ 3 câu. Cả 3 đã được viết lại, không dùng `asr_reviewed`:
- “rộng 60 mét vuông” → nghe thành “động … m vung”. Đổi thành “có diện tích”.
- “lặp lại … hàng nghìn lần” → nghe thành “lập … nhiên”. Đổi thành “làm đi làm lại … rất nhiều lần”.
- Câu 3 từ “Đến lượt bạn.” → “bản”. Ghép vào câu sau.

TTS: lượt đầu 7/122 câu bị dịch vụ trả `NoAudioReceived`. Lệnh báo BLOCKED và không treo; lượt sau đọc nốt, 0 lỗi.

**Xem bằng mắt** (đọc ảnh PNG): khung 10 (hook), 19 (ôn nền), 37 (ký hiệu ŷ), 45 (công thức dự đoán; tại đây phát hiện lỗi dấu “số”), 67 (bảng tự sửa), 75 và 81 (hai nhà), 91 (bản đồ khoá học sau khi sửa), 103 (lỗi thường gặp), 112 (đáp án), 123 (khung cuối). Không còn chữ đè, tràn bảng hay ký hiệu chưa được giải thích.

## 3. Phát âm “logarit” (nút thắt B20, OPEN)

Probe `scratchpad/log_probe.py`: 3 cách viết × 4 ngữ cảnh × small + medium, có đối chứng âm “lô-ga-ních”. Chấm lại theo dạng bỏ dấu (`log_rescore.py`):

| Cách viết | Nghe ra “logarit” |
|---|---|
| logarit | 3/8 |
| lô-ga-rít | 1/8 |
| lô-ga-rit | 4/8 |
| đối chứng âm “lô-ga-ních” | 0/8 (8/8 nghe ra “logani…”) |

Không cách nào đạt ngưỡng 7/8, nên không thêm luật lexicon. L00 bỏ từ này khỏi lời đọc và giữ trên màn hình. Câu đọc vẫn đúng vì vẫn nói tới hàm mũ và xác suất. Nút thắt được ghi vào `fix` của L11.

## 4. Còn mở (NOT_VERIFIED)

- Chưa có người nghe thật. Phát âm mới được ghi là **ASR-checked**, chưa phải “đã nghe”.
- Hiệu quả sư phạm với người mới: chưa đo.
- Mô hình chỉ có 1 trọng số (giữ cố định 2 và 1) là cách đơn giản hoá có chủ đích, và bài đã nói rõ điều này với người học.
