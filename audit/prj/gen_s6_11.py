"""Sinh 6 bài dự án PRJ L05–L10 cho Chặng 6–11 (đầy đủ E39 >= 900 từ, checks, SVG, labs/PRJ, screen_code)."""
import sys as _sys; from pathlib import Path as _P; _sys.path.insert(0, str(_P(__file__).resolve().parents[1])); import _frozen  # noqa: E402,F401
import subprocess
import sys
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "audit" / "review"))
import lv  # noqa: E402
import af2_kit as ak  # noqa: E402
import af2_upgrader as up  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")

SERIES = "PRJ · Dự án tổng hợp cuối mỗi chặng"

PROJECTS = [
    {
        "id": "L05",
        "fname": "L05_du_an_chang_6_bo_giai_khung_lap_lich.yaml",
        "title": "Bài 5 — Dự án Chặng 6 — Giải mã khung nhị phân & lập lịch đa nhân",
        "obj": [
            "Giải mã cấu trúc khung gói nhị phân gồm header 4 byte và tải bằng Python struct",
            "Cài bộ lập lịch Round Robin với lượng tử q = 4 cho danh sách tác vụ khung",
            "So sánh thời gian chờ và độ trễ khung khi số luồng xử lý tăng gấp 4 lần",
        ],
        "prereq": [
            ("Biểu diễn byte, struct căn lề (CPR/CSA)", "Đọc chuẩn nhị phân <code>uint16_t</code> little-endian không lệch byte"),
            ("Lập lịch CPU Round Robin q = 4 (OSY)", "Chia lát thời gian đều cho các luồng tránh tác vụ lớn chiếm CPU"),
            ("Đóng khung gói & trễ truyền (NET/LNX)", "Kiểm tra kích thước header + payload chuẩn Ethernet/TCP"),
        ],
        "prereq_say": (
            "Dự án Chặng 6 ghép ba nền tảng hệ thống cốt lõi mà bạn đã học xuyên suốt chặng này. "
            "Thứ nhất là cách giải mã cấu trúc nhị phân cấp byte bằng thư viện chuẩn mà không đọc sai thứ tự byte. "
            "Thứ hai là thuật toán lập lịch CPU xoay vòng giúp chia lát công bằng giữa nhiều gói tin đến đồng thời. "
            "Thứ ba là quy tắc kiểm đủ độ dài tải khi đóng khung truyền tin trên mạng và bộ chứa ảo hoá."
        ),
        "svg_boxes": [("Khung nhị phân", "Header 4 B + Tải"), ("Hàng đợi RR q=4", "Xoay vòng công bằng"), ("Kết quả đo", "Chờ TB & kiểm tổng")],
        "svg_say": (
            "Sơ đồ minh họa ba bước nối tiếp của bộ phân tích khung và lập lịch đa nhân. "
            "Ở chặng đầu, hệ thống bóc phần đầu bốn byte để lấy mã gói và độ dài tải. "
            "Ở chặng hai, tác vụ được xếp vào hàng đợi xoay vòng có lượng tử bốn để không gói lớn nào chặn gói nhỏ. "
            "Cuối cùng bộ đo tổng hợp thời gian chờ trung bình và kiểm tra toàn vẹn độ dài."
        ),
        "hook_say": (
            "Chào bạn đến với dự án chốt Chặng 6 tổng hợp hệ thống máy tính, hệ điều hành và mạng máy tính. "
            "Một bộ định tuyến hay trình thu thập nhật ký hiệu năng cao luôn gặp hai bài toán đi liền nhau. "
            "Đầu tiên là phải đọc đúng từng byte nhị phân từ luồng thô mà không lệch căn lề hay sai đầu cuối. "
            "Tiếp theo là lập lịch xử lý sao cho một yêu cầu nặng hai mươi bốn mi-li-giây không chặn các gói nhẹ phía sau. "
            "Hôm nay ta cài trọn vẹn bộ giải mã nhị phân chuẩn cấu trúc và hàng đợi xoay vòng kiểm chứng bằng Python thật."
        ),
        "hook_txt": "Đọc đúng <b>header 4 byte</b> (2 trường 16 bit không dấu) từ luồng nhị phân thô, rồi lập lịch Round Robin <code>q = 4</code> cho ba tác vụ <code>[24, 3, 3]</code> giữ thời gian chờ trung bình <b>5,67</b> thay vì <b>17,00</b> của FCFS.",
        "hook_chk": ["4 + 64 == 68", "(6 + 4 + 7) / 3 > 5"],
        "formula_txt": "<p><b>1. Giải mã cấu trúc 4 B:</b> <code>struct.unpack('&lt;HH', buf[:4])</code> tách ra <code>(pkt_id, payload_len)</code>.</p><p><b>2. Lập lịch Round Robin q=4:</b> tổng chờ <code>(6 + 4 + 7) / 3 = <b>5,67</b></code> so với FCFS <code>17,00</code>.</p>",
        "formula_say": (
            "Ta rà lại hai công thức quyết định tính đúng của dự án trước khi viết mã thật. "
            "Ở phép giải mã, ký hiệu nhỏ trước nghĩa là đọc hai số nguyên không dấu mười sáu bít từ bốn byte đầu. "
            "Tổng kích thước khung hợp lệ phải bằng đúng bốn cộng thêm độ dài tải công bố trong phần đầu. "
            "Ở bộ lập lịch, cắt lát bốn đơn vị giúp hai tác vụ ngắn ba đơn vị hoàn tất sớm chỉ sau hai vòng đợi. "
            "Nhờ vậy thời gian chờ trung bình tụt từ mười bảy xuống năm phẩy sáu bảy đơn vị."
        ),
        "sym_rows": [
            ["<code>struct.unpack('&lt;HH', b)</code>", "Giải mã 2 số 16 bit little-endian chiếm đúng 4 byte đầu tiên"],
            ["<code>collections.deque</code>", "Hàng đợi hai đầu lấy đầu O(1) và trả phần còn dư về cuối"],
            ["<code>q = 4</code>", "Lượng tử thời gian tối đa mỗi lượt chạy trước khi nhường CPU"],
        ],
        "sym_say": (
            "Bảng ký hiệu giải thích ba công cụ Python phục vụ trực tiếp cho dự án Chặng 6. "
            "Thứ nhất là hàm giải gói cấu trúc nhỏ trước để tách mã định danh và chiều dài tải. "
            "Thứ hai là hàng đợi hai đầu giúp rút và trả tác vụ cuối lượt trong thời gian hằng số. "
            "Thứ ba là lượng tử bằng bốn giúp cân bằng giữa độ nhạy và chi phí chuyển ngữ cảnh."
        ),
        "ex_code": (
            "import struct\nfrom collections import deque\n"
            "buf = struct.pack('<HH', 101, 64) + b'A' * 64\n"
            "pid, plen = struct.unpack('<HH', buf[:4])\n"
            "rem, t, fin, q = [24, 3, 3], 0, [0]*3, deque([0,1,2])\n"
            "while q:\n"
            "    i = q.popleft(); d = min(4, rem[i]); t += d; rem[i] -= d\n"
            "    if rem[i] > 0: q.append(i)\n"
            "    else: fin[i] = t\n"
            "w = [fin[i] - [24,3,3][i] for i in range(3)]\n"
            "print(f'pkt={pid} len={plen} frame={4+plen}')\n"
            "print(f'rr_waits={w[0]},{w[1]},{w[2]} avg={sum(w)/3:.2f}')\n"
        ),
        "ex_say": (
            "Đoạn mã này đóng gói thử một khung sáu mươi tám byte gồm bốn byte đầu và sáu mươi bốn byte dữ liệu. "
            "Sau khi giải mã lấy đúng mã một trăm lẻ một và độ dài sáu tư, chương trình chạy hàng đợi xoay vòng cho ba tác vụ. "
            "Mỗi tác vụ chạy tối đa bốn đơn vị rồi nhường chỗ nên hai gói ngắn thoát ngay ở lượt đầu tiên."
        ),
        "ex_out_say": (
            "Đầu ra chạy thật trên Python xác nhận tổng kích thước khung đúng bằng sáu mươi tám byte. "
            "Thời gian chờ lần lượt của ba tác vụ là sáu, bốn và bảy nên giá trị trung bình đạt năm phẩy sáu bảy."
        ),
        "chk_code": (
            "b = [24, 3, 3]; t = 0; fw = []\n"
            "for x in b: fw.append(t); t += x\n"
            "print(f'fcfs_avg={sum(fw)/3:.2f} saved={sum(fw)/3 - 17/3:.2f}')\n"
        ),
        "chk_say": (
            "Ở phép kiểm chứng độc lập, ta tính ngược lại thời gian chờ của hàng đợi đến trước phục vụ trước để so sánh. "
            "Do gói đầu chiếm trọn hai mươi bốn đơn vị nên hai gói sau phải chờ tích lũy tới hai tư và hai bảy."
        ),
        "chk_out_say": (
            "Kết quả đối chứng cho thấy trung bình của đến trước phục vụ trước lên tới mười bảy nên lập lịch xoay vòng tiết kiệm hơn mười một đơn vị. "
            "Số liệu khớp chặt với công thức lý thuyết nhờ chia đúng lát thời gian."
        ),
        "quymo": [
            ("1 000 khung/s", "0,5% tải 1 nhân", "Độ trễ ổn định < 1 ms"),
            ("100 000 khung/s", "50% tải 1 nhân", "Cần gom lô giảm gọi hệ thống"),
            ("1 000 000 khung/s", "Quá tải 1 nhân", "Tách 4–8 worker pin vào từng nhân"),
        ],
        "quymo_say": (
            "Bảng quy mô đối chiếu khả năng đáp ứng khi lưu lượng gói tăng từ một nghìn lên một triệu khung mỗi giây. "
            "Ở mức một trăm nghìn khung, gom lô nhiều khung mỗi lần đọc giúp giảm hẳn số lần chuyển ngữ cảnh vào nhân. "
            "Lên tới một triệu khung thì một luồng đơn sẽ nghẽn, buộc ta phải chia luồng theo nhân bộ xử lý."
        ),
        "pitfalls": [
            "<b>Lỗi 1 (-30đ):</b> Dùng sai endianness <code>&gt;HH</code> cho luồng <code>&lt;HH</code> làm sai độ dài gói.",
            "<b>Lỗi 2 (-20đ):</b> Không đưa phần tử chưa xong về cuối hàng đợi làm mất tính xoay vòng.",
            "<b>Lỗi 3 (-10đ):</b> Quên kiểm tra độ dài thực tế <code>len(payload) == plen</code> dễ đọc vượt biên.",
        ],
        "pitfalls_say": (
            "Có ba lỗi phổ biến làm bài dự án bị trừ nặng điểm khi chạy bộ kiểm thử tự động. "
            "Lỗi nặng nhất là giải mã nhầm thứ tự byte lớn trước làm chiều dài tải nhảy vọt vô lý. "
            "Thứ hai là quên đẩy lại tác vụ chưa xong vào cuối hàng đợi khiến thuật toán thoái hoá thành chạy tuần tự. "
            "Thứ ba là quên đối chiếu chiều dài bộ đệm thực nhận với trường độ dài khai báo."
        ),
        "q_text": "<ol><li>Khung có header 4 B và tải 64 B thì tổng kích thước khung bằng bao nhiêu?</li><li>Với [24, 3, 3], Round Robin q = 4 cho thời gian chờ trung bình gần đúng là bao nhiêu?</li></ol>",
        "q_say": "Trước khi mở đề thực hành, bạn trả lời nhanh hai câu hỏi kiểm hiểu bên dưới. Câu một, khung có bốn byte đầu và tải sáu mươi bốn byte thì tổng bằng bao nhiêu? Câu hai, với chuỗi hai tư, ba, ba, thời gian chờ trung bình khi cắt lát bốn gần đúng là mấy? Bấm tạm dừng và trả lời.",
        "q_ans1": "Tổng kích thước khung là <code>4 + 64 = <b>68</b> byte</code>.",
        "q_ans1_say": "Đáp án câu một: tổng kích thước khung bằng bốn cộng sáu mươi bốn là sáu mươi tám byte.",
        "q_ans2": "Các thời gian chờ 6, 4, 7 cho trung bình <code>17 / 3 ≈ <b>5,67</b></code>.",
        "q_ans2_say": "Đáp án câu hai: tổng thời gian chờ của ba tiến trình bằng mười bảy nên chia ba ra năm phẩy sáu bảy.",
        "lab_de": "# Dự án PRJ L05 — Giải mã khung nhị phân & lập lịch đa nhân\n\nViết chương trình Python giải mã header `<HH` của khung `(id=7, len=32)` cộng tải 32 byte, và chạy Round Robin `q=4` cho `[24, 3, 3]`, in đúng 3 dòng:\n1. `frame_total_bytes=36`\n2. `rr_avg_wait=5.67`\n3. `header_valid=1`\n\nChấm tự động:\n```bash\nbash labs/cham.sh PRJ L05 duong_dan/bai_cua_ban.py\n```",
        "lab_sol": (
            "import struct\nfrom collections import deque\n"
            "buf = struct.pack('<HH', 7, 32) + b'x' * 32\n"
            "pid, plen = struct.unpack('<HH', buf[:4])\n"
            "rem, t, fin, q = [24, 3, 3], 0, [0]*3, deque([0,1,2])\n"
            "while q:\n"
            "    i = q.popleft(); d = min(4, rem[i]); t += d; rem[i] -= d\n"
            "    if rem[i] > 0: q.append(i)\n"
            "    else: fin[i] = t\n"
            "w = [fin[i] - [24,3,3][i] for i in range(3)]\n"
            "print(f'frame_total_bytes={4 + plen}')\n"
            "print(f'rr_avg_wait={sum(w)/3:.2f}')\n"
            "print(f'header_valid={int(pid == 7 and len(buf) == 4 + plen)}')\n"
        ),
        "chain": ["Header &lt;HH 4 B", "Round Robin q=4", "Kiểm đủ độ dài tải"],
    },
    {
        "id": "L06",
        "fname": "L06_du_an_chang_7_nhat_ky_hmac_sqlite.yaml",
        "title": "Bài 6 — Dự án Chặng 7 — Nhật ký HMAC có chỉ mục SQLite & bảo vệ tốc độ",
        "obj": [
            "Lưu nhật ký vào cơ sở dữ liệu SQLite có chỉ mục B-Tree và dùng truy vấn tham số hoá",
            "Ký và kiểm chứng toàn vẹn từng bản ghi nhật ký bằng HMAC-SHA256",
            "Đánh giá chi phí quét có chỉ mục khi bảng nhật ký mở rộng tới hàng triệu dòng",
        ],
        "prereq": [
            ("Chỉ mục B-Tree & SQL tham số hoá (DBS/SWF)", "Tìm log trong O(log N) và chặn hoàn toàn tấn công chèn SQL"),
            ("Mẫu thiết kế sạch (SDP)", "Tách lớp ký HMAC khỏi lớp lưu trữ SQLite"),
            ("HMAC-SHA256 RFC 2104 (SEC/WEB)", "Xác thực bản ghi không bị sửa trộm sau khi ghi"),
        ],
        "prereq_say": (
            "Dự án Chặng 7 nối ba mảnh kiến thức lớn của chặng kỹ nghệ phần mềm, cơ sở dữ liệu và an toàn thông tin. "
            "Thứ nhất là dùng chỉ mục cây cân bằng trên SQLite kết hợp tham số hoá để truy xuất nhanh và an toàn. "
            "Thứ hai là tổ chức hàm ký tách biệt giúp dễ kiểm thử độc lập như đã học ở mẫu thiết kế. "
            "Thứ ba là gắn thẻ xác thực thông điệp có khoá để phát hiện mọi thao tác sửa trộm dữ liệu sau khi ghi."
        ),
        "svg_boxes": [("Sự kiện log", "Ký HMAC-SHA256"), ("SQLite + Index", "Truy vấn tham số ?"), ("Kiểm toàn vẹn", "Chặn SQLi & sửa lậu")],
        "svg_say": (
            "Luồng xử lý an toàn của dịch vụ nhật ký đi qua ba khâu nối tiếp. "
            "Đầu tiên mỗi thông điệp được băm kèm khoá bí mật thành chữ ký sáu mươi bốn ký tự hexa. "
            "Tiếp đó bản ghi đi qua lệnh chèn tham số dấu hỏi vào bảng SQLite đã đánh chỉ mục sẵn. "
            "Khi đọc lại, hệ thống vừa chống được chèn mã SQL vừa kiểm chữ ký tức thì."
        ),
        "hook_say": (
            "Chào bạn đến với dự án chốt Chặng 7 tổng hợp kỹ nghệ phần mềm, cơ sở dữ liệu và bảo mật. "
            "Nếu chỉ lưu nhật ký bằng văn bản trơn trong cơ sở dữ liệu, kẻ xâm nhập có thể âm thầm sửa xoá dấu vết. "
            "Đồng thời nếu nối chuỗi trực tiếp khi lọc tên người dùng, ứng dụng sẽ lộ toàn bộ dữ liệu trước câu lệnh SQL độc hại. "
            "Hôm nay ta dựng một sổ nhật ký SQLite thật có chỉ mục tìm nhanh, tham số hoá và chữ ký HMAC xác thực từng bản ghi."
        ),
        "hook_txt": "Ghi bản ghi vào SQLite có <code>CREATE INDEX</code>, chặn 100% payload chèn SQL bằng <code>?</code> và kiểm chứng <b>HMAC-SHA256</b> dài 64 hex phát hiện ngay bất kỳ bản ghi nào bị sửa 1 ký tự.",
        "hook_chk": ["32 * 2 == 64", "256 // 8 == 32"],
        "formula_txt": "<p><b>1. Ký toàn vẹn:</b> <code>mac = hmac.new(key, msg, sha256).hexdigest()</code>, đối chiếu bằng <code>compare_digest</code>.</p><p><b>2. Truy vấn an toàn &amp; nhanh:</b> chỉ mục B-Tree tìm trong <code>log2(N)</code> bước, tham số <code>?</code> tách mã khỏi dữ liệu.</p>",
        "formula_say": (
            "Cơ chế bảo vệ dựa trên hai công thức và quy chuẩn cốt lõi. "
            "Nhờ dùng hàm băm có khoá theo chuẩn RFC, kẻ xấu không biết khoá bí mật thì không thể tính lại thẻ chữ ký khớp sau khi sửa dữ liệu. "
            "Khi so sánh hai chuỗi băm, hàm đối chiếu hằng thời gian giúp tránh rò rỉ thông tin theo thời gian chạy. "
            "Ở tầng lưu trữ, chỉ mục cây giữ số bước tìm kiếm ở mức lô-ga-rít cơ số hai của số dòng."
        ),
        "sym_rows": [
            ["<code>hmac.new(k, m, sha256)</code>", "Tạo mã xác thực 256 bit (64 ký tự hexa) gắn với khoá bí mật"],
            ["<code>hmac.compare_digest</code>", "So sánh chữ ký trong thời gian hằng số chống kênh kề"],
            ["<code>WHERE msg = ?</code>", "Truy vấn tham số hoá trên SQLite chặn hoàn toàn chèn SQL"],
        ],
        "sym_say": (
            "Ba hàm trên màn hình là trụ cột triển khai dự án Chặng 7. "
            "Hàm tạo thẻ HMAC sinh chuỗi sáu mươi bốn ký tự thập lục phân đại diện cho nội dung và khoá. "
            "Hàm đối chiếu digest kiểm chữ ký an toàn mà không dừng sớm ở ký tự sai đầu tiên. "
            "Cuối cùng dấu chấm hỏi giữ cho dữ liệu người dùng luôn chỉ là chuỗi thuần trong SQLite."
        ),
        "ex_code": (
            "import hashlib, hmac, sqlite3\n"
            "c = sqlite3.connect(':memory:')\n"
            "c.execute('CREATE TABLE log(id INT PRIMARY KEY, msg TEXT, mac TEXT)')\n"
            "c.execute('CREATE INDEX idx_msg ON log(msg)')\n"
            "k = b'k7'; tag = hmac.new(k, b'login:an', hashlib.sha256).hexdigest()\n"
            "c.execute('INSERT INTO log VALUES(?,?,?)', (1, 'login:an', tag))\n"
            "sqli = c.execute('SELECT * FROM log WHERE msg=?', (\"' OR '1'='1\",)).fetchall()\n"
            "row = c.execute('SELECT msg, mac FROM log WHERE id=1').fetchone()\n"
            "ok = hmac.compare_digest(row[1], hmac.new(k, row[0].encode(), hashlib.sha256).hexdigest())\n"
            "print(f'mac_hex_len={len(tag)} sqli_rows={len(sqli)} hmac_ok={int(ok)}')\n"
        ),
        "ex_say": (
            "Chương trình mẫu khởi tạo bảng nhật ký trong bộ nhớ và gắn ngay chỉ mục lên cột thông điệp. "
            "Sau khi chèn một bản ghi đã ký HMAC hợp lệ, ta thử tiêm chuỗi tấn công chèn SQL quen thuộc qua dấu hỏi. "
            "Cuối cùng ta truy xuất bản ghi từ SQLite và tính lại HMAC để khẳng định chữ ký trùng khớp."
        ),
        "ex_out_say": (
            "Đầu ra chạy thật cho thấy độ dài thẻ đúng bằng sáu mươi bốn ký tự hexa. "
            "Payload tấn công trả về đúng không dòng và kiểm tra chữ ký trả về một tức hoàn toàn hợp lệ."
        ),
        "chk_code": (
            "import hashlib, hmac\n"
            "t1 = hmac.new(b'k7', b'login:an', hashlib.sha256).hexdigest()\n"
            "t2 = hmac.new(b'k7', b'login:xx', hashlib.sha256).hexdigest()\n"
            "print(f'tamper_detected={int(not hmac.compare_digest(t1, t2))}')\n"
        ),
        "chk_say": (
            "Ở phép kiểm chứng thứ hai, ta cố tình thay đổi hai ký tự cuối của thông điệp nhật ký rồi băm lại bằng cùng khoá bí mật. "
            "Vì đặc tính hiệu ứng tuyết lở của hàm băm, hai chữ ký phải khác hẳn nhau."
        ),
        "chk_out_say": (
            "Kết quả chạy độc lập in ra bằng một vì đối chiếu chữ ký đã lập tức phát hiện hành vi sửa nội dung bản ghi. "
            "Như vậy bất kỳ thay đổi trái phép nào trong bảng đều không thể qua mặt bước kiểm tra."
        ),
        "quymo": [
            ("10 000 dòng", "Quét bảng ~1 ms", "Chỉ mục ~0,05 ms"),
            ("1 000 000 dòng", "Quét toàn bảng ~120 ms", "Chỉ mục B-Tree 3 tầng ~0,1 ms"),
            ("100 000 000 dòng", "Quét toàn bảng treo vài giây", "Chỉ mục 4 tầng giữ độ trễ < 1 ms"),
        ],
        "quymo_say": (
            "Bảng quy mô giải thích vì sao dịch vụ nhật ký bắt buộc phải đánh chỉ mục ngay từ thiết kế ban đầu. "
            "Từ một triệu lên một trăm triệu dòng, chi phí quét tuần tự tăng tuyến tính gây nghẽn toàn bộ hệ thống. "
            "Trong khi đó cây cân bằng chỉ tăng thêm đúng một tầng đọc đĩa nên thời gian phản hồi giữ dưới một mi-li-giây."
        ),
        "pitfalls": [
            "<b>Lỗi 1 (-30đ):</b> Nối chuỗi <code>f\"WHERE msg='{u}'\"</code> thay vì dùng <code>?</code> làm hở lỗ hổng SQLi.",
            "<b>Lỗi 2 (-20đ):</b> So sánh chữ ký bằng <code>==</code> dễ lộ thông tin thời gian; phải dùng <code>compare_digest</code>.",
            "<b>Lỗi 3 (-10đ):</b> Lưu khoá HMAC cứng trong lịch sử mã nguồn công khai.",
        ],
        "pitfalls_say": (
            "Khi triển khai dịch vụ nhật ký bảo mật, bạn tuyệt đối tránh ba lỗi mất điểm sau đây. "
            "Thứ nhất là ghép trực tiếp biến đầu vào vào chuỗi câu lệnh SQL thay vì dùng tham số dấu hỏi. "
            "Thứ hai là so sánh chuỗi băm bằng toán tử hai dấu bằng thông thường thay cho hàm hằng thời gian. "
            "Thứ ba là đưa khoá bí mật lên kho lưu trữ chung khiến ai có quyền đọc mã đều giả được chữ ký."
        ),
        "q_text": "<ol><li>Thẻ HMAC-SHA256 dạng thập lục phân gồm bao nhiêu ký tự?</li><li>Tham số hoá <code>?</code> chặn tấn công gì khi lọc nhật ký?</li></ol>",
        "q_say": "Hãy dừng lại để tự trả lời hai câu hỏi ôn tập cho dự án Chặng 7. Câu một, mã HMAC chuẩn SHA hai trăm năm mươi sáu dưới dạng chuỗi hexa có bao nhiêu ký tự? Câu hai, dấu chấm hỏi tham số trong câu truy vấn giúp chặn kiểu tấn công nào? Bấm tạm dừng và trả lời.",
        "q_ans1": "Hàm băm SHA-256 xuất 256 bit = 32 byte = <code><b>64</b> ký tự hexa</code>.",
        "q_ans1_say": "Đáp án câu một: hàm băm hai trăm năm mươi sáu bít tương ứng ba mươi hai byte, viết ra chuỗi thập lục phân đúng sáu mươi bốn ký tự.",
        "q_ans2": "Tham số hoá tách dữ liệu khỏi cú pháp lệnh nên chặn hoàn toàn <b>chèn SQL (SQL injection)</b>.",
        "q_ans2_say": "Đáp án câu hai: nhờ tách phần dữ liệu ra khỏi cú pháp lệnh nên truy vấn tham số chặn triệt để tấn công chèn SQL.",
        "lab_de": "# Dự án PRJ L06 — Sổ nhật ký HMAC-SHA256 & chỉ mục SQLite\n\nViết chương trình Python tạo bảng SQLite có chỉ mục, chèn bản ghi `'pay:100'` kèm chữ ký HMAC-SHA256 (khoá `b'sec_key'`), kiểm tra truy vấn SQLi `' OR 1=1--` trả 0 dòng và chữ ký hợp lệ, in đúng 3 dòng:\n1. `mac_len=64`\n2. `sqli_blocked=1`\n3. `hmac_verified=1`\n\nChấm tự động:\n```bash\nbash labs/cham.sh PRJ L06 duong_dan/bai_cua_ban.py\n```",
        "lab_sol": (
            "import hashlib, hmac, sqlite3\n"
            "c = sqlite3.connect(':memory:')\n"
            "c.execute('CREATE TABLE log(id INT PRIMARY KEY, m TEXT, mac TEXT)')\n"
            "c.execute('CREATE INDEX idx_m ON log(m)')\n"
            "mac = hmac.new(b'sec_key', b'pay:100', hashlib.sha256).hexdigest()\n"
            "c.execute('INSERT INTO log VALUES(?,?,?)', (1, 'pay:100', mac))\n"
            "bad = c.execute('SELECT * FROM log WHERE m=?', (\"' OR 1=1--\",)).fetchall()\n"
            "m, sg = c.execute('SELECT m, mac FROM log WHERE id=1').fetchone()\n"
            "ok = hmac.compare_digest(sg, hmac.new(b'sec_key', m.encode(), hashlib.sha256).hexdigest())\n"
            "print(f'mac_len={len(mac)}')\nprint(f'sqli_blocked={int(len(bad)==0)}')\nprint(f'hmac_verified={int(ok)}')\n"
        ),
        "chain": ["HMAC-SHA256 + compare_digest", "SQLite ? chặn SQLi", "B-Tree Index"],
    },
    {
        "id": "L07",
        "fname": "L07_du_an_chang_8_duong_ong_outbox_cb.yaml",
        "title": "Bài 7 — Dự án Chặng 8 — Đường ống Outbox, Băm nhất quán & Circuit Breaker",
        "obj": [
            "Ghi đơn hàng và hàng đợi Outbox trong cùng giao dịch SQLite bảo đảm không mất sự kiện",
            "Ánh xạ khoá đơn hàng tới các phân vùng nút bằng thuật toán băm nhất quán SHA-256",
            "Cài máy trạng thái Circuit Breaker tự ngắt sang OPEN sau 3 lỗi liên tiếp",
        ],
        "prereq": [
            ("Băm nhất quán & Quorum (DSY/SAR)", "Chỉ di chuyển ~1/N khoá khi thêm nút phân vùng"),
            ("Outbox & người tiêu thụ lũy đẳng (DEN/EVT)", "Chặn mất sự kiện khi tiến trình sập giữa hai thao tác"),
            ("Chịu lỗi Circuit Breaker (CLD)", "Ngắt mạch khi dịch vụ đích lỗi liên tiếp để tránh sập dây chuyền"),
        ],
        "prereq_say": (
            "Dự án Chặng 8 ghép ba cơ chế cốt lõi của kiến trúc sư hệ thống phân tán và dữ liệu lớn. "
            "Thứ nhất là mẫu Outbox ghi đơn hàng và sự kiện trong cùng giao dịch để bảo toàn dữ liệu khi sập tiến trình. "
            "Thứ hai là vòng băm nhất quán giữ cho phần lớn khoá ổn định chỗ khi mở rộng số nút phân vùng. "
            "Thứ ba là cầu dao tự ngắt để chặn đứng bão gọi lỗi vào dịch vụ hạ lưu đang quá tải."
        ),
        "svg_boxes": [("SQLite Outbox", "Cùng 1 TX nguyên tử"), ("Băm nhất quán", "Định tuyến phân vùng"), ("Circuit Breaker", "CLOSED → OPEN sau 3 lỗi")],
        "svg_say": (
            "Sơ đồ đường ống gồm ba chốt bảo vệ liên hoàn cho giao dịch phân tán. "
            "Ghi đơn và sự kiện xảy ra đồng thời trong một giao dịch SQLite duy nhất. "
            "Vòng băm phân phối sự kiện sang nút đích ổn định trước khi qua cầu dao kiểm soát lỗi."
        ),
        "hook_say": (
            "Chào bạn đến với dự án chốt Chặng 8 tổng hợp hệ phân tán, dữ liệu lớn và kiến trúc đám mây. "
            "Trong hệ thống nhiều dịch vụ, nếu lưu cơ sở dữ liệu xong rồi mới gọi gửi sự kiện qua mạng, sập nguồn ở giữa sẽ làm mất vĩnh viễn sự kiện. "
            "Đồng thời khi cụm bốn máy tăng thêm máy thứ năm, băm modulo ngây thơ đẩy tới tám mươi phần trăm khoá sang chỗ mới. "
            "Hôm nay ta cài trọn vẹn Outbox nguyên tử trên SQLite, băm nhất quán và cầu dao ba trạng thái."
        ),
        "hook_txt": "Ghi kép <code>orders + outbox</code> trong <b>1 giao dịch SQLite</b> không mất sự kiện, điều phối <b>1 000 khoá</b> với tỉ lệ dời dưới 25% khi thêm nút thứ 5, và chuyển trạng thái <code>CLOSED → OPEN</code> ngay sau <b>3 lỗi</b> liên tiếp.",
        "hook_chk": ["100 // 5 == 20", "4 + 1 == 5"],
        "formula_txt": "<p><b>1. Nguyên tử Outbox:</b> <code>COUNT(orders) == COUNT(outbox)</code> kể cả khi một giao dịch khác <code>ROLLBACK</code>.</p><p><b>2. Băm nhất quán:</b> thêm nút thứ 5 chỉ dời lý thuyết <code>1/5 = <b>20%</b></code> khoá thay vì <code>80%</code> của modulo.</p>",
        "formula_say": (
            "Hai bất biến định lượng dẫn đường cho toàn bộ dự án Chặng 8 này. "
            "Bất biến đầu tiên bảo đảm mọi đơn hàng đã xác nhận đều có đúng một bản ghi tương ứng ở hàng đợi Outbox vì cùng chung một giao dịch. "
            "Bất biến thứ hai là khi thêm nút thứ năm vào vòng băm, tỉ lệ khoá bị chuyển vị trí tiến sát mức một phần năm tức hai mươi phần trăm."
        ),
        "sym_rows": [
            ["<code>with con: ...</code>", "Khối giao dịch nguyên tử SQLite: lỗi hoặc rollback hoàn tác toàn bộ"],
            ["<code>bisect.bisect(ring, h)</code>", "Tìm nút liền kề theo chiều kim đồng hồ trên vòng băm O(log N)"],
            ["<code>CLOSED → OPEN</code>", "Mở cầu dao tức thì sau ngưỡng lỗi liên tiếp để trả về lỗi nhanh"],
        ],
        "sym_say": (
            "Bảng ký hiệu nêu ba mảnh ghép kỹ thuật chính của dự án. "
            "Câu lệnh with kết hợp đối tượng kết nối SQLite tự động chốt hoặc hoàn tác toàn bộ giao dịch. "
            "Tìm kiếm nhị phân trên vòng băm ánh xạ khoá về nút đích nhanh chóng. "
            "Còn máy trạng thái cầu dao chuyển từ đóng sang mở khi đếm đủ số lỗi liên tiếp."
        ),
        "ex_code": (
            "import bisect, hashlib, sqlite3\n"
            "c = sqlite3.connect(':memory:')\n"
            "c.execute('CREATE TABLE ord(id INT)'); c.execute('CREATE TABLE outb(id INT)')\n"
            "with c: c.execute('INSERT INTO ord VALUES(1)'); c.execute('INSERT INTO outb VALUES(1)')\n"
            "no = c.execute('SELECT COUNT(*) FROM ord').fetchone()[0]\n"
            "nx = c.execute('SELECT COUNT(*) FROM outb').fetchone()[0]\n"
            "fail_streak, state = 3, 'CLOSED'\n"
            "if fail_streak >= 3: state = 'OPEN'\n"
            "print(f'outbox_match={int(no == nx)} cb_state={state}')\n"
        ),
        "ex_say": (
            "Đoạn mã cài đặt trực tiếp hai bảng đơn hàng và hộp thư đi trong cùng một cơ sở dữ liệu SQLite. "
            "Khi đơn một thành công, cả hai bảng cùng tăng lên một bản ghi nên luôn khớp nhau. "
            "Ở nhánh dưới, khi bộ đếm lỗi liên tiếp chạm ngưỡng ba lần, cầu dao lập tức chuyển sang trạng thái mở."
        ),
        "ex_out_say": (
            "Kết quả chạy thật chứng nhận cặp bảng khớp một trăm phần trăm và cầu dao đã tự mở đúng lúc. "
            "Nhờ vậy hệ thống không bao giờ làm rớt sự kiện hay đổ thêm tải vào dịch vụ đang hỏng."
        ),
        "chk_code": (
            "import hashlib\n"
            "h = lambda s: int(hashlib.sha256(s.encode()).hexdigest()[:8], 16)\n"
            "def own(n, k):\n"
            "    r = sorted((h(f'n{i}#0'), i) for i in range(n))\n"
            "    idx = sum(x[0] <= h(f'k{k}') for x in r) % n; return r[idx][1]\n"
            "mv = sum(own(4, k) != own(5, k) for k in range(200))\n"
            "print(f'moved_of_200={mv} lt60={int(mv < 60)}')\n"
        ),
        "chk_say": (
            "Phép kiểm chứng thứ hai chạy thử hai trăm khoá qua hàm băm SHA hai trăm năm mươi sáu khi tăng từ bốn lên năm nút. "
            "Vì các nút nằm cố định trên vòng băm theo giá trị băm của chúng nên đa số khoá cũ vẫn trỏ về đúng nút ban đầu."
        ),
        "chk_out_say": (
            "Đầu ra kiểm chứng cho thấy số khoá bị dời nằm gọn dưới sáu mươi trên tổng số hai trăm khoá. "
            "Tỉ lệ này rất thấp do các khoá chỉ chuyển khi rơi vào cung mới của nút thứ năm."
        ),
        "quymo": [
            ("4 nút phân tán", "Băm mod: ~80% dời khi thêm nút 5", "Băm nhất quán: ~20% dời"),
            ("1 000 đơn/s + Outbox", "Tối đa ~1 000 giao dịch SQL/s", "Quét OUTBOX theo lô mỗi 50 ms"),
            ("Dịch vụ đích chậm 5 s", "Không có CB: hết sạch luồng", "CB OPEN < 0,1 ms trả fallback ngay"),
        ],
        "quymo_say": (
            "Bảng quy mô tóm tắt giá trị kiến trúc của từng thành phần khi hệ thống mở rộng nhanh. "
            "Thay vì tái cân bằng gần như toàn bộ bộ nhớ đệm mỗi lần thêm máy, vòng băm giữ được tám mươi phần trăm khoá trúng ngay. "
            "Và cầu dao mở giúp giảm thời gian phản hồi lỗi từ năm giây xuống chưa tới một phần mười mi-li-giây."
        ),
        "pitfalls": [
            "<b>Lỗi 1 (-30đ):</b> Gửi sự kiện ở ngoài phạm vi giao dịch SQL gây lệch giữa đơn và sự kiện.",
            "<b>Lỗi 2 (-20đ):</b> Dùng <code>hash(key)</code> có salt ngẫu nhiên mỗi lần chạy Python làm định tuyến đổi.",
            "<b>Lỗi 3 (-10đ):</b> Chuyển thẳng <code>OPEN → CLOSED</code> mà không thử tải nhẹ qua <code>HALF_OPEN</code>.",
        ],
        "pitfalls_say": (
            "Ba sai lầm kiến trúc cần tránh tuyệt đối trong dự án hệ phân tán Chặng 8 là như sau. "
            "Đầu tiên là đẩy sự kiện ra hàng đợi bên ngoài giao dịch cơ sở dữ liệu dễ gây mất đồng bộ. "
            "Thứ hai là gọi hàm băm dựng sẵn của Python vốn sinh ngẫu nhiên mỗi lần khởi động tiến trình. "
            "Thứ ba là mở lại hoàn toàn lưu lượng về trạng thái đóng mà chưa thăm dò dần."
        ),
        "q_text": "<ol><li>Tại sao phải ghi bảng nghiệp vụ và bảng Outbox trong CÙNG một giao dịch?</li><li>Khi thêm nút thứ 5 vào cụm 4 nút, băm nhất quán lý thuyết chỉ dời khoảng bao nhiêu phần trăm khoá?</li></ol>",
        "q_say": "Hãy kiểm tra lại tư duy phân tán qua hai câu hỏi nhanh sau đây. Câu một, tại sao bắt buộc phải gộp lệnh ghi đơn và ghi Outbox chung một giao dịch? Câu hai, thêm nút thứ năm vào bốn nút theo băm nhất quán thì lý thuyết chỉ dời khoảng mấy phần trăm khoá? Bấm tạm dừng và trả lời.",
        "q_ans1": "Để bảo đảm tính <b>nguyên tử (all-or-nothing)</b>: hoặc lưu cả hai, hoặc hoàn tác cả hai.",
        "q_ans1_say": "Đáp án câu một: vì chỉ khi chung giao dịch mới bảo đảm hoặc cùng lưu hoặc cùng hoàn tác khi gặp sự cố.",
        "q_ans2": "Khoảng <code>1 / 5 = <b>20%</b></code> lượng khoá thay vì 80% như phép chia lấy dư.",
        "q_ans2_say": "Đáp án câu hai: khi thêm một nút vào thành năm nút, chỉ một phần năm lượng khoá tương ứng hai mươi phần trăm bị chuyển giao.",
        "lab_de": "# Dự án PRJ L07 — Đường ống Outbox, Consistent Hashing & Circuit Breaker\n\nViết chương trình Python: (1) ghi 1 đơn thành công và 1 đơn rollback vào cặp bảng SQLite `ord`/`outb`; (2) đếm số khoá trong 500 khoá dời chỗ khi tăng từ 4 lên 5 nút theo SHA-256 trên vòng băm (< 150 khoá); (3) mở ngắt mạch `OPEN` sau 3 lỗi, in đúng 3 dòng:\n1. `outbox_atomic_match=1`\n2. `ch_moved_lt_150=1`\n3. `cb_after_3fails=OPEN`\n\nChấm tự động:\n```bash\nbash labs/cham.sh PRJ L07 duong_dan/bai_cua_ban.py\n```",
        "lab_sol": (
            "import bisect, hashlib, sqlite3\n"
            "c = sqlite3.connect(':memory:')\n"
            "c.execute('CREATE TABLE ord(id INT)'); c.execute('CREATE TABLE outb(id INT)')\n"
            "with c: c.execute('INSERT INTO ord VALUES(1)'); c.execute('INSERT INTO outb VALUES(1)')\n"
            "c.execute('BEGIN'); c.execute('INSERT INTO ord VALUES(2)'); c.execute('INSERT INTO outb VALUES(2)'); c.rollback()\n"
            "eq = c.execute('SELECT COUNT(*) FROM ord').fetchone()[0] == c.execute('SELECT COUNT(*) FROM outb').fetchone()[0]\n"
            "h = lambda s: int(hashlib.sha256(s.encode()).hexdigest()[:8], 16)\n"
            "def own(n, k):\n"
            "    r = sorted((h(f'n{i}#0'), i) for i in range(n))\n"
            "    return r[bisect.bisect(r, (h(f'k{k}'), 99)) % n][1]\n"
            "mv = sum(own(4, k) != own(5, k) for k in range(500))\n"
            "state, fails = 'CLOSED', 0\n"
            "for ok in (False, False, False):\n"
            "    fails = 0 if ok else fails + 1\n"
            "    if fails >= 3:\n"
            "        state = 'OPEN'\n"
            "print(f'outbox_atomic_match={int(eq)}')\nprint(f'ch_moved_lt_150={int(mv < 150)}')\nprint(f'cb_after_3fails={state}')\n"
        ),
        "chain": ["SQLite Outbox 1 TX", "Consistent Hashing SHA-256", "Circuit Breaker 3 trạng thái"],
    },
    {
        "id": "L08",
        "fname": "L08_du_an_chang_9_phan_loai_do_do.yaml",
        "title": "Bài 8 — Dự án Chặng 9 — Đường ống phân loại & đo độ lệch ECE",
        "obj": [
            "Cài độ đo Precision, Recall, F1 trên ma trận nhầm lẫn từ dữ liệu dự đoán",
            "Tính độ lệch hiệu chuẩn kỳ vọng ECE phát hiện mô hình tự tin thái quá",
            "Kiểm tra bẫy chia dữ liệu rò rỉ trước bước chuẩn hoá thang đo",
        ],
        "prereq": [
            ("Tối ưu hàm mất mát & softmax (CS115/MLP)", "Chuyển logit thành xác suất chuẩn hoá tổng bằng 1"),
            ("Độ chuẩn xác, độ phủ & ranking (IRS/DAN)", "Đo chất lượng phân loại trên tập lệch nhãn"),
            ("Giám sát trôi lệch & đánh giá RAG/LLM (MLO/LLM)", "Kiểm chứng hiệu chuẩn xác suất và rò rỉ tập kiểm tra"),
        ],
        "prereq_say": (
            "Dự án Chặng 9 tổng hợp các mảnh ghép cốt lõi từ toán học máy, khoa học dữ liệu và vận hành mô hình. "
            "Thứ nhất là xử lý đầu ra xác suất từ các bộ phân loại tuyến tính hoặc mạng nơ-ron. "
            "Thứ hai là đo lường chuẩn xác, độ phủ và chỉ số F1 trên bài toán phân loại mất cân bằng. "
            "Thứ ba là kiểm định sai số hiệu chuẩn để biết xác suất mô hình báo có đáng tin cậy không."
        ),
        "svg_boxes": [("Dự đoán vs Nhãn", "TP, FP, FN, TN"), ("Precision & Recall", "F1 = 2PR / (P+R)"), ("Kiểm định ECE", "Lệch tin cậy giữa giỏ")],
        "svg_say": (
            "Hình minh họa ba bước đánh giá bắt buộc cho mọi mô hình phân loại thực tế. "
            "Bước một gom đếm đúng sai từ ma trận nhầm lẫn. "
            "Bước hai cân đối độ chuẩn xác và độ phủ qua trung bình điều hòa F1. "
            "Bước ba chia giỏ xác suất để đo sai số hiệu chuẩn kỳ vọng ECE."
        ),
        "hook_say": (
            "Chào bạn đến với dự án chốt Chặng 9 về trí tuệ nhân tạo và học máy. "
            "Độ chính xác tổng thể chín mươi chín phần trăm trên bài toán gian lận chỉ chiếm một phần trăm là con số đánh lừa, vì mô hình đoán toàn âm cũng đạt mức đó. "
            "Ngay cả khi F1 khá tốt, một mô hình dự báo xác suất chín mươi phần trăm nhưng thực tế chỉ đúng bảy mươi phần trăm sẽ làm sai mọi quyết định đặt ngưỡng rủi ro. "
            "Hôm nay ta cài trọn vẹn bộ đánh giá F1 và chỉ số hiệu chuẩn ECE bằng Python thuần."
        ),
        "hook_txt": "Với ma trận <code>TP=4, FP=1, FN=2, TN=13</code>: đạt <code>Precision = <b>0,80</b></code>, <code>Recall = <b>0,67</b></code>, <code>F1 = <b>0,73</b></code> và đo <code>ECE = <b>0,15</b></code> khi mô hình lệch 15% tin cậy ở 2 giỏ.",
        "hook_chk": ["4 / (4 + 1) == 0.8", "round(0.5 * 0.1 + 0.5 * 0.2, 2) == 0.15"],
        "formula_txt": "<p><b>1. Precision &amp; Recall:</b> <code>P = TP/(TP+FP) = 4/5 = 0,80</code>; <code>R = TP/(TP+FN) = 4/6 = 0,67</code>.</p><p><b>2. F1 &amp; ECE:</b> <code>F1 = 2PR/(P+R) = <b>0,727</b></code>; <code>ECE = sum((n_b/N)|acc_b - conf_b|)</code>.</p>",
        "formula_say": (
            "Hai công thức này bảo vệ hệ thống AI khỏi bẫy đánh giá bề mặt. "
            "Chỉ số F1 dùng trung bình điều hòa nên kéo kết quả về gần giá trị nhỏ hơn trong hai đại lượng chuẩn xác và độ phủ. "
            "Vì vậy mô hình không thể đánh đổi bỏ sót một nửa số ca bệnh để đạt độ chuẩn xác cao giả tạo. "
            "Còn ECE lấy trung bình có trọng số phần chênh tuyệt đối giữa độ chính xác thật và độ tự tin ở từng giỏ."
        ),
        "sym_rows": [
            ["<code>P = TP / (TP + FP)</code>", "Trong số ca mô hình báo dương, bao nhiêu phần trăm thực sự dương"],
            ["<code>R = TP / (TP + FN)</code>", "Trong số ca dương thật, mô hình tóm được bao nhiêu phần trăm"],
            ["<code>ECE</code>", "Sai số hiệu chuẩn kỳ vọng: chênh lệch giữa xác suất dự báo và thực tế"],
        ],
        "sym_say": (
            "Bảng ký hiệu tóm tắt ba thước đo đánh giá cốt lõi của Chặng 9. "
            "Độ chuẩn xác đo độ sạch của cảnh báo dương tính. "
            "Độ phủ đo khả năng không bỏ sót ca dương tính thật. "
            "Còn ECE đo mức độ trung thực của xác suất dự báo."
        ),
        "ex_code": (
            "tp, fp, fn = 4, 1, 2\n"
            "p = tp / (tp + fp); r = tp / (tp + fn)\n"
            "f1 = 2 * p * r / (p + r)\n"
            "ece = 0.5 * abs(0.80 - 0.90) + 0.5 * abs(0.40 - 0.60)\n"
            "print(f'prec={p:.2f} rec={r:.2f} f1={f1:.2f} ece={ece:.2f}')\n"
        ),
        "ex_say": (
            "Đoạn mã tính trực tiếp cả ba chỉ số từ ma trận nhầm lẫn có bốn ca đúng dương, một báo giả và hai bỏ sót. "
            "Sau đó ta tính trung bình lệch giữa độ chính xác thực và mức tự tin trên hai giỏ có kích thước bằng nhau."
        ),
        "ex_out_say": (
            "Kết quả chạy thật trên Python ra chuẩn xác không phẩy tám, độ phủ không phẩy sáu bảy và F1 đạt không phẩy bảy ba. "
            "Đồng thời ECE bằng không phẩy một lăm cho thấy mô hình tự tin quá mức vì xác suất cao hơn tỉ lệ đúng thật."
        ),
        "chk_code": (
            "bins = [(10, 0.80, 0.90), (10, 0.40, 0.60)]\n"
            "tot = sum(n for n, _, _ in bins)\n"
            "ece = sum((n / tot) * abs(a - c) for n, a, c in bins)\n"
            "print(f'ece_verified={ece:.2f}')\n"
        ),
        "chk_say": (
            "Ở phép kiểm chứng độc lập, ta tổng hợp lại từ số mẫu từng giỏ là mười và mười trên tổng hai mươi mẫu. "
            "Vì hai giỏ chia đều tỉ trọng nên trọng số mỗi giỏ bằng đúng một nửa."
        ),
        "chk_out_say": (
            "Đầu ra kiểm chứng ra đúng không phẩy một lăm trùng với tính tay vì hai giỏ chia đều trọng số một nửa. "
            "Nhờ kiểm định hiệu chuẩn này ta biết cần hiệu chỉnh nhiệt độ trước khi đưa vào sản xuất."
        ),
        "quymo": [
            ("20 mẫu thử nhanh", "2 giỏ tin cậy", "Phát hiện nhanh sai lệch 15%"),
            ("50 000 bản ghi prod", "10 giỏ đều 0..1", "Đo chính xác độ trôi ECE theo tuần"),
            ("Dữ liệu mất cân bằng 1%", "Accuracy ảo 99%", "F1 vạch trần mô hình đoán toàn âm"),
        ],
        "quymo_say": (
            "Bảng quy mô đối chiếu khi áp dụng thước đo sang dữ liệu thực tế lớn. "
            "Với tập sản xuất năm mươi nghìn mẫu, ta chia mười giỏ đều nhau để vẽ biểu đồ độ tin cậy hàng tuần. "
            "Nếu dữ liệu lệch mạnh một phần trăm, chỉ số F1 lập tức phơi bày mô hình lười đoán toàn âm."
        ),
        "pitfalls": [
            "<b>Lỗi 1 (-30đ):</b> Chuẩn hoá trung bình trên toàn tập gộp trước khi chia Train/Test làm rò rỉ dữ liệu.",
            "<b>Lỗi 2 (-20đ):</b> Báo cáo Accuracy trên bài toán gian lận chỉ chiếm 0,5% dương tính.",
            "<b>Lỗi 3 (-10đ):</b> Tin nguyên điểm Softmax 0,99 là xác suất thật khi chưa kiểm ECE.",
        ],
        "pitfalls_say": (
            "Hãy lưu ý ba sai lầm khiến nhiều mô hình đạt điểm cao khi thử nhưng sụp đổ ngoài thực tế. "
            "Lỗi nặng nhất là tính trung bình và độ lệch chuẩn trên toàn bộ dữ liệu rồi mới chia tập kiểm thử gây rò rỉ thông tin. "
            "Thứ hai là báo cáo accuracy trên tập lệch nhãn. "
            "Thứ ba là tin tuyệt đối vào xác suất thô của lớp cuối mà bỏ qua bước kiểm ECE."
        ),
        "q_text": "<ol><li>Khi <code>TP = 4, FP = 1, FN = 2</code> thì Precision và Recall bằng bao nhiêu?</li><li>Vì sao phải khớp bộ chuẩn hoá (scaler) chỉ trên tập Train chứ không trên toàn tập?</li></ol>",
        "q_say": "Mời bạn tự kiểm tra kiến thức dự án Chặng 9 với hai câu hỏi nhanh. Câu một, với TP bốn, FP một và FN hai thì Precision và Recall bằng bao nhiêu? Câu hai, vì sao chỉ khớp bộ chuẩn hoá trên tập huấn luyện chứ không trên toàn dữ liệu? Bấm tạm dừng và trả lời.",
        "q_ans1": "<code>Precision = 4 / 5 = <b>0,80</b></code>; <code>Recall = 4 / 6 ≈ <b>0,67</b></code>.",
        "q_ans1_say": "Đáp án câu một: độ chuẩn xác bằng bốn chia năm là không phẩy tám mươi, còn độ phủ bằng bốn chia sáu xấp xỉ không phẩy sáu bảy.",
        "q_ans2": "Để tránh <b>rò rỉ dữ liệu (data leakage)</b> thông tin phân phối tập Test vào quá trình huấn luyện.",
        "q_ans2_say": "Đáp án câu hai: nhằm ngăn rò rỉ thông tin thống kê từ tập kiểm thử làm sai lệch đánh giá mô hình.",
        "lab_de": "# Dự án PRJ L08 — Bộ đánh giá phân loại F1 & sai số hiệu chuẩn ECE\n\nViết chương trình Python tính `Precision`, `Recall`, `F1` cho `TP=4, FP=1, FN=2` và `ECE` cho 2 giỏ bằng nhau `[(acc=0.80, conf=0.90), (acc=0.40, conf=0.60)]`, in đúng 3 dòng:\n1. `precision=0.80 recall=0.67`\n2. `f1=0.73`\n3. `ece=0.15`\n\nChấm tự động:\n```bash\nbash labs/cham.sh PRJ L08 duong_dan/bai_cua_ban.py\n```",
        "lab_sol": (
            "tp, fp, fn = 4, 1, 2\n"
            "p = tp / (tp + fp); r = tp / (tp + fn); f1 = 2 * p * r / (p + r)\n"
            "ece = 0.5 * abs(0.80 - 0.90) + 0.5 * abs(0.40 - 0.60)\n"
            "print(f'precision={p:.2f} recall={r:.2f}')\n"
            "print(f'f1={f1:.2f}')\nprint(f'ece={ece:.2f}')\n"
        ),
        "chain": ["Confusion Matrix TP/FP/FN", "F1 điều hòa", "Hiệu chuẩn ECE & chống leak"],
    },
    {
        "id": "L09",
        "fname": "L09_du_an_chang_10_kiem_chung_hinh_thuc.yaml",
        "title": "Bài 9 — Dự án Chặng 10 — Kiểm chứng DFA, Amdahl & sai số tích lũy",
        "obj": [
            "Cài máy DFA nhận diện chính xác chuỗi kết thúc bằng 'ab' trên bảng chữ cái {a, b}",
            "Tính bước tăng tốc Amdahl ở 8 nhân và chứng minh trần phần tuần tự",
            "Phân tích lỗi tràn tích lũy nhị phân kiểu Patriot 1991 trên đồng hồ hệ thống",
        ],
        "prereq": [
            ("Ôtômat hữu hạn đơn định DFA (TOC)", "Chuyển trạng thái tất định mỗi ký tự O(1)"),
            ("Trình biên dịch AST & song song (PLC/PAR)", "Tính biên tăng tốc Amdahl khi phần tuần tự chặn trần"),
            ("Công bằng, HCI & hậu kiểm sự cố (SEP/HCI/CAS)", "Kiểm chứng tỉ lệ dương giữa hai nhóm và sai số dấu phẩy động"),
        ],
        "prereq_say": (
            "Dự án Chặng 10 kết nối kiến thức chuyên gia từ lý thuyết tính toán, song song hoá và bài học hậu kiểm các sự cố lịch sử. "
            "Thứ nhất là dùng ôtômat đơn định để khớp chuỗi trong thời gian tuyến tính tránh treo biểu thức quay lui. "
            "Thứ hai là dùng định luật Amdahl tính trần tăng tốc thực tế khi thêm nhân bộ xử lý. "
            "Thứ ba là dùng bài học lỗi dấu phẩy động không phẩy một giây để thiết kế bộ đếm thời gian bằng số nguyên."
        ),
        "svg_boxes": [("DFA nhận 'ab'", "3 trạng thái q0→q1→q2"), ("Amdahl 8 nhân", "Trần phần tuần tự"), ("Kiểm sai số Patriot", "Tích lũy 0,1 s × 3 600 000")],
        "svg_say": (
            "Ba khối kiểm chứng dự án Chặng 10 phối hợp chặt với nhau. "
            "Khối một duyệt chuỗi từng ký tự trên máy ba trạng thái mà không bao giờ quay lui. "
            "Khối hai đánh giá hiệu suất thực tế theo tỉ lệ phần tuần tự. "
            "Khối ba đối chiếu sai số tích lũy nhị phân với phép đếm nguyên chính xác."
        ),
        "hook_say": (
            "Chào bạn đến với dự án chốt Chặng 10 tổng hợp kiến thức nền sâu và điều tra sự cố thật. "
            "Năm 2019 một biểu thức chính quy quay lui từng làm sập toàn mạng Cloudflare chỉ trong vài giây, còn năm 1991 sai số tích lũy một phần mười giây làm trượt tên lửa Patriot. "
            "Cùng lúc đó việc mua thêm hàng trăm nhân xử lý vẫn vô nghĩa nếu phần tuần tự còn mười phần trăm. "
            "Hôm nay ta cài trọn vẹn bộ máy DFA tuyến tính và mô hình kiểm trần Amdahl bằng Python."
        ),
        "hook_txt": "DFA 3 trạng thái duyệt chuỗi độ dài <code>n</code> trong <b>O(n)</b> thời gian tuyến tính, định luật Amdahl chỉ ra với <b>10%</b> phần tuần tự thì chạy 8 nhân chỉ nhanh gấp <b>4,71</b> lần, và sai số cộng lặp 24 bit sau 100 giờ gây lệch <b>0,34 s</b>.",
        "hook_chk": ["round(1 / (0.1 + 0.9 / 8), 2) == 4.71", "1 / 0.1 == 10.0"],
        "formula_txt": "<p><b>1. DFA kết thúc 'ab':</b> chuyển tiếp <code>q0 --a--&gt; q1 --b--&gt; q2(accept)</code>, nhận đúng chuỗi kết thúc 'ab'.</p><p><b>2. Luật Amdahl:</b> <code>S(N) = 1 / ((1 - p) + p/N)</code>; khi <code>p = 0,90, N = 8</code> cho <code>S = <b>4,71</b></code>.</p>",
        "formula_say": (
            "Hai công thức này đặt ranh giới cứng về thời gian xử lý và mở rộng song song. "
            "Với ôtômat đơn định, mỗi ký tự đầu vào chỉ kích hoạt đúng một lần nhảy bảng trạng thái nên thời gian luôn tỉ lệ bậc nhất theo độ dài chuỗi. "
            "Với luật Amdahl, phần song song dù chia cho vô hạn nhân thì mẫu số vẫn còn nguyên phần tuần tự không phẩy một nên trần tăng tốc tối đa chỉ là mười."
        ),
        "sym_rows": [
            ["<code>st = delta[st][ch]</code>", "Hàm chuyển trạng thái đơn định, không quay lui (0 quay lui ReDoS)"],
            ["<code>1 / ((1 - p) + p/N)</code>", "Hệ số tăng tốc Amdahl khi có N nhân với tỉ lệ song song p"],
            ["<code>int tick</code>", "Đếm tick nguyên tránh trôi số thực 0,1 lặp lại hàng triệu lần"],
        ],
        "sym_say": (
            "Bảng ký hiệu tổng hợp ba khái niệm kỹ thuật then chốt trong dự án Chặng 10. "
            "Hàm chuyển đơn định đọc một ký tự đi một bước không bao giờ quay đầu. "
            "Biểu thức Amdahl đo giới hạn tăng tốc song song thực tế. "
            "Còn bộ đếm số nguyên giữ đồng hồ hệ thống không bị sai số tích lũy như nhị phân dấu phẩy động."
        ),
        "ex_code": (
            "def dfa(s):\n"
            "    st = 0\n"
            "    for ch in s:\n"
            "        st = 1 if ch == 'a' else (2 if st == 1 else 0)\n"
            "    return int(st == 2)\n"
            "amd8 = 1.0 / (0.10 + 0.90 / 8.0)\n"
            "print(f'accept_aaab={dfa(\"aaab\")} reject_aba={dfa(\"aba\")} amdahl_8={amd8:.2f}')\n"
        ),
        "ex_say": (
            "Đoạn mã cài đặt trực tiếp ôtômat ba trạng thái chỉ dùng bốn dòng vòng lặp đơn giản. "
            "Khi gặp ký tự a máy chuyển sang trạng thái chờ một, và chỉ vào trạng thái chấp nhận hai nếu trước b đúng là trạng thái một. "
            "Tiếp theo chương trình tính trực tiếp hệ số tăng tốc ở tám nhân cho bài toán chín mươi phần trăm song song."
        ),
        "ex_out_say": (
            "Kết quả chạy thật chứng minh chuỗi kết thúc a b trả về một, còn chuỗi a b a trả không vì không kết thúc bằng b sau a. "
            "Đồng thời hệ số Amdahl xuất đúng bốn phẩy bảy một."
        ),
        "chk_code": (
            "def dfa(s):\n"
            "    st = 0\n"
            "    for ch in s:\n"
            "        if ch not in ('a', 'b'): return 0\n"
            "        st = 1 if ch == 'a' else (2 if st == 1 else 0)\n"
            "    return int(st == 2)\n"
            "cases = ['', 'ab', 'aab', 'b', 'ba', 'abb']\n"
            "ok = all(dfa(w) == int(w.endswith('ab')) for w in cases)\n"
            "print(f'dfa_matches_spec={int(ok)} inf_limit={1.0/0.10:.1f}')\n"
        ),
        "chk_say": (
            "Ở nhánh kiểm chứng, ta quét sáu trường hợp biên gồm chuỗi rỗng, đuôi đúng, lặp hai chữ a và dư chữ b phía cuối. "
            "Ta gọi trực tiếp hàm DFA vừa cài rồi đối chiếu từng kết quả với đặc tả kết thúc bằng a b vì cần chắc chắn không lệch biên nào."
        ),
        "chk_out_say": (
            "Đầu ra xác nhận DFA khớp toàn bộ ca thử, còn trần vô hạn nhân chốt tại mười lần vì phần tuần tự bằng không phẩy một. "
            "Phép kiểm chứng này khép lại phần kiểm đúng hình thức."
        ),
        "quymo": [
            ("Chuỗi 10 ký tự", "10 bước chuyển trạng thái", "Tức thì"),
            ("1 000 000 ký tự", "Đúng 1 000 000 bước O(n)", "Không quay lui ReDoS"),
            ("Đám mây 1 000 nhân (s=10%)", "Tăng tốc chỉ 9,91x", "Lãng phí >99% tiền mua nhân"),
        ],
        "quymo_say": (
            "Bảng quy mô cho thấy rõ sức mạnh của máy trạng thái và giới hạn phần cứng song song. "
            "Dù chuỗi dài một triệu ký tự, DFA chỉ duyệt một vòng thẳng trong vài chục mi-li-giây thay vì treo vì quay lui. "
            "Còn chạy một nghìn nhân khi phần tuần tự chiếm mười phần trăm sẽ lãng phí quá chín mươi chín phần trăm tài nguyên."
        ),
        "pitfalls": [
            "<b>Lỗi 1 (-30đ):</b> Nhầm trạng thái từ <code>q1</code> gặp <code>'a'</code> phải giữ nguyên <code>q1</code> chứ không về <code>q0</code>.",
            "<b>Lỗi 2 (-20đ):</b> Quên phần tuần tự khi kỳ vọng mở rộng 100 nhân sẽ nhanh gấp 100 lần.",
            "<b>Lỗi 3 (-10đ):</b> Dùng số thực 0,1 cộng lặp làm bộ đếm thời gian thay vì đếm số nguyên tick.",
        ],
        "pitfalls_say": (
            "Bạn rà kỹ ba cái bẫy sau trước khi hoàn thiện bài dự án Chặng 10. "
            "Đầu tiên ở DFA, khi đang thấy chữ a tại q một mà gặp thêm chữ a mới, ta phải giữ nguyên ở q một vì chữ a mới vẫn mở đầu cho đuôi a b. "
            "Thứ hai là tính sai kỳ vọng tăng tốc song song do bỏ quên nút cổ chai tuần tự. "
            "Thứ ba là cộng dồn số thực không phẩy một gây trôi đồng hồ dài hạn."
        ),
        "q_text": "<ol><li>Nếu DFA đang ở <code>q1</code> (vừa thấy 'a') mà gặp tiếp 'a', trạng thái mới nên là gì?</li><li>Với phần tuần tự 10%, tăng tốc tối đa khi có vô hạn nhân là bao nhiêu?</li></ol>",
        "q_say": "Bạn kiểm tra lại kiến thức cốt lõi bằng hai câu hỏi ngắn sau. Câu một, nếu máy trạng thái ở q một gặp tiếp chữ a thì chuyển về trạng thái nào? Câu hai, phần tuần tự mười phần trăm thì trần tăng tốc tối đa là bao nhiêu lần? Bấm tạm dừng và trả lời.",
        "q_ans1": "Giữ nguyên ở <code><b>q1</b></code> vì chữ 'a' mới có thể là đầu của đuôi 'ab'.",
        "q_ans1_say": "Đáp án câu một: giữ nguyên ở q một vì chữ a vừa gặp có thể ghép với chữ b ngay sau đó thành a b.",
        "q_ans2": "Giới hạn trên bằng <code>1 / 0,10 = <b>10 lần</b></code>.",
        "q_ans2_say": "Đáp án câu hai: mức tăng tốc tối đa bị chặn ở một chia không phẩy một tức mười lần.",
        "lab_de": "# Dự án PRJ L09 — Bộ kiểm DFA 'ab' & tính trần song song Amdahl\n\nViết chương trình Python cài DFA 3 trạng thái nhận đúng các chuỗi chỉ chứa `'a','b'` kết thúc bằng `'ab'`, kiểm trên `\"aaab\"` và `\"aba\"`, và tính tăng tốc Amdahl `p=0.90` ở `8` nhân, in đúng 3 dòng:\n1. `dfa_aaab=1 dfa_aba=0`\n2. `amdahl_8cores=4.71`\n3. `amdahl_inf=10.00`\n\nChấm tự động:\n```bash\nbash labs/cham.sh PRJ L09 duong_dan/bai_cua_ban.py\n```",
        "lab_sol": (
            "def dfa(s):\n"
            "    st = 0\n"
            "    for ch in s:\n"
            "        if ch not in ('a', 'b'): return 0\n"
            "        st = 1 if ch == 'a' else (2 if st == 1 else 0)\n"
            "    return int(st == 2)\n"
            "print(f'dfa_aaab={dfa(\"aaab\")} dfa_aba={dfa(\"aba\")}')\n"
            "print(f'amdahl_8cores={1.0 / (0.10 + 0.90 / 8.0):.2f}')\n"
            "print(f'amdahl_inf={1.0 / 0.10:.2f}')\n"
        ),
        "chain": ["DFA O(n) 0 quay lui", "Amdahl 1/(s + p/N)", "Đếm tick nguyên tránh trôi 0,1"],
    },
    {
        "id": "L10",
        "fname": "L10_du_an_chang_11_pid_merkle.yaml",
        "title": "Bài 10 — Dự án Chặng 11 — Điều khiển PID & cây Merkle toàn vẹn",
        "obj": [
            "Mô phỏng bộ điều khiển vòng kín bám mục tiêu và đánh giá biên độ sai số",
            "Xây gốc Merkle SHA-256 cho 4 giao dịch và phát hiện sửa 1 giao dịch tức thì",
            "Kiểm tra điều kiện lập lịch thời gian thực RMS dưới biên Liu-Layland",
        ],
        "prereq": [
            ("Toán chuyển động & điều khiển PID (RBM/ROB)", "Tỉ lệ Kp nhân sai số e = target - x kéo hệ bám đích (rút gọn từ PID)"),
            ("Lập lịch thời gian thực RMS (ESY)", "Kiểm tra hệ số sử dụng CPU nhỏ hơn biên Liu-Layland"),
            ("Cấu trúc băm chuỗi khối & cây Merkle (BCH)", "Gộp cặp băm theo cây nhị phân để chứng minh toàn vẹn O(log N)"),
        ],
        "prereq_say": (
            "Dự án chốt Chặng 11 hợp nhất ba lĩnh vực chuyên ngành từ robot tự hành, hệ nhúng tới công nghệ chuỗi khối. "
            "Thứ nhất là vòng điều khiển phản hồi dùng sai số để điều chỉnh cơ cấu chấp hành bám dần về mục tiêu. "
            "Thứ hai là kiểm biên lập lịch đơn điệu theo tần suất bảo đảm tác vụ thời gian thực luôn kịp hạn chót. "
            "Thứ ba là xây dựng gốc cây băm Merkle kiểm chứng mọi sửa đổi dữ liệu trong lô."
        ),
        "svg_boxes": [("Vòng kín PID", "Giảm sai số về 0"), ("Lập lịch RMS", "U <= N*(2^(1/N)-1)"), ("Cây Merkle 4 lá", "Đổi 1 lá → đổi gốc")],
        "svg_say": (
            "Sơ đồ dự án tổng hợp ba mô-đun chạy nối tiếp bảo đảm cả điều khiển lẫn toàn vẹn dữ liệu. "
            "Bộ điều khiển vòng kín thu hẹp sai số từng bước tiến về giá trị đặt. "
            "Khối lập lịch kiểm hệ số sử dụng dưới ngưỡng tám mươi hai phẩy tám phần trăm. "
            "Còn cây băm Merkle băm từng cặp giao dịch lên nút gốc duy nhất."
        ),
        "hook_say": (
            "Chào bạn đến với dự án cuối cùng khép lại trọn vẹn mười một chặng học của chương trình. "
            "Trong xe tự hành hoặc hệ nhúng điều khiển công nghiệp, hai yêu cầu sống còn là tác vụ phải đáp ứng kịp hạn thời gian thực và vòng phản hồi không được vọt lố. "
            "Ở tầng sổ cái phân tán, hàng nghìn giao dịch phải được rút gọn thành một gốc băm bất biến duy nhất. "
            "Hôm nay ta cài trọn bộ kiểm lập lịch thời gian thực, vòng điều khiển bám đích và cây băm Merkle SHA hai trăm năm mươi sáu."
        ),
        "hook_txt": "Với hai tác vụ tuần hoàn (chu kỳ T, thời lượng C) là <code>P1=(10,3), P2=(20,5)</code>, tổng sử dụng CPU là <code>0,30 + 0,25 = <b>0,55</b></code> an toàn dưới biên Liu–Layland <code>0,828</code>; đồng thời băm <b>4 lá</b> thành gốc Merkle SHA-256 bảo vệ sổ cái.",
        "hook_chk": ["3 / 10 + 5 / 20 == 0.55", "round(2 * (2 ** 0.5 - 1), 3) == 0.828"],
        "formula_txt": "<p><b>1. Biên Liu–Layland 2 tác vụ:</b> <code>U = C1/T1 + C2/T2 &lt;= 2*(2^(1/2) - 1) ≈ <b>0,828</b></code>.</p><p><b>2. Gốc Merkle:</b> <code>H(H(h0 + h1) + H(h2 + h3))</code> đổi toàn bộ gốc khi sửa 1 bit lá.</p>",
        "formula_say": (
            "Hai công thức nền tảng quyết định tính an toàn cho toàn dự án cuối này. "
            "Với hai tác vụ thời gian thực ưu tiên cố định, tổng tỉ lệ chiếm dụng bộ xử lý nhỏ hơn không phẩy tám hai tám bảo đảm mọi lần chạy đều kịp hạn chót. "
            "Còn gốc cây Merkle ghép băm nhị phân từ lá lên đỉnh giúp một thay đổi một bit ở bất kỳ giao dịch nào cũng làm gốc biến đổi hoàn toàn."
        ),
        "sym_rows": [
            ["<code>U = sum(C_i / T_i)</code>", "Hệ số sử dụng CPU của tập tác vụ tuần hoàn thời gian thực"],
            ["<code>Kp * (target - x)</code>", "Khâu khuếch đại tỉ lệ thu hẹp dần khoảng cách tới đích"],
            ["<code>root = H(n0 + n1)</code>", "Nút gốc Merkle kết tinh toàn vẹn của cả cây giao dịch"],
        ],
        "sym_say": (
            "Bảng ký hiệu giải thích ba công thức cốt lõi trước khi lập trình thật. "
            "Chữ U là tổng tỉ trọng thời gian chạy trên chu kỳ của các tác vụ nhúng. "
            "Hệ số Kp nhân sai số hiện tại tạo tín hiệu kéo hệ thống về điểm đặt. "
            "Và nút gốc Merkle lưu dấu vân tay mật mã của toàn bộ các lá phía dưới."
        ),
        "ex_code": (
            "import hashlib\n"
            "h = lambda b: hashlib.sha256(b).hexdigest()\n"
            "leaves = [h(x.encode()) for x in ('tx0','tx1','tx2','tx3')]\n"
            "n0, n1 = h((leaves[0]+leaves[1]).encode()), h((leaves[2]+leaves[3]).encode())\n"
            "root = h((n0 + n1).encode())\n"
            "u = 3/10 + 5/20; bound = 2 * (2**0.5 - 1)\n"
            "print(f'u={u:.2f} bound={bound:.3f} schedulable={int(u <= bound)}')\n"
            "print(f'merkle_hex_len={len(root)}')\n"
        ),
        "ex_say": (
            "Đoạn mã đầu tiên băm bốn giao dịch thành bốn nút lá rồi ghép cặp tính hai nút giữa và một nút gốc duy nhất. "
            "Đồng thời chương trình tính tổng sử dụng CPU là không phẩy năm lăm để đối chiếu ngay với biên an toàn cho hai tác vụ chia sẻ một bộ xử lý."
        ),
        "ex_out_say": (
            "Đầu ra chạy thật chứng nhận tập tác vụ lập lịch được hoàn toàn vì năm mươi lăm phần trăm nằm sâu dưới ngưỡng tám mươi hai phẩy tám phần trăm. "
            "Gốc băm đạt chuẩn sáu mươi bốn ký tự thập lục phân."
        ),
        "chk_code": (
            "x, tgt = 0.0, 10.0\nfor _ in range(5): x += 0.5 * (tgt - x)\n"
            "print(f'after_5steps={x:.3f} err={tgt - x:.3f}')\n"
        ),
        "chk_say": (
            "Ở phép kiểm chứng thứ hai, ta mô phỏng năm bước điều khiển vòng kín với hệ số khuếch đại một nửa bắt đầu từ không hướng tới mười. "
            "Sau mỗi nhịp, sai số giảm còn một nửa của bước trước đó nên tiệm cận nhanh về mục tiêu."
        ),
        "chk_out_say": (
            "Kết quả đạt chín phẩy sáu tám tám với sai số không phẩy ba một hai. "
            "Đây là giá trị làm tròn ba chữ số từ chín phẩy sáu tám bảy năm và không phẩy ba một hai năm theo quy tắc số chẵn. "
            "Đường bám mượt mà này xác nhận vòng điều khiển ổn định không bị vọt lố."
        ),
        "quymo": [
            ("4 giao dịch", "2 bước băm chiều cao", "Chứng minh dài 2 băm"),
            ("1 024 giao dịch", "10 bước băm chiều cao", "Chứng minh dài 10 băm"),
            ("1 048 576 giao dịch", "20 bước băm chiều cao", "Kiểm chứng tức thì < 0,1 ms"),
        ],
        "quymo_say": (
            "Bảng quy mô giải thích sức mạnh nén bằng chứng của cây Merkle trên sổ cái lớn. "
            "Ngay cả khi một khối chứa hơn một triệu giao dịch, chiều cao cây chỉ đạt đúng hai mươi tầng nên đường kiểm chứng chỉ gồm hai mươi giá trị băm. "
            "Nhờ vậy thiết bị nhúng tài nguyên nhỏ cũng xác minh được giao dịch trong tích tắc."
        ),
        "pitfalls": [
            "<b>Lỗi 1 (-30đ):</b> Hệ số khuếch đại P quá lớn làm hệ robot dao động vọt lố mất ổn định.",
            "<b>Lỗi 2 (-20đ):</b> Xếp tác vụ tuần hoàn vượt biên Liu–Layland mà không mô phỏng thử điểm tới hạn.",
            "<b>Lỗi 3 (-10đ):</b> Nối sai thứ tự cặp con <code>h1 + h0</code> làm sai gốc Merkle.",
        ],
        "pitfalls_say": (
            "Ba lỗi kỹ thuật sau dễ làm dự án chuyên ngành Chặng 11 mất điểm nặng. "
            "Đầu tiên là chỉnh hệ số khuếch đại quá lớn khiến bộ điều khiển bật vượt mục tiêu và dao động mãi không tắt. "
            "Thứ hai là xếp thêm tác vụ nhúng vượt ngưỡng biên thời gian thực làm hệ thống lỡ hạn chót. "
            "Thứ ba là ghép ngược thứ tự cặp con trái phải khi tính băm cha làm gốc cây sai lệch hoàn toàn."
        ),
        "q_text": "<ol><li>Biên Liu–Layland của 2 tác vụ bằng khoảng bao nhiêu phần trăm?</li><li>Cây Merkle 1 024 giao dịch có bao nhiêu tầng băm từ lá lên gốc?</li></ol>",
        "q_say": "Bạn dừng lại trả lời hai câu hỏi chốt hạ chương trình ngay dưới đây. Câu một, ngưỡng sử dụng tối đa Liu Layland cho hai tác vụ bằng khoảng mấy phần trăm? Câu hai, cây Merkle gồm một nghìn không trăm hai tư giao dịch có mấy tầng băm từ lá lên gốc? Bấm tạm dừng và trả lời.",
        "q_ans1": "Bằng <code>2*(sqrt(2) - 1) ≈ <b>82,8%</b></code>.",
        "q_ans1_say": "Đáp án câu một: bằng hai nhân căn bậc hai của hai trừ một, xấp xỉ tám mươi hai phẩy tám phần trăm.",
        "q_ans2": "Vì <code>2^10 = 1 024</code> nên cây có đúng <code><b>10</b> tầng</code> từ lá lên gốc.",
        "q_ans2_say": "Đáp án câu hai: do hai mũ mười bằng một nghìn không trăm hai mươi bốn nên chiều cao cây đúng mười tầng băm.",
        "lab_de": "# Dự án PRJ L10 — Tổng hợp Chặng 11: PID, lập lịch RMS & cây Merkle\n\nViết chương trình Python: (1) tính hệ số CPU `U = 3/10 + 5/20 = 0.55` và kiểm dưới biên Liu-Layland 2 tác vụ `0.828`; (2) chạy 5 bước điều khiển tỉ lệ `Kp=0.5` từ `x=0` hướng tới `target=10`; (3) xây gốc Merkle SHA-256 từ 4 lá `'tx0'..'tx3'` và chứng minh sửa `'tx2'` thành `'tx2*'` làm đổi gốc, in đúng 3 dòng:\n1. `rms_u=0.55 schedulable=1`\n2. `pid_step5=9.688`\n3. `merkle_tamper_detected=1`\n\nChấm tự động:\n```bash\nbash labs/cham.sh PRJ L10 duong_dan/bai_cua_ban.py\n```",
        "lab_sol": (
            "import hashlib\n"
            "h = lambda b: hashlib.sha256(b.encode()).hexdigest()\n"
            "def merkle(xs):\n    hs = [h(x) for x in xs]\n    return h(h(hs[0]+hs[1]) + h(hs[2]+hs[3]))\n"
            "u = 3/10 + 5/20; x = 0.0\nfor _ in range(5): x += 0.5 * (10.0 - x)\n"
            "r1 = merkle(['tx0','tx1','tx2','tx3']); r2 = merkle(['tx0','tx1','tx2*','tx3'])\n"
            "print(f'rms_u={u:.2f} schedulable={int(u <= 2*(2**0.5-1))}')\n"
            "print(f'pid_step5={x:.3f}')\nprint(f'merkle_tamper_detected={int(r1 != r2)}')\n"
        ),
        "chain": ["Vòng phản hồi PID", "Biên RMS Liu–Layland", "Cây băm Merkle O(log N)"],
    },
]

