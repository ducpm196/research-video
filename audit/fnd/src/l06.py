from lib import *
from labkit import write_lab, practice_steps, practice_scene

DON = """{
  "ma": 7,
  "khach": "Le Hoa",
  "hang": [
    {"ten": "but", "sl": 3, "gia": 5000},
    {"ten": "vo", "sl": 2, "gia": 12000}
  ],
  "da_tra": true
}
"""
DON_YAML = """ma: 7
khach: Le Hoa
hang:
  - ten: but
    sl: 3
    gia: 5000
  - ten: vo
    sl: 2
    gia: 12000
da_tra: true
"""
DON_CSV = "ten,sl,gia\nbut,3,5000\nvo,2,12000\n"
YAML_LAB = """may_chu:
  cong: 8080
  ten_mien: [a.vn, b.vn]
co_so_du_lieu:
  host: localhost
  cong: 5432
gioi_han:
  thu_lai: 3
"""
LAB_SOL = """cat > don.json <<'EOF'
{
  "ma": 21,
  "khach": "Tran Mai",
  "hang": [
    {"ten": "ao", "sl": 4, "gia": 90000},
    {"ten": "non", "sl": 1, "gia": 45000},
    {"ten": "tat", "sl": 6, "gia": 8000}
  ],
  "da_tra": false
}
EOF
cat > doc.py <<'EOF'
import json
d = json.load(open("don.json"))
hang = d["hang"]
tong = sum(h["sl"] * h["gia"] for h in hang)
print(len(hang), tong)
EOF
python doc.py
echo 8080
echo 2
echo 13512
echo 3"""
LAB_OUT = "3 453000\n8080\n2\n13512\n3"


