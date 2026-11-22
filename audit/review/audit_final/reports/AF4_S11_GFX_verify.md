# Báo cáo kiểm định độc lập 100% khoá Stage 11 `GFX` (L00–L13) — `WP-AF4-5`

**Kết luận tổng thể: `NO-GO`**

Khoá `GFX` (14 bài `L00..L13`) có nền tảng toán học/đồ hoạ chính xác (19/19 `verify_gfx.py` PASS, 14/14 phép kiểm độc lập khớp, `lv.lint` 0 FAIL / 0 WARN, `spec_sha256` & `tts_sha256` & `SRT` khớp 14/14, `ASR` 0 thiếu audio / 0 chưa xem xét, 14/14 `loi_giai.py` chạy ra khớp từng ký tự `mong_doi.txt`). Tuy nhiên khoá **KHÔNG ĐẠT** chuẩn `BRIEF_R4.md` / `ADDENDUM.md` (`MUST=0; P1=2 ≥ 90%; P8=2 100%`) do lỗi hệ thống nghiêm trọng ở `P1`, `P8`, `P9`, `E51 covers:` và `screen_code/GFX.yaml`.

---

## 1. Bảng tóm tắt chỉ số

| Chỉ số | Kết quả đo độc lập | Ghi chú |
|---|---|---|
| Tổng số bài kiểm | **14 / 14** (`L00..L13`) | Chỉ đọc 100%, không mở `audit/review/audit_final/reports/` |
| Số bài `MUST = 0` | **0 / 14** | 14/14 bài đều vướng lỗi hệ thống ở `practice#1/#2` (lộ `loi_giai.py` + `mong_doi.txt` trước `pause: 30`), `de.md` thiếu định dạng stdout, `covers:` E51 trỏ sai cảnh |
| Số bài `P1 = 2` (chuẩn chặt BRIEF_R4) | **0 / 14** | 14/14 bài đạt `P1 = 0` (mỗi bài có ≥ 3 mục cú pháp/viết tắt/thuật ngữ chưa giảng ở `practice#1/#3`, `de.md` hoặc thân bài) |
| Số bài `P8 = 2` | **0 / 14** | 14/14 đạt `P8 = 1` (lab chạy được nhưng lộ code+đáp án trước `pause`, `de.md` không tự đứng được, 13/14 trùng nguyên số ví dụ) |
| Số bài `P9 = 2` | **0 / 14** | 0/14 bài có mục chuẩn `Hai mức quy mô:` trong `recap`; 7/14 bài có ≥ 2 mức quy mô kèm đánh đổi trong thân bài (`L00, L05, L07, L11, L12, L13` và phần so sánh góc/mức ở `L10` chỉ 1 mức hệ thống) |
| Số bài `spec_sha256` & `tts_sha256` khớp | **14 / 14** | `lv.spec_digest` và `lv.tts_digest` khớp 100% `out/GFX/L*/build_report.json` |
| Số bài `SRT == say` khớp từng câu | **14 / 14** | Khớp từng câu về số lượng và nội dung |
| Số bài `ASR` sạch (`thiếu audio=0`, `chưa xem xét=0`) | **14 / 14** | 14/14 bài đều `thiếu audio: 0, chưa xem xét: 0` |
| Số bài `lab` chạy khớp `mong_doi.txt` | **14 / 14** | `.venv\Scripts\python.exe` chạy `loi_giai.py` khớp từng ký tự `mong_doi.txt` |
| Số bài đạt thời lượng AF2 (≥ 9 phút) | **12 / 14** | `L06` = 7,79 phút (1 330 từ), `L13` = 7,42 phút (1 230 từ) |
| Số lỗi `MUST` (tổng phát hiện) | **3 nhóm hệ thống (ảnh hưởng 14/14 bài)** + **1 lỗi sổ `screen_code`** | Lộ lời giải+đáp án trước `pause` (14 bài), `de.md` thiếu định dạng stdout (14 bài), `E51 covers` trỏ sai cảnh (14 bài); `screen_code/GFX.yaml` ghi sai 14 khối Python thành `kind: other, lang: text` |
| Số lỗi `SHOULD` (tổng phát hiện) | **6 nhóm** | `P9` thiếu `Hai mức quy mô:` ở `recap` (14 bài) và thiếu quy mô ở thân bài (7 bài); trùng số liệu lab–ví dụ (13/14 bài); `L06`/`L13` < 9 phút; SVG `L09` đè chữ; `L04`/`L05`/`L06` `loi_giai.py` hardcode kết quả; `L05`/`L12` nhắc đạo hàm chưa giảng gốc; `sources_L00..L06` còn trích sách `[RTR4]/[FCG5]` ở trạng thái `NOT_VERIFIED nguyên văn` |

---

## 2. Bảng tổng hợp 14 bài (`L00..L13`)

