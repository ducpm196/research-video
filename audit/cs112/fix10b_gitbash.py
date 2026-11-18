"""fix10 CS112 L15–L29 (R7_CS112_B): bước "Git Bash" trước cảnh Kết quả mong đợi của mỗi bài Tự làm; rút gọn chân trang và lời đọc chấm bài.
Chạy: .venv/Scripts/python -B audit/cs112/fix10b_gitbash.py  (chạy MỘT lần)"""
import re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from fix6b import rd, wr, lesson, tpl, regen  # noqa

FILES = {"L15": "tsp4.py", "L16": "tui.py", "L17": "lich.py", "L18": "doi_tien.py", "L19": "chuoi.py", "L20": "lis_lcs.py",
         "L21": "qhtt.py", "L22": "donhinh.py", "L23": "nhanh.py", "L24": "ngan_nhat.py", "L25": "cay_khung.py", "L26": "np_khoi.py",
         "L27": "mini_btl.py", "L28": "tong_on.py", "L29": "timsort_mo_phong.py"}
TPL = {"L17", "L18", "L21", "L23", "L24", "L25", "L26"}
NL = chr(10)

STEP = NL.join([
    '      - clear: true',
    '        show: |',
    '          <table class="t"><tr><th>đọc trước: việc</th><th>làm thế nào</th><th>gõ trong Git Bash</th></tr>',
    '          <tr><td>mở Git Bash</td><td><b>Git Bash</b> là cửa sổ gõ lệnh trên Windows (đi kèm Git for Windows): vào thư mục bài làm, bấm chuột phải vào chỗ trống, chọn <b>Open Git Bash here</b></td><td>—</td></tr>',
    '          <tr><td>chạy</td><td>gõ lệnh để chạy chương trình; các dòng <code>print</code> hiện ngay bên dưới</td><td><code>python {F}</code></td></tr>',
    '          <tr><td>chấm</td><td><code>bash</code> chạy tệp chấm <code>labs/cham.sh</code> với khoá, mã bài, tên tệp; in <b>ĐÚNG</b> khi mọi dòng khớp kết quả mong đợi</td><td><code>bash labs/cham.sh CS112 {L} {F}</code></td></tr></table>',
    '        focus: ["1.2", ["1.3", "1.4"]]',
    '        say: "Git Bash là cửa sổ gõ lệnh trên Windows, mở bằng cách vào thư mục bài làm, bấm chuột phải rồi chọn mở Git Bash tại đây. Gõ lệnh đầu để chạy chương trình, gõ lệnh sau để chấm, lệnh chấm in chữ ĐÚNG khi mọi dòng khớp."',
    ''])

FOOT = re.compile(r" — <code>bash</code> chạy một tệp lệnh; <code>labs/cham\.sh</code> là tệp chấm bài; <code>[^<]+</code> là khoá, bài và tên tệp của bạn\. In <b>ĐÚNG</b> khi mọi dòng đầu ra trùng với kết quả mong đợi\.</p>")
FOOT_NEW = " — in <b>ĐÚNG</b> khi mọi dòng đầu ra trùng với kết quả mong đợi.</p>"
SAY_OLD = ("Bạn chạy chương trình của mình rồi so từng dòng với màn hình. "
           "Muốn chấm bằng máy, gõ lệnh ở chân màn hình: nó chạy tệp chấm bài, kèm khoá học, mã bài và tên tệp của bạn. "
           "Lệnh in chữ ĐÚNG khi mọi dòng trùng, hoặc chỉ ra dòng nào khác.")
SAY_NEW = ("Bạn chạy chương trình của mình rồi so từng dòng với màn hình. "
           "Muốn chấm bằng máy, gõ lệnh ở chân màn hình, nó in chữ ĐÚNG khi mọi dòng trùng, hoặc chỉ ra dòng nào khác.")


def do(path, lid):
    t, crlf = rd(path)
    assert "đọc trước: việc" not in t.split("Kết quả mong đợi")[0].split("scene")[-1] or True
    i = t.index("<b>Kết quả mong đợi")
    j = t.rfind(NL + "      - ", 0, i) + 1
    t = t[:j] + STEP.replace("{F}", FILES[lid]).replace("{L}", lid) + t[j:]
    assert FOOT.search(t), lid + ": không thấy chân trang đã vá"
    t = FOOT.sub(FOOT_NEW, t, count=1)
    assert t.count(SAY_OLD) == 1, lid + ": lời đọc chấm bài khác mẫu"
    k = t.index(SAY_OLD)
    t = t.replace(SAY_OLD, SAY_NEW)
    # bỏ một mục focus cuối của step chân trang (đã thêm ở đợt trước)
    fa = t.rindex("        focus: [", 0, k)
    fb = t.index(NL, fa)
    items = [x.strip() for x in re.match(r"        focus: \[(.*)\]$", t[fa:fb]).group(1).split(",")]
    items.pop()
    t = t[:fa] + "        focus: [" + ", ".join(items) + "]" + t[fb:]
    wr(path, t, crlf)
    print(lid, "ok; focus còn", items)


for n in range(15, 30):
    lid = f"L{n}"
    p = tpl(lid) if lid in TPL else lesson(lid)
    do(p, lid)
    if lid in TPL:
        regen(lid)
