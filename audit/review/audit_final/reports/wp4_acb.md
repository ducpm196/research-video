# WP4 — nâng khoá ACB (L00–L08) lên chuẩn AF2 — 2026-11-14

Phạm vi: chỉ ACB (không chạm INT/BNX). ACB không có bộ sinh: YAML trong `lessons/acb/` là nguồn, sửa trực tiếp; không chạy build/tts/asr/audit_all/git/docker.

## Tiến độ
- L00–L02 xong (lint, verify, lab, render, khung PNG). L03–L05 xong. L06–L08 xong. Cổng cuối chạy lại sau mọi sửa (xem "Cổng thật").

## Cổng thật (số đo sau lần sửa cuối)
| Cổng | Kết quả |
|---|---|
| `tools/lv.py lint` (9 bài, chạy một tiến trình) | 0 FAIL, 0 WARN (có E51 `covers`, E52 thuật ngữ, E53 lab, E55 chính tả) |
| `audit/acb/verify_acb.py` | 211/211 PASS (có đối chứng âm: đổi một dòng hiện/một dòng mã thì lệch) |
| `tools/lv.py render` (9 bài) | 0 vấn đề mỗi bài (đã tách/ rút ngắn khung tràn: code L02/L03/L04/L05/L07/L08, practice, recap L08) |
| `audit/review/lab_gate.py ACB` | 9 PASS · 0 FAIL (chạy lại qua `labs/cham.sh`) |
| `audit/review/screen_code.py check --course ACB` | PASS 81 · FAIL 0 · STALE 0 · MISSING 0 · ORPHAN 0 · WARN 0 |
| `tools/lv.py curriculum curriculum/acb.yaml` | 9 bài, 0 lỗi |
| `audit/check_curricula_graph.py` | phần ACB: không chu trình, không VER lệch (dòng "VER … WEB:L04 FAIL" là của khoá khác, không phải ACB) |
| `python tests/test_e52.py` | 0 FAIL |
| `audit/review/check_legal.py` (và `--strict`) | 0 FAIL, không dòng nào liên quan ACB |
| `check_xref.py` | không có tham chiếu "như đã học ở khoá…" ở ACB (14 lượt là của BNX) |
| `check_meta.py` | 0 vấn đề (sau khi sửa tên L04 ở `curriculum/acb.yaml` cho khớp chuẩn hoá "khóa"→"khoá") |
| `check_course_refs.py`, `check_next_refs.py` | lần chạy giữa chừng (trước sửa tên L04): course_refs không in dòng ACB nào; next_refs "551 lời hẹn, 0 lệch dãy học". Lần chạy lại sau sửa cuối bị dừng vì chậm — nên chạy lại một lần cho chắc |

Khung PNG đã xem (≥ 3 mỗi bài): L00 khung 44, 49, 58, 89; L01, L05, L06, L08 (lưới 4 khung: code, code cuối, quy mô, practice); L01 frame 90 và L02 frame 63 (trước sửa, lỗi tràn đã khắc phục), L03 frame 47 (trước sửa). L02, L03, L04, L07 được kiểm bằng `render` 0 vấn đề và lưới khung (sheet) tạo cho cả tám bài L01–L08.

## Việc đã làm ở mỗi bài
Mọi bài: `af2: true` + `covers` (8–9 mục tiêu viết lại cho đúng điều video dạy, chép sang `curriculum/acb.yaml`); cảnh `code` (mã Python **mô phỏng** chạy thật, ghi rõ "mô phỏng" trên màn hình và lời đọc); cảnh `quymo` (×1, ×100, ×10 000 cộng một mục "theo thời gian", có "(số minh hoạ)"); cảnh `practice` + lab `labs/ACB/Lxx/{de.md,mong_doi.txt,loi_giai.py}` (số liệu khác ví dụ); thuật ngữ giảng tại chỗ; bỏ lời hứa lương ("tự tin chinh phục 50 triệu gross", "xứng đáng") ở recap; chuẩn hoá "khoá", "tệp" (E55).

