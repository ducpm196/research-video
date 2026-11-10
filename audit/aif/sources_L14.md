# Nguồn đã đọc nguyên văn cho AIF L14 (bài hành trình: máy chơi cờ từ Deep Blue tới AlphaZero)

Đọc ngày 2026-11-02 (curl tải PDF rồi `pdftotext -layout`; trang HTML tải bằng curl rồi bỏ thẻ). Chỉ trích các câu bài giảng dựa vào
(CITED); mọi con số khác trong bài là phép tính lại (VER, `checks` của bài và `audit/aif/verify_aif.py` L14) hoặc ghi rõ “(số minh hoạ)”.
Không nêu tên cá nhân trong lời đọc (kể cả các kỳ thủ là đối thủ của máy); tên tác giả chỉ ở `source:`.

## [DB02] M. Campbell, A. J. Hoane Jr., F.-h. Hsu, *Deep Blue*, Artificial Intelligence 134 (2002) 57–83
Bản chính thức: sciencedirect.com/science/article/pii/S0004370201001291 — curl và WebFetch đều **403**. Bản tác giả do trang tìm kiếm
chỉ ra ở cefns.nau.edu: kết nối bị từ chối (ECONNREFUSED / 302 rỗng), web.archive.org không có bản lưu. Đọc bản PDF đầy đủ 27 trang
(trang 57–83, có đầu trang “Artificial Intelligence 134 (2002) 57–83”, PII S0004-3702(01)00129-1) lưu ở
www.cs.oswego.edu/~mgrzenda/CSC466/Paper%20Sources/Deep%20Blue.pdf (171 823 byte, sha256 db5aa5f355cdc2bc…). Đây là bản chép của
bài đã in, không phải bản do tác giả hay nhà xuất bản đăng — nội dung trùng bản in (đầu trang, số trang, PII).
- Abstract: “Deep Blue is the chess machine that defeated then-reigning World Chess Champion Garry Kasparov in a six-game match in 1997.”
  Các yếu tố: “a single-chip chess search engine, a massively parallel system with multiple levels of parallelism, a strong emphasis on
  search extensions, a complex evaluation function, and effective use of a Grandmaster game database.”
- §1.1: “In 1988 Deep Thought was the first chess machine to beat a Grandmaster in tournament play. These systems used a single-chip chess
  move generator [12] to achieve search speeds in the neighborhood of 500,000 positions per second (ChipTest) to 700,000 positions per
  second (Deep Thought).”
- §1.2: “Deep Thought 2 initially had 24 chess engines”; “the evaluation function was relatively simple”; phần vá bằng phần mềm “slowed
  down the overall system speed and created numerous search anomalies at the hardware/software boundary.”
- §1.3: “Deep Blue I ran on a 36-node IBM RS/6000 SP computer, and used 216 chess chips. The chips each searched about 1.6–2 million chess
  positions per second. Overall search speed was 50–100 million chess positions per second.” “This match was won by Kasparov by a fairly
  decisive 4–2 score” (trận tháng 2/1996).
- §1.4: “The new chess chip had a completely redesigned evaluation function, going from around 6400 features to over 8000. A number of the
  new features were in response to specific problems observed in the 1996 Kasparov games”; “per chip search speed to 2–2.5 million
  positions per second”; “we spent the vast majority of our time between the two matches designing, testing, and tuning the new evaluation
  function.” “Deep Blue defeated Garry Kasparov in the 1997 match by a score of 3.5–2.5.” Trận tái đấu “took place in May of 1997”.
- §2: “a 30-node (30-processor) IBM RS/6000 SP computer and 480 single-chip chess search engines, with 16 chess chips per SP processor.”
  “In the course of the 1997 match with Kasparov, the overall average system speed observed in searches longer than one minute was 126
  million positions per second.” “A three minute search on Deep Blue would reach a full-width depth of 12.2 on average.”
