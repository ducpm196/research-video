# Nguồn bài RLN L13 — hành trình: học chơi trò Atari 2013–2020

Đọc 2026-11-02. Mọi PDF tải bằng WebFetch (trả nhị phân → lưu) rồi trích chữ bằng `pdftotext`; ký tự lạ do trích ghi lại trong ngoặc vuông.

| Nhãn | Nguồn | URL đã đọc |
|---|---|---|
| [D13] | V. Mnih và cộng sự, *Playing Atari with Deep Reinforcement Learning*, arXiv:1312.5602 (2013) | `https://arxiv.org/pdf/1312.5602` |
| [D15] | V. Mnih và cộng sự, *Human-level control through deep reinforcement learning*, Nature 518 (2015) 529–533 | `https://storage.googleapis.com/deepmind-media/dqn/DQNNaturePaper.pdf` (bản PDF do nhóm tác giả đăng) |
| [R17] | M. Hessel và cộng sự, *Rainbow: Combining Improvements in Deep Reinforcement Learning*, arXiv:1710.02298 (2017) | `https://arxiv.org/pdf/1710.02298` |
| [M18] | M. C. Machado, M. G. Bellemare, E. Talvitie, J. Veness, M. Hausknecht, M. Bowling, *Revisiting the Arcade Learning Environment: Evaluation Protocols and Open Problems for General Agents*, arXiv:1709.06009 v2 (1/12/2017), JAIR 61 (2018) | `https://arxiv.org/pdf/1709.06009` |
| [A20] | A. P. Badia và cộng sự, *Agent57: Outperforming the Atari Human Benchmark*, arXiv:2003.13350 (30/3/2020) | `https://arxiv.org/pdf/2003.13350` |

## Câu trích nguyên văn

