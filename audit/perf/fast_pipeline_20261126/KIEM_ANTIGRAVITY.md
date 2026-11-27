# Kiểm tác tử Antigravity sau khi áp dụng 3 tối ưu + lỗi mất slide — 2026-11-26

Tier: inline kèm tệp bằng chứng. Chỉ đọc trên kho và hàng đang chạy; mọi phép dựng thử làm trong thư mục cách ly, ưu tiên thấp nhất.
Final: **PARTIAL** — ba thay đổi được tác tử áp dụng đúng; phát hiện 34 video mất slide (lỗi có sẵn từ lv.py); bản sửa ĐÃ cài vào lv_fast.py 21:23 (mục 9) và vào lv.py 21:51 (mục 10); video hỏng chưa dựng lại.

## 1. Đối chiếu với yêu cầu giao cho tác tử lúc 16:06 (OBSERVED trừ khi ghi khác)
| Yêu cầu | Kết quả |
|---|---|
| NVENC 10 khung/giây | PASS — mọi BUILD_OK (89 lúc 21:15) là h264_nvenc@10fps, 0 lần lùi x264; tiếng − timeline 0,0423–0,0427 s, đúng bằng bản lv.py |
| Đọc YAML bằng C | PASS — qua tools/lv_fast.py (chỉ curriculum/) |
| Máy nghe song song | PASS — viết lại build_queue.py (không dùng build_queue_fast.sh); 0 cảnh báo GPU, 0 thiếu audio, mọi asr_report mới hơn bản dựng |
| Không ảnh hưởng phần đã xong | PASS — hàng cũ dừng sau khi CSA/L07 nghe xong (16:09:59), bỏ qua L00–L07; mọi khoá ngoài hàng (gồm FND) đều đúng đặc tả |
| Chuẩn xác, không lỗi, đầy đủ | FAIL — xem mục 2, 3, 4 |

## 2. Lỗi mất slide (có sẵn từ lv.py, không do tác tử; `verify` không bắt)
- Hiện tượng: màn hình nhảy sang slide sau quá sớm; thường 2 slide không xuất hiện (7–42 s) trong khi giọng vẫn giảng; DSC/L09, EVT/L09 mất hình đầu bài.
- Nguyên nhân: render (Playwright) thỉnh thoảng trả một PNG RGBA (16–32 điểm ảnh alpha<255) giữa các PNG RGB; ffmpeg dựng lại bộ lọc khi định dạng đổi.
- Quy mô lúc 14:17:53Z: **34/805 video** (25 dựng bằng lv.py, 9 bằng lv_fast). 20 bài hàng đang chạy sẽ dựng lại (vẫn có thể trúng lại nếu chưa cài sửa); 14 bài hàng không quay lại: BNX/L09, CLC/L11, CS115/L04, CVI/L09, DEN/L05, DEN/L07, DSC/L09, DSY/L00, DSY/L05, DSY/L11, DVO/L06, DVO/L07, PYT/L00, PYT/L13.
- Ngẫu nhiên: dựng lại DSC/L09 trong bản cách ly ra toàn RGB. Tỉ lệ đợt mới 9/89 so với 4/157 của hàng cũ cùng ngày; KHÔNG do máy nghe song song (0/9 ảnh RGBA được render lúc máy nghe chạy); nguyên nhân chênh lệch NOT_VERIFIED.

## 3. Việc tác tử bỏ dở
- Không còn hoạt động từ 16:42:56; hẹn giờ 20 phút đặt lúc 16:31 không thấy báo về (lý do NOT_VERIFIED). Hàng dựng là tiến trình riêng nên vẫn chạy.
- BUILD_FAIL chưa ai xử lý, hàng không tự thử lại: CSA/L11, DEN/L04 (render: nội dung TRÀN bảng).
- Cờ máy nghe chưa xem xét trong đợt này: 82 bài, 463 câu (lúc 21:16).

## 4. Điểm yếu trong build_queue.py mới (đọc mã)
- Đổi tiêu chí bỏ qua ASR: chỉ cần "thiếu audio: 0" (bản cũ đòi "chưa xem xét: 0") → khi chạy lại, bài còn cờ bị đếm vào asr_ok trong dòng DONE.
- Không có vòng chờ 1 giờ như audit/build_queue.sh: cả hai giọng bị chặn thì ghi BUILD_FAIL rồi đi tiếp.
- Thời gian ASR trong log gồm cả lúc chờ bài kế tiếp (không phải thời gian nghe thật).

