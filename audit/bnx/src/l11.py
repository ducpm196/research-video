import lib2
from lib2 import *

lib2.begin("L11")

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

# Đầu ra THẬT: prog() chạy nguyên văn lúc import (Python 3.13) và so với hằng *_OUT hiện trên màn hình (khác thì dừng).
P_IBAN = prog("Iban", IBAN_PY, lang="python", out=IBAN_OUT)
P_MOD = prog("Mod", MOD_PY, lang="python", out=MOD_OUT)
P_FX = prog("Fx", FX_PY, lang="python", out=FX_OUT)
lib2.other("<FIToFICstmrCdtTrf>", kind="other", lang="xml",
           reason="Bản tin pacs.008.001.08 RÚT GỌN (bài nói rõ “rút gọn”): chỉ giữ các phần tử bài giảng; không phải bản tin đầy đủ để gửi.",
           read_check="(1) Phân tích thật bằng xml.etree.ElementTree trong audit/bnx/ver/l11.py (nhập hằng PACS008_XML): XML đúng cú pháp, gốc FIToFICstmrCdtTrf, có GrpHdr/MsgId = MSG-0001, "
                      "CdtTrfTxInf/IntrBkSttlmAmt thuộc tính Ccy = USD, giá trị 1000.00 (2 chữ số lẻ theo ISO 4217), ChrgBr = SHAR, CdtrAgt/FinInstnId/BICFI = WESTGB2L (8 ký tự). "
                      "(2) Tên thẻ và đường dẫn đối chiếu nguyên văn với CBPR+ Usage Guideline pacs.008.001.08 SR2025 (13/12/2024). (3) Ánh xạ 71A ↔ ChrgBr theo BNY “A deep dive on pacs.008” (02/2021).",
           unverified_claims=["Bản rút gọn thiếu các phần tử bắt buộc của CBPR+ và không khai không gian tên của lược đồ — không kiểm theo lược đồ XSD (máy không có XSD chính thức); bài chỉ dùng để đọc tên thẻ",
                              "BIC WESTGB2L là mã minh hoạ (bài ghi “mã minh hoạ”), không tra danh bạ BIC"])

# Cảnh quy mô: cộng 0,10 nhiều lần bằng số thực dấu phẩy động và bằng số thập phân chính xác — đo thật, ba cỡ.
SCALE_PY = """from decimal import Decimal
for n in (10, 10000, 1000000):
    f, d = 0.0, Decimal(0)
    for _ in range(n):
        f += 0.10
        d += Decimal("0.10")
    print(n, "lan cong 0.10: float", f, "| Decimal", d)"""
P_SCALE = prog("Scale", SCALE_PY, lang="python", timeout=300)
LAB_PY = """def chu_so(s):
    return "".join(str(int(c, 36)) for c in s)
def du97(iban):
    return int(chu_so(iban[4:] + iban[:4])) % 97
bic = "ABCDDEFFXXX"
print(f"BIC {bic}: to chuc {bic[:4]}, quoc gia {bic[4:6]}, dia diem {bic[6:8]}, chi nhanh {bic[8:] or '-'}")
iban = "GB90BANK98765432101234"
sai = iban[:-2] + iban[-1] + iban[-2]
for x in (iban, sai):
    r = du97(x)
    print(x + ": du", r, "->", "hop le" if r == 1 else "khong hop le")
tien, phi_gui, phi_tg = 2000, 8, 12
print("nguoi nhan: OUR", tien, "SHA", tien - phi_tg, "BEN", tien - phi_gui - phi_tg)
print("nguoi gui tra: OUR", tien + phi_gui + phi_tg)
"""
P_LAB = prog("Lab", LAB_PY, lang="python")
LAB_OUT = P_LAB.out

NOTE_ILL = "<span class='note'>(số minh hoạ — không phải tỉ giá hay biểu phí của ngân hàng nào)</span>"


