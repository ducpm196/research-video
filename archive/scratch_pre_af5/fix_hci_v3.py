"""Fix all HCI v3 MUST (5 covers + scene alignment) and SHOULD (ast_p1 rows, L10 p2=1.0), then verify."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(r"D:\research-video")


def patch_file(rel: str, repls: list[tuple[str, str]]) -> None:
    p = ROOT / rel
    txt = p.read_text(encoding="utf-8")
    for old, new in repls:
        if new in txt and old not in txt:
            continue
        assert old in txt and txt.count(old) == 1, f"{rel}: missing/multi {old!r}"
        txt = txt.replace(old, new, 1)
    p.write_text(txt, encoding="utf-8", newline="\n")


# 1. L02: edge + corners in example#2, covers obj1->example/formula, obj2->example, obj3->example
patch_file("lessons/hci/L02_dinh_luat_fitts.yaml", [
    ("<tr><td>nút đặt sát mép màn hình ($W_{\\text{hiệu dụng}}$ rất lớn)</td><td>sát $1$</td><td>giảm mạnh</td><td>sát mức sàn</td><td>không cần hãm phanh chiều dọc</td></tr>",
     "<tr><td>nút đặt sát mép hoặc bốn góc màn hình ($W_{\\text{hiệu dụng}}$ rất lớn)</td><td>sát $1$</td><td>giảm mạnh</td><td>sát mức sàn</td><td>viền màn hình chặn 1–2 chiều, khỏi hãm phanh</td></tr>"),
    ("Đặc biệt nếu đặt thanh thực đơn dính sát mép trên màn hình, viền màn hình chặn con trỏ lại nên người dùng đẩy chuột thẳng lên mép mà không tốn nhịp hãm phanh nào.",
     "Đặt thực đơn sát mép hay bốn góc màn hình giúp viền chặn con trỏ ở một hoặc hai chiều, đẩy thẳng tới đích khỏi cần nhịp hãm phanh."),
    ("covers:\n- objective: 1\n  scene: example\n- objective: 2\n  scene: formula\n- objective: 3\n  scene: check",
     "covers:\n- objective: 1\n  scene: formula\n- objective: 1\n  scene: example\n- objective: 2\n  scene: example\n- objective: 3\n  scene: example"),
])

# 2. L08: explicitly contrast between-subject (36) vs within-subject (12) in example#0, fix covers
patch_file("lessons/hci/L08_thi_nghiem_giao_dien.yaml", [
    ("<p><b>Bước 1 — thông số thật của bài toán.</b> So sánh $k = 3$ giao diện đặt vé $A, B, C$ trên $N = 12$ người (số minh hoạ):</p>",
     "<p><b>Bước 1 — chọn thiết kế và thông số thật.</b> Dùng thiết kế <i>giữa chủ thể</i> cần tới $12 \\times 3 = 36$ người (lệch nhóm), nên ta chọn thiết kế <i>trong chủ thể</i> trên $N = 12$ người cho $k = 3$ giao diện đặt vé $A, B, C$ (số minh hoạ):</p>"),
    ("Bước một, ta xét bài toán so sánh ba giao diện đặt vé A, B, C trên 12 người dùng thử nghiệm.",
     "Bước một, thay vì tuyển 36 người cho thiết kế giữa chủ thể, ta chọn thiết kế trong chủ thể với 12 người lần lượt thử ba giao diện A, B, C."),
    ("Duyệt qua từng phần tử <code>x</code> trong <code>ds</code> để tạo danh sách hoặc tổng mới",
     "Duyệt qua từng phần tử <code>x</code> trong <code>ds</code> để tạo danh sách mới"),
    ("covers:\n- objective: 1\n  scene: example\n- objective: 2\n  scene: pitfalls\n- objective: 3\n  scene: check",
     "covers:\n- objective: 1\n  scene: example\n- objective: 2\n  scene: intuition\n- objective: 2\n  scene: example\n- objective: 3\n  scene: formula"),
])

# 3. L09: explicitly tie upgraded button to curb-cut/temporary disadvantage in example#3, fix covers
patch_file("lessons/hci/L09_truy_cap.yaml", [
    ("<tr><td><b>trình đọc màn hình</b></td><td>không có nhãn chữ</td><td>gắn nhãn ngữ nghĩa: <b>“Tìm kiếm sản phẩm, nút bấm”</b></td></tr></table>",
     "<tr><td><b>trình đọc màn hình</b></td><td>không có nhãn chữ</td><td>gắn nhãn ngữ nghĩa: <b>“Tìm kiếm sản phẩm, nút bấm”</b></td></tr></table>\n      <p class=\"note\"><b>Lợi ích cho mọi người:</b> Vùng chạm lớn, viền tiêu điểm rõ và nhãn chuẩn giúp đồng thời người khuyết tật lẫn người dùng một tay ngoài nắng gắt.</p>"),
    ("Cuối cùng, ta gắn nhãn chữ Tìm kiếm sản phẩm để trình đọc màn hình phát âm rõ ràng ngay khi tiêu điểm chạm tới nút.",
     "Cuối cùng, ta gắn nhãn chữ Tìm kiếm sản phẩm để trình đọc màn hình phát âm rõ, đồng thời giúp cả người dùng một tay ngoài trời nắng gắt."),
    ("covers:\n- objective: 1\n  scene: example\n- objective: 2\n  scene: formula\n- objective: 3\n  scene: concept\n- objective: 4\n  scene: example",
     "covers:\n- objective: 1\n  scene: example\n- objective: 2\n  scene: example\n- objective: 3\n  scene: sym\n- objective: 3\n  scene: example\n- objective: 4\n  scene: example"),
])

# 4. L11: obj4 -> prereq + quiz
patch_file("lessons/hci/L11_tinh_huong_canh_bao.yaml", [
    ("covers:\n- objective: 1\n  scene: formula\n- objective: 2\n  scene: intuition\n- objective: 3\n  scene: example\n- objective: 4\n  scene: pitfalls",
     "covers:\n- objective: 1\n  scene: formula\n- objective: 2\n  scene: intuition\n- objective: 3\n  scene: example\n- objective: 4\n  scene: prereq\n- objective: 4\n  scene: quiz"),
])

# 5. L12: tie scale choice of automated + human testing into stage4 (AF2_DO_SCENES), and add stage2+stage3 to obj2
patch_file("lessons/hci/L12_hanh_trinh_wcag.yaml", [
    ("<p>• <b>Xác thực dễ tiếp cận (3.3.8):</b> nếu đăng nhập đòi một bài kiểm tra nhận thức (như nhớ rồi gõ lại mật khẩu), phải có cách khác hoặc cơ chế hỗ trợ, ví dụ cho dán hay dùng trình quản lý mật khẩu.</p>",
     "<p>• <b>Xác thực dễ tiếp cận (3.3.8):</b> nếu đăng nhập đòi một bài kiểm tra nhận thức (như nhớ rồi gõ lại mật khẩu), phải có cách khác hoặc cơ chế hỗ trợ, ví dụ cho dán hay dùng trình quản lý mật khẩu.</p>\n      <p class=\"note\"><b>Kiểm theo quy mô sản phẩm:</b> Chạy công cụ quét tự động hằng ngày trên toàn bộ trang để bắt lỗi màu và thẻ, đồng thời kiểm người thật bằng bàn phím và trình đọc màn hình trên các luồng chính.</p>"),
    ("    focus:\n    - 1\n    - 2\n    - 3\n    - 4\n    say: Năm 2023, phiên bản 2.2 loại bỏ tiêu chí kiểm tra cú pháp thẻ, vì phần mềm trợ năng nay không còn tự đọc trực tiếp mã trang nữa mà lấy thông tin qua trình duyệt. Chuẩn bổ sung chín tiêu chí mới, nâng tổng số lên 86 tiêu chí hiệu lực. Nổi bật là quy định đích chạm tối thiểu 24 nhân 24 điểm ảnh cho các giao diện thực tế. Đồng thời, nếu đăng nhập đòi nhớ và gõ lại mật khẩu, chuẩn yêu cầu có cơ chế hỗ trợ như cho dán, để bảo vệ người có trí nhớ ngắn hạn hạn chế.",
     "    focus:\n    - 1\n    - 2\n    - 3\n    - 4\n    - 5\n    say: Năm 2023, phiên bản 2.2 loại bỏ tiêu chí kiểm tra cú pháp thẻ, vì phần mềm trợ năng nay không còn tự đọc trực tiếp mã trang nữa mà lấy thông tin qua trình duyệt. Chuẩn bổ sung chín tiêu chí mới, nâng tổng số lên 86 tiêu chí hiệu lực. Nổi bật là quy định đích chạm tối thiểu 24 nhân 24 điểm ảnh cho các giao diện thực tế. Nếu đăng nhập đòi nhớ mật khẩu, chuẩn yêu cầu cho dán hoặc cách thay thế để bảo vệ trí nhớ ngắn hạn. Ở quy mô sản phẩm, ta quét tự động toàn bộ trang và kiểm bằng người thật trên các luồng chính."),
    ("covers:\n- objective: 1\n  scene: stage1\n- objective: 1\n  scene: stage2\n- objective: 1\n  scene: stage3\n- objective: 1\n  scene: stage4\n- objective: 2\n  scene: check\n- objective: 3\n  scene: stage4\n- objective: 3\n  scene: practice",
     "covers:\n- objective: 1\n  scene: stage1\n- objective: 1\n  scene: stage2\n- objective: 1\n  scene: stage3\n- objective: 1\n  scene: stage4\n- objective: 2\n  scene: stage2\n- objective: 2\n  scene: stage3\n- objective: 2\n  scene: check\n- objective: 3\n  scene: stage4"),
])

# 6. SHOULD: L04 & L07 ast_p1 table wording + L10 explicit p2 = 1.0
patch_file("lessons/hci/L04_tai_nhan_thuc.yaml", [
    ("Duyệt qua từng phần tử <code>x</code> trong <code>ds</code> để tạo danh sách hoặc tổng mới",
     "Duyệt qua từng phần tử <code>x</code> trong <code>ds</code> để tạo danh sách mới"),
])
patch_file("lessons/hci/L07_thang_sus.yaml", [
    ("<tr><td><code>[bt for x in ds]</code></td><td>Duyệt qua từng phần tử <code>x</code> trong <code>ds</code> để tạo danh sách hoặc tổng mới</td></tr>",
     "<tr><td><code>(bt for x in ds)</code></td><td>Biểu thức sinh tuần tự từng phần tử <code>x</code> (thường truyền vào <code>sum(...)</code>)</td></tr>"),
])
patch_file("labs/hci/L10/loi_giai.py", [
    ("p1 = 1.0 / 500.0\np_indep = p1 * (1.0 / 50.0)\nprint(f\"indep_leak={p_indep:.2e} shared_leak={p1:.2e}\")",
     "p1 = 1.0 / 500.0\np2 = 1.0\np_indep = p1 * (1.0 / 50.0)\np_shared = p1 * p2\nprint(f\"indep_leak={p_indep:.2e} shared_leak={p_shared:.2e}\")"),
])

PY = str(ROOT / ".venv" / "Scripts" / "python.exe")
for fp in sorted((ROOT / "lessons" / "hci").glob("L*.yaml")):
    r = subprocess.run([PY, "-B", "tools/lv.py", "lint", str(fp)], cwd=ROOT)
    assert r.returncode == 0, f"lint failed: {fp}"

for cmd in (
    [PY, "-B", "tools/lv.py", "curriculum", "curriculum/hci.yaml"],
    [PY, "-B", "audit/hci/verify_hci.py"],
    [PY, "-B", "audit/review/sync_tpl_from_lesson.py", "HCI", "--write"],
    [PY, "-B", "audit/review/screen_code.py", "check", "--course", "HCI"],
    [PY, "-B", "audit/review/lab_gate.py", "HCI"],
    [PY, "-B", "audit/layout_scan.py", "HCI"],
):
    print(">>> RUN:", " ".join(cmd), flush=True)
    r = subprocess.run(cmd, cwd=ROOT)
    assert r.returncode == 0, f"FAILED: {cmd}"
print("HCI v3 FIXES & ALL GATES + LAYOUT PASSED!", flush=True)