| Bài | sha16 lúc đọc | Phút | P1 | P2 | P3 | P4 | P5 | P6 | P7 | Tổng | Mất gốc | P8 | P9 | MUST | SHOULD | Cần biết trước / Chỗ thiếu chính |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `L00` | `1fc1c70d7cff4189` | 11,25 | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | GẦN | 1 | 1 | 3 | 2 | `f"{:.2f}"`, gán bộ `a, b =`, `1080p`, `fps`, `pixel`, `Hz`, `bash/.sh`; thiếu `Hai mức quy mô:` ở recap; `covers` sai |
| `L01` | `0fc6d54d81f77a82` | 11,05 | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | GẦN | 1 | 0 | 3 | 3 | `lambda` 2 đối số, tuple, toán tử giải nén `*tr(...)`, `bash/.sh`; không có P9; `covers` sai |
| `L02` | `3d252ada547812bb` | 10,05 | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | GẦN | 1 | 0 | 3 | 3 | `lambda` 4 đối số + mặc định `f=1.0`, `round(...)`, `bash/.sh`; không có P9; `covers` sai |
| `L03` | `f801c7060f9289a3` | 10,38 | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | GẦN | 1 | 0 | 3 | 3 | `W=1920`, `round`, list `[...]`, `NDC`, `bash/.sh`; không có P9; `covers` sai |
| `L04` | `7f4c6de3465981e9` | 10,41 | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | GẦN | 1 | 0 | 3 | 4 | `OpenGL`, `int(...>0)`, `:.2f` vs `:.3f`, `bash/.sh`; `loi_giai.py` hardcode cạnh; không có P9; `covers` sai |
| `L05` | `30e6a1b07820c60f` | 10,08 | 0 | 1 | 2 | 2 | 2 | 2 | 1 | 10 | GẦN | 1 | 1 | 3 | 4 | Khái niệm đạo hàm, `#` comment, `:.0f`, `near`, `vs`, `z-fighting`, `bash/.sh`; `loi_giai.py` hardcode `1.0/0.1`; thiếu `Hai mức quy mô:` ở recap |
| `L06` | `e8a865c93a9c870d` | 7,79 | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | GẦN | 1 | 0 | 3 | 4 | `Lambert/Blinn/Phong`, `diffuse/specular/ambient`, `**`, `:.1f/:.4f`, `vs`, `bash/.sh`; < 9 phút; `loi_giai.py` hardcode `0.8` |
| `L07` | `75146e5491d56157` | 12,12 | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | GẦN | 1 | 1 | 3 | 2 | `MB`, `**`, `range(1, 11)`, generator `for k in range(...)`, `bash/.sh`; thiếu `Hai mức quy mô:` ở recap; `covers` sai |
| `L08` | `996ee7cd9aef1137` | 11,19 | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | GẦN | 1 | 0 | 3 | 3 | `sRGB`, `**`, `round`, `:.0f`, `vs`, `~188`, `bash/.sh`; không có P9; `covers` sai |
| `L09` | `313d9fc460a82c7f` | 11,13 | 0 | 2 | 1 | 2 | 2 | 2 | 1 | 10 | GẦN | 1 | 0 | 3 | 4 | `print(...)` thiếu trong `practice#0`, `#` comment, `R=1`, `bash/.sh`; SVG `00014.png` đè chữ; không có P9; `covers` sai |
| `L10` | `0d532b5f90c8948b` | 11,58 | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | GẦN | 1 | 0 | 3 | 3 | `F0=0.04` mặc định, `**5`, `:.2f`, `PBR`, `bash/.sh`; không có P9; `covers` sai |
| `L11` | `fa14dfda0e0b4f45` | 11,14 | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | GẦN | 1 | 1 | 3 | 2 | `:.1f`, `overdraw`, `bash/.sh`; thiếu `Hai mức quy mô:` ở recap; `covers` sai |
| `L12` | `6d80946780533ca3` | 10,85 | 0 | 1 | 2 | 2 | 2 | 2 | 1 | 10 | GẦN | 1 | 1 | 3 | 3 | Đạo hàm $\frac{dz_n}{dz}$, `**2`, dịch bit `1 << 24`, `:.2f`, `z-fighting`, `near`, `bash/.sh`; thiếu `Hai mức quy mô:` ở recap; `covers` sai |
| `L13` | `2005a06c2c228165` | 7,42 | 0 | 2 | 2 | 2 | 2 | 2 | 1 | 11 | GẦN | 1 | 1 | 3 | 3 | `UE4`, `60 fps`, `**`, `:.1f`, `Monte Carlo`, `bash/.sh`; < 9 phút; thiếu `Hai mức quy mô:` ở recap; `covers` sai |

*(Lưu ý: cả 14 bài đều có thêm lỗi `MUST` ở sổ `audit/review/screen_code/GFX.yaml` ghi sai `practice 1 0` thành `kind: other, lang: text`.)*

---

## 3. Chi tiết từng hạng mục kiểm định

