# Nguồn đã đọc nguyên văn cho ROB L13 (bài hành trình: xe tự lái từ sa mạc 2004 tới đường phố 2025)

Đọc ngày 2026-11-02 bằng curl + `pdftotext -layout` (bản chữ lưu ở thư mục nháp của phiên, không đưa vào kho). Chỉ trích các câu bài
giảng dựa vào (CITED); mọi con số khác trong bài là phép tính lại (VER, `checks` của bài và `audit/verify_plan_curricula.py` ROB:L13)
hoặc ghi rõ “(số minh hoạ)”. Không nêu tên cá nhân trong lời đọc; tên tác giả chỉ ở `source:` và dòng nguồn trên màn hình.
Đơn vị giữ như nguồn (dặm, dặm/giờ); đổi sang m/s là phép tính lại (1 dặm/giờ = 0,44704 m/s; 1 dặm ≈ 1,609 km).

## [ST06] S. Thrun và cộng sự (Stanford, Volkswagen, Intel Research, Mohr Davidow), *Stanley: The Robot that Won the DARPA Grand Challenge*, Journal of Field Robotics 23(9), 661–692, 2006 (DOI 10.1002/rob.20147)
Tải: http://robots.stanford.edu/papers/thrun.stanley05.pdf (trang của nhóm tác giả; curl 200, 3 569 074 byte; bản PDF mang số trang
và chân trang “Journal of Field Robotics DOI 10.1002/rob” của bản in). Trang Wiley KHÔNG đọc (không cần: bản tác giả là bản dàn trang của
tạp chí; khớp từng câu với bản trên Wiley: NOT_VERIFIED).
- §1 (chặng 2004): “The Grand Challenge was launched by the Defense Advanced Research Projects Agency DARPA in 2003 to spur innovation in
  unmanned ground vehicle navigation.” “The first competition, which carried a prize of $1M, took place on March 13, 2004. It required robots
  to navigate a 142-mile long course through the Mojave desert in no more than 10 h. 107 teams registered and 15 raced, yet none of the
  participating robots navigated more than 5% of the entire course.”
- §1 (chặng 2005): “The challenge was repeated on October 8, 2005, with an increased prize of $2M. This time, 195 teams registered and 23
  raced. Of those, five teams finished. Stanford's robot "Stanley" finished the course ahead of all other vehicles in 6 h, 53 min, and 58 s”.
- §1: “The main technological challenge in the development of Stanley was to build a highly reliable system, capable of driving at relatively
  high speeds through diverse and unstructured off-road environments”.
- §1.1: “Absolutely no manual intervention was allowed.” “The specific race course was kept secret from all teams until 2 h before the race.”
  “In the 2005 race, the RDDF contained 2,935 waypoints.” “The speed limits varied between 5 and 50 mph.”
- §4 (định vị): “the vehicle state comprises a total of 15 variables.” “An unscented Kalman filter UKF … estimates these quantities at an
  update rate of 100 Hz. The UKF incorporates observations from the GPS, the GPS compass, the IMU, and the wheel encoders.” Khi mất GPS:
  “a more restrictive UKF motion model is used”; “able to maintain accurate pose of the vehicle during GPS outages of up to 2 min long; the
  accrued error is usually in the order of centimeters. Stanley's health monitor will decrease the maximum vehicle velocity during GPS outages
  to 10 mph”.
- §5 (bản đồ bằng tia laser): “a small error in the vehicle's roll/pitch estimation leads to a massive terrain classification error, forcing
  the vehicle off the road.” “the lasers are aimed at the road up to 30 m in front of the vehicle. In our reference dataset of labeled
  terrain, we found that 12.6% of known drivable area is classified as obstacle, for a height threshold parameter = 15 cm. Such situations
  occur even for roll/pitch errors smaller than 0.5°. Pose errors of this magnitude can be avoided by pose estimation systems that cost
  hundreds of thousands of dollars, but such a choice was too costly for this project.” Sau xử lý xác suất + học tham số từ dữ liệu đã ghi:
  “the false positive rate … drops from 12.6% to 0.002%.”
