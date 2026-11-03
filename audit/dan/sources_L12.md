# Nguồn đã đọc nguyên văn cho DAN L12 (bài hành trình: thử nghiệm có đối chứng trực tuyến ở quy mô lớn)

Đọc ngày 2026-11-02. Tải bằng curl từ trang chính thức của nhóm tác giả (exp-platform.com, nhóm Experimentation Platform của Microsoft —
bản tác giả của các bài KDD/WSDM), trích văn bản bằng `pdftotext` (bản thường và `-layout`). Chỉ trích các câu bài giảng dựa vào (CITED);
mọi con số khác là phép tính lại (VER, `checks` của bài và `audit/dan/verify_dan.py` L12) hoặc ghi rõ “(số minh hoạ)”. Không nêu tên cá
nhân trong lời đọc; tên tác giả chỉ ở `source:`.

Nguồn ứng viên ở ROADMAP §8.1 mục 3 (Kohavi và cộng sự, KDD 2013) đọc được và khớp nội dung. Thêm bốn bài khác của chính nhóm này
(2007, 2009, 2012, WSDM 2013) và một bài liên công ty năm 2019 để đủ trục thời gian khai sinh → ổn định. Các tệp PDF tải được còn có
“Seven Pitfalls” (KDD 2009), “A Dirty Dozen” (KDD 2017), “Seven Rules of Thumb” (KDD 2014) nhưng KHÔNG đọc kỹ, KHÔNG dạy.

Lưu ý trích văn bản: `pdftotext` làm mất chỉ số trên và một số ký hiệu. Chỗ bị mất được ghi rõ bên dưới; con số được dạy ở những chỗ ấy
đều tính lại khớp với số trong câu chữ (VER), không dựa vào ký hiệu bị mất.

## [KO07] R. Kohavi, R. M. Henne, D. Sommerfield, *Practical Guide to Controlled Experiments on the Web: Listen to Your Customers not to the HiPPO*, KDD 2007
Tải: https://exp-platform.com/Documents/GuideControlledExperiments.pdf (200, 504 860 byte, bản tác giả “Appears in KDD 2007”).
- Tóm tắt: “Our experience indicates that significant learning and return-on-investment (ROI) are seen when development teams listen to their
  customers, not to the Highest Paid Person’s Opinion (HiPPO).”
- §3.1 (A/A): “An A/A test can be used to (i) collect data and assess its variability for power calculations, and (ii) test the
  experimentation system (the Null hypothesis should be rejected about 5% of the time when a 95% confidence level is used).”
- §3.2: “The following formula approximates the desired sample size, assuming the desired confidence level is 95% and the desired power is
  90%: n = (4rσ/Δ)^2 where n is the sample size, r is the number of variants (assumed to be approximately equal in size), σ is the std-dev
  of the OEC, and Δ is the minimum difference between the OECs.” (ký hiệu bị mất khi trích; đọc lại từ bản `-layout` và câu định nghĩa)
- §3.2: “Suppose you have an e-commerce site and 5% of users who visit during the experiment period end up purchasing. Those purchasing
  spend about $75. The average user therefore spends $3.75 (95% spend $0). Assume the standard deviation is $30. If you are running an A/B
  test and want to detect a 5% change to revenue, you will need over 1.6 million users to achieve the desired 90% power”
  → VER: (4 · 2 · 30 / (3,75 · 0,05))² = 1 638 400.
- §3.2: “If, however, you were only looking for a 5% change in conversion rate (not revenue) … you will need less than 500,000 users”
  → VER: (4 · 2 · √(0,05 · 0,95) / (0,05 · 0,05))² = 486 400.
- §3.2: “Because of the square factor, if the goal is relaxed so that you want to detect a 20% change in conversion (a factor of 4), the
  number of users needed drops by a factor of 16 to 30,400.” → VER: 486 400 / 16 = 30 400.
