# BRIEF_FIXF — sửa các phát hiện của mẫu F (đợt AF2, 2026-11-13)

Nguồn phát hiện: `audit/review/sample_f/REPORT.md` mục 2 (bảng "Sổ phát hiện chuẩn xác": bài, mức, chỗ, vấn đề, hướng sửa, tin cậy) và mục 3 (chỗ người học kẹt). Chuẩn chung: `BRIEF_AF2.md` (đọc mục "Quy trình mỗi bài" và "Bẫy"). Bạn chỉ SỬA các bài được giao; mỗi bài sau khi sửa phải qua cổng và để lại "trạng thái đã sửa, chưa dựng lại" (người điều phối dựng).

## Nguyên tắc
1. **Tự kiểm lại từng phát hiện trên tệp thật trước khi sửa**: mở bài (`lessons/<khoá>/Lxx_*.yaml`, hoặc nguồn sinh), tìm đúng chữ được trích, tính lại bằng Python nếu là con số. Phát hiện CONFIRMED mà bạn kiểm thấy đúng → sửa. PLAUSIBLE → chỉ sửa khi bạn kiểm được bằng nguồn/tính toán; không kiểm được → KHÔNG sửa nội dung, ghi vào báo cáo "chưa kiểm được" (đừng đoán). Phát hiện sai → ghi "phát hiện sai" kèm bằng chứng.
2. **Sửa tối thiểu, đúng chỗ**, giữ số câu `say` khớp `focus` (nếu thêm câu thì thêm mục `focus` tương ứng); không mở rộng phạm vi.
3. **Mục tiêu giáo án hứa điều bài không dạy** (AGT L04, CLC L10, CSA L07, ROB L10, SEC L11, DVO L03, BNX L05…): ưu tiên THÊM nội dung dạy đúng mục tiêu (một step/cảnh ngắn có ví dụ số, hoặc mã chạy được) hơn là xoá mục tiêu; nếu thêm quá nặng thì đổi mục tiêu cho đúng điều bài dạy (ở cả đặc tả lẫn `curriculum/<khoá>.yaml`), và nói rõ trong báo cáo.
4. Mã trên màn hình phải chạy (`audit/review/screen_code.py check --course <khoá>`; sổ ghim sha — đổi một chữ trong khối mã là STALE: cập nhật mục sổ đúng cách theo hướng dẫn đầu `screen_code.py`, không xoá mục để lách).
5. Bài sinh từ mẫu (`audit/<khoá>/src/*.tpl.yaml`, `audit/jva|bnx|bnk|fnd|jv2/src`) → sửa NGUỒN rồi chạy bộ sinh/`fill_all`; bài còn lại sửa YAML bằng Edit. Sau khi sửa: `audit/review/sync_tpl_from_lesson.py <khoá>` phải báo 0 mẫu lệch. Không dùng heredoc bash/python cho chuỗi có `\`; sau khi sửa `grep -c` ký tự 0x08 (và 0x01) trong tệp đã đổi.
6. Cổng cho MỖI bài đã sửa: `tools/lv.py lint` (0 FAIL, 0 WARN), `tools/lv.py render` (0 vấn đề; tràn khung → tách step + `clear: true`), `audit/verify_plan_curricula.py` nếu đổi `curriculum` (không làm FAIL), `audit/review/check_xref.py`, `check_legal.py`, `arith_scan.py <KHOÁ>`. KHÔNG chạy `build`/`tts`/`asr`/`audit_all.py`/`final_gates.sh`/git. Thêm kiểm tra số cho mọi con số mới (`checks`).
7. Cần đoạn nói mới: câu ≥ 4 từ, ≤ 38 từ, số đọc bằng chữ, không `$ \ _ ^ { }`, tên riêng/sản phẩm chỉ dùng nếu đã có luật đọc trong `tools/registry/lexicon_vi.<KHOÁ>.yaml` (không thì chỉ hiện trên màn hình).

## Báo cáo
`audit/review/audit_final/reports/fixf_<A|B>.md`: bảng mỗi phát hiện: bài | đã làm gì (trích chữ trước/sau) | cổng nào PASS | hoặc "chưa kiểm được"/"phát hiện sai" + bằng chứng. Cuối cùng liệt kê danh sách "KHOÁ Lxx" đã đổi để người điều phối đưa vào hàng dựng. Tin nhắn cuối gọn.
