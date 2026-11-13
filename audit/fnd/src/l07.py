from pathlib import Path
from lib import *
from labkit import write_lab, practice_steps, practice_scene

MAY_CHU = (Path(__file__).resolve().parents[1] / "assets" / "may_chu_l07.py").read_text(encoding="utf-8")
LAB_SERVER = """import sys
from http.server import BaseHTTPRequestHandler, HTTPServer


class Xu(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def tra(self, ma, nd):
        nd = nd.encode()
        self.send_response_only(ma)
        self.send_header("Content-Length", str(len(nd)))
        self.end_headers()
        self.wfile.write(nd)

    def do_GET(self):
        if self.path == "/chao":
            self.tra(200, "xin chao tu lab")
        elif self.path == "/tai_khoan/42":
            self.tra(200, "so du 750000")
        else:
            self.tra(404, "khong thay")

    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        self.rfile.read(n)
        self.tra(201 if self.path == "/nap" else 404, "da nhan")

    def log_message(self, *a):
        pass


HTTPServer(("127.0.0.1", int(sys.argv[1])), Xu).serve_forever()
"""
LAB_START = "cat > may_chu.py <<'EOF'\n" + LAB_SERVER + """EOF
python may_chu.py 18766 > /dev/null 2>&1 &
SV=$!
for i in 1 2 3 4 5 6 7 8 9 10; do
  curl -s -o /dev/null http://127.0.0.1:18766/ && break
  sleep 0.3
done
U=http://127.0.0.1:18766"""
LAB_BODY = """curl -s -o /dev/null -w "%{http_code}\\n" $U/chao
curl -s -o /dev/null -w "%{http_code}\\n" $U/khong_co
curl -s $U/tai_khoan/42; echo
curl -s -o /dev/null -w "%{http_code}\\n" -X POST -d so_tien=100000 $U/nap
kill $SV"""
LAB_OUT = "200\n404\nso du 750000\n201"
U = "http://127.0.0.1:18765"


