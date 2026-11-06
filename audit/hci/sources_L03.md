# Nguồn bài HCI L03 — Định luật Hick–Hyman: thời gian chọn trong n lựa chọn

Đọc nguyên văn ngày 2026-11-03. Công thức $T = b \cdot \log_2(n + 1)$ và entropy có trọng số được kiểm bằng `checks` (`alg.hci_hick_time`, `alg.hci_hick_entropy`) và `audit/verify_plan_curricula.py` (`HCI:L03`).

## [HI52] W. E. Hick — *On the Rate of Gain of Information*. Quarterly Journal of Experimental Psychology, 4(1), 1952, tr. 11–26.

| Câu trích nguyên văn | Dùng ở |
|---|---|
| “Reaction time is approximately proportional to the logarithm of the number of equally probable alternatives, $n$, plus 1 — i.e., to $\log(n + 1)$.” | `sym`, `formula`, `example`: thời gian chọn trong $n$ lựa chọn quen thuộc có xác suất ngang nhau tỉ lệ với $\log_2(n + 1)$ |
| “The ‘+1’ represents the additional alternative of ‘no signal’ (or the uncertainty as to when the signal will occur).” | `formula`: giải thích vì sao trong biểu thức có $+1$ bên cạnh $n$ lựa chọn |

## [HY53] Ray Hyman — *Stimulus Information as a Determinant of Reaction Time*. Journal of Experimental Psychology, 45(3), 1953, tr. 188–196.

| Câu trích nguyên văn | Dùng ở |
|---|---|
| “The amount of information per stimulus presentation was varied in three ways: (a) by varying the number of equally probable alternatives from which it could be chosen; (b) by altering the probability of occurrence of particular choices; and (c) by introducing sequential dependencies between successive choices of alternatives.” | `concept`, `check`: mở rộng từ $n$ lựa chọn đồng확 suất sang trường hợp các mục có tần suất dùng khác nhau (entropy) |
| “Reaction time was found to be a linear function of stimulus information (in bits) after the subjects had practiced sufficiently to learn the statistical structure of the stimulus series.” | `pitfalls` (lỗi 1): định luật lôgarit chỉ đúng khi người dùng đã quen thuộc và biết cấu trúc sắp xếp; người mới phải đọc dò tuần tự từng mục nên thời gian tăng tuyến tính theo $n$ |

## Điều KHÔNG dạy / NOT_VERIFIED
- Bộ số $b = 0{,}2\text{ s}$, menu phẳng 15 mục so với menu hai cấp ($3$ nhóm $\times 5$ mục) là SỐ MINH HOẠ trong `curriculum/hci.yaml` (`VER HCI:L03`).
- Tên riêng `Hick`, `Hyman` chỉ hiện trên màn hình; lời đọc dùng “định luật thời gian chọn”.
