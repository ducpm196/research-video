# Nguồn bài RLN L06 — xấp xỉ hàm và mạng Q sâu

Đọc 2026-11-02. Tải PDF bằng WebFetch (bản chính thức), trích chữ bằng pdftotext; ký tự Hy Lạp mất khi trích, ghi trong ngoặc vuông.

- **[D13]** V. Mnih và cộng sự, *Playing Atari with Deep Reinforcement Learning*, arXiv:1312.5602 (2013), `https://arxiv.org/pdf/1312.5602`.
- **[D15]** V. Mnih và cộng sự, *Human-level control through deep reinforcement learning*, Nature 518 (2015), bản PDF do nhóm tác giả đăng
  `https://storage.googleapis.com/deepmind-media/dqn/DQNNaturePaper.pdf`.
- **[SB18]** Sutton & Barto bản 2 (2018), `http://incompleteideas.net/book/RLbook2020.pdf` (curl qua http; https báo chứng chỉ tự ký).
- **[R17]** M. Hessel và cộng sự, *Rainbow*, arXiv:1710.02298, `https://arxiv.org/pdf/1710.02298`.

| Nguồn | Câu trích nguyên văn | Dùng ở |
|---|---|---|
| D13 tóm tắt | “We apply our method to seven Atari 2600 games from the Arcade Learning Environment … We find that it outperforms all previous approaches on six of the games and surpasses a human expert on three of them.” | hook (7 trò, 6, 3) |
| D13 mục 5 | “In these experiments, we used the RMSProp algorithm with minibatches of size 32. The behavior policy during training was [ε]-greedy with [ε] annealed linearly from 1 to 0.1 over the first million frames, and fixed at 0.1 thereafter. We trained for a total of 10 million frames and used a replay memory of one million most recent frames.” | hình (1 triệu bước, lô 32), quy ước |
| D13 mục 4 | “we store the agent's experiences at each time-step, et = (st, at, rt, st+1) in a data-set D = e1, ..., eN, pooled over many episodes into a replay memory … drawn at random from the pool of stored samples” | hình, ví dụ bước 4 |
| D15 | “Reinforcement learning is known to be unstable or even to diverge when a nonlinear function approximator such as a neural network is used to represent the action-value (also known as Q) function.” | hook, lỗi 4 |
| D15 | “we used a biologically inspired mechanism termed experience replay that randomizes over the data, thereby removing correlations in the observation sequence and smoothing over changes in the data distribution” | ví dụ bước 4 |
| D15 Methods | “every C updates we clone the network Q to obtain a target network Q^ and use Q^ for generating the Q-learning targets yj for the following C updates to Q. This modification makes the algorithm more stable compared to standard online Q-learning, where an update that increases Q(st,at) often also increases Q(st+1,a) for all a and hence also increases the target yj, possibly leading to oscillations or divergence of the policy.” | công thức bước 3–4, lỗi 1 |
| D15 | “… across a set of 49 games, using the same algorithm, network architecture and hyperparameters” ; “achieving more than 75% of the human score on more than half of the games (29 games” | quy ước (không đưa lên màn hình bài này; dùng ở L13) |
| D15 Methods | “for a total of 50 million frames (that is, around 38 days of game experience in total) and used a replay memory of 1 million most recent frames.” | quy ước |
| SB18 11.3 | “the danger of instability and divergence arises whenever we combine all of the following three elements, making up what we call the deadly triad: Function approximation … Bootstrapping … Off-policy training” ; “If any two elements of the deadly triad are present, but not all three, then instability can be avoided.” | lỗi 4 |
| R17 | “Double DQN (DDQN; van Hasselt, Guez, and Silver 2016) addresses an overestimation bias of Q-learning (van Hasselt 2010), by decoupling selection and evaluation of the bootstrap action.” | lỗi 3 |

## Điều KHÔNG dạy (nguồn không ghi được / không đọc được)
- Giá trị cụ thể của C (tần suất chép mạng mục tiêu) nằm trong bảng siêu tham số dạng ảnh của [D15] — pdftotext không trích được,
  nên bài chỉ nói “mỗi C lần cập nhật”, không nêu con số (NOT_VERIFIED).
- [D13] lấy mẫu từ bộ nhớ “at random”; bài dùng mô hình lấy đều, độc lập để tính số cặp liền nhau (kỳ vọng 0,000992; đếm chính xác
  không hoàn lại cũng 0,000992) — đây là phép tính của bài, không phải số của bài báo.
- Ví dụ 3 hành động lệch ±1 (kỳ vọng max = 0,75), mô hình một tham số θ·x, ảnh 10 × 10 điểm, bộ nhớ 50 000 là SỐ MINH HOẠ.
- Không nói “mạng Q sâu đạt trình độ người ở mọi trò” — chỉ đúng các con số trích ở trên.
