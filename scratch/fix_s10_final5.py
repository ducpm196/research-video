from pathlib import Path
import io
import sys
from contextlib import redirect_stdout

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import lv  # noqa: E402


def rep(rel: str, old: str, new: str) -> None:
    p = ROOT / rel
    txt = p.read_text(encoding="utf-8")
    assert old in txt, f"Missing in {rel}: {old[:120]!r}"
    assert txt.count(old) == 1, f"Multi in {rel}"
    p.write_text(txt.replace(old, new, 1), encoding="utf-8")


rep(
    "lessons/plc/L03_cay_cu_phap.yaml",
    "Đó là lý do các ngôn ngữ dù khác cú pháp bề mặt vẫn chia sẻ cùng một cấu trúc cây biểu thức.",
    "Đó là lý do các ngôn ngữ dù khác cú pháp bề mặt vẫn chia sẻ cùng một cấu trúc cây biểu thức. Nhờ tách rời pha đọc văn bản và pha xử lý ngữ nghĩa trên cây, người viết trình biên dịch có thể tái sử dụng toàn bộ tầng tối ưu và sinh mã cho nhiều cú pháp nguồn khác nhau một cách rất gọn gàng.",
)
rep(
    "lessons/plc/L06_suy_luan_kieu.yaml",
    "Hãy xem từng thông báo lệch ràng buộc kiểu là đồng minh bảo vệ logic chứ không phải rào cản phiền phức.",
    "Hãy xem từng thông báo lệch ràng buộc kiểu là đồng minh bảo vệ logic chứ không phải rào cản phiền phức. Một mô hình ràng buộc rõ ràng cho phép mở rộng ngôn ngữ an toàn hơn nhiều, giúp hàng nghìn dòng mã cộng tác chặt chẽ mà vẫn giữ được tốc độ kiểm tra tức thì.",
)
rep(
    "lessons/plc/L07_bao_dong.yaml",
    "sự kiện bất đồng bộ hay callback.",
    "sự kiện bất đồng bộ hay hàm gọi lại.",
)
rep(
    "lessons/plc/L07_bao_dong.yaml",
    "Nắm chắc mối liên hệ giữa bao đóng và môi trường trên vùng nhớ đống giúp bạn tránh hoàn toàn lỗi rò rỉ bộ nhớ lẫn bẫy giữ biến vòng lặp.",
    "Nắm chắc mối liên hệ giữa bao đóng và môi trường trên vùng nhớ đống giúp bạn tránh hoàn toàn lỗi rò rỉ bộ nhớ lẫn bẫy giữ biến vòng lặp. Hơn thế nữa, kỹ thuật biến đổi bao đóng trong trình biên dịch còn biến mọi hàm lồng nhau thành cặp con trỏ hàm kèm cấu trúc môi trường phẳng. Nhờ đó ngay cả những ngôn ngữ biên dịch ra mã máy trực tiếp không cần máy ảo vẫn chạy được hàm bậc cao nhanh gọn và an toàn bộ nhớ tuyệt đối.",
)
rep(
    "lessons/plc/L10_sinh_ma_ngan_xep.yaml",
    "Nắm vững kỹ thuật sinh mã bằng duyệt hậu tố cũng mở đường cho bạn đọc hiểu tệp mã byte của máy ảo và viết các bộ thông dịch nhỏ cực nhanh.",
    "Nắm vững kỹ thuật sinh mã bằng duyệt hậu tố cũng mở đường cho bạn đọc hiểu tệp mã trung gian của máy ảo và viết các bộ thông dịch nhỏ cực nhanh. Sau này khi thiết kế biểu thức điều kiện, vòng lặp hay lời gọi hàm đệ quy trên ngăn xếp, bạn vẫn giữ nguyên quy tắc đọc đỉnh và đẩy kết quả cực kỳ nhất quán đó.",
)
rep(
    "lessons/hci/L12_hanh_trinh_wcag.yaml",
    """    focus:
    - 1
    - 1
    - 1
    - 1
    - 1
    say: Tư duy lớn nhất bạn cần mang theo là công nghệ chỉ thực sự có ý nghĩa khi phục vụ bình đẳng tất cả mọi người. Từ những nguyên lý nhỏ như chọn kích thước nút theo định luật trỏ hay giữ trật tự thực đơn quen thuộc, ta xây nên phần mềm an toàn hơn. Đừng đợi tới ngày nghiệm thu mới kiểm tra khả năng tiếp cận hay phòng chống lỗi, mà hãy tích hợp chúng ngay từ bản phác thảo đầu tiên. Kiến thức thực hành cùng mười ba bài thực nghiệm tự chấm sẽ là hành trang tin cậy để bạn thiết kế sản phẩm số chất lượng cao. Chúc mừng bạn đã hoàn thành trọn vẹn khoá học Tương tác người máy!""",
    """    focus:
    - 1
    - 1
    - 1
    - 1
    - 1
    - 1
    say: Tư duy lớn nhất bạn cần mang theo là công nghệ chỉ thực sự có ý nghĩa khi phục vụ bình đẳng tất cả mọi người. Từ những nguyên lý nhỏ như chọn kích thước nút theo định luật trỏ hay giữ trật tự thực đơn quen thuộc, ta xây nên phần mềm an toàn hơn. Đừng đợi tới ngày nghiệm thu mới kiểm tra khả năng tiếp cận hay phòng chống lỗi, mà hãy tích hợp chúng ngay từ bản phác thảo đầu tiên. Khi đo đạc được trải nghiệm người dùng bằng con số cụ thể, mọi quyết định thiết kế đều đứng vững trước áp lực tiến độ dự án. Kiến thức thực hành cùng mười ba bài thực nghiệm tự chấm sẽ là hành trang tin cậy để bạn thiết kế sản phẩm số chất lượng cao. Chúc mừng bạn đã hoàn thành trọn vẹn khoá học Tương tác người máy!""",
)

errs = warns = 0
for c in ("toc", "plc", "par", "hci", "sep", "cas"):
    for p in sorted((ROOT / "lessons" / c).glob("L*.yaml")):
        sp = lv.load_spec(p)
        with redirect_stdout(io.StringIO()):
            res = lv.lint(sp, quiet=True)
        w = sum(len((s.get("say") or "").split()) for sc in sp["scenes"] for s in sc["steps"])
        errs += len(res.errors)
        warns += len(res.warnings)
        if res.errors or res.warnings or w < 1620:
            print(f"{c.upper()}:{sp['id']} w={w} FAIL={len(res.errors)} WARN={len(res.warnings)} {res.errors[:2]} {res.warnings[:2]}")
print(f"STAGE 10 FINAL LINT (80 lessons): FAIL={errs}, WARN={warns}", flush=True)
assert errs == 0 and warns == 0
