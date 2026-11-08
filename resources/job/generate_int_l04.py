import os
import yaml
import re

os.makedirs(r"D:\research-video\lessons\int", exist_ok=True)

SENT_RE = re.compile(r"(?<=[.!?…])\s+(?=[^\s])")

def count_sentences(text):
    text = " ".join(str(text).split())
    return len([s for s in SENT_RE.split(text) if s.strip()])

def build_step(show, say, clear=False, pause=None):
    n_sents = count_sentences(say)
    step = {
        "show": show,
        "focus": [0] * n_sents,
        "say": say
    }
    if clear:
        step["clear"] = True
    if pause is not None:
        step["pause"] = pause
    return step

def save_spec(data, path):
    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True, sort_keys=False)
    print(f"Saved {path}")

# =========================================================================
# LESSON 4: NGHIỆP VỤ NGÂN HÀNG TOÀN DIỆN, CORE T24 & CỔNG NAPAS
# =========================================================================
l04 = {
    "id": "L04",
    "course": "INT",
    "series": "Giáo trình Phỏng vấn Senior Banking ACB",
    "title": "Chuyên đề 4 — Nghiệp vụ Ngân hàng Core T24 và NAPAS 247",
    "voice": "piper:vi_VN-vais1000-medium",
    "rate": "-5%",
    "depth": "full",
    "source": "interview/04_banking_domain_t24_napas.md; Temenos T24 OFS XML Guide; NAPAS 247 ISO 8583 Technical Specification 2026",
    "assumes": ["arith", "approx", "log"],
    "objectives": [
        "Làm chủ bản tin OFS XML trên Temenos T24 và kết nối hàng đợi IBM MQ bất đồng bộ",
        "Nắm vững cấu trúc bản tin ISO 8583 MTI 0200 cổng NAPAS 247 và bảo mật giải mã PIN",
        "Bao quát 6 trụ cột tín dụng bán lẻ Squad Lending: Thấu chi sổ tiết kiệm, lương, thẻ và cổng CIC"
    ],
    "scenes": [
        {
            "id": "hook",
            "kind": "hook",
            "title": "Vòng đời Bản tin Chuyển tiền Liên ngân hàng NAPAS 247",
            "steps": [
                build_step(
                    """<p>Khi khách hàng bấm nút chuyển tiền nhanh 247 trên ứng dụng ngân hàng số ACB, gói tin di chuyển qua những trạm kiểm soát nào?</p>
<div class="box key">Chỉ trong vòng 1.5 giây, hệ thống phải trích nợ sổ cái Core T24, mã hóa gói tin ISO 8583 qua cổng chuyển mạch NAPAS, giải mã khối PIN qua thiết bị bảo mật phần cứng HSM và đối soát cuối ngày. Làm sao làm chủ trọn vẹn?</div>""",
                    "Chào bạn, một lệnh chuyển tiền nhanh liên ngân hàng diễn ra chỉ trong một giây nhưng phải đi qua hàng loạt chốt kiểm soát an ninh nghiêm ngặt. Hệ thống phải vừa hạch toán sổ cái ngân hàng lõi, vừa đóng gói bản tin tài chính quốc tế và bảo vệ khối mã pin bằng phần cứng chuyên dụng. Hôm nay, ta cùng nhau khám phá bức tranh nghiệp vụ ngân hàng toàn diện."
                ),
                build_step(
                    """<table class="t">
  <tr><th>trụ cột nghiệp vụ</th><th>tiêu chuẩn kỹ thuật lõi</th><th>phân hệ tích hợp</th></tr>
  <tr><td>Ngân hàng lõi Temenos T24</td><td>Bản tin OFS XML qua hàng đợi IBM MQ bất đồng bộ</td><td>Bộ điều hợp chuyển đổi dữ liệu và hạch toán sổ cái</td></tr>
  <tr><td>Chuyển mạch NAPAS 247</td><td>Chuẩn ISO 8583 qua giao thức kết nối TCP nhị phân</td><td>Cổng thanh toán liên ngân hàng và giải mã HSM</td></tr>
  <tr><td>Tín dụng số Squad Lending</td><td>Phong tỏa sổ cái hai pha, cấp thấu chi và cổng CIC</td><td>Hệ thống quản lý khoản vay và ký số đám mây</td></tr>
</table>
<p>Hôm nay, ta làm chủ: <b>Tích hợp Core T24</b>, <b>chuyển mạch NAPAS 247</b>, và <b>sáu trụ cột tín dụng bán lẻ</b>.</p>""",
                    "Hôm nay, ta cùng nhau khám phá ba trụ cột nghiệp vụ cốt lõi của ngân hàng thương mại. Ta tìm hiểu cách giao tiếp với ngân hàng lõi qua bản tin đặc tả mở. Ta nắm vững quy chuẩn gói tin chuyển mạch liên ngân hàng quốc tế. Ta cũng làm chủ toàn bộ hệ sinh thái tín dụng bán lẻ tốc độ cao.",
                    clear=True
                )
            ]
        },
        {
            "id": "prereq",
            "kind": "prereq",
            "title": "Ôn lại: Bản tin OFS XML, Mã giao dịch MTI và Thiết bị Bảo mật HSM",
            "checks": [
                "8000 * 60 == 480000",
                "1500 - 120 == 1380"
            ],
            "steps": [
                build_step(
                    """<p><b>Ba khái niệm then chốt trong hạ tầng thanh toán ngân hàng</b>:</p>
<table class="t">
  <tr><th>khái niệm</th><th>định nghĩa kỹ thuật</th><th>vai trò trong giao dịch</th></tr>
  <tr><td>Temenos T24 OFS XML</td><td>Định dạng bản tin mở giao tiếp trực tiếp với ngân hàng lõi</td><td>Hạch toán tài khoản tiền gửi, tiền vay và hạn mức</td></tr>
  <tr><td>NAPAS 247 ISO 8583</td><td>Giao thức nhị phân chuẩn tài chính thẻ và chuyển khoản</td><td>Định tuyến lệnh chuyển tiền liên ngân hàng tức thời</td></tr>
  <tr><td>Thiết bị HSM</td><td>Hộp phần cứng bảo mật chuyên dụng mã hóa khối mã PIN</td><td>Bảo vệ mã pin thẻ không bị giải mã trong bộ nhớ máy chủ</td></tr>
</table>""",
                    "Trước tiên ta ôn lại ba khái niệm then chốt trong thanh toán ngân hàng. Bản tin mở của ngân hàng lõi giúp giao tiếp trực tiếp với sổ cái tài khoản. Giao thức chuyển mạch liên ngân hàng điều phối dòng tiền giữa các tổ chức tín dụng. Thiết bị bảo mật phần cứng bảo đảm mã pin thẻ luôn được mã hóa tuyệt đối."
                ),
                build_step(
                    """<div class="box key">Quy tắc mã tương quan trên IBM MQ: Để tránh làm nghẽn luồng xử lý của ngân hàng lõi, ta luôn dùng mô hình yêu cầu phản hồi bất đồng bộ. Mỗi bản tin gửi đi được gắn một mã tương quan duy nhất (JMSCorrelationID). Bộ điều hợp chỉ lắng nghe bản tin trả về có đúng mã định danh này!</div>""",
                    "Để tránh nghẽn kết nối khi giao tiếp với ngân hàng lõi, ta sử dụng mô hình gửi nhận bất đồng bộ qua mã tương quan. Ứng dụng gửi lệnh vào hàng đợi rồi giải phóng luồng ngay, sau đó chỉ nhận kết quả khi có bản tin trùng mã tương quan xuất hiện.",
                    clear=True
                )
            ]
        },
        {
            "id": "concept",
            "kind": "concept",
            "title": "Toàn cảnh Sáu Trụ cột Tín dụng Bán lẻ Squad Lending",
            "steps": [
                build_step(
                    """<p><b>Hệ sinh thái Tín dụng Bán lẻ Tốc độ cao gồm 6 phân hệ cốt lõi</b>:</p>
<svg viewBox="0 0 700 220" style="width:100%;max-height:200px;">
  <rect x="20" y="20" width="200" height="85" rx="6" fill="#e8f4fd" stroke="#003366"/>
  <text x="30" y="45" font-size="12" font-weight="bold" fill="#003366">1. Thấu chi Sổ tiết kiệm</text>
  <text x="30" y="68" font-size="11" fill="#555">Phong tỏa Core T24 AZ</text>
  <text x="30" y="88" font-size="11" fill="#555">Cấp hạn mức LTV 90%</text>
  <rect x="250" y="20" width="200" height="85" rx="6" fill="#d4edda" stroke="#28a745"/>
  <text x="260" y="45" font-size="12" font-weight="bold" fill="#155724">2. Thấu chi Lương tín chấp</text>
  <text x="260" y="68" font-size="11" fill="#555">Phân tích lô chi lương</text>
  <text x="260" y="88" font-size="11" fill="#555">Cấp hạn mức tự động 3x</text>
  <rect x="480" y="20" width="200" height="85" rx="6" fill="#fff3cd" stroke="#ffc107"/>
  <text x="490" y="45" font-size="12" font-weight="bold" fill="#856404">3. Vay trên Hạn mức Thẻ</text>
  <text x="490" y="68" font-size="11" fill="#555">Rút tiền mặt trả góp</text>
  <text x="490" y="88" font-size="11" fill="#555">Mở thẻ ảo dưới 60 giây</text>
  <rect x="20" y="120" width="200" height="85" rx="6" fill="#d1ecf1" stroke="#17a2b8"/>
  <text x="30" y="145" font-size="12" font-weight="bold" fill="#0c5460">4. Ký số Đám mây Cloud CA</text>
  <text x="30" y="168" font-size="11" fill="#555">Hợp đồng điện tử FPT</text>
  <text x="30" y="188" font-size="11" fill="#555">Khuôn mặt chuẩn 2345</text>
  <rect x="250" y="120" width="200" height="85" rx="6" fill="#f8d7da" stroke="#dc3545"/>
  <text x="260" y="145" font-size="12" font-weight="bold" fill="#721c24">5. Cổng CIC B2B Quốc gia</text>
  <text x="260" y="168" font-size="11" fill="#555">Tra cứu năm nhóm nợ xấu</text>
  <text x="260" y="188" font-size="11" fill="#555">Kiểm soát trần DTI 45%</text>
  <rect x="480" y="120" width="200" height="85" rx="6" fill="#e2e3e5" stroke="#6c757d"/>
  <text x="490" y="145" font-size="12" font-weight="bold" fill="#383d41">6. Giải ngân & Thu nợ</text>
  <text x="490" y="168" font-size="11" fill="#555">Khóa Redis 300 giây</text>
  <text x="490" y="188" font-size="11" fill="#555">Trích nợ từng phần</text>
</svg>""",
                    "Sáu trụ cột tín dụng bán lẻ bao quát trọn vẹn vòng đời một khoản vay số. Từ thấu chi cầm cố sổ tiết kiệm và thấu chi lương, đến vay tiền mặt trên hạn mức thẻ tín dụng. Quy trình được khép kín bằng ký số đám mây, tra cứu nợ xấu tại trung tâm thông tin tín dụng quốc gia và giải ngân an toàn."
                ),
                build_step(
                    """<div class="box key">Cơ chế thu nợ từng phần Partial Debit: Khi đến hạn thanh toán mà tài khoản khách hàng không đủ toàn bộ số tiền, hệ thống tự động trích nợ từng phần theo số dư khả dụng thay vì báo lỗi. Điều này giúp ngân hàng thu hồi tối đa nợ và bảo vệ điểm tín dụng cho khách hàng!</div>""",
                    "Một điểm sáng kỹ thuật là cơ chế trích nợ từng phần thông minh. Khi tài khoản không đủ số dư để trả toàn bộ, hệ thống sẽ tự động thu tối đa số tiền hiện có. Tính năng này giúp giảm tỉ lệ nợ xấu cho ngân hàng và hạn chế phát sinh phí phạt cho người vay.",
                    clear=True
                )
            ]
        },
        {
            "id": "symbol",
            "kind": "symbol",
            "title": "Cấu trúc Bản tin OFS XML và Gói tin ISO 8583 NAPAS",
            "checks": [
                "100000000 * 85 // 100 == 85000000",
                "300 // 60 == 5"
            ],
            "steps": [
                build_step(
                    r"""<p><b>Cấu trúc bản tin hạch toán Core T24 OFS XML</b>:</p>
<pre><code>FUNDS.TRANSFER,ACTP/I/PROCESS//0,USER123/PASS123,TX20261107,
DEBIT.ACCT.NO=12345678,
CREDIT.ACCT.NO=87654321,
DEBIT.AMOUNT=50000000,
DEBIT.CURRENCY=VND</code></pre>
<p>Bản tin gồm mã giao dịch, chế độ xử lý tức thời, thông tin xác thực, và các cặp trường giá trị hạch toán ghi nợ, ghi có.</p>""",
                    "Đây là cấu trúc bản tin mở chuẩn mực dùng để hạch toán vào hệ thống ngân hàng lõi. Bản tin khai báo tường minh tài khoản trích nợ, tài khoản thụ hưởng, số tiền chuyển khoản và loại tiền tệ hạch toán."
                ),
                build_step(
                    r"""<p><b>Cấu trúc bản tin chuyển mạch NAPAS 247 ISO 8583 MTI 0200</b>:</p>
<pre><code>Field 0 (MTI): 0200 (Yêu cầu chuyển tiền)
Field 3 (Processing Code): 400000 (Chuyển khoản liên ngân hàng)
Field 4 (Amount): 000005000000 (50,000,000 VND)
Field 11 (STAN): 123456 (Mã số thứ tự phiên giao dịch)
Field 37 (RRN): 202611070001 (Mã đối soát duy nhất 12 ký tự)
Field 52 (PIN Block): Khối mã pin đã mã hóa qua HSM</code></pre>""",
                    "Trong cổng chuyển mạch liên ngân hàng, gói tin tuân theo chuẩn quốc tế với các trường dữ liệu định dạng nhị phân. Mã số phiên và mã đối soát mười hai ký tự là căn cứ pháp lý duy nhất để đối soát giao dịch giữa các ngân hàng thành viên.",
                    clear=True
                )
            ]
        },
        {
            "id": "example",
            "kind": "example",
            "title": "Thực hành: Đối soát Ba bên Cuối ngày EOD bằng Thuật toán Hai con trỏ",
            "checks": [
                "3000000 // 1000000 == 3",
                "180 < 300",
                "100 - 90 == 10"
            ],
            "steps": [
                build_step(
                    """<p><b>Dữ liệu bài toán đối soát 3 bên cuối ngày tại ACB</b>:</p>
<ul>
  <li>Quy mô dữ liệu: $3\,000\,000$ giao dịch trong ngày giữa Core T24, NAPAS và Đối tác.</li>
  <li>Thời gian cho phép: Hoàn tất đối soát trong vòng 5 phút (300 giây).</li>
  <li>Nếu dùng vòng lặp quét lồng nhau O(N^2): Tốn hàng nghìn tỉ phép so sánh, làm tê liệt máy chủ!</li>
</ul>""",
                    "Ta xem xét bài toán đối soát cuối ngày với ba triệu giao dịch giữa ngân hàng lõi, cổng chuyển mạch và đối tác thu hộ. Thời gian quy định chỉ vỏn vẹn trong năm phút. Nếu dùng thuật toán duyệt lồng nhau thông thường, hệ thống sẽ chạy mất hàng tuần lễ."
                ),
                build_step(
                    """<p><b>Bước 1: Sắp xếp các tệp dữ liệu theo Mã đối soát RRN</b>:</p>
$$\text{Độ phức tạp sắp xếp: } O(N \log N) \text{ với thuật toán TimSort}$$
<div class="box key">Sau khi sắp xếp, cả 3 danh sách giao dịch đều có trật tự mã đối soát tăng dần!</div>""",
                    "Bước một, ta tiến hành sắp xếp các tệp dữ liệu theo mã đối soát tăng dần với độ phức tạp tối ưu. Sau bước này, toàn bộ hàng triệu bản ghi của ba bên đều nằm trên một đường thẳng có thứ tự hoàn hảo.",
                    clear=True
                ),
                build_step(
                    """<p><b>Bước 2: Duyệt đồng thời bằng Thuật toán Hai con trỏ O(N)</b>:</p>
<pre><code>// Duyệt tịnh tiến con trỏ i và j mà không bao giờ quay lui
while (i < coreList.size() && j < napasList.size()) {
    if (coreList[i].rrn == napasList[j].rrn) {
        matchTransaction(coreList[i], napasList[j]);
        i++; j++;
    } else if (coreList[i].rrn < napasList[j].rrn) {
        reportMissingInNapas(coreList[i]); i++;
    } else {
        reportMissingInCore(napasList[j]); j++;
    }
}</code></pre>""",
                    "Bước hai, ta áp dụng giải thuật hai con trỏ tịnh tiến đồng thời. Con trỏ chỉ duyệt tiến một chiều với độ phức tạp tuyến tính. Các giao dịch khớp nhau được ghi nhận tức thì, còn các lệnh lệch được tách riêng vào danh sách nghi vấn.",
                    clear=True
                ),
                build_step(
                    """<p><b>Bước 3: Kết quả thực nghiệm đối soát 3 triệu bản ghi</b>:</p>
<div class="box key">Thời gian hoàn tất: Chỉ mất 180 giây (3 phút) trên máy chủ tiêu chuẩn! Độ chính xác đạt 100%, tự động sinh danh sách bồi hoàn cho các giao dịch treo!</div>""",
                    "Bước ba, kết quả thực tế cho thấy toàn bộ ba triệu bản ghi được so khớp hoàn toàn chỉ trong một trăm tám mươi giây. Thuật toán tự động phát hiện các giao dịch bị lệch để chuyển sang luồng bồi hoàn tiền cho khách hàng.",
                    clear=True
                )
            ]
        },
        {
            "id": "check",
            "kind": "check",
            "title": "Tự Kiểm tra: Xử lý Bản tin Mã lỗi 68 Nghi vấn từ NAPAS",
            "checks": [
                "1014 - 1000 == 14",
                "68 > 0"
            ],
            "steps": [
                build_step(
                    """<p><b>Tình huống phỏng vấn Senior</b>: Khi gửi lệnh chuyển khoản 50 triệu qua NAPAS 247 mà cổng trả về mã phản hồi 68 (Giao dịch đang nghi vấn do ngân hàng thụ hưởng chưa trả lời kịp), hệ thống xử lý ra sao?</p>
<ul>
  <li>(A) Hoàn tiền ngay lập tức vào tài khoản người gửi.</li>
  <li>(B) Trừ tiền lần thứ hai và gửi lại gói tin.</li>
  <li>(C) Giữ nguyên trạng thái Chờ đối soát (In-doubt), không tự ý hoàn tiền hay trừ tiền kép, và tự động truy vấn lại sau 5 phút qua bản tin tra soát MTI 0400.</li>
</ul>""",
                    "Mời bạn trả lời tình huống xử lý mã lỗi nhạy cảm của cổng chuyển mạch. Khi phía chuyển mạch phản hồi mã sáu mươi tám báo hiệu giao dịch nghi vấn, kỹ sư tích hợp cấp cao sẽ điều khiển luồng tiền như thế nào."
                ),
                build_step(
                    """<p><b>Đáp án chính xác: Lựa chọn (C)</b></p>
<div class="box key">Giải thích vì: Mã lỗi 68 có nghĩa là ngân hàng thụ hưởng có thể đã cộng tiền cho người nhận nhưng chưa kịp phản hồi. Nếu ACB vội vàng hoàn tiền cho người gửi, ngân hàng sẽ bị thất thoát tài chính. Ta bắt buộc phải treo trạng thái và phát lệnh tra soát đối soát tự động!</div>""",
                    "Đáp án chính xác là lựa chọn C vì mã lỗi nghi vấn cho thấy người nhận có thể đã được cộng tiền. Nếu hệ thống vội vã hoàn tiền, ngân hàng sẽ chịu rủi ro mất vốn. Ta bắt buộc phải chuyển sang luồng tra soát tự động.",
                    clear=True
                )
            ]
        },
        {
            "id": "pitfall",
            "kind": "pitfall",
            "title": "Bẫy Nguy hiểm: Tin tưởng Tuyệt đối vào Mạng Viễn thông",
            "steps": [
                build_step(
                    """<div class="box pit">Sai lầm nghiêm trọng khi tích hợp cổng thanh toán liên ngân hàng:</div>
<table class="t" style="margin-top: 10px;">
  <tr><th>sai lầm sơ cấp</th><th>hiểm họa tài chính</th><th>giải pháp chuẩn Senior</th></tr>
  <tr><td>Cộng tiền khi nhận gói tin không xác thực</td><td>Bị tấn công làm giả gói tin chuyển tiền</td><td>Luôn kiểm tra mã xác thực toàn vẹn MAC bit 128</td></tr>
  <tr><td>Bỏ qua kiểm tra trùng lặp khóa phân tán</td><td>Khách hàng quẹt thẻ một lần bị trừ nợ hai lần</td><td>Khóa nguyên tử Redis theo mã phiên STAN và RRN</td></tr>
</table>""",
                    "Một sai lầm nguy hiểm là việc cộng tiền khi chưa xác thực mã kiểm tra toàn vẹn của gói tin. Kỹ sư phải luôn kiểm tra mã băm bảo mật và kích hoạt khóa khử trùng lặp để bảo vệ an toàn tuyệt đối cho tài khoản khách hàng."
                )
            ]
        },
        {
            "id": "quiz",
            "kind": "quiz",
            "title": "Trắc nghiệm Tính toán: Thứ tự Hai pha khi Cấp Thấu chi Cầm cố",
            "checks": [
                "100 - 85 == 15",
                "90 > 85"
            ],
            "steps": [
                build_step(
                    """<p><b>Câu hỏi trắc nghiệm nghiệp vụ tín dụng</b>: Khi cấp hạn mức thấu chi cầm cố sổ tiết kiệm 100 triệu với tỉ lệ cấp vốn 85%, thứ tự điều phối nào sau đây bảo đảm an toàn sổ cái tuyệt đối?</p>
<ul>
  <li><b>A</b>: Mở hạn mức thấu chi 85 triệu trước, sau đó gửi thông báo phong tỏa sổ tiết kiệm sau.</li>
  <li><b>B</b>: Phong tỏa số dư sổ tiết kiệm trên phân hệ tiền gửi Core T24 trước, sau khi thành công mới cấp hạn mức thấu chi vào tài khoản thanh toán CASA.</li>
  <li><b>C</b>: Giải ngân tiền mặt trực tiếp cho khách hàng mà không cần ghi nhận vào ngân hàng lõi.</li>
  <li><b>D</b>: Chờ khách hàng ký giấy tờ tại quầy mới thực hiện thao tác.</li>
</ul>""",
                    "Xin mời bạn lựa chọn quy trình hai pha chuẩn mực khi cấp hạn mức thấu chi cầm cố tài sản. Bạn có 15 giây suy nghĩ trước khi nghe giải thích quy chuẩn ngân hàng số.",
                    pause=15
                ),
                build_step(
                    """<div class="box key"><b>Đáp án chính xác là B</b>!</div>
<p><b>Bước 1 — Nguyên tắc tài sản bảo đảm trong ngân hàng</b>:</p>
<table class="t">
  <tr><th>trình tự</th><th>thao tác Core T24</th><th>ý nghĩa quản trị rủi ro</th></tr>
  <tr><td>Pha 1: Phong tỏa</td><td>Phong tỏa sổ tiết kiệm trên Core T24</td><td>Khách hàng không thể rút tiền gửi khi đang vay</td></tr>
  <tr><td>Pha 2: Cấp vốn</td><td>Ghi hạn mức thấu chi CASA</td><td>Chỉ cấp vốn khi tài sản thế chấp đã an toàn</td></tr>
</table>""",
                    "Đáp án chính xác là phương án B. Sổ tiết kiệm đóng vai trò là tài sản bảo đảm nên bắt buộc phải được phong tỏa an toàn trước. Chỉ khi bước khóa sổ thành công thì hạn mức chi tiêu mới được kích hoạt.",
                    clear=True
                ),
                build_step(
                    """<p><b>Bước 2 — Cơ chế phục hồi khi pha 2 gặp sự cố</b>:</p>
<div class="box key">Nếu bước cấp hạn mức thấu chi bị lỗi mạng, hệ thống tự động phát lệnh mở phong tỏa sổ tiết kiệm để trả lại trạng thái nguyên vẹn cho khách hàng, loại bỏ rủi ro tài sản bị khóa oan!</div>""",
                    "Bước hai, nếu bước cấp hạn mức gặp lỗi, hệ thống sẽ tự động giải tỏa phong tỏa để hoàn trả trạng thái ban đầu cho sổ tiết kiệm. Điều này bảo đảm quyền lợi hợp pháp cho khách hàng và giữ uy tín cho ngân hàng.",
                    clear=True
                )
            ]
        },
        {
            "id": "recap",
            "kind": "recap",
            "title": "Tổng kết chuỗi logic Nghiệp vụ Ngân hàng và Cổng NAPAS",
            "steps": [
                build_step(
                    """<div class="chain">
  <span>Tích hợp Core T24 OFS XML qua IBM MQ bất đồng bộ</span> &rarr;
  <span>Chuyển mạch NAPAS 247 ISO 8583 & Mã hóa khối PIN HSM</span> &rarr;
  <span>Làm chủ 6 Trụ cột Tín dụng Bán lẻ Squad Lending</span> &rarr;
  <span>Đối soát Ba bên EOD Thuật toán Hai con trỏ O(N)</span> &rarr;
  <span>Xử lý Chuẩn xác Mã lỗi Nghi vấn 68 bảo toàn nguồn vốn</span>
</div>
<table class="t" style="margin-top: 15px;">
  <tr><th>giá trị chuyên môn</th><th>đóng góp thực tế tại Khối Công nghệ ACB</th></tr>
  <tr><td>Làm chủ T24 & NAPAS 247</td><td>Vận hành cổng giao dịch hàng chục nghìn TPS ổn định 4 số 9</td></tr>
  <tr><td>Kiến trúc Squad Lending</td><td>Tự động hóa toàn trình phê duyệt và giải ngân tín dụng số sub-1 phút</td></tr>
  <tr><td>Đối soát siêu tốc EOD</td><td>Tiết kiệm 95% thời gian tra soát và triệt tiêu nguy cơ thất thoát vốn</td></tr>
</table>
<p style="margin-top: 15px;"><b>Bản lĩnh Kỹ sư Tích hợp Cấp cao</b>: Nắm vững huyết mạch thanh toán ngân hàng, bảo vệ từng đồng tiền của khách hàng và tự tin chốt mức lương 50 triệu gross.</p>""",
                    "Tóm lại, chuỗi logic gồm tích hợp ngân hàng lõi, chuẩn hóa gói tin chuyển mạch, bao quát sáu trụ cột tín dụng và đối soát hai con trỏ siêu tốc. Làm chủ nghiệp vụ ngân hàng cốt lõi này, bạn tự tin thể hiện bản lĩnh chuyên gia và khẳng định mức đãi ngộ 50 triệu gross tại ACB."
                )
            ]
        }
    ]
}

save_spec(l04, r"D:\research-video\lessons\int\L04_banking_domain_t24_napas.yaml")
print("L04 generated successfully!")
