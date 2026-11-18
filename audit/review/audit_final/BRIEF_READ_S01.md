# BRIEF_READ_S01 — đọc độc lập Chặng 1 (FND, JVA, JV2) để chốt "bắt đầu học" — 2026-11-13

Người học: **mất gốc, chưa từng lập trình**, chỉ có video + thư mục `labs/`. Tiêu chí = `audit/review/sample_f/BRIEF.md` (Phần A chuẩn xác, Phần B P1–P7) + `audit/review/audit_final/ADDENDUM.md` (P8 thực nghiệm, P9 quy mô/thời gian, cột "Cần biết trước", mục "Người học kẹt ở đâu"). ĐỌC CẢ HAI TỆP TRƯỚC.

## Khác với BRIEF mẫu F
- Đọc **TRỌN mọi bài được giao** (không chỉ một bài mỗi khoá).
- **Được chạy lab**: với mỗi bài có `labs/<KHOÁ>/<Lxx>/`, làm như người học: đọc `de.md`, tự viết lời giải trong thư mục tạm ở scratchpad (không nhìn `loi_giai.*` trước), chấm bằng `bash D:/research-video/labs/cham.sh <KHOÁ> <Lxx> <tệp>`; sau đó so với `loi_giai.*`. Ghi: đề đủ để tự làm chưa? thiếu kiến thức gì? kết quả mong đợi trên màn hình khớp `mong_doi.txt` không? Dùng Git Bash (`bash`), JDK 21, `.venv/Scripts/python`.
- Vẫn **không sửa/tạo tệp trong `D:\research-video`**, không chạy `build`/`tts`/`asr`/`render`/`gen.py`/git/docker. Ngoại lệ DUY NHẤT: được ghi báo cáo cuối vào `D:/research-video/audit/review/audit_final/reports/<tên tệp được giao>`.
- Không mở báo cáo cũ: `audit/review/full_review_*`, `sample_*/REPORT.md`, `audit/review/audit_final/reports/*` (trừ tệp của chính bạn), `audit/review/audit_final/handover_*`, `plan_*`.
- Ghi sha16 của mỗi YAML lúc đọc.

## Báo cáo
Ghi vào tệp được giao (và trả lại trong tin nhắn cuối bản rút gọn ≤ 40 dòng):
1. `# S01 <phần>: đã đọc K/K bài`.
2. Bảng chuẩn xác (như BRIEF mẫu F) — chỉ lỗi có bằng chứng.
3. Bảng độ sâu một dòng mỗi bài: `Bài | sha16 | Phút | P1…P7 | P8 | P9 | Tổng(P1–P7) | Mất gốc | Cần biết trước | Chỗ thiếu chính`.
4. **Lab**: bảng `Bài | tự làm được (có/không/phần) | thời gian | kẹt ở đâu | mong_doi khớp màn hình`.
5. **Người học kẹt ở đâu**: một dòng mỗi bài.
6. Số đã tính lại / mã đã chạy: bao nhiêu, bao nhiêu khớp.
7. Khung hình đã xem (≥ 5 mỗi bài) và lỗi hiển thị.
8. Nhận xét chung ≤ 8 gạch.
Ngưỡng chốt của kế hoạch: MUST 0; P1 = 2 ≥ 90%; P8 = 2 = 100%.
