import lib2
from lib2 import *
from labkit import write_lab, practice_steps, practice_scene
from spk12 import spoken

lib2.begin("L12")

# ── Mã hiện trên màn hình: mỗi khối là prog(...) chạy THẬT (đệm ở audit/bnx/progcache/L12.json); đầu ra viết không dấu ASCII ──
LIMIT_PY = """HAN_MUC = 100_000_000   # theo Thông tư 40/2024; kiểm lại văn bản
giao_dich = [30_000_000, 45_000_000, 20_000_000, 10_000_000]
da_dung = 0
for so_tien in giao_dich:
    if da_dung + so_tien > HAN_MUC:
        print("tu choi", so_tien, "da dung", da_dung)
    else:
        da_dung += so_tien
        print("chap nhan", so_tien, "da dung", da_dung)"""
LIMIT_OUT = """chap nhan 30000000 da dung 30000000
chap nhan 45000000 da dung 75000000
chap nhan 20000000 da dung 95000000
tu choi 10000000 da dung 95000000"""
LIMIT = prog("Limit", LIMIT_PY, lang="python", out=LIMIT_OUT,
             claims=["bước 5: ba giao dịch đầu được chấp nhận, tổng chạy lên 95 triệu; giao dịch thứ tư 10 triệu bị từ chối vì 95 + 10 = 105 triệu vượt hạn mức 100 triệu"],
             unverified_claims=["con số 100 000 000 đồng/tháng theo Thông tư 40/2024/TT-NHNN: bản hợp nhất 76/VBHN-NHNN (audit/legal/registry.yaml, CITED LF2); chú thích trên mã và bảng văn bản ghi kiểm lại văn bản hiện hành; loại giao dịch nào tính vào hạn mức không kiểm bằng máy"])

REPLAY_PY = """bao_dam, vi = 500_000, {"A": 0, "B": 0, "C": 500_000}
nhat_ky = [("nap", "A", 2_000_000), ("chuyen", "A", "B", 800_000),
           ("rut", "B", 500_000)]
for g in nhat_ky:
    if g[0] == "chuyen":
        vi[g[1]] -= g[3]
        vi[g[2]] += g[3]
    else:
        dau = 1 if g[0] == "nap" else -1
        vi[g[1]] += dau * g[2]
        bao_dam += dau * g[2]
print(vi, "tong vi", sum(vi.values()), "dam bao", bao_dam)"""
REPLAY_OUT = "{'A': 1200000, 'B': 300000, 'C': 500000} tong vi 2000000 dam bao 2000000"
REPLAY = prog("Replay", REPLAY_PY, lang="python", out=REPLAY_OUT,
              claims=["chạy lại nhật ký: ví A 1 200 000, ví B 300 000, ví C 500 000, tổng 2 000 000, tài khoản đảm bảo 2 000 000 — khớp tính tay (phép ③, ④)"])

TAX_PY = """ngan_hang = {"R1": 1_500_000, "R2": 2_000_000, "R3": 800_000}
kho_bac = {"R1": 1_500_000, "R3": 800_000}
for so_tc, tien in ngan_hang.items():
    if so_tc not in kho_bac:
        print(so_tc, "chua sang Kho bac: phai tra soat")
    elif kho_bac[so_tc] != tien:
        print(so_tc, "lech so tien")
    else:
        print(so_tc, "khop")"""
TAX_OUT = """R1 khop
R2 chua sang Kho bac: phai tra soat
R3 khop"""
TAX = prog("Tax", TAX_PY, lang="python", out=TAX_OUT,
           claims=["bước 6: máy báo R2 chưa sang phía Kho bạc nên ngân hàng chưa xong việc, phải tra soát; R1 và R3 khớp"],
           unverified_claims=["ngày đã nộp thuế = ngày ngân hàng trích tiền (Luật Quản lý thuế 108/2025/QH15 Điều 14 khoản 5, nguồn tổng hợp, chưa đối chiếu bản gốc; luật cũ 38/2019/QH14 Điều 58 hết hiệu lực 30/6/2026) — điều pháp lý, máy không kiểm",
                              "R1, R2, R3 là nhãn minh hoạ (bài nói rõ không phải cấu trúc số thật); cấu trúc số tham chiếu theo Thông tư 19/2021/TT-BTC không dạy vì nguồn đã đọc không nêu"])

# Quy mô: đếm phép so sánh khi đối soát hai danh sách n chứng từ (số tham chiếu 0..n-1, mọi chứng từ đều có ở cả hai bên)
SCALE_PY = """def quet_danh_sach(n):
    kho_bac = list(range(n))
    dem = 0
    for so_nh in range(n):
        for so_kb in kho_bac:
            dem += 1
            if so_kb == so_nh:
                break
    return dem

def tra_bang(n):
    kho_bac = set(range(n))
    dem = 0
    for so_nh in range(n):
        dem += 1
        if so_nh not in kho_bac:
            print("thieu", so_nh)
    return dem

for n in (100, 10_000):
    ds, bt = quet_danh_sach(n), tra_bang(n)
    print("n =", n, "danh sach", ds, "bang tra", bt)
n = 1_000_000
tinh = n * (n + 1) // 2
print("n =", n, "danh sach (tinh)", tinh, "bang tra", tra_bang(n))"""
SCALE_OUT = """n = 100 danh sach 5050 bang tra 100
n = 10000 danh sach 50005000 bang tra 10000
n = 1000000 danh sach (tinh) 500000500000 bang tra 1000000"""
SCALE = prog("Scale", SCALE_PY, lang="python", out=SCALE_OUT, timeout=240,
             claims=["số phép so sánh khi đối soát bằng vòng lặp lồng: 5 050 (n = 100) và 50 005 000 (n = 10 000), đo thật bằng bộ đếm; n = 1 000 000 chỉ tính (n(n+1)/2)",
                     "tra bảng: đúng n lần tra, đo thật ở 100, 10 000 và 1 000 000"])

# Lab (số liệu khác ví dụ): nhật ký 6 dòng có một lệnh rút bị từ chối vì ví không đủ tiền; hạn mức 50 triệu, giao dịch vừa đủ hạn mức vẫn được nhận
LAB_PY = """bao_dam = 250_000
vi = {"X": 0, "Y": 250_000, "Z": 0}
nhat_ky = [("nap", "X", 3_000_000), ("chuyen", "X", "Z", 1_200_000),
           ("rut", "Z", 400_000), ("nap", "Y", 500_000),
           ("rut", "Y", 2_000_000), ("chuyen", "Z", "Y", 300_000)]
for g in nhat_ky:
    if g[0] == "chuyen":
        vi[g[1]] -= g[3]
        vi[g[2]] += g[3]
    elif g[0] == "rut" and vi[g[1]] < g[2]:
        print("tu choi rut", g[1], g[2])
    else:
        dau = 1 if g[0] == "nap" else -1
        vi[g[1]] += dau * g[2]
        bao_dam += dau * g[2]
tong = sum(vi.values())
print("vi", *vi.values())
print("tong vi", tong, "dam bao", bao_dam, "dat", bao_dam >= tong)
HAN_MUC = 50_000_000
da_dung = 0
for so_tien in [20_000_000, 25_000_000, 10_000_000, 5_000_000]:
    if da_dung + so_tien > HAN_MUC:
        print("tu choi", so_tien, "da dung", da_dung)
    else:
        da_dung += so_tien
        print("chap nhan", so_tien, "da dung", da_dung)"""