### 3.1. `curriculum/gfx.yaml` vs `lessons/gfx/L*.yaml` và `covers:` (E51)
- **Title & Objectives:** Khớp **14/14** giữa `curriculum/gfx.yaml` và `lessons/gfx/L*.yaml` (sau khi bỏ tiền tố `"Bài N — "` ở title của bài). Mọi mục tiêu trong giáo án đều có nội dung tương ứng xuất hiện trong video (không hứa điều bài không dạy hoàn toàn).
- **Lỗi `covers:` E51 bị rập khuôn (14/14 bài):**
  - Toàn bộ `L00..L05` gán máy móc `1: example, 2: check, 3: practice`; `L06..L12` gán `1: example, 2: check, 3: check, 4: practice`; `L13` gán `1: stage1, 2: stage2, 3: practice`.
  - Bằng chứng sai cảnh dạy thực tế trên từng bài:
    - `L00` (`lessons/gfx/L00_duong_ong_ket_xuat.yaml:416-422`): Mục tiêu 1 ("Kể đúng thứ tự năm tầng...") trỏ `example` (chỉ tính `1920*1080*60`, không dạy 5 tầng — 5 tầng nằm ở `intuition`); Mục tiêu 3 ("Giải thích vì sao một khung hình trễ làm người xem thấy giật...") trỏ `practice` (không nhắc khung trễ — nằm ở `pitfalls#0`).
    - `L01` (`L01_bien_doi.yaml:389-395`): Mục tiêu 3 ("Giải thích vì sao vector pháp tuyến phải biến đổi bằng ma trận nghịch đảo chuyển vị...") trỏ `practice` (chỉ làm `T*R` vs `R*T`, pháp tuyến nằm ở `pitfalls#0-#1`).
    - `L02` (`L02_chieu_phoi_canh.yaml:367-373`): Mục tiêu 2 ("...đường song song hội tụ, và cách ma trận 4×4 gửi z vào w") trỏ `check` (chỉ kiểm `z=3`, hội tụ nằm ở `formula#0`); Mục tiêu 3 ("Tính nội suy... theo 1/z") trỏ `practice` (chỉ chiếu `(2,1,4)` và `(2,1,8)`, không nội suy — nằm ở `example#2`).
    - `L03` (`L03_cat_khung_nhin.yaml:393-399`): Mục tiêu 3 ("Tính giao điểm cắt... bằng tham số nội suy t") trỏ `practice` (chỉ đổi NDC→pixel, cắt nằm ở `example#2` và `quiz#2`).
    - `L04` (`L04_raster_hoa.yaml:383-389`): Mục tiêu 3 ("Giải thích vì sao điểm ảnh trên cạnh chung... cần quy tắc cạnh trên–trái") trỏ `practice` (không có quy tắc trên–trái — nằm ở `intuition` và `pitfalls#0`).
    - `L05` (`L05_bo_dem_do_sau.yaml:362-368`): Mục tiêu 2 (vì sao bit dồn sát mặt gần) trỏ `check`; Mục tiêu 3 (đẩy gần hiệu quả hơn kéo xa) trỏ `practice` (không tính mặt xa — nằm ở `example#2`).
    - `L06` (`L06_chieu_sang.yaml:342-350`): Mục tiêu 4 (quên chuẩn hoá pháp tuyến sau nội suy) trỏ `practice` (hardcode `n_dot_l=0.8`, không nhắc chuẩn hoá — nằm ở `pitfalls#0`).
    - `L07` (`L07_ket_cau.yaml:382-390`): Mục tiêu 3 (vì sao thu nhỏ không lọc gây sọc lấp lánh) trỏ `check`; Mục tiêu 4 (chọn chế độ lọc) trỏ `practice` (không chọn bộ lọc — nằm ở `quiz#2`).
    - `L08` (`L08_gamma.yaml:408-416`): Mục tiêu 3 (vì sao 128 chỉ còn 21,6% sáng) trỏ `check` (không tính 128 — nằm ở `example#0`); Mục tiêu 4 (xác định loại kết cấu nào cần giải mã) trỏ `practice` (không phân loại kết cấu — nằm ở `pitfalls#2` và `quiz#2`).
    - `L09` (`L09_do_tia.yaml:363-371`): Mục tiêu 4 (chẩn đoán tự che bóng lốm đốm và dịch gốc tia) trỏ `practice` (chỉ giải $t^2-10t+24=0$, không nhắc dịch gốc — nằm ở `pitfalls#0`).
    - `L10` (`L10_ket_xuat_vat_ly.yaml:375-383`): Mục tiêu 3 (điện môi vs kim loại) trỏ `check`; Mục tiêu 4 (độ nhám vi bề mặt) trỏ `practice` (không nhắc độ nhám — nằm ở `formula#2` và `quiz#2`).
    - `L11` (`L11_hieu_nang.yaml:359-367`): Mục tiêu 4 (ngoại lệ vật bán trong suốt / mất Early-Z) trỏ `practice` (không nhắc ngoại lệ — nằm ở `pitfalls#1-#2`).
    - `L12` (`L12_tinh_huong_do_sau.yaml:372-380`): Mục tiêu 2 (thay đổi mặt cắt xa không ảnh hưởng ở 1000 m) trỏ `check` (nằm ở `example#1`); Mục tiêu 3 (so sánh 3 phương án) trỏ `check` (nằm ở `pitfalls#2`); Mục tiêu 4 (ra quyết định thiết kế) trỏ `practice` (nằm ở `pitfalls#2` và `quiz#2`).
    - `L13` (`L13_hanh_trinh_chieu_sang.yaml:371-377`): Mục tiêu 1 (kể 4 chặng) chỉ trỏ `stage1` (bỏ `stage2..4`); Mục tiêu 2 (tính 4 con số 0,194 / 100 / 0,04 / 0,25) chỉ trỏ `stage2` (cả 4 số nằm ở `check`); Mục tiêu 3 (chọn mô hình theo ngân sách) trỏ `practice` (nằm ở `quiz`).

