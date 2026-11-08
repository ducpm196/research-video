import os
import sys

lesson_yaml = """id: L00
course: ACB
series: "Phỏng vấn Kỹ sư Tích hợp ACB"
title: "Bài 0 — Cẩm nang Phỏng vấn Tích hợp Ngân hàng: Từ Mất gốc đến Senior"
voice: vi-VN-NamMinhNeural
rate: "-5%"
depth: full
source: "curriculum/acb.yaml L00; OCB Global System Analytics Hub (hub-system-graph.md); JD Tuyển dụng Kỹ sư Tích hợp ACB 2026; Chuẩn thanh toán quốc tế ISO 8583 MTI 0200/0210; Temenos T24 OFS XML over IBM MQ"
assumes: [arith, approx]
objectives:
  - "Hiểu rõ kiến trúc tích hợp Core Banking Temenos T24 và Cổng thanh toán NAPAS 247"
  - "Làm chủ mô hình điều phối SAGA, chống trừ tiền kép và tối ưu hóa Oracle 19c"
  - "Nắm vững kịch bản phản xạ tình huống thực tế và tự tin deal mức lương 50 triệu gross"

scenes:
  # ──────────────────────── 1. HOOK ────────────────────────
  - id: hook
    kind: hook
    title: "Khoảng cách giữa lập trình viên bình thường và Kỹ sư Tích hợp Ngân hàng"
    steps:
      - show: |
          <p>Nhiều bạn nghĩ làm backend tích hợp chỉ đơn giản là viết vài API REST để lưu dữ liệu. Nhưng khi bước vào ngân hàng lớn như ACB, một lệnh bị nghẽn mạng có thể gây thất thoát hàng tỉ đồng.</p>
          <div class="box key">Hôm nay: <b>Toàn cảnh kiến trúc tích hợp ngân hàng</b> — từ Temenos T24, NAPAS 247, SAGA đến bí quyết chinh phục mức lương <b>50 triệu gross</b>.</div>
        focus: [1, 1, 2]
        say: "Chào bạn, nhiều bạn nghĩ làm lập trình viên tích hợp chỉ đơn giản là viết vài giao diện lập trình để lưu dữ liệu. Nhưng trong ngân hàng, một lệnh nghẽn mạng có thể làm thất thoát hàng tỉ đồng hoặc trừ tiền hai lần. Hôm nay ta cùng phân tích toàn cảnh kiến trúc tích hợp ngân hàng, từ Core T24, Cổng NAPAS, điều phối SAGA, tới mức lương 50 triệu gross."

  # ──────────────────────── 2. PREREQ ────────────────────────
  - id: prereq
    kind: prereq
    title: "Ôn lại: Đơn vị thời gian, bắt tay mạng và tính nhất quán dữ liệu"
    checks:
      - "1000 * 1000 == 1000000 and 1000 // 10 == 100"
      - "10000 // 100 == 100 and 60 * 1000 == 60000"
    steps:
      - show: |
          <table class="t">
            <tr><th>thông số</th><th>giá trị ngân hàng</th><th>ý nghĩa thực tế</th></tr>
            <tr><td>Độ trễ P99</td><td>dưới 100 ms</td><td>99% giao dịch phản hồi dưới 0,1 giây</td></tr>
            <tr><td>Thông lượng</td><td>10 000 TPS</td><td>hệ thống gánh 10 nghìn lệnh mỗi giây</td></tr>
            <tr><td>Thời gian sống khoá</td><td>60 giây</td><td>khoá chống trùng lặp giữ trong một phút</td></tr>
          </table>
        focus: [1, "1.2", "1.3", "1.4", "1.4"]
        say: "Trước tiên ta ôn lại ba chỉ số hiệu năng huyết mạch trong ngân hàng. Một giây bằng một nghìn mi li giây. Độ trễ 99 phần trăm phải dưới 100 mi li giây, nghĩa là hầu hết giao dịch phản hồi rất nhanh. Thông lượng giờ cao điểm đạt 10 nghìn giao dịch mỗi giây. Và khoá khử trùng lặp được giữ trong 60 giây, tức 60 nghìn mi li giây."

  # ──────────────────────── 3. SYMBOL ────────────────────────
  - id: symbol
    kind: symbol
    title: "Giải mã các thuật ngữ và ký hiệu cốt lõi trong ngành ngân hàng"
    steps:
      - show: |
          <table class="t">
            <tr><th>thuật ngữ</th><th>tên đầy đủ</th><th>vai trò kỹ thuật</th></tr>
            <tr><td>T24 OFS</td><td>Open Financial Service</td><td>chuỗi bản tin giao tiếp với Core Banking Temenos T24</td></tr>
            <tr><td>ISO 8583</td><td>Financial Transaction Message</td><td>chuẩn bản tin tài chính liên ngân hàng qua socket TCP</td></tr>
            <tr><td>SAGA</td><td>Distributed Saga Pattern</td><td>chuỗi giao dịch cục bộ kèm giao dịch bồi hoàn tự động</td></tr>
            <tr><td>STAN / RRN</td><td>Trace & Reference Number</td><td>số định danh đối soát giao dịch duy nhất trong ngày</td></tr>
          </table>
        focus: [1, "1.2", "1.3", "1.4", "1.5"]
        say: "Để phỏng vấn tự tin, bạn cần giải mã bốn thuật ngữ nền tảng sau. Bản tin OFS là định dạng giao tiếp chuẩn của Core Banking Temenos T24 qua hàng đợi IBM MQ. Chuẩn ISO 8583 là giao thức bản tin tài chính qua cổng chuyển mạch NAPAS. Mô hình SAGA là chuỗi giao dịch phân tán giúp tự động hoàn tiền khi đối tác sập. Số kiểm toán STAN cùng số tham chiếu RRN là hai mã số dùng để đối soát liên ngân hàng."

  # ──────────────────────── 4. CONCEPT ────────────────────────
  - id: concept
    kind: concept
    title: "Kiến trúc luồng chuyển tiền liên ngân hàng 247 qua cổng NAPAS"
    steps:
      - show: |
          <div>
            <svg width="1500" height="380" viewBox="0 0 1500 380">
              <g font-size="22" fill="#1f2937">
                <text x="750" y="35" text-anchor="middle" font-weight="bold" font-size="26">Kiến trúc Tích hợp Luồng Thanh toán Ngân hàng ACB</text>
                <rect x="40" y="70" width="260" height="240" rx="12" fill="#e0f2fe" stroke="#0284c7" stroke-width="3"/>
                <text x="170" y="115" text-anchor="middle" font-weight="bold">1. Kênh số & Ứng dụng</text>
                <text x="170" y="160" text-anchor="middle">ACB One App</text>
                <text x="170" y="200" text-anchor="middle">API Gateway</text>
                <text x="170" y="240" text-anchor="middle">Xác thực mTLS & FaceID</text>

                <rect x="360" y="70" width="340" height="240" rx="12" fill="#fef3c7" stroke="#d97706" stroke-width="3"/>
                <text x="530" y="115" text-anchor="middle" font-weight="bold">2. Payment Hub & SAGA</text>
                <text x="530" y="160" text-anchor="middle">Khử trùng lặp Redis dedup</text>
                <text x="530" y="200" text-anchor="middle">Máy trạng thái Saga State</text>
                <text x="530" y="240" text-anchor="middle">Hàng đợi sự kiện Kafka</text>

                <rect x="760" y="70" width="320" height="240" rx="12" fill="#dcfce7" stroke="#16a34a" stroke-width="3"/>
                <text x="920" y="115" text-anchor="middle" font-weight="bold">3. Cổng NAPAS & HSM</text>
                <text x="920" y="160" text-anchor="middle">Bản tin ISO 8583 0200/0210</text>
                <text x="920" y="200" text-anchor="middle">Socket TCP nhị phân</text>
                <text x="920" y="240" text-anchor="middle">Mã hoá PIN Block phần cứng</text>

                <rect x="1140" y="70" width="320" height="240" rx="12" fill="#f3e8ff" stroke="#9333ea" stroke-width="3"/>
                <text x="1300" y="115" text-anchor="middle" font-weight="bold">4. Core Banking T24</text>
                <text x="1300" y="160" text-anchor="middle">IBM MQ OFS Queue</text>
                <text x="1300" y="200" text-anchor="middle">Hạch toán ghi nợ ghi có</text>
                <text x="1300" y="240" text-anchor="middle">Oracle 19c PL-SQL</text>

                <line x1="300" y1="190" x2="360" y2="190" stroke="#0284c7" stroke-width="4"/>
                <line x1="700" y1="190" x2="760" y2="190" stroke="#d97706" stroke-width="4"/>
                <line x1="1080" y1="190" x2="1140" y2="190" stroke="#16a34a" stroke-width="4"/>
              </g>
            </svg>
          </div>
        focus: [1, 1, 1, 1, 1]
        say: "Hãy nhìn vào bức tranh toàn cảnh kiến trúc gồm bốn tầng khép kín. Tầng một là kênh số tiếp nhận yêu cầu và xác thực danh tính. Tầng hai là trung tâm thanh toán kiểm tra khử trùng lặp trong Redis và điều phối trạng thái. Tầng ba đóng gói bản tin tài chính ISO 8583 gửi qua socket TCP tới cổng NAPAS. Và tầng bốn giao tiếp với Core Banking Temenos T24 qua hàng đợi IBM MQ. Toàn bộ hạch toán số dư được ghi nhận an toàn trên cơ sở dữ liệu Oracle."

  # ──────────────────────── 5. EXAMPLE ────────────────────────
  - id: example
    kind: example
    title: "Tính toán lưu lượng giao dịch và kiểm soát rủi ro"
    checks:
      - "10000 * 60 == 600000 and 600000 * 60 == 36000000"
      - "120 + 35 == 155 and 1500 - 155 == 1345"
      - "60 * 1000 == 60000"
    steps:
      - show: |
          <p><b>Bước 1 — Tính lưu lượng mỗi phút và mỗi giờ</b>:</p>
          <table class="t">
            <tr><th>đơn vị</th><th>phép tính</th><th>kết quả</th></tr>
            <tr><td>Mỗi phút</td><td>$10\,000 \times 60$</td><td>$600\,000$ giao dịch</td></tr>
            <tr><td>Mỗi giờ</td><td>$600\,000 \times 60$</td><td>$36\,000\,000$ giao dịch</td></tr>
          </table>
        focus: [1, "1.2", "1.3"]
        say: "Bước một, ta tính toán lưu lượng tải thực tế. Ở mức 10 nghìn lệnh mỗi giây, mỗi phút hệ thống xử lý 600 nghìn giao dịch. Trong một giờ cao điểm, tổng số giao dịch đạt tới 36 triệu giao dịch."
      - show: |
          <p><b>Bước 2 — Đo lường thời gian phản hồi toàn trình</b>:</p>
          <table class="t">
            <tr><th>thành phần</th><th>thời gian</th><th>ghi chú</th></tr>
            <tr><td>Mạng NAPAS</td><td>$120$ ms</td><td>vòng khứ hồi qua mạng liên ngân hàng</td></tr>
            <tr><td>Hạch toán Core</td><td>$35$ ms</td><td>ghi nhận giao dịch trên Core T24</td></tr>
            <tr><td>Toàn trình</td><td>$120 + 35 = 155$ ms</td><td>thấp hơn rất nhiều hạn mức 1500 ms</td></tr>
          </table>
        focus: [1, "1.2", "1.3", "1.4"]
        say: "Bước hai, ta đo lường độ trễ toàn trình. Thời gian mạng NAPAS tốn 120 mi li giây. Hạch toán Core T24 tốn 35 mi li giây. Tổng thời gian là 155 mi li giây, thấp hơn rất nhiều hạn mức 1500 mi li giây của ngân hàng."
      - show: |
          <p><b>Bước 3 — Cấu hình khoá khử trùng lặp trong Redis</b>:</p>
          <div class="box key">Thời gian hết hạn khoá: $60 \text{ giây} = 60 \times 1000 = 60\,000 \text{ ms}$. Chặn đứng mọi bản tin gửi lại do lỗi mạng.</div>
        focus: [1, 1]
        say: "Bước ba, ta thiết lập khoá khử trùng lặp trong Redis. Khoá được giữ trong 60 giây, tức 60 nghìn mi li giây. Nhờ đó, mọi bản tin gửi lặp do mạng chập chờn đều bị chặn đứng hoàn toàn."

  # ──────────────────────── 6. CHECK ────────────────────────
  - id: check
    kind: check
    title: "Kiểm tra lại cơ chế bồi hoàn SAGA khi đối tác thứ ba gặp sự cố"
    checks:
      - "1000000 - 500000 == 500000 and 500000 + 500000 == 1000000"
      - "3000 // 1000 == 3"
    steps:
      - show: |
          <p><b>Tình huống</b>: Khách hàng có 1 triệu đồng, thanh toán hoá đơn điện lực 500 nghìn đồng.</p>
          <p>Core Banking đã trích nợ 500 nghìn, số dư còn 500 nghìn. Nhưng cổng điện lực phản hồi hết giờ.</p>
        focus: [1, 2]
        say: "Ta kiểm tra tình huống kinh điển khi đối tác thanh toán bị nghẽn. Giả sử tài khoản có một triệu đồng, ngân hàng trừ 500 nghìn để trả tiền điện, số dư còn 500 nghìn đồng nhưng đối tác báo hết giờ."
      - show: |
          <div class="box key"><b>Quy tắc bồi hoàn SAGA</b>: Vì đối tác chưa phản hồi rõ ràng, hệ thống chuyển sang trạng thái nghi vấn, gọi truy vấn sau 3 giây. Do đối tác xác nhận chưa nhận tiền, ta kích hoạt bồi hoàn cộng lại 500 nghìn: $500\,000 + 500\,000 = 1\,000\,000$ đồng.</div>
        focus: [1, 1]
        say: "Vì đối tác chưa rõ kết quả, hệ thống chuyển sang trạng thái nghi vấn và tra cứu sau 3 giây. Do đối tác xác nhận chưa nhận tiền, ta kích hoạt bồi hoàn để hoàn lại đủ một triệu đồng an toàn."

  # ──────────────────────── 7. PITFALL ────────────────────────
  - id: pitfall
    kind: pitfall
    title: "Ba sai lầm nghiêm trọng khiến ứng viên bị đánh trượt vòng kỹ thuật"
    steps:
      - show: |
          <table class="t">
            <tr><th>sai lầm sơ cấp</th><th>hậu quả kỹ thuật</th><th>giải pháp chuẩn Senior</th></tr>
            <tr><td>Tự gọi hàm nội bộ trong Spring</td><td>mất giao dịch quản lý @Transactional</td><td>tách dịch vụ riêng hoặc tự tiêm phụ thuộc</td></tr>
            <tr><td>Khoá tài khoản ngẫu nhiên</td><td>gây lỗi bế tắc khoá trong Oracle</td><td>khoá theo thứ tự tăng dần của số tài khoản</td></tr>
            <tr><td>Thiếu chỉ mục khoá ngoại</td><td>khoá toàn bộ bảng con khi cập nhật cha</td><td>đánh chỉ mục B-Tree trên mọi cột khoá ngoại</td></tr>
          </table>
        focus: [1, "1.2", "1.3", "1.4"]
        say: "Có ba sai lầm chết người mà người phỏng vấn ACB hay dùng để thử thách ứng viên. Thứ nhất là gọi hàm nội bộ trong cùng một lớp Spring, khiến mất giao dịch khi có sự cố. Thứ hai là cập nhật tài khoản theo thứ tự ngẫu nhiên, dẫn tới bế tắc khoá trong Oracle. Ta giải quyết bằng cách luôn khoá tài khoản nhỏ trước, lớn sau. Và thứ ba là quên đánh chỉ mục trên khoá ngoại, làm Oracle khoá toàn bộ bảng con."

  # ──────────────────────── 8. QUIZ ────────────────────────
  - id: quiz
    kind: quiz
    title: "Tự kiểm tra phản xạ kiến trúc và định vị bản thân"
    checks:
      - "50 - 45 == 5 and 45 + 5 == 50"
      - "12 * 50 == 600 and 600 + 150 == 750"
    steps:
      - show: |
          <table class="t">
            <tr><th>câu hỏi</th><th>nội dung thử thách</th></tr>
            <tr><td>1</td><td>Khi cổng NAPAS phản hồi hết giờ với bản tin 0200, ta nên xử lý thế nào?</td></tr>
            <tr><td>2</td><td>Nếu nhà tuyển dụng ACB nói bạn mới có 3 năm tại OCB nên chỉ nhận 35 đến 40 triệu, bạn phản hồi ra sao?</td></tr>
          </table>
        focus: [1, "1.2", "1.3"]
        say: "Bây giờ đến lượt bạn tự trả lời hai câu hỏi then chốt. Câu một, khi cổng NAPAS phản hồi hết giờ với bản tin 0200, ta nên xử lý thế nào? Câu hai, nếu nhà tuyển dụng nói bạn mới có 3 năm tại OCB nên chỉ nhận 35 đến 40 triệu, bạn phản hồi ra sao? Hãy dừng video để suy nghĩ."
        pause: 15
      - show: |
          <p><b>Đáp án câu 1</b>: Không hoàn tiền ngay vì tiền có thể đã sang người nhận. Chuyển trạng thái nghi vấn, gửi bản tin đảo hủy MTI 0420, nếu không được thì chờ đối soát cuối ngày.</p>
        focus: [1, 1]
        say: "Đáp án câu một, tuyệt đối không hoàn tiền ngay vì có thể tiền đã vào tài khoản người nhận. Ta chuyển trạng thái nghi vấn, gửi bản tin đảo hủy, và nếu không được thì chờ đối soát cuối ngày."
      - show: |
          <p><b>Đáp án câu 2</b>: Khẳng định 3 năm tại OCB giữ vai trò Chuyên viên chính gánh vác Core T24 và NAPAS, từng phụ trách cho vay tại Mirae Asset, có bằng Cử nhân AI tại trường top UIT. Mức <b>50 triệu gross</b> (tổng gói 750 triệu mỗi năm) hoàn toàn tương xứng với giá trị tạo ra ngay.</p>
        focus: [1, 1]
        say: "Đáp án câu hai, hãy chứng minh chiều sâu thực chiến. Bạn là Chuyên viên chính tại OCB trực tiếp kiến trúc cổng Core T24 và NAPAS, từng phụ trách cho vay tại Mirae Asset, và có bằng Cử nhân AI tại trường UIT. Mức lương 50 triệu gross mỗi tháng là 600 triệu một năm, cùng thưởng thành 750 triệu, hoàn toàn tương xứng với giá trị mang lại."

  # ──────────────────────── 9. RECAP ────────────────────────
  - id: recap
    kind: recap
    title: "Tổng kết chuỗi logic và hành trang bước vào phòng phỏng vấn"
    steps:
      - show: |
          <div class="chain">
            <span class="n">Nghiệp vụ Core T24 & NAPAS: Bảo toàn 100% dòng tiền</span><span class="a">→</span>
            <span class="n">Hệ phân tán Kafka & Oracle: Chịu tải 10 000 TPS mượt mà</span><span class="a">→</span>
            <span class="n">Đột phá Trí tuệ Nhân tạo UIT: Phát hiện gian lận & định tuyến</span><span class="a">→</span>
            <span class="n">Chuyên viên chính thực chiến: Bảo vệ trọn vẹn mức lương 50 triệu gross</span>
          </div>
        focus: [1, 1]
        say: "Tổng kết lại, hành trang phỏng vấn ACB được gắn kết theo chuỗi logic sau. Nắm vững Core T24 và NAPAS giúp bạn bảo toàn dòng tiền. Làm chủ Kafka và Oracle đảm bảo hệ thống chịu tải mượt mà. Nền tảng Trí tuệ Nhân tạo từ trường UIT là vũ khí khác biệt vượt trội. Và vị thế Chuyên viên chính thực chiến giúp bạn tự tin đàm phán mức lương 50 triệu gross."
      - show: |
          <div class="box key"><b>Tư duy Senior:</b> Kỹ sư cấp cao không phải là người viết nhiều dòng mã nhất, mà là người hiểu sâu bản chất hệ thống và bảo vệ an toàn tuyệt đối cho tài sản của khách hàng và ngân hàng.</div>
        focus: [1]
        say: "Điều quan trọng nhất cần ghi nhớ, một kỹ sư cấp cao không phải là người viết nhiều dòng mã nhất, mà là người hiểu sâu bản chất hệ thống và bảo vệ an toàn tuyệt đối cho tài sản của khách hàng."
"""

target_path = r"D:\research-video\lessons\acb\L00_phong_van_tich_hop_acb.yaml"
with open(target_path, "w", encoding="utf-8") as f:
    f.write(lesson_yaml)

interview_copy = r"D:\research-video\interview\L00_phong_van_tich_hop_acb.yaml"
with open(interview_copy, "w", encoding="utf-8") as f:
    f.write(lesson_yaml)

print("Updated lesson YAML written successfully.")
