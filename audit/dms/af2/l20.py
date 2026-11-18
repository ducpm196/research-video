"""DMS L20 → AF2 (WP5 phiên 2): bài hành trình, CẮT lời đọc từ 3 192 xuống ≤ 2 300 từ rồi thêm cảnh practice + lab.
Bài YAML viết tay (CRLF). Script nạp bản gốc đã chép ở audit/dms/af2/base/, bỏ câu (và mục focus tương ứng), bỏ vài step, thêm practice, ghi lại.
Chạy: .venv/Scripts/python -B audit/dms/af2/l20.py  (chạy lại bao nhiêu lần cũng ra cùng kết quả)."""
import re
import shutil
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from af2lib import *  # noqa
from fix6b import *  # noqa
from af2lib import _paths, _write, BASE  # noqa

import yaml

LID = "L20"

# ── lab ──
DE = """# Lab DMS L20 — Tính lại các con số của hành trình hàm băm bằng chương trình

Viết `hamBam.py` (Python 3.11 trở lên); chạy: `python hamBam.py`.

Giả định máy thử một tỉ (10^9) lần mỗi giây (số minh hoạ). In đúng sáu dòng (không dấu):
1. `2^80 = <số nguyên đầy đủ>` — số lần thử vét cạn kiểu ngày sinh cho hàm băm 160 bit (`2 ** 80`)
2. `2^64 lan thu o 1e9 lan moi giay: <số> nam` — số năm (một năm = 31 536 000 giây), làm tròn số nguyên (`round`)
3. `nhanh hon vet can (2^80 / 2^61): <số> lan` — tỉ số `2 ** 80 // 2 ** 61`, cho một tấn công giả định cần `2^61` phép tính
4. `1000000 tep, ma 32 bit: ky vong cap trung gia <số>` — kỳ vọng số cặp tệp trùng mã băm do ngẫu nhiên: `C(1000000, 2) / 2**32`, làm tròn 1 chữ số thập phân
5. `1000000 tep, ma 64 bit: ky vong cap trung gia <số>` — như trên với 64 bit, in bằng định dạng khoa học một chữ số thập phân: `'%.1e' % giá_trị`
6. `ma bang bit can de vet can ngay sinh >= 2^100: <số>` — số bit n nhỏ nhất sao cho `2 ** (n / 2)` đạt ít nhất `2 ** 100` (duyệt n = 1, 2, 3, ...)

Chấm: `bash labs/cham.sh DMS L20 hamBam.py` — in `ĐÚNG` khi đầu ra trùng `mong_doi.txt`.
"""
SOL = r"""from math import comb

print('2^80 =', 2 ** 80)
print('2^64 lan thu o 1e9 lan moi giay:', round(2 ** 64 / 10 ** 9 / 31536000), 'nam')
print('nhanh hon vet can (2^80 / 2^61):', 2 ** 80 // 2 ** 61, 'lan')
print('1000000 tep, ma 32 bit: ky vong cap trung gia', round(comb(1000000, 2) / 2 ** 32, 1))
print('1000000 tep, ma 64 bit: ky vong cap trung gia', '%.1e' % (comb(1000000, 2) / 2 ** 64))
n = 1
while n / 2 < 100:
    n = n + 1
print('ma bang bit can de vet can ngay sinh >= 2^100:', n)"""
EXP = make_lab(LID, DE.replace("hamBam", "hambam"), SOL)
print(EXP)

HINT_BOX = ('<div class="box key"><b>Nếu kẹt:</b> vét cạn ngày sinh cho mã $n$ bit cần $2^{n/2}$ lần thử. Số năm = số lần thử chia $10^9$ chia 31 536 000. Kỳ vọng cặp trùng giả = số cặp chia $2^{n}$, số cặp = $\\binom{k}{2}$ (<code>comb(k, 2)</code>). '
    "Số bit: tìm $n$ nhỏ nhất có $n/2 \\ge 100$. Lời giải ở <code>labs/DMS/L20/loi_giai.py</code> — chỉ mở sau khi đã thử.</div>")
HINT_SAY = ("Nếu kẹt, vét cạn ngày sinh cho mã n bit cần hai mũ n chia hai lần thử. Số năm bằng số lần thử chia một tỉ chia số giây mỗi năm. "
    "Kỳ vọng số cặp trùng giả bằng số cặp chia hai mũ n, với số cặp là tổ hợp chập 2 của số tệp.")
