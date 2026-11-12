from lib import *

# ── Mã hiện trên màn hình (chạy NGUYÊN VĂN ở audit/bnx/ver/l12.py và cổng screen_code) ──
LIMIT_PY = """HAN_MUC = 100_000_000   # theo Thông tư 40/2024; kiểm lại văn bản
giao_dich = [30_000_000, 45_000_000, 20_000_000, 10_000_000]
da_dung = 0
for so_tien in giao_dich:
    if da_dung + so_tien > HAN_MUC:
        print("từ chối", so_tien, "đã dùng", da_dung)
    else:
        da_dung += so_tien
        print("chấp nhận", so_tien, "đã dùng", da_dung)"""
LIMIT_OUT = """chấp nhận 30000000 đã dùng 30000000
chấp nhận 45000000 đã dùng 75000000
chấp nhận 20000000 đã dùng 95000000
từ chối 10000000 đã dùng 95000000"""

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
print(vi, "tổng ví", sum(vi.values()), "đảm bảo", bao_dam)"""
REPLAY_OUT = "{'A': 1200000, 'B': 300000, 'C': 500000} tổng ví 2000000 đảm bảo 2000000"

TAX_PY = """ngan_hang = {"R1": 1_500_000, "R2": 2_000_000, "R3": 800_000}
kho_bac = {"R1": 1_500_000, "R3": 800_000}
for so_tc, tien in ngan_hang.items():
    if so_tc not in kho_bac:
        print(so_tc, "chưa sang Kho bạc: phải tra soát")
    elif kho_bac[so_tc] != tien:
        print(so_tc, "lệch số tiền")
    else:
        print(so_tc, "khớp")"""
TAX_OUT = """R1 khớp
R2 chưa sang Kho bạc: phải tra soát
R3 khớp"""

NOTE_ILL = "<span class='note'>(mọi số tiền trong bài là số minh hoạ)</span>"
NOTE_TT40 = "<span class='note'>(văn bản hiện hành, kiểm lại trước khi áp dụng)</span>"


def build():
    hook = sc("hook", "hook", "Ví hiện 2 000 000 đồng: tiền đó nằm ở đâu?", [
        st(f"""<p>Bạn nạp <b>2 000 000 đồng</b> từ tài khoản ngân hàng vào ví điện tử. Ứng dụng ví hiện số dư 2 000 000.</p>
