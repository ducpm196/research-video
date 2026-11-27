# Rà soát tiến độ Antigravity và cấu trúc repo — 2026-11-27, số liệu lấy 11:34–12:00 (+07)

Phạm vi: chỉ đọc. Không sửa, không xoá, không dừng tiến trình nào; tệp duy nhất được thêm là báo cáo này.
Nhãn: OBSERVED = đã chạy/đọc trong phiên; CITED = trích nhật ký của Antigravity; INFERRED = suy luận, chưa kiểm.

## A. Tiến độ

| Mục | Kết quả | Nhãn | Cách đo |
|---|---|---|---|
| Hàng dựng chính (task-14716) | DONE 07:59:41; built 526, skipped 107, build_fail 12; 56 840 s | OBSERVED | dòng DONE trong nhật ký hàng |
| Đợt dựng lại 1 (task-17547) | 136 bài: 103 OK, 33 lỗi (3 build: EVT/L08, EVT/L09, MLO/L14; 30 còn câu ASR chưa xem); cả 3 bài build đã qua ở đợt 2 | OBSERVED | nhật ký task |
| Đợt dựng lại 2 (task-18650) | 60 bài; lúc 12:00: 32 OK, 7 FAIL_ASR, 0 FAIL_BUILD | OBSERVED | nhật ký task |
| Video mất slide | 806 kiểm, 0 hỏng (12:00) | OBSERVED | fix_rgba/video_gap_scan.py |
| Video khớp giáo án hiện tại | 773/806 (11:35–11:39) | OBSERVED | scratch/check_fresh_read_af5.py của Antigravity |
| Báo cáo đọc độc lập read_af5 | 737 khớp, 69 cũ (giáo án đã sửa sau khi đọc), 0 thiếu | OBSERVED | cùng lệnh |
| Câu ASR chưa xem thật | 198 câu / 42 bài (~11:41). 363 báo cáo còn ghi "chưa xem xét > 0", trong đó 321 cũ hơn tệp giáo án (cần chạy lại asr) | OBSERVED | so asr_report với asr_reviewed hiện tại |
| Lý do "đã xem" sinh theo mẫu | cụm "NOT_VERIFIED bằng tai người" xuất hiện 4 234 lần trong 693 giáo án | OBSERVED | đếm trong lessons/ |
| Tiền kiểm | screen_code 4 680 PASS, 0 FAIL, 26 STALE, 9 MISSING, 1 ORPHAN (Antigravity đang xử lý); verify_plan_curricula 641/0 | OBSERVED | nhật ký task-18690 |
| verify_spb | 13 PASS, 1 FAIL (SPB:L10, Maven: 2 test lỗi); nguyên nhân NOT_VERIFIED | OBSERVED | nhật ký task-18743 |
| Đọc lại còn ra MUST | DSC/L02, DSY/L10 (đã sửa, cần dựng lại) | CITED | transcript 04:42Z |
| quality.yaml | updated_at 2026-11-24; lớp C vẫn nhãn "Tự làm đang làm lại", CPR/LNX/MLP/PRJ "Đang viết lại" | OBSERVED | đọc tệp |
| Git | ~1 216 mục chưa commit từ 9dca8d86 | OBSERVED | git status |

Theo plan_AF5_20261123T0110Z.md: WP-6 (dựng, ASR) đang ở đoạn cuối; WP-7 (nghiệm thu: 26 cổng chế độ day_du, mẫu >= 60 bài với người đọc mới, sinh lại trang học, bàn giao) chưa thấy bắt đầu. Việc hoàn thành WP-0..WP-5 chỉ là CITED từ hồ sơ của Antigravity, lượt này không kiểm lại nội dung.

### Dự kiến xong (INFERRED)

| Bước | Ước lượng | Căn cứ |
|---|---|---|
| Xong đợt dựng lại 2 | ~12:30 | còn 21 bài, ~86 s/bài |
| ASR, đọc lại, dựng phần vừa sửa | 1–2 giờ | 169 lượt tác tử, trung vị 449 s |
| 26 cổng day_du | 4–5 giờ | hôm nay: screen_code 32', tts_speed 19', verify_spb 18'; trước đó: audit_all 77', lab_gate 48'; pack --decode chưa đo |
| WP-7 phần còn lại | 1,5–2,5 giờ | |

Sớm nhất khoảng 20:00 ngày 27/11 nếu mọi cổng đạt ngay; thực tế hơn là trong ngày 28/11. Giả định tác tử không dừng vì giới hạn lượt (đã xảy ra 25/11) hay đứng yên (26/11, ~5 giờ).
Theo chính plan, trạng thái cuối là PARTIAL khi BN-08 (tai người) chưa đóng. Commit cần người dùng cho phép.

## B. Cấu trúc repo

Tổng ~107,9 GB (OBSERVED, quét tệp 11:43).