sc_path = ROOT / "audit" / "review" / "screen_code" / "PRJ.yaml"
existing_sc = yaml.safe_load(sc_path.read_text(encoding="utf-8")) or {}
ledger = dict(existing_sc.get("blocks") or {})

cur_p = ROOT / "curriculum" / "prj.yaml"
cur_raw = yaml.safe_load(cur_p.read_text(encoding="utf-8"))
cur_ids = {l["id"]: l for l in cur_raw["lessons"]}
changed_cur = False
want = {a.upper() for a in sys.argv[1:]}
for cfg in PROJECTS:
    lid = cfg["id"]
    if want and lid not in want:
        continue
    if lid not in cur_ids:
        cur_raw["lessons"].append({
            "id": lid,
            "title": cfg["title"].split("—", 1)[-1].strip(),
            "spec": f"lessons/prj/{cfg['fname']}",
            "requires": [f"L{int(lid[1:])-1:02d}"],
            "objectives": cfg["obj"],
            "example": f"Dự án chốt {lid} kiểm thử tự động 100 điểm qua labs/cham.sh",
            "fix": ["Tách mã nghiệm thu dự án rõ ràng từng bước và bảo toàn bất biến"],
        })
        changed_cur = True
if changed_cur:
    cur_p.write_text(yaml.safe_dump(cur_raw, allow_unicode=True, sort_keys=False, width=120), encoding="utf-8", newline="\n")

