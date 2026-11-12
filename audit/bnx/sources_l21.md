# Nguồn riêng của BNX L21 (hệ thống cho vay số) — ghi 2026-11-11; người điều phối gộp vào audit/bnx/sources.md

| Mã | Dữ kiện dùng trong bài | Nguồn | Mức |
|---|---|---|---|
| [TT31] | Nhóm nợ theo số ngày quá hạn: nhóm 1 quá hạn dưới 10 ngày; nhóm 2 từ 10 đến 90 ngày; nhóm 3 từ 91 đến 180 ngày; nhóm 4 từ 181 đến 360 ngày; nhóm 5 trên 360 ngày | Thông tư 31/2024/TT-NHNN, Điều 10; Công báo số 825+826 ngày 21-7-2024 | CITED văn bản gốc: người điều phối đối chiếu nguyên văn Công báo số 825+826 ngày 21-7-2024 trong phiên 2026-11-11 (người soạn L21 không tự mở văn bản). Bài chỉ dạy phần định lượng theo số ngày và ghi trên màn hình “văn bản còn các điều kiện khác, đọc nguyên văn thông tư trước khi áp dụng” |
| [L21RUN] | `openssl dgst -sha256 -sign/-verify` in “Verified OK” / “Verification failure”; SHA-256 của chuỗi hợp đồng mẫu bắt đầu `662097aa0554ed46`, bản đổi một ký tự `93938eab15e6cccc`, khác 60/64 vị trí; chữ ký RSA 2048 dài 256 byte | Chạy thật trên máy này 2026-11-11: OpenSSL 3.5.5 (27 Jan 2026, mingw64), Python 3.13 hashlib | OBSERVED (audit/bnx/ver/l21.py chạy lại) |
| [OFSMV] | Dạng trường `FIELD:MV:SV=VALUE` trong bản tin OFS; phần đầu `APPLICATION,VERSION/FUNCTION/PROCESS,USER/PASSWORD/COMPANY,TRANSACTION.ID` | Bài trong kho lessons/acb/L01_tich_hop_core_t24_ibm_mq.yaml (cảnh symbol) | CITED thứ cấp nội bộ; KHÔNG mở được tài liệu Temenos. Bài ghi “mẫu minh hoạ, tên trường giả định”; không khẳng định hành vi nào của T24 ngoài ý “mỗi giá trị kèm vị trí giá trị và vị trí phần con” |

Không có nguồn cho (nên bài KHÔNG dạy): điều khoản cụ thể của Luật Giao dịch điện tử 2023; quy trình thật của dịch vụ ký số từ xa của nhà cung cấp nào; ngưỡng DTI/điểm duyệt/thẻ điểm của tổ chức thật; nghĩa chính xác của tên lớp `OfsDataField` trên CV (bài chỉ dạy khái niệm trường đa trị).

## Bổ sung 2026-11-12 (đợt áp phát hiện đọc độc lập LF2)
| Mã | Dữ kiện dùng trong bài | Nguồn | Mức |
|---|---|---|---|
| [RFC5280] | (L21) Chứng thư số: "public key certificates, which are data structures that bind public key values to subjects." và "The binding is asserted by having a trusted CA digitally sign each certificate." (§3.1). Bài chỉ nói ý này; ví dụ openssl của bài KHÔNG có chứng thư và ghi rõ "chỉ minh hoạ phần toán" | rfc-editor.org/rfc/rfc5280 (đọc 2026-11-12) | CITED |
| [TT31b] | (L21) Đối chiếu lại Điều 10 khoản 1 (phân loại định lượng) với bản tiếng Anh của luatvietnam: nhóm 1 "overdue for less than 10 days and assessed as fully recoverable", nhóm 2 "overdue for up to 90 days", nhóm 3 "91 days to 180 days", nhóm 4 "181 days and 360 days", nhóm 5 "more than 360 days"; ban hành 30-6-2024, hiệu lực 1-7-2024; còn điều kiện cơ cấu lại, miễn giảm lãi, vi phạm, thu hồi sớm | english.luatvietnam.vn (đọc 2026-11-12, thứ cấp; văn bản gốc đã được người điều phối đối chiếu ở [TT31]) | CITED thứ cấp |
