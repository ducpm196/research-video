# Nguồn đã đọc nguyên văn cho RBM L17 (bài hành trình: lọc Kalman từ Apollo vào công nghiệp, 1960 → 1985)

Đọc ngày 2026-11-02 bằng curl + `pdftotext` (bản quét có OCR; chữ OCR lỗi được sửa chính tả khi trích, ví dụ “Kal_n” → “Kalman”,
không đổi nghĩa). Chỉ trích các câu bài giảng dựa vào (CITED); mọi con số khác trong bài là phép tính lại (VER, `checks` của bài,
`audit/rbm/verify_rbm.py` L17 và `audit/verify_plan_curricula.py` RBM:L17) hoặc ghi rõ “(số minh hoạ)”.
Không nêu tên cá nhân trong lời đọc; tên tác giả và tên người phát triển thuật toán chỉ ở `source:` và dòng nguồn trên màn hình.
Số trang dưới đây là trang của tệp PDF (“tr. PDF N”, 25 trang), không phải số in ở chân trang.

## [MS85] L. A. McGee, S. F. Schmidt, *Discovery of the Kalman Filter as a Practical Tool for Aerospace and Industry*, NASA Technical Memorandum 86847, Ames Research Center, 11/1985
Tìm: https://ntrs.nasa.gov/api/citations/search?q=McGee%20Schmidt%20Kalman%20filter%20aerospace%20industry (curl 200) → mã NTRS
19860003843. Tải: https://ntrs.nasa.gov/api/citations/19860003843/downloads/19860003843.pdf (curl 200, 1 599 167 byte, 25 trang).
Hai tác giả là người trong cuộc (nhóm Ames làm mô phỏng Apollo 1960–1961; nhóm làm RAINPAL 1969–1972) — nguồn do chính đội viết lại.

### Khai sinh (1959–1961)
- Tóm tắt (tr. PDF 3): “The first publicly known application was made at NASA Ames Research Center in the early 1960s during feasibility
  studies for circumlunar navigation and control of the Apollo space capsule.” “The resulting extended Kalman filter, as it is now known, is
  often still referred to simply as the Kalman filter.” “the problems of implementation on small spaceborne and airborne computers led to a
  ‘square-root’ formulation of the filter to overcome numerical difficulties associated with computer word length.” “the first airborne
  computer implementation and flight test which was conducted in 1972.”
- Mở đầu (tr. PDF 3): “In 1960, Dr. Kalman published his now-famous paper … presenting a sequential solution to the time-varying linear
  filtering problem.”
- Quy mô nhóm (tr. PDF 5): “The Dynamics Analysis Branch had only eight analytically oriented research persons--too few to carry out two very
  complex research programs.”
- Yêu cầu trên tàu (tr. PDF 5): “the software for the mission would have to be resident in a reliable, on-board digital computer with
  considerable memory and relatively high computational speed. The midcourse algorithms would have to be as efficient as possible.”
- Máy mô phỏng (tr. PDF 5): “Ames had an IBM 704, which would be our simulation computer.” “we had to write all of our own matrix-handling
  subroutines. We soon found, however, that the double indexing needed for matrix operations ran so slowly that our matrix-handling
  subroutines had to be rewritten to use single indexing. Otherwise, a circumlunar trajectory with a Kalman filter would have taken hours of
  computer time.”
- Điểm nghẽn ước lượng (tr. PDF 6): “we had reviewed the iterative weighted, least-squares estimator in use by JPL and decided that it was not
  only too complex for state-of-the-art on-board computers but would also put a severe burden on the IBM 704”. Lọc Wiener: “The difficulties
  were the nonlinearity of the problem and the requirement, for lunar vehicle navigation, of an irregular series of discrete measurements
  (whereas missile navigation had assumed continuous measurements).”
- Phát hiện (tr. PDF 6–7): “In the fall of 1960, Dr. Kalman … called and arranged to visit Dr. Schmidt”. “the sequential solution features of
  Dr. Kalman's formulation were of interest because they could certainly relieve some of the computational problems we were facing with the
  IBM 704.” “The notation, as well as the concepts, used by Dr. Kalman were also very difficult for practicing engineers to grasp.”
  “the linear perturbation concepts we had been using in our guidance studies could be used to produce the linear system needed to apply
  Dr. Kalman's theory.”
