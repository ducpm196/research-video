from lib import *

# ── Mã hiện trên màn hình (chạy NGUYÊN VĂN ở audit/bnx/ver/l11.py và cổng screen_code) ──
IBAN_PY = """iban = "GB82WEST12345698765432"
s = iban[4:] + iban[:4]     # đưa 4 ký tự đầu ra cuối
so = ""
for c in s:
    so += str(int(c, 36))   # chữ số giữ nguyên, A=10 … Z=35
print(s)
print(so)
print(int(so) % 97)"""
IBAN_OUT = """WEST12345698765432GB82
3214282912345698765432161182
1"""

MOD_PY = """so = "3214282912345698765432161182"
du = 0
for c in so:
    du = (du * 10 + int(c)) % 97   # chỉ giữ số dư, số luôn nhỏ
print(du)"""
MOD_OUT = "1"

FX_PY = """from decimal import Decimal, ROUND_HALF_UP
CHU_SO_LE = {"USD": 2, "VND": 0}          # ISO 4217
def tron(x, ccy):
    mau = Decimal(1).scaleb(-CHU_SO_LE[ccy])
    return x.quantize(mau, rounding=ROUND_HALF_UP)
usd = tron(Decimal("1000"), "USD")
ti_gia = Decimal("25400")                 # tỉ giá bán, số minh hoạ
print(usd, "USD ->", tron(usd * ti_gia, "VND"), "VND")
phi = tron(Decimal("15"), "USD")          # phí trung gian, minh hoạ
print("SHA: người nhận", tron(usd - phi, "USD"), "USD")"""
FX_OUT = """1000.00 USD -> 25400000 VND
SHA: người nhận 985.00 USD"""

FLOAT_PY = """from decimal import Decimal, ROUND_HALF_UP
print(0.1 + 0.2)
print(round(2.675, 2))
x = Decimal("2.675")
print(x.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))"""
FLOAT_OUT = """0.30000000000000004
2.67
2.68"""

PACS008_XML = """<FIToFICstmrCdtTrf>
  <GrpHdr>
    <MsgId>MSG-0001</MsgId>
  </GrpHdr>
  <CdtTrfTxInf>
    <IntrBkSttlmAmt Ccy="USD">1000.00</IntrBkSttlmAmt>
    <ChrgBr>SHAR</ChrgBr>
    <CdtrAgt><FinInstnId>
      <BICFI>WESTGB2L</BICFI>
    </FinInstnId></CdtrAgt>
  </CdtTrfTxInf>
</FIToFICstmrCdtTrf>"""

NOTE_ILL = "<span class='note'>(số minh hoạ — không phải tỉ giá hay biểu phí của ngân hàng nào)</span>"


