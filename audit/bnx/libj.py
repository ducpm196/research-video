"""Khuôn bảng 'viết trong mã -> đọc là -> ví dụ' dùng chung cho BNX L13-L25 (fix6 BNX_B, R4 P1 chặt): Java, Python nền, YAML, shell.
Bài tự đứng được: mỗi bài nêu đúng token bài đó dùng (<= 4 hàng mỗi step), nhắc lại một dòng ở bài dùng lại.
Dùng:  from libj import jstep, JROW, nowrap
    jstep([("for", "<code>for (int i = 1; i <= 10; i++)</code>: i chạy từ 1 tới 10", "biến đếm i chạy từ một tới mười"), ...])
Mục tự khai (token riêng của bài): thay khoá bằng bộ ba (mã_html, đọc_là_html, đọc_là_lời).
Lời đọc KHÔNG chứa chữ Latin (lexicon): mô tả bằng tiếng Việt. Chỉ THÊM mới, không đổi đầu ra của bài khác (tệp mới, không đụng lib.py/lib2.py)."""
import lib2


def nowrap(s):
    """Ô bảng không ngắt dòng giữa số (vd '10 000 (×10 000)')."""
    return f"<span style='white-space:nowrap'>{s}</span>"


JHEAD = ["viết trong mã", "đọc là", "ví dụ"]
JROW = {
    # ── Java ──
    "class": ("<code>public class Ten { … }</code>",
              "khai một <b>lớp</b>: khối chứa các hàm và dữ liệu của chương trình; <code>public</code>: nơi khác dùng được; phần thân nằm giữa cặp ngoặc nhọn",
              "Khai một lớp là mở khối chứa các hàm và dữ liệu của chương trình, công khai nghĩa là nơi khác dùng được, phần thân nằm giữa cặp ngoặc nhọn."),
    "main": ("<code>public static void main(String[] a)</code>",
             "hàm máy chạy đầu tiên khi mở chương trình; <code>String[] a</code>: mảng chuỗi gõ kèm lúc chạy, bài này không dùng",
             "Hàm chính là chỗ máy bắt đầu chạy chương trình, còn tham số là mảng chuỗi gõ kèm lúc chạy, bài này không dùng đến."),
    "sig": ("<code>public static kiểu tên(kiểu a, kiểu b)</code>",
            "khai một hàm: <b>kiểu trả về</b> (<code>void</code> là không trả gì), <b>tên</b>, rồi <b>tham số</b> trong ngoặc tròn, mỗi tham số là kiểu rồi tên; <code>static</code>: thuộc cả lớp",
            "Khai một hàm gồm kiểu giá trị trả về, rỗng nghĩa là không trả gì, rồi tên hàm, rồi các tham số trong ngoặc tròn, mỗi tham số là kiểu rồi tên."),
    "throws": ("<code>… throws Lỗi {</code>",
               "lời báo: hàm này có thể ném lỗi loại đó; ai gọi hàm phải bắt lỗi hoặc khai báo tiếp",
               "Lời báo ném lỗi nghĩa là hàm có thể ném lỗi loại đó, và ai gọi hàm phải bắt lỗi hoặc khai báo tiếp."),
    "for": ("<code>for (int i = 1; i &lt;= 10; i++) { … }</code>",
            "vòng lặp đếm: khai biến đếm; điều kiện để còn lặp; bước sau mỗi vòng (<code>i++</code>: tăng i thêm 1); thân giữa cặp ngoặc nhọn",
            "Vòng lặp đếm có ba phần cách nhau bằng chấm phẩy: khai biến đếm, điều kiện để còn lặp, và bước sau mỗi vòng, trong đó hai dấu cộng nghĩa là tăng thêm một."),
    "foreach": ("<code>for (long x : ca) { … }</code>",
                "duyệt từng phần tử: mỗi vòng <code>x</code> nhận một phần tử của <code>ca</code>, theo thứ tự",
                "Dấu hai chấm trong vòng lặp nghĩa là duyệt từng phần tử, mỗi vòng biến nhận một phần tử của dãy, theo thứ tự."),
    "decl": ("<code>int so = i;</code>, <code>long t0</code>, <code>boolean ok</code>, <code>String s</code>",
             "khai biến: <b>kiểu</b> rồi tên, rồi <code>=</code> giá trị; <code>int</code>: số nguyên, <code>long</code>: số nguyên lớn, <code>boolean</code>: đúng hoặc sai, <code>String</code>: chuỗi chữ",
             "Khai biến là viết kiểu rồi tên, rồi dấu bằng và giá trị; có kiểu số nguyên, số nguyên lớn, đúng sai, và chuỗi chữ."),
    "new": ("<code>new Kiểu(…)</code>, <code>new int[] {3, 4}</code>",
            "<code>new</code>: tạo mới; <code>new Kiểu(…)</code> tạo một đối tượng; <code>new int[] {3, 4}</code> tạo mảng số nguyên với các giá trị liệt kê; <code>&lt;&gt;</code> để trống thì lấy kiểu ở vế trái",
            "Chữ tạo mới tạo một đối tượng, hoặc một mảng với các giá trị liệt kê trong ngoặc nhọn; cặp ngoặc nhọn nhỏ để trống nghĩa là lấy kiểu từ vế trái."),
    "print": ("<code>System.out.println(\"n = \" + n);</code>",
              "in một dòng ra màn hình; dấu <code>+</code> giữa chuỗi và số nối chúng thành một chuỗi",
              "Lệnh này in một dòng ra màn hình, và dấu cộng giữa chuỗi và số nối chúng thành một chuỗi."),
    "div": ("<code>(10 + 4 - 1) / 4</code>, <code>i % 3</code>",
            "chia hai số nguyên thì <b>bỏ phần lẻ</b> (<code>7 / 2</code> ra 3); <code>%</code>: phần dư (<code>7 % 2</code> ra 1)",
            "Chia hai số nguyên thì bỏ phần lẻ, bảy chia hai ra ba, còn dấu phần trăm cho phần dư, bảy chia hai dư một."),
    "ctor": ("<code>ChiaDoi(int tu, int den) { this.tu = tu; … }</code>",
             "<b>hàm tạo</b>: cùng tên lớp, không có kiểu trả về, chạy khi <code>new</code>; <code>this.tu = tu</code>: chép tham số vào trường của chính đối tượng này",
             "Hàm tạo cùng tên với lớp, không có kiểu trả về, và chạy khi tạo mới; câu gán có chữ chính nó chép tham số vào trường của đối tượng này."),
    "fld": ("<code>static final int NGUONG = 1000;</code>, <code>final int tu, den;</code>",
            "<code>final</code>: gán giá trị một lần rồi không đổi; <code>static</code>: một bản chung cho cả lớp, không có thì mỗi đối tượng một bản riêng",
            "Chữ cuối cùng nghĩa là gán một lần rồi không đổi, còn chữ tĩnh nghĩa là một bản chung cho cả lớp, không có thì mỗi đối tượng giữ một bản riêng."),
    "try": ("<code>try { … } catch (Lỗi e) { … } finally { … }</code>",
            "thử chạy khối <code>try</code>; lỗi loại đó thì nhảy sang <code>catch</code>; <code>finally</code> luôn chạy sau cùng, có lỗi hay không",
            "Khối thử chạy trước, nếu có lỗi loại đã nêu thì nhảy sang khối bắt lỗi, còn khối cuối cùng luôn chạy sau cùng, dù có lỗi hay không."),
    "throw": ("<code>throw new IllegalStateException(\"…\");</code>",
              "ném lỗi: tạo một đối tượng lỗi mới rồi ném đi; việc đang làm dừng, nhảy tới nơi bắt lỗi",
              "Câu này tạo một đối tượng lỗi rồi ném đi, việc đang làm dừng lại và nhảy tới nơi bắt lỗi."),
    "lambda": ("<code>() -&gt; { … }</code>, <code>x -&gt; x + 1</code>",
               "hàm ngắn không tên: bên trái mũi tên là tham số, bên phải là việc làm; <code>()</code>: không tham số",
               "Hàm ngắn không tên có tham số ở bên trái mũi tên và việc làm ở bên phải; cặp ngoặc tròn rỗng nghĩa là không có tham số."),
    "mref": ("<code>Ban::khoe</code>, <code>Integer::sum</code>",
             "viết gọn tên một hàm có sẵn; <code>Ban::khoe</code> nghĩa là <code>b -&gt; b.khoe()</code>",
             "Hai dấu hai chấm là cách viết gọn tên một hàm có sẵn, thay cho hàm ngắn gọi đúng hàm đó."),
    "record": ("<code>record Ban(String ten, boolean khoe)</code>",
               "lớp dữ liệu gọn: khai tên các trường, Java tự có hàm tạo và hàm đọc cùng tên (<code>b.ten()</code>)",
               "Lớp dữ liệu gọn chỉ cần khai các trường, Java tự sinh hàm tạo và hàm đọc cùng tên với trường."),
    "impl": ("<code>class A implements Filter</code>",
             "lớp A cam kết có đủ các hàm mà <b>giao diện</b> <code>Filter</code> (bản liệt kê tên hàm phải có) yêu cầu",
             "Lớp cam kết có đủ các hàm mà giao diện yêu cầu, giao diện là bản liệt kê tên các hàm phải có."),
    "gen": ("<code>List&lt;TaiKhoan&gt;</code>, <code>Map&lt;String, Integer&gt;</code>",
            "kiểu chứa: giữa cặp ngoặc nhọn nhỏ là kiểu phần tử; danh sách các TaiKhoan; bảng tra có khoá là chuỗi, giá trị là số nguyên",
            "Giữa cặp ngoặc nhọn nhỏ là kiểu của phần tử: danh sách các tài khoản, hoặc bảng tra có khoá là chuỗi và giá trị là số nguyên."),
    "annot": ("<code>@Id</code>, <code>@OneToMany(…)</code>",
              "chú thích bắt đầu bằng <code>@</code>: dán nhãn cho trường hay lớp ngay sau nó để thư viện đọc; không tự chạy gì",
              "Chú thích bắt đầu bằng dấu a còng, dán nhãn cho trường hay lớp ngay sau nó để thư viện đọc, và tự nó không chạy gì."),
    "ifelse": ("<code>if (đk) a(); else b();</code>",
               "nếu điều kiện đúng thì làm câu sau <code>if</code>, ngược lại làm câu sau <code>else</code>",
               "Nếu điều kiện đúng thì làm câu đứng ngay sau, ngược lại làm câu sau từ khoá còn lại."),
    "incr": ("<code>dem++;</code>, <code>x += y;</code>",
             "<code>dem++</code>: tăng thêm 1; <code>x += y</code>: cộng y vào x; <code>&amp;=</code>: giữ đúng chỉ khi cả hai vế cùng đúng",
             "Hai dấu cộng tăng biến thêm một, dấu cộng bằng cộng một giá trị vào biến."),
    "eqeq": ("<code>a == b</code>",
             "với đối tượng: hỏi a và b có phải <b>cùng một đối tượng</b> trong bộ nhớ không, chứ không hỏi nội dung có giống nhau",
             "Hai dấu bằng giữa hai đối tượng hỏi chúng có phải cùng một đối tượng trong bộ nhớ, chứ không hỏi nội dung có giống nhau."),
    "pkg": ("<code>package com.vidu.site;</code>, <code>private String ten;</code>",
            "<code>package</code>: tên thư mục chứa lớp; <code>private</code>: chỉ mã trong lớp này dùng được; giá trị đọc ra qua hàm <code>getTen()</code>",
            "Câu gói ghi lớp nằm ở thư mục nào, chữ riêng tư nghĩa là chỉ mã trong lớp này dùng được trường đó."),
    "impstatic": ("<code>import static … .assertEquals;</code>",
                  "nhập sẵn một hàm tĩnh để gọi bằng tên ngắn, khỏi viết tên lớp phía trước",
                  "Câu nhập tĩnh lấy sẵn một hàm để gọi bằng tên ngắn, khỏi viết tên lớp phía trước."),
    "cast": ("<code>(Kiểu) giá_trị</code>",
             "ép kiểu: bảo máy coi giá trị đứng sau là kiểu ghi trong ngoặc tròn",
             "Ép kiểu là bảo máy coi giá trị đứng sau thuộc kiểu ghi trong ngoặc tròn đứng trước nó."),
    "idx": ("<code>a[i]</code>, <code>a.length</code>",
            "<code>a[i]</code>: ô thứ i của mảng a, ô đầu là <code>a[0]</code>; <code>a.length</code>: số ô của mảng, không có ngoặc tròn",
            "Chỉ số trong ngoặc vuông chọn một ô của mảng, ô đầu có chỉ số không, và chấm độ dài cho biết số ô của mảng."),
    "call": ("<code>hàm(a, b)</code>, <code>s.length()</code>",
             "gọi một hàm: các giá trị trong ngoặc tròn là đối số; <code>s.length()</code> cho số ký tự của chuỗi s",
             "Gọi một hàm thì các giá trị trong ngoặc tròn là đối số, và chấm độ dài kèm ngoặc tròn cho số ký tự của chuỗi."),
    # ── Python nền ──
    "pdef": ("<code>def ten(a, b):</code> … <code>return x</code>",
             "khai một hàm: <code>def</code>, tên, tham số trong ngoặc tròn, dấu hai chấm; các dòng thụt vào là thân hàm; <code>return</code> trả giá trị về chỗ gọi",
             "Khai hàm Python gồm chữ khai hàm, tên, tham số và dấu hai chấm; các dòng thụt vào là thân hàm, và lệnh trả về đưa giá trị về chỗ gọi."),
    "pfor": ("<code>for x in (1, 2, 3):</code>",
             "vòng lặp: mỗi vòng <code>x</code> nhận một giá trị trong dãy, theo thứ tự; các dòng thụt vào là thân vòng",
             "Vòng lặp Python cho biến nhận lần lượt từng giá trị trong dãy, và các dòng thụt vào là thân vòng."),
    "pwhile": ("<code>while đk:</code>, <code>j += 1</code>",
               "lặp lại thân vòng chừng nào điều kiện còn đúng; <code>j += 1</code>: cộng 1 vào j",
               "Vòng lặp có điều kiện lặp lại thân vòng chừng nào điều kiện còn đúng, và dấu cộng bằng cộng một giá trị vào biến."),
    "pslice": ("<code>s[:16]</code>, <code>s[a:b]</code>, <code>p[-1]</code>, <code>p[:-1]</code>",
               "cắt lát: <code>s[:16]</code> là 16 phần tử đầu; <code>s[a:b]</code> từ vị trí a tới trước b; <code>p[-1]</code> phần tử cuối; <code>p[:-1]</code> mọi phần tử trừ cuối",
               "Cắt lát lấy một đoạn của dãy: số đầu là vị trí bắt đầu, số sau là vị trí dừng không lấy; số âm đếm từ cuối về."),
    "pcond": ("<code>a if đk else b</code>",
              "biểu thức điều kiện: giá trị là a nếu điều kiện đúng, ngược lại là b",
              "Biểu thức điều kiện cho giá trị thứ nhất nếu điều kiện đúng, ngược lại cho giá trị sau cùng."),
    "pcomp": ("<code>[f(x) for x in xs]</code>",
              "<b>danh sách sinh sẵn</b>: lặp từng x trong xs, tính f(x), gom kết quả vào một danh sách; thêm <code>if</code> ở cuối thì chỉ lấy x thoả điều kiện",
              "Danh sách sinh sẵn lặp từng phần tử, tính một biểu thức rồi gom kết quả vào danh sách; thêm điều kiện ở cuối thì chỉ lấy phần tử thoả."),
    "pimp": ("<code>from m import x as y</code>",
             "lấy tên x từ thư viện m về dùng, và gọi nó là y trong mã này",
             "Câu nhập lấy một tên từ thư viện về dùng, và chữ gọi là đổi tên ngắn gọn hơn."),
    "pf": ("<code>f\"n = {x}\"</code>",
           "chuỗi f: phần trong ngoặc nhọn được thay bằng giá trị của biểu thức; <code>{x:.1e}</code> in dạng khoa học một chữ số thập phân",
           "Chuỗi bắt đầu bằng chữ f thay phần trong ngoặc nhọn bằng giá trị của biểu thức đó."),
    "pdigit": ("<code>1_000_000</code>, <code>7 // 2</code>, <code>7 % 2</code>",
               "dấu gạch dưới chỉ để dễ đọc số; <code>//</code> chia lấy phần nguyên (3); <code>%</code> phần dư (1)",
               "Dấu gạch dưới trong số chỉ để dễ đọc, hai dấu gạch chéo chia lấy phần nguyên, và dấu phần trăm cho phần dư."),
    "ptuple": ("<code>a, b = b, a</code>",
               "gán nhiều biến một lúc: vế phải tính xong rồi mới gán vào các tên vế trái, theo thứ tự",
               "Gán nhiều biến một lúc tính xong vế phải rồi mới gán vào các tên bên trái, theo thứ tự."),
    "pnone": ("<code>x is None</code>, <code>k not in d</code>",
              "<code>None</code>: giá trị rỗng, chưa có gì; <code>is None</code>: đúng khi x là rỗng; <code>not in</code>: đúng khi k không có trong d",
              "Giá trị rỗng nghĩa là chưa có gì, và phép không thuộc đúng khi phần tử không nằm trong dãy hay bảng tra."),
    "penum": ("<code>for i, x in enumerate(xs):</code>",
              "duyệt dãy xs và có luôn số thứ tự: i là 0, 1, 2…, x là phần tử tương ứng",
              "Hàm đánh số cho cả số thứ tự lẫn phần tử trong mỗi vòng lặp, số thứ tự bắt đầu từ không."),
    "pdict": ("<code>{\"a\": 1}</code>, <code>d[k] += 1</code>",
              "từ điển: cặp khoá và giá trị trong ngoặc nhọn; <code>d[k]</code> là giá trị của khoá k; <code>+= 1</code> tăng nó thêm 1",
              "Từ điển là các cặp khoá và giá trị trong ngoặc nhọn, và ngoặc vuông với khoá chọn giá trị của khoá đó."),
    "pprint": ("<code>print(a, b)</code>, <code>#</code>",
               "in các giá trị ra màn hình, cách nhau một dấu cách; từ <code>#</code> tới hết dòng là ghi chú, máy bỏ qua",
               "Lệnh in đưa các giá trị ra màn hình cách nhau một dấu cách, còn dấu thăng mở đầu một ghi chú mà máy bỏ qua."),
    # ── YAML, shell ──
    "yflow": ("<code>{app: x}</code>, <code>[a, b]</code>, <code>- name: n</code>",
              "YAML: <code>{k: v}</code> là một nhóm cặp khoá và giá trị viết trên một dòng; <code>[a, b]</code> là danh sách; dòng bắt đầu bằng <code>-</code> là một phần tử của danh sách",
              "Trong tệp YAML, ngoặc nhọn gom các cặp khoá và giá trị trên một dòng, ngoặc vuông là danh sách, và dòng bắt đầu bằng gạch ngang là một phần tử của danh sách."),
    "shpipe": ("<code>lệnh_a | lệnh_b</code>, <code>\"$BIEN\"</code>",
               "dấu <code>|</code> đưa kết quả lệnh a làm đầu vào lệnh b; <code>$BIEN</code>: giá trị của biến môi trường BIEN",
               "Dấu gạch đứng đưa kết quả của lệnh trước làm đầu vào của lệnh sau, và dấu đô la đứng trước tên biến lấy giá trị của biến đó."),
}


def jstep(items, intro="", clear=True, **kw):
    """items: [(khoá JROW hoặc bộ ba (mã_html, đọc_là_html, đọc_là_lời), ví dụ HTML, ví dụ lời đọc hoặc '')].
    Trả về một step: bảng ba cột. Ví dụ rỗng thì bỏ cả câu ví dụ trong lời đọc."""
    rows, say = [], [intro] if intro else []
    has_ex = any(vd for _, vd, _ in items)   # không hàng nào có ví dụ -> bỏ cả cột (bảng hai cột, không để cột trống)
    for k, vd, vs in items:
        r = JROW[k] if isinstance(k, str) else k
        rows.append([r[0], r[1], vd] if has_ex else [r[0], r[1]])
        say.append(r[2] + (f" Ví dụ, {vs}" if vs else ""))
    html = lib2.table(JHEAD if has_ex else JHEAD[:2], rows).replace("$", "<span>&#36;</span>")   # `$` trong bảng không được thành công thức KaTeX
    return lib2.st(html, " ".join(say), clear=clear, **kw)
