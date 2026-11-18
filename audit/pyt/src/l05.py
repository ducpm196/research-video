from lib import *
from labkit import write_lab, practice_steps, practice_scene

CSV_DATA = "ma,loai,so_tien\nA01,chuyen,500000\nA02,nap,2000000\nA03,rut,300000\n"
R_JSON = repl("Json", [
    ("import json", ""), ('json.dumps({"a": True, "b": None, "c": [1, 2.5]})', '\'{"a": true, "b": null, "c": [1, 2.5]}\''),
    ("json.loads('{\"so\": 5, \"ten\": \"A01\"}')", "{'so': 5, 'ten': 'A01'}"),
    ('json.dumps("tiền")', r"""'"ti\\u1ec1n"'"""), ('json.dumps("tiền", ensure_ascii=False)', """'"tiền"'"""),
])
R_MOJI = repl("Moji", [('"tiền".encode("utf-8")', r"b'ti\xe1\xbb\x81n'"), ('"tiền".encode("utf-8").decode("latin-1")', r"'tiá»\x81n'"),
                       ('"tiền".encode("utf-8").decode("utf-8")', "'tiền'")])
R_KIEM = repl("Kiem", [('"A01,chuyen,500000".split(",")', "['A01', 'chuyen', '500000']"), ("500000 + 2000000 + 300000", "2800000")])
R_QUIZ = repl("Quiz", [('"A02,nap,2000000\\n".rstrip("\\n").split(",")[2]', "'2000000'"), ('int("2000000") + 1', "2000001")])

P_GHI = py("ghi_doc", '''with open("ghi_chu.txt", "w", encoding="utf-8") as f:
    f.write("tiền mặt\\n")
    f.write("2.000.000 đồng\\n")
with open("ghi_chu.txt", encoding="utf-8") as f:
    noi_dung = f.read()
print(len(noi_dung.split("\\n")) - 1, "dong")
print(len(noi_dung), "ky tu")
print(len(noi_dung.encode("utf-8")), "byte")''', "2 dong\n24 ky tu\n31 byte")
P_CSV = py("doc_csv", '''import csv
tong = 0
with open("gd.csv", encoding="utf-8", newline="") as f:
    for hang in csv.DictReader(f):
        print(hang["ma"], hang["loai"], type(hang["so_tien"]).__name__)
        tong = tong + int(hang["so_tien"])
print("Tong:", tong)''', "A01 chuyen str\nA02 nap str\nA03 rut str\nTong: 2800000", files={"gd.csv": CSV_DATA})
P_CSVW = py("ghi_csv", '''import csv
hang = [["A04", "chuyen", 150000], ["A05", "nap", 900000]]
with open("moi.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f)
    w.writerow(["ma", "loai", "so_tien"])
    w.writerows(hang)
print(open("moi.csv", encoding="utf-8").read())''', "ma,loai,so_tien\nA04,chuyen,150000\nA05,nap,900000\n")
P_JSON = py("ghi_json", '''import json
bao_cao = {"ngay": "2026-03-05", "so_gd": 2, "tong": 2500000, "loai": ["chuyen", "nap"]}
with open("bc.json", "w", encoding="utf-8") as f:
    json.dump(bao_cao, f, ensure_ascii=False)
with open("bc.json", encoding="utf-8") as f:
    doc = json.load(f)
print(doc["tong"], doc["loai"][1])
print(doc == bao_cao)
print(open("bc.json", encoding="utf-8").read())''', '2500000 nap\nTrue\n{"ngay": "2026-03-05", "so_gd": 2, "tong": 2500000, "loai": ["chuyen", "nap"]}')
P_PATH = py("duong_dan", '''from pathlib import Path
thu_muc = Path("bao_cao") / "2026"
thu_muc.mkdir(parents=True, exist_ok=True)
tep = thu_muc / "thang3.txt"
tep.write_text("xin chao", encoding="utf-8")
print(tep.name, tep.suffix, tep.exists())
print(tep.read_text(encoding="utf-8"))
print([p.name for p in thu_muc.iterdir()])''', "thang3.txt .txt True\nxin chao\n['thang3.txt']")
P_DONG = py("tung_dong", '''tong = 0
dem = 0
with open("gd.csv", encoding="utf-8") as f:
    next(f)
    for dong in f:
        tong = tong + int(dong.split(",")[2])
        dem = dem + 1
print(dem, tong)''', "3 2800000", files={"gd.csv": CSV_DATA})
P_XOA = py("che_do_w", '''from pathlib import Path
Path("a.txt").write_text("abcdef", encoding="utf-8")
print(Path("a.txt").stat().st_size)
with open("a.txt", "w", encoding="utf-8") as f:
    f.write("xy")
print(Path("a.txt").stat().st_size)
with open("a.txt", "a", encoding="utf-8") as f:
    f.write("z")
print(Path("a.txt").read_text(encoding="utf-8"))''', "6\n2\nxyz")
P_BUF = py("chua_dong", '''f = open("kq.txt", "w", encoding="utf-8")
f.write("tong=2500000")
print(repr(open("kq.txt", encoding="utf-8").read()))
f.close()
print(repr(open("kq.txt", encoding="utf-8").read()))''', "''\n'tong=2500000'")
SH_ENC = sh("MaHoa", [
    ("PYTHONIOENCODING=cp1252 python -c \"print('tiền')\" 2> loi.txt; echo $?", "1"),
    ("tail -n 1 loi.txt | cut -d: -f1", "UnicodeEncodeError"),
    ("PYTHONIOENCODING=utf-8 python -c \"print('tiền')\"", "tiền"),
])
measure("l05_doc", '''import json, os, time, tempfile, tracemalloc
res = {}
d = tempfile.mkdtemp()
for k, n in (("1e4", 10000), ("1e6", 1000000)):
    p = os.path.join(d, "g" + k + ".csv")
    with open(p, "w", encoding="utf-8", newline="\\n") as f:
        f.write("ma,loai,so_tien\\n")
        for i in range(n):
            f.write("A%07d,chuyen,%d\\n" % (i, 100000 + i % 900000))
    res["size_" + k] = os.path.getsize(p)
    t0 = time.perf_counter()
    with open(p, encoding="utf-8") as f:
        txt = f.read()
    tong = 0
    for dong in txt.split("\\n")[1:-1]:
        tong += int(dong.split(",")[2])
    res["t_all_" + k] = time.perf_counter() - t0
    del txt
    t0 = time.perf_counter()
    tong2 = 0
    with open(p, encoding="utf-8") as f:
        next(f)
        for dong in f:
            tong2 += int(dong.split(",")[2])
    res["t_line_" + k] = time.perf_counter() - t0
    assert tong == tong2
    tracemalloc.start()
    with open(p, encoding="utf-8") as f:
        txt = f.read()
    dong = txt.split("\\n")[1:-1]
    res["m_all_" + k] = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()
    del txt, dong
    tracemalloc.start()
    with open(p, encoding="utf-8") as f:
        next(f)
        for j, dong in enumerate(f):
            int(dong.split(",")[2])
            if j >= 20000:
                break
    res["m_line_" + k] = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()
print(json.dumps(res))''')