<div class="box key">Nếu máy chủ của tổ chức ví hỏng cả ngày, 2 000 000 đó <b>nằm ở đâu</b>? Và khi nộp thuế qua ngân hàng, ngày nào được tính là <b>đã nộp</b>, và ngân hàng còn phải làm gì sau khi trích tiền?</div>
{NOTE_ILL}""",
           """Chào bạn, giả sử bạn nạp hai triệu đồng từ tài khoản ngân hàng vào ví điện tử, và ứng dụng ví hiện số dư hai triệu.
           Nếu máy chủ của tổ chức ví hỏng cả ngày, thì hai triệu đó nằm ở đâu? Và khi nộp thuế qua ngân hàng, ngày nào được tính là đã nộp, và ngân hàng còn phải làm gì sau khi trích tiền?
           Mọi số tiền trong bài là số minh hoạ.""",
           focus=[1, 2, 2, 3]),
        st(table(["câu hỏi", "phần trả lời trong bài"],
                 [["tiền thật nằm ở đâu", "tài khoản đảm bảo thanh toán của tổ chức ví, mở tại ngân hàng"],
                  ["nạp, rút, chuyển ghi sổ thế nào", "bút toán ở sổ ngân hàng và sổ ví"],
                  ["cuối ngày kiểm gì", "tài khoản đảm bảo không thấp hơn tổng số dư ví"],
                  ["một tháng được dùng bao nhiêu", "cộng dồn, từ chối giao dịch làm vượt hạn mức"],
                  ["nộp thuế: ngày nào là đã nộp, ngân hàng xong việc khi nào", "ngày ngân hàng trích tiền, ghi trên chứng từ; ngân hàng xong khi chứng từ đã sang phía Kho bạc và đối soát khớp số tham chiếu"]]),
           """Bài này trả lời năm câu hỏi. Tiền thật nằm ở tài khoản nào. Nạp, rút và chuyển tiền được ghi vào những cuốn sổ nào.
           Cuối ngày phải kiểm điều gì. Một tháng được dùng ví bao nhiêu. Và khi nộp thuế qua ngân hàng, ngày nào là ngày đã nộp, còn ngân hàng xong việc khi nào.""",
           focus=[0, "1.2", "1.3", "1.4", "1.5", "1.6"]),
    ], checks=["alg.bnx_wallet_run(0, {'A': 0}, [('nap', 'A', 2000000)])[1]['A'] == 2000000",
               "alg.bnx_wallet_run(0, {'A': 0}, [('nap', 'A', 2000000)])[0] == 2000000"])

    pre = sc("prereq", "prereq", "Trước hết: bốn điều cần hiểu", [
        st(table(["khái niệm", "nghĩa", "ví dụ"],
                 [["① Nợ và Có", "mỗi giao dịch: tổng Nợ bằng tổng Có; tài khoản tiền gửi: ghi Nợ là giảm, ghi Có là tăng", "Nợ khách 2 000 000, Có tài khoản khác 2 000 000"],
                  ["② Hai cuốn sổ", "ngân hàng ghi số dư tài khoản; tổ chức ví ghi sổ ví: mỗi khách có bao nhiêu trong ví", "tài khoản 3 000 000; ví 2 000 000"],
                  ["③ Đối soát", "so hai danh sách theo một khoá chung, tìm dòng có bên này mà bên kia không có", "{R1, R2, R3} so với {R1, R3}: lệch R2"],
                  ["④ Cộng dồn", "giữ một tổng chạy, cộng thêm từng giao dịch", "30 + 45 + 20 = 95 (triệu)"]]),
           """Trước hết ta cần hiểu bốn điều. Ở bài trước, mỗi giao dịch ghi Nợ và Có với tổng bằng nhau, và với tài khoản tiền gửi thì ghi Nợ là giảm, ghi Có là tăng.
           Hôm nay có hai cuốn sổ. Ngân hàng ghi số dư tài khoản, còn tổ chức ví ghi sổ ví, tức mỗi khách có bao nhiêu trong ví.
           Đối soát là so hai danh sách theo một khoá chung để tìm dòng bên này có mà bên kia không có.
           Cộng dồn là giữ một tổng chạy và cộng thêm từng giao dịch.""",
           focus=[0, "1.2", "1.3", "1.3", "1.4", "1.5"]),
        st("""$$30 + 45 + 20 = 95 \\text{ triệu đồng}$$""",
           """Một ví dụ số cho cộng dồn. Ba mươi triệu cộng bốn mươi lăm triệu cộng hai mươi triệu, bằng chín mươi lăm triệu đồng. Ta sẽ dùng lại con số này khi kiểm hạn mức."""),
    ], checks=["alg.bnx_tax_recon({'R1': 1, 'R2': 1, 'R3': 1}, {'R1': 1, 'R3': 1})['chua_sang'] == ['R2']",
               "alg.bnx_monthly_limit([30, 45, 20], 10**9)[-1][2] == 95",
               "5000000 - 2000000 == 3000000"])

    sym = sc("sym", "symbol", "Giải mã từ ngữ và văn bản pháp lý", [
        st(table(["từ", "nghĩa"],
                 [["tổ chức ví", "tổ chức cung ứng dịch vụ ví điện tử: giữ sổ ví; tiền của các ví nằm ở tài khoản đảm bảo"],
                  ["tài khoản đảm bảo thanh toán", "tài khoản của tổ chức ví mở tại ngân hàng: nơi tiền thật của mọi ví nằm"],
                  ["tài khoản liên kết", "tài khoản thanh toán hoặc thẻ ghi nợ <b>của chính khách</b>, dùng để nạp và rút"],
                  ["hạn mức tháng", "tổng giá trị giao dịch tối đa trong một tháng"],
                  ["mã định danh khoản phải nộp (ID)", "mã gắn với một khoản thuế phải nộp, lấy từ cổng thuế"],
                  ["số tham chiếu", "số do ngân hàng tạo cho chứng từ nộp ngân sách, đi kèm số tiền sang phía Kho bạc"]]),
           """Bảng này giải mã sáu từ. Tổ chức ví là tổ chức cung ứng dịch vụ ví điện tử, giữ sổ ví, còn tiền của các ví nằm ở tài khoản đảm bảo.
           Tài khoản đảm bảo thanh toán là tài khoản của tổ chức ví mở tại ngân hàng, nơi tiền thật của mọi ví nằm.
           Tài khoản liên kết là tài khoản thanh toán hoặc thẻ ghi nợ của chính khách, dùng để nạp và rút. Hạn mức tháng là tổng giá trị giao dịch tối đa trong một tháng.
           Mã định danh khoản phải nộp gắn với một khoản thuế, lấy từ cổng thuế. Số tham chiếu do ngân hàng tạo cho chứng từ nộp ngân sách, đi kèm số tiền sang phía Kho bạc.""",
           focus=[0, "1.2", "1.3", "1.4", "1.5", "1.6", "1.7"]),
        st(table(["văn bản", "điều bài dùng"],
                 [["Nghị định 52/2024/NĐ-CP (hiệu lực 01/7/2024)", "tổng số dư tài khoản đảm bảo thanh toán <b>không thấp hơn</b> tổng số dư các ví đã phát hành; chỉ cho dùng ví có liên kết tài khoản thanh toán hoặc thẻ ghi nợ của chính khách"],
                  ["Thông tư 40/2024/TT-NHNN", f"tổng giao dịch qua các ví cá nhân của một khách tại một tổ chức tối đa 100 triệu đồng/tháng {NOTE_TT40} <span class='note'>(tính chuyển tiền và thanh toán; không tính rút về tài khoản liên kết của chính mình)</span>"],
                  ["Thông tư 41/2025/TT-NHNN (hiệu lực 05/11/2025)", "cho phép <b>thêm</b> một hạn mức riêng, không quá 300 triệu đồng/tháng, cho <b>một số</b> khoản thanh toán thiết yếu (dịch vụ công, điện, nước, học phí, viện phí…)"],
                  ["Thông tư 19/2021/TT-BTC", "nộp thuế điện tử: mã định danh khoản phải nộp; ngân hàng tạo số tham chiếu, chuyển cùng số tiền sang ngân hàng nơi Kho bạc mở tài khoản"],
                  ["Luật Quản lý thuế 38/2019/QH14, Điều 58", "nộp không bằng tiền mặt: ngày đã nộp thuế là ngày ngân hàng trích tiền từ tài khoản người nộp và được ghi nhận trên chứng từ nộp tiền thuế"]]),
           """Năm văn bản này là căn cứ của bài. Nghị định năm mươi hai năm hai nghìn không trăm hai mươi tư nói tổng số dư tài khoản đảm bảo không thấp hơn tổng số dư các ví. Nghị định này cũng chỉ cho dùng ví có liên kết tài khoản của chính khách.
           Theo Thông tư bốn mươi năm hai nghìn không trăm hai mươi tư, tổng giao dịch qua các ví cá nhân của một khách tại một tổ chức tối đa một trăm triệu đồng một tháng.
           Hạn mức này tính chuyển tiền và thanh toán, không tính tiền rút về tài khoản liên kết của chính mình. Thông tư bốn mươi mốt năm hai nghìn không trăm hai mươi lăm cho phép thêm một hạn mức riêng, không quá ba trăm triệu, cho một số khoản thanh toán thiết yếu.
           Thông tư mười chín năm hai nghìn không trăm hai mươi mốt quy định cách nộp thuế điện tử, có mã định danh khoản phải nộp và số tham chiếu.
           Luật Quản lý thuế năm hai nghìn không trăm mười chín, Điều năm mươi tám, quy định ngày đã nộp thuế khi nộp không bằng tiền mặt.
           Đó là ngày ngân hàng trích tiền từ tài khoản người nộp và được ghi trên chứng từ nộp tiền thuế.""",
           focus=[0, "1.2", "1.2", "1.3", "1.3", "1.4", "1.5", "1.6", "1.6"], clear=True),
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
               arrow(725, 310, 815, 140, "#9333ea", dash=True),
               txt(750, 455, "Cuối ngày: tài khoản đảm bảo 2 500 000 không thấp hơn tổng ví 2 500 000", 24, "middle", "#1f2937", True)),
           """Hình cho thấy hai cuốn sổ. Bên trái là ngân hàng, nơi có tiền thật. Khi khách A nạp hai triệu, tài khoản của A giảm từ năm triệu còn ba triệu, và tài khoản đảm bảo của tổ chức ví tăng từ năm trăm nghìn lên hai triệu năm trăm nghìn.
           Bên phải là sổ của tổ chức ví, chỉ ghi ai có bao nhiêu. Ví A tăng từ không lên hai triệu, nên tổng ví cũng thành hai triệu năm trăm nghìn.
           Cuối ngày, tài khoản đảm bảo không được thấp hơn tổng ví."""),
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
               txt(750, 410, "Ngày đã nộp thuế = ngày ngân hàng trích tiền, ghi trên chứng từ (Luật Quản lý thuế, Điều 58)", 22, "middle", "#1f2937", True),
               txt(750, 448, "Chứng từ chưa sang phía Kho bạc thì ngân hàng CHƯA xong việc: phải tra soát, xử lý", 22, "middle", "#dc2626", True)),
           """Hình thứ hai là luồng nộp thuế điện tử. Người nộp chọn khoản phải nộp trên cổng thuế, mỗi khoản có một mã định danh.
           Ngân hàng trích nợ tài khoản của người nộp và tạo số tham chiếu cho chứng từ. Rồi ngân hàng chuyển số tiền cùng số tham chiếu sang ngân hàng nơi Kho bạc mở tài khoản.
           Hai bên đối soát theo số tham chiếu. Theo Luật Quản lý thuế, ngày đã nộp là ngày ngân hàng trích tiền và ghi trên chứng từ. Nhưng chứng từ chưa sang phía Kho bạc thì ngân hàng vẫn chưa xong việc, phải tra soát và xử lý."""),
    ])

    form = sc("formula", "formula", "Suy ra từng bước: nạp, chuyển, rút, bất biến, hạn mức, thuế", [
        st(table(["Bước 1: nạp 2 000 000", "sổ ngân hàng", "sổ ví"],
                 [["ghi", "Nợ tài khoản khách A 2 000 000; Có tài khoản đảm bảo 2 000 000", "ví A tăng 2 000 000"],
                  ["vì sao", "tiền thật rời tài khoản của khách sang tài khoản đảm bảo", "tổ chức ví nợ khách thêm 2 000 000"]]),
           """Bước một là nạp hai triệu. Ở sổ ngân hàng, ghi Nợ tài khoản khách A hai triệu và ghi Có tài khoản đảm bảo hai triệu, vì tiền thật rời tài khoản của khách sang tài khoản đảm bảo.
           Ở sổ ví, ví A tăng hai triệu, vì tổ chức ví nay nợ khách thêm hai triệu. Làm thử, tổng Nợ hai triệu bằng tổng Có hai triệu.""",
           focus=[0, "1.2", "1.2", "1.3"]),
        st(table(["Bước 2: ví A chuyển ví B 800 000", "sổ ngân hàng", "sổ ví"],
                 [["ghi", "không có bút toán", "ví A giảm 800 000; ví B tăng 800 000"],
                  ["vì sao", "hai ví cùng một tổ chức: tiền thật vẫn nằm yên ở tài khoản đảm bảo", "tổng ví không đổi"]]),
           """Bước hai, ví A chuyển cho ví B tám trăm nghìn. Sổ ngân hàng không có bút toán nào, vì hai ví cùng một tổ chức nên tiền thật vẫn nằm yên ở tài khoản đảm bảo.
           Sổ ví ghi ví A giảm tám trăm nghìn, ví B tăng tám trăm nghìn, nên tổng ví không đổi.""",
           focus=[0, "1.3", "1.2"], clear=True),
        st(table(["Bước 3: ví B rút 500 000", "sổ ngân hàng", "sổ ví"],
                 [["ghi", "Nợ tài khoản đảm bảo 500 000; Có tài khoản khách B 500 000", "ví B giảm 500 000"],
                  ["vì sao", "tiền thật ra khỏi tài khoản đảm bảo, về tài khoản liên kết của B", "tổ chức ví bớt nợ B 500 000"]]),
           """Bước ba, ví B rút năm trăm nghìn về tài khoản liên kết. Ở sổ ngân hàng, ghi Nợ tài khoản đảm bảo năm trăm nghìn và ghi Có tài khoản khách B năm trăm nghìn, vì tiền thật ra khỏi tài khoản đảm bảo.
           Ở sổ ví, ví B giảm năm trăm nghìn. Đây đúng là bút toán ngược của phép nạp.""",
           focus=[0, "1.2", "1.2", 0], clear=True),
        st("""<p><b>Bước 4.</b> Nạp và rút đổi tài khoản đảm bảo và tổng ví <b>cùng một lượng</b>; chuyển ví → ví không đổi cả hai. Vì vậy hiệu giữ nguyên qua mọi giao dịch đúng:</p>
