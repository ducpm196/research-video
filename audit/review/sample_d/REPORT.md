# Đọc mẫu độc lập đợt D — 42 bài sau đọc kiểm lần ba (2026-11-10)

**Mục đích**: đo lỗi còn sót **sau** đợt C (đọc kiểm lần ba 656/656 bài, 591 bài dựng lại), để cập nhật BN-0039 bằng số đo thay vì ước đoán.

**Cách rút mẫu**: mỗi khoá một bài, bỏ các bài đã có trong mẫu C (`sample_c/REPORT.md`, 42 bài), `random.Random(20261110).choice(...)` theo thứ tự tên thư mục `lessons/`; chạy 2026-11-10T02:51:55Z.

**Người đọc**: 4 tác tử AI mới, chỉ đọc, không mở `audit/review/full_review_c/*` (báo cáo của người đã sửa). Tiêu chí: `FULL_REVIEW_BRIEF_C.md` mục A (MUST/SHOULD) và B (bài tự đứng được). Mỗi tác tử tự tính lại bằng Python mọi con số hiện trên màn hình hoặc đọc ra. Chi tiết từng phát hiện (trích nguyên chữ, bằng chứng, mức tin cậy) và cách đã sửa: `part_1.md` … `part_4.md`.

**Người điều phối kiểm lại**: hai MUST trên tệp thật (SDP L05 chạy mã bằng Python; CS115 L21 đọc cảnh `metrics`); xem tận nơi các sửa nội dung có tính sự kiện (ROB L03 đỉnh 3,60; ESY L08 byte cuối không xác nhận theo UM10204 §3.1.6; GFX L06 “ba thành phần ánh sáng”; SWF L12 chỉ ở mức khái niệm phòng thủ; ACB L05 không khẳng định ACB dùng T24).

## Kết quả

| Phần | Bài | MUST | SHOULD | Bài không có phát hiện |
|---|---|---:|---:|---|
| 1 | ACB L05, AGT L11, AIF L02, BCH L10, BNK L14, CAS L08, CLC L12, CLD L10, CS112 L12, CS115 L21, CSA L05 | 1 (CS115 L21) | 13 | BNK L14, CAS L08 |
| 2 | CVI L09, DAN L06, DBS L07, DEN L13, DMS L10, DSC L09, DSY L08, DVO L06, ESY L08, EVT L03, GFX L06 | 0 | 18 | — |
| 3 | HCI L12, INT L04, IRS L08, JVA L12, LLM L06, MLO L14, NET L12, OSY L03, PAR L03, PLC L09 | 0 | 15 | IRS L08, OSY L03 |
| 4 | RBM L16, RLN L09, ROB L03, SAR L02, SDP L05, SEC L03, SEP L05, SWF L12, TOC L01, WEB L01 | 1 (SDP L05) | 10 | SEP L05 |
| **Tổng** | 42 | **2** | **56** | 5 |

Hai MUST (CONFIRMED):
- **SDP L05** — khối mã trên màn hình không chạy được: `class QuyTac:      def ap(...)` trên một dòng là lỗi cú pháp, và lớp không có `__init__` nên `Thue(0.1)` không có `self.ti_le`, trong khi bài nói kết quả 220 000. Sửa: mã nhiều dòng, `__init__` ở lớp gốc; chạy thử ra 220000 và 209000; lời đọc giải thích lớp gốc nhận tỉ lệ và lớp con thừa hưởng.
- **CS115 L21** — tiêu đề cảnh “Bốn chỉ số: mỗi cái là một xác suất có điều kiện” và mục tiêu “đọc chúng như xác suất có điều kiện” sai: tỉ lệ đúng là xác suất không điều kiện, F1 không phải xác suất. Sửa: “hai trong đó là xác suất có điều kiện”; mục tiêu nêu đúng độ chuẩn xác, độ phủ.

SHOULD: 56 mục (55 dòng bảng) ở 37 bài. 36/55 dòng (đếm theo từ khoá “định nghĩa/giải nghĩa/giải thích/nhắc lại/giảng lại”) là **thuật ngữ hoặc ký hiệu dùng trước khi giảng lại tại chỗ** (luật B.4, ví dụ “chỉ mục”, “lũy đẳng”, “ngăn xếp”, “bit”, O/Ω/Θ, γ và V(s)). Các mục còn lại là màn hình lệch lời đọc (GFX L06, INT L04, PAR L03, DAN L06), thiếu điều kiện (ESY L08 byte cuối, CLD L10 Little “luôn đúng”, PLC L09 phép gán với C/C++, DEN L13 hậu tố cho phép nối, SWF L12), nhãn hình sai (ROB L03 đỉnh 3,99 → 3,60), số không nguồn (SAR L02, ACB L05). **Không có con số tính sai**: mọi số hiện ra đều được tính lại và khớp.

## Tỉ lệ (khoảng Wilson 95%, tính bằng Python)
- Bài có ít nhất một MUST: **2/42 = 4,8%** (1,3–15,8%), ước tính khoảng 9–104 trong 656 bài. Mẫu C trước đợt C: 5/42 = 11,9% (5,2–25,0%). Hai khoảng chồng nhau, nên **chưa** khẳng định được mức giảm có ý nghĩa thống kê; điểm ước lượng giảm khoảng một nửa.
- Bài có ít nhất một phát hiện: **37/42 = 88,1%** (75,0–94,8%). Mẫu C chỉ có 16/42, nhưng hai số **không so được trực tiếp**: mẫu D đọc theo tiêu chí B (định nghĩa lại mọi khái niệm mượn tại chỗ), chặt hơn mẫu C.

## Xử lý
- 2 MUST do người điều phối sửa; 56 SHOULD do chính 4 tác tử sửa sau khi đo xong (kiểm lại từng mục trên tệp, không mục nào bị bác). 37 bài đổi lời/hình (SDP L05 + 36 bài) → dựng lại tuần tự, log `audit/review/rebuild_d.out`.
- Quy trình giữ nguyên: JVA L12 sửa qua `audit/jva/src/l12.py` + `gen.py`; mẫu `.tpl` của RBM L16, TOC L01, CLD L10, CSA L05, NET L12 đồng bộ bằng `sync_tpl_from_lesson.py --write`; lint 0 FAIL/0 WARN mọi bài; bộ kiểm khoá liên quan 0 FAIL; `verify_plan_curricula` 545 PASS; `check_xref` 0.
- RLN L09 dựng lần đầu FAIL (cảnh `prereq` mới tràn bảng) → tách thành hai bước có `clear: true`, render 0 vấn đề.

## Kết luận
Lỗi MUST còn sót đã giảm (ước lượng điểm 11,9% → 4,8%) nhưng **chưa bằng 0**. Phần lớn còn lại là SHOULD về định nghĩa thuật ngữ tại chỗ, nghĩa là ở khoảng 9/10 bài người học có thể gặp ít nhất một từ chưa được giảng lại. Lời khuyên: một đợt đọc kiểm D tập trung riêng vào “định nghĩa tại chỗ” trên 614 bài ngoài hai mẫu (BN-0039).