LAB_CSV = "ma,loai,tai_khoan,so_tien\n1,rut,A02,500000\n2,chuyen,A01,1200000\n3,nap,A03,3000000\n4,chuyen,A02,250000\n5,rut,A01,700000\n6,chuyen,A03,90000\n"
LAB_SOL = '''import csv
import json
from pathlib import Path

Path("gd.csv").write_text("ma,loai,tai_khoan,so_tien\\n1,rut,A02,500000\\n2,chuyen,A01,1200000\\n3,nap,A03,3000000\\n4,chuyen,A02,250000\\n5,rut,A01,700000\\n6,chuyen,A03,90000\\n", encoding="utf-8")
tong = {}
dem = 0
with open("gd.csv", encoding="utf-8", newline="") as f:
    for hang in csv.DictReader(f):
        dem = dem + 1
        tong[hang["loai"]] = tong.get(hang["loai"], 0) + int(hang["so_tien"])
bao_cao = {"so_giao_dich": dem, "tong_theo_loai": tong}
with open("bao_cao.json", "w", encoding="utf-8") as f:
    json.dump(bao_cao, f, ensure_ascii=False, sort_keys=True)
doc = json.loads(Path("bao_cao.json").read_text(encoding="utf-8"))
print(Path("bao_cao.json").read_text(encoding="utf-8"))
print(doc["so_giao_dich"], doc["tong_theo_loai"]["nap"])'''
LAB_OUT = '{"so_giao_dich": 6, "tong_theo_loai": {"chuyen": 1540000, "nap": 3000000, "rut": 1200000}}\n6 3000000'
P_LAB = py("lab_l05", LAB_SOL, LAB_OUT)


