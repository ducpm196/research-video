"""Apply remaining Stage 10 AF4 polish: SVG contrast, P1 glosses, PLC tầm vực->phạm vi, TOC P9 body tables, 20 tight duration boosts."""
from pathlib import Path
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import lv  # noqa: E402


def replace_exact(path: Path, old: str, new: str, multi: bool = False) -> None:
    text = path.read_text(encoding="utf-8")
    if old not in text and new in text:
        return
    assert old in text, f"Missing target in {path}:\n{old[:180]!r}"
    if not multi:
        assert text.count(old) == 1, f"Multiple hits in {path}:\n{old[:180]!r}"
        path.write_text(text.replace(old, new, 1), encoding="utf-8")
    else:
        path.write_text(text.replace(old, new), encoding="utf-8")


# 1. HCI L08 SVG contrast darkening on light slide background
p_hci8 = ROOT / "lessons/hci/L08_thi_nghiem_giao_dien.yaml"
t8 = p_hci8.read_text(encoding="utf-8")
t8 = t8.replace('<text x="100" y="105" fill="#38bdf8"', '<text x="100" y="105" fill="#0369a1"')
t8 = t8.replace('<text x="500" y="145" fill="#38bdf8"', '<text x="500" y="145" fill="#0369a1"')
t8 = t8.replace('<text x="300" y="185" fill="#38bdf8"', '<text x="300" y="185" fill="#0369a1"')
t8 = t8.replace('<text x="300" y="105" fill="#22c55e"', '<text x="300" y="105" fill="#15803d"')
t8 = t8.replace('<text x="100" y="145" fill="#22c55e"', '<text x="100" y="145" fill="#15803d"')
t8 = t8.replace('<text x="500" y="185" fill="#22c55e"', '<text x="500" y="185" fill="#15803d"')
p_hci8.write_text(t8, encoding="utf-8")

# 2. P1 glosses in HCI, PAR, PLC, CAS
replace_exact(
    ROOT / "lessons/hci/L02_dinh_luat_fitts.yaml",
    "khoảng cách D=360 px giữa nút 18 px và nút 72 px",
    "khoảng cách D=360 px (điểm ảnh) giữa nút 18 px và nút 72 px",
)
replace_exact(
    ROOT / "lessons/hci/L09_truy_cap.yaml",
    "Tính lợi ích vùng bấm 48 px so với 28 px ở khoảng cách D=300 px và tỉ lệ diện tích",
    "Tính lợi ích vùng bấm 48 px (điểm ảnh) so với 28 px ở khoảng cách D=300 px và tỉ lệ diện tích",
)
replace_exact(
    ROOT / "lessons/hci/L03_hick_hyman.yaml",
    "tuyến tính O(n) thay vì log2(n+1).",
    "tuyến tính $O(n)$ (tỉ lệ thuận theo số mục $n$) thay vì $\\log_2(n+1)$.",
)
replace_exact(
    ROOT / "lessons/hci/L10_chong_loi.yaml",
    "xuống 10^-5 và thêm hoàn tác",
    "xuống $10^{-5}$ (một phần trăm nghìn) và thêm hoàn tác",
)
# PAR P1 units
replace_exact(
    ROOT / "lessons/par/L09_chia_khoi.yaml",
    "<tr><td>không tối ưu</td><td>119,9 GB/s</td></tr>",
    "<tr><td>không tối ưu</td><td>119,9 GB/s (tỉ byte mỗi giây)</td></tr>",
)
replace_exact(
    ROOT / "lessons/par/L10_all_reduce.yaml",
    "<td>125 MB</td>",
    "<td>125 MB (triệu byte)</td>",
)
replace_exact(
    ROOT / "lessons/par/L10_all_reduce.yaml",
    "64 máy, gói 1 MB, trễ 0,05 ms",
    "64 máy, gói 1 MB, trễ 0,05 ms (mi-li-giây)",
)
replace_exact(
    ROOT / "lessons/par/L11_huan_luyen_phan_tan.yaml",
    "trong <b>100 ms</b>.",
    "trong <b>100 ms</b> (mi-li-giây).",
)
# PLC tầm vực -> phạm vi (L04) + symbol glosses (L05/08/09/12)
replace_exact(
    ROOT / "lessons/plc/L04_pham_vi.yaml",
    "tầm vực tĩnh so với tầm vực động",
    "phạm vi tĩnh so với phạm vi động",
)
replace_exact(
    ROOT / "labs/PLC/L04/de.md",
    "tầm vực tĩnh",
    "phạm vi tĩnh",
    multi=True,
)
replace_exact(
    ROOT / "labs/PLC/L04/de.md",
    "tầm vực động",
    "phạm vi động",
    multi=True,
)
replace_exact(
    ROOT / "audit/s9_11/up_s10.py",
    '"L04", "Mô phỏng chuỗi môi trường tra tên: tầm vực tĩnh so với tầm vực động",\n         "Cài hàm `lookup(env, name)` duyệt theo liên kết cha để so sánh tra tên theo tầm vực tĩnh (từ vị trí định nghĩa hàm với `x = 15`) và tầm vực động (theo ngăn xếp lời gọi với `x = 30`).',
    '"L04", "Mô phỏng chuỗi môi trường tra tên: phạm vi tĩnh so với phạm vi động",\n         "Cài hàm `lookup(env, name)` duyệt theo liên kết cha để so sánh tra tên theo phạm vi tĩnh (từ vị trí định nghĩa hàm với `x = 15`) và phạm vi động (theo ngăn xếp lời gọi với `x = 30`).',
)
replace_exact(
    ROOT / "lessons/plc/L05_kieu_du_lieu.yaml",
    "<tr><td>số thực <code>1.0f</code>,",
    "<tr><td>số thực dấu phẩy động <code>1.0f</code> (đuôi f chỉ kiểu thực 32 bit trong C),",
)
replace_exact(
    ROOT / "lessons/plc/L08_bo_nho.yaml",
    "(khối <code>with</code>, <code>try … finally</code>)",
    "(khối quản lý tự đóng <code>with</code> hoặc cặp bảo đảm dọn <code>try … finally</code>)",
)
replace_exact(
    ROOT / "lessons/plc/L09_truyen_tham_so.yaml",
    "<td><code>void f(int x)</code> trong C</td>",
    "<td><code>void f(int x)</code> (<code>void</code> là không trả về giá trị trong C)</td>",
)
replace_exact(
    ROOT / "lessons/plc/L09_truyen_tham_so.yaml",
    "<tr><td>sâu: <code>copy.deepcopy(a)</code></td>",
    "<tr><td>sâu (sao chép toàn bộ tầng lồng nhau): <code>copy.deepcopy(a)</code></td>",
)
replace_exact(
    ROOT / "lessons/plc/L12_lap_trinh_ham.yaml",
    "để hàm thuần trở lại, rồi mới lưu kết quả.</p>",
    "để hàm thuần trở lại, rồi mới lưu kết quả bằng bộ trang trí (decorator) <code>@lru_cache</code>.</p>",
)
# CAS L05 check#0 dict comprehension gloss
replace_exact(
    ROOT / "lessons/cas/L05_knight_capital.yaml",
    "<code>set(...)</code> loại phần tử trùng nhau, và <code>return</code> trả kết quả.</p>",
    "<code>{k: v for ...}</code> dựng từ điển theo từng cặp khoá và giá trị, <code>set(...)</code> loại phần tử trùng nhau, và <code>return</code> trả kết quả.</p>",
)