## 5. Tốc độ (OBSERVED, không phải phép so có kiểm soát)
- Ghép MP4: trung vị 115 s (hàng cũ, 157 bài) → 24 s.
- Cả bài: trung bình 261 s → 204 s (nhanh hơn khoảng 22 %); phần chờ giọng online chiếm phần lớn các bài chậm (380–680 s).
- Còn 447 bài ≈ 25 giờ (INFERRED). Ước tính 16–17 giờ trong REPORT.md quá lạc quan: đã giả định giọng có sẵn.

## 6. Bản sửa (đã cài 21:23, người dùng duyệt)
- `fix_rgba/lv_fast.py.candidate` (sha256 2dd084764fdd4d59…), diff `fix_rgba/lv_fast_rgba.patch`: đưa ảnh khung về RGB trước khi ghép; sau khi ghép, khung bị giữ lâu hoặc hình ngắn hơn timeline → đổi tên .broken.mp4 và FAIL.
- Cài (đổi hành vi hàng đang chạy từ bài kế tiếp; chỉ khi tools/lv_fast.py còn sha fca4b17501267dd5):
  `cp audit/perf/fast_pipeline_20261126/fix_rgba/lv_fast.py.candidate tools/lv_fast.py.tmp && mv tools/lv_fast.py.tmp tools/lv_fast.py`
- (21:23) lv.py chưa đổi; đã sửa lúc 21:51, xem mục 10.
- Quét lại bất kỳ lúc nào: `.venv/Scripts/python -B audit/perf/fast_pipeline_20261126/fix_rgba/video_gap_scan.py`

## 7. Bằng chứng
| ID | CLAIM | METHOD | OBSERVED RESULT | validity |
|---|---|---|---|---|
| K-1 | 34 video hỏng | video_gap_scan.py (bảng stts/mdhd) | "kiểm 805 video, hỏng 34", checked_at=2026-11-26T14:17:53Z | VALID |
| K-2 | Người xem thấy sai slide | lấy khung thật, so với PNG (DEN/L05, DSC/L09, CS115/L04) | hiện slide sau thay cho 2 slide đáng lẽ phải hiện | VALID |
| K-3 | Tương quan với PNG RGBA | quét IHDR mọi bài | 32/32 bài PNG lẫn định dạng đều hỏng; 0 bài lẫn định dạng mà lành (lúc quét có 33 hỏng; bài thứ 33 đã được render lại ảnh sau khi ghép) | VALID |
| K-4 | Tái hiện và sửa | ghép lại bản sao DSC/L09, DEN/L05 (cũ) và +CS115/L04, EVT/L09, CSA/L07 (sửa) | cũ: sai 2 slide/bài; sửa: 88/88, 105/105, 147/147, 74/74; CSA/L07 md5 hình giống hệt bản cũ | VALID |
| K-5 | Đầu-cuối | lv_fast build DSC/L09 trong bản cách ly, giọng từ bộ đệm | verify PASS, mã 0; lần render này không sinh RGBA | VALID |
| K-6 | Cổng bắt lỗi | cổng trên 805 video; tắt phần sửa rồi ghép ảnh lỗi | báo đúng 33/33 bài biết lúc đó, 0 báo nhầm; đường FAIL đổi tên .broken.mp4 | VALID |
| K-7 | ASR + NVENC cùng lúc | mốc tệp của 89 bài | 3 lần trùng, không lỗi; ghép 24,8–25,9 s mỗi 10 phút video so với trung vị 20,7 | VALID |

## 8. Contract bottleneck
| ID | undefined or unverified | dependent work | missing evidence | consequence | resolution test | state |
|---|---|---|---|---|---|---|
| BN-FP6 | ASR GPU chạy cùng NVENC | REQUIRED: thay đổi 3 | — | — | K-7 | CLOSED (K-7) |
| BN-RG1 | Bản sửa trên hàng thật | REQUIRED: các bài còn lại dựng đúng | mới quan sát 3 bài (DVO/L11–L13), chưa gặp ảnh RGBA | bài dựng tiếp có thể FAIL hoặc còn mất slide | quét video_gap_scan sau ≥ 20 bài dựng bằng bản mới | OPEN (since 2026-11-26; owner: agent) |
| BN-RG2 | Dựng lại 14 video hàng không quay lại (và soát 20 bài còn lại) | REQUIRED: kho video đúng | chưa dựng lại | video mất slide được coi là đã xong | video_gap_scan báo 0 | OPEN (since 2026-11-26; owner: agent) |
| BN-RG3 | Vì sao render sinh PNG RGBA, và vì sao đợt này nhiều hơn | OPTIONAL: sửa tại gốc | chưa tìm | bản sửa ở khâu ghép không phụ thuộc | tái hiện render nhiều lần | OPEN (since 2026-11-26; owner: agent) |
| BN-RG4 | Cổng trong lv.py verify không soi phần hình | OPTIONAL: gọi lv.py trực tiếp | — | — | K-11…K-14 | CLOSED (K-11, K-13) |
| BN-AG1 | Tác tử Antigravity ngừng theo dõi | REQUIRED: xử lý BUILD_FAIL và cờ nghe | lý do ngừng | hai bài lỗi và 82 bài còn cờ bị bỏ lại | mở cửa sổ agy, yêu cầu làm tiếp | OPEN (since 2026-11-26; owner: person) |
| BN-FP7 | Phát trên điện thoại, nền tảng video | OPTIONAL: phân phối | chưa thử | có thể phải đổi cách ghép | mở thử trên thiết bị đích | OPEN (since 2026-11-26; owner: person) |

