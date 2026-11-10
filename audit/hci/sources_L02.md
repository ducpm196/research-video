# Nguồn bài HCI L02 — Định luật Fitts: thời gian trỏ tới một đích

Ghi ngày 2026-11-03 (đối chiếu bản mở 2026-11-09: các câu trích đã sửa theo bản gốc — xem mục cuối). Mọi con số độ khó $\text{ID} = \log_2(D/W + 1)$ và thời gian $T = a + b \cdot \text{ID}$ được kiểm bằng `checks` (`alg.hci_fitts_id`, `alg.hci_fitts_time`) và `audit/verify_plan_curricula.py` (`HCI:L02`).

## [FI54] Paul M. Fitts — *The Information Capacity of the Human Motor System in Controlling the Amplitude of Movement*. Journal of Experimental Psychology, 47(6), 1954, tr. 381–391.
URL: https://www2.psychology.uiowa.edu/faculty/mordkoff/InfoProc/pdfs/Fitts%201954.pdf

| Câu trích (trạng thái đối chiếu nguồn 2026-11-09) | Dùng ở |
|---|---|
| “If we follow the above reasoning and conventional information notation, a binary index of difficulty ($I_d$) is defined as $I_d = -\log_2 \frac{W_s}{2A}$ bits/response, (1) where $W_s$ is the tolerance range in inches and $A$ is the average amplitude of the particular class of movements.” — **đã sửa theo bản gốc** (mục *Information Analysis*, bản in lại APA Centennial, tr. 266–267): bản gốc **không có** chữ “tentatively” và viết “a binary index of difficulty”, “the particular class of movements” | `formula`, `pitfalls`: công thức lịch sử năm 1954 gắn độ khó của thao tác trỏ với tỉ số khoảng cách chia bề rộng đích theo cơ số 2 |
| “If the amplitude and tolerance limits of a task are controlled by E, and S is instructed to work at his maximum rate, then the average time per response will be directly proportional to the minimum average amount of information per response demanded by the particular conditions of amplitude and tolerance.” — **đã sửa theo bản gốc** (bản in lại tr. 263): đuôi câu là “by the particular conditions of amplitude and tolerance”, không phải “by the task conditions” | `intuition`, `formula`: thời gian di chuyển tăng tuyến tính theo chỉ số độ khó tính bằng bit |

## [MK92] I. Scott MacKenzie — *Fitts’ Law as a Research and Design Tool in Human-Computer Interaction*. Human-Computer Interaction, 7(1), 1992, tr. 91–139.
URL: https://www.yorku.ca/mack/hci1992.pdf

| Câu trích (trạng thái đối chiếu nguồn 2026-11-09) | Dùng ở |
|---|---|
| “The variation of Fitts’ law suggested by direct analogy with Shannon’s information theorem is: $MT = a + b \log_2(A/W + 1)$ (10)” — **đã sửa theo bản gốc tr. 104** (§3.3 *Variations on Fitts’ Law*). Câu cũ “A variation of Fitts’ law is proposed as a model for human movement in HCI. The variation—actually a direct adaptation of Shannon’s Theorem 17—is …” **không có** trong tóm tắt (tr. 91) lẫn §3.3 (tr. 103–106) của [MK92], cũng không có trong trang HTML của MacKenzie 1989 (*J. Motor Behavior*) → coi là diễn giải | `sym`, `formula`, `example`: dạng công thức chuẩn trong tương tác người–máy với $+1$ bên trong lôgarit cơ số 2 |
| “It is noteworthy of Equation 10 that the logarithm cannot be negative.” (tr. 104) và “Thus, the Shannon formulation addresses several theoretical issues and offers slightly better prediction power than Fitts’ or Welford’s formulation.” (tr. 106) — **đã sửa theo bản gốc**. Câu cũ “The Shannon formulation is preferable because it: (a) … (b) … (c) always gives a positive rating for the index of difficulty.” **không tìm thấy** trong §3.3 của [MK92] hay trang MacKenzie 1989 → NOT_VERIFIED nguyên văn (diễn giải) | `formula`, `check`: lý do cộng thêm 1 trong $\log_2(D/W + 1)$ để độ khó luôn dương ngay cả khi khoảng cách $D$ rất nhỏ so với bề rộng $W$ |
| **NOT_VERIFIED nguyên văn (diễn giải)**: câu cũ “Intercept and slope parameters ($a$ and $b$) vary across devices, tasks, and limbs.” không tìm thấy ở các trang đã đọc (tr. 91, 98–106). Câu gốc dùng được, nguyên văn: “The intercept (a) and slope (b) coefficients in Equation 6 are empirically determined constants.” (tr. 98) và trong tóm tắt: “An analysis of the performance measures reveals tremendous inconsistencies, making across-study comparisons difficult.” (tr. 91) | `pitfalls` (lỗi 1): hằng số $a, b$ phải đo riêng cho từng thiết bị và nhóm người dùng, không lấy hằng số của chuột áp sang màn hình cảm ứng |

## Điều KHÔNG dạy / NOT_VERIFIED
- Bộ số $a = 0{,}1\text{ s}$, $b = 0{,}15\text{ s/bit}$, khoảng cách $D = 256\text{ px}$, bề rộng $W = 16\text{ px}$ và $W = 64\text{ px}$ là SỐ MINH HOẠ đã cố định trong `curriculum/hci.yaml` (`VER HCI:L02`) để học viên nhẩm được $\log_2 17 \approx 4{,}09$ và $\log_2 5 \approx 2{,}32$.
- Các tên riêng `Fitts`, `MacKenzie`, `Shannon` chỉ hiện trên màn hình; lời đọc gọi là “định luật thời gian trỏ”, “dạng công thức chuẩn có cộng một”.

## Đối chiếu nguồn mở 2026-11-09 (BN-0040)
- [FI54]: URL cũ www2.psychology.uiowa.edu/…/Fitts%201954.pdf trả **HTTP 404** ngày 2026-11-09. Đã đọc bản in lại toàn văn “APA Centennial Feature” (*J. Exp. Psychol.: General* 121(3), 1992, tr. 262–269; chữ có lớp văn bản): https://www.cs.princeton.edu/courses/archive/fall08/cos436/FittsJEP1954.pdf. Số trang ghi trong bảng là số trang **bản in lại 1992**, không phải tr. 381–391 của bản 1954 (chưa thấy bản quét gốc).
  - Hai câu trích đều đã sửa theo bản gốc (bỏ “tentatively”; sửa đuôi câu giả thuyết).
- [MK92]: https://www.yorku.ca/mack/hci1992.pdf (bản quét 50 trang, không có lớp chữ; đọc bằng ảnh trang tr. 91, 98–106). Đã kiểm thêm https://www.yorku.ca/mack/JMB89.html (MacKenzie 1989).
  - Công thức (10) $MT = a + b\log_2(A/W + 1)$ đúng, tr. 104.
  - Ba câu trích cũ không tìm thấy ở các trang đã đọc → đã thay bằng câu gốc có số trang; câu “Intercept and slope … vary across devices, tasks, and limbs” để NOT_VERIFIED.
- Không phát hiện sai số liệu: công thức Fitts 1954 $I_d = -\log_2(W_s/2A)$ và dạng Shannon $\log_2(A/W+1)$ khớp bản gốc.
