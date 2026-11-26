# Đánh giá độc lập Sample I-b (AF5 — 10 bài Lớp A, trọng tâm S5 Thực hành & Lab + đối chiếu S1–5)

- Ngày kiểm: `2026-11-24`
- Phạm vi: đọc độc lập 10 bài Lớp A (`JV2 L03`, `DMS L11`, `DMS L05`, `BNX L15`, `CS115 L19`, `FND L06`, `BNK L01`, `ACB L05`, `FND L09`, `DMS L17`) — trọn YAML, `curriculum/*.yaml`, `labs/<KHOÁ>/<Lxx>/*`, `labs/CONTRACT.yaml`, `audit/review/boiler_deny.txt`, `out/<KHOÁ>/<Lxx>/{build_report.json,asr_report.md,frames/*.png}` (tối thiểu 4 khung/bài).
- Môi trường kiểm trên máy đọc: JDK 22.0.2 (`javac`/`java`) và PowerShell chạy được; `python` / `bash` bị chặn quyền (`Access is denied` / `NtCreateDirectoryObject 0xC0000022`) nên lab Python/Shell ghi rõ `CHƯA KIỂM (sandbox chặn python/bash)` kèm kiểm tra phép tính và logic thủ công/PowerShell.
- Cả 10/10 bài thuộc Lớp A nên theo `labs/CONTRACT.yaml` đều có `ca_them: 'mien: lop_A_da_dat', ca_an: false` (`L5` được miễn theo hợp đồng).
- `boiler_deny.txt`: **0/10** bài dính câu khuôn mẫu rỗng. `checks` hằng đẳng thức rỗng / chấm điểm giả: **0/10** bài vi phạm.
- ASR `chưa xem xét`: **0/10** bài còn câu chưa xem xét trong `asr_report.md` (lưu ý: 5 bài `DMS L11`, `DMS L05`, `BNK L01`, `ACB L05`, `FND L09` có `asr_report.md` `checked_at` cũ hơn lần `build` gần nhất).

---

## Bảng tổng hợp 10 bài

