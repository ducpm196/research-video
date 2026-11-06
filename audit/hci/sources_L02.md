# Nguồn bài HCI L02 — Định luật Fitts: thời gian trỏ tới một đích

Đọc nguyên văn ngày 2026-11-03. Mọi con số độ khó $\text{ID} = \log_2(D/W + 1)$ và thời gian $T = a + b \cdot \text{ID}$ được kiểm bằng `checks` (`alg.hci_fitts_id`, `alg.hci_fitts_time`) và `audit/verify_plan_curricula.py` (`HCI:L02`).

## [FI54] Paul M. Fitts — *The Information Capacity of the Human Motor System in Controlling the Amplitude of Movement*. Journal of Experimental Psychology, 47(6), 1954, tr. 381–391.
URL: https://www2.psychology.uiowa.edu/faculty/mordkoff/InfoProc/pdfs/Fitts%201954.pdf

| Câu trích nguyên văn | Dùng ở |
|---|---|
| “The index of difficulty of a movement is defined tentatively as $I_d = -\log_2 \frac{W_s}{2A}$ bits/response, where $W_s$ is the tolerance range in inches and $A$ is the average amplitude of the movement.” | `formula`, `pitfalls`: công thức lịch sử năm 1954 gắn độ khó của thao tác trỏ với tỉ số khoảng cách chia bề rộng đích theo cơ số 2 |
| “If the amplitude and tolerance limits of a task are controlled by E, and S is instructed to work at his maximum rate, then the average time per response will be directly proportional to the minimum average amount of information per response demanded by the task conditions.” | `intuition`, `formula`: thời gian di chuyển tăng tuyến tính theo chỉ số độ khó tính bằng bit |

## [MK92] I. Scott MacKenzie — *Fitts’ Law as a Research and Design Tool in Human-Computer Interaction*. Human-Computer Interaction, 7(1), 1992, tr. 91–139.
URL: https://www.yorku.ca/mack/hci1992.pdf

| Câu trích nguyên văn | Dùng ở |
|---|---|
| “A variation of Fitts’ law is proposed as a model for human movement in human-computer interaction (HCI). The variation—actually a direct adaptation of Shannon’s Theorem 17—is $MT = a + b \log_2(A/W + 1)$.” | `sym`, `formula`, `example`: dạng công thức chuẩn trong tương tác người–máy với $+1$ bên trong lôgarit cơ số 2 |
| “The Shannon formulation is preferable because it: (a) provides a slightly better fit with observations, (b) exactly mimics the information theorem underlying Fitts’ law, and (c) always gives a positive rating for the index of difficulty.” | `formula`, `check`: lý do cộng thêm 1 trong $\log_2(D/W + 1)$ để độ khó luôn dương ngay cả khi khoảng cách $D$ rất nhỏ so với bề rộng $W$ |
| “Intercept and slope parameters ($a$ and $b$) vary across devices, tasks, and limbs.” | `pitfalls` (lỗi 1): hằng số $a, b$ phải đo riêng cho từng thiết bị và nhóm người dùng, không lấy hằng số của chuột áp sang màn hình cảm ứng |

## Điều KHÔNG dạy / NOT_VERIFIED
- Bộ số $a = 0{,}1\text{ s}$, $b = 0{,}15\text{ s/bit}$, khoảng cách $D = 256\text{ px}$, bề rộng $W = 16\text{ px}$ và $W = 64\text{ px}$ là SỐ MINH HOẠ đã cố định trong `curriculum/hci.yaml` (`VER HCI:L02`) để học viên nhẩm được $\log_2 17 \approx 4{,}09$ và $\log_2 5 \approx 2{,}32$.
- Các tên riêng `Fitts`, `MacKenzie`, `Shannon` chỉ hiện trên màn hình; lời đọc gọi là “định luật thời gian trỏ”, “dạng công thức chuẩn có cộng một”.