## 9. Cài đặt và bàn giao
| ID | CLAIM | METHOD | OBSERVED RESULT | validity |
|---|---|---|---|---|
| K-8 | Cài đúng tệp đã thử | sha256 trước/sau, chép tệp tạm rồi mv | trước fca4b17501267dd5, sau 2dd084764fdd4d59, import được; lúc 2026-11-26T14:23:01Z | VALID |
| K-9 | Hàng dùng bản mới không hỏng | kiểm DVO/L11, L12 (bắt đầu sau 21:23:01) | BUILD_OK, cổng ổn, tiếng − timeline +0,0427 s, khung 6946/6946 và 7241/7241, không ảnh RGBA nên đường đổi ảnh chưa chạy trên hàng thật; DVO/L13 (21:38:13) cũng đạt, 10647/10647 khung | VALID |
| K-10 | Công cụ quét không báo nhầm bài đang ghi | quét lúc DVO/L13 đang ghép (báo "không đọc được"), sửa công cụ, quét lại sau khi xong | 805 video, hỏng 34, không bài nào mới so với danh sách trước; trạng thái "đang dựng" chưa được chạy thử trên bài đang ghi | VALID |
- DVO/L10 (bắt đầu 21:22:04, mã cũ) BUILD_FAIL do chữ tràn bảng.
- Bàn giao: `BAN_GIAO_ANTIGRAVITY.md`. CLI agy không có lệnh gửi tin vào phiên đang mở, nên người dùng phải dán lời giao.
- Bản trước khi cài còn ở git index (`git show :tools/lv_fast.py`).

## 10. Sửa gốc trong tools/lv.py (người dùng yêu cầu "sửa hoặc xoá"; không xoá vì 143 tệp Python import lv, lv_fast.py bọc quanh nó)
Chỉ thêm 75 dòng: `force_rgb` gọi ngay sau mỗi ảnh chụp trong `cmd_render`; `video_problem` trong `cmd_verify`. Không đụng spec_digest/tts_digest.
| ID | CLAIM | METHOD | OBSERVED RESULT | validity |
|---|---|---|---|---|
| K-11 | Đổi RGB không đổi hình; cổng mới đúng | force_rgb trên 4 ảnh RGBA thật + 1 ảnh RGB; video_problem trên 805 video | điểm ảnh RGB giống hệt, ảnh RGB giữ nguyên byte; báo 34, trùng video_gap_scan | VALID |
| K-12 | verify cũ lọt, verify mới chặn | verify DSC/L09, DEN/L05, CSA/L07 | cũ PASS cả ba; mới FAIL, FAIL, PASS | VALID |
| K-13 | Đầu-cuối và đối chứng | build trong bản cách ly, ép 2 ảnh thành RGBA | lv_fast và lv: đổi 2 ảnh, PASS; tắt force_rgb: khung bị giữ 13,8 s, verify FAIL | VALID |
| K-14 | Cài và chạy thật | chép tạm rồi mv lúc 21:51:42; ESY/L05 (bắt đầu 21:52:18) | sha 999fb87ae0970911 → 6e627c3e2fbfa7d1; BUILD_OK, verify PASS; lần này không sinh ảnh RGBA | VALID |
- Quay lại bản cũ: `git show HEAD:tools/lv.py` (tệp chưa đổi gì khác trước lần sửa này).
- lv_fast.py còn bản chuẩn hoá/cổng trùng với lv.py; vô hại, có thể gọn lại sau khi hàng xong.
- BUILD_FAIL mới: ESY/L03 (tràn bảng, 21:49, trước khi cài).
