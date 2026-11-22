"""Close all Stage 11 v3 verifier MUSTs + clean SHOULDs across RBM, ESY, ROB, GFX, BCH."""
from pathlib import Path
import re
import yaml


def replace_exact(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    if new in text:
        return
    assert old in text, f"Missing target in {path}:\n{old[:160]!r}"
    assert text.count(old) == 1, f"Multiple hits in {path}:\n{old[:160]!r}"
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


# ---------------------------------------------------------------------------
# 1. RBM
# ---------------------------------------------------------------------------
# L00: match say to show (1° / 1,7 cm)
replace_exact(
    Path("lessons/rbm/L00_phep_quay_2d.yaml"),
    "Hai mức quy mô: robot 1 mét lệch góc nhỏ chỉ sai vài mi-li-mét",
    "Hai mức quy mô: robot 1 mét lệch góc 1 độ sai khoảng 1 phẩy 7 xen-ti-mét",
)

# L10: covers obj1 -> ponly, addi, addd
replace_exact(
    Path("lessons/rbm/L10_dieu_khien_pid.yaml"),
    "covers:\n- objective: 1\n  scene: addi\n",
    "covers:\n- objective: 1\n  scene: ponly\n- objective: 1\n  scene: addi\n- objective: 1\n  scene: addd\n",
)

# L13: match say to show ("hơn 15 biến")
replace_exact(
    Path("lessons/rbm/L13_kalman_nhieu_chieu.yaml"),
    "nhưng trên xe 15 biến phải giữ ma trận luôn đối xứng dương.",
    "nhưng trên xe thật với hơn 15 biến phải giữ ma trận luôn đối xứng dương.",
)

# L17: add selection rule note in stage4#2 so stage4 (kind: example) directly teaches obj3 + E51 PASS,
# and update covers obj2 -> [stage1, stage2, check, stage4], obj3 -> stage4
replace_exact(
    Path("lessons/rbm/L17_hanh_trinh_kalman_apollo.yaml"),
    """      <div class="box key">Kết luận năm 1985 của hai tác giả: người có kinh nghiệm đang <b>bỏ cách vá tình thế</b> để chọn thuật toán có điều kiện số tốt hơn. Trên máy lớn, số độ chính xác kép có thể chữa lỗi số, nhưng <b>mô hình sai</b> thì vẫn còn.</div>
    focus:
    - 1
    - '1.2'
    - '1.3'
    - '1.4'
    - 2
    - 2
    say: Năm 1983, một số chuyên đề của tạp chí điều khiển tự động gom các ứng dụng thật khác nhau. Có quỹ đạo tàu vũ trụ, theo dõi bằng ra-đa, dẫn đường và chuyển động tàu thuỷ. Có dự đoán đàn gia súc ở Pháp, và đo phóng xạ khi thăm dò giếng dầu khí. Có cả dây chuyền công nghiệp, dò lỗi thiết bị đo nhà máy hạt nhân, và điều khiển nhà máy điện. Năm 1985, hai tác giả kết luận người có kinh nghiệm đang bỏ cách vá tình thế, để chọn thuật toán có điều kiện số tốt hơn. Trên máy lớn, số độ chính xác kép có thể chữa lỗi số, nhưng mô hình sai thì vẫn còn đó.""",
    """      <div class="box key">Kết luận năm 1985 của hai tác giả: người có kinh nghiệm đang <b>bỏ cách vá tình thế</b> để chọn thuật toán có điều kiện số tốt hơn. Trên máy lớn, số độ chính xác kép có thể chữa lỗi số, nhưng <b>mô hình sai</b> thì vẫn còn.</div>
      <p class="note"><b>Chọn công thức cho robot của mình:</b> dùng dạng chuẩn khi điều kiện số nhỏ; đổi sang công thức căn bậc hai hoặc phân tích U-D khi tỷ số thang đo lớn như đo 0,002 m trên quãng 20 m ($10^8 > 2^{24}$), và luôn cộng nhiễu quá trình $Q$ vừa đủ.</p>
    focus:
    - 1
    - '1.2'
    - '1.3'
    - '1.4'
    - 2
    - 2
    - 3
    say: Năm 1983, một số chuyên đề của tạp chí điều khiển tự động gom các ứng dụng thật khác nhau. Có quỹ đạo tàu vũ trụ, theo dõi bằng ra-đa, dẫn đường và chuyển động tàu thuỷ. Có dự đoán đàn gia súc ở Pháp, và đo phóng xạ khi thăm dò giếng dầu khí. Có cả dây chuyền công nghiệp, dò lỗi thiết bị đo nhà máy hạt nhân, và điều khiển nhà máy điện. Năm 1985, hai tác giả kết luận người có kinh nghiệm đang bỏ cách vá tình thế, để chọn thuật toán có điều kiện số tốt hơn. Trên máy lớn, số độ chính xác kép có thể chữa lỗi số, nhưng mô hình sai thì vẫn còn đó. Vì vậy khi cài bộ lọc, hãy giữ công thức căn bậc hai hoặc U D ngay khi tỷ số thang đo lớn hơn độ phân giải dấu phẩy động, như đo 0 phẩy 002 mét trên quãng 20 mét.""",
)
replace_exact(
    Path("lessons/rbm/L17_hanh_trinh_kalman_apollo.yaml"),
    """- objective: 2
  scene: stage2
- objective: 2
  scene: check
- objective: 3
  scene: practice""",
    """- objective: 2
  scene: stage1
- objective: 2
  scene: stage2
- objective: 2
  scene: check
- objective: 2
  scene: stage4
- objective: 3
  scene: stage4""",
)

# ---------------------------------------------------------------------------
# 2. GFX
# ---------------------------------------------------------------------------
replace_exact(
    Path("lessons/gfx/L06_chieu_sang.yaml"),
    "- dotprod\n",
    "",
)
# Replace any remaining mipmap on show: (say already cleaned earlier)
l06_p = Path("lessons/gfx/L06_chieu_sang.yaml")
l06_txt = l06_p.read_text(encoding="utf-8")
l06_txt = l06_txt.replace("bộ ảnh mipmap", "tầng ảnh thu nhỏ").replace(", mipmap,", ", tầng ảnh thu nhỏ,").replace(" mipmap ", " tầng ảnh thu nhỏ ")
l06_p.write_text(l06_txt, encoding="utf-8")

# L09 SVG overlap fix
replace_exact(
    Path("lessons/gfx/L09_do_tia.yaml"),
    '<text x="175" y="215" fill="#2a78d6">Tia hướng d = (0,0,1)</text>',
    '<text x="355" y="226" text-anchor="middle" fill="#2a78d6">Tia hướng d = (0,0,1)</text>',
)
replace_exact(
    Path("lessons/gfx/L09_do_tia.yaml"),
    '<text x="545" y="215" text-anchor="middle" fill="#059669">Pháp tuyến n</text>',
    '<text x="530" y="218" text-anchor="end" fill="#059669">Pháp tuyến n</text>',
)

# L13 remove dotprod, add real-time 60fps vs offline rule to stage4, covers obj3 -> stage4
replace_exact(
    Path("lessons/gfx/L13_hanh_trinh_chieu_sang.yaml"),
    "- dotprod\n",
    "",
)
replace_exact(
    Path("lessons/gfx/L13_hanh_trinh_chieu_sang.yaml"),
    """      <p class="note">Phép bình phương giúp mắt người cảm nhận độ bóng thay đổi tuyến tính và êm ái hơn khi điều chỉnh.</p>
    focus:
    - 1
    - 2
    - 3
    - 4
    say: Năm 2012 và 2013, một xưởng phim hoạt hình rồi một công cụ làm trò chơi lớn đã chuẩn hoá bộ tham số vật liệu dựa trên vật lý. Ba thông số chính là màu gốc, độ kim loại và độ nhám cảm nhận, trong đó màu gốc là màu khuếch tán với phi kim và là màu phản xạ gương với kim loại. Việc lấy bình phương độ nhám giúp giá trị 0 phẩy 5 đổi thành 0 phẩy 25, tạo cảm giác chuyển đổi mượt mà. Nhờ đó, vật liệu trông nhất quán hơn khi đổi điều kiện chiếu sáng.""",
    """      <p class="note">Phép bình phương giúp mắt người cảm nhận độ bóng thay đổi tuyến tính và êm ái hơn khi điều chỉnh.</p>
      <p class="note"><b>Chọn mô hình cho dự án:</b> ngân sách thời gian thực 60 khung hình/giây ($16{,}67$ ms) chỉ dùng được mô hình cục bộ hay chuẩn vật lý gọn kèm khử nhiễu ít tia; dựng phim ngoại tuyến nhiều phút mỗi khung mới dò đường đi đầy đủ nhiều lần nảy.</p>
    focus:
    - 1
    - 2
    - 3
    - 4
    - 5
    say: Năm 2012 và 2013, một xưởng phim hoạt hình rồi một công cụ làm trò chơi lớn đã chuẩn hoá bộ tham số vật liệu dựa trên vật lý. Ba thông số chính là màu gốc, độ kim loại và độ nhám cảm nhận, trong đó màu gốc là màu khuếch tán với phi kim và là màu phản xạ gương với kim loại. Việc lấy bình phương độ nhám giúp giá trị 0 phẩy 5 đổi thành 0 phẩy 25, tạo cảm giác chuyển đổi mượt mà. Nhờ đó, vật liệu trông nhất quán hơn khi đổi điều kiện chiếu sáng. Khi chọn mô hình cho dự án, trò chơi 60 khung hình mỗi giây chỉ có 16 phẩy 67 mi-li-giây nên dùng vật liệu vật lý gọn kèm khử nhiễu, chỉ dò đường đi nhiều lần nảy khi dựng phim ngoại tuyến.""",
)
replace_exact(
    Path("lessons/gfx/L13_hanh_trinh_chieu_sang.yaml"),
    """- objective: 3
  scene: practice""",
    """- objective: 3
  scene: stage4""",
)

# ---------------------------------------------------------------------------
# 3. ROB
# ---------------------------------------------------------------------------
# L03: add 2-scale pitfalls comparison step
replace_exact(
    Path("lessons/rob/L03_mo_hinh_cam_bien.yaml"),
    """      <div class="box warn"><b>Lỗi 3.</b> Đọc mật độ như xác suất <b class="red">(“2,42 &gt; 1?”)</b>
      <br><span class="note">Mật độ có thể lớn hơn 1. Xác suất là <b>diện tích</b> dưới mật độ trên một khoảng; để so hai giả thuyết thì chỉ cần so mật độ với nhau.</span></div>
    say: Lỗi thứ ba, đọc mật độ như xác suất, rồi thắc mắc vì sao 2 phẩy 42 lại lớn hơn 1. Mật độ có thể lớn hơn 1. Xác suất là diện tích dưới mật độ trên một khoảng, còn để so hai giả thuyết thì chỉ cần so mật độ với nhau.""",
    """      <div class="box warn"><b>Lỗi 3.</b> Đọc mật độ như xác suất <b class="red">(“2,42 &gt; 1?”)</b>
      <br><span class="note">Mật độ có thể lớn hơn 1. Xác suất là <b>diện tích</b> dưới mật độ trên một khoảng; để so hai giả thuyết thì chỉ cần so mật độ với nhau.</span></div>
    say: Lỗi thứ ba, đọc mật độ như xác suất, rồi thắc mắc vì sao 2 phẩy 42 lại lớn hơn 1. Mật độ có thể lớn hơn 1. Xác suất là diện tích dưới mật độ trên một khoảng, còn để so hai giả thuyết thì chỉ cần so mật độ với nhau.
  - show: |
      <table class="t"><tr><th>quy mô quét LiDAR</th><th>số tia độc lập thật</th><th>đánh đổi tin cậy</th></tr><tr><td>1 tia đơn lẻ</td><td>1 phép đo cộng nhiễu $z_{\\text{hỏng}}$</td><td>chậm thu hẹp vị trí nhưng không quá tự tin</td></tr><tr><td>Quét 360 tia sát nhau</td><td>trùng vật cản động → nhân 360 lần bị vọt</td><td>cần giảm tỉ trọng (lấy căn bậc $k$ hoặc hạ số tia)</td></tr></table>
    say: Ở quy mô một tia đơn lẻ, thành phần đo hỏng giữ cho niềm tin không loại nhầm giả thuyết đúng khi vướng người đi qua. Nhưng khi quét dày hàng trăm tia sát nhau, giả định các tia hoàn toàn độc lập làm bằng chứng bị nhân lên quá mức. Ta phải hạ trọng số mỗi tia hoặc lọc bớt tia kề nhau để bộ lọc không quá tự tin.""",
)

# L04: add ESS check row + check expression + covers obj3 -> check
replace_exact(
    Path("lessons/rob/L04_dinh_vi_loc_bayes.yaml"),
    """  checks:
  - abs(0.8 * 0.8 - 0.64) < 1e-9 and abs(0.8 * 0.1 - 0.08) < 1e-9 and abs(0.1 * 0.8 - 0.08) < 1e-9 and abs(0.1 * 0.1 - 0.01) < 1e-9 and abs(2 * 0.64 + 2 * 0.08 + 6 * 0.01 - 1.5) < 1e-9
  - round(0.64 / 1.5, 3) == 0.427 and round(0.08 / 1.5, 3) == 0.053 and round(0.01 / 1.5, 3) == 0.007""",
    """  checks:
  - abs(0.8 * 0.8 - 0.64) < 1e-9 and abs(0.8 * 0.1 - 0.08) < 1e-9 and abs(0.1 * 0.8 - 0.08) < 1e-9 and abs(0.1 * 0.1 - 0.01) < 1e-9 and abs(2 * 0.64 + 2 * 0.08 + 6 * 0.01 - 1.5) < 1e-9
  - round(0.64 / 1.5, 3) == 0.427 and round(0.08 / 1.5, 3) == 0.053 and round(0.01 / 1.5, 3) == 0.007
  - round(1.0 / (0.96 ** 2 + 4 * (0.01 ** 2)), 3) == 1.085 and 1.085 < 2.5""",
)
replace_exact(
    Path("lessons/rob/L04_dinh_vi_loc_bayes.yaml"),
    """      <tr><td>6 ô khác: tường rồi tường</td><td>$0{,}1 \\cdot 0{,}1 = 0{,}01$</td><td>$\\approx 0{,}007$ ✓</td></tr></table>
    focus:
    - 1
    - 1
    - '1.2'
    - '1.3'
    - '1.5'
    say: Kiểm bằng đường khác, không chuẩn hoá từng lần mà đếm thẳng theo từng đường đi, vì mọi ô bắt đầu bằng nhau. Mỗi ô hiện tại ứng với một ô xuất phát cách nó 3 ô, ta nhân khả năng của hai lần đo dọc đường đó. Ô 4 và ô 7 đi từ cửa tới cửa, được 0 phẩy 8 nhân 0 phẩy 8 bằng 0 phẩy 64, chia tổng 1 phẩy 5 ra 0 phẩy 427. Ô 0 đi từ cửa tới tường, ô 1 đi từ tường tới cửa, cùng được 0 phẩy 08, chia ra 0 phẩy 053. Sáu ô khác được 0 phẩy 01, chia ra 0 phẩy 007, khớp hết với kết quả chuẩn hoá từng bước.""",
    """      <tr><td>6 ô khác: tường rồi tường</td><td>$0{,}1 \\cdot 0{,}1 = 0{,}01$</td><td>$\\approx 0{,}007$ ✓</td></tr></table>
      <p class="note"><b>Kiểm lấy mẫu lại (kích thước mẫu hiệu dụng ESS):</b> với 5 hạt có trọng số $(0{,}96; 0{,}01 \\times 4)$, tính $\\text{ESS} = \\frac{1}{0{,}96^2 + 4 \\cdot 0{,}01^2} \\approx 1{,}085 \\lt 2{,}5$ → dưới một nửa số hạt nên phải <b>lấy mẫu lại</b>.</p>
    focus:
    - 1
    - 1
    - '1.2'
    - '1.3'
    - '1.5'
    - 2
    say: Kiểm bằng đường khác, không chuẩn hoá từng lần mà đếm thẳng theo từng đường đi, vì mọi ô bắt đầu bằng nhau. Mỗi ô hiện tại ứng với một ô xuất phát cách nó 3 ô, ta nhân khả năng của hai lần đo dọc đường đó. Ô 4 và ô 7 đi từ cửa tới cửa, được 0 phẩy 8 nhân 0 phẩy 8 bằng 0 phẩy 64, chia tổng 1 phẩy 5 ra 0 phẩy 427. Ô 0 đi từ cửa tới tường, ô 1 đi từ tường tới cửa, cùng được 0 phẩy 08, chia ra 0 phẩy 053. Sáu ô khác được 0 phẩy 01, chia ra 0 phẩy 007, khớp hết với kết quả chuẩn hoá từng bước. Ngoài ra, với 5 hạt bị dồn trọng số thành 0 phẩy 96 và bốn hạt 0 phẩy 01, kích thước mẫu hiệu dụng chỉ còn khoảng 1 phẩy 085, dưới một nửa số hạt nên cần lấy mẫu lại.""",
)
replace_exact(
    Path("lessons/rob/L04_dinh_vi_loc_bayes.yaml"),
    """- objective: 3
  scene: practice""",
    """- objective: 3
  scene: check""",
)

# ---------------------------------------------------------------------------
# 4. ESY
# ---------------------------------------------------------------------------
# L02 isr#0: compare interrupt vs polling + explain cli()/sei()/() explicitly
replace_exact(
    Path("lessons/esy/L02_ngat_chong_doi.yaml"),
    """      <p class="note">Vì sao? Chip 8 bit đọc số 16 bit làm hai lần. Đếm đang 255 (<code>0x00FF</code>): đọc byte thấp FF, ngắt chen vào tăng lên 256 (<code>0x0100</code>), đọc byte cao 01 → được <code>0x01FF</code> = $\\hl{511}$, không phải 255 hay 256.</p>
    focus:
    - '1.1'
    - '1.1'
    - '1.1'
    - '1.1'
    - '1.2'
    - 2
    - 3
    - 3
    - 3
    - 3
    say: Trên bảng mã C, từ khoá đầu bắt đọc mới từ bộ nhớ mỗi lần. Từ khoá kế khai báo số nguyên không âm 16 bit, còn hai lệnh cuối tắt rồi bật lại ngắt. Hàm xử lý ngắt có ba quy tắc. Một, phải ngắn, chỉ ghi nhận sự kiện như tăng biến đếm hay đặt cờ, việc nặng để vòng lặp chính làm. Hai, biến dùng chung với ngắt phải khai báo đặc biệt, để trình biên dịch đọc lại từ bộ nhớ mỗi lần mà không giữ một bản cũ trong thanh ghi. Ba, đọc một biến nhiều byte thì tạm tắt ngắt, như đoạn mã này. Vì sao cần tắt ngắt? Chip 8 bit đọc số 16 bit làm hai lần. Giả sử biến đếm đang là 255, ta đọc byte thấp được F F. Đúng lúc đó ngắt chen vào tăng lên 256, rồi ta đọc byte cao được 01, ghép lại thành 511, không phải 255 cũng không phải 256.""",
    """      <p class="note">Vì sao? Chip 8 bit đọc số 16 bit làm hai lần. Đếm đang 255 (<code>0x00FF</code>): đọc byte thấp FF, ngắt chen vào tăng lên 256 (<code>0x0100</code>), đọc byte cao 01 → được <code>0x01FF</code> = $\\hl{511}$, không phải 255 hay 256. Nhờ phần cứng báo ngay, ngắt chỉ trễ vài phần triệu giây so với vòng thăm dò có thể trễ tới cả chu kỳ 10 ms; cặp ngoặc <code>()</code> là lệnh gọi hàm tắt ngắt <code>cli</code> và bật lại ngắt <code>sei</code>.</p>
    focus:
    - '1.1'
    - '1.1'
    - '1.1'
    - '1.1'
    - '1.2'
    - 2
    - 3
    - 3
    - 3
    - 3
    - 3
    say: Trên bảng mã C, từ khoá đầu bắt đọc mới từ bộ nhớ mỗi lần. Từ khoá kế khai báo số nguyên không âm 16 bit, còn cặp ngoặc tròn trên hai lệnh tắt và bật lại ngắt là lời gọi hàm không tham số. Hàm xử lý ngắt có ba quy tắc. Một, phải ngắn, chỉ ghi nhận sự kiện như tăng biến đếm hay đặt cờ, việc nặng để vòng lặp chính làm. Hai, biến dùng chung với ngắt phải khai báo đặc biệt, để trình biên dịch đọc lại từ bộ nhớ mỗi lần mà không giữ một bản cũ trong thanh ghi. Ba, đọc một biến nhiều byte thì tạm tắt ngắt, như đoạn mã này. Vì sao cần tắt ngắt? Chip 8 bit đọc số 16 bit làm hai lần. Giả sử biến đếm đang là 255, ta đọc byte thấp được F F. Đúng lúc đó ngắt chen vào tăng lên 256, rồi ta đọc byte cao được 01, ghép lại thành 511, không phải 255 cũng không phải 256. So với vòng thăm dò phải đợi tới hết một vòng lặp 10 mi-li-giây, ngắt được phần cứng đánh thức trong vài phần triệu giây nên kịp giữ mọi xung ngắn.""",
)

# L03 sym + pwm: add (PWM) & clk gloss, compute timer freq explicitly inside pwm#0
replace_exact(
    Path("lessons/esy/L03_dinh_thoi_pwm.yaml"),
    """      <p>Bộ định thời là một <b>bộ đếm</b> tăng 1 sau mỗi $N$ nhịp xung nhịp ($N$: hệ số chia trước). Đếm tới <b>TOP</b> thì quay về 0: mỗi chu kỳ có $\\text{TOP} + 1$ lần đếm.</p>
      <p>$f = \\dfrac{f_{\\text{clk}}}{N \\cdot (\\text{TOP} + 1)}$</p>""",
    """      <p><b>Điều chế độ rộng xung (PWM)</b> dùng bộ định thời làm <b>bộ đếm</b> tăng 1 sau mỗi $N$ nhịp xung nhịp ($N$: hệ số chia trước; $f_{\\text{clk}}$: tần số xung nhịp gốc). Đếm tới <b>TOP</b> thì quay về 0: mỗi chu kỳ có $\\text{TOP} + 1$ lần đếm.</p>
      <p>$f = \\dfrac{f_{\\text{clk}}}{N \\cdot (\\text{TOP} + 1)}$</p>""",
)
replace_exact(
    Path("lessons/esy/L03_dinh_thoi_pwm.yaml"),
    """      <p><b>Bước 1 — luật so sánh:</b> thêm giá trị so sánh CMP: chân ra ở mức cao (5 V) khi bộ đếm $\\lt$ CMP, mức thấp (0 V) khi còn lại. Hình thu nhỏ TOP = 9: CMP = 3 → cao 3 trên 10 lần đếm; CMP = 7 → cao 7 trên 10.</p>
    focus:
    - 1
    - 2
    - 2
    say: Hình vẽ thu nhỏ với TOP bằng 9. Bước một, thêm một giá trị so sánh, chân ra ở mức cao 5 vôn khi bộ đếm nhỏ hơn giá trị so sánh, và ở mức thấp 0 vôn khi còn lại. Giá trị so sánh bằng 3 cho mức cao 3 phần 10 thời gian, bằng 7 cho 7 phần 10.""",
    """      <p><b>Bước 1 — tần số và luật so sánh:</b> trước tiên tính tần số từ xung nhịp $16$ MHz, chia trước $N=64$, $\\text{TOP}=249$: $f = 16\\,000\\,000 / (64 \\cdot 250) = \\hl{1000}\\text{ Hz}$. Thêm giá trị so sánh CMP: chân ra ở mức cao (5 V) khi bộ đếm $\\lt$ CMP, mức thấp (0 V) khi còn lại. Hình thu nhỏ TOP = 9: CMP = 3 → cao 3 trên 10 lần đếm; CMP = 7 → cao 7 trên 10.</p>
    focus:
    - 1
    - 2
    - 2
    - 2
    say: Hình vẽ thu nhỏ với TOP bằng 9. Bước một, ta tính tần số định thời từ xung nhịp 16 mê-ga-héc chia cho 64 nhân 250 được đúng một nghìn héc. Sau đó thêm một giá trị so sánh, chân ra ở mức cao 5 vôn khi bộ đếm nhỏ hơn giá trị so sánh, và ở mức thấp 0 vôn khi còn lại. Giá trị so sánh bằng 3 cho mức cao 3 phần 10 thời gian, bằng 7 cho 7 phần 10.""",
)

# L05 recap: match N=8 in body instead of N=64
replace_exact(
    Path("lessons/esy/L05_loc_so.yaml"),
    "trung bình trượt $N=64$ giảm nhiễu 8× nhưng thêm trễ hàng chục mẫu.",
    "trung bình trượt $N=8$ mẫu giảm nhiễu căn 8 lần nhưng nhớ nhiều mẫu và thêm trễ lớn hơn.",
)

# L06 sym: explain signed MSB bit so 127.996 is clear
replace_exact(
    Path("lessons/esy/L06_dau_phay_tinh.yaml"),
    "<p><b>Q8.8</b>: số nguyên có dấu 16 bit, coi 8 bit cuối là phần lẻ. Giá trị thật = số nguyên chia $2^8 = 256$.</p>",
    "<p><b>Q8.8</b>: số nguyên có dấu 16 bit (gồm 1 bit dấu ở đầu của 8 bit phần nguyên, nên phần nguyên chỉ đạt $-128$ tới $127$), coi 8 bit cuối là phần lẻ. Giá trị thật = số nguyên chia $2^8 = 256$.</p>",
)

# L07 speed: teach reading 8N1 frame explicitly before computing 9600/10, then covers obj1 -> speed
replace_exact(
    Path("lessons/esy/L07_uart.yaml"),
    """      <p>Hai đầu phải hẹn trước cùng một tốc độ, ví dụ 9600 baud = 9600 bit mỗi giây. Mỗi bit dài $1 / 9600 \\approx 0{,}104$ ms.</p>
      <p>Mỗi byte tốn 10 bit → $9600 / 10 = \\hl{960}$ byte mỗi giây, không phải 1200.</p>
      <div class="box key">Bên nhận thấy cạnh xuống (chỗ dây đổi từ 1 xuống 0) của bit bắt đầu, đợi <b>nửa bit</b>, rồi cứ mỗi một bit lấy mẫu một lần — đúng giữa bit.</div>
    focus:
    - 1
    - 1
    - 2
    - 3
    say: Hai đầu phải hẹn trước cùng một tốc độ, ví dụ 9600 bit mỗi giây. Khi đó mỗi bit dài khoảng 0 phẩy 104 mi li giây. Mỗi byte tốn 10 bit, nên tốc độ là 960 byte mỗi giây, không phải 1200. Bên nhận thấy cạnh xuống, tức chỗ dây đổi từ 1 xuống 0, của bit bắt đầu, đợi nửa bit, rồi cứ mỗi một bit lấy mẫu một lần, đúng vào giữa bit.""",
    """      <p>Đọc khung 8N1 ký tự <code>'A'</code> (<code>0x41</code> = <code>01000001</code>): truyền từ bit thấp trước thành 10 bit <code>[0 | 1,0,0,0,0,0,1,0 | 1]</code> (bắt đầu 0, 8 bit dữ liệu, dừng 1, không chẵn lẻ).</p>
      <p>Hai đầu hẹn tốc độ 9600 baud = 9600 bit mỗi giây (mỗi bit $\\approx 0{,}104$ ms). Mỗi byte tốn 10 bit → $9600 / 10 = \\hl{960}$ byte mỗi giây, không phải 1200.</p>
      <div class="box key">Bên nhận thấy cạnh xuống (chỗ dây đổi từ 1 xuống 0) của bit bắt đầu, đợi <b>nửa bit</b>, rồi cứ mỗi một bit lấy mẫu một lần — đúng giữa bit.</div>
    focus:
    - 1
    - 2
    - 2
    - 3
    - 4
    say: Đọc một khung 8N1 cho chữ A có mã 01000001, bắt đầu bằng bit 0, tám bit dữ liệu gửi từ bit thấp trước, và kết thúc bằng bit 1. Hai đầu phải hẹn trước cùng một tốc độ, ví dụ 9600 bit mỗi giây, nên mỗi bit dài khoảng 0 phẩy 104 mi li giây. Vì mỗi byte tốn đúng 10 bit, tốc độ truyền đạt 960 byte mỗi giây, không phải 1200. Bên nhận thấy cạnh xuống, tức chỗ dây đổi từ 1 xuống 0, của bit bắt đầu, rồi đợi nửa bit. Sau đó nó cứ mỗi một bit lấy mẫu một lần, đúng vào giữa bit.""",
)
replace_exact(
    Path("lessons/esy/L07_uart.yaml"),
    "- objective: 1\n  scene: example",
    "- objective: 1\n  scene: speed",
)

# L08: expand SDA/SCL in sym, expand i2c (kind: concept -> example) with SPI vs I2C summary row, covers obj1 -> i2c, de.md expand ACK
replace_exact(
    Path("lessons/esy/L08_i2c_spi.yaml"),
    "<td>chỉ 2: dữ liệu SDA, xung nhịp SCL</td>",
    "<td>chỉ 2: dữ liệu nối tiếp (SDA), xung nhịp (SCL)</td>",
)
replace_exact(
    Path("lessons/esy/L08_i2c_spi.yaml"),
    """- id: i2c
  kind: concept""",
    """- id: i2c
  kind: example""",
)
replace_exact(
    Path("lessons/esy/L08_i2c_spi.yaml"),
    """      <p class="note">Giữa một byte, dây dữ liệu chỉ được đổi khi xung nhịp ở 0, nên bên nhận không nhầm bit dữ liệu với bắt đầu hay dừng.</p>
    focus:
    - 0
    - '1.2'
    - - '1.3'
      - '1.4'
    - '1.5'
    - 2
    say: Trước khi xem một lần đọc dữ liệu, ta cần hiểu bốn thuật ngữ. Thanh ghi là một ô nhớ nhỏ có đánh số bên trong chip, ví dụ ô chứa nhiệt độ vừa đo. Bắt đầu là khi dây dữ liệu bị kéo xuống 0 trong lúc dây xung nhịp đang ở mức 1, còn dừng là khi dây dữ liệu nhả lên 1 trong lúc xung nhịp đang ở mức 1. Bắt đầu lại là bắt đầu thêm một lần mà không dừng trước, để vi điều khiển giữ đường dây cho mình. Giữa một byte, dây dữ liệu chỉ được đổi khi xung nhịp ở 0, nên bên nhận không nhầm bit dữ liệu với bắt đầu hay dừng.""",
    """      <p class="note">So với SPI dùng 4 đường dây trở lên và chân chọn chip riêng để chạy hàng chục MHz, I²C chỉ dùng 2 dây chung và chọn thiết bị bằng byte địa chỉ kèm bit xác nhận nên gọn dây hơn nhiều. Giữa một byte, dây dữ liệu chỉ được đổi khi xung nhịp ở 0, nên bên nhận không nhầm bit dữ liệu với bắt đầu hay dừng.</p>
    focus:
    - 0
    - '1.2'
    - - '1.3'
      - '1.4'
    - '1.5'
    - 2
    - 2
    say: Trước khi xem một lần đọc dữ liệu, ta cần hiểu bốn thuật ngữ. Thanh ghi là một ô nhớ nhỏ có đánh số bên trong chip, ví dụ ô chứa nhiệt độ vừa đo. Bắt đầu là khi dây dữ liệu bị kéo xuống 0 trong lúc dây xung nhịp đang ở mức 1, còn dừng là khi dây dữ liệu nhả lên 1 trong lúc xung nhịp đang ở mức 1. Bắt đầu lại là bắt đầu thêm một lần mà không dừng trước, để vi điều khiển giữ đường dây cho mình. So với SPI chạy hàng chục mê-ga-héc và phải kéo dây chọn chip riêng, I2C chỉ dùng 2 dây và gửi byte địa chỉ 7 bit nên gọn chân hơn hẳn. Giữa một byte, dây dữ liệu chỉ được đổi khi xung nhịp ở 0, nên bên nhận không nhầm bit dữ liệu với bắt đầu hay dừng.""",
)
replace_exact(
    Path("lessons/esy/L08_i2c_spi.yaml"),
    "- objective: 1\n  scene: example",
    "- objective: 1\n  scene: i2c",
)
replace_exact(
    Path("labs/ESY/L08/de.md"),
    "kèm bit `ACK` cho mỗi byte",
    "kèm 1 bit xác nhận `ACK` cho mỗi byte",
)

# L09, L10, L11, L14 light P1 glosses
replace_exact(
    Path("lessons/esy/L09_lap_lich_rm.yaml"),
    "<p>Tác vụ $i$: chạy tối đa $C_i$, lặp lại mỗi chu kỳ $T_i$, phải xong trước lần thả kế tiếp (hạn = chu kỳ).</p>",
    "<p>Với $n$ tác vụ độc lập, mỗi tác vụ $i$ chạy tối đa $C_i$, lặp lại mỗi chu kỳ $T_i$, phải xong trước lần thả kế tiếp (hạn = chu kỳ).</p>",
)
replace_exact(
    Path("lessons/esy/L09_lap_lich_rm.yaml"),
    "hoặc một khoảng bị chặn.</span></div>",
    "hoặc một khoảng bị chặn (hàm xử lý ngắt là đoạn mã phần cứng kích hoạt ngoài vòng lặp chính).</span></div>",
)
replace_exact(
    Path("lessons/esy/L10_edf_dao_uu_tien.yaml"),
    "<p><b>Hạn sớm nhất</b> (EDF):",
    "<p><b>Hạn sớm nhất</b> (EDF — Earliest Deadline First):",
)
replace_exact(
    Path("lessons/esy/L11_rtos.yaml"),
    "Gọi hàm có thể chờ trong hàm xử lý ngắt",
    "Gọi hàm có thể chờ trong hàm xử lý ngắt (ISR)",
)
replace_exact(
    Path("lessons/esy/L11_rtos.yaml"),
    "<tr><th>quy mô RAM trên RTOS</th>",
    "<tr><th>quy mô bộ nhớ (RAM) trên hệ điều hành thời gian thực (RTOS)</th>",
)
replace_exact(
    Path("lessons/esy/L11_rtos.yaml"),
    "<td>MCU nhỏ (2 KB RAM)</td>",
    "<td>Vi điều khiển (MCU) nhỏ (2 KB RAM)</td>",
)
replace_exact(
    Path("lessons/esy/L14_cap_nhat_an_toan.yaml"),
    "tính lại CRC mới",
    "tính lại mã kiểm tổng (CRC) mới",
)

# L15: add memory strategy choice note to stage5#0 + covers obj3 -> stage5
replace_exact(
    Path("lessons/esy/L15_hanh_trinh_sao_hoa.yaml"),
    """<tr><td>thư viện thành phần dùng lại <b>không cần sửa</b>; công cụ thử đơn vị và thử tích hợp</td><td>“thử cái mình bay” của chặng 1</td></tr></table>
    focus:
    - 1
    - 1
    - '2.2'
    - '2.3'
    - '2.4'
    say: Ở chặng năm, Phòng thí nghiệm Sức đẩy Phản lực viết rằng họ phải hỗ trợ nhiều nhiệm vụ bay hơn bao giờ hết, trên nhiều loại bộ xử lý và hệ điều hành. Ngân sách chặt hơn, lịch ngắn hơn, và lời đáp là một khung phần mềm bay mã nguồn mở. Khung chia phần mềm thành thành phần có giao diện rõ, nối qua cổng, giống tác vụ và hàng đợi ở bài 11. Nó chạy được cả khi không có hệ điều hành, trên vi điều khiển yếu như ở bài 0. Thư viện thành phần dùng lại không cần sửa, kèm công cụ thử đơn vị và thử tích hợp.""",
    """<tr><td>thư viện thành phần dùng lại <b>không cần sửa</b>; công cụ thử đơn vị và thử tích hợp</td><td>“thử cái mình bay” của chặng 1</td></tr></table>
      <p class="note"><b>Chọn chiến lược bộ nhớ cho thiết bị bay:</b> luôn giới hạn cỡ vùng nhớ cố định và giám sát ngưỡng ngay khi phát triển; chỉ dùng khởi động lại định kỳ nếu hệ ngắn ngày có thể dựng lại sạch từ đầu mà không làm mất trạng thái nhiệm vụ.</p>
    focus:
    - 1
    - 1
    - '2.2'
    - '2.3'
    - '2.4'
    - 3
    say: Ở chặng năm, Phòng thí nghiệm Sức đẩy Phản lực viết rằng họ phải hỗ trợ nhiều nhiệm vụ bay hơn bao giờ hết, trên nhiều loại bộ xử lý và hệ điều hành. Ngân sách chặt hơn, lịch ngắn hơn, và lời đáp là một khung phần mềm bay mã nguồn mở. Khung chia phần mềm thành thành phần có giao diện rõ, nối qua cổng, giống tác vụ và hàng đợi ở bài 11. Nó chạy được cả khi không có hệ điều hành, trên vi điều khiển yếu như ở bài 0. Thư viện thành phần dùng lại không cần sửa, kèm công cụ thử đơn vị và thử tích hợp. Để giữ ổn định dài ngày, ta chọn giới hạn vùng nhớ cố định và giám sát ngưỡng, chỉ khởi động lại định kỳ cho thiết bị ngắn ngày chịu được mất trạng thái.""",
)
replace_exact(
    Path("lessons/esy/L15_hanh_trinh_sao_hoa.yaml"),
    "- objective: 3\n  scene: practice",
    "- objective: 3\n  scene: stage5",
)

# ---------------------------------------------------------------------------
# 5. BCH
# ---------------------------------------------------------------------------
# L00: ms gloss on show
replace_exact(
    Path("lessons/bch/L00_so_cai_phan_tan.yaml"),
    "lúc 0 ms, “trả Chi” lúc 10 ms",
    "lúc 0 ms (mi-li-giây), “trả Chi” lúc 10 ms",
)
# L01: SHA-256 gloss on show + de.md
replace_exact(
    Path("lessons/bch/L01_chuoi_bam.yaml"),
    "<p><b>Hàm băm</b> SHA-256:",
    "<p><b>Hàm băm mật mã</b> SHA-256 (thuật toán băm an toàn 256 bit):",
)
# L03: RSA gloss + check#1 check address=hash(pubkey) + covers obj3 -> check
replace_exact(
    Path("lessons/bch/L03_chu_ky_khoa.yaml"),
    "<tr><td><b>khoá bí mật</b> $d$</td>",
    "<tr><td><b>khoá bí mật</b> $d$ (hệ mật mã RSA)</td>",
)
replace_exact(
    Path("lessons/bch/L03_chu_ky_khoa.yaml"),
    """<tr><td>ký rồi kiểm với mọi h từ 0 tới 3232</td><td>3233 / 3233 lần trả lại đúng h ✓</td></tr></table>
    focus:
    - 0
    - '1.2'
    - '1.3'
    say: Ta thêm hai phép thử nữa, lần này để máy tính làm. Chữ ký lệch chỉ một đơn vị, 2165 mũ 17 lấy dư cho 3233, ra 79, khác hẳn 3010, nên đoán bừa chữ ký không qua được. Máy ký rồi kiểm với mọi giá trị h từ 0 tới 3232, và cả 3233 lần đều trả lại đúng h, nên phép kiểm luôn đảo ngược được phép ký.""",
    """<tr><td>ký rồi kiểm với mọi h từ 0 tới 3232</td><td>3233 / 3233 lần trả lại đúng h ✓</td></tr>
      <tr><td>băm khoá công khai $e, n$ thành địa chỉ</td><td>đổi 1 ký tự khoá là địa chỉ đổi khác hoàn toàn ✓</td></tr></table>
    focus:
    - 0
    - '1.2'
    - '1.3'
    - '1.4'
    say: Ta thêm ba phép thử nữa, lần này để máy tính làm. Chữ ký lệch chỉ một đơn vị, 2165 mũ 17 lấy dư cho 3233, ra 79, khác hẳn 3010, nên đoán bừa chữ ký không qua được. Máy ký rồi kiểm với mọi giá trị h từ 0 tới 3232, và cả 3233 lần đều trả lại đúng h, nên phép kiểm luôn đảo ngược được phép ký. Khi băm khoá công khai để ra địa chỉ nhận tiền, đổi một ký tự của khoá là địa chỉ đổi khác hoàn toàn, giúp người kiểm đối chiếu đúng chủ.""",
)
replace_exact(
    Path("lessons/bch/L03_chu_ky_khoa.yaml"),
    "- objective: 3\n  scene: practice",
    "- objective: 3\n  scene: check",
)
replace_exact(
    Path("labs/BCH/L03/de.md"),
    "Với cặp khoá RSA đồ chơi",
    "Với cặp khoá hệ mật mã bất đối xứng RSA (Rivest–Shamir–Adleman) đồ chơi",
)

# L04: UTXO & RAM gloss + add UTXO vs Account check row in check#1 (covers obj3 -> check)
replace_exact(
    Path("lessons/bch/L04_dong_chua_tieu.yaml"),
    "<tr><th>quy mô UTXO vs tài khoản</th>",
    "<tr><th>quy mô đầu ra chưa tiêu (UTXO) vs tài khoản</th>",
)
replace_exact(
    Path("lessons/bch/L04_dong_chua_tieu.yaml"),
    "trong RAM nút",
    "trong bộ nhớ làm việc (RAM) nút",
)
replace_exact(
    Path("lessons/bch/L04_dong_chua_tieu.yaml"),
    """<tr><td>ví sau 3,9 + người nhận 6 + phí 0,1</td><td>$\\hl{10}$ ✓ không mất, không thêm</td></tr></table>
    focus:
    - 0
    - '1.2'
    - '1.3'
    say: Một phép thử nữa là đếm lại tổng tiền trước và sau. Ví trước có 5 cộng 3 cộng 2, bằng 10. Sau giao dịch, ví còn 3 phẩy 9, người nhận có 6, người tạo khối giữ phí 0 phẩy 1, cộng lại vẫn đúng 10, nên không có đồng nào mất đi hay tự sinh ra.""",
    """<tr><td>ví sau 3,9 + người nhận 6 + phí 0,1</td><td>$\\hl{10}$ ✓ không mất, không thêm</td></tr>
      <tr><td>so với mô hình tài khoản (lưu 1 số dư)</td><td>tài khoản chỉ cập nhật 10 → 3,9 gọn nhẹ hơn giữ 2 đồng xu (5; 3), nhưng UTXO kiểm song song tốt hơn</td></tr></table>
    focus:
    - 0
    - '1.2'
    - '1.3'
    - '1.4'
    say: Một phép thử nữa là đếm lại tổng tiền trước và sau. Ví trước có 5 cộng 3 cộng 2, bằng 10. Sau giao dịch, ví còn 3 phẩy 9, người nhận có 6, người tạo khối giữ phí 0 phẩy 1, cộng lại vẫn đúng 10, nên không có đồng nào mất đi hay tự sinh ra. So với mô hình tài khoản chỉ lưu một con số dư duy nhất 3 phẩy 9, mô hình đồng chưa tiêu tốn nhiều bản ghi hơn nhưng cho phép kiểm nhiều giao dịch song song độc lập.""",
)
replace_exact(
    Path("labs/BCH/L04/de.md"),
    "trong giao dịch UTXO",
    "trong giao dịch đầu ra chưa tiêu (UTXO)",
)

# L06: obj1 -> example (add longest/heaviest work note in example#0), obj3 -> check (add confirmation choice rule in check#1)
replace_exact(
    Path("lessons/bch/L06_dong_thuan_nakamoto.yaml"),
    """  - show: |
      <p><b>Bước 1 — số khối kẻ gian kỳ vọng</b> ($q = 0{,}1$, $z = 6$): $\\frac{q}{p} = \\frac{0{,}1}{0{,}9} \\approx 0{,}111$, nên $\\lambda = 6 \\cdot 0{,}111 \\approx \\hl{0{,}667}$ khối.</p>
    say: Bước một, làm tay công thức với q bằng 0 phẩy 1 và z bằng 6. q chia p bằng 0 phẩy 1 chia 0 phẩy 9, khoảng 0 phẩy 111, nên lam-đa bằng 6 nhân 0 phẩy 111, khoảng 0 phẩy 667 khối. Trong lúc chờ 6 khối, kẻ gian trung bình chỉ đào được chừng hai phần ba khối.""",
    """  - show: |
      <p><b>Bước 1 — nguyên tắc chọn chuỗi và số khối kẻ gian kỳ vọng</b> ($q = 0{,}1$, $z = 6$): giữa nhánh 3 khối độ khó 1 (tổng công 3) và nhánh 2 khối độ khó 2 (tổng công 4), nút theo nhánh 4. Tính công thức: $\\frac{q}{p} = \\frac{0{,}1}{0{,}9} \\approx 0{,}111$, nên $\\lambda = 6 \\cdot 0{,}111 \\approx \\hl{0{,}667}$ khối.</p>
    say: Bước một, nhắc quy tắc chọn chuỗi có tổng công lớn nhất, chẳng hạn giữa nhánh 3 khối độ khó 1 và nhánh 2 khối độ khó 2 thì nút theo nhánh tổng công 4, rồi mới tính số khối kẻ gian kỳ vọng với q bằng 0 phẩy 1 và z bằng 6. q chia p bằng 0 phẩy 1 chia 0 phẩy 9, khoảng 0 phẩy 111, nên lam-đa bằng 6 nhân 0 phẩy 111, khoảng 0 phẩy 667 khối. Trong lúc chờ 6 khối, kẻ gian trung bình chỉ đào được chừng hai phần ba khối.""",
)
replace_exact(
    Path("lessons/bch/L06_dong_thuan_nakamoto.yaml"),
    """<tr><td>công thức xấp xỉ 2008</td><td>0,177 — thấp hơn hẳn</td></tr></table>
    focus:
    - 1
    - '1.2'
    - '1.3'
    - '1.4'
    say: Đường thứ hai, cho máy chơi thật 20000 cuộc đua khối, với kẻ gian nắm 30 phần trăm sức tính và cửa hàng chờ 5 khối. Kẻ gian thắng 3979 lần, nên tỉ lệ thắng khoảng 0 phẩy 199. Con số đó rất gần giá trị chính xác 0 phẩy 1976. Còn công thức xấp xỉ năm 2008 chỉ cho 0 phẩy 177, thấp hơn hẳn so với cuộc đua thật.""",
    """<tr><td>công thức xấp xỉ 2008</td><td>0,177 — thấp hơn hẳn</td></tr>
      <tr><td>chọn ngưỡng xác nhận theo giá trị (khi $q=0{,}1$)</td><td>cốc cà phê chọn $z=1$ (rủi ro 20%); giao dịch lớn chờ $z=6$ (rủi ro $\\approx 0{,}06\\%$)</td></tr></table>
    focus:
    - 1
    - '1.2'
    - '1.3'
    - '1.4'
    - '1.5'
    say: Đường thứ hai, cho máy chơi thật 20000 cuộc đua khối, với kẻ gian nắm 30 phần trăm sức tính và cửa hàng chờ 5 khối. Kẻ gian thắng 3979 lần, nên tỉ lệ thắng khoảng 0 phẩy 199. Con số đó rất gần giá trị chính xác 0 phẩy 1976. Còn công thức xấp xỉ năm 2008 chỉ cho 0 phẩy 177, thấp hơn hẳn so với cuộc đua thật. Từ kết quả đó, giao dịch giá trị nhỏ có thể chốt sớm sau 1 khối, còn khoản tiền lớn cần chờ từ 6 khối trở lên theo công thức chính xác.""",
)

# L07: BFT + validator gloss + check#0 compare probabilistic vs deterministic finality + covers obj3 -> check
replace_exact(
    Path("lessons/bch/L07_bang_chung_co_phan.yaml"),
    "<tr><td>$n$</td><td>số bên xác thực (cùng quyền biểu quyết)</td></tr>",
    "<tr><td>$n$</td><td>số bên xác thực (validator — nút cùng quyền biểu quyết chịu lỗi Byzantine BFT)</td></tr>",
)
replace_exact(
    Path("lessons/bch/L07_bang_chung_co_phan.yaml"),
    """<tr><td>3, muốn chịu 1</td><td>chỉ đợi được 2</td><td>3</td><td>1</td><td>phần chung có thể toàn gian lận</td></tr></table>
    focus:
    - 1
    - '1.2'
    - '1.3'
    - '1.4'
    say: Kiểm bằng đường khác, không dùng công thức mà cho máy liệt kê mọi nhóm chốt có thể, rồi đo phần chung nhỏ nhất của từng cặp. Với 4 bên, có 4 nhóm 3 phiếu, phần chung nhỏ nhất là 2, lớn hơn 1 bên gian lận, nên an toàn. Với 7 bên chịu 2 gian lận, có 21 nhóm 5 phiếu, phần chung nhỏ nhất là 3, vẫn an toàn. Còn 3 bên mà muốn chịu 1 bên gian lận thì chỉ đợi được 2 phiếu, phần chung có thể chỉ 1 bên, và đó có thể chính là bên gian lận, nên 3 bên là không đủ.""",
    """<tr><td>3, muốn chịu 1</td><td>chỉ đợi được 2</td><td>3</td><td>1</td><td>phần chung có thể toàn gian lận</td></tr>
      <tr><td>so cuối cùng tất định vs xác suất (bài 6)</td><td>chờ $z$ khối vs đạt $n-f$ phiếu</td><td>—</td><td>chờ $z$ xác suất đảo &gt; 0</td><td>BFT tất định: chốt xong không đảo được nếu $\\le f$ gian lận ✓</td></tr></table>
    focus:
    - 1
    - '1.2'
    - '1.3'
    - '1.4'
    - '1.5'
    say: Kiểm bằng đường khác, không dùng công thức mà cho máy liệt kê mọi nhóm chốt có thể, rồi đo phần chung nhỏ nhất của từng cặp. Với 4 bên, có 4 nhóm 3 phiếu, phần chung nhỏ nhất là 2, lớn hơn 1 bên gian lận, nên an toàn. Với 7 bên chịu 2 gian lận, có 21 nhóm 5 phiếu, phần chung nhỏ nhất là 3, vẫn an toàn. Còn 3 bên mà muốn chịu 1 bên gian lận thì chỉ đợi được 2 phiếu, phần chung có thể chỉ 1 bên, và đó có thể chính là bên gian lận, nên 3 bên là không đủ. Điều này khác hẳn tính cuối cùng xác suất ở bài 6, thay vì xác suất đảo giảm dần nhưng vẫn lớn hơn 0, cơ chế chịu lỗi Byzantine chốt dứt điểm ngay khi đủ phiếu.""",
)
replace_exact(
    Path("lessons/bch/L07_bang_chung_co_phan.yaml"),
    "- objective: 3\n  scene: example",
    "- objective: 3\n  scene: check",
)
replace_exact(
    Path("labs/BCH/L07/de.md"),
    "ngưỡng chịu lỗi BFT và số phiếu chốt cho cụm 16 validator",
    "ngưỡng chịu lỗi Byzantine (BFT) và số phiếu chốt cho cụm 16 bên xác thực (validator)",
)

# L09/de.md: add self in recv(self, vault)
replace_exact(
    Path("labs/BCH/L09/de.md"),
    "có hàm `recv(vault)` tự gọi lại",
    "có phương thức `recv(self, vault)` tự gọi lại",
)

# L10: Layer-1 & TPS gloss
replace_exact(
    Path("lessons/bch/L10_mo_rong.yaml"),
    "<p><b>Thông lượng</b> =",
    "<p><b>Thông lượng chuỗi gốc</b> (TPS — giao dịch mỗi giây trên tầng 1, Layer-1) =",
)
replace_exact(
    Path("labs/BCH/L10/de.md"),
    "Tính thông lượng tối đa (TPS)",
    "Tính thông lượng giao dịch mỗi giây tối đa (TPS)",
)

# L12: RAM/GB/TWh glosses + stage5 decision note for obj3 -> stage5
replace_exact(
    Path("lessons/bch/L12_hanh_trinh_dong_thuan.yaml"),
    "<tr><td>Bước 4. so với RAM 2 GB năm 2008</td>",
    "<tr><td>Bước 4. so với bộ nhớ làm việc (RAM) 2 giga-byte (GB) năm 2008</td>",
)
replace_exact(
    Path("lessons/bch/L12_hanh_trinh_dong_thuan.yaml"),
    "<td>21 TWh chia 0,0026 TWh</td>",
    "<td>21 tê-ra-oát-giờ (TWh, tỉ số điện) chia 0,0026 TWh</td>",
)
replace_exact(
    Path("lessons/bch/L12_hanh_trinh_dong_thuan.yaml"),
    """      <p class="note">Hợp nhất <b>không</b> có tính năng rút cổ phần — tính năng này được tách sang một bản nâng cấp sau, để bản lớn tập trung vào việc chuyển đồng thuận. Thực hành: nhịp thời gian cố định, phạt khi ký mâu thuẫn, giới hạn tốc độ thao tác nguy hiểm, chia việc lớn thành nhiều bản nâng cấp. Điều kiện: quy tắc chỉ an toàn khi cổ phần không dồn vào vài bên — hai phần ba tính theo cổ phần, không theo số người.</p>
    focus:
    - 1
    - 1
    - 1
    - 2
    - 2
    - 2
    say: Con số 0 phẩy 33 phần trăm là cách tính cũ. Từ bản nâng cấp ngày 7 tháng 5 năm 2025, mỗi kỷ nguyên chỉ cho rút tối đa 256 đồng tiền gốc. Một ngày có 225 kỷ nguyên, nên mỗi ngày rút tối đa 225 nhân 256, bằng 57 nghìn 600 đồng, và khi tổng cổ phần lớn thì tỉ lệ rút còn thấp hơn. Hợp nhất không có tính năng rút cổ phần, tính năng đó được tách sang bản nâng cấp sau. Thực hành rút ra là nhịp thời gian cố định, phạt khi ký mâu thuẫn, giới hạn tốc độ việc nguy hiểm, và chia việc lớn thành nhiều bản. Điều kiện là cổ phần không dồn vào vài bên, vì như bài 7, hai phần ba tính theo cổ phần chứ không theo số người.""",
    """      <p class="note">Hợp nhất <b>không</b> có tính năng rút cổ phần — tính năng này được tách sang một bản nâng cấp sau, để bản lớn tập trung vào việc chuyển đồng thuận. Thực hành: nhịp thời gian cố định, phạt khi ký mâu thuẫn, giới hạn tốc độ thao tác nguy hiểm, chia việc lớn thành nhiều bản nâng cấp. Điều kiện: quy tắc chỉ an toàn khi cổ phần không dồn vào vài bên — hai phần ba tính theo cổ phần, không theo số người.</p>
      <p class="note"><b>Chọn cách nâng cấp theo quy mô mạng:</b> mạng nhỏ vài công ty quen nhau chọn ngày hẹn nâng cấp cứng và thử song song; mạng công khai hàng vạn nút vô danh bắt buộc nâng cấp mềm tương thích ngược kèm ngưỡng tín hiệu sẵn sàng.</p>
    focus:
    - 1
    - 1
    - 1
    - 2
    - 2
    - 2
    - 3
    say: Con số 0 phẩy 33 phần trăm là cách tính cũ. Từ bản nâng cấp ngày 7 tháng 5 năm 2025, mỗi kỷ nguyên chỉ cho rút tối đa 256 đồng tiền gốc. Một ngày có 225 kỷ nguyên, nên mỗi ngày rút tối đa 225 nhân 256, bằng 57 nghìn 600 đồng, và khi tổng cổ phần lớn thì tỉ lệ rút còn thấp hơn. Hợp nhất không có tính năng rút cổ phần, tính năng đó được tách sang bản nâng cấp sau. Thực hành rút ra là nhịp thời gian cố định, phạt khi ký mâu thuẫn, giới hạn tốc độ việc nguy hiểm, và chia việc lớn thành nhiều bản. Điều kiện là cổ phần không dồn vào vài bên, vì như bài 7, hai phần ba tính theo cổ phần chứ không theo số người. Khi chọn cách nâng cấp cho mạng của mình, nhóm nhỏ vài bên biết nhau có thể hẹn ngày chuyển cứng sau khi thử song song, còn mạng công khai hàng vạn nút phải ưu tiên nâng cấp mềm tương thích ngược.""",
)
replace_exact(
    Path("lessons/bch/L12_hanh_trinh_dong_thuan.yaml"),
    "- objective: 3\n  scene: practice",
    "- objective: 3\n  scene: stage5",
)

# ---------------------------------------------------------------------------
# 6. Sync audit/s9_11/up_s11.py COVERS & BCH L09 / ESY L08 de.md
# ---------------------------------------------------------------------------
up11 = Path("audit/s9_11/up_s11.py")
replace_exact(
    up11,
    '"RBM:L10": [(1, \'addi\'), (2, \'ponly\'), (3, \'pitfalls\')],',
    '"RBM:L10": [(1, \'ponly\'), (1, \'addi\'), (1, \'addd\'), (2, \'ponly\'), (3, \'pitfalls\')],',
)
replace_exact(
    up11,
    '"RBM:L17": [(1, \'stage1\'), (1, \'stage2\'), (1, \'stage3\'), (1, \'stage4\'), (2, \'stage2\'), (2, \'check\'), (3, \'practice\')],',
    '"RBM:L17": [(1, \'stage1\'), (1, \'stage2\'), (1, \'stage3\'), (1, \'stage4\'), (2, \'stage1\'), (2, \'stage2\'), (2, \'check\'), (2, \'stage4\'), (3, \'stage4\')],',
)
replace_exact(
    up11,
    '"ESY:L07": [(1, \'example\'), (2, \'speed\'), (3, \'example\')],',
    '"ESY:L07": [(1, \'speed\'), (2, \'speed\'), (3, \'example\')],',
)
replace_exact(
    up11,
    '"ESY:L08": [(1, \'example\'), (2, \'i2c\'), (3, \'example\')],',
    '"ESY:L08": [(1, \'i2c\'), (2, \'i2c\'), (3, \'example\')],',
)
replace_exact(
    up11,
    '"ESY:L15": [(1, \'stage1\'), (1, \'stage2\'), (1, \'stage3\'), (1, \'stage4\'), (1, \'stage5\'), (2, \'check\'), (3, \'practice\')],',
    '"ESY:L15": [(1, \'stage1\'), (1, \'stage2\'), (1, \'stage3\'), (1, \'stage4\'), (1, \'stage5\'), (2, \'check\'), (3, \'stage5\')],',
)
replace_exact(
    up11,
    '"ROB:L04": [(1, \'example\'), (2, \'example\'), (3, \'practice\')],',
    '"ROB:L04": [(1, \'example\'), (2, \'example\'), (3, \'check\')],',
)
replace_exact(
    up11,
    '"GFX:L13": [(1, \'stage1\'), (1, \'stage2\'), (1, \'stage3\'), (1, \'stage4\'), (2, \'check\'), (3, \'practice\')],',
    '"GFX:L13": [(1, \'stage1\'), (1, \'stage2\'), (1, \'stage3\'), (1, \'stage4\'), (2, \'check\'), (3, \'stage4\')],',
)
replace_exact(
    up11,
    '"BCH:L03": [(1, \'example\'), (2, \'check\'), (3, \'practice\')],',
    '"BCH:L03": [(1, \'example\'), (2, \'check\'), (3, \'check\')],',
)
replace_exact(
    up11,
    '"BCH:L07": [(1, \'example\'), (2, \'check\'), (3, \'example\')],',
    '"BCH:L07": [(1, \'example\'), (2, \'check\'), (3, \'check\')],',
)
replace_exact(
    up11,
    '"BCH:L12": [(1, \'stage1\'), (1, \'stage2\'), (1, \'stage3\'), (1, \'stage4\'), (1, \'stage5\'), (2, \'check\'), (3, \'practice\')],',
    '"BCH:L12": [(1, \'stage1\'), (1, \'stage2\'), (1, \'stage3\'), (1, \'stage4\'), (1, \'stage5\'), (2, \'check\'), (3, \'stage5\')],',
)
replace_exact(up11, "kèm bit `ACK` cho mỗi byte", "kèm 1 bit xác nhận `ACK` cho mỗi byte")
replace_exact(up11, "Với cặp khoá RSA đồ chơi", "Với cặp khoá hệ mật mã bất đối xứng RSA (Rivest–Shamir–Adleman) đồ chơi")
replace_exact(up11, "trong giao dịch UTXO", "trong giao dịch đầu ra chưa tiêu (UTXO)")
replace_exact(up11, "ngưỡng chịu lỗi BFT và số phiếu chốt cho cụm 16 validator", "ngưỡng chịu lỗi Byzantine (BFT) và số phiếu chốt cho cụm 16 bên xác thực (validator)")
replace_exact(up11, "có hàm `recv(vault)` tự gọi lại", "có phương thức `recv(self, vault)` tự gọi lại")
replace_exact(up11, "Tính thông lượng tối đa (TPS)", "Tính thông lượng giao dịch mỗi giây tối đa (TPS)")

# Sanity YAML load on all touched lessons
for pat in (
    "lessons/rbm/L00*.yaml", "lessons/rbm/L10*.yaml", "lessons/rbm/L13*.yaml", "lessons/rbm/L17*.yaml",
    "lessons/gfx/L06*.yaml", "lessons/gfx/L09*.yaml", "lessons/gfx/L13*.yaml",
    "lessons/rob/L03*.yaml", "lessons/rob/L04*.yaml",
    "lessons/esy/L02*.yaml", "lessons/esy/L03*.yaml", "lessons/esy/L05*.yaml",
    "lessons/esy/L06*.yaml", "lessons/esy/L07*.yaml", "lessons/esy/L08*.yaml",
    "lessons/esy/L09*.yaml", "lessons/esy/L10*.yaml", "lessons/esy/L11*.yaml",
    "lessons/esy/L14*.yaml", "lessons/esy/L15*.yaml",
    "lessons/bch/L00*.yaml", "lessons/bch/L01*.yaml", "lessons/bch/L03*.yaml",
    "lessons/bch/L04*.yaml", "lessons/bch/L06*.yaml", "lessons/bch/L07*.yaml",
    "lessons/bch/L10*.yaml", "lessons/bch/L12*.yaml",
):
    p = next(Path(".").glob(pat))
    yaml.safe_load(p.read_text(encoding="utf-8"))

print("fix_s11_v3.py: ALL PATCHES APPLIED & PARSED CLEANLY!")
