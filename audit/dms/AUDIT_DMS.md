# Khoá DMS · Toán rời rạc: báo cáo kiểm chứng (2026-10-28)

**Nhãn bằng chứng:**
- **OBSERVED:** đã chạy hoặc xem trong phiên này.
- **CITED:** có nguồn tra được.
- **INFERRED:** suy luận.

**Trạng thái:** DONE cho phần dựng và kiểm bằng máy; PARTIAL cho phát âm. Mục 4 nêu những gì chưa kiểm được.

## 1. Sản phẩm (OBSERVED)

**Video:** 20 bài L00–L19, tổng 115,8 phút. Mỗi bài nằm ở `out/DMS/<id>/` gồm `<id>.mp4`, `.srt`, `chapters.txt`, `asr_report.md`.

**Đặc tả:**
- Bài nằm ở `lessons/dms/`.
- 4 bài có hình sinh bằng máy (L08, L16, L17, L18) được soạn ở mẫu `audit/dms/src/*.tpl.yaml`.
- Hình sinh từ dữ liệu, không vẽ tay:
  - `hasse_svg.py`: cạnh là quan hệ phủ, máy tính ra.
  - `multigraph_svg.py`: bậc và đường đi Euler tính bằng thuật toán Hierholzer.
  - `tree_svg.py`.
  - `plain_svg.py`: màu tô do thuật toán tham lam tính.

**Tách biệt khoá cũ:** ký hiệu riêng ở `tools/registry/symbols.DMS.yaml`, luật đọc riêng ở `lexicon_vi.DMS.yaml`. CS115 và CS112 không dùng hai tệp này.

## 2. Kiểm chứng (OBSERVED, 2026-10-27T20:01Z)

| Mục | Kết quả |
|---|---|
| lint | 20/20 bài: 0 FAIL, 0 WARN. Mọi con số trên màn hình đều có `checks` (biểu thức Python) |
| verify | 20/20 PASS |
| bố cục (`audit/layout_scan.py DMS`) | 1143 khung, 0 lỗi |
| lộ trình | 20/20 có đặc tả, 0 lỗi (gồm kiểm `assumes` theo bài tiên quyết) |
| máy nghe | 0 câu gắn cờ chưa xem xét. Mỗi câu có lý do theo nhóm đã dò, hoặc lý do viết tay (`audit/dms/asr_review_dms.py`) |
| tests | 0 FAIL, gồm ca thử cho hai luật mới E33, E34 |

**Lỗi máy bắt được trong lúc viết** (không lọt vào video):
- Số cặp “là ước của” trên {1, 2, 3, 4, 6, 12} là 12, không phải 11.
- `3 * (-2) % 7` viết sai thành phép kiểm.
- Một phép kiểm Python bị lỗi do nối chuỗi so sánh với `is`.
- Ba bước bị tràn khung, đã tách sang khung mới.
- Bảy chỗ dùng ký hiệu trước khi giải thích.

## 3. Phát âm (probe: `audit/dms/probes/`)

| Tên | Kết quả | Dùng trong lời đọc |
|---|---|---|
| De Morgan | “Đơ Mo-gần” 8/8, đối chứng âm 0/8 | có |
| Fermat | “Phéc-ma” 8/8 | có |
| Euler | “Ơ-le” 8/8 | có |
| Cayley | “Kê-li” 8/8 | có |
| Pascal | thô 7/8 | có (một câu NOT_VERIFIED) |
| chữ “p” | thô 7/8 | có |
| Bézout, Königsberg, Hasse, RSA, Hamilton, Carmichael | ≤ 6/8 | **không**, chỉ hiện trên màn hình |
| domino | 8/8 nhưng đối chứng âm cũng 4/8 | **không** |

## 4. Còn NOT_VERIFIED

- **Câu cần tai người nghe:** 8 câu có ghi chú NOT_VERIFIED trong `asr_reviewed`, thuộc 5 bài L03, L05, L10, L12, L16. Đều là nhầm thanh hỏi/ngã (chẵn/chẳng), r/đ (rỗng/động), hoặc “Pascal” ở một câu.
- **Hiệu quả sư phạm** với người học thật.
- **Nguồn:** các năm (1736, 1889, 1976, 1978) và tên tác giả viết theo kiến thức chuẩn, chưa tra lại nguồn gốc trong phiên này.

## 5. Thay đổi công cụ trong đợt này

| Thay đổi | Lý do (lỗi thật) |
|---|---|
| E33: tên lệnh LaTeX thiếu `\` (`$equiv$`) | sed nuốt dấu `\` ở L01 |
| E34: khoá step lạ | dòng thừa `set:` ở L02 |
| `load_yaml` báo lỗi khi gặp khoá trùng | 30 tệp CS112 có hai `asr_reviewed` (đã dọn, verify vẫn 29/29) |
| `player.css`: dòng mã có đệm ngang | viền nhấn đè chữ cái đầu dòng mã |
| phép đo `viền-đè-chữ` | đối chứng dương: CSS cũ thì bắt đúng L02 #28–29 và 34 khung ở 13 bài CS112 |
| cột được nhấn: viền cách 10px | viền cách chữ 4px trông sát |

Các bài bị ảnh hưởng đã được dựng lại, tất cả verify PASS:
- CS112: 16 bài.
- CS115: 2 bài (L13, L14).
- DMS: 8 bài (L00, L02–L08).