| # | Bài | `sha16` | Từ đọc / Thời lượng (không pause) | `built_at >= mtime` | ASR chưa xem | `covers` | `P1–P7` (`P8,P9`) | `L1–L5` | MUST | SHOULD | Lỗi chặn / Ghi chú chính |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `JV2 L03` | `3095efcc985c2abd` | 2 369 từ / 13,42 phút (`pause 205s`) | Đạt (`03:31:09Z >= 03:07:56Z`) | 0 | 4/5 | 14/14 (`2,2`) ĐỦ | `1/1/2/2/N/A` | **0** | 4 | Vượt trần 2 300 từ (2 369); `covers` obj 1 trỏ `formula` thay vì `sym`; `practice` step 1 thiếu bảng 8 giao dịch trên màn hình; `counting()`/`merge()` chưa giảng trước `practice` |
| 2 | `DMS L11` | `bd89346c33d36faf` | 1 979 từ / 11,14 phút (`pause 390s`) | Đạt (`00:30:52Z >= 17:37:34Z`) | 0 *(checked 17/11)* | 5/5 | 14/14 (`2,2`) ĐỦ | `1/2/2/CK*/N/A` | **0** | 2 | `pause = 390s > 300s`; `practice` step 1 thiếu bộ số cụ thể 4 bài đếm trên màn hình |
| 3 | `DMS L05` | `793dc54a10573409` | 2 128 từ / 12,61 phút (`pause 248s`) | Đạt (`00:11:55Z >= 16:54:25Z`) | 0 *(checked 17/11)* | 5/5 | 14/14 (`2,2`) ĐỦ | `2/2/2/CK*/N/A` | **0** | 0 | Sạch; `asr_report` cũ hơn lần build |
| 4 | `BNX L15` | `8f7476b41a038717` | 2 298 từ / 12,12 phút (`pause 145s`) | **LỖI** (`06:18:51Z < 07:53:50Z`) | 0 | 6/6 | 14/14 (`2,2`) ĐỦ | `2/2/2/CK*/N/A` | **1** | 0 | **BLOCKER**: `built_at` & `L15.mp4` cũ hơn `mtime` YAML ~95 phút, cần rebuild |
| 5 | `CS115 L19` | `3883e59e5299a43e` | 1 952 từ / 11,22 phút (`pause 300s`) | Đạt (`02:47:18Z >= 02:40:16Z`) | 0 | 6/6 | 14/14 (`2,2`) ĐỦ | `2/2/2/CK*/N/A` | **0** | 0 | Sạch |
| 6 | `FND L06` | `83592fa59573ca57` | 2 060 từ / 11,85 phút (`pause 360s`) | Đạt (`22:20:12Z >= 21:22:54Z`) | 0 | 6/6 | 14/14 (`2,2`) ĐỦ | `1/2/2/CK*/N/A` | **0** | 2 | `pause = 360s > 300s`; `practice` step 1 không hiện mã `doc.py` và khối YAML trên màn hình (phải mở `de.md`) |
| 7 | `BNK L01` | `7a41320fa0003902` | 2 299 từ / 12,82 phút (`pause 145s`) | Đạt (`19:56:39Z >= 16:47:30Z`) | 0 *(checked 17/11)* | 5/5 | 14/14 (`2,2`) ĐỦ | `2/2/2/2/N/A` | **0** | 0 | Sạch; chạy thật `TongBaLuong.java` ra `tong = 600000` khớp `mong_doi.txt`; `asr_report` cũ hơn lần build |
| 8 | `ACB L05` | `4f2e83ffcc0a3e37` | 2 296 từ / 12,53 phút (`pause 285s`) | Đạt (`19:40:44Z >= 17:12:51Z`) | 0 *(checked 22/11)* | 9/9 | 14/14 (`2,2`) ĐỦ | `2/2/2/CK*/N/A` | **0** | 0 | Sạch; `asr_report` cũ hơn lần build |
| 9 | `FND L09` | `2e5acf1f68b62b40` | 2 230 từ / 12,78 phút (`pause 300s`) | Đạt (`02:57:28Z >= 02:41:18Z`) | 0 *(checked 22/11)* | 8/8 | 14/14 (`2,2`) ĐỦ | `2/2/2/CK*/N/A` | **0** | 0 | Sạch; `asr_report` cũ hơn lần build |
| 10 | `DMS L17` | `035c50447e6c4178` | 2 213 từ / 12,25 phút (`pause 300s`) | **LỖI** (`00:51:28Z < 02:46:00Z`) | 0 | 5/5 | 14/14 (`2,2`) ĐỦ | `1/2/2/CK*/N/A` | **1** | 1 | **BLOCKER**: `built_at` & `L17.mp4` cũ hơn `mtime` YAML ~115 phút; `practice` step 1 thiếu danh sách cạnh 4 đồ thị `H1..H4` trên màn hình |

*\*`CK`: `CHƯA KIỂM` chạy `cham.sh` do sandbox chặn `python`/`bash`; đã kiểm lại công thức/số liệu và đối chiếu logic `loi_giai.*` với `mong_doi.txt`.*

**Kết luận chung lô Sample I-b:** **KHÔNG đạt `MUST = 0` — có 2 lỗi chặn (`MUST = 2` trên toàn lô)** tại `BNX L15` và `DMS L17` do `built_at` của video (`build_report.json` & `.mp4`) cũ hơn `mtime` của tệp YAML đặc tả. Về nội dung kiến thức, độ sâu mất gốc (`P1–P7 = 14/14`, `P8 = 2`, `P9 = 2`) và cấu trúc lab (`L3`, `mong_doi.txt`, miễn `ca_an` theo `CONTRACT.yaml`), cả 10 bài đều đạt chuẩn, chỉ còn các lỗi `SHOULD` ở `JV2 L03`, `DMS L11`, `FND L06`, `DMS L17`.

---

## Chi tiết từng bài