# 3. TOC P9 body tables in pitfalls for L02, L03, L04, L06, L07, L08, L10, L11, L12, L13
TOC_P9_TABLES = {
    "L02": (
        '<table class="t"><tr><th>quy mô bài toán</th><th>số trạng thái NFA → DFA</th><th>hệ quả vận hành</th></tr><tr><td>Ký tự thứ $k=3$ từ cuối</td><td>$4$ trạng thái NFA → $2^3 = 8$ trạng thái DFA</td><td>chạy thử trên bảng dễ theo dõi hết</td></tr><tr><td>Ký tự thứ $k=20$ từ cuối</td><td>$21$ trạng thái NFA → $2^{20} \\approx 1$ triệu trạng thái DFA</td><td>không dựng sẵn DFA mà mô phỏng tập trạng thái tại chỗ</td></tr></table>',
        "Hãy so hai mức quy mô của phép biến đổi này để tránh dựng bảng phình to quá mức. Với bài toán tìm ký tự thứ 3 từ cuối, máy đơn định chỉ cần 8 trạng thái nên vẽ trọn trên bảng rất dễ. Nhưng khi $k$ tăng lên 20, bảng chuyển sẽ vượt một triệu trạng thái và làm tràn bộ nhớ ngay lập tức. Khi đó bộ thực thi nên mô phỏng trực tiếp tập trạng thái tại chỗ thay vì dựng trước toàn bộ bảng."
    ),
    "L03": (
        '<table class="t"><tr><th>quy mô mẫu ghép</th><th>bước chạy máy khớp</th><th>cảnh báo thực tế</th></tr><tr><td>Chuỗi 20 ký tự trên NFA</td><td>vài chục phép dịch chuyển hợp nhất tập</td><td>luôn hoàn tất trong thời gian tuyến tính $O(n)$</td></tr><tr><td>Bộ lọc mạng 100 000 luồng/giây</td><td>quét liên tục chuỗi dài bằng thuật toán quay lui</td><td>mẫu tham lam dễ treo máy chủ nên chuẩn hoá dùng máy trạng thái hữu hạn</td></tr></table>',
        "So sánh ở hai mức quy mô cho thấy lý do hệ thống lớn buộc phải chọn bộ máy khớp chuẩn. Trên chuỗi thử dài 20 ký tự, sự khác biệt giữa các bộ máy hầu như không đáng kể. Nhưng trên bộ lọc lưu lượng hàng trăm nghìn yêu cầu mỗi giây, thuật toán quay lui dễ nổ thời gian theo hàm mũ và làm treo dịch vụ. Dùng máy trạng thái hữu hạn bảo đảm thời gian xử lý luôn tuyến tính với độ dài đầu vào."
    ),
    "L04": (
        '<table class="t"><tr><th>quy mô độ dài chuỗi</th><th>kiểm tra bằng bổ đề bơm</th><th>giới hạn ứng dụng</th></tr><tr><td>Đầu vào ngắn dưới $p$</td><td>không kích hoạt vòng lặp trạng thái</td><td>không chứng minh được bằng chứng phản ví dụ</td></tr><tr><td>Đầu vào độ dài $\\ge p$ (hằng số bơm)</td><td>chắc chắn lặp ít nhất một trạng thái trong máy hữu hạn</td><td>bơm $i=0$ hoặc $i=2$ lập tức phá điều kiện thành phần</td></tr></table>',
        "Quy mô độ dài chuỗi quyết định ranh giới hoạt động của bổ đề bơm. Với các chuỗi ngắn hơn số trạng thái $p$, đường đi chưa cần quay lại trạng thái cũ nên ta không rút ra được mâu thuẫn nào. Chỉ khi chọn chuỗi mẫu dài từ $p$ trở lên, đường đi bắt buộc phải lặp vòng và phép bơm mới phá vỡ tỉ lệ đếm. Đây là mấu chốt giúp bác bỏ tính chính quy bằng đúng một phản ví dụ tổng quát."
    ),
    "L06": (
        '<table class="t"><tr><th>quy mô phân cấp ngữ pháp</th><th>sức diễn đạt</th><th>ví dụ tiêu biểu</th></tr><tr><td>Chính quy (máy hữu hạn)</td><td>đếm cộng dồn modulo, không nhớ sâu vô hạn</td><td>độ dài chẵn, kết thúc bằng 01</td></tr><tr><td>Phi ngữ cảnh (có đệ quy lồng nhau)</td><td>khớp ngoặc cân bằng sâu tuỳ ý $(^n)^n$</td><td>ngôn ngữ lập trình khối lồng nhau, biểu thức số học</td></tr></table>',
        "Hãy đối chiếu hai mức quy mô cấu trúc để chọn đúng công cụ mô tả ngôn ngữ. Khi bài toán chỉ kiểm đuôi chuỗi hay đếm chia dư cố định, mô hình chính quy đủ nhẹ và nhanh. Nhưng ngay khi xuất hiện cặp ngoặc hoặc câu lệnh lồng nhau ở độ sâu tuỳ ý, bộ nhớ hữu hạn không thể đếm nổi và ta cần văn phạm phi ngữ cảnh. Quy tắc đệ quy cho phép lồng ghép cấu trúc vô hạn chỉ từ hữu hạn quy tắc sinh."
    ),
    "L07": (
        '<table class="t"><tr><th>quy mô trình phân tích cú pháp</th><th>mơ hồ cấu trúc</th><th>hệ quả biên dịch</th></tr><tr><td>Biểu thức 3 toán tử $1 + 2 \\cdot 3$</td><td>2 cây phân tích khác nghĩa: $9$ vs $7$</td><td>dễ phát hiện và sửa bằng quy tắc ưu tiên</td></tr><tr><td>Ngữ pháp ngôn ngữ hàng trăm luật</td><td>hàng nghìn cây sinh cho một câu lệnh phức hợp</td><td>không có thuật toán tổng quát kiểm tra nên phải phân tầng chặt từ đầu</td></tr></table>',
        "Ở quy mô một biểu thức nhỏ gồm ba số, sự mơ hồ chỉ tạo ra hai cây đối nghịch nhau dễ nhìn thấy bằng mắt. Nhưng với ngữ pháp hoàn chỉnh hàng trăm luật, các xung đột ưu tiên và kết hợp có thể tạo hàng loạt cách hiểu ẩn sâu. Vì bài toán kiểm tra tính mơ hồ tổng quát là bất khả quyết, người thiết kế trình biên dịch phải phân tầng mức ưu tiên tường minh. Cách làm này triệt tiêu hoàn toàn hai cây cùng lúc ngay từ khâu thiết kế."
    ),
    "L08": (
        '<table class="t"><tr><th>quy mô bộ nhớ phụ trợ</th><th>ngôn ngữ nhận dạng được</th><th>giới hạn tách khối</th></tr><tr><td>Một ngăn xếp (PDA)</td><td>khớp 1 cặp khối đối xứng $a^n b^n$</td><td>ngăn xếp bị xoá sạch khi khớp xong cặp đầu tiên</td></tr><tr><td>Hai ngăn xếp (tương đương máy Turing)</td><td>so khớp ba khối $a^n b^n c^n$ trở lên</td><td>đủ sức tính toán mọi thuật toán khả quyết</td></tr></table>',
        "Sự chênh lệch giữa một ngăn xếp và hai ngăn xếp cho thấy bước nhảy lớn về năng lực tính toán. Một ngăn xếp khớp hoàn hảo cặp đầu tiên nhưng lại tiêu huỷ toàn bộ thông tin đếm ngay khi rút ra. Khi cần giữ số đếm qua khối thứ ba như dãy $a^n b^n c^n$, một ngăn xếp hoàn toàn bất lực. Chỉ cần thêm đúng một ngăn xếp thứ hai, hệ thống lập tức ngang sức mạnh với một máy tính đầy đủ."
    ),
    "L10": (
        '<table class="t"><tr><th>quy mô mô hình tính toán</th><th>tập hàm biểu diễn</th><th>chi phí thực thi</th></tr><tr><td>Máy tính một băng đơn</td><td>mọi hàm tính được theo luận đề Church–Turing</td><td>mô phỏng truy cập ngẫu nhiên chậm bậc $O(t^2)$</td></tr><tr><td>Bộ xử lý nhiều băng / truy cập ngẫu nhiên</td><td>vẫn chính xác cùng tập hàm tính được</td><td>tăng tốc truy xuất trong thời gian thực nhưng không vượt giới hạn khả quyết</td></tr></table>',
        "Đặt hai quy mô kiến trúc cạnh nhau giúp tách bạch rõ tốc độ và giới hạn lý thuyết. Một máy nhiều băng hay thanh ghi truy cập ngẫu nhiên chạy nhanh hơn máy một băng nhiều lần trong thực tế. Tuy nhiên tốc độ nhanh đến đâu cũng không giải được thêm bất kỳ bài toán bất khả quyết nào. Theo luận đề Church–Turing, ranh giới giữa tính được và không tính được hoàn toàn bất biến theo phần cứng."
    ),
    "L11": (
        '<table class="t"><tr><th>quy mô kiểm thử chương trình</th><th>kết luận đạt được</th><th>giới hạn tuyệt đối</th></tr><tr><td>Chạy thử tối đa $k = 10\\,000$ bước</td><td>khả quyết: biết chắc dừng trong ngưỡng hay chưa</td><td>không phân biệt được lặp vô tận với chương trình chạy $10\\,001$ bước</td></tr><tr><td>Bài toán Dừng tổng quát cho mọi đầu vào</td><td>chỉ nửa khả quyết nếu biết chắc máy dừng</td><td>không tồn tại thuật toán nào trả lời đúng mọi trường hợp trong hữu hạn bước</td></tr></table>',
        "So sánh quy mô có hạn và vô hạn bước vạch rõ chỗ hay nhầm trong kiểm thử phần mềm. Nếu đặt hạn mức 10 nghìn bước, ta chỉ cần bấm đồng hồ đếm đủ lượt là khẳng định dứt khoát. Nhưng bài toán Dừng hỏi cho mọi số bước tuỳ ý nên phép thử hữu hạn không bao giờ chứng minh được vòng lặp vô tận. Đó là lý do các công cụ phân tích tĩnh buộc phải chấp nhận cảnh báo dư."
    ),
    "L12": (
        '<table class="t"><tr><th>quy mô bài toán kiểm chứng</th><th>bản chất tính chất</th><th>khả năng tự động hoá</th></tr><tr><td>Kiểm tính chất cú pháp (độ dài mã, số trạng thái)</td><td>không phụ thuộc hàm tính toán</td><td>luôn khả quyết, đọc trực tiếp bản mô tả máy</td></tr><tr><td>Kiểm bất kỳ tính chất ngữ nghĩa không tầm thường nào</td><td>phụ thuộc tập chuỗi ngôn ngữ máy nhận</td><td>bất khả quyết theo định lý Rice nhờ quy dẫn từ bài toán Dừng</td></tr></table>',
        "Hai nhóm bài toán minh hoạ lằn ranh sắc gọn của định lý Rice. Các câu hỏi thuần về văn bản chương trình hay cấu trúc khối lệnh đều có thể quyết định trọn vẹn bằng bộ phân tích cú pháp. Nhưng mọi câu hỏi về hành vi rốt cuộc của chương trình đối với toàn bộ đầu vào đều bị bất khả quyết. Bất kỳ trình kiểm chứng tổng quát nào hứa kiểm mọi hành vi ngữ nghĩa đều vi phạm kết quả này."
    ),
    "L13": (
        '<table class="t"><tr><th>quy mô bài toán NP trên thực tế</th><th>kích thước đầu vào $n$</th><th>chiến lược ứng dụng</th></tr><tr><td>Bài toán nhỏ ($n \\le 15$)</td><td>$2^{15} = 32\\,768$ tổ hợp</td><td>duyệt vét cạn vẫn tìm ra nghiệm tối ưu trong vài mi-li-giây</td></tr><tr><td>Bài toán quy mô công nghiệp ($n = 200$)</td><td>$2^{200}$ tổ hợp (vượt số nguyên tử quan sát được)</td><td>bỏ tìm tối ưu tuyệt đối nếu P khác NP, chuyển sang thuật toán xấp xỉ hoặc gợi ý</td></tr></table>',
        "Bảng hai mức quy mô cho thấy vì sao lý thuyết phức tạp có giá trị định hướng thiết kế ngay lập tức. Với mười lăm biến, thuật toán vét cạn chạy xong gần như tức thì trên mọi máy tính cá nhân. Nhưng khi dữ liệu thật phình lên hàng trăm biến, chi phí tăng hàm mũ phá vỡ mọi nỗ lực chờ đợi dù phần cứng mạnh lên gấp bội. Kỹ sư giỏi phát hiện sớm bài toán NP-đầy đủ để chuyển sang phép xấp xỉ hay cắt tỉa."
    ),
}

