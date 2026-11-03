# Nguồn đã đọc nguyên văn cho DSC L15 (bài hành trình: cuộc thi Netflix Prize 2006 → 2012)

Đọc ngày 2026-11-02 (curl + `pdftotext`). Chỉ trích các câu bài giảng dựa vào (CITED); mọi con số khác trong bài là phép tính lại
(VER, `checks` của bài, `audit/dsc/verify_dsc.py` L15 và `audit/verify_plan_curricula.py` DSC:L15) hoặc ghi rõ “(số minh hoạ)”.
Không nêu tên cá nhân trong lời đọc; tên tác giả chỉ ở `source:` và trên màn hình nguồn. Tên đội thi chỉ trên màn hình.

## Nguồn ứng viên KHÔNG đọc được (ROADMAP §8.1 mục 3: “blog Netflix 2012”)
- Netflix Technology Blog, *Netflix Recommendations: Beyond the 5 stars* (Part 1, 4/2012; Part 2, 6/2012):
  netflixtechblog.com/… và netflixtechblog.medium.com/… trả **403** (curl và WebFetch); techblog.netflix.com/2012/04/… trả 403;
  web.archive.org (bản chụp 20170430215314 có trong API `archive.org/wayback/available`) trả **429** sau 3 lần thử cách nhau 90 giây;
  WebFetch không được phép tới web.archive.org. → KHÔNG dạy chi tiết chỉ có ở blog (ví dụ tỉ lệ “75%” lượt xem đến từ gợi ý).
- Thay bằng bài cùng tác giả, cùng năm, do Netflix viết, đăng ở SIGKDD Explorations [AM12] — đoạn §2 chứa đúng các câu mà các báo
  trích lại từ blog (“did not seem to justify the engineering effort…”). Bài ACM TMIS 2015 của Netflix (dl.acm.org/doi/10.1145/2843948) trả 403.

## [BL07] J. Bennett, S. Lanning (Netflix), *The Netflix Prize*, KDD Cup and Workshop 2007 (12/8/2007)
Tải: www.cs.uic.edu/~liub/KDD-cup-2007/proceedings/The-Netflix-Prize-Bennett.pdf (200, 358 958 byte, 4 trang).
- Tóm tắt: “In October, 2006 Netflix released a dataset containing 100 million anonymous movie ratings and challenged the data mining,
  machine learning and computer science communities to develop systems that could beat the accuracy of its recommendation system, Cinematch.”
- §1: “To date, the company has collected over 1.9 billion ratings from more than 11.7 million subscribers on over 85 thousand titles since
  October, 1998. … It receives over 2 million ratings per day.”
- §1: “The Cinematch recommendation system automatically analyzes the accumulated movie ratings weekly using a variant of Pearson's
  correlation with all other movies to determine a list of "similar" movies”.
- §1: “the accuracy of the system is determined by computing the root mean squared error (RMSE) … Improvements … have resulted, to date, in a
  roughly 10% improvement in RMSE over simply reporting the movie average rating.”
- §2: “Netflix provided over 100 million ratings (and their dates) from over 480 thousand randomly-chosen, anonymous subscribers on nearly
  18 thousand movie titles. … The ratings are on a scale from 1 to 5 (integral) stars. It withheld over 3 million most-recent ratings”.
- §2: “The RMSE is computed immediately and automatically for a fixed but unknown half of the qualifying set (the "quiz" subset). This value
  is reported to the contestant and posted to the leader board … The RMSE for the other half of the qualifying set (the "test" subset) is
  not reported and is used by Netflix to identify potential winners of a Prize.”
- §2: “The company reported the RMSE performance of Cinematch trained on the Prize dataset against the quiz subset as 0.9514, a 9.6%
  improvement over simply predicting individual movie averages.” “The company will award a Grand Prize to the team with a system that
  can improve on that accuracy by an additional 10%.”
- §3: “To protect some information about the Netflix subscriber base [5], a perturbation technique was then applied to the ratings”.
  “Selecting the most recent ratings reflects the Netflix business goal of predicting future ratings based on past ratings.”
