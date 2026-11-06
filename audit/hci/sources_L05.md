# Nguồn bài HCI L05 — Mô hình phím bấm KLM: ước lượng thời gian thao tác trước khi làm

Đọc nguyên văn ngày 2026-11-03. Các hằng số thao tác và tổng thời gian nhiệm vụ được kiểm bằng `checks` (`alg.hci_klm_time`) và `audit/verify_plan_curricula.py` (`HCI:L05`).

## [CMN80] Stuart K. Card, Thomas P. Moran, Allen Newell — *The Keystroke-Level Model for User Performance Time with Interactive Systems*. Communications of the ACM, 23(7), 7/1980, tr. 396–410.
URL: https://dl.acm.org/doi/10.1145/358886.358895 (bản PDF học thuật: https://courses.cs.washington.edu/courses/cse440/12au/readings/files/klm.pdf)

| Câu trích nguyên văn | Dùng ở |
|---|---|
| “The Keystroke-Level Model is a simple numerical model for predicting the time it takes an expert user to perform a given task on a given computer system.” | `hook`, `sym`, `pitfalls`: mô hình ước lượng bằng số thời gian thực hiện một nhiệm vụ của người dùng đã thành thạo |
| “The execution time of a unit task is the sum of the time for the physical operators ($K, P, H, D$), the mental operator ($M$), and the system response operator ($R$): $T_{\text{execute}} = T_K + T_P + T_H + T_D + T_M + T_R$.” | `sym`, `formula`, `example`: công thức cộng tuyến tính các thao tác cơ sở |
| “Table I. The Operators of the Keystroke-Level Model: $K$ Keystroke (average non-secretarial typist: $0.20\text{ sec}$; button press or release with mouse: $0.10\text{ sec}$); $P$ Pointing with mouse to a target on a display ($1.10\text{ sec}$); $H$ Homing hands on keyboard or other device ($0.40\text{ sec}$); $M$ Mentally preparing for executing physical actions ($1.35\text{ sec}$).” | `sym`, `formula`, `example`, `check`, `quiz`: bảng trọng số chuẩn $K = 0{,}2\text{ s}$, $B = 0{,}1\text{ s}$ (một lần nhấn-thả chuột $BB = 0{,}2\text{ s}$), $P = 1{,}1\text{ s}$, $H = 0{,}4\text{ s}$, $M = 1{,}35\text{ s}$ |
| “Given: A task (or series of subtasks); the method used to accomplish the task; the command language of the system; the motor skill parameters of the user; the response time parameters of the system. Predict: The time an expert user will take to execute the task using the method, provided he uses the method without error.” | `pitfalls` (lỗi 1): mô hình chỉ tính thao tác thuần thục không mắc lỗi, không đo được thời gian người mới học dùng hoặc thời gian sửa lỗi |

## Điều KHÔNG dạy / NOT_VERIFIED
- Phép so sánh nhiệm vụ xoá tệp bằng chuột ($H + M + P + BB + M + P + BB = 5{,}7\text{ s}$) và bằng phím tắt khi tay đang đặt sẵn trên bàn phím ($M + K + K = 1{,}75\text{ s}$) là SỐ MINH HOẠ ứng dụng bảng hằng số chuẩn của bài báo năm 1980 (`VER HCI:L05`).
- Tên riêng và từ viết tắt `Card`, `Moran`, `Newell`, `KLM`, `CACM` chỉ hiện trên màn hình; lời đọc gọi là “mô hình cộng thao tác phím bấm”.