- §3.3.1: “if you plan to run an A/B test at 50%/50%, you might start with a 99.9%/0.1% split, then rampup the Treatment from 0.1% to 0.5%
  to 2.5% to 10% to 50%. At each step, which could run for, say, a couple of hours, you can analyze the data to make sure there are no
  egregious problems with the Treatment before exposing it to more users.”
- §5.2.2: “experiments can be auto-aborted if a treatment is statistically significantly underperforming relative to the Control. An
  auto-abort simply reduces the percentage of users assigned to a treatment to zero.”
- §5.2.4: “we recommend that 50% of users see each of the variants in an A/B test. … a good approximation for the multiplicative increase in
  running time for an A/B test relative to 50%/50% is 1/(4p(1 − p)) where the treatment receives portion p of the traffic. For example, if
  an experiment is run at 99%/1%, then it will have to run about 25 times longer than if it ran at 50%/50%.”
  → VER: 1 / (4 · 0,01 · 0,99) ≈ 25,25.
- §5.2.5: “if the experiment were run at 95%/5%, the running time would have to be increased by a factor of 5 to 25 days … Such an
  experiment should not be run at 99%/1% because it would require over 125 days”.
- §5.2.1: “Continuously run A/A tests in parallel with other experiments.”

## [KO09] R. Kohavi, T. Crook, R. Longbotham, *Online Experimentation at Microsoft*, Third Workshop on Data Mining Case Studies, 2009
Tải: https://exp-platform.com/Documents/ExP_DMCaseStudies.pdf (200, 911 418 byte).
- “In March 2006, the Experimentation Platform team (ExP) was formed as a small incubation project. By end of summer we were seven people:
  three developers, two program managers, a tester, and a general manager.”
- “Over the last three years, we built an experimentation platform system (ExP) at Microsoft … we ran many experiments on over a dozen
  Microsoft properties”.
- “Evaluating well-designed and executed experiments that were designed to improve a key metric, only about one-third were successful at
  improving the key metric!”

## [KO12] R. Kohavi, A. Deng, B. Frasca, R. Longbotham, T. Walker, Y. Xu, *Trustworthy Online Controlled Experiments: Five Puzzling Outcomes Explained*, KDD 2012
Tải: https://exp-platform.com/Documents/puzzlingOutcomesInControlledExperiments.pdf (200, 1 461 328 byte, “Appears in KDD 2012”).
- Tóm tắt: “Each of these took multiple-person weeks to months to properly analyze and get to the often surprising root cause.”
- §3.1.2: “When Bing had a bug in an experiment, which resulted in very poor results being shown to users, two key organizational metrics
  improved significantly: distinct queries per user went up over 10%, and revenue per user went up over 30%!”
- §3.1.3: “degraded algorithmic results … force people to issue more queries (increasing queries per user) and click more on ads (increasing
  revenues). However, these are clearly short-term improvements, similar to raising prices at a retail store”.
- §3.1.3: “Distinct queries per month can be decomposed into the product of three terms” (công thức (1) mất ký hiệu khi trích); ba thành
  phần được giảng ngay sau: “Users per month”, “Distinct queries per task … Distinct queries per session is a surrogate metric”,
  “Sessions/user is the key metric to optimize (increase) in experiments, as satisfied users will come more. This is a key component of
  our OEC in Bing.”
- §3.1.3 (thành phần 1): “If the ratio of users in the variants varies significantly from the design, it’s a good indication of a bug.”
- §2: “The A/A test has been our most useful tool in identifying issues in practical systems. We strongly recommend that every practical
  system continuously run A/A tests.”
- §3.2.3: “Chrome, Firefox, and Safari are aggressive about terminating requests on navigation away from the current page and a
  non-negligible percentage of click-beacons never make it to the server. This is especially true for the Safari browser, where losses are
  sometimes over 50%. Adding even a small delay gives the beacon more time … We have seen multiple experiments where added delays made an
  experiment look better artificially.”