### 3.2. Độ chính xác toán học/đồ hoạ, phép kiểm độc lập & `sources_L*.md`
- `audit/gfx/verify_gfx.py`: Chạy trực tiếp bằng `.venv\Scripts\python.exe -B audit/gfx/verify_gfx.py` → **19/19 PASS** (`exit 0`).
- **Tự chạy Python kiểm lại độc lập (không gọi `alg.gfx_*`, dùng `Fraction`, `sympy`, `numpy`):** Toàn bộ số học, ma trận, chiếu phối cảnh, nội suy `1/z`, cắt thuần nhất, trọng tâm tam giác, độ sâu 24-bit & 16-bit, Lambert/Blinn–Phong, song tuyến/mipmap, sRGB IEC 61966-2-1, giao tia–cầu, Schlick Fresnel, tô đè và các phép kiểm trong `checks:` + `example` + `check` + `pitfalls` + `quiz` của cả **14/14 bài** đều **ĐÚNG 100%**.
- `audit/gfx/sources_L13.md` vs `L13`: Khớp chính xác cả 7 nguồn `[PH75]`, `[BL77]`, `[WH80]`, `[KA86]`, `[SC94]`, `[BU12]`, `[KA13]` và các số liệu (`0,95³² ≈ 0,194`, `10² = 100`, `n=1,5 → F₀=0,04`, `cos=0,5 → F=0,07`, `1−F=0,93`, `α=0,5²=0,25`); ghi nhận đúng đóng góp `α = Roughness²` từ `[BU12]` được `[KA13]` dùng lại.
- Lưu ý nhẹ về nguồn: Trong `sources_L00.md..sources_L06.md` vẫn còn các dòng trích gián tiếp sách giáo trình đóng `[RTR4]`/`[FCG5]`/`[PIN88]`/`[PHO75]`/`[BLI77]` đánh dấu `NOT_VERIFIED nguyên văn`, nhưng các công thức cốt lõi đã được kiểm số học và đối chiếu qua chuẩn mở `[GL46]`/`[PBR4]`/Microsoft Learn.

### 3.3. Kiểm `P1` nghiêm ngặt (đường chính + `practice#0` vs `practice#1` + `de.md` + từ khoá/viết tắt/ký hiệu)

