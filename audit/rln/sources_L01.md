# Nguồn bài RLN L01 — hàm giá trị và phương trình Bellman kỳ vọng

Đọc 2026-11-02 từ bản PDF chính thức **[SB18]** Sutton & Barto, *Reinforcement Learning: An Introduction*, bản 2 (2018),
`http://incompleteideas.net/book/RLbook2020.pdf` (cách tải ghi ở sources_L00.md). Ký tự Hy Lạp mất khi trích, ghi lại trong ngoặc vuông.

| Mục | Câu trích nguyên văn | Dùng ở |
|---|---|---|
| 3.5 | “Formally, a policy is a mapping from states to probabilities of selecting each possible action. If the agent is following policy [π] at time t, then [π](a\|s) is the probability that At = a if St = s.” | ký hiệu π(a \| s) |
| 3.5 | “the "\|" in the middle of [π](a\|s) merely reminds us that it defines a probability distribution over a ∈ A(s) for each s ∈ S.” | đọc vạch đứng là “khi biết” |
| 3.5 | “The value function of a state s under a policy [π], denoted v[π](s), is the expected return when starting in s and following [π] thereafter.” | định nghĩa V(s); ghi chú cách viết v_π |
| 3.5 | “Equation (3.14) is the Bellman equation for v[π]. It expresses a relationship between the value of a state and the values of its successor states.” | phương trình tự nhất quán |
| 3.6 | “Because v[*] is the value function for a policy, it must satisfy the self-consistency condition given by the Bellman equation for state values (3.14).” | tên gọi “tự nhất quán”; lỗi 3 (lấy max là phương trình tối ưu, khác) |
| 4.1 | “If the environment's dynamics are completely known, then (4.4) is a system of \|S\| simultaneous linear equations in \|S\| unknowns … In principle, its solution is a straightforward, if tedious, computation.” | giải hệ; lỗi 4 (giải thẳng tốn kém) |
| 4.1 | “the sequence {vk} can be shown in general to converge to v[π] as k → ∞ … This algorithm is called iterative policy evaluation.” | tự kiểm 2: lặp tới điểm bất động |
| 3.6 | “Because the game has about 10^20 states, it would take thousands of years on today's fastest computers to solve the Bellman equation for v[*]” | (không dạy con số này; lỗi 4 tự tính 10 000 trạng thái) |

## Điều KHÔNG dạy (nguồn không ghi)
- Trò hai ô A, B và mọi con số (5,263; 4,737; 3,448; 3,103; 2,667; 1,333) là SỐ MINH HOẠ, tính lại trong checks và verify_parts/L01.py.
- “800 triệu byte”, “n³/3 phép tính” là phép đếm của phép khử Gauss thông thường (khoá Toán cho khoa học máy tính), không trích từ sách.
