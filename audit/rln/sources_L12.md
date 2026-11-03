# Nguồn bài RLN L12 — tình huống: đánh giá chính sách mới từ nhật ký cũ

Đọc 2026-11-02.

**[B13]** L. Bottou, J. Peters, J. Quiñonero-Candela, D. X. Charles, D. M. Chickering, E. Portugaly, D. Ray, P. Simard, E. Snelson,
*Counterfactual Reasoning and Learning Systems: The Example of Computational Advertising*, Journal of Machine Learning Research 14
(2013) 3207–3260. PDF chính thức của tạp chí: `https://jmlr.org/papers/volume14/bottou13a/bottou13a.pdf` (WebFetch trả nhị phân → lưu,
trích chữ bằng pdftotext). Đây là bài viết của chính nhóm vận hành hệ thống đặt quảng cáo (dữ liệu Bing).
**[SB18]** Sutton & Barto, bản 2 (2018), mục 5.5 — PDF chính thức (xem sources_L00.md).

| Nguồn, mục | Câu trích nguyên văn | Dùng ở |
|---|---|---|
| [B13] 2.2 | “The basic idea is to randomly split the users into treatment and control groups (Kohavi et al., 2008). … Monitoring various performance metrics for a couple months usually gives sufficient information to reliably decide which variant of the system delivers the most satisfactory performance.” | hook (“thường mất vài tháng”) |
| [B13] 2.2 | “They are slow because each experiment typically demands a couple months.” | hook |
| [B13] 4.3 | “Importance sampling relies on the assumption that all the factors appearing in the denominator of the reweighting ratio (6) are nonzero whenever the factors appearing in the numerator are nonzero. … this assumption means that the data must be collected with an experiment involving active randomization.” | sai 1 |
| [B13] 4.4 | “Unfortunately, when P(ω) is small, the reweighting ratio w(ω) takes large values with low probability. This heavy tailed distribution has annoying consequences because the variance of the integrand could be very high or infinite.” ; “Importance sampling works best when the actual distribution and the counterfactual distribution overlap.” | ví dụ (trọng số 9, 1024), sai 2 |
| [B13] 4.4 | “When the counterfactual distribution has significant mass in domains where the actual distribution is small, the few samples available in these domains receive very high weights. Their noisy contribution dominates the reweighted estimate (7).” | sai 2 (“lấn át”) |
| [B13] 4.4 | “Let us choose the maximum weight value R deemed acceptable for the weights. We have obtained very consistent results in practice with R equal to the fifth largest reweighting ratio observed on the empirical data.” ; “The resulting bias can be bounded using prior knowledge, for instance with an assumption about the range of values taken by ℓ(ω)” | sai 3 (cắt có điều kiện) |
| [B13] 4.6 | “The main treatment bucket was processed with mainline reserves randomized by a multiplier drawn as explained above with μ = 1 and σ = 0.3. With these parameters, the mean multiplier is exactly 1, and 95% of the multipliers are in range [0.52, 1.74]. Samples describing 22 million search result pages were collected during five consecutive weeks.” | hook (22 triệu trang, năm tuần), sai 1 (0,52 tới 1,74) |
| [B13] 4.6 | “In order to validate the accuracy of these counterfactual estimates, a second traffic bucket of equal size was configured with mainline reserves reduced by about 18%. … The effective measurements and the counterfactual estimates match with high accuracy.” | sai 4 |
| [SB18] 5.5, (5.5) (5.6) | “When importance sampling is done as a simple average in this way it is called ordinary importance sampling. An important alternative is weighted importance sampling, which uses a weighted average” | ký hiệu (hai ước lượng) |
| [SB18] 5.5 | “Ordinary importance sampling is unbiased whereas weighted importance sampling is biased (though the bias converges asymptotically to zero). On the other hand, the variance of ordinary importance sampling is in general unbounded because the variance of the ratios can be unbounded” | tự kiểm 1 (ước lượng thường đúng trung bình), sai 3 (có trọng số cũng lệch) |
| [SB18] Ví dụ 5.5 | “Even after millions of episodes, the estimates fail to converge to the correct value of 1.” | (bối cảnh phương sai vô hạn; bài không đọc số) |

## Điều KHÔNG dạy (nguồn không ghi)
- Nhật ký 10 lượt (0,9 / 0,1; lợi nhuận 1 / 2), lượt chơi 10 bước trọng số 2 mỗi bước, nhật ký 1000 lượt, các số trong câu đố
  (ESS = 3 trên 10 000 lượt, “tăng 20%”) là SỐ MINH HOẠ, tính bằng checks và verify_parts/L12.py.
- [B13] không dùng công thức số mẫu hiệu dụng (Σw)² / Σw²; bài dạy nó như một phép đo tự kiểm thường dùng, không gán cho nhóm tác giả.
- Không nêu doanh thu, lượt nhấp cụ thể của hệ thống (Hình 13 của [B13]); không nêu tên người.
- Không gọi tên công ty trong lời đọc; trên màn hình chỉ ghi tên bài báo trong `source`.
