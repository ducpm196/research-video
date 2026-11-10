# BCH — đã đọc 13/13 bài

Đọc kiểm lần ba theo `audit/review/FULL_REVIEW_BRIEF_C.md` (2026-11-09): mọi `show` (cả chữ SVG), `say`, `checks`, quiz, mục giáo án `curriculum/bch.yaml`, `audit/bch/sources_L12.md`. Số trên màn hình/lời đọc tính lại bằng Python (`checklib`: `exact_double_spend`, `nakamoto_catch_up`, `pow_mine`, `median_oracle`…; toạ độ đường cong SVG L06 khớp từng điểm). Khoá không có `audit/bch/src/*.tpl.yaml` → sửa thẳng `lessons/bch/*.yaml`.

Tổng: **1 MUST, 12 SHOULD**; check_xref **16 → 0** lượt.

| Bài | Kết luận | Lỗi nội dung đã sửa (cảnh: MUST/SHOULD — lý do ngắn) | Độc lập (tham chiếu khoá khác đã thay bằng gì) | Nguồn | lint / render |
|---|---|---|---|---|---|
| L00 | đã sửa | sym: SHOULD — “mã băm”, “cơ chế đồng thuận” dùng chưa định nghĩa → thêm định nghĩa lời thường; quiz: SHOULD — “chữ ký số / khoá công khai” chưa định nghĩa → thêm ghi chú | prereq “Ở khoá Hệ phân tán và dữ liệu lớn … mạng có độ trễ” → step mới (clear) giảng lại độ trễ: ví dụ số 2 máy X/Y, gửi lúc 0 và 10 ms, trễ 20/50 và 90/30 ms → X thấy Bình trước, Y thấy Chi trước (check mới) | Wüst & Gervais 2018; Nakamoto 2008 §1–2 | lint: 0 FAIL, 0 WARN, 14 PASS; render 71 khung (0 vấn đề) |
| L01 | đã sửa | — (chỉ mục B) | prereq “Ở khoá An toàn thông tin: hàm băm…” → “Trước hết, ta cần hiểu hàm băm là gì … như một dấu vân tay”, giữ ví dụ SHA-256 thật | FIPS 180-4 | lint: 0 FAIL, 0 WARN, 17 PASS; render 67 khung (0 vấn đề) |
| L02 | đã sửa | — (chỉ mục B) | prereq “ở khoá Phân tích và thiết kế thuật toán” → định nghĩa cây nhị phân tại chỗ (nút, tối đa hai con, lá, gốc) + ví dụ 8 lá: 4 + 2 + 1 = 7 nút, 3 tầng | Merkle 1987; RFC 6962 | lint: 0 FAIL, 0 WARN, 20 PASS; render 66 khung (0 vấn đề) |
| L03 | đã sửa | example: SHOULD — “3120 = 60 · 52” nhảy cóc → “(61 − 1)·(53 − 1)” trên màn hình và lời đọc, check mới | prereq “đã gặp ở khoá Toán rời rạc, phần mã khoá công khai” → “Trước hết, ta cần hiểu phép chia lấy dư, tức chia rồi giữ phần dư” (ví dụ 17 mod 5, 3⁴ mod 7 đã có) | Rivest–Shamir–Adleman 1978 | lint: 0 FAIL, 0 WARN, 19 PASS; render 74 khung (0 vấn đề) |
| L04 | không phát hiện lỗi | — | — | Nakamoto 2008 §2, §9 | — |
| L05 | đã sửa | check: SHOULD — “32 196 / 8 ≈ 4024” (đúng 4024,5; làm tròn nửa lên ra 4025) → hiện 4024,5, check đổi thành `== 4024.5` | prereq “Ở khoá Toán rời rạc, phần xác suất, ta đã gặp quy tắc này” → giảng lại: vì sao trung bình 1/p (E = 1 + (1 − p)E ⇒ E = 1/p), ví dụ đồng xu E = 1 + 0,5E ⇒ E = 2 (check mới); thêm `cdot` vào `assumes` | Back 2002; Nakamoto 2008 §4 | lint: 0 FAIL, 0 WARN, 23 PASS; render 74 khung (0 vấn đề) |
| L06 | đã sửa | prereq: SHOULD — “tụt 1 khối thì gỡ hoà với xác suất q/p” nêu không lý do → dẫn x = q + p·x², thử x = 1/9: 0,1 + 0,9/81 = 1/9 (check Fraction); “con bạc cháy túi” giải nghĩa | — | Nakamoto 2008 §11; Grunspan & Pérez-Marco 2018 (đã chốt: bảng 2008 xấp xỉ, chính xác cao hơn) | lint: 0 FAIL, 0 WARN, 28 PASS; render 94 khung (0 vấn đề) |
| L07 | đã sửa | pitfalls Lỗi 1: SHOULD — “34% cổ phần đủ chặn mọi lần chốt” tuyệt đối → “mà không bỏ phiếu thì chặn việc chốt, cho tới khi bị phạt dần (lỗi 2)” | — | Castro–Liskov 1999 (ngưỡng n − f, đã chốt); consensus-specs altair (inactivity leak) | lint: 0 FAIL, 0 WARN, 22 PASS; render 70 khung (0 vấn đề) |
| L08 | đã sửa | — (chỉ mục B) | prereq “Ở khoá Nền tảng phần mềm đúng đắn, máy trạng thái là một bảng” → định nghĩa tại chỗ, giữ ví dụ công tắc TẮT → BẬT → TẮT | Yellow Paper (G_transaction = 21 000) | lint: 0 FAIL, 0 WARN, 19 PASS; render 71 khung (0 vấn đề) |
| L09 | đã sửa | sym: SHOULD — “khoá chống gọi lồng” chưa định nghĩa → “cờ ‘đang chạy’, lời gọi lồng thấy cờ bật thì bị từ chối”; xoá 1 mục `asr_reviewed` cũ | — | Atzei và cộng sự 2017; tài liệu Solidity (CEI, checked arithmetic ≥ 0.8) | lint: 0 FAIL, 0 WARN, 20 PASS; render 78 khung (0 vấn đề) |
| L10 | đã sửa | — (chỉ mục B) | prereq “Ở khoá Mạng máy tính: thời gian truyền = …” → định nghĩa + lý do (mỗi giây đường truyền chỉ đẩy được một số bit cố định), giữ ví dụ 8·10⁶ / 10⁷ = 0,8 s | Croman và cộng sự 2016 | lint: 0 FAIL, 0 WARN, 19 PASS; render 70 khung (0 vấn đề) |
| L11 | đã sửa | intuition: SHOULD — “ba ô đỏ không chiếm được ô giữa, trung vị vẫn là giá đúng” bỏ sót điều kiện (giá sai lọt giữa, ví dụ 99,5, có thể là trung vị, nhưng vẫn trong khoảng giá đúng) → thêm ghi chú + lời đọc + check `median([99,100,100,101,99.5,99.5,99.5]) == 99.5` | prereq “Ở khoá Khoa học dữ liệu: trung vị …” → “Trước hết, ta cần hiểu trung vị …”, giữ ví dụ 5, 1, 9 và 100/101/10⁶ | Meiklejohn và cộng sự 2013 | lint: 0 FAIL, 0 WARN, 22 PASS; render 67 khung (0 vấn đề) |
| L12 | đã sửa | stage5: **MUST (BN-0038)** — “cổ phần của bên bỏ phiếu ngược đa số bị rút dần” sai so với spec: rò rỉ phạt người xác thực KHÔNG có cờ đúng hạn cho điểm mốc (vắng mặt hoặc theo nhánh khác) → sửa màn hình + lời đọc, thêm “dừng khi phần còn lại đủ hai phần ba”; stage5: SHOULD — phạt 1/4096 là mức từ 7/5/2025 (trước đó 1/32) → ghi rõ thời điểm ở bảng, bước 4, lời đọc, check; prereq: SHOULD — nhắc 0,0002428 như sự thật → “bảng xấp xỉ 2008; chính xác ≈ 0,0005914” (check `exact_double_spend`); stage3: SHOULD — màn hình “khối không báo tín hiệu bị từ chối” bỏ điều kiện mà lời đọc có → “khi đề xuất này có hiệu lực” | — (chỉ nhắc bài trong khoá) | consensus-specs master (phase0 `MIN_EPOCHS_TO_INACTIVITY_PENALTY = 4`, altair `get_inactivity_penalty_deltas`, bellatrix quotient 32, electra 4096), truy cập 2026-11-09, no revision given — thêm mục [CS] vào `audit/bch/sources_L12.md` và `source:`; BIP 91 | lint: 0 FAIL, 0 WARN, 38 PASS; render 148 khung (0 vấn đề) |

