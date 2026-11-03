# Nguồn bài IRS L05 — Học để xếp hạng: theo điểm, theo cặp, theo danh sách

Đọc nguyên văn ngày 2026-11-03 (pdftotext).

## [BU05] C. Burges, T. Shaked, E. Renshaw, A. Lazier, M. Deeds, N. Hamilton, G. Hullender — Learning to Rank using Gradient Descent. ICML 2005.
URL: https://icml.cc/Conferences/2015/wp-content/uploads/2015/06/icml_ranking.pdf
- "We investigate using gradient descent methods for learning ranking functions; we propose a simple probabilistic cost function, and we introduce RankNet, an implementation of these ideas using a neural network to model the underlying ranking function."
- "In the training phase, some query/document pairs are labeled for relevance ("excellent match", "good match", etc.). Only those documents returned for a given query are to be ranked against each other." (dùng cho lỗi 2 của bài)
- "We consider models where the learning algorithm is given a set of pairs of samples [A, B] in R^d, together with target probabilities P̄_AB that sample A is to be ranked higher than sample B."
- "Define o_i ≡ f(x_i) and o_ij ≡ f(x_i) − f(x_j). We will use the cross entropy cost function C_ij ≡ C(o_ij) = −P̄_ij log P_ij − (1 − P̄_ij) log(1 − P_ij) (1) where the map from outputs to probabilities are modeled using a logistic function P_ij ≡ e^{o_ij} / (1 + e^{o_ij}) (2)"
- "C_ij then becomes C_ij = −P̄_ij o_ij + log(1 + e^{o_ij}) (3)" ; "Note that C_ij asymptotes to a linear function; for problems with noisy labels this is likely to be more robust than a quadratic cost."
- "when P̄_ij = 1/2 (when no information is available as to the relative rank of the two patterns), C_ij becomes symmetric, with its minimum at the origin."
- "For each query, one or more of the returned documents had a manually generated rating, from 1 (meaning 'poor match') to 5 (meaning 'excellent match'). Unlabeled documents were given rating 0. Ranking accuracy was computed using a normalized discounted cumulative gain measure (NDCG)"
- "We shuffled the data and used 2/3 (11,336 queries) for training and 1/6 each (2,834 queries) for validation and testing."

## [ZH19] Zhao và cộng sự (RecSys 2019) — URL ở sources_L13.md.
- "This approach of making predictions for each candidate is a pointwise approach [6]. In contrast, pair-wise or list-wise approaches learn to make predictions on ordering of two or multiple candidates."

## [CO16] Covington và cộng sự (RecSys 2016) — URL ở sources_L13.md.
- Bảng 1 đo “weighted, per-user loss”: "If the negative impression receives a higher score than the positive impression, then we consider the positive impression's watch time to be mispredicted watch time."

## Ghi chú toán
- Với P̄ = 1 (a chắc chắn hơn b), công thức (3) thành C = −o + ln(1 + e^{o}) = ln(1 + e^{−o}), o = s_a − s_b — đúng dạng giáo án; kiểm bằng máy ở verify_parts/L05.py.
- “Theo danh sách” (LambdaRank, ListNet…): KHÔNG có bài báo đã đọc → chỉ dạy ý (trọng số theo thay đổi nDCG khi đổi chỗ) như một cách làm, không gán tên, năm, con số (NOT_VERIFIED).