- §2 (2): “There are so many features (8000) that tuning the relative values of the features becomes a difficult task.”
- §6.3: hệ 24 chip so với 1 chip: “speedups averaged about 7, for an observed efficiency of about 30%. For quieter positions, speedups
  averaged 18, for an observed efficiency of 75%.” Cả hệ 30 nút: “an overall observed efficiency of about 8% in tactical positions and
  about 12% in quiet positions … it was a conscious design decision of the Deep Blue team to focus on improving the evaluation function
  following the 1996 Kasparov match, and the parallel search code was largely untouched between the 1996 and 1997 matches.”
- §7.3: “the large majority of the features and weights in the Deep Blue evaluation function were created/tuned by hand”; công cụ tự động
  cho thấy “the hand-tuned weights were systematically too low”.
- §8.1: “The book consisted of about 4000 positions”. §8.2: “a 700,000 game database”.
- Đọc lại 2026-11-08 (cùng bản PDF oswego, pdftotext): §8.1 “The opening book in Deep Blue was created by hand, primarily by Grandmaster
  Joel Benjamin, with assistance from Grandmasters Nick De Firmian, John Fedorowicz, and Miguel Illescas.” §8.2 “The extended book … allows
  a large Grandmaster game database to influence and direct Deep Blue's play in the absence of opening book information … a 700,000 game
  database”. §8.3 “The endgame databases did not play a critical role in the matches against Kasparov.” → bài giảng KHÔNG nói cơ sở dữ
  liệu tàn cuộc là một phần của chiến thắng (đã sửa bài học sai 2, rà soát đợt B). §7.3 trọng số “systematically too low” là trọng số
  “related to pawn shelter” (tốt che chắn vua).
- §9: “The success of Deep Blue in the 1997 match was not the result of any one factor.” “Evaluation function tuning, both automatic and
  manual, was far from complete.”

## [AG16] D. Silver và cộng sự, *Mastering the game of Go with deep neural networks and tree search*, Nature 529 (28/1/2016), từ trang 484
Bản PDF do DeepMind đăng: storage.googleapis.com/deepmind-media/alphago/AlphaGoNaturePaper.pdf (2 682 222 byte, sha256 9c9184385a3d37b4…;
đầu trang “NATURE | VOL 529 | 28 JANUARY 2016”, doi:10.1038/nature16961). Trang nature.com không cần đọc vì đây là bản in đầy đủ.
- “In large games, such as chess (b≈35, d≈80) and especially Go (b≈250, d≈150), exhaustive search is infeasible”.
- “We trained a 13-layer policy network … from 30 million positions from the KGS Go Server. The network predicted expert moves on a held
  out test set with an accuracy of 57.0% using all input features”.
- Mạng giá trị: “The naive approach of predicting game outcomes from data consisting of complete games leads to overfitting. The problem is
  that successive positions are strongly correlated, differing by just one stone, but the regression target is shared for the entire game.
  … achieving a minimum MSE of 0.37 on the test set, compared to 0.19 on the training set. To mitigate this problem, we generated a new
  self-play data set consisting of 30 million distinct positions, each sampled from a separate game. … MSEs of 0.226 and 0.234 on the
  training and test set respectively, indicating minimal overfitting.”
- “The final version of AlphaGo used 40 search threads, 48 CPUs, and 8 GPUs.” Bản phân tán: “40 search threads, 1,202 CPUs and 176 GPUs”.
- “winning 494 out of 495 games (99.8%) against other Go programs.” “Over 5–9 October 2015 AlphaGo and Fan Hui competed in a formal
  five-game match. AlphaGo won the match 5 games to 0”; “a professional 2 dan, and the winner of the 2013, 2014 and 2015 European Go
  championships”; “a feat that was previously believed to be at least a decade away”.
- “During the match against Fan Hui, AlphaGo evaluated thousands of times fewer positions than Deep Blue did in its chess match against
  Kasparov”; “while Deep Blue relied on a handcrafted evaluation function, the neural networks of AlphaGo are trained directly from
  gameplay purely through general-purpose supervised and reinforcement learning methods.”
- Methods: mạng chính sách học có giám sát “Training took around 3 weeks for 340 million training steps” (50 GPU).