def build():
    hook = sc("hook", "hook", "Chuyển 1 000 USD, người nhận chỉ thấy 985 USD", [
        st(f"""<p>Khách ở Việt Nam chuyển <b>1 000 USD</b> trả học phí cho một trường ở Anh. Ngân hàng trừ <b>25 400 000 đồng</b> theo tỉ giá bán 25 400.</p>
<div class="box key">Vài ngày sau trường báo chỉ nhận <b>985 USD</b>. 15 USD đi đâu, và có ai làm sai không?</div>
{NOTE_ILL}""",
           """Chào bạn, một khách ở Việt Nam chuyển một nghìn đô la Mỹ trả học phí cho một trường ở Anh.
           Ngân hàng trừ hai mươi lăm triệu bốn trăm nghìn đồng, theo tỉ giá bán minh hoạ hai mươi lăm nghìn bốn trăm.
           Vài ngày sau trường báo chỉ nhận chín trăm tám mươi lăm đô la. Mười lăm đô la đã đi đâu?""",
           focus=[1, 1, 2, 2]),
        st(table(["câu hỏi", "phần trả lời trong bài"],
                 [["gửi tới đâu, số có bị gõ nhầm không", "mã <b>BIC</b> (mã định danh ngân hàng), số <b>IBAN</b> (số tài khoản quốc tế) và phép kiểm chia 97"],
                  ["tiền đi qua những sổ nào", "tài khoản <b>nostro</b> (tài khoản của ta mở ở ngân hàng nước ngoài), vostro và bút toán hai đồng tiền"],
                  ["vì sao người nhận thiếu 15 USD", "tỉ giá và ba cách chịu phí OUR, SHA, BEN"],
                  ["lệnh được gửi bằng bản tin gì", "từ 22/11/2025: chuẩn bản tin <b>ISO 20022</b>, pacs.008 thay MT103"]]),
           """Bài này trả lời bốn câu hỏi. Số tài khoản có bị gõ nhầm không, tiền đi qua những cuốn sổ nào, vì sao người nhận thiếu mười lăm đô la, và lệnh đi bằng loại bản tin nào.""",
           introduces=["bnx_bic", "bnx_iban", "bnx_nostro", "bnx_iso20022"]),
    ], checks=["alg.bnx_fx_vnd('1000', '25400') == 25400000", "alg.bnx_fee(1000, 'SHA', 0, 15)[1] == 985",
               "1000 - alg.bnx_fee(1000, 'SHA', 0, 15)[1] == 15"])

    pre = sc("prereq", "prereq", "Trước hết: bốn điều cần hiểu", [
        st(table(["khái niệm", "nghĩa", "ví dụ"],
                 [["① Bút toán kép, Nợ và Có", "mỗi giao dịch ghi ít nhất hai dòng, tổng Nợ bằng tổng Có; với tài khoản tiền gửi của khách: ghi Nợ là giảm, ghi Có là tăng; với tài sản của ngân hàng (như tiền gửi ở ngân hàng khác) thì ngược lại: ghi Nợ là tăng, ghi Có là giảm",
                   "A chuyển B 500 000: Nợ A 500 000, Có B 500 000"],
                  ["② Chia lấy dư", "phần còn lại khi chia một số nguyên cho số khác", "100 chia 97 được 1, dư 3"],
                  ["③ Đơn vị nhỏ nhất của đồng tiền", "ISO 4217 ghi số chữ số lẻ: USD có 2 (cent), VND có 0", "985,00 USD; 25 400 000 đồng"],
                  ["④ Tỉ giá bán", "số đồng khách trả để mua của ngân hàng 1 đơn vị ngoại tệ", "1 USD = 25 400 đồng (số minh hoạ)"]]),
           """Trước hết ta cần hiểu bốn điều. Kế toán gọi hai phía là Nợ và Có, và tổng Nợ bằng tổng Có. Với tiền gửi của khách, ghi Nợ là giảm, ghi Có là tăng, còn với tài sản của chính ngân hàng thì ngược lại.
           Chia lấy dư là phần còn lại khi chia, một trăm chia chín mươi bảy dư ba. Theo chuẩn ISO bốn hai một bảy, đô la Mỹ có hai chữ số lẻ, còn đồng Việt Nam không có. Tỉ giá bán là số đồng khách trả để mua một đơn vị ngoại tệ."""),
        st("""$$1\\,000 \\cdot 25\\,400 = 25\\,400\\,000 \\text{ đồng}$$
<span class='note'>tỉ giá 25 400 là số minh hoạ</span>""",
           """Một ví dụ số. Mua một nghìn đô la với tỉ giá bán hai mươi lăm nghìn bốn trăm, đây là số minh hoạ.
           Dấu chấm giữa là phép nhân, nên kết quả là hai mươi lăm triệu bốn trăm nghìn đồng.""",
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
           """Bảng này giải mã sáu từ. Mạng bản tin giữa các ngân hàng chỉ chở lệnh chuyển tiền, không chở tiền. Mã định danh ngân hàng dài tám hoặc mười một ký tự.
           Số tài khoản quốc tế gồm hai chữ quốc gia, hai chữ số kiểm, rồi số tài khoản trong nước. Tài khoản của chúng tôi là tài khoản mình mở ở ngân hàng nước ngoài, còn tài khoản của bạn là chính nó nhìn từ ngân hàng giữ.
           Ba mã cuối cho biết ai chịu phí.""",
           focus=[0, "1.2", "1.3", "1.4", "1.5", "1.7"]),
        st(table(["phần của BIC", "số ký tự", "ví dụ WESTGB2LXXX (mã minh hoạ)"],
                 [["mã tổ chức", "4", "WEST"], ["mã quốc gia (ISO 3166)", "2 chữ cái", "GB = Vương quốc Anh"],
                  ["mã địa điểm", "2", "2L"], ["mã chi nhánh (tuỳ chọn)", "3", "XXX = trụ sở chính; bỏ đi còn 8 ký tự WESTGB2L"]]),
           """Mã định danh ngân hàng chia thành bốn phần. Bốn ký tự đầu là mã tổ chức, W E S T. Hai chữ cái tiếp theo là mã quốc gia, G B là Vương quốc Anh. Hai ký tự sau là mã địa điểm, và ba ký tự cuối là mã chi nhánh, có thể bỏ.""",
           focus=[0, "1.2", "1.3", "1.4", "1.5", "1.5"], clear=True),
        st(table(["viết trong thẻ", "đọc là", "trong ví dụ"],
                 [["<code>&lt;GrpHdr&gt;</code> chứa <code>&lt;MsgId&gt;</code>", "phần đầu của cả bản tin; <code>MsgId</code> là mã bản tin", "<code>MSG-0001</code>"],
                  ["<code>&lt;CdtTrfTxInf&gt;</code> chứa <code>&lt;IntrBkSttlmAmt Ccy=&quot;USD&quot;&gt;</code>", "thông tin một giao dịch; số tiền giữa hai ngân hàng, thuộc tính <code>Ccy</code> ghi đồng tiền", "<code>1000.00</code> đô la Mỹ"],
                  ["<code>&lt;ChrgBr&gt;</code>", "bên chịu phí: <code>DEBT</code> người gửi, <code>SHAR</code> chia hai bên, <code>CRED</code> người nhận", "<code>SHAR</code> = chia phí"],
                  ["<code>&lt;CdtrAgt&gt;</code> chứa <code>&lt;FinInstnId&gt;</code> chứa <code>&lt;BICFI&gt;</code>", "ngân hàng của người nhận; định danh của định chế; mã BIC của nó", "<code>WESTGB2L</code>"]])
           + """<p class="note"><b>XML</b>: văn bản chữ chia thành các <b>thẻ</b> lồng nhau; mỗi thẻ mở bằng <code>&lt;Tên&gt;</code>, đóng bằng <code>&lt;/Tên&gt;</code>, chữ ở giữa là giá trị.</p>""",
           """Bản tin chuẩn mới viết bằng XML: văn bản chia thành các thẻ lồng nhau, mỗi thẻ mở rồi đóng, chữ ở giữa là giá trị.
           Thẻ tiêu đề nhóm chứa mã bản tin. Thẻ thông tin giao dịch chứa số tiền, thuộc tính ghi loại tiền. Thẻ bên chịu phí ghi ai trả phí, và thẻ ngân hàng người nhận chứa mã ngân hàng.""",
           clear=True),
        st(code(PACS008_XML, "Bản tin pacs.008 rút gọn (ISO 20022, dạng XML)"),
           """Đây là bản tin theo chuẩn ISO hai không không hai hai, đã rút gọn: số tiền đô la Mỹ, cách chia phí và ngân hàng nhận bằng mã tám ký tự vừa giải mã.""",
           clear=True),
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
           """Ngân hàng A có tài khoản đô la mở sẵn ở ngân hàng đại lý C. Ngân hàng C trừ mười lăm đô la phí chia rồi chuyển chín trăm tám mươi lăm đô la tới ngân hàng D ở Anh.
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
           """ Trong sổ của A, đó là tài sản, tức tiền của A đang gửi ở C, gọi là tài khoản của chúng tôi.
           Trong sổ của C, đó là khoản phải trả, tức tiền C giữ hộ A, gọi là tài khoản của bạn.
"""),
        st(table(["", "bản tin MT (cũ)", "ISO 20022 (bắt buộc từ 22/11/2025)"],
                 [["chuyển tiền cho khách hàng", "MT103", "pacs.008"],
                  ["chuyển tiền giữa hai định chế (tổ chức tài chính)", "MT202", "pacs.009"],
                  ["ai chịu phí", "trường 71A: OUR / SHA / BEN", "ChrgBr: DEBT / SHAR / CRED"],
                  ["số tiền, đồng tiền, ngày", "gộp trong một trường 32A", "tách: IntrBkSttlmAmt (Ccy) và IntrBkSttlmDt"],
                  ["địa chỉ, các bên", "dòng chữ tự do", "mỗi phần có thẻ riêng (có cấu trúc)"]]),
           """ Từ hai mươi hai tháng mười một năm hai nghìn không trăm hai mươi lăm, chỉ thị thanh toán giữa các định chế tài chính trên mạng chỉ dùng chuẩn mới.
           Bản tin cũ được thay bằng bản tin mới, ba mã chịu phí cũ đổi thành ba mã mới, và số tiền, đồng tiền, ngày nay tách thành các thẻ riêng.""",
           clear=True),
    ])

    form = sc("formula", "formula", "Suy ra từng bước: kiểm IBAN, đổi tiền, ghi sổ", [
        st("""<p><b>Bước 1.</b> Đưa 4 ký tự đầu <b>GB82</b> ra cuối: <code>WEST12345698765432GB82</code>. Vì số kiểm được tính khi mã quốc gia và số kiểm đứng sau cùng, ta phải xếp lại đúng như lúc tính.</p>
<span class='note'>Làm thử: chuỗi vẫn đủ 22 ký tự.</span>""",
           """Bước một, ta đưa bốn ký tự đầu ra cuối chuỗi. Vì số kiểm được tính khi mã quốc gia và hai chữ số kiểm đứng sau cùng, nên ta phải xếp lại đúng như lúc tính.
"""),
        st("""<p><b>Bước 2.</b> Đổi mỗi chữ cái thành số: A = 10, B = 11, …, Z = 35. Vì phép chia chỉ làm trên số, chữ phải thành số theo một bảng cố định.</p>
<span class='note'>Làm thử: W = 32, E = 14, S = 28, T = 29, G = 16, B = 11 nên đầu chuỗi WEST thành 32142829.</span>""",
           """Bước hai, ta đổi mỗi chữ cái thành số, A là mười, B là mười một, cứ thế tới Z là ba mươi lăm. Vì phép chia chỉ làm trên số, nên chữ phải đổi thành số theo một bảng cố định.
           Làm thử, bốn chữ W E S T thành ba mươi hai, mười bốn, hai mươi tám, hai mươi chín."""),
        st(table(["cách viết trong Python", "nghĩa"],
                 [["<code>iban[4:] + iban[:4]</code>", "lát cắt: từ ký tự thứ 4 trở đi (đếm từ 0), nối với 4 ký tự đầu"],
                  ["<code>int(c, 36)</code>", "đọc ký tự <code>c</code> như một chữ số của hệ 36: chữ số giữ nguyên, <code>A</code> = 10 … <code>Z</code> = 35"],
                  ["<code>for c in s:</code>", "lặp lần lượt từng ký tự <code>c</code> của chuỗi <code>s</code>, mỗi lần chạy các dòng thụt vào dưới nó"],
                  ["<code>so += str(…)</code>, <code>% 97</code>", "nối thêm vào chuỗi <code>so</code>; lấy dư khi chia cho 97"]]),
           """Mã Python sắp tới có vài cách viết mới, nên ta giải nghĩa trước. Lát cắt lấy một đoạn chuỗi, hàm đổi ký tự theo hệ ba mươi sáu cho chữ cái thành số, vòng lặp đi qua từng ký tự, và dấu phần trăm lấy số dư.""", clear=True),
        st(code(IBAN_PY, "Bước 3. Chia cho 97 lấy dư: đúng thì dư bằng 1") + out(IBAN_OUT),
           """Bước ba, ta cho Python làm cả ba việc. Câu lệnh thứ hai xếp lại chuỗi, vòng lặp đổi từng ký tự thành số theo cơ số ba mươi sáu, trong đó A là mười.
           Máy in chuỗi đã xếp, chuỗi hai mươi tám chữ số, và số dư khi chia chín mươi bảy bằng một.""",
           focus=[1, 2, 4], clear=True),
        st("""<p><b>Bước 4.</b> Vì sao đúng thì dư bằng 1? Vì người lập IBAN chọn số kiểm sao cho dư bằng 1: đặt <code>00</code> vào chỗ số kiểm, lấy dư $r$, rồi số kiểm $= 98 - r$.</p>
$$98 - 16 = 82$$""",
           """Bước bốn, vì sao đúng thì dư bằng một? Vì người lập số đã chọn hai chữ số kiểm sao cho dư bằng một.
           Họ đặt hai số không vào chỗ số kiểm và lấy dư, ở đây là mười sáu. Chín mươi tám trừ mười sáu bằng tám mươi hai, đúng hai chữ số kiểm của mẫu.""",
           focus=[1, 1, 1, 2], clear=True),
        st(table(["cách viết trong Python", "nghĩa"],
                 [["<code>from decimal import Decimal, ROUND_HALF_UP</code>", "nạp kiểu số thập phân chính xác <code>Decimal</code> và kiểu làm tròn nửa lên; <code>Decimal(&quot;1000&quot;)</code> không làm tròn ngầm như số thực"],
                  ["<code>def tron(x, ccy): … return …</code>", "định nghĩa hàm nhận <code>x</code> và đồng tiền <code>ccy</code>; <code>return</code> trả kết quả ra"],
                  ["<code>Decimal(1).scaleb(-2)</code>", "<code>scaleb</code> dịch dấu phẩy: <code>Decimal(1).scaleb(-2)</code> là 0,01; <code>scaleb(0)</code> là 1; dùng làm mẫu số chữ số lẻ"],
                  ["<code>x.quantize(mau, rounding=ROUND_HALF_UP)</code>", "làm tròn <code>x</code> theo mẫu số chữ số lẻ; nửa trở lên thì làm tròn lên"],
                  ["<code>CHU_SO_LE = {&quot;USD&quot;: 2, &quot;VND&quot;: 0}</code>", "từ điển: đồng tiền → số chữ số lẻ theo ISO 4217"]]),
           """Mã đổi tiền có vài cách viết mới, nên ta giải nghĩa trước. Dòng nạp lấy kiểu số chính xác và kiểu làm tròn. Hàm nhận số tiền và đồng tiền rồi trả kết quả. Phép dịch dấu phẩy tạo mẫu số chữ số lẻ, hàm làm tròn nhận mẫu đó, và từ điển ghi mỗi đồng tiền có mấy chữ số lẻ.""", clear=True),
        st(code(FX_PY, "Bước 5. Đổi tiền bằng số thập phân chính xác, làm tròn theo từng đồng tiền") + out(FX_OUT),
           """Bước năm là đổi tiền. Vì máy lưu số thực theo nhị phân mà không phẩy một là số lặp vô hạn, nên nó bị cắt và không đúng hẳn. Ta dùng kiểu số thập phân chính xác, số chữ số lẻ theo chuẩn ISO bốn hai một bảy, làm tròn nửa lên.
           Máy in hai mươi lăm triệu bốn trăm nghìn đồng, và chín trăm tám mươi lăm đô la sau khi trung gian trừ mười lăm đô la.""",
           focus=[1, "2.1", 4], clear=True),
        st(table(["đồng tiền", "tài khoản (tên minh hoạ)", "Nợ", "Có"],
                 [["VND", "tiền gửi của khách", "25 400 000", ""], ["VND", "mua bán ngoại tệ (VND)", "", "25 400 000"],
                  ["USD", "mua bán ngoại tệ (USD)", "1 000", ""], ["USD", "nostro USD tại ngân hàng C", "", "1 000"]]),
           """Bước sáu là ghi sổ ở ngân hàng A, và mỗi đồng tiền phải tự cân. Vì không thể cộng đô la với đồng, nên ta tách hai vế qua tài khoản mua bán ngoại tệ của chính ngân hàng.
           Vế đồng: Nợ tiền gửi của khách hai mươi lăm triệu bốn trăm nghìn, Có tài khoản mua bán ngoại tệ. Vế đô la: Nợ tài khoản mua bán ngoại tệ một nghìn, Có tài khoản ở nước ngoài một nghìn.""",
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
           """ Chuyển một nghìn đô la, tỉ giá bán hai mươi lăm nghìn bốn trăm, phí trung gian mười lăm đô la, phí ngân hàng gửi năm đô la, đều là số minh hoạ.
           Phép tính thứ nhất, tiền gốc chưa tính phí bằng hai mươi lăm triệu bốn trăm nghìn đồng."""),
        st("""<p>Chia phí (SHA): người gửi trả phí ngân hàng mình riêng; phí trung gian trừ vào tiền chuyển.</p>
$$② \\; 1\\,000 - 15 = \\hl{985} \\text{ USD người nhận được}$$""",
           """Phép tính thứ hai, với cách chia phí, người gửi trả phí ngân hàng của mình riêng, còn phí trung gian trừ thẳng vào tiền chuyển.
           Vì vậy người nhận được chín trăm tám mươi lăm đô la, đúng con số ở đầu bài."""),
        st("""<p>Người gửi chịu hết (OUR): người nhận <b>thường</b> được đủ 1 000 (theo mô hình, nếu không ngân hàng nào trừ thêm); người gửi trả thêm phí ngân hàng mình và phí trung gian.</p>
$$③ \\; 1\\,000 + 5 + 15 = \\hl{1\\,020} \\text{ USD người gửi trả}$$""",
           """Phép tính thứ ba, với cách người gửi chịu hết, người nhận thường được đủ một nghìn đô la, nếu không ngân hàng nào trừ thêm. Người gửi trả một nghìn cộng năm cộng mười lăm, bằng một nghìn không trăm hai mươi đô la."""),
        st("""<p>Dùng lại $1\\,020$ ở phép ③, đổi ra đồng:</p>
$$④ \\; 1\\,020 \\cdot 25\\,400 = \\hl{25\\,908\\,000} \\text{ đồng, hơn tiền gốc ở phép ① là } 508\\,000$$""",
           """Phép tính thứ tư, dùng lại một nghìn không trăm hai mươi đô la, nhân hai mươi lăm nghìn bốn trăm, bằng hai mươi lăm triệu chín trăm lẻ tám nghìn đồng.
           So với tiền gốc, khách trả thêm năm trăm lẻ tám nghìn đồng.""", clear=True),
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
           """Kiểm bằng đường khác. Thay vì dựng số hai mươi tám chữ số, ta đi qua từng chữ số và chỉ giữ số dư.
           Mỗi bước nhân số dư cũ với mười, cộng chữ số mới rồi lấy dư, vì phép lấy dư đi qua được phép cộng và phép nhân. Máy in một, khớp cách tính cả số.""",
           focus=[2, "2.4", "2.4", 4, 0]),
        st(table(["điều cần kiểm", "đường khác", "kết quả"],
                 [["① 25 400 000 đồng", "chia ngược: 25 400 000 ÷ 25 400", "= 1 000 USD"],
                  ["② 985 USD (SHA)", "cộng lại: 985 + 15", "= 1 000 USD"],
                  ["bút toán ở bước 6", "tổng Nợ trừ tổng Có, từng đồng tiền", "VND: 0; USD: 0"]]),
           """Bảng này kiểm ba kết quả còn lại bằng phép ngược. Vì phép chia ngược phép nhân, hai mươi lăm triệu bốn trăm nghìn chia cho tỉ giá được đúng một nghìn đô la. Chín trăm tám mươi lăm cộng mười lăm phí cũng được một nghìn.""",
           clear=True),
    ], checks=["(lambda s: __import__('functools').reduce(lambda d, c: (d * 10 + int(c)) % 97, s, 0))(alg.bnx_iban_digits('GB82WEST12345698765432')) == 1",
               "alg.bnx_fx_vnd(1000, 25400) // 25400 == 1000 and alg.bnx_fx_vnd(1000, 25400) % 25400 == 0",
               "alg.bnx_fee(1000, 'SHA', 0, 15)[1] + 15 == 1000",
               "set(alg.bnx_balanced_by_ccy(alg.bnx_nostro_entries('1000', '25400')).values()) == {0}"])

    quymo = sc("quymo", "example", "Khi giao dịch lớn dần và chạy lâu: phí cố định và sai số dấu phẩy động", [
        st(table(["cách viết trong Python", "nghĩa"],
                 [["<code>for _ in range(n):</code>", "lặp <code>n</code> lần; <code>_</code> là tên biến bỏ đi, không dùng giá trị"],
                  ["<code>f, d = 0.0, Decimal(0)</code>", "gán hai biến cùng lúc: <code>f</code> là số thực, <code>d</code> là số thập phân chính xác"],
                  ["<code>f += 0.10</code>", "cộng thêm 0,10 vào <code>f</code>"]]),
           """Khối đo dùng thêm vài cách viết, nên ta giải nghĩa trước. Vòng lặp chạy đúng n lần, dấu gạch dưới là tên biến bỏ đi, và hai biến cùng cộng một khoản nhỏ mỗi lần.""", clear=True),
        st(P_SCALE.show(title="Đo thật: cộng 0,10 nhiều lần bằng số thực dấu phẩy động và bằng số thập phân chính xác")
           + P_SCALE.out_html(),
           """ Mỗi vòng cộng không phẩy mười, như một khoản phí nhỏ, bằng hai kiểu số, ở ba cỡ mười, mười nghìn và một triệu lần.
 Với mười nghìn lần, số thực lệch ở chữ số thập phân thứ mười. Với một triệu lần, lệch ở chữ số thập phân thứ sáu, còn số thập phân chính xác luôn đúng.
 Vì thế tiền lưu bằng số thập phân chính xác hoặc số nguyên theo đơn vị nhỏ nhất.""",
           focus=[2, 4, "4.2", "4.3", "4.3"], clear=True),
        st(table(["số tiền chuyển (USD)", "SHA: người nhận được", "thiếu so với hoá đơn (phí trung gian 15)", "một phí cố định khác, 20 USD, chiếm (số minh hoạ)"],
                 [["1 000", "985", "15", "2 %"],
                  ["100 000 (gấp 100 lần)", "99 985", "15", "0,02 %"],
                  ["10 000 000 (gấp 10 000 lần)", "9 999 985", "15", "0,0002 %"]]),
           """Phí cố định đổi ý nghĩa theo quy mô. Phí cố định hai mươi đô la là một khoản khác với mười lăm đô la của trung gian, và ở cỡ lớn gấp mười nghìn lần chỉ còn chiếm hai phần mười nghìn của một phần trăm.
           Nhưng chỗ thiếu mười lăm đô la của cách chia phí không đổi. Vì hoá đơn chỉ tất toán khi nhận đủ, người nhận ở mọi cỡ vẫn phải xử lý chuyển bù.""",
           focus=[0, 1, "1.2", "1.3", "1.4", 0], clear=True),
    ], checks=["[repr(alg.bnx_l11_float_sum(n)) for n in (10, 10000, 1000000)] == ['0.9999999999999999', '1000.0000000001588', '100000.00000133288']",
               "[alg.bnx_l11_fixed_fee_pct(a, 20) for a in (1000, 100000, 10000000)] == ['2', '0.02', '0.0002']",
               "[str(alg.bnx_fee(a, 'SHA', 0, 15)[1]) for a in (1000, 100000, 10000000)] == ['985.00', '99985.00', '9999985.00']",
               "100000 // 1000 == 10000000 // 100000 == 100 and 10000000 // 1000 == 10000"])

    pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, có lỗi của người đã đi làm", [
        st("""<div class="box warn"><b>Lỗi 1 (người đã đi làm).</b> Chọn chia phí (SHA) cho một hoá đơn phải trả <b>đủ</b> 1 000 USD. Người nhận được 985 USD, hoá đơn còn nợ 15 USD và phải chuyển thêm một lần nữa, lại mất phí. Chọn OUR cũng <b>chưa chắc</b> nhận đủ.
<br><span class="note">Phép thử: đối chiếu số tiền người nhận báo có với số trên hoá đơn; ngân hàng trung gian hoặc ngân hàng nhận <b>có thể</b> trừ phí kể cả khi chọn OUR.</span></div>""",
           """Lỗi thứ nhất, của người đã đi làm, là chọn chia phí cho hoá đơn phải trả đủ một nghìn đô la. Người nhận chỉ được chín trăm tám mươi lăm, còn thiếu mười lăm, phải chuyển thêm và lại mất phí. Chọn người gửi chịu hết cũng chưa chắc đủ, vì ngân hàng trung gian hoặc ngân hàng nhận vẫn có thể trừ phí, nên luôn đối chiếu số báo có.""", clear=True),
        st("""<div class="box warn"><b>Lỗi 2 (người đã đi làm).</b> Coi IBAN “qua phép chia 97” là <b>tài khoản đúng người</b>. Phép kiểm chỉ bắt lỗi gõ: đổi chỗ hai chữ số cuối thì dư 49, nhưng một số hợp lệ của người khác vẫn dư 1.
<br><span class="note">Cách chữa: kiểm số trước khi gửi, rồi vẫn đối chiếu tên người nhận và xử lý lệnh bị trả về.</span></div>""",
           """Lỗi thứ hai, của người đã đi làm, là coi số tài khoản quốc tế qua phép chia chín mươi bảy là đúng người nhận.
           Phép kiểm chỉ bắt lỗi gõ, như đổi chỗ hai chữ số cuối thì dư bốn mươi chín, nhưng số hợp lệ của người khác vẫn dư một.
           Cách chữa là kiểm số rồi vẫn đối chiếu tên người nhận."""),
    ], checks=["alg.bnx_iban_mod97('GB82WEST12345698765423') == 49",
               "1000 - alg.bnx_fee(1000, 'SHA', 0, 15)[1] == 15"])

    quiz = sc("quiz", "quiz", "Đến lượt bạn", [
        st(table(["câu", "đề"],
                 [["1", "Khách gõ GB82WEST12345698765423 (hai chữ số cuối đổi chỗ). Chuỗi số sau khi xếp lại và đổi chữ là 3214282912345698765423161182, chia 97 dư 49. Hệ thống làm gì?"],
                  ["2", "Chuyển 2 500 USD, tỉ giá bán 25 400, chia phí, ngân hàng gửi không thu phí, trung gian trừ 20 USD (số minh hoạ). Khách trả bao nhiêu đồng, người nhận được bao nhiêu?"],
                  ["3", "Quyết định: khách trả một hoá đơn phải nhận đủ 2 500 USD. Khuyên chọn người gửi chịu hết (OUR) hay chia phí (SHA)?"],
                  ["4", "Ngân hàng A chuyển 1 000 USD qua tài khoản nostro USD mở ở ngân hàng C. Sổ của A ghi Nợ hay Có, sổ của C ghi Nợ hay Có, ở tài khoản nào?"],
                  ["5", "Lệnh chuyển tiền cho khách hàng, chọn chia phí: bản tin MT cũ và bản tin ISO 20022 mới gọi tên gì, và mã chịu phí viết thế nào?"]]),
           """Đến lượt bạn, năm câu trên màn hình. Câu ba chọn cách chịu phí cho hoá đơn phải nhận đủ. Hãy dừng video và làm ra giấy.""",
           pause=40),
        st("""<p>Câu 1: dư phải bằng 1 mới qua.</p>
$$49 \\neq 1 \\;\\Rightarrow\\; \\text{từ chối ngay, báo khách gõ lại}$$""",
           """Đáp án câu một. Số dư phải bằng một mới qua, mà ở đây là bốn mươi chín, khác một. Dấu gạch chéo qua dấu bằng nghĩa là khác, mũi tên đôi nghĩa là suy ra. Vì vậy hệ thống từ chối ngay.""",
           introduces=["neq"]),
        st("""$$2\\,500 \\cdot 25\\,400 = \\hl{63\\,500\\,000} \\text{ đồng};\\quad 2\\,500 - 20 = \\hlg{2\\,480} \\text{ USD}$$""",
           """Đáp án câu hai. Khách trả hai nghìn năm trăm nhân hai mươi lăm nghìn bốn trăm, bằng sáu mươi ba triệu năm trăm nghìn đồng.
           Vì chia phí nên người nhận được hai nghìn năm trăm trừ hai mươi, bằng hai nghìn bốn trăm tám mươi đô la."""),
        st(table(["lựa chọn", "được", "mất"],
                 [["người gửi chịu hết (OUR)", "người nhận thường nhận đủ 2 500, hoá đơn thường tất toán một lần", "khách trả thêm phí; phí trung gian khó biết trước; vẫn phải đối chiếu số báo có vì ngân hàng nhận có thể trừ phí"],
                  ["chia phí (SHA)", "khách trả ít phí hơn", "người nhận có thể thiếu, phải chuyển bù một lần nữa và lại mất phí"]]),
           """Đáp án câu ba. Chọn người gửi chịu hết thì người nhận thường nhận đủ và hoá đơn thường tất toán một lần, đổi lại khách trả thêm phí.
           Chia phí thì khách trả ít hơn, nhưng người nhận có thể thiếu. Với hoá đơn phải nhận đủ, nên khuyên người gửi chịu hết."""),
        st(table(["câu", "kết quả", "vì sao"],
                 [["4", "sổ A: ghi <b>Có</b> nostro USD tại C, giảm 1 000; sổ C: ghi <b>Nợ</b> vostro của A, giảm 1 000", "nostro là tài sản của A, vostro là nợ phải trả của C: ghi Có giảm tài sản, ghi Nợ giảm nợ phải trả"],
                  ["5", "MT103 trường 71A = SHA; pacs.008 thẻ ChrgBr = SHAR", "cùng một ý chia phí, nay có thẻ riêng trong bản tin có cấu trúc"]]),
           """Đáp án câu bốn. Sổ A ghi Có tài khoản ở nước ngoài, giảm một nghìn, vì đó là tài sản của A. Sổ C ghi Nợ tài khoản của A, cũng giảm một nghìn, vì đó là khoản C nợ A.
           Đáp án câu năm. Bản tin cũ ghi chia phí ở trường bảy mươi mốt A, còn bản tin mới ghi ở thẻ chịu phí.""",
           focus=["1.2", "1.2", "1.3", "1.3"], clear=True),
    ], checks=["alg.bnx_iban_digits('GB82WEST12345698765423') == '3214282912345698765423161182'",
               "alg.bnx_iban_mod97('GB82WEST12345698765423') == 49 and 49 != 1",
               "alg.bnx_fx_vnd(2500, 25400) == 63500000", "alg.bnx_fee(2500, 'SHA', 0, 20)[1] == 2480",
               "alg.bnx_fee(2500, 'OUR', 0, 20)[1] == 2500",
               "alg.bnx_nostro_entries('1000', '25400')[3][0] == 'USD' and alg.bnx_nostro_entries('1000', '25400')[3][2] == 0 and alg.bnx_nostro_entries('1000', '25400')[3][3] == 1000"])

    lab_pr = practice_scene(sc, "Tự làm: đọc BIC, kiểm IBAN và tính ba cách chịu phí", practice_steps2(
        st, "BNX", "L11",
        """<p><b>Đề</b>: viết <code>mau.py</code> (Python, in không dấu), số liệu là số minh hoạ:</p>
<ol><li>BIC <code>ABCDDEFFXXX</code>: tách mã tổ chức, mã quốc gia, mã địa điểm, mã chi nhánh và in một dòng</li>
<li>IBAN <code>GB90BANK98765432101234</code> và bản đổi chỗ hai ký tự cuối: xếp lại (4 ký tự đầu ra cuối), đổi chữ thành số (A = 10 … Z = 35), chia 97 lấy dư; in dư và <code>hop le</code> (dư 1) hoặc <code>khong hop le</code></li>
<li>chuyển 2 000 USD, phí ngân hàng gửi 8, phí trung gian 12: in số người nhận được theo OUR, SHA, BEN và số người gửi trả theo OUR</li></ol>
<p class="note">Chữ in ra phải đúng từng ký tự như kết quả mong đợi.</p>""",
        """Bây giờ tới phần bạn tự làm. Viết chương trình tách mã định danh ngân hàng thành bốn phần, kiểm một số tài khoản quốc tế và bản gõ nhầm của nó, rồi tính ba cách chịu phí cho hai nghìn đô la. Hãy dừng video và tự viết.""",
        LAB_OUT, "mau.py",
        """<div class="box key"><b>Nếu kẹt:</b> đổi từng ký tự bằng <code>str(int(c, 36))</code>, ghép lại rồi <code>int(...) % 97</code>. Phí: OUR người gửi trả thêm cả hai phí; SHA trừ phí trung gian khỏi tiền nhận; BEN trừ cả hai.
Lời giải đầy đủ ở <code>labs/BNX/L11/loi_giai.py</code> — chỉ mở sau khi bạn đã thử.</div>""",
        """Nếu kẹt, đổi từng ký tự thành số bằng cơ số ba mươi sáu, ghép lại rồi chia chín mươi bảy lấy dư. Về phí, người gửi chịu hết thì trả thêm cả hai phí, chia phí thì trừ phí trung gian khỏi tiền nhận, người nhận chịu thì trừ cả hai.""", pause=120), "BNX", "L11")

    rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        st(chain("BIC + IBAN (kiểm chia 97)", "bản tin pacs.008", "nostro ở A = vostro ở C", "tỉ giá + phí OUR/SHA/BEN", "số thập phân, số chữ số lẻ theo ISO 4217, làm tròn nửa lên"),
           """Mã định danh và số tài khoản quốc tế cho biết gửi tới đâu, và phép chia chín mươi bảy bắt lỗi gõ. Lệnh đi bằng bản tin chuẩn, còn tiền đi qua tài khoản của chúng tôi ở ngân hàng nước ngoài. Số tiền phụ thuộc tỉ giá và cách chịu phí.""",
           focus=[0, "1.1", "1.3", "1.5", "1.7", "1.9"]),
        st("""<div class='box key'><b>Tư duy:</b> trong thanh toán quốc tế, <b>lệnh</b> và <b>tiền</b> đi hai đường khác nhau. Lệnh đi bằng bản tin; tiền chỉ đổi số dư trong sổ của từng ngân hàng, và mỗi trạm có thể trừ phí.</div>""",
           """Điều cần mang theo: trong thanh toán quốc tế, lệnh và tiền đi hai đường khác nhau. Lệnh đi bằng bản tin, còn tiền chỉ đổi số dư trong sổ của từng ngân hàng, và mỗi trạm có thể trừ phí."""),
        st("""<p class='small'>Bài sau: ví điện tử và nộp thuế điện tử — tiền trong ví thật ra nằm ở đâu, và khi nào một khoản nộp thuế mới thật sự xong.</p>""",
           """Bài sau học ví điện tử và nộp thuế điện tử, tức tiền trong ví nằm ở đâu và khi nào nộp thuế mới xong.""",
           forward_ref=True),
    ])
    return lesson("L11", "thanh_toan_quoc_te_ngoai_te", "Bài 11 — Thanh toán quốc tế và ngoại tệ: SWIFT, ISO 20022, tài khoản nostro và tỉ giá",
                  "curriculum/bnx.yaml L11; audit/bnx/verify_bnx.py L11; audit/bnx/sources.md [CBPR] [IBAN] [BIC] [ISO4217] [MT71A] [P8UG] [P8BNY] [NOSTRO]: "
                  "ISO 13616:2020 (IBAN, mod 97), ISO 9362:2022 (BIC), ISO 4217 danh sách SIX công bố 2026-09-17, Swift Category 1 MT Message Reference Guide 19/07/2024 (MT103 trường 71A), "
                  "CBPR+ pacs.008.001.08 Usage Guideline SR2025 13/12/2024, BNY 'A deep dive on pacs.008' (02/2021), Clearstream CBPR+ (cập nhật 03/11/2026); tỉ giá, phí, BIC WESTGB2L là số/mã minh hoạ",
                  ["Đọc mã BIC và kiểm số IBAN", "Ghi bút toán chuyển tiền quốc tế qua tài khoản nostro",
                   "Tính số tiền khi đổi ngoại tệ và chịu phí theo OUR, SHA, BEN", "Nêu thay đổi từ bản tin MT sang ISO 20022",
                   "So sánh phần trăm phí cố định và sai số cộng dồn của số thực ở ba cỡ giao dịch"],
                  [hook, pre, sym, intu, form, ex, chk, quymo, pit, quiz, lab_pr, rec],
                  covers=[(1, "practice"), (2, "formula"), (3, "example"), (4, "intuition"), (5, "quymo")])


LAB_DE = """# Lab BNX L11 — Đọc BIC, kiểm IBAN bằng phép chia 97 và tính ba cách chịu phí (không cần mạng)

Viết `mau.py` (Python 3, chỉ thư viện chuẩn), in đúng năm dòng như `mong_doi.txt`. Số liệu là số minh hoạ, không phải tỉ giá hay biểu phí của ngân hàng nào.

1. BIC `ABCDDEFFXXX`: in `BIC ABCDDEFFXXX: to chuc <4 ký tự>, quoc gia <2>, dia diem <2>, chi nhanh <3 ký tự>` (không có chi nhánh thì in `-`).
2. IBAN `GB90BANK98765432101234` và bản đổi chỗ hai ký tự cuối: đưa 4 ký tự đầu ra cuối, đổi mỗi chữ thành số (A = 10, …, Z = 35, chữ số giữ nguyên), chia 97 lấy dư. In `<IBAN>: du <r> -> hop le` nếu r = 1, ngược lại `khong hop le`.
3. Chuyển 2 000 USD, phí ngân hàng gửi 8, phí trung gian 12: in `nguoi nhan: OUR <số> SHA <số> BEN <số>` rồi `nguoi gui tra: OUR <số>`.

Chạy: `python mau.py`. Chấm: `bash labs/cham.sh BNX L11 mau.py`.
"""

# Lab ghi lúc import để gen và lab_gate cùng thấy (ghi đè mỗi lần, tất định)
from labkit import write_lab, practice_steps, practice_scene  # noqa: E402,F401
write_lab("BNX", "L11", LAB_DE, "py", LAB_PY, LAB_OUT)
