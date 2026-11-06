# Nguồn bài HCI L04 — Trí nhớ làm việc, gom nhóm và tải nhận thức

Đọc nguyên văn ngày 2026-11-03. Phép đếm số ký tự và số nhóm được kiểm bằng `checks` (`alg.hci_chunks`) và `audit/verify_plan_curricula.py` (`HCI:L04`).

## [MI56] George A. Miller — *The Magical Number Seven, Plus or Minus Two: Some Limits on Our Capacity for Processing Information*. Psychological Review, 63(2), 1956, tr. 81–97.
URL: https://labs.la.utexas.edu/gilden/files/2016/04/MagicNumberSeven-Miller1956.pdf

| Câu trích nguyên văn | Dùng ở |
|---|---|
| “The span of immediate memory imposes severe limitations on the amount of information that we are able to receive, process, and remember. By organizing the stimulus input simultaneously into several dimensions and successively into a sequence of chunks, we manage to break (or at least stretch) this informational bottleneck.” | `intuition`, `formula`, `example`: gom các ký tự rời thành từng nhóm có nghĩa (chunk) để giảm số đơn vị mà trí nhớ làm việc phải giữ |
| “The number of bits of information is constant for absolute judgment and the number of chunks of information is constant for immediate memory. The span of immediate memory seems to be almost independent of the number of bits per chunk.” | `sym`, `formula`: giới hạn của trí nhớ ngắn hạn tính theo số nhóm (đơn vị gợi nhớ), không tính theo số chữ số thô |
| “And finally, what about the magical number seven? What about the seven wonders of the world, the seven seas, the seven deadly sins… Perhaps there is something deep and profound behind all these sevens, something just calling out for us to discover it. But I suspect that it is only a pernicious, Pythagorean coincidence.” | `pitfalls` (lỗi 1): con số $7 \pm 2$ là khoảng nhớ trong thí nghiệm tâm lý học, không phải quy tắc bắt buộc “menu trên màn hình chỉ được có tối đa 7 mục” |

## [CO01] Nelson Cowan — *The Magical Number 4 in Short-Term Memory: A Reconsideration of Mental Storage Capacity*. Behavioral and Brain Sciences, 24(1), 2001, tr. 87–114.
URL: https://pubmed.ncbi.nlm.nih.gov/11515286/

| Câu trích nguyên văn | Dùng ở |
|---|---|
| “New evidence and a careful reanalysis of older evidence converge on the conclusion that there is a pure capacity limit of about 4 chunks (plus or minus 1) in young adults when supplementary mechanisms such as rehearsal and long-term memory recoding are prevented.” | `concept`, `example`, `pitfalls`: khi không được nhẩm lại hoặc gom nhóm thêm, trí nhớ làm việc chỉ giữ thuần tuý khoảng $4 \pm 1$ nhóm |

## Điều KHÔNG dạy / NOT_VERIFIED
- Mã xác thực 6 chữ số `482913` tách thành `482 913` (2 nhóm), số thẻ 16 chữ số tách thành 4 nhóm 4 số, và chuỗi 12 ký tự ngẫu nhiên là SỐ MINH HOẠ trong `curriculum/hci.yaml` (`VER HCI:L04`).
- Tên riêng `Miller`, `Cowan` chỉ hiện trên màn hình; lời đọc dùng tiếng Việt tự nhiên.
