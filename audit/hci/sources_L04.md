# Nguồn bài HCI L04 — Trí nhớ làm việc, gom nhóm và tải nhận thức

Ghi ngày 2026-11-03 (đối chiếu bản mở 2026-11-09: câu [CO01] cũ không có trong bài báo — xem mục cuối). Phép đếm số ký tự và số nhóm được kiểm bằng `checks` (`alg.hci_chunks`) và `audit/verify_plan_curricula.py` (`HCI:L04`).

## [MI56] George A. Miller — *The Magical Number Seven, Plus or Minus Two: Some Limits on Our Capacity for Processing Information*. Psychological Review, 63(2), 1956, tr. 81–97.
URL: https://labs.la.utexas.edu/gilden/files/2016/04/MagicNumberSeven-Miller1956.pdf

| Câu trích (trạng thái đối chiếu nguồn 2026-11-09) | Dùng ở |
|---|---|
| “First, the span of absolute judgment and the span of immediate memory impose severe limitations on the amount of information that we are able to receive, process, and remember. By organizing the stimulus input simultaneously into several dimensions and successively into a sequence of chunks, we manage to break (or at least stretch) this informational bottleneck.” — **đã sửa theo bản gốc tr. 95** (mục *Summary*): bản cũ bỏ mất “the span of absolute judgment and”, đổi “impose” thành “imposes” | `intuition`, `formula`, `example`: gom các ký tự rời thành từng nhóm có nghĩa (chunk) để giảm số đơn vị mà trí nhớ làm việc phải giữ |
| “Then I can say that the number of bits of information is constant for absolute judgment and the number of chunks of information is constant for immediate memory. The span of immediate memory seems to be almost independent of the number of bits per chunk, at least over the range that has been examined to date.” — **VERIFIED 2026-11-09** (tr. 92–93; bản cũ cắt bớt đầu/đuôi câu, nay ghi đủ) | `sym`, `formula`: giới hạn của trí nhớ ngắn hạn tính theo số nhóm (đơn vị gợi nhớ), không tính theo số chữ số thô |
| “And finally, what about the magical number seven? What about the seven wonders of the world, the seven seas, the seven deadly sins, … and the seven days of the week? … For the present I propose to withhold judgment. Perhaps there is something deep and profound behind all these sevens, something just calling out for us to discover it. But I suspect that it is only a pernicious, Pythagorean coincidence.” — **VERIFIED 2026-11-09** (tr. 96, đoạn kết); đã thêm dấu “…” đúng chỗ lược và câu “For the present I propose to withhold judgment.” bị bỏ ở bản cũ | `pitfalls` (lỗi 1): con số $7 \pm 2$ là khoảng nhớ trong thí nghiệm tâm lý học, không phải quy tắc bắt buộc “menu trên màn hình chỉ được có tối đa 7 mục” |

## [CO01] Nelson Cowan — *The Magical Number 4 in Short-Term Memory: A Reconsideration of Mental Storage Capacity*. Behavioral and Brain Sciences, 24(1), 2001, tr. 87–114.
URL: https://pubmed.ncbi.nlm.nih.gov/11515286/

| Câu trích (trạng thái đối chiếu nguồn 2026-11-09) | Dùng ở |
|---|---|
| **NOT_VERIFIED nguyên văn (câu bản cũ không có trong bài báo)**: câu cũ “New evidence and a careful reanalysis of older evidence converge on the conclusion that there is a pure capacity limit of about 4 chunks (plus or minus 1) in young adults …” **không có** trong toàn văn [CO01] (không có cụm “careful reanalysis”, “plus or minus 1”). Câu gốc, nguyên văn: “A single, central capacity limit averaging about four chunks is implicated along with other, noncapacity-limited sources.” (tóm tắt, tr. 87) và “The experimental means for groups of adults generally range from about 3 to 5 chunks, whereas individual subject means range more widely from 2 to 6 chunks.” (§3.5 *Empirical summary*, tr. 106–107) — **VERIFIED 2026-11-09** cho hai câu gốc này | `concept`, `example`, `pitfalls`: khi không được nhẩm lại hoặc gom nhóm thêm, trí nhớ làm việc chỉ giữ thuần tuý khoảng $4 \pm 1$ nhóm (“3 đến 5 nhóm” theo §3.5) |

## Điều KHÔNG dạy / NOT_VERIFIED
- Mã xác thực 6 chữ số `482913` tách thành `482 913` (2 nhóm), số thẻ 16 chữ số tách thành 4 nhóm 4 số, và chuỗi 12 ký tự ngẫu nhiên là SỐ MINH HOẠ trong `curriculum/hci.yaml` (`VER HCI:L04`).
- Tên riêng `Miller`, `Cowan` chỉ hiện trên màn hình; lời đọc dùng tiếng Việt tự nhiên.

## Đối chiếu nguồn mở 2026-11-09 (BN-0040)
- [MI56]: https://labs.la.utexas.edu/gilden/files/2016/04/MagicNumberSeven-Miller1956.pdf (bản chép lại của *Classics in the History of Psychology*, psychclassics.yorku.ca, có mốc “[p. N]” theo bản in *Psychological Review* 63, 81–97). Câu 1 đã sửa theo bản gốc (tr. 95); câu 2 và 3 VERIFIED (tr. 92–93, tr. 96), ghi đủ chỗ lược.
- [CO01]: https://memory.psych.missouri.edu/assets/doc/articles/2001/cowan-bbs-2001.pdf (toàn văn kèm bình luận); tóm tắt đối chiếu thêm qua Europe PMC (PMID 11515286; BBS 24(1), 87–114). Câu trích cũ không có trong bài → NOT_VERIFIED; đã ghi hai câu gốc có trang (tr. 87; tr. 106–107).
- **Lưu ý số liệu:** Cowan viết “about four chunks” và “3 to 5 chunks” cho trung bình nhóm (cá nhân 2–6); ký hiệu “$4 \pm 1$” là cách viết gọn của bài, không phải chữ của Cowan.
- Lời ghi URL cũ của [CO01] (pubmed) chỉ cho tóm tắt; pubmed.ncbi.nlm.nih.gov chặn trình tải tự động ngày 2026-11-09.
