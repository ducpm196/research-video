# Lab IRS L02 — Mô hình không gian vector TF-IDF và cosin

Đọc từ đầu vào chuẩn (`stdin`) gồm 6 dòng: 3 dòng đầu `d1=...`, `d2=...`, `d3=...` là ba văn bản (các từ cách nhau khoảng trắng), dòng 4 là câu hỏi `q=...`, dòng 5 là `w1=<từ1>` và dòng 6 là `w2=<từ2>`. Tính `IDF = ln(N / df)` cho hai từ cần in và tính độ tương đồng cosin TF-IDF giữa câu hỏi `q` với `d2`, `d3`.

In 1 dòng đúng nhãn (`<.1f>` làm tròn 1 chữ số thập phân, `<.3f>` làm tròn 3 chữ số): `idf_xe=<.1f> idf_dien=<.3f> cos_d2=<.3f> cos_d3=<.3f>`.
Chấm tự động: `bash labs/cham.sh IRS L02 duong_dan/bai_cua_ban.py`
