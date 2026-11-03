# Nguồn bài RLN L07 — gradient chính sách cơ bản (REINFORCE) và đường cơ sở

Đọc 2026-11-02, bản PDF chính thức [SB18] Sutton & Barto, *Reinforcement Learning: An Introduction*, bản 2 (2018),
`http://incompleteideas.net/book/RLbook2020.pdf` (curl qua http từ máy chủ chính thức; https báo chứng chỉ tự ký). Trích bằng pdftotext,
ký tự Hy Lạp và ∇ mất khi trích, ghi lại trong ngoặc vuông.

| Mục | Câu trích nguyên văn | Dùng ở |
|---|---|---|
| 13.3 | “our current interest is the classical REINFORCE algorithm (Willams, 1992) whose update at time t involves just At, the one action actually taken at time t.” | công thức bước 3 (năm 1992) |
| 13.3 | “= E[Gt [∇]π(At\|St, θ) / π(At\|St, θ)], (because E[Gt\|St, At] = qπ(St, At)) … The final expression in brackets is exactly what is needed, a quantity that can be sampled on each time step whose expectation is proportional to the gradient.” | công thức bước 2 (mẹo lôgarit, ước lượng bằng mẫu) |
| 13.3, (13.8) | “θt+1 = θt + [α] Gt [∇]π(At\|St, θt) / π(At\|St, θt). (13.8)” | công thức bước 3 |
| 13.3 | “The update increases the parameter vector in this direction proportional to the return, and inversely proportional to the action probability … otherwise actions that are selected frequently are at an advantage (the updates will be more often in their direction) and might win out even if they do not yield the highest return.” | hình, lỗi 1 |
| 13.3 | “REINFORCE uses the complete return from time t … In this sense REINFORCE is a Monte Carlo algorithm and is well defined only for the episodic case” | nối bài 4 (chờ hết lượt) |
| 13.4 | “The baseline can be any function, even a random variable, as long as it does not vary with a; the equation remains valid because the subtracted quantity is zero” | công thức bước 4, lỗi 2 |
| 13.4 | “In general, the baseline leaves the expected value of the update unchanged, but it can have a large effect on its variance.” ; “for MDPs the baseline should vary with state.” | ví dụ bước 4, quiz câu 2 |

Ghi chú: sách viết ∇π/π; bài viết ∇ ln π — bằng nhau theo đạo hàm của lôgarit (∇ ln x = ∇x / x), sách cũng dùng dạng ln π
(“eligibility vector” ∇ ln π ở mục 13.7).

## Điều KHÔNG dạy (nguồn không ghi / không đọc được)
- Bài báo gốc của R. J. Williams (Machine Learning 8, 1992) không đọc được toàn văn (nhà xuất bản thu phí) — chỉ dẫn qua [SB18];
  NOT_VERIFIED trực tiếp.
- Chính sách hai hành động σ(θ), lợi nhuận 10/12, 4/8, 110/112, α = 0,1 là SỐ MINH HOẠ; mọi kết quả kiểm bằng checks và
  verify_parts/L07.py (sympy, phân số, mô phỏng).