| Bài | Các mục chưa giảng (trích nguyên văn & vị trí) | Bảng cách đọc (`practice#0`) có phủ không? | Điểm P1 |
|---|---|---|---|
| `L00` | 1) `practice.1`: `ms60, ms120 = 1000 / 60, 1000 / 120` (gán đồng thời nhiều biến, `/`, `*`), `:.2f` khác `:.3f`; 2) `practice.3`: `1080p`, `fps`, `pixel` (bài chỉ dùng "khung mỗi giây", "điểm ảnh"); 3) `practice.3`: `bash labs/cham.sh GFX L00 duong_dan/bai_cua_ban.py` (`bash`, `.sh`, tham số dòng lệnh); 4) `de.md`: `60 Hz`, `120 Hz` (`Hz` chưa giảng) | **Không** (`practice#0` chỉ có `f"{val:.3f}"` và `print(...)`) | **0** |
| `L01` | 1) `practice.1`: `rot90 = lambda x, y: (-y, x)` (`lambda` nhiều đối số, trả bộ giá trị); 2) `practice.1`: `rot90(*tr(1,0))`, `tr(*rot90(1,0))` (toán tử giải nén `*` chưa từng giảng); 3) `practice.3`: `bash labs/cham.sh GFX L01 ...` (`bash`, `.sh`) | **Không** (`practice#0` chỉ ghi `lambda x: ...`, không phủ `*` hay bộ) | **0** |
| `L02` | 1) `practice.1`: `lambda x, y, z, f=1.0:` (nhiều đối số + giá trị mặc định `f=1.0`); 2) `practice.1`: `round(f*x/z, 3)` (hàm `round` chưa giảng); 3) `practice.3`: `bash labs/cham.sh ...` (`bash`, `.sh`) | **Không** (`practice#0` thiếu `round` và đối số mặc định) | **0** |
| `L03` | 1) `practice.1`: `W=1920`, `round(...)`, danh sách `[vp(-1.0), vp(0.5), vp(1.0)]`; 2) `practice.3` & `de.md`: `NDC` (bài chỉ nói "Toạ độ thiết bị chuẩn hoá", chưa giảng chữ viết tắt `NDC`); 3) `practice.3`: `bash labs/cham.sh ...` (`bash`, `.sh`) | **Không** (`practice#0` thiếu `round`, `[...]`, `NDC`) | **0** |
| `L04` | 1) `pitfalls.1`: `(tắt sẵn trong một số giao diện lập trình, như OpenGL)` (`OpenGL` chưa giải thích); 2) `practice.1`: `int(min(l0,l1,l2)>0)` (ép kiểu `int(...)` và biểu thức logic `>0` cho `1`), `:.2f` khác `:.3f`, `de.md` dùng `l0, l1, l2` (bài dùng $\alpha, \beta, \gamma$); 3) `practice.3`: `bash labs/cham.sh ...` | **Không** (`practice#0` chỉ có `f"{val:.3f}"`, `sum/len/max/min`, `print(...)`) | **0** |
| `L05` | 1) `formula.1`: `đạo hàm của d(z)` (dùng khái niệm đạo hàm chưa giảng gốc); 2) `practice.1`: `# Khoảng phân biệt...` (cú pháp chú thích `#`), `:.0f` khác `:.3f`; 3) `practice.3`: `near=0.1 vs near=1.0`, `z-fighting` (bài chỉ dùng $n$ và "giành điểm ảnh"), `bash labs/cham.sh ...` | **Không** (`practice#0` chỉ có `f"{val:.3f}"`, `print(...)`) | **0** |
| `L06` | 1) `formula.0/1`: `Lambert`, `Blinn–Phong`, `I_diffuse`, `I_specular`, `I_ambient` (chỉ số tiếng Anh không giải thích nghĩa trên màn hình); 2) `practice.1`: `0.95 ** 32` (toán tử `**`), `:.1f`, `:.4f` khác `:.3f`; 3) `practice.3`: `vs`, `bash labs/cham.sh ...` | **Không** (`practice#0` thiếu `**`, `:.1f`, `:.4f`) | **0** |
| `L07` | 1) `pitfalls.1`: `4 MB`, `5,33 MB` (viết tắt `MB` trên màn hình không giải thích); 2) `practice.1`: `sum(0.25**k for k in range(1, 11))` (toán tử `**`, `range(1, 11)`, biểu thức sinh); 3) `practice.3`: `bash labs/cham.sh ...` | **Không** (`practice#0` chỉ có `for x in ds:`, thiếu `**`, `range`, generator) | **0** |
| `L08` | 1) `sym.0`: `(sRGB)` (viết tắt không giải thích nghĩa); 2) `practice.1`: `lin_mid ** (1.0 / 2.4)`, `round(srgb_right)`, `:.0f`; 3) `practice.3`: `vs`, `~188`, `bash labs/cham.sh ...` | **Không** (`practice#0` thiếu `**`, `round`, `:.0f`) | **0** |
| `L09` | 1) `practice.1`: `# t^2 - 10t + 24 = 0` (`#` chú thích) và `print(...)` (bài L09 **thiếu hẳn dòng `print(...)`** trong bảng `practice#0`!); 2) `practice.3` & `de.md`: `R=1` (bài dùng `r`), `bash labs/cham.sh ...` | **Không** (`practice#0` thiếu `print(...)` và `#`) | **0** |
| `L10` | 1) `practice.1`: `F0=0.04` (đối số mặc định), `((1.0 - cos_t)**5)` (toán tử `**`), `:.2f`; 2) `practice.3`: `PBR Fresnel Schlick` (chữ viết tắt `PBR` chưa từng xuất hiện/giảng trong bài); 3) `practice.3`: `bash labs/cham.sh ...` | **Không** (`practice#0` thiếu `**`, `:.2f`, đối số mặc định) | **0** |
| `L11` | 1) `practice.1`: `saved_pct={2/3*100:.1f}%` (`:.1f` khác `:.3f`, phép tính trong `{}`); 2) `practice.3`: `overdraw` (bài chỉ dùng "tô đè", không giới thiệu từ `overdraw`); 3) `practice.3`: `bash labs/cham.sh ...` | **Không** (`practice#0` chỉ có `f"{val:.3f}"`, `print(...)`) | **0** |
| `L12` | 1) `formula.0`: $\frac{d z_n}{d z}$ (ký hiệu đạo hàm Leibniz và khái niệm đạo hàm chưa giảng); 2) `practice.1`: `1000**2`, **`1 << 24`** (toán tử dịch bit `<<` hoàn toàn không giảng!), `:.2f`; 3) `practice.3`: `z-fighting`, `near`, `bash labs/cham.sh ...` | **Không** (`practice#0` thiếu `**`, `<<`, `:.2f`) | **0** |
| `L13` | 1) `hook.0`: `UE4 [KA13]` (`UE4` chưa giải thích viết tắt) và `quiz.1`: `60 fps`; 2) `practice.1`: `0.95 ** 32`, `(64 / 4) ** 0.5` (`**`), `:.1f`; 3) `practice.3`: `Monte Carlo` (thân bài chỉ viết "lấy mẫu ngẫu nhiên (dò đường)", chưa giảng `Monte Carlo`), `bash labs/cham.sh ...` | **Không** (`practice#0` thiếu `**`, `:.1f`) | **0** |

### 3.4. Kiểm thực hành `P8` nghiêm ngặt & chạy trực tiếp lab
- **Lộ lời giải & kết quả mong đợi TRƯỚC `pause: 30` (14/14 bài — lỗi `MUST`):**
  Trong cả 14 bài `L00..L13`, cảnh `practice` đều có cấu trúc 5 step giống nhau:
  - `practice#0`: bảng "viết trong mã → đọc và hiểu là"
  - `practice#1`: `<p><b>Cài đặt kiểm chứng GFX:Lxx bằng Python</b></p><div class="code">...` — **hiển thị nguyên văn 100% nội dung `labs/GFX/Lxx/loi_giai.py`**!
  - `practice#2`: `<p><b>Đầu ra chạy thật (1 dòng)</b></p><div class="code">...` — **hiển thị nguyên văn 100% nội dung `labs/GFX/Lxx/mong_doi.txt`**!
  - `practice#3`: mới có `pause: 30` với lời đọc *"Hãy bấm tạm dừng và tự làm trước."* (lúc này học viên đã thấy toàn bộ lời giải và đáp án ở 2 bước ngay trước đó!).
  - `practice#4`: lặp lại `mong_doi.txt`.
