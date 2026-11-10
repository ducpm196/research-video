# Đọc mẫu độc lập đợt C — 42 bài (2026-11-09)

**Mục đích**: đo lỗi còn sót sau các đợt rà soát (Mục 9–11 của `interview/HANDOVER_INTERVIEW.md`), không dựa vào kết luận của người đã sửa.

**Cách rút mẫu**: mỗi khoá một bài, `random.Random(20261109).choice(sorted(lessons/<khoá>/L*.yaml))` theo thứ tự tên thư mục (42 khoá → 42 bài), chạy 2026-11-09T00:03:19Z.

**Người đọc**: 4 tác tử AI mới (không thấy báo cáo cũ), chỉ đọc, không sửa; mỗi tác tử 9–11 bài; đọc toàn bộ `show`, `say`, `checks`, quiz, mục giáo án và `audit/<khoá>/sources_*.md`; tự tính lại số bằng Python. Người điều phối kiểm lại từng mục MUST trên tệp thật trước khi sửa (cột "Kiểm lại").

## Kết quả

| Bài | Mức | Phát hiện (tóm tắt) | Kiểm lại | Xử lý |
|---|---|---|---|---|
| ACB L02 | MUST | `curriculum/acb.yaml` ghi “giải mã PIN Block … mã hoá MAC”, trái bài (PIN chỉ được dịch trong HSM; MAC là mã toàn vẹn) | CONFIRMED (bài L02 dòng mục tiêu) | giáo án ACB/INT đồng bộ lại toàn bộ từ bài |
| ACB L02 | SHOULD | sơ đồ đặt “ghi nợ” sau khi gửi NAPAS, trong khi phần tự kiểm nói “hoàn tiền” | CONFIRMED | ô Core Banking: “Giữ tiền trước khi gửi 0200 / Chốt trích nợ khi nhận 0210”, lời đọc bước 4 |
| ACB L02 | SHOULD | thuật ngữ chưa giải thích: bản đồ bit thứ hai, HSM, Redis, IN_DOUBT, EOD, PCI DSS | chưa kiểm | **chưa sửa** |
| AGT L00 | SHOULD | “thử lại tối đa 2 lần” nhưng tính 0,05² (2 lần làm); “1 − 0,642³ ≈ 0,736” (thật 0,7354) | CONFIRMED (tính lại) | “làm tối đa 2 lần (thử lại 1 lần)”; hiện 0,6415³ |
| BNK L09 | SHOULD | mục tiêu hứa câu truy vấn tổng nhóm nhưng không hiện câu | CONFIRMED | hiện `SELECT txn FROM entry GROUP BY txn HAVING SUM(amt) <> 0;` (đúng câu `checklib.bnk_ledger_unbalanced` chạy) + giải thích |
| CLC L06 | SHOULD | “36,5 / 0,00000187 ≈ 19,6” (bấm máy ra 19,52) | CONFIRMED | hiện 1,867 (36,5 / 0,000001867 = 19,55) |
| CSA L14 | MUST | “201 ns nếu không có TLB” — không có TLB là 100 + 100 = 200 ns | CONFIRMED | 200 ns + check `100 + 100 == 200` |
| CVI L01 | SHOULD | `G_y = 0` gọi là “cạnh … hướng ngang”, trong khi cùng cảnh gọi là cạnh dọc; S_x gọi “bộ lọc tìm cạnh ngang” | CONFIRMED | “độ sáng chỉ thay đổi theo chiều ngang, tức cạnh dọc”; S_x “đo thay đổi theo chiều ngang” |
| DAN L03 | MUST | “không ORDER BY thì lũy kế phụ thuộc cách máy đọc” — `SUM(...) OVER ()` cho tổng cả bảng, ổn định | CONFIRMED (sqlite: mọi dòng 100) | sửa màn hình + lời đọc + check sqlite mới |
| DSY L10 | SHOULD | 255/v₂₅₆ và 1/√254 không giải thích | CONFIRMED | giải thích k − 1 và sai số chuẩn 1/√(k − 2) |
| GFX L05 | SHOULD | `sources_L05.md` ghi “câu trích nguyên văn” RTR4 nhưng đọc như diễn giải; tên mục có thể sai | không mở được sách | đổi nhãn cột ở cả 7 tệp `audit/gfx/sources_L0*.md` thành NOT_VERIFIED nguyên văn; ghi chú tên mục |
| HCI L06 | SHOULD | 15,2 / 28,0 lệch làm tròn (chính xác 15,26 / 27,95) | xét: tính từ số đã làm tròn hiện trên màn hình (99,6 − 84,4; 16,9 + 11,1) nên nhất quán | không sửa |
| INT L06 | MUST | QĐ 2345: chỉ nêu “trên 10 triệu”, thiếu ngưỡng tổng ngày vượt 20 triệu, mà đáp án B lại ghi “đúng quy định” | CONFIRMED (ACB L06, Mục 9) | đủ hai ngưỡng ở câu hỏi, phương án B, giải thích, lời đọc |
| INT L06 | MUST | giáo án hứa STAR, Split-Brain, Data Drift, “dưới 3 phút” — bài không có | CONFIRMED | giáo án đồng bộ từ bài |
| INT L06 | SHOULD | sơ đồ đề bài giả định ghi “Core T24” cho ACB | CONFIRMED (JD không nói ACB dùng T24) | “Core banking”; mục tiêu “core banking (T24)” |
| INT L06 | SHOULD | “5-Whys Deep Dive” — 5 Whys là kỹ thuật tìm nguyên nhân gốc | CONFIRMED | ghi rõ khung tự đặt, khác 5 Whys |
| INT L06 | SHOULD | nguyên nhân “thiếu chỉ mục khoá ngoại” không gây bế tắc khi chỉ UPDATE số dư | PLAUSIBLE | bước 2 nay chỉ ra vòng chờ do khoá hai tài khoản ngược thứ tự (khớp bước 3) |
| INT L06 | SHOULD | “60 ngày tiếp theo” lệch “ba mốc 30 ngày” | CONFIRMED | “tới ngày 60 … tới ngày 90” |
| JVA L09 | SHOULD | “kiểu trong ngoặc nhọn là lớp bọc” (String không phải); xoá trong vòng lặp không phải lúc nào cũng ném ngoại lệ; không thấy nội dung `ds` | CONFIRMED | sửa `audit/jva/src/l09.py` → `gen.py L09`; hiện dòng 5–14 |
| MLO L06 | SHOULD | màn hình “thông lượng đổi lấy độ trễ” ngược lời đọc; “vài yêu cầu chờ rất lâu, phần lớn nhanh” sai với ví dụ đến đều | CONFIRMED | “đổi độ trễ lấy thông lượng”; giải thích chờ từ 0 tới 310 ms |
| SAR L13 | MUST | “mỗi cụm chỉ dùng khoảng 33%” — slide nguồn [AN14] là ba phần chia cứng 33% của trung tâm dữ liệu | PLAUSIBLE (nguồn mơ hồ) | ghi đúng điều slide nói; 33% bận là số minh hoạ |
| SEP L04 | SHOULD | “chỉ cần gom 3 bản thông báo”, bỏ yêu cầu riêng của Apache 2.0 | CONFIRMED | thêm giấy phép, NOTICE, đánh dấu tệp sửa |
| TOC L05 | SHOULD | “máy 4 trạng thái” trong khi bảng có 5 | CONFIRMED | “5 trạng thái, 4 tới được” |
| WEB L15 | SHOULD | RFC 2616: “không quá 2 [kết nối]” bỏ “tới mỗi máy chủ” | CONFIRMED | thêm “tới mỗi máy chủ” |

25 bài còn lại không có phát hiện: AIF L07, BCH L04, CAS L02, CLD L11, CS112 L05, CS115 L00, DBS L15, DEN L03, DMS L11, DSC L05, DVO L10, ESY L09, EVT L02, IRS L03, LLM L09, NET L02, OSY L06, PAR L02, PLC L11, RBM L08, RLN L02, ROB L09, SDP L14, SEC L04, SWF L05.

## Tỉ lệ (tính bằng Python, khoảng Wilson 95%)
- Bài có ít nhất một MUST: **5/42 = 11,9%** (5,2–25,0%) → ước tính **34–164** trong 656 bài còn lỗi mức MUST trước đợt sửa này.
- Bài có ít nhất một phát hiện thật (bỏ HCI L06): **16/42 = 38,1%** (25,0–53,2%).
- Lỗi tập trung ở hai khoá phỏng vấn INT/ACB (giáo án chưa từng đồng bộ với bài sau Mục 9) và ở các câu diễn đạt/làm tròn; phép tính trong `checks` đều đúng.

Kết luận: các cổng kiểm máy đều qua nhưng **không đủ** để khẳng định “không còn lỗi”; mẫu cho thấy vẫn còn lỗi nội dung mà máy không bắt được.
