# Nguồn bài IRS L08 — Phản hồi ngầm, lấy mẫu âm và thiên lệch phổ biến

Đọc nguyên văn ngày 2026-11-03 (pdftotext).

## [HU08] Y. Hu, Y. Koren, C. Volinsky — Collaborative Filtering for Implicit Feedback Datasets. ICDM 2008.
URL: http://yifanhu.net/PUB/cf.pdf
- "1. No negative feedback. By observing the users behavior, we can infer which items they probably like and thus chose to consume. However, it is hard to reliably infer which items a user did not like. For example, a user that did not watch a certain show might have done so because she dislikes the show or just because she did not know about the show or was not available to watch it."
- "3. The numerical value of explicit feedback indicates preference, whereas the numerical value of implicit feedback indicates confidence."
- "c_ui = 1 + α·r_ui ... The rate of increase is controlled by the constant α. In our experiments, setting α = 40 was found to produce good results."
- "a user may watch a TV show just because she is staying on the channel of the previously watched show. Or a consumer may buy an item as gift for someone else, despite not liking the item for himself."
- "we toggle to zero all entries with r_ui < 0.5, as watching less than half of a program is not a strong indication that a user likes the program."

## [MI13] T. Mikolov, I. Sutskever, K. Chen, G. Corrado, J. Dean — Distributed Representations of Words and Phrases and their Compositionality. NIPS 2013 (arXiv 1310.4546).
URL: https://arxiv.org/pdf/1310.4546
- "We investigated a number of choices for P_n(w) and found that the unigram distribution U(w) raised to the 3/4rd power (i.e., U(w)^{3/4}/Z) outperformed significantly the unigram and the uniform distributions"
- "Our experiments indicate that values of k in the range 5–20 are useful for small training datasets, while for large datasets the k can be as small as 2–5."

## [CO16] Covington và cộng sự (RecSys 2016) — URL ở sources_L13.md.
- "we use the implicit feedback [16] of watches to train the model, where a user completing a video is a positive example. This choice is based on the orders of magnitude more implicit user history available"
- "In practice several thousand negatives are sampled, corresponding to more than 100 times speedup over traditional softmax."
- "generate a fixed number of training examples per user, effectively weighting our users equally in the loss function. This prevented a small cohort of highly active users from dominating the loss."

## [YI19] Yi và cộng sự (RecSys 2019) — URL ở sources_L13.md.
- "popular items are overly penalized as negatives due to the high probability of being included in a batch."
- "s^c(x_i, y_j) = s(x_i, y_j) − log(p_j)" ; "if one item gets sampled every 50 steps, then we have p = 0.02."

## [BA08] Baluja và cộng sự (WWW 2008)
- "Hindsight is not 20/20: ... If the recommendation had been shown, the user might have watched it. The fact that it was not watched may simply be indicate that it was not discovered by the user."
