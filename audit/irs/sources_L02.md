# Nguồn bài IRS L02 — Mô hình không gian vector: TF-IDF và độ tương tự cosin

Bài chủ yếu là toán (định nghĩa trọng số và cosin), kiểm bằng `checks` và audit/irs/verify_parts/L02.py. Phần đã dạy ở khoá khác trỏ bằng
requires_ext: DEN bài 7 (chỉ mục ngược, công thức xếp hạng có bão hoà và phạt độ dài), LLM bài 3 (cosin của vector nhúng).

## NOT_VERIFIED
- Manning, Raghavan, Schütze, Introduction to Information Retrieval (2008), mục 6.2–6.3 (idf = log N/df, tf-idf, cosin): nlp.stanford.edu không kết nối được ngày 2026-11-03 (hết giờ cổng 443), web.archive.org trả 429 → bài KHÔNG trích câu của sách; chỉ dạy định nghĩa toán (máy tự kiểm) và ghi tên sách ở `source` như sách tham khảo (CITED trong giáo án từ trước).

## Sửa 2026-11-09 (đợt đọc kiểm C — bài tự đứng được)
- Bỏ câu nhắc tên khoá khác ở màn hình và lời đọc; ôn nền (lôgarit tự nhiên, tích vô hướng, độ dài, cosin) giảng lại trong cảnh `prereq`,
  bằng ví dụ số tự kiểm (`checks` + verify_parts/L02.py L02j). Hai dòng `requires_ext` trong giáo án giữ nguyên làm chú thích nội bộ.
- Lỗi 2: thay “công thức có cộng thêm hằng số như ở khoá …” bằng một công thức làm trơn cụ thể ln((N + 1)/(df + 1)) — là phép biến đổi
  toán tự kiểm được (sạc: ln 4 ≈ 1,386; máy: ln 1 = 0), bài trình bày như “một công thức làm trơn”, KHÔNG gán cho một thư viện cụ thể
  (scikit-learn `TfidfTransformer(smooth_idf=True)` dùng dạng gần giống nhưng cộng thêm 1 bên ngoài lôgarit — không mở lại tài liệu ngày này).
- Lỗi 4: giảng bão hoà tần suất bằng hàm tf/(tf + k) với k = 1 (số minh hoạ). Dạng tf/(k + tf) là hàm bão hoà mà S. Robertson,
  H. Zaragoza, “The Probabilistic Relevance Framework: BM25 and Beyond”, Foundations and Trends in IR 3(4), 2009, mục 3 dùng để dẫn
  tới BM25 — NOT_VERIFIED nguyên văn (chưa mở lại PDF ngày 2026-11-09); bài chỉ dạy tính chất toán (tăng dần, không vượt 1), máy tự kiểm (L02k).
