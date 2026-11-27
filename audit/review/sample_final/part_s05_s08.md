# Kiểm mẫu đối chứng cuối `WP-7` — Lô `S05..S08` (hạt giống `20261127`)

- **Phạm vi kiểm:** `24` bài thuộc `S05..S08` (`6` bài/chặng).
- **Tổng bài đã kiểm đủ (YAML + `read_af5` + `lv.py lint` + ≥ 2 frames + `de.md` + chạy thử lab trong thư mục tạm):** **24 / 24**
- **Khớp `sha16` giữa YAML hiện hành và `audit/review/read_af5/<C>/<Lxx>.md`:** **24 / 24**
- **Kiểm `tools/lv.py lint`:** **24 / 24 đạt `0 FAIL`**
- **Kiểm `boiler_deny.txt`:** **24 / 24 có `0` chuỗi trùng**
- **Kiểm lời đọc / thời lượng (không kể `pause`):** **24 / 24 đạt ≥ 1 300 từ (1 809–3 449 từ) và ≥ 9,0 phút (9,74–18,26 phút)** (`OSY/L15` là `case: journey`)
- **Kiểm chạy lab trong thư mục tạm (`mong_doi.txt` + `ca_an/` nếu có):** **24 / 24 PASS** (`18/18` bài có `ca_an/` đều chặn cứng hardcode `mong_doi.txt`; `6` bài S05 miễn `ca_an/` theo `labs/CONTRACT.yaml`).
- **Tổng số lỗi `MUST` thực sự phát hiện:** **0**

---

## Bảng tổng kết 24 bài

