# Báo cáo kiểm định độc lập WP-AF4-5 Stage 8 — Khóa CLD (`L00–L15`, 16/16 bài)

**Phán quyết tổng thể: `NO-GO`**

## 1. Tóm tắt kiểm tra tự động
- `lv.py curriculum curriculum/cld.yaml`: **16/16, 0 lỗi**
- `lv.py lint lessons/cld/L*.yaml`: **16/16 PASS (`0 FAIL, 0 WARN`)**
- `audit/cld/verify_cld.py`: **20/20 PASS** *(phần socket L00a bị sandbox chặn)*
- `loi_giai.py == mong_doi.txt`: **16/16 PASS**
- `srt == say` & giọng đọc & ASR cũ: **16/16 khớp**; **"càng "**, lặp ngoặc, nguồn `L15`: sạch
- `spec_sha256` & PNG: **16/16 STALE**; `audit/layout_CLD.tsv`: trống

## 2. Danh sách MUST fix
1. **Rebuild MP4/ASR `16/16` + chạy `layout_scan.py CLD`**.
2. **`L10` SVG đè chữ (`lessons/cld/L10_hang_doi.yaml:185`, `00039.png`)**: `"công suất"` (`x=860 y=36 end`) bị đường cong xanh lam cắt ngang -> dời sang phải (`x=868 start`) hoặc nâng cao tách khỏi đường cong.
3. **`covers:` trỏ sai cảnh dạy thật (`L03, L04, L08, L09` + chỉnh `L00, L02, L10, L12, L15`)**:
   - `L03` obj1→`sym`; `L04` obj2→`example`, obj3→`sym`; `L08` obj2→`sym`; `L09` obj1→`sym/prereq`, obj2→`sym/example`.
4. **`[P8]` Lỗi tự đủ & sai diễn đạt `de.md` (`L01, L05, L09`)**:
   - `L01/de.md:3`: sửa phủ định kép `"không tốn 0 MB"` → `"tốn 0 MB nhân riêng"` / `"không tốn nhân riêng"`.
   - `L05/de.md:3-6`: bổ sung đầu vào dư `['p1','p2','p3','p4']` và định nghĩa `idempotent_noop=1`.
   - `L09/de.md:3-6`: định nghĩa `p2c_balanced=1` (`m2 < 220`), `randrange(100)`, tie-break `<=`.
5. **Thời lượng MP4 thực tế `< 9.0` phút (`12/16` bài `L00, L02–L09, L12–L14`, `7.93–8.52p`)**: bổ sung nội dung giảng để đạt `>= 9.0p` thực tế (`>= 540s`).

## 3. SHOULD fix
- `[P8]` đổi bộ số 12/16 lab (`L03–L12, L15` + `L02, L13, L14`) & bỏ lộ kết quả trung gian (`L02, L04, L06, L07, L08, L14`); chỉnh `L02, L04, L07, L10` `de.md`; đồng bộ `audit/cld/af2/upgrade_cld.py`.
- `[P1]` mở nghĩa `P2C`, `seed` (`L09`), `desired/running` (`L05`), `max_in_flight` (`L08`), `-&gt;`→`→` (`L11`), `"vs"`→`"so với"` (`L00, L01, L09, L15`).
- `P9` thân bài `L13` bổ sung so sánh `1 máy` vs `100 dịch vụ`; tinh chỉnh `covers` phụ trợ (`L00, L02, L10, L12, L15`).
