# Nguồn bài RLN L00 — lợi nhuận chiết khấu

Đọc 2026-11-02 từ bản PDF chính thức của sách (tải trực tiếp từ trang tác giả, `http://incompleteideas.net/book/RLbook2020.pdf`,
73 129 769 byte; WebFetch qua https báo “self signed certificate” nên tải bằng curl qua http từ cùng máy chủ chính thức — không dùng
dịch vụ trung gian). Trích bằng `pdftotext`; ký tự Hy Lạp mất khi trích, ghi lại trong ngoặc vuông.

**[SB18]** R. S. Sutton, A. G. Barto, *Reinforcement Learning: An Introduction*, bản 2, MIT Press 2018 (bản PDF 2020).

| Mục | Câu trích nguyên văn | Dùng ở |
|---|---|---|
| ch. 1 | “Reinforcement learning is learning what to do--how to map situations to actions--so as to maximize a numerical reward signal. The learner is not told which actions to take, but instead must discover which actions yield the most reward by trying them.” | hình vòng lặp: “không ai nói cho tác tử biết hành động nào là đúng” |
| 3.1 | “The learner and decision maker is called the agent. The thing it interacts with, comprising everything outside the agent, is called the environment.” | ký hiệu, hình vòng lặp |
| 3.3, (3.8) | “where [γ] is a parameter, 0 ≤ [γ] ≤ 1, called the discount rate.” | ký hiệu γ |
| 3.3 | “a reward received k time steps in the future is worth only [γ]^(k−1) times what it would be worth if it were received immediately. If [γ] < 1, the infinite sum in (3.8) has a finite value as long as the reward sequence {Rk} is bounded.” | chiết khấu, tổng hữu hạn |
| 3.3, (3.9) | “Note that this works for all time steps t < T , even if termination occurs at t + 1, provided we define GT = 0. This often makes it easy to compute returns from reward sequences.” | công thức đệ quy G_t = r_{t+1} + γ·G_{t+1}, tính ngược |
| 3.3, (3.10) | “if the reward is a constant +1, then the return is G_t = Σ_k [γ]^k = 1 / (1 − [γ])” | tổng 1 / (1 − γ) |
| 3.4 | “… including the possibility that [γ] = 1 if the sum remains defined (e.g., because all episodes terminate).” | γ = 1 chỉ dùng được khi lượt chơi kết thúc |
| Bài tập 3.16 | “Now consider adding a constant c to all the rewards in an episodic task, such as maze running. Would this have any effect, or would it leave the task unchanged as in the continuing task above?” | lỗi 4: cộng hằng số vào mọi phần thưởng của nhiệm vụ có lượt chơi (bài giảng tự tính ví dụ, không trích đáp án) |

Ghi chú về chỉ số: sách viết phần thưởng sau bước 1 là $R_{t+1}$, nên phần thưởng thứ k được nhân $γ^{k−1}$; bài giảng viết $r_1, r_2, r_3$
và “chậm k bước nhân γ mũ k” với k đếm từ 0 (phần thưởng đầu nhân γ⁰ = 1) — cùng một công thức.

## Điều KHÔNG dạy (nguồn không ghi)
- Không gán γ cho một “mức kiên nhẫn” cụ thể của người; “đường chân trời 1 / (1 − γ)” là cách hiểu theo (3.10), bài nói “khoảng”.
- Ví dụ trò chơi 6 điểm / 10 điểm, chuỗi −1, −1, 10 và “thưởng sống sót +2” là SỐ MINH HOẠ dựng tay, kiểm bằng `checks` và verify_parts/L00.py.