- **`de.md` không tự đứng được (14/14 bài — lỗi `MUST`):**
  - Không một tệp `labs/GFX/L00..L13/de.md` nào nêu định dạng stdout bắt buộc (`key=value`, thứ tự khoá, số chữ số thập phân, dấu ngoặc hay đơn vị dính liền). Ví dụ:
    - `L00/de.md`: *"Tính tổng điểm ảnh mỗi giây và thời gian tối đa cho phép mỗi khung ở `60 Hz` và `120 Hz`."* — không hề nói phải in `px_60hz=124416000 ms60=16.67 ms120=8.33`.
    - `L12/de.md`: *"Tính bước phân biệt Z xấp xỉ tại `z=1000m` khi tăng mặt phẳng gần gấp 50 lần."* — không hề nói phải in `dz_near001=5.96m dz_near05=0.12m` (và chữ `m` dính liền).
- **Trùng số liệu với ví dụ trong bài (13/14 bài `L00..L12` + 1 phần của `L13`):**
  - `L00` (`1920*1080`, `60`, `120`), `L01` (`(1,0)`, `90°`, `(2,0)`), `L02` (`(2,1,4)`, `(2,1,8)`), `L03` (`-1, 0.5, 1`, `W=1920`), `L04` (`(0,0),(4,0),(0,4)`, `(1,1)`), `L05` (`0.1 vs 1.0`, `far=1000, z=100`), `L06` (`0.8`, `0.95^32`, `0.95^128`), `L07` (`10,20,30,40`, `1024`), `L08` (`0` và `255`), `L09` (`(0,0,0)+(0,0,1)t`, cầu `(0,0,5)` `R=1`), `L10` (`F0=0.04`, `cos=1, 0.5`), `L11` (`1080p`, `overdraw=3`), `L12` (`z=1000`, `0.01 vs 0.5`) đều **trùng y hệt** số liệu của `example` trong bài. Riêng `L13` dùng `0.95^32` (trùng `stage1`) nhưng đổi tỉ lệ Monte Carlo từ `16→1600` (giảm `10x`) sang `4→64` (giảm `4.0x`).
- **Kết quả chạy thật `loi_giai.py` bằng `.venv\Scripts\python.exe` so từng ký tự `mong_doi.txt` (14/14 khớp 100%):**
  - `L00`: `px_60hz=124416000 ms60=16.67 ms120=8.33` (PASS)
  - `L01`: `T_then_R=(0, 3) R_then_T=(2, 1)` (PASS)
  - `L02`: `at_z4=(0.5, 0.25) at_z8=(0.25, 0.125)` (PASS)
  - `L03`: `ndc_to_px=[0, 1440, 1920]` (PASS)
  - `L04`: `bary=(0.50, 0.25, 0.25) inside=1` (PASS — lưu ý code hardcode `0.5 * 1 * 4` thay vì tính hàm cạnh từ toạ độ)
  - `L05`: `precision_gain_at_z100=10x` (PASS — lưu ý code chỉ chia `1.0 / 0.1`, không dùng `far=1000, z=100`)
  - `L06`: `diffuse=0.8 spec_s32=0.1937 spec_s128=0.0014` (PASS — lưu ý code gán cứng `n_dot_l = 0.8` không tính tích vô hướng)
  - `L07`: `bilerp=25.0 mip_extra_ratio=0.333` (PASS)
  - `L08`: `wrong_srgb=128 correct_linear_blend=188` (PASS)
  - `L09`: `hits=(4.0, 6.0) nearest=4.0` (PASS)
  - `L10`: `F_0deg=0.04 F_60deg=0.070` (PASS)
  - `L11`: `overdraw3=6220800 earlyZ=2073600 saved_pct=66.7%` (PASS)
  - `L12`: `dz_near001=5.96m dz_near05=0.12m` (PASS)
  - `L13`: `phong=0.194 mc_noise_reduction_64=4.0x` (PASS)

### 3.5. Kiểm `P9` (quy mô / thời gian)
- **`recap` có mục chuẩn `Hai mức quy mô:`:** **0 / 14 bài** có mục `"Hai mức quy mô:"` trong `recap`.
- **Thân bài có ≥ 2 mức quy mô kèm số đo và đánh đổi:**
  - **Có trong thân bài (6 bài, `P9 = 1` vì thiếu ở `recap`):** `L00` (`60` vs `120 fps`, VR `2160×2160×2 @ 90 fps`, đánh đổi tầng nghẽn); `L05` (`16-bit` vs `24-bit`, `z=50/100/200 m`, `n=0.1` vs `1.0` + đánh đổi cắt vật gần); `L07` (`256×256` vs `1024×1024`, `+1/3` bộ nhớ vs răng cưa, 4 chế độ lọc); `L11` (`1080p` vs `1440p`, `500` draw calls vs `1`, `50k` tris vs `3125`, ngoại lệ bán trong suốt / `Early-Z`); `L12` (`z=500` vs `1000 m`, `f=10 km` vs `100 km`, bảng 3 phương án kèm đánh đổi băng thông/lệnh vẽ/vật sát mắt); `L13` (4 mốc 1975→1980→1994→2012–2013 + di động `60 fps / 16,67 ms` vs phim `2 giờ/khung`).
  - **Không có trong thân bài (8 bài, `P9 = 0`):** `L01, L02, L03, L04, L06, L08, L09, L10` (chỉ có `L10` so sánh 3 góc nhìn của cùng 1 vật liệu, `L06` so sánh `s=32` vs `128`, `L02` so sánh `z=4` vs `8` — đều không có quy mô hệ thống & đánh đổi kỹ thuật).

