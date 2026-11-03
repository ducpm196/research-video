# Nguồn bài RLN L04 — Monte Carlo và TD(0)

Đọc 2026-11-02, bản PDF chính thức [SB18] R. S. Sutton, A. G. Barto, *Reinforcement Learning: An Introduction*, bản 2 (2018),
`http://incompleteideas.net/book/RLbook2020.pdf` (tải bằng curl qua http từ máy chủ chính thức, vì https báo chứng chỉ tự ký;
trích bằng pdftotext — ký tự Hy Lạp mất khi trích, ghi lại trong ngoặc vuông).

| Mục | Câu trích nguyên văn | Dùng ở |
|---|---|---|
| ch. 6 mở đầu | “Like Monte Carlo methods, TD methods can learn directly from raw experience without a model of the environment's dynamics. Like DP, TD methods update estimates based in part on other learned estimates, without waiting for a final outcome (they bootstrap).” | hook, ôn nền, “tự khởi động” |
| 6.1, (6.1) | “V(St) ← V(St) + [α][Gt − V(St)], (6.1) where Gt is the actual return following time t, and [α] is a constant step-size parameter … Let us call this method constant-[α] MC.” | công thức bước 2 |
| 6.1 | “Whereas Monte Carlo methods must wait until the end of the episode to determine the increment to V(St) (only then is Gt known), TD methods need to wait only until the next time step.” | hình, lỗi 3 |
| 6.1, (6.2) | “V(St) ← V(St) + [α][Rt+1 + [γ]V(St+1) − V(St)] (6.2) … the target for the Monte Carlo update is Gt, whereas the target for the TD update is Rt+1 + [γ]V(St+1). This TD method is called TD(0), or one-step TD” | công thức bước 3 |
| 6.1 | “Because TD(0) bases its update in part on an existing estimate, we say that it is a bootstrapping method, like DP.” | “tự khởi động”, lỗi 1 |
| 6.1 | “the quantity in brackets in the TD(0) update is a sort of error … This quantity, called the TD error” | ký hiệu đen-ta |
| Ví dụ 6.2 | “all episodes start in the center state, C, then proceed either left or right by one state on each step, with equal probability … the true value of each state is the probability of terminating on the right if starting from that state. Thus, the true value of the center state is v(C) = 0.5.” | tự kiểm (1/6 … 5/6 tính lại bằng giải hệ) |
| Ví dụ 6.2 | “with a constant step-size parameter ([α] = 0.1 in this example), the values fluctuate indefinitely in response to the outcomes of the most recent episodes” ; “the approximate value function was initialized to the intermediate value V(s) = 0.5, for all s” | tự kiểm, lỗi 4 |
| Ví dụ 6.4 | “Suppose you observe the following eight episodes: A, 0, B, 0 / B, 1 / B, 1 / B, 1 / B, 1 / B, 1 / B, 1 / B, 0” ; “the optimal value for V(B) is 3/4” | hook, ví dụ |
| Ví dụ 6.4 | “which indeed in this case gives V(A) = 3/4. This is also the answer that batch TD(0) gives.” ; “we therefore estimate V(A) as 0. This is the answer that batch Monte Carlo methods give. Notice that it is also the answer that gives minimum squared error on the training data.” | ví dụ bước 2–4 |
| Ví dụ 6.4 | “If the process is Markov, we expect that the first answer will produce lower error on future data, even though the Monte Carlo answer is better on the existing data.” | ví dụ bước 4 |

Số tự tính (không phải của sách, kiểm bằng checks + verify_parts/L04.py): độ lệch trung bình 100 lần chạy 0,236 / 0,128 / 0,055
(α = 0,1 sau 0 / 10 / 100 lượt), 0,055 và 0,024 sau 1000 lượt (α = 0,1 / 0,02) — mô phỏng của bài, không phải số đọc từ hình của sách.

## Điều KHÔNG dạy (nguồn không ghi)
- Không nói “sai phân thời gian luôn học nhanh hơn”: sách ghi đây là câu hỏi mở (“no one has been able to prove mathematically that one
  method converges faster than the other”), chỉ “usually been found to converge faster … on stochastic tasks”.
- Không đọc số trên đồ thị của sách; mọi đường học trong bài là mô phỏng của chính bài.
- Ví dụ khách hàng 30 ngày và các số 4, 6, 8; V = 6; V(s′) = 10 là SỐ MINH HOẠ.
