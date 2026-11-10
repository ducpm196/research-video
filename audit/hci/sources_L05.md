# Nguồn bài HCI L05 — Mô hình phím bấm KLM: ước lượng thời gian thao tác trước khi làm

Ghi ngày 2026-11-03 (đối chiếu bản quét gốc 2026-11-09: cả bốn câu trích cũ đã sửa theo bản gốc; B/BB chuyển nguồn sang [KI01] — xem mục cuối). Các hằng số thao tác và tổng thời gian nhiệm vụ được kiểm bằng `checks` (`alg.hci_klm_time`) và `audit/verify_plan_curricula.py` (`HCI:L05`).

## [CMN80] Stuart K. Card, Thomas P. Moran, Allen Newell — *The Keystroke-Level Model for User Performance Time with Interactive Systems*. Communications of the ACM, 23(7), 7/1980, tr. 396–410.
URL: https://dl.acm.org/doi/10.1145/358886.358895 (bản PDF học thuật cũ https://courses.cs.washington.edu/courses/cse440/12au/readings/files/klm.pdf cần đăng nhập UW — 2026-11-09; bản quét mở tr. 396–400: https://iiif.library.cmu.edu/file/Newell_box00072_fld05094_doc0001/Newell_box00072_fld05094_doc0001.pdf)

| Câu trích (trạng thái đối chiếu nguồn 2026-11-09) | Dùng ở |
|---|---|
| “This article proposes a simple model, the Keystroke-Level Model, for predicting one aspect of performance: the time it takes an expert user to perform a given task on a given computer system.” — **đã sửa theo bản gốc tr. 396** (tóm tắt). Câu cũ “The Keystroke-Level Model is a simple numerical model for predicting …” không có trong bài | `hook`, `sym`, `pitfalls`: mô hình ước lượng bằng số thời gian thực hiện một nhiệm vụ của người dùng đã thành thạo |
| “The Keystroke-Level Model asserts that the execution part of a task can be described in terms of four different physical-motor operators: K (keystroking), P (pointing), H (homing), and D (drawing), and one mental operator, M, by the user, plus a response operator, R, by the system. These operators are listed in Figure 1. Execution time is simply the sum of the time for each of the operators. $T_{\text{execute}} = T_K + T_P + T_H + T_D + T_M + T_R$. (1)” — **đã sửa theo bản gốc tr. 398** (§3.1 *Operators*). Câu cũ “The execution time of a unit task is the sum of …” là diễn giải | `sym`, `formula`, `example`: công thức cộng tuyến tính các thao tác cơ sở |
| *Fig. 1. The Operators of the Keystroke Model* (tr. 399), nguyên văn: K “Keystroke or button press. Pressing the SHIFT or CONTROL key counts as a separate K operation. Time varies with the typing skill of the user; the following shows the range of typical values:” Best typist (135 wpm) .08; Good typist (90 wpm) .12; **Average skilled typist (55 wpm) .20**; **Average non-secretary typist (40 wpm) .28**; Typing random letters .50; Typing complex codes .75; Worst typist (unfamiliar with keyboard) 1.20. P “Pointing to a target on a display with a mouse.” 1.10 (“… This operator does *not* include the button press that often follows (.2 sec).”). H “Homing the hand(s) on the keyboard or other device.” .40. D($n_D$, $l_D$) .9$n_D$ + .16$l_D$. M “Mentally preparing for executing physical actions.” 1.35. R($t$) “Response of $t$ sec by the system.” $t$. — **đã sửa theo bản gốc**: bản cũ ghi sai tên bảng (“Table I”), gán 0,20 s cho “average non-secretarial typist” (đúng là 0,28 s; 0,20 s là “average skilled typist (55 wpm)”), và bịa dòng “button press or release with mouse: 0.10 sec” — **Fig. 1 không có toán tử B**; nhấn nút chuột được tính là **K** (tr. 398: “This key press is not part of P; it is represented by a K following the P.”) | `sym`, `formula`, `example`, `check`, `quiz`: bảng trọng số chuẩn $K = 0{,}2\text{ s}$ (người gõ thành thạo mức trung bình 55 wpm), $P = 1{,}1\text{ s}$, $H = 0{,}4\text{ s}$, $M = 1{,}35\text{ s}$ lấy từ [CMN80]; $B = 0{,}1\text{ s}$, $BB = 0{,}2\text{ s}$ lấy từ [KI01] bên dưới, **không** từ [CMN80] |
| “Given: A task (possibly involving several subtasks); the command language of a system; the motor skill parameters of the user; the response time parameters of the system; the method used for the task. Predict: The time an expert user will take to execute the task using the system, providing he uses the method without error.” — **đã sửa theo bản gốc tr. 397** (§2 *The Time Prediction Problem*): bản cũ đổi thứ tự các mục và sửa chữ (“or series of subtasks”, “using the method, provided he …”) | `pitfalls` (lỗi 1): mô hình chỉ tính thao tác thuần thục không mắc lỗi, không đo được thời gian người mới học dùng hoặc thời gian sửa lỗi |

## [KI01] David Kieras — *Using the Keystroke-Level Model to Estimate Execution Times*. University of Michigan, bản tài liệu © 2001 (PDF 6 trang).
URL: https://web.eecs.umich.edu/~kieras/docs/GOMS/KLM.pdf (truy cập 2026-11-09)

