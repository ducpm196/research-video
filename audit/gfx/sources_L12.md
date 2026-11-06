# Nguồn bài GFX L12 — Tình huống chuyên gia: cảnh thế giới mở bị nhấp nháy ở xa — chẩn đoán bộ đệm độ sâu

Đọc và đối chiếu 2026-11-03. Nhãn dùng trong `source` của bài `lessons/gfx/L12_tinh_huong_do_sau.yaml`.

## [RE15] N. Reed, “Depth Precision Visualized”, पोस्ट kỹ thuật / NVIDIA Developer & Reedbeta (2015); kèm [UD12] P. Upchurch, M. Desbrun, “Tightening the Precision of Perspective Rendering”, Journal of Graphics Tools, Vol. 16, No. 1, pp. 40–56 (2012) & [AM18] T. Akenine-Möller và cộng sự, “Real-Time Rendering” (4th ed., 2018), mục 23.7 (Depth Buffering)
- **Công thức bước lượng tử độ sâu ở khoảng cách $z$:**
  Với phép chiếu phối cảnh chuẩn ánh xạ khoảng $[n, f]$ vào $[0, 1]$ bằng $d(z) = \frac{f(z - n)}{z(f - n)}$, đạo hàm theo $z$ là $\frac{\mathrm{d}d}{\mathrm{d}z} = \frac{f \cdot n}{z^2(f - n)}$. Với bộ đệm số nguyên $b$ bit (có $2^b$ mức chia đều trên $[0, 1]$), khoảng cách nhỏ nhất phân biệt được ở độ sâu $z$ là:
  $$\Delta z \approx \frac{z^2(f - n)}{f \cdot n \cdot 2^b}$$
  Khi $f \gg n$, $\frac{f - n}{f} \approx 1$, nên $\Delta z \approx \frac{z^2}{n \cdot 2^b}$: bước lượng tử tăng theo bình phương khoảng cách $z^2$, tỉ lệ nghịch với mặt phẳng gần $n$, và hầu như **không phụ thuộc vào mặt phẳng xa $f$**.
- **Con số chẩn đoán trong bài (kiểm bằng `alg.gfx_depth_step`):**
  - Cấu hình gây lỗi: $b = 24$ bit ($2^{24} = 16\,777\,216$), mặt phẳng gần $n = 0{,}01\text{ m}$ ($1\text{ cm}$), mặt phẳng xa $f = 10\,000\text{ m}$ ($10\text{ km}$). Tại $z = 1000\text{ m}$ ($1\text{ km}$):
    $$\Delta z = \frac{1000^2 \cdot (10\,000 - 0{,}01)}{10\,000 \cdot 0{,}01 \cdot 2^{24}} \approx 5{,}96\text{ m} \approx 6\text{ m}$$
    Hai bề mặt ở cách camera $1\text{ km}$ nếu cách nhau dưới $6\text{ m}$ (như mái nhà, tường, biển quảng cáo gắn trên tường) sẽ rơi vào cùng một mức độ sâu lượng tử hoá và giành điểm ảnh (*z-fighting*), gây nhấp nháy dữ dội khi camera nhúc nhích.
  - Thử thay $f = 100\,000\text{ m}$ hay rút $f = 2000\text{ m}$: với $f = 100\,000\text{ m}$, $\Delta z$ vẫn $\approx 5{,}96\text{ m}$ (tỉ số $\approx 1{,}000$); với $f = 2000\text{ m}$, $\Delta z$ vẫn $\approx 5{,}96\text{ m}$ — sửa mặt phẳng xa không giải quyết được gốc rễ.
  - Cách sửa 1 (không tốn thêm bộ nhớ): đẩy mặt phẳng gần từ $n = 0{,}01\text{ m}$ lên $n = 0{,}5\text{ m}$ (gấp $50$ lần) $\Rightarrow \Delta z$ giảm $50$ lần, từ $\approx 5{,}96\text{ m}$ xuống $\approx 0{,}119\text{ m} \approx 0{,}12\text{ m}$ ($12\text{ cm}$).
  - Cách sửa 2 (chuẩn công nghiệp cho cảnh thế giới mở hiện đại theo [RE15]): dùng bộ đệm độ sâu dấu phẩy động 32 bit kết hợp **đảo chiều độ sâu** (*reversed-Z*, đặt mặt phẳng gần ứng với $d = 1$ và mặt phẳng xa ứng với $d = 0$). Số dấu phẩy động có mật độ giá trị dày đặc quanh số $0$ (do số mũ nhị phân giảm dần khi tiến về $0$), bù trừ đúng vào sự co cụm của hàm $1/z$ ở vùng xa.

## Điều KHÔNG dạy / NOT_VERIFIED
- Không nêu tên cá nhân hay hãng trò chơi cụ thể nào như một sự cố riêng lẻ — bài trình bày dưới dạng tình huống chẩn đoán kỹ thuật chuẩn mực của ngành đồ hoạ thời gian thực.
- Không đi sâu công thức bộ đệm độ sâu lôgarit (*logarithmic depth buffer*, vốn làm hỏng kiểm độ sâu sớm trên phần cứng nếu phải ghi lại độ sâu trong bộ tô mảnh).
