# Nguồn bài RLN L03 — khám phá và khai thác

Đọc 2026-11-02 từ bản PDF chính thức **[SB18]** Sutton & Barto, bản 2 (2018), `http://incompleteideas.net/book/RLbook2020.pdf`
(cách tải ghi ở sources_L00.md). Ký tự Hy Lạp mất khi trích, ghi lại trong ngoặc vuông.

| Mục | Câu trích nguyên văn | Dùng ở |
|---|---|---|
| 2.1 | “This is the original form of the k-armed bandit problem, so named by analogy to a slot machine, or "one-armed bandit," except that it has k levers instead of one.” | tên bài toán, ký hiệu k |
| 2.1 | “When you select one of these actions, we say that you are exploiting your current knowledge of the values of the actions. If instead you select one of the nongreedy actions, then we say you are exploring” | khai thác / khám phá |
| 2.2 | “A simple alternative is to behave greedily most of the time, but every once in a while, say with small probability [ε], instead select randomly from among all the actions with equal probability, independently of the action-value estimates.” | ε-tham lam: nhánh khám phá chọn đều MỌI tay (kể cả tay tốt nhất) → (1 − ε) + ε/k |
| 2.2 | “This of course implies that the probability of selecting the optimal action converges to greater than 1 − [ε], that is, to near certainty.” | đối chiếu 0,91 > 0,9 |
| 2.4 | “NewEstimate ← OldEstimate + StepSize [Target − OldEstimate]” | trung bình cộng dồn (bước 1/n) |
| 2.5 | (đoạn về bài toán thay đổi theo thời gian, bước cố định α; hình 2.3 ghi “Both methods used a constant step-size parameter, [α] = 0.1.”) | lỗi 4: bước cố định 1/10 |
| 2.7, (2.10) | “At = argmax_a [ Qt(a) + c √( ln t / Nt(a) ) ], where ln t denotes the natural logarithm of t …, Nt(a) denotes the number of times that action a has been selected prior to time t …, and the number c > 0 controls the degree of exploration. If Nt(a) = 0, then a is considered to be a maximizing action.” | công thức điểm, lỗi 3 (N = 0) |
| 2.7 | “The idea of this upper confidence bound (UCB) action selection is that the square-root term is a measure of the uncertainty or variance in the estimate of a's value.” | tên “cận trên tin cậy”; hình cột cộng thêm |
| 2.7 | “UCB often performs well, as shown here, but is more difficult than [ε]-greedy to extend beyond bandits … One difficulty is in dealing with nonstationary problems” | quiz câu 3: đánh đổi khi phần thưởng đổi nhanh |
| 2.10 | “The [ε]-greedy methods choose randomly a small fraction of the time, whereas UCB methods choose deterministically but achieve exploration by subtly favoring at each step the actions that have so far received fewer samples.” | hình hai cách khám phá |

## Điều KHÔNG dạy (nguồn không ghi)
- Trang tin 10 tiêu đề, “để vậy suốt một năm”, các con số 0,5 điểm, 45 / 450, chiến dịch 30 ngày là SỐ MINH HOẠ.
- “Mất mát tăng đều theo thời gian” với ε cố định là phép tính trực tiếp 0,09 · Δ mỗi lượt (giáo án `fix`), không trích từ sách.
