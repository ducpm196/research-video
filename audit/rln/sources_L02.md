# Nguồn bài RLN L02 — lặp chính sách và tốc độ hội tụ của lặp giá trị

Đọc 2026-11-02 từ bản PDF chính thức **[SB18]** Sutton & Barto, bản 2 (2018), `http://incompleteideas.net/book/RLbook2020.pdf`
(cách tải ghi ở sources_L00.md). Ký tự Hy Lạp mất khi trích, ghi lại trong ngoặc vuông.

| Mục | Câu trích nguyên văn | Dùng ở |
|---|---|---|
| 4.2 | “That this is true is a special case of a general result called the policy improvement theorem.” … “Thus, if q[π](s, a) > v[π](s), then the changed policy is indeed better than [π].” | bước cải thiện: đổi khi Q lớn hơn V |
| 4.2 | “The greedy policy takes the action that looks best in the short term--after one step of lookahead--according to v[π]. By construction, the greedy policy meets the conditions of the policy improvement theorem (4.7), so we know that it is as good as, or better than, the original policy.” | hình vòng đánh giá – cải thiện |
| 4.3 | “Each policy is guaranteed to be a strict improvement over the previous one (unless it is already optimal). Because a finite MDP has only a finite number of deterministic policies, this process must converge to an optimal policy and the optimal value function in a finite number of iterations.” | hữu hạn vòng; lỗi 2 (chỉ đổi khi tốt hơn hẳn — để mỗi chính sách là cải thiện thật) |
| 4.3 | “Policy iteration often converges in surprisingly few iterations” | hook: 3 lần đánh giá |
| 4.4 | “One drawback to policy iteration is that each of its iterations involves policy evaluation, which may itself be a protracted iterative computation requiring multiple sweeps through the state set.” | lỗi 3 |
| 4.4 | “the policy evaluation step of policy iteration can be truncated in several ways without losing the convergence guarantees of policy iteration. One important special case is when policy evaluation is stopped after just one sweep (one update of each state). This algorithm is called value iteration.” | lỗi 3 (đánh giá dở dang), quan hệ hai thuật toán |
| 4.4 | “Like policy evaluation, value iteration formally requires an infinite number of iterations to converge exactly to v[*]. In practice, we stop once the value function changes by only a small amount in a sweep.” | lỗi 4 (điều kiện dừng theo thay đổi giữa hai vòng) |
| 3 (ghi chú lịch sử) | “Action-value functions also played a central role in Denardo's (1967) theoretical treatment of dynamic programming in terms of contraction mappings.” | tên gọi “tính co” |

## Điều KHÔNG dạy (nguồn không ghi)
- Bất đẳng thức co e_{k+1} ≤ γ·e_k và cận γ/(1 − γ) của lỗi 4 được SUY RA tại chỗ trong bài (vì thưởng như nhau, max không làm xa hơn,
  tổng cấp số nhân), không trích từ sách; kiểm bằng máy trong verify_parts/L02.py.
- Trò “chờ / đi / ở / về”, “kho hàng”, “1 giây mỗi vòng”, “15 phút” là SỐ MINH HOẠ.
