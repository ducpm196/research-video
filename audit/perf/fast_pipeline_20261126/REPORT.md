# Áp dụng 3 tối ưu tốc độ dựng video — 2026-11-26

Tier: inline kèm tệp bằng chứng này (không chạy lifecycle `full` vì `HANDOVER.md`/`state/` đang được tác tử khác ghi).
**Bổ sung 21:00 cùng ngày:** xem `KIEM_ANTIGRAVITY.md` — phát hiện lỗi mất slide có sẵn từ `lv.py` mà phép so ở đây không thấy (hai bài thử đều không trúng); BN-FP6 đã đóng; ước tính 16–17 giờ quá lạc quan.

Final: **PARTIAL** — ba thay đổi đã cài và kiểm; mức lợi của thay đổi 3 khi máy nghe chạy trên GPU thật chưa đo (BN-FP6).

## Phạm vi
- Chỉ THÊM tệp: `tools/lv_fast.py`, `audit/build_queue_fast.sh`, thư mục này. Không sửa tệp nào đang dùng, không commit.
- Hàng đang chạy (`build_queue.py` của Antigravity gọi `tools/lv.py`) **không** dùng ba thay đổi này.

## Cách dùng
```bash
.venv/Scripts/python tools/lv_fast.py build lessons/<khoá>/Lxx_*.yaml     # thay đổi 1 + 2
bash audit/build_queue_fast.sh KHOÁ [Lxx …]                              # 1 + 2 + 3
SKIP_FRESH=1 bash audit/build_queue_fast.sh KHOÁ                         # bỏ qua bài đã đúng đặc tả và đã nghe sạch
for C in CSA CVI DAN; do SKIP_FRESH=1 bash audit/build_queue_fast.sh $C || break; done
touch audit/review/queue_fast.stop                                        # dừng sạch (xoá tệp trước lần chạy sau)
```
Tắt từng phần: `LV_FAST_ENC=nvenc|x264|off`, `LV_FAST_FPS=10`, `LV_FAST_YAML=0`. Hàng nhanh từ chối chạy khi có hàng dựng khác (`ALLOW_PARALLEL=1` để bỏ rào).

## Thay đổi
1. Ghép MP4 10 khung/giây bằng `h264_nvenc` (`-cq 23 -g 83 -bf 0`), lỗi NVENC → `libx264` 10 khung/giây; bỏ `-shortest`, giữ `-t`.
2. `curriculum/*.yaml` đọc bằng `CSafeLoader`; mọi tệp khác giữ bộ đọc cũ.
3. Máy nghe chạy nền, song song với bài kế tiếp; nhiều nhất một ASR. Chính sách giọng, log, `production_log.tsv` như `audit/build_queue.sh`.

## Contract bottleneck
| ID | undefined or unverified | dependent work | missing evidence | consequence | resolution test | state |
|---|---|---|---|---|---|---|
| BN-FP1 | Thay đổi có đụng hàng đang chạy không | REQUIRED: 1, 2, 3 | — | hàng đang chạy hỏng hoặc đổi hành vi | sha256 tệp đang dùng trước = sau; log không thêm lỗi | CLOSED (V-1) |
| BN-FP2 | MP4 10 khung/giây giữ đúng đầu ra | REQUIRED: 1 | — | video sai, lệch tiếng/phụ đề | `verify_ab.py`, `verify`, giải mã, phát thử | CLOSED (V-2, V-3; 2 bài) |
| BN-FP3 | CSafeLoader đọc y hệt | REQUIRED: 2 | — | đổi nội dung lặng lẽ | `yaml_eq.py` | CLOSED (V-4) |
| BN-FP4 | NVENC không dùng được | REQUIRED: 1 | — | dựng FAIL | giả lập mất GPU | CLOSED (V-5) |
| BN-FP5 | Hàng song song đúng thứ tự và chính sách giọng | REQUIRED: 3 | — | log sai, tranh tệp | công cụ giả + 2 bài thật | CLOSED (V-6) |
| BN-FP6 | ASR trên GPU chạy cùng NVENC: đủ bộ nhớ, không chậm | REQUIRED: mức lợi của 3 | chưa đo (GPU đang phục vụ hàng đang chạy) | chậm hơn ước tính; kết quả không sai (cả hai có đường lùi) | chạy ≥ 5 bài có câu mới khi hàng hiện tại đã xong; tìm “[WARN] ASR” và “lùi về libx264” | OPEN (since 2026-11-26; owner: agent) |
| BN-FP7 | Phát trên điện thoại, nền tảng video | OPTIONAL: phân phối | chưa thử | có thể phải đổi cách ghép | mở thử MP4 10 khung/giây trên thiết bị đích | OPEN (since 2026-11-26; owner: person) |

