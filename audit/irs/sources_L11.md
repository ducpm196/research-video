# Nguồn bài IRS L11 — Đa dạng, công bằng và vòng phản hồi của hệ gợi ý

Đọc nguyên văn ngày 2026-11-03 (pdftotext).

## [CG98] J. Carbonell, J. Goldstein — The Use of MMR, Diversity-Based Reranking for Reordering Documents and Producing Summaries. SIGIR 1998.
URL: https://www.cs.cmu.edu/~jgc/publication/The_Use_MMR_Diversity_Based_LTMIR_1998.pdf (trang của tác giả, CMU)
- "The Maximal Marginal Relevance (MMR) criterion strives to reduce redundancy while maintaining query relevance in re-ranking retrieved documents"
- "a document has high marginal relevance if it is both relevant to the query and contains minimal similarity to previously selected documents."
- (công thức) "MMR ≝ Arg max_{D_i ∈ R\S} [ λ (Sim1(D_i, Q) − (1 − λ) max_{D_j ∈ S} Sim2(D_i, D_j)) ]" (bản trích chữ làm hỏng dấu ngoặc; dạng đọc được: λ·liên quan − (1 − λ)·giống nhất với kết quả đã chọn)
- "MMR computes incrementally the standard relevance-ranked list when the parameter λ=1, and computes a maximal diversity ranking among the documents in R when λ=0."
- "Users wishing to sample the information space around the query, should set λ at a smaller value"

## [ZH19] Zhao và cộng sự (RecSys 2019) — URL ở sources_L13.md.
- "models trained using data generated from the current system will be biased, causing a feedback loop effect"

## [CO16] Covington và cộng sự (RecSys 2016)
- "Training examples are generated from all YouTube watches (even those embedded on other sites) rather than just watches on the recommendations we produce. Otherwise, it would be very difficult for new content to surface and the recommender would be overly biased towards exploitation."

## [CH19] Chen và cộng sự (WSDM 2019)
- "the more the behavior policy chooses a sub-optimal item, the more the new policy will be biased toward choosing the same item."

## Liên hệ khoá khác
- Trôi khái niệm, vòng phản hồi, huấn luyện lại: MLO bài 9 — chỉ ôn.
## Không dạy
- Định nghĩa pháp lý hay chỉ số công bằng của một tổ chức cụ thể (chưa đọc nguồn) — “công bằng” chỉ dạy ở mức phơi bày (tỉ lệ hiển thị theo nhóm), số minh hoạ.