LABSOL = prog("LabSol", LAB_PY, lang="python", kind="lab")
_p = lib2.PROGRAMS.pop()  # chỉ để chạy: đầu ra thật làm mong_doi.txt
_rc, _so, _se = _p.execute()
assert _rc == 0, _se
LAB_OUT = _so.strip("\n")
EXPECT_LAB = """tu choi rut Y 2000000
vi 1800000 1050000 500000
tong vi 3350000 dam bao 3350000 dat True
chap nhan 20000000 da dung 20000000
chap nhan 25000000 da dung 45000000
tu choi 10000000 da dung 45000000
chap nhan 5000000 da dung 50000000"""
assert LAB_OUT == EXPECT_LAB, LAB_OUT

LAB_DE = """# Lab BNX L12 — Chạy lại nhật ký ví, kiểm bất biến và hạn mức tháng

Số liệu là số minh hoạ. Viết chương trình Python `mau.py` (chỉ dùng Python có sẵn). Dữ liệu cho sẵn, chép vào đầu tệp:

```python
bao_dam = 250_000                    # tài khoản đảm bảo đầu ngày
vi = {"X": 0, "Y": 250_000, "Z": 0}  # số dư ba ví đầu ngày
nhat_ky = [("nap", "X", 3_000_000), ("chuyen", "X", "Z", 1_200_000),
           ("rut", "Z", 400_000), ("nap", "Y", 500_000),
           ("rut", "Y", 2_000_000), ("chuyen", "Z", "Y", 300_000)]
```

**Phần 1 — chạy lại nhật ký.** Duyệt từng dòng theo thứ tự:
- `nap`: ví tăng và tài khoản đảm bảo tăng cùng số tiền;
- `rut`: ví giảm và tài khoản đảm bảo giảm cùng số tiền; nhưng nếu số dư ví **nhỏ hơn** số tiền rút thì **từ chối**: in `tu choi rut <ví> <số tiền>` và không đổi gì;
- `chuyen`: ví đi giảm, ví đến tăng, tài khoản đảm bảo không đổi.

Sau khi duyệt hết, in hai dòng: `vi <số dư X> <số dư Y> <số dư Z>` (ba số cách nhau một dấu cách, ví dụ dùng `print("vi", *vi.values())`) và `tong vi <tổng> dam bao <số> dat <True/False>` (đạt khi tài khoản đảm bảo ≥ tổng ví).

**Phần 2 — hạn mức tháng 50 000 000.** Cộng dồn lần lượt các giao dịch `20_000_000, 25_000_000, 10_000_000, 5_000_000`. Giao dịch nào làm tổng **vượt** hạn mức thì từ chối, giao dịch làm tổng **vừa bằng** hạn mức vẫn được nhận. Mỗi giao dịch in một dòng: `chap nhan <tiền> da dung <tổng đã dùng>` hoặc `tu choi <tiền> da dung <tổng đã dùng>`.

Chạy: `python mau.py`. Chấm: `bash labs/cham.sh BNX L12 mau.py`. Đầu ra viết không dấu để chạy được trên mọi cửa sổ lệnh.
"""