$$\\text{đảm bảo} - \\text{tổng ví} \\geq 0$$
<span class='note'>Làm thử: đầu ngày 500 000 − 500 000 = 0; sau ba bước 2 000 000 − 2 000 000 = 0. Hiệu đổi mà không có giao dịch giải thích được là có lỗi.</span>""",
           """Bước bốn là bất biến. Nạp và rút làm tài khoản đảm bảo và tổng ví thay đổi cùng một lượng, còn chuyển ví sang ví không đổi cả hai.
           Vì vậy hiệu giữa tài khoản đảm bảo và tổng ví giữ nguyên qua mọi giao dịch đúng, và phải lớn hơn hoặc bằng không.
           Làm thử, đầu ngày năm trăm nghìn trừ năm trăm nghìn bằng không, sau ba bước hai triệu trừ hai triệu vẫn bằng không. Nếu hiệu đổi mà không có giao dịch nào giải thích được, là có lỗi.""",
           focus=[1, 1, 2, 3, 3], clear=True),
        st(code(LIMIT_PY) + out(LIMIT_OUT, "Bước 5 — kết quả chạy thật: cộng dồn, từ chối giao dịch làm vượt"),
           """Bước năm là hạn mức tháng. Chương trình Python giữ tổng đã dùng trong tháng, và trước mỗi giao dịch kiểm xem cộng thêm có vượt một trăm triệu không.
           Ba giao dịch đầu được chấp nhận, tổng chạy lên chín mươi lăm triệu, đúng con số cộng dồn lúc nãy.
           Giao dịch thứ tư chỉ mười triệu nhưng bị từ chối, vì chín mươi lăm cộng mười là một trăm lẻ năm triệu, vượt hạn mức.""",
           focus=[2, "1.5", "3.3", "3.4"], clear=True),
        st(code(TAX_PY, "Bước 6. Nộp thuế: đối soát theo số tham chiếu (R1, R2, R3 là nhãn minh hoạ)") + out(TAX_OUT),
           """Bước sáu là đối soát nộp thuế. Hai danh sách được so theo số tham chiếu, ở đây ghi tạm là R một, R hai, R ba, không phải cấu trúc số thật.
           Ngân hàng đã trích tiền cả ba chứng từ, nhưng phía Kho bạc mới có R một và R ba.
           Vì vậy máy báo R hai chưa sang phía Kho bạc, nên ngân hàng chưa xong việc và phải tra soát, dù ngày đã nộp của người nộp vẫn là ngày trích tiền. Thực tế còn phải so cả chiều ngược lại.""",
           focus=[1, ["2.1", "2.2"], ["2.1", "2.2"], "4.2", 0], clear=True),
    ], checks=["alg.bnx_wallet_run(500000, {'A': 0, 'B': 0, 'C': 500000}, [('nap', 'A', 2000000)])[3] == [('tiền gửi khách A', 'đảm bảo thanh toán', 2000000)]",
               "(lambda r: r[0] == 2500000 and sum(r[1].values()) == 2500000)(alg.bnx_wallet_run(500000, {'A': 0, 'B': 0, 'C': 500000}, [('nap', 'A', 2000000), ('chuyen', 'A', 'B', 800000)]))",
               "alg.bnx_wallet_run(500000, {'A': 0, 'B': 0, 'C': 500000}, [('nap', 'A', 2000000), ('chuyen', 'A', 'B', 800000)])[3] == [('tiền gửi khách A', 'đảm bảo thanh toán', 2000000)]",
               "alg.bnx_wallet_run(2500000, {'A': 1200000, 'B': 800000, 'C': 500000}, [('rut', 'B', 500000)])[3] == [('đảm bảo thanh toán', 'tiền gửi khách B', 500000)]",
               "alg.bnx_invariant(500000, {'C': 500000})[2] == 0 and alg.bnx_invariant(2000000, [500000, 1200000, 300000])[2] == 0",
               "alg.bnx_monthly_limit([30_000_000, 45_000_000, 20_000_000, 10_000_000], 100_000_000) == [(30000000, True, 30000000), (45000000, True, 75000000), (20000000, True, 95000000), (10000000, False, 95000000)]",
               "95_000_000 + 10_000_000 > 100_000_000",
               "alg.bnx_tax_recon({'R1': 1500000, 'R2': 2000000, 'R3': 800000}, {'R1': 1500000, 'R3': 800000}) == {'khop': ['R1', 'R3'], 'chua_sang': ['R2'], 'lech_tien': [], 'thua': []}"])

    ex = sc("example", "example", "Ví dụ một ngày của ba ví, từng phép tính", [
        st(f"""<p>Đầu ngày: tài khoản khách A <b>5 000 000</b>; ví A 0, ví B 0, ví C <b>500 000</b>; tài khoản đảm bảo <b>500 000</b>. {NOTE_ILL}</p>
