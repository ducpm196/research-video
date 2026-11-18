# Lab PYT L02 — Phí rút, thuế và hàm nhận hàm

Cần: Python 3.11 trở lên. Tạo `phi_thue.py` với ba hàm (số nguyên đồng; số liệu minh hoạ, khác ví dụ trong bài):

1. `phi_rut(tien)`: trả `1100` nếu `tien < 2000000`; ngược lại trả `tien * 5 // 10000`.
2. `vat(phi, ty_le=10)`: trả `phi * ty_le // 100`.
3. `tong_chi(tien, ham_phi)`: tính `phi = ham_phi(tien)`, trả `phi + vat(phi)`.

Rồi in:
- với mỗi `tien` trong `[500000, 3000000, 80000000]` một dòng `tien phi tong` (`phi` = `phi_rut(tien)`, `tong` = `tong_chi(tien, phi_rut)`);
- một dòng: `tong_chi(3000000, lambda t: t // 1000)`.
- **đo** (lab chấm *hình dạng* kết quả, không chấm số giây tuyệt đối vì mỗi máy một khác): với `import time`, viết hai hàm không đối số, một hàm gọi `vat(1100)` một triệu lần trong vòng lặp, một hàm tính `phi * 10 // 100` (`phi = 1100`) một triệu lần trong vòng lặp. Mỗi hàm chạy ba lần, lấy thời gian ngắn nhất (hiệu hai lần đọc `time.perf_counter()` quanh lần chạy; lấy số nhỏ nhất của ba số bằng `min(a, b, c)`, hoặc vòng `for` ba lần cập nhật `nhanh = min(nhanh, lan_nay)`). In dòng cuối `Goi ham cham hon viet thang: CO` nếu thời gian của hàm gọi `vat` lớn hơn, ngược lại `KHONG`.

Chạy: `python phi_thue.py`. Chấm (chạy từ thư mục gốc của bộ khoá, nơi có thư mục `labs`; để tệp của bạn ở đó hoặc ghi đường dẫn tới tệp): `bash labs/cham.sh PYT L02 phi_thue.py`.
