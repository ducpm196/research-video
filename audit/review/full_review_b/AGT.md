# AGT — đã đọc 13/13 bài

Người đọc: tác tử đợt B, 2026-11-08. Đọc mọi cảnh (`show`, `say`, `checks`, quiz, đáp án) qua bản trích chữ của từng tệp; L12 đối chiếu từng sự kiện, năm và con số với `audit/agt/sources_L12.md`. Bài không sinh từ mẫu (`audit/agt/src/` không tồn tại).

| Bài | Kết luận | Mục đã sửa (cảnh: MUST/SHOULD — lý do ngắn) | Nguồn | lint / render |
|---|---|---|---|---|
| L00 | đã sửa | example bước 5: SHOULD — các con số thử lại (0,951; 0,998) ngầm coi lần thử lại độc lập với lần trước, bài chưa nói → thêm điều kiện; pitfalls lỗi 3: SHOULD — “thanh toán, xoá, gửi đi **là** không thu hồi được” → “thường không thu hồi được”; quiz: MUST (màn hình–lời đọc lệch) — màn hình hỏi “Nên làm cách nào?”, lời đọc không có → thêm vào `say`, sửa `focus` | tính lại; LLM bài 11 (các lần sinh tương quan) | lint: 0 FAIL, 0 WARN, 20 PASS; render: 76 khung (0 vấn đề) |
| L01 | đã sửa | pitfalls lỗi 2: SHOULD — khoá lũy đẳng chỉ chặn lần hai khi máy chủ hỗ trợ khoá đó → thêm điều kiện | Stripe API docs, *Idempotent requests*, docs.stripe.com/api/idempotent_requests (truy cập 2026-11-08, no revision given): khoá do máy khách sinh, máy chủ dùng để nhận ra lần gửi lại; khoá có thể bị xoá sau 24 giờ | lint: 0 FAIL, 0 WARN, 19 PASS; render: 70 khung (0 vấn đề) |
| L02 | không phát hiện lỗi | — (đã tính lại 12/9 giây, đường găng, xếp lịch 2 lời gọi: 13/12, quiz 17/10/9) | — | — |
| L03 | không phát hiện lỗi | — (đã tính lại 60/58 lượt, 45/59, quiz 18/17, lượt 24–40) | — | — |
| L04 | không phát hiện lỗi | — (đã tính lại 0,6/0,8/0,9; 0,82; 0,892; 0,935) | — | — |
| L05 | đã sửa | sym: SHOULD — “kiểm bằng chương trình thường có tỉ lệ nhận nhầm gần 0” thiếu điều kiện → thêm “với điều kiện phép kiểm đủ chặt”; quiz: MUST (màn hình–lời đọc lệch) — thiếu “Nên chọn bộ nào?” trong `say` | Cobbe và cộng sự 2021 (bộ kiểm chứng); tính lại | lint: 0 FAIL, 0 WARN, 22 PASS; render: 78 khung (0 vấn đề) |
| L06 | đã sửa | quiz: MUST (màn hình–lời đọc lệch) — thiếu “Có nên bỏ bớt một tầng?” trong `say` | — | lint: 0 FAIL, 0 WARN, 21 PASS; render: 70 khung (0 vấn đề) |
| L07 | không phát hiện lỗi | — (đã tính lại 0,973/0,343, ước lượng không chệch 0,992, 0,59/0,951) | — | — |
| L08 | đã sửa | sym: SHOULD — bộ nhớ đệm tiền tố bỏ sót các điều kiện quan trọng: độ dài tối thiểu, hạn dùng (mặc định 5 phút), lần ghi đắt hơn giá thường → thêm, nói rõ ví dụ bỏ qua các điều này; `source` thay “tài liệu các nhà cung cấp” chung chung bằng trang cụ thể; quiz: MUST (màn hình–lời đọc lệch) — thiếu “Có đáng giữ phần đầu lời nhắc cố định không?” | Anthropic, *Prompt caching*, platform.claude.com/docs/en/build-with-claude/prompt-caching (truy cập 2026-11-08, no revision given): “Cache hits require 100 percent identical prompt segments”, “By default, the cache has a 5-minute lifetime”, ghi 1,25 lần, đọc 0,1 lần giá vào, độ dài tối thiểu theo mô hình | lint: 0 FAIL, 0 WARN, 21 PASS; render: 72 khung (0 vấn đề) |
| L09 | đã sửa | example bước 1: SHOULD — “đọc trang không làm gì ra ngoài → chạy ngay” bỏ sót kênh rò rỉ: tác tử tự chọn địa chỉ thì chính địa chỉ mang dữ liệu ra ngoài → thêm lưu ý “chỉ đọc địa chỉ đã được phép” (mức khái niệm phòng thủ); quiz: MUST (màn hình–lời đọc lệch) — thiếu “Nên chọn thay đổi nào?” | S. Willison, *The lethal trifecta for AI agents*, simonwillison.net/2025/Jun/16/the-lethal-trifecta/ (16/6/2025, truy cập 2026-11-08): công cụ gửi được yêu cầu HTTP, tải ảnh hay tạo liên kết “can be used to pass stolen information back to an attacker”; OWASP Top 10 for LLM Applications 2025, LLM01 | lint: 0 FAIL, 0 WARN, 18 PASS; render: 70 khung (0 vấn đề) |
| L10 | không phát hiện lỗi | — (đã tính lại 44/30/18/8%, 86%/77%, 8,1 giây, 37%, 83%, 65 vết) | — | — |
| L11 | đã sửa | example bước 5: **MUST** — kết luận “quy trình cố định vừa đúng hơn” mâu thuẫn bảng ngay trên (tác tử có kiểm chứng 0,985 > quy trình 0,922) → so công bằng: gắn cùng bộ kiểm chứng vào quy trình, 0,9996⁴ ≈ 0,998 > 0,985, thêm `checks`; sym: SHOULD — “viết được các bước thì **không** cần tác tử” → “thường không cần” | tính lại; Anthropic, *Building Effective Agents* (2024) | lint: 0 FAIL, 0 WARN, 21 PASS; render: 71 khung (0 vấn đề) |
| L12 | không phát hiện lỗi | — (đối chiếu sources_L12.md: 56%, 5 câu, 7 bước, 71/45/37%, 200 vết, 23%; 6,7 tỉ, 0,29, 40,4/14,8, 97,9%; 90 000 → 2294, trung vị 51, 438 nghìn dòng, 32,8 dòng, 1,96%; 286/2294, 15,0/18,0, 15,7/12,0, $4, $1,21/12 bước, $2,52/21 bước, 93%; 6/2024, 8/2024, 7/2025 65% trên 500 bài) | audit/agt/sources_L12.md | — |