## Bằng chứng (OBSERVED trong phiên)
| ID | CLAIM | METHOD | OBSERVED RESULT | validity |
|---|---|---|---|---|
| V-1 | Tệp đang dùng không đổi | `sha256sum` đầu phiên và lúc 08:44:02Z | `lv.py` 999fb87a…, `build_queue.sh` = `.build_queue_run.sh` ba996eb2…, `build_queue.py` c2b6fa52… giống nhau; không thêm `BUILD_FAIL` sau 14:30 | VALID |
| V-2 | Đầu ra tương đương | `verify_ab.py` trên CLC L07 (A, B cùng dựng trong bản cách ly) và L08 (A = bản hàng đang chạy dựng) | âm thanh AAC, `.srt`, chương, `_frames.txt`, mọi PNG, `spec_sha256`, `tts_sha256` giống; mốc slide 91/91 và 95/95, lệch ≤ 0,033 s; thời lượng giống; giải mã không lỗi; `verify` PASS | VALID |
| V-3 | Phát được trong Edge, chữ không đổi | Playwright `msedge`: nạp, tua 7 mốc, phát 3 s; xem ảnh cắt cạnh nhau | không lỗi, 0 khung rớt, ảnh hai bản lệch ≤ 0,19/255 | VALID |
| V-4 | YAML giống | `yaml_eq.py` | 1 914 tệp: khác 0 (lúc 07:39Z; chạy lại 08:48Z: khác 0, 1 tệp cùng lỗi ở cả hai bộ đọc, lần quét ngay sau không còn lỗi); 40 000 đột biến: 0 ca khác giá trị, 292 ca bộ C dễ dãi hơn; `lint` hai bài ra giống hệt | VALID |
| V-5 | Đường lỗi đúng | `CUDA_VISIBLE_DEVICES=-1`, `LV_FAST_ENC`, lệnh ghép bị đổi, đường dẫn hỏng | lùi về x264; `off` ra đúng 30 khung/giây; lệnh lạ → cảnh báo và chạy nguyên lệnh gốc; cả hai hỏng → lỗi đẩy lên | VALID |
| V-6 | Hàng nhanh đúng hành vi | công cụ giả 7 bài; hàng thật CLC L07, L08; `SKIP_FRESH=1`; rào | 10/10 tiêu chí thứ tự; dựng L07 46 s, L08 40 s (ưu tiên thấp nhất, giọng và ASR từ bộ nhớ đệm); bỏ qua đúng bài đã mới; từ chối khi hàng khác đang chạy | VALID |

## Lỗi bắt được trong lúc kiểm, đã sửa
- Ở 10 khung/giây, `-shortest` cắt 1 568 mẫu (0,065 s) cuối bài; `verify` vẫn PASS nên cổng không thấy → bỏ `-shortest`.
- B-frame làm `av_scan.py` đo hình − tiếng −0,33 s (video thật đủ dài) → `-bf 0`, đo −0,03 s.
- CSafeLoader chấp nhận TAB và vài cú pháp sai mà bộ cũ từ chối → thu hẹp còn `curriculum/`, né ký tự lạ, lỗi thì đọc lại bằng bộ cũ.
- Ghi nhãn bộ mã hoá lỗi có thể làm bài đã PASS trả mã FAIL → bắt ngoại lệ.
- Rào chạy chồng bỏ sót hàng bash lúc đang ngủ, và khớp nhầm shell chỉ nhắc tên tệp → sửa mẫu, thử 3 tình huống.

## Thời gian
- OBSERVED, bước ghép MP4 trọn CLC L07 (656,8 s), xen kẽ 2 vòng, ưu tiên thấp nhất: gốc 240 s; NVENC 10 khung/giây 27 s; x264 10 khung/giây 51 s.
- OBSERVED, đọc 54 giáo án: bộ cũ 1,5–6,3 s, bộ C 0,1–0,5 s (tuỳ tải) → lợi 1–6 s mỗi bài (con số "≈ 8 s" nói trước đó là quá cao).
- OBSERVED, kích thước: lớn hơn 3–5 % (20,05 → 21,05 MB; 21,04 → 21,76 MB).
- INFERRED (từ 80 bài gần nhất, lúc 15:43; phụ thuộc BN-FP6): còn 458 bài — giữ nguyên ≈ 33 giờ; thay đổi 1 + 2 ≈ 21–22 giờ; cả ba ≈ 16–17 giờ.
- Không tối ưu nào ở đây giúp việc chờ giọng đọc online: CSA L00–L02 (21–23 câu mới mỗi bài) chờ 141–374 s.

## Ảnh hưởng của việc kiểm lên hàng đang chạy
Phép thử chạy ở mức ưu tiên thấp nhất (trừ vài lệnh ngắn), không gọi dịch vụ giọng đọc, có dùng NVENC. Tốc độ ghép của hàng đang chạy trong lúc thử (14:34–15:35) là 5,2–6,1× thời gian thực, so với trung vị 6,0× của 78 bài đo trước khi thử (OBSERVED): vài bài chậm tới khoảng 13 %, không loại trừ do phép thử (INFERRED).
