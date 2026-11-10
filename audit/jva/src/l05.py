from lib import *


def ln(p, s):
    """Số thứ tự (tính từ 1) của dòng đầu tiên trong mã của p có chứa s."""
    for i, l in enumerate(p["code"].split("\n"), 1):
        if s in l:
            return i
    raise ValueError(s)


SO_DU = "{1500000, 250000, 4000000, 750000, 3200000}"
L = [1500000, 250000, 4000000, 750000, 3200000]


def build():
    mang = prog("Mang", """
import java.util.Arrays;

public class Mang {
    public static void main(String[] args) {
        long[] soDu = %s;
        System.out.println(soDu.length);           // số phần tử
        System.out.println(soDu[0]);               // phần tử đầu
        System.out.println(soDu[4]);               // phần tử cuối
        System.out.println(Arrays.toString(soDu)); // in cả mảng
    }
}""" % SO_DU, out="5\n1500000\n3200000\n[1500000, 250000, 4000000, 750000, 3200000]")
    tao = prog("TaoMang", """
import java.util.Arrays;

public class TaoMang {
    public static void main(String[] args) {
        long[] a = new long[5];              // 5 ô, ô nào cũng bằng 0
        System.out.println(Arrays.toString(a));
        a[0] = 1500000;                      // gán ô chỉ số 0
        a[4] = 3200000;                      // gán ô chỉ số 4, ô cuối
        System.out.println(Arrays.toString(a));
        Arrays.sort(a);                      // sắp tăng dần, sửa ngay trên a
        System.out.println(Arrays.toString(a));
    }
}""", out="[0, 0, 0, 0, 0]\n[1500000, 0, 0, 0, 3200000]\n[0, 0, 0, 1500000, 3200000]")
    tong = prog("TongMang", """
public class TongMang {
    public static void main(String[] args) {
        long[] soDu = %s;
        long tong = 0;
        long lonNhat = soDu[0];              // tạm coi phần tử đầu là lớn nhất
        int viTri = 0;
        for (int i = 0; i < soDu.length; i++) {
            tong += soDu[i];
            if (soDu[i] > lonNhat) {         // gặp số lớn hơn thì ghi lại
                lonNhat = soDu[i];
                viTri = i;
            }
        }
        System.out.println("Tong: " + tong);
        System.out.println("Lon nhat: " + lonNhat + " o chi so " + viTri);
    }
}""" % SO_DU, out="Tong: 9700000\nLon nhat: 4000000 o chi so 2")
    kiem = prog("KiemMang", """
import java.util.Arrays;

public class KiemMang {
    public static void main(String[] args) {
        long[] soDu = %s;
        long[] banSao = Arrays.copyOf(soDu, soDu.length);
        Arrays.sort(banSao);                 // sắp bản sao, giữ nguyên mảng gốc
        System.out.println(Arrays.toString(banSao));
        long tong = 0;
        int i = banSao.length - 1;
        while (i >= 0) {                     // cộng từ ô cuối về ô đầu
            tong += banSao[i];
            i--;
        }
        System.out.println("Lon nhat: " + banSao[banSao.length - 1] + ", tong: " + tong);
    }
}""" % SO_DU, out="[250000, 750000, 1500000, 3200000, 4000000]\nLon nhat: 4000000, tong: 9700000")
    lech = prog("LechMot", """
public class LechMot {
    public static void main(String[] args) {
        long[] soDu = %s;
        for (int i = 0; i <= soDu.length; i++) {   // SAI: dấu <= cho i chạy tới 5
            System.out.println(soDu[i]);
        }
    }
}""" % SO_DU, out="1500000\n250000\n4000000\n750000\n3200000", expect="runtime_error:ArrayIndexOutOfBoundsException",
        err='Exception in thread "main" java.lang.ArrayIndexOutOfBoundsException: Index 5 out of bounds for length 5')
    do_dai = prog("DoDai", """
public class DoDai {
    public static void main(String[] args) {
        long[] soDu = {1500000, 250000};
        System.out.println(soDu.length());   // SAI: độ dài của mảng không có ngoặc tròn
    }
}""", expect="compile_error:cannot find symbol")
    tham = prog("ThamChieu", """
import java.util.Arrays;

public class ThamChieu {
    public static void main(String[] args) {
        long[] soDu = {1500000, 250000, 4000000};
        long[] nhap = soDu;                  // KHÔNG chép: cùng một mảng
        nhap[0] = 0;
        System.out.println(soDu[0]);         // mảng gốc cũng đổi
        long[] banSao = Arrays.copyOf(soDu, soDu.length);  // chép thật
        banSao[1] = 0;
        System.out.println(soDu[1]);         // mảng gốc giữ nguyên
    }
}""", out="0\n250000")
    quiz = prog("DoanMang", """
public class DoanMang {
    public static void main(String[] args) {
        int[] a = {3, 8, 1, 8, 6};
        int viTri = 0;
        int dem = 0;
        for (int i = 0; i < a.length; i++) {
            if (a[i] > a[viTri]) {
                viTri = i;
            }
            if (a[i] > 4) {
                dem++;
            }
        }
        System.out.println(a.length + " " + a[a.length - 1]);
        System.out.println(viTri + " " + dem);
    }
}""", out="5 6\n1 3")

    sc_hook = sc("hook", "hook", "Năm tài khoản, năm nghìn tài khoản: viết bao nhiêu biến?", [
        st("""<p>Ngân hàng nhỏ của bạn có $5$ tài khoản. Người quản lý hỏi: <b>tổng số dư</b> là bao nhiêu, tài khoản nào <b>nhiều tiền nhất</b>?</p>
<div class="box warn">Với những gì đã học, bạn phải khai năm biến <code>soDu1</code> … <code>soDu5</code> và viết năm lệnh cộng. Năm nghìn tài khoản thì không viết nổi.</div>""",
           """Ngân hàng nhỏ của bạn có năm tài khoản. Người quản lý hỏi tổng số dư bao nhiêu, và tài khoản nào nhiều tiền nhất.
           Với những gì đã học, bạn phải khai năm biến riêng, còn năm nghìn tài khoản thì không viết nổi."""),
        st("""<p>Hôm nay ta học <b>mảng</b>: một tên duy nhất giữ cả một dãy giá trị cùng kiểu; mỗi ô có một số thứ tự gọi là <b>chỉ số</b>.</p>
<div class="box key">Mảng ghép với vòng lặp đếm: năm hay năm nghìn tài khoản đều dùng cùng một đoạn mã.</div>""",
           """Hôm nay ta học mảng, tức là một tên giữ cả một dãy giá trị cùng kiểu, mỗi ô có một số thứ tự gọi là chỉ số.
           Ghép mảng với vòng lặp đếm, năm hay năm nghìn tài khoản đều dùng cùng một đoạn mã."""),
    ])
    sc_pre = sc("prereq", "prereq", "Ôn lại ba điều sẽ dùng hôm nay", [
        st(table(["đã học", "viết", "dùng lại hôm nay"],
                 [["① biến kiểu số nguyên dài, tiền tính bằng đồng", "<code>long tong = 0;</code>", "giữ tổng số dư"],
                  ["② vòng lặp đếm", "<code>for (int i = 0; i &lt; 5; i++)</code>", "i lần lượt là 0, 1, 2, 3, 4"],
                  ["③ rẽ nhánh nếu và cộng dồn", "<code>if (x &gt; lon)</code>, <code>tong += x;</code>", "tìm số lớn nhất, cộng tổng"]]),
           """Trước hết ta ôn lại ba điều. Thứ nhất, tiền được giữ trong biến kiểu số nguyên dài, tính theo đơn vị đồng.
           Thứ hai, vòng lặp đếm từ không, chạy khi biến đếm còn nhỏ hơn năm, nên chạy đúng năm lần với không, một, hai, ba, bốn.
           Thứ ba, lệnh rẽ nhánh nếu so sánh hai số, còn phép cộng dồn cộng thêm từng giá trị vào tổng.""", focus=[1, "1.2", "1.3", "1.4"]),
    ])
    sc_sym = sc("sym", "symbol", "Giải mã ký hiệu của mảng", [
        st(code_block(mang, title="Tệp Mang.java"),
           """Đây là chương trình đầu tiên có mảng. Nó khai một mảng năm số dư, mỗi giá trị trong mảng gọi là một phần tử, rồi in số phần tử, phần tử đầu, phần tử cuối, và cả mảng."""),
        st(table(["viết", "nghĩa"],
                 [["<code>long[] soDu</code>", "biến mảng; dấu <code>[]</code> sau kiểu nghĩa là <b>nhiều</b> giá trị kiểu <code>long</code>"],
                  ["<code>{1500000, …}</code>", "liệt kê sẵn giá trị; mỗi giá trị là một <b>phần tử</b>; máy đếm được 5 phần tử"],
                  ["<code>soDu[0]</code>", "phần tử có chỉ số 0, tức phần tử <b>đầu tiên</b>"],
                  ["<code>soDu[4]</code>", "phần tử <b>cuối</b>, vì chỉ số chạy từ 0 tới 5 − 1"],
                  ["<code>soDu.length</code>", "số phần tử: một con số gắn sẵn với mảng (gọi là <b>thuộc tính</b>), <b>không</b> có ngoặc tròn"],
                  ["<code>import java.util.Arrays;</code>", "mượn bộ công cụ mảng; <code>Arrays.toString</code> in cả mảng"],
                  ["<code>new long[5]</code>", "tạo mảng 5 ô mới, ô nào cũng bằng 0"]]),
           """Ngoặc vuông sau tên kiểu nghĩa là biến giữ nhiều số nguyên dài.
           Ngoặc nhọn liệt kê sẵn năm giá trị ban đầu.
           Chỉ số không là phần tử đầu tiên.
           Chỉ số bốn là phần tử cuối, vì chỉ số chạy từ không tới năm trừ một.
           Độ dài là một con số gắn sẵn với mảng, gọi là thuộc tính, cho biết số phần tử, và không có ngoặc tròn.
           Dòng nhập ở đầu tệp mượn bộ công cụ mảng, có hàm in cả mảng.
           Từ khoá tạo mới kèm số năm tạo mảng năm ô, ô nào cũng bằng không.""", clear=True,
           focus=["1.2", "1.3", "1.4", "1.5", "1.6", "1.7", "1.8"]),
        st(out_block(mang),
           """Chạy thật, ta được bốn dòng: năm, một triệu năm trăm nghìn, ba triệu hai trăm nghìn, và cả mảng trong ngoặc vuông."""),
    ])
    cells = [box(340 + k * 225, 150, 210, 90, str(v), C_BLUE, 26, True) for k, v in enumerate(L)]
    idx = [txt(445 + k * 225, 130, f"chỉ số {k}", 22, "middle", "#2a78d6", True) for k in range(5)]
    nth = [txt(445 + k * 225, 275, f"ô thứ {k + 1}", 20, "middle", "#6b7280") for k in range(5)]
    sc_int = sc("intuition", "intuition", "Hình dung: dãy ô liền nhau và một mũi tên trỏ tới", [
        st(svg(1500, 380,
               box(20, 150, 180, 90, ["soDu", "biến mảng"], C_AMBER, 24, True),
               arrow(205, 195, 330, 195, "#d97706", "trỏ tới"),
               *cells, *idx, *nth,
               txt(750, 345, "length = 5; chỉ số hợp lệ từ 0 tới 4; không có ô chỉ số 5", 26, "middle", "#dc2626", True)),
           """Hãy hình dung mảng như một dãy ô liền nhau trong bộ nhớ, phía trên mỗi ô là chỉ số của nó.
           Ô thứ nhất có chỉ số không, ô thứ năm có chỉ số bốn, nghĩa là chỉ số luôn kém số thứ tự thông thường một đơn vị.
           Không có ô nào mang chỉ số năm, vì mảng chỉ có năm ô."""),
        st(svg(1500, 400,
               box(20, 60, 200, 90, ["soDu", "biến thứ nhất"], C_AMBER, 24, True),
               box(20, 250, 200, 90, ["nhap", "biến thứ hai"], C_AMBER, 24, True),
               arrow(225, 105, 560, 180, "#d97706"),
               arrow(225, 295, 560, 230, "#d97706"),
               txt(390, 225, "nhap = soDu", 24, "middle", "#1f2937", True),
               *[box(570 + k * 180, 160, 170, 90, str(v), C_BLUE, 24) for k, v in enumerate(L[:3])],
               txt(1100, 120, "MỘT dãy ô duy nhất trong bộ nhớ", 24, "middle", "#2a78d6", True),
               txt(1000, 330, "gán chỉ chép mũi tên, không chép các ô", 26, "middle", "#dc2626", True)),
           """Điều thứ hai, biến mảng không chứa các con số, mà giữ đường dẫn tới dãy ô, gọi là tham chiếu.
           Gán một biến mảng khác bằng biến này thì máy chỉ chép mũi tên, không chép các ô.
           Vì thế hai biến cùng trỏ vào một dãy ô, sửa qua tên nào thì tên kia cũng thấy."""),
    ])
    a5, a9, a11 = ln(tao, "new long"), ln(tao, "a[4] ="), ln(tao, "Arrays.sort")
    sc_form = sc("formula", "formula", "Suy ra từng bước: tạo, gán, sắp xếp, duyệt mảng", [
        st("<p><b>Bước 1. Tạo mảng 5 ô.</b></p>" + code_block(tao, lines=(a5, a5 + 1))
           + "<span class='note'>Ô kiểu số được Java đặt sẵn giá trị 0, nên in ra [0, 0, 0, 0, 0].</span>",
           """Bước một, tạo mảng. Từ khoá tạo mới kèm số năm trong ngoặc vuông xin bộ nhớ cho năm ô số nguyên dài.
           Java đặt sẵn giá trị không cho mọi ô kiểu số, nên lệnh in cho ra năm số không."""),
        st("<p><b>Bước 2. Gán từng ô theo chỉ số.</b></p>" + code_block(tao, lines=(a5 + 2, a9 + 1))
           + "<span class='note'>Ô 0 và ô 4 đổi, ba ô giữa vẫn là 0: [1500000, 0, 0, 0, 3200000].</span>",
           """Bước hai, gán từng ô. Ta viết tên mảng, chỉ số trong ngoặc vuông, rồi dấu bằng và giá trị, giống gán một biến thường.
           Chỉ ô chỉ số không và ô chỉ số bốn được gán, nên ba ô giữa vẫn là không."""),
        st("<p><b>Bước 3. Sắp xếp tăng dần.</b></p>" + code_block(tao, lines=(a11, a11 + 1)) + out_block(tao),
           """Bước ba, sắp xếp. Hàm sắp xếp của bộ công cụ mảng xếp các ô tăng dần, và sửa ngay trên mảng đó chứ không tạo mảng mới.
           Vì vậy dòng in thứ ba có ba số không đứng trước, rồi tới hai số lớn.""", focus=[1, 2, 4]),
        st("<p><b>Bước 4. Suy ra vòng lặp duyệt mảng.</b></p>" + table(["điều đã biết", "suy ra"],
                 [["chỉ số đầu là 0, mảng có <code>a.length</code> ô", "chỉ số cuối là <code>a.length - 1</code>"],
                  ["chỉ số hợp lệ: 0, 1, …, <code>a.length - 1</code>", "điều kiện lặp <code>i &lt; a.length</code>, <b>không</b> có dấu bằng"],
                  ["vòng lặp đếm từ 0, mỗi lần tăng 1", "<code>for (int i = 0; i &lt; a.length; i++)</code> thăm mỗi ô đúng một lần"]]),
           """Bước bốn, suy ra vòng lặp duyệt mảng. Chỉ số bắt đầu từ không, nên chỉ số cuối bằng độ dài trừ một.
           Vì vậy điều kiện lặp là biến đếm nhỏ hơn độ dài, không có dấu bằng.
           Nhờ đó vòng lặp thăm mỗi ô đúng một lần.""", clear=True),
    ], checks=["sorted([1500000, 0, 0, 0, 3200000]) == [0, 0, 0, 1500000, 3200000]",
               "list(range(0, 5)) == [0, 1, 2, 3, 4] and max(range(0, 5)) == 5 - 1"])
    t3, t7 = ln(tong, "long[] soDu"), ln(tong, "for (")
    sc_ex = sc("example", "example", "Ví dụ: tổng, số dư lớn nhất và vị trí của nó, từng phép tính", [
        st(code_block(tong, lines=(t3, t3 + 3), title="Tệp TongMang.java, phần chuẩn bị"),
           """Bây giờ ta trả lời người quản lý. Biến tổng bắt đầu bằng không, biến lớn nhất tạm lấy phần tử đầu, và biến vị trí bằng không."""),
        st(code_block(tong, lines=(t7, t7 + 6), title="Vòng lặp duyệt mảng"),
           """Vòng lặp đếm đi qua các chỉ số từ không tới bốn, mỗi vòng cộng phần tử hiện tại vào tổng.
           Nếu phần tử hiện tại lớn hơn số lớn nhất đang giữ, ta ghi lại cả giá trị lẫn chỉ số của nó."""),
        st(code_block(tong, lines=(t7 + 1, t7 + 1))
           + "$$① \\; i = 0: \\; \\text{tong} = 0 + 1500000 = \\hl{1500000}$$"
           + "$$② \\; i = 1: \\; \\text{tong} = 1500000 + 250000 = \\hl{1750000}$$",
           """Phép tính thứ nhất, chỉ số không, tổng thành một triệu năm trăm nghìn, và số này không lớn hơn chính nó.
           Phép tính thứ hai, tổng thành một triệu bảy trăm năm mươi nghìn, còn hai trăm năm mươi nghìn nhỏ hơn nên không ghi lại."""),
        st(code_block(tong, lines=(t7 + 2, t7 + 5))
           + "$$③ \\; i = 2: \\; \\text{tong} = 1750000 + 4000000 = \\hl{5750000}$$"
           + "<p>Vì $4000000$ lớn hơn $1500000$: lớn nhất thành $4000000$, vị trí thành $2$.</p>",
           """Phép tính thứ ba, chỉ số hai, tổng thành năm triệu bảy trăm năm mươi nghìn.
           Vì bốn triệu lớn hơn một triệu năm trăm nghìn, nên lớn nhất thành bốn triệu và vị trí thành hai."""),
        st(code_block(tong, lines=(t7 + 1, t7 + 1))
           + "$$④ \\; i = 3: \\; \\text{tong} = 5750000 + 750000 = \\hl{6500000}$$"
           + "$$⑤ \\; i = 4: \\; \\text{tong} = 6500000 + 3200000 = \\hlg{9700000}$$",
           """Phép tính thứ tư, tổng thành sáu triệu năm trăm nghìn. Phép tính thứ năm, tổng thành chín triệu bảy trăm nghìn,
           và ba triệu hai trăm nghìn không lớn hơn bốn triệu nên lớn nhất giữ nguyên."""),
        st(out_block(tong),
           """Chạy thật, hai dòng in ra đúng như ta tính tay: tổng chín triệu bảy trăm nghìn, lớn nhất bốn triệu ở chỉ số hai."""),
    ], checks=["sum([1500000, 250000]) == 1750000", "1750000 + 4000000 == 5750000",
               "5750000 + 750000 + 3200000 == 9700000 == sum([1500000, 250000, 4000000, 750000, 3200000])",
               "max([1500000, 250000, 4000000, 750000, 3200000]) == 4000000",
               "[1500000, 250000, 4000000, 750000, 3200000].index(4000000) == 2"])
    k6, k10 = ln(kiem, "copyOf"), ln(kiem, "int i =")
    sc_chk = sc("check", "check", "Tự kiểm bằng đường khác: sắp xếp bản sao và cộng ngược", [
        st(code_block(kiem, lines=(k6, k6 + 2), title="Tệp KiemMang.java"),
           """Ta kiểm bằng một đường khác hẳn. Chép mảng ra bản sao bằng hàm chép của bộ công cụ mảng, rồi sắp xếp bản sao,
           vì vị trí ban đầu của mảng gốc còn cần dùng. Sau khi sắp tăng dần, số lớn nhất phải nằm ở ô cuối."""),
        st(code_block(kiem, lines=(k10, k10 + 5)),
           """Rồi ta cộng ngược từ ô cuối về ô đầu, bằng vòng lặp chạy khi chỉ số còn lớn hơn hoặc bằng không.
           Phép cộng không phụ thuộc thứ tự, nên tổng này phải trùng tổng lúc trước."""),
        st(out_block(kiem) + table(["", "vòng lặp đếm, mảng gốc", "sắp bản sao, cộng ngược"],
                                   [["lớn nhất", "4000000", "4000000 ✓"], ["tổng", "9700000", "9700000 ✓"]]),
           """Chạy thật, ô cuối của bản sao là bốn triệu, và tổng cộng ngược là chín triệu bảy trăm nghìn.
           Hai cách độc lập cho cùng kết quả, nên ta tin được cả hai con số."""),
    ], checks=["sorted([1500000, 250000, 4000000, 750000, 3200000]) == [250000, 750000, 1500000, 3200000, 4000000]",
               "sum(reversed([250000, 750000, 1500000, 3200000, 4000000])) == 9700000"])
    sc_pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st('<div class="box warn"><b>Lỗi 1 (người mới).</b> Dùng <code>&lt;=</code> thay cho <code>&lt;</code> trong vòng lặp duyệt mảng.</div>'
           + code_block(lech, lines=(3, 6)) + out_block(lech),
           """Lỗi thứ nhất, của người mới, là viết dấu nhỏ hơn hoặc bằng trong vòng lặp duyệt mảng. Năm ô đầu được in bình thường.
           Tới vòng thứ sáu, máy truy cập ô chỉ số năm không tồn tại, và ném ra ngoại lệ vượt chỉ số mảng.
           Thông báo ghi rõ chỉ số năm, độ dài năm, đúng dấu hiệu của lỗi lệch một.""", focus=[1, 4, [2, 4], 4]),
        st('<div class="box warn"><b>Lỗi 2 (người mới).</b> Viết ngoặc tròn sau <code>length</code> của mảng.</div>'
           + code_block(do_dai, lines=(4, 4)) + out_block(do_dai, "Trình biên dịch báo"),
           """Lỗi thứ hai, cũng của người mới, là viết thêm ngoặc tròn sau độ dài của mảng.
           Độ dài của mảng là thuộc tính chứ không phải hàm, nên trình biên dịch báo không tìm thấy ký hiệu.""", focus=[2, 4]),
        st('<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> Gán <code>nhap = soDu</code> rồi tưởng mình đang sửa một bản nháp.</div>'
           + code_block(tham, lines=(5, 11)) + out_block(tham),
           """Lỗi thứ ba gặp cả ở người đã đi làm: gán một biến mới bằng mảng số dư để làm bản nháp, rồi sửa bản nháp.
           Phép gán chỉ chép mũi tên, nên ô đầu của mảng gốc cũng thành không.
           Muốn bản nháp thật thì phải chép bằng hàm chép, khi đó mảng gốc giữ nguyên.""", focus=[2, 4, [2, 4]]),
    ])
    sc_quiz = sc("quiz", "quiz", "Bây giờ tới phần bạn tự làm", [
        st(code_block(quiz, lines=(3, 15), title="Đoán hai dòng in ra"),
           """Bây giờ tới phần bạn tự làm. Mảng có năm số là ba, tám, một, tám, sáu.
           Vòng lặp ghi lại vị trí số lớn nhất bằng phép so sánh lớn hơn, và đếm các số lớn hơn bốn.
           Hãy dừng video, viết ra giấy hai dòng in ra.""", pause=20),
        st(table(["i", "a[i]", "a[i] &gt; a[viTri]?", "viTri", "a[i] &gt; 4?", "dem"],
                 [["0", "3", "3 &gt; 3: sai", "0", "sai", "0"], ["1", "8", "8 &gt; 3: đúng", "1", "đúng", "1"],
                  ["2", "1", "1 &gt; 8: sai", "1", "sai", "1"], ["3", "8", "8 &gt; 8: sai", "1", "đúng", "2"],
                  ["4", "6", "6 &gt; 8: sai", "1", "đúng", "3"]]),
           """Đáp án như sau. Ở chỉ số một, tám lớn hơn ba, nên vị trí thành một.
           Ở chỉ số ba, tám không lớn hơn tám, vì phép so sánh không có dấu bằng, nên vị trí vẫn là một.
           Các số lớn hơn bốn là tám, tám và sáu, nên đếm được ba.""", focus=[1, "1.3", "1.5", ["1.3", "1.5", "1.6"]]),
        st("<p>Dòng thứ nhất: độ dài là $5$; phần tử cuối có chỉ số $5 - 1 = 4$, giá trị $6$. Dòng thứ hai: vị trí $1$, đếm được $3$.</p>"
           "$$\\hl{\\text{5 6}} \\qquad \\hl{\\text{1 3}}$$",
           """Dòng thứ nhất in độ dài năm, rồi phần tử ở chỉ số bốn, tức là sáu. Dòng thứ hai in vị trí một và số đếm ba."""),
        st(out_block(quiz),
           """Chạy thật chương trình, hai dòng in ra đúng là năm sáu, và một ba."""),
    ], checks=["[3, 8, 1, 8, 6].index(max([3, 8, 1, 8, 6])) == 1",
               "len([x for x in [3, 8, 1, 8, 6] if x > 4]) == 3",
               "[3, 8, 1, 8, 6][len([3, 8, 1, 8, 6]) - 1] == 6"])
    sc_rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        st(chain("mảng: n ô cùng kiểu", "chỉ số 0 … n − 1", "duyệt bằng i &lt; length", "biến mảng giữ tham chiếu"),
           """Tổng kết chuỗi logic. Mảng là một dãy ô cùng kiểu, chỉ số chạy từ không tới độ dài trừ một,
           nên vòng lặp duyệt dùng điều kiện nhỏ hơn độ dài. Còn biến mảng chỉ giữ tham chiếu tới dãy ô."""),
        st("""<div class='box key'><b>Tư duy:</b> mỗi lần viết vòng lặp duyệt mảng, tự hỏi “chỉ số cuối là bao nhiêu?”.
Muốn sửa thử mà không đụng dữ liệu thật thì <b>chép</b> bằng <code>Arrays.copyOf</code>, đừng chỉ gán.</div>""",
           """Điều cần mang theo. Mỗi lần viết vòng lặp duyệt mảng, hãy tự hỏi chỉ số cuối là bao nhiêu.
           Muốn sửa thử mà không đụng dữ liệu thật, hãy chép ra bản sao, đừng chỉ gán."""),
    ])
    return lesson("L05", "mang", "Bài 5 — Mảng: nhiều giá trị cùng kiểu dưới một tên",
                  "curriculum/jva.yaml L05; audit/jva/verify_jva.py L05 (javac/java chạy thật); The Java Language Specification, "
                  "Java SE 21 (JLS §10 mảng, §10.4 truy cập và ArrayIndexOutOfBoundsException, §10.7 length, §4.12.5 giá trị mặc định); "
                  "java.util.Arrays (toString, sort, copyOf), Java SE 21 API; dev.java/learn",
                  ["Tạo mảng, đọc và gán phần tử theo chỉ số từ 0 tới length − 1",
                   "Duyệt mảng bằng vòng lặp đếm để tính tổng, tìm lớn nhất và vị trí",
                   "Dùng Arrays.toString, Arrays.sort, Arrays.copyOf",
                   "Giải thích vì sao gán một biến mảng cho biến khác không tạo bản sao"],
                  [sc_hook, sc_pre, sc_sym, sc_int, sc_form, sc_ex, sc_chk, sc_pit, sc_quiz, sc_rec])