def build():
    TONG_PY = 'import json\nd = json.load(open("don.json"))\nhang = d["hang"]\ntong = sum(h["sl"] * h["gia"] for h in hang)\nprint(len(hang), tong)\n'
    F = {"don.json": DON, "don.yaml": DON_YAML, "don.csv": DON_CSV, "tong.py": TONG_PY}
    csv_ = cmd("PhienCsv", [("cut -d, -f2 don.csv", "sl\n3\n2"), ("head -n 1 don.csv", "ten,sl,gia")], files=F)
    js = cmd("PhienJson", [
        ("python -c \"import json; d = json.load(open('don.json')); print(d['hang'][1]['gia'])\"", "12000"),
        ("python tong.py", "2 39000"),
        ("python -c \"import json; d = json.load(open('don.json')); print(d['khach'])\"", "Le Hoa"),
    ], files=F)
    demdong = cmd("PhienDem", [("grep -c '\"ten\"' don.json", "2"), ("grep -c 'ten:' don.yaml", "2")], files=F)
    loi = cmd("PhienLoi", [
        ("python -m json.tool loi_nhay.json", "Expecting property name enclosed in double quotes: line 1 column 2 (char 1)"),
        ("python -m json.tool loi_phay.json", "Expecting ',' delimiter: line 2 column 2 (char 10)"),
    ], files={"loi_nhay.json": "{'ma': 7}\n", "loi_phay.json": '{"ma": 7\n "khach": "Le Hoa"}\n'})
    cut = cmd("PhienCut", [
        ("cut -d, -f2 kh_ngoac.csv", 'ten\n"Nguyen\nLe Binh'), ("cut -d, -f2 kh_thuong.csv", "ten\nNguyen An\nLe Binh"),
    ], files={"kh_ngoac.csv": 'ma,ten,so_du\n1,"Nguyen, An",500000\n2,Le Binh,750000\n', "kh_thuong.csv": "ma,ten,so_du\n1,Nguyen An,500000\n2,Le Binh,750000\n"})
    quymo = cmd("PhienQuyMo", [
        ("seq 1 1 | sed 's/.*/&,Le Hoa,39000/' | wc -c", "15"),
        ("seq 1 1 | sed 's/.*/{\"ma\":&,\"khach\":\"Le Hoa\",\"tong\":39000}/' | wc -c", "39"),
        ("seq 1 100 | sed 's/.*/&,Le Hoa,39000/' > a100.csv", ""), ("wc -c a100.csv", "1592 a100.csv"),
        ("seq 1 100 | sed 's/.*/{\"ma\":&,\"khach\":\"Le Hoa\",\"tong\":39000}/' > a100.json", ""), ("wc -c a100.json", "3992 a100.json"),
        ("seq 1 10000 | sed 's/.*/&,Le Hoa,39000/' > a10k.csv", ""), ("wc -c a10k.csv", "178894 a10k.csv"),
        ("seq 1 10000 | sed 's/.*/{\"ma\":&,\"khach\":\"Le Hoa\",\"tong\":39000}/' > a10k.json", ""), ("wc -c a10k.json", "418894 a10k.json"),
        ("head -n 1 a10k.csv", "1,Le Hoa,39000"), ("head -n 1 a10k.json", '{"ma":1,"khach":"Le Hoa","tong":39000}'),
    ])
    quiz = cmd("PhienQuiz", [
        ("python -c \"import json; d = json.load(open('tk.json')); print(d['cac_the'][2]['han_muc'])\"", "30000000"),
        ("python -c \"import json; d = json.load(open('tk.json')); print(sum(t['han_muc'] for t in d['cac_the']))\"", "60000000"),
    ], files={"tk.json": '{"chu": "Pham Nam", "cac_the": [\n  {"loai": "ghi_no", "han_muc": 10000000},\n  {"loai": "tin_dung", "han_muc": 20000000},\n  {"loai": "tra_truoc", "han_muc": 30000000}\n]}\n'})

    sc_hook = sc("hook", "hook", "Thiếu một dấu phẩy, cả tệp bị từ chối: hai hệ thống nói chuyện bằng chữ", [
        st(term_block(loi, 1, 2, title="Máy đối tác nhận tệp JSON thiếu một dấu phẩy")
           + file_block(loi, "loi_phay.json", title="Tệp loi_phay.json"),
           """Chào bạn, hai hệ thống ngân hàng gửi dữ liệu cho nhau bằng tệp chữ. Chỉ cần thiếu một dấu phẩy giữa hai khoá, máy nhận từ chối cả tệp, và báo dòng hai, cột hai, vị trí thứ mười.
           Chữ có cấu trúc nghĩa là mỗi dấu đều có nhiệm vụ, và hôm nay ta học ba dạng phổ biến nhất."""),
        st("""<div class="box key">Hôm nay ta trả lời ba câu hỏi:
<ol><li><b>CSV, JSON, YAML</b> khác nhau thế nào, và mỗi dạng hợp việc gì?</li>
<li>Làm sao <b>đọc</b> một giá trị nằm sâu, ví dụ giá của mặt hàng thứ hai trong đơn?</li>
<li>Lỗi cú pháp nào hay gặp, và khi dữ liệu <b>nhân lên</b> thì chọn dạng nào?</li></ol></div>""",
           """Hôm nay ta trả lời ba câu hỏi. Ba dạng bảng, JSON và YAML khác nhau thế nào, mỗi dạng hợp việc gì. Làm sao đọc một giá trị nằm sâu, ví dụ giá của mặt hàng thứ hai trong đơn.
           Lỗi cú pháp nào hay gặp, và khi dữ liệu nhân lên thì chọn dạng nào."""),
    ])
    sc_pre = sc("prereq", "prereq", "Ôn lại: tệp văn bản, bảng mã, ống và lọc", [
        st(table(["điều đã biết", "nhắc lại, kèm ví dụ"],
                 [["① tệp văn bản UTF-8", "dãy byte đọc ra chữ; mỗi dòng kết thúc bằng ký tự xuống dòng"],
                  ["② cột trong tệp bảng", "<code>cut -d, -f2 f</code> lấy cột thứ 2 khi các cột cách nhau bằng dấu phẩy"],
                  ["③ đếm", "<code>grep -c mẫu f</code> đếm số dòng chứa mẫu"],
                  ["④ đọc thông báo lỗi", "tệp : dòng : cột : mô tả; sửa lỗi đầu tiên trước"]]),
           """Ta ôn lại bốn điều. Tệp văn bản là dãy byte đọc ra chữ theo bảng mã. Lệnh cắt cột lấy một cột khi các cột cách nhau bằng dấu phẩy. Lệnh tìm có cờ c đếm số dòng chứa mẫu.
           Và thông báo lỗi nói tệp, dòng, cột, mô tả, rồi ta sửa lỗi đầu tiên trước.""",
           focus=[1, "1.2", "1.3", "1.4", "1.5"]),
    ])
    sc_sym = sc("sym", "symbol", "Giải mã ba dạng: bảng CSV, JSON và YAML", [
        st(table(["dạng", "cách viết", "nghĩa"],
                 [["<b>CSV</b>", "<code>ten,sl,gia</code> rồi <code>but,3,5000</code>", "bảng bằng chữ: <b>mỗi dòng một hàng</b>, cột cách nhau bằng dấu phẩy; dòng đầu thường là <b>tên cột</b>"],
                  ["<b>JSON</b>", "<code>{\"ten\": \"but\", \"sl\": 3}</code>", "<code>{ }</code> là một <b>đối tượng</b> gồm cặp <b>khoá: giá trị</b>; khoá luôn trong nháy kép; ngăn cặp bằng dấu phẩy"],
                  ["", "<code>[1, 2, 3]</code>", "<code>[ ]</code> là một <b>mảng</b>: danh sách có thứ tự, vị trí đếm từ <b>0</b>"],
                  ["", "<code>\"abc\"  42  true  null</code>", "bốn kiểu giá trị: chữ (nháy kép), số, đúng/sai viết thường, rỗng"]]),
           """Bảng này giải mã dạng bảng và JSON. Dạng bảng thì mỗi dòng là một hàng, các cột cách nhau bằng dấu phẩy, dòng đầu thường là tên cột. JSON dùng ngoặc nhọn cho một đối tượng gồm các cặp khoá và giá trị, khoá luôn nằm trong nháy kép.
           Ngoặc vuông là một mảng, tức danh sách có thứ tự, vị trí đếm từ không. Và giá trị có bốn kiểu, chữ trong nháy kép, số, đúng hoặc sai viết thường, và rỗng.""",
           focus=[1, "1.2", "1.3", "1.4", "1.5"]),
        st(table(["viết", "nghĩa"],
                 [["<code>khoa: gia_tri</code>", "một cặp khoá và giá trị; <b>có khoảng trắng sau dấu hai chấm</b>"],
                  ["thụt lề", "YAML dùng <b>dấu cách</b> đầu dòng để lồng nhau (không dùng phím Tab); cùng cấp thì cùng độ thụt"],
                  ["<code>- ten: but</code>", "dấu gạch đầu dòng bắt đầu <b>một phần tử</b> của danh sách"],
                  ["<code># ghi chú</code>", "chú thích: máy bỏ qua (JSON <b>không</b> có chú thích)"]]),
           """Bảng thứ hai là YAML, dạng viết cho người đọc. Một cặp khoá và giá trị cách nhau bằng dấu hai chấm kèm khoảng trắng. Cấu trúc lồng nhau thể hiện bằng thụt lề dấu cách, không dùng phím nhảy cột, cùng cấp thì cùng độ thụt.
           Dấu gạch đầu dòng bắt đầu một phần tử của danh sách. Và dấu thăng bắt đầu chú thích, mà JSON không có.""",
           focus=[1, "1.2", "1.3", "1.4", "1.5"], clear=True),
    ])
    sc_int = sc("intuition", "intuition", "Hình dung: cùng một đơn hàng, ba cách viết", [
        st(svg(1500, 560,
               panel(10, 10, 440, 530, "CSV: bảng", C_GREEN),
               txt(230, 110, "ten,sl,gia", 28, "middle", "#1f2937", True), txt(230, 160, "but,3,5000", 28, "middle", "#1f2937"), txt(230, 210, "vo,2,12000", 28, "middle", "#1f2937"),
               txt(230, 300, "mỗi dòng = một hàng", 24, "middle", "#16a34a", True), txt(230, 345, "ngắn gọn, mọi hàng cùng cột", 22, "middle", "#1f2937"),
               txt(230, 395, "không có kiểu, không lồng nhau", 22, "middle", "#dc2626"),
               panel(480, 10, 520, 530, "JSON: máy đọc", C_BLUE),
               txt(740, 100, "{ \"ma\": 7,", 24, "middle", "#1f2937"), txt(740, 135, "\"hang\": [", 24, "middle", "#1f2937"),
               txt(740, 170, "{\"ten\": \"but\", \"sl\": 3},", 24, "middle", "#1f2937"), txt(740, 205, "{\"ten\": \"vo\", \"sl\": 2} ] }", 24, "middle", "#1f2937"),
               txt(740, 300, "đối tượng { } và mảng [ ]", 24, "middle", "#2a78d6", True), txt(740, 345, "lồng nhau tự do, có kiểu", 22, "middle", "#1f2937"),
               txt(740, 395, "mọi ngôn ngữ đều có sẵn bộ đọc", 22, "middle", "#1f2937"),
               panel(1030, 10, 460, 530, "YAML: người đọc", C_AMBER),
               txt(1100, 100, "ma: 7", 24, "start", "#1f2937"), txt(1100, 135, "hang:", 24, "start", "#1f2937"),
               txt(1140, 170, "- ten: but", 24, "start", "#1f2937"), txt(1163, 205, "sl: 3", 24, "start", "#1f2937"),
               txt(1260, 300, "thụt lề thay ngoặc", 24, "middle", "#d97706", True), txt(1260, 345, "có chú thích, dễ viết tay", 22, "middle", "#1f2937"),
               txt(1260, 395, "sai một dấu cách là sai nghĩa", 22, "middle", "#dc2626")),
           """Hình này là cùng một đơn hàng viết ba cách. Dạng bảng chỉ có hàng và cột, ngắn gọn, nhưng không có kiểu và không lồng nhau được. JSON dùng ngoặc nhọn và ngoặc vuông, lồng nhau tự do, và mọi ngôn ngữ lập trình đều có sẵn bộ đọc.
           YAML dùng thụt lề thay cho ngoặc, có chú thích, dễ viết tay, nhưng sai một dấu cách là sai nghĩa. Ba dạng chứa cùng thông tin, chỉ khác cách trình bày."""),
    ])
    sc_form = sc("formula", "formula", "Suy ra từng bước: đường đi tới một giá trị nằm sâu", [
        st(file_block(cmd("Mau", [("true", "")], files=F), "don.json", title="Tệp don.json")
           + "<p><b>Bước 1.</b> Muốn giá của <b>mặt hàng thứ hai</b>. Vì ngoài cùng là đối tượng <code>{ }</code>, đi vào bằng <b>tên khoá</b>: <code>hang</code>.</p>",
           """Bước một, muốn giá của mặt hàng thứ hai trong đơn. Vì ngoài cùng là một đối tượng, nên ta đi vào bằng tên khoá. Khoá hang trỏ tới một mảng hai phần tử."""),
        st("""<p><b>Bước 2.</b> <code>hang</code> là mảng <code>[ ]</code>, đi vào bằng <b>vị trí</b>, và vị trí đếm từ $0$. Phần tử <b>thứ hai</b> có vị trí $2 - 1 = \\hl{1}$.</p>
<p class="note">Làm thử: mảng có $2$ phần tử, vị trí hợp lệ là $0$ và $1$; vị trí $2$ không tồn tại.</p>""",
           """Bước hai, khoá hang là một mảng, nên đi vào bằng vị trí, và vị trí đếm từ không. Phần tử thứ hai có vị trí hai trừ một bằng một. Làm thử, mảng có hai phần tử nên vị trí hợp lệ là không và một, còn vị trí hai không tồn tại."""),
        st("""<p><b>Bước 3.</b> Phần tử đó là đối tượng, lại đi vào bằng khoá <code>gia</code>. Ghép các bước từ ngoài vào trong:</p>
$$\\text{hang} \\to [1] \\to \\text{gia} \\;\\Rightarrow\\; \\hl{12000}$$""",
           """Bước ba, phần tử đó lại là một đối tượng, nên đi tiếp bằng khoá gia. Ghép các bước từ ngoài vào trong, khoá hang, vị trí một, khoá gia, ta được mười hai nghìn."""),
    ], checks=["2 - 1 == 1", "__import__('json').loads('{\"hang\": [{\"gia\": 5000}, {\"gia\": 12000}]}')['hang'][1]['gia'] == 12000"])
    sc_ex = sc("example", "example", "Ví dụ: đọc cùng một đơn hàng bằng ba dạng, năm phép làm", [
        st(file_block(cmd("Mau2", [("true", "")], files=F), "don.csv", title="① Dạng bảng: tệp don.csv") + term_block(csv_, 0, 1, title="Lấy cột sl (số lượng)"),
           """Phép làm thứ nhất, dạng bảng. Dòng đầu là tên cột, hai dòng sau là hai mặt hàng. Lệnh cắt cột thứ hai lấy cột số lượng, và kết quả có cả tên cột. Muốn bỏ tên cột, ta dùng lệnh bỏ dòng đầu đã học."""),
        st(term_block(js, 0, 1, title="② JSON: giá của mặt hàng thứ hai")
           + "<p>Đường đi <code>d['hang'][1]['gia']</code> ra $12000$, đúng như tính ở bước 3.</p>",
           """Phép làm thứ hai, đọc JSON bằng một dòng lệnh của ngôn ngữ thứ hai. Đường đi là khoá hang, vị trí một, khoá gia. Màn hình ra mười hai nghìn, đúng như ta tính ở bước ba."""),
        st(file_block(cmd("Mau4", [("true", "")], files=F), "tong.py", title="③ Tệp tong.py: số mặt hàng và tổng tiền") + term_block(js, 1, 2)
           + "<p>Tổng $= 3 \\times 5000 + 2 \\times 12000 = 15000 + 24000 = \\hl{39000}$ ✓</p>",
           """Phép làm thứ ba, tính trên dữ liệu. Có hai mặt hàng, và tổng tiền là ba nhân năm nghìn cộng hai nhân mười hai nghìn, bằng mười lăm nghìn cộng hai mươi tư nghìn, tức ba mươi chín nghìn. Máy tính ra cùng con số."""),
        st(file_block(cmd("Mau3", [("true", "")], files=F), "don.yaml", title="④ YAML: cùng nội dung, thụt lề thay ngoặc")
           + "<p>Hai dấu cách đầu dòng nghĩa là <b>nằm trong</b> khoá <code>hang</code>; dấu <code>-</code> mở phần tử mới; <code>sl</code> và <code>gia</code> thẳng cột với <code>ten</code> nên cùng một phần tử.</p>",
           """Phép làm thứ tư, cùng đơn hàng viết bằng YAML. Hai dấu cách đầu dòng nghĩa là nằm trong khoá hang. Dấu gạch đầu dòng mở một phần tử mới. Số lượng và giá thẳng cột với tên, nên thuộc cùng một phần tử.
           Đọc bằng mắt, giá của mặt hàng thứ hai vẫn là mười hai nghìn."""),
        st(term_block(loi, 0, 1, title="⑤ Lỗi cú pháp JSON: nháy đơn thay nháy kép")
           + "<p>Thông báo nói: <b>cần tên khoá trong nháy kép</b>, ở dòng 1, cột 2 (đúng chỗ dấu <code>'</code>).</p>".replace("dòng 1", "dòng thứ 1"),
           """Phép làm thứ năm, một lỗi cú pháp thật. Tệp dùng nháy đơn thay cho nháy kép. Thông báo nói cần tên khoá trong nháy kép, ở dòng một, cột hai, đúng chỗ dấu nháy đơn."""),
    ], checks=["3 * 5000 + 2 * 12000 == 39000", "15000 + 24000 == 39000",
               "__import__('json').loads('{\"ma\": 7, \"khach\": \"Le Hoa\", \"hang\": [{\"ten\": \"but\", \"sl\": 3, \"gia\": 5000}, {\"ten\": \"vo\", \"sl\": 2, \"gia\": 12000}], \"da_tra\": true}')['hang'][1]['gia'] == 12000"])
    sc_chk = sc("check", "check", "Tự kiểm bằng đường khác: JSON và YAML là cùng dữ liệu, đếm theo hai cách", [
        st(term_block(demdong, title="Đếm số mặt hàng bằng cách đếm khoá ten trong mỗi tệp")
           + "<p>Hai tệp, hai cách viết, cùng đếm ra $2$ mặt hàng. Khớp với mảng có $2$ phần tử ✓</p>",
           """Đường kiểm khác là đếm số mặt hàng bằng cách đếm khoá tên trong từng tệp. Tệp JSON ra hai, tệp YAML cũng ra hai, nên khớp với mảng có hai phần tử, vì mỗi mặt hàng có đúng một khoá tên."""),
        st("""<p>Kiểm cuối: JSON và YAML ở trên <b>cùng một dữ liệu</b>. Nạp cả hai vào bộ đọc rồi so sánh, kết quả là <b>bằng nhau</b> ✓</p>
<p class="note">Hai cách viết khác nhau, nghĩa như nhau: chọn dạng theo người đọc và theo bên nhận, không theo nội dung.</p>""",
           """Kiểm cuối, nạp cả hai tệp vào bộ đọc rồi so sánh, kết quả là bằng nhau. Hai cách viết khác nhau nhưng nghĩa như nhau. Vì vậy ta chọn dạng theo người đọc và theo bên nhận, không theo nội dung."""),
    ], checks=["__import__('json').loads(\"\"\"" + DON + "\"\"\") == __import__('yaml').safe_load(\"\"\"" + DON_YAML + "\"\"\")",
               "__import__('json').loads(\"\"\"" + DON + "\"\"\")['hang'].__len__() == 2"])
    sc_scale = sc("scale", "example", "Khi số bản ghi nhân lên: JSON lặp khoá nên to hơn CSV", [
        st(term_block(quymo, 10, 12, title="Một bản ghi giống nhau, hai cách viết"),
           """Ta sinh cùng một bản ghi giả bằng hai cách. Dạng bảng chỉ có giá trị, còn JSON lặp lại tên khoá ở mỗi bản ghi. Ở đây ta lặp bản ghi ấy nhiều lần bằng lệnh in dãy số nối với lệnh thay chữ, rồi đo dung lượng."""),
        st(table(["số bản ghi", "CSV (byte)", "JSON mỗi dòng một bản ghi (byte)", "tỉ lệ JSON / CSV"],
                 [["×1: 1", "15", "39", "2,6"], ["×100: 100", "1 592", "3 992", "2,5"], ["×10 000: 10 000", "178 894", "418 894", "2,3"]])
           + "<div class='box key'><b>Đánh đổi:</b> JSON to hơn gấp hơn hai lần vì lặp khoá, nhưng tự mô tả và lồng nhau được; CSV gọn nhưng người nhận phải biết sẵn ý nghĩa từng cột. "
             "Hàng chục triệu bản ghi: ưu tiên dạng gọn hoặc dạng nén, và đọc <b>từng dòng</b> thay vì nạp cả tệp.</div>",
           """Bảng này là dung lượng đo được. Một bản ghi bảng chỉ mười lăm byte, JSON ba mươi chín byte. Một nghìn lần nhiều hơn cũng thế, JSON luôn to hơn gấp hơn hai lần, vì lặp tên khoá ở mỗi bản ghi.
           Người làm nghề phải cân đối. JSON tự mô tả và lồng nhau được, bảng thì gọn nhưng người nhận phải biết ý nghĩa từng cột. Với hàng chục triệu bản ghi, hãy ưu tiên dạng gọn, và đọc từng dòng thay vì nạp cả tệp.""", clear=True),
    ], checks=["round(39 / 15, 1) == 2.6", "round(3992 / 1592, 1) == 2.5", "round(418894 / 178894, 1) == 2.3", "10000 // 100 == 100"])
    sc_pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st('<div class="box warn"><b>Lỗi 1 (người mới).</b> JSON khắt khe: thiếu dấu phẩy giữa hai cặp, hoặc dùng nháy đơn.</div>'
           + term_block(loi) + "<p>Phép thử: <b>chạy bộ kiểm cú pháp</b> trước khi gửi; đọc dòng, cột trong thông báo. JSON không cho nháy đơn, không cho chú thích, không cho dấu phẩy thừa ở cuối.</p>",
           """Lỗi thứ nhất, của người mới, là JSON khắt khe. Dùng nháy đơn hay thiếu dấu phẩy giữa hai cặp đều bị từ chối, kèm dòng và cột. Phép thử là chạy bộ kiểm cú pháp trước khi gửi, và đọc dòng, cột trong thông báo.
           JSON cũng không cho chú thích."""),
        st('<div class="box warn"><b>Lỗi 2 (người mới).</b> YAML hiểu giá trị theo cách nó <b>đoán</b>: <code>co: no</code> thành <b>đúng/sai</b>, không phải chữ “no”.</div>'
           + table(["bạn viết", "một số bộ đọc YAML hiểu là"], [["<code>co: no</code>", "giá trị sai (false), không phải chữ <code>no</code>"], ["<code>ma: 007</code>", "số, có thể mất hai số 0 đầu"], ["<code>ma: \"007\"</code>", "chữ <code>007</code> nguyên vẹn"]])
           + "<p>Cách tránh: đặt <b>nháy kép</b> quanh giá trị là chữ. Phép thử: nạp tệp vào bộ đọc và in kiểu từng giá trị.</p>",
           """Lỗi thứ hai, cũng của người mới, là YAML đoán kiểu của giá trị. Viết no có thể thành giá trị sai, không phải chữ no. Viết số có hai số không đầu có thể mất các số không. Cách tránh là đặt nháy kép quanh giá trị là chữ.
           Phép thử là nạp tệp vào bộ đọc và in kiểu từng giá trị."""),
        st('<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> Cắt cột CSV bằng <code>cut -d,</code> khi ô có dấu phẩy bên trong.</div>'
           + term_block(cut) + "<p>Ô <code>\"Nguyen, An\"</code> bị cắt làm hai: cột 2 chỉ còn <code>\"Nguyen</code>. CSV thật cần bộ đọc biết nháy kép; <code>cut</code> thì không.</p>",
           """Lỗi thứ ba, của cả người đã đi làm, là cắt cột bằng lệnh cắt khi ô có dấu phẩy bên trong. Ở đây tên có dấu phẩy được bọc trong nháy kép, nhưng lệnh cắt không biết, nên chỉ lấy được nửa tên. Kết quả sai mà không báo lỗi.
           Tệp bảng thật cần bộ đọc của ngôn ngữ lập trình, biết xử lý nháy kép."""),
    ])
    sc_quiz = sc("quiz", "quiz", "Bây giờ tới phần bạn tự làm", [
        st(file_block(quiz, "tk.json", title="Tệp tk.json (số minh hoạ)")
           + "<p><b>Đề.</b> (1) Hạn mức của thẻ <b>thứ ba</b> là bao nhiêu? Viết đường đi. (2) Tổng hạn mức các thẻ? <b>Chọn</b>: gửi 10 triệu bản ghi dạng này cho đối tác, bạn chọn CSV hay JSON, và vì sao?</p>",
           """Bây giờ tới phần bạn tự làm. Tệp có tên chủ thẻ và ba thẻ, mỗi thẻ có một hạn mức. Câu một, hạn mức của thẻ thứ ba là bao nhiêu, và viết đường đi. Câu hai, tổng hạn mức các thẻ. Câu ba là một quyết định,
           gửi mười triệu bản ghi dạng này cho đối tác thì chọn dạng bảng hay JSON, và vì sao. Hãy dừng video và làm.""", pause=60),
        st(term_block(quiz)
           + table(["câu", "đáp án", "lý do"],
                   [["1", "<code>cac_the</code> → <code>[2]</code> → <code>han_muc</code> = <b>30 000 000</b>", "thẻ thứ ba có vị trí $3 - 1 = 2$"],
                    ["2", "$10 + 20 + 30 = \\hl{60}$ triệu = <b>60 000 000</b>", "cộng ba hạn mức"]]),
           """Đáp án câu một, đường đi là khoá các thẻ, vị trí hai, khoá hạn mức, ra ba mươi triệu, vì thẻ thứ ba có vị trí ba trừ một bằng hai. Câu hai, mười cộng hai mươi cộng ba mươi bằng sáu mươi triệu. Máy chạy thật cho cùng kết quả."""),
        st("<div class='box key'><b>Quyết định:</b> với $10$ triệu bản ghi đồng dạng, chọn <b>CSV</b> (hoặc JSON mỗi dòng một bản ghi, nén): chênh $\\approx 2{,}3\\times$ dung lượng (bảng đo ở bước trước). "
           "Chọn JSON khi bản ghi <b>lồng nhau</b> hoặc bên nhận cần tự hiểu cấu trúc. Dù chọn gì, thỏa thuận trước <b>bảng mã UTF-8</b> và <b>cách xuống dòng</b>.</div>",
           """Về quyết định, với mười triệu bản ghi đồng dạng, nên chọn dạng bảng, hoặc JSON mỗi dòng một bản ghi rồi nén, vì chênh khoảng hai phẩy ba lần dung lượng. Chọn JSON khi bản ghi lồng nhau hoặc bên nhận cần tự hiểu cấu trúc.
           Dù chọn gì, hãy thoả thuận trước bảng mã và cách xuống dòng.""", clear=True),
    ], checks=["10 + 20 + 30 == 60", "3 - 1 == 2", "round(418894 / 178894, 1) == 2.3"])
    sc_prac = practice_scene(sc, "Tự làm: viết tay một tệp JSON và đọc một tệp YAML", pr_steps(
        st, "FND", "L06",
        """<p><b>Đề</b>: tạo <code>doc_ghi.sh</code>.</p>
<ol><li>Bằng <code>cat &gt; don.json &lt;&lt;'EOF'</code>, <b>viết tay</b> JSON đơn <code>21</code>, khách <code>Tran Mai</code>, đã trả <code>false</code>, 3 mặt hàng: <code>ao</code> 4 × 90000, <code>non</code> 1 × 45000, <code>tat</code> 6 × 8000.</li>
<li>Tạo <code>doc.py</code> (chép từ <code>de.md</code>) rồi <code>python doc.py</code>: in <b>số mặt hàng</b> và <b>tổng tiền</b>.</li>
<li>Đọc YAML trong <code>de.md</code>, in bốn số: cổng máy chủ; số tên miền; tổng hai cổng; số lần thử lại.</li></ol>""",
        """Bây giờ tới phần bạn tự làm. Tạo một tệp lệnh. Viết tay một tệp JSON cho đơn hai mươi mốt, khách Trần Mai, chưa trả. Có ba mặt hàng, áo bốn cái giá chín mươi nghìn, nón một cái giá bốn mươi lăm nghìn, tất sáu đôi giá tám nghìn.
        Rồi tạo tệp đọc theo đề và chạy, in số mặt hàng và tổng tiền. Cuối cùng đọc một tệp YAML trong đề và in bốn con số. Hãy dừng video và làm.""",
        LAB_OUT, "doc_ghi.sh",
        """<div class="box key"><b>Nếu kẹt:</b> JSON: ngoặc nhọn ngoài; <code>"hang"</code> là mảng <code>[ ]</code> chứa ba đối tượng, khoá trong nháy kép, ngăn bằng dấu phẩy, <b>không</b> có dấu phẩy sau phần tử cuối; <code>false</code> viết thường.
Tổng tiền $= 4 \\times 90000 + 45000 + 6 \\times 8000 = 453000$. Lời giải ở <code>labs/FND/L06/loi_giai.sh</code>.</div>""",
        """Nếu kẹt, JSON có ngoặc nhọn ngoài cùng, khoá hàng là một mảng chứa ba đối tượng. Khoá nằm trong nháy kép, các cặp ngăn bằng dấu phẩy, và không có dấu phẩy sau phần tử cuối. Giá trị sai viết thường.
        Tổng tiền là bốn nhân chín mươi nghìn, cộng bốn mươi lăm nghìn, cộng sáu nhân tám nghìn, bằng bốn trăm năm mươi ba nghìn. Lời giải nằm trong thư mục thực hành, chỉ mở sau khi đã thử.""", pause=300), "FND", "L06")
    write_lab("FND", "L06", """# Lab FND L06 — Viết tay JSON, đọc YAML

Tạo `doc_ghi.sh`:

1. **Viết tay** tệp `don.json` bằng `cat > don.json <<'EOF' … EOF`: đơn `ma` 21, `khach` `Tran Mai`, `da_tra` `false` (viết thường), `hang` là mảng 3 phần tử, mỗi phần tử có `ten`, `sl`, `gia`: `ao` 4 × 90000, `non` 1 × 45000, `tat` 6 × 8000.
2. Tạo `doc.py` (chép nguyên; đọc JSON bằng Python, in số mặt hàng và tổng tiền) rồi chạy `python doc.py`:

```python
import json
d = json.load(open("don.json"))
hang = d["hang"]
tong = sum(h["sl"] * h["gia"] for h in hang)
print(len(hang), tong)
```

3. Đọc YAML dưới đây **bằng mắt**, rồi dùng `echo` in bốn số (mỗi số một dòng): (a) cổng của `may_chu`; (b) số tên miền trong `ten_mien`; (c) tổng hai cổng (`may_chu` + `co_so_du_lieu`); (d) `thu_lai`.

```yaml
""" + YAML_LAB + """```

Chạy `bash doc_ghi.sh`; chấm: `bash labs/cham.sh FND L06 doc_ghi.sh`. Cần Python theo bài đầu tiên. Dòng sai cú pháp JSON sẽ in lỗi (đọc dòng, cột) thay cho số.
""", "sh", LAB_SOL, LAB_OUT)
    sc_rec = sc("recap", "recap", "Chuỗi logic và tư duy cần mang theo", [
        st(chain("CSV: hàng, cột, dấu phẩy", "JSON: { } khoá–giá trị, [ ] mảng từ 0", "YAML: thụt lề, dấu - mở phần tử",
                 "đường đi: khoá → vị trí → khoá", "chạy bộ kiểm cú pháp trước khi gửi", "chọn dạng theo bên nhận và quy mô"),
           """Tổng kết chuỗi logic. Bảng có hàng, cột và dấu phẩy. JSON có ngoặc nhọn cho cặp khoá và giá trị, ngoặc vuông cho mảng đếm từ không. YAML thụt lề, và dấu gạch đầu dòng mở một phần tử.
           Đường đi tới giá trị sâu là khoá, vị trí, khoá. Chạy bộ kiểm cú pháp trước khi gửi, và chọn dạng theo bên nhận và quy mô."""),
        st("""<div class='box key'><b>Tư duy:</b> dữ liệu có cấu trúc là hợp đồng giữa người viết và máy đọc: kiểm cú pháp bằng máy, đừng tin mắt; kiểm <b>kiểu</b> của giá trị, đừng tin cách nó trông.</div>
<p>Bài sau: hai chương trình nói chuyện qua mạng bằng HTTP, và bạn sẽ hỏi một máy chủ bằng chữ.</p>""",
           """Điều cần mang theo, dữ liệu có cấu trúc là hợp đồng giữa người viết và máy đọc. Hãy kiểm cú pháp bằng máy, đừng tin mắt, và kiểm kiểu của giá trị, đừng tin cách nó trông.
           Bài sau, ta học hai chương trình nói chuyện qua mạng bằng HTTP, và bạn sẽ hỏi một máy chủ bằng chữ.""", forward_ref=True),
    ])
    return lesson("L06", "du_lieu_co_cau_truc", "Bài 6 — Dữ liệu có cấu trúc: CSV, JSON và YAML",
                  "curriculum/fnd.yaml L06; audit/fnd/verify_fnd.py L06 (Git Bash + Python: json.tool, json.load, cut, sed, wc chạy thật); "
                  "RFC 8259 (JSON); RFC 4180 (CSV); YAML 1.2 specification (yaml.org); Python docs: json (json.tool), "
                  "PyYAML safe_load (YAML 1.1: no → false; dùng trong checks, không hiện trên màn hình); dung lượng 15/39, 1 592/3 992, 178 894/418 894 byte đo bằng verify_fnd",
                  ["Đọc cùng một đơn hàng ở ba dạng CSV, JSON, YAML và chỉ ra hàng, cột, khoá, giá trị, mảng",
                   "Tính đường đi tới một giá trị nằm sâu: khoá, vị trí đếm từ 0, khoá",
                   "Kiểm một giá trị bằng hai đường: đếm khoá và nạp vào bộ đọc",
                   "So sánh dung lượng CSV và JSON khi số bản ghi nhân lên rồi chọn dạng",
                   "Chỉ ra ba lỗi hay gặp: JSON khắt khe, YAML đoán kiểu, cắt cột CSV khi ô có dấu phẩy",
                   "Viết tay một tệp JSON hợp lệ và đọc các giá trị trong một tệp YAML"],
                  [sc_hook, sc_pre, sc_sym, sc_int, sc_form, sc_ex, sc_chk, sc_scale, sc_pit, sc_quiz, sc_prac, sc_rec],
                  covers=[(1, "example"), (2, "formula"), (3, "check"), (4, "scale"), (5, "pitfalls"), (6, "practice")])
