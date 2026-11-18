# BNX2 — cắt độ dài L24–L30 xuống lời đọc ≤ 2 300 từ (2026-11-14)

Mục tiêu: lint ước ≤ 16 phút (150 từ/phút → ≤ 2 400 từ; đặt trần riêng 2 300 từ). Chỉ sửa NGUỒN `audit/bnx/src/lNN.py` (lời đọc `say`, `focus`, xoá vài step phụ, đánh số lại hộp lỗi); không sửa `curriculum/bnx.yaml`, không đổi `objectives`/`covers`, không đổi khối mã, không chạy build/tts/asr/git.

## Kết quả

| Bài | Từ trước → sau | Phút trước → sau | lint | render | verify_bnx | screen_fast | Ghi chú cắt |
|---|---|---|---|---|---|---|---|
| L24 | 3 349 → 2 281 | 22,3 → 15,2 | 0F/0W | 0 | 20/20 | 34/0 | bỏ step lộ trình hook, bỏ Lỗi 1 (tải ngay), nén mọi lời |
| L25 | 2 864 → 2 226 | 19,1 → 14,8 | 0F/0W | 0 | 13/13 | 24/0 | bỏ step lộ trình hook, nén lời |
| L26 | 2 828 → 2 271 | 18,9 → 15,1 | 0F/0W | 0 | 23/23 | 36/0 | bỏ step lộ trình hook, nén lời |
| L27 | 2 729 → 2 197 | 18,2 → 14,6 | 0F/0W | 0 | 20/20 | 25/0 | bỏ step lộ trình hook, nén lời |
| L28 | 2 667 → 2 234 | 17,8 → 14,9 | 0F/0W | 0 | 18/18 | 24/0 | bỏ step lộ trình hook, bỏ Lỗi 1 (người mới) |
| L29 | 2 599 → 2 270 | 17,3 → 15,1 | 0F/0W | 0 | 21/21 | 24/0 | bỏ step lộ trình hook, nén lời |
| L30 | 2 626 → 2 264 | 17,5 → 15,1 | 0F/0W | 0 | 17/17 | 23/0 | bỏ step lộ trình hook, nén lời |

`python audit/review/lab_gate.py BNX`: 13 PASS · 0 FAIL. `lib2.py gen-screen` chạy lại cho cả 7 bài (sổ khối mã khớp, khối mã không đổi).

## Đã cắt gì

- Mọi bài: bỏ step "Hôm nay ta trả lời bốn câu" (bảng lộ trình ở hook, ≈ 90–100 từ mỗi bài). Hook còn một step có con số.
- Nén lời đọc cảnh `recap`: bảng "Nếu bị hỏi về dòng này trên CV" giữ nguyên trên màn hình, lời chỉ nêu ba câu hỏi và dặn tự nói lại từ bảng (trước ≈ 100–130 từ, nay ≈ 45).
- Nén `quiz` (đề đọc gọn, đáp án giữ đủ phép tính), `pitfalls`, `quymo`, `formula`, `example`, `prereq`, `sym`, `intuition`: bỏ câu lặp, tách câu dài > 38 từ, giữ lý do ("vì/nên") ở mỗi bước suy luận (lint không cờ).
- L24 bỏ Lỗi 1 (đổi mọi quan hệ sang tải ngay) và L28 bỏ Lỗi 1 (chọn hệ vì mọi người dùng); các hộp lỗi còn lại đánh số lại 1–3 trên màn hình. Cả hai bài còn 3 lỗi, đều là "người đã đi làm"; L25, L26, L27, L29, L30 giữ 4 lỗi.

## Giữ nguyên (đã kiểm)

- Mọi mục tiêu `covers` (E51/E53 PASS), cảnh Tự làm + lab (13/13 lab PASS), cảnh quy mô với số đo thật (×1/×100/×10 000), thuật ngữ giảng tại chỗ (lint E52 sạch, không WARN), mọi khối mã chạy được (sổ màn hình khớp, không STALE/MISSING).
- Số trong lời đọc khớp màn hình và `verify_bnx` (không đổi số nào; chỉ bỏ bớt số lặp trong lời, màn hình vẫn đủ).
- Quét 7 bài: 0 câu < 8 từ, 0 câu > 38 từ hay > 170 ký tự (sau khi ghép câu ngắn của `_spoken`).

## Đề xuất tách bài

Không cần. Cả 7 bài xuống ≤ 2 300 từ mà không mất mục tiêu. Lưu ý cho người điều phối:

- L24 gồm hai chủ đề (Hibernate/ngữ cảnh bền vững + Spring Data), nhưng phần Spring Data chỉ là một step đọc theo hướng dẫn (không chạy được ở máy này) nên vẫn vừa; L24 là bài sát trần nhất (2 281 từ, 15,2 phút).
- Biên còn lại mỏng: L24 2 281, L26 2 271, L29 2 270, L30 2 264 từ (trần 2 300). Đừng thêm lời nếu không cắt chỗ khác.
- Hook không còn bảng "bài này trả lời mấy câu" (roadmap); nếu muốn lại, phải cắt chỗ khác tương ứng.
- Chưa dựng video: thời lượng thật sau TTS có thể lệch so với ước 150 từ/phút; nên đo lại ở lần build kế tiếp.

## Tệp sửa

`audit/bnx/src/l24.py` … `l30.py` (nguồn); YAML sinh lại `lessons/bnx/L24…L30_*.yaml` bằng `gen.py`; sổ khối mã `audit/bnx/screen/lNN.yaml` do `gen-screen` ghi lại (nội dung khớp).