### 1. `JV2 L03` — `sha16`: `3095efcc985c2abd`
- Tệp: `lessons/jv2/L03_ham_la_gia_tri_stream.yaml`, `labs/JV2/L03/{de.md, mong_doi.txt, loi_giai.java}`
- Thời lượng / từ: `16:50` (`1009,933s`), `pause = 205s` (`25 + 180`), không pause `13,42 phút` / `2 369 từ`.
- `built_at` `2026-11-24T03:31:09Z` >= `mtime` `2026-11-24T03:07:56Z`. ASR: 163 câu, thiếu 0, gắn cờ 2 (đã `asr_reviewed`), chưa xem xét: 0.
- Khung hình đã xem: `00025.png`, `00031.png`, `00035.png`, `00090.png`, `00130.png`, `00142.png`, `00150.png`, `00157.png` — bố cục rõ, SVG băng chuyền sạch, không chồng chữ/cắt cụt.
- Thực nghiệm chạy lại:
  - Biên dịch và chạy thật `labs/JV2/L03/loi_giai.java` (`ThongKeStream.java`) bằng JDK 22.0.2 trong `%TEMP%`: in đúng 4 dòng `Rut tu 500000: 1700000`, `Dem: {chuyen=2, nap=3, rut=3}`, `Tong: {chuyen=2300000, nap=3850000, rut=2150000}`, `Khop vong lap: true` — khớp `mong_doi.txt`.
  - Tính lại tổng `TaoFile 1000000` bằng PowerShell: `chuyen=1333332000`, `nap=1333334000`, `rut=1333332000`, tổng `3999998000` — khớp chính xác màn hình `scale`.
- Đánh giá S1–5 & Lab (`L1=1, L2=1, L3=2, L4=2, L5=N/A`):
  - **SHOULD 1**: Lời đọc `2 369` từ vượt trần `2 300` từ của hợp đồng (`CONTRACT` / `BRIEF_AF5.md` §D; bài không phải `kind: journey`). Đề xuất: rút gọn ~80 từ ở `scale`/`pitfalls`.
  - **SHOULD 2**: `covers` gán `objective: 1` ("Đọc hàm ngắn, giao diện hàm và tham chiếu hàm") vào `scene: formula`, trong khi phần giải mã ký hiệu (`->`, `Predicate`, `Function`, `GiaoDich::soTien`) giảng ở `sym`. Đề xuất: sửa `covers` trỏ `sym`.
  - **SHOULD 3 (`L1 = 1`)**: `practice` step 1 chỉ ghi `tám giao dịch (số liệu trong de.md)` mà không hiện 8 cặp số liệu lên màn hình video.
  - **SHOULD 4 (`L2 = 1`)**: `de.md` yêu cầu `Collectors.counting()` và `TreeMap.merge(..., Long::sum)` chưa giảng trước phần `practice` (mới xuất hiện trong gợi ý `Nếu kẹt`).

### 2. `DMS L11` — `sha16`: `bd89346c33d36faf`
- Tệp: `lessons/dms/L11_chia_keo.yaml`, `labs/DMS/L11/{de.md, mong_doi.txt, loi_giai.py}`
- Thời lượng / từ: `17:38` (`1058,2s`), `pause = 390s` (`30 + 360`), không pause `11,14 phút` / `1 979 từ`.
- `built_at` `2026-11-24T00:30:52Z` >= `mtime` `2026-11-23T17:37:34Z`. ASR: 109 câu, chưa xem xét: 0 (lưu ý `checked_at: 2026-11-17T11:14:14Z` cũ hơn lần build 24/11).
- Khung hình đã xem: `00022.png`, `00027.png` (SVG 12 ô sao & vạch rõ đẹp), `00060.png`, `00095.png`, `00105.png`.
- Kiểm chứng số liệu: $\binom{10}{3}=120$, $\binom{8}{2}=28$, $\binom{9}{5}=126$, $\binom{12}{2}-3\binom{6}{2}=66-45=21$ khớp `mong_doi.txt`. Chạy `loi_giai.py`: `CHƯA KIỂM (sandbox chặn python/bash)`.
- Đánh giá S1–5 & Lab (`L1=1, L2=2, L3=2, L4=CHƯA KIỂM, L5=N/A`):
  - `covers`: 5/5 đúng.
  - **SHOULD 1**: Tổng `pause = 390s > 300s` (vi phạm ngưỡng `≤ 300s`). Đề xuất: giảm `practice pause` xuống `<= 270s`.
  - **SHOULD 2 (`L1 = 1`)**: `practice` step 1 nêu 4 loại bài đếm nhưng không hiện bộ số cụ thể (`x1+x2+x3+x4=7`, `x1+x2+x3=12, >=2`, `4 viên từ 6 vị`, `<=5`) trên màn hình.