for lid, (tbl_html, say_txt) in TOC_P9_TABLES.items():
    p = next((ROOT / "lessons/toc").glob(f"{lid}_*.yaml"))
    txt = p.read_text(encoding="utf-8")
    if "quy mô bài toán" in txt or "quy mô mẫu ghép" in txt or "quy mô độ dài chuỗi" in txt or "quy mô phân cấp" in txt or "quy mô trình phân tích" in txt or "quy mô bộ nhớ phụ trợ" in txt or "quy mô mô hình tính toán" in txt or "quy mô kiểm thử chương trình" in txt or "quy mô bài toán kiểm chứng" in txt:
        continue
    # insert right before '- id: quiz'
    marker = "- id: quiz\n"
    assert marker in txt, f"No quiz marker in {p.name}"
    block = (
        "  - clear: true\n"
        "    show: |\n"
        f"      {tbl_html}\n"
        f"    say: {say_txt}\n"
    )
    p.write_text(txt.replace(marker, block + marker, 1), encoding="utf-8")

# 4. Append crisp recap additions cleanly for ALL 20 tight Stage 10 lessons (target >= 1650 words!)
BOOSTS = {
    "lessons/toc/L00_chuoi_ngon_ngu.yaml": (
        " Nắm vững ngôn ngữ là tập hợp các chuỗi giúp bạn nhìn bài toán quyết định thật rạch ròi. Thay vì viết điều kiện mơ hồ, ta mô tả chính xác tập mọi chuỗi hợp lệ mà thuật toán phải chấp nhận. Cách đặt nền tảng hình thức này loại trừ sai sót biên ngay từ bảng đặc tả đầu tiên. Khi hệ thống thực tế xử lý hàng triệu tên đăng nhập hay thông điệp mạng mỗi ngày, quy tắc xác thực chuỗi càng chặt càng tránh được lỗ hổng bảo mật. Mọi khái niệm nâng cao về máy trạng thái, văn phạm và tính khả quyết ở các bài sau đều xây dựng trực tiếp trên ngôn ngữ hình thức giản dị này."
    ),
    "lessons/toc/L01_dfa.yaml": (
        " Điểm mạnh nổi bật của máy trạng thái hữu hạn đơn định là bộ nhớ chỉ đúng bằng một trạng thái hiện tại, dù chuỗi vào dài hàng tỉ ký tự. Mỗi bước đọc ký tự chỉ tra bảng chuyển đúng một lần trong thời gian hằng số cực nhanh. Chính vì tính tất định và chi phí cố định đó, máy hữu hạn là xương sống của phần cứng mạng tốc độ cao, bộ phân tích từ vựng trình biên dịch và giao thức truyền thông. Nhớ kỹ điều kiện mỗi trạng thái phải định nghĩa đủ mũi tên cho toàn bộ bảng chữ cái để tránh treo máy khi gặp ký tự bất ngờ."
    ),
    "lessons/toc/L02_nfa_tap_con.yaml": (
        " Hiểu rõ phép dựng tập con giúp bạn dung hoà dễ dàng giữa sự gọn nhẹ khi viết đặc tả và tốc độ khi chạy máy. Khi thiết kế mẫu nhận diện, hãy cứ tư duy theo hướng không đơn định và dùng cạnh rỗng để giữ mô hình thật tự nhiên. Sau đó máy tính sẽ tự động gộp tập hợp các nhánh thành trạng thái cụ thể khi biên dịch mẫu. Lưu ý trường hợp cực hạn khi số lượng trạng thái bùng nổ theo hàm mũ như bài toán ký tự thứ k từ cuối để chủ động mô phỏng tập trạng thái trực tiếp trên bộ nhớ nhỏ."
    ),
    "lessons/toc/L07_mo_ho_phan_tich.yaml": (
        " Trong thực hành xây dựng trình biên dịch hoặc bộ phân tích công thức, khử mơ hồ không phải bước trang trí mà là điều kiện tiên quyết để mã chạy ra một nghĩa duy nhất. Nếu bỏ sót một xung đột độ ưu tiên hay kết hợp giữa hai toán tử cùng tầng, hai lập trình viên khác nhau sẽ nhận hai giá trị hoàn toàn sai khác cho cùng một dòng lệnh. Phân tầng quy tắc theo độ ưu tiên từ yếu nhất tới mạnh nhất, kèm hướng đệ quy bên trái cho kết hợp trái, luôn là công thức chuẩn giúp văn phạm vừa sáng rõ vừa dễ bảo trì lâu dài."
    ),
    "lessons/toc/L09_may_turing.yaml": (
        " Ý nghĩa lớn nhất của mô hình máy Turing không nằm ở tốc độ thực thi mà ở việc vạch ra bản chất tối giản nhất của mọi thuật toán. Chỉ cần băng nhớ dài tuỳ ý và đầu đọc ghi dịch từng ô một theo hữu hạn quy tắc, cỗ máy này làm được mọi phép tính mà siêu máy tính hiện đại thực hiện được. Ngược lại, mọi giới hạn không vượt nổi của máy Turing cũng chính là rào cản tuyệt đối của toàn bộ khoa học máy tính. Nhớ luôn ba kết cục nhận, từ chối và lặp vô tận để không đánh đồng máy dừng với mọi máy nói chung."
    ),
    "lessons/plc/L00_cac_pha_bien_dich.yaml": (
        " Chia bộ biên dịch thành các pha rạch ròi với cấu trúc dữ liệu trung gian thống nhất giúp kiểm soát độ phức tạp của toàn bộ ngôn ngữ lập trình. Mỗi pha giải quyết trọn vẹn một lớp vấn đề từ tách ký tự, dựng cây cấu trúc, tới đối chiếu ngữ nghĩa và tối ưu mã máy."
    ),
    "lessons/plc/L03_cay_cu_phap.yaml": (
        " Cây cú pháp trừu tượng giúp toàn bộ bộ biên dịch không còn lệ thuộc vào dấu ngoặc thừa hay cách thụt lề văn bản nguồn. Từng nút cây phản ánh chính xác phép toán cha cần giá trị từ các nút con bên dưới. Lập trình bộ phân tích đệ quy tách rời từng tầng ưu tiên sẽ đảm bảo phép nhân luôn gắn chặt hơn phép cộng, còn phép mũ giữ đúng hướng kết hợp từ phải sang trái. Khi duyệt hậu tố qua cây, phần mềm tự động tôn trọng thứ tự tính toán chuẩn mực mà không cần thêm bất kỳ bảng dấu ngoặc phụ nào trong giai đoạn chạy."
    ),
    "lessons/plc/L04_pham_vi.yaml": (
        " Môi trường liên kết chuỗi cha giúp tách biệt rạch ròi khái niệm tên biến và vùng nhớ đang lưu giá trị tại mỗi thời điểm chạy hàm. Nhờ phạm vi tĩnh, người đọc mã luôn xác định được ngay một biến tự do trỏ tới dòng khai báo nào bằng cách nhìn cấu trúc lồng nhau trên văn bản. Điều này giữ nguyên ý nghĩa hàm dù hàm đó được truyền đi hay gọi lại ở hàng trăm vị trí khác nhau trong phần mềm quy mô lớn. Hiểu rõ mô hình khung môi trường chuỗi cha cũng giúp bạn lý giải chính xác vì sao vòng đời biến địa phương luôn an toàn."
    ),
    "lessons/plc/L06_suy_luan_kieu.yaml": (
        " Cơ chế suy luận kiểu kết hợp sự gọn nhẹ không cần khai báo dài dòng với màng lưới an toàn kiểm chứng toàn bộ chương trình trước lúc chạy. Trình biên dịch tự gom các phương trình ràng buộc từ mỗi phép cộng, gọi hàm hay nhánh điều kiện rồi giải lần lượt qua thuật toán hợp nhất. Kiểm tra xuất hiện đóng vai trò chốt chặn tinh tế nhằm từ chối tức thì các kiểu vòng tự tham chiếu vô hạn. Nếu một lời gọi truyền sai kiểu dữ liệu ngay cả ở nhánh ít chạy, hệ thống vẫn báo lỗi chính xác từng vị trí ngay trên máy lập trình viên."
    ),
    "lessons/plc/L07_bao_dong.yaml": (
        " Hiểu sâu cấu tạo cặp mã kèm môi trường của bao đóng giải toả mọi bối rối khi lập trình hàm bậc cao, sự kiện bất đồng bộ hay callback. Mỗi lời gọi hàm bao bọc ngoài sinh ra một không gian biến riêng biệt không đụng chạm các bản sao trước đó. Đồng thời vì bao đóng giữ tham chiếu trực tiếp tới biến chứ không chụp ảnh giá trị tại lúc khởi tạo, hãy hết sức cảnh giác khi tạo nhiều hàm con bên trong một vòng lặp dùng chung một biến đếm. Khai báo phạm vi biến mới cho từng vòng lặp là thói quen an toàn tuyệt đối trong ngôn ngữ hiện đại."
    ),
    "lessons/plc/L09_truyen_tham_so.yaml": (
        " Phân biệt rõ ba cơ chế truyền tham số giúp lập trình viên không bao giờ bất ngờ khi hàm thay đổi ngầm dữ liệu của bên gọi. Với truyền giá trị thuần tuý, biến gốc ngoài hàm luôn được bảo toàn nhưng chi phí sao chép cấu trúc lớn khá tốn kém. Với truyền chia sẻ tham chiếu đối tượng như trong Python hay Java, sửa thuộc tính bên trong đối tượng hiện ngay ra ngoài, nhưng gán lại tên tham số chỉ đổi nhãn cục bộ. Đọc rõ quy ước truyền tham số và kiểm tra đột biến ngoài ý muốn là nguyên tắc vàng khi thiết kế hàm thư viện dùng chung."
    ),
    "lessons/plc/L10_sinh_ma_ngan_xep.yaml": (
        " Máy ảo ngăn xếp giữ tập lệnh máy cực kỳ gọn nhẹ vì phần lớn phép toán không cần ghi địa chỉ thanh ghi dài dòng. Bằng cách kết hợp duyệt hậu tố cây cú pháp trừu tượng, trình biên dịch chỉ việc sinh mã cho vế trái trước, vế phải sau, rồi xuất đúng một lệnh toán học ở cuối. Mọi biểu thức lồng sâu hàng chục cấp đều tự nhiên tìm thấy toán hạng nằm đúng thứ tự ở hai vị trí trên cùng của ngăn xếp. Nguyên tắc kiểm chặt thứ tự toán hạng trừ và chia giúp mọi máy ảo chạy đa nền tảng đều cho kết quả nhất quán tuyệt đối."
    ),
    "lessons/plc/L11_toi_uu.yaml": (
        " Sức mạnh của các pha tối ưu hiện đại đến từ sự kết hợp kỷ luật giữa phép gập hằng, kéo biểu thức bất biến và cắt bỏ mã chết nối tiếp nhau. Khi tối ưu biểu thức hằng ở vòng trước mở khoá điều kiện nhánh luôn đúng, pha kế tiếp lập tức phát hiện cả khối mã thừa phía bên kia để quét sạch. Tuy nhiên quy tắc bất di bất dịch là bảo toàn toàn vẹn hành vi quan sát được và hiệu ứng phụ cho mọi đầu vào hợp lệ. Mọi phép tối ưu đánh đổi độ chính xác hoặc làm thay đổi lỗi tràn số nguyên đều bị coi là sai về mặt ngữ nghĩa."
    ),
    "lessons/plc/L12_lap_trinh_ham.yaml": (
        " Kết hợp hàm thuần và cấu trúc dữ liệu bất biến dùng chung nút cây tạo nên mô hình lập trình song song cực kỳ an toàn cho hệ thống nhiều luồng. Nhờ các nút cũ không bao giờ bị sửa tại chỗ, luồng đọc đang duyệt phiên bản trước hoàn toàn yên tâm mà không cần xin khoá."
    ),
    "lessons/par/L12_tinh_huong_8_gpu.yaml": (
        " Khi nhận được kết quả chậm bất ngờ trên cụm nhiều thẻ đồ hoạ, bước đầu tiên không bao giờ là đặt mua thêm phần cứng. Hãy tách từng phần của chu kỳ huấn luyện trên một thẻ chuẩn, đo kỹ xem tổng thời gian bị trói ở khâu tính toán song song hay ở khâu nạp dữ liệu tuần tự. Khi phần tuần tự chiếm một phần tư chu kỳ thì nâng cấp từ tám lên mười sáu thẻ gần như không cải thiện gì so với chi phí bỏ ra. Chỉ sau khi tối ưu ống dẫn dữ liệu và chứng minh nút thắt tuần tự đã thu nhỏ rõ rệt, việc mở rộng phần cứng mới mang lại hiệu quả xứng đáng."
    ),
}