def build():
    hook = sc("hook", "hook", "Chuyển 1 000 USD, người nhận chỉ thấy 985 USD", [
        st(f"""<p>Khách ở Việt Nam chuyển <b>1 000 USD</b> trả học phí cho một trường ở Anh. Ngân hàng trừ <b>25 400 000 đồng</b> theo tỉ giá bán 25 400.</p>
<div class="box key">Vài ngày sau trường báo chỉ nhận <b>985 USD</b>. 15 USD đi đâu, và có ai làm sai không?</div>
{NOTE_ILL}""",
           """Chào bạn, một khách ở Việt Nam chuyển một nghìn đô la Mỹ trả học phí cho một trường ở Anh.
           Ngân hàng trừ của khách hai mươi lăm triệu bốn trăm nghìn đồng, theo tỉ giá bán hai mươi lăm nghìn bốn trăm, đây là số minh hoạ.
           Vài ngày sau, trường báo chỉ nhận chín trăm tám mươi lăm đô la. Mười lăm đô la đã đi đâu, và có ai làm sai không?""",
           focus=[1, 1, 2, 2]),
        st(table(["câu hỏi", "phần trả lời trong bài"],
                 [["gửi tới đâu, số có bị gõ nhầm không", "mã BIC của ngân hàng, số IBAN và phép kiểm chia 97"],
                  ["tiền đi qua những sổ nào", "tài khoản nostro, vostro và bút toán hai đồng tiền"],
                  ["vì sao người nhận thiếu 15 USD", "tỉ giá và ba cách chịu phí OUR, SHA, BEN"],
                  ["lệnh được gửi bằng bản tin gì", "từ 22/11/2025: ISO 20022, bản tin pacs.008 thay MT103"]]),
           """Bài này trả lời bốn câu hỏi. Thứ nhất, gửi tới ngân hàng nào, và số tài khoản có bị gõ nhầm không.
           Thứ hai, tiền đi qua những cuốn sổ nào. Thứ ba, vì sao người nhận thiếu mười lăm đô la.
           Thứ tư, lệnh chuyển tiền đi bằng loại bản tin nào, khi chuẩn mới bắt buộc từ ngày hai mươi hai tháng mười một năm hai nghìn không trăm hai mươi lăm."""),
    ], checks=["alg.bnx_fx_vnd('1000', '25400') == 25400000", "alg.bnx_fee(1000, 'SHA', 0, 15)[1] == 985",
               "1000 - alg.bnx_fee(1000, 'SHA', 0, 15)[1] == 15"])

    pre = sc("prereq", "prereq", "Trước hết: bốn điều cần hiểu", [
        st(table(["khái niệm", "nghĩa", "ví dụ"],
                 [["① Bút toán kép, Nợ và Có", "mỗi giao dịch ghi ít nhất hai dòng, tổng Nợ bằng tổng Có; với tài khoản tiền gửi của khách: ghi Nợ là giảm, ghi Có là tăng; với tài sản của ngân hàng (như tiền gửi ở ngân hàng khác) thì ngược lại: ghi Nợ là tăng, ghi Có là giảm",
                   "A chuyển B 500 000: Nợ A 500 000, Có B 500 000"],
                  ["② Chia lấy dư", "phần còn lại khi chia một số nguyên cho số khác", "100 chia 97 được 1, dư 3"],
                  ["③ Đơn vị nhỏ nhất của đồng tiền", "ISO 4217 ghi số chữ số lẻ: USD có 2 (cent), VND có 0", "985,00 USD; 25 400 000 đồng"],
                  ["④ Tỉ giá bán", "số đồng khách trả để mua của ngân hàng 1 đơn vị ngoại tệ", "1 USD = 25 400 đồng (số minh hoạ)"]]),
           """Trước hết ta cần hiểu bốn điều. Trong sổ sách ngân hàng, mỗi giao dịch ghi ít nhất hai dòng có tổng bằng không.
           Kế toán ngân hàng gọi hai phía là Nợ và Có, và tổng Nợ luôn bằng tổng Có. Với tài khoản tiền gửi của khách, ghi Nợ là giảm, ghi Có là tăng.
           Còn với tài sản của chính ngân hàng, như tiền ngân hàng gửi ở ngân hàng khác, thì ngược lại, ghi Nợ là tăng, ghi Có là giảm.
           Chia lấy dư là phần còn lại khi chia, ví dụ một trăm chia chín mươi bảy được một, dư ba.
           Theo chuẩn ISO bốn hai một bảy, đô la Mỹ có hai chữ số lẻ, còn đồng Việt Nam không có chữ số lẻ.
           Tỉ giá bán là số đồng khách trả để mua của ngân hàng một đơn vị ngoại tệ."""),
        st("""$$1\\,000 \\cdot 25\\,400 = 25\\,400\\,000 \\text{ đồng}$$
<span class='note'>tỉ giá 25 400 là số minh hoạ</span>""",
           """Một ví dụ số. Mua một nghìn đô la với tỉ giá bán hai mươi lăm nghìn bốn trăm, đây là số minh hoạ.
           Dấu chấm giữa là phép nhân, nên khách trả một nghìn nhân hai mươi lăm nghìn bốn trăm, bằng hai mươi lăm triệu bốn trăm nghìn đồng.""",
           focus=[1, 2, 1], clear=True),
    ], checks=["100 % 97 == 3 and 100 // 97 == 1",
               "alg.bnx_balanced_by_ccy([('VND', 'A', 500000, 0), ('VND', 'B', 0, 500000)]) == {'VND': 0}",
               "alg.bnx_minor_units('USD') == 2 and alg.bnx_minor_units('VND') == 0",
               "str(alg.bnx_round('985', 'USD')) == '985.00'", "alg.bnx_fx_vnd(1000, 25400) == 25400000"])

    sym = sc("sym", "symbol", "Giải mã các từ của thanh toán quốc tế", [
        st(table(["từ", "nghĩa"],
                 [["Swift", "mạng bản tin giữa các ngân hàng trên thế giới: chở <b>lệnh</b>, không chở tiền"],
                  ["BIC (ISO 9362)", "mã định danh ngân hàng, 8 hoặc 11 ký tự"],
                  ["IBAN (ISO 13616)", "số tài khoản quốc tế: 2 chữ quốc gia, 2 chữ số kiểm, rồi số tài khoản trong nước"],
                  ["nostro", "tài khoản của <b>ta</b> mở ở ngân hàng nước ngoài (tiếng Ý: “của chúng tôi”)"],
                  ["vostro", "cùng tài khoản đó nhìn từ ngân hàng giữ nó: tài khoản <b>của bạn</b> ở chỗ tôi"],
                  ["OUR, SHA, BEN", "ai chịu phí: người gửi, chia hai bên, người nhận"]]),
           """Bảng này giải mã sáu từ. Mạng bản tin liên ngân hàng quốc tế chỉ chở lệnh chuyển tiền, không chở tiền.
           Mã định danh ngân hàng có tám hoặc mười một ký tự. Số tài khoản quốc tế gồm hai chữ quốc gia, hai chữ số kiểm, rồi số tài khoản trong nước.
           Tài khoản ngân hàng ta mở ở ngân hàng nước ngoài gọi theo tiếng Ý là của chúng tôi.
           Cùng tài khoản đó, nhìn từ ngân hàng đang giữ nó, gọi là của bạn.
           Ba mã cuối cho biết ai chịu phí: người gửi, chia hai bên, hay người nhận.""",
           focus=[0, "1.2", "1.3", "1.4", "1.5", "1.6", "1.7"]),
        st(table(["phần của BIC", "số ký tự", "ví dụ WESTGB2LXXX (mã minh hoạ)"],
                 [["mã tổ chức", "4", "WEST"], ["mã quốc gia (ISO 3166)", "2 chữ cái", "GB = Vương quốc Anh"],
                  ["mã địa điểm", "2", "2L"], ["mã chi nhánh (tuỳ chọn)", "3", "XXX = trụ sở chính; bỏ đi còn 8 ký tự WESTGB2L"]]),
           """Mã định danh ngân hàng chia thành bốn phần. Bốn ký tự đầu là mã tổ chức, ở đây là W E S T.
           Hai chữ cái tiếp theo là mã quốc gia, G B là Vương quốc Anh. Hai ký tự sau là mã địa điểm.
           Ba ký tự cuối là mã chi nhánh, có thể bỏ. Ba chữ X nghĩa là trụ sở chính, nên bỏ đi thì còn tám ký tự, vẫn trỏ về trụ sở chính.""",
           focus=[0, "1.2", "1.3", "1.4", "1.5", "1.5"], clear=True),
        st(code(PACS008_XML, "Bản tin pacs.008 rút gọn (ISO 20022, dạng XML)"),
           """Đây là bản tin chuyển tiền cho khách hàng theo chuẩn ISO hai không không hai hai, viết bằng XML và đã rút gọn.
           Phần nhóm đầu chứa mã bản tin. Phần thông tin giao dịch chứa số tiền thanh toán liên ngân hàng, kèm thuộc tính đồng tiền là đô la Mỹ.
           Thẻ người chịu phí ghi chia hai bên. Cuối cùng là ngân hàng của người nhận, nhận diện bằng mã tám ký tự vừa giải mã.""",
           focus=[2, "2.3", "2.6", "2.7", "2.9"], clear=True),
    ], checks=["alg.bnx_bic_parts('WESTGB2LXXX') == {'to_chuc': 'WEST', 'quoc_gia': 'GB', 'dia_diem': '2L', 'chi_nhanh': 'XXX'}",
               "alg.bnx_bic_parts('WESTGB2L')['chi_nhanh'] == 'XXX' and len('WESTGB2L') == 8 and len('WESTGB2LXXX') == 11",
               "len('GB82WEST12345698765432') == 22 and 'GB82WEST12345698765432'[:2] == 'GB'"])

    intu = sc("intuition", "intuition", "Hình dung: lệnh đi qua mạng, tiền đi qua các tài khoản", [
        st(svg(1500, 470,
               box(20, 170, 220, 110, ["Khách", "trả 25 400 000 đ"], C_BLUE, bold=True, size=22),
               box(300, 170, 250, 110, ["Ngân hàng A", "(Việt Nam)"], C_BLUE, bold=True, size=22),
               box(640, 170, 280, 110, ["Ngân hàng C", "đại lý, trung gian"], C_AMBER, bold=True, size=22),
               box(1010, 170, 230, 110, ["Ngân hàng D", "(Anh)"], C_GREEN, bold=True, size=22),
               box(1300, 170, 180, 110, ["Trường", "nhận"], C_GREEN, bold=True, size=22),
               arrow(240, 225, 295, 225), arrow(550, 225, 635, 225, "#475569", "1 000"),
               arrow(920, 225, 1005, 225, "#475569", "985"), arrow(1240, 225, 1295, 225),
               box(640, 330, 280, 80, ["giữ tài khoản", "nostro USD của A"], C_GRAY, size=20),
               txt(780, 120, "C trừ 15 USD phí (SHA)", 22, "middle", "#dc2626", True),
               txt(750, 455, "Lệnh đi bằng bản tin; tiền chỉ đổi số dư trong sổ của từng ngân hàng (số minh hoạ)", 22, "middle", "#1f2937")),
           """Hình cho thấy đường đi của một nghìn đô la. Khách trả đồng Việt Nam cho ngân hàng A. Ngân hàng A có một tài khoản đô la mở sẵn ở ngân hàng C, một ngân hàng đại lý.
           Ngân hàng C nhận lệnh, trừ mười lăm đô la phí vì lệnh ghi chia phí, rồi chuyển chín trăm tám mươi lăm đô la tới ngân hàng D ở Anh.
           Không có tờ tiền nào bay qua biên giới, mỗi ngân hàng chỉ đổi số dư trong sổ của mình."""),
        st(svg(1500, 450,
               panel(30, 30, 660, 330, "Sổ của ngân hàng A", C_BLUE),
               box(70, 110, 580, 100, ["“nostro USD tại C”", "tài sản: tiền của A đang gửi ở C"], C_GRAY, size=22),
               box(70, 230, 580, 100, ["chuyển đi 1 000 USD", "ghi Có nostro: giảm 1 000"], C_RED, size=22),
               panel(810, 30, 660, 330, "Sổ của ngân hàng C", C_AMBER),
               box(850, 110, 580, 100, ["“vostro của A”", "nợ phải trả: tiền C giữ hộ A"], C_GRAY, size=22),
               box(850, 230, 580, 100, ["trả theo lệnh của A", "ghi Nợ vostro: giảm 1 000"], C_RED, size=22),
               txt(750, 178, "=", 56, "middle", "#1f2937", True),
               txt(750, 420, "Hai cái tên cho cùng một tài khoản: A gọi là nostro, C gọi là vostro", 24, "middle", "#1f2937", True)),
           """Bây giờ nhìn cùng một tài khoản từ hai phía. Trong sổ của A, đó là tài sản, tức tiền của A đang gửi ở C, gọi là tài khoản của chúng tôi.
           Trong sổ của C, đó là khoản phải trả, tức tiền C giữ hộ A, gọi là tài khoản của bạn.
           Khi A chuyển đi một nghìn đô la, cả hai sổ cùng giảm một nghìn, chỉ khác tên phía ghi."""),
        st(table(["", "bản tin MT (cũ)", "ISO 20022 (bắt buộc từ 22/11/2025)"],
                 [["chuyển tiền cho khách hàng", "MT103", "pacs.008"],
                  ["chuyển tiền giữa hai định chế", "MT202", "pacs.009"],
                  ["ai chịu phí", "trường 71A: OUR / SHA / BEN", "ChrgBr: DEBT / SHAR / CRED"],
                  ["số tiền, đồng tiền, ngày", "gộp trong một trường 32A", "tách: IntrBkSttlmAmt (Ccy) và IntrBkSttlmDt"],
                  ["địa chỉ, các bên", "dòng chữ tự do", "mỗi phần có thẻ riêng (có cấu trúc)"]]),
           """Bảng này so bản tin cũ và chuẩn mới. Từ ngày hai mươi hai tháng mười một năm hai nghìn không trăm hai mươi lăm, chỉ thị thanh toán giữa các định chế trên mạng chỉ dùng chuẩn mới.
           Bản tin chuyển tiền cho khách hàng loại cũ được thay bằng loại mới tương ứng. Bản tin chuyển tiền giữa hai ngân hàng cũng có loại mới tương ứng.
           Trường ai chịu phí đổi ba mã cũ thành ba mã mới, người gửi, chia hai bên, người nhận.
           Số tiền, đồng tiền và ngày trước kia gộp trong một trường, nay tách thành các thẻ riêng. Địa chỉ cũng tách thành từng phần có cấu trúc.""",
           clear=True),
    ])

    form = sc("formula", "formula", "Suy ra từng bước: kiểm IBAN, đổi tiền, ghi sổ", [
        st("""<p><b>Bước 1.</b> Đưa 4 ký tự đầu <b>GB82</b> ra cuối: <code>WEST12345698765432GB82</code>. Vì số kiểm được tính khi mã quốc gia và số kiểm đứng sau cùng, ta phải xếp lại đúng như lúc tính.</p>
<span class='note'>Làm thử: chuỗi vẫn đủ 22 ký tự.</span>""",
           """Bước một, ta đưa bốn ký tự đầu ra cuối chuỗi. Vì số kiểm được tính khi mã quốc gia và hai chữ số kiểm đứng sau cùng, nên ta phải xếp lại đúng như lúc tính.
           Làm thử, chuỗi mới vẫn đủ hai mươi hai ký tự."""),
        st("""<p><b>Bước 2.</b> Đổi mỗi chữ cái thành số: A = 10, B = 11, …, Z = 35. Vì phép chia chỉ làm trên số, chữ phải thành số theo một bảng cố định.</p>
<span class='note'>Làm thử: W = 32, E = 14, S = 28, T = 29, G = 16, B = 11 nên đầu chuỗi WEST thành 32142829.</span>""",
           """Bước hai, ta đổi mỗi chữ cái thành số, A là mười, B là mười một, cứ thế tới Z là ba mươi lăm. Vì phép chia chỉ làm trên số, nên chữ phải đổi thành số theo một bảng cố định.
           Làm thử, bốn chữ W E S T thành ba mươi hai, mười bốn, hai mươi tám, hai mươi chín."""),
        st(code(IBAN_PY, "Bước 3. Chia cho 97 lấy dư: đúng thì dư bằng 1") + out(IBAN_OUT),
           """Bước ba, ta cho Python làm cả ba việc. Câu lệnh thứ hai xếp lại chuỗi, vòng lặp đổi từng ký tự thành số theo cơ số ba mươi sáu.
           Cơ số ba mươi sáu là hệ đếm dùng mười chữ số rồi hai mươi sáu chữ cái, nên A là mười và Z là ba mươi lăm.
           Máy in chuỗi đã xếp, chuỗi hai mươi tám chữ số, và số dư khi chia chín mươi bảy bằng một. Vì dư bằng một, nên số này qua phép kiểm.""",
           focus=[1, 2, "2.5", 4, "4.3"], clear=True),
        st("""<p><b>Bước 4.</b> Vì sao đúng thì dư bằng 1? Vì người lập IBAN chọn số kiểm sao cho dư bằng 1: đặt <code>00</code> vào chỗ số kiểm, lấy dư $r$, rồi số kiểm $= 98 - r$.</p>
$$98 - 16 = 82$$""",
           """Bước bốn, vì sao đúng thì dư bằng một? Vì người lập số tài khoản quốc tế đã chọn hai chữ số kiểm sao cho dư bằng một.
           Họ đặt hai số không vào chỗ số kiểm và lấy số dư khi chia chín mươi bảy, ở đây là mười sáu. Chín mươi tám trừ mười sáu bằng tám mươi hai, đúng hai chữ số kiểm của mẫu.""",
           focus=[1, 1, 1, 2], clear=True),
        st(code(FX_PY, "Bước 5. Đổi tiền bằng số thập phân chính xác, làm tròn theo từng đồng tiền") + out(FX_OUT),
           """Bước năm là đổi tiền. Vì số thực dấu phẩy động không biểu diễn đúng nhiều số thập phân như không phẩy một, nên ta dùng kiểu số thập phân chính xác của Python.
           Hàm làm tròn lấy số chữ số lẻ theo chuẩn ISO bốn hai một bảy, đô la tới từng xu, đồng Việt Nam tới từng đồng.
           Máy in một nghìn đô la thành hai mươi lăm triệu bốn trăm nghìn đồng, và người nhận được chín trăm tám mươi lăm đô la khi trung gian trừ mười lăm đô la.""",
           focus=[1, "2.1", "2.2", 4], clear=True),
        st(table(["đồng tiền", "tài khoản (tên minh hoạ)", "Nợ", "Có"],
                 [["VND", "tiền gửi của khách", "25 400 000", ""], ["VND", "mua bán ngoại tệ (VND)", "", "25 400 000"],
                  ["USD", "mua bán ngoại tệ (USD)", "1 000", ""], ["USD", "nostro USD tại ngân hàng C", "", "1 000"]]),
           """Bước sáu là ghi sổ ở ngân hàng A, và mỗi đồng tiền phải tự cân. Vì không thể cộng đô la với đồng, nên ta tách hai vế qua một tài khoản mua bán ngoại tệ.
           Vế đồng Việt Nam, ghi Nợ tiền gửi của khách hai mươi lăm triệu bốn trăm nghìn, tức là trừ tiền khách, và ghi Có tài khoản mua bán ngoại tệ cùng số đó.
           Vế đô la, ghi Nợ tài khoản mua bán ngoại tệ một nghìn, ghi Có tài khoản ở nước ngoài một nghìn, vì tiền của A ở ngân hàng C giảm đi.""",
           focus=[0, 0, ["1.2", "1.3"], ["1.4", "1.5"]], clear=True),
    ], checks=["alg.bnx_iban_digits('GB82WEST12345698765432') == '3214282912345698765432161182'",
               "alg.bnx_iban_mod97('GB82WEST12345698765432') == 1",
               "len('WEST12345698765432GB82') == 22 and 'GB82WEST12345698765432'[4:] + 'GB82' == 'WEST12345698765432GB82'",
               "[ord(c) - 55 for c in 'WESTGB'] == [32, 14, 28, 29, 16, 11]",
               "alg.bnx_iban_check_digits('GB', 'WEST12345698765432') == ('82', 16)",
               "alg.bnx_fx_vnd('1000', '25400') == 25400000 and str(alg.bnx_fee('1000', 'SHA', 0, 15)[1]) == '985.00'",
               "alg.bnx_balanced_by_ccy(alg.bnx_nostro_entries('1000', '25400')) == {'VND': 0, 'USD': 0}",
               "[e[2] or e[3] for e in alg.bnx_nostro_entries('1000', '25400')] == [25400000, 25400000, 1000, 1000]"])

    ex = sc("example", "example", "Ví dụ 1 000 USD với ba cách chịu phí, từng phép tính", [
        st(f"""<p>Chuyển <b>1 000 USD</b>, tỉ giá bán <b>25 400</b>, phí của trung gian <b>15 USD</b>, phí của ngân hàng gửi <b>5 USD</b>. {NOTE_ILL}</p>
$$① \\; 1\\,000 \\cdot 25\\,400 = \\hl{{25\\,400\\,000}} \\text{{ đồng tiền gốc, chưa tính phí}}$$""",
           """Ta tính từng phép. Chuyển một nghìn đô la, tỉ giá bán hai mươi lăm nghìn bốn trăm, phí trung gian mười lăm đô la, phí ngân hàng gửi năm đô la, đều là số minh hoạ.
           Phép tính thứ nhất, tiền gốc chưa tính phí là một nghìn nhân hai mươi lăm nghìn bốn trăm, bằng hai mươi lăm triệu bốn trăm nghìn đồng."""),
        st("""<p>Chia phí (SHA): người gửi trả phí ngân hàng mình riêng; phí trung gian trừ vào tiền chuyển.</p>
$$② \\; 1\\,000 - 15 = \\hl{985} \\text{ USD người nhận được}$$""",
           """Phép tính thứ hai, với cách chia phí, người gửi trả phí ngân hàng của mình riêng, còn phí trung gian trừ thẳng vào tiền chuyển.
           Vì vậy người nhận được một nghìn trừ mười lăm, bằng chín trăm tám mươi lăm đô la. Đó chính là con số trường báo ở đầu bài."""),
        st("""<p>Người gửi chịu hết (OUR): người nhận được đủ 1 000; người gửi trả thêm phí ngân hàng mình và phí trung gian.</p>
$$③ \\; 1\\,000 + 5 + 15 = \\hl{1\\,020} \\text{ USD người gửi trả}$$""",
           """Phép tính thứ ba, với cách người gửi chịu hết, người nhận được đủ một nghìn đô la. Người gửi trả một nghìn cộng năm cộng mười lăm, bằng một nghìn không trăm hai mươi đô la."""),
        st("""<p>Dùng lại $1\\,020$ ở phép ③, đổi ra đồng:</p>
$$④ \\; 1\\,020 \\cdot 25\\,400 = \\hl{25\\,908\\,000} \\text{ đồng, hơn tiền gốc ở phép ① là } 508\\,000$$""",
           """Phép tính thứ tư, dùng lại một nghìn không trăm hai mươi đô la, nhân hai mươi lăm nghìn bốn trăm, bằng hai mươi lăm triệu chín trăm lẻ tám nghìn đồng.
           So với tiền gốc ở phép thứ nhất, khách trả thêm năm trăm lẻ tám nghìn đồng, chính là tiền phí để trường nhận đủ.""", clear=True),
        st("""<p>Người nhận chịu hết (BEN): cả phí ngân hàng gửi lẫn phí trung gian trừ vào tiền chuyển.</p>
$$⑤ \\; 1\\,000 - 5 - 15 = \\hlg{980} \\text{ USD người nhận được}$$""",
           """Phép tính thứ năm, với cách người nhận chịu hết, cả hai khoản phí đều trừ vào tiền chuyển. Người nhận được một nghìn trừ năm trừ mười lăm, bằng chín trăm tám mươi đô la."""),
    ], checks=["alg.bnx_fx_vnd(1000, 25400) == 25400000",
               "alg.bnx_fee(1000, 'SHA', 5, 15) == (alg.bnx_round(1005, 'USD'), alg.bnx_round(985, 'USD'))",
               "alg.bnx_fee(1000, 'OUR', 5, 15) == (alg.bnx_round(1020, 'USD'), alg.bnx_round(1000, 'USD'))",
               "alg.bnx_fx_vnd(alg.bnx_fee(1000, 'OUR', 5, 15)[0], 25400) == 25908000",
               "alg.bnx_fx_vnd(alg.bnx_fee(1000, 'OUR', 5, 15)[0], 25400) - alg.bnx_fx_vnd(1000, 25400) == 508000",
               "alg.bnx_fee(1000, 'BEN', 5, 15)[1] == 980"])

    chk = sc("check", "check", "Tự kiểm bằng đường khác: chia từng chữ số, đổi ngược, cộng sổ", [
        st(code(MOD_PY, "Đường khác: không dựng số 28 chữ số, chỉ mang số dư qua từng chữ số") + out(MOD_OUT),
           """Kiểm bằng đường khác. Thay vì dựng một số hai mươi tám chữ số, ta đi qua từng chữ số và chỉ giữ số dư.
           Mỗi bước nhân số dư cũ với mười, cộng chữ số mới, rồi chia chín mươi bảy lấy dư, vì phép lấy dư đi qua được phép cộng và phép nhân.
           Máy in một, khớp với cách tính cả số. Cách này còn dùng được ở ngôn ngữ không có số nguyên lớn.""",
           focus=[2, "2.4", "2.4", 4, 0]),
        st(table(["điều cần kiểm", "đường khác", "kết quả"],
                 [["① 25 400 000 đồng", "chia ngược: 25 400 000 ÷ 25 400", "= 1 000 USD"],
                  ["② 985 USD (SHA)", "cộng lại: 985 + 15", "= 1 000 USD"],
                  ["bút toán ở bước 6", "tổng Nợ trừ tổng Có, từng đồng tiền", "VND: 0; USD: 0"]]),
           """Bảng này kiểm ba kết quả còn lại bằng phép ngược. Vì phép chia ngược phép nhân, hai mươi lăm triệu bốn trăm nghìn chia ngược cho tỉ giá được đúng một nghìn đô la.
           Chín trăm tám mươi lăm cộng mười lăm phí được đúng một nghìn. Còn bút toán ở bước sáu, tổng Nợ trừ tổng Có của từng đồng tiền đều bằng không.""",
           clear=True),
    ], checks=["(lambda s: __import__('functools').reduce(lambda d, c: (d * 10 + int(c)) % 97, s, 0))(alg.bnx_iban_digits('GB82WEST12345698765432')) == 1",
               "alg.bnx_fx_vnd(1000, 25400) // 25400 == 1000 and alg.bnx_fx_vnd(1000, 25400) % 25400 == 0",
               "alg.bnx_fee(1000, 'SHA', 0, 15)[1] + 15 == 1000",
               "set(alg.bnx_balanced_by_ccy(alg.bnx_nostro_entries('1000', '25400')).values()) == {0}"])

    pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st(code(FLOAT_PY, "Lỗi 1 (người mới): tính tiền bằng số thực dấu phẩy động") + out(FLOAT_OUT),
           """Lỗi thứ nhất, của người mới, là tính tiền bằng số thực dấu phẩy động. Máy in không phẩy một cộng không phẩy hai thành một số lẻ dài, không phải không phẩy ba.
           Làm tròn hai phẩy sáu trăm bảy mươi lăm tới hai chữ số lại ra hai phẩy sáu bảy, vì số đó được lưu là hai phẩy sáu bảy bốn chín chín chín.
           Kiểu số thập phân chính xác cho đúng hai phẩy sáu tám. Phép thử bắt lỗi này là đối chiếu với cách tính bằng số nguyên theo xu.""",
           focus=[1, "4.1", "4.2", "4.3", 0]),
        st("""<div class="box warn"><b>Lỗi 2 (người đã đi làm).</b> Chọn chia phí (SHA) cho một hoá đơn phải trả <b>đủ</b> 1 000 USD. Người nhận được 985 USD, hoá đơn còn nợ 15 USD và phải chuyển thêm một lần nữa, lại mất phí.
<br><span class="note">Phép thử: đối chiếu số tiền người nhận báo có với số trên hoá đơn; ngân hàng trung gian <b>có thể</b> trừ phí.</span></div>""",
           """Lỗi thứ hai, của người đã đi làm, là chọn chia phí cho một hoá đơn phải trả đủ một nghìn đô la.
           Người nhận chỉ được chín trăm tám mươi lăm, hoá đơn còn thiếu mười lăm, và phải chuyển thêm một lần nữa, lại mất phí.
           Phép thử là đối chiếu số người nhận báo có với số trên hoá đơn, vì ngân hàng trung gian có thể trừ phí.""", clear=True),
        st("""<div class="box warn"><b>Lỗi 3 (người đã đi làm).</b> Coi IBAN “qua phép chia 97” là <b>tài khoản đúng người</b>. Phép kiểm chỉ bắt lỗi gõ: đổi chỗ hai chữ số cuối thì dư 49, nhưng một số hợp lệ của người khác vẫn dư 1.
<br><span class="note">Cách chữa: kiểm số trước khi gửi, rồi vẫn đối chiếu tên người nhận và xử lý lệnh bị trả về.</span></div>""",
           """Lỗi thứ ba, cũng của người đã đi làm, là coi số tài khoản quốc tế qua phép chia chín mươi bảy là đúng người nhận.
           Phép kiểm chỉ bắt lỗi gõ, ví dụ đổi chỗ hai chữ số cuối thì số dư thành bốn mươi chín. Nhưng một số hợp lệ của người khác vẫn cho dư một.
           Cách chữa là kiểm số trước khi gửi, rồi vẫn đối chiếu tên người nhận và xử lý lệnh bị trả về."""),
    ], checks=["alg.bnx_float_demo()[0] != 0.3 and repr(alg.bnx_float_demo()[0]) == '0.30000000000000004'",
               "alg.bnx_float_demo()[1] == 2.67 and str(alg.bnx_float_demo()[2]) == '2.68'",
               "__import__('decimal').Decimal(2.675) < __import__('decimal').Decimal('2.675')",
               "alg.bnx_iban_mod97('GB82WEST12345698765423') == 49",
               "1000 - alg.bnx_fee(1000, 'SHA', 0, 15)[1] == 15"])

    quiz = sc("quiz", "quiz", "Đến lượt bạn", [
        st(table(["câu", "đề"],
                 [["1", "Khách gõ GB82WEST12345698765423 (hai chữ số cuối đổi chỗ). Chuỗi số sau khi xếp lại và đổi chữ là 3214282912345698765423161182, chia 97 dư 49. Hệ thống làm gì?"],
                  ["2", "Chuyển 2 500 USD, tỉ giá bán 25 400, chia phí, ngân hàng gửi không thu phí, trung gian trừ 20 USD (số minh hoạ). Khách trả bao nhiêu đồng, người nhận được bao nhiêu?"],
                  ["3", "Quyết định: khách trả một hoá đơn phải nhận đủ 2 500 USD. Khuyên chọn người gửi chịu hết (OUR) hay chia phí (SHA)?"]]),
           """Đến lượt bạn. Câu một, khách gõ nhầm, đổi chỗ hai chữ số cuối, và chuỗi số sau khi xếp lại chia chín mươi bảy dư bốn mươi chín. Hệ thống nên làm gì?
           Câu hai, chuyển hai nghìn năm trăm đô la, tỉ giá bán hai mươi lăm nghìn bốn trăm, chia phí, ngân hàng gửi không thu phí, trung gian trừ hai mươi đô la. Khách trả bao nhiêu đồng, người nhận được bao nhiêu?
           Câu ba, khách trả một hoá đơn phải nhận đủ hai nghìn năm trăm đô la. Bạn khuyên chọn người gửi chịu hết hay chia phí? Hãy dừng video và làm ra giấy.""",
           pause=25),
        st("""<p>Câu 1: dư phải bằng 1 mới qua.</p>
$$49 \\neq 1 \\;\\Rightarrow\\; \\text{từ chối ngay, báo khách gõ lại}$$""",
           """Đáp án câu một. Số dư phải bằng một mới qua, mà ở đây là bốn mươi chín, khác một. Dấu gạch chéo qua dấu bằng nghĩa là khác, mũi tên đôi nghĩa là suy ra.
           Vì vậy hệ thống từ chối ngay khi khách nhập, chưa gửi lệnh nào, và yêu cầu khách gõ lại.""",
           introduces=["neq"]),
        st("""$$2\\,500 \\cdot 25\\,400 = \\hl{63\\,500\\,000} \\text{ đồng};\\quad 2\\,500 - 20 = \\hlg{2\\,480} \\text{ USD}$$""",
           """Đáp án câu hai. Khách trả hai nghìn năm trăm nhân hai mươi lăm nghìn bốn trăm, bằng sáu mươi ba triệu năm trăm nghìn đồng.
           Vì chia phí nên phí trung gian trừ vào tiền chuyển, người nhận được hai nghìn năm trăm trừ hai mươi, bằng hai nghìn bốn trăm tám mươi đô la."""),
        st(table(["lựa chọn", "được", "mất"],
                 [["người gửi chịu hết (OUR)", "người nhận nhận đủ 2 500, hoá đơn tất toán một lần", "khách trả thêm phí; phí trung gian khó biết trước"],
                  ["chia phí (SHA)", "khách trả ít phí hơn", "người nhận có thể thiếu, phải chuyển bù một lần nữa và lại mất phí"]]),
           """Đáp án câu ba. Chọn người gửi chịu hết thì người nhận nhận đủ và hoá đơn tất toán một lần, đổi lại khách trả thêm phí, mà phí trung gian khó biết trước.
           Chọn chia phí thì khách trả ít phí hơn, nhưng người nhận có thể thiếu và phải chuyển bù, lại mất phí. Với hoá đơn phải nhận đủ, nên khuyên người gửi chịu hết."""),
    ], checks=["alg.bnx_iban_digits('GB82WEST12345698765423') == '3214282912345698765423161182'",
               "alg.bnx_iban_mod97('GB82WEST12345698765423') == 49 and 49 != 1",
               "alg.bnx_fx_vnd(2500, 25400) == 63500000", "alg.bnx_fee(2500, 'SHA', 0, 20)[1] == 2480",
               "alg.bnx_fee(2500, 'OUR', 0, 20)[1] == 2500"])

    rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        st(chain("BIC + IBAN (kiểm chia 97)", "bản tin pacs.008", "nostro ở A = vostro ở C", "tỉ giá + phí OUR/SHA/BEN", "số thập phân, làm tròn theo ISO 4217"),
           """Tổng kết chuỗi logic. Mã định danh ngân hàng và số tài khoản quốc tế cho biết gửi tới đâu, và phép chia chín mươi bảy bắt lỗi gõ.
           Lệnh đi bằng bản tin chuẩn ISO hai không không hai hai. Tiền đi qua tài khoản mà ngân hàng gửi gọi là của chúng tôi, còn ngân hàng giữ gọi là của bạn.
           Số tiền phụ thuộc tỉ giá và cách chịu phí. Mọi phép tính dùng số thập phân chính xác, làm tròn theo đơn vị nhỏ nhất của từng đồng tiền.""",
           focus=[0, "1.1", "1.3", "1.5", "1.7", "1.9"]),
        st("""<div class='box key'><b>Tư duy:</b> trong thanh toán quốc tế, <b>lệnh</b> và <b>tiền</b> đi hai đường khác nhau. Lệnh đi bằng bản tin; tiền chỉ đổi số dư trong sổ của từng ngân hàng, và mỗi trạm có thể trừ phí.</div>""",
           """Điều cần mang theo. Trong thanh toán quốc tế, lệnh và tiền đi hai đường khác nhau. Lệnh đi bằng bản tin, còn tiền chỉ đổi số dư trong sổ của từng ngân hàng, và mỗi trạm có thể trừ phí."""),
        st("""<p class='small'>Bài sau: ví điện tử và nộp thuế điện tử — tiền trong ví thật ra nằm ở đâu, và khi nào một khoản nộp thuế mới thật sự xong.</p>""",
           """Ở bài sau, ta học về ví điện tử và nộp thuế điện tử, tức là tiền trong ví thật ra nằm ở đâu, và khi nào một khoản nộp thuế mới thật sự xong.""",
           forward_ref=True),
    ])
    return lesson("L11", "thanh_toan_quoc_te_ngoai_te", "Bài 11 — Thanh toán quốc tế và ngoại tệ: SWIFT, ISO 20022, tài khoản nostro và tỉ giá",
                  "curriculum/bnx.yaml L11; audit/bnx/verify_bnx.py L11; audit/bnx/sources.md [CBPR] [IBAN] [BIC] [ISO4217] [MT71A] [P8UG] [P8BNY] [NOSTRO]: "
                  "ISO 13616:2020 (IBAN, mod 97), ISO 9362:2022 (BIC), ISO 4217 danh sách SIX công bố 2026-09-17, Swift Category 1 MT Message Reference Guide 19/07/2024 (MT103 trường 71A), "
                  "CBPR+ pacs.008.001.08 Usage Guideline SR2025 13/12/2024, BNY 'A deep dive on pacs.008' (02/2021), Clearstream CBPR+ (cập nhật 03/11/2026); tỉ giá, phí, BIC WESTGB2L là số/mã minh hoạ",
                  ["Đọc mã BIC và kiểm số IBAN", "Ghi bút toán chuyển tiền quốc tế qua tài khoản nostro",
                   "Tính số tiền khi đổi ngoại tệ và chịu phí theo OUR, SHA, BEN", "Nêu thay đổi từ bản tin MT sang ISO 20022"],
                  [hook, pre, sym, intu, form, ex, chk, pit, quiz, rec])