- §6 (thị giác): “The effective maximum range at which obstacles can be detected with the laser mapper is approximately 22 m. This range is
  sufficient for Stanley to reliably avoid obstacles at speeds up to 25 mph. Based on the 2004 Race Course, the development team estimated
  that Stanley would need to reach speeds of 35 mph in order to successfully complete the challenge. To extend the sensor range enough to
  allow safe driving at 35 mph, Stanley uses a color camera”. Hình 14: “the reach of lasers is approximately 22 m, whereas the vision module
  often looks 70 m ahead.”
- §10.1 (chuẩn bị): “Emphasis was placed on early integration, so that an end-to-end prototype was available nearly a year before the race.”
  “In the months leading up to the race, all software and hardware modules were debugged and subsequently frozen.”
  “The primary measure of system capability was "MDBCF"--mean distance between catastrophic failures. A catastrophic failure was defined as a
  condition under which a human driver had to intervene.” “In December 2004, the MDBCF was approximately 1 mile. It increased to 20 miles in
  July 2005. The last 418 miles before the National Qualification Event were free of failures; this included a single 200-mile run over a
  cyclic testing course.” “The vehicle had logged more than 1,200 autonomous miles.”
- §10.1 (bỏ radar): radar “proved highly effective in testing, two reasons prevented its use in the race. The first reason was technical:
  During the NQE, the USB driver of the receiving computer repeatedly caused trouble”. “the team felt that the technical risks associated with
  the RADAR system outweighed its benefits”.
- §10.3 (cuộc đua): “Its overall average velocity was 19.1 mph.” “Stanley reached its top speed of 38.0 mph”. “The vision module caused
  Stanley to slow down to 25 mph for 13.1% of the total distance; however, without the vision module Stanley would have been forced to a 25 mph
  maximum speed, which would have resulted in a finishing time of approximately 7 h and 5 min, possibly behind CMU's Sandstorm robot.”
- §10.3 (sự cố): “Stanley's laser data stream repeatedly stalled for durations of 300 to 1,100 ms. There were a total of 17 incidents”. “The
  resulting inaccurate time stamping of the laser data led to the insertion of phantom obstacles into the map. In four of those cases, those
  incidents resulted in a significant swerve.” Hình 32: “None of these incidents led to a collision or an unsafe driving situation during the
  race.”
- §11: “the race environment was static. Stanley is unable to navigate in traffic. For autonomous cars to succeed, robots, such as Stanley,
  must be able to perceive and interact with moving traffic.”

## [WM20] M. Schwall, T. Daniel, T. Victor, F. Favarò, H. Hohnhold (Waymo LLC), *Waymo Public Road Safety Performance Data*, 2020 (arXiv:2011.00038)
Tải: https://arxiv.org/pdf/2011.00038 (curl 200, 7 414 041 byte; “Copyright © 2020 Waymo LLC”).
- Abstract: “The data presented in this paper represents more than 6.1 million miles of automated driving in the Phoenix, Arizona metropolitan
  area, including operations with a trained operator behind the steering wheel from calendar year 2019 and 65,000 miles of driverless
  operation without a human behind the steering wheel from 2019 and the first nine months of 2020.” “There were 47 contact events that occurred
  over this time period, consisting of 18 actual and 29 simulated contact events, none of which would be expected to result in severe or
  life-threatening injuries.”
- Abstract: “the Waymo Driver completely avoided certain collision modes that human-driven vehicles are frequently involved in, including road
  departure and collisions with fixed objects.” “the presence of collisions that resulted from challenging situations induced by other drivers
  serves as a reminder of the limits of AV collision avoidance as long as AVs share roadways with human drivers.”
- §1: “The Waymo Driver, has driven over 20 million miles on public roads since testing began in 2009.” “By early 2020, these services were
  providing a combined 1,000 to 2,000 rides per week, 5% to 10% of which were driverless”.
