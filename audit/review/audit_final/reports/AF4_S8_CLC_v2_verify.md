# Báo cáo kiểm định độc lập WP-AF4-5 Stage 8 — Khóa CLC (`L00–L12`, 13/13 bài) — v2

**Phán quyết tổng thể:** **`NO-GO`**

## 1. Tóm tắt kiểm tra tự động
- `tools/lv.py curriculum curriculum/clc.yaml`: **PASS** (`13 bài, 0 lỗi`)
- `audit/clc/verify_clc.py`: **13/13 PASS**
- `tools/lv.py lint` (`L00–L12`): **13/13 PASS** (`0 FAIL, 0 WARN`)
- `audit/review/screen_code.py check --course CLC`: **15 khối PASS**
- `loi_giai.py == mong_doi.txt`: **13/13 PASS**
- Chính tả / lặp ngoặc / nguồn `L12` / `"càng "`: sạch
- `out/CLC/L00–L12` `spec_sha256` / PNG: **13/13 STALE** (`layout_CLC.tsv` chờ quét lại)

## 2. Danh sách MUST fix

1. **Rebuild MP4/PNG/ASR `13/13` + `layout_scan.py CLC`** (hiện `L10/00018.png`, `L12/00124.png` và `recap` ở video vẫn mang bản cũ).
2. **Thời lượng MP4 thực tế `< 9.0` phút ở `12/13` bài (`L00–L11`, `6.56–8.46p`)**: bổ sung nội dung giảng giải thuật ngữ P1, đọc `Hai mức quy mô`, mở rộng ví dụ/tự kiểm để đạt `>= 9.0p` thực tế (`>= 540s`).
3. **`covers:` sai cảnh dạy thật (`7/13` bài)**:
   - `L00` obj2→`sym`; `L01` obj1→`sym`; `L02` obj3→`pitfalls/example`; `L03` obj2→`pitfalls`; `L04` obj1→`sym/intuition`; `L06` obj2→`pitfalls/sym/intuition`; `L12` obj3→`quiz`.
4. **`[P8]` Lộ đáp án ở `de.md` (`13/13`) & `practice#0` (`10/13`: `L01, L02, L04..L10, L12`) + thiếu tự đủ (`L01, L03, L04, L05, L08..L12`)**:
   - Bỏ các dòng giá trị đáp án khỏi `de.md` (`13/13`) và bỏ con số kết quả khỏi ô `Kiểm chứng` của `practice#0`.
   - `L03/de.md:1,3`: bổ sung đầy đủ input `p1`, `p2` & 3 lệnh gọi + bỏ spoiler `(Deny > Allow > mặc định Deny)`.
   - Bổ sung quy ước làm tròn & công thức: `L01` (`525 600` phút, `.4f/.6f/.1f`), `L04, L05, L08, L10`, `L09` (`1 KB = 1000 B`, bỏ `320 000 B`), `L11` (`1 - (1 - a)^n`, `spof_eliminated`), `L12` (`525 600 * (1 - 0.9999)`, bỏ `257 phút / 52.56`).
5. **`[P1]` Thuật ngữ tiếng Anh & token Python (`practice` chưa giảng ở `12/13` bài)**:
   - Bổ sung bảng đọc mã Python qua `ast_p1.py` (kèm `ipaddress` L02, `eval_iam` L03...).
   - `L00`: thống nhất mô hình 7 tầng (hoặc giải thích gọn cách gộp 4 lớp).
   - Thuật ngữ chưa giảng ở thân bài (`L01–L11`): `AZ` (`L01`), `VPC, IP, subnet, cloud, ipaddress` (`L02`), `IAM, Allow/Deny` (`L03`), `Reserved/On-Demand, USD` (`L05`), `serverless, RAM` (`L06`), `snapshot, WAL` (`L07`), `Egress, CDN, cache, USD` (`L08`), `KMS, KB` (`L09`), `Active-Active, req/s, N+1` (`L10`), `managed DB, stateless, spof` (`L11`).

## 3. SHOULD fix
- Đổi bộ số `12/13` lab (`L00–L10, L12`) khỏi lặp ví dụ bài giảng & bỏ gợi ý đáp số trung gian (`L02, L04, L06..08, L14`).
- Thêm `say:` đọc phần `Hai mức quy mô` (`recap.1` `L00–L12` & `pitfalls` `L00, L03, L07, L11`).
- SVG `L11:81`: dời `"co giãn theo nhóm"` từ `y="160"` lên `y="108"`.
- Sửa `"vs"` → `"so với"` (`L00, L05`), `"->"` → `"sang"` (`L11`), đồng bộ `audit/clc/af2/upgrade_clc.py`.
