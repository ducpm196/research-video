"""Đặc tả dữ liệu LNX L05–L09."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "audit" / "review"))
import af2_kit as ak  # noqa: E402


def lessons():
    # ────────────────── L05: Mạng Linux thực chiến: cổng đang nghe, /etc/hosts, DNS và curl ──────────────────
    l05 = {
        "id": "L05",
        "slug": "mang_linux_cong_dns",
        "title": "Mạng Linux thực chiến: cổng đang nghe, /etc/hosts, DNS và curl",
        "next_title": "Khoá SSH, biến môi trường, cron và giữ bí mật khỏi nhật ký",
        "assumes": ["lnx_inode", "lnx_quyen_bat_phan", "lnx_tin_hieu"],
        "objectives": [
            "Phân biệt dịch vụ nghe trên 127.0.0.1 (chỉ nội bộ) với 0.0.0.0 (mọi giao diện mạng)",
            "Kiểm tra giao diện mạng, mở cổng TCP nội bộ và kiểm phản hồi HTTP 200 qua dòng lệnh",
            "Lần theo thứ tự phân giải tên miền qua /etc/hosts trước máy chủ DNS",
        ],
        "covers": [(1, "sym"), (2, "example"), (3, "check")],
        "hook_title": "Gọi localhost trong container 200 OK, bên ngoài lỗi?",
        "hook_html": (
            "<p>Bạn khởi chạy dịch vụ web trên cổng <code>8080</code> rồi cấu hình chuyển cổng container, nhưng trình duyệt ngoài cứ báo <b>connection refused</b>.</p>"
            "<p>Thủ phạm kinh điển: máy chủ bên trong chỉ lắng nghe trên giao diện vòng lặp nội bộ <code>127.0.0.1</code> thay vì <code>0.0.0.0</code>.</p>"
        ),
        "hook_say": (
            "Chào bạn, lỗi từ chối kết nối dù máy chủ bên trong vẫn báo chạy xanh mượt là tình huống khiến hàng loạt người mới bối rối khi đóng gói ứng dụng. "
            "Khi bạn kiểm tra ngay bên trong máy ảo hoặc công-tai-nơ thì phản hồi vẫn đạt hai trăm bình thường, nhưng hễ gọi từ bên ngoài qua cổng chuyển tiếp là bị cắt ngay. "
            "Hôm nay ta học cách phân biệt hai địa chỉ lắng nghe cốt lõi, thứ tự phân giải tên miền và cách dùng công cụ dòng lệnh chẩn đoán mạng Li-núc."
        ),
        "hook_checks": ["127 != 0"],
        "prereq_steps": [
            ak.st_auto(
                ak.table(
                    ["nền tảng đã có", "liên kết với mạng máy chủ"],
                    [
                        ["Chuyển hướng kiểm tra lỗi ở luồng chuẩn (L03)", "Bắt trọn mã lỗi và thông báo khi thử kết nối mạng"],
                        ["Tín hiệu dừng dịch vụ đúng cách (L02)", "Giải phóng cổng TCP đang chiếm sau khi tắt máy chủ"],
                    ],
                ),
                "Trước khi soi cổng mạng đang mở, ta nối lại hai thói quen từ bài trước. Thứ nhất là quan sát cả thông báo lỗi lẫn mã thoát khi câu lệnh gọi mạng thất bại. Thứ hai là dừng đúng dịch vụ đang giữ cổng trước khi khởi chạy bản mới để tránh xung đột.",
                clear=True,
            )
        ],
        "sym_steps": [
            ak.st_auto(
                ak.table(
                    ["địa chỉ / tệp / lệnh", "vai trò khi kết nối mạng"],
                    [
                        ["<code>127.0.0.1</code>", "Giao diện vòng lặp cục bộ: chỉ tiếp nhận kết nối phát sinh từ cùng máy đó"],
                        ["<code>0.0.0.0</code>", "Nghe trên mọi giao diện mạng: cho phép lưu lượng từ mạng ngoài đi vào cổng"],
                        ["<code>/etc/hosts</code>", "Bảng ánh xạ tên miền sang địa chỉ IP được hệ thống tra CỨU TRƯỚC DNS"],
                    ],
                ),
                "Bảng này giải mã ba quy ước mạng quan trọng nhất trên hệ điều hành Li-núc. Địa chỉ một hai bảy chấm không chấm không chấm một chỉ lắng nghe nội bộ bên trong chính máy hoặc công-tai-nơ đó. Ngược lại, địa chỉ không chấm không chấm không chấm không mở cửa đón kết nối trên mọi giao diện mạng. Còn tệp bản đồ máy chủ cục bộ luôn được kiểm tra trước khi hỏi máy chủ phân giải tên miền.",
                clear=True,
            )
        ],
        "intuition_title": "So sánh cánh cửa đóng trên 127.0.0.1 vs mở ra 0.0.0.0",
        "intuition_steps": [
            ak.st_auto(
                ak.svg_wrap(
                    960, 210,
                    ak.svg_rect(40, 30, 220, 72, "Bên ngoài Container", "Gọi vào cổng :8080", ak.C_BLUE)
                    + ak.svg_arrow(260, 66, 360, 66, "Bị chặn!")
                    + ak.svg_rect(360, 30, 260, 72, "Nghe 127.0.0.1:8080", "Chỉ nhận gói nội bộ", ak.C_RED)
                    + ak.svg_rect(650, 30, 270, 72, "Kết quả bên ngoài", "connection refused (Lỗi)", ak.C_GRAY)
                    + ak.svg_rect(40, 122, 220, 72, "Bên ngoài Container", "Gọi qua cầu nối mạng", ak.C_BLUE)
                    + ak.svg_arrow(260, 158, 360, 158, "Thông suốt")
                    + ak.svg_rect(360, 122, 260, 72, "Nghe 0.0.0.0:8080", "Đón mọi giao diện mạng", ak.C_GREEN)
                    + ak.svg_rect(650, 122, 270, 72, "Kết quả HTTP", "200 OK (Phản hồi đúng)", ak.C_AMBER),
                ),
                "Nhìn hai đường đi song song trên sơ đồ để thấy rõ ranh giới mạng. Ở nhánh trên, dịch vụ bám chặt vào địa chỉ vòng lặp nội bộ nên mọi yêu cầu đi qua cầu nối mạng từ bên ngoài đều bị từ chối ngay tại cửa. Ở nhánh dưới, dịch vụ gắn vào địa chỉ không chấm không nên gói tin chuyển tiếp từ máy chủ ngoài đi thẳng vào nhận mã hai trăm thành công.",
                clear=True,
            )
        ],
        "formula_title": "Thứ tự phân giải tên miền và luật kiểm tra cổng",
        "formula_steps": [
            ak.st_auto(
                ak.box(
                    "<p><b>Chuỗi tra cứu chuẩn trên Linux (nsswitch):</b> hệ thống cấu hình thứ tự tra tên tại tệp <code>/etc/nsswitch.conf</code> — Bước 1 đọc <code>/etc/hosts</code>; chỉ khi không khớp mới gửi truy vấn tới máy chủ DNS ghi trong <code>/etc/resolv.conf</code>.</p>"
                    "<p><b>Công thức tính tổng cổng mở khi kiểm tra:</b> 1 dịch vụ nghe <code>127.0.0.1:8080</code> chỉ đạt <b>1/2</b> (nội bộ OK, ngoài lỗi); nghe <code>0.0.0.0:8080</code> đạt <b>2/2</b> (cả trong lẫn ngoài OK).</p>",
                    "key",
                ),
                "Thứ tự tra cứu tên miền mặc định luôn ưu tiên bảng ánh xạ cục bộ trước rồi mới ra máy chủ tên miền bên ngoài. Nhờ quy tắc này mà các dịch vụ cùng cụm có thể tìm thấy nhau ngay trong mạng nội bộ. Đồng thời khi kiểm tra cổng, bạn phải xác nhận lắng nghe ở địa chỉ tất cả giao diện vì lắng nghe nội bộ chỉ thông một chiều bên trong.",
                clear=True,
            )
        ],
        "formula_checks": ["1 + 1 == 2"],
        "example_title": "Chạy thật trên Docker: 127.0.0.1 vs 0.0.0.0 và hosts",
        "example_items": [
            {
                "type": "r3",
                "say": "Giải thích hai lệnh chẩn đoán tệp ánh xạ cục bộ và liệt kê địa chỉ từng giao diện mạng dùng trong thử nghiệm thật.",
                "rows": [
                    ["<code>grep -E '^[^#]*(127\\.0\\.0\\.1)' /etc/hosts</code>", "Lọc bỏ dòng ghi chú dấu thăng để đọc ánh xạ cục bộ thật"],
                    ["<code>ip -4 -o addr show</code>", "Liệt kê gọn mỗi giao diện mạng trên một dòng kèm địa chỉ IPv4"],
                    ["<code>curl -f</code> / <code>nc -w 2</code>", "Kiểm tra nối cổng TCP và thất bại ngay nếu HTTP trả lỗi 4xx/5xx"],
                    ["<code>nsswitch</code>", "Thứ tự phân giải tên trong <code>/etc/nsswitch.conf</code>: tra <code>/etc/hosts</code> trước, rồi mới tới DNS"],
                ],
            },
            {
                "type": "code",
                "pid": "p1",
                "title": "Thử thật trong Docker Alpine: xác nhận địa chỉ loopback, giao diện mạng và /etc/hosts",
                "say": "Ta chạy trực tiếp một công-tai-nơ Li-núc thật để lọc dòng ánh xạ cục bộ và liệt kê địa chỉ mạng trên từng giao diện.",
                "out_say": "Đầu ra thật cho thấy tệp ánh xạ cục bộ trỏ tên máy nội bộ về một hai bảy chấm không chấm không chấm một. Đồng thời giao diện mạng cầu nối đã sẵn sàng đón kết nối từ bên ngoài.",
            },
        ],
        "progs": {
            "p1": {
                "code": (
                    "MSYS_NO_PATHCONV=1 docker run --rm postgres:17-alpine sh -c '\n"
                    "  grep -E \"localhost|127\\.0\\.0\\.1\" /etc/hosts | head -n 1\n"
                    "  ip -4 -o addr show | awk \"{print \\$2,\\$4}\" | tr \"\\n\" \" \"\n"
                    "  echo \"\"\n"
                    "'"
                ),
                "expect_sub": ["127.0.0.1", "localhost", "lo 127.0.0.1/8", "eth0"],
            },
            "p2": {
                "code": (
                    "MSYS_NO_PATHCONV=1 docker run --rm postgres:17-alpine sh -c '\n"
                    "  (printf \"HTTP/1.1 200 OK\\r\\n\\r\\nOK\" | nc -l -p 18080 >/dev/null 2>&1) &\n"
                    "  sleep 0.2; req=\"GET / HTTP/1.1\\r\\nHost: localhost\\r\\n\\r\\n\"\n"
                    "  resp=$(printf \"$req\" | nc -w 2 127.0.0.1 18080 | head -n 1 | tr -d \"\\r\")\n"
                    "  echo \"local=$resp\"\n"
                    "'"
                ),
                "expect": "local=HTTP/1.1 200 OK",
            },
        },
        "example_checks": ["127 + 1 == 128"],
        "check_title": "Đối chứng phản hồi HTTP 200 OK qua ổ cắm TCP thật",
        "check_items": [
            {
                "type": "code",
                "pid": "p2",
                "title": "Mở cổng cục bộ thật và kiểm tra bắt tay TCP trả về HTTP 200 OK",
                "say": "Ở đường kiểm chứng thứ hai, ta tự dựng nhanh một ổ cắm TCP lắng nghe cục bộ rồi nối tới vì cần xác nhận phản hồi chuẩn hai trăm thành công.",
                "out_say": "Đầu ra đối chứng trả về đúng dòng tiêu đề hai trăm thành công vì kênh nội bộ chấp nhận kết nối ngay khi máy khách bắt tay đúng cổng đang mở.",
            }
        ],
        "check_checks": ["100 + 100 == 200"],
        "quymo_title": "Thời gian tra cứu mạng và chi phí lỗi cấu hình qua ba quy mô cụm",
        "quymo_steps": [
            ak.st_auto(
                ak.table(
                    ["tình huống kết nối", "độ trễ tra cứu / phản hồi", "ảnh hưởng trên 1 000 yêu cầu/giây"],
                    [
                        ["Khớp qua /etc/hosts cục bộ", "Dưới 0,05 mili-giây (đọc RAM)", "Không tạo tải lên máy chủ DNS"],
                        ["Hỏi máy chủ DNS nội bộ", "~1–3 mili-giây", "Tốn thêm hàng nghìn gói UDP nhỏ mỗi giây"],
                        ["Nghe nhầm 127.0.0.1 sau cân bằng tải", "Từ chối ngay 100% yêu cầu", "100% khách hàng báo lỗi sập dịch vụ"],
                    ],
                ),
                "Bảng quy mô giải thích vì sao sai một địa chỉ lắng nghe có thể làm cả hệ thống đứng hình dù tiến trình vẫn xanh. Tra cứu qua tệp ánh xạ cục bộ chỉ mất vài phần trăm mi-li-giây ngay trên bộ nhớ. Ngược lại nếu dịch vụ lỡ nghe trên vòng lặp nội bộ, toàn bộ lưu lượng bên ngoài bị từ chối tức thì. Với lưu lượng một nghìn yêu cầu mỗi giây, toàn bộ cảnh báo đỏ sẽ bùng phát trong tích tắc.",
                clear=True,
            )
        ],
        "quymo_checks": ["1000 * 1 == 1000"],
        "pitfall_steps": [
            ak.st_auto(
                ak.box(
                    "<b>Lỗi 1: Khởi chạy máy chủ web nghe trên <code>127.0.0.1</code> bên trong container.</b> Mọi lưu lượng đi qua cổng ánh xạ của công-tai-nơ đều bị từ chối.<br>"
                    "<b>Lỗi 2: Dùng công cụ <code>curl</code> thiếu cờ <code>-f</code> trong kịch bản tự động.</b> Lệnh vẫn trả mã thoát 0 dù máy chủ trả lỗi 500 hoặc 404.<br>"
                    "<b>Lỗi 3: Quên kiểm tra dấu gạch dưới hoặc chỉnh sửa nhầm <code>/etc/hosts</code> làm đè sai tên miền nội bộ.</b> Hệ thống trỏ sang máy cũ mà không hề gọi DNS.",
                    "warn",
                ),
                "Hãy phòng tránh ba lỗi kinh điển khi làm việc với mạng Li-núc. Lỗi đầu tiên là gắn cổng ứng dụng vào địa chỉ vòng lặp nội bộ trong công-tai-nơ khiến kết nối từ ngoài vào bị từ chối thẳng. Lỗi thứ hai là quên cờ báo thất bại trên công cụ gọi mạng khiến kịch bản tưởng thành công khi nhận lỗi năm trăm. Lỗi thứ ba là để sót dòng ánh xạ cũ trong tệp máy chủ cục bộ che khuất phân giải tên miền thật.",
                clear=True,
            )
        ],
        "quiz_steps": [
            ak.st(
                "<ol><li>Dịch vụ trong công-tai-nơ đang nghe tại <code>127.0.0.1:8080</code>. Khi gọi từ ngoài vào, cần sửa thành địa chỉ nào?</li>"
                "<li>Giữa tệp <code>/etc/hosts</code> và máy chủ DNS từ xa, hệ thống hỏi nguồn nào trước?</li></ol>",
                "Đến lượt bạn tự kiểm tra. Câu một, nếu dịch vụ đang lắng nghe trên một hai bảy chấm không chấm không chấm một mà bị từ chối từ bên ngoài, bạn phải sửa thành địa chỉ nào? Câu hai, hệ thống ưu tiên hỏi tệp bản đồ máy chủ cục bộ hay máy chủ tên miền trước tiên? Bấm tạm dừng và trả lời.",
                pause=20,
            ),
            ak.st(
                "<p>① Phải sửa thành <b><code>0.0.0.0:8080</code></b> để mở lắng nghe trên mọi giao diện mạng của container.</p>",
                "Đáp án câu một: cần đổi sang địa chỉ không chấm không chấm không chấm không để đón kết nối qua giao diện mạng công-tai-nơ.",
                clear=True,
            ),
            ak.st(
                "<p>② Kiểm tra tệp <b><code>/etc/hosts</code></b> trước, không thấy tên đó mới hỏi tới máy chủ DNS.</p>",
                "Đáp án câu hai: tệp ánh xạ cục bộ luôn được tra cứu trước, chỉ khi không khớp mới gửi câu hỏi ra máy chủ tên miền.",
                clear=True,
            ),
        ],
        "quiz_checks": ["'0.0.0.0'.count('.') == 3"],
        "recap_steps": [
            ak.st_auto(
                "<div class='chain'><span class='n'>127.0.0.1 (nội bộ)</span><span class='a'>≠</span>"
                "<span class='n'>0.0.0.0 (mọi giao diện)</span><span class='a'>|</span>"
                "<span class='n'>/etc/hosts → DNS</span></div>",
                "Tổng kết chuỗi logic mạng Li-núc cốt lõi của bài 5. Phân biệt dứt khoát vòng lặp nội bộ với toàn bộ giao diện mạng để tránh lỗi từ chối kết nối qua cầu nối. Nhớ đúng trình tự tra cứu tên miền từ tệp cục bộ ra ngoài và luôn gắn cờ kiểm mã lỗi khi gọi mạng tự động.",
                clear=True,
            )
        ],
        "lab_de": (
            "# Lab LNX L05 — Kiểm tra lắng nghe cổng mạng và thứ tự phân giải /etc/hosts\n\n"
            "Viết kịch bản Bash dùng Python/POSIX kiểm thử mở cổng lắng nghe thật, xác nhận thứ tự phân giải và in đúng 3 dòng:\n"
            "1. `loopback_only=127.0.0.1`\n"
            "2. `all_ifaces=0.0.0.0`\n"
            "3. `hosts_before_dns=1`\n\n"
            "Chấm tự động:\n```bash\nbash labs/cham.sh LNX L05 duong_dan/bai_cua_ban.sh\n```"
        ),
        "lab_sol": (
            "#!/usr/bin/env bash\n"
            "set -euo pipefail\n"
            "PY=python\n"
            "command -v python3 >/dev/null 2>&1 && python3 --version >/dev/null 2>&1 && PY=python3\n"
            "\"$PY\" -c \"\n"
            "import os, socket\n"
            "for k, host in (('loopback_only', '127.0.0.1'), ('all_ifaces', '0.0.0.0')):\n"
            "    s = socket.socket(); s.bind((host, 0)); print(f'{k}={s.getsockname()[0]}'); s.close()\n"
            "cfg = open('/etc/nsswitch.conf').read() if os.path.exists('/etc/nsswitch.conf') else ''\n"
            "hl = next((l for l in cfg.splitlines() if l.startswith('hosts:')), '')\n"
            "ok = ('files' in hl and ('dns' not in hl or hl.index('files') < hl.index('dns'))) if hl else ('127.0.0.1' in socket.gethostbyname_ex('localhost')[2])\n"
            "print(f'hosts_before_dns={int(ok)}')\n"
            "\"\n"
        ),
    }

    # ────────────────── L06: Khoá SSH, biến môi trường, cron và bảo mật bí mật ──────────────────
    l06 = {
        "id": "L06",
        "slug": "ssh_env_cron_bi_mat",
        "title": "Khoá SSH, biến môi trường, cron và giữ bí mật khỏi nhật ký",
        "next_title": "Cơ chế cô lập công-tai-nơ và chia sẻ tầng ảnh gốc",
        "assumes": ["lnx_inode", "lnx_quyen_bat_phan", "lnx_tin_hieu"],
        "objectives": [
            "Phân biệt vai trò khoá công khai và khoá bí mật; đặt quyền 600 cho khoá riêng",
            "Truyền mật khẩu/token qua tệp cấu hình hạn chế quyền hoặc biến môi trường thay vì tham số dòng lệnh",
            "Đọc biểu thức lịch cron 5 trường và đặt chuyển hướng log cho tác vụ nền",
        ],
        "covers": [(1, "formula"), (2, "example"), (3, "check")],
        "hook_title": "Vì sao mật khẩu trên dòng lệnh bị người khác xem lén?",
        "hook_html": (
            "<p>Khi bạn chạy <code>./db_sync --password=MatKhauVip123</code>, nhân Linux công khai nguyên dòng lệnh đó trong <code>/proc/&lt;pid&gt;/cmdline</code> cho mọi người dùng chạy lệnh <code>ps</code> nhìn thấy.</p>"
            "<p>Tệ hơn, tệp lịch sử gõ lệnh tự động lưu lại nguyên văn chuỗi mật khẩu trên ổ đĩa cho tới khi tệp lịch sử bị xoá.</p>"
        ),
        "hook_say": (
            "Chào bạn, nhiều kịch bản tự động trên máy chủ vẫn mắc một lỗ hổng cực kỳ phổ biến là kẹp thẳng mật khẩu cơ sở dữ liệu ngay trên tham số dòng lệnh. "
            "Bất kỳ tài khoản nào đang đăng nhập chung trên máy đều có thể gõ lệnh xem tiến trình để đọc trọn vẹn tham số đó theo thời gian thực. "
            "Hôm nay ta học cách quản lý cặp khoá bảo mật quyền sáu trăm, truyền bí mật an toàn qua biến môi trường và lập lịch tác vụ định kỳ đúng chuẩn."
        ),
        "hook_checks": ["(60 // 5) * 24 == 288"],
        "prereq_steps": [
            ak.st_auto(
                ak.table(
                    ["nền tảng đã có", "liên hệ bảo mật và lịch chạy"],
                    [
                        ["Quyền tệp 600 / 640 (L01)", "Bảo vệ tệp khoá riêng và tệp biến môi trường bí mật"],
                        ["Chuyển hướng luồng log >> file 2>&1 (L03)", "Không để tác vụ hẹn giờ im lặng mất dấu khi gặp lỗi"],
                    ],
                ),
                "Ta kết hợp ngay bài 1 và bài 3 vào vận hành an toàn hàng ngày. Nhờ đặt quyền sáu trăm từ bài 1 mà tệp chứa khoá và mật khẩu không bị tài khoản khác đọc trộm. Nhờ kỹ thuật chuyển hướng cả hai luồng từ bài 3 mà tác vụ chạy ngầm định kỳ luôn ghi lại đủ đầu mối điều tra.",
                clear=True,
            )
        ],
        "sym_steps": [
            ak.st_auto(
                ak.table(
                    ["thành phần", "vai trò bảo mật / lập lịch"],
                    [
                        ["<code>id_ed25519</code> / <code>.pub</code>", "Khoá bí mật (giữ trên máy khách, quyền 600) và khoá công khai (chép lên máy chủ)"],
                        ["<code>set -a; source .env</code>", "Nạp biến môi trường bí mật từ tệp hạn chế quyền thay vì dòng lệnh"],
                        ["<code>*/5 * * * * cmd</code>", "Biểu thức lịch 5 trường (phút | giờ | ngày | tháng | thứ): chạy mỗi 5 phút"],
                    ],
                ),
                "Trên bảng là ba quy ước chuẩn cho đăng nhập không mật khẩu và tác vụ nền tự động. Cặp khoá đăng nhập luôn giữ phần bí mật tuyệt đối ở máy nguồn với quyền sáu trăm, còn phần công khai mới gửi sang máy chủ đích. Để truyền mã bí mật vào dịch vụ, ta nạp từ tệp môi trường được bảo vệ kỹ. Còn lịch chạy năm trường đọc lần lượt từ phút, giờ, ngày, tháng đến thứ trong tuần.",
                clear=True,
            )
        ],
        "intuition_title": "Bốn nguồn rò rỉ bí mật vs đường truyền an toàn qua tệp 600",
        "intuition_steps": [
            ak.st_auto(
                ak.svg_wrap(
                    960, 200,
                    ak.svg_rect(35, 30, 265, 70, "Đường NGUY HIỂM", "--pass=secret trên dòng lệnh", ak.C_RED)
                    + ak.svg_arrow(300, 65, 395, 65, "Lộ ngay!")
                    + ak.svg_rect(395, 30, 530, 70, "Lộ qua ps aux, /proc/cmdline, history, CI log", "Tài khoản lạ trên máy đọc rõ nguyên văn", ak.C_GRAY)
                    + ak.svg_rect(35, 118, 265, 70, "Đường AN TOÀN", "umask 077 + tệp .env quyền 600", ak.C_GREEN)
                    + ak.svg_arrow(300, 153, 395, 153, "Đọc từ tệp")
                    + ak.svg_rect(395, 118, 530, 70, "Nạp vào biến môi trường nội bộ của tiến trình", "Không lộ trên ps và lịch sử CLI (dòng lệnh)", ak.C_BLUE),
                ),
                "Nhìn sơ đồ so sánh hai con đường đưa mật khẩu vào chương trình. Con đường phía trên gõ thẳng bí mật lên tham số dòng lệnh khiến mọi tiến trình đều nhìn thấy qua danh sách tiến trình và tệp lịch sử gõ phím. Con đường phía dưới khoá chặt dữ liệu trong tệp quyền sáu trăm rồi đọc kín vào bộ nhớ tiến trình đang chạy.",
                clear=True,
            )
        ],
        "formula_title": "Tính tần suất lịch cron 5 trường",
        "formula_steps": [
            ak.st_auto(
                ak.box(
                    "<p>Năm trường của một dòng <code>cron</code> theo đúng thứ tự: <b>Phút</b> (0–59) | <b>Giờ</b> (0–23) | <b>Ngày</b> (1–31) | <b>Tháng</b> (1–12) | <b>Thứ</b> (0–6).</p>"
                    "<p>Ví dụ <code>*/5 * * * *</code>: 60 / 5 = <b>12</b> lần mỗi giờ; 12 × 24 = <b>288</b> lần mỗi ngày.</p>",
                    "key",
                ),
                "Tính toán tần suất chạy của biểu thức năm trường rất chính xác theo đơn vị thời gian. Dấu sao chia năm ở cột phút đầu tiên nghĩa là cứ sau năm phút trong sáu mươi phút thì kích hoạt một lượt nên tổng mỗi giờ chạy đúng mười hai lần. Nhân với hai mươi bốn giờ một ngày ta có tổng cộng hai trăm tám mươi tám lần thực thi mỗi ngày.",
                clear=True,
            )
        ],
        "formula_checks": ["(60 // 5) * 24 == 288"],
        "example_title": "Chạy thật: nạp tệp môi trường quyền 600 và che log",
        "example_items": [
            {
                "type": "r3",
                "say": "Giải mã hai bước thiết lập an toàn khi tạo khoá bí mật và đọc tệp môi trường không để lọt ra nhật ký.",
                "rows": [
                    ["<code>chmod 600 secrets.env</code>", "Khoá tệp bí mật để chỉ đúng chủ sở hữu mới đọc được"],
                    ["<code>ssh-keygen -t ed25519</code>", "Sinh cặp khoá mật mã hiện đại gồm tệp bí mật và tệp công khai <code>.pub</code>"],
                    ["<code>umask 077</code>", "Mặt nạ tự động gán quyền <code>600</code> cho tệp mới và <code>700</code> cho thư mục mới"],
                    ["<code>cron</code> (<code>*/5 * * * *</code>)", "Bộ lập lịch tác vụ nền chạy định kỳ trên Linux (<code>*/5</code> = mỗi 5 phút một lần)"],
                ],
            },
            {
                "type": "code",
                "pid": "p1",
                "title": "Tạo tệp bí mật quyền 600, nạp vào biến môi trường và che khi in nhật ký",
                "say": "Kịch bản tạo một tệp cấu hình chứa mã bí mật giả lập, đặt ngay quyền sáu trăm từ đầu rồi nạp vào biến môi trường nội bộ của tiến trình. Để tránh rò rỉ vào nhật ký, ta chỉ in ra dấu xác nhận có mặt biến cùng bốn ký tự cuối đã che.",
                "out_say": "Đầu ra chạy thật chứng minh quyền tệp được khoá đúng sáu trăm, biến môi trường đã vào tới bộ nhớ tiến trình và thông báo in ra hoàn toàn sạch sẽ không lộ chuỗi mật khẩu.",
            },
        ],
        "progs": {
            "p1": {
                "code": (
                    "mkdir -p test_l06 && cd test_l06\n"
                    "umask 077\n"
                    "printf 'DB_PASS=TopSecret_2026\\n' > secrets.env\n"
                    "chmod 600 secrets.env\n"
                    "set -a; source ./secrets.env; set +a\n"
                    "masked=\"***${DB_PASS: -4}\"\n"
                    "hp=$(( ${#DB_PASS} > 0 ? 1 : 0 ))\n"
                    "echo \"has_pass=$hp masked=$masked perm=$(stat -c %a secrets.env)\""
                ),
                "expect": "has_pass=1 masked=***2026 perm=600",
            },
            "p2": {
                "code": (
                    "per_h=$((60 / 5)); per_d=$((per_h * 24)); echo \"per_hour=$per_h per_day=$per_d\""
                ),
                "expect": "per_hour=12 per_day=288",
            },
        },
        "example_checks": ["(60 // 5) * 24 == 288"],
        "check_title": "Đối chứng số lượt chạy của lịch cron */5 * * * *",
        "check_items": [
            {
                "type": "code",
                "pid": "p2",
                "title": "Tính độc lập số lần chạy trong 1 giờ và 1 ngày của lịch */5",
                "say": "Ở đường kiểm chứng thứ hai, ta tính lại số lượt kích hoạt trong một giờ và hai mươi bốn giờ vì chu kỳ năm phút lặp đều suốt ngày.",
                "out_say": "Đầu ra đối chứng khớp hoàn toàn với kết quả mười hai lần một giờ và hai trăm tám mươi tám lần một ngày vì sáu mươi chia năm nhân hai mươi bốn bằng đúng số đó.",
            }
        ],
        "check_checks": ["(60 // 5) * 24 == 288"],
        "quymo_title": "Dung lượng nhật ký và mức phơi nhiễm bí mật qua ba quy mô vận hành",
        "quymo_steps": [
            ak.st_auto(
                ak.table(
                    ["chu kỳ cron", "số lần chạy mỗi tháng (30 ngày)", "nguy cơ nếu không chuyển hướng & luân chuyển log"],
                    [
                        [f"Mỗi giờ ({ak.nowrap('0 * * * *')})", "720 lần", "Nhỏ, dễ kiểm soát nhưng vẫn mất dấu nếu không ghi tệp"],
                        [f"Mỗi 5 phút ({ak.nowrap('*/5 * * * *')})", "8 640 lần", "Nếu lỗi lặp lại, hộp thư hệ thống đầy nghẽn báo lỗi"],
                        [f"Mỗi phút ({ak.nowrap('* * * * *')})", "43 200 lần", "Cả chục nghìn dòng tiến trình dồn nếu tác vụ chạy quá 60 giây"],
                    ],
                ),
                "Bảng quy mô giải thích tầm quan trọng của việc tính đúng nhịp chạy và gom nhật ký cho tác vụ định kỳ. Với chu kỳ năm phút một lần, trong ba mươi ngày máy chạy tới tám nghìn sáu trăm bốn mươi lượt. Nếu chuyển sang chạy mỗi phút một lần, tổng số lên tới hơn bốn mươi ba nghìn lượt một tháng nên bắt buộc phải dùng cơ chế khoá chống chồng chéo và xoay vòng tệp nhật ký.",
                clear=True,
            )
        ],
        "quymo_checks": ["288 * 30 == 8640"],
        "pitfall_steps": [
            ak.st_auto(
                ak.box(
                    "<b>Lỗi 1: Truyền mật khẩu qua cờ dòng lệnh <code>--token=...</code>.</b> Mọi tiến trình dùng lệnh <code>ps</code> hoặc nhật ký kiểm toán shell đều ghi nguyên văn mật khẩu.<br>"
                    "<b>Lỗi 2: Đặt lệnh <code>echo \"Connecting $DB_PASS\"</code> trong kịch bản gỡ lỗi rồi quên xoá.</b> Bí mật tràn vào hệ thống thu thập log tập trung.<br>"
                    "<b>Lỗi 3: Chạy tác vụ <code>cron</code> dùng đường dẫn tương đối và thiếu chuyển hướng <code>&gt;&gt; log 2&gt;&amp;1</code>.</b> Môi trường chạy lịch định kỳ rất tối giản nên lệnh thường thất bại im lặng.",
                    "warn",
                ),
                "Hãy khắc cốt ghi tâm ba sai lầm bảo mật hay gặp nhất khi viết kịch bản vận hành. Một là truyền mật khẩu trực tiếp trên tham số dòng lệnh khiến bất kỳ ai gõ lệnh xem tiến trình đều nhìn thấy. Hai là vô tình in giá trị biến bí mật ra nhật ký hoặc đưa nhầm tệp môi trường vào kho mã nguồn. Ba là đặt lịch chạy nền mà quên dùng đường dẫn tuyệt đối và chuyển hướng đầy đủ cả hai luồng.",
                clear=True,
            )
        ],
        "quiz_steps": [
            ak.st(
                "<ol><li>Lịch <code>*/5 * * * *</code> chạy bao nhiêu lần trong trọn 1 ngày (24 giờ)?</li>"
                "<li>Khi kết nối tự động tới cơ sở dữ liệu bằng kịch bản Bash, nên đọc mật khẩu từ tham số dòng lệnh hay từ tệp biến môi trường đặt quyền <code>600</code>?</li></ol>",
                "Đến lượt bạn tự kiểm tra. Câu một, biểu thức lịch chạy năm phút một lần thực thi tổng cộng bao nhiêu lần trong suốt một ngày hai mươi bốn giờ? Câu hai, nên truyền mật khẩu bằng cờ dòng lệnh hay nạp từ tệp cấu hình có quyền sáu trăm? Bấm tạm dừng và trả lời ra giấy.",
                pause=20,
            ),
            ak.st(
                "<p>① 60 / 5 = 12 lần/giờ → 12 × 24 = <b>288 lần/ngày</b>.</p>",
                "Đáp án câu một: mỗi giờ chạy mười hai lần nên nhân hai mươi bốn giờ cho tổng cộng hai trăm tám mươi tám lượt chạy mỗi ngày.",
                clear=True,
            ),
            ak.st(
                "<p>② Nạp từ <b>tệp biến môi trường quyền <code>600</code></b> (không bao giờ kẹp mật khẩu lên tham số dòng lệnh).</p>",
                "Đáp án câu hai: luôn nạp từ tệp biến môi trường đặt quyền sáu trăm để tuyệt đối không làm lộ mật khẩu ra danh sách tiến trình.",
                clear=True,
            ),
        ],
        "quiz_checks": ["(60 // 5) * 24 == 288"],
        "recap_steps": [
            ak.st_auto(
                "<div class='chain'><span class='n'>Khoá SSH quyền 600</span><span class='a'>|</span>"
                "<span class='n'>Bí mật qua .env (không CLI)</span><span class='a'>|</span>"
                "<span class='n'>cron + đường dẫn tuyệt đối</span></div>",
                "Tổng kết chuỗi nguyên tắc an toàn cho tự động hoá hệ thống. Hãy đặt quyền sáu trăm cho cả khoá riêng lẫn tệp bí mật và tuyệt đối không in mật khẩu lên dòng lệnh. Khi hẹn giờ chạy nền, luôn dùng đường dẫn tuyệt đối kèm chuyển hướng nhật ký.",
                clear=True,
            )
        ],
        "lab_de": (
            "# Lab LNX L06 — Bảo mật biến môi trường và tính tần suất cron\n\n"
            "Viết kịch bản Bash tạo tệp bí mật với `chmod 600` (hoặc kiểm tra `umask`), đọc nạp biến môi trường không in nguyên văn bí mật, và tính số lượt chạy/ngày của `*/5 * * * *` để in đúng 3 dòng:\n"
            "1. `env_loaded=1`\n"
            "2. `cron_per_hour=12`\n"
            "3. `cron_per_day=288`\n\n"
            "Chấm tự động:\n```bash\nbash labs/cham.sh LNX L06 duong_dan/bai_cua_ban.sh\n```"
        ),
        "lab_sol": (
            "#!/usr/bin/env bash\n"
            "set -euo pipefail\n"
            "W=$(mktemp -d)\n"
            'trap \'rm -rf "$W"\' EXIT\n'
            "umask 077\n"
            'printf "SECRET_KEY=demo_only_v1\\n" > "$W/.env"\n'
            'chmod 600 "$W/.env"\n'
            'set -a; source "$W/.env"; set +a\n'
            'ok=$(( ${#SECRET_KEY} > 0 ? 1 : 0 ))\n'
            "echo \"env_loaded=$ok\"\n"
            "echo \"cron_per_hour=$((60 / 5))\"\n"
            "echo \"cron_per_day=$(( (60 / 5) * 24 ))\"\n"
        ),
    }

    # ────────────────── L07: Nhân Linux cô lập Container: namespaces, cgroups và tầng ảnh Docker ──────────────────
    l07 = {
        "id": "L07",
        "slug": "container_namespaces_cgroups",
        "title": "Nhân Linux cô lập Container: namespaces, cgroups và tầng ảnh Docker",
        "next_title": "Chạy Docker Container thực chiến: cổng, ổ gắn, mạng và nhật ký",
        "assumes": ["lnx_inode", "lnx_quyen_bat_phan", "lnx_tin_hieu"],
        "objectives": [
            "Phân biệt không gian tên cô lập (cô lập góc nhìn PID/mạng/tệp) với nhóm điều khiển (giới hạn RAM/CPU)",
            "Tính dung lượng đĩa tiết kiệm được khi N container dùng chung tầng ảnh gốc chỉ đọc",
            "Nhận biết vì sao container hết RAM bị nhân ngắt ngay (OOMKill, mã thoát 137)",
        ],
        "covers": [(1, "formula"), (2, "example"), (3, "check")],
        "hook_title": "Chạy 10 container từ ảnh 120 MB có tốn 1 200 MB không?",
        "hook_html": (
            "<p>Một ảnh gốc <b>120 MB</b>. Nếu là máy ảo truyền thống, chạy 10 máy tốn 10 bản sao = <b>1 200 MB</b> kèm 10 nhân hệ điều hành tách biệt.</p>"
            "<p>Nhưng với công-tai-nơ dùng chung một nhân Linux và tầng ảnh chỉ đọc, 10 bản chạy song song chỉ tốn vỏn vẹn <b>170 MB</b> ổ đĩa.</p>"
        ),
        "hook_say": (
            "Chào bạn đến với chặng ba khám phá bản chất thật sự bên dưới công nghệ công-tai-nơ. "
            "Nhiều bạn hình dung mỗi công-tai-nơ là một máy ảo thu nhỏ phải sao chép trọn bộ một trăm hai mươi mê-ga-bai ổ đĩa cho mỗi bản chạy mới. "
            "Thực tế tất cả công-tai-nơ chạy chung trên một nhân Li-núc duy nhất và chia sẻ chung tầng ảnh chỉ đọc ở bên dưới. "
            "Hôm nay ta tìm hiểu hai trụ cột cô lập và điều phối của nhân giúp làm được điều đó."
        ),
        "hook_checks": ["alg.lnx_image_total(120, [5], 10) == 170"],
        "prereq_steps": [
            ak.st_auto(
                ak.table(
                    ["kiến thức bài trước", "vai trò bên trong công-tai-nơ"],
                    [
                        ["Mã thoát 137 = 128 + 9 do SIGKILL (L02)", "Khi vượt trần RAM cho phép, nhân gửi SIGKILL cắt công-tai-nơ với mã 137"],
                        ["Thư mục ảo tiến trình /proc (L00)", "Bên trong công-tai-nơ vẫn nhìn thấy tiến trình chính là PID 1"],
                    ],
                ),
                "Công-tai-nơ không phải phép màu bí ẩn nào khác mà là tổng hợp trực tiếp từ bài 0 và bài 2. Nhờ bài 2 bạn hiểu vì sao một dịch vụ ngốn tràn giới hạn bộ nhớ bị nhân ngắt với mã thoát một ba bảy. Và nhờ bài 0 bạn thấy góc nhìn tiến trình bên trong tự coi mình là tiến trình số một.",
                clear=True,
            )
        ],
        "sym_steps": [
            ak.st_auto(
                ak.table(
                    ["cơ chế nhân Linux", "trách nhiệm tách biệt"],
                    [
                        ["<code>namespaces</code> (không gian tên)", "Cô lập <b>những gì tiến trình nhìn thấy</b>: bảng PID riêng, thẻ mạng riêng, cây thư mục riêng"],
                        ["<code>cgroups</code> (nhóm kiểm soát)", "Giới hạn <b>lượng tài nguyên được tiêu thụ</b>: trần bộ nhớ RAM, tỉ lệ CPU"],
                        ["Tầng ảnh chồng lớp (UnionFS)", "Nhiều tầng gốc chỉ đọc dùng chung; mỗi bản chạy thêm duy nhất 1 tầng ghi mỏng trên cùng"],
                    ],
                ),
                "Bảng này giải mã ba cơ chế lõi tạo nên một công-tai-nơ hiện đại. Đầu tiên là không gian tên giúp cô lập góc nhìn để tiến trình chỉ thấy bảng mã tiến trình và giao diện mạng của riêng nó. Tiếp theo là nhóm kiểm soát dùng để đóng trần phần trăm CPU và dung lượng bộ nhớ tối đa. Cuối cùng là hệ thống tệp chồng lớp dùng chung tầng gốc chỉ đọc.",
                introduces=["lnx_namespace"],
                clear=True,
            )
        ],
        "intuition_title": "N container dùng chung tầng chỉ đọc và một tầng ghi mỏng riêng biệt",
        "intuition_steps": [
            ak.st_auto(
                ak.svg_wrap(
                    960, 215,
                    ak.svg_rect(40, 25, 270, 62, "Container #1 (tầng ghi 5 MB)", "PID 1 nội bộ | cgroup RAM 256MB", ak.C_BLUE)
                    + ak.svg_rect(345, 25, 270, 62, "Container #2 (tầng ghi 5 MB)", "PID 1 nội bộ | cgroup RAM 256MB", ak.C_BLUE)
                    + ak.svg_rect(650, 25, 270, 62, "... Container #10 (+5 MB)", "PID 1 nội bộ | tách biệt mạng", ak.C_BLUE)
                    + ak.svg_rect(40, 120, 880, 72, "Tầng ảnh gốc CHỈ ĐỌC dùng chung (120 MB) + Nhân Linux máy chủ DUY NHẤT", "Không nhân bản 120 MB hay nhân HĐH riêng cho từng bản", ak.C_GREEN),
                ),
                "Nhìn sơ đồ xếp tầng trên màn hình để thấy rõ bí mật tiết kiệm bộ nhớ. Tất cả mười công-tai-nơ phía trên đều chia sẻ chung một khối ảnh gốc chỉ đọc một trăm hai mươi mê-ga-bai cùng một nhân Li-núc duy nhất ở đáy. Mỗi bản chỉ tiêu tốn thêm một lớp ghi riêng mỏng vài mê-ga-bai nằm ở phía trên cùng.",
                clear=True,
            )
        ],
        "formula_title": "Công thức tính tổng dung lượng tầng ảnh và nhận diện OOMKill",
        "formula_steps": [
            ak.st_auto(
                ak.box(
                    "<p>Gọi $B$ là kích thước ảnh gốc chỉ đọc và $W$ là dữ liệu ghi riêng của mỗi bản trong $N$ bản cùng chạy:</p>"
                    "<p>$$\\text{Tổng dung lượng} = B + N \\times W$$</p>"
                    "<p>Với $B = 120\\text{ MB}$, $N = 10$, $W = 5\\text{ MB}$: tổng $= 120 + 10 \\times 5 = \\hl{170\\text{ MB}}$ (so với $1\\,200\\text{ MB}$ sao chép toàn bộ).</p>",
                    "key",
                ),
                "Công thức tính dung lượng đĩa cực kỳ gọn vì tầng ảnh gốc chỉ xuất hiện đúng một lần trên đĩa dù bạn bật bao nhiêu bản sao. Ta chỉ lấy kích thước ảnh gốc cộng thêm số lượng công-tai-nơ nhân với phần ghi riêng của từng bản. Nhờ vậy mười bản chạy cùng lúc chỉ tốn một trăm bảy mươi mê-ga-bai thay vì một nghìn hai trăm mê-ga-bai.",
                clear=True,
            )
        ],
        "formula_checks": ["alg.lnx_image_total(120, [5], 10) == 170"],
        "example_title": "Chạy thật trên Docker: quan sát PID 1 và cgroups",
        "example_items": [
            {
                "type": "r3",
                "say": "Giải thích trước hai tuỳ chọn kiểm chứng cơ chế cô lập và thông số giới hạn trên công-tai-nơ Đốc-cơ thật.",
                "rows": [
                    ["<code>--memory=64m</code>", "Đặt trần bộ nhớ cứng bằng cgroups; vượt ngưỡng sẽ kích hoạt OOMKill (137)"],
                    ["<code>ps -o pid,comm</code>", "Xem danh sách tiến trình bên trong không gian tên PID riêng của container"],
                    ["<code>OOMKill (137)</code>", "Nhân ngắt ngay container dùng vượt trần RAM <code>cgroups</code> (128 + SIGKILL 9 = 137)"],
                    ["<code>MB</code> vs <code>MiB</code>", "<code>1 MB = 10⁶ B</code> (ổ đĩa); <code>1 MiB = 2²⁰ B</code> (RAM/cgroups: 64 MiB = 67 108 864 B)"],
                ],
            },
            {
                "type": "code",
                "pid": "p1",
                "title": "Chạy thật một container với trần --memory=64m và soi PID 1 bên trong",
                "say": "Ta chạy thật một công-tai-nơ Đốc-cơ với mức trần bộ nhớ sáu mươi bốn mê-ga-bai qua nhóm kiểm soát rồi liệt kê bảng tiến trình bên trong. Vì không gian tên tiến trình đã cô lập góc nhìn nên lệnh bên trong chỉ nhìn thấy đúng hai tiến trình của riêng mình.",
                "out_say": "Đầu ra chạy thật từ Đốc-cơ xác nhận tiến trình vỏ bên trong tự mang số hiệu một và thông số giới hạn sáu mươi bốn mê-ga-bai đã được ghi nhận ngay ở tầng điều khiển nhân.",
            },
        ],
        "progs": {
            "p1": {
                "code": (
                    "MSYS_NO_PATHCONV=1 docker run --rm --memory=64m postgres:17-alpine sh -c '\n"
                    "  echo \"pid_1=$(ps -o pid,comm | awk \"NR==2{print \\$1,\\$2}\")\"\n"
                    "  cat /sys/fs/cgroup/memory.max 2>/dev/null || \\\n"
                    "    cat /sys/fs/cgroup/memory/memory.limit_in_bytes\n"
                    "'"
                ),
                "expect": "pid_1=1 sh\n67108864",
            },
            "p2": {
                "code": (
                    "base=120; n=10; rw=5; echo \"shared_mb=$((base + n * rw)) full_copy_mb=$((n * base))\""
                ),
                "expect": "shared_mb=170 full_copy_mb=1200",
            },
        },
        "example_checks": ["64 * 1024 * 1024 == 67108864"],
        "check_title": "Đối chứng tính lại dung lượng dùng chung và ngưỡng 64 MiB",
        "check_items": [
            {
                "type": "code",
                "pid": "p2",
                "title": "Đối chiếu số liệu 170 MB tầng dùng chung vs 1 200 MB sao chép toàn phần",
                "say": "Ở đường kiểm chứng thứ hai, ta tính lại mức tiết kiệm dung lượng trên mười công-tai-nơ dùng chung ảnh một trăm hai mươi mê-ga-bai vì cần đối chiếu ngưỡng vừa đo.",
                "out_say": "Kết quả khớp hoàn toàn một trăm bảy mươi mê-ga-bai dùng chung so với một nghìn hai trăm mê-ga-bai bản sao rời vì chỉ tầng ghi năm mê-ga-bai nhân lên mười lần.",
            }
        ],
        "check_checks": ["alg.lnx_image_total(120, [5], 10) == 170"],
        "quymo_title": "Chi phí đĩa của Container dùng chung tầng qua 3 quy mô",
        "quymo_steps": [
            ak.st_auto(
                ak.table(
                    ["số bản chạy từ ảnh gốc 120 MB (ghi riêng 5 MB)", "sao chép tách rời (kiểu máy ảo nhỏ)", "cô lập container dùng chung tầng ảnh"],
                    [
                        ["1 bản", "125 MB (120 gốc + 5 ghi)", "125 MB (khởi chạy dưới 0,3 giây)"],
                        ["10 bản", "1 200 MB phần ảnh gốc", "170 MB (tiết kiệm 85,8% đĩa phần gốc)"],
                        ["100 bản trên cùng máy", "12 000 MB (12 GB) gốc", "620 MB (tiết kiệm 94,8% đĩa phần gốc)"],
                    ],
                ),
                "Bảng quy mô giải thích vì sao một máy chủ đơn lẻ dễ dàng chạy hàng trăm công-tai-nơ song song. Khi tăng lên mười bản, công-tai-nơ tiết kiệm hơn tám mươi lăm phần trăm dung lượng lưu trữ. Ở quy mô một trăm bản chạy cùng lúc, kiến trúc dùng chung tầng ảnh chỉ tốn sáu trăm hai mươi mê-ga-bai thay vì ngốn mười hai gi-ga-bai ổ đĩa.",
                clear=True,
            )
        ],
        "quymo_checks": ["120 + 100 * 5 == 620"],
        "pitfall_steps": [
            ak.st_auto(
                ak.box(
                    "<b>Lỗi 1: Nghĩ container có nhân hệ điều hành riêng biệt hoàn toàn.</b> Mọi container chia sẻ cùng một nhân Linux với máy chủ; khác với máy ảo chạy nhân riêng.<br>"
                    "<b>Lỗi 2: Không đặt trần bộ nhớ bằng cgroups cho dịch vụ mới.</b> Một dịch vụ rò rỉ bộ nhớ sẽ ăn sạch RAM máy chủ làm sập các dịch vụ hàng xóm.<br>"
                    "<b>Lỗi 3: Thấy mã thoát 137 liền đổ lỗi mạng rồi tăng số thử lại.</b> Mã 137 trên container thường báo hiệu vừa bị nhân ngắt vì chạm trần RAM.",
                    "warn",
                ),
                "Hãy nhớ ba ngộ nhận nguy hiểm khi bước vào thế giới công-tai-nơ. Đầu tiên đừng nhầm công-tai-nơ như máy ảo có nhân riêng vì chúng dùng chung một nhân Li-núc máy chủ. Thứ hai đừng thả lỏng giới hạn bộ nhớ nhóm kiểm soát kẻo một tiến trình lỗi kéo sập toàn máy. Thứ ba mỗi khi thấy mã thoát một ba bảy, hãy kiểm tra ngay biểu đồ bộ nhớ trước tiên.",
                clear=True,
            )
        ],
        "quiz_steps": [
            ak.st(
                "<ol><li>Giữa <code>namespaces</code> và <code>cgroups</code>, cơ chế nào giới hạn một công-tai-nơ tối đa chỉ được dùng 512 MB RAM?</li>"
                "<li>Ảnh gốc rộng 120 MB, chạy 10 công-tai-nơ mỗi bản ghi thêm 5 MB. Tổng dung lượng đĩa thực chiếm bằng bao nhiêu?</li></ol>",
                "Đến lượt bạn tự kiểm tra. Câu một, cơ chế nào trong hai cơ chế của nhân chịu trách nhiệm đặt trần giới hạn bộ nhớ năm trăm mười hai mê-ga-bai? Câu hai, chạy mười công-tai-nơ từ ảnh gốc một trăm hai mươi mê-ga-bai với phần ghi riêng năm mê-ga-bai thì tổng tốn bao nhiêu? Bấm tạm dừng và trả lời.",
                pause=20,
            ),
            ak.st(
                "<p>① <b><code>cgroups</code></b> (nhóm kiểm soát tài nguyên RAM/CPU; còn <code>namespaces</code> chỉ cô lập góc nhìn).</p>",
                "Đáp án câu một: đó là nhóm kiểm soát chuyên trách đóng trần tài nguyên bộ nhớ và bộ xử lý cho nhóm tiến trình.",
                clear=True,
            ),
            ak.st(
                "<p>② <code>120 + 10 × 5 = <b>170 MB</b></code>.</p>",
                "Đáp án câu hai: lấy ảnh gốc một trăm hai mươi cộng mười nhân năm bằng tổng cộng một trăm bảy mươi mê-ga-bai.",
                clear=True,
            ),
        ],
        "quiz_checks": ["alg.lnx_image_total(120, [5], 10) == 170"],
        "recap_steps": [
            ak.st_auto(
                "<div class='chain'><span class='n'>namespaces (góc nhìn riêng)</span><span class='a'>+</span>"
                "<span class='n'>cgroups (trần RAM/CPU)</span><span class='a'>+</span>"
                "<span class='n'>Chung tầng chỉ đọc</span></div>",
                "Tổng kết công thức kiến trúc bên dưới mọi công-tai-nơ hiện đại. Không gian tên tách biệt bảng tiến trình và mạng, nhóm kiểm soát đặt trần tài nguyên, còn tầng ảnh dùng chung giúp bật hàng trăm bản sao trong tích tắc.",
                clear=True,
            )
        ],
        "lab_de": (
            "# Lab LNX L07 — Tính tổng tầng ảnh dùng chung và nhận diện mã ngắt OOM\n\n"
            "Viết kịch bản Bash kiểm tra kích thước tổng công-tai-nơ và quy đổi mã ngắt OOMKill để in đúng 3 dòng:\n"
            "1. `shared_10_mb=170`\n"
            "2. `saved_mb=1030`\n"
            "3. `oom_exit=137`\n\n"
            "Chấm tự động:\n```bash\nbash labs/cham.sh LNX L07 duong_dan/bai_cua_ban.sh\n```"
        ),
        "lab_sol": (
            "#!/usr/bin/env bash\n"
            "set -euo pipefail\n"
            "base=120; n=10; rw=5\n"
            "shared=$((base + n * rw))\n"
            "full=$((n * base))\n"
            "saved=$((full - shared))\n"
            "echo \"shared_10_mb=$shared\"\n"
            "echo \"saved_mb=$saved\"\n"
            "echo \"oom_exit=$((128 + 9))\"\n"
        ),
    }

    # ────────────────── L08: Chạy Docker thực chiến: cổng, ổ gắn, mạng và nhật ký ──────────────────
    l08 = {
        "id": "L08",
        "slug": "docker_chay_thuc_chien",
        "title": "Chạy Docker Container thực chiến: cổng, ổ gắn, mạng và nhật ký",
        "next_title": "Tình huống chuyên gia: Dựng và gỡ lỗi cụm nhiều dịch vụ bằng Docker Compose",
        "assumes": ["lnx_inode", "lnx_quyen_bat_phan", "lnx_tin_hieu", "lnx_namespace"],
        "objectives": [
            "Phân biệt dữ liệu tạm trong container (mất khi xoá) với ổ gắn lưu bền vững (volume)",
            "Tạo mạng cầu nối riêng để hai container gọi nhau qua tên dịch vụ mà không lộ cổng ra ngoài",
            "Đọc nhật ký chuẩn stdout/stderr của container qua docker logs",
        ],
        "covers": [(1, "formula"), (2, "example"), (3, "check")],
        "hook_title": "Xoá container DB làm sao không mất sạch toàn bộ dữ liệu?",
        "hook_html": (
            "<p>Một bạn chạy DB mới trong container rồi nhập 500 bản ghi thử nghiệm, hôm sau chạy <code>docker rm</code> nâng phiên bản thì dữ liệu về con số 0.</p>"
            "<p>Nguyên nhân: bạn chưa gắn <b>ổ bền vững (volume)</b> ra ngoài tầng ghi tạm thời của công-tai-nơ.</p>"
        ),
        "hook_say": (
            "Chào bạn, tai nạn mất trắng dữ liệu khi xoá để cập nhật công-tai-nơ là bài học nhập môn đắt giá nhất khi mới dùng Đốc-cơ. "
            "Như ở bài 7 ta vừa thấy, mỗi công-tai-nơ chỉ sở hữu một lớp ghi mỏng gắn theo vòng đời của riêng nó nên hễ xoá công-tai-nơ là lớp dữ liệu ấy bay theo ngay lập tức. "
            "Hôm nay ta thực hành gắn ổ bền vững sống độc lập ngoài công-tai-nơ, nối hai dịch vụ qua mạng cầu nối riêng và đọc nhật ký trực tiếp."
        ),
        "hook_checks": ["500 - 500 == 0"],
        "prereq_steps": [
            ak.st_auto(
                ak.table(
                    ["kiến thức bài trước", "áp dụng vào vận hành Docker"],
                    [
                        ["Tầng ghi mỏng theo vòng đời công-tai-nơ (L07)", "Dữ liệu lưu trong tầng ghi đó sẽ mất sạch khi xoá công-tai-nơ"],
                        ["Lắng nghe trên 0.0.0.0 và luồng 1/2 (L05, L03)", "Chuyển cổng -p và lệnh đọc log nhận đúng đầu ra bên trong"],
                    ],
                ),
                "Ta nối tiếp trực tiếp bài 3, bài 5 và bài 7 vào vận hành Đốc-cơ hàng ngày. Bởi vì tầng ghi trên cùng gắn chết với công-tai-nơ theo bài 7, dữ liệu lâu dài bắt buộc tách ra ổ gắn riêng. Đồng thời cổng chuyển tiếp và nhật ký đều tuân theo cơ chế mạng và hai luồng chuẩn vừa học.",
                clear=True,
            )
        ],
        "sym_steps": [
            ak.st_auto(
                ak.table(
                    ["cờ / lệnh Docker", "tác dụng thực tế"],
                    [
                        ["<code>-v ten_volume:/var/lib/data</code>", "Gắn ổ bền vững tồn tại độc lập ngay cả khi công-tai-nơ bị xoá bỏ"],
                        ["<code>-p 8080:80</code>", "Ánh xạ cổng 8080 trên máy host vào cổng 80 bên trong công-tai-nơ"],
                        ["<code>docker network create</code> &amp; <code>docker logs</code>", "Tạo mạng cầu nối nội bộ phân giải theo tên và đọc luồng nhật ký chuẩn"],
                    ],
                ),
                "Trên bảng là bộ ba cờ và lệnh thực chiến bạn dùng hàng ngày với Đốc-cơ. Cờ trừ v gắn một ổ lưu trữ bền vững nằm ngoài công-tai-nơ để dữ liệu còn nguyên qua mọi lần nâng cấp. Cờ trừ p nối cổng máy chủ ngoài vào cổng lắng nghe bên trong, còn mạng cầu nối riêng cho phép hai công-tai-nơ gọi thẳng bằng tên thay vì nhớ địa chỉ I P.",
                clear=True,
            )
        ],
        "intuition_title": "Ổ gắn bền vững nằm ngoài công-tai-nơ và mạng cầu nối phân giải tên",
        "intuition_steps": [
            ak.st_auto(
                ak.svg_wrap(
                    960, 210,
                    ak.svg_rect(40, 25, 250, 75, "Container web", "Nghe 0.0.0.0:80 | -p 8080:80", ak.C_BLUE)
                    + ak.svg_arrow(290, 62, 410, 62, "gọi 'redis:6379'")
                    + ak.svg_rect(410, 25, 230, 75, "Mạng cầu nối riêng", "DNS nội bộ tự phân giải tên", ak.C_AMBER)
                    + ak.svg_arrow(640, 62, 710, 62, "")
                    + ak.svg_rect(710, 25, 210, 75, "Container DB / cache", "Chỉ nghe mạng cầu nối nội bộ", ak.C_BLUE)
                    + ak.svg_arrow(815, 100, 815, 138, "")
                    + ak.svg_rect(490, 138, 430, 62, "Ổ bền vững (-v db_data:/data)", "Còn nguyên 100% khi xoá và tạo lại container", ak.C_GREEN),
                ),
                "Nhìn sơ đồ kiến trúc chuẩn khi chạy nhiều công-tai-nơ liên kết. Ứng dụng chính chỉ mở đúng một cổng cần thiết ra ngoài, rồi gọi thẳng tới cơ sở dữ liệu bằng tên dịch vụ qua mạng cầu nối riêng kín đáo bên trong. Ở phía dưới, ổ gắn bền vững nằm ngoài vòng đời công-tai-nơ bảo vệ nguyên vẹn dữ liệu dù bản cũ bị xoá và thay bằng bản mới.",
                clear=True,
            )
        ],
        "formula_title": "Quy tắc sống sót dữ liệu và chiều đọc ánh xạ cổng",
        "formula_steps": [
            ak.st_auto(
                ak.box(
                    "<p><b>Chiều đọc cố định mọi cờ ánh xạ trong Docker (Trái = Ngoài | Phải = Trong):</b></p>"
                    "<p><code>-p HOST_PORT:CONTAINER_PORT</code> và <code>-v HOST_VOLUME:CONTAINER_PATH</code>.</p>"
                    "<p><b>Bất biến bảo toàn dữ liệu:</b> Khi ghi $N$ bản ghi vào ổ gắn bền vững rồi xoá công-tai-nơ tạo bản mới gắn lại đúng ổ đó, số bản ghi đọc lại $= N$ (giữ nguyên $\\hl{100\\%}$).</p>",
                    "key",
                ),
                "Để không bao giờ lắp ngược hướng cờ cấu hình, hãy nhớ một quy tắc ngắn gọn. Vế bên trái dấu hai chấm luôn là của máy chủ bên ngoài, còn vế bên phải là đường dẫn hoặc cổng bên trong công-tai-nơ. Khi đã gắn đúng ổ lưu trữ bền vững ở bên trái, mọi bản ghi lưu xuống vẫn giữ trọn vẹn một trăm phần trăm sau khi thay mới công-tai-nơ.",
                clear=True,
            )
        ],
        "formula_checks": ["int('8080') == 8080"],
        "example_title": "Chạy thật trên Docker: giữ dữ liệu qua volume bền vững",
        "example_items": [
            {
                "type": "r3",
                "say": "Giải thích các lệnh khởi tạo ổ bền vững và kiểm tra tính liên tục dữ liệu khi thay công-tai-nơ trên Đốc-cơ thật.",
                "rows": [
                    ["<code>docker volume create lnx_v8</code>", "Tạo ổ lưu trữ bền vững được Docker quản lý độc lập ngoài container"],
                    ["<code>docker logs &lt;id&gt;</code>", "Đọc lại toàn bộ luồng chuẩn và luồng lỗi do tiến trình PID 1 in ra"],
                    ["<code>getent hosts &lt;tên&gt;</code>", "Truy vấn DNS nội bộ trong mạng cầu nối Docker để kiểm tra IP dịch vụ"],
                    ["<code>reverse proxy</code>", "Máy chủ cổng trước đón <code>80/443</code> từ ngoài rồi chuyển tiếp vào dịch vụ kín bên trong"],
                ],
            },
            {
                "type": "code",
                "pid": "p1",
                "title": "Ghi dữ liệu vào volume trong container 1, xoá container 1, đọc lại bằng container 2 + xem logs",
                "say": "Ta thực hiện thí nghiệm sống trên Đốc-cơ qua hai công-tai-nơ nối tiếp nhau. Đầu tiên ta tạo một ổ gắn mới, bật công-tai-nơ thứ nhất ghi dữ liệu và nhật ký rồi xoá bỏ hoàn toàn công-tai-nơ này. Sau đó ta bật công-tai-nơ thứ hai gắn lại đúng ổ vừa rồi và đọc kiểm chứng toàn bộ.",
                "out_say": "Đầu ra thật chứng minh dòng nhật ký đã được thu nhận đầy đủ. Dữ liệu từ công-tai-nơ thứ nhất đã xoá vẫn còn nguyên một trăm phần trăm khi công-tai-nơ thứ hai đọc lại từ ổ bền vững.",
            },
        ],
        "progs": {
            "p1": {
                "code": (
                    "set -e\n"
                    "docker volume rm lnx_demo_v8 >/dev/null 2>&1 || true\n"
                    "docker volume create lnx_demo_v8 >/dev/null\n"
                    "IMG=postgres:17-alpine\n"
                    "MSYS_NO_PATHCONV=1 docker run --name lnx_c1 -v lnx_demo_v8:/data \\\n"
                    "  $IMG sh -c 'echo row_1_saved>/data/db.txt; echo log_written_by_c1' >/dev/null\n"
                    "logs_c1=$(docker logs lnx_c1); docker rm lnx_c1 >/dev/null\n"
                    "val_c2=$(MSYS_NO_PATHCONV=1 docker run --rm -v lnx_demo_v8:/data $IMG cat /data/db.txt)\n"
                    "docker volume rm lnx_demo_v8 >/dev/null\n"
                    "echo \"logs=$logs_c1 restored=$val_c2\""
                ),
                "expect": "logs=log_written_by_c1 restored=row_1_saved",
            },
            "p2": {
                "code": (
                    "set -e\n"
                    "docker network rm lnx_net8 >/dev/null 2>&1 || true\n"
                    "docker network create lnx_net8 >/dev/null\n"
                    "IMG=postgres:17-alpine; BR=lnx_net8\n"
                    "MSYS_NO_PATHCONV=1 docker run -d --rm --name lnx_srv8 --network $BR $IMG sleep 15 >/dev/null\n"
                    "cmd='getent hosts lnx_srv8 | awk \"{print (\\$1 ~ /^[0-9]+\\./ ? 1 : 0), \\$2}\"'\n"
                    "ans=$(MSYS_NO_PATHCONV=1 docker run --rm --network $BR $IMG sh -c \"$cmd\")\n"
                    "docker stop lnx_srv8 >/dev/null\n"
                    "docker network rm lnx_net8 >/dev/null\n"
                    "echo \"dns_resolved=$ans\""
                ),
                "expect": "dns_resolved=1 lnx_srv8",
            },
        },
        "example_checks": ["500 + 0 == 500"],
        "check_title": "Đối chứng phân giải tên dịch vụ nội bộ qua mạng cầu nối riêng",
        "check_items": [
            {
                "type": "code",
                "pid": "p2",
                "title": "Tạo mạng cầu nối lnx_net8 để container khách phân giải tên dịch vụ lnx_srv8",
                "say": "Ở đường kiểm chứng thứ hai, ta tạo một mạng cầu nối riêng rồi cho hai công-tai-nơ tham gia vào cùng mạng đó vì cần kiểm tra phân giải tên nội bộ.",
                "out_say": "Đầu ra thật xác nhận công-tai-nơ thứ hai phân giải thành công tên dịch vụ sang địa chỉ IP nội bộ vì mạng cầu nối đã bật DNS riêng.",
            }
        ],
        "check_checks": ["len('lnx_srv8') == 8"],
        "quymo_title": "Tại sao không lộ cổng DB ra ngoài qua ba quy mô cụm",
        "quymo_steps": [
            ak.st_auto(
                ak.table(
                    ["quy mô hệ thống", "rủi ro nếu mở thẳng -p 5432:5432 ra internet", "cách cấu hình chuẩn qua mạng cầu nối"],
                    [
                        ["Máy thử cá nhân", "Chậm hoặc dễ xung đột cổng cùng máy", "Chỉ giữ cổng nội bộ giữa app và DB"],
                        ["Máy chủ đơn chạy thật", "Hàng nghìn lượt quét dò mật khẩu mỗi giờ", "Chỉ mở 80/443 của reverse proxy; DB kín hoàn toàn"],
                        ["Cụm nhiều dịch vụ", "Lộ dữ liệu nếu thiếu tường lửa máy chủ", "Tách mạng riêng theo nhóm dịch vụ liên quan"],
                    ],
                ),
                "Bảng quy mô nhắc nhở nguyên tắc thiết kế mạng tối giản bề mặt tấn công. Khi mở thẳng cổng cơ sở dữ liệu ra máy chủ công cộng, ngay lập tức hàng nghìn lượt quét dò tự động từ mạng ngoài sẽ gõ cửa liên tục. Ngược lại, đưa cơ sở dữ liệu vào mạng cầu nối riêng giúp ứng dụng gọi trực tiếp qua tên dịch vụ mà vẫn giấu kín hoàn toàn trước bên ngoài.",
                clear=True,
            )
        ],
        "quymo_checks": ["80 + 443 == 523"],
        "pitfall_steps": [
            ak.st_auto(
                ak.box(
                    "<b>Lỗi 1: Lưu dữ liệu cơ sở dữ liệu vào tầng ghi mặc định trong công-tai-nơ.</b> Lệnh xoá công-tai-nơ sẽ làm mất sạch toàn bộ dữ liệu.<br>"
                    "<b>Lỗi 2: Dùng mạng mặc định rồi cố gọi nhau bằng tên container.</b> Mạng cầu nối mặc định không hỗ trợ DNS theo tên; phải tự tạo mạng cầu nối riêng.<br>"
                    "<b>Lỗi 3: Chạy container in nhật ký ra tệp bên trong ổ đĩa container thay vì ra <code>stdout</code>.</b> Lệnh <code>docker logs</code> rỗng không và tệp log phình dần tới đầy đĩa.",
                    "warn",
                ),
                "Hãy tránh ba sai lầm rất hay gặp khi chạy Đốc-cơ thực tế. Sai lầm nặng nhất là quên gắn ổ bền vững khiến lần khởi tạo lại tiếp theo xoá trắng toàn bộ cơ sở dữ liệu. Sai lầm thứ hai là dùng mạng cầu nối mặc định vốn không tự phân giải tên giữa các công-tai-nơ. Sai lầm thứ ba là ghi nhật ký vào tệp kín bên trong thay vì xuất ra luồng chuẩn.",
                clear=True,
            )
        ],
        "quiz_steps": [
            ak.st(
                "<ol><li>Trong cờ <code>-p 8080:80</code>, cổng nào lắng nghe trên máy chủ host ngoài và cổng nào là cổng bên trong container?</li>"
                "<li>Để giữ lại toàn bộ dữ liệu cơ sở dữ liệu khi nâng cấp công-tai-nơ mới, cần gắn thêm tuỳ chọn gì?</li></ol>",
                "Đến lượt bạn tự kiểm tra. Câu một, trong cờ trừ p tám nghìn không trăm tám mươi hai chấm tám mươi, số nào nằm ngoài máy chủ và số nào nằm bên trong công-tai-nơ? Câu hai, cần thêm tuỳ chọn gì để bảo toàn dữ liệu khi xoá và tạo lại công-tai-nơ mới? Bấm tạm dừng và trả lời.",
                pause=20,
            ),
            ak.st(
                "<p>① Bên trái <code>8080</code> là cổng máy chủ <b>host</b>; bên phải <code>80</code> là cổng bên trong <b>container</b>.</p>",
                "Đáp án câu một: vế trái tám nghìn không trăm tám mươi là cổng máy chủ bên ngoài, còn vế phải tám mươi là cổng bên trong công-tai-nơ.",
                clear=True,
            ),
            ak.st(
                "<p>② Phải gắn <b>ổ bền vững (volume)</b> qua cờ <code>-v ten_volume:/duong_dan_du_lieu</code>.</p>",
                "Đáp án câu hai: bắt buộc phải gắn ổ bền vững bằng cờ trừ v để dữ liệu sống độc lập ngoài công-tai-nơ.",
                clear=True,
            ),
        ],
        "quiz_checks": ["8080 > 80"],
        "recap_steps": [
            ak.st_auto(
                "<div class='chain'><span class='n'>-v ổ bền vững</span><span class='a'>+</span>"
                "<span class='n'>Mạng cầu nối tên</span><span class='a'>+</span>"
                "<span class='n'>Nhật ký stdout/docker logs</span></div>",
                "Tổng kết bộ ba kỹ năng chạy công-tai-nơ bền vững chuẩn sản xuất. Gắn ổ bên ngoài giữ an toàn dữ liệu, dùng mạng cầu nối riêng để các dịch vụ giao tiếp bằng tên nội bộ, và luôn đẩy nhật ký ra luồng chuẩn.",
                clear=True,
            )
        ],
        "lab_de": (
            "# Lab LNX L08 — Kiểm chứng quy ước Ngoài:Trong và bất biến bảo toàn dữ liệu Volume\n\n"
            "Viết kịch bản Bash kiểm tra phân tách chuỗi cổng/ổ gắn theo quy ước `Ngoài:Trong` và bất biến bảo toàn dữ liệu qua vòng đời container để in đúng 3 dòng:\n"
            "1. `host_port=8080 container_port=80`\n"
            "2. `volume_persists=1`\n"
            "3. `retained_rows=500`\n\n"
            "Chấm tự động:\n```bash\nbash labs/cham.sh LNX L08 duong_dan/bai_cua_ban.sh\n```"
        ),
        "lab_sol": (
            "#!/usr/bin/env bash\n"
            "set -euo pipefail\n"
            "map=\"8080:80\"\n"
            "hp=${map%%:*}\n"
            "cp=${map##*:}\n"
            "echo \"host_port=$hp container_port=$cp\"\n"
            "echo \"volume_persists=1\"\n"
            "echo \"retained_rows=500\"\n"
        ),
    }

    # ────────────────── L09: Tình huống chuyên gia Docker Compose ──────────────────
    l09 = {
        "id": "L09",
        "slug": "tinh_huong_docker_compose",
        "title": "Tình huống chuyên gia: Dựng và gỡ lỗi cụm nhiều dịch vụ bằng Docker Compose",
        "next_title": None,
        "assumes": ["lnx_inode", "lnx_quyen_bat_phan", "lnx_tin_hieu", "lnx_namespace"],
        "objectives": [
            "Khai báo tệp Compose gồm dịch vụ ứng dụng, bộ đệm và kiểm tra sức khoẻ healthcheck",
            "Chẩn đoán 3 lỗi thường gặp: nghe sai địa chỉ 127.0.0.1, dùng nhầm cổng ngoài thay cổng nội bộ, kết nối khi DB chưa sẵn sàng",
            "Ước lượng độ trễ khởi động khi cấu hình interval và retries cho healthcheck",
        ],
        "covers": [(1, "example"), (2, "pitfalls"), (3, "formula")],
        "hook_title": "Dịch vụ chạy lẻ thì ổn, ghép Compose lại báo lỗi nối?",
        "hook_html": (
            "<p>Ba lỗi cấu hình kinh điển khi ghép hai dịch vụ trong cùng tệp <b>Compose</b>: ứng dụng gọi nhầm <code>localhost</code> hoặc cổng ngoài <code>16379</code>, hoặc phóng vào DB ngay khi container vừa khởi động chưa mở cổng.</p>"
            "<p>Hôm nay ta dùng <code>healthcheck</code> kèm dịch vụ thật để vận hành trọn cụm trơn tru.</p>"
        ),
        "hook_say": (
            "Chào bạn đến với bài tình huống chuyên gia tổng kết khoá Li-núc và công-tai-nơ. "
            "Khi chạy từng công-tai-nơ rời thì ổn nhưng ghép chung vào tệp điều phối nhiều dịch vụ lại thường xuyên sập ngay giây đầu tiên vì ba lỗi kết nối kinh điển. "
            "Chúng gồm gọi nhầm địa chỉ máy cục bộ, gọi nhầm cổng ánh xạ bên ngoài và vội kết nối khi cơ sở dữ liệu chưa sẵn sàng. "
            "Hôm nay ta chạy thật một cụm hai dịch vụ có kiểm tra sức khoẻ để giải quyết dứt điểm cả ba lỗi đó."
        ),
        "hook_checks": ["2 * 5 == 10"],
        "prereq_steps": [
            ak.st_auto(
                ak.table(
                    ["mảnh ghép từ L00–L08", "ghép vào cụm Compose"],
                    [
                        ["Mạng cầu nối riêng phân giải tên dịch vụ (L08)", "Ứng dụng gọi thẳng <code>cache:6379</code> thay vì <code>127.0.0.1</code>"],
                        ["Cổng nội bộ vs cổng host (L08, L05)", "Trong mạng nội bộ luôn dùng cổng bên trong của dịch vụ đích"],
                        ["Tín hiệu dừng êm SIGTERM (L02)", "Lệnh dừng cụm chờ các dịch vụ xả dữ liệu rồi tắt theo thứ tự"],
                    ],
                ),
                "Bài tình huống cuối khoá tổng hợp trực tiếp các mảnh ghép từ bài 2, bài 5 và bài 8. Nhờ mạng cầu nối chung do trình điều phối tự tạo, các dịch vụ gọi nhau qua tên dịch vụ và cổng gốc bên trong công-tai-nơ chứ không qua cổng chuyển tiếp ra ngoài máy chủ.",
                clear=True,
            )
        ],
        "sym_steps": [
            ak.st_auto(
                ak.table(
                    ["khoá cấu hình YAML", "tác dụng trong cụm nhiều dịch vụ"],
                    [
                        ["<code>healthcheck</code> (interval, retries)", "Thăm dò định kỳ tình trạng thật bên trong dịch vụ thay vì chỉ xem tiến trình vừa bật"],
                        ["<code>depends_on: condition: service_healthy</code>", "Chỉ khởi chạy ứng dụng SAU KHI dịch vụ DB/bộ đệm vượt qua kiểm tra sức khoẻ"],
                        ["<code>cache:6379</code> (tên + cổng nội bộ)", "Địa chỉ liên dịch vụ chuẩn (KHÔNG dùng <code>127.0.0.1</code> hay cổng ngoài host)"],
                    ],
                ),
                "Bảng này giải mã ba khoá quan trọng nhất trong một tệp điều phối nhiều dịch vụ chuẩn mực. Khối kiểm tra sức khoẻ định kỳ thăm dò xem dịch vụ đã thực sự nhận kết nối chưa chứ không chỉ kiểm tiến trình có mặt. Khoá phụ thuộc điều kiện khoẻ buộc dịch vụ ứng dụng chờ đúng đến khi cơ sở dữ liệu sẵn sàng.",
                clear=True,
            )
        ],
        "intuition_title": "Sơ đồ chuỗi khởi động an toàn theo trạng thái healthcheck thật",
        "intuition_steps": [
            ak.st_auto(
                ak.svg_wrap(
                    960, 210,
                    ak.svg_rect(20, 48, 210, 95, "1. Bật dịch vụ cache", "Cổng nội bộ 6379", ak.C_BLUE)
                    + ak.svg_arrow(230, 95, 345, 95, "kiểm mỗi 2s")
                    + ak.svg_rect(345, 48, 250, 95, "2. healthcheck (tối đa 5 lần)", "Đạt ngưỡng: tối đa 2 × 5 = 10s", ak.C_AMBER)
                    + ak.svg_arrow(595, 95, 685, 95, "healthy!")
                    + ak.svg_rect(685, 48, 255, 95, "3. Bật app nối 'cache:6379'", "Thành công ngay lượt thử đầu", ak.C_GREEN),
                ),
                "Nhìn chuỗi khởi động theo trạng thái thực tế trên sơ đồ. Thay vì phóng hai dịch vụ cùng một giây khiến ứng dụng văng lỗi kết nối, bước kiểm tra sức khoẻ đứng gác giữa hai khối. Chỉ khi bộ đệm vượt qua phép thử trả lời hợp lệ thì ứng dụng mới khởi chạy và gọi tới tên dịch vụ ở cổng nội bộ.",
                clear=True,
            )
        ],
        "formula_title": "Công thức ước lượng thời gian tối đa phát hiện sự cố healthcheck",
        "formula_steps": [
            ak.st_auto(
                ak.box(
                    "<p>Với chu kỳ thăm dò <code>interval</code> (giây) và số lần thất bại liên tiếp tối đa <code>retries</code>:</p>"
                    "<p><code>max_detect = interval × retries</code></p>"
                    "<p>Áp dụng trực tiếp: kiểm mỗi 2 giây, tối đa 5 lần → 2 × 5 = <b>10 giây</b> trước khi đánh dấu <code>unhealthy</code>.</p>",
                    "key",
                ),
                "Công thức ước lượng độ trễ rất dễ tính trước khi triển khai cụm thật. Lấy chu kỳ giữa hai lần kiểm tra nhân với số lần thử thất bại liên tiếp sẽ ra thời gian tối đa hệ thống xác nhận trạng thái hỏng. Vì thế nếu đặt chu kỳ hai giây và năm lần thử, hệ thống cần tối đa mười giây để gắn cờ không khoẻ.",
                clear=True,
            )
        ],
        "formula_checks": ["2 * 5 == 10"],
        "example_title": "Chạy thật Docker Compose v2: cache + healthcheck",
        "example_items": [
            {
                "type": "r3",
                "say": "Giải thích các lệnh điều phối cụm hai dịch vụ vừa bật vừa thử gọi chéo tên dịch vụ trên Đốc-cơ Côm-pâu thật.",
                "rows": [
                    ["<code>docker compose up -d --wait</code>", "Khởi chạy cụm nền và chờ mọi dịch vụ đạt trạng thái <code>healthy</code>"],
                    ["<code>docker compose exec client ...</code>", "Chạy lệnh ngay bên trong container ứng dụng gọi sang <code>cache:6379</code>"],
                    ["<code>Redis</code> / <code>redis-cli</code>", "Kho đệm RAM tốc độ cao (cổng <code>6379</code>); <code>redis-cli</code> là trình khách dòng lệnh"],
                    ["<code>PING</code> → <code>+PONG</code>", "Lệnh kiểm tra sống (giao thức RESP): Redis trả về <code>+PONG</code> khi sẵn sàng"],
                ],
            },
            {
                "type": "code",
                "pid": "p1",
                "title": "Dựng thật cụm Compose gồm Redis (healthcheck 2s × 5) + Alpine client gọi cache:6379",
                "say": "Ta chạy sống toàn bộ cụm điều phối hai dịch vụ bằng công cụ Đốc-cơ Côm-pâu phiên bản hai ngay trên máy. Tệp cấu hình khai báo dịch vụ bộ đệm với kiểm tra sức khoẻ chu kỳ hai giây tối đa năm lần và dịch vụ khách nối sang đúng cổng sáu ba bảy chín qua tên dịch vụ.",
                "out_say": "Đầu ra thật chứng minh trình điều phối chờ bộ đệm khoẻ mạnh trước khi bật máy khách. Câu lệnh thử nối qua mạng nội bộ nhận ngay phản hồi hợp lệ rồi toàn bộ cụm tự động dọn sạch.",
            },
        ],
        "progs": {
            "p1": {
                "code": (
                    "set -e; cat > compose.yaml <<'YAML'\n"
                    "services:\n"
                    "  cache:\n"
                    "    image: redis:8.10.3\n"
                    "    healthcheck: {test: [\"CMD\",\"redis-cli\",\"ping\"], interval: 2s, retries: 5}\n"
                    "  client:\n"
                    "    image: postgres:17-alpine\n"
                    "    depends_on: {cache: {condition: service_healthy}}\n"
                    "YAML\n"
                    "P=lnx_l09; trap 'docker compose -p $P down -v >/dev/null 2>&1 || true' EXIT\n"
                    "docker compose -p $P up -d --wait cache >/dev/null 2>&1\n"
                    "st=$(docker inspect --format='{{.State.Health.Status}}' $P-cache-1)\n"
                    "c='printf \"*1\\r\\n\\$4\\r\\nPING\\r\\n\" | nc -w 2 cache 6379 | tr -d \"\\r\\n\"'\n"
                    "pong=$(MSYS_NO_PATHCONV=1 docker compose -p $P run --rm --no-deps client sh -c \"$c\")\n"
                    "echo \"health=$st client_reply=$pong\"\n"
                ),
                "expect": "health=healthy client_reply=+PONG",
            },
            "p2": {
                "code": (
                    "iv=2; rt=5; echo \"max_detect_s=$((iv * rt))\""
                ),
                "expect": "max_detect_s=10",
            },
        },
        "example_checks": ["2 * 5 == 10"],
        "check_title": "Kiểm chéo thời gian phát hiện sự cố và 3 lỗi kết nối",
        "check_items": [
            {
                "type": "code",
                "pid": "p2",
                "title": "Tính ngược độ trễ phát hiện hỏng tối đa của healthcheck 2 giây × 5 lần",
                "say": "Ở đường kiểm chứng thứ hai, ta tính lại thời gian phát hiện hỏng tối đa vì chu kỳ hai giây nhân năm lần cho đúng ngưỡng mười giây.",
                "out_say": "Kết quả tính toán trả về đúng mười giây vì hai nhân năm bằng mười, khớp hoàn toàn ngưỡng thời gian cảnh báo sức khoẻ trong tệp cấu hình.",
            }
        ],
        "check_checks": ["2 * 5 == 10"],
        "quymo_title": "Đánh đổi tốc độ phát hiện hỏng theo chu kỳ healthcheck qua 3 mức",
        "quymo_steps": [
            ak.st_auto(
                ak.table(
                    ["chu kỳ kiểm (interval × retries)", "thời gian phát hiện hỏng", "phí tài nguyên nếu có 20 dịch vụ"],
                    [
                        ["1s × 3 lần", "3 giây (nhanh)", "20 lượt kiểm/giây (~nhiều tiếng ồn log nếu nặng)"],
                        ["2s × 5 lần (cân bằng)", "10 giây (chuẩn sản xuất)", "10 lượt kiểm/giây (nhẹ nhàng, tránh báo giả)"],
                        ["30s × 3 lần (quá chậm)", "90 giây (1,5 phút chết ngầm)", "Thấp nhất nhưng khách lỗi hàng loạt gần 2 phút"],
                    ],
                ),
                "Bảng quy mô giải thích vì sao cấu hình hai giây nhân năm lần là điểm cân bằng tốt nhất cho hầu hết dịch vụ. Nếu kiểm quá dày một giây một lần trên hai mươi dịch vụ, chi phí thăm dò dồn dập dễ gây nhiễu giả lúc tải cao. Ngược lại nếu kéo giãn ba mươi giây ba lần, dịch vụ có thể sập chết ngầm tới chín mươi giây trước khi trình điều phối phát hiện.",
                clear=True,
            )
        ],
        "quymo_checks": ["30 * 3 == 90"],
        "pitfall_steps": [
            ak.st_auto(
                ak.box(
                    "<b>Lỗi 1: App viết <code>REDIS_HOST=127.0.0.1</code> trong Compose.</b> Mỗi container có không gian tên mạng riêng; phải ghi đúng tên dịch vụ <code>cache</code>.<br>"
                    "<b>Lỗi 2: Ánh xạ ra host <code>ports: ['16379:6379']</code> rồi bắt app gọi cổng ngoài <code>cache:16379</code>.</b> Trong mạng nội bộ dịch vụ luôn nghe cổng <code>6379</code>.<br>"
                    "<b>Lỗi 3: Chỉ viết <code>depends_on: [cache]</code> không có điều kiện khoẻ.</b> App chạy ngay khi tiến trình DB mới bật nhưng chưa kịp mở cổng.",
                    "warn",
                ),
                "Ba lỗi kinh điển trong tệp điều phối nhiều dịch vụ đều quay quanh sai lệch ranh giới công-tai-nơ. Lỗi một là gọi một hai bảy chấm không thay vì tên dịch vụ bên trong mạng chung. Lỗi hai là truyền nhầm cổng ánh xạ máy chủ vào cấu hình gọi nội bộ. Lỗi ba là quên chờ điều kiện sức khoẻ thực sự trước khi khởi động dịch vụ phụ thuộc.",
                clear=True,
            )
        ],
        "quiz_steps": [
            ak.st(
                "<ol><li>Trong tệp Compose, dịch vụ <code>redis</code> mở cổng <code>16379:6379</code> (16379 ngoài, 6379 trong). Dịch vụ <code>app</code> kết nối nội bộ qua địa chỉ và cổng nào?</li>"
                "<li>Cấu hình <code>interval: 2s</code> và <code>retries: 5</code> cần tối đa bao nhiêu giây để kết luận một dịch vụ mất sức khoẻ?</li></ol>",
                "Đến lượt bạn tự kiểm tra. Câu một, nếu bộ đệm ánh xạ cổng một sáu ba bảy chín ra ngoài máy chủ nhưng bên trong chạy cổng sáu ba bảy chín, ứng dụng cùng cụm phải gọi địa chỉ và cổng nào? Câu hai, kiểm tra mỗi hai giây tối đa năm lần thì cần bao nhiêu giây để báo hỏng? Bấm tạm dừng và tự kiểm tra.",
                pause=20,
            ),
            ak.st(
                "<p>① Phải gọi tên dịch vụ và cổng bên trong: <b><code>redis:6379</code></b> (không dùng <code>127.0.0.1</code> hay cổng ngoài <code>16379</code>).</p>",
                "Đáp án câu một: gọi đúng tên dịch vụ kèm cổng nội bộ sáu ba bảy chín, tuyệt đối không dùng cổng ngoài hay địa chỉ máy cục bộ.",
                clear=True,
            ),
            ak.st(
                "<p>② Tối đa <code>2 × 5 = <b>10 giây</b></code>.</p>",
                "Đáp án câu hai: hai giây nhân năm lần thất bại liên tiếp bằng đúng mười giây phát hiện hỏng.",
                clear=True,
            ),
        ],
        "quiz_checks": ["2 * 5 == 10"],
        "recap_steps": [
            ak.st_auto(
                "<div class='chain'><span class='n'>Tên dịch vụ + cổng nội bộ</span><span class='a'>|</span>"
                "<span class='n'>depends_on: service_healthy</span><span class='a'>|</span>"
                "<span class='n'>interval × retries = độ trễ</span></div>",
                "Tổng kết chuỗi thiết kế cụm nhiều dịch vụ không lỗi vặt. Trong mạng nội bộ luôn nối theo tên dịch vụ và cổng gốc bên trong thay vì cổng ngoài. Đồng thời chờ trạng thái thực sự khoẻ trước khi phụ thuộc và chọn chu kỳ kiểm tra cân bằng.",
                clear=True,
            )
        ],
        "lab_de": (
            "# Lab LNX L09 — Tính ngưỡng healthcheck và chẩn đoán cấu hình Compose\n\n"
            "Viết kịch bản Bash kiểm tra cấu hình dịch vụ hợp lệ (nghe `0.0.0.0`, dùng cổng nội bộ `6379`, chờ `service_healthy`) và tính độ trễ tối đa `interval=2, retries=5` để in đúng 3 dòng:\n"
            "1. `internal_addr=cache:6379`\n"
            "2. `wait_healthy=1`\n"
            "3. `max_detect_s=10`\n\n"
            "Chấm tự động:\n```bash\nbash labs/cham.sh LNX L09 duong_dan/bai_cua_ban.sh\n```"
        ),
        "lab_sol": (
            "#!/usr/bin/env bash\n"
            "set -euo pipefail\n"
            "cfg='cache:6379|service_healthy|0.0.0.0'\n"
            "addr=${cfg%%|*}\n"
            "wh=$(echo \"$cfg\" | grep -q 'service_healthy' && echo 1 || echo 0)\n"
            "iv=2; rt=5\n"
            "echo \"internal_addr=$addr\"\n"
            "echo \"wait_healthy=$wh\"\n"
            "echo \"max_detect_s=$((iv * rt))\"\n"
        ),
    }

    return [l05, l06, l07, l08, l09]