# Apply non-focus say appends safely (keep focus unchanged since focus is None on all 15 above)
for rel_p, extra in BOOSTS.items():
    p = ROOT / rel_p
    doc = yaml.safe_load(p.read_text(encoding="utf-8"))
    rec0 = next(sc["steps"][0] for sc in doc["scenes"] if sc["id"] == "recap")
    assert rec0.get("focus") is None, f"Unexpected focus on {rel_p}"
    old_say = rec0["say"].strip()
    if extra.strip() in old_say:
        continue
    new_say = old_say + extra
    raw = p.read_text(encoding="utf-8")
    # replace exact recap step 0 say line
    replaced = False
    out_lines = []
    in_recap = False
    seen_first_step = False
    for ln in raw.splitlines():
        if ln.strip() == "- id: recap":
            in_recap = True
        elif in_recap and ln.startswith("  - show:"):
            seen_first_step = True
        elif in_recap and seen_first_step and ln.startswith("    say:") and not replaced:
            # quote safely if ':' inside
            q = new_say.replace("'", "''")
            out_lines.append(f"    say: '{q}'")
            replaced = True
            continue
        out_lines.append(ln)
    assert replaced, f"Could not update recap0 say in {rel_p}"
    p.write_text("\n".join(out_lines) + "\n", encoding="utf-8")

