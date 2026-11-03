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

## Liên hệ khoá khác
- Công thức xếp hạng có bão hoà (BM25) và chỉ mục ngược: DEN bài 7 (Robertson & Zaragoza 2009) — không dạy lại.
- Cosin của vector nhúng: LLM bài 3.