| Nguồn | Câu trích | Dùng ở |
|---|---|---|
| [D13] tóm tắt | “The model is a convolutional neural network, trained with a variant of Q-learning, whose input is raw pixels and whose output is a value function estimating future rewards. We apply our method to seven Atari 2600 games from the Arcade Learning Environment, with no adjustment of the architecture or learning algorithm. We find that it outperforms all previous approaches on six of the games and surpasses a human expert on three of them.” | hook (7 trò), chặng 1 |
| [D13] 4 | “Second, learning directly from consecutive samples is inefficient, due to the strong correlations between the samples; randomizing the samples breaks these correlations and therefore reduces the variance of the updates. Third, when learning on-policy the current parameters determine the next data sample … It is easy to see how unwanted feedback loops may arise” | chặng 1 (điểm nghẽn) |
| [D13] 5 | “we used the RMSProp algorithm with minibatches of size 32. The behavior policy during training was [ε]-greedy with [ε] annealed linearly from 1 to 0.1 over the first million frames, and fixed at 0.1 thereafter. We trained for a total of 10 million frames and used a replay memory of one million most recent frames.” | chặng 1 (lịch epsilon: 0,775 / 0,55 / 90% là phép tính lại) |
| [D13] 5 | “the agent sees and selects actions on every kth frame instead of every frame, and its last action is repeated on skipped frames … We use k = 4 for all games except Space Invaders” | khung / bước quyết định |
| [D15] | “Reinforcement learning is known to be unstable or even to diverge when a nonlinear function approximator such as a neural network is used to represent the action-value (also known as Q) function.” | chặng 2 (điểm nghẽn) |
| [D15] | “The target network parameters [θ⁻] are only updated with the Q-network parameters ([θ]) every C steps and are held fixed between individual updates” | chặng 2 (mạng đích) |
| [D15] | “Our DQN method outperforms the best existing reinforcement learning methods on 43 of the games … achieving more than 75% of the human score on more than half of the games (29 games” ; “across the set of 49 games” | chặng 2 (43, 29, 49) |
| [D15] Hình 3 | “the normalized performance of DQN, expressed as a percentage, is calculated as: 100 × (DQN score − random play score)/(human score − random play score)” ; “Error bars indicate s.d. across the 30 evaluation episodes” | ký hiệu (điểm chuẩn hoá) |
| [D15] Methods | “We trained for a total of 50 million frames (that is, around 38 days of game experience in total) and used a replay memory of 1 million most recent frames.” ; “We use k = 4 for all games.” ; “(210 × 160 colour video at 60 Hz)” | hook, chặng 2 (9,6 / 38,6 ngày là phép tính lại) |
| [D15] Methods | “The professional human tester used the same emulator engine as the agents” ; “Audio output was disabled for both human players and agents.” | chặng 2 (điều kiện của thực hành) |
| [R17] tóm tắt | “This paper examines six extensions to the DQN algorithm and empirically studies their combination.” | chặng 3 |
| [R17] Hình 1 | “we match DQN's best performance after 7M frames, surpass any baseline within 44M frames” | chặng 3 |
| [R17] | “The 7M frames required to match DQN's final performance correspond to less than 10 hours of wall-clock time. A full run of 200M frames corresponds to approximately 10 days” ; “we ran each agent on a single GPU” | chặng 3 (28,6 lần; 20 triệu khung/ngày; 231 khung/giây là phép tính lại), quiz |
| [R17] | “Rainbow achieves a median score of 223% in the no-ops regime; in the human starts regime we measured a median score of 153%.” ; “the difference between the two regimes indicates the extent to which the agent has over-fit to its own trajectories.” | chặng 3 (70 điểm phần trăm là phép tính lại) |
| [R17] | “Prioritized replay and multi-step learning were the two most crucial components of Rainbow … (the full Rainbow performed better than either ablation in 53 games out of 57).” | chặng 3 |
| [R17] | “Double DQN … addresses an overestimation bias of Q-learning” | chặng 3 (“chống đánh giá quá cao”) |
| [M18] tóm tắt | “we introduce a new version of the ALE that supports multiple game modes and provides a form of stochasticity we call sticky actions.” | chặng 4 (phiên bản mới) |
| [M18] 4 | “Currently, it is fairly standard to train agents for 200 million frames, in order to facilitate comparison with the DQN results reported by Mnih et al. (2015). This is equivalent to approximately 38 days of real-time gameplay” | hook, chặng 4 (38,6 ngày là phép tính lại) |
| [M18] 3 | “we advocate taking the number of skipped frames into consideration when measuring training data” | khung (đếm khung), bài học sai 2 |
| [M18] 3 | “we recommend that only the game over signal be used for termination.” | chặng 4 |
| [M18] 5.1 | “Bellemare et al. (2015), using a different evaluation protocol, reports that the Brute outperformed the best learning method at the time on 45 out of 55 Atari 2600 games. However, … this performance critically depends on the environment's determinism.” | chặng 4, bài học sai 3 |
| [M18] 5.2 | “In other words, if [ς] = 0.25, there is 25% chance the environment will not execute the desired action right away.” ; “We can see that the Brute is the only algorithm substantially impacted by the sticky actions.” | ký hiệu, chặng 4 (0,75 và 0,25⁴ là phép tính lại) |
| [M18] 6 | “evaluating the final performance while learning, at 10, 50, 100 and 200 million frames. We computed score averages of each trial using the 100 final episodes … We report the average over 5 trials for DQN” ; “in 60 different Atari 2600 games” | chặng 4, quiz |
| [A20] tóm tắt | “We propose Agent57, the first deep RL agent that outperforms the standard human benchmark on all 57 Atari games.” | hook, chặng 5 |
| [A20] 1 | “despite the human baseline scores potentially underestimating human performance relative to what is possible” | bài học sai 1 |
| [A20] 1 | “MuZero (Schrittwieser et al., 2019), and in model-free RL, R2D2 (Kapturowski et al., 2018) surpass 100% HNS on 51 and 52 games, respectively. … in the games they fail to do so, they often fail to learn completely.” | chặng 5 (51, 52 — trên màn hình ghi 2018, 2019) |
| [A20] 1 | “Games like Private Eye, Montezuma's Revenge, Pitfall! or Venture are widely considered hard exploration games … as hundreds of actions may be required before a first positive reward is seen.” ; “The reward, given only at the end, is proportional to the time elapsed.” (trò Skiing) | chặng 5 |
| [A20] 5 | “Agent57 uses the first 5 billion frames to surpass the human benchmark on 51 games. … Lastly, Agent57 surpasses the human benchmark on Skiing after 78 billion frames.” ; “in the game of Skiing, the human baseline is very competitive, with a score of -4336.9, where -17098.1 is random and -3272 is the optimal score one can achieve.” | chặng 5 (390 lần, 25 lần, 108,3% là phép tính lại) |
| [A20] 4.4 | “running R2D2 with a high discount factor, [γ] = 0.9999 surpasses the human baseline in the game of Skiing.” ; “Using the meta-controller allows to include very high discount values” | chặng 5 (γ = 0,9999; 10 000 bước là phép tính lại theo bài 0) |
| [A20] tóm tắt | “we train a neural network which parameterizes a family of policies ranging from very exploratory to purely exploitative. We propose an adaptive mechanism to choose which policy to prioritize” | thực hành chặng 5 |

## Điều KHÔNG dạy (nguồn không ghi hoặc không trích được)
- **Giá trị C** của mạng đích (năm 2015): chỉ có trong Bảng mở rộng 1 dạng ảnh, pdftotext không trích được → NOT_VERIFIED, bài chỉ nói “mỗi C bước”.
- Không đổi 10 triệu khung (2013), 5 tỉ hay 78 tỉ khung (2020) sang ngày chơi: các bài này không nói rõ đếm khung của máy hay bước
  quyết định; bài chỉ so tỉ lệ với 200 triệu khung (390 lần, 25 lần) và nói “theo cách đếm của chính bài báo”.
- “3900 ngày” ở bài học sai 4 là phép tính lại từ tốc độ của [R17] (20 triệu khung/ngày, một GPU), không phải chi phí thật của [A20].
- Câu đố (một GPU, một tuần, 5 lần chạy, 28 triệu khung) là SỐ MINH HOẠ dựa trên tốc độ của [R17] và chuẩn báo cáo của [M18].
- Ví dụ điểm chuẩn hoá (60 / 10 / 110 → 50%) là SỐ MINH HOẠ.
- Không đọc tên hệ thống (DQN, Rainbow, Agent57, MuZero, R2D2), tên trò (Skiing, Montezuma's Revenge…), tên nhóm/công ty, tên tác giả
  trong lời đọc; probe audit/rln/probes/p1_thuat_ngu chưa cho tên nào đạt (nhánh chính quyết định luật đọc).
- Không trùng AIF bài 14 (Deep Blue → AlphaZero): bài này không nói về cờ hay tìm kiếm cây.
