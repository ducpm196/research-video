# Nguồn bài RLN L05 — học Q (Q-learning) và SARSA

Đọc 2026-11-02, bản PDF chính thức [SB18] Sutton & Barto, *Reinforcement Learning: An Introduction*, bản 2 (2018),
`http://incompleteideas.net/book/RLbook2020.pdf` (curl qua http từ máy chủ chính thức; https báo chứng chỉ tự ký). Trích bằng pdftotext,
ký tự Hy Lạp mất khi trích, ghi lại trong ngoặc vuông.

| Mục | Câu trích nguyên văn | Dùng ở |
|---|---|---|
| 6.4, (6.7) | “Q(St, At) ← Q(St, At) + [α][Rt+1 + [γ]Q(St+1, At+1) − Q(St, At)]. (6.7)” | công thức bước 2 |
| 6.4 | “If St+1 is terminal, then Q(St+1, At+1) is defined as zero. This rule uses every element of the quintuple of events, (St, At, Rt+1, St+1, At+1), that make up a transition from one state–action pair to the next. This quintuple gives rise to the name Sarsa for the algorithm.” | tên SARSA, lỗi 3 (ô kết thúc = 0) |
| 6.5, (6.8) | “One of the early breakthroughs in reinforcement learning was the development of an off-policy TD control algorithm known as Q-learning (Watkins, 1989), defined by Q(St, At) ← Q(St, At) + [α][Rt+1 + [γ] max_a Q(St+1, a) − Q(St, At)].” | công thức bước 3, năm 1989 |
| 6.5 | “In this case, the learned action-value function, Q, directly approximates q*, the optimal action-value function, independent of the policy being followed.” | “học giá trị của cách chơi tham lam”, lỗi 1 |
| Ví dụ 6.6 | “This gridworld example compares Sarsa and Q-learning, highlighting the difference between on-policy (Sarsa) and off-policy (Q-learning) methods.” ; “Reward is −1 on all transitions except those into the region marked "The Cliff." Stepping into this region incurs a reward of −100 and sends the agent instantly back to the start.” | hook, hình |
| Ví dụ 6.6 | “the performance of the Sarsa and Q-learning methods with [ε]-greedy action selection, [ε] = 0.1. After an initial transient, Q-learning learns values for the optimal policy, that which travels right along the edge of the cliff. Unfortunately, this results in its occasionally falling off the cliff because of the [ε]-greedy action selection. Sarsa, on the other hand, takes the action selection into account and learns the longer but safer path through the upper part of the grid. Although Q-learning actually learns the values of the optimal policy, its online performance …” | ví dụ bước 4, tự kiểm, lỗi 2 |

Kích thước lưới 4 × 12 (vách 10 ô) lấy theo hình của Ví dụ 6.6; đường tối ưu 13 bước và đường hàng trên 17 bước là bài tự đếm (kiểm
bằng lặp giá trị trong verify_parts/L05.py). Tốc độ học α = 0,1 là số bài chọn (không đọc được α trong phần đã trích).
Các số −47, −23, 0,30 và 0,05 lần rơi là mô phỏng của bài (20 lần chạy × 500 lượt), được kiểm lại bằng đánh giá chính xác hai chính sách
epsilon tham lam (−46,6 và −22,3; 0,304 và 0,029 lần rơi) — không phải số đọc từ đồ thị của sách.

## Điều KHÔNG dạy (nguồn không ghi)
- Không đọc giá trị trên đồ thị của sách (đồ thị có trục “Sum of rewards during episode” từ −100 tới −25; bài dùng số mô phỏng của mình).
- Không khẳng định một phương pháp “luôn tốt hơn”; sách chỉ so “online performance” khi còn epsilon tham lam.
- Ví dụ robot kho hàng cạnh cầu thang là SỐ MINH HOẠ.
- Bài báo Watkins & Dayan (Machine Learning, 1992) không đọc được bản toàn văn (nhà xuất bản thu phí) — chỉ dẫn qua [SB18] (năm 1989
  là năm sách ghi cho luận án của Watkins); NOT_VERIFIED trực tiếp.
