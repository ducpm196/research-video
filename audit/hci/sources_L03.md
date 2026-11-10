# Nguồn bài HCI L03 — Định luật Hick–Hyman: thời gian chọn trong n lựa chọn

Ghi ngày 2026-11-03 (đối chiếu 2026-11-09: **chưa đọc được nguyên văn** [HI52], [HY53] — xem mục cuối). Công thức $T = b \cdot \log_2(n + 1)$ và entropy có trọng số được kiểm bằng `checks` (`alg.hci_hick_time`, `alg.hci_hick_entropy`) và `audit/verify_plan_curricula.py` (`HCI:L03`).

## [HI52] W. E. Hick — *On the Rate of Gain of Information*. Quarterly Journal of Experimental Psychology, 4(1), 1952, tr. 11–26.

| Câu trích (trạng thái đối chiếu nguồn 2026-11-09) | Dùng ở |
|---|---|
| **NOT_VERIFIED nguyên văn (diễn giải; không mở được nguồn)**: “Reaction time is approximately proportional to the logarithm of the number of equally probable alternatives, $n$, plus 1 — i.e., to $\log(n + 1)$.” — chưa đọc được toàn văn [HI52]; tóm tắt chính thức (Crossref) không chứa câu này | `sym`, `formula`, `example`: thời gian chọn trong $n$ lựa chọn quen thuộc có xác suất ngang nhau tỉ lệ với $\log_2(n + 1)$ |
| **NOT_VERIFIED nguyên văn (diễn giải; không mở được nguồn)**: “The ‘+1’ represents the additional alternative of ‘no signal’ (or the uncertainty as to when the signal will occur).” | `formula`: giải thích vì sao trong biểu thức có $+1$ bên cạnh $n$ lựa chọn |
| Câu đọc được, nguyên văn từ tóm tắt [HI52] (metadata Crossref, DOI 10.1080/17470215208416600): “The principal finding is that the rate of gain of information is, on the average, constant with respect to time, within the duration of one perceptual-motor act, and has a value of the order of five ‘bits’ per second.” — **VERIFIED 2026-11-09** (tóm tắt, không có số trang) | có thể thay cho hai dòng trên nếu cần một câu trích đã kiểm |

## [HY53] Ray Hyman — *Stimulus Information as a Determinant of Reaction Time*. Journal of Experimental Psychology, 45(3), 1953, tr. 188–196.

| Câu trích (trạng thái: **NOT_VERIFIED nguyên văn** cả hai dòng — diễn giải; không mở được nguồn 2026-11-09) | Dùng ở |
|---|---|
| “The amount of information per stimulus presentation was varied in three ways: (a) by varying the number of equally probable alternatives from which it could be chosen; (b) by altering the probability of occurrence of particular choices; and (c) by introducing sequential dependencies between successive choices of alternatives.” | `concept`, `check`: mở rộng từ $n$ lựa chọn đồng xác suất sang trường hợp các mục có tần suất dùng khác nhau (entropy) |
| “Reaction time was found to be a linear function of stimulus information (in bits) after the subjects had practiced sufficiently to learn the statistical structure of the stimulus series.” | `pitfalls` (lỗi 1): định luật lôgarit chỉ đúng khi người dùng đã quen thuộc và biết cấu trúc sắp xếp; người mới phải đọc dò tuần tự từng mục nên thời gian tăng tuyến tính theo $n$ |

## Điều KHÔNG dạy / NOT_VERIFIED
- Bộ số $b = 0{,}2\text{ s}$, menu phẳng 15 mục so với menu hai cấp ($3$ nhóm $\times 5$ mục) là SỐ MINH HOẠ trong `curriculum/hci.yaml` (`VER HCI:L03`).
- Tên riêng `Hick`, `Hyman` chỉ hiện trên màn hình; lời đọc dùng “định luật thời gian chọn”.

## Đối chiếu nguồn mở 2026-11-09 (BN-0040)
- [HI52]: không tìm được bản mở đọc được. typeset.io/scispace.com chặn bằng trang “Human Verification”; CiteSeerX (10.1.1.937.1766) trả 429; web.archive.org trả 429; OpenAlex ghi `oa_status: closed`. Chỉ đọc được tóm tắt qua https://api.crossref.org/works/10.1080/17470215208416600 (xác nhận QJEP 4(1), tr. 11–26) — tóm tắt **không** nêu $\log(n+1)$; hai câu trích để NOT_VERIFIED.
- [HY53]: không tìm được bản mở (typeset.io/scispace chặn; OpenAlex `closed`). Crossref https://api.crossref.org/works/10.1037/h0056940 xác nhận JEP 45(3), tr. 188–196 nhưng không có tóm tắt. Hai câu trích để NOT_VERIFIED.
- Không phát hiện mâu thuẫn số liệu (năm, tập, trang khớp Crossref).