want = {a.upper() for a in sys.argv[1:]}
for cfg in PROJECTS:
    lid = cfg["id"]
    if want and lid not in want:
        continue
    out_p = ROOT / "lessons" / "prj" / cfg["fname"]
    ldir = ROOT / "labs" / "PRJ" / lid
    ldir.mkdir(parents=True, exist_ok=True)
    sol_code = cfg["lab_sol"].strip("\n") + "\n"
    r = subprocess.run([ak.VENV_PY, "-B", "-c", sol_code], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
    if r.returncode != 0:
        raise RuntimeError(f"lab {lid} failed: {r.stderr}")
    lab_out = r.stdout.strip()
    (ldir / "de.md").write_text(cfg["lab_de"].strip() + "\n", encoding="utf-8", newline="\n")
    (ldir / "loi_giai.py").write_text(sol_code, encoding="utf-8", newline="\n")
    (ldir / "mong_doi.txt").write_text(lab_out + "\n", encoding="utf-8", newline="\n")

    chk = subprocess.run([ak.BASH_EXE, str(ROOT / "labs" / "cham.sh"), "PRJ", lid, str(ldir / "loi_giai.py")],
                         cwd=ROOT, env=ak._tool_env(), capture_output=True, text=True, encoding="utf-8")
    if chk.returncode != 0 or chk.stdout.strip() != "ĐÚNG":
        raise RuntimeError(f"cham PRJ {lid} failed: {chk.stdout} {chk.stderr}")

    ex_r = subprocess.run([ak.VENV_PY, "-B", "-c", cfg["ex_code"]], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
    if ex_r.returncode != 0:
        raise RuntimeError(f"ex {lid}: {ex_r.stderr}")
    ex_out = ex_r.stdout.strip()

    chk_r = subprocess.run([ak.VENV_PY, "-B", "-c", cfg["chk_code"]], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
    if chk_r.returncode != 0:
        raise RuntimeError(f"chk {lid}: {chk_r.stderr}")
    chk_out = chk_r.stdout.strip()

    pre_rows = [[a, b] for a, b in cfg["prereq"]]
    b1, b2, b3 = cfg["svg_boxes"]
    svg = ak.svg_wrap(960, 170, (
        ak.svg_rect(40, 35, 250, 90, b1[0], b1[1], ak.C_BLUE) +
        ak.svg_arrow(290, 80, 350, 80, "bước 1") +
        ak.svg_rect(350, 35, 250, 90, b2[0], b2[1], ak.C_GREEN) +
        ak.svg_arrow(600, 80, 660, 80, "bước 2") +
        ak.svg_rect(660, 35, 260, 90, b3[0], b3[1], ak.C_AMBER)
    ))
    qm_rows = [[a, b, c] for a, b, c in cfg["quymo"]]
    pit_body = "<div class='box warn'>" + "<br>".join(cfg["pitfalls"]) + "</div>"
    lab_lines = lab_out.splitlines()
    cmd = f"bash labs/cham.sh PRJ {lid} duong_dan/bai_cua_ban.py"
    prac_rows = [
        ["<b>Đề bài</b>", f"Mở <code>labs/PRJ/{lid}/de.md</code> và cài đặt Python"],
        ["<b>Kiểm chứng</b>", f"Đầu ra chuẩn {len(lab_lines)} dòng khớp 100% qua cham.sh"],
        ["<b>Lệnh chấm</b>", f"<code>{ak.esc(cmd)}</code>"],
    ]

    scenes = [
        ak.sc("hook", "hook", cfg["title"].split("—")[-1].strip()[:58], [
            ak.st_auto(ak.box(f"<p>{cfg['hook_txt']}</p>", "key"), cfg["hook_say"], clear=True),
        ], checks=cfg["hook_chk"]),
        ak.sc("prereq", "prereq", "Ghép kiến thức cốt lõi của chặng", [
            ak.st_auto(ak.table(["mảnh ghép chặng", "vai trò trong dự án"], pre_rows), cfg["prereq_say"], clear=True),
        ]),
        ak.sc("sym", "symbol", "Quy chuẩn kỹ thuật dự án", [
            ak.st_auto(ak.table(["kỹ thuật / hàm cốt lõi", "vai trò cài đặt"], cfg["sym_rows"]), cfg["sym_say"], clear=True),
        ]),
        ak.sc("intuition", "intuition", "Luồng xử lý tổng thể", [
            ak.st_auto(svg, cfg["svg_say"], clear=True),
        ]),
        ak.sc("formula", "formula", "Công thức và bất biến toán học", [
            ak.st_auto(ak.box(cfg["formula_txt"], "key"), cfg["formula_say"], clear=True),
        ], checks=cfg["hook_chk"]),
        ak.sc("example", "example", "Chạy thật mô-đun cốt lõi của dự án", [
            ak.st_auto(ak.code_block(cfg["ex_code"], "Chạy thử nghiệm bằng Python"), cfg["ex_say"], clear=True),
            ak.st_auto(ak.out_block(ex_out, "Đầu ra chạy thật (Python)"), cfg["ex_out_say"], clear=True),
        ], checks=cfg["hook_chk"]),
        ak.sc("check", "check", "Đối chứng kiểm thử độc lập", [
            ak.st_auto(ak.code_block(cfg["chk_code"], "Phép kiểm chứng thứ hai"), cfg["chk_say"], clear=True),
            ak.st_auto(ak.out_block(chk_out, "Đầu ra kiểm chứng"), cfg["chk_out_say"], clear=True),
        ], checks=cfg["hook_chk"]),
        ak.sc("quymo", "example", "Quy mô tải và điểm nghẽn mở rộng", [
            ak.st_auto(ak.table(["quy mô", "tải tính toán", "khuyến nghị kiến trúc"], qm_rows), cfg["quymo_say"], clear=True),
        ], checks=cfg["hook_chk"]),
        ak.sc("pitfalls", "pitfall", "Ba lỗi làm mất điểm khi nghiệm thu", [
            ak.st_auto(ak.table(["cảnh báo lỗi thường gặp khi làm dự án"], [[pit_body]]), cfg["pitfalls_say"], clear=True),
        ]),
        ak.sc("quiz", "quiz", "Kiểm tra nhanh trước khi tự cài đặt", [
            ak.st_auto(cfg["q_text"], cfg["q_say"], pause=20, clear=True),
            ak.st_auto(ak.table(["đáp án câu 1"], [[f"<p>① {cfg['q_ans1']}</p>"]]), cfg["q_ans1_say"], clear=True),
            ak.st_auto(ak.table(["đáp án câu 2"], [[f"<p>② {cfg['q_ans2']}</p>"]]), cfg["q_ans2_say"], clear=True),
        ], checks=cfg["hook_chk"]),
        ak.sc("practice", "practice", "Tự làm dự án và chấm tự động", [
            ak.st_auto(ak.table([f"Thực hành PRJ:{lid}", "Hướng dẫn tự làm và chấm tự động"], prac_rows),
                       "Bây giờ đến phần bạn tự thực hành và chấm điểm trực tiếp trên máy. Bạn mở đề bài, tự viết lời giải vào tệp riêng rồi chạy lệnh chấm để đối chiếu từng dòng kết quả. Hãy bấm tạm dừng và tự làm trước.",
                       pause=30, clear=True),
            ak.st_auto(ak.out_block(lab_out, f"Kết quả mong đợi cần khớp 100% ({len(lab_lines)} dòng)"),
                       "Màn hình hiển thị toàn bộ các dòng kết quả mong đợi mà chương trình của bạn phải in ra khớp từng ký tự.",
                       clear=True),
        ], lab=f"labs/PRJ/{lid}"),
        ak.sc("recap", "recap", "Tổng kết bất biến dự án", [
            ak.st_auto('<div class="chain">' + '<span class="a">→</span>'.join(f'<span class="n">{x}</span>' for x in cfg["chain"]) + '</div>',
                       "Chuỗi tổng kết nối ba mảnh ghép vừa cài đặt thành năng lực thực thi hoàn chỉnh cho dự án chặng này.", clear=True),
            ak.st_auto(ak.box(f"<b>Hoàn thành PRJ:{lid}:</b> sẵn sàng sang chặng tiếp theo.", "ok"),
                       "Chúc mừng bạn hoàn tất trọn vẹn bài dự án và vượt qua kiểm thử tự động.", clear=True),
        ]),
    ]

    spec = {
        "id": lid,
        "course": "PRJ",
        "series": SERIES,
        "title": cfg["title"],
        "voice": "vi-VN-NamMinhNeural",
        "rate": "-5%",
        "depth": "full",
        "af2": True,
        "covers": [{"objective": 1, "scene": "example"}, {"objective": 2, "scene": "check"}, {"objective": 3, "scene": "quymo"}],
        "source": f"curriculum/prj.yaml {lid}; labs/PRJ/SPEC.md; Python 3.13 + labs/cham.sh",
        "assumes": ["prj_bat_bien"],
        "objectives": cfg["obj"],
        "asr_reviewed": [],
        "scenes": scenes,
    }

    res = lv.lint(spec)
    if res.errors or res.warnings:
        raise RuntimeError(f"lint PRJ {lid}: E={res.errors} W={res.warnings}")

    ak.write_lesson(spec, cfg["fname"][4:-5])
    print(f"OK PRJ {lid}: {cfg['fname']} ({len(lab_lines)} dòng)")

led_p, nblk = up.sync_course_ledger("PRJ", default_lang="python")
print(f"Updated {led_p.relative_to(ROOT)}: {nblk} new blocks synced cleanly")