### 3.6. Quét câu `"càng "`, ký hiệu thô, `SPELL_CANON`, `lv.lint`, `build_report.json`, `SRT`, `ASR`, `screen_code`, `layout_GFX.tsv`
- **Câu `"càng "` trong `say`/`show`:** Chỉ xuất hiện 2 chỗ ở `L06`:
  - `L06 sym.0`: `vật liệu càng bóng, $s$ càng lớn` (chính xác: $s$ lớn → đốm sáng gom hẹp sắc hơn).
  - `L06 pitfalls.0`: `tam giác càng lớn trên mặt cong thì lệch càng nhiều` (chính xác: tam giác càng rộng, pháp tuyến đỉnh lệch góc càng lớn nên nội suy tuyến tính co ngắn nhiều hơn).
- **Ký hiệu toán thô trong `say`:** **0** phát hiện ở cả 14 bài.
- **`SPELL_CANON` & `lv.lint`:** **0** vi phạm `SPELL_CANON`; `lv.lint` đạt **0 FAIL, 0 WARN** trên cả 14 bài.
- **`build_report.json` (`spec_sha256` & `tts_sha256`):** **14/14 khớp 100%** với `lv.spec_digest` và `lv.tts_digest`.
- **`L*.srt == say`:** **14/14 khớp 100%** từng câu.
- **`asr_report.md`:** **14/14** đều có `thiếu audio: 0` và `chưa xem xét: 0` (số câu gắn cờ đã `asr_reviewed` hết: L00:5, L01:1, L02:6, L03:9, L04:3, L05:3, L06:4, L07:3, L08:23, L09:6, L10:12, L11:3, L12:3, L13:0).
- **`audit/layout_GFX.tsv`:** Rỗng (1 dòng trống) — 0 lỗi bố cục tự động.
- **`audit/review/screen_code/GFX.yaml` (LỖI `MUST`):** Có đủ 42/42 khối (`missing=[]`, `orphan=[]`, `stale=[]`), nhưng **toàn bộ 14 khối mã Python `GFX L00..L13 practice 1 0` bị khai sai thành `kind: other, lang: text`** với `reason: "Đầu ra mong đợi chính xác của lab labs/GFX/Lxx..."` thay vì `kind: run, lang: python`. Do đó cổng `screen_code.py` chưa bao giờ thực sự chạy kiểm các khối mã Python trên màn hình qua sổ này.

### 3.7. Kiểm tra trực quan bằng `read_file` các khung hình PNG (67 khung hình)
- **Phát hiện khi xem bằng mắt:**
  - `D:\research-video\out\GFX\L09\frames\00014.png` (`intuition`): Chữ `"Tia trượt (Δ < 0)"` bị đường tia nét đứt màu xám cắt ngang qua; chữ `"Tia bóng đổ tới đèn"` đè lên mép trên vòng tròn quả cầu xanh lam (`y=135` sát đỉnh `y=130`).
  - `D:\research-video\out\GFX\L00..L13`: Tất cả các khung `practice#1` (`00073`, `00069`, `00064`, `00065`, `00065`, `00062`, `00051`, `00074`, `00065`, `00065`, `00070`, `00066`, `00073`, `00052`) hiển thị rõ nét, không cắt chữ nhưng **lộ nguyên văn lời giải `loi_giai.py`** ngay trước khung `practice#3` (`pause: 30`).
  - Các khung KaTeX, bảng, chuỗi logic đã đọc (`L00..L13` SVG, `practice#0/#1/#3`, `hook`, `quiz`, `recap`) đều rõ tương phản màu, không cắt công thức KaTeX, không tràn viền, không xuống 2 dòng đè tiêu đề.

