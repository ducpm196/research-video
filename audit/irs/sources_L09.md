# Nguồn bài IRS L09 — Khởi động lạnh và khám phá trong gợi ý

Đọc nguyên văn ngày 2026-11-03 (pdftotext).

## [CL11] O. Chapelle, L. Li — An Empirical Evaluation of Thompson Sampling. NIPS 2011.
URL: https://proceedings.neurips.cc/paper/2011/file/e53a0a2978c28872a4505bdb51db06dc-Paper.pdf
- "Thompson sampling is one of oldest heuristic to address the exploration / exploitation trade-off, but it is surprisingly unpopular in the literature. ... it is highly competitive. And since this heuristic is very easy to implement, we argue that it should be part of the standard baselines to compare against."
- "The idea of Thompson sampling is to randomly draw each arm according to its probability of being optimal."
- "It is standard to model the mean reward of each arm using a Beta distribution since it is the conjugate distribution of the binomial distribution."
- Thuật toán 2: "S_i = 0, F_i = 0 ... Draw θ_i according to Beta(S_i + α, F_i + β). ... Draw arm î = arg max_i θ_i and observe reward r ; if r = 1 then S_î = S_î + 1 else F_î = F_î + 1"
- "The initial prior distribution is Beta(1,1)."
- "the feedback is typically not processed immediately because of various runtime constraints. Instead it usually arrives in batches over a certain period of time."
- Quảng cáo hiển thị: "About 13,000 contexts, representing a small random subset of the total traffic, are presented every hour to the policy"

## [BA08] Baluja và cộng sự (WWW 2008) — URL ở sources_L13.md.
- "This suggests that for very casual users (who visit a system infrequently), recommending the most popular videos is a useful strategy."
- "we require that videos and users exist on YouTube during the training and testing phases of the recommendation systems in order to be counted in the evaluation. In deployment, this restriction will not be necessary; all models will be continuously updated."

## [CO16] Covington và cộng sự (RecSys 2016)
- "Many hours worth of videos are uploaded each second to YouTube. Recommending this recently uploaded ("fresh") content is extremely important for YouTube as a product."
- "Demographic features are important for providing priors so that the recommendations behave reasonably for new users."
- "Otherwise, it would be very difficult for new content to surface and the recommender would be overly biased towards exploitation."

## [CH19] Chen và cộng sự (WSDM 2019) — URL ở sources_L13.md.
- "brute-force exploration, such as ε-greedy, is not viable in a production system like YouTube"
- "we observe a statistically significant increase in ViewTime by 0.07% ... (only 5% of users experience the stochastic policy)."

## Liên hệ khoá khác
- Kẻ cướp nhiều tay, ε-tham lam, cận trên tin cậy: RLN bài 3 — chỉ ôn, không dạy lại.
