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
# LESSON 3: HỆ THỐNG PHÂN TÁN, SAGA PATTERN & TỐI ƯU HÓA ORACLE 19C
# =========================================================================
l03 = {
    "id": "L03",
    "course": "INT",
    "series": "Giáo trình Phỏng vấn Senior Banking ACB",
    "title": "Chuyên đề 3 — Hệ thống Phân tán, SAGA Pattern và Tối ưu hóa Oracle 19c",
    "voice": "piper:vi_VN-vais1000-medium",
    "rate": "-5%",
    "depth": "full",
    "source": "interview/03_distributed_systems_senior.md; Khung chuẩn UIT DSY, DEN, EVT, DBS; Oracle Database 19c Performance Tuning Guide",
    "assumes": ["arith", "approx"],
    "objectives": [
        "Hiểu rõ hạn chế của giao thức 2PC và làm chủ mô hình SAGA Orchestration trong ngân hàng",
        "Triển khai mẫu Transactional Outbox với CDC Debezium khử triệt để hiểm họa ghi kép",
        "Tối ưu hóa bảng ghi Oracle 19c bằng Partitioning và triệt tiêu bế tắc khóa ORA-00060"
    ],
    "scenes": [
        {
            "id": "hook",
            "kind": "hook",
            "title": "Sự thất bại của giao thức khóa chặn hai pha ở quy mô ngân hàng cao tải",
            "steps": [
                build_step(
                    """<p>Khi tích hợp nhiều hệ thống ngân hàng độc lập, giao thức khóa chặn hai pha truyền thống khiến toàn bộ bảng dữ liệu bị đóng băng nếu một đối tác bị chậm mạng.</p>
<div class="box key">Làm sao một ngân hàng như ACB có thể thanh toán hóa đơn điện nước qua bên thứ ba, tự động bồi hoàn khi có lỗi mà không làm nghẽn kết nối cơ sở dữ liệu?</div>""",
                    "Chào bạn, trong các hệ thống phân tán quy mô lớn, giao thức khóa hai pha truyền thống bộc lộ nhược điểm chí tử khi một đối tác bị chậm mạng. Toàn bộ bảng dữ liệu tài khoản sẽ bị đóng băng khiến ứng dụng cạn kiệt kết nối. Hôm nay, ta cùng nhau giải mã mô hình điều phối giao dịch phân tán và tối ưu hóa cơ sở dữ liệu lõi."
                ),
                build_step(
                    """<table class="t">
  <tr><th>vấn đề phân tán</th><th>nguy cơ hệ thống</th><th>giải pháp chuẩn Kỹ sư Cấp cao</th></tr>
  <tr><td>Giao thức khóa chặn hai pha</td><td>Treo cứng hàng đợi kết nối khi mạng chậm</td><td>Mô hình SAGA điều phối tập trung với máy trạng thái</td></tr>
  <tr><td>Hiểm họa ghi kép dữ liệu</td><td>Mất tính nhất quán giữa cơ sở dữ liệu và Kafka</td><td>Mẫu Transactional Outbox kết hợp bắt biến động dữ liệu CDC</td></tr>
  <tr><td>Bế tắc khóa Oracle ngày chi lương</td><td>Xảy ra lỗi ORA-00060 làm treo cổng hạch toán</td><td>Sắp xếp thứ tự tài khoản trước khi khóa hàng</td></tr>
</table>
<p>Hôm nay, ta làm chủ: <b>Mô hình SAGA Orchestration</b>, <b>mẫu Transactional Outbox</b>, và <b>thuật toán khử bế tắc khóa Oracle 19c</b>.</p>""",
                    "Hôm nay, ta cùng nhau khám phá ba giải pháp then chốt cho hệ thống phân tán. Ta tìm hiểu cách tổ chức chuỗi giao dịch bù trừ để bảo đảm an toàn dòng tiền. Ta nắm vững kỹ thuật truyền biến động dữ liệu qua hộp thư sự kiện. Ta cũng làm chủ thuật toán triệt tiêu bế tắc khóa trong cơ sở dữ liệu.",
                    clear=True
                )
            ]
        },
        {
            "id": "prereq",
            "kind": "prereq",
            "title": "Ôn lại: Định lý CAP, Mô hình ACID và Hiểm họa Ghi kép",
            "checks": [
                "50000 * 60 == 3000000",
                "1000 // 100 == 10"
            ],
            "steps": [
                build_step(
                    """<p><b>Định lý CAP và Sự đánh đổi trong Kiến trúc Ngân hàng</b>:</p>
<table class="t">
  <tr><th>thuộc tính</th><th>định nghĩa</th><th>chiến lược của ngân hàng</th></tr>
  <tr><td>Tính nhất quán (Consistency)</td><td>Mọi nút đều nhìn thấy dữ liệu mới nhất</td><td>Bắt buộc đối với số dư tài khoản tiền gửi</td></tr>
  <tr><td>Tính sẵn sàng (Availability)</td><td>Mọi yêu cầu đều nhận phản hồi không lỗi</td><td>Đạt 99.99% thời gian hoạt động liên tục</td></tr>
  <tr><td>Chịu đựng phân vùng (Partition)</td><td>Hệ thống vẫn chạy khi mạng bị đứt đoạn</td><td>Bắt buộc trong mạng phân tán đám mây</td></tr>
</table>""",
                    "Trước tiên ta ôn lại định lý cơ bản của hệ thống phân tán. Trong môi trường tài chính, ta bắt buộc phải duy trì tính nhất quán tuyệt đối của số dư sổ cái. Ngân hàng không thể chấp nhận việc dữ liệu bị sai lệch khi có sự cố phân vùng mạng."
                ),
                build_step(
                    """<div class="box key">Hiểm họa ghi kép: Nếu dịch vụ vừa ghi cơ sở dữ liệu vừa phát bản tin vào Kafka mà không nằm trong cùng một giao dịch, việc một trong hai bước thất bại sẽ làm hỏng tính toàn vẹn dữ liệu. Ta bắt buộc phải áp dụng mẫu hộp thư sự kiện Transactional Outbox!</div>""",
                    "Hiểm họa ghi kép xảy ra khi dịch vụ vừa ghi cơ sở dữ liệu vừa gửi thông điệp ra ngoài. Nếu bước gửi mạng bị lỗi, dữ liệu giữa hai bên sẽ không khớp nhau. Ta giải quyết triệt để bằng mẫu hộp thư sự kiện dùng chung giao dịch.",
                    clear=True
                )
            ]
        },
        {
            "id": "concept",
            "kind": "concept",
            "title": "Mô hình SAGA Điều phối Tập trung và Mẫu Transactional Outbox",
            "steps": [
                build_step(
                    """<p><b>Luồng Điều phối SAGA Orchestration trong Thanh toán Hóa đơn</b>:</p>
<svg viewBox="0 0 700 220" style="width:100%;max-height:200px;">
  <rect x="250" y="10" width="200" height="60" rx="8" fill="#e8f4fd" stroke="#003366" stroke-width="2"/>
  <text x="270" y="45" font-size="13" font-weight="bold" fill="#003366">SAGA Điều phối Tập trung</text>
  <rect x="30" y="130" width="160" height="60" rx="6" fill="#d4edda" stroke="#28a745"/>
  <text x="40" y="155" font-size="11" font-weight="bold" fill="#155724">Bước 1: Trích nợ CASA</text>
  <text x="40" y="175" font-size="10" fill="#155724">Bồi hoàn: Hoàn tiền ví</text>
  <rect x="270" y="130" width="160" height="60" rx="6" fill="#fff3cd" stroke="#ffc107"/>
  <text x="280" y="155" font-size="11" font-weight="bold" fill="#856404">Bước 2: Gạch nợ đối tác</text>
  <text x="280" y="175" font-size="10" fill="#856404">Đối tác báo lỗi mạng</text>
  <rect x="510" y="130" width="160" height="60" rx="6" fill="#d1ecf1" stroke="#17a2b8"/>
  <text x="520" y="155" font-size="11" font-weight="bold" fill="#0c5460">Bước 3: Gửi thông báo</text>
  <text x="520" y="175" font-size="10" fill="#0c5460">Tin nhắn ứng dụng</text>
  <path d="M 310 70 L 110 130" stroke="#28a745" stroke-width="2"/>
  <path d="M 350 70 L 350 130" stroke="#ffc107" stroke-width="2"/>
  <path d="M 390 70 L 590 130" stroke="#17a2b8" stroke-width="2"/>
</svg>""",
                    "Nhìn vào sơ đồ điều phối tập trung, bộ điều phối quản lý chuỗi các bước cục bộ độc lập. Khi bước gọi đối tác bên ngoài bị lỗi, bộ điều phối sẽ tự động kích hoạt luồng bồi hoàn ngược lại để hoàn trả tiền cho khách hàng một cách an toàn."
                ),
                build_step(
                    """<div class="box key">Kiến trúc Hộp thư sự kiện Transactional Outbox: Dữ liệu nghiệp vụ và sự kiện được ghi chung vào bảng outbox trong cùng một transaction. Sau đó, công cụ CDC đọc trực tiếp từ tệp nhật ký ghi trước của cơ sở dữ liệu để đẩy vào Kafka, bảo đảm không bao giờ thất lạc tin nhắn!</div>""",
                    "Với mẫu hộp thư sự kiện, ứng dụng ghi thông tin nghiệp vụ và bản tin sự kiện vào cùng một giao dịch cơ sở dữ liệu. Công cụ truyền luồng sẽ đọc trực tiếp từ nhật ký hệ điều hành để phát bản tin, bảo đảm dữ liệu luôn được chuyển phát đầy đủ.",
                    clear=True
                )
            ]
        },
        {
            "id": "symbol",
            "kind": "symbol",
            "title": "Quy ước Ký hiệu và Cơ chế Zero-Copy trong Apache Kafka",
            "checks": [
                "600000 // 60 == 10000",
                "60 - 60 == 0"
            ],
            "steps": [
                build_step(
                    r"""<p><b>Cấu hình đảm bảo Không mất tin nhắn trong Apache Kafka</b>:</p>
<div class="box key">
$$\text{Xác nhận toàn bộ bản sao: } \text{acks} = \text{all}$$
$$\text{Số bản sao tối thiểu đồng bộ: } \text{min.insync.replicas} = 2$$
$$\text{Khử trùng lặp phát tin: } \text{enable.idempotence} = \text{true}$$
</div>
<p>Khi bật tính năng phát tin lũy thừa, mỗi nhà sản xuất được cấp một định danh duy nhất kèm số thứ tự tuần tự, giúp máy chủ Kafka tự động loại bỏ các gói tin gửi lặp lại do lỗi mạng!</p>""",
                    "Theo chuẩn vận hành của ngân hàng, ta thiết lập chế độ xác nhận toàn bộ bản sao đồng bộ. Khi kích hoạt tính năng phát tin lũy thừa, máy chủ sẽ tự động nhận biết số thứ tự của bản tin để loại bỏ hoàn toàn các gói tin bị gửi trùng lặp."
                ),
                build_step(
                    r"""<p><b>Cơ chế Zero-Copy truyền dữ liệu siêu tốc ra mạng</b>:</p>
<pre><code>// Lệnh truyền trực tiếp từ bộ nhớ đệm hệ điều hành ra cổng mạng
sendfile(socket_fd, file_fd, offset, count);

// Bỏ qua hoàn toàn việc sao chép qua vùng nhớ ứng dụng JVM
Disk File -> OS Page Cache -> Network Socket Buffer -> Network Card</code></pre>""",
                    "Để đạt thông lượng hàng chục nghìn thông điệp mỗi giây, hệ thống sử dụng lệnh truyền trực tiếp của nhân hệ điều hành. Dữ liệu từ vùng đệm tập tin được đẩy thẳng ra cổng mạng mà không cần sao chép qua bộ nhớ ứng dụng Java.",
                    clear=True
                )
            ]
        },
        {
            "id": "example",
            "kind": "example",
            "title": "Thực hành: Khử Triệt để Bế tắc Khóa Oracle ORA-00060 Ngày Chi lương",
            "checks": [
                "150000000000 // 10000 == 15000000",
                "19 > 11",
                "3 - 1 == 2"
            ],
            "steps": [
                build_step(
                    """<p><b>Dữ liệu bài toán chi lương tập đoàn lớn tại ACB</b>:</p>
<ul>
  <li>Quy mô lô lệnh: $10\,000$ nhân viên nhận tổng số tiền $150$ tỉ đồng.</li>
  <li>Hiện tượng lỗi: Xuất hiện liên tục mã lỗi bế tắc khóa Oracle ORA-00060 vào giờ cao điểm.</li>
  <li>Nguyên nhân: Hai tiến trình chuyển tiền đồng thời khóa tài khoản theo thứ tự đảo ngược nhau.</li>
</ul>""",
                    "Ta xem xét bài toán chi lương cho mười nghìn nhân viên với tổng ngân sách một trăm năm mươi tỉ đồng. Vào giờ cao điểm, cơ sở dữ liệu liên tục báo lỗi bế tắc khóa do hai luồng đồng thời tranh chấp tài nguyên theo thứ tự ngược chiều."
                ),
                build_step(
                    """<p><b>Bước 1: Phân tích tệp nhật ký vết bế tắc khóa (.trc) của Oracle</b>:</p>
<div class="box pit">Tiến trình A giữ khóa tài khoản X và chờ tài khoản Y. Trong khi đó tiến trình B đang giữ khóa tài khoản Y và chờ tài khoản X. Hai tiến trình chờ nhau vô hạn tạo thành chu trình bế tắc khóa!</div>""",
                    "Bước một, khi phân tích tệp vết của cơ sở dữ liệu, ta thấy tiến trình thứ nhất giữ tài khoản này và chờ tài khoản kia. Ngược lại, tiến trình thứ hai lại giữ tài khoản kia và chờ tài khoản này, tạo thành vòng tròn chờ đợi bế tắc.",
                    clear=True
                ),
                build_step(
                    """<p><b>Bước 2: Áp dụng Thuật toán Khóa hàng có Thứ tự Xác định</b>:</p>
<pre><code>-- Sắp xếp danh sách tài khoản tăng dần trước khi thực hiện lệnh khóa
SELECT account_no, balance 
FROM accounts 
WHERE account_no IN (acc_from, acc_to)
ORDER BY account_no ASC 
FOR UPDATE;</code></pre>
<div class="box key">Nguyên lý toán học: Khi mọi tiến trình đều bắt buộc phải khóa tài khoản nhỏ trước, lớn sau, đồ thị quan hệ tài nguyên luôn là một đồ thị có hướng không có chu trình. Bế tắc khóa bị triệt tiêu 100%!</div>""",
                    "Bước hai, ta áp dụng thuật toán sắp xếp thứ tự tài khoản tăng dần trước khi phát lệnh khóa. Do mọi tiến trình đều tuân theo cùng một trật tự duy nhất, đồ thị phụ thuộc tài nguyên sẽ không bao giờ xuất hiện chu trình bế tắc.",
                    clear=True
                ),
                build_step(
                    """<p><b>Bước 3: Tối ưu hóa xử lý theo lô với Bulk Collect và Forall</b>:</p>
<pre><code>-- Gom mười nghìn bản ghi vào mảng bộ nhớ để cập nhật đồng loạt
OPEN cur_payroll;
FETCH cur_payroll BULK COLLECT INTO l_accounts LIMIT 1000;
FORALL i IN 1..l_accounts.COUNT
    UPDATE accounts SET balance = balance + l_accounts(i).amount
    WHERE account_no = l_accounts(i).acc_no;</code></pre>""",
                    "Bước ba, kỹ sư kết hợp gom cụm dữ liệu và thực thi đồng loạt trong ngôn ngữ thủ tục của cơ sở dữ liệu. Kỹ thuật này giúp giảm hàng nghìn lần chi phí chuyển đổi ngữ cảnh và hoàn tất toàn bộ đợt chi lương chỉ trong ba phút.",
                    clear=True
                )
            ]
        },
        {
            "id": "check",
            "kind": "check",
            "title": "Tự Kiểm tra: So sánh Mô hình SAGA Tự phối hợp và Điều phối",
            "checks": [
                "100 > 10",
                "60 * 1000 == 60000"
            ],
            "steps": [
                build_step(
                    """<p><b>Tình huống phỏng vấn Senior</b>: Trong luồng thanh toán hóa đơn gồm 8 dịch vụ tham gia, tại sao ngân hàng nên chọn mô hình SAGA Điều phối tập trung thay vì mô hình Tự phối hợp qua sự kiện?</p>
<ul>
  <li>(A) Mô hình điều phối tập trung dễ triển khai hơn và không cần cơ sở dữ liệu.</li>
  <li>(B) Mô hình tự phối hợp dễ rơi vào bẫy vòng lặp sự kiện và rất khó truy vết khi có lỗi, trong khi điều phối tập trung quản lý máy trạng thái rõ ràng và kiểm soát bù trừ chuẩn xác.</li>
  <li>(C) Mô hình tự phối hợp có độ bảo mật cao hơn.</li>
</ul>""",
                    "Mời bạn trả lời câu hỏi lựa chọn kiến trúc giao dịch phân tán. Với quy trình phức tạp gồm tám bước tham gia, vì sao mô hình điều phối tập trung lại là lựa chọn ưu tiên hàng đầu của các ngân hàng thương mại."
                ),
                build_step(
                    """<p><b>Đáp án chính xác: Lựa chọn (B)</b></p>
<div class="box key">Giải thích vì: Khi số lượng dịch vụ lớn hơn bốn, mô hình tự phối hợp khiến đồ thị sự kiện trở nên hỗn loạn và rất khó kiểm soát trạng thái bồi hoàn. Do đó mô hình điều phối tập trung giúp lưu vết máy trạng thái vào cơ sở dữ liệu và kích hoạt bồi hoàn hai pha an toàn tuyệt đối!</div>""",
                    "Đáp án chính xác là lựa chọn B vì khi quy trình có nhiều bước, việc để các dịch vụ tự lắng nghe nhau sẽ gây hỗn loạn đồ thị sự kiện. Do đó máy điều phối tập trung giúp lưu vết trạng thái và kích hoạt bù trừ chuẩn xác.",
                    clear=True
                )
            ]
        },
        {
            "id": "pitfall",
            "kind": "pitfall",
            "title": "Bẫy Nguy hiểm: Thiếu Phân vùng Bảng và Quên Đánh Chỉ mục Khóa ngoại",
            "steps": [
                build_step(
                    """<div class="box pit">Hai sai lầm kinh điển làm sập cơ sở dữ liệu Oracle vào giờ cao điểm:</div>
<table class="t" style="margin-top: 10px;">
  <tr><th>sai lầm sơ cấp</th><th>hậu quả vận hành</th><th>giải pháp chuẩn Senior</th></tr>
  <tr><td>Bảng giao dịch không phân vùng</td><td>Quét toàn bảng hàng chục triệu dòng làm đơ I/O</td><td>Phân vùng theo khoảng ngày kết hợp lược tỉa phân vùng</td></tr>
  <tr><td>Thiếu chỉ mục trên cột khóa ngoại</td><td>Khóa toàn bộ bảng con khi cập nhật bảng cha</td><td>Luôn tạo chỉ mục trực tiếp trên mọi cột khóa ngoại</td></tr>
</table>""",
                    "Hai sai lầm phổ biến là để bảng giao dịch phình to mà không phân vùng theo thời gian, và quên đánh chỉ mục trên cột khóa ngoại. Khi cập nhật bảng chính, hệ thống sẽ khóa toàn bộ bảng phụ khiến mọi kết nối đều bị treo cứng."
                )
            ]
        },
        {
            "id": "quiz",
            "kind": "quiz",
            "title": "Trắc nghiệm Tính toán: Điều tra Nguyên nhân Bế tắc Khóa Oracle",
            "checks": [
                "100 - 90 == 10",
                "19 * 10 == 190"
            ],
            "steps": [
                build_step(
                    """<p><b>Câu hỏi trắc nghiệm thực chiến</b>: Khi nhật ký ứng dụng báo lỗi ORA-00060, công cụ nào sau đây cho phép Kỹ sư Cấp cao xác định chính xác câu lệnh và dòng dữ liệu gây ra tranh chấp?</p>
<ul>
  <li><b>A</b>: Khởi động lại máy chủ cơ sở dữ liệu để xóa phiên treo.</li>
  <li><b>B</b>: Mở tệp vết nhật ký trace file có đuôi chấm trc trong thư mục cảnh báo của Oracle để đọc biểu đồ chu trình bế tắc khóa.</li>
  <li><b>C</b>: Xóa bỏ toàn bộ các chỉ mục trên bảng giao dịch.</li>
  <li><b>D</b>: Chuyển toàn bộ cơ sở dữ liệu sang bảng nhớ tạm.</li>
</ul>""",
                    "Xin mời bạn chọn phương án xử lý sự cố chuẩn mực khi hệ thống gặp lỗi bế tắc khóa. Bạn có 15 giây suy nghĩ trước khi nghe phân tích quy trình điều tra của chuyên gia cơ sở dữ liệu.",
                    pause=15
                ),
                build_step(
                    """<div class="box key"><b>Đáp án chính xác là B</b>!</div>
<p><b>Bước 1 — Quy trình điều tra sự cố chuyên nghiệp</b>:</p>
<table class="t">
  <tr><th>bước thực hiện</th><th>công cụ sử dụng</th><th>kết quả trích xuất</th></tr>
  <tr><td>1. Định vị tệp vết</td><td>Thư mục nhật ký trace directory</td><td>Tệp vết chứa định danh phiên làm việc và mã lỗi</td></tr>
  <tr><td>2. Đọc đồ thị chu trình</td><td>Biểu đồ Deadlock Graph</td><td>Xác định chính xác hai câu lệnh SQL và địa chỉ dòng bị khóa</td></tr>
</table>""",
                    "Đáp án chính xác là phương án B. Khi xảy ra bế tắc khóa, hệ quản trị tự động sinh một tệp vết ghi lại toàn bộ biểu đồ tranh chấp. Kỹ sư cấp cao sẽ đọc tệp này để tìm chính xác hai câu lệnh xung đột.",
                    clear=True
                ),
                build_step(
                    """<p><b>Bước 2 — Hành động khắc phục triệt để</b>:</p>
<div class="box key">Sau khi xác định hai câu lệnh gây xung đột, kỹ sư áp dụng ngay thuật toán sắp xếp thứ tự tài khoản trước khi khóa hàng và bổ sung chỉ mục khóa ngoại để triệt tiêu hoàn toàn sự cố tái diễn!</div>""",
                    "Bước hai, sau khi đã làm rõ nguyên nhân gốc rễ, kỹ sư tiến hành chuẩn hóa trật tự khóa tài nguyên và bổ sung chỉ mục cần thiết. Giải pháp này giúp triệt tiêu hoàn toàn sự cố tái diễn trên môi trường thực tế.",
                    clear=True
                )
            ]
        },
        {
            "id": "recap",
            "kind": "recap",
            "title": "Tổng kết chuỗi logic Hệ thống Phân tán và Oracle 19c",
            "steps": [
                build_step(
                    """<div class="chain">
  <span>Mô hình SAGA Orchestration quản lý giao dịch bồi hoàn</span> &rarr;
  <span>Mẫu Transactional Outbox loại bỏ hiểm họa ghi kép</span> &rarr;
  <span>Apache Kafka Zero-Copy truyền tin không mất mát</span> &rarr;
  <span>Thuật toán Khóa hàng theo thứ tự triệt tiêu ORA-00060</span> &rarr;
  <span>Phân vùng Bảng và Đánh chỉ mục Khóa ngoại tối ưu I/O</span>
</div>
<table class="t" style="margin-top: 15px;">
  <tr><th>năng lực phân tán</th><th>giá trị bảo vệ tài sản số ngân hàng ACB</th></tr>
  <tr><td>SAGA & Outbox CDC</td><td>Giao dịch đa hệ thống luôn nhất quán, tự động hoàn tiền khi đối tác lỗi</td></tr>
  <tr><td>Kafka Idempotent</td><td>Truyền tải hàng chục nghìn thông điệp mỗi giây với độ tin cậy tuyệt đối</td></tr>
  <tr><td>Tối ưu Oracle 19c</td><td>Xử lý các lô chi lương trăm tỉ trong 3 phút mà không nghẽn khóa sổ cái</td></tr>
</table>
<p style="margin-top: 15px;"><b>Khẳng định đẳng cấp Senior tại ACB</b>: Làm chủ kiến trúc hệ thống phân tán, tối ưu hóa cơ sở dữ liệu huyết mạch và xứng đáng mức lương 50 triệu gross.</p>""",
                    "Tóm lại, chuỗi logic gồm điều phối giao dịch bù trừ, truyền sự kiện qua hộp thư an toàn, phát tin không mất mát và sắp xếp thứ tự khóa cơ sở dữ liệu. Nắm vững những vũ khí phân tán này, bạn tự tin làm chủ hạ tầng thanh toán cốt lõi và khẳng định mức đãi ngộ 50 triệu gross tại ACB."
                )
            ]
        }
    ]
}

save_spec(l03, r"D:\research-video\lessons\int\L03_distributed_systems_senior.yaml")
print("L03 generated successfully!")