Tổng: 7 bài sửa; 6 mục MUST (1 mâu thuẫn kiến thức ở L11, 5 lệch màn hình–lời đọc ở quiz), 7 mục SHOULD.

Giáo án `curriculum/agt.yaml` sửa cho khớp bài: L01 `example` (bài dùng 4 lời gọi, chỉ 1 hợp lệ — giáo án ghi 3 lời gọi), L09 `example` (“đọc (địa chỉ đã được phép) tự do”), L11 `fix` (thêm “cũng được lợi từ bộ kiểm chứng như tác tử”).

## Không sửa và vì sao
- L03 hook: “ngữ cảnh đầy … phần đầu bị cắt bỏ” — cách ứng dụng xử lý khi tràn khác nhau (cắt đầu hoặc báo lỗi); bài là tình huống minh hoạ của một trợ lý cụ thể, nên giữ nguyên.
- L09 lỗi 1: “không bộ lọc nào chặn được hết” — khẳng định tuyệt đối, nhưng khớp OWASP LLM01:2025 và nguồn [GR23] (“effective mitigations … are currently lacking”), nên giữ.
- L02 lỗi 4: “xếp việc dài nhất lên trước” là heuristic LPT, không luôn tối ưu; trong ví dụ của bài nó cho đúng kết quả tối ưu (12 s, kiểm bằng vét cạn trong `checks`).
- L12 chặng 4: so 286 bài với 45 bài năm 2023 (cùng tập) là đúng; nguồn [SA24] ghi kết quả tốt nhất trước đó là 3,8% (một hệ khác), bài không nói 45 bài là “tốt nhất trước đó” nên không sai.

## Điều cần người điều phối
- `audit/verify_plan_curricula.py` `rec("AGT:L01", …)` vẫn mã hoá ví dụ 3 lời gọi `[True, False, True]`, nhưng giáo án và bài dùng 4 lời gọi (1 hợp lệ). Hiện vẫn PASS. Nên đổi `_calls` thành 4 lời gọi của bài (`(500000,"0123456789")`, `(-200,…)`, `("1000","98765")`, `(1000,"9876543210", ghi_chu)`) với kỳ vọng `[True, False, False, False]`. Tôi không sửa tệp này, theo hướng dẫn.

## Kết quả bộ kiểm
- `audit/agt/verify_agt.py`: TỔNG: 15 PASS · 0 FAIL
- `tools/lv.py curriculum curriculum/agt.yaml`: curriculum: 13 bài, 13 đã có đặc tả, 0 lỗi
- `audit/verify_plan_curricula.py`: TỔNG: 521 PASS · 0 FAIL
- `audit/review/scan_ctrl.py`: không có lượt nào ở `lessons/agt`