### 3. `DMS L05` — `sha16`: `793dc54a10573409`
- Tệp: `lessons/dms/L05_tap_hop.yaml`, `labs/DMS/L05/{de.md, mong_doi.txt, loi_giai.py}`
- Thời lượng / từ: `16:45` (`1004,5s`), `pause = 248s` (`8 + 240`), không pause `12,61 phút` / `2 128 từ`.
- `built_at` `2026-11-24T00:11:55Z` >= `mtime` `2026-11-23T16:54:25Z`. ASR: 127 câu, chưa xem xét: 0 (`checked_at: 2026-11-17T13:38:29Z`).
- Khung hình đã xem: `00043.png`, `00080.png`, `00112.png`, `00120.png` — rõ, không chồng lấn.
- Kiểm chứng số liệu: `A={2,3,5,7,11,13}`, `B={1,3,5,7,9,11}` -> `hop: 1 2 3 5 7 9 11 13`, `giao: 3 5 7 11`, `A bo B: 2 13`, `B bo A: 1 9`, `2^6=64`, `1000//4 + 1000//6 - 1000//12 = 250 + 166 - 83 = 333` khớp `mong_doi.txt`. Chạy `loi_giai.py`: `CHƯA KIỂM (sandbox chặn python/bash)`.
- Đánh giá S1–5 & Lab (`L1=2, L2=2, L3=2, L4=CHƯA KIỂM, L5=N/A`): 0 lỗi MUST/SHOULD.

### 4. `BNX L15` — `sha16`: `8f7476b41a038717`
- Tệp: `lessons/bnx/L15_tinh_huong_du_an_mau.yaml`, `labs/BNX/L15/{de.md, mong_doi.txt, loi_giai.py}`
- Thời lượng / từ: `14:32` (`872,367s`), `pause = 145s` (`25 + 120`), không pause `12,12 phút` / `2 298 từ`.
- **Trạng thái build**: `built_at` (`2026-11-22T06:18:51Z`) và `out/BNX/L15/L15.mp4` (`2026-11-22T06:18:51Z`) **CŨ HƠN** `YAML mtime` (`2026-11-22T07:53:50Z`). ASR: 108 câu, chưa xem xét: 0 (`checked_at: 2026-11-22T07:53:58Z`).
- Khung hình đã xem: `00025.png`, `00030.png`, `00032.png`, `00035.png`, `00095.png`, `00105.png` — 2 SVG kiến trúc & ngân sách độ trễ rất rõ, không chồng chữ.
- Kiểm chứng số liệu (PowerShell): `cung_luc(116)=5`, `cung_luc(11574)=463`, `cung_luc(1157407)=46297` khớp `quymo`; bài lab `5_000_000/86400 = 57,87 -> 57.9`, `cao = 347,22 -> 347`, `du = 400 - 166 = 234`, `dong_thoi = 41,667 -> 41.7`, `ceil = 42` khớp `mong_doi.txt`. Chạy `loi_giai.py`: `CHƯA KIỂM (sandbox chặn python/bash)`.
- Đánh giá S1–5 & Lab (`L1=2, L2=2, L3=2, L4=CHƯA KIỂM, L5=N/A`):
  - **MUST 1 (Blocker build)**: `built_at` (`06:18:51Z`) cũ hơn `mtime` YAML (`07:53:50Z`). Cần build lại `BNX L15` để video khớp bản YAML hiện tại.

### 5. `CS115 L19` — `sha16`: `3883e59e5299a43e`
- Tệp: `lessons/cs115/L19_qua_khop_chinh_quy_hoa.yaml`, `labs/CS115/L19/{de.md, mong_doi.txt, loi_giai.py}`
- Thời lượng / từ: `16:13` (`973,4s`), `pause = 300s` (`45 + 255`), không pause `11,22 phút` / `1 952 từ`.
- `built_at` `2026-11-24T02:47:18Z` >= `mtime` `2026-11-24T02:40:16Z`. ASR: 114 câu, chưa xem xét: 0 (`checked_at: 2026-11-24T02:47:21Z`).
- Khung hình đã xem: `00001.png`, `00050.png`, `00085.png`, `00105.png` — đồ thị quá khớp, bảng, công thức, hint `Nếu kẹt` đều sắc nét.
- Kiểm chứng số liệu: `X=[[1,1],[2,2],[3,3]]`, `y=[2,4,6]` -> `X^T X = [[14,14],[14,14]]` (`det=0`), `b=[28,28]`, `lam=1`: `det=29`, `w=[28/29, 28/29]`; `lam=1/10`: `det=281/100`, `w=[280/281, 280/281]`; L1 (`lam=2`): `3->2, 1/2->0, -2->-1`; CV 4 phần 12 mẫu: `9, 3` — khớp `mong_doi.txt`. Chạy `loi_giai.py`: `CHƯA KIỂM (sandbox chặn python/bash)`.
- Đánh giá S1–5 & Lab (`L1=2, L2=2, L3=2, L4=CHƯA KIỂM, L5=N/A`): 0 lỗi MUST/SHOULD.

