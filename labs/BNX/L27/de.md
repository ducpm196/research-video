# Lab BNX L27 — Đối soát tệp lô: số dòng và mã băm

Tệp lô có dạng: các dòng dữ liệu, rồi **một dòng cuối** `TRAILER|<số dòng dữ liệu>|<sha256 của toàn bộ phần dữ liệu>` (dữ liệu = mọi dòng trước trailer, mỗi dòng kết thúc bằng xuống dòng). Mã băm là sha256 của dữ liệu đã mã hoá UTF-8, ghi dạng hex chữ thường (`hexdigest()` của `hashlib`).

Viết `mau.py` có hàm `kiem(noi_dung)` trả `"THIEU DONG"` khi số dòng dữ liệu khác số ghi ở trailer, trả `"SAI MA BAM"` khi số dòng đủ nhưng sha256 không khớp, ngược lại trả `"OK"`.
Kiểm theo thứ tự: số dòng trước, mã băm sau. Rồi tự dựng 5 dòng dữ liệu `A01|100` … `A05|500` (số minh hoạ) cùng trailer đúng, và in 4 dòng:

1. `lo tot: …` (lô đúng)   2. `lo thieu mot dong: …` (bỏ dòng `A05|500` nhưng giữ trailer cũ)   3. `lo sai mot chu so: …` (đổi `A03|300` thành `A03|301`)   4. `lo co trailer gia: …` (trailer ghi đúng 5 dòng nhưng mã băm toàn số 0)

Chạy: `python mau.py`. Chấm: `bash labs/cham.sh BNX L27 mau.py`.