- §5 (6/2007): “To date over 20 thousand teams have registered from over 152 countries … 2 thousand have submitted prediction sets”.
  “after early and dramatic improvements, as of early February, progress slowed and appeared to have reached an asymptote just below 7%”.

## [KO09] Y. Koren, *The BellKor Solution to the Netflix Grand Prize*, 8/2009
Tải: www.asc.ohio-state.edu/statistics/statgen/joul_aut2009/BellKor.pdf (200, 130 845 byte; trùng từng byte với bản ở
www2.seas.gwu.edu/~simhaweb/champalg/cf/papers/KorenBellKor2009.pdf). netflixprize.com không còn; không đọc được bản trên trang đó.
- §II: “more than 100 million date-stamped movie ratings … m = 480,189 users and n = 17,770 movies”. “About 99% of the possible ratings
  are missing”.
- §II: “the prizemaster returns the root mean squared error (RMSE) achieved on the Quiz set, which is posted on a public leaderboard …
  the winner of the prize is the one that scores best on the Test set, and those scores were never disclosed by Netflix. This precludes
  clever systems which might "game" the competition by learning about the Quiz set through repeated submissions.”
- §III: “say that the average rating over all movies, μ, is 3.7 stars. Furthermore, Titanic is better than an average movie, so it tends to
  be rated 0.5 stars above the average. On the other hand, Joe is a critical user, who tends to rate 0.3 stars lower than the average. Thus,
  the baseline estimate for Titanic's rating by Joe would be 3.9 stars by calculating 3.7 - 0.3 + 0.5.”
- §III-B: “RMSE drops from 0.9555 to 0.9278. Notably, it shows a baseline predictor with a prediction accuracy significantly better than
  that of the original Netflix Cinematch algorithm.” và “the commercial Netflix Cinematch recommender system, whose published RMSE on the
  same Quiz set is 0.9514”.
- §VII: “a set of 454 predictors, which represent all predictors of the BellKor's Pragmatic Chaos team”. “As we entered the final 30 days
  of the competition … we realized that individual predictors, even if novel and accurate, are unlikely to make a difference to the blend.”
- §VIII: “the split of the test set into three parts: Probe, Quiz, and Test, which was essential to ensure the fairness of the competition.
  Despite being planned well ahead, it proved to be a decisive factor at the very last minute of the competition, three years later.”
- §VIII: “we have learned that an accurate treatment of main effects is probably at least as significant as coming up with modeling
  breakthroughs.” “the choice of the 10% improvement goal. Any small deviation from this number, would have made the competition either
  too easy or impossibly difficult.”

## [TJ09] A. Töscher, M. Jahrer, R. M. Bell, *The BigChaos Solution to the Netflix Grand Prize*, 5/9/2009
Tải: www.asc.ohio-state.edu/statistics/statgen/joul_aut2009/BigChaos.pdf (200, 468 043 byte).
- §2: “In total, the number of ratings is 100480507; the probe set of size 1408395 … predict the qualifying set (size: 2817131 samples) and
  achieve a RMSE score of at least 0.8563 on the quiz subset, to get qualified for the Grand Prize. The quiz set is an unknown 50% random
  subset of the qualifying set. The judging criteria for winning the Netflix Grand Prize is the four digits rounded RMSE score on the test
  set (remaining 50%). In the case of a tie the earliest submission wins.”
- §7: “The whole ensemble of predictors from BellKor's Pragmatic Chaos is blended linearly in the end.”
- §7.2: “For ordinary least squares regression, the "bias" of the quiz MSE (MSEq) as an estimate of the test MSE (MSEt) is -2p/N, where p
  is the number of prediction sets and N is the size of the quiz data”; bảng 9: p = 800 → “Optimism of MSE 0.00114”.
  Chú thích 2: “Because we get the RMSE for the Quiz data, there is some danger of overfitting the Quiz data, leading to poorer predictions
  for the test data.”