$$① \\; \\text{{nạp: }} 5\\,000\\,000 - 2\\,000\\,000 = \\hl{{3\\,000\\,000}};\\quad 500\\,000 + 2\\,000\\,000 = \\hl{{2\\,500\\,000}}$$""",
           """Ta theo dõi một ngày. Đầu ngày, tài khoản khách A có năm triệu, ví A và ví B bằng không, ví C năm trăm nghìn, tài khoản đảm bảo năm trăm nghìn.
           Phép tính thứ nhất, A nạp hai triệu. Tài khoản của A còn năm triệu trừ hai triệu, bằng ba triệu. Tài khoản đảm bảo thành năm trăm nghìn cộng hai triệu, bằng hai triệu năm trăm nghìn, và ví A bằng hai triệu."""),
        st("""<p>Dùng lại ví A = 2 000 000 ở phép ①.</p>
$$② \\; \\text{A chuyển B: } 2\\,000\\,000 - 800\\,000 = \\hl{1\\,200\\,000};\\quad \\text{ví B} = 800\\,000$$""",
           """Phép tính thứ hai, dùng lại ví A hai triệu. A chuyển cho B tám trăm nghìn, ví A còn một triệu hai trăm nghìn, ví B có tám trăm nghìn. Tài khoản đảm bảo vẫn hai triệu năm trăm nghìn."""),
        st("""$$③ \\; \\text{B rút: } 800\\,000 - 500\\,000 = \\hl{300\\,000};\\quad 2\\,500\\,000 - 500\\,000 = \\hl{2\\,000\\,000}$$""",
           """Phép tính thứ ba, B rút năm trăm nghìn. Ví B còn tám trăm nghìn trừ năm trăm nghìn, bằng ba trăm nghìn. Tài khoản đảm bảo còn hai triệu năm trăm nghìn trừ năm trăm nghìn, bằng hai triệu."""),
        st("""$$④ \\; \\text{tổng ví} = 500\\,000 + 1\\,200\\,000 + 300\\,000 = \\hl{2\\,000\\,000}$$""",
           """Phép tính thứ tư, cộng ba ví C, A và B, năm trăm nghìn cộng một triệu hai trăm nghìn cộng ba trăm nghìn, bằng hai triệu."""),
        st("""$$⑤ \\; 2\\,000\\,000 \\geq 2\\,000\\,000 \\;\\Rightarrow\\; \\hlg{\\text{đạt, phần dư } 0}$$""",
           """Phép tính thứ năm, tài khoản đảm bảo hai triệu lớn hơn hoặc bằng tổng ví hai triệu, suy ra bất biến đạt, phần dư bằng không. Ba ví này cần tài khoản đảm bảo ít nhất hai triệu."""),
    ], checks=["alg.bnx_wallet_run(500000, {'A': 0, 'B': 0, 'C': 500000}, [('nap', 'A', 2000000)], {'A': 5000000})[2]['A'] == 3000000",
               "alg.bnx_wallet_run(500000, {'A': 0, 'B': 0, 'C': 500000}, [('nap', 'A', 2000000)])[0] == 2500000",
               "alg.bnx_wallet_run(500000, {'A': 0, 'B': 0, 'C': 500000}, [('nap', 'A', 2000000), ('chuyen', 'A', 'B', 800000)])[1] == {'A': 1200000, 'B': 800000, 'C': 500000}",
               "(lambda r: r[1]['B'] == 300000 and r[0] == 2000000)(alg.bnx_wallet_run(500000, {'A': 0, 'B': 0, 'C': 500000}, [('nap', 'A', 2000000), ('chuyen', 'A', 'B', 800000), ('rut', 'B', 500000)]))",
               "alg.bnx_invariant(2000000, [500000, 1200000, 300000]) == (True, 2000000, 0)"])

    chk = sc("check", "check", "Tự kiểm bằng đường khác: chạy lại cả nhật ký từ đầu ngày", [
        st(code(REPLAY_PY) + out(REPLAY_OUT, "Kết quả chạy thật: chạy lại nhật ký, không đọc số dư đã lưu"),
           """Kiểm bằng đường khác. Thay vì tin các số dư đã tính tay, ta cho Python chạy lại cả nhật ký từ số đầu ngày.
           Mỗi dòng nhật ký là một bộ, phần tử số không là loại giao dịch; chuyển ví sang ví chỉ đổi hai ví, còn nạp và rút đổi cả ví lẫn tài khoản đảm bảo.
           Máy in ví A một triệu hai trăm nghìn, ví B ba trăm nghìn, ví C năm trăm nghìn, tổng hai triệu, tài khoản đảm bảo hai triệu, khớp với tính tay.""",
           focus=[2, "1.1", ["1.5", "1.9"], 3]),
        st(table(["cách tính", "tài khoản đảm bảo", "tổng ví"],
                 [["tính tay ở phép ③ và ④", "2 000 000", "2 000 000"],
                  ["chạy lại nhật ký", "500 000 + 2 000 000 − 500 000 = 2 000 000", "2 000 000"],
                  ["sổ ngân hàng: Có trừ Nợ của tài khoản đảm bảo", "2 000 000 − 500 000 = 1 500 000 trong ngày, cộng 500 000 đầu ngày", "—"]]),
           """Bảng này đặt ba cách tính cạnh nhau. Tính tay cho tài khoản đảm bảo hai triệu và tổng ví hai triệu. Chạy lại nhật ký cũng ra năm trăm nghìn cộng hai triệu trừ năm trăm nghìn, bằng hai triệu.
           Cách thứ ba đọc sổ ngân hàng. Trong ngày tài khoản đảm bảo có hai triệu bên Có và năm trăm nghìn bên Nợ, nên tăng một triệu năm trăm nghìn. Cộng năm trăm nghìn đầu ngày là hai triệu.""",
           focus=[0, "1.2", "1.3", "1.4", "1.4", "1.4"], clear=True),
    ], checks=["(lambda r: r[0] == 2000000 and r[1] == {'A': 1200000, 'B': 300000, 'C': 500000})(alg.bnx_wallet_run(500000, {'A': 0, 'B': 0, 'C': 500000}, [('nap', 'A', 2000000), ('chuyen', 'A', 'B', 800000), ('rut', 'B', 500000)]))",
               "500000 + sum(a if cr == 'đảm bảo thanh toán' else -a for dr, cr, a in alg.bnx_wallet_run(500000, {'A': 0, 'B': 0, 'C': 500000}, [('nap', 'A', 2000000), ('chuyen', 'A', 'B', 800000), ('rut', 'B', 500000)])[3]) == 2000000",
               "2000000 - 500000 == 1500000 and 1500000 + 500000 == 2000000"])

    pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st("""<div class="box warn"><b>Lỗi 1 (người mới).</b> Nghĩ tiền “nằm trong ví” hay trong máy chủ của ứng dụng. Tiền thật nằm ở <b>tài khoản đảm bảo thanh toán tại ngân hàng</b>; sổ ví chỉ ghi tổ chức ví đang nợ mỗi khách bao nhiêu.
