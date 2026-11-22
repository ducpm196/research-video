"""Đặc tả dữ liệu LNX L00–L04."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "audit" / "review"))
import af2_kit as ak  # noqa: E402


def lessons():
    # ────────────────── L00: Hệ thống tệp Linux, /proc và liên kết ──────────────────
    l00 = {
        "id": "L00",
        "slug": "he_thong_tep_inode_link",
        "title": "Hệ thống tệp Linux, /proc và liên kết cứng vs liên kết mềm",
        "next_title": "Người dùng, nhóm và phân quyền bát phân theo chữ số",
        "assumes": [],
        "objectives": [
            "Phân biệt vai trò các thư mục gốc /etc, /var, /tmp, /proc trên Linux",
            "Phân biệt liên kết cứng (chung số nút chỉ mục) với liên kết mềm (lưu đường dẫn)",
            "Giải thích vì sao xoá một tên tệp liên kết cứng không làm mất dữ liệu khi còn liên kết khác",
        ],
        "covers": [(1, "sym"), (2, "example"), (3, "check")],
        "hook_title": "Xoá tệp nguồn: vì sao một liên kết sống, một liên kết hỏng?",
        "hook_html": (
            "<p>Trên Linux, một người tạo hai tệp cùng trỏ về dữ liệu <code>orig.txt</code> rồi xoá <code>orig.txt</code>.</p>"
            "<p>Kết quả: <b>liên kết cứng</b> đọc trọn vẹn nội dung vì trỏ thẳng tới nút dữ liệu gốc; <b>liên kết mềm</b> hỏng ngay lập tức.</p>"
        ),
        "hook_say": (
            "Chào bạn đến với khoá Li-núc và công-tai-nơ thực chiến. "
            "Nhiều bạn rất ngạc nhiên khi thấy hai tệp cùng trỏ tới một nội dung nhưng lúc xoá tệp đầu thì tệp này còn nguyên còn tệp kia lại hỏng mất. "
            "Nguyên nhân nằm ở cách hệ điều hành tách biệt tên tệp trong thư mục với nút mô tả dữ liệu nằm trên ổ đĩa. "
            "Hôm nay ta học cấu trúc thư mục gốc, hệ thống tệp ảo tiến trình và hai loại liên kết này."
        ),
        "hook_checks": ["2 - 1 == 1"],
        "prereq_steps": [
            ak.st_auto(
                ak.table(
                    ["nền tảng dòng lệnh", "ứng dụng trên Linux"],
                    [
                        ["Chạy lệnh ls, cat, rm trên dòng lệnh", "Đọc chỉ số nút mô tả, bộ đếm liên kết và mã thoát lệnh"],
                        ["Đường dẫn tuyệt đối và tương đối", "Phân biệt thư mục cấu hình gốc với thư mục làm việc"],
                    ],
                ),
                "Trước khi khám phá cây thư mục hệ thống, ta nhắc lại hai kỹ năng nền tảng từ khoá thực hành dòng lệnh cơ bản. Thứ nhất là thói quen chạy lệnh kiểm tra tệp và đối chiếu mã thoát sau mỗi thao tác. Thứ hai là phân biệt rạch ròi đường dẫn tuyệt đối bắt đầu từ gốc với đường dẫn tương đối.",
                clear=True,
            )
        ],
        "sym_steps": [
            ak.st_auto(
                ak.table(
                    ["khái niệm / lệnh mới", "vai trò chuẩn trên hệ thống"],
                    [
                        ["inode (nút chỉ mục)", "Cấu trúc đánh số duy nhất lưu siêu dữ liệu và vị trí khối của tệp"],
                        ["<code>ln A B</code>", "Tạo liên kết cứng B dùng chung số nút chỉ mục với A (nlinks tăng +1)"],
                        ["<code>ln -s A C</code>", "Tạo liên kết mềm C chỉ lưu chuỗi đường dẫn trỏ sang tên tệp A"],
                        ["<code>/etc /var /tmp /proc</code>", "Thư mục cấu hình tĩnh, nhật ký biến đổi, tệp tạm và thông số nhân đang chạy"],
                    ],
                ),
                "Bảng này giải mã bốn thành phần trọng tâm giúp bạn đọc hiểu toàn bộ hệ thống tệp Li-núc. Mỗi tệp thực chất được đại diện bởi một nút chỉ mục mang mã số duy nhất trên phân vùng đĩa gọi là i-nốt. Liên kết cứng tạo thêm tên mới bám chung vào i-nốt đó nên bộ đếm tăng một, còn liên kết mềm chỉ giữ tên đường dẫn. Bên dưới là bốn thư mục gốc quen thuộc gồm cấu hình tĩnh, nhật ký thay đổi, tệp tạm và hệ thống tệp ảo của nhân.",
                introduces=["lnx_inode"],
                clear=True,
            )
        ],
        "intuition_title": "Sơ đồ hai cách trỏ tới dữ liệu: cùng i-nốt vs qua tên tệp",
        "intuition_steps": [
            ak.st_auto(
                ak.svg_wrap(
                    960, 215,
                    ak.svg_rect(40, 22, 240, 68, "hard.txt (Tên A)", "Trỏ thẳng i-nốt #1001", ak.C_GREEN)
                    + ak.svg_arrow(280, 56, 390, 56, "nlinks=2")
                    + ak.svg_rect(390, 22, 260, 68, "i-nốt #1001 (Dữ liệu thật)", "Nội dung + quyền + kích thước", ak.C_AMBER)
                    + ak.svg_rect(40, 124, 240, 68, "orig.txt (Tên B)", "Cùng trỏ i-nốt #1001", ak.C_GREEN)
                    + ak.svg_arrow(630, 158, 280, 158, "trỏ tên → đứt khi xoá orig")
                    + ak.svg_rect(630, 124, 290, 68, "sym.txt (Liên kết mềm)", "Lưu chuỗi tên 'orig.txt' (#1002)", ak.C_RED),
                ),
                "Nhìn sơ đồ so sánh hai cơ chế liên kết trên hệ thống tệp. Cả hai tên tệp cứng nằm bên trái đều trỏ trực tiếp vào chung khối mô tả i-nốt một nghìn không trăm linh một nên bộ đếm liên kết bằng hai. Trong khi đó liên kết mềm ở bên phải là một tệp nhỏ mang mã i-nốt riêng chỉ ghi mỗi dòng chữ tên tệp gốc. Vì thế khi xoá tên tệp gốc, dữ liệu vẫn còn nguyên cho liên kết cứng, còn liên kết mềm trở thành đường dẫn đứt đoạn.",
                clear=True,
            )
        ],
        "formula_title": "Quy tắc thu hồi dữ liệu của nhân Linux",
        "formula_steps": [
            ak.st_auto(
                ak.box(
                    "<p><b>Quy tắc giải phóng ổ đĩa chuẩn POSIX:</b></p>"
                    "<p>Dữ liệu trên ổ đĩa chỉ bị thu hồi khi <b>cả hai điều kiện</b> cùng đạt 0: bộ đếm tên tệp <code>link_count == 0</code> <b>và</b> không còn tiến trình nào mở tệp.</p>"
                    "<p>Ví dụ: ban đầu <code>link_count = 2</code>; sau khi <code>rm orig.txt</code>, <code>link_count = 1 &gt; 0</code> nên dữ liệu giữ nguyên 100%.</p>",
                    "key",
                ),
                "Quy tắc thu hồi dữ liệu rất nhất quán trên mọi máy chủ Li-núc. Nhân hệ điều hành chỉ đánh dấu thu hồi các khối dữ liệu khi bộ đếm liên kết giảm về không và không còn tiến trình nào đang mở tệp đó. Vì thế với hai tên tệp cứng ban đầu, khi xoá một tên thì bộ đếm vẫn bằng một lớn hơn không nên dữ liệu còn nguyên vẹn.",
                clear=True,
            )
        ],
        "formula_checks": ["(2 - 1) >= 1"],
        "example_title": "Chạy thật trên Alpine Linux: kiểm tra liên kết và /proc",
        "example_items": [
            {
                "type": "r3",
                "say": "Trước khi xem kết quả chạy thật trên nhân Li-núc thật, ta giải mã bốn quy ước quan trọng. Hai lệnh đầu tạo hai kiểu liên kết, lệnh sau đọc mã i-nốt, và cờ môi trường giữ nguyên đường dẫn trên máy.",
                "rows": [
                    ["<code>stat -c '%i %h'</code>", "In ra đúng hai con số: mã số i-nốt và số liên kết trỏ tới nó (chuẩn POSIX = bộ quy ước chung Unix/Linux)"],
                    ["<code>ln orig.txt hard.txt</code>", "Tạo liên kết cứng dùng chung i-nốt với tệp gốc"],
                    ["<code>ln -s orig.txt sym.txt</code>", "Tạo liên kết mềm trỏ gián tiếp theo tên đường dẫn"],
                    ["<code>MSYS_NO_PATHCONV=1</code>", "Biến môi trường Git Bash Windows cấm tự đổi đường dẫn Linux <code>/tmp</code>"],
                ],
                "focus": [0, 1, 2, 3],
            },
            {
                "type": "code",
                "pid": "p1",
                "title": "Kiểm chứng thật trong container Alpine Linux về i-nốt và bộ đếm liên kết",
                "say": "Ta chạy trực tiếp một công-tai-nơ An-pin Li-núc thật để chứng minh hoạt động của bộ đếm liên kết và thư mục gốc. Kịch bản tạo một tệp văn bản, gắn thêm một liên kết cứng và một liên kết mềm, rồi xoá tệp nguồn và đo lại hai liên kết đó.",
                "out_say": "Đầu ra thật xác nhận liên kết cứng và tệp gốc giữ cùng mã số i-nốt với bộ đếm bằng hai. Sau khi xoá tệp nguồn, liên kết cứng vẫn đọc trọn vẹn chuỗi dữ liệu còn liên kết mềm trả mã thoát một báo lỗi không tìm thấy tệp.",
            },
        ],
        "progs": {
            "p1": {
                "code": (
                    "MSYS_NO_PATHCONV=1 docker run --rm postgres:17-alpine sh -c '\n"
                    "  cd /tmp && printf \"hello_linux\\n\" > orig.txt\n"
                    "  ln orig.txt hard.txt && ln -s orig.txt sym.txt\n"
                    "  o=$(stat -c %i:%h orig.txt) h=$(stat -c %i:%h hard.txt)\n"
                    "  s=$(stat -c %i:%h sym.txt); echo \"before: $o | $h | $s\"\n"
                    "  rm orig.txt\n"
                    "  echo \"hard_cat=$(cat hard.txt) nlinks=$(stat -c %h hard.txt)\"\n"
                    "  cat sym.txt >/dev/null 2>&1; echo \"sym_rc=$?\"\n"
                    "  ls -d /etc /var /tmp /proc | tr \"\\n\" \" \"\n"
                    "  echo \"\"\n"
                    "'"
                ),
                "expect_sub": ["nlinks=1", "hard_cat=hello_linux", "sym_rc=1", "/etc /proc /tmp /var"],
            },
            "p2": {
                "code": (
                    "mkdir -p test_ln && cd test_ln\n"
                    "printf 'data_v1\\n' > a.txt\n"
                    "ln a.txt b.txt\n"
                    "inode_a=$(stat -c '%i' a.txt)\n"
                    "inode_b=$(stat -c '%i' b.txt)\n"
                    "rm a.txt\n"
                    "echo \"same_inode=$((inode_a == inode_b ? 1 : 0)) after_rm_read=$(cat b.txt)\""
                ),
                "expect": "same_inode=1 after_rm_read=data_v1",
            },
        },
        "example_checks": ["(2 - 1) >= 1"],
        "check_title": "Đối chứng cục bộ: tạo liên kết cứng rồi xoá bản đầu",
        "check_items": [
            {
                "type": "code",
                "pid": "p2",
                "title": "Tạo liên kết cứng và kiểm tra cùng i-nốt trước khi xoá tên đầu",
                "say": "Ở đường kiểm chứng thứ hai, ta chạy thẳng trên tệp cục bộ để đối chiếu mã số i-nốt trước và sau khi xoá tên đầu tiên. Vì cả hai tên cùng nắm giữ một nút chỉ mục nên phép so sánh hai mã số bắt buộc bằng nhau.",
                "out_say": "Đầu ra thật trả về cờ cùng i-nốt bằng một và đọc lại nguyên vẹn giá trị dữ liệu, vì việc xoá một tên tệp chỉ giảm bộ đếm liên kết từ hai xuống một.",
            }
        ],
        "check_checks": ["(2 - 1) >= 1"],
        "quymo_title": "Ảnh hưởng của liên kết và hệ thống tệp ảo qua ba quy mô dự án",
        "quymo_steps": [
            ak.st_auto(
                ak.table(
                    ["tình huống", "dữ liệu sao lưu / lưu trữ", "khác biệt khi dùng liên kết cứng"],
                    [
                        ["Dự án nhỏ (10 bản sao)", "10 × 10 MB = 100 MB trùng lặp", "Dùng 10 MB thật nhờ trỏ chung i-nốt (tiết kiệm 90%)"],
                        ["Dịch vụ vừa (100 tệp gói)", "100 × 20 MB = 2 000 MB", "Kho gói toàn cầu giữ 1 bản 20 MB (giảm 99% đĩa)"],
                        ["Lịch sử lớn (1 000 ảnh chụp)", "1 000 × 50 MB = 50 GB", "Chỉ tốn dung lượng cho phần tệp mới thay đổi"],
                    ],
                ),
                "Bảng quy mô giải thích vì sao các trình quản lý gói hiện đại và công cụ sao lưu gia tăng đều tận dụng liên kết cứng. Khi mười bản dự án cần cùng bộ thư viện mười mê-ga-bai, liên kết cứng giữ chỉ một bản duy nhất trên đĩa giúp tiết kiệm chín mươi phần trăm dung lượng. Lên tới quy mô một trăm đến một nghìn ảnh chụp, cách làm này giảm hàng chục gi-ga-bai sao chép thừa thãi.",
                clear=True,
            )
        ],
        "quymo_checks": ["100 * 20 == 2000"],
        "pitfall_steps": [
            ak.st_auto(
                ak.box(
                    "<b>Lỗi 1: Nhầm liên kết mềm giống hệt liên kết cứng.</b> Khi tệp gốc đổi tên hoặc chuyển thư mục, mọi liên kết mềm trỏ tới nó lập tức hỏng.<br>"
                    "<b>Lỗi 2: Tạo liên kết cứng xuyên khác phân vùng đĩa.</b> Mỗi phân vùng đánh số i-nốt riêng nên liên kết cứng không vượt ranh giới phân vùng.<br>"
                    "<b>Lỗi 3: Chỉnh sửa cấu hình trong thư mục ảo /proc như tệp đĩa thường.</b> Các tệp trong đó là cửa sổ trực tiếp vào bộ nhớ nhân đang chạy.",
                    "warn",
                ),
                "Hãy tránh ba lỗi rất phổ biến khi thao tác cây thư mục Li-núc. Lỗi đầu là nhầm liên kết mềm bền vững như liên kết cứng khiến cấu hình đứt gãy ngay khi dời thư mục gốc. Lỗi thứ hai là cố tạo liên kết cứng băng qua hai phân vùng ổ đĩa độc lập dù bảng mã i-nốt nằm riêng từng phân vùng. Lỗi thứ ba là tưởng thư mục hệ thống tiến trình ảo giống tệp văn bản thông thường.",
                clear=True,
            )
        ],
        "quiz_steps": [
            ak.st(
                "<ol><li>Ban đầu tệp A có <code>link_count = 2</code> do đã liên kết cứng với B. Nếu chạy <code>rm A</code>, dữ liệu có bị mất không?</li>"
                "<li>Thư mục gốc nào chứa thông tin các tiến trình đang chạy trong bộ nhớ nhân?</li></ol>",
                "Đến lượt bạn tự kiểm tra kiến thức vừa học. Câu một, một tệp có hai tên liên kết cứng với nhau rồi xoá mất một tên thì dữ liệu có còn hay không? Câu hai, thư mục gốc nào hiển thị thông tin các tiến trình đang chạy trực tiếp từ nhân hệ điều hành? Hãy bấm tạm dừng và trả lời ra giấy.",
                pause=20,
            ),
            ak.st(
                "<p>① Không mất, vì sau khi xoá A thì <code>link_count = 1 &gt; 0</code> nên B vẫn đọc đầy đủ dữ liệu.</p>",
                "Đáp án câu một: dữ liệu không hề bị mất vì bộ đếm liên kết vẫn còn bằng một nên tên thứ hai tiếp tục đọc trọn vẹn.",
                clear=True,
            ),
            ak.st(
                "<p>② Thư mục ảo <code>/proc</code> (mỗi thư mục con mang số PID của một tiến trình đang chạy).</p>",
                "Đáp án câu hai: đó là thư mục ảo hệ thống tiến trình, nơi chứa từng thư mục đánh số theo mã tiến trình đang hoạt động.",
                clear=True,
            ),
        ],
        "quiz_checks": ["(2 - 1) >= 1"],
        "recap_steps": [
            ak.st_auto(
                "<div class='chain'><span class='n'>Tên tệp → i-nốt</span><span class='a'>|</span>"
                "<span class='n'>Cứng: chung i-nốt</span><span class='a'>|</span>"
                "<span class='n'>Mềm: lưu đường dẫn</span></div>",
                "Tổng kết chuỗi tư duy cốt lõi về hệ thống tệp Li-núc. Mỗi tệp giữ dữ liệu qua mã i-nốt duy nhất và chỉ giải phóng khi bộ đếm liên kết cùng số tiến trình đang mở cùng chạm không. Nắm vững cây thư mục gốc và phân biệt hai loại liên kết giúp bạn tự tin quản trị mọi máy chủ sau này.",
                clear=True,
            )
        ],
        "lab_de": (
            "# Lab LNX L00 — Liên kết cứng vs liên kết mềm và đếm link_count\n\n"
            "Viết kịch bản Bash tạo `orig.txt` chứa `SAFE_DATA` trong môi trường Linux thật (chạy trực tiếp nếu là Linux, hoặc qua `docker run --rm postgres:17-alpine` trên Windows để giữ chuẩn liên kết mềm POSIX), tạo:\n"
            "- `hard.txt` bằng `ln orig.txt hard.txt`\n"
            "- `sym.txt` bằng `ln -s orig.txt sym.txt`\n"
            "Sau đó `rm orig.txt` và in đúng 3 dòng:\n"
            "1. `hard_content=SAFE_DATA`\n"
            "2. `hard_links=1`\n"
            "3. `sym_failed=1` (bằng 1 vì đọc `sym.txt` thất bại sau khi xoá `orig.txt`)\n\n"
            "Chấm tự động:\n```bash\nbash labs/cham.sh LNX L00 duong_dan/bai_cua_ban.sh\n```"
        ),
        "lab_sol": (
            "#!/usr/bin/env bash\n"
            "set -u\n"
            "run_posix() {\n"
            "  cd /tmp && rm -rf l00_lab && mkdir -p l00_lab && cd l00_lab\n"
            "  printf 'SAFE_DATA\\n' > orig.txt\n"
            "  ln orig.txt hard.txt && ln -s orig.txt sym.txt\n"
            "  rm orig.txt\n"
            "  printf 'hard_content=%s\\n' \"$(cat hard.txt)\"\n"
            "  printf 'hard_links=%s\\n' \"$(stat -c %h hard.txt)\"\n"
            "  if cat sym.txt >/dev/null 2>&1; then sf=0; else sf=1; fi\n"
            "  printf 'sym_failed=%s\\n' \"$sf\"\n"
            "}\n"
            "if [ \"$(uname -s)\" = \"Linux\" ]; then\n"
            "  run_posix\n"
            "else\n"
            "  MSYS_NO_PATHCONV=1 docker run --rm postgres:17-alpine sh -c '\n"
            "    cd /tmp && printf \"SAFE_DATA\\n\" > orig.txt\n"
            "    ln orig.txt hard.txt && ln -s orig.txt sym.txt && rm orig.txt\n"
            "    printf \"hard_content=%s\\n\" \"$(cat hard.txt)\"\n"
            "    printf \"hard_links=%s\\n\" \"$(stat -c %h hard.txt)\"\n"
            "    if cat sym.txt >/dev/null 2>&1; then sf=0; else sf=1; fi\n"
            "    printf \"sym_failed=%s\\n\" \"$sf\"\n"
            "  '\n"
            "fi\n"
        ),
    }

    # ────────────────── L01: Người dùng, nhóm và phân quyền bát phân chmod 755 / 640 ──────────────────
    l01 = {
        "id": "L01",
        "slug": "nguoi_dung_quyen_rwx",
        "title": "Người dùng, nhóm và phân quyền bát phân chmod 755 / 640",
        "next_title": "Tiến trình, mã thoát và điều khiển tác vụ đang chạy",
        "assumes": ["lnx_inode"],
        "objectives": [
            "Quy đổi quyền đọc (4), ghi (2), thực thi (1) giữa ký hiệu rwx và 3 chữ số bát phân",
            "Chọn quyền an toàn cho tệp bí mật (600/640) và tệp chạy/thư mục (755)",
            "Nhận biết rủi ro đặt quyền 777 trên máy chủ dùng chung",
        ],
        "covers": [(1, "formula"), (2, "example"), (3, "pitfalls")],
        "hook_title": "Vì sao phần mềm từ chối đọc khoá khi quyền là 644?",
        "hook_html": (
            "<p>Khi tệp khoá bí mật mang quyền <code>644</code> (<code>rw-r--r--</code>), mọi người dùng khác trên cùng máy chủ đều đọc được khoá riêng của bạn.</p>"
            "<p>Chương trình chuẩn bảo mật yêu cầu khoá riêng phải thu hẹp về <code>600</code> (<code>rw-------</code>) và từ chối khởi động nếu quá lỏng.</p>"
        ),
        "hook_say": (
            "Chào bạn trở lại với thực chiến Li-núc. "
            "Nếu bạn vừa sao chép một tệp khoá bảo mật lên máy chủ mới mà công cụ kết nối lập tức từ chối làm việc, nguyên nhân thường gặp nhất là quyền tệp quá rộng. "
            "Ở quyền sáu bốn bốn mặc định, mọi tài khoản khác trên cùng máy chủ đều có quyền đọc trộm nội dung bí mật đó. "
            "Hôm nay ta học cách quy đổi ba chữ số quyền hệ tám và chọn đúng mức tối thiểu an toàn cho từng loại tệp."
        ),
        "hook_checks": ["4 + 2 + 1 == 7", "4 + 2 == 6"],
        "prereq_steps": [
            ak.st_auto(
                ak.table(
                    ["nền tảng từ L00", "liên kết phân quyền"],
                    [
                        ["Mỗi tệp gắn liền với một i-nốt", "Mọi thông số chủ sở hữu, nhóm và quyền đều lưu ngay trong i-nốt đó"],
                        ["Số nhị phân và ba nhóm bít", "Mỗi nhóm người dùng dùng đúng ba bít tương ứng đọc, ghi, chạy"],
                    ],
                ),
                "Từ bài 0 bạn đã biết mọi siêu dữ liệu của tệp đều nằm trong nút chỉ mục i-nốt. Ba bít quyền đại diện cho ba hành động cơ bản là đọc, ghi và thực thi, nhân lên cho ba nhóm đối tượng tách biệt.",
                clear=True,
            )
        ],
        "sym_steps": [
            ak.st_auto(
                ak.table(
                    ["ký hiệu / lệnh", "quy đổi chuẩn ba nhóm (Chủ | Nhóm | Khác)"],
                    [
                        ["<code>r = 4, w = 2, x = 1</code>", "Trọng số bít: đọc bằng 4, ghi bằng 2, thực thi (hoặc vào thư mục) bằng 1"],
                        ["<code>chmod 755 file</code>", "<code>rwxr-xr-x</code>: Chủ toàn quyền (7), Nhóm &amp; Khác chỉ đọc/chạy (5)"],
                        ["<code>chmod 640 / 600</code>", "<code>rw-r-----</code> / <code>rw-------</code>: Chuẩn tệp cấu hình nhóm / tệp khoá riêng"],
                    ],
                ),
                "Trên bảng là quy tắc đọc và lệnh đặt quyền bát phân trong Li-núc. Ba ký hiệu r, w, x lần lượt mang trọng số bốn, hai và một theo lũy thừa hai. Lệnh phân quyền sẽ áp ba chữ số cộng dồn đó lần lượt cho chủ sở hữu, nhóm cùng dự án và toàn bộ tài khoản khác trên máy.",
                introduces=["lnx_quyen_bat_phan"],
                clear=True,
            )
        ],
        "intuition_title": "Cấu trúc 9 bit phân quyền thành 3 chữ số hệ tám",
        "intuition_steps": [
            ak.st_auto(
                ak.svg_wrap(
                    960, 195,
                    ak.svg_rect(40, 45, 270, 100, "Chủ sở hữu (Owner)", "rwx = 4+2+1 = 7 | rw- = 6", ak.C_BLUE)
                    + ak.svg_rect(345, 45, 270, 100, "Nhóm (Group)", "r-x = 4+0+1 = 5 | r-- = 4", ak.C_AMBER)
                    + ak.svg_rect(650, 45, 270, 100, "Mọi người (Others)", "r-x = 5 | --- = 0 (khoá kín)", ak.C_GREEN),
                ),
                "Hình dung dãy chín bít quyền luôn chia thành ba ngăn đều đặn từ trái sang phải. Ngăn đầu tiên dành cho chính tài khoản tạo ra tệp nên thường mang giá trị sáu hoặc bảy. Ngăn giữa dành cho đồng đội chung nhóm, còn ngăn cuối dành cho mọi tài khoản lạ nên các tệp nhạy cảm phải khoá về không.",
                clear=True,
            )
        ],
        "formula_title": "Công thức cộng trọng số bát phân cho từng nhóm",
        "formula_steps": [
            ak.st_auto(
                ak.box(
                    "<p>Với mỗi nhóm 3 bit <code>(r, w, x)</code>: tổng quyền = <code>4×r + 2×w + 1×x</code> (từ 0 đến 7).</p>"
                    "<ul><li><code>rwxr-xr-x</code>: 4+2+1=7, 4+0+1=5, 4+0+1=5 → <b>755</b></li>"
                    "<li><code>rw-r-----</code>: 4+2+0=6, 4+0+0=4, 0+0+0=0 → <b>640</b></li>"
                    "<li><code>rw-------</code>: 6, 0, 0 → <b>600</b></li></ul>",
                    "key",
                ),
                "Công thức cộng trọng số rất đơn giản vì mỗi quyền đứng ứng với một bít độc lập của số ba bít. Nhờ ghép bốn cho đọc, hai cho ghi và một cho thực thi nên r-w-x cộng ra bảy, r-gạch-x ra năm và r-w-gạch ra sáu. Như vậy chuỗi ký hiệu r-w-x dài chín chữ cái được thu gọn hoàn toàn thành ba chữ số từ không đến bảy.",
                clear=True,
            )
        ],
        "formula_checks": ["alg.lnx_octal_mode('rwx', 'r-x', 'r-x') == '755'", "alg.lnx_octal_mode('rw-', 'r--', '---') == '640'", "alg.lnx_octal_mode('rw-', '---', '---') == '600'"],
        "example_title": "Chạy thật trên Docker Linux: đặt quyền 755, 640 và 600",
        "example_items": [
            {
                "type": "r3",
                "say": "Giải mã hai định dạng đầu ra của lệnh kiểm tra thuộc tính tệp trước khi chạy trong công-tai-nơ Li-núc thật.",
                "rows": [
                    ["<code>stat -c '%a' file</code>", "In ra mã quyền bát phân thực tế (ví dụ <code>755</code> hoặc <code>640</code>)"],
                    ["<code>stat -c '%A' file</code>", "In ra chuỗi 10 ký tự chuẩn như <code>-rw-r-----</code>"],
                    ["<code>SSH</code> (khoá 600)", "Giao thức kết nối máy chủ từ xa; bắt buộc giữ khoá riêng quyền <code>600</code>"],
                    ["<code>MSYS_NO_PATHCONV=1</code>", "Giữ nguyên đường dẫn Linux (<code>/tmp/...</code>) khi gọi Docker trên Git Bash Windows"],
                ],
            },
            {
                "type": "code",
                "pid": "p1",
                "title": "Đặt quyền thật 755 cho kịch bản chạy, 640 cho cấu hình và 600 cho khoá bí mật",
                "say": "Ta chạy thật trong công-tai-nơ Li-núc bằng cách tạo ba tệp tượng trưng cho chương trình chạy, tệp cấu hình nhóm và tệp khoá riêng tư. Sau khi gọi lệnh đặt quyền cho từng tệp, ta đọc ngược cả chữ số hệ tám lẫn chuỗi r-w-x từ hệ thống tệp nhân.",
                "out_say": "Đầu ra thật khớp từng chữ số với công thức cộng trọng số vì mã bảy năm năm hiện đủ quyền chạy và mã sáu không không xoá sạch mọi quyền của nhóm lẫn người ngoài.",
            },
        ],
        "progs": {
            "p1": {
                "code": (
                    "MSYS_NO_PATHCONV=1 docker run --rm postgres:17-alpine sh -c '\n"
                    "  touch /tmp/run.sh /tmp/app.env /tmp/id_ed25519\n"
                    "  chmod 755 /tmp/run.sh && chmod 640 /tmp/app.env && chmod 600 /tmp/id_ed25519\n"
                    "  for f in /tmp/run.sh /tmp/app.env /tmp/id_ed25519; do\n"
                    "    echo \"$(basename $f): $(stat -c \"%a %A\" $f)\"\n"
                    "  done\n"
                    "'"
                ),
                "expect": "run.sh: 755 -rwxr-xr-x\napp.env: 640 -rw-r-----\nid_ed25519: 600 -rw-------",
            },
            "p2": {
                "code": (
                    "awk 'BEGIN{\n"
                    "  n=split(\"rwxr-xr-x rw-r----- rw-------\", arr, \" \");\n"
                    "  for(k=1;k<=n;k++){ s=arr[k]; out=\"\";\n"
                    "    for(g=0;g<3;g++){ v=0;\n"
                    "      if(substr(s,g*3+1,1)==\"r\") v+=4;\n"
                    "      if(substr(s,g*3+2,1)==\"w\") v+=2;\n"
                    "      if(substr(s,g*3+3,1)==\"x\") v+=1; out=out v; }\n"
                    "    printf \"%s=%s%s\", s, out, (k<n?\" \":\"\\n\"); }\n"
                    "}'"
                ),
                "expect": "rwxr-xr-x=755 rw-r-----=640 rw-------=600",
            },
        },
        "example_checks": ["alg.lnx_octal_mode('rwx', 'r-x', 'r-x') == '755'"],
        "check_title": "Đối chứng quy đổi chuỗi rwx sang mã bát phân",
        "check_items": [
            {
                "type": "code",
                "pid": "p2",
                "title": "Tính lại trọng số từng cụm 3 ký tự từ chuỗi ký hiệu quyền",
                "say": "Ở đường kiểm chứng thứ hai, ta tính độc lập ba chữ số hệ tám trực tiếp từ chín ký tự r-w-x vì mỗi cụm ba ký tự cộng đúng một chữ số.",
                "out_say": "Đầu ra đối chứng khớp tuyệt đối ba kết quả bảy trăm năm mươi lăm, sáu trăm bốn mươi và sáu trăm vì phép tách từng cụm ba ký tự cộng đúng trọng số bít.",
            }
        ],
        "check_checks": ["alg.lnx_octal_mode('rwx', 'r-x', 'r-x') == '755'"],
        "quymo_title": "Hệ quả mở nhầm quyền 777 qua ba quy mô hạ tầng",
        "quymo_steps": [
            ak.st_auto(
                ak.table(
                    ["quy mô máy chủ", "số tài khoản/dịch vụ trên máy", "tác động nếu đặt quyền 777 bừa bãi"],
                    [
                        ["Máy cá nhân (1 người)", "1 tài khoản chính", "Vô tình tạo thói quen xấu trước khi lên máy thật"],
                        ["Máy chủ dùng chung (10 dịch vụ)", "10 tài khoản dịch vụ khác nhau", "Bất kỳ dịch vụ nào bị lộ đều sửa được tệp của dịch vụ kia"],
                        ["Cụm hệ thống (100 máy chủ)", "Hàng trăm khoá và cấu hình", "Mất hoàn toàn ranh giới cô lập đặc quyền tối thiểu"],
                    ],
                ),
                "Bảng quy mô giải thích vì sao nguyên tắc đặc quyền tối thiểu cấm tuyệt đối lệnh đặt quyền bảy bảy bảy để chữa cháy. Trên máy cá nhân lỗi này chưa gây hại rõ. Khi lên máy chủ có mười dịch vụ độc lập, chỉ một dịch vụ bị lỗi sẽ đọc và chép đè toàn bộ tệp của chín dịch vụ còn lại. Trên cụm một trăm máy chủ, quyền mở rộng toàn phần sẽ phá vỡ mọi lớp bảo vệ hệ thống.",
                clear=True,
            )
        ],
        "quymo_checks": ["7 * 100 + 7 * 10 + 7 == 777"],
        "pitfall_steps": [
            ak.st_auto(
                ak.box(
                    "<b>Lỗi 1: Dùng <code>chmod -R 777 /var/www</code> để 'sửa nhanh' lỗi Permission denied.</b> Bạn vừa trao quyền ghi và xoá cho mọi tài khoản trên máy.<br>"
                    "<b>Lỗi 2: Đặt quyền <code>644</code> cho tệp <code>.env</code> chứa mật khẩu DB.</b> Tài khoản khác dù không sửa được nhưng vẫn đọc hết mật khẩu.<br>"
                    "<b>Lỗi 3: Bỏ thiếu bit thực thi <code>x</code> trên thư mục (ví dụ đặt <code>644</code> cho thư mục).</b> Người dùng nhìn thấy tên tệp nhưng không <code>cd</code> vào được.",
                    "warn",
                ),
                "Có ba lỗi kinh điển về phân quyền mà kỹ sư mới rất hay vấp. Lỗi nguy hiểm nhất là gõ vội quyền bảy bảy bảy cho cả cây thư mục khiến mọi tài khoản trên máy đều sửa xoá được tệp quan trọng. Lỗi thứ hai là để tệp chứa mật khẩu ở quyền sáu bốn bốn làm lộ dữ liệu nhạy cảm. Lỗi thứ ba là bỏ quên quyền x trên thư mục khiến lệnh đi vào thư mục bị từ chối.",
                clear=True,
            )
        ],
        "quiz_steps": [
            ak.st(
                "<ol><li>Quy đổi chuỗi quyền <code>rw-r-----</code> sang mã 3 chữ số bát phân?</li>"
                "<li>Tệp chứa khoá SSH bí mật của riêng bạn nên đặt mã quyền bao nhiêu để vừa bảo mật vừa chạy được?</li></ol>",
                "Đến lượt bạn tự kiểm tra. Câu một, chuỗi r-w-gạch r-gạch-gạch và ba gạch cuối đổi sang mã ba chữ số bằng bao nhiêu? Câu hai, tệp chứa khoá bí mật của riêng bạn cần đặt mã quyền bao nhiêu để phần mềm kết nối chấp nhận? Hãy bấm tạm dừng và tự tính.",
                pause=20,
            ),
            ak.st(
                "<p>① <code>rw-</code> = 4+2 = <b>6</b>; <code>r--</code> = <b>4</b>; <code>---</code> = <b>0</b> → mã quyền là <b>640</b>.</p>",
                "Đáp án câu một: bốn cộng hai bằng sáu, chỉ đọc bằng bốn, và không có quyền bằng không, ghép lại thành mã sáu bốn không.",
                clear=True,
            ),
            ak.st(
                "<p>② Đặt <b>600</b> (<code>rw-------</code>) để chỉ duy nhất chủ sở hữu có quyền đọc và sửa.</p>",
                "Đáp án câu hai: luôn đặt mã sáu trăm để khoá kín hoàn toàn quyền đọc đối với nhóm lẫn mọi người dùng khác.",
                clear=True,
            ),
        ],
        "quiz_checks": ["alg.lnx_octal_mode('rw-', 'r--', '---') == '640'", "alg.lnx_octal_mode('rw-', '---', '---') == '600'"],
        "recap_steps": [
            ak.st_auto(
                "<div class='chain'><span class='n'>r=4, w=2, x=1</span><span class='a'>→</span>"
                "<span class='n'>Chủ | Nhóm | Khác</span><span class='a'>→</span>"
                "<span class='n'>755 chạy | 600/640 kín</span></div>",
                "Tổng kết công thức phân quyền bát phân cần nhớ suốt sự nghiệp vận hành Li-núc. Cộng các trọng số bốn hai một theo từng cụm ba bít cho chủ, nhóm và người ngoài. Dùng bảy năm năm cho tệp thực thi và luôn giữ sáu trăm hoặc sáu bốn không cho mọi tệp chứa thông tin nhạy cảm.",
                clear=True,
            )
        ],
        "lab_de": (
            "# Lab LNX L01 — Quy đổi phân quyền bát phân và xác định ngưỡng tối thiểu an toàn\n\n"
            "Viết kịch bản Bash tạo `sec.key` và `app.sh` trong thư mục tạm, thực hiện `chmod` và tính quy đổi để in đúng 3 dòng:\n"
            "1. `rwxr-xr-x=755`\n"
            "2. `rw-r-----=640`\n"
            "3. `rw-------=600`\n\n"
            "Chấm tự động:\n```bash\nbash labs/cham.sh LNX L01 duong_dan/bai_cua_ban.sh\n```"
        ),
        "lab_sol": (
            "#!/usr/bin/env bash\n"
            "set -euo pipefail\n"
            "W=$(mktemp -d)\n"
            "trap 'rm -rf \"$W\"' EXIT\n"
            "touch \"$W/sec.key\" \"$W/app.sh\"\n"
            "chmod 755 \"$W/app.sh\" && chmod 600 \"$W/sec.key\"\n"
            "awk 'BEGIN{\n"
            "  split(\"rwxr-xr-x rw-r----- rw-------\", a, \" \");\n"
            "  for(k=1;k<=3;k++){ s=a[k]; o=\"\";\n"
            "    for(g=0;g<3;g++){ v=0;\n"
            "      if(substr(s,g*3+1,1)==\"r\") v+=4;\n"
            "      if(substr(s,g*3+2,1)==\"w\") v+=2;\n"
            "      if(substr(s,g*3+3,1)==\"x\") v+=1; o=o v; }\n"
            "    printf \"%s=%s\\n\", s, o; }\n"
            "}'\n"
        ),
    }

    # ────────────────── L02: Tiến trình, mã thoát và tín hiệu SIGTERM vs SIGKILL ──────────────────
    l02 = {
        "id": "L02",
        "slug": "tien_trinh_tin_hieu",
        "title": "Tiến trình, mã thoát và tín hiệu SIGTERM vs SIGKILL",
        "next_title": "Luồng chuẩn, đường ống và lọc nhật ký dịch vụ trên Linux",
        "assumes": ["lnx_inode", "lnx_quyen_bat_phan"],
        "objectives": [
            "Giải thích quy ước mã thoát chuẩn 128 + số hiệu tín hiệu khi tiến trình bị ngắt",
            "Phân biệt SIGTERM (15 — cho phép dọn dẹp, đóng kết nối) với SIGKILL (9 — nhân ép dừng ngay)",
            "Nhận diện tiến trình thây ma (zombie) và cách tiến trình cha thu hồi trạng thái",
        ],
        "covers": [(1, "formula"), (2, "example"), (3, "check")],
        "hook_title": "Vì sao kill -9 hay làm hỏng dữ liệu đang chạy dở?",
        "hook_html": (
            "<p>Khi bạn gửi lệnh ép dừng số <b>9</b>, nhân hệ điều hành cắt ngang tiến trình tại chỗ mà không cho phép lưu tệp tạm hay đóng kết nối cơ sở dữ liệu.</p>"
            "<p>Ngược lại, tín hiệu dừng lịch sự số <b>15</b> gõ cửa yêu cầu tiến trình dọn dẹp sạch trước khi thoát với mã thoát <b>143</b>.</p>"
        ),
        "hook_say": (
            "Chào bạn, mỗi khi một dịch vụ bị treo, phản xạ đầu tiên của nhiều người là gõ ngay lệnh ép dừng số chín. "
            "Nhưng chính cú ép dừng đột ngột đó lại cắt ngang các yêu cầu đang ghi dở xuống cơ sở dữ liệu và để lại tệp khoá hỏng. "
            "Hôm nay ta phân biệt quy trình tắt dịch vụ lịch sự với lệnh chấm dứt cưỡng bức, đồng thời giải mã hai con số mã thoát quen thuộc một bốn ba và một ba bảy."
        ),
        "hook_checks": ["128 + 15 == 143", "128 + 9 == 137"],
        "prereq_steps": [
            ak.st_auto(
                ak.table(
                    ["nền tảng đã có", "vai trò ở bài tiến trình"],
                    [
                        ["Mã thoát 0 là thành công, khác 0 là lỗi (dòng lệnh)", "Tín hiệu ngắt quy ước mã thoát lớn hơn 128"],
                        ["Thư mục /proc chứa mã PID (L00)", "PID là mã định danh tiến trình; trạng thái lộ rõ tại /proc"],
                    ],
                ),
                "Bài này nối trực tiếp kiến thức về mã thoát và thư mục tiến trình ở các bài trước. Trong dòng lệnh Li-núc, mọi lệnh thành công đều trả về mã thoát bằng không. Khi tiến trình bị hệ thống ngắt bởi tín hiệu, mã thoát được cộng thêm một trăm hai mươi tám để phân biệt.",
                clear=True,
            )
        ],
        "sym_steps": [
            ak.st_auto(
                ak.table(
                    ["tín hiệu / lệnh", "số hiệu và cơ chế hoạt động"],
                    [
                        ["<code>SIGTERM</code> (mã 15)", "Tín hiệu dừng chuẩn: ứng dụng bắt được, chạy hàm <code>trap</code> dọn sạch rồi thoát"],
                        ["<code>SIGKILL</code> (mã 9)", "Tín hiệu cưỡng bức của nhân: không thể chặn, không thể bắt, cắt ngang tức thì"],
                        ["<code>trap ... TERM</code>", "Đăng ký hàm dọn dẹp trong Bash hoặc ứng dụng khi nhận tín hiệu dừng"],
                    ],
                ),
                "Trên bảng là ba quy ước tín hiệu cốt lõi của hệ điều hành Li-núc. Tín hiệu thứ nhất là tín hiệu dừng lịch sự mang số mười lăm viết tắt là xích-tơm, cho phép ứng dụng chạy xong tác vụ hiện tại rồi mới đóng tài nguyên. Tín hiệu thứ hai mang số chín gọi là xích-kiu do chính nhân thực thi ngay lập tức mà ứng dụng không tài nào chặn nổi.",
                introduces=["lnx_tin_hieu"],
                clear=True,
            )
        ],
        "intuition_title": "So sánh dòng sự kiện khi tiến trình nhận tín hiệu 15 vs tín hiệu 9",
        "intuition_steps": [
            ak.st_auto(
                ak.svg_wrap(
                    960, 210,
                    ak.svg_rect(40, 30, 260, 72, "Gửi SIGTERM (15)", "Mặc định của lệnh kill PID", ak.C_GREEN)
                    + ak.svg_arrow(300, 66, 395, 66, "Chạy handler")
                    + ak.svg_rect(395, 30, 270, 72, "Ứng dụng tự dọn sạch", "Đóng DB, xoá lock, xả log", ak.C_BLUE)
                    + ak.svg_arrow(665, 66, 735, 66, "Thoát")
                    + ak.svg_rect(735, 30, 185, 72, "Mã thoát 143", "128 + 15", ak.C_GRAY)
                    + ak.svg_rect(40, 122, 260, 72, "Gửi SIGKILL (9)", "Nhân ngắt thẳng tay", ak.C_RED)
                    + ak.svg_arrow(300, 158, 735, 158, "Không dọn gì cả")
                    + ak.svg_rect(735, 122, 185, 72, "Mã thoát 137", "128 + 9", ak.C_AMBER),
                ),
                "Nhìn hai đường chạy song song trên sơ đồ để thấy sự khác biệt một trời một vực. Ở nhánh trên, tín hiệu mười lăm gõ cửa để ứng dụng hoàn tất việc đóng kết nối, ghi hết bộ đệm rồi tự thoát với mã một trăm bốn mươi ba. Ở nhánh dưới, tín hiệu chín gạt bỏ mọi bước dọn dẹp và thu hồi tiến trình ngay lập tức kèm mã thoát một trăm ba mươi bảy.",
                clear=True,
            )
        ],
        "formula_title": "Công thức quy ước mã thoát từ tín hiệu nhân",
        "formula_steps": [
            ak.st_auto(
                ak.box(
                    "<p>Theo chuẩn POSIX, khi một tiến trình chấm dứt vì nhận tín hiệu số $S$, tiến trình cha nhận về mã thoát:</p>"
                    "<p><code>exit_code = 128 + S</code></p>"
                    "<p>Áp dụng ngay: <code>SIGTERM</code> (S = 15) → 128 + 15 = <b>143</b>; <code>SIGKILL</code> (S = 9) → 128 + 9 = <b>137</b>.</p>",
                    "key",
                ),
                "Công thức chuẩn rất ngắn gọn vì được quy định thống nhất trên toàn bộ thế giới dòng lệnh Li-núc. Khi một tiến trình dừng do tín hiệu mang số hiệu S, mã thoát trả về đúng bằng một trăm hai mươi tám cộng thêm số hiệu S đó. Do vậy nếu thấy container báo mã một bốn ba tức là nhận tín hiệu dừng bình thường, còn một ba bảy thường báo hiệu vừa bị cắt cưỡng bức.",
                clear=True,
            )
        ],
        "formula_checks": ["alg.lnx_sig_exit(15) == 143", "alg.lnx_sig_exit(9) == 137"],
        "example_title": "Chạy thật trên Docker: SIGTERM (143) vs SIGKILL (137)",
        "example_items": [
            {
                "type": "r3",
                "say": "Giải mã hai lệnh điều phối tiến trình nền trong thử nghiệm gửi tín hiệu thật.",
                "rows": [
                    ["<code>kill -TERM $pid</code>", "Gửi tín hiệu 15 lịch sự cho tiến trình có mã PID vừa chạy nền"],
                    ["<code>wait $pid; rc=$?</code>", "Chờ tiến trình kết thúc và thu nhận mã thoát thực sự vào biến <code>$?</code>"],
                    ["<code>PID</code> / <code>OOMKill</code>", "<code>PID</code>: mã số tiến trình trong nhân; <code>OOMKill</code>: nhân ngắt tiến trình vượt RAM (137)"],
                    ["<code>trap '...' TERM</code>", "Đăng ký lệnh dọn dẹp chạy trước khi tiến trình dừng khi nhận tín hiệu <code>SIGTERM</code>"],
                ],
            },
            {
                "type": "code",
                "pid": "p1",
                "title": "Thử thật trong Docker Alpine: tiến trình chạy hàm dọn khi gặp TERM và bỏ qua khi gặp KILL",
                "say": "Ta chạy hai tiến trình con ngay trong môi trường Li-núc thật và đều cài đặt hàm bẫy tín hiệu để ghi nhận quá trình dọn dẹp. Tiến trình thứ nhất nhận tín hiệu dừng mười lăm, còn tiến trình thứ hai nhận tín hiệu ép dừng chín.",
                "out_say": "Đầu ra chạy thật chứng minh tiến trình nhận tín hiệu mười lăm đã in ra dòng báo dọn dẹp trước khi thoát với mã một bốn ba. Tiến trình nhận tín hiệu chín im bặt không kịp chạy hàm dọn dẹp và trả ngay mã thoát một ba bảy.",
            },
        ],
        "progs": {
            "p1": {
                "code": (
                    "MSYS_NO_PATHCONV=1 docker run --rm postgres:17-alpine sh -c '\n"
                    "  sh -c \"trap \\\"echo cleaned; exit 143\\\" TERM; sleep 10\" &\n"
                    "  p1=$!; sleep 0.2; kill -TERM $p1; wait $p1 2>/dev/null; echo \"term_rc=$?\"\n"
                    "  sh -c \"trap \\\"echo should_not_print\\\" TERM; sleep 10\" &\n"
                    "  p2=$!; sleep 0.2; kill -KILL $p2; wait $p2 2>/dev/null; echo \"kill_rc=$?\"\n"
                    "'"
                ),
                "expect": "cleaned\nterm_rc=143\nkill_rc=137",
            },
            "p2": {
                "code": (
                    "echo \"TERM=$((128 + 15)) KILL=$((128 + 9))\""
                ),
                "expect": "TERM=143 KILL=137",
            },
        },
        "example_checks": ["alg.lnx_sig_exit(15) == 143", "alg.lnx_sig_exit(9) == 137"],
        "check_title": "Đối chứng quy đổi mã tín hiệu và nhận diện tiến trình thây ma",
        "check_items": [
            {
                "type": "code",
                "pid": "p2",
                "title": "Kiểm chéo trực tiếp công thức cộng 128 trên hai tín hiệu chính",
                "say": "Ta kiểm chéo lại hai con số cốt lõi bằng công thức số học vì cần đối chiếu trực tiếp với hai mã thoát vừa đo từ nhân Li-núc.",
                "out_say": "Kết quả tính toán trả về một trăm bốn mươi ba và một trăm ba bảy, vì cộng một trăm hai mươi tám với mười lăm và chín khớp chính xác hai mã vừa đo.",
            }
        ],
        "check_checks": ["128 + 15 == 143", "128 + 9 == 137"],
        "quymo_title": "Thời gian tắt máy chủ và rủi ro hỏng dữ liệu qua ba quy mô cụm",
        "quymo_steps": [
            ak.st_auto(
                ak.table(
                    ["quy mô máy chủ", "hậu quả nếu dùng kill -9 thường xuyên", "quy trình chuẩn tắt dịch vụ"],
                    [
                        ["1 dịch vụ đơn", "Mất vài kết nối người dùng hiện tại", "Gửi tín hiệu 15, chờ tối đa 10 giây"],
                        ["10 dịch vụ nền hàng đợi", "Công việc xử lý nửa chừng mất dấu vết", "Nhận tín hiệu 15 để hoàn tất tác vụ đang dở"],
                        ["100 nút cụm triển khai lại", "Hàng nghìn yêu cầu rớt lỗi 502 hàng loạt", "Chờ tắt êm rồi mới rút máy khỏi cân bằng tải"],
                    ],
                ),
                "Bảng quy mô cho thấy thói quen dùng lệnh ép dừng gây thiệt hại lớn ra sao khi hệ thống mở rộng. Ở cụm một trăm máy chủ triển khai liên tục, cắt ngang kết nối thay vì chờ dừng êm rất nguy hiểm. Hành động này làm hàng nghìn yêu cầu khách hàng văng lỗi năm trăm linh hai cùng lúc. Do đó mọi trình điều phối chuẩn đều gửi tín hiệu mười lăm trước rồi mới đếm ngược thời gian chờ.",
                clear=True,
            )
        ],
        "quymo_checks": ["100 * 10 == 1000"],
        "pitfall_steps": [
            ak.st_auto(
                ak.box(
                    "<b>Lỗi 1: Chạy <code>kill -9</code> ngay từ đầu thay vì dùng <code>kill</code> mặc định (SIGTERM).</b> Tín hiệu 9 không cho phép đóng kết nối hay lưu trạng thái.<br>"
                    "<b>Lỗi 2: Gửi lại tín hiệu cho tiến trình thây ma (trạng thái Z / zombie) mà thấy không chết.</b> Tiến trình đó đã chết sẵn, chỉ chờ tiến trình cha thu hồi mã thoát.<br>"
                    "<b>Lỗi 3: Quên viết hàm đón tín hiệu dừng trong ứng dụng container.</b> Khi nhận tín hiệu 15 không có bộ xử lý, dịch vụ phải đợi hết hạn 10 giây mới bị cắt bằng mã 137.",
                    "warn",
                ),
                "Hãy tránh ba lỗi rất phổ biến khi quản lý tiến trình Li-núc. Thứ nhất đừng bao giờ gõ vội số chín trước khi thử tín hiệu mười lăm. Thứ hai nếu thấy tiến trình mang trạng thái chữ Z thây ma, lệnh giết sẽ vô tác dụng vì nó đã chết rồi mà chỉ chờ tiến trình cha thu hồi trạng thái. Thứ ba nhớ luôn viết bộ đón tín hiệu dừng trong ứng dụng công-tai-nơ để khởi động lại nhanh chóng.",
                clear=True,
            )
        ],
        "quiz_steps": [
            ak.st(
                "<ol><li>Nhật ký công-tai-nơ báo vừa thoát với mã thoát <code>137</code>. Đây là hậu quả của tín hiệu số mấy?</li>"
                "<li>Khi triển khai phiên bản mới cho máy chủ web đang phục vụ khách, nên gửi tín hiệu nào trước?</li></ol>",
                "Đến lượt bạn tự kiểm tra. Câu một, nếu dịch vụ vừa dừng đột ngột kèm mã thoát một trăm ba mươi bảy, nó vừa nhận tín hiệu mang số mấy? Câu hai, khi nâng cấp phiên bản máy chủ đang phục vụ người dùng thật, ta phải gửi tín hiệu nào trước tiên? Dừng vi-đê-ô lại và kiểm tra câu trả lời.",
                pause=20,
            ),
            ak.st(
                "<p>① Tín hiệu số <code>137 - 128 = 9</code> (<code>SIGKILL</code> — ép dừng ngay hoặc hết RAM OOMKill).</p>",
                "Đáp án câu một: lấy một trăm ba mươi bảy trừ đi một trăm hai mươi tám bằng chín, tức là vừa bị ép dừng bằng tín hiệu số chín hoặc hết bộ nhớ.",
                clear=True,
            ),
            ak.st(
                "<p>② Luôn gửi <code>SIGTERM</code> (15) trước để ứng dụng hoàn tất giao dịch dở rồi tự tắt sạch.</p>",
                "Đáp án câu hai: luôn gửi tín hiệu mười lăm trước để ứng dụng hoàn tất nốt yêu cầu đang xử lý rồi tự đóng sạch sẽ.",
                clear=True,
            ),
        ],
        "quiz_checks": ["137 - 128 == 9", "143 - 128 == 15"],
        "recap_steps": [
            ak.st_auto(
                "<div class='chain'><span class='n'>SIGTERM (15) → dọn sạch → 143</span><span class='a'>|</span>"
                "<span class='n'>SIGKILL (9) → cắt ngang → 137</span></div>",
                "Tổng kết chuỗi logic về tiến trình và tín hiệu điều khiển. Tín hiệu mười lăm lịch sự trả mã thoát một bốn ba, còn tín hiệu chín cưỡng bức trả mã một ba bảy và không chạy dọn dẹp. Luôn ưu tiên tắt êm trước khi buộc phải dùng đến biện pháp cuối cùng.",
                clear=True,
            )
        ],
        "lab_de": (
            "# Lab LNX L02 — Tính mã thoát POSIX và kiểm chứng dọn dẹp khi nhận SIGTERM\n\n"
            "Viết kịch bản Bash tạo subshell có `trap` đón tín hiệu `TERM` in ra `graceful=1` rồi thoát mã `143`, gửi `kill -TERM`, và in đúng 3 dòng:\n"
            "1. `graceful=1`\n"
            "2. `term_exit=143`\n"
            "3. `kill_exit=137`\n\n"
            "Chấm tự động:\n```bash\nbash labs/cham.sh LNX L02 duong_dan/bai_cua_ban.sh\n```"
        ),
        "lab_sol": (
            "#!/usr/bin/env bash\n"
            "set -u\n"
            "bash -c 'trap \"echo graceful=1; exit 143\" TERM; while :; do sleep 0.05; done' &\n"
            "p1=$!\n"
            "sleep 0.15\n"
            "kill -TERM \"$p1\"\n"
            "wait \"$p1\" 2>/dev/null\n"
            "echo \"term_exit=$?\"\n"
            "echo \"kill_exit=$((128 + 9))\"\n"
        ),
    }

    # ────────────────── L03: Luồng chuẩn, đường ống và lọc nhật ký ──────────────────
    l03 = {
        "id": "L03",
        "slug": "luong_nhat_ky_loc_du_lieu",
        "title": "Luồng chuẩn, đường ống và lọc nhật ký dịch vụ trên Linux",
        "next_title": "Ổ đĩa, phần trăm dung lượng và giới hạn chỉ mục hệ thống tệp",
        "assumes": ["lnx_inode", "lnx_quyen_bat_phan", "lnx_tin_hieu"],
        "objectives": [
            "Tách luồng chuẩn (1) và luồng lỗi (2) khi ghi log và chuyển hướng",
            "Dùng grep/awk theo đường ống để đếm số lỗi 5xx theo phút trên tệp log lớn",
            "Ước lượng thời gian quét 100 000 dòng log khi lọc tại chỗ so với truyền mạng",
        ],
        "covers": [(1, "formula"), (2, "example"), (3, "quymo")],
        "hook_title": "Vì sao chuyển hướng ra tệp lại bỏ sót dòng báo lỗi?",
        "hook_html": (
            "<p>Bạn gõ <code>./app &gt; run.log</code> rồi đi ngủ, sáng dậy thấy tệp trống trơn trong khi màn hình ban đêm tràn ngập lỗi đỏ.</p>"
            "<p>Lý do: dấu <code>&gt;</code> mặc định chỉ gom <b>luồng chuẩn (số 1)</b>, còn <b>luồng lỗi (số 2)</b> đi lối riêng nếu không gộp <code>2&gt;&amp;1</code>.</p>"
        ),
        "hook_say": (
            "Chào bạn, rất nhiều người vận hành máy chủ từng gặp cảnh chuyển đầu ra ra tệp nhưng sáng hôm sau mở lên chỉ thấy tệp trống. "
            "Lý do nằm ở cơ chế tách hai ống dẫn dữ liệu song song cho mỗi chương trình chạy trên Li-núc. "
            "Hôm nay ta nắm vững cách tách gộp luồng chuẩn với luồng lỗi và cách dùng đường ống lọc nhanh hàng trăm nghìn dòng nhật ký tại chỗ."
        ),
        "hook_checks": ["120 + 30 == 150"],
        "prereq_steps": [
            ak.st_auto(
                ak.table(
                    ["nền tảng đã có", "ứng dụng lọc nhật ký"],
                    [
                        ["Đường ống dẫn đầu ra giữa hai lệnh", "Nối đầu ra của lệnh đọc lọc thẳng sang lệnh thống kê"],
                        ["Mã thoát tiến trình khi kết thúc (L02)", "Kiểm tra pipeline không bỏ sót lỗi âm thầm"],
                    ],
                ),
                "Ta nối tiếp thói quen dùng đường ống và kiểm tra mã thoát từ các bài trước. Đường ống cho phép dữ liệu chảy trực tiếp từ lệnh trước sang lệnh sau qua bộ nhớ mà không phải ghi ra tệp trung gian chậm chạp.",
                clear=True,
            )
        ],
        "sym_steps": [
            ak.st_auto(
                ak.table(
                    ["ký hiệu luồng / lọc", "ý nghĩa trên dòng lệnh"],
                    [
                        ["<code>1&gt; out.txt</code> / <code>2&gt; err.txt</code>", "Chuyển hướng tách riêng luồng chuẩn (1) và luồng lỗi (2)"],
                        ["<code>&gt; all.log 2&gt;&amp;1</code>", "Ghi cả luồng chuẩn lẫn luồng lỗi vào chung một tệp nhật ký"],
                        ["<code>grep</code> | <code>awk</code> | <code>wc -l</code>", "Lọc mẫu văn bản, tách cột trường dữ liệu và đếm số dòng khớp"],
                    ],
                ),
                "Trên bảng là ba quy ước thao tác với luồng chuẩn và bộ công cụ lọc dòng lệnh. Số một đại diện cho luồng chuẩn in kết quả bình thường, còn số hai đại diện cho luồng lỗi báo sự cố. Khi cần gom trọn cả hai luồng vào chung một tệp, ta đặt lệnh gộp luồng hai vào luồng một ở phía sau tên tệp. Phía dưới là ba công cụ chuẩn gồm gờ-rếp tìm mẫu, oóc tách cột và đếm dòng.",
                clear=True,
            )
        ],
        "intuition_title": "Hai dòng chảy song song từ một tiến trình: stdout (1) và stderr (2)",
        "intuition_steps": [
            ak.st_auto(
                ak.svg_wrap(
                    960, 200,
                    ak.svg_rect(40, 50, 210, 95, "Tiến trình chạy", "Xuất 2 luồng riêng", ak.C_BLUE)
                    + ak.svg_arrow(250, 75, 390, 62, "FD 1 (stdout)")
                    + ak.svg_arrow(250, 120, 390, 138, "FD 2 (stderr)")
                    + ak.svg_rect(390, 25, 230, 68, "Luồng chuẩn (1)", "> out.log bắt được", ak.C_GREEN)
                    + ak.svg_rect(390, 108, 230, 68, "Luồng lỗi (2)", "Phải dùng 2> hoặc 2>&1", ak.C_RED)
                    + ak.svg_arrow(620, 98, 710, 98, "2>&1 gộp")
                    + ak.svg_rect(710, 48, 210, 95, "Đường ống lọc", "grep 5xx | awk | sort", ak.C_AMBER),
                ),
                "Nhìn sơ đồ hai ống xả riêng biệt thoát ra từ một tiến trình đang chạy. Ống phía trên mang số hiệu một đi qua dấu lớn hơn để chảy vào tệp nhật ký chuẩn. Ống phía dưới mang số hiệu hai vẫn chảy thẳng ra màn hình trừ khi bạn chuyển riêng hoặc nối thẳng vào ống số một qua ký hiệu gộp hai trỏ sang một.",
                clear=True,
            )
        ],
        "formula_title": "Thống kê lỗi 5xx và quy tắc thứ tự chuyển hướng",
        "formula_steps": [
            ak.st_auto(
                ak.box(
                    "<p>Thứ tự đọc từ trái sang phải trong shell: <code>cmd &gt; all.log 2&gt;&amp;1</code> (luồng 1 trỏ vào tệp trước, rồi luồng 2 mới chép địa chỉ của luồng 1).</p>"
                    "<p>Ví dụ kiểm chứng log 10 000 dòng: 120 lỗi 500 + 30 lỗi 503 → tổng lỗi 5xx = 120 + 30 = <b>150</b> dòng, tỉ lệ = 150 / 10 000 = <b>1,5%</b>.</p>",
                    "key",
                ),
                "Trình dòng lệnh phân tích các dấu chuyển hướng nghiêm ngặt từ trái sang phải nên thứ tự viết quyết định tất cả. Vì luồng một phải gắn vào tệp nhật ký trước thì phép nối luồng hai sang luồng một đứng sau mới trỏ đúng vào tệp đó. Trong ví dụ mười nghìn dòng, một trăm hai mươi lỗi năm trăm cộng ba mươi lỗi năm trăm linh ba bằng đúng một trăm năm mươi lỗi. Con số này tương đương tỉ lệ một phẩy năm phần trăm.",
                clear=True,
            )
        ],
        "formula_checks": ["120 + 30 == 150", "abs(150 / 10000 - 0.015) < 1e-9"],
        "example_title": "Chạy thật: tách hai luồng 1/2 và lọc tổng lỗi 5xx bằng awk",
        "example_items": [
            {
                "type": "r3",
                "say": "Giải mã hai mẫu biểu thức tách trường và bộ đếm cộng dồn dùng trong kịch bản lọc nhật ký. Các lệnh kết hợp ba bộ mô tả luồng không một hai, biểu thức mẫu và lệnh sắp xếp.",
                "rows": [
                    ["<code>$2 ~ /^5[0-9][0-9]$/</code>", "Kiểm tra cột thứ hai có đúng là mã lỗi 5xx (từ 500 đến 599)"],
                    ["<code>c[$1]++</code> | <code>sort</code>", "<code>c[$1]++</code> đếm gộp theo cột phút; <code>sort</code> sắp xếp dòng theo thứ tự"],
                    ["<code>FD 0 / 1 / 2</code>", "Mã luồng (File Descriptor): <code>0</code> nhập chuẩn, <code>1</code> xuất chuẩn, <code>2</code> luồng lỗi"],
                ],
            },
            {
                "type": "code",
                "pid": "p1",
                "title": "Sinh 10 000 dòng log mẫu (120 lỗi 500, 30 lỗi 503) và lọc nhanh bằng awk",
                "say": "Kịch bản tạo một tệp nhật ký mẫu đúng mười nghìn dòng gồm chín nghìn tám trăm năm mươi dòng hai trăm, một trăm hai mươi lỗi năm trăm và ba mươi lỗi năm trăm linh ba. Sau đó dùng một đường ống chuẩn để tách riêng luồng chuẩn với luồng lỗi rồi đếm số lỗi năm ích-ích.",
                "out_say": "Đầu ra chạy thật chứng minh luồng chuẩn và luồng lỗi được ghi vào hai tệp tách biệt không lẫn lộn. Lệnh lọc oóc đếm ra đúng một trăm năm mươi dòng lỗi ứng với tỉ lệ một phẩy năm phần trăm trên tổng mười nghìn dòng.",
            },
        ],
        "progs": {
            "p1": {
                "code": (
                    "mkdir -p test_l03 && cd test_l03\n"
                    "(echo 'ok_stdout'; echo 'err_stderr' >&2) > out.txt 2> err.txt\n"
                    "awk 'BEGIN{for(i=1;i<=10000;i++){\n"
                    "  if(i<=120) print \"10:01 500\"; else if(i<=150) print \"10:02 503\";\n"
                    "  else print \"10:00 200\"}}' > app.log\n"
                    "ec=$(awk '$2~/^5[0-9][0-9]$/{n++} END{print n+0}' app.log)\n"
                    "tot=$(wc -l < app.log | tr -d ' ')\n"
                    "echo \"stdout=$(cat out.txt) stderr=$(cat err.txt) total=$tot err5xx=$ec\""
                ),
                "expect": "stdout=ok_stdout stderr=err_stderr total=10000 err5xx=150",
            },
            "p2": {
                "code": (
                    "awk 'BEGIN{tot=10000; err=150; printf \"pct=%.1f%%\\n\", (err*100.0)/tot}'"
                ),
                "expect": "pct=1.5%",
            },
        },
        "example_checks": ["120 + 30 == 150", "10000 - 150 == 9850"],
        "check_title": "Đối chứng tỉ lệ phần trăm lỗi 5xx và kiểm tra thứ tự gộp 2>&1",
        "check_items": [
            {
                "type": "code",
                "pid": "p2",
                "title": "Tính tỉ lệ phần trăm lỗi trên 10 000 dòng nhật ký",
                "say": "Ở đường kiểm chứng thứ hai, ta tính độc lập tỉ lệ phần trăm lỗi năm ích-ích vì cần đối chiếu lại số liệu mười nghìn dòng ban đầu.",
                "out_say": "Đầu ra đối chứng trả về đúng một phẩy năm phần trăm vì một trăm năm mươi chia mười nghìn nhân một trăm vừa tròn con số đó.",
            }
        ],
        "check_checks": ["round(150 * 100 / 10000, 1) == 1.5"],
        "quymo_title": "So sánh tốc độ lọc tại chỗ bằng đường ống vs tải toàn bộ log về máy",
        "quymo_steps": [
            ak.st_auto(
                ak.table(
                    ["cỡ tệp nhật ký", "lọc tại chỗ trên máy chủ (awk/grep)", "tải toàn bộ qua mạng văn phòng 50 Mbps"],
                    [
                        ["10 000 dòng (~1 MB)", "Dưới 0,02 giây tại đĩa", "~0,2 giây truyền mạng"],
                        ["100 000 dòng (~10 MB)", "~0,05 giây tại đĩa (lọc xong trước)", "~1,6 giây truyền mạng"],
                        ["10 000 000 dòng (~1 GB)", "~2 giây đọc tuần tự", "~160 giây kéo qua mạng mới đọc"],
                    ],
                ),
                "Bảng quy mô giải thích nguyên tắc vàng khi chẩn đoán sự cố: luôn lọc trực tiếp trên máy chủ nơi tệp nhật ký đang nằm thay vì tải cả tệp về máy cá nhân. Ở mức một trăm nghìn dòng, lệnh oóc chạy ngay tại đĩa chỉ mất năm phần trăm giây, nhanh gấp hơn ba mươi lần so với kéo toàn tệp qua mạng văn phòng. Lên tới một gi-ga-bai nhật ký, lọc tại chỗ tiết kiệm hàng phút quý báu giữa lúc sự cố.",
                clear=True,
            )
        ],
        "quymo_checks": ["round(10 * 8 / 50, 2) == 1.6"],
        "pitfall_steps": [
            ak.st_auto(
                ak.box(
                    "<b>Lỗi 1: Viết ngược <code>cmd 2&gt;&amp;1 &gt; run.log</code>.</b> Luồng 2 chép nhầm đích màn hình của luồng 1 trước khi luồng 1 rẽ vào tệp, khiến lỗi vẫn rớt ra ngoài.<br>"
                    "<b>Lỗi 2: Dùng dấu <code>&gt;</code> đơn đè mất nhật ký cũ.</b> Phải dùng <code>&gt;&gt;</code> nếu muốn nối tiếp vào cuối nhật ký đang chạy.<br>"
                    "<b>Lỗi 3: Chạy <code>cat big.log | grep ERR</code> thay vì <code>grep ERR big.log</code>.</b> Tạo tiến trình thừa thãi đọc lại toàn bộ tệp qua đường ống.",
                    "warn",
                ),
                "Hãy tránh ba lỗi rất dễ mắc với luồng và nhật ký. Lỗi hay gặp nhất là đảo ngược hai cụm chuyển hướng làm luồng lỗi vẫn thoát ra màn hình dù bạn tưởng đã ghi chung tệp. Lỗi thứ hai là dùng một dấu lớn hơn ghi đè bay sạch dữ liệu điều tra cũ. Lỗi thứ ba là lạm dụng lệnh đọc dư thừa trước lệnh tìm mẫu trên tệp hàng trăm mê-ga-bai.",
                clear=True,
            )
        ],
        "quiz_steps": [
            ak.st(
                "<ol><li>Muốn ghi CẢ đầu ra chuẩn lẫn thông báo lỗi của <code>./srv</code> vào cuối tệp <code>app.log</code> (không xoá cũ), viết thế nào?</li>"
                "<li>Trên tệp log 10 000 dòng có 150 dòng mã 5xx, tỉ lệ lỗi bằng bao nhiêu phần trăm?</li></ol>",
                "Đến lượt bạn tự kiểm tra. Câu một, viết chính xác lệnh nối tiếp cả luồng chuẩn lẫn luồng lỗi vào cuối tệp nhật ký mà không ghi đè dữ liệu cũ? Câu hai, một trăm năm mươi dòng lỗi trên mười nghìn dòng là bao nhiêu phần trăm? Bấm tạm dừng và trả lời ra giấy.",
                pause=20,
            ),
            ak.st(
                "<p>① <code>./srv &gt;&gt; app.log 2&gt;&amp;1</code> (dùng <code>&gt;&gt;</code> trước, đặt <code>2&gt;&amp;1</code> ở cuối).</p>",
                "Đáp án câu một: mở nối tiếp tệp nhật ký bằng dấu nối đôi rồi đặt cụm gộp luồng hai sang luồng một ở vị trí sau cùng.",
                clear=True,
            ),
            ak.st(
                "<p>② <code>150 / 10 000 = 1,5%</code>.</p>",
                "Đáp án câu hai: lấy một trăm năm mươi chia cho mười nghìn ta được tỉ lệ lỗi bằng một phẩy năm phần trăm.",
                clear=True,
            ),
        ],
        "quiz_checks": ["round(150 * 100 / 10000, 1) == 1.5"],
        "recap_steps": [
            ak.st_auto(
                "<div class='chain'><span class='n'>1=chuẩn | 2=lỗi</span><span class='a'>→</span>"
                "<span class='n'>&gt; tệp 2&gt;&amp;1</span><span class='a'>→</span>"
                "<span class='n'>Lọc tại chỗ bằng grep/awk</span></div>",
                "Tổng kết ba điểm cốt lõi cần giữ khi làm việc với nhật ký dịch vụ. Tách rạch ròi luồng chuẩn một với luồng lỗi hai, luôn đặt cụm nối gộp phía sau tên tệp đích, và tận dụng đường ống lọc dữ liệu ngay tại chỗ trên máy chủ.",
                clear=True,
            )
        ],
        "lab_de": (
            "# Lab LNX L03 — Tách luồng 1/2 và lọc lỗi 5xx bằng đường ống\n\n"
            "Viết kịch bản Bash tách stdout (luồng 1) và stderr (luồng 2), tạo nhật ký 100 dòng có 12 lỗi 500 và 3 lỗi 503 rồi in đúng 3 dòng:\n"
            "1. `stdout_ok=1`\n"
            "2. `stderr_ok=1`\n"
            "3. `err_5xx=15`\n\n"
            "Chấm tự động:\n```bash\nbash labs/cham.sh LNX L03 duong_dan/bai_cua_ban.sh\n```"
        ),
        "lab_sol": (
            "#!/usr/bin/env bash\n"
            "set -euo pipefail\n"
            "W=$(mktemp -d)\n"
            'trap \'rm -rf "$W"\' EXIT\n'
            'cd "$W"\n'
            "(echo 'OK'; echo 'ERR' >&2) > o.txt 2> e.txt\n"
            "awk 'BEGIN{for(i=1;i<=100;i++){if(i<=12)print \"500\"; else if(i<=15)print \"503\"; else print \"200\"}}' > log.txt\n"
            "c=$(grep -cE '^5[0-9]{2}$' log.txt)\n"
            '[ "$(cat o.txt)" = "OK" ] && so=1 || so=0\n'
            '[ "$(cat e.txt)" = "ERR" ] && se=1 || se=0\n'
            "echo \"stdout_ok=$so\"\n"
            "echo \"stderr_ok=$se\"\n"
            "echo \"err_5xx=$c\"\n"
        ),
    }

    # ────────────────── L04: Ổ đĩa, dung lượng khối vs hết inode ──────────────────
    l04 = {
        "id": "L04",
        "slug": "o_dia_dung_luong_inode",
        "title": "Ổ đĩa, phần trăm dung lượng và lỗi hết inode khi đĩa vẫn còn trống",
        "next_title": "Mạng Linux thực chiến: cổng đang nghe, /etc/hosts, DNS và curl",
        "assumes": ["lnx_inode", "lnx_quyen_bat_phan", "lnx_tin_hieu"],
        "objectives": [
            "Phân biệt báo cáo dung lượng khối (df -h) với số lượng inode còn lại (df -i)",
            "Giải thích vì sao hàng triệu tệp 0 byte làm đầy bảng inode dù dung lượng chiếm gần 0%",
            "Đếm số inode tiêu thụ cho n tệp trong một thư mục",
        ],
        "covers": [(1, "formula"), (2, "example"), (3, "check")],
        "hook_title": "Báo hết đĩa dù df -h chỉ báo mới dùng 40%?",
        "hook_html": (
            "<p>Một dịch vụ sinh <b>10 triệu tệp phiên (session) rỗng</b> kích thước vài chục byte trong thư mục <code>/tmp</code>.</p>"
            "<p>Dung lượng ổ đĩa mới tốn 40%, nhưng toàn bộ bảng chỉ mục tệp đã hết sạch chỗ trống, khiến hệ thống không tạo nổi một tệp 1 byte nào nữa.</p>"
        ),
        "hook_say": (
            "Chào bạn, đây là một trong những sự cố kinh điển khiến nhiều kỹ sư vận hành lúng túng hàng giờ liền. "
            "Ứng dụng đột ngột báo lỗi hết dung lượng ổ đĩa nhưng khi chạy lệnh kiểm tra phần trăm đĩa thì thấy mới dùng có bốn mươi phần trăm. "
            "Thủ phạm nằm ở giới hạn số lượng i-nốt mà phân vùng đĩa hỗ trợ cho các tệp nhỏ xíu. "
            "Hôm nay ta học cách kiểm tra song song dung lượng khối lẫn số i-nốt và tính đúng mức tiêu thụ trên thư mục."
        ),
        "hook_checks": ["10000 + 1 == 10001"],
        "prereq_steps": [
            ak.st_auto(
                ak.table(
                    ["nền tảng từ bài trước", "liên kết với sự cố hết đĩa"],
                    [
                        ["Mỗi tệp và thư mục riêng dùng 1 i-nốt (L00)", "Không thể tạo tệp mới nếu bảng i-nốt đã cạn kiệt"],
                        ["Dùng đường ống lọc sắp xếp đếm nhanh (L03)", "Tìm chính xác thư mục nào đang ôm hàng triệu tệp nhỏ"],
                    ],
                ),
                "Ta ghép bài 0 và bài 3 để xử lý sự cố đĩa ảo. Nhờ bài 0 ta biết mỗi tệp lẫn mỗi thư mục đều tốn đúng một mục trong bảng i-nốt cố định của phân vùng. Nhờ đường ống lọc từ bài 3, ta dễ dàng thống kê thư mục nào đang tích trữ lượng tệp khổng lồ.",
                clear=True,
            )
        ],
        "sym_steps": [
            ak.st_auto(
                ak.table(
                    ["lệnh kiểm tra đĩa", "những gì nó thực sự đo"],
                    [
                        ["<code>df -h</code>", "Kiểm tra phần trăm dung lượng khối dữ liệu (GB) đang dùng và còn trống"],
                        ["<code>df -i</code>", "Kiểm tra số lượng i-nốt tối đa, đã dùng và phần trăm i-nốt còn lại"],
                        ["<code>du -sh *</code>", "Đo dung lượng thật từng thư mục con (khác với đếm số lượng tệp)"],
                    ],
                ),
                "Trên bảng là ba lệnh đo đạc lưu trữ không thể thiếu khi ứng cứu máy chủ. Lệnh đầu kiểm tra phần trăm dung lượng khối dữ liệu tính bằng gi-ga-bai. Lệnh thứ hai kiểm tra số lượng nút chỉ mục i-nốt đã dùng trên mỗi phân vùng. Lệnh thứ ba đo tổng kích thước từng thư mục để khoanh vùng chỗ đang phình to.",
                clear=True,
            )
        ],
        "intuition_title": "Hai giới hạn độc lập trên cùng một phân vùng: khối dữ liệu vs khe i-nốt",
        "intuition_steps": [
            ak.st_auto(
                ak.svg_wrap(
                    960, 200,
                    ak.svg_rect(40, 45, 410, 110, "Bãi dữ liệu (df -h): 40% đã dùng", "Còn dư 60 GB cho nội dung lớn", ak.C_BLUE)
                    + ak.svg_rect(510, 45, 410, 110, "Bảng thẻ i-nốt (df -i): 100% ĐẦY", "Cạn sạch chỗ tạo thêm tệp dù 0 byte", ak.C_RED),
                ),
                "Hãy tưởng tượng phân vùng đĩa giống một thư viện có hai tài nguyên hoàn toàn tách biệt. Bên trái là kệ sách rộng lớn chứa dung lượng ghi dữ liệu mới lấp bốn mươi phần trăm. Bên phải là tủ phiếu đánh số i-nốt có số ngăn cố định từ lúc định dạng đĩa. Nay tủ phiếu đã đầy kín một trăm phần trăm nên không thể cấp thẻ mới cho bất kỳ tệp nào.",
                clear=True,
            )
        ],
        "formula_title": "Công thức đếm i-nốt tiêu thụ trong thư mục",
        "formula_steps": [
            ak.st_auto(
                ak.box(
                    "<p>Mỗi tệp thông thường chiếm $1$ i-nốt <b>và</b> chính thư mục chứa nó cũng chiếm $1$ i-nốt.</p>"
                    "<p>Do đó một thư mục chứa $N$ tệp rỗng $0$ byte tốn $N \\times 0 = \\hl{0\\text{ byte}}$ dữ liệu, nhưng tiêu thụ đúng $N + 1$ i-nốt.</p>"
                    "<p>Với $N = 10\\,000$ tệp rỗng: tổng i-nốt $= 10\\,000 + 1 = \\hl{10\\,001}$ i-nốt.</p>",
                    "key",
                ),
                "Công thức đếm rất chính xác vì cả tệp thường lẫn thư mục chứa đều là một đối tượng trong cây hệ thống tệp. Một tệp rỗng không bai không tiêu tốn thêm khối lưu trữ dữ liệu nhưng vẫn bắt buộc phải giữ một mục i-nốt riêng. Vì vậy thư mục chứa mười nghìn tệp rỗng tiêu thụ đúng mười nghìn cộng một bằng mười nghìn không trăm linh một i-nốt.",
                clear=True,
            )
        ],
        "formula_checks": ["alg.lnx_inode_used(10_000) == 10_001"],
        "example_title": "Chạy thật trên Docker: kiểm df -h, df -i và đếm i-nốt",
        "example_items": [
            {
                "type": "r3",
                "say": "Giải thích hai lệnh đếm số lượng đối tượng trên phân vùng trước khi chạy thử nghiệm trên hệ thống tệp Li-núc.",
                "rows": [
                    ["<code>find dir | wc -l</code>", "Đếm cả thư mục cha lẫn tất cả tệp con (= số i-nốt riêng biệt nếu không có hardlink)"],
                    ["<code>df -i /tmp</code>", "Đọc số lượng i-nốt tối đa và hiện có của phân vùng chứa <code>/tmp</code>"],
                ],
            },
            {
                "type": "code",
                "pid": "p1",
                "title": "Chạy thật trên Docker Alpine: đo df -h, df -i và tạo 200 tệp 0 byte đếm i-nốt",
                "say": "Ta chạy trực tiếp trong công-tai-nơ Li-núc để quan sát hai báo cáo đĩa rồi tạo một thư mục chứa hai trăm tệp không bai. Sau đó dùng lệnh tìm kiếm đếm toàn bộ phần tử và kiểm tra tổng dung lượng nội dung lẫn siêu dữ liệu thư mục.",
                "out_say": "Đầu ra thật xác nhận hai trăm tệp rỗng cùng thư mục cha tạo thành hai trăm linh một đối tượng i-nốt. Tổng dữ liệu nội dung bằng không bai và thư mục chỉ tốn bốn ki-lô-bai siêu dữ liệu tên tệp.",
            },
        ],
        "progs": {
            "p1": {
                "code": (
                    "MSYS_NO_PATHCONV=1 docker run --rm postgres:17-alpine sh -c '\n"
                    "  mkdir -p /tmp/sess; i=1\n"
                    "  while [ $i -le 200 ]; do : > /tmp/sess/f_$i; i=$((i+1)); done\n"
                    "  cnt=$(find /tmp/sess | wc -l)\n"
                    "  db=$(cat /tmp/sess/f_* | wc -c)\n"
                    "  sz=$(du -sk /tmp/sess | awk \"{print \\$1}\")\n"
                    "  df -h /tmp | tail -n 1 | awk \"{print \\\"blocks_pct=\\\"\\$5}\"\n"
                    "  echo \"objects=$cnt content_bytes=$db dir_meta_kb=$sz\"\n"
                    "'"
                ),
                "expect_sub": ["objects=201", "content_bytes=0"],
            },
            "p2": {
                "code": (
                    "n=10000; d=1; echo \"data_bytes=$((n * 0)) inodes=$((n + d))\""
                ),
                "expect": "data_bytes=0 inodes=10001",
            },
        },
        "example_checks": ["alg.lnx_inode_used(200) == 201"],
        "check_title": "Kiểm chéo mô hình số i-nốt cho 10 000 tệp rỗng",
        "check_items": [
            {
                "type": "code",
                "pid": "p2",
                "title": "Tính ngược dung lượng dữ liệu và số i-nốt khi có 10 000 tệp 0 byte",
                "say": "Ở đường kiểm chứng thứ hai, ta tính lại mức tiêu thụ i-nốt cho mười nghìn tệp rỗng vì cần xác nhận công thức cộng một thư mục.",
                "out_say": "Kết quả tính toán xác nhận dữ liệu bằng không bai và số i-nốt bằng mười nghìn không trăm linh một vì mỗi tệp cộng thêm một thư mục cha đều tốn một i-nốt.",
            }
        ],
        "check_checks": ["alg.lnx_inode_used(10000) == 10001"],
        "quymo_title": "Khi nào bảng i-nốt chạm trần qua ba quy mô tệp nhỏ",
        "quymo_steps": [
            ak.st_auto(
                ak.table(
                    ["quy mô tạo tệp nhỏ (100 byte/tệp)", "dung lượng khối thực chiếm", "số i-nốt bị ngốn trên phân vùng"],
                    [
                        ["1 000 tệp phiên", "~100 KB (gần 0%)", "1 001 i-nốt"],
                        ["100 000 tệp phiên rác", "~10 MB (0,1% đĩa 10 GB)", "100 001 i-nốt (~15% bảng i-nốt)"],
                        ["655 360 tệp trên đĩa 10 GB (~16KB/i-nốt)", "~65 MB (chưa tới 1% đĩa)", "100% i-nốt ĐẦY CỨNG → Sập toàn máy"],
                    ],
                ),
                "Bảng quy mô giải thích vì sao một phân vùng mười gi-ga-bai chỉ mới dùng chưa tới một phần trăm dung lượng nhưng đã sập hoàn toàn. Với cấu hình định dạng mặc định, cứ khoảng mười sáu ki-lô-bai ổ đĩa mới sinh ra một i-nốt nên tổng phân vùng chứa được hơn sáu trăm năm mươi nghìn tệp. Chỉ cần một dịch vụ rác sinh đủ con số tệp đó thì toàn máy không tạo nổi thêm bất kỳ tệp mới nào nữa.",
                clear=True,
            )
        ],
        "quymo_checks": ["100000 * 100 == 10_000_000"],
        "pitfall_steps": [
            ak.st_auto(
                ak.box(
                    "<b>Lỗi 1: Chỉ xem <code>df -h</code> rồi kết luận đĩa không hề đầy.</b> Khi ứng dụng báo hết chỗ, luôn chạy thêm <code>df -i</code> ngay lập tức.<br>"
                    "<b>Lỗi 2: Dùng <code>rm /tmp/sess/*</code> trên thư mục có 500 000 tệp.</b> Lệnh mở rộng ký tự sao sẽ văng lỗi 'Argument list too long'; hãy dùng <code>find ... -delete</code>.<br>"
                    "<b>Lỗi 3: Xoá nhầm tệp lớn đang có tiến trình giữ mở mà tưởng dung lượng về ngay.</b> Như bài 0 đã dạy, chỗ trống chỉ nhả ra khi tiến trình đóng tệp.",
                    "warn",
                ),
                "Có ba cái bẫy rất hay gặp khi xử lý đầy đĩa trên máy chủ thật. Thứ nhất chỉ xem phần trăm dung lượng mà bỏ quên kiểm tra số i-nốt còn lại. Thứ hai chạy lệnh xoá kèm dấu sao lên thư mục nửa triệu tệp làm dòng lệnh vỡ tràn danh sách đối số thay vì dùng lệnh tìm để xoá từng đợt. Thứ ba xoá nhầm nhật ký đang được tiến trình mở nên dung lượng đĩa vẫn không giảm xuống.",
                clear=True,
            )
        ],
        "quiz_steps": [
            ak.st(
                "<ol><li>Ổ đĩa báo <code>df -h</code> dùng 35% nhưng <code>df -i</code> dùng 100%. Kết quả khi chạy <code>touch new.txt</code> là gì?</li>"
                "<li>Một thư mục mới tạo chứa 50 tệp 0 byte tiêu thụ tất cả bao nhiêu i-nốt?</li></ol>",
                "Đến lượt bạn tự kiểm tra. Câu một, nếu dung lượng khối mới chiếm ba mươi lăm phần trăm nhưng bảng i-nốt đã đạt một trăm phần trăm, lệnh tạo tệp mới sẽ thành công hay thất bại? Câu hai, một thư mục chứa đúng năm mươi tệp không bai tiêu thụ tất cả bao nhiêu i-nốt? Bấm tạm dừng và trả lời ra giấy.",
                pause=20,
            ),
            ak.st(
                "<p>① Thất bại ngay với lỗi hết chỗ (<code>No space left on device</code>), vì không còn khe i-nốt trống.</p>",
                "Đáp án câu một: lệnh tạo tệp thất bại ngay lập tức vì hết hoàn toàn khe i-nốt dù dung lượng đĩa vẫn còn rất rộng.",
                clear=True,
            ),
            ak.st(
                "<p>② 50 tệp + 1 thư mục chứa = <b>51 i-nốt</b>.</p>",
                "Đáp án câu hai: năm mươi tệp cộng thêm một i-nốt của chính thư mục chứa bằng đúng năm mươi mốt i-nốt.",
                clear=True,
            ),
        ],
        "quiz_checks": ["alg.lnx_inode_used(50) == 51"],
        "recap_steps": [
            ak.st_auto(
                "<div class='chain'><span class='n'>df -h (GB)</span><span class='a'>≠</span>"
                "<span class='n'>df -i (số lượng i-nốt)</span><span class='a'>|</span>"
                "<span class='n'>N tệp + 1 thư mục = N + 1 i-nốt</span></div>",
                "Tổng kết công thức chẩn đoán lưu trữ cần nắm chắc sau bài 4. Luôn kiểm tra đồng thời dung lượng khối và giới hạn i-nốt mỗi khi gặp thông báo hết chỗ. Nhớ rằng mỗi thư mục chứa N tệp luôn tiêu thụ tổng cộng N cộng một i-nốt bất kể kích thước tệp bằng không.",
                clear=True,
            )
        ],
        "lab_de": (
            "# Lab LNX L04 — Đếm i-nốt tiêu thụ thực tế của thư mục chứa nhiều tệp nhỏ\n\n"
            "Viết kịch bản Bash tạo thư mục tạm chứa `50` tệp 0 byte (nhỏ gọn trong lab), tính cả quy mô `10 000` tệp qua công thức và in đúng 3 dòng:\n"
            "1. `files=50`\n"
            "2. `objects_50=51`\n"
            "3. `inodes_10k=10001`\n\n"
            "Chấm tự động:\n```bash\nbash labs/cham.sh LNX L04 duong_dan/bai_cua_ban.sh\n```"
        ),
        "lab_sol": (
            "#!/usr/bin/env bash\n"
            "set -euo pipefail\n"
            "W=$(mktemp -d)\n"
            'trap \'rm -rf "$W"\' EXIT\n'
            'mkdir -p "$W/dir"\n'
            'i=1; while [ "$i" -le 50 ]; do : > "$W/dir/f_$i"; i=$((i + 1)); done\n'
            'fc=$(find "$W/dir" -type f | wc -l | tr -d " ")\n'
            'oc=$(find "$W/dir" | wc -l | tr -d " ")\n'
            "echo \"files=$fc\"\n"
            "echo \"objects_50=$oc\"\n"
            "echo \"inodes_10k=$((10000 + 1))\"\n"
        ),
    }

    return [l00, l01, l02, l03, l04]
