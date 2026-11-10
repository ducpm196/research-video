# knowledge-graph_LS1_20261110T1420Z: đồ thị chứng cứ của đợt LS1 (chuẩn bị hai lộ trình để bắt đầu học)

Chỉ ghi nút OBSERVED hoặc CITED; máy chạy trong phiên 2026-11-10 → 11-11 (giờ UTC).
Môi trường:
- Windows 11; `.venv` Python 3.13.5; JDK 22.0.2; ffmpeg/ffprobe (chocolatey); Playwright (msedge).
- TTS edge-tts, giọng vi-VN-NamMinhNeural.

| ID | Khẳng định | Phương pháp (lệnh đã chạy) | Quan sát | validity | checked_at |
|---|---|---|---|---|---|
| LS-01 | Lộ trình P có 45 bài (JVA 13 → BNK 15 → INT 8 → ACB 9). Lộ trình N có 74 bài (DMS 21 → CS112 30 → CS115 23), thứ tự thoả mọi tiên quyết | `pack.py list` (Kahn trên requires/requires_ext, kiểm từng cạnh) | `P: 45 bài`, `N: 74 bài`; DMS L19 xếp sau CS115 L13 (tiên quyết) | VALID | 2026-11-10T14:2xZ |
| LS-02 | 9 người đọc độc lập đọc trọn 119 bài | báo cáo từng tác tử (dòng `ĐÃ ĐỌC K/K`) | 13+15+8+9+21+15+15+12+11 = 119 | VALID (CITED: báo cáo tác tử) | 2026-11-10 |
| LS-03 | Phát hiện: 17 MUST, cùng SHOULD / BLOCK; mọi MUST đã sửa | `findings_LS1.md`; người điều phối kiểm diff MUST (CS112 L07, ACB L00/L06/L08, INT L03/L04, BNK L04) | MUST: CS115 1, JVA 3, BNK 2, INT 6 (gồm nhóm nợ), ACB 4, CS112 1 | VALID | 2026-11-10 |
| LS-04 | Nhóm nợ 2 theo TT 31/2024/TT-NHNN là quá hạn 10–90 ngày, nhóm 3 là 91–180 | WebFetch cafef.vn (đăng 2026-07-21), hethongphapluat.com | "từ khoảng 10 ngày đến dưới 91 ngày"; "quá hạn đến 90 ngày", nhóm 3 "91–180", nhóm 4 "181–360", nhóm 5 "trên 360" | VALID (CITED, nguồn thứ cấp, no revision given; nguyên văn Điều 10 chưa đọc được: thuvienphapluat trả 403) | 2026-11-10 |
| LS-05 | 97 bài đổi đều đã dựng lại | `rebuild_ls1.sh a/b/c` → `rebuild.done` | queue 97 = done 97 (`comm -3` rỗng); 98 dòng `verify … → PASS`, 0 dòng khác | VALID | 2026-11-10T17:53:44Z |
| LS-06 | Máy nghe: 0 câu gắn cờ chưa xem xét ở 97 bài | `asr_pending.py`, sau `asr_review_dms.py` (nhóm + 6 lý do viết tay trích bản chép) và chạy lại `lv.py asr` | `# 97 bài đã dựng; bài còn câu chưa xem xét: 0` | VALID | 2026-11-10T18:0xZ |
| LS-07 | 119 bài: tệp đầy đủ, video giải mã trọn, khớp đặc tả, bản duyệt nhanh mới | `pack.py check --decode` → `logs/check_decode_final.out` | `# 119 bài · có vấn đề 0 · tổng 1136.7 phút · giải mã trọn 119` | VALID | 2026-11-10T18:2xZ |
| LS-08 | Bộ kiểm khoá và kiểm nhất quán sạch | `logs/verify_final.out` | verify_jva 110/110; verify_bnk 21/21; verify_cs112 FAIL 0; verify_cs112_p2 37/0; verify_plan_curricula 545/0; check_xref 0; check_meta 0; scan_ctrl 8 (JVA cố ý); check_course_refs 0; sync_tpl CS112/DMS/CS115 0 lệch | VALID | 2026-11-10T18:23:00Z |
| LS-09 | Toàn kho sạch sau mọi sửa | `audit_all.py` → `logs/audit_all_final.out` | `audit_all: 656 bài, 656 đã dựng, 0 bài có vấn đề` | VALID | 2026-11-10T18:46Z |
| LS-10 | Video phỏng vấn trùng byte với bản dựng | `interview_sync_video.py`, rồi `--check` | `92 pairs, 92 identical, 0 mismatched`; tổng 365,61 phút | VALID | 2026-11-10T18:3xZ |
| LS-11 | Trang học không có liên kết chết; chạy được trên máy tính và điện thoại | `pack.py page`; Playwright `shot.py` | 119 bài, HOC_TAP.html 357 liên kết chết 0, xem.html 710 chết 0; scrollWidth bằng viewport (1280, 390); dấu đã học giữ sau tải lại; bấm mục lục nhảy đúng mốc | VALID | 2026-11-10 |
| LS-12 | Đề xuất cổng J25 (cân ngoặc / lệnh in) không đưa vào cổng | `brace_scan.py`, `print_scan.py` (scratchpad) | 20 đoạn lệch ngoặc đều là trích dần có chủ đích; 11 step thiếu lệnh in: 8 lỗi biên dịch/ngoại lệ, 3 đã xét chấp nhận | VALID | 2026-11-10 |

## Điểm nghẽn hợp đồng (từ plan_LS1)
- LB-1 CLOSED (LS-01).
- LB-2 CLOSED (LS-07).
- LB-3 CLOSED (LS-02).
- LB-4 CLOSED (LS-03, LS-04).
- LB-5 CLOSED (LS-05, LS-06, LS-08, LS-09, LS-10).
- LB-6 CLOSED (LS-11).

## Còn mở, không chặn DONE của phạm vi đã cam kết (ghi rõ thay vì gọi là đã kiểm)
- **OB-1**: QĐ 2345/QĐ-NHNN ở BNK L13. Điều kiện "khách hàng cá nhân" và việc nội dung QĐ 2345 có thể nay nằm ở TT 50/2024/TT-NHNN đều NOT_VERIFIED. Bài giữ nguyên câu cũ.
- **OB-2**: TT 31/2024 mới kiểm qua hai nguồn thứ cấp (LS-04), chưa đọc được nguyên văn.
- **OB-3**: phát âm chỉ được máy nghe kiểm; tai người NOT_VERIFIED.
- **OB-4**: hiệu quả với người học thật NOT_VERIFIED (ROADMAP §8.2).
- **OB-5**: 537 bài ngoài hai lộ trình không được đọc lại trong đợt này.
- **OB-6**: CB-2 của SC1 (không có trình biên dịch C) và CB-5 (hệ thống ngoài: Redis/Oracle/Kafka/T24/NAPAS) vẫn NOT_VERIFIED. Khối mã của hai lộ trình chạy được trên máy thì đã chạy (Java, Python, sqlite, node, go).