- §3.3.3: “the first day has a 67% chance of falling outside the 95% confidence bound at the end of the experiment; the second day has a 55%
  chance” (giả định của bài: không có người dùng lặp lại, số người tỉ lệ với số ngày; đường “21-day bound” ở hình 4)
  → VER: P(|Z| > 1,96 · √(1/21)) ≈ 0,669; P(|Z| > 1,96 · √(2/21)) ≈ 0,545.
- §3.3.3: “The graph in Figure 3 actually is from an A/A test (no difference between the control and treatment)”.
- §3.3.4: “We could not find a single experiment where a statistically significant result in one direction became statistically significant
  in the other direction due to these effects”.
- §3.4.4: “(We consider a week to be the minimum to look at day-of-week effects.)”
- §3.5.3: “Even after three months, the user buckets still had not fully recovered to their pre-experiment levels.” (hiệu ứng mang sang)

## [KO13] R. Kohavi, A. Deng, B. Frasca, T. Walker, Y. Xu, N. Pohlmann, *Online Controlled Experiments at Large Scale*, KDD 2013
Tải: https://exp-platform.com/Documents/2013%20controlledExperimentsAtScale.pdf (200, 1 122 001 byte, “To appear at KDD 2013”).
- Tóm tắt: “At Microsoft's Bing, the use of controlled experiments has grown exponentially over time, with over 200 concurrent experiments
  now running on any given day.”
- Tóm tắt: “A 1% improvement to revenue equals more than $10M annually in the US”.
- §1: “to increase the experiment sensitivity (detectable effect size) by a factor of 10, say from 5% delta to 0.5%, you need 10^2 = 100
  times more users.” (chỉ số trên bị mất khi trích: “102 = 100”)
- §1: “our general guidance is at least thousands of active users”.
- §1: “it distributes traffic from about 100 million monthly users executing over 3.2B queries a month to over 200 experiments running
  concurrently. Almost every user is in some experiment: 90% of users eligible for experimentation … are each rotated into over 15 concurrent
  experiments, while 10% are put into a holdout group”.
- §1: “Analysis of an experiment utilizing 20% of eligible users (10% control, 10% treatment) over 2 weeks processes about 4TB of data”.
  “With about 5 experiments in each one of 15 concurrent experimentation areas (conservative numbers), users end up in one of 5^15 ≈ 30
  billion possible variants of Bing.” (chỉ số trên bị mất: “515  30 billion”) → VER: 5^15 = 30 517 578 125.
- §2 Tenet 3: “Only one third of the ideas tested at Microsoft improved the metric(s) they were designed to improve”.
- §3.3: “The team ran it and it failed again. The new pipeline shipped after five iterations.” (đường đặt hàng mới thử bằng A/B, lần đầu
  “failed with a 2% revenue loss”).
- §3.4: “We recently ran a slowdown experiment where we slowed 10% of users by 100msec … and another 10% by 250msec for two weeks. The results
  showed that performance absolutely matters a lot today: every 100msec improves revenue by 0.6%.”
- §3.5: “Twyman wrote that “Any figure that looks interesting or different is usually wrong.””; “Our recommendation is classical science:
  replication.”
- §4.1: “A Number Line is an orthogonal assignment … a user will be in only one flight per number line. A user is assigned to multiple
  concurrent flights, one per number line.” “a pseudo random hash of an anonymous user id is used”.
- §4.2: “our ranker has four layers, and if three treatments (+ 1 control) are running concurrently (on different number lines), we fragment
  the cache by a factor of 4^4 = 256!”
- §4.2: “we holdout 10% of our total users from any experimentation. … The experiment group consistently showed a 25msec to 30msec delay. A
  separate study for the impact of web cache shows the web cache fragmentation alone contributes about 20msec.”
- §4.3: “we do not alert on a 2 millisecond degradation to Page-Load-Time, even if we have very high confidence the degradation is a real
  effect”; “in a 7-day experiment, the p-value cutoff for the 1st day is 5 × 10^−8, which is much smaller than 0.05, while the last cutoff is
  0.040”; “The most severe changes result in automatic shutdown of an experiment”.
