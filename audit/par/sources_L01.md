# Nguồn PAR L01 — Mở rộng theo cỡ bài toán: định luật Gustafson

Đọc nguyên văn 2026-11-02. Văn bản tải về: scratchpad `par_work/src/gustafson88.pdf` (pdftotext).

## [GU88] J. L. Gustafson, “Reevaluating Amdahl's Law”, Communications of the ACM 31(5), 5/1988, tr. 532–533
- Bản đọc: bản chép lại văn bản (đánh máy lại, chân trang in nhầm “May 1088”) tại
  https://users.cs.utah.edu/~hari/teaching/paralg/Gustafson88.pdf (trang khoá học của University of Utah). Trang tác giả
  johngustafson.net lỗi bắt tay SSL; web.archive.org không tải được từ công cụ; bản quét ACM tại dma.unina.it có trong kết quả tìm
  nhưng chưa mở.
- Câu trích dùng trong bài:
  - “At Sandia National Laboratories, we are currently engaged in research involving massively-parallel processing.”
  - “We now have timing results for a 1024-processor system …”
  - “Yet for three very practical applications (s = 0.4 – 0.8 percent) used at Sandia, we have achieved the speedup factors on a
    1024-processor hypercube which we believe are unprecedented [2]: 1021 for beam stress analysis using conjugate gradients, 1020 for
    baffled surface wave simulation using explicit finite differences, and 1016 for unstable fluid flow using flux-corrected transport.
    How can this be, when Amdahl's argument would predict otherwise?” → hook + câu “bài báo tự hỏi sao lại thế được”.
  - “… in practice, the problem size scales with the number of processors. … Hence, it may be most realistic to assume that run time,
    not problem size, is constant.” → mở rộng yếu.
  - “If we use s' and p' to represent serial and parallel time spent on the parallel system, then a serial processor would require time
    s' + p' x N to perform the task.” → q của bài = s′ (đo trên máy song song).
  - “Scaled speedup = (s' + p' x N) / (s' + p') = s' + p' x N = N + (1 − N) x s'” → công thức G(n) và dạng gom 1024 − 1023·q.
  - “speedup should be measured by scaling the problem to the number of processors, not fixing problem size.”

## Phép tính lại (VER, không phải câu trong nguồn)
- Coi 0,4–0,8% là s′ (đo trên máy 1024 bộ xử lý): N + (1 − N)s′ = 1019,9 và 1015,8 — khớp 1020 và 1016 đã đo. Bài báo không viết
  rõ 0,4–0,8% là s hay s′; bài ghi trên màn hình “đây là phép tính lại của bài, không phải câu trong báo cáo”.
- Amdahl với cùng tỉ lệ (đo trên một lõi): 111 và 201 lần.

## Điều KHÔNG dạy
- Tên người đề xuất công thức trong bài báo (“suggested by E. Barsis at Sandia”) — không cần cho bài, không đọc tên.
- Bài phê bình năm 1996 (Y. Shi) cho rằng hai định luật tương đương — chỉ thấy qua kết quả tìm kiếm, CHƯA đọc nguyên văn (NOT_VERIFIED);
  bài tự chứng minh sự tương đương bằng đổi cách đo (VER, sympy trong verify_parts/L01.py), không dẫn bài 1996.
- Mọi số khác (100 s, 1450 s, bảng 100/102/105/111 s, 5%, 64 lõi, đọc tệp 5 s) là SỐ MINH HOẠ.