| Bài | Mã mô phỏng trên màn hình | Lab (chạy qua cham.sh) | Ghi chú |
|---|---|---|---|
| L00 | tải mỗi phút/giờ, độ trễ toàn trình, P99 | tải 4 000/s, 90+40 ms, TTL, bồi hoàn SAGA | thêm cảnh `vaitro` (hai nhóm vai trò theo JD: nền tảng thanh toán hiện đại / hệ thống kế thừa và nghiệp vụ); viết lại đáp án lương theo dữ kiện đã kiểm |
| L01 | ráp/tách bản tin OFS, ghép trả lời theo mã tương quan (sai thứ tự) | OFS hai dòng, ghép 3 trả lời, Little 90, 91 kết nối | quy mô thêm "hàng đợi ứ theo thời gian" (5 000 đến, 4 000 xử lý → ứ 60 000 sau 60 s) |
| L02 | bản đồ bit (hệ 16), khoá khử trùng lặp có hạn (TTL hết hạn thì bản tin trùng lọt, nên cần ràng buộc duy nhất) | bitmap A/B (trường 128 → bản đồ thứ hai), giải mã, TTL 80 s | HSM không có số thông lượng (không có nguồn): chỉ nói "thêm thiết bị" |
| L03 | hàm chọn kênh (cùng lôgic CASE, kể cả hồ sơ rỗng của LEFT JOIN), hàng đợi ưu tiên (OTP ra trước) | chọn kênh, hàng ưu tiên, xô thẻ, miễn cước | khoá chống trùng 24 giờ ở ×10 000 = 7,2 tỉ khoá → thời gian sống theo loại tin |
| L04 | khoá lạc quan bằng **sqlite thật** (số dòng tác động 1 rồi 0), máy trạng thái | sqlite 3 người mua, lãi mất khi rút sớm, trạng thái | thêm vì sao số phiên bản an toàn hơn dấu thời gian thô |
| L05 | bảng khoá mô phỏng: xin ngược thứ tự → vòng chờ; cùng thứ tự → không vòng; số dư đầu đoạn | kiểm vòng chờ, số dư đầu đoạn, số khối | thêm chỗ nghẽn còn lại: mọi lệnh trừ cùng một tài khoản công ty → trừ một lần tổng |
| L06 | ngưỡng 10/20 triệu có cộng dồn và đặt lại, kiểm vé (HMAC mô phỏng chữ ký, hết hạn, dùng lại) | ngưỡng + vé với số khác | xem mục Pháp lý |
| L07 | HMAC-SHA256 thật (hmac/hashlib), webhook theo mã sự kiện, đối soát hai con trỏ | HMAC, mã sự kiện, đối soát ba nguồn | quy mô N², N·log₂N: 25 giờ so với 0,65 giây ở N = 3 triệu (số minh hoạ 10⁸ phép so/giây) |
| L08 | hạn mức và lãi, quy trình hai pha, giải ngân lũy đẳng bằng sqlite thật (khoá chính) | hạn mức/lãi, hai pha, nhóm nợ CIC, giải ngân | thêm khung vai trò "giữ một mảng nghiệp vụ" (JD); bỏ "như bài 4" (L04 không thuộc dãy tiên quyết của L08) |

Hạ tầng: `audit/acb/verify_acb.py` (kiểm số/mã/đầu ra, ghép nguyên văn khối trên màn hình), `audit/acb/gen_sc_acb.py` (sinh mục sổ `screen_code/ACB.yaml` cho cảnh `code` và đầu ra lab; chạy lại sau khi sửa khối mã), `tools/registry/symbols.ACB.yaml` (22 thuật ngữ `term:` với `introduces`/`assumes`), 9 thư mục `labs/ACB/L00..L08`, `tools/registry/lexicon_vi.ACB.yaml` (+Java, Python, OTP: chép từ JVA/PYT đã qua ASR cùng giọng; NOT_VERIFIED bằng tai người), `curriculum/acb.yaml` (mục tiêu khớp bài, `requires_ext` PYT/FND cho mã Python và sqlite).

