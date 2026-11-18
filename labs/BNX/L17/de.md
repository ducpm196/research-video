# Lab BNX L17 — Bảng quyết định 401/403 và chia xoay vòng cho các bản khoẻ

Viết `mau.py` (Python, không cần cài thêm gì). Đây là **mô hình Python** của bảng quyết định và phép chia tải, không chạy Spring. Số liệu là số minh hoạ.

**Phần 1 — bảng quyết định.** Hàm `kiem(ma, duong)` trả về mã trạng thái, theo luật: đường `/chuyen-tien` đòi quyền `chuyen_tien`, mọi đường khác chỉ cần đã xác thực.
`ma` là `None` (không mang mã) hoặc một từ điển `{"chu_ky_dung": bool, "het_han": bool, "quyen": [...]}`. Luật theo thứ tự: không mã → 401; chữ ký sai hoặc đã hết hạn → 401;
đường `/chuyen-tien` mà `quyen` thiếu `chuyen_tien` → 403; còn lại → 200.
Dựng 4 mã: `an` (chữ ký đúng, còn hạn, quyền `["so_du"]`), `binh` (như `an` nhưng quyền `["so_du", "chuyen_tien"]`), `gia` (như `binh` nhưng chữ ký sai), `cu` (như `binh` nhưng đã hết hạn).
Rồi gọi hàm cho 6 ca theo thứ tự: (không mã, `/so-du`), (`gia`, `/so-du`), (`cu`, `/chuyen-tien`), (`an`, `/so-du`), (`an`, `/chuyen-tien`), (`binh`, `/chuyen-tien`), in `ca <i>: <mã trạng thái>`.

**Phần 2 — chia xoay vòng.** Có 4 bản dịch vụ `b1, b2, b3, b4`, trong đó `b2` trượt kiểm sức khoẻ. Chia **250 yêu cầu** xoay vòng chỉ cho các bản khoẻ
(yêu cầu thứ i, đếm từ 0, giao cho bản khoẻ thứ i chia lấy dư cho số bản khoẻ). In một dòng `b1=<n> b3=<n> b4=<n>`.

In đúng 7 dòng như `mong_doi.txt`. Chấm: `bash labs/cham.sh BNX L17 mau.py`.