## [AGZ17] D. Silver và cộng sự, *Mastering the game of Go without human knowledge*, Nature, 2017 (số tập, trang không có trong bản tác giả — không ghi)
Bản tác giả (accepted manuscript, “Mastering the Game of Go without Human Knowledge”) ở kho UCL: discovery.ucl.ac.uk/id/eprint/10045895/1/
agz_unformatted_nature.pdf (2 559 336 byte, sha256 a23add75aa06054c…). Trang nature.com không đọc (bản tác giả đủ cho các câu dưới đây).
- Abstract: “an algorithm based solely on reinforcement learning, without human data, guidance, or domain knowledge beyond game rules.”
  “Starting tabula rasa, our new program AlphaGo Zero achieved superhuman performance, winning 100-0 against the previously published,
  champion-defeating AlphaGo.”
- “AlphaGo Lee is the program that defeated Lee Sedol 4–1 in March, 2016.”
- §2: “Training started from completely random behaviour and continued without human intervention for approximately 3 days. Over the course
  of training, 4.9 million games of self-play were generated, using 1,600 simulations for each MCTS, which corresponds to approximately
  0.4s thinking time per move.”
- “AlphaGo Zero outperformed AlphaGo Lee after just 36 hours; for comparison, AlphaGo Lee was trained over several months. After 72 hours
  … AlphaGo Zero used a single machine with 4 Tensor Processing Units (TPUs), while AlphaGo Lee was distributed over many machines and used
  48 TPUs. AlphaGo Zero defeated AlphaGo Lee by 100 games to 0”.
- Lần chạy lớn: “continued for approximately 40 days. Over the course of training, 29 million games of self-play were generated.”
  So với AlphaGo Master: “AlphaGo Zero won by 89 games to 11”.

## [AZ17] D. Silver và cộng sự, *Mastering Chess and Shogi by Self-Play with a General Reinforcement Learning Algorithm*, arXiv:1712.01815v1, 5/12/2017
Tải: arxiv.org/pdf/1712.01815 (636 527 byte, sha256 26c43408551c22f4…).
- Abstract: “AlphaZero achieved within 24 hours a superhuman level of play in the games of chess and shogi (Japanese chess) as well as Go”.
- “the same algorithm settings, network architecture, and hyper-parameters were used for all three games.”
- “In chess, AlphaZero outperformed Stockfish after just 4 hours (300k steps)”.
- Bảng 1 (cờ vua, 100 ván, 1 phút mỗi nước): AlphaZero cầm trắng 25 thắng, 25 hoà, 0 thua; cầm đen 3 thắng, 47 hoà, 0 thua.
- “AlphaZero searches just 80 thousand positions per second in chess and 40 thousand in shogi, compared to 70 million for Stockfish”.

## [AZ18] D. Silver và cộng sự, *A general reinforcement learning algorithm that masters chess, shogi, and Go through self-play*, Science, 2018 (blog DeepMind ngày 6/12/2018 báo đăng; số tập, trang chưa đọc được — không ghi)
Thử science.org/doi/10.1126/science.aar6404 — WebFetch **403** (không xác nhận được trang này). Đọc hai nguồn chính thức của DeepMind:
(a) blog “AlphaZero: Shedding new light on chess, shogi, and Go”, ngày “December 6, 2018” — deepmind.google/discover/blog/
alphazero-shedding-new-light-on-chess-shogi-and-go/ (curl, 169 890 byte); blog ghi “the full evaluation of AlphaZero, published in the
journal Science (Open Access version here), that confirms and updates those preliminary results.”
(b) bản truy cập mở (bản tác giả) storage.googleapis.com/deepmind-media/DeepMind.com/Blog/alphazero-shedding-new-light-on-chess-shogi-and-go/
alphazero_preprint.pdf (3 913 039 byte, sha256 9e298fbfbcfbb50c…; tiêu đề trùng bài Science). Liên kết “Open Access version” trong
trang blog nạp bằng JavaScript nên không lấy được từ HTML tĩnh; đường dẫn này nằm cùng thư mục lưu trữ của bài blog — ghi rõ là suy ra
theo đường dẫn, nội dung (tiêu đề, tác giả, kết quả 155/6/1000) khớp blog.
- (b): “Training proceeded for 700,000 steps … During training only, 5,000 first-generation tensor processing units (TPUs) were used to
  generate self-play games, and 16 second-generation TPUs were used to train the neural networks. Training lasted for approximately 9 hours
  in chess, 12 hours in shogi and 13 days in Go”.
