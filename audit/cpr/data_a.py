"""Đặc tả dữ liệu CPR L00–L04."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "audit" / "review"))
import af2_kit as ak  # noqa: E402


def lessons():
    # ────────────────── L00: Chương trình C đầu tiên, GCC và sizeof ──────────────────
    l00 = {
        "id": "L00",
        "slug": "chuong_trinh_c_sizeof",
        "title": "Chương trình C đầu tiên, biên dịch với GCC và kích thước bộ nhớ",
        "next_title": "Biến, vòng lặp và ranh giới tràn số nguyên trong C",
        "assumes": [],
        "objectives": [
            "Biên dịch và chạy chương trình C với cờ -std=c11 -Wall -Wextra -Werror",
            "Đo kích thước byte của char, short, int, long long và con trỏ trên máy 64-bit",
            "Tính dung lượng mảng số nguyên 64-bit ở ba quy mô 100, 10 000 và 1 000 000 phần tử",
        ],
        "covers": [(1, "example"), (2, "formula"), (3, "quymo")],
        "hook_title": "Vì sao một dòng code C sai kích thước có thể làm hết bộ nhớ?",
        "hook_html": (
            "<p>Một chương trình xử lý <b>1 000 000</b> mã giao dịch cần cấp bộ nhớ trước khi chạy. "
            "Nếu mỗi phần tử chiếm <b>4 byte</b>, ta chỉ tốn <b>4 MB</b>. Nếu dùng kiểu <b>8 byte</b>, chi phí tăng gấp đôi lên <b>8 MB</b>.</p>"
            "<p>Khác với ngôn ngữ thông dịch, C biên dịch thẳng ra mã máy và yêu cầu bạn làm chủ từng byte dữ liệu ngay từ dòng đầu tiên.</p>"
        ),
        "hook_say": (
            "Chào bạn đến với khoá lập trình C và quản lý bộ nhớ. "
            "Một chương trình xử lý một triệu mã giao dịch cần biết chính xác mỗi phần tử tốn bao nhiêu bai để cấp đúng bộ nhớ. "
            "Nếu chọn nhầm kiểu dữ liệu từ bốn bai sang tám bai, tổng dung lượng sẽ tăng gấp đôi ngay lập tức. "
            "Hôm nay chúng ta học cách biên dịch mã C chặt chẽ và đo chính xác kích thước từng kiểu trong bộ nhớ."
        ),
        "hook_focus": [1, 1, 2, 2],
        "hook_checks": ["1_000_000 * 4 == 4_000_000", "1_000_000 * 8 == 8_000_000"],
        "prereq_steps": [
            ak.st(
                ak.table(
                    ["kiến thức nền đã có", "vai trò trong bài này"],
                    [
                        ["Mở cửa sổ dòng lệnh và chạy tệp kịch bản", "Chạy lệnh biên dịch và thực thi tệp nhị phân tạo ra"],
                        ["Đơn vị bit và byte (1 byte = 8 bit)", "Đọc kết quả đo kích thước bộ nhớ trả về theo đơn vị byte"],
                    ],
                ),
                "Trước khi viết dòng C đầu tiên, ta nhớ lại hai nền tảng từ khoá thực hành dòng lệnh. "
                "Thứ nhất, bạn biết cách chạy lệnh và kiểm tra mã thoát trong cửa sổ dòng lệnh. "
                "Thứ hai, một bai gồm tám bít, là đơn vị đo kích thước nhỏ nhất mà ngôn ngữ C làm việc trực tiếp.",
                focus=[0, "1.2", "1.3"],
                clear=True,
            )
        ],
        "sym_steps": [
            ak.st(
                ak.table(
                    ["ký hiệu trên màn hình", "ý nghĩa"],
                    [
                        ["<code>gcc -std=c11 -Wall -Wextra -Werror</code>", "Trình biên dịch chuẩn C11, bật mọi cảnh báo và coi cảnh báo là lỗi"],
                        ["<code>sizeof(T)</code>", "Toán tử tính số byte mà kiểu <code>T</code> hoặc biến chiếm tại lúc biên dịch"],
                        ["<code>%zu</code>", "Mã định dạng dùng trong <code>printf</code> để in giá trị kiểu kích thước <code>size_t</code>"],
                    ],
                ),
                "Ta giải mã ba ký hiệu quan trọng nhất trên màn hình. "
                "Đầu tiên là bộ bốn cờ biên dịch nghiêm ngặt giúp phát hiện sớm lỗi tiềm ẩn trước khi chạy. "
                "Thứ hai là toán tử đo kích thước trả về chính xác số bai mà một kiểu dữ liệu chiếm dụng. "
                "Cuối cùng là ký hiệu định dạng dùng để in giá trị kích thước không dấu ra màn hình.",
                focus=[0, "1.2", "1.3", "1.4"],
                clear=True,
            )
        ],
        "intuition_title": "Đường đi từ mã nguồn C tới tệp nhị phân chạy thật",
        "intuition_steps": [
            ak.st(
                ak.svg_wrap(
                    960, 210,
                    ak.svg_rect(25, 55, 220, 95, "1. Mã nguồn .c", "Chữ người đọc, dùng sizeof", ak.C_BLUE)
                    + ak.svg_arrow(245, 102, 355, 102, "GCC dịch")
                    + ak.svg_rect(355, 55, 250, 95, "2. Tệp thực thi", "Mã máy 64-bit, -Werror", ak.C_AMBER)
                    + ak.svg_arrow(605, 102, 715, 102, "Nạp RAM")
                    + ak.svg_rect(715, 55, 220, 95, "3. Tiến trình chạy", "Cấp ô nhớ đúng từng byte", ak.C_GREEN),
                ),
                "Sơ đồ mô tả ba chặng biến văn bản C thành chương trình chạy trên máy. "
                "Tệp mã nguồn chứa văn bản con người viết cùng các khai báo kiểu rõ ràng. "
                "Trình biên dịch kiểm tra chặt toàn bộ quy tắc kiểu, biến dịch sang tệp mã máy thực thi. "
                "Khi chạy, hệ điều hành nạp mã máy vào bộ nhớ và cấp từng ô đúng kích thước đã xác định.",
                clear=True,
            )
        ],
        "formula_title": "Quy tắc kích thước kiểu cơ bản trên kiến trúc 64-bit",
        "formula_steps": [
            ak.st(
                ak.table(
                    ["kiểu dữ liệu C", "kích thước chuẩn đo trên máy 64-bit", "ứng dụng điển hình"],
                    [
                        ["<code>char</code>", "1 byte", "Lưu 1 ký tự hoặc 1 byte dữ liệu thô"],
                        ["<code>short</code>", "2 byte", "Số nguyên nhỏ, mã trạng thái ngắn"],
                        ["<code>int</code>", "4 byte", "Biến đếm vòng lặp, số nguyên thông dụng"],
                        ["<code>long long</code> / <code>void *</code>", "8 byte", "Số tiền lớn 64-bit và địa chỉ bộ nhớ 64-bit"],
                    ],
                ),
                "Bảng tổng hợp kích thước bốn nhóm kiểu hay dùng nhất trên hệ thống sáu mươi bốn bít. "
                "Kiểu ký tự luôn rộng đúng một bai theo chuẩn ngôn ngữ C. "
                "Kiểu số nguyên ngắn chiếm hai bai, số nguyên chuẩn chiếm bốn bai, còn số nguyên dài và địa chỉ bộ nhớ chiếm tám bai. "
                "Tuy nhiên trên thiết bị nhúng mười sáu bít hoặc ba mươi hai bít, độ rộng này có thể khác nên luôn đo bằng toán tử đo kích thước.",
                focus=[0, "1.2", "1.3", "1.4", "1.5"],
                clear=True,
            )
        ],
        "formula_checks": ["alg.cpr_sizeof_64() == {'char': 1, 'short': 2, 'int': 4, 'long_long': 8, 'ptr': 8}"],
        "example_title": "Biên dịch và chạy chương trình đo kích thước thật",
        "example_items": [
            {
                "type": "r3",
                "say": "Trước khi đọc mã C đầy đủ, ta giải mã đủ bốn thành phần trên bảng để nhìn là hiểu ngay. "
                       "Dòng đầu nạp thư viện vào ra chuẩn, dòng hai là hàm chính bắt đầu chạy. "
                       "Hàm in xuất kích thước không dấu, còn tham chiếu rỗng giúp đo kích thước một địa chỉ ô nhớ trên máy.",
                "rows": [
                    ["<code>#include &lt;stdio.h&gt;</code>", "Nạp khai báo hàm in <code>printf</code> từ thư viện chuẩn"],
                    ["<code>int main(void) { ... return 0; }</code>", "Điểm bắt đầu chạy chương trình; trả về 0 nghĩa là thành công"],
                    ["<code>printf(\"... %zu\\n\", sizeof(int));</code>", "In chữ kèm giá trị kích thước không dấu, <code>\\n</code> để xuống dòng"],
                    ["<code>sizeof(void *)</code>", "Kích thước của một biến giữ địa chỉ ô nhớ trên máy hiện tại"],
                ],
                "focus": [0, 1, 2, 3],
            },
            {
                "type": "code",
                "pid": "p1",
                "title": "Chương trình C đo kích thước các kiểu dữ liệu thật trên máy",
                "say": "Đoạn mã hoàn chỉnh chỉ gồm mười dòng nhưng dùng toán tử đo kích thước cho cả năm kiểu cơ bản rồi in thẳng ra màn hình.",
                "out_say": "Khi biên dịch và chạy thật bằng trình biên dịch C trên máy sáu mươi bốn bít, kết quả lần lượt là một, hai, bốn, tám và tám bai.",
            },
        ],
        "progs": {
            "p1": {
                "code": (
                    "#include <stdio.h>\n"
                    "int main(void) {\n"
                    '    printf("char=%zu\\n", sizeof(char));\n'
                    '    printf("short=%zu\\n", sizeof(short));\n'
                    '    printf("int=%zu\\n", sizeof(int));\n'
                    '    printf("long_long=%zu\\n", sizeof(long long));\n'
                    '    printf("ptr=%zu\\n", sizeof(void *));\n'
                    "    return 0;\n"
                    "}"
                ),
                "expect": "char=1\nshort=2\nint=4\nlong_long=8\nptr=8",
            },
            "p2": {
                "code": (
                    "#include <stdio.h>\n"
                    "int main(void) {\n"
                    "    int arr[100];\n"
                    '    printf("arr_bytes=%zu elem=%zu\\n", sizeof(arr), sizeof(arr[0]));\n'
                    '    printf("len=%zu\\n", sizeof(arr) / sizeof(arr[0]));\n'
                    "    return 0;\n"
                    "}"
                ),
                "expect": "arr_bytes=400 elem=4\nlen=100",
            },
        },
        "example_checks": ["4 * 100 == 400", "400 // 4 == 100"],
        "check_title": "Kiểm chéo bằng kích thước cả mảng và độ dài suy ngược",
        "check_items": [
            {
                "type": "code",
                "pid": "p2",
                "title": "Đo trực tiếp tổng số byte của mảng 100 phần tử int",
                "say": "Ta kiểm tra bằng một đường khác vì cần đối chiếu kích thước cả mảng: khai báo mảng một trăm số nguyên rồi lấy tổng số bai của mảng chia cho kích thước phần tử đầu.",
                "out_say": "Đầu ra thật xác nhận tổng bộ nhớ bằng đúng bốn trăm bai và phép chia ngược trả lại đúng một trăm phần tử vì mỗi phần tử chiếm bốn bai.",
            }
        ],
        "check_checks": ["400 // 4 == 100"],
        "quymo_title": "Bảng quy mô: một mảng int và long long tốn bao nhiêu RAM?",
        "quymo_steps": [
            ak.st(
                ak.table(
                    ["số phần tử n", "mảng int (4 byte)", "mảng long long (8 byte)"],
                    [
                        [ak.nowrap("100 (×1)"), "400 byte", "800 byte"],
                        [ak.nowrap("10 000 (×100)"), "40 000 byte (~39 KB)", "80 000 byte (~78 KB)"],
                        [ak.nowrap("1 000 000 (×10 000)"), "4 000 000 byte (~3,8 MB)", "8 000 000 byte (~7,6 MB)"],
                    ],
                ),
                "Nhìn bảng quy mô ta thấy mối quan hệ tuyến tính rõ rệt: gấp trăm lần số phần tử tốn gấp trăm lần bộ nhớ, gấp vạn lần tốn gấp vạn lần. "
                "Một triệu phần tử kiểu bốn bai tốn bốn triệu bai, tức gần bốn mê-ga-bai. "
                "Chọn sai kiểu dữ liệu sang tám bai làm nhân đôi toàn bộ chi phí bộ nhớ đệm khi xử lý dữ liệu lớn.",
                focus=[0, "1.2", "1.3", "1.4"],
                clear=True,
            )
        ],
        "quymo_checks": ["100 * 4 == 400", "10_000 * 4 == 40_000", "1_000_000 * 4 == 4_000_000"],
        "pitfall_steps": [
            ak.st(
                ak.box(
                    "<b>Lỗi 1: Đoán cứng int luôn bằng 4 byte mà không dùng sizeof.</b> Khi chuyển sang hệ thống nhúng 16-bit, kích thước thật chỉ còn 2 byte.<br>"
                    "<b>Lỗi 2: Bỏ qua cảnh báo lúc biên dịch.</b> Thiếu cờ <code>-Wall -Wextra -Werror</code> khiến biến chưa khởi tạo hoặc sai mã in âm thầm vượt qua.<br>"
                    "<b>Lỗi 3: Nhầm <code>sizeof(mảng)</code> khi truyền vào hàm.</b> Bên ngoài mảng biết đủ 400 byte, còn bên trong hàm chỉ nhận kích thước địa chỉ 8 byte (sẽ học kỹ ở phần sau).",
                    "warn",
                ),
                "Ba lỗi phổ biến kể cả người đã đi làm hay vấp. "
                "Thứ nhất là đoán cứng độ rộng kiểu dữ liệu thay vì dùng toán tử đo kích thước. "
                "Thứ hai là tắt cảnh báo trình biên dịch khiến lỗi định dạng hoặc biến rác chạy ngầm ngoài thực tế. "
                "Thứ ba là nhầm tổng dung lượng mảng bên ngoài với tham số nhận vào trong hàm.",
                clear=True,
            )
        ],
        "quiz_steps": [
            ak.st(
                "<ol><li>Trên hệ 64-bit, một mảng 250 phần tử kiểu <code>long long</code> chiếm bao nhiêu byte?</li>"
                "<li>Cờ biên dịch nào biến mọi cảnh báo thành lỗi bắt buộc sửa trước khi tạo tệp chạy?</li></ol>",
                "Đến lượt bạn tự kiểm tra nhanh. "
                "Câu một, trên máy sáu mươi bốn bít, mảng hai trăm năm mươi phần tử kiểu số nguyên tám bai chiếm bao nhiêu bai? "
                "Câu hai, cờ biên dịch nào biến mọi cảnh báo thành lỗi dừng biên dịch? Dừng vi-đê-ô và tính ra giấy.",
                pause=20,
            ),
            ak.st(
                "<p>① 250 × 8 = <b>2 000</b> byte.</p>",
                "Đáp án câu một: mỗi phần tử tám bai nhân hai trăm năm mươi bằng đúng hai nghìn bai.",
                clear=True,
            ),
            ak.st(
                "<p>② Cờ <code>-Werror</code> kết hợp với <code>-Wall -Wextra</code> buộc mọi cảnh báo phải được sửa sạch.</p>",
                "Đáp án câu hai: thêm cờ biến cảnh báo thành lỗi giúp chặn mọi sai sót cú pháp và kiểu ngay tại bước biên dịch.",
                clear=True,
            ),
        ],
        "quiz_checks": ["250 * 8 == 2000"],
        "recap_steps": [
            ak.st(
                "<div class='chain'><span class='n'>Chọn kiểu đúng</span><span class='a'>→</span>"
                "<span class='n'>Đo bằng sizeof</span><span class='a'>→</span>"
                "<span class='n'>Biên dịch -Wall -Wextra -Werror</span></div>",
                "Tổng kết lại, chuỗi làm việc chuẩn trong C là chọn đúng kiểu dữ liệu, đo lại bằng toán tử kích thước và luôn biên dịch nghiêm ngặt. Khi giữ thói quen này từ ngày đầu, bạn sẽ tránh được hàng loạt lỗi âm thầm về bộ nhớ ở các hệ thống lớn sau này.",
                clear=True,
            )
        ],
        "lab_de": (
            "# Lab CPR L00 — Đo kích thước kiểu cơ bản và mảng trên GCC\n\n"
            "Viết chương trình C chuẩn C11 in đúng 3 dòng sau (mỗi giá trị đo trực tiếp bằng `sizeof`):\n"
            "1. `char=1 int=4 ll=8 ptr=8`\n"
            "2. `arr50=200`\n"
            "3. `total1M=4000000`\n\n"
            "Chấm tự động bằng Git Bash:\n"
            "```bash\nbash labs/cham.sh CPR L00 duong_dan/bai_cua_ban.c\n```"
        ),
        "lab_sol": (
            "#include <stdio.h>\n"
            "int main(void) {\n"
            '    printf("char=%zu int=%zu ll=%zu ptr=%zu\\n", sizeof(char), sizeof(int), sizeof(long long), sizeof(void *));\n'
            "    int a[50];\n"
            '    printf("arr50=%zu\\n", sizeof(a));\n'
            '    printf("total1M=%zu\\n", (size_t)1000000 * sizeof(int));\n'
            "    return 0;\n"
            "}\n"
        ),
    }

    # ────────────────── L01: Biến, vòng lặp và ranh giới tràn số nguyên ──────────────────
    l01 = {
        "id": "L01",
        "slug": "bien_vong_lap_tran_so",
        "title": "Biến, vòng lặp và ranh giới tràn số nguyên trong C",
        "next_title": "Hàm, truyền tham trị và khung ngăn xếp (stack frame)",
        "assumes": [],
        "objectives": [
            "Phân biệt tràn số không dấu (quay vòng theo mô-đun 2^n) với tràn số có dấu (hành vi không xác định)",
            "Dùng đúng kiểu uint8_t, int32_t, int64_t khi cần miền giá trị cố định",
            "Viết kiểm tra chặn tràn trước khi cộng hoặc nhân số nguyên có dấu",
        ],
        "covers": [(1, "formula"), (2, "example"), (3, "check")],
        "hook_title": "Vì sao cộng thêm 10 vào 250 đôi khi lại cho ra số 4?",
        "hook_html": (
            "<p>Một bộ đếm 8-bit không dấu chỉ chứa tối đa đến <b>255</b>. Khi đang ở <b>250</b> và cộng thêm <b>10</b>, kết quả quay vòng thành <b>4</b>.</p>"
            "<p>Nhưng với số nguyên <b>có dấu</b> trong C, vượt quá cực đại không phải quay vòng an toàn mà làm trình tối ưu tạo ra <b>kết quả khó lường</b>.</p>"
        ),
        "hook_say": (
            "Chào bạn trở lại khoá lập trình C. "
            "Nếu một biến đếm tám bít không dấu đang giữ giá trị hai trăm năm mươi rồi cộng thêm mười, kết quả quay vòng thành bốn chứ không phải hai trăm sáu mươi. "
            "Nguy hiểm hơn, nếu tràn xảy ra trên số nguyên có dấu, chương trình có thể cho ra kết quả sai lệch hoàn toàn ngoài dự đoán của lập trình viên. Nhiều lỗ hổng bảo mật cấp cao phát sinh đúng từ phép cộng vượt ngưỡng kiểu có dấu như vậy."
        ),
        "hook_checks": ["(250 + 10) % 256 == 4"],
        "prereq_steps": [
            ak.st(
                ak.table(
                    ["nền tảng đã có", "áp dụng vào tràn số C"],
                    [
                        ["Kiểu 1 byte rộng 8 bit (L00)", "8 bit biểu diễn đúng 2 mũ 8 = 256 trạng thái khác nhau"],
                        ["Cờ -Wall -Wextra -Werror (L00)", "Bắt sớm lỗi trộn số có dấu và không dấu khi so sánh"],
                    ],
                ),
                "Ta nhắc nhanh hai điểm cốt lõi từ bài 0 trước khi đi sâu vào tràn số. Một bai gồm tám bít tạo ra đúng hai trăm năm mươi sáu giá trị nguyên khác nhau. Đồng thời các cờ kiểm tra lúc biên dịch luôn giúp ta phát hiện sớm lỗi trộn kiểu dữ liệu.",
                clear=True,
            )
        ],
        "sym_steps": [
            ak.st(
                ak.table(
                    ["ký hiệu mới", "ý nghĩa"],
                    [
                        ["<code>uint8_t</code> / <code>int32_t</code> / <code>int64_t</code>", "Kiểu số nguyên cố định bề rộng từ <code>&lt;stdint.h&gt;</code>"],
                        ["<code>INT32_MAX</code>", "Giá trị lớn nhất của số có dấu 32-bit bằng 2³¹ − 1 = 2 147 483 647"],
                        ["Hành vi không xác định", "Chuẩn C không bảo đảm kết quả nếu tràn số có dấu; không được phép phụ thuộc"],
                    ],
                ),
                "Trên bảng là ba quy ước của bài hôm nay. "
                "Thư viện chuẩn cố định bề rộng cung cấp các kiểu số tám bít không dấu, ba mươi hai bít và sáu mươi bốn bít có dấu đồng nhất trên mọi máy. "
                "Điểm then chốt cần nhớ là tràn số nguyên có dấu tạo ra hành vi không xác định nên bắt buộc phải kiểm tra điều kiện trước khi cộng hoặc nhân.",
                introduces=["cpr_ub"],
                focus=[0, "1.2", "1.3", "1.4"],
                clear=True,
            )
        ],
        "intuition_title": "Đồng hồ quay vòng mô-đun 256 của số không dấu",
        "intuition_steps": [
            ak.st(
                ak.svg_wrap(
                    960, 210,
                    ak.svg_rect(35, 55, 250, 95, "uint8_t = 250", "8 bit: 11111010", ak.C_BLUE)
                    + ak.svg_arrow(285, 102, 365, 102, "+ 10 bước")
                    + ak.svg_rect(365, 55, 250, 95, "Vượt 255", "Bit nhớ thứ 9 bị cắt bỏ", ak.C_AMBER)
                    + ak.svg_arrow(615, 102, 695, 102, "mod 256")
                    + ak.svg_rect(695, 55, 230, 95, "Kết quả = 4", "00000100 (quay vòng)", ak.C_GREEN),
                ),
                "Hình dung tám bít như mặt đồng hồ có hai trăm năm mươi sáu vạch từ không đến hai trăm năm mươi lăm. "
                "Khi từ hai trăm năm mươi tiến thêm mười bước, kim đi qua vạch không rồi dừng tại bốn vì bít thứ chín tràn ra ngoài thanh ghi tám bít. Bất kỳ phép cộng không dấu nào cũng tự động lấy phần dư theo đúng chu kỳ này.",
                clear=True,
            )
        ],
        "formula_title": "Quy tắc an toàn trước phép cộng và nhân có dấu",
        "formula_steps": [
            ak.st(
                ak.box(
                    "<p><b>Định lý chuẩn C11:</b></p>"
                    "<ul><li>Số <b>không dấu</b> $k$ bit cộng tràn luôn tính theo mod 2ᵏ.</li>"
                    "<li>Số <b>có dấu</b> tuyệt đối không được vượt <code>INT32_MAX</code>: muốn kiểm a + b (với b &gt; 0), kiểm <code>a &gt; INT32_MAX - b</code> <b>trước</b> khi cộng.</li></ul>",
                    "key",
                ),
                "Để không rơi vào hành vi không xác định trên số có dấu, ta luôn chuyển vế phép so sánh sang phép trừ trước khi thực hiện phép cộng. "
                "Thay vì viết phép cộng dễ tràn rồi mới kiểm, ta kiểm xem số thứ nhất có vượt ngưỡng trừ đi số thứ hai hay chưa. Cách chuyển vế này hoàn toàn an toàn vì phép trừ số dương khỏi giá trị cực đại không bao giờ bị tràn.",
                clear=True,
            )
        ],
        "formula_checks": ["alg.cpr_u8_wrap(250, 10) == 4", "2**31 - 1 == 2_147_483_647"],
        "example_title": "Chạy thật trên GCC: số 8 bít không dấu và vòng lặp chặn tràn",
        "example_items": [
            {
                "type": "r3",
                "say": "Trước khi xem mã hoàn chỉnh, ta giải thích đủ bốn quy ước xuất hiện trong chương trình. Thư viện cố định bề rộng cung cấp cả các hằng biên trên dưới cho số ba mươi hai bít. Mã định dạng phần trăm u và d in lần lượt số không dấu và có dấu, từ khoá giới hạn nội bộ giữ hàm trong tệp, còn dấu và kép nối hai điều kiện đúng đồng thời.",
                "rows": [
                    ["<code>#include &lt;stdint.h&gt;</code>", "Cung cấp <code>uint8_t</code>, <code>int32_t</code> và hằng <code>INT32_MAX</code>, <code>INT32_MIN</code>"],
                    ["<code>%u</code> / <code>%d</code>", "Định dạng in số nguyên <b>không dấu</b> (<code>%u</code>) và <b>có dấu</b> (<code>%d</code>)"],
                    ["<code>static</code> / <code>&amp;&amp;</code>", "Giới hạn hàm nội bộ tệp; phép <b>VÀ</b> logic đúng khi cả hai vế đúng"],
                    ["<code>(uint8_t)(u + 10)</code>", "Ép rõ về 8-bit không dấu (tránh cảnh báo chuyển kiểu của GCC)"],
                ],
                "focus": [0, 1, 2, 3],
            },
            {
                "type": "code",
                "pid": "p1",
                "title": "Thử thật phép cộng quay vòng uint8_t và tổng vòng lặp an toàn",
                "say": "Chương trình thử cộng mười vào biến tám bít không dấu đang giữ giá trị hai trăm năm mươi. Sau đó vòng lặp cộng dồn mười số nguyên đầu tiên với điều kiện dừng rõ ràng.",
                "out_say": "Kết quả chạy thật trên trình biên dịch C xác nhận giá trị quay vòng đúng bằng bốn vì hai trăm sáu mươi chia hai trăm năm mươi sáu dư bốn. Tổng vòng lặp mười bước trả về năm mươi lăm khớp công thức toán học.",
            },
        ],
        "progs": {
            "p1": {
                "code": (
                    "#include <stdio.h>\n"
                    "#include <stdint.h>\n"
                    "int main(void) {\n"
                    "    uint8_t u = 250;\n"
                    "    uint8_t wrapped = (uint8_t)(u + 10);\n"
                    '    printf("u8=%u\\n", wrapped);\n'
                    "    int32_t sum = 0;\n"
                    "    for (int i = 1; i <= 10; i++) { sum += i; }\n"
                    '    printf("sum=%d\\n", sum);\n'
                    "    return 0;\n"
                    "}"
                ),
                "expect": "u8=4\nsum=55",
            },
            "p2": {
                "code": (
                    "#include <stdio.h>\n"
                    "#include <stdint.h>\n"
                    "static int safe_add_ok(int32_t a, int32_t b) {\n"
                    "    if (b > 0 && a > INT32_MAX - b) return 0;\n"
                    "    if (b < 0 && a < INT32_MIN - b) return 0;\n"
                    "    return 1;\n"
                    "}\n"
                    "int main(void) {\n"
                    "    int32_t a = 2000000000, b1 = 100000000, b2 = 200000000;\n"
                    "    int ok1 = safe_add_ok(a, b1), ok2 = safe_add_ok(a, b2);\n"
                    "    int32_t res = ok1 ? (a + b1) : 0;\n"
                    '    printf("ok1=%d res=%d ok2=%d\\n", ok1, res, ok2);\n'
                    "    return 0;\n"
                    "}"
                ),
                "expect": "ok1=1 res=2100000000 ok2=0",
            },
        },
        "example_checks": ["sum(range(1, 11)) == 55", "alg.cpr_u8_wrap(250, 10) == 4"],
        "check_title": "Kiểm chứng hàm cộng an toàn chặn tràn trước khi cộng",
        "check_items": [
            {
                "type": "code",
                "pid": "p2",
                "title": "Hàm safe_add_ok chặn trước trường hợp 2 tỉ + 200 triệu > INT32_MAX",
                "say": "Ta dùng đường kiểm chứng thứ hai bằng cách viết hàm kiểm tra ranh giới trước khi thực hiện phép cộng. Phép thử hai tỉ cộng một trăm triệu cho tổng hai tỉ một trăm triệu vẫn nhỏ hơn ngưỡng tối đa nên được phép chạy. Ngược lại phép cộng hai trăm triệu vượt ngưỡng nên bị chặn ngay.",
                "out_say": "Đầu ra thật khớp hoàn toàn với phân tích trước đó vì hàm kiểm tra đã chặn đứng phép cộng vượt biên. Phép thứ nhất hợp lệ trả về cờ một và tổng đúng, còn phép thứ hai trả về cờ bằng không.",
            }
        ],
        "check_checks": ["2_000_000_000 + 100_000_000 < 2**31", "2_000_000_000 + 200_000_000 >= 2**31"],
        "quymo_title": "Miền an toàn theo độ rộng bit của số nguyên",
        "quymo_steps": [
            ak.st(
                ak.table(
                    ["độ rộng", "kiểu không dấu max", "kiểu có dấu max", "ngưỡng giao dịch tiền"],
                    [
                        [ak.nowrap("8 bit (×1)"), "255", "127", "Không đủ đếm giao dịch"],
                        [ak.nowrap("32 bit (×4)"), "4 294 967 295", "2 147 483 647", "Tràn ngay nếu vượt 2,14 tỉ đồng"],
                        [ak.nowrap("64 bit (×8)"), "18 446 744 073 709 551 615", "9 223 372 036 854 775 807", "An toàn cho tổng tiền ngân hàng"],
                    ],
                ),
                "Bảng đối chiếu ba độ rộng số nguyên cho thấy lý do hệ thống thanh toán cấm dùng kiểu ba mươi hai bít cho số tiền. "
                "Giới hạn hơn hai tỉ một trăm triệu sẽ bị vượt qua chỉ trong một giao dịch chuyển khoản doanh nghiệp lớn. "
                "Ở hàng dưới, kiểu sáu mươi bốn bít chịu được hàng tỉ tỉ đồng. Vì thế số tiền luôn phải đặt trong kiểu sáu mươi bốn bít có kiểm tra biên.",
                focus=[0, "1.2", "1.3", "1.4"],
                clear=True,
            )
        ],
        "quymo_checks": ["2**8 - 1 == 255", "2**31 - 1 == 2_147_483_647"],
        "pitfall_steps": [
            ak.st(
                ak.box(
                    "<b>Lỗi 1: Viết <code>if (a + b &lt; a)</code> để bắt tràn có dấu.</b> Phép cộng đã tràn trước lúc so sánh, là hành vi không xác định nên trình biên dịch có quyền xoá hẳn câu lệnh <code>if</code>.<br>"
                    "<b>Lỗi 2: Dùng <code>uint8_t i</code> đếm lùi <code>i &gt;= 0</code>.</b> Khi <code>i = 0</code> rồi trừ 1, biến không dấu nhảy lên 255 tạo vòng lặp vô hạn.<br>"
                    "<b>Lỗi 3: Nhầm tràn int 32-bit khi tính chỉ số mảng lớn.</b> Phép nhân <code>n * sizeof(T)</code> cần ép sang <code>size_t</code> trước.",
                    "warn",
                ),
                "Có ba bẫy tràn số thực tế rất hay gặp khi viết mã C. Kiểm tra sau khi cộng là hành vi không xác định nên trình biên dịch có thể xoá sạch câu lệnh kiểm tra. Đếm lùi biến không dấu tới không sẽ quay vòng thành hai trăm năm mươi lăm gây lặp vô tận. Cuối cùng là nhân kích thước mảng mà quên ép sang kiểu kích thước không dấu lớn.",
                clear=True,
            )
        ],
        "quiz_steps": [
            ak.st(
                "<ol><li><code>uint8_t x = 200; uint8_t y = (uint8_t)(x + 70);</code> cho giá trị <code>y</code> bằng bao nhiêu?</li>"
                "<li>Viết điều kiện kiểm tra tràn <b>trước</b> khi cộng hai số dương <code>a, b</code> kiểu <code>int32_t</code>.</li></ol>",
                "Đến lượt bạn tự kiểm tra. "
                "Câu một, biến tám bít không dấu giữ hai trăm cộng thêm bảy mươi cho kết quả bằng bao nhiêu? "
                "Câu hai, viết điều kiện kiểm tra tràn trước khi cộng hai số dương ba mươi hai bít. Dừng vi-đê-ô và làm ra giấy.",
                pause=20,
            ),
            ak.st(
                "<p>① (200 + 70) mod 256 = 270 − 256 = <b>14</b>.</p>",
                "Đáp án câu một: hai trăm cộng bảy mươi bằng hai trăm bảy mươi, trừ hai trăm năm mươi sáu còn mười bốn.",
                clear=True,
            ),
            ak.st(
                "<p>② Kiểm tra <code>if (a &gt; INT32_MAX - b)</code> trước khi thực hiện <code>a + b</code>.</p>",
                "Đáp án câu hai: chuyển số hạng sang vế trừ để so sánh trước khi phép cộng kịp xảy ra.",
                clear=True,
            ),
        ],
        "quiz_checks": ["(200 + 70) % 256 == 14"],
        "recap_steps": [
            ak.st(
                "<div class='chain'><span class='n'>Không dấu: mod 2^n</span><span class='a'>|</span>"
                "<span class='n'>Có dấu tràn: không xác định</span><span class='a'>→</span>"
                "<span class='n'>Luôn kiểm trước khi tính</span></div>",
                "Ghi nhớ chuỗi quy tắc cốt lõi của bài hôm nay. Số không dấu quay vòng theo lũy thừa hai, còn tràn số có dấu là hành vi không xác định cực kỳ nguy hiểm. Mọi phép kiểm tra biên bắt buộc phải đặt trước khi phép tính diễn ra.",
                clear=True,
            )
        ],
        "lab_de": (
            "# Lab CPR L01 — Kiểm tra quay vòng uint8_t và chặn tràn int32_t\n\n"
            "Viết chương trình C chuẩn C11 thực hiện và in đúng 3 dòng:\n"
            "1. Giá trị `uint8_t` của `(250 + 10)`: `wrap=4`\n"
            "2. Cộng có kiểm tra `2147483640 + 7`: `add1=2147483647`\n"
            "3. Cộng có kiểm tra `2147483640 + 8` (bị chặn tràn): `add2=OVERFLOW`\n\n"
            "Chấm tự động:\n```bash\nbash labs/cham.sh CPR L01 duong_dan/bai_cua_ban.c\n```"
        ),
        "lab_sol": (
            "#include <stdio.h>\n"
            "#include <stdint.h>\n"
            "int main(void) {\n"
            "    uint8_t u = (uint8_t)(250 + 10);\n"
            '    printf("wrap=%u\\n", u);\n'
            "    int32_t a = 2147483640, b1 = 7, b2 = 8;\n"
            "    if (a <= INT32_MAX - b1) printf(\"add1=%d\\n\", a + b1); else printf(\"add1=OVERFLOW\\n\");\n"
            "    if (a <= INT32_MAX - b2) printf(\"add2=%d\\n\", a + b2); else printf(\"add2=OVERFLOW\\n\");\n"
            "    return 0;\n"
            "}\n"
        ),
    }

    # ────────────────── L02: Hàm, truyền tham trị và khung ngăn xếp ──────────────────
    l02 = {
        "id": "L02",
        "slug": "ham_ngan_xep",
        "title": "Hàm, truyền tham trị và khung ngăn xếp (stack frame)",
        "next_title": "Mảng và chuỗi ký tự kết thúc bằng byte không",
        "assumes": ["cpr_ub"],
        "objectives": [
            "Giải thích vì sao hàm nhận bản sao giá trị nên sửa tham số không đổi biến ngoài",
            "Cộng kích thước khung ngăn xếp qua 3 tầng gọi hàm và nhận diện nguy cơ tràn ngăn xếp",
            "Chỉ ra vì sao không được dùng giá trị biến cục bộ sau khi hàm đã trả về",
        ],
        "covers": [(1, "example"), (2, "quymo"), (3, "pitfalls")],
        "hook_title": "Vì sao hàm hoán đổi viết bình thường lại không đổi được giá trị ngoài?",
        "hook_html": (
            "<p>Bạn gọi <code>swap(x, y)</code> với <b>x = 10, y = 25</b>, nhưng sau lệnh gọi, <b>x</b> vẫn là <b>10</b> và <b>y</b> vẫn là <b>25</b>.</p>"
            "<p>Lý do nằm ở cơ chế <b>truyền tham trị</b> và cách mỗi lời gọi hàm mở rồi thu hồi một <b>khung ngăn xếp</b> riêng.</p>"
        ),
        "hook_say": (
            "Chào bạn, nhiều người mới bất ngờ khi viết hàm hoán đổi hai biến trong C nhưng biến bên ngoài không hề thay đổi giá trị. "
            "Lý do nằm ở hai khái niệm cốt lõi: C luôn truyền bản sao giá trị vào hàm, và mỗi hàm đang chạy sở hữu một khung bộ nhớ cục bộ trên ngăn xếp. "
            "Khi hàm kết thúc, khung bộ nhớ đó bị thu hồi ngay lập tức. Hiểu cơ chế ngăn xếp này còn giúp bạn tránh luôn lỗi tràn bộ nhớ khi khai báo mảng lớn hoặc viết hàm đệ quy sâu."
        ),
        "hook_checks": ["10 != 25"],
        "prereq_steps": [
            ak.st(
                ak.table(
                    ["nền tảng đã có", "liên hệ bài mới"],
                    [
                        ["Biến có kích thước byte xác định (L00)", "Khung ngăn xếp bằng tổng kích thước các biến cục bộ cộng phần quản lý"],
                        ["Hành vi không xác định (L01)", "Đọc vùng ngăn xếp đã thu hồi sau khi hàm kết thúc là hành vi không xác định"],
                    ],
                ),
                "Ta nối tiếp bài 0 và bài 1 để giải thích cách hàm quản lý bộ nhớ tạm. Mỗi biến cục bộ chiếm một số bai xác định bên trong khung ngăn xếp của hàm đó. Khi hàm thoát ra, vùng nhớ cục bộ hết hạn ngay và mọi truy cập lại đều là hành vi không xác định.",
                clear=True,
            )
        ],
        "sym_steps": [
            ak.st(
                ak.table(
                    ["thuật ngữ", "ý nghĩa"],
                    [
                        ["Truyền tham trị", "Hàm nhận <b>bản sao</b> của giá trị đối số đặt vào khung ngăn xếp mới"],
                        ["Khung ngăn xếp", "Vùng nhớ cấp tự động theo kiểu vào sau ra trước cho mỗi lần gọi hàm"],
                        ["Biến cục bộ", "Biến khai báo bên trong thân hàm, tự động huỷ ngay khi gặp <code>return</code>"],
                    ],
                ),
                "Ba khái niệm cần nhớ trong bài hôm nay là truyền tham trị, khung ngăn xếp và biến cục bộ. "
                "Hàm luôn làm việc trên bản sao riêng đặt trong khung ngăn xếp của nó và tự giải phóng ngay lúc trả kết quả.",
                focus=[0, "1.2", "1.3", "1.4"],
                clear=True,
            )
        ],
        "intuition_title": "Khung ngăn xếp xếp chồng khi gọi hàm và thu hồi khi trả về",
        "intuition_steps": [
            ak.st(
                ak.svg_wrap(
                    960, 220,
                    ak.svg_rect(25, 35, 220, 150, "Khung hàm main", "x = 10, y = 25 (ngoài hàm)", ak.C_BLUE)
                    + ak.svg_arrow(245, 110, 365, 110, "Chép 10, 25")
                    + ak.svg_rect(365, 35, 240, 150, "Khung swap_thu", "a = 25, b = 10 (bản sao)", ak.C_AMBER)
                    + ak.svg_arrow(605, 110, 725, 110, "return → xoá")
                    + ak.svg_rect(725, 35, 210, 150, "Sau lời gọi", "x vẫn 10, y vẫn 25", ak.C_RED),
                ),
                "Nhìn sơ đồ khung ngăn xếp đang xếp cạnh nhau trên màn hình. Khung của hàm chính nắm giữ hai biến x bằng mười và y bằng hai mươi lăm. "
                "Khi gọi hàm hoán đổi thử, hệ thống mở một khung mới rồi chép hai giá trị sang hai ô nhớ tách biệt. "
                "Mọi phép đổi giá trị chỉ xảy ra trên hai ô nhớ bản sao cục bộ bên trong khung mới. Khi hàm hoán đổi vừa kết thúc, toàn bộ khung thứ hai bị thu hồi nên hai biến ban đầu ngoài hàm chính không hề thay đổi.",
                clear=True,
            )
        ],
        "formula_title": "Cộng kích thước khung ngăn xếp và định luật vào sau ra trước",
        "formula_steps": [
            ak.st(
                ak.box(
                    "<p>Nếu chuỗi gọi hàm <code>main → f1 → f2</code> có kích thước khung lần lượt <b>32</b>, <b>48</b> và <b>64 byte</b>:</p>"
                    "<p>Tổng độ sâu ngăn xếp lúc <code>f2</code> đang chạy $= 32 + 48 + 64 = \\hl{144}$ byte. Khi <code>f2</code> kết thúc, 64 byte được thu hồi ngay.</p>",
                    "key",
                ),
                "Khi hàm chính gọi hàm một rồi hàm một gọi hàm hai, ba khung xếp chồng lên nhau. Tổng dung lượng ngăn xếp đạt ba mươi hai cộng bốn mươi tám cộng sáu mươi bốn bằng một trăm bốn mươi bốn bai. "
                "Ngăn xếp mặc định của hệ điều hành thường chỉ rộng từ một đến tám mê-ga-bai nên cấp mảng quá lớn trên đó sẽ tràn ngay. Vì thế mọi dữ liệu kích thước lớn phải chuyển ra khỏi biến cục bộ.",
                clear=True,
            )
        ],
        "formula_checks": ["alg.cpr_stack_bytes([32, 48, 64]) == 144"],
        "example_title": "Chạy thật trên GCC: chứng minh bản sao giữ nguyên biến gốc",
        "example_items": [
            {
                "type": "r3",
                "say": "Trước khi chạy mã, ta giải mã ba quy ước hàm cơ bản trong C. Từ khoá hàm nội bộ không trả về giúp thực hiện tác vụ mà không xuất giá trị. Định dạng phần trăm d in số nguyên có dấu, còn câu lệnh kiểm tra nhỏ hơn không chặn điểm dừng đệ quy.",
                "rows": [
                    ["<code>static void ham(int a, int b)</code>", "Hàm phụ nội bộ nhận bản sao <code>a, b</code> và không trả về giá trị"],
                    ["<code>printf(\"... %d\\n\", x)</code>", "In chuỗi kèm giá trị số nguyên có dấu <code>int</code>"],
                    ["<code>if (n &lt;= 0) return 0;</code>", "Điều kiện dừng đệ quy trước khi gọi lại chính hàm đó"],
                ],
                "focus": [0, 1, 2],
            },
            {
                "type": "code",
                "pid": "p1",
                "title": "Thử hoán đổi bằng tham trị: biến gốc ở main vẫn không đổi",
                "say": "Trong hàm hoán đổi thử, ta hoán đổi giá trị của a và b thông qua biến tạm rồi in kết quả ngay bên trong hàm. Sau khi hàm trả về, hàm chính in lại cặp biến x và y để chứng minh biến gốc ngoài hàm không hề bị tác động.",
                "out_say": "Đầu ra chạy thật khớp lý thuyết: bên trong hàm bản sao đã đảo thành hai mươi lăm và mười. Tuy nhiên khi thoát về hàm chính, hai biến x và y vẫn giữ nguyên mười và hai mươi lăm vì khung bộ nhớ kia đã biến mất.",
            },
        ],
        "progs": {
            "p1": {
                "code": (
                    "#include <stdio.h>\n"
                    "static void swap_copy(int a, int b) {\n"
                    "    int tmp = a; a = b; b = tmp;\n"
                    '    printf("inside: a=%d b=%d\\n", a, b);\n'
                    "}\n"
                    "int main(void) {\n"
                    "    int x = 10, y = 25;\n"
                    "    swap_copy(x, y);\n"
                    '    printf("outside: x=%d y=%d\\n", x, y);\n'
                    "    return 0;\n"
                    "}"
                ),
                "expect": "inside: a=25 b=10\noutside: x=10 y=25",
            },
            "p2": {
                "code": (
                    "#include <stdio.h>\n"
                    "static int sum_rec(int n) {\n"
                    "    if (n <= 0) return 0;\n"
                    "    return n + sum_rec(n - 1);\n"
                    "}\n"
                    "int main(void) {\n"
                    '    printf("sum5=%d sum10=%d\\n", sum_rec(5), sum_rec(10));\n'
                    "    return 0;\n"
                    "}"
                ),
                "expect": "sum5=15 sum10=55",
            },
        },
        "example_checks": ["10 != 25"],
        "check_title": "Kiểm chứng độ sâu đệ quy: mỗi lần gọi mở một khung riêng",
        "check_items": [
            {
                "type": "code",
                "pid": "p2",
                "title": "Tổng đệ quy 1..n: mỗi tầng giữ biến n độc lập trên ngăn xếp",
                "say": "Ở đường kiểm chứng thứ hai, ta tính tổng cộng dồn đệ quy từ một đến năm và một đến mười vì mỗi lần gọi tự tạo một khung riêng. Mỗi khung giữ một biến đếm n độc lập trên ngăn xếp nên không bao giờ đè lên giá trị của lần gọi trước.",
                "out_say": "Đầu ra thật trả về đúng mười lăm và năm mươi lăm, khớp công thức toán học n nhân n cộng một chia đôi vì các khung xếp chồng cộng ngược từ điểm dừng đi lên.",
            }
        ],
        "check_checks": ["sum(range(1, 6)) == 15", "sum(range(1, 11)) == 55"],
        "quymo_title": "Bảng quy mô: khi nào ngăn xếp bị tràn (Stack Overflow)?",
        "quymo_steps": [
            ak.st(
                ak.table(
                    ["dữ liệu đặt trên ngăn xếp", "dung lượng chiếm (4 byte/int)", "trạng thái trên ngăn xếp ~1–8 MB"],
                    [
                        [ak.nowrap("1 000 số (×1)"), "4 000 byte (~4 KB)", "An toàn hoàn toàn"],
                        [ak.nowrap("100 000 số (×100)"), "400 000 byte (~390 KB)", "Cẩn thận nếu lồng nhiều hàm"],
                        [ak.nowrap("10 000 000 số (×10 000)"), "40 000 000 byte (~38 MB)", "Tràn ngăn xếp — sập chương trình ngay"],
                    ],
                ),
                "Bảng quy mô giải thích vì sao ta không được đặt mảng lớn lên ngăn xếp. "
                "Một nghìn phần tử chỉ tốn bốn ki-lô-bai nên rất an toàn. Ở mức trung bình một trăm nghìn phần tử tốn bốn trăm ki-lô-bai vẫn nằm gọn trên một số máy nhưng rất chật. Ngược lại, mười triệu phần tử tốn gần bốn mươi mê-ga-bai, vượt xa giới hạn mặc định của hệ điều hành và làm sập ngay chương trình.",
                focus=[0, "1.2", "1.3", "1.4"],
                clear=True,
            )
        ],
        "quymo_checks": ["1000 * 4 == 4000", "10_000_000 * 4 == 40_000_000"],
        "pitfall_steps": [
            ak.st(
                ak.box(
                    "<b>Lỗi 1: Nghĩ rằng thay đổi tham số hàm tự đổi biến ngoài.</b> Trong C muốn sửa biến ngoài phải truyền địa chỉ ô nhớ.<br>"
                    "<b>Lỗi 2: Đặt mảng kích thước hàng triệu phần tử làm biến cục bộ.</b> Ngăn xếp tràn trước khi dòng lệnh đầu tiên kịp chạy.<br>"
                    "<b>Lỗi 3: Đệ quy không có điều kiện dừng hoặc quá sâu.</b> Hàng trăm nghìn tầng gọi làm cạn toàn bộ ngăn xếp.",
                    "warn",
                ),
                "Có ba lỗi thường gặp khi dùng hàm và ngăn xếp trong C. Lỗi đầu là sửa bản sao tham số mà tưởng đã đổi được biến ngoài hàm. Hai lỗi sau là khai báo mảng quá lớn ngay trong hàm hoặc viết hàm đệ quy thiếu điểm dừng gây tràn ngăn xếp tức thì.",
                clear=True,
            )
        ],
        "quiz_steps": [
            ak.st(
                "<ol><li>Bốn khung ngăn xếp xếp chồng có cỡ 24, 40, 56 và 80 byte thì tổng dung lượng đang chiếm là bao nhiêu?</li>"
                "<li>Nếu muốn giữ lại mảng 5 triệu số <code>int</code> (~20 MB), có nên đặt làm biến cục bộ trên ngăn xếp không?</li></ol>",
                "Đến lượt bạn tự kiểm tra. "
                "Câu một, bốn khung ngăn xếp có kích thước lần lượt hai mươi tư, bốn mươi, năm mươi sáu và tám mươi bai thì tổng dung lượng bằng bao nhiêu? "
                "Câu hai, có nên khai báo mảng năm triệu số nguyên làm biến cục bộ trong hàm không? Dừng vi-đê-ô và trả lời.",
                pause=20,
            ),
            ak.st(
                "<p>① 24 + 40 + 56 + 80 = <b>200</b> byte.</p>",
                "Đáp án câu một: cộng bốn khung lại cho tổng hai trăm bai.",
                clear=True,
            ),
            ak.st(
                "<p>② <b>Không:</b> mảng ~20 MB vượt ngưỡng ngăn xếp mặc định trên Windows (1 MB) và Linux (8 MB), dễ gây tràn ngăn xếp.</p>",
                "Đáp án câu hai: không được đặt mảng hai mươi mê-ga-bai trên ngăn xếp, mà phải cấp phát trên vùng nhớ mở.",
                clear=True,
            ),
        ],
        "quiz_checks": ["alg.cpr_stack_bytes([24, 40, 56, 80]) == 200"],
        "recap_steps": [
            ak.st(
                "<div class='chain'><span class='n'>Truyền tham trị = bản sao</span><span class='a'>→</span>"
                "<span class='n'>Khung ngăn xếp tự huỷ khi return</span><span class='a'>→</span>"
                "<span class='n'>Dữ liệu lớn không đặt trên ngăn xếp</span></div>",
                "Tổng kết lại ba điểm cần mang theo từ bài 2. Truyền tham trị luôn tạo bản sao, biến cục bộ hết hạn ngay khi hàm trả kết quả, và tuyệt đối không nhồi mảng lớn lên ngăn xếp.",
                clear=True,
            )
        ],
        "lab_de": (
            "# Lab CPR L02 — Kiểm chứng truyền tham trị và tính cộng dồn khung ngăn xếp\n\n"
            "Viết chương trình C chuẩn C11 có hàm `double_val(int x)` cộng thêm gấp đôi trên bản sao và hàm đệ quy `sum_to(int n)`, in đúng 2 dòng:\n"
            "1. `after_call=7`\n"
            "2. `sum8=36 stack_frames=144`\n"
            "(với 3 khung mẫu cộng lại `32 + 48 + 64 = 144`).\n\n"
            "Chấm tự động:\n```bash\nbash labs/cham.sh CPR L02 duong_dan/bai_cua_ban.c\n```"
        ),
        "lab_sol": (
            "#include <stdio.h>\n"
            "static void double_val(int x) { x = x * 2; (void)x; }\n"
            "static int sum_to(int n) { return n <= 0 ? 0 : n + sum_to(n - 1); }\n"
            "int main(void) {\n"
            "    int v = 7;\n"
            "    double_val(v);\n"
            '    printf("after_call=%d\\n", v);\n'
            '    printf("sum8=%d stack_frames=%d\\n", sum_to(8), 32 + 48 + 64);\n'
            "    return 0;\n"
            "}\n"
        ),
    }

    # ────────────────── L03: Mảng và chuỗi ký tự '\0' ──────────────────
    l03 = {
        "id": "L03",
        "slug": "mang_chuoi_c",
        "title": "Mảng và chuỗi ký tự kết thúc bằng byte không",
        "next_title": "Con trỏ và địa chỉ bộ nhớ: toán tử & và *",
        "assumes": ["cpr_ub"],
        "objectives": [
            "Tính đúng số byte đệm tối thiểu = độ dài chuỗi + 1 byte kết thúc '\\0'",
            "Phân biệt sao chép có giới hạn độ dài với hàm không kiểm biên gây tràn bộ đệm",
            "Chặn đọc quá chỉ số cuối mảng n phần tử (0..n-1)",
        ],
        "covers": [(1, "formula"), (2, "example"), (3, "pitfalls")],
        "hook_title": "Thiếu đúng 1 byte cho ký tự không mà hàng nghìn phần mềm bị tấn công?",
        "hook_html": (
            "<p>Chuỗi <code>\"NGUYEN\"</code> có <b>6 ký tự</b>, nhưng nếu khai báo mảng <code>char buf[6]</code> thì bạn vừa tạo ra một lỗi tràn ranh giới nghiêm trọng.</p>"
            "<p>Chuỗi trong C bắt buộc có thêm <b>1 byte bằng 0</b> (<code>'\\0'</code>) ở cuối để các hàm biết điểm dừng.</p>"
        ),
        "hook_say": (
            "Chào bạn, nếu chuỗi chữ có sáu ký tự mà bạn chỉ cấp vùng đệm đúng sáu bai, chương trình sẽ thiếu chỗ cho bai đánh dấu kết thúc bằng không. "
            "Khi thiếu dấu chặn cuối, hàm đọc chuỗi tiếp tục chạy tràn sang các biến lân cận trong bộ nhớ. Hàng loạt lỗ hổng bảo mật nổi tiếng xuất phát đúng từ lỗi tràn bộ đệm thiếu một bai kết thúc này."
        ),
        "hook_checks": ["alg.cpr_str_bytes(5) == 6", "alg.cpr_str_bytes(6) == 7"],
        "prereq_steps": [
            ak.st(
                ak.table(
                    ["nền tảng đã có", "áp dụng vào chuỗi C"],
                    [
                        ["Mỗi ký tự char chiếm đúng 1 byte (L00)", "Độ dài byte bằng đúng số ký tự cộng một byte kết thúc"],
                        ["Biến cục bộ nằm kề trên ngăn xếp (L02)", "Ghi tràn quá chỉ số cuối mảng có thể ghi đè biến nằm cạnh"],
                    ],
                ),
                "Nhờ bài 0 và bài 2, ta biết mỗi ký tự trong bảng mã chuẩn chỉ tốn một bai bộ nhớ. Trên ngăn xếp các mảng cục bộ nằm kề sát nhau nên chỉ cần ghi lố một bai là đủ làm hỏng dữ liệu của biến lân cận.",
                clear=True,
            )
        ],
        "sym_steps": [
            ak.st(
                ak.table(
                    ["ký hiệu mới", "ý nghĩa"],
                    [
                        ["<code>'\\0'</code>", "Byte có giá trị số bằng 0 đánh dấu hết chuỗi ký tự trong C"],
                        ["<code>strlen(s)</code>", "Đếm số byte trước dấu <code>'\\0'</code> (không tính byte 0 vào độ dài)"],
                        ["<code>snprintf(dst, cap, ...)</code>", "Ghi an toàn tối đa <code>cap - 1</code> ký tự rồi luôn tự chèn <code>'\\0'</code>"],
                    ],
                ),
                "Có ba ký hiệu cần ghi nhớ khi xử lý chuỗi C. Mọi chuỗi chuẩn đều phải kết thúc bằng bai giá trị không. Hàm đếm độ dài chỉ tính phần chữ đứng trước bai không đó. Khi ghi chuỗi có giới hạn dung lượng, hàm chuẩn luôn tự chừa một bai cuối cho dấu kết thúc.",
                focus=[0, "1.2", "1.3", "1.4"],
                clear=True,
            )
        ],
        "intuition_title": "Sơ đồ từng ô nhớ của chuỗi 5 chữ cái trong mảng 6 byte",
        "intuition_steps": [
            ak.st(
                ak.svg_wrap(
                    960, 180,
                    ak.svg_rect(40, 45, 110, 80, "[0] 'H'", "1 byte", ak.C_BLUE)
                    + ak.svg_rect(165, 45, 110, 80, "[1] 'E'", "1 byte", ak.C_BLUE)
                    + ak.svg_rect(290, 45, 110, 80, "[2] 'L'", "1 byte", ak.C_BLUE)
                    + ak.svg_rect(415, 45, 110, 80, "[3] 'L'", "1 byte", ak.C_BLUE)
                    + ak.svg_rect(540, 45, 110, 80, "[4] 'O'", "1 byte", ak.C_BLUE)
                    + ak.svg_rect(675, 45, 240, 80, "[5] '\\0' (số 0)", "Bắt buộc để dừng đọc", ak.C_GREEN),
                ),
                "Chuỗi gồm năm chữ cái xếp liên tiếp từ chỉ số không đến chỉ số bốn. "
                "Ô thứ sáu mang chỉ số năm chứa bai giá trị không để báo cho mọi hàm biết nơi kết thúc chuỗi. Vì phải chừa một ô cuối cho ký tự không này nên tổng kích thước mảng tối thiểu luôn phải bằng năm cộng một là sáu bai.",
                clear=True,
            )
        ],
        "formula_title": "Công thức tính bộ đệm tối thiểu và chỉ số hợp lệ",
        "formula_steps": [
            ak.st(
                ak.box(
                    "<p>Mảng <code>a[n]</code> chỉ có các chỉ số hợp lệ từ <b>0</b> tới <b>n − 1</b>.</p>"
                    "<p>Chuỗi dài L ký tự đòi kích thước mảng tối thiểu L + 1 byte (với 5 ký tự cần ít nhất 6 byte).</p>",
                    "key",
                ),
                "Công thức nền tảng rất gọn nhưng không bao giờ được quên khi khai báo mảng trong C. Vì chỉ số bắt đầu từ không nên mảng có n phần tử chỉ hợp lệ tới n trừ một. Tương tự, một bộ đệm giữ chuỗi dài tối đa L ký tự luôn cần ít nhất L cộng một bai.",
                clear=True,
            )
        ],
        "formula_checks": ["alg.cpr_str_bytes(5) == 6"],
        "example_title": "Chạy thật trên GCC: đo strlen vs sizeof và cắt gọn bằng snprintf",
        "example_items": [
            {
                "type": "r3",
                "say": "Trước khi chạy mã C, ta giải mã đủ bốn ký hiệu chuẩn trên bảng. Thư viện chuỗi cung cấp hàm đếm độ dài, và từ khoá chỉ đọc ngăn hàm sửa mảng đầu vào. Hàm ghi giới hạn tự cắt chuỗi vừa kích thước, còn ép kiểu bỏ qua biến thừa giúp qua cờ biên dịch nghiêm ngặt.",
                "rows": [
                    ["<code>#include &lt;string.h&gt;</code>", "Chứa hàm đếm độ dài chuỗi <code>strlen</code>"],
                    ["<code>const char s[]</code>", "Tham số mảng chuỗi chỉ đọc: hàm xem ký tự nhưng bị cấm sửa đổi"],
                    ["<code>snprintf(dst, sizeof(dst), \"%s\", src)</code>", "Tự cắt nếu chuỗi nguồn dài quá <code>sizeof(dst) - 1</code>, không bao giờ tràn"],
                    ["<code>(void)need;</code>", "Báo trình biên dịch bỏ qua giá trị trả về để khỏi lỗi biến không dùng (<code>-Werror</code>)"],
                ],
                "focus": [0, 1, 2, 3],
            },
            {
                "type": "code",
                "pid": "p1",
                "title": "So sánh trực tiếp strlen và sizeof trên chuỗi 5 ký tự",
                "say": "Đoạn mã khai báo một chuỗi chuẩn năm ký tự rồi kiểm tra đồng thời độ dài ký tự và kích thước thật trong bộ nhớ. Tiếp theo ta thử ép chuỗi năm ký tự đó vào bộ đệm chỉ rộng bốn bai qua hàm ghi có giới hạn dung lượng.",
                "out_say": "Chạy thật bằng trình biên dịch xác nhận độ dài chuỗi bằng năm trong khi tổng bộ nhớ là sáu bai vì chứa thêm bai không ở cuối. Khi đưa vào bộ đệm bốn bai, hàm an toàn tự động cắt gọn còn ba chữ cái đầu kèm bai kết thúc đúng chuẩn.",
            },
        ],
        "progs": {
            "p1": {
                "code": (
                    "#include <stdio.h>\n"
                    "#include <string.h>\n"
                    "static int copy_cut(char dst[], size_t cap, const char s[]) {\n"
                    '    return snprintf(dst, cap, "%s", s);\n'
                    "}\n"
                    "int main(void) {\n"
                    '    char s[6] = "HELLO";\n'
                    "    char small[4];\n"
                    "    int need = copy_cut(small, sizeof(small), s); (void)need;\n"
                    '    printf("len=%zu bytes=%zu last=%d\\n", strlen(s), sizeof(s), (int)s[5]);\n'
                    '    printf("safe=%s\\n", small);\n'
                    "    return 0;\n"
                    "}"
                ),
                "expect": "len=5 bytes=6 last=0\nsafe=HEL",
            },
            "p2": {
                "code": (
                    "#include <stdio.h>\n"
                    "int main(void) {\n"
                    "    int arr[4] = {10, 20, 30, 40};\n"
                    "    int sum = 0;\n"
                    "    for (int i = 0; i < 4; i++) { sum += arr[i]; }\n"
                    '    printf("sum=%d first=%d last=%d\\n", sum, arr[0], arr[3]);\n'
                    "    return 0;\n"
                    "}"
                ),
                "expect": "sum=100 first=10 last=40",
            },
        },
        "example_checks": ["alg.cpr_str_bytes(5) == 6"],
        "check_title": "Kiểm chứng chỉ số mảng hợp lệ 0..n-1",
        "check_items": [
            {
                "type": "code",
                "pid": "p2",
                "title": "Duyệt đúng biên i < 4 trên mảng 4 phần tử",
                "say": "Ở phần kiểm chứng, ta dùng phép duyệt tổng mảng bốn số nguyên theo chỉ số chặt chẽ. Vì vòng lặp dừng ngay khi biến chạy chạm bốn nên phần tử cuối truy cập đúng chỉ số ba mà không trượt ra ngoài biên mảng.",
                "out_say": "Đầu ra thật in tổng bằng đúng một trăm với phần tử đầu là mười và phần tử cuối là bốn mươi, vì bốn số hạng cộng dồn vừa khớp biên trên.",
            }
        ],
        "check_checks": ["10 + 20 + 30 + 40 == 100"],
        "quymo_title": "Bảng quy mô: chi phí bộ đệm chuỗi qua 3 cỡ danh sách tên",
        "quymo_steps": [
            ak.st(
                ak.table(
                    ["số lượng chuỗi (mỗi chuỗi tối đa 31 ký tự)", "kích thước mỗi ô đệm", "tổng RAM chiếm"],
                    [
                        [ak.nowrap("10 (×1)"), "32 byte (31 + '\\0')", "320 byte"],
                        [ak.nowrap("1 000 (×100)"), "32 byte (31 + '\\0')", "32 000 byte (~31 KB)"],
                        [ak.nowrap("100 000 (×10 000)"), "32 byte (31 + '\\0')", "3 200 000 byte (~3,1 MB)"],
                    ],
                ),
                "Với quy ước độ dài tối đa ba mươi mốt ký tự, mỗi ô nhớ cần tròn ba mươi hai bai gồm cả bai không kết thúc. "
                "Với danh sách nhỏ mười chuỗi, tổng dung lượng chỉ ba trăm hai mươi bai. Tăng lên một nghìn chuỗi thì bộ nhớ chiếm ba mươi hai nghìn bai, và đạt một trăm nghìn chuỗi sẽ tốn hơn ba phẩy hai triệu bai trong bộ nhớ.",
                focus=[0, "1.2", "1.3", "1.4"],
                clear=True,
            )
        ],
        "quymo_checks": ["1000 * alg.cpr_str_bytes(31) == 32_000", "100_000 * 32 == 3_200_000"],
        "pitfall_steps": [
            ak.st(
                ak.box(
                    "<b>Lỗi 1: Dùng vòng lặp <code>i &lt;= n</code> trên mảng <code>n</code> phần tử.</b> Lệch 1 ô (off-by-one) đọc hoặc ghi quá biên mảng là hành vi không xác định.<br>"
                    "<b>Lỗi 2: Dùng <code>strcpy(dst, src)</code> không kiểm kích thước nguồn.</b> Dữ liệu từ người dùng dài quá ô chứa sẽ phá huỷ ngăn xếp.<br>"
                    "<b>Lỗi 3: Tưởng <code>strncpy</code> luôn tự thêm <code>'\\0'</code>.</b> Khi chuỗi nguồn đủ dài bằng <code>n</code>, <code>strncpy</code> để sót chuỗi không có byte 0 cuối; nên dùng <code>snprintf</code>.",
                    "warn",
                ),
                "Có ba lỗi rất hay gặp về mảng và chuỗi trong thực tế lập trình C. Lỗi đầu là lệch một bước do viết dấu nhỏ hơn hoặc bằng làm vòng lặp đọc vượt biên mảng. Lỗi thứ hai là dùng hàm chép không kiểm độ dài gây tràn ngăn xếp. Lỗi thứ ba là nhầm hàm chép độ dài n tự động thêm bai không khi chuỗi nguồn dài vừa khít.",
                clear=True,
            )
        ],
        "quiz_steps": [
            ak.st(
                "<ol><li>Để chứa an toàn chuỗi tối đa 15 ký tự, mảng <code>char</code> cần khai báo tối thiểu bao nhiêu byte?</li>"
                "<li>Một mảng <code>int a[12]</code> thì chỉ số phần tử hợp lệ cuối cùng là số mấy?</li></ol>",
                "Đến lượt bạn tự kiểm tra. "
                "Câu một, để chứa an toàn chuỗi dài tối đa mười lăm ký tự, mảng cần tối thiểu bao nhiêu bai? "
                "Câu hai, mảng mười hai phần tử thì chỉ số hợp lệ cuối cùng là bao nhiêu? Dừng vi-đê-ô và trả lời.",
                pause=20,
            ),
            ak.st(
                "<p>① 15 + 1 = <b>16</b> byte (15 ký tự và 1 byte <code>'\\0'</code>).</p>",
                "Đáp án câu một: mười lăm cộng thêm một bai kết thúc bằng mười sáu bai.",
                clear=True,
            ),
            ak.st(
                "<p>② Chỉ số hợp lệ cuối cùng là 12 − 1 = <b>11</b> (dải <code>0..11</code>).</p>",
                "Đáp án câu hai: chỉ số chạy từ không tới mười một.",
                clear=True,
            ),
        ],
        "quiz_checks": ["alg.cpr_str_bytes(15) == 16", "12 - 1 == 11"],
        "recap_steps": [
            ak.st(
                "<div class='chain'><span class='n'>Mảng n phần tử: 0..n−1</span><span class='a'>→</span>"
                "<span class='n'>Chuỗi L chữ: cần L + 1 byte</span><span class='a'>→</span>"
                "<span class='n'>Ghi an toàn dùng snprintf</span></div>",
                "Ghi nhớ chuỗi quy tắc cốt lõi khi thao tác với mảng và chuỗi C. Mảng n phần tử luôn kết thúc ở chỉ số n trừ một. Chuỗi dài L ký tự cần tối thiểu L cộng một bai, và luôn dùng hàm ghi có kiểm biên dung lượng.",
                clear=True,
            )
        ],
        "lab_de": (
            "# Lab CPR L03 — Đếm độ dài chuỗi và sao chép chống tràn\n\n"
            "Viết chương trình C chuẩn C11 nhận chuỗi `\"BANKING_2026\"`, đặt vào `buf[8]` bằng `snprintf` và in đúng 2 dòng:\n"
            "1. `src_len=12 buf_size=8`\n"
            "2. `cut=BANKING last_byte=0`\n\n"
            "Chấm tự động:\n```bash\nbash labs/cham.sh CPR L03 duong_dan/bai_cua_ban.c\n```"
        ),
        "lab_sol": (
            "#include <stdio.h>\n"
            "#include <string.h>\n"
            "static int cut_copy(char *dst, size_t cap, const char *s) {\n"
            '    return snprintf(dst, cap, "%s", s);\n'
            "}\n"
            "int main(void) {\n"
            '    const char src[] = "BANKING_2026";\n'
            "    char buf[8];\n"
            "    int need = cut_copy(buf, sizeof(buf), src); (void)need;\n"
            '    printf("src_len=%zu buf_size=%zu\\n", strlen(src), sizeof(buf));\n'
            '    printf("cut=%s last_byte=%d\\n", buf, (int)buf[7]);\n'
            "    return 0;\n"
            "}\n"
        ),
    }

    # ────────────────── L04: Con trỏ và địa chỉ bộ nhớ: & và * ──────────────────
    l04 = {
        "id": "L04",
        "slug": "con_tro_dia_chi",
        "title": "Con trỏ và địa chỉ bộ nhớ: toán tử & và *",
        "next_title": "Con trỏ, mảng và số học bước nhảy con trỏ",
        "assumes": ["cpr_ub"],
        "objectives": [
            "Phân biệt địa chỉ ô nhớ (&x), biến con trỏ (p) và giá trị tại địa chỉ (*p)",
            "Viết hàm hoán đổi hai biến thông qua con trỏ truyền địa chỉ",
            "Kiểm tra NULL trước khi giải tham chiếu để tránh sập chương trình",
        ],
        "covers": [(1, "sym"), (2, "example"), (3, "check")],
        "hook_title": "Làm sao một hàm sửa trực tiếp biến gốc ở bên ngoài?",
        "hook_html": (
            "<p>Ở bài 2, hàm hoán đổi thất bại vì chỉ sửa bản sao. Thay vì gửi giá trị <b>10</b> và <b>25</b>, ta gửi <b>địa chỉ ô nhớ</b> nơi hai biến đang nằm.</p>"
            "<p>Biến đặc biệt chứa con số địa chỉ ấy là chìa khoá để C làm việc trực tiếp với bộ nhớ bên ngoài hàm.</p>"
        ),
        "hook_say": (
            "Chào bạn, ở bài 2 hàm hoán đổi thất bại vì chỉ cầm bản sao giá trị. "
            "Hôm nay ta giải quyết dứt điểm bài toán đó bằng cách gửi thẳng con số địa chỉ ô nhớ của biến gốc vào hàm. "
            "Nhờ nắm đúng địa chỉ nhà, hàm mới có quyền mở cửa bước vào sửa giá trị thực sự."
        ),
        "hook_checks": ["10 != 25"],
        "prereq_steps": [
            ak.st(
                ak.table(
                    ["nền tảng đã có", "liên kết với địa chỉ ô nhớ"],
                    [
                        ["Mọi biến nằm tại ô nhớ RAM với địa chỉ 8 byte trên hệ 64-bit (L00)", "Địa chỉ này là số nguyên xác định vị trí bắt đầu của biến"],
                        ["Hàm chỉ nhận bản sao đối số (L02)", "Bản sao của địa chỉ vẫn trỏ tới đúng ô nhớ gốc"],
                    ],
                ),
                "Nhớ lại bài 0 và bài 2 trước khi viết ký hiệu mới. Trên hệ thống sáu mươi bốn bít, mọi biến đều có địa chỉ tám bai cố định trên bộ nhớ RAM. Dù hàm chỉ nhận bản sao của địa chỉ đó thì con số địa chỉ vẫn trỏ trúng ngay ô nhớ gốc.",
                clear=True,
            )
        ],
        "sym_steps": [
            ak.st(
                ak.table(
                    ["ký hiệu mới", "tên gọi và tác dụng"],
                    [
                        ["<code>&amp;x</code>", "Lấy địa chỉ ô nhớ của biến <code>x</code>"],
                        ["<code>int *p</code>", "Khai báo biến con trỏ <code>p</code> chứa địa chỉ của một biến <code>int</code>"],
                        ["<code>*p</code>", "Giải tham chiếu: đọc hoặc ghi trực tiếp vào ô nhớ mà <code>p</code> đang trỏ tới"],
                        ["<code>NULL</code>", "Địa chỉ rỗng đặc biệt báo hiệu con trỏ hiện không trỏ tới biến nào"],
                    ],
                ),
                "Bảng này giải mã bốn ký hiệu trọng tâm của con trỏ trong C. "
                "Dấu và đứng trước biến lấy địa chỉ ô nhớ của biến đó. "
                "Dấu sao khi khai báo biến tạo thành con trỏ giữ địa chỉ, còn dấu sao đứng trong biểu thức nghĩa là đọc hoặc ghi tại ô nhớ đích. "
                "Cuối cùng là giá trị rỗng chuẩn báo hiệu con trỏ chưa trỏ tới đâu.",
                introduces=["cpr_con_tro"],
                focus=[0, "1.2", "1.3", "1.4", "1.5"],
                clear=True,
            )
        ],
        "intuition_title": "Gửi địa chỉ nhà thay vì gửi bản photo tờ giấy",
        "intuition_steps": [
            ak.st(
                ak.svg_wrap(
                    960, 210,
                    ak.svg_rect(40, 50, 230, 105, "Biến gốc x", "Giá trị: 10 | tại 0x7000", ak.C_BLUE)
                    + ak.svg_arrow(270, 102, 370, 102, "&x = 0x7000")
                    + ak.svg_rect(370, 50, 240, 105, "Con trỏ p", "Giữ địa chỉ 0x7000", ak.C_AMBER)
                    + ak.svg_arrow(610, 102, 700, 102, "*p = 99")
                    + ak.svg_rect(700, 50, 220, 105, "Ô nhớ 0x7000", "x đổi ngay thành 99", ak.C_GREEN),
                ),
                "Nhìn sơ đồ: biến gốc x nằm tại ô nhớ đánh địa chỉ hệ thập lục phân bảy nghìn. "
                "Toán tử lấy địa chỉ đưa đúng con số vị trí ấy cất vào biến con trỏ p. "
                "Khi hàm thực hiện phép ghi qua dấu sao giải tham chiếu, giá trị tại đúng ô nhớ địa chỉ bảy nghìn đổi từ mười thành chín mươi chín. Hai khái niệm vị trí ô nhớ và giá trị bên trong ô nhớ luôn đi đôi nhưng hoàn toàn khác vai trò.",
                clear=True,
            )
        ],
        "formula_title": "Luật đọc/ghi an toàn qua con trỏ",
        "formula_steps": [
            ak.st(
                ak.box(
                    "<p>Ba quy tắc bất di bất dịch:</p>"
                    "<ol><li>Khởi tạo ngay lúc tạo: <code>int *p = &amp;x;</code> hoặc <code>int *p = NULL;</code></li>"
                    "<li>Chỉ giải tham chiếu sau khi kiểm: <code>if (p != NULL) { *p = ...; }</code></li>"
                    "<li>Không trộn kiểu trỏ: địa chỉ của <code>int</code> đi với <code>int *</code>, của <code>double</code> đi với <code>double *</code>.</li></ol>",
                    "key",
                ),
                "Ba quy tắc bảo vệ sau giúp tránh gần hết lỗi con trỏ kinh điển. Bạn hãy luôn gán giá trị ban đầu ngay khi khai báo biến trỏ. Sau đó luôn kiểm tra khác rỗng trước khi ghi và giữ đúng kiểu dữ liệu đích.",
                clear=True,
            )
        ],
        "formula_checks": ["10 + 15 == 25"],
        "example_title": "Chạy thật trên GCC: hàm hoán đổi thật qua địa chỉ",
        "example_items": [
            {
                "type": "r3",
                "say": "Ta giải mã đủ bốn ký hiệu trước khi đọc mã nguồn. Tham số nhận hai địa chỉ kiểu số nguyên, câu lệnh phép hoặc loại trừ ngay khi một con trỏ rỗng. Cách viết rút gọn kiểm tra trực tiếp con trỏ khác rỗng ngay trước dấu sao giải tham chiếu.",
                "rows": [
                    ["<code>static void swap_ptr(int *pa, int *pb)</code>", "Hàm nhận hai địa chỉ kiểu <code>int *</code> để sửa trực tiếp biến gốc"],
                    ["<code>swap_ptr(&amp;a, &amp;b);</code>", "Truyền địa chỉ của hai biến gốc từ <code>main</code> vào hàm"],
                    ["<code>||</code> (HOẶC logic)", "Đúng nếu ít nhất một vế đúng: <code>pa == NULL || pb == NULL</code>"],
                    ["<code>if (q)</code> / <code>0x7000</code>", "<code>if (q)</code> viết gọn của <code>q != NULL</code>; <code>0x...</code> là số địa chỉ hệ thập lục phân"],
                ],
                "focus": [0, 1, 2, 3],
            },
            {
                "type": "code",
                "pid": "p1",
                "title": "Hoán đổi thật qua con trỏ và kiểm tra NULL an toàn",
                "say": "Hàm hoán đổi nhận vào hai con trỏ, chủ động kiểm tra cả hai đều khác rỗng trước khi giải tham chiếu. Nhờ trỏ trúng hai biến gốc, biến tạm bên trong hàm đổi được trực tiếp giá trị nằm ngoài hàm chính.",
                "out_say": "Đầu ra chạy thật cho thấy biến a và biến b ở hàm chính đã thực sự hoán đổi thành hai mươi lăm và mười. Phép hoán đổi này thành công hoàn toàn khác hẳn kết quả thất bại ở bài trước.",
            },
        ],
        "progs": {
            "p1": {
                "code": (
                    "#include <stdio.h>\n"
                    "static void swap_ptr(int *pa, int *pb) {\n"
                    "    if (pa == NULL || pb == NULL) return;\n"
                    "    int tmp = *pa; *pa = *pb; *pb = tmp;\n"
                    "}\n"
                    "int main(void) {\n"
                    "    int a = 10, b = 25;\n"
                    "    swap_ptr(&a, &b);\n"
                    '    printf("after: a=%d b=%d\\n", a, b);\n'
                    "    return 0;\n"
                    "}"
                ),
                "expect": "after: a=25 b=10",
            },
            "p2": {
                "code": (
                    "#include <stdio.h>\n"
                    "static void divmod_i(int x, int d, int *q, int *r) {\n"
                    "    if (q) *q = x / d;\n"
                    "    if (r) *r = x % d;\n"
                    "}\n"
                    "int main(void) {\n"
                    "    int thuong = 0, du = 0;\n"
                    "    divmod_i(29, 6, &thuong, &du);\n"
                    '    printf("q=%d r=%d\\n", thuong, du);\n'
                    "    return 0;\n"
                    "}"
                ),
                "expect": "q=4 r=5",
            },
        },
        "example_checks": ["(lambda a, b: (b, a))(10, 25) == (25, 10)"],
        "check_title": "Đường khác: dùng con trỏ trả về nhiều kết quả cùng lúc",
        "check_items": [
            {
                "type": "code",
                "pid": "p2",
                "title": "Hàm trả cả phần nguyên và phần dư thông qua hai con trỏ đầu ra",
                "say": "Ở đường kiểm chứng thứ hai, ta giải bài toán trả về cả phần thương lẫn phần dư chỉ trong một lần gọi hàm. Vì ngôn ngữ C chỉ cho phép trả về một giá trị trực tiếp nên hàm kiểm tra khác rỗng rồi ghi song song hai kết quả qua hai con trỏ đầu ra.",
                "out_say": "Đầu ra thật xác nhận thương bằng bốn và số dư bằng năm, nghĩa là hai mươi chín bằng sáu nhân bốn cộng năm khớp tuyệt đối mà vẫn an toàn trước con trỏ rỗng.",
            }
        ],
        "check_checks": ["29 // 6 == 4", "29 % 6 == 5"],
        "quymo_title": "Bảng quy mô: chi phí truyền struct lớn theo giá trị vs qua con trỏ",
        "quymo_steps": [
            ak.st(
                ak.table(
                    ["số lượt gọi hàm truyền cấu trúc 4 KB", "chép nguyên khối (tham trị)", "truyền địa chỉ con trỏ (8 byte)"],
                    [
                        [ak.nowrap("100 lượt (×1)"), "400 KB sao chép", "800 byte địa chỉ"],
                        [ak.nowrap("10 000 lượt (×100)"), "40 MB sao chép", "80 KB địa chỉ"],
                        [ak.nowrap("1 000 000 lượt (×10 000)"), "4 GB sao chép", "8 MB địa chỉ (nhanh hơn ~500 lần)"],
                    ],
                ),
                "Ngoài việc sửa giá trị gốc, truyền địa chỉ còn tránh sao chép khối dữ liệu lớn. "
                "Ở mức một trăm lượt truyền cấu trúc bốn ki-lô-bai, truyền địa chỉ chỉ tốn tám trăm bai so với bốn trăm ki-lô-bai. Khi tăng lên một triệu lượt gọi hàm, truyền bản sao tốn bốn gi-ga-bai sao chép, còn truyền địa chỉ chỉ tốn tám mê-ga-bai, nhanh hơn gấp năm trăm lần.",
                focus=[0, "1.2", "1.3", "1.4"],
                clear=True,
            )
        ],
        "quymo_checks": ["1_000_000 * 8 == 8_000_000", "4096 // 8 == 512"],
        "pitfall_steps": [
            ak.st(
                ak.box(
                    "<b>Lỗi 1: Khai báo <code>int *p;</code> không gán giá trị rồi ghi <code>*p = 5;</code>.</b> Con trỏ mang địa chỉ rác làm sập chương trình ngay.<br>"
                    "<b>Lỗi 2: Giải tham chiếu con trỏ <code>NULL</code> khi chưa kiểm tra.</b> Luôn kiểm <code>if (p != NULL)</code> ở ranh giới hàm.<br>"
                    "<b>Lỗi 3: Trả về địa chỉ biến cục bộ <code>int x = 5; return &amp;x;</code>.</b> Khung ngăn xếp của hàm vừa bị huỷ, địa chỉ trả về thành con trỏ treo.",
                    "warn",
                ),
                "Có ba lỗi nghiêm trọng rất hay gặp khi mới làm việc với con trỏ. Lỗi thứ nhất là khai báo con trỏ chưa khởi tạo chứa địa chỉ rác rồi ghi thẳng vào đó. Lỗi thứ hai là quên kiểm tra khác rỗng trước khi giải tham chiếu. Lỗi thứ ba là trả về địa chỉ của một biến cục bộ vừa hết hạn.",
                clear=True,
            )
        ],
        "quiz_steps": [
            ak.st(
                "<ol><li>Cho <code>int a = 12; int *p = &amp;a; *p = *p + 8;</code> — sau ba lệnh, <code>a</code> bằng bao nhiêu?</li>"
                "<li>Viết lệnh kiểm tra an toàn bắt buộc trước khi ghi vào <code>*out</code> trong hàm?</li></ol>",
                "Đến lượt bạn tự kiểm tra. "
                "Câu một, biến a giữ mười hai, con trỏ p trỏ tới a, rồi tăng giá trị tại ô nhớ đích thêm tám đơn vị thì a bằng bao nhiêu? "
                "Câu hai, viết điều kiện kiểm tra bắt buộc trước khi ghi vào giá trị tại con trỏ đầu ra. Dừng vi-đê-ô và trả lời.",
                pause=20,
            ),
            ak.st(
                "<p>① <code>*p</code> sửa trực tiếp ô nhớ của <code>a</code> nên $a = 12 + 8 = \\hl{20}$.</p>",
                "Đáp án câu một: ghi qua con trỏ làm biến a tăng từ mười hai lên hai mươi.",
                clear=True,
            ),
            ak.st(
                "<p>② Luôn kiểm <code>if (out != NULL)</code> trước khi gán <code>*out = ...</code>.</p>",
                "Đáp án câu hai: luôn kiểm tra con trỏ khác rỗng trước khi giải tham chiếu.",
                clear=True,
            ),
        ],
        "quiz_checks": ["12 + 8 == 20"],
        "recap_steps": [
            ak.st(
                "<div class='chain'><span class='n'>&amp;x lấy địa chỉ</span><span class='a'>→</span>"
                "<span class='n'>p giữ địa chỉ</span><span class='a'>→</span>"
                "<span class='n'>kiểm p != NULL rồi mới dùng *p</span></div>",
                "Tổng kết chuỗi tư duy hôm nay để dùng suốt khoá học. Dùng toán tử lấy địa chỉ đưa vào con trỏ lưu vị trí, luôn kiểm tra khác rỗng trước khi ghi, và không bao giờ trả về địa chỉ biến cục bộ.",
                clear=True,
            )
        ],
        "lab_de": (
            "# Lab CPR L04 — Sửa trực tiếp hai biến qua con trỏ và hàm divmod\n\n"
            "Viết chương trình C chuẩn C11 hoán đổi `x=42, y=99` qua con trỏ và gọi `divmod(47, 5, &q, &r)`, in đúng 2 dòng:\n"
            "1. `swap: x=99 y=42`\n"
            "2. `divmod: q=9 r=2`\n\n"
            "Chấm tự động:\n```bash\nbash labs/cham.sh CPR L04 duong_dan/bai_cua_ban.c\n```"
        ),
        "lab_sol": (
            "#include <stdio.h>\n"
            "static void swap_ptr(int *a, int *b) {\n"
            "    if (!a || !b) return;\n"
            "    int t = *a; *a = *b; *b = t;\n"
            "}\n"
            "static void divmod_i(int x, int d, int *q, int *r) {\n"
            "    if (q) *q = x / d;\n"
            "    if (r) *r = x % d;\n"
            "}\n"
            "int main(void) {\n"
            "    int x = 42, y = 99, q = 0, r = 0;\n"
            "    swap_ptr(&x, &y);\n"
            "    divmod_i(47, 5, &q, &r);\n"
            '    printf("swap: x=%d y=%d\\n", x, y);\n'
            '    printf("divmod: q=%d r=%d\\n", q, r);\n'
            "    return 0;\n"
            "}\n"
        ),
    }

    return [l00, l01, l02, l03, l04]