- Tách hai bước (tr. PDF 7): “Dr. Kalman's original formulation would have required an on-board crew to make a continuous sequence of optical
  measurements equally spaced in time throughout the lunar mission, an impractical scenario.” “The solution to the problem was obtained by
  decomposing the original formulation into a discrete-time update portion and a discrete-time optical measurement update portion”.
  “Looking back, the decomposition seems almost trivial; at the time, however, it was a major and critical step forward”.
- Lọc mở rộng (tr. PDF 8): “a relinearization about the current estimated state might offer substantial advantages”. “We reasoned that ‘on
  the average,’ the estimated state would be closer to the actual, or true, state than to the reference, or nominal, state”. “An accidental
  error in input conditions to a simulation run caused the true trajectory to remain in an orbit around Earth, but the estimated trajectory had
  the proper starting conditions for a lunar transfer trajectory.” “At first, the Kalman-filter estimator caused some relatively large
  overshoots in the estimated state owing to the nonlinear effects, but the estimated state soon successfully converged close to the true
  state. This modification … has come to be known as the ‘extended Kalman filter.’”
- Ma trận chuyển (tr. PDF 9): “The only remaining alternative was to integrate the additional 18 second-order differential equations along
  with those for the true, reference, and estimated trajectories.” “At this point we were about 6 months behind the schedule”.
- Lần chạy đầu (tr. PDF 9–10): “When the simulation program was finally ready for a test run on the IBM 704, it took a little over an hour of
  execution time. The first run showed disappointing results in the state estimation scheme. … Then, an error was found in the way we were
  calling a subroutine. On the second run everything worked fine!” “By early 1961, the simulation program had been used extensively to
  validate the extended Kalman filter”.
- Kết quả (tr. PDF 10): “the extended Kalman filter would give accuracies comparable to those of weighted least-square estimators, but with a
  tremendous reduction in requirements for on-board computer memory and computational speed.”
- Thứ tự nhân (tr. PDF 10): “The order chosen in which to multiply the three matrices in the measurement update equation, that is, (KH)P rather
  than K(HP) was the most numerically stable of the two possibilities”. “we might have found that double-precision matrix operations were
  necessary with a resultant large increase in computer time”.
- Apollo (tr. PDF 11): “Potter … devised the first square-root filter implementation, which was used for the Apollo system. His formulation
  could not handle random forcing functions, but it was useful for implementation in small-word-size on-board computers, such as that of the
  Apollo system.”

### Phân kỳ, dữ liệu thật (1961–1966)
- (tr. PDF 12): “at this point in time (1961) no problems had been experienced in the digital simulations owing to truncation or modeling
  errors. Later, however, many researchers began to report substantial problems of instability with Kalman filtering”.
- Hướng nghiên cứu 1962–1964 (tr. PDF 12): “To study the effect of the relatively short word length accommodated by most of the airborne
  computers of that time.” “It was during the early phases of this work that the ‘divergence’ problem was first noticed.”
- Bốn cách vá (tr. PDF 13): “the first attempts to fix the computer round-off problem involved working with the covariance matrix P to make it
  symmetric with nonnegative eigenvalues.” “Second, by averaging the off-diagonal terms to force symmetry.” “And fourth, by adding a small
  positive number to all of the diagonal terms of the covariance matrix, P, after measurement and time-update operations.” “the third and
  fourth fixes worked best”.
- P quá nhỏ (tr. PDF 13): “The new problem was most apparent after a series of very accurate measurements had been processed by the filter,
  causing the covariance matrix P to become so ‘small’ that additional measurements would be essentially ignored by the filter. … the
  estimated state would diverge from the true state. The basic problem here is due to modeling errors. The use of ‘pseudonoise’ in the
  time-update proved quite effective against this problem.”
