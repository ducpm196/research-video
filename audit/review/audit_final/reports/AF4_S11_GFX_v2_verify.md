# Báo cáo kiểm định độc lập AF4 v2 — Stage 11 `GFX` (L00–L13)

**Kết luận tổng thể: `NO-GO`**

Đã khắc phục triệt để: **0/14 lộ code/output trước `pause: 30`**, **`lv.py lint` 0 FAIL / 0 WARN & >= 9 phút (14/14)**, **`P9 = 2` (14/14)**, **`screen_code` 28/28 PASS**, **`verify_gfx.py` 19/19 PASS**, **`layout_GFX.tsv` 0 lỗi**, **`loi_giai.py == mong_doi.txt` 14/14**.

Còn 4 nhóm vấn đề cần vá:
1. **`covers:` (E51) trỏ sai cảnh thực dạy ở 12/14 bài** (`L00, L01, L03..L08, L10..L13`; thêm `L02, L09` trỏ yếu 1 mục tiêu).
2. **`P1` (`0/14` đạt `P1=2`):** Bảng `practice#2/#3` chèn thừa `dict(...)` (13 bài), `set()` (`L03`), `all(...)` (`L01, L06, L07`) nhưng thiếu cú pháp thật (`a, b = ...`, `lambda` nhiều đối số/mặc định, `tuple(...)`, `M[i][j]`, `for a, b in zip`, `range(a, b)`, `#`, `> 0`); `de.md`/`practice#0`/thân bài còn ký hiệu/viết tắt chưa mở nghĩa (`720p, px, Hz, fps, NDC, near/far, sRGB, OpenGL, PBR, BVH, UE4, overdraw, Monte Carlo, bash/.sh`).
3. **`P8` (`11/14` đạt `P8=2`):** `L08/de.md` trùng 100% số bài (`128, 0, 255, 0.5`); `L02/de.md` trùng `z0=2, z1=6`; `L05/de.md` & `L07/de.md` thiếu quy ước làm tròn; `L07/loi_giai.py` có dòng chết `if False` & hardcode `levels=10`; `L01/de.md` thiếu chú thích int 2D.
4. **SVG `L09` (`intuition#0`)**: `"Tia hướng d = (0,0,1)"` tại `y=195` bị đường nét đứt cắt ngang (cần dời xuống `y=228`); và **14/14 MP4 chưa rebuild**.

---

## Bảng chi tiết từng bài (`L00..L13`)
| Bài | Phút | MUST | P1 | P8 | P9 | Lỗi chính |
|---|---:|---:|---:|---:|---:|---|
| `L00` | 13,3 | 1 | 0 | 2 | 2 | `covers` obj1/3; `ms60, ms144 =`, `dict` ma; `720p/px/Hz/fps` |
| `L01` | 14,1 | 1 | 0 | 2* | 2 | `covers` obj3; `tuple()`, `(1,2,1)`, `M[i][j]`, `round(,2)`, `dict`/`all` ma; `de.md` int 2D |
| `L02` | 13,1 | 0* | 0 | 1 | 2 | `covers` obj2; `lambda` nhiều đối số/mặc định, `tuple`, `dict` ma; `de.md` trùng `z0=2,z1=6` |
| `L03` | 12,8 | 1 | 0 | 2 | 2 | `covers` obj1/3; `lambda` 2 đối số/mặc định, `set` ma; `NDC/px` |
| `L04` | 13,1 | 1 | 0 | 2 | 2 | `covers` obj3; `lambda` 3 đối số, unpacking, `(0,0)`, `>0`, `dict` ma; `OpenGL` |
| `L05` | 12,4 | 1 | 0 | 1 | 2 | `covers` obj2/3; `lambda` mặc định, `d1,d2=`, `dict` ma; `de.md` thiếu làm tròn |
| `L06` | 9,7 | 1 | 0 | 2 | 2 | `covers` obj3/4; `(0,0.6,0.8)`, `for a, b in zip`, `dict/all` ma; `I_diffuse/fps` |
| `L07` | 14,7 | 1 | 0 | 1* | 2 | `covers` obj3/4; `u,v=`, `range(1,10)`, `if False` chết + hardcode `levels=10`, `dict/all` ma; `de.md` thiếu làm tròn `bilerp` |
| `L08` | 13,4 | 1 | 0 | 1 | 2 | `covers` obj4; `dict` ma, `sRGB`; `de.md` trùng 100% số bài (`128, 0, 255, 0.5`) |
| `L09` | 14,4 | 0* | 0 | 2 | 2 | `covers` obj2; `#`, `b,c=`, `t1,t2=`, `dict` ma, `BVH`; SVG `y=195 -> 228` |
| `L10` | 14,9 | 1 | 0 | 2 | 2 | `covers` obj4; `lambda` 2 đối số/mặc định, `dict` ma, `PBR` |
| `L11` | 14,0 | 1 | 0 | 2 | 2 | `covers` obj2; `dict` ma, `overdraw` |
| `L12` | 13,5 | 1 | 0 | 2 | 2 | `covers` obj3; `lambda` 3 đối số/mặc định, `dict` ma |
| `L13` | 9,3 | 1 | 0 | 2 | 2 | `covers` obj3; `dict` ma, `UE4/fps/PBR/Monte Carlo` |
