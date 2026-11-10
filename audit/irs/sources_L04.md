# Nguồn bài IRS L04 — Truy hồi lai và hợp nhất thứ hạng

Đọc nguyên văn ngày 2026-11-03 (pdftotext).

## [CO09] G. V. Cormack, C. L. A. Clarke, S. Büttcher — Reciprocal Rank Fusion outperforms Condorcet and individual Rank Learning Methods. SIGIR 2009 (bài ngắn 2 trang).
URL: https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf (trang của tác giả, Đại học Waterloo)
- "Reciprocal Rank Fusion (RRF), a simple method for combining the document rankings from multiple IR systems, consistently yields better results than any individual system, and better results than the standard method Condorcet Fuse."
- "RRFscore(d ∈ D) = Σ_{r∈R} 1/(k + r(d)) where k = 60 was fixed during a pilot investigation and not altered during subsequent validation."
- "while highly-ranked documents are more important, the importance of lower-ranked documents does not vanish as it would were, say, an exponential function used. The constant k mitigates the impact of high rankings by outlier systems."
- "The results of the first, shown in table 1, indicated that k = 60 was near-optimal, but that the choice was not critical."
- "unsupervised methods are attractive because they require no training examples."
- "The pilot and TREC experiments indicate that RRF outperforms Condorcet, CombMNZ and the best system by 4% to 5% on average."

## Phần nền giảng lại trong bài (đợt C, 2026-11-09 — bài tự đứng được)
- Công thức xếp hạng có bão hoà (BM25): S. Robertson, H. Zaragoza, The Probabilistic Relevance Framework: BM25 and Beyond, Foundations and Trends in IR 3(4), 2009 — điểm = Σ theo từ câu hỏi của độ hiếm · f·(k1 + 1)/(f + k1·(1 − b + b·dl/avdl)); k1, b là tham số tự do, giá trị 1,2 và 0,75 là lựa chọn thường gặp. Bài dùng độ hiếm dạng ln(1 + (N − n + 0,5)/(n + 0,5)) (luôn dương; dạng gốc không có “1 +” có thể âm khi từ có ở hơn nửa số văn bản) — cùng hàm `alg.bm25_idf` / `alg.bm25`. Đối chiếu nội dung, không trích nguyên văn trong đợt này. Ví dụ “mèo” (0,646 / 0 / 0,414) là số minh hoạ, tính lại ở verify_parts/L04.py (L04k, L04l).
- Cosin: tích vô hướng chia tích hai độ dài, nằm trong [−1; 1]; vector trọng số không âm cho [0; 1] (Manning–Raghavan–Schütze 2008, mục 6.3). Ví dụ 0,956 kiểm ở L04m.
- Sửa đợt C: bài cũ ghi “cosin luôn từ 0 tới 1” cho cả vector nhúng (sai: vector nhúng có thành phần âm, cosin có thể âm) và “điểm từ khoá không có trần” (với một câu hỏi cố định, mỗi từ góp tối đa độ hiếm · (k1 + 1); đúng hơn là không có trần chung giữa các câu hỏi).
