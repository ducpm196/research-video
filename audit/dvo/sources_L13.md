# Nguồn đã đọc nguyên văn cho DVO L13 (bài hành trình: đo năng lực phân phối phần mềm, 2014 → 2024)

Đọc ngày 2026-11-02. Các báo cáo PDF tải bằng curl từ `services.google.com/fh/files/misc/` (nơi Google/DORA lưu các báo cáo State of
DevOps, kể cả các năm Puppet phát hành), trích văn bản bằng pypdf 4.3.1 (thư mục nháp, không đưa vào kho). Trang ghi theo số trang PDF.
Trang dora.dev đọc bằng curl. Chỉ trích các câu bài giảng dựa vào (CITED); mọi con số khác là phép tính lại (VER, `checks` của bài,
`audit/dvo/verify_dvo.py` L13 và `audit/verify_plan_curricula.py` DVO:L13) hoặc ghi rõ “(số minh hoạ)”. Không nêu tên cá nhân trong lời
đọc; tên tác giả chỉ ở `source:`.

Nguồn ROADMAP §8.1 mục 3 (“báo cáo DORA State of DevOps 2014–2023”): ĐỌC ĐƯỢC cả 2014, 2015, 2016, 2017, 2018, 2019, 2021, 2023.
Bản 2022 (`state-of-devops-2022.pdf`) trả 404 → không dùng. Thêm trang chính thức dora.dev “A history of DORA's software delivery
metrics” (cập nhật 2026-01-02) cho chặng cuối 2024, vì trang này do chính chương trình DORA viết lại lịch sử bốn chỉ số.

## [SD14] Puppet Labs, IT Revolution Press, ThoughtWorks — *2014 State of DevOps Report*
URL: https://services.google.com/fh/files/misc/state-of-devops-2014.pdf (31 trang).
- tr. 3: “an analysis of more than 9,200 survey responses from technical professionals around the world”.
- tr. 4: “Last year, we found that … high-performing IT organizations were more agile and reliable, deploying code 30 times more
  frequently with 50 percent fewer failures.”
- tr. 14: “we started with a set of related independent variables: deployment frequency, lead time for changes, mean time to recover and
  change fail rate. After a lot of refining and statistical testing, we found that change fail rate was not significantly correlated with
  the other variables leading us to our current definition of IT performance: deployment frequency, lead time for changes and mean time to
  recover.”
- tr. 14: “IT performance is measured in terms of throughput and stability, two attributes that seem to be opposed, yet are both essential”.
- tr. 14 (thực hành tương quan): Deployment Frequency — “Continuous delivery … turning deployment into a non-event that can be performed on
  demand.” “Use of version control for all production artifacts”. Lead Time — version control, “Automated testing”. MTTR — version control
  (“quickly either redeploy the last good state or fix the problem and roll forward”), “Monitoring system and application health”.
- tr. 15: “High performing IT organizations have 50% lower change fail rates than medium and low performing IT organizations.”
  “Deployment is often the biggest pain point leading to the implementation of DevOps practices.”

## [SD15] Puppet Labs — *2015 State of DevOps Report*
URL: https://services.google.com/fh/files/misc/state-of-devops-2015.pdf (36 trang).
- tr. 3: “High-performing IT organizations deploy 30x more frequently with 200x shorter lead times; they have 60x fewer failures and recover
  168x faster.”
- tr. 4: “more than 20,000 technical professionals we’ve surveyed over the past four years.” (chỉ dùng trong nguồn, bài không dạy)

## [SD16] Puppet + DORA — *2016 State of DevOps Report*
URL: https://services.google.com/fh/files/misc/state-of-devops-2016.pdf (55 trang).
- tr. 14: “high performers had: 200 times more frequent code deployments; 2,555 times faster lead times; 24 times faster mean time to
  recover; 3 times lower change failure rate”.
- tr. 15 (bảng 2016 IT Performance by Cluster): tần suất triển khai — cao “On demand (multiple deploys per day)”, thấp “Between once per
  month and once every 6 months”; thời gian đưa thay đổi lên — cao “Less than one hour”, thấp “Between one month and 6 months”.
- tr. 16: “We normalized these ranges to 1,460 deploys per year (four deploys per day x 365 days) for high performers and seven deploys per
  year for low performers (average of two deploys and 12 deploys). These figures show that high performers deploy code 200 times more
  frequently”.
- tr. 16: “we used lead times of 60 minutes for high performers, and 3.5 months for low performers (the average of one and six months).”
- tr. 17: “We took the average of these two ranges (7.5 percent for high performers and 23 percent for low performers), and calculated that
  high performers have three times lower change failure rates”.

