# Nguồn bài IRS L03 — Truy hồi dày và tìm láng giềng gần đúng

Đọc nguyên văn ngày 2026-11-03 (pdftotext; ar5iv cho ký hiệu căn bị mất khi trích chữ).

## [JO17f] J. Johnson, M. Douze, H. Jégou — Billion-scale similarity search with GPUs. arXiv 1702.08734 (2017).
URL: https://arxiv.org/pdf/1702.08734 ; https://ar5iv.labs.arxiv.org/html/1702.08734
- "For IVFADC the search is not exhaustive. Vectors for which the distance is computed are pre-selected depending on the first-level quantizer q1"
- "The multi-probe parameter τ is the number of coarse-level centroids we consider."
- "The corresponding data structure, the inverted file, groups the vectors y_i into |C1| inverted lists I1, ..., I|C1| with homogeneous q1(y_i)."
- "We typically use |C1| ≈ √ℓ, trained via k-means." (ℓ = số vector trong kho; ar5iv giữ mã LaTeX \sqrt{\ell})
- "They obtain a nearest neighbor recall at 1 (fraction of queries where the true nearest neighbor is in the top 1 result) of R@1 = 0.51"
- "Our implementation enables the construction of a high accuracy k-NN graph on 95 million images from the Yfcc100M dataset in 35 minutes, and of a graph connecting 1 billion vectors in less than 12 hours on 4 Maxwell Titan X GPUs."

## [MA16] Yu. A. Malkov, D. A. Yashunin — Efficient and robust approximate nearest neighbor search using Hierarchical Navigable Small World graphs. arXiv 1603.09320.
URL: https://arxiv.org/pdf/1603.09320
- "The quality of an inexact search (the recall) is defined as the ratio between the number of found true nearest neighbors and K."
- "Hierarchical NSW incrementally builds a multi-layer structure consisting from hierarchical set of proximity graphs (layers) for nested subsets of the stored elements."
- "a new fully graph based incremental K-ANNS structure, which can offer a much better logarithmic complexity scaling."

## [CO16] Covington, Adams, Sargin (RecSys 2016) — URL ở sources_L13.md.
- "Scoring millions of items under a strict serving latency of tens of milliseconds requires an approximate scoring scheme sublinear in the number of classes."
- "the scoring problem reduces to a nearest neighbor search in the dot product space for which general purpose libraries can be used [12]. We found that A/B results were not particularly sensitive to the choice of nearest neighbor search algorithm."

## Không dạy
- Số đo tốc độ cụ thể của thư viện trên phần cứng cụ thể (phụ thuộc máy); bài dùng số minh hoạ cho thời gian; số phép so tính lại được.
