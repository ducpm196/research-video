# Nguồn bài CVI L05 — ước lượng bền vững bằng bốc mẫu ngẫu nhiên

Đọc 2026-11-03 (curl + pdftotext; bản tải ở scratchpad `cvi_work/src/fb.pdf`, 13 trang chụp của bản in, văn bản trích có lỗi nhận dạng
chữ nhỏ — câu trích dưới đây đã đối chiếu, lỗi nhận dạng giữ trong ngoặc vuông nếu có).

**[FB81]** M. A. Fischler, R. C. Bolles, “Random Sample Consensus: A Paradigm for Model Fitting with Applications to Image Analysis
and Automated Cartography”, Communications of the ACM 24(6), 6/1981, tr. 381–395 (siêu dữ liệu Crossref DOI 10.1145/358669.358692).
Bản đọc: bản PDF do SRI International (nơi tác giả làm việc) lưu, https://www.sri.com/wp-content/uploads/2021/12/ransac-publication.pdf

| Mục | Câu trích nguyên văn | Dùng ở |
|---|---|---|
| I | “Classification errors, however, are gross errors, having a significantly larger effect than measurement errors, and do not average out.” | lỗi 1 |
| II | “Rather than using as much of the data as possible to obtain an initial solution and then attempting to eliminate the invalid data points, RANSAC uses as small an initial data set as feasible and enlarges this set with consistent data when possible.” | tiêu đề thủ tục “ít điểm nhất có thể” |
| II | “randomly select a subset S1 of n data points from P and instantiate the model. Use the instantiated model M1 to determine the subset S1* of points in P that are within some error tolerance of M1. The set S1* is called the consensus set of S1.” | bảng thủ tục bước 1–3 |
| II | “use S1* to compute (possibly using least squares) a new model M1*.” … “If, after some predetermined number of trials, no consensus set with t or more members has been found, either solve the model with the largest consensus set found, or terminate in failure.” | bước 4 (giữ tập lớn nhất, làm lại bình phương tối thiểu) |
| II.A | “The error tolerance could then be set at one or two standard deviations beyond the measured average error.” | lỗi 3 |
| II.B | “Let w be the probability that any selected data point is within the error tolerance of the model.” … “E(k) = 1/b = w^-n” | ký hiệu w; trung bình 16 lần (w = 0,5, n = 4) |
| II.B | “if we want to ensure with probability z that at least one of our random selections is an error-free set of n data points, then we must expect to make at least k selections (n data points per selection), where (1 − b)^k = (1 − z), k = [log(1 − z)]/[log(1 − b)].” | công thức N (bài viết s cho n, p cho z — ghi ở notation_note) |
| II.B | “For example, if (w = 0.5) and (n = 4), then (b = 1/16). To obtain a 90 percent assurance of making at least one error-free selection, k = log(0.1)/log(15/16) = 35.7.” | ví dụ bước 4 (tính lại: 35,68 → 36) |

## Điều KHÔNG dạy (nguồn không ghi / số minh hoạ)
- Đường thẳng 8 điểm, ngưỡng 0,5, các tỉ lệ đúng 0,3 / 0,4 / 0,6 / 0,7, ứng dụng thời gian thực 100 lần bốc mỗi khung là SỐ MINH HOẠ.
- “Lọc bằng phép thử tỉ số nâng w từ 0,3 lên 0,5” là giả định minh hoạ (nối bài 4), không phải số đo của bài báo nào.
- Bài không nêu tên phép biến đổi “homography”; chỉ nói “phép biến đổi giữa hai ảnh của một mặt phẳng cần 4 điểm” (Hartley–Zisserman chưa đọc → không trích).
- Tên tác giả chỉ trên màn hình; lời đọc nói “hai nhà nghiên cứu công bố năm 1981”.