## [SD17] Puppet + DORA — *2017 State of DevOps Report*
URL: https://services.google.com/fh/files/misc/state-of-devops-2017.pdf (53 trang).
- tr. 21: “46 times more frequent code deployments; 440 times faster lead time from commit to deploy; 96 times faster mean time to recover
  from downtime; 5 times lower change failure rate”.
- tr. 21: “the gap between high and low performers narrowed for throughput … and widened for stability … We speculate that this is due to
  low-performing teams working to increase speed, but not investing enough in building quality into the process. The result is larger
  failures, and more time to restore service. High performers understand that they don’t have to trade speed for stability”.
- tr. 22: “low performers went from shipping between once per month and once every six months in 2016, to shipping between once per week and
  once per month in 2017.” “all these measures are relative”.
- tr. 24: “1,460 deploys per year … and 32 deploys per year for low performers (mean of 52 deploys and 12 deploys)”; “we used lead times of
  60 minutes for high performers, and 26,940 minutes for low performers (the mean of 10,080 minutes per week and 43,800 minutes per month).”
- tr. 25: MTTR “one hour for high performers, and the mean of one day (24 hours) and one week (168 hours) for low performers”; CFR “7.5
  percent … and 38.5 percent for low performers”. Ghi chú: “Prior to 2016, we allowed respondents to input a number. In 2016 and 2017, we
  changed the answers to ranges.”

## [SD18] DORA — *Accelerate: State of DevOps 2018: Strategies for a New Economy*
URL: https://services.google.com/fh/files/misc/state-of-devops-2018.pdf (78 trang).
- tr. 13: “This year, the data shows a fourth high-performance group: elite performers. … we see the high-performing group growing and
  expanding, suggesting the overall industry is improving”. Tỉ lệ: “ELITE 7%”, high 48%, medium 37%, low 15%.
- tr. 14: bảng bốn chỉ số theo nhóm (Elite, High, Medium, Low); chú thích “The elite performance group is a subset of the high performance
  group.” “Medians reported because distributions are not normal.”

## [SD19] DORA (Google Cloud) — *Accelerate: State of DevOps 2019*
URL: https://services.google.com/fh/files/misc/state-of-devops-2019.pdf (82 trang).
- tr. 3: “data from over 31,000 professionals”.
- tr. 20: tỉ lệ 2018 → 2019: elite 7% → 20%, high 48% → 23%, medium 37% → 44%, low 15% → 12%; “The proportion of our elite performers has
  almost tripled”; “< 100% due to rounding”.
- tr. 21: “elite performers have … 208 times more frequent code deployments … 106 times faster lead time from commit to deploy … 2,604 times
  faster time to recover … 7 times lower change failure rate”.
- tr. 22: “low performers reported deploying between once per month (12 per year) and once per six months (two per year) … seven deploys per
  year for low performers (average of 12 deploys and two deploys). … elite performers deploy code 208 times more frequently”.
- tr. 23: “With lead times of 24 hours for elite performers … and 2,555 hours for low performers (the mean of 730 hours per month and 4,380
  hours over six months), the elite group has 106 times faster change lead times”.
- tr. 25: “All of the measures shown are relative; that is, they compare the highest and the lowest performers each year.”

## [SD21] DORA (Google Cloud) — *Accelerate State of DevOps 2021*
URL: https://services.google.com/fh/files/misc/state-of-devops-2021.pdf (45 trang).
- tr. 4: “data from more than 32,000” (người làm nghề, qua bảy năm).
- tr. 6: “Elite performers now make up 26% of teams in our study, and have decreased their lead times for changes to production.”
- tr. 9: “these metrics focus on system-level outcomes, which helps avoid the common pitfalls of software metrics, such as pitting functions
  against each other and making local optimizations at the cost of overall outcomes.”
- tr. 9 (bảng): nhóm thấp — “Fewer than once per six months”, “More than six months”.
- tr. 10: “The primary metric for operational performance is reliability, which is the degree to which a team can keep promises and
  assertions about the software they operate.”
- tr. 11: “For the first time, our high and elite performers make up two-thirds of respondents.” Tỉ lệ 2021: elite 26%, high 40%,
  medium 28%, low 7%.
- tr. 12: “1,460 deploys per year … to 1.5 deploys per year for low performers (average of two deploys and one deploy). This analysis
  approximates that elite performers deploy code 973 times more frequently”; “6,570 hours for low performers–calculated by taking the
  average of 8,760 hours per year and 4,380 hours over six months–the elite group has 6,570 times faster change lead times”.