- §7.2: “This is consistent with the test RMSE target of 0.8572 being 0.0009 higher than the quiz target.”
  “ridge regression reduced the effective degrees of freedom from 820 to about 521”.
  “Nonetheless, even when our quiz RMSE reached an improvement of 10.09%, there was no guarantee that the test RMSE exceeded 10.00%.”

## [FH12] A. Feuerverger, Y. He, S. Khatri, *Statistical Significance of the Netflix Challenge*, Statistical Science 27(2), 2012
Tải: arxiv.org/pdf/1207.5649 (200, 660 228 byte). Bài tổng quan (không phải đội thi) — dùng cho kết quả cuối cùng.
- §1: “The contest's Grand Prize of one million US dollars was offered to anyone who could first improve the predictions so as to attain an
  RMSE value of not more than 90% of 0.9525, namely, 0.8572, or better, on the test set.” “The Netflix contest began on Oct 2, 2006”.
  “More than 50,000 contestants internationally participated”.
- §1: “on July 26, 2009, the Grand Prize winning entry was submitted by the "BellKor's Pragmatic Chaos" team, attaining RMSE values of
  0.8554 and 0.8567 on the quiz and test sets, respectively, with the latter value representing a 10.06% improvement over the contest's
  baseline. Twenty minutes after that submission … a competing submission was made by "The Ensemble" … who attained an RMSE value of
  0.8553 on the quiz set, and an RMSE value of 0.8567 on the test set. To two additional decimal places, the RMSE values attained on the
  test set were 0.856704 by the winners, and 0.856714 by the runners up. Since the contest rules were based on test set RMSE, and also were
  limited to four decimal places, these two submissions were in fact a tie.”
- Bảng 1: “Cinematch, on quiz set 0.9514”; “Cinematch, on test set 0.9525”; “Progress Prize, 2007, quiz 0.8712”; “Progress Prize, 2007,
  test 0.8723”.

## [NS07] A. Narayanan, V. Shmatikov, *Robust De-anonymization of Large Datasets (How to Break Anonymity of the Netflix Prize Dataset)*,
arXiv cs/0610105 v2, 22/11/2007 (đăng IEEE S&P 2008)
Tải: arxiv.org/pdf/cs/0610105 (200, 655 242 byte). Chỉ dạy ở mức khái niệm phòng thủ (dữ liệu thưa, bỏ tên chưa phải ẩn danh).
- Tóm tắt: “an adversary who knows only a little bit about an individual subscriber can easily identify this subscriber's record in the
  dataset.”
- §5: “With 8 movie ratings (of which 2 may be completely wrong) and dates that may have a 14-day error, 99% of records be uniquely
  identified in the dataset. For 68%, two ratings and dates (with a 3-day error) are sufficient”.
  “the additional information required for complete de-anonymization is only around 3 bits in the latter case (with no auxiliary
  information, this number is 19 bits).”
- §1: “Our de-anonymization algorithm is robust to imprecision of the adversary's background knowledge and to sanitization or
  perturbation that may have been applied to the data prior to release.”

## [AM12] X. Amatriain (Netflix), *Mining Large Streams of User Data for Personalized Recommendations*, SIGKDD Explorations 14(2), 2012
Tải: www.kdd.org/exploration_files/V14-02-05-Amatriain.pdf (200, 2 443 939 byte, 6 trang).
- §2: “In 2006, Netflix announced the Netflix Prize … We offered $1 million to whoever improved the accuracy of our existing system called
  Cinematch by 10%. … we had to come up with a proxy question that was easier to evaluate and quantify: the root mean squared error (RMSE) of
  the predicted rating.”