- Bản ghi nhớ Honeywell 8/7/1964 (tr. PDF 13): “recommended that the symmetry problem with P be solved by computing only the diagonal plus the
  upper triangular elements of the matrix”; dạng Joseph “reduces to Kalman's measurement equation when the gain … is optimal … It is also the
  general equation for the covariance matrix after a state change owing to an arbitrary gain.”
- (tr. PDF 14): “when the covariance matrix P is a too-optimistic representation of estimated state errors, external measurements are given too
  little weight.” “ground radar data are generally superior to on-board measurements … These results supported the ultimate decisions to have
  the primary Apollo navigation conducted from the ground, using ground radar data with a backup system on the spacecraft.”
- Agena 1961, Lockheed (tr. PDF 14): “Dr. Schmidt had his first opportunity to process actual measurement data with the extended Kalman
  filter”. “A bad-data rejection technique was developed which compared the measurement residual magnitude to its standard deviation as
  computed from the Kalman-filter measurement update algorithm. If the residual magnitude exceeded n times the standard deviation, the
  measurement was rejected. The value of n used was 3, corresponding to a 3-sigma residual magnitude test.” “The Kalman filter was used as a
  data compression algorithm”.
- Philco-WDL 1962 (tr. PDF 15): “General computational techniques for saving machine time by taking account of the sparsity of the transition
  matrix and symmetry of the covariance matrix.”

### Thời gian thực trên máy bay, dạng căn bậc hai (1966–1972)
- C-5A (tr. PDF 15–16): “By 1966, the advantages of the extended Kalman filter were widely recognized. When Lockheed became the prime
  contractor for the C-5A aircraft, the Kalman filter was specified for the navigation system.” “The C-5A system, to the best of the authors'
  knowledge, was the first real-time application of a Kalman filter on board an aircraft.” “the real-world problems of selecting appropriate
  error states, adding error estimates to the system outputs, working with a limited word size, and making the whole computational burden work
  within the time-frames of small computers had to be confronted.” “a method was needed wherein the filter's error covariance would be
  computed and propagated in square-root form and would therefore require less computational precision to maintain filter stability.” “the
  standard extended Kalman algorithm, with the epsilon technique and other ad hoc procedures, was used for controlling numerical problems”.
- (tr. PDF 16): “In early 1968, he successfully developed a method … that looked promising for application on a small, fixed-point on-board
  computer.”
- RAINPAL (tr. PDF 17): “The flight-test aircraft was to be a Convair CV-340 with a gross takeoff weight of 44,000 lb. The on-board computer
  would be a ruggedized XDS-920 with a 24-bit-word length and a 32K memory.” “The original formulation used Potter's algorithm for a
  measurement update and a modified Gram-Schmidt algorithm for the time update”; Householder “could be used for the time update and save
  computational operations”. “The square-root filter, however, performed flawlessly once it had been debugged early in the software
  development; in fact, it soon became possible to place the square-root Kalman filter above all suspicion when software problems occurred.
  With the standard formulation, the filter would always have been suspect because of its propensity to diverge or develop negative
  eigenvalues”.
- (tr. PDF 18): “The flight-test results showed that with only three range measurements versus seven theodolites, on the final approach to
  touchdown the RAINPAL system gave position and velocity estimates that were smoother and had accuracies of the same order as those of the
  WSMR system.” “Since the flight test of the RAINPAL system in January 1972”.

### Ổn định, nhanh hơn, lan sang công nghiệp (1973–1985)
- Carlson 1973 (tr. PDF 18; ref. 35 ghi “AIAA J., vol. 11, no. 9, Sept. 1973”): “Carlson's algorithm maintained the covariance square-root
  matrix in triangular form, but, more importantly, reduced the computation time … for a moderate number of states, Carlson's method would
  approach the speed of the standard extended Kalman-filter formulation.”
- (tr. PDF 19): “In 1975 Bierman (ref. 36) introduced his U-D factorization of the Kalman filter which appears to be the most efficient
  square-root method to be developed to date: it uses only slightly more computer time than the standard extended Kalman filter. (With this
  algorithm there is no requirement for square-root operations.)” “Dyer and McReynolds in 1969 … whose filter algorithms were successfully
  used for the navigational computations on the Mariner 10 Venus-Mercury space mission in 1973.”