- §1.1: trained operators “are highly trained to focus on monitoring … and to be prepared to assume control”. “the outcome of an event
  experienced by an AV being tested with an operator may not reflect the outcome that the same AV would have experienced if operating in
  driverless mode”.
- §1.2: “Simulating what might have transpired had a disengagement not occurred is an example of counterfactual ("what if") simulation”. “The
  disengagement event is also added to a library of scenarios, so that future software can be tested against the scenario.” “these
  simulations carry the limitation of being informative, but not definitive.”
- §1.3: “This mileage figure represents over 500 years of driving for the average U.S. licensed driver”.

## [WS20] Waymo LLC (N. Webb, D. Smith và cộng sự), *Waymo's Safety Methodologies and Safety Readiness Determinations*, 10/2020 (arXiv:2011.00054)
Tải: https://arxiv.org/pdf/2011.00054 (curl 200, 589 628 byte).
- Executive Summary: “To date, Waymo has compiled over 20 million self-driving miles on public roads operating in over 25 cities, including
  74,000 driverless miles.” (khác 65 000 của [WM20] vì [WM20] chỉ tính vùng Phoenix trong khung thời gian của bài — bài giảng dùng 65 000 khi
  nói về [WM20].)
- “Waymo's various safety methodologies are supported by three basic types of system-level testing (simulation, closed-course, and public
  road)”. “we specify the inclusion of redundant braking and steering actuators”.
- “Waymo's Risk Management Program identifies, prioritizes, and drives the resolution of potential safety issues before new or updated
  features or software are used on public roads”. “Our Field Safety Program identifies and effectuates appropriate disposition of potential
  safety issues based on information collected after updated features or software have been released”.
- Readiness: “a discrete determination … with regard to the readiness of a specific configuration of the ADS for a specific deployment. The
  determination is focused on the ODD, the specific use case, and the particular vehicle platform.” “the level of detail … is the highest
  when removing the trained operator due to the absence of the operator as a risk mitigation.”

## [KU24] K. D. Kusano và cộng sự (Waymo), *Comparison of Waymo Rider-Only Crash Data to Human Benchmarks at 7.1 Million Miles*, Traffic Injury Prevention 2024 (arXiv:2312.12675v3, 24/10/2024)
Tải: https://arxiv.org/pdf/2312.12675 (curl 200, 1 159 648 byte; bản “Accepted Manuscript”, DOI 10.1080/15389588.2024.2380786).
- Abstract: “ADS crash data were derived from NHTSA's Standing General Order (SGO) reporting over 7.14 million RO miles through the end of
  October 2023 in Phoenix, AZ, San Francisco, CA, and Los Angeles, CA and compared to human benchmarks from the literature.”
- “the any-injury-reported crashed vehicle rate was 0.6 incidents per million miles (IPMM) for the ADS vs 2.80 IPMM for the human benchmark,
  an 80% reduction”. “Police-reported crashed vehicle rates for all locations together were 2.1 IPMM for the ADS vs. 4.68 IPMM for the human
  benchmark, a 55% reduction or a human crash rate that was 2.2 times higher than the ADS rate.”
- “When excluding ADS crashes with a delta-V less than 1 mph … about half of the ADS collisions were excluded”. “The direction and
  significance of comparisons in the any property damage or injury outcome group are inconclusive due to difficulties in estimating a matching
  human benchmark.”
- Introduction: “Retrospective studies cannot be used to make safety determinations prior to deployment.” “Since July 2021, the NHTSA Standing
  General Order (SGO) 2021-01 has required ADS developers to report all crashes meeting certain criteria”.
- Table 4 (Phoenix): “RO Miles (millions) 5.34”; “SGO Police-Reported 12 2.2 (1.2,3.9)”; “SGO any-injury-reported 3 0.6 (0.1, 3.2)”.
  (San Francisco: 1.76 triệu dặm; any-injury 1 → 0.6 (<0.1, 3.2).)

