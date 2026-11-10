# BCH — đã đọc 13/13 bài

Đọc kiểm 2026-11-08: mọi cảnh, mọi `show`/`say`/`checks`, quiz và đáp án của `lessons/bch/L00`…`L12`. Khoá BCH không có mẫu `audit/bch/src/*.tpl.yaml`.
Bản sửa ký tự điều khiển (`\text`) ở L07 được giữ nguyên (chỉ sửa chữ trong HTML, không chạm chuỗi LaTeX; `scan_ctrl.py` 0 lượt ở `lessons/bch/`).
Tổng: 6 bài đã sửa, 7 bài không phát hiện lỗi; 1 mục MUST, 5 mục SHOULD.

| Bài | Kết luận | Mục đã sửa (cảnh: MUST/SHOULD — lý do ngắn) | Nguồn | lint / render |
|---|---|---|---|---|
| L00 | không phát hiện lỗi | — | Wüst & Gervais (CVCBT 2018) | — |
| L01 | không phát hiện lỗi | — | FIPS 180-4; hashlib (verify_bch L01) | — |
| L02 | không phát hiện lỗi | — | RFC 6962 §2.1 (tiền tố 0x00/0x01) | — |
| L03 | đã sửa | sym: SHOULD — “địa chỉ là băm của khoá công khai” nói như mọi kiểu địa chỉ → “(kiểu địa chỉ phổ biến)” | BIP 341/350 (địa chỉ Taproot mang thẳng khoá công khai) | lint: 0 FAIL, 0 WARN, 19 PASS; render: 74 khung (0 vấn đề) |
| L04 | không phát hiện lỗi | — | Nakamoto (2008) §2, §9 | — |
| L05 | không phát hiện lỗi | — | SHA-256 thật + Monte Carlo (verify_bch L05) | — |
| L06 | không phát hiện lỗi | — | Nakamoto (2008) §11; Grunspan & Pérez-Marco (2018); mô phỏng verify_bch L06 | — |
| L07 | đã sửa | pitfalls (lỗi 2, lỗi 4) + recap: SHOULD — “quá một phần ba ngoại tuyến thì hệ đứng lại” chỉ đúng với đồng thuận bỏ phiếu thuần; chuỗi bằng chứng cổ phần lớn vẫn ra khối, chỉ dừng CHỐT và phạt dần bên vắng mặt → sửa thành “việc chốt dừng”, nêu cả hai trường hợp; thêm nguồn Gasper | ethereum.org Proof-of-stake (“inactivity leak … whenever the chain fails to finalize for more than four epochs”, audit/bch/sources_L12.md [E22p]); Buterin và cs., Combining GHOST and Casper (arXiv 2003.03052, 2020) | lint: 0 FAIL, 0 WARN, 22 PASS; render: 70 khung (0 vấn đề) |
| L08 | đã sửa | pitfalls (lỗi 2): SHOULD — “dấu thời gian và mã khối do người tạo khối chọn trong một giới hạn” lỗi thời với chuỗi bằng chứng cổ phần (dấu thời gian cố định theo khe) → “người tạo khối biết trước … và tác động được ở một mức (chọn giờ trong giới hạn, hay bỏ không công bố khối)” | ethereum.org Proof-of-stake (khe 12 giây, [E22p]); Yellow Paper | lint: 0 FAIL, 0 WARN, 19 PASS; render: 71 khung (0 vấn đề) |
| L09 | không phát hiện lỗi | — | tài liệu Solidity (Checks-Effects-Interactions; kiểm tràn mặc định từ 0.8) | — |
| L10 | đã sửa | sym: SHOULD — “gộp giao dịch đưa lên dữ liệu nén và bằng chứng” chỉ đúng với một loại; loại còn lại chờ thời hạn để nộp bằng chứng gian lận → nêu cả hai; xoá mục `asr_reviewed` cũ | V. Buterin, An Incomplete Guide to Rollups (2021) — optimistic và validity rollup | lint: 0 FAIL, 0 WARN, 19 PASS; render: 70 khung (0 vấn đề) |
| L11 | đã sửa | pitfalls (lỗi 3): SHOULD — “chỉ lưu mã băm lên chuỗi” cho dữ liệu cá nhân bỏ sót điều kiện: băm trơn của dữ liệu dễ đoán (số điện thoại) bị dò ngược → băm kèm chuỗi ngẫu nhiên | căn cứ chính: băm tất định của không gian nhỏ (số điện thoại ~10¹⁰ giá trị) bị vét cạn được — nguyên lý cam kết có chuỗi ngẫu nhiên (A. Narayanan và cs. 2016, chương 1, “hiding” cần nonce ngẫu nhiên); tham khảo EDPB, Guidelines 02/2025 on processing of personal data through blockchain technologies (bản lấy ý kiến 14/4–9/6/2025; đã kiểm tên văn bản, chưa kiểm được đoạn nói về băm) | lint: 0 FAIL, 0 WARN, 21 PASS; render: 66 khung (0 vấn đề) |
| L12 | đã sửa | stage5: MUST — giới hạn rút “khoảng 0,33% tổng cổ phần mỗi ngày → 303 ngày” trình bày như quy tắc hiện hành, nhưng đó là cách tính TRƯỚC Pectra; từ 7/5/2025 trần rút là 256 ETH mỗi kỷ nguyên (225 kỷ nguyên/ngày → 57 600 ETH/ngày). Giữ con số của trang chính thức (ghi rõ “cách tính cũ”), thêm ghi chú và lời đọc, `checks`, `stage.scale`, `source` [E25]; thêm câu trích nguyên văn vào `audit/bch/sources_L12.md` [E25] và một phép kiểm vào `audit/bch/verify_bch.py` L12 (chú thích có nguồn) | ethereum.org/en/roadmap/pectra (“activated … at epoch 364032, on 07-May-2025”); ethereum/consensus-specs `specs/electra/beacon-chain.md` (`MAX_PER_EPOCH_ACTIVATION_EXIT_CHURN_LIMIT = 256 ETH`, `MIN_SLASHING_PENALTY_QUOTIENT_ELECTRA = 4096`) — truy cập 2026-11-08, no revision given | lint: 0 FAIL, 0 WARN, 38 PASS; render: 146 khung (0 vấn đề) |

