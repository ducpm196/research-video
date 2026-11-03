# Nguồn bài RLN L11 — khai thác phần thưởng

Đọc 2026-11-02.

**[DM20]** V. Krakovna và cộng sự, *Specification gaming: the flip side of AI ingenuity*, blog DeepMind, 21/4/2020,
`https://deepmind.google/discover/blog/specification-gaming-the-flip-side-of-ai-ingenuity/` (WebFetch, đọc được).
**[A16]** D. Amodei, C. Olah, J. Steinhardt, P. Christiano, J. Schulman, D. Mané, *Concrete Problems in AI Safety*, arXiv:1606.06565 (2016),
`https://arxiv.org/pdf/1606.06565` (PDF, trích chữ bằng pdftotext).
**[SB18]** Sutton & Barto, bản 2 (2018), PDF chính thức `http://incompleteideas.net/book/RLbook2020.pdf` (xem sources_L00.md về cách tải).
**NOT_VERIFIED:** blog OpenAI “Faulty reward functions in the wild” (`https://openai.com/index/faulty-reward-functions/`) trả HTTP 403 —
không dùng bất cứ chi tiết nào chỉ có ở đó (điểm số so với người chơi, ngọn lửa, đầm nước…). Không dùng dịch vụ lách chặn.

| Nguồn | Câu trích nguyên văn | Dùng ở |
|---|---|---|
| [DM20] | “Specification gaming is a behaviour that satisfies the literal specification of an objective without achieving the intended outcome.” | ký hiệu “khai thác phần thưởng” |
| [DM20] | “Consider an agent controlling a boat in the Coast Runners game, where the intended goal was to finish the boat race as quickly as possible. The agent was given a shaping reward for hitting green blocks along the race track, which changed the optimal policy to going in circles and hitting the same green blocks over and over again.” | hook, hình, ví dụ (cơ chế; con số là minh hoạ) |
| [DM20] | “In a Lego stacking task, the desired outcome was for a red block to end up on top of a blue block. The agent was rewarded for the height of the bottom face of the red block when it is not touching the block. Instead of performing the relatively difficult maneuver of picking up the red block and placing it on top of the blue one, the agent simply flipped over the red block to collect the reward.” | hook, lỗi 3 |
| [A16] mục 4 | “From the agent's point of view, this is not a bug, but simply how the environment works, and is thus a valid strategy like any other for achieving reward.” | ký hiệu (hộp “tác tử không gian lận”) |
| [A16] mục 4 | “if our cleaning robot is set up to earn reward for not seeing any messes, it might simply close its eyes rather than ever cleaning anything up.” | khái niệm (nguồn 1), câu đố (a) |
| [A16] mục 4 | “if we base the robot's reward on this measure, it might use more bleach than it needs, or simply pour bleach down the drain in order to give the appearance of success. In the economics literature this is known as Goodhart's law [63]: "when a metric is used as a target, it ceases to be a good metric."” | ký hiệu (định luật), khái niệm (nguồn 2), câu đố (b) |
| [A16] mục 4 | “an ad placement algorithm that displays more popular ads in larger font will tend to further accentuate the popularity of those ads” | khái niệm (nguồn 3) |
| [A16] mục 4 | “For example, a board-game playing agent could tamper with the sensor that counts the score.” | khái niệm (nguồn 4) |
| [A16] mục 4 | “Reward Capping: In some cases, simply capping the maximum possible reward may be an effective solution. However, while capping can prevent extreme low-probability, high-payoff strategies, it can't prevent strategies like the cleaning robot closing its eyes to avoid seeing dirt. Also, the correct capping strategy could be subtle as we might need to cap total reward rather than reward per timestep.” | lỗi 4 |
| [SB18] 3.2 | “For example, a chess-playing agent should be rewarded only for actually winning, not for achieving subgoals such as taking its opponent's pieces or gaining control of the center of the board. If achieving these sorts of subgoals were rewarded, then the agent might find a way to achieve them without achieving the real goal. For example, it might find a way to take the opponent's pieces even at the cost of losing the game.” | lỗi 1 |
| [SB18] 3.2 | “The reward signal is your way of communicating to the agent what you want achieved, not how you want it achieved.” | tư duy ở tổng kết |

## Điều KHÔNG dạy (nguồn không ghi)
- Mọi con số đua thuyền (100 bước, +100, mốc +1 mỗi 5 bước, 1000 bước, các bản vá 0,7 / 0,4) là SỐ MINH HOẠ, tính bằng alg.rln_race /
  alg.rln_boat và verify_parts/L11.py. [DM20] chỉ ghi cơ chế (thưởng định hướng → đi vòng tròn), không ghi điểm, thời gian hay γ.
- Không nói tác tử Coast Runners “được điểm cao hơn người chơi bao nhiêu phần trăm” (chỉ có ở blog OpenAI bị chặn — NOT_VERIFIED).
- Robot dọn dẹp và thuốc tẩy là ví dụ GIẢ ĐỊNH của [A16], bài nói rõ “trong bài báo”, không trình bày như sự cố có thật.
- Không nêu tên người thiết kế phần thưởng nào.