HINT_TAIL = "Lời giải nằm trong thư mục thực hành, và bạn chỉ nên mở sau khi đã thử."
H_HTML, H_SAY, H_FOC = hint_parts2(HINT_BOX, HINT_SAY, [
    ("comb(k, 2)", "hàm có sẵn cho tổ hợp chập 2 của k, tức số cặp trong k phần tử", "comb(4, 2) = 6"),
], [
    "Hàm có sẵn này cho sẵn tổ hợp chập 2 của số tệp, tức số cặp tệp cần đếm.",
], HINT_TAIL)

prac = practice(
    LID, "Tự làm: tính lại số lần thử và kỳ vọng trùng mã cho việc của bạn",
    "<p><b>Đề</b>: viết <code>hambam.py</code> in: $2^{80}$ (vét cạn ngày sinh cho mã 160 bit); số năm cho $2^{64}$ lần thử ở một tỉ lần mỗi giây; tỉ số $2^{80} / 2^{61}$ cho một tấn công giả định; "
    "kỳ vọng số cặp tệp trùng mã giả khi có một triệu tệp với mã 32 bit và 64 bit; và số bit tối thiểu để vét cạn ngày sinh cần ít nhất $2^{100}$ lần (sáu dòng, định dạng ở <code>labs/DMS/L20/de.md</code>).</p>"
    '<p class="note">Số liệu khác ví dụ trong bài. Cuối cùng tự hỏi: với một triệu tệp nội bộ và không ai cố ý làm giả, mã 32 bit hay 64 bit đủ?</p>',
    "Bây giờ tới phần bạn tự làm: tính lại các con số của hành trình cho việc của bạn. "
    "In số lần thử của mã 160 bit, số năm cho hai mũ 64 lần thử, và tỉ số cho một tấn công giả định. Rồi tính kỳ vọng trùng mã giả của một triệu tệp ở hai độ dài, và số bit tối thiểu cho mức hai mũ 100. "
    "Sáu dòng và định dạng nằm trong thư mục thực hành. Hãy dừng video và tự làm.",
    EXP, "hambam.py", H_HTML, H_SAY,
    pause=420, focus1=[1, 1, 1, 1, 0], focus3=H_FOC)
patch_cham(prac, LID, "hambam.py")
prac["id"] = "practice"

# ── cắt: scene.step -> chỉ số câu bỏ (đồng thời bỏ mục focus cùng chỉ số) ──
DROP = {
    "hook.0": [1, 2, 4], "prereq.0": [4, 6], "sym.0": [5], "intuition.0": [0], "funnel.0": [2], "funnel.1": [2],
    "stage1.0": [1, 2], "stage1.1": [0], "stage1.2": [2],
    "stage2.0": [4, 5, 7, 8],
    "stage3.0": [3], "stage3.1": [0, 5],
    "stage4.0": [2, 4], "stage4.1": [0, 5],
    "stage5.0": [1, 2, 3, 4, 6], "stage5.1": [0, 3],
    "check.0": [3, 4, 5], "pitfalls.0": [0, 4], "pitfalls.1": [3], "quiz.1": [1, 3], "quiz.2": [0, 3, 4], "recap.0": [4],
}
DROP_STEPS = {"prereq": [1], "stage2": [1], "stage3": [2]}


def sents(s):
    return [x for x in re.split(r"(?<=[.!?])\s+", s.strip()) if x]


f, _ = _paths(LID)
b = BASE / f.name
BASE.mkdir(exist_ok=True)
if not b.exists():
    shutil.copyfile(f, b)
raw = b.read_bytes()
text = raw.decode("utf-8").replace("\r\n", "\n")
d = yaml.safe_load(text)
words0 = sum(len(str(st.get("say", "")).split()) for s in d["scenes"] for st in s["steps"])
for sc in d["scenes"]:
    keep_steps = []
    for ti, st in enumerate(sc["steps"]):
        if ti in DROP_STEPS.get(sc["id"], []):
            continue
        key = f"{sc['id']}.{ti}"
        if key in DROP:
            ss = sents(str(st["say"]))
            fo = st.get("focus")
            if fo is not None:
                assert len(fo) == len(ss), (key, len(fo), len(ss))
            idx = [i for i in range(len(ss)) if i not in DROP[key]]
            st["say"] = " ".join(ss[i] for i in idx)
            if fo is not None:
                st["focus"] = [fo[i] for i in idx]
        keep_steps.append(st)
    sc["steps"] = keep_steps