### 6. `FND L06` — `sha16`: `83592fa59573ca57`
- Tệp: `lessons/fnd/L06_du_lieu_co_cau_truc.yaml`, `labs/FND/L06/{de.md, mong_doi.txt, loi_giai.sh}`
- Thời lượng / từ: `17:51` (`1071,033s`), `pause = 360s` (`60 + 300`), không pause `11,85 phút` / `2 060 từ`.
- `built_at` `2026-11-16T22:20:12Z` >= `mtime` `2026-11-16T21:22:54Z`. ASR: 131 câu, chưa xem xét: 0 (`checked_at: 2026-11-16T22:20:58Z`).
- Khung hình đã xem: `00025.png` (SVG 3 cột CSV/JSON/YAML rõ), `00030.png`, `00090.png`, `00118.png`, `00127.png`.
- Kiểm chứng số liệu: `scale` 15/39 (`2.6`), 1592/3992 (`2.5`), 178894/418894 (`2.3`); lab `4*90000+45000+6*8000=453000`, `8080+5432=13512` khớp `mong_doi.txt`. Chạy `loi_giai.sh`: `CHƯA KIỂM (sandbox chặn python/bash)`.
- Đánh giá S1–5 & Lab (`L1=1, L2=2, L3=2, L4=CHƯA KIỂM, L5=N/A`):
  - **SHOULD 1**: Tổng `pause = 360s > 300s`.
  - **SHOULD 2 (`L1 = 1`)**: `practice` step 1 chỉ hiện dữ liệu phần 1 (viết `don.json`), còn phần 2 (`doc.py`) và phần 3 (nội dung YAML cần đọc) buộc mở `de.md`.

### 7. `BNK L01` — `sha16`: `7a41320fa0003902`
- Tệp: `lessons/bnk/L01_da_luong_khoa_luong_ao.yaml`, `labs/BNK/L01/{de.md, mong_doi.txt, loi_giai.java}`
- Thời lượng / từ: `15:14` (`914,1s`), `pause = 145s` (`25 + 120`), không pause `12,82 phút` / `2 299 từ`.
- `built_at` `2026-11-23T19:56:39Z` >= `mtime` `2026-11-23T16:47:30Z`. ASR: 139 câu, chưa xem xét: 0 (`checked_at: 2026-11-17T07:20:45Z`).
- Khung hình đã xem: `00030.png` (SVG xen kẽ A/B rõ), `00095.png`, `00125.png`, `00135.png`.
- Thực nghiệm chạy lại: biên dịch và chạy thật `labs/BNK/L01/loi_giai.java` (`TongBaLuong.java`) bằng JDK 22.0.2 trong `%TEMP%` -> in `tong = 600000`, khớp `mong_doi.txt`.
- Đánh giá S1–5 & Lab (`L1=2, L2=2, L3=2, L4=2, L5=N/A`): 0 lỗi MUST/SHOULD.

### 8. `ACB L05` — `sha16`: `4f2e83ffcc0a3e37`
- Tệp: `lessons/acb/L05_cong_chi_luong_va_sao_ke_divide_conquer.yaml`, `labs/ACB/L05/{de.md, mong_doi.txt, loi_giai.py}`
- Thời lượng / từ: `17:17` (`1036,733s`), `pause = 285s` (`15 + 270`), không pause `12,53 phút` / `2 296 từ`.
- `built_at` `2026-11-23T19:40:44Z` >= `mtime` `2026-11-23T17:12:51Z`. ASR: 128 câu, chưa xem xét: 0 (`checked_at: 2026-11-22T05:15:31Z`).
- Khung hình đã xem: `00018.png`, `00024.png` (SVG 4 tầng), `00035.png`, `00038.png` (SVG vòng chờ Deadlock), `00110.png`, `00124.png` — đều rõ đẹp.
- Kiểm chứng logic & số liệu: lịch gốc `(A,7),(B,3),(A,3),(B,7)` -> A giữ 7, B giữ 3, A chờ B, B chờ A -> `co`; lịch đã sắp `(A,3),(B,3),(A,7),(B,7)` -> `khong`; `dau doan: [20, 24, 18, 21, 19] cuoi: 24`, `so khoi: 5` khớp `mong_doi.txt`. Chạy `loi_giai.py`: `CHƯA KIỂM (sandbox chặn python/bash)`.
- Đánh giá S1–5 & Lab (`L1=2, L2=2, L3=2, L4=CHƯA KIỂM, L5=N/A`): 0 lỗi MUST/SHOULD.

