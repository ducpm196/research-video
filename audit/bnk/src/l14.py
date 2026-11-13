from lib import *
from labkit import write_lab, practice_steps, practice_scene

BANK = "[('r7', 500000), ('r7b', 500000)]"
SW = "[('r7', 500000)]"


def build():
    sua = prog("SuaSaiTruHaiLan", """
CREATE TABLE ngan_hang (ma TEXT, tk TEXT, tien INTEGER);
CREATE TABLE chuyen_mach (ma TEXT, tien INTEGER);
INSERT INTO ngan_hang VALUES ('r7', 'A', -500000), ('r7b', 'A', -500000);
INSERT INTO chuyen_mach VALUES ('r7', 500000);
SELECT ma FROM ngan_hang WHERE ma NOT IN (SELECT ma FROM chuyen_mach);
SELECT 2000000 + SUM(tien) FROM ngan_hang;
INSERT INTO ngan_hang SELECT 'dao-' || ma, tk, -tien FROM ngan_hang WHERE ma = 'r7b';
SELECT 2000000 + SUM(tien) FROM ngan_hang;""", out="""r7b
1000000
1500000""", lang="sqlite")
    lab_sua = prog("SuaSaiLab", """
CREATE TABLE ngan_hang (ma TEXT, tk TEXT, tien INTEGER);
CREATE TABLE chuyen_mach (ma TEXT, tien INTEGER);
INSERT INTO ngan_hang VALUES ('r8', 'A', -800000), ('r8b', 'A', -800000), ('r8c', 'A', -800000);
INSERT INTO chuyen_mach VALUES ('r8', 800000);
SELECT ma FROM ngan_hang WHERE ma NOT IN (SELECT ma FROM chuyen_mach) ORDER BY ma;
SELECT 3000000 + SUM(tien) FROM ngan_hang;
INSERT INTO ngan_hang SELECT 'dao-' || ma, tk, -tien FROM ngan_hang WHERE ma NOT IN (SELECT ma FROM chuyen_mach);
SELECT 3000000 + SUM(tien) FROM ngan_hang;""", out="""r8b
r8c
600000
2200000""", lang="sqlite")
    hook = sc("hook", "hook", "Tình huống giả định: khách bị trừ hai lần cho một lệnh chuyển", [
        st("""<p><b>Tình huống giả định, số minh hoạ, không phải sự cố có thật.</b> Khách chuyển $500\\,000$ đồng. Ứng dụng báo lỗi mạng, khách bấm lại. Sao kê hiện <b>hai</b> khoản trừ.</p>
<div class="box key">Bài này dùng mọi thứ đã học để <b>tìm nguyên nhân, sửa cho khách, và ngăn lần sau</b>. Cuối bài là khung để bạn kể sự cố <b>thật</b> của mình.</div>""",
           """Chào bạn, đây là một tình huống giả định với số liệu minh hoạ, không phải sự cố có thật. Khách chuyển năm trăm nghìn đồng. Ứng dụng báo lỗi mạng, khách bấm lại. Sao kê hiện hai khoản trừ.
           Bài này dùng mọi thứ đã học để tìm nguyên nhân, sửa cho khách, và ngăn lần sau. Cuối bài là khung để bạn kể sự cố thật của chính mình."""),
        st(table(["bước", "việc", "kiến thức dùng"],
                 [["1", "tìm nguyên nhân", "hết giờ chờ, thử lại, lõi đã hạch toán"], ["2", "xác nhận bằng sổ", "đối soát hai bên theo mã"],
                  ["3", "hoàn tiền đúng cách", "bút toán đảo, không xoá dòng"], ["4", "ngăn lần sau", "khoá lũy đẳng, truy vấn trước khi thử lại"]]),
           """Bảng này là lộ trình bốn bước. Một, tìm nguyên nhân, dùng hiểu biết về hết giờ chờ và thử lại. Hai, xác nhận bằng sổ, dùng đối soát. Ba, hoàn tiền đúng cách, dùng bút toán đảo.
           Bốn, ngăn lần sau, dùng khoá lũy đẳng và truy vấn trước khi thử lại."""),
    ])
    pre = sc("prereq", "prereq", "Nhắc lại từ đầu: năm mảnh ghép sẽ dùng", [
        st(table(["mảnh ghép", "nghĩa", "ví dụ số"],
                 [["thử lại", "phản hồi có thể mất trên mạng, nên ứng dụng (hoặc khách) gửi lại cùng một lệnh", "1 lệnh, gửi 3 lần"],
                  ["khoá lũy đẳng", "mã duy nhất gắn với mỗi lệnh, gửi kèm mọi lần thử; máy chủ thấy khoá đã có thì không làm lại", "3 lần gửi cùng khoá → trừ 1 lần"],
                  ["hết giờ chờ", "không nhận phản hồi kịp: chưa biết lõi ngân hàng đã hạch toán (ghi vào sổ) hay chưa, phải truy vấn", "đã hạch toán mà gửi lại → ghi nợ (trừ tiền) 2 lần"]]),
           """Ôn năm mảnh ghép. Thử lại là khi phản hồi mất trên mạng, nên ứng dụng hoặc khách gửi lại cùng một lệnh.
           Khoá lũy đẳng là mã duy nhất gắn với mỗi lệnh và gửi kèm mọi lần thử. Máy chủ thấy khoá đã có thì không làm lại, nên ba lần gửi cùng khoá chỉ trừ tiền một lần.
           Hết giờ chờ nghĩa là chưa biết lõi ngân hàng đã hạch toán, tức đã ghi vào sổ hay chưa, nên phải truy vấn. Nếu đã hạch toán mà gửi lại, khách bị trừ tiền hai lần."""),
        st(table(["mảnh ghép", "nghĩa", "ví dụ số"],
                 [["đối soát", "đặt sổ ngân hàng cạnh sổ chuyển mạch (hệ thống ở giữa các ngân hàng), ghép theo mã giao dịch, chia bốn loại: khớp, lệch tiền, chỉ ngân hàng có, chỉ chuyển mạch có", "ngân hàng có r1, r2; chuyển mạch có r1 → r2 chỉ ngân hàng có"],
                  ["bút toán đảo", "sổ không được xoá dòng; sửa sai bằng một dòng mới ngược dấu", "−500 000 rồi +500 000: tổng 0"]]),
           """Đối soát là đặt sổ ngân hàng cạnh sổ của chuyển mạch, tức hệ thống ở giữa các ngân hàng, rồi ghép theo mã giao dịch và chia bốn loại. Bốn loại là khớp, lệch tiền, chỉ ngân hàng có, và chỉ chuyển mạch có.
           Bút toán đảo là cách sửa sai mà không xoá dòng nào, bằng một dòng mới ngược dấu. Ví dụ trừ năm trăm nghìn rồi cộng năm trăm nghìn, tổng bằng không.""", clear=True),
        st("""$$2 \\cdot 500\\,000 = 1\\,000\\,000$$""",
           """Một phép tính khởi động. Hai lần trừ, mỗi lần năm trăm nghìn, tổng bị trừ một triệu. Đúng ra chỉ nên trừ năm trăm nghìn."""),
    ], checks=["2 * 500000 == 1000000", "alg.bnk_retry_sim(2000000, 500000, 3, True) == 2000000 - 500000",
               "alg.bnk_reconcile([('r1', 1), ('r2', 1)], [('r1', 1)]) == (1, 1, 0, 0)", "-500000 + 500000 == 0"])
    sym = sc("sym", "symbol", "Giải mã khung kể sự cố: STAR", [
        st(table(["chữ", "nghĩa", "câu hỏi tự hỏi"],
                 [["S — Situation", "bối cảnh", "hệ thống nào, ai dùng, rủi ro gì"],
                  ["T — Task", "nhiệm vụ của bạn", "bạn chịu trách nhiệm phần nào"],
                  ["A — Action", "hành động của bạn", "bạn làm gì, từng bước, vì sao"],
                  ["R — Result", "kết quả", "thay đổi gì, đo bằng gì, học được gì"]]),
           """Khung S T A R giúp kể sự cố có cấu trúc. S là bối cảnh, hệ thống nào, ai dùng, rủi ro gì. T là nhiệm vụ của bạn, bạn chịu trách nhiệm phần nào. A là hành động, bạn làm gì, từng bước, vì sao.
           R là kết quả, thay đổi gì, đo bằng gì, học được gì."""),
    ])
    intu = sc("intuition", "intuition", "Hình dung: dòng thời gian của sự cố giả định", [
        st(svg(1500, 440,
               box(30, 60, 330, 90, ["1. khách gửi lệnh", "ngân hàng ghi nợ r7"], C_BLUE), box(400, 60, 330, 90, ["2. phản hồi mất", "ứng dụng báo lỗi"], C_RED),
               box(770, 60, 330, 90, ["3. khách bấm lại", "không có khoá lũy đẳng"], C_AMBER), box(1140, 60, 330, 90, ["4. ngân hàng ghi nợ r7b", "lần hai"], C_RED),
               arrow(360, 105, 395, 105), arrow(730, 105, 765, 105), arrow(1100, 105, 1135, 105),
               box(30, 250, 700, 90, ["chuyển mạch từ chối r7b là trùng, chỉ ghi r7", "ngân hàng không tự hoàn ghi nợ r7b"], C_GREEN, size=22),
               box(770, 250, 700, 90, ["sổ ngân hàng: trừ hai lần", "sổ chuyển mạch: một lần → LỆCH"], C_RED, bold=True),
               txt(750, 400, "đối soát cuối ngày sẽ thấy r7b chỉ có ở ngân hàng", 26, "middle", "#1f2937", True)),
           """Hình cho thấy dòng thời gian giả định. Khách gửi lệnh, ngân hàng ghi nợ r bảy. Phản hồi mất, ứng dụng báo lỗi. Khách bấm lại, và vì không có khoá lũy đẳng, ngân hàng ghi nợ lần hai là r bảy b.
           Trong tình huống giả định này, chuyển mạch từ chối lệnh thứ hai vì trùng, nhưng ngân hàng không tự hoàn lại khoản ghi nợ r bảy b, nên sổ hai bên lệch nhau.
           Nếu chuyển mạch nhận cả hai lệnh, người nhận sẽ được cộng hai lần, và việc đòi lại tiền còn khó hơn. Đối soát cuối ngày sẽ thấy r bảy b chỉ có ở ngân hàng."""),
        st(svg(1500, 440,
               box(40, 40, 640, 80, "nguyên nhân gốc: thử lại không có khoá lũy đẳng", C_RED, bold=True, size=24),
               box(40, 150, 640, 80, "khuếch đại: ứng dụng coi lỗi mạng là thất bại", C_AMBER, size=24),
               box(40, 260, 640, 80, "phát hiện chậm: chỉ thấy khi đối soát hoặc khách báo", C_AMBER, size=24),
               box(780, 40, 680, 80, ["sửa 1: khoá lũy đẳng cho mọi lệnh thay đổi tiền,", "sinh khi tạo lệnh, dùng lại khi khách bấm lại"], C_GREEN, size=20),
               box(780, 150, 680, 80, "sửa 2: hết giờ chờ thì truy vấn trạng thái, không gửi lại ngay", C_GREEN, size=22),
               box(780, 260, 680, 80, "sửa 3: cảnh báo lệch sổ gần thời gian thực", C_GREEN, size=24),
               txt(750, 400, "mỗi nguyên nhân có một biện pháp tương ứng", 26, "middle", "#1f2937", True)),
           """Hình thứ hai ghép nguyên nhân với biện pháp. Nguyên nhân gốc là thử lại không có khoá lũy đẳng. Khuếch đại là ứng dụng coi lỗi mạng là thất bại. Phát hiện chậm là chỉ thấy khi đối soát hoặc khi khách báo.
           Mỗi nguyên nhân có một biện pháp tương ứng, ở cột bên phải. Lưu ý, khoá lũy đẳng phải được sinh khi tạo lệnh, ở màn hình xác nhận, và dùng lại khi khách bấm lại.
           Nếu mỗi lần bấm sinh một khoá mới, lệnh vẫn bị trùng.""",
           clear=True),
    ])
    form = sc("formula", "formula", "Suy ra từng bước: từ triệu chứng tới cách ngăn", [
        st("""<p><b>Bước 1. Triệu chứng.</b> Khách bị trừ $2$ lần cho $1$ lệnh. Số tiền trừ dư $= (2 - 1) \\cdot 500\\,000$.</p>
<span class='note'>Làm thử: $(2 - 1) \\cdot 500\\,000 = 500\\,000$ đồng trừ dư.</span>""",
           """Bước một, triệu chứng. Khách bị trừ hai lần cho một lệnh, nên số tiền trừ dư bằng hai trừ một, nhân năm trăm nghìn. Làm thử, kết quả là năm trăm nghìn đồng trừ dư."""),
        st("""<p><b>Bước 2. Bằng chứng.</b> Đối soát theo mã: r7 có ở cả hai sổ và khớp, r7b chỉ có ở ngân hàng.</p>
<span class='note'>Làm thử: khớp $1$, chỉ ngân hàng $1$, chỉ chuyển mạch $0$, lệch tiền $0$.</span>""",
           """Bước hai, bằng chứng. Vì đối soát theo mã tách được từng giao dịch, nên r bảy có ở cả hai sổ và khớp, còn r bảy b chỉ có ở ngân hàng. Làm thử, khớp một, chỉ ngân hàng một, hai loại còn lại bằng không."""),
        st("""<p><b>Bước 3. Sửa cho khách.</b> Thêm bút toán đảo cho r7b, không xoá dòng. Số dư khách sau đảo chỉ còn bị trừ đúng $500\\,000$.</p>
<span class='note'>Làm thử:</span>
$$-500\\,000 - 500\\,000 + 500\\,000 = -500\\,000$$""",
           """Bước ba, sửa cho khách. Vì sổ không được xoá dòng, nên ta thêm bút toán đảo cho r bảy b. Sau khi đảo, khách chỉ còn bị trừ đúng năm trăm nghìn. Làm thử, âm năm trăm nghìn, âm năm trăm nghìn, cộng năm trăm nghìn, bằng âm năm trăm nghìn."""),
        st("""<p><b>Bước 4. Ngăn lần sau.</b> Cùng khoá thì chỉ một dòng; hết giờ chờ thì truy vấn trước khi thử lại.</p>
<span class='note'>Làm thử: gửi hai lần cùng khoá → $1$ dòng.</span>""",
           """Bước bốn, ngăn lần sau. Vì khoá lũy đẳng chỉ cho một dòng, và truy vấn trước giúp biết đã hạch toán chưa, nên gửi hai lần cùng khoá chỉ còn một dòng."""),
    ], checks=["(2 - 1) * 500000 == 500000", "alg.bnk_reconcile(" + BANK + ", " + SW + ") == (1, 1, 0, 0)", "-500000 - 500000 + 500000 == -500000",
               "alg.bnk_unique_key_rows(2) == 1"])
    ex = sc("example", "example", "Ví dụ bằng số, từng phép tính", [
        st("""<p>Số dư đầu $2\\,000\\,000$ đồng <i>(số minh hoạ)</i>. Không khoá, ứng dụng gửi $2$ lần.</p>
$$① \\; 2\\,000\\,000 - 2 \\cdot 500\\,000 = \\hl{1\\,000\\,000}$$""",
           """Ta tính số liệu giả định. Số dư đầu hai triệu đồng, đây là số minh hoạ. Không có khoá, ứng dụng gửi hai lần. Phép tính thứ nhất, hai triệu trừ hai nhân năm trăm nghìn, còn một triệu."""),
        st("""<p>Số dư đúng là $2\\,000\\,000 - 500\\,000 = 1\\,500\\,000$.</p>
$$② \\; 1\\,500\\,000 - 1\\,000\\,000 = \\hl{500\\,000}\\ \\text{trừ dư}$$""",
           """Phép tính thứ hai, số dư đúng phải là hai triệu trừ năm trăm nghìn, bằng một triệu năm trăm nghìn. Chênh lệch so với thực tế là năm trăm nghìn, đúng bằng số trừ dư."""),
        st("""<p>Đối soát: ngân hàng có r7 và r7b, chuyển mạch chỉ có r7.</p>
$$③ \\; \\text{chỉ ngân hàng} = 2 - 1 = \\hl{1}\\ (r7b)$$""",
           """Phép tính thứ ba, đối soát. Ngân hàng có hai mã, chuyển mạch có một mã. Mã chỉ có ở ngân hàng là hai trừ một, bằng một, và đó là r bảy b."""),
        st("""<p>Thêm bút toán đảo $+500\\,000$ cho r7b vào tài khoản khách.</p>
$$④ \\; 1\\,000\\,000 + 500\\,000 = \\hlg{1\\,500\\,000}$$""",
           """Phép tính thứ tư, thêm bút toán đảo cộng năm trăm nghìn cho r bảy b. Số dư của khách về một triệu cộng năm trăm nghìn, bằng một triệu năm trăm nghìn, đúng như một lần chuyển."""),
        st("""<p>Từ nay có khoá lũy đẳng: gửi $2$ lần cùng khoá.</p>
$$⑤ \\; 2\\,000\\,000 - 500\\,000 = \\hlg{1\\,500\\,000}\\ \\text{ngay từ đầu}$$""",
           """Phép tính thứ năm, từ nay có khoá lũy đẳng, gửi hai lần cùng khoá. Số dư đúng một triệu năm trăm nghìn ngay từ đầu, và không cần hoàn tiền."""),
    ], checks=["2000000 - 2 * 500000 == 1000000", "(2000000 - 500000) - 1000000 == 500000", "alg.bnk_reconcile(" + BANK + ", " + SW + ")[1] == 2 - 1",
               "1000000 + 500000 == 1500000 == alg.bnk_retry_sim(2000000, 500000, 2, True)", "alg.bnk_retry_sim(2000000, 500000, 2, False) == 1000000"])
    chk = sc("check", "check", "Tự kiểm bằng đường khác: sổ phải cân đối sau khi sửa", [
        st("""<p>Đường khác: dựng sổ nhiều dòng rồi hỏi cơ sở dữ liệu. Giao dịch gốc và giao dịch đảo đều phải cân đối, tức <b>không giao dịch nào lệch</b>.</p>
$$\\text{giao dịch lệch} = \\hlg{[\\ ]}$$""",
           """Kiểm bằng đường khác. Vì sổ cái cân đối theo từng giao dịch, ta dựng sổ nhiều dòng rồi hỏi cơ sở dữ liệu. Giao dịch gốc và giao dịch đảo đều cân đối, nên không giao dịch nào lệch."""),
        st(table(["kiểm tra", "kết quả mong đợi"],
                 [["mỗi giao dịch cân đối (tổng 0)", "danh sách lệch rỗng"], ["số dòng sau khi đảo", "4 dòng cũ (r7, r7b) + 2 dòng đảo = 6, không dòng nào bị xoá"],
                  ["đối soát sau sửa", "r7 khớp; r7b vẫn chỉ ngân hàng có nhưng đã có bút toán đảo đi kèm, tổng 0, nên được đóng"]]),
           """Bảng này là ba phép kiểm sau khi sửa, vì sửa xong mới cần chắc sổ đúng. Mỗi giao dịch cân đối thì danh sách lệch rỗng.
           Số dòng bằng bốn dòng cũ của r bảy và r bảy b, cộng hai dòng đảo, là sáu dòng, không dòng nào bị xoá.
           Còn đối soát lại thì r bảy khớp. R bảy b vẫn chỉ ngân hàng có, nhưng đã có bút toán đảo đi kèm với tổng bằng không, nên khoản lệch đó được đóng."""),
    ], checks=["alg.bnk_ledger_unbalanced([(1, 'khach', -500000), (1, 'nhan', 500000), (2, 'khach', -500000), (2, 'cho_tt_chuyen_mach', 500000), (3, 'khach', 500000), (3, 'cho_tt_chuyen_mach', -500000)]) == []",
               "len([(1, 'khach', -500000), (1, 'nhan', 500000), (2, 'khach', -500000), (2, 'cho_tt_chuyen_mach', 500000), (3, 'khach', 500000), (3, 'cho_tt_chuyen_mach', -500000)]) == 4 + 2 == 6",
               "-500000 + 500000 == 0"])
    pit = sc("pitfalls", "pitfall", "Lỗi hay gặp khi kể sự cố trong phỏng vấn", [
        st("""<div class="box warn"><b>Lỗi 1.</b> <b class="red">Kể sự cố không phải của mình</b> như của mình, hoặc thêm con số không có nguồn. Người phỏng vấn đào sâu hai ba lớp là lộ. Chỉ kể điều bạn thật sự làm, và con số nào cũng phải có nguồn.</div>""",
           """Lỗi thứ nhất, và nặng nhất. Kể sự cố không phải của mình như của mình, hoặc thêm con số không có nguồn. Người phỏng vấn đào sâu hai ba lớp là lộ. Chỉ kể điều bạn thật sự làm, và con số nào cũng phải có nguồn."""),
        st("""<div class="box warn"><b>Lỗi 2.</b> <b class="red">Đổ lỗi cho người hay hệ thống khác</b>. Sự cố tốt được kể bằng cơ chế và bài học, không bằng đổ lỗi. Nói rõ phần bạn sai hoặc chưa biết lúc đó.</div>""",
           """Lỗi thứ hai, đổ lỗi cho người hay hệ thống khác. Sự cố tốt được kể bằng cơ chế và bài học, không bằng đổ lỗi. Hãy nói rõ phần bạn sai hoặc chưa biết lúc đó."""),
        st("""<div class="box warn"><b>Lỗi 3.</b> Chỉ kể cách sửa nóng mà <b class="red">bỏ phần ngăn lặp lại</b>. Người cấp cao được đánh giá ở chỗ sự cố đó không xảy ra lần hai: khoá lũy đẳng, giám sát, đối soát.</div>""",
           """Lỗi thứ ba, chỉ kể cách sửa nóng mà bỏ phần ngăn lặp lại. Người cấp cao được đánh giá ở chỗ sự cố đó không xảy ra lần hai, bằng khoá lũy đẳng, giám sát và đối soát."""),
    ])
    quiz = sc("quiz", "quiz", "Đến lượt bạn", [
        st(table(["câu", "đề"],
                 [["1", "Số dư đầu 3 000 000, chuyển 400 000, gửi 3 lần không khoá. Bị trừ dư bao nhiêu?"],
                  ["2", "Ngân hàng có 3 mã, chuyển mạch 2 mã, cả 2 mã đều chung. Mấy mã chỉ ở ngân hàng?"],
                  ["3", "Bài tập: viết bốn câu STAR cho một sự cố THẬT của bạn."]]),
           """Đến lượt bạn. Câu một, số dư đầu ba triệu, chuyển bốn trăm nghìn, gửi ba lần không khoá, bị trừ dư bao nhiêu? Câu hai, ngân hàng có ba mã, chuyển mạch có hai mã, cả hai mã đều chung, mấy mã chỉ ở ngân hàng?
           Câu ba là bài tập, viết bốn câu S T A R cho một sự cố thật của bạn. Hãy dừng video và làm ra giấy.""",
           pause=30),
        st("""<p>Câu 1: trừ $3 \\cdot 400\\,000$ nhưng đúng ra chỉ $1 \\cdot 400\\,000$.</p>
$$(3 - 1) \\cdot 400\\,000 = \\hl{800\\,000}$$""",
           """Đáp án câu một. Bị trừ ba lần nhưng đúng ra chỉ một lần, nên trừ dư là ba trừ một, nhân bốn trăm nghìn, bằng tám trăm nghìn."""),
        st("""$$3 - 2 = \\hlg{1}\\ \\text{mã chỉ ở ngân hàng}$$""",
           """Đáp án câu hai. Ngân hàng ba mã, hai mã chung, nên còn một mã chỉ có ở ngân hàng."""),
        st("""<div class="box key"><b>Khung điền cho sự cố THẬT của bạn</b> <i>(bài này không bịa hộ bạn)</i><br>
S: [hệ thống, rủi ro] &nbsp; T: [phần bạn chịu trách nhiệm]<br>A: [các bước bạn làm, vì sao] &nbsp; R: [thay đổi đo được, nguồn số liệu, bài học]</div>""",
           """Câu ba là bài của riêng bạn, nên bài này không bịa hộ bạn. Hãy điền bối cảnh, nhiệm vụ, hành động và kết quả của một sự cố thật. Mỗi con số phải có nguồn, và nếu không nhớ chính xác thì nói rõ là ước chừng.""",
           clear=True),
    ], checks=["(3 - 1) * 400000 == 800000 == 3000000 - alg.bnk_retry_sim(3000000, 400000, 3, False) - 400000",
               "alg.bnk_reconcile([('a', 1), ('b', 1), ('c', 1)], [('a', 1), ('b', 1)])[1] == 3 - 2"])
    rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        st(chain("triệu chứng", "bằng chứng từ sổ", "sửa bằng bút toán đảo", "ngăn bằng khoá lũy đẳng"),
           """Tổng kết chuỗi logic. Bắt đầu từ triệu chứng, tìm bằng chứng từ sổ, sửa bằng bút toán đảo, và ngăn lặp lại bằng khoá lũy đẳng."""),
        st("""<div class='box key'><b>Tư duy:</b> kỹ sư cấp cao không chỉ sửa lỗi. Họ <b>giải thích cơ chế</b>, <b>chứng minh bằng dữ liệu</b>, và <b>làm cho lỗi đó không thể lặp lại</b>. Hãy kể đúng việc mình đã làm.</div>""",
           """Điều cần mang theo. Kỹ sư cấp cao không chỉ sửa lỗi. Họ giải thích cơ chế, chứng minh bằng dữ liệu, và làm cho lỗi đó không thể lặp lại. Hãy kể đúng việc mình đã làm."""),
    ])
    # ── AF2: P1 SQL tối thiểu, SQL chạy thật trên sqlite (đối soát, đảo, kiểm số dư), quy mô, tự làm ──
    add_steps([pre], "prereq", [
        st(table(["thêm một điều để đọc mã", "nghĩa", "ví dụ"],
                 [["SQL dùng trong bài", "<code>x NOT IN (SELECT …)</code>: x không nằm trong kết quả của truy vấn con; <code>INSERT INTO t SELECT …</code>: chèn mọi dòng mà truy vấn trả về; <code>'dao-' || ma</code>: nối hai chuỗi; <code>SUM(cột)</code>: cộng", "<code>'dao-' || 'r7b'</code> = <code>dao-r7b</code>"]]),
           """Thêm một điều để đọc mã SQL trong bài. Điều kiện không nằm trong cho biết một giá trị không có trong kết quả của một truy vấn con. Lệnh chèn kèm truy vấn chèn mọi dòng mà truy vấn trả về. Hai gạch đứng nối hai chuỗi. Và hàm cộng là hàm tính tổng, nó cộng mọi giá trị của một cột lại với nhau.""",
           clear=True),
    ], at=1)
    pre["title"] = "Nhắc lại từ đầu: các mảnh ghép sẽ dùng"
    run = sc("chay_that", "example", "Chạy thật: tìm lệnh trừ trùng, đảo bút toán, kiểm số dư (sqlite)", [
        st(code_block(sua, lines=(1, 4), title="Dựng hai sổ: ngân hàng ghi hai lần trừ, chuyển mạch chỉ ghi một"),
           """Ta dựng lại tình huống bằng SQL. Sổ ngân hàng của khách A có hai dòng trừ năm trăm nghìn, mã r bảy và r bảy b. Sổ chuyển mạch chỉ có một dòng, mã r bảy. Số dư đầu của A là hai triệu."""),
        st(code_block(sua, lines=(5, 8), title="Tìm dòng chỉ ngân hàng có, kiểm số dư, đảo, kiểm lại") + out_block(sua),
           """Câu thứ nhất tìm các mã có ở sổ ngân hàng mà không có ở sổ chuyển mạch. Câu thứ hai tính số dư bằng số dư đầu cộng tổng các dòng. Lệnh chèn thêm một dòng đảo, ngược dấu, cho mã r bảy b, không xoá dòng nào. Câu cuối tính lại số dư.
           Khi chạy thật, mã thừa là r bảy b. Số dư trước khi sửa là một triệu, bị trừ dư năm trăm nghìn. Sau khi đảo, số dư là một triệu năm trăm nghìn, đúng bằng hai triệu trừ năm trăm nghìn.""", clear=True),
    ])
    scale = sc("quy_mo", "example", "Quy mô: vụ trừ trùng nhỏ thành hàng nghìn người làm mỗi ngày nếu xử lý tay", [
        st("""<p>Giả sử $0{,}01\\%$ lệnh bị trừ trùng, và mỗi vụ cần $10$ phút xử lý tay (đối soát, đảo bút toán, báo khách) <i>(số minh hoạ)</i>; một người làm $8$ giờ mỗi ngày:</p>"""
           + table(["tải", "lệnh mỗi ngày", "vụ trừ trùng", "thời gian xử lý tay", "số người cần"],
                   [["×1", "100 000", "10", "100 phút", "≈ 0,2"],
                    ["×100", "10 000 000", "1 000", "≈ 167 giờ", "<b>≈ 21</b>"],
                    ["×10 000", "1 000 000 000", "100 000", "≈ 16 667 giờ", "<b>≈ 2 083</b>"]]),
           """Giả sử một phần mười nghìn số lệnh bị trừ trùng, và mỗi vụ cần mười phút xử lý tay, gồm đối soát, đảo bút toán và báo khách. Mỗi người làm tám giờ mỗi ngày. Đây là số minh hoạ.
           Với một trăm nghìn lệnh mỗi ngày, có mười vụ, chỉ một trăm phút, chưa đến một người. Tải tăng một trăm lần thì một nghìn vụ, cần khoảng hai mươi mốt người. Tải tăng mười nghìn lần thì một trăm nghìn vụ, cần khoảng hai nghìn người, mỗi ngày.""", clear=True),
        st("""<div class="box warn"><b>Giải pháp cũ gãy ở đâu.</b> Sửa từng vụ bằng tay: ở ×1 chỉ một người làm thêm, ở ×100 cần cả một nhóm, ở ×10 000 là một nhà máy; và càng nhiều người sửa tay càng dễ thêm lỗi.</div>
<div class="box key"><b>Đánh đổi:</b> phòng hơn chữa (khoá lũy đẳng, truy vấn trước khi thử lại kéo số vụ về gần 0); với vụ còn lại thì tự động hoá đối soát và đảo bút toán, nhưng đặt ngưỡng, bước duyệt và nhật ký kiểm toán để máy không tự hoàn nhầm.</div>""",
           """Câu hỏi là giải pháp cũ sẽ gãy ở chỗ nào khi tải tăng lên. Sửa từng vụ bằng tay thì ở tải gốc chỉ cần một người làm thêm. Ở tải gấp trăm lần cần cả một nhóm, và ở tải gấp mười nghìn lần là một nhà máy. Càng nhiều người sửa tay càng dễ thêm lỗi.
           Đánh đổi là phòng hơn chữa, vì khoá lũy đẳng và truy vấn trước khi thử lại kéo số vụ về gần không. Với các vụ còn lại thì tự động hoá đối soát và đảo bút toán, nhưng phải đặt ngưỡng, bước duyệt và nhật ký kiểm toán để máy không tự hoàn nhầm.""", clear=True),
    ], checks=["100000 * 0.0001 == 10", "round(10_000_000 * 0.0001) == 1000", "round(1_000_000_000 * 0.0001) == 100_000",
               "10 * 10 == 100", "round(1000 * 10 / 60) == 167", "round(100000 * 10 / 60) == 16667",
               "round(1000 * 10 / 60 / 8) == 21", "round(100000 * 10 / 60 / 8) == 2083", "round(10 * 10 / 60 / 8, 1) == 0.2"])
    write_lab("BNK", "L14", """# Lab BNK L14 — Ba lần gửi, một lần ghi chuyển mạch

Khách A có số dư đầu **3 000 000**. Sổ ngân hàng ghi **ba** dòng trừ 800 000 (mã `r8`, `r8b`, `r8c`); sổ chuyển mạch chỉ ghi một dòng, mã `r8`.

Viết tệp `sua_sai.sql` (chạy bằng `python labs/sqlrun.py sua_sai.sql`, hoặc `sqlite3 :memory: < sua_sai.sql`):
1. Tạo hai bảng `ngan_hang (ma TEXT, tk TEXT, tien INTEGER)` và `chuyen_mach (ma TEXT, tien INTEGER)`; chèn các dòng nói trên (ngân hàng: `-800000` mỗi dòng, tài khoản `'A'`; chuyển mạch: `('r8', 800000)`).
2. `SELECT` các mã có ở ngân hàng mà không có ở chuyển mạch, `ORDER BY ma`.
3. `SELECT 3000000 + SUM(tien) FROM ngan_hang;` (số dư trước khi sửa).
4. `INSERT INTO ngan_hang SELECT 'dao-' || ma, tk, -tien …` cho **đúng các mã thừa** (dùng lại điều kiện `NOT IN` ở bước 2).
5. Lại `SELECT 3000000 + SUM(tien) FROM ngan_hang;` (số dư sau khi sửa).

Chấm: `bash labs/cham.sh BNK L14 sua_sai.sql`.
""", "sql", lab_sua["code"], lab_sua["out"])
    lab = practice_scene(sc, "Tự làm: ba lần gửi, một lần ghi chuyển mạch", practice_steps(
        st, "BNK", "L14",
        """<p><b>Đề</b>: số dư đầu 3 000 000; ngân hàng trừ 800 000 ba lần (<code>r8</code>, <code>r8b</code>, <code>r8c</code>), chuyển mạch chỉ có <code>r8</code>. Viết <code>sua_sai.sql</code>:</p>
<ol><li>hai bảng và dữ liệu (chi tiết ở <code>de.md</code>)</li><li>tìm mã thừa; số dư trước khi sửa</li>
<li>đảo <b>đúng các mã thừa</b> bằng <code>INSERT … SELECT</code>; số dư sau khi sửa</li></ol>""",
        """Bây giờ tới phần bạn tự làm. Khách tên A có số dư ba triệu đồng. Sổ ngân hàng trừ tám trăm nghìn ba lần, mã r tám, r tám b và r tám c, còn sổ chuyển mạch chỉ có mã r tám. Hãy viết một tệp SQL dựng hai bảng và dữ liệu đó.
        Rồi tìm các mã thừa, tính số dư trước khi sửa, đảo đúng các mã thừa bằng lệnh chèn kèm truy vấn, và tính lại số dư. Hãy dừng video, tự viết và chạy, đừng chép lại ví dụ.""",
        lab_sua["out"], "sua_sai.sql",
        """<div class="box key"><b>Nếu kẹt:</b> mô theo ví dụ; điều kiện mã thừa là <code>ma NOT IN (SELECT ma FROM chuyen_mach)</code>, dùng cho cả câu tìm lẫn lệnh chèn đảo.
Lời giải ở <code>labs/BNK/L14/loi_giai.sql</code> — chỉ mở sau khi bạn đã thử.</div>""",
        """Nếu kẹt, làm theo ví dụ vừa xem. Điều kiện mã thừa là mã không nằm trong sổ chuyển mạch, và ta dùng đúng điều kiện đó cho cả câu tìm lẫn lệnh chèn dòng đảo. Lời giải đầy đủ nằm trong thư mục thực hành của bài, chỉ mở sau khi bạn đã tự thử.""", pause=180), "BNK", "L14")
    return lesson("L14", "tinh_huong_tru_tien_hai_lan", "Bài 14 — Tình huống giả định: từ triệu chứng tới thiết kế tốt hơn",
                  "curriculum/bnk.yaml L14; audit/bnk/verify_bnk.py L14; audit/review/screen_code/BNK.yaml (SQL chạy thật trên sqlite 3.49); tình huống giả định, số liệu minh hoạ do người soạn đặt ra (không phải sự cố có thật); dùng lại các hàm kiểm của các bài trước; tỉ lệ trừ trùng và thời gian xử lý tay trong bảng quy mô là số minh hoạ",
                  ["Đi từ triệu chứng tới nguyên nhân, bằng chứng, cách sửa và cách ngăn", "Tính số tiền trừ dư và phân loại lệch bằng đối soát",
                   "Sửa sai bằng bút toán đảo", "Kể một sự cố thật theo khung STAR, trung thực và có số liệu có nguồn",
                   "Chạy SQL tìm lệnh trừ trùng, đảo bút toán và kiểm số dư để thấy kết quả",
                   "Tính số vụ trừ trùng và nhân lực xử lý tay khi tải tăng ×100, ×10 000",
                   "Viết SQL tìm các mã thừa, đảo chúng và kiểm số dư"],
                  [hook, pre, sym, intu, form, ex, run, chk, pit, quiz, scale, lab, rec],
                  covers=[(1, "formula"), (2, "example"), (3, "chay_that"), (4, "pitfalls"), (5, "chay_that"), (6, "quy_mo"), (7, "practice")])