## [SD23] DORA (Google Cloud) — *Accelerate State of DevOps Report 2023* (v. 2023-12)
URL: https://services.google.com/fh/files/misc/2023_final_report_sodr.pdf (95 trang).
- tr. 3: “For nearly a decade, the DORA research program has been investigating … We’ve heard from more than 36,000 professionals”.
- tr. 10: “The first step in improving performance is to set a baseline … These measures, though, are not the means by which a team will
  improve.” Bẫy: “Setting metrics as a goal. Ignoring Goodhart’s law and making broad statements like “every application must demonstrate
  ‘elite’ performance by year’s end” increases the likelihood that teams will try to game the metrics.” “Goodhart’s law: when a measure
  becomes a target it ceases to be a good measure.” “One metric to rule them all.” “Narrowly scoped metrics.”
- tr. 11: “The best comparisons are those performed over time on the same applications rather than between different applications”.
  Bốn chỉ số: change lead time, deployment frequency, change failure rate, “Failed deployment recovery time—how long it takes to recover from
  a failed deployment.” “A common approach to improving all four measures is reducing the batch size of changes for an application.”
- tr. 12 (bảng): tỉ lệ thay đổi thất bại elite 5%, high 10%, medium 15%, low 64%; tỉ lệ người trả lời elite 18%, high 31%, medium 33%,
  low 17%; elite: “On demand”, “Less than one day”, “Less than one hour”.
- tr. 92: “In previous years, respondents were presented with six options (0-15%, 16-30%, etc.). This year we presented respondents with a
  slider so that they could select any value between 0% and 100%.”
- tr. 93: “We are now using the term “Failed deployment recovery time” to distinguish our measure from the more generic “time-to-restore” …
  MTTR has caused some confusion in the community: is that “M” for mean or median?” “The previous way of asking about recovery times did not
  allow for a distinction between a failure initiated by a software change and a failure initiated by something like an earthquake”.

## [DH26] dora.dev — *A history of DORA's software delivery metrics* (Last updated: January 2, 2026)
URL: https://dora.dev/insights/dora-metrics-history/ (curl). Kèm https://dora.dev/guides/dora-metrics-four-keys/ (Last updated: January 5, 2026).
- “By 2015, the model solidified into the duality of throughput and stability. The research debunked the myth that speed comes at the
  expense of stability”.
- “in 2018, DORA expanded its scope … they introduced “availability” as a measure of operational health.”
- “The 2021 report inaccurately called the “reliability” metric the “fifth metric” when, in reality, “reliability” is more a measure of
  operational performance than a measure of software delivery performance.”
- “From four keys to five (2024) … DORA researchers identified that change failure rate … acted as a proxy for the amount of rework a team
  must perform. To test this, they introduced a fifth metric: deployment rework rate.” “Deployment rework rate: Percentage of deployments that
  are unplanned work to fix bugs.”
- Trang hướng dẫn: “speed and stability are not tradeoffs”; “best suited for measuring one application or service at a time”; bẫy “Setting
  metrics as a goal … “Every application must deploy multiple times per day by year’s end””; “Competing. The goal is to improve your team’s
  performance over time, not to compete against other teams or organizations.”

## Điều KHÔNG dạy (nguồn không ghi hoặc nguồn tự mâu thuẫn)
- Số “440 lần” của [SD17]: tính lại từ chính số của báo cáo, 26 940 chia 60 = 449. Bài nói “tính lại ra khoảng 449; báo cáo ghi 440”,
  không đoán vì sao lệch.
- Số “2 604 lần” (thời gian khôi phục, [SD18] tr. 19 và [SD19] tr. 24): báo cáo lấy một tháng = 5 040 giờ, trong khi [SD19] tr. 23 lấy một
  tháng = 730 giờ → không dạy con số này. [SD18] tr. 16 cũng ghi 26 940 phút là “trung bình của 43 800 và 262 800” (không khớp) → không dạy
  phép tính thời gian đưa thay đổi lên của 2018.
- Tên công ty và số lần triển khai mỗi ngày của từng công ty ([SD16]–[SD19] nhắc vài hãng): không dạy; bài chỉ dùng số chuẩn hoá 4 lần/ngày.
- Báo cáo 2020, 2022, 2024: không đọc (2022 trả 404); chặng 2024 chỉ dựa vào [DH26]. Bảng nhóm và con số của 2024: không dạy.
- Nhân quả: các báo cáo là khảo sát; bài nói “đi cùng”, “tương quan”, “báo cáo ghi”, không nói thực hành X “gây ra” kết quả Y.
- Đội 20 người, 40 lần triển khai, 3 lần lỗi trong tháng, mục tiêu “mọi đội tinh hoa trong năm” của quiz là SỐ MINH HOẠ.