| Thành phần | Dung lượng | Đánh giá |
|---|---:|---|
| cuahang.jar (gốc repo) | 42,6 GB | Rác. Là ZIP 577 363 mục chứa bản chụp out/ (có PYT/L13/L13.mp4...), tạo 23/11 20:23 |
| out/_cache/tts | 30,0 GB | 23,8 GB đang được lessons/ dùng; 6,19 GB (39 465 tệp) không còn dùng |
| out/ mp4 | 19,9 GB | sản phẩm |
| out/ frames PNG | 10,2 GB | GIỮ: HOC_TAP.html trỏ tới 1 182 ảnh |
| labs/.venv-ml, .venv-pyt | 1,16 GB | môi trường chạy lab, mã đang trỏ tới; giữ |
| interview/video | 0,91 GB | bản chép từ out/ (interview_sync_video.py) |
| .venv-tts, .venv | 1,44 GB | môi trường |
| audit/ | 0,71 GB | bnx/deps 0,45 GB; ảnh snap + sheets 140 MB đang nằm trong git |
| .git | 0,35 GB | |

Nguyên nhân rác ở gốc (INFERRED; ai chạy: NOT_VERIFIED): lời giải lab chạy ngay tại gốc repo thay vì thư mục tạm. Dòng cuối labs/JV2/L00/loi_giai.sh là "jar --create --file cuahang.jar ... -C out ."; tại gốc, out là toàn bộ video của kho.
26 tệp rác đã bị commit trong 9dca8d86 (Tong.java, tinh.py, cua_hang/, vp/, src/, tien_ich/...). Ngoài ra Tong.class, out.bin, __pycache__ không được theo dõi. *.jar bị .gitignore nên git status không bao giờ báo tệp 42,6 GB.

Chỗ chưa hợp lý khác:
- audit/ trộn bốn loại: bộ cổng (audit/review/), bộ kiểm từng khoá, bộ sinh đã khoá + mốc so af2/base (557 tệp), báo cáo/nhật ký.
- Gốc audit/: 49 layout_*.tsv (do layout_scan.py ghi), 45 REVIEW_*.md (không mã nào trỏ), 16 tệp .py rời.
- Gốc repo: HANDOVER.md, STATE.md, state/ (hồ sơ cũ); skills/ là bản chép một skill (bản Gemini) — còn ai dùng: NOT_VERIFIED.

Phần ổn, không nên đụng: tools/, curriculum/, lessons/, labs/, tests/, examples/ (test_lint.py dùng), resources/ (cổng giáo án dùng).

### Đề xuất theo giai đoạn

| GĐ | Việc | Được | Rủi ro | Thời điểm |
|---|---|---|---|---|
| 1a | Xoá cuahang.jar | 42,6 GB | Không hoàn tác; không mã nào đọc tệp ở gốc | làm được ngay |
| 0 | Commit mốc | điểm quay lui | — | sau khi Antigravity xong |
| 1b | git rm 26 tệp rác, xoá 3 mục không theo dõi, thêm cổng "gốc repo chỉ gồm danh sách cho phép" | gốc sạch, hết tái diễn âm thầm | thấp | sau GĐ 0 |
| 2 | Xoá cache TTS không dùng | 6,2 GB | quay lại lời cũ phải tạo giọng lại qua mạng | sau nghiệm thu |
| 2 | Dồn REVIEW_*.md, layout_*.tsv vào audit/reports/; bộ sinh + af2/base vào archive/; HANDOVER/STATE/state vào docs/ | gọn | trung bình: layout_scan.py, frame_step.py, af2_upgrader.py, s9_11/common.py, dms/af2 trỏ đường dẫn | sau nghiệm thu |
| 2 | Bỏ theo dõi ảnh snap/sheets | chỉ mục git nhẹ hơn 140 MB (lịch sử vẫn giữ) | thấp | sau nghiệm thu |
| 3 | Đổi tên/tách audit/review | thẩm mỹ | cao: 156 tệp mã trỏ tới | không khuyến nghị |

Không di chuyển tệp nào khi hàng dựng, tác tử và cổng còn chạy.

## Contract bottleneck còn mở

| ID | Chưa xác định | Phụ thuộc | Thiếu chứng cứ | Hệ quả | Phép đóng | Trạng thái |
|---|---|---|---|---|---|---|
| BN-RR1 | 26 cổng day_du chưa từng có lượt chạy trọn được ghi lại | REQUIRED: ETA, WP-7 | thời lượng và kết quả thật | ETA có thể lệch nhiều | chạy final_gates_af5.sh day_du, đọc dòng tổng | OPEN (since 2026-11-27; owner: agent) |
| BN-RR2 | SPB:L10 FAIL | REQUIRED: WP-7 | nguyên nhân | cổng 26 không đạt | chạy lại verify_spb khi máy rảnh | OPEN (owner: agent) |
| BN-RR3 | Cho phép xoá/di chuyển/commit | REQUIRED: GĐ 0–2 | quyết định của người dùng | repo giữ nguyên | người dùng trả lời | OPEN (owner: person) |
| BN-RR4 | Ai chạy lời giải lab tại gốc repo | OPTIONAL: GĐ 1b | nhật ký lệnh | có thể tái diễn | cổng danh sách cho phép ở gốc | OPEN (owner: agent) |

Trạng thái lượt rà soát: DONE cho phần đánh giá; việc tổ chức lại chưa thực hiện (chờ BN-RR3).

Ghi lúc 2026-11-27 12:01:38.