def build():
    write_lab("BNX", "L12", LAB_DE, "py", LAB_PY, LAB_OUT)
    hook = sc("hook", "hook", "Ví hiện 2 000 000 đồng: tiền đó nằm ở đâu?", [
        st("""<p>Bạn nạp <b>2 000 000 đồng</b> từ tài khoản ngân hàng vào ví điện tử, tức ứng dụng giữ tiền để thanh toán. Ứng dụng hiện số dư 2 000 000.</p>
<div class="box key">Nếu máy chủ của công ty vận hành ví hỏng cả ngày, 2 000 000 đó <b>nằm ở đâu</b>? Khi nộp thuế qua ngân hàng, ngày nào là <b>đã nộp</b>, và nếu mỗi ngày có cả triệu khoản nộp thì so khớp chúng chậm tới mức nào?</div>
<span class='note'>(mọi số tiền trong bài là số minh hoạ)</span>""",
           """Chào bạn, giả sử bạn nạp hai triệu đồng từ ngân hàng vào ví điện tử, tức ứng dụng giữ tiền để thanh toán, và ví hiện số dư hai triệu.
           Nếu máy chủ của công ty vận hành ví hỏng cả ngày, thì hai triệu đó nằm ở đâu? Khi nộp thuế qua ngân hàng, ngày nào là ngày đã nộp, và có cả triệu khoản nộp thì so khớp chậm tới mức nào?
           """,
           focus=[1, 2, 2]),
        st(table(["câu hỏi", "phần trả lời trong bài"],
                 [["tiền thật nằm ở đâu", "tài khoản riêng của công ty vận hành ví (<b>tổ chức ví</b>), mở tại ngân hàng: <b>tài khoản đảm bảo thanh toán</b>"],
                  ["nạp, rút, chuyển ghi sổ thế nào", "mỗi việc là một <b>bút toán</b>: một dòng ghi sổ, trừ ở tài khoản này, cộng ở tài khoản kia"],
                  ["luật đòi gì ở tài khoản đảm bảo", "mọi lúc không thấp hơn tổng số dư các ví; cuối ngày đối soát để kiểm"],
                  ["một tháng được dùng bao nhiêu", "cộng dồn, từ chối giao dịch làm vượt <b>hạn mức</b> (mức tối đa)"],
                  ["nộp thuế: ngày nào là đã nộp, ngân hàng xong việc khi nào", "ngày ngân hàng trích tiền; ngân hàng xong khi <b>chứng từ</b> (bản ghi điện tử của khoản nộp) sang <b>Kho bạc</b> (cơ quan nhà nước giữ ngân sách) và hai bên khớp"],
                  ["cả triệu chứng từ: so khớp nhanh hay chậm", "đếm số phép so sánh ở 100, 10 000 và 1 000 000 chứng từ"]]),
           """Bài này trả lời sáu câu hỏi. Tiền thật nằm ở tài khoản đảm bảo thanh toán, tài khoản riêng của tổ chức ví mở tại ngân hàng.
           Nạp, rút và chuyển đều là bút toán, tức một dòng ghi sổ, và mọi lúc tài khoản đảm bảo không được thấp hơn tổng số dư các ví. Mỗi tháng ví cộng dồn và từ chối giao dịch vượt hạn mức.
           Ngân hàng chỉ xong việc nộp thuế khi chứng từ sang Kho bạc, nơi giữ ngân sách nhà nước, và hai bên khớp. Cuối cùng ta đếm việc so khớp ở nhiều cỡ.""",
           clear=True,
           introduces=["bnx_tk_dam_bao", "bnx_chung_tu", "bnx_kho_bac"]),
    ], checks=["alg.bnx_wallet_run(0, {'A': 0}, [('nap', 'A', 2000000)])[1]['A'] == 2000000",
               "alg.bnx_wallet_run(0, {'A': 0}, [('nap', 'A', 2000000)])[0] == 2000000"])

    pre = sc("prereq", "prereq", "Trước hết: năm điều cần hiểu", [
        st(table(["khái niệm", "nghĩa", "ví dụ"],
                 [["① Nợ và Có", "mỗi bút toán ghi Nợ một tài khoản và ghi Có một tài khoản, cùng số tiền; với tài khoản tiền gửi: ghi Nợ là giảm, ghi Có là tăng", "Nợ khách 2 000 000, Có tài khoản khác 2 000 000"],
                  ["② Hai cuốn sổ", "ngân hàng ghi số dư tài khoản; tổ chức ví ghi sổ ví: mỗi khách có bao nhiêu trong ví", "tài khoản 3 000 000; ví 2 000 000"],
                  ["③ Đối soát", "so hai danh sách theo một khoá chung, tìm dòng có bên này mà bên kia không có", "{R1, R2, R3} so với {R1, R3}: lệch R2"],
                  ["④ Cộng dồn", "giữ một tổng chạy, cộng thêm từng giao dịch", "30 + 45 + 20 = 95 (triệu)"],
                  ["⑤ Đọc mã Python", "<code>for x in ds:</code> lặp qua từng phần tử; <code>+=</code> cộng dồn; <code>{khoá: giá trị}</code> là bảng tra theo khoá", "<code>da_dung += 30</code> cộng thêm 30 vào tổng"]]),
           """Trước hết ta cần hiểu năm điều. Một, bút toán ghi Nợ một tài khoản và ghi Có một tài khoản cùng số tiền, và với tài khoản tiền gửi thì Nợ là giảm, Có là tăng.
           Hai, có hai cuốn sổ: ngân hàng ghi số dư tài khoản, còn tổ chức ví ghi sổ ví. Ba, đối soát là so hai danh sách theo một khoá chung để tìm dòng chỉ có ở một bên.
           Bốn, cộng dồn là giữ một tổng chạy rồi cộng thêm từng giao dịch. Năm, mã Python dùng vòng lặp qua từng phần tử, dấu cộng bằng để cộng dồn, và bảng tra theo khoá.""",
           focus=[0, "1.2", "1.3", "1.4", "1.5", "1.6"]),
        st("""$$30 + 45 + 20 = 95 \\text{ triệu đồng}$$""",
           """Một ví dụ số cho cộng dồn: ba mươi triệu cộng bốn mươi lăm triệu cộng hai mươi triệu bằng chín mươi lăm triệu đồng, con số ta dùng lại khi kiểm hạn mức."""),
        st(table(["viết trong mã", "nghĩa", "ví dụ nhỏ"],
                 [["<code>for ma, tien in bang.items():</code>", "lặp qua từng cặp (khoá, giá trị) của bảng tra", "với <code>{\"R1\": 5}</code> thì ma là R1, tien là 5"],
                  ["<code>x not in bang</code>", "x không có trong bảng", "<code>\"R2\" not in {\"R1\": 5}</code> là đúng"],
                  ["<code>g[0]</code>, <code>g[1]</code>", "phần tử thứ nhất, thứ hai của bộ g; máy đếm từ 0", "g = (\"nap\", \"A\", 5) thì g[0] là \"nap\""],
                  ["<code>bao_dam, vi = 500_000, {…}</code>", "dấu phẩy ở hai vế: gán cùng lúc nhiều biến, giá trị thứ nhất cho biến thứ nhất, và tiếp theo", "<code>a, b = 1, 2</code> thì a là 1, b là 2"]]),
           """Mã Python còn vài ký hiệu nữa. Lệnh lấy từng cặp của bảng tra cho ta khoá và giá trị. Cụm không có trong hỏi khoá có vắng không.
           Còn số không trong ngoặc vuông chỉ phần tử đầu của bộ, vì máy đếm từ không. Dấu phẩy ở hai vế gán cùng lúc nhiều biến.""", clear=True),
        st(table(["viết trong mã", "nghĩa", "ví dụ nhỏ"],
                 [["<code>if a: … elif b: … else: …</code>", "thử điều kiện a trước; a sai mới thử b; cả hai sai thì chạy nhánh <code>else</code>", "x = 5: <code>if x &gt; 9</code> sai, <code>elif x &gt; 3</code> đúng, chạy nhánh elif"],
                  ["<code>1 if đk else -1</code>", "lấy 1 nếu điều kiện đúng, ngược lại lấy −1", "<code>1 if 3 &gt; 2 else -1</code> là 1"],
                  ["<code>sum(ds)</code>; <code>a // b</code>", "cộng mọi số trong ds; chia a cho b lấy phần nguyên", "<code>sum([2, 3])</code> là 5; <code>7 // 2</code> là 3"],
                  ["<code>1_000_000</code>; <code>list(range(3))</code>", "gạch dưới chỉ để dễ đọc, bằng một triệu; danh sách các số từ 0 tới 2", "<code>[0, 1, 2]</code>"]]),
           """Cụm nếu, nếu khác, còn lại chạy nhánh đầu tiên có điều kiện đúng. Cụm một nếu điều kiện thì một, nếu không thì âm một, chọn giá trị theo điều kiện. Hàm cộng mọi số, còn hai gạch chéo chia lấy phần nguyên, nên bảy chia hai ra ba.
           Dấu gạch dưới trong số chỉ để dễ đọc, và dãy ba số từ không tới hai là một danh sách.""", clear=True),
    ], checks=["alg.bnx_tax_recon({'R1': 1, 'R2': 1, 'R3': 1}, {'R1': 1, 'R3': 1})['chua_sang'] == ['R2']",
               "alg.bnx_monthly_limit([30, 45, 20], 10**9)[-1][2] == 95",
               "5000000 - 2000000 == 3000000"])

    sym = sc("sym", "symbol", "Giải mã từ ngữ và văn bản pháp lý", [
        st(table(["từ", "nghĩa"],
                 [["tài khoản liên kết", "tài khoản thanh toán hoặc thẻ ghi nợ <b>của chính khách</b>, dùng để nạp và rút"],
                  ["mã định danh khoản phải nộp", "mã gắn với một khoản thuế phải nộp, lấy từ cổng thuế (trang điện tử của cơ quan thuế)"],
                  ["số tham chiếu", "số do ngân hàng tạo cho chứng từ nộp ngân sách, đi kèm số tiền sang phía Kho bạc"],
                  ["hạn mức tháng", "tổng giá trị giao dịch tối đa trong một tháng"]]),
           """Bảng này giải mã bốn từ còn lại. Tài khoản liên kết là tài khoản hoặc thẻ ghi nợ của chính khách, dùng để nạp và rút.
           Mã định danh khoản phải nộp gắn với một khoản thuế, lấy từ cổng thuế, tức trang điện tử của cơ quan thuế. Số tham chiếu là số ngân hàng tạo cho chứng từ nộp ngân sách.
           Hạn mức tháng là tổng giá trị giao dịch tối đa trong một tháng.""",
           focus=[0, "1.2", "1.3", "1.4", "1.5"], introduces=["bnx_so_tham_chieu"]),
        st(table(["văn bản", "điều bài dùng", "tình trạng"],
                 [["Nghị định 52/2024/NĐ-CP", "nghị định nền về thanh toán không dùng tiền mặt (15/5/2024); bài không dẫn điều cụ thể nào của nó", "<span class='note'>cần kiểm lại văn bản hiện hành</span>"],
                  ["Thông tư 40/2024/TT-NHNN (bản hợp nhất 76/VBHN-NHNN; VBHN = văn bản hợp nhất: một bản ghép văn bản ban đầu với các lần sửa)", "Điều 27 khoản 1: tổng số dư các tài khoản đảm bảo không thấp hơn tổng số dư các ví <b>tại cùng một thời điểm</b>; hạn mức: tổng giao dịch qua các ví cá nhân của một khách tại một tổ chức tối đa 100 triệu đồng/tháng (tính chuyển tiền và thanh toán; không tính rút về tài khoản liên kết của chính mình)", "<span class='note'>kiểm lại trước khi áp dụng</span>"],
                  ["Thông tư 41/2025/TT-NHNN", "thêm một hạn mức riêng, không quá 300 triệu đồng/tháng, cho <b>một số</b> khoản thanh toán thiết yếu (dịch vụ công, điện, nước, học phí, viện phí…)", "hiệu lực 05/11/2025"]]),
           """Ba văn bản đầu nói về ví. Nghị định năm mươi hai là nghị định nền về thanh toán không dùng tiền mặt, bài không dẫn điều nào của nó và cần kiểm lại văn bản hiện hành.
           Thông tư bốn mươi là văn bản hợp nhất, tức bản ghép văn bản ban đầu với các lần sửa, và đòi tài khoản đảm bảo không thấp hơn tổng ví. Nó cũng đặt mức một trăm triệu đồng một tháng cho ví cá nhân của một khách.
           Thông tư bốn mươi mốt cho thêm hạn mức riêng tới ba trăm triệu cho một số khoản thiết yếu.""",
           clear=True),
        st(table(["văn bản", "điều bài dùng", "tình trạng"],
                 [["Thông tư 19/2021/TT-BTC", "nộp thuế điện tử: mã định danh khoản phải nộp; ngân hàng tạo số tham chiếu và chuyển cùng số tiền sang ngân hàng nơi Kho bạc mở tài khoản", "<span class='note'>đã sửa đổi, cần kiểm lại</span>"],
                  ["Luật Quản lý thuế 108/2025/QH15, Điều 14 khoản 5", "nộp điện tử: ngày nộp thuế là ngày ngân hàng trích tiền từ tài khoản người nộp", "<span class='note'>thay luật cũ từ 01/7/2026; nguồn tổng hợp, cần kiểm lại</span>"]]),
           """Hai văn bản còn lại nói về nộp thuế. Thông tư mười chín quy định nộp thuế điện tử và đã được sửa, nên cần kiểm lại.
           Luật Quản lý thuế mới thay luật cũ từ tháng bảy năm hai nghìn không trăm hai mươi sáu, và ngày nộp thuế điện tử là ngày ngân hàng trích tiền.""",
           focus=[0, "1.2", "1.3"], clear=True),
    ], checks=["[x[1] for x in alg.bnx_monthly_limit([100_000_000, 1], 100_000_000)] == [True, False]",
               "[x[1] for x in alg.bnx_monthly_limit([100_000_000, 1], 300_000_000)] == [True, True]",
               "300_000_000 // 100_000_000 == 3"])

    intu = sc("intuition", "intuition", "Hình dung: tiền thật ở ngân hàng, và đường đi của tiền thuế", [
        st(svg(1500, 480,
               panel(20, 20, 700, 380, "Ngân hàng: tiền thật", C_BLUE),
               box(60, 100, 620, 100, ["tài khoản của khách A", "5 000 000 → 3 000 000"], C_GRAY, size=22),
               box(60, 260, 620, 100, ["tài khoản đảm bảo của tổ chức ví", "500 000 → 2 500 000"], C_GREEN, size=22, bold=True),
               arrow(370, 205, 370, 255, "#16a34a"),
               txt(560, 240, "nạp 2 000 000", 22, "middle", "#16a34a", True),
               panel(780, 20, 700, 380, "Tổ chức ví: sổ ghi", C_PURPLE),
               box(820, 100, 620, 80, "ví A: 0 → 2 000 000", C_GRAY, size=22),
               box(820, 200, 620, 80, "ví C: 500 000", C_GRAY, size=22),
               box(820, 300, 620, 80, "tổng ví: 500 000 → 2 500 000", C_PURPLE, size=22, bold=True),
               txt(750, 455, "Mọi lúc (kiểm cuối ngày): tài khoản đảm bảo 2 500 000 không thấp hơn tổng ví 2 500 000", 24, "middle", "#1f2937", True)),
           """Hình có hai cuốn sổ. Bên trái là ngân hàng: khách A nạp hai triệu nên tài khoản của A còn ba triệu, tài khoản đảm bảo thành hai triệu năm trăm nghìn.
           Bên phải là sổ ví, chỉ ghi ai có bao nhiêu: ví A thành hai triệu nên tổng ví cũng hai triệu năm trăm nghìn, và cuối ngày ta đối soát."""),
        st(svg(1500, 470,
               box(10, 150, 240, 130, ["Người nộp thuế", "chọn khoản nộp"], C_BLUE, bold=True, size=22),
               box(300, 150, 260, 130, ["Cổng thuế", "mã định danh", "khoản phải nộp"], C_PURPLE, bold=True, size=22),
               box(610, 150, 270, 130, ["Ngân hàng", "trích nợ tài khoản,", "tạo số tham chiếu"], C_AMBER, bold=True, size=22),
               box(930, 150, 280, 130, ["Ngân hàng nơi", "Kho bạc mở", "tài khoản"], C_GREEN, bold=True, size=22),
               box(1260, 150, 230, 130, ["Kho bạc", "Nhà nước"], C_GREEN, bold=True, size=22),
               arrow(250, 215, 295, 215), arrow(560, 215, 605, 215), arrow(880, 215, 925, 215, "#475569"), arrow(1210, 215, 1255, 215),
               txt(905, 130, "tiền + số tham chiếu", 20, "middle", "#475569"),
               arrow(1070, 300, 760, 300, "#dc2626", dash=True),
               txt(915, 345, "đối soát theo số tham chiếu", 22, "middle", "#dc2626", True),
               txt(750, 410, "Ngày đã nộp thuế = ngày ngân hàng trích tiền (Luật Quản lý thuế 2025, Điều 14: cần kiểm lại)", 22, "middle", "#1f2937", True),
               txt(750, 448, "Chứng từ chưa sang phía Kho bạc thì ngân hàng CHƯA xong việc: phải tra soát, xử lý", 22, "middle", "#dc2626", True)),
           """Hình thứ hai là luồng nộp thuế điện tử. Người nộp chọn khoản nộp trên cổng thuế, rồi ngân hàng trích tiền và tạo số tham chiếu cho chứng từ.
           Ngân hàng chuyển tiền cùng số tham chiếu sang ngân hàng nơi Kho bạc mở tài khoản, và hai bên đối soát theo số đó."""),
    ])

    form = sc("formula", "formula", "Suy ra từng bước: nạp, chuyển, rút, bất biến, hạn mức, thuế", [
        st(table(["Bước 1: nạp 2 000 000", "sổ ngân hàng", "sổ ví"],
                 [["ghi", "Nợ tài khoản khách A 2 000 000; Có tài khoản đảm bảo 2 000 000", "ví A tăng 2 000 000"],
                  ["vì sao", "tiền thật rời tài khoản của khách sang tài khoản đảm bảo", "tổ chức ví nợ khách thêm 2 000 000"]]),
           """Bước một là nạp hai triệu. Sổ ngân hàng ghi Nợ tài khoản khách A và ghi Có tài khoản đảm bảo, vì tiền thật chuyển sang đó.
           Sổ ví cộng hai triệu cho ví A, vì tổ chức ví nợ khách thêm hai triệu.""",
           focus=[0, "1.2", "1.3"]),
        st(table(["Bước 2: ví A chuyển ví B 800 000", "sổ ngân hàng", "sổ ví"],
                 [["ghi", "không có bút toán", "ví A giảm 800 000; ví B tăng 800 000"],
                  ["vì sao", "hai ví cùng một tổ chức: tiền thật vẫn nằm yên ở tài khoản đảm bảo", "tổng ví không đổi"]]),
           """Bước hai, ví A chuyển cho ví B tám trăm nghìn. Sổ ngân hàng không có bút toán vì tiền thật vẫn ở tài khoản đảm bảo, còn sổ ví ghi A giảm, B tăng nên tổng ví không đổi.""",
           focus=[0, ["1.2", "1.3"]], clear=True),
        st(table(["Bước 3: ví B rút 500 000", "sổ ngân hàng", "sổ ví"],
                 [["điều kiện", "—", "số dư ví B (800 000) ≥ 500 000; nếu thiếu thì từ chối"],
                  ["ghi", "Nợ tài khoản đảm bảo 500 000; Có tài khoản khách B 500 000", "ví B giảm 500 000"],
                  ["vì sao", "tiền thật ra khỏi tài khoản đảm bảo, về tài khoản liên kết của B", "tổ chức ví bớt nợ B 500 000"]]),
           """Bước ba, ví B rút năm trăm nghìn, và chỉ được rút khi số dư ví đủ, thiếu thì từ chối. Sổ ngân hàng ghi Nợ tài khoản đảm bảo và ghi Có tài khoản khách B, vì tiền thật ra khỏi đó.
           Sổ ví giảm ví B năm trăm nghìn.""",
           focus=["1.2", "1.3", "1.3"], clear=True),
        st("""<p><b>Bước 4.</b> Nạp và rút đổi tài khoản đảm bảo và tổng ví <b>cùng một lượng</b>; chuyển ví → ví không đổi cả hai. Vì vậy hiệu giữ nguyên qua mọi giao dịch đúng, gọi là <b>bất biến</b> (điều luôn đúng suốt quá trình):</p>
$$\\text{đảm bảo} - \\text{tổng ví} \\geq 0$$
<span class='note'>Làm thử: đầu ngày 500 000 − 500 000 = 0; sau ba bước 2 000 000 − 2 000 000 = 0. Hiệu đổi mà không có giao dịch giải thích được là có lỗi.</span>""",
           """Bước bốn là bất biến, tức điều luôn đúng suốt quá trình. Nạp và rút đổi tài khoản đảm bảo và tổng ví cùng một lượng, chuyển ví sang ví không đổi cả hai, nên hiệu của chúng giữ nguyên và phải lớn hơn hoặc bằng không.
           Làm thử: đầu ngày năm trăm nghìn trừ năm trăm nghìn bằng không, sau ba bước hai triệu trừ hai triệu vẫn bằng không.""",
           focus=[1, 2, 3], clear=True),
        st(LIMIT.show() + LIMIT.out_html(title="Bước 5 — kết quả chạy thật: từ chối giao dịch làm vượt hạn mức"),
           """Bước năm là hạn mức tháng. Chương trình giữ tổng đã dùng và trước mỗi giao dịch kiểm xem cộng thêm có vượt một trăm triệu không.
           Ba giao dịch đầu được nhận, tổng lên chín mươi lăm triệu, còn giao dịch mười triệu thứ tư bị từ chối vì chín mươi lăm cộng mười là một trăm lẻ năm triệu.""",
           focus=[1, ["1.5"], ["3.1", "3.2", "3.3", "3.4"]], clear=True),
        st(TAX.show() + TAX.out_html(title="Bước 6 — kết quả chạy thật (R1, R2, R3 là nhãn minh hoạ)"),
           """Bước sáu là đối soát nộp thuế theo số tham chiếu, ở đây ghi tạm R một, R hai, R ba. Ngân hàng đã trích tiền cả ba chứng từ, nhưng Kho bạc mới có R một và R ba, nên máy báo R hai chưa sang và ngân hàng phải tra soát.""",
           focus=[["1.1", "1.2"], ["3.2", "1.4"]], clear=True),
    ], checks=["alg.bnx_wallet_run(500000, {'A': 0, 'B': 0, 'C': 500000}, [('nap', 'A', 2000000)])[3] == [('tiền gửi khách A', 'đảm bảo thanh toán', 2000000)]",
               "(lambda r: r[0] == 2500000 and sum(r[1].values()) == 2500000)(alg.bnx_wallet_run(500000, {'A': 0, 'B': 0, 'C': 500000}, [('nap', 'A', 2000000), ('chuyen', 'A', 'B', 800000)]))",
               "alg.bnx_wallet_run(500000, {'A': 0, 'B': 0, 'C': 500000}, [('nap', 'A', 2000000), ('chuyen', 'A', 'B', 800000)])[3] == [('tiền gửi khách A', 'đảm bảo thanh toán', 2000000)]",
               "alg.bnx_wallet_run(2500000, {'A': 1200000, 'B': 800000, 'C': 500000}, [('rut', 'B', 500000)])[3] == [('đảm bảo thanh toán', 'tiền gửi khách B', 500000)]",
               "800000 >= 500000",
               "alg.bnx_invariant(500000, {'C': 500000})[2] == 0 and alg.bnx_invariant(2000000, [500000, 1200000, 300000])[2] == 0",
               "alg.bnx_monthly_limit([30_000_000, 45_000_000, 20_000_000, 10_000_000], 100_000_000) == [(30000000, True, 30000000), (45000000, True, 75000000), (20000000, True, 95000000), (10000000, False, 95000000)]",
               "95_000_000 + 10_000_000 > 100_000_000",
               "alg.bnx_tax_recon({'R1': 1500000, 'R2': 2000000, 'R3': 800000}, {'R1': 1500000, 'R3': 800000}) == {'khop': ['R1', 'R3'], 'chua_sang': ['R2'], 'lech_tien': [], 'thua': []}"])

    ex = sc("example", "example", "Ví dụ một ngày của ba ví, từng phép tính", [
        st("""<p>Đầu ngày: tài khoản khách A <b>5 000 000</b>; ví A 0, ví B 0, ví C <b>500 000</b>; tài khoản đảm bảo <b>500 000</b>. <span class='note'>(số minh hoạ)</span></p>
$$① \\; \\text{nạp: }5\\,000\\,000 - 2\\,000\\,000 = \\hl{3\\,000\\,000};\\quad 500\\,000 + 2\\,000\\,000 = \\hl{2\\,500\\,000}$$""",
           """Đầu ngày tài khoản khách A có năm triệu, ví C và tài khoản đảm bảo mỗi bên năm trăm nghìn. A nạp hai triệu: tài khoản của A còn ba triệu, tài khoản đảm bảo thành hai triệu năm trăm nghìn.""", clear=True),
        st("""<p>Dùng lại ví A = 2 000 000 ở phép ①.</p>
$$② \\; \\text{A chuyển B: } 2\\,000\\,000 - 800\\,000 = \\hl{1\\,200\\,000};\\quad \\text{ví B} = 800\\,000$$""",
           """A chuyển cho B tám trăm nghìn: ví A còn một triệu hai trăm nghìn, ví B có tám trăm nghìn, tài khoản đảm bảo không đổi.""", clear=True),
        st("""$$③ \\; \\text{B rút: } 800\\,000 - 500\\,000 = \\hl{300\\,000};\\quad 2\\,500\\,000 - 500\\,000 = \\hl{2\\,000\\,000}$$""",
           """B rút năm trăm nghìn: ví B còn ba trăm nghìn, tài khoản đảm bảo còn hai triệu.""", clear=True),
        st("""$$④ \\; \\text{tổng ví} = 500\\,000 + 1\\,200\\,000 + 300\\,000 = \\hl{2\\,000\\,000}$$""",
           """Tổng ba ví là năm trăm nghìn cộng một triệu hai trăm nghìn cộng ba trăm nghìn, bằng hai triệu.""", clear=True),
        st("""$$⑤ \\; 2\\,000\\,000 \\geq 2\\,000\\,000 \\;\\Rightarrow\\; \\hlg{\\text{đạt, phần dư } 0}$$""",
           """Hai triệu lớn hơn hoặc bằng hai triệu nên bất biến đạt, phần dư bằng không.""", clear=True),
    ], checks=["alg.bnx_wallet_run(500000, {'A': 0, 'B': 0, 'C': 500000}, [('nap', 'A', 2000000)], {'A': 5000000})[2]['A'] == 3000000",
               "alg.bnx_wallet_run(500000, {'A': 0, 'B': 0, 'C': 500000}, [('nap', 'A', 2000000)])[0] == 2500000",
               "alg.bnx_wallet_run(500000, {'A': 0, 'B': 0, 'C': 500000}, [('nap', 'A', 2000000), ('chuyen', 'A', 'B', 800000)])[1] == {'A': 1200000, 'B': 800000, 'C': 500000}",
               "(lambda r: r[1]['B'] == 300000 and r[0] == 2000000)(alg.bnx_wallet_run(500000, {'A': 0, 'B': 0, 'C': 500000}, [('nap', 'A', 2000000), ('chuyen', 'A', 'B', 800000), ('rut', 'B', 500000)]))",
               "alg.bnx_invariant(2000000, [500000, 1200000, 300000]) == (True, 2000000, 0)"])

    chk = sc("check", "check", "Tự kiểm bằng đường khác: chạy lại cả nhật ký từ đầu ngày", [
        st(REPLAY.show() + REPLAY.out_html(title="Kết quả chạy thật: chạy lại nhật ký, không đọc số dư đã lưu"),
           """Kiểm bằng đường khác: vì số tính tay có thể sai, ta cho Python chạy lại cả nhật ký từ số đầu ngày. Chuyển ví sang ví chỉ đổi hai ví, còn nạp và rút đổi cả ví lẫn tài khoản đảm bảo.
           Máy in ba số dư ví, còn tổng ví và tài khoản đảm bảo cùng là hai triệu.""",
           focus=[1, ["1.6", "1.7", "1.10", "1.11"], "3.1"], clear=True),
        st(table(["cách tính", "tài khoản đảm bảo", "tổng ví"],
                 [["tính tay ở phép ③ và ④", "2 000 000", "2 000 000"],
                  ["chạy lại nhật ký", "500 000 + 2 000 000 − 500 000 = 2 000 000", "2 000 000"],
                  ["sổ ngân hàng: Có trừ Nợ của tài khoản đảm bảo", "2 000 000 − 500 000 = 1 500 000 trong ngày, cộng 500 000 đầu ngày", "—"]]),
           """Bảng đặt ba cách tính cạnh nhau, và cả ba cùng cho hai triệu nên đáng tin. Cách thứ ba đọc sổ ngân hàng: trong ngày tài khoản đảm bảo tăng một triệu năm trăm nghìn, cộng năm trăm nghìn đầu ngày là hai triệu.""",
           focus=[["1.2", "1.3"], "1.4"], clear=True),
    ], checks=["(lambda r: r[0] == 2000000 and r[1] == {'A': 1200000, 'B': 300000, 'C': 500000})(alg.bnx_wallet_run(500000, {'A': 0, 'B': 0, 'C': 500000}, [('nap', 'A', 2000000), ('chuyen', 'A', 'B', 800000), ('rut', 'B', 500000)]))",
               "500000 + sum(a if cr == 'đảm bảo thanh toán' else -a for dr, cr, a in alg.bnx_wallet_run(500000, {'A': 0, 'B': 0, 'C': 500000}, [('nap', 'A', 2000000), ('chuyen', 'A', 'B', 800000), ('rut', 'B', 500000)])[3]) == 2000000",
               "2000000 - 500000 == 1500000 and 1500000 + 500000 == 2000000"])

    quymo = sc("quymo", "example", "Khi số chứng từ lớn dần: đối soát chậm tới đâu", [
        st(SCALE.show(lines=(1, 9), title="Cách 1: với mỗi chứng từ ngân hàng, quét danh sách của Kho bạc tới khi gặp")
           + """<p class="note"><code>def</code> định nghĩa hàm; <code>return</code> trả kết quả; <code>range(n)</code> là dãy 0 tới n−1; <code>break</code> thoát vòng lặp; <b>vòng lặp lồng</b> là vòng này nằm trong vòng kia; <code>set</code> (bước sau) là tập hợp tra nhanh.</p>""",
           """Đối soát chạy hằng ngày, nên ta xem nó đổi thế nào khi số chứng từ n lớn dần. Cách một dùng vòng lặp lồng, tức vòng trong quét danh sách của Kho bạc từ đầu tới khi gặp, còn biến đếm ghi số phép so sánh.
           Chứng từ thứ i phải quét i phần tử mới gặp, nên n chứng từ tốn một cộng hai cộng dần tới n phép, tức n nhân n cộng một rồi chia hai.""",
           focus=[2, ["2.5", "2.6"], ["2.3", "2.4", "2.5"]], clear=True),
        st(SCALE.show(lines=(11, 18), title="Cách 2: đưa danh sách Kho bạc vào bảng tra (tập hợp), mỗi chứng từ chỉ tra một lần"),
           """Cách hai đưa danh sách của Kho bạc vào một bảng tra, hỏi có hay không gần như tức thì. Mỗi chứng từ chỉ tra một lần, và biến đếm ghi số lần tra.""",
           focus=[["2.2"], ["2.4", "2.5", "2.6"]], clear=True),
        st(SCALE.show(lines=(20, 25), title="Chạy ở 100, 10 000 và 1 000 000 chứng từ") + SCALE.out_html()
           + """<p class="note">Ở 1 000 000, cách 1 chỉ <b>tính</b> bằng công thức n(n+1)/2: chứng từ thứ i phải quét i phần tử mới gặp, nên tổng là 1 + 2 + … + n; chạy thật sẽ rất lâu.</p>""",
           """Ta chạy ở một trăm, mười nghìn và một triệu chứng từ. Cách một đo thật ở hai cỡ đầu, còn mức một triệu chỉ tính bằng công thức, vì chạy thật sẽ rất lâu. Cách hai đo thật ở cả ba cỡ.""",
           focus=[2, ["4.1", "4.2", "4.3", "5"], ["4.1", "4.2", "4.3"]], clear=True),
        st(table(["số chứng từ n", "cách 1: số phép so sánh", "chờ nếu 50 ns mỗi phép (số minh hoạ)", "cách 2: số lần tra", "chờ nếu 50 ns mỗi lần (số minh hoạ)"],
                 [["100 (×1)", "5 050 (đo)", "0,25 ms (phần nghìn giây)", "100 (đo)", "5 µs (phần triệu giây)"],
                  ["10 000 (×100)", "50 005 000 (đo)", "2,5 giây", "10 000 (đo)", "0,5 ms"],
                  ["1 000 000 (×10 000)", "500 000 500 000 (tính)", "25 000 giây, gần 7 giờ", "1 000 000 (đo)", "0,05 giây"]]),
           """Dữ liệu tăng một trăm lần thì cách một tăng gần mười nghìn lần, từ hơn năm nghìn lên hơn năm mươi triệu phép. Với số minh hoạ năm mươi nano giây mỗi phép, tức năm mươi phần tỉ giây, một triệu chứng từ tốn gần bảy giờ ở cách một, còn cách hai chỉ chừng năm mươi mili giây.""",
           focus=[["1.2", "1.3"], "1.4"], clear=True),
        st(table(["cách", "được", "mất", "khi nào chọn"],
                 [["quét danh sách (vòng lặp lồng)", "đơn giản, không tốn thêm bộ nhớ", "số phép tăng theo n nhân n (bình phương của n)", "vài chục chứng từ"],
                  ["bảng tra", "số lần tra tăng đúng theo n", "tốn bộ nhớ cho cả bảng (ở đây một triệu mục)", "từ hàng nghìn tới vài triệu chứng từ vừa bộ nhớ"],
                  ["để cơ sở dữ liệu ghép hai bảng theo một cột chung (phép nối bảng), hoặc sắp xếp hai tệp rồi đọc song song", "không phải nạp hết vào bộ nhớ", "phải dựng chỉ mục (mục lục để tra nhanh) hoặc thêm bước sắp xếp; bài này không chạy thử", "dữ liệu quá lớn, không vừa bộ nhớ"]]),
           """Quét danh sách đơn giản và không tốn bộ nhớ nhưng chỉ hợp vài chục chứng từ. Bảng tra đổi bộ nhớ lấy tốc độ, hợp tới vài triệu chứng từ.
           Dữ liệu lớn hơn nữa thì để cơ sở dữ liệu ghép hai bảng theo cột chung, hoặc sắp xếp hai tệp rồi đọc song song, hướng này ta chưa chạy thử.""",
           focus=["1.2", "1.3", "1.4"], clear=True),
    ], checks=["[alg.bnx_l12_scan_cmp(n) for n in (100, 10_000, 1_000_000)] == [5050, 50_005_000, 500_000_500_000]",
               "[alg.bnx_l12_lookup_cmp(n) for n in (100, 10_000, 1_000_000)] == [100, 10_000, 1_000_000]",
               "[alg.bnx_l12_time_s(alg.bnx_l12_scan_cmp(n), 50) for n in (100, 10_000)] == [0.0002525, 2.50025]",
               "round(alg.bnx_l12_time_s(alg.bnx_l12_scan_cmp(1_000_000), 50)) == 25000 and 6.9 < alg.bnx_l12_time_s(alg.bnx_l12_scan_cmp(1_000_000), 50) / 3600 < 7",
               "[alg.bnx_l12_time_s(alg.bnx_l12_lookup_cmp(n), 50) for n in (100, 10_000, 1_000_000)] == [0.000005, 0.0005, 0.05]",
               "9900 < alg.bnx_l12_scan_cmp(10_000) / alg.bnx_l12_scan_cmp(100) < 9910",
               "10_000 // 100 == 100 and 1_000_000 // 100 == 10_000"])

    pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st("""<div class="box warn"><b>Lỗi 1 (người mới).</b> Nghĩ tiền “nằm trong ví” hay trong máy chủ của ứng dụng. Tiền thật nằm ở <b>tài khoản đảm bảo thanh toán tại ngân hàng</b>; sổ ví chỉ ghi tổ chức ví đang nợ mỗi khách bao nhiêu.
<br><span class="note">Phép thử: hỏi “số này khớp với số dư tài khoản nào ở ngân hàng?”</span></div>""",
           """Lỗi của người mới là nghĩ tiền nằm trong ví hay trong máy chủ ứng dụng. Tiền thật nằm ở tài khoản đảm bảo tại ngân hàng, nên hãy hỏi số này khớp với số dư tài khoản nào."""),
        st("""<div class="box warn"><b>Lỗi 2 (người đã đi làm).</b> Ghi tăng sổ ví <b>trước</b> khi ngân hàng xác nhận đã trích nợ. Lệnh nạp 1 000 000 hết giờ chờ, ngân hàng thật ra chưa trích, nhưng ví đã cộng:</div>
$$2\\,000\\,000 + 1\\,000\\,000 = 3\\,000\\,000 \\;>\\; 2\\,000\\,000 \\;\\Rightarrow\\; \\text{thiếu } 1\\,000\\,000$$
<span class="note">Phép thử: đối soát cuối ngày bắt được. Cách chữa: chỉ cộng ví khi có xác nhận; hỏi lại trạng thái lệnh hết giờ chờ.</span>""",
           """Lỗi của người đã đi làm là ghi tăng sổ ví trước khi ngân hàng xác nhận trích nợ. Lệnh nạp một triệu hết giờ chờ mà ví đã cộng thì tổng ví thành ba triệu, lớn hơn tài khoản đảm bảo hai triệu, thiếu một triệu.
           Cách chữa là chỉ cộng ví khi có xác nhận, và hỏi lại trạng thái lệnh hết giờ.""",
           focus=[[1, 2], 3], clear=True),
        st("""<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> Viết cứng <code>100_000_000</code> trong mã. Khi Thông tư 41/2025 cho thêm hạn mức riêng tới 300 triệu cho <b>một số</b> khoản thanh toán thiết yếu, hệ thống từ chối sai, hoặc sửa vội thành 300 triệu cho mọi loại.
<br><span class="note">Cách chữa: hạn mức là cấu hình gắn văn bản, ngày hiệu lực và loại giao dịch (kiểm lại văn bản hiện hành).</span></div>""",
           """Lỗi thứ ba là viết cứng một trăm triệu trong mã. Khi Thông tư bốn mươi mốt cho thêm hạn mức ba trăm triệu cho một số khoản thiết yếu, hệ thống từ chối sai hoặc bị sửa vội cho mọi loại.
           Hãy để hạn mức thành cấu hình gắn với văn bản, ngày hiệu lực và loại giao dịch.""",
           clear=True),
    ], checks=["alg.bnx_invariant(2000000, [2000000 + 1000000]) == (False, 3000000, -1000000)",
               "[x[1] for x in alg.bnx_monthly_limit([95_000_000, 10_000_000], 100_000_000)] == [True, False]",
               "[x[1] for x in alg.bnx_monthly_limit([95_000_000, 10_000_000], 300_000_000)] == [True, True]"])

    quiz = sc("quiz", "quiz", "Đến lượt bạn", [
        st(table(["câu", "đề"],
                 [["1", "Ba ví 700 000, 900 000, 400 000; tài khoản đảm bảo 1 900 000. Bất biến có đạt không, lệch bao nhiêu?"],
                  ["2", "Hạn mức 100 000 000/tháng, đã dùng 92 000 000. Giao dịch 10 000 000 có được không? Còn dùng tối đa bao nhiêu?"],
                  ["3", "Quyết định: đối soát cuối ngày thấy chứng từ R2 đã trích tiền nhưng phía Kho bạc chưa có. Ngân hàng chuyển lại R2 ngay, hay tra soát với phía Kho bạc trước rồi mới xử lý?"]]),
           """Đến lượt bạn, ta có ba câu. Câu một: ba ví có bảy trăm nghìn, chín trăm nghìn và bốn trăm nghìn, tài khoản đảm bảo một triệu chín trăm nghìn, bất biến có đạt không?
           Câu hai: hạn mức một trăm triệu, đã dùng chín mươi hai triệu, giao dịch mười triệu có được không? Câu ba: chứng từ R hai đã trích tiền nhưng Kho bạc chưa có, nên chuyển lại ngay hay tra soát trước?
           Hãy dừng video và làm ra giấy.""",
           focus=[0, "1.2", "1.3", "1.4", 0], pause=25),
        st("""$$700\\,000 + 900\\,000 + 400\\,000 = 2\\,000\\,000 \\;>\\; 1\\,900\\,000 \\;\\Rightarrow\\; \\hl{\\text{không đạt, thiếu } 100\\,000}$$""",
           """Đáp án câu một: tổng ví là hai triệu, lớn hơn một triệu chín trăm nghìn, nên bất biến không đạt, thiếu một trăm nghìn."""),
        st("""$$92 + 10 = 102 > 100 \\;\\Rightarrow\\; \\text{từ chối};\\quad 100 - 92 = \\hlg{8} \\text{ triệu còn dùng được}$$""",
           """Đáp án câu hai: chín mươi hai cộng mười là một trăm lẻ hai triệu, vượt hạn mức nên từ chối, khách còn dùng tối đa tám triệu."""),
        st(table(["lựa chọn", "được", "mất"],
                 [["tra soát với phía Kho bạc trước, rồi chuyển lại hoặc xử lý", "không chuyển trùng nếu bên kia thật ra đã nhận mà chỉ báo trễ", "chậm hơn; trong lúc chờ, tiền chưa vào ngân sách, phải theo dõi tới khi khớp"],
                  ["chuyển lại R2 ngay", "nhanh", "nếu lần đầu thật ra đã tới, tiền bị chuyển hai lần, phải đối soát lại và hoàn trả"]]),
           """Đáp án câu ba: nên tra soát trước, vì nếu Kho bạc thật ra đã nhận mà chỉ báo trễ thì chuyển lại ngay sẽ làm tiền chuyển hai lần. Đổi lại chậm hơn và phải theo dõi tới khi khớp.""",
           ),
    ], checks=["alg.bnx_invariant(1900000, [700000, 900000, 400000]) == (False, 2000000, -100000)",
               "alg.bnx_monthly_limit([92_000_000, 10_000_000], 100_000_000)[1] == (10_000_000, False, 92_000_000)",
               "100_000_000 - alg.bnx_monthly_limit([92_000_000], 100_000_000)[0][2] == 8_000_000"])

    lab_pr = practice_scene(sc, "Tự làm: chạy lại nhật ký ví và hạn mức", [st(
        code(LAB_PY, lines=(1, 5), title="Dữ liệu cho sẵn: chép vào đầu mau.py (số minh hoạ)"),
        """Đây là dữ liệu cho sẵn, gồm tài khoản đảm bảo đầu ngày, số dư ba ví và nhật ký sáu dòng. Mỗi dòng nhật ký là một bộ gồm loại việc, tên ví và số tiền, riêng dòng chuyển có thêm ví nhận.""")] + practice_steps(
        st, "BNX", "L12",
        """<p><b>Đề</b>: viết <code>mau.py</code> với dữ liệu trong <code>de.md</code> (ba ví X, Y, Z; tài khoản đảm bảo đầu ngày 250 000; nhật ký 6 dòng):</p>
<ol><li><b>Chạy lại nhật ký</b>: nạp, rút, chuyển; rút mà ví <b>không đủ</b> thì in <code>tu choi rut …</code> và bỏ qua</li>
<li>In <code>vi …</code> (ba số dư) và <code>tong vi … dam bao … dat …</code></li>
<li><b>Hạn mức 50 000 000</b>: cộng dồn 20, 25, 10, 5 triệu; vượt thì từ chối, vừa bằng thì nhận</li></ol>
<p class="note">Số liệu khác ví dụ trong bài; đầu ra viết không dấu.</p>""",
        """Bây giờ tới phần bạn tự làm: chạy lại nhật ký sáu dòng, trong đó một lệnh rút bị từ chối vì ví không đủ tiền, rồi in số dư và kiểm tài khoản đảm bảo. Sau đó cộng dồn bốn giao dịch với hạn mức năm mươi triệu. Hãy dừng video và tự viết.""",
        EXPECT_LAB, "mau.py",
        """<div class="box key"><b>Nếu kẹt:</b> trước khi rút, so <code>vi[tên] &lt; tiền</code>; nếu đúng thì in từ chối rồi sang dòng nhật ký sau. Hạn mức: từ chối khi <code>da_dung + so_tien &gt; HAN_MUC</code> (dấu lớn hơn, không phải lớn hơn hoặc bằng).
Lời giải ở <code>labs/BNX/L12/loi_giai.py</code> — chỉ mở sau khi bạn đã thử.</div>""",
        """Nếu kẹt, trước khi rút hãy so số dư ví với số tiền rút. Với hạn mức, chỉ từ chối khi tổng cộng thêm lớn hơn hạn mức, nên giao dịch vừa bằng vẫn được nhận. Lời giải nằm trong thư mục thực hành, chỉ mở sau khi đã tự thử.""", pause=120), "BNX", "L12")
    lab_pr["checks"] = ["alg.bnx_l12_lab() == ({'X': 1800000, 'Y': 1050000, 'Z': 500000}, 3350000, 3350000, True)",
                        "[(a, b) for a, b, c in alg.bnx_monthly_limit([20_000_000, 25_000_000, 10_000_000, 5_000_000], 50_000_000)] == [(20000000, True), (25000000, True), (10000000, False), (5000000, True)]",
                        "[c for a, b, c in alg.bnx_monthly_limit([20_000_000, 25_000_000, 10_000_000, 5_000_000], 50_000_000)] == [20000000, 45000000, 45000000, 50000000]"]

    rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        st(chain("nạp, rút: qua tài khoản đảm bảo", "ví → ví: chỉ sổ ví đổi", "mọi lúc: đảm bảo ≥ tổng ví", "hạn mức: cộng dồn tháng", "thuế: khớp số tham chiếu", "quy mô: dùng bảng tra"),
           """Nạp và rút đưa tiền thật qua tài khoản đảm bảo, chuyển ví sang ví chỉ đổi sổ ví, và tài khoản đảm bảo luôn không thấp hơn tổng ví.
           Hạn mức cộng dồn theo tháng, nộp thuế xong khi khớp Kho bạc, và hàng triệu chứng từ thì dùng bảng tra.""",
           focus=[["1.1", "1.3", "1.5"], ["1.7", "1.9", "1.11"]]),
        st("""<div class='box key'><b>Tư duy:</b> con số trên màn hình chỉ là <b>ghi chép</b>. Luôn hỏi: tiền thật nằm ở tài khoản nào, ai giữ, ai đối soát hai bên, và cách làm này còn chạy được khi dữ liệu lớn gấp một trăm lần không?</div>""",
           """Điều cần mang theo: con số trên màn hình chỉ là ghi chép. Vì vậy hãy luôn hỏi tiền thật nằm ở tài khoản nào, ai đối soát hai bên, và cách này còn chạy khi dữ liệu lớn gấp trăm lần không."""),
        st("""<p class='small'>Bài sau: đóng gói dịch vụ thành ảnh chạy được, cho đường ống tự kiểm rồi đưa lên cụm máy chủ.</p>""",
           """Bài sau học đóng gói dịch vụ thành gói chạy ở mọi máy, cho đường ống tự động kiểm tra rồi đưa lên cụm máy chủ.""",
           forward_ref=True),
    ])
    scenes = spoken([hook, pre, sym, intu, form, ex, chk, quymo, pit, quiz, lab_pr, rec])
    return lesson("L12", "vi_dien_tu_thue_dien_tu", "Bài 12 — Ví điện tử và nộp thuế điện tử: tiền thật nằm ở đâu, bút toán và đối soát",
                  "curriculum/bnx.yaml L12; audit/bnx/verify_bnx.py L12; audit/bnx/sources.md [ND52] Nghị định 52/2024/NĐ-CP (15/5/2024, hiệu lực 01/7/2024; audit/legal/registry.yaml: CHUA_KIEM, cần kiểm lại văn bản hiện hành), "
                  "[TT40] Thông tư 40/2024/TT-NHNN (bản hợp nhất 76/VBHN-NHNN; kiểm lại văn bản hiện hành), [TT41] Thông tư 41/2025/TT-NHNN (05/11/2025), "
                  "[TT19] Thông tư 19/2021/TT-BTC (đã sửa đổi bởi 46/2024/TT-BTC, cần kiểm lại văn bản hiện hành từ 01/7/2026), [LQLT14] Luật Quản lý thuế 108/2025/QH15 Điều 14 khoản 5 (ngày nộp thuế; thay Luật 38/2019/QH14 Điều 58 hết hiệu lực 30/6/2026; nguồn toàn văn thứ cấp expertis.vn đọc 2026-11-12, cần kiểm lại); "
                  "số tiền, nhãn R1–R3 là minh hoạ; cấu trúc số tham chiếu không dạy (nguồn không nêu); số đo quy mô: Python 3 chạy thật (prog Scale)",
                  ["Ghi bút toán nạp, rút, chuyển giữa ví và tài khoản ngân hàng", "Kiểm bất biến: tài khoản đảm bảo thanh toán không thấp hơn tổng số dư ví",
                   "Kiểm hạn mức giao dịch ví theo tháng", "Mô tả luồng nộp thuế điện tử qua ngân hàng và đối soát theo số tham chiếu",
                   "Đếm số phép so sánh của hai cách đối soát (quét danh sách, bảng tra) ở 100, 10 000 và 1 000 000 chứng từ",
                   "Viết chương trình Python chạy lại nhật ký ví, kiểm bất biến và hạn mức tháng"],
                  scenes,
                  covers=[(1, "formula"), (2, "formula"), (3, "formula"), (4, "intuition"), (5, "quymo"), (6, "practice")])