def build():
    z4, z6 = M("l05_doc", "size_1e4"), M("l05_doc", "size_1e6")
    ma4, ma6 = M("l05_doc", "m_all_1e4"), M("l05_doc", "m_all_1e6")
    ml4, ml6 = M("l05_doc", "m_line_1e4"), M("l05_doc", "m_line_1e6")
    ta6, tl6 = M("l05_doc", "t_all_1e6"), M("l05_doc", "t_line_1e6")
    bz4, bz6, bz8 = b_show(z4), b_show(z6), b_show(z6 * 100)
    bma4, bma6, bma8 = b_show(ma4), b_show(ma6), b_show(ma6 * 100)
    bml4, bml6 = b_show(ml4), b_show(ml6)
    sta6, stl6 = t_show(ta6), t_show(tl6)
    sc_hook = sc("hook", "hook", "Tệp giao dịch 23 MB mở được, tệp 2,3 GB thì có thể hết bộ nhớ", [
        st(table(["số dòng giao dịch", "dung lượng tệp (đo)", f"bộ nhớ khi đọc cả tệp một lần rồi tách thành dòng (đỉnh)", "bộ nhớ khi đọc từng dòng (đỉnh)"],
                 [["10 000", bz4[0], bma4[0], bml4[0]], ["1 000 000", bz6[0], bma6[0], bml6[0]],
                  ["100 000 000 (ngoại suy)", bz8[0], bma8[0] + " (tuyến tính)", bml6[0] + " (không đổi)"]])
           + "<p class='note'><b>Ngoại suy</b> = nhân theo tỉ lệ từ số đã đo để đoán quy mô lớn hơn (ước lượng, chưa đo). MB = triệu byte, GB = tỉ byte.</p>",
           f"""Chào bạn, một tệp giao dịch một triệu dòng nặng {bz6[1]}. Nếu đọc cả tệp vào bộ nhớ một lần rồi tách thành dòng, đỉnh bộ nhớ của chương trình, tức mức cao nhất trong lúc chạy, lên tới {bma6[1]}. Nếu đọc từng dòng, bộ nhớ chỉ cỡ {bml6[1]}, dù tệp có lớn đến đâu.
           Ngoại suy, tức nhân theo tỉ lệ từ số đã đo, cho một trăm triệu dòng: đọc cả tệp cần {bma8[1]}, nhiều hơn bộ nhớ của nhiều máy cá nhân. Số đo trên máy kiểm, số minh hoạ."""),
        st("""<div class="box key">Hôm nay ta trả lời ba câu hỏi:
<ol><li>Mở, đọc, ghi, <b>đóng</b> một tệp văn bản đúng cách và đúng <b>bảng mã</b>?</li>
<li>Đọc và ghi hai định dạng bảng và cấu trúc: <b>CSV</b> và <b>JSON</b>?</li>
<li>Khi tệp lớn hơn bộ nhớ thì đọc <b>từng dòng</b> giúp thế nào?</li></ol></div>""",
           """Hôm nay ta trả lời ba câu hỏi. Một, mở, đọc, ghi và đóng một tệp văn bản đúng cách và đúng bảng mã. Hai, đọc và ghi hai định dạng, một cho bảng và một cho dữ liệu có cấu trúc. Ba, khi tệp lớn hơn bộ nhớ thì đọc từng dòng giúp thế nào."""),
    ])
    sc_pre = sc("prereq", "prereq", "Ôn lại: tệp văn bản, bảng mã và hai định dạng bảng, cấu trúc", [
        st(table(["điều đã biết", "nhắc lại, kèm ví dụ"],
                 [["① tệp văn bản", "dãy byte trên đĩa; mỗi dòng kết thúc bằng một ký tự xuống dòng"],
                  ["② bảng mã", "UTF-8: chữ Việt có dấu chiếm 2–3 byte; <code>\"tiền\"</code> là $4$ ký tự, $6$ byte"],
                  ["③ CSV, JSON", "CSV: bảng, cột cách nhau dấu phẩy; JSON: lồng nhau, có kiểu số, chuỗi, danh sách"],
                  ["④ chuỗi và từ điển", "<code>s.split(\",\")</code> tách một dòng; từ điển là bảng tra khoá → giá trị"]]),
           """Ta ôn lại bốn điều. Tệp văn bản là dãy byte trên đĩa, mỗi dòng kết thúc bằng ký tự xuống dòng. Chữ Việt có dấu chiếm hai hoặc ba byte, nên chữ tiền là bốn ký tự nhưng sáu byte. Hai định dạng dữ liệu là bảng ngăn bằng dấu phẩy và định dạng lồng nhau có kiểu.
           Và ta đã biết cách tách chuỗi và dùng từ điển.""",
           focus=[1, "1.2", "1.3", "1.4", "1.5"]),
    ])
    sc_sym = sc("sym", "symbol", "Giải mã mở tệp, chế độ, khối with, và các lệnh CSV, JSON, đường dẫn", [
        st(table(["viết", "đọc là", "nghĩa"],
                 [["<code>open(tên, chế_độ, encoding=\"utf-8\")</code>", "mở tệp", "chế độ <code>\"r\"</code> đọc (mặc định), <code>\"w\"</code> ghi (<b>xoá hết</b> nội dung cũ), <code>\"a\"</code> ghi nối thêm; <code>encoding</code> nói rõ bảng mã"],
                  ["<code>with open(…) as f:</code>", "khối đảm bảo đóng", "ra khỏi khối là tệp <b>tự đóng</b>, kể cả khi có lỗi; <code>f</code> là nhãn của tệp"],
                  ["<code>f.read()</code>, <code>for dong in f:</code>, <code>f.write(s)</code>", "đọc cả, đọc từng dòng, ghi", "<code>read</code> lấy <b>toàn bộ</b> thành một chuỗi; <code>for</code> lấy <b>từng dòng</b> một; <code>write</code> ghi một chuỗi"],
                  ["<code>\"…\\n\"</code>", "xuống dòng", "hai ký tự <code>\\</code> và <code>n</code> trong một chuỗi là <b>một</b> ký tự xuống dòng; <code>s.split(\"\\n\")</code> cắt chuỗi <code>s</code> thành các dòng"]]),
           """Bảng đầu là mở tệp. Lệnh mở nhận tên tệp, chế độ và bảng mã, trong đó chế độ đọc là mặc định. Chế độ ghi xoá hết nội dung cũ. Chế độ nối thêm ghi vào cuối. Khối thứ hai đảm bảo tệp tự đóng khi ra khỏi khối, kể cả khi có lỗi.
           Đọc cả tệp lấy toàn bộ thành một chuỗi, còn vòng lặp lấy từng dòng một. Lệnh ghi ghi một chuỗi. Hai ký tự gạch ngược và n trong một chuỗi là một ký tự xuống dòng, và tách chuỗi tại nó cho ra các dòng.""",
           focus=[1, "1.2", "1.2", "1.2", "1.3", "1.4", "1.4", "1.5"]),
        st(table(["viết", "đọc là", "nghĩa"],
                 [["<code>csv.DictReader(f)</code>", "đọc CSV theo cột", "mỗi dòng là một <b>từ điển</b> (khoá = tên cột); mọi giá trị là <b>chuỗi</b>; mở tệp với <code>newline=\"\"</code> để bộ đọc tự xử lý dấu xuống dòng nằm trong một ô"],
                  ["<code>csv.writer(f).writerow([…])</code>", "ghi một dòng CSV", "ghi các giá trị, thêm dấu phẩy và xuống dòng đúng cách"],
                  ["<code>json.dump(đối_tượng, f)</code>, <code>json.load(f)</code>", "ghi JSON, đọc JSON", "đổi qua lại giữa từ điển/danh sách và chữ JSON; <code>ensure_ascii=False</code> giữ nguyên chữ Việt"],
                  ["<code>from pathlib import Path</code>, <code>Path(\"a\") / \"b\"</code>", "nạp công cụ, rồi ghép đường dẫn", "<code>from X import Y</code>: lấy riêng công cụ <code>Y</code> từ thư viện <code>X</code>, viết một lần ở đầu tệp; rồi <code>.name</code>, <code>.suffix</code>, <code>.exists()</code>, <code>.read_text()</code>, <code>.mkdir()</code>"]]),
           """Bảng thứ hai là bốn công cụ cho dữ liệu. Bộ đọc bảng cho mỗi dòng một từ điển, khoá là tên cột, và mọi giá trị đều là chuỗi. Bộ ghi bảng ghi một dòng với dấu ngăn đúng cách, và cả hai bộ cần mở tệp kèm tham số xuống dòng rỗng để tự xử lý dấu xuống dòng. Hai lệnh dữ liệu cấu trúc đổi qua lại giữa từ điển, danh sách và chữ, và một tham số giữ nguyên chữ Việt.
           Cuối cùng là công cụ đường dẫn: dòng nạp lấy riêng một công cụ từ thư viện của nó, rồi ghép đường dẫn bằng dấu gạch chéo, kèm các lệnh hỏi tên, đuôi, sự tồn tại.""",
           focus=[1, "1.2", "1.3", "1.4", "1.5"], clear=True),
    ])
    sc_int = sc("intuition", "intuition", "Hình dung: chương trình, bộ đệm và đĩa; đọc cả tệp hay từng dòng", [
        st(svg(1500, 400,
               box(20, 140, 290, 120, ["chương trình", "f.write(\"...\")"], C_BLUE, 26, True),
               arrow(315, 200, 470, 200, "#2a78d6", "ghi"),
               box(475, 120, 330, 160, ["bộ đệm (trong bộ nhớ)", "gom chữ chờ ghi"], C_AMBER, 26, True),
               arrow(810, 200, 970, 200, "#16a34a", "đóng tệp"),
               box(975, 140, 250, 120, ["đĩa", "tệp thật"], C_GREEN, 26, True),
               txt(750, 330, "ghi chưa chắc đã xuống đĩa: phải ĐÓNG tệp (hoặc ra khỏi khối with)", 28, "middle", "#dc2626", True),
               txt(750, 375, "khối with đóng tệp giúp bạn, kể cả khi chương trình gặp lỗi", 26, "middle", "#1f2937")),
           """Hình này giải thích vì sao phải đóng tệp. Khi chương trình ghi, chữ chưa đi thẳng xuống đĩa mà được gom trong một bộ đệm trong bộ nhớ. Chỉ khi đóng tệp, bộ đệm mới được đổ xuống đĩa. Vì vậy ghi mà quên đóng thì tệp có thể còn rỗng. Khối đảm bảo đóng làm việc này giúp bạn, kể cả khi chương trình gặp lỗi."""),
        st(svg(1500, 400,
               txt(375, 40, "đọc cả tệp: read()", 28, "middle", "#dc2626", True),
               box(60, 70, 630, 90, ["toàn bộ tệp nằm trong bộ nhớ cùng lúc"], C_RED, 26, True),
               txt(375, 215, "bộ nhớ tăng theo kích thước tệp", 26, "middle", "#dc2626"),
               txt(375, 255, "tệp lớn hơn bộ nhớ: hết bộ nhớ", 26, "middle", "#dc2626"),
               txt(1125, 40, "đọc từng dòng: for dong in f", 28, "middle", "#16a34a", True),
               box(900, 70, 450, 50, ["một dòng"], C_GREEN, 24),
               txt(1125, 160, "xử lý xong thì bỏ, lấy dòng kế", 26, "middle", "#16a34a"),
               txt(1125, 215, "bộ nhớ gần như không đổi", 26, "middle", "#16a34a", True),
               txt(1125, 255, "tệp lớn cỡ nào cũng đọc được", 26, "middle", "#16a34a"),
               txt(750, 350, "đổi lại: đọc từng dòng chỉ cho mỗi lần một dòng, không quay lại được; muốn sắp xếp cả tệp thì phải nghĩ cách khác", 24, "middle", "#1f2937")),
           """Hình thứ hai so sánh hai cách đọc. Đọc cả tệp đặt toàn bộ nội dung vào bộ nhớ cùng lúc, nên bộ nhớ tăng theo kích thước tệp, và tệp lớn hơn bộ nhớ thì chương trình thất bại. Đọc từng dòng chỉ giữ một dòng tại một thời điểm, xử lý xong thì bỏ, nên bộ nhớ gần như không đổi.
           Đổi lại, ta chỉ thấy mỗi lần một dòng, và không quay lại được.""", clear=True),
    ])
    sc_form = sc("formula", "formula", "Suy ra từng bước: ghi rồi đọc, byte của tệp, CSV toàn chuỗi, JSON đổi kiểu", [
        st(run_block(P_GHI, title="Bước 1. Ghi rồi đọc lại, cùng bảng mã")
           + "<p>Vì ghi và đọc cùng <code>encoding=\"utf-8\"</code>, chữ giữ nguyên: $2$ dòng. Nội dung đọc ra có $24$ ký tự nhưng $31$ byte (UTF-8) vì chữ có dấu chiếm nhiều byte.</p>",
           """Bước một, ghi rồi đọc lại cùng bảng mã. Ta ghi hai dòng chữ Việt, rồi đọc cả tệp. Vì ghi và đọc cùng một bảng mã, chữ giữ nguyên, có hai dòng. Nội dung có hai mươi bốn ký tự, nhưng ba mươi mốt byte, vì các chữ có dấu chiếm nhiều byte hơn một."""),
        st("<div class='box key'>Số $31$ byte là của <b>nội dung</b> đọc ra. Trên Windows, tệp nằm trên đĩa là $33$ byte vì mỗi dấu xuống dòng lưu bằng $2$ byte; trên Linux và macOS vẫn $31$.</div>",
           """Trên một số hệ điều hành, mỗi dấu xuống dòng lưu bằng hai byte, nên tệp trên đĩa lớn hơn nội dung đọc ra một chút.""", clear=True),
        st(repl_block(R_MOJI, title="Bước 2. Đọc sai bảng mã cho chữ hỏng")
           + "<p>Vì <code>ề</code> được lưu bằng $3$ byte, đọc theo bảng mã cũ mỗi byte thành một ký tự lạ: <code>tiá»\\x81n</code>. Đúng bảng mã thì trả lại <code>tiền</code>.</p>",
           """Bước hai, đọc sai bảng mã. Chữ tiền được lưu bằng sáu byte. Nếu đọc bằng một bảng mã cũ coi mỗi byte là một ký tự, ta nhận các ký tự lạ thay cho chữ có dấu. Đọc đúng bảng mã thì trả lại đúng chữ. Vì thế luôn nói rõ bảng mã khi mở tệp.""", clear=True),
        st(raw_block(CSV_DATA.strip().split("\n"), title="Bước 3a. Tệp gd.csv (gõ bằng trình soạn thảo, lưu cùng thư mục với chương trình)")
           + "<p>Dòng đầu là <b>tên các cột</b>; mỗi dòng sau là một giao dịch; các cột cách nhau dấu phẩy. Tạo tệp như ở bài đầu: mở trình soạn thảo chữ thuần, gõ nội dung, lưu tên <code>gd.csv</code> (đuôi <code>.csv</code>, mã hoá UTF-8) vào thư mục đang đứng trong cửa sổ lệnh.</p>",
           """Trước khi đọc, ta cần có tệp bảng. Đây là nội dung của nó. Hãy tạo tệp như ở bài đầu, bằng một trình soạn thảo chữ thuần, lưu với tên hiện trên màn hình, đuôi chấm xê ét vê, cùng thư mục với chương trình. Dòng đầu là tên các cột, nên mỗi dòng sau là một giao dịch, các cột cách nhau dấu phẩy.""", clear=True),
        st(run_block(P_CSV, title="Bước 3b. CSV: mỗi dòng một từ điển, mọi giá trị là chuỗi")
           + "<p>Vì CSV chỉ là chữ, <code>hang[\"so_tien\"]</code> là chuỗi <code>'500000'</code>; <code>type(x).__name__</code> cho tên kiểu viết bằng chữ (<code>str</code> = chuỗi); muốn cộng phải <code>int(...)</code>: $500\\,000 + 2\\,000\\,000 + 300\\,000 = 2\\,800\\,000$.</p>",
           """Bước ba, đọc tệp bảng, ở đây bộ đọc cho mỗi dòng một từ điển với khoá là tên cột. Vì tệp chỉ chứa chữ, mọi giá trị đều là chuỗi, kể cả cột số tiền. Dòng in thứ ba hỏi tên kiểu của cột số tiền bằng dấu chấm, và nhận về tên kiểu là chuỗi. Muốn cộng phải đổi sang số nguyên, và tổng ba giao dịch là hai triệu tám trăm nghìn.""", clear=True),
        st(repl_block(R_JSON, 0, 3, title="Bước 4. JSON đổi kiểu qua lại")
           + "<p>Vì JSON có kiểu riêng: <code>True</code> → <code>true</code>, <code>None</code> → <code>null</code>, dấu ngoặc nhọn → đối tượng, ngoặc vuông → mảng. Đọc lại thì trả về từ điển và danh sách. <code>json.dumps(x)</code> đổi <code>x</code> thành chữ JSON (<code>s</code> = chuỗi); <code>json.loads(chữ)</code> đổi chữ JSON ngược lại; bản không có <code>s</code> làm việc với tệp.</p>",
           """Bước bốn, JSON. Lệnh có chữ s ở cuối, nghĩa là chuỗi, đổi dữ liệu thành chữ JSON, và lệnh tải có chữ s đổi ngược lại; bản không có chữ s làm việc với tệp. Vì JSON có kiểu riêng, các kiểu được đổi qua lại. Giá trị đúng của ngôn ngữ này thành chữ viết thường trong JSON, giá trị rỗng thành một từ riêng, từ điển thành đối tượng, danh sách thành mảng. Đọc chữ JSON lại thì trả về từ điển và danh sách như ban đầu.""", clear=True),
    ], checks=["len('tiền mặt\\n2.000.000 đồng\\n'.encode('utf-8')) == 31 and len('tiền mặt\\n2.000.000 đồng\\n') == 24",
               "500000 + 2000000 + 300000 == 2800000", "'tiền'.encode('utf-8').decode('latin-1') != 'tiền'"])
    sc_ex = sc("example", "example", "Ví dụ: ghi và đọc CSV, JSON, và tìm tệp bằng đường dẫn", [
        st(run_block(P_CSVW, title="Ghi CSV: tiêu đề rồi từng hàng"),
           """Ví dụ một, ghi tệp bảng. Ta ghi dòng tiêu đề, rồi hai hàng bằng một lệnh. Bộ ghi tự thêm dấu phẩy ngăn cột và dấu xuống dòng. Đọc lại cho thấy nội dung đúng như mong đợi."""),
        st(run_block(P_JSON, title="Ghi và đọc JSON"),
           """Ví dụ hai, JSON. Ta ghi một báo cáo gồm ngày, số giao dịch, tổng và danh sách loại, rồi đọc lại. Đối tượng đọc lại bằng đúng đối tượng đã ghi, và chữ JSON trong tệp đọc được bằng mắt.""", clear=True),
        st(table(["viết trong mã", "đọc là", "nghĩa"],
                 [["<code>thu_muc.iterdir()</code>", "liệt kê thư mục", "đi qua từng mục (tệp, thư mục con) nằm trong <code>thu_muc</code>"],
                  ["<code>[p.name for p in dãy]</code>", "danh sách suy ra", "dựng một danh sách <b>mới</b>: với mỗi <code>p</code> trong dãy, lấy <code>p.name</code> bỏ vào danh sách"]]),
           """Ở ví dụ sau, ta liệt kê thư mục bằng một danh sách suy ra. Lệnh liệt kê đi qua từng mục trong thư mục. Danh sách suy ra dựng một danh sách mới, với mỗi mục lấy tên của nó bỏ vào danh sách.""", clear=True),
        st(run_block(P_PATH, title="Đường dẫn: dựng thư mục, ghi, hỏi, liệt kê")
           + "<p><code>mkdir</code> tạo thư mục: <code>parents=True</code> tạo luôn thư mục cha còn thiếu (<code>bao_cao</code>); <code>exist_ok=True</code> không báo lỗi nếu thư mục đã có.</p>",
           """Ví dụ ba, đường dẫn. Dấu gạch chéo ghép các phần của đường dẫn. Ta dựng thư mục lồng nhau, ghi một tệp, rồi hỏi tên, đuôi, và liệt kê nội dung thư mục. Lệnh dựng thư mục có hai đối số: đối số đầu dựng luôn thư mục cha còn thiếu, đối số sau không báo lỗi nếu thư mục đã có. Cách này chạy được cả trên các hệ điều hành khác nhau, không cần lo dấu gạch xuôi hay ngược.""", clear=True),
        st(run_block(P_DONG, title="Đọc từng dòng, cộng dồn, không giữ cả tệp"),
           """Ví dụ bốn, đọc từng dòng. Lệnh lấy dòng kế tiếp bỏ dòng tiêu đề. Rồi mỗi lượt xử lý một dòng, cộng dồn tổng và đếm. Bộ nhớ chỉ giữ một dòng, nên cách này dùng được cho tệp lớn. Kết quả ba giao dịch, tổng hai triệu tám trăm nghìn, trùng với bước ba.""", clear=True),
    ], checks=["500000 + 2000000 + 300000 == 2800000"])
    sc_chk = sc("check", "check", "Tự kiểm bằng đường khác: hai cách đọc cho cùng tổng, và cộng tay", [
        st(repl_block(R_KIEM, title="Cộng tay ba số, không qua tệp")
           + "<p>Cách đọc bằng bộ đọc bảng và cách đọc từng dòng bằng <code>split</code> đều cho $2\\,800\\,000$; cộng tay $500\\,000 + 2\\,000\\,000 + 300\\,000$ cũng $2\\,800\\,000$ ✓</p>",
           """Đường kiểm khác, không dùng tệp. Vì ba đường độc lập nên đáng tin. Cộng tay ba số tiền được hai triệu tám trăm nghìn. Hai chương trình đọc tệp bằng hai cách khác nhau, một dùng bộ đọc bảng và một tách từng dòng, đều cho đúng con số này. Ba đường độc lập cùng ra một kết quả."""),
    ], checks=["500000 + 2000000 + 300000 == 2800000"])
    sc_scale = sc("scale", "concept", "Khi tệp lớn dần: đọc cả tệp hết bộ nhớ, đọc từng dòng thì không", [
        st(table(["số dòng", "dung lượng", "đọc cả tệp rồi tách: đỉnh bộ nhớ", "đọc từng dòng: đỉnh bộ nhớ"],
                 [["10 000", bz4[0], bma4[0], bml4[0]], ["1 000 000", bz6[0], bma6[0], bml6[0]],
                  ["100 000 000 (ngoại suy)", bz8[0], bma8[0], bml6[0] + " (không đổi)"]])
           + "<p class='note'>Đo bằng công cụ theo dõi bộ nhớ trên máy kiểm; số minh hoạ. Ngoại suy: bộ nhớ đọc cả tệp tỉ lệ với số dòng.</p>",
           f"""Bảng này là kết quả đo. Mười nghìn dòng chiếm {bz4[1]}, đọc cả tệp cần {bma4[1]}. Một triệu dòng chiếm {bz6[1]}, đọc cả tệp cần {bma6[1]}. Đọc từng dòng, bộ nhớ chỉ cỡ {bml6[1]} ở cả hai quy mô.
           Ngoại suy một trăm triệu dòng, đọc cả tệp cần {bma8[1]}. Đây là số minh hoạ trên máy kiểm."""),
        st(table(["cách đọc, 1 000 000 dòng", "thời gian (đo trên máy kiểm, số minh hoạ)"],
                 [["đọc cả tệp rồi tách", sta6[0]], ["đọc từng dòng", stl6[0]]])
           + "<div class='box key'><b>Đánh đổi:</b> thời gian của hai cách cùng cỡ, nhưng <b>bộ nhớ</b> khác hẳn. Đọc cả tệp tiện khi cần quay lại hay sắp xếp và tệp nhỏ; "
             "đọc từng dòng là lựa chọn mặc định cho tệp có thể lớn, và khi cần thì cộng dồn kết quả thay vì giữ dữ liệu.</div>",
           f"""Còn thời gian thì hai cách cùng cỡ. Đọc cả tệp rồi tách mất {sta6[1]}, đọc từng dòng mất {stl6[1]}. Đánh đổi nằm ở bộ nhớ chứ không ở thời gian. Đọc cả tệp tiện khi cần quay lại hoặc sắp xếp và tệp còn nhỏ. Đọc từng dòng nên là lựa chọn mặc định cho tệp có thể lớn, và khi cần thì cộng dồn kết quả thay vì giữ dữ liệu.""", clear=True),
    ], checks=["100 * 1000000 == 100000000", "16 + 23 * 1000000 == 23000016"])
    sc_pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st('<div class="box warn"><b>Lỗi 1 (người mới).</b> Mở bằng chế độ ghi để “thêm” dữ liệu: chế độ <code>"w"</code> xoá tệp.</div>' + run_block(P_XOA),
           """Lỗi thứ nhất, của người mới, là mở bằng chế độ ghi để thêm dữ liệu. Hai số đầu là kích thước tệp tính bằng byte, hỏi từ hệ điều hành. Chế độ ghi xoá hết nội dung cũ, tệp sáu byte còn hai byte."""),
        st('<div class="box key">Muốn ghi tiếp, dùng chế độ <code>"a"</code>. Phép thử bắt được lỗi: in <b>kích thước tệp</b> trước và sau khi ghi (<code>.stat().st_size</code> hỏi hệ điều hành kích thước tệp theo <b>byte</b>).</div>',
           """Muốn ghi tiếp phải dùng chế độ nối thêm. Phép thử bắt được lỗi này là in kích thước tệp trước và sau khi ghi.""", clear=True),
        st('<div class="box warn"><b>Lỗi 2 (người đã đi làm).</b> Không nói rõ bảng mã: chương trình chạy ở máy này, hỏng ở máy kia.</div>' + term_block(SH_ENC, 0, 1)
           + "<div class='box key'><code>PYTHONIOENCODING=cp1252 python -c \"…\"</code>: tiền tố <code>TÊN=giá_trị</code> đặt biến chỉ cho riêng lệnh này (ở đây ép <b>luồng in</b>, chỗ in chữ ra màn hình, dùng bảng mã cũ <code>cp1252</code>); <code>2&gt; loi.txt</code> chuyển thông báo lỗi vào tệp <code>loi.txt</code>; <code>;</code> kết thúc lệnh này để chạy lệnh kế; <code>echo &#36;?</code> in mã thoát.</div>",
           """Lỗi thứ hai, của người đã đi làm, là không nói rõ bảng mã. Bảng mã mặc định phụ thuộc máy, nên chương trình chạy ở máy này mà hỏng ở máy khác. Ở đây ta đặt một biến ngay trước lệnh, tiền tố chỉ có tác dụng với lệnh đó, ép chỗ in chữ ra màn hình dùng một bảng mã cũ. Dấu lớn hơn kèm số hai chuyển thông báo lỗi vào một tệp. Dấu chấm phẩy kết thúc lệnh này để chạy lệnh kế, và lệnh kế in mã thoát, là một."""),
        st(term_block(SH_ENC, 1, 2, title="Đọc dòng lỗi trong tệp")
           + "<div class='box key'><code>tail -n 1 loi.txt</code> giữ <b>dòng cuối</b> của tệp (thông báo lỗi nằm ở dòng cuối); <code>|</code> chuyển kết quả đó sang lệnh sau; <code>cut -d: -f1</code> lấy phần trước dấu hai chấm đầu tiên.</div>",
           """Lệnh giữ dòng cuối, với số một, lấy dòng cuối của tệp, nơi có tên lỗi. Dấu gạch đứng chuyển kết quả đó sang lệnh sau. Lệnh cắt lấy phần trước dấu hai chấm, và ta nhận tên lỗi mã hoá.""", clear=True),
        st(term_block(SH_ENC, 2, 3, title="Đặt bảng mã cho luồng in thì hết lỗi")
           + '<div class="box key">Luôn ghi <code>encoding="utf-8"</code> khi mở tệp. Khi in chữ Việt bị hỏng, đặt <code>PYTHONIOENCODING=utf-8</code> (hoặc <code>PYTHONUTF8=1</code>).</div>',
           """Đặt bảng mã cho luồng in là hết lỗi. Quy tắc là luôn ghi rõ bảng mã khi mở tệp, và khi in chữ Việt bị hỏng thì đặt bảng mã cho luồng in.""", clear=True),
        st('<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> Ghi xong chưa đóng tệp rồi đọc lại.</div>' + run_block(P_BUF)
           + "<p><code>repr(x)</code> in giá trị <b>kèm cặp nháy</b>: chuỗi rỗng hiện là <code>''</code>, không lẫn với một dòng trống.</p>",
           """Lỗi thứ ba, của người đã đi làm, là ghi xong chưa đóng tệp rồi đọc lại. Lệnh in dạng có nháy cho ta thấy chuỗi rỗng là hai dấu nháy liền nhau, chứ không phải một dòng trống. Chữ còn nằm trong bộ đệm, chưa xuống đĩa, nên đọc ra rỗng. Sau khi đóng tệp, nội dung mới có.""", clear=True, introduces=["pyt_repr"]),
        st('<div class="box key">Dùng khối <code>with</code>: ra khỏi khối là tệp tự đóng. Lỗi này <b>không báo gì</b> và có thể chập chờn, nên rất khó lần ra.</div>',
           """Hãy dùng khối đảm bảo đóng. Lỗi này không báo gì và có thể chập chờn, nên rất khó lần ra.""", clear=True),
    ], checks=["6 > 2 and 6 - 2 == 4"])
    sc_quiz = sc("quiz", "quiz", "Bây giờ tới phần bạn tự làm", [
        st("""<p><b>Đề.</b> Dòng đọc từ tệp: <code>"A02,nap,2000000\\n"</code>.</p>
<ol><li>Bỏ dấu xuống dòng rồi tách: phần tử thứ ba là gì, kiểu gì?</li>
<li>Cộng thêm $1$ vào phần tử đó thế nào?</li></ol>
<p><b>Quyết định:</b> tệp nhật ký có thể $5$ GB, cần đếm số dòng chứa chữ <code>LOI</code>: đọc cả tệp hay từng dòng? Vì sao?</p>""",
           """Bây giờ tới phần bạn tự làm. Một dòng đọc từ tệp có dấu xuống dòng ở cuối. Câu một, bỏ dấu xuống dòng rồi tách, phần tử thứ ba là gì và kiểu gì. Câu hai, cộng thêm một vào phần tử đó thế nào.
           Sau đó là một quyết định, tệp nhật ký có thể năm gi-ga-bai, cần đếm số dòng chứa chữ lỗi, đọc cả tệp hay từng dòng, và vì sao. Hãy dừng video và làm.""".replace("năm gi-ga-bai", "nặng năm tỉ byte"), pause=60),
        st(repl_block(R_QUIZ, title="Câu 1 và câu 2")
           + "<p><code>rstrip(\"\\n\")</code> cắt bỏ dấu xuống dòng ở <b>cuối</b> chuỗi. Tách được <code>['A02', 'nap', '2000000']</code>; phần tử thứ ba là <b>chuỗi</b> <code>'2000000'</code>. Phải đổi kiểu trước khi cộng: $2\\,000\\,000 + 1 = 2\\,000\\,001$.</p>",
           """Đáp án như sau. Lệnh cắt cuối chuỗi bỏ dấu xuống dòng ở cuối dòng. Sau khi tách, phần tử thứ ba là chuỗi hai triệu. Muốn cộng phải đổi sang số nguyên trước, và kết quả là hai triệu không trăm linh một.""", introduces=["pyt_rstrip"]),
        st("<div class='box key'><b>Quyết định:</b> <b>từng dòng</b>. Chỉ cần đếm, không cần quay lại: mỗi dòng xem xong là bỏ, bộ nhớ không đổi dù tệp nặng bao nhiêu. "
           "Đọc cả tệp $5$ GB sẽ cần cỡ $5$ GB bộ nhớ hoặc hơn, nhiều máy không đủ.</div>",
           """Quyết định, đọc từng dòng. Ta chỉ cần đếm, không cần quay lại. Mỗi dòng xem xong là bỏ, nên bộ nhớ không đổi dù tệp nặng bao nhiêu. Đọc cả tệp năm tỉ byte cần cỡ năm tỉ byte bộ nhớ hoặc hơn, nhiều máy không đủ.""", clear=True),
    ], checks=["int('2000000') + 1 == 2000001"])
    sc_prac = practice_scene(sc, "Tự làm: đọc CSV giao dịch, tổng theo loại, ghi JSON báo cáo", pr_steps(
        st, "PYT", "L05",
        """<p><b>Đề</b>: tạo <code>bao_cao.py</code>. Dòng đầu chương trình <b>ghi sẵn</b> tệp <code>gd.csv</code> (6 giao dịch; chép từ <code>de.md</code>: cột <code>ma, loai, tai_khoan, so_tien</code>). Rồi:</p>
<ol><li>đọc bằng <code>csv.DictReader</code>, tính <b>tổng tiền theo loại</b> và <b>số giao dịch</b>;</li>
<li>ghi <code>bao_cao.json</code> (<code>sort_keys=True</code>), đọc lại, in nội dung tệp và <code>so_giao_dich</code>, tổng loại <code>nap</code>.</li></ol>""",
        """Bây giờ tới phần bạn tự làm. Viết chương trình ghi sẵn một tệp bảng sáu giao dịch, chép từ tệp đề bài. Rồi đọc nó bằng bộ đọc bảng, tính tổng tiền theo từng loại và đếm số giao dịch. Ghi kết quả ra một tệp dữ liệu có cấu trúc với các khoá được xếp theo thứ tự, đọc lại, in nội dung tệp, số giao dịch và tổng của loại nạp.
        Hãy dừng video và làm.""",
        LAB_OUT, "bao_cao.py",
        """<div class="box key"><b>Nếu kẹt:</b> <code>tong[loai] = tong.get(loai, 0) + int(hang["so_tien"])</code> trong vòng <code>for hang in csv.DictReader(f)</code>. Ghi: <code>json.dump(bao_cao, f, ensure_ascii=False, sort_keys=True)</code>. Mở mọi tệp với <code>encoding="utf-8"</code>.
Lời giải ở <code>labs/PYT/L05/loi_giai.py</code>.</div>""",
        """Nếu kẹt, dùng từ điển cộng dồn như bài trước, với mỗi hàng đọc từ bộ đọc bảng nhớ đổi số tiền sang số nguyên. Khi ghi, đặt tham số xếp khoá. Mở mọi tệp với bảng mã rõ ràng.
        Lời giải nằm trong thư mục thực hành, chỉ mở sau khi đã thử.""", pause=300), "PYT", "L05")
    write_lab("PYT", "L05", """# Lab PYT L05 — Đọc CSV giao dịch, ghi JSON báo cáo

Cần: Python 3.11 trở lên. Tạo `bao_cao.py`. Dòng đầu chương trình **ghi sẵn** tệp `gd.csv` bằng `Path("gd.csv").write_text(..., encoding="utf-8")` với nội dung (minh hoạ, khác ví dụ trong bài):

```
ma,loai,tai_khoan,so_tien
1,rut,A02,500000
2,chuyen,A01,1200000
3,nap,A03,3000000
4,chuyen,A02,250000
5,rut,A01,700000
6,chuyen,A03,90000
```

1. Đọc bằng `csv.DictReader`; tính **tổng tiền theo loại** (số nguyên) và **số giao dịch**.
2. Ghi `bao_cao.json` dạng `{"so_giao_dich": …, "tong_theo_loai": {…}}` với `sort_keys=True`, `ensure_ascii=False`.
3. Đọc lại tệp; in **nội dung tệp** (một dòng) rồi dòng `<so_giao_dich> <tổng loại nap>`.

Chạy: `python bao_cao.py`. Chấm (chạy từ thư mục gốc của bộ khoá, nơi có thư mục `labs`; để tệp của bạn ở đó hoặc ghi đường dẫn tới tệp): `bash labs/cham.sh PYT L05 bao_cao.py`.
""", "py", LAB_SOL, LAB_OUT)
    sc_rec = sc("recap", "recap", "Chuỗi logic và tư duy cần mang theo", [
        st(chain("with open(…, encoding=\"utf-8\"): mở, dùng, tự đóng", "\"w\" xoá, \"a\" nối thêm", "CSV: mọi giá trị là chuỗi; JSON: giữ kiểu",
                 "Path ghép đường dẫn, chạy mọi hệ điều hành", "đọc từng dòng: bộ nhớ không đổi", "đọc cả tệp: bộ nhớ tăng theo tệp"),
           """Tổng kết chuỗi logic. Mở, dùng, tự đóng trong khối đảm bảo, và luôn nói rõ bảng mã. Chế độ ghi xoá, chế độ nối thêm ghi tiếp. Bảng ngăn dấu phẩy cho mọi giá trị là chuỗi, còn dữ liệu cấu trúc giữ được kiểu. Công cụ đường dẫn chạy trên mọi hệ điều hành.
           Đọc từng dòng giữ bộ nhớ không đổi, còn đọc cả tệp làm bộ nhớ tăng theo kích thước tệp."""),
        st("""<div class='box key'><b>Tư duy:</b> trước khi đọc một tệp, hỏi hai câu: <b>nó lớn đến đâu?</b> và <b>mình có cần giữ cả nó không?</b> Phần lớn việc chỉ cần cộng dồn, đếm, lọc: một dòng một lần.</div>
<p>Bài sau: lớp và đối tượng, để gói dữ liệu cùng hành vi của một tài khoản.</p>""",
           """Điều cần mang theo, trước khi đọc một tệp hãy hỏi hai câu. Nó lớn đến đâu, và mình có cần giữ cả nó không. Phần lớn việc chỉ cần cộng dồn, đếm, lọc, mỗi lần một dòng.
           Bài sau, ta học lớp và đối tượng, để gói dữ liệu cùng hành vi của một tài khoản.""", forward_ref=True),
    ])
    return lesson("L05", "tep_csv_json", "Bài 5 — Tệp: đọc và ghi văn bản, CSV, JSON",
                  "curriculum/pyt.yaml L05; audit/pyt/verify_pyt.py L05 (chạy thật trên Python 3.11 và 3.13, Git Bash; bộ nhớ và thời gian đọc tệp 10^4 và 10^6 dòng đo bằng verify_pyt, máy kiểm, số minh hoạ; ngoại suy 10^8 tuyến tính); "
                  "Python Tutorial §7.2 (Reading and Writing Files), Library Reference: open, csv, json, pathlib, io (bộ đệm); RFC 4180 (CSV), RFC 8259 (JSON), RFC 3629 (UTF-8)",
                  ["Mở, đọc, ghi tệp văn bản trong khối with với bảng mã UTF-8",
                   "Phân biệt các chế độ mở r, w, a và nêu vì sao phải đóng tệp",
                   "Đọc và ghi CSV bằng DictReader và writer, nhớ mọi giá trị đọc ra là chuỗi",
                   "Ghi và đọc JSON, nêu cách kiểu được đổi qua lại",
                   "Ghép và hỏi đường dẫn bằng Path",
                   "Nêu bộ nhớ của đọc cả tệp và đọc từng dòng thay đổi thế nào ở ba quy mô",
                   "Chỉ ra ba lỗi hay gặp: chế độ w xoá tệp, không nói rõ bảng mã, chưa đóng tệp",
                   "Viết chương trình đọc CSV giao dịch và ghi báo cáo JSON"],
                  [sc_hook, sc_pre, sc_sym, sc_int, sc_form, sc_ex, sc_chk, sc_scale, sc_pit, sc_quiz, sc_prac, sc_rec],
                  assumes=["pyt_ngoai_suy"],
                  covers=[(1, "formula"), (2, "pitfalls"), (3, "formula"), (4, "example"), (5, "example"), (6, "scale"), (7, "pitfalls"), (8, "practice")])
