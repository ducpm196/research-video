# Lab IRS L11 — Cân bằng độ liên quan với độ đa dạng (MMR)

Đọc từ đầu vào chuẩn (`stdin`, dạng `khoá=giá_trị`) năm số thực `lam=<f> rx=<f> sx=<f> ry=<f> sy=<f>`. Tính `lam * rel - (1 - lam) * sim` cho hai ứng viên `X`, `Y` và chọn bên điểm cao hơn (hoà lấy `Y` nếu `my > mx` hoặc so đúng `X if mx >= my else Y`).

In 1 dòng đúng nhãn (`<.3f>` làm tròn 3 chữ số thập phân, `<X|Y>` in chữ cái `X` hoặc `Y`): `mmr_X=<.3f> mmr_Y=<.3f> pick=<X|Y>`.
Chấm tự động: `bash labs/cham.sh IRS L11 duong_dan/bai_cua_ban.py`
