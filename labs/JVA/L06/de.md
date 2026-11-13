# Lab JVA L06 — Ba hàm cho máy rút tiền

Trong Git Bash, viết `RutATM` (tệp `RutATM.java`, số liệu là số minh hoạ). Mỗi hàm là `static`, đặt trong lớp `RutATM`:

1. `static long tinhPhiRut(long soTien)`: dưới **2 000 000** thì phí **1 100**, từ 2 000 000 trở lên phí **3 300**.
2. `static long conLai(long soDu, long soTien)`: **gọi `tinhPhiRut`** và trả về `soDu - soTien - phí`.
3. `static void nap(long[] tk, long soTien)`: cộng `soTien` vào ô `tk[0]` (hàm không trả gì).
4. Hàm chính in đúng bốn dòng: `Phi rut 1500000: …`, `Phi rut 2000000: …`, `Con lai: …` (số dư đầu 10 000 000, rút 2 000 000), `Sau nap: …` (mảng `{10000000}`, nạp 500 000).

Chạy: `javac RutATM.java && java RutATM`. Chấm: `bash labs/cham.sh JVA L06 RutATM.java`.