| Chặng | Bài | `sha16` (YAML = `read_af5`) | `lv.py lint` | Từ / Phút (không pause) | Khung hình đã xem (`out/<C>/<Lxx>/frames/`) | Lab (chạy trong thư mục tạm) | MUST | SHOULD (đối chiếu `read_af5`) |
|---|---|---|---|---|---|---|---|---|
| S05 | `CS112/L03` | `de6f1962ae22ee28` (khớp) | `0 FAIL, 0 WARN` | 2254 từ / 12.76p | `00029.png`, `00101.png` (rõ, không cắt chữ/chồng hộp) | `PASS` (`python loi_giai.py`, 5/5 dòng `mong_doi.txt`; miễn `ca_an`) | 0 | 1 (`pause=308s` > 300s; `2320` từ tính theo báo cáo cũ / `2254` từ `say` thực tế) |
| S05 | `CS112/L06` | `17574090f5fd4b0c` (khớp) | `0 FAIL, 0 WARN` | 2296 từ / 13.05p | `00028.png`, `00096.png` (bảng/highlight rõ nét) | `PASS` (`python loi_giai.py`, 7/7 dòng `mong_doi.txt`; miễn `ca_an`) | 0 | 1 (`pause=488s` > 300s) |
| S05 | `CS115/L05` | `6ff1fad3665ca9ee` (khớp) | `0 FAIL, 1 WARN` | 2317 từ / 13.79p | `00035.png`, `00121.png` (SVG vector & bảng practice sạch) | `PASS` (`python loi_giai.py`, 8/8 dòng `mong_doi.txt`; miễn `ca_an`) | 0 | 4 (`say` 2317 từ, `pause=360s`, `example.4` dùng `M=[[5,2],[2,2]]` thiếu output trên slide, `covers` obj 5) |
| S05 | `DMS/L02` | `1e6ca4940562a781` (khớp) | `0 FAIL, 0 WARN` | 2279 từ / 12.67p | `00032.png`, `00110.png` (KaTeX & practice rõ nét) | `PASS` (`python loi_giai.py`, 5/5 dòng `mong_doi.txt`; miễn `ca_an`) | 0 | 0 |
| S05 | `DMS/L11` | `bd89346c33d36faf` (khớp) | `0 FAIL, 1 WARN` | 1965 từ / 11.14p | `00027.png`, `00092.png` (SVG sao & vạch rõ, không tràn) | `PASS` (`python loi_giai.py`, 4/4 dòng `mong_doi.txt`; miễn `ca_an`) | 0 | 1 (`pause=390s` > 300s) |
| S05 | `DMS/L14` | `b624139d88f934a1` (khớp) | `0 FAIL, 0 WARN` | 2292 từ / 13.12p | `00031.png`, `00105.png` (KaTeX, pause badge chuẩn) | `PASS` (`python loi_giai.py`, 5/5 dòng `mong_doi.txt`; miễn `ca_an`) | 0 | 1 (`pause=450s` > 300s) |
| S06 | `CPR/L04` | `25337b8f38ff38ac` (khớp) | `0 FAIL, 0 WARN` | 2011 từ / 9.74p | `00022.png`, `00076.png` (SVG con trỏ & gợi ý `scanf` rõ nét) | `PASS` (`gcc` + `du_lieu.txt` 2/2 dòng; `ca_an` `2/2` PASS; chống hardcode OK) | 0 | 3 (bảng `example.0` nhắc `if (q)`/`0x7000`, tiêu đề `quymo` ghi `struct`, `build_report.json` cũ) |
| S06 | `LNX/L03` | `49b44eeffa003cd5` (khớp) | `0 FAIL, 1 WARN` | 2066 từ / 9.77p | `00021.png`, `00073.png` (công thức & gợi ý Bash sạch) | `PASS` (`bash loi_giai.sh` + `du_lieu.txt` 3/3 dòng; `ca_an` `2/2` PASS; chống hardcode OK) | 0 | 1 (`practice.0` `say` nhắc dấu hai chấm trong khi `stdin` ngăn khoảng trắng) |
| S06 | `OSY/L07` | `7702cff135f9a0ca` (khớp) | `0 FAIL, 0 WARN` | 2053 từ / 11.84p | `00027.png`, `00094.png` (mã giả & bảng dữ liệu mẫu rõ) | `PASS` (`python loi_giai.py` + `du_lieu.txt` 3/3 dòng; `ca_an` `2/2` PASS; chống hardcode OK) | 0 | 3 (`00094.png` đặt `;` sau `avail`/`alloc`, `practice.2` `say` sót Bước 3, `du_lieu.txt` trùng `example`) |
| S06 | `OSY/L14` | `efb71204e19dc1de` (khớp) | `0 FAIL, 0 WARN` | 2016 từ / 10.83p | `00025.png`, `00087.png` (KaTeX & bảng 3 bước gợi ý rõ) | `PASS` (`python loi_giai.py` + `du_lieu.txt` 3/3 dòng; `ca_an` `2/2` PASS; chống hardcode OK) | 0 | 3 (`practice` bước 1 thiếu tên khoá cố định, lệch đánh số 2 vs 3 bước ở `practice.2`, `P9=0`) |
| S06 | `OSY/L15` | `50f45c122a77d4c3` (khớp) | `0 FAIL, 0 WARN` | 3449 từ / 18.26p | `00038.png`, `00130.png` (bảng thuật ngữ & quiz lựa chọn sạch) | `PASS` (`python loi_giai.py` + `du_lieu.txt` 3/3 dòng; `ca_an` `3/3` PASS; chống hardcode OK) | 0 | 3 (`du_lieu.txt` trùng số ví dụ, `practice.2` `say` gộp Bước 1–2, `covers` obj 1/3 hẹp) |
| S06 | `PRJ/L05` | `15b4ef4ceda8c6e2` (khớp) | `0 FAIL, 0 WARN` | 2190 từ / 10.30p | `00023.png`, `00078.png` (SVG luồng & bảng `stdin` rõ nét) | `PASS` (`python loi_giai.py` + `du_lieu.txt` 3/3 dòng; `ca_an` `2/2` PASS; chống hardcode OK) | 0 | 1 (`practice.0` `show` ghi `q=4` cố định dù `ca_an` đổi `q=2`, `q=5`) |
| S07 | `SDP/L00` | `8dfbe3f8fb3daed3` (khớp) | `0 FAIL, 10 WARN` | 2139 từ / 11.50p | `00028.png`, `00096.png` (code + bảng đường cơ sở & gợi ý AST rõ) | `PASS` (`python loi_giai.py` + `du_lieu.txt` 3/3 dòng; `ca_an` `2/2` PASS; chống hardcode OK) | 0 | 2 (`example.4` dùng list comprehension, `practice` chưa nêu mẫu `isinstance`/`n.values`) |
| S07 | `SDP/L02` | `186cddb576a3baa3` (khớp) | `0 FAIL, 4 WARN` | 1812 từ / 9.74p | `00023.png`, `00079.png` (khối giải mã & bảng 3 bước sạch) | `PASS` (`python loi_giai.py` + `du_lieu.txt` 3/3 dòng; `ca_an` `2/2` PASS; chống hardcode OK) | 0 | 2 (`practice.1` nói "decorator property" chưa giải thích chữ `decorator`, `du_lieu.txt` trùng `100/150`) |
| S07 | `SDP/L13` | `2468c84b5b825418` (khớp) | `0 FAIL, 4 WARN` | 1866 từ / 10.38p | `00025.png`, `00085.png` (SVG lưới an toàn & bảng gợi ý rõ) | `PASS` (`python loi_giai.py` + `du_lieu.txt` 3/3 dòng; `ca_an` `2/2` PASS; chống hardcode OK) | 0 | 2 (`du_lieu.txt` trùng ví dụ, `practice.0` `show` tóm tắt ngắn) |
| S07 | `SDP/L16` | `adc5908a4bd293fa` (khớp) | `0 FAIL, 2 WARN` | 1809 từ / 10.05p | `00023.png`, `00080.png` (SVG giỏ hàng Strategy & gợi ý sạch) | `PASS` (`python loi_giai.py` + `du_lieu.txt` 3/3 dòng; `ca_an` `2/2` PASS; chống hardcode OK) | 0 | 2 (`du_lieu.txt` trùng `example`/`pitfalls`, `hook.0` `say` 400 vs 500 dòng) |
| S07 | `SEC/L12` | `929408c968d16c6d` (khớp) | `0 FAIL, 3 WARN` | 1917 từ / 10.07p | `00024.png`, `00082.png` (SVG 4 vùng mạng & luật quiz rõ nét) | `PASS` (`python loi_giai.py` + `du_lieu.txt` 3/3 dòng; `ca_an` `2/2` PASS; chống hardcode OK) | 0 | 5 (`pitfalls.1`/`3` thừa câu `say` lệch hộp, `example.1` lệch tên vùng, `covers` obj 2, nhãn khoá `ca_an`, `build_report.json` cũ) |
| S07 | `SWF/L12` | `372d077591d9148e` (khớp) | `0 FAIL, 9 WARN` | 1978 từ / 9.99p | `00022.png`, `00074.png` (code SQLite & bảng 3 bước gợi ý sạch) | `PASS` (`python loi_giai.py` + `du_lieu.txt` 3/3 dòng; `ca_an` `2/2` PASS; chống hardcode OK) | 0 | 4 (`prereq.2` `show: ''`, câu `say` nhảy ý ở `prereq`/`intuition`, `du_lieu.txt` trùng payload mẫu, `recap.1` `say` bỏ qua mục quy mô) |
| S08 | `CLD/L04` | `ad61979c29a42625` (khớp) | `0 FAIL, 1 WARN` | 1972 từ / 10.68p | `00026.png`, `00088.png` (SVG cây 1→3→9→27 & gợi ý sạch) | `PASS` (`python loi_giai.py` + `du_lieu.txt` 2/2 dòng; `ca_an` `2/2` PASS; chống hardcode OK) | 0 | 4 (`pitfalls` 1/3 lệch `say`/`show`, thuật ngữ "nửa mở" chưa định nghĩa ở `sym`, `covers` obj 3, nhãn Mục tiêu `practice`) |
| S08 | `DSY/L08` | `6c513931e12a0118` (khớp) | `0 FAIL, 0 WARN` | 2032 từ / 10.76p | `00025.png`, `00086.png` (bảng nguồn chậm & bảng `stdin` rõ) | `PASS` (`python loi_giai.py` + `du_lieu.txt` 3/3 dòng; `ca_an` `2/2` PASS; chống hardcode OK) | 0 | 2 (`du_lieu.txt` trùng `hook` + nhãn Mục tiêu `practice`, `pitfalls.3` `say` lạc đề khoá rỗng) |
| S08 | `DSY/L14` | `9977eb453d5ad986` (khớp) | `0 FAIL, 1 WARN` | 2017 từ / 10.76p | `00024.png`, `00084.png` (SVG hàng đợi–người nhận & gợi ý rõ) | `PASS` (`python loi_giai.py` + `du_lieu.txt` 3/3 dòng; `ca_an` `2/2` PASS; chống hardcode OK) | 0 | 3 (`pitfalls.1` khung chữ đệm E39, `pitfalls.3`/`quiz.1` thừa câu `say` cuối, `practice.0` nhãn Mục tiêu lệch nội dung lab) |
| S08 | `DVO/L05` | `2b2dbf75c3429861` (khớp) | `0 FAIL, 10 WARN` | 1891 từ / 10.09p | `00025.png`, `00087.png` (SVG khai báo vs mệnh lệnh & bảng `stdin` rõ) | `PASS` (`python loi_giai.py` + `du_lieu.txt` 3/3 dòng; `ca_an` `2/2` PASS; chống hardcode OK) | 0 | 3 (`pitfalls` 6 thẻ vs tiêu đề "3 lỗi" & E39, `example.4` thiếu `focus` & viết `luỹ`, `du_lieu.txt` trùng ví dụ) |
| S08 | `EVT/L06` | `ac301990f6d80d03` (khớp) | `0 FAIL, 1 WARN` | 2007 từ / 10.51p | `00026.png`, `00088.png` (SVG đi tới/lùi lại & `mong_doi` rõ) | `PASS` (`python loi_giai.py` + `du_lieu.txt` 2/2 dòng; `ca_an` `2/2` PASS; chống hardcode OK) | 0 | 4 (`practice` nhãn Mục tiêu ghi obj 3, `saga`/`bước xoay chiều` chỉ có trong `say`, `pitfalls` E39, `recap.1` `say` sót số 50/20) |
| S08 | `SAR/L04` | `81005a7411d535ea` (khớp) | `0 FAIL, 0 WARN` | 2145 từ / 11.35p | `00024.png`, `00084.png` (bảng chiến lược ghi & bảng `stdin` rõ) | `PASS` (`python loi_giai.py` + `du_lieu.txt` 3/3 dòng; `ca_an` `2/2` PASS; chống hardcode OK) | 0 | 3 (`example.1` `say` "gần 20 lần" thiếu mốc so, `covers` obj 2 trỏ `check`, `practice`/`recap` lệch nhỏ `say`/`show`) |