| Câu trích nguyên văn (đã đọc 2026-11-09) | Dùng ở |
|---|---|
| “B - Press or release mouse button (.1 sec). This is a highly practiced, very rapid movement. Figure .1 sec for pushing the button down or letting it up.” (tr. 2) — **VERIFIED** | nguồn của $B = 0{,}1\text{ s}$ |
| “BB - Click mouse button (.2 sec). Pushing and releasing the mouse button rapidly, as in a selection click, counts as two B operators, for a total of .2 sec.” (tr. 2) — **VERIFIED** | nguồn của $BB = 0{,}2\text{ s}$ trong ví dụ xoá tệp bằng chuột |
| Bảng K của Kieras (tr. 2): “Expert typist (90 wpm): .12 sec; Average skilled typist (55 wpm): .20 sec; Average nonsecretarial typist (40 wpm): .28 sec; Worst typist (unfamiliar with keyboard): 1.2 sec” và “.28 recommended for most users” — **VERIFIED** | đối chiếu: Kieras khuyên K = 0,28 s cho người dùng điển hình; bài dùng 0,2 s (55 wpm) |

## Điều KHÔNG dạy / NOT_VERIFIED
- Phép so sánh nhiệm vụ xoá tệp bằng chuột ($H + M + P + BB + M + P + BB = 5{,}7\text{ s}$) và bằng phím tắt khi tay đang đặt sẵn trên bàn phím ($M + K + K = 1{,}75\text{ s}$) là SỐ MINH HOẠ ứng dụng bảng hằng số chuẩn của bài báo năm 1980 (`VER HCI:L05`).
- Tên riêng và từ viết tắt `Card`, `Moran`, `Newell`, `KLM`, `CACM` chỉ hiện trên màn hình; lời đọc gọi là “mô hình cộng thao tác phím bấm”.

## Ghi chú đọc kiểm 2026-11-08
- Dòng trích “Table I … average non-secretarial typist: 0.20 sec; button press or release with mouse: 0.10 sec” ở trên **không khớp** các bản
  chép lại bảng K của [CMN80] (truy cập 2026-11-08, no revision given: en.wikipedia.org/wiki/Keystroke-level_model; bản tóm tắt của D. Kieras):
  0,20 s là “average skilled typist (55 wpm)”, còn “average non-secretary typist (40 wpm)” là 0,28 s. Toán tử B = 0,1 s (nhấn hoặc nhả nút
  chuột) xuất hiện trong các hướng dẫn KLM về sau; bản PDF [CMN80] không tải được trong phiên (đường dẫn courses.cs.washington.edu trả trang
  HTML) → **chưa kiểm được nguồn** cho B trong bài báo năm 1980.
- Bài đã sửa: K ghi “người gõ thành thạo mức trung bình”; B ghi “cách tính hay dùng về sau”; lời đọc chỉ gán K, P, H, M cho bài báo năm 1980.

## Đối chiếu nguồn mở 2026-11-09 (BN-0040 + BN-0038)
- URL courses.cs.washington.edu/…/klm.pdf: chuyển sang trang đăng nhập CSE/UW NetID (không phải bản mở).
- [CMN80] — bản quét lưu trữ của Đại học Carnegie Mellon (hồ sơ Allen Newell, hộp 72, thư mục 5094), 5 trang = tạp chí tr. 396–400: https://iiif.library.cmu.edu/file/Newell_box00072_fld05094_doc0001/Newell_box00072_fld05094_doc0001.pdf. Đã đọc tr. 396 (tóm tắt), tr. 397 (§2), tr. 398 (§3.1), tr. 399 (Fig. 1, đọc trên ảnh trang). Chưa thấy tr. 401–410 (trang cuối 410 chưa đối chiếu được).
- **BN-0038 — kết luận:** Fig. 1 của [CMN80] (tr. 399) **không có** toán tử B. Bảng chỉ có K, P, H, D, M, R. Nhấn nút chuột = K (“Keystroke or button press”; tr. 398: “This key press is not part of P; it is represented by a K following the P.”); chú thích dòng P nói lần nhấn nút sau khi trỏ mất “.2 sec”. Dòng K: Average skilled typist (55 wpm) **.20**; Average non-secretary typist (40 wpm) **.28** (chú thích b: tốc độ trung bình của nhóm người không phải thư ký trong thí nghiệm §4.1).
- $B = 0{,}1\text{ s}$ và $BB = 0{,}2\text{ s}$ có trong [KI01] tr. 2 (Kieras 2001). Kieras ghi tài liệu “based on Card, Moran, & Newell (1983), but has several extensions”. Chưa kiểm sách CMN 1983 và John & Kieras 1996 nên không gán B cho hai nguồn đó.
- Số liệu ví dụ trong bài: tổng $H + M + P + BB + M + P + BB = 0{,}4 + 1{,}35 + 1{,}1 + 0{,}2 + 1{,}35 + 1{,}1 + 0{,}2 = 5{,}7\text{ s}$ đúng. Theo cách tính của [CMN80] một cú nhấp = một K = 0,20 s (55 wpm), nên con số vẫn bằng nhau; chỉ cần ghi nguồn của B/BB là [KI01].
