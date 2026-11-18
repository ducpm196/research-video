# fix13 CS115 L12–L21, L44–L46 (vòng r13, chỉ đổi chữ trên màn hình) — 2026-11-18

Nguyên tắc: chỉ đổi `show` (và `focus` ở mục 8). **Không câu `say` nào đổi** (so từng step với bản trước fix12: 13/13 giống hệt; `asr_reviewed` 0 mục mất). Không chạy build/tts/asr/audit_all/git/docker; có `tools/lv.py render`.

## Đã làm
1. L15 eigen.1, spd.0: ngoặc "phương sai theo một hướng" đổi thành "= độ trải của dữ liệu khi chỉ nhìn dọc hướng đó: thả mỗi điểm vuông góc xuống đường theo hướng ấy rồi tính phương sai các chân thả" (spd.0 dùng bản ngắn "tính trên các chân thả vuông góc"); không còn dùng "hình chiếu".
2. L16 proof.1: "Hai vector riêng trực chuẩn vuông góc và dài 1, nên như hai trục toạ độ mới: mọi u đi a bước theo v₁ rồi b bước theo v₂, tức u = a·v₁ + b·v₂; vì u dài 1 nên a² + b² = 1" (bỏ chữ "cơ sở").
3. L17 practice.0: thêm hàng `Fraction(1, 4)` (phân số 1/4, in ra 1/4). Ở L15, L16, L17, L19, L46 ô "đọc là" của hàng danh sách/ma trận thêm "dòng in ra: print ra Fraction(5, 2); muốn hiện 5/2 dùng str(x) rồi nối bằng ", ".join(…)" (gộp vào hàng sẵn có để giữ ≤ 4 hàng/step; L15 và L17 thu cỡ chữ bảng 0,82em và nhãn cột "mã gõ / dòng in ra" để khỏi tràn).
4. L12 practice.0: ô mã `(f(x + h) - f(x - h)) / (2 * h)` `white-space:nowrap`.
5. L20 gradient.0: dòng "Nhân lại: …" xuống dòng riêng và bọc nowrap, không gãy trong ngoặc phân số.
6. L15 practice "Nếu kẹt": thêm `clear: true`.
7. L12 ví dụ: "t: 1.0, rồi 0.2, rồi ≈ 0.04 (làm tròn)" và đạo hàm hai phía "cho ≈ 2 (làm tròn)".
8. Dòng mồ côi: L12 hook (khung 0) "khác&nbsp;0." và ghi chú "399 chữ số&nbsp;0."; L21 "Nếu kẹt" "đoán&nbsp;0.".
9. (bổ sung của điều phối) Ghi chú Git Bash/kho luôn sáng, cả 13 bài: ở bước "Đọc trước khi làm", focus của mọi câu đọc hàng bảng đổi từ "2.k" thành [1, "2.k"] (giữ đoạn mở sáng, có nội dung "Git Bash là cửa sổ gõ lệnh…"); chân trang chấm bài (có đoạn "Kho = …") đổi màu chữ #374151 (đậm hơn xám nhạt của `.note`), cỡ 0,8em.

## Cổng (2026-11-18)
- `lint` 13/13: 0 FAIL, 0 WARN. `verify_cs115_af2`: 184 PASS · 0 FAIL. `tests/test_e52.py`: 0 FAIL. `screen_code check --course CS115`: PASS 59 · FAIL/STALE/MISSING/ORPHAN/WARN đều 0.
- `render` cả 13 bài: lượt đầu sau mục 8 TRÀN ở L15, L17, L46 (hàng "dòng in ra" quá dài); đã rút chữ, thu cỡ chữ, đổi nhãn cột; lượt cuối **0 vấn đề ở 13/13**. Khung đã xem: L15 00091 (trước khi thu cỡ), L17 00092, L12 00000.
- Không đổi khối mã trên màn hình, không đổi lab → `lab_gate` không chạy lại (kết quả gần nhất 25 PASS · 0 FAIL).

## Bài đổi (để requeue)
Cả 13 bài L12–L21, L44, L45, L46 (mục 9 chạm tất cả). Không bài nào đổi `say`; không bài nào chưa kiểm render.
