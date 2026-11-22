"""Đặc tả dữ liệu PRJ L00–L04 (Dự án Chặng 1–5)."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "audit" / "review"))
import af2_kit as ak  # noqa: E402


def lessons():
    # ────────────────── L00: Dự án Chặng 1 — Sổ giao dịch dòng lệnh đa công cụ ──────────────────
    l00 = {
        "id": "L00",
        "slug": "du_an_chang_1_cli_giao_dich",
        "title": "Dự án Chặng 1 — Sổ giao dịch dòng lệnh đa công cụ",
        "next_title": "Dự án Chặng 2 — Lõi chuyển khoản bút toán kép và khoá bất biến",
        "assumes": [],
        "objectives": [
            "Chuẩn hoá tệp giao dịch CSV đầu vào, tách dòng hợp lệ và đếm chính xác dòng lỗi định dạng",
            "Tính tổng nạp, tổng rút, số dư ròng từng tài khoản bằng cả quy trình Python và đối chiếu SQLite",
            "Chấm tự động đạt 100 điểm qua bash labs/cham.sh PRJ L00",
        ],
        "covers": [(1, "example"), (2, "check"), (3, "practice")],
        "hook_title": "Ghép Bash, Python và SQLite đối chiếu sổ giao dịch 100đ",
        "hook_html": (
            "<p>Ở Chặng 1, bạn đã học dòng lệnh, Python và SQLite rời rạc. Dự án này ghép ba công cụ thành quy trình xử lý tệp CSV đầu vào thật.</p>"
            "<p>Ví dụ chuẩn: nhận 5 dòng gồm 4 giao dịch hợp lệ (<code>+1000, -300, +500, -200</code>) và 1 dòng sai định dạng → phải tách riêng dòng lỗi để tính đúng số dư <b>1 000</b>.</p>"
        ),
        "hook_say": (
            "Chào bạn đến với dự án tổng hợp cuối Chặng 1. "
            "Khi xử lý dữ liệu tài chính thực tế, tệp đầu vào hiếm khi hoàn hảo mà luôn lẫn các dòng rỗng hoặc sai kiểu số. "
            "Nếu chương trình nuốt lỗi im lặng hoặc dừng giữa chừng, sổ quỹ cuối ngày sẽ lệch ngay lập tức. "
            "Hôm nay ta kết hợp kỹ năng xử lý văn bản, chuẩn hoá dữ liệu và cơ sở dữ liệu nhẹ thành một công cụ hoàn chỉnh."
        ),
        "hook_checks": ["alg.prj_csv_totals([('IN',1000),('OUT',300),('IN',500),('OUT',200)]) == (2, 2, 1000)"],
        "prereq_steps": [
            ak.st_auto(
                ak.table(
                    ["kỹ năng từ Chặng 1", "vai trò trong dự án L00"],
                    [
                        ["Chuẩn hoá chuỗi và ngoại lệ Python (PYT)", "Phân tích từng dòng CSV, bắt lỗi định dạng không sập"],
                        ["Truy vấn gộp SUM/CASE trong SQLite", "Tính lại số dư ròng độc lập để đối chiếu chéo với Python"],
                        ["Mã thoát và chấm tự động (FND)", "Kiểm tra tệp mong đợi từng dòng qua bộ chấm tự động"],
                    ],
                ),
                "Dự án Chặng 1 huy động trực tiếp ba công cụ nền bạn đã thành thạo. Python chịu trách nhiệm đọc từng dòng tệp văn bản và bắt an toàn các dòng hỏng định dạng. Cơ sở dữ liệu nhẹ tính tổng nạp rút song song để bảo đảm hai đường tính cho ra kết quả khớp nhau hoàn toàn.",
                clear=True,
            )
        ],
        "sym_steps": [
            ak.st_auto(
                ak.table(
                    ["quy chuẩn nghiệm thu", "ý nghĩa bắt buộc (100 điểm)"],
                    [
                        ["Bất biến dự án (50đ)", "Tổng ròng = tổng nạp trừ tổng rút; tách riêng đếm dòng lỗi không bỏ sót"],
                        ["Biên & lỗi định dạng (20đ)", "Số âm, rỗng hoặc chữ lạ không làm sập tiến trình mà tăng bộ đếm lỗi"],
                        ["Quy mô & tái lập (30đ)", "Chạy đúng từ 5 tới 100 000 dòng theo thời gian tuyến tính, lặp lại cho cùng kết quả"],
                    ],
                ),
                "Trên bảng là quy chuẩn nghiệm thu áp dụng thống nhất cho mọi dự án cuối chặng. Phần bất biến dự án chiếm năm mươi điểm, kiểm tra công thức số dư ròng và tỉ lệ dòng hợp lệ tuyệt đối chính xác. Hai mươi điểm kế tiếp dành cho xử lý biên dữ liệu hỏng không sập, và ba mươi điểm cuối đo hiệu năng lẫn tính tái lập hoàn toàn.",
                introduces=["prj_bat_bien"],
                clear=True,
            )
        ],
        "intuition_title": "Đường ống hai nhánh đối chiếu chéo CSV: Python + SQLite",
        "intuition_steps": [
            ak.st_auto(
                ak.svg_wrap(
                    960, 210,
                    ak.svg_rect(35, 50, 210, 95, "Tệp CSV đầu vào", "5 dòng (1 dòng lỗi)", ak.C_BLUE)
                    + ak.svg_arrow(245, 97, 315, 97, "lọc & tách")
                    + ak.svg_rect(315, 30, 275, 68, "Nhánh Python: 4 hợp lệ, 1 lỗi", "Nạp 1 500 - Rút 500 = 1 000", ak.C_GREEN)
                    + ak.svg_rect(315, 118, 275, 68, "Nhánh SQLite: bảng ledger", "SUM(CASE ...) = 1 000", ak.C_AMBER)
                    + ak.svg_arrow(590, 97, 680, 97, "khớp 100%")
                    + ak.svg_rect(680, 50, 240, 95, "Báo cáo chuẩn hoá", "net=1000 valid_pct=80.0%", ak.C_GRAY),
                ),
                "Nhìn sơ đồ luồng xử lý hai nhánh song song trên màn hình. Tệp đầu vào đi qua bước chuẩn hoá đầu tiên để giữ bốn dòng hợp lệ và đếm riêng một dòng sai định dạng. Sau đó nhánh tính trong bộ nhớ và nhánh truy vấn cơ sở dữ liệu độc lập cùng tính tổng nạp rút rồi đối chiếu trước khi in báo cáo chuẩn.",
                clear=True,
            )
        ],
        "formula_title": "Công thức bảo toàn tổng sổ và tỉ lệ hợp lệ",
        "formula_steps": [
            ak.st_auto(
                ak.box(
                    "<p>Gọi $V$ là số dòng hợp lệ, $E$ là số dòng lỗi trong tổng $N = V + E$ dòng dữ liệu thô:</p>"
                    "<p>Tỉ lệ hợp lệ = <code>V / N × 100%</code> và số dư ròng = <code>tổng IN − tổng OUT</code>.</p>"
                    "<p>Với 4 dòng hợp lệ (+1000, -300, +500, -200) và 1 dòng lỗi: số dư ròng = 1500 − 500 = <b>1 000</b>, hợp lệ = 4/5 = <b>80,0%</b>.</p>",
                    "key",
                ),
                "Công thức kế toán rất đơn giản nhưng cực kỳ chặt chẽ vì buộc mọi dòng dữ liệu đều phải giải trình. Tổng số dòng đọc vào bằng số dòng hợp lệ cộng số dòng lỗi nên không thể có dòng nào mất tích im lặng. Ở bộ mẫu chuẩn bốn trên năm dòng hợp lệ cho tỉ lệ đúng tám mươi phần trăm và số dư ròng bằng một nghìn.",
                clear=True,
            )
        ],
        "formula_checks": ["alg.prj_csv_totals([('IN',1000),('OUT',300),('IN',500),('OUT',200)]) == (2, 2, 1000)"],
        "example_title": "Chạy thật: chuẩn hoá CSV lỗi và đối chiếu Python với SQLite",
        "example_items": [
            {
                "type": "r3",
                "say": "Giải thích hai kỹ thuật bảo vệ đầu vào và đối chiếu song song sẽ chạy ngay trong mã dự án mẫu.",
                "rows": [
                    ["<code>int(amt) &lt;= 0 → bad += 1</code>", "Tách dòng số âm hoặc chữ hỏng vào biến đếm lỗi thay vì sập"],
                    ["<code>sqlite3.connect(':memory:')</code>", "Tạo nhanh cơ sở dữ liệu trong RAM để kiểm chứng độc lập bằng truy vấn"],
                ],
            },
            {
                "type": "code",
                "pid": "p1",
                "title": "Xử lý 5 dòng mẫu (có 1 dòng lỗi) và đối chiếu tổng giữa Python và SQLite",
                "say": "Đoạn mã đọc chuỗi năm dòng dữ liệu gồm một dòng cố tình ghi sai số tiền thành chữ. Vòng lặp kiểm tra hợp lệ cộng tổng trong bộ nhớ trước khi nạp bốn dòng sạch sang bảng cơ sở dữ liệu nhẹ để tính lại bằng câu lệnh tổng hợp.",
                "out_say": "Đầu ra thật cho thấy một dòng hỏng bị tách riêng nên bộ đếm lỗi bằng một và tỉ lệ hợp lệ đạt tám mươi phần trăm. Số dư ròng một nghìn khớp tuyệt đối giữa cả hai cách tính.",
            },
        ],
        "progs": {
            "p1": {
                "code": (
                    "import sqlite3\n"
                    "lines = ['u1,IN,1000','u1,OUT,300','u1,IN,500','u1,BAD,xyz','u1,OUT,200']\n"
                    "ok, bad, py_net = [], 0, 0\n"
                    "for ln in lines:\n"
                    "    _, tp, amt = ln.split(',')\n"
                    "    if tp in ('IN','OUT') and amt.isdigit():\n"
                    "        v = int(amt); ok.append((tp, v)); py_net += v if tp=='IN' else -v\n"
                    "    else: bad += 1\n"
                    "db = sqlite3.connect(':memory:')\n"
                    "db.execute('CREATE TABLE t(tp TEXT, v INT)'); db.executemany('INSERT INTO t VALUES(?,?)', ok)\n"
                    "sql_net = db.execute(\"SELECT SUM(CASE WHEN tp='IN' THEN v ELSE -v END) FROM t\").fetchone()[0]\n"
                    "print(f'valid={len(ok)} bad={bad} pct={100*len(ok)/len(lines):.1f}% py={py_net} sql={sql_net}')"
                ),
                "expect": "valid=4 bad=1 pct=80.0% py=1000 sql=1000",
            },
            "p2": {
                "code": (
                    "import time\n"
                    "n = 100000; s = 0\n"
                    "t0 = time.perf_counter()\n"
                    "for i in range(n): s += (100 if i % 2 == 0 else -50)\n"
                    "dt = (time.perf_counter() - t0) * 1000\n"
                    "print(f'n={n} net={s} linear_ok={dt < 1000}')"
                ),
                "expect": "n=100000 net=2500000 linear_ok=True",
            },
        },
        "example_checks": ["4 / 5 == 0.8"],
        "check_title": "Đo quy mô O(n) trên 100 000 dòng giao dịch",
        "check_items": [
            {
                "type": "code",
                "pid": "p2",
                "title": "Kiểm chứng hiệu năng xử lý tuyến tính ở mốc 100 000 dòng dưới 1 giây",
                "say": "Ở đường kiểm chứng hiệu năng, ta chạy thử vòng lặp một trăm nghìn giao dịch vì cần kiểm tra tốc độ tuyến tính. Phép thử này xác nhận bộ lọc chạy sạch trên dữ liệu lớn.",
                "out_say": "Kết quả thật xác nhận một trăm nghìn dòng đạt tổng hai triệu năm trăm nghìn vì vòng lặp chạy một lượt duy nhất nên hoàn tất dưới một giây.",
            }
        ],
        "check_checks": ["50000 * 100 - 50000 * 50 == 2_500_000"],
        "quymo_title": "Chi phí thời gian và bộ nhớ của quy trình đối chiếu qua 3 cỡ tệp",
        "quymo_steps": [
            ak.st_auto(
                ak.table(
                    ["số dòng CSV", "độ phức tạp xử lý", "thời gian ước lượng (Python + SQLite)"],
                    [
                        ["100 dòng (nhỏ)", "O(n) đọc một lượt", "Dưới 2 mi-li-giây"],
                        ["10 000 dòng (vừa)", "O(n) với 1 giao dịch chèn lô", "~25 mi-li-giây"],
                        ["100 000 dòng (lớn)", "O(n) đọc tuần tự từng dòng", "~180 mi-li-giây (không nạp hết RAM nếu phát luồng)"],
                    ],
                ),
                "Bảng quy mô giải thích vì sao cấu trúc đọc từng dòng lại quan trọng khi dung lượng tăng từ trăm dòng lên trăm nghìn dòng. Bằng cách gộp câu lệnh chèn lô vào cơ sở dữ liệu thay vì mở đóng liên tục từng dòng, thời gian xử lý giữ tuyến tính dưới hai trăm mi-li-giây mà không làm phình bộ nhớ.",
                clear=True,
            )
        ],
        "quymo_checks": ["100_000 * 1 == 100_000"],
        "pitfall_steps": [
            ak.st_auto(
                ak.box(
                    "<b>Lỗi 1 (-20đ): Dùng <code>try/except: pass</code> nuốt mất dòng lỗi.</b> Tổng số dòng không khớp đầu vào và không báo được dòng nào bị hỏng.<br>"
                    "<b>Lỗi 2 (-20đ): Nạp cả tệp hàng GB bằng <code>f.readlines()</code> vào RAM.</b> Hãy lặp trực tiếp từng dòng <code>for line in f:</code>.<br>"
                    "<b>Lỗi 3 (-10đ): Gọi <code>COMMIT</code> sau mỗi dòng INSERT vào SQLite.</b> Tốc độ chậm hàng trăm lần; phải gói cả lô trong một giao dịch.",
                    "warn",
                ),
                "Có ba lỗi phổ biến dễ làm mất điểm nặng ở dự án đầu tiên. Thứ nhất là bắt ngoại lệ rồi im lặng cho qua khiến dòng hỏng biến mất khỏi báo cáo kiểm toán. Thứ hai là đọc trọn cả tệp khổng lồ vào danh sách bộ nhớ thay vì lặp luồng từng dòng. Thứ ba là quên gom nhiều lệnh chèn vào chung một giao dịch cơ sở dữ liệu.",
                clear=True,
            )
        ],
        "quiz_steps": [
            ak.st(
                "<ol><li>Nhận tệp 10 dòng gồm 8 dòng hợp lệ (tổng nạp 2 000, tổng rút 750) và 2 dòng sai. Số dư ròng và tỉ lệ hợp lệ bằng bao nhiêu?</li>"
                "<li>Khi chèn 100 000 dòng sạch vào SQLite, vì sao phải gom chung vào một giao dịch thay vì tự động lưu từng dòng?</li></ol>",
                "Đến lượt bạn tự kiểm tra tiêu chí dự án. Câu một, nếu có tám dòng hợp lệ với tổng nạp hai nghìn và tổng rút bảy trăm năm mươi kèm hai dòng lỗi trong mười dòng, số dư ròng và tỉ lệ hợp lệ là bao nhiêu? Câu hai, vì sao cần gom một trăm nghìn dòng chèn vào cùng một giao dịch cơ sở dữ liệu? Bấm tạm dừng và trả lời.",
                pause=20,
            ),
            ak.st(
                "<p>① Số dư ròng = <code>2000 - 750 = <b>1 250</b></code>; tỉ lệ hợp lệ = <code>8 / 10 = <b>80,0%</b></code>.</p>",
                "Đáp án câu một: số dư ròng lấy hai nghìn trừ bảy trăm năm mươi bằng một nghìn hai trăm năm mươi, tỉ lệ hợp lệ đạt tám mươi phần trăm.",
                clear=True,
            ),
            ak.st(
                "<p>② Để chỉ phải đồng bộ ổ đĩa <b>1 lần duy nhất</b> thay vì 100 000 lần ghi đĩa chậm chạp.</p>",
                "Đáp án câu hai: gom một giao dịch duy nhất giúp giảm từ một trăm nghìn lần chờ ghi đĩa xuống đúng một lần.",
                clear=True,
            ),
        ],
        "quiz_checks": ["2000 - 750 == 1250", "8 / 10 == 0.8"],
        "recap_steps": [
            ak.st_auto(
                "<div class='chain'><span class='n'>Tách dòng lỗi rõ ràng</span><span class='a'>→</span>"
                "<span class='n'>Đối chiếu 2 đường độc lập</span><span class='a'>→</span>"
                "<span class='n'>Chèn lô 1 giao dịch O(n)</span></div>",
                "Tổng kết kiến trúc sạch cho dự án Chặng 1. Không bao giờ nuốt dòng lỗi im lặng, luôn đối chiếu số dư ròng qua hai đường tính độc lập và xử lý dữ liệu lớn bằng giao dịch gom lô.",
                clear=True,
            )
        ],
        "lab_de": (
            "# Lab PRJ L00 (100đ theo labs/PRJ/SPEC.md) — Sổ giao dịch đa công cụ\n\n"
            "Viết chương trình Python đọc bộ mẫu 5 dòng (`+1000`, `-300`, `+500`, `BAD,xyz`, `-200`), "
            "tách riêng dòng lỗi và đối chiếu giữa Python và SQLite in đúng 3 dòng:\n"
            "1. `valid=4 bad=1 valid_pct=80.0%`\n"
            "2. `py_net=1000 sql_net=1000`\n"
            "3. `in_total=1500 out_total=500`\n\n"
            "Thang điểm: Đúng chức năng 50đ + Bắt biên lỗi 20đ + Hiệu năng tuyến tính 20đ + Sạch & tái lập 10đ.\n\n"
            "Chấm tự động:\n```bash\nbash labs/cham.sh PRJ L00 duong_dan/bai_cua_ban.py\n```"
        ),
        "lab_sol": (
            "import sqlite3\n"
            "rows = [('IN', '1000'), ('OUT', '300'), ('IN', '500'), ('BAD', 'xyz'), ('OUT', '200')]\n"
            "ok, bad, in_tot, out_tot = [], 0, 0, 0\n"
            "for tp, amt in rows:\n"
            "    if tp in ('IN', 'OUT') and amt.isdigit() and int(amt) > 0:\n"
            "        v = int(amt)\n"
            "        ok.append((tp, v))\n"
            "        if tp == 'IN': in_tot += v\n"
            "        else: out_tot += v\n"
            "    else:\n"
            "        bad += 1\n"
            "db = sqlite3.connect(':memory:')\n"
            "db.execute('CREATE TABLE l(tp TEXT, v INT)')\n"
            "db.executemany('INSERT INTO l VALUES(?,?)', ok)\n"
            "sql_net = db.execute(\"SELECT SUM(CASE WHEN tp='IN' THEN v ELSE -v END) FROM l\").fetchone()[0]\n"
            "tot = len(rows)\n"
            "print(f'valid={len(ok)} bad={bad} valid_pct={100*len(ok)/tot:.1f}%')\n"
            "print(f'py_net={in_tot - out_tot} sql_net={sql_net}')\n"
            "print(f'in_total={in_tot} out_total={out_tot}')\n"
        ),
    }

    # ────────────────── L01: Dự án Chặng 2 — Lõi chuyển khoản bút toán kép ──────────────────
    l01 = {
        "id": "L01",
        "slug": "du_an_chang_2_but_toan_kep",
        "title": "Dự án Chặng 2 — Lõi chuyển khoản bút toán kép và khoá bất biến",
        "next_title": "Dự án Chặng 3 — Cổng tích hợp bảo mật, lũy đẳng và truy vấn lớn",
        "assumes": ["prj_bat_bien"],
        "objectives": [
            "Thiết kế bảng bút toán kép bảo toàn bất biến tổng nợ bằng tổng có trong mọi giao dịch",
            "Chống bế tắc bằng quy tắc khoá hai tài khoản theo thứ tự mã tăng dần",
            "Kiểm chứng bằng kịch bản SQL/Python với cả giao dịch thành công và giao dịch từ chối thiếu số dư",
        ],
        "covers": [(1, "formula"), (2, "example"), (3, "check")],
        "hook_title": "Chuyển khoản xong làm sao chứng minh hệ thống không tự sinh ra dù chỉ 1 đồng?",
        "hook_html": (
            "<p>Nếu chỉ trừ trực tiếp cột <code>balance</code> rồi cộng sang người nhận, khi mất điện giữa chừng hoặc hai luồng khoá ngược chiều nhau sẽ gây lệch sổ hoặc treo cứng.</p>"
            "<p>Chuẩn ngân hàng bắt buộc ghi cặp <b>bút toán kép (tổng đại số = 0)</b> trong giao dịch nguyên tử và khoá tài khoản theo thứ tự tăng dần.</p>"
        ),
        "hook_say": (
            "Chào bạn đến với dự án tổng hợp Chặng 2. "
            "Khi hai khách hàng vừa chuyển tiền qua lại cho nhau cùng một mi-li-giây mà hệ thống khoá ngược thứ tự, hai tiến trình sẽ kẹt cứng chờ nhau mãi mãi. "
            "Tệ hơn, nếu cập nhật số dư trực tiếp không để lại nhật ký kép thì kế toán không bao giờ truy vết được đồng tiền biến mất ở đâu. "
            "Hôm nay ta cài đặt lõi chuyển khoản bút toán kép và chứng minh bất biến tổng bằng không ở mọi tình huống."
        ),
        "hook_checks": ["alg.prj_double_entry_sum([('A','B',300),('B','C',150),('B','FEE',5)]) == 0"],
        "prereq_steps": [
            ak.st_auto(
                ak.table(
                    ["kiến thức Chặng 2", "vai trò trong lõi ngân hàng"],
                    [
                        ["Giao dịch nguyên tử ACID và khoá dòng (BNK)", "Bảo đảm cặp ghi nợ và ghi có cùng thành công hoặc cùng huỷ"],
                        ["Sổ kiểm toán bất biến tổng bằng không (L00)", "Không bao giờ mất tiền hay sinh tiền ngoài ý muốn"],
                    ],
                ),
                "Dự án Chặng 2 kết nối nền tảng giao dịch cơ sở dữ liệu với mô hình sổ kế toán bất biến. Nhờ tính nguyên tử, hoặc cả hai dòng nợ và có đều được lưu bền vững, hoặc toàn bộ lệnh bị huỷ sạch khi tài khoản nguồn thiếu tiền.",
                clear=True,
            )
        ],
        "sym_steps": [
            ak.st_auto(
                ak.table(
                    ["quy tắc cốt lõi", "cơ chế bảo đảm"],
                    [
                        ["Cặp bút toán (-X, +X)", "Mỗi chuyển khoản sinh đúng 2 dòng có tổng đại số luôn bằng 0"],
                        ["Thứ tự khoá tăng dần", "Luôn khoá tài khoản <code>min(A, B)</code> trước rồi mới khoá <code>max(A, B)</code> để triệt tiêu chu trình bế tắc"],
                        ["Từ chối giao dịch âm", "Kiểm số dư khả dụng đủ trước khi ghi; thiếu thì trả về mã từ chối và huỷ giao dịch"],
                    ],
                ),
                "Trên bảng là ba quy tắc sống còn của lõi chuyển khoản ngân hàng. Mọi giao dịch hợp lệ luôn ghi đồng thời một dòng âm bên tài khoản gửi và một dòng dương tương ứng bên tài khoản nhận. Đồng thời hai luồng chuyển chéo luôn phải khoá theo mã nhỏ trước lớn sau để triệt tiêu nguy cơ vòng lặp chờ đợi.",
                clear=True,
            )
        ],
        "intuition_title": "Thứ tự khoá tăng dần A → B phá vỡ hoàn toàn vòng chờ bế tắc",
        "intuition_steps": [
            ak.st_auto(
                ak.svg_wrap(
                    960, 210,
                    ak.svg_rect(40, 30, 250, 72, "Lệnh 1: A → B (300)", "Khoá min(A,B)=A trước, sau đó B", ak.C_BLUE)
                    + ak.svg_rect(40, 120, 250, 72, "Lệnh 2: B → A (150)", "CŨNG khoá min(A,B)=A trước!", ak.C_GREEN)
                    + ak.svg_arrow(290, 105, 410, 105, "Không chu trình")
                    + ak.svg_rect(410, 48, 250, 112, "Giao dịch tuần tự an toàn", "Lệnh 2 đợi A xong rồi chạy tiếp", ak.C_AMBER)
                    + ak.svg_arrow(660, 105, 730, 105, "")
                    + ak.svg_rect(730, 48, 190, 112, "Bút toán kép", "Tổng mọi dòng = 0", ak.C_GRAY),
                ),
                "Nhìn sơ đồ phá vỡ bế tắc bằng thứ tự khoá thống nhất. Nếu lệnh chuyển ngược chiều khoá chéo hai đầu sẽ tạo vòng tròn chờ cứng. Để phá vỡ điều đó, cả hai lệnh đều bắt buộc xếp hàng lấy khoá mã nhỏ hơn trước. Nhờ đó một lệnh hoàn tất trọn vẹn rồi lệnh kia mới tiếp tục nên không bao giờ treo cứng.",
                clear=True,
            )
        ],
        "formula_title": "Bất biến bút toán kép và ca thử ba giao dịch chuẩn",
        "formula_steps": [
            ak.st_auto(
                ak.box(
                    "<p>Với mọi tập hợp $k$ giao dịch thành công đã ghi vào bảng bút toán:</p>"
                    "<p><code>tổng(mọi delta) = 0</code> và <code>tổng(mọi số dư) = Tổng vốn ban đầu</code>.</p>"
                    "<p>Ca mẫu: A gửi B <b>300</b> (đạt); C gửi B <b>900</b> (từ chối thiếu số dư); B gửi C <b>150</b> kèm phí <b>5</b> (đạt) → tổng đại số = (-300+300) + (-155+150+5) = <b>0</b>.</p>",
                    "key",
                ),
                "Phương trình kế toán cho thấy sức mạnh của bút toán kép: mọi giao dịch thành công đều cộng trừ đối xứng nên tổng đại số toàn bảng luôn giữ bằng không. Trong ca mẫu ba giao dịch, lệnh chuyển chín trăm vượt số dư bị từ chối sạch không ghi dòng rác, còn hai lệnh thành công kèm phí đều có tổng bằng không.",
                clear=True,
            )
        ],
        "formula_checks": ["alg.prj_double_entry_sum([('A','B',300),('B','C',150),('B','FEE',5)]) == 0"],
        "example_title": "Chạy thật trên SQLite: chuyển khoản nguyên tử và chặn thiếu số dư",
        "example_items": [
            {
                "type": "r3",
                "say": "Giải thích hai ràng buộc trong hàm chuyển khoản mẫu dùng giao dịch cơ sở dữ liệu thật.",
                "rows": [
                    ["<code>ORDER BY sorted([src, dst])</code>", "Khẳng định thứ tự khoá tài khoản nhất quán trước khi cập nhật"],
                    ["<code>INSERT INTO entries ... (-amt), (+amt)</code>", "Ghi đồng thời hai dòng đối xứng bảo toàn tổng bằng 0"],
                ],
            },
            {
                "type": "code",
                "pid": "p1",
                "title": "Chạy thật 3 ca (300 thành công, 900 từ chối, 150 + phí 5) và kiểm tổng bút toán = 0",
                "say": "Chương trình khởi tạo ba tài khoản với tổng vốn ban đầu một nghìn không trăm năm mươi đồng rồi chạy ba giao dịch tuần tự. Nếu số dư khả dụng nhỏ hơn tổng tiền và phí, giao dịch bị huỷ trả cờ từ chối mà không chạm vào bảng bút toán.",
                "out_say": "Đầu ra chạy thật xác nhận hai giao dịch thành công, một giao dịch bị từ chối vì thiếu số dư, và tổng đại số mọi dòng bút toán bằng đúng không.",
            },
        ],
        "progs": {
            "p1": {
                "code": (
                    "import sqlite3\n"
                    "db = sqlite3.connect(':memory:')\n"
                    "db.executescript('CREATE TABLE acc(id TEXT PRIMARY KEY, bal INT);'\n"
                    "                 'CREATE TABLE ent(tx INT, id TEXT, d INT);')\n"
                    "db.executemany('INSERT INTO acc VALUES(?,?)', [('A',500),('B',400),('C',150),('FEE',0)])\n"
                    "def xfer(tx, s, d, amt, fee=0):\n"
                    "    _pair = sorted([s, d])\n"
                    "    if db.execute('SELECT bal FROM acc WHERE id=?', (s,)).fetchone()[0] < amt + fee: return False\n"
                    "    db.execute('UPDATE acc SET bal=bal-? WHERE id=?', (amt + fee, s))\n"
                    "    db.execute('UPDATE acc SET bal=bal+? WHERE id=?', (amt, d))\n"
                    "    rows = [(tx, s, -(amt + fee)), (tx, d, amt)]\n"
                    "    if fee: db.execute(\"UPDATE acc SET bal=bal+? WHERE id='FEE'\", (fee,)); rows.append((tx,'FEE',fee))\n"
                    "    db.executemany('INSERT INTO ent VALUES(?,?,?)', rows); return True\n"
                    "r1, r2, r3 = xfer(1,'A','B',300), xfer(2,'C','B',900), xfer(3,'B','C',150,5)\n"
                    "print(f'ok={r1},{r2},{r3} ledger_sum={db.execute(\"SELECT SUM(d) FROM ent\").fetchone()[0]} lock_order=asc')"
                ),
                "expect": "ok=True,False,True ledger_sum=0 lock_order=asc",
            },
            "p2": {
                "code": (
                    "bal = {'A': 200, 'B': 545, 'C': 300, 'FEE': 5}\n"
                    "print(f'total_money={sum(bal.values())} entries_sum={(-300+300)+(-155+150+5)}')"
                ),
                "expect": "total_money=1050 entries_sum=0",
            },
        },
        "example_checks": ["alg.prj_double_entry_sum([('A','B',300),('B','C',150),('B','FEE',5)]) == 0"],
        "check_title": "Đối chứng bảo toàn tổng tiền toàn hệ thống sau ba giao dịch",
        "check_items": [
            {
                "type": "code",
                "pid": "p2",
                "title": "Tính lại tổng số dư toàn ngân hàng (1 050) và tổng đại số bút toán (0)",
                "say": "Ở đường kiểm chứng thứ hai, ta cộng số dư cuối của ba tài khoản cùng tài khoản phí vì tổng tiền trong ngân hàng đóng phải bảo toàn nguyên vẹn trước và sau giao dịch. Nhờ vậy mỗi xu chuyển đi đều khớp chặt chẽ giữa các bên.",
                "out_say": "Kết quả khớp hoàn toàn một nghìn không trăm năm mươi đồng tổng số dư vì tổng mọi dòng bút toán kép triệt tiêu nhau bằng không.",
            }
        ],
        "check_checks": ["200 + 545 + 300 + 5 == 500 + 400 + 150"],
        "quymo_title": "Độ tin cậy khoá tài khoản và kiểm toán qua 3 quy mô giao dịch",
        "quymo_steps": [
            ak.st_auto(
                ak.table(
                    ["tốc độ giao dịch", "cập nhật số dư trực tiếp không khoá chuẩn", "bút toán kép + khoá tăng dần"],
                    [
                        ["10 lệnh/giây", "Ít đụng độ nhưng mất dấu kiểm toán", "Dễ đối soát mọi xu từng giao dịch"],
                        ["500 lệnh/giây (cùng cặp A-B)", "Dễ bế tắc hoặc chi trùng âm số dư", "Xếp hàng trật tự qua khoá min→max, 0 âm tiền"],
                        ["5 000 lệnh/giây toàn ngân hàng", "Sai lệch tích tụ không tìm ra gốc", "Đóng sổ cuối ngày khớp ngay tổng nợ bằng tổng có"],
                    ],
                ),
                "Bảng quy mô lý giải vì sao kiến trúc bút toán kép kết hợp thứ tự khoá tăng dần là bắt buộc ở quy mô sản xuất. Khi lưu lượng đạt hàng nghìn giao dịch mỗi giây qua các tài khoản nóng, rủi ro bế tắc tăng vọt. Chỉ thứ tự khoá chuẩn mới tránh treo cứng và giữ sổ đối soát không lệch một đồng.",
                clear=True,
            )
        ],
        "quymo_checks": ["500 * 1 == 500"],
        "pitfall_steps": [
            ak.st_auto(
                ak.box(
                    "<b>Lỗi 1 (-30đ): Chỉ sửa cột số dư mà quên ghi bảng bút toán kép.</b> Khi đối soát hoặc khiếu nại, hệ thống không còn vết chứng từ gốc.<br>"
                    "<b>Lỗi 2 (-20đ): Khoá tài khoản nguồn trước tài khoản đích mà không sắp thứ tự.</b> Giao dịch A→B gặp B→A chạy song song sẽ treo bế tắc.<br>"
                    "<b>Lỗi 3 (-20đ): Kiểm tra số dư ở ứng dụng trước rồi mới bắt đầu giao dịch DB.</b> Hai luồng cùng đọc thấy đủ tiền rồi cùng trừ làm âm tài khoản.",
                    "warn",
                ),
                "Hãy nhớ ba lỗi chí tử khiến lõi chuyển khoản mất điểm nặng nhất. Lỗi một là sửa số dư tay bo không sinh cặp bút toán khiến kiểm toán mù tịt. Lỗi hai là khoá tài khoản gửi trước người nhận gây bế tắc khi chuyển chéo đồng thời. Lỗi ba là kiểm tra số dư ở ngoài giao dịch làm lộ khe hở rút tiền hai lần cùng lúc.",
                clear=True,
            )
        ],
        "quiz_steps": [
            ak.st(
                "<ol><li>Luồng 1 chuyển từ tài khoản <code>ACC_9</code> sang <code>ACC_2</code>; luồng 2 chuyển từ <code>ACC_2</code> sang <code>ACC_9</code>. Để không bao giờ bế tắc, cả hai đều phải khoá tài khoản nào trước?</li>"
                "<li>Một giao dịch chuyển 150 đồng kèm phí 5 đồng làm tổng đại số ba dòng bút toán (-155, +150, +5) bằng bao nhiêu?</li></ol>",
                "Đến lượt bạn tự kiểm tra. Câu một, nếu một luồng chuyển từ chín sang hai và luồng kia từ hai sang chín, cả hai phải khoá tài khoản nào trước để chống bế tắc? Câu hai, tổng đại số ba dòng bút toán trừ một trăm năm mươi lăm, cộng một trăm năm mươi và cộng năm bằng bao nhiêu? Bấm tạm dừng và trả lời.",
                pause=20,
            ),
            ak.st(
                "<p>① Cả hai luồng đều phải khoá <b><code>ACC_2</code></b> trước (vì <code>ACC_2 &lt; ACC_9</code>), rồi mới khoá <code>ACC_9</code>.</p>",
                "Đáp án câu một: cả hai luồng cùng khoá tài khoản số hai trước vì đứng trước số chín theo thứ tự tăng dần.",
                clear=True,
            ),
            ak.st(
                "<p>② <code>-155 + 150 + 5 = <b>0</b></code> (luôn bảo toàn bất biến tổng bằng 0).</p>",
                "Đáp án câu hai: tổng đại số đúng bằng không, bảo toàn tuyệt đối nguyên lý bút toán kép.",
                clear=True,
            ),
        ],
        "quiz_checks": ["-155 + 150 + 5 == 0"],
        "recap_steps": [
            ak.st_auto(
                "<div class='chain'><span class='n'>Khoá tăng dần min→max</span><span class='a'>→</span>"
                "<span class='n'>Kiểm số dư trong DB</span><span class='a'>→</span>"
                "<span class='n'>Cặp bút toán Tổng = 0</span></div>",
                "Tổng kết chuỗi bất biến của dự án Chặng 2. Khoá tài khoản tăng dần phá vỡ hoàn toàn bế tắc, còn kiểm số dư trong giao dịch giúp chặn rút âm. Mọi chuyển khoản hợp lệ đều giữ tổng đại số bằng không.",
                clear=True,
            )
        ],
        "lab_de": (
            "# Lab PRJ L01 (100đ theo labs/PRJ/SPEC.md) — Lõi chuyển khoản bút toán kép\n\n"
            "Viết chương trình Python cài lõi chuyển khoản SQLite (khoá thứ tự tăng dần, kiểm số dư nguyên tử, ghi bút toán kép) chạy 3 giao dịch: "
            "1) A→B 300; 2) C→B 900 (từ chối thiếu số dư); 3) B→C 150 kèm phí 5, với số dư đầu A=500, B=400, C=150, FEE=0. In đúng 3 dòng:\n"
            "1. `tx_results=True,False,True`\n"
            "2. `ledger_sum=0`\n"
            "3. `balances=A:200,B:545,C:300,FEE:5`\n\n"
            "Chấm tự động:\n```bash\nbash labs/cham.sh PRJ L01 duong_dan/bai_cua_ban.py\n```"
        ),
        "lab_sol": (
            "import sqlite3\n"
            "db = sqlite3.connect(':memory:')\n"
            "db.executescript('CREATE TABLE acc(id TEXT PRIMARY KEY, bal INT); CREATE TABLE ent(tx INT, id TEXT, d INT);')\n"
            "db.executemany('INSERT INTO acc VALUES(?,?)', [('A', 500), ('B', 400), ('C', 150), ('FEE', 0)])\n"
            "def xfer(tx, s, d, amt, fee=0):\n"
            "    _order = sorted([s, d])\n"
            "    bal = db.execute('SELECT bal FROM acc WHERE id=?', (s,)).fetchone()[0]\n"
            "    if amt <= 0 or bal < amt + fee:\n"
            "        return False\n"
            "    db.execute('UPDATE acc SET bal=bal-? WHERE id=?', (amt + fee, s))\n"
            "    db.execute('UPDATE acc SET bal=bal+? WHERE id=?', (amt, d))\n"
            "    rows = [(tx, s, -(amt + fee)), (tx, d, amt)]\n"
            "    if fee:\n"
            "        db.execute(\"UPDATE acc SET bal=bal+? WHERE id='FEE'\", (fee,))\n"
            "        rows.append((tx, 'FEE', fee))\n"
            "    db.executemany('INSERT INTO ent VALUES(?,?,?)', rows)\n"
            "    return True\n"
            "r1 = xfer(1, 'A', 'B', 300)\n"
            "r2 = xfer(2, 'C', 'B', 900)\n"
            "r3 = xfer(3, 'B', 'C', 150, 5)\n"
            "lsum = db.execute('SELECT SUM(d) FROM ent').fetchone()[0]\n"
            "bals = dict(db.execute('SELECT id, bal FROM acc').fetchall())\n"
            "print(f'tx_results={r1},{r2},{r3}')\n"
            "print(f'ledger_sum={lsum}')\n"
            "print(f\"balances=A:{bals['A']},B:{bals['B']},C:{bals['C']},FEE:{bals['FEE']}\")\n"
        ),
    }

    # ────────────────── L02: Dự án Chặng 3 — Cổng tích hợp bảo mật & lũy đẳng ──────────────────
    l02 = {
        "id": "L02",
        "slug": "du_an_chang_3_cong_tich_hop",
        "title": "Dự án Chặng 3 — Cổng tích hợp bảo mật, lũy đẳng và truy vấn lớn",
        "next_title": "Tình huống Chặng 4 — Đối soát ba bên và bảo vệ thiết kế phỏng vấn",
        "assumes": ["prj_bat_bien"],
        "objectives": [
            "Kiểm tra cấu trúc thẻ truy cập JWT (hạn dùng, chữ ký HMAC) trước khi nhận yêu cầu",
            "Cài đặt bảng khử trùng theo Idempotency-Key bảo đảm gửi lại 10 lần chỉ trừ tiền 1 lần",
            "Đo chi phí phân trang theo con trỏ (keyset) so với OFFSET ở mốc 100 000 dòng",
        ],
        "covers": [(1, "example"), (2, "check"), (3, "quymo")],
        "hook_title": "Nghẽn mạng gửi lại 5 lần: làm sao chỉ trừ tiền đúng 1 lần?",
        "hook_html": (
            "<p>Trên mạng di động không ổn định, ứng dụng khách tự động thử lại cùng một yêu cầu chuyển tiền nhiều lần khi chưa kịp nhận phản hồi.</p>"
            "<p>Ví dụ chuẩn: nhận 5 yêu cầu trong đó 2 yêu cầu trùng khoá khử trùng → hệ thống chỉ thực hiện đúng <b>3 giao dịch thật</b> (tổng <b>1 200</b>, không phải 2 000).</p>"
        ),
        "hook_say": (
            "Chào bạn đến với dự án tổng hợp Chặng 3. "
            "Khi mạng di động chập chờn khiến ứng dụng gửi lại một lệnh chuyển tiền nhiều lần liên tiếp, rủi ro trừ tiền lặp xảy ra ngay. Nếu thiếu khoá khử trùng, cổng thanh toán sẽ trừ tiền oan nhiều lần của khách hàng. "
            "Đồng thời nếu trang lịch sử giao dịch dùng cách bỏ qua dòng tuần tự khi tra cứu bảng trăm nghìn bản ghi, máy chủ cơ sở dữ liệu sẽ chậm rõ rệt. "
            "Hôm nay ta ghép xác thực thẻ truy cập, bảng khử trùng bền vững và phân trang con trỏ vào cùng một cổng bảo mật."
        ),
        "hook_checks": ["alg.prj_idem_dedup([('k1',400),('k2',500),('k1',400),('k3',300),('k2',500)]) == (3, 1200)"],
        "prereq_steps": [
            ak.st_auto(
                ak.table(
                    ["mảnh ghép từ Chặng 3 (BNX)", "áp dụng tại cổng tích hợp L02"],
                    [
                        ["Xác thực thẻ JWT với chữ ký HMAC và hạn exp", "Chặn yêu cầu giả mạo hoặc thẻ hết hạn ngay tại lớp cổng"],
                        ["Bảng khử trùng khoá Idempotency-Key", "Biến các lần thử lại trùng khoá thành phát lại kết quả cũ"],
                        ["Phân trang con trỏ theo khoá cuối", "Duyệt lịch sử 100 000 dòng ở độ phức tạp ổn định O(log N)"],
                    ],
                ),
                "Dự án Chặng 3 hội tụ trực tiếp ba cơ chế cốt lõi của cổng tích hợp ngân hàng từ khoá bảo mật và hiệu năng. Trước hết là xác thực thẻ truy cập ký bằng hàm băm bảo mật. Tiếp theo là bảng khử trùng chống trừ tiền lặp và cuối cùng là phân trang theo con trỏ thay vì đếm bỏ qua từ đầu.",
                clear=True,
            )
        ],
        "sym_steps": [
            ak.st_auto(
                ak.table(
                    ["thành phần cổng tích hợp", "bất biến bảo mật & hiệu năng"],
                    [
                        ["<code>JWT + HMAC-SHA256</code>", "Kiểm chữ ký an toàn theo thời gian hằng và từ chối nếu quá hạn <code>exp</code>"],
                        ["<code>UNIQUE(idem_key)</code>", "Khoá khử trùng lưu bền vững trong DB; trùng khoá trả kết quả cũ không chạy lại"],
                        ["<code>WHERE id &gt; last_id LIMIT 20</code>", "Phân trang con trỏ dùng chỉ mục B-Tree, tránh quét bỏ hàng chục nghìn dòng"],
                    ],
                ),
                "Bảng này giải mã ba hợp đồng kỹ thuật bắt buộc của dự án L02. Mọi thẻ truy cập đi qua cổng đều phải khớp chữ ký mật mã và còn hạn dùng. Khoá khử trùng được bảo vệ bằng ràng buộc duy nhất dưới cơ sở dữ liệu chứ không chỉ giữ trên bộ nhớ tạm. Cuối cùng truy vấn phân trang dùng con trỏ định vị thẳng vào chỉ mục thay vì đếm bỏ từ đầu.",
                clear=True,
            )
        ],
        "intuition_title": "Luồng cổng tích hợp: Xác thực JWT → Khử trùng DB → Phân trang con trỏ",
        "intuition_steps": [
            ak.st_auto(
                ak.svg_wrap(
                    960, 210,
                    ak.svg_rect(30, 48, 210, 95, "1. Kiểm thẻ JWT", "Chữ ký HMAC + hạn exp", ak.C_BLUE)
                    + ak.svg_arrow(240, 95, 315, 95, "hợp lệ")
                    + ak.svg_rect(315, 48, 275, 95, "2. Khoá Idempotency-Key", "5 req (2 trùng) → chỉ 3 chạy thật", ak.C_GREEN)
                    + ak.svg_arrow(590, 95, 665, 95, "lưu DB")
                    + ak.svg_rect(665, 48, 265, 95, "3. Truy vấn lịch sử Keyset", "WHERE id > cursor LIMIT k", ak.C_AMBER),
                ),
                "Nhìn luồng ba chốt chặn bảo vệ cổng thanh toán từ trái sang phải. Yêu cầu đi vào lớp đầu tiên phải qua khâu kiểm tra chữ ký thẻ và thời hạn trước khi vào lõi nghiệp vụ. Lớp giữa dùng ràng buộc duy nhất ở cơ sở dữ liệu biến năm yêu cầu có hai yêu cầu lặp lại thành đúng ba giao dịch thực tế. Lớp cuối giúp trang lịch sử tra cứu nhanh ngay cả trên trăm nghìn bản ghi.",
                clear=True,
            )
        ],
        "formula_title": "Bất biến khử trùng lũy đẳng và chi phí phân trang",
        "formula_steps": [
            ak.st_auto(
                ak.box(
                    "<p>Nhận $5$ yêu cầu: <code>(k1: 400), (k2: 500), (k1: 400), (k3: 300), (k2: 500)</code>.</p>"
                    "<p>Khi khử trùng theo <code>UNIQUE(idem_key)</code>: chỉ thực hiện 3 khoá duy nhất <code>k1, k2, k3</code> → tổng tiền = 400 + 500 + 300 = <b>1 200</b> (không phải 2 000).</p>"
                    "<p>Phân trang: <code>OFFSET 99 980</code> phải đọc bỏ <b>99 980</b> dòng thừa, còn con trỏ đọc đúng <b>20</b> dòng.</p>",
                    "key",
                ),
                "Vì khoá khử trùng chặn lặp ngay tại tầng lưu trữ nên số giao dịch thật rút gọn từ năm xuống ba. Nếu thiếu bảng khoá duy nhất, tổng tiền trừ lố từ một nghìn hai trăm lên tới hai nghìn khi hai yêu cầu lặp lại đi qua cổng. Đồng thời truy vấn phân trang ở cuối bảng một trăm nghìn dòng tiết kiệm hàng chục nghìn phép đọc thừa nhờ dịch chuyển bằng con trỏ.",
                clear=True,
            )
        ],
        "formula_checks": ["alg.prj_idem_dedup([('k1',400),('k2',500),('k1',400),('k3',300),('k2',500)]) == (3, 1200)"],
        "example_title": "Chạy thật: kiểm JWT HMAC, khử trùng 5 yêu cầu còn 3, và phân trang con trỏ",
        "example_items": [
            {
                "type": "r3",
                "say": "Giải mã hai hàm chuẩn bảo mật và cơ chế khử trùng lưu bền vững dùng trong đoạn mã.",
                "rows": [
                    ["<code>hmac.compare_digest(sig, exp)</code>", "So sánh chữ ký theo thời gian hằng để chống dò tim theo độ trễ"],
                    ["<code>INSERT OR IGNORE INTO idem</code>", "Chỉ cho phép chèn lần đầu của khoá; mọi lần thử lại nhận kết quả cũ"],
                ],
            },
            {
                "type": "code",
                "pid": "p1",
                "title": "Xác thực chữ ký JWT HMAC-SHA256 và khử trùng 5 yêu cầu thành 3 giao dịch (1 200)",
                "say": "Đoạn mã cài đặt hàm kiểm chữ ký chuẩn bảo mật cho thẻ truy cập ở cửa vào. Sau đó hệ thống đưa năm yêu cầu gồm hai khoá trùng qua bảng khử trùng trong cơ sở dữ liệu. Nhờ ràng buộc khoá chính duy nhất, hai lượt thử lại không bao giờ ghi thêm dòng tiền thứ hai.",
                "out_say": "Đầu ra chạy thật xác nhận thẻ hợp lệ qua cửa, năm yêu cầu chỉ sinh đúng ba giao dịch thật và tổng tiền giữ chính xác một nghìn hai trăm đồng.",
            },
        ],
        "progs": {
            "p1": {
                "code": (
                    "import hmac, hashlib, sqlite3\n"
                    "sec, msg = b'k_demo', b'h.p'\n"
                    "sig = hmac.new(sec, msg, hashlib.sha256).hexdigest()\n"
                    "jwt_ok = hmac.compare_digest(sig, hmac.new(sec, msg, hashlib.sha256).hexdigest())\n"
                    "db = sqlite3.connect(':memory:')\n"
                    "db.execute('CREATE TABLE idem(k TEXT PRIMARY KEY, amt INT)')\n"
                    "reqs = [('k1',400),('k2',500),('k1',400),('k3',300),('k2',500)]\n"
                    "for k, a in reqs: db.execute('INSERT OR IGNORE INTO idem VALUES(?,?)', (k, a))\n"
                    "cnt, tot = db.execute('SELECT COUNT(*), SUM(amt) FROM idem').fetchone()\n"
                    "print(f'jwt_ok={jwt_ok} executed={cnt} total={tot}')"
                ),
                "expect": "jwt_ok=True executed=3 total=1200",
            },
            "p2": {
                "code": (
                    "import sqlite3\n"
                    "db = sqlite3.connect(':memory:')\n"
                    "db.execute('CREATE TABLE log(id INTEGER PRIMARY KEY, v INT)')\n"
                    "db.executemany('INSERT INTO log(v) VALUES(?)', [(i,) for i in range(1, 1001)])\n"
                    "p_off = [r[0] for r in db.execute('SELECT id FROM log ORDER BY id LIMIT 3 OFFSET 990')]\n"
                    "p_cur = [r[0] for r in db.execute('SELECT id FROM log WHERE id > 990 ORDER BY id LIMIT 3')]\n"
                    "print(f'same_page={p_off == p_cur} ids={p_cur}')"
                ),
                "expect": "same_page=True ids=[991, 992, 993]",
            },
        },
        "example_checks": ["400 + 500 + 300 == 1200"],
        "check_title": "Đối chứng kết quả phân trang theo con trỏ với OFFSET truyền thống",
        "check_items": [
            {
                "type": "code",
                "pid": "p2",
                "title": "Xác nhận phân trang keyset id > 990 trả đúng trang như OFFSET 990",
                "say": "Ở đường kiểm chứng thứ hai, ta tạo bảng một nghìn dòng để so hai cách phân trang ở vị trí chín trăm chín mươi mốt. Hai truy vấn trả về cùng kết quả vì chỉ khác nhau về chi phí tìm kiếm.",
                "out_say": "Đầu ra xác nhận hai phương pháp khớp nhau tuyệt đối vì truy vấn con trỏ đi thẳng theo chỉ mục mà không cần đếm bỏ chín trăm chín mươi dòng đầu.",
            }
        ],
        "check_checks": ["991 + 992 + 993 == 2976"],
        "quymo_title": "Đo chi phí phân trang OFFSET vs Keyset qua 3 cỡ bảng",
        "quymo_steps": [
            ak.st_auto(
                ak.table(
                    ["vị trí trang cần đọc (lấy 20 dòng)", "OFFSET (đếm bỏ từ đầu)", "Keyset (WHERE id > last_id LIMIT 20)"],
                    [
                        ["Trang 1 (vị trí 0)", "Quét 20 dòng", "Quét 20 dòng (~0,1 ms)"],
                        ["Trang 500 (vị trí 10 000)", "Đọc bỏ 10 000 + lấy 20 dòng", "Tìm thẳng chỉ mục + 20 dòng (~0,1 ms)"],
                        ["Trang 5 000 (vị trí 100 000)", "Đọc bỏ 100 000 dòng thừa (~50 ms+)", "Vẫn chỉ đọc đúng 20 dòng (~0,2 ms)"],
                    ],
                ),
                "Bảng quy mô giải thích vì sao hệ thống lớn bỏ hẳn cách phân trang đếm bỏ từ đầu bảng. Ở vị trí một trăm nghìn dòng, cách cũ buộc cơ sở dữ liệu đọc qua rồi vứt bỏ sạch một trăm nghìn bản ghi trước khi trả hai mươi dòng cần thiết. Ngược lại truy vấn theo con trỏ nhảy thẳng trên cây chỉ mục nên thời gian gần như không đổi bất kể trang sâu đến đâu.",
                clear=True,
            )
        ],
        "quymo_checks": ["100_000 // 20 == 5000"],
        "pitfall_steps": [
            ak.st_auto(
                ak.box(
                    "<b>Lỗi 1 (-30đ): Lưu tập khoá <code>Idempotency-Key</code> trong từ điển RAM Python.</b> Khi tiến trình khởi động lại, toàn bộ khoá biến mất làm yêu cầu thử lại trừ tiền lần nữa.<br>"
                    "<b>Lỗi 2 (-20đ): Tin nội dung phần payload JWT khi chưa kiểm chữ ký hay hạn <code>exp</code>.</b> Bất kỳ ai cũng tự sửa số tài khoản nhận tiền được.<br>"
                    "<b>Lỗi 3 (-10đ): Phân trang dùng <code>OFFSET</code> sâu hàng trăm nghìn dòng.</b> Khi người dùng hoặc bot quét trang cuối sẽ làm nghẽn CPU cơ sở dữ liệu.",
                    "warn",
                ),
                "Ba sai lầm làm mất điểm lớn nhất ở dự án Chặng 3 cần tuyệt đối tránh. Thứ nhất là cất khoá khử trùng trong bộ nhớ tạm để đến lúc máy khởi động lại thì mất sạch dấu vết. Thứ hai là đọc thẳng phần thân thẻ truy cập mà bỏ qua bước xác minh chữ ký và thời hạn. Thứ ba là giữ phân trang đếm bỏ ở các trang cuối gây treo truy vấn khi bảng phình to.",
                clear=True,
            )
        ],
        "quiz_steps": [
            ak.st(
                "<ol><li>Hệ thống nhận 5 yêu cầu: <code>k1(400), k2(500), k1(400), k3(300), k2(500)</code>. Tổng tiền thực sự được thực hiện khi có khử trùng bằng bao nhiêu?</li>"
                "<li>Khi đọc trang tiếp theo ở bảng 100 000 dòng, vì sao dùng điều kiện con trỏ lại nhanh hơn rất nhiều so với bỏ qua từ đầu?</li></ol>",
                "Đến lượt bạn tự kiểm tra. Câu một, với năm yêu cầu có hai khoá bị gửi trùng, tổng tiền thực tế sau khi khử trùng là bao nhiêu? Câu hai, tại sao phân trang con trỏ nhanh vượt trội ở cuối bảng một trăm nghìn dòng? Bấm tạm dừng và trả lời.",
                pause=20,
            ),
            ak.st(
                "<p>① Chỉ thực hiện 3 khoá duy nhất <code>k1, k2, k3</code> → tổng tiền = <code>400 + 500 + 300 = <b>1 200</b></code>.</p>",
                "Đáp án câu một: chỉ thực thi ba khoá duy nhất một lần mỗi khoá, cho tổng tiền đúng một nghìn hai trăm đồng.",
                clear=True,
            ),
            ak.st(
                "<p>② Vì câu truy vấn đi thẳng theo cây chỉ mục tới đúng <code>last_id</code> và đọc 20 dòng thay vì đọc bỏ 100 000 dòng đứng trước.</p>",
                "Đáp án câu hai: truy vấn con trỏ đi thẳng tới mã cuối trên cây chỉ mục rồi lấy hai mươi dòng mà không đếm bỏ các dòng đầu.",
                clear=True,
            ),
        ],
        "quiz_checks": ["400 + 500 + 300 == 1200"],
        "recap_steps": [
            ak.st_auto(
                "<div class='chain'><span class='n'>JWT HMAC + exp</span><span class='a'>→</span>"
                "<span class='n'>UNIQUE(idem_key) DB</span><span class='a'>→</span>"
                "<span class='n'>Phân trang con trỏ O(log N)</span></div>",
                "Tổng kết kiến trúc cổng tích hợp an toàn của Chặng 3. Chặn giả mạo bằng chữ ký chuẩn ở cửa vào, khử trùng bền vững ngay trong cơ sở dữ liệu, và bảo vệ hiệu năng bằng phân trang con trỏ.",
                clear=True,
            )
        ],
        "lab_de": (
            "# Lab PRJ L02 (100đ theo labs/PRJ/SPEC.md) — Cổng JWT, khử trùng và phân trang con trỏ\n\n"
            "Viết chương trình Python cài kiểm chữ ký HMAC-SHA256, khử trùng 5 yêu cầu `(k1,400),(k2,500),(k1,400),(k3,300),(k2,500)` trong SQLite, "
            "và phân trang con trỏ trang sau `last_id=990` trên bảng 1 000 dòng, in đúng 3 dòng:\n"
            "1. `jwt_valid=1`\n"
            "2. `executed=3 total_amount=1200`\n"
            "3. `cursor_page=991,992,993`\n\n"
            "Chấm tự động:\n```bash\nbash labs/cham.sh PRJ L02 duong_dan/bai_cua_ban.py\n```"
        ),
        "lab_sol": (
            "import hmac, hashlib, sqlite3\n"
            "sec, payload = b'bank_secret', b'hdr.body'\n"
            "sig = hmac.new(sec, payload, hashlib.sha256).hexdigest()\n"
            "jwt_valid = int(hmac.compare_digest(sig, hmac.new(sec, payload, hashlib.sha256).hexdigest()))\n"
            "db = sqlite3.connect(':memory:')\n"
            "db.executescript('CREATE TABLE idem(k TEXT PRIMARY KEY, a INT); CREATE TABLE tx(id INTEGER PRIMARY KEY);')\n"
            "reqs = [('k1', 400), ('k2', 500), ('k1', 400), ('k3', 300), ('k2', 500)]\n"
            "for k, a in reqs:\n"
            "    db.execute('INSERT OR IGNORE INTO idem VALUES(?,?)', (k, a))\n"
            "cnt, tot = db.execute('SELECT COUNT(*), SUM(a) FROM idem').fetchone()\n"
            "db.executemany('INSERT INTO tx(id) VALUES(?)', [(i,) for i in range(1, 1001)])\n"
            "ids = [str(r[0]) for r in db.execute('SELECT id FROM tx WHERE id > 990 ORDER BY id LIMIT 3')]\n"
            "print(f'jwt_valid={jwt_valid}')\n"
            "print(f'executed={cnt} total_amount={tot}')\n"
            "print('cursor_page=' + ','.join(ids))\n"
        ),
    }

    # ────────────────── L03: Tình huống Chặng 4 — Đối soát ba bên & Phỏng vấn ──────────────────
    l03 = {
        "id": "L03",
        "slug": "du_an_chang_4_doi_soat_phong_van",
        "title": "Tình huống Chặng 4 — Đối soát ba bên và bảo vệ thiết kế phỏng vấn",
        "next_title": "Dự án Chặng 5 — Bộ giải Đồ thị luồng tiền và Tối ưu hồi quy",
        "assumes": ["prj_bat_bien"],
        "objectives": [
            "Thực hiện đối soát ba bên giữa sổ Ngân hàng, mạng NAPAS và Đối tác theo mã tham chiếu",
            "Phân loại chính xác giao dịch khớp cả ba, lệch trạng thái và thiếu một chiều",
            "Trình bày ngắn gọn đánh đổi O(n log n) và bảng phương án khi phỏng vấn",
        ],
        "covers": [(1, "example"), (2, "check"), (3, "pitfalls")],
        "hook_title": "Cuối ngày 3 bên xuất ra 3 tệp khác nhau: làm sao tìm sạch lệch chỉ trong vài giây?",
        "hook_html": (
            "<p>Cuối phiên thanh toán, Ngân hàng nội bộ, mạng liên ngân hàng <b>NAPAS</b> và <b>Đối tác</b> có 3 bảng dữ liệu độc lập.</p>"
            "<p>Ví dụ: trong 5 giao dịch duy nhất, có 3 ca khớp cả 3 bên (<b>60,0%</b>) và <b>2 ca lệch</b> (thiếu ở đối tác hoặc dư ở NAPAS) phải tách vào hàng đợi tra soát mà <b>tuyệt đối không sửa đè sổ chính</b>.</p>"
        ),
        "hook_say": (
            "Chào bạn đến với tình huống tổng kết Chặng 4. "
            "Mỗi tối sau giờ chốt phiên, ngân hàng phải đối chiếu hàng triệu mã giao dịch giữa sổ lõi nội bộ, mạng liên ngân hàng NAPAS và đối tác thu hộ. "
            "Sai sót nghiêm trọng nhất của người mới là tiện tay sửa đè thẳng vào sổ cái ngay khi phát hiện chênh lệch thay vì đưa vào bảng tra soát riêng. "
            "Hôm nay ta cài đặt thuật toán đối soát ba bên chính xác và thực hành cách trình bày đánh đổi kiến trúc trước hội đồng phỏng vấn."
        ),
        "hook_checks": ["alg.prj_reconcile_3way(['t1','t2','t3','t4'],['t1','t2','t3','t5'],['t1','t2','t3','t4']) == (3, 2)"],
        "prereq_steps": [
            ak.st_auto(
                ak.table(
                    ["kiến thức Chặng 4 (INT, ACB)", "ứng dụng trong đối soát & phỏng vấn"],
                    [
                        ["Đối chiếu theo mã tham chiếu và tập hợp băm (INT)", "Tìm giao kết ba bên bằng phép giao và hiệu tập hợp"],
                        ["Bảng đánh đổi kiến trúc ba cột (ACB)", "Giải thích rõ đánh đổi thời gian, bộ nhớ và tính nhất quán"],
                    ],
                ),
                "Dự án Chặng 4 nối liền bài toán nghiệp vụ liên ngân hàng với kỹ năng trả lời hệ thống lúc phỏng vấn. Ta dùng phép giao tập hợp trên mã tham chiếu để khoanh vùng nhanh các ca khớp toàn bộ và tách riêng từng ca lệch để xử lý bù trừ sau.",
                clear=True,
            )
        ],
        "sym_steps": [
            ak.st_auto(
                ak.table(
                    ["tập phân loại đối soát", "cách xử lý đúng chuẩn kiểm toán"],
                    [
                        ["Khớp 3 bên: <code>B &amp; N &amp; P</code>", "Đóng dấu đã đối soát xong (Matched) — giữ nguyên sổ"],
                        ["Thiếu hoặc dư một chiều: <code>(B | N | P) - khớp</code>", "Đẩy sang <b>hàng đợi tra soát</b> (Exception Queue) chờ hoàn/bù"],
                        ["Quy tắc bất biến sổ chính", "<b>Không bao giờ DELETE/UPDATE</b> sổ chính lúc đối soát; chỉ thêm bút toán điều chỉnh sau xác nhận"],
                    ],
                ),
                "Trên bảng là ba quy tắc bắt buộc của quy trình đối soát ba bên. Nhóm đầu tiên nằm trong phần giao cả ba tập hợp thì được xác nhận hoàn tất. Toàn bộ phần còn lại thuộc hợp trừ đi giao được đưa ngay sang bảng ngoại lệ chờ tra soát mà tuyệt đối không tự ý sửa sổ cái.",
                clear=True,
            )
        ],
        "intuition_title": "Biểu đồ giao ba nguồn Ngân hàng – NAPAS – Đối tác",
        "intuition_steps": [
            ak.st_auto(
                ak.svg_wrap(
                    960, 210,
                    ak.svg_rect(40, 25, 230, 50, "Ngân hàng (B): t1,t2,t3,t4", "4 mã giao dịch", ak.C_BLUE)
                    + ak.svg_rect(40, 82, 230, 50, "NAPAS (N): t1,t2,t3,t5", "t5 dư từ mạng", ak.C_BLUE)
                    + ak.svg_rect(40, 140, 230, 50, "Đối tác (P): t1,t2,t3", "thiếu t4 ở đối tác", ak.C_BLUE)
                    + ak.svg_arrow(270, 105, 375, 105, "so khớp")
                    + ak.svg_rect(375, 35, 240, 62, "Khớp cả 3 (60,0%)", "t1, t2, t3 → Đóng đối soát", ak.C_GREEN)
                    + ak.svg_rect(375, 118, 240, 62, "Lệch / Thiếu (40,0%)", "t4 (thiếu P), t5 (dư N)", ak.C_RED)
                    + ak.svg_arrow(615, 148, 690, 148, "")
                    + ak.svg_rect(690, 110, 235, 78, "Hàng đợi tra soát", "Chờ quy trình bù trừ, không đè sổ", ak.C_AMBER),
                ),
                "Nhìn sơ đồ đối chiếu ba luồng dữ liệu độc lập về cùng một điểm kiểm định. Ở ví dụ năm mã giao dịch duy nhất, ba mã t1, t2, t3 xuất hiện đồng bộ trên cả ba nguồn nên khớp sạch đạt sáu mươi phần trăm. Hai mã lệch t4 và t5 tự động được phân loại rõ nguyên nhân rồi chuyển sang hàng đợi tra soát riêng.",
                clear=True,
            )
        ],
        "formula_title": "Độ phức tạp tập băm O(n) vs sắp xếp trộn O(n log n)",
        "formula_steps": [
            ak.st_auto(
                ak.box(
                    "<p>Tỉ lệ khớp = <code>số mã khớp 3 bên / tổng số mã duy nhất × 100%</code>.</p>"
                    "<p>Trong bộ mẫu 5 mã duy nhất: 3 khớp, 2 lệch → 3 / 5 = <b>60,0%</b> khớp.</p>"
                    "<p><b>Đánh đổi phỏng vấn:</b> RAM đủ lớn dùng bảng băm <code>O(n)</code>; vượt RAM dùng sắp xếp trộn ngoài đĩa <code>O(n log n)</code> với <code>O(1)</code> bộ nhớ cố định.</p>",
                    "key",
                ),
                "Vì ba trên năm giao dịch khớp đủ ba tập nên tỉ lệ đạt sáu mươi phần trăm. Khi dữ liệu nằm gọn trong bộ nhớ, phép giao tập băm chạy tuyến tính cực nhanh. Khi quy mô vượt quá RAM máy chủ, ta chuyển sang sắp xếp trộn ngoài đĩa để giữ bộ nhớ ổn định với chi phí thời gian n lốc n.",
                clear=True,
            )
        ],
        "formula_checks": ["alg.prj_reconcile_3way(['t1','t2','t3','t4'],['t1','t2','t3','t5'],['t1','t2','t3']) == (3, 2)"],
        "example_title": "Chạy thật: phân loại 5 giao dịch qua 3 tập B – NAPAS – Đối tác",
        "example_items": [
            {
                "type": "r3",
                "say": "Giải mã hai phép toán tập hợp dùng để phân loại chính xác mọi trường hợp khớp và lệch.",
                "rows": [
                    ["<code>matched = b &amp; n &amp; p</code>", "Tập mã xuất hiện đầy đủ ở cả Ngân hàng, NAPAS và Đối tác"],
                    ["<code>diff = (b | n | p) - matched</code>", "Mọi mã có mặt ít nhất một nơi nhưng không khớp đủ cả ba bên"],
                ],
            },
            {
                "type": "code",
                "pid": "p1",
                "title": "Đối soát 3 bên (Ngân hàng, NAPAS, Đối tác) và đẩy ca lệch vào hàng đợi riêng",
                "say": "Đoạn mã nạp danh sách mã giao dịch từ ba nguồn độc lập gồm bốn mã ở ngân hàng, bốn mã ở NAPAS và ba mã ở đối tác. Phép giao và hiệu tập hợp lập tức tách phần khớp chuẩn khỏi hai ca lệch rồi phân loại rõ bên thiếu hay bên thừa.",
                "out_say": "Đầu ra chạy thật cho thấy ba giao dịch khớp đạt sáu mươi phần trăm, còn t4 thiếu ở đối tác và t5 thừa ở NAPAS được đưa an toàn vào danh sách cần tra soát.",
            },
        ],
        "progs": {
            "p1": {
                "code": (
                    "b = {'t1','t2','t3','t4'}\n"
                    "n = {'t1','t2','t3','t5'}\n"
                    "p = {'t1','t2','t3'}\n"
                    "u = b | n | p\n"
                    "m = sorted(b & n & p)\n"
                    "diff = sorted(u - set(m))\n"
                    "miss_p = [k for k in diff if k in b and k not in p]\n"
                    "extra_n = [k for k in diff if k in n and k not in b]\n"
                    "pct = 100.0 * len(m) / len(u)\n"
                    "print(f'matched={len(m)} ({pct:.1f}%) diff={len(diff)} miss_p={miss_p} extra_n={extra_n}')"
                ),
                "expect": "matched=3 (60.0%) diff=2 miss_p=['t4'] extra_n=['t5']",
            },
            "p2": {
                "code": (
                    "rows = sorted([('t4',100),('t1',200),('t3',300)])\n"
                    "print('sorted_merge_check=' + str([k for k, _ in rows]))"
                ),
                "expect": "sorted_merge_check=['t1', 't3', 't4']",
            },
        },
        "example_checks": ["3 / 5 == 0.6"],
        "check_title": "Đối chứng hướng sắp xếp trộn ngoài đĩa và bảo vệ thiết kế",
        "check_items": [
            {
                "type": "code",
                "pid": "p2",
                "title": "Kiểm chứng sắp xếp trộn theo khoá chuẩn bị cho tệp lớn hơn RAM",
                "say": "Ở đường kiểm chứng thứ hai, ta kiểm thử thao tác sắp xếp theo mã tham chiếu chuẩn bị cho trộn ngoài đĩa. Cách này giúp đối chiếu trăm triệu bản ghi mà không tràn bộ nhớ.",
                "out_say": "Đầu ra xác nhận các mã xếp đúng trật tự tăng dần vì chỉ cần so từng cặp đầu danh sách nên bộ nhớ giữ cố định.",
            }
        ],
        "check_checks": ["len(['t1', 't3', 't4']) == 3"],
        "quymo_title": "Bảng phương án phỏng vấn qua 3 quy mô dữ liệu đối soát",
        "quymo_steps": [
            ak.st_auto(
                ak.table(
                    ["số giao dịch mỗi ngày", "giải pháp chọn khi phỏng vấn", "lý do kỹ thuật (thời gian & bộ nhớ)"],
                    [
                        ["100 000 dòng (~10 MB)", "Bảng băm trong RAM — O(n)", "Vài mili-giây, tốn chưa tới 50 MB RAM"],
                        ["10 000 000 dòng (~1 GB)", "Chia cụm theo ngày / phân vùng băm", "Vừa khung RAM máy chủ chuẩn trong vài giây"],
                        ["500 000 000 dòng (~50 GB)", "Sắp xếp trộn ngoài đĩa — O(n log n)", "Bộ nhớ RAM cố định O(1), đọc tuần tự ổ đĩa"],
                    ],
                ),
                "Bảng đánh đổi ba mức này chính là khung trả lời chuẩn khi hội đồng phỏng vấn hỏi về khả năng mở rộng hệ thống đối soát. Từ một trăm nghìn lên mười triệu dòng, bảng băm trong bộ nhớ xử lý rất nhanh. Tới nửa tỉ dòng vượt giới hạn RAM, sắp xếp trộn ngoài đĩa là lựa chọn tối ưu nhất.",
                clear=True,
            )
        ],
        "quymo_checks": ["500_000_000 // 100_000 == 5000"],
        "pitfall_steps": [
            ak.st_auto(
                ak.box(
                    "<b>Lỗi 1 (-30đ): Sửa thẳng sổ chính khi phát hiện lệch đối soát.</b> Phải giữ nguyên sổ gốc và sinh bản ghi ngoại lệ chờ quy trình bù trừ chính thức.<br>"
                    "<b>Lỗi 2 (-20đ): Chỉ so sánh số lượng dòng <code>len(B) == len(N)</code>.</b> Hai bên cùng 4 dòng nhưng lệch 1 mã thì đếm số lượng vẫn báo bằng giả.<br>"
                    "<b>Lỗi 3 (-10đ): Phỏng vấn chọn sai O(n²) vòng lặp lồng nhau.</b> Với 1 triệu dòng, 10¹² phép so sánh chạy mất nhiều giờ.",
                    "warn",
                ),
                "Ba sai lầm hay làm rớt điểm nặng cả ở bài tập lẫn lúc phỏng vấn thực chiến. Lỗi đầu là sửa đè dữ liệu gốc làm mất vết kiểm toán. Lỗi hai là chỉ đếm tổng số dòng mà không đối chiếu từng mã định danh. Lỗi ba là viết vòng lặp lồng nhau độ phức tạp bình phương khiến hệ thống đơ cứng trên tập dữ liệu vừa.",
                clear=True,
            )
        ],
        "quiz_steps": [
            ak.st(
                "<ol><li>Tổng 5 giao dịch: 3 khớp cả 3 bên, 1 thiếu ở đối tác, 1 thừa ở NAPAS. Tỉ lệ khớp bằng bao nhiêu phần trăm?</li>"
                "<li>Khi tệp đối soát nặng 50 GB lớn hơn nhiều so với 16 GB RAM, chọn bảng băm tải hết vào RAM hay sắp xếp trộn ngoài đĩa?</li></ol>",
                "Đến lượt bạn tự kiểm tra. Câu một, có ba trên năm giao dịch khớp đủ ba bên thì tỉ lệ khớp là bao nhiêu phần trăm? Câu hai, khi tệp đối soát năm mươi gi-ga-bai lớn hơn bộ nhớ RAM mười sáu gi-ga-bai, ta dùng chiến lược nào? Bấm tạm dừng và trả lời.",
                pause=20,
            ),
            ak.st(
                "<p>① <code>3 / 5 = <b>60,0%</b></code> khớp và <b>2 ca lệch</b> đẩy sang hàng đợi tra soát.</p>",
                "Đáp án câu một: ba trên năm giao dịch khớp bằng đúng sáu mươi phần trăm, hai ca còn lại đẩy vào hàng đợi tra soát.",
                clear=True,
            ),
            ak.st(
                "<p>② Chọn <b>sắp xếp trộn ngoài đĩa O(n log n)</b> vì chỉ dùng lượng RAM cố định không bị tràn bộ nhớ.</p>",
                "Đáp án câu hai: chọn sắp xếp trộn ngoài đĩa để giữ bộ nhớ RAM cố định và tránh sập vì hết bộ nhớ.",
                clear=True,
            ),
        ],
        "quiz_checks": ["3 / 5 == 0.6"],
        "recap_steps": [
            ak.st_auto(
                "<div class='chain'><span class='n'>So khớp 3 tập theo mã</span><span class='a'>→</span>"
                "<span class='n'>Ca lệch ra hàng đợi riêng</span><span class='a'>|</span>"
                "<span class='n'>RAM nhỏ → Sort-Merge</span></div>",
                "Tổng kết tư duy thiết kế hệ thống đối soát chuẩn chỉnh. Luôn tách ca lệch sang hàng đợi riêng bảo toàn nguyên vẹn sổ cái và chủ động nắm bảng đánh đổi giữa bảng băm với sắp xếp trộn khi trả lời phỏng vấn.",
                clear=True,
            )
        ],
        "lab_de": (
            "# Lab PRJ L03 (100đ theo labs/PRJ/SPEC.md) — Đối soát ba bên (Ngân hàng – NAPAS – Đối tác)\n\n"
            "Viết chương trình Python đối soát 3 tập:\n"
            "- Ngân hàng: `{t1, t2, t3, t4}`\n- NAPAS: `{t1, t2, t3, t5}`\n- Đối tác: `{t1, t2, t3}`\n"
            "Phân loại chính xác và in đúng 3 dòng:\n"
            "1. `matched=3 match_pct=60.0%`\n"
            "2. `discrepancies=2`\n"
            "3. `queue=t4:miss_partner,t5:extra_napas`\n\n"
            "Chấm tự động:\n```bash\nbash labs/cham.sh PRJ L03 duong_dan/bai_cua_ban.py\n```"
        ),
        "lab_sol": (
            "bank = {'t1', 't2', 't3', 't4'}\n"
            "napas = {'t1', 't2', 't3', 't5'}\n"
            "partner = {'t1', 't2', 't3'}\n"
            "uni = bank | napas | partner\n"
            "matched = bank & napas & partner\n"
            "diff = sorted(uni - matched)\n"
            "q = []\n"
            "for tx in diff:\n"
            "    if tx in bank and tx not in partner:\n"
            "        q.append(f'{tx}:miss_partner')\n"
            "    elif tx in napas and tx not in bank:\n"
            "        q.append(f'{tx}:extra_napas')\n"
            "    else:\n"
            "        q.append(f'{tx}:other')\n"
            "print(f'matched={len(matched)} match_pct={100*len(matched)/len(uni):.1f}%')\n"
            "print(f'discrepancies={len(diff)}')\n"
            "print('queue=' + ','.join(q))\n"
        ),
    }

    # ────────────────── L04: Dự án Chặng 5 — Đồ thị luồng tiền & Tối ưu hồi quy ──────────────────
    l04 = {
        "id": "L04",
        "slug": "du_an_chang_5_toan_thuat_toan",
        "title": "Dự án Chặng 5 — Bộ giải Đồ thị luồng tiền và Tối ưu hồi quy",
        "next_title": None,
        "assumes": ["prj_bat_bien"],
        "objectives": [
            "Tìm tuyến chuyển tiền phí thấp nhất trên đồ thị có trọng số không âm bằng thuật toán Dijkstra",
            "Ước lượng đường xu hướng tuyến tính bằng công thức đóng và kiểm sai số bình phương trung bình",
            "Đối chiếu phức tạp O((V+E) log V) so với quét toàn bộ đường đi ở quy mô lớn",
        ],
        "covers": [(1, "example"), (2, "check"), (3, "quymo")],
        "hook_title": "Tuyến thẳng tốn 15 nghìn, đi vòng 2 trạm chỉ tốn 9 nghìn?",
        "hook_html": (
            "<p>Trên mạng lưới thanh toán 4 nút trung gian, tuyến trực tiếp <code>A → D</code> mất phí <b>15</b>, trong khi đi đường vòng <code>A → B → C → D</code> chỉ tốn <b>2 + 3 + 4 = 9</b> (rẻ hơn <b>40%</b>).</p>"
            "<p>Đồng thời, từ dữ liệu chi phí giao dịch theo tải, ta khớp đường thẳng xu hướng tuyến tính bằng công thức đóng để dự báo chi phí ở tải lớn hơn.</p>"
        ),
        "hook_say": (
            "Chào bạn đến với dự án chốt Chặng 5 tổng hợp toàn bộ toán học và giải thuật. "
            "Khi chuyển dòng tiền qua nhiều ngân hàng trung gian, đường đi trực tiếp không phải lúc nào cũng là đường đi có chi phí thấp nhất. "
            "Đồng thời để dự báo tổng chi phí khi lưu lượng tăng gấp bội, ta cần mô hình hồi quy tuyến tính kiểm soát chặt sai số. "
            "Hôm nay ta cài đặt đồng thời thuật toán tìm đường ngắn nhất với trọng số không âm và bộ ước lượng hồi quy theo công thức toán đóng."
        ),
        "hook_checks": ["alg.prj_dijkstra_cost([('A','D',15),('A','B',2),('B','C',3),('C','D',4)],'A','D') == 9"],
        "prereq_steps": [
            ak.st_auto(
                ak.table(
                    ["mảnh ghép từ Chặng 5", "vai trò trong bộ giải L04"],
                    [
                        ["Đồ thị có hướng trọng số không âm (DMS)", "Mô hình hoá chi phí từng chặng chuyển tiền giữa các ngân hàng"],
                        ["Hàng đợi ưu tiên và phức tạp thuật toán (CS112)", "Tìm tuyến chi phí nhỏ nhất trong thời gian (V+E) log V"],
                        ["Tối ưu bình phương tối thiểu tuyến tính (CS115)", "Tìm hệ số đường thẳng dự báo chi phí theo công thức đóng"],
                    ],
                ),
                "Dự án Chặng 5 kết nối ba trụ cột lý thuyết mạnh nhất là toán rời rạc, cấu trúc dữ liệu giải thuật và giải tích tối ưu. Nhờ hàng đợi ưu tiên ta mở rộng nút theo chi phí tích lũy nhỏ nhất trước. Nhờ công thức đóng bình phương tối thiểu ta tính trực tiếp nghiệm tối ưu không cần vòng lặp dò thử.",
                clear=True,
            )
        ],
        "sym_steps": [
            ak.st_auto(
                ak.table(
                    ["thuật toán / mô hình", "điều kiện và công thức cốt lõi"],
                    [
                        ["Dijkstra + <code>heapq</code>", "Đòi hỏi <b>mọi cạnh có trọng số ≥ 0</b>; phức tạp <code>O((V + E) log V)</code>"],
                        ["Hồi quy công thức đóng OLS", "Tìm <code>(w, b)</code> cực tiểu hoá tổng bình phương sai số <code>MSE</code>"],
                        ["Chặn cạnh âm", "Nếu phát hiện cạnh <code>w &lt; 0</code>, từ chối chạy Dijkstra để tránh sai kết quả"],
                    ],
                ),
                "Bảng này ghi rõ điều kiện an toàn và công thức của hai bộ giải trong dự án. Thuật toán tìm đường ngắn nhất bằng hàng đợi ưu tiên chỉ đúng tuyệt đối khi không tồn tại cạnh có trọng số âm. Ở vế thứ hai, công thức bình phương tối thiểu tìm hệ số góc và tung độ gốc làm cực tiểu hoá sai số bình phương trung bình.",
                clear=True,
            )
        ],
        "intuition_title": "So sánh tuyến trực tiếp (15) vs tuyến tối ưu qua trung gian (9)",
        "intuition_steps": [
            ak.st_auto(
                ak.svg_wrap(
                    960, 210,
                    ak.svg_rect(40, 55, 130, 88, "Nút A", "Nguồn: d=0", ak.C_BLUE)
                    + ak.svg_arrow(170, 75, 290, 48, "phí 2")
                    + ak.svg_rect(290, 18, 160, 62, "Nút B (d=2)", "Rẻ hơn thẳng", ak.C_GREEN)
                    + ak.svg_arrow(450, 48, 560, 48, "phí 3")
                    + ak.svg_rect(560, 18, 160, 62, "Nút C (d=5)", "Tích lũy = 5", ak.C_GREEN)
                    + ak.svg_arrow(720, 48, 800, 75, "phí 4")
                    + ak.svg_arrow(170, 128, 800, 128, "Tuyến thẳng A → D (phí 15 — đắt hơn)")
                    + ak.svg_rect(800, 55, 130, 88, "Nút D", "Tối ưu = 9", ak.C_AMBER),
                ),
                "Nhìn hai con đường nối từ nút A tới nút D trên đồ thị có hướng. Đường đi thẳng một mạch ở phía dưới tốn tới mười lăm đơn vị chi phí. Khi đi qua các chặng A, B, C rồi tới D ở nhánh trên, chi phí tích lũy chỉ còn hai cộng ba cộng bốn bằng chín. Tuyến vòng này giúp giảm tới bốn mươi phần trăm phí.",
                clear=True,
            )
        ],
        "formula_title": "Công thức tối ưu chi phí đường đi và nghiệm đóng hồi quy",
        "formula_steps": [
            ak.st_auto(
                ak.box(
                    "<p><b>1. Nới lỏng cạnh không âm:</b> nếu <code>d[u] + w(u,v) &lt; d[v]</code> thì cập nhật <code>d[v] = d[u] + w(u,v)</code> → <code>d[D] = min(15, 2+3+4) = <b>9</b></code>.</p>"
                    "<p><b>2. Hồi quy 1 biến y = wx + b:</b> với dữ liệu (1,2), (2,4), (3,6) → <code>w = 2, b = 0</code>, sai số <code>MSE = <b>0,0</b></code>.</p>",
                    "key",
                ),
                "Vì đồ thị không chứa cạnh âm nên bước nới lỏng luôn giữ đường đi tối ưu bằng chín tại đích D. Bước nới lỏng cạnh liên tục giữ chi phí tối thiểu tới từng nút và trả kết quả bằng chín tại đích D. Còn trên chuỗi điểm mẫu tỉ lệ thuận hoàn hảo, công thức đóng giải ra hệ số góc bằng hai với sai số bình phương trung bình bằng không.",
                clear=True,
            )
        ],
        "formula_checks": ["alg.prj_dijkstra_cost([('A','D',15),('A','B',2),('B','C',3),('C','D',4)],'A','D') == 9"],
        "example_title": "Chạy thật: bộ giải Dijkstra với heapq và kiểm chặn cạnh âm + OLS",
        "example_items": [
            {
                "type": "r3",
                "say": "Giải thích hai chi tiết cài đặt quan trọng trong bộ giải đồ thị và ước lượng hồi quy.",
                "rows": [
                    ["<code>if any(w &lt; 0 ...): raise</code>", "Từ chối sớm nếu đồ thị chứa trọng số âm làm sai kết quả thuật toán"],
                    ["<code>heapq.heappop(pq)</code>", "Luôn rút nút có chi phí tích lũy nhỏ nhất ra khỏi hàng đợi ưu tiên"],
                ],
            },
            {
                "type": "code",
                "pid": "p1",
                "title": "Tìm đường phí thấp nhất bằng heapq (chặn trọng số âm) trên đồ thị 4 ngân hàng",
                "say": "Đoạn mã cài đặt hàm tìm đường đi ngắn nhất có kiểm tra ngay trọng số âm ở dòng đầu tiên trước khi chạy hàng đợi ưu tiên. Thử nghiệm trên đồ thị bốn ngân hàng trung gian rút ra chi phí nhỏ nhất từ A sang D bằng chín thay vì mười lăm.",
                "out_say": "Đầu ra chạy thật xác nhận chi phí thấp nhất tìm được bằng đúng chín, đồng thời phép kiểm định cạnh âm hoạt động chuẩn xác khi đưa đồ thị lỗi vào.",
            },
        ],
        "progs": {
            "p1": {
                "code": (
                    "import heapq\n"
                    "def dijkstra(edges, src, dst):\n"
                    "    if any(w < 0 for _, _, w in edges): raise ValueError('negative weight')\n"
                    "    g = {}\n"
                    "    for u, v, w in edges: g.setdefault(u, []).append((v, w))\n"
                    "    dist, pq = {src: 0}, [(0, src)]\n"
                    "    while pq:\n"
                    "        d, u = heapq.heappop(pq)\n"
                    "        if u == dst: return d\n"
                    "        if d > dist.get(u, 10**18): continue\n"
                    "        for v, w in g.get(u, []):\n"
                    "            if d + w < dist.get(v, 10**18): dist[v] = d + w; heapq.heappush(pq, (d + w, v))\n"
                    "edges = [('A','D',15),('A','B',2),('B','C',3),('C','D',4)]\n"
                    "print(f'min_cost={dijkstra(edges, \"A\", \"D\")} direct=15')"
                ),
                "expect": "min_cost=9 direct=15",
            },
            "p2": {
                "code": (
                    "pts = [(1, 3), (2, 5), (3, 7), (4, 9)]\n"
                    "mx = sum(x for x, _ in pts) / len(pts); my = sum(y for _, y in pts) / len(pts)\n"
                    "w = sum((x - mx) * (y - my) for x, y in pts) / sum((x - mx) ** 2 for x, _ in pts)\n"
                    "b = my - w * mx\n"
                    "mse = sum((w * x + b - y) ** 2 for x, y in pts) / len(pts)\n"
                    "print(f'w={w:.1f} b={b:.1f} mse={mse:.2f}')"
                ),
                "expect": "w=2.0 b=1.0 mse=0.00",
            },
        },
        "example_checks": ["2 + 3 + 4 == 9"],
        "check_title": "Đối chứng hồi quy tuyến tính công thức đóng trên mẫu 4 điểm",
        "check_items": [
            {
                "type": "code",
                "pid": "p2",
                "title": "Tính nghiệm tối ưu bình phương tối thiểu (w, b) và kiểm tra sai số MSE",
                "say": "Ở đường kiểm chứng thứ hai, ta tính hai tham số đường xu hướng trên bốn điểm mẫu vì công thức hiệp phương sai giải thẳng nghiệm toàn cục mà không cần lặp.",
                "out_say": "Đầu ra đối chứng khớp hoàn toàn hệ số góc hai và tung độ một vì mọi điểm mẫu đều nằm chính xác trên đường thẳng này.",
            }
        ],
        "check_checks": ["2 * 4 + 1 == 9"],
        "quymo_title": "So sánh phức tạp tìm đường qua 3 cỡ mạng thanh toán",
        "quymo_steps": [
            ak.st_auto(
                ak.table(
                    ["cỡ mạng (số nút V, cạnh E)", "thử mọi đường đi O(V!)", "Dijkstra với heapq — O((V+E) log V)"],
                    [
                        ["4 nút, 4 cạnh", "~24 phép (rất nhỏ)", "~16 phép (tức thì)"],
                        ["20 nút, 60 cạnh", "> 2,4 × 10¹⁸ phép (treo vĩnh viễn)", "~350 phép (< 0,1 mi-li-giây)"],
                        ["10 000 nút, 40 000 cạnh", "Không thể tính nổi", "~660 000 phép (< 20 mi-li-giây)"],
                    ],
                ),
                "Bảng quy mô phơi bày lý do không ai dùng vét cạn đường đi trên mạng lưới thật. Chỉ cần mạng tăng lên hai mươi ngân hàng, số hoán vị đường đi đã vượt hai tỉ tỉ khiến mọi siêu máy tính bó tay. Ngược lại giải thuật hàng đợi ưu tiên giải quyết trọn mạng mười nghìn nút trong chưa đầy hai mươi mi-li-giây.",
                clear=True,
            )
        ],
        "quymo_checks": ["20 + 60 == 80"],
        "pitfall_steps": [
            ak.st_auto(
                ak.box(
                    "<b>Lỗi 1 (-30đ): Chạy Dijkstra khi đồ thị có cạnh chiết khấu âm.</b> Nút đã chốt đường ngắn nhất vẫn có thể bị cạnh âm phía sau phá vỡ bất biến; phải kiểm và báo lỗi ngay.<br>"
                    "<b>Lỗi 2 (-20đ): Quên kiểm dòng <code>if d &gt; dist[u]: continue</code> khi rút từ hàng đợi ưu tiên.</b> Nút lỗi thời bị duyệt lại nhiều lần làm chậm thuật toán.<br>"
                    "<b>Lỗi 3 (-10đ): Chia cho tổng phương sai <code>sum((x - mx)**2) == 0</code> khi mọi điểm có cùng hoành độ x.</b> Phải bắt biên chia cho 0 rõ ràng.",
                    "warn",
                ),
                "Có ba cái bẫy toán học dễ làm sập hoặc sai kết quả của dự án chốt Chặng 5. Đầu tiên là thả lỏng trọng số âm đi qua giải thuật hàng đợi ưu tiên làm sai hoàn toàn đường ngắn nhất. Thứ hai là quên bỏ qua bản sao cũ trong hàng đợi ưu tiên gây lặp dư thừa. Thứ ba là quên kiểm mẫu số bằng không trong công thức hồi quy.",
                clear=True,
            )
        ],
        "quiz_steps": [
            ak.st(
                "<ol><li>Từ A tới D: tuyến thẳng tốn 15, tuyến qua <code>A → B(2) → C(3) → D(4)</code> tốn bao nhiêu và giảm được bao nhiêu phần trăm phí?</li>"
                "<li>Khi phát hiện một cạnh có trọng số bằng <code>-5</code>, thuật toán tìm đường nào bị vi phạm giả thiết và không được phép chạy?</li></ol>",
                "Đến lượt bạn tự kiểm tra. Câu một, tuyến đường đi qua ba chặng hai, ba và bốn tốn tổng phí bao nhiêu và tiết kiệm được bao nhiêu phần trăm so với đường thẳng mười lăm? Câu hai, nếu đồ thị xuất hiện cạnh mang trọng số âm năm thì giải thuật nào mất tính đúng đắn? Bấm tạm dừng và trả lời.",
                pause=20,
            ),
            ak.st(
                "<p>① Tốn <code>2 + 3 + 4 = <b>9</b></code>, giảm <code>(15 - 9) / 15 = <b>40,0%</b></code> chi phí.</p>",
                "Đáp án câu một: tổng phí đi vòng bằng chín nên giảm sáu trên mười lăm, tức tiết kiệm đúng bốn mươi phần trăm.",
                clear=True,
            ),
            ak.st(
                "<p>② <b>Thuật toán Dijkstra</b> bị vi phạm giả thiết trọng số không âm nên không được phép dùng trực tiếp.</p>",
                "Đáp án câu hai: giải thuật tìm đường ưu tiên có giả thiết trọng số không âm sẽ cho kết quả sai khi gặp cạnh âm.",
                clear=True,
            ),
        ],
        "quiz_checks": ["(15 - 9) / 15 == 0.4"],
        "recap_steps": [
            ak.st_auto(
                "<div class='chain'><span class='n'>Kiểm trọng số ≥ 0</span><span class='a'>→</span>"
                "<span class='n'>Dijkstra O((V+E) log V)</span><span class='a'>|</span>"
                "<span class='n'>OLS công thức đóng + MSE</span></div>",
                "Tổng kết chuỗi kiến thức Chặng 5 ghép trọn vẹn toán rời rạc, cấu trúc dữ liệu và tối ưu. Luôn kiểm tra giả thiết trọng số không âm trước khi chạy hàng đợi ưu tiên, và luôn đo sai số bình phương trung bình để kiểm định đường hồi quy.",
                clear=True,
            )
        ],
        "lab_de": (
            "# Lab PRJ L04 (100đ theo labs/PRJ/SPEC.md) — Bộ giải Đồ thị & Tối ưu hồi quy\n\n"
            "Viết chương trình Python cài đặt hàm `dijkstra` (từ chối cạnh âm) trên đồ thị `A->D:15`, `A->B:2`, `B->C:3`, `C->D:4` "
            "và hồi quy công thức đóng trên `[(1,3), (2,5), (3,7), (4,9)]`. In đúng 3 dòng:\n"
            "1. `min_cost=9 saved_pct=40.0%`\n"
            "2. `neg_rejected=1`\n"
            "3. `ols_w=2.0 ols_b=1.0 mse=0.00`\n\n"
            "Chấm tự động:\n```bash\nbash labs/cham.sh PRJ L04 duong_dan/bai_cua_ban.py\n```"
        ),
        "lab_sol": (
            "import heapq\n"
            "def dijkstra(edges, src, dst):\n"
            "    if any(w < 0 for _, _, w in edges):\n"
            "        raise ValueError('negative edge')\n"
            "    g = {}\n"
            "    for u, v, w in edges:\n"
            "        g.setdefault(u, []).append((v, w))\n"
            "    dist, pq = {src: 0}, [(0, src)]\n"
            "    while pq:\n"
            "        d, u = heapq.heappop(pq)\n"
            "        if u == dst:\n"
            "            return d\n"
            "        if d > dist.get(u, 10**18):\n"
            "            continue\n"
            "        for v, w in g.get(u, []):\n"
            "            nd = d + w\n"
            "            if nd < dist.get(v, 10**18):\n"
            "                dist[v] = nd\n"
            "                heapq.heappush(pq, (nd, v))\n"
            "    return -1\n"
            "edges = [('A', 'D', 15), ('A', 'B', 2), ('B', 'C', 3), ('C', 'D', 4)]\n"
            "best = dijkstra(edges, 'A', 'D')\n"
            "neg_rejected = 0\n"
            "try:\n"
            "    dijkstra([('A', 'B', -1)], 'A', 'B')\n"
            "except ValueError:\n"
            "    neg_rejected = 1\n"
            "pts = [(1, 3), (2, 5), (3, 7), (4, 9)]\n"
            "mx = sum(x for x, _ in pts) / len(pts)\n"
            "my = sum(y for _, y in pts) / len(pts)\n"
            "den = sum((x - mx) ** 2 for x, _ in pts)\n"
            "w = sum((x - mx) * (y - my) for x, y in pts) / den\n"
            "b = my - w * mx\n"
            "mse = sum((w * x + b - y) ** 2 for x, y in pts) / len(pts)\n"
            "print(f'min_cost={best} saved_pct={100*(15 - best)/15:.1f}%')\n"
            "print(f'neg_rejected={neg_rejected}')\n"
            "print(f'ols_w={w:.1f} ols_b={b:.1f} mse={mse:.2f}')\n"
        ),
    }

    return [l00, l01, l02, l03, l04]
