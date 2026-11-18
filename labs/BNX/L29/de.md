# Lab BNX L29 — Phát lại sự kiện, bản chụp và sự kiện bù

Kho sự kiện của một tài khoản (số minh hoạ), theo thứ tự: `NAP 500`, `RUT 100`, `NAP 200`, `RUT 50`, `NAP 25`, `RUT 75`. Số dư = phát lại từ 0: `NAP` cộng, `RUT` trừ.

Viết `mau.py`:
1. Hàm `phat_lai(kho, tu=0, so_du=0)`: áp dụng các sự kiện từ vị trí `tu` (đếm từ 0) bắt đầu với `so_du`. In `phat lai het: <số dư> (doc <n> su kien)`.
2. Bản chụp sau 4 sự kiện đầu: in `ban chup tai su kien 4 : <số dư>`, rồi phát lại phần còn lại từ bản chụp và in `phat lai tu ban chup: <số dư> (doc <m> su kien)`.
3. Giả sử có thêm một sự kiện `RUT 300` bị GHI NHẦM vào cuối kho (thêm nó: kho thành 7 sự kiện). Không sửa, không xoá nó: thêm sự kiện bù `NAP 300` ở cuối (kho thành 8 sự kiện), phát lại toàn bộ rồi in số dư mới: `sau khi bu su kien rut nham: <số dư>`.

Chạy: `python mau.py`. Chấm: `bash labs/cham.sh BNX L29 mau.py`.