- §5.1: “there is one final scorecard at the end of the experiment, which we require to be a multiple of weeks, usually two weeks.”
- §5.1: “the probability of statistical significance grows from 2.5% (positive movement in a two-sided test) to (1 − 0.975^k). … If a team
  tries five treatments, then the 2.5% false positive rate grows to 12%. If they do six iterations of 5-treatment experiments, there is more
  than a 50% chance of getting a positive statistically significant result.” → VER: 1 − 0,975⁵ ≈ 0,119; 1 − 0,975³⁰ ≈ 0,532.
- §5.1: “Replication Stage … there should be a “final” run, preferably with higher statistical power, which determines the final results.”
- §5.2: “If we are running N experiments at a time, the complexity of detecting pairwise-interactions is quadratic in N. … the system must
  sometimes run hundreds of thousands of hypothesis tests.” → VER: 200 · 199 / 2 = 19 900 cặp.
- §5.2: “each Bing experiment defines a set of constraints … a constraint associated with all ad visual experiments ensures that a user is
  never assigned to two such experiments at the same time.”
- §3.7: “In our experience, interactions are relatively rare and more often represent bugs than true statistical interactions”.

## [DE13] A. Deng, Y. Xu, R. Kohavi, T. Walker, *Improving the Sensitivity of Online Controlled Experiments by Utilizing Pre-Experiment Data*, WSDM 2013
Tải: https://exp-platform.com/Documents/2013-02-CUPED-ImprovingSensitivityOfControlledExperiments.pdf (200, 564 364 byte).
- Tóm tắt: “We propose an approach (CUPED) that utilizes data from the pre-experiment period to reduce metric variability … we can reduce
  variance by about 50%, effectively achieving the same statistical power with only half of the users, or half the duration.”
- §3.2: “Compare (5) to the variance of Y, the variance is reduced by a factor of ρ^2. The larger ρ, the better the variance reduction.”
  (ρ = tương quan giữa chỉ số trong thử nghiệm và cùng chỉ số trước thử nghiệm; công thức (5) mất ký hiệu khi trích — bài chỉ dạy ý
  “tương quan càng cao, phương sai giảm càng nhiều” và “giảm khoảng 50%”, ρ = 0,7 là SỐ MINH HOẠ, 1 − 0,7² = 0,51).
- §3.2: “choose X to be the same as Y … using the same variable during pre-experiment observation window as the control variate … this indeed
  turns out to be the most effective choice we found”.

## [GU19] S. Gupta, R. Kohavi, D. Tang, Y. Xu và cộng sự, *Top Challenges from the first Practical Online Controlled Experiments Summit*, SIGKDD Explorations 21(1), 6/2019
Tải: https://exp-platform.com/Documents/2019-FirstPracticalOnlineControlledExperimentsSummit_SIGKDDExplorations.pdf (200, 418 954 byte).
- Tóm tắt: “representatives with experience in large-scale experimentation from thirteen different organizations (Airbnb, Amazon,
  Booking.com, Facebook, Google, LinkedIn, Lyft, Microsoft, Netflix, Twitter, Uber, Yandex, and Stanford University) were invited … Together
  these organizations tested more than one hundred thousand experiment treatments last year. Thirty-four experts from these organizations
  participated in the summit in Sunnyvale, CA, USA on December 13-14, 2018.”
- §2: “While the sample Ratio Mismatch test is a standard industry test to indicate data quality issues in OCEs”.
- §4.1: “A set of data quality metrics, like a sample ratio, help raise red flags on critical data quality issues. After checking the data
  quality metrics, we want to know the outcome of the experiment. … there is a set of guardrail metrics which are not clearly indicative of
  success of the feature being tested, but metrics that we do not want to harm.”
