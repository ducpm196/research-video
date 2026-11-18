from lib import *
from labkit import write_lab, practice_steps, practice_scene


def nofill(steps):
    """Bỏ hai câu đệm tự động của lib.split_note (lời bài đã nêu lý do ở cả hai nửa)."""
    for s_ in steps:
        t_ = s_["say"].replace("Nghĩa là mỗi kết luận ở đây đều kiểm được bằng con số trên màn hình. ", "").replace(" Vì vậy ta đọc kết quả thật của máy ngay bên dưới.", "")
        if t_ != s_["say"]:  # tính lại `focus` cho khớp số câu mới
            s_["say"] = t_
            sents_, units_ = lv.sentences(t_), lv.html_units(s_["show"])
            if len(units_) >= 2 and len(sents_) >= 2:
                s_["focus"] = [1 + (j * len(units_)) // len(sents_) for j in range(len(sents_))]
            else:
                s_.pop("focus", None)
    return steps


R_TYPE = repl("LoaiLoi", [
    ("int('abc')", 'Traceback (most recent call last):\n  File "<stdin>", line 1, in <module>\nValueError: invalid literal for int() with base 10: \'abc\''),
    ("10 // 0", 'Traceback (most recent call last):\n  File "<stdin>", line 1, in <module>\nZeroDivisionError: integer division or modulo by zero'),
    ("{'a': 1}['b']", 'Traceback (most recent call last):\n  File "<stdin>", line 1, in <module>\nKeyError: \'b\''),
    ("[1, 2][5]", 'Traceback (most recent call last):\n  File "<stdin>", line 1, in <module>\nIndexError: list index out of range'),
])
R_QUIZ = repl("Quiz", [("int('12')", "12"), ("int(' 7 ')", "7")])

P_TRY = py("doc_tien", '''def doc_tien(chuoi):
    try:
        return int(chuoi.replace(".", ""))
    except ValueError:
        return None

for s in ["1.250.000", "500000", "abc", ""]:
    print(repr(s), doc_tien(s))''', "'1.250.000' 1250000\n'500000' 500000\n'abc' None\n'' None")
P_TB = py("trung_binh_loi", '''def chia(a, b):
    return a // b

def trung_binh(ds):
    return chia(sum(ds), len(ds))

print(trung_binh([10, 20]))
print(trung_binh([]))''', "15", expect="error:ZeroDivisionError",
          err='File "…", line 8, in <module>\nFile "…", line 5, in trung_binh\nFile "…", line 2, in chia\nZeroDivisionError: integer division or modulo by zero')
P_RAISE = py("tu_dinh_nghia", '''class SoDuKhongDu(Exception):
    pass

def rut(so_du, tien):
    if tien > so_du:
        raise SoDuKhongDu(f"thieu {tien - so_du}")
    return so_du - tien

try:
    rut(100000, 250000)
except SoDuKhongDu as loi:
    print("Khong rut duoc:", loi)
print(rut(500000, 200000))''', "Khong rut duoc: thieu 150000\n300000")
P_FIN = py("finally_chay", '''def xu_ly(so):
    print("mo giao dich")
    try:
        return 100 // so
    except ZeroDivisionError:
        return -1
    finally:
        print("dong giao dich")

print(xu_ly(5))
print(xu_ly(0))''', "mo giao dich\ndong giao dich\n20\nmo giao dich\ndong giao dich\n-1")
P_LOG = py("ghi_nhat_ky", '''import logging
import sys

logging.basicConfig(stream=sys.stdout, format="%(levelname)s %(message)s", level=logging.INFO)
logging.info("bat dau xu ly 3 giao dich")
logging.warning("giao dich 2 thieu so tien")
logging.debug("chi tiet: se khong hien")
logging.error("giao dich 3 loi dinh dang")''', "INFO bat dau xu ly 3 giao dich\nWARNING giao dich 2 thieu so tien\nERROR giao dich 3 loi dinh dang")
P_SAI = py("sai_loai", '''try:
    so = int("abc")
except ZeroDivisionError:
    so = 0
print(so)''', "", expect="error:ValueError", err="ValueError: invalid literal for int() with base 10: 'abc'")
P_NUOT = py("nuot_loi", '''tong = 0
for tien in [100, 200, 300]:
    try:
        tong = tong + tien_gui
    except Exception:
        pass
print(tong)''', "0")
P_THUTU = py("thu_tu_except", '''try:
    int("abc")
except Exception:
    print("loi chung")
except ValueError:
    print("loi dinh dang")''', "loi chung")
measure("l07_exc", '''import json, time
res = {}
n = 1000000
for name, rate in (("0", 0), ("1", 1), ("50", 50)):
    data = ["1250" if (i % 100) >= rate else "x" for i in range(n)]
    bt = bc = 1e9
    for _ in range(5):
        t0 = time.perf_counter()
        tong = 0
        for s in data:
            try:
                tong += int(s)
            except ValueError:
                pass
        bt = min(bt, time.perf_counter() - t0)
        t0 = time.perf_counter()
        tong2 = 0
        for s in data:
            if s.isdigit():
                tong2 += int(s)
        bc = min(bc, time.perf_counter() - t0)
        assert tong == tong2
    res["t_try_" + name] = bt
    res["t_check_" + name] = bc
print(json.dumps(res))''')

LAB_SOL = '''class SoTienAm(Exception):
    pass

def doc_so_tien(chuoi):
    so = int(chuoi.replace(".", ""))
    if so < 0:
        raise SoTienAm(chuoi)
    return so

giao_dich = ["2.500.000", "75.000", "n/a", "", "-30.000", "1.000.000"]
tong = 0
da_xu_ly = 0
for chuoi in giao_dich:
    try:
        tong = tong + doc_so_tien(chuoi)
    except ValueError:
        print("Bo qua (dinh dang):", repr(chuoi))
    except SoTienAm:
        print("Bo qua (am):", chuoi)
    finally:
        da_xu_ly = da_xu_ly + 1
print("Tong:", tong)
print("Da xu ly:", da_xu_ly)'''
LAB_OUT = "Bo qua (dinh dang): 'n/a'\nBo qua (dinh dang): ''\nBo qua (am): -30.000\nTong: 3575000\nDa xu ly: 6"
P_LAB = py("lab_l07", LAB_SOL, LAB_OUT)

def build():
    T = {k: M("l07_exc", k) for k in ("t_try_0", "t_try_1", "t_try_50", "t_check_0", "t_check_1", "t_check_50")}
    S = {k: t_show(v) for k, v in T.items()}
    sc_hook = sc("hook", "hook", "Một dòng sai định dạng làm chết cả đợt xử lý triệu giao dịch", [
        st(run_block(P_TB, title="Chia cho không ở sâu ba tầng hàm (<code>sum</code> cộng các số, <code>len</code> đếm phần tử)"),
           """Chào bạn, một chương trình xử lý một triệu giao dịch. Đến giao dịch thứ chín trăm nghìn có một dòng sai định dạng, và cả chương trình chết, tám trăm chín mươi chín nghìn giao dịch trước đó chưa lưu. Ở đây là bản nhỏ của chuyện đó. Hàm trung bình lấy tổng các số chia cho số phần tử, và với danh sách rỗng thì chia cho không, nên chương trình dừng với một thông báo dài.
           Máy gọi mỗi sự cố như vậy là một ngoại lệ, tức một lỗi được báo ra, có tên loại và lý do, để chương trình bắt lấy hoặc để nó dừng. Hôm nay ta học cách đọc thông báo đó, và cách xử lý lỗi một cách có chủ đích.""", introduces=["pyt_ngoai_le"]),
        st("""<div class="box key">Hôm nay ta trả lời ba câu hỏi:
<ol><li>Đọc <b>thông báo lỗi nhiều tầng</b> (traceback) thế nào để thấy lỗi ở đâu?</li>
<li><b>Bắt</b> đúng loại lỗi, <b>ném</b> lỗi của mình, và việc <b>luôn phải làm</b> dù có lỗi hay không?</li>
<li>Khi chưa biết lỗi do đâu, <b>gỡ lỗi</b> và <b>ghi nhật ký</b> ra sao? Và ngoại lệ có đắt không?</li></ol></div>""",
           """Hôm nay ta trả lời ba câu hỏi. Một, đọc thông báo lỗi nhiều tầng thế nào để thấy lỗi ở đâu. Hai, bắt đúng loại lỗi, ném lỗi của mình, và việc luôn phải làm dù có lỗi hay không. Ba, khi chưa biết lỗi do đâu thì gỡ lỗi và ghi nhật ký ra sao, và ngoại lệ có đắt không."""),
    ])
    sc_pre = sc("prereq", "prereq", "Ôn lại: hàm gọi hàm, lớp, và đọc thông báo lỗi từ dòng cuối", [
        st(table(["điều đã biết", "nhắc lại, kèm ví dụ"],
                 [["① hàm gọi hàm", "mỗi lần gọi dựng một hộp biến riêng; hàm trong gọi xong thì hộp bị xoá"],
                  ["② lớp", "<code>class A(B):</code> là kế thừa: <code>A</code> là một loại của <code>B</code>"],
                  ["③ đọc lỗi", "dòng cuối thông báo nói <b>loại lỗi</b> và lý do; các dòng trên là chuỗi các lần gọi dẫn tới đó"]]),
           """Ta ôn lại ba điều. Hàm gọi hàm, mỗi lần gọi dựng một hộp biến riêng. Lớp con kế thừa lớp cha, là một loại của lớp cha. Và khi có lỗi, dòng cuối thông báo nói loại lỗi và lý do, còn các dòng trên là chuỗi các lần gọi dẫn tới đó.
           Hôm nay ta học cách đọc kỹ hơn và cách xử lý.""",
           focus=[1, "1.2", "1.3", "1.4", 1]),
    ])
    sc_sym = sc("sym", "symbol", "Giải mã khối bắt lỗi, ném lỗi, nhật ký và công cụ gỡ lỗi", [
        st(table(["viết", "đọc là", "nghĩa"],
                 [["<code>try:</code> … <code>except Loại as e:</code>", "thử, và bắt lỗi", "chạy khối <code>try</code>; <b>nếu</b> sinh lỗi loại <code>Loại</code> thì nhảy sang khối <code>except</code>; <code>e</code> là đối tượng lỗi"],
                  ["<code>finally:</code>", "luôn làm", "khối này chạy <b>dù có lỗi hay không</b>, kể cả khi <code>return</code> giữa chừng"],
                  ["<code>raise Loại(\"…\")</code>", "ném lỗi", "tự dừng và báo lỗi loại <code>Loại</code>; <code>class MyErr(Exception):</code> là loại lỗi tự định nghĩa"]]),
           """Bảng đầu là ba khối. Khối thử và bắt chạy phần thử, và nếu sinh lỗi đúng loại ghi trong khối bắt thì nhảy sang đó. Khối luôn làm chạy dù có lỗi hay không, kể cả khi hàm trả về giữa chừng. Lệnh ném lỗi tự dừng và báo một lỗi, và ta có thể tự định nghĩa loại lỗi bằng một lớp kế thừa từ lớp lỗi chung."""),
        st(table(["viết", "đọc là", "nghĩa"],
                 [["<code>ValueError</code>, <code>ZeroDivisionError</code>", "lỗi giá trị, chia cho không", "<code>int(\"abc\")</code>; <code>10 // 0</code>"],
                  ["<code>KeyError</code>, <code>IndexError</code>", "lỗi khoá, lỗi chỉ số", "<code>d[\"thieu\"]</code>; <code>ds[5]</code> khi chỉ có $2$ phần tử"],
                  ["<code>logging.info(…)</code>", "ghi nhật ký", "ghi theo <b>mức</b>: <code>debug &lt; info &lt; warning &lt; error &lt; critical</code> (năm mức chuẩn); chỉ mức đã cài trở lên mới hiện"],
                  ["<code>breakpoint()</code>", "điểm dừng gỡ lỗi", "dừng chương trình ngay quanh dòng đó (bản $3.11$ dừng ở dòng <b>kế</b>, bản $3.13$ dừng ngay ở dòng <b>này</b>), mở cửa sổ gỡ lỗi: <code>p biến</code> xem giá trị, <code>n</code> dòng kế, <code>c</code> chạy tiếp, <code>q</code> thoát"]]),
           """Bảng thứ hai là các loại lỗi hay gặp và công cụ tìm lỗi. Lỗi giá trị khi đổi chữ sang số hỏng. Lỗi chia cho không. Lỗi khoá khi hỏi từ điển một khoá thiếu. Lỗi chỉ số khi hỏi quá cuối danh sách. Ghi nhật ký theo năm mức, từ chi tiết đến nghiêm trọng nhất, và chỉ mức đã cài trở lên mới hiện.
           Điểm dừng cho ta dừng chương trình quanh một dòng, rồi xem giá trị biến, chạy dòng kế, hoặc chạy tiếp. Phiên bản ba chấm mười một dừng ở dòng kế, còn ba chấm mười ba dừng ngay ở dòng đó, nên hãy nhìn dòng mà cửa sổ gỡ lỗi chỉ ra.""",
           focus=[1, "1.2", "1.2", "1.3", "1.3", "1.4", "1.5", "1.5"], clear=True),
    ])
    sc_int = sc("intuition", "intuition", "Hình dung: lỗi đi ngược lên chuỗi hàm gọi cho tới khi có ai bắt", [
        st(svg(1500, 430,
               box(40, 50, 330, 90, ["chương trình chính"], C_GRAY, 26, True),
               box(40, 160, 330, 90, ["trung_binh(ds)"], C_BLUE, 26, True),
               box(40, 270, 330, 90, ["chia(a, b)", "a // b → lỗi!"], C_RED, 26, True),
               arrow(205, 140, 205, 160, "#475569"), arrow(205, 250, 205, 270, "#475569"),
               box(560, 270, 400, 90, ["ném: ZeroDivisionError"], C_RED, 26, True),
               arrow(375, 315, 555, 315, "#dc2626"),
               arrow(760, 265, 760, 255, "#dc2626"),
               box(560, 140, 400, 70, ["không có try ở tầng này"], C_AMBER, 24),
               box(560, 40, 400, 70, ["có try … except?", "→ bắt, chạy tiếp"], C_GREEN, 24, True),
               txt(1230, 140, "lỗi trồi lên từng tầng", 26, "middle", "#1f2937", True),
               txt(1230, 180, "cho tới khi gặp một khối", 26, "middle", "#1f2937", True),
               txt(1230, 220, "bắt đúng loại.", 26, "middle", "#1f2937", True),
               txt(1230, 290, "không ai bắt: chương trình dừng,", 24, "middle", "#dc2626"),
               txt(1230, 325, "in chuỗi các tầng đã đi qua", 24, "middle", "#dc2626"),
               txt(1230, 360, "(thông báo nhiều dòng)", 24, "middle", "#dc2626")),
           """Hình này giải thích thông báo lỗi nhiều tầng. Hàm chính gọi hàm trung bình, hàm này gọi hàm chia, và hàm chia gặp phép chia cho không. Hàm chia ném một ngoại lệ. Nếu tầng đó không có khối bắt, lỗi trồi lên tầng trên, rồi tầng trên nữa, cho tới khi gặp một khối bắt đúng loại.
           Nếu không ai bắt, chương trình dừng và in chuỗi các tầng đã đi qua, chính là thông báo nhiều dòng."""),
    ])
    sc_form = sc("formula", "formula", "Suy ra từng bước: bắt đúng loại, ném lỗi của mình, finally, thứ tự các khối bắt", nofill(splitall([
        st(run_block(P_TRY, title="Bước 1. Bắt ĐÚNG loại lỗi mình dự đoán trước")
           + "<p>Vì dữ liệu từ ngoài có thể sai định dạng, <code>int(...)</code> có thể ném <code>ValueError</code>; ta chỉ bắt loại đó và trả <code>None</code> để nơi gọi biết. Lỗi loại khác (lỗi của chính ta) vẫn trồi lên. <code>repr(s)</code> in <code>s</code> <b>kèm cặp nháy</b>, để chuỗi rỗng hiện là <code>''</code> chứ không lẫn với dòng trống.</p>",
           """Bước một, bắt đúng loại lỗi mình dự đoán trước. Vì dữ liệu từ ngoài có thể sai định dạng, việc đổi chữ sang số có thể ném lỗi giá trị. Ta chỉ bắt loại lỗi đó, và trả về giá trị rỗng để nơi gọi biết đây là dữ liệu hỏng. Số một triệu hai trăm năm mươi nghìn đọc đúng, chuỗi chữ cái và chuỗi rỗng cho giá trị rỗng. Lệnh in dạng có nháy cho ta thấy cả chuỗi rỗng là hai dấu nháy liền nhau. Lỗi loại khác vẫn trồi lên, vì ta không bắt chúng."""),
        st(code_block(P_RAISE, lines=(1, 7), title="Bước 2. Định nghĩa loại lỗi riêng và ném khi vi phạm quy tắc")
           + "<p>Vì rút quá số dư là lỗi <b>nghiệp vụ</b> chứ không phải lỗi của ngôn ngữ, ta định nghĩa loại lỗi riêng <code>SoDuKhongDu</code> (kế thừa lớp lỗi chung) rồi ném nó. "
           "Dòng <code>pass</code> nghĩa là “không làm gì”: một khối không được để trống, nên ta đặt nó ở đó. <code>f\"thieu {x}\"</code> điền giá trị của <code>x</code> vào chuỗi.</p>",
           """Bước hai, ném lỗi của mình. Vì rút quá số dư là lỗi nghiệp vụ chứ không phải lỗi của ngôn ngữ, ta định nghĩa loại lỗi riêng. Loại này kế thừa lớp lỗi chung. Dòng chỉ có một từ khoá ngay dưới tên lớp nghĩa là không làm gì, vì một khối không được để trống. Hàm rút ném lỗi đó khi số tiền vượt số dư, kèm chuỗi có chỗ điền cho số tiền thiếu.""", clear=True, introduces=["pyt_pass"]),
        st(run_block(P_RAISE, lines=(9, 13), title="Dùng: bắt đúng loại lỗi của mình")
           + "<p>Rút $250\\,000$ từ $100\\,000$: thiếu $250\\,000 - 100\\,000 = 150\\,000$. Lần rút hợp lệ trả về $500\\,000 - 200\\,000 = 300\\,000$.</p>",
           """Rút hai trăm năm mươi nghìn từ một trăm nghìn thì thiếu một trăm năm mươi nghìn, và lý do đi kèm lỗi. Nơi gọi bắt đúng loại lỗi đó và in thông báo, còn lần rút hợp lệ trả về ba trăm nghìn.""", clear=True),
        st(code_block(P_FIN, lines=(1, 8), title="Bước 3. finally chạy dù có lỗi, dù return")
           + "<p>Vì khối <code>finally</code> chạy <b>mọi trường hợp</b>, kể cả khi hàm đã <code>return</code> ở khối <code>try</code> hay <code>except</code>.</p>",
           """Bước ba, việc luôn phải làm. Hàm mở một giao dịch, thử chia, và dù chia được hay không, khối luôn làm in dòng đóng giao dịch. Vì khối này chạy trong mọi trường hợp, kể cả khi hàm đã trả về giá trị.""", clear=True),
        st(run_block(P_FIN, lines=(10, 11), title="Chạy hai lần: chia được và chia cho không")
           + "<p>Dòng “dong giao dich” hiện ở <b>cả hai</b> lần gọi. Đây là nơi đặt việc giải phóng tài nguyên: đóng tệp, đóng kết nối.</p>",
           """Vì khối luôn làm chạy trong mọi trường hợp, dòng đóng giao dịch hiện ở cả hai lần gọi. Đây là nơi đặt việc giải phóng tài nguyên, như đóng tệp hay đóng kết nối.""", clear=True),
        st(run_block(P_THUTU, title="Bước 4. Máy xét các khối bắt từ trên xuống, khối đúng đầu tiên thắng")
           + "<p>Vì <code>ValueError</code> <b>là một loại</b> của <code>Exception</code>, khối <code>except Exception</code> ở trên đã nhận; khối <code>except ValueError</code> không bao giờ chạy. Quy tắc: <b>loại hẹp đặt trước, loại rộng đặt sau</b>.</p>",
           """Bước bốn, thứ tự các khối bắt. Máy xét các khối từ trên xuống và dùng khối đúng đầu tiên. Vì lỗi giá trị là một loại của lớp lỗi chung, khối bắt lỗi chung ở trên đã nhận, và khối bắt lỗi giá trị bên dưới không bao giờ chạy. Quy tắc là loại hẹp đặt trước, loại rộng đặt sau.""", clear=True),
    ], only=[0])), checks=["250000 - 100000 == 150000", "issubclass(ValueError, Exception)", "100 // 5 == 20"])
    sc_ex = sc("example", "example", "Ví dụ: gom ba kỹ thuật vào một lần xử lý, ghi nhật ký", nofill(splitall([
        st(run_block(P_TB, title="Đọc thông báo: dòng cuối nói LỖI GÌ, các dòng trên nói ĐI ĐƯỜNG NÀO")
           + "<p>Đọc từ dưới lên: <code>chia</code> dòng $2$ là nơi lỗi xảy ra; nó được gọi từ <code>trung_binh</code> dòng $5$; được gọi từ chương trình chính dòng $8$. Dòng $8$ gọi với danh sách <b>rỗng</b>: đó là nguyên nhân gốc. Máy của bạn còn in thêm dòng mã và dấu <code>~^</code> dưới mỗi dòng <code>File …</code> (video rút gọn cho vừa khung); cách đọc không đổi.</p>",
           """Ta đọc thông báo thật. Đọc từ dưới lên. Dòng cuối nói loại lỗi, chia cho không. Dòng ngay trên cho biết hàm chia ở dòng hai là nơi lỗi xảy ra. Nó được gọi từ hàm trung bình ở dòng năm, và hàm này được gọi từ chương trình chính ở dòng tám. Dòng tám gọi với danh sách rỗng, đó là nguyên nhân gốc.
           Nơi lỗi xảy ra và nguyên nhân gốc thường ở hai tầng khác nhau. Máy của bạn còn in thêm dòng mã dưới mỗi dòng ghi tệp, nhưng cách đọc vẫn như vậy.""", clear=True),
        st(repl_block(R_TYPE, 0, 2, title="Lỗi giá trị và lỗi chia cho không")
           + "<p class='note'>Từ phiên bản $3.13$, cửa sổ <code>&gt;&gt;&gt;</code> ghi <code>&lt;python-input-N&gt;</code> thay cho <code>&lt;stdin&gt;</code> và in thêm dòng mã kèm dấu <code>~^</code>; dòng cuối (loại lỗi và lý do) giống hệt.</p>",
           """Ví dụ một, bốn loại lỗi hay gặp. Đổi một chuỗi chữ cái sang số cho lỗi giá trị. Chia mười cho không cho lỗi chia cho không. Từ phiên bản ba chấm mười ba, cửa sổ gõ lệnh in thêm dòng mã bên dưới, nhưng dòng cuối vẫn giống hệt."""),
        st(repl_block(R_TYPE, 2, 4, title="Lỗi khoá và lỗi chỉ số"),
           """Hỏi một khoá thiếu cho lỗi khoá. Hỏi chỉ số năm của danh sách hai phần tử cho lỗi chỉ số. Mỗi loại có một dòng cuối khác nhau, và dòng đó cho ta biết nên bắt loại nào.""", clear=True),
        st(code_block(P_LOG, title="Ghi nhật ký theo mức thay cho in rải rác")
           + "<p>Dòng cài đặt có ba phần: <code>stream=sys.stdout</code> ghi ra màn hình (<code>import sys</code> lấy tên <code>sys</code>), <code>format=…</code> là khuôn mỗi dòng: <code>%(levelname)s</code> điền tên mức, <code>%(message)s</code> điền nội dung, <code>level=logging.INFO</code> là mức thấp nhất còn hiện.</p>",
           """Ví dụ hai, ghi nhật ký. Dòng cài đặt chọn ghi ra màn hình, đặt khuôn mỗi dòng gồm hai chỗ trống, một chỗ điền tên mức và một chỗ điền nội dung, và cài mức thông tin trở lên.""", clear=True),
        st(out_block(P_LOG, title="Kết quả chạy"),
           """Ba dòng ở các mức thông tin, cảnh báo và lỗi hiện ra. Dòng ở mức chi tiết không hiện vì thấp hơn mức đã cài. Nhờ vậy khi cần xem chi tiết, ta chỉ đổi mức, không phải sửa từng dòng in.""", clear=True),
        st(table(["công cụ", "khi nào dùng", "cách dùng"],
                 [["traceback", "chương trình đã chết", "đọc từ dòng cuối lên; tìm nguyên nhân GỐC, không chỉ nơi lỗi xảy ra"],
                  ["nhật ký", "chạy lâu, hoặc ở máy khác", "ghi theo mức; đọc lại sau khi xảy ra"],
                  ["điểm dừng", "chưa hiểu vì sao giá trị sai", "dừng tại dòng nghi ngờ, xem giá trị biến, chạy từng dòng"]]),
           """Ba công cụ, ba tình huống. Khi chương trình đã chết, đọc thông báo từ dòng cuối lên và tìm nguyên nhân gốc. Khi chương trình chạy lâu hoặc chạy ở máy khác, ghi nhật ký theo mức rồi đọc lại. Khi chưa hiểu vì sao một giá trị sai, đặt điểm dừng tại dòng nghi ngờ, xem biến và chạy từng dòng.""", clear=True),
    ], only=[0])), checks=["issubclass(ZeroDivisionError, ArithmeticError)"])
    sc_chk = sc("check", "check", "Tự kiểm bằng đường khác: kiểm tra trước thay cho bắt lỗi, hai đường cùng kết quả", [
        st(repl_block(repl("KiemTra", [('"1250".isdigit()', "True"), ('"abc".isdigit()', "False"), ('"".isdigit()', "False"), ('"1.250.000".isdigit()', "False")]), title="Kiểm tra trước: chuỗi toàn chữ số?")
           + "<p>Cách khác với <code>try</code>: hỏi trước. Với chuỗi <b>chỉ gồm chữ số $0$–$9$ hoặc chữ cái</b>, hai cách phân loại <b>giống nhau</b>: <code>\"1250\"</code> hợp lệ, <code>\"abc\"</code> và <code>\"\"</code> không. Tổng hai cách cho cùng kết quả ở phép đo bên dưới. Nhưng chuỗi có dấu chấm như <code>\"1.250.000\"</code> thì <code>isdigit()</code> nói <code>False</code>, dù hàm ở bước $1$ đọc được: hai cách chỉ khớp khi dữ liệu thuộc hai loại trên.</p>",
           """Đường kiểm khác, kiểm tra trước thay cho bắt lỗi. Hỏi chuỗi có toàn chữ số không. Chuỗi một nghìn hai trăm năm mươi hợp lệ, một chuỗi chữ cái và chuỗi rỗng thì không. Với dữ liệu chỉ gồm chữ số hoặc chữ cái, hai cách phân loại giống nhau, và phép đo ở phần sau đã kiểm điều này, tổng hai cách bằng nhau. Nhưng chuỗi có dấu chấm ngăn cách, như một triệu hai trăm năm mươi nghìn viết kiểu cũ, thì cách hỏi trước nói không hợp lệ, dù hàm ở bước một đọc được."""),
    ], checks=["'1250'.isdigit() and not 'abc'.isdigit() and not ''.isdigit()"])
    sc_scale = sc("scale", "concept", "Khi dữ liệu lớn dần: ngoại lệ rẻ khi hiếm, đắt khi thường xuyên", [
        st(table(["một triệu chuỗi, tỉ lệ chuỗi hỏng", "bắt lỗi (try)", "kiểm tra trước (isdigit)"],
                 [["0%", S["t_try_0"][0], S["t_check_0"][0]], ["50%", S["t_try_50"][0], S["t_check_50"][0]]])
           + "<p class='note'>Đo trên máy kiểm, số minh hoạ; dữ liệu chỉ gồm chuỗi toàn số hoặc “abc”, nên hai cách cho cùng tổng. Ở tỉ lệ hỏng rất thấp (cỡ $1\\%$) hai cách xấp xỉ nhau, thứ tự đổi theo máy và phiên bản. Ở một nửa hỏng, bắt lỗi chậm hơn kiểm tra trước cỡ vài lần (tỉ số đổi theo máy); mỗi ô lấy lần nhanh nhất trong năm lần.</p>",
           f"""Bảng này đo một triệu chuỗi ở hai tỉ lệ hỏng. Khi không có chuỗi hỏng, bắt lỗi mất {S['t_try_0'][1]}, kiểm tra trước mất {S['t_check_0'][1]}. Khi một nửa hỏng, bắt lỗi tăng lên {S['t_try_50'][1]}, còn kiểm tra trước chỉ {S['t_check_50'][1]}. Ở tỉ lệ hỏng rất thấp, cỡ một phần trăm, hai cách xấp xỉ nhau. Ở một nửa hỏng, bắt lỗi chậm hơn kiểm tra trước cỡ vài lần, tỉ số đổi theo máy."""),
        st("<div class='box key'><b>Đánh đổi:</b> khối <code>try</code> gần như <b>miễn phí khi không có lỗi</b>; mỗi lần lỗi <b>thật sự xảy ra</b> tốn một khoản đáng kể. "
           "Lỗi hiếm (dữ liệu sạch): dùng <code>try</code>, mã gọn hơn. Lỗi thường xuyên (dữ liệu bẩn, ví dụ một nửa): hỏi trước rẻ hơn. "
           "Quan trọng hơn tốc độ: <b>đừng dùng lỗi thay cho việc rẽ nhánh thông thường</b> khi có cách rõ ràng hơn.</div>",
           """Đánh đổi là khối thử gần như miễn phí khi không có lỗi, nhưng mỗi lần lỗi thật sự xảy ra thì tốn một khoản đáng kể. Lỗi hiếm thì dùng khối thử, mã gọn hơn. Lỗi thường xuyên thì hỏi trước rẻ hơn. Và quan trọng hơn tốc độ, đừng dùng lỗi thay cho việc rẽ nhánh thông thường khi có cách rõ ràng hơn.""", clear=True),
    ], checks=["1000000 // 100 == 10000"])
    sc_pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st('<div class="box warn"><b>Lỗi 1 (người mới).</b> Bắt sai loại: khối <code>except</code> không đúng loại thì lỗi vẫn thoát ra.</div>' + run_block(P_SAI)
           + "<p>Đọc dòng cuối: lỗi là <code>ValueError</code>, mà ta chỉ bắt <code>ZeroDivisionError</code>. Phép thử: <b>cố ý gây lỗi</b> rồi xem khối của mình có chạy không.</p>",
           """Lỗi thứ nhất, của người mới, là bắt sai loại. Ta chỉ bắt lỗi chia cho không, nhưng lỗi thật là lỗi giá trị, nên nó vẫn thoát ra và chương trình chết. Phép thử là cố ý gây lỗi rồi xem khối của mình có chạy không."""),
        st('<div class="box warn"><b>Lỗi 2 (người đã đi làm).</b> Bắt quá rộng rồi bỏ qua: nuốt cả lỗi do chính mình gõ sai.</div>' + run_block(P_NUOT)
           + "<p>Biến <code>tien_gui</code> gõ nhầm (đúng là <code>tien</code>) gây <code>NameError</code>, nhưng <code>except Exception: pass</code> nuốt mất: tổng $0$, <b>không báo gì</b>. Chỉ bắt loại cụ thể, và <b>ghi nhật ký</b> khi bỏ qua.</p>",
           """Lỗi thứ hai, của người đã đi làm, là bắt quá rộng rồi bỏ qua. Biến gõ nhầm tên gây lỗi tên chưa định nghĩa, nhưng khối bắt lỗi chung nuốt mất, nên tổng bằng không mà không có báo cáo nào. Con số sai lọt thẳng vào kết quả. Hãy chỉ bắt loại cụ thể, và ghi nhật ký mỗi khi bỏ qua một lỗi.""", clear=True),
        st('<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> Đặt khối bắt rộng trước khối bắt hẹp.</div>' + run_block(P_THUTU)
           + "<p>Khối thứ hai <b>không bao giờ chạy</b>; máy không cảnh báo. Phép thử: với mỗi khối <code>except</code>, tự hỏi “có lỗi nào tới được đây không?”.</p>",
           """Lỗi thứ ba, của người đã đi làm, là đặt khối bắt rộng trước khối bắt hẹp. Khối thứ hai không bao giờ chạy, và máy không cảnh báo. Phép thử là với mỗi khối bắt, tự hỏi có lỗi nào tới được đây không.""", clear=True),
    ], checks=["isinstance(ValueError('x'), Exception)"])
    sc_quiz = sc("quiz", "quiz", "Bây giờ tới phần bạn tự làm", [
        st("""<p><b>Đề.</b> Hàm <code>def rut(so_du, tien)</code> ném <code>SoDuKhongDu</code> khi <code>tien &gt; so_du</code>.</p>
<ol><li>Gọi <code>rut(100, 250)</code> ngoài khối <code>try</code>: chương trình làm gì?</li>
<li>Trong <code>try … finally</code>, dòng <code>print("xong")</code> ở <code>finally</code> hiện khi nào?</li></ol>
<p><b>Quyết định:</b> đọc $50$ nghìn dòng dữ liệu, $1$ dòng hỏng: <b>bỏ qua dòng hỏng rồi chạy tiếp</b> hay <b>dừng cả chương trình</b>? Vì sao?</p>""",
           """Bây giờ tới phần bạn tự làm. Hàm rút ném lỗi số dư không đủ khi số tiền lớn hơn số dư. Câu một, gọi rút một trăm với hai trăm năm mươi ngoài khối thử, chương trình làm gì. Câu hai, dòng in trong khối luôn làm hiện khi nào.
           Sau đó là một quyết định, đọc năm mươi nghìn dòng dữ liệu, một dòng hỏng, bỏ qua dòng hỏng rồi chạy tiếp hay dừng cả chương trình, và vì sao. Hãy dừng video và làm.""", pause=60),
        st(table(["câu", "đáp án"], [["1", "lỗi trồi lên khỏi mọi hàm, <b>chương trình dừng</b> và in thông báo nhiều dòng; dòng cuối là <code>SoDuKhongDu: …</code>"],
                                     ["2", "<b>mọi trường hợp</b>: không lỗi, có lỗi đã bắt, có lỗi không bắt, hay <code>return</code> giữa chừng"]]),
           """Đáp án như sau. Câu một, lỗi trồi lên khỏi mọi hàm, chương trình dừng và in thông báo nhiều dòng với loại lỗi ở dòng cuối. Câu hai, dòng trong khối luôn làm hiện trong mọi trường hợp, không lỗi, có lỗi đã bắt, có lỗi không bắt, hoặc hàm trả về giữa chừng."""),
        st("<div class='box key'><b>Quyết định:</b> <b>tuỳ hậu quả</b>. Nếu dữ liệu hỏng chỉ ảnh hưởng một dòng độc lập (như nhật ký): bỏ qua, nhưng <b>ghi lại</b> dòng nào, và đếm số dòng bỏ. "
           "Nếu sai một dòng làm sai kết quả cả mẻ (như đối soát tiền): <b>dừng</b>, vì một con số sai lặng lẽ tệ hơn một chương trình dừng. Luôn báo số dòng bỏ qua để người dùng quyết định.</div>",
           """Quyết định, tuỳ hậu quả. Nếu dòng hỏng chỉ ảnh hưởng một dòng độc lập, như nhật ký, thì bỏ qua nhưng phải ghi lại dòng nào và đếm số dòng bỏ. Nếu sai một dòng làm sai kết quả cả mẻ, như đối soát tiền, thì dừng, vì một con số sai lặng lẽ tệ hơn một chương trình dừng. Luôn báo số dòng bỏ qua.""", clear=True),
    ], checks=["50000 // 1 == 50000"])
    sc_prac = practice_scene(sc, "Tự làm: sửa chương trình hỏng, bắt đúng loại ngoại lệ", pr_steps(
        st, "PYT", "L07",
        """<p><b>Đề</b>: chương trình trong <code>de.md</code> chết ngay ở giao dịch <code>"n/a"</code>. Viết <code>sua_loi.py</code>:</p>
<ol><li>định nghĩa <code>SoTienAm(Exception)</code>; <code>doc_so_tien</code> bỏ dấu chấm, đổi sang số, <b>ném</b> <code>SoTienAm</code> nếu số âm;</li>
<li>vòng lặp: bắt <code>ValueError</code> in <code>Bo qua (dinh dang): …</code> (dùng <code>repr</code>), bắt <code>SoTienAm</code> in <code>Bo qua (am): …</code>;</li>
<li>dùng <code>finally</code> đếm số giao dịch đã xử lý; cuối in <code>Tong: …</code> và <code>Da xu ly: …</code>.</li></ol>""",
        """Bây giờ tới phần bạn tự làm. Chương trình trong tệp đề bài chết ở giao dịch có chữ không phải số, hãy sửa nó như sau. Định nghĩa một loại lỗi số tiền âm và ném nó khi số âm. Trong vòng lặp, bắt lỗi giá trị và lỗi số tiền âm, mỗi loại in một thông báo riêng. Dùng khối luôn làm để đếm số giao dịch đã xử lý. Cuối cùng in tổng và số đã xử lý.
        Hãy dừng video và làm.""",
        LAB_OUT, "sua_loi.py",
        """<div class="box key"><b>Nếu kẹt:</b> <code>try: tong = tong + doc_so_tien(chuoi)</code>, rồi hai khối <code>except ValueError:</code> và <code>except SoTienAm:</code>, rồi <code>finally: da_xu_ly = da_xu_ly + 1</code>. <code>int("")</code> cũng ném <code>ValueError</code>. <code>repr("n/a")</code> cho <code>'n/a'</code>.
Lời giải ở <code>labs/PYT/L07/loi_giai.py</code>.</div>""",
        """Nếu kẹt, đặt phép cộng trong khối thử, rồi hai khối bắt cho hai loại lỗi, rồi khối luôn làm tăng biến đếm. Chuỗi rỗng đổi sang số cũng ném lỗi giá trị. Hàm lấy dạng chữ có nháy giúp thấy rõ chuỗi rỗng.
        Lời giải nằm trong thư mục thực hành, chỉ mở sau khi đã thử.""", pause=300), "PYT", "L07")
    write_lab("PYT", "L07", """# Lab PYT L07 — Sửa chương trình hỏng, bắt đúng loại ngoại lệ

Cần: Python 3.11 trở lên. Chương trình hỏng (chết ngay ở `"n/a"` với `ValueError`):

```python
def doc_so_tien(chuoi):
    return int(chuoi.replace(".", ""))

giao_dich = ["2.500.000", "75.000", "n/a", "", "-30.000", "1.000.000"]
tong = 0
for chuoi in giao_dich:
    tong = tong + doc_so_tien(chuoi)
print("Tong:", tong)
```

Viết `sua_loi.py` (số minh hoạ; khác ví dụ trong bài):

1. Định nghĩa `class SoTienAm(Exception)`. `doc_so_tien` bỏ dấu chấm, đổi sang số nguyên và **ném** `SoTienAm(chuoi)` nếu số âm.
2. Trong vòng lặp: `except ValueError` in `Bo qua (dinh dang): <repr(chuoi)>`; `except SoTienAm` in `Bo qua (am): <chuoi>`.
3. Dùng `finally` tăng biến đếm `da_xu_ly` mỗi giao dịch. Sau vòng lặp in `Tong: …` rồi `Da xu ly: …`.

Chạy: `python sua_loi.py`. Chấm (chạy từ thư mục gốc của bộ khoá, nơi có thư mục `labs`; để tệp của bạn ở đó hoặc ghi đường dẫn tới tệp): `bash labs/cham.sh PYT L07 sua_loi.py`.
""", "py", LAB_SOL, LAB_OUT)
    sc_rec = sc("recap", "recap", "Chuỗi logic và tư duy cần mang theo", [
        st(chain("traceback: đọc từ dưới lên; nơi lỗi xảy ra ≠ nguyên nhân gốc", "bắt đúng loại, loại hẹp đặt trước", "raise: ném lỗi nghiệp vụ bằng loại riêng",
                 "finally: việc phải làm trong mọi trường hợp", "ngoại lệ rẻ khi hiếm, đắt khi thường xuyên", "gỡ lỗi: nhật ký theo mức, điểm dừng"),
           """Tổng kết chuỗi logic. Đọc thông báo lỗi từ dưới lên, và nhớ nơi lỗi xảy ra khác nguyên nhân gốc. Bắt đúng loại, loại hẹp đặt trước. Ném lỗi nghiệp vụ bằng loại riêng. Khối luôn làm chứa việc phải làm trong mọi trường hợp.
           Ngoại lệ rẻ khi hiếm, đắt khi thường xuyên. Và khi gỡ lỗi, dùng nhật ký theo mức và điểm dừng."""),
        st("""<div class='box key'><b>Tư duy:</b> lỗi là <b>thông tin</b>, đừng giấu nó. Bắt lỗi nào mình biết cách xử lý; để các lỗi còn lại trồi lên và báo to. Một chương trình dừng với thông báo rõ tốt hơn một chương trình chạy tiếp với con số sai.</div>
<p>Bài sau: mô-đun, gói và môi trường ảo, để chia chương trình thành nhiều tệp và cài thư viện của người khác một cách có kiểm soát.</p>""",
           """Điều cần mang theo, lỗi là thông tin, đừng giấu nó. Bắt lỗi nào mình biết cách xử lý, để các lỗi còn lại trồi lên và báo to. Một chương trình dừng với thông báo rõ tốt hơn một chương trình chạy tiếp với con số sai.
           Bài sau, ta học mô-đun, gói và môi trường ảo, để chia chương trình thành nhiều tệp và cài thư viện của người khác một cách có kiểm soát.""", forward_ref=True),
    ])
    return lesson("L07", "ngoai_le_va_go_loi", "Bài 7 — Ngoại lệ và gỡ lỗi: khi chương trình hỏng",
                  "curriculum/pyt.yaml L07; audit/pyt/verify_pyt.py L07 (chạy thật trên Python 3.11 và 3.13; chi phí ngoại lệ đo bằng verify_pyt, máy kiểm, số minh hoạ); "
                  "Python Tutorial §8 (Errors and Exceptions), Library Reference: Built-in Exceptions, logging, pdb; Python FAQ (EAFP/LBYL: 'How fast are exceptions?')",
                  ["Đọc thông báo lỗi nhiều tầng từ dưới lên và chỉ ra nơi lỗi xảy ra cùng nguyên nhân gốc",
                   "Bắt đúng loại ngoại lệ bằng try và except, đặt loại hẹp trước loại rộng",
                   "Ném ngoại lệ bằng raise và viết loại ngoại lệ tự định nghĩa",
                   "Dùng finally cho việc phải làm trong mọi trường hợp",
                   "Ghi nhật ký theo mức và nêu cách dùng điểm dừng để gỡ lỗi",
                   "Nêu chi phí của ngoại lệ khi lỗi hiếm và khi lỗi thường xuyên",
                   "Chỉ ra ba lỗi hay gặp: bắt sai loại, bắt quá rộng rồi bỏ qua, đặt loại rộng trước loại hẹp",
                   "Sửa chương trình hỏng bằng cách bắt đúng loại ngoại lệ và ném ngoại lệ của mình"],
                  [sc_hook, sc_pre, sc_sym, sc_int, sc_form, sc_ex, sc_chk, sc_scale, sc_pit, sc_quiz, sc_prac, sc_rec],
                  assumes=["pyt_repr"],
                  covers=[(1, "example"), (2, "formula"), (3, "formula"), (4, "formula"), (5, "example"), (6, "scale"), (7, "pitfalls"), (8, "practice")])