def build():
    h = cmd("PhienHttp", [
        ("python may_chu.py 18765 > /dev/null 2>&1 & SV=$!", ""), ("sleep 1", ""), ("U=" + U, ""),
        ("curl -s $U/", "xin chao"),
        ("curl -s -i $U/so_du", "HTTP/1.1 200 OK\nContent-Type: text/plain\nContent-Length: 7\n\n1500000"),
        ('curl -s -o /dev/null -w "%{http_code}\\n" $U/khong_co', "404"),
        ('curl -s $U/khong_co; echo " ma thoat: $?"', "khong thay ma thoat: 0"),
        ('curl -sf $U/khong_co; echo "ma thoat: $?"', "ma thoat: 22"),
        ("curl -s -i -X POST -d a=1 $U/chuyen", "HTTP/1.1 201 Created\nContent-Type: text/plain\nContent-Length: 12\n\nda nhan: a=1"),
        ("curl -s -i $U/chuyen", "HTTP/1.1 405 Method Not Allowed\nContent-Type: text/plain\nContent-Length: 13\n\nchi nhan POST"),
        ('curl -s -o /dev/null -w "%{http_code}\\n" $U/loi', "500"),
        ("curl -s $U/het_han", '{"loi": "het han"}'),
        ('curl -s -o /dev/null -w "%{http_code}\\n" $U/het_han', "200"),
        ('curl -s --max-time 1 $U/cham; echo "ma thoat: $?"', "ma thoat: 28"),
        ("kill $SV", ""),
    ], files={"may_chu.py": MAY_CHU})

    sc_hook = sc("hook", "hook", "Một địa chỉ, một yêu cầu, một con số: máy chủ trả lời bằng chữ", [
        st(term_block(h, 3, 5, title="Hỏi một máy chủ nhỏ chạy ngay trên máy bạn, đọc nguyên văn câu trả lời")
           + "<p>Dòng đầu có <b>mã trạng thái</b> <code>200</code>: “thành công”. Tiếp là các dòng tiêu đề, một dòng trống, rồi <b>nội dung</b>.</p>",
           """Chào bạn, mỗi lần bạn mở một trang mạng hay một ứng dụng ngân hàng gọi máy chủ, đều có một cuộc hỏi đáp bằng chữ như thế này. Ta hỏi một máy chủ nhỏ chạy ngay trên máy bạn, và đọc nguyên văn câu trả lời.
           Dòng đầu có mã trạng thái hai trăm, nghĩa là thành công. Tiếp là các dòng tiêu đề, một dòng trống, rồi nội dung, ở đây là số một triệu năm trăm nghìn."""),
        st("""<div class="box key">Hôm nay ta trả lời ba câu hỏi:
<ol><li>Một <b>yêu cầu</b> và một <b>phản hồi</b> HTTP gồm những phần nào?</li>
<li>Mã trạng thái <b>2xx, 4xx, 5xx</b> nói điều gì, và <b>phương thức</b> GET, POST khác nhau thế nào?</li>
<li>Vì sao <code>curl</code> báo mã thoát 0 dù gặp 404, và khi yêu cầu nhân lên thì cần bao nhiêu “người phục vụ”?</li></ol></div>""",
           """Hôm nay ta trả lời ba câu hỏi. Một yêu cầu và một phản hồi HTTP gồm những phần nào. Mã trạng thái hai trăm, bốn trăm, năm trăm nói điều gì, và phương thức đọc với phương thức gửi khác nhau thế nào.
           Và vì sao lệnh gửi yêu cầu báo mã thoát không dù gặp lỗi bốn trăm linh bốn, cùng việc khi yêu cầu nhân lên thì cần bao nhiêu người phục vụ."""),
    ])
    pre_rows = [["① biến", code("U=http://127.0.0.1:18765") + " rồi " + code("$U/so_du")],
                ["② mã thoát", code("$?") + " = <b>0</b> thành công, khác 0 thất bại"],
                ["③ chạy nền", code("lệnh &") + ": chạy ngầm, cửa sổ vẫn nhận lệnh khác; " + code("$!") + " là số tiến trình vừa chạy ngầm"],
                ["④ bỏ đầu ra", code("> /dev/null 2>&1") + " vứt cả kết quả lẫn thông báo lỗi"]]
    sc_pre = sc("prereq", "prereq", "Ôn lại: biến, mã thoát, chạy nền, bỏ đầu ra", [
        st(table(["điều đã biết", "nhắc lại, kèm ví dụ"], pre_rows),
           """Ta ôn lại bốn điều. Biến giữ địa chỉ để khỏi gõ lại. Mã thoát không là thành công, khác không là thất bại. Dấu và ở cuối lệnh chạy nó ngầm, cửa sổ vẫn nhận lệnh khác, và dấu đô la chấm than là số của tiến trình vừa chạy ngầm.
           Và ta có thể vứt cả kết quả lẫn thông báo lỗi vào thùng không đáy.""",
           focus=[1, "1.2", "1.3", "1.4", "1.5"]),
    ])
    sc_sym = sc("sym", "symbol", "Giải mã: máy khách, máy chủ, địa chỉ, phương thức, mã trạng thái", [
        st(table(["thuật ngữ", "nghĩa"],
                 [["<b>máy chủ</b> và <b>máy khách</b>", "máy chủ là chương trình <b>chờ</b> yêu cầu và trả lời; máy khách (trình duyệt, <code>curl</code>, ứng dụng) là bên <b>hỏi</b>"],
                  ["<b>địa chỉ</b> (URL)", code("http://127.0.0.1:18765/so_du") + " = giao thức + <b>địa chỉ máy</b> (<code>127.0.0.1</code> là chính máy bạn) + <b>cổng</b> (<code>18765</code>, cửa của chương trình) + <b>đường dẫn</b>"],
                  ["<b>phương thức</b>", "<code>GET</code> = đọc (không làm đổi gì); <code>POST</code> = gửi dữ liệu để tạo hoặc xử lý"],
                  ["<b>mã trạng thái</b>", "số ba chữ số trong dòng đầu phản hồi: <b>chữ số đầu là nhóm</b>"]]),
           """Bảng này giải mã năm thuật ngữ. Máy chủ là chương trình chờ yêu cầu và trả lời, máy khách là bên hỏi. Địa chỉ gồm giao thức, địa chỉ máy, cổng, tức cửa của chương trình, và đường dẫn. Địa chỉ một hai bảy chấm không chấm không chấm một là chính máy bạn.
           Phương thức đọc không làm đổi gì, phương thức gửi đưa dữ liệu để tạo hoặc xử lý. Và mã trạng thái là số ba chữ số trong dòng đầu của phản hồi, chữ số đầu cho biết nhóm.""",
           focus=[1, "1.2", "1.3", "1.4", "1.5", "1.5"]),
        st(table(["viết", "nghĩa"],
                 [["<code>curl -s URL</code>", "gửi yêu cầu <b>GET</b> tới địa chỉ, in nội dung; <code>-s</code> = im lặng (bỏ thanh tiến độ)"],
                  ["<code>-i</code>", "in cả <b>dòng trạng thái và tiêu đề</b> của phản hồi"],
                  ["<code>-X POST -d a=1</code>", "đổi phương thức thành POST, gửi nội dung <code>a=1</code>"],
                  ["<code>-o /dev/null -w \"%{http_code}\"</code>", "bỏ nội dung, chỉ in <b>mã trạng thái</b>"],
                  ["<code>-f</code> và <code>--max-time 1</code>", "<code>-f</code>: gặp lỗi 4xx/5xx thì <b>thất bại</b> (mã thoát 22); <code>--max-time</code>: bỏ cuộc sau 1 giây"]]),
           """Bảng thứ hai là các cờ của lệnh gửi yêu cầu. Cờ s làm lệnh im lặng, không in thanh tiến độ. Cờ i in thêm dòng trạng thái và tiêu đề của phản hồi. Cờ X kèm cờ d đổi sang phương thức gửi và đính nội dung.
           Cờ o kèm cờ w cho bỏ nội dung và chỉ in mã trạng thái. Cờ f cho thất bại khi gặp lỗi bốn hoặc năm trăm, và cờ thời gian chờ bỏ cuộc sau một giây.""",
           focus=[1, "1.2", "1.3", "1.4", "1.5", "1.6"], clear=True),
    ])
    sc_int = sc("intuition", "intuition", "Hình dung: một vòng yêu cầu rồi phản hồi, và bốn nhóm mã", [
        st(svg(1500, 470,
               box(10, 50, 330, 120, ["máy khách", "curl, trình duyệt"], C_BLUE, bold=True),
               box(1160, 50, 330, 120, ["máy chủ", "chương trình chờ ở cổng 18765"], C_GREEN, bold=True),
               arrow(345, 80, 1155, 80, "#2a78d6", "① yêu cầu"),
               arrow(1155, 140, 345, 140, "#16a34a", "② phản hồi"),
               box(10, 220, 730, 230, ["GET /so_du HTTP/1.1", "Host: 127.0.0.1:18765", "(không có nội dung)", "", "phương thức + đường dẫn + tiêu đề (+ nội dung)"], C_BLUE),
               box(760, 220, 730, 230, ["HTTP/1.1 200 OK", "Content-Type: text/plain", "Content-Length: 7", "", "1500000  (nội dung)"], C_GREEN)),
           """Hình này là một vòng hỏi đáp. Máy khách gửi một yêu cầu, gồm phương thức, đường dẫn, các tiêu đề, và đôi khi có nội dung. Máy chủ chờ ở một cổng, nhận yêu cầu rồi gửi phản hồi.
           Phản hồi gồm dòng trạng thái có mã số, các tiêu đề, một dòng trống, rồi nội dung. Mọi thứ đều là chữ, nên ta đọc và gõ được bằng tay."""),
        st(table(["nhóm", "ý nghĩa", "ví dụ", "ai có lỗi?"],
                 [["<b>2xx</b>", "thành công", "200 OK, 201 Created", "không ai"],
                  ["<b>3xx</b>", "chuyển hướng", "301, 302", "—"],
                  ["<b>4xx</b>", "yêu cầu <b>có vấn đề</b>", "404 Not Found, 405 Method Not Allowed", "bên <b>gửi</b>"],
                  ["<b>5xx</b>", "máy chủ <b>gặp sự cố</b>", "500 Internal Server Error", "bên <b>nhận</b>"]]),
           """Bảng này là bốn nhóm mã trạng thái. Nhóm hai trăm là thành công. Nhóm ba trăm là chuyển hướng. Nhóm bốn trăm nghĩa là yêu cầu có vấn đề, lỗi ở bên gửi, ví dụ không tìm thấy hay sai phương thức.
           Nhóm năm trăm nghĩa là máy chủ gặp sự cố, lỗi ở bên nhận. Chỉ cần nhìn chữ số đầu là biết nên sửa phía nào.""",
           focus=[1, "1.2", "1.3", "1.4", "1.5", "1.5"]),
    ])
    sc_form = sc("formula", "formula", "Suy ra từng bước: đọc một phản hồi để quyết định làm gì", [
        st(term_block(h, 4, 5, title="Bước 1. Đọc dòng đầu: nhóm của mã")
           + "<p>Vì chữ số đầu của <code>200</code> là $2$, đây là nhóm <b>thành công</b>; nên nội dung <code>1500000</code> dùng được.</p>",
           """Bước một, đọc dòng đầu của phản hồi. Vì chữ số đầu của hai trăm là hai, đây là nhóm thành công, nên nội dung một triệu năm trăm nghìn dùng được."""),
        st(term_block(h, 8, 10, title="Bước 2. Cùng đường dẫn /chuyen, hai phương thức, hai kết quả")
           + "<p>Vì đường dẫn <code>/chuyen</code> chỉ <b>nhận POST</b>, gửi POST ra <code>201</code> (đã tạo), còn GET ra <code>405</code>: nhóm $4$, <b>lỗi của bên gửi</b>.</p>",
           """Bước hai, cùng một đường dẫn mà hai phương thức cho hai kết quả. Vì đường dẫn chuyển chỉ nhận phương thức gửi, nên gửi thì ra hai trăm linh một, tức đã tạo. Còn phương thức đọc ra bốn trăm linh năm, nhóm bốn, lỗi của bên gửi."""),
        st(table(["mã", "nhóm", "ai có lỗi", "thử lại ngay có ích không?"],
                 [["200, 201", "2xx", "không", "không cần"], ["404, 405", "4xx", "bên gửi", "<b>không</b>: sửa yêu cầu trước"],
                  ["500", "5xx", "bên nhận", "đọc (GET): có thể, ghi (POST): <b>cẩn thận</b>"]])
           + "<p>Bước 3: nhóm quyết định hành động; nhóm 4xx thì sửa yêu cầu, nhóm 5xx thì cân nhắc thử lại.</p>",
           """Bước ba, nhóm của mã quyết định hành động. Mã nhóm hai không cần làm gì thêm. Mã nhóm bốn thì thử lại ngay vô ích, vì lỗi ở yêu cầu, phải sửa yêu cầu trước.
           Mã nhóm năm là lỗi của máy chủ, nên đọc thì thử lại được, còn ghi thì phải cẩn thận, vì có thể đã ghi một nửa.""", clear=True),
    ], checks=["200 // 100 == 2", "404 // 100 == 4 and 405 // 100 == 4", "500 // 100 == 5", "201 // 100 == 2"])
    sc_ex = sc("example", "example", "Ví dụ: một phiên hỏi máy chủ, năm phép làm", [
        st(term_block(h, 0, 4, title="① Khởi động máy chủ ở nền, rồi hỏi trang chủ")
           + "<p><code>may_chu.py</code> là máy chủ nhỏ cho sẵn (chạy cục bộ, cổng $18765$). Trả lời <code>xin chao</code> mà <b>không xuống dòng</b>.</p>",
           """Phép làm thứ nhất, khởi động máy chủ ở nền, chờ một giây cho nó sẵn sàng, đặt địa chỉ vào một biến, rồi hỏi trang chủ. Máy chủ trả lời xin chào, và lệnh gửi yêu cầu không thêm ký tự xuống dòng, nên dấu nhắc có thể dính ngay sau chữ."""),
        st(term_block(h, 4, 5, title="② Đọc cả phản hồi bằng -i")
           + "<p>$1$ dòng trạng thái, $2$ tiêu đề, $1$ dòng trống, rồi nội dung $7$ ký tự: <code>Content-Length: 7</code> khớp <code>1500000</code> ✓</p>",
           """Phép làm thứ hai, đọc cả phản hồi bằng cờ i. Có một dòng trạng thái, hai tiêu đề, một dòng trống, rồi nội dung. Tiêu đề độ dài nói bảy, và chuỗi một triệu năm trăm nghìn đúng là bảy ký tự."""),
        st(term_block(h, 5, 8, title="③ Địa chỉ không tồn tại: 404, nhưng curl vẫn báo thành công")
           + "<p>Mặc định, <code>curl</code> chỉ báo lỗi khi <b>không nối được</b>; nhận <code>404</code> vẫn là “đã nhận được trả lời”, mã thoát <code>0</code>. Thêm <code>-f</code>: mã thoát <code>22</code>.</p>",
           """Phép làm thứ ba, gọi một địa chỉ không tồn tại. Máy chủ trả bốn trăm linh bốn. Lệnh gửi yêu cầu mặc định chỉ báo lỗi khi không nối được, nên nhận bốn trăm linh bốn vẫn là đã nhận được trả lời, và mã thoát bằng không.
           Thêm cờ f thì gặp lỗi bốn hoặc năm trăm sẽ thất bại, với mã thoát hai mươi hai."""),
        st(term_block(h, 8, 10, title="④ Phương thức gửi, rồi sai phương thức")
           + "<p>POST <code>/chuyen</code> → $201$ (đã tạo); GET cùng đường dẫn → $405$.</p>",
           """Phép làm thứ tư, hai mã khác nhau cho cùng một đường dẫn. Gửi dữ liệu bằng phương thức gửi ra hai trăm linh một. Gọi đường dẫn đó bằng phương thức đọc ra bốn trăm linh năm.""", clear=True),
        st(term_block(h, 10, 11, title="④ Sự cố ở máy chủ")
           + "<p><code>/loi</code> → $500$ (nhóm $5$: lỗi ở máy chủ).</p>",
           """Và đường dẫn lỗi cố ý ra năm trăm, vì máy chủ gặp sự cố.""", clear=True),
        st(term_block(h, 11, 14, title="⑤ Mã 200 chưa chắc là việc đã đúng; và đừng chờ vô hạn")
           + "<p>Trang <code>/het_han</code> trả <code>200</code> nhưng nội dung nói <b>lỗi</b>; trang <code>/cham</code> chậm: <code>--max-time 1</code> bỏ cuộc, mã thoát $28$.</p>",
           """Phép làm thứ năm, hai bẫy thật. Một trang trả hai trăm, nhưng nội dung nói hết hạn, tức mã trạng thái chưa nói hết sự thật, phải đọc cả nội dung. Một trang rất chậm, và cờ thời gian chờ giúp ta bỏ cuộc sau một giây, mã thoát hai mươi tám.""", clear=True),
    ], checks=["len('1500000') == 7", "1 + 2 + 1 + 7 >= 7", "404 // 100 == 4", "22 != 0", "28 != 0"])
    sc_chk = sc("check", "check", "Tự kiểm bằng đường khác: mã trạng thái và nội dung phải cùng nói một điều", [
        st(term_block(h, 5, 6, title="Cách 1: chỉ in mã (-w)") + term_block(h, 3, 4, title="Cách 2: đọc dòng đầu của -i ở trên"),
           """Đường kiểm khác, hỏi cùng một việc bằng hai cách. Cách một in riêng mã trạng thái bằng cờ w. Cách hai đọc dòng đầu của phản hồi đầy đủ ở phép làm thứ hai. Hai cách phải cho cùng mã cho cùng địa chỉ, vì cùng hỏi một việc."""),
        st(term_block(h, 11, 13, title="Kiểm cả mã VÀ nội dung")
           + "<p>Mã $200$ và nội dung <code>{\"loi\": \"het han\"}</code>: <b>không khớp ý nghĩa</b>, nên coi là thất bại. Khi viết chương trình gọi máy chủ, kiểm <b>cả hai</b>.</p>",
           """Kiểm cuối, nhìn cả mã lẫn nội dung của trang hết hạn. Mã hai trăm nhưng nội dung báo lỗi, nên ý nghĩa không khớp, và ta coi đó là thất bại. Khi viết chương trình gọi máy chủ, hãy kiểm cả hai."""),
    ], checks=["200 // 100 == 2"])
    sc_scale = sc("scale", "example", "Khi yêu cầu nhân lên: cần bao nhiêu người phục vụ cùng lúc?", [
        st("""<p>Giả sử mỗi yêu cầu mất $20$ mili giây để xử lý (số minh hoạ). Một “người phục vụ” (một luồng) làm lần lượt: $1 / 0{,}02 = \\hl{50}$ yêu cầu mỗi giây.</p>
$$\\text{số người phục vụ cần} = \\text{số yêu cầu mỗi giây} \\times \\text{thời gian một yêu cầu}$$
<span class='note'>Quan hệ này là định luật hàng đợi của J. D. C. Little (1961), áp dụng cho mọi hàng đợi ổn định.</span>""",
           """Giả sử mỗi yêu cầu mất hai mươi phần nghìn giây để xử lý, đây là số minh hoạ. Một người phục vụ làm lần lượt, nên làm được một chia không phẩy không hai, tức năm mươi yêu cầu mỗi giây. Số người phục vụ cần bằng số yêu cầu mỗi giây nhân thời gian một yêu cầu.
           Quan hệ này là một định luật về hàng đợi, đúng cho mọi hàng đợi ổn định."""),
        st(table(["yêu cầu mỗi giây", "tính", "người phục vụ cùng lúc"],
                 [["×1: 50", "$50 \\times 0{,}02$", "<b>1</b>"], ["×100: 5 000", "$5\\,000 \\times 0{,}02$", "<b>100</b>"], ["×10 000: 500 000", "$500\\,000 \\times 0{,}02$", "<b>10 000</b>"]])
           + "<div class='box key'><b>Đánh đổi:</b> máy chủ một luồng như <code>may_chu.py</code> chỉ hợp để học (50 yêu cầu mỗi giây). "
             "Ở quy mô lớn phải chạy <b>nhiều tiến trình/luồng</b>, đặt <b>thời gian chờ</b> cho mọi cuộc gọi, và xếp hàng thay vì để yêu cầu tràn. Mỗi “người phục vụ” cũng tốn bộ nhớ.</div>",
           """Bảng này cho thấy quy mô. Năm mươi yêu cầu mỗi giây cần một người phục vụ. Năm nghìn yêu cầu mỗi giây cần một trăm người. Năm trăm nghìn yêu cầu mỗi giây cần mười nghìn người phục vụ cùng lúc.
           Máy chủ một luồng chỉ hợp để học. Ở quy mô lớn phải chạy nhiều tiến trình, đặt thời gian chờ cho mọi cuộc gọi, và xếp hàng thay vì để yêu cầu tràn, vì mỗi người phục vụ cũng tốn bộ nhớ."""),
    ], checks=["round(1 / 0.02) == 50", "50 * 0.02 == 1.0", "round(5000 * 0.02) == 100", "round(500000 * 0.02) == 10000", "5000 // 50 == 100"])
    sc_pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st('<div class="box warn"><b>Lỗi 1 (người mới).</b> Tin <code>curl</code> “im lặng và mã thoát 0” nghĩa là thành công.</div>'
           + term_block(h, 6, 8) + "<p>Phép thử: thêm <code>-f</code>, hoặc in mã bằng <code>-w '%{http_code}'</code> rồi so với $200$.</p>",
           """Lỗi thứ nhất, của người mới, là tin rằng im lặng và mã thoát bằng không nghĩa là thành công. Gặp bốn trăm linh bốn, lệnh vẫn in nội dung và trả mã không. Phép thử là thêm cờ f, hoặc in mã trạng thái bằng cờ w rồi so với hai trăm."""),
        st('<div class="box warn"><b>Lỗi 2 (người mới).</b> Dùng sai phương thức: gọi bằng GET một đường dẫn chỉ nhận POST.</div>'
           + term_block(h, 9, 10) + "<p>Nhóm $4$ nghĩa là lỗi ở yêu cầu của bạn; thử lại y nguyên sẽ <b>luôn</b> cho cùng kết quả, mỗi lần trả thêm tải cho máy chủ.</p>",
           """Lỗi thứ hai, cũng của người mới, là dùng sai phương thức. Gọi bằng phương thức đọc một đường dẫn chỉ nhận phương thức gửi thì nhận bốn trăm linh năm. Nhóm bốn nghĩa là lỗi ở yêu cầu của bạn, nên thử lại y nguyên vẫn ra kết quả cũ."""),
        st('<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> Không đặt thời gian chờ, hoặc thử lại mù quáng một yêu cầu <b>ghi</b>.</div>'
           + term_block(h, 13, 14) + "<p>Quá hạn không có nghĩa máy chủ <b>chưa</b> làm: yêu cầu POST có thể đã được xử lý. Thử lại POST khi chưa kiểm tra có thể làm <b>hai lần</b> (ví dụ trừ tiền hai lần).</p>",
           """Lỗi thứ ba, của cả người đã đi làm, là hai việc. Một là không đặt thời gian chờ, nên chương trình treo vô hạn khi máy chủ chậm. Hai là thử lại mù quáng một yêu cầu ghi. Quá hạn không có nghĩa máy chủ chưa làm, yêu cầu có thể đã được xử lý.
           Thử lại khi chưa kiểm tra có thể làm hai lần, ví dụ trừ tiền hai lần. Người làm nghề hỏi trạng thái trước, hoặc thiết kế để làm hai lần cũng như một lần."""),
    ])
    sc_quiz = sc("quiz", "quiz", "Bây giờ tới phần bạn tự làm", [
        st("""<p><b>Đề.</b> Chương trình thanh toán của bạn gọi máy chủ và nhận các kết quả sau. Với mỗi dòng, <b>chọn</b>: thử lại hay không, và vì sao?</p>
<ol><li><code>GET /so_du</code> trả <code>500</code></li><li><code>GET /so_du_sai</code> trả <code>404</code></li>
<li><code>POST /chuyen</code> (chuyển 1 000 000 đồng) quá <b>thời gian chờ</b>, không nhận được gì</li></ol>""",
           """Bây giờ tới phần bạn tự làm. Chương trình thanh toán gọi máy chủ và nhận ba kết quả. Một, đọc số dư và nhận năm trăm. Hai, đọc một đường dẫn sai và nhận bốn trăm linh bốn. Ba, gửi lệnh chuyển một triệu đồng, và quá thời gian chờ mà không nhận được gì.
           Với mỗi kết quả, hãy chọn thử lại hay không, và vì sao. Hãy dừng video và làm.""", pause=60),
        st(table(["kết quả", "thử lại?", "lý do"],
                 [["1. GET trả 500", "<b>có</b>, vài lần, giãn dần khoảng cách", "đọc không đổi dữ liệu; lỗi 5xx có thể là tạm thời"],
                  ["2. GET trả 404", "<b>không</b>", "nhóm 4xx: yêu cầu sai; thử lại cho cùng kết quả, phải sửa đường dẫn"],
                  ["3. POST quá hạn", "<b>không thử mù</b>", "không biết máy chủ đã chuyển tiền chưa; <b>hỏi trạng thái</b> trước, hoặc gửi kèm mã chống lặp"]]),
           """Đáp án một, đọc mà nhận năm trăm thì nên thử lại vài lần, giãn dần khoảng cách, vì đọc không đổi dữ liệu và lỗi năm trăm có thể là tạm thời. Hai, bốn trăm linh bốn thì không thử lại, vì yêu cầu sai, phải sửa đường dẫn.
           Ba, gửi lệnh chuyển tiền quá hạn thì không thử lại mù quáng, vì không biết máy chủ đã chuyển chưa. Phải hỏi trạng thái trước, hoặc gửi kèm một mã chống lặp.""",
           focus=["1.2", "1.3", "1.4", "1.4"]),
        st(term_block(h, 10, 11) + term_block(h, 5, 6)
           + "<div class='box key'><b>Quyết định:</b> nhóm của mã và <b>phương thức</b> cùng quyết định có thử lại không. 5xx + đọc: thử lại; 4xx: sửa; ghi mà không chắc kết quả: <b>kiểm tra trạng thái</b>, không thử mù.</div>",
           """Máy chạy lại hai trường hợp đầu cho đúng mã mô tả. Quyết định nằm ở hai thứ cùng nhau, nhóm của mã và phương thức. Lỗi năm trăm mà đọc thì thử lại, lỗi bốn trăm thì sửa, còn ghi mà không chắc kết quả thì kiểm tra trạng thái, không thử mù.""", clear=True),
    ], checks=["500 // 100 == 5", "404 // 100 == 4"])
    sc_prac = practice_scene(sc, "Tự làm: khởi động máy chủ lab và hỏi bốn câu", pr_steps(
        st, "FND", "L07",
        """<p><b>Đề</b>: tạo <code>http.sh</code>. Dòng đầu chép nguyên đoạn khởi động máy chủ lab (xem <code>de.md</code>: tạo <code>may_chu.py</code>, chạy ở nền cổng $18766$, chờ sẵn sàng, đặt biến <code>U</code>). Rồi viết <b>bốn lệnh <code>curl</code></b> và cuối cùng <code>kill $SV</code>:</p>
<ol><li>in <b>mã</b> của <code>GET $U/chao</code>;</li><li>in <b>mã</b> của <code>GET $U/khong_co</code>;</li>
<li>in <b>nội dung</b> của <code>GET $U/tai_khoan/42</code> (nhớ xuống dòng);</li><li>in <b>mã</b> của <code>POST $U/nap</code> với nội dung <code>so_tien=100000</code>.</li></ol>""".replace("$18766$", "18766").replace("kill $SV", "kill <span>&#36;</span>SV").replace("$U", "<span>&#36;</span>U"),
        """Bây giờ tới phần bạn tự làm. Tạo một tệp lệnh. Chép nguyên đoạn khởi động máy chủ của bài thực hành, nó chạy ở nền và đặt một biến địa chỉ. Rồi viết bốn lệnh gửi yêu cầu. Một, in mã của một đường dẫn có thật. Hai, in mã của một đường dẫn không có.
        Ba, in nội dung của đường dẫn tài khoản bốn mươi hai. Bốn, gửi phương thức gửi tới đường dẫn nạp và in mã. Cuối cùng dừng máy chủ. Hãy dừng video và làm.""",
        LAB_OUT, "http.sh",
        """<div class="box key"><b>Nếu kẹt:</b> in mã: <code>curl -s -o /dev/null -w "%{http_code}\\n" URL</code>. In nội dung: <code>curl -s URL; echo</code>. POST: thêm <code>-X POST -d so_tien=100000</code>.
Lời giải ở <code>labs/FND/L07/loi_giai.sh</code>.</div>""".replace("\\n", "<span>&#92;</span>n"),
        """Nếu kẹt, để in mã thì dùng cờ bỏ nội dung kèm cờ in mã trạng thái. Để in nội dung thì không cần cờ nào, rồi thêm một lệnh in chữ để xuống dòng. Phương thức gửi thì thêm hai cờ, đổi phương thức và đính nội dung.
        Lời giải nằm trong thư mục thực hành, chỉ mở sau khi đã thử.""", pause=300), "FND", "L07")
    write_lab("FND", "L07", """# Lab FND L07 — Hỏi một máy chủ cục bộ bằng curl

Tạo `http.sh`. **Dòng đầu chép nguyên** (tạo máy chủ nhỏ `may_chu.py`, chạy ở nền cổng 18766, chờ nó sẵn sàng, đặt biến `U`):

```bash
""" + LAB_START + """
```

Rồi viết bốn lệnh `curl -s …` (mỗi lệnh in một dòng) và cuối cùng `kill $SV`:
1. **mã trạng thái** của `GET $U/chao`;
2. **mã trạng thái** của `GET $U/khong_co`;
3. **nội dung** của `GET $U/tai_khoan/42` (thêm `echo` để xuống dòng);
4. **mã trạng thái** của `POST $U/nap` với nội dung `so_tien=100000`.

Gợi ý lấy mã: `curl -s -o /dev/null -w "%{http_code}\\n" URL`. Chạy `bash http.sh`; chấm: `bash labs/cham.sh FND L07 http.sh`. Cần Python và curl (có sẵn trong Git Bash). Cổng 18766 phải trống.
""", "sh", LAB_START + "\n" + LAB_BODY, LAB_OUT)
    sc_rec = sc("recap", "recap", "Chuỗi logic và tư duy cần mang theo", [
        st(chain("máy khách hỏi, máy chủ đáp", "yêu cầu: phương thức + đường dẫn + tiêu đề", "phản hồi: mã + tiêu đề + nội dung",
                 "2xx tốt, 4xx lỗi bên gửi, 5xx lỗi bên nhận", "curl -f, -w, --max-time", "đọc thử lại được, ghi thì kiểm trạng thái trước"),
           """Tổng kết chuỗi logic. Máy khách là bên đặt câu hỏi, còn máy chủ là bên trả lời. Yêu cầu có phương thức, đường dẫn, tiêu đề. Phản hồi có mã, tiêu đề, nội dung. Nhóm hai trăm là tốt, bốn trăm là lỗi bên gửi, năm trăm là lỗi bên nhận.
           Lệnh gửi yêu cầu có cờ f, cờ w và cờ thời gian chờ. Đọc thì thử lại được, ghi thì kiểm tra trạng thái trước."""),
        st("""<div class='box key'><b>Tư duy:</b> đừng tin một con số: đọc <b>mã, nội dung, thời gian</b> cùng nhau; và với việc ghi, hỏi “nếu chạy hai lần thì sao?”.</div>
<p>Bài sau: viết câu SQL đầu tiên để hỏi một cái bảng, và biết vì sao “ghi hai lần” cần giao dịch.</p>""",
           """Điều cần mang theo, đừng tin một con số. Hãy đọc mã, nội dung và thời gian cùng nhau, và với việc ghi, hãy hỏi nếu chạy hai lần thì sao.
           Bài sau, ta viết câu SQL đầu tiên để hỏi một cái bảng, và biết vì sao ghi hai lần cần đến giao dịch.""", forward_ref=True),
    ])
    return lesson("L07", "http_va_curl", "Bài 7 — Máy khách, máy chủ và HTTP: hỏi một máy chủ bằng curl",
                  "curl.se (curl man page: -s -i -X -d -o -w -f --max-time, mã thoát 22 và 28); audit/fnd/verify_fnd.py L07 (máy chủ http.server của Python 3 chạy cục bộ, curl chạy thật); "
                  "RFC 9110 (HTTP Semantics: phương thức, mã trạng thái 2xx/4xx/5xx; GET an toàn và idempotent, POST thì không); "
                  "Little, J.D.C. 1961, A Proof for the Queuing Formula L = λW, Operations Research 9(3) (NOT_VERIFIED: trích theo trí nhớ); số 20 mili giây là số minh hoạ",
                  ["Nêu các phần của một yêu cầu và một phản hồi HTTP",
                   "Đọc mã trạng thái 2xx, 4xx, 5xx và chọn hành động tương ứng",
                   "Chạy curl tới máy chủ cục bộ: đọc, gửi dữ liệu, in riêng mã trạng thái",
                   "Kiểm một câu trả lời bằng hai cách và bằng cả mã lẫn nội dung",
                   "Tính số người phục vụ cần cùng lúc khi số yêu cầu nhân lên",
                   "Chỉ ra ba lỗi hay gặp: curl mã thoát 0 khi gặp 404, sai phương thức, không đặt thời gian chờ và thử lại mù",
                   "Nêu vì sao thử lại hay không cho từng kết quả",
                   "Viết tệp lệnh hỏi máy chủ lab và in đúng bốn kết quả"],
                  [sc_hook, sc_pre, sc_sym, sc_int, sc_form, sc_ex, sc_chk, sc_scale, sc_pit, sc_quiz, sc_prac, sc_rec],
                  covers=[(1, "intuition"), (2, "formula"), (3, "example"), (4, "check"), (5, "scale"), (6, "pitfalls"), (7, "quiz"), (8, "practice")])