- §6.2: “When a company tests thousands of experiments a year, it is impossible for experimentation teams to monitor each experiment”;
  §7.2: “Booking.com also has a separate “Peer-Review Program” … Every week participants are paired with a random counterpart. Currently
  approximately 80 people participate.”

## [FA19] A. Fabijan, J. Gupchup, S. Gupta, J. Omhover, W. Qin, L. Vermeer, P. Dmitriev, *Diagnosing Sample Ratio Mismatch in Online Controlled Experiments*, KDD 2019
Tải: https://exp-platform.com/Documents/2019_KDDFabijanGupchupFuptaOmhoverVermeerDmitriev.pdf (200, 1 078 972 byte, bản tác giả).
- Tóm tắt: “Sample Ratio Mismatch (SRM) – the situation when the observed sample ratio in the experiment is different from the expected. Just
  like fever is a symptom for multiple types of illness, an SRM is a symptom for a variety of data quality issues.”
- §1: “A product team at MSN increased the number of rotating cards on the carousel from 12 to 16 … this experiment revealed a significant
  decrease in engagement … the treatment group which was exposed to the new 16 card carousel had fewer users in the analysis compared to what
  was configured … After resolving the issue that was causing the SRM … it was found that the change was in fact positive”.
- §5.3: “the most engaged users in the treatment group were being classified as computer bots and removed from the experiment analysis”.
- §4.1: “approximately 6% of experiments at Microsoft exhibit an SRM … a product running ten thousand experiments in a year can expect to see
  at least one SRM per day.” → VER: 10 000 · 0,06 / 365 ≈ 1,64.
- §5.1: “The experiment assignment service used a hash function to randomize users into one thousand buckets, each bucket representing 0.1
  percent of users. … the control variant was assigned one less bucket than the required number of buckets. A 50/50 test would incorrectly
  be setup as a 49.9/50 split, which is not necessarily an obvious issue.”

## Điều KHÔNG dạy (nguồn không ghi)
- Ngưỡng giá trị p để báo lệch tỉ lệ chia nhóm: [FA19] không ghi một con số (chỉ nói “highly statistically significant”). Bài chỉ dùng phép
  tính sai số chuẩn của tỉ lệ đã học và ngưỡng 1,96 của khoá Khoa học dữ liệu, nói rõ đây là cách tính của bài, không phải ngưỡng của Microsoft.
- Số người dùng thật của thử nghiệm có lỗi 49,9/50: [FA19] không ghi; 1 triệu và 10 triệu người là SỐ MINH HOẠ.
- Số chỉ số dùng khi dò tương tác: [KO13] chỉ ghi “a set of metrics” và “hundreds of thousands of hypothesis tests”; 10 chỉ số là SỐ MINH HOẠ.
- Thứ tự ba thừa số trong công thức (1) của [KO12] mất khi trích; bài nêu ba thành phần theo câu chữ, ví dụ 1000 · 2 · 3 là SỐ MINH HOẠ.
- Tên và năm của các công ty/website ngoài nhóm (Amazon, Google, Etsy…): chỉ dẫn qua [KO13]/[KO12], không dạy chi tiết.
- Quy tắc ngưỡng giảm dần [KO13] §4.3 dựa trên một bài năm 1979 (O’Brien & Fleming) — bài báo đó KHÔNG đọc; chỉ dạy hai con số [KO13] ghi.
- Cơ chế thống kê của bộ lọc tỉ lệ phát hiện sai (Empirical Bayesian FDR, [KO13] §5.2) và mô hình nhị thức âm ([KO12] §3.4): không dạy.
- “Seven Pitfalls” (KDD 2009), “A Dirty Dozen” (KDD 2017), “Seven Rules of Thumb” (KDD 2014): tải được nhưng không đọc kỹ, không dạy.
- Website 20 000 người mỗi tuần, tỉ lệ mua 5% ở quiz, ρ = 0,7, 5 màu nút: SỐ MINH HOẠ.
