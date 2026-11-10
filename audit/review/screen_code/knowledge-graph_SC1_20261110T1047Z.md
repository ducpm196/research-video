# knowledge-graph_SC1_20261110T1047Z: đồ thị chứng cứ của việc 1 (cổng mã trên màn hình)

Chỉ ghi nút OBSERVED hoặc CITED (máy chạy trong phiên này). Mũi tên `→` nghĩa là "là căn cứ cho".
Môi trường: Windows 11; `.venv` Python 3.13.5; Python hệ thống 3.11.9 có pycparser 3.00 ở user site; JDK 22.0.2; node v25.8.0; go1.25.5; GNU bash 5.2.37. Không có gcc/clang/cl; Docker daemon không chạy.

| ID | Khẳng định | Phương pháp (lệnh đã chạy) | Quan sát | validity | checked_at |
|---|---|---|---|---|---|
| SC-001 | Kho có 540 khối mã hiển thị, ở 27 khoá | `screen_code.py inventory` | `# 540 khối` | VALID | 2026-11-10T10:5xZ |
| SC-002 | Một phép đếm độc lập cho cùng 540 khối | `scratchpad/sc/crosscount.py` (regex trên `show` đã nạp) | `540 {...}`, số theo khoá giống SC-001 | VALID | 2026-11-10 |
| SC-003 | Chữ cổng trích ra = chữ trên khung hình | so `show` với `out/SDP/L02/frames/00023.png`, `out/CAS/L03/frames/00062.png`, `out/JVA/L11/frames/00059.png` | khớp từng dòng, cả thụt lề | VALID | 2026-11-10 |
| SC-004 | JVA: 306 khối khớp 110 chương trình nguồn | `screen_code.py gen-jva` | `306 khối, ghi 306, nguồn 110, chưa khớp 0` | VALID | 2026-11-10T11:05Z |
| SC-005 | Cổng JVA sạch | `screen_code.py check --course JVA` | `PASS 416 · FAIL 0 · STALE 0 · MISSING 0 · ORPHAN 0 · WARN 0` | VALID | 2026-11-10T11:05:45Z |
| SC-006 | JVA L00, L11: khối thông báo javac khác điều javac in thật (MUST) | lần chạy cổng trước khi sửa + javac 22.0.2 | `error: class Chao is public, should be…`; dòng `phi(long) in MienPhi cannot implement…` cộng một dòng thụt lề | VALID (lỗi đã sửa) | 2026-11-10T10:59Z |
| SC-007 | verify_jva còn PASS sau khi sửa lib/l00/l11 | `audit/jva/verify_jva.py` | `110/110 PASS` | VALID | 2026-11-10T11:01:34Z |
| SC-008 | Cổng bắt đủ các loại lỗi cấy | `screen_code/negative_controls.py` | `22/22 ca đúng kết luận` | VALID | 2026-11-10T11:08:27Z |
| SC-009 | Ca dương bắt được lỗi trong chính cổng (`-I` tắt user site, mất pycparser) | negative_controls lần 1 | `21/22`; sửa xong `22/22` | VALID | 2026-11-10T11:07:58Z |
| SC-010 | Giáo án không có khối mã | `grep -c 'class="code"\|<pre' curriculum/*.yaml` | không tệp nào ≠ 0 | VALID | 2026-11-10T11:06:37Z |
| SC-011 | audit_all có chạy cổng | `audit_all.py jva` | chỉ báo JVA L00/L11 STALE (chờ dựng lại), không có dòng `mã màn hình` | VALID | 2026-11-10 |
| SC-012 | SDP L02, L04: mã sau sửa chạy đúng các con số bài nói | `check --course SDP -v` | 3 PASS `post qua` | VALID | 2026-11-10T11:07:27Z |

| SC-013 | Cổng toàn kho sạch (bản cuối: so cả dòng, `twin_of` được kiểm, `-X utf8`, bỏ chú thích C) | `screen_code.py check -v` → `logs/check_all_final.out` | `541 khối — PASS 724 · FAIL 0 · STALE 0 · MISSING 0 · ORPHAN 0 · WARN 0`; unverified 122 | VALID | 2026-11-10T12:42:16Z |
| SC-014 | Lỗi cấy, bản cuối | `negative_controls.py` | `30/30 ca đúng kết luận` | VALID | 2026-11-10T12:3xZ |
| SC-015 | Đã sửa 17 khối MUST ở 15 bài, 6 SHOULD (danh sách ở report_SC1 §2) | đếm bằng Python từ báo cáo nhóm + diff | `MUST blocks 17 lessons 15 · SHOULD 6` | VALID | 2026-11-10T13:1xZ |
| SC-016 | 17 bài dựng lại đều PASS, ASR chưa xem xét 0 | `logs/rebuild_{jva,g13,g24,jva08}.out` | mỗi dòng `verify: … → PASS`, `chưa xem xét 0` | VALID | 2026-11-10 (18:13–19:36 +07) |
| SC-017 | Kho sạch toàn bộ sau mọi sửa | `audit_all.py` → `logs/audit_all_final.out` | `656 bài, 656 đã dựng, 0 bài có vấn đề` | VALID | 2026-11-10 ≈13:08Z |
| SC-018 | Bộ kiểm khoá và cổng phụ | verify_{sdp,web,plc,cvi,esy,cs112,cs112_p2,jva,gfx,dbs}; check_xref; check_meta; scan_ctrl | 0 FAIL mọi bộ; xref 0; meta 0; ctrl 8 (JVA cố ý) | VALID | 2026-11-10 ≈12:40Z |
| SC-019 | Kiểm độc lập: không MUST, không NÉ; 9 phát hiện sổ/cổng đã xử lý | 2 tác tử chỉ đọc → `verify_AB.md` | xét 304 mục, 20 bài đổi | VALID (CITED: báo cáo tác tử; mọi sửa do người điều phối đã chạy lại cổng — SC-013) | 2026-11-10 |
| SC-020 | Bản sao video phỏng vấn trùng byte | `interview_sync_video.py --check` | `92 pairs, 92 identical` | VALID | 2026-11-10 |

Điểm nghẽn:
- CB-1 CLOSED (SC-001, SC-002, SC-003; thêm bộ trích `<code>…<br/>` sửa theo nhóm 3, 6 khối ACB kiểm lại).
- CB-3 CLOSED (SC-019).
- CB-4 CLOSED (SC-019 + sửa sổ; SC-013).
- CB-6 CLOSED (SC-016, SC-017, SC-018).
- CB-2 OPEN: không có trình biên dịch C; 10 khối C chỉ kiểm cú pháp.
- CB-5 OPEN: hệ thống ngoài; 122 NOT_VERIFIED.

Hai điểm nghẽn còn mở đã ghi rõ trong báo cáo; chúng không chặn DONE của phạm vi đã cam kết, vì phần không kiểm được đã được liệt kê thay vì gọi là đã kiểm.
