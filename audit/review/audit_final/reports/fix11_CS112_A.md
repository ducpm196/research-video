# fix11 CS112 L00–L14 (chữ trên màn hình, không đổi say) — 2026-11-17

- Cảnh practice (bước "kết quả mong đợi") của cả 15 bài: đầu ghi chú thêm đúng chữ của L15: "Git Bash là cửa sổ gõ lệnh trên Windows (đi kèm Git for Windows): vào thư mục bài làm, bấm chuột phải vào chỗ trống, chọn Open Git Bash here." rồi giữ câu cũ "Chấm bằng Git Bash: …". Chỉ đổi `show`; mẫu `.tpl.yaml` sửa trước rồi `regen_a.py gen` cho L05, L06, L07, L14; 11 bài còn lại sửa YAML.
- L12 scale (bảng 3 hàng cuối): ô ví dụ `[1, 2] + [] + [7]` có `white-space:nowrap`, không gãy giữa danh sách.
- Không đổi `say`: so băm chuỗi `lv.sentences` toàn bài trước/sau cho 15 bài: "không bài nào khác". Lời đọc vẫn ≤ 2300 như fix10.
- "tiêu đề cột 'đọc trước: việc'" chưa áp: đó là tiêu đề bảng riêng của L15; bài L00–L14 không có bảng đó (chân trang Git Bash là ghi chú một dòng), nên không đổi.
- Cổng: lint 15/15 bài 0 FAIL 0 WARN; curriculum cs112 30 bài 0 lỗi; verify_cs112 38 PASS · 0 FAIL, verify_cs112_a 30 PASS · 0 FAIL; screen_code CS112 PASS 144, FAIL/STALE/MISSING/ORPHAN 0.
- Render không chạy (đã bị từ chối quyền trước đó, không đi vòng); ghi chú dài hơn một câu nhưng cùng dạng với L15–L29 đã dựng. Cần điều phối render khi dựng.
