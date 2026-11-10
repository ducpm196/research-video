# Nguồn bài IRS L10 — Thiên lệch vị trí: đánh giá ngoại tuyến bằng trọng số nghịch đảo xu hướng

Đọc nguyên văn ngày 2026-11-03 (pdftotext).

## [JO17] T. Joachims, A. Swaminathan, T. Schnabel — Unbiased Learning-to-Rank with Biased Feedback. WSDM 2017 (arXiv 1608.04468).
URL: https://arxiv.org/pdf/1608.04468
- "For example, position bias in search rankings strongly influences how many clicks a result receives, so that directly using click data as a training signal in Learning-to-Rank (LTR) methods yields sub-optimal results."
- "Our approach uses inverse propensity scoring (IPS), originally employed in causal inference from observational studies"
- "This is an unbiased estimate ... if Q(o_i(y) = 1 | x_i, ȳ_i, r_i) > 0 for all y that are relevant"
- "In this model, examination depends only on the rank of y in ȳ. So, P(e_i(y) = 1 | rank(y|ȳ_i)) can be represented by a vector of examination probabilities p_r, one for each rank r."
- "it suffices to estimate the p_r up to some positive multiplicative constant, since any such constant does not change how the IPS estimator (5) orders different systems."
- "we collect new click data via randomized interventions for 7 days ... with landmark rank k = 1. Before presenting the ranking, we take the top-ranked document and swap it with the document at a uniformly at random chosen rank j ∈ {1, . . . 21}. The ratio of observed click-through rates (CTR) on the formerly top-ranked document now at position j vs. its CTR at position 1 gives a noisy estimate of p_j/p_1"
- "This yields p_r that approximately decay with rank r with the smallest p_r ≈ 0.12."
- "the increased variance of R̂_IPS(S) can be a drawback for small datasets. ... This can be remedied using techniques like "propensity clipping" [23], where small propensities are clipped to some threshold value τ to trade bias for variance."

## [ZH19] Zhao và cộng sự (RecSys 2019) — URL ở sources_L13.md.
- "users are inclined to clicking and watching videos displayed closer to the top of the list, regardless of their actual user utility"
- "Figure 6 shows the distribution of CTR in relative scale for position 1 to 9. As expected, we see a significantly lower CTR as position gets lower and lower. The higher CTRs at higher positions are due to a combination effect of recommending more relevant items and position bias."

## [CH19] Chen và cộng sự (WSDM 2019) — URL ở sources_L13.md.
- "Smaller value of c reduces variance in the gradient estimate, but introduces larger bias." ; cắt c = 3, nới lên 5 → "a significant drop of 0.52% in ViewTime".

## [CO16] Covington và cộng sự (RecSys 2016)
- "live A/B results are not always correlated with offline experiments."

## Liên hệ khoá khác
- Biến gây nhiễu, nghịch lý Simpson: DSC bài 7; thử nghiệm hai nhóm: DSC bài 8, DAN.
- Đợt C (2026-11-09): bài nay TỰ GIẢNG lại, không nhắc khoá khác: xác suất, độc lập, kỳ vọng (phần ôn ①); biến gây nhiễu bằng một nhật ký
  minh hoạ theo vị trí có đảo chiều khi gộp (B thắng từng vị trí, A thắng gộp: 0,022 so với 0,0127 — kiểm ở verify_parts/L10.py L10i;
  không gọi tên “Simpson” trong lời đọc); thử nghiệm hai nhóm (chia ngẫu nhiên, đối chứng/thử) ở đầu cảnh `online`; độ lệch chuẩn, thiên lệch
  ở cảnh `check`; đặc trưng, tháp nông ở cảnh `online`.

## Đọc lại 2026-11-09 (đợt C, pdftotext bản `daiwk.github.io/assets/youtube-multitask.pdf`)
- [ZH19] mục 5.4.3: "Besides position bias, there are many other types of biases. Some of these biases may be unknown and unpredictable" (khớp câu “ngoài vị trí còn nhiều thiên lệch khác, có cái chưa biết”).
- [ZH19] Bảng 2 chỉ ghi "Engagement Metric": Input Feature −0.07% / Adversarial Loss +0.01% / Shallow Tower +0.24%; bài báo không ghi rõ chữ “relative” —
  bài giảng đọc là thay đổi so với hệ gốc trong thử nghiệm (cách đọc thông thường), không nêu con số tuyệt đối.
