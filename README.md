# research-video — xưởng video giảng giải cho người mới / mất gốc: CNTT, khoa học máy tính, dữ liệu, AI

Mục tiêu: một người **mất gốc, chưa từng lập trình**, chỉ cần xem video theo đúng thứ tự, tự làm các phần **Tự làm** (lab chạy được trên máy của mình) và làm các dự án cuối chặng, là đạt **năng lực nền của kỹ sư senior**: hiểu cơ chế, vận dụng được, thấy vấn đề đổi thế nào theo thời gian và theo quy mô. (Kinh nghiệm vận hành hệ thống thật thì không video nào thay được; kho nói rõ điều này.)

## Bắt đầu học
1. Mở **[`HOC_TAP.html`](HOC_TAP.html)** bằng trình duyệt (không cần mạng): lộ trình 11 chặng, bấm ▶ xem bài, tự kiểm, lịch ôn ngắt quãng, ghi chú, sao lưu tiến độ. `HOC_TAP.md` là bản chữ.
2. Chuẩn bị máy một lần: [`labs/ENV.md`](labs/ENV.md) — Windows + **Git Bash**, JDK 21, Python 3.11+, sqlite3, Git. Kiểm: `bash labs/check_env.sh`.
3. Mỗi bài có cảnh **Tự làm**: đề ở `labs/<KHOÁ>/<Lxx>/de.md`; tự làm trước, rồi chấm: `bash labs/cham.sh <KHOÁ> <Lxx> <tệp của bạn>` (in `ĐÚNG` khi đầu ra trùng kết quả mong đợi). Chỉ mở `loi_giai.*` sau khi đã thử.
4. Thứ tự học là thứ tự trong `HOC_TAP.html` (máy đã kiểm: mọi bài cần học trước đều đứng trước; trong một khoá, bài sau luôn sau bài trước).

## Cấu trúc kho
| Thư mục / tệp | Vai trò |
|---|---|
| `curriculum/` | lộ trình mỗi khoá (`<khoá>.yaml`), `ROADMAP.md` (kiến trúc chương trình), `STATUS.md` + `TRACKS.md` (sinh tự động, không sửa tay) |
| `lessons/<khoá>/` | đặc tả từng bài (YAML): màn hình, lời đọc, quiz, `checks`. Nhiều khoá được SINH từ `audit/<khoá>/src/` — sửa nguồn, rồi chạy `gen.py`, không sửa YAML tay |
| `labs/` | thực hành: `ENV.md`, `cham.sh`, `check_env.sh`, `<KHOÁ>/<Lxx>/{de.md, mong_doi.txt, loi_giai.*}` |
| `out/<KHOÁ>/<id>/` | video `.mp4`, phụ đề `.srt`, `chapters.txt`, `preview.html`, báo cáo máy nghe (không theo dõi bằng git) |
| `tools/` | `lv.py` (lint, dựng, nghe lại, lộ trình), hồ sơ chuyên ngành, sổ ký hiệu và phát âm, mẫu giao diện khung hình |
| `audit/` | bộ kiểm độc lập từng khoá (`verify_<khoá>.py` chạy mã/lệnh THẬT), bộ sinh bài, cổng toàn kho (`audit/review/`), sổ pháp lý (`audit/legal/`) |
| `interview/` | tài liệu ôn phỏng vấn backend ngân hàng (khoá JVA→BNK→BNX→INT→ACB), `MASTER_CURRICULUM_INDEX.md` |
| `archive/` | bàn giao cũ (giữ làm lịch sử) |
| `HANDOVER.md` | bàn giao mới nhất ở đầu tệp; phiên mới đọc theo mục "Phiên mới đọc theo thứ tự" |

## Chuẩn của một bài (lint chặn)
Bài đủ cho người mất gốc (`depth: full`) và đạt chuẩn AF2 (`af2: true`): mọi mục tiêu có cảnh dạy (`covers`), có cảnh **Tự làm** trỏ lab chạy được (`practice` + `lab:`), mọi thuật ngữ được giảng tại chỗ, có ví dụ làm tay, hình cơ chế, quiz kiểm hiểu, cảnh quy mô/thời gian (số tính được), mọi con số trên màn hình được máy tính lại, mã trên màn hình chạy được nguyên văn. Chi tiết: `audit/review/audit_final/BRIEF_AF2.md` và `.claude/skills/lecture-video/`.

## Lệnh thường dùng (từ gốc kho, Git Bash; Python = `.venv/Scripts/python`)
```
python tools/lv.py lint     lessons/<khoá>/Lxx_*.yaml      # 0 FAIL, 0 WARN
python tools/lv.py render   lessons/<khoá>/Lxx_*.yaml      # kiểm bố cục khung hình, không cần giọng
python tools/lv.py build    lessons/<khoá>/Lxx_*.yaml      # lint → giọng → khung hình → mp4 → verify
python tools/lv.py asr      lessons/<khoá>/Lxx_*.yaml      # máy nghe lại giọng đọc
python tools/lv.py curriculum curriculum/<khoá>.yaml
bash audit/review/audit_final/final_gates_af2.sh > audit/review/audit_final/logs/gates_af2.out 2>&1   # cổng toàn kho (chạy nền, MỘT bản)
python audit/review/lab_gate.py [KHOÁ]                      # mọi lab chạy lời giải và so kết quả
python audit/review/learn_start/pack.py page                # sinh lại HOC_TAP.html / HOC_TAP.md / xem.html
python tools/lv.py new-course <KHOÁ> --title "…"            # khoá mới (xem references/new-domain.md)
```
Cài môi trường máy mới: `python -m venv .venv` rồi `.venv/Scripts/python -m pip install -r requirements.txt`; `cd tools/vendor && npm install katex@0.16.11`.

## Giọng đọc và quyền riêng tư
Mọi bài dùng giọng `vi-VN-NamMinhNeural` (một bài một giọng, một khoá một giọng; dự phòng chỉ đổi cho cả bài). Giọng dùng dịch vụ trực tuyến edge-tts: nội dung câu đọc được gửi tới máy chủ Microsoft.
Phát âm được kiểm bằng máy nghe (ASR), **chưa có người nghe**: câu bị gắn cờ ghi `NOT_VERIFIED bằng tai người`.

## Hiện trạng và việc còn mở
Xem đầu `HANDOVER.md` và `audit/review/audit_final/STATE.md`.
