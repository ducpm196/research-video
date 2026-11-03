# Nguồn bài IRS L07 — Phân rã ma trận cho gợi ý

Đọc nguyên văn ngày 2026-11-03 (pdftotext; bản layout để lấy công thức cập nhật).

## [KO09] Y. Koren, R. Bell, C. Volinsky — Matrix Factorization Techniques for Recommender Systems. IEEE Computer 42(8), 2009.
URL: https://datajobs.com/data-science-repo/Recommender-Systems-%5BNetflix%5D.pdf (bản chép; IEEE Xplore cần đăng nhập)
- "characterizing both items and users on, say, 20 to 100 factors inferred from the ratings patterns."
- "each item i is associated with a vector q_i ∈ R^f, and each user u is associated with a vector p_u ∈ R^f."
- "min_{q*, p*} Σ_{(u,i)∈κ} (r_ui − q_i^T p_u)^2 + λ(‖q_i‖^2 + ‖p_u‖^2) (2) Here, κ is the set of the (u,i) pairs for which r_ui is known (the training set)."
- "the system should avoid overfitting the observed data by regularizing the learned parameters, whose magnitudes are penalized. The constant λ controls the extent of regularization and is usually determined by cross-validation."
- "Simon Funk popularized a stochastic gradient descent optimization of Equation 2 ... wherein the algorithm loops through all ratings in the training set. For each given training case, the system predicts r_ui and computes the associated prediction error e_ui = r_ui − q_i^T p_u. Then it modifies the parameters by a magnitude proportional to γ in the opposite direction of the gradient, yielding: q_i ← q_i + γ·(e_ui·p_u − λ·q_i) ; p_u ← p_u + γ·(e_ui·q_i − λ·p_u)"
- "While in general stochastic gradient descent is easier and faster than ALS, ALS is favorable in at least two cases. The first is when the system can use parallelization."
- "suppose that you want a first-order estimate for user Joe's rating of the movie Titanic. Now, say that the average rating over all movies, μ, is 3.7 stars. Furthermore, Titanic is better than an average movie, so it tends to be rated 0.5 stars above the average. On the other hand, Joe is a critical user, who tends to rate 0.3 stars lower than the average. Thus, the estimate for Titanic's rating by Joe would be 3.9 stars (3.7 + 0.5 - 0.3)."
- "much of the observed variation in rating values is due to effects associated with either users or items, known as biases or intercepts, independent of any interactions. For example, typical collaborative filtering data exhibits large systematic tendencies for some users to give higher ratings than others, and for some items to receive higher ratings than others."
- "the more refined factor models, whose descriptions involve more distinct sets of parameters, are more accurate."
- "For comparison, the Netflix system achieves RMSE = 0.9514 on the same dataset, while the grand prize's required accuracy is RMSE = 0.8563."

## [KO09b] Y. Koren, The BellKor Solution to the Netflix Grand Prize (8/2009) — MƯỢN câu trích đã đọc nguyên văn ở audit/dsc/sources_L15.md (khoá DSC)
- §II: "more than 100 million date-stamped movie ratings … m = 480,189 users and n = 17,770 movies". "About 99% of the possible ratings are missing".
- Tính lại (VER trong verify_parts/L07.py): 480 189 · 17 770 = 8 532 958 530 ô; 100 480 507 lượt chấm (DSC sources_L15.md, [TJ09] §2: “the number of ratings is 100480507”) ≈ 1,18% ô; vector 50 chiều (giữa 20 và 100 của [KO09]) cần (480 189 + 17 770) · 50 = 24 897 950 số.

## Liên hệ khoá khác (không dạy lại)
- Cuộc thi 2006–2009, sai số căn quân phương, lịch sử các đội: DSC bài 15.
- SVD và cái bóng dài nhất: CS115 bài 16; bước xuống dốc theo từng mẫu (SGD): CS115 bài 9.
