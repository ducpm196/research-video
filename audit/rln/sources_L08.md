# Nguồn bài RLN L08 — diễn viên–nhà phê bình và hàm lợi thế

Đọc 2026-11-02, bản PDF chính thức [SB18] Sutton & Barto, *Reinforcement Learning: An Introduction*, bản 2 (2018),
`http://incompleteideas.net/book/RLbook2020.pdf` (curl qua http từ máy chủ chính thức; https báo chứng chỉ tự ký). Trích bằng pdftotext.

| Mục | Câu trích nguyên văn | Dùng ở |
|---|---|---|
| 13.5 | “In REINFORCE with baseline, the learned state-value function estimates the value of the first state of each state transition. This estimate sets a baseline for the subsequent return, but is made prior to the transition's action and thus cannot be used to assess that action.” | hook, công thức bước 1 |
| 13.5 | “The estimated value of the second state, when discounted and added to the reward, constitutes the one-step return, Gt:t+1, which is a useful estimate of the actual return and thus is a way of assessing the action.” | công thức bước 2 |
| 13.5 | “the one-step return is often superior to the actual return in terms of its variance and computational congeniality, even though it introduces bias.” | quiz câu 3 (đánh đổi) |
| 13.5 | “When the state-value function is used to assess actions in this way it is called a critic, and the overall policy-gradient method is termed an actor–critic method. Note that the bias in the gradient estimate is not due to bootstrapping as such; the actor would be biased even if the critic was learned by a Monte Carlo method.” | ký hiệu, hình, lỗi 1 và lỗi 4 (nhà phê bình sai → diễn viên lệch) |
| 13.5 | “One-step actor–critic methods replace the full return of REINFORCE (13.11) with the one-step return (and use a learned state-value function as the baseline) … = θt + [α] [δ]t [∇]π(At\|St, θt) / π(At\|St, θt)” | công thức, ví dụ |
| 13.5 | “The main appeal of one-step methods is that they are fully online and incremental” | hook (học sau từng bước) |

## Điều KHÔNG dạy (nguồn không ghi)
- Câu “kỳ vọng của đen-ta bằng lợi thế” là phép suy của bài từ định nghĩa Q của bài 1 (kiểm bằng số: 0,6 ở checks và mô phỏng
  verify_parts/L08.py), không phải câu trích.
- Không nêu tên các biến thể đời sau (A2C, A3C, GAE); bài sau (PPO) dùng lợi thế này.
- Mọi số (r = 1, V = 4, 5, 3, 14, α = 0,1 và 0,2, lượt 10 000 bước) là SỐ MINH HOẠ.
