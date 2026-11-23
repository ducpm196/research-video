# Sổ tác tử Mẫu H (AF5) — mở 2026-11-22T15:26Z

Giới hạn: 4 tác tử chỉ đọc cùng lúc, mỗi tác tử 10 bài. Chuẩn: `BRIEF.md`. Danh sách: `sample_h.json` (hạt giống 20261122, loại 214 bài Mẫu C–G).
Tác tử bị ngắt vì hạn mức: tiếp tục bằng SendMessage tới đúng tên, không mở tác tử mới. Báo cáo cuối của tác tử được người điều phối chép vào `part_<N>.md`.

| Phần | Tên tác tử | Bài | Trạng thái |
|---|---|---|---|
| 1 | sample-h-p1 | CPR L08, LNX L05, MLP L12, BNX L09, BNK L12, JV2 L09, DMS L18, CLC L05, GFX L11, PLC L03 | XONG 15:43Z; báo cáo ở `part_N.md` |
| 2 | sample-h-p2 | CPR L04, LNX L03, PRJ L07, BNX L28, BNK L08, PYT L04, CS112 L08, CLD L15, LLM L10, RLN L13 | XONG 15:43Z; báo cáo ở `part_N.md` |
| 3 | sample-h-p3 | CPR L06, MLP L08, PRJ L04, BNX L36, FND L10, INT L08, CS115 L43, CSA L00, NET L11, ROB L05 | XONG 15:43Z; báo cáo ở `part_N.md` |
| 4 | sample-h-p4 | LNX L06, MLP L04, PRJ L05, BNX L26, JVA L04, ACB L03, AIF L10, DBS L01, OSY L02, TOC L10 | XONG 15:43Z; báo cáo ở `part_N.md` |

Ghi chú 15:46Z: nhật ký tác vụ của phần 2–4 rỗng (0 byte) sau khi trả báo cáo; ba tác tử đó được tiếp tục bằng SendMessage để tự ghi nguyên văn báo cáo vào `part_2.md`, `part_3.md`, `part_4.md` (ngoại lệ duy nhất của luật chỉ đọc). Phần 1 trích từ nhật ký. Tổng hợp: `tally.py` → `tally.out`, `REPORT.md`.