- (b): “The training algorithm achieved similar performance in all independent runs (see fig. S3), suggesting that the high performance of
  AlphaZero's training algorithm is repeatable.”
- (b): “Stockfish and Elmo used 44 central processing unit (CPU) cores …, whereas AlphaZero and AlphaGo Zero used a single machine with four
  first-generation TPUs and 44 CPU cores”; “All matches were played using time controls of 3 hours per game, plus an additional 15 seconds
  for each move.”
- (b): “In chess, AlphaZero defeated Stockfish, winning 155 games and losing 6 games out of 1,000”; “AlphaZero defeated Stockfish in each
  opening”; “AlphaZero searches just 60,000 positions per second in chess and shogi, compared with 60 million for Stockfish”.
- (b): “we introduce AlphaZero: a more generic version of the AlphaGo Zero algorithm … using the same algorithm and network architecture
  for all three games.”
- (a): “taking approximately 9 hours for chess, 12 hours for shogi, and 13 days for Go”; “winning 155 games and losing just six games out of
  1,000”; “Traditional chess engines – including the world computer chess champion Stockfish and IBM's ground-breaking Deep Blue – rely on
  thousands of rules and heuristics handcrafted by strong human players”.

## Đọc lại 2026-11-09 (đợt C, curl + `pdftotext -layout`, cùng sha256 với các bản ở trên)
- [AZ17] (sha256 26c43408551c22f4…): “2016 Top Chess Engine Championship (TCEC) world-champion Stockfish”; “Stockfish …, an open source
  program that won the 2016 TCEC computer chess championship”.
- [AZ18] bản truy cập mở (sha256 9e298fbfbcfbb50c…): “The chess match was played against the 2016 TCEC (season 9) world champion
  Stockfish”. → câu “chương trình vô địch giải máy cờ vua năm 2016” ở cảnh mở đầu L14 khớp nguồn.
- [AGZ17] “AlphaGo Zero used a single machine with 4 Tensor Processing Units (TPUs), while AlphaGo Lee was distributed over many machines
  and used 48 TPUs” → bài nay nói “ít bộ tăng tốc hơn 12 lần” (bản cũ ghi “ít máy hơn 12 lần”: sai đơn vị, 12 là tỉ số TPU, không phải số máy).

## Điều KHÔNG dạy (nguồn không ghi hoặc chưa đọc)
- Số ván hoà của trận 1000 ván 2018: nguồn chỉ ghi 155 thắng, 6 thua → 839 hoà là PHÉP TÍNH (1000 − 155 − 6), ghi rõ là tính ra.
- Diễn biến từng ván 1996/1997, “nước đi gây tranh cãi”, chuyện máy “bị nghi gian lận”, Deep Blue bị tháo dỡ sau trận: không có trong
  [DB02] → không dạy.
- Trận 2016 với kỳ thủ Hàn Quốc chỉ dạy đúng câu của [AGZ17] (“4–1 in March, 2016”); chi tiết ván 4, “nước 37”: không đọc → không dạy.
- Phần cứng của AlphaGo trong trận 3/2016 ngoài “48 TPUs” của [AGZ17]: không dạy.
- Chi phí tiền điện, giá thuê TPU: không có nguồn → không dạy. Mọi “máy của bạn” trong quiz là SỐ MINH HOẠ.
- Bản Science 2018 trên science.org: không đọc được (403); dạy theo bản truy cập mở và blog chính thức của DeepMind.
- Tên người (kỳ thủ, tác giả) không đọc trong lời; trên màn hình chỉ ở dòng nguồn.