# practice trước recap
ri = next(i for i, s in enumerate(d["scenes"]) if s["id"] == "recap")
d["scenes"].insert(ri, prac)
# reader B: sửa lời đọc/hiển thị sau khi cắt
import re as _re
SAYREPL = [
    ("mã dài 20 byte, tức 160 bit", "mã dài 20 byte, mỗi byte là 8 bit, tức 160 bit"),
    # fix6b (P1): "bit" định nghĩa tại lần dùng đầu ở cảnh ôn; rút gọn lời kết để giữ ≤ 2 300 từ
    # fix12 (R8): chủ thể của yêu cầu năm 2006; MD5 (RFC 6151) tách khỏi SHA-1 (suy luận); đếm thuật ngữ khớp lời
    ("Dù vậy, ngày 15 tháng 3 năm 2006, viện yêu cầu thôi dùng SHA-1 cho chữ ký số", "Ngày 15 tháng 3 năm 2006, viện yêu cầu các cơ quan liên bang thôi dùng SHA-1 cho chữ ký số"),
    ("MD5 hay SHA-1 vẫn chấp nhận được.", "MD5 vẫn chấp nhận được theo văn bản năm 2011, còn SHA-1 là suy luận chưa kiểm được nguồn."),
    ("Bài dùng năm thuật ngữ.", "Bài dùng bốn thuật ngữ."),
    # fix12 (giữ ≤ 2 300 từ): bỏ lời dẫn ít giá trị ở các bước không có focus theo câu, rút gọn hai câu
    ("Đây là thước đo của cả hành trình. Một hàm băm", "Một hàm băm"),
    ("Tổng kết lại hành trình. MD5 bị phá khi", "Tổng kết, MD5 bị phá khi"),
    ("khớp với câu nhanh hơn vét cạn hơn 100 nghìn lần.", "khớp với câu hơn 100 nghìn lần."),
    ("hỏi xem có ai cố ý làm giả không, và chuyển đi trước khi", "hỏi có ai cố ý làm giả không, và chuyển trước khi"),
    ("Mã băm 128 bit chỉ có 2 mũ 128 giá trị", "Mã băm 128 bit, tức 128 chữ số nhị phân, chỉ có 2 mũ 128 giá trị"),
    ("Đây là bài cuối của khoá Toán rời rạc, đi từ logic và chứng minh, qua tập hợp, hàm, đếm, số học mô-đun, đồ thị và xác suất rời rạc. Ở bài này,", "Đây là bài cuối của khoá Toán rời rạc. Ở bài này,"),
    ("Ta kiểm lại bốn con số theo đường khác.", "Ta kiểm lại hai trong bốn con số theo đường khác."),
    # fix4 (R2 SHOULD B): nguồn của danh sách tấn công là tài liệu của Git (màn hình và sources_L20.md), không phải viện tiêu chuẩn
    ("Họ liệt kê một kiểu tấn công mạnh hơn", "Còn phía Git liệt kê một kiểu tấn công mạnh hơn"),
]
SHOWREPL = [
    ("<tr><td><b>bị phá</b></td><td>có cách tìm va chạm với số lần thử ít hơn hẳn $2^{n/2}$</td></tr></table>", "</table>"),
    ("MD5 đã bị phá.</p>", "MD5 đã bị phá (có cách tìm va chạm với số lần thử ít hơn hẳn $2^{n/2}$).</p>"),
    ("<td>MD5 hay SHA-1 vẫn chấp nhận được</td>", "<td>MD5 vẫn chấp nhận được (RFC 6151); SHA-1: suy luận tương tự, chưa kiểm được nguồn</td>"),
    ("Mô-đun mật mã dùng cho cơ quan liên bang", "Mô-đun mật mã (phần mềm hoặc thiết bị làm việc mã hoá) dùng cho cơ quan liên bang"),
    ("dù cách dùng này chưa bị phá.", "dù chưa cấp bách phải bỏ cách dùng này."),
    ("mã 128 bit chỉ có $2^{128}$ giá trị", "mã 128 bit (bit là một chữ số nhị phân, 0 hoặc 1) chỉ có $2^{128}$ giá trị"),
    ("chứng chỉ của trang web (TLS)", "chứng chỉ của trang web (giao thức TLS bảo vệ kết nối)"),
]
for sc in d["scenes"]:
    for st in sc["steps"]:
        for o, n in SHOWREPL:
            if o in str(st.get("show", "")):
                st["show"] = st["show"].replace(o, n)
        for o, n in SAYREPL:
            if o in str(st.get("say", "")):
                st["say"] = st["say"].replace(o, n)
    if sc["id"] == "hook":
        # fix4 (R2 SHOULD B): lời đọc nói cả 2004/2007/“10 giây” và “hơn 100 000 lần” như màn hình hook
        hk = sc["steps"][0]
        hk["say"] = ("Chào bạn, năm 1992 có hàm băm MD5 với mã dài 128 bit. "
                     "Năm 2004 có hai cặp tin trùng mã MD5, và tới 2007 tìm một cặp chỉ mất mười giây. "
                     "Năm 2017, cặp trùng đầu tiên của SHA-1 tốn khoảng 6 nghìn 500 năm trên bộ xử lý thường và 100 năm trên bộ xử lý đồ hoạ. "
                     "Con số đó vẫn nhanh hơn vét cạn hơn một trăm nghìn lần.")
        hk["focus"] = [1, 1, 2, 2]
    if sc["id"] == "check":
        sc["title"] = "Tự kiểm hai con số của hành trình bằng đường khác"
        for st in sc["steps"]:
            st["show"] = "\n".join(l for l in st["show"].split("\n") if "<td>1796 ngày</td>" not in l and "2{,}8 \\times 10^{14}" not in l)