- **Danh sách chính xác 67 tệp PNG đã đọc bằng `read_file`:**
  - Hook: `out/GFX/L00/frames/00000.png`, `out/GFX/L01/frames/00000.png`, `out/GFX/L02/frames/00000.png`, `out/GFX/L13/frames/00000.png`
  - SVG (`intuition` / `timeline`): `out/GFX/L00/frames/00025.png`, `out/GFX/L01/frames/00021.png`, `out/GFX/L02/frames/00017.png`, `out/GFX/L03/frames/00017.png`, `out/GFX/L04/frames/00019.png`, `out/GFX/L05/frames/00017.png`, `out/GFX/L06/frames/00016.png`, `out/GFX/L07/frames/00022.png`, `out/GFX/L08/frames/00015.png`, `out/GFX/L09/frames/00014.png`, `out/GFX/L10/frames/00019.png`, `out/GFX/L11/frames/00021.png`, `out/GFX/L12/frames/00017.png`, `out/GFX/L13/frames/00013.png`
  - `practice#0 / #1 / #3` (14 × 3 = 42 PNG):
    - `L00`: `00072.png`, `00073.png`, `00075.png`
    - `L01`: `00068.png`, `00069.png`, `00071.png`
    - `L02`: `00063.png`, `00064.png`, `00066.png`
    - `L03`: `00064.png`, `00065.png`, `00067.png`
    - `L04`: `00064.png`, `00065.png`, `00067.png`
    - `L05`: `00061.png`, `00062.png`, `00064.png`
    - `L06`: `00050.png`, `00051.png`, `00053.png`
    - `L07`: `00073.png`, `00074.png`, `00076.png`
    - `L08`: `00064.png`, `00065.png`, `00067.png`
    - `L09`: `00064.png`, `00065.png`, `00067.png`
    - `L10`: `00069.png`, `00070.png`, `00072.png`
    - `L11`: `00065.png`, `00066.png`, `00068.png`
    - `L12`: `00072.png`, `00073.png`, `00075.png`
    - `L13`: `00051.png`, `00052.png`, `00054.png`
  - Khung KaTeX / Quiz / Recap bổ sung: `out/GFX/L01/frames/00028.png`, `out/GFX/L06/frames/00049.png`, `out/GFX/L08/frames/00020.png`, `out/GFX/L10/frames/00030.png`, `out/GFX/L12/frames/00025.png`, `out/GFX/L13/frames/00050.png`, `out/GFX/L13/frames/00058.png` (tất cả thuộc `D:\research-video\...`).

---

## 4. Người học kẹt ở đâu (14 bài)

- **`L00`**: Kẹt ở `practice.1` (`ms60, ms120 = 1000 / 60, 1000 / 120`, `:.2f` khác `:.3f`) và `practice.3` (`1080p`, `fps`, `pixel`, `bash labs/cham.sh ...`) + `de.md` không ghi định dạng stdout.
- **`L01`**: Kẹt ở `practice.1` (`rot90(*tr(1,0))` — toán tử giải nén `*` và `lambda x, y:` hai đối số chưa giảng) và `practice.3` (`bash labs/cham.sh ...`).
- **`L02`**: Kẹt ở `practice.1` (`lambda x, y, z, f=1.0:` và `round(...)` chưa giảng) và `practice.3` (`bash labs/cham.sh ...`).
- **`L03`**: Kẹt ở `practice.1` (`round(...)`, `[vp(-1.0), vp(0.5), vp(1.0)]` danh sách Python) và `practice.3` (`NDC`, `bash labs/cham.sh ...`).
- **`L04`**: Kẹt ở `pitfalls.1` (`OpenGL`), `practice.1` (`int(min(l0,l1,l2)>0)`, `:.2f`) và `de.md` dùng ký hiệu `l0, l1, l2` khác $\alpha, \beta, \gamma$ trong bài.
- **`L05`**: Kẹt ở `formula.1` (`đạo hàm của d(z)` chưa giảng), `practice.1` (chú thích `#`, `:.0f`) và `practice.3` (`near=0.1 vs near=1.0`, `z-fighting`, `bash labs/cham.sh ...`).
- **`L06`**: Kẹt ở `formula.0/1` (chỉ số tiếng Anh `diffuse`, `specular`, `ambient`), `practice.1` (`0.95 ** 32` toán tử `**`, `:.1f`, `:.4f`) và `practice.3` (`vs`, `bash labs/cham.sh ...`).
- **`L07`**: Kẹt ở `pitfalls.1` (`4 MB`, `5,33 MB`), `practice.1` (`sum(0.25**k for k in range(1, 11))` — `**`, `range`, biểu thức sinh) và `practice.3` (`bash labs/cham.sh ...`).
- **`L08`**: Kẹt ở `sym.0` (`sRGB` chưa giải thích nghĩa), `practice.1` (`**`, `round`, `:.0f`) và `practice.3` (`vs`, `~188`, `bash labs/cham.sh ...`).
- **`L09`**: Kẹt ở `practice.1` (`# t^2 - 10t + 24 = 0`, `print(...)` không có trong `practice#0`) và `de.md` (`R=1`) + `practice.3` (`bash labs/cham.sh ...`).
- **`L10`**: Kẹt ở `practice.1` (`F0=0.04` mặc định, `**5`, `:.2f`) và `practice.3` (`PBR` chưa giảng, `bash labs/cham.sh ...`).
- **`L11`**: Kẹt ở `practice.1` (`{2/3*100:.1f}`) và `practice.3` (`overdraw`, `bash labs/cham.sh ...`).
- **`L12`**: Kẹt ở `formula.0` (đạo hàm $\frac{dz_n}{dz}$), `practice.1` (`1000**2`, **`1 << 24`** chưa giảng), `practice.3` (`z-fighting`, `near`, `bash labs/cham.sh ...`).
- **`L13`**: Kẹt ở `hook.0` (`UE4`), `quiz.1` (`60 fps`), `practice.1` (`0.95 ** 32`, `(64 / 4) ** 0.5`), và `practice.3` (`Monte Carlo`, `bash labs/cham.sh ...`).