---

## Kiểm chứng độc lập bổ sung

1. **Chạy lại đoạn mã minh hoạ trong YAML tại thư mục tạm (không sửa kho):**
   - Python (`CS112/L03`, `CS112/L06`, `CS115/L05`, `DMS/L02`, `DMS/L11`, `DMS/L14`, `PRJ/L05`, `DVO/L05`), C11 (`CPR/L04` biên dịch bằng `gcc -std=c11 -Wall -Wextra -Werror`), và Bash (`LNX/L03`) đều cho đầu ra khớp 100% giá trị hiển thị trên màn hình YAML.
2. **Kiểm chống rò đáp án trong `de.md` & `practice`:**
   - Kiểm tra 4 bài có dòng trùng ngắn giữa `mong_doi.txt` và `de.md` (`CS115/L05` 1/8 dòng, `DMS/L02` 2/5 dòng, `DMS/L14` 1/5 dòng, `PRJ/L05` 1/3 dòng): đều là chuỗi định dạng đầu ra / nhãn phương án (`"3: dung" hoặc "3: sai"`, `header_valid=1`, `khong co`), không lộ giá trị đáp án.
   - Không có bài nào chiếu nguyên `loi_giai.*` trong `practice`.
3. **Kết luận chốt lô `S05..S08`:**
   - **0 lỗi MUST** trên toàn bộ 24 bài mẫu đối chứng cuối. Mọi phát hiện còn lại đều thuộc mức `SHOULD` và đã được ghi nhận nhất quán trong các báo cáo `audit/review/read_af5/<C>/<Lxx>.md`.
