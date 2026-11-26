"""Clean up all lint FAIL/WARN and boost remaining Stage 10 lessons >= 1640w."""
from pathlib import Path
import io
import sys
from contextlib import redirect_stdout
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import lv  # noqa: E402


def replace_exact(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    if old not in text and new in text:
        return
    assert old in text, f"Missing target in {path}:\n{old[:160]!r}"
    assert text.count(old) == 1, f"Multiple hits in {path}:\n{old[:160]!r}"
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


# 1. TOC L00: remove "bài sau" phrasing + add +45w
replace_exact(
    ROOT / "lessons/toc/L00_chuoi_ngon_ngu.yaml",
    "Mọi khái niệm nâng cao về máy trạng thái, văn phạm và tính khả quyết ở các bài sau đều xây dựng trực tiếp trên ngôn ngữ hình thức giản dị này.",
    "Mọi mô hình máy trạng thái, văn phạm phi ngữ cảnh và khái niệm tính khả quyết đều đứng trên ngôn ngữ hình thức giản dị này. Tập hợp chuỗi càng tường minh thì phép kiểm chứng càng chắc chắn và không bao giờ suy diễn sai biên. Chuẩn bị kỹ khái niệm bảng chữ cái và tập chuỗi ngay hôm nay sẽ giúp bạn đọc thông mọi chứng minh toán học trong phần lý thuyết tính toán.",
)

# 2. TOC L02: pitfalls.4 $k$ -> k, split long 39w sentence in recap.0
replace_exact(
    ROOT / "lessons/toc/L02_nfa_tap_con.yaml",
    "Nhưng khi $k$ tăng lên 20, bảng chuyển sẽ vượt một triệu trạng thái và làm tràn bộ nhớ ngay lập tức.",
    "Nhưng khi k tăng lên 20, bảng chuyển sẽ vượt một triệu trạng thái và làm tràn bộ nhớ ngay lập tức.",
)
replace_exact(
    ROOT / "lessons/toc/L02_nfa_tap_con.yaml",
    "Lưu ý trường hợp cực hạn khi số lượng trạng thái bùng nổ theo hàm mũ như bài toán ký tự thứ k từ cuối để chủ động mô phỏng tập trạng thái trực tiếp trên bộ nhớ nhỏ.",
    "Tuy nhiên cần cảnh giác trường hợp cực hạn khiến số trạng thái bùng nổ theo hàm mũ như bài toán ký tự thứ k từ cuối. Khi đó ta chủ động mô phỏng trực tiếp tập trạng thái ngay trên bộ nhớ nhỏ.",
)

# 3. TOC L04: pitfalls.4 $p$ -> p
replace_exact(
    ROOT / "lessons/toc/L04_bo_de_bom.yaml",
    "Với các chuỗi ngắn hơn số trạng thái $p$, đường đi chưa cần quay lại trạng thái cũ nên ta không rút ra được mâu thuẫn nào. Chỉ khi chọn chuỗi mẫu dài từ $p$ trở lên, đường đi bắt buộc phải lặp vòng và phép bơm mới phá vỡ tỉ lệ đếm.",
    "Với các chuỗi ngắn hơn số trạng thái p, đường đi chưa cần quay lại trạng thái cũ nên ta không rút ra được mâu thuẫn nào. Chỉ khi chọn chuỗi mẫu dài từ p trở lên, đường đi bắt buộc phải lặp vòng và phép bơm mới phá vỡ tỉ lệ đếm.",
)

# 4. TOC L07: pitfalls.4 \cdot -> \times (avoid cdot) + split 178-char recap.0 sentence
replace_exact(
    ROOT / "lessons/toc/L07_mo_ho_phan_tich.yaml",
    "<td>Biểu thức 3 toán tử $1 + 2 \\cdot 3$</td>",
    "<td>Biểu thức 3 toán tử $1 + 2 \\times 3$</td>",
)
replace_exact(
    ROOT / "lessons/toc/L07_mo_ho_phan_tich.yaml",
    "Phân tầng quy tắc theo độ ưu tiên từ yếu nhất tới mạnh nhất, kèm hướng đệ quy bên trái cho kết hợp trái, luôn là công thức chuẩn giúp văn phạm vừa sáng rõ vừa dễ bảo trì lâu dài.",
    "Hãy phân tầng quy tắc theo độ ưu tiên từ yếu nhất tới mạnh nhất. Kèm thêm đệ quy bên trái cho kết hợp trái, văn phạm sẽ vừa sáng rõ vừa dễ bảo trì lâu dài.",
)

# 5. TOC L08: pitfalls.4 $a^n b^n c^n$ -> words
replace_exact(
    ROOT / "lessons/toc/L08_otomat_day_xuong.yaml",
    "Khi cần giữ số đếm qua khối thứ ba như dãy $a^n b^n c^n$, một ngăn xếp hoàn toàn bất lực.",
    "Khi cần giữ số đếm qua khối thứ ba như dãy n chữ a rồi n chữ b rồi n chữ c, một ngăn xếp hoàn toàn bất lực.",
)

# 6. TOC L09: add ~155w in recap.0
replace_exact(
    ROOT / "lessons/toc/L09_may_turing.yaml",
    "Nhớ luôn ba kết cục nhận, từ chối và lặp vô tận để không đánh đồng máy dừng với mọi máy nói chung.",
    "Nhớ luôn ba kết cục nhận, từ chối và lặp vô tận để không đánh đồng máy dừng với mọi máy nói chung. Trong lập trình mô phỏng băng vô hạn hai chiều, ta chỉ cần lưu những ô đã ghi khác ký tự trắng để bộ nhớ luôn gọn. Khi kiểm thử bằng tay từng bước dịch chuyển đầu đọc, hãy viết rõ cấu hình gồm trạng thái hiện tại, vị trí đầu đọc và chuỗi đang nằm trên băng. Khả năng quay ngược lại ghi đè lên các ô cũ chính là điểm khác biệt căn bản giúp máy Turing vượt qua mọi giới hạn của ngăn xếp đơn lẻ. Nắm chắc cơ chế dịch đầu đọc trên băng nhớ là bước chuẩn bị bắt buộc để hiểu bài toán bất khả quyết ở phía trước.",
)

# 7. TOC L10: pitfalls.4 Church -> words
replace_exact(
    ROOT / "lessons/toc/L10_luan_de_van_nang.yaml",
    "Theo luận đề Church–Turing, ranh giới giữa tính được và không tính được hoàn toàn bất biến theo phần cứng.",
    "Theo luận đề vạn năng năm 1936, ranh giới giữa tính được và không tính được hoàn toàn bất biến theo phần cứng.",
)

# 8. PLC boosts & wording fixes on recap.0 (focus: None)
PLC_ADD = {
    "lessons/plc/L03_cay_cu_phap.yaml": (
        "khi duyệt hậu tố qua cây, phần mềm tự động tôn trọng thứ tự tính toán chuẩn mực mà không cần thêm bất kỳ bảng dấu ngoặc phụ nào trong giai đoạn chạy.",
        "khi duyệt hậu tố qua cây, phần mềm tôn trọng thứ tự tính toán chuẩn mực mà không cần bảng dấu ngoặc phụ. Tách rõ cấu trúc lồng nhau ngay tại khâu dựng cây cũng làm cho pha kiểm kiểu và pha sinh mã về sau trở nên thẳng tắp. Thay vì ghép chuỗi lộn xộn, mọi công cụ phân tích tĩnh, trình định dạng và trình tối ưu hiện đại đều làm việc trực tiếp trên từng nút của cây trừu tượng. Đó là lý do các ngôn ngữ dù khác cú pháp bề mặt vẫn chia sẻ cùng một cấu trúc cây biểu thức.",
    ),
    "lessons/plc/L04_pham_vi.yaml": (
        "Hiểu rõ mô hình khung môi trường chuỗi cha cũng giúp bạn lý giải chính xác vì sao vòng đời biến địa phương luôn an toàn.",
        "Hiểu rõ mô hình khung môi trường chuỗi cha cũng giúp bạn lý giải chính xác vì sao vòng đời biến địa phương luôn an toàn. Mỗi khi hàm được gọi lại, một khung mới riêng rẽ được cấp phát mà không đè lên các biến ở tầng trước. Trong thực tế, quy tắc phạm vi tĩnh ngăn chặn lỗi ngầm khó dò khi lập trình viên đổi tên biến trung gian ở hàm gọi. Chỉ trong những tình huống ngoại lệ đặc biệt như cấu hình động hay biến môi trường mới nên dùng quy tắc tra theo ngăn xếp.",
    ),
    "lessons/plc/L06_suy_luan_kieu.yaml": (
        "Nếu một lời gọi truyền sai kiểu dữ liệu ngay cả ở nhánh ít chạy, hệ thống vẫn báo lỗi chính xác từng vị trí ngay trên máy lập trình viên.",
        "Nếu một lời gọi truyền sai kiểu dữ liệu ngay cả ở nhánh ít chạy, hệ thống vẫn báo lỗi chính xác từng vị trí ngay trên máy lập trình viên. Mô hình hợp nhất ràng buộc cũng cho phép suy ra kiểu tổng quát cho các hàm đa hình mà không cần ép kiểu thủ công. Nhờ vậy đội ngũ phát triển vừa giữ được mã nguồn ngắn gọn dễ đọc vừa tin tưởng vào tính nhất quán toàn hệ thống. Trước khi tối ưu hiệu năng chạy, bộ suy luận kiểu giúp loại bỏ ngay toàn bộ lỗi nhầm kiểu số, chuỗi hay danh sách ngay từ lúc biên dịch. Hãy xem từng thông báo lệch ràng buộc kiểu là đồng minh bảo vệ logic chứ không phải rào cản phiền phức.",
    ),
    "lessons/plc/L07_bao_dong.yaml": (
        "Đồng thời vì bao đóng giữ tham chiếu trực tiếp tới biến chứ không chụp ảnh giá trị tại lúc khởi tạo, hãy hết sức cảnh giác khi tạo nhiều hàm con bên trong một vòng lặp dùng chung một biến đếm. Khai báo phạm vi biến mới cho từng vòng lặp là thói quen an toàn tuyệt đối trong ngôn ngữ hiện đại.",
        "Ngoài ra, bao đóng giữ tham chiếu trực tiếp tới biến chứ không chụp lại giá trị tại lúc khởi tạo. Vì thế hãy hết sức cảnh giác khi tạo nhiều hàm con bên trong một vòng lặp dùng chung biến đếm. Khai báo phạm vi biến mới cho từng vòng lặp là thói quen an toàn tuyệt đối. Trong giao diện hiện đại hay xử lý hàm gọi lại bất đồng bộ, bao đóng là công cụ gọn nhất để đóng gói trạng thái nhẹ nhàng mà không cần tạo hẳn lớp đối tượng cồng kềnh. Nắm chắc mối liên hệ giữa bao đóng và môi trường trên vùng nhớ đống giúp bạn tránh hoàn toàn lỗi rò rỉ bộ nhớ lẫn bẫy giữ biến vòng lặp.",
    ),
    "lessons/plc/L09_truyen_tham_so.yaml": (
        "Với truyền chia sẻ tham chiếu đối tượng như trong Python hay Java, sửa thuộc tính bên trong đối tượng hiện ngay ra ngoài, nhưng gán lại tên tham số chỉ đổi nhãn cục bộ. Đọc rõ quy ước truyền tham số và kiểm tra đột biến ngoài ý muốn là nguyên tắc vàng khi thiết kế hàm thư viện dùng chung.",
        "Với cơ chế truyền chia sẻ đối tượng phổ biến hiện nay, sửa thuộc tính bên trong hiện ngay ra ngoài, còn gán lại tên tham số chỉ đổi nhãn cục bộ. Đọc rõ quy ước truyền tham số và kiểm tra đột biến ngoài ý muốn là nguyên tắc vàng khi thiết kế hàm dùng chung. Khi thực sự cần giữ nguyên dữ liệu gốc qua nhiều tầng xử lý lồng sâu, hãy dùng phép sao chép sâu hoặc cấu trúc bất biến thay cho sao chép nông. Một vài phút xác nhận cơ chế truyền đối số sẽ cứu dự án khỏi hàng giờ truy vết sai lệch dữ liệu âm thầm.",
    ),
    "lessons/plc/L10_sinh_ma_ngan_xep.yaml": (
        "Nguyên tắc kiểm chặt thứ tự toán hạng trừ và chia giúp mọi máy ảo chạy đa nền tảng đều cho kết quả nhất quán tuyệt đối.",
        "Nguyên tắc kiểm chặt thứ tự toán hạng trừ và chia giúp mọi máy ảo chạy đa nền tảng đều cho kết quả nhất quán tuyệt đối. Khi muốn chuyển từ máy ngăn xếp sang máy dùng thanh ghi thực tế trên bộ xử lý, thuật toán chỉ việc ánh xạ hai vị trí đỉnh ngăn xếp vào các thanh ghi tạm tương ứng. Nắm vững kỹ thuật sinh mã bằng duyệt hậu tố cũng mở đường cho bạn đọc hiểu tệp mã byte của máy ảo và viết các bộ thông dịch nhỏ cực nhanh.",
    ),
    "lessons/plc/L11_toi_uu.yaml": (
        "Mọi phép tối ưu đánh đổi độ chính xác hoặc làm thay đổi lỗi tràn số nguyên đều bị coi là sai về mặt ngữ nghĩa.",
        "Mọi phép tối ưu đánh đổi độ chính xác hoặc làm thay đổi lỗi tràn số nguyên đều bị coi là sai về mặt ngữ nghĩa. Do đó các trình biên dịch chuyên nghiệp luôn kiểm chứng từng bước biến đổi trên tập đầu vào biên và phân tích phụ thuộc hiệu ứng phụ thật chặt chẽ. Đo thời gian thực tế trước và sau khi bật tối ưu giúp bạn biết chắc vòng lặp nào đang được rút gọn thay vì phỏng đoán cảm tính.",
    ),
}

for rel, (old_part, new_part) in PLC_ADD.items():
    p = ROOT / rel
    text = p.read_text(encoding="utf-8")
    if old_part.lower() in text.lower() and new_part not in text:
        # case-match exact
        idx = text.find(old_part)
        if idx == -1:
            idx = text.find(old_part[0].upper() + old_part[1:])
            if idx != -1:
                old_exact = text[idx:idx + len(old_part)]
                new_exact = new_part[0].upper() + new_part[1:]
                replace_exact(p, old_exact, new_exact)
                continue
        replace_exact(p, old_part, new_part)

# 9. HCI L11 & HCI L12: adjust sentences & exact focus counts
replace_exact(
    ROOT / "lessons/hci/L11_tinh_huong_canh_bao.yaml",
    """    focus:
    - 1
    - 1
    - 1
    - 1
    - 1
    - 1
    say: Ở bài 12 tới, ta sẽ bước vào bài tổng kết hành trình lịch sử về các chuẩn tiếp cận web giúp mọi người đều tiếp cận được không gian số. Ta sẽ chứng kiến sự chuyển dịch từ mười bốn lời khuyên chung chung sang hàng loạt tiêu chí đo lường được bằng con số chính xác. Nhờ những thay đổi này, người khiếm thị dùng trình đọc màn hình hay người vận động khó khăn trên thiết bị di động nhỏ gọn đều sử dụng sản phẩm công bằng hơn. Đây cũng là mảnh ghép hoàn thiện bức tranh thiết kế hướng về con người trong suốt mười hai bài học vừa qua. Hãy chuẩn bị giấy bút để cùng nhìn lại toàn bộ hành trình phát triển đầy cảm hứng này. Hẹn gặp bạn ở video tiếp theo.""",
    """    focus:
    - 1
    - 1
    - 1
    - 1
    - 1
    - 1
    - 1
    say: Ở bài 12 tới, ta sẽ bước vào bài tổng kết hành trình lịch sử về các chuẩn tiếp cận web giúp mọi người đều tiếp cận được không gian số. Ta sẽ chứng kiến sự chuyển dịch từ mười bốn lời khuyên chung chung sang hàng loạt tiêu chí đo lường được bằng con số chính xác. Nhờ những thay đổi này, người khiếm thị dùng trình đọc màn hình hay người vận động khó khăn trên thiết bị nhỏ đều sử dụng sản phẩm công bằng hơn. Mọi nút bấm, độ tương phản và nhãn trường nhập đều được kiểm chứng bằng định lượng cụ thể chứ không cảm tính. Đây cũng là mảnh ghép hoàn thiện bức tranh thiết kế hướng về con người trong suốt mười hai bài học vừa qua. Hãy chuẩn bị giấy bút để cùng nhìn lại toàn bộ hành trình phát triển đầy cảm hứng này. Hẹn gặp bạn ở video tiếp theo.""",
)
replace_exact(
    ROOT / "lessons/hci/L12_hanh_trinh_wcag.yaml",
    """    focus:
    - 1
    - 1
    - 2
    - 2
    - 2
    - 2
    - 2
    say: Tổng kết toàn bộ khoá học Tương tác người máy, chúng ta đã đi từ cách nhìn lỗi do thiết kế và mô hình tâm trí, qua các định luật đo được, tới chuẩn tiếp cận quốc tế. Thiết kế tốt không phải là làm cho đẹp mắt, mà là xây dựng sự thấu cảm và trách nhiệm bảo vệ người dùng. Từ 65 điểm kiểm năm 1999 tới 86 tiêu chí đo được năm 2023 cho màn hình nhỏ và đích 24 điểm ảnh. Công cụ tự động chỉ kiểm được một phần trên web lớn. Muốn đạt chuẩn thực chất, đội ngũ phát triển vẫn cần kiểm tra điều hướng bằng bàn phím thật và thử cùng người dùng sử dụng công nghệ hỗ trợ. Mỗi tiêu chí về độ tương phản, dàn dòng và kích thước vùng chạm đều có cơ sở đo lường cụ thể giúp sản phẩm phục vụ bền vững.""",
    """    focus:
    - 1
    - 1
    - 2
    - 2
    - 2
    - 2
    say: Tổng kết toàn bộ khoá học Tương tác người máy, chúng ta đã đi từ cách nhìn lỗi do thiết kế và mô hình tâm trí, qua các định luật đo được, tới chuẩn tiếp cận quốc tế. Thiết kế tốt không phải là làm cho đẹp mắt, mà là xây dựng sự thấu cảm và trách nhiệm bảo vệ người dùng. Từ 65 điểm kiểm năm 1999 tới 86 tiêu chí đo được năm 2023 cho màn hình nhỏ và đích 24 điểm ảnh, tiêu chuẩn ngày càng rõ ràng. Công cụ tự động chỉ kiểm được một phần trên web lớn nên đội ngũ phát triển cần kiểm tra thêm điều hướng bàn phím thật. Thử trực tiếp cùng người dùng sử dụng công nghệ hỗ trợ giúp phát hiện các rào cản ẩn sâu trong quy trình. Mỗi tiêu chí về độ tương phản, dàn dòng và kích thước vùng chạm đều có cơ sở đo lường cụ thể.""",
)
replace_exact(
    ROOT / "lessons/hci/L12_hanh_trinh_wcag.yaml",
    """    focus:
    - 1
    - 1
    - 1
    - 1
    - 1
    - 1
    say: Tư duy lớn nhất bạn cần mang theo là công nghệ chỉ thực sự có ý nghĩa khi phục vụ bình đẳng tất cả mọi người. Từ những nguyên lý nhỏ như chọn kích thước nút theo định luật trỏ hay giữ trật tự thực đơn quen thuộc, ta xây nên phần mềm an toàn hơn. Đừng đợi tới ngày nghiệm thu mới kiểm tra khả năng tiếp cận hay phòng chống lỗi, mà hãy tích hợp chúng ngay từ bản phác thảo đầu tiên. Kiến thức thực hành cùng mười ba bài thực nghiệm tự chấm sẽ là hành trang tin cậy để bạn tự tin thiết kế mọi sản phẩm số chất lượng cao. Chúc mừng bạn đã hoàn thành trọn vẹn toàn bộ khoá học Tương tác người máy!""",
    """    focus:
    - 1
    - 1
    - 1
    - 1
    - 1
    say: Tư duy lớn nhất bạn cần mang theo là công nghệ chỉ thực sự có ý nghĩa khi phục vụ bình đẳng tất cả mọi người. Từ những nguyên lý nhỏ như chọn kích thước nút theo định luật trỏ hay giữ trật tự thực đơn quen thuộc, ta xây nên phần mềm an toàn hơn. Đừng đợi tới ngày nghiệm thu mới kiểm tra khả năng tiếp cận hay phòng chống lỗi, mà hãy tích hợp chúng ngay từ bản phác thảo đầu tiên. Kiến thức thực hành cùng mười ba bài thực nghiệm tự chấm sẽ là hành trang tin cậy để bạn thiết kế sản phẩm số chất lượng cao. Chúc mừng bạn đã hoàn thành trọn vẹn khoá học Tương tác người máy!""",
)

# Sync HCI L11 recap.0 focus length exactly to lv._sentences count if off
p_hci11 = ROOT / "lessons/hci/L11_tinh_huong_canh_bao.yaml"
d11 = yaml.safe_load(p_hci11.read_text(encoding="utf-8"))
r0_11 = next(sc["steps"][0] for sc in d11["scenes"] if sc["id"] == "recap")
# Count sentences using lv
n11 = len(lv._sentences(r0_11["say"])) if hasattr(lv, "_sentences") else len([s for s in r0_11["say"].replace("?", ".").replace("!", ".").split(".") if s.strip()])
print("HCI L11 recap.0 estimated sentences:", n11, "current focus len:", len(r0_11["focus"]))
if n11 != len(r0_11["focus"]):
    new_f = [1, 1] + [2] * (n11 - 2)
    old_block = "    focus:\n" + "\n".join(f"    - {x}" for x in r0_11["focus"]) + "\n    say: Tổng kết bài học tình huống,"
    new_block = "    focus:\n" + "\n".join(f"    - {x}" for x in new_f) + "\n    say: Tổng kết bài học tình huống,"
    replace_exact(p_hci11, old_block, new_block)

# Lint all 80 Stage 10 lessons!
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
print(f"STAGE 10 SUMMARY (80 lessons): FAIL={errs}, WARN={warns}", flush=True)
assert errs == 0 and warns == 0