<br><span class="note">Phép thử: hỏi “số này khớp với số dư tài khoản nào ở ngân hàng?”</span></div>""",
           """Lỗi thứ nhất, của người mới, là nghĩ tiền nằm trong ví hay trong máy chủ của ứng dụng. Tiền thật nằm ở tài khoản đảm bảo thanh toán tại ngân hàng.
           Sổ ví chỉ ghi tổ chức ví đang nợ mỗi khách bao nhiêu. Phép thử là hỏi số này khớp với số dư tài khoản nào ở ngân hàng."""),
        st("""<div class="box warn"><b>Lỗi 2 (người đã đi làm).</b> Ghi tăng sổ ví <b>trước</b> khi ngân hàng xác nhận đã trích nợ. Lệnh nạp 1 000 000 hết giờ chờ, ngân hàng thật ra chưa trích, nhưng ví đã cộng:</div>
$$2\\,000\\,000 + 1\\,000\\,000 = 3\\,000\\,000 \\;>\\; 2\\,000\\,000 \\;\\Rightarrow\\; \\text{thiếu } 1\\,000\\,000$$
<span class="note">Phép thử: đối soát cuối ngày bắt được. Cách chữa: chỉ cộng ví khi có xác nhận; hỏi lại trạng thái lệnh hết giờ chờ.</span>""",
           """Lỗi thứ hai, của người đã đi làm, là ghi tăng sổ ví trước khi ngân hàng xác nhận đã trích nợ. Ví dụ lệnh nạp một triệu bị hết giờ chờ, ngân hàng thật ra chưa trích, nhưng ví đã cộng.
           Tổng ví thành hai triệu cộng một triệu, bằng ba triệu, lớn hơn tài khoản đảm bảo hai triệu, nên thiếu một triệu.
           Đối soát cuối ngày bắt được lỗi này. Cách chữa là chỉ cộng ví khi có xác nhận, và hỏi lại trạng thái của lệnh bị hết giờ chờ.""",
           focus=[1, 1, 2, 3, 3], clear=True),
        st(f"""<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> Viết cứng <code>100_000_000</code> trong mã. Khi Thông tư 41/2025 cho thêm hạn mức riêng tới 300 triệu cho <b>một số</b> khoản thanh toán thiết yếu, hệ thống từ chối sai, hoặc sửa vội thành 300 triệu cho mọi loại.