Giáo án `curriculum/bch.yaml`: SHOULD — `objectives` của cả 13 mục thiếu mục tiêu thứ ba của bài (L00 còn ghi “blockchain” khác bài) → đồng bộ nguyên văn từ bài; L12 `fix` thêm E25, CS và ghi chú rò rỉ/mức phạt. Tiêu đề 13/13 khớp. Ghi chú đầu tệp (nhắc SEC/DSY/DMS) là chú thích YAML, giữ theo B.1.

## Không sửa và vì sao
- L01/L05 “tính lại mã cả chuỗi chỉ tốn vài mi li giây”: đúng cỡ với chuỗi ngắn hay vài nghìn khối; không đủ căn cứ coi là sai.
- L05 “mạng điều chỉnh k”: chuỗi thật chỉnh ngưỡng mục tiêu mịn hơn từng bit; bài ở mô hình k bit, đã ghi trong chú thích quy ước.
- L06 bước 4 lời đọc làm tròn ít chữ số hơn màn hình (0,205 / 0,198…): làm tròn đúng, không mâu thuẫn.
- L10 “mạng thẻ xử lý hàng nghìn giao dịch mỗi giây”: định tính, không đưa số; giữ.
- L12 “ngày 36 bị loại”, “0,33% mỗi ngày”: nguyên văn [E22p]/[E22]; spec cho withdrawable sau EPOCHS_PER_SLASHINGS_VECTOR ≈ 36,4 ngày và churn cũ 225/65 536 ≈ 0,343 %/ngày — khớp “khoảng”, giữ.
- L12 BIP 91 “ngưỡng hạ còn 80%”: BIP 91 là cơ chế riêng ép tín hiệu cho BIP 9, không hạ ngưỡng 95% của BIP 9 trực tiếp; câu khớp abstract BIP 91 (“activate … with a majority hashpower less than 95%”), chỉ thêm điều kiện hiệu lực.
- `requires_ext` của giáo án giữ nguyên (không hiện, không đọc).

## Dương tính giả của check_xref
- Không có. (L12 câu cuối “bài cuối của khoá Blockchain và sổ cái phân tán” là chính khoá này; check_xref không báo.) Mọi “khoá” còn lại là khoá mật mã / “khoá tiền” / khoá chống gọi lồng / “khoá” trạng thái BIP 9 — đã grep, không sửa.

## Kết quả bộ kiểm cuối
- `audit/bch/verify_bch.py`: `verify_bch: 13/13 PASS`
- `check_xref.py --course BCH`: không còn dòng `BCH:` nào (0 lượt; trước: `BCH: 16 lượt ở 8 tệp`); dòng tổng in ra là `check_xref: 44 lượt tham chiếu sang khoá khác ở 22 tệp` (tổng các khoá khác, không thuộc BCH)
- `lv.py curriculum curriculum/bch.yaml`: `curriculum: 13 bài, 13 đã có đặc tả, 0 lỗi`
- `scan_ctrl.py`: `hits: 8` (đều `\tat` của JVA, không có lượt BCH)