## Pháp lý (L06, L08)
- L06: **Quyết định 2345/QĐ-NHNN không có trong sổ** (và mã số không có năm nên `check_legal.py` không bắt). Đã thêm mục `CHUA_KIEM` vào `audit/legal/registry.yaml`. Bài nay: chỉ dùng ngưỡng của Thông tư 50/2024/TT-NHNN (sửa đổi bởi 77/2025/TT-NHNN, bản hợp nhất 25/VBHN-NHNN, đã đọc nguyên văn theo sổ); QĐ 2345 ghi "theo bài phỏng vấn đã lưu: 18/12/2023, hiệu lực 01/07/2024 — chưa đọc nguyên văn, chưa rõ còn áp dụng hay đã được Thông tư thay"; không nêu số điều. Tiêu đề bài vẫn có "Quyết định 2345" (giữ id/tiêu đề; đề xuất đổi tiêu đề sau khi có người đọc nguyên văn). Câu "OTP hoặc hình thức tương đương theo phụ lục QĐ 2345" đã gỡ (chưa kiểm).
- L08: bỏ chỗ dẫn **23/2025/NĐ-CP** (CHUA_KIEM, chưa rõ có đúng chủ đề chữ ký số) và **14/2017/TT-NHNN** (bài dẫn cho "phương pháp tính lãi" nhưng sổ ghi tiêu đề khác — mâu thuẫn; nay bài nói 365 ngày là giả định, theo hợp đồng). Giữ Thông tư 31/2024/TT-NHNN (HIEU_LUC, đã đọc Công báo; nhóm 2 là quá hạn 10–90 ngày). L04: Thông tư 48/2018, 49/2018 chỉ còn ở `source` kèm "chưa kiểm".
- Lương (L00): theo `resources/job/JD.md`, ACB ghi "Thương lượng"; chỉ có lương tháng 13 cố định và thưởng 1–4 tháng là dữ kiện ghi rõ. Bài nay nói 50 triệu gross chỉ là con số người học tự đề xuất; không còn khung thị trường 45–80 triệu (không nguồn chính thức). Không bài nào dẫn tên ngân hàng khác làm nguồn sự thật (khung "hai nhóm vai trò" ghi "nhiều tin tuyển dụng ngân hàng, bản đã lưu, chưa kiểm lại trang gốc").

## P1 dự kiến
Hầu hết thuật ngữ then chốt (SAGA, Redis, Kafka, HSM, MTI/STAN/RRN, MAC, HMAC, lũy đẳng, khử trùng lặp, bế tắc khoá, Outbox, CIC, mTLS, LTV, CDC, hàng đợi thư lỗi, webhook, độ sống, P99, OFS, IBM MQ) có `introduces` ở step giảng hoặc `assumes` từ bài đứng trước trong dãy; lint E52 sạch. Dự kiến P1 = 2 ở ≥ 90% bài; rủi ro còn lại: cú pháp Python trên màn hình được giảng một câu mỗi cấu trúc (người mất gốc hoàn toàn chưa học Python vẫn cần `requires_ext` PYT:L00–L03, L07, L08 như đã ghi).

## Mục không làm / hạn chế
- Không chạy `build/tts/asr`: mọi câu lời đọc mới hoặc đổi cần ASR sau dựng; các mục `asr_reviewed` của câu đã đổi được xoá (E30), câu mới chưa có ghi chú. Từ lạ mới trong lời đọc chỉ có Java, Python, OTP (luật chép từ khoá khác, chưa nghe lại ở ACB); sqlite KHÔNG đọc thành tiếng (FND đo 2/8) — lời đọc nói "cơ sở dữ liệu nhỏ có sẵn trong Python".
- T24, NAPAS, CIC, HSM, Oracle, Kafka, ksqlDB, PostgreSQL, Redis không chạy trên máy: chỉ mô phỏng bằng mã thật nhỏ (ghi rõ trên màn hình); cú pháp OFS và các khối ksql/PL/SQL/Go cũ vẫn `other`/`syntax` với `unverified_claims` trong sổ (không đổi).
- Không chạm `interview/`, `interview_gen_tables.py`, `interview_sync_video.py` (người điều phối chạy sau dựng). `interview/04_banking_domain_t24_napas.md` vẫn nói QĐ 2345 "ban hành 18/12/2023, hiệu lực 01/07/2024" như sự thật: nên rà theo cùng cách.
- Lab L05 mô phỏng bảng khoá bằng từ điển (không dùng luồng thật vì kết quả không xác định); đã chọn đúng cho tính tái lập của chấm tự động.
- `curriculum/acb.yaml` nay lưu LF (công cụ Edit đổi); git `autocrlf` chuẩn hoá khi commit.

## Đề xuất tách bài
- L05 (2 222 từ ≈ 14,8 phút, sát trần 2 300): nếu thêm nội dung nên tách "sao kê chia để trị" (đoạn 7+7+7+9, số dư đầu đoạn, quy mô sao kê) thành bài riêng; không tự tách/đánh số lại.
- L07 và L02 (≈ 2 030 từ) còn dư địa nhỏ; không cần tách.