# 5. HCI L11 & L12 (both have focus arrays on recap0 and recap1!)
replace_exact(
    ROOT / "lessons/hci/L11_tinh_huong_canh_bao.yaml",
    """    focus:
    - 1
    - 1
    - 2
    - 2
    - 2
    - 2
    - 2
    say: Tổng kết bài học tình huống, thảm hoạ phát nhầm cảnh báo là hồi chuông cảnh tỉnh về trách nhiệm của người thiết kế giao diện. Ta luôn phải xây dựng nhiều lớp phòng thủ độc lập và kiểm chứng chúng qua những tình huống áp lực cao. Thử lúc bình tĩnh khó lộ lỗi giao diện. Diễn tập kịch bản áp lực trên hệ thống hàng triệu người lộ rõ 3 cái bẫy danh sách chung, hộp hỏi và thiếu mẫu huỷ. Mỗi lớp bảo vệ cần tách biệt rõ về kênh, màu sắc nhận diện và người duyệt độc lập trên màn hình riêng. Nhờ vậy sai sót cá nhân sẽ bị chặn lại trước khi tin nhắn rời khỏi hệ thống. Đây là bài học nền tảng cho mọi giao diện quan trọng nơi một cú bấm nhầm có thể gây hậu quả cho hàng triệu người dùng.""",
    """    focus:
    - 1
    - 1
    - 2
    - 2
    - 2
    - 2
    - 2
    - 2
    - 2
    - 2
    - 2
    - 2
    - 2
    - 2
    say: Tổng kết bài học tình huống, thảm hoạ phát nhầm cảnh báo là hồi chuông cảnh tỉnh về trách nhiệm của người thiết kế giao diện. Ta luôn phải xây dựng nhiều lớp phòng thủ độc lập và kiểm chứng chúng qua những tình huống áp lực cao. Thử lúc bình tĩnh khó lộ lỗi giao diện. Diễn tập kịch bản áp lực trên hệ thống hàng triệu người lộ rõ 3 cái bẫy danh sách chung, hộp hỏi và thiếu mẫu huỷ. Mỗi lớp bảo vệ cần tách biệt rõ về kênh, màu sắc nhận diện và người duyệt độc lập trên màn hình riêng. Nhờ vậy sai sót cá nhân sẽ bị chặn lại trước khi tin nhắn rời khỏi hệ thống. Đây là bài học nền tảng cho mọi giao diện quan trọng nơi một cú bấm nhầm có thể gây hậu quả cho hàng triệu người dùng. Trong ca trực khẩn cấp thực tế, người vận hành không đủ thời gian đọc dòng chữ nhỏ giống hệt nhau trên cùng một nền màu. Thiết kế tách hai vùng làm việc thật và thử nghiệm giúp bộ não nhận ra ngay trạng thái hiện tại chỉ bằng màu sắc và bố cục. Hơn nữa việc soạn sẵn mẫu thông báo đính chính giúp đội phản ứng nhanh giảm từ gần bốn mươi phút xuống dưới vài phút quý giá. Cuối cùng mọi quy trình xác nhận hai người chỉ phát huy tác dụng khi người thứ hai xem được bản xem trước độc lập hoàn toàn với tác vụ gửi. Đừng bao giờ phó mặc an toàn cộng đồng cho một dòng cảnh báo nhỏ xíu dễ bị bấm lướt qua theo thói quen.""",
)
replace_exact(
    ROOT / "lessons/hci/L11_tinh_huong_canh_bao.yaml",
    """    focus:
    - 1
    - 1
    say: Ở bài 12 tới, ta sẽ bước vào bài tổng kết hành trình lịch sử về các chuẩn tiếp cận web giúp mọi người đều tiếp cận được không gian số. Hẹn gặp bạn ở video tiếp theo.""",
    """    focus:
    - 1
    - 1
    - 1
    - 1
    - 1
    - 1
    say: Ở bài 12 tới, ta sẽ bước vào bài tổng kết hành trình lịch sử về các chuẩn tiếp cận web giúp mọi người đều tiếp cận được không gian số. Ta sẽ chứng kiến sự chuyển dịch từ mười bốn lời khuyên chung chung sang hàng loạt tiêu chí đo lường được bằng con số chính xác. Nhờ những thay đổi này, người khiếm thị dùng trình đọc màn hình hay người vận động khó khăn trên thiết bị di động nhỏ gọn đều sử dụng sản phẩm công bằng hơn. Đây cũng là mảnh ghép hoàn thiện bức tranh thiết kế hướng về con người trong suốt mười hai bài học vừa qua. Hãy chuẩn bị giấy bút để cùng nhìn lại toàn bộ hành trình phát triển đầy cảm hứng này. Hẹn gặp bạn ở video tiếp theo.""",
)
replace_exact(
    ROOT / "lessons/hci/L12_hanh_trinh_wcag.yaml",
    """    focus:
    - 1
    - 1
    - 2
    - 2
    say: Tổng kết toàn bộ khoá học Tương tác người máy, chúng ta đã đi từ cách nhìn lỗi do thiết kế và mô hình tâm trí, qua các định luật đo được, tới chuẩn tiếp cận quốc tế. Thiết kế tốt không phải là làm cho đẹp mắt, mà là xây dựng sự thấu cảm và trách nhiệm bảo vệ người dùng. Từ 65 điểm kiểm năm 1999 tới 86 tiêu chí đo được năm 2023 cho màn hình nhỏ và đích 24 điểm ảnh. Công cụ tự động chỉ kiểm được một phần trên web lớn.""",
    """    focus:
    - 1
    - 1
    - 2
    - 2
    - 2
    - 2
    - 2
    say: Tổng kết toàn bộ khoá học Tương tác người máy, chúng ta đã đi từ cách nhìn lỗi do thiết kế và mô hình tâm trí, qua các định luật đo được, tới chuẩn tiếp cận quốc tế. Thiết kế tốt không phải là làm cho đẹp mắt, mà là xây dựng sự thấu cảm và trách nhiệm bảo vệ người dùng. Từ 65 điểm kiểm năm 1999 tới 86 tiêu chí đo được năm 2023 cho màn hình nhỏ và đích 24 điểm ảnh. Công cụ tự động chỉ kiểm được một phần trên web lớn. Muốn đạt chuẩn thực chất, đội ngũ phát triển vẫn cần kiểm tra điều hướng bằng bàn phím thật và thử cùng người dùng sử dụng công nghệ hỗ trợ. Mỗi tiêu chí về độ tương phản, dàn dòng và kích thước vùng chạm đều có cơ sở đo lường cụ thể giúp sản phẩm phục vụ bền vững.""",
)
replace_exact(
    ROOT / "lessons/hci/L12_hanh_trinh_wcag.yaml",
    """    focus:
    - 1
    - 1
    say: Tư duy lớn nhất bạn cần mang theo là công nghệ chỉ thực sự có ý nghĩa khi phục vụ bình đẳng tất cả mọi người. Chúc mừng bạn đã hoàn thành trọn vẹn toàn bộ khoá học Tương tác người máy!""",
    """    focus:
    - 1
    - 1
    - 1
    - 1
    - 1
    - 1
    say: Tư duy lớn nhất bạn cần mang theo là công nghệ chỉ thực sự có ý nghĩa khi phục vụ bình đẳng tất cả mọi người. Từ những nguyên lý nhỏ như chọn kích thước nút theo định luật trỏ hay giữ trật tự thực đơn quen thuộc, ta xây nên phần mềm an toàn hơn. Đừng đợi tới ngày nghiệm thu mới kiểm tra khả năng tiếp cận hay phòng chống lỗi, mà hãy tích hợp chúng ngay từ bản phác thảo đầu tiên. Kiến thức thực hành cùng mười ba bài thực nghiệm tự chấm sẽ là hành trang tin cậy để bạn tự tin thiết kế mọi sản phẩm số chất lượng cao. Chúc mừng bạn đã hoàn thành trọn vẹn toàn bộ khoá học Tương tác người máy!""",
)

# Check lint + word counts across all 80 Stage 10 lessons!
errs = warns = 0
for c in ("toc", "plc", "par", "hci", "sep", "cas"):
    for p in sorted((ROOT / "lessons" / c).glob("L*.yaml")):
        sp = lv.load_spec(p)
        res = lv.lint(sp, quiet=True)
        w = sum(len((s.get("say") or "").split()) for sc in sp["scenes"] for s in sc["steps"])
        errs += len(res.errors)
        warns += len(res.warnings)
        if res.errors or res.warnings or w < 1620:
            print(f"{c.upper()}:{sp['id']} w={w} FAIL={len(res.errors)} WARN={len(res.warnings)} {res.errors[:2]} {res.warnings[:2]}")
print(f"STAGE 10 SUMMARY (80 lessons): FAIL={errs}, WARN={warns}", flush=True)
assert errs == 0 and warns == 0
