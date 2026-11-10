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

## Đọc kiểm 2026-11-08 (đợt B)
- [CH19] arXiv 1812.02353 (PDF tải lại, pdftotext), mục thử nghiệm khám phá: "we split users on the platform into three buckets: 90%, 5%, 5%." — xác nhận con số 90/5/5 ở lỗi 4.

## Đọc kiểm 2026-11-09 (đợt C)
- [CH19] arXiv 1812.02353 (PDF tải lại, pdftotext), §5: "In practice, brute-force exploration, such as ε-greedy, is not viable in a production system like YouTube where this could, and mostly likely would, result in inappropriate recommendations and a bad user experience." — xác nhận lý do “gợi ý không phù hợp” ở lỗi 2. §6.2.1: "we split users on the platform into three buckets: 90%, 5%, 5%. ... we observe a statistically significant increase in ViewTime by 0.07% in the test population. ... (only 5% of users experience the stochastic policy)." Ghi chú: khám phá của họ là lấy mẫu từ softmax (Boltzmann), không phải lấy mẫu theo niềm tin — bài không nói ngược lại.
- [BA08] PDF Google Research 34407 (pdftotext), §4 (Hình 5): "GP has the best performance for users who viewed just one video during the training period, but it quickly degrades as the view frequency increases" ; "as the amount of information about a user increases, and we are given more chances to recommend videos, we can do much better than simply recommending the most popular videos." — xác nhận hai dòng “mới xem 1 video” và “xem nhiều” ở cảnh người dùng mới.
- Mô phỏng hook (verify_parts L09k): xếp theo trung bình, hạt 0 — tai nghe mới hiện ở lượt 1–18 và lượt 77, 0 lượt bấm; bài sửa “từ lần thứ 20 tới lần thứ 2000” → “sau đó, tới hết 2000 lượt”, “từ lượt 20” → “sau lần hiện thứ 19”.
- Tự kiểm: các bộ rút 200 nghìn cặp trong `checks` cho 0,94979 và 0,356585 → màn hình sửa 0,949 → 0,950 và 0,354 → 0,357.
- Bỏ câu “Ở khoá Học tăng cường”: bài toán kẻ cướp nhiều tay, khai thác/khám phá, kiểu tham lam có khám phá ngẫu nhiên được giảng lại tại chỗ (ví dụ 2 tay: 0,5² = 0,25); Beta: đường cong, độ lệch chuẩn √(ab/((a+b)²(a+b+1))), Beta(6,6) 0,139 so với Beta(51,51) 0,049.
