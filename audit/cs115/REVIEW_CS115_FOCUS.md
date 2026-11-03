# Rà soát CS115 lần 2: focus theo câu và lỗi hình (2026-10-27)

**Yêu cầu.** CS112 đã làm tốt phần chỉ chỗ đang nói. CS115 thì chưa: phải rà soát lại để video trực quan, chính xác và đầy đủ.

**Trạng thái:** DONE với mọi phần máy kiểm được và các khung đã xem bằng mắt. Phần còn NOT_VERIFIED nằm ở mục 5.

## 1. Khoảng trống `focus` (OBSERVED)

Đo bằng `audit/cs115/focus_gap.py`. Một step được tính là cần focus khi nó có ≥ 2 câu nói về khối có ≥ 2 phần, hoặc khi step không có `show` mà vẫn nói tiếp về bảng có nhiều khối.

| | Trước | Sau |
|---|---|---|
| CS115: step cần focus đã có | **213/612** (35 %) | **612/612** |
| CS112, để so sánh | 233/248 (94 %) | không đổi |
| CS115: khung có viền chỉ chỗ | 708/3683 | 1844/3683 |

**Nguyên nhân.** E32 chỉ cảnh báo khi step có **≥ 3 câu và khối ≥ 3 phần**. Vì vậy lint vẫn báo 0 WARN, trong khi 399 step lọt qua:
- step 2 câu trên khối 2 phần (đoạn chữ cộng công thức);
- step không có `show` nhưng nói tiếp về bảng.

**Cách làm.**
1. `focus_dump.py Lxx` in từng phần, kể cả công thức con, dòng bảng và mục danh sách, cùng từng câu được đánh số.
2. Soạn focus tay cho cả 399 step vào `focus_plan/Lxx.yaml`.
3. `focus_apply.py` chèn dòng `focus:` ngay trước `say:`, đọc lại bài và so từng step.
4. Lint E31 kiểm chỉ số. Lúc dựng, render kiểm thêm xem trình duyệt có tìm thấy phần được trỏ không.

## 2. Lỗi tìm thấy khi xem bằng mắt và đã sửa

| Chỗ | Lỗi | Sửa |
|---|---|---|
| L02 khung 163–164, L08, L09 ×2, L13 ×2 | Focus trỏ vào một chữ in đậm giữa câu (“khác nhau”, “vuông góc”, “Bước đầu tiên”…) thay vì công thức hay cả dòng | Trỏ lại vào công thức hoặc cả dòng. `focus_targets.py` liệt kê mọi mục trỏ phần con; còn 9 mục `<span>`, đều là ô quy trình hoặc cả dòng giải thích, đúng ý |
| L20 khung 24, L40 khung 3 | Viền ôm ký hiệu nhỏ (z, k) trong khi câu nói về cả công thức | Trỏ cả dòng |
| L36 khung 25–26 | Viền ôm 4 dòng bảng cùng lúc, trông như 4 hộp chồng nhau | Trỏ cả bảng |
| L36 khung 21, L43 khung 8 | Câu nói 2 chỗ mà viền chỉ 1 chỗ | Thêm chỗ thứ hai |
| **L11, mọi khung** | Tiêu đề 104 ký tự làm dòng đầu trang xuống 2 dòng | “Bài 11 — Tối ưu lồi & phương pháp Newton, ba cách thay thế khi Hessian quá đắt”; sửa cả curriculum và README |
| L26 khung 0–2 | Nhãn SVG “hướng tốt hơn” bị cắt ở mép phải | `text-anchor="end"`, đặt bên trái đường |
| `out/CS115/L04`–`L08` | Còn `L03.mp4`…`L07.mp4` cũ từ đợt đánh số lại ngày 24/10, mỗi thư mục có 2 video | Chuyển sang `out/_stale_renumber_2026-10-24/`; không xoá |

## 3. Phép kiểm mới

- **`render` FAIL khi dòng đầu trang hoặc tiêu đề phân cảnh xuống 2 dòng** (`player.html` headWrap, `lv.py`).
  - Đối chứng dương: L11 cũ bị bắt.
  - Đối chứng âm: 25 bài CS112 và 43 bài CS115 không bị bắt.
  - Bài đã dựng kiểm được mà không cần dựng lại: `audit/cs115/head_wrap.py <khoá>`.
- **Các script đo:**
  - `focus_gap.py <khoá>`: độ phủ focus;
  - `focus_targets.py <khoá>`: mục trỏ vào chữ thay vì công thức hay dòng;
  - `svg_scan.py <khoá>`: chữ SVG sát mép.

## 4. Kết quả kiểm (OBSERVED)

Xem mục 6.

## 5. NOT_VERIFIED

- **Xem bằng mắt chỉ là lấy mẫu.** Đã xem khoảng 230 khung có focus mới qua ảnh ghép 2×2 thu nhỏ. `focus_frames.py` ưu tiên các mục trỏ phần con hoặc trỏ nhiều chỗ: L00–L15 lấy 8 khung mỗi bài, L16–L43 lấy 4. Trong khoảng 1844 khung có viền, phần lớn chưa được mắt người xem. Duyệt `preview.html` từng bài sẽ chắc hơn.
- **Ý chọn focus là phán đoán của tôi.** Mỗi câu một mục, dựa trên đọc câu và đọc phần trên bảng. Người dạy có thể muốn trỏ khác ở một số câu.
- **Lời đọc không đổi.** TTS lấy từ cache nên ASR không phải chạy lại. Các câu cần người nghe vẫn như báo cáo trước.

## 6. Kiểm cuối
`checked_at=2026-10-27T06:55Z`:

- **CS115:**
  - verify **44/44 PASS**;
  - lint 0 FAIL, 0 WARN ở 44/44 bài;
  - render 0 vấn đề ở mọi bài;
  - dòng đầu trang không xuống dòng ở 44/44 bài;
  - ASR còn 0 câu gắn cờ chưa xem xét;
  - `preview.html` được sinh lại sau video ở cả 44 bài.
- **CS112 không bị ảnh hưởng:** verify 25/25 PASS. Chỉ sửa `player.html` (thêm phép kiểm), không đổi CSS hiển thị.
- **tests:** `tests/test_lint.py` 0 FAIL.
