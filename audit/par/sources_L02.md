# Nguồn PAR L02 — công việc, đường găng, cận lịch tham lam (đọc nguyên văn 2026-11-02)

## [BR74] R. P. Brent, “The Parallel Evaluation of General Arithmetic Expressions”, JACM 21(2), 1974, 201–206
Bản tác giả: https://maths-people.anu.edu.au/~brent/pd/rpb022.pdf (curl + pdftotext, 6 trang, đọc được).

- Mô hình: “We assume that a number of processors are available and that each can perform an arithmetic operation (addition,
  multiplication, and sometimes division) in unit time. The time required for accessing data, storing results, communicating between
  processors, etc., is ignored.” → bài dạy: mỗi phép cộng 1 bước; Lỗi 4 “mô hình bỏ qua đọc dữ liệu và trao đổi giữa các bộ xử lý”.
- “LEMMA 2. If a computation C can be performed in time t with q operations and sufficiently many processors which perform arithmetic
  operations in unit time, then C can be performed in time t + (q − t)/p with p such processors.”
  → bài dạy: T_n ≤ T∞ + (T₁ − T∞)/n (t = T∞, q = T₁, p = n của khoá); dạng gọn T₁/n + T∞ lớn hơn (vì T∞ ≥ T∞/n).
- Cận dưới cho phép cộng n số: “Consider the expression x1 + x2 + ... + xn. By a fan-in argument, its evaluation requires time at least
  log2 n. Also, at least n − 1 operations must be performed, so p processors require time at least (n − 1)/p.”
  → bài dạy: T∞ = 10 = log2 1024, T₁ = 1023 = n − 1, cận dưới max(T₁/n, T∞).

## [OW05] J. Owens và cộng sự, A Survey of General-Purpose Computation on Graphics Hardware, Eurographics 2005 STAR
https://research.nvidia.com/sites/default/files/pubs/2005-08_A-Survey-of/ASurveyofGeneralPurposeComputationonGraphicsHardware.pdf
- “On each rendering pass, the size of the output, the computational range, is reduced by one half. In general, we can compute a
  reduction over a set of data in O(log n) steps using the parallel GPU hardware, compared to O(n) steps for a sequential reduction on
  the CPU.” → chỉ dùng làm nguồn đối chiếu (cộng theo cặp, mỗi lượt giảm một nửa); không đọc tên trong lời.

## Số minh hoạ (không có nguồn, ghi rõ trên màn hình)
- Máy 16 lõi và máy 64 lõi giá gấp 4 (quiz); 1 bước đồng bộ thêm mỗi tầng (Lỗi 4).

## Điều KHÔNG dạy (nguồn không ghi / không đọc được)
- Không gán cận T₁/n + T∞ cho riêng Brent: Lemma 2 ghi dạng t + (q − t)/p; dạng gọn gọi là “dạng hay gặp”. Không nhắc Graham (1969)
  vì chưa đọc nguyên văn.
- Không nói lịch tham lam theo tầng là tối ưu cho mọi đồ thị; chỉ nói nó nằm giữa hai cận (bài kiểm vét hết lịch cho cây 8 số / 2 lõi).
- Bài báo work stealing (Blumofe–Leiserson) không tải được (trang trả HTML), không dùng.
