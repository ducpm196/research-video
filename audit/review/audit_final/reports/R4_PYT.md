# R4 PYT (vòng 4b, đọc độc lập, P1 chặt gồm cả loại B): 14/14 bài — ghi lại bởi người điều phối từ tin nhắn của reader (a713154842367d6e5)

(Ghi chú: tệp này ghi đè báo cáo vòng 4a cùng tên trước đó — số liệu vòng 4a: P1=2 8/14 chuẩn chặt cũ.)

## 1. Tóm tắt
MUST 0 (14/14). P1=2: 0/14 (P1=1: L03, L07, L08, L09, L11; P1=0: 9 bài). Nếu chỉ tính mục "chắc": P1=2 ở L04, L07, L09, L11; P1=1 ở các bài còn lại trừ L05 (P1=0). P8=2 14/14; P9=2 14/14. spec khớp 14/14. SRT khớp 14/14 (SRT sinh từ say, không độc lập với ASR). Lab ĐÚNG 14/14 (L08 `pip install` cần mạng: chỉ đọc). ~320 phép so mã tự động + ~170 dòng so tay: khớp, trừ chỗ lệch giải thích được. SHOULD 7. Mất gốc: ĐỦ 5, GẦN 9, CHƯA 0.
Loại mục: A = chưa giảng ở đâu trong khoá; B = giảng ở bài trước, bài này không nhắc lại một dòng; M = giảng muộn hơn trong cùng bài/cảnh sau lần xuất hiện đầu.
Mẫu lặp: (1) cấu trúc hiện ở cảnh này, giảng ở cảnh kế (L00 f-string và `__name__`, L05 lệnh shell, L10 `.loc`) → chuyển lời giảng lên NGAY lần xuất hiện đầu. (2) Cấu trúc chỉ xuất hiện trong gợi ý phần tự làm mà chưa dạy: `+=`, chuỗi ba nháy (L13), `from…import` (L05, L06), biểu thức điều kiện (L12). (3) "ngoại suy" dùng ở L02–L13 (trừ L07, L08, L09) chỉ có `assumes: pyt_ngoai_suy`, không nhắc định nghĩa → thêm một dòng nhắc ở mỗi bài.

## 2. SHOULD
| Bài | Cảnh | Trích | Lý do | Đề xuất | Tin cậy |
|---|---|---|---|---|---|
| L02 | scale#3 | "Đây là cận trên: hàm làm việc thật thì khoản gọi nhỏ hơn nhiều" (sau "chậm hơn ≈ 1,7 lần ở 10⁷") | cùng bảng: 10⁶ gọi hàm 240 ms vs 100 ms = 2,4 lần > 1,7 → "1,7" không là cận trên; đo lại 3.11: 2,1 lần ở 10⁶, 1,75 ở 10⁷ | "cỡ 1,7 đến 2,4 lần" | CONFIRMED |
| L04 | scale#2 | "4 000 ký tự ≈ 30 ms, 8 000 ký tự ≈ 250 ms, chuỗi dài gấp đôi mà thời gian gấp nhiều lần" | đo `re.search(r"a+b","a"*(n-1)+"c")` 3.11: 11,6 ms và 46,5 ms, tỉ số 4,0 (bậc hai), không 8,3 | ghi tỉ số đo được / "cỡ gấp bốn khi dài gấp đôi" | PLAUSIBLE (máy khác) |
| L06 | formula#3, scale#2 | "Đối tượng thường là một từ điển thuộc tính kèm liên kết tới lớp" | mô hình đơn giản hoá; từ CPython 3.11 thuộc tính lưu nội tuyến, từ điển dựng muộn; số đo 19/15/16 MB khớp | thêm "(về mặt khái niệm; từ 3.11 máy dựng từ điển muộn)" | PLAUSIBLE |
| L07 | sym#2 | "ghi theo mức: debug < info < warning < error"; "bốn mức" | logging có 5 mức chuẩn (CRITICAL) | thêm critical hoặc "các mức thường dùng" | CONFIRMED |
| L08 | sym#2 hàng `2>&1` | "để \| lọc được cả hai" | ký tự `\|` thừa giữa câu (khung 00018) | bỏ hoặc đặt trong code | CONFIRMED |
| L12 | intuition#1, example#3, quiz#2–3 | "Mỗi ngưỡng đổi nhánh: lỗi hay gặp là dấu < / <= bị đổi nhầm"; "Ba ca ở mỗi ngưỡng … bắt gần hết lỗi lệch một và lỗi đổi nhầm dấu so sánh" | chỉ ngưỡng 50 000 là điểm hàm nhảy; đột biến thử 0–13 triệu: đổi `phi < 1100` thành `<=` và `phi > 11000` thành `>=` cho kết quả y hệt ở mọi giá trị, không ca nào bắt; nhánh trần thật sự đổi ở 11 001 000 | nói rõ ca biên chỉ bắt lỗi dấu ở chỗ hàm nhảy (50 000); 1 100 000 và 11 000 000 chỉ kiểm giá trị chặn | CONFIRMED (brute-force) |
| L13 | practice#3 khung 00124 | `for hang in csv.DictReader(f): try: tien = int(hang["so_tien"]) except ValueError: bo_qua += 1; continue` | khối mã thụt lề bị dán thành 1 dòng văn xuôi | hiển thị bằng div.code nhiều dòng | CONFIRMED |
Khác: L11 P3=1 (thang lôgarit và hexbin chỉ có mã/chữ, không có hình đường thẳng hay ô lục giác); L08 P3=1 (`\|` thừa); L12/L13 video dài 33,8/34,0 phút (gồm 20 phút dừng làm bài).

