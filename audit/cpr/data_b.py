"""Đặc tả dữ liệu CPR L05–L09."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "audit" / "review"))
import af2_kit as ak  # noqa: E402


def lessons():
    # ────────────────── L05: Con trỏ, mảng và số học bước nhảy con trỏ ──────────────────
    l05 = {
        "id": "L05",
        "slug": "so_hoc_con_tro",
        "title": "Con trỏ, mảng và số học bước nhảy con trỏ",
        "next_title": "Bộ nhớ động trên vùng nhớ mở và bốn lỗi kinh điển",
        "assumes": ["cpr_con_tro", "cpr_ub"],
        "objectives": [
            "Tính độ lệch byte thật khi cộng thêm k vào con trỏ kiểu T* (k × sizeof(T))",
            "Dùng từ khoá const đúng chỗ để bảo vệ dữ liệu chỉ đọc khi truyền mảng",
            "So sánh truy cập chỉ số a[i] và bước nhảy con trỏ *(p + i)",
        ],
        "covers": [(1, "formula"), (2, "example"), (3, "check")],
        "hook_title": "Vì sao cộng 1 vào con trỏ không hề nhảy đúng 1 byte?",
        "hook_html": (
            "<p>Cho con trỏ <code>int *p</code> và thực hiện <code>p + 3</code>. Địa chỉ không tăng thêm <b>3 byte</b> mà nhảy vọt thêm <b>12 byte</b>.</p>"
            "<p>Con trỏ luôn nhảy theo bội số kích thước phần tử <code>sizeof(*p)</code> để trỏ trúng đầu phần tử kế tiếp.</p>"
        ),
        "hook_say": (
            "Chào bạn, ở bài trước bạn đã biết con trỏ giữ địa chỉ ô nhớ. "
            "Nếu lấy một con trỏ số nguyên bốn bai rồi cộng thêm ba, địa chỉ trong bộ nhớ không tăng ba bai mà nhảy hẳn mười hai bai. "
            "Cơ chế bước nhảy tự động nhân theo kích thước phần tử này giúp ngôn ngữ C duyệt qua các phần tử mảng cực kỳ chính xác và nhanh gọn. Tuy nhiên nhầm lẫn giữa phần tử và bai lại là nguồn cơn của rất nhiều lỗi vượt biên."
        ),
        "hook_checks": ["alg.cpr_ptr_offset(3, 4) == 12"],
        "prereq_steps": [
            ak.st(
                ak.table(
                    ["kiến thức nền đã học", "vai trò ở bài này"],
                    [
                        ["Mỗi phần tử int = 4 byte, double = 8 byte (L00)", "Độ rộng một bước nhảy bằng kích thước kiểu mà con trỏ trỏ tới"],
                        ["Biến con trỏ & và * (L04)", "Tên mảng khi truyền vào hàm tự chuyển thành địa chỉ phần tử đầu tiên"],
                    ],
                ),
                "Ta nối tiếp bài 0 và bài 4 để làm rõ bản chất liên kết giữa mảng và con trỏ. Độ dài mỗi bước dịch chuyển luôn phụ thuộc vào kích thước kiểu dữ liệu đích đang trỏ tới. Ngoài ra khi đưa tên mảng làm đối số gọi hàm, trình biên dịch chỉ truyền địa chỉ của phần tử đầu tiên.",
                clear=True,
            )
        ],
        "sym_steps": [
            ak.st(
                ak.table(
                    ["ký hiệu mới", "ý nghĩa"],
                    [
                        ["<code>*(p + i)</code>", "Nhảy <code>i × sizeof(*p)</code> byte từ <code>p</code> rồi đọc phần tử thứ <code>i</code> (giống hệt <code>a[i]</code>)"],
                        ["<code>const int *p</code>", "Con trỏ chỉ đọc dữ liệu đích: hàm được xem mảng nhưng bị cấm sửa phần tử"],
                        ["<code>(const char *)p</code>", "Ép sang con trỏ 1 byte để tính khoảng cách địa chỉ theo đúng đơn vị byte"],
                    ],
                ),
                "Có ba quy ước quan trọng trong số học con trỏ. Biểu thức cộng bước nhảy tương đương với dấu ngoặc vuông chỉ số mảng. Từ khoá bảo vệ chỉ đọc cấm hàm sửa mảng nguồn, còn ép sang con trỏ một bai giúp đo đúng khoảng cách bai.",
                focus=[0, "1.2", "1.3", "1.4"],
                clear=True,
            )
        ],
        "intuition_title": "Bước nhảy p + 0, p + 1, p + 2, p + 3 trên mảng int 4 byte",
        "intuition_steps": [
            ak.st(
                ak.svg_wrap(
                    960, 195,
                    ak.svg_rect(40, 45, 200, 95, "p + 0 (+0 B)", "a[0] = 10", ak.C_BLUE)
                    + ak.svg_rect(265, 45, 200, 95, "p + 1 (+4 B)", "a[1] = 20", ak.C_BLUE)
                    + ak.svg_rect(490, 45, 200, 95, "p + 2 (+8 B)", "a[2] = 30", ak.C_BLUE)
                    + ak.svg_rect(715, 45, 200, 95, "p + 3 (+12 B)", "a[3] = 40", ak.C_GREEN),
                ),
                "Nhìn bốn ô nhớ kề nhau: phần tử không nằm tại độ lệch không bai, phần tử một tại cộng bốn bai, phần tử hai tại cộng tám bai và phần tử ba tại cộng mười hai bai. "
                "Mỗi lần tăng con trỏ một đơn vị, địa chỉ thực sự dịch chuyển đúng bốn bai sang đầu phần tử kế tiếp. Phép cộng ba vào con trỏ số nguyên bốn bai tương đương đi thẳng mười hai bai tới đúng đầu phần tử thứ ba.",
                clear=True,
            )
        ],
        "formula_title": "Công thức số học con trỏ chuẩn C",
        "formula_steps": [
            ak.st(
                ak.box(
                    "<p>Với con trỏ kiểu <code>T *p</code> và số nguyên $k$:</p>"
                    "<p>địa chỉ(p + k) = địa chỉ(p) + k × sizeof(T)</p>"
                    "<p>Ví dụ: với <code>int</code> 4 byte, k=3 cho +12 byte; với double 8 byte, k=3 cho +24 byte.</p>",
                    "key",
                ),
                "Công thức chuẩn rất rõ ràng: dịch chuyển theo đơn vị phần tử nhân với kích thước của mỗi phần tử. Với số nguyên bốn bai, bước nhảy ba dịch chuyển mười hai bai vì ba nhân bốn bằng mười hai. Với số thực tám bai, bước nhảy ba dịch chuyển hai mươi bốn bai vì ba nhân tám bằng hai mươi bốn. Khi trừ hai con trỏ cùng mảng, trình biên dịch tự chia lại cho kích thước phần tử.",
                clear=True,
            )
        ],
        "formula_checks": ["alg.cpr_ptr_offset(3, 4) == 12", "alg.cpr_ptr_offset(3, 8) == 24"],
        "example_title": "Chạy thật trên GCC: đo khoảng cách byte và tổng hàm chỉ đọc const",
        "example_items": [
            {
                "type": "r3",
                "say": "Ta giải mã trước ba quy ước quan trọng dùng trong chương trình mẫu. Hàm tổng nhận con trỏ chỉ đọc ngăn sửa mảng gốc. Kiểu hiệu con trỏ có dấu từ thư viện chuẩn định nghĩa hiệu hai con trỏ và in ra bằng mã phần trăm t d, sau khi ép về con trỏ một bai để đo khoảng cách thật.",
                "rows": [
                    ["<code>const int *a, size_t n</code>", "Truyền mảng vào hàm: luôn kèm độ dài <code>n</code> và gắn <code>const</code> chống sửa nhầm"],
                    ["<code>#include &lt;stddef.h&gt;</code> / <code>ptrdiff_t</code> / <code>%td</code>", "Kiểu có dấu giữ hiệu hai con trỏ cùng mảng và mã in trong <code>printf</code>"],
                    ["<code>(ptrdiff_t)((const char *)(p + 3) - (const char *)p)</code>", "Ép sang con trỏ 1 byte rồi trừ để ra đúng khoảng cách byte"],
                ],
                "focus": [0, 1, 2],
            },
            {
                "type": "code",
                "pid": "p1",
                "title": "Đo độ lệch byte của p+3 với int và double, cùng sum_const",
                "say": "Chương trình thực nghiệm đo trực tiếp hiệu số bai thật giữa con trỏ gốc và con trỏ đã cộng ba trên hai kiểu dữ liệu. Tiếp theo nó gọi hàm cộng tổng mảng chỉ đọc qua từng bước nhảy để đối chiếu lại kết quả.",
                "out_say": "Kết quả chạy thật xác nhận bước nhảy ba trên kiểu bốn bai đúng bằng mười hai bai. Trên kiểu tám bai mức dịch đúng hai mươi bốn bai, và tổng bốn phần tử trả về chính xác một trăm.",
            },
        ],
        "progs": {
            "p1": {
                "code": (
                    "#include <stdio.h>\n"
                    "#include <stddef.h>\n"
                    "static int sum_const(const int *a, size_t n) {\n"
                    "    int s = 0;\n"
                    "    for (size_t i = 0; i < n; i++) { s += *(a + i); }\n"
                    "    return s;\n"
                    "}\n"
                    "int main(void) {\n"
                    "    int ai[4] = {10, 20, 30, 40};\n"
                    "    double ad[4] = {1.0, 2.0, 3.0, 4.0};\n"
                    "    ptrdiff_t d_int = (const char *)(ai + 3) - (const char *)ai;\n"
                    "    ptrdiff_t d_dbl = (const char *)(ad + 3) - (const char *)ad;\n"
                    '    printf("d_int=%td d_dbl=%td sum=%d\\n", d_int, d_dbl, sum_const(ai, 4));\n'
                    "    return 0;\n"
                    "}"
                ),
                "expect": "d_int=12 d_dbl=24 sum=100",
            },
            "p2": {
                "code": (
                    "#include <stdio.h>\n"
                    "static size_t param_sizeof(const int *p) { return sizeof(p); }\n"
                    "int main(void) {\n"
                    "    int arr[10] = {0};\n"
                    '    printf("outer=%zu param=%zu\\n", sizeof(arr), param_sizeof(arr));\n'
                    "    return 0;\n"
                    "}"
                ),
                "expect": "outer=40 param=8",
            },
        },
        "example_checks": ["alg.cpr_ptr_offset(3, 4) == 12", "alg.cpr_ptr_offset(3, 8) == 24"],
        "check_title": "Kiểm chứng kích thước mảng khi truyền qua hàm (array decay)",
        "check_items": [
            {
                "type": "code",
                "pid": "p2",
                "title": "Ngoài hàm sizeof(arr)=40; bên trong hàm chỉ nhận con trỏ 8 byte",
                "say": "Ở bài 0 ta từng lưu ý về kích thước mảng bên ngoài và bên trong hàm. Giờ ta chạy thật để thấy rõ: bên ngoài đo đủ bốn mươi bai, còn bên trong hàm tham số đã thành con trỏ nên đo được đúng tám bai.",
                "out_say": "Đầu ra thật chứng minh lý do vì sao không bao giờ đo được độ dài mảng ở bên trong hàm bằng toán tử kích thước. Bên ngoài là mảng bốn mươi bai, bên trong là con trỏ tám bai nên bắt buộc phải truyền kèm số lượng phần tử.",
            }
        ],
        "check_checks": ["10 * 4 == 40"],
        "quymo_title": "Bảng quy mô: khoảng cách phần tử vs khoảng cách byte thật",
        "quymo_steps": [
            ak.st(
                ak.table(
                    ["bước nhảy k", "trên int * (4 byte)", "trên double * (8 byte)", "trên khối 64 byte"],
                    [
                        [ak.nowrap("k = 1 (×1)"), "+4 byte", "+8 byte", "+64 byte"],
                        [ak.nowrap("k = 100 (×100)"), "+400 byte", "+800 byte", "+6 400 byte"],
                        [ak.nowrap("k = 10 000 (×10 000)"), "+40 000 byte", "+80 000 byte", "+640 000 byte"],
                    ],
                ),
                "Nhìn bảng quy mô, khoảng cách bộ nhớ luôn tỉ lệ thuận với cả bước nhảy lẫn kích thước mỗi phần tử. "
                "Với một bước nhảy trên kiểu tám bai chỉ dịch tám bai. Khi tăng lên một trăm bước nhảy là tám trăm bai, và ở mức mười nghìn bước nhảy ta đã đi suốt tám mươi nghìn bai liên tiếp trong bộ nhớ.",
                focus=[0, "1.2", "1.3", "1.4"],
                clear=True,
            )
        ],
        "quymo_checks": ["alg.cpr_ptr_offset(10000, 4) == 40_000", "alg.cpr_ptr_offset(10000, 8) == 80_000"],
        "pitfall_steps": [
            ak.st(
                ak.box(
                    "<b>Lỗi 1: Dùng <code>sizeof(arr) / sizeof(arr[0])</code> bên trong hàm.</b> Vì tham số mảng tự suy biến thành con trỏ 8 byte, công thức đó cho kết quả sai (8/4 = 2)!<br>"
                    "<b>Lỗi 2: Cộng bước nhảy vượt quá sau phần tử <code>n</code>.</b> C chỉ cho phép tạo địa chỉ kết thúc ngay sau phần tử cuối (<code>a + n</code>), tuyệt đối không được giải tham chiếu nó.<br>"
                    "<b>Lỗi 3: Trừ hai con trỏ thuộc hai mảng tách biệt.</b> Phép trừ chỉ hợp lệ khi cả hai cùng nằm trên một mảng.",
                    "warn",
                ),
                "Có ba lỗi thường gặp về số học con trỏ. Gọi toán tử đo kích thước trên tham số mảng trong hàm sẽ cho kết quả sai. Ngoài ra cần tránh đọc phần tử ngay sau mảng và không trừ hai địa chỉ khác mảng.",
                clear=True,
            )
        ],
        "quiz_steps": [
            ak.st(
                "<ol><li>Con trỏ <code>double *p</code> đang ở địa chỉ 1000, vậy <code>p + 5</code> trỏ tới địa chỉ bao nhiêu (biết <code>sizeof(double) = 8</code>)?</li>"
                "<li>Vì sao hàm đọc mảng nên khai báo tham số <code>const int *a</code> thay vì <code>int *a</code>?</li></ol>",
                "Đến lượt bạn tự kiểm tra. "
                "Câu một, con trỏ số thực tám bai đang ở địa chỉ một nghìn thì vị trí cộng thêm năm nằm ở địa chỉ nào? "
                "Câu hai, vì sao hàm chỉ đọc mảng nên thêm từ khoá bảo vệ chỉ đọc vào tham số? Dừng vi-đê-ô và trả lời.",
                pause=20,
            ),
            ak.st(
                "<p>① 1000 + 5 × 8 = <b>1040</b>.</p>",
                "Đáp án câu một: năm phần tử nhân tám bai bằng bốn mươi bai, cộng một nghìn thành một nghìn không trăm bốn mươi.",
                clear=True,
            ),
            ak.st(
                "<p>② Thêm <code>const</code> để trình biên dịch chặn ngay ở bước biên dịch nếu hàm lỡ ghi đè mảng đầu vào.</p>",
                "Đáp án câu hai: khai báo chỉ đọc giúp trình biên dịch ngăn mọi thao tác sửa nhầm dữ liệu đầu vào.",
                clear=True,
            ),
        ],
        "quiz_checks": ["1000 + alg.cpr_ptr_offset(5, 8) == 1040"],
        "recap_steps": [
            ak.st(
                "<div class='chain'><span class='n'>p + k dịch k × sizeof(*p) byte</span><span class='a'>→</span>"
                "<span class='n'>Tên mảng truyền hàm → con trỏ (kèm n)</span><span class='a'>→</span>"
                "<span class='n'>Bảo vệ bằng const</span></div>",
                "Ghi nhớ chuỗi quy tắc quan trọng của bài 5. Mọi bước nhảy con trỏ đều nhân với kích thước phần tử đích. Truyền mảng vào hàm luôn phải truyền kèm biến độ dài và gắn từ khoá chỉ đọc cho đầu vào.",
                clear=True,
            )
        ],
        "lab_de": (
            "# Lab CPR L05 — Đo bước nhảy con trỏ và hàm mảng chỉ đọc const\n\n"
            "Viết chương trình C chuẩn C11 dùng mảng `int v[5] = {2, 4, 6, 8, 10}`, tính hiệu byte giữa `v + 4` và `v`, và tổng qua hàm `sum_ro(const int *a, size_t n)`, in đúng 2 dòng:\n"
            "1. `offset4=16`\n"
            "2. `sum=30`\n\n"
            "Chấm tự động:\n```bash\nbash labs/cham.sh CPR L05 duong_dan/bai_cua_ban.c\n```"
        ),
        "lab_sol": (
            "#include <stdio.h>\n"
            "#include <stddef.h>\n"
            "static int sum_ro(const int *a, size_t n) {\n"
            "    int s = 0;\n"
            "    for (size_t i = 0; i < n; i++) s += *(a + i);\n"
            "    return s;\n"
            "}\n"
            "int main(void) {\n"
            "    int v[5] = {2, 4, 6, 8, 10};\n"
            "    ptrdiff_t d = (const char *)(v + 4) - (const char *)v;\n"
            '    printf("offset4=%td\\n", d);\n'
            '    printf("sum=%d\\n", sum_ro(v, 5));\n'
            "    return 0;\n"
            "}\n"
        ),
    }

    # ────────────────── L06: Bộ nhớ Heap: malloc, calloc, realloc, free ──────────────────
    l06 = {
        "id": "L06",
        "slug": "cap_phat_dong_heap",
        "title": "Bộ nhớ Heap: malloc, calloc, realloc, free và 4 lỗi kinh điển",
        "next_title": "Kiểu ghép cấu trúc, bố cục bộ nhớ và danh sách liên kết",
        "assumes": ["cpr_con_tro", "cpr_ub"],
        "objectives": [
            "Phân biệt malloc (chưa xoá rác), calloc (gán 0) và realloc (mở rộng)",
            "Tính dung lượng rò rỉ bộ nhớ khi quên free trong vòng lặp quy mô lớn",
            "Tránh bốn lỗi: quên free, dùng sau free, free hai lần và không kiểm kết quả NULL",
        ],
        "covers": [(1, "sym"), (2, "quymo"), (3, "pitfalls")],
        "hook_title": "Quên trả lại 1 KB mỗi vòng lặp, bao lâu thì máy chủ hết RAM?",
        "hook_html": (
            "<p>Ở bài 2, ta thấy mảng 10 triệu số nguyên làm sập ngăn xếp. Giải pháp của C là xin vùng nhớ trên <b>vùng nhớ mở (Heap)</b> với dung lượng lớn và vòng đời tự kiểm soát.</p>"
            "<p>Nhưng nếu mỗi yêu cầu xin <b>1 024 byte</b> rồi quên trả lại, sau <b>1 000 000</b> yêu cầu, dịch vụ âm thầm rò rỉ mất <b>~1 GB RAM</b>.</p>"
        ),
        "hook_say": (
            "Chào bạn, ở bài 2 ta thấy ngăn xếp không chứa được mảng hàng chục mê-ga-bai. "
            "Hôm nay ta học cách xin bộ nhớ trên vùng nhớ mở với vòng đời do chính bạn quyết định. "
            "Tuy nhiên quyền tự do này cũng đi kèm trách nhiệm kỷ luật rất cao. Nếu quên trả lại dù chỉ một ki-lô-bai mỗi vòng lặp, dịch vụ chạy lâu dài sẽ rò rỉ hàng gi-ga-bai bộ nhớ và đột ngột ngừng hoạt động."
        ),
        "hook_checks": ["1000 * 1024 == 1_024_000", "1_000_000 * 1024 == 1_024_000_000"],
        "prereq_steps": [
            ak.st(
                ak.table(
                    ["nền tảng đã có", "áp dụng vào Heap"],
                    [
                        ["Biến cục bộ mất ngay khi hàm return (L02)", "Vùng nhớ động vẫn sống qua mọi lời gọi hàm tới khi được trả lại"],
                        ["Kiểm tra NULL trước khi giải tham chiếu (L04)", "Hàm xin bộ nhớ trả về NULL nếu hệ thống hết RAM"],
                    ],
                ),
                "Ta ghép kiến thức từ bài 2 và bài 4 để thiết kế vùng nhớ động an toàn. Khác với biến cục bộ mất ngay lúc hàm kết thúc, khối nhớ vùng mở tồn tại bền bỉ cho tới khi bạn gọi lệnh trả về. Tuy nhiên khi xin cấp phát luôn phải kiểm tra khác rỗng phòng khi hệ thống hết RAM.",
                clear=True,
            )
        ],
        "sym_steps": [
            ak.st(
                ak.table(
                    ["hàm chuẩn &lt;stdlib.h&gt;", "tác dụng"],
                    [
                        ["<code>malloc(bytes)</code>", "Xin <code>bytes</code> byte vùng nhớ mở, nội dung ban đầu <b>rác chưa xoá</b>"],
                        ["<code>calloc(n, sz)</code>", "Xin <code>n × sz</code> byte và <b>gán toàn bộ bằng 0</b> (tự kiểm tràn nhân)"],
                        ["<code>realloc(p, new_bytes)</code>", "Đổi kích thước vùng <code>p</code>; trả địa chỉ mới hoặc <code>NULL</code> nếu thất bại"],
                        ["<code>free(p)</code>", "Trả vùng nhớ về hệ thống; đặt ngay <code>p = NULL</code> sau đó"],
                    ],
                ),
                "Thư viện chuẩn cung cấp bốn hàm quản lý vùng nhớ động. Hai hàm xin cấp phát gồm hàm giữ nguyên rác cũ và hàm xoá sạch về không. Hai hàm còn lại dùng để đổi kích thước vùng đang chạy và giải phóng trả lại hệ thống.",
                introduces=["cpr_cap_phat_dong"],
                focus=[0, "1.2", "1.3", "1.4", "1.5"],
                clear=True,
            )
        ],
        "intuition_title": "Vòng đời khối vùng nhớ động: Xin → Kiểm → Dùng → Trả",
        "intuition_steps": [
            ak.st(
                ak.svg_wrap(
                    960, 200,
                    ak.svg_rect(25, 50, 200, 95, "1. calloc(n, sz)", "Xin khối trên vùng nhớ mở", ak.C_BLUE)
                    + ak.svg_arrow(225, 97, 290, 97, "")
                    + ak.svg_rect(290, 50, 185, 95, "2. if (!p)", "Kiểm khác NULL", ak.C_AMBER)
                    + ak.svg_arrow(475, 97, 535, 97, "")
                    + ak.svg_rect(535, 50, 180, 95, "3. Đọc / Ghi", "Đúng biên 0..n-1", ak.C_GREEN)
                    + ak.svg_arrow(715, 97, 770, 97, "")
                    + ak.svg_rect(770, 50, 170, 95, "4. free(p); p=NULL", "Trả sạch, chống treo", ak.C_GRAY),
                ),
                "Mọi khối nhớ động tốt đều phải đi trọn vòng đời bốn bước khép kín như trên sơ đồ. Đầu tiên ta xin cấp phát một địa chỉ từ vùng nhớ mở và lập tức kiểm tra địa chỉ khác rỗng. Sau khi đọc ghi xong trong phạm vi được phép, ta giải phóng vùng nhớ rồi gán ngay con trỏ về rỗng.",
                clear=True,
            )
        ],
        "formula_title": "Mẫu realloc an toàn không làm mất con trỏ gốc khi thiếu RAM",
        "formula_steps": [
            ak.st(
                ak.box(
                    "<p>Không viết <code>p = realloc(p, new_sz);</code>! Nếu cấp mới thất bại trả về <code>NULL</code>, bạn mất luôn địa chỉ cũ để giải phóng.</p>"
                    "<p><b>Mẫu chuẩn:</b> <code>int *tmp = realloc(p, new_sz); if (tmp == NULL) { free(p); return 1; } p = tmp;</code></p>",
                    "key",
                ),
                "Quy tắc vàng khi mở rộng kích thước là luôn hứng kết quả qua một con trỏ tạm. Vì khi thay đổi kích thước thất bại hàm sẽ trả về con trỏ rỗng mà không hề động chạm vùng nhớ cũ. Nếu hứng thẳng vào biến con trỏ cũ bạn sẽ đánh mất địa chỉ gốc mãi mãi. Nhờ giữ qua con trỏ tạm, ta dọn sạch được khối cũ rồi mới thoát lỗi an toàn.",
                clear=True,
            )
        ],
        "formula_checks": ["4 * 4 == 16", "4 * 8 == 32"],
        "example_title": "Chạy thật trên GCC: cấp bằng calloc, mở rộng bằng realloc và đếm cân bằng",
        "example_items": [
            {
                "type": "r3",
                "say": "Trước khi chạy mã, ta giải mã đủ bốn quy ước cấp phát động chuẩn. Thư viện chuẩn cung cấp hàm xin, xoá và mở rộng vùng nhớ. Cách viết rút gọn dấu chấm than kiểm tra ngay xem cấp phát có rỗng hay không. Giải phóng đi kèm gán rỗng khoá chặt lỗi dùng trỏ treo.",
                "rows": [
                    ["<code>#include &lt;stdlib.h&gt;</code>", "Khai báo <code>malloc</code>, <code>calloc</code>, <code>realloc</code>, <code>free</code>"],
                    ["<code>if (!p)</code> / <code>if (!tmp)</code>", "Dấu <code>!</code> phủ định: viết gọn của <code>p == NULL</code> khi cấp phát thất bại"],
                    ["<code>int *tmp = realloc(a, 6 * sizeof(int));</code>", "Mở rộng từ 4 lên 6 phần tử bằng biến tạm để giữ nguyên con trỏ cũ"],
                    ["<code>free(a); a = NULL;</code>", "Giải phóng và xoá ngay địa chỉ khỏi con trỏ để tránh lỗi dùng sau giải phóng"],
                ],
                "focus": [0, 1, 2, 3],
            },
            {
                "type": "code",
                "pid": "p1",
                "title": "Cấp phát 4 int, mở rộng lên 6 int, tính tổng và trả sạch",
                "say": "Đoạn mã dùng hàm cấp phát đã xoá sạch về không cho bốn số nguyên rồi gán giá trị mười đến bốn mươi. Tiếp theo chương trình gọi mở rộng lên sáu ô thông qua con trỏ tạm an toàn, gán tiếp hai ô cuối rồi tính tổng và giải phóng sạch.",
                "out_say": "Kết quả chạy thật chứng minh bốn giá trị đầu được bảo toàn nguyên vẹn sau khi mở rộng lên sáu phần tử. Tổng toàn mảng thu được bằng hai trăm mười và toàn bộ bộ nhớ đã được giải phóng an toàn.",
            },
        ],
        "progs": {
            "p1": {
                "code": (
                    "#include <stdio.h>\n"
                    "#include <stdlib.h>\n"
                    "int main(void) {\n"
                    "    int *a = calloc(4, sizeof(int));\n"
                    "    if (!a) return 1;\n"
                    "    for (int i = 0; i < 4; i++) a[i] = (i + 1) * 10;\n"
                    "    int *tmp = realloc(a, 6 * sizeof(int));\n"
                    "    if (!tmp) { free(a); return 1; }\n"
                    "    a = tmp; a[4] = 50; a[5] = 60;\n"
                    "    int s = 0; for (int i = 0; i < 6; i++) s += a[i];\n"
                    '    printf("n=6 sum=%d last=%d\\n", s, a[5]);\n'
                    "    free(a); a = NULL;\n"
                    '    printf("is_null=%d\\n", a == NULL);\n'
                    "    return 0;\n"
                    "}"
                ),
                "expect": "n=6 sum=210 last=60\nis_null=1",
            },
            "p2": {
                "code": (
                    "#include <stdio.h>\n"
                    "#include <stdlib.h>\n"
                    "int main(void) {\n"
                    "    int allocs = 0, frees = 0;\n"
                    "    for (int i = 0; i < 5; i++) {\n"
                    "        int *buf = malloc(1024);\n"
                    "        if (!buf) return 1;\n"
                    "        allocs++;\n"
                    "        buf[0] = i;\n"
                    "        free(buf); frees++;\n"
                    "    }\n"
                    '    printf("allocs=%d frees=%d leak=%d\\n", allocs, frees, allocs - frees);\n'
                    "    return 0;\n"
                    "}"
                ),
                "expect": "allocs=5 frees=5 leak=0",
            },
        },
        "example_checks": ["sum((i + 1) * 10 for i in range(6)) == 210"],
        "check_title": "Kiểm cân bằng: đếm số lần cấp phát phải bằng số lần giải phóng",
        "check_items": [
            {
                "type": "code",
                "pid": "p2",
                "title": "Mỗi vòng lặp ghép cặp 1 lần cấp với 1 lần trả → cân bằng = 0",
                "say": "Ở phần kiểm chứng, ta mô phỏng một vòng lặp năm lượt có cấp phát và giải phóng vùng nhớ để kiểm tra tính cân bằng. Vì mỗi lần cấp phát thành công đều đi kèm đúng một lần giải phóng nên tổng số khối còn giữ lại luôn bằng không.",
                "out_say": "Đầu ra thật ghi nhận năm lần cấp phát, năm lần giải phóng và độ chênh bằng không vì mọi khối đã được thu hồi đúng lúc.",
            }
        ],
        "check_checks": ["alg.cpr_heap_leak(5, 5) == 0"],
        "quymo_title": "Bảng quy mô: tốc độ rò rỉ RAM nếu quên giải phóng 1 KB mỗi lượt",
        "quymo_steps": [
            ak.st(
                ak.table(
                    ["số lượt rò rỉ (mỗi lần 1 024 byte)", "tổng bộ nhớ bị giữ lại", "hệ quả"],
                    [
                        [ak.nowrap("1 000 lượt (×1)"), "1 024 000 byte (~1 MB)", "Khó thấy bằng mắt thường khi thử nhỏ"],
                        [ak.nowrap("100 000 lượt (×100)"), "102 400 000 byte (~98 MB)", "RAM dịch vụ tăng đều theo thời gian"],
                        [ak.nowrap("1 000 000 lượt (×1 000)"), "1 024 000 000 byte (~977 MB)", "Nhân hệ điều hành ngắt dịch vụ vì cạn RAM"],
                    ],
                ),
                "Lỗi rò rỉ bộ nhớ thường lọt qua bài kiểm nhỏ một nghìn lần vì mới mất một mê-ga-bai. Nếu chỉ kiểm tra năm hoặc một trăm vòng lặp, lượng rò rỉ mới vài chục ki-lô-bai nên rất khó thấy. Lên tới một nghìn vòng đã mất một mê-ga-bai, và chạy một triệu lượt sẽ ngốn gần một gi-ga-bai khiến dịch vụ bị chấm dứt đột ngột.",
                focus=[0, "1.2", "1.3", "1.4"],
                clear=True,
            )
        ],
        "quymo_checks": ["alg.cpr_heap_leak(1000, 0) * 1024 == 1_024_000", "1_000_000 * 1024 == 1_024_000_000"],
        "pitfall_steps": [
            ak.st(
                ak.box(
                    "<b>1. Quên free (rò rỉ):</b> cấp phát rồi thoát hàm sớm ở nhánh lỗi trước khi xuống tới lệnh giải phóng.<br>"
                    "<b>2. Dùng sau giải phóng (use-after-free):</b> đọc/ghi qua con trỏ cũ sau khi vùng nhớ đã trả về hệ thống.<br>"
                    "<b>3. Giải phóng hai lần (double free):</b> gọi giải phóng cùng một địa chỉ hai lượt làm hỏng bộ cấp phát.<br>"
                    "<b>4. Không kiểm NULL:</b> ghi thẳng vào kết quả cấp phát khi máy cạn RAM.",
                    "warn",
                ),
                "Khi dùng vùng nhớ động có bốn lỗi rất dễ mắc. Đó là quên giải phóng ở nhánh thoát sớm và bỏ qua bước kiểm tra rỗng. Lỗi nặng hơn là dùng lại vùng nhớ đã trả hoặc giải phóng cùng địa chỉ hai lần.",
                clear=True,
            )
        ],
        "quiz_steps": [
            ak.st(
                "<ol><li>Hàm nào tự khởi tạo mọi byte cấp phát về 0: <code>malloc</code> hay <code>calloc</code>?</li>"
                "<li>Một hàm cấp 4 KB nhưng nhánh báo lỗi <code>return -1</code> quên gọi <code>free</code>; sau 250 000 lượt lỗi đó thì rò rỉ bao nhiêu MB (~1024 KB)?</li></ol>",
                "Đến lượt bạn tự kiểm tra. "
                "Câu một, giữa hai hàm xin vùng nhớ thì hàm nào tự động đặt toàn bộ các bai về không? "
                "Câu hai, nếu mỗi lượt nhánh lỗi rò bốn ki-lô-bai thì sau hai trăm năm mươi nghìn lượt sẽ mất khoảng bao nhiêu mê-ga-bai? Dừng vi-đê-ô và trả lời.",
                pause=20,
            ),
            ak.st(
                "<p>① <code>calloc</code> đặt toàn bộ vùng nhớ về 0 (khác với <code>malloc</code> giữ rác cũ).</p>",
                "Đáp án câu một: dùng hàm cấp phát tự xoá sạch về không khi cần vùng đệm sạch ngay lập tức để tránh đọc nhầm rác cũ.",
                clear=True,
            ),
            ak.st(
                "<p>② 250 000 × 4 KB = 1 000 000 KB ≈ <b>976,6 MB</b> (gần 1 GB).</p>",
                "Đáp án câu hai: hai trăm năm mươi nghìn nhân bốn ki-lô-bai bằng một triệu ki-lô-bai, xấp xỉ gần một gi-ga-bai.",
                clear=True,
            ),
        ],
        "quiz_checks": ["250_000 * 4 == 1_000_000"],
        "recap_steps": [
            ak.st(
                "<div class='chain'><span class='n'>calloc/malloc + kiểm NULL</span><span class='a'>→</span>"
                "<span class='n'>realloc qua biến tạm</span><span class='a'>→</span>"
                "<span class='n'>free ở mọi nhánh rồi gán NULL</span></div>",
                "Tổng kết chuỗi tư duy quản lý vùng nhớ mở để giữ sạch bộ nhớ. Luôn kiểm tra khác rỗng ngay sau khi cấp phát, mở rộng qua con trỏ tạm, và giải phóng trên mọi nhánh thoát rồi gán về rỗng.",
                clear=True,
            )
        ],
        "lab_de": (
            "# Lab CPR L06 — Cấp phát động, mở rộng realloc an toàn và giải phóng\n\n"
            "Viết chương trình C chuẩn C11 cấp 3 phần tử `int` bằng `calloc`, gán `{10, 20, 30}`, mở rộng bằng `realloc` an toàn lên 5 phần tử thêm `{40, 50}`, tính tổng và `free`, in đúng 2 dòng:\n"
            "1. `len=5 sum=150`\n"
            "2. `freed=1`\n\n"
            "Chấm tự động:\n```bash\nbash labs/cham.sh CPR L06 duong_dan/bai_cua_ban.c\n```"
        ),
        "lab_sol": (
            "#include <stdio.h>\n"
            "#include <stdlib.h>\n"
            "int main(void) {\n"
            "    int *p = calloc(3, sizeof(int));\n"
            "    if (!p) return 1;\n"
            "    p[0] = 10; p[1] = 20; p[2] = 30;\n"
            "    int *tmp = realloc(p, 5 * sizeof(int));\n"
            "    if (!tmp) { free(p); return 1; }\n"
            "    p = tmp; p[3] = 40; p[4] = 50;\n"
            "    int sum = 0; for (int i = 0; i < 5; i++) sum += p[i];\n"
            '    printf("len=5 sum=%d\\n", sum);\n'
            "    free(p); p = NULL;\n"
            '    printf("freed=%d\\n", p == NULL);\n'
            "    return 0;\n"
            "}\n"
        ),
    }

    # ────────────────── L07: struct, padding và danh sách liên kết ──────────────────
    l07 = {
        "id": "L07",
        "slug": "struct_padding_linked_list",
        "title": "Kiểu ghép struct, căn lề bộ nhớ và danh sách liên kết",
        "next_title": "Tệp nhị phân, phép toán bit và tách trường đóng gói",
        "assumes": ["cpr_con_tro", "cpr_cap_phat_dong", "cpr_ub"],
        "objectives": [
            "Tính kích thước struct có tính byte đệm (padding) theo bội số căn lề",
            "Sắp xếp lại thứ tự trường từ lớn đến nhỏ để tiết kiệm bộ nhớ",
            "Cài đặt thêm đầu và giải phóng toàn bộ danh sách liên kết đơn không rò rỉ",
        ],
        "covers": [(1, "formula"), (2, "example"), (3, "check")],
        "hook_title": "Đảo thứ tự hai dòng khai báo trường mà giảm được 33% RAM?",
        "hook_html": (
            "<p>Một cấu trúc chứa 1 <code>char</code> (1B), 1 <code>int</code> (4B), 1 <code>char</code> (1B) tưởng chỉ tốn <b>6 byte</b>, nhưng máy tính cấp tới <b>12 byte</b>.</p>"
            "<p>Chỉ cần xếp lại thứ tự trường từ lớn tới nhỏ, kích thước tụt xuống <b>8 byte</b> — giảm ngay <b>33,3%</b> bộ nhớ cho hàng triệu bản ghi.</p>"
        ),
        "hook_say": (
            "Chào bạn, nếu bạn gộp hai ký tự một bai với một số nguyên bốn bai vào cùng một cấu trúc, tổng kích thước thường không phải sáu bai mà nhảy lên mười hai bai. "
            "Hôm nay ta tìm hiểu vì sao phần cứng tự động chèn các ô đệm trống giữa các trường dữ liệu. Chỉ cần sắp lại thứ tự trường là giảm được ba mươi ba phần trăm bộ nhớ trước khi nối các nút thành danh sách liên kết sạch rò rỉ."
        ),
        "hook_checks": ["alg.cpr_struct_size([(1, 1), (4, 4), (1, 1)]) == (12, 6)", "alg.cpr_struct_size([(4, 4), (1, 1), (1, 1)]) == (8, 2)"],
        "prereq_steps": [
            ak.st(
                ak.table(
                    ["nền tảng đã có", "vai trò ở bài này"],
                    [
                        ["Kích thước 1, 4, 8 byte (L00)", "Ngưỡng chia hết tự nhiên bằng kích thước mỗi trường cơ bản"],
                        ["Cấp phát động và giải phóng sạch (L06)", "Tạo từng nút danh sách trên vùng nhớ mở và thu hồi theo chuỗi"],
                    ],
                ),
                "Bài hôm nay kết hợp trực tiếp hai nền tảng từ bài 0 và bài 6. Từ bài 0 ta biết độ rộng chuẩn của từng trường ký tự và số nguyên. Từ bài 6 ta dùng vùng nhớ mở để tạo từng nút dữ liệu và giải phóng sạch khi không dùng nữa.",
                clear=True,
            )
        ],
        "sym_steps": [
            ak.st(
                ak.table(
                    ["ký hiệu mới", "ý nghĩa"],
                    [
                        ["<code>struct Node { ... };</code>", "Định nghĩa kiểu bản ghi gộp nhiều trường nằm liền kề theo thứ tự khai báo"],
                        ["<code>p-&gt;next</code>", "Truy cập trường của cấu trúc thông qua con trỏ (viết gọn của <code>(*p).next</code>)"],
                        ["Căn lề / byte đệm (padding)", "Byte trống do trình biên dịch chèn để địa chỉ mỗi trường chia hết cho kích thước nó"],
                    ],
                ),
                "Trên bảng là ba quy ước mới về cấu trúc dữ liệu. Từ khoá định nghĩa cấu trúc cho phép gộp nhiều trường và truy cập qua mũi tên con trỏ. Cuối cùng là khái niệm căn lề chèn bai đệm để bộ xử lý đọc nhanh.",
                introduces=["cpr_padding"],
                focus=[0, "1.2", "1.3", "1.4"],
                clear=True,
            )
        ],
        "intuition_title": "So sánh bố cục bộ nhớ trước và sau khi sắp trường lớn đứng trước",
        "intuition_steps": [
            ak.st(
                ak.svg_wrap(
                    960, 215,
                    ak.svg_rect(35, 30, 880, 68, "Thứ tự XẤU (12 byte): [char a: 1B] [3B ĐỆM] [int b: 4B] [char c: 1B] [3B ĐỆM đuôi]", "Lãng phí tới 6 byte đệm (50%)", ak.C_RED)
                    + ak.svg_rect(35, 120, 600, 68, "Thứ tự TỐT (8 byte): [int b: 4B] [char a: 1B] [char c: 1B] [2B ĐỆM đuôi]", "Giảm 4 byte = tiết kiệm 33,3%", ak.C_GREEN),
                ),
                "So sánh hai hàng trên sơ đồ bố cục bộ nhớ. Khi đặt trường nhỏ xen giữa trường lớn, trình biên dịch phải chèn sáu bai đệm làm tổng kích thước tăng lên mười hai bai. "
                "Ngược lại khi đặt trường bốn bai lên đầu tiên, hai ký tự đứng kề nhau ngay phía sau chỉ cần chèn thêm hai bai đệm ở đuôi nên tổng kích thước thu gọn chỉ còn tám bai.",
                clear=True,
            )
        ],
        "formula_title": "Hai quy tắc tính kích thước struct có padding",
        "formula_steps": [
            ak.st(
                ak.box(
                    "<ol><li>Mỗi trường có mức căn lề A phải bắt đầu tại độ lệch chia hết cho A.</li>"
                    "<li>Tổng kích thước của toàn <code>struct</code> phải chia hết cho mức căn lề lớn nhất trong các trường.</li></ol>"
                    "<p>Mẹo thực hành: luôn khai báo trường theo thứ tự giảm dần căn lề (8 → 4 → 2 → 1 byte).</p>",
                    "key",
                ),
                "Quy tắc tính kích thước cấu trúc gồm hai bước rất nhất quán theo phần cứng. Thứ nhất là vị trí bắt đầu mỗi trường luôn phải chia hết cho mức căn lề của trường đó. Thứ hai là tổng kích thước cuối cùng phải làm tròn theo bội số của trường có mức căn lề lớn nhất.",
                clear=True,
            )
        ],
        "formula_checks": ["alg.cpr_struct_size([(1, 1), (4, 4), (1, 1)]) == (12, 6)", "alg.cpr_struct_size([(4, 4), (1, 1), (1, 1)]) == (8, 2)"],
        "example_title": "Chạy thật trên GCC: đo sizeof hai kiểu struct và danh sách liên kết",
        "example_items": [
            {
                "type": "r3",
                "say": "Ta giải mã đủ bốn quy ước dùng trong cấu trúc và danh sách liên kết. Từ khoá định nghĩa nút cho phép tự trỏ sang nút kế tiếp, còn vòng lặp điều kiện dừng khi chạm rỗng. Chỉ thị đo độ lệch từ thư viện chuẩn tính chính xác vị trí bai của từng trường.",
                "rows": [
                    ["<code>typedef struct Node { int val; struct Node *next; } Node;</code>", "Đặt tên gọn <code>Node</code> cho nút chứa con trỏ tự trỏ tới nút tiếp theo"],
                    ["<code>while (h)</code>", "Viết gọn của <code>while (h != NULL)</code>: lặp tới khi hết danh sách"],
                    ["<code>#include &lt;stddef.h&gt;</code> / <code>offsetof(S, field)</code>", "Macro chuẩn trả về độ lệch theo byte của trường bên trong <code>struct</code>"],
                    ["<code>struct Bad / struct Good</code>", "Hai cấu trúc cùng 3 trường nhưng khác thứ tự khai báo"],
                ],
                "focus": [0, 1, 2, 3],
            },
            {
                "type": "code",
                "pid": "p1",
                "title": "Đo thật sizeof và chạy danh sách liên kết 3 nút giải phóng sạch",
                "say": "Chương trình đo kích thước thật của cấu trúc đặt trường xấu và cấu trúc đã sắp xếp lại từ lớn đến nhỏ. Phần sau tạo ba nút trên vùng nhớ mở, nối thành danh sách liên kết, cộng tổng giá trị rồi giải phóng sạch từ đầu tới cuối.",
                "out_say": "Đầu ra chạy thật khớp lý thuyết: cấu trúc xếp xấu tốn mười hai bai, cấu trúc xếp tốt chỉ còn tám bai. Ba nút mang giá trị mười, hai mươi, ba mươi cho tổng đúng sáu mươi và không để lại rò rỉ bộ nhớ.",
            },
        ],
        "progs": {
            "p1": {
                "code": (
                    "#include <stdio.h>\n"
                    "#include <stdlib.h>\n"
                    "struct Bad { char a; int b; char c; };\n"
                    "struct Good { int b; char a, c; };\n"
                    "typedef struct Node { int v; struct Node *next; } Node;\n"
                    "int main(void) {\n"
                    '    printf("bad=%zu good=%zu\\n", sizeof(struct Bad), sizeof(struct Good));\n'
                    "    Node *h = NULL;\n"
                    "    for (int v = 10; v <= 30; v += 10) {\n"
                    "        Node *n = malloc(sizeof(Node)); if (!n) return 1;\n"
                    "        n->v = v; n->next = h; h = n; }\n"
                    "    int s = 0, fr = 0;\n"
                    "    for (Node *c = h; c; c = c->next) s += c->v;\n"
                    '    while (h) { Node *nx = h->next; free(h); h = nx; fr++; }\n'
                    '    printf("sum=%d freed=%d\\n", s, fr); return 0; }'
                ),
                "expect": "bad=12 good=8\nsum=60 freed=3",
            },
            "p2": {
                "code": (
                    "#include <stdio.h>\n"
                    "#include <stddef.h>\n"
                    "struct Bad { char a; int b; char c; };\n"
                    "int main(void) {\n"
                    '    printf("off_a=%zu off_b=%zu off_c=%zu\\n",\n'
                    "           offsetof(struct Bad, a),\n"
                    "           offsetof(struct Bad, b),\n"
                    "           offsetof(struct Bad, c));\n"
                    "    return 0;\n"
                    "}"
                ),
                "expect": "off_a=0 off_b=4 off_c=8",
            },
        },
        "example_checks": ["10 + 20 + 30 == 60"],
        "check_title": "Kiểm chứng độ lệch thật của từng trường bằng offsetof",
        "check_items": [
            {
                "type": "code",
                "pid": "p2",
                "title": "Đo vị trí từng trường trong struct Bad",
                "say": "Ta dùng chỉ thị đo độ lệch trường trong chuẩn ngôn ngữ C để soi thẳng chỗ chèn bai đệm. Trường đầu đứng tại độ lệch không, trường số nguyên bị đẩy sang độ lệch bốn do phải chèn ba bai đệm trống. Cuối cùng trường ký tự nằm tại tám cộng một bằng chín, làm tròn theo bội số bốn thành tổng kích thước mười hai bai.",
                "out_say": "Kết quả chạy thật in ra đúng ba độ lệch không, bốn và tám bai vì có ba bai đệm trống nằm kẹp giữa trường đầu và trường thứ hai.",
            }
        ],
        "check_checks": ["(12 - 8) / 12 == 1 / 3"],
        "quymo_title": "Bảng quy mô: tiết kiệm RAM khi sắp trường cho 1 000 000 bản ghi",
        "quymo_steps": [
            ak.st(
                ak.table(
                    ["số bản ghi", "struct Xấu (12 byte)", "struct Tốt (8 byte)", "lượng RAM tiết kiệm"],
                    [
                        [ak.nowrap("1 000 (×1)"), "12 KB", "8 KB", "4 KB (33,3%)"],
                        [ak.nowrap("100 000 (×100)"), "1,2 MB", "0,8 MB", "0,4 MB (33,3%)"],
                        [ak.nowrap("1 000 000 (×1 000)"), "12 MB", "8 MB", "4 MB tiết kiệm miễn phí"],
                    ],
                ),
                "Với một trăm nghìn bản ghi đã tiết kiệm ngay không phẩy bốn mê-ga-bai RAM hoàn toàn miễn phí. Lên tới một triệu bản ghi trong bộ nhớ, chỉ cần đổi chỗ một dòng khai báo đã tiết kiệm ngay bốn mê-ga-bai RAM mà không mất một bít dữ liệu nào.",
                focus=[0, "1.2", "1.3", "1.4"],
                clear=True,
            )
        ],
        "quymo_checks": ["1_000_000 * 12 - 1_000_000 * 8 == 4_000_000"],
        "pitfall_steps": [
            ak.st(
                ak.box(
                    "<b>Lỗi 1: Giải phóng nút hiện tại rồi mới đọc <code>head->next</code>.</b> Phải lưu <code>nx = head->next</code> trước khi gọi <code>free(head)</code>!<br>"
                    "<b>Lỗi 2: Dùng <code>memcmp</code> so sánh hai <code>struct</code> có padding.</b> Các byte đệm có thể chứa giá trị rác khác nhau dù mọi trường bằng nhau.<br>"
                    "<b>Lỗi 3: Cộng tay kích thước từng trường thay vì dùng <code>sizeof(struct S)</code>.</b> Dễ thiếu hẳn phần byte đệm.",
                    "warn",
                ),
                "Có ba lỗi kinh điển khi dùng cấu trúc và danh sách liên kết. Lỗi nặng nhất là đọc con trỏ kế tiếp sau khi đã giải phóng nút. Hai lỗi kia là so sánh từng bai chứa đệm rác và tự cộng kích thước trường.",
                clear=True,
            )
        ],
        "quiz_steps": [
            ak.st(
                "<ol><li>Cấu trúc gồm <code>char a; long long b;</code> (1 byte và 8 byte) có kích thước <code>sizeof</code> bằng bao nhiêu byte?</li>"
                "<li>Khi duyệt vòng lặp để giải phóng danh sách liên kết, ta phải làm thao tác gì TRƯỚC khi gọi <code>free(cur)</code>?</li></ol>",
                "Đến lượt bạn tự kiểm tra. "
                "Câu một, cấu trúc gồm một ký tự một bai theo sau là một số tám bai chiếm tổng cộng bao nhiêu bai kể cả căn lề? "
                "Câu hai, phải lưu gì trước khi giải phóng nút hiện tại trong danh sách liên kết? Dừng vi-đê-ô và trả lời.",
                pause=20,
            ),
            ak.st(
                "<p>① Trường <code>b</code> căn lề 8 nên bắt đầu tại offset 8 (chèn 7 byte đệm) → tổng $\\hl{16}$ byte.</p>",
                "Đáp án câu một: chèn bảy bai đệm sau ký tự đầu để số tám bai nằm tại vị trí tám, tổng là mười sáu bai.",
                clear=True,
            ),
            ak.st(
                "<p>② Lưu con trỏ nút kế tiếp (<code>Node *nx = cur-&gt;next;</code>) trước khi gọi <code>free(cur)</code> để tránh đọc vào vùng nhớ vừa trả.</p>",
                "Đáp án câu hai: luôn cất địa chỉ nút kế tiếp sang biến tạm trước khi giải phóng nút đang giữ.",
                clear=True,
            ),
        ],
        "quiz_checks": ["alg.cpr_struct_size([(1, 1), (8, 8)]) == (16, 7)"],
        "recap_steps": [
            ak.st(
                "<div class='chain'><span class='n'>Xếp trường lớn → nhỏ</span><span class='a'>→</span>"
                "<span class='n'>Lưu next trước khi free</span><span class='a'>→</span>"
                "<span class='n'>Không đọc padding</span></div>",
                "Ghi nhớ chuỗi quy tắc làm việc với cấu trúc dữ liệu. Luôn xếp trường từ lớn xuống nhỏ để giảm bai đệm, lưu con trỏ kế trước lúc giải phóng nút, và không so sánh từng bai chứa đệm rác.",
                clear=True,
            )
        ],
        "lab_de": (
            "# Lab CPR L07 — Đo căn lề struct và cộng nút danh sách liên kết\n\n"
            "Viết chương trình C chuẩn C11 định nghĩa `struct S1 { char a; int b; char c; }` và `struct S2 { int b; char a; char c; }`, "
            "rồi dựng danh sách 4 nút mang giá trị `5, 10, 15, 20`, tính tổng và giải phóng toàn bộ, in đúng 2 dòng:\n"
            "1. `s1=12 s2=8`\n"
            "2. `list_sum=50 freed=4`\n\n"
            "Chấm tự động:\n```bash\nbash labs/cham.sh CPR L07 duong_dan/bai_cua_ban.c\n```"
        ),
        "lab_sol": (
            "#include <stdio.h>\n"
            "#include <stdlib.h>\n"
            "struct S1 { char a; int b; char c; };\n"
            "struct S2 { int b; char a; char c; };\n"
            "typedef struct Node { int v; struct Node *next; } Node;\n"
            "int main(void) {\n"
            '    printf("s1=%zu s2=%zu\\n", sizeof(struct S1), sizeof(struct S2));\n'
            "    Node *h = NULL;\n"
            "    int vals[4] = {5, 10, 15, 20};\n"
            "    for (int i = 0; i < 4; i++) {\n"
            "        Node *n = malloc(sizeof(Node)); if (!n) return 1;\n"
            "        n->v = vals[i]; n->next = h; h = n;\n"
            "    }\n"
            "    int s = 0, fr = 0;\n"
            "    for (Node *c = h; c; c = c->next) s += c->v;\n"
            "    while (h) { Node *nx = h->next; free(h); h = nx; fr++; }\n"
            '    printf("list_sum=%d freed=%d\\n", s, fr);\n'
            "    return 0;\n"
            "}\n"
        ),
    }

    # ────────────────── L08: Tệp nhị phân và phép toán bit ──────────────────
    l08 = {
        "id": "L08",
        "slug": "tep_nhi_phan_bit",
        "title": "Tệp nhị phân, phép toán bit và tách trường đóng gói",
        "next_title": "Tình huống chuyên gia: Xây bộ phân tích tệp nhật ký nhị phân sạch bộ nhớ",
        "assumes": ["cpr_con_tro", "cpr_cap_phat_dong", "cpr_padding", "cpr_ub"],
        "objectives": [
            "Mở, ghi và đọc chính xác bản ghi cố định từ tệp nhị phân bằng fopen/fwrite/fread/fclose",
            "Kiểm tra số phần tử thực sự đọc/ghi được thay vì giả định luôn đủ",
            "Dùng dịch bit và mặt nạ để tách cờ và độ dài đóng gói trong 1 byte/2 byte",
        ],
        "covers": [(1, "example"), (2, "check"), (3, "formula")],
        "hook_title": "Làm sao lưu 100 000 bản ghi nhanh hơn tệp chữ và nhỏ gọn từng bit?",
        "hook_html": (
            "<p>Ghi văn bản <code>\"1000000\"</code> tốn <b>7 byte</b> và phải phân tích chuỗi mỗi lần đọc. Lưu nhị phân đúng dạng <b>16 byte cố định</b> ghi một phát hết bản ghi, không đổi chữ.</p>"
            "<p>Hơn nữa một <code>uint16_t</code> (2 byte) vừa gói được <b>4 bit loại</b> vừa gói được <b>12 bit độ dài</b> bằng phép dịch bit và mặt nạ.</p>"
        ),
        "hook_say": (
            "Chào bạn, lưu dữ liệu dạng chữ vừa tốn dung lượng vừa mất công phân tích ký tự mỗi lần đọc lại từ đĩa. "
            "Giải pháp hiệu năng cao là ghi thẳng các khối bai cố định xuống tệp nhị phân rồi đọc ngược nguyên khối lên bộ nhớ. "
            "Hôm nay ta học cách mở tệp đúng chế độ, kiểm tra số khối đọc ghi và dùng phép toán bít tách các trường đóng gói gọn trong hai bai."
        ),
        "hook_checks": ["3 * 16 == 48"],
        "prereq_steps": [
            ak.st(
                ak.table(
                    ["nền tảng đã có", "ứng dụng bài mới"],
                    [
                        ["Bố cục struct căn lề chẵn (L07)", "Thiết kế bản ghi không dư padding khi ghi xuống tệp nhị phân"],
                        ["Số nguyên cố định bề rộng uint16_t/uint32_t (L01)", "Giữ kích thước đồng nhất khi đọc/ghi từng byte"],
                    ],
                ),
                "Ta kết hợp bài 1 và bài 7 để tạo định dạng tệp nhị phân chuẩn mực. Nhờ kiểu nguyên cố định độ rộng từ bài 1 và sắp trường gọn khít từ bài 7, mỗi bản ghi trên tệp luôn có đúng kích thước xác định từng bai trên mọi máy.",
                clear=True,
            )
        ],
        "sym_steps": [
            ak.st(
                ak.table(
                    ["ký hiệu mới", "ý nghĩa"],
                    [
                        ["<code>fopen(path, \"wb\" / \"rb\")</code>", "Mở tệp ở chế độ nhị phân ghi (<code>wb</code>) hoặc đọc (<code>rb</code>) (bắt buộc chữ <code>b</code> trên Windows)"],
                        ["<code>fwrite / fread(ptr, sz, n, f)</code>", "Ghi hoặc đọc <code>n</code> khối cỡ <code>sz</code>; trả về đúng số khối thực tế đã xử lý"],
                        ["<code>(h &gt;&gt; 12) &amp; 0xF</code>", "Dịch phải 12 bit rồi giữ 4 bit thấp bằng mặt nạ <code>0xF</code> (giá trị 0..15)"],
                    ],
                ),
                "Có ba quy ước cốt lõi với tệp nhị phân và phép bít. Mở tệp nhị phân luôn gắn chữ b để hệ thống giữ nguyên mọi bai mà không tự đổi ký tự xuống dòng. Tiếp theo là kiểm tra số khối thực tế hàm trả về rồi dùng dịch bít cùng mặt nạ lấy lại từng trường nhỏ.",
                focus=[0, "1.2", "1.3", "1.4"],
                clear=True,
            )
        ],
        "intuition_title": "Đóng gói 16 bit đầu gói tin: 4 bit loại | 12 bit độ dài",
        "intuition_steps": [
            ak.st(
                ak.svg_wrap(
                    960, 185,
                    ak.svg_rect(40, 45, 280, 90, "Bit 15..12 (4 bit)", "Loại (0..15) | mặt nạ 0xF", ak.C_AMBER)
                    + ak.svg_rect(340, 45, 580, 90, "Bit 11..0 (12 bit)", "Độ dài (0..4095) | mặt nạ 0xFFF", ak.C_BLUE),
                ),
                "Một số nguyên không dấu mười sáu bít được chia làm hai khoang rõ ràng. Bốn bít cao bên trái lưu mã loại bản ghi từ không đến mười lăm. Mười hai bít thấp bên phải lưu độ dài từ không đến bốn nghìn không trăm chín mươi lăm. Nhờ đóng gói hai giá trị vào chung một số nguyên, ta tiết kiệm phân nửa không gian phần đầu.",
                clear=True,
            )
        ],
        "formula_title": "Công thức đóng và mở trường bằng phép bit",
        "formula_steps": [
            ak.st(
                ak.box(
                    "<p>Gói <code>type = 5</code> (4 bit) và <code>len = 320</code> (12 bit):</p>"
                    "<p>h = (5 &lt;&lt; 12) | 320 = 20 480 + 320 = <b>20 800</b> (<code>0x5140</code>).</p>"
                    "<p>Mở lại: <code>type = (h &gt;&gt; 12) &amp; 0xF = 5</code>, <code>len = h &amp; 0xFFF = 320</code>.</p>",
                    "key",
                ),
                "Dịch số năm sang trái mười hai bít tương đương nhân bốn nghìn không trăm chín mươi sáu thành hai mươi nghìn bốn trăm tám mươi. Cộng thêm ba trăm hai mươi ta thu được giá trị đóng gói hai mươi nghìn tám trăm. Vì bốn bít cao dịch sang trái mười hai vị trí không bao giờ đè lên mười hai bít thấp. Khi mở ra, ta chỉ việc dịch phải mười hai bít kèm mặt nạ bốn bít để thu lại số năm và dùng mặt nạ mười hai bít giữ lại ba trăm hai mươi.",
                clear=True,
            )
        ],
        "formula_checks": ["((5 << 12) | 320) == 20800", "(20800 >> 12) & 0xF == 5", "20800 & 0xFFF == 320"],
        "example_title": "Chạy thật trên GCC: ghi và đọc 3 bản ghi 16 byte trong tệp nhị phân",
        "example_items": [
            {
                "type": "r3",
                "say": "Ta giải mã đủ bốn quy ước đọc ghi tệp và đóng gói bít trong C. Kiểu con trỏ tệp quản lý luồng mở để ghi đọc từng khối rồi phải gọi đóng tệp cho dữ liệu xuống đĩa. Khi gói và mở trường, dịch trái dịch phải đi kèm phép hoặc bít và mặt nạ mười hai bít.",
                "rows": [
                    ["<code>typedef struct { uint64_t ts; uint16_t hdr; uint16_t flag; uint32_t amt; } Rec;</code>", "8 + 2 + 2 + 4 = đúng 16 byte, 0 byte đệm"],
                    ["<code>FILE *f</code> / <code>fclose(f)</code>", "Con trỏ luồng tệp; <code>fclose(f)</code> đẩy sạch đệm xuống đĩa và giải phóng bộ mô tả"],
                    ["<code>(type &lt;&lt; 12) | len</code>", "Dịch trái <code>&lt;&lt; 12</code> đẩy lên 4 bit cao rồi ghép bit bằng phép HOẶC <code>|</code>"],
                    ["<code>h &amp; 0xFFF</code>", "Mặt nạ 12 bit <code>1111_1111_1111</code> giữ nguyên giá trị <code>len</code> từ 0 đến 4095"],
                ],
                "focus": [0, 1, 2, 3],
            },
            {
                "type": "code",
                "pid": "p1",
                "title": "Ghi 3 bản ghi 16 byte ra tệp nhị phân, đọc lại và giải mã bit",
                "say": "Chương trình đóng gói sẵn một mảng ba bản ghi mười sáu bai rồi ghi thẳng xuống tệp nhị phân tạm. Ngay sau đó chương trình mở tệp ở chế độ đọc nhị phân, đếm số khối đọc được và dùng mặt nạ bít tách loại cùng độ dài bản ghi đầu tiên.",
                "out_say": "Đầu ra chạy thật xác nhận mỗi bản ghi chiếm tròn mười sáu bai và số khối đọc về bằng đúng ba. Phép toán bít tách lại chính xác loại bằng năm và độ dài bằng ba trăm hai mươi khớp hoàn toàn dữ liệu ban đầu.",
            },
        ],
        "progs": {
            "p1": {
                "code": (
                    "#include <stdio.h>\n"
                    "#include <stdint.h>\n"
                    "typedef struct { uint64_t ts; uint16_t hdr, flag; uint32_t amt; } Rec;\n"
                    "int main(void) {\n"
                    "    Rec w[3] = {{1001, (uint16_t)((5<<12)|320), 1, 50000},\n"
                    "                {1002, (uint16_t)((2<<12)|128), 0, 12000},\n"
                    "                {1003, (uint16_t)((5<<12)|64),  1, 8000}};\n"
                    '    FILE *f = fopen("rec.bin", "wb"); if (!f) return 1;\n'
                    "    size_t nw = fwrite(w, sizeof(Rec), 3, f); fclose(f);\n"
                    "    Rec r[3]; f = fopen(\"rec.bin\", \"rb\"); if (!f) return 1;\n"
                    "    size_t nr = fread(r, sizeof(Rec), 3, f); fclose(f);\n"
                    '    printf("sz=%zu nw=%zu nr=%zu\\n", sizeof(Rec), nw, nr);\n'
                    '    printf("r0 type=%u len=%u amt=%u\\n", (r[0].hdr>>12)&0xF, r[0].hdr&0xFFF, r[0].amt);\n'
                    "    return 0;\n"
                    "}"
                ),
                "expect": "sz=16 nw=3 nr=3\nr0 type=5 len=320 amt=50000",
            },
        },
        "example_checks": ["alg.cpr_pack_rec_bytes() == 16", "3 * 16 == 48"],
        "check_title": "Kiểm chéo bằng tính tổng độ dài tệp và số dư 0 byte đệm",
        "check_items": [
            {
                "type": "math",
                "show": ak.box("<p>Tổng byte tệp nhị phân = 3 × (8 + 2 + 2 + 4) = 3 × 16 = <b>48</b> byte.</p>"
                               "<p>Phép tách <code>(20800 &gt;&gt; 12) &amp; 0xF == 5</code> và <code>20800 &amp; 0xFFF == 320</code> khớp hoàn toàn với kết quả đọc từ tệp thật.</p>", "ok"),
                "say": "Ta kiểm chéo lại bằng tính tay vì cần xác nhận kích thước và giá trị bít không có sai số ngầm. Ba bản ghi mỗi bản ghi mười sáu bai cho tổng tệp đúng bốn mươi tám bai. Con số đóng gói dịch phải mười hai bít ra đúng năm và lấy mười hai bít thấp ra đúng ba trăm hai mươi.",
                "clear": True,
            }
        ],
        "check_checks": ["alg.cpr_pack_rec_bytes() * 3 == 48"],
        "quymo_title": "Bảng quy mô: dung lượng tệp nhị phân 16 byte cố định",
        "quymo_steps": [
            ak.st(
                ak.table(
                    ["số bản ghi", "tệp chữ CSV (~40 B/dòng)", "nhị phân 16 B/bản ghi", "tiết kiệm đĩa"],
                    [
                        [ak.nowrap("1 000 (×1)"), "40 KB", "16 KB", "60% nhỏ hơn"],
                        [ak.nowrap("100 000 (×100)"), "4,0 MB", "1,6 MB", "60% nhỏ hơn"],
                        [ak.nowrap("10 000 000 (×10 000)"), "400 MB", "160 MB", "Tiết kiệm 240 MB"],
                    ],
                ),
                "Với một nghìn bản ghi sự khác biệt dung lượng mới là bốn mươi ki-lô-bai so với mười sáu ki-lô-bai. Nhưng ở quy mô mười triệu bản ghi, lưu dạng văn bản tốn tới bốn trăm mê-ga-bai trong khi tệp nhị phân chỉ tốn một trăm sáu mươi mê-ga-bai và đọc nhanh gấp nhiều lần.",
                focus=[0, "1.2", "1.3", "1.4"],
                clear=True,
            )
        ],
        "quymo_checks": ["10_000_000 * 16 == 160_000_000"],
        "pitfall_steps": [
            ak.st(
                ak.box(
                    "<b>Lỗi 1: Mở tệp nhị phân chỉ ghi <code>\"w\"</code> thay vì <code>\"wb\"</code>.</b> Trên Windows, chế độ văn bản tự đổi byte <code>0x0A</code> thành <code>0x0D 0x0A</code> làm hỏng dữ liệu.<br>"
                    "<b>Lỗi 2: Không kiểm giá trị trả về của <code>fread</code>/<code>fwrite</code>.</b> Nếu tệp bị cắt ngắn giữa chừng hoặc đầy đĩa, phần tử cuối chứa dữ liệu cũ.<br>"
                    "<b>Lỗi 3: Dịch bit trên số nguyên có dấu âm.</b> Luôn dùng kiểu không dấu (<code>uint16_t</code>, <code>uint32_t</code>) cho mặt nạ và dịch bit.",
                    "warn",
                ),
                "Có ba lỗi rất dễ gặp với tệp nhị phân và phép bít. Quên cờ b sẽ làm hỏng dữ liệu xuống dòng trên hệ thống Windows. Ngoài ra nhiều người bỏ qua giá trị trả về của hàm đọc ghi hoặc dịch bít số âm.",
                clear=True,
            )
        ],
        "quiz_steps": [
            ak.st(
                "<ol><li>Số đóng gói <code>0x3080</code> (4 bit cao là loại, 12 bit thấp là độ dài): tách ra được loại và độ dài bằng bao nhiêu?</li>"
                "<li>Ghi 250 bản ghi mỗi bản ghi 16 byte thành công ra tệp nhị phân thì tệp dài bao nhiêu byte?</li></ol>",
                "Đến lượt bạn tự kiểm tra. "
                "Câu một, từ số hệ mười sáu là ba không tám không gồm bốn bít cao chỉ loại và mười hai bít thấp chỉ độ dài, ta tách được loại và độ dài là bao nhiêu? "
                "Câu hai, hai trăm năm mươi bản ghi mười sáu bai chiếm tệp dài bao nhiêu bai? Dừng vi-đê-ô và tính ra giấy.",
                pause=20,
            ),
            ak.st(
                "<p>① Loại: <code>(0x3080 >> 12) & 0xF</code> $= \\hl{3}$; độ dài: <code>0x080</code> $= 8 \\times 16 = \\hl{128}$.</p>",
                "Đáp án câu một: loại bằng ba và độ dài ở hệ mười sáu là không tám không, tức một trăm hai mươi tám.",
                clear=True,
            ),
            ak.st(
                "<p>② 250 × 16 = <b>4 000</b> byte.</p>",
                "Đáp án câu hai: hai trăm năm mươi nhân mười sáu bằng bốn nghìn bai.",
                clear=True,
            ),
        ],
        "quiz_checks": ["(0x3080 >> 12) & 0xF == 3", "0x3080 & 0xFFF == 128", "250 * 16 == 4000"],
        "recap_steps": [
            ak.st(
                "<div class='chain'><span class='n'>Mở \"rb\"/\"wb\"</span><span class='a'>→</span>"
                "<span class='n'>Kiểm số khối fread/fwrite</span><span class='a'>→</span>"
                "<span class='n'>Dịch bit + mặt nạ trên số không dấu</span></div>",
                "Tổng kết lại chuỗi tư duy hôm nay khi làm việc ở mức bai và bít. Luôn mở tệp kèm cờ nhị phân, kiểm tra số khối thực sự đọc ghi được, và dùng phép toán bít trên kiểu không dấu.",
                clear=True,
            )
        ],
        "lab_de": (
            "# Lab CPR L08 — Đóng gói trường bit và kiểm tệp nhị phân 16 byte\n\n"
            "Viết chương trình C chuẩn C11 đóng gói `type=7, len=250` vào `uint16_t`, ghi 4 bản ghi 16 byte ra tệp `out.bin`, đọc lại rồi in đúng 2 dòng:\n"
            "1. `packed=28922 type=7 len=250`\n"
            "2. `bytes=64 count=4`\n\n"
            "Chấm tự động:\n```bash\nbash labs/cham.sh CPR L08 duong_dan/bai_cua_ban.c\n```"
        ),
        "lab_sol": (
            "#include <stdio.h>\n"
            "#include <stdint.h>\n"
            "typedef struct { uint64_t ts; uint16_t hdr; uint16_t flag; uint32_t amt; } Rec;\n"
            "int main(void) {\n"
            "    uint16_t pk = (uint16_t)((7 << 12) | 250);\n"
            '    printf("packed=%u type=%u len=%u\\n", pk, (pk >> 12) & 0xF, pk & 0xFFF);\n'
            "    Rec a[4] = {{1, pk, 0, 100}, {2, pk, 1, 200}, {3, pk, 0, 300}, {4, pk, 1, 400}};\n"
            '    FILE *f = fopen("out.bin", "wb"); if (!f) return 1;\n'
            "    fwrite(a, sizeof(Rec), 4, f); fclose(f);\n"
            "    Rec b[4]; f = fopen("
            '"out.bin", "rb"); if (!f) return 1;\n'
            "    size_t nr = fread(b, sizeof(Rec), 4, f); fclose(f);\n"
            '    printf("bytes=%zu count=%zu\\n", nr * sizeof(Rec), nr);\n'
            "    return 0;\n"
            "}\n"
        ),
    }

    # ────────────────── L09: Tình huống chuyên gia (Case Study) ──────────────────
    l09 = {
        "id": "L09",
        "slug": "tinh_huong_phan_tich_nhat_ky",
        "title": "Tình huống chuyên gia: Xây bộ phân tích tệp nhật ký nhị phân sạch bộ nhớ",
        "next_title": None,
        "assumes": ["cpr_con_tro", "cpr_cap_phat_dong", "cpr_padding", "cpr_ub"],
        "objectives": [
            "Thiết kế bản ghi nhị phân 16 byte không lãng phí byte đệm",
            "Đọc luồng lớn quy mô triệu bản ghi bằng mảng động tăng gấp đôi dung lượng và free sạch",
            "Kiểm lỗi biên tệp cụt và phát hiện tràn tổng tiền 64-bit",
        ],
        "covers": [(1, "formula"), (2, "example"), (3, "check")],
        "hook_title": "Tình huống thực chiến: dịch vụ C ăn RAM tăng vọt và sập lúc 3 giờ sáng",
        "hook_html": (
            "<p>Hệ thống đối soát mỗi đêm đọc lô <b>100 000 bản ghi</b> giao dịch nhị phân. Bản cũ định nghĩa sai thứ tự <code>struct</code> mất <b>24 byte</b> mỗi bản ghi, và quên kiểm <code>realloc</code> nên sập khi tăng tải.</p>"
            "<p>Ta thiết kế lại bản ghi <b>16 byte</b> không đệm (<b>1,6 MB</b> thay vì <b>2,4 MB</b>), mảng động tăng gấp đôi an toàn và dọn sạch 0 rò rỉ.</p>"
        ),
        "hook_say": (
            "Chào bạn đến với bài tình huống chuyên gia tổng kết khoá C. "
            "Một dịch vụ đọc một trăm nghìn bản ghi mỗi đêm bị đội bộ nhớ từ một phẩy sáu lên hai phẩy bốn mê-ga-bai do bai đệm sai thứ tự. Hệ thống còn có nguy cơ sập vì quên kiểm tràn lúc cấp phát động. "
            "Hôm nay ta kết hợp trọn bộ kỹ năng từ bài 0 đến bài 8 để viết lại bộ phân tích vừa chuẩn từng bai vừa sạch bộ nhớ hoàn toàn."
        ),
        "hook_checks": ["100_000 * 16 == 1_600_000", "100_000 * 24 == 2_400_000"],
        "prereq_steps": [
            ak.st(
                ak.table(
                    ["kỹ năng tổng hợp từ khoá CPR", "vai trò trong bài tình huống"],
                    [
                        ["Sắp trường giảm padding + đóng gói bit (L07–L08)", "Giữ bản ghi đúng 16 byte thay vì 24 byte"],
                        ["Kiểm tràn phép nhân + realloc an toàn + free sạch (L01, L06)", "Chống sập và rò rỉ bộ nhớ ở quy mô lớn"],
                    ],
                ),
                "Tình huống chuyên gia hôm nay huy động trọn bộ bốn mảnh ghép từ các bài trước. Đầu tiên là sắp xếp cấu trúc chuẩn mười sáu bai không dư bai đệm và tách trường đóng gói bít. Sau đó kiểm tra ngưỡng tràn trước khi nhân kích thước để mở rộng mảng động và thu hồi sạch hoàn toàn.",
                clear=True,
            )
        ],
        "sym_steps": [
            ak.st(
                ak.table(
                    ["quy ước kỹ thuật của bài", "ý nghĩa"],
                    [
                        ["<code>cap *= 2</code>", "Chiến lược nhân đôi sức chứa mảng động giúp giảm số lần gọi <code>realloc</code> từ O(N) xuống O(log N)"],
                        ["<code>SIZE_MAX / sizeof(Rec)</code>", "Ngưỡng tối đa phần tử trước khi nhân kích thước gây tràn số nguyên"],
                    ],
                ),
                "Hai kỹ thuật chuyên gia được áp dụng trong bài tình huống này. Kỹ thuật đầu là nhân đôi dung lượng mảng động để giữ số lần sao chép ở mức lô-ga-rít. Kỹ thuật sau là chia kiểm tra ngưỡng trước khi nhân để chặn tràn.",
                focus=[0, "1.2", "1.3"],
                clear=True,
            )
        ],
        "intuition_title": "Luồng xử lý an toàn từ luồng dữ liệu tới tổng kết toán 64-bit",
        "intuition_steps": [
            ak.st(
                ak.svg_wrap(
                    960, 200,
                    ak.svg_rect(20, 50, 205, 95, "1. Đọc khối 16 B", "Kiểm số khối == 1", ak.C_BLUE)
                    + ak.svg_arrow(225, 97, 265, 97, "")
                    + ak.svg_rect(265, 50, 255, 95, "2. Đầy → Kiểm & Nhân đôi", "realloc qua biến tạm", ak.C_AMBER)
                    + ak.svg_arrow(520, 97, 560, 97, "")
                    + ak.svg_rect(560, 50, 205, 95, "3. Cộng uint64_t", "Chặn tràn trước cộng", ak.C_GREEN)
                    + ak.svg_arrow(765, 97, 800, 97, "")
                    + ak.svg_rect(800, 50, 145, 95, "4. free & Đóng", "0 byte rò rỉ", ak.C_GRAY),
                ),
                "Luồng dữ liệu chuẩn gồm bốn khâu liên hoàn. Ở hai khâu đầu, luồng đọc nhận từng khối mười sáu bai kèm kiểm tra số khối rồi nhân đôi sức chứa mảng động qua con trỏ tạm khi đầy. Ở hai khâu sau, hệ thống lọc bản ghi đúng loại để cộng dồn vào tổng sáu mươi bốn bít có chặn tràn rồi giải phóng sạch bộ nhớ.",
                clear=True,
            )
        ],
        "formula_title": "Tính lại chi phí và số lần realloc khi nhân đôi sức chứa",
        "formula_steps": [
            ak.st(
                ak.box(
                    "<p>Bắt đầu sức chứa <code>cap = 4</code>. Để nạp <b>100 000</b> phần tử, chỉ cần nhân đôi đến 4 × 2¹⁵ = 131 072 — tức đúng <b>15 lần</b> <code>realloc</code> (so với 25 000 lần nếu mỗi lần chỉ tăng 4 ô).</p>"
                    "<p>Kiểm tra tràn trước khi nhân: <code>if (new_cap &gt; SIZE_MAX / sizeof(Rec)) return 1;</code></p>",
                    "key",
                ),
                "Với dung lượng khởi điểm bằng bốn và nhân đôi mỗi lần đầy, chỉ cần đúng mười lăm lần mở rộng đã đạt sức chứa hơn một trăm ba mươi mốt nghìn bản ghi. Vì chiến lược nhân đôi tăng theo lũy thừa hai nên số lần cấp phát lại rất nhỏ dù dữ liệu lên tới hàng trăm nghìn bản ghi. Trước mọi phép nhân kích thước mở rộng ta bắt buộc kiểm tra phép chia ngưỡng nhằm loại bỏ hoàn toàn nguy cơ tràn số.",
                clear=True,
            )
        ],
        "formula_checks": ["4 * (2 ** 15) == 131_072"],
        "example_title": "Chạy thật trên GCC: mảng động tăng gấp đôi phân tích 6 bản ghi nhị phân",
        "example_items": [
            {
                "type": "r3",
                "say": "Ta giải mã đủ bốn thành phần cốt lõi trong đoạn mã tình huống trước khi chạy kiểm thử. Cấu trúc mảng động gói dữ liệu, độ dài và sức chứa; phép chia chặn tràn ngăn lỗi nhân kích thước. Kiểm định tĩnh chuẩn C11 khoá kích thước mười sáu bai lúc biên dịch. Hằng cấu trúc tạm và mã không dấu sáu mươi bốn bít hoàn tất phần hiển thị tổng.",
                "rows": [
                    ["<code>typedef struct { Rec *d; size_t len, cap; int res; } Vec;</code>", "Mảng động giữ con trỏ, độ dài, sức chứa và số lần mở rộng"],
                    ["<code>if (nc &gt; SIZE_MAX / sizeof(Rec)) return 0;</code>", "Chặn tràn phép nhân kích thước trước khi gọi <code>realloc</code>"],
                    ["<code>_Static_assert(sizeof(Rec) == 16, \"...\");</code>", "Kiểm định tĩnh chuẩn C11 ngay lúc biên dịch (bắt buộc đủ 2 tham số)"],
                    ["<code>(Rec){...}</code> / <code>(unsigned long long)sum</code> + <code>%llu</code>", "Khởi tạo cấu trúc tạm ngay tại chỗ và định dạng in số nguyên 64-bit không dấu"],
                ],
                "focus": [0, 1, 2, 3],
            },
            {
                "type": "code",
                "pid": "p1",
                "title": "Mảng động tăng gấp đôi sức chứa có kiểm tràn nhân kích thước",
                "say": "Chương trình tạo mảng động sức chứa ban đầu bằng không rồi thêm sáu phần tử theo cơ chế nhân đôi từ hai lên bốn rồi tám. Hàm thêm phần tử kiểm tra ngưỡng chia trước khi nhân kích thước để chặn tràn số và đưa con trỏ về rỗng sau khi giải phóng.",
                "out_say": "Đầu ra chạy thật xác nhận sức chứa tăng đúng từ không lên hai, bốn rồi tám sau ba lần cấp phát lại. Biến sạch bằng một chứng tỏ con trỏ dữ liệu đã được đưa an toàn về rỗng sau khi giải phóng.",
            },
        ],
        "progs": {
            "p1": {
                "code": (
                    "#include <stdio.h>\n"
                    "#include <stdlib.h>\n"
                    "#include <stdint.h>\n"
                    "typedef struct { uint64_t ts; uint16_t hdr, f; uint32_t amt; } Rec;\n"
                    "typedef struct { Rec *d; size_t len, cap; int res; } Vec;\n"
                    "static int push(Vec *v, Rec r) {\n"
                    "    if (v->len == v->cap) { size_t nc = v->cap ? v->cap * 2 : 2;\n"
                    "        if (nc > SIZE_MAX / sizeof(Rec)) return 0;\n"
                    "        Rec *t = realloc(v->d, nc * sizeof(Rec)); if (!t) return 0;\n"
                    "        v->d = t; v->cap = nc; v->res++; } v->d[v->len++] = r; return 1; }\n"
                    "int main(void) { Vec v = {NULL,0,0,0}; uint32_t i;\n"
                    "    for (i = 0; i < 6; i++) if (!push(&v, (Rec){i+1, 1<<12, 0, 100})) return 1;\n"
                    '    printf("len=%zu cap=%zu resizes=%d\\n", v.len, v.cap, v.res);\n'
                    '    free(v.d); v.d = NULL; printf("clean=%d\\n", v.d == NULL); return 0; }'
                ),
                "expect": "len=6 cap=8 resizes=3\nclean=1",
            },
            "p2": {
                "code": (
                    "#include <stdio.h>\n"
                    "#include <stdint.h>\n"
                    "typedef struct { uint64_t ts; uint16_t hdr, f; uint32_t amt; } Rec;\n"
                    "_Static_assert(sizeof(Rec) == 16, \"Rec must be 16B\");\n"
                    "int main(void) {\n"
                    "    uint32_t a[6] = {100000, 50000, 200000, 75000, 250000, 350000};\n"
                    "    uint64_t sum = 0; size_t matched = 0;\n"
                    "    for (int i = 0; i < 6; i++) {\n"
                    "        Rec r = {(uint64_t)(i + 1), (uint16_t)((i % 2 ? 2 : 1) << 12), 0, a[i]};\n"
                    "        if (((r.hdr >> 12) & 0xF) == 1) { sum += r.amt; matched++; }\n"
                    "    }\n"
                    '    printf("matched=%zu sum=%llu\\n", matched, (unsigned long long)sum);\n'
                    "    return 0; }"
                ),
                "expect": "matched=3 sum=550000",
            },
        },
        "example_checks": ["2 * 2 * 2 == 8"],
        "check_title": "Đối chứng lọc bản ghi 16 byte và tính tổng 64-bit",
        "check_items": [
            {
                "type": "code",
                "pid": "p2",
                "title": "Kiểm static_assert 16B, lọc loại 1 qua bit và cộng tổng 64-bit",
                "say": "Ở đường kiểm chứng thứ hai, ta khoá cứng kích thước cấu trúc mười sáu bai bằng kiểm định tĩnh lúc biên dịch rồi chạy lọc sáu bản ghi. Vì chỉ các bản ghi vị trí chẵn mang mã loại một nên đúng ba giao dịch một trăm nghìn, hai trăm nghìn và hai trăm năm mươi nghìn được cộng vào tổng.",
                "out_say": "Đầu ra thật khớp tuyệt đối vì ba giao dịch khớp điều kiện cho tổng sáu mươi bốn bít đúng bằng năm trăm năm mươi nghìn đồng.",
            }
        ],
        "check_checks": ["100_000 * 24 - 100_000 * 16 == 800_000"],
        "quymo_title": "Bảng quy mô: so sánh chiến lược cấp phát cộng thêm vs nhân đôi",
        "quymo_steps": [
            ak.st(
                ak.table(
                    ["số bản ghi nạp", "tăng đều +10 phần tử", "nhân đôi sức chứa (×2)", "tổng RAM (16 B/bản ghi)"],
                    [
                        [ak.nowrap("1 000 (×1)"), "100 lần realloc", "9 lần realloc (cap 1024)", "16 KB"],
                        [ak.nowrap("100 000 (×100)"), "10 000 lần realloc", "16 lần realloc (cap 131 072)", "1,6 MB"],
                        [ak.nowrap("10 000 000 (×10 000)"), "1 000 000 lần realloc", "23 lần realloc", "160 MB"],
                    ],
                ),
                "Bảng quy mô cho thấy sự chênh lệch khổng lồ giữa hai chiến lược mở rộng mảng động. Nếu chỉ tăng tuyến tính thêm mười ô mỗi lần đầy, mười triệu bản ghi tốn tới một triệu lần sao chép lại bộ nhớ. Ngược lại chiến lược nhân đôi dung lượng chỉ cần hai mươi ba lần mở rộng cực kỳ nhanh gọn.",
                focus=[0, "1.2", "1.3", "1.4"],
                clear=True,
            )
        ],
        "quymo_checks": ["10_000_000 * 16 == 160_000_000", "2 ** 23 == 8_388_608"],
        "pitfall_steps": [
            ak.st(
                ak.box(
                    "<b>Lỗi chuyên gia 1: Quên kiểm tràn khi tính <code>nc * sizeof(Rec)</code>.</b> Kẻ tấn công đưa tệp khai số bản ghi giả rất lớn khiến phép nhân tràn thành số nhỏ, cấp buffer tí hon rồi ghi tràn Heap.<br>"
                    "<b>Lỗi chuyên gia 2: Dùng trực tiếp cấu trúc không ép thứ tự trường để đọc luồng ngoài mà quên độ đệm.</b> Phải dùng <code>sizeof</code> và kiểm <code>_Static_assert(sizeof(Rec) == 16, \"Rec 16B\")</code>.<br>"
                    "<b>Lỗi chuyên gia 3: Rò rỉ trên nhánh thoát sớm khi tệp bị cắt ngắn.</b> Luôn dọn con trỏ mảng động trước mọi câu lệnh <code>return</code>.",
                    "warn",
                ),
                "Hãy mang theo ba bài học xương máu khi viết mã cấp hệ thống. Luôn kiểm tràn nhân kích thước trước khi mở rộng vùng nhớ động. Đồng thời khoá chặt kích thước cấu trúc bằng kiểm định tĩnh và dọn sạch bộ nhớ ở cả nhánh lỗi.",
                clear=True,
            )
        ],
        "quiz_steps": [
            ak.st(
                "<ol><li>Bắt đầu với sức chứa 2, nạp đủ 1 000 phần tử theo luật nhân đôi thì qua mấy lần mở rộng (<code>cap</code> cuối bằng bao nhiêu)?</li>"
                "<li>Viết điều kiện kiểm tra tràn <b>trước</b> khi nhân <code>nc * sizeof(Rec)</code>.</li></ol>",
                "Đến lượt bạn tự kiểm tra. "
                "Câu một, khởi đầu sức chứa bằng hai và nhân đôi mỗi khi đầy, nạp một nghìn phần tử cần tối thiểu mấy lần mở rộng và sức chứa cuối bằng bao nhiêu? "
                "Câu hai, viết điều kiện chặn tràn phép nhân kích thước trước khi gọi mở rộng. Dừng vi-đê-ô và trả lời.",
                pause=20,
            ),
            ak.st(
                "<p>① 2 → 4 → 8 → … → 1024 = 2 × 2⁹: qua <b>9</b> lần mở rộng, sức chứa cuối bằng <b>1 024</b>.</p>",
                "Đáp án câu một: hai nhân hai lũy thừa chín bằng một nghìn không trăm hai mươi bốn, tức chỉ cần qua đúng chín lần mở rộng.",
                clear=True,
            ),
            ak.st(
                "<p>② Kiểm tra <code>if (nc &gt; SIZE_MAX / sizeof(Rec))</code> trước khi thực hiện phép nhân.</p>",
                "Đáp án câu hai: chia giá trị lớn nhất của kiểu kích thước cho cỡ phần tử để kiểm ngưỡng trước khi nhân.",
                clear=True,
            ),
        ],
        "quiz_checks": ["2 * (2 ** 9) == 1024"],
        "recap_steps": [
            ak.st(
                "<div class='chain'><span class='n'>Struct gọn không đệm</span><span class='a'>→</span>"
                "<span class='n'>Kiểm tràn + realloc nhân đôi</span><span class='a'>→</span>"
                "<span class='n'>Đóng tệp &amp; free sạch</span></div>",
                "Tổng kết trọn bộ kỹ năng lập trình C cấp hệ thống sau mười bài học. Chọn cấu trúc không dư bai đệm, mở rộng mảng động bằng nhân đôi kèm kiểm tràn, và luôn giải phóng sạch bộ nhớ ở mọi đường thoát.",
                clear=True,
            )
        ],
        "lab_de": (
            "# Lab CPR L09 — Phân tích mảng động Rec 16 byte sạch bộ nhớ\n\n"
            "Viết chương trình C chuẩn C11 dùng `typedef struct { uint64_t ts; uint16_t hdr; uint16_t flag; uint32_t amt; } Rec;`, "
            "cài mảng động tăng gấp đôi từ `cap=2` để nạp 5 bản ghi có `amt = {100, 250, 400, 150, 600}` (các mục vị trí chẵn 0,2,4 mang loại 1, vị trí lẻ mang loại 2), rồi tính tổng loại 1 và giải phóng sạch, in đúng 2 dòng:\n"
            "1. `rec_size=16 cap=8 sum_t1=1100`\n"
            "2. `clean=1`\n\n"
            "Chấm tự động:\n```bash\nbash labs/cham.sh CPR L09 duong_dan/bai_cua_ban.c\n```"
        ),
        "lab_sol": (
            "#include <stdio.h>\n"
            "#include <stdlib.h>\n"
            "#include <stdint.h>\n"
            "typedef struct { uint64_t ts; uint16_t hdr; uint16_t flag; uint32_t amt; } Rec;\n"
            "int main(void) {\n"
            "    size_t cap = 2, len = 0;\n"
            "    Rec *d = malloc(cap * sizeof(Rec)); if (!d) return 1;\n"
            "    uint32_t amts[5] = {100, 250, 400, 150, 600};\n"
            "    for (int i = 0; i < 5; i++) {\n"
            "        if (len == cap) {\n"
            "            size_t nc = cap * 2;\n"
            "            if (nc > SIZE_MAX / sizeof(Rec)) { free(d); return 1; }\n"
            "            Rec *t = realloc(d, nc * sizeof(Rec));\n"
            "            if (!t) { free(d); return 1; }\n"
            "            d = t; cap = nc;\n"
            "        }\n"
            "        uint16_t tp = (uint16_t)(i % 2 == 0 ? 1 : 2);\n"
            "        d[len++] = (Rec){(uint64_t)(i + 1), (uint16_t)(tp << 12), 0, amts[i]};\n"
            "    }\n"
            "    uint64_t s1 = 0;\n"
            "    for (size_t i = 0; i < len; i++) if (((d[i].hdr >> 12) & 0xF) == 1) s1 += d[i].amt;\n"
            '    printf("rec_size=%zu cap=%zu sum_t1=%llu\\n", sizeof(Rec), cap, (unsigned long long)s1);\n'
            "    free(d); d = NULL;\n"
            '    printf("clean=%d\\n", d == NULL);\n'
            "    return 0;\n"
            "}\n"
        ),
    }

    return [l05, l06, l07, l08, l09]
