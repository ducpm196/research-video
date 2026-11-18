# fix13 DMS L01–L10 (item-verifier, chỉ đổi `show`) — 2026-11-17

Không đổi câu `say` nào: băm `lv.sentences` của toàn bộ `say` mỗi bài trước/sau trùng nhau (L00–L10 đều SAME), và so với `out/dms/*/asr_report.json` bản dựng gần nhất: 0 câu khác ở cả 11 bài. Không build/tts/asr/render/git/docker (render bị từ chối quyền, không đi vòng).

## Việc đã làm (chỉ chữ trên màn hình)
1. Git Bash: ghi chú chân trang L01–L10 có thêm ĐẦU ghi chú đúng chữ L11 ("Git Bash là cửa sổ gõ lệnh trên Windows … chọn Open Git Bash here."). Cách làm: L01–L10 dùng `patch_cham` của `audit/dms/af2/fix6b.py` (chỉ import `patch_cham`; không import `*` vì fix6b ghi đè `read_steps` bằng câu mở khác).
2. L06 practice hàng `f.values()`: cột "đọc là" nói từ điển viết `{khoá: giá_trị}`, đọc ở bảng ngay sau.
3. L06 quymo: thêm hàng `print(n, 'khoa: toi thieu', …)` vào bảng đợt hai (4 hàng, không đổi chỉ số step), và `**` là lũy thừa trong hàng `% 2 ** 32`.
4. L01 "Nếu kẹt": `break` kèm "(thoát ngay khỏi vòng lặp)" trong hộp gợi ý.
5. L03 contradiction.1: ghi chú "ℚ là tập các phân số a/b với a, b nguyên, b khác 0 (số hữu tỉ); số vô tỉ là số thực không viết được dưới dạng đó".

Sửa nguồn: audit/dms/af2/l01…l10.py (bài sinh lại từ script). Bài đổi: L01–L10 (L00 không đổi).

## Cổng
lint L01–L10: 0 FAIL, 0 WARN (lời đọc không đổi nên ≤ 2300 giữ nguyên). verify_dms: 324 PASS · 0 FAIL. screen_code DMS: 72 khối, PASS 95, FAIL/STALE/MISSING/ORPHAN 0.

## Lưu ý
- L05: lời đọc câu mở "…dùng bảy ký hiệu…" khớp bản dựng nhưng bảng thực có 8 hàng (sau khi thêm hàng `if` ở fix12). Giữ nguyên để không đổi `say`; nếu muốn sửa thành "tám" thì một câu L05 phải tổng hợp lại giọng.
- L01 giữ câu mở "Tiếp theo là các ký hiệu còn lại của chương trình này." (truyền `intro2` tường minh) để khớp bản dựng.