## 3. Mục chưa giảng (P1 chặt) — theo bài
Loại; độ chắc (chắc/yếu = suy ra được phần nào từ ngữ cảnh); bảng cách đọc phủ?
- L00 (4): example#1 `print(f"Tong: {so_du + round(lai):,}")` M chắc, không; practice#1 `type(lai).__name__` M chắc; formula#5/scale#3 "hệ nhị phân/hệ hai" A yếu; scale#1/#3 số mũ âm 10⁻¹⁶, ×10⁶, ×10¹⁵ A yếu.
- L01 (3): formula#4 `so_du = so_du + so_du * 5 // 1000` B chắc (`//` ở L00); sym#4 `list(range(3))` A yếu (bảng có `range`, không `list`); scale#2 "≈ 93 µs" A yếu.
- L02 (3): example#3 `t0 = time.perf_counter()` A chắc (dấu chấm mô-đun); `for i in range(n): y = tang(y)` B yếu; scale#3 "ngoại suy: 10⁹ ≈ 3,4 phút" B yếu.
- L03 (2): scale#2 "≈ 40 MB", "bốn mươi triệu byte" A chắc (byte giảng ở L04); scale#1 "ngoại suy ×100 000" B yếu.
- L04 (3): example#2 `if m is None:` B yếu; `continue` B yếu; scale#1 "31 ký tự (ngoại suy)" B yếu.
- L05 (5): `from pathlib import Path` A chắc (from…import giảng ở L08); formula#1 `f.write("tiền mặt\n")`, `split("\n")` A chắc (`\n`); pitfalls#3 `PYTHONIOENCODING=cp1252 python -c … 2> loi.txt; echo $?`, `tail -n 1 loi.txt | cut -d: -f1` M chắc (giải ở pitfalls#4; tiền tố biến môi trường và `;` không giải); formula#6 `json.dumps/loads` A yếu; hook#1/scale#1 "(ngoại suy)" B yếu.
- L06 (3): example#3 `from dataclasses import dataclass` A chắc; example#10 `[A("A" + str(i), i) for i in range(100000)]` A/B yếu; "(ngoại suy)" B yếu.
- L07 (1): formula#1 `print(repr(s), doc_tien(s))` B yếu (repr ở L05).
- L08 (2): example#1 `source .venv/Scripts/activate && python -c "…"` A chắc (`&&`); formula#5 `python -c "import sys; print(sys.prefix != sys.base_prefix)"` A yếu (`;`).
- L09 (2): example#3 `np.array([[1., 10.], …])` A yếu (`1.`); pitfalls#2 "số nguyên 4 byte (32 bit, một bit dành cho dấu)" A yếu (bit).
- L10 (4): formula#4 `gd.loc[gd["loai"] == "nap", "so_tien"].sum()` M chắc; formula#9 `gd.dropna(subset=["so_tien"])` A yếu; pitfalls#3 `gd["so_tien"] == float("nan")` A yếu; "(ngoại suy)" B yếu.
- L11 (2): formula#1 `[int(p.get_height()) for p in ax.patches]` B yếu; scale#1 "ngoại suy tuyến tính" B yếu.
- L12 (4): pitfalls#4 `mong_doi = 0 if tien <= 50000 else max(tien // 1000, 1100)` A chắc; "theo đặc tả (không theo mã)" A yếu (chưa định nghĩa "đặc tả"); hook#1 khung diff `- if tien < 50000:` / `+ if tien <= 50000:` A yếu; "ngoại suy tuyến tính" B yếu.
- L13 (4): practice#3 `except ValueError: bo_qua += 1; continue` A chắc (`+=`); "chuỗi mã ba nháy thường, ký tự xuống dòng viết `\\n`" (bắt buộc `"""…"""` để viết MODULE, TESTS) A chắc; `;` nối hai câu lệnh A yếu; "(ngoại suy)" B yếu. de.md hàm `cham` dùng `importlib`, `exec_module`, `subprocess.run`, bảo "chép nguyên".

## 4. Người học kẹt ở đâu
L00 nhẹ (example#1 f-string, giải ở example#3); L01 formula#4 `//`; L02 example#3 `time.perf_counter()`; L03 scale#2 "byte"; L04 không kẹt; L05 formula#1 `\n` và pitfalls#3 dòng shell dài; L06 example#3 `from … import`; L07 không kẹt; L08 example#1 `&&`; L09 không kẹt chặn (pitfalls#2 không cho thấy vì sao ra -294967296); L10 formula#4 `.loc`; L11 không kẹt chặn (formula#6 Simpson vòng lồng, từ điển chứa bộ); L12 pitfalls#4 biểu thức điều kiện một dòng; L13 practice#1–3: MODULE/TESTS bằng chuỗi ba nháy, `bo_qua += 1`, hàm `cham` trong de.md.