## Không sửa và vì sao
- L02: Bitcoin dùng SHA-256 hai lần và nhân đôi lá cuối khi số lá lẻ — bài đã quy ước cây đơn giản (số lá là lũy thừa của 2), không dạy là quy tắc của Bitcoin.
- L05: độ khó thật là ngưỡng mục tiêu, không đúng “k bit 0” — đơn giản hoá đã ghi trong quy ước.
- L08: phí sau EIP-1559 = phí cơ bản (bị đốt) + tiền boa; bài chỉ nói “giá mỗi đơn vị” với số minh hoạ — không sai, không đủ căn cứ để thêm.
- L10: “mạng thanh toán thẻ xử lý hàng nghìn giao dịch mỗi giây” không dẫn nguồn — mức độ chung, không phải con số cụ thể.
- L12: “người xác thực đặt cọc 32 ETH” — sau Pectra số dư hiệu dụng tối đa 2048 ETH, 32 vẫn là mức tối thiểu; trích đúng [E22p]. Phạt ngày đầu 1/4096, trần 0,5 khớp spec Electra (2048 / 4096 = 0,5).
- L12: câu “cổ phần của bên bỏ phiếu ngược đa số bị rút dần” không có câu trích nguyên văn trong sources_L12 (chỉ có “inactivity leak … more than four epochs”) — đúng ý cơ chế, để nguyên; chưa kiểm được nguyên văn.
- `audit/verify_plan_curricula.py` rec("BCH:L12") không mã hoá con số 0,33% → không cần đổi.

## Kết quả cuối
- `audit/bch/verify_bch.py`: `verify_bch: 13/13 PASS`
- `tools/lv.py curriculum curriculum/bch.yaml`: `curriculum: 13 bài, 13 đã có đặc tả, 0 lỗi` (đã thêm `fix` cho L07 và L12 cho khớp bài)
- `audit/review/scan_ctrl.py`: 0 lượt ở `lessons/bch/`