## [KU25] K. D. Kusano và cộng sự (Waymo), *Comparison of Waymo Rider-Only Crash Rates by Crash Type to Human Benchmarks at 56.7 Million Miles*, accepted Traffic Injury Prevention (arXiv:2505.01515v1, 2/5/2025)
Tải: https://arxiv.org/pdf/2505.01515v1 (curl 200, 1 856 910 byte).
- Abstract: “Data was examined over 56.7 million RO miles through the end of January 2025, resulting in a statistically significant lower
  crashed vehicle rate for all crashes compared to the benchmarks in Any-Injury-Reported and Airbag Deployment, and Suspected Serious Injury+
  crashes.” “There was no statistically significant disbenefit found in any of the 11 crash type groups.”
- Introduction: “Schwall et al. (2020) found through a counterfactual simulation method that a human present was able to prevent 62% of
  crashes over 6.1 million miles of testing operations.”
- Introduction: “As the benchmark becomes more rare (i.e., a lower crash rate), more miles and/or a larger relative difference in performance
  between the ADS and benchmark is needed to draw statistically significant conclusions.” “An ADS with a crash rate of 10% the national
  suspected serious injury+ benchmark (i.e., a 90% reduction of the benchmark of 0.11 Incidents per Million Miles, IPMM) would require 56.3
  million miles.” “retrospective evidence … would serve as a continuous confidence growth in the safety assurance process … that used
  design-based and prospective studies during system development”.
- Results: “31.159 million miles in Phoenix, 18.260 million miles in San Francisco, 6.448 million miles in Los Angeles, and 0.834 million miles
  in Austin … for a total mileage of 56.700 million miles.” Table 3 “All Locations 48 18 2” (any-injury, airbag, suspected serious injury+);
  “Phoenix 24 8 0”, “San Francisco 16 7 2”. Table 4 any-injury: Phoenix “2.09 0.77 … -63%”; “All Locations … Mileage Blended 4.04 0.85 -79%*
  -85% -71%”. “These comparisons were not statistically significant for Los Angeles due to limited mileage.”
- Limitations: “there is an endless list of possible factors to potentially account for”; benchmark adjusted for “the 33% of injury crashes
  that were estimated to not be reported to police”.

## Điều KHÔNG dạy (nguồn không ghi, hoặc không đọc được)
- Kết quả từng đội năm 2004 (đội nào đi xa nhất, bao nhiêu dặm): [ST06] chỉ ghi “none … more than 5%” → bài chỉ nói “chưa xe nào quá 5%,
  tức chưa quá 7,1 dặm” (7,1 là phép tính lại). Trang chính thức của DARPA về 2004: không đọc trong phiên này.
- Gia tốc phanh và thời gian phản ứng của Stanley: [ST06] không ghi → 4 m/s² và 0,2 s là SỐ MINH HOẠ; chỉ dùng để thấy vì sao 22 m đủ cho
  25 dặm/giờ mà không đủ cho 35 dặm/giờ.
- Nguyên nhân gốc của việc dòng dữ liệu laser bị ngắt (300–1100 ms): [ST06] chỉ ghi hậu quả (dấu thời gian sai → vật cản ma) → không dạy
  nguyên nhân.
- Tỉ lệ va chạm của người lái “trung bình” ngoài các mốc so sánh đã trích; số dặm hiện tại của đội xe (trang “Safety Impact” của hãng, các
  con số sau 1/2025): không đọc → không dạy.
- Phương pháp tính khoảng tin cậy (Poisson chính xác, phân phối beta prime) của [KU24]: bài chỉ đọc khoảng đã in trong bảng, không dạy cách tính.
- Tên robot của đội khác, tên người: chỉ trên màn hình nguồn khi cần, không đọc.
- Số liệu của các hãng khác, báo cáo “disengagement” của bang California: không đọc trong phiên → không dạy.
- Tình huống quiz (10 xe giao hàng 2 m/s, cảm biến 3 m, phanh 0,8 m/s², trễ 0,25 s, tuyến 1,5 km, 2000 km thử, 1 lần mỗi 1000 km):
  SỐ MINH HOẠ.
