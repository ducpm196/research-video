# Báo cáo kiểm định độc lập WP-AF4-3 Stage 8 — Khóa CLD (`L00–L15`, 16/16 bài)

- **Phạm vi**: Đọc toàn bộ `curriculum/cld.yaml`, `audit/cld/sources_L15.md`, `audit/cld/verify_cld.py`, 16 tệp `lessons/cld/L*.yaml`, 16 bộ lab `labs/CLD/L*/{de.md, loi_giai.py, mong_doi.txt}`, `out/CLD/L*/{build_report.json, asr_report.md, L*.srt}`, và kiểm tra trực quan 51 khung hình PNG (`frames/*.png`). Không sửa bất kỳ tệp nào.
- **Kết quả cổng tự động**:
  - `lv.py lint` (16/16): `0 FAIL, 0 WARN`.
  - `lv.py curriculum curriculum/cld.yaml`: `16/16 có đặc tả, 0 lỗi`.
  - `spec_sha256 == lv.spec_digest`: **16/16 khớp**; `voices`: **16/16 một giọng**.
  - `L*.srt == say`: **16/16 khớp**; `asr_report.md`: **16/16** `thiếu audio: 0, chưa xem xét: 0`.
  - `checks` YAML: **16/16 PASS**; `loi_giai.py == mong_doi.txt`: **16/16 PASS**.

## Tổng hợp tỷ lệ & Kết luận: **`NO-GO`**

| Chỉ số | Bao gồm `practice#0` & `de.md` | Chỉ tính thân bài |
|---|---:|---:|
| **P1 = 2** | **4/16 (25,0%)** (`L03, L05, L12, L14`) | **14/16 (87,5%)** |
| **P8 = 2** (thực hành cụ thể + chạy khớp) | **16/16 (100%)** | — |
| **P9 = 2** (≥ 2 mức quy mô trong thân) | **14/16 (87,5%)** (`L05, L14` = 1) | — |
| **`recap` `Hai mức quy mô`** | **0/16 (0%)** | — |
| **`covers:` khớp cảnh dạy thật** | **0/16 (0%)** | — |
| **SVG/bảng sạch** | **15/16 (93,8%)** (`L10` `00039.png` đè chữ `"công suất"`) | — |

Lý do chặn chốt:
1. **16/16 bài** thiếu `<p class="note"><b>Hai mức quy mô:</b> ...` trong `recap`; `L05` và `L14` cần thêm so sánh 2 quy mô trong thân bài.
2. **16/16 bài** `covers:` gán cứng `[(1,example/stage1), (2,check), (3,practice)]`.
3. **12/16 bài** (`L00, L01, L02, L04, L06, L07, L08, L09, L10, L11, L13, L15`) còn thuật ngữ/viết tắt tiếng Anh lạ chưa chú thích tại chỗ trong `practice#0`/`de.md` (`L02` `example#0` giải thích ngắn lệnh `FROM/COPY/RUN/CMD`; `L15` `IP`, `de.md` dùng `điểm giữa` thay `trung vị`).
4. **`L08` `de.md`** chưa định nghĩa `max_in_flight` (`được phép thiếu + được phép dư`).
5. **`L10` `example#4`** (`out/CLD/L10/frames/00039.png`) nhãn `"công suất"` bị đường cong xanh cắt ngang.

*(51 PNG đã xem trực tiếp: `L00–L15` mỗi bài 3–4 khung tiêu biểu gồm `prereq`, `intuition`/SVG, `practice#0`.)*
