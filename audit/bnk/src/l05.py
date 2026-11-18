from lib import *
from labkit import write_lab, practice_steps, practice_scene


def build():
    ora = prog("KhoaTheoThuTu", """
SET HEADING OFF
SET PAGESIZE 0
SET SERVEROUTPUT ON
BEGIN EXECUTE IMMEDIATE 'DROP TABLE bnk_tk'; EXCEPTION WHEN OTHERS THEN NULL; END;
/
CREATE TABLE bnk_tk (id NUMBER PRIMARY KEY, so_du NUMBER);
INSERT INTO bnk_tk VALUES (2, 1000000);
INSERT INTO bnk_tk VALUES (5, 500000);
COMMIT;
DECLARE
  v_nho NUMBER;
  v_lon NUMBER;
BEGIN
  SELECT so_du INTO v_nho FROM bnk_tk WHERE id = 2 FOR UPDATE;   -- khoá id nhỏ trước
  SELECT so_du INTO v_lon FROM bnk_tk WHERE id = 5 FOR UPDATE;   -- rồi mới tới id lớn
  UPDATE bnk_tk SET so_du = so_du - 300000 WHERE id = 2;
  UPDATE bnk_tk SET so_du = so_du + 300000 WHERE id = 5;
  COMMIT;
  DBMS_OUTPUT.PUT_LINE('xong, tong truoc = ' || (v_nho + v_lon));
END;
/
SELECT id || ' ' || so_du FROM bnk_tk ORDER BY id;""", out="""xong, tong truoc = 1500000
2 700000
5 800000""", lang="oracle")
    be_tac = prog("BeTac", """
import java.util.concurrent.TimeUnit;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;
public class BeTac {
    static boolean lam(Lock dau, Lock sau) {
        dau.lock();                                   // khoá hàng thứ nhất
        try {
            Thread.sleep(200);                        // để luồng kia kịp khoá hàng của nó
            boolean duoc = sau.tryLock(500, TimeUnit.MILLISECONDS);   // xin hàng sau, tối đa 0,5 giây
            if (duoc) sau.unlock();
            return duoc;
        } catch (InterruptedException e) {
            return false;
        } finally { dau.unlock(); }
    }
    static String thu(Lock x1, Lock y1, Lock x2, Lock y2) throws Exception {
        boolean[] ok = new boolean[2];
        Thread t1 = new Thread(() -> ok[0] = lam(x1, y1));
        Thread t2 = new Thread(() -> ok[1] = lam(x2, y2));
        t1.start(); t2.start(); t1.join(); t2.join();
        return ok[0] && ok[1] ? "xong" : "be tac";
    }
    public static void main(String[] args) throws Exception {
        Lock a = new ReentrantLock(), b = new ReentrantLock();
        System.out.println("A roi B  va  B roi A: " + thu(a, b, b, a));
        System.out.println("A roi B  va  A roi B: " + thu(a, b, a, b));
    }
}""", out="""A roi B  va  B roi A: be tac
A roi B  va  A roi B: xong""")
    lab_tk = prog("ThuTuKhoa", """
public class ThuTuKhoa {
    public static void main(String[] args) {
        int[][] lenh = { {4, 9}, {9, 4}, {7, 4}, {4, 7} };
        for (int[] l : lenh) {
            int dau = Math.min(l[0], l[1]);
            int sau = Math.max(l[0], l[1]);
            System.out.println(l[0] + " -> " + l[1] + ": khoa " + dau + " roi " + sau);
        }
    }
}""", out="""4 -> 9: khoa 4 roi 9
9 -> 4: khoa 4 roi 9
7 -> 4: khoa 4 roi 7
4 -> 7: khoa 4 roi 7""")
    hook = sc("hook", "hook", "Vì sao hai lệnh chuyển tiền ngược chiều lại làm nhau treo?", [
        st("""<p>Lệnh 1 chuyển từ tài khoản A sang B. Lệnh 2 chuyển từ B sang A, cùng lúc. Mỗi lệnh <b>khoá hàng của mình trước</b> rồi chờ hàng của lệnh kia.</p>
<div class="box key">Cả hai chờ nhau mãi. Oracle phát hiện và trả lỗi <b>ORA-00060</b> cho một trong hai.</div>""",
           """Chào bạn, lệnh một chuyển từ tài khoản A sang B. Lệnh hai chuyển từ B sang A, cùng lúc. Mỗi lệnh khoá hàng của mình trước, rồi chờ hàng của lệnh kia.
           Cả hai chờ nhau mãi. Oracle phát hiện chuyện này và trả lỗi O R A không không không sáu không cho một trong hai lệnh."""),
        st(table(["thứ tự khoá của hai phiên", "kết quả mô phỏng"],
                 [["A rồi B  và  B rồi A (ngược nhau)", "bế tắc khoá"],
                  ["A rồi B  và  A rồi B (cùng thứ tự)", "chạy bình thường"]]),
           """Hai phiên khoá ngược thứ tự thì bế tắc. Hai phiên khoá cùng thứ tự thì chạy bình thường."""),
    ])
    pre = sc("prereq", "prereq", "Trước hết: bốn điều cần hiểu", [
        st(table(["khái niệm", "nghĩa", "ví dụ"],
                 [["① Phiên", "một kết nối đang làm việc với cơ sở dữ liệu (cơ sở dữ liệu: phần mềm lưu bảng, hỏi bằng ngôn ngữ SQL), thường của một luồng (dòng việc chạy riêng) của chương trình", "phiên 1, phiên 2"],
                  ["② Giao dịch", "nhiều thao tác cùng thành công hoặc cùng huỷ; kết thúc bằng commit (chốt lưu) hoặc rollback (huỷ hết)", "trừ A rồi cộng B"],
                  ["③ Khoá hàng", "khi một phiên sửa một hàng, hàng đó bị khoá tới khi giao dịch kết thúc", "UPDATE (lệnh SQL sửa hàng) tài khoản A"],
                  ["④ Chờ", "phiên khác muốn sửa hàng đang khoá thì phải đứng chờ", "phiên 2 chờ hàng A"]]),
           """Trước hết ta cần hiểu bốn điều. Phiên là một kết nối đang làm việc với cơ sở dữ liệu, tức phần mềm lưu bảng dữ liệu mà ta hỏi bằng ngôn ngữ SQL.
           Giao dịch là nhiều thao tác cùng thành công hoặc cùng huỷ, và kết thúc bằng chốt để lưu, hoặc hoàn tác để huỷ hết.
           Khi một phiên sửa một hàng, hàng đó bị khoá cho tới khi giao dịch kết thúc. Phiên khác muốn sửa hàng đang khoá thì phải đứng chờ.
           Mỗi phiên thường thuộc về một luồng, tức một dòng việc chạy riêng của chương trình."""),
        st("""$$2 \\cdot 2 = 4$$""",
           """Hai phiên, mỗi phiên có hai cách chọn thứ tự khoá hai hàng, nên có hai nhân hai bằng bốn cặp thứ tự. """),
    ], checks=["2 * 2 == 4"])
    sym = sc("sym", "symbol", "Giải mã vài từ hay gặp", [
        st(table(["từ", "nghĩa"],
                 [["id", "mã số định danh mỗi hàng, ví dụ mã tài khoản 2, 5"],
                  ["deadlock (bế tắc)", "hai hay nhiều phiên chờ nhau theo vòng tròn, không ai đi tiếp được"],
                  ["SELECT ... FOR UPDATE", "đọc và khoá luôn các hàng đọc được để sửa an toàn"],
                  ["ORA-00060", "mã lỗi Oracle: phát hiện bế tắc khi chờ tài nguyên"],
                  ["đồ thị chờ", "mũi tên từ phiên đang chờ tới phiên đang giữ khoá; có vòng tròn là bế tắc"],
                  ["PL/SQL", "ngôn ngữ lập trình thủ tục của Oracle, chạy ngay trong cơ sở dữ liệu"]]),
           """Mã số định danh là con số riêng của mỗi hàng. Bế tắc là khi hai hay nhiều phiên chờ nhau theo vòng tròn, không ai đi tiếp được. Câu lệnh đọc kèm khoá cho phép đọc rồi khoá luôn các hàng để sửa an toàn.
           Mã lỗi sáu mươi là cách Oracle báo đã phát hiện bế tắc. Đồ thị chờ có mũi tên từ phiên chờ tới phiên giữ khoá, có vòng tròn là bế tắc.
           Cuối cùng, P L S Q L là ngôn ngữ thủ tục của Oracle, chạy ngay trong cơ sở dữ liệu."""),
    ])
    intu = sc("intuition", "intuition", "Hình dung: vòng tròn chờ", [
        st(svg(1500, 450,
               box(60, 130, 340, 120, ["Phiên 1", "đang giữ hàng A"], C_BLUE, bold=True),
               box(1100, 130, 340, 120, ["Phiên 2", "đang giữ hàng B"], C_AMBER, bold=True),
               arrow(405, 165, 1095, 165, "#dc2626", "chờ: phiên 1 muốn hàng B, phiên 2 đang giữ", 22),
               arrow(1095, 225, 405, 225, "#dc2626", "chờ: phiên 2 muốn hàng A, phiên 1 đang giữ", 22),
               txt(750, 330, "Mũi tên đi từ phiên đang chờ tới phiên đang giữ khoá", 24, "middle", "#475569"),
               txt(750, 395, "Hai mũi tên khép vòng → vòng tròn chờ → bế tắc", 28, "middle", "#dc2626", True)),
           """Hình cho thấy vòng tròn chờ, vẽ theo quy ước mũi tên đi từ phiên đang chờ tới phiên đang giữ khoá. Phiên một đang giữ hàng A và muốn hàng B, nên mũi tên đi sang phiên hai.
           Phiên hai đang giữ hàng B và muốn hàng A, nên mũi tên đi ngược lại. Hai mũi tên khép thành vòng, không phiên nào chịu nhả khoá đang giữ, nên đó là bế tắc."""),
        st(svg(1500, 420,
               txt(750, 40, "Quy tắc: luôn khoá theo thứ tự id tăng dần", 28, "middle", "#1f2937", True),
               box(60, 90, 300, 80, ["Phiên 1: chuyển", "id 2 → id 5"], C_BLUE, size=22), box(60, 220, 300, 80, ["Phiên 2: chuyển", "id 5 → id 2"], C_AMBER, size=22),
               arrow(365, 130, 560, 130, "#475569"), arrow(365, 260, 560, 260, "#475569"),
               box(570, 90, 360, 80, "sắp lại: khoá 2 rồi 5", C_GREEN), box(570, 220, 360, 80, "sắp lại: khoá 2 rồi 5", C_GREEN),
               box(1020, 150, 420, 100, ["cả hai cùng thứ tự", "→ không có vòng tròn"], C_GREEN, bold=True),
               arrow(935, 130, 1015, 190, "#475569"), arrow(935, 260, 1015, 220, "#475569")),
           """Phiên một chuyển từ tài khoản mã hai sang mã năm, phiên hai chuyển ngược lại. Dù lệnh chuyển theo chiều nào, ta luôn khoá hàng có id nhỏ trước, rồi mới khoá hàng có id lớn.
           Khi mọi phiên cùng một thứ tự, không thể có vòng tròn chờ."""),
        st(svg(1500, 400,
               box(60, 40, 1380, 60, "DECLARE  — khai báo biến (không bắt buộc)", C_GRAY),
               box(60, 120, 1380, 100, ["BEGIN  — các lệnh chạy theo thứ tự", "khoá hàng nhỏ trước, rồi hàng lớn; trừ; cộng"], C_BLUE),
               box(60, 240, 1380, 70, "EXCEPTION  — xử lý lỗi, ví dụ ORA-00060", C_RED),
               box(60, 330, 1380, 50, "END;", C_GRAY, size=24)),
           """Một khối P L S Q L gồm bốn phần.  Phần chính chạy các lệnh theo thứ tự, ở đây là khoá hàng nhỏ trước, rồi hàng lớn, rồi trừ và cộng.
           Phần xử lý lỗi bắt những lỗi như bế tắc. Cuối cùng là từ khoá kết thúc."""),
    ])
    form = sc("formula", "formula", "Suy ra từng bước: vì sao thứ tự khoá chặn được bế tắc?", [
        st("""<p><b>Bước 1.</b> Bế tắc cần một <b>vòng tròn chờ</b>: phiên 1 chờ phiên 2, phiên 2 chờ phiên 1.</p>
<span class='note'>Làm thử: 2 phiên, 2 mũi tên chờ khép kín.</span>""",
           """Bước một, vì bế tắc cần một vòng tròn chờ, nên ta chỉ cần ngăn vòng tròn xuất hiện. """),
        st("""<p><b>Bước 2.</b> Vòng tròn <b>chỉ có thể</b> xuất hiện khi hai phiên lấy hai khoá theo <b>thứ tự ngược nhau</b>, và xảy ra thật khi cả hai kịp giữ khoá đầu. Với 2 khoá có $2 \\cdot 2 = 4$ cặp thứ tự, trong đó $2$ cặp ngược nhau.</p>
<span class='note'>Làm thử: (A,B)+(B,A) và (B,A)+(A,B) là hai cặp ngược.</span>""",
           """Bước hai, vì phiên giữ một khoá rồi xin khoá thứ hai, nên trong mô hình hai hàng này, vòng tròn chỉ có thể xuất hiện khi hai phiên lấy hai khoá theo thứ tự ngược nhau. 
           Với hai khoá có bốn cặp thứ tự, trong đó hai cặp ngược nhau."""),
        st("""<p><b>Bước 3.</b> Nếu mọi phiên đều khoá theo thứ tự tăng của id, mọi cặp thứ tự đều <b>giống nhau</b>, nên số cặp ngược là $0$.</p>
<span class='note'>Làm thử: sắp lại cả hai phiên thành (2,5) và (2,5) → chạy bình thường.</span>""",
           """Bước ba, vì nếu mọi phiên đều khoá theo thứ tự tăng của id, thì mọi cặp thứ tự đều giống nhau, nên số cặp ngược là không. Làm thử, sắp lại cả hai phiên thành hai rồi năm, thì chạy bình thường."""),
    ], checks=["2 * 2 == 4", "[alg.bnk_lock_sim([p, q]) for p in (['A', 'B'], ['B', 'A']) for q in (['A', 'B'], ['B', 'A'])] == ['ok', 'deadlock', 'deadlock', 'ok']",
               "alg.bnk_lock_sim([sorted([5, 2]), sorted([2, 5])]) == 'ok'"])
    ex = sc("example", "example", "Ví dụ bằng số, từng phép tính", [
        st("""<p>Hai tài khoản có id $2$ và $5$. Lệnh 1 chuyển $2 \\to 5$, lệnh 2 chuyển $5 \\to 2$. Mỗi lệnh khoá <b>nguồn trước</b>.</p>
$$① \\; \\text{Phiên 1 khoá } 2,\\ \\text{Phiên 2 khoá } 5$$""",
           """Hai tài khoản có id hai và năm. Lệnh một chuyển từ hai sang năm, lệnh hai chuyển từ năm sang hai, mỗi lệnh khoá nguồn trước.
           Bước thứ nhất, phiên một khoá hàng hai, phiên hai khoá hàng năm."""),
        st("""<p>Vòng chờ kế tiếp: Phiên 1 xin hàng $5$ nhưng $5$ đang bị Phiên 2 giữ; Phiên 2 xin hàng $2$ nhưng $2$ đang bị Phiên 1 giữ.</p>
$$② \\; \\text{không ai tiến thêm được} \\Rightarrow \\hl{\\text{bế tắc}}$$""",
           """Bước thứ hai, phiên một xin hàng năm nhưng hàng năm đang do phiên hai giữ. Phiên hai xin hàng hai nhưng hàng hai đang do phiên một giữ. Không ai tiến thêm được, nên là bế tắc."""),
        st("""<p>Áp quy tắc: mỗi lệnh sắp hai id tăng dần, ra $(2, 5)$.</p>
$$③ \\; \\text{Phiên 1: } 2 \\to 5,\\quad \\text{Phiên 2: } 2 \\to 5$$""",
           """Bước thứ ba, áp quy tắc. Mỗi lệnh sắp hai id tăng dần, nên cả hai cùng khoá hai rồi mới tới năm.""", clear=True),
        st("""<p>Phiên 1 khoá $2$ trước. Phiên 2 cũng xin $2$ nên <b>chờ ngay từ đầu</b> và chưa giữ gì cả.</p>
$$④ \\; \\text{số khoá Phiên 2 đang giữ} = \\hlg{0} \\Rightarrow \\text{không ai bị chờ vòng}$$""",
           """Bước thứ tư, phiên một khoá hai trước. Phiên hai cũng cần hai nên chờ ngay từ đầu và chưa giữ khoá nào. Vì phiên hai không giữ gì, nên không ai bị chờ vòng."""),
        st("""<p>Phiên 1 khoá $5$, trừ, cộng, commit, nhả cả hai khoá. Phiên 2 vào.</p>
$$⑤ \\; \\text{kết quả} = \\hlg{\\text{cả hai lệnh xong lần lượt}}$$""",
           """Bước thứ năm, phiên một khoá hàng năm, trừ và cộng, rồi commit và nhả cả hai khoá. Phiên hai mới vào, nên cả hai lệnh xong lần lượt."""),
    ], checks=["alg.bnk_lock_sim([[2, 5], [5, 2]]) == 'deadlock'", "alg.bnk_lock_sim([sorted([2, 5]), sorted([5, 2])]) == 'ok'"])
    chk = sc("check", "check", "Tự kiểm bằng đường khác: thử hết cặp thứ tự", [
        st("""<p>Đường khác: vì chỉ có hai khoá, ta vét cạn mọi cặp thứ tự, rồi chạy mô phỏng cho từng cặp.</p>""",
           """Kiểm bằng đường khác. Ta vét cạn mọi cặp thứ tự của hai khoá, rồi chạy mô phỏng cho từng cặp. Mô phỏng này kiểm logic thứ tự khoá; bế tắc thật cần hai phiên chạy cùng lúc, nên ta mô phỏng bằng Java."""),
        st(table(["phiên 1", "phiên 2", "kết quả (khi cả hai kịp giữ khoá đầu)"],
                 [["A, B", "A, B", "bình thường"], ["A, B", "B, A", "bế tắc"], ["B, A", "A, B", "bế tắc"], ["B, A", "B, A", "bình thường"]]),
           """Vì chỉ hai cặp ngược nhau mới bế tắc, nên kết quả khớp với bước hai."""),
        st(table(["nguyên nhân ORA-00060 ngoài đời", "sắp thứ tự hàng có chữa được?", "cách chữa"],
                 [["hai phiên khoá hàng ngược thứ tự", "có", "khoá theo id tăng dần"],
                  ["khoá ngoại (cột ở bảng con trỏ tới bảng cha) không có chỉ mục: xoá hay sửa khoá chính ở bảng cha thì Oracle khoá cả bảng con", "không", "tạo chỉ mục (cấu trúc tra nhanh) cho cột khoá ngoại"],
                  ["thiếu chỗ ITL (danh sách giao dịch đang sửa khối) trong khối dữ liệu (đơn vị nhỏ nhất Oracle đọc ghi trên đĩa, chứa nhiều hàng); tham số INITRANS khai số chỗ ITL dành sẵn, nếu thấp thì thiếu", "không", "tăng INITRANS (số chỗ ITL dành sẵn) cho bảng hay chỉ mục nóng"]]),
           """Ngoài đời, bế tắc còn có nguyên nhân khác. Một là khoá ngoại, cột ở bảng con trỏ tới bảng cha, không có chỉ mục: sửa khoá chính ở bảng cha làm Oracle khoá cả bảng con.
           Hai là khối dữ liệu, đơn vị nhỏ nhất Oracle đọc ghi, thiếu chỗ ghi các giao dịch đang sửa nó. Vì vậy sắp thứ tự hàng không chữa được hai loại này, mà phải tạo chỉ mục hoặc tăng chỗ trong khối.""",
           clear=True),
    ], checks=["sum(1 for p in (['A', 'B'], ['B', 'A']) for q in (['A', 'B'], ['B', 'A']) if alg.bnk_lock_sim([p, q]) == 'deadlock') == 2"])
    pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st("""<div class="box warn"><b>Lỗi 1 (người mới).</b> Nghĩ đọc dữ liệu cũng làm người khác chờ. Với Oracle, <b>câu SELECT thường không khoá hàng</b> và người đọc không chặn người ghi.</div>""",
           """Lỗi thứ nhất, của người mới. Nghĩ đọc dữ liệu cũng làm người khác chờ. Với Oracle, câu đọc thông thường không khoá hàng, và người đọc không chặn người ghi."""),
        st("""<div class="box warn"><b>Lỗi 2 (người đã đi làm).</b> <b class="red">Khoá theo thứ tự người gọi đưa vào</b>, tức nguồn rồi đích. Hai lệnh ngược chiều sẽ gặp bế tắc đúng lúc cao điểm.
<br><span class="note">Cách chữa: sắp các id tăng dần rồi khoá từng hàng bằng câu riêng; đừng tin <code>ORDER BY … FOR UPDATE</code> khoá theo thứ tự ORDER BY.</span></div>""",
           """Lỗi thứ hai, của người đã đi làm, là khoá theo thứ tự người gọi đưa vào, tức nguồn rồi đích. Hai lệnh ngược chiều sẽ gặp bế tắc đúng lúc cao điểm.
           Cách chữa là sắp các id tăng dần, rồi khoá từng hàng bằng một câu lệnh riêng. Đừng tin rằng một câu đọc kèm khoá có sắp thứ tự sẽ khoá đúng theo thứ tự đã sắp."""),
        st("""<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> Gặp ORA-00060 rồi <b>thử lại ngay</b>. Theo mô tả của Oracle, chỉ <b>câu lệnh</b> bị huỷ, không phải cả giao dịch, nên các khoá cũ vẫn còn.
<br><span class="note">Cách chữa: rollback cả giao dịch rồi mới thử lại, kèm giới hạn số lần thử.</span></div>""",
           """Lỗi thứ ba, cũng của người đã đi làm, là gặp lỗi bế tắc rồi thử lại ngay. Theo mô tả của Oracle, chỉ câu lệnh bị huỷ, không phải cả giao dịch, nên các khoá cũ vẫn còn.
           Cách chữa là rollback cả giao dịch rồi mới thử lại, kèm giới hạn số lần thử."""),
    ])
    quiz = sc("quiz", "quiz", "Đến lượt bạn", [
        st(table(["câu", "đề"],
                 [["1", "Với 3 khoá, mỗi phiên khoá cả 3 theo một thứ tự. Mỗi phiên có bao nhiêu thứ tự?"],
                  ["2", "Chuyển tiền từ tài khoản 9 sang tài khoản 4. Thứ tự khoá đúng?"],
                  ["3", "Quyết định: tránh bế tắc bằng sắp thứ tự, hay đặt giới hạn chờ rồi thử lại?"]]),
           """Đến lượt bạn. Câu một, với ba khoá, mỗi phiên khoá cả ba theo một thứ tự, mỗi phiên có bao nhiêu thứ tự? Câu hai, chuyển tiền từ tài khoản chín sang tài khoản bốn, thứ tự khoá đúng là gì?
           Câu ba, nên tránh bế tắc bằng sắp thứ tự, hay đặt giới hạn chờ rồi thử lại? Hãy dừng video và làm ra giấy.""",
           pause=25),
        st("""<p>Câu 1: chọn khoá đầu có $3$ cách, khoá hai có $2$ cách, khoá ba có $1$ cách.</p>
$$3 \\cdot 2 \\cdot 1 = \\hl{6}$$""",
           """Đáp án câu một. Khoá đầu có ba cách chọn, khoá thứ hai có hai cách, khoá thứ ba còn một cách. Ba nhân hai nhân một bằng sáu thứ tự."""),
        st("""<p>Câu 2: id nhỏ trước, id lớn sau.</p>
$$\\text{khoá } 4 \\text{ trước, rồi khoá } 9$$""",
           """Đáp án câu hai. Luôn khoá id nhỏ trước, nên khoá tài khoản bốn trước, rồi mới khoá tài khoản chín, dù tiền đi từ chín sang bốn."""),
        st(table(["lựa chọn", "được", "mất"],
                 [["sắp thứ tự khoá", "ngăn bế tắc từ gốc", "phải biết trước mọi khoá cần lấy"],
                  ["giới hạn chờ rồi thử lại", "đơn giản, bắt được mọi trường hợp", "bế tắc vẫn xảy ra, tốn thời gian chờ và thử lại"]]),
           """Đáp án câu ba. Sắp thứ tự khoá ngăn bế tắc từ gốc, nhưng phải biết trước mọi khoá cần lấy. Giới hạn chờ rồi thử lại đơn giản và bắt được mọi trường hợp, nhưng bế tắc vẫn xảy ra."""),
    ], checks=["3 * 2 * 1 == 6 == len(list(__import__('itertools').permutations('ABC')))", "sorted([9, 4]) == [4, 9]"])
    rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        st(chain("giữ khoá, xin khoá khác", "hai phiên ngược thứ tự", "vòng tròn chờ = bế tắc", "luôn khoá theo thứ tự id tăng"),
           """Hai phiên ngược thứ tự thì tạo vòng tròn chờ, tức bế tắc. Luôn khoá theo thứ tự id tăng dần để chặn vòng tròn."""),
        st("""<div class='box key'><b>Tư duy:</b> bế tắc là lỗi <b>thiết kế thứ tự</b>, không phải lỗi may rủi.
Gặp bế tắc: rollback cả giao dịch, thử lại có giới hạn, và sửa thứ tự khoá.</div>""",
           """Bế tắc là lỗi thiết kế thứ tự, không phải lỗi may rủi. Gặp bế tắc thì rollback cả giao dịch, thử lại có giới hạn, và sửa thứ tự khoá."""),
    ])
    # ── AF2: PL/SQL chạy thật trên Oracle, mô phỏng bế tắc bằng Java, quy mô, tự làm ──
    run = sc("chay_that", "example", "Chạy thật: khoá hàng theo thứ tự trên Oracle, và mô phỏng bế tắc", [
        st(code_block(ora, lines=(3, 3), title="Chạy thật trên Oracle 26ai Free (Docker): bật in đầu ra, dựng bảng hai hàng")
           + code_block(ora, lines=(6, 9)),
           """Trước hết là mã chạy thật trên Oracle, cài trong Docker, một công cụ chạy phần mềm trong một hộp riêng, tách khỏi phần còn lại của máy. Lệnh đầu của công cụ gõ lệnh Oracle bật cho hàm in hiển thị chữ ra màn hình. Ta dựng bảng hai hàng: mã hai có một triệu, mã năm có năm trăm nghìn, rồi chốt lưu."""),
        st(code_block(ora, lines=(10, 20), title="PL/SQL: khoá id nhỏ trước"),
           """Khối này khai hai biến kiểu số của Oracle, và từ khoá vào cất giá trị đọc được vào biến, và hàm in của Oracle ghi dòng chữ ra màn hình. Rồi nó khoá hàng có mã hai, và sau đó mới khoá hàng có mã năm, tức là luôn khoá mã nhỏ trước.
           Sau khi giữ cả hai hàng, nó trừ ba trăm nghìn ở hàng thứ nhất, cộng ba trăm nghìn ở hàng thứ hai, chốt lưu, và in tổng trước khi chuyển.""", clear=True),
        st(code_block(ora, lines=(21, 22), title="Câu hỏi cuối: xem số dư hai hàng") + out_block(ora),
           """Cuối cùng ta hỏi số dư hai hàng. Khi chạy thật, tổng trước khi chuyển là một triệu rưỡi. Hàng hai còn bảy trăm nghìn, hàng năm có tám trăm nghìn, tổng vẫn một triệu rưỡi, nên không mất đồng nào.
            Dấu gạch chéo ở dòng riêng báo hết khối để Oracle chạy nó, và hai gạch đứng nối mã với số dư thành một dòng chữ.""", clear=True),
        *jsteps([("base", "<code>import …;</code>, <code>System.out.println(x)</code>, <code>return duoc;</code>, <code>// chú thích</code>, <code>\"A roi B \" + …</code>", None)]),
        st(code_block(be_tac, lines=(1, 4), title="Mô phỏng bế tắc bằng Java (phần 1): nhập các lớp khoá và mở lớp"),
           """Oracle tự phát hiện vòng chờ, nên để thấy bế tắc ta mô phỏng bằng Java, với mỗi hàng là một khoá. """, clear=True),
        *jsteps([("sig", "<code>static boolean lam(Lock dau, Lock sau)</code>: hàm <code>lam</code>, trả về đúng hoặc sai, nhận hai khoá",
                "hàm làm, nhận hai khoá và trả về đúng hoặc sai."),
               ("throws", "<code>static String thu(Lock x1, …) throws Exception</code>: trả về chuỗi, được ném lỗi",
                "hàm thử ở phần ba, được phép ném lỗi chờ luồng."),
               ("if", "<code>if (duoc) sau.unlock();</code>: xin được hàng sau thì nhả nó ngay", None)]),
        st(code_block(be_tac, lines=(5, 15), title="Phần 2: mỗi luồng khoá hàng đầu rồi xin hàng sau"),
           """Mỗi luồng giữ hàng thứ nhất, ngủ một chút để luồng kia kịp giữ hàng của nó, rồi xin hàng thứ hai, chờ tối đa nửa giây. Lệnh khoá xin khoá và chờ tới khi được, còn lệnh thử khoá chỉ chờ một lúc rồi bỏ.
           Nếu hết giờ mà chưa xin được, ta coi là bế tắc. Khối thử là phần làm việc có thể gặp sự cố. Khối bắt lo sự cố luồng bị đánh thức giữa lúc ngủ, ta coi như thất bại. Khối cuối luôn chạy dù có sự cố hay không, nên khoá luôn được nhả.""", clear=True),
        *jsteps([("thread", "<code>t1.start(); t2.start(); t1.join(); t2.join();</code>: cho hai luồng chạy, rồi chờ cả hai xong", None)]),
        st(code_block(be_tac, lines=(16, 28), title="Phần 3: thử hai thứ tự khoá"),
           """Phần này chạy hai luồng, và trả về xong hay bế tắc. Mảng hai ô đúng sai ghi kết quả của từng luồng, và mũi tên là một việc nhỏ gọi hàm khoá rồi ghi vào ô của mình. Dấu hỏi chấm chọn một trong hai chữ, tuỳ cả hai ô đều đúng hay không. """, clear=True),
        st(out_block(be_tac),
           """Khi chạy thật, khoá ngược thứ tự thì bế tắc, vì mỗi luồng giữ hàng mà luồng kia cần. Khoá cùng thứ tự thì xong, vì luồng thứ hai không giữ được hàng đầu tiên nên chưa giữ gì cả, và đợi luồng thứ nhất làm xong.
           Mô phỏng này dùng hết giờ chờ, còn Oracle trả lỗi không không không sáu không cho một phiên.""", clear=True),
    ])
    scale = sc("quy_mo", "example", "Quy mô: cặp phiên tăng bình phương, bế tắc từ hiếm thành liên tục", [
        st("""<p>Gọi $T$ là số phiên chạy cùng lúc. Số cặp phiên là $\\frac{T \\cdot (T - 1)}{2}$. Giả sử mỗi cặp có xác suất $0{,}0001$ gây bế tắc (tính cả khả năng khoá ngược thứ tự lẫn chồng thời gian) <i>(số minh hoạ)</i>; số cặp gây bế tắc kỳ vọng là số cặp nhân $0{,}0001$.</p><p class="note">Kỳ vọng: giá trị trung bình khi lặp lại thật nhiều lần. Số cặp là T(T−1)/2 vì mỗi phiên ghép với T−1 phiên khác, nhưng mỗi cặp bị đếm hai lần. Giả định: số hàng nóng giữ nguyên khi tải tăng nên xác suất mỗi cặp không đổi; 100 000 phiên cùng tranh hai hàng là trường hợp cực đoan.</p>"""
           + table(["tải", "phiên cùng lúc T", "số cặp phiên", "cặp gây bế tắc kỳ vọng (giả định)"],
                   [["×1", "10", "45", "0,0045 (hiếm)"],
                    ["×100", "1 000", "499 500", "<b>≈ 50</b>"],
                    ["×10 000", "100 000", "4 999 950 000", "<b>≈ 500 000</b>"]]),
           """Gọi T là số phiên chạy cùng lúc, thì số cặp phiên là T nhân T trừ một, chia hai, vì mỗi phiên ghép với T trừ một phiên khác và mỗi cặp bị đếm hai lần. Giả sử mỗi cặp có xác suất một phần mười nghìn gây bế tắc, và số hàng nóng giữ nguyên khi tải tăng. Đây là số minh hoạ, và một trăm nghìn phiên cùng tranh hai hàng là trường hợp cực đoan. Kỳ vọng là giá trị trung bình khi lặp lại thật nhiều lần.
           Với mười phiên có bốn mươi lăm cặp, kỳ vọng chỉ không phẩy không không bốn năm cặp gây bế tắc, rất hiếm. Tải tăng một trăm lần, có gần năm trăm nghìn cặp và kỳ vọng khoảng năm mươi cặp.
           Tải tăng mười nghìn lần, khoảng năm trăm nghìn cặp.""", clear=True),
        st("""<div class="box warn"><b>Giải pháp cũ gãy ở đâu.</b> Dựa vào “bế tắc hiếm, để cơ sở dữ liệu phát hiện rồi thử lại”: ở ×1 hiếm tới mức không ai thấy, ở ×100 xảy ra vài chục lần mỗi lượt, ở ×10 000 liên tục; mỗi lần có một phiên bị huỷ rồi thử lại, càng thử càng thêm phiên chờ.</div>
<div class="box key"><b>Quy tắc khoá theo thứ tự mã tăng dần</b> xoá hẳn vòng chờ ở mọi tải. <b>Đánh đổi:</b> phải biết trước mọi hàng cần khoá để sắp thứ tự; khi chỉ biết dần trong lúc chạy thì vẫn cần hết giờ chờ và thử lại có giới hạn.</div>""",
           """Giải pháp cũ là dựa vào việc bế tắc hiếm, để cơ sở dữ liệu phát hiện rồi thử lại. Ở tải gốc nó hiếm, ở tải gấp trăm lần xảy ra vài chục lần mỗi lượt, và ở tải gấp mười nghìn lần là liên tục, càng thử lại càng thêm phiên chờ. 
           Đánh đổi là phải biết trước mọi hàng cần khoá, nếu không vẫn cần hết giờ chờ và thử lại có giới hạn.""", clear=True),
    ], checks=["10 * 9 // 2 == 45", "round(45 * 0.0001, 4) == 0.0045", "1000 * 999 // 2 == 499500", "round(499500 * 0.0001) == 50",
               "100000 * 99999 // 2 == 4_999_950_000", "round(4_999_950_000 * 0.0001) == 499995"])
    d_lab = write_lab("BNK", "L05", """# Lab BNK L05 — Thứ tự khoá cho bốn lệnh chuyển

Quy tắc chống bế tắc: **luôn khoá hàng có mã nhỏ hơn trước**, dù lệnh chuyển đi từ đâu tới đâu.

Viết chương trình `ThuTuKhoa` (tệp `ThuTuKhoa.java`). Có bốn lệnh chuyển `(từ, tới)`: `(4, 9) (9, 4) (7, 4) (4, 7)`. Với mỗi lệnh, tính mã khoá trước (nhỏ hơn) và mã khoá sau (lớn hơn) bằng `Math.min` và `Math.max`, rồi in một dòng đúng dạng:

`4 -> 9: khoa 4 roi 9`

Chạy: `javac ThuTuKhoa.java && java ThuTuKhoa`. Chấm: `bash labs/cham.sh BNK L05 ThuTuKhoa.java`.

## Phần thêm (không chấm): thấy bế tắc rồi phá nó
Thư mục `be_tac/` có sẵn `BeTac.java` đầy đủ (đúng như trong video) và `ket_qua.txt`. Cần JDK 21.
1. Chạy `cd be_tac`, rồi `javac BeTac.java && java BeTac`: dòng đầu phải ra `A roi B  va  B roi A: be tac`, dòng sau `A roi B  va  A roi B: xong`.
2. Coi `a` là hàng mã 4, `b` là hàng mã 9; lệnh 4 → 9 và lệnh 9 → 4 đi ngược chiều. **Đoán trước**: nếu cả hai lệnh áp quy tắc "khoá mã nhỏ trước" thì mỗi lệnh khoá cặp nào, và kết quả là `xong` hay `be tac`?
3. Thêm vào `main` một dòng `System.out.println("hai chieu nguoc, khoa ma nho truoc: " + thu(...));` với đúng thứ tự khoá mà bạn đoán (bốn tham số: khoá đầu và khoá sau của luồng 1, rồi của luồng 2), chạy lại và so với đoán.
""", "java", lab_tk["code"], lab_tk["out"])
    (d_lab / "be_tac").mkdir(exist_ok=True)
    (d_lab / "be_tac" / "BeTac.java").write_text(be_tac["code"] + chr(10), encoding="utf-8", newline=chr(10))
    (d_lab / "be_tac" / "ket_qua.txt").write_text(be_tac["out"] + chr(10), encoding="utf-8", newline=chr(10))
    lab = practice_scene(sc, "Tự làm: thứ tự khoá cho bốn lệnh chuyển", practice_steps(
        st, "BNK", "L05",
        """<p><b>Đề</b>: quy tắc <b>khoá mã nhỏ trước</b>. Bốn lệnh chuyển <code>(từ, tới)</code>: <code>(4,9) (9,4) (7,4) (4,7)</code>. Viết <code>ThuTuKhoa.java</code>:</p>
<ol><li>duyệt bốn lệnh</li><li>mỗi lệnh tính mã nhỏ hơn bằng <code>Math.min</code>, mã lớn hơn bằng <code>Math.max</code></li>
<li>in một dòng <code>4 -&gt; 9: khoa 4 roi 9</code></li></ol>
<p class="note">Phần thêm (không chấm): thư mục <code>be_tac/</code> của lab có <code>BeTac.java</code> để chạy và sửa thứ tự khoá.</p>""",
        """Bây giờ tới phần bạn tự làm. Có bốn lệnh chuyển, từ bốn tới chín, từ chín tới bốn, từ bảy tới bốn, và từ bốn tới bảy.
        Hãy duyệt từng lệnh, tìm số nhỏ hơn và số lớn hơn để ra thứ tự khoá, rồi in ra. Hãy dừng video, tự viết và chạy. Nếu còn sức, làm phần thêm trong thư mục thực hành.""",
        lab_tk["out"], "ThuTuKhoa.java",
        """<div class="box key"><b>Nếu kẹt:</b> khai <code>int[][] lenh = { {4, 9}, {9, 4}, {7, 4}, {4, 7} };</code> (mảng của các cặp), duyệt bằng <code>for (int[] l : lenh)</code> (<code>l</code> lần lượt là từng cặp), rồi
<code>int dau = Math.min(l[0], l[1]);</code> và <code>int sau = Math.max(l[0], l[1]);</code> (<code>l[0]</code>: số đầu của cặp, <code>l[1]</code>: số sau). Lời giải ở <code>labs/BNK/L05/loi_giai.java</code> — chỉ mở sau khi bạn đã thử.</div>""",
        """Nếu kẹt, khai một mảng gồm bốn cặp số, duyệt từng cặp, rồi lấy số nhỏ hơn làm khoá trước và số lớn hơn làm khoá sau. Trong mỗi cặp, ô số không là số đầu, ô số một là số sau. Lời giải đầy đủ nằm trong thư mục thực hành, chỉ mở sau khi tự thử.""", pause=120), "BNK", "L05")
    return lesson("L05", "plsql_khoa_hang_deadlock", "Bài 5 — PL/SQL, khoá hàng và bế tắc ORA-00060",
                  "curriculum/bnk.yaml L05; audit/bnk/verify_bnk.py L05; audit/review/screen_code/BNK.yaml (PL/SQL chạy thật trên Oracle AI Database 26ai Free 23.26 trong Docker bnx-ora; mô phỏng bế tắc bằng ReentrantLock.tryLock, JDK 21); Oracle Database Concepts (Data Concurrency and Consistency: phát hiện bế tắc, rollback một câu lệnh; khoá bảng con khi khoá ngoại không có chỉ mục); Oracle Database Error Messages (ORA-00060); thứ tự khoá của ORDER BY … FOR UPDATE: không nên giả định (khẳng định thận trọng, chưa kiểm thực nghiệm); số cặp phiên T(T−1)/2 (tổ hợp)",
                  ["Nhận ra vòng tròn chờ gây bế tắc trên đồ thị chờ", "Đếm số cặp thứ tự khoá gây bế tắc",
                   "Áp quy tắc khoá theo thứ tự id tăng dần", "Xử lý đúng khi gặp ORA-00060",
                   "Chạy PL/SQL khoá hàng theo thứ tự trên Oracle và chạy mô phỏng bế tắc",
                   "Tính số cặp phiên và số cặp ngược thứ tự kỳ vọng khi tải tăng ×100 và ×10 000"],
                  [hook, pre, sym, intu, form, ex, run, chk, pit, quiz, scale, lab, rec],
                  covers=[(1, "intuition"), (2, "check"), (3, "practice"), (4, "pitfalls"), (5, "chay_that"), (6, "quy_mo")], intro={('chay_that', 0): ['bnk_docker'], ('check', 2): ['bnk_initrans'], ('quy_mo', 0): ['bnk_ky_vong']})