# asr_reviewed: bỏ câu không còn
alltext = " ".join(str(st.get("say", "")) for s in d["scenes"] for st in s["steps"])
d["assumes"] = list(d["assumes"]) + ["dms_taphop"]
_asr = (d.get("asr_reviewed") or []) + asr_entries(LID)
for _a in _asr:
    for _o, _n in SAYREPL:
        _a["sentence"] = _a["sentence"].replace(_o, _n)
d["asr_reviewed"] = [a for a in _asr if a["sentence"] in alltext]
words1 = sum(len(str(st.get("say", "")).split()) for s in d["scenes"] for st in s["steps"])
print("lời đọc:", words0, "→", words1)

OBJ = [
    "Kể lại hành trình của hàm băm qua năm chặng từ 2004 tới 2030, mỗi chặng một điểm nghẽn và một cách xử lý",
    "Tính lại số lần thử của vét cạn kiểu ngày sinh, tỉ lệ nhanh hơn vét cạn và khoảng thời gian chuyển đổi",
    "Chọn độ dài mã băm hợp với việc của mình, có hay không có kẻ tấn công, kèm điều kiện đổi lựa chọn",
    "Viết chương trình tính lại số lần thử, số năm và kỳ vọng trùng mã giả cho việc của mình",
]
COVERS = [{"objective": 1, "scene": "intuition"}, {"objective": 2, "scene": "stage3"}, {"objective": 3, "scene": "stage5"}, {"objective": 4, "scene": "practice"}]
new = {}
for k, v in d.items():
    if k == "scenes":
        new["scenes"] = v
        continue
    new[k] = v
    if k == "depth":
        new["af2"] = True
    if k == "objectives":
        new["objectives"] = OBJ
        new["covers"] = COVERS
d = new
body = dump(d)
# giữ khối chú thích quy ước (giữa assumes và objectives) của bản gốc
com = []
lines = text.split("\n")
ai = next(i for i, l in enumerate(lines) if l.startswith("assumes:"))
oi = next(i for i, l in enumerate(lines) if l.startswith("objectives:"))
com = [l for l in lines[ai + 1:oi] if l.startswith("#")]
out = body.split("\n")
oi2 = next(i for i, l in enumerate(out) if l.startswith("objectives:"))
out[oi2:oi2] = com
_write(f, "\n".join(out), crlf=b"\r\n" in raw)
cur_set(LID, OBJ, PYT_EXT)
print(f)
print(ledger_sync(LID, claims=None))