<br><span class="note">Cách chữa: hạn mức là cấu hình gắn văn bản, ngày hiệu lực và loại giao dịch {NOTE_TT40}.</span></div>""",
           """Lỗi thứ ba, cũng của người đã đi làm, là viết cứng một trăm triệu trong mã. Thông tư bốn mươi mốt năm hai nghìn không trăm hai mươi lăm cho thêm hạn mức riêng tới ba trăm triệu cho một số khoản thanh toán thiết yếu. Khi đó hệ thống từ chối sai, hoặc bị sửa vội thành ba trăm triệu cho mọi loại.
           Cách chữa là để hạn mức thành cấu hình gắn với văn bản, ngày hiệu lực và loại giao dịch, và luôn kiểm lại văn bản hiện hành.""",
           clear=True),
    ], checks=["alg.bnx_invariant(2000000, [2000000 + 1000000]) == (False, 3000000, -1000000)",
               "[x[1] for x in alg.bnx_monthly_limit([95_000_000, 10_000_000], 100_000_000)] == [True, False]",
               "[x[1] for x in alg.bnx_monthly_limit([95_000_000, 10_000_000], 300_000_000)] == [True, True]"])

    quiz = sc("quiz", "quiz", "Đến lượt bạn", [
        st(table(["câu", "đề"],
                 [["1", "Ba ví 700 000, 900 000, 400 000; tài khoản đảm bảo 1 900 000. Bất biến có đạt không, lệch bao nhiêu?"],
                  ["2", "Hạn mức 100 000 000/tháng, đã dùng 92 000 000. Giao dịch 10 000 000 có được không? Còn dùng tối đa bao nhiêu?"],
                  ["3", "Quyết định: đối soát cuối ngày thấy chứng từ R2 đã trích tiền nhưng phía Kho bạc chưa có. Ngân hàng chuyển lại R2 ngay, hay tra soát với phía Kho bạc trước rồi mới xử lý?"]]),
           """Đến lượt bạn. Câu một, ba ví có bảy trăm nghìn, chín trăm nghìn và bốn trăm nghìn, tài khoản đảm bảo một triệu chín trăm nghìn. Bất biến có đạt không, lệch bao nhiêu?
           Câu hai, hạn mức một trăm triệu một tháng, đã dùng chín mươi hai triệu. Giao dịch mười triệu có được không, và còn dùng tối đa bao nhiêu?
           Câu ba, đối soát cuối ngày thấy chứng từ R hai đã trích tiền nhưng phía Kho bạc chưa có. Ngân hàng nên chuyển lại ngay, hay tra soát với phía Kho bạc trước rồi mới xử lý? Hãy dừng video và làm ra giấy.""",
           pause=25),
        st("""$$700\\,000 + 900\\,000 + 400\\,000 = 2\\,000\\,000 \\;>\\; 1\\,900\\,000 \\;\\Rightarrow\\; \\hl{\\text{không đạt, thiếu } 100\\,000}$$""",
           """Đáp án câu một. Tổng ví bằng bảy trăm nghìn cộng chín trăm nghìn cộng bốn trăm nghìn, bằng hai triệu. Vì hai triệu lớn hơn một triệu chín trăm nghìn, nên bất biến không đạt, thiếu một trăm nghìn, phải điều tra ngay."""),
        st("""$$92 + 10 = 102 > 100 \\;\\Rightarrow\\; \\text{từ chối};\\quad 100 - 92 = \\hlg{8} \\text{ triệu còn dùng được}$$""",
           """Đáp án câu hai. Chín mươi hai cộng mười bằng một trăm lẻ hai triệu, lớn hơn một trăm triệu, nên từ chối. Tháng này khách còn dùng được tối đa một trăm trừ chín mươi hai, bằng tám triệu."""),
        st(table(["lựa chọn", "được", "mất"],
                 [["tra soát với phía Kho bạc trước, rồi chuyển lại hoặc xử lý", "không chuyển trùng nếu bên kia thật ra đã nhận mà chỉ báo trễ", "chậm hơn; trong lúc chờ, tiền chưa vào ngân sách, phải theo dõi tới khi khớp"],
                  ["chuyển lại R2 ngay", "nhanh", "nếu lần đầu thật ra đã tới, tiền bị chuyển hai lần, phải đối soát lại và hoàn trả"]]),
           """Đáp án câu ba. Chứng từ chưa sang thì tiền chưa vào ngân sách, và ngân hàng phải tra soát, xử lý cho xong.
           Tra soát trước thì không chuyển trùng nếu bên kia thật ra đã nhận mà chỉ báo trễ. Đổi lại chậm hơn, và phải theo dõi tới khi đối soát khớp.
           Chuyển lại ngay thì nhanh, nhưng nếu lần đầu thật ra đã tới, tiền bị chuyển hai lần và phải hoàn trả. Vì vậy nên tra soát trước."""),
    ], checks=["alg.bnx_invariant(1900000, [700000, 900000, 400000]) == (False, 2000000, -100000)",
               "alg.bnx_monthly_limit([92_000_000, 10_000_000], 100_000_000)[1] == (10_000_000, False, 92_000_000)",
               "100_000_000 - alg.bnx_monthly_limit([92_000_000], 100_000_000)[0][2] == 8_000_000"])

    rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        st(chain("nạp, rút: tiền thật qua tài khoản đảm bảo", "ví → ví: chỉ sổ ví đổi", "cuối ngày: đảm bảo ≥ tổng ví", "hạn mức: cộng dồn theo tháng", "thuế: ngân hàng xong khi khớp số tham chiếu"),
           """Tổng kết chuỗi logic. Nạp và rút làm tiền thật đi qua tài khoản đảm bảo. Chuyển ví sang ví chỉ đổi sổ ví.
           Cuối ngày, tài khoản đảm bảo phải lớn hơn hoặc bằng tổng ví. Hạn mức được cộng dồn theo tháng. Còn ngân hàng chỉ xong việc nộp thuế khi đối soát khớp số tham chiếu với phía Kho bạc.""",
           focus=[0, "1.1", "1.3", "1.5", "1.7", "1.9"]),
        st("""<div class='box key'><b>Tư duy:</b> con số trên màn hình chỉ là <b>ghi chép</b>. Luôn hỏi: tiền thật nằm ở tài khoản nào, ai giữ, và ai đối soát hai bên?</div>""",
           """Điều cần mang theo. Con số trên màn hình chỉ là ghi chép. Luôn hỏi tiền thật nằm ở tài khoản nào, ai giữ, và ai đối soát hai bên."""),
        st("""<p class='small'>Bài sau: đóng gói dịch vụ thành ảnh chạy được, cho đường ống tự kiểm rồi đưa lên cụm máy chủ.</p>""",
           """Ở bài sau, ta học cách đóng gói một dịch vụ thành gói chạy được ở mọi máy, cho một đường ống tự động kiểm tra, rồi đưa lên cụm máy chủ.""",
           forward_ref=True),
    ])
    return lesson("L12", "vi_dien_tu_thue_dien_tu", "Bài 12 — Ví điện tử và nộp thuế điện tử: tiền thật nằm ở đâu, bút toán và đối soát",
                  "curriculum/bnx.yaml L12; audit/bnx/verify_bnx.py L12; audit/bnx/sources.md [ND52] Nghị định 52/2024/NĐ-CP (15/5/2024, hiệu lực 01/7/2024), "
                  "[TT40] Thông tư 40/2024/TT-NHNN (nguồn thứ cấp, chưa đọc nguyên văn: ghi kiểm lại trên màn hình), [TT41] Thông tư 41/2025/TT-NHNN (05/11/2025), "
                  "[TT19] Thông tư 19/2021/TT-BTC, [LQLT58] Luật Quản lý thuế 38/2019/QH14 Điều 58 (ngày đã nộp thuế); số tiền, nhãn R1–R3 là minh hoạ; cấu trúc số tham chiếu không dạy (nguồn không nêu)",
                  ["Ghi bút toán nạp, rút, chuyển giữa ví và tài khoản ngân hàng", "Kiểm bất biến: tài khoản đảm bảo thanh toán không thấp hơn tổng số dư ví",
                   "Kiểm hạn mức giao dịch ví theo tháng", "Mô tả luồng nộp thuế điện tử qua ngân hàng và đối soát theo số tham chiếu"],
                  [hook, pre, sym, intu, form, ex, chk, pit, quiz, rec])