- §2.1: “A year into the competition, the Korbell team won the first Progress Prize with an 8.43% improvement. They reported more than
  2000 hours of work in order to come up with the final combination of 107 algorithms that gave them this prize. And they gave us the
  source code. We looked at the two underlying algorithms with the best performance in the ensemble: Matrix Factorization (MF) and
  Restricted Boltzmann Machines (RBM). Matrix Factorization by itself provided a 0.8914 RMSE, while RBM alone provided a competitive but
  slightly worse 0.8990 RMSE. A linear blend of these two reduced the error to 0.88. To put these algorithms to use, we had to work to
  overcome some limitations, for instance that they were built to handle 100 million ratings, instead of the more than 5 billion that we
  have, and that they were not built to adapt as members added more ratings. But once we overcame those challenges, we put the two
  algorithms into production, where they are still used as part of our recommendation engine.”
- §2.1: “In order to predict a rating, we first estimate a baseline buv = μ+bu+bv as the user and item deviation from average.”
- §2.1: “Herlocker et al. coined the term "magic barrier" to refer to the limit in accuracy … This limit was in fact relatively close to the
  actual Prize threshold, and might have played a role in why it took so much effort to squeeze the last fractions of RMSE.”
- §2.1: “The final Grand Prize ensemble that won the $1M two years later was a truly impressive compilation and culmination of years of
  work, blending hundreds of predictive models to finally cross the finish line. … At Netflix, we evaluated some of the new methods included
  in the final solution. The additional accuracy gains that we measured did not seem to justify the engineering effort needed to bring them
  into a production environment. Also, our focus on improving Netflix personalization had by then shifted from pure rating prediction to the
  next level.”
- §3.1: A/B: “Start with a hypothesis … Design a test … Execute the test … Let data speak for itself”. “we ultimately trust member engagement
  (e.g. viewing hours) and retention. Tests usually have thousands of members and anywhere from 2 to 20 cells … We typically have scores of
  A/B tests running in parallel.” “offline performance is used only as an indication to make informed decisions on follow up tests.”
- §3.3: “an obvious baseline is item popularity … However, popularity is the opposite of personalization”. “a linear combination of
  popularity and predicted rating … score(u, v) = w1p(v)+w2r(u, v)+b”. “Using predicted ratings on their own as a ranking function can lead
  to items that are too niche or unfamiliar”.
- §3.4: “We have several billion item ratings from members. And we receive millions of new ratings every day.”
- §4: “Many teams showed later that adding content features from IMDB or the like to an optimized algorithm had little to no improvement.”
  “More data, even in the form of different features, does not always help.”
- §6: “The Netflix Prize abstracted the recommendation problem to a proxy and simplified question of predicting ratings.”

## Điều KHÔNG dạy (nguồn không ghi hoặc nguồn không đọc được)
- Tỉ lệ “75% lượt xem đến từ gợi ý”, “mọi thứ là một gợi ý” theo nghĩa số liệu, và các chi tiết riêng của blog 2012 phần 2: blog không
  đọc được (403/429) → không dạy. Chỉ dạy những câu có trong [AM12].
- Cuộc thi thứ hai bị huỷ năm 2010, vụ kiện, thư của cơ quan thương mại Mỹ: không đọc nguồn gốc nào → không dạy.
- Nhiễu “perturbation” cụ thể Netflix đã áp vào dữ liệu: [BL07] ghi rõ không mô tả → không dạy. Cách tấn công nhận diện lại: chỉ dạy kết
  quả và bài học phòng thủ, không dạy thuật toán.
- Số mô hình chính xác trong bản ghép cuối: [AM12] ghi “hundreds”, [KO09] ghi tập 454, [TJ09] ghi bậc tự do 820 → bài nói “hàng trăm”,
  đưa 454 và 800 (dòng của bảng 9) đúng chỗ nguồn ghi; không nói “800 mô hình được triển khai”.
- Mức cải thiện thật trên thử nghiệm A/B khi Netflix đưa hai thuật toán vào chạy thật: không nguồn nào ghi → không dạy.
- Đội thứ hai cụ thể gồm ai, nộp lúc mấy giờ: chỉ dạy “20 phút sau”, “hoà ở bốn chữ số thập phân”.
- Số người dùng, giờ xem, cỡ thử nghiệm của người học trong quiz: số minh hoạ.