- Kết luận (tr. PDF 19): “success or failure with this approach may be dependent on many factors, such as computer round-off errors,
  inadequate statistical models and nonlinearities in the problem”. “If the filter is being run on a large machine, extra precision arithmetic
  may be a reliable solution to the problem of numerical instability, but stability problems may still remain because of mismodeling. In the
  case of an airborne application, extra precision is often not a practical alternative.” “those experienced in applying Kalman filters to
  real-world problems are abandoning the ad hoc stabilization techniques and the standard filter formulation in favor of algorithms that are
  numerically better conditioned.”
- (tr. PDF 20): “The square-root filter, by its nature, is inherently more stable and better conditioned”. “Square-root algorithms have gained
  acceptance rather slowly … the early algorithms ran slower than the standard Kalman formulation, and the factorization techniques appeared
  too complicated and used too much computer storage”.
- Công nghiệp (tr. PDF 20; ref. 38 = IEEE Trans. Auto. Control, vol. AC-28, no. 3, Mar. 1983): “spacecraft orbit determination, prediction of
  cattle populations in France, radar tracking, navigation, ship motion, natural gamma ray spectroscopy in oil- and gas-well exploration,
  measurement of instantaneous flow rates, and estimation and prediction of unmeasurable variables in industrial processes, on-line failure
  detection in nuclear plant instrumentation, and power station control systems. In many cases, the solutions in these papers were implemented
  and were operationally successful.” “we have only scratched the surface”.
- Giới hạn của nguồn (tr. PDF 20): “The recording of those events is almost totally dependent on the recollections of and personal contacts
  made by the authors.”

## Điều KHÔNG dạy (nguồn không ghi, hoặc đọc không chắc)
- Số bit phần định trị của máy mô phỏng (tr. PDF 14, OCR “2i bits” — không đọc chắc là 27): không dạy con số này.
- Bộ lọc trên máy tính dẫn đường của chính tàu Apollo (cỡ từ, số trạng thái, tần suất đo): [MS85] chỉ ghi “small-word-size on-board
  computers, such as that of the Apollo system” và việc dùng thuật toán căn bậc hai của Potter → không dạy chi tiết máy Apollo.
- Số trạng thái của bộ lọc C-5A, RAINPAL; độ chính xác (mét) của chuyến bay 1972: nguồn không ghi số → không dạy.
- Số phép tính của Carlson, U-D so với dạng chuẩn: nguồn chỉ ghi định tính (“approach the speed”, “only slightly more computer time”) → bài
  không đưa phần trăm.
- Năm 1975 của U-D là theo câu văn của [MS85]; tài liệu tham khảo ref. 36 là cuốn sách (Academic Press) — năm in của sách không đọc rõ
  trong OCR → bài chỉ nói “năm 1975”, như câu văn.
- Thứ tự nhân (KH)P “ổn định số hơn” K(HP): là nhận định của [MS85]; bài KHÔNG giải thích cơ chế làm tròn (nguồn không giải thích), chỉ đếm
  số phép nhân của hai cách (VER) để thấy cái giá của lựa chọn ổn định.
- Số minh hoạ trong bài (ghi rõ trên màn hình): 100 phép đo; Q = 0,5 mỗi giờ và khoảng cách 1 giờ / 4 giờ; hàm đo h(x) = x² với x thật 3;
  Q = 0,1, R = 1; P = 3, R = 1, phần dư 5 và 7; ma trận P có ô lệch 1,0004 / 0,9996; độ lệch chuẩn 0,1 m và 1000 m; số thực 32 bit;
  robot của câu đố (4 trạng thái, đo mỗi giây, chạy 8 giờ).
- Câu “chỉ khoảng 7 chữ số có nghĩa” của số thực 32 bit là kiến thức chung (IEEE 754: 24 bit phần định trị, 2²⁴ ≈ 1,68 · 10⁷), không lấy từ
  [MS85].