### 9. `FND L09` — `sha16`: `2e5acf1f68b62b40`
- Tệp: `lessons/fnd/L09_git_toi_thieu.yaml`, `labs/FND/L09/{de.md, mong_doi.txt, loi_giai.sh}`
- Thời lượng / từ: `17:47` (`1067,067s`), `pause = 300s` (`60 + 240`), không pause `12,78 phút` / `2 230 từ`.
- `built_at` `2026-11-24T02:57:28Z` >= `mtime` `2026-11-24T02:41:18Z`. ASR: 150 câu, chưa xem xét: 0 (`checked_at: 2026-11-22T07:17:33Z`).
- Khung hình đã xem: `00030.png`, `00037.png` (2 SVG 3 vùng & nhánh Git rõ), `00130.png`, `00142.png`.
- Kiểm chứng lệnh: `loi_giai.sh` dùng `git init -q -b main repo`, `user.name`/`user.email`, 3 lần chốt (`tao kho`, `them non`, `sua so luong ao`), `git log --format=%s` (mới nhất trước), `git branch --show-current` (`main`), `git rev-list --count HEAD` (`3`) khớp `mong_doi.txt`. Chạy `loi_giai.sh`: `CHƯA KIỂM (sandbox chặn bash)`.
- Đánh giá S1–5 & Lab (`L1=2, L2=2, L3=2, L4=CHƯA KIỂM, L5=N/A`): 0 lỗi MUST/SHOULD.

### 10. `DMS L17` — `sha16`: `035c50447e6c4178`
- Tệp: `lessons/dms/L17_cay.yaml` (sinh từ `audit/dms/src/L17_cay.tpl.yaml`), `labs/DMS/L17/{de.md, mong_doi.txt, loi_giai.py}`
- Thời lượng / từ: `17:15` (`1035,1s`), `pause = 300s` (`30 + 270`), không pause `12,25 phút` / `2 213 từ`.
- **Trạng thái build**: `built_at` (`2026-11-24T00:51:28Z`) và `out/DMS/L17/L17.mp4` (`2026-11-24T00:51:28Z`) **CŨ HƠN** `YAML mtime` (`2026-11-24T02:46:00Z`). ASR: 123 câu, chưa xem xét: 0 (`checked_at: 2026-11-24T02:59:19Z`).
- Khung hình đã xem: `00025.png`, `00040.png` (SVG 3 cây 3 đỉnh rõ), `00095.png`, `00112.png`.
- Kiểm chứng số liệu: `H1` (đường thẳng 6 đỉnh, 5 cạnh: liên thông 1, chu trình 0, cây 1, lá 2); `H2` (tam giác + đoạn 3 đỉnh, 5 cạnh: liên thông 0, chu trình 1, cây 0); `H3` (sao 6 đỉnh, 5 cạnh: cây 1, lá 5); `H4` (vòng 6 đỉnh, 6 cạnh: chu trình 1, cây 0); `8^6 = 262144` khớp `mong_doi.txt`. Chạy `loi_giai.py`: `CHƯA KIỂM (sandbox chặn python/bash)`.
- Đánh giá S1–5 & Lab (`L1=1, L2=2, L3=2, L4=CHƯA KIỂM, L5=N/A`):
  - **MUST 1 (Blocker build)**: `built_at` (`00:51:28Z`) cũ hơn `mtime` YAML (`02:46:00Z`). Cần rebuild (lưu ý `DMS L17` dùng `.tpl.yaml`).
  - **SHOULD 1 (`L1 = 1`)**: `practice` step 1 không hiện danh sách cạnh `DO_THI` của 4 đồ thị `H1..H4` trên màn hình (chỉ dẫn sang `de.md`).
