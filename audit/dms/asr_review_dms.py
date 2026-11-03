"""Ghi `asr_reviewed` cho câu ASR gắn cờ của khoá DMS — đọc thẳng out/DMS/<id>/asr_report.md (bảng đầu, cột “đã xem xét” = —).
Lý do theo nhóm đã có bằng chứng dò (audit/dms/probes/*.md); câu không thuộc nhóm nào phải có lý do viết tay ở HAND, nếu không
script in “THIẾU LÝ DO” và KHÔNG ghi — câu đó phải sửa lời đọc (câu ngắn) hoặc người nghe lại.
Bài sinh từ mẫu (audit/dms/src/*.tpl.yaml) thì ghi vào MẪU rồi ghép lại, vì mẫu là nguồn duy nhất.
Chạy: .venv/Scripts/python audit/dms/asr_review_dms.py L01 L02 …  (khoá khác: --course CSA L00 L01 …)"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
import lv  # noqa: E402

P2 = "chữ cái “p” đọc thô — probe audit/dms/probes/p2_chu_p.md: thô 7/8, đối chứng “tê” 0/8; ASR lẫn p/t, không phải TTS đọc sai; chữ hiện trên màn hình"
HAND = {
    'Giờ ta xem một cách xen kẽ cụ thể giữa hai luồng.':
        'câu đã viết dài ra (bản 6 từ khớp 0,714); vẫn xen/xem, kẽ/kẻ, luồng/luôn: cặp nhầm âm cuối n/m, ng/n và thanh ngã/hỏi lặp ở mọi câu có “luồng” của L01, L04, L09 — NOT_VERIFIED bằng tai người',
    # ── DBS (2026-10-29): bản chép trong out/DBS/<id>/asr_report.md ──
    'Có ba loại ràng buộc toàn vẹn.':
        'ASR chép “Có 3 loại tràn buộc toàn vén”: ràng/tràn (r → tr, đã biết ở TOC “Rai” → “trai”), vẹn/vén (thanh nặng/sắc); “ràng buộc toàn vẹn” chép đúng ở các câu dài của L00 — NOT_VERIFIED bằng tai người',
    'Câu ba, xoá sinh viên mã 4.':
        'ASR chép “Câu 3. Xóa sinh viên mả búng”: mã/mả (thanh ngã/hỏi), “bốn” → “búng” ở cuối câu ngắn; số 4 hiện trên màn hình, các câu khác của L00 có “mã” chép đúng — NOT_VERIFIED bằng tai người',
    'Bảng có bốn dòng.':
        'ASR chép “Bạn có bốn dòng”: bảng/bạn (nhầm âm cuối ng/n và thanh), “bốn dòng” đúng; cặp bảng/bản lặp ở nhiều bài DBS — NOT_VERIFIED bằng tai người',
    'Từ khoá ở cuối nghĩa là giảm dần.':
        'ASR chép “Tư khóa ở cuối nghĩa là giảm dân”: từ/tư, dần/dân (thanh huyền/ngang); nghĩa giữ nguyên — NOT_VERIFIED bằng tai người',
    'Khoá là mã số.':
        'ASR chép “Khoá là mả số?”: mã/mả (thanh ngã/hỏi, ASR lẫn thường xuyên); câu 4 từ khớp 0,75 > 0,7 nên không viết lại — NOT_VERIFIED bằng tai người',
    'Ta được bảng sinh viên gồm mã số, tên, mã lớp, và bảng lớp gồm mã lớp, tên lớp, đúng hai bảng của bài 0.':
        'ASR chép “bán sinh viên gồm mả số … đúng 2 bản của bài không”: bảng/bán/bản, mã/mả là cặp thanh và âm cuối ng/n ASR lẫn trong mọi bài DBS; “bài 0” → “bài không” đúng âm — NOT_VERIFIED bằng tai người',
    'Lỗi thứ nhất, tách bảng theo cột tuỳ ý.':
        'ASR chép “tách bản theo cục tùy ý”: bảng/bản (ng/n), cột/cục (vần ôt/uc); “tách … theo … tuỳ ý” đúng — NOT_VERIFIED bằng tai người',
    'Cách sửa là tách theo phụ thuộc vi phạm, một bảng giữ mã lớp với tên lớp, bảng kia giữ phần còn lại.':
        'ASR chép “Các sửa … một bản giữ mà lớp … bản kỳ giữ phần còn lại”: cách/các (âm cuối ch/c), bảng/bản, mã/mà, kia/kỳ — nhầm thanh và âm cuối của ASR; câu đủ nghĩa — NOT_VERIFIED bằng tai người',
    'Câu hai, lồng theo khối với 52 trang đệm thì sao?':
        'ASR chép “lòng theo khối với 52 trang đệm thứ 6”: lồng/lòng (thanh), “thì sao” → “thứ sáu” (cặp âm gần ở cuối câu hỏi); số 52 khớp — NOT_VERIFIED bằng tai người',
    'Nối theo khối chia nhỏ số lần đọc S.':
        'ASR chép “chiên nhỏ số lần độc X”: chia/chiên, đọc/độc (thanh), chữ S → X (tên chữ cái đọc kiểu Việt “ét”/“ích”, nhóm đã biết); chữ S hiện trên màn hình — NOT_VERIFIED bằng tai người',
    'Nếu có lỗi giữa chừng, hệ quản trị tự huỷ cả giao dịch.':
        'ASR chép “giữa chân, hề quản trị từ hủy cả giao dịch”: chừng/chân (vần), hệ/hề, tự/từ (thanh); “quản trị … hủy cả giao dịch” đúng — NOT_VERIFIED bằng tai người',
    'Câu một, đây là dị thường nào?':
        'ASR chép “Câu 1, đây là dĩ thương nào?”: dị/dĩ, thường/thương (thanh); câu hỏi 6 từ khớp 0,714 > 0,7 — NOT_VERIFIED bằng tai người',
    'Mức đọc đã ghi nhận chặn đọc bẩn, nhưng vẫn cho đọc không lặp lại và bóng ma.':
        'ASR chép “Mức độc … chặn độc bẩn … cho độc không lập lại”: đọc/độc (thanh nặng), lặp/lập — nhầm thanh của ASR; “đã ghi nhận”, “bóng ma” đúng — NOT_VERIFIED bằng tai người',
    'Chuẩn SQL định nghĩa bốn mức cô lập.':
        'SQL đọc “ét quy eo” (lexicon DBS p1 8/8); ASR chép “SQ Eo” — đủ ba chữ cái, chỉ khác cách viết',
    # ── ESY (2026-10-29) ──
    'Một tác vụ có hạn 10 mi li giây.':
        'ASR chép “Một tác vũ có hạn 10 mili dây”: “mili dây” = cách ASR viết liền “mi li giây” (gi/d), vụ/vũ (thanh) — câu 8 âm tiết; NOT_VERIFIED bằng tai người',
    'Xung nhịp 16 mê-ga-héc, so với khoảng 3 gi-ga-héc.':
        'ASR chép “16 MHz … 3 GHz”: ASR tự viết đơn vị thành ký hiệu — chứng tỏ nghe đúng “mê-ga-héc”, “gi-ga-héc”; điểm thấp chỉ do cách viết',
    'So với máy tính xách tay, chênh lệch rất lớn.':
        'ASR chép “so với mấy tính sách tay trên lật rất lớn”: máy/mấy, x/s, chênh lệch/trên lật (ch/tr, l) — nhầm âm điển hình của ASR tiếng Việt; NOT_VERIFIED bằng tai người',
    'Một mảng 4 ki-lô-byte đã vượt cả 2 ki-lô-byte bộ nhớ, nên mỗi byte, mỗi mi li giây đều phải tính.':
        'ASR chép “4 kilobytes … 2 kilobytes … mili dây”: ASR viết liền đơn vị (nghe đúng “ki-lô-byte”); gi/d của ASR',
    'Lỗi thứ ba, viết mã nhúng như viết mã cho máy tính.':
        'ASR chép “Lội thứ ba, viết mạ nhúng …”: lỗi/lội, mã/mạ — nhầm thanh ngã/nặng điển hình của ASR (câu tương tự “Lỗi thứ …” khớp ở mọi khoá khác); NOT_VERIFIED bằng tai người',
    'Một vi điều khiển phổ biến chỉ có 2 ki-lô-byte bộ nhớ, so với 16 gi-ga-byte, ít hơn tám triệu lần.':
        'ASR chép “2 kilobyte … 16 gigabyte”: ASR viết liền đơn vị — nghe đúng; chỉ khác cách viết',
    # ── ESY L01–L14 (2026-10-29): lý do theo bản chép trong out/ESY/<id>/asr_report.md ──
    'Lỗi thứ ba, đếm bit từ trái sang.':
        'ASR chép “Lội thứ Ba, đếm biết từ trái sang”: lỗi/lội nhầm thanh (cùng mẫu “Lỗi thứ …” ở các bài khác chép đúng), bit → “biết” như probe p1 CSA (không phân định âm cuối t/ch) — NOT_VERIFIED bằng tai người',
    'Giả sử phím dội tối đa 5 mi li giây.':
        'ASR chép “giả sự phím dội tối đa 5 mili dây”: sử/sự nhầm thanh, “mi li giây” → “mili dây” (gi/d ASR đã biết); “phím dội” và số 5 chép đúng',
    'Chip 8 bit đọc số 16 bit làm hai lần.':
        'ASR chép “Chịp 8 biết đọc số 16 biết làm 2 lần”: chip đọc thô (foreign_ok), “chịp” cùng âm lệch thanh; bit → “biết” như probe p1 CSA; số 8, 16, hai chép đúng',
    'Câu một, phím dội tối đa 8 mi li giây, lấy mẫu mỗi 2 mi li giây, cần mấy mẫu liên tiếp giống nhau?':
        'ASR chép “phiếm dụi tối ra 8 mili giây, lấy mẫu mỗi 2 mili giây cần mấy mẫu liên tiếp giống nhau”: nhầm vần/thanh ở “phím dội”, đ/r; câu cùng từ “phím dội” ở khung 15 chép đúng; các số 8, 2 khớp — NOT_VERIFIED bằng tai người',
    'Câu một, xung nhịp 8 mê-ga-héc, hệ số chia trước 8, cần TOP bằng bao nhiêu để được một nghìn héc?':
        'ASR chép “xuân nhịp 8 MHz … cần tốt bằng bao nhiêu để được 1000 Hz”: “mê-ga-héc” → MHz, “héc” → Hz là đúng đơn vị viết tắt; xung/xuân nhầm vần (cùng nhầm ở L08); TOP đọc thô, chữ TOP hiện trên màn hình',
    'Đề-xi-ben là thang lô-ga-rít, thêm khoảng 6 nghĩa là tỉ số biên độ gấp đôi.':
        'ASR chép “Deciben là thang logatic … tỷ số biên độ gấp đôi”: đề-xi-ben → “Deciben” đúng từ, lô-ga-rít → “logatic” cùng bốn âm lệch âm cuối, tỉ/tỷ chỉ khác chính tả — NOT_VERIFIED bằng tai người',
    'Câu một, mỗi bậc bao nhiêu mi li vôn?':
        'ASR chép “Câu 1. Mỗi bậc bao nhiêu mili vốn?”: “mi li vôn” → “mili vốn” lệch thanh; câu khác có cùng đơn vị (khung 19) chép “mV” — đúng đơn vị',
    'Với một sóng sin dùng hết thang đo, tỉ số tín hiệu trên nhiễu lượng tử xấp xỉ 6 phẩy 02 nhân n, cộng 1 phẩy 76, tính bằng đề-xi-ben.':
        'ASR chép “sóng sinh … nhiễu lượng từ sắp xị 6,02n n cộng 1,76”: sin → “sinh” cùng âm (foreign_ok), tử/từ và xấp/sắp nhầm thanh/âm đầu; các số 6,02 và 1,76 khớp',
    'Với 10 bit, mỗi bậc 3 phẩy 22 mi li vôn, nhiễu bằng khoảng 3 bậc.':
        'ASR chép “mỗi bật 3,22 mV, nhiễu bằng khoảng 3 bật”: “mi li vôn” → mV đúng đơn vị; bậc/bật lệch âm cuối c/t (ASR đã biết, như “héc/hét”); số 3,22 khớp',
    'Cách sửa là giữ thêm bit cho phần lẻ.':
        'ASR chép “Cách sữa là giữ thêm bích cho phần lẻ”: sửa/sữa nhầm thanh hỏi/ngã, bit → “bích” như probe p1 CSA — NOT_VERIFIED bằng tai người',
    'Khi đó mỗi bit dài khoảng 0 phẩy 104 mi li giây.':
        'ASR chép “khi đó mỗi biết dài khoảng 0,104 ms”: “0 phẩy 104 mi li giây” → “0,104 ms” đúng số và đơn vị viết tắt; bit → “biết” như probe p1 CSA',
    'Lỗi thứ hai, dùng điện trở 10 ki-lô-ôm cho dây dài ở bốn trăm ki-lô-héc.':
        'ASR chép “10 kOhm … 400 kHz”: đúng đơn vị viết tắt và số',
    'Với 200 pi-cô-pha-ra, ngay cả chế độ một trăm ki-lô-héc cũng chỉ cho tới khoảng 5 phẩy 9 ki-lô-ôm, cạnh lên quá chậm và bit bị đọc sai.':
        'ASR chép “200 picofara … 100 kHz … 5,9 kOhm … biết bị đọc sa…”: đơn vị và số đúng; bit → “biết” như probe p1 CSA',
    'Ta chọn trong khoảng 1 tới 1 phẩy 8 ki-lô-ôm, ví dụ 1 phẩy 5 ki-lô-ôm.':
        'ASR chép “1 tới 1,8 kg, ví dụ 1,5 kg”: số khớp; cùng cách viết “ki-lô-ôm” ở khung 22 và 23 được chép “kOhm”, nên đây là ASR đoán đơn vị “ki lô” quen hơn — NOT_VERIFIED bằng tai người',
    'Câu hai, chế độ bốn trăm ki-lô-héc, dây có điện dung 100 pi-cô-pha-ra, điện trở kéo lên lớn nhất là bao nhiêu?':
        'ASR chép “chế độ 400 kHz, dày có điện dung 100 picofarad”: đúng đơn vị; dây/dày nhầm thanh',
    'Về tốc độ, SPI chạy hàng chục mê-ga-héc và gửi nhận cùng lúc, còn I²C thường chạy một trăm hoặc bốn trăm ki-lô-héc.':
        'ASR chép “SPI … MHz … Y2C … 100 hoặc 400 KHz”: SPI đọc “ét-pi-ai” được chép đúng tên viết tắt SPI; đơn vị đúng; I²C → “Y2C” (i đọc “i”, ASR chọn chữ Y) — tên hiện trên màn hình',
    'Về số dây, SPI cần dây xung nhịp, dây ra, dây vào, cộng thêm một dây chọn chip cho mỗi chip, còn I²C chỉ cần hai dây, dữ liệu và xung nhịp.':
        'ASR chép “FBI cần dây xuân nhịp … E2C”: SPI ở đầu câu dài bị chép “FBI” (cùng vần “bi ai”), cùng cách đọc ở khung 6 và 7 chép đúng “SPI”; xung/xuân nhầm vần — NOT_VERIFIED bằng tai người; tên hiện trên màn hình',
    'Chào bạn, bộ điều khiển phanh phải tính lại sau mỗi 4 mi li giây, màn hình cập nhật mỗi 6 mi li giây, và ghi nhật ký mỗi 12 mi li giây.':
        'ASR chép “Bộ điều khiển fan … mỗi 4 ms … 6 ms … 12 ms”: phanh/“fan” cùng âm đầu ph/f, lệch âm cuối nh/n; đơn vị và số đúng',
    'Độ sử dụng U là tổng các tỉ số C i chia T i.':
        'ASR chép “Độ sử dụng u là tổng các tỷ số c e chi ti”: tên chữ cái đọc kiểu Việt (C i, T i) bị chép nhầm — nhóm đã biết (SKILL Bước 5), công thức hiện trên màn hình; tỉ/tỷ chỉ khác chính tả',
    'Ví dụ hạn là 100 mi li giây, vòng chính dài nhất 60 mi li giây.':
        'ASR chép “100ml … 60ml”: số khớp, “mi li giây” rút thành “ml” (ASR viết tắt nhầm); cùng đơn vị ở các câu khác của bài chép “mili giây”',
    'Làm thử, thức 1 phần trăm thời gian ở 10 mi-li-am-pe, ngủ ở 10 mi-crô-am-pe, tức 0 phẩy 01 mi-li-am-pe.':
        'ASR chép cả hai đơn vị thành “mA”; cùng cách viết “mi-crô-am-pe” ở khung 17, 18, 20, 26 chép “microamper/microampe/µA”, nên TTS đọc ổn định, ASR chuẩn hoá nhầm; “phẩy” → “phải” đã biết; số khớp — NOT_VERIFIED bằng tai người',
    'Lỗi thứ nhất, bỏ qua dòng ngủ vì chỉ vài chục mi-crô-am-pe.':
        'ASR chép “dòng ngũ vị chỉ vài chục microamper”: đúng đơn vị; ngủ vì/ngũ vị nhầm thanh',
    'Bây giờ đến lượt bạn tự làm, thiết bị thức 0 phẩy 1 phần trăm ở 20 mi-li-am-pe, ngủ ở 5 mi-crô-am-pe, pin một nghìn mi-li-am-pe giờ.':
        'ASR chép “0,1% ở 20 mA, ngủ ở 5 µA, thin 1000 mA giờ”: đơn vị và số đúng; pin/“thin” lệch âm đầu — NOT_VERIFIED bằng tai người',
    'Dòng trung bình bằng 0 phẩy 1099 mi-li-am-pe.':
        'ASR chép “bằng không phải 1.099 mili ampere”: đúng đơn vị; “phẩy” → “phải” đã biết ở mọi khoá',
    'Ngủ ở 100 mi-crô-am-pe thay vì 10, dòng trung bình thành 0 phẩy 199 mi-li-am-pe, và tuổi thọ tụt từ 379 xuống 209 ngày.':
        'ASR chép “100 microampe thấy vì 10 … 0,199 miliampe … 379 xuống 209 ngày”: đơn vị và mọi số đúng; thay/thấy nhầm thanh',
    'Đèn báo nguồn, bộ ổn áp, cảm biến không được tắt, mỗi thứ tốn vài chục tới vài trăm mi-crô-am-pe, cộng thẳng vào dòng ngủ.':
        'ASR chép “Đen báo nguồn … vài trăm microamper”: đúng đơn vị; đèn/đen nhầm thanh',
    # ── DBS L06–L07 (2026-10-30) ──
    'Câu hai, bảng nhà xuất bản, bảng sách có khoá ngoại tới nhà xuất bản, bảng bạn đọc, và bảng mượn làm bảng nối.':
        'ASR chép “bản nhà xuất bản, bản sách … bản bản đọc … bản nối”: bảng/bản lệch thanh hỏi/sắc-ngang ở mọi lần (ASR đã biết, cùng mẫu các câu “bảng” khác của bài chép đúng); bạn/bản lệch thanh — NOT_VERIFIED bằng tai người; tên bảng hiện trên màn hình',
    'Khoá chính của bảng mượn gồm mã bạn đọc, mã sách và ngày mượn.':
        'ASR chép “Khóa chính của bản mượn gồm mã bản đọc, mã sách và ngay mượn”: bảng/bản, bạn/bản, ngày/ngay chỉ lệch thanh; ba cột khoá hiện trên màn hình — NOT_VERIFIED bằng tai người',
    'Còn đọc ngẫu nhiên mỗi trang mất khoảng 8 mi li giây.':
        'ASR chép “còn độc nỗ nhiên mũi trang mất khoảng 8 mili giây”: cụm “đọc ngẫu nhiên” bị chép lệch cả ở khung 18 (“độc nẫu nhiên”) nhưng đúng ở các câu khác của bài; số 8 và đơn vị đúng — NOT_VERIFIED bằng tai người',
    'Lỗi thứ hai, nghĩ dòng rộng cũng không sao.':
        'ASR chép “Lội thứ hai, nghĩ dòng dòng cũng không sao”: lỗi/lội nhầm thanh (đã biết); rộng → “dòng” lặp từ đứng trước — NOT_VERIFIED bằng tai người; ý “dòng rộng” nói lại ngay ở câu sau (400 byte mỗi dòng)',
    'Với ổ thể rắn, đọc ngẫu nhiên khoảng 0 phẩy 1 mi li giây, mười nghìn trang chỉ khoảng 1 giây.':
        'ASR chép “độc nẫu nhiên khoảng 0,1 mili dây, 10.000 trang chỉ khoảng 1 dây”: số và đơn vị đúng; giây/dây (gi/d) đã biết; “đọc ngẫu” lệch như khung 16',
    # ── RBM L00, L11 dựng lại (2026-10-30) ──
    'Vì sao lại đặt hai toạ độ này thành các cột của ma trận?':
        'ASR chép “Vì sao lại đặt hai tỏa độ này thành các cục của ma trẩn?”: toạ/tỏa, trận/trẩn lệch thanh; cột → “cục” lệch vần — các câu khác của bài có “cột của ma trận” chép đúng — NOT_VERIFIED bằng tai người',
    'Với bước h bằng 0 phẩy 05, hệ số bằng 0 phẩy 5, nên dãy hội tụ êm.':
        'ASR chép “bước hát bằng 0.005, hệ số bằng 0.005 … hội tụi em”: ASR chuẩn hoá “không phẩy …” thành số theo kiểu riêng (cả hai số bị viết 0.005), h đọc tên chữ cái “hát”; hai số 0,05 và 0,5 hiện trên màn hình — NOT_VERIFIED bằng tai người',
    'Lệch tích lũy tới giữa bit dừng phải dưới nửa bit, nên tổng lệch hai bên phải dưới khoảng 5 phẩy 3 phần trăm, thực hành giữ mỗi bên dưới 2 phần trăm.':
        'ASR chép “Lịch tích lũy tới giữ biết dừng phải dưới nữ biết … 5,3% … dưới 2%”: lệch/lịch, nửa/nữ lệch vần–thanh, bit → “biết” như probe p1 CSA; hai con số 5,3% và 2% chép đúng — NOT_VERIFIED bằng tai người (câu đổi chữ “luỹ” → “lũy” theo E38, nội dung giữ nguyên)',
    # ── PLC L00–L05 (2026-10-30) ──
    'Lỗi thứ nhất, nói một ngôn ngữ là ngôn ngữ thông dịch.':
        'ASR chép “Lội thứ nhất, nói một ngu ngữ là ngu ngữ thông dịch”: lỗi/lội nhầm thanh (đã biết); “ngôn” → “ngu” ở cả hai lần — cụm “ngôn ngữ” ở các câu khác của bài chép đúng — NOT_VERIFIED bằng tai người',
    'Dấu hai chấm hai chấm bằng đọc là gồm, gạch đứng là hoặc, còn ngoặc kèm dấu sao là lặp lại không hay nhiều lần.':
        'ASR chép “Dấu 2.2. bàn đọc là gồm, gạt đứng là hoặc … dấu sau là lập lại”: ASR đổi “hai chấm hai chấm” thành chữ số, bằng/bàn, gạch/gạt, sao/sau lệch thanh–âm cuối; ký hiệu ::= | ( )* hiện trên màn hình — NOT_VERIFIED bằng tai người',
    'Lỗi thứ nhất, nghĩ phạm vi tĩnh nhớ giá trị lúc định nghĩa.':
        'ASR chép “nghỉ phạm vì tỉnh nhớ giá trị lúc định nghĩa”: nghĩ/nghỉ, vi/vì, tĩnh/tỉnh chỉ lệch thanh; cụm “phạm vi tĩnh” ở các câu khác của bài chép đúng — NOT_VERIFIED bằng tai người',
    'Phép tối ưu thứ nhất là gấp hằng số.':
        'ASR chép “Phép tối yêu thứ nhất là gấp hàng số”: ưu → “yêu” (cùng vần), hằng/hàng lệch thanh; cụm “gấp hằng số” ở các câu khác của bài chép đúng — NOT_VERIFIED bằng tai người',
    # ── SWF L00–L12 (2026-10-30) ──
    'Mệnh đề đó đúng trước mọi vòng, nhưng khi dừng không suy ra được s bằng tổng, nên bất biến phải đủ mạnh cho bước kết thúc.':
        'ASR chép “không suy ra được ác bàn tổng”: tên chữ cái s đọc kiểu Việt “ét” bị nghe thành “ác”, bằng/bàn lệch thanh; phần còn lại của câu chép đúng nguyên văn (0,926) — NOT_VERIFIED bằng tai người',
    'Lỗi thứ nhất, chọn bất biến đúng nhưng quá yếu, như s không âm.':
        'ASR chép “như F không âm”: tên chữ cái s (“ét”) bị nghe thành “ép”; câu còn lại chép đúng, ký hiệu s ≥ 0 hiện trên màn hình — NOT_VERIFIED bằng tai người',
    'Hàm biến thiên V là một số nguyên tính từ các biến của vòng lặp, thoả hai điều.':
        'ASR chép “Hàm biến thiên với là … vòng lập”: tên chữ cái V đọc kiểu Việt “vê” bị nghe thành “với”, lặp/lập lệch thanh (đã biết); ký hiệu V hiện trên màn hình — NOT_VERIFIED bằng tai người',
    'V giảm thật sự vì phần dư khi chia cho b luôn nhỏ hơn b.':
        'ASR chép “Với giảm thật sự … chia cho bê luôn nhỏ hơn bê”: V (“vê”) nghe thành “với”; b chép thành “bê” đúng cách đọc tên chữ cái — NOT_VERIFIED bằng tai người',
    'Câu hai, b đi 35, 30, 5, 0, ước chung lớn nhất là 5.':
        'ASR chép “Câu 2, về đi 35, 30, 5, 0”: tên chữ cái b (“bê”) nghe thành “về”; mọi con số chép đúng — NOT_VERIFIED bằng tai người',
    'Thử với 252 và 105, b đi qua 105, 42, 21 rồi 0.':
        'ASR chép “bề đi qua 105, 42, 21 rồi không?”: tên chữ cái b (“bê”) nghe thành “bề”, số 0 chép thành chữ “không”; mọi con số chép đúng — NOT_VERIFIED bằng tai người',
    'Một hàm trả khoảng đóng, hàm khác lại nhận nửa mở, và ở ranh giới sẽ lệch một.':
        'ASR chép “Một ham trả khoảng đóng, ham khác … ở tranh dưới sẽ lệch mục”: hàm/ham lệch thanh, ranh giới → “tranh dưới” (r/tr, gi/d), một/mục lệch âm cuối; độ khớp 0,722 trên câu 18 từ, ý câu vẫn đọc ra được — NOT_VERIFIED bằng tai người',
    'Có hai kiểu khoảng.':
        'ASR chép “Có 2 kiểu khoảnh”: khoảng/khoảnh lệch âm cuối ng/nh; ngay sau câu này màn hình hiện hai kiểu khoảng [a, b] và [a, b), chữ “khoảng” ở các câu khác chép đúng — NOT_VERIFIED bằng tai người',
    'Lỗi thứ hai, dùng chính mã đang kiểm làm trọng tài.':
        'ASR chép “Lội thứ hai, dùng chín mã đang kiểm làm trọng tay”: lỗi/lội lệch thanh (đã biết ở PLC), chính/chín lệch âm cuối, tài/tay lệch vần; câu 10 từ khớp 0,727 — NOT_VERIFIED bằng tai người',
    'Lỗi thứ ba, rải logic chuyển trạng thái khắp nơi.':
        'ASR chép “Lội thứ 3, rãi lô kích chuyển trạng thái khắp nơi”: lỗi/lội, rải/rãi lệch thanh; “logic” qua lexicon đọc “lô gíc” và ASR viết “lô kích” — NOT_VERIFIED bằng tai người',
    'Như ô-tô-mát ở khoá Lý thuyết tính toán, máy trạng thái gồm tập trạng thái, trạng thái đầu, và bảng chuyển.':
        'ASR chép “như Automat ở khóa lý thuyết tính toán … bản chuyển”: ASR viết “ô tô mát” thành “Automat”, đúng từ được nói; bảng/bản lệch âm cuối — NOT_VERIFIED bằng tai người',
    'Nếu luồng 2 lấy A, C, B thì sao?':
        'ASR chép “Nếu lùng 2 lấy A, C, B thì 6”: luồng/lùng lệch vần, “sao” cuối câu hỏi bị nghe thành số “sáu”; thứ tự A, C, B chép đúng — NOT_VERIFIED bằng tai người',
    'Khoảng 95 phần trăm là d ngang cộng trừ 2 phẩy 045 nhân sai số chuẩn, với n bằng 30.':
        'ASR chép “Khoảng 95% là gian ngang cộng trừ 2,045 nhân sai số chuẩn với n bằng 30”: tên chữ cái d (“đê”) nghe thành “gian”; 2,045 chép đúng giá trị (cột khác biệt đọc lại thành chữ “nghìn không trăm” là do chuẩn hoá số của bộ so) — NOT_VERIFIED bằng tai người',
    'Với bộ thứ i, gọi d i là thời gian của A trừ thời gian của B, dương nghĩa là B nhanh hơn.':
        'ASR chép “Với bộ thứ Y, gọi dY là thời gian của A trừ thời gian của B”: “d i” đọc liền được ASR viết “dY”, i đọc tên chữ cái “i” viết thành “Y”; ký hiệu dᵢ hiện trên màn hình — NOT_VERIFIED bằng tai người',
    'Lỗi thứ ba, để nhánh sống quá lâu rồi mới gộp.':
        'ASR chép “Lội thứ 3, để nhắn sống quá lâu rồi mới gục”: lỗi/lội lệch thanh (đã biết), nhánh/nhắn lệch vần, gộp/gục lệch vần; câu 10 từ khớp 0,727 — NOT_VERIFIED bằng tai người',
    'Chép chuỗi 9 ký tự cộng ký tự kết thúc mà không kiểm độ dài làm tràn 2 byte, byte cờ thành mã của chữ B, bằng 66, khác 0, và người dùng thành quản trị.':
        'ASR chép “Chép chủ chính ký từ cọng ký từ … tràn hai bay, bay cờ … chữ B bằng 66”: chuỗi/chủ, chín/chính lệch âm cuối, tự/từ lệch thanh; “byte” đọc thô và ASR viết “bay” đúng như probe CSA p1 (8/8); các số 2, 66, 0 chép đúng — NOT_VERIFIED bằng tai người',
    'Với tràn bộ đệm, xét mô hình một mảng 8 ký tự nằm ngay trước một byte cờ quản trị bằng 0.':
        'ASR chép “Với trang bộ đềm, xếp mô hình … một bay cờ quản trị bằng không”: tràn/trang lệch âm cuối, đệm/đềm, xét/xếp lệch thanh–âm cuối, “byte” viết “bay” như probe CSA p1 (8/8) — NOT_VERIFIED bằng tai người',
    'Hãy dùng hàm chép có giới hạn, luôn chừa chỗ cho ký tự kết thúc, khi đó chuỗi 9 ký tự bị cắt còn 7, và byte cờ vẫn là 0.':
        'ASR chép “khi đó chủ chính ký tự bị cắt còn bảy và bay cờ vẫn là không”: chuỗi chín → “chủ chính” như câu khung 12, “byte” viết “bay” như probe CSA p1 (8/8); số 7 và 0 chép đúng — NOT_VERIFIED bằng tai người',
    'Câu hai, 12 cộng 1 trừ 8, tràn 5 byte.':
        'ASR chép “Câu 2, 12 cộng 1 trừ 8 tràn 5 bay”: chỉ “byte” viết thành “bay”, đúng như probe CSA p1 (8/8); mọi con số chép đúng — NOT_VERIFIED bằng tai người',
    'Câu hai, chép chuỗi 12 ký tự cộng ký tự kết thúc vào mảng 8 ký tự mà không kiểm độ dài, thì tràn bao nhiêu byte?':
        'ASR chép nguyên văn trừ “byte” → “bay”, đúng như probe CSA p1 (8/8); độ khớp 0,964 — NOT_VERIFIED bằng tai người',
    # ── DSY L00–L14 (2026-10-30) ──
    'Phần tuần tự giới hạn tăng tốc theo định luật Amdahl, và thêm máy còn thêm chi phí phối hợp.':
        'ASR chép “theo định luật am đang”: Amdahl đọc “Am-đan” theo lexicon (probe CSA p1 8/8), đan/đang lệch âm cuối; phần còn lại chép đúng (0,952) — NOT_VERIFIED bằng tai người',
    'Theo định luật Amdahl ở khoá Hệ thống máy tính, nếu 90 phần trăm công việc song song được và dùng 10 máy, tăng tốc chỉ khoảng 5 phẩy 26 lần.':
        'ASR chép “Theo định luật Amdang … 5,26 lần”: Amdahl đọc “Am-đan” theo lexicon, ASR viết liền “Amdang”; mọi con số (90%, 10, 5,26) chép đúng — NOT_VERIFIED bằng tai người',
    'Đồng hồ của máy B chạy chậm 5 mi li giây, thông điệp tới sau 3 mi li giây, nên B ghi là nhận lúc 98 mi li giây.':
        'ASR chép “5 mili giây … 3 mili giây, nên BG là nhận lúc 98 mili giây”: “mi li” được viết liền “mili” (đúng từ), “B ghi” bị viết dính thành “BG”; các số 5, 3, 98 chép đúng — NOT_VERIFIED bằng tai người',
    'Hôm nay ta học các kiểu hỏng hóc, và cách xếp thứ tự sự kiện mà không cần đồng hồ chung, với đồng hồ lô-gic của Lamport.':
        'ASR chép “hỏng hốc … các xếp thứ tự … đồng hồ logic của Lampa”: hóc/hốc, cách/các lệch thanh–âm cuối, “lô-gic” viết “logic” (đúng từ), Lamport đọc “Lam-po” theo lexicon (probe DSY p1 8/8) nhưng câu này chép “Lampa” — NOT_VERIFIED bằng tai người',
    'Câu hai, P2 đã có 7 sự kiện với nhãn tới 7, rồi nhận một thông điệp mang nhãn 1.':
        'ASR chép “T2 đã có 7 sự kiện”: tên chữ cái P (“pê”) nghe thành “tê”; mọi con số chép đúng, P2 hiện trên màn hình — NOT_VERIFIED bằng tai người',
    'Câu một, P1 có hai sự kiện cục bộ rồi gửi m, P2 nhận m ở sự kiện đầu tiên rồi có một sự kiện cục bộ.':
        'ASR chép “P1 có 2 sự kiện … T2 nhận m”: P1 chép đúng, P2 (“pê hai”) nghe thành “T2”; phần còn lại đúng (0,966) — NOT_VERIFIED bằng tai người',
    'Nhãn Lamport ở bài 1 luôn xếp được một bản là sau, nhưng có thể cả hai được ghi độc lập, không bên nào thấy bên kia.':
        'ASR chép “Nhãng lampo ở bài 1”: Lamport đọc “Lam-po” theo lexicon và ASR chép “lampo” đúng như probe DSY p1; nhãn/nhãng lệch âm cuối — NOT_VERIFIED bằng tai người',
    'Sự kiện 0, 1, 0 có nhãn Lamport 1, nhỏ hơn nhãn 2 của sự kiện 2, 0, 1, nhưng hai vector không so được với nhau, nên hai sự kiện đồng thời.':
        'ASR chép “Sự kiện 0, 1, không có nhãn lamppor 1”: Lamport (“Lam-po”) viết “lamppor”, số 0 cuối bộ ba viết thành chữ “không”; các vector hiện trên màn hình — NOT_VERIFIED bằng tai người',
    'Tổng quát, ghi chịu được N trừ W máy hỏng, đọc chịu được N trừ R máy hỏng.':
        'ASR chép “Tổng quắc, ghi chịu được N-V đúc máy hỏng”: W đọc tên chữ cái “vê đúp” (ASR viết “V đúc”) như mọi câu có W của bài; “trừ” bị ASR đổi thành dấu “-”; quát/quắc lệch thanh — NOT_VERIFIED bằng tai người',
    'Luôn gặp đúng khi R cộng W lớn hơn N.':
        'ASR chép “R cộng với đút lớn hơn N”: W đọc tên chữ cái “vê đúp”, ASR viết “với đút”; R, N chép đúng, công thức R + W > N hiện trên màn hình — NOT_VERIFIED bằng tai người',
    'Hàng R bằng 1 chỉ luôn gặp khi W bằng 3.':
        'ASR chép “khi V đúc bằng ba”: W đọc “vê đúp” (tên chữ cái), các số chép đúng — NOT_VERIFIED bằng tai người',
    'Với đại biểu N, R, W, nếu R cộng W lớn hơn N thì đọc luôn gặp ghi, và ghi chịu được N trừ W, đọc chịu được N trừ R máy hỏng.':
        'ASR chép “N, R, V-đúc … R cộng V-đúc … N trừ V-đúc”: cả ba lần W đọc tên chữ cái “vê đúp”; phần còn lại chép đúng — NOT_VERIFIED bằng tai người',
    'Hàng R bằng 2 luôn gặp khi W từ 2 trở lên.':
        'ASR chép “khi V-đút từ 2 trở lên”: W đọc “vê đúp” (tên chữ cái), các số chép đúng — NOT_VERIFIED bằng tai người',
    'Lỗi thứ hai, nghĩ R cộng W lớn hơn N là giải quyết mọi chuyện.':
        'ASR chép “nghĩ R cộng V đúc lớn hơn N”: W đọc “vê đúp” (tên chữ cái); câu còn lại chép đúng — NOT_VERIFIED bằng tai người',
    'Với N bằng 5, có thể chọn cân bằng, R và W đều bằng 3, khi đó cả đọc lẫn ghi chịu được 2 máy hỏng.':
        'ASR chép “R và V đút đều bằng 3 … cả độc lẫn ghi”: W đọc “vê đúp”, đọc/độc lệch thanh; các số chép đúng — NOT_VERIFIED bằng tai người',
    'Cách thứ ba là đại biểu, có N bản sao, ghi xong khi W bản xác nhận.':
        'ASR chép “ghi xong khi về đúc bản xác nhận”: W đọc “vê đúp” (tên chữ cái), ASR viết “về đúc” — NOT_VERIFIED bằng tai người',
    'N bằng 4 với R và W bằng 3 vẫn chỉ chịu được 1 máy hỏng, giống N bằng 3 với R và W bằng 2, nên máy thứ tư chỉ thêm chi phí.':
        'ASR chép “R và V đút bằng 3 … R và V đút bằng 2”: W đọc “vê đúp” cả hai lần; các số chép đúng — NOT_VERIFIED bằng tai người',
    'Câu hai, với R bằng 2 và W bằng 4, ghi chịu được mấy máy hỏng, đọc chịu được mấy?':
        'ASR chép “R bằng 2 và V đúc bằng 4”: W đọc “vê đúp” (tên chữ cái); câu còn lại đúng — NOT_VERIFIED bằng tai người',
    'Câu một, trong ba cặp R và W là 2 và 3, 2 và 4, 3 và 3, cặp nào bảo đảm đọc thấy bản mới nhất?':
        'ASR chép “trong 3 cặp R và V đúc là 2 và 3, 2 và 4, 3 và 3”: W đọc “vê đúp”; mọi cặp số chép đúng — NOT_VERIFIED bằng tai người',
    'Hoặc chọn đọc nhanh, R bằng 1 và W bằng 5, đọc chịu được 4 máy hỏng nhưng ghi không chịu được máy hỏng nào, chỉ một máy hỏng là không ghi được.':
        'ASR chép “R bằng 1 và V đút bằng 5”: W đọc “vê đúp” (tên chữ cái); câu còn lại đúng (0,955) — NOT_VERIFIED bằng tai người',
    'Hàm ánh xạ và rút gọn phải là hàm thuần, như khoá Ngôn ngữ lập trình.':
        'ASR chép “Hàm ánh xạ và trúc gòn phải là hàm thương như khóa ngôn ngữ lập trinh”: rút gọn → “trúc gòn” (r/tr, lệch thanh), thuần/thương lệch vần, trình/trinh lệch thanh; câu 14 từ khớp 0,75 — NOT_VERIFIED bằng tai người',
    'Bây giờ đến lượt bạn tự làm với hai dòng, x y x và y y z.':
        'ASR chép “x, y, x và y, z”: chữ y thứ hai của dòng “y y z” bị gộp khi hai tên chữ cái “i” liền nhau; hai dòng dữ liệu hiện trên màn hình — NOT_VERIFIED bằng tai người',
    'Một tỉ địa chỉ, mỗi địa chỉ khoảng 50 byte, tổng cộng 50 ghi-ga-byte, không vừa bộ nhớ một máy.':
        'ASR chép “Một tỷ địa chỉ … 50by, tổng cộng 50GB”: tỉ/tỷ chỉ khác chính tả, “ghi-ga-byte” được ASR viết tắt “GB” (đúng đơn vị); các số chép đúng — NOT_VERIFIED bằng tai người',
    'Câu hai, 100 triệu nhân 8 bit là 100 triệu byte, tức 100 mê-ga-byte.':
        'ASR chép nguyên văn, chỉ viết “mê-ga-byte” thành “megabyte” (đúng từ) — NOT_VERIFIED bằng tai người',
    'Câu hai, 100 triệu phần tử, 8 bit mỗi phần tử, bộ lọc cần bao nhiêu mê-ga-byte?':
        'ASR chép nguyên văn, chỉ viết “mê-ga-byte” thành “megabyte” (đúng từ) — NOT_VERIFIED bằng tai người',
    'Nếu chấp nhận thỉnh thoảng nói nhầm là đã thấy, rồi bỏ qua một trang chưa ghé, thì chỉ cần khoảng 1 phẩy 25 ghi-ga-byte.':
        'ASR chép nguyên văn, chỉ viết “1 phẩy 25 ghi-ga-byte” thành “1,25 GB” (đúng giá trị và đơn vị) — NOT_VERIFIED bằng tai người',
    'Câu hai, lưu theo dòng phải đọc 4 ghi-ga-byte, theo cột chỉ đọc 0 phẩy 8 ghi-ga-byte.':
        'ASR chép “phải đọc 4 GB, theo cục chỉ đọc 0,8 GB”: “ghi-ga-byte” viết tắt “GB” (đúng đơn vị), cột/cục lệch vần (cùng nhầm ở các câu khác của bài); các số 4 và 0,8 chép đúng — NOT_VERIFIED bằng tai người',
    'Lưu theo dòng phải đọc bao nhiêu ghi-ga-byte, theo cột thì bao nhiêu?':
        'ASR chép “bao nhiêu gigabyte, theo cục thì bao nhiêu”: “ghi-ga-byte” viết “gigabyte” (đúng từ), cột/cục lệch vần — NOT_VERIFIED bằng tai người',
    'Chào bạn, một bảng bán hàng có 100 triệu dòng, 8 cột, mỗi ô 8 byte, tổng cộng 6 phẩy 4 ghi-ga-byte.':
        'ASR chép “một bản bán hàng … 8 cục, mỗi ô 8 bay, tổng cộng 6,4 ghi gà bay”: bảng/bản lệch âm cuối, cột/cục lệch vần, byte → “bay” như probe CSA p1 (8/8); các số chép đúng — NOT_VERIFIED bằng tai người',
    'Nhưng nếu đĩa lưu từng dòng liền nhau, ta phải đọc cả 6 phẩy 4 ghi-ga-byte.':
        'ASR chép “Nhưng nếu để lưu từng dòng … 6,4 gigabyte”: đĩa/để lệch vần–thanh, “ghi-ga-byte” viết “gigabyte” (đúng từ); số 6,4 chép đúng — NOT_VERIFIED bằng tai người',
    'Câu hỏi giá trung bình là bao nhiêu chỉ cần cột giá, tức 0 phẩy 8 ghi-ga-byte.':
        'ASR chép nguyên văn, chỉ viết “0 phẩy 8 ghi-ga-byte” thành “0,8 GB” (đúng giá trị và đơn vị) — NOT_VERIFIED bằng tai người',
    'Câu hai, bảng 100 triệu dòng, 10 cột, mỗi ô 4 byte, một truy vấn cần 2 cột.':
        'ASR chép nguyên văn trừ “byte” → “bay”, đúng như probe CSA p1 (8/8) — NOT_VERIFIED bằng tai người',
    'Trong lúc chờ, A giữ khoá trên dòng tài khoản, mọi giao dịch khác chạm dòng đó cũng bị chặn.':
        'ASR chép “ai giữ khóa trên dòng tai khoảng”: tên chữ cái A (“a”) nghe thành “ai”, tài/tai lệch thanh, khoản/khoảng lệch âm cuối — NOT_VERIFIED bằng tai người',
    # ── DSC L00–L14 (2026-10-30) ──
    'Rào Tukey đi từ Q1 trừ 1 phẩy 5 lần khoảng tứ phân vị, tới Q3 cộng 1 phẩy 5 lần, tức từ âm 1 tới 7.':
        'ASR chép “Rào tu kỳ đi từ quy mục trừ 1,5 lần … tới quy 3 cộng 1,5 lần, thức từ âm 1 tới 7”: Tukey đọc theo lexicon và ASR viết “tu kỳ”, Q đọc tên chữ cái “quy”, “một” → “mục”, tức/thức; các số 1,5, âm 1, 7 chép đúng — NOT_VERIFIED bằng tai người',
    'Rào Tukey đánh dấu để xem, và với mỗi ngoại lai, hãy hỏi đó là lỗi hay là một phát hiện.':
        'ASR chép “Rào Tuki … mỗi ngoại like”: Tukey được viết “Tuki” (đúng âm), “lai” → “like” do ASR chen từ tiếng Anh; câu còn lại đúng (0,905) — NOT_VERIFIED bằng tai người',
    'Câu hai, với Q1 bằng 5 phẩy 5 và Q3 bằng 8 phẩy 75, rào Tukey là gì?':
        'ASR chép “với quy 1 bằng 5,5 và quy 3 bằng 8,75, rào Tu Ky là gì”: Q đọc tên chữ cái “quy”, Tukey viết “Tu Ky” (đúng âm); các số chép đúng — NOT_VERIFIED bằng tai người',
    'Bên trái, cột B trông cao gấp đôi cột A.':
        'ASR chép “Bên trái, cục B trong cao gấp đôi cục A”: cột/cục lệch vần (cùng nhầm ở nhiều bài DSY, DSC), trông/trong lệch thanh; câu 9 từ khớp 0,7, hai cột A, B hiện trên biểu đồ — NOT_VERIFIED bằng tai người',
    'Lỗi thứ ba, gộp các nhóm khác nhau rồi tính một r.':
        'ASR chép “gục các nhóm … rồi tính một error”: gộp/gục lệch vần, tên chữ cái r (“e-rờ”) được viết “error”; câu còn lại đúng — NOT_VERIFIED bằng tai người',
    'Năm 1973, một nhà thống kê đã dựng bốn bộ dữ liệu có cùng r khoảng 0 phẩy 82 nhưng hình dạng khác hẳn.':
        'ASR chép “có cùng error khoảng 0,82”: tên chữ cái r (“e-rờ”) được viết “error”; năm 1973, số 4 và 0,82 chép đúng (0,969) — NOT_VERIFIED bằng tai người',
    'Hãy hiệu chỉnh mức ý nghĩa, hoặc chọn trước giả thuyết, và luôn nhớ tỉ lệ nền.':
        'ASR chép “Hãy hiểu chính mức ý nghĩa … luôn nhớ tỷ lệ nên”: hiệu chỉnh → “hiểu chính” lệch thanh, tỉ/tỷ chỉ khác chính tả, nền/nên lệch thanh; câu 16 từ khớp 0,765 — NOT_VERIFIED bằng tai người',
    # ── DSC L07 dựng lại (2026-10-30) ──
    'Lỗi thứ ba, chỉ báo tỉ lệ gộp chung của tất cả các nhóm.':
        'ASR chép “Lội thứ Ba chỉ báo tỷ lệ gục chung của tất cả các nhóm”: lỗi/lội lệch thanh (đã biết), tỉ/tỷ chỉ khác chính tả, gộp/gục lệch vần; câu đã viết dài từ bản 7 từ (0,75) — NOT_VERIFIED bằng tai người',
    # ── SDP L00–L16 (2026-10-30) ──
    'Câu kiểm danh sách rỗng là điểm rẽ thứ nhất, vòng lặp là điểm rẽ thứ hai.':
        'ASR chép “Câu kiểm danh sách rộng là điểm rẻ thứ nhất, vòng lập là điểm rẻ thứ 2”: rỗng/rộng, rẽ/rẻ, lặp/lập đều là cặp lệch thanh ngã–nặng/hỏi–ngã mà ASR hay lẫn (lặp/lập đã gặp ở các khoá trước); khung chữ, số và cấu trúc câu khớp đủ — NOT_VERIFIED bằng tai người',
    'Lỗi thứ ba, dựng sẵn điểm mở rộng cho mọi thứ phòng khi cần.':
        'ASR chép “Lội thứ Ba, dựng sản điểm mở rộng cho mọi thứ phòng khí cân”: lỗi/lội lệch thanh (đã biết ở DSC L07), sẵn/sản và khi cần/khí cân lệch thanh; câu 12 từ, phần còn lại khớp — NOT_VERIFIED bằng tai người',
    'Đưa vào một hình vuông thì ra 16.':
        'ASR chép “đưa vào một hình vuông thị tra 16”: “thì ra” bị nối âm thành “thị tra”, mọi từ nội dung (hình vuông, 16) khớp; độ khớp 0,778 — NOT_VERIFIED bằng tai người',
    'Đáp án câu một, A thấy 2 cộng 1 bằng 3.':
        'ASR chép “Đáp án câu 1 à thấy 2 cộng 1 bằng 3”: chữ cái A (tên kiểm thử) đọc “a”, ASR viết thành thán từ “à”; phép tính khớp đủ (0,909) — NOT_VERIFIED bằng tai người',
    'Lớp đổi sang độ C nhận cảm biến cũ và giữ nó bên trong.':
        'ASR chép “Lớp đổi sang độ sẽ nhận…”: chữ C đọc tên chữ cái “xê”, ASR viết thành “sẽ” (tên chữ cái kiểu Việt, như x → “ích”); phần còn lại khớp (0,929) — NOT_VERIFIED bằng tai người',
    # ── CLD L00–L14 (2026-10-30) ──
    'Một vòng khứ hồi mạng trong cùng trung tâm dữ liệu mất khoảng 500 mi-crô giây, tức 500 nghìn na-nô giây.':
        'ASR chép “Một vòng khứ hồi mạng trong cùng trung tâm dữ liệu mất khoảng 500 micro dây, tức 500 nghìn nano dây.” (0.792): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh — NOT_VERIFIED bằng tai người',
    'Câu một, một trang gọi nối tiếp 4 dịch vụ, mỗi vòng khứ hồi 500 mi-crô giây.':
        'ASR chép “Câu 1. Một trang gọi nối tiếp bốn dịch vụ, mỗi vòng khứ hồi 500 micro dây.” (0.865): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh — NOT_VERIFIED bằng tai người',
    'Riêng mạng tốn bao nhiêu mi li giây?':
        'ASR chép “riêng mạng tốn bao nhiêu mì lý dây?” (0.75): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh — NOT_VERIFIED bằng tai người',
    'Đáp án câu một, 4 nhân 500 bằng 2000 mi-crô giây, tức 2 mi li giây.':
        'ASR chép “Đáp án câu 1, 4 nhân 500 bằng 2 nghìn micro dây tức 2 mê ly dây.” (0.757): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh — NOT_VERIFIED bằng tai người',
    'Dựng một máy ảo cho mỗi chương trình thì nặng, mỗi máy ảo cả GB và khởi động hàng chục giây.':
        'ASR chép “Dựng 1 máy ảo cho mỗi chương trình thì nặng, mỗi máy ảo cả GIGABY và khởi động hàng chục dây.” (0.952): GB đọc “ghi-ga-byte” theo lexicon của khoá, ASR viết “gigabyte” — NOT_VERIFIED bằng tai người',
    'Hôm nay ta học container, đóng gói chương trình cùng mọi thứ nó cần, và chạy như một tiến trình được cô lập.':
        'ASR chép “Hôm nay ta học cần tenner, đóng gõi chương trình cùng mọi thứ nó cần và chạy như một tiến trình được cô lập.” (0.894): container đọc thô (probe CLD p1: 5/8, small viết “cần tên nơi”); lệch âm/thanh thuần Việt: gói/gõi — NOT_VERIFIED bằng tai người',
    'Bảng so container với máy ảo theo ba tiêu chí.':
        'ASR chép “Bản so cần Tenner với máy ảo theo 3 tiêu chí.” (0.762): container đọc thô (probe CLD p1: 5/8, small viết “cần tên nơi”); lệch âm/thanh thuần Việt: bảng/bản — NOT_VERIFIED bằng tai người',
    'Về nhân hệ điều hành, container dùng chung nhân của máy chủ, còn mỗi máy ảo có nhân riêng.':
        'ASR chép “Về nhân hệ điều hành cần tên nơi dùng chung nhân của máy chủ còn mỗi máy ảo có nhân riêng.” (0.9): container đọc thô (probe CLD p1: 5/8, small viết “cần tên nơi”) — NOT_VERIFIED bằng tai người',
    'Chạy với quyền quản trị bên trong container, cộng thêm một lỗ hổng nhân, có thể thoát ra máy chủ.':
        'ASR chép “Chạy với quyền quản trị bên trong Canter, cộng thêm một lỗ hổng nhân có thể thoát ra máy chủ.” (0.95): container đọc thô (probe CLD p1: 5/8, small viết “cần tên nơi”) — NOT_VERIFIED bằng tai người',
    'Mỗi container chỉ nên có một tiến trình chính.':
        'ASR chép “Mỗi cân tenner chỉ nên có một tiếng trình chính.” (0.737): container đọc thô (probe CLD p1: 5/8, small viết “cần tên nơi”); lệch âm/thanh thuần Việt: tiến/tiếng — NOT_VERIFIED bằng tai người',
    'Đáp án câu một, không gian tên tiến trình làm nó thấy mình là số 1, còn nhóm kiểm soát giới hạn CPU.':
        'ASR chép “Đáp án câu một, không gian tên tiến trình làm nó thấy mình là số một, còn nhóm kiểm soát giới hạn CPL.” (0.957): CPU đọc thô (probe CLD p1: 7/8) — NOT_VERIFIED bằng tai người',
    'Container không có phép màu, chỉ là các tính năng nhân đã có từ lâu được ghép lại.':
        'ASR chép “Cần Tener không có phép màu, chỉ là các tính năng nhân đã có từ lâu được ghép lại.” (0.919): container đọc thô (probe CLD p1: 5/8, small viết “cần tên nơi”) — NOT_VERIFIED bằng tai người',
    'Ở bài sau, bài 2, ta học cách dựng ảnh container tái lập, với các lớp, bộ nhớ đệm khi dựng, và ghim phiên bản.':
        'ASR chép “Ở bài sau, bài 2, ta học cách dựng ảnh cần tenor tái lập với các lớp, bộ nhớ đệm khí dựng và game phiên bản.” (0.863): container đọc thô (probe CLD p1: 5/8, small viết “cần tên nơi”); lệch âm/thanh thuần Việt: khi/khí, ghim/game — NOT_VERIFIED bằng tai người',
    'Hôm nay ta học về ảnh container, dựng nhanh nhờ bộ nhớ đệm, và tái lập được, tức cùng đầu vào thì cùng kết quả.':
        'ASR chép “Hôm nay ta học về ảnh cần tenner, dựng nhanh nhờ bộ nhớ đệm và tái lập được, tức cùng đầu vào thì cùng kết quả.” (0.941): container đọc thô (probe CLD p1: 5/8, small viết “cần tên nơi”) — NOT_VERIFIED bằng tai người',
    'Pod là đơn vị chạy nhỏ nhất, gồm một hoặc vài container chung mạng, chung ổ đĩa, và có thể bị xoá rồi tạo lại bất cứ lúc nào.':
        'ASR chép “Phúc là đơn vị chạy nhỏ nhất, gồm một hoặc vài cân tê nơi chung mạng, chung ổ đĩa và có thể bị xóa rồi tạo lại bất cứ lúc nào.” (0.9): Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút); container đọc thô (probe CLD p1: 5/8, small viết “cần tên nơi”) — NOT_VERIFIED bằng tai người',
    'đối tượng triển khai khai báo muốn có n bản Pod từ một ảnh, và lo việc tạo lại, cập nhật.':
        'ASR chép “Đối tượng triển khai khai báo muốn có n bản phúc từ một ảnh và lo việc tạo lại, cập nhật.” (0.952): Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút) — NOT_VERIFIED bằng tai người',
    'đối tượng dịch vụ là một địa chỉ ổn định trỏ tới các Pod đang sống, dù Pod đổi liên tục.':
        'ASR chép “Đối tượng dịch vụ là một địa chỉ ổn định trọa tới các phút đang sống, dù phút đổi liên tục.” (0.857): Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút); lệch âm/thanh thuần Việt: trỏ/troạ — NOT_VERIFIED bằng tai người',
    'Đây là khai báo chứ không ra lệnh, ta không viết tạo thêm một Pod, mà viết muốn có 3 Pod.':
        'ASR chép “Đây là khai báo chứ không ra lệnh, ta không viết tạo thêm 1 phút mà viết muốn có 3 phút.” (0.905): Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút) — NOT_VERIFIED bằng tai người',
    'Bảng ghi ba nhịp của vòng với mong muốn là 3 Pod.':
        'ASR chép “Bảng ghi ba nhịp của vòng với mong muốn là ba pút.” (0.917): Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút) — NOT_VERIFIED bằng tai người',
    'Nhịp một, một Pod chết, thực tế còn 2, khác 3, nên bộ điều khiển tạo thêm 1.':
        'ASR chép “Nhịp 1, 1 phút chết, thực tế còn 2, khác 3, nên bộ điều khiển tạo thêm 1.” (0.944): Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút) — NOT_VERIFIED bằng tai người',
    'Nhịp ba, một máy chết làm mất 2 Pod, bộ điều khiển tạo thêm 2 và đưa về 3.':
        'ASR chép “Nhịp 3, một máy chất làm mất 2 pút, bộ điều khiển tạo thêm 2 và đưa về 3.” (0.895): Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút); lệch âm/thanh thuần Việt: chết/chất — NOT_VERIFIED bằng tai người',
    'Lỗi thứ nhất, lưu dữ liệu quan trọng trong hệ tệp của Pod.':
        'ASR chép “Lội thứ nhất, lưu dữ liệu quan trọng trong hệ tệp cuộc phút.” (0.769): Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút); lệch âm/thanh thuần Việt: lỗi/lội — NOT_VERIFIED bằng tai người',
    'Pod bị xoá và tạo lại là chuyện thường ngày, và Pod mới có hệ tệp mới.':
        'ASR chép “Phúc bị xóa và tạo lại là chuyện thương ngay và Phúc mới có hệ tệp mới.” (0.765): Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút); lệch âm/thanh thuần Việt: thường ngày/thương ngay — NOT_VERIFIED bằng tai người',
    'Xoá bớt một Pod cho nhẹ thì bộ điều khiển tạo lại ngay, vì mong muốn vẫn là 3.':
        'ASR chép “Xóa bớt 1 phút cho nhẹ thì bộ điều khiển tạo lại ngay vì mong muốn vẫn là ba.” (0.947): Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút) — NOT_VERIFIED bằng tai người',
    'Lỗi thứ ba, gọi thẳng địa chỉ của một Pod.':
        'ASR chép “Lỗi thứ ba, gọi thẳng địa chỉ của 1 phút.” (0.9): Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút) — NOT_VERIFIED bằng tai người',
    'Pod tạo lại sẽ có địa chỉ mới, nên luôn gọi qua đối tượng dịch vụ, một địa chỉ ổn định tự trỏ tới các Pod đang sống.':
        'ASR chép “Phốt tạo lại sẽ có địa chỉ mới, nên luôn gọi qua đối tượng dịch vụ, một địa chỉ ổn định từ trỏ tới các phốt đang sống.” (0.893): Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút); lệch âm/thanh thuần Việt: tự/từ — NOT_VERIFIED bằng tai người',
    'Bây giờ đến lượt bạn tự làm, đối tượng triển khai muốn 5 Pod.':
        'ASR chép “Bây giờ đến lượt bạn tự làm, đối tượng triển khai muốn 5 phút.” (0.929): Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút) — NOT_VERIFIED bằng tai người',
    'Nhịp một có 2 Pod chết, nhịp hai không có gì, nhịp ba có 1 Pod chết.':
        'ASR chép “Nhịp 1 có 2 phút chết, nhịp 2 không có gì, nhịp 3 có 1 phút chết.” (0.882): Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút) — NOT_VERIFIED bằng tai người',
    'Câu một, ở mỗi nhịp, bộ điều khiển thấy bao nhiêu Pod và tạo thêm bao nhiêu?':
        'ASR chép “Câu 1. Ở mỗi nhịp, bộ điều khiển thấy bao nhiêu pốt và tạo thêm bao nhiêu?” (0.941): Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút) — NOT_VERIFIED bằng tai người',
    'Câu hai, bạn xoá tay 1 Pod khi đang đủ 5, chuyện gì xảy ra?':
        'ASR chép “Câu 2, bạn xóa tay một phút khi đang đủ năm, chuyện gì xảy ra?” (0.933): Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút) — NOT_VERIFIED bằng tai người',
    'Câu hai, bộ điều khiển thấy 4 khác 5 nên tạo lại 1 Pod ngay, muốn 4 thì phải sửa khai báo thành 4.':
        'ASR chép “Câu 2, bộ điều khiển thấy 4 khác 5 nên tạo lại 1 phút ngay, muốn 4 thì phải sửa khai báo thành 4.” (0.958): Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút) — NOT_VERIFIED bằng tai người',
    'Pod là tạm thời, đối tượng dịch vụ là ổn định, và muốn đổi thì đổi khai báo, không sửa tay.':
        'ASR chép “Pope là tạm thời, đối tượng dịch vụ là ổn định, và muốn đổi thì đổi khai báo, không sửa tay.” (0.952): Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút) — NOT_VERIFIED bằng tai người',
    'Ở bài sau, bài 6, ta học cách xếp lịch Pod, với yêu cầu, giới hạn tài nguyên, và bài toán xếp thùng.':
        'ASR chép “Ở bài sau, bài 6, ta học cách xếp lịch bốc với yêu cầu giới hạn tài nguyên và bài toán xếp thùng.” (0.957): Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút) — NOT_VERIFIED bằng tai người',
    'Vậy mà Pod mới cứ nằm chờ vì không đủ tài nguyên.':
        'ASR chép “Vậy mà Phúc mới cứ nằm chờ vì không đủ tài nguyên.” (0.917): Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút) — NOT_VERIFIED bằng tai người',
    'Phần trống bị chia vụn trên nhiều nút, và không nút nào đủ chỗ cho một Pod.':
        'ASR chép “Phần trống bị chia vụn trên nhiều nút và không nút nào đủ chỗ cho một pút.” (0.941): Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút) — NOT_VERIFIED bằng tai người',
    'Hôm nay ta học xếp lịch Pod, với yêu cầu, giới hạn, và bài toán xếp thùng.':
        'ASR chép “Hôm nay ta học xếp lịch bốc với yêu cầu, giới hạn và bài toán xếp thung.” (0.882): Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút); lệch âm/thanh thuần Việt: thùng/thung — NOT_VERIFIED bằng tai người',
    'Yêu cầu được bộ xếp lịch dùng, nó chỉ đặt Pod lên nút còn đủ tổng yêu cầu, còn giới hạn được nhân hệ điều hành áp lúc chạy.':
        'ASR chép “Yêu cầu được bộ xếp lịch dùng, nó chỉ đặt phút lên nút còn đủ tổng yêu cầu, còn giới hạn được nhân hệ điều hành áp lúc chạy.” (0.966): Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút) — NOT_VERIFIED bằng tai người',
    'Hình vẽ một nút có 4 CPU, mỗi Pod yêu cầu 1 phẩy 5 CPU.':
        'ASR chép “Hình vẽ một nút có 4 CPU, mỗi bốc yêu cầu 1.5 CPU.” (0.897): Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút); “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải” — NOT_VERIFIED bằng tai người',
    'Số Pod vừa là phần nguyên của 4 chia 1 phẩy 5, bằng 2.':
        'ASR chép “số 4 vừa là phần nguyên của 4 chia 1,5 bằng 2.” (0.929): Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút) — NOT_VERIFIED bằng tai người',
    'Hai Pod dùng 3 CPU, thừa 1 CPU, không đủ cho Pod thứ ba.':
        'ASR chép “Hai pốt dùng 3 CPU thừa một CPU không đủ cho pốt thứ ba.” (0.857): Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút) — NOT_VERIFIED bằng tai người',
    'Tổng CPU trống của cụm không nói được gì, phải có một nút đủ chỗ, và trộn Pod lớn với Pod nhỏ giúp lấp chỗ thừa.':
        'ASR chép “Tổng CPU trống cuộc cùng không nói được gì phải có một nút đủ chỗ và trộn pốt lớn với pốt nhỏ giúp lắp chỗ thừa.” (0.808): Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút); lệch âm/thanh thuần Việt: của cụm/cuộc cùng, lấp/lắp — NOT_VERIFIED bằng tai người',
    'Bộ xếp lịch coi Pod cần 0 tài nguyên và nhồi quá nhiều Pod vào một nút.':
        'ASR chép “Bộ xếp lịch coi pốt cần không tài nguyên và nhồi quá nhiều pốt vào một nút.” (0.882): Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút) — NOT_VERIFIED bằng tai người',
    'Pod thật dùng 0 phẩy 2 CPU mà yêu cầu 2, nên chỗ giữ trống, nút báo đầy mà máy vẫn rảnh.':
        'ASR chép “Pốt thực dùng không phải hai CPU mà yêu cầu hai, nền chỗ giữ trống, nút báo đầy mà máy vẫn rảnh.” (0.818): Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút); “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; lệch âm/thanh thuần Việt: nên/nền — NOT_VERIFIED bằng tai người',
    'Pod khởi động lại liên tục thường là vượt giới hạn bộ nhớ.':
        'ASR chép “Thúc khởi động lại liên tục thường là vượt giới hạn bộ nhớ.” (0.923): Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút) — NOT_VERIFIED bằng tai người',
    'Pod chậm bất thường mà không chết thường là bị hãm CPU, hai triệu chứng khác nhau cần hai cách sửa khác nhau.':
        'ASR chép “Phúc chậm bất thường mà không chết thường là bị hảm CPU. 2 triệu chứng khác nhau cần 2 cách sửa khác nhau.” (0.913): Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút); lệch âm/thanh thuần Việt: hãm/hảm — NOT_VERIFIED bằng tai người',
    'Câu một, nút 8 CPU, Pod yêu cầu 2 phẩy 5 CPU, vừa mấy Pod và thừa bao nhiêu?':
        'ASR chép “Câu 1, nút 8CPU, pốt yêu cầu 2,5CPU vừa mấy pốt và thừa bao nhiêu?” (0.895): Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút) — NOT_VERIFIED bằng tai người',
    'Câu hai, có hai nút 4 CPU.':
        'ASR chép “Câu 2, có 2 nút 4 sé phù.” (0.8): CPU đọc thô (probe CLD p1: 7/8) — NOT_VERIFIED bằng tai người',
    'Xếp lần lượt 4 Pod 1 phẩy 5 CPU rồi 1 Pod 1 CPU, mỗi Pod vào nút đầu tiên còn đủ chỗ.':
        'ASR chép “Xếp lần lượt 4 pốt 1.5 CPU rồi 1 pốt 1 CPU, mỗi pốt vào nút đầu tiên còn đủ chỗ.” (0.844): Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút); “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải” — NOT_VERIFIED bằng tai người',
    'Pod 1 CPU vào nút nào, và còn thừa bao nhiêu?':
        'ASR chép “Phúc 1 CPU vào nút nào và còn thừa bao nhiêu.” (0.909): Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút) — NOT_VERIFIED bằng tai người',
    'Đáp án câu một, phần nguyên của 8 chia 2 phẩy 5 bằng 3 Pod, thừa 0 phẩy 5 CPU.':
        'ASR chép “Đáp án câu 1, phần nguyên của 8 chia 2 phải 5 bằng 3 pút, thừa 0 phải 5 cp.” (0.8): “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút); CPU đọc thô (probe CLD p1: 7/8) — NOT_VERIFIED bằng tai người',
    'Câu hai, nút một nhận 2 Pod lớn và còn 1, nút hai nhận 2 Pod lớn và còn 1.':
        'ASR chép “Câu 2, nút 1 nhận 2 phút lớn và còn 1, nút 2 nhận 2 phút lớn và còn 1.” (0.9): Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút) — NOT_VERIFIED bằng tai người',
    'Pod 1 CPU vào nút một, nên nút một còn 0 và nút hai còn 1.':
        'ASR chép “Phúc 1 CPU vào nút 1, nên nút 1 còn 0 và nút 2 còn 1.” (0.938): Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút) — NOT_VERIFIED bằng tai người',
    'Cuốn chiếu thay dần từng nhóm Pod cũ bằng Pod mới, ít tài nguyên thừa, nhưng bản cũ và bản mới chạy cùng lúc.':
        'ASR chép “Cũng chiếu thay dần từng nhóm pốt cũ bằng pốt mới, ít tài nguyên thừa, nhưng bản cũ và bản mới chạy cùng lúc.” (0.875): Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút); lệch âm/thanh thuần Việt: cuốn/cũng — NOT_VERIFIED bằng tai người',
    'Số được dư làm tròn lên thành 3, nên có tối đa 13 Pod cùng lúc.':
        'ASR chép “Số được dư làm trọn lên thành 3 nên có tối đa 13 phút cùng lúc.” (0.882): Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút); lệch âm/thanh thuần Việt: tròn/trọn — NOT_VERIFIED bằng tai người',
    'Pod mới vừa khởi động đã nhận lưu lượng trong khi còn đang nạp dữ liệu, và khách gặp lỗi.':
        'ASR chép “Pốt mới vừa khởi động đã nhận lưu lượng trong khi còn đang nạp dữ liệu và khách gặp lỗi.” (0.95): Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút) — NOT_VERIFIED bằng tai người',
    'Hãy khai báo kiểm tra sẵn sàng, để Pod chỉ nhận yêu cầu khi đã sẵn sàng thật.':
        'ASR chép “Hãy khai báo kiểm tra sẵn sàng để phút chỉ nhận yêu cầu khi đã sẵn sàng thật.” (0.944): Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút) — NOT_VERIFIED bằng tai người',
    'Câu một, 4 bản, được thiếu 25 phần trăm, được dư 25 phần trăm, tối thiểu mấy bản sẵn sàng, và tối đa mấy Pod?':
        'ASR chép “Câu 1-4 bản được thiếu 25% được dư 25% tối thiểu mấy bản sẵn sàng và tối đa mấy phút.” (0.966): Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút) — NOT_VERIFIED bằng tai người',
    'Đáp án câu một, 4 nhân 0 phẩy 25 bằng 1, nên thiếu 1 và dư 1, tối thiểu 3 bản sẵn sàng, tối đa 5 Pod.':
        'ASR chép “Đáp án câu 1, 4 nhân không phải 25 bằng 1, nên thiếu 1 và dư 1, tối thiểu 3 bạn sẵn sàng, tối đa 5 phút.” (0.897): “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút); lệch âm/thanh thuần Việt: bản/bạn — NOT_VERIFIED bằng tai người',
    'Khám phá dịch vụ nghĩa là gọi bằng một tên ổn định, hệ phân giải tên nội bộ trả về địa chỉ, và danh sách Pod phía sau được cập nhật tự động.':
        'ASR chép “Khám phá dịch vụ nghĩa là gọi bằng một tên ổn định, hề phân giải tên nội bộ trả về địa chỉ và danh sách hút phía sau được cập nhật tự động.” (0.939): Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút); lệch âm/thanh thuần Việt: hệ/hề — NOT_VERIFIED bằng tai người',
    'Phân giải tên một lần lúc khởi động rồi giữ địa chỉ, thì khi Pod đổi chương trình vẫn gọi địa chỉ cũ.':
        'ASR chép “Phân giải tên một lần lúc khởi động rồi giữ địa chỉ thì khi pốt đổi chương trình vẫn gọi địa chỉ cũ.” (0.957): Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút) — NOT_VERIFIED bằng tai người',
    'Ở bài sau, bài 10, ta học dung lượng và hàng đợi, với định luật Little và mô hình hàng đợi một máy.':
        'ASR chép “Ở bài sau, bài 10, ta học dung lượng và hàng đợi, với định luật liết tồ và mô hình hàng đợi một máy.” (0.936): Little đọc thô (probe CLD p1: 5/8, ASR viết “lít tồ”) — NOT_VERIFIED bằng tai người',
    'Định luật Little nói số yêu cầu đang ở trong hệ bằng tốc độ đến nhân thời gian mỗi yêu cầu ở trong hệ.':
        'ASR chép “Định luật Lycto nói số yêu cầu đang ở trong hệ bằng tốc độ đến dân thời gian mỗi yêu cầu ở trong hệ.” (0.917): Little đọc thô (probe CLD p1: 5/8, ASR viết “lít tồ”); lệch âm/thanh thuần Việt: nhân/dân — NOT_VERIFIED bằng tai người',
    'Với mô hình hàng đợi một máy cơ bản, yêu cầu đến ngẫu nhiên, phục vụ ngẫu nhiên, và lam-đa nhỏ hơn muy, thời gian trong hệ W bằng 1 chia muy trừ lam-đa.':
        'ASR chép “Với mô hình hàng đợi một máy cơ bản, yêu cầu đến ngẫu nhiên, phục vụ ngẫu nhiên và lambda nhỏ hơn nguy, thời gian trong hệ vê đúc bằng một chia nguy trừ lambda.” (0.904): muy (μ) ASR viết “my/nguy”; W đọc tên chữ cái “vê đúp”, ASR viết “vê đúc/về đút” (đã chấp nhận ở các khoá trước) — NOT_VERIFIED bằng tai người',
    'Muy bằng 100, lam-đa bằng 80 thì W bằng 1 phần 20 giây, tức 50 mi li giây.':
        'ASR chép “My bằng 100, lambda bằng 80 thì về đút bằng một phần 20 giây, tức 50 mili giây.” (0.826): muy (μ) ASR viết “my/nguy”; W đọc tên chữ cái “vê đúp”, ASR viết “vê đúc/về đút” (đã chấp nhận ở các khoá trước); tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh — NOT_VERIFIED bằng tai người',
    'Theo Little, số yêu cầu trong hệ là 80 nhân 0 phẩy 05, bằng 4.':
        'ASR chép “Theo listo, số yêu cầu trong hệ là 80 nhân 0.05 bằng 4.” (0.903): Little đọc thô (probe CLD p1: 5/8, ASR viết “lít tồ”); “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải” — NOT_VERIFIED bằng tai người',
    'Lam-đa bằng 95 thì W bằng 1 phần 5 giây, tức 200 mi li giây, và có 19 yêu cầu trong hệ.':
        'ASR chép “Lam đa bằng 95 thì về đúc bằng 1 phần 5 giây, tức 200 mili giây và có 19 yêu cầu trong hệ.” (0.889): W đọc tên chữ cái “vê đúp”, ASR viết “vê đúc/về đút” (đã chấp nhận ở các khoá trước); tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh — NOT_VERIFIED bằng tai người',
    'Nhưng hình dạng dựng đứng gần công suất thì hệ nào cũng có, và định luật Little thì luôn đúng.':
        'ASR chép “Nhưng hình dạng dựng đứng gần công suất thì hệ nào cũng có, và định luật liết tổ thì luôn đúng.” (0.927): Little đọc thô (probe CLD p1: 5/8, ASR viết “lít tồ”) — NOT_VERIFIED bằng tai người',
    'Câu hai, theo Little, W bằng 30 chia 600 giây, tức 50 mi li giây, không cần biết phân phối.':
        'ASR chép “Câu 2, theo liếc tụ, về đút bằng 30 chia 600 giây tức 50 mili giây không cần biết phân phối.” (0.809): Little đọc thô (probe CLD p1: 5/8, ASR viết “lít tồ”); W đọc tên chữ cái “vê đúp”, ASR viết “vê đúc/về đút” (đã chấp nhận ở các khoá trước); tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh — NOT_VERIFIED bằng tai người',
    'Tổng kết lại, định luật Little luôn đúng.':
        'ASR chép “Tổng kết lại, định lực lít tồ luôn đúng.” (0.706): Little đọc thô (probe CLD p1: 5/8, ASR viết “lít tồ”) — NOT_VERIFIED bằng tai người',
    'Chào bạn, bảng theo dõi ghi độ trễ trung bình 52 phẩy 7 mi li giây, rất đẹp.':
        'ASR chép “Chào bạn! Bản theo dõi di độ trễ trung bình 52,7mL rất đẹp.” (0.789): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; lệch âm/thanh thuần Việt: bảng/bản, ghi/di — NOT_VERIFIED bằng tai người',
    'Đó chỉ là cách viết byte bằng chữ cái, ai cũng giải ngược được, chuỗi mã trên màn hình giải ra đúng mật khẩu.':
        'ASR chép “Đó chỉ là cách viết bay bằng chữ cái, ai cũng giải ngược được. Chủi mã trên màn hình giải ra đúng mật khẩu.” (0.917): byte đọc thô, ASR viết “bay” (probe CSA p1 8/8); lệch âm/thanh thuần Việt: chuỗi/chủi — NOT_VERIFIED bằng tai người',
    # ── DVO L00–L12 (2026-10-30) ──
    'Hôm nay ta học DevOps, rút ngắn vòng phản hồi từ lúc viết mã tới lúc biết nó chạy đúng với người dùng.':
        'ASR chép “Hôm nay ta học Devos, đúc ngắn vòng phản hồi từ lúc viết mã tới lúc biết nó chạy đúng với người dùng.” (0.913): DevOps đọc thô (probe DVO p1: 6/8, NOT_VERIFIED) — NOT_VERIFIED bằng tai người',
    'Tổng kết lại, DevOps rút ngắn vòng phản hồi từ mã tới người dùng.':
        'ASR chép “Tổng kết lại, Devoop rút ngắn vòng phản hội từ mã tới người dung.” (0.786): DevOps đọc thô (probe DVO p1: 6/8, NOT_VERIFIED); lệch âm/thanh thuần Việt: hồi/hội, dùng/dung — NOT_VERIFIED bằng tai người',
    'Lỗi thứ nhất, tin rằng bản vá không bao giờ phá chương trình.':
        'ASR chép “Lỗi thứ nhất, tình trạng bản vã không bao giờ phá chương trình.” (0.769): lệch âm/thanh thuần Việt: tin rằng/tình trạng, vá/vã — NOT_VERIFIED bằng tai người',
    'Hãy kiểm logic ở tầng đơn vị, chỉ vài kịch bản quan trọng nhất mới đi hết đầu cuối.':
        'ASR chép “Hãy kiểm logist ở tầng đơn vị, chỉ vài kịch bản quan trọng nhất mới đi hết đầu cuối.” (0.947): logic đọc “lô-gíc” theo lexicon chung, ASR viết dạng tiếng Anh — NOT_VERIFIED bằng tai người',
    'Mã băm là dấu vân tay của nội dung, đổi một byte là đổi mã băm, và ta dùng nó để chỉ chính xác bản nào.':
        'ASR chép “Mả băm là giấu vân tay của nội dung, đổi một bay là đổi mả băm và ta dùng nó để chỉ chính xác bản nào.” (0.885): byte đọc thô, ASR viết “bay” (probe CSA p1 8/8); lệch âm/thanh thuần Việt: mã/mả, mã/mả — NOT_VERIFIED bằng tai người',
    'Tái lập nghĩa là cùng mã nguồn, cùng công cụ thì dựng ra đúng cùng từng byte.':
        'ASR chép “Tái lập nghĩa là cùng mảm nguồn, cùng công cụ thì dựng ra đúng cùng từng bay.” (0.882): byte đọc thô, ASR viết “bay” (probe CSA p1 8/8); lệch âm/thanh thuần Việt: mã/mảm — NOT_VERIFIED bằng tai người',
    'Lần hai dựng lại với mã y nguyên, nhưng thời điểm là chiều ngày 2, và mã băm khác hẳn.':
        'ASR chép “Lần hai dựng lại với mã yên nguyên, nhưng thời điểm là chiều ngày hai và mã băm khắc hẳn.” (0.9): lệch âm/thanh thuần Việt: i/yên, khác/khắc — NOT_VERIFIED bằng tai người',
    'Đáp án câu một, có đổi, vì đổi một byte nội dung là đổi mã băm.':
        'ASR chép “Đáp án câu một có đổi, vì đổi một vai nội dung là đổi mã băm.” (0.938): byte đọc thô, ASR viết “bay” (probe CSA p1 8/8) — NOT_VERIFIED bằng tai người',
    'Đổi một byte là phải kiểm lại.':
        'ASR chép “Đổi một bay là phải kiểm lại.” (0.857): byte đọc thô, ASR viết “bay” (probe CSA p1 8/8) — NOT_VERIFIED bằng tai người',
    'Chào bạn, một kịch bản thêm 2 máy chủ web bị lỗi mạng giữa chừng, người trực chạy lại cho chắc.':
        'ASR chép “Chào bạn, một kịch bản thêm hai máy chủ hét bị lỗi mạng giữa chừng, người trực chạy lại cho chắc.” (0.952): web đọc thô (probe NET p2: 8/8), lần này ASR viết sai — NOT_VERIFIED bằng tai người',
    'Bảng so hai cách mô tả hạ tầng.':
        'ASR chép “Vãng so 2 cách mô tả hạ từng.” (0.75): lệch âm/thanh thuần Việt: bảng/vãng, tầng/từng — NOT_VERIFIED bằng tai người',
    'Mã mới lỗi, quay lui về mã cũ, nhưng lược đồ đã đổi nên mã cũ cũng không chạy.':
        'ASR chép “Mạ mới lỗi quay lui về mạ cũ nhưng lực đồ đã đổi nên mạ cũ cũng không chạy.” (0.789): lệch âm/thanh thuần Việt: mã/mạ, mã/mạ, lược/lực, mã/mạ — NOT_VERIFIED bằng tai người',
    'Xét 1000 yêu cầu mỗi giây, mỗi yêu cầu ghi 1 ki lô byte nhật ký.':
        'ASR chép “Xét 1.000 yêu cầu mỗi giây, mỗi yêu cầu ghi 1 kg 3 nhật ký.” (0.848): “ki-lô-byte” đọc tách âm tiết, ASR viết “kg” rồi chép “byte” thành “bay/ba”; byte đọc thô, ASR viết “bay” (probe CSA p1 8/8) — NOT_VERIFIED bằng tai người',
    'Câu một, 500 yêu cầu mỗi giây, 2 ki lô byte nhật ký mỗi yêu cầu, giữ 7 ngày, cần bao nhiêu GB?':
        'ASR chép “Câu 1, 500 yêu cầu mỗi giây, 2 kg bay nhật ký mỗi yêu cầu, giữ 7 ngày, cần bao nhiêu GB?” (0.894): “ki-lô-byte” đọc tách âm tiết, ASR viết “kg” rồi chép “byte” thành “bay/ba”; byte đọc thô, ASR viết “bay” (probe CSA p1 8/8) — NOT_VERIFIED bằng tai người',
    'Đáp án câu một, 500 nhân 2000 nhân 86 nghìn 400 nhân 7, bằng 604 phẩy 8 GB.':
        'ASR chép “Đáp án câu 1, 500 nhân 2.000 nhân 86.400 nhân 7, bằng 604,8 gigabyte.” (0.962): GB đọc “ghi-ga-byte” theo lexicon của khoá, ASR viết “gigabyte” — NOT_VERIFIED bằng tai người',
    # ── MLO L00–L13 (2026-10-30) ──
    'Mã băm nội dung được tính từ từng byte của tệp, cùng nội dung thì cùng mã, đổi một byte thì mã khác hẳn, và tên tệp không ảnh hưởng.':
        'ASR chép “Mả băm nội dung được tính từ từng bay của tệp, cùng nội dung thì cùng mả, đổi một bay thì mả khác hẳn và tên tệp không ảnh hưởng.” (0.833): byte đọc thô, ASR viết “bay” (probe CSA p1 8/8); lệch âm/thanh thuần Việt: mã/mả, mã/mả, mã/mả — NOT_VERIFIED bằng tai người',
    'Mở rồi lưu lại bằng trình soạn thảo khác có thể đổi kiểu xuống dòng hay mã hoá ký tự, cùng bảng số nhưng khác byte nên khác mã băm.':
        'ASR chép “Mở rồi lưu lại bằng trình soạn thảo khác có thể đổi kiểu xuống dòng hay mã hóa ký tự, cùng bản số nhưng khác bai nên khác mã băm.” (0.933): byte đọc thô, ASR viết “bay” (probe CSA p1 8/8); lệch âm/thanh thuần Việt: bảng/bản — NOT_VERIFIED bằng tai người',
    'Kho mã giữ mọi phiên bản mãi mãi, một tệp 5 GB sửa 10 lần là 50 GB.':
        'ASR chép “Kho mả giữ mọi phiên bản mãi mãi, một tếp 5GB xử 10 lần là 50GB.” (0.842): GB đọc “ghi-ga-byte” theo lexicon của khoá, ASR viết “GB/gigabyte”; lệch âm/thanh thuần Việt: mã/mả, tệp/tếp, sửa/xử — NOT_VERIFIED bằng tai người',
    'Cách sửa là gộp tối đa 32 cái hoặc tối đa 10 mi li giây, điều kiện nào tới trước.':
        'ASR chép “Các sữa là gột tối đa 32 cái hoặc tối đa 10 mili giây, điều kiện nào tới trước.” (0.791): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; lệch âm/thanh thuần Việt: cách sửa/các sữa, gộp/gột — NOT_VERIFIED bằng tai người',
    'Tổng kết lại, chia khoảng và so tỉ lệ, cộng các số hạng a trừ e nhân lôgarit a chia e, tổng luôn không âm.':
        'ASR chép “Tổng kết lại, chia khoản và so tỷ lệ, cộng các số hạng A trừ E nhân Logarit A-GE, tổng luôn không âm.” (0.857): “tỉ” ASR viết chính tả “tỷ” (cùng âm); chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: khoảng/khoản — NOT_VERIFIED bằng tai người',
    'Trôi khái niệm có thể xảy ra khi phân bố đầu vào y nguyên, và chỉ lộ ra khi so dự đoán với nhãn thật, nên cần có đường thu nhãn, dù bị trễ.':
        'ASR chép “Trôi khái niệm có thể xảy ra khi phân bố đầu vào yên nguyên và chỉ lộ ra khi so dự đoán với nhãn thật nên cần có đường thu nhãn, dù bị trễ.” (0.971): lệch âm/thanh thuần Việt: i/yên — NOT_VERIFIED bằng tai người',
    'Chào bạn, một mô hình 7 tỉ tham số, mỗi tham số là số thực 32 bit, tức 4 byte.':
        'ASR chép “Chào bạn, một mô hình 7 tỷ tham số, mỗi tham số là số thật 32 bit, tức 4 vai.” (0.864): “tỉ” ASR viết chính tả “tỷ” (cùng âm); byte đọc thô, ASR viết “bay” (probe CSA p1 8/8); lệch âm/thanh thuần Việt: thực/thật — NOT_VERIFIED bằng tai người',
    'Riêng trọng số đã cần 28 GB, không vừa bộ nhớ của bộ xử lý đồ hoạ 24 GB đang có.':
        'ASR chép “Riêng trọng số đã cần 28GB, không vừa bộ nhớ của bộ sử lý đồ họa 24GB đang có.” (1.0): GB đọc “ghi-ga-byte” theo lexicon của khoá, ASR viết “GB/gigabyte” — NOT_VERIFIED bằng tai người',
    'Số thực 32 bit, 4 byte mỗi tham số, cần 28 GB.':
        'ASR chép “Số thực 32-bit, 4 bài mỗi tham số, cần 28 GB.” (0.938): byte đọc thô, ASR viết “bay” (probe CSA p1 8/8) — NOT_VERIFIED bằng tai người',
    'Mô hình 13 tỉ tham số ở 16 bit cần bao nhiêu GB?':
        'ASR chép “Mô hình 13 tỷ tham số ở 16 biết cần bao nhiêu gigabyte?” (0.8): “tỉ” ASR viết chính tả “tỷ” (cùng âm); GB đọc “ghi-ga-byte” theo lexicon của khoá, ASR viết “gigabyte”; lệch âm/thanh thuần Việt: bit/biết — NOT_VERIFIED bằng tai người',
    'Tổng kết lại, bộ nhớ bằng số tham số nhân số byte.':
        'ASR chép “Tổng kết lại, bộ nhớ bằng số tham số nhân số bay.” (0.917): byte đọc thô, ASR viết “bay” (probe CSA p1 8/8) — NOT_VERIFIED bằng tai người',
    'Người nói giọng đó gặp lỗi gấp bốn lần.':
        'ASR chép “Người nói dòng đó gặp lụi gấp 4 lần.” (0.778): lệch âm/thanh thuần Việt: giọng/dòng, lỗi/lụi — NOT_VERIFIED bằng tai người',
    'Tệp trọng số có thể đã được cài cửa sau, hoặc chứa mã chạy khi nạp, nên hãy kiểm mã băm, chữ ký, và nạp bằng định dạng không chạy mã, như quét phụ thuộc ở khoá DevOps.':
        'ASR chép “Tạp trọng số có thể đã được cài cửa sau hoặc chứa mã chạy khi nạp, nên hãy kiểm mã băm, chữ ký và nạp bằng định dạng không chạy mã, như quét phụ thuộc ở khóa Devos.” (0.947): DevOps đọc thô (probe DVO p1: 6/8, NOT_VERIFIED); lệch âm/thanh thuần Việt: tệp/tạp — NOT_VERIFIED bằng tai người',
    # ── SAR L00–L12 (2026-10-30) ──
    'Băng thông bằng yêu cầu mỗi giây nhân kích thước trả về, nhân 8 để đổi byte sang bit.':
        'ASR chép “bằng thông bằng yêu cầu mỗi dây nhân kích thước trả về, nhần 8 để đổi bay sang bit.” (0.842): byte đọc thô, ASR viết “bay” (probe CSA p1 8/8); lệch âm/thanh thuần Việt: băng/bằng, nhân/nhần — NOT_VERIFIED bằng tai người',
    'Nếu mỗi người đăng 1 bài 2 KB mỗi ngày, lưu trữ khoảng 7 phẩy 3 tê-ra-byte mỗi năm.':
        'ASR chép “Nếu mỗi người đăng một bài 2 kilobytes mỗi ngày, lưu trữ khoảng 7,3 terabytes mỗi năm.” (0.85): KB đọc “ki-lô-byte” theo lexicon của khoá, ASR viết “kilobyte/kg”; “tê-ra-byte” đọc tách âm tiết (đã dựng ở OSY/NET), ASR viết “TB/terabyte” — NOT_VERIFIED bằng tai người',
    'Nếu mỗi lần trả về 50 KB, băng thông trung bình khoảng 926 mê-ga-bít mỗi giây.':
        'ASR chép “Nếu mỗi lần trả về 50 kilobyte, bàn thông trung bình khoảng 926 megabit mỗi giây.” (0.818): KB đọc “ki-lô-byte” theo lexicon của khoá, ASR viết “kilobyte/kg”; “mê-ga-bít” đọc tách âm tiết (đã dựng ở NET), ASR viết “megabit”; lệch âm/thanh thuần Việt: băng (trong “kb băng” → “kilobyte bàn”) — NOT_VERIFIED bằng tai người',
    'Lỗi thứ hai là nhầm lẫn giữa đơn vị byte và đơn vị bit.':
        'ASR chép “Lỗi thứ 2 là nhầm lẫn giữa đơn vị bay và đơn vị biết.” (0.857): byte đọc thô, ASR viết “bay” (probe CSA p1 8/8); lệch âm/thanh thuần Việt: bit/biết — NOT_VERIFIED bằng tai người',
    'Đường truyền 1 ghi-ga-bít mỗi giây chỉ chở khoảng 125 MB mỗi giây, sai 8 lần, nên hãy ghi rõ đơn vị ở mỗi bước.':
        'ASR chép “Đừng truy mục ghi ra biết mỗi dây chỉ chở khoảng 125 MB mỗi dây, sai 8 lần, nên hãy ghi rõ đơn vị ở mỗi bước.” (0.839): “ghi-ga-bít / mê-ga-bít” đọc tách âm tiết; mê-ga-bít đã dựng ở NET, ghi-ga-bít NOT_VERIFIED riêng cụm (lexicon SAR); lệch âm/thanh thuần Việt: đường truyền một/đừng truy mục — NOT_VERIFIED bằng tai người',
    'Có 7 phẩy 3 tê-ra-byte dữ liệu, sao chép 3 bản, thêm chỉ mục và nhật ký, thì dung lượng đĩa thật dễ gấp 4 đến 5 lần con số thô.':
        'ASR chép “Có 7,3 terabyte dữ liệu, sao chép 3 bảng, thêm chỉ một vài nhật ký thì dung lượng để thật dễ gấp 4 đến 5 lần con số thô.” (0.812): “tê-ra-byte” đọc tách âm tiết (đã dựng ở OSY/NET), ASR viết “TB/terabyte”; lệch âm/thanh thuần Việt: bản/bảng, mục và/một vài, đĩa/để — NOT_VERIFIED bằng tai người',
    'Mỗi người gửi 50 tin, tạo 100 KB dữ liệu mới mỗi ngày, cao điểm gấp 4.':
        'ASR chép “Mỗi người gửi 50 tin tạo 100kg dữ liệu mới mỗi ngày, cao điểm gấp 4.” (0.947): KB đọc “ki-lô-byte” theo lexicon của khoá, ASR viết “kilobyte/kg” — NOT_VERIFIED bằng tai người',
    'Câu hai, 2 triệu nhân 100 KB nhân 365, khoảng 73 tê-ra-byte mỗi năm.':
        'ASR chép “Câu 2, 2 triệu nhân 100kg nhân 365 khoảng 73TB mỗi năm.” (0.864): KB đọc “ki-lô-byte” theo lexicon của khoá, ASR viết “kilobyte/kg”; “tê-ra-byte” đọc tách âm tiết (đã dựng ở OSY/NET), ASR viết “TB/terabyte” — NOT_VERIFIED bằng tai người',
    'Lấy thời gian đọc đệm là 1 mi li giây, đọc cơ sở dữ liệu là 50 mi li giây.':
        'ASR chép “Lấy thời gian độc đệm là 1 millijay, độc cơ sở dữ liệu là 50 millijay.” (0.684): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; lệch âm/thanh thuần Việt: đọc/độc, đọc (trong “mi li giây đọc” → “millijay độc”) — NOT_VERIFIED bằng tai người',
    'Muốn dưới 5 thì 2h cộng 100 nhân 1 trừ h phải nhỏ hơn 5, nên h lớn hơn 95 phần 98, khoảng 96 phẩy 9 phần trăm.':
        'ASR chép “Muốn dưới 5 thì 2 giờ cộng 100 nhân 1 trừ hát phải nhỏ hơn 5, nền hát lớn hơn 95 phần 98, khoảng 96,9%.” (0.944): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: nên/nền — NOT_VERIFIED bằng tai người',
    'Có 5 tê-ra-byte dữ liệu, mỗi nút giữ 500 GB, sao chép 3 bản, thì cần 5000 chia 500 bằng 10, nhân 3, tức 30 nút.':
        'ASR chép “Có 5TB dữ liệu, mỗi nút giữ 500GB, sau chép 3 bảng thì cần 5000 chia 500 bằng 10, nhân 3, tức 30 nút.” (0.871): “tê-ra-byte” đọc tách âm tiết (đã dựng ở OSY/NET), ASR viết “TB/terabyte”; lệch âm/thanh thuần Việt: sao/sau, bản/bảng — NOT_VERIFIED bằng tai người',
    'Câu một, 12 tê-ra-byte dữ liệu, mỗi nút 2 tê-ra-byte, sao chép 3, cần bao nhiêu nút?':
        'ASR chép “Câu 1, 12TB dữ liệu, mỗi nút 2TB, xào chép 3, cần bao nhiêu nút?” (0.75): “tê-ra-byte” đọc tách âm tiết (đã dựng ở OSY/NET), ASR viết “TB/terabyte”; lệch âm/thanh thuần Việt: sao (trong “t ra byte sao” → “tb xào”) — NOT_VERIFIED bằng tai người',
    'Câu hai, 7 phẩy 3 tê-ra-byte như ước lượng ở bài 2, mỗi nút 1 tê-ra-byte, sao chép 3, cần bao nhiêu nút?':
        'ASR chép “Câu 2, 7,3TB như ước lượng ở bài 2, mỗi nút 1TB, xào chép 3, cần bao nhiêu nút?” (0.8): “tê-ra-byte” đọc tách âm tiết (đã dựng ở OSY/NET), ASR viết “TB/terabyte”; lệch âm/thanh thuần Việt: sao (trong “t ra byte sao” → “tb xào”) — NOT_VERIFIED bằng tai người',
    'Nhận hết để không phụ lòng khách thì hàng đợi phình, độ trễ bùng nổ, hết giờ, thử lại, rồi sập.':
        'ASR chép “Nhận hết để không phụ lòng khách thi hàng đời phinh, đồ trễ buồn nổ, hết giờ, thử lại, rồi sập.” (0.762): lệch âm/thanh thuần Việt: thì/thi, đợi phình độ/đời phinh đồ, bùng/buồn — NOT_VERIFIED bằng tai người',
    'Câu một, thùng 5 token mỗi giây, sức chứa 10, khách gửi 100 yêu cầu mỗi giây trong 2 giây, tức 200 yêu cầu, được nhận bao nhiêu?':
        'ASR chép “Câu một, thùng 5 tô cần mỗi giây, sức chứa 10, khách gửi 100 yêu cầu mỗi giây trong 2 giây, tức 200 yêu cầu, được nhận bao nhiêu?” (0.968): token đọc “tâu-cần” theo lexicon SAR (probe p1 8/8), ASR viết “tô cần” — NOT_VERIFIED bằng tai người',
    'Bảng theo dõi tồn đọng qua hai giai đoạn.':
        'ASR chép “Bản theo dõi tồn đồng qua 2 giai đoạn.” (0.778): lệch âm/thanh thuần Việt: bảng/bản, đọng/đồng — NOT_VERIFIED bằng tai người',
    'Hàng đợi không giới hạn chỉ hoãn sự cố tới lúc hết đĩa hay độ trễ tính bằng ngày.':
        'ASR chép “Hàn đợi không giới hạn chỉ hoảng sự cố tới lúc hết để hay đồ trở tính bằng ngay.” (0.684): lệch âm/thanh thuần Việt: hàng/hàn, hoãn/hoảng, đĩa/để, độ trễ/đồ trở, ngày/ngay — NOT_VERIFIED bằng tai người',
    'Bất đồng bộ chỉ chờ vùng gần, mất 10 mi li giây.':
        'ASR chép “Bất đồng bộ chỉ chờ vùng gần, mất 10 mili dây.” (0.783): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh — NOT_VERIFIED bằng tai người',
    'Dữ liệu lưu 5 năm, 500 byte mỗi bản ghi, với mã ngắn 7 ký tự.':
        'ASR chép “Giữ liệu lưu năm năm, năm trăm bai mỗi bạn ghi với mạng ngắn 7 ký tự.” (0.824): byte đọc thô, ASR viết “bay” (probe CSA p1 8/8); lệch âm/thanh thuần Việt: bản/bạn, mã/mạng — NOT_VERIFIED bằng tai người',
    'Lưu trữ trong 5 năm là 3 tê-ra-byte.':
        'ASR chép “lưu trữ trong 5 năm là 3TB.” (0.778): “tê-ra-byte” đọc tách âm tiết (đã dựng ở OSY/NET), ASR viết “TB/terabyte” — NOT_VERIFIED bằng tai người',
    'Với 3 tê-ra-byte sao chép 3 bản trên nút 1 tê-ra-byte thì cần 9 nút, phân mảnh theo mã ngắn.':
        'ASR chép “Với 3TB sau chép 3 bảng trên nút 1TB thì cần 9 nút, phân mảnh theo mã ngắn.” (0.727): “tê-ra-byte” đọc tách âm tiết (đã dựng ở OSY/NET), ASR viết “TB/terabyte”; lệch âm/thanh thuần Việt: sao (trong “t ra byte sao” → “tb sau”), bản/bảng — NOT_VERIFIED bằng tai người',
    # ── SEC L00–L14 (2026-10-30) ──
    'Câu hai, người dùng tải lên tệp 5 GB làm đầy đĩa, đó là loại nào?':
        'ASR chép “Câu 2. Người dùng tải lên tệp 5GB làm đầy đĩa. Đó là loại nào?” (1.0): GB đọc “ghi-ga-byte” theo lexicon của khoá, ASR viết “GB/gigabyte” — NOT_VERIFIED bằng tai người',
    'Câu một, mã PIN 4 chữ số ngẫu nhiên có entropy bao nhiêu bit?':
        'ASR chép “Câu một, mãp bình bốn chữ số ngẫu nhiên có entropy bao nhiêu biết?” (0.786): lệch âm/thanh thuần Việt: mã pin/mãp bình, bit/biết — NOT_VERIFIED bằng tai người',
    'Câu hai, đổi thành mức chặt thì sao?':
        'ASR chép “Câu 2. Đổi thành mức chặt thị xáo.” (0.75): lệch âm/thanh thuần Việt: thì sao/thị xáo — NOT_VERIFIED bằng tai người',
    'Tổng kết lại, lỗ hổng chèn là khi dữ liệu bị hiểu thành mã.':
        'ASR chép “Tổng kết lại, lỗ hổng chen là khi giữ liệu bị hiểu thanh mả.” (0.786): lệch âm/thanh thuần Việt: chèn/chen, thành mã/thanh mả — NOT_VERIFIED bằng tai người',
    'Hàm khối mã một khối cố định, ví dụ 16 byte, bằng khoá, và nó tất định, cùng khoá cùng khối thì cùng kết quả.':
        'ASR chép “Hàm khối mã một khối cố định, ví dụ 16 bay, bằng khóa và nó tất định, cùng khóa cùng khối thì cùng kết quả.” (0.962): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    '6 byte đầu bằng 0 vì hai tin giống nhau ở đó, chỉ khác ở byte thứ bảy, nên lộ ra hai tin chỉ khác một chữ số.':
        'ASR chép “6 bai đầu bằng không vì 2 tin giống nhau ở đó, chỉ khác ở bai thứ 7, nên lộ ra 2 tin chỉ khác 1 chữ số.” (0.929): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Kiểm chuỗi có qua không, và vì sao?':
        'ASR chép “kiểm chuỗi có qua không và vi xáo.” (0.75): lệch âm/thanh thuần Việt: vì sao/vi xáo — NOT_VERIFIED bằng tai người',
    'Trước tấn công va chạm chỉ còn cỡ b chia 2 bit, nên muốn 128 bit an toàn thì cần băm ít nhất 256 bit.':
        'ASR chép “Trước tấn công va chạm chỉ còn cửa BG-2-bit nên muốn 128 bit an toàn thì cần bấm ít nhất 256 bit.” (0.892): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: cỡ chia (trong “cỡ b chia” → “cửa bg”), băm/bấm — NOT_VERIFIED bằng tai người',
    'Chào bạn, một hàm cấp 16 byte cho tên người dùng nhưng không kiểm độ dài.':
        'ASR chép “Chào bạn, một hàm cấp 16 bay cho tên người dùng nhưng không kiểm độ dài.” (0.941): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Ai đó gửi tên 20 byte, và 4 byte thừa tràn sang ô nhớ bên cạnh, có thể là một biến khác, hoặc địa chỉ mà hàm sẽ quay về khi xong.':
        'ASR chép “Ai đó gửi tên 20 bay và 4 bay thừa tràn sang ô nhớ bên cạnh có thể là một biến khác hoặc địa chỉ mà hàm sẽ quay về khi xong.” (0.939): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Luật hẹp đặt trước, và cuối cùng là mặc định chặn.':
        'ASR chép “Luộc hẹp đặt trước và cuối cùng là mặt định chẳng.” (0.727): lệch âm/thanh thuần Việt: luật/luộc, mặc/mặt, chặn/chẳng — NOT_VERIFIED bằng tai người',
    'Lỗi thứ hai, chỉ nhìn tỉ lệ bắt được mà quên tỉ lệ nền.':
        'ASR chép “Lỗi thứ hai, chỉ nhìn tỷ lệ bắt được mà quên tỷ lệ nên.” (0.786): “tỉ” ASR viết chính tả “tỷ” (cùng âm); lệch âm/thanh thuần Việt: nền/nên — NOT_VERIFIED bằng tai người',
    # ── AIF L00–L13 (2026-10-30) ──
    'Phòng hai ô là tĩnh, đường phố là động, thay đổi cả khi xe đang suy nghĩ.':
        'ASR chép “Phòng 2O là tỉnh, đường phố là động, thay đổi cả khi xe đang suy nghĩ.” (0.882): lệch âm/thanh thuần Việt: ô/o, tĩnh/tỉnh — NOT_VERIFIED bằng tai người',
    'g của n là chi phí đã đi từ trạng thái đầu tới nút n.':
        'ASR chép “V của N là chi phí đã đi từ trạng thái đầu tới nút N.” (0.933): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Giả sử nó lấy ra một đích G 2 có chi phí lớn hơn chi phí tối ưu C sao.':
        'ASR chép “Giả sử nó lấy ra một đích V2 có chi phí lớn hơn chi phí tối ưu xe sao.” (0.95): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'h 2 là tổng khoảng cách Manhattan của các ô tới chỗ đúng, bằng 18, và A sao chỉ mở 1 nghìn 481 nút.':
        'ASR chép “H2 là tổng khoảng cách mang hát tầng của các ô tới chỗ đúng bằng 18 và A sao chỉ mở 1481 nút.” (0.935): Manhattan đọc “Man-hát-tần” theo lexicon chung, ASR viết “mang hát tân/tầng” — NOT_VERIFIED bằng tai người',
    'A sao cũng phải kiểm đích khi lấy nút ra khỏi hàng đợi ưu tiên, lúc đó f của đích là nhỏ nhất, mới chắc là tối ưu.':
        'ASR chép “À sao cũng phải kiểm đích khi lấy nút ra khỏi hàng đời ưu tiên, lúc đó ép của đích là nhỏ nhất, mới chắc là tối ưu.” (0.929): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: đợi/đời — NOT_VERIFIED bằng tai người',
    'A sao giữ mọi nút đã sinh trong bộ nhớ.':
        'ASR chép “À, sao giữ mọi nút đã sinh trong bộ nhớ?” (0.9): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Theo khoảng cách Manhattan, ô 1 lệch 1, ô 6 lệch 2, ô 7 lệch 1, ô 4 lệch 2, nên h 2 bằng 6.':
        'ASR chép “Theo khoảng cách mang hát từ O1 lệch 1, O6 lệch 2, O7 lệch 1, O4 lệch 2, nền hát 2 bằng 6.” (0.741): Manhattan đọc “Man-hát-tần” theo lexicon chung, ASR viết “mang hát tân/tầng”; lệch âm/thanh thuần Việt: ô (trong “tần ô” → “từ o”), ô/o, ô/o, ô/o, nên/nền — NOT_VERIFIED bằng tai người',
    'Chào bạn, bài trước dùng hai hàm đánh giá cho trò xếp 8 ô số, số ô sai chỗ và tổng khoảng cách Manhattan.':
        'ASR chép “Chào bạn, bài trước dùng hai hàm đánh giá cho trò xếp 8 ô số, số ô sai chỗ và tổng khoảng cách mang hát tân.” (0.923): Manhattan đọc “Man-hát-tần” theo lexicon chung, ASR viết “mang hát tân/tầng” — NOT_VERIFIED bằng tai người',
    'Luật thật là một ô đi được sang ô kề nếu ô đó trống.':
        'ASR chép “Luật thật là một ô đi điều sang OK nếu ô đó trống.” (0.815): lệch âm/thanh thuần Việt: được/điều, ô kề/ok — NOT_VERIFIED bằng tai người',
    'Không có ước lượng, tìm chi phí đều mở 173 nghìn 799 nút, b sao bằng 1 phẩy 53.':
        'ASR chép “Không có ước lượng, tìm chi phí đã mở 173.799 nút, bè sao bằng 1,53.” (0.931): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: đều/đã — NOT_VERIFIED bằng tai người',
    'Nới lỏng luật nào để có hàm đánh giá Manhattan, và nới lỏng thêm nữa thì được hàm nào?':
        'ASR chép “nới lỏng lượt nào để có hàm đánh giá mang hát tần và nới lỏng thêm nữa thì được hàm nào.” (0.905): Manhattan đọc “Man-hát-tần” theo lexicon chung, ASR viết “mang hát tân/tầng”; lệch âm/thanh thuần Việt: luật/lượt — NOT_VERIFIED bằng tai người',
    'Câu hai, bỏ luật không đi xuyên tường thì được khoảng cách Manhattan.':
        'ASR chép “Câu 2. Bỏ luật không đi xuyên tường thì được khoảng cách mang hát tân.” (0.867): Manhattan đọc “Man-hát-tần” theo lexicon chung, ASR viết “mang hát tân/tầng” — NOT_VERIFIED bằng tai người',
    'Bỏ thêm luật chỉ đi 4 hướng, cho bay thẳng, thì được khoảng cách đường chim bay, nhỏ hơn và vẫn chấp nhận được, nhưng bị Manhattan trội.':
        'ASR chép “Bỏ thêm lược chỉ đi 4 hướng, cho bay thẳng thì được khoảng cách đường chim bay, nhỏ hơn và vẫn chấp nhận được nhưng bị man hát tân trội.” (0.933): Manhattan đọc “Man-hát-tần” theo lexicon chung, ASR viết “mang hát tân/tầng”; lệch âm/thanh thuần Việt: luật/lược — NOT_VERIFIED bằng tai người',
    'Trạng thái là hàng của hậu ở từng cột.':
        'ASR chép “Trạng thái là hàng của Hậu ở Tân Cô.” (0.778): lệch âm/thanh thuần Việt: từng cột/tân cô — NOT_VERIFIED bằng tai người',
    'Láng giềng là dời một hậu trong cột của nó, có 8 nhân 7 bằng 56 láng giềng.':
        'ASR chép “Lán viền là giờ một hậu trong cụt của nó, có 8 nhân 7 bằng 56 láng viền.” (0.75): lệch âm/thanh thuần Việt: láng giềng/lán viền, dời/giờ, cột/cụt, giềng/viền — NOT_VERIFIED bằng tai người',
    'Ở bài sau, bài 6, ta học trò chơi đối kháng, thuật toán cực đại cực tiểu, và cắt tỉa alpha beta.':
        'ASR chép “Ở bài sau, bài sáu, ta học trò chơi đối kháng, thuộc toán cực đại cực tiểu và cắt tỉa an pha beta.” (0.851): beta đọc “bê-ta”, ASR viết “bê/beta”; alpha đọc thô (probe AIF p1: 7/8, bản chép “an pha / ANFA / α”); lệch âm/thanh thuần Việt: thuật/thuộc — NOT_VERIFIED bằng tai người',
    'alpha là giá trị tốt nhất mà bên cực đại chắc chắn có được trên đường từ gốc tới nút đang xét.':
        'ASR chép “An pha là giá trị tốt nhất mà bên cực đại chắc chắn có được trên đường từ gốc tới nút đăng xét.” (0.889): alpha đọc thô (probe AIF p1: 7/8, bản chép “an pha / ANFA / α”); lệch âm/thanh thuần Việt: đang/đăng — NOT_VERIFIED bằng tai người',
    'Khi alpha lớn hơn hoặc bằng beta, nhánh đang xét không thể ảnh hưởng tới kết quả, nên bỏ qua phần còn lại của nó.':
        'ASR chép “Khi an pha lớn hơn hoặc bằng beta, nhánh đàn xét không thể ảnh hưởng tới kết quả nên bỏ qua phần còn lại của nó.” (0.868): alpha đọc thô (probe AIF p1: 7/8, bản chép “an pha / ANFA / α”); beta đọc “bê-ta”, ASR viết “bê/beta”; lệch âm/thanh thuần Việt: đang/đàn — NOT_VERIFIED bằng tai người',
    'Giờ cắt tỉa, xét xong B thì alpha bằng 3.':
        'ASR chép “Giờ cắt tỉa, xét xong b thì an pha bằng 3.” (0.857): alpha đọc thô (probe AIF p1: 7/8, bản chép “an pha / ANFA / α”) — NOT_VERIFIED bằng tai người',
    'Câu hai, xét xong nước thứ hai thì alpha bằng 6, nước thứ ba gặp lá 1 nhỏ hơn 6 nên bỏ lá 9, xét 5 lá.':
        'ASR chép “Câu 2, xét xong nước thứ 2 thì an pha bằng 6, nước thứ 3 gặp lá 1 nhỏ hơn 6 nên bỏ lá 9, xét 5 lá.” (0.945): alpha đọc thô (probe AIF p1: 7/8, bản chép “an pha / ANFA / α”) — NOT_VERIFIED bằng tai người',
    'alpha và beta ghi lại điều đã chắc chắn, alpha lớn hơn hoặc bằng beta thì bỏ nhánh, và xét nước tốt trước để cắt được nhiều.':
        'ASR chép “Anfa và Beta ghi lại điều đã chắc chắn, Anfa lớn hơn hoặc bằng Beta thì bỏ nhánh, và xét nước tốt trước để cắt được nhiều.” (0.862): alpha đọc thô (probe AIF p1: 7/8, bản chép “an pha / ANFA / α”); beta đọc “bê-ta”, ASR viết “bê/beta” — NOT_VERIFIED bằng tai người',
    'Có ba nước, C thắng 5 trên 10, D thắng 9 trên 10, E thắng 0 trên 1.':
        'ASR chép “Có 3 nước, xe thắng 5 trên 10, dè thắng 9 trên 10, e thắng 0 trên 1.” (0.944): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Đáp án câu một, C xấp xỉ 1 phẩy 274, D xấp xỉ 1 phẩy 674, E xấp xỉ 2 phẩy 448, nên lần tới thử E, vì mới có 1 lượt và chưa biết gì.':
        'ASR chép “Đáp án câu 1, xe sắp xỉ 1,274, dề sắp xỉ 1,674, e sắp xỉ 2,448, nên lần tới thử e, vì mới có một lượt và chưa biết gì.” (0.854): “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: xấp/sắp, xấp (trong “d xấp” → “dề sắp”), xấp/sắp — NOT_VERIFIED bằng tai người',
    'Tri thức kéo theo logic câu alpha nếu alpha đúng ở mọi mô hình của tri thức.':
        'ASR chép “Tri thức kéo theo logic câu α nếu α đúng ở mọi mô hình của tri thức.” (0.882): alpha đọc thô (probe AIF p1: 7/8, bản chép “an pha / ANFA / α”) — NOT_VERIFIED bằng tai người',
    'Kiểm mô hình nghĩa là liệt kê đủ 2 mũ n mô hình, giữ các mô hình của tri thức, rồi xem alpha có đúng ở tất cả không.':
        'ASR chép “Kiểm mô hình nghĩa là liệt kê đủ 2 mũ n mô hình, giữa các mô hình của tri thức, rồi xem an pha có đúng ở tất cả không.” (0.915): alpha đọc thô (probe AIF p1: 7/8, bản chép “an pha / ANFA / α”); lệch âm/thanh thuần Việt: giữ/giữa — NOT_VERIFIED bằng tai người',
    'Tri thức gồm ba câu, P kéo theo Q, Q kéo theo R, và P.':
        'ASR chép “Tri thức gồm 3 câu, T kéo theo Q, Q kéo theo R và P.” (0.933): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Tri thức có kéo theo câu không mưa không?':
        'ASR chép “Trị thức có kéo theo cầu không mưa không?” (0.778): lệch âm/thanh thuần Việt: tri/trị, câu/cầu — NOT_VERIFIED bằng tai người',
    'Trộm và động đất cùng trỏ tới báo động, còn báo động trỏ tới hai hàng xóm gọi điện.':
        'ASR chép “Trộm và động đức cùng trọ tới báo động, còn báo động trọ tới hai hàng sống gọi điện.” (0.789): lệch âm/thanh thuần Việt: đất/đức, trỏ/trọ, trỏ/trọ, xóm/sống — NOT_VERIFIED bằng tai người',
    'Các bảng cho xác suất trộm 0 phẩy 001, động đất 0 phẩy 002, và chuông tự kêu khi không có gì là 0 phẩy 001.':
        'ASR chép “các bản cho xác xuất trộm 0.001, động đất 0.002 và chung tự keo khi không có gì là 0.001.” (0.739): “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; lệch âm/thanh thuần Việt: bảng/bản, không (trong “không phẩy” → “”), không (trong “không phẩy” → “”), chuông/chung, kêu/keo, không (trong “không phẩy” → “”) — NOT_VERIFIED bằng tai người',
    'Biết chuông kêu thì xác suất trộm khoảng 0 phẩy 374.':
        'ASR chép “Biết chuông keo thì xác suất trộn khoảng 0,374.” (0.786): “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; lệch âm/thanh thuần Việt: kêu/keo, trộm/trộn, không (trong “không phẩy” → “”) — NOT_VERIFIED bằng tai người',
    'Câu một, biết có trộm, xác suất chuông kêu là bao nhiêu?':
        'ASR chép “Câu 1, biết có trộm, sẽ suốt chung kêu là bao nhiêu?” (0.75): lệch âm/thanh thuần Việt: xác suất chuông/sẽ suốt chung — NOT_VERIFIED bằng tai người',
    'Tổng kết lại, mạng Bayes gồm đồ thị và các bảng điều kiện, và phân phối đồng thời bằng tích các bảng.':
        'ASR chép “Tổng kết lại, mạng bay X gồm đồ thị và các bản điều kiện và phân phối đồng thời bằng tích các bản.” (0.87): Bayes đọc “Bay-ét” theo lexicon chung (probe 3/8, NOT_VERIFIED), ASR viết “bay X/S”; lệch âm/thanh thuần Việt: bảng/bản, bảng/bản — NOT_VERIFIED bằng tai người',
    'P của s phẩy khi biết s và a là xác suất tới ô s phẩy khi ở s và chọn hành động a, 0 phẩy 8 đúng hướng và 0 phẩy 1 mỗi bên.':
        'ASR chép “P của X phải khi biết X và A là xa xuất tới OX phải khi ở X và chọn hành động A, không phải 8 đúng hướng và không phải một mỗi bên.” (0.812): “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: xác/xa, ô (trong “ô s phẩy” → “ox phải”) — NOT_VERIFIED bằng tai người',
    'Có đối thủ thì dùng cực đại cực tiểu, alpha beta, hay cây mô phỏng ngẫu nhiên, ở bài 6 và 7.':
        'ASR chép “Có đối thủ thì dùng cực đại cực tiểu, an pha beta, hay cây mô phỏng ngẫu nhiên ở bài 6 và 7.” (0.894): beta đọc “bê-ta”, ASR viết “bê/beta”; alpha đọc thô (probe AIF p1: 7/8, bản chép “an pha / ANFA / α”) — NOT_VERIFIED bằng tai người',
    'Không chắc chắn về thế giới thì dùng mạng Bayes, ở bài 11.':
        'ASR chép “không chắc chắn về thế giới thì dùng mạng bay S ở bài 11.” (0.933): Bayes đọc “Bay-ét” theo lexicon chung (probe 3/8, NOT_VERIFIED), ASR viết “bay X/S” — NOT_VERIFIED bằng tai người',
    'Thứ hai, cắt tỉa alpha beta với thứ tự tốt, còn khoảng 2449 lá ở độ sâu 4.':
        'ASR chép “Thứ 2, các tiể Anfa Beta với thứ tự tốt còn khoảng 2449 lá ở độ sâu 4.” (0.84): beta đọc “bê-ta”, ASR viết “bê/beta”; alpha đọc thô (probe AIF p1: 7/8, bản chép “an pha / ANFA / α”); lệch âm/thanh thuần Việt: cắt tỉa (trong “cắt tỉa alpha b” → “các tiể anfa bê”) — NOT_VERIFIED bằng tai người',
    'Bài hai, dùng mạng Bayes, lỗi là nguyên nhân, triệu chứng là bằng chứng, và ta hỏi xác suất từng lỗi khi biết triệu chứng.':
        'ASR chép “Bài 2 Dùng mạn bay x lỗi là nguyên nhân, triệu chứng là bằng chứng và ta hỏi xác xuất từng lỗi khi biết triệu chứng.” (0.923): Bayes đọc “Bay-ét” theo lexicon chung (probe 3/8, NOT_VERIFIED), ASR viết “bay X/S”; lệch âm/thanh thuần Việt: mạng/mạn — NOT_VERIFIED bằng tai người',
    # ── CSA L11 dựng lại vì âm thanh cụt (2026-10-30) ──
    'Câu một, bộ nhớ đệm 8 nghìn byte, mỗi dòng dài 32 byte, địa chỉ 32 bit, có bao nhiêu dòng, và mỗi trường có mấy bit?':
        'ASR chép “Câu 1, bộ nhớ đệm 8.000 bay, mỗi dòng dài 32 bay, địa chỉ 32 bit, có bao nhiêu dòng và mỗi trường có mấy bit.” (0.935): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    # ── LLM L00–L13 (2026-10-31) ──
    'Ở bài sau, bài 1, ta học mô hình n-gram, cách làm trơn, và độ hỗn loạn.':
        'ASR chép “Ở bài sau, bài một, ta học mô hình engram, cách làm chân và độ hỗn loạn.” (0.857): n-gram đọc “en-gram” theo lexicon LLM, ASR viết “engram/N-RAM”; lệch âm/thanh thuần Việt: trơn/chân — NOT_VERIFIED bằng tai người',
    'Mô hình n-gram cho rằng từ tố tiếp theo phụ thuộc n trừ 1 từ tố trước, và mô hình cặp từ là trường hợp n bằng 2.':
        'ASR chép “Mô hình Engram cho rằng từ tố tiếp theo phụ thuộc N trừ 1 từ tố trước và mô hình cặp từ là trường hợp N bằng 2.” (0.947): n-gram đọc “en-gram” theo lexicon LLM, ASR viết “engram/N-RAM” — NOT_VERIFIED bằng tai người',
    'Tổng kết lại, mô hình n-gram nhìn n trừ 1 từ tố trước, và cặp chưa gặp cho xác suất 0.':
        'ASR chép “Tổng kết lại, mô hình N-RAM nhìn N trừ một từ tối trước và cặp chưa gặp cho xá suốt 0.” (0.818): n-gram đọc “en-gram” theo lexicon LLM, ASR viết “engram/N-RAM”; lệch âm/thanh thuần Việt: tố/tối, xác suất/xá suốt — NOT_VERIFIED bằng tai người',
    'Ở bài sau, bài 2, ta học cách tách văn bản thành từ tố, bằng mã hoá cặp byte.':
        'ASR chép “Ở bài sau, bài 2, ta học cách tách văn bản thành từ tố bằng mã hóa cặp bay.” (0.947): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Hôm nay ta học mã hoá cặp byte, cách học các mảnh từ từ dữ liệu mà hầu hết mô hình ngôn ngữ lớn dùng để tách văn bản.':
        'ASR chép “Hôm nay ta học mã hóa cặp bay, cách học các mảnh từ từ dữ liệu mà hầu hết mô hình ngôn ngữ lớn dùng để tách văn bản.” (0.966): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Bảng ghi năm lần gộp đầu tiên.':
        'ASR chép “Bản ghi 5 lần gột đầu tiên.” (0.714): lệch âm/thanh thuần Việt: bảng/bản, gộp/gột — NOT_VERIFIED bằng tai người',
    'Lần hai gộp mảnh e s với t, cũng 9 lần, trong cùng hai từ đó.':
        'ASR chép “Lần 2 gột mảnh EF với T cũng 9 lần trong cùng 2 từ đó.” (0.839): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: gộp/gột — NOT_VERIFIED bằng tai người',
    'Lần ba gộp đuôi e s t với dấu cuối từ, 9 lần.':
        'ASR chép “Lần 3 gọt đuôi, ST với giấu cuối từ, 9 lần.” (0.88): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: gộp/gọt — NOT_VERIFIED bằng tai người',
    'Lỗi thứ hai, quên rằng chữ có dấu tốn nhiều byte hơn, nên tiếng Việt đắt hơn.':
        'ASR chép “Lỗi thứ 2, quên rằng chữ có dấu tốn nhiều bay hơn, nền tiếng Việt đắt hơn.” (0.882): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: nên/nền — NOT_VERIFIED bằng tai người',
    'Bộ tách theo byte bắt đầu từ byte của văn bản, câu tôi thích mèo có 13 ký tự nhưng 16 byte, còn câu tiếng Anh cùng nghĩa có 11 ký tự và 11 byte.':
        'ASR chép “Bộ tách theo bai bắt đầu từ bai của văn bản, câu tôi thích mèo có 13 ký tự nhưng 16 bai, còn câu tiếng Anh cùng nghĩa có 11 ký tự và 11 bai.” (0.897): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Hoà thì lấy cặp gặp trước, nên luật sáu gộp n và e.':
        'ASR chép “Hoa thì lấy cặp gặp trước, nền lực 6 gộp N và E.” (0.769): lệch âm/thanh thuần Việt: hoà/hoa, nên luật/nền lực — NOT_VERIFIED bằng tai người',
    'Câu hai, từ đầu tiên được tách thành mảnh l o w và dấu cuối từ, tức 2 từ tố.':
        'ASR chép “Câu 2, từ đầu tiên được tách thành mảnh L-O-V-K-T và dấu cuối từ, tức 2 từ tố.” (0.93): chữ w đọc “vê kép” (luật chung), ASR viết tách chữ — NOT_VERIFIED bằng tai người',
    'Tổng kết lại, bắt đầu từ chữ cái hay byte, gộp cặp hay gặp nhất và lặp lại.':
        'ASR chép “Tổng kết lại, bắt đầu từ chữ cái hay bay, gột cặp hay gặp nhất và lập lại.” (0.833): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: gộp (trong “byte gộp” → “bay gột”), lặp/lập — NOT_VERIFIED bằng tai người',
    'Mặt nạ nhân quả cho vị trí i chỉ được chú ý tới các vị trí j không lớn hơn i.':
        'ASR chép “Mặt nạ nhân quả cho vị trí y chỉ được chú ý tới các vị trí y không lớn hơn y.” (0.952): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Bảng là mặt nạ cho chuỗi 4 từ tố.':
        'ASR chép “Bản là mặt nạ cho chuỗi bốn tư tố.” (0.778): lệch âm/thanh thuần Việt: bảng/bản, từ/bốn — NOT_VERIFIED bằng tai người',
    'Chào bạn, một mô hình khoảng 6 phẩy 4 tỉ tham số chiếm gần 13 GB ở dạng 2 byte mỗi số, vừa một thẻ tính toán.':
        'ASR chép “Chào bạn, một mô hình khoảng 6,4 tỷ tham số chiếm gần 13GB ở dạng 2 BI mỗi số, vừa mục thể tính toán.” (0.857): “tỉ” ASR viết chính tả “tỷ” (cùng âm); byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: một thẻ/mục thể — NOT_VERIFIED bằng tai người',
    'Nhưng phục vụ 16 người dùng cùng lúc, mỗi người ngữ cảnh 4096 từ tố, lại cần thêm khoảng 34 tỉ byte chỉ để nhớ khoá và giá trị của các từ tố đã đọc.':
        'ASR chép “Nhưng phục vụ 16 người dùng cùng lúc, mỗi người ngửi cảnh 4096 từ tố lại cần thêm khoảng 34 tỷ bay chỉ để nhớ khóa và giá trị của các từ tố đã đọc.” (0.932): “tỉ” ASR viết chính tả “tỷ” (cùng âm); byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: ngữ/ngửi — NOT_VERIFIED bằng tai người',
    'Đó là bộ nhớ đệm khoá giá trị, cần 2 nhân L nhân d nhân n số cho mỗi chuỗi.':
        'ASR chép “Đó là bộ nhớ đem khóa giá trị, cần 2 nhân L nhân V nhân N số cho mỗi chuỗi.” (0.9): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: đệm/đem — NOT_VERIFIED bằng tai người',
    'Bộ nhớ đệm cho một chuỗi 4096 từ tố bằng 2 nhân 32 nhân 4096 nhân 4096 nhân 2 byte, khoảng 2 tỉ 147 triệu byte.':
        'ASR chép “Bộ nhớ đệm cho một chuỗi 4.096 từ tố bằng 2 nhân, 32 nhân, 4.096 nhân, 4.096 nhân hai bay, khoảng 2.147 triệu bay.” (0.94): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); “tỉ” ASR viết chính tả “tỷ” (cùng âm) — NOT_VERIFIED bằng tai người',
    'Với băng thông 1 nghìn tỉ byte mỗi giây, một số minh hoạ, tối đa khoảng 78 từ tố mỗi giây.':
        'ASR chép “Với băng thông 1.000 tỷ bay mỗi giây, một số minh họa tối đa khoảng 78 từ tố mỗi giây.” (0.913): “tỉ” ASR viết chính tả “tỷ” (cùng âm); byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Lỗi thứ ba, lẫn đơn vị GB thập phân với đơn vị nhị phân, lệch nhau khoảng 7 phần trăm.':
        'ASR chép “Lỗi thứ 3, lẫn đơn vị Gigabyte thập phân với đơn vị Nhi Phân lịch nhau khoảng 7%” (0.85): GB đọc “ghi-ga-byte” theo lexicon của khoá, ASR viết “GB/gigabyte”; lệch âm/thanh thuần Việt: nhị/nhi, lệch/lịch — NOT_VERIFIED bằng tai người',
    'Một GB là 10 mũ 9 byte, còn một đơn vị nhị phân là 2 mũ 30, tức 1 tỉ 73 triệu 741 nghìn 824 byte.':
        'ASR chép “Một gigabyte là 10 mũ chín bay, còn một đơn vị nhị phân là 2 mũ 30, tức 1 tỷ 73,741,824 bay.” (0.892): GB đọc “ghi-ga-byte” theo lexicon của khoá, ASR viết “GB/gigabyte”; byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); “tỉ” ASR viết chính tả “tỷ” (cùng âm) — NOT_VERIFIED bằng tai người',
    'Mô hình có 40 tầng, chiều 5120, ngữ cảnh 8192 từ tố, 2 byte mỗi số.':
        'ASR chép “Mô hình có 40 tần, chiều 5.120 ngữ cảnh 8.192 từ tố, hai bay mỗi số.” (0.929): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: tầng/tần — NOT_VERIFIED bằng tai người',
    'Câu hai, bộ nhớ đệm khoá giá trị cho một chuỗi là bao nhiêu byte?':
        'ASR chép “Câu 2. Bộ nhớ đệm khóa giá trị cho một chuổi là bao nhiêu bay?” (0.867): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: chuỗi/chuổi — NOT_VERIFIED bằng tai người',
    'Câu hai, 2 nhân 40 nhân 5120 nhân 8192 nhân 2, bằng 6 tỉ 710 triệu 886 nghìn 400 byte, tức 6 phẩy 25 đơn vị nhị phân.':
        'ASR chép “Câu 2, 2 nhân 40 nhân 5.120 nhân 8.192, bằng 6 tỷ 710.886.400 bài, tức 6,25 đơn vị nhị phân.” (0.938): “tỉ” ASR viết chính tả “tỷ” (cùng âm); byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); “nhân 2” cuối dãy: small bỏ sót, medium chép đủ “… nhân 8.192 nhân 2” (âm thanh đủ, 0,444 s/từ) — NOT_VERIFIED bằng tai người',
    'Tổng kết lại, số tham số xấp xỉ 12 L d bình phương, bộ nhớ đệm bằng 2 L d n cho mỗi chuỗi.':
        'ASR chép “Tổng kết lại, số tham số sắp xỉ 12LV bình phương, bộ nhớ đem bằng 2LVN cho mỗi chuỗi.” (0.766): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: xấp/sắp, đệm/đem — NOT_VERIFIED bằng tai người',
    'Liên hệ với bài 1, độ hỗn loạn bằng e mũ mất mát, vì cùng dùng lôgarit tự nhiên.':
        'ASR chép “Liên hệ với bài 1, Độ hỗn loạn bằng e mũ mất mát, vì cùng dùng Logatrix tự nhiên.” (0.947): lệch âm/thanh thuần Việt: lôgarit/logatrix — NOT_VERIFIED bằng tai người',
    'Một nghiên cứu năm 2022 cho thấy với ngân sách cố định, mất mát nhỏ nhất khi D xấp xỉ 20 nhân N.':
        'ASR chép “Một nghiên cứu năm 2022 cho thấy với ngân sách cố định, mất mát nhỏ nhất khi về sắp xỉ 20 nhân N.” (0.933): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: xấp (trong “d xấp” → “về sắp”) — NOT_VERIFIED bằng tai người',
    'Bảng tính mất mát ở ba vị trí.':
        'ASR chép “Bản tính mất mắt ở 3 vị trí.” (0.75): lệch âm/thanh thuần Việt: bảng/bản, mát/mắt — NOT_VERIFIED bằng tai người',
    'Số phép tính xấp xỉ 6 N D, và tỉ lệ dữ liệu trên tham số chọn theo mục tiêu chi phí.':
        'ASR chép “số phép tính sắp xị 6NG và tỷ lệ dữ liệu trên tham số chọn theo mục tiêu chi phí.” (0.791): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; “tỉ” ASR viết chính tả “tỷ” (cùng âm); lệch âm/thanh thuần Việt: xấp xỉ/sắp xị — NOT_VERIFIED bằng tai người',
    'Tinh chỉnh hạng thấp giữ nguyên ma trận W cỡ d nhân d, và học thêm hai ma trận nhỏ B cỡ d nhân r, A cỡ r nhân d, với r nhỏ, ví dụ 8.':
        'ASR chép “Tinh chỉnh hạng thấp giữ nguyên ma trận về đúc cỡ dây nhân dê và học thêm hai ma trận nhỏ b cỡ dây nhân r, a cỡ r nhân dê, với r nhỏ, ví dụ 8.” (0.904): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Ma trận mới bằng W cộng B nhân A, và tích B nhân A có hạng tối đa r, tức thay đổi bị giới hạn trong r hướng.':
        'ASR chép “Ma trận mới bằng V đút cộng B nhân A và tích B nhân A có hạng tối đa R, tức thay đổi bị giới hạn trong R hướng.” (0.947): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'B khởi tạo bằng 0, nên lúc đầu mô hình y như cũ.':
        'ASR chép “Bế khởi tạo bằng không nên lúc đầu mô hình y như cũ.” (0.923): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Tổng kết lại, tinh chỉnh toàn bộ tốn khoảng 16 byte mỗi tham số, còn hạng thấp chỉ học r nhân d cộng d số.':
        'ASR chép “Tổng kết lại, tinh chính toàn bộ tốn khoảng 16 bai mỗi tham số còn hạn thấp chỉ học error nhân dê cộng dê số.” (0.846): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: chỉnh/chính, hạng/hạn — NOT_VERIFIED bằng tai người',
    'Tối ưu mạnh sẽ đẩy mô hình về phía câu dài dòng.':
        'ASR chép “Tối yêu mạnh sẽ đẩy mô hình về phía câu da dông.” (0.75): lệch âm/thanh thuần Việt: ưu/yêu, dài dòng/da dông — NOT_VERIFIED bằng tai người',
    'Lỗi thứ nhất, đọc bảng xếp hạng không có sai số, nên thấy chênh lệch ảo.':
        'ASR chép “Lỗi thứ nhất, đọc bản xếp hạng không có sai số, nên thấy trên là chảo.” (0.75): lệch âm/thanh thuần Việt: bảng/bản, chênh lệch ảo/trên là chảo — NOT_VERIFIED bằng tai người',
    'Lượng tử hoá lưu trọng số bằng ít bit hơn, 1 byte hay nửa byte thay vì 2 byte, nên tốn ít bộ nhớ và băng thông.':
        'ASR chép “Lượng tử hóa lưu trọng số bằng ít biết hơn, một bay hay nửa bay thay vì hai bay, nên tốn ít bộ nhớ và băng thông.” (0.852): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: bit/biết — NOT_VERIFIED bằng tai người',
    'Nếu mỗi từ được chấp nhận với xác suất alpha, số từ tố kỳ vọng mỗi lần kiểm bằng 1 trừ alpha mũ k cộng 1, chia 1 trừ alpha.':
        'ASR chép “Nếu mỗi từ được chấp nhận với sát xuất an pha, số từ tố kỳ vọng mỗi lần kiểm bằng 1 trừ an pha mũ ca cộng 1, chia 1 trừ an pha.” (0.825): alpha đọc thô (probe AIF p1: 7/8, bản chép “an pha / ANFA / α”); lệch âm/thanh thuần Việt: xác/sát — NOT_VERIFIED bằng tai người',
    'Lượng tử hoá trọng số của mô hình 6 phẩy 44 tỉ tham số từ 2 byte xuống 1 byte rồi nửa byte.':
        'ASR chép “Lượng tử hóa trọng số của mô hình 6,44 tỷ tham số từ hai bay xuống một bay rồi nửa bay.” (0.84): “tỉ” ASR viết chính tả “tỷ” (cùng âm); byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Giải mã suy đoán với k bằng 4 và alpha bằng 0 phẩy 8 cho khoảng 3 phẩy 36 từ tố mỗi lần mô hình lớn chạy.':
        'ASR chép “Giải mã suy đoán với ca bằng 4 và an pha bằng 0,8 cho khoảng 3,36 từ tố mỗi lần mô hình lớn chạy.” (0.949): alpha đọc thô (probe AIF p1: 7/8, bản chép “an pha / ANFA / α”) — NOT_VERIFIED bằng tai người',
    'Nửa byte mỗi tham số thường làm mô hình kém đi ở một số việc như toán hay viết mã.':
        'ASR chép “Nửa bay mỗi tham số thường là mô hình kém đi ở một số việc như toán hay viết mã.” (0.9): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: làm/là — NOT_VERIFIED bằng tai người',
    'Khi alpha thấp, phần lớn đề xuất bị bỏ, với alpha bằng 0 phẩy 6 và k bằng 4 chỉ được khoảng 2 phẩy 3 từ tố mỗi lần kiểm, mà vẫn tốn công chạy mô hình nhỏ.':
        'ASR chép “Khi an pha thấp, phần lớn đề xuất bị bỏ, với an pha bằng 0,6 và ca bằng 4 chỉ được khoảng 2,3 từ tố mỗi lần kiểm mà vẫn tốn công chạy mua hình nhỏ.” (0.897): alpha đọc thô (probe AIF p1: 7/8, bản chép “an pha / ANFA / α”); lệch âm/thanh thuần Việt: mô/mua — NOT_VERIFIED bằng tai người',
    'Hãy đo alpha trên đúng loại văn bản của ứng dụng.':
        'ASR chép “Hãy đo an pha trên đúng loại văn bản của ứng dụng.” (0.87): alpha đọc thô (probe AIF p1: 7/8, bản chép “an pha / ANFA / α”) — NOT_VERIFIED bằng tai người',
    'Câu hai, giải mã suy đoán với alpha bằng 0 phẩy 6 và k bằng 4, mỗi lần kiểm được khoảng bao nhiêu từ tố?':
        'ASR chép “Câu 2, giải mã suy đoán với an pha bằng 0,6 và ca bằng 4, mỗi lần kiểm được khoảng bao nhiêu từ tố?” (0.941): alpha đọc thô (probe AIF p1: 7/8, bản chép “an pha / ANFA / α”) — NOT_VERIFIED bằng tai người',
    # ── AGT L00–L11 (2026-10-31) ──
    'Lỗi ở nguồn S 2 chỉ bắt được khi kiểm câu trích có trong nguồn.':
        'ASR chép “Lỗi ở nguồn F2 chỉ bắt được khi kiểm câu trích có trong nguồn.” (0.933): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Đây đúng là công thức tỉ lệ nền theo định lý Bayes.':
        'ASR chép “Đây đúng là công thức tỷ lệ nên theo định lý bay S.” (0.769): “tỉ” ASR viết chính tả “tỷ” (cùng âm); Bayes đọc “Bay-ét” theo lexicon chung (probe 3/8, NOT_VERIFIED), ASR viết “bay X/S”; lệch âm/thanh thuần Việt: nền/nên — NOT_VERIFIED bằng tai người',
    'Bước thứ i, đếm từ 0, gửi S cộng G nhân i từ tố.':
        'ASR chép “Bước thứ Y, đếm từ 0, gửi S cộng Ve nhân Y từ tố.” (0.929): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Tác tử đọc lịch thì chỉ cần quyền đọc lịch.':
        'ASR chép “Tát tử độc lịch thì chỉ cần quyền độc lịch.” (0.7): lệch âm/thanh thuần Việt: tác/tát, đọc/độc, đọc/độc — NOT_VERIFIED bằng tai người',
    'Bảng tính độ tin cậy của các kiến trúc với số minh hoạ.':
        'ASR chép “Bản tính đầu tiên cậy của các kiến trúc với số minh họa.” (0.769): lệch âm/thanh thuần Việt: bảng/bản, độ tin/đầu tiên — NOT_VERIFIED bằng tai người',
    # ── ROB L00–L12 (2026-10-31) ──
    'Bước định vị mất 9 mi li giây.':
        'ASR chép “Bước định vị mất chính mi ly giây.” (0.75): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; lệch âm/thanh thuần Việt: chín/chính — NOT_VERIFIED bằng tai người',
    'Tổng là 16 mi li giây, dư 4 trong chu kỳ 1000 chia 50, bằng 20 mi li giây.':
        'ASR chép “Tổng là 16 mili dây, dự bốn trong chu kỳ 1000 chia 50 bằng 20 mili dây.” (0.727): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; lệch âm/thanh thuần Việt: dư (trong “mi li giây dư” → “mili dây dự”) — NOT_VERIFIED bằng tai người',
    'Vận tốc góc ô-mê-ga bằng hiệu tốc độ bánh phải trừ bánh trái, chia L, bánh phải nhanh hơn thì xe quay trái.':
        'ASR chép “Vận tốc cốc omega bằng hiệu tốc độ bánh phải trừ bánh trái, chia L, bánh phải nhanh hơn thì xe quay trái.” (0.875): ô-mê-ga (ω) đọc tách âm tiết, ASR viết “omega/ω”; lệch âm/thanh thuần Việt: góc (trong “góc ô mê ga” → “cốc omega”) — NOT_VERIFIED bằng tai người',
    'Bán kính quay R bằng v chia ô-mê-ga, và khi ô-mê-ga bằng 0 thì xe đi thẳng.':
        'ASR chép “Bán kính quay R bằng V chia Omega và khi Omega bằng không thì sẽ đi thẳng.” (0.737): ô-mê-ga (ω) đọc tách âm tiết, ASR viết “omega/ω”; lệch âm/thanh thuần Việt: xe/sẽ — NOT_VERIFIED bằng tai người',
    'Tư thế x, y, tê-ta thay đổi theo ba phương trình, x phẩy bằng v cos tê-ta, y phẩy bằng v sin tê-ta, tê-ta phẩy bằng ô-mê-ga, tức xe chỉ đi theo hướng đầu xe.':
        'ASR chép “Từ thế ít, ít, tê ta thay đổi theo 3 phương trình, ít phải bằng v cô sin tê ta, ít phải bằng v sin tê ta, tê ta phải bằng omega, tức xe chỉ đi theo hướng đầu xe.” (0.805): “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; ô-mê-ga (ω) đọc tách âm tiết, ASR viết “omega/ω”; lệch âm/thanh thuần Việt: bốn/từ, i/x, i (trong “i phẩy” → “x phải”) — NOT_VERIFIED bằng tai người',
    'Một vòng mất 2 pi chia ô-mê-ga, khoảng 15 phẩy 71 giây, đi quãng 2 pi R, khoảng 7 phẩy 85 mét.':
        'ASR chép “Một vòng mất 2P chia Omega khoảng 15,71 giây đi quảng 2P-R khoảng 7,85 mét.” (0.821): pi (π) ASR viết “P/π”; ô-mê-ga (ω) đọc tách âm tiết, ASR viết “omega/ω”; lệch âm/thanh thuần Việt: quãng/quảng — NOT_VERIFIED bằng tai người',
    'Công thức cho ô-mê-ga theo đơn vị ra-đi-an mỗi giây.':
        'ASR chép “Công thức cho omega theo đơn vị radian mỗi giây.” (0.667): ô-mê-ga (ω) đọc tách âm tiết, ASR viết “omega/ω”; ra-đi-an: probe RBM p1 8/8, ASR viết “radian/radiant” — NOT_VERIFIED bằng tai người',
    'Đưa vào hàm cos hay sin ở dạng độ, hay ra lệnh động cơ theo độ mỗi giây mà không đổi đơn vị, thì xe quay sai hẳn, vì 1 ra-đi-an xấp xỉ 57 phẩy 3 độ.':
        'ASR chép “Đưa vào hàm cô sinh hay sinh ở dạng độ, hay ra lệnh động cơ theo độ mỗi giây mà không đổi đơn vị, thì xe quay sai hẳn vì 1 ra đi an sắp xỉ 57,3 độ.” (0.929): sin đọc thô, ASR viết “sinh” (gần âm); lệch âm/thanh thuần Việt: xấp/sắp — NOT_VERIFIED bằng tai người',
    'Câu một, hai bánh cùng 0 phẩy 5 mét mỗi giây, L bằng 0 phẩy 5 mét, v và ô-mê-ga bằng bao nhiêu?':
        'ASR chép “Câu 1, 2 bánh cùng không phải 5 mét mỗi giây, L bằng không phải 5 mét, V và omega bằng bao nhiêu?” (0.833): “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; ô-mê-ga (ω) đọc tách âm tiết, ASR viết “omega/ω” — NOT_VERIFIED bằng tai người',
    'Câu hai, bánh trái âm 0 phẩy 3, bánh phải 0 phẩy 3 mét mỗi giây, v và ô-mê-ga bằng bao nhiêu?':
        'ASR chép “Câu 2, bánh trái âm 0,3, bánh phải 0,3 m每 giây về vào omega bằng bao nhiêu?” (0.8): đơn vị mét, ASR viết ký hiệu “m”; ô-mê-ga (ω) đọc tách âm tiết, ASR viết “omega/ω”; lệch âm/thanh thuần Việt: mỗi (trong “mét mỗi” → “m每”), và (trong “và ô mê ga” → “vào omega”) — NOT_VERIFIED bằng tai người',
    'Đáp án câu một, v bằng 0 phẩy 5 và ô-mê-ga bằng 0, nên xe đi thẳng.':
        'ASR chép “Đáp án câu 1 về bằng 0,5 và omega bằng 0 nên xe đi thẳng.” (0.889): ô-mê-ga (ω) đọc tách âm tiết, ASR viết “omega/ω” — NOT_VERIFIED bằng tai người',
    'Câu hai, v bằng 0 và ô-mê-ga bằng 0 phẩy 6 chia 0 phẩy 5, bằng 1 phẩy 2 ra-đi-an mỗi giây, nên xe quay tại chỗ sang trái.':
        'ASR chép “Câu 2, V bằng 0 và ω bằng 0,6 chia 0,5 bằng 1,2 radian mỗi giây, nền xe quay tại chỗ sang trái.” (0.839): ô-mê-ga (ω) đọc tách âm tiết, ASR viết “omega/ω”; ra-đi-an: probe RBM p1 8/8, ASR viết “radian/radiant”; lệch âm/thanh thuần Việt: nên/nền — NOT_VERIFIED bằng tai người',
    'Tổng kết lại, vận tốc tiến là trung bình hai bánh, vận tốc góc là hiệu hai bánh chia L, bán kính quay bằng v chia ô-mê-ga.':
        'ASR chép “Tổng cất lại, vận tốc tiếng là trung bình 2 bánh, vận tốc góc là hiệu 2 bánh chia L, bản kính quay bằng V chia omega.” (0.821): ô-mê-ga (ω) đọc tách âm tiết, ASR viết “omega/ω”; lệch âm/thanh thuần Việt: kết/cất, tiến/tiếng, bán/bản — NOT_VERIFIED bằng tai người',
    'Quãng mỗi xung bằng pi nhân D chia N, tức chu vi bánh chia số xung mỗi vòng.':
        'ASR chép “Quảng mổi sung bằng pi nhân dê chia n, tức chú vì bánh chia số sung mổi vòng.” (0.722): lệch âm/thanh thuần Việt: quãng mỗi/quảng mổi, chu vi/chú vì, mỗi/mổi — NOT_VERIFIED bằng tai người',
    'Góc quay bằng hiệu quãng bánh phải trừ bánh trái, chia L, tính bằng ra-đi-an, giống ô-mê-ga ở bài 1 nhân thời gian.':
        'ASR chép “Góc quay bằng hiệu quản bánh phải trừ bánh trái, chia L, tính bằng radiant, giống omega ở bài một nhân thời gian.” (0.8): ra-đi-an: probe RBM p1 8/8, ASR viết “radian/radiant”; ô-mê-ga (ω) đọc tách âm tiết, ASR viết “omega/ω”; lệch âm/thanh thuần Việt: quãng/quản — NOT_VERIFIED bằng tai người',
    'Bánh đường kính 0 phẩy 1 mét, 1000 xung mỗi vòng, nên mỗi xung khoảng 0 phẩy 314 mi li mét.':
        'ASR chép “Bánh đường kính 0,1m, 1000 xuống mỗi vòng, nền mỗi xuống khoảng 0,314mm.” (0.75): đơn vị mét, ASR viết ký hiệu “m”; đơn vị mi-li-mét, ASR viết ký hiệu “mm”; lệch âm/thanh thuần Việt: xung/xuống, nên/nền, xung/xuống — NOT_VERIFIED bằng tai người',
    'Bảng đổi số xung đếm được ra quãng.':
        'ASR chép “Bản đổi số xung đếm được ra quản.” (0.75): lệch âm/thanh thuần Việt: bảng/bản, quãng/quản — NOT_VERIFIED bằng tai người',
    'Bảng chấm ba phép đo khi khoảng cách thật là 2 mét và xích-ma bằng 0 phẩy 1 mét.':
        'ASR chép “Bản chấm 3 phép đo khi khoảng cách thật là 2m và sigma bằng 0,1m.” (0.769): đơn vị mét, ASR viết ký hiệu “m”; xích-ma (σ) đọc tách âm tiết, ASR viết “sigma”; lệch âm/thanh thuần Việt: bảng/bản — NOT_VERIFIED bằng tai người',
    'Ở bài sau, bài 4, ta học định vị bằng bộ lọc Bayes rời rạc và bộ lọc hạt.':
        'ASR chép “Ở bài sau, bài 4, ta học định vị bằng bộ lọc bay ếch rời rạc và bộ lọc hạt.” (0.95): Bayes đọc “Bay-ét” theo lexicon chung (probe 3/8, NOT_VERIFIED), ASR viết “bay X/S” — NOT_VERIFIED bằng tai người',
    'Thấy cửa lần nữa, ô 4 và ô 7 mỗi ô 0 phẩy 427, còn ô 0 và ô 1 chỉ 0 phẩy 053.':
        'ASR chép “Thấy cửa lần nữa, O4 và O7 mỗi ô không phải 427, còn O0 và O1 chỉ không phải 053.” (0.8): “ô” (ô lưới) ASR viết chữ “O”; “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải” — NOT_VERIFIED bằng tai người',
    'Trung bình của hai đỉnh ở ô 4 và ô 7 là ô 5 phẩy 5, chỗ mà robot gần như chắc chắn không ở.':
        'ASR chép “Trung bình của hai đỉnh ở O4 và O7 là O5.5, chỗ mà robot gần như chắc chắn không ở.” (0.857): “ô” (ô lưới) ASR viết chữ “O”; “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải” — NOT_VERIFIED bằng tai người',
    'Mô hình có ba phương trình, x phẩy bằng x cộng s cos tê-ta, y phẩy bằng y cộng s sin tê-ta, tê-ta phẩy bằng tê-ta, với s là quãng đi trong một bước.':
        'ASR chép “Mô hình có ba phương trình, x phải bằng x cộng s cos theta, y phải bằng y cộng s sin theta, theta phải bằng theta, với s là quảng đi trong một bước.” (0.789): “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: quãng/quảng — NOT_VERIFIED bằng tai người',
    'Ma trận có đường chéo bằng 1, cột thứ ba có âm s sin tê-ta và s cos tê-ta.':
        'ASR chép “Ma trận có đường cháo bằng một, cục thứ ba có âm S sinh tê ta và S co sinh tê ta.” (0.791): sin đọc thô, ASR viết “sinh” (gần âm); cos đọc “cô-sin” theo lexicon RBM/ROB, ASR viết “cô sinh/co sinh”; lệch âm/thanh thuần Việt: chéo/cháo, cột/cục — NOT_VERIFIED bằng tai người',
    'Với P là ma trận chéo 0 phẩy 01, tích F P F chuyển vị cho phương sai theo y bằng 0 phẩy 02, cùng tương quan 0 phẩy 01 giữa y và tê-ta.':
        'ASR chép “Với P là ma trận chéo 0.001, tích Fp F chuyển vị cho phương sai theo Y bằng 0.02, cùng tương quan 0.01 giữa Y và Teta.” (0.892): “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; tê-ta theo lexicon RBM/ROB, ASR viết “theta/teta”; lệch âm/thanh thuần Việt: không (trong “không phẩy” → “”) — NOT_VERIFIED bằng tai người',
    'Vì sao lần này không phải trục y?':
        'ASR chép “Vì sao lần này không phải trục ý?” (0.875): lệch âm/thanh thuần Việt: i/ý — NOT_VERIFIED bằng tai người',
    'Tổng kết lại, mô hình cong có cos và sin, nên ta lấy Jacobian tại ước lượng hiện tại.':
        'ASR chép “Tổng kết lại, mô hình công có cô sinh và sinh nên ta lấy gia cô biên tại ước lượng hiện tại.” (0.864): sin đọc thô, ASR viết “sinh” (gần âm); lệch âm/thanh thuần Việt: cong/công — NOT_VERIFIED bằng tai người',
    'Hôm nay ta học bản đồ lưới chiếm chỗ, mỗi ô một xác suất, cập nhật bằng phép cộng trên thang lôgarit tỉ số khả năng.':
        'ASR chép “Hôm nay ta học bản đồ lưới chiếm chỗ, mỗi ôm một xác xuất, cập nhật bằng phép cộng trên thang Logarith tỷ số khả năng.” (0.923): “ô” (ô lưới) ASR viết chữ “O”; “tỉ” ASR viết chính tả “tỷ” (cùng âm) — NOT_VERIFIED bằng tai người',
    'Sau 1 lần đo chiếm, l cộng 0 phẩy 847, p bằng 0 phẩy 7.':
        'ASR chép “Sau một lần đo chiếm, L cộng 0,847, T bằng 0,7.” (0.889): “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: không (trong “không phẩy” → “”) — NOT_VERIFIED bằng tai người',
    'Nếu chặn trị tuyệt đối của l không quá 3 phẩy 5, tức p không quá 0 phẩy 971, thì sau 6 lần quét trống xác suất đã còn 0 phẩy 744.':
        'ASR chép “Nếu chặn trị tuyệt đối của L không quá 3,5, tức tề không quá 0,971 thì sau 6 lần quét trống xác suất đã còn 0,744.” (0.921): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; lệch âm/thanh thuần Việt: không (trong “không phẩy” → “”), không (trong “không phẩy” → “”) — NOT_VERIFIED bằng tai người',
    'Cập nhật cả ô bị chiếm lẫn các ô tia đi qua, và chặn giá trị để bản đồ còn sửa được.':
        'ASR chép “Cập nhật cao bị chiếm lẫn các OT đi qua và chặn giá trị để bản đồ còn sửa được.” (0.857): “ô” (ô lưới) ASR viết chữ “O”; lệch âm/thanh thuần Việt: cả (trong “cả ô” → “cao”), tia (trong “ô tia” → “ot”) — NOT_VERIFIED bằng tai người',
    'Cạnh đóng vòng nói x j trừ x i xấp xỉ d, khi robot nhận ra nơi đã đến, nối hai nút xa nhau.':
        'ASR chép “Cảnh đóng vòng nói xy trừ xy sắp xỉ dê, khi robot nhận ra nơi đã đến, nối hai nút xa nhau.” (0.783): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: cạnh/cảnh, i xấp (trong “x i xấp” → “xy sắp”) — NOT_VERIFIED bằng tai người',
    'Tối ưu kéo mọi bước còn 0 phẩy 5 mét, cả bản đồ co lại một nửa.':
        'ASR chép “Tối yêu kéo mọi bước còn không phải 5 m, cả bản đồ có lại 1 nữa.” (0.706): “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; đơn vị mét, ASR viết ký hiệu “m”; lệch âm/thanh thuần Việt: ưu/yêu, co/có, nửa/nữa — NOT_VERIFIED bằng tai người',
    'Cạnh từ bánh xe trên sàn trơn kém tin cậy hơn cạnh từ quét khớp với tường.':
        'ASR chép “Cảnh từ bánh xe trên sàn trân kém tinh cậy hơn cảnh từ quét khớp với tương.” (0.706): lệch âm/thanh thuần Việt: cạnh/cảnh, trơn/trân, tin/tinh, cạnh/cảnh, tường/tương — NOT_VERIFIED bằng tai người',
    'Chỉ lưu một byte mỗi ô đã cần một nghìn tỉ byte.':
        'ASR chép “Chỉ lưu một bay mỗi ô đã cần 1 nghìn tỷ bay.” (0.75): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); “tỉ” ASR viết chính tả “tỷ” (cùng âm) — NOT_VERIFIED bằng tai người',
    'Đường từ các mẫu ngẫu nhiên thường ngoằn ngoèo.':
        'ASR chép “đường từ các mẫu ngẫu nhiên thường hoang ngoeo.” (0.778): lệch âm/thanh thuần Việt: ngoằn ngoèo/hoang ngoeo — NOT_VERIFIED bằng tai người',
    'Robot cần quyết định ngay trong chu kỳ này, đi tiếp, rẽ, hay chậm lại, với tốc độ mà bánh xe thật sự đạt được.':
        'ASR chép “Robo cần quyết định ngay trong chu kỳ này đi tiếp, rẻ hay chậm lại với tốc độ mà bánh xe thật sự đạt được.” (0.92): robot đọc thô (probe RBM p1: 7/8, r → tr/ro); lệch âm/thanh thuần Việt: rẽ/rẻ — NOT_VERIFIED bằng tai người',
    'Ô-mê-ga bằng v nhân ka-pa là vận tốc góc cần ra lệnh khi đi với tốc độ v.':
        'ASR chép “Omega bằng v nhân kappa là vận tốc góc cần ra lệnh khi đi với tốc độ v.” (0.821): ô-mê-ga (ω) đọc tách âm tiết, ASR viết “omega/ω”; ka-pa (κ) đọc tách âm tiết, ASR viết “kappa” — NOT_VERIFIED bằng tai người',
    'Đi 0 phẩy 5 mét mỗi giây với khoảng nhìn 2 mét thì ô-mê-ga bằng 0 phẩy 5 nhân 0 phẩy 25, bằng 0 phẩy 125 ra-đi-an mỗi giây.':
        'ASR chép “Đi 0,5 mét mỗi giây với khoảng nhìn 2 mét thì omega bằng 0,5 nhân 0,25, bằng 0,125 radian mỗi giây.” (0.861): ô-mê-ga (ω) đọc tách âm tiết, ASR viết “omega/ω”; “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; ra-đi-an: probe RBM p1 8/8, ASR viết “radian/radiant”; lệch âm/thanh thuần Việt: không (trong “không phẩy” → “”) — NOT_VERIFIED bằng tai người',
    'Câu hai, ô-mê-ga bằng 0 phẩy 6 nhân âm 0 phẩy 4, bằng âm 0 phẩy 24 ra-đi-an mỗi giây, âm nghĩa là quay phải.':
        'ASR chép “Câu 2, omega bằng 0,6 nhân âm 0,4, bằng âm 0,24 radian mỗi giây, âm nghĩa là quay phải.” (0.862): ô-mê-ga (ω) đọc tách âm tiết, ASR viết “omega/ω”; ra-đi-an: probe RBM p1 8/8, ASR viết “radian/radiant” — NOT_VERIFIED bằng tai người',
    'Tổng kết lại, chọn một điểm trên đường cách xe L, đổi sang hệ toạ độ của xe, rồi tính ka-pa bằng 2 y chia L bình phương và ô-mê-ga bằng v nhân ka-pa.':
        'ASR chép “Tổng kết lại, chọn một điểm trên đường cách xe L, đổi sang hệ tỏa độ của xe, rồi tính kappa bằng 2y chia L bình phương và omega bằng v nhân kappa.” (0.833): ka-pa (κ) đọc tách âm tiết, ASR viết “kappa”; ô-mê-ga (ω) đọc tách âm tiết, ASR viết “omega/ω”; lệch âm/thanh thuần Việt: toạ/toả — NOT_VERIFIED bằng tai người',
    'Ống kính góc rộng làm điểm ở mép ảnh lệch hàng chục điểm ảnh, nên phải hiệu chuẩn hệ số méo và khử méo trước khi dùng phép chiếu lỗ kim.':
        'ASR chép “Ông kính gốc động làm điểm ở mép ảnh là hàng chục điểm ảnh, nên phải hiệu chuẩn hệ số máu và khử máu trước khi dùng phép chiếu lộ kim.” (0.774): lệch âm/thanh thuần Việt: ống/ông, góc rộng/gốc động, lệch/là, méo/máu, méo/máu, lỗ/lộ — NOT_VERIFIED bằng tai người',
    'Quãng phanh với gia tốc a bằng v bình phương chia 2 a.':
        'ASR chép “Quảng Phanh với gia tốc A bằng với Bình Phương chia 2A.” (0.846): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: quãng/quảng — NOT_VERIFIED bằng tai người',
    # ── DEN L00–L13 (2026-10-31) ──
    'Hôm nay ta học tải giao dịch và tải phân tích, và vì sao cách xếp byte trên đĩa quyết định tốc độ.':
        'ASR chép “Hôm nay ta học tải giao dịch và tải phân tích, và vì sao cách xếp bay trên đĩa quyết định tốc độ.” (0.957): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Bảng đơn hàng có 100 triệu dòng, 50 cột, mỗi ô 8 byte, một số minh hoạ.':
        'ASR chép “Bảng đơn hàng có 100 triệu dòng, 50 cột, mỗi ô tám bay, một số minh họa.” (0.947): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Lưu theo cột chỉ đọc 3 cột, bằng 2 phẩy 4 GB.':
        'ASR chép “Lưu theo cục chỉ độc 3 cục bằng 2,4 GB.” (0.75): lệch âm/thanh thuần Việt: cột/cục, đọc/độc, cột/cục — NOT_VERIFIED bằng tai người',
    'Câu một, bảng 1 tỉ dòng, 20 cột, mỗi ô 4 byte.':
        'ASR chép “Câu một, bảng một tỷ dòng, hai mươi cục, mỗi ô bốn bay.” (0.769): “tỉ” ASR viết chính tả “tỷ” (cùng âm); byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: cột/cục — NOT_VERIFIED bằng tai người',
    'Câu hỏi dùng 2 cột, lưu theo hàng và theo cột phải đọc bao nhiêu GB?':
        'ASR chép “Câu hỏi dùng hai cục, lưu theo hàng và theo cục phải đọc bao nhiêu gigabyte?” (0.812): GB đọc “ghi-ga-byte” theo lexicon của khoá, ASR viết “GB/gigabyte”; lệch âm/thanh thuần Việt: cột/cục, cột/cục — NOT_VERIFIED bằng tai người',
    'Số byte phải đọc bằng số dòng nhân số cột dùng nhân kích thước, nên hãy tách hai hệ và chọn cách lưu theo tải.':
        'ASR chép “Số bai phải đọc bằng số dòng nhân số cuộc dùng nhân kích thước nên hãy tách 2 hệ và chọn cách lưu theo tải.” (0.92): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: cột/cuộc — NOT_VERIFIED bằng tai người',
    'Chào bạn, bạn đổi trạng thái một đơn hàng, chỉ 100 byte.':
        'ASR chép “Chào bạn, bạn đổi trạng thái một đơn hàng, chỉ một trăm bay.” (0.923): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Nhưng cơ sở dữ liệu dùng cây B ghi lại cả trang 4096 byte chứa đơn đó, nên đĩa ghi gấp 40 phẩy 96 lần điều bạn muốn.':
        'ASR chép “Nhưng cơ sở dữ liệu dùng cây B ghi lại cả trang 4096 bài chứa đơn đó nên địa ghi gấp 40,96 lần điều bạn muốn.” (0.946): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: đĩa/địa — NOT_VERIFIED bằng tai người',
    'Khuếch đại ghi là số byte ghi xuống đĩa chia số byte muốn ghi.':
        'ASR chép “Quét đại ghi là số bài ghi xuống địa chia số bài muốn ghi.” (0.714): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: khuếch/quét, đĩa/địa — NOT_VERIFIED bằng tai người',
    'Khuếch đại đọc là số lần đọc đĩa cho một lần tìm.':
        'ASR chép “Khuết đại độc là số lần độc địa cho một lần tim.” (0.583): lệch âm/thanh thuần Việt: khuếch/khuết, đọc/độc, đọc đĩa/độc địa, tìm/tim — NOT_VERIFIED bằng tai người',
    'Cây B sửa 100 byte trong trang 4096 byte, nên khuếch đại ghi bằng 4096 chia 100, tức 40 phẩy 96, chưa kể nhật ký.':
        'ASR chép “KB xử 100 bài trong trang 4.096 bài, nền khuết đại ghi bằng 4.096 chia 100, tức 40,96, chưa kể nhật ký.” (0.843): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: cây sửa (trong “cây b sửa” → “kb xử”), nên khuếch (trong “byte nên khuếch” → “bài nền khuết”) — NOT_VERIFIED bằng tai người',
    'Với gộp theo bậc, mỗi bậc gộp 4 tệp, 256 lần xả tạo 4 bậc.':
        'ASR chép “Với gột theo bật, mỗi bật gột 4 tệp, 256 lần xả tạo 4 bật.” (0.737): lệch âm/thanh thuần Việt: gộp/gột, bậc/bật, bậc gộp/bật gột, bậc/bật — NOT_VERIFIED bằng tai người',
    'Mỗi byte được ghi 1 lần vào nhật ký, 1 lần khi xả, và 4 lần khi gộp, tổng là 6 lần, toàn ghi tuần tự.':
        'ASR chép “Mỗi bay được ghi một lần vào nhật ký, một lần khi xả và bốn lần khi gột, tổng là 6 lần, toàn ghi tuần tự.” (0.923): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: gộp/gột — NOT_VERIFIED bằng tai người',
    'Mô hình gộp ở đây đơn giản hoá, mỗi byte bị ghi lại một lần ở mỗi bậc.':
        'ASR chép “Mua hình gột ở đây đơn giản hóa, mỗi bay bị ghi lại một lần ở mỗi bậc.” (0.833): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: mô/mua, gộp/gột — NOT_VERIFIED bằng tai người',
    'Gộp nhiều bậc vẫn ghi lại mỗi byte nhiều lần.':
        'ASR chép “Gục nhiều bậc vẫn ghi lại mỗi bai nhiều lần.” (0.8): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: gộp/gục — NOT_VERIFIED bằng tai người',
    'Lợi thế là các lần ghi tuần tự lớn, rất hợp với đĩa, không phải tổng số byte nhỏ hơn.':
        'ASR chép “Lợi thế là các lần ghi tuần tự lớn, rất hợp với địa, không phải tổng số ba nhỏ hơn.” (0.9): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: đĩa/địa — NOT_VERIFIED bằng tai người',
    'Câu một, trang 16384 byte, sửa bản ghi 128 byte, khuếch đại ghi của cây B là bao nhiêu?':
        'ASR chép “Câu 1, trang 16.384 bai, sửa bản ghi 128 bai, khuết đại ghi của cây B là bao nhiêu?” (0.9): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: khuếch (trong “byte khuếch” → “bai khuết”) — NOT_VERIFIED bằng tai người',
    'Một văn bản tối đa 16 MiB, tức 16 nhân 2 mũ 20, bằng 16777216 byte.':
        'ASR chép “Một văn bản tối đa 16 Mb, tức 16 nhân 2 mũ 20, bằng 16777216 bay.” (0.935): MiB đọc “mê-ga-byte” (quy ước OSY/DEN: cách nói thông dụng, màn hình giữ MiB, câu nêu rõ 2 mũ 20), ASR viết “MB”; byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Mỗi dòng hàng nhúng khoảng 200 byte, một số minh hoạ, nên làm tròn xuống thương được 83886 dòng, một đơn bình thường thừa sức.':
        'ASR chép “Mỗi dòng hàng nhúng khoảng 200 bay, một số minh họa, nên làm tròn xuống thương được 83.886 dòng, một đơn bình thường thừa sức.” (0.971): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Nhưng nhật ký truy cập của một khách, mỗi mục 1 nghìn byte, tăng mãi.':
        'ASR chép “nhưng nhật ký truy cập của một khách mỗi một một ngàn bay tăng mãi.” (0.867): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: mục/một — NOT_VERIFIED bằng tai người',
    'Thứ nào nhúng, thứ nào tham chiếu?':
        'ASR chép “Thử nào nhúng, thử nào tham chiếu.” (0.714): lệch âm/thanh thuần Việt: thứ/thử, thứ/thử — NOT_VERIFIED bằng tai người',
    'Ở bài sau, bài 5, ta học kho cột rộng, với cách thiết kế bảng theo truy vấn.':
        'ASR chép “Ở bài sau, bài 5, ta học khó cột động, với các thiết kế bản theo truy vấn.” (0.778): lệch âm/thanh thuần Việt: kho/khó, rộng/động, cách/các, bảng/bản — NOT_VERIFIED bằng tai người',
    'Chào bạn, một cảm biến ghi 100 byte mỗi giây, và khoá phân vùng là mã cảm biến.':
        'ASR chép “Chào bạn, một cảm biến ghi mục trăm bay mỗi giây và khóa phân vùng là mạ cảm biến.” (0.842): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: một/mục, mã/mạ — NOT_VERIFIED bằng tai người',
    'Câu một, thiết bị gửi 1000 byte mỗi 10 giây.':
        'ASR chép “Câu 1. Thiết bị gửi 1.000 bai mỗi 10 giây.” (0.909): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Phân vùng theo thiết bị và ngày nặng bao nhiêu MB, còn theo thiết bị và tháng 30 ngày thì sao?':
        'ASR chép “Phân vùng theo thiết bị và ngày nặng bao nhiêu megabyte, còn theo thiết bị và tháng 30 ngày thì sao?” (0.955): MB đọc “mê-ga-byte” theo lexicon của khoá, ASR viết “MB/megabyte” — NOT_VERIFIED bằng tai người',
    'Bảng này duyệt đồ thị lần lượt từng bước.':
        'ASR chép “Bán này duyệt đô thị lần lượt từng bước.” (0.778): lệch âm/thanh thuần Việt: bảng/bán, đồ/đô — NOT_VERIFIED bằng tai người',
    'Ghi đôi mất kỳ vọng bao nhiêu sự kiện?':
        'ASR chép “Gì đôi mất kỳ vọng bao nhiêu sự kiến?” (0.778): lệch âm/thanh thuần Việt: ghi/gì, kiện/kiến — NOT_VERIFIED bằng tai người',
    'Chào bạn, kho dữ liệu lưu 100 ngày đơn hàng trong tệp cột.':
        'ASR chép “Chào bạn, khó dữ liệu lưu 100 ngày đơn hàng trong tạp cục.” (0.786): lệch âm/thanh thuần Việt: kho/khó, tệp cột/tạp cục — NOT_VERIFIED bằng tai người',
    'Lỗi thứ nhất, quá nhiều tệp nhỏ, nên chi phí mở tệp lấn át.':
        'ASR chép “Lỗi thứ nhất, quá nhiều tẹp nhỏ nên chi phí mở tẹp lấn ác.” (0.786): lệch âm/thanh thuần Việt: tệp/tẹp, tệp/tẹp, át/ác — NOT_VERIFIED bằng tai người',
    'Luồng ghi mỗi phút một tệp vài trăm nghìn byte.':
        'ASR chép “Luồng ghi mỗi phút một tạp vài trăm nghìn bay.” (0.8): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: tệp/tạp — NOT_VERIFIED bằng tai người',
    '10 nghìn tệp, mỗi tệp 2 mi li giây để mở và đọc siêu dữ liệu, là 20 giây trước khi đọc byte dữ liệu nào.':
        'ASR chép “10.000 tập, mỗi tập 20 li dây để mở và đọc siêu dữ liệu là 20 giây trước khi đọc 3 dữ liệu nào.” (0.852): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: tệp/tập, tệp/tập — NOT_VERIFIED bằng tai người',
    'Gộp thành 100 tệp thì chỉ còn 0 phẩy 2 giây, nên hãy gộp tệp định kỳ.':
        'ASR chép “Gột thành 100 tập thì chỉ còn không phải 2 giây, nên hãy gột tập định kỳ.” (0.722): “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; lệch âm/thanh thuần Việt: gộp/gột, tệp/tập, gộp tệp/gột tập — NOT_VERIFIED bằng tai người',
    'Hãy lưu ở độ mịn dòng hàng, rồi dựng bảng tổng hợp từ đó.':
        'ASR chép “Hãy lưu ở độ miệng dòng hàng, đôi dựng bản tổng hợp từ đó.” (0.786): lệch âm/thanh thuần Việt: mịn/miệng, rồi/đôi, bảng/bản — NOT_VERIFIED bằng tai người',
    'Chào bạn, đường ống chạy đêm nối bảng giao dịch 1000 GB với bảng cửa hàng 1 GB trên 100 máy.':
        'ASR chép “Chào bạn, đường ống chạy đêm lối bản giao dịch 1000GB với bản cửa hàng 1GB trên 100 máy.” (0.87): lệch âm/thanh thuần Việt: nối bảng/lối bản, bảng/bản — NOT_VERIFIED bằng tai người',
    'Câu hai, không được, vì bảng 2 GB không vừa 1 GB bộ nhớ mỗi máy, nên phải xáo trộn, hoặc lọc bớt cột và dòng của bảng nhỏ trước.':
        'ASR chép “Câu 2, không được, vì bảng 2GB không vừa 1GB bộ nhớ mỗi máy, nên phải 6 trộn, hoặc lọc bớt cột và dòng của bảng nhỏ trước.” (0.967): lệch âm/thanh thuần Việt: xáo/sáu — NOT_VERIFIED bằng tai người',
    'Bạn đã đi qua hàng và cột, cây gộp theo nhật ký, khuếch đại, văn bản, khoá giá trị, cột rộng và đồ thị.':
        'ASR chép “Bạn đã đi qua hàng và cục, cây gục theo nhật ký, khuết đại, văn bản, khóa giá trị, cục động và đô thi.” (0.708): lệch âm/thanh thuần Việt: cột/cục, gộp/gục, khuếch/khuết, cột rộng/cục động, đồ thị/đô thi — NOT_VERIFIED bằng tai người',
    # ── CLC L00–L11 (2026-10-31) ──
    'Hôm nay ta học vùng và vùng sẵn sàng, các miền lỗi của đám mây, và cách tính lợi ích của dự phòng.':
        'ASR chép “Hôm nay ta học vùng và vùng sẵn sàng các miền lỗi của đám may và cách tính lợi íp của dự phong.” (0.87): lệch âm/thanh thuần Việt: mây/may, ích/íp, phòng/phong — NOT_VERIFIED bằng tai người',
    'Lưu trữ đối tượng đọc ghi cả đối tượng qua HTTP theo khoá, không sửa giữa chừng, và gần như không giới hạn dung lượng, hợp với ảnh, video, sao lưu, nhật ký và hồ dữ liệu.':
        'ASR chép “Lưu trữ đối tượng đọc ghi cả đối tượng qua Http theo khóa, không sửa giữa chân và gần như không giới hạn dung lượng, hợp với ảnh, video, sao lưu, nhật ký và hồ dữ liệu.” (0.973): lệch âm/thanh thuần Việt: chừng/chân — NOT_VERIFIED bằng tai người',
    'Muốn thêm một dòng vào tệp nhật ký 1 GB là phải ghi lại cả 1 GB.':
        'ASR chép “Muốn thêm một dòng vào tập nhật ký 1GB là phải ghi lại cả 1GB.” (0.941): lệch âm/thanh thuần Việt: tệp/tập — NOT_VERIFIED bằng tai người',
    'Hàm theo sự kiện là một đoạn mã chạy khi có sự kiện, như ảnh mới, yêu cầu HTTP, hay tin nhắn, và nhà cung cấp lo máy cùng việc co giãn.':
        'ASR chép “Hàm theo sự kiện là một đoạn mã chạy khi có sự kiện, như ảnh mới, yêu cầu Http, hay tin nhắn và nhà cung cấp lo máy cùng việc có giảng.” (0.938): lệch âm/thanh thuần Việt: co giãn/có giảng — NOT_VERIFIED bằng tai người',
    'GB giây bằng số lần gọi nhân thời gian mỗi lần tính bằng giây, nhân bộ nhớ cấp tính bằng GB, là đơn vị tính tiền chính.':
        'ASR chép “Gigabyte dây bằng số lần gọi nhân thời gian mỗi lần tính bằng dây, nhân bộ nhớ cấp tính bằng Gigabyte là đơn vị tính tiền chính.” (0.926): GB đọc “ghi-ga-byte” theo lexicon của khoá, ASR viết “GB/gigabyte” — NOT_VERIFIED bằng tai người',
    'GB giây bằng 10 mũ 6 nhân 0 phẩy 2 nhân 0 phẩy 5, bằng 100 nghìn.':
        'ASR chép “Gigabyte dây bằng 10 mũ 6 nhân 0.2 nhân 0.5, bằng 100.000.” (0.882): GB đọc “ghi-ga-byte” theo lexicon của khoá, ASR viết “GB/gigabyte”; “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải” — NOT_VERIFIED bằng tai người',
    'Tiền GB giây là 100 nghìn nhân đơn giá, khoảng 1 phẩy 67 đô la.':
        'ASR chép “Tiền Gigabyte dây là 100.000 nhân đơn giá, khoảng 1,67 đô la.” (0.944): GB đọc “ghi-ga-byte” theo lexicon của khoá, ASR viết “GB/gigabyte” — NOT_VERIFIED bằng tai người',
    'Hàm A gọi đồng bộ hàm B rồi ngồi chờ thì cả hai đều tính GB giây.':
        'ASR chép “Hàm A gọi đồng bộ hàm B, rồi ngồi chờ thì cả hai đều tính giga ba giây.” (0.914): GB đọc “ghi-ga-byte” theo lexicon của khoá, ASR viết “GB/gigabyte” — NOT_VERIFIED bằng tai người',
    'Câu một, 50 triệu lần mỗi tháng, mỗi lần 100 mi li giây, 1 GB, cùng đơn giá.':
        'ASR chép “Câu 1, 50 triệu lần mỗi tháng, mỗi lần 100 mili giây, 1 ghi gà vai, cùng đơn giá.” (0.837): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; GB đọc “ghi-ga-byte” theo lexicon của khoá, ASR viết “GB/gigabyte” — NOT_VERIFIED bằng tai người',
    'GB giây và tổng tiền là bao nhiêu?':
        'ASR chép “Ghi ga 3 giây và tổng tiền là bao nhiêu?” (0.9): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Đáp án câu một, 5 nhân 10 mũ 7 nhân 0 phẩy 1 nhân 1, bằng 5 triệu GB giây, khoảng 83 phẩy 33 đô la.':
        'ASR chép “Đáp án câu 1 5 nhân 10 mũ 7 nhân 0 phải 1 nhân 1 bằng 5 triệu gigabyte dây, khoảng 83,33 đô la.” (0.933): “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; GB đọc “ghi-ga-byte” theo lexicon của khoá, ASR viết “GB/gigabyte” — NOT_VERIFIED bằng tai người',
    'Tổng kết lại, tiền của hàm gồm GB giây cộng số lần gọi.':
        'ASR chép “Tổng kết lại, tiền của hàm gồm Gigabyte giấy cộng số lần gọi.” (0.846): GB đọc “ghi-ga-byte” theo lexicon của khoá, ASR viết “GB/gigabyte” — NOT_VERIFIED bằng tai người',
    'Bản sao đọc dùng để chia tải đọc, và có thể trễ vài giây.':
        'ASR chép “Bản sao độc dùng để chia tải độc và có thể trễ vai dây.” (0.786): lệch âm/thanh thuần Việt: đọc/độc, đọc/độc, vài/vai — NOT_VERIFIED bằng tai người',
    'Máy và hàm tính theo giờ và GB giây, hay bị quên vì máy thử quên tắt.':
        'ASR chép “Máy và hàm tính theo giờ và giga 3 giây, hay bị quên vì máy thử quên tắt.” (0.914): GB đọc “ghi-ga-byte” theo lexicon của khoá, ASR viết “GB/gigabyte” — NOT_VERIFIED bằng tai người',
    'Lưu trữ tính theo GB mỗi tháng và số lần đọc ghi, hay bị quên vì bản chụp cũ và nhật ký không có hạn xoá.':
        'ASR chép “Lưu trữ tính theo gigabyte mỗi tháng và số lần đọc ghi, hay bị quên vì bản chụp cũ và nhật ký không có hạn xóa.” (0.962): GB đọc “ghi-ga-byte” theo lexicon của khoá, ASR viết “GB/gigabyte” — NOT_VERIFIED bằng tai người',
    'Dữ liệu ra ngoài tính theo GB ra Internet và GB giữa các vùng, hay bị quên vì không thấy khi thử với ít người dùng.':
        'ASR chép “Giữ liệu ra ngoại tính theo GIGABY ra internet và GIGABY giữa các vùng hay bị quên vì không thấy khi thử với ít người dùng?” (0.885): GB đọc “ghi-ga-byte” theo lexicon của khoá, ASR viết “GB/gigabyte”; lệch âm/thanh thuần Việt: ngoài/ngoại — NOT_VERIFIED bằng tai người',
    'Lỗi thứ hai, đặt các dịch vụ nói chuyện nhiều với nhau ở khác vùng, nên trả tiền cho mỗi GB qua lại.':
        'ASR chép “Lỗi thứ 2, đặt các dịch vụ nói chuyện nhiều với nhau ở khác vùng nên trả tiền cho mỗi gigabyte qua lại.” (0.957): GB đọc “ghi-ga-byte” theo lexicon của khoá, ASR viết “GB/gigabyte” — NOT_VERIFIED bằng tai người',
    'Với cách làm đúng, mỗi lần đổi chỉ chạm 320 nghìn byte.':
        'ASR chép “Với cách làm đúng, mỗi lần đổi chỉ chạm 320.000 bai.” (0.933): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Một khoá mã hoá trực tiếp 1000 GB thì xoay khoá phải mã hoá lại 10 mũ 12 byte dữ liệu.':
        'ASR chép “Một khóa mã hóa trực tiếp 1000 GB thì xoay khóa phải mã hóa lại 10 mũ 12 by dữ liệu.” (0.957): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Dữ liệu không đổi một byte nào, chỉ có phong bì bọc khoá dữ liệu được làm lại bằng khoá chính mới.':
        'ASR chép “Giữ liệu không đổi một bay nào chỉ có phong bị bọc khóa giữ liệu được làm lại bằng khóa chính mới.” (0.909): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: bì/bị — NOT_VERIFIED bằng tai người',
    'Xoay khoá chính phải mã hoá lại bao nhiêu byte?':
        'ASR chép “Xoay khóa chính phải mã hóa lại bao nhiêu bay?” (0.9): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Đáp án câu một, 50 nghìn nhân 32, bằng 1 triệu 600 nghìn byte, khoảng 1 phẩy 6 MB.':
        'ASR chép “Đáp án câu 1, 50.000 nhân 32, bằng 1.600.000 bai, khoảng 1,6 megabyte.” (0.913): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); MB đọc “mê-ga-byte” theo lexicon của khoá, ASR viết “MB/megabyte” — NOT_VERIFIED bằng tai người',
    'Điều cần mang theo, thêm một tầng gián tiếp biến việc khó, như mã hoá lại 1000 GB, thành việc dễ, như mã hoá lại vài trăm nghìn byte.':
        'ASR chép “Điều cần mang theo, thêm một tầng gián tiếp biến việc khó, như mã hóa lại 1000GB, thành việc dễ, như mã hóa lại vài trăm nghìn byte.” (1.0): GB đọc “ghi-ga-byte” theo lexicon của khoá, ASR viết “GB/gigabyte” — NOT_VERIFIED bằng tai người',
    # ── WEB L00–L14 (2026-10-31) ──
    'Phần lớn thời gian chờ không phải để tải byte, mà để đi và về nhiều lượt trước khi byte đầu tiên tới.':
        'ASR chép “Phần lớn thời gian chờ không phải để tải bay, mà để đi và về nhiều lượt trước khi bay đầu tiên tới.” (0.913): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Câu một, người dùng ở xa, vòng khứ hồi 200 mi li giây.':
        'ASR chép “Câu 1. Người dùng ở xa vòng khứ hội 200 mê lý dây.” (0.786): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; lệch âm/thanh thuần Việt: hồi/hội — NOT_VERIFIED bằng tai người',
    'Kết nối mới tốn bao lâu trước byte đầu tiên?':
        'ASR chép “Kết nối mới tốn bao lâu trước bay đầu tiên.” (0.9): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Đáp án câu một, 3 nhân 200, bằng 600 mi li giây.':
        'ASR chép “Đáp án câu 1, 3 nhìn 200 bằng 600 mê lý dây.” (0.786): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; lệch âm/thanh thuần Việt: nhân/nhìn — NOT_VERIFIED bằng tai người',
    'Khác nhau nằm ở thẻ HTML viết bên dưới.':
        'ASR chép “Khác nhau nằm ở thẻ html viết bên dưới.” (1.0): HTML đọc “hát tê em eo” theo lexicon WEB, ASR viết “html/HT ML” — NOT_VERIFIED bằng tai người',
    'Cây có 4 phần tử và độ sâu 3, đếm bằng một bộ đọc HTML có sẵn.':
        'ASR chép “Cây có 4 phần tử và độ sâu 3, đếm bằng một bộ độc HT ML có sẵn.” (0.857): HTML đọc “hát tê em eo” theo lexicon WEB, ASR viết “html/HT ML”; lệch âm/thanh thuần Việt: đọc (trong “đọc html” → “độc ht ml”) — NOT_VERIFIED bằng tai người',
    'Cỡ chữ là việc của phần kiểu dáng.':
        'ASR chép “Cở chữ là việc của phần kiểu dán.” (0.75): lệch âm/thanh thuần Việt: cỡ/cở, dáng/dán — NOT_VERIFIED bằng tai người',
    'Mô hình hộp đi từ trong ra ngoài, gồm nội dung, đệm, viền, và lề ngoài.':
        'ASR chép “Mua hình hộp đi tự trong trang ngoại, gồm nội dung, đệm, viên và lề ngoài” (0.688): lệch âm/thanh thuần Việt: mô/mua, từ/tự, ra ngoài/trang ngoại, viền/viên — NOT_VERIFIED bằng tai người',
    'Bộ chọn theo tên thẻ đếm vào cột 3.':
        'ASR chép “Bộ chọn theo tinh thẻ đếm vào cục 3.” (0.778): lệch âm/thanh thuần Việt: tên/tinh, cột/cục — NOT_VERIFIED bằng tai người',
    'Chào bạn, bạn hẹn giờ một việc sau 0 mi li giây, rồi chạy một vòng lặp tính toán 200 mi li giây.':
        'ASR chép “Chào bạn, bạn hẹn giờ một việc sau không mê ly giây, rồi chạy một vòng lập tính toán 200 mê ly giây.” (0.792): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; lệch âm/thanh thuần Việt: lặp/lập — NOT_VERIFIED bằng tai người',
    'Vòng lặp 200 mi li giây chặn mọi thứ, hẹn giờ 0 mi li giây phải chạy sau khoảng 200 mi li giây, bấm nút không phản hồi, và màn hình không vẽ lại.':
        'ASR chép “Vòng lập 200 mili dây chặn mọi thứ, hẹn giờ 0 mili dây phải chạy sau khoảng 200 mili dây, bấm nút không phản hồi và màn hình không vẽ lại.” (0.754): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; lệch âm/thanh thuần Việt: lặp/lập — NOT_VERIFIED bằng tai người',
    'Hẹn 1000 mi li giây nghĩa là ít nhất 1000 mi li giây, và trình duyệt còn giãn hẹn giờ của các thẻ đang ở nền.':
        'ASR chép “Hẹn 1 nghìn mili dây nghĩa là ít nhất 1 nghìn mili dây và trình việc còn giãn hẹn giờ của các thể đang ở nền.” (0.741): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; lệch âm/thanh thuần Việt: duyệt/việc, thẻ/thể — NOT_VERIFIED bằng tai người',
    'Đoạn mã in A, hẹn giờ in B, nối hai bước sau lời hứa để in C rồi D, xếp thẳng một tác vụ vi mô in E, rồi in F.':
        'ASR chép “Đoạn mã in A, hẹn giờ in B, nối hai bước sau lời hứa để in C rồi G, xếp thẳng một tác vụ vi mô in E, rồi in F.” (0.968): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Thứ tự in ra là gì, biết rằng D chỉ được xếp hàng sau khi C chạy xong?':
        'ASR chép “Thứ tự in ra là gì? Biết rằng ve chỉ được xếp hàng sau khi xe chạy sống.” (0.889): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: xong/sống — NOT_VERIFIED bằng tai người',
    'Kết quả là A, F, C, E, D, B, đúng như khi chạy thật.':
        'ASR chép “Kết quả là A, F, C, E, G, B, đúng như khi chạy thật.” (0.929): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Phần phụ thuộc thì chờ tuần tự, phần độc lập thì chạy đồng thời, lỗi từng phần thì dùng chờ tất cả đã ngã ngũ, và luôn giới hạn số yêu cầu cùng lúc.':
        'ASR chép “Phân phụ thuộc thi chờ tuần tự, phân độc lập thi chạy đồng thơi, lỗi từng phân thi dùng chờ tất cả đã ngã ngủ, và luôn giới hạn số yêu cầu cùng lúc.” (0.765): lệch âm/thanh thuần Việt: phần/phân, thì/thi, phần/phân, thì/thi, thời/thơi, phần thì/phân thi, ngũ/ngủ — NOT_VERIFIED bằng tai người',
    'Chào bạn, trong danh sách việc cần làm, bạn tích ô mua sữa ở dòng đầu.':
        'ASR chép “Chào bạn! Trong danh sách việc cần làm, bạn tích ôm mua sữa ở dòng đâu?” (0.875): “ô” (ô lưới) ASR viết chữ “O”; lệch âm/thanh thuần Việt: đầu/đâu — NOT_VERIFIED bằng tai người',
    'Viết vị trí cũ theo thứ tự mới, C ở 2, A ở 0, B ở 1, D ở 3, E ở 4.':
        'ASR chép “Viết vị trí của theo thứ tự mới C ở 2, A ở 0, B ở 1, G ở 3, E ở 4.” (0.913): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: cũ/của — NOT_VERIFIED bằng tai người',
    'Dãy vị trí cũ là gì, và cần di chuyển mấy dòng?':
        'ASR chép “giải vị trí củ là gì và cần di chuyển máy dòng.” (0.75): lệch âm/thanh thuần Việt: dãy/giải, cũ/củ, mấy/máy — NOT_VERIFIED bằng tai người',
    'GET đọc đơn 42, an toàn và lũy đẳng.':
        'ASR chép “ghét đọc đơn 42, an toàn và lủy đẳng.” (0.818): GET đọc “gét” theo lexicon WEB, ASR viết “ghét”; lệch âm/thanh thuần Việt: luỹ/luỷ — NOT_VERIFIED bằng tai người',
    'POST tạo một đơn mới, không an toàn và không lũy đẳng.':
        'ASR chép “Poster tạo một đơn mới, không an toàn và không lũy đẳng.” (0.917): POST đọc “pâu-xt” theo lexicon WEB, ASR viết “poster” — NOT_VERIFIED bằng tai người',
    'Lỗi thứ hai, dùng GET để thay đổi dữ liệu, nên máy đi trước tự bấm thay người.':
        'ASR chép “Lội thứ 2 dùng ghét để thay đổi giữ liệu nên máy đi trước tự bấm thay người.” (0.889): GET đọc “gét” theo lexicon WEB, ASR viết “ghét”; lệch âm/thanh thuần Việt: lỗi/lội — NOT_VERIFIED bằng tai người',
    'Trình duyệt tải trước liên kết, công cụ quét, và bộ nhớ đệm đều có quyền gọi GET bất cứ lúc nào.':
        'ASR chép “Trình duyệt tải trước liên kết, công cụ quát và bộ nhớ đệm đều có quyền gọi ghét bất cứ lúc nào.” (0.909): GET đọc “gét” theo lexicon WEB, ASR viết “ghét”; lệch âm/thanh thuần Việt: quét/quát — NOT_VERIFIED bằng tai người',
    'Còn POST thanh toán gửi hai lần thì sao?':
        'ASR chép “Còn poster thanh toán gửi 2 lần thì sao?” (0.889): POST đọc “pâu-xt” theo lexicon WEB, ASR viết “poster” — NOT_VERIFIED bằng tai người',
    'Còn POST thanh toán có thể trừ tiền hai lần, nên cần khoá lũy đẳng.':
        'ASR chép “Còn poster thanh toán có thể trừ tiền hai lần nên cần khóa lũy đẳng.” (0.933): POST đọc “pâu-xt” theo lexicon WEB, ASR viết “poster” — NOT_VERIFIED bằng tai người',
    'Chào bạn, mỗi lần mở ứng dụng, trình duyệt tải lại biểu trưng, phông chữ và tệp kịch bản, hàng trăm KB không đổi từ tuần trước.':
        'ASR chép “Chào bạn, mỗi lần mở ứng dụng, trình duyệt tải lại biểu trưng, phong chữ và tệp kịch bản 100KB không đổi từ tuần trước.” (0.926): lệch âm/thanh thuần Việt: phông/phong, hàng/một — NOT_VERIFIED bằng tai người',
    'Bảng có ba tình huống, với trang 50 KB và thời gian tươi 600 giây.':
        'ASR chép “Bạn có 3 tình huống với tràn 50 kb và thời gian từ 600 giây.” (0.824): lệch âm/thanh thuần Việt: bảng/bạn, trang/tràn, tươi/từ — NOT_VERIFIED bằng tai người',
    'Bản lưu 700 giây tuổi đã cũ, trình duyệt hỏi kèm thẻ v 7, máy chủ vẫn là v 7 nên trả 304, chỉ vài trăm byte tiêu đề.':
        'ASR chép “Bảng lưu 700 dây tuổi đã cũ, trình duyệt hỏi kèm thể V7, máy chủ vẫn là V7 nên trả 304, chỉ vài trăm bay tiêu đề.” (0.909): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: bản/bảng, thẻ/thể — NOT_VERIFIED bằng tai người',
    'Nếu máy chủ đã là v 8 thì trả 200 kèm thân mới, 50 KB.':
        'ASR chép “Nếu máy chủ đã là V8 thì trả 200 kèm thân mới, 50 kilobytes.” (0.941): KB đọc “ki-lô-byte” theo lexicon của khoá, ASR viết “kilobyte/kg” — NOT_VERIFIED bằng tai người',
    'Như vậy ngay cả khi đã cũ, trình duyệt cũng không tải lại 50 KB nếu nội dung chưa đổi.':
        'ASR chép “Như vậy, ngay cả khi đã cũ, trình duyệt cũng không tải lại 50KB nếu nội dung chưa đổi.” (1.0): KB đọc “ki-lô-byte” theo lexicon của khoá, ASR viết “KB/kilobyte” — NOT_VERIFIED bằng tai người',
    'Lỗi thứ nhất, cho trang HTML tươi rất lâu, nên người dùng kẹt ở bản cũ.':
        'ASR chép “Lỗi thứ nhất, cho trang HT MLT rất lâu nên người dùng kẹt ở bản cũ.” (0.875): HTML đọc “hát tê em eo” theo lexicon WEB, ASR viết “html/HT ML”; lệch âm/thanh thuần Việt: tươi (trong “html tươi” → “ht mlt”) — NOT_VERIFIED bằng tai người',
    'Trang HTML là điểm vào, trỏ tới mọi tệp khác.':
        'ASR chép “Trang html là điểm vào, trỏ tới mọi tệp khác.” (1.0): HTML đọc “hát tê em eo” theo lexicon WEB, ASR viết “html/HT ML” — NOT_VERIFIED bằng tai người',
    'Trang HTML luôn xác thực lại, còn tệp có mã băm trong tên thì lưu lâu.':
        'ASR chép “Trang html luôn xác thực lại, còn tệp có mã băm trong tên thì lưu lâu.” (1.0): HTML đọc “hát tê em eo” theo lexicon WEB, ASR viết “html/HT ML” — NOT_VERIFIED bằng tai người',
    'Khách hàng dùng điện thoại tầm trung, mạng di động yếu khoảng 200 KB mỗi giây, nên chỉ riêng 2 MB mã kịch bản đã mất 10 giây để tải, chưa kể thời gian máy yếu chạy nó.':
        'ASR chép “Khách hàng dùng điện thoại tầm trung màng di động yếu khoảng 200 kilobyte mỗi giây nên chỉ riêng 2 MB mà kịch bản đã mất 10 giây để tải chưa kể thời gian máy yếu chạy nó.” (0.923): KB đọc “ki-lô-byte” theo lexicon của khoá, ASR viết “kilobyte/kg”; lệch âm/thanh thuần Việt: mạng/màng, mã/mà — NOT_VERIFIED bằng tai người',
    'Hôm nay ta học hiệu năng web, byte nào chặn màn hình hiện ra, và cách cắt bớt.':
        'ASR chép “Hôm nay ta học hiệu năng huếp, vai nào chặn màn hình hiện ra và cách cắt bớt.” (0.889): web đọc thô (probe NET p2: 8/8), lần này ASR viết sai; byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Độ xê dịch bố cục đo việc nội dung nhảy chỗ khi đang đọc, tốt khi không quá 0 phẩy 1.':
        'ASR chép “Độ xây dịch bố cục đó việc nội dung nhảy chỗ khi đang đọc, tốt khi không quá không phải một.” (0.857): “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; lệch âm/thanh thuần Việt: xê/xây, đo/đó — NOT_VERIFIED bằng tai người',
    'Bảng so hai bản mã kịch bản trên mạng 200 KB mỗi giây.':
        'ASR chép “Bản so 2 bản mả kịch bản trên mạng 200 kb mũi dây.” (0.786): lệch âm/thanh thuần Việt: bảng/bản, mã/mả, mỗi/mũi — NOT_VERIFIED bằng tai người',
    'Sau khi nén, bỏ mã không dùng, tách theo trang, và tải phần còn lại sau, chỉ còn 500 KB, tải mất 2 phẩy 5 giây.':
        'ASR chép “Sau khi nén, bỏ mã không dùng, tách theo trang và tải phần còn lại sau chỉ còn 500 kilobyte tại mức 2,5 giây.” (0.889): KB đọc “ki-lô-byte” theo lexicon của khoá, ASR viết “kilobyte/kg”; lệch âm/thanh thuần Việt: tải mất (trong “kb tải mất” → “kilobyte tại mức”) — NOT_VERIFIED bằng tai người',
    'HTML trỏ tới tệp kiểu dáng, tệp kiểu dáng mới trỏ tới phông chữ, nên 3 lần tải nối tiếp nhân 100 mi li giây khứ hồi là 300 mi li giây trước khi chữ hiện.':
        'ASR chép “HT em eo trọ tới tệp kiểu dán, tệp kiểu dán mới trọ tới phong chữ. Nên 3 lần tại nối tiếp nhân 100 mili giây khứ hội là 300 mili giây trước khi chữ hiện.” (0.709): HTML đọc “hát tê em eo” theo lexicon WEB, ASR viết “html/HT ML”; tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; lệch âm/thanh thuần Việt: trỏ/trọ, dáng/dán, dáng/dán, trỏ/trọ, phông/phong, tải/tại, hồi/hội — NOT_VERIFIED bằng tai người',
    'Câu một, trang có 1 phẩy 2 MB tài nguyên chặn hiển thị, mạng 150 KB mỗi giây.':
        'ASR chép “Câu 1, tràn có 1,2 megabyte tài nguyên chặn hiển thị mạng 150 kilobyte mỗi giây.” (0.857): MB đọc “mê-ga-byte” theo lexicon của khoá, ASR viết “MB/megabyte”; KB đọc “ki-lô-byte” theo lexicon của khoá, ASR viết “kilobyte/kg”; lệch âm/thanh thuần Việt: trang/tràn — NOT_VERIFIED bằng tai người',
    'Câu hai, muốn tải xong trong 2 phẩy 5 giây trên mạng đó, tổng tài nguyên chặn hiển thị tối đa bao nhiêu KB?':
        'ASR chép “Câu 2, muốn tải xong trong 2,5 giây trên mạng đó, tổng tài nguyên chặn hiển thị tối đa bao nhiêu kilobyte?” (0.958): KB đọc “ki-lô-byte” theo lexicon của khoá, ASR viết “kilobyte/kg” — NOT_VERIFIED bằng tai người',
    'Câu hai, 2 phẩy 5 nhân 150, bằng 375 KB, đó là ngân sách cho mọi thứ trên đường kết xuất quan trọng.':
        'ASR chép “Câu 2, 2,5 nhân 150 bằng 375 kilobyte đó là ngân sách cho mọi thứ trên đường kết xúc quan trọng.” (0.933): KB đọc “ki-lô-byte” theo lexicon của khoá, ASR viết “kilobyte/kg”; lệch âm/thanh thuần Việt: xuất/xúc — NOT_VERIFIED bằng tai người',
    'Hãy cắt byte trên đường kết xuất quan trọng, báo trước tài nguyên, giữ chỗ cho ảnh, đo người dùng thật, và đặt ngân sách.':
        'ASR chép “Hãy các bài trên đường kết xúc quan trọng, báo trước tài nguyên, giữ chỗ cho ảnh, đo người dùng thật và đặt ngân sách.” (0.88): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: cắt (trong “cắt byte” → “các bài”), xuất/xúc — NOT_VERIFIED bằng tai người',
    'Ô nhập sai chỉ đổi viền đỏ, trong khi khoảng 8 phần trăm nam giới có rối loạn sắc giác đỏ lục.':
        'ASR chép “Ôn nhập sai chỉ đổi viền đỏ, trong khi khoảng 8% nam giới có trối loạn sắc giác đỏ lụt.” (0.864): “ô” (ô lưới) ASR viết chữ “O”; lệch âm/thanh thuần Việt: rối/trối, lục/lụt — NOT_VERIFIED bằng tai người',
    'Đọc một tệp mất 50 mi li giây ngay trên luồng giao diện ở 60 héc chiếm chỗ của khoảng 3 khung, nên danh sách đang cuộn khựng lại.':
        'ASR chép “Đọc một tờ mất 50 mili dây ngay trên luồn giao diện ở 60 hét chiếm chỗ của khoảng 3 khung, nền danh sách đang cuộn khựng lại.” (0.787): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; lệch âm/thanh thuần Việt: tệp/tờ, luồng/luồn, héc/hét, nên/nền — NOT_VERIFIED bằng tai người',
    'Câu một, mỗi khung, luồng giao diện mất 12 mi li giây.':
        'ASR chép “Câu 1, mỗi khung luôn giao diện mất 12ml.” (0.75): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; lệch âm/thanh thuần Việt: luồng/luôn — NOT_VERIFIED bằng tai người',
    # ── BCH L00–L11 (2026-10-31) ──
    'Khối 3 là B trả C 2, mã bắt đầu bằng a d c 7.':
        'ASR chép “Khối 3 là B trả C2 mà bắt đầu bằng A, V, C7.” (0.867): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: mã/mà — NOT_VERIFIED bằng tai người',
    'Ở bài sau, bài 2, ta học cây Merkle và bằng chứng thuộc về.':
        'ASR chép “Ở bài sau, bài hai, ta học cây mơ cổ và bằng chứng thuộc về.” (0.933): Merkle đọc “Mơ-cồ” theo lexicon BCH, ASR viết “mơ cổ” — NOT_VERIFIED bằng tai người',
    'Với cây Merkle, ví chỉ cần 10 mã băm, tức 320 byte, cộng với gốc của khối, là kiểm được.':
        'ASR chép “Với cây mơ cổ, ví chỉ cần 10 mả băm, tức 320 bay, cộng với gốc của khối là kiểm được.” (0.875): Merkle đọc “Mơ-cồ” theo lexicon BCH, ASR viết “mơ cổ”; byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: mã/mả — NOT_VERIFIED bằng tai người',
    'Hôm nay ta học cây Merkle, cách tóm tắt n giao dịch bằng một gốc, và chứng minh một giao dịch thuộc về bằng lôgarit cơ số 2 của n mã băm.':
        'ASR chép “Hôm nay ta học cây mơ cổ, cách tóm tắt n giao dịch bằng một gốc và chứng minh một giao dịch thuộc về bằng logarith cơ số 2 của n mã băm.” (0.97): Merkle đọc “Mơ-cồ” theo lexicon BCH, ASR viết “mơ cổ” — NOT_VERIFIED bằng tai người',
    'Số tầng trên lá là lôgarit cơ số 2 của 1024, bằng 10.':
        'ASR chép “Số tầng trên lá là Logar Tricker số 2 của 1024, bằng 10.” (0.895): lệch âm/thanh thuần Việt: lôgarit cơ/logar tricker — NOT_VERIFIED bằng tai người',
    'Bằng chứng cho giao dịch 357 gồm 10 mã, mỗi mã 32 byte, tổng 320 byte.':
        'ASR chép “bằng chứng cho giao dịch 357 gồm 10 mã, mỗi mã 32 bay, tổng 320 bay.” (0.92): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Hãy thêm tiền tố khác nhau trước khi băm, một byte 0 cho lá và một byte 1 cho nút trong, như tiêu chuẩn minh bạch chứng chỉ.':
        'ASR chép “Hãy thêm tiền tố khác nhau trước khi băm, một bai không cho lá và một bai một cho nút trong, như tiêu chuẩn minh bạch chứng chỉ.” (0.929): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Cây Merkle thường chỉ chứng minh một phần tử có trong cây.':
        'ASR chép “Cây mơ cổ thường chỉ chứng minh một phần tử có trong cây.” (0.923): Merkle đọc “Mơ-cồ” theo lexicon BCH, ASR viết “mơ cổ” — NOT_VERIFIED bằng tai người',
    'Bằng chứng cần bao nhiêu mã băm, và bao nhiêu byte?':
        'ASR chép “bằng chứng cần bao nhiêu mã băm và bao nhiêu bay.” (0.909): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Đáp án câu một, 2 mũ 19 nhỏ hơn một triệu, còn 2 mũ 20 thì không nhỏ hơn, nên cần 20 mã, nhân 32, bằng 640 byte.':
        'ASR chép “Đáp án câu 1, 2 mũ 19 nhỏ hơn 1 triệu, còn 2 mũ 20 thì không nhỏ hơn, nên cần 20 mã, nhần 32, bằng 643.” (0.944): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: nhân/nhần — NOT_VERIFIED bằng tai người',
    'Khoá công khai gồm e và n, ai cũng có, dùng để kiểm xem s mũ e chia lấy dư cho n có bằng h không.':
        'ASR chép “Hóa công khai gồm E và N, ai cũng có, dùng để kiểm xem F mũ E chi lấy dư cho N có bằng hát không?” (0.885): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: khoá/hoá, chia/chi — NOT_VERIFIED bằng tai người',
    'Với chữ ký đường cong elip, chỉ cần dùng lại số ngẫu nhiên khi ký là đủ để tính ra khoá bí mật.':
        'ASR chép “Với chữ ký đường công Elite, chỉ cần dùng lại số ngẫu nhiên khi ký là đủ để tính ra khóa bí mật.” (0.913): lệch âm/thanh thuần Việt: cong elip/công elite — NOT_VERIFIED bằng tai người',
    'Người kiểm tính s mũ 17 chia lấy dư cho 3233 thì ra bao nhiêu nếu chữ ký đúng?':
        'ASR chép “Người kiểm tính F mũ 17 chia lấy dư cho 3233 thì ra bao nhiêu nếu chữ ký đúng?” (0.962): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Xác suất chưa trúng sau đúng 2 mũ 16 lần là 1 trừ 2 mũ âm 16, mũ 65536, xấp xỉ 1 chia e, khoảng 0 phẩy 368.':
        'ASR chép “Xác suất chưa trúng sau đúng 2 mũ 16 lần là 1 trừ 2 mũ âm 16, mũ 65536, sắp xỉ 1 GE, khoảng 0,368.” (0.914): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; lệch âm/thanh thuần Việt: xấp/sắp, chia (trong “chia e” → “ge”), không (trong “không phẩy” → “”) — NOT_VERIFIED bằng tai người',
    'Hôm nay ta học đồng thuận theo chuỗi nhiều công nhất, và công thức tính xác suất kẻ tấn công đuổi kịp sau z khối.':
        'ASR chép “Hôm nay ta học đồng thuận theo chuổi nhiều công nhất và công thức tính xác xuất kẻ tấn công đuổi kịp sau giá khối.” (0.92): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: chuỗi/chuổi — NOT_VERIFIED bằng tai người',
    'Lỗi thứ ba, dùng bảng xấp xỉ như con số chính xác, nên đánh giá thấp rủi ro.':
        'ASR chép “Lội thứ 3, dùng bản sắp xỉ như con số chính xác, nên đánh giá thấp rũi ro.” (0.778): lệch âm/thanh thuần Việt: lỗi/lội, bảng xấp/bản sắp, rủi/rũi — NOT_VERIFIED bằng tai người',
    'Tổng kết lại, mỗi nút theo chuỗi có tổng công lớn nhất, nên kẻ tấn công phải đuổi kịp z khối.':
        'ASR chép “Tổng kết lại, mỗi nút theo chuỗi có tổng công lớn nhất, nên kẻ tấn công phải đuổi kịp giá khối.” (0.952): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Bảng so hai thứ tự trong hàm rút tiền.':
        'ASR chép “Bản so 2 thứ tự trong hàm rút tiên.” (0.778): lệch âm/thanh thuần Việt: bảng/bản, tiền/tiên — NOT_VERIFIED bằng tai người',
    'Thêm khoá chống gọi lồng nếu cần.':
        'ASR chép “thêm khóa chóng gọi lòng nếu cần.” (0.714): lệch âm/thanh thuần Việt: chống/chóng, lồng/lòng — NOT_VERIFIED bằng tai người',
    'Một chuỗi khối với khối 1 MB mỗi 10 phút, giao dịch trung bình 250 byte, chỉ được khoảng 6 phẩy 7 giao dịch mỗi giây, cho cả thế giới.':
        'ASR chép “Một chuỗi khối với khối 1 MB mỗi 10 phút, giao dịch trung bình 253 chỉ được khoảng 6,7 giao dịch mỗi giây cho cả thế giới.” (0.97): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Trên chuỗi chỉ còn vài byte mỗi giao dịch, cộng bằng chứng cho cả lô.':
        'ASR chép “Trên chuỗi chỉ còn vài bay mỗi giao dịch, cộng bằng chứng cho cả lô.” (0.933): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Chuỗi gốc có khối 1 MB mỗi 600 giây, giao dịch 250 byte, nên thông lượng bằng 10 mũ 6 chia 250 nhân 600, khoảng 6 phẩy 7 giao dịch mỗi giây.':
        'ASR chép “Chủy gốc có khối 1 MB mỗi 600 giây, giao dịch 250 bai, nên thông lượng bằng 10 mũ 6 chia 250 nhân 600, khoảng 6,7 giao dịch mỗi giây.” (0.95): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: chuỗi/chuỷ — NOT_VERIFIED bằng tai người',
    'Câu một, khối 4 MB mỗi 600 giây, giao dịch trung bình 400 byte.':
        'ASR chép “Câu 1, khổ 4 MB mỗi 600 giây, giao dịch trung bình 400 bai.” (0.875): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: khối/khổ — NOT_VERIFIED bằng tai người',
    'Bạn đã đi qua chi tiêu hai lần, liên kết băm, cây Merkle, chữ ký, đồng chưa tiêu, bằng chứng công việc và đồng thuận.':
        'ASR chép “Bạn đã đi qua chi tiêu hai lần, liền kết băm, cây mơ cổ, chữ ký, đồng chưa tiêu, bằng chứng công việc và đồng thuận.” (0.923): Merkle đọc “Mơ-cồ” theo lexicon BCH, ASR viết “mơ cổ”; lệch âm/thanh thuần Việt: liên/liền — NOT_VERIFIED bằng tai người',
    # ── DAN L00–L11 (2026-10-31) ──
    'Bảng cho biết chỉ số nào gộp tiếp được từ bảng đã gộp.':
        'ASR chép “Bản cho biết chỉ số nào gột tiếp được từ bản đã gột.” (0.692): lệch âm/thanh thuần Việt: bảng/bản, gộp/gột, bảng/bản, gộp/gột — NOT_VERIFIED bằng tai người',
    'Lỗi thứ ba, gộp làm đảo chiều kết luận, gọi là nghịch lý Simpson.':
        'ASR chép “Lỗi thứ ba, gột làm đảo chiều kết luận, gọi là nghịch lý sim sân.” (0.867): Simpson đọc “Xim-xơn” theo lexicon DAN, ASR viết “sim sân”; lệch âm/thanh thuần Việt: gộp/gột — NOT_VERIFIED bằng tai người',
    'Bảng này so sánh độ mịn của ba bảng dữ liệu.':
        'ASR chép “Bản này so sánh độ miền của ba bản giữ liệu.” (0.727): lệch âm/thanh thuần Việt: bảng/bản, mịn/miền, bảng/bản — NOT_VERIFIED bằng tai người',
    'Quy tắc là sau phép nối, độ mịn của kết quả là độ mịn của bảng mịn hơn.':
        'ASR chép “Quy tắc là sau phép nối, độ mình của kết quả là độ mình của bản mình hơn.” (0.778): lệch âm/thanh thuần Việt: mịn/mình, mịn/mình, bảng mịn/bản mình — NOT_VERIFIED bằng tai người',
    'Hãy báo kèm trung vị, và tỉ trọng nhóm đầu, tức k phần trăm khách lớn nhất chiếm bao nhiêu phần trăm doanh thu.':
        'ASR chép “Hãy báo kèm trung vị và tỷ trọng nhóm đầu tất cả phần trăm khách lớn nhất chiếm bao nhiêu phần trăm doanh thu.” (0.875): “tỉ” ASR viết chính tả “tỷ” (cùng âm); chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: tức (trong “tức k” → “tất cả”) — NOT_VERIFIED bằng tai người',
    'Hệ số 1 phẩy 4826 làm điểm bền vững xấp xỉ điểm z khi dữ liệu có phân phối chuẩn và không có ngoại lai.':
        'ASR chép “Hệ số 1,4826 làm điểm bền vững sắp xỉ điểm dép khi dữ liệu có phân phối chuẩn và không có ngoại lai.” (0.935): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: xấp/sắp — NOT_VERIFIED bằng tai người',
    'A có 2 mua trên 2 xem, tỉ lệ thô 100 phần trăm, khoảng tin cậy từ 0 phẩy 342 tới 1.':
        'ASR chép “À, có 2 mua trên 2 xem tỷ lệ thô 100%, khoảng tiên cậy từ 0,342 tới 1.” (0.846): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; “tỉ” ASR viết chính tả “tỷ” (cùng âm); “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; lệch âm/thanh thuần Việt: tin/tiên, không (trong “không phẩy” → “”) — NOT_VERIFIED bằng tai người',
    # ── EVT L00–L10 (2026-10-31) ──
    'Hai máy lệch nhau vài trăm mi li giây là thường, nên bản mới viết trên máy chậm đồng hồ trông cũ hơn.':
        'ASR chép “Hai máy lệch nhau vài trăm mili dây là thường, nền bản mới viết trên máy chậm đồng hồ trong củ hơn.” (0.756): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; lệch âm/thanh thuần Việt: nên/nền, trông cũ/trong củ — NOT_VERIFIED bằng tai người',
    'Câu một, cập nhật đến theo thứ tự v bằng 2, 1, 4, 3, với giá trị X, W, Z, Y.':
        'ASR chép “Câu 1, cập nhật đến theo thứ tự về bằng 2, 1, 4, 3, với giá trị ích, về đúc, giết, y.” (0.884): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Lỗi thứ nhất, sửa hoặc xoá sự kiện cũ, nên mất dấu vết và các bảng đọc lệch nhau.':
        'ASR chép “Lội thứ nhất, sửa hoặc xóa sự kiện cũ nên mất dấu vết và các bản độc lệch nhau.” (0.789): lệch âm/thanh thuần Việt: lỗi/lội, vết/véc, bảng đọc/bản độc — NOT_VERIFIED bằng tai người',
    'Câu hai, phát hiện lần rút 80 là trừ nhầm, thì ghi gì vào nhật ký?':
        'ASR chép “Câu 2, phát hiện lần trúc 80 là trường nhầm thì di dì vào nhật ký.” (0.765): lệch âm/thanh thuần Việt: rút/trúc, trừ/trường, ghi gì/di dì — NOT_VERIFIED bằng tai người',
    'Mô hình đọc trễ vài giây có thể cho rút hai lần.':
        'ASR chép “Mua hình độc trễ và dây có thể cho rút hai lần.” (0.75): lệch âm/thanh thuần Việt: mô/mua, đọc/độc, vài/và — NOT_VERIFIED bằng tai người',
    'Tổng kết lại, mô hình ghi kiểm luật, còn mô hình đọc là bảng làm sẵn.':
        'ASR chép “Tổng kết lại, mô hình di kiểm lực, còn mô hình độc là bản làm sẵn.” (0.75): lệch âm/thanh thuần Việt: ghi/di, luật/lực, đọc/độc, bảng/bản — NOT_VERIFIED bằng tai người',
    'Mười bước có nhánh thì logic rải khắp nơi, khó biết đơn đang kẹt ở đâu, nên hãy dùng điều phối và lưu trạng thái từng giao dịch dài.':
        'ASR chép “Mười bước có nhánh thì lô ghét rãi khắp nơi, khó biết đơn đang kẹt ở đâu, nên hãy dùng điều phối và lưu trạng thái từng giao dịch dài.” (0.933): lệch âm/thanh thuần Việt: gíc rải/ghét rãi — NOT_VERIFIED bằng tai người',
    'Nối luồng với luồng là ghép hai sự kiện cùng mã, nếu thời điểm bấm trừ thời điểm hiển thị nằm từ 0 tới W, ví dụ W bằng 10 phút.':
        'ASR chép “Nối luồng với luồng là ghép hai sự kiện cùng mã nếu thời điểm bấm trừ thời điểm hiển thị nằm từ không tới v-dup, ví dụ v-dup bằng 10 phút.” (0.906): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Ở đây t là thời điểm xảy ra sự kiện, W là độ dài cửa sổ.':
        'ASR chép “Ở đây tê là thời điểm xảy ra sự kiện, về đúc là độ dài cửa sổ.” (0.909): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Nối luồng với luồng phải giữ các lượt hiển thị trong W phút gần nhất để chờ lượt bấm.':
        'ASR chép “Nối lùng với lùng phải giữ các lượt hiện thị trong về đúc phút gần nhất để chờ lượt bấm.” (0.769): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: luồng/lùng, luồng/lùng, hiển/hiện — NOT_VERIFIED bằng tai người',
    'Hãy chọn W theo hành vi thật, vì phần lớn lượt bấm đến trong vài phút, và luôn có giới hạn.':
        'ASR chép “Hãy chọn vê đúc theo hành vi thật, vì phần lớn lượt bấm đến trong vài phút và luôn có giới hạn.” (0.93): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Lỗi thứ ba, nối luồng với bảng mà bảng chưa nạp xong, nên đơn đầu ngày thiếu hạng thành viên.':
        'ASR chép “Lỗi thứ ba, nối lùng với bản mà bản chưa nặp xong nên đơn đầu ngày thiếu hàng thành viên.” (0.75): lệch âm/thanh thuần Việt: luồng/lùng, bảng/bản, bảng/bản, nạp/nặp, hạng/hàng — NOT_VERIFIED bằng tai người',
    'Lượt hiển thị là x lúc 5, y lúc 8, còn lượt bấm là x lúc 4, x lúc 9, y lúc 20, z lúc 9, với cửa sổ W bằng 10.':
        'ASR chép “Lược hiển thị là X lúc 5, Y lúc 8, còn lược bấm là X lúc 4, X lúc 9, Y lúc 20, Jack lúc 9, với cửa sổ V đúc bằng 10.” (0.866): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: lượt/lược, lượt/lược — NOT_VERIFIED bằng tai người',
    'Tổng kết lại, nối luồng với bảng là tra bản mới nhất, còn nối luồng với luồng là ghép cùng mã trong cửa sổ W.':
        'ASR chép “Tổng kết lại, nối luồng với bảng là tra bảng mới nhất, còn nối luồng với luồng là ghép cùng mã trong cửa sổ v-duc.” (0.902): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: bản/bảng — NOT_VERIFIED bằng tai người',
    'Ghép theo thời điểm xảy ra, và nhớ rằng W càng dài thì trạng thái phải giữ càng lớn.':
        'ASR chép “Gép theo thời điểm xảy ra, và nhớ rằng với đúc càng dài thì trạng thái phải giữ càng lớn.” (0.872): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: ghép/gép — NOT_VERIFIED bằng tai người',
    'K càng gần 1 thì hai cách tính càng lệch xa.':
        'ASR chép “Cá càng gần một thì hai cách tính càng lệch xa.” (0.909): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Cộng tất cả là sai, ra 110 mi li giây.':
        'ASR chép “Cộng tất cả là sai, ra 110 mili dây.” (0.783): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh — NOT_VERIFIED bằng tai người',
    # ── LLM L05 viết lại theo chuẩn độ sâu (2026-10-31) ──
    'Chào bạn, một mô hình khoảng 6 phẩy 4 tỉ tham số chiếm gần 13 GB ở dạng 2 byte mỗi số, vừa một thẻ tính toán.':
        'ASR chép “Chào bạn, một mô hình khoảng 6,4 tỷ tham số chiếm gần 13GB ở dạng 2 BI mỗi số, vừa mục thể tính toán.” (0.857): “tỉ” ASR viết chính tả “tỷ” (cùng âm); byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: một thẻ/mục thể — NOT_VERIFIED bằng tai người',
    'Nhưng phục vụ 16 người dùng cùng lúc, mỗi người ngữ cảnh 4096 từ tố, lại cần thêm khoảng 34 tỉ byte chỉ để nhớ khoá và giá trị của các từ tố đã đọc.':
        'ASR chép “Nhưng phục vụ 16 người dùng cùng lúc, mỗi người ngửi cảnh 4096 từ tố lại cần thêm khoảng 34 tỷ bay chỉ để nhớ khóa và giá trị của các từ tố đã đọc.” (0.932): “tỉ” ASR viết chính tả “tỷ” (cùng âm); byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: ngữ/ngửi — NOT_VERIFIED bằng tai người',
    'Hôm nay ta trả lời ba câu hỏi, con số 6 phẩy 4 tỉ từ đâu ra, 34 tỉ byte kia là gì, và vì sao mô hình sinh chữ chậm dù thẻ tính rất nhanh.':
        'ASR chép “Hôm nay ta trả lời ba câu hỏi, còn số 6,4 tỷ từ đâu ra, 34 tỷ bay kia là gì, và vì sao mô hình sinh chữ chậm dù thể tính rất nhanh.” (0.868): “tỉ” ASR viết chính tả “tỷ” (cùng âm); byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: con/còn, thẻ/thể — NOT_VERIFIED bằng tai người',
    'Một số ở dạng nửa độ chính xác chiếm 2 byte, nên 6 số chiếm 12 byte.':
        'ASR chép “Một số ở dạng nửa độ chính xác chiếm hai bay nên 6 số chiếm 10 hai bay.” (0.889): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); “12” ASR viết “10 hai” (đọc “mười hai”, cùng giá trị) — NOT_VERIFIED bằng tai người',
    'Một GB là 10 mũ 9 byte.':
        'ASR chép “1 GB là 10 mũ chín bay.” (0.857): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Còn một đơn vị nhị phân là 2 mũ 30 byte, lớn hơn khoảng 7 phần trăm.':
        'ASR chép “Còn 1 đơn vị nhị phân là 2 mũ 30 bai, lớn hơn khoảng 7 phần trăm.” (0.944): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Với đường ống 1 nghìn tỉ byte mỗi giây, một số minh hoạ, việc đọc mất 12 phẩy 9 mi li giây.':
        'ASR chép “với đường ống 1.000 tỷ bay mỗi giây, một số minh họa, việc độc mất 12,9 mili giây.” (0.8): “tỉ” ASR viết chính tả “tỷ” (cùng âm); byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; lệch âm/thanh thuần Việt: đọc/độc — NOT_VERIFIED bằng tai người',
    'Mỗi ma trận có d nhân 4d, tức 4 d bình phương số, nên hai ma trận có 8 d bình phương.':
        'ASR chép “Mỗi ma trận có dây nhân 4d, tức 4d bình phương số, nên 2 ma trận có 8d bình phương.” (0.957): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Nhân lần lượt theo số tầng, số từ tố, và số byte mỗi số, ta được 2 nhân L nhân d nhân n nhân 2 byte cho mỗi chuỗi.':
        'ASR chép “Nhân lần lượt theo số tầng, số tự tố và số bay mỗi số, ta được 2 nhân L nhân D nhân N nhân 2 bay cho mỗi chuỗi.” (0.897): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: từ/tự — NOT_VERIFIED bằng tai người',
    'Số 2 đầu là khoá và giá trị, số 2 cuối là 2 byte mỗi số.':
        'ASR chép “Số 2 đầu là khóa và giá trị. Số 2 cuối là 2 bay mỗi số.” (0.938): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Làm thử với một từ tố của mô hình ví dụ, 2 nhân 32 nhân 4096 nhân 2 bằng 524 nghìn 288 byte.':
        'ASR chép “Làm thử với một tự tố của mô hình ví dụ, 2 nhân 32 nhân 4.096 nhân 2 bằng 524.288 bay.” (0.949): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: từ/tự — NOT_VERIFIED bằng tai người',
    'Phép tính thứ ba, một từ tố cần 524 nghìn 288 byte, nên một chuỗi 4096 từ tố cần 2 tỉ 147 triệu byte, khoảng 2 phẩy 15 GB.':
        'ASR chép “Phép tính thứ ba, một tự tố cần 524.288 bai, nên một chuỗi 4.096 tự tố cần 2.147 triệu bai, khoảng 2,15 gigabyte.” (0.875): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); “2 tỉ 147 triệu” ASR viết gộp “2.147 triệu” (cùng giá trị); GB đọc “ghi-ga-byte” theo lexicon của khoá, ASR viết “GB/gigabyte”; lệch âm/thanh thuần Việt: từ/tự, từ/tự — NOT_VERIFIED bằng tai người',
    'Một chuỗi cần thêm 2 phẩy 15 GB bộ nhớ đệm.':
        'ASR chép “Một chuỗi cần thêm 2,15GB bộ nhớ đệm” (1.0): GB đọc “ghi-ga-byte” theo lexicon của khoá, ASR viết “GB/gigabyte” — NOT_VERIFIED bằng tai người',
    'Kiểm tra thứ nhất, vì công thức chỉ là một tích nên ta nhân thẳng, 2 nhân 32 nhân 4096 nhân 4096 nhân 2, cũng được 2 tỉ 147 triệu byte, khớp kết quả phép tính thứ ba.':
        'ASR chép “Kiểm tra thứ nhất, vì công thức chỉ là mục tích nền ta nhân thẳng, 2 nhân 32 nhân 4.096 nhân 4.096 nhân 2 cũng được 2 tỷ 147 triệu bay, khớp kết quả phép tính thứ 3.” (0.929): “tỉ” ASR viết chính tả “tỷ” (cùng âm); byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: một/mục, nên/nền — NOT_VERIFIED bằng tai người',
    'Câu hai, 2 nhân 40 nhân 5120 nhân 8192 nhân 2 bằng 6 tỉ 710 triệu 886 nghìn 400 byte, khoảng 6 phẩy 71 GB.':
        'ASR chép “Câu 2, 2 nhân 40 nhân 5.120 nhân 8.192 nhân 2 bằng 6 tỷ 710.886.400 bai, khoảng 6,71 gigabyte.” (0.935): “tỉ” ASR viết chính tả “tỷ” (cùng âm); byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); GB đọc “ghi-ga-byte” theo lexicon của khoá, ASR viết “GB/gigabyte” — NOT_VERIFIED bằng tai người',
    'Bộ nhớ đệm bằng 2 L d n nhân 2 byte cho mỗi chuỗi.':
        'ASR chép “Bộ nhớ đệm bằng 2 LVN nhân 2 byte cho mỗi chuỗi.” (0.846): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Điều cần mang theo, trước khi chọn mô hình hay mua phần cứng, hãy tính bộ nhớ và số byte phải đọc mỗi bước cho đúng số người dùng và độ dài ngữ cảnh thật.':
        'ASR chép “Điều cần mang theo trước khi chọn mô hình hay mua phần cứng, hãy tính bộ nhớ và số bai phải đọc mỗi bước cho đúng số người dùng và độ dài ngữ cảnh thật.” (0.971): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    # ── CLD L14–L15 bài hành trình (2026-10-31) ──
    'Ở bài sau, bài 15, ta đi lại mười năm quản lý container ở quy mô lớn, từ Borg tới Kubernetes, theo từng chặng, để thấy mỗi thực hành tốt ra đời từ điểm nghẽn nào.':
        'ASR chép “Ở bài sau, bài 15, ta đi lại 10 năm quản lý container ở quy mô lớn từ Boga tới Kubernetes theo từng chặn để thấy mỗi thực hành tốt ra đời từ điểm ngãn nào.” (0.919): Borg đọc “Bo-gờ” theo lexicon CLD (probe p3/p4: 7/8, PARTIAL), ASR viết “burger/boga/bò gờ/bog”; lệch âm/thanh thuần Việt: chặng/chặn, nghẽn/ngãn — NOT_VERIFIED bằng tai người',
    'Nhưng những ý tưởng cốt lõi của nó đã được thử thách từ trước đó hơn mười năm, trên hai hệ thống nội bộ tên Borg và Omega.':
        'ASR chép “nhưng những ý tưởng cốt lõi của nó đã được thử thách từ trước đó hơn 10 năm trên 2 hệ thống nội bộ tên Burger và Omega.” (0.964): Borg đọc “Bo-gờ” theo lexicon CLD (probe p3/p4: 7/8, PARTIAL), ASR viết “burger/boga/bò gờ/bog” — NOT_VERIFIED bằng tai người',
    'Ở bài 5, vòng điều khiển so trạng thái mong muốn với thực tế rồi hành động để khớp, ví dụ muốn 3 Pod mà thấy 2 thì tạo thêm 1.':
        'ASR chép “Ở bài năm, vòng điều khiển so trạng thái mong muốn với thực tế rồi hành động để khớp, ví dụ muốn 3 phút mà thấy 2 thì tạo thêm 1.” (0.968): Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút) — NOT_VERIFIED bằng tai người',
    'Trước Borg có hai hệ riêng, máy không dùng chung.':
        'ASR chép “Trước bò G có hai hệ riêng, máy không dùng chung.” (0.857): Borg đọc “Bo-gờ” theo lexicon CLD (probe p3/p4: 7/8, PARTIAL), ASR viết “burger/boga/bò gờ/bog” — NOT_VERIFIED bằng tai người',
    'Container cô lập để việc theo lô không làm chậm dịch vụ, và lấy lại phần giữ chỗ bỏ trống.':
        'ASR chép “cần tên nơ cô lập để việc theo lô không làm chậm dịch vụ và lấy lại phần giữ chỗ bỏ trống.” (0.905): container đọc thô (probe CLD p1: 5/8, small viết “cần tên nơi”) — NOT_VERIFIED bằng tai người',
    'Theo bài báo năm 2015 của nhóm Borg, tách hai loại việc ra hai ô riêng sẽ cần thêm 20 đến 30 phần trăm số máy ở ô trung vị.':
        'ASR chép “Theo bài báo năm 2015 của nhóm Burger, tách hai loại việc ra 2 ô riêng sẽ cần thêm 20-30% sổ máy ở ô Trung vị.” (0.932): Borg đọc “Bo-gờ” theo lexicon CLD (probe p3/p4: 7/8, PARTIAL), ASR viết “burger/boga/bò gờ/bog”; lệch âm/thanh thuần Việt: số/sổ; “20 đến 30 phần trăm” ASR viết “20-30%” (cùng nghĩa) — NOT_VERIFIED bằng tai người',
    'Ở chặng ba, quanh Borg mọc lên rất nhiều công cụ, từ đặt tên, cân bằng tải, co giãn, tới phát hành và giám sát.':
        'ASR chép “Ở chặng 3, quanh bò gờ mọc lên rất nhiều công cụ, từ đặt tên, cân bằng tải, co dãng, tới phát hành và giám sát.” (0.923): Borg đọc “Bo-gờ” theo lexicon CLD (probe p3/p4: 7/8, PARTIAL), ASR viết “burger/boga/bò gờ/bog”; lệch âm/thanh thuần Việt: giãn/dãng — NOT_VERIFIED bằng tai người',
    'Lần này người dùng ở bên ngoài, nên những vết sẹo của Borg được sửa ngay từ thiết kế.':
        'ASR chép “Lần này người dùng ở bên ngoài, nền những vết sẹo của BoG được sửa ngay từ thiết kế.” (0.842): Borg đọc “Bo-gờ” theo lexicon CLD (probe p3/p4: 7/8, PARTIAL), ASR viết “burger/boga/bò gờ/bog”; lệch âm/thanh thuần Việt: nên/nền, vết/véc — NOT_VERIFIED bằng tai người',
    'Trong Borg, container chung địa chỉ máy và hệ cấp số cổng, nên công cụ mạng quen thuộc phải viết lại, còn ở đây mỗi Pod có một địa chỉ IP riêng.':
        'ASR chép “Trong bloger, cần thay nơi chung địa chỉ máy và hệ cấp số cổng, nên công cụ mạng quen thuộc phải viết lại, còn ở đây mỗi phút có một địa chỉ IP riêng.” (0.879): container đọc thô (probe CLD p1: 5/8, small viết “cần tên nơi”); Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút); Borg đọc “Bo-gờ” theo lexicon CLD (probe p3/p4: 7/8, PARTIAL), ASR viết “burger/boga/bò gờ/bog” — NOT_VERIFIED bằng tai người',
    'Tháng 12 năm 2016, bản 1 chấm 5 cho phép thay trình chạy container khác, tức mở rộng qua một giao diện chuẩn.':
        'ASR chép “Tháng 12 năm 2016, bản 1.5 cho phép thay trình chạy Cantener khác, tức mở rộng qua một giao diện chuẩn.” (0.947): container đọc thô (probe CLD p1: 5/8, small viết “cần tên nơi”); “1 chấm 5” ASR viết số “1.5” (cùng giá trị) — NOT_VERIFIED bằng tai người',
    'Chính nhóm xây Borg viết rằng điều phối container chỉ là khởi đầu, không phải đích, nên đặt tên, cân bằng tải, co giãn, phát hành và giám sát vẫn phải thiết kế.':
        'ASR chép “Chính nhóm Seyborger viết rằng điều phối container chỉ là khởi đầu, không phải đức, nền đặt tên, cân bằng tải, co giãn, phát hành và giám sát vẫn phải thiết kế.” (0.892): Borg đọc “Bo-gờ” theo lexicon CLD (probe p3/p4: 7/8, PARTIAL), ASR viết “burger/boga/bò gờ/bog”; lệch âm/thanh thuần Việt: đích nên/đức nền — NOT_VERIFIED bằng tai người',
    'Nhóm Borg ghi rằng ngôn ngữ đó dần thành ngôn ngữ lập trình đầy đủ, nhưng thiếu công cụ gỡ lỗi và kiểm thử.':
        'ASR chép “Nhóm Burger ghi rằng ngôn ngữ đó dần thành ngôn ngữ lập trình đầy đủ, nhưng thiếu công cụ gỡ lỗi và kiểm thử.” (0.958): Borg đọc “Bo-gờ” theo lexicon CLD (probe p3/p4: 7/8, PARTIAL), ASR viết “burger/boga/bò gờ/bog” — NOT_VERIFIED bằng tai người',
    'Một cụm chung tận dụng máy tốt hơn, và nếu tỉ lệ giống Borg, một giả định, tách ra sẽ cần thêm khoảng 40 đến 60 máy, nhưng một lỗi cấu hình có thể ảnh hưởng mọi đội.':
        'ASR chép “Một cùng chung tận dụng máy tốt hơn, và nếu tỷ lệ giống boga, một giả định, tách ra sẽ cần thêm khoảng 40 đến 60 máy, nhưng một lỗi cấu hình có thể ảnh hưởng mọi đôi.” (0.9): “tỉ” ASR viết chính tả “tỷ” (cùng âm); Borg đọc “Bo-gờ” theo lexicon CLD (probe p3/p4: 7/8, PARTIAL), ASR viết “burger/boga/bò gờ/bog”; lệch âm/thanh thuần Việt: cụm/cùng, đội/đôi — NOT_VERIFIED bằng tai người',
    'Hãy đổi sang nhiều cụm khi một đội cần cô lập nghiêm ngặt, cũng là lý do Borg giữ mỗi ô độc lập.':
        'ASR chép “Hãy đổi sang nhiều cùng khi một đội cần cố lập nghiêm ngặt, cũng là lý do bogey giữ mỗi ô độc lập.” (0.87): Borg đọc “Bo-gờ” theo lexicon CLD (probe p3/p4: 7/8, PARTIAL), ASR viết “burger/boga/bò gờ/bog”; lệch âm/thanh thuần Việt: cụm/cùng, cô/cố — NOT_VERIFIED bằng tai người',
    'Nhãn, IP riêng cho mỗi Pod và giao diện thống nhất sửa các vết sẹo cũ.':
        'ASR chép “Nhãn, IP riêng cho mỗi phút và giao diện thống nhất sự các vết sẹo cũ.” (0.812): Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút); lệch âm/thanh thuần Việt: sửa/sự, vết/véc — NOT_VERIFIED bằng tai người',
    # ── AIF L02–L13 đào sâu (2026-10-31) ──
    'Khoảng cách Manhattan giữa hai ô là số bước đi dọc theo hàng và theo cột, không được đi chéo.':
        'ASR chép “Khoảng cách mang hát tầng giữa hai ô là số bước đi dọc theo hàng và theo cột, không được đi cháo.” (0.864): Manhattan đọc “Man-hát-tần” theo lexicon chung, ASR viết “mang hát tân/tầng”; lệch âm/thanh thuần Việt: chéo/cháo — NOT_VERIFIED bằng tai người',
    'Bước hai, tính h 2 bằng tổng khoảng cách Manhattan của từng ô tới chỗ đúng.':
        'ASR chép “Bước 2, tính hát 2 bằng tổng khoảng cách mang hát tần của từng ô tới chỗ đúng.” (0.944): Manhattan đọc “Man-hát-tần” theo lexicon chung, ASR viết “mang hát tân/tầng” — NOT_VERIFIED bằng tai người',
    'Thứ ba, cộng lại bảng Manhattan bằng tay cũng được 18.':
        'ASR chép “Thứ 3, cộng lại bảng mang hát tần bằng tay cũng được 18.” (0.929): Manhattan đọc “Man-hát-tần” theo lexicon chung, ASR viết “mang hát tân/tầng” — NOT_VERIFIED bằng tai người',
    'Ở bài 2, với trạng thái đầu quen thuộc, số ô sai chỗ h 1 bằng 8, tổng khoảng cách Manhattan h 2 bằng 18, và chi phí thật là 26.':
        'ASR chép “Ở bài 2, với trạng thái độ quen thuộc, số ô sai chỗ hát 1 bằng 8, tổng khoảng cách mang hát tần hát 2 bằng 18 và chi phí thật là 26.” (0.944): Manhattan đọc “Man-hát-tần” theo lexicon chung, ASR viết “mang hát tân/tầng”; lệch âm/thanh thuần Việt: đầu/độ — NOT_VERIFIED bằng tai người',
    'Và vì mỗi ô sai chỗ cần ít nhất một bước Manhattan, nên h 1 luôn không vượt h 2, ở cả hai trạng thái đã gặp, 8 so với 18 và 4 so với 6.':
        'ASR chép “Và vì mỗi ô sai chỗ cần ít nhất một bước mang hát từng nên hát một luôn không vượt hát hai, ở cả hai trạng thái đã gặp 8 xo với 18 và 4 xo với 6.” (0.949): Manhattan đọc “Man-hát-tần” theo lexicon chung, ASR viết “mang hát tân/tầng” — NOT_VERIFIED bằng tai người',
    'Bỏ luật không đi xuyên tường thì được khoảng cách Manhattan.':
        'ASR chép “Bỏ luật không đi xuyên tường thì được khoảng cách mang hát tân.” (0.846): Manhattan đọc “Man-hát-tần” theo lexicon chung, ASR viết “mang hát tân/tầng” — NOT_VERIFIED bằng tai người',
    'Hậu ở hàng 1 cột 0 và hậu ở hàng 3 cột 3 có chênh hàng 2 khác chênh cột 3, nên không.':
        'ASR chép “Hậu ở hàng một cục không và hậu ở hàng ba cục ba có trên hàng hai khác trên cục ba, nên không.” (0.783): lệch âm/thanh thuần Việt: cột/cục (ASR lẫn “cột/cục” 28 lần trên toàn kho báo cáo, các khoá khác đã xem xét), cột/cục, chênh/trên, chênh cột/trên cục — NOT_VERIFIED bằng tai người',
    'Vì vậy số lần chạy kỳ vọng là 1 chia p, khoảng 6 phẩy 7 lần.':
        'ASR chép “Vì vậy số lần chạy kỳ vọng là 1 GP khoảng 6,7 lần.” (0.903): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: chia (trong “chia p” → “gp”) — NOT_VERIFIED bằng tai người',
    'Vì vậy bên cực đại chắc chắn có ít nhất 3 điểm, nên alpha bằng 3.':
        'ASR chép “Vì vậy bên cực đại chắc chắn có ít nhất 3 điểm nên an pha bằng 3.” (0.909): alpha đọc thô (probe AIF p1: 7/8, bản chép “an pha / ANFA / α”) — NOT_VERIFIED bằng tai người',
    'Mà 2 nhỏ hơn alpha bằng 3, nên bên cực đại không bao giờ chọn C.':
        'ASR chép “mà hai nhỏ hơn an pha bằng ba nên binh cực đại không bao giờ chọn xe.” (0.848): alpha đọc thô (probe AIF p1: 7/8, bản chép “an pha / ANFA / α”); lệch âm/thanh thuần Việt: bên/binh — NOT_VERIFIED bằng tai người',
    'Xét từ trái sang, xong nước thứ hai thì alpha bằng 6, nước thứ ba gặp lá 1 nhỏ hơn 6 nên bỏ lá 9, xét 5 lá.':
        'ASR chép “Xét từ trái sang, xong nước thứ 2 thì an pha bằng 6, nước thứ 3 gặp lá 1 nhỏ hơn 6 nên bỏ lá 9, xét 5 lá.” (0.947): alpha đọc thô (probe AIF p1: 7/8, bản chép “an pha / ANFA / α”) — NOT_VERIFIED bằng tai người',
    'Xếp nước 6 và 7 lên đầu thì alpha bằng 6 ngay, nước tiếp theo gặp 5 nhỏ hơn 6 nên bỏ lá 3, nước cuối bỏ lá 9, chỉ xét 4 lá.':
        'ASR chép “Sếp nước 6 và 7 lên đầu thì an pha bằng 6 ngày, nước tiếp theo gặp 5 nhỏ hơn 6 nên bỏ lá 3, nước cuối bỏ lá 9, chỉ xét 4 lá.” (0.925): alpha đọc thô (probe AIF p1: 7/8, bản chép “an pha / ANFA / α”); lệch âm/thanh thuần Việt: ngay/ngày — NOT_VERIFIED bằng tai người',
    'Câu này chỉ sai trong đúng một trường hợp, P đúng mà Q sai.':
        'ASR chép “Câu này chỉ sai trong đúng một trường hợp về đúng mà quý sai.” (0.929): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Bên trái, vùng xanh dương là các mô hình của tri thức, nằm trọn trong vùng câu alpha đúng, nên tri thức kéo theo alpha.':
        'ASR chép “Bên trái, vùng xanh dưng là các mô hình của trí thức, nằm trọn trong vùng câu an pha đúng, nên trí thức kéo theo an pha.” (0.769): alpha đọc thô (probe AIF p1: 7/8, bản chép “an pha / ANFA / α”); lệch âm/thanh thuần Việt: dương/dưng, tri/trí, tri/trí — NOT_VERIFIED bằng tai người',
    'Thấy một người mang ô, xác suất đang mưa bằng 0 phẩy 24 chia cho 0 phẩy 24 cộng 0 phẩy 07, xấp xỉ 0 phẩy 774.':
        'ASR chép “Thấy một người ma nô, sát xuất đang mưa bằng 0,24 chia cho 0,24 cộng 0,07, sắp xỉ 0,774.” (0.853): “mang ô” nối âm thành “ma nô” (ô là cái ô che mưa); “xác/sát”, “xấp/sắp” lẫn x/s ở đầu từ; “0 phẩy 24” ASR viết số thập phân 0,24 — các con số đều khớp — NOT_VERIFIED bằng tai người',
    'Mạng Bayes làm đúng phép này, nhưng với nhiều biến.':
        'ASR chép “Mạng bay x làm đúng phép này, nhưng với nhiều biến.” (0.909): Bayes đọc “Bay-ét” theo lexicon chung (probe 3/8, NOT_VERIFIED), ASR viết “bay X/S” — NOT_VERIFIED bằng tai người',
    'Bước ba, ở bài 6 ta đã thấy cắt tỉa alpha beta bỏ những nhánh chắc chắn không được chọn.':
        'ASR chép “Bước 3. Ở bài 6 ta đã thấy các tỉa an pha beta bỏ những nhánh chắc chắn không được chọn.” (0.837): beta đọc “bê-ta”, ASR viết “bê/beta”; alpha đọc thô (probe AIF p1: 7/8, bản chép “an pha / ANFA / α”); lệch âm/thanh thuần Việt: cắt/các — NOT_VERIFIED bằng tai người',
    # ── LLM L02–L07 đào sâu (2026-10-31) ──
    'Thứ hai, máy lưu chữ thành byte, chữ a không dấu cần 1 byte, còn chữ ô hay chữ e huyền cần 2 byte.':
        'ASR chép “Thứ hai, máy lưu chữ thành bay, chữ A không dấu cần một bay, còn chữ O hay chữ E huyền cần hai bay.” (0.833): byte đọc thô, ASR viết “bay” (probe CSA p1: “bay” 8/8); “ô” là tên chữ cái, ASR viết chữ “O”; mọi con số khớp — NOT_VERIFIED bằng tai người',
    'Hình vẽ mất mát âm lôgarit p theo xác suất p mà mô hình gán cho từ tố đúng.':
        'ASR chép “Hình vẽ mất mát âm Logarith về theo sát suất p mà mô hình gán cho tự tố đúng.” (0.842): tên chữ cái p (“pê”) bị nghe thành “về” ở lần đầu, lần sau chép đúng “p”; “xác/sát” lẫn x/s; “từ/tự” lệch thanh — NOT_VERIFIED bằng tai người',
    'Và e mũ lôgarit của 7 lại bằng 7, vì hai phép này triệt tiêu nhau.':
        'ASR chép “và e-mũ Logatrix của 7 lại bằng 7, vì hai phép này triệt tiêu nhau.” (0.938): “lôgarit” là từ phiên âm, ASR viết lại theo chính tả Latin (“Logatrix/Logarith”); phần còn lại chép đúng nguyên văn — NOT_VERIFIED bằng tai người',
    'Vì độ hỗn loạn bằng e mũ mất mát, nên nó xấp xỉ 2 phẩy 16.':
        'ASR chép “vì độ hỗn loạn bằng em mũ mất mát nên nó xấp xỉ 2,16.” (0.941): tên chữ cái e đọc kiểu Việt, ASR viết “em”; con số 2,16 khớp — NOT_VERIFIED bằng tai người',
    # ── LLM L08 + SWF L05 đào sâu (2026-10-31) ──
    'Ma trận gốc W là hình vuông lớn, giữ nguyên, không học.':
        'ASR chép “Ma trận gốc về đúc là hình vùng lớn, giữ nguyên, không học.” (0.8): W đọc tên chữ cái “vê đúp”, ASR viết “về đúc/V đúc” (đã chấp nhận ở mọi khoá); “vuông/vùng” lẫn vần ở từ ngắn, các từ còn lại chép đúng — NOT_VERIFIED bằng tai người',
    'Ta chỉ học hai dải mỏng màu cam, B có d hàng nhưng chỉ r cột, A có r hàng và d cột, với r nhỏ như 8, và tích của chúng có cùng cỡ với W.':
        'ASR chép “Ta chỉ học hai giải mỏng màu cam, B có dây hàng nhưng chỉ R cọt, A có R hàng và dây cọt, với R nhỏ như 8, và tích của chúng có cùng cỡ với V đúc.” (0.853): tên chữ cái d (“đê”), r, W đọc kiểu Việt, ASR viết “dây/R/V đúc”; “dải/giải” lẫn d/gi, “cột/cọt” lệch thanh; số 8 khớp — NOT_VERIFIED bằng tai người',
    'Câu hai, B bằng 0 thì tích B nhân A bằng 0, nên lúc đầu ma trận mới bằng đúng W, và mô hình bắt đầu đúng như mô hình gốc.':
        'ASR chép “Câu 2, B bằng không thì tích B nhân A bằng không nên lúc đầu ma trận mới bằng đúng V đúc và mô hình bắt đầu đúng như mô hình gốc.” (0.952): W đọc tên chữ cái “vê đúp”, ASR viết “V đúc” (đã chấp nhận ở mọi khoá) — NOT_VERIFIED bằng tai người',
    'Và 8 triệu 388 nghìn 608 nhân 2 byte bằng 16 triệu 777 nghìn 216, đúng bằng số phần tử của một ma trận đầy đủ, một cách nhớ thú vị.':
        'ASR chép “và 8,388,608 nhân hai bay bằng 16,777,216, đúng bằng số phần tử của một ma trận đầy đủ, một cách nhớ thú vị.” (0.978): byte đọc thô, ASR viết “bay” (probe CSA p1: “bay” 8/8); mọi con số khớp — NOT_VERIFIED bằng tai người',
    'Bước bốn, lưu kết quả tinh chỉnh chỉ cần khoảng 16 triệu 800 nghìn byte, thay vì gần 13 GB cho cả mô hình, nên nhiều bản tinh chỉnh dùng chung được một mô hình gốc.':
        'ASR chép “Bước 4, lưu kết quả tinh chỉnh chỉ cần khoảng 16.800.000 byte, thay vì gần 13GB cho cả mô hình, …” (1.0): gắn cờ vì có từ rủi ro (byte, GB) nhưng cả hai mô hình chép đúng nguyên văn — NOT_VERIFIED bằng tai người',
    'Dòng mã nói nếu x dương thì đặt y bằng 10.':
        'ASR chép “Dòng mã nói nếu quyết dương thì đặt y bằng mươi.” (0.818): tên chữ cái x (“ích”) bị nghe thành “quyết”; “mười/mươi” lệch thanh, số 10 hiện trên màn hình — NOT_VERIFIED bằng tai người',
    # ── Đợt A đào sâu: LLM, AIF, CLC, SWF, SEC, SDP (2026-10-31, lượt 2) ──
    'Ở khoá toán, ta đã học tổng 1 cộng alpha cộng alpha bình phương, tới alpha mũ k, bằng 1 trừ alpha mũ k cộng 1, chia 1 trừ alpha.':
        'ASR chép “Ở khóa toán, ta đã học tổng một cộng an pha cộng an pha bình phương tới an pha mũ ca bằng một trừ an pha mũ ca cộng một, chia một trừ an pha.” (0.769): alpha đọc thô (probe AIF p1: 7/8, bản chép “an pha / ANFA / α”) — NOT_VERIFIED bằng tai người',
    'Làm thử với alpha bằng 0 phẩy 5 và k bằng 2, cộng thẳng được 1 phẩy 75, công thức cũng ra 1 phẩy 75.':
        'ASR chép “Làm thử với an pha bằng 0,5 và ca bằng 2, cộng thẳng được 1,75, công thức cũng ra 1,75.” (0.949): alpha đọc thô (probe AIF p1: 7/8, bản chép “an pha / ANFA / α”) — NOT_VERIFIED bằng tai người',
    'Bước hai, giải mã suy đoán với k bằng 4 và alpha bằng 0 phẩy 8.':
        'ASR chép “Bước 2, giải mã suy đoán với ca bằng 4 và an pha bằng 0,8.” (0.909): alpha đọc thô (probe AIF p1: 7/8, bản chép “an pha / ANFA / α”) — NOT_VERIFIED bằng tai người',
    'Trước hết, đổi đơn vị trước khi nhân, vì đơn giá tính theo giây và GB.':
        'ASR chép “Trước hết, đổi đơn vị trước khi nhân, vị đơn giá tính theo dây và gigabyte.” (0.875): GB đọc “ghi-ga-byte” theo lexicon của khoá, ASR viết “GB/gigabyte”; lệch âm/thanh thuần Việt: vì/vị — NOT_VERIFIED bằng tai người',
    'Bước một, với số minh hoạ, tính GB giây bằng 10 mũ 6 lần nhân 0 phẩy 2 giây nhân 0 phẩy 5 GB, bằng 100 nghìn GB giây.':
        'ASR chép “Bước 1, với số minh họa, tính Gigabyte dây bằng 10 mũ 6 lần nhân không phải 2 dây nhân không phải 5 Gigabyte bằng 100.000 Gigabyte dây.” (0.833): GB đọc “ghi-ga-byte” theo lexicon của khoá, ASR viết “GB/gigabyte”; “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải” — NOT_VERIFIED bằng tai người',
    'GB giây bằng 5 nhân 10 mũ 7 nhân 0 phẩy 1 nhân 1, bằng 5 triệu, nhân đơn giá được khoảng 83 phẩy 33 đô la.':
        'ASR chép “Gigabyte dây bằng 5 nhân 10 mũ 7 nhân 0,1 nhân 1, bằng 5 triệu, nhận đơn giá được khoảng 83,33 đô la.” (0.935): GB đọc “ghi-ga-byte” theo lexicon của khoá, ASR viết “GB/gigabyte”; lệch âm/thanh thuần Việt: nhân/nhận — NOT_VERIFIED bằng tai người',
    'Trước hết, một bài toán quen thuộc, chép 500 GB ở tốc độ 200 MB mỗi giây mất bao lâu.':
        'ASR chép “Trước hết, một bài toán quen thuộc chép 500GB ở tốc độ 200MB mỗi giây mất bao lâu.” (1.0): GB đọc “ghi-ga-byte” theo lexicon của khoá, ASR viết “GB/gigabyte”; MB đọc “mê-ga-byte” theo lexicon của khoá, ASR viết “MB/megabyte” — NOT_VERIFIED bằng tai người',
    'Đổi cùng đơn vị, với MB bằng 10 mũ 6 byte và GB bằng 10 mũ 9 byte, 500 GB bằng 500 nghìn MB.':
        'ASR chép “Đổi cùng đơn vị, với Megabyte bằng 10 mũ 6b và Gigabyte bằng 10 mũ 9b, 500GB bằng 500.000 MB.” (0.846): MB đọc “mê-ga-byte” theo lexicon của khoá, ASR viết “MB/megabyte”; byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); GB đọc “ghi-ga-byte” theo lexicon của khoá, ASR viết “GB/gigabyte” — NOT_VERIFIED bằng tai người',
    'Kiểm bằng đường khác, đổi tốc độ ra GB mỗi phút trước khi chia, vì một phút có 60 giây.':
        'ASR chép “Kiểm bằng đường khác, đổi tốc độ ra gigabyte mỗi phút trước khi chia vì 1 phút có 60 giây.” (0.952): GB đọc “ghi-ga-byte” theo lexicon của khoá, ASR viết “GB/gigabyte” — NOT_VERIFIED bằng tai người',
    'Nhân 0 phẩy 09 đô la mỗi GB được khoảng 4608 đô la mỗi tháng, một khoản không thấy khi chỉ thử với ít người dùng.':
        'ASR chép “Nhân 0,09 đô la mỗi Gigabyte được khoảng 4.608 đô la mỗi tháng, một khoảng không thấy khi chỉ thử với ít người dùng.” (0.935): GB đọc “ghi-ga-byte” theo lexicon của khoá, ASR viết “GB/gigabyte”; lệch âm/thanh thuần Việt: khoản/khoảng — NOT_VERIFIED bằng tai người',
    'Không có khoá thì bản mã chỉ là dãy byte vô nghĩa.':
        'ASR chép “Không có khóa thì bản mã chỉ là dạy bay vô nghĩa.” (0.833): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: dãy (trong “dãy byte” → “dạy bay”) — NOT_VERIFIED bằng tai người',
    'Dữ liệu không đổi một byte nào.':
        'ASR chép “Giữ liệu không đổi một bay nào.” (0.857): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    '10 mũ 8 byte dữ liệu chia 32 byte khoá được 3 triệu 125 nghìn.':
        'ASR chép “10 mũ tám bay giữ liệu chia 32 bay khóa được 3 triệu 125.000.” (0.905): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Đáp án câu một, xoay khoá chính chỉ mã hoá lại các khoá dữ liệu, 50 nghìn nhân 32, bằng 1 triệu 600 nghìn byte, khoảng 1 phẩy 6 MB.':
        'ASR chép “Đáp án câu một, xoay khóa chính chỉ mã hóa lại các khóa dữ liệu 50.000 nhân 32 bằng 1.600.000 byte, khoảng 1.6 megabyte.” (0.955): “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; MB đọc “mê-ga-byte” theo lexicon của khoá, ASR viết “MB/megabyte” — NOT_VERIFIED bằng tai người',
    'Hình dung một hàng quân cờ đô-mi-nô.':
        'ASR chép “Hình dung một hàng quân cờ Domino” (0.75): “đô-mi-nô” ASR viết đúng từ mượn gốc “Domino”, cả câu đúng nghĩa — NOT_VERIFIED bằng tai người',
    'Dòng mã nói nếu x dương thì đặt y bằng 10.':
        'ASR chép “Dòng mã nói nếu quyết dương thì đặt y bằng mươi.” (0.818): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: mười/mươi — NOT_VERIFIED bằng tai người',
    'Vậy mảng không phải đống nhỏ nhất, vi phạm ở hai chỗ.':
        'ASR chép “Vậy mạng không phải đóng nhỏ nhất vì phạm ở hai chỗ.” (0.75): lệch âm/thanh thuần Việt: mảng/mạng, đống/đóng, vi/vì — NOT_VERIFIED bằng tai người',
    'Ở khoá Lý thuyết tính toán, đây chính là ô-tô-mát hữu hạn đơn định.':
        'ASR chép “Ở khóa lý thuyết tính toán, đây chính là automa khử hạn đơn định.” (0.8): “ô-tô-mát” ASR viết theo từ gốc “automa”; “hữu/khử” lệch phụ âm đầu ở từ ngắn ngay sau — NOT_VERIFIED bằng tai người',
    'Nhưng chạy thử chỉ phủ dãy ngắn, còn đọc bảng thì phủ mọi dãy.':
        'ASR chép “Nhưng chạy thử chỉ phủ giảy ngắn, còn đọc bản thì phủ mọi giảy.” (0.786): lệch âm/thanh thuần Việt: dãy/giảy, bảng/bản, dãy/giảy — NOT_VERIFIED bằng tai người',
    'Bước hai, xét một cách xen kẽ cụ thể.':
        'ASR chép “Bước 2, xét 1 cách xem kẻ cụ thể.” (0.778): lệch âm/thanh thuần Việt: xen kẽ/xem kẻ — NOT_VERIFIED bằng tai người',
    'Ở khoá Kiến trúc máy tính, mỗi chữ cái tiếng Anh được lưu bằng một byte, chữ A có mã 65, chữ B có mã 66.':
        'ASR chép “Ở khóa kiến trúc máy tính, mỗi chữ cái tiếng Anh được lưu bằng một bay, chữ A có mã 65, chữ B có mã 66.” (0.967): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Trong ngôn ngữ C, chuỗi kết thúc bằng một byte 0, nên chuỗi 9 chữ cần 10 byte.':
        'ASR chép “Trong ngôn ngữ C, chuỗi kết thúc bằng một bay không, nền chuỗi 9 chữ cần 10 bay.” (0.833): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: nên/nền — NOT_VERIFIED bằng tai người',
    'Hình vẽ mô hình bộ nhớ, mảng 8 byte màu xanh nằm sát ngay trước byte cờ quản trị.':
        'ASR chép “Hình về mô hình bộ nhớ, mảng 8 bai màu xanh nằm xác ngay trước bai cờ quản trị.” (0.789): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: vẽ/về, sát/xác — NOT_VERIFIED bằng tai người',
    'Chép 10 byte vào chỗ chỉ có 8 mà không kiểm độ dài, hai byte cuối tràn sang ô hàng xóm, tô đỏ.':
        'ASR chép “Chép 10 bay vào chỗ chỉ có 8 mà không kiểm độ dài, 2 bay cuối tràn sang ô hàng xóm, tô đỏ.” (0.913): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Byte cờ bị ghi thành 66, mã của chữ B, dù không ai cấp quyền.':
        'ASR chép “Bay cờ bị ghi thành 66, mã của chữ B, dù không ai cấp quyền.” (0.941): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Bước hai, với tràn bộ đệm, xét mô hình một mảng 8 ký tự nằm ngay trước một byte cờ quản trị bằng 0.':
        'ASR chép “Bước 2, với trang bộ đệm, xét mô hình một mảng 8 ký tự nằm ngay trước một bay cờ quản trị bằng 0.” (0.917): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: tràn/trang — NOT_VERIFIED bằng tai người',
    'Cần chép 9 chữ cộng một byte kết thúc, tức 10 byte, vào chỗ chỉ có 8, nên tràn 2 byte.':
        'ASR chép “Cần chép 9 chữ cộng 1 bay kết thúc, tức 10 bay, vào chỗ chỉ có 8, nên tràn 2 bay.” (0.857): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Byte cờ thành mã của chữ B, bằng 66, khác 0, và người dùng thành quản trị.':
        'ASR chép “bay cờ thành mã của chữ B bằng 66, khác không và người dùng thành quản trị.” (0.947): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Bước ba, cách sửa là chép có kiểm độ dài, chỉ giữ 7 chữ cộng byte kết thúc cho vừa 8 byte.':
        'ASR chép “Bước 3. Các sữa là chép có kiểm độ dài, chỉ giữ 7 chữ cộng bay kết thúc cho vừa 8 bay.” (0.818): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: cách sửa/các sữa — NOT_VERIFIED bằng tai người',
    'Khi đó không byte nào tràn, và byte cờ vẫn bằng 0.':
        'ASR chép “Khi đó không bay nào tràn và bay cờ vẫn bằng không.” (0.833): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Đếm tay, 9 cộng 1 trừ 8 bằng 2 byte tràn, khớp mô hình.':
        'ASR chép “Đếm tay, 9 cộng 1 trừ 8 bằng hai bay tràng, khớp mô hình.” (0.857): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: tràn (trong “byte tràn” → “bay tràng”) — NOT_VERIFIED bằng tai người',
    'Chữ thứ 9 là B, rơi đúng vào ô ngay sau mảng, tức byte cờ, nên byte cờ bằng 66.':
        'ASR chép “Chữ thứ 9 là b, rơi đúng vào ôn ngay sau mảnh, tích bai cờ, nên bai cờ bằng 66.” (0.773): “ô” (ô nhớ) ASR chép “ôn”; byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: mảng tức (trong “mảng tức byte” → “mảnh tích bai”) — NOT_VERIFIED bằng tai người',
    'Chạy lại mô hình với bản có kiểm độ dài, không byte nào tràn và cờ vẫn bằng 0.':
        'ASR chép “Chạy lại mô hình với bảng có kiểm độ dài, không bay nào tràn và cờ vẫn bằng không.” (0.895): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: bản/bảng — NOT_VERIFIED bằng tai người',
    'Câu hai, cần 12 cộng 1 bằng 13 byte, trong khi chỗ chỉ có 8, nên tràn 13 trừ 8 bằng 5 byte.':
        'ASR chép “Câu 2, cần 12 cộng 1 bằng 13 bai, trong khi chỗ chỉ có 8, nên tràn 13 trừ 8 bằng 5 bai.” (0.923): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Băm có khoá bí mật và khoảng số 2 cho 20 byte, nửa thấp của byte cuối bằng 4, nên ta lấy 4 byte bắt đầu từ vị trí 4.':
        'ASR chép “Bầm có khóa bí mật và khoảng số 2 cho 20 bai, nửa thấp của bai cuối bằng 4, nên ta lấy 4 bai bắt đầu từ vị trí 4.” (0.871): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: băm/bầm — NOT_VERIFIED bằng tai người',
    'Bốn byte đó, bỏ bit đầu, đổi ra số được 137 359 152.':
        'ASR chép “4 bài đó, bỏ biết đầu, đổi ra số được 137-359-152.” (0.92): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: bit/biết — NOT_VERIFIED bằng tai người',
    'Kế toán tạo hoá đơn, ô ghi có, nên cho.':
        'ASR chép “Kế toán tạo hóa đơn, ồ ghi có, nên cho.” (0.9): “ô” (ô ghi có trong bảng) ASR chép thán từ “ồ”, phần còn lại đúng — NOT_VERIFIED bằng tai người',
    'Câu một, trang lạ có một liên kết, người dùng bấm vào là mở đường dẫn xoá đơn số 7 của ngân hàng bằng phương thức lấy, cookie đặt mức nới lỏng.':
        'ASR chép “Câu 1. Trang lạ có một liên kết. Người dùng bấm vào là mở đường dẫn xóa đơn số 7 của ngân hàng bằng phương thức lấy. Cúc kỳ đặt mức nới lỏng.” (0.954): lệch âm/thanh thuần Việt: cookie/cúc kỳ — NOT_VERIFIED bằng tai người',
    'Ở khoá Mạng máy tính, mã hoá đối xứng là hai bên dùng chung một khoá, khoá 16 byte dài 16 nhân 8 bằng 128 bit.':
        'ASR chép “Ở khóa mạng máy tính, mã hóa đối xứng là hai bên dùng chung một khóa, khóa 16 3 dài 16 nhân 8 bằng 128 bit.” (0.969): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Ví dụ theo byte, mã chữ 9 cộng loại trừ mã chữ 5 ra một byte khác 0, và cộng loại trừ tiếp với mã chữ 9 thì ra lại mã chữ 5.':
        'ASR chép “Ví dụ theo bay, mã chữ 9 cộng loại trừ mã chữ 5 ra một bay khác không và cộng loại trừ tiếp với mã chữ 9 thì ra lại mã chữ 5.” (0.939): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Tự băm khoá ghép với khối một bằng thư viện băm và lấy 8 byte đầu, ta được đúng bản mã của khối một.':
        'ASR chép “Tự băm khóa kép với khối 1 bằng thư viện băm và lấy 8 bay đầu, ta được đúng bản mã của khối 1.” (0.917): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: ghép/kép — NOT_VERIFIED bằng tai người',
    'Byte đầu của chế độ bộ đếm, khối một, là mã chữ T cộng loại trừ byte đầu của dòng khoá, tính tay ra a 6, khớp máy.':
        'ASR chép “Bay đầu của chế độ bộ đếm, khối 1 là mã chữ T cộng loại trừ bay đầu của dòng khóa tính tay ra A6, khớp máy.” (0.929): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Khối ba cũng bắt đầu bằng chữ T, nhưng dòng khoá khác, nên byte đầu ra b e, khác a 6.':
        'ASR chép “Khối ba cũng bắt đầu bằng chữ T, nhưng dòng khóa khác nên bay đầu ra BE khác A6.” (0.952): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Byte thứ bảy là mã chữ 9 cộng loại trừ mã chữ 5, khác 0.':
        'ASR chép “Bài thứ 7 là mã chữ 9 cộng loại trừ mã chữ 5, khác không?” (0.933): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Nếu kẻ xem trộm biết tin thứ nhất là lương 9 triệu, cộng loại trừ mã chữ 9 với byte vừa tìm ra đúng mã chữ 5, nên đọc được tin thứ hai.':
        'ASR chép “Nếu kẻ xem trộm biết tin thứ nhất là lương 9 triệu, cộng loại trừ mã chữ 9 với bay vừa tìm ra đúng mã chữ 5 nên đọc được tin thứ 2.” (0.97): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Kẻ xấu không sửa gì, chỉ gửi lại y nguyên một tin cũ kèm mã cũ, và mã vẫn đúng.':
        'ASR chép “Kẻ xấu không sửa gì, chỉ gửi lại yên nguyên một tim cũ kè mã cũ, và mã vẫn đúng.” (0.85): lệch âm/thanh thuần Việt: i/yên, tin/tim, kèm/kè — NOT_VERIFIED bằng tai người',
    'Băm 64 bit chỉ cần khoảng 5 phẩy 06 tỉ giá trị.':
        'ASR chép “Bàm 64 biết chỉ cần khoảng 5,06 tỷ giá trị.” (0.786): “tỉ” ASR viết chính tả “tỷ” (cùng âm); lệch âm/thanh thuần Việt: băm/bàm, bit/biết — NOT_VERIFIED bằng tai người',
    'Ở khoá Kiến trúc máy tính, bộ nhớ là một dãy ô 1 byte, mỗi ô có một địa chỉ.':
        'ASR chép “Ở khóa kiến trúc máy tính, bộ nhớ là một giảy ô một bay, mỗi ô có một địa chỉ.” (0.9): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: dãy/giảy — NOT_VERIFIED bằng tai người',
    'Mảng 16 byte đặt ở địa chỉ 100 chiếm tới ô 115, nên ghi 20 byte từ ô 100 sẽ tới ô 119, tràn sang 4 ô hàng xóm.':
        'ASR chép “Mản 16 bay đặt ở địa chỉ 109 tới ô 115, nên ghi 20 bay từ ô 100 sẽ tới ô 119, tràn sang 4 ô hàng xóm.” (0.886): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); “100 chiếm” ASR chép “109” (âm “chiếm” bị nghe thành “chín”), mọi con số khác khớp, địa chỉ 100 hiện trên màn hình; “mảng/mản” — NOT_VERIFIED bằng tai người',
    'Chép 20 byte mà không kiểm độ dài, phần thừa tràn sang phải và chạm chim hoàng yến trước tiên.':
        'ASR chép “Chép 20 bay mà không kiểm độ dài, phần thừa trang sang phải và chạm chim hoàn yến trước tiên.” (0.857): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: tràn/trang, hoàng/hoàn — NOT_VERIFIED bằng tai người',
    'Dòng cuối là mặc định, còn lại thì chặn.':
        'ASR chép “Dòng cuối là mặc định, còn lại thi chẳng.” (0.778): lệch âm/thanh thuần Việt: thì chặn/thi chẳng — NOT_VERIFIED bằng tai người',
    'Ví dụ 2 nghìn GB tức 2 triệu MB, chép qua đường 100 MB mỗi giây, mất 20 nghìn giây, khoảng 5 phẩy 6 giờ.':
        'ASR chép “Ví dụ 2000GB tức 2 triệu megabyte, chép qua đường 100 megabyte mỗi giây, mất 20.000 giây, khoảng 5,6 giờ.” (0.926): MB đọc “mê-ga-byte” theo lexicon của khoá, ASR viết “MB/megabyte” — NOT_VERIFIED bằng tai người',
    'Chuỗi x gặp kí tự lạ ngay, nên trả 0 mà không báo gì.':
        'ASR chép “Chủy ít gặp ký từ lạ ngay nên trả không mà không báo gì.” (0.786): lệch âm/thanh thuần Việt: chuỗi/chuỷ, kí tự/ký từ — NOT_VERIFIED bằng tai người',
    'B tăng thêm 2 thành 3, nhưng A đã kiểm xong rồi.':
        'ASR chép “V tăng thêm 2 thành 3, nhưng A đã kiểm xong rồi.” (0.917): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    # ── Đợt A đào sâu: LLM, SWF, SEC, SDP, CLD (2026-10-31, lượt 3) ──
    'V giảm thật sự vì phần dư khi chia cho b luôn nhỏ hơn b, nên b mới nhỏ hơn b cũ.':
        'ASR chép “Vế giảm thật sự vì phần dư khi chia cho bê luôn nhỏ hơn bê, nên bê mới nhỏ hơn bê cũ.” (0.955): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Đơn dưới 500 nghìn và 3 ki-lô-mét không vượt 5, nên phí giao là 15 nghìn.':
        'ASR chép “đơn giới 500.000 và 3 km không vực năm nên phí giao là 15.000.” (0.789): “ki-lô-mét” ASR viết ký hiệu “km” (đúng); mọi con số khớp; dưới/giới, vượt/vực lệch phụ âm đầu và thanh — NOT_VERIFIED bằng tai người',
    'Trước hết, ôn phân số ra số thập phân.':
        'ASR chép “Trước hết, ông phần số ra số thập phân.” (0.778): lệch âm/thanh thuần Việt: ôn phân/ông phần — NOT_VERIFIED bằng tai người',
    'Z chỉ sang W, nên có 1 mũi tên đi ra, tức Z dựa vào một mô-đun.':
        'ASR chép “Giác chỉ sang về đúc nên có một mũi tên đi ra tức giác dựa vào một mô đun.” (0.919): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Một mi li giây bằng 1000 mi-crô giây, nên 0 phẩy 5 mi li giây bằng 500 mi-crô giây.':
        'ASR chép “Một mili dây bằng 1.000 micro dây nên không phải 5 mili dây bằng 500 micro dây.” (0.476): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải” — NOT_VERIFIED bằng tai người',
    'Vậy 500 mi-crô giây bằng 500 nhân 1000, tức 500 nghìn na-nô giây.':
        'ASR chép “Vậy 500 micro dây bằng 500 nhân 1 nghìn, tức 500 nghìn nano dây.” (0.722): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh — NOT_VERIFIED bằng tai người',
    'Một mi li giây bằng một triệu na-nô giây.':
        'ASR chép “1 mili giấy bằng 1 triệu nano giấy.” (0.444): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh — NOT_VERIFIED bằng tai người',
    'Mỗi mũi tên đứt nét là một vòng khứ hồi qua mạng, cỡ 500 mi-crô giây, và có thể mất, hết giờ hoặc bị lặp lại.':
        'ASR chép “Mỗi mũi tên đức nét là một vòng khứ hồi qua mạng, cỡ 500 micro dây và có thể mất, hết giờ hoặc bị lập lại.” (0.836): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; lệch âm/thanh thuần Việt: đứt/đức, lặp/lập — NOT_VERIFIED bằng tai người',
    'Một dịch vụ tốn 500 mi-crô giây, tức 0 phẩy 5 mi li giây.':
        'ASR chép “Một dịch vụ tốn 500 micro dây, tức 0,5 mili dây.” (0.667): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh — NOT_VERIFIED bằng tai người',
    'Hai dịch vụ tốn 1000 mi-crô giây, tức 1 mi li giây.':
        'ASR chép “2 dịch vụ tốn 1 ngàn micro dây tức 1 mili dây.” (0.615): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh — NOT_VERIFIED bằng tai người',
    'Cùng 10 bước ấy là 10 lời gọi hàm, dù rộng tay cho mỗi lời gọi 100 na-nô giây thì tổng cũng chỉ 1 mi-crô giây, và không hỏng giữa chừng.':
        'ASR chép “Cùng 10 bước ấy là 10 lời gọi hàm, dù động tay cho mỗi lời gọi 100 nano dây thì tổng cũng chỉ 1 micro dây và không hỏng giữa chân.” (0.788): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; lệch âm/thanh thuần Việt: rộng/động, chừng/chân — NOT_VERIFIED bằng tai người',
    'Bên vi dịch vụ là 5000 mi-crô giây, và lời gọi nào cũng có thể mất, hết giờ, hoặc tới nơi mà phản hồi thì lạc.':
        'ASR chép “Bên vi dịch vụ là 5.000 microj và lời gọi nào cũng có thể mất hết giờ hoặc tới nơi mà phản hồi thi lạc.” (0.889): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; lệch âm/thanh thuần Việt: thì/thi — NOT_VERIFIED bằng tai người',
    'Đổi 5 mi li giây ra 5 triệu na-nô giây rồi chia cho 100, được 50 nghìn lần đọc bộ nhớ, đúng bằng 10 lần 5000.':
        'ASR chép “Đổi 5 mili dây ra 5 triệu nano dây rồi chia cho 100, được 50 nghìn lần độc bộ nhớ, đúng bằng 10 lần 5 nghìn.” (0.793): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; lệch âm/thanh thuần Việt: đọc/độc — NOT_VERIFIED bằng tai người',
    'Đổi 500 mi-crô giây ra 0 phẩy 5 mi li giây trước rồi mới nhân 10, vẫn ra 5 mi li giây.':
        'ASR chép “Đổi 500 micro dây ra 0.5 mili dây trước rồi mới nhân 10, vẫn ra 5 mili dây.” (0.636): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải” — NOT_VERIFIED bằng tai người',
    'Đổi 5 mi li giây ra 5000 mi-crô giây rồi chia cho 1 mi-crô giây của nguyên khối, lại ra tỉ lệ 5000 lần.':
        'ASR chép “Đổi 5 mili dây ra 5.000 micro dây rồi chia cho 1 micro dây của nguyên khối, lại ra tỷ lệ 5.000 lần.” (0.679): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; “tỉ” ASR viết chính tả “tỷ” (cùng âm) — NOT_VERIFIED bằng tai người',
    'Giỏ 50 món hỏi tồn kho, trong nguyên khối là 50 lời gọi hàm, chỉ cỡ 5 mi-crô giây.':
        'ASR chép “Giỏ 50 món hỏi tồn khô, trong nguyên khối là 50 lời gọi hàm, chỉ cỡ 5 micro dây.” (0.837): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; lệch âm/thanh thuần Việt: kho/khô — NOT_VERIFIED bằng tai người',
    'Bước một, ta đếm xem container thấy riêng những gì.':
        'ASR chép “Bước 1, ta đếm xem cần tenner thấy riêng những gì.” (0.857): container đọc thô (probe CLD p1: 5/8, small viết “cần tên nơi”) — NOT_VERIFIED bằng tai người',
    'Cả ba chạy trên cùng một nhân, nên không container nào phải mang một hệ điều hành riêng.':
        'ASR chép “Cả ba chạy trên cùng một nhân, nên không cần tay nơi nào phải mang một hệ điều hành riêng.” (0.895): container đọc thô (probe CLD p1: 5/8, small viết “cần tên nơi”) — NOT_VERIFIED bằng tai người',
    'Bước bốn, bảng so container với máy ảo theo ba tiêu chí.':
        'ASR chép “Bước 4, bạn so cần tenor với máy ảo theo 3 tiêu chí.” (0.8): container đọc thô (probe CLD p1: 5/8, small viết “cần tên nơi”); lệch âm/thanh thuần Việt: bảng/bạn — NOT_VERIFIED bằng tai người',
    'Lỗi thứ tư hay gặp ở người đã đi làm, bỏ giới hạn bộ nhớ để container khỏi bị giết.':
        'ASR chép “Lỗi thứ tư hay gặp ở người đã đi làm, bỏ giới hạn bộ nhớ để cần tenner khỏi bị giết.” (0.927): container đọc thô (probe CLD p1: 5/8, small viết “cần tên nơi”) — NOT_VERIFIED bằng tai người',
    'Giả sử máy 4096 MB, container A rò rỉ bộ nhớ và phình tới 3500 MB, còn B và C cần 512 MB mỗi cái.':
        'ASR chép “Giả sử máy 4.096 MB, cần thay nơ A đò rỉ bộ nhớ và phìn tới 3.500 MB, còn B và C cần 512 MB mỗi cái.” (0.895): container đọc thô (probe CLD p1: 5/8, small viết “cần tên nơi”); lệch âm/thanh thuần Việt: rò/đò, phình/phìn — NOT_VERIFIED bằng tai người',
    'Câu hai, container không mang nhân riêng mà gọi thẳng vào nhân của máy chủ, nên máy chủ phải có đúng loại nhân mà container cần.':
        'ASR chép “Câu 2, cần tenner không mang nhân riêng mà gọi thẳng vào nhân của máy chủ, nên máy chủ phải có đúng loại nhân mà cần tenner cần.” (0.889): container đọc thô (probe CLD p1: 5/8, small viết “cần tên nơi”) — NOT_VERIFIED bằng tai người',
    'Chỉ đổi một chữ thành a b d, mã đổi hẳn, bắt đầu bằng a 5 2 d.':
        'ASR chép “Chỉ đổi một chữ thành abv, mả đổi hẳn, bắt đầu bằng a52v.” (0.743): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: mã (trong “a b d mã” → “abv mả”) — NOT_VERIFIED bằng tai người',
    'Bộ điều khiển so hai ô, thấy thiếu 3 trừ 2 bằng 1, nên hành động tạo 1 Pod mới, và thực tế về lại 3.':
        'ASR chép “Bộ điều khiển so 2 ô thấy thiếu 3 trừ 2 bằng 1 nên hành động tạo một pốc mới và thực tế về lại 3.” (0.962): Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút) — NOT_VERIFIED bằng tai người',
    'Bộ điều khiển không cần biết vì sao mất Pod, chỉ cần biết thiếu bao nhiêu.':
        'ASR chép “Bộ điều khiển không cần biết vì sao mất pốt, chỉ cần biết thiếu bao nhiêu.” (0.938): Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút) — NOT_VERIFIED bằng tai người',
    'Nếu mong muốn trừ thực tế là số dương, như 3 trừ 1 bằng 2, thì tạo 2 Pod.':
        'ASR chép “Nếu mong muốn trừ thực tế là số dương, như 3 trừ 1 bằng 2 thì tạo 2 pút.” (0.947): Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút) — NOT_VERIFIED bằng tai người',
    'Nếu là số âm, ví dụ vì lý do nào đó thực tế là 4, thì 3 trừ 4 bằng âm 1, nên xoá bớt 1 Pod.':
        'ASR chép “Nếu là số âm, ví dụ vì lý do nào đó thực tế là 4 thì 3 trừ 4 bằng âm 1 nên xóa bớt 1 phút.” (0.963): Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút) — NOT_VERIFIED bằng tai người',
    'Cuối nhịp nào cũng về 3, nên thực tế của mỗi nhịp là 3 trừ số Pod chết, tức 2, 3 và 1, khớp với bảng.':
        'ASR chép “Cuối nhịp nào cũng về ba nên thực tế của mỗi nhịp là ba trừ số pốt chất, tức hai, ba và một, khớp với bản.” (0.885): Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút); lệch âm/thanh thuần Việt: chết (trong “pod chết” → “pốt chất”), bảng/bản — NOT_VERIFIED bằng tai người',
    'Cũng vì thế, tổng số Pod tạo thêm phải bằng tổng số Pod chết, 1 cộng 0 cộng 2 bằng 3, và máy đếm lại ra đúng 3.':
        'ASR chép “Cũng vì thế, tổng số pốt tạo thêm phải bằng tổng số pốt chất, 1 cộng 0 cộng 2 bằng 3 và máy đếm lại ra đúng 3.” (0.893): Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút); lệch âm/thanh thuần Việt: chết (trong “pod chết” → “pốt chất”) — NOT_VERIFIED bằng tai người',
    'Nhịp một có 2 Pod chết nên thấy 3, mong muốn trừ thực tế bằng 2, nên tạo 2.':
        'ASR chép “Nhịp 1 có 2 phút chết nên thấy 3, mong muốn trừ thực tế bằng 2 nên tạo 2.” (0.947): Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút) — NOT_VERIFIED bằng tai người',
    'Ở bài 5 của khoá này, khi bộ điều khiển thấy thiếu và tạo một Pod mới, bộ xếp lịch là phần chọn nút, tức chọn máy sẽ chạy Pod đó.':
        'ASR chép “Ở bài 5 của khóa này, khi bộ điều khiển thấy thiếu và tạo 1 bốc mới, bộ xếp lịch là phần chọn nút, tức chọn máy sẽ chạy bốc đó.” (0.935): Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút) — NOT_VERIFIED bằng tai người',
    'Mỗi nút đã chạy hai Pod 1 phẩy 5 CPU, nên nút nào cũng chỉ trống 1 CPU.':
        'ASR chép “Mỗi nút đã chạy 2 pốt 1,5 CPU nên nút nào cũng chỉ trống 1 CPU.” (0.944): Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút) — NOT_VERIFIED bằng tai người',
    'Nhưng Pod mới cần 1 phẩy 5 CPU trên một nút, nên không vừa nút nào cả, vì bộ xếp lịch phải tìm một nút còn đủ chỗ chứ không gom phần trống của nhiều nút.':
        'ASR chép “Nhưng Poc mới cần 1,5 CPU trên 1 nút, nên không vừa nút nào cả vì bộ xếp lịch phải tìm 1 nút còn đủ chỗ chứ không gom phần trống của nhiều nút.” (0.972): Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút) — NOT_VERIFIED bằng tai người',
    'Bước hai, đặt từng Pod để thấy phần thừa.':
        'ASR chép “Bước 2, đặt từng pốt để thấy phần thừa.” (0.889): Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút) — NOT_VERIFIED bằng tai người',
    'Vì Pod thứ ba cần 1 phẩy 5 mà nút chỉ còn 1, nên một phần tư nút bị bỏ không.':
        'ASR chép “Vì pốt thứ 3 cần 1,5 mà nút chỉ còn 1 nên 1 phần tư nút bị bỏ không?” (0.952): Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút) — NOT_VERIFIED bằng tai người',
    'Chỉ có Pod lớn thì nút còn trống 1.':
        'ASR chép “Chỉ có bút lớn thì nút còn trống một.” (0.889): Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút) — NOT_VERIFIED bằng tai người',
    'Thêm một Pod nhỏ 1 CPU thì nút giữ đủ 4, không còn trống.':
        'ASR chép “Thêm 1 phút nhỏ 1 CPU thì nút giữ đủ 4, không còn trống.” (0.929): Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút) — NOT_VERIFIED bằng tai người',
    'Bước bốn, thật ra mỗi Pod yêu cầu nhiều loại tài nguyên cùng lúc.':
        'ASR chép “Bước 4. Thật ra mỗi phút yêu cầu nhiều loại tài nguyên cùng lúc.” (0.929): Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút) — NOT_VERIFIED bằng tai người',
    'Nút có 4 CPU và 8 GB bộ nhớ, Pod yêu cầu 1 CPU và 3 GB.':
        'ASR chép “Núc có 4 CPU và 8GB bộ nhớ, pốc yêu cầu 1 CPU và 3GB.” (0.882): Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút); lệch âm/thanh thuần Việt: nút/núc — NOT_VERIFIED bằng tai người',
    'Chỉ xét CPU thì vừa 4 Pod, chỉ xét bộ nhớ thì phần nguyên của 8 chia 3 là 2, dư 2 GB.':
        'ASR chép “Chỉ xét CPU thì vừa 4 pút, chỉ xét bộ nhớ thì phần nguyên của 8x3 là 2, dù 2GB.” (0.87): Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút); lệch âm/thanh thuần Việt: chia/x, dư/dù — NOT_VERIFIED bằng tai người',
    'Pod phải vừa cả hai, nên chỉ đặt được 2, là số nhỏ hơn.':
        'ASR chép “Phúc phải vừa cả 2, nên chỉ đặt được 2 là số nhỏ hơn.” (0.929): Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút) — NOT_VERIFIED bằng tai người',
    'Lý do là 8 chia 2 phẩy 5 bằng 3 phẩy 2, ba Pod giữ 7 phẩy 5 CPU, nên còn 8 trừ 7 phẩy 5 bằng 0 phẩy 5.':
        'ASR chép “Lý do là 8 chia 2,5 bằng 3,2, 3 pút giữ 7,5 CPU, nên còn 8 trừ 7,5 bằng 0,5.” (0.967): Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút) — NOT_VERIFIED bằng tai người',
    'Pod thứ ba vào nút hai vì nút một chỉ còn 1, không đủ 1 phẩy 5.':
        'ASR chép “Phúc thứ 3 vào nút 2 vì nút 1 chỉ còn 1, không đủ 1,5.” (0.941): Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút) — NOT_VERIFIED bằng tai người',
    'Đối tượng triển khai khai báo muốn có n bản Pod từ một ảnh, ví dụ muốn 3 bản.':
        'ASR chép “Đối tượng trĩnh khai khai báo muốn có n bản phúc từ một ảnh, ví dụ muốn ba bản.” (0.895): Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút); lệch âm/thanh thuần Việt: triển/trĩnh — NOT_VERIFIED bằng tai người',
    'Vòng điều khiển thấy thiếu thì tạo, thấy thừa thì xoá, nên khi một Pod chết, nó thấy 2 và tạo lại 1 cho đủ 3.':
        'ASR chép “Vòng điều khiển thấy thiếu thì tạo, thấy thừa thì xóa, nên khi một phút chức, nó thấy hai và tạo lại một cho đủ ba.” (0.923): Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút); lệch âm/thanh thuần Việt: chết (trong “pod chết” → “phút chức”) — NOT_VERIFIED bằng tai người',
    'Một Pod chỉ tính là sẵn sàng khi đã khởi động xong và nhận được yêu cầu, Pod vừa tạo còn đang nạp dữ liệu thì chưa sẵn sàng.':
        'ASR chép “Một Phúc chỉ tính là sẵn sàng khi đã khởi động xong và nhận được yêu cầu, Phúc vừa tạo còn đang nạp dữ liệu thì chưa sẵn sàng.” (0.931): Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút) — NOT_VERIFIED bằng tai người',
    'Ô xanh là Pod cũ, ô cam đặc là Pod mới đã sẵn sàng, ô cam đứt nét là Pod mới đang khởi động.':
        'ASR chép “Ô xanh là pốt cũ, ô cam đặt là pốt mới đã sẵn sàng, ô cam đức nét là pốt mới đang khởi động.” (0.792): Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút); lệch âm/thanh thuần Việt: đặc/đặt, đứt/đức — NOT_VERIFIED bằng tai người',
    'Ở mọi hàng, số ô đặc, tức số Pod sẵn sàng, không bao giờ xuống dưới đường xanh lá 8 bản.':
        'ASR chép “Ở mọi hàng, số ô đặc, tức số pốt sẵn sàng không bao giờ xuống dưới đường xanh lá 8 bản.” (0.952): Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút) — NOT_VERIFIED bằng tai người',
    'Pod cũ chỉ bị xoá khi đã có đủ Pod khác sẵn sàng thay chỗ, nên khách không thấy gián đoạn.':
        'ASR chép “Phúc cụ chỉ bị xóa khi đã có đủ phúc khác sẵn sàng thay chỗ nên khách không thấy gián đoạn.” (0.857): Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút); lệch âm/thanh thuần Việt: cũ (trong “pod cũ” → “phúc cụ”) — NOT_VERIFIED bằng tai người',
    'Trong mỗi vòng, lúc Pod mới vừa được tạo mà Pod cũ chưa xoá, tổng số Pod lên tới 13.':
        'ASR chép “Trong mỗi vòng, lúc pốt mới vừa được tạo mà pốt cũ chưa xóa, tổng số pốt lên tới 13.” (0.857): Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút) — NOT_VERIFIED bằng tai người',
    'Không có nửa Pod, nên phải làm tròn, và mỗi tham số làm tròn theo một hướng.':
        'ASR chép “Không có nửa phút nên phải làm tròn và mỗi tham số làm tròn theo một hướng.” (0.941): Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút) — NOT_VERIFIED bằng tai người',
    'Vì vậy có tối đa 10 cộng 3, bằng 13 Pod cùng lúc.':
        'ASR chép “Vì vậy có tối đa 10 cộng 3 bằng 13 phút cùng lúc.” (0.929): Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút) — NOT_VERIFIED bằng tai người',
    'Làm tròn lên cho phép tạo thêm nhiều Pod mới một lúc, nên cập nhật xong nhanh hơn.':
        'ASR chép “Làm tròn lên cho phép tạo thêm nhiều bốc mới một lúc nên cập nhật xong nhanh hơn.” (0.944): Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút) — NOT_VERIFIED bằng tai người',
    'Vòng một tạo 3 Pod mới cho tổng lên 13, rồi xoá 2 Pod cũ, còn 8 Pod cũ sẵn sàng.':
        'ASR chép “Vòng 1 tạo 3 phút mới cho tổng lên 13, rồi xóa 2 phút cũ, còn 8 phút cũ sẵn sang.” (0.818): Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút); lệch âm/thanh thuần Việt: sàng/sang — NOT_VERIFIED bằng tai người',
    'Vòng hai, 3 Pod mới đã sẵn sàng nên xoá được 3 Pod cũ, còn 5, và tạo thêm 2 Pod mới.':
        'ASR chép “Vòng 2, 3 phút mới đã sẵn sàng nên xóa được 3 phút cũ, còn 5 và tạo thêm 2 phút mới.” (0.864): Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút) — NOT_VERIFIED bằng tai người',
    'Vòng ba tạo 3, xoá 2, còn 3 Pod cũ.':
        'ASR chép “Vòng 3 tạo 3, xóa 2, còn 3 pút cũ.” (0.9): Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút) — NOT_VERIFIED bằng tai người',
    'Vòng bốn tạo 2, xoá 3 Pod cũ cuối cùng.':
        'ASR chép “Vòng 4 tạo 2, xóa 3 phút cũ cuối cùng.” (0.9): Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút) — NOT_VERIFIED bằng tai người',
    'Suốt bốn vòng, không lúc nào dưới 8 bản sẵn sàng hay trên 13 Pod, và việc cập nhật xong sau 4 vòng.':
        'ASR chép “Suốt 4 vòng không lúc nào dưới 8 bản sẵn sàng hay trên 13 phút và vì cập nhật xong sau 4 vòng.” (0.917): Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút); lệch âm/thanh thuần Việt: việc/vì — NOT_VERIFIED bằng tai người',
    'Cộng cột tạo được 3 cộng 2 cộng 3 cộng 2, bằng 10 Pod mới, cộng cột xoá cũng được 10 Pod cũ, nên đã thay hết.':
        'ASR chép “Cộng cột tạo được 3 cộng 2 cộng 3 cộng 2 bằng 10 phút mới, cộng cột xóa cũng được 10 phút cũ nên đã thay hết.” (0.926): Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút) — NOT_VERIFIED bằng tai người',
    'Tối đa là 4 cộng 1, bằng 5 Pod.':
        'ASR chép “Tối đa là 4 cộng 1 bằng 5 phút.” (0.889): Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút) — NOT_VERIFIED bằng tai người',
    'Tối đa là 8 cộng 2, bằng 10 Pod.':
        'ASR chép “Tối đa là 8 cộng 2 bằng 10 pốt.” (0.889): Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút) — NOT_VERIFIED bằng tai người',
    'Ở bài 5, đối tượng dịch vụ là một địa chỉ ổn định trỏ tới các Pod đang sống, nên khi Pod chết và Pod mới thay chỗ thì địa chỉ dịch vụ vẫn không đổi.':
        'ASR chép “Ở bài năm, đối tượng dịch vụ là một địa chỉ ổn định trọ tới các phút đang sống, nên khi phút chết và phút mới thay chỗ thì địa chỉ dịch vụ vẫn không đổi.” (0.889): Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút); lệch âm/thanh thuần Việt: trỏ/trọ — NOT_VERIFIED bằng tai người',
    'Khách không nhớ địa chỉ Pod nào, mà hỏi tên đơn hàng và nhận về địa chỉ ổn định của dịch vụ.':
        'ASR chép “Khách không nhớ địa chỉ post nào mà hỏi tên đơn hàng và nhận về địa chỉ ổn định của dịch vụ.” (0.955): Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút) — NOT_VERIFIED bằng tai người',
    'Sau địa chỉ đó là bộ cân bằng, và danh sách Pod phía sau được cập nhật tự động khi Pod đổi.':
        'ASR chép “Sau địa chỉ đó là bộ cân bằng và danh sách phúc phía sau được cập nhật tự động khi phúc đổi.” (0.909): Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút) — NOT_VERIFIED bằng tai người',
    'Với cách chọn tốt hơn trong hai, bộ cân bằng bốc ngẫu nhiên 2 máy, ở đây là Pod 1 tải 5 và Pod 2 tải 3.':
        'ASR chép “Với cách chọn tốt hơn trong 2, bộ cân bằng bốc ngẫu nhiên 2 máy, ở đây là phút 1 tại 5 và phút 2 tại 3.” (0.852): Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút); lệch âm/thanh thuần Việt: tải/tại, tải/tại — NOT_VERIFIED bằng tai người',
    'Nó gửi yêu cầu tới Pod 2 vì ít tải hơn, còn Pod 3 lần này không được bốc.':
        'ASR chép “Nó gửi yêu cầu tới pốt 2 vị ích tải hơn, còn pốt 3 lần này không được bốc.” (0.842): Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút); lệch âm/thanh thuần Việt: vì/vị — NOT_VERIFIED bằng tai người',
    'Làm thử khi gần như không có tải, lam-đa xấp xỉ 0, thì W bằng 1 phần 100 giây, tức 10 mi li giây.':
        'ASR chép “Làm thử khi gần như không có tải, làm đa xắp xỉ không, thì về đúc bằng 1 phần 100 giây, tức 10 mili giây.” (0.808): lam-đa (λ), ASR viết “lambda”; chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; lệch âm/thanh thuần Việt: xấp/xắp — NOT_VERIFIED bằng tai người',
    'Bước ba, dùng định luật Little để đếm số yêu cầu trong hệ.':
        'ASR chép “Bước 3 Dùng định lực liết tồ để đếm số yêu cầu trong hệ.” (0.815): Little đọc thô (probe CLD p1: 5/8, ASR viết “lít tồ”); lệch âm/thanh thuần Việt: luật (trong “luật little” → “lực liết tồ”) — NOT_VERIFIED bằng tai người',
    'Đảo định luật Little ở tải 95, W bằng 19 chia 95 giây, đúng 200 mi li giây.':
        'ASR chép “Đảo định lực liếc tổ ở tải 95, về đút bằng 19 chia 95 giây, đúng 200 mili giây.” (0.776): Little đọc thô (probe CLD p1: 5/8, ASR viết “lít tồ”); chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; lệch âm/thanh thuần Việt: luật (trong “luật little” → “lực liếc tổ”) — NOT_VERIFIED bằng tai người',
    'Thời gian chờ bằng rô chia muy trừ lam-đa, tức 0 phẩy 8 chia 20 giây, bằng 40 mi li giây, cộng 10 mi li giây phục vụ là 50.':
        'ASR chép “Thời gian chờ bằng row chi mươi trừ lambda tức 0,8 chia 20 giây bằng 40 ms cộng 10 ms phục vụ là 50.” (0.781): muy (μ) ASR viết “my/nguy”; tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; lệch âm/thanh thuần Việt: rô chia (trong “rô chia muy” → “row chi mươi”) — NOT_VERIFIED bằng tai người',
    'Ta đảo định luật Little, lấy 30 yêu cầu trong hệ chia cho tốc độ đến 600 mỗi giây.':
        'ASR chép “Ta đảo định luật liếc tồ lấy 30 yêu cầu trong hệ chia cho tốc độ đến 600 mũi dây.” (0.884): Little đọc thô (probe CLD p1: 5/8, ASR viết “lít tồ”); lệch âm/thanh thuần Việt: mỗi/mũi — NOT_VERIFIED bằng tai người',
    'Cách này luôn dùng được, vì định luật Little đúng cho mọi hệ ổn định.':
        'ASR chép “Cách này luôn dùng được vì định lực lít tô đúng cho mọi hệ ổn định.” (0.839): Little đọc thô (probe CLD p1: 5/8, ASR viết “lít tồ”); lệch âm/thanh thuần Việt: luật (trong “luật little” → “lực lít tô”) — NOT_VERIFIED bằng tai người',
    'Điều thứ hai, mã cơ số 64 là cách viết byte bằng chữ cái.':
        'ASR chép “Điều thứ 2, mạ cơ số 64 là cách viết bay bằng chữ Cái.” (0.875): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: mã/mạ — NOT_VERIFIED bằng tai người',
    'Ba byte cho 4 chữ.':
        'ASR chép “3 bài cho 4 chữ.” (0.8): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Năm byte cần 2 nhóm, làm tròn lên, nên ra 8 chữ, dấu bằng ở cuối chỉ để đệm cho đủ nhóm.':
        'ASR chép “Năm bay cần hai nhóm, làm tròn linh, nên ra tám chữ, giấu bằng ở cuối chỉ để đệm cho đủ nhóm.” (0.909): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: lên/linh — NOT_VERIFIED bằng tai người',
    'Bảy byte cần 3 nhóm, nên ra 12 chữ.':
        'ASR chép “7 bai cần 3 nhóm nên ra 12 chữ.” (0.9): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Bước ba, hệ tệp ghép lúc chạy đi từ dưới lên.':
        'ASR chép “Bước ba, hãy tạp ghép lúc chạy đi từ dưới lân.” (0.727): lệch âm/thanh thuần Việt: hệ tệp/hãy tạp, lên/lân — NOT_VERIFIED bằng tai người',
    'Chương trình chạy trong container không mở được tệp mật khẩu nữa.':
        'ASR chép “Chương trình chạy trong cân tay nơ không mở được tạp mật khẩu nữa.” (0.769): container đọc thô (probe CLD p1: 5/8, small viết “cần tên nơi”); lệch âm/thanh thuần Việt: tệp/tạp — NOT_VERIFIED bằng tai người',
    'Liệt kê thẳng tệp nén của lớp hai, không ghép lớp nào, ta thấy một tệp 16 byte có chứa mật khẩu.':
        'ASR chép “Liệt kê thẳng tập nén của lớp 2, không ghép lớp nào, ta thấy 1 tập 16 bai có chứa mật khẩu.” (0.87): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: tệp/tập, tệp/tập — NOT_VERIFIED bằng tai người',
    'Tám chữ là hai nhóm, ứng với 6 byte, trừ một byte đệm còn 5 byte.':
        'ASR chép “Tám chữ là 2 nhóm, ứng với 6 bai, trừ 1 bai đệm còn 5 bai.” (0.812): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    # ── Đợt A đào sâu: DSY ──
    'P2 cũng có một sự kiện cục bộ, nhãn 1.':
        'ASR chép “Thế 2 cũng có một sự kiện cục bộ nhãn một.” (0.909): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Bước bốn, P3 chưa có sự kiện nào, đồng hồ là 0.':
        'ASR chép “Bước 4, về 3 chưa có sự kiện nào, đồng hồ là không?” (0.923): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Chuỗi kia, P2 cục bộ rồi P2 nhận, chỉ có 2, nên nhãn là 3, khớp.':
        'ASR chép “Chủy kia, P2 cuộc bộ rồi P2 nhận, chỉ có 2, nên nhẳng là 3, khúp.” (0.778): lệch âm/thanh thuần Việt: chuỗi/chuỷ, cục/cuộc, nhãn/nhẳng, khớp/khúp — NOT_VERIFIED bằng tai người',
    'P2 chưa có sự kiện nào nên đồng hồ là 0, khi nhận m thì lấy số lớn hơn giữa 0 và 3, cộng 1, được 4.':
        'ASR chép “T2 chưa có sự kiện nào nên đồng hồ là không, khi nhận m thì lấy số lớn hơn giữa 0 và 3, cộng 1 được 4.” (0.964): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Câu hai, P2 đang ở 7, thông điệp mang nhãn 1, số lớn hơn giữa 7 và 1, cộng 1, bằng 8, vì đồng hồ không bao giờ lùi.':
        'ASR chép “Câu 2, T2 đang ở 7, thông điệp mang nhãn 1, số lớn hơn giữa 7 và 1, cộng 1 bằng 8 vì đồng hồ không bao giờ lui.” (0.933): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: lùi/lui — NOT_VERIFIED bằng tai người',
    'Sự kiện cục bộ hay gửi thì C tăng 1, ví dụ từ 2 lên 3.':
        'ASR chép “Sự kiện cục bộ hay gửi thì sẽ tăng mục, ví dụ từ 2 lên 3.” (0.875): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: một/mục — NOT_VERIFIED bằng tai người',
    'Rồi việc nhận cũng là một sự kiện của P2, nên ô của P2 tăng lên, được 1, 2, 0, tức P2 biết một việc của P1 và hai việc của mình.':
        'ASR chép “Rồi việc nhận cũng là một sự kiện của P2, nền O của P2 tăng lên, được 1, 2, 0, tức P2 biết một việc của P1 và hai việc của mình.” (0.944): “ô” (ô lưới) ASR viết chữ “O”; lệch âm/thanh thuần Việt: nên (trong “nên ô” → “nền o”) — NOT_VERIFIED bằng tai người',
    'Bước ba, P2 nhận thông điệp từ P1.':
        'ASR chép “Bước 3, T2 nhận thông điệp từ P1.” (0.9): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Nhãn Lamport của hai sự kiện cuối đều là 2, không phân biệt được gì, còn đồng hồ vector cho biết chắc chúng đồng thời.':
        'ASR chép “Nhãn lam por của hai sự kiện cuối đều là hai, không phân biệt được gì, còn đồng hồ vét tơ cho biết chắc chúng đồng thời.” (0.963): lệch âm/thanh thuần Việt: po/por — NOT_VERIFIED bằng tai người',
    'Nếu mỗi số chiếm 8 byte, ba máy sao chép nhận ghi chỉ cần 3 thành phần, tức 24 byte kèm mỗi bản ghi.':
        'ASR chép “Nếu mỗi số chiếm 8 bay, bà máy sao chép nhận ghi chỉ cần 3 thành phần, tức 24 bay kèm mỗi bảng ghi.” (0.846): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: ba (trong “byte ba” → “bay bà”), bản/bảng — NOT_VERIFIED bằng tai người',
    'Một triệu máy khách thì cần một triệu thành phần, tức 8 triệu byte kèm mỗi bản ghi.':
        'ASR chép “1 triệu máy khách thì cần 1 triệu thành phần, tức 8 triệu bay kèm mỗi bản ghi” (0.944): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Bước một, lấy N bằng 3 và W bằng 2, lệnh ghi x bằng v2 xong khi máy 1 và máy 2 xác nhận, còn máy 3 vẫn giữ v1.':
        'ASR chép “Bước 1, lấy N bằng 3 và V đúc bằng 2, lệnh ghi ít bằng V2 xong khi máy 1 và máy 2 xác nhận, còn máy 3 vẫn giữ V1.” (0.954): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Bước hai, giữ W bằng 2 nhưng chỉ đọc một máy.':
        'ASR chép “Bước 2, giữ vây đúc bằng 2 nhưng chỉ đọc một máy.” (0.87): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Với N bằng 3, R và W bằng 2, có 9 cặp đọc và ghi, không cặp nào rời nhau, khớp với luôn gặp.':
        'ASR chép “Với N bằng 3, R và V đúc bằng 2, có 9 cặp độc và ghi, không cặp nào rời nhau, khớp với luôn gặp.” (0.898): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: đọc/độc — NOT_VERIFIED bằng tai người',
    'Với R bằng 1 và W bằng 2, cũng có 9 cặp, trong đó đúng 3 cặp rời nhau, vì mỗi máy đọc lẻ có đúng một tập ghi không chứa nó.':
        'ASR chép “Với error bằng 1 và vi đúc bằng 2 cũng có 9 cặp, trong đó đúng 3 cặp rời nhau vì mỗi máy đọc lẽ có đúng 1 tập ghi không chứa nó.” (0.892): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: linh/lẽ — NOT_VERIFIED bằng tai người',
    'Với N bằng 5, R và W bằng 3, có 10 nhân 10, bằng 100 cặp, không cặp nào rời nhau.':
        'ASR chép “Với N bằng 5, R và V đúc bằng 3, có 10 nhân 10 bằng 100 cặp, không cặp nào rời nhau.” (0.933): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Lỗi thứ tư hay gặp ở người đã đi làm, thấy ghi chậm thì hạ W xuống 1, trong khi đọc vẫn chỉ hỏi một máy.':
        'ASR chép “Lỗi thứ tư hay gặp ở người đã đi làm, thấy ghi chậm thì hạ về đút xuống một, trong khi độc vẫn chỉ hỏi một máy.” (0.906): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: đọc/độc — NOT_VERIFIED bằng tai người',
    'Giả sử ba bản sao trả lời sau 1, 20 và 150 mi li giây, thì ghi chỉ phải chờ bản xác nhận thứ W, tức 1, 20 hoặc 150 mi li giây.':
        'ASR chép “Giả sử 3 bản sao trả lời sau 1, 20 và 150 mili giây thì ghi chỉ phải chờ bản xác nhận thứ về đúc, tức 1, 20 hoặc 150 mili giây.” (0.889): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Hạ W xuống 1 đúng là nhanh nhất, nhưng 1 cộng 1 không lớn hơn 3, nên đọc có thể gặp bản cũ.':
        'ASR chép “Hạ với Đúc xuống một đúng là nhanh nhất, nhưng một cộng 1 không lớn hơn 3 nên đọc có thể gặp bản cũ.” (0.936): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Cách của người có kinh nghiệm là giữ W bằng 2 và R bằng 2.':
        'ASR chép “Cách của người có kinh nghiệm là giữ V đúc bằng 2 và R bằng 2.” (0.903): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Câu hai, với R bằng 2 và W bằng 4.':
        'ASR chép “Câu 2, với R bằng 2 và V đúc bằng 4.” (0.857): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Ghi xong khi W bản xác nhận, đọc thì hỏi R bản, và nếu R cộng W lớn hơn N thì đọc luôn gặp bản mới nhất.':
        'ASR chép “Ghi xong khi VDUK bản xác nhận, đọc thì hỏi R bản, và nếu R cộng VDUK lớn hơn N thì đọc luôn gặp bản mới nhất.” (0.926): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Chọn R và W cùng bằng 3, tức hơn một nửa, gọi là đa số, thì tổng 6 lớn hơn 5, đọc luôn gặp ghi.':
        'ASR chép “Chọn R và V đút cùng bằng 3, tức hơn một nửa, gọi là đa số, thì tổng 6 lớn hơn 5, đọc luôn gặp ghi.” (0.941): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Hàng giữa là máy giữ khoá khi có 4 máy, tức k chia 4 lấy dư, hàng dưới là máy khi có 5 máy, tức k chia 5 lấy dư.':
        'ASR chép “Hàng giữa là máy giữ khóa khi có 4 máy, tất cả chia 4 lấy dư. Hàng dưới là máy khi có 5 máy, tất cả chia 5 lấy dư.” (0.867): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: tức (trong “tức k” → “tất cả”), tức (trong “tức k” → “tất cả”) — NOT_VERIFIED bằng tai người',
    'Máy a nhận danh sách 1, 1, 1, hoặc 2 và 1 nếu đã gộp sớm.':
        'ASR chép “Mấy ai nhận danh sách 1, 1, 1, hoặc 2 và 1 nếu đã gột sớm?” (0.812): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: máy (trong “máy a” → “mấy ai”), gộp/gột — NOT_VERIFIED bằng tai người',
    'Từ lặp càng nhiều, gộp sớm càng bớt nhiều cặp phải gửi.':
        'ASR chép “Tự lập càng nhiều, gột sớm càng bớt nhiều cặp phải gửi.” (0.75): lệch âm/thanh thuần Việt: từ lặp/tự lập, gộp/gột — NOT_VERIFIED bằng tai người',
    'Ánh xạ phát mỗi từ kèm số 1, ba cặp cho mỗi dòng.':
        'ASR chép “Ánh xả phát mũi từ kèm số 1, 3 cặp cho mũi dòng.” (0.769): lệch âm/thanh thuần Việt: xạ/xả, mỗi/mũi, mỗi/mũi — NOT_VERIFIED bằng tai người',
    'Thứ nhất, đổi đơn vị, 1 byte gồm 8 bit.':
        'ASR chép “Thứ nhất, đổi đơn vị, một bay gồm 8 bit.” (0.9): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Chia cho 8 được 1 phẩy 25 tỉ byte, tức 1 phẩy 25 ghi-ga-byte, đúng con số ở phần mở đầu.':
        'ASR chép “chia cho 8 được 1,25 tỷ bay, tức 1,25 gigabyte, đúng còn số ở phần mở đầu.” (0.808): “tỉ” ASR viết chính tả “tỷ” (cùng âm); byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); GB đọc “ghi-ga-byte” theo lexicon của khoá, ASR viết “GB/gigabyte”; lệch âm/thanh thuần Việt: con/còn — NOT_VERIFIED bằng tai người',
    'Khoá 33 cũng cho 3, trùng với 23, vì khoá khác nhau vẫn có thể rơi vào cùng một ô.':
        'ASR chép “Khóa 33 cũng cho 3, trùng với 23, vì khóa khác nhau vẫn có thể rơi vào cùng một cô.” (0.958): “ô” (ô lưới) ASR viết chữ “O” — NOT_VERIFIED bằng tai người',
    'Một lần băm bật đúng 1 trong m bit, nên một bit cố định không bị lần băm đó bật với xác suất 1 trừ 1 phần m.':
        'ASR chép “Một lần băm bật đúng mục trong mbit, nên mục bit cố định không bị lần băm đó bật với sát suốt 1 trừ 1 phần m.” (0.8): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: một/mục, bit (trong “m bit” → “mbit”), một/mục, xác suất/sát suốt — NOT_VERIFIED bằng tai người',
    'Từng bước, tổng số bit là 100 triệu nhân 8, tức 800 triệu bit, rồi chia cho 8 để đổi ra byte.':
        'ASR chép “Từng bước, tổng số biết là 100 triệu nhân 8, tức 800 triệu biết, rồi chia cho 8 để đổi ra bay.” (0.875): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: bit/biết, bit/biết — NOT_VERIFIED bằng tai người',
    'Trong bài này, một ghi-ga-byte là 10 mũ 9 byte, tức một tỉ byte.':
        'ASR chép “Trong bài này, một gigabyte là mười mũ chín byte, tức một tỷ byte.” (0.8): GB đọc “ghi-ga-byte” theo lexicon của khoá, ASR viết “GB/gigabyte”; “tỉ” ASR viết chính tả “tỷ” (cùng âm) — NOT_VERIFIED bằng tai người',
    'Một cột có 100 triệu dòng, mỗi ô 8 byte, là 10 mũ 8 nhân 8, bằng 8 nhân 10 mũ 8 byte, tức 0 phẩy 8 ghi-ga-byte.':
        'ASR chép “Một cô có 100 triệu dòng, mỗi ô 8 bài là 10 mũ 8x8, bằng 8 nhân 10 mũ 8 bài, tức không phải 8 ghi gà bay.” (0.774): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; GB đọc “ghi-ga-byte” theo lexicon của khoá, ASR viết “GB/gigabyte”; lệch âm/thanh thuần Việt: cột/cô, nhân/x — NOT_VERIFIED bằng tai người',
    'Cả 8 cột thì gấp 8 lần, bằng 6 phẩy 4 ghi-ga-byte.':
        'ASR chép “Cả 8 cột thì gấp 8 lần, bằng 6,4 GB.” (0.846): GB đọc “ghi-ga-byte” theo lexicon của khoá, ASR viết “GB/gigabyte” — NOT_VERIFIED bằng tai người',
    'Bước một, xét cột nước của 10 dòng.':
        'ASR chép “Bước 1 sẽ cột nước của mưu dòng.” (0.75): lệch âm/thanh thuần Việt: xét/sẽ, mười/mưu — NOT_VERIFIED bằng tai người',
    'Tính lại 6 phẩy 4 ghi-ga-byte theo từng dòng, mỗi dòng có 8 cột, nhân 8 byte bằng 64 byte.':
        'ASR chép “Tính lại 6,4 GB theo từng dòng, mỗi dòng có 8 cột, nhân 8 by bằng 64 by.” (0.826): GB đọc “ghi-ga-byte” theo lexicon của khoá, ASR viết “GB/gigabyte”; byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Nhân 100 triệu dòng được 6 phẩy 4 ghi-ga-byte, và chia cho 0 phẩy 8 thì được 8, đúng bằng số cột.':
        'ASR chép “Nhưng 100 triệu dòng được 6,4 GB và chia cho 0,8 thì được 8, đúng bằng số cầu.” (0.833): GB đọc “ghi-ga-byte” theo lexicon của khoá, ASR viết “GB/gigabyte”; lệch âm/thanh thuần Việt: nhân/nhưng, cột/cầu — NOT_VERIFIED bằng tai người',
    'Vì theo dòng phải đọc cả 10 cột, 10 mũ 8 nhân 10 nhân 4, bằng 4 nhân 10 mũ 9 byte.':
        'ASR chép “Vì theo dòng phải đọc cả 10 cột, 10 mũ 8 nhân 10 nhân 4, bằng 4 nhân 10 mũ 9 bay.” (0.955): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Còn theo cột chỉ đọc 2 cột, 10 mũ 8 nhân 2 nhân 4, bằng 8 nhân 10 mũ 8 byte.':
        'ASR chép “Còn theo cục chỉ đọc 2 cục, 10 mũ 8 nhân 2 nhân 4 bằng 8 nhân 10 mũ 8 vai.” (0.857): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: cột/cục, cột/cục — NOT_VERIFIED bằng tai người',
    'Vì không phân biệt được hai khả năng, A phải chờ.':
        'ASR chép “vì không phân biệt được hai khả năng, à, phải chờ.” (0.909): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    # ── Đợt A đào sâu: DBS ──
    'Có An, mã 1.':
        'ASR chép “Có an, mã mục” (0.75): lệch âm/thanh thuần Việt: một/mục — NOT_VERIFIED bằng tai người',
    'Và Bình, mã 2.':
        'ASR chép “và bình mả 2.” (0.75): lệch âm/thanh thuần Việt: mã/mả — NOT_VERIFIED bằng tai người',
    'Dòng chữ cam nhắc rằng ta viết mệnh đề lấy cột trước, nhưng hệ quản trị chạy mệnh đề lấy bảng trước.':
        'ASR chép “Dòng chữ cam nhắc rằng ta viết mệnh để lấy cực trước, nhưng hãy quản trị chạy mệnh để lấy bản trước.” (0.773): lệch âm/thanh thuần Việt: đề/để, cột/cực, hệ/hãy, đề/để, bảng/bản — NOT_VERIFIED bằng tai người',
    'K1 xuất hiện hai lần nên còn một, cộng với K2 và giá trị rỗng, được 3 dòng.':
        'ASR chép “Cà màu xuất hiện hai lần nên còn một, cộng với cà hai và giá trị rỏng, được ba dòng.” (0.8): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: một (trong “k một” → “cà màu”), rỗng/rỏng — NOT_VERIFIED bằng tai người',
    'Câu hai, dò từng điểm so với 9.':
        'ASR chép “Câu 2 do từng điểm so với chính.” (0.75): lệch âm/thanh thuần Việt: dò/do, chín/chính — NOT_VERIFIED bằng tai người',
    'K2 chỉ có Chi nên trung bình 9.':
        'ASR chép “Cà 2 chỉ có chi nên trung bình chính.” (0.778): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: chín/chính — NOT_VERIFIED bằng tai người',
    'Bước một, tính bao đóng của A, lượt đầu bắt đầu từ chính A.':
        'ASR chép “Bước 1, tính bao đóng của A, lượt đầu bắt đầu từ chính nha.” (0.929): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Luật B C xác định D cần cả B lẫn C, mà C chưa có, nên chưa áp được.':
        'ASR chép “Luật B xe xác định dây cần cả B lẫn xe mà xe chưa có nên chưa áp được.” (0.947): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Bên trái, bảng to chép tên lớp Khoa học máy tính ở 2 dòng, ô tô cam, nên đổi tên lớp phải sửa 2 chỗ.':
        'ASR chép “Bên trái, bảng to chép tên lớp khoa học máy tính ở hai vòng, auto cam, nên đổi tên lớp phải sửa hai chỗ.” (0.898): “ô” (ô lưới) ASR viết chữ “O”; lệch âm/thanh thuần Việt: dòng tô (trong “dòng ô tô” → “vòng auto”) — NOT_VERIFIED bằng tai người',
    'Câu truy vấn nối bảng đăng ký với bảng sinh viên theo mã số.':
        'ASR chép “Câu truy vẫn nối bạn đăng ký với bạn sinh viên theo mã số.” (0.786): lệch âm/thanh thuần Việt: vấn/vẫn, bảng/bạn, bảng/bạn — NOT_VERIFIED bằng tai người',
    'Một ki-lô-byte là 1024 byte, nên 8 ki-lô-byte là 8 nhân 1024 bằng 8192 byte.':
        'ASR chép “1 kg bài là 1.024 bài, nên 8 kg bài là 8 nhân 1.024 bằng 8.192 bài.” (0.806): KB đọc “ki-lô-byte” theo lexicon của khoá, ASR viết “kilobyte/kg”; byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Một mi li giây bằng một triệu na-nô giây, nên 8 mi li giây là tám triệu na-nô giây.':
        'ASR chép “Một mili giây bằng 1 triệu nano giây, nên 8 mili giây là 8 triệu nano giây.” (0.684): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh — NOT_VERIFIED bằng tai người',
    'Dù chỉ cần một dòng, đĩa vẫn phải đọc cả trang 8 ki-lô-byte chứa nó.':
        'ASR chép “Du chỉ cần một dòng, đĩa vẫn phải đọc cả trang 8kg bai chứa nó.” (0.788): KB đọc “ki-lô-byte” theo lexicon của khoá, ASR viết “kilobyte/kg”; lệch âm/thanh thuần Việt: dù/du — NOT_VERIFIED bằng tai người',
    'Kiểm bằng đường khác, ta đếm theo byte thay vì theo dòng.':
        'ASR chép “Kiểm bằng đường khác, ta đếm theo bài thay vì theo dòng.” (0.917): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Một triệu dòng nhân 80 byte được tám mươi triệu byte, chia cho 8192 byte mỗi trang, làm tròn lên được 9766 trang.':
        'ASR chép “1 triệu dòng nhân 80 bai được 80 triệu bai, chia cho 8.192 bai mỗi trang, làm tròn lên được 9.766 trang.” (0.917): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Lượt đầu đọc R1 rồi đọc S1, S2.':
        'ASR chép “Lược đầu đọc Adder 1 đổi đọc S1, S2.” (0.727): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: lượt/lược, rồi/đổi — NOT_VERIFIED bằng tai người',
    'Lượt hai đọc R2 rồi lại S1, S2.':
        'ASR chép “Lược hai độc R2 đổi lại S1, S2.” (0.727): lệch âm/thanh thuần Việt: lượt/lược, đọc/độc, rồi/đổi — NOT_VERIFIED bằng tai người',
    'Lượt ba đọc R3 rồi lại S1, S2.':
        'ASR chép “Lược 3 đọc ED3 đổi lại S1, S2.” (0.727): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: lượt/lược, rồi/đổi — NOT_VERIFIED bằng tai người',
    'T2 đọc A rồi T1 đọc A, hai lần đọc, không xung đột.':
        'ASR chép “T2 độc A rồi T1 độc A, hai lần độc, không xung độc.” (0.733): lệch âm/thanh thuần Việt: đọc/độc, đọc/độc, đọc/độc, đột/độc — NOT_VERIFIED bằng tai người',
    'T2 ghi A trước khi T1 đọc A, xung đột, cho cạnh T2 sang T1.':
        'ASR chép “T2Va trước khi T1 độc A xung đột, cho cạnh T2 sang T1.” (0.865): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: ghi (trong “ghi a” → “va”), đọc/độc — NOT_VERIFIED bằng tai người',
    'Bước hai, T2 xin khoá độc quyền trên B, B đang trống nên cũng được cấp.':
        'ASR chép “Bước 2, T2 xin khóa độc quyền trên B, về đàn trống nên cũng được cấp.” (0.882): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: đang (trong “b đang” → “về đàn”) — NOT_VERIFIED bằng tai người',
    'Chữ A của ACID đòi chỉ có trước hoặc sau, không có nửa chừng.':
        'ASR chép “Chữ A của ACI đây đòi chỉ có trước hoặc sau, không có nửa chừng.” (0.941): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'T1 đã ghi nhận nên còn đủ, đó là chữ D.':
        'ASR chép “T1 đã ghi nhận nên còn đủ, đó là chữ V.” (0.917): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Bản ghi thứ tư trả C về 1, rồi bản ghi thứ nhất trả A về 10.':
        'ASR chép “Bản ghi thứ 4 trả CV1, rồi bản ghi thứ nhất trả AV10.” (0.812): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: về (trong “c về” → “cv”), về (trong “a về” → “av”) — NOT_VERIFIED bằng tai người',
    'T2 ghi A bằng 200 nhưng chưa ghi nhận, nên số 200 chỉ là tạm thời.':
        'ASR chép “T2gA bằng 200 nhưng chưa ghi nhận nên số 200 chỉ là tạm thời.” (0.919): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: ghi (trong “ghi a” → “ga”) — NOT_VERIFIED bằng tai người',
    'Thời điểm thứ hai, T2 ghi A bằng 200.':
        'ASR chép “Thời điểm thứ 2, T2GA bằng 200.” (0.857): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: ghi (trong “ghi a” → “ga”) — NOT_VERIFIED bằng tai người',
    # ── Đợt A đào sâu: EVT ──
    'Chiều ngược, người nhận mới đọc sự kiện cũ thiếu ghi chú, thì tự điền rỗng, nên đọc được.':
        'ASR chép “Chiều Ngư, người nhận mới đọc sự kiện của thiếu ghi chú, thì tự điên rộng nên đọc đưa.” (0.737): lệch âm/thanh thuần Việt: ngược/ngư, cũ/của, điền rỗng/điên rộng, được/đưa — NOT_VERIFIED bằng tai người',
    'Đáp án câu một, thêm kênh là trường tuỳ chọn có giá trị mặc định, ví dụ web, rồi thử từng chiều.':
        'ASR chép “Đáp án câu 1, thêm kênh là trường tùy chọn có giá trị mặc định, ví dụ quét, rồi thử từng chiêu.” (0.909): web đọc thô (probe NET p2: 8/8), lần này ASR viết sai; lệch âm/thanh thuần Việt: chiều/chiêu — NOT_VERIFIED bằng tai người',
    'Gom lại thành bảng.':
        'ASR chép “gom lại thành bản.” (0.75): lệch âm/thanh thuần Việt: bảng/bản — NOT_VERIFIED bằng tai người',
    'Đáp án câu một, giải từng dòng.':
        'ASR chép “Đáp án câu một, giải tương dung.” (0.714): lệch âm/thanh thuần Việt: từng dòng/tương dung — NOT_VERIFIED bằng tai người',
    'Bản v bằng 1, giá trị W, có 1 không lớn hơn 2 nên bỏ, trong khi ghi đè mù đổi sang W.':
        'ASR chép “Bản V bằng 1, giá trị V đúc có 1 không lớn hơn 2 nên bỏ trong khi ghi đề mù đổi sang V đúc.” (0.833): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: đè/đề — NOT_VERIFIED bằng tai người',
    'Bước ba, lượt bấm d, lượt hiển thị d lúc 3.':
        'ASR chép “Bước 3, lượt bấm G, lượt hiển thị G lúc 3.” (0.818): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Mỗi lượt hiển thị phải nằm trong bộ nhớ suốt W phút.':
        'ASR chép “Mỗi lượt hiển thị phải nằm trong bộ nhớ suốt về đúc phúc.” (0.8): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: phút (trong “w phút” → “về đúc phúc”) — NOT_VERIFIED bằng tai người',
    'Giả sử có 1000 lượt hiển thị mỗi phút và W bằng 10, thì lúc nào cũng giữ khoảng 1000 nhân 10, bằng 10 nghìn lượt.':
        'ASR chép “Giả sử có 1 nghìn lượt hiển thị mỗi phút và về đúc bằng 10 thì lúc nào cũng giữ khoảng 1 nghìn nhân 10 bằng 10 nghìn lượt.” (0.947): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Hàng a 3 chỉ có ô a cùng mã, hiệu 3, khớp.':
        'ASR chép “Hàng A3 chỉ có OA cùng mã, hiệu 3, khớp.” (0.87): “ô” (ô lưới) ASR viết chữ “O”; chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Hàng b 13 chỉ có ô b cùng mã, hiệu 12, quá 10.':
        'ASR chép “Hàng B13 chỉ có OB cùng mã, hiệu 12, quá mười.” (0.897): “ô” (ô lưới) ASR viết chữ “O”; chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Thử nới cửa sổ từ 10 lên 15 phút, ô b có hiệu 12, nhỏ hơn 15, nên khớp, và kết quả thành 3 cặp.':
        'ASR chép “Thử nới cửa sổ từ 10 lên 15 phút, OB có hiểu 12, nhỏ hơn 15, nên khớp và kết quả thành 3 cặp.” (0.909): “ô” (ô lưới) ASR viết chữ “O”; chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: hiệu/hiểu — NOT_VERIFIED bằng tai người',
    'Cùng một dữ liệu, độ dài cửa sổ làm đổi kết quả, nên W là một quyết định nghiệp vụ, không chỉ là một tham số kỹ thuật.':
        'ASR chép “Cùng một giữ liệu, độ dài cửa số làm đổi kết quả nên VDUP là một quyết định nghiệp vụ, không chỉ là một tham số kỹ thuật.” (0.929): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: sổ/số — NOT_VERIFIED bằng tai người',
    'Người làm nghề đo khoảng cách thật giữa hiển thị và bấm, rồi chọn W phủ phần lớn các lượt bấm, chứ không chọn theo cảm giác.':
        'ASR chép “Người làm nghề đo khoảng cách thật giữa hiển thị và bấm, rồi chọn vê đúc phủ phần lớn các lược bấm, chứ không chọn theo cảm giác.” (0.909): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: lượt/lược — NOT_VERIFIED bằng tai người',
    'Hình vẽ bốn dịch vụ A, B, C, D trên cùng một trục thời gian tính bằng mi li giây.':
        'ASR chép “Hình vẽ bốn dịch vụ A, B, C, G trên cùng một trục thời gian tính bằng mili giây.” (0.872): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh — NOT_VERIFIED bằng tai người',
    'D chỉ bắt đầu khi cả hai đã xong, nên kết quả cuối có mặt lúc 90.':
        'ASR chép “Vê chỉ bắt đầu khi cả hai đã xong nên kết quả cuối có mặt lúc 90.” (0.944): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    # ── Đợt A đào sâu: SAR ──
    'Tải ghi hiện tại là 900 mỗi giây.':
        'ASR chép “tại vì hiện tại là 900 mỗi dây.” (0.778): lệch âm/thanh thuần Việt: tải ghi/tại vì — NOT_VERIFIED bằng tai người',
    'KB là một nghìn byte, GB là một tỉ byte, tê-ra-byte là một nghìn tỉ byte.':
        'ASR chép “Kilobyte là 1.000 byte, Gigabyte là 1 tỷ byte, Terabyte là 1.000 tỷ byte.” (0.647): KB đọc “ki-lô-byte” theo lexicon của khoá, ASR viết “kilobyte/kg”; GB đọc “ghi-ga-byte” theo lexicon của khoá, ASR viết “GB/gigabyte”; “tỉ” ASR viết chính tả “tỷ” (cùng âm); “tê-ra-byte” đọc tách âm tiết (đã dựng ở OSY/NET), ASR viết “TB/terabyte” — NOT_VERIFIED bằng tai người',
    'Ví dụ 1 triệu bài, mỗi bài 2 KB, là 2 nhân 10 mũ 3 nhân 10 mũ 6, bằng 2 nhân 10 mũ 9 byte, tức 2 GB.':
        'ASR chép “Ví dụ 1 triệu bài, mỗi bài 2 kilobyte là 2 nhân 10 mũ 3 nhân 10 mũ 6 bằng 2 nhân 10 mũ 9 bài tức 2 gigabyte.” (0.897): KB đọc “ki-lô-byte” theo lexicon của khoá, ASR viết “kilobyte/kg”; byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); GB đọc “ghi-ga-byte” theo lexicon của khoá, ASR viết “GB/gigabyte” — NOT_VERIFIED bằng tai người',
    'Thứ ba, ở khoá Mạng máy tính ta đã biết 1 byte bằng 8 bit, và tốc độ đường truyền tính bằng bit mỗi giây.':
        'ASR chép “Thứ ba, ở khóa mạng máy tính ta đã biết một bay bằng 8 bit và tốc độ đường truyền tính bằng bit mỗi giây.” (0.96): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Đường truyền một tỉ bit mỗi giây chỉ chở được một tỉ chia 8, tức 125 triệu byte mỗi giây.':
        'ASR chép “Đường truy 1 tỷ biết mỗi dây chỉ chở được 1 tỷ chia 8, tức 125 triệu bay mỗi dây.” (0.792): “tỉ” ASR viết chính tả “tỷ” (cùng âm); byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: truyền/truy, bit (trong “tỉ bit” → “tỷ biết”) — NOT_VERIFIED bằng tai người',
    'Mỗi người đăng 1 bài 2 KB mỗi ngày thì mỗi ngày có 20 GB, nhân 365 thành 7300 GB.':
        'ASR chép “Mỗi người đăng một bài 2 kilobytes mỗi ngày thì mỗi ngày có 20 GB, nhận 365 x 7300 GB.” (0.893): KB đọc “ki-lô-byte” theo lexicon của khoá, ASR viết “kilobyte/kg”; lệch âm/thanh thuần Việt: nhân/nhận, thành/x — NOT_VERIFIED bằng tai người',
    'Đó là vì 2315 nhân 50 KB là khoảng 115 phẩy 7 MB mỗi giây, nhân 8 để đổi sang bit.':
        'ASR chép “Đó là vì 2.315 nhân 50 kB là khoảng 115,7 MB mỗi giây, nhân 8 để đổi sang bích.” (0.967): lệch âm/thanh thuần Việt: bit/bích — NOT_VERIFIED bằng tai người',
    'Trung bình khoảng 2315 yêu cầu mỗi giây, cao điểm khoảng 6944, lưu trữ khoảng 7 phẩy 3 tê-ra-byte mỗi năm, băng thông trung bình khoảng 926 mê-ga-bít mỗi giây.':
        'ASR chép “Trung Bình khoảng 2.315 yêu cầu mỗi giây, cao điểm khoảng 6.944, lưu trữ khoảng 7,3TB mỗi năm, bằng thông Trung Bình khoảng 926Mb mỗi giây.” (0.894): “tê-ra-byte” đọc tách âm tiết (đã dựng ở OSY/NET), ASR viết “TB/terabyte”; “mê-ga-bít” đọc tách âm tiết (đã dựng ở NET), ASR viết “megabit”; lệch âm/thanh thuần Việt: băng/bằng — NOT_VERIFIED bằng tai người',
    'Tính lưu trữ theo một người trước, 2 KB nhân 365 là 730 KB mỗi năm, nhân 10 triệu người lại ra 7 phẩy 3 tê-ra-byte.':
        'ASR chép “Tính lưu trữ theo một người trước, 2 kilobyte nhân 365 là 730 kilobyte mỗi năm, nhân 10 triệu người lại ra 7,3 terabyte.” (0.882): KB đọc “ki-lô-byte” theo lexicon của khoá, ASR viết “kilobyte/kg”; “tê-ra-byte” đọc tách âm tiết (đã dựng ở OSY/NET), ASR viết “TB/terabyte” — NOT_VERIFIED bằng tai người',
    'Lấy 926 chia 8 được khoảng 115 phẩy 8 MB mỗi giây, chia tiếp cho 50 KB lại ra khoảng 2315 lần trả về mỗi giây.':
        'ASR chép “Lấy 926 chia 8 được khoảng 115,8 MB mỗi giây, chia tiếp cho 50 kilobyte lại ra khoảng 2.315 lần trả về mỗi giây.” (0.974): KB đọc “ki-lô-byte” theo lexicon của khoá, ASR viết “kilobyte/kg” — NOT_VERIFIED bằng tai người',
    'Câu hai, mỗi ngày có 2 triệu nhân 100 KB, bằng 200 GB, nhân 365 thành 73 nghìn GB.':
        'ASR chép “Câu 2, mỗi ngày có 2 triệu nhân 100kg bằng 200GB nhận 365x73.000GB.” (0.852): KB đọc “ki-lô-byte” theo lexicon của khoá, ASR viết “kilobyte/kg”; lệch âm/thanh thuần Việt: nhân/nhận, thành/x, nghìn/không — NOT_VERIFIED bằng tai người',
    'Luật là cạnh a gọi b hợp lệ khi hạng của b lớn hơn hạng của a.':
        'ASR chép “Luật là cạnh A gọi B hợp lệ khi hạng của B lớn hơn hạng qua.” (0.909): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: của (trong “của a” → “qua”) — NOT_VERIFIED bằng tai người',
    'Cất 7 phẩy 3 tê-ra-byte vào các ổ 1 tê-ra-byte thì 7 ổ mới chứa 7, phần 0 phẩy 3 còn lại vẫn cần thêm một ổ, nên cần 8 ổ.':
        'ASR chép “Các 7,3tb vào các ổ 1tb thì 7 ổ mới chứa 7, phần 0,3 còn lại vẫn cần thêm 1 ổ, nên cần 8 ổ.” (0.848): “tê-ra-byte” đọc tách âm tiết (đã dựng ở OSY/NET), ASR viết “TB/terabyte”; lệch âm/thanh thuần Việt: cất/các — NOT_VERIFIED bằng tai người',
    'Bước một, đổi cùng đơn vị, 5 tê-ra-byte là 5000 GB, chia cho 500 GB mỗi nút được 10 phần, làm tròn lên vẫn là 10.':
        'ASR chép “Bước 1, đổi cùng đơn vị, 5TB là 5000GB, chia cho 500GB mỗi nút được 10 phần, làm tròn lên vẫn là 10.” (0.931): “tê-ra-byte” đọc tách âm tiết (đã dựng ở OSY/NET), ASR viết “TB/terabyte” — NOT_VERIFIED bằng tai người',
    'Thùng bắt đầu đầy với 20 token, nên 20 yêu cầu đầu tiên, đến trong 20 mi li giây đầu, được nhận ngay.':
        'ASR chép “Thùng bắt đầu đầy với 20 tô cần, nên 20 yêu cầu đầu tiên đến trọng 20 mili giấy đầu được nhận ngay.” (0.83): token đọc “tâu-cần” theo lexicon SAR (probe p1 8/8), ASR viết “tô cần”; tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; lệch âm/thanh thuần Việt: trong/trọng — NOT_VERIFIED bằng tai người',
    'Giây đầu nhận 29, gồm 20 token có sẵn và 9 token vừa nạp.':
        'ASR chép “Giây đầu nhận 29, gồm 20 tô cần có sẵn và 9 tô cần vừa nạp.” (0.895): token đọc “tâu-cần” theo lexicon SAR (probe p1 8/8), ASR viết “tô cần” — NOT_VERIFIED bằng tai người',
    'Ví dụ 3000 GB trên nút 1000 GB với 3 bản sao cần 9 nút.':
        'ASR chép “Ví dụ 3000GB trên nút 1000GB với 3 bảng sao cần 9 nút.” (0.941): lệch âm/thanh thuần Việt: bản/bảng — NOT_VERIFIED bằng tai người',
    'Bước bốn, 6 tỉ bản ghi nhân 500 byte là 3 nghìn tỉ byte.':
        'ASR chép “Bước 4, 6 tỷ bản ghi nhân 500 bai là 3.000 tỷ bai.” (0.733): “tỉ” ASR viết chính tả “tỷ” (cùng âm); byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Tính lưu trữ theo từng năm, mỗi năm 1 phẩy 2 tỉ bản ghi nhân 500 byte là 0 phẩy 6 tê-ra-byte, nhân 5 năm ra 3 tê-ra-byte.':
        'ASR chép “Tính lưu trữ theo từng năm, mỗi năm 1,2 tỷ bảng ghi nhân 500 byte là 0,6 terabyte, nhân năm năm ra 3 terabyte.” (0.806): “tỉ” ASR viết chính tả “tỷ” (cùng âm); “tê-ra-byte” đọc tách âm tiết (đã dựng ở OSY/NET), ASR viết “TB/terabyte”; lệch âm/thanh thuần Việt: bản (trong “tỉ bản” → “tỷ bảng”) — NOT_VERIFIED bằng tai người',
    # ── Đợt A đào sâu: DVO ──
    'Bước một, đề bài.':
        'ASR chép “Bước 1. Đề bay” (0.75): lệch âm/thanh thuần Việt: bài/bay — NOT_VERIFIED bằng tai người',
    'Mỗi thay đổi của người khác là một chấm rơi vào một ô ngẫu nhiên.':
        'ASR chép “Mỗi thay đổi của người khác là một chấm rơi vào một ôn ngẫu nhiên.” (0.933): “ô” (ô lưới) ASR viết chữ “O” — NOT_VERIFIED bằng tai người',
    'Ma đứng trước mo vì ký tự đầu bằng nhau, ký tự thứ hai a đứng trước o.':
        'ASR chép “mà đứng trước Mo vì ký tự đầu bằng nhau, ký tự thứ 2A đứng trước Co.” (0.889): “ma/mo” là hai chuỗi ví dụ, ASR viết hoa/đổi thanh; chữ cái đứng riêng a, o đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    '1 chấm 2 chấm 0 thành 10200.':
        'ASR chép “1.2.0x10.200” (0.778): lệch âm/thanh thuần Việt: chấm/∅, chấm/∅, thành/x — NOT_VERIFIED bằng tai người',
    '1 chấm 10 chấm 0 thành 11000.':
        'ASR chép “1.10.0 x 11.000” (0.75): lệch âm/thanh thuần Việt: chấm/∅, chấm/∅, thành/x — NOT_VERIFIED bằng tai người',
    'Hàm băm biến một dãy byte bất kỳ thành một chuỗi 64 ký tự, và ta chỉ xem 12 ký tự đầu.':
        'ASR chép “Hàm băm biến một giải bay bất kỳ thành một chuỗi 64 ký tự và ta chỉ xem 12 ký tự đâu.” (0.88): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: dãy (trong “dãy byte” → “giải bay”), đầu/đâu — NOT_VERIFIED bằng tai người',
    'Thêm đúng một dấu chấm than, tức một byte, thì mã băm khác hoàn toàn, không giống dù chỉ vài ký tự.':
        'ASR chép “Thêm đúng một dấu chấm than, tức một bay, thì mã băm khác hoàn toàn, không giống dù chỉ vài ký tự.” (0.955): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Tiếp theo là thứ tự các tệp, vì đổi thứ tự là đổi dãy byte.':
        'ASR chép “Tiếp theo là thứ tự các tệp, vì đổi thứ tự là đổi giải bay.” (0.867): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: dãy (trong “dãy byte” → “giải bay”) — NOT_VERIFIED bằng tai người',
    'Kiểm bằng đường khác, không băm nữa mà đặt hai gói cạnh nhau và so từng byte.':
        'ASR chép “Kiểm bằng đường khác, không băm nữa mà đặt hai gói cạnh nhau và so từng bay.” (0.941): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Gói lần một và lần hai cùng dài 128 byte, nhưng khác nhau ở 6 byte.':
        'ASR chép “Gói lần 1 và lần 2 cùng dài 128 bài, nhưng khác nhau ở 6 bài.” (0.9): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Cả 6 byte đó nằm ở hai chỗ ghi thời điểm, một ở đầu gói, một ở mục lục cuối gói.':
        'ASR chép “Cả sáu bài đó nằm ở hai chỗ ghi thời điểm, một ở đầu gói, một ở mục lục cuối gói.” (0.952): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Gói lần một và lần ba thì trùng từng byte.':
        'ASR chép “Gói lần 1 và lần 3 thì trùng từng bay.” (0.9): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Bảng có ba bản.':
        'ASR chép “Bản có ba bản” (0.75): lệch âm/thanh thuần Việt: bảng/bản — NOT_VERIFIED bằng tai người',
    'Bản B 10 ngày và bản C 2 ngày thì còn.':
        'ASR chép “Bán B 10 ngày và bán C 2 ngày thì con.” (0.727): lệch âm/thanh thuần Việt: bản/bán, bản/bán, còn/con — NOT_VERIFIED bằng tai người',
    'Vì thế công cụ xoá 3 máy web.':
        'ASR chép “vì thế công cụ xóa 3 máy huét.” (0.875): web đọc thô (probe NET p2: 8/8), lần này ASR viết sai — NOT_VERIFIED bằng tai người',
    'Nhưng câu một vừa cho thấy 15 lỗi chưa làm quy tắc quay lui, nên phải hỏi ở ngưỡng thật là 19 lỗi.':
        'ASR chép “Nhưng câu một vừa cho thấy 15 lỗi chưa làm quy tắc quay lui nên phải hỏi ấn ngưỡng thật là 19 lỗi.” (0.96): lệch âm/thanh thuần Việt: ở/ấn — NOT_VERIFIED bằng tai người',
    'Bản cũ vẫn thấy cột tên, bản mới thấy cột họ tên, nên cả hai đều chạy.':
        'ASR chép “Bạn cũ vẫn thấy cuộc tinh, bạn mới thấy cuộc họ tinh, nên cả hai đều chạy.” (0.647): lệch âm/thanh thuần Việt: bản/bạn, cột tên bản/cuộc tinh bạn, cột/cuộc, tên/tinh — NOT_VERIFIED bằng tai người',
    'Dòng An có họ tên nhờ lần chép.':
        'ASR chép “Dòng An có họ tin nhờ lần chiếc.” (0.75): lệch âm/thanh thuần Việt: tên/tin, chép/chiếc — NOT_VERIFIED bằng tai người',
    'Dòng Chi do bản cũ ghi sau lần chép, nên cột họ tên còn trống.':
        'ASR chép “Dòng chi do bản củ ghi sau lần chết, nên cục họ tin còn trống.” (0.733): lệch âm/thanh thuần Việt: cũ/củ, chép/chết, cột/cục, tên/tin — NOT_VERIFIED bằng tai người',
    'Mỗi vạch xanh là một lần triển khai, đếm số vạch mỗi ngày ra tần suất triển khai.':
        'ASR chép “Mỗi vặt xanh là một lần triển khai, đếm số vặt mỗi ngày ra từng suốt triển khai.” (0.778): lệch âm/thanh thuần Việt: vạch/vặt, tần suất/từng suốt — NOT_VERIFIED bằng tai người',
    'Vạch đỏ là lần triển khai gây sự cố, số vạch đỏ chia cho mọi vạch ra tỉ lệ thay đổi thất bại.':
        'ASR chép “Vặt đỏ là lần triển khai ghê sự cuốn, số vặt đỏ chia cho mọi vặt ra tỷ lệ thay đổi thất bại.” (0.739): “tỉ” ASR viết chính tả “tỷ” (cùng âm); lệch âm/thanh thuần Việt: vạch/vặt, gây/ghê, cố/cuốn, vạch/vặt, vạch/vặt — NOT_VERIFIED bằng tai người',
    'Bước một, đề bài.':
        'ASR chép “Bước 1. Đề bay” (0.75): lệch âm/thanh thuần Việt: bài/bay — NOT_VERIFIED bằng tai người',
    '1 MB là 1000 ki lô byte, tức một triệu byte.':
        'ASR chép “Một megabyte là một nghìn kilobytes, tức một triệu byte.” (0.727): MB đọc “mê-ga-byte” theo lexicon của khoá, ASR viết “MB/megabyte”; KB đọc “ki-lô-byte” theo lexicon của khoá, ASR viết “kilobyte/kg” — NOT_VERIFIED bằng tai người',
    '1 GB là 1000 MB, tức một tỉ byte.':
        'ASR chép “1 gigabyte là 1 nghìn megabyte, tức 1 tỷ byte.” (0.7): GB đọc “ghi-ga-byte” theo lexicon của khoá, ASR viết “GB/gigabyte”; MB đọc “mê-ga-byte” theo lexicon của khoá, ASR viết “MB/megabyte”; “tỉ” ASR viết chính tả “tỷ” (cùng âm) — NOT_VERIFIED bằng tai người',
    'Ví dụ, 3 tỉ byte là 3 GB, cứ mỗi lần lên một bậc thì chia cho 1000.':
        'ASR chép “Ví dụ, 3 tỷ byte là 3GB, cứ mỗi lần lên một bật thì chia cho một nghìn.” (0.895): “tỉ” ASR viết chính tả “tỷ” (cùng âm); lệch âm/thanh thuần Việt: bậc/bật — NOT_VERIFIED bằng tai người',
    'Nhánh trên là nhật ký, mỗi yêu cầu ghi một dòng chừng 1 ki lô byte, nên kho nhật ký phình theo đúng số yêu cầu.':
        'ASR chép “Nhánh trên là nhật ký, mỗi yêu cầu ghi một dòng chừng 1 kg, nên khó nhật ký phình theo đúng số yêu cầu.” (0.88): KB đọc “ki-lô-byte” theo lexicon của khoá, ASR viết “kilobyte/kg”; lệch âm/thanh thuần Việt: kho/khó — NOT_VERIFIED bằng tai người',
    '1000 nhân 1000 byte, bằng một triệu byte, tức 1 MB mỗi giây.':
        'ASR chép “Một nghìn nhân một nghìn bay, bằng một triệu bay, tức một megabyte mỗi giây.” (0.8): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); MB đọc “mê-ga-byte” theo lexicon của khoá, ASR viết “MB/megabyte” — NOT_VERIFIED bằng tai người',
    'Ở mức bình thường, mỗi yêu cầu ghi 1 ki lô byte, mỗi ngày 86 phẩy 4 GB, giữ 30 ngày là 2592 GB.':
        'ASR chép “Ở mức bình thường, mỗi yêu cầu ghi 1 KB, mỗi ngày 86,4 GB, giữa 30 ngày là 2.592 GB.” (0.906): KB đọc “ki-lô-byte” theo lexicon của khoá, ASR viết “kilobyte/kg”; lệch âm/thanh thuần Việt: giữ/giữa — NOT_VERIFIED bằng tai người',
    'Nếu mức chi tiết ghi 10 ki lô byte mỗi yêu cầu, đây là số minh hoạ, thì mỗi ngày thành 864 GB, và 30 ngày thành 25 nghìn 920 GB, gấp 10 lần.':
        'ASR chép “Nếu mức chi tiết ghi 10 kilobytes mỗi yêu cầu, đây là số minh họa, thì mỗi ngày thành 864 GB và 30 ngày thành 25920 GB, gấp 10 lần.” (0.953): KB đọc “ki-lô-byte” theo lexicon của khoá, ASR viết “kilobyte/kg” — NOT_VERIFIED bằng tai người',
    'Làm từng bước, mỗi giây có 500 nhân 2000 byte, bằng một triệu byte, tức 1 MB, đúng bằng ví dụ lúc nãy.':
        'ASR chép “Làm từng bước, mỗi dây có 500 nhân 2000 byte, bằng 1 triệu byte, tức 1 megabyte, đúng bằng ví dụ lúc nãy.” (0.96): MB đọc “mê-ga-byte” theo lexicon của khoá, ASR viết “MB/megabyte” — NOT_VERIFIED bằng tai người',
    'Ở bài 4, mã băm là dấu vân tay của nội dung, đổi một byte là đổi mã băm.':
        'ASR chép “Ở bài 4, mã băm là giấu vân tay của nội dung. Đổi một bài là đổi mã băm.” (0.947): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Câu hai, bước quét nên chặn lần dựng, và báo rõ hai thư viện cần nâng lên bản đã vá, a lên ít nhất 1 chấm 4 chấm 3, c lên ít nhất 1 chấm 0 chấm 0.':
        'ASR chép “Câu 2, bước quét nên chặn lần dựng và báo rõ hai thư viện cần nâng lên bản đa vá, a lên ít nhất 1.4.3, cê lên ít nhất 1.0.0.” (0.889): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: đã/đa, chấm/∅, chấm/∅, chấm/∅, chấm/∅ — NOT_VERIFIED bằng tai người',
    # ── Đợt A đào sâu: SDP ──
    'Bảng dưới đây ghi lại một thứ tự xen kẽ của hai luồng.':
        'ASR chép “Bạn dưới đây ghi lại 1 thứ tự sen kẻ của 2 luôn.” (0.769): lệch âm/thanh thuần Việt: bảng/bạn, kẽ/kẻ, luồng/luôn — NOT_VERIFIED bằng tai người',
    'Lớp tính thuế thì không phải sửa dòng nào.':
        'ASR chép “lật tính thuế thì không phải sử dòng nào.” (0.778): lệch âm/thanh thuần Việt: lớp/lật, sửa/sử — NOT_VERIFIED bằng tai người',
    # ── Đợt A đào sâu: DEN ──
    'Trong bài này, mỗi ô chứa một con số như số tiền hay mã đơn chiếm 8 byte.':
        'ASR chép “Trong bài này, mỗi ô chứa một con số như số tiền hay mã đơn chiếm 8 bay.” (0.944): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Một GB là 10 mũ 9 byte, tức một tỉ byte, nên 8 nhân 10 mũ 8 byte bằng 0 phẩy 8 GB.':
        'ASR chép “1 GB là 10 mũ 9 bai, tức 1 tỷ bai, nền 8 nhân 10 mũ 8 bai bằng 0,8 GB.” (0.783): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); “tỉ” ASR viết chính tả “tỷ” (cùng âm); lệch âm/thanh thuần Việt: nên (trong “tỉ byte nên” → “tỷ bai nền”) — NOT_VERIFIED bằng tai người',
    'Một bảng có số ô bằng số dòng nhân số cột, và số byte bằng số ô nhân số byte mỗi ô.':
        'ASR chép “Một bản có số ô bằng số dòng nhân số cọt và số bay bằng số ô nhân số bay mỗi ô.” (0.818): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: bảng/bản, cột/cọt — NOT_VERIFIED bằng tai người',
    'Ví dụ bảng 1000 dòng, 5 cột, 8 byte mỗi ô thì có 1000 nhân 5 nhân 8, bằng 40 nghìn byte.':
        'ASR chép “Ví dụ bảng 1.000 dòng, 5 cột, 8 bay mỗi ô thì có 1.000 nhân 5 nhân 8 bằng 40.000 bay.” (0.92): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Theo cột, 3 giá trị của cột tỉnh nằm liền nhau, cột ngày nằm liền nhau, nên câu hỏi chỉ cần 3 cột thì chỉ đọc 9 ô màu lục.':
        'ASR chép “Theo cột, ba giá trị của cột tỉnh nằm liền nhau, cột ngày nằm liền nhau, nên câu hỏi chỉ cần ba cột thì chỉ đọc chín ôm màu luộc.” (0.933): “ô” (ô lưới) ASR viết chữ “O”; lệch âm/thanh thuần Việt: lục/luộc — NOT_VERIFIED bằng tai người',
    'Phần của một dòng mà cách lưu theo cột phải đọc là 3 nhân 8, bằng 24 byte, nhân 10 mũ 8 được 2 phẩy 4 GB, cũng khớp.':
        'ASR chép “Phần của một dòng mà cách lưu theo cột phải đọc là 3 nhân 8, bằng 24 by, nhân 10 mũ 8 được 2,4 gigabyte, cũng khớp.” (0.935): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); GB đọc “ghi-ga-byte” theo lexicon của khoá, ASR viết “GB/gigabyte” — NOT_VERIFIED bằng tai người',
    'Với 8 khoá a, c, e, g, k, m, p, t, tìm m thì so với g ở giữa rồi sang nửa phải, so với k rồi lại sang nửa phải, so với m thì thấy.':
        'ASR chép “Với 8 khóa A, C, E, G, K, M, T, T, tìm M thì so với G ở giữa rồ sang nửa phải, so với K đồ lại sang nửa phải, so với M thì thấy.” (0.917): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: rồi/rồ, rồi/đồ — NOT_VERIFIED bằng tai người',
    'Khi đọc, ta đi theo mũi tên cam từ bộ đệm sang tệp mới nhất rồi lùi dần về tệp cũ, còn gộp nền chạy ngầm, trộn các tệp cũ thành một tệp và bỏ bản cũ.':
        'ASR chép “Khi đọc, ta đi theo mũi tên cam từ bộ đệm sang tẹp mới nhất đôi lùi dần về tẹp cũ còn gột nên chạy ngầm, trộn các tẹp cũ thành một tẹp và bỏ bảng cũ.” (0.784): lệch âm/thanh thuần Việt: tệp/tẹp, rồi/đôi, tệp/tẹp, gộp nền/gột nên, tệp/tẹp, tệp/tẹp, bản/bảng — NOT_VERIFIED bằng tai người',
    'Chỉ 100 byte màu cam đổi, nhưng cả trang 4096 byte được ghi lại, vào một chỗ nằm rải rác trên đĩa.':
        'ASR chép “Chỉ 100 bay màu cam đổi, nhưng cả trang 4.096 bay được ghi lại vào một chỗ nằm rại rác trên đĩa.” (0.897): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: rải/rại — NOT_VERIFIED bằng tai người',
    'Hình bên phải là gộp theo bậc, mỗi lần xả tạo một tệp nhỏ ở bậc 0.':
        'ASR chép “Hình bên phải là gột theo bật, mỗi lần xả tạo một tẹp nhỏ ở bật không?” (0.765): lệch âm/thanh thuần Việt: gộp/gột, bậc/bật, tệp/tẹp, bậc/bật — NOT_VERIFIED bằng tai người',
    'Mỗi lần lên bậc, cùng một byte bị ghi lại, nhưng luôn là ghi tuần tự những đoạn dài.':
        'ASR chép “Mỗi lần Linh Bật cùng một bai bị ghi lại nhưng luôn là ghi tuần tự những đoạn dài.” (0.842): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: lên bậc/linh bật — NOT_VERIFIED bằng tai người',
    'Bước hai, tính khuếch đại đọc của cây B.':
        'ASR chép “Bước 2. Tính khuết đại độc của cây B.” (0.778): lệch âm/thanh thuần Việt: khuếch/khuết, đọc/độc — NOT_VERIFIED bằng tai người',
    'Bước ba, đếm số bậc của gộp theo bậc.':
        'ASR chép “Bước 3. Đếm số bật của gột theo bật” (0.667): lệch âm/thanh thuần Việt: bậc/bật, gộp/gột, bậc/bật — NOT_VERIFIED bằng tai người',
    'Bước bốn, cộng các lần ghi của một byte.':
        'ASR chép “Bước 4. Cộng cắt lần ghi của một bay.” (0.778): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: các/cắt — NOT_VERIFIED bằng tai người',
    'Lỗi thứ tư hay gặp ở người đã đi làm, lập kế hoạch đĩa theo số byte ứng dụng ghi, quên nhân khuếch đại ghi.':
        'ASR chép “Lỗi thứ 4 hay gặp ở người đã đi làm, lập kế hoạch để theo số bay ứng dụng ghi, quên nhân khuết đại ghi.” (0.88): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: đĩa/để, khuếch/khuết — NOT_VERIFIED bằng tai người',
    'Giả sử ứng dụng ghi 50 GB mỗi ngày, một số minh hoạ.':
        'ASR chép “Giả sử ứng dụng ghi 50GB mỗi ngày, một số minh họa.” (1.0): GB đọc “ghi-ga-byte” theo lexicon của khoá, ASR viết “GB/gigabyte” — NOT_VERIFIED bằng tai người',
    'Với cây B, mỗi lần sửa một bản ghi 100 byte, đĩa thật sự ghi 50 nhân 40 phẩy 96, bằng 2048 GB mỗi ngày, trung bình khoảng 23 phẩy 7 MB mỗi giây.':
        'ASR chép “Với KB, mỗi lần xử một bản ghi 100B, để thực sự ghi 50 nhân 40,96 bằng 2.048 GB mỗi ngày, trung bình khoảng 23,7 MB mỗi giây.” (0.882): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: cây (trong “cây b” → “kb”), sửa/xử, đĩa thật (trong “byte đĩa thật” → “b để thực”) — NOT_VERIFIED bằng tai người',
    'Ổ thể rắn có giới hạn tổng số byte ghi trong đời.':
        'ASR chép “Ủa thể trắng có giới hạn tổng số ba ghi trong đời.” (0.75): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: ổ/ủa, rắn/trắng — NOT_VERIFIED bằng tai người',
    'Vì vậy người có kinh nghiệm đo số byte đĩa thật sự ghi, rồi chia cho số byte ứng dụng ghi để ra khuếch đại của chính hệ mình.':
        'ASR chép “Vì vậy người có kinh nghiệm đo số bay để thật sự ghi, rồi chia cho số bay ứng dụng ghi để ra khuết đại của chính hệ minh.” (0.828): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: đĩa (trong “byte đĩa” → “bay để”), khuếch/khuết, mình/minh — NOT_VERIFIED bằng tai người',
    'Đáp án câu một, khuếch đại ghi bằng byte ghi xuống đĩa chia byte muốn ghi, tức 16384 chia 128, bằng 128 lần.':
        'ASR chép “Đáp án câu 1, khuết đại ghi bằng bay ghi xuống để chia bay muốn ghi, tức 16384 chia 128, bằng 128 lần.” (0.895): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: khuếch/khuết, đĩa/để — NOT_VERIFIED bằng tai người',
    'Đơn vị nhỏ nhất trong bảng bằng 2 mũ 10, tức 1024 byte.':
        'ASR chép “đơn vị nhỏ nhất trong bản bằng 2 mũ 10, tức 1.024 bay.” (0.895): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: bảng/bản — NOT_VERIFIED bằng tai người',
    'Vậy 16 MiB là 16 nhân 2 mũ 20, bằng 16777216 byte.':
        'ASR chép “Vậy 16 MB là 16 nhân 2 mũ 20 bằng 16777216B.” (0.926): MiB đọc “mê-ga-byte” (quy ước OSY/DEN: cách nói thông dụng, màn hình giữ MiB, câu nêu rõ 2 mũ 20), ASR viết “MB”; byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Chính xác hơn, mỗi mục là 2 mũ 10, tức 1024 byte, nên 16777216 chia 1024 bằng 16384 mục là chạm giới hạn.':
        'ASR chép “Chính xác hơn, mỗi mục là 2 mũ 10, tức 1.024 bay, nên 16777216 chia 1.024 bằng 16.384 mục là chạm giới hạn.” (0.981): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    '83886 dòng nhân 200 byte được 16777200, vẫn vừa trần.':
        'ASR chép “83.886 dòng nhân 200 by được 16777200, vẫn vừa trần.” (0.966): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Bảng giả sử mỗi bình luận nhúng 500 byte, một số minh hoạ.':
        'ASR chép “Bản giả sử mỗi bình luận nhúng 500 vai, một số minh họa.” (0.857): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: bảng/bản — NOT_VERIFIED bằng tai người',
    'Bài nổi tiếng có 30 nghìn bình luận, văn bản 15 triệu byte, vẫn dưới trần, nhưng 1000 lượt đọc kéo về tới 15 GB.':
        'ASR chép “Bài nổi tiếng có 30.000 bình luận, văn bản 15 triệu bay, vẫn dưới trần, nhưng một nghìn lượt độc kéo về tới 15 GB.” (0.931): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: đọc/độc — NOT_VERIFIED bằng tai người',
    'Một MB là 10 mũ 6 byte, một GB là 10 mũ 9 byte, nên 8 triệu 640 nghìn byte bằng 8 phẩy 64 MB.':
        'ASR chép “1 MB là 10 mũ 6 bai, 1 GB là 10 mũ 9 bai, nên 8.640.000 bai bằng 8,64 MB.” (0.9): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Mỗi giây 100 byte, một ngày 86400 giây, nên 100 nhân 86400, bằng 8 triệu 640 nghìn byte, tức 8 phẩy 64 MB.':
        'ASR chép “Mỗi giây 100 bai, 1 ngày 86.400 giây, nên 100 nhân 86.400, bằng 8.640.000 bai, tích 8,64 megabyte.” (0.9): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); MB đọc “mê-ga-byte” theo lexicon của khoá, ASR viết “MB/megabyte”; lệch âm/thanh thuần Việt: tức (trong “byte tức” → “bai tích”) — NOT_VERIFIED bằng tai người',
    'Bước bốn, xét truy vấn dài hơn.':
        'ASR chép “Bước 4 sẽ trì vấn dài hơn.” (0.714): lệch âm/thanh thuần Việt: xét truy/sẽ trì — NOT_VERIFIED bằng tai người',
    'Đi theo giờ, mỗi giờ 100 nhân 3600, bằng 360 nghìn byte, tức 0 phẩy 36 MB, nhân 24 giờ được 8 phẩy 64 MB, khớp.':
        'ASR chép “Đi theo giờ, mỗi giờ 100 nhân 3600 bằng 360.000 bai, tức 0,36 MB, nhần 24 giờ được 8,64 MB khớp.” (0.949): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: nhân/nhần — NOT_VERIFIED bằng tai người',
    'Đếm giây của cả năm trước, 86400 nhân 365 bằng 31 triệu 536 nghìn giây, nhân 100 byte được khoảng 3 tỉ 154 triệu byte, tức khoảng 3 phẩy 15 GB, cũng khớp.':
        'ASR chép “Đếm giây của cả năm trước, 86.400 nhân 365 bằng 31 triệu 536.000 giây, nhân 100 bai được khoảng 3.154 triệu bai, tức khoảng 3,15 gigabyte, cũng khớp.” (0.926): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); “tỉ” ASR viết chính tả “tỷ” (cùng âm); GB đọc “ghi-ga-byte” theo lexicon của khoá, ASR viết “GB/gigabyte” — NOT_VERIFIED bằng tai người',
    'Bảng tính cho ba mức ghi, mức 100 byte mỗi giây cho 8 phẩy 64 MB mỗi ngày như ví dụ.':
        'ASR chép “Bản tính cho 3 mức ghi, mức 100 bai mỗi dây cho 8,64 MB mỗi ngày như ví dụ.” (0.917): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: bảng/bản — NOT_VERIFIED bằng tai người',
    'Một thiết bị ghi gấp 100 lần, 10 nghìn byte mỗi giây, có phân vùng ngày nặng 864 MB.':
        'ASR chép “Một thiết bị ghi gấp 100 lần, 10.000 bai mỗi giây có phân vùng ngày nặng 864 MB.” (0.958): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Bước bốn, lọc trùng.':
        'ASR chép “Bước 4, lọc trung” (0.75): lệch âm/thanh thuần Việt: trùng/trung — NOT_VERIFIED bằng tai người',
    'Bước bốn, gom lại thành bảng để rút ra quy tắc.':
        'ASR chép “Bước 4, gom lại thành bản để trúc tra quy tắc” (0.727): lệch âm/thanh thuần Việt: bảng/bản, rút ra/trúc tra — NOT_VERIFIED bằng tai người',
    'Bước hai, phát tán.':
        'ASR chép “Bước 2. Phát tảnh” (0.75): lệch âm/thanh thuần Việt: tán/tảnh — NOT_VERIFIED bằng tai người',
    'Bước ba, xáo trộn.':
        'ASR chép “Bước 3. Sáu trộn” (0.75): lệch âm/thanh thuần Việt: xáo/sáu — NOT_VERIFIED bằng tai người',
    'Vì bảng nhỏ 1 GB vừa bộ nhớ mỗi máy, ta chọn phát tán.':
        'ASR chép “Vì bảng nhỏ 1GB vừa bộ nhớ mỗi máy, ta chọn phát tán.” (1.0): GB đọc “ghi-ga-byte” theo lexicon của khoá, ASR viết “GB/gigabyte” — NOT_VERIFIED bằng tai người',
    'Bảng nhỏ cần 2 GB mà mỗi máy chỉ có 1 GB trống.':
        'ASR chép “Bản nhỏ cần 2GB mà mỗi máy chỉ có 1GB trống.” (0.923): lệch âm/thanh thuần Việt: bảng/bản — NOT_VERIFIED bằng tai người',
    # ── Đợt A đào sâu: MLO ──
    'Trước hết ta ôn một điều về tệp.':
        'ASR chép “Trước hết ta ôm một điều về tệ.” (0.75): lệch âm/thanh thuần Việt: ôn/ôm, tệp/tệ — NOT_VERIFIED bằng tai người',
    'Một tệp dữ liệu chỉ là một dãy byte, mỗi ký tự thường là 1 byte, mang một con số.':
        'ASR chép “Một tệp dữ liệu chỉ là một giải bay, mỗi ký từ thường là một bay, mang một con số.” (0.8): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: dãy (trong “dãy byte” → “giải bay”), tự/từ — NOT_VERIFIED bằng tai người',
    'Chữ số 1 là byte 49, dấu phẩy là 44, chữ số 0 là 48, và dấu xuống dòng là byte 10.':
        'ASR chép “Chữ số 1 là bai 49, giấu phải là 44, chữ số 0 là 48 và giấu xuống dòng là bai 10.” (0.893): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải” — NOT_VERIFIED bằng tai người',
    'Hình vẽ hai tệp, mỗi ô là một byte, ô xám là dấu xuống dòng.':
        'ASR chép “Hình vẽ 2 tệp, mỗi ô là một bay, ô xám là giấu xuống dòng.” (0.933): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Tệp A và tệp B dài 20 byte và chỉ khác nhau đúng một byte, ô viền đỏ, nơi nhãn 1 đổi thành 0.':
        'ASR chép “Tẹp A và tẹp B dài hai mươi bay và chỉ khác nhau đúng một bay, ồ viền đỏ, nơi nhãn một đổi thành không.” (0.8): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); “ô” (ô lưới) ASR viết chữ “O”; lệch âm/thanh thuần Việt: tệp/tẹp, tệp/tẹp — NOT_VERIFIED bằng tai người',
    'Bước một, tệp A có ba dòng, mẫu thứ hai mang nhãn 1, ta đưa đủ 20 byte của nó vào hàm băm và lấy 12 ký tự đầu.':
        'ASR chép “Bước một, tạp A có ba dòng, mẫu thứ hai mang nhãn một. Ta đưa đủ hai mi bay của nó vào hàm băm và lấy mười hai ký tự đầu.” (0.903): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: tệp/tạp, mươi (trong “mươi byte” → “mi bay”) — NOT_VERIFIED bằng tai người',
    'Thực ra chỉ đúng một byte đổi, từ 49 thành 48.':
        'ASR chép “Thực tra chỉ đúng một bay đổi từ 49 thành 48.” (0.867): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: ra/tra — NOT_VERIFIED bằng tai người',
    'Băm lại 20 byte của A bằng một công cụ khác vẫn ra đúng mã cũ.':
        'ASR chép “Băm lại 20 bai của A bằng một công cụ khác vẫn ra đúng mạ cũ.” (0.882): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: mã/mạ — NOT_VERIFIED bằng tai người',
    'Còn nếu lưu với kiểu xuống dòng khác, mỗi dòng thêm 1 byte, tệp thành 24 byte, và mã băm khác.':
        'ASR chép “Còn nếu lưu với kiểu xuống dòng khác, mỗi dòng thêm một bay, tẹp thành 24 bay và mã băm khác.” (0.87): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: tệp (trong “byte tệp” → “bay tẹp”) — NOT_VERIFIED bằng tai người',
    'Lưu theo mã băm từng tệp thì chỉ tốn 5 GB ban đầu cộng 9 tệp sửa, mỗi tệp 0 phẩy 05 GB, tổng 5 phẩy 45 GB, ít hơn khoảng 9 lần.':
        'ASR chép “Lưu theo mả 3 từng tệp thì chỉ tốn 5GB ban đầu cộng 9 tệp sửa, mỗi tệp không phải 0.5GB, tổng 5.45GB, ít hơn khoảng 9 lần.” (0.886): “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; lệch âm/thanh thuần Việt: mã băm/mả ba — NOT_VERIFIED bằng tai người',
    'Tên tệp không nằm trong byte nội dung, nên tên khác nhau không nói lên điều gì.':
        'ASR chép “Tên Tật không nằm trong bài nội dung, nền tên khác nhau không nói lên điều gì.” (0.824): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: tệp/tật, nên/nền — NOT_VERIFIED bằng tai người',
    'Ở khoá DevOps, một kiểm thử chạy mã với một đầu vào rồi so với điều kỳ vọng, kết quả là đạt hoặc trượt, ví dụ hàm cộng nhận 2 và 3 phải trả về 5.':
        'ASR chép “Ở khóa Devoop, một kiểm thử chạy mã với một đầu vào rồi so với điều kỳ vọng, kết quả là đạt hoặc trượt, ví dụ hàm cộng nhận 2 và 3 phải trả về 5.” (0.972): DevOps đọc thô (probe DVO p1: 6/8, NOT_VERIFIED) — NOT_VERIFIED bằng tai người',
    'Bước hai, nhóm một giảm còn 10 phần trăm, số hạng là âm 0 phẩy 15 nhân lôgarit của 0 phẩy 4, khoảng 0 phẩy 1374.':
        'ASR chép “Bước 2, nhóm 1 giảm còn 10%, số hạng là âm 0,15 nhân Logatrix của 0,4, khoảng 0,1374.” (0.97): lệch âm/thanh thuần Việt: lôgarit/logatrix — NOT_VERIFIED bằng tai người',
    'Bước hai, các vòng sau lặp lại y hệt.':
        'ASR chép “Bước 2, các vòng sau lập lại y hợp.” (0.778): lệch âm/thanh thuần Việt: lặp/lập, hệt/hợp — NOT_VERIFIED bằng tai người',
    'Bảng so một mô hình lười, luôn nói đúng tỉ lệ có bệnh.':
        'ASR chép “Bản sau một mô hình lươi luôn nói đúng tỷ lệ có bệnh.” (0.692): “tỉ” ASR viết chính tả “tỷ” (cùng âm); lệch âm/thanh thuần Việt: bảng so/bản sau, lười/lươi — NOT_VERIFIED bằng tai người',
    'Ở khoá Hệ thống máy tính, ta đã học 8 bit làm thành 1 byte.':
        'ASR chép “Ở khóa hệ thống máy tính, ta đã học 8 bit làm thành một bay.” (0.933): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Số thực 32 bit chiếm 32 chia 8, bằng 4 byte.':
        'ASR chép “Số thực 32 biết chiếm 32 chia 8, bằng 4 vai.” (0.867): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: bit/biết — NOT_VERIFIED bằng tai người',
    'Số thực 16 bit chiếm 2 byte.':
        'ASR chép “Số thực 16 biết chiếm hai bay.” (0.75): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: bit/biết — NOT_VERIFIED bằng tai người',
    'Số nguyên 8 bit chiếm đúng 1 byte.':
        'ASR chép “Số nguyên 8 bịch chiếm đúng một bay.” (0.75): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: bit/bịch — NOT_VERIFIED bằng tai người',
    'Nhân số lớn thì nhân phần số rồi giữ đơn vị, 7 tỉ tham số nhân 4 byte được 28 tỉ byte.':
        'ASR chép “Nhân số lớn thì nhân phần số rồi giữ đơn vị, 7 tỷ tham số nhân 4 bay được 28 tỷ bay.” (0.833): “tỉ” ASR viết chính tả “tỷ” (cùng âm); byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Vì 1 GB là 1 tỉ byte, đó là 28 GB.':
        'ASR chép “Vì 1GB là 1 tỷ bay, đó là 28GB.” (0.846): “tỉ” ASR viết chính tả “tỷ” (cùng âm); byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Với bộ nhớ, đếm theo bit, 7 tỉ tham số nhân 8 bit được 56 tỉ bit, chia 8 được 7 tỉ byte.':
        'ASR chép “Với bộ nhớ, đếm theo bit, 7 tỷ tham số nhân 8 bit được 56 tỷ bit, chia 8 được 7 tỷ bay.” (0.84): “tỉ” ASR viết chính tả “tỷ” (cùng âm); byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Còn bộ nhớ, 16 bit là 2 byte.':
        'ASR chép “Còn bộ nhớ, 16 bit là hai bay.” (0.889): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Đáp án câu một, 0 phẩy 3 cộng 0 phẩy 2 bằng 0 phẩy 5, dương, nên nhãn 1.':
        'ASR chép “Đáp án câu 1, không phải 3 cộng, không phải 2 bằng, không phải 5. Du, nên nhãn 1.” (0.789): “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; lệch âm/thanh thuần Việt: dương/du — NOT_VERIFIED bằng tai người',
    # ── Đợt A đào sâu: DAN ──
    'Thứ hai, múi giờ.':
        'ASR chép “Thứ 2. Mũi giờ” (0.75): lệch âm/thanh thuần Việt: múi/mũi — NOT_VERIFIED bằng tai người',
    'Bước ba, cột hạng theo tiền giảm dần.':
        'ASR chép “Bước 3. Cột hàng theo tiền giảm dân.” (0.75): lệch âm/thanh thuần Việt: hạng/hàng, dần/dân — NOT_VERIFIED bằng tai người',
    'Cộng các chênh lệch, 20 trừ 10 cộng 20 được 30.':
        'ASR chép “Cộng các chính lịch 20 trường 10 cộng 20 được 30.” (0.786): lệch âm/thanh thuần Việt: chênh lệch/chính lịch, trừ/trường — NOT_VERIFIED bằng tai người',
    'Bước hai, điểm z.':
        'ASR chép “Bước 2. Điểm Jack” (0.75): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Đáp án câu một, ta so trị tuyệt đối của điểm z với ngưỡng, trị tuyệt đối của âm 2 phẩy 44 là 2 phẩy 44, nhỏ hơn 3.':
        'ASR chép “Đáp án câu 1, ta so trị tuyệt đối của điểm dép với ngưỡng, trị tuyệt đối của âm 2,44 là 2,44, nhỏ hơn 3.” (0.97): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    # ── Đợt A đào sâu: DSC ──
    'Chia cho 4 trừ 1 bằng 3, phương sai mẫu xấp xỉ 6 phẩy 667.':
        'ASR chép “Chia cho 4,1 triệu bằng 3, phương sai mẫu sắp xị 6,667.” (0.769): “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; lệch âm/thanh thuần Việt: trừ/phẩy, xấp xỉ/sắp xị — NOT_VERIFIED bằng tai người',
    'Độ lệch là giá trị trừ trung bình.':
        'ASR chép “Đỗ lịch là giá trị trừ trung bình.” (0.75): lệch âm/thanh thuần Việt: độ lệch/đỗ lịch — NOT_VERIFIED bằng tai người',
    'Lỗi thứ tư, người đã đi làm cũng hay mắc, là tính r chỉ trên những người đã qua vòng lọc.':
        'ASR chép “Lỗi thứ 4, người đã đi làm cũng hay mắc là tính error chỉ trên những người đã qua vòng lộc.” (0.905): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: lọc/lộc — NOT_VERIFIED bằng tai người',
    'Sau chuẩn hoá thành âm 1, 0, 1.':
        'ASR chép “Sau chuẩn hóa thành âm mụt, không mụt.” (0.75): lệch âm/thanh thuần Việt: một/mụt, một/mụt — NOT_VERIFIED bằng tai người',
    'Đảo hai vế là đổi nhóm để đếm, nên kết quả khác nhau.':
        'ASR chép “Đạo 2 với là đội nhóm để đếm nên kết quả khác nhau.” (0.769): lệch âm/thanh thuần Việt: đảo/đạo, vế/với, đổi/đội — NOT_VERIFIED bằng tai người',
    # ── Đợt A đào sâu: WEB ──
    'Tải 100 KB, tức 800 nghìn bit, qua đường 10 triệu bit mỗi giây mất 80 mi li giây.':
        'ASR chép “Tải 100 kilobytes, tức 800.000 bit, qua đường 10 triệu bit mỗi giây mất 80 mili giây.” (0.884): KB đọc “ki-lô-byte” theo lexicon của khoá, ASR viết “kilobyte/kg”; tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh — NOT_VERIFIED bằng tai người',
    'Vì vậy byte đầu tiên chỉ tới ở mốc 150 mi li giây, dù đường truyền rộng tới đâu.':
        'ASR chép “Vì vậy bay đầu tiên chỉ tới ở mốc 150 mili dây, dù đường truyền rộng tới đâu.” (0.837): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh — NOT_VERIFIED bằng tai người',
    'Đồng hồ cộng dồn đi từ 0 lên 50 mi li giây, mà chưa có byte dữ liệu nào.':
        'ASR chép “Đồng hồ cộng dồn đi từ không lên 50 ms mà chưa có 3 dữ liệu nào.” (0.842): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Đồng hồ cộng dồn lên 50 cộng 50, bằng 100 mi li giây, và vẫn chưa có byte dữ liệu nào.':
        'ASR chép “Đồng hồ cộng dồn lên 50 cộng 50 bằng 100ml và vẫn chưa có bai giữ liệu nào.” (0.87): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Bảng cộng dồn các bước với vòng khứ hồi 50 mi li giây, tới đây là 150 mi li giây thì byte đầu tiên mới tới.':
        'ASR chép “Bảng cộng dồn các bước với vòng khứ hồi 50mS, tới đây là 150mS thì bay đầu tiên mới tới.” (0.821): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Bảng so hai nơi đo, cùng 3 vòng khứ hồi trước byte đầu tiên.':
        'ASR chép “Bảng so hai nơi đo cùng ba vòng khứ hội trước bay đầu tiên.” (0.857): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: hồi/hội — NOT_VERIFIED bằng tai người',
    'Đo cạnh máy chủ với vòng khứ hồi 1 mi li giây, trang chỉ tốn 3 mi li giây.':
        'ASR chép “Đo cạnh máy chủ với vòng khứ hồi 1 mili dây, trang chỉ tốn 3 mili dây.” (0.722): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh — NOT_VERIFIED bằng tai người',
    'Người dùng ở xa với vòng khứ hồi 200 mi li giây phải chờ 600 mi li giây, gấp 200 lần, nên hãy đo với vòng khứ hồi của người dùng thật.':
        'ASR chép “Người dùng ở xa với vòng khứ hội 200 mili dây phải chờ 600 mili dây gấp 200 lần nên hãy đo với vòng khứ hội của người dùng thật.” (0.794): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; lệch âm/thanh thuần Việt: hồi/hội, hồi/hội — NOT_VERIFIED bằng tai người',
    'Thẻ HTML lồng nhau y hệt như ngoặc, thẻ mở là ngoặc mở, thẻ đóng là ngoặc đóng.':
        'ASR chép “Thẻ HT-ML lồng nhau y hệt như ngọc, thẻ mở là ngọc mở, thẻ đóng là ngọc đóng.” (0.757): HTML đọc “hát tê em eo” theo lexicon WEB, ASR viết “html/HT ML”; lệch âm/thanh thuần Việt: ngoặc/ngọc, ngoặc/ngọc, ngoặc/ngọc — NOT_VERIFIED bằng tai người',
    'Thêm một phép thử nữa, đổi chỗ dòng hẹn giờ và dòng lời hứa rồi chạy thật, thứ tự in vẫn y nguyên.':
        'ASR chép “Thêm một phép thử nữa, đổ chỗ dòng hẹn giờ và dòng lời hứa trôi chạy thật, thứ tự in vẫn yên nguyên.” (0.87): lệch âm/thanh thuần Việt: đổi/đổ, rồi/trôi, i/yên — NOT_VERIFIED bằng tai người',
    'A và F là mã đồng bộ, B là hẹn giờ nên vào hàng tác vụ, C và E vào hàng vi mô.':
        'ASR chép “A và S là mã đồng bộ, B là hẹn giờ nên vào hàng tác vụ, C và E vào hàng vi mô.” (0.957): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Điều thứ hai, nhắc lại bài 0 và bài 6, mỗi yêu cầu GET tốn ít nhất một vòng khứ hồi, và tải thân trang thì thêm thời gian truyền.':
        'ASR chép “Điều thứ hai, nhắc lại bài 0 và bài 6, mỗi yêu cầu ghét tốn ít nhất một vòng khứ hội và tải thân trang thì thêm thời gian truyền.” (0.933): GET đọc “gét” theo lexicon WEB, ASR viết “ghét”; lệch âm/thanh thuần Việt: hồi/hội — NOT_VERIFIED bằng tai người',
    'Bảng dùng vòng khứ hồi 50 mi li giây và đường 10 triệu bit mỗi giây để so ba cách lấy trang 50 KB.':
        'ASR chép “Bản dùng vòng khứ hồi 50 mili dây và đường 10 triệu biết mỗi dây để so ba cách lấy tràng 50 kilobytes.” (0.745): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; KB đọc “ki-lô-byte” theo lexicon của khoá, ASR viết “kilobyte/kg”; lệch âm/thanh thuần Việt: bảng/bản, bit/biết, trang/tràng — NOT_VERIFIED bằng tai người',
    'Tải lại cả thân 400 nghìn bit thì thêm 40 mi li giây truyền, tổng 90 mi li giây.':
        'ASR chép “Tải lại cả thân 400.000 bit thì thêm 40 mili dây truyền, tổng 90 mili dây.” (0.762): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh — NOT_VERIFIED bằng tai người',
    'Trình duyệt dùng thẳng bản lưu, không ra mạng, tải về 0 byte và chờ 0 mi li giây.':
        'ASR chép “Trình duyệt dùng thẳng bảng lưu, không ra mạng, tải về không bay và chờ không milli dây.” (0.757): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; lệch âm/thanh thuần Việt: bản/bảng — NOT_VERIFIED bằng tai người',
    'Đã cũ và đã đổi thì mới phải chờ 90 mi li giây để tải lại 50 KB.':
        'ASR chép “Đã củ và đã đổi thì mới phải chờ 90mg để tải lại 50kb.” (0.842): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; lệch âm/thanh thuần Việt: cũ/củ — NOT_VERIFIED bằng tai người',
    'Thân trang chỉ phải tải đúng 50 KB, thay vì 12 nhân 50 bằng 600 KB.':
        'ASR chép “Thân trang chỉ phải tải đúng 50 kilobyte, thay vì 12 nhân 50 bằng 600 kilobyte.” (0.9): KB đọc “ki-lô-byte” theo lexicon của khoá, ASR viết “kilobyte/kg” — NOT_VERIFIED bằng tai người',
    'Bảng dùng số minh hoạ, 2000 người, mỗi người mở 5 lần một ngày, tệp tĩnh 500 KB.':
        'ASR chép “Bản dùng số minh họa, 2.000 người, mỗi người mở 5 lần 1 ngày, tẹp tỉnh 500 kg.” (0.8): KB đọc “ki-lô-byte” theo lexicon của khoá, ASR viết “kilobyte/kg”; lệch âm/thanh thuần Việt: bảng/bản, tệp tĩnh/tẹp tỉnh — NOT_VERIFIED bằng tai người',
    'Tắt bộ nhớ đệm thì mỗi ngày tải 2000 nhân 5 nhân 500 KB, bằng 5 GB.':
        'ASR chép “Tắt bộ nhớ đệm thì mỗi ngày tại 2.000 nhân 5 nhân 500KB bằng 5GB.” (0.947): lệch âm/thanh thuần Việt: tải/tại — NOT_VERIFIED bằng tai người',
    'Bước một, ứng dụng tạo chuỗi bí mật từ 32 byte ngẫu nhiên, viết thành 43 ký tự, nằm trong độ dài cho phép từ 43 tới 128.':
        'ASR chép “Bước 1 ứng dụng tạo chuỗi bí mật từ 32 bai ngẫu nhiên, viết thành 43 ký tự, nằm trong độ dài cho phép từ 43 tới 128.” (0.974): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Bước hai, băm chuỗi bí mật bằng hàm băm đã ôn, được đúng 32 byte, tức 256 bit, bắt đầu bằng các byte 13, d 3, 1 e, viết theo hệ mười sáu.':
        'ASR chép “Bước 2, băm chuỗi bí mật bằng hàm băm đã ôn, được đúng 32 bay, tức 256 bit, bắt đầu bằng các bay 13, V3, 1E, viết theo hệ 16.” (0.925): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Ba byte đầu của mã băm là 13, d 3, 1 e, viết ra thành 24 bit.':
        'ASR chép “Ba bay đầu của mã BAM là 13, D3, 1E, viết ra thành 24 bit.” (0.9): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: băm/bam — NOT_VERIFIED bằng tai người',
    'Trước hết, ta quy ước trong bài này 1 KB là 1000 byte, và 1 MB là 1000 KB.':
        'ASR chép “Trước hết, ta quy ước trong bài này 1 kilobyte là 1000 byte và 1 megabyte là 1000 kilobyte.” (0.857): KB đọc “ki-lô-byte” theo lexicon của khoá, ASR viết “kilobyte/kg”; MB đọc “mê-ga-byte” theo lexicon của khoá, ASR viết “MB/megabyte” — NOT_VERIFIED bằng tai người',
    'Ví dụ tệp 600 KB trên mạng 200 KB mỗi giây thì tải mất 600 chia 200, bằng 3 giây.':
        'ASR chép “Ví dụ tệp 600 kilobyte trên mạng 200 kilobyte mỗi dây thì tại mất 600 chi 200, bằng 3 dây.” (0.833): KB đọc “ki-lô-byte” theo lexicon của khoá, ASR viết “kilobyte/kg”; lệch âm/thanh thuần Việt: tải/tại, chia/chi — NOT_VERIFIED bằng tai người',
    'Hàng trên của hình là đường kết xuất quan trọng, từ HTML tới phần kiểu dáng và mã đồng bộ, rồi dựng cây, tính bố cục, và vẽ.':
        'ASR chép “Hàng trên của hình là đường kết xuất quan trọng, từ html tới phần kiểu dán và mã đồng bộ, rồi dựng cây, tính bố cục và vẽ.” (0.964): lệch âm/thanh thuần Việt: dáng/dán — NOT_VERIFIED bằng tai người',
    'Hai thanh ở dưới vẽ đúng tỉ lệ thời gian tải trên mạng 200 KB mỗi giây, thanh cam 10 giây, thanh xanh 2 phẩy 5 giây, ngắn hơn đúng 4 lần.':
        'ASR chép “2 thanh ở dưới vẽ đúng tỷ lệ thời gian tải trên mạng 200 kb mỗi giây, thanh ca 10 giây, thanh xanh 2,5 giây, ngãn hơn đúng 4 lần.” (0.909): “tỉ” ASR viết chính tả “tỷ” (cùng âm); lệch âm/thanh thuần Việt: cam/ca, ngắn/ngãn — NOT_VERIFIED bằng tai người',
    'Bước một, đổi về cùng đơn vị, vì băng thông tính theo KB mỗi giây nên kích thước cũng phải tính theo KB.':
        'ASR chép “Bước 1, đổi về cùng đơn vị, vì ban thông tính theo kilobyte mỗi giây, nên kích thước cũng phải tính theo kilobyte.” (0.87): KB đọc “ki-lô-byte” theo lexicon của khoá, ASR viết “kilobyte/kg”; lệch âm/thanh thuần Việt: băng/ban — NOT_VERIFIED bằng tai người',
    'Ta có 2 MB bằng 2 nhân 1000, tức 2000 KB.':
        'ASR chép “ta có 2 megabyte bằng 2 nhân 1 nghìn, tức 2 nghìn kilobyte.” (0.846): MB đọc “mê-ga-byte” theo lexicon của khoá, ASR viết “MB/megabyte”; KB đọc “ki-lô-byte” theo lexicon của khoá, ASR viết “kilobyte/kg” — NOT_VERIFIED bằng tai người',
    'Giả sử ảnh chính nặng 300 KB, đây là số minh hoạ, thì tổng trên đường kết xuất là 500 cộng 300, bằng 800 KB.':
        'ASR chép “Giả sự ảnh chính nặng 300 kilobyte, đây là số minh họa, thì tổng trên đường kết xuất là 500 cộng 300 bằng 800 kilobyte.” (0.897): KB đọc “ki-lô-byte” theo lexicon của khoá, ASR viết “kilobyte/kg”; lệch âm/thanh thuần Việt: sử/sự — NOT_VERIFIED bằng tai người',
    'Mười giây nhân 200 KB mỗi giây được 2000 KB, đúng 2 MB.':
        'ASR chép “10 giây nhân 200 kilobyte mỗi giây được 2.000 kilobyte, đúng 2 megabyte.” (0.8): KB đọc “ki-lô-byte” theo lexicon của khoá, ASR viết “kilobyte/kg”; MB đọc “mê-ga-byte” theo lexicon của khoá, ASR viết “MB/megabyte” — NOT_VERIFIED bằng tai người',
    'Hai phẩy 5 giây nhân 200 được 500 KB, khớp bản đã cắt.':
        'ASR chép “2,5 dây nhân 200 được 500kg, khớp bạn đã cắt.” (0.867): KB đọc “ki-lô-byte” theo lexicon của khoá, ASR viết “kilobyte/kg”; lệch âm/thanh thuần Việt: bản/bạn — NOT_VERIFIED bằng tai người',
    'Bốn giây nhân 200 được 800 KB, khớp tổng có ảnh chính.':
        'ASR chép “Bốn dây nhân 200 được 800 kilobyte, khớp tổng có ảnh chính.” (0.929): KB đọc “ki-lô-byte” theo lexicon của khoá, ASR viết “kilobyte/kg” — NOT_VERIFIED bằng tai người',
    'Bảng so hai cách khi sửa một dòng trên mạng 200 KB mỗi giây.':
        'ASR chép “bản so 2 cách khi sửa 1 dòng trên mạng 200 kb mỗi dây.” (0.933): lệch âm/thanh thuần Việt: bảng/bản — NOT_VERIFIED bằng tai người',
    'Một tệp 2 MB thì phải tải lại 2000 KB, mất 10 giây.':
        'ASR chép “Một tệp 2MB thì phải tải lại 2000KB, mất 10 giây.” (1.0): KB đọc “ki-lô-byte” theo lexicon của khoá, ASR viết “KB/kilobyte”; MB đọc “mê-ga-byte” theo lexicon của khoá, ASR viết “MB/megabyte” — NOT_VERIFIED bằng tai người',
    'Nếu tách riêng phần hay đổi chỉ 100 KB thì chỉ tải lại 100 KB, mất 0 phẩy 5 giây, nhanh gấp 20 lần.':
        'ASR chép “Nếu tách riêng phần hay đổi chỉ 100 kilobyte thì chỉ tải lại 100 kilobyte, mất 0,5 giây, nhành gấp 20 lần.” (0.889): KB đọc “ki-lô-byte” theo lexicon của khoá, ASR viết “kilobyte/kg”; lệch âm/thanh thuần Việt: nhanh/nhành — NOT_VERIFIED bằng tai người',
    'Câu ba là một quyết định, phải cắt bớt bao nhiêu KB khỏi trang ở câu một để đạt ngân sách đó?':
        'ASR chép “Câu 3 là một quyết định phải cắt bớt bao nhiêu kilobytes khỏi trang ở câu 1 để đạt ngân sách đó.” (0.955): KB đọc “ki-lô-byte” theo lexicon của khoá, ASR viết “kilobyte/kg” — NOT_VERIFIED bằng tai người',
    'Câu ba, phải cắt 1200 trừ 375, bằng 825 KB, tức hơn hai phần ba trang, nên cần tách và tải sau phần lớn tài nguyên.':
        'ASR chép “Câu 3 phải cắt 1.200-375 bằng 825 kilobytes, tức hơn 2 phần 3 trang, nền cần tách và tải sau phần lớn tại nguyên.” (0.904): KB đọc “ki-lô-byte” theo lexicon của khoá, ASR viết “kilobyte/kg”; lệch âm/thanh thuần Việt: trừ/∅, nên/nền, tài/tại — NOT_VERIFIED bằng tai người',
    'Bảng lấy 10 khung đo được, 9 khung mỗi khung 8 mi li giây và 1 khung 48 mi li giây.':
        'ASR chép “Bản lấy 10 khung đo được 9 khung mổi, khung 8 mili giây và 1 khung 48 mili giây.” (0.773): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; lệch âm/thanh thuần Việt: bảng/bản, mỗi/mổi — NOT_VERIFIED bằng tai người',
    'Bảng dùng số minh hoạ, mỗi mục 200 byte.':
        'ASR chép “Bản dùng số minh họa mỗi 1-200 bay.” (0.7): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: bảng/bản, mục/một — NOT_VERIFIED bằng tai người',
    'Gửi toàn bộ 5000 mục là 1 triệu byte mỗi lần đồng bộ.':
        'ASR chép “Gửi toàn bộ 5.000 mục là 1 triệu bai mỗi lần đồng bộ.” (0.929): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    # ── Đợt A đào sâu: PLC ──
    'Riêng ký tự a còng không khớp mẫu từ tố nào của ngôn ngữ, nên lỗi bị bắt ngay ở pha từ vựng.':
        'ASR chép “Riên ký tự A còn không khắp mẫu từ tố nào của ngôn ngữ nên lỗi bị bắt ngay ở pha tư vận.” (0.783): lệch âm/thanh thuần Việt: riêng/riên, còng/còn, khớp/khắp, từ vựng/bốn vận — NOT_VERIFIED bằng tai người',
    'Hình vẽ một phần ô-tô-mát của bộ phân tích, mỗi vòng tròn là một trạng thái, vòng kép là trạng thái chấp nhận được, tức là đã đọc đủ một từ tố.':
        'ASR chép “Hình với một phần Automat của bộ phân tích, mỗi vòng tròn là một trạng thái, vòng kép là trạng thái chấp nhận được, tức là đã đọc đủ một tư tố.” (0.879): “ô” (ô lưới) ASR viết chữ “O”; lệch âm/thanh thuần Việt: vẽ/với, tô mát (trong “ô tô mát” → “automat”), từ/bốn — NOT_VERIFIED bằng tai người',
    'In không ngoặc thành 8 trừ 3 trừ 2.':
        'ASR chép “tình không hoạt thành 8 trừ 3 trừ 2.” (0.778): lệch âm/thanh thuần Việt: in/tình, ngoặc/hoạt — NOT_VERIFIED bằng tai người',
    'Khi g gọi f, chồng lời gọi có thêm f ở trên cùng.':
        'ASR chép “Khi ve gọi F, chồng lời gọi có thêm F ở trên cùng.” (0.923): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Viết ở hệ mười sáu, đó là 3 F 8 0 0 0 0 0, đúng dãy bit ta vừa ôn ở phần chuẩn bị.':
        'ASR chép “Viết ở hệ 16, đó là 3F800000, đúng vậy biết ta vừa ôn ở phần chuẩn bị.” (0.766): lệch âm/thanh thuần Việt: không không không không không/trăm nghìn, dãy bit/vậy biết — NOT_VERIFIED bằng tai người',
    'Khung của f đã bị gỡ, nên mũi tên từ biến của f tới S biến mất, và số đếm của S tụt từ 1 về 0.':
        'ASR chép “Khung của ép đã bị gỡ nên mũi tên từ biến của ép tới ép biến mất và số đếm của ép tục từ 1 về 0.” (0.889): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: tụt (trong “s tụt” → “ép tục”) — NOT_VERIFIED bằng tai người',
    'Với câu hai, đếm trước số tham chiếu, R có 1 từ gốc, X có 2 từ R và Y, Y có 1, Z có 0, W có 1 từ Z.':
        'ASR chép “Với câu 2, đểm trước số tham chiếu, R có một từ gốc, Y có hai từ R và Y, Y có một, Z có không, Về đút có một từ Z.” (0.889): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: đếm/đểm — NOT_VERIFIED bằng tai người',
    'Câu một, hỏi cuối cùng k của m bằng mấy, và vì sao?':
        'ASR chép “Câu 1 Hỏi cuối cùng ca của em mờ bằng mấy và vì sao?” (0.889): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Cách thứ nhất là sửa đối tượng, gán khoá k của d bằng 3, vì sửa đối tượng thì người gọi thấy.':
        'ASR chép “Cách thứ nhất là sửa đối tượng, gán khóa ca của dây bằng 3 vì sửa đối tượng thì người gọi thấy.” (0.955): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Đẩy 4 vào, ngăn xếp có 4.':
        'ASR chép “Đẩy bún vào, ngăn xếp có bún.” (0.714): lệch âm/thanh thuần Việt: bốn/bún, bốn/bún — NOT_VERIFIED bằng tai người',
    'Bước một, sinh mã cho cây 1 cộng 2 nhân 3 bằng duyệt sau.':
        'ASR chép “Bước 1, xin mã cho cây 1 cộng 2 nhân 3 bằng vùi sâu.” (0.786): lệch âm/thanh thuần Việt: sinh/xin, duyệt sau/vùi sâu — NOT_VERIFIED bằng tai người',
    'Trước tối ưu, vòng lặp chạy một nghìn lần, mỗi lần một phép, tổng cộng một nghìn phép.':
        'ASR chép “Trước tối yêu, vòng lập chạy một nghìn lần, mỗi lần một phét, tổng cộng một nghìn phét.” (0.778): lệch âm/thanh thuần Việt: ưu/yêu, lặp/lập, phép/phét, phép/phét — NOT_VERIFIED bằng tai người',
    # ── Đợt A đào sâu: AGT ──
    'Còn chuỗi chữ 1000, viết trong ngoặc kép, cộng với chính nó thì máy nối hai chuỗi lại, thành một dãy tám chữ số 10001000, chứ không phải 2000.':
        'ASR chép “Còn chủ chữ 1000, viết trong hoạt kết, cộng với chính nó thì máy nối 2 chủ lại, thành một dạy 8 chữ số 1000000, chứ không phải 2000.” (0.754): chữ w đọc “vê kép” (luật chung), ASR viết tách chữ; lệch âm/thanh thuần Việt: chuỗi/chủ, ngoặc (trong “ngoặc kép” → “hoạt kết”), chuỗi/chủ, dãy/dạy, mười/một, không trăm linh một nghìn/∅ — NOT_VERIFIED bằng tai người',
    'Chia 80 cho 30, được xấp xỉ 2 phẩy 67, dấu bằng lượn sóng đọc là xấp xỉ.':
        'ASR chép “Chìa 80 cho 30, được sắp xỉ 2,67, dấu bằng lượng sóng độc là sắp xỉ.” (0.773): lệch âm/thanh thuần Việt: chia/chìa, xấp/sắp, lượn/lượng, đọc/độc, xấp/sắp — NOT_VERIFIED bằng tai người',
    'Trước hết, ôn khái niệm độ phủ.':
        'ASR chép “Trước hết, ông khái niệm đồ phủ.” (0.714): lệch âm/thanh thuần Việt: ôn/ông, độ/đồ — NOT_VERIFIED bằng tai người',
    'Câu nghỉ phép 12 ngày mỗi năm có nguyên văn trong nguồn S 1, nên đạt.':
        'ASR chép “Câu nghỉ phép 12 ngày mỗi năm có nguyên văn trong nguồn F1, nên đạt.” (0.941): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Hình bên phải là một ngôi sao, tác tử điều phối Đ ở giữa và 5 tác tử làm việc xung quanh.':
        'ASR chép “Hình bên phải là một ngôi sao, tác tử điều phối đe ở giữa và 5 tác tử làm việc xung quanh.” (0.955): lệch âm/thanh thuần Việt: đ/đe — NOT_VERIFIED bằng tai người',
    'Mỗi tác tử chỉ có một đường tới Đ, đi và về là 2 kênh, tổng cộng 10 kênh.':
        'ASR chép “Mỗi tác tử chỉ có một đường tới đê, đi và về là 2 kênh, tổng cộng 10 kênh.” (0.947): lệch âm/thanh thuần Việt: đ/d — NOT_VERIFIED bằng tai người',
    'Đổi lại, mọi tin nhắn đều đi qua Đ, nên Đ là chỗ dễ nghẽn nhất.':
        'ASR chép “Đổi lại, mọi tin nhắn đều đi qua đe, nên đe là chỗ dễ ngãng nhất.” (0.812): lệch âm/thanh thuần Việt: đ/đe, đ/đe, nghẽn/ngãng — NOT_VERIFIED bằng tai người',
    'Với điều phối, ta đứng ở Đ, đếm 5 tin gửi đi và 5 tin nhận về, ra 10, khớp.':
        'ASR chép “Với điều phối, ta đứng ở đây, đếm 5 tin gửi đi và 5 tin nhận về, ra 10 khớp.” (0.95): lệch âm/thanh thuần Việt: đ/đây — NOT_VERIFIED bằng tai người',
    # ── Đợt A đào sâu: BCH ──
    'Còn dấu gạch đứng nghĩa là nối hai chuỗi với một vạch ngăn ở giữa, ví dụ a b nối c d thành a b, vạch, c d.':
        'ASR chép “Còn dấu gạt đứng nghĩa là nối hai chuỗi với một vạc ngăn ở giữa, ví dụ AB nối CG thành AB, vạc CG.” (0.778): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: gạch/gạt, vạch/vạc, vạch (trong “vạch c d” → “vạc cg”) — NOT_VERIFIED bằng tai người',
    'Ta viết lôgarit cơ số 2 của 1024 bằng 10, nghĩa là số lần chia đôi để về 1.':
        'ASR chép “Ta viết logatic cơ số 2 của 1024 bằng 10, nghĩa là số lần chia đôi để về một.” (0.96): lệch âm/thanh thuần Việt: lôgarit/logatic — NOT_VERIFIED bằng tai người',
    'Ở bài 1, mã băm dài 256 bit, đổi một ký tự là mã đổi hoàn toàn, và 256 bit chia 8 là 32 byte mỗi mã.':
        'ASR chép “Ở bài 1, mã băm dài 256 bit, đổi một ký tự là mã đổi hoàn toàn và 256 bit chia 8 là 32 bài mỗi mã.” (0.973): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Ba ô màu cam là toàn bộ bằng chứng, đúng bằng lôgarit cơ số 2 của 8, bằng 3 mã.':
        'ASR chép “Ba ô màu cam là toàn bộ bằng chứng, đúng bằng Logatrix cơ số 2 của 8, bằng ba mã.” (0.95): lệch âm/thanh thuần Việt: lôgarit/logatrix — NOT_VERIFIED bằng tai người',
    'Còn nếu tải chỉ riêng 1024 mã lá thôi, chưa kể giao dịch, đã là 1024 nhân 32, bằng 32768 byte, gấp 102 phẩy 4 lần bằng chứng.':
        'ASR chép “Còn nếu tại chỉ riêng 1024 mã lá thôi, chưa kể giao dịch, đã là 1024 nhân 32 bằng 32.768 bai, gấp 102.4 lần bằng chứng.” (0.952): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; lệch âm/thanh thuần Việt: tải/tại — NOT_VERIFIED bằng tai người',
    'Ta lấy n bằng 61 nhân 53, bằng 3233, khoá công khai e bằng 17, và khoá bí mật d bằng 2753.':
        'ASR chép “Ta lấy N bằng 61 nhân 53, bằng 3233, khóa công khai E bằng 17 và khóa bí mật G bằng 2753.” (0.974): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Bước hai, người kiểm tính s mũ 17 chia lấy dư cho 3233.':
        'ASR chép “Bước 2 Người kiểm tính F mũ 17 chia lấy dư cho 3.233” (0.95): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Mỗi bit đầu bằng 0 với xác suất một phần hai, 16 bit liền nhau thì nhân 16 lần, nên p bằng 2 mũ âm 16, tức 1 phần 65536.':
        'ASR chép “Mỗi biết đầu bằng không với xác suốt 1 phần 2, 16 biết liền nhau thì nhân 16 lần, nên tề bằng 2 mũ âm 16, tức 1 phần 65.536.” (0.902): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: bit/biết, suất/suốt, bit/biết — NOT_VERIFIED bằng tai người',
    'Cứ thế, sau lần rút thứ k thì kho còn 10 trừ k.':
        'ASR chép “Cứ thế, sau lần trúc thứ ca thì khó còn 10 trứ ca.” (0.769): lệch âm/thanh thuần Việt: rút/trúc, kho/khó, trừ/trứ — NOT_VERIFIED bằng tai người',
    'Trong bài này, 1 MB là 10 mũ 6, tức một triệu byte.':
        'ASR chép “Trong bài này, một megabyte là mười mũ sáu, tức một triệu byte.” (0.923): MB đọc “mê-ga-byte” theo lexicon của khoá, ASR viết “MB/megabyte” — NOT_VERIFIED bằng tai người',
    'Và mỗi byte gồm 8 bit, điều này dùng khi tính thời gian truyền qua mạng.':
        'ASR chép “Và mỗi bay gồm 8 bit, điều này dùng khi tính thời gian truyền qua mạng.” (0.938): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Bên phải, hàng nghìn giao dịch chạy ngoài chuỗi được nén lại, mỗi giao dịch chỉ còn vài byte, và cả lô nằm gọn trong một khối.':
        'ASR chép “Bên phải, hàng nghìn giao dịch chạy ngoài chuỗi được nén lại, mỗi giao dịch chỉ còn vài bay và cả lô nằm gọn trong một khối.” (0.963): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Một khối có một triệu byte, mỗi giao dịch 250 byte, nên một khối chứa 10 mũ 6 chia 250, bằng 4000 giao dịch.':
        'ASR chép “Một khối có 1 triệu bai, mỗi giao dịch 250 bai, nên 1 khối chứa 10 mũ 6 chia 250 bằng 4 ngàn giao dịch.” (0.935): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Bước bốn, với gộp giao dịch, mỗi giao dịch chỉ còn 12 byte trên chuỗi.':
        'ASR chép “Bước 4, với gột giao dịch. Mỗi giao dịch chỉ còn 12 bay trên chuỗi.” (0.875): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: gộp/gột — NOT_VERIFIED bằng tai người',
    'Kiểm thêm tỉ lệ, vì kích thước khối và thời gian giữa hai khối không đổi, chỉ cỡ giao dịch đổi từ 250 xuống 12 byte.':
        'ASR chép “Kiểm thêm tỷ lệ vì kích thước khối và thời gian giữa hai khối không đổi, chỉ cỡ giao dịch đổi từ 250 xuống 12 bay.” (0.933): “tỉ” ASR viết chính tả “tỷ” (cùng âm); byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    # ── Đợt A đào sâu: ESY ──
    'Một ki-lô-byte là 1024 byte, nên 2 ki-lô-byte là 2048 byte.':
        'ASR chép “1 kg bài là 1.024 bài, nên 2 kg bài là 2.048 bài.” (0.731): KB đọc “ki-lô-byte” theo lexicon của khoá, ASR viết “kilobyte/kg”; byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Một gi-ga-byte là 2 mũ 30 byte, khoảng một tỉ byte.':
        'ASR chép “Một gigabyte là hai mũ ba mươi bay, khoảng một tỷ bay.” (0.615): GB đọc “ghi-ga-byte” theo lexicon của khoá, ASR viết “GB/gigabyte”; byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); “tỉ” ASR viết chính tả “tỷ” (cùng âm); lệch âm/thanh thuần Việt: gi (trong “gi ga byte” → “gigabyte”) — NOT_VERIFIED bằng tai người',
    'Chia 16 gi-ga-byte cho 2 ki-lô-byte, ta được 2 mũ 23, tức là 8 triệu 388 nghìn 608 lần.':
        'ASR chép “Chia 16 GB cho 2 KB, ta được 2 mũ 23, tức là 8.388.608 lần.” (0.871): GB đọc “ghi-ga-byte” theo lexicon của khoá, ASR viết “GB/gigabyte”; KB đọc “ki-lô-byte” theo lexicon của khoá, ASR viết “kilobyte/kg”; lệch âm/thanh thuần Việt: gi (trong “gi ga byte” → “gb”) — NOT_VERIFIED bằng tai người',
    'Hạn 10 mi li giây lớn gấp khoảng 7 phẩy 8 lần con số trung bình này.':
        'ASR chép “hàng 10 mili dây lớn gấp khoảng 7,8 lần con số trung bình này.” (0.788): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; lệch âm/thanh thuần Việt: hạn/hàng — NOT_VERIFIED bằng tai người',
    'Nhưng lần xấu nhất 12 mi li giây vượt hạn 10 tới 2 mi li giây, nên tác vụ A không kịp hạn.':
        'ASR chép “Nhưng lần xấu nhất 12 mili dây vượt hạng 10 tới 2 mili dây, nền tác vụ A không kịp hạng.” (0.652): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; lệch âm/thanh thuần Việt: hạn/hạng, nên (trong “mi li giây nên” → “mili dây nền”), hạn/hạng — NOT_VERIFIED bằng tai người',
    'Một byte gồm 8 bit, viết gọn bằng hai chữ số hệ mười sáu, chẳng hạn F F bằng 15 nhân 16 cộng 15, tức là 255.':
        'ASR chép “Một bay gồm 8 bit, viết gọn bằng hai chữ số hệ 16, chẳng hạn FF bằng 15 nhân 16 cộng 15, tức là 255.” (0.971): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Một số 16 bit gồm hai byte, giá trị bằng byte cao nhân 256 rồi cộng byte thấp.':
        'ASR chép “Một số 16 biết gồm hai bay, giá trị bằng bay cao nhân 256 rồi cộng bay thấp.” (0.826): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: bit/biết — NOT_VERIFIED bằng tai người',
    'Số 255 có byte cao 00 và byte thấp F F.':
        'ASR chép “Số 255 có bài cao 00 và bài thấp FF.” (0.867): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Số 256 có byte cao 01 và byte thấp 00.':
        'ASR chép “số 256 có bài cao 01 và bài thấp 00.” (0.857): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Số 511 có byte cao 01 và byte thấp F F, vì 256 cộng 255 bằng 511.':
        'ASR chép “Số 511 có bai cao 01 và bai thấp FF vì 256 cộng 255 bằng 511.” (0.935): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Tiếp theo là phép làm tròn lên, ví dụ cần phủ kín 7 mi li giây bằng các khoảng dài 2 mi li giây.':
        'ASR chép “Tiếp theo là phép làm tròn lên, ví dụ cần phụ kính 7 mili giây bằng các khoảng dài 2 mili giây.” (0.783): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; lệch âm/thanh thuần Việt: phủ kín/phụ kính — NOT_VERIFIED bằng tai người',
    'Vòng chính đọc byte thấp trước, lúc đó bộ nhớ đang là 255 nên byte thấp là F F.':
        'ASR chép “Vòng chính độc bai thấp trước, lúc đó bộ nhớ đang là 255 nên bai thấp là FF.” (0.87): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: đọc (trong “đọc byte” → “độc bai”) — NOT_VERIFIED bằng tai người',
    'Quay lại vòng chính, ta đọc byte cao của số mới là 01, ghép với F F cũ thành 511, một số chưa từng nằm trong bộ nhớ.':
        'ASR chép “Quay lại vòng 9, ta đọc bay cao của số mới là 01, gép với FF củ thành 511, một số chưa từng nằm trong bộ nhớ.” (0.871): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: chính/chín, ghép/gép, cũ/củ — NOT_VERIFIED bằng tai người',
    'Năm mẫu cách nhau 1 mi li giây phủ kín 5 mi li giây dội, nên khi đủ 5 mẫu giống nhau thì phím chắc chắn đã hết nảy.':
        'ASR chép “5 mẫu cách nhau 1 mili dây phủ kiếm 5 mili dây dội, nên khi đủ 5 mẫu giống nhau thì phím chắc chắn đã hết nảy.” (0.786): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; lệch âm/thanh thuần Việt: kín/kiếm — NOT_VERIFIED bằng tai người',
    'Kiểm từng lần đọc như trong hình, lần đầu biến đang là 511 nên byte thấp đọc được F F.':
        'ASR chép “Kiếm từng lần độc như trong hình, lần đầu biến đang là 511 nên bay thấp độc được FF.” (0.826): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: kiểm/kiếm, đọc/độc, đọc/độc — NOT_VERIFIED bằng tai người',
    'Ngắt chen vào tăng biến lên 512, viết là 02 00, nên lần sau byte cao đọc được 02.':
        'ASR chép “Ngắt chen vào tăng biến lên 512, viết là 0200, nên lần sau bay cao độc được 02.” (0.864): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: không/trăm, đọc/độc — NOT_VERIFIED bằng tai người',
    'Bước một, đầu vào nhảy từ 0 lên 1, y bắt đầu từ 0.':
        'ASR chép “Bước 1, đầu vào nhảy từ không lên 1 thì bắt đầu từ không.” (0.929): lệch âm/thanh thuần Việt: i/thì — NOT_VERIFIED bằng tai người',
    'Đáp án câu một, với a bằng 0 phẩy 5 thì khoảng còn lại mỗi mẫu nhân 0 phẩy 5, nên y đi 0 phẩy 5, 0 phẩy 75, rồi 0 phẩy 875.':
        'ASR chép “Đáp án câu 1 với A bằng 0,5 thì khoảng còn lại mỗi mẫu nhân 0,5 nên ED 0,5, 0,75 rồi 0,875.” (0.933): “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; lệch âm/thanh thuần Việt: i đi/ed, không (trong “không phẩy” → “”) — NOT_VERIFIED bằng tai người',
    'Chữ số 4 là 0 1 0 0.':
        'ASR chép “Chữ số 4 là 0100.” (0.714): lệch âm/thanh thuần Việt: không/∅, không không/trăm — NOT_VERIFIED bằng tai người',
    'Hàng chấm đỏ lệch 6 phần trăm, mẫu cuối rơi ra ngoài khung, nên bên nhận đọc sai bit dừng.':
        'ASR chép “Hàng chấm đỏ lịch 6% mẫu cuối trơi ra ngoài khung nên bên nhận độc sai bít dưng.” (0.75): lệch âm/thanh thuần Việt: lệch/lịch, rơi/trơi, đọc/độc, bit dừng/bít dưng — NOT_VERIFIED bằng tai người',
    'Bảng cho thấy mỗi byte mất khoảng 1 phẩy 042 mi li giây, tức khoảng 16 nghìn 667 nhịp đồng hồ chỉ để đứng chờ.':
        'ASR chép “Bản cho thấy mỗi bay mất khoảng 1,0420 lý dây, tức khoảng 16,667 nhịp đồng hồ chỉ để đứng chờ.” (0.812): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; lệch âm/thanh thuần Việt: bảng/bản, hai (trong “hai mi li giây” → “lý dây”) — NOT_VERIFIED bằng tai người',
    'Câu ba, xung nhịp vẫn là 16 mê-ga-héc, và hệ cần gửi ít nhất 3000 byte mỗi giây.':
        'ASR chép “Câu Ba, xung nhịp vẫn là 16 MHz và hãy cần gửi ít nhất 3.000 bai mỗi giây.” (0.81): “mê-ga-…” đọc tách âm tiết (đã dựng ở NET), ASR viết dạng gộp; byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: héc (trong “mê ga héc” → “mhz”), hệ/hãy — NOT_VERIFIED bằng tai người',
    'Với vế sau, 100 byte nhân 10 bit là 1000 bit, chia cho 9600 bit mỗi giây.':
        'ASR chép “Với với sau, 103 nhân 10 bit là 1000 bit, chia cho 9600 bit mỗi giây.” (0.889): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: vế/với — NOT_VERIFIED bằng tai người',
    'Câu ba, tốc độ ba mươi tám nghìn bốn trăm chia 10 được 3840 byte mỗi giây, đã đủ hơn 3000, lại chỉ lệch 0 phẩy 16 phần trăm.':
        'ASR chép “Câu 3, tốc độ 38.410 được 3.843 mỗi giây đã đủ hơn 3.000, lại chỉ lệch 0,16%.” (0.958): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: chia/∅ — NOT_VERIFIED bằng tai người',
    'Lần đọc thanh ghi ở trên gồm 5 byte, nên tốn 5 nhân 9, bằng 45 nhịp.':
        'ASR chép “Lần độc Thanh Ghi ở trên gồm Năm Bai, nền Tốn Năm Nhân Chính bằng 45 Nhịp.” (0.789): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: đọc/độc, nên (trong “byte nên” → “bai nền”), chín/chính — NOT_VERIFIED bằng tai người',
    'Hình vẽ điện áp trên dây dữ liệu khi chip thả dây ra, dây có điện dung 200 pi-cô-pha-ra.':
        'ASR chép “Hình vẽ điện áp trên dây dữ liệu khi chiếp thả dây ra, dày có điện dung 200 picofarad.” (0.791): pi (π) ASR viết “P/π”; lệch âm/thanh thuần Việt: chip/chiếp, dây/dày, cô pha ra (trong “pi cô pha ra” → “picofarad”) — NOT_VERIFIED bằng tai người',
    '1 ki-lô-ôm cho thời gian lên 169 na-nô giây và dòng điện 2 phẩy 9 mi-li-am-pe, đều đạt nhưng sát biên dòng.':
        'ASR chép “Một kilo ôm cho thời gian lên 169 nanoj và dòng điện 2,9 mA, đều đạt nhân sát biên dòng.” (0.759): “ki-lô-byte” đọc tách âm tiết, ASR viết “kg” rồi chép “byte” thành “bay/ba”; tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; lệch âm/thanh thuần Việt: am pe (trong “mi li am pe” → “ma”), nhưng/nhân — NOT_VERIFIED bằng tai người',
    '1 phẩy 5 ki-lô-ôm cho 254 na-nô giây và 1 phẩy 93 mi-li-am-pe, xa cả hai biên.':
        'ASR chép “1,5 kOhm cho 254 nano dây và 1,93 mA, xa cả hai biên.” (0.731): “ki-lô-byte” đọc tách âm tiết, ASR viết “kg” rồi chép “byte” thành “bay/ba”; tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; lệch âm/thanh thuần Việt: ôm (trong “ki lô ôm” → “kohm”), am pe (trong “mi li am pe” → “ma”) — NOT_VERIFIED bằng tai người',
    '1 phẩy 8 ki-lô-ôm đã cho 305 na-nô giây, vượt giới hạn 300.':
        'ASR chép “1,8 kOhm đã cho 300 Linh 5-nano dây, vượt giới hạn 300.” (0.757): “ki-lô-byte” đọc tách âm tiết, ASR viết “kg” rồi chép “byte” thành “bay/ba”; tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; lệch âm/thanh thuần Việt: ôm (trong “ki lô ôm” → “kohm”) — NOT_VERIFIED bằng tai người',
    'Ta chọn trong khoảng 1 tới 1 phẩy 7 ki-lô-ôm, ví dụ 1 phẩy 5 ki-lô-ôm.':
        'ASR chép “Ta chọn trong khoảng 1 tới 1,7 kg, ví dụ 1,5 kg.” (0.778): “ki-lô-byte” đọc tách âm tiết, ASR viết “kg” rồi chép “byte” thành “bay/ba”; lệch âm/thanh thuần Việt: ôm (trong “ki lô ôm” → “kg”), ôm (trong “ki lô ôm” → “kg”) — NOT_VERIFIED bằng tai người',
    'Với 1 phẩy 5 ki-lô-ôm và 200 pi-cô-pha-ra, điện áp chạm 30 phần trăm ở khoảng 107 na-nô giây.':
        'ASR chép “với 1,5 kg và 200 picofada, điện áp chạm 30% ở khoảng 107 nanoj.” (0.755): “ki-lô-byte” đọc tách âm tiết, ASR viết “kg” rồi chép “byte” thành “bay/ba”; pi (π) ASR viết “P/π”; tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; lệch âm/thanh thuần Việt: ôm (trong “ki lô ôm” → “kg”), cô pha ra (trong “pi cô pha ra” → “picofada”) — NOT_VERIFIED bằng tai người',
    'Bảng tính sẵn, 10 ki-lô-ôm cho thời gian lên 1695 na-nô giây, vượt cả hai giới hạn 300 và 1000 na-nô giây.':
        'ASR chép “Bản tính sẵn 10kg cho thời gian lên 1.695 nanoj, vượt cả hai giới hạn 300 và 1.000 nanoj.” (0.774): “ki-lô-byte” đọc tách âm tiết, ASR viết “kg” rồi chép “byte” thành “bay/ba”; tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; lệch âm/thanh thuần Việt: bảng/bản, ôm (trong “ki lô ôm” → “kg”) — NOT_VERIFIED bằng tai người',
    'Câu ba, vẫn dây 100 pi-cô-pha-ra và nguồn 3 phẩy 3 vôn, nên chọn 1 ki-lô-ôm, 2 phẩy 2 ki-lô-ôm, hay 4 phẩy 7 ki-lô-ôm?':
        'ASR chép “Câu ba, vẫn dây 100 pico fada và nguồn 3,3 vôn nên chọn 1 kg, 2,2 kg, hay 4,7 kg ống.” (0.698): pi (π) ASR viết “P/π”; “ki-lô-byte” đọc tách âm tiết, ASR viết “kg” rồi chép “byte” thành “bay/ba”; lệch âm/thanh thuần Việt: cô pha ra (trong “pi cô pha ra” → “pico fada”), ôm (trong “ki lô ôm” → “kg”), ôm (trong “ki lô ôm” → “kg”), ôm (trong “ki lô ôm” → “kg ống”) — NOT_VERIFIED bằng tai người',
    '1 ki-lô-ôm nằm trong khoảng nhưng dòng điện 2 phẩy 9 mi-li-am-pe, sát biên 3 mi-li-am-pe.':
        'ASR chép “1 kg ôm nằm trong khoảng nhân dòng điện 2,9 mA, sát biên 3 mA.” (0.634): “ki-lô-byte” đọc tách âm tiết, ASR viết “kg” rồi chép “byte” thành “bay/ba”; tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; lệch âm/thanh thuần Việt: nhưng/nhân, am pe (trong “mi li am pe” → “ma”), am pe (trong “mi li am pe” → “ma”) — NOT_VERIFIED bằng tai người',
    'A có chu kỳ 4 nên ưu tiên cao nhất, tỉ lệ 0 phẩy 25.':
        'ASR chép “À có chu kỳ 4 nền ưu tiên cao nhất, tỷ lệ 0,25.” (0.824): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; “tỉ” ASR viết chính tả “tỷ” (cùng âm); lệch âm/thanh thuần Việt: nên/nền — NOT_VERIFIED bằng tai người',
    'Kiểm bằng đường khác, vì đọc bảng quyết định có thể sót một dòng.':
        'ASR chép “Kiểm bằng đường khác vì độc bản quyết định có thể sóc một dòng.” (0.786): lệch âm/thanh thuần Việt: đọc bảng/độc bản, sót/sóc — NOT_VERIFIED bằng tai người',
    'Trước hết, nhắc lại khung truyền nối tiếp ở bài 7, mỗi byte được gói trong một khung.':
        'ASR chép “Trước hết, nhắc lại khung truyền nối tiếp ở bài bảy, mỗi bài được gói trong một khung.” (0.944): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Cộng lại là 10 bit cho mỗi byte.':
        'ASR chép “Cộng lại là 10 bích cho mỗi bay.” (0.75): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: bit/bích — NOT_VERIFIED bằng tai người',
    'Trong 20 mi li giây, tức 0 phẩy 02 giây, đến 960 nhân 0 phẩy 02, bằng 19 phẩy 2 byte.':
        'ASR chép “trong 20 ms tức 0,02 giây đến 960 nhân 0,02 bằng 19,23.” (0.863): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Vì sao không lấy 19, vì mỗi chỗ trong hàng đợi chứa trọn một byte, nên phần 0 phẩy 2 nghĩa là có lúc byte thứ 20 đã tới, không có chỗ thì byte đó bị mất.':
        'ASR chép “Vì sao không lấy 19, vì mỗi chỗ trong hàng đời chứa trọn một bay, nên phần không phải hay nghĩa là có lúc bay thứ 20 đã tới, không có chỗ thì bay đó bị mất.” (0.846): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; lệch âm/thanh thuần Việt: đợi/đời, hai (trong “phẩy hai” → “phải hay”) — NOT_VERIFIED bằng tai người',
    'Khi một byte đến, phần cứng báo ngắt, và việc vẽ tạm dừng.':
        'ASR chép “Khi một bay đến, phần cứng báo ngắt và việc vẽ tạm dừng.” (0.923): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Hình vẽ đường đi của một byte, từ lúc tới cổng cho tới lúc được giải mã.':
        'ASR chép “Hình vẽ đường đi của một bay từ lúc tới cổng cho tới lúc được giải mã.” (0.941): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Byte đến cổng nối tiếp thì hàm xử lý ngắt chạy ngay, việc duy nhất của nó là đẩy byte vào hàng đợi, ở đây đang có 5 byte chờ.':
        'ASR chép “Bay đến cổng nối tiếp thì hàm xử lý ngắt chạy ngay. Việc duy nhất của nó là đẩy bay vào hàng đợi. Ở đây đang có 5 bay chờ.” (0.9): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Tác vụ giải mã lấy từng byte ra theo nhịp của nó, còn tác vụ vẽ màn hình có ưu tiên thấp hơn, nên dù vẽ lâu cũng không làm mất byte nào.':
        'ASR chép “Tác vụ giải mã lấy từng bay ra theo nhiệt của nó, còn tác vụ vẽ màn hình có ưu tiên thấp hơn, nên dù vẽ lâu cũng không làm mất bay nào.” (0.909): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: nhịp/nhiệt — NOT_VERIFIED bằng tai người',
    'Nhưng nếu chính tác vụ giải mã bị một tác vụ ưu tiên cao hơn giữ lại thì sao, hình vẽ số byte chờ theo thời gian bị giữ.':
        'ASR chép “Nhưng nếu 9 tác vụ giải mã bị một tác vụ ưu tiên cao hơn giữ lại thì sao, hình vẽ số bay chờ theo thời gian bị giữ.” (0.931): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: chính/chín — NOT_VERIFIED bằng tai người',
    'Byte vẫn đến đều, mỗi mi li giây khoảng 11 phẩy 52 byte, nên đường xanh đi lên thẳng, tới 10 mi li giây là 115 phẩy 2 byte.':
        'ASR chép “Bai vẫn đến đều mỗi mili dây khoảng 11,52 bai, nên đường xanh đi lên thẳng tới 10 mili dây là 115,2 bai.” (0.765): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh — NOT_VERIFIED bằng tai người',
    'Hàng đợi 64 chỗ đã đầy lúc khoảng 5 phẩy 6 mi li giây, từ đó mọi byte đến đều bị mất.':
        'ASR chép “Hàng đời 64 chỗ đã đầy lúc khoảng 5,6 mili giây, từ đó mọi bay đến đều bị mất.” (0.851): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: đợi/đời — NOT_VERIFIED bằng tai người',
    'Bước một, tính tốc độ đến, cổng nối tiếp chạy một trăm mười lăm nghìn hai trăm bit mỗi giây, khung 8N1, mỗi byte tốn 10 bit.':
        'ASR chép “Bước 1, tính tốc độ đến, cộng nối tiếp chạy 115,200 bit mỗi giây, khung 8N1, mỗi bay tốn 10 bit.” (0.931): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: cổng/cộng — NOT_VERIFIED bằng tai người',
    'Bước ba, làm tròn lên vì mỗi chỗ chứa trọn một byte, nên hàng đợi cần ít nhất 116 chỗ.':
        'ASR chép “Bước 3, làm tròn lên vì mỗi chỗ chứa trọn một bay, nên hàng đợi cần ít nhất 116 chỗ.” (0.957): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Nếu chỉ có 115 chỗ, sẽ có lúc byte thứ 116 tới mà không còn chỗ để cất.':
        'ASR chép “Nếu chỉ có 115 chỗ, sẽ có lúc bay thứ 116 tới mà không còn chỗ để cất.” (0.958): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Lấy đúng 116 thì không có chỗ dư nào, và tốn khoảng 5 phẩy 7 phần trăm bộ nhớ của một vi điều khiển 2 ki-lô-byte.':
        'ASR chép “Lấy đúng 116 thì không có chỗ dư nào và tốn khoảng 5,7% bộ nhớ của một vi điều khiển 2 kilobyte.” (0.933): KB đọc “ki-lô-byte” theo lexicon của khoá, ASR viết “kilobyte/kg” — NOT_VERIFIED bằng tai người',
    'Vì vậy chọn 128, đổi 12 byte bộ nhớ lấy một khoảng dư cho sai số khi đo thời gian bị giữ.':
        'ASR chép “Vì vậy, chọn 128, đổi 12 bai bộ nhớ lấy 1 khoảng dư cho sai số khi đo thời gian bị giữ.” (0.963): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Thay vì nhân tốc độ với thời gian, ta hỏi ngược lại, hàng đợi đầy sau bao lâu, biết mỗi byte cách nhau khoảng 86 phẩy 8 phần triệu giây.':
        'ASR chép “Thay vì nhân tốc độ với thời gian, ta hỏi ngược lại, hàng đợi đầy sao bao lâu, biết mỗi bay cách nhau khoảng 86,8 phần triệu giây.” (0.938): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: sau/sao — NOT_VERIFIED bằng tai người',
    'Hàng đợi 115 chỗ đầy sau khoảng 9 phẩy 98 mi li giây, trước khi tác vụ giải mã được chạy lại, nên mất byte.':
        'ASR chép “Hàng đợi 115 chỗ đầy sau khoảng 9,98 mili giây trước khi tác vụ giải mã được chạy lại nên mất bay.” (0.915): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Kết quả là 51 byte bị mất trong một lần tác vụ bị giữ, và lệnh nhận được bị cắt cụt.':
        'ASR chép “Kết quả là 51 bai bị mất trong một lần tác vụ bị giữ và lệnh nhận được bị cắt cục.” (0.913): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: cụt/cục — NOT_VERIFIED bằng tai người',
    'Câu ba là một quyết định, hàng đợi 16 chỗ đầy sau 16 chia 960 giây, khoảng 16 phẩy 7 mi li giây, sớm hơn 20 mi li giây bị giữ, nên sẽ mất byte.':
        'ASR chép “Câu 3 là một quyết định, hàng đợi 16 chỗ đầy sau 16 chia 960 giây, khoảng 16,7 mili giây, sớm hơn 20 mili giây bị giữ, nên sẽ mất bay.” (0.902): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Vì vậy không duyệt, cần ít nhất 20 chỗ, mà 4 chỗ thêm chỉ tốn đúng 4 byte bộ nhớ.':
        'ASR chép “Vì vậy không duyệt, cần ít nhất 20 chỗ mà 4 chỗ thêm chỉ tốn đúng 4 bài bộ nhớ.” (0.952): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Hàm chính có khung 10 byte gọi hàm f có khung 20 byte, ngăn xếp đang giữ 30 byte.':
        'ASR chép “Hàm 9 có khung 10 bay gọi hàm F có khung 20 bay, ngàn xếp đang giữ 30 bay.” (0.762): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: chính/chín, ngăn (trong “byte ngăn” → “bay nghìn”) — NOT_VERIFIED bằng tai người',
    'Hàm f gọi tiếp hàm g có khung 30 byte, ngăn xếp lên tới 60 byte, đây là lúc sâu nhất.':
        'ASR chép “Hàm F gọi tiếp hàm V có khung 30b, ngàn xếp lên tới 60b, đây là lúc sâu nhất.” (0.826): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: ngăn (trong “byte ngăn” → “b nghìn”) — NOT_VERIFIED bằng tai người',
    'Khi g trả về, khung của nó được gỡ ra, ngăn xếp lại còn 30 byte.':
        'ASR chép “Khi Giê trả về, khung của nó được gỡ ra ngăn xếp lại còn 30 bay.” (0.941): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Một bộ đếm lùi được nạp 100 và mỗi mi li giây trừ đi 1, nên sau 60 mi li giây nó còn 40, sau 100 mi li giây thì về 0.':
        'ASR chép “Một bộ đếm lùi được nạp 100 và mỗi mili dây trừ đi 1, nên sau 60 mili dây nó còn 40, sau 100 mili dây thì về không?” (0.783): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh — NOT_VERIFIED bằng tai người',
    'Vạch đỏ là 310 sau khi nhân biên, còn khung đứt nét là 320 byte ta thực sự cấp.':
        'ASR chép “Vạch đỏ là 310 sau khi nhân biên, còn khung đức nét là 320 baita thực sự cấp.” (0.894): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: đứt/đức, ta (trong “byte ta” → “baita”) — NOT_VERIFIED bằng tai người',
    'Bước một, cộng ba khung của chuỗi gọi này, được 208 byte.':
        'ASR chép “Bước 1, cộng 3 khung của chuỗi gọi này được 208 bay.” (0.933): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Ví dụ còn 72 byte trên cùng giữ nguyên mẫu, nghĩa là đã dùng 320 trừ 72, bằng 248 byte, khớp với ước lượng.':
        'ASR chép “Ví dụ còn 72 bai trên cùng giữ nguyên mẫu, nghĩa là đã dùng 320-72 bằng 248 bai, khớp với ước lượng.” (0.928): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: trừ/∅ — NOT_VERIFIED bằng tai người',
    'Ngắt đến khi đang ở hàm chính thì ngăn xếp là 104 byte.':
        'ASR chép “Ngắt đến khi đang ở hàm chính thì ngăn xét là 104 bay.” (0.875): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: xếp/xét — NOT_VERIFIED bằng tai người',
    'Đến khi đang ở hàm đọc cảm biến thì là 152 byte.':
        'ASR chép “Đến khi đang ở Hàm Đọc Cảm biến thì là 152 bay.” (0.938): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Đến khi đang ở hàm lọc thì là 248 byte, lớn nhất trong ba trường hợp, khớp với cách tính ở trên.':
        'ASR chép “Đến khi đang ở Hàm Lộc thì là 248 bài, lớn nhất trong 3 trường hợp, khớp với các tính ở trên.” (0.885): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: lọc/lộc, cách/các — NOT_VERIFIED bằng tai người',
    'Với ví dụ của bài, quên ngắt chỉ được 208, nhân biên ra 260 byte, thấp hơn mức thật cần là 310.':
        'ASR chép “Với ví dụ của bài, quen ngắt chỉ được 208, nhận biên ra 260 bài, thấp hơn mức thật cần là 310.” (0.9): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: quên/quen, nhân/nhận — NOT_VERIFIED bằng tai người',
    'Pin một nghìn mi-li-am-pe giờ khi thiết bị tiêu thụ 10 mi-li-am-pe thì dùng được một nghìn chia 10, bằng 100 giờ, khoảng 4 phẩy 2 ngày.':
        'ASR chép “Pin 1000 mAh khi thiết bị tiêu thủ 10 mA thì dùng được 1000 chi 10 bằng 100 giờ khoảng 4,2 ngày.” (0.754): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; lệch âm/thanh thuần Việt: am pe giờ (trong “mi li am pe giờ” → “mah”), thụ/thủ, am pe (trong “mi li am pe” → “ma”), chia/chi — NOT_VERIFIED bằng tai người',
    'Dòng trung bình là 10 chia 10, bằng 1 mi-li-am-pe, giống hệt 0 phẩy 1 nhân 10, tức tỉ lệ thời gian nhân dòng điện.':
        'ASR chép “Vòng trung bình là 10 chia 10 bằng 1 mA, giống hệt 0,1 nhân 10, tức tỷ lệ thời gian nhân vòng điện.” (0.792): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; “tỉ” ASR viết chính tả “tỷ” (cùng âm); lệch âm/thanh thuần Việt: dòng/vòng, am pe (trong “mi li am pe” → “ma”), dòng/vòng — NOT_VERIFIED bằng tai người',
    'Hình chia dòng trung bình thành hai phần, phần xanh do lúc thức ở 10 mi-li-am-pe, phần cam do lúc ngủ ở 10 mi-crô-am-pe.':
        'ASR chép “Hình chia dòng trung bình thành hai phần, phần xanh do lúc thức ở 10 mA, phần cam do lúc ngủ ở 10 µA.” (0.815): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; lệch âm/thanh thuần Việt: am pe (trong “mi li am pe” → “ma”), am pe (trong “mi crô am pe” → “µa”) — NOT_VERIFIED bằng tai người',
    'Dòng trung bình còn 0 phẩy 0599 mi-li-am-pe.':
        'ASR chép “Dòng trung bình còn 0.0599mA.” (0.769): “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; lệch âm/thanh thuần Việt: am pe (trong “mi li am pe” → “ma”) — NOT_VERIFIED bằng tai người',
    'Khi thức rất ít, dòng ngủ mới là thứ quyết định, và 10 mi-crô-am-pe lúc này là phần lớn nhất.':
        'ASR chép “Khi thức rất ít, dòng ngủ mới là thứ quyết định và 10 µA lúc này là phần lớn nhất.” (0.884): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; lệch âm/thanh thuần Việt: am pe (trong “mi crô am pe” → “µa”) — NOT_VERIFIED bằng tai người',
    'Câu ba, nếu chỉ được sửa một thứ, giảm dòng thức còn 10 mi-li-am-pe hay giảm dòng ngủ còn 2 phẩy 5 mi-crô-am-pe, bạn chọn cách nào?':
        'ASR chép “Câu ba, nếu chỉ được sửa một thứ, giảm dòng thức còn 10mA hay giảm dòng ngủ còn 2,5mA, bạn chọn cách nào?” (0.833): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; lệch âm/thanh thuần Việt: am pe (trong “mi li am pe” → “ma”), am pe (trong “mi crô am pe” → “ma”) — NOT_VERIFIED bằng tai người',
    'Hình vẽ bộ nhớ chương trình 1024 ki-lô-byte như một dải dài, bộ nạp nhỏ ở đầu, rồi hai ngăn bằng nhau là phân vùng A và phân vùng B, phần còn lại để trống.':
        'ASR chép “Hình vẽ bộ nhớ chương trình 1024 kilobytes như một dải dài, bộ nạp nhỏ ở đầu, rồi hai ngăn bằng nhau là phân vùng A và phân vùng B, phần còn lại để trống.” (0.952): KB đọc “ki-lô-byte” theo lexicon của khoá, ASR viết “kilobyte/kg” — NOT_VERIFIED bằng tai người',
    'Bước một là bước chia bộ nhớ, và còn dư 192 ki-lô-byte.':
        'ASR chép “Bước 1 là bước chia bộ nhớ và còn dư 192 kilobyte.” (0.882): KB đọc “ki-lô-byte” theo lexicon của khoá, ASR viết “kilobyte/kg” — NOT_VERIFIED bằng tai người',
    'Tải 400 ki-lô-byte qua cổng nối tiếp tốc độ 115 nghìn 200 bit mỗi giây, tức khoảng 11 nghìn 520 byte mỗi giây, mất khoảng 35 phẩy 6 giây.':
        'ASR chép “Tại 400 kilobytes qua cổng nối tiếp tốc độ 115,200 bit mỗi giây, tức khoảng 11.520 bit mỗi giây, mất khoảng 35,6 giây.” (0.902): KB đọc “ki-lô-byte” theo lexicon của khoá, ASR viết “kilobyte/kg”; byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: tải/tại — NOT_VERIFIED bằng tai người',
    'Câu một, hai phân vùng cần 2 nhân 600, bằng 1200, thêm bộ nạp 64 thành 1264, thiếu 240 ki-lô-byte.':
        'ASR chép “Câu 1, 2 phân vùng cần 2 nhân 600 bằng 1.200 thêm bộ nạp 64 x1.264 thiếu 240 kg.” (0.917): KB đọc “ki-lô-byte” theo lexicon của khoá, ASR viết “kilobyte/kg”; lệch âm/thanh thuần Việt: thành/x — NOT_VERIFIED bằng tai người',
    'Muốn vừa thì mỗi phân vùng chỉ được tối đa 1024 trừ 64, chia đôi, tức là 480 ki-lô-byte.':
        'ASR chép “Muốn vừa thì mỗi phân vùng chỉ được tối đa 1024-64, chia đôi, tức là 480 kilobytes.” (0.918): KB đọc “ki-lô-byte” theo lexicon của khoá, ASR viết “kilobyte/kg”; lệch âm/thanh thuần Việt: trừ/∅ — NOT_VERIFIED bằng tai người',
    # ── Đợt A đào sâu: ESY (cờ THIẾU) ──
    'Chữ số 1 là 0 0 0 1.':
        'ASR chép “Chữ số 1 là 0001.” (0.769): ba chữ số 0 đứng liền được ASR gộp thành một số “0001”, không phải âm thanh cụt — mọi chữ số đều có trong bản chép — NOT_VERIFIED bằng tai người',
    'Tiếp theo, một mi-li-am-pe bằng một nghìn mi-crô-am-pe, nên 10 mi-crô-am-pe là 0 phẩy 01 mi-li-am-pe, còn 100 mi-crô-am-pe là 0 phẩy 1 mi-li-am-pe.':
        'ASR chép “Tiếp theo, 1 mA bằng 1000 µA, nên 10 µA là 0,01 mA, còn 100 µA là 0,1 mA.” (0.559): ASR viết đơn vị đọc tách âm tiết thành ký hiệu mA/µA nên đếm thiếu chữ, không phải âm thanh cụt — mọi số khớp — NOT_VERIFIED bằng tai người',
    # ── Đợt A đào sâu: ROB ──
    'Vòng 10 héc có chu kỳ 1000 chia 10, bằng 100 mi li giây.':
        'ASR chép “Vòng 10 hét có chu kỳ 1000 chia 10 bằng 100 mili dây.” (0.774): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; lệch âm/thanh thuần Việt: héc/hét — NOT_VERIFIED bằng tai người',
    'Vòng 100 héc chỉ còn 10 mi li giây cho mỗi lần lặp.':
        'ASR chép “vàng 100 hếch chỉ còn 10 mili giây cho mỗi lần lập.” (0.667): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; lệch âm/thanh thuần Việt: vòng/vàng, héc/hếch, lặp/lập — NOT_VERIFIED bằng tai người',
    'Đọc cảm biến cộng định vị là 13 mi li giây, thêm 2 và 1 nữa là 16 mi li giây.':
        'ASR chép “Đọc cảm biến cộng định vị là 13ml, thêm 2 và 1 nửa là 16ml.” (0.762): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; lệch âm/thanh thuần Việt: nữa/nửa — NOT_VERIFIED bằng tai người',
    'Đếm trong trọn một giây, có 50 vòng, mỗi vòng bận 16 mi li giây, tổng cộng 800 mi li giây bận.':
        'ASR chép “Đếm trong trọng 1 dây có 50 vòng, mỗi vòng bận 16 mili dây, tổng cộng 800 mili dây bận.” (0.75): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; lệch âm/thanh thuần Việt: trọn/trọng — NOT_VERIFIED bằng tai người',
    'Còn lại 200 mi li giây rảnh, đúng bằng 50 vòng nhân 4 mi li giây dư, khớp với kết quả trước.':
        'ASR chép “Còn lại 200 mili dây trảnh đúng bằng 50 vòng nhân 4 mili dây dư, khớp với kết quả trước.” (0.739): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; lệch âm/thanh thuần Việt: rảnh (trong “mi li giây rảnh” → “mili dây trảnh”) — NOT_VERIFIED bằng tai người',
    'Đi trên đường tròn thì quãng cung bằng bán kính nhân góc tính bằng ra-đi-an, bán kính 2 mét quay 0 phẩy 5 ra-đi-an thì đi được 1 mét.':
        'ASR chép “Đi trên đường tròn thì quảng cung bằng bán kính nhân gốc tính bằng Jadian. Bán kính 2 mét quay không phải 5 Jadian thì đi được 1 m.” (0.742): ra-đi-an: probe RBM p1 8/8, ASR viết “radian/radiant”; “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; đơn vị mét, ASR viết ký hiệu “m”; lệch âm/thanh thuần Việt: quãng/quảng, góc/gốc — NOT_VERIFIED bằng tai người',
    'Khi xe rẽ trái, cả hai bánh cùng quay quanh một tâm với cùng vận tốc góc 0 phẩy 4 ra-đi-an mỗi giây.':
        'ASR chép “Khi xe rẻ trái, cả hai bánh cùng quay quanh mục tâm với cùng vận tốc gốc 0,4 radian mỗi giây.” (0.792): ra-đi-an: probe RBM p1 8/8, ASR viết “radian/radiant”; lệch âm/thanh thuần Việt: rẽ/rẻ, một/mục, góc/gốc — NOT_VERIFIED bằng tai người',
    'Hai vòng cách nhau đúng bằng L, 0 phẩy 5 mét, nên hai bánh chênh nhau ô-mê-ga nhân L, bằng 0 phẩy 2 mét mỗi giây.':
        'ASR chép “2 vòng cách nhau đúng bằng L, không phải 5 mét, nên 2 bánh trên nhau omega nhân L, bằng không phải 2 mét mỗi dây.” (0.815): “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; ô-mê-ga (ω) đọc tách âm tiết, ASR viết “omega/ω”; lệch âm/thanh thuần Việt: chênh/trên — NOT_VERIFIED bằng tai người',
    'Tốc độ bánh trái bằng ô-mê-ga nhân R trừ nửa L, tốc độ bánh phải bằng ô-mê-ga nhân R cộng nửa L.':
        'ASR chép “Tốc độ bánh trái bằng omega nhân r trừ nửa l, tốc độ bánh phải bằng omega nhân r cộng nửa l.” (0.833): ô-mê-ga (ω) đọc tách âm tiết, ASR viết “omega/ω” — NOT_VERIFIED bằng tai người',
    'Lấy hai vế trừ nhau thì phần R triệt tiêu, hiệu hai bánh bằng ô-mê-ga nhân L, chia cho L là ra công thức vận tốc góc.':
        'ASR chép “Lấy 2 với trừ nhau thì phần R triệt tiêu, hiệu 2 bánh bằng omega nhân L, chia cho L là ra công thức vận tốc cốc.” (0.857): ô-mê-ga (ω) đọc tách âm tiết, ASR viết “omega/ω”; lệch âm/thanh thuần Việt: vế/với, góc/cốc — NOT_VERIFIED bằng tai người',
    'Còn cộng hai vế rồi chia 2 thì trung bình hai bánh bằng ô-mê-ga nhân R, chính là vận tốc tiến v.':
        'ASR chép “Còn cộng 2 vế rồi chi 2 thì trung bình 2 bánh bằng omega nhân error chính là vận tốc tiếng V.” (0.783): ô-mê-ga (ω) đọc tách âm tiết, ASR viết “omega/ω”; chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: chia/chi, tiến/tiếng — NOT_VERIFIED bằng tai người',
    'Bước một, tính vận tốc tiến của tâm xe.':
        'ASR chép “Bước 1. Tính vận tóc tiếng của Tâm Xe” (0.778): lệch âm/thanh thuần Việt: tốc tiến/tóc tiếng — NOT_VERIFIED bằng tai người',
    'Bước bốn, một vòng tròn là 2 pi ra-đi-an, mà mỗi giây xe quay được ô-mê-ga ra-đi-an.':
        'ASR chép “Bước 4, một vòng tròn là 2 pi radian, mà mỗi dây xe quay được omega radian.” (0.7): ra-đi-an: probe RBM p1 8/8, ASR viết “radian/radiant”; ô-mê-ga (ω) đọc tách âm tiết, ASR viết “omega/ω” — NOT_VERIFIED bằng tai người',
    'Bước đầu cho x bằng 0 phẩy 005, y vẫn bằng 0, còn tê-ta tăng 0 phẩy 4 nhân 0 phẩy 01, bằng 0 phẩy 004 ra-đi-an.':
        'ASR chép “Bước đầu cho ít bằng 0,005, y vẫn bằng 0, còn Teta tăng 0,4 nhân 0,01 bằng 0,004 radian.” (0.792): “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; tê-ta theo lexicon RBM/ROB, ASR viết “theta/teta”; ra-đi-an: probe RBM p1 8/8, ASR viết “radian/radiant”; lệch âm/thanh thuần Việt: không (trong “không phẩy” → “”), không (trong “không phẩy” → “”) — NOT_VERIFIED bằng tai người',
    'Bước hai, nhân số xung với quãng mỗi xung.':
        'ASR chép “Bước 2, nhận số sung với quảng mỗi sung.” (0.778): lệch âm/thanh thuần Việt: nhân/nhận, quãng/quảng — NOT_VERIFIED bằng tai người',
    'Một cộng 1 phẩy 05 chia 2, được 1 phẩy 025 mét.':
        'ASR chép “Một cổng 1,05 chi 2 được 1,02 5m.” (0.741): đơn vị mét, ASR viết ký hiệu “m”; lệch âm/thanh thuần Việt: cộng/cổng, chia/chi, mươi/∅ — NOT_VERIFIED bằng tai người',
    'Bước hai, phép đo 2 phẩy 3 mét lệch 0 phẩy 3 mét, tức 3 xích-ma.':
        'ASR chép “Bước 2, phép đo 2,3m lật 0,3m, tức 3 sigma.” (0.727): đơn vị mét, ASR viết ký hiệu “m”; xích-ma (σ) đọc tách âm tiết, ASR viết “sigma”; lệch âm/thanh thuần Việt: lệch (trong “mét lệch” → “m lật”) — NOT_VERIFIED bằng tai người',
    'Chú ý lệch 0 phẩy 1 mét bây giờ là 2 xích-ma, vì xích-ma chỉ còn 0 phẩy 05.':
        'ASR chép “Chú ý lịch không phải 1 mét bây giờ là 2 sít ma, vì sít ma chỉ còn 0,005.” (0.75): “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; lệch âm/thanh thuần Việt: lệch/lịch, xích/sít, xích/sít, không (trong “không phẩy” → “”) — NOT_VERIFIED bằng tai người',
    'Giả thuyết A lệch 1 xích-ma, mật độ khoảng 2 phẩy 188.':
        'ASR chép “giả thuyết A lịch 1 sigma mật độ khoảng 2,188.” (0.788): xích-ma (σ) đọc tách âm tiết, ASR viết “sigma”; “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; lệch âm/thanh thuần Việt: lệch/lịch — NOT_VERIFIED bằng tai người',
    'Thấy cửa thì ba cột trước ba cánh cửa vọt lên, mỗi cột 0 phẩy 258.':
        'ASR chép “Thấy cửa thì ba cục trước ba cánh cửa vọc lên mỗi cục 0,258.” (0.789): “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; lệch âm/thanh thuần Việt: cột/cục, vọt/vọc, cột không (trong “cột không phẩy” → “cục”) — NOT_VERIFIED bằng tai người',
    'Ô 4 và ô 7 vừa là đỉnh vừa là cửa, nên được khoảng 0 phẩy 206.':
        'ASR chép “O4 và O7 vừa là đỉnh vừa là cửa nên được khoảng không phải 206.” (0.85): “ô” (ô lưới) ASR viết chữ “O”; “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải” — NOT_VERIFIED bằng tai người',
    'Ô 4 và ô 7 đi từ cửa tới cửa, được 0 phẩy 8 nhân 0 phẩy 8 bằng 0 phẩy 64, chia tổng 1 phẩy 5 ra 0 phẩy 427.':
        'ASR chép “O4 và O7 đi từ cửa tới cửa, được 0,8 nhân, 0,8 bằng, 0,64, chia tổng 1,5 ra, 0,427.” (0.917): “ô” (ô lưới) ASR viết chữ “O”; “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; lệch âm/thanh thuần Việt: không (trong “không phẩy” → “”) — NOT_VERIFIED bằng tai người',
    'Đạo hàm của sin là cos, tại 0 thì bằng 1, nên gần 0 ta có sin tê-ta xấp xỉ tê-ta.':
        'ASR chép “Đạo hàm của sinh là cô sinh, tại không thì bằng một, nền gần không ta có sinh tê ta sắp xỉ tê ta.” (0.792): sin đọc thô, ASR viết “sinh” (gần âm); lệch âm/thanh thuần Việt: nên/nền, xấp/sắp — NOT_VERIFIED bằng tai người',
    'Làm thử, sin của 0 phẩy 1 ra-đi-an là khoảng 0 phẩy 0998, rất gần 0 phẩy 1.':
        'ASR chép “Làm thử, sinh của 0.1 radiant là khoảng 0.000998 rất gần 0.1.” (0.791): sin đọc thô, ASR viết “sinh” (gần âm); “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; ra-đi-an: probe RBM p1 8/8, ASR viết “radian/radiant” — NOT_VERIFIED bằng tai người',
    'Điểm đến lệch ngang khoảng 0 phẩy 1 mét, đúng bằng quãng đi nhân góc lệch, nhờ sin tê-ta xấp xỉ tê-ta.':
        'ASR chép “Điểm đến lệch ngang khoảng 0,1m đúng bằng quảng đi nhân gốc lệch, nhờ sinh theta sắp xỉ theta.” (0.708): đơn vị mét, ASR viết ký hiệu “m”; sin đọc thô, ASR viết “sinh” (gần âm); lệch âm/thanh thuần Việt: quãng/quảng, góc/gốc, tê/sinh thê, xấp/sắp, tê/thê — NOT_VERIFIED bằng tai người',
    'Hình bên phải so đường cong sin tê-ta màu xanh với tiếp tuyến tê-ta màu cam, khi góc lệch tăng từ 0 tới 90 độ.':
        'ASR chép “Hình bên phải so đường công xinh teta màu xanh với tiết tuyến teta màu cam khi gốc lệch tăng từ 0 tới 90 độ.” (0.741): tê-ta theo lexicon RBM/ROB, ASR viết “theta/teta”; sin đọc thô, ASR viết “sinh” (gần âm); lệch âm/thanh thuần Việt: cong (trong “cong sin t ta” → “công xinh teta”), tiếp/tiết, góc/gốc — NOT_VERIFIED bằng tai người',
    'Bước một, tính Jacobian tại ước lượng hiện tại, với tê-ta bằng 0 và s bằng 1, nên âm s sin 0 bằng 0, còn s cos 0 bằng 1.':
        'ASR chép “Bước 1, tính da cô biên tại ước lượng hiện tại, với Teta bằng 0 và S bằng 1, nền âm S sinh không bằng 0, còn Ecosin không bằng 1.” (0.831): tê-ta theo lexicon RBM/ROB, ASR viết “theta/teta”; sin đọc thô, ASR viết “sinh” (gần âm); chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: nên/nền, cô (trong “s cô sin” → “ecosin”) — NOT_VERIFIED bằng tai người',
    'Bước bốn, thêm hai lần đo trống, mỗi lần cộng lôgarit của 0 phẩy 4 chia 0 phẩy 6, tức trừ khoảng 0 phẩy 405.':
        'ASR chép “Bước 4, thêm hai lần đo trống, mỗi lần cộng logatic của 0,4-0,6, tức trừ khoảng 0,405.” (0.906): “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; lệch âm/thanh thuần Việt: lôgarit/logatic, chia/∅, không (trong “không phẩy” → “”) — NOT_VERIFIED bằng tai người',
    'Bảng lấy một kho 100 mét nhân 100 mét, mỗi ô giữ 1 byte.':
        'ASR chép “Bản lấy 1 kho 100 mét nhân 100 mét mỗi ô giữ 1 bay.” (0.875): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: bảng/bản — NOT_VERIFIED bằng tai người',
    'Ô 5 xen-ti-mét cho 4 triệu ô, tức 4 triệu byte, và một tia 10 mét đi qua 200 ô.':
        'ASR chép “O5 cm cho 4 triệu ô, tức 4 triệu bay và một tia 10 mét đi qua 200 ô.” (0.87): “ô” (ô lưới) ASR viết chữ “O”; byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: xen/xăng — NOT_VERIFIED bằng tai người',
    'Ô 2 xen-ti-mét cho 25 triệu ô, tức 25 triệu byte, và mỗi tia đi qua 500 ô, tức mỗi lần quét chậm hơn 2 phẩy 5 lần.':
        'ASR chép “Ô 2 cm cho 25 triệu ô, tức 25 triệu bay và mỗi ti đi qua 500 ô, tức mỗi lần quét chậm hơn 2,5 lần.” (0.914): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: xen/xăng, tia/ti — NOT_VERIFIED bằng tai người',
    'Lệnh cho xe là một cặp v và ô-mê-ga, tốc độ tiến và vận tốc góc, như cặp 0 phẩy 5 và 0 nghĩa là đi thẳng.':
        'ASR chép “Lệnh cho xe là một cặp V và Omega, tốc độ tiến và vận tốc góc, như cặp 0.5 và không nghĩa là đi thẳng.” (0.909): ô-mê-ga (ω) đọc tách âm tiết, ASR viết “omega/ω”; “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải” — NOT_VERIFIED bằng tai người',
    'Bán kính quay bằng v chia ô-mê-ga, nên cặp 0 phẩy 3 và 0 phẩy 5 là rẽ trái với bán kính 0 phẩy 6 mét.':
        'ASR chép “Bán kính quay bằng V-omega nên cặp 0,3 và 0,5 là đệ trái với bán kính 0,6 m.” (0.83): ô-mê-ga (ω) đọc tách âm tiết, ASR viết “omega/ω”; đơn vị mét, ASR viết ký hiệu “m”; lệch âm/thanh thuần Việt: chia (trong “chia ô mê ga” → “omega”), rẽ/đệ — NOT_VERIFIED bằng tai người',
    'Hình vẽ mỗi lệnh như một điểm, trục ngang là tốc độ v, trục đứng là vận tốc góc ô-mê-ga.':
        'ASR chép “Hình vẽ mỗi lệnh như 1 điểm, trục ngang là tốc độ V, trục đứng là vận tốc góp omega.” (0.857): ô-mê-ga (ω) đọc tách âm tiết, ASR viết “omega/ω”; lệch âm/thanh thuần Việt: góc (trong “góc ô mê ga” → “góp omega”) — NOT_VERIFIED bằng tai người',
    'Điều thứ hai, ở bài 1 ta đã thấy xe vi sai đi trên vòng bán kính R bằng v chia ô-mê-ga, tức vận tốc góc bằng v chia R.':
        'ASR chép “Điều thứ 2, ở bài 1 ta đã thấy xe V-Side đi trên vòng bán kính R bằng V-Omega, tức vận tốc góc bằng V-R.” (0.833): ô-mê-ga (ω) đọc tách âm tiết, ASR viết “omega/ω”; lệch âm/thanh thuần Việt: vi sai/v side, chia (trong “chia ô mê ga” → “omega”), chia/∅ — NOT_VERIFIED bằng tai người',
    'Bước ba, đổi độ cong ra lệnh vận tốc góc cho xe đi 0 phẩy 5 mét mỗi giây.':
        'ASR chép “Bước 3. Đổi độ công tra lệnh vận tốc gốc cho xe đi không phải 5 mét mỗi giây.” (0.789): “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; lệch âm/thanh thuần Việt: cong ra/công tra, góc/gốc — NOT_VERIFIED bằng tai người',
    'Mô phỏng bằng bước Euler 0 phẩy 001 giây với v bằng 0 phẩy 5 và ô-mê-ga bằng 0 phẩy 125, chạy trong khoảng 4 phẩy 04 giây.':
        'ASR chép “Mô phỏng bằng bước Euler 0.001 dây với V bằng 0.5 và Omega bằng 0.125, chạy trong khoảng 4.04 dây.” (0.833): “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; ô-mê-ga (ω) đọc tách âm tiết, ASR viết “omega/ω”; lệch âm/thanh thuần Việt: không (trong “không phẩy” → “”), không (trong “không phẩy” → “”) — NOT_VERIFIED bằng tai người',
    'Hộp xa lệch 1 mét và cách 8 mét, tỉ số cũng là 0 phẩy 125.':
        'ASR chép “Hộp xa lệch 1m và cách 8m, tỷ số cũng là 0,125.” (0.789): đơn vị mét, ASR viết ký hiệu “m”; “tỉ” ASR viết chính tả “tỷ” (cùng âm); “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; lệch âm/thanh thuần Việt: không (trong “không phẩy” → “”) — NOT_VERIFIED bằng tai người',
    'Câu ba, chuyển vế công thức độ sâu, khoảng cách hai camera bằng Z nhân d chia f, tức 8 nhân 24 chia 800, bằng 0 phẩy 24 mét, gấp đôi khoảng cách cũ.':
        'ASR chép “Câu 3, chuyển với công thức độ sâu, khoảng cách 2 camera bằng giác nhân dê chia s, tức 8 nhân 24 chia 800, bằng 0,24m, gấp đôi khoảng cách cũ.” (0.923): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; đơn vị mét, ASR viết ký hiệu “m”; lệch âm/thanh thuần Việt: vế/với — NOT_VERIFIED bằng tai người',
    'Bước ba, cộng hai phần lại thành quãng dừng.':
        'ASR chép “Bước 3, cộng 2 phần lại thành quảng dưng.” (0.778): lệch âm/thanh thuần Việt: quãng dừng/quảng dưng — NOT_VERIFIED bằng tai người',
    'Bước năm, thử trường hợp xấu, cùng tốc độ nhưng sàn ướt.':
        'ASR chép “Bước năm, thử trường hợp xấu cùng tốc độ nhân sản ước.” (0.75): lệch âm/thanh thuần Việt: nhưng sàn ướt/nhân sản ước — NOT_VERIFIED bằng tai người',
    # ── Đợt A đào sâu: CLD (lượt 4) ──
    'Tương tự, một mi-crô giây lại bằng 1000 na-nô giây.':
        'ASR chép “Tương tự, một micro dấy lại bằng một nghìn nano dấy.” (0.583): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh — NOT_VERIFIED bằng tai người',
    'Số 3 đứng đầu là số của bản chính.':
        'ASR chép “Số 3 đứng đầu là số của bạn 9.” (0.778): lệch âm/thanh thuần Việt: bản chính/bạn chín — NOT_VERIFIED bằng tai người',
    'Câu hai, ta lập bảng đặt từng Pod vào các nút theo đúng thứ tự.':
        'ASR chép “Câu 2. Ta lập bảng đặt từng pốt vào các nút theo đúng thứ tự.” (0.933): Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút) — NOT_VERIFIED bằng tai người',
    # ── Đợt B đào sâu: NET ──
    'Trên màn hình, chữ B viết tắt cho byte, ví dụ 20 B nghĩa là 20 byte.':
        'ASR chép “Trên màn hình, chữ bềm chiếc tắt cho bay, ví dụ 20b nghĩa là 20 bay.” (0.789): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: viết (trong “b viết” → “bềm chiếc”) — NOT_VERIFIED bằng tai người',
    'Thứ hai là tỉ lệ phần trăm, bằng phần có ích chia cho toàn bộ, rồi nhân 100.':
        'ASR chép “Thứ 2 là tỷ lệ phần trăm, bằng phần có chia cho toàn bộ, rồi nhân 100.” (0.919): “tỉ” ASR viết chính tả “tỷ” (cùng âm); lệch âm/thanh thuần Việt: ích/∅ — NOT_VERIFIED bằng tai người',
    'Tầng ứng dụng có 1460 byte dữ liệu.':
        'ASR chép “Tần ứng dụng có 1.463 giữ liệu.” (0.846): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: tầng/tần — NOT_VERIFIED bằng tai người',
    'Tầng vận chuyển bọc thêm 20 byte TCP, thành 1480 byte.':
        'ASR chép “Tân vận chuyển bọc thêm 20 bai TCP thành 1480 bai.” (0.824): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: tầng/tân — NOT_VERIFIED bằng tai người',
    'Tầng mạng bọc thêm 20 byte IP, thành 1500 byte, rồi tầng liên kết thêm 14 byte đầu và 4 byte đuôi Ethernet, thành 1518 byte.':
        'ASR chép “Tần mạng bọc thêm 20 vai IP, thành 1.500 vai, rồi tầng liên kết thêm 14 vai đầu và 4 vai đuôi Ethernet, thành 1.518 vai.” (0.833): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: tầng/tần — NOT_VERIFIED bằng tai người',
    'TCP 20 byte, IP 20 byte, Ethernet gồm 14 byte đầu và 4 byte đuôi, tức 18 byte, cộng lại là 58 byte phong bì.':
        'ASR chép “TCP-20-BYE, IP-20-BYE, Ethernet Go 14-BYE đầu và 4-BYE đuôi, tức 18-BYE, cộng lại là 58-BYE phong bì.” (0.774): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: gồm/go — NOT_VERIFIED bằng tai người',
    'Bước bốn, đổi sang một gói nhỏ chỉ 100 byte dữ liệu, ví dụ một tin nhắn ngắn.':
        'ASR chép “Bước 4, đổi sang một gói nhỏ chỉ 130 dữ liệu, ví dụ một tin nhắn ngắn.” (0.923): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Phong bì vẫn là 58 byte, nên khung dài 100 cộng 58, bằng 158 byte.':
        'ASR chép “Phong bị vẫn là 58 bài nên khung dài 158 bằng 158 bài.” (0.851): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: bì/bị, cộng/∅ — NOT_VERIFIED bằng tai người',
    'Ví dụ khi TCP thêm 12 byte tuỳ chọn, phần đầu TCP dài 32 byte, khung vẫn dài 1518 byte, thì dữ liệu chỉ còn 1448 byte, hiệu suất khoảng 95 phẩy 4 phần trăm.':
        'ASR chép “Ví dụ khi TCP thêm 12 bay tùy chọn, phần đầu TCP dài 32 bay, khung vẫn dài 1518 bay, thì dữ liệu chỉ còn 1448 bay, hiệu suất khoảng 95,4%.” (0.922): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Một dịch vụ gửi 1000 tin mỗi giây, mỗi tin 100 byte, chỉ đếm dữ liệu thì là 100 nghìn byte mỗi giây.':
        'ASR chép “Một dịch vụ gửi 1.000 tin mỗi giây, mỗi tin 100 bay, chỉ đếm dữ liệu thì là 100.000 bay mỗi giây.” (0.923): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Đếm cả khung, mỗi tin thành 158 byte, nên thật ra là 158 nghìn byte mỗi giây, gấp 1 phẩy 58 lần.':
        'ASR chép “Đếm cả khung, mỗi tinh thành 158 bài nên thật ra là 158.000 bài mỗi dây gấp 1,58 lần.” (0.906): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: tin/tinh — NOT_VERIFIED bằng tai người',
    'Con số này nằm giữa 63 phẩy 3 của gói nhỏ và 96 phẩy 2 của khung đầy, đúng như ta dự đoán, vì 500 byte nằm giữa 100 và 1460.':
        'ASR chép “Con số này nằm giữa 63,3 của gói nhỏ và 96,2 của khung đầy, đúng như ta dự đoán, vì 500 by nằm giữa 100 và 1460.” (0.976): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Còn mi li giây là một phần nghìn giây, ví dụ 0 phẩy 0 0 4 giây nhân 1000 thành 4 mi li giây.':
        'ASR chép “Còn mili giây là một phần nghìn giây, ví dụ không phải 004 nân 1 nghìn thành 4 mili giây.” (0.711): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; lệch âm/thanh thuần Việt: không không (trong “phẩy không không” → “phải”), nhân (trong “giây nhân” → “nân”) — NOT_VERIFIED bằng tai người',
    'Bước một, tính trễ truyền, tốc độ liên kết đo bằng bit, nên trước hết đổi 1500 byte thành 1500 nhân 8, bằng 12 nghìn bit.':
        'ASR chép “Bước 1, tính trễ truyền, tốc độ liên kết đo bằng bit, nền trước hết đổi 1.500 bay thành 1.500 nhân 8 bằng 12.000 bit.” (0.939): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: nên/nền — NOT_VERIFIED bằng tai người',
    'Chia 12 nghìn bit cho 100 triệu bit mỗi giây, được 0 phẩy 0 0 0 1 2 giây, tức 0 phẩy 12 mi li giây.':
        'ASR chép “Chi 12.000 bit cho 100 triệu bit mỗi giây được 0.00012 giây, tức 0.12 mili giây.” (0.769): “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; lệch âm/thanh thuần Việt: chia/chi, không không không một (trong “phẩy không không không một” → “mười”) — NOT_VERIFIED bằng tai người',
    'Trong ví dụ của ta, kết quả sai sẽ là 0 phẩy 0 1 5 mi li giây thay vì 0 phẩy 12 mi li giây.':
        'ASR chép “Trong ví dụ của ta, kết quả sai sẽ là 0,05ml thay vì 0,12ml.” (0.792): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; lệch âm/thanh thuần Việt: không một/∅ — NOT_VERIFIED bằng tai người',
    'Đáp án câu một, trước hết đổi 1250 byte thành 1250 nhân 8, bằng 10 nghìn bit.':
        'ASR chép “Đáp án câu một trước hết đổi 1.250 bai thành 1.250 nhân tám bằng 10.000 bít.” (0.926): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: bit/bít — NOT_VERIFIED bằng tai người',
    'Trễ truyền bằng 10 nghìn bit chia 10 triệu bit mỗi giây, được 1 mi li giây.':
        'ASR chép “trễ truyền bằng 10.000 bít chia 10 triệu bít mỗi giây, được 1 mili giây.” (0.788): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; lệch âm/thanh thuần Việt: bit/bít, bit/bít — NOT_VERIFIED bằng tai người',
    'Dung lượng tệp đo bằng MB, tức triệu byte, ví dụ 2 MB là 2 triệu byte.':
        'ASR chép “Dung lượng tẹp đo bằng megabyte, tức triệu byte, ví dụ hai megabyte là hai triệu byte.” (0.824): MB đọc “mê-ga-byte” theo lexicon của khoá, ASR viết “MB/megabyte”; lệch âm/thanh thuần Việt: tệp/tẹp — NOT_VERIFIED bằng tai người',
    'Bước năm, đổi ra byte bằng cách chia cho 8.':
        'ASR chép “Bước 5, đổi ra bay bằng cách chia cho 8.” (0.9): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Liên kết 100 triệu bit mỗi giây đẩy được 100 nghìn bit mỗi mi li giây, nhân 50 mi li giây được 5 triệu bit.':
        'ASR chép “Liên kết 100 triệu bit mỗi dây đẩy được 100.000 bit mỗi mili dây, nhần 50 mili dây được 5 triệu bit.” (0.778): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; lệch âm/thanh thuần Việt: nhân (trong “mi li giây nhân” → “mili dây nhần”) — NOT_VERIFIED bằng tai người',
    'Lỗi thứ năm hay gặp ở người đã đi làm, hẹn sao lưu một nghìn tỉ byte qua đường 100 triệu bit mỗi giây, trong khung đêm 8 giờ.':
        'ASR chép “Lỗi thứ năm hay gặp ở người đã đi làm, hẹn sao lưu 1.000 tỷ bay qua đường 100 triệu bit mỗi giây, trong khung đêm 8 giờ.” (0.933): “tỉ” ASR viết chính tả “tỷ” (cùng âm); byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Chia cho 8 để ra byte, ta được 12 phẩy 5 triệu byte, tức 12 phẩy 5 MB đang nằm trên đường.':
        'ASR chép “Chia cho 8 để ra bay, ta được 12,5 triệu bay, tức 12,5 megabyte đang nằm trên đường.” (0.875): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); MB đọc “mê-ga-byte” theo lexicon của khoá, ASR viết “MB/megabyte” — NOT_VERIFIED bằng tai người',
    'Chuỗi 1 0 1 1, 0 0 1 có bốn bit 1, chia cho 2 dư 0, nên là số chẵn.':
        'ASR chép “Chủy 101.001 có 4bit 1, chia cho 2 dư không nên là số chẳng.” (0.682): lệch âm/thanh thuần Việt: chuỗi/chuỷ, một một không không/trăm linh, chẵn/chẳng — NOT_VERIFIED bằng tai người',
    'Một khung Ethernet đầy dài 1518 byte, nhưng chỉ có 4 byte đuôi kiểm lỗi bằng CRC.':
        'ASR chép “Một khung Ethernet đầy dài 1.518 bai, nhưng chỉ có 4 bai đuôi kiểm lỗi bằng CRC.” (0.909): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Vậy ở đây CRC bắt được mọi lỗi một bit, nhưng không bắt được mọi lỗi nhiều bit.':
        'ASR chép “Vậy ở đây xe ra xe bắt được mọi lỗi 1 bit, nhưng không bắt được mọi lỗi nhiều bit.” (0.895): lệch âm/thanh thuần Việt: crc/xe ra xe — NOT_VERIFIED bằng tai người',
    'Bên nhận chia chuỗi đó được 0 0 1, nên báo lỗi dù dây không hề có nhiễu.':
        'ASR chép “Bên nhận chi chủ đó được 001, nên báo lỗi dù dây không hề có nhiều.” (0.765): lệch âm/thanh thuần Việt: chia chuỗi/chi chủ, không không/∅, nhiễu/nhiều — NOT_VERIFIED bằng tai người',
    'Do đó bit hỏng ngay trong bộ định tuyến sẽ được bọc bằng một CRC hợp lệ.':
        'ASR chép “Do đó biết hỏng ngay trong bộ định tuyến sẽ được bọc bằng một xe rơi xe hợp lệ.” (0.833): lệch âm/thanh thuần Việt: bit/biết, crc/xe rơi xe — NOT_VERIFIED bằng tai người',
    'Phần dư là 0 0 0, nên đáp án 0 1 1 là đúng.':
        'ASR chép “Phần du là 0000 nên đáp án 011 là đúng.” (0.72): lệch âm/thanh thuần Việt: dư/du, không không/∅, không một/mười — NOT_VERIFIED bằng tai người',
    'Bước 2, thay G bằng 0 phẩy 5 vào công thức của ALOHA thuần.':
        'ASR chép “Bước hai, thay dê bằng không phải nằm vào công thức của Aloha thuần.” (0.857): “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; lệch âm/thanh thuần Việt: năm (trong “phẩy năm” → “phải nằm”) — NOT_VERIFIED bằng tai người',
    'Bước 3, cũng với G bằng 0 phẩy 5, thay vào công thức của ALOHA chia khe.':
        'ASR chép “Bước 3 cũng với dê bằng 0,5, thay vào công thức của Aloha chia khe.” (1.0): chữ cái G đứng riêng đọc tên kiểu Việt “giê”, ASR viết “dê”; mọi từ và số còn lại khớp — NOT_VERIFIED bằng tai người',
    'Với ALOHA thuần, 10 nhân 0 phẩy 184 chỉ còn 1 phẩy 84 triệu bit mỗi giây.':
        'ASR chép “Với Aloha Thuận, 10 nhân 0,184 chỉ còn 1,84 triệu bit mỗi giây.” (0.909): “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; lệch âm/thanh thuần Việt: thuần/thuận, không (trong “không phẩy” → “”) — NOT_VERIFIED bằng tai người',
    'Với ALOHA chia khe, 10 nhân 0 phẩy 303 được 3 phẩy 03 triệu bit mỗi giây, gấp khoảng 1 phẩy 6 lần chỉ nhờ phát đúng đầu khe.':
        'ASR chép “Với Aloha chi khe, 10 nhân 0,303 được 3,03 triệu bit mỗi giây, gấp khoảng 1,6 lần chỉ nhờ phát đúng đầu khe.” (0.935): “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; lệch âm/thanh thuần Việt: chia/chi, không (trong “không phẩy” → “”) — NOT_VERIFIED bằng tai người',
    'Kiểm mức tối đa 36 phẩy 8 phần trăm của ALOHA chia khe bằng cách thử các giá trị G nằm hai bên số 1.':
        'ASR chép “Kiểm mức tối đa 36,8% của Aloha chi khe bằng cách thử các giá trị dê nằm 2 bên số 1.” (0.963): lệch âm/thanh thuần Việt: chia/chi — NOT_VERIFIED bằng tai người',
    'Vạch đỏ cắt ngang byte cuối, nên hai bit đầu của byte cuối thuộc về phần mạng.':
        'ASR chép “Vặt đỏ cắt ngang bay cuối, nên hai biết đầu của bay cuối thuộc về phần mạng.” (0.765): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: vạch/vặt, bit/biết — NOT_VERIFIED bằng tai người',
    'Hình dưới trải byte cuối thành một trục từ 0 tới 255, và hai bit mạng đó chia trục thành bốn khối, mỗi khối 64 địa chỉ.':
        'ASR chép “hình dưới trải bay cuối thành một trục từ 0 tới 255 và hai biết mạng đó chia trục thành bốn khối, mỗi khối 64 địa chỉ.” (0.939): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: bit/biết — NOT_VERIFIED bằng tai người',
    'Để thấy rõ, hai byte đầu là 16 bit mạng, nên giữ nguyên 10 chấm 0.':
        'ASR chép “Để thấy rõ, hai bay đầu là 16 bích mạng nên giữ nguyên 10.0.” (0.848): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: bit/bích, chấm/∅ — NOT_VERIFIED bằng tai người',
    'Byte thứ ba còn 22 trừ 16 bằng 6 bit mạng và 2 bit máy, bật hai bit máy được 2 cộng 1, bằng 3.':
        'ASR chép “Bài thứ 3 còn 22,16 bằng 6 biết mạng và 2 biết máy. Bật 2 biết máy được 2 cộng 1 bằng 3.” (0.821): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: trừ/phẩy, bit/biết, bit/biết, bit/biết — NOT_VERIFIED bằng tai người',
    'Byte thứ tư toàn bit máy, bật hết được 255.':
        'ASR chép “Bài thứ tư toàn bích máy bật hết được 255.” (0.857): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: bit/bích — NOT_VERIFIED bằng tai người',
    'Trước hết, ôn lại cách đổi một byte ra nhị phân, như ở bài 5 khi ta tìm mạng con chứa một địa chỉ.':
        'ASR chép “Trước hết, ông lại cách đổi một bay ra nhị phân, như ở bài năm khi ta tìm mạng con chứa một địa chỉ.” (0.917): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: ôn/ông — NOT_VERIFIED bằng tai người',
    'Hình này đặt ba mục của bảng lên trục byte thứ ba của địa chỉ, với hai byte đầu là 200 chấm 23.':
        'ASR chép “Hình này đặt ba mục của bảng lên trục bay thứ ba của địa chỉ, với hai bay đầu là 200.23.” (0.902): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: chấm/∅ — NOT_VERIFIED bằng tai người',
    'Cột giữa ghi những bit đầu của byte thứ ba mà mỗi mục đòi phải trùng, dấu gạch dưới là chỗ bit nào cũng được.':
        'ASR chép “Cột giữ ghi những biết đầu của bay thứ ba mà mỗi một đòi phải trung, giấu gạch dưới là chỗ biết nào cũng được.” (0.76): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: giữa/giữ, bit/biết, mục/một, trùng/trung, bit/biết — NOT_VERIFIED bằng tai người',
    'Bước ba, gói thứ hai tới 200 chấm 23 chấm 18 chấm 1, byte thứ ba 18 viết nhị phân là 0 0 0 1, 0 0 1 0.':
        'ASR chép “Bước 3, gói thứ 2 tới 200.23.18.1, bài thứ 3-18 viết nhị phân là 0001-0010.” (0.78): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: chấm/∅, chấm/∅, chấm/∅, không không không/∅, không không một không/mười — NOT_VERIFIED bằng tai người',
    'Bước bốn, gói thứ ba tới 8 chấm 8 chấm 8 chấm 8.':
        'ASR chép “Bước 4 gọi thứ 3 tới 8.8.8.8.” (0.783): lệch âm/thanh thuần Việt: gói/gọi, chấm/∅, chấm/∅, chấm/∅ — NOT_VERIFIED bằng tai người',
    'Byte đầu là 8, viết nhị phân 0 0 0 0, 1 0 0 0, còn 200 là 1 1 0 0, 1 0 0 0, khác nhau ngay từ bit đầu tiên.':
        'ASR chép “Bay đầu là 8, viết nhị phân 0000-1000, còn 200 là 1100-1000, khác nhau ngay từ biết đầu tiên.” (0.689): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: không không không/∅, không không không/nghìn, không không/trăm, không không không/nghìn, bit/biết — NOT_VERIFIED bằng tai người',
    'Khối bắt đầu ở 16, nên byte thứ ba chạy từ 16 tới 16 cộng 16 trừ 1, bằng 31.':
        'ASR chép “Khối bắt đầu ở 16, nên bài thứ 3 chạy từ 16 tới 16 cộng 16.1 bằng 31.” (0.941): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: trừ/∅ — NOT_VERIFIED bằng tai người',
    'Bắt đầu ở 24, byte thứ ba chạy từ 24 tới 31.':
        'ASR chép “Bắt đầu ở 24, bài thứ 3 chạy từ 24 tới 31.” (0.944): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Khi đã tính ra khoảng bằng lũy thừa của 2, ta chỉ cần xem byte thứ ba có nằm trong khoảng hay không.':
        'ASR chép “Khi đã tính ra khoảng bằng lũy Thừa của 2, ta chỉ cần xem bay thứ 3 có nằm trong khoảng hay không?” (0.957): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Bước một, chốt S với khoảng cách 0.':
        'ASR chép “Bước 1, chốt ét với khoảng cách 0.” (0.875): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Bước ba, còn A tạm 3, C tạm 6, D tạm 9, nên chốt A với khoảng cách 3.':
        'ASR chép “Bước 3 còn A tạm 3, C tạm 6, G tạm 9, nền chốt A với khoảng cách 3.” (0.895): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: nên/nền — NOT_VERIFIED bằng tai người',
    'Kiểm bằng đường khác, không chạy thuật toán mà liệt kê hết mọi đường đơn từ S tới D, tức đường không ghé một bộ định tuyến hai lần.':
        'ASR chép “Kiểm bằng đường khác, không chạy thuộc toán mà liệt kê hết mọi đường đơn từ S tới G, tức đường không ghé 1 bộ định tuyến 2 lần.” (0.931): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: thuật/thuộc — NOT_VERIFIED bằng tai người',
    'Đáp án, ta chạy lại thuật toán từ S với liên kết S, B nay tốn 10.':
        'ASR chép “Đáp án, ta chạy lại thuộc toán từ F với liên kết S, B này tốn 10.” (0.824): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: thuật/thuộc, nay/này — NOT_VERIFIED bằng tai người',
    'Nếu bắt đầu ở ô s và lấy n ô, thì ô cuối là s cộng n trừ 1, ở đây 101 cộng 500 trừ 1 bằng 600.':
        'ASR chép “Nếu bắt đầu ở OS và lấy NO thì ô cuối là X cộng N trừ 1, ở đây 100 linh 1 cộng 500 trừ 1 bằng 600.” (0.906): “ô” (ô lưới) ASR viết chữ “O”; chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Còn ô kế tiếp ngay sau đó là s cộng n, tức 601, con số này sẽ quay lại nhiều lần trong bài.':
        'ASR chép “Còn OK tiếp ngay sau đó là S cộng N, tức 600-01, còn số này sẽ quay lại nhiều lần trong bài.” (0.88): “ô” (ô lưới) ASR viết chữ “O”; lệch âm/thanh thuần Việt: kế (trong “ô kế” → “ok”), linh/∅, con/còn — NOT_VERIFIED bằng tai người',
    'Hãy hình dung dữ liệu của một chiều như một con phố dài, mỗi byte là một ngôi nhà có số riêng.':
        'ASR chép “Hãy hình dung giữ liệu của một chiều như một con phố dài, mỗi bay là một ngôi nhà có số riêng.” (0.955): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Đoạn thứ nhất chở các byte từ 101 tới 600, nên số thứ tự của nó là 101, số của ngôi nhà đầu tiên.':
        'ASR chép “Đoạn thứ nhất cho các bài từ 101 tới 600 nên số thứ tự của nó là 101 số của ngôi nhà đầu tiên.” (0.935): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: chở/cho — NOT_VERIFIED bằng tai người',
    'Đoạn thứ hai bắt đầu đúng ở 601, chở 300 byte tới 900, nên số xác nhận tiếp theo là 901.':
        'ASR chép “Đoạn thứ 2 bắt đầu đúng ở 601, chở 300 bài tới 900, nên số xác nhận tiếp theo là 901.” (0.966): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Bước hai, khách gửi tiếp một đoạn 300 byte.':
        'ASR chép “Bước 2, khách gửi tiếp 1 đoạn 300 bay.” (0.9): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Đoạn này bắt đầu đúng ở byte mà máy chủ đang chờ, nên số thứ tự của nó là 601.':
        'ASR chép “Đoạn này bắt đầu đúng ở bay mà mấy chủ đang chờ, nên số thứ tự của nó là 601.” (0.913): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: máy/mấy — NOT_VERIFIED bằng tai người',
    'Bước ba, máy chủ trả lời 200 byte.':
        'ASR chép “Bước 3, máy chủ trả lời 200 bay.” (0.889): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Bây giờ kiểm các số xác nhận bằng một đường khác, không cộng từng đoạn nữa mà đếm thẳng cả dòng byte.':
        'ASR chép “Bây giờ kiểm ca số xác nhận bằng một đường khác, không cộng từng đoạn nữa mà đếm thẳng cãi dòng bay.” (0.864): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: các/ca, cả/cãi — NOT_VERIFIED bằng tai người',
    'Chiều từ khách tới máy chủ đã nhận các byte từ 101 tới 900, tức 900 trừ 101 cộng 1, bằng 800 byte, cộng vào byte đầu 101 được 901, khớp với bước hai.':
        'ASR chép “Chiều từ khách tới máy chủ đã nhận các bay từ 101 tới 900, tức 900 trừ 101 cộng 1, bằng 800 bay, cộng vào bay đầu 101 được 901, khớp với bước 2.” (0.939): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Chiều ngược lại đã nhận các byte từ 301 tới 500, đúng 200 byte, nên số xác nhận là 501, khớp với bước ba.':
        'ASR chép “Chiều ngược lại đã nhận các bai từ 301 tới 500, đúng 200 bai, nên số xác nhận là 501, khớp với bước 3.” (0.938): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Byte đầu mang số 2001 vì gói mở kết nối đã dùng số 2000, và 100 byte chiếm các số từ 2001 tới 2100.':
        'ASR chép “Bay đầu mang số 2.001 vì gói mở kết nối đã dùng số 2.000 và 100 bay chiếm các số từ 2.001 tới 2.100.” (0.949): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Kiểm lại bằng phép đếm, từ 2001 tới 2100 có 2100 trừ 2001 cộng 1, đúng 100 byte.':
        'ASR chép “Kiểm lại bằng phép đếm. Từ 2000 linh 1 tới 2100 có 2100 trừ 2000 linh 1 cộng 1, đúng 100 bay.” (0.909): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: không trăm/∅, không trăm/∅ — NOT_VERIFIED bằng tai người',
    'Còn 10 gói phát trong 12 mi li giây, đủ lấp cả chu kỳ.':
        'ASR chép “Còn 10 gói phát trong 12ml đủ lấp cả cho kỳ.” (0.786): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; lệch âm/thanh thuần Việt: chu/cho — NOT_VERIFIED bằng tai người',
    'Một lượt thì chờ 50 mi li giây.':
        'ASR chép “Một lượt thì chờ 50ml dây.” (0.706): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh — NOT_VERIFIED bằng tai người',
    'Gói xác nhận thứ ba có thể mang kèm dữ liệu, nên bắt tay tốn đúng một lượt đi về trước byte dữ liệu đầu tiên.':
        'ASR chép “Gói xác nhận thứ 3 có thể mang kèm giữ liệu, nên bắt tay tốn đúng một lượt đi về trước bay giữ liệu đầu tiên.” (0.962): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Đặt ba kết quả cạnh nhau cho một trang HTML và 10 đối tượng.':
        'ASR chép “Đặt 3 kết quả cạnh nhau cho 1 trang HT, ML và 10 đối tượng.” (0.897): HTML đọc “hát tê em eo” theo lexicon WEB, ASR viết “html/HT ML” — NOT_VERIFIED bằng tai người',
    'Kết nối không bền, trang HTML tốn 2 lượt, mỗi đối tượng lại mở kết nối mới nên thêm 2 lượt.':
        'ASR chép “Kết nối không bình, trang HT-ML tốn hai lượt, mỗi đối tượng lại mở kết nối mới nên thêm hai lượt.” (0.884): HTML đọc “hát tê em eo” theo lexicon WEB, ASR viết “html/HT ML”; lệch âm/thanh thuần Việt: bền/bình — NOT_VERIFIED bằng tai người',
    'Câu hai, kết nối bền, trang HTML vẫn tốn 2 lượt, nhưng mỗi đối tượng chỉ còn 1 lượt yêu cầu.':
        'ASR chép “Câu 2, kết nối bình, trang html vẫn tốn hai lượt, nhưng mỗi đối tượng chỉ còn một lượt yêu cầu.” (0.952): lệch âm/thanh thuần Việt: bền/bình — NOT_VERIFIED bằng tai người',
    # ── Đợt B đào sâu: NET (cờ THIẾU) ──
    'Nhân với 1000 để đổi ra mi li giây, được 0 phẩy 0 0 8 mi li giây.':
        'ASR chép “Nhân với 1 nghìn để đổi ra mili giây được 0.008 mili giây.” (0.688): cờ THIẾU là giả — ASR gộp “0 phẩy 0 0 8” thành số “0.008” (đúng giá trị) và viết gộp “mili”; mọi từ đều có mặt, không có âm thanh cụt — NOT_VERIFIED bằng tai người',
    # ── Đợt B đào sâu: CSA ──
    'Hình này cho thấy một byte như một hàng tám công tắc.':
        'ASR chép “Hình này cho thấy một bay như một hàng tám công tắc.” (0.917): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Thử ngay, 0 1 0 1 cộng 0 0 1 1 ra 1 0 0 0, đúng là 5 cộng 3 bằng 8.':
        'ASR chép “Thử ngay, 0101 cộng 001-1000, đúng là 5 cộng 3 bằng 8.” (0.7): lệch âm/thanh thuần Việt: không/∅, không/trăm linh, không không/∅, ra một không không không/nghìn — NOT_VERIFIED bằng tai người',
    'Mười hai bằng 8 cộng 4, nên viết là 1 1 0 0, còn 10 bằng 8 cộng 2, viết là 1 0 1 0.':
        'ASR chép “12 bằng 8 cộng 4, nền viết là 1100, còn 10 bằng 8 cộng 2, viết là 1010.” (0.784): lệch âm/thanh thuần Việt: nên/nền, không không/trăm, một không/trăm mười — NOT_VERIFIED bằng tai người',
    'Hàng trên là byte cấu hình 1 0 1 1, 0 1 1 1, hàng giữa là mặt nạ 0F, bốn bit 0 rồi bốn bit 1.':
        'ASR chép “Hàng trên là bay cấu hình 1.0.1.1, 0.1.1, hàng giữa là mặt nạ 0F, 4 biệt 0 rồi 4 biệt 1.” (0.873): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: một/∅, bit/biệt, bit/biệt — NOT_VERIFIED bằng tai người',
    'Bước một, viết 12 thành bit, được 1 1 0 0, bit 1 thấp nhất nằm ở cột 4.':
        'ASR chép “Bước 1, viết 12 thành bích, được 1 màu 00, bích 1 thấp nhất, nằm ở cọc 4.” (0.769): lệch âm/thanh thuần Việt: bit/bích, một/màu, không bit/bích, cột/cọc — NOT_VERIFIED bằng tai người',
    'Bước ba, và từng cột, chỉ cột 8 có cả hai bit là 1.':
        'ASR chép “Bước 3, và từng cục, chỉ cục 8 có cả 2 bits là 1.” (0.786): lệch âm/thanh thuần Việt: cột/cục, cột/cục, bit/bits — NOT_VERIFIED bằng tai người',
    'Mặt nạ đảo đó có bit 1 ở mọi chỗ trừ bit 0, nên các bit khác giữ nguyên.':
        'ASR chép “Mặc nạ đạo đó có biết một ở mọi chỗ trừ biết không nên các biết khác giữ nguyên.” (0.737): lệch âm/thanh thuần Việt: mặt/mặc, đảo/đạo, bit/biết, bit/biết, bit/biết — NOT_VERIFIED bằng tai người',
    'Để thấy vì sao, viết 96 bằng 64 cộng 32, tức 1 1 0 0 0 0 0, còn 95 là 1 0 1 1 1 1 1.':
        'ASR chép “Để thấy vì sao, viết 96 bằng 64 cộng 32, tức 11000, còn 95 là 1011111.” (0.778): lệch âm/thanh thuần Việt: một không không không không không/nghìn, một một/∅ — NOT_VERIFIED bằng tai người',
    'Từ đó dãy chữ số 0 0 1 1 lặp lại mãi, phần lẻ không bao giờ về đúng 0.':
        'ASR chép “Từ đó dạy chữ số 0011 lặp lại mãi, phần lẽ không bao giờ về đúng không.” (0.789): lệch âm/thanh thuần Việt: dãy/dạy, không không một/mười, linh/lẽ — NOT_VERIFIED bằng tai người',
    'Hộp cột 0 nhận nhớ vào bằng 0, và với 0 1 1 1 cộng 0 1 0 1, ba bit nhớ đầu đều bằng 1, bit nhớ ra khỏi cột 3 bằng 0.':
        'ASR chép “Hộp cột không nhận nhớ vào bằng 0 và với 0111 cộng 0101, bà bịt nhớ đầu đều bằng 1, bịt nhớ ra khỏi cột 3 bằng 0.” (0.794): lệch âm/thanh thuần Việt: không/∅, một/trăm mười, không/∅, không/trăm linh, ba bit/bà bịt, bit/bịt — NOT_VERIFIED bằng tai người',
    'Bước một, với 0 1 1 1 cộng 0 1 0 1, ta lấy hàng nhớ từ bảng của phần nối tiếp nhớ.':
        'ASR chép “Bước 1, với 0111-0101, ta lấy hàng nhớ từ bảng của phần nối tiếp nhớ.” (0.756): lệch âm/thanh thuần Việt: không/một trăm mười, một cộng không một không/trăm linh — NOT_VERIFIED bằng tai người',
    'Nhớ ra khỏi cột 3 bằng 0, nên cờ C bằng 0.':
        'ASR chép “Nhớ ra khỏi cục ba bằng không nên cờ xếp bằng không.” (0.833): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: cột/cục — NOT_VERIFIED bằng tai người',
    'Nhớ vào cột 3 bằng 1 mà nhớ ra bằng 0, hai bit khác nhau, nên cờ V bằng 1.':
        'ASR chép “Nhớ vào cục 3 bằng 1 mà nhớ ra bằng 0, hay biết khác nhau, nên cờ với bằng 1.” (0.8): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: cột/cục, hai bit/hay biết — NOT_VERIFIED bằng tai người',
    'Cờ C bằng 0 nên kết quả không dấu 12 là đúng.':
        'ASR chép “VC bằng 0 nên kết quả 0 dấu 12 là đúng.” (0.88): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: cờ (trong “cờ c” → “vc”) — NOT_VERIFIED bằng tai người',
    'Cờ V bằng 1 nên kết quả có dấu bị tràn, vì 12 vượt quá 7, và máy đọc ra âm 4.':
        'ASR chép “CV bằng một nền kết quả có giấu bị tràn vì 12 vượt quá bảy và máy đọc ra âm búng.” (0.844): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: cờ (trong “cờ v” → “cv”), nên/nền, bốn/búng — NOT_VERIFIED bằng tai người',
    'Nhớ vào và nhớ ra của cột 3 đều bằng 1, giống nhau, nên cờ V bằng 0.':
        'ASR chép “Nhớ vào và nhớ ra của cục 3 đều bằng 1 giống nhau nên cờ với bằng không.” (0.889): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: cột/cục — NOT_VERIFIED bằng tai người',
    'Hai nhân 10 mũ 9 là 2 tỉ.':
        'ASR chép “2 nhân 10 mũ chính là 2 tỷ” (0.75): “tỉ” ASR viết chính tả “tỷ” (cùng âm); lệch âm/thanh thuần Việt: chín/chính — NOT_VERIFIED bằng tai người',
    'Một na-nô giây là một phần tỉ giây.':
        'ASR chép “Một nano dây là một phần tỉ dây.” (0.706): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh — NOT_VERIFIED bằng tai người',
    'Trong 3 na-nô giây, máy A làm xong 4 lệnh, còn máy B chưa xong lệnh thứ tư.':
        'ASR chép “Trong 3 nano dây, mẫy A làm xong 4 lệnh, còn mẫy B chưa xong lệnh thứ 4.” (0.757): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; lệch âm/thanh thuần Việt: máy (trong “na nô giây máy” → “nano dây mẫy”), máy/mẫy — NOT_VERIFIED bằng tai người',
    'Ở bài 0, ta biết một byte là 8 bit, nên một số thực 64 bit chiếm 8 byte.':
        'ASR chép “Ở bài 0, ta biết một bay là 8 bit, nên một số thực 64 bit chiếm 8 bay.” (0.905): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Khi lưu theo hàng, hết hàng 0 mới tới hàng 1, nên phần tử ở hàng i cột j nằm ở byte thứ i nhân 64 cộng j, tất cả nhân 8.':
        'ASR chép “Khi lưu theo hàng, hết hàng không mới tới hàng một, nền phần tự ở hàng y cục di nằm ở bay thứ y nhân 64 cộng di, tất cả nhân 8.” (0.882): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: nên/nền, tử/tự, cột/cục — NOT_VERIFIED bằng tai người',
    'Ví dụ hàng 1 cột 2 nằm ở byte thứ 528.':
        'ASR chép “Ví dụ hàng một cột hai nằm ở bai thứ 528.” (0.933): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Hình vẽ ba hàng đầu của ma trận, mỗi khung xanh là một dòng của bộ nhớ đệm, dài 64 byte, chứa 8 phần tử liền nhau.':
        'ASR chép “Hình vẽ ba hàng đầu của ma trận, mỗi khung xanh là một dòng của bộ nhớ đệm, dài 64 bai, chứa 8 phần tử liền nhau.” (0.966): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Đi theo cột, mũi tên đỏ nhảy thẳng xuống hàng kế tiếp, cách 512 byte, tức sang một dòng khác hẳn, nên lần nào cũng phải nạp dòng mới.':
        'ASR chép “Đi theo cục, mũi tên đỏ nhảy thẳng xuống hàng kế tiếp, cách 512 bay tức sang một dòng khác hẳn, nên lần nào cũng phải nạp dòng mới.” (0.938): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: cột/cục — NOT_VERIFIED bằng tai người',
    'Bước một, mỗi phần tử 8 byte, nên một dòng chứa 64 chia 8, bằng 8 phần tử.':
        'ASR chép “Bước 1, mỗi phần tử 8 bai nên 1 dòng chứa 64 chia 8, bằng 8 phần tử.” (0.95): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Bước bốn, một cột chạm tới 64 dòng khác nhau, trong khi bộ nhớ đệm 2048 byte trong mô phỏng chỉ giữ được 32 dòng.':
        'ASR chép “Bước 4, một cột chạm tới 64 dòng khác nhau trong khi bộ nhớ đệm 2048 bai trong mô phỏng chỉ giữ được 32 dòng.” (0.971): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Bộ nhớ đệm có 32 nhân 1024, bằng 32768 byte, chia cho 64 byte mỗi dòng được 512 dòng.':
        'ASR chép “Bộ nhớ đệm có 32 nhân 1.024 bằng 32.768 bài, chia cho 64 bài mỗi dòng được 512 dòng.” (0.95): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Dòng đó lưu một bit hợp lệ, một thẻ và 64 byte dữ liệu.':
        'ASR chép “Dòng đó lưu 1 bích hợp lệ, 1 thẻ và 64 bai giữ liệu.” (0.875): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: bit/bích — NOT_VERIFIED bằng tai người',
    'Cuối cùng, độ dời chọn ra byte 56 trong 64 byte của dòng.':
        'ASR chép “Cuối cùng, độ dời chọn ra bay 56 trong 64 bay của dòng.” (0.882): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Bước một, lấy 6 bit thấp bằng phép và với 63, được độ dời 56, vì byte thấp nhất là 78 hệ mười sáu, tức 120.':
        'ASR chép “Bước 1, lấy 6 bit thấp bằng phết và với 63, được độ dời 56, vị bay thấp nhất là 78 hệ 16, tức 120.” (0.914): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: phép/phết, vì (trong “vì byte” → “vị bay”) — NOT_VERIFIED bằng tai người',
    'Khi trúng, độ dời 56 chọn ra đúng byte cần đọc.':
        'ASR chép “Khi trúng, độ dời 56 chọn ra đúng vai cần đọc.” (0.923): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Vì mỗi giá trị thẻ ứng với 32768 byte và mỗi dòng ứng với 64 byte, ta ghép ngược lại được.':
        'ASR chép “Vì mỗi giá trị thể ứng với 32.768 bai và mỗi dòng ứng với 64 bai, ta ghép ngược lại được.” (0.903): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: thẻ/thể — NOT_VERIFIED bằng tai người',
    'Bộ nhớ đệm có 8 nhân 1024, bằng 8192 byte, chia 32 bằng 256 dòng.':
        'ASR chép “Bộ nhớ đệm có 8 nhân 1.024 bằng 8.192 bài, chia 32 bằng 256 dòng.” (0.97): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Nhắc lại, số khối là địa chỉ chia cho kích thước dòng, ví dụ địa chỉ 320 với dòng 64 byte là khối 5.':
        'ASR chép “Nhắc lại, số khối là địa chỉ chia cho kích thước dòng, ví dụ địa chỉ 320 với dòng 64b là khối 5.” (0.966): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Kiểm bằng đường khác, ta không dịch bit mà chia trong hệ mười, vì trang dài 4096 byte nên số trang chính là thương của phép chia cho 4096.':
        'ASR chép “Kiểm bằng đường khác, ta không dịch bích mà chia trong hệ 10 vì trang dại 4.096 bài nên số trang chính là thương của phép chia cho 4.096.” (0.927): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: bit/bích, dài/dại — NOT_VERIFIED bằng tai người',
    'Số dư 2748 đúng bằng A B C hệ mười sáu, tức độ dời.':
        'ASR chép “số dư 2.748 đúng bằng AVC hệ 16, tức độ dơi.” (0.842): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: dời/dơi — NOT_VERIFIED bằng tai người',
    'Ở bài 0, ta đã biết một byte gồm 8 bit.':
        'ASR chép “Ở bài không, ta đã biết một bay gồm 8 bit.” (0.909): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Vì vậy mạng 1 tỉ bit mỗi giây chở được 10 mũ 9 chia 8, bằng 125 triệu byte mỗi giây.':
        'ASR chép “Vì vậy mạng 1 tỷ biết mỗi giây chở được 10 mũ 9 chia 8 bằng 125 triệu bay mỗi giây.” (0.88): “tỉ” ASR viết chính tả “tỷ” (cùng âm); byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: bit (trong “tỉ bit” → “tỷ biết”) — NOT_VERIFIED bằng tai người',
    'Mỗi khối 4096 byte, nên số ngắt là 100 triệu chia 4096, khoảng 24414 ngắt mỗi giây.':
        'ASR chép “Mỗi khối 4.096 bai, nền số ngắt là 100 triệu chia 4.096, khoảng 24.414 ngắt mỗi giây.” (0.946): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: nên (trong “byte nên” → “bai nền”) — NOT_VERIFIED bằng tai người',
    'Kiểm bằng đường khác, ta đếm số byte tới trong lúc xử lý một ngắt, thay vì đếm ngắt mỗi giây.':
        'ASR chép “Kiểm bằng đường khác, ta đếm số bay tới trong lúc xử lý một ngắt, thay vì đếm ngắt mỗi giây.” (0.952): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Trong 2 phần triệu giây, ổ đĩa đã đưa tới 10 mũ 8 nhân 2 nhân 10 mũ âm 6, bằng 200 byte.':
        'ASR chép “Trong 2 phần triệu dây, ổ địa đã đưa tới 10 mũ 8 nhân 2 nhân 10 mũ âm 6 bằng 200 bay.” (0.917): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: đĩa/địa — NOT_VERIFIED bằng tai người',
    'Ngắt mỗi 16 byte thì trong lúc xử lý một ngắt đã có 200 chia 16, bằng 12 phẩy 5 ngắt mới dồn tới, nên cần 12 phẩy 5 bộ xử lý, khớp bước hai.':
        'ASR chép “Ngắt mỗi 16 bài thì trong lúc sử lý 1 ngắt đã có 216 bằng 12,5 ngắt mới dồn tới, nên cần 12,5 bộ sử lý, khớp bước 2.” (0.962): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: chia/∅ — NOT_VERIFIED bằng tai người',
    'Với khối 4096 byte, một ngắt đến sau 4096 chia 200, bằng 20 phẩy 48 lần thời gian xử lý.':
        'ASR chép “Với khối 4.096-1 ngắt đến sau 4.096-200 bằng 20,48 lần thời gian xử lý.” (0.971): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: chia/∅ — NOT_VERIFIED bằng tai người',
    'Chia cho 1500 byte mỗi gói được khoảng 83 nghìn gói mỗi giây.':
        'ASR chép “chia cho 1.500 bai mỗi gói được khoảng 83.000 gói mỗi dây.” (0.944): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    # ── Đợt B đào sâu: OSY ──
    'Một mi li giây là một phần nghìn giây.':
        'ASR chép “Một mili dây là một phần nghìn dây.” (0.706): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh — NOT_VERIFIED bằng tai người',
    'Gom vào bộ đệm 4096 byte rồi mới ghi thì chỉ cần 15 nghìn 625 lời gọi, khoảng 0 phẩy 016 giây, ít hơn 64 lần.':
        'ASR chép “Gom vào bộ đệm 4.096 bai rồi mới ghi thì chỉ cần 15.625 lời gọi, khoảng 0.016 giây, ít hơn 64 lần.” (0.949): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; lệch âm/thanh thuần Việt: không (trong “không phẩy” → “”) — NOT_VERIFIED bằng tai người',
    'Lỗi thứ năm, nghĩ lỗi trong nhân chỉ làm hỏng một chương trình.':
        'ASR chép “Lội thứ 5. Nghỉ lỗi trong nhân chỉ làm hổng một chương trình.” (0.769): lệch âm/thanh thuần Việt: lỗi/lội, nghĩ/nghỉ, hỏng/hổng — NOT_VERIFIED bằng tai người',
    'Bắt đầu từ 1, nhân 2 được 2, nhân 2 nữa được 4, nhân 2 lần nữa được 8.':
        'ASR chép “Bắt đầu từ một, nhần hai được hai, nhần hai nửa được bốn, nhần hai lần nữa được tám.” (0.789): lệch âm/thanh thuần Việt: nhân/nhần, nhân/nhần, nữa/nửa, nhân/nhần — NOT_VERIFIED bằng tai người',
    'Lỗi thứ tư, chỉ nhìn con số trung bình.':
        'ASR chép “Lội thứ 4, triển nhìn con số trung bình.” (0.778): lệch âm/thanh thuần Việt: lỗi/lội, chỉ/triển — NOT_VERIFIED bằng tai người',
    'Vậy x cuối chỉ bằng 1, mất một lần cộng của A.':
        'ASR chép “Vậy ít cuối chỉ bằng một, mất một lần cộng qua.” (0.87): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: của (trong “của a” → “qua”) — NOT_VERIFIED bằng tai người',
    'Bây giờ dò từng lệnh bằng số.':
        'ASR chép “Bây giờ do từng lệnh băng số.” (0.714): lệch âm/thanh thuần Việt: dò/do, bằng/băng — NOT_VERIFIED bằng tai người',
    'Cách một, cộng hai bộ đếm ở mỗi dòng đã dò, 5 với 0, 4 với 1, cho tới 0 với 5, lúc nào cũng được 5, đúng bằng số ô.':
        'ASR chép “Cách 1, cộng 2 bộ đếm ở mũi dòng đã giò 5 với 0, 4 với 1, cho tới 0 với 5, lúc nào cũng được 5, đúng bằng số ố.” (0.935): “ô” (ô lưới) ASR viết chữ “O”; lệch âm/thanh thuần Việt: mỗi/mũi — NOT_VERIFIED bằng tai người',
    'Bảng nhắc lại hai kết quả đó của máy với bản đảo thứ tự, quầy 5 ô.':
        'ASR chép “Bạn nhắc lại hai kết quả đó của máy với bảng đạo thứ tự, quầy 5 ohm.” (0.765): “ô” (ô lưới) ASR viết chữ “O”; lệch âm/thanh thuần Việt: bảng/bạn, bản đảo/bảng đạo — NOT_VERIFIED bằng tai người',
    'Tiến trình 1 giữ một R2 và xin một R1, tiến trình 2 giữ một R1 và xin một R2.':
        'ASR chép “Tiến trình 1 giữ 1 Eder 2 và sinh 1 Eder 1, tiến trình 2 giữ 1 Eder 1 và sinh 1 Eder 2.” (0.75): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: xin/sinh, xin/sinh — NOT_VERIFIED bằng tai người',
    'Tiến trình 2 chạy xong và trả một R1, nên phần trống thành 2 và 1.':
        'ASR chép “Tiến trình 2 chạy xong và trả 1 error 1 nên phần trống thành 2 và 1.” (0.941): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Thử lại, luồng B giờ phải xin khoá 1 trước, mà khoá 1 đang ở chỗ A, nên B đứng đợi khi chưa giữ gì cả.':
        'ASR chép “Thử lại, luôn bây giờ phải sinh khóa một trước mà khóa một đang ở chỗ A nên bê đứng đợi khi chưa giữ gì cả.” (0.885): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: luồng (trong “luồng b” → “luôn bây”), xin/sinh — NOT_VERIFIED bằng tai người',
    'Cấp nốt 2 cho tiến trình a, nó chạy xong và trả lại cả 6 thể hiện, nên còn rảnh thành 3 trừ 2 cộng 6, bằng 7.':
        'ASR chép “Cấp nút 2 cho tiến trình nha, nó chạy xong và trả lại cả 6 thể hiện, nên còn rảnh thành 3 trừ 2,6 bằng 7.” (0.893): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: nốt/nút, cộng/phẩy — NOT_VERIFIED bằng tai người',
    'Mấu chốt là ở đây, phần trả lại làm kho đầy lên, và tiến trình b giờ cần thêm 5, không vượt 7, nên cũng chạy xong.':
        'ASR chép “Mấu chốt là ở đây, phần trả lại làm kho đầy lên và tiến trình bây giờ cần thêm 5, không vượt 7, nền cũng chạy xong.” (0.926): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: nên/nền — NOT_VERIFIED bằng tai người',
    'Muốn chứa 72766 byte bằng các khối 4096 byte, thử 17 khối thì được 17 nhân 4096 bằng 69632, nhỏ hơn 72766, chưa đủ.':
        'ASR chép “Muốn chứa 72,766 bài bằng các khối 4,096 bài, thử 17 khối thì được 17 nhân 4,096 bằng 69,632, nhỏ hơn 72,766, chưa đủ.” (0.968): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Bảng dò từng bước ví dụ đó.':
        'ASR chép “Bản do từng bước ví dụ đó.” (0.714): lệch âm/thanh thuần Việt: bảng dò/bản do — NOT_VERIFIED bằng tai người',
    'Nếu lệch mốc, vùng nhớ chạm 3 bảng con, tổng cộng 16 KiB.':
        'ASR chép “Nếu lệch móc, vùng nhớ chạm 3 bảng con, tổng cộng 16 kilobytes.” (0.857): lệch âm/thanh thuần Việt: mốc/móc; KiB/MiB/TiB đọc theo lexicon_vi.OSY.yaml (“ki-lô-byte”, “mê-ga-byte”, “tê-ra-byte”), ASR chép “kilobyte/MB/TB/terabyte” hoặc tách “kg bay” — đúng đơn vị, chỉ khác cách viết — NOT_VERIFIED bằng tai người',
    'Chia 14975 cho 4096, vì mỗi trang 4096 byte, được phần nguyên 3, đó là số trang.':
        'ASR chép “Chia 14.975 cho 4.096 vì mỗi tràn 4.096 bay được phần nguyên 3, đó là số trang.” (0.944): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: trang/tràn — NOT_VERIFIED bằng tai người',
    'Bảng cho thấy 2 trang chỉ chứa 8192 byte, chưa đủ, còn 3 trang chứa 12288 byte, thừa 2288.':
        'ASR chép “Bản cho thấy hai trang chỉ chứa 8.192 bai, chưa đủ, còn ba trang chứa 12.288 bai, thừa 2.288.” (0.921): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: bảng/bản — NOT_VERIFIED bằng tai người',
    'Mười bit giữa chỉ có bit cuối bằng 1, nên chỉ số bảng con là 1.':
        'ASR chép “Mười biết giữ chỉ có biết cuối bằng một, nên chỉ số bản con là một.” (0.75): lệch âm/thanh thuần Việt: bit giữa/biết giữ, bit/biết, bảng/bản — NOT_VERIFIED bằng tai người',
    'Trước hết, ta nhắc lại bài 9, nơi chương trình được cắt thành các mẩu bằng nhau gọi là trang, mỗi trang 4 KiB.':
        'ASR chép “Trước hết, ta nhắc lại bài chính nơi chương trình được cắt thành các mẫu bằng nhau gọi là trang, mỗi trang 4 kilobyte.” (0.875): lệch âm/thanh thuần Việt: chín/chính, mẩu/mẫu; KiB/MiB/TiB đọc theo lexicon_vi.OSY.yaml (“ki-lô-byte”, “mê-ga-byte”, “tê-ra-byte”), ASR chép “kilobyte/MB/TB/terabyte” hoặc tách “kg bay” — đúng đơn vị, chỉ khác cách viết — NOT_VERIFIED bằng tai người',
    'Có 1 lần lỗi, mất 8 triệu na-nô giây.':
        'ASR chép “Có một lần lỗi, mất 8 triệu nano dây.” (0.737): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh — NOT_VERIFIED bằng tai người',
    'Một KiB bằng 2 mũ 10, tức 1024 byte.':
        'ASR chép “1 kg bay bằng 2 mũ 10, tức 1.024 bay.” (0.839): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); KiB/MiB/TiB đọc theo lexicon_vi.OSY.yaml (“ki-lô-byte”, “mê-ga-byte”, “tê-ra-byte”), ASR chép “kilobyte/MB/TB/terabyte” hoặc tách “kg bay” — đúng đơn vị, chỉ khác cách viết — NOT_VERIFIED bằng tai người',
    'Bốn KiB bằng 2 mũ 12, tức 4096 byte, còn MiB và TiB là 2 mũ 20 và 2 mũ 40, mỗi bậc gấp 1024 lần bậc trước.':
        'ASR chép “4 kilobyte bằng 2 mũ 12, tức 4.096 byte, còn megabyte và terabyte là 2 mũ 20 và 2 mũ 40, mỗi bật cấp 1.024 lần bật trước.” (0.86): MiB đọc “mê-ga-byte” (quy ước OSY/DEN: cách nói thông dụng, màn hình giữ MiB, câu nêu rõ 2 mũ 20), ASR viết “MB”; lệch âm/thanh thuần Việt: bậc gấp/bật cấp, bậc/bật; KiB/MiB/TiB đọc theo lexicon_vi.OSY.yaml (“ki-lô-byte”, “mê-ga-byte”, “tê-ra-byte”), ASR chép “kilobyte/MB/TB/terabyte” hoặc tách “kg bay” — đúng đơn vị, chỉ khác cách viết — NOT_VERIFIED bằng tai người',
    'Điều thứ hai, các khối của một tệp được đánh số từ 0, và byte ở vị trí x nằm ở khối có số bằng phần nguyên của x chia cho cỡ khối.':
        'ASR chép “Điều thứ hai, các khối của một tệch được đánh số từ 0 và bay ở vị trí x nằm ở khối có số bằng phần nguyên của x chia cho cỡ khối.” (0.939): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: tệp/tệch — NOT_VERIFIED bằng tai người',
    'Ví dụ vị trí 40 KiB là 40960 byte, chia 4096 được đúng 10, nên byte đó nằm ở khối số 10, tức là khối thứ mười một.':
        'ASR chép “Ví dụ vị trí 40 kilobyte là 40.960 bay, chia 4.096 được đúng 10, nên bay đó nằm ở khối số 10, tức là khối thứ 11.” (0.927): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); KiB/MiB/TiB đọc theo lexicon_vi.OSY.yaml (“ki-lô-byte”, “mê-ga-byte”, “tê-ra-byte”), ASR chép “kilobyte/MB/TB/terabyte” hoặc tách “kg bay” — đúng đơn vị, chỉ khác cách viết — NOT_VERIFIED bằng tai người',
    'Bước một, phần trực tiếp là 12 khối, còn gián tiếp đơn phủ 1024 khối, vì một khối 4096 byte chia cho 4 byte mỗi con trỏ được 1024 con trỏ.':
        'ASR chép “Bước 1, phần trực tiếp là 12 khối, còn dán tiếp đơn phủ 1024 khối, vì 1 khối 4096 bài chia cho 4 bài mỗi con trỏ được 1024 con trỏ.” (0.96): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Bước năm, đổi số khối ra byte rồi ra TiB.':
        'ASR chép “Bước 5, đổi số khối ra byte rồi ra terabyte.” (0.9): KiB/MiB/TiB đọc theo lexicon_vi.OSY.yaml (“ki-lô-byte”, “mê-ga-byte”, “tê-ra-byte”), ASR chép “kilobyte/MB/TB/terabyte” hoặc tách “kg bay” — đúng đơn vị, chỉ khác cách viết — NOT_VERIFIED bằng tai người',
    'Tầng gián tiếp ba cho 2 mũ 42 byte, đúng 4 TiB.':
        'ASR chép “Tần gián tiếp 3 cho 2 mũ 42 bay, đúng 4 tê ra bay.” (0.812): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: tầng/tần — NOT_VERIFIED bằng tai người',
    'Tầng gián tiếp đôi cho 2 mũ 32 byte, chia 2 mũ 40 được 1 phần 256, khoảng 0 phẩy 0039 TiB.':
        'ASR chép “Tần gián tiếp đôi cho hai mũ 32B, chia hai mũ 40 được một phần 256, khoảng 0.0039TB.” (0.885): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; lệch âm/thanh thuần Việt: tầng/tần; KiB/MiB/TiB đọc theo lexicon_vi.OSY.yaml (“ki-lô-byte”, “mê-ga-byte”, “tê-ra-byte”), ASR chép “kilobyte/MB/TB/terabyte” hoặc tách “kg bay” — đúng đơn vị, chỉ khác cách viết — NOT_VERIFIED bằng tai người',
    'Phần gián tiếp đơn và trực tiếp chỉ khoảng 4 MiB, nhỏ tới mức chỉ đóng góp chừng 4 phần triệu TiB.':
        'ASR chép “Phần gián tiếp đơn và trực tiếp chỉ khoảng 4 MB, nhỏ tới mức chỉ đóng góp chừng 4 phần triệu TB.” (0.909): MiB đọc “mê-ga-byte” (quy ước OSY/DEN: cách nói thông dụng, màn hình giữ MiB, câu nêu rõ 2 mũ 20), ASR viết “MB”; KiB/MiB/TiB đọc theo lexicon_vi.OSY.yaml (“ki-lô-byte”, “mê-ga-byte”, “tê-ra-byte”), ASR chép “kilobyte/MB/TB/terabyte” hoặc tách “kg bay” — đúng đơn vị, chỉ khác cách viết — NOT_VERIFIED bằng tai người',
    'Cụ thể, 256 bình phương bằng 65536, cộng thêm 266 được 65802 khối, mỗi khối 1 KiB, nên chia 1024 được khoảng 64 phẩy 26 MiB.':
        'ASR chép “Cụ thể, 256 bình phương bằng 65,536, cộng thêm 266 được 65,802 khối, mỗi khối 1 kilobyte, nên chi 1.024 được khoảng 64,26 MB.” (0.949): MiB đọc “mê-ga-byte” (quy ước OSY/DEN: cách nói thông dụng, màn hình giữ MiB, câu nêu rõ 2 mũ 20), ASR viết “MB”; lệch âm/thanh thuần Việt: chia/chi; KiB/MiB/TiB đọc theo lexicon_vi.OSY.yaml (“ki-lô-byte”, “mê-ga-byte”, “tê-ra-byte”), ASR chép “kilobyte/MB/TB/terabyte” hoặc tách “kg bay” — đúng đơn vị, chỉ khác cách viết — NOT_VERIFIED bằng tai người',
    'Từng bước, vì khối 1 KiB nên byte ở vị trí 300 KiB nằm ở khối số 300.':
        'ASR chép “Từng bước vì khối 1 kilobyte nên bay ở vị trí 300 kilobyte nằm ở khối số 300.” (0.85): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); KiB/MiB/TiB đọc theo lexicon_vi.OSY.yaml (“ki-lô-byte”, “mê-ga-byte”, “tê-ra-byte”), ASR chép “kilobyte/MB/TB/terabyte” hoặc tách “kg bay” — đúng đơn vị, chỉ khác cách viết — NOT_VERIFIED bằng tai người',
    'Số 7 bằng 4 cộng 2 cộng 1, tức ba bit 1, 1, 1, là r w x.':
        'ASR chép “Số 7 bằng 4 cộng 2 cộng 1, tức 3 bit 1, 1, 1 là rv kết x.” (0.947): chữ w đọc “vê kép” (luật chung), ASR viết tách chữ — NOT_VERIFIED bằng tai người',
    # ── Đợt B đào sâu: DMS ──
    'Từ điểm bắt đầu, p tách thành hai nhánh, đúng hoặc sai, rồi ở mỗi nhánh q lại tách đôi, nên có 2 nhân 2, bằng 4 lá, mỗi lá là một dòng của bảng.':
        'ASR chép “Từ điểm bắt đầu, t tách thành hai nhánh, đúng hoặc sai, rồi ở mỗi nhánh quy lại tắt đôi, nền có hai nhân hai, bằng bốn lá, mỗi lá là một dòng của bảng.” (0.914): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: tách/tắt, nên/nền — NOT_VERIFIED bằng tai người',
    'Đường khác thứ hai, đếm lại công thức 2 mũ 3 bằng cách liệt kê ba mệnh đề p, q, r.':
        'ASR chép “Đường khác thứ hai, đếm lại công thức hai mũ ba bằng cách liệt kê ba mệnh DP, Q, R.” (0.927): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: đề (trong “đề p” → “dp”) — NOT_VERIFIED bằng tai người',
    'P kéo theo q sai, vì đây đúng là trường hợp vế đầu đúng mà vế sau sai.':
        'ASR chép “Tề kéo theo quy sai, vì đây đúng là trường hợp với đầu đúng mà với sau sai.” (0.833): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: vế/với, vế/với — NOT_VERIFIED bằng tai người',
    'Chỉ ô xanh ở góc trên trái được vào, ba ô đỏ còn lại phải bị chặn, và ba ô đó chính là thiếu tuổi hoặc thiếu vé, đúng như luật De Morgan nói.':
        'ASR chép “Chỉ ô xanh ở góc trên trái được vào, 3 ô đỏ còn lại phải bị chặn, và 3 ô đó chính là thiếu tuổi hoặc thiếu vé, đúng như luật đơ Morgan nói.” (0.971): lệch âm/thanh thuần Việt: de/đơ — NOT_VERIFIED bằng tai người',
    'Đáp án câu một, bước một, theo De Morgan, phủ định của hoặc là và của hai phủ định.':
        'ASR chép “Đáp án câu một, bước một, theo đơ mor gần, phủ định của hoặc là và của hai phủ định.” (0.95): lệch âm/thanh thuần Việt: mo/mor — NOT_VERIFIED bằng tai người',
    'Việc thứ hai là luật De Morgan đã học ở bài 1, phủ định của phép và là phép hoặc của hai phủ định.':
        'ASR chép “Việc thứ hai là luật đơ Morgan đã học ở bài một, phủ định của phép và là phép hoặc của hai phủ định.” (0.958): lệch âm/thanh thuần Việt: de/đơ — NOT_VERIFIED bằng tai người',
    'Câu với mọi là phép và của tất cả các ô, nên chỉ một ô đỏ là đủ làm cả câu sai.':
        'ASR chép “Câu với mọi là phép và của tất cả các cô, nền chỉ một ô đỏ là đủ làm cả câu sai.” (0.909): “ô” (ô lưới) ASR viết chữ “O”; lệch âm/thanh thuần Việt: nên (trong “ô nên” → “cô nền”) — NOT_VERIFIED bằng tai người',
    'Mỗi số đều nằm kẹp giữa hai số chính phương liền nhau, ví dụ 50 nằm giữa 49 và 64, nên không có a nguyên nào.':
        'ASR chép “Mỗi số đời nằm kẹp giữa hai số chính phương liền nhau, ví dụ 50 nằm giữa 49 và 64, nên không có an nguyên nào.” (0.935): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: đều/đời — NOT_VERIFIED bằng tai người',
    'Thứ hai là xem một hiệu chẵn hay lẻ.':
        'ASR chép “Thứ hai là xem một hiệu chẳng hay lẽ.” (0.778): lệch âm/thanh thuần Việt: chẵn/chẳng, linh/lẽ — NOT_VERIFIED bằng tai người',
    'Câu hai, phản xạ đòi hỏi a nhỏ hơn hẳn chính a, điều này sai với mọi a, ví dụ 0 không nhỏ hơn 0, nên không phản xạ.':
        'ASR chép “Câu 2, phản xạ đòi hỏi ai nhỏ hơn hẳn chính A, điều này sai với mọi A, ví dụ 0 không nhỏ hơn 0, nên không phản xạ” (0.966): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Tiếp theo, ôn tính bắc cầu ở bài 7, a R b và b R c thì a R c.':
        'ASR chép “Tiếp theo, ông tính bắt cầu ở bài bẫy A, B và B, R, C thì A, L, C.” (0.769): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: ôn/ông, bắc/bắt, bảy/bẫy — NOT_VERIFIED bằng tai người',
    'Bước một, nắm luật.':
        'ASR chép “Bước 1. Nắm lực” (0.75): lệch âm/thanh thuần Việt: luật/lực — NOT_VERIFIED bằng tai người',
    'Công cụ thứ hai là phá ngoặc, nhân mỗi số hạng của ngoặc đầu với mỗi số hạng của ngoặc sau.':
        'ASR chép “Công cụ thứ hai là phá hoặc, nhân mỗi số hạng cuốn hoặc đầu với mỗi số hạng cuốn hoặc sau.” (0.762): lệch âm/thanh thuần Việt: ngoặc/hoặc, của ngoặc/cuốn hoặc, của ngoặc/cuốn hoặc — NOT_VERIFIED bằng tai người',
    'Thử với 4 người, cố định người 1 và 2 thì chỉ còn hai cách, A B C D và A B D C, đúng bằng 2 giai thừa chứ không phải 6.':
        'ASR chép “Thử với 4 người, cố định người 1 và 2 thì chỉ còn 2 cách ABCG và ABCC, đúng bằng 2 dai thừa chứ không phải 6.” (0.833): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Hình này cho thấy Fermat nhỏ hoạt động thế nào.':
        'ASR chép “Hình này cho thấy FACMA nhỏ hoạt động thế nào?” (0.9): lệch âm/thanh thuần Việt: fermat/facma — NOT_VERIFIED bằng tai người',
    'Kiểm ví dụ bằng một đường khác hẳn, lũy thừa nhanh, không dùng Fermat.':
        'ASR chép “Kiểm ví dụ bằng một đường khác hẳn, lũy thừa nhanh, không dùng phét ma.” (0.933): lệch âm/thanh thuần Việt: phéc/phét — NOT_VERIFIED bằng tai người',
    'Ba mươi hai bằng 4 lần 7 cộng 4, nên dư 4, khớp với cách dùng Fermat.':
        'ASR chép “32 bằng 4 lần 7 cộng 4, nên dư 4, khớp với cách dùng phét ma.” (0.944): lệch âm/thanh thuần Việt: phéc/phét — NOT_VERIFIED bằng tai người',
    'Theo công thức Cayley, số mạng như thế là 10 mũ 8, tức 100 triệu cách.':
        'ASR chép “Theo công thức kê ly, số mạng như thế là 10 mũ 8, tức 100 triệu cách.” (0.944): “Cayley” đọc theo lexicon_vi.DMS.yaml là “Kê-li” (probe p1_ten 8/8), ASR viết “kê ly” — đúng âm, chỉ khác cách viết — NOT_VERIFIED bằng tai người',
    'Vì cần chắc chắn, ta tìm đường thứ ba để ra con số 16, không dùng công thức Cayley, cũng không dùng hình dạng.':
        'ASR chép “Vì cần chắc chắn, ta tìm đường thứ 3 để ra con số 16, không dùng công thức kê ly, cũng không dùng hình dạng.” (0.962): “Cayley” đọc theo lexicon_vi.DMS.yaml là “Kê-li” (probe p1_ten 8/8), ASR viết “kê ly” — đúng âm, chỉ khác cách viết — NOT_VERIFIED bằng tai người',
    'Bước hai, theo công thức Euler, số mặt F bằng 2 trừ V cộng E, thay vào ta được 3 nhân 2 trừ V cộng E, nhỏ hơn hoặc bằng 2E.':
        'ASR chép “Bước 2, theo công thức ơ lê, số mặt F bằng 2 trừ v cộng E, thay vào ta được ba nhân 2 trừ v cộng E, nhỏ hơn hoặc bằng 2 E.” (0.97): lệch âm/thanh thuần Việt: le/lê — NOT_VERIFIED bằng tai người',
    'Câu hai, từ công thức Euler, chuyển vế để tìm số mặt, F bằng 2 trừ V cộng E, tức 2 trừ 8 cộng 12, bằng 6 mặt.':
        'ASR chép “Câu 2, từ công thức OLE, chuyển vế để tìm số mặt, F bằng 2 trừ V cộng E, tức 2 trừ 8 cộng 12, bằng 6 mặt.” (0.966): lệch âm/thanh thuần Việt: euler/ole — NOT_VERIFIED bằng tai người',
    # ── Đợt B đào sâu: TOC ──
    'Gốc ở trên cùng, ghi chữ rỗng, là chuỗi rỗng.':
        'ASR chép “Gốc ở trên cùng ghi chữ trỏng là chuổi trỏng.” (0.7): lệch âm/thanh thuần Việt: rỗng/trỏng, chuỗi rỗng/chuổi trỏng — NOT_VERIFIED bằng tai người',
    'Liệt kê ra để kiểm, 1 cộng 3 cộng 3 cộng 1 bằng 8, khớp với 2 mũ 3.':
        'ASR chép “Li kê ra để kiểm 1 cọng 3 cọng 3 cọng 1 bằng 8 khớp với 2 mũ 3.” (0.789): lệch âm/thanh thuần Việt: liệt/li, cộng/cọng, cộng/cọng, cộng/cọng — NOT_VERIFIED bằng tai người',
    'Từ A, C đọc 1 về tập A.':
        'ASR chép “Từ A, sẽ đọc một về tập A.” (0.875): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Đây đúng là điều định lý Kleene hứa, hai cách mô tả cho cùng câu trả lời trên mọi chuỗi.':
        'ASR chép “Đây đúng là điều định lý Clooney hứa, hai cách mô tả cho cùng câu trả lời trên mọi chuỗi.” (0.95): “Kleene” đọc “Cờ-li-ni” theo lexicon_vi.TOC.yaml (probe 7/8), ASR viết thành tên “Clooney/Clini” — chỉ khác cách viết tên riêng — NOT_VERIFIED bằng tai người',
    'Chuỗi 0 1 0 1 không có hai chữ 1 liền nhau, nên không khớp, đúng như mong muốn.':
        'ASR chép “Chủi 0101 không có hai chữ một liền nhau, nền không khớp, đúng như mong muốn.” (0.789): lệch âm/thanh thuần Việt: chuỗi không/chủi, không/trăm linh, nên/nền — NOT_VERIFIED bằng tai người',
    'Chuỗi 0 1 1 0 chia được thành hai cặp, nên khớp.':
        'ASR chép “Chủi 011 không chia được thành hai cặp, nên khớp.” (0.783): lệch âm/thanh thuần Việt: chuỗi không một/chủi mười — NOT_VERIFIED bằng tai người',
    'Điều thứ nhất là nguyên lý chuồng bồ câu.':
        'ASR chép “Điều thứ nhất là nguyên lý chùng bộ câu.” (0.778): lệch âm/thanh thuần Việt: chuồng bồ/chùng bộ — NOT_VERIFIED bằng tai người',
    'Với x là 1 và z là 1, ghép x, y mũ 2 rồi z được 1 0 0 0 0 1.':
        'ASR chép “Với x là 1 và jack là 1, get x, y mũ 2 đổi jack được 1-0-0-0-1.” (0.791): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: ghép/get, rồi (trong “rồi z” → “đổi jack”), không/∅ — NOT_VERIFIED bằng tai người',
    'Điều này mâu thuẫn với bổ đề, vậy L không chính quy.':
        'ASR chép “Điều này mâu thuận với bổ đề, vậy L09 quy.” (0.783): lệch âm/thanh thuần Việt: thuẫn/thuận, không chính/chín — NOT_VERIFIED bằng tai người',
    'Xuất phát từ trạng thái chẵn và đọc 1 0 1, máy đi chẵn, lẻ, lẻ, chẵn, nên nhận.':
        'ASR chép “Xuất phát từ trạng thái chẳng và đọc 101. Máy đi chẳng, lẻ, lẻ, chẳng, nên nhận.” (0.769): lệch âm/thanh thuần Việt: chẵn/chẳng, không/trăm linh, chẵn/chẳng, chẵn/chẳng — NOT_VERIFIED bằng tai người',
    'Kết quả, 5 trong 6 cặp bị đánh dấu, chỉ còn một cặp trống là s với c.':
        'ASR chép “Kết quả, 5 trong 6 cặp bị đánh dấu, chỉ còn 1 cặp trống là F với C.” (0.944): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Không chuỗi nào cho kết quả khác nhau, nên khớp với kết luận gộp s với c.':
        'ASR chép “không chuổi nào cho kết quả khác nhau, nên khớp với kết luận gột F với C.” (0.824): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: chuỗi/chuổi, gộp (trong “gộp s” → “gột f”) — NOT_VERIFIED bằng tai người',
    'Đây cũng chính là cách văn phạm sinh chuỗi, vì quy tắc mở ngoặc S đóng ngoặc S tách đúng tại chỗ đó.':
        'ASR chép “Đây cũng chính là cách văn phạm sinh chuỗi vì quy tắc mở hoặc ép đóng hoặc ép tách đúng tại chỗ đó.” (0.826): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: ngoặc (trong “ngoặc s” → “hoặc ép”), ngoặc (trong “ngoặc s” → “hoặc ép”) — NOT_VERIFIED bằng tai người',
    'Bước hai, biến T bên phải phải sinh ra 2 nhân 3, nên dùng quy tắc T sinh ra T nhân F.':
        'ASR chép “Bước 2, biến tệ bên phải phải sinh ra 2 nhân 3, nền dùng quy tắc t sinh ra t nhân f.” (0.909): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: nên/nền — NOT_VERIFIED bằng tai người',
    'Biến T đầu tiên đi qua F để ra số 2.':
        'ASR chép “Biến tây đầu tiên đi qua F để ra số 2.” (0.909): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Ở bài 4, bổ đề bơm cho thấy không ô-tô-mát hữu hạn nào nhận được ngôn ngữ n chữ 0 rồi n chữ 1.':
        'ASR chép “Ở bài 4, bổ đề bơm cho thấy không automa khử hạn nào nhận được ngôn ngữ N chữ không rồi N chữ 1.” (0.88): “ô-tô-mát” ASR viết “automa” (đúng thuật ngữ, khác cách viết); hữu/khử lệch phụ âm đầu — NOT_VERIFIED bằng tai người',
    'Hết chuỗi đúng lúc ngăn xếp rỗng, nên máy nhận chuỗi 0 0 1 1.':
        'ASR chép “Hết chuỗi đúng lúc ngăn xếp rỏng, nên máy nhận chuỗi 0011.” (0.786): lệch âm/thanh thuần Việt: rỗng/rỏng, không không/mười, một/∅ — NOT_VERIFIED bằng tai người',
    'Trước hết, ôn lại máy Turing của bài 9.':
        'ASR chép “Trước hết, ôn lại máy tô trinh của bài 9.” (0.842): “Turing” đọc “Tua-rinh” theo lexicon_vi.TOC.yaml (cách viết tốt nhất trong probe, 6/8), ASR viết “tô trinh/tu trinh” — NOT_VERIFIED bằng tai người',
    'Vòng lặp này chạy tới khi không còn dòng nào khớp, đó là lúc M dừng.':
        'ASR chép “Vòng lập này chạy tới khi không còn dòng nào khớp, đó là lúc em mơ dừng.” (0.848): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: lặp/lập — NOT_VERIFIED bằng tai người',
    'Bước ba, ô 2 có chữ 1, ghi 0, băng thành 0 1 0 1.':
        'ASR chép “Bước 3, O2 có chữ một, ghi không, băng thành 0101.” (0.8): “ô” (ô lưới) ASR viết chữ “O”; lệch âm/thanh thuần Việt: không/∅, không/trăm linh — NOT_VERIFIED bằng tai người',
    'Đáp án câu một, tra bảng từng vòng.':
        'ASR chép “Đáp án câu một, tra bản từng vong.” (0.75): lệch âm/thanh thuần Việt: bảng/bản, vòng/vong — NOT_VERIFIED bằng tai người',
    'Vòng một, ô 0 có chữ 0, ghi 1, băng thành 1 1 1 0.':
        'ASR chép “Vòng một, ồ không có chữ không, ghi một, băng thành 1110.” (0.774): “ô” (ô lưới) ASR viết chữ “O”; lệch âm/thanh thuần Việt: một không/trăm mười — NOT_VERIFIED bằng tai người',
    'Vòng ba, ô 2 có chữ 1, ghi 0, băng thành 1 0 0 0.':
        'ASR chép “Vòng 3, O2 có chữ 1, ghi không, ban thành 1-0-0-0.” (0.867): “ô” (ô lưới) ASR viết chữ “O”; lệch âm/thanh thuần Việt: băng/ban — NOT_VERIFIED bằng tai người',
    'Vòng năm gặp ô trống thì dừng.':
        'ASR chép “Vòng năm gặp Ô Trống Thi Dưng” (0.714): lệch âm/thanh thuần Việt: thì dừng/thi dưng — NOT_VERIFIED bằng tai người',
    'Kiểm bằng đường khác, đảo từng chữ của 0 1 1 0 cũng được 1 0 0 1.':
        'ASR chép “Kiểm bằng đường khác, đảo từng chữ của 0101 cũng được 1001.” (0.789): lệch âm/thanh thuần Việt: không/∅, không/∅, không/trăm linh — NOT_VERIFIED bằng tai người',
    'Chạy như vậy, U đóng vai một trình thông dịch đang thông dịch chính mình.':
        'ASR chép “Chạy như vậy, ủ đóng vai một trình thông dịch đang thông dịch chính mình.” (0.933): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'D nhận mã của một chương trình P, rồi hỏi H xem P chạy trên chính mã của nó có dừng không.':
        'ASR chép “Ve nhận mã của một chương trình P, rồi hỏi HCM P chạy trên chính mã của nó có dừng không?” (0.884): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: xem (trong “h xem” → “hcm”) — NOT_VERIFIED bằng tai người',
    'Hàng P một, cột 1, ô là 0, đảo thành 1.':
        'ASR chép “Hàng P1, Cột 1, O là 0, đảo thành 1.” (0.909): “ô” (ô lưới) ASR viết chữ “O” — NOT_VERIFIED bằng tai người',
    'Hàng P hai, cột 2, ô là 1, đảo thành 0.':
        'ASR chép “Hàng P2, cột 2, O là 1, đảo thành không.” (0.909): “ô” (ô lưới) ASR viết chữ “O” — NOT_VERIFIED bằng tai người',
    'Hàng P ba, cột 3, ô là 0, đảo thành 1.':
        'ASR chép “Hàng P3, Cột 3, O là 0, đảo thành 1.” (0.909): “ô” (ô lưới) ASR viết chữ “O” — NOT_VERIFIED bằng tai người',
    'Chuỗi 1 0 0 1 đổi thành 9, chia hết cho 3, nên câu trả lời là có.':
        'ASR chép “Chủy 1001 đổi thành chính, chia hết cho ba nên câu trả lời là có.” (0.789): lệch âm/thanh thuần Việt: chuỗi/chuỷ, không/trăm linh, chín/chính — NOT_VERIFIED bằng tai người',
    'P hai trên băng trống không dừng, vì mỗi vòng nó lại sang một ô trống mới, và B cũng nói không về Q hai, cũng khớp.':
        'ASR chép “T2 trên băng trống không dừng vì mỗi vòng nó lại sang một ô trống mới, và B cũng nói không về quy 2, cũng khớp.” (0.963): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Mô phỏng tối đa 101 bước, P một dừng ở bước 5 nên không quá 100 bước, còn P hai tới bước 101 vẫn chạy nên có quá.':
        'ASR chép “Mô phỏng tối ra 101 bước, T1 dừng ở bước 5 nên không quá 100 bước, còn T2 tới bước 101 vẫn chạy nên có quá.” (0.914): lam-đa (λ), ASR viết “lambda”; chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    # ── Đợt B đào sâu: RBM ──
    'Thay theta bằng âm 30 độ, cos vẫn là 0 phẩy 866, còn sin đổi dấu thành âm 0 phẩy 5.':
        'ASR chép “Thay teta bằng âm 30 độ, cosine vẫn là 0,866, còn sinh đổi dấu thành âm 0,5.” (0.84): cos đọc “cô-sin” theo lexicon RBM/ROB, ASR viết “cô sinh/co sinh”; “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; sin đọc thô, ASR viết “sinh” (gần âm); lệch âm/thanh thuần Việt: không (trong “không phẩy” → “”); “theta” đọc “tê-ta” theo lexicon_vi.RBM.yaml (probe p2 7/8), ASR viết “teta/TETA” — đúng âm — NOT_VERIFIED bằng tai người',
    'Bước ba, ở tích bên phải, R z làm trước.':
        'ASR chép “Bước 3. Ở tích bên phải, e đợi giác làm trước.” (0.762): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Thay theta bằng 90 độ, cos bằng 0 và sin bằng 1, ta được ma trận này.':
        'ASR chép “Thay tê ta bằng 90 độ, cô sinh bằng 0 và sinh bằng 1, ta được ma trận này.” (0.9): sin đọc thô, ASR viết “sinh” (gần âm) — NOT_VERIFIED bằng tai người',
    'Câu hai, khi theta y bằng 90 độ thì ma trận chỉ phụ thuộc vào hiệu theta x trừ theta z, ở đây là 40 trừ 10, bằng 30 độ.':
        'ASR chép “Câu 2. Khi TETA-I bằng 90 độ thì má trận chỉ phụ thuộc vào hiệu TETA-X trừ TETA-Z, ở đây là 40 trừ 10, bằng 30 độ.” (0.879): “theta” đọc “tê-ta” theo lexicon_vi.RBM.yaml (probe p2 7/8), ASR viết “teta/TETA” — đúng âm — NOT_VERIFIED bằng tai người',
    'Điều thứ hai, góc 45 độ có cos và sin bằng nhau, cùng bằng căn 2 chia 2, xấp xỉ 0 phẩy 707.':
        'ASR chép “Điều thứ 2, góc 45 độ có cô sinh và sinh bằng nhau, cùng bằng căn 2 chi 2, sắp xỉ 0,707.” (0.821): sin đọc thô, ASR viết “sinh” (gần âm); “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; lệch âm/thanh thuần Việt: chia/chi, xấp/sắp, không (trong “không phẩy” → “”) — NOT_VERIFIED bằng tai người',
    'Hai nửa cộng lại bằng 1, và con số 1 này sẽ xuất hiện ngay trong ví dụ quay 90 độ, vì quaternion dùng nửa góc.':
        'ASR chép “Hai nửa cộng lại bằng mục, và con số mục này sẽ xuất hiện ngay trong ví dụ quay 90 độ vì qua tơ niơn dùng nửa góc.” (0.881): lệch âm/thanh thuần Việt: một/mục, một/mục; “quaternion” đọc “qua-tơ-ni-ơn” theo lexicon_vi.RBM.yaml (tốt nhất 4/8 trong probe), ASR chép cùng dáng âm “qua tơ niơn / qua tên ni ân” — NOT_VERIFIED bằng tai người',
    'Hình này cho thấy vì sao quaternion chỉ chứa nửa góc.':
        'ASR chép “Hình này cho thấy vì sao qua tên ni ân chỉ chứa nửa góc.” (0.857): “quaternion” đọc “qua-tơ-ni-ơn” theo lexicon_vi.RBM.yaml (tốt nhất 4/8 trong probe), ASR chép cùng dáng âm “qua tơ niơn / qua tên ni ân” — NOT_VERIFIED bằng tai người',
    'Nhân q vào bên trái, mũi tên quay thêm 45 độ, thành mũi tên cam 0 phẩy 707, 0 phẩy 707, 0.':
        'ASR chép “Nhân quy vào bên trái, mũi tên quay thêm 45 độ, thành mũi tên cam 0.707, 0.707, 0.” (0.786): “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; lệch âm/thanh thuần Việt: không (trong “không phẩy” → “bảy trăm linh bảy”), bảy trăm linh bảy không (trong “phẩy bảy trăm linh bảy không” → “”) — NOT_VERIFIED bằng tai người',
    'Bước một, vector 1, 0, 0 ghép thành quaternion i, ta nhân q với i, nhân phân phối được c i cộng c k i.':
        'ASR chép “Bước 1, vector 1, 0, không ghép thành qua tên i ân y, ta nhận quy với y, nhận phần phối được c y cộng ck y.” (0.792): lệch âm/thanh thuần Việt: nhân/nhận, nhân phân/nhận phần; “quaternion” đọc “qua-tơ-ni-ơn” theo lexicon_vi.RBM.yaml (tốt nhất 4/8 trong probe), ASR chép cùng dáng âm “qua tơ niơn / qua tên ni ân” — NOT_VERIFIED bằng tai người',
    'Còn lại hai lần c bình phương nhân j.':
        'ASR chép “Còn lại 2 lần xe bình phương nhân gì?” (0.889): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Bước bốn, c bình phương bằng một nửa như đã ôn, nên 2 c bình phương bằng 1, kết quả là j.':
        'ASR chép “Bước 4, xe bình phương bằng một nửa như đã ôn, nên 2 xe bình phương bằng một, kết quả là gì?” (0.955): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Làm sao biết phép tính quaternion đúng?':
        'ASR chép “Làm sao biết phép tính qua tơ ni ân đúng?” (0.9): “quaternion” đọc “qua-tơ-ni-ơn” theo lexicon_vi.RBM.yaml (tốt nhất 4/8 trong probe), ASR chép cùng dáng âm “qua tơ niơn / qua tên ni ân” — NOT_VERIFIED bằng tai người',
    'Đường thứ hai, kiểm q đúng là quaternion đơn vị, c bình phương cộng c bình phương bằng một nửa cộng một nửa, bằng 1.':
        'ASR chép “Đường thứ 2, kiểm quy đúng là qua tên ni ân đơn vị, xe bình phương cộng xe bình phương bằng một nửa cộng một nửa, bằng một.” (0.929): “quaternion” đọc “qua-tơ-ni-ơn” theo lexicon_vi.RBM.yaml (tốt nhất 4/8 trong probe), ASR chép cùng dáng âm “qua tơ niơn / qua tên ni ân” — NOT_VERIFIED bằng tai người',
    'Câu hai, phần số là cos 30 độ nên nửa góc là 30 độ, và phần vector chỉ có thành phần x.':
        'ASR chép “Câu 2, phần số là cosine 30 độ nên nửa góc là 30 độ và phần vector chỉ có thành phần x.” (0.958): cos đọc “cô-sin” theo lexicon RBM/ROB, ASR viết “cô sinh/co sinh” — NOT_VERIFIED bằng tai người',
    'Đầu tay là hai khâu nối đuôi nhau, nên hoành độ của nó bằng tổng hai đoạn đậm dưới trục x, L 1 cos theta 1 cộng L 2 cos của theta 1 cộng theta 2.':
        'ASR chép “Đầu tay là hai khâu nối đuôi nhau, nên hoành độ của nó bằng tổng hai đoạn đậm dưới trục x L1 cos Teta 1 cộng L2 cos Teta 1 cộng Teta2.” (0.901): “theta” đọc “tê-ta” theo lexicon_vi.RBM.yaml (probe p2 7/8), ASR viết “teta/TETA” — đúng âm — NOT_VERIFIED bằng tai người',
    'Bước ba, đoạn khâu 2 dài 1 theo hướng 90 độ là cos 90 độ, sin 90 độ, tức 0 và 1, đi thẳng lên một đơn vị.':
        'ASR chép “Bước 3, đoạn khâu 2 dài 1 theo hướng 90 độ là cô sinh 90 độ, sinh 90 độ, tức 0 và 1, đi thẳng lên một đơn vị.” (0.938): sin đọc thô, ASR viết “sinh” (gần âm) — NOT_VERIFIED bằng tai người',
    'Điều thứ hai, góc 60 độ và góc âm 60 độ có cùng cos bằng 0 phẩy 5, chỉ khác dấu của sin.':
        'ASR chép “Điều thứ hai, góc 60 độ và góc âm 60 độ có cùng cô sinh bằng 0,5, chỉ khác giấu của sinh.” (0.923): sin đọc thô, ASR viết “sinh” (gần âm) — NOT_VERIFIED bằng tai người',
    'Còn cos luôn nằm giữa âm 1 và 1, nên đòi cos bằng 2 là vô nghiệm, hai ý này chính là hai nghiệm và vô nghiệm của bài hôm nay.':
        'ASR chép “Còn cô sinh luôn nằm giữa âm 1 và 1, nên đòi cô sinh bằng 2 là vô nghiệm, 2 ý này chính là 2 nghiệm và vô nghiệm của bài hôm nay.” (0.939): sin đọc thô, ASR viết “sinh” (gần âm) — NOT_VERIFIED bằng tai người',
    'Vì vậy theta 1 bằng hướng đích trừ góc lệch, 60 trừ 30, bằng 30 độ.':
        'ASR chép “Vì vậy, teta 1 bằng hướng đức trừ gốc lệch 60 trừ 30 bằng 30 độ.” (0.842): lệch âm/thanh thuần Việt: đích/đức, góc/gốc; “theta” đọc “tê-ta” theo lexicon_vi.RBM.yaml (probe p2 7/8), ASR viết “teta/TETA” — đúng âm — NOT_VERIFIED bằng tai người',
    'Còn theta 2 thì tìm trước, chỉ từ khoảng cách giữa gốc và đích.':
        'ASR chép “Còn Teta2 thì tìm trước, chỉ từ khoảng cách giữa gốc và đích.” (0.929): “theta” đọc “tê-ta” theo lexicon_vi.RBM.yaml (probe p2 7/8), ASR viết “teta/TETA” — đúng âm — NOT_VERIFIED bằng tai người',
    'Góc lệch là a-tan 2 của sin theta 2 và 1 cộng cos theta 2, với cos bằng 0 thì đó là a-tan 2 của 1 và 1.':
        'ASR chép “Góc lịch là A tan 2 của sin τ2 và một cộng cô sin τ2, với cô sin bằng không thì đó là A tan 2 của 1 và 1.” (0.879): tê-ta theo lexicon RBM/ROB, ASR viết “theta/teta”; lệch âm/thanh thuần Việt: lệch/lịch — NOT_VERIFIED bằng tai người',
    'Điều thứ hai là quy tắc chuỗi, nếu cả a và b đều thay đổi theo thời gian thì tốc độ thay đổi của f là tổng của hai phần.':
        'ASR chép “Điều thứ 2 là quy tắc chuỗi. Nếu cả A và B đều thay đổi theo thời gian thì tốc độ thay đổi của S là tổng của 2 phần.” (0.967): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Sin 30 độ bằng 0 phẩy 5, cos 30 độ bằng 0 phẩy 866, còn theta 1 cộng theta 2 bằng 90 độ nên s 1 2 bằng 1 và c 1 2 bằng 0.':
        'ASR chép “Xin 30 độ bằng 0,5, cô xin 30 độ bằng 0,866, còn Teta 1 cộng Teta 2 bằng 90 độ nên S1 2 bằng 1 và C1 2 bằng 0.” (0.907): “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; tê-ta theo lexicon RBM/ROB, ASR viết “theta/teta”; lệch âm/thanh thuần Việt: không (trong “không phẩy” → “”) — NOT_VERIFIED bằng tai người',
    'Công thức là x mới bằng x cộng h nhân f của x.':
        'ASR chép “Công thức là ít mới bằng ít cộng hát nhân ép cuối.” (0.88): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: của (trong “của x” → “cuối”) — NOT_VERIFIED bằng tai người',
    'Hai đường đứt là hai hướng riêng của A, hướng xanh 1, âm 1 và hướng cam 1, âm 2.':
        'ASR chép “Hai đường đức là hai hướng riêng của á, hướng xanh một, âm một và hướng ca một, âm hai.” (0.85): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: đứt/đức, cam/ca — NOT_VERIFIED bằng tai người',
    'Bước một, trừ lambda ở hai ô đường chéo của A, rồi tính định thức theo a nhân d trừ b nhân c.':
        'ASR chép “Bước 1, trừ lambda ở 2 ô đường chéo qua, rồi tính định thức theo a nhân dê trừ b nhân c.” (0.936): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: của (trong “của a” → “qua”) — NOT_VERIFIED bằng tai người',
    'Ví dụ lambda bình phương cộng 2 lambda cộng 4 có b bình phương trừ 4 c bằng 4 trừ 16, bằng âm 12, nên nghiệm là âm 1 cộng trừ căn 3 i.':
        'ASR chép “Ví dụ lambda bình phương cộng 2 lambda cộng 4 có bình phương trừ 4C bằng 4 trừ 16, bằng âm 12, nên nghiệm là âm 1 cộng trừ căn bay.” (0.946): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: ba i/bay — NOT_VERIFIED bằng tai người',
    'Ngưỡng nằm đúng giữa hai bước này, nên kết quả khớp với công thức 2 chia a.':
        'ASR chép “Ngưỡng nằm đúng giữa hai bước này nên kết quả khớp với công thức Hai Chia.” (0.97): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'H P H chuyển vị chỉ lấy ô trên trái của P, bằng 2, nên S bằng 2 cộng 1, bằng 3, và K bằng cột 2, 1 chia 3.':
        'ASR chép “HP hát chuyển vị chỉ lấy O trên trái của P bằng 2, nền S bằng 2 cộng 1 bằng 3 và K bằng cột 2, 1 chia 3.” (0.933): “ô” (ô lưới) ASR viết chữ “O”; lệch âm/thanh thuần Việt: nên/nền — NOT_VERIFIED bằng tai người',
    'Đường thứ nhất, nếu chỉ nhìn vị trí thì đây là bài toán một chiều của bài 12, với P bằng 2 là ô trên trái, và R bằng 1.':
        'ASR chép “Đường thứ nhất, nếu chỉ nhìn vị trí thì đây là bài toán 1 chiều của bài 12 với P bằng 2 là O trên trái và R bằng 1.” (0.968): “ô” (ô lưới) ASR viết chữ “O” — NOT_VERIFIED bằng tai người',
    'Phương sai vị trí nhân với 1 trừ K, tức còn một phần ba của 2, tức 0 phẩy 667, khớp ô trên trái của P mới.':
        'ASR chép “Phương sai vị trí nhân với 1 trừ ca, tức còn 1 phần 3 của 2, tức 0,667, khớp o trên trái của P mới.” (0.933): “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; “ô” (ô lưới) ASR viết chữ “O”; lệch âm/thanh thuần Việt: không (trong “không phẩy” → “”) — NOT_VERIFIED bằng tai người',
    'Ví dụ 0 phẩy 3 vòng cho cos bằng âm 0 phẩy 309.':
        'ASR chép “Ví dụ 0.3 vòng cho cosine bằng âm 0.309.” (0.828): “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; cos đọc “cô-sin” theo lexicon RBM/ROB, ASR viết “cô sinh/co sinh”; lệch âm/thanh thuần Việt: không (trong “không phẩy” → “”) — NOT_VERIFIED bằng tai người',
    'Tín hiệu 7 Hz đã quay 0 phẩy 7 vòng, tín hiệu 3 Hz đã quay 0 phẩy 3 vòng, và cả hai đều cho cos bằng âm 0 phẩy 309.':
        'ASR chép “Tín hiệu 7Hz đã quay 0.7 vòng, tín hiệu 3Hz đã quay 0.3 vòng và cả hai đều cho cosine bằng âm 0.309.” (0.906): “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; cos đọc “cô-sin” theo lexicon RBM/ROB, ASR viết “cô sinh/co sinh”; lệch âm/thanh thuần Việt: không (trong “không phẩy” → “”) — NOT_VERIFIED bằng tai người',
    'Bước ba, mẫu lúc 0 phẩy 2 giây, tín hiệu 7 Hz quay 1 phẩy 4 vòng, bỏ vòng trọn thì dừng ở 0 phẩy 4 vòng, còn tín hiệu 3 Hz quay 0 phẩy 6 vòng.':
        'ASR chép “Bước 3, mẫu lúc 0,2 giây, tín hiệu bậy hét quay 1,4 vòng, bỏ vòng trọn thì dừng ở 0,4 vòng, còn tín hiệu 3 hét quay 0,6 vòng.” (0.919): “Hz” đọc “héc” theo lexicon_vi.RBM.yaml; ASR không tách âm cuối c/t nên chép “hét” (probe p1: đối chứng “hét” cũng chép “hét”) — NOT_VERIFIED bằng tai người',
    'Ba hàng 3 Hz, 7 Hz và 13 Hz giống hệt nhau từng số, đúng như quy tắc nói cả ba đều trông như 3 Hz.':
        'ASR chép “Ba hàng ba hét, bảy hét và mười ba hét giống hệt nhau từng số, đúng như quy tắc nói cả ba đều trông như ba hét.” (0.852): “Hz” đọc “héc” theo lexicon_vi.RBM.yaml; ASR không tách âm cuối c/t nên chép “hét” (probe p1: đối chứng “hét” cũng chép “hét”) — NOT_VERIFIED bằng tai người',
    'Lúc này 7 Hz quay khoảng 0 phẩy 467 vòng giữa hai lần đọc, cho mẫu âm 0 phẩy 978.':
        'ASR chép “Lúc này 7 hét quay khoảng 0,467 vòng giữa hai lần độc, cho mẫu âm 0,978.” (0.846): “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; lệch âm/thanh thuần Việt: không (trong “không phẩy” → “”), đọc/độc, không (trong “không phẩy” → “”); “Hz” đọc “héc” theo lexicon_vi.RBM.yaml; ASR không tách âm cuối c/t nên chép “hét” (probe p1: đối chứng “hét” cũng chép “hét”) — NOT_VERIFIED bằng tai người',
    'Còn 3 Hz chỉ quay 0 phẩy 2 vòng, cho mẫu 0 phẩy 309.':
        'ASR chép “Còn 3 hét chỉ quay 0,2 vòng, cho mẫu 0,309.” (0.875): “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; lệch âm/thanh thuần Việt: không (trong “không phẩy” → “”); “Hz” đọc “héc” theo lexicon_vi.RBM.yaml; ASR không tách âm cuối c/t nên chép “hét” (probe p1: đối chứng “hét” cũng chép “hét”) — NOT_VERIFIED bằng tai người',
    'Hai dãy mẫu khác nhau ngay từ mẫu thứ hai, nên với 15 lần đọc mỗi giây ta thấy đúng 7 Hz, khớp với dòng cuối của bảng quy tắc.':
        'ASR chép “2 dãy mẫu khác nhau ngay từ mẫu thứ 2, nên với 15 lần độc mỗi dây ta thấy đúng 7 hét, khớp với dòng cuối của bạn quy tắc.” (0.903): lệch âm/thanh thuần Việt: đọc/độc, bảng/bạn; “Hz” đọc “héc” theo lexicon_vi.RBM.yaml; ASR không tách âm cuối c/t nên chép “hét” (probe p1: đối chứng “hét” cũng chép “hét”) — NOT_VERIFIED bằng tai người',
    'Bảng cho thấy sin 7 Hz đọc 14 lần mỗi giây ra toàn số 0, còn đọc 15 lần mỗi giây thì các mẫu đã khác 0.':
        'ASR chép “Bảng cho thấy sinh 7 hét đọc 14 lần mỗi dây ra toàn số 0, còn đọc 15 lần mỗi dây thì các mẫu đã khác không.” (0.931): sin đọc thô, ASR viết “sinh” (gần âm); “Hz” đọc “héc” theo lexicon_vi.RBM.yaml; ASR không tách âm cuối c/t nên chép “hét” (probe p1: đối chứng “hét” cũng chép “hét”) — NOT_VERIFIED bằng tai người',
    'Từ ô hàng 1 cột 0 tới ô hàng 1 cột 3, chênh hàng là 0, chênh cột là 3, cộng lại là 3.':
        'ASR chép “Từ ô hàng một cục không tới ô hàng một cục ba, trên hàng là không, trên cục là ba, cộng lại là ba.” (0.792): lệch âm/thanh thuần Việt: cột/cục, cột/cục, chênh/trên, chênh cột/trên cục — NOT_VERIFIED bằng tai người',
    'Ở S, f chỉ bằng 3, vì khoảng cách Manhattan không biết có tường chắn, nó lạc quan hơn sự thật.':
        'ASR chép “Ở S, F chỉ bằng 3, vì khoảng cách mang hát tầng không biết có tường trắng, nó lạc quan hơn sự thật.” (0.87): Manhattan đọc “Man-hát-tần” theo lexicon chung, ASR viết “mang hát tân/tầng”; lệch âm/thanh thuần Việt: chắn/trắng — NOT_VERIFIED bằng tai người',
    'A sao luôn ưu tiên ô có f nhỏ, nên nó bám theo những ô có cột cao đúng bằng đường dài thật.':
        'ASR chép “À sao luôn ưu tiên ô có ép nhỏ nên nó bám theo những ô có cực cao đúng bằng đường dài thật.” (0.913): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: cột/cực — NOT_VERIFIED bằng tai người',
    'Bước một, ô xuất phát S có g bằng 0 vì chưa đi bước nào, h bằng 0 cộng 3, tức 3, nên f bằng 3.':
        'ASR chép “Bước 1, O xuất phát X có dê bằng không vì chưa đi bước nào, hát bằng không cộng 3, tức 3, nên F bằng 3.” (0.962): “ô” (ô lưới) ASR viết chữ “O” — NOT_VERIFIED bằng tai người',
    'Bước hai, ta mở ô xuất phát S để xét các ô kề của nó.':
        'ASR chép “Bước 2, ta mở ô xúc phác S để xét các OK của nó.” (0.759): “ô” (ô lưới) ASR viết chữ “O”; lệch âm/thanh thuần Việt: xuất phát/xúc phác, kề (trong “ô kề” → “ok”) — NOT_VERIFIED bằng tai người',
    'Bước ba, mở ô phía trên rồi đi dọc hàng trên, mỗi ô đều có f bằng 5, vì g tăng 1 thì h giảm 1.':
        'ASR chép “Bước 3, mở ô phía trên rồi đi dọc hàng trên, mỗi ô đều có S bằng năm, vì dê tăng 1 thì hát giảm 1.” (0.962): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Ví dụ từ ô góc tới ô hàng 2 cột 2, đi chéo chỉ mất 2 bước, mà Manhattan báo 4, vượt gấp đôi.':
        'ASR chép “Ví dụ từ ô góc tới ô hàng 2 cột 2, đi chéo chỉ mất 2 bước mà mang hát tầng báo 4 vượt gấp đôi.” (0.923): Manhattan đọc “Man-hát-tần” theo lexicon chung, ASR viết “mang hát tân/tầng” — NOT_VERIFIED bằng tai người',
    'Đáp án câu một, ô này cách S đúng một bước nên g bằng 1.':
        'ASR chép “Đáp án câu 1, o này cách x đúng 1 bước nên dê bằng 1.” (0.933): “ô” (ô lưới) ASR viết chữ “O” — NOT_VERIFIED bằng tai người',
    'Hàng cuối là bình phương độ lệch của x.':
        'ASR chép “Hàng cuối là bình phương độ lệch cuối.” (0.824): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: của (trong “của x” → “cuối”) — NOT_VERIFIED bằng tai người',
    # ── Đợt B đào sâu: CS112 ──
    'Bước hai, viết thành tổng Sigma của i cộng 1, rồi tách ra tổng từ 1 đến n cộng với tổng của hằng số 1.':
        'ASR chép “Bước 2, viết thành tổng sigma của y cộng 1, rồi tách ra tổng từ 1 đến n cộng với tổng của hàng số 1.” (0.96): lệch âm/thanh thuần Việt: hằng/hàng — NOT_VERIFIED bằng tai người',
    'Nút 9 trỏ tới rỗng, nên ta dừng.':
        'ASR chép “Nút 9 trọ tới rổng, nên ta dừng.” (0.75): lệch âm/thanh thuần Việt: trỏ/trọ, rỗng/rổng — NOT_VERIFIED bằng tai người',
    'Số 12 chia 5 dư 2, ô 2 còn trống nên vào ô 2.':
        'ASR chép “Số 12 chia 5 dư 2, ồ 2 còn trống nên vào ồ 2.” (0.867): “ô” (ô lưới) ASR viết chữ “O” — NOT_VERIFIED bằng tai người',
    'Số 6 giờ ở ô 2, mà con của ô 2 là ô 5 và ô 6, đều nằm ngoài mảng năm phần tử, nên dừng.':
        'ASR chép “Số 6 giờ ở O2 mà con của O2 là O5 và O6 đều nằm ngoài mảng 5 phần tử nên dừng.” (0.846): “ô” (ô lưới) ASR viết chữ “O” — NOT_VERIFIED bằng tai người',
    'Tầng đáy cũng vậy, vì mỗi lời gọi ở đó trả về T của 2 bằng 2.':
        'ASR chép “Tần đấy cũng vậy, vì mỗi lời gọi ở đó trả VT của 2 bằng 2.” (0.788): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: tầng đáy/tần đấy, về (trong “về t” → “vt”) — NOT_VERIFIED bằng tai người',
    'Cộng thêm tầng đáy, ta đoán được đáp số thuộc Theta của n nhân lôgarit lôgarit n, và tám bước sau đây sẽ chứng minh chặt điều đó.':
        'ASR chép “Cộng thêm tầng đáy, ta đoán được đáp số thuộc Teta của n nhân Logarith Logarith n và 8 bước sau đây sẽ chứng minh chặt điều đó.” (0.964): “theta” đọc “tê-ta” theo lexicon_vi.CS112.yaml (probe p1_tiem_can 8/8), ASR viết “teta/θ” — đúng âm — NOT_VERIFIED bằng tai người',
    'Tầng đáy có 32768 lời gọi, mỗi lời gọi trả về T của 2 bằng 2, cũng được 65536.':
        'ASR chép “Tần đáy có 32.768 lời gọi, mỗi lời gọi trả VT của 2 bằng 2 cũng được 65.536.” (0.928): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: tầng/tần, về (trong “về t” → “vt”) — NOT_VERIFIED bằng tai người',
    'Quay về, bước ba trả dấu số 3, ô thứ ba trống lại.':
        'ASR chép “Quay về Bước 3 trả giấu số 3, ồ thứ 3 trống lại.” (0.923): “ô” (ô lưới) ASR viết chữ “O” — NOT_VERIFIED bằng tai người',
    'Cuối cùng, sắp giảm dần, như sắp xếp trộn ở bài 12 tốn Theta của n lôgarit n, ba số này xếp thành 1 phẩy 6, 1 phẩy 5, rồi 1 phẩy 389.':
        'ASR chép “Cuối cùng, sắp giảm dần, như sắp xếp trộn ở bài 12 tốn Teta của N Logarith N, ba số này xếp thành 1,6, 1,5, rồi 1,389.” (0.947): “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; “theta” đọc “tê-ta” theo lexicon_vi.CS112.yaml (probe p1_tiem_can 8/8), ASR viết “teta/θ” — đúng âm — NOT_VERIFIED bằng tai người',
    'Chỉ nửa trên có nghĩa, vì đoạn phải có i không lớn hơn j, nên bảng có hình tam giác.':
        'ASR chép “Chỉ nửa trên có nghĩa vì đoạn phải có y không lớn hơn gì, nên bạn có hình tam giác.” (0.9): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: bảng/bạn — NOT_VERIFIED bằng tai người',
    'Với mỗi chỗ cắt, ô đích cộng hai ô vừa tính với chi phí ghép là 40 nhân p k nhân 30.':
        'ASR chép “Với mỗi chỗ cắt, ô đích cộng hai ô vừa tính với chi phí ghép là 40 nhân tê ca nhân 30.” (0.958): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Vậy đáp số 4 khớp với bảng, trong khi cách lập bảng chỉ cần 28 phép so sánh, mỗi cặp j đứng trước i đúng một lần, thay vì xét 256 dãy.':
        'ASR chép “Vậy đáp số 4 khớp với bạn, trong khi cách lập bạn chỉ cần 28 phép so sánh, mỗi cặp gì đứng trước y đúng một lần, thay vì xét 256 giảy.” (0.895): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: bảng/bạn, bảng/bạn, dãy/giảy — NOT_VERIFIED bằng tai người',
    'Bảng đầu đặt x một, x hai bằng 0, đó là đỉnh O.':
        'ASR chép “Bảng đầu đặt x1, x2 bằng 0, đó là đỉnh nho.” (0.923): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Chốt B bằng 3, C nhận số nhỏ hơn giữa 7 và 3 cộng 3, tức 6.':
        'ASR chép “Chút b bằng 3, sẽ nhận số nhỏ hơn giữa 7 và 3 cộng 3, tức 6.” (0.882): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: chốt/chút — NOT_VERIFIED bằng tai người',
    'Con số này không thừa, vì đường ngắn nhất tới C đi S, A, B, C, dùng đủ ba cạnh.':
        'ASR chép “Con số này không thừa vì đường ngắn nhất tới CDS, A, B, C dùng đủ 3 cạnh.” (0.895): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: đi (trong “c đi s” → “cds”) — NOT_VERIFIED bằng tai người',
    'Bảng có 50 hàng, mỗi hàng có W cộng 1 cột, tính cả cột sức chứa bằng 0.':
        'ASR chép “Bạn có 50 hàng, mỗi hàng có về đúc cộng 1 cục, tính cả cục sức chứa bằng không.” (0.769): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: bảng/bạn, cột/cục, cột/cục — NOT_VERIFIED bằng tai người',
    'Nếu f bằng 1, nhỏ hơn hẳn một lũy thừa, đó là trường hợp một, Theta của n.':
        'ASR chép “Nếu f bằng mục nhỏ hơn hẳn mục lũy Thừa, đó là trường hợp mục θ của n.” (0.778): lệch âm/thanh thuần Việt: một/mục, một/mục; “theta” đọc “tê-ta” theo lexicon_vi.CS112.yaml (probe p1_tiem_can 8/8), ASR viết “teta/θ” — đúng âm — NOT_VERIFIED bằng tai người',
    'Vậy có 3 tầng có việc, mỗi tầng 8 bước, tổng 24, đúng bằng 8 nhân lôgarit cơ số 2 của 8.':
        'ASR chép “Vậy có 3 tầng có việc, mỗi tầng 8 bước, tổng 24, đúng bằng 8 nhân Logatrix cơ số 2 của 8.” (0.958): lệch âm/thanh thuần Việt: lôgarit/logatrix — NOT_VERIFIED bằng tai người',
    'Ký hiệu chữ e cách điệu đọc là thuộc, T của n thuộc lớp Theta của n lôgarit n.':
        'ASR chép “Ký hiệu chữ E-cách điệu độc là thuộc T của N thuộc lớp Teta của N Logarith N.” (0.895): lệch âm/thanh thuần Việt: đọc/độc; “theta” đọc “tê-ta” theo lexicon_vi.CS112.yaml (probe p1_tiem_can 8/8), ASR viết “teta/θ” — đúng âm — NOT_VERIFIED bằng tai người',
    'Riêng ô 8 bằng 1 cộng số nhỏ nhất của 3, 1 và 3, tức 2, ứng với hai đồng 4.':
        'ASR chép “Riêng O8 bằng một cộng số nhỏ nhất của 3, 1 và 3, tức 2, ứng với 2 đồng 4.” (0.952): “ô” (ô lưới) ASR viết chữ “O” — NOT_VERIFIED bằng tai người',
    # ── Đợt B đào sâu: CS115 ──
    'Quy tắc tự sửa chính là lần theo sườn bát để đi xuống đáy.':
        'ASR chép “Quy tắc tự sự chính là lần theo sường bác để đi xuống đáy.” (0.786): lệch âm/thanh thuần Việt: sửa/sự, sườn bát/sường bác — NOT_VERIFIED bằng tai người',
    'Vẽ đường đi trên mặt phẳng x, y, đáy ở gốc toạ độ.':
        'ASR chép “Vẽ đường đi trên mạc phẳng x, y, đáy ở gốc tòa đầu.” (0.769): lệch âm/thanh thuần Việt: mặt/mạc, toạ độ/toà đầu — NOT_VERIFIED bằng tai người',
    'Theo công thức Newton, w một bằng 2 trừ 12 phần 14, bằng tám phần bảy.':
        'ASR chép “Theo công thức Newton, V kết 1 bằng 2 triệu 12 phần 14 bằng 8 phần 7.” (0.9): chữ w đọc “vê kép” (luật chung), ASR viết tách chữ; lệch âm/thanh thuần Việt: trừ/triệu — NOT_VERIFIED bằng tai người',
    'Làm theo quy tắc chuỗi cũng ra như vậy, vì 1 chia x bình phương, nhân với đạo hàm 2 x của hàm trong, bằng 2 chia x.':
        'ASR chép “Làm theo quy tắc chuỗi củng trai như vậy vì một chi ít bình phương, nhận với đạo hàm 2x của hàm trông bằng 2 chi ít.” (0.786): lệch âm/thanh thuần Việt: cũng ra/củng trai, chia/chi, nhân/nhận, trong/trông, chia/chi — NOT_VERIFIED bằng tai người',
    'Khi nghe tin kết quả lớn hơn 3, ta gạch mờ hàng trên, chỉ giữ ba ô 4, 5, 6 trong khung cam, chính là B.':
        'ASR chép “Khi nghe tin kết quả lớn hơn 3, ta gạch mờ hàng trên, chỉ giữ 3O4, 5, 6 trong khung cam, chính là B.” (0.962): “ô” (ô lưới) ASR viết chữ “O” — NOT_VERIFIED bằng tai người',
    'Biết kết quả là số chẵn thì chỉ còn ba ô 2, 4 và 6, trong đó có đúng một ô là 6, nên xác suất là một phần ba.':
        'ASR chép “Biết kết quả là số chẳng thì chỉ còn 3O2, 4 và 6, trồng đó có đúng 1O là 6, nên xác xuất là 1 phần 3.” (0.867): “ô” (ô lưới) ASR viết chữ “O”; lệch âm/thanh thuần Việt: chẵn/chẳng, trong/trồng — NOT_VERIFIED bằng tai người',
    'Ma trận X có ba cột, cột số 1, cột x, và cột x bình phương.':
        'ASR chép “ma trận ít có 3 cục, cục số 1, cục ít và cục ít bình phương.” (0.75): lệch âm/thanh thuần Việt: cột cột/cục cục, cột/cục, cột/cục — NOT_VERIFIED bằng tai người',
    'Mô hình vẫn là tổng các cột nhân trọng số, tức là tuyến tính theo w.':
        'ASR chép “Mô hình vẫn là tổng các cột nhân trọng số, tức là tuyến tính theo v kết.” (0.941): chữ w đọc “vê kép” (luật chung), ASR viết tách chữ — NOT_VERIFIED bằng tai người',
    'Vì thế ta dùng lại đúng phương trình chuẩn, chỉ đổi các cột của X.':
        'ASR chép “Vì thế ta dùng lại đúng phương trình chuẩn, chỉ đổi các cột cuối.” (0.897): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: của (trong “của x” → “cuối”) — NOT_VERIFIED bằng tai người',
    'Giả sử w âm thì đạo hàm cho w bằng a cộng 1, bằng 1 phẩy 5, cũng trái với giả sử.':
        'ASR chép “Giả sử về kết âm thì đạo hàm cho về kết bằng A cộng 1, bằng 1,5 cũng trái với giả sử.” (0.917): chữ w đọc “vê kép” (luật chung), ASR viết tách chữ — NOT_VERIFIED bằng tai người',
    'Hình này vẽ hàm sigmoid, trục ngang là điểm số z, trục dọc là xác suất.':
        'ASR chép “Hình này vẽ hàm xích môi, trục ngang là điểm số giác, trục dọc là xá xuất.” (0.882): lệch âm/thanh thuần Việt: moi/môi, xác/xá — NOT_VERIFIED bằng tai người',
    'Bước hai, với sai số bình phương, quy tắc chuỗi nhân đạo hàm theo dự đoán với độ dốc của sigmoid.':
        'ASR chép “Bước 2, với sai số bình phương, quy tắc chuỗi nhân đạo hàm theo dự đoán với độ dốc của sít moi.” (0.955): lệch âm/thanh thuần Việt: xích/sít — NOT_VERIFIED bằng tai người',
    'Câu một, ta đặt s bằng x cộng y cho cổng cộng, rồi f bằng s nhân z cho cổng nhân.':
        'ASR chép “Câu 1, ta đặt f bằng x cộng y cho cổng cộng, rồi f bằng f nhân vét cho cổng nhân.” (0.857): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Lượt tiến cho s bằng 3, rồi f bằng 3 nhân 4, bằng 12.':
        'ASR chép “Lượt tiếng cho F bằng 3, rồi F bằng 3 x4 bằng 12.” (0.8): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: tiến/tiếng, nhân/x — NOT_VERIFIED bằng tai người',
    'Cổng nhân tráo đổi, z nhận 1 nhân s bằng 3, còn s nhận 1 nhân z bằng 4.':
        'ASR chép “Cổng nhân tráo đuổi, giác nhận một nhân S bằng ba, còn giác nhận một nhân Z bằng bốn.” (0.895): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: đổi/đuổi — NOT_VERIFIED bằng tai người',
    'Cổng nhân với 2 gửi xuống cho m gradient bằng 1 nhân 2, tức là 2.':
        'ASR chép “Cổng nhân với hai gửi xuống cho mGradient bằng một nhân hai, tức là hai.” (0.903): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: gradient (trong “m gradient” → “mgradient”) — NOT_VERIFIED bằng tai người',
    'Lớp ẩn ReLU của lời giải vừa rồi dời mỗi điểm tới một chỗ mới, với toạ độ là h một và h hai.':
        'ASR chép “Lớp ẩn tre lưu của lời giải vừa trôi dời mỗi điểm tới một chỗ mới, với tọa độ là H1 và H2.” (0.898): lệch âm/thanh thuần Việt: rồi/trôi; “ReLU” đọc “Re-lu” theo lexicon_vi.yaml (probe L23 8/8); lần này ASR chép “tre lưu” (đổi r → tr như “rồi/trôi” cùng câu) — NOT_VERIFIED bằng tai người',
    'Bước một, đếm lớp ẩn, bắt đầu từ ma trận W một.':
        'ASR chép “Bước 1, đếm lớp ẩn bắt đầu từ ma trận về đúc 1.” (0.88): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Ta gộp chúng thành hàm Lagrange, trừ đi lam-đa nhân với tổng ba thê ta trừ 1.':
        'ASR chép “Ta gọc chúng thành hàm Lagerang trừ Đi Lam đa nhân với tổng ba theta trừ một.” (0.889): lệch âm/thanh thuần Việt: gộp/gọc; “Lagrange” đọc “La-gơ-răng” theo lexicon_vi.yaml (tốt nhất 3/8 trong probe L24), ASR chép “lagrang/lagerang” — đúng tên — NOT_VERIFIED bằng tai người',
    'Nghiệm Lagrange cho lôgarit khả năng âm 10 phẩy 297.':
        'ASR chép “Nghiệm Lagrang cho Logarith khả năng âm 10,297.” (0.857): “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; “Lagrange” đọc “La-gơ-răng” theo lexicon_vi.yaml (tốt nhất 3/8 trong probe L24), ASR chép “lagrang/lagerang” — đúng tên — NOT_VERIFIED bằng tai người',
    'Hai bộ khác cho âm 10 phẩy 549 và âm 10 phẩy 601, đều nhỏ hơn, nên nghiệm Lagrange thắng cả hai.':
        'ASR chép “2 bộ khác cho âm 10.549 và âm 10.601, đều nhỏ hơn, nên nghiệm Lagrang thắng cả 2.” (0.897): “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; “Lagrange” đọc “La-gơ-răng” theo lexicon_vi.yaml (tốt nhất 3/8 trong probe L24), ASR chép “lagrang/lagerang” — đúng tên — NOT_VERIFIED bằng tai người',
    'Câu một, ta lập hàm Lagrange, x nhân y trừ lam-đa nhân với x cộng 2 y trừ 8.':
        'ASR chép “Câu 1, ta lập hàm lá gơ răng ít nhân y trừ Lam Đa Nhân với ít cộng 2 y trừ Tám.” (0.955): lệch âm/thanh thuần Việt: la/lá — NOT_VERIFIED bằng tai người',
    'Vì S w là ma trận chéo với hai số 9 và 0 phẩy 25, w chuyển vị nhân S w nhân w chỉ là 9 nhân 3 bình phương, cộng 0 phẩy 25 nhân 1 bình phương.':
        'ASR chép “Vì fvkp là ma trận chéo với 2 số 9 và 0,25. Vkp chuyển vị nhân fvkp nhân vkp chỉ là 9 nhân 3 bình phương, cộng 0,25 nhân 1 bình phương.” (0.878): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Câu hai, vì S w là ma trận chéo, nhân với nghịch đảo của nó là chia từng chiều cho độ trải.':
        'ASR chép “Câu 2, vì fvk là ma trận chéo, nhận với nghiệt đạo của nó là chia từng chiều cho độ trải.” (0.791): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: nhân/nhận, nghịch đảo/nghiệt đạo — NOT_VERIFIED bằng tai người',
    'Vậy J bằng 64 chia 8, bằng 8, gấp đôi hướng ngang.':
        'ASR chép “Vậy dì bằng 64 chia 8, bằng 8, gấp đôi hướng ngang.” (0.929): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Gán lại lần nữa thì không điểm nào đổi cụm, và thuật toán dừng.':
        'ASR chép “Gán lại lần nữa thì không điểm nào đổi cùng và thuật bán dưng.” (0.786): lệch âm/thanh thuần Việt: cụm/cùng, toán dừng/bán dưng — NOT_VERIFIED bằng tai người',
    'Ma trận Laplacian của bốn điểm ví dụ được viết ra đầy đủ, đường chéo là bậc của mỗi điểm, các ô khác là trọng số mang dấu trừ.':
        'ASR chép “Ma trận lắp la xiang của 4 điểm ví dụ được viết ra đầy đủ, đường chéo là bật của mỗi điểm, các ô khác là trọng số mang dấu trư.” (0.867): lệch âm/thanh thuần Việt: bậc/bật, trừ/trư; “Laplacian” đọc “Láp-la-xi-an” theo lexicon_vi.yaml, ASR chép cùng dáng âm “lắp la xiang” — NOT_VERIFIED bằng tai người',
    'Văn bản 4 lấy mỗi phần một lần, ra 1, 1, 1, 1, đúng hàng cuối của X.':
        'ASR chép “Văn bản 4 lấy mỗi phần 1 lần ra 1, 1, 1, 1, đúng hàng cuối cuối.” (0.914): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: của (trong “của x” → “cuối”) — NOT_VERIFIED bằng tai người',
    'Bước ba, chia từng số cho tổng, đúng như softmax của bài 20.':
        'ASR chép “Bước ba, chia từng số cho tổng đúng như sắp mát của bài 20.” (0.897): “softmax” đọc “sóp-mác” theo lexicon_vi.yaml (tốt nhất 3/8, B44 OPEN), ASR chép “sắp mát” — tên tiếng Anh khó, cần người nghe — NOT_VERIFIED bằng tai người',
    'Bước bốn, tính entropy bằng cách cộng ba số hạng âm p nhân lôgarit p, được khoảng 0 phẩy 545.':
        'ASR chép “Bước 4, tính entropy bằng cách cộng 3 số hạng ấm tê nhân logarithmê được khoảng 0,545.” (0.8): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; lệch âm/thanh thuần Việt: âm (trong “âm p” → “ấm t”), lôgarit (trong “lôgarit p” → “logarithmê”), không (trong “không phẩy” → “”) — NOT_VERIFIED bằng tai người',
    'Lấy e mũ lôgarit của 2 thì được đúng 2.':
        'ASR chép “Lấy e-mũ Logatrix của 2 thì được đúng 2.” (0.9): lệch âm/thanh thuần Việt: lôgarit/logatrix — NOT_VERIFIED bằng tai người',
    'Hàm ngoài là tanh, có đạo hàm 1 trừ h t bình phương, còn hàm trong có đạo hàm bằng w.':
        'ASR chép “Hàm ngoài là tanh, có đạo hàm 1 trừ ht bình phương, còn hàm trong có đạo hàm bằng v kết.” (0.955): chữ w đọc “vê kép” (luật chung), ASR viết tách chữ — NOT_VERIFIED bằng tai người',
    'Lỗi thứ tư hay gặp ở người đã đi làm, chạy AdaBoost trên dữ liệu có nhãn gán nhầm mà không xem trọng số mẫu.':
        'ASR chép “Lỗi thứ tư hay gặp ở người đã đi làm, chạy Adabook trên dữ liệu có nhãn gán nhằm mà không xem trọng số mẫu.” (0.92): lệch âm/thanh thuần Việt: nhầm/nhằm; “AdaBoost” đọc “A-đa-bút” theo lexicon_vi.yaml, ASR chép “adabook” — NOT_VERIFIED bằng tai người',
    'Một nửa lôgarit của 9 bằng lôgarit của 3, vì 9 là 3 bình phương, xấp xỉ 1 phẩy 099.':
        'ASR chép “Một nửa logarith của chính bằng logarith của ba vì chính là ba bình phương, sắp xỉ 1.099.” (0.783): “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; lệch âm/thanh thuần Việt: chín/chính, chín/chính, xấp/sắp — NOT_VERIFIED bằng tai người',
    'Cùng một độ lệch 10 xăng-ti-mét, cột ghi bằng mét lệch 0 phẩy 1, còn cột ghi bằng mi-li-mét lệch 100.':
        'ASR chép “Cùng mục đổ lệch 10 cm, cột vi bằng mét lệch 0,1 còn cột vi bằng millimet lệch 100.” (0.76): đơn vị mi-li-mét, ASR viết ký hiệu “mm”; lệch âm/thanh thuần Việt: một độ/mục đổ, ghi/vi, ghi/vi — NOT_VERIFIED bằng tai người',
    'Câu một, nhân từng hàng của A với s, được 0 và âm 1 phẩy 5.':
        'ASR chép “Câu 1, nhân từng hàng của AVS được 0 và âm 1,5.” (0.867): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: với (trong “a với s” → “avs”) — NOT_VERIFIED bằng tai người',
    'Nhỏ nhất là 0 phẩy 546, khi v bằng đúng w.':
        'ASR chép “Nhỏ nhất là 0,546 khi V bằng đúng V két.” (0.867): “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; chữ w đọc “vê kép” (luật chung), ASR viết tách chữ; lệch âm/thanh thuần Việt: không (trong “không phẩy” → “”) — NOT_VERIFIED bằng tai người',
    'Độ dốc bằng 0 đúng tại v bằng 0 phẩy 8, tức là v bằng w, khớp kết quả máy dò.':
        'ASR chép “Độ dốc bằng không đúng tại v bằng 0,8, tức là v bằng v két, khớp kết quả máy dò.” (0.955): chữ w đọc “vê kép” (luật chung), ASR viết tách chữ — NOT_VERIFIED bằng tai người',
    'Được 2 phẩy 028, 1 và 2 phẩy 028, cộng lại bằng 5 phẩy 056.':
        'ASR chép “được 2,028, 1 và 2,028 cộng lại bằng 5,056.” (0.75): “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải” — NOT_VERIFIED bằng tai người',
    'Câu một, thay vào công thức độ lệch, cả hai đều có phương sai 1, và lôgarit của 1 bằng 0.':
        'ASR chép “Câu một, thay vào công thức độ lệch, cả hai đều có phương sai một và logatic của một bằng không.” (0.952): lệch âm/thanh thuần Việt: lôgarit/logatic — NOT_VERIFIED bằng tai người',
    'Bước một, nhiễu rút được bằng 1.':
        'ASR chép “Bước 1, nhiễu trúc được bằng mục” (0.714): lệch âm/thanh thuần Việt: rút/trúc, một/mục — NOT_VERIFIED bằng tai người',
    'Nên hai nhiễu nhỏ gộp lại thành một nhiễu với hệ số căn 0 phẩy 5904, xấp xỉ 0 phẩy 768.':
        'ASR chép “nên 2 nhũ nhỏ gột lại thành 1 nhũ với hệ số căng 0,5904, xắp xỉ 0,768.” (0.793): “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; lệch âm/thanh thuần Việt: nhiễu/nhũ, gộp/gột, nhiễu/nhũ, căn/căng, xấp/xắp, không (trong “không phẩy” → “”) — NOT_VERIFIED bằng tai người',
    # ── Đợt A đào sâu: SAR (câu viết lại) ──
    'Cái giá phải trả là 1 tê-ra-byte dữ liệu chiếm tới 3 tê-ra-byte trên đĩa.':
        'ASR chép “Cái giá phải trả là 1 terabyte dữ liệu chiếm tới 3 terabytes trên địa.” (0.706): “tê-ra-byte” đọc tách âm tiết, ASR viết gộp “terabyte(s)” — đúng đơn vị; số 1 và 3 khớp; đĩa/địa lệch thanh — NOT_VERIFIED bằng tai người',
    # ── Đợt A đào sâu: DVO (câu viết lại) ──
    'Trước tiên, 1 ki lô byte gồm đúng 1000 byte.':
        'ASR chép “Trước tiên, 1 kg bay gồm đúng 1.000 bay.” (0.667): “ki lô byte” ASR viết tắt “kg” rồi chép “byte” thành “bay” (cùng âm, probe p1 CSA “bay” 8/8); số 1 và 1000 khớp; mọi từ khác khớp — NOT_VERIFIED bằng tai người',
    # ── Đợt A đào sâu: ESY (câu viết lại) ──
    'Ghép hai nhóm lại, ta được 0 1 0 0, rồi tới 1 0 1 1.':
        'ASR chép “Gép hai nhóm lại ta được 0100 rồi tới 1011.” (0.688): ASR gộp từng chữ số đọc rời thành số “0100” và “1011” — đúng thứ tự và đúng từng chữ số, nên phép so chữ đọc thấy thiếu/thừa “trăm, nghìn”; ghép/gép lệch phụ âm đầu — NOT_VERIFIED bằng tai người',
    # ── Đợt B đào sâu: CSA (câu viết lại) ──
    'Bước năm, cùng một dãy bit 1 1 0 0, 1 0 0 0 lại cho ra hai cách đọc khác nhau.':
        'medium chép “… 1100, 1100 …” (0.636), nhưng probe 2026-11-02 (scratchpad probe_csa2.py, cùng câu, NamMinh −5%): small chép đúng “1 1 0 0, 1 0 0 0” ở cả bản gốc lẫn bản “rồi 1 0 0 0” (3/4), còn medium chép nhóm hai thành “1100” ở 4/4 — medium lặp lại nhóm vừa nghe, TTS đọc đúng; dãy/giải, bit/bít, đọc/đầu lệch âm — NOT_VERIFIED bằng tai người',
    'Đảo mọi bit, ta được nhóm 1 1 1 1, rồi tới nhóm 0 0 1 1.':
        'ASR chép “Đảo mọi biết ta được nhóm 1111 rồi tới nhóm 0011.” (0.706): ASR gộp chữ số đọc rời thành “1111”, “0011” — đúng từng chữ số và thứ tự; bit/biết lệch âm — NOT_VERIFIED bằng tai người',
    'Bước ba, ta cộng dãy 1 1 0 0 với chính dãy 1 1 0 0.':
        'ASR chép “Bước 3, ta cộng dãy 1100 với 9 dãy 1100.” (0.688): ASR gộp chữ số đọc rời thành “1100” — đúng từng chữ số; chính/chín lệch thanh (probe “với chính nó” cả small lẫn medium chép đúng “chính”) — NOT_VERIFIED bằng tai người',
    # ── Đợt C hành trình: DBS ──
    'Năm 2017, Stripe cần chuyển hàng trăm triệu đối tượng, và nếu mỗi đối tượng mất 1 giây, làm tuần tự 100 triệu cái sẽ mất hơn 3 năm.':
        'ASR chép “Năm 2017, Striper cần chuyển hàng trăm triệu đối tượng, và nếu mỗi đối tượng mất một giây, làm tuần tử một trăm triệu cái sẽ mất hơn ba năm.” (0.943): lệch âm/thanh thuần Việt: tự/tử; “Stripe” đọc “Xờ-trai-pơ” theo lexicon_vi.DBS.yaml (probe p2 8/8, bản chép luôn là “Striper”) — đúng tên — NOT_VERIFIED bằng tai người',
    'Bảng bóng là bản sao rỗng của bảng, đã mang lược đồ mới.':
        'ASR chép “Bản bóng là bản sao trọng của bản đã mang lực đồ mới.” (0.692): lệch âm/thanh thuần Việt: bảng/bản, rỗng/trọng, bảng/bản, lược/lực — NOT_VERIFIED bằng tai người',
    'Đổi bảng là bước cuối, khi bảng bóng thay chỗ bảng cũ.':
        'ASR chép “Đổi bản là bước cuối, khi bản bóng thay chỗ bản cũ.” (0.75): lệch âm/thanh thuần Việt: bảng/bản, bảng/bản, bảng/bản — NOT_VERIFIED bằng tai người',
    'Ở chặng hai, năm 2016, nền tảng lưu trữ mã nguồn ấy đổi lược đồ nhiều lần mỗi ngày, trên các bảng từ rỗng tới nhiều trăm GB.':
        'ASR chép “Ở chặng 2, năm 2016, nền tảng lưu trữ mã nguồn ấy đổi lượt đồ nhiều lần mỗi ngày, trên các bản từ đóng tới nhiều trăm gigabyte.” (0.879): GB đọc “ghi-ga-byte” theo lexicon của khoá, ASR viết “GB/gigabyte”; lệch âm/thanh thuần Việt: lược/lượt, bảng/bản, rỗng/đóng — NOT_VERIFIED bằng tai người',
    'Ở chặng ba, năm 2017, Stripe có hàng trăm triệu đối tượng đăng ký thanh toán định kỳ, cần chuyển từ bảng khách hàng sang bảng riêng.':
        'ASR chép “Ở chặn 3, năm 2017, Striper có hàng trăm triệu đối tượng đăng ký thanh toán định kỳ, cần chuyển từ bản khách hàng sang bản riêng.” (0.875): lệch âm/thanh thuần Việt: chặng/chặn, bảng/bản, bảng/bản; “Stripe” đọc “Xờ-trai-pơ” theo lexicon_vi.DBS.yaml (probe p2 8/8, bản chép luôn là “Striper”) — đúng tên — NOT_VERIFIED bằng tai người',
    'Ở chặng bốn, trước năm 2018, thêm cột nghĩa là dựng lại cả bảng, mất rất lâu với bảng lớn và cần thêm chỗ đĩa xấp xỉ bằng chính bảng cũ.':
        'ASR chép “Ở chặn 4, trước năm 2018, thêm cột nghĩa là dựng lại cả bản, mất trất lâu với bản lớn và cần thêm chỗ đi xắp sĩ bằng chính bản cũ.” (0.778): lệch âm/thanh thuần Việt: chặng/chặn, bảng/bản, rất/trất, bảng/bản, đĩa xấp xỉ/đi xắp sĩ, bảng/bản — NOT_VERIFIED bằng tai người',
    'Hãy kiểm bằng đường khác như Stripe chạy lại phép tìm, hay đội năm 2016 so tổng kiểm của cả bảng.':
        'ASR chép “Hãy kiểm bằng đường khác như Striper chạy lại phép tìm, hay đổi năm 2016 so tổng kiểm của cả bản.” (0.885): lệch âm/thanh thuần Việt: đội/đổi, bảng/bản; “Stripe” đọc “Xờ-trai-pơ” theo lexicon_vi.DBS.yaml (probe p2 8/8, bản chép luôn là “Striper”) — đúng tên — NOT_VERIFIED bằng tai người',
    # ── Đợt C hành trình: DSY ──
    'Ở chặng một, hệ bảng lớn được thiết kế cho hàng nghìn TB trên hàng nghìn máy, và chạy thật từ tháng 4 năm 2005.':
        'ASR chép “Ở chặn 1, hệ bản lớn được thiết kế cho hàng nghìn terabyte trên hàng nghìn máy và chạy thật từ tháng 4 năm 2005.” (0.9): lệch âm/thanh thuần Việt: chặng/chặn, bảng/bản; “TB” đọc “tê-ra-byte” theo lexicon_vi.DSY.yaml, ASR chép “terabyte/tetaby” — đúng đơn vị — NOT_VERIFIED bằng tai người',
    'Cách xử lý là một bảng sắp theo khoá, mỗi dải dòng liên tiếp là một mảnh khoảng 100 đến 200 mê-ga-byte.':
        'ASR chép “Cách xử lý là một bản sắp theo khóa, mỗi giải dòng liên tiếp là một mảnh khoảng 100-200 MB.” (0.857): MB đọc “mê-ga-byte” theo lexicon của khoá, ASR viết “MB/megabyte”; lệch âm/thanh thuần Việt: bảng/bản, đến/∅ — NOT_VERIFIED bằng tai người',
    'Mảnh gốc dài 128 mê-ga-byte, mỗi dòng khoảng 1 KB, nên chứa 128 nhân 1024, tức 2 mũ 17 vị trí mảnh chỉ mục.':
        'ASR chép “Mảnh gốc dài 128 MB mỗi dòng khoảng 1 kilobyte nên chứa 128 nhân 1.024 tức 2 mũ 17 vị trí mảnh chỉ 1.” (0.9): MB đọc “mê-ga-byte” theo lexicon của khoá, ASR viết “MB/megabyte”; KB đọc “ki-lô-byte” theo lexicon của khoá, ASR viết “kilobyte/kg”; lệch âm/thanh thuần Việt: mục/một — NOT_VERIFIED bằng tai người',
    'Ở chặng ba, trước năm 2011, hệ quảng cáo của Google chạy trên cơ sở dữ liệu quan hệ chia mảnh bằng tay, hàng chục TB, và mã ứng dụng phải biết mảnh.':
        'ASR chép “Ở chặn 3, trước năm 2011, hệ quảng cáo của Google chạy trên cơ sở dữ liệu quan hệ chi mảnh bằng tay hàng chục terabyte và mà ứng dụng phải biết mảnh.” (0.895): lệch âm/thanh thuần Việt: chặng/chặn, chia/chi, mã/mà; “TB” đọc “tê-ra-byte” theo lexicon_vi.DSY.yaml, ASR chép “terabyte/tetaby” — đúng đơn vị — NOT_VERIFIED bằng tai người',
    'Mã 0 tới 3 có hai số dư như nhau nên đứng yên.':
        'ASR chép “Mạ không tới bà có hai số dư như nhau nên đứng nhiên.” (0.769): lệch âm/thanh thuần Việt: mã/mạ, ba/bà, yên/nhiên — NOT_VERIFIED bằng tai người',
    'Năm 2017, hệ chạy hơn 5 nghìn cơ sở dữ liệu, hàng chục triệu truy vấn mỗi giây, hàng trăm nghìn TB.':
        'ASR chép “Năm 2017, hệ chạy hơn 5.000 cơ sở dữ liệu, hàng chục triệu truy vấn mỗi giây, hàng trăm nghìn TETABY.” (0.963): “TB” đọc “tê-ra-byte” theo lexicon_vi.DSY.yaml, ASR chép “terabyte/tetaby” — đúng đơn vị — NOT_VERIFIED bằng tai người',
    'Câu một, cửa hàng trực tuyến có một máy chủ chứa 200 ghi-ga-byte, mỗi năm tăng gấp 1 phẩy 5, máy chứa thoải mái 1 TB, vậy có nên chia mảnh ngay không?':
        'ASR chép “Câu một, cửa hàng trực tuyến có một máy chủ chứa 200GB, mỗi năm tăng gấp 1,5. Máy chứa thoải mái 1TB, vậy có nên chia mảnh ngay không?” (0.943): GB đọc “ghi-ga-byte” theo lexicon của khoá, ASR viết “GB/gigabyte” — NOT_VERIFIED bằng tai người',
    'Đáp án câu một, bước một là tính dung lượng, 200 nhân 1 phẩy 5 được 300, rồi 450, rồi 675, và năm thứ tư là 1012 phẩy 5 ghi-ga-byte, mới vượt 1 TB.':
        'ASR chép “Đáp án câu 1, bước 1 là tính dung lượng, 200 nhân 1,5 được 300, rồi 450, rồi 675, và năm thứ 4 là 1012,5 GB, mới vượt 1 TB.” (0.959): GB đọc “ghi-ga-byte” theo lexicon của khoá, ASR viết “GB/gigabyte” — NOT_VERIFIED bằng tai người',
    # ── Đợt C hành trình: EVT ──
    'Chào bạn, năm 2011, hệ nhật ký sự kiện Kafka ở một mạng xã hội việc làm lớn nhận gần 1 tỉ tin mỗi ngày.':
        'ASR chép “Chào bạn, năm 2011 hãy nhật ký sự kiện cắp ca ở một mạng xã hội việc làm lớn nhận gần 1 tỷ tin mỗi ngày.” (0.885): “tỉ” ASR viết chính tả “tỷ” (cùng âm); lệch âm/thanh thuần Việt: hệ/hãy; “Kafka” để đọc thô (foreign_ok, probe p1 8/8): ASR chép phiên âm “cắp ca/cấp ca” — đúng âm, không ra chữ Latinh — NOT_VERIFIED bằng tai người',
    'Ở chặng một, năm 2011, hệ nhận hàng trăm GB, tức gần 1 tỉ tin mỗi ngày.':
        'ASR chép “Ở chẳng 1, năm 2011 hệ nhận hàng trăm gigabyte tức gần 1 tỷ tin mỗi ngày.” (0.864): GB đọc “ghi-ga-byte” theo lexicon của khoá, ASR viết “GB/gigabyte”; “tỉ” ASR viết chính tả “tỷ” (cùng âm); lệch âm/thanh thuần Việt: chặng/chẳng — NOT_VERIFIED bằng tai người',
    'Trong thử nghiệm với tin 200 byte, gộp 50 tin một lần cho 400 nghìn tin mỗi giây, so với 50 nghìn khi gửi lẻ, tức gấp 8 lần.':
        'ASR chép “Trong thử nghiệm với tin 200b, gột 50 tin một lần cho 400.000 tin mỗi giây so với 50.000 khi gửi lẻ tức gấp 8 lần.” (0.939): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: gộp (trong “byte gộp” → “b gột”) — NOT_VERIFIED bằng tai người',
    'Riêng phần nội dung là 400 nghìn nhân 200 byte nhân 8 bit, bằng 640 triệu bit mỗi giây.':
        'ASR chép “Ruyên phần nội dung là 400.200 bài nhân 8 bit bằng 640 triệu bit mỗi giây.” (0.894): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: riêng/ruyên, nhân/∅ — NOT_VERIFIED bằng tai người',
    'Cách xử lý ở bản 0 chấm 8 chấm 0 được tóm tắt trong bảng.':
        'ASR chép “Các xử lý ở bảng 0.8.0 được tóm tắt trong bảng.” (0.786): lệch âm/thanh thuần Việt: cách/các, bản/bảng, chấm/∅, chấm/∅ — NOT_VERIFIED bằng tai người',
    'Làm thử với số minh hoạ, mỗi ngày ghi 1 nghìn GB và muốn chịu được 1 máy hỏng.':
        'ASR chép “Làm thử với số minh họa, mỗi ngày di 1.000 GB và muốn chịu được một máy hỏng.” (0.947): lệch âm/thanh thuần Việt: ghi/di — NOT_VERIFIED bằng tai người',
    '650 nghìn GB đọc chia cho 175 nghìn GB ghi được khoảng 3 phẩy 7, tức mỗi byte được nhiều hệ khác nhau đọc lại vài lần.':
        'ASR chép “650.000 GB đọc chia cho 175.000 GB ghi được khoảng 3,7, tức mỗi bay được nhiều hệ khác nhau đọc lại vài lần.” (0.971): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Cỡ tin năm 2015 tính theo ngày là 175 nghìn GB chia 800 tỉ tin, khoảng 219 byte, còn tính theo giờ cao điểm là khoảng 212 byte.':
        'ASR chép “Cở tin năm 2015 tính theo ngày là 175.000 GB chia 800 tỷ tin, khoảng 219.000, còn tính theo giờ cao điểm là khoảng 212.000.” (0.909): “tỉ” ASR viết chính tả “tỷ” (cùng âm); byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: cỡ/cở — NOT_VERIFIED bằng tai người',
    'Câu một, ba dịch vụ ghi tổng 1000 sự kiện mỗi giây, mỗi sự kiện 1000 byte, cần chịu 1 máy hỏng và có lúc phải tính lại 30 ngày.':
        'ASR chép “Câu 1, ba dịch vụ ghi tổng 1.000 sự kiện mỗi giây, mỗi sự kiện 1.000 bay, cần chịu một máy hỏng và có lúc phải tính lại 30 ngày.” (0.97): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    # ── Đợt C hành trình: NET ──
    'Ở bài 2, tích băng thông nhân trễ là lượng dữ liệu đang bay cần để lấp đầy đường, ví dụ 100 triệu bit mỗi giây nhân 50 mi li giây được 625 nghìn byte.':
        'ASR chép “Ở bài 2, tích bằng thông nhân trễ là lượng dữ liệu đang bay cần để lấp đầy đường, ví dụ 100 triệu bit mỗi dây nhân 50 mili dây được 625.000 bay.” (0.889): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: băng/bằng — NOT_VERIFIED bằng tai người',
    'Bài báo năm 1988 cho bốn kết nối TCP cũ chia một đường 25 nghìn byte mỗi giây.':
        'ASR chép “Bài báo năm 1988 cho bốn kết nối TCP, cụ chia một đường 25.000 bai mỗi giây.” (0.923): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: cũ/cụ — NOT_VERIFIED bằng tai người',
    'Chia đều thì mỗi kết nối được 25 chia 4, khoảng 6 nghìn byte mỗi giây.':
        'ASR chép “Chia đều thì mỗi kết nối được 25 chi 4, khoảng 6.000 bai mỗi giây.” (0.889): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: chia/chi — NOT_VERIFIED bằng tai người',
    'Phần biến mất là 6 phẩy 5 nghìn byte mỗi giây, nguồn ghi tròn là 6.':
        'ASR chép “Phần biến mất là 6,5000 bai mỗi giây, nguồn ghi tròn là 6.” (0.938): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Bước bốn, trên đường thật năm 1988 thông lượng đạt 16 nghìn byte mỗi giây, so với 7 khi không có khởi động chậm, gấp khoảng 2 phẩy 3 lần.':
        'ASR chép “Bước 4, trên đường thật năm 1988 thông lượng đạt 16.000 bay mỗi giây so với 7 khi không có khởi động chậm, gấp khoảng 2,3 lần.” (0.973): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Bước một, tích băng thông nhân trễ là 10 mũ 10 nhân 0 phẩy 1 chia 8, bằng 125 triệu byte phải đang bay.':
        'ASR chép “Bước 1, tích băng thông nhân trở là 10 mũ 10 nhân không phải 1 chia 8 bằng 125 triệu bay phải đang bay.” (0.893): “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: trễ/trở — NOT_VERIFIED bằng tai người',
    'Bước bốn, đường vào nhà 10 triệu bit mỗi giây, vòng 40 mi li giây, có tích là 50 nghìn byte, khoảng 33 gói nếu mỗi gói 1500 byte, một số minh hoạ.':
        'ASR chép “Bước 4, đường vào nhà 10 triệu bit mỗi giây, vòng 40 mili giây, có tích là 50.000 bay, khoảng 33 gói nếu mỗi gói 1.500 bay, một số minh họa.” (0.911): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Bộ chuẩn khuyên dùng 10 lần kích thước gói lớn nhất, nhưng không vượt số lớn hơn trong hai số, 14 nghìn 720 byte và 2 lần kích thước gói.':
        'ASR chép “Bộ chuẩn khuyên dùng 10 lần kích thước gói lớn nhất, nhưng không vượt số lớn hơn trong 2 số, 14723 và 2 lần kích thước gói.” (0.971): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Với gói 1200 byte, 10 lần là 12 nghìn, còn giới hạn là 14 nghìn 720, nên cửa sổ đầu là 12 nghìn byte.':
        'ASR chép “Với gói 1.200 bay, 10 lần là 12.000, còn giới hạn là 14.720, nền cửa sổ đầu là 12.000 bay.” (0.909): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: nên/nền — NOT_VERIFIED bằng tai người',
    'Với gói 1472 byte, 10 lần vừa đúng 14 nghìn 720.':
        'ASR chép “với có 1.472 bai 10 lần vừa đúng 14.720.” (0.905): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: gói/có — NOT_VERIFIED bằng tai người',
    'Với 125 triệu byte, đổi trước tốc độ ra byte, 10 tỉ bit mỗi giây là 1 phẩy 25 tỉ byte, nhân 0 phẩy 1 giây được 125 triệu byte.':
        'ASR chép “Với 125 triệu bay, đổi trước tốc độ ra bay, 10 tỷ bích mỗi giây là 1,25 tỷ bay, nhận không phải 1 giây được 125 triệu bay.” (0.775): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); “tỉ” ASR viết chính tả “tỷ” (cùng âm); “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; lệch âm/thanh thuần Việt: bit (trong “tỉ bit” → “tỷ bích”), nhân (trong “tỉ byte nhân” → “tỷ bay nhận”) — NOT_VERIFIED bằng tai người',
    'Với bộ đệm, một gói 1500 byte qua đường 10 triệu bit mỗi giây mất 1 phẩy 2 mi li giây, nên 1000 gói mất 1 phẩy 2 giây.':
        'ASR chép “Với Bộ Đềm, 1 gói 1.503 qua đường 10 triệu biết mỗi dây mất 1,20 li dây nên 1.000 gói mất 1,2 dây.” (0.866): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; lệch âm/thanh thuần Việt: đệm/đềm, bit/biết — NOT_VERIFIED bằng tai người',
    'Năm 1988, khi không có quy tắc chung, một kết nối chỉ còn 0 phẩy 5 nghìn byte mỗi giây trong khi kết nối khác được 8.':
        'ASR chép “Năm 1988, khi không có quy tắc chung, một kết nối chỉ còn 0,5.000 bai mỗi giây trong khi kết nối khác được 8.” (0.97): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Câu một, ứng dụng di động gửi phản hồi đầu tiên 20 nghìn byte qua giao thức mới, gói 1200 byte, mỗi vòng 80 mi li giây.':
        'ASR chép “Câu 1, ứng dụng di động gửi phản hồi đầu tiên 20.000 bai qua giao thức mới gói 1.200 bai mỗi vòng 80.000 ly dây.” (0.875): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh — NOT_VERIFIED bằng tai người',
    'Có nên cắt phản hồi đầu xuống 12 nghìn byte không?':
        'ASR chép “Có nên cắt phản hồi đầu xuống 12.000 bay không?” (0.917): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Giữ 20 nghìn byte thì đủ dữ liệu ngay, nhưng cửa sổ đầu chỉ 12 nghìn byte, còn 8 nghìn byte phải chờ thêm 1 vòng, tức 80 mi li giây.':
        'ASR chép “Giữ 20.000 bai thì đủ dữ liệu ngay, nhưng cửa sổ đầu chỉ 12.000 bai, còn 8.000 bai phải chờ thêm một vòng, tức 80 mili giây.” (0.866): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh — NOT_VERIFIED bằng tai người',
    'Cắt xuống 12 nghìn byte thì xong trong 1 vòng, đổi lại phải tách phản hồi và gửi phần sau khi cần.':
        'ASR chép “Cắt xuống 12.000 bay thì xong trong một vòng, đổi lại phải tách phản hội và gửi phần sau khi cần.” (0.913): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: hồi/hội — NOT_VERIFIED bằng tai người',
    # ── Đợt C hành trình: WEB ──
    'Ở bài 10, thời gian tải bằng kích thước chia tốc độ, 2000 KB ở 200 KB mỗi giây mất 10 giây.':
        'ASR chép “Ở bài 10, thời gian tải bằng kích thước chia tốc độ 2.000 kB ở 200 kB mỗi giây mất 10 giây.” (1.0): KB đọc “ki-lô-byte” theo lexicon của khoá, ASR viết “KB/kilobyte” — NOT_VERIFIED bằng tai người',
    'Đếm vòng với trang 1 tệp và 10 ảnh, tải lần lượt, mỗi vòng 50 mi li giây.':
        'ASR chép “Đếm vòng với trang 1 tẹp và 10 ảnh tại lần lượt mỗi vòng 50 mì ly giây.” (0.789): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; lệch âm/thanh thuần Việt: tệp/tẹp, tải/tại — NOT_VERIFIED bằng tai người',
    'Làm thử với số minh hoạ, 100 yêu cầu, mỗi tiêu đề 500 byte, và cửa sổ đầu 10 gói, mỗi gói 1460 byte, nhân đôi mỗi vòng như ở khoá mạng.':
        'ASR chép “Làm thử với số minh họa, 100 yêu cầu, mỗi tiêu đề 500 bai và cửa sổ đầu 10 gói, mỗi gói 1460 bai, nhân đôi mỗi vòng như ở khóa mạng.” (0.949): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Bước một, tiêu đề không nén tổng cộng 50 nghìn byte.':
        'ASR chép “Bước 1, tiêu đề không nén tổng cộng 50.000 bay.” (0.917): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Bước hai, cửa sổ đầu là 14 nghìn 600 byte.':
        'ASR chép “Bước 2, cửa sổ đầu là 14.600 bay.” (0.917): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Bước bốn, nếu nén để mỗi tiêu đề lặp lại chỉ còn 20 byte, tổng là 2480 byte, gửi trong 1 vòng.':
        'ASR chép “Bước 4, nếu nén để mỗi tiêu đề lập lại chỉ còn 20 byte, tổng là 2.483, gửi trong 1 vòng.” (0.929): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: lặp/lập — NOT_VERIFIED bằng tai người',
    'Với tiêu đề, sau 2 vòng mới gửi được 43 nghìn 800 byte, chưa đủ 50 nghìn, nên phải tới vòng 3.':
        'ASR chép “Với tiêu đề, sau 2 vòng mới gửi được 43.800 bai, chưa đủ 50.000 nên phải tới vòng 3.” (0.962): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Mỗi kết nối tốn tài nguyên máy chủ, và TCP không chia kiểm soát tắc nghẽn giữa các kết nối, nên 6 kết nối mỗi cái 10 gói đầu là 60 gói ồ ạt, một số minh hoạ.':
        'ASR chép “Mỗi kết nối tốn tại nguyên máy chủ và TCP không chia kiểm soát tắt ngạn giữa các kết nối nên 6 kết nối mỗi cái 10 gói đầu là 60 gói oạt, một số minh họa.” (0.883): lệch âm/thanh thuần Việt: tài/tại, tắc nghẽn/tắt ngạn, ồ ạt/oạt — NOT_VERIFIED bằng tai người',
    # ── Đợt C hành trình: SEC ──
    'Bốn năm sau, 72 tới 95 phần trăm lượt tải trang đã dùng HTTP có mã hoá.':
        'ASR chép “Bốn năm sau, 72 tới 95% lượt tại trang đã dùng Http có mã hóa.” (0.952): lệch âm/thanh thuần Việt: tải/tại — NOT_VERIFIED bằng tai người',
    'Ở bài 11, đọc quá biên một vùng nhớ làm lộ ô bên cạnh, mảng 16 byte mà đọc 20 byte là lộ 4 byte kề bên.':
        'ASR chép “Ở bài 11, Đọc Quá Biên một vùng nhớ làm lộ ô bên cạnh, mảng 16 bài mà đọc 20 bài là lộ 4 bài kề bên.” (0.9): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Điểm nghẽn nằm ở một thông điệp nhịp tim có trường độ dài 2 byte, mà bản cài đặt thiếu kiểm biên.':
        'ASR chép “điểm ngãn nằm ở một thông điệp nhịp tim có trường độ dài hai vai mà bản cài đặt thiếu kiễn biên.” (0.864): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: nghẽn/ngãn, kiểm/kiễn — NOT_VERIFIED bằng tai người',
    'Vì vậy máy chủ có thể trả về phần bộ nhớ nằm sau dữ liệu thật, tối đa khoảng 64 KB.':
        'ASR chép “Vì vậy máy chủ có thể trả về phần bộ nhớ nằm sau dữ liệu thật, tối đa khoảng 64 kilobytes.” (0.957): KB đọc “ki-lô-byte” theo lexicon của khoá, ASR viết “kilobyte/kg” — NOT_VERIFIED bằng tai người',
    'Bước một, trường độ dài 2 byte là 2 nhân 8, bằng 16 bit, nên có 2 mũ 16 giá trị, tức 65 nghìn 536 byte, chia 1024 được 64 KB.':
        'ASR chép “Bước 1, trường độ dài 2 bai là 2 x 8, bằng 16 bit, nền có 2 mũ 16 giá trị, tức 65536 bai, chi 1.024 được 64 kilobai.” (0.872): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); KB đọc “ki-lô-byte” theo lexicon của khoá, ASR viết “kilobyte/kg”; lệch âm/thanh thuần Việt: nhân/x, nên/nền, chia (trong “byte chia” → “bai chi”) — NOT_VERIFIED bằng tai người',
    'Mỗi byte có 256 giá trị, nên hai byte có 256 nhân 256, bằng 65 nghìn 536.':
        'ASR chép “Mỗi bài có 256 giá trị, nên hai bài có 256 nhân 256 vàng 65.536.” (0.914): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: bằng/vàng — NOT_VERIFIED bằng tai người',
    'Năm 2014, một chỗ thiếu kiểm biên làm lộ tới 64 KB bộ nhớ, việc vá thì nhanh nhưng thay khoá thì chậm.':
        'ASR chép “Năm 2014, một chỗ thiếu kiểm biên làm lộ tới 64 kilobyte bộ nhớ, việc vá thì nhanh nhưng thay khóa thì chậm.” (0.967): KB đọc “ki-lô-byte” theo lexicon của khoá, ASR viết “kilobyte/kg” — NOT_VERIFIED bằng tai người',
    'Điều cần mang theo, an toàn ở quy mô cả web không đến từ việc dặn mọi người cẩn thận hơn, mà từ việc làm cho cách an toàn trở thành cách dễ nhất và tự động.':
        'ASR chép “Điều cần mang theo, an toàn ở quy mô cả oét không đến từ việc dặn mọi người cẩn thận hơn mà từ việc làm cho cách an toàn trở thành cách dễ nhất và tự động.” (0.973): web đọc thô (probe NET p2: 8/8), lần này ASR viết sai — NOT_VERIFIED bằng tai người',
    # ── Đợt C hành trình: DVO ──
    'Nó ghi rằng triển khai thường là điểm đau lớn nhất khiến các đội bắt đầu làm DevOps.':
        'ASR chép “Nó ghi rằng triển khai thường là điểm đau lớn nhất khiến các đội bắt đầu làm Devo” (0.944): DevOps đọc thô (probe DVO p1: 6/8, NOT_VERIFIED) — NOT_VERIFIED bằng tai người',
    # ── Đợt C hành trình: DEN ──
    'Bước hai, bài sắp xếp có 10 mũ 10 bản ghi, mỗi bản 100 byte.':
        'ASR chép “Bước 2, bài sắp xếp có 10 mũ 10 bản ghi, mỗi bản 100 bay.” (0.938): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    # ── Đợt C hành trình: SWF ──
    'Bước ba, với một đồ thị phụ thuộc nhỏ, sửa thư viện chung thì chạy kiểm thử của cả hai dự án, còn sửa dự án A chỉ chạy kiểm thử của A.':
        'ASR chép “Bước 3. Với 1 đồ thi phụ thuộc nhỏ, sửa thư viện chung thì chạy kiểm thử của cả 2 dự án, còn sửa dự án A chỉ chạy kiểm thử qua.” (0.923): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: thị/thi, của (trong “của a” → “qua”) — NOT_VERIFIED bằng tai người',
    # ── Đợt C hành trình: CLC ──
    'Chào bạn, năm 2006 Amazon ra mắt một kho lưu trữ đối tượng trên đám mây.':
        'ASR chép “Chào bạn, năm 2006, Amadron ra mắt một kho lưu trữ đối tượng trên đám mây.” (0.952): “Amazon” đọc thô (probe CLC p1: 8/8 nhưng đối chứng “A-ma-tôn” 5/8 — PARTIAL), ASR chép “Amadron/Amaroan/Amarone”, cần người nghe — NOT_VERIFIED bằng tai người',
    'Năm 2013, kho có 2 nghìn tỉ đối tượng, nhờ thiết kế thêm máy là thêm sức, rồi năm 2017 một lệnh gõ sai dẫn tới chặn mức tối thiểu và chia ô.':
        'ASR chép “Năm 2013, kho có 2.000 tỷ đối tượng, nhờ thiết kế thêm máy là thêm sức, rồi năm 2017 một lệnh gõ sai dẫn tới chặn mức tối thiểu và chiều.” (0.941): “tỉ” ASR viết chính tả “tỷ” (cùng âm); “ô” (ô lưới) ASR viết chữ “O”; lệch âm/thanh thuần Việt: chia (trong “chia ô” → “chiều”) — NOT_VERIFIED bằng tai người',
    'Hình này dựng theo bài tổng kết sự cố năm 2017 của Amazon.':
        'ASR chép “Hình này dựng theo bài tổng kết sự cố năm 2017 của Amaroan.” (0.944): “Amazon” đọc thô (probe CLC p1: 8/8 nhưng đối chứng “A-ma-tôn” 5/8 — PARTIAL), ASR chép “Amadron/Amaroan/Amarone”, cần người nghe — NOT_VERIFIED bằng tai người',
    'Giá năm 2006 là 0 phẩy 15 đô la mỗi GB mỗi tháng để lưu, và 0 phẩy 20 đô la mỗi GB truyền đi.':
        'ASR chép “Giá năm 2006 là 0,15 đô la mỗi Gigabyte mỗi tháng để lưu và 0,20 đô la mỗi Gigabyte truyền đi.” (0.938): GB đọc “ghi-ga-byte” theo lexicon của khoá, ASR viết “GB/gigabyte” — NOT_VERIFIED bằng tai người',
    'Bước hai, truyền đi 100 GB tốn 20 đô la.':
        'ASR chép “Bước 2, truyền đi 100GB tốn 20 đô la.” (1.0): GB đọc “ghi-ga-byte” theo lexicon của khoá, ASR viết “GB/gigabyte” — NOT_VERIFIED bằng tai người',
    'Bước bốn, một tệp 12 GB không vừa một đối tượng 5 GB, hai đối tượng chỉ chứa 10 GB, nên cần 3 đối tượng.':
        'ASR chép “Bước bốn, một tệp 12GB không vừa một đối tượng 5GB, hai đối tượng chỉ chứa 10GB, nên cần ba đối tượng.” (1.0): GB đọc “ghi-ga-byte” theo lexicon của khoá, ASR viết “GB/gigabyte” — NOT_VERIFIED bằng tai người',
    'Bước một, 200 nghìn tỉ chia 800 triệu được 250 nghìn lần, khớp con số Amazon công bố.':
        'ASR chép “Bước 1, 200.000 tỷ chia 800 triệu được 250.000 lần, khớp con số Amarone công bố.” (0.913): “tỉ” ASR viết chính tả “tỷ” (cùng âm); “Amazon” đọc thô (probe CLC p1: 8/8 nhưng đối chứng “A-ma-tôn” 5/8 — PARTIAL), ASR chép “Amadron/Amaroan/Amarone”, cần người nghe — NOT_VERIFIED bằng tai người',
    # ── Đợt C hành trình: LLM ──
    'Chuỗi 4 từ tố có 1 cộng 2 cộng 3 cộng 4, bằng 10 ô được phép.':
        'ASR chép “Chủi 4 từ tố có 1 cọng, 2 cọng, 3 cọng, 4, bằng 10 ô được phép.” (0.765): lệch âm/thanh thuần Việt: chuỗi/chủi, cộng/cọng, cộng/cọng, cộng/cọng — NOT_VERIFIED bằng tai người',
    'Ở bài 5, số tham số xấp xỉ 12 nhân L nhân d bình phương, nên L bằng 2, d bằng 2 cho 96.':
        'ASR chép “Ở bài năm, số tham số sắp sĩ 12 nhân L nhân dế bình phương nên L bằng 2, dê bằng 2 cho 96.” (0.889): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: xấp xỉ/sắp sĩ — NOT_VERIFIED bằng tai người',
    'Ngân sách ấy chia cho hai cái núm, số tham số N làm mô hình to hơn, và số từ tố D làm mô hình đọc nhiều hơn.':
        'ASR chép “Ngân sách ấy chia cho hai cái núng, số tham số N làm mô hình to hơn và số từ tố G làm mô hình độc nhiều hơn.” (0.893): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: núm/núng, đọc/độc — NOT_VERIFIED bằng tai người',
    'Đầu năm 2020, một nhóm nghiên cứu huấn luyện rất nhiều mô hình nhỏ, và thấy mất mát giảm theo hàm lũy thừa của N, D và C, với xu hướng trải hơn bảy bậc độ lớn.':
        'ASR chép “Đầu năm 2020, một nhóm nghiên cứu huấn luyện rất nhiều mô hình nhỏ và thấy mất mát giảm theo hàm lụy thừa của N, G và C, với xu hướng trải hơn 7 bậc độ lớn.” (0.952): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: luỹ/luỵ — NOT_VERIFIED bằng tai người',
    'Quy mô do ngân sách quyết định, nên hãy tính 6 N D với số thẻ, số ngày của chính mình.':
        'ASR chép “Quy mô do ngân sách quyết định nên hãy tính 6 energy với số thẻ số ngày của chính mình.” (0.927): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Cách A dùng 2 tỉ tham số và 40 tỉ từ tố, cách B dùng 8 tỉ tham số và 10 tỉ từ tố.':
        'ASR chép “Cách A dùng 2 tỷ tham số và 40 tỷ tư tố, cách B dùng 8 tỷ tham số và 10 tỷ tư tố.” (0.76): “tỉ” ASR viết chính tả “tỷ” (cùng âm); lệch âm/thanh thuần Việt: từ (trong “tỉ từ” → “tỷ bốn”), từ (trong “tỉ từ” → “tỷ bốn”) — NOT_VERIFIED bằng tai người',
    'Năm 2022, mô hình Chinchilla cho thấy N và D nên tăng bằng nhau, và dữ liệu tốt trở thành nút thắt mới.':
        'ASR chép “Năm 2022, mô hình Chinchilla cho thấy N và Z nên tăng bằng nhau và dữ liệu tốt trở thành nút thác mới.” (0.931): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: thắt/thác — NOT_VERIFIED bằng tai người',
    # ── Đợt C hành trình: AIF ──
    'Không chắc chắn về thế giới thì dùng mạng Bayes.':
        'ASR chép “không chắc chắn về thế giới thì dùng mạng bayát.” (0.9): “Bayes” đọc “Bay-ét” theo lexicon chung, ASR chép “bayát” — cùng dáng âm — NOT_VERIFIED bằng tai người',
    'Ta sẽ thấy mỗi chặng tìm kiếm và học được kết hợp ra sao.':
        'ASR chép “Ta sẽ thấy mỗi chặn tìm kiếm và học được cất hợp ra sau.” (0.786): lệch âm/thanh thuần Việt: chặng/chặn, kết/cất, sao/sau — NOT_VERIFIED bằng tai người',
    'Dùng lôgarit cơ số 10, con số đó xấp xỉ 10 mũ 123 nút.':
        'ASR chép “Dùng Logatricker số 10, còn số đó sắp xỉ 10 mũ 123 nút.” (0.8): lệch âm/thanh thuần Việt: lôgarit cơ/logatricker, con/còn, xấp/sắp — NOT_VERIFIED bằng tai người',
    'Câu một, dùng cực đại cực tiểu với hàm đánh giá viết tay thì nhìn trước được mấy lượt, có và không có alpha beta?':
        'ASR chép “Câu 1, dùng cực đại cực tiểu với hàm đánh giá viết tay thì nhìn trước được mấy lượt, có và không có an pha beta.” (0.906): beta đọc “bê-ta”, ASR viết “bê/beta”; alpha đọc thô (probe AIF p1: 7/8, bản chép “an pha / ANFA / α”) — NOT_VERIFIED bằng tai người',
    # ── Đợt C hành trình: SAR ──
    'Về sau, Twitter nhận hơn 500 triệu bài đăng mỗi ngày, và một bài đăng 140 ký tự cỡ khoảng 200 byte.':
        'ASR chép “Về sau, Twitter nhận hơn 500 triệu bài đăng mỗi ngày và một bài đăng 140 ký tự cỡ khoảng 200 bài.” (0.963): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Bước một, 500 triệu nhân 200 byte được 100 GB mỗi ngày.':
        'ASR chép “Bước 1, 500 triệu nhân 200 byte được 100 gigabyte mỗi ngày.” (0.933): GB đọc “ghi-ga-byte” theo lexicon của khoá, ASR viết “GB/gigabyte” — NOT_VERIFIED bằng tai người',
    'Gom 5 bài đăng thì được 1000 byte, tức 1 KB, nên 500 triệu bài đăng là 100 triệu KB, đúng 100 GB.':
        'ASR chép “Gom 5 bài đăng thì được 1.000 bài, tức 1 kilobyte, nên 500 triệu bài đăng là 100 triệu kilobyte, đúng 100 gigabyte.” (0.852): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); KB đọc “ki-lô-byte” theo lexicon của khoá, ASR viết “kilobyte/kg”; GB đọc “ghi-ga-byte” theo lexicon của khoá, ASR viết “GB/gigabyte” — NOT_VERIFIED bằng tai người',
    'Hãy theo dõi tỉ lệ lỗi và độ trễ đuôi, báo động khi tỉ lệ đổi.':
        'ASR chép “Hãy theo dõi tỷ lệ lỗi và độ trễ đuôi, báo đồng khi tỷ lệ đuỗi.” (0.75): “tỉ” ASR viết chính tả “tỷ” (cùng âm); lệch âm/thanh thuần Việt: động/đồng, đổi/đuỗi — NOT_VERIFIED bằng tai người',
    # ── Đợt C hành trình: MLO ──
    'Nợ ẩn nguy hiểm vì nó lãi chồng lãi trong im lặng.':
        'ASR chép “Nờ ẩn nguy hiểm vì nó lại chồng lại trong im lặng.” (0.75): lệch âm/thanh thuần Việt: nợ/nờ, lãi/lại, lãi/lại — NOT_VERIFIED bằng tai người',
    # ── Đợt C hành trình: DAN ──
    'Lệch tỉ lệ chia nhóm là khi số người thật trong mỗi nhóm khác hẳn tỉ lệ đã đặt.':
        'ASR chép “Lạc tỷ lệ chi nhóm là khi số người thật trong mỗi nhóm khác hẳn tỷ lệ đã đặt.” (0.789): “tỉ” ASR viết chính tả “tỷ” (cùng âm); lệch âm/thanh thuần Việt: lệch (trong “lệch tỉ” → “lạc tỷ”), chia/chi — NOT_VERIFIED bằng tai người',
    'Cách xử lý là hạ ngưỡng giá trị p, và chạy lại một lần cuối với độ mạnh cao hơn.':
        'ASR chép “Cách xử lý là hạ ngưỡng giá trị T và chạy lại một lần cuối với độ mạnh cao hơn.” (0.95): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    # ── Đợt C hành trình: BCH ──
    'Chào bạn, năm 2008, sách trắng của Nakamoto tính rằng mỗi khối chỉ thêm một tiêu đề 80 byte, 10 phút một khối, nên mỗi năm chỉ thêm 4 phẩy 2 MB.':
        'ASR chép “Chào bạn! Năm 2008, sách trắng của Nakamoto tính rằng mỗi khối chỉ thêm 1 tiêu đe 80 bai, 10 phút 1 khối, nên mỗi năm chỉ thêm 4,2 MB.” (0.947): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: đề/đe — NOT_VERIFIED bằng tai người',
    'Năm 2015, có một khối mất tới 25 giây chỉ để kiểm chữ ký, trong khi mỗi khối bị giới hạn một triệu byte.':
        'ASR chép “Năm 2015, có một khối mất tới 25 giây chỉ để kiểm chữ ký trong khi mỗi khối bị giới hạn 1 triệu bay.” (0.968): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Ở bài 2, cây Merkle chứng minh một giao dịch thuộc khối 1024 giao dịch bằng 10 mã băm, 320 byte.':
        'ASR chép “Ở bài 2, Cây mơ cổ chứng minh một giao dịch thuộc hối 1024 giao dịch bằng 10 mã băm, 320 bay.” (0.903): Merkle đọc “Mơ-cồ” theo lexicon BCH, ASR viết “mơ cổ”; byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: khối/hối — NOT_VERIFIED bằng tai người',
    'Ở bài 10, khối một triệu byte, giao dịch 250 byte, chứa được 4000 giao dịch.':
        'ASR chép “Ở bài 10, khối 1 triệu bài, giao dịch 250 bài, chữa được 4.000 giao dịch.” (0.85): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: chứa (trong “byte chứa” → “bài chữa”) — NOT_VERIFIED bằng tai người',
    'Nhân chứng có cây Merkle riêng, và gốc của cây này vẫn được ghi vào khối, như gốc cây giao dịch ở bài 2.':
        'ASR chép “Nhân chứng có cây mơ cổ riêng và gốc của cây này vẫn được ghi vào khối như gốc cây giao dịch ở bài 2.” (0.96): Merkle đọc “Mơ-cồ” theo lexicon BCH, ASR viết “mơ cổ” — NOT_VERIFIED bằng tai người',
    'Nút nhẹ chỉ giữ tiêu đề và nhánh Merkle nối giao dịch với khối, nên không cần chạy nút đầy đủ.':
        'ASR chép “Nút nhẹ chỉ giữ tiêu đề và nhánh mơ cô nối giao dịch với khối, nên không cần chạy nút đầy đủ.” (0.955): Merkle đọc “Mơ-cồ” theo lexicon BCH, ASR viết “mơ cổ” — NOT_VERIFIED bằng tai người',
    'Bước ba, nhân với 80 byte được 4 triệu 204 nghìn 800 byte, khoảng 4 phẩy 2 MB.':
        'ASR chép “Bước 3, nhân với 80 by được 4.200.000 linh 4.800 by, khoảng 4.2 megabyte.” (0.826): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; MB đọc “mê-ga-byte” theo lexicon của khoá, ASR viết “MB/megabyte” — NOT_VERIFIED bằng tai người',
    'Bước bốn, bộ nhớ 2 tỉ byte của máy năm 2008 chứa được khoảng 475 năm tiêu đề.':
        'ASR chép “Bước 4, bộ nhớ 2 tỷ bay của máy năm 2008 chứa được khoảng 475 năm tiêu đề.” (0.926): “tỉ” ASR viết chính tả “tỷ” (cùng âm); byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Thực hành rút ra là nút nhẹ kiểm thanh toán bằng tiêu đề và nhánh Merkle.':
        'ASR chép “Thực hành trúc tra là nút nhẹ kiểm thanh toán bằng tiêu đề và nhánh mơ cô.” (0.824): Merkle đọc “Mơ-cồ” theo lexicon BCH, ASR viết “mơ cổ”; lệch âm/thanh thuần Việt: rút ra/trúc tra — NOT_VERIFIED bằng tai người',
    'Thứ nhất, khối giới hạn một triệu byte, khoảng 6 phẩy 7 giao dịch mỗi giây như bài 10.':
        'ASR chép “Thứ nhất, khối giới hạn 1 triệu bay khoảng 6,7 giao dịch mỗi giây như bài 10.” (0.947): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Nói cách khác, mỗi byte nhân chứng nặng 1, còn mỗi byte khác nặng 4.':
        'ASR chép “Nói cách khác, mỗi bay nhân chứng nặng 1, còn mỗi bay khác nặng 4.” (0.867): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Bước hai, giao dịch 250 byte có 100 byte chữ ký, một số minh hoạ, thì trọng lượng là 3 nhân 150 cộng 250, bằng 700.':
        'ASR chép “Bước 2, giao dịch 250 bai có 100 bai chữ ký, một số minh họa thì trọng lượng là 3 nhân 150 cộng 250 bằng 700.” (0.946): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Đếm theo byte, 150 byte cơ sở nặng 4 là 600, cộng 100 byte nhân chứng nặng 1 được 700.':
        'ASR chép “Đếm theo bay, 150 bay cơ sở nặng 4 là 600, cộng 100 bay nhân chứng nặng 1 được 700.” (0.885): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Hãy sửa cơ chế trước, và đo thời gian kiểm chứ không chỉ đo số byte.':
        'ASR chép “Hãy sửa cơ chế trước và đo thời gian kiểm chứ không chỉ đo số bay.” (0.938): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    # ── Đợt C hành trình: OSY ──
    'Cứ thế, sau 6 lượt 4 mi li giây, cả ba được đúng 8 mi li giây mỗi tác vụ.':
        'ASR chép “Cứ thế, sau 6 lực 4 mili giây, cả 3 được đúng 8 mili giây mỗi tác vụ.” (0.789): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; lệch âm/thanh thuần Việt: lượt/lực — NOT_VERIFIED bằng tai người',
    'Đổi sang mi li giây, mỗi mi li giây một lần chọn, mỗi lần xem 1000 tiến trình, trong 1000 mi li giây là đúng một triệu lần.':
        'ASR chép “Đổi sang mili giây, mỗi mili giây một lần chọn, mỗi lần xe 1.000 tiến trình, trong 1.000 mili giây là đúng 1 triệu lân.” (0.772): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; lệch âm/thanh thuần Việt: xem/xe, lần/lân — NOT_VERIFIED bằng tai người',
    'Hãy đo trước, còn nếu thử thì dùng chế độ từng phần, giữ đường cũ dự phòng.':
        'ASR chép “Hãy đo trước, còn nếu thử thì dùng chế độ tương phân giữ đường củ dự phong.” (0.765): lệch âm/thanh thuần Việt: từng phần/tương phân, cũ/củ, phòng/phong — NOT_VERIFIED bằng tai người',
    # ── Đợt C hành trình: CSA ──
    'Ở bài 13, định luật Amdahl nói phần tuần tự quyết định giới hạn, 90% song song được thì 8 lõi chỉ nhanh khoảng 4 phẩy 71 lần.':
        'ASR chép “Ở bài 13, định luật am đang nói phần tuần tự quyết định giới hạn, 90% song song được thì 8 loại chỉ nhanh khoảng 4,71 lần.” (0.943): lệch âm/thanh thuần Việt: lõi/loại; “Amdahl” đọc “Am-đan” theo lexicon_vi.CSA.yaml (probe p1 8/8), ASR chép “âm đàn/am đang” — cùng âm — NOT_VERIFIED bằng tai người',
    'Bài báo năm 2005 viết hai lõi 3 tỉ nhịp không bằng một lõi 6 tỉ nhịp.':
        'ASR chép “Bài báo năm 2000, 0505 viết 2 loại 3 tỉ nhiệt, không bằng 1 loại 6 tỉ nhiệt.” (0.773): lệch âm/thanh thuần Việt: không/năm, lõi/loại, nhịp/nhiệt, lõi/loại, nhịp/nhiệt — NOT_VERIFIED bằng tai người',
    'Hãy tính theo Amdahl trước khi mua thêm lõi.':
        'ASR chép “Hãy tính theo âm đàn trước khi mua thêm lõi.” (0.842): “Amdahl” đọc “Am-đan” theo lexicon_vi.CSA.yaml (probe p1 8/8), ASR chép “âm đàn/am đang” — cùng âm — NOT_VERIFIED bằng tai người',
    'Từ 2005, tốc độ đến từ đa nhân, và định luật Amdahl quyết định ta được bao nhiêu.':
        'ASR chép “Từ 2000 linh năm, tốc độ đến từ đa nhân và định luật am đang quyết định ta được bao nhiêu?” (0.913): lệch âm/thanh thuần Việt: không trăm/∅; “Amdahl” đọc “Am-đan” theo lexicon_vi.CSA.yaml (probe p1 8/8), ASR chép “âm đàn/am đang” — cùng âm — NOT_VERIFIED bằng tai người',
    'Bạn đã đi từ bit và số nguyên, qua mạch lô-gích, tập lệnh, hiệu năng và đường ống.':
        'ASR chép “Bạn đã đi từ bích và số nguyên qua mặt logics, tập lệnh, hiểu năng và đường ống.” (0.757): “lô-gích” ASR viết gộp “logics”; lệch âm/thanh thuần Việt: bit/bích, mạch gích (trong “mạch lô gích” → “mặt logics”), hiệu/hiểu — NOT_VERIFIED bằng tai người',
    # ── Đợt C hành trình: TOC ──
    'Bạn sẽ thấy chọn sai cách chạy ô-tô-mát có thể làm sập cả một hệ thống rất lớn.':
        'ASR chép “Bạn sẽ thấy chọn sai cách chạy Otomac có thể làm sập cả một hệ thống rất lớn.” (0.895): “ô” (ô lưới) ASR viết chữ “O”; “ô-tô-mát” ASR viết theo dạng tiếng Anh “automa/otomac” — đúng thuật ngữ, khác cách viết — NOT_VERIFIED bằng tai người',
    'Chào bạn, ngày 2 tháng 7 năm 2019, Cloudflare cập nhật một quy tắc của tường lửa ứng dụng.':
        'ASR chép “Chào bạn, ngày 2 tháng 7 năm 2019, Kehlaufler cập nhật một quy tắc của tường lửa ứng dụng.” (0.958): “Cloudflare” đọc “Cờ-lao-phle-ơ” theo lexicon_vi.TOC.yaml (probe p3 6/8, dưới ngưỡng — NOT_VERIFIED), ASR chép biến thể “Kehlaufler/Klauffler” — NOT_VERIFIED bằng tai người',
    'Hôm nay ta đi qua năm chặng từ 1968 tới 2025, để thấy lý thuyết ô-tô-mát của khoá này cứu được những hệ thống rất lớn.':
        'ASR chép “Hôm nay, ta đi qua năm chặn từ 1968 tới 2025 để thấy lý thuyết automa của khóa này cứu được những hệ thống rất lớn.” (0.923): “ô” (ô lưới) ASR viết chữ “O”; lệch âm/thanh thuần Việt: chặng/chặn; “ô-tô-mát” ASR viết theo dạng tiếng Anh “automa/otomac” — đúng thuật ngữ, khác cách viết — NOT_VERIFIED bằng tai người',
    'Ở bài 3, biểu thức chính quy có ba phép hoặc, ghép, sao, và mô tả cùng lớp ngôn ngữ với ô-tô-mát.':
        'ASR chép “Ở bài 3, biểu thức chính quy có 3 phép hoặc, ghép, sao và mô tả cùng lớp ngôn ngữ với Automat.” (0.913): “ô” (ô lưới) ASR viết chữ “O”; “ô-tô-mát” ASR viết theo dạng tiếng Anh “automa/otomac” — đúng thuật ngữ, khác cách viết — NOT_VERIFIED bằng tai người',
    'Bước một, mỗi mẫu tốn khoảng 10 KB bộ nhớ, so với khoảng nửa KB, tức 0 phẩy 5 KB, của thư viện quay lui, tức gấp 20 lần.':
        'ASR chép “Bước 1, mỗi mẫu tốn khoảng 10 kilobyte bầu nhớ so với khoảng nửa kilobyte tức 0,5 kilobyte của thư viện quay lui tức gấp 20 lần.” (0.867): KB đọc “ki-lô-byte” theo lexicon của khoá, ASR viết “kilobyte/kg”; lệch âm/thanh thuần Việt: bộ (trong “kb bộ” → “kilobyte bầu”) — NOT_VERIFIED bằng tai người',
    'Bước hai, nếu lưu 1000 mẫu, một số minh hoạ, thì cần 10 nghìn KB thay vì 500 KB.':
        'ASR chép “Bước 2, nếu lưu 1 nghìn mẫu, một số minh họa thì cần 10.000 Kb thay vì 500 Kb.” (1.0): KB đọc “ki-lô-byte” theo lexicon của khoá, ASR viết “KB/kilobyte” — NOT_VERIFIED bằng tai người',
    'Ở chặng bốn, bài hậu kiểm của Cloudflare ngày 12 tháng 7 năm 2019 cho biết đội quy tắc xử lý 476 thay đổi trong 60 ngày.':
        'ASR chép “Ở chặn 4, bài hậu kiểm của Klauffler ngày 12 tháng 7 năm 2019 cho biết đội quy tắc xử lý 476 thay đổi trong 60 ngày.” (0.947): lệch âm/thanh thuần Việt: chặng/chặn; “Cloudflare” đọc “Cờ-lao-phle-ơ” theo lexicon_vi.TOC.yaml (probe p3 6/8, dưới ngưỡng — NOT_VERIFIED), ASR chép biến thể “Kehlaufler/Klauffler” — NOT_VERIFIED bằng tai người',
    'Đổi lại, 200 mẫu nhân 10 KB là 2000 KB thay vì 100 KB, và không có tham chiếu ngược.':
        'ASR chép “Đổi lại, 200 mẫu nhân 10 kilobytes là 2.000 kilobytes thay vì 100 kilobytes và không có tham chiếu ngược.” (0.87): KB đọc “ki-lô-byte” theo lexicon của khoá, ASR viết “kilobyte/kg” — NOT_VERIFIED bằng tai người',
    'Lý thuyết ô-tô-mát của bài 2 và biểu thức chính quy của bài 3 không chỉ để thi, nó cho ta lời bảo đảm về thời gian.':
        'ASR chép “Lý thuyết Otomac của bài 2 và biểu thức chính quy của bài 3 không chỉ để thi, nó cho ta lời bảo đảm về thời gian.” (0.929): “ô” (ô lưới) ASR viết chữ “O”; “ô-tô-mát” ASR viết theo dạng tiếng Anh “automa/otomac” — đúng thuật ngữ, khác cách viết — NOT_VERIFIED bằng tai người',
    'Từ chuỗi và ô-tô-mát, qua văn phạm, máy Turing, bài toán không khả quyết và hai lớp P, NP, bạn đã đi một chặng dài.':
        'ASR chép “Từ chuỗi vào Automat, qua văn phạm, máy Turin, bài toán không khả quyết và hai lớp P, NP, bạn đã đi một chặng dài.” (0.846): “ô” (ô lưới) ASR viết chữ “O”; “ô-tô-mát” ASR viết theo dạng tiếng Anh “automat” — đúng thuật ngữ, khác cách viết; “Turing” đọc “Tua-rinh” theo lexicon_vi.TOC.yaml (cách viết tốt nhất 6/8), ASR chép “Turin” — NOT_VERIFIED bằng tai người',
    # ── Đợt C hành trình: CS112 ──
    'Khi đó hàm cần 41 ô ngăn xếp nhưng mã chỉ cấp 40, nên chương trình dừng vì vượt chỉ số mảng.':
        'ASR chép “Khi đó hàm cần 41 ôn ngăn xếp, nhưng mã chỉ cấp 40, nên chương trình dừng vì vượt chỉ số mãn.” (0.92): “ô” (ô lưới) ASR viết chữ “O”; lệch âm/thanh thuần Việt: mảng/mãn — NOT_VERIFIED bằng tai người',
    'Ở bài 23, mọi cách sắp xếp bằng so sánh cần ít nhất lôgarit cơ số 2 của n giai thừa phép so sánh.':
        'ASR chép “Ở bài 23, mọi cách sắp xếp bằng so sánh cận ít nhất Logatrix cơ số 2 của N giai thừa phép so sánh.” (0.923): lệch âm/thanh thuần Việt: cần/cận, lôgarit/logatrix — NOT_VERIFIED bằng tai người',
    # ── Đợt C hành trình: DMS ──
    'Năm 2017, cặp trùng đầu tiên của SHA-1, một hàm băm 160 bit, tốn khoảng 6 nghìn 500 năm tính trên bộ xử lý thường và 100 năm trên bộ xử lý đồ hoạ.':
        'ASR chép “Năm 2017, cặp trùng đầu tiên của SHA1, một hàm 3160 bit, tốn khoảng 6.500 năm tính trên bộ xử lý thường và 100 năm trên bộ xử lý đồ họa.” (0.967): lệch âm/thanh thuần Việt: băm/ba nghìn — NOT_VERIFIED bằng tai người',
    'Ở bài 19, với m ô thì khoảng 1 phẩy 18 nhân căn bậc hai của m khoá đã có một nửa khả năng va chạm.':
        'ASR chép “Ở bài 19, với M thì khoảng 1,18 nhân căn bật 2 của M khóa đã có một nửa khả năng va chạm.” (0.945): “ô” (ô lưới) ASR viết chữ “O”; lệch âm/thanh thuần Việt: bậc/bật — NOT_VERIFIED bằng tai người',
    'Hàm băm biến một tin dài bao nhiêu cũng được thành một mã băm có độ dài cố định n bit.':
        'ASR chép “Hàm băm biến một tin dài bao nhiêu cũng được thành một mả băm có độ dài cố định Enervics.” (0.878): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: mã/mả, bit (trong “n bit” → “enervics”) — NOT_VERIFIED bằng tai người',
    'SHA-1 thành chuẩn năm 1995, mã dài 20 byte, tức 160 bit, vét cạn cần 2 mũ 80 lần thử.':
        'ASR chép “SHA một thành chuẩn năm 1995, mã dài 20 byte, tức 160 bit, vét cạn cần hai mũ tám mưu lần thử.” (0.938): lệch âm/thanh thuần Việt: vét/véc, mươi/mưu — NOT_VERIFIED bằng tai người',
    'Từ 2006 tới 2015, viện tiêu chuẩn của Mỹ đặt lịch chuyển đổi và mở cuộc thi tìm hàm băm mới, rồi năm 2017 có cặp trùng đầu tiên của SHA-1.':
        'ASR chép “Từ 2006 tới 2015, Viện Tiêu chuẩn của Mỹ đặt lịch chuyển đổi và mở cuộc thi tìm hàm băm mới, rồi năm 2017 có cặp trùng đầu tiên của SHA1.” (1.0): Bayes đọc “Bay-ét” theo lexicon chung (probe 3/8, NOT_VERIFIED), ASR viết “bay X/S”; chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Năm 2017 và 2018, một hệ quản lý mã nguồn phát hiện va chạm trước, rồi chọn hàm 256 bit, và từ 2022 tới 2030 là giai đoạn rút hẳn SHA-1.':
        'ASR chép “Năm 2017 và 2018, một hệ quản lý mã nguồn phát hiện va chạm trước, rồi chọn hàm 256 bit, và từ 2022 tới 2030 là giai đoạn rút hẳn SHA1.” (1.0): Bayes đọc “Bay-ét” theo lexicon chung (probe 3/8, NOT_VERIFIED), ASR viết “bay X/S”; chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Nếu MD5 không có điểm yếu, muốn tìm va chạm phải vét cạn kiểu ngày sinh, với một máy băm một tỉ lần mỗi giây, một số minh hoạ.':
        'ASR chép “Nếu em đi nằm không có điểm yếu, muốn tìm va chạm phải vét cạn kiểu ngày sinh với một máy 31 tỷ lần mỗi giây, một số minh họa.” (0.806): “tỉ” ASR viết chính tả “tỷ” (cùng âm); lệch âm/thanh thuần Việt: vét/véc, băm/ba mươi; “MD5” đọc thô (probe p5 8/8), ASR chép “em đi năm/nằm” — đúng âm chữ cái — NOT_VERIFIED bằng tai người',
    'Điều kiện quan trọng, nếu MD5 chỉ dùng để phát hiện lỗi ngẫu nhiên khi truyền, không có ai cố ý làm giả, thì văn bản ấy vẫn coi là chấp nhận được.':
        'ASR chép “Điều kiện quan trọng, nếu em đi 5 chỉ dùng để phát hiện lỗi nẫu nhiên khi truyền, không có ai cố ý làm giả, thì văn bản ấy vẫn coi là chấp nhận được.” (0.928): lệch âm/thanh thuần Việt: ngẫu/nẫu; “MD5” đọc thô (probe p5 8/8), ASR chép “em đi” — đúng âm chữ cái — NOT_VERIFIED bằng tai người',
    'Lúc đó chưa ai có một cặp va chạm SHA-1 thật.':
        'ASR chép “Lúc đó chưa ai có một cặp va chạm FHA một thật.” (0.917): “SHA-1” đọc “ét-hát-a một” theo lexicon_vi.DMS.yaml (probe p6 7/8), ASR chép “fha” — cần người nghe — NOT_VERIFIED bằng tai người',
    'Dù vậy, ngày 15 tháng 3 năm 2006, viện yêu cầu thôi dùng SHA-1 cho chữ ký số càng sớm càng tốt, và sau năm 2010 thì bắt buộc dùng họ hàm băm thứ hai.':
        'ASR chép “Dù vậy, ngày 15 tháng 3 năm 2006, viện yêu cầu thôi dùng SHA1 cho chữ ký số càng sớm càng tốt và sau năm 2010 thì bắt buộc dùng họ hạm băm thứ 2.” (0.978): lệch âm/thanh thuần Việt: hàm/hạm — NOT_VERIFIED bằng tai người',
    'Ở chặng ba, năm 2017, SHA-1 vẫn được dùng rộng rãi cho chữ ký văn bản, cho chứng chỉ của các trang mạng, và trong một hệ quản lý phiên bản mã nguồn phổ biến.':
        'ASR chép “Ở chặng 3, năm 2017, SHA1 vẫn được dùng rộng rãi cho chữ ký văn bản, cho chứng chỉ của các trang mạng và trong một hệ quản lý phiên bản mã nguồn phổ biến.” (1.0): Bayes đọc “Bay-ét” theo lexicon chung (probe 3/8, NOT_VERIFIED), ASR viết “bay X/S”; chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Nhóm nghiên cứu năm 2017 trả lời bằng một cặp thật, hai tệp văn bản khác nội dung mà cùng mã SHA-1.':
        'ASR chép “Nhóm nghiên cứu năm 2017 trả lời bằng một cặp thật, hay tẹp văn bản khác nội dung mà cùng mã SHA1.” (0.929): lệch âm/thanh thuần Việt: hai tệp/hay tẹp — NOT_VERIFIED bằng tai người',
    'Ở chặng bốn, một hệ quản lý phiên bản mã nguồn phổ biến đặt tên mọi tệp, thư mục và phiên bản bằng mã SHA-1 của nội dung, nên đổi hàm băm là đổi tên của mọi thứ.':
        'ASR chép “Ở chặng 4, một hệ quản lý phiên bản mã nguồn phổ biến đặt tên mọi tệp, thư mục và phiên bản bằng mã sha 1 của nội dung nên đổi hàm băm là đổi tên của mọi thứ.” (1.0): Bayes đọc “Bay-ét” theo lexicon chung (probe 3/8, NOT_VERIFIED), ASR viết “bay X/S”; chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Nhưng họ vẫn ghi rằng SHA-1 còn yếu, vì tấn công sau có thể không vá được.':
        'ASR chép “Nhưng họ vẫn ghi rằng SHA 1 còn yếu, vì tấn công sau có thể không vá được.” (1.0): Bayes đọc “Bay-ét” theo lexicon chung (probe 3/8, NOT_VERIFIED), ASR viết “bay X/S”; chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Bước một, vét cạn kiểu ngày sinh của SHA-1 cần 2 mũ 80 lần thử, vì 160 chia 2 là 80.':
        'ASR chép “Bước 1, vẽ cạn kiểu ngày sinh của SHA 1 cần 2 mũ 80 lần thử vì 162 là 80.” (0.943): lệch âm/thanh thuần Việt: vét/vẽ, chia/∅ — NOT_VERIFIED bằng tai người',
    'Từ lời khuyên thôi SHA-1 năm 2006 tới cặp trùng thật năm 2017 là 11 năm, và người có nhiều tài nguyên có thể làm sớm hơn mà không công bố.':
        'ASR chép “Từ lời khuyên thôi XHA tháng 1 năm 2006 tới cặp trùng thật năm 2017 là 11 năm và người có nhiều tài nguyên có thể làm sớm hơn mà không công bố.” (0.989): từ rủi ro ét, hát, a cả hai mô hình viết khác (cách viết, không phải âm) — NOT_VERIFIED bằng tai người',
    'Câu hai, bản cài đặt phát hành ra ngoài kèm chữ ký số đang ký trên mã SHA-1, vậy đổi sang gì và chuyển thế nào?':
        'ASR chép “Câu 2, bản cài đã phát hành ra ngoài kèm chữ ký số đăng ký trên mạ SHA1, vậy đổi sang gì và chuyển thế nào?” (0.889): lệch âm/thanh thuần Việt: đặt/đã, đang/đăng, mã/mạ — NOT_VERIFIED bằng tai người',
    'Vì không ai cố ý làm giả, 64 bit hay MD5 đều đủ.':
        'ASR chép “Vì không ai cố ý làm giả, 64 biết hay em đi 5 đều đủ.” (0.848): lệch âm/thanh thuần Việt: bit/biết; “MD5” đọc thô (probe p5 8/8), ASR chép “em đi” — đúng âm chữ cái — NOT_VERIFIED bằng tai người',
    'Giữ SHA-1 tới khi bị ép thì hôm nay không tốn gì.':
        'ASR chép “Giữ SHA một tới khi bị ép thì hôm nay không tốn gì.” (1.0): Bayes đọc “Bay-ét” theo lexicon chung (probe 3/8, NOT_VERIFIED), ASR viết “bay X/S”; chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Năm 2017, cặp SHA-1 thật ra đời, nhanh hơn vét cạn khoảng 122 nghìn lần.':
        'ASR chép “Năm 2017, cặp SHA một thật ra đời, nhanh hơn vết cạn khoảng 122.000 lần.” (0.96): lệch âm/thanh thuần Việt: vét/véc — NOT_VERIFIED bằng tai người',
    'Hệ quản lý mã nguồn phát hiện trước rồi chuyển từng kho, và tới 2030 SHA-1 bị rút hẳn sau 8 năm chuẩn bị.':
        'ASR chép “Hệ quản lý mã nguồn phát hiện trước trồi chuyển từng kho và tới 2030 SHA một bị trúc hẳn sau 8 năm chuẩn bị.” (0.933): lệch âm/thanh thuần Việt: rồi/trồi, rút/trúc — NOT_VERIFIED bằng tai người',
    # ── Đợt C hành trình: CS115 ──
    'Bước hai, phạt L2 trừ đi eta nhân lam-đa phẩy nhân w, bằng 0 phẩy 001.':
        'ASR chép “Bước 2, Phạt L2 trừ DA ta nhân Lam đa phải nhân về kép, bằng 0.001.” (0.811): “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; lệch âm/thanh thuần Việt: đi ê/da, không (trong “không phẩy” → “”) — NOT_VERIFIED bằng tai người',
    'Khi đã chạy lâu, s lặp lại theo chu kỳ, máy tính ra các giá trị đã làm tròn.':
        'ASR chép “Khi đã chạy lâu, ép lập lại theo chu kỳ, máy tính ra các giá trị đã làm tròn.” (0.895): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: lặp (trong “s lặp” → “ép lập”) — NOT_VERIFIED bằng tai người',
    'Bước một có gradient 3, s lên khoảng 8 phẩy 21, nên bước bị chia gần 3 lần, chỉ còn 1 phẩy 05 về phía âm 1.':
        'ASR chép “Bước 1 có gradient 3, ép lên khoảng 8,21, nền bước bị chia gần 3 lần, chỉ còn 1,05 về phía âm 1.” (0.935): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: nên/nền — NOT_VERIFIED bằng tai người',
    'Cách xử lý của bài báo là một biến thể nhớ giá trị lớn nhất của s từng gặp.':
        'ASR chép “Cách xử lý của bài báo là một biến thể nhớ giá trị lớn nhất của Ad từng gặp.” (0.947): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Ngày 8 tháng 8 năm 2019, bản 1 chấm 2 của một thư viện học sâu phổ biến thêm sẵn bộ tối ưu Adam tách rời.':
        'ASR chép “Ngày 8 tháng 8 năm 2019, bản 1.2 của một thư viện học sâu phổ biến thêm sẵn bộ tối UADAM tắt trời.” (0.867): lệch âm/thanh thuần Việt: chấm/∅, ưu adam tách rời/uadam tắt trời — NOT_VERIFIED bằng tai người',
    # ── Đợt C hành trình: RBM ──
    'Thứ hai là làm tròn trên máy có độ dài từ ngắn, làm P mất đối xứng, thậm chí thành âm.':
        'ASR chép “Thứ hai là làm tròn trên máy có độ dài từ ngắn, làm tê mất đối xứng, thậm chí thành âm.” (0.952): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Bước một, phép đo đến sau 1 giờ, P thành 1 phẩy 5, nên K bằng 1 phẩy 5 chia 2 phẩy 5, tức 0 phẩy 6.':
        'ASR chép “Bước 1, phép đo đến sau 1 giờ, tê thành 1,5, nền ca bằng 1,5 chia 2,5, tức 0,6.” (0.926): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: nên/nền — NOT_VERIFIED bằng tai người',
    'Bước một, với số của bài 12, P bằng 1 nên s bằng 1.':
        'ASR chép “Bước 1, với số của bài 12, t bằng 1 nên x bằng 1.” (0.933): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Phân tích U D viết P bằng U nhân D nhân U chuyển vị.':
        'ASR chép “Phân tích UD viết T bằng u nhân dây nhân u chuyển vị.” (0.857): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Bước một, với ma trận dự đoán 2, 1, 1, 1 của bài 13, ta chọn U có ô trên phải bằng 1, và D là ma trận đơn vị, chỉ cần lưu 3 con số.':
        'ASR chép “Bước 1, với ma trận dự đoán 2, 1, 1, 1 của bài 13, ta chọn UCO trên phải bằng 1 và dê là ma trận đơn vị, chỉ cần lưu 3 con số.” (0.944): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; “ô” (ô lưới) ASR viết chữ “O”; lệch âm/thanh thuần Việt: có (trong “u có ô” → “uco”) — NOT_VERIFIED bằng tai người',
    'Độ chính xác kép chữa được lỗi làm tròn, nhưng P co về 0 vì mô hình sai thì vẫn còn, như K khoảng 0 phẩy 0099 ở chặng hai.':
        'ASR chép “Độ chính xác kép chữa được lỗi làm tròn, nhưng T có về không vì mô hình sai thì vẫn còn, như ca khoảng 0.0099 ở chẳng 2.” (0.889): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; lệch âm/thanh thuần Việt: co (trong “p co” → “t có”), chặng/chẳng — NOT_VERIFIED bằng tai người',
    'Nếu độ lệch chuẩn nhỏ nhất là 0 phẩy 002 mét, tỉ số thành 10 mũ 8, vượt 2 mũ 24, khi đó nên chọn U D như máy bay năm 1972.':
        'ASR chép “Nếu độ lệch chuẩn nhỏ nhất là 0,002 mét, tỷ số thành 10 mũ 8, vượt 2 mũ 24, khi đó nên chọn UV như máy bay năm 1972.” (0.909): “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; “tỉ” ASR viết chính tả “tỷ” (cùng âm); chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: không (trong “không phẩy” → “”) — NOT_VERIFIED bằng tai người',
    'Như hai tác giả ghi, P quá lạc quan thì phép đo bên ngoài bị coi nhẹ.':
        'ASR chép “Như hai tác giả ghi, tệ quá lạc quan thì phép đo bên ngoài bị coi nhẹ” (0.941): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    # ── Đợt C hành trình: ROB ──
    'Ở bài 6, bản đồ lưới cho mỗi ô một niềm tin có vật cản hay không.':
        'ASR chép “Ở bài 6, bản đồ lưới cho mỗi ôm một niềm tin có vật cản hay không?” (0.941): “ô” (ô lưới) ASR viết chữ “O” — NOT_VERIFIED bằng tai người',
    'Thứ nhất, báo tỉ lệ kèm khoảng tin cậy.':
        'ASR chép “Thứ nhất, báo tỷ lệ kèm khoảng tiên cậy.” (0.778): “tỉ” ASR viết chính tả “tỷ” (cùng âm); lệch âm/thanh thuần Việt: tin/tiên — NOT_VERIFIED bằng tai người',
    # ── Đợt C hành trình: ESY ──
    'Ở bài 14, ta luôn giữ một đường lui, hai phân vùng 400 cộng bộ nạp 32 là 832 ki-lô-byte.':
        'ASR chép “Ở bài 14, ta luôn giữ một đường lui 2 phân vùng 400 cộng bộ nạp 32 là 832 kilobyte.” (0.931): KB đọc “ki-lô-byte” theo lexicon của khoá, ASR viết “kilobyte/kg” — NOT_VERIFIED bằng tai người',
    'Từ 2014, nhiệm vụ 3 tháng đã thành hơn 10 năm và flash mòn.':
        'ASR chép “Từ 2014, nhiệm vụ 3 tháng đã thành hơn 10 năm và for last month.” (0.872): “flash” đọc thô (foreign_ok, probe p2 6/8 — PARTIAL), ASR chép theo âm “for last/phơ lát/folas”; mòn lệch âm — NOT_VERIFIED bằng tai người',
    'Tác vụ khí tượng còn giữ khoá 2 mi li giây.':
        'ASR chép “Tắt vụ khí tượng còn giữ khóa 2 mili giây.” (0.762): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; lệch âm/thanh thuần Việt: tác/tắt — NOT_VERIFIED bằng tai người',
    'Phần mềm bay dùng hệ điều hành thương mại cùng thư viện tệp đi kèm, với bộ nhớ flash 224 mê-ga-byte.':
        'ASR chép “Phần mềm bay dùng hệ điều hành thương mại cùng thư viện tạp đi kèm với bộ nhớ Flash 224 Megabyte.” (0.885): MB đọc “mê-ga-byte” theo lexicon của khoá, ASR viết “MB/megabyte”; lệch âm/thanh thuần Việt: tệp/tạp — NOT_VERIFIED bằng tai người',
    'Bước ba, cấu hình cho phép vùng nhớ riêng xin thêm từng 256 ki-lô-byte mà không giới hạn, lấy bộ nhớ trống khoảng 4096 ki-lô-byte thì chừng 16 lần xin là cạn.':
        'ASR chép “Bước 3, cấu hình cho phép vùng nhớ riêng sinh thêm từng 256 kilobyte mà không giới hạn, lấy bộ nhớ trống khoảng 4.096 kilobyte thì chừng 16 lần sinh là cạn.” (0.867): KB đọc “ki-lô-byte” theo lexicon của khoá, ASR viết “kilobyte/kg”; lệch âm/thanh thuần Việt: xin/sinh, xin/sinh — NOT_VERIFIED bằng tai người',
    'Khởi động lại thì lại gắn ổ flash, lại cạn bộ nhớ, và mỗi lần đặt lại được hoãn 15, 15, rồi 60 phút để mặt đất kịp can thiệp.':
        'ASR chép “Khởi động lại thì lại gắn ổ phơ lát, lại cạn bộ nhớ và mỗi lần đặt lại được khoảng 15, 15, rồi 60 phút để mặt đất kịp can thiệp.” (0.925): lệch âm/thanh thuần Việt: hoãn/khoảng; “flash” đọc thô (foreign_ok, probe p2 6/8 — PARTIAL), ASR chép theo âm “for last/phơ lát/folas” — NOT_VERIFIED bằng tai người',
    'Ở chặng ba, đội điều tra gửi lệnh chế độ hạn chế, phần cứng bật vài bit trong một thanh ghi để phần mềm không dùng flash.':
        'ASR chép “Ở chặn 3, đội điều tra gửi lệnh chế độ hạn chế, phần cứng bật vài biết trong một thanh ghi để phần mềm không dùng pha last.” (0.873): lệch âm/thanh thuần Việt: chặng/chặn, bit/biết; “flash” đọc thô (foreign_ok, probe p2 6/8 — PARTIAL), ASR chép theo âm “for last/phơ lát/folas” — NOT_VERIFIED bằng tai người',
    'Khi bộ nhớ trống còn 800 ki-lô-byte trở xuống, xe dừng mọi hoạt động.':
        'ASR chép “Khi bộ nhớ trống còn 800kg trở xuống, xe dừng mọi hoạt động.” (0.875): KB đọc “ki-lô-byte” theo lexicon của khoá, ASR viết “kilobyte/kg” — NOT_VERIFIED bằng tai người',
    'Bước một, ngưỡng 800 ki-lô-byte chia 256 được 3 phẩy 125, tức còn đủ 3 lần xin thêm trước khi cạn, nên dừng kịp.':
        'ASR chép “Bước 1, ngưỡng 800 kilobyte chi 256 được 3,125, tức còn đủ 3 lần xin thêm trước khi cạn nên dừng kịp.” (0.882): KB đọc “ki-lô-byte” theo lexicon của khoá, ASR viết “kilobyte/kg”; “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; lệch âm/thanh thuần Việt: chia (trong “ki lô byte chia” → “kilobyte chi”) — NOT_VERIFIED bằng tai người',
    'Họ định dạng lại flash để tìm ô hỏng và đánh dấu tránh, ít rủi ro vì phần mềm bay nằm ở một bộ nhớ lưu lâu khác.':
        'ASR chép “Họ định dạng lại phơ lách để tìm ô hỏng và đánh dấu tránh, ít trủi ro vì phần mềm bay nằm ở một bộ nhớ lưu lâu khác.” (0.912): lệch âm/thanh thuần Việt: rủi/trủi; “flash” đọc thô (foreign_ok, probe p2 6/8 — PARTIAL), ASR chép theo âm “for last/phơ lát/folas” — NOT_VERIFIED bằng tai người',
    'Trong lúc chờ, xe chạy không dùng flash, dữ liệu giữ ở bộ nhớ tạm và phải gửi về trước khi ngủ.':
        'ASR chép “Trong lúc chờ, xe chạy không dùng phó lát, dữ liệu giữ ở bộ nhớ tạm và phải gửi về trước khi ngủ.” (0.933): “flash” đọc thô (foreign_ok, probe p2 6/8 — PARTIAL), ASR chép theo âm “for last/phơ lát/folas” — NOT_VERIFIED bằng tai người',
    'Họ sửa phần mềm để tránh hẳn dãy thứ 7 trong 7 dãy flash, và từ ngày 20 tháng 3 năm 2015 xe dùng lại 6 dãy kia.':
        'ASR chép “Họ sửa phần mềm để tránh hãng dãy thứ bảy trong bảy dãy Folas và từ ngày 20 tháng 3 năm 2015 xe dùng lại 6 dãy kia.” (0.941): lệch âm/thanh thuần Việt: hẳn/hãng; “flash” đọc thô (foreign_ok, probe p2 6/8 — PARTIAL), ASR chép theo âm “for last/phơ lát/folas” — NOT_VERIFIED bằng tai người',
    'Nhân ngược, 16 nhân 256 là 4096 ki-lô-byte.':
        'ASR chép “Nhân ngược, 16 nhân 256 là 4.096 kilobytes.” (0.9): KB đọc “ki-lô-byte” theo lexicon của khoá, ASR viết “kilobyte/kg” — NOT_VERIFIED bằng tai người',
    'Câu một, thư viện ghi thẻ nhớ mua về làm bộ nhớ trống giảm 20 ki-lô-byte mỗi ngày, hiện còn 600.':
        'ASR chép “Câu một, Thứ viện ghi thể nhớ mua về làm bộ nhớ trống giảm 20 kilobytes mỗi ngày, hiện còn 600.” (0.833): KB đọc “ki-lô-byte” theo lexicon của khoá, ASR viết “kilobyte/kg”; lệch âm/thanh thuần Việt: thư/thứ, thẻ/thể — NOT_VERIFIED bằng tai người',
    'Bạn khởi động lại mỗi đêm, giới hạn cỡ cố định cho thư viện, hay giám sát ngưỡng 100 ki-lô-byte?':
        'ASR chép “Bạn khởi động lại mỗi đêm, giới hạn cỡ cố định cho thư viện, hay giám sát ngưỡng 100 kilobytes.” (0.909): KB đọc “ki-lô-byte” theo lexicon của khoá, ASR viết “kilobyte/kg” — NOT_VERIFIED bằng tai người',
    'Đáp án câu một bắt đầu bằng phép tính, 600 trừ 100 chia 20 là 25 ngày thì chạm ngưỡng, còn 90 ngày cần 1800 ki-lô-byte.':
        'ASR chép “Đáp án câu 1 bắt đầu bằng phép tính 600 trừ 120 là 25 ngày thì chạm ngưỡng, còn 90 ngày cần 1.800 kilobyte.” (0.93): KB đọc “ki-lô-byte” theo lexicon của khoá, ASR viết “kilobyte/kg”; lệch âm/thanh thuần Việt: chia/∅ — NOT_VERIFIED bằng tai người',
    # ── Khoá mới: SEP ──
    'Bốn nguyên tắc dùng ngay trong bài này.':
        'ASR chép “Bốn nguyên tác dụng ngay trong bài này.” (0.75): lệch âm/thanh thuần Việt: tắc dùng/tác dụng — NOT_VERIFIED bằng tai người',
    'Nguyên tắc 1 chấm 2 ghi rằng báo rủi ro tuỳ tiện hay sai lệch tự nó có thể gây hại.':
        'ASR chép “Nguyên tắc 1.2 ghi rằng báo đuổi do tuy tiện hay sai lệch từ nó có thể gây hại.” (0.78): lệch âm/thanh thuần Việt: chấm/∅, rủi ro tuỳ/đuổi do tuy, tự/từ — NOT_VERIFIED bằng tai người',
    'Chỉ giữ năm sinh, c còn 160, và khả năng gần như bằng 0.':
        'ASR chép “Chỉ giữ 5 sinh sẽ còn 160 và khả năng gần như bằng không.” (0.941): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Hãy ghi rõ mục đích, cấm gộp với dữ liệu khác và hẹn ngày xoá.':
        'ASR chép “Hãy di trỏ mục đích, cấm gục với dữ liệu khác và hẹn ngay xóa.” (0.733): lệch âm/thanh thuần Việt: ghi rõ/di trỏ, gộp/gục, ngày/ngay — NOT_VERIFIED bằng tai người',
    'Bài dùng bốn từ.':
        'ASR chép “Bài dùng bốn tư.” (0.75): lệch âm/thanh thuần Việt: từ/bốn — NOT_VERIFIED bằng tai người',
    'Bài dùng bốn từ.':
        'ASR chép “Bài dùng bốn tư.” (0.75): lệch âm/thanh thuần Việt: từ/bốn — NOT_VERIFIED bằng tai người',
    'Hai thư viện tiện ích là dễ dãi, chỉ cần kèm hai bản thông báo.':
        'ASR chép “Hai thư viện tiền íp là dễ dãi, chỉ cần kèm hai bản thông báo.” (0.867): lệch âm/thanh thuần Việt: ích/tiền íp, tiện (trong “tiện x” → “tiền íp”) — NOT_VERIFIED bằng tai người',
    'Ở đây n nhân p bằng 1, nên kết quả là 1 trừ 1 chia e, xấp xỉ 0 phẩy 632.':
        'ASR chép “Ở đây n n nhân P bằng 1, nên kết quả là 1 trừ 1 GE, sắp xỉ 0,632.” (0.833): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; lệch âm/thanh thuần Việt: chia xấp (trong “chia e xấp” → “ge sắp”), không (trong “không phẩy” → “”) — NOT_VERIFIED bằng tai người',
    'Nhưng thứ tự đúng là theo p nhân D, lỗi A 1000 đô la, lỗi B chỉ 100 đô la.':
        'ASR chép “Nhưng thứ tự đúng là theo P nhân V, lỗi A 1000 đô la, lỗi B chỉ 100 đô la.” (0.955): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Cuối cùng, c là số ki lô gam khí thải quy đổi cho mỗi số điện của lưới điện.':
        'ASR chép “Cuối cùng, sẽ là số kilogram khí thải quy đổi cho mỗi số điện của lưới điện.” (0.833): chữ c đứng riêng đọc “xê”, ASR chép “sẽ”; “ki lô gam” ASR viết gộp “kilogram” — đúng đơn vị — NOT_VERIFIED bằng tai người',
    'Nếu thêm cột người ở khu phố, chịu xe đỗ và tiếng ồn, X bị thêm âm 1.':
        'ASR chép “Nếu thêm cột người ở khu phố, chịu xe đổ và tí ngôn, ít bị thêm âm mục.” (0.778): lệch âm/thanh thuần Việt: đỗ/đổ, tiếng ồn/tí ngôn, một/mục — NOT_VERIFIED bằng tai người',
    'Tổng mới của X còn 3, bằng Y và Z, và nó còn thêm một bên bị thiệt.':
        'ASR chép “Tổng mới của ít còn ba bằng y và jack và nó còn thêm một bên bị thiệt.” (0.944): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Hãy ghi lại để các bên đọc và phản hồi, ví dụ chọn Z vì X làm tài xế thiệt nặng, còn Y và Z hoà tổng nhưng Z có lợi hơn cho tài xế.':
        'ASR chép “Hãy ghi lại để các bên đọc và phản hồi, ví dụ chọn Jack vì ít làm tài xế thiệt nặng, còn Y và Jack hòa tổng nhưng Jack có lợi hơn cho tài xế.” (0.914): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'D có tổng 5, nhỏ nhất là 0, lớn nhất trong các phương án còn lại.':
        'ASR chép “Vê có tổng năm, nhỏ nhất là không, lớn nhất trong các phương án còn lại.” (0.938): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'E là ước lượng ba điểm gộp cả ba con số.':
        'ASR chép “là ước lượng 3 điểm gục cả 3 con số.” (0.857): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: gộp/gục — NOT_VERIFIED bằng tai người',
    # ── Khoá mới: CAS ──
    'Phần lẻ còn lại là 0 phẩy 2, giống hệt sau lần nhân đầu, nên dãy 0011 lặp mãi, không bao giờ dừng.':
        'ASR chép “Phần lẻ còn lại là 0.2, giống hợp 6 lần nhân đầu, nền dạy 0011 lập mãi, không bao giờ dừng.” (0.766): “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; lệch âm/thanh thuần Việt: hệt sau/hợp sáu, nên dãy/nền dạy, lặp/lập — NOT_VERIFIED bằng tai người',
    'Bảng còn một cột thứ hai, độ lệch của cổng cự ly tính bằng mét.':
        'ASR chép “Bản còn một cục thứ hai, độ lệch của cổng cử ly tín bằng mét.” (0.733): lệch âm/thanh thuần Việt: bảng/bản, cột/cục, cự/cử, tính/tín — NOT_VERIFIED bằng tai người',
    'Nhờ vết ghi để sẵn, đội tìm ra lỗi, và kế thừa ưu tiên đưa thời gian chờ về r.':
        'ASR chép “Nhờ vết ghi để sẵn, đổi tìm ra lỗi và kế thừa ưu tiên đưa thời gian chờ về error.” (0.85): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: vết/véc, đội/đổi — NOT_VERIFIED bằng tai người',
    'Nên chia ô, đúng hướng Amazon đã ghi, và chỉ giữ một khối khi hệ còn nhỏ, việc khởi động lại toàn bộ đã được tập thường xuyên.':
        'ASR chép “Nên Chiô, đúng hướng Amarron đã ghi và chỉ giữ một khối khi hệ còn nhỏ việc khởi động lại toàn bộ đã được tập thường xuyên.” (0.909): “ô” (ô lưới) ASR viết chữ “O”; lệch âm/thanh thuần Việt: chia (trong “chia ô” → “chiô”); “Amazon” đọc thô (probe CLC p1 8/8, đối chứng 5/8 — PARTIAL), ASR chép “Amarron” — NOT_VERIFIED bằng tai người',
    'Lệnh bị dừng chỉ sau một hai giây, nhưng khoảng 300 ghi-ga-byte dữ liệu đã bị xoá.':
        'ASR chép “Lệnh bị dừng chỉ sau 1-2 giây, nhưng khoảng 300 GB dữ liệu đã bị xóa.” (0.895): GB đọc “ghi-ga-byte” theo lexicon của khoá, ASR viết “GB/gigabyte” — NOT_VERIFIED bằng tai người',
    'Về băng thông, một byte là 8 bit, nên số triệu bit mỗi giây chia 8 ra số mê-ga-byte mỗi giây.':
        'ASR chép “Về băng thông, một byte là 8 bit, nên số triệu bit mỗi giây chia 8 ra số megabyte mỗi giây.” (0.909): MB đọc “mê-ga-byte” theo lexicon của khoá, ASR viết “MB/megabyte” — NOT_VERIFIED bằng tai người',
    'Vậy 60 triệu bit mỗi giây là 7 phẩy 5 mê-ga-byte mỗi giây, tức 27 nghìn mê-ga-byte mỗi giờ.':
        'ASR chép “Vậy 60 triệu bit mỗi giây là 7,5 megabyte mỗi giây, tức 27.000 megabyte mỗi giờ.” (0.833): MB đọc “mê-ga-byte” theo lexicon của khoá, ASR viết “MB/megabyte” — NOT_VERIFIED bằng tai người',
    'Nhân 7 phẩy 5 mê-ga-byte mỗi giây với 18 giờ, ta ước lượng đã chép khoảng 486 ghi-ga-byte, một con số của riêng bài này.':
        'ASR chép “Nhân 7,5 MB mỗi giây với 18 giờ, ta ước lượng đã chép khoảng 486 GB, một con số của riêng bài này.” (0.875): MB đọc “mê-ga-byte” theo lexicon của khoá, ASR viết “MB/megabyte”; GB đọc “ghi-ga-byte” theo lexicon của khoá, ASR viết “GB/gigabyte” — NOT_VERIFIED bằng tai người',
    'Tính theo giờ, 27 nghìn mê-ga-byte mỗi giờ là 27 ghi-ga-byte mỗi giờ, và 27 nhân 18 cũng ra 486.':
        'ASR chép “Tính theo giờ, 27.000 megabyte mỗi giờ là 27 gigabyte mỗi giờ, và 27 nhân 18 cũng ra 486.” (0.879): MB đọc “mê-ga-byte” theo lexicon của khoá, ASR viết “MB/megabyte”; GB đọc “ghi-ga-byte” theo lexicon của khoá, ASR viết “GB/gigabyte” — NOT_VERIFIED bằng tai người',
    'Câu một, cơ sở dữ liệu của bạn 200 ghi-ga-byte, nếu phải chép lại qua đường 60 triệu bit mỗi giây thì mất bao lâu?':
        'ASR chép “Câu một, cơ sở dữ liệu của bạn 200 GB, nếu phải chép lại qua đường 60 triệu bit mỗi giây thì mất bao lâu?” (0.929): GB đọc “ghi-ga-byte” theo lexicon của khoá, ASR viết “GB/gigabyte” — NOT_VERIFIED bằng tai người',
    'Bước một, 200 nghìn mê-ga-byte chia 7 phẩy 5 mê-ga-byte mỗi giây là khoảng 26 nghìn 667 giây, tức khoảng 7 phẩy 4 giờ.':
        'ASR chép “Bước 1, 200.000 MB chia 7,5 MB mỗi giây là khoảng 26.667 giây, tức khoảng 7,4 giờ.” (0.879): MB đọc “mê-ga-byte” theo lexicon của khoá, ASR viết “MB/megabyte” — NOT_VERIFIED bằng tai người',
    'Bước hai, 1 tỉ bit mỗi giây là 1000 triệu bit chia 8, bằng 125 mê-ga-byte mỗi giây, nên 200 nghìn chia 125 là 1600 giây, khoảng 26 phẩy 7 phút.':
        'ASR chép “Bước 2, 1 tỷ bit mỗi giây là 1.000 triệu bit chia 8 bằng 125 megabyte mỗi giây, nền 200.000 chia 125 là 1.600 giây, khoảng 26,7 phút.” (0.915): “tỉ” ASR viết chính tả “tỷ” (cùng âm); MB đọc “mê-ga-byte” theo lexicon của khoá, ASR viết “MB/megabyte”; lệch âm/thanh thuần Việt: nên/nền — NOT_VERIFIED bằng tai người',
    'Bản tin viết rằng thiếu một phép kiểm biên khi xử lý phần mở rộng nhịp tim có thể để lộ tới 64 nghìn byte bộ nhớ cho máy bên kia.':
        'ASR chép “Bản tin viết rằng thiếu mục phép kiểm biên khi xử lý phần mở rộng nhịp tim có thể để lộ tới 64.000 bai bộ nhớ cho máy bên kia.” (0.939): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: một/mục — NOT_VERIFIED bằng tai người',
    'Vùng 20 byte mà đọc 30 byte thì 10 byte cuối không thuộc vùng đó.':
        'ASR chép “Vùng 20 bay mà đọc 30 bay thì 10 bay cuối không thuộc vùng đó.” (0.824): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Độ dài khai báo là trường 2 byte trong tin, do chính bên gửi tự ghi, nói rằng phần dữ liệu dài n byte.':
        'ASR chép “Độ dài khai báo là trường hai bay trong tin, do chính bên gửi tự ghi, nói rằng phần dữ liệu dài n-bay.” (0.917): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Phần đệm là các byte ngẫu nhiên ở cuối, ít nhất 16 byte, và bên nhận bỏ qua.':
        'ASR chép “Phần đệm là các bay ngẫu nhiên ở cuối, ít nhất 16 bay và bên nhận bỏ qua.” (0.895): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Còn độ dài thật L của bản ghi là số byte thật sự đã nhận, do lớp bên dưới đếm, bên gửi không sửa được.':
        'ASR chép “Còn độ dài thật L của bản ghi là số bay thật sự đã nhận, do lớp bên dưới đến, bên gửi không sửa được.” (0.92): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: đếm/đến — NOT_VERIFIED bằng tai người',
    'Trong đó có 1 byte loại, 2 byte độ dài, 1 byte dữ liệu, và 16 byte đệm, cộng lại đúng 20.':
        'ASR chép “Trong đó có một bay loại, hai bay độ dài, một bay giữ liệu và 16 bay đệm, cộng lại đúng 20.” (0.833): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Câu trả lời phải chép n byte bắt đầu từ ô dữ liệu, và n lấy từ trường độ dài do bên kia khai.':
        'ASR chép “Câu trả lời phải chép n-by bắt đầu từ ô dữ liệu và n lấy từ trường độ dài do bên kia khai.” (0.958): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Bước một, theo đặc tả, loại 1 byte, độ dài 2 byte, dữ liệu n byte và đệm p byte cộng lại bằng độ dài bản ghi L.':
        'ASR chép “Bước 1, theo đặc tả, loại 1 bai, độ dài 2 bai, dữ liệu N-bai và đệm P-bai cộng lại bằng độ dài bản G-E-L.” (0.807): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: ghi/g e — NOT_VERIFIED bằng tai người',
    'Làm thử ngay với bản ghi 20 byte, n bằng 1 cho 1 cộng 2 cộng 1 cộng 16 bằng 20, không vượt 20, nên nhận, còn n bằng 2 cho 21, vượt 20, nên bỏ.':
        'ASR chép “Làm thử ngay với bản ghi 20 by, n bằng 1 trong 1 cộng 2 cộng 1 cộng 16 bằng 20, không vượt 20, nên nhận còn n bằng 2 cho 21, vượt 20 nên bỏ.” (0.953): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: cho/trong — NOT_VERIFIED bằng tai người',
    'Bước một, trường độ dài có 2 byte, tức 16 bit, nên khai báo lớn nhất là 2 mũ 16 trừ 1, bằng 65 nghìn 535 byte, khớp chữ tới 64 nghìn byte của bản tin.':
        'ASR chép “Bước 1, trường độ dài có 2 bai, tức 16 bit, nên khai báo lớn nhất là 2 mũ 16,1 bằng 65.535 bai, khớp giữ tới 64.000 bai của bản tin.” (0.891): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: trừ/phẩy, chữ/giữ — NOT_VERIFIED bằng tai người',
    'Bước hai, kiểm với bản ghi 20 byte, 1 cộng 2 cộng 65 nghìn 535 cộng 16 là 65 nghìn 554, vượt xa 20, nên phải bỏ.':
        'ASR chép “Bước 2, kiểm với bản ghi 23, 1 cộng 2 cộng 65.535 cộng 16 là 65.554, vượt xa 20, nên phải bỏ.” (0.976): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Bước ba, nếu thiếu phép kiểm mà vẫn chép 65 nghìn 535 byte, trong khi bản ghi chỉ có 1 byte dữ liệu, thì 65 nghìn 534 byte trả về không thuộc bản ghi.':
        'ASR chép “Bước 3, nếu thiếu phép kiểm mà vẫn chép 65.535 bay, trong khi bản ghi chỉ có một bay giữ liệu, thì 65.534 bay trả về không thuộc bản ghi.” (0.935): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Bước bốn, bản ghi ngắn nhất hợp lệ, với n bằng 0, dài 1 cộng 2 cộng 16 là 19 byte, và bản vá kiểm điều này trước cả khi đọc trường độ dài.':
        'ASR chép “Bước 4, bản ghi ngắn nhất hợp lệ, với n bằng 0, dài 1 cọng 2 cọng 16 là 19 by và bản vác kiểm điều này trước cả khi đọc trường độ dài.” (0.889): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: cộng/cọng, cộng/cọng, vá/vác — NOT_VERIFIED bằng tai người',
    'Bước năm, đặc tả giới hạn cả tin không vượt 2 mũ 14, tức 16 nghìn 384 byte, trừ 19 thì n hợp lệ lớn nhất là 16 nghìn 365.':
        'ASR chép “Bước năm, đặc tả giới hạn cá tin không vượt 2 mũ 14, tức 16,384 bài, trừ 19 thì n hợp lệ lớn nhất là 16,365.” (0.952): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: cả/cá — NOT_VERIFIED bằng tai người',
    'Trang thông tin về lỗi ghi rõ, giới hạn 64 nghìn byte chỉ là cho một lần, lặp lại thì lộ thêm.':
        'ASR chép “Trang thông tin về lỗi ghi rõ, giới hạn 64.000 bay chỉ lại cho một lần, lặp lại thì lộ thêm.” (0.917): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: là/lại — NOT_VERIFIED bằng tai người',
    'Trường 2 byte có 65 nghìn 536 giá trị, từ 0 tới 65 nghìn 535.':
        'ASR chép “Trường Hai Bài có 65.536 giá trị từ không tới 65.535.” (0.963): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Với bản ghi 20 byte, chỉ n bằng 0 và n bằng 1 được nhận, còn 65 nghìn 534 giá trị bị bỏ.':
        'ASR chép “Với bảng ghi 23, chỉ n bằng 0 và n bằng 1 được nhận, còn 65.534 giá trị bị bỏ.” (0.933): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: bản/bảng — NOT_VERIFIED bằng tai người',
    'Bài học sai thứ ba là nghĩ chỉ 64 nghìn byte nên thiệt hại nhỏ, trong khi đó chỉ là cho một lần, và có thể lặp lại nhiều lần.':
        'ASR chép “Bài học sai thứ 3 là nghĩ chỉ 64 nghìn bay nên thiệt hại nhỏ, trong khi đó chỉ là cho một lần và có thể lặp lại nhiều lần.” (0.969): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Câu một, bạn viết phần đọc một định dạng tin riêng, gồm 2 byte độ dài rồi tới dữ liệu, không có đệm.':
        'ASR chép “Câu một, bạn viết phần đọc một định dạng tinh riêng, gồm hai vai độ dài rồi tới dữ liệu, không có đệm.” (0.913): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: tin/tinh — NOT_VERIFIED bằng tai người',
    'Một tin thật dài 50 byte mà trường độ dài ghi 300, hãy viết điều kiện kiểm và cho biết nhận hay bỏ.':
        'ASR chép “Một tin thật dài 53 mà trường độ dài ghi 300. Hãy viết điều kiện kiểm và cho biết nhận hay bỏ.” (0.96): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Tổng kết lại, trường độ dài 2 byte do bên gửi ghi, phần mềm thiếu bước đối chiếu với độ dài thật, nên câu trả lời chép vượt biên và lộ bộ nhớ kề.':
        'ASR chép “Tổng kết lại, trường độ dài hai bay do bên gửi ghi, phần mềm thiếu bước đối chiếu với độ dài thật, nên câu trả lời chép vượt biên và lộ bộ nhớ kê.” (0.941): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: kề/kê — NOT_VERIFIED bằng tai người',
    'Một hệ tệp phổ biến với nút chỉ mục 128 byte lưu dấu thời gian 32 bit có dấu, và tệp trên đĩa giữ định dạng cũ.':
        'ASR chép “Một hệ tệp phổ biến với nút chỉ một 128 by lưu dấu thời gian 32 bits có giấu và tệp trên đĩa giữ định dạng cũ.” (0.909): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: mục/một, bit/bits — NOT_VERIFIED bằng tai người',
    # ── Khoá mới: PAR ──
    'Năm 1967, trong một bài báo ngắn, Amdahl viết rằng trong các lần chạy thật, khoảng 40 phần trăm số lệnh là việc quản lý dữ liệu.':
        'ASR chép “Năm 1967, trong một bài báo ngắn, Am đang viết rằng trong các lần chạy thật, khoảng 40% số lệnh là việc quản lý dữ liệu.” (0.971): “Amdahl” đọc “Am-đan” theo lexicon_vi.CSA.yaml (probe p1 8/8), ASR chép “am đang/amdang/âm đăng” — cùng âm — NOT_VERIFIED bằng tai người',
    'Điều thứ hai là định luật Amdahl, đã học ở khoá Hệ thống máy tính.':
        'ASR chép “Điều thứ hai là định luật am đang, đã học ở khóa hệ thống máy tính.” (0.938): “Amdahl” đọc “Am-đan” theo lexicon_vi.CSA.yaml (probe p1 8/8), ASR chép “am đang/amdang/âm đăng” — cùng âm — NOT_VERIFIED bằng tai người',
    'Bước sáu, khi có rất nhiều lõi, p chia n về gần 0, nên tăng tốc tiến tới 1 chia 0 phẩy 1, bằng 10 lần, không bao giờ hơn.':
        'ASR chép “Bước 6, khi có rất nhiều lõi, tê chia N về gần không nên tăng tốc tiến tới 1 chia 0,1 bằng 10 lần, không bao giờ hơn.” (0.967): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Nhưng theo định luật Amdahl ở bài 0, phần tuần tự như vậy chỉ cho khoảng 111 tới 201 lần.':
        'ASR chép “nhưng theo định luật am đang ở bài không, phần tuần tử như vậy chỉ cho khoảng 111 tới 200 linh một lần.” (0.926): lệch âm/thanh thuần Việt: tự/tử; “Amdahl” đọc “Am-đan” theo lexicon_vi.CSA.yaml (probe p1 8/8), ASR chép “am đang/amdang/âm đăng” — cùng âm — NOT_VERIFIED bằng tai người',
    'Tăng tốc theo Amdahl bằng 1 chia cho phần tuần tự cộng p chia n, với p đo trên một lõi, nên p bằng 0 phẩy 9 và 16 lõi cho 6 phẩy 4 lần.':
        'ASR chép “Tăng tốc theo Amdang bằng một chia cho phần tuần tự cộng P chia N với P đo trên một lõi, nền P bằng 0,9 và 16 lõi cho 6,4 lần.” (0.944): lệch âm/thanh thuần Việt: nên/nền; “Amdahl” đọc “Am-đan” theo lexicon_vi.CSA.yaml (probe p1 8/8), ASR chép “am đang/amdang/âm đăng” — cùng âm — NOT_VERIFIED bằng tai người',
    'Mở rộng mạnh là giữ nguyên bài toán và thêm lõi để xong sớm hơn, đây là câu hỏi của Amdahl.':
        'ASR chép “Mở rộng mạnh là giữ nguyên bài toán và thêm loại để xong sớm hơn. Đây là câu hỏi của Amnang.” (0.905): lệch âm/thanh thuần Việt: lõi/loại; “Amdahl” đọc “Am-đan” theo lexicon_vi.CSA.yaml (probe p1 8/8), ASR chép “am đang/amdang/âm đăng” — cùng âm — NOT_VERIFIED bằng tai người',
    'G của n là tăng tốc theo cỡ, tức máy một lõi phải mất bao nhiêu lần thời gian để làm cùng bài toán lớn đó.':
        'ASR chép “V của n là tăng tốc theo cỡ, tức mấy 1 loại phải mất bao nhiêu lần thời gian để làm cùng bài toán lớn đó.” (0.885): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: máy/mấy, lõi/loại — NOT_VERIFIED bằng tai người',
    'Đường thứ ba đổi sang cách đo của Amdahl.':
        'ASR chép “Đường thứ 3 đổi sang cách đo của Amdang” (0.889): “Amdahl” đọc “Am-đan” theo lexicon_vi.CSA.yaml (probe p1 8/8), ASR chép “am đang/amdang/âm đăng” — cùng âm — NOT_VERIFIED bằng tai người',
    'Chính bài báo năm 1988 đã tự hỏi sao lại thế được, khi lập luận của Amdahl dự đoán khác, và câu trả lời nằm ở hai cách đo phần tuần tự.':
        'ASR chép “Chính bài báo năm 1988 đã tự hỏi sao lại thế được, khi lập luận của Am đang dự đoán khác và câu trả lời nằm ở hai cách đo phần tuần tự.” (0.974): “Amdahl” đọc “Am-đan” theo lexicon_vi.CSA.yaml (probe p1 8/8), ASR chép “am đang/amdang/âm đăng” — cùng âm — NOT_VERIFIED bằng tai người',
    'Thứ nhất, ở bài 0, định luật Amdahl nói phần tuần tự giới hạn tăng tốc, 90 phần trăm song song được thì 16 lõi chỉ nhanh 6 phẩy 4 lần.':
        'ASR chép “Thứ nhất, ở bài 0, định luật am đang nói phần tuần tự giới hạn tăng tốc. 90% song song được thì 16 loại chỉ nhanh 6,4 lần.” (0.941): lệch âm/thanh thuần Việt: lõi/loại; “Amdahl” đọc “Am-đan” theo lexicon_vi.CSA.yaml (probe p1 8/8), ASR chép “am đang/amdang/âm đăng” — cùng âm — NOT_VERIFIED bằng tai người',
    'Vì vậy 0 phẩy 1 cộng 0 phẩy 2 ra 0 phẩy 3 với một đuôi số 4 rất nhỏ.':
        'ASR chép “Vì vậy, không phải 1 cộng, không phải 2 tra, không phải 3 với 1 đôi số 4 rất nhỏ.” (0.75): “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; lệch âm/thanh thuần Việt: ra/tra, đuôi/đôi — NOT_VERIFIED bằng tai người',
    'Chuẩn lập trình song song bộ nhớ chung phổ biến có sẵn cả lịch tĩnh lẫn lịch động có cỡ khúc.':
        'ASR chép “Chưởng lập trình xong xong bộ nhớ chung phộ biến có sẵn cả lịch tỉnh lẫn lịch đồng có cớ khúc.” (0.762): lệch âm/thanh thuần Việt: chuẩn/chưởng, phổ/phộ, tĩnh/tỉnh, động/đồng, cỡ/cớ — NOT_VERIFIED bằng tai người',
    'Lý do là 8 bộ đếm, mỗi bộ 8 byte, nằm sát nhau trong cùng một dòng 64 byte của bộ nhớ đệm.':
        'ASR chép “Lý do là 8 bộ đếm, mỗi bộ 8 bai nằm sát nhau trong cùng 1 dòng 64 bai của bộ nhớ đệm.” (0.92): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Ở khoá Hệ thống máy tính, phần bộ nhớ đệm, ta đã thấy bộ nhớ đệm chép dữ liệu theo từng dòng 64 byte liền nhau, không chép từng byte.':
        'ASR chép “Ở khóa hệ thống máy tính, phân bộ nhớ đệm, ta đã thấy bộ nhớ đệm chép giữ liệu theo từng dòng 64 bay liền nhau, không chép từng bay.” (0.906): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: phần/phân — NOT_VERIFIED bằng tai người',
    'Địa chỉ 130 chia 64 được 2 dư 2, nên nằm ở dòng số 2, byte thứ 2 trong dòng.':
        'ASR chép “Địa chỉ 134 được 2 dư 2, nên nằm ở dòng số 2, bài thứ 2 trong dòng.” (0.894): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: mươi chia sáu/∅ — NOT_VERIFIED bằng tai người',
    'Một dòng 64 byte chứa được 8 số loại 8 byte.':
        'ASR chép “Một dòng 64 bay chứa được 8 số loại 8 bay.” (0.846): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Hình trên là cách ghép sát, 8 bộ đếm 8 byte nằm vừa khít một dòng 64 byte, mỗi lõi chỉ ghi vào ô của mình.':
        'ASR chép “Hình trên là cách ghép sát, 8 bộ đếm 8 bay nằm vừa khuyết một dòng 64 bay, mỗi loại chỉ ghi vào ô của mình.” (0.857): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: khít/khuyết, lõi/loại — NOT_VERIFIED bằng tai người',
    'Ghép sát tốn 8 nhân 8 bằng 64 byte và kéo 8000 lần.':
        'ASR chép “Gép sát tốn 8 x 8 bằng 64 by và kéo 8.000 lần.” (0.812): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: ghép/gép, nhân/x — NOT_VERIFIED bằng tai người',
    'Đệm tốn 8 nhân 64 bằng 512 byte, gấp 8 lần bộ nhớ, nhưng chỉ kéo 8 lần.':
        'ASR chép “Đệm tốn 8 nhân 64 bằng 512 bai, gấp 8 lần bộ nhớ, nhưng chỉ kéo 8 lần.” (0.957): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Nếu đệm mỗi bộ đếm ra 32 byte, các địa chỉ 0, 32, 64 cứ thế tới 224 rơi vào dòng 0, 0, 1, 1, 2, 2, 3, 3.':
        'ASR chép “Nếu đệm mỗi bộ đếm ra 32 bai, các địa chỉ 0, 32, 64 cứ thể tới 224 rơi vào dòng 0, 0, 1, 1, 2, 2, 3, 3.” (0.949): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: thế/thể — NOT_VERIFIED bằng tai người',
    'Cuối cùng, đếm cặp luồng chung dòng, ghép sát có 8 nhân 7 chia 2, bằng 28 cặp giẫm chân nhau, còn đệm 64 byte thì không có cặp nào.':
        'ASR chép “Cuối cùng, đếm cặp luồng chung dòng, ghép sát có 8 nhân 7 chi 2, bằng 28 cặp dẫm chân nhau, còn đềm 64 bay thì không có cặp nào.” (0.912): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: chia/chi, đệm/đềm — NOT_VERIFIED bằng tai người',
    'Lỗi thứ hai, đệm nửa dòng, 32 byte vẫn để 2 luồng chung một dòng, vẫn 8000 lần kéo.':
        'ASR chép “Lỗi thứ hai, đềm nửa dòng, 32 by vẫn để hai luồng chung một dòng, vẫn 8.000 lần kéo.” (0.909): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: đệm/đềm — NOT_VERIFIED bằng tai người',
    'Bây giờ đến lượt bạn, 16 luồng, mỗi luồng tăng bộ đếm riêng 1000 lần, bộ đếm 4 byte, dòng 64 byte, đều là số minh hoạ.':
        'ASR chép “Bây giờ đến lược bạn, 16 luồng, mỗi luồng tăng bộ đếm riêng 1000 lần, bộ đếm 4 bay, dòng 64 bay đều là số minh họa.” (0.903): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: lượt/lược — NOT_VERIFIED bằng tai người',
    'Câu hai, đệm mỗi bộ đếm ra một dòng thì tốn bao nhiêu byte và kéo bao nhiêu lần?':
        'ASR chép “Câu 2. Đệm mỗi bộ đếm ra một dòng thì tốn bao nhiêu bai và kéo bao nhiêu lần?” (0.947): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Câu hai, đệm tốn 16 nhân 64, bằng 1024 byte, so với 64 byte khi ghép sát.':
        'ASR chép “Câu 2 Đệm tốn 16 nhân 64 bằng 1024 bai so với 64 bai khi ghép sát” (0.929): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Đệm cũng chỉ 16 lần kéo và đọc được giữa chừng, nhưng tốn 1024 byte, gấp 16 lần.':
        'ASR chép “Đệm cũng chỉ 16 lần kéo và đọc được giữa chân, nhưng tốn 1024 bay, gấp 16 lần.” (0.923): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: chừng/chân — NOT_VERIFIED bằng tai người',
    'Tổng kết lại, bộ nhớ đệm làm việc theo dòng 64 byte, và dòng của một địa chỉ là địa chỉ chia 64 làm tròn xuống.':
        'ASR chép “Tổng kết lại, bộ nhớ đệm làm việc theo dòng 64 bay, và dòng của một địa chỉ là địa chỉ chia 64 làm tròn xuống.” (0.967): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Lỗi thứ hai, ép vector hoá vòng có phụ thuộc, làn sau dùng giá trị cũ nên ra 1, 1, 1 thay vì 1, 2, 3.':
        'ASR chép “Lỗi thứ 2, F vét tờ hóa vòng có phụ thuộc là sau dùng giá trị cũ nên ra 1, 1, 1 thay vì 1, 2, 3.” (0.889): lệch âm/thanh thuần Việt: ép/f, tơ/tờ, làn/là — NOT_VERIFIED bằng tai người',
    'Nhưng bộ nhớ chỉ đưa được 20 tỉ byte mỗi giây, mỗi phần tử cần đọc 8 byte và ghi 4 byte, tức chỉ khoảng 1 phẩy 67 tỉ phần tử mỗi giây.':
        'ASR chép “Nhưng bộ nhớ chỉ đưa được 20 tỷ bai mỗi giây, mỗi phần tử cần đọc 8 bai và ghi 4 bai, tức chỉ khoảng 1,67 tỷ phần tử mỗi giây.” (0.861): “tỉ” ASR viết chính tả “tỷ” (cùng âm); byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Vòng B, s i bằng s i trừ 1 chia 2 cộng x i, có vector hoá trực tiếp được không?':
        'ASR chép “Vòng B, S y bằng S y trừ 1 chia 2 cộng x y, có vét tờ hóa trực tiếp được không?” (0.955): lệch âm/thanh thuần Việt: tơ/tờ — NOT_VERIFIED bằng tai người',
    'Đáp án vòng A, số làn w bằng 512 chia 64, tức 8, và 1000 chia hết cho 8 được 125, không có phần dư.':
        'ASR chép “Đáp án vòng A, số lạng V kết bằng 512 chia 64, tức 8 và 1000 chia hết cho 8 được 125, không có phần dư.” (0.944): chữ w đọc “vê kép” (luật chung), ASR viết tách chữ; lệch âm/thanh thuần Việt: làn/lạng — NOT_VERIFIED bằng tai người',
    'Ở bài sau, bài 7, ta học cách biết một chương trình bị chặn bởi phép tính hay bởi bộ nhớ, bằng mô hình mái nhà, đếm số phép tính trên mỗi byte phải đọc.':
        'ASR chép “Ở bài sau, bài 7, ta học cách biết một chương trình bị chặn bởi phép tính hay bởi bộ nhớ bằng mô hình máy nhà, đếm số phép tính trên mỗi bài phải đọc.” (0.943): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: mái/máy — NOT_VERIFIED bằng tai người',
    'Hôm nay ta trả lời ba câu hỏi, chương trình đang chạm trần nào, trần đó tính bằng gì, và nên sửa phép tính hay sửa số byte.':
        'ASR chép “Hôm nay ta trả lời ba câu hỏi, chương trình đang chạm trần nào, trần đó tính bằng gì, và nên sửa phép tính hay sửa số bay.” (0.964): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Điều thứ hai, một số thực 32 bit chiếm 4 byte, nên 3 số chiếm 12 byte.':
        'ASR chép “Điều thứ 2, một số thật 32 biết chiếm 4 bài, nên 3 số chiếm 12 bài.” (0.8): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: thực/thật, bit/biết — NOT_VERIFIED bằng tai người',
    'Băng thông là số byte bộ nhớ chuyển được mỗi giây.':
        'ASR chép “Băng thông là số bay bộ nhớ chuyển được mỗi giây.” (0.909): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Với 1 nghìn tỉ byte mỗi giây, chuyển 1 tỉ byte mất một phần nghìn giây, tức 1 mi li giây.':
        'ASR chép “Với một nghìn tỷ bay mỗi giây, chuyển một tỷ bay mất một phần nghìn giây, tức một mili giây.” (0.732): “tỉ” ASR viết chính tả “tỷ” (cùng âm); byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh — NOT_VERIFIED bằng tai người',
    'Điều thứ ba, ở bài 6, một lệnh vector 256 bit xử lý 8 số 32 bit cùng lúc, nên phép tính rẻ đi tới 8 lần, nhưng số byte cần đọc thì không đổi.':
        'ASR chép “Điều thứ 3, ở bài 6, một lệnh vector 256 biết xử lý 8 số 32-bit cùng lúc, nên phép tính rẽ đi tới 8 lần, nhưng số 3 cần độc thì không đổi.” (0.902): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: bit/biết, rẻ/rẽ, đọc/độc — NOT_VERIFIED bằng tai người',
    'Một việc 0 phẩy 1 mi li giây và một việc 12 mi li giây thì xong sau 12 mi li giây.':
        'ASR chép “Một việc không phải một mili giây và một việc 12 mili giây thì xong sau 12 mili giây.” (0.756): “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh — NOT_VERIFIED bằng tai người',
    'B là băng thông bộ nhớ chính, số byte mỗi giây, máy ví dụ có 1 nghìn tỉ.':
        'ASR chép “B là ban thông bộ nhớ chính, số bai mỗi giây, mẫy ví dụ có 1 nghìn tỉ.” (0.833): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: băng/ban, máy/mẫy — NOT_VERIFIED bằng tai người',
    'I là cường độ số học, bằng số phép tính chia số byte phải đọc và ghi.':
        'ASR chép “Y là cường độ số học, bằng số phép tính chia số bai phải đọc và ghi.” (0.941): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Chương trình làm nhiều phép trên mỗi byte thì I lớn, làm ít thì I nhỏ.':
        'ASR chép “Chương trình làm nhiều phép trên mỗi bay thị y lớn, làm ít thị y nhỏ.” (0.812): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: thì (trong “byte thì” → “bay thị”), thì/thị — NOT_VERIFIED bằng tai người',
    'Lưu ý, byte ở đây là byte đi giữa bộ nhớ chính và chip, đếm sau khi bộ nhớ đệm đã lọc bớt, đúng cách định nghĩa của nhóm ba tác giả đề xuất mô hình năm 2008.':
        'ASR chép “Lưu ý, bay ở đây là bay đi giữa bộ nhớ chính và chip, đếm sau khi bộ nhớ đềm đã lọc bớt, đúng cách định nghĩa của nhóm ba tác giả đề xuất mô hình năm 2008.” (0.93): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: đệm/đềm — NOT_VERIFIED bằng tai người',
    'Làm thử, cộng hai số 32 bit là 1 phép, đọc 8 byte và ghi 4 byte, nên I bằng 1 phần 12, khoảng 0 phẩy 083 phép mỗi byte.':
        'ASR chép “Làm thử, cộng 2 số 32 bit là 1 phép, đọc 8 bai và ghi 4 bai, nên y bằng 1 phần 12, khoảng 0,083 phép mỗi bai.” (0.882): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; lệch âm/thanh thuần Việt: không (trong “không phẩy” → “”) — NOT_VERIFIED bằng tai người',
    'Dữ liệu nằm ở bộ nhớ chính, đi qua một đường ống 1 nghìn tỉ byte mỗi giây, tới khối tính làm được 10 nghìn tỉ phép mỗi giây.':
        'ASR chép “Dữ liệu nằm ở bộ nhớ chính, đi qua một đường ống 1.000 tỷ bay mỗi giây, tới khối tính làm được 10.000 tỷ phép mỗi giây.” (0.897): “tỉ” ASR viết chính tả “tỷ” (cùng âm); byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Mỗi giây chỉ có 1 nghìn tỉ byte tới, nên mỗi byte phải được dùng cho ít nhất 10 phép thì khối tính mới bận hết.':
        'ASR chép “Mỗi giây chỉ có 1 nghìn tỷ bai tới nên mỗi bai phải được dùng cho ít nhất 10 phép thị khối tính mới bận hết.” (0.846): “tỉ” ASR viết chính tả “tỷ” (cùng âm); byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: thì/thị — NOT_VERIFIED bằng tai người',
    'Chương trình làm W phép tính, và khối tính làm F phép mỗi giây, nên nó cần ít nhất W chia F giây.':
        'ASR chép “Chương trình làm về đúc phép tính và khối tính làm ép ép mỗi giây, nên nó cần ít nhất về đúc chia ép giây.” (0.833): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: phép/ép — NOT_VERIFIED bằng tai người',
    'Làm thử với phép cộng hai vector một tỉ số, W bằng 10 mũ 9 phép, chia 10 mũ 13 được 0 phẩy 1 mi li giây.':
        'ASR chép “Làm thử với phép cộng 2 vector 1 tỷ số về đúc bằng 10 mũ 9 phép, chia 10 mũ 13 được 0,1 ms.” (0.836): “tỉ” ASR viết chính tả “tỷ” (cùng âm); chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh — NOT_VERIFIED bằng tai người',
    'Chương trình đọc ghi Q byte, và đường ống chuyển B byte mỗi giây, nên nó cần ít nhất Q chia B giây.':
        'ASR chép “Chương trình độc vi quy bay và đường ống chuyển bê bay mỗi giây, nên nó cần ít nhất quy chia bê giây.” (0.826): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: đọc ghi/độc vi — NOT_VERIFIED bằng tai người',
    'Làm thử, mỗi phần tử tốn 12 byte, nên Q bằng 12 tỉ byte, chia 1 nghìn tỉ được 12 mi li giây.':
        'ASR chép “Làm thử, mỗi phần tử tốn 12 bai, nên quý bằng 12 tỷ bai, chia 1 nghìn tỷ được 12 mg.” (0.76): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); “tỉ” ASR viết chính tả “tỷ” (cùng âm); tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh — NOT_VERIFIED bằng tai người',
    'Vì vậy thời gian lớn hơn hoặc bằng số lớn hơn trong hai số W chia F và Q chia B.':
        'ASR chép “Vì vậy, thời gian lớn hơn hoặc bằng số lớn hơn trong hai số về đúc chia F và quy chia B.” (0.93): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Chia W cho từng giới hạn và thay W chia Q bằng I, ta được hiệu năng nhỏ hơn hoặc bằng min của F và B nhân I.':
        'ASR chép “Chia v-đút cho từng giới hạn và thay v-đút chia quy bằng y, ta được hiểu năng nhỏ hơn hoặc bằng min của f và b nhân y.” (0.862): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: hiệu/hiểu — NOT_VERIFIED bằng tai người',
    'Hai giới hạn gặp nhau ở điểm gãy, F chia B bằng 10 phép mỗi byte.':
        'ASR chép “Hai giới hạn gặp nhau ở điểm gãy, F chia B bằng 10 phép mỗi bay.” (0.938): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Bước một, cộng hai vector số 32 bit, c i bằng a i cộng b i, chữ i nhỏ dưới chân là phần tử thứ i.':
        'ASR chép “Bước 1, cộng 2 vét tờ số 32 bit ce bằng ai cộng bi, chữ i nhỏ dưới chân là phần tử thứ i.” (0.912): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: tơ/tờ, i (trong “c i” → “ce”) — NOT_VERIFIED bằng tai người',
    'Mỗi phần tử làm 1 phép, đọc 8 byte và ghi 4 byte, nên cường độ bằng 1 phần 12, khoảng 0 phẩy 083 phép mỗi byte.':
        'ASR chép “Mỗi phần tử là một phép, đọc 8 bài và ghi 4 bài, nên cường độ bằng một phần 12, khoảng 0.083 phép mỗi bài.” (0.828): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; lệch âm/thanh thuần Việt: làm/là, không (trong “không phẩy” → “”) — NOT_VERIFIED bằng tai người',
    'Mỗi ô kết quả cần 4096 phép nhân và 4096 phép cộng, nên W bằng 2 nhân 4096 mũ 3, khoảng 137 tỉ phép.':
        'ASR chép “Mỗi ô kết quả cần 4.096 phép nhân và 4.096 phép cộng, nên về đúc bằng 2 nhân 4.096 mũ ba, khoảng 137 tỷ phép.” (0.946): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; “tỉ” ASR viết chính tả “tỷ” (cùng âm) — NOT_VERIFIED bằng tai người',
    'Trong trường hợp lý tưởng, mỗi số của ba ma trận chỉ đi qua đường ống một lần, nên Q bằng 3 nhân 4096 bình phương nhân 4 byte.':
        'ASR chép “Trong trường hợp lý tưởng, mỗi số của ba ma trận chỉ đi qua đường ống một lần, nền quy bằng ba nhân 4.096 bình phương nhân bốn bay.” (0.943): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: nên/nền — NOT_VERIFIED bằng tai người',
    'Chia ra, cường độ khoảng 682 phẩy 7 phép mỗi byte.':
        'ASR chép “Chia ra cường độ khoảng 682,7 phép mỗi bay.” (0.933): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Bước bốn, vì 682 phẩy 7 lớn hơn 10, B nhân I khoảng 682 phẩy 7 nghìn tỉ, vượt xa F.':
        'ASR chép “Bước 4, vì 682,7 lớn hơn 10, bề nhân y khoảng 682,7 nghìn tỷ, vượt xa ép.” (0.931): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; “tỉ” ASR viết chính tả “tỷ” (cùng âm) — NOT_VERIFIED bằng tai người',
    'Mỗi phép nhân cộng gồm 2 phép, phải đọc lại một số của A và một số của B từ bộ nhớ chính, tức 8 byte.':
        'ASR chép “Mỗi phép nhân cộng gồm 2 phép, phải đọc lại một số của A và một số của B từ bộ nhớ 9, tức 8 bài.” (0.923): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: chính/chín — NOT_VERIFIED bằng tai người',
    'Phép cộng vector một tỉ phần tử cần 0 phẩy 1 mi li giây tính và 12 mi li giây chuyển, nên xong sau 12 mi li giây.':
        'ASR chép “Phép cộng vector 1 tỷ phần tử cần 0,1 ms tính và 12 ms chuyển, nền xong sau 12 ms.” (0.704): “tỉ” ASR viết chính tả “tỷ” (cùng âm); tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; lệch âm/thanh thuần Việt: nên/nền — NOT_VERIFIED bằng tai người',
    'Máy hai chip đo trong bài báo có đỉnh 17 phẩy 6 tỉ phép mỗi giây và băng thông đo được 15 tỉ byte mỗi giây.':
        'ASR chép “Máy hai chiếp đo trong bài báo có đỉnh 17,6 tỷ phép mỗi giây và băng thông đo được 15 tỷ bay mỗi giây.” (0.857): “tỉ” ASR viết chính tả “tỷ” (cùng âm); byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: chip/chiếp — NOT_VERIFIED bằng tai người',
    'Nhân mẫu lưới của phương trình nhiệt làm 8 phép cho mỗi 24 byte, cường độ khoảng 0 phẩy 33, nên hiệu năng tối đa chỉ khoảng 5 tỉ.':
        'ASR chép “Nhân mẫu lưới của phương trình nhiệt làm tám phép cho mỗi 24 bay cường độ khoảng 0,33 nên hiệu năng tối đa chỉ khoảng 5 tỷ.” (0.939): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); “tỉ” ASR viết chính tả “tỷ” (cùng âm) — NOT_VERIFIED bằng tai người',
    'Thẻ X có đỉnh 20 nghìn tỉ phép mỗi giây và băng thông 1 nghìn tỉ byte mỗi giây.':
        'ASR chép “Thệ x có đỉnh 20.000 tỷ phép mỗi giây và băng thông 1.000 tỷ bay mỗi giây.” (0.8): “tỉ” ASR viết chính tả “tỷ” (cùng âm); byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: thẻ/thệ — NOT_VERIFIED bằng tai người',
    'Cường độ nhỏ thì sửa số byte, cường độ lớn thì sửa phép tính.':
        'ASR chép “Cường độ nhỏ thì sửa số bay, cường độ lớn thì sửa phép tính.” (0.929): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Phiên bản B chỉ thêm một điều kiện, luồng chẵn làm việc này, luồng lẻ làm việc kia, và mất 2 mi li giây.':
        'ASR chép “Phiên bản B chỉ thay 1 điều kiện, luôn chẳng làm việc này, luôn lẽ làm việc kia và mất 2 milli giây.” (0.723): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; lệch âm/thanh thuần Việt: thêm/thay, luồng chẵn/luôn chẳng, luồng linh/luôn lẽ — NOT_VERIFIED bằng tai người',
    'Phiên bản C đọc ảnh theo cột thay vì theo hàng, mất tới 8 mi li giây.':
        'ASR chép “phiên bản sẽ đọc ảnh theo cục thay vì theo hàng, mất tới 8 mê lý dây.” (0.765): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; lệch âm/thanh thuần Việt: cột/cục — NOT_VERIFIED bằng tai người',
    'Điều thứ hai, ở bài 7, ta thấy nhân có cường độ thấp bị chặn bởi băng thông, nên mỗi byte đọc phí là tốc độ mất đi.':
        'ASR chép “Điều thứ 2, ở bài 7, ta thấy nhân có cường độ thấp bị chặn bởi băng thông, nên mỗi bay đọc phí là tốc độ mất đi.” (0.964): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Số thực 32 bit chiếm 4 byte, nên phần tử thứ 5 nằm ở địa chỉ 4 nhân 5 bằng 20.':
        'ASR chép “Số thực 32 biết chiếm 4 bài nên phần tử thứ 5 nằm ở địa chỉ 4 nhân 5 bằng 20.” (0.917): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: bit/biết — NOT_VERIFIED bằng tai người',
    'Bộ nhớ được chia thành các đoạn 32 byte, và địa chỉ 100 chia 32 được 3 dư 4, nên nằm ở đoạn số 3.':
        'ASR chép “Bộ nhớ được chia thành các đoạn 32 bay và địa chỉ 100 chia 32 được 3 dư 4 nên nằm ở đoạn số 3.” (0.967): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Theo hướng dẫn tối ưu chính thức của hãng, các lượt đọc của 32 luồng được gộp lại thành số giao dịch 32 byte cần để phục vụ mọi luồng.':
        'ASR chép “Theo hướng dẫn tối ưu chính thức của hãng, các lượt đọc của 32 luôn được gộp lại thành số giao dịch 32 bai cần để phục vụ mọi luôn.” (0.912): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: luồng/luôn, luồng/luôn — NOT_VERIFIED bằng tai người',
    'Vậy ta chỉ cần đếm số đoạn 32 byte khác nhau mà các địa chỉ chạm tới.':
        'ASR chép “Vậy ta chỉ cần đếm số đoạn 32 bay khác nhau mà các địa chỉ chạm tới.” (0.947): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Làm thử với đọc liền nhau, luồng 0 tới 7 nằm ở đoạn 0, luồng 8 tới 15 ở đoạn 1, và luồng 31 ở đoạn 3, tổng cộng 4 giao dịch cho 128 byte.':
        'ASR chép “Làm thử với độc liền nhau, luôn 0 tới 7 nằm ở đoạn 0, luôn 8 tới 15 ở đoạn 1 và luôn 31 ở đoạn 3, tổng cộng 4 giao dịch cho 128 vai.” (0.881): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: đọc/độc, luồng/luôn, luồng/luôn, luồng/luôn — NOT_VERIFIED bằng tai người',
    'Mỗi giao dịch chuyển 32 byte, trong khi 32 luồng chỉ cần 128 byte, nên hiệu suất đọc bằng 128 chia 32 nhân số giao dịch.':
        'ASR chép “Mỗi giao dịch chuyển 32 bay, trong khi 32 luồng chỉ cần 128 bay, nên hiệu suất độc bằng 128 chia 32 nhân số giao dịch.” (0.925): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: đọc/độc — NOT_VERIFIED bằng tai người',
    'Bước bốn là phiên bản C, đọc một cột của ảnh 32 cột, mỗi luồng cách nhau 128 byte, nên mỗi luồng một đoạn riêng, tổng 32 giao dịch, hiệu suất chỉ 12 phẩy 5 phần trăm.':
        'ASR chép “Bước 4 là phiên bản xe, độc 1 cột của ảnh 32 cột, mỗi lùng cách nhau 128 bài, nên mỗi lùng một đoạn riêng, tổng 32 giao dịch, hiệu suất chỉ 12,5%.” (0.913): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: đọc/độc, luồng/lùng, luồng/lùng — NOT_VERIFIED bằng tai người',
    'Bước năm, đọc liền nhau nhưng lệch 4 byte so với đầu đoạn, các địa chỉ vắt qua 5 đoạn, hiệu suất 80 phần trăm.':
        'ASR chép “Bước năm, đọc liền nhau nhân lệch 4 bài so với đầu đoạn, các địa chỉ vắt qua 5 đoạn, hiệu xuất 80%.” (0.923): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: nhưng/nhân — NOT_VERIFIED bằng tai người',
    'Thẻ minh hoạ chuyển 1 nghìn tỉ byte mỗi giây, nhưng đọc theo cột chỉ dùng 12 phẩy 5 phần trăm số byte đã chuyển.':
        'ASR chép “Thế minh hòa chuyển 1.000 tỷ bay mỗi giây, nhưng đọc theo cột chỉ dùng 12,5% số bay đã chuyển.” (0.808): “tỉ” ASR viết chính tả “tỷ” (cùng âm); byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: thẻ/thế, hoạ/hoà — NOT_VERIFIED bằng tai người',
    'Vậy chỉ còn 125 tỉ byte có ích mỗi giây, ít hơn 8 lần, khớp với 8 mi li giây so với 1 mi li giây, nếu nhân bị chặn bởi băng thông.':
        'ASR chép “Vậy chỉ còn 125 tỷ bay có ít mỗi giây, ít hơn 8 lần, khớp với 8 mili giây so với 1 mili giây nếu nhân bị chặn bởi băng thông.” (0.861): “tỉ” ASR viết chính tả “tỷ” (cùng âm); byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh — NOT_VERIFIED bằng tai người',
    'Câu một, số giao dịch mỗi lần đọc của một nhóm, câu hai, chọn cách nào, câu ba, điều kiện t nhỏ hơn 16 có làm nhóm phân kỳ không?':
        'ASR chép “Câu 1, số giao dịch mỗi lần đọc của một nhóm. Câu 2, chọn cách nào. Câu 3, điều kiện tây nhỏ hơn 16 có làm nhóm phân kỳ không?” (0.968): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Cách một, 32 luồng đọc 32 hàng khác nhau, cách nhau 1024 nhân 4 byte, nên mỗi luồng một đoạn, 32 giao dịch, hiệu suất 12 phẩy 5 phần trăm.':
        'ASR chép “Cách 1, 32 luồng đọc 32 hàng khác nhau, cách nhau 1.024 nhân 4 bài, nên mỗi luồng một đoạn, 32 giao dịch, hiểu suốt 12,5%.” (0.93): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: hiệu suất/hiểu suốt — NOT_VERIFIED bằng tai người',
    'Cách hai, 32 luồng đọc 32 cột liền nhau của cùng một hàng, cách nhau 4 byte, nên chỉ 4 giao dịch, đạt 100 phần trăm.':
        'ASR chép “Cách 2, 32 luồng đọc 32 cục liền nhau của cùng một hàng, cách nhau 4 vai, nên chỉ 4 giao dịch đạt 100%.” (0.935): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: cột/cục — NOT_VERIFIED bằng tai người',
    'Ở câu ba, điều kiện t nhỏ hơn 16 chia mỗi nhóm thành 16 luồng đúng và 16 luồng sai, nên nhóm chạy 2 lượt.':
        'ASR chép “Ở câu 3, điều kiện tế nhỏ hơn 16 chi mỗi nhóm thành 16 lùng đúng và 16 lùng sai nên nhóm chạy hai lượt.” (0.857): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: chia/chi, luồng/lùng, luồng/lùng — NOT_VERIFIED bằng tai người',
    'Nếu viết điều kiện theo số thứ tự nhóm, tức t chia 32, thì cả 32 luồng cùng đúng hoặc cùng sai, chỉ 1 lượt.':
        'ASR chép “Nếu viết điều kiện theo số thứ tự nhóm, tức tây chia 32, thì cả 32 luồng cùng đúng hoặc cùng sai, chỉ một lượt.” (0.966): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Vì vậy số lượt bằng số nhánh khác nhau trong nhóm, và số giao dịch bằng số đoạn 32 byte mà các luồng chạm tới.':
        'ASR chép “Vì vậy số lượt bằng số nhánh khác nhau trong nhóm và số giao dịch bằng số đoạn 32-by mà các luồng chạm tới.” (0.963): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Trước khi viết, hỏi hai câu, 32 luồng cạnh nhau có đi cùng nhánh không, và có đọc 128 byte liền nhau không.':
        'ASR chép “Trước khi viết, hỏi hai câu, 32 luồng cạnh nhau có đi cùng nhánh không và có đọc 128 bài liền nhau không?” (0.966): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Phiên bản không tối ưu đạt băng thông hiệu dụng 119 phẩy 9 tỉ byte mỗi giây.':
        'ASR chép “phiên bản không tối ưu đạt ban thông hiệu dụng 119,9 tỷ bai mỗi giây.” (0.85): “tỉ” ASR viết chính tả “tỷ” (cùng âm); byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: băng/ban — NOT_VERIFIED bằng tai người',
    'Ở bài 7, cường độ là phép tính chia byte, và nhân ma trận ngây thơ chỉ có 2 phép cho 8 byte, tức 0 phẩy 25.':
        'ASR chép “Ở bài 7, Cường Độ là phép tính chi bài và nhân ma trận ngây thơ chỉ có 2 phép cho 8 bài, tức 0,25.” (0.897): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: chia (trong “chia byte” → “chi bài”) — NOT_VERIFIED bằng tai người',
    'Ở bài 8, các luồng của một khối chạy trên một cụm và dùng chung bộ nhớ chia sẻ, năm 2008 mỗi cụm có 16 KB, tức 16 nghìn 384 byte.':
        'ASR chép “Ở bài 8, các luận của một khối chạy trên một cụm và dùng chung bộ nhớ chia sẻ năm 2008 mỗi cụm có 16 kilobyte, tức 16.384 bay.” (0.929): KB đọc “ki-lô-byte” theo lexicon của khoá, ASR viết “kilobyte/kg”; byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: luồng/luận — NOT_VERIFIED bằng tai người',
    'M là dung lượng bộ nhớ nhanh tính bằng byte, ví dụ 16 nghìn 384.':
        'ASR chép “M là dung lượng bộ nhớ nhanh tính bằng bay, ví dụ 16.384.” (0.95): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Trong lúc tính, bộ nhớ nhanh phải giữ 3 khối, một của A, một của B và một của C, mỗi khối b bình phương số, 4 byte mỗi số.':
        'ASR chép “Trong lúc tính, bộ nhớ nhanh phải giữ 3 khối, 1 của A, 1 của B và 1 của C, mỗi khối B bình phương số, 4 bài mỗi số.” (0.967): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Làm thử với M bằng 16 nghìn 384, khối 32 cần 12 nghìn 288 byte nên vừa, còn khối 64 cần 49 nghìn 152 byte nên không vừa.':
        'ASR chép “Làm thử với M bằng 16.384, khối 32 cần 12.288 bay nên vừa, còn khối 64 cần 49.152 bay nên không vừa.” (0.958): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Bước một, cách ngây thơ đọc 2 nhân 1024 mũ 3, tức 2 tỉ 147 triệu 483 nghìn 648 phần tử, khoảng 8 phẩy 59 tỉ byte.':
        'ASR chép “Bước 1, cách Ngày Thơ đọc 2 nhân 1.024 mũ ba, tức 2.147.483.648 phần tử, khoảng 8,59 tỷ bay.” (0.936): “tỉ” ASR viết chính tả “tỷ” (cùng âm); byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: ngây/ngày — NOT_VERIFIED bằng tai người',
    'Bước hai, chia khối 32 thì chia số đó cho 32, còn 67 triệu 108 nghìn 864 phần tử, khoảng 268 triệu byte.':
        'ASR chép “Bước 2, chia khối 32 thì chia số đó cho 32, còn 67,108,864 phần tử, khoảng 268 triệu bay.” (0.975): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Bước ba, khối 32 cần 3 nhân 32 bình phương nhân 4, bằng 12 nghìn 288 byte, vừa 16 nghìn 384.':
        'ASR chép “Bước 3. Khối 32 cần 3 nhân 32 bình phương nhân 4 bằng 12.288 bài vừa 16.384.” (0.971): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Bước bốn, khối 64 cần 49 nghìn 152 byte, không vừa.':
        'ASR chép “Bước 4, khối 64 cần 49.152 bai, không vừa.” (0.947): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Bước năm nối với bài 7, nơi cường độ số học là số phép chia số byte.':
        'ASR chép “Bước 5 nối với bài 7, nơi cường độ số học là số phép chia số bay.” (0.941): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Số phép vẫn là 2 n mũ 3, còn số byte giờ là 4 nhân 2 n mũ 3 chia b.':
        'ASR chép “Số phép vẫn là 2n mũ 3, còn số 3 giờ là 4 nhân 2n mũ 3 chi b.” (0.905): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: chia/chi — NOT_VERIFIED bằng tai người',
    'Chia ra, cường độ bằng b chia 4, với khối 32 là 8 phép mỗi byte, gấp 32 lần so với 0 phẩy 25 của cách ngây thơ.':
        'ASR chép “Chia ra, cường độ bằng B chi 4, với khối 32 là 8 phép mỗi bay, gấp 32 lần so với 0,25 của cách ngay thơ.” (0.912): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: chia/chi, ngây/ngay — NOT_VERIFIED bằng tai người',
    'Khối 64 cần 49 nghìn 152 byte, không vừa 16 nghìn 384, nên lợi ích mất, và phép thử là tính 3 nhân b bình phương nhân 4 trước.':
        'ASR chép “Khối 64 cần 49.152 bai, 0 vừa 16.384 nên lợi ít mất và phép thử là tính 3 nhân bê bình phương nhân 4 trước.” (0.976): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Kiểm thử chỉ so kết quả chứ không đo số byte, nên phải đo thời gian và so với mái nhà.':
        'ASR chép “Kiểm thử chỉ sau kết quả chứ không đo số bay nên phải đo thời gian và so với máy nhà.” (0.857): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: so/sau, mái/máy — NOT_VERIFIED bằng tai người',
    'Khối 32 cần 12 nghìn 288 byte, nên mỗi cụm chỉ giữ được một khối luồng, vì hai khối cần 24 nghìn 576.':
        'ASR chép “Khối 32 cần 12.288 bai nên mỗi cụm chỉ giữ được một khối luồng vì hai khối cần 24.576.” (0.972): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Khối 16 chỉ cần 3 nghìn 72 byte, cụm giữ được 5 khối, nên luôn có việc khác để chạy khi một khối chờ bộ nhớ.':
        'ASR chép “Khối 16 chỉ cần 3.072 bay cùng giữ được 5 khối nên luôn có việc khác để chạy khi một khối chờ bộ nhớ.” (0.9): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: cụm (trong “byte cụm” → “bay cùng”) — NOT_VERIFIED bằng tai người',
    'Thẻ mới có bộ nhớ chia sẻ 48 KB, tức 49 nghìn 152 byte mỗi cụm, một số minh hoạ.':
        'ASR chép “Thẻ mới có bộ nhớ chia sẻ 48 kilobyte tức 49.152 bay mỗi cùng, một số minh họa.” (0.893): KB đọc “ki-lô-byte” theo lexicon của khoá, ASR viết “kilobyte/kg”; byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: cụm/cùng — NOT_VERIFIED bằng tai người',
    'Câu ba, nếu đổi sang số thực 64 bit, 8 byte mỗi số, ta giữ cỡ khối hay đổi?':
        'ASR chép “Câu 3, nếu đổi sang số thực 64 biết 8 vai mỗi số, ta giữ cỡ khối hay đổi?” (0.905): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: bit/biết — NOT_VERIFIED bằng tai người',
    'Giữ khối 64 với số 8 byte cần 98 nghìn 304 byte, không vừa.':
        'ASR chép “Giữ khối 64 với số 8 bài cần 98.304 bài, không vừa.” (0.905): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Đổi sang khối 32 chỉ cần 24 nghìn 576 byte, vừa, và còn chỗ cho một khối luồng thứ hai.':
        'ASR chép “Đổi sang khối 32 chỉ cần 24.576 bài, vừa và còn chỗ cho một khối lùng thứ 2.” (0.929): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: luồng/lùng — NOT_VERIFIED bằng tai người',
    'Điều cần mang theo, ở đây nhanh hơn không phải nhờ làm ít phép hơn, mà nhờ chuyển ít byte hơn.':
        'ASR chép “Điều cần mang theo ở đây nhanh hơn không phải nhờ làm ích phép hơn, mà nhờ chuyển ích bay hơn.” (0.952): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Có n máy, mỗi máy giữ một vector gradient D byte.':
        'ASR chép “Có N máy, mỗi máy giữ một vector gradient dê bay.” (0.815): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: véc tơ/vector — NOT_VERIFIED bằng tai người',
    'Mọi máy gửi gradient vào một máy chủ, máy chủ cộng rồi gửi tổng trở lại, nên đường vào máy chủ phải chở n nhân D byte, đó là cổ chai.':
        'ASR chép “Mọi máy gửi Gradian vào một máy chủ, máy chủ cộng rồi gửi tổng trở lại, nên đường vào máy chủ phải chở N nhân dê bay, đó là cổ trai.” (0.939): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: chai/trai — NOT_VERIFIED bằng tai người',
    'Sau n trừ 1 bước, mỗi mảnh đã đi qua đủ n máy, nên mỗi máy giữ tổng đầy đủ của đúng một mảnh, và mỗi máy đã gửi n trừ 1 nhân D chia n.':
        'ASR chép “Sau N trừ một bước, mỗi mảnh đã đi qua đủ N máy nên mỗi máy giữ tổng đầy đủ của đúng một mảnh và mỗi máy đã gửi N trừ một nhân dây chia N.” (0.972): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Bước bốn, với 8 máy, máy chủ nhận 8 GB rồi gửi lại 8 GB, mất 0 phẩy 8 cộng 0 phẩy 8 bằng 1 phẩy 6 giây.':
        'ASR chép “Bước 4, với 8 máy, máy chủ nhận 8GB rồi gửi lại 8GB, mất 0,8 cộng 0,8 bằng 1,6 giây.” (1.0): GB đọc “ghi-ga-byte” theo lexicon của khoá, ASR viết “GB/gigabyte” — NOT_VERIFIED bằng tai người',
    'Lỗi thứ hai là gộp từng gói nhỏ một.':
        'ASR chép “Lỗi thứ 2 là gục từng có nhỏ 1.” (0.778): lệch âm/thanh thuần Việt: gộp/gục, gói/có — NOT_VERIFIED bằng tai người',
    'Câu một, mỗi máy có 2 GB gradient, vòng mất bao lâu nếu bỏ qua trễ, còn máy chủ tham số với một máy và với hai máy chia đôi thì sao?':
        'ASR chép “Câu 1, mỗi máy có 2GB Gradient, vòng mất bao lâu nếu bỏ qua trễ, còn máy chủ tham số với một máy và với hai máy chia đôi thì sao?” (0.943): GB đọc “ghi-ga-byte” theo lexicon của khoá, ASR viết “GB/gigabyte” — NOT_VERIFIED bằng tai người',
    'Một máy chủ nhận 32 GB rồi gửi 32 GB, mất 2 phẩy 56 giây.':
        'ASR chép “Một máy chủ nhận 32GB rồi gửi 32GB, mất 2,56 giây.” (1.0): GB đọc “ghi-ga-byte” theo lexicon của khoá, ASR viết “GB/gigabyte” — NOT_VERIFIED bằng tai người',
    'Hai máy chủ chia đôi, mỗi máy chủ 16 GB vào và 16 GB ra, mất 1 phẩy 28 giây.':
        'ASR chép “Hai máy chủ chia đôi, mỗi máy chủ 16GB vào và 16GB ra, mất 1,28 giây.” (1.0): GB đọc “ghi-ga-byte” theo lexicon của khoá, ASR viết “GB/gigabyte” — NOT_VERIFIED bằng tai người',
    'Vòng phải đi 30 bước, mỗi bước 5 mi li giây trễ, cộng 0 phẩy 15 mi li giây dữ liệu, khoảng 150 mi li giây.':
        'ASR chép “Vòng phải đi 30 bước, mỗi bước 5 mili dây trễ, cộng 0,15 mili dây dữ liệu, khoảng 150 mili dây.” (0.746): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh — NOT_VERIFIED bằng tai người',
    'Máy chủ chỉ có 2 lần trễ, 10 mi li giây, cộng 2 phẩy 56 mi li giây dữ liệu, tổng 12 phẩy 56 mi li giây.':
        'ASR chép “Máy chủ chỉ có hai lần trễ, 10 ms, cộng 2,56 ms dữ liệu, tổng 12,56 ms.” (0.793): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh — NOT_VERIFIED bằng tai người',
    'Chào bạn, một thẻ tính xong một bước huấn luyện trong 100 mi li giây.':
        'ASR chép “Chào bạn, một thể tính sau một bước huấn luyện trong 100 mê ly giây.” (0.75): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; lệch âm/thanh thuần Việt: thẻ/thể, xong/sau — NOT_VERIFIED bằng tai người',
    'Hình vẽ một bước theo đúng tỉ lệ, 100 mi li giây tính rồi tới phần gộp.':
        'ASR chép “Hình với một bước theo đúng tỷ lệ, 100 mili giây tính rồi tới phần gục.” (0.743): “tỉ” ASR viết chính tả “tỷ” (cùng âm); tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; lệch âm/thanh thuần Việt: vẽ/với, gộp/gục — NOT_VERIFIED bằng tai người',
    'Hàng trên chờ tính xong hết rồi mới gộp 30 mi li giây.':
        'ASR chép “Hàng trên chờ tính xong hết rồi mới gột 30 mê ly giây.” (0.786): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; lệch âm/thanh thuần Việt: gộp/gột — NOT_VERIFIED bằng tai người',
    'Hàng dưới gửi gradient tầng cuối ngay khi có, nên 20 mi li giây gộp chạy chồng lên lúc tính, chỉ còn 10 mi li giây lộ ra.':
        'ASR chép “Hàng dưới gửi gradient tần cuối ngay khi có, nền 20 mili dây gột chạy trồng lên lúc tính, chỉ còn 10 mili dây lộ ra.” (0.7): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; lệch âm/thanh thuần Việt: tầng/tần, nên/nền, gộp (trong “mi li giây gộp” → “mili dây gột”), chồng/trồng — NOT_VERIFIED bằng tai người',
    'Bước một, mô hình 150 triệu tham số, mỗi tham số một gradient 4 byte, nên D bằng 0 phẩy 6 GB.':
        'ASR chép “Bước 1, mô hình 150 triệu tham số, mỗi tham số 1 gradient 4 vai, nên dê bằng 0,6 gigabyte.” (0.893): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); GB đọc “ghi-ga-byte” theo lexicon của khoá, ASR viết “GB/gigabyte” — NOT_VERIFIED bằng tai người',
    'Đổi hết sang byte và giây, 1 phẩy 05 tỉ byte chia 35 tỉ byte mỗi giây bằng 0 phẩy 03 giây, đúng 30 mi li giây.':
        'ASR chép “Đổi hết sang bay và dây, 1,05 tỷ bay chia 35 tỷ bay mỗi dây bằng 0,03 dây, đúng 30 mili dây.” (0.746): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); “tỉ” ASR viết chính tả “tỷ” (cùng âm); tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh — NOT_VERIFIED bằng tai người',
    'Còn D, 150 triệu nhân 4 bằng 600 triệu byte, tức 0 phẩy 6 GB.':
        'ASR chép “Còn dê 150 triệu nhân bốn bằng 600 triệu byte, tức 0,6 gigabyte.” (0.947): GB đọc “ghi-ga-byte” theo lexicon của khoá, ASR viết “GB/gigabyte” — NOT_VERIFIED bằng tai người',
    'Câu hai, nếu mạng chỉ 10 GB mỗi giây thì E khi chồng là bao nhiêu, có nên nâng mạng?':
        'ASR chép “Câu 2, nếu mạng chỉ 10GB mỗi giây thì e khi chồng là bao nhiêu, có nên nâng mẳn?” (0.95): lệch âm/thanh thuần Việt: mạng/mẳn — NOT_VERIFIED bằng tai người',
    'Quyết định là ở 10 GB mỗi giây, nâng mạng hay gom gói đáng hơn thêm thẻ, còn ở 35 GB mỗi giây thì mạng đã đủ.':
        'ASR chép “Quyết định là ở 10GB mỗi giây, nâng mạng hay gom gói đáng hơn thêm thẻ, còn ở 35GB mỗi giây thì mạng đã đủ.” (1.0): GB đọc “ghi-ga-byte” theo lexicon của khoá, ASR viết “GB/gigabyte” — NOT_VERIFIED bằng tai người',
    'Ở bài 0, định luật Amdahl nói tăng tốc bằng 1 chia cho phần tuần tự cộng phần song song chia số lõi.':
        'ASR chép “Ở bài không, định luật âm đang nói tăng tốc bằng một chia cho phần tuần từ cộng phần xong xong chia số lõi.” (0.894): lệch âm/thanh thuần Việt: tự/từ; “Amdahl” đọc “Am-đan” theo lexicon_vi.CSA.yaml (probe p1 8/8), ASR chép “am đang/amdang/âm đăng” — cùng âm — NOT_VERIFIED bằng tai người',
    'Người đo hiệu năng dùng bốn thuật ngữ.':
        'ASR chép “Người đó hiểu năng dùng bốn thuật ngữ.” (0.75): lệch âm/thanh thuần Việt: đo hiệu/đó hiểu — NOT_VERIFIED bằng tai người',
    'Bài báo năm 1967 của Amdahl đã ghi rằng phần quản lý dữ liệu chiếm khoảng 40 phần trăm số lệnh của các chương trình sản xuất thời đó.':
        'ASR chép “Bài báo năm 1967 của Amdang đã ghi rằng phần quản lý dữ liệu chiếm khoảng 40% số lệnh của các chương trình sản xuất thời đó.” (0.972): “Amdahl” đọc “Am-đan” theo lexicon_vi.CSA.yaml (probe p1 8/8), ASR chép “am đang/amdang/âm đăng” — cùng âm — NOT_VERIFIED bằng tai người',
    'Ta tái hiện con số bằng định luật Amdahl.':
        'ASR chép “Ta tái hiện con số bằng định lược âm đăng.” (0.737): “Amdahl” đọc “Am-đan” theo lexicon_vi.CSA.yaml (probe p1 8/8), ASR chép “am đang/amdang/âm đăng” — cùng âm — NOT_VERIFIED bằng tai người',
    'Tổng kết lại, ta đo ngân sách trên một thẻ, tìm ra phần tuần tự 25 phần trăm, và định luật Amdahl tái hiện đúng con số 2 phẩy 91 cùng trần 4.':
        'ASR chép “Tổng kết lại, ta đo ngân sách trên một thẻ, tìm ra phần tuần tự 25% và định luật am đang tái hiện đúng con số 2,91 cùng trần 4.” (0.974): “Amdahl” đọc “Am-đan” theo lexicon_vi.CSA.yaml (probe p1 8/8), ASR chép “am đang/amdang/âm đăng” — cùng âm — NOT_VERIFIED bằng tai người',
    'Thực hành rút ra là chia việc thành rất nhiều khối độc lập, tránh rẽ nhánh trong nhóm 32 luồng, và chép dữ liệu dùng lại vào bộ nhớ chia sẻ 16 KB.':
        'ASR chép “Thực hành trúc ra là chia việc thành rất nhiều khối độc lập, tránh rẽ nhánh trong nhóm 32 luồng và chép dữ liệu dùng lại vào bộ nhớ chia sẻ 16 kilobytes.” (0.944): KB đọc “ki-lô-byte” theo lexicon của khoá, ASR viết “kilobyte/kg”; lệch âm/thanh thuần Việt: rút/trúc — NOT_VERIFIED bằng tai người',
    'Bạn đã đi từ phần tuần tự của Amdahl, qua công việc và đường găng, tranh chấp, bộ nhớ đệm và vector.':
        'ASR chép “Bạn đã đi từ phần tuần tự của Amdang qua công việc và đường găng, tranh chấp, bộ nhớ đệm và vét tơ.” (0.936): “Amdahl” đọc “Am-đan” theo lexicon_vi.CSA.yaml (probe p1 8/8), ASR chép “am đang/amdang/âm đăng” — cùng âm — NOT_VERIFIED bằng tai người',
    # ── CSA L03 dựng lại (2026-10-29) ──
    'Giải mã dãy bit 3 E 2 0 0 0 0 0 hệ mười sáu.':
        'đọc tách từng ký tự (E36); ASR chép “3-E-2000-0016”: đủ 3, E, 2 và năm chữ số 0, rồi “16” (hệ mười sáu) — dãy ký tự khớp (audit/asr_digits.py lệch chỉ vì công cụ đổi “sáu” thành 6 mà không ghép “mười sáu”); dải/giải, dậy/dãy là nhầm gi/d của ASR',
    'Câu một, giải mã dãy bit C 0 2 0 0 0 0 0 hệ mười sáu, gợi ý C 0 là 1 1 0 0, 0 0 0 0.':
        'ASR chép “C0200000”, “C0” đúng từng ký tự; nhóm “1 1 0 0, 0 0 0 0” chép “1100000” (thiếu một chữ số 0 khi tám chữ số liền) — cùng loại lệch của ASR với dãy “không” lặp ở L04 — NOT_VERIFIED bằng tai người',
    # ── OSY (2026-10-29): mỗi lý do dựa trên bản chép trong out/OSY/<id>/asr_report.md ──
    'Trước vòng lặp có 1 tiến trình.':
        'lặp/lập, tiến/tiếng: nhầm thanh và âm cuối của ASR ở câu 7 từ; “tiến trình” chép đúng ở các câu dài của L01; số 1 khớp — NOT_VERIFIED bằng tai người',
    'Còn luồng thì dùng chung bộ nhớ trong một tiến trình.':
        'còn/con, luồng/luôn, tiến/tiếng: nhầm thanh và âm cuối ng/n của ASR; “luồng” chép đúng ở các khung khác của L01 — NOT_VERIFIED bằng tai người',
    'Hai, tìm cặp đọc rồi ghi mà luồng khác chen vào giữa được.':
        'hai/hay (cặp đã biết, SKILL Bước 5), đọc/độc, rồi/đồ, luồng/luôn: nhầm thanh và phụ âm đầu của ASR; câu đủ nghĩa — NOT_VERIFIED bằng tai người',
    'Câu hai, thứ tự A A A B B B thì sao?':
        'chuỗi “A A A” đọc tên chữ cái liền nhau; ASR bỏ mất, còn “B B B” chép đúng “BBB”; thứ tự hiện trên màn hình — NOT_VERIFIED bằng tai người',
    'Bước ghi, chép thanh ghi về lại x.':
        'chữ “x” (đọc “ích”) ở cuối câu bị ASR bỏ; mọi từ khác khớp; x hiện trên màn hình — NOT_VERIFIED bằng tai người',
    'Semaphore đếm số vé và bắt chờ khi hết vé.':
        'Semaphore đọc “Xe-ma-pho” (lexicon_vi.OSY.yaml); ASR chép “Xe MAFO” — đủ ba âm tiết xe, ma, pho, chỉ khác cách viết — NOT_VERIFIED bằng tai người',
    'Hệ điều hành làm y hệt với tài nguyên.':
        'hệ/hãy, hệt/hợp: nhầm thanh của ASR; “hệ điều hành” chép đúng ở mọi câu khác của L07 — NOT_VERIFIED bằng tai người',
    'Vì 959 KB đó nằm rải rác thành năm mẩu, mẩu lớn nhất chỉ 300 KB.':
        'KB đọc “ki-lô-byte”; ASR chép “kg” (ki-lô + mất âm “bai”), trong khi cùng cách viết được chép “kilobyte” ở 4 câu khác của L08; rải/rại, rác/trắc, mẩu/mẫu là nhầm thanh; các số 959, 300 khớp — NOT_VERIFIED bằng tai người',
    'Mỗi tiến trình có bảng riêng, và khi chuyển ngữ cảnh thì đổi luôn thanh ghi trỏ tới bảng trang.':
        'tiến/tiếng, bảng/bản (âm cuối ng/n), luôn/lung, trỏ/trọ: nhầm thanh và âm cuối của ASR; câu đủ nghĩa — NOT_VERIFIED bằng tai người',
    'Một tiến trình dùng 8 MiB liền nhau chỉ cần thư mục 4 KiB cộng 2 bảng con, tổng 12 KiB thay vì 4 MiB.':
        'MiB đọc “mê-ga-byte”, ASR chép “MB”; KiB chép “kilobyte” — đúng đơn vị; mục/một, bảng/bản là nhầm của ASR; các số 8, 4, 2, 12 khớp',
    'Chào bạn, ở bài 8, chương trình phải nằm trong một vùng liền, nên bộ nhớ còn 959 KB trống mà không đặt nổi 426 KB.':
        'KB → “kg” như câu cùng số 959 ở L08 (mất âm “bai”); trống/trong là nhầm âm cuối; các số 8, 959, 426 khớp — NOT_VERIFIED bằng tai người',
    'Giả sử truy cập bộ nhớ mất 100 na-nô giây, còn xử lý một lỗi trang phải đọc đĩa mất 8 mi li giây, tức 8 triệu na-nô giây.':
        '“na-nô giây” → “nanoday”, “mi li giây” → “mili dây”: giây/dây là nhầm gi/d đã biết (CSA L08), na-nô, mi-li cùng âm; đĩa/để là nhầm của ASR; các số 100, 8, 8 triệu khớp',
    'Câu hai, chuyển vế bất đẳng thức, p không vượt quá 10 chia cho 8 triệu trừ 100.':
        'chữ “p” → “tê”: ASR lẫn p/t (probe audit/dms/probes/p2_chu_p.md, đối chứng 0/8); vế/với, trừ/trường là nhầm của ASR; các số khớp',
    'Ý nghĩa của nó là số khung mà tiến trình cần để chạy mà không bị lỗi trang liên tục.':
        '“Ý” đầu câu → “Yến”: ASR thêm âm cuối ở âm tiết đầu câu; mọi từ khác khớp — NOT_VERIFIED bằng tai người',
    'Với thư mục, ba bit mang nghĩa khác.':
        'ba/bà là nhầm thanh, bit/biết là nhầm âm cuối đã biết (probe p1 CSA: NOT_VERIFIED); “ba quyền r, w, x” hiện trên màn hình — NOT_VERIFIED bằng tai người',
    'Hai, nhớ các ranh giới, con trỏ trực tiếp phủ tới 48 KiB, gián tiếp đơn phủ thêm 4 MiB.':
        'KiB → “kilobytes”, MiB → “megabytes”: đúng đơn vị; các ranh/cắt tranh, trỏ/trọi, gián/dán (gi/d) là nhầm của ASR; số 48, 4 khớp — NOT_VERIFIED bằng tai người',
    'Nhân với 4096 byte mỗi khối, được khoảng 4 phẩy 004 TiB.':
        'byte → “bai/bay” (probe p1 CSA, cùng âm), TiB → “tê ra bay”: đúng đơn vị; “4 phẩy 004” ASR viết thành “4.004” (dấu chấm thập phân) — dãy chữ số 4004 khớp',
    # ── CSA (2026-10-29): mỗi lý do dựa trên bản chép trong out/CSA/<id>/asr_report.md và audit/asr_digits.py ──
    'Ba, cộng thêm 1, ta được 1 1 1 1, 1 0 1 1.':
        'dãy chữ số: audit/asr_digits.py — dãy chữ số bản chép trùng hoàn toàn kỳ vọng (3111111011); độ khớp thấp chỉ vì ASR gộp chữ số thành “1111, 1011”',
    'Câu hai, 200 vượt quá 127, dãy bit 1 1 0 0, 1 0 0 0 đọc có dấu là âm 56.':
        'dãy chữ số: audit/asr_digits.py — nhóm “1 0 0 0”: small chép “10000”, medium chép “1100” — hai mô hình lệch theo hai cách khác nhau (lỗi ASR với dãy “không” lặp); nhóm đầu và các số khác khớp — NOT_VERIFIED bằng tai người',
    'Ví dụ 12 là 1 1 0 0, 11 là 1 0 1 1, và với nhau ra 1 0 0 0 bằng 8.':
        'dãy chữ số: audit/asr_digits.py — nhóm “1 0 0 0”: small “10000”, medium “1100” — lệch không nhất quán giữa hai mô hình (lỗi ASR); 1100, 1011, 8 khớp — NOT_VERIFIED bằng tai người',
    'Đáp án câu một, hoặc với 1 dịch trái 6 ta được 1 1 1 1, 0 1 1 1.':
        'dãy chữ số: audit/asr_digits.py — dãy chữ số trùng hoàn toàn (11611110111); ASR chỉ gộp chữ số',
    'Sau đó và với phần đảo của 1 để tắt bit 0, ta được 1 1 1 1, 0 1 1 0.':
        'dãy chữ số: audit/asr_digits.py — dãy chữ số trùng hoàn toàn (1011110110); ASR chỉ gộp chữ số',
    'Dịch lô-gích luôn điền 0, nên cùng dãy bit đó ra 124.':
        '“lô-gích” → “Logit”: cùng âm, ASR viết theo chữ Anh (giống “lôgarit” → “Logatrix” ở CS112); điền/điện, bit/biết: nhầm thanh và âm cuối; số 124 khớp',
    'Lỗi thứ tư, nghĩ cổng đổi trạng thái tức thì.':
        'lỗi/lội, cổng/cộng, trạng/tràn: nhầm thanh của ASR (cổng nghe đúng ở các câu khác của L05) — NOT_VERIFIED bằng tai người',
    'Cổng không đảo đầu vào, ký hiệu dấu móc.':
        'cổng/tổng, dấu/giấu (d/gi), móc/mất: ASR lẫn phụ âm đầu và âm cuối; ký hiệu dấu móc hiện trên màn hình — NOT_VERIFIED bằng tai người',
    'Câu trả lời là vài công tắc nối với nhau theo đúng một bảng chân trị, và hôm nay ta học cổng lô-gích, đại số lô-gích và mạch cộng hai bit.':
        'tắc/tác, bảng/bản, mạch/mặt (âm cuối c/t, ng/n), “lô-gích” → “logit” (cùng âm): nhầm của ASR; câu đủ nghĩa',
    'Chào bạn, bộ cộng 4 bit tính 0 1 1 1 cộng 0 1 0 1 ra 1 1 0 0.':
        'dãy chữ số: audit/asr_digits.py — dãy chữ số trùng hoàn toàn (4011101011100); bit/biết là nhầm âm cuối (probe p1 CSA)',
    'Cờ C báo tràn không dấu, cờ V báo tràn có dấu.':
        '“cờ C”, “cờ V” → “thì xe”, “xe về”: tên chữ cái đọc kiểu Việt (C → xê, V → vê), ASR không nhận ra cụm “cờ + chữ cái”; tràn/trạng, dấu/giấu: nhầm của ASR; chữ C, V hiện trên màn hình',
    'Ví dụ 6 trừ 3, cộng 0 1 1 0 với 1 1 0 0 và nhớ 1, giữ 4 bit thấp, ra 0 0 1 1 bằng 3.':
        'dãy chữ số: audit/asr_digits.py — dãy chữ số trùng hoàn toàn (63011011001400113); bit/bịch là nhầm âm cuối',
    'Câu một, tính 0 1 0 1 cộng 0 1 0 0 trên 4 bit, cờ C và V là bao nhiêu?':
        'dãy chữ số: audit/asr_digits.py — dãy chữ số trùng hoàn toàn (1010101004); “cờ C” → “CC”: tên chữ cái',
    'Mã 1 0 chọn phép cộng, ra 9.':
        'medium chép đúng “Mả 1 không chọn phép cộng, ra 9” (đủ chữ số); small nghe 9 → “chính” (chín/chính) — lỗi ASR; mã/mả là nhầm thanh',
    'Mã 1 1 chọn phép trừ, ra 3.':
        '“1 1” → “mục một” ở cả hai mô hình: ASR lẫn “một/mục” khi hai chữ số lặp (câu ngắn); mã 11 hiện trên màn hình — NOT_VERIFIED bằng tai người',
    'Câu hai, cộng 0 0 1 0 với phần đảo của 5 là 1 0 1 0, cộng thêm nhớ 1, ra 1 1 0 1, đọc có dấu là âm 3.':
        'dãy chữ số: audit/asr_digits.py — dãy chữ số trùng hoàn toàn (2001051010111013); đảo/đạo là nhầm thanh',
    'Hôm nay ta học bộ cộng nhiều bit, phép trừ và các cờ tràn.':
        'bit/bích (probe p1 CSA: NOT_VERIFIED, ASR lẫn âm cuối t/ch), cờ/cơ, tràn/trang: nhầm thanh của ASR',
    'Chữ f là tần số xung nhịp, 2 tỉ nhịp mỗi giây nghĩa là mỗi nhịp dài nửa na-nô giây.':
        'xung/xuân, giây/dây (gi/d), tỉ/tỷ (chính tả), “na-nô” → “nano” (cùng âm): nhầm của ASR; con số khớp',
    'Hôm nay ta học định luật Amdahl, công thức cho giới hạn này, và hệ quả của nó với cách ta đầu tư vào song song.':
        'Amdahl đọc “Am-đan” (lexicon CSA, probe p1 8/8); câu này ASR chép “âm đang” — lẫn âm cuối n/ng, cùng loại nhầm đã biết; các câu khác của L13 chép “Am-đan/Amdahl”',
    'Câu hai, 0 phẩy 9 nhân 101 cộng 0 phẩy 1 nhân 201, bằng 111 na-nô giây.':
        'medium chép “100 linh 1”, “200 linh 1”, “111” (số đúng); “phẩy” → “phải”, 9 → “chiến”: nhầm thanh/âm cuối của ASR',
    "Phủ định phải đổi và thành hoặc, và dòng p đúng, q sai cho hai kết quả khác nhau, đúng là lỗi ở đầu bài.":
        P2 + "; “thành hoặc” → “thanh hoạt”: nhầm thanh, âm cuối của ASR; “hoặc” ở các câu khác cùng bài nghe đúng",
    "Định lý, tổng hai số lẻ là số chẵn.":
        "chẵn/chẳng, lẻ/lẽ: ASR lẫn thanh ngã/hỏi — lặp ở nhiều câu L03 (mục tham khảo), “lẻ” khung 9 nghe đúng; NOT_VERIFIED bằng tai người",
    "Bước một, giả sử căn 2 bằng a chia b, với phân số đã rút gọn tối giản.":
        "chia/chi, phân/phần, rút/trúc, giản/giãn: ASR lẫn âm cuối, thanh; “phân số”, “tối giản” nghe đúng ở các câu khác của L03 — NOT_VERIFIED bằng tai người",
    "Xếp các tổ hợp thành từng hàng, ta được tam giác Pascal.":
        "“Pascal” đọc thô (probe p1_ten 7/8; “Pa-xcan” cũng 7/8, không tốt hơn); ở câu này ASR chép “task an”, câu khác chép “pascan” (cùng âm) — NOT_VERIFIED bằng tai người",
    "Cả khai triển có hệ số 1, 4, 6, 4, 1, đúng hàng 4 của tam giác Pascal.":
        "“Pascal” ASR chép “pascan”: cùng âm (probe p1_ten 7/8); tam/tàm là nhầm thanh của ASR",
    "Ví dụ hai, đi trên lưới tới ô cách 3 bước sang phải và 2 bước lên trên.":
        "“ô” (ô lưới) ASR chép “ồ”: từ một âm tiết, nhầm thanh; chữ “ô” và hình lưới mô tả trên màn hình",
    "Và tỉ lệ hoán vị không điểm cố định tiến về một chia e.":
        "tỉ/tỷ là chính tả; “một chia” → “mục chi”: nhầm âm cuối của ASR; cụm “một chia e” ở khung khác chép “một GE” — chữ e đọc kiểu Việt; NOT_VERIFIED bằng tai người",
    "Ở đây e xấp xỉ 2 phẩy 718, là cơ số của lôgarit tự nhiên.":
        "“lôgarit” → “Logatrix”: nút thắt B20 đã biết (CS112), cùng âm; xấp/sắp (x/s) và chữ e đọc kiểu Việt; con số 2,718 hiện trên màn hình",
    "Hệ quả, số đỉnh có bậc lẻ luôn là số chẵn.": "bậc/bật (âm cuối c/t, cùng loại với Fermat → “phét ma” ở probe p1), chẵn/chẳng, lẻ/lẽ (thanh ngã/hỏi): nhầm của ASR lặp ở mọi bài đồ thị; NOT_VERIFIED bằng tai người",
    "Câu hai, mỗi đỉnh có bậc 4, là số chẵn.": "bậc/bật (âm cuối c/t, cùng loại với Fermat → “phét ma” ở probe p1), chẵn/chẳng, lẻ/lẽ (thanh ngã/hỏi): nhầm của ASR lặp ở mọi bài đồ thị; đỉnh/định là nhầm thanh — NOT_VERIFIED bằng tai người",
    "Lý do là tổng mọi bậc thì chẵn, mà phần các bậc chẵn đã chẵn, nên phần các bậc lẻ cũng phải có tổng chẵn.": "bậc/bật (âm cuối c/t, cùng loại với Fermat → “phét ma” ở probe p1), chẵn/chẳng, lẻ/lẽ (thanh ngã/hỏi): nhầm của ASR lặp ở mọi bài đồ thị; NOT_VERIFIED bằng tai người",
    "Đồ thị lại liên thông, nên có chu trình Euler đi qua cả 10 cạnh.": "Euler → “ở lè” (probe p1_ten 8/8, cùng âm); đồ/đô, chu/chư: nhầm thanh của ASR",
    "Lỗi thứ nhất, coi tập rỗng và tập chứa tập rỗng là một.":
        "rỗng/động (r/đ), lỗi/lội: ASR lẫn phụ âm đầu và thanh; “tập rỗng” nghe đúng ở khung sym_set của L05 — NOT_VERIFIED bằng tai người",
    'Độ dài 3 có bốn chuỗi 0 0 0, 0 1 1, 1 0 1 và 1 1 0.':
        'dãy chữ số đọc tách từng chữ; small chép “0000, 001, 1001, 1100” (gộp các chữ số kề nhau qua dấu phẩy), không có từ nào khác sai — bốn chuỗi hiện trên màn hình; NOT_VERIFIED bằng tai người',
    'Một chuỗi là dãy hữu hạn ký hiệu lấy từ bảng chữ cái, viết liền nhau, như 0 1 1 0.':
        'dãy chữ số đọc tách từng chữ; ASR gộp thành một số (“0110”) — đủ từng chữ số theo đúng thứ tự, lệch chỉ vì cách viết liền; dãy hiện trên màn hình; dãy/giải (d/gi), bảng/bản là nhầm của ASR',
    'Câu hai, chạy trên chuỗi 1 0 1 0.':
        'dãy chữ số đọc tách từng chữ; ASR gộp thành một số (“1010”) — đủ từng chữ số theo đúng thứ tự, lệch chỉ vì cách viết liền; dãy hiện trên màn hình; mọi từ khác khớp',
    'Hai, y không rỗng.':
        'ASR chép “2. Y không rổng”: đủ cả bốn từ, chỉ lệch thanh ngã/hỏi ở “rỗng”; điều kiện hiện trên màn hình',
    'Ghi vết trên chuỗi 0 0 1 1.':
        'dãy chữ số đọc tách từng chữ; ASR gộp thành một số (“0011”) — đủ từng chữ số theo đúng thứ tự, lệch chỉ vì cách viết liền; dãy hiện trên màn hình; mọi từ khác khớp',
    'Bảng cộng một của bài 9 biến 1 0 1 1 thành 1 1 0 0 sau 3 bước.':
        'ASR chép “101 x 1100”: dãy sau đúng, dãy đầu gộp “1 0 1” và nuốt chữ 1 cuối cùng “thành” — lệch ở chỗ hai dãy chữ số liền nhau, cùng loại với “0011” của L08; băng hiện trên màn hình — NOT_VERIFIED bằng tai người',
    'Câu một, nạp bảng đảo bit vào bộ mô phỏng với đầu vào 0 1 1 0, băng cuối là gì, sau mấy bước?':
        'dãy chữ số đọc tách từng chữ; ASR gộp thành một số (“0110”) — đủ từng chữ số theo đúng thứ tự, lệch chỉ vì cách viết liền; dãy hiện trên màn hình; bảng/bản, bit/biết (probe p1 CSA), băng/bằng là nhầm âm cuối, thanh của ASR',
    'Câu một, có bao nhiêu chuỗi ngoặc cân bằng độ dài 8?':
        'ngoặc/hoặc, cân/kinh, 8/“tắm”: ASR nghe sai ở câu 11 từ; “chuỗi ngoặc cân bằng” chép đúng ở các câu dài khác của L06 — NOT_VERIFIED bằng tai người',
    # ── NET (2026-10-29): mỗi lý do dựa trên bản chép trong out/NET/<id>/asr_report.md ──
    'Tầng vật lý đẩy từng bit qua dây đồng, sóng vô tuyến hay cáp quang.':
        'ASR chép “Tần vật lý để từng biết qua giây đồng, sống vô tuyến hay cáp quan”: tầng/tần, quang/quan (âm cuối ng/n), đẩy/để, sóng/sống (thanh), bit/biết (nhóm bit đã biết, probe CSA); đủ mọi âm tiết — NOT_VERIFIED bằng tai người',
    'Hình này vẽ đúng tỉ lệ thời gian.':
        'ASR chép “Hình này phải đúng tỷ lệ thời gian”: tỉ/tỷ là hai cách viết cùng từ; vẽ/phải lệch ở câu 7 từ — NOT_VERIFIED bằng tai người',
    'Nhưng 15 mi li giây lan truyền vẫn còn nguyên.':
        '“mi li giây” ASR viết tắt “ml dây/ml/ms” (cùng âm mi-li, giây/dây là nhầm gi/d đã biết); 15 khớp',
    'Câu hai, tổng là 2 phẩy 5 mi li giây.':
        'ASR chép “Câu 2 tổng là 2,5ml.”: số 2,5 khớp; “mi li giây” viết tắt “ml” — cùng âm, ASR rút gọn đơn vị',
    'Nâng lên 1 tỉ bit mỗi giây, nhanh gấp 10 lần, thì vẫn mất khoảng 5 phẩy 0 1 2 mi li giây.':
        'ASR chép “1 tỷ bit… gấp 10 lần… 5.01mm lý giây”: tỉ/tỷ cùng từ; “5 phẩy 0 1 2” gộp còn 5.01 và chữ 2 dính vào “mi li” — dãy chữ số đọc tách, ASR gộp số (nhóm đã biết) — NOT_VERIFIED bằng tai người',
    'Tệp 25 MB tải mất bao lâu?':
        'ASR chép “tệp 25 MB tại mức bao lâu?”: MB (mê-ga-byte) khớp; tải mất/tại mức là nhầm thanh và âm cuối ở câu 7 từ — NOT_VERIFIED bằng tai người',
    'Bit chẵn lẻ là thêm một bit để tổng số bit 1 thành số chẵn.':
        'ASR chép “Biết chẳng lẽ … số chẳng”: bit/biết (nhóm bit, probe CSA), chẵn/chẳng và lẻ/lẽ chỉ khác thanh ngã/hỏi; cụm “chẵn lẻ” lặp ở mọi câu L03 — NOT_VERIFIED bằng tai người',
    'Dữ liệu 1 0 1 1, 0 0 1 có 4 bit 1, nên bit chẵn lẻ là 0.':
        'ASR chép “1011-001 … 4 bit 1, nền bit chẳng lẽ là không”: hai dãy chữ số đúng từng chữ (ASR gộp, nhóm đã biết); chẵn lẻ/chẳng lẽ khác thanh; số 0 cuối chép “không” — đúng',
    'Chào bạn, nhiễu điện làm một bit trên dây đổi từ 0 thành 1.':
        'ASR chép “nhũ điện là một bức tranh giây đổi từ không thành một”: nhiễu/nhũ, bit trên/bức tranh, dây/giây là nhầm của ASR ở đầu đoạn; 0, 1 khớp — NOT_VERIFIED bằng tai người',
    'Nếu số bit bị lật là số chẵn thì bit chẵn lẻ không đổi, mà nhiễu thường làm lật cả một chùm bit liền nhau.':
        'ASR chép “số bít … số chẳng … bít chẳng lẽ … chùn bít”: bit/bít, chẵn/chẳng, lẻ/lẽ, chùm/chùn chỉ khác thanh hoặc âm cuối m/n; mọi từ còn lại khớp — NOT_VERIFIED bằng tai người',
    'Lỗi thứ ba, tin bit chẵn lẻ bắt được mọi lỗi.':
        'ASR chép “tin biết chẳng lẽ bắt được mọi lỗi”: bit/biết (nhóm bit), chẵn lẻ/chẳng lẽ khác thanh; như mọi câu “chẵn lẻ” của L03',
    'Dữ liệu 1 0 1 1, 1 0, đa thức sinh 1 0 0 1.':
        'ASR chép “101.1.0 đã thức sinh 1001”: dãy chữ số đúng từng chữ (ASR gộp/chấm); dữ/giữ, đa/đã là nhầm d/gi và thanh — NOT_VERIFIED bằng tai người',
    'Sau 9 lần XOR, ba bit cuối còn lại là phần dư 1 0 0.':
        'ASR chép “Sau 9 lần XOR, bà biết cuối còn lại là phần dư 100”: XOR khớp; ba bit/bà biết khác thanh (nhóm bit); “1 0 0” gộp thành “100” — đủ chữ số',
    'Chuỗi gửi đi là dữ liệu nối thêm 0 1 1.':
        'ASR chép “Chủy gửi đi là giữ liệu nối thêm 011”: chuỗi/chủy khác vần, dữ/giữ nhầm d/gi; “0 1 1” gộp thành “011” — đủ chữ số — NOT_VERIFIED bằng tai người',
    'Hôm nay ta học cách chia sẻ một đường truyền chung, Ethernet, và bộ chuyển mạch, lý do mạng ngày nay gần như không còn va chạm.':
        'độ khớp 1,0: ASR chép đúng “ethernet” (Ê-thơ-nét, lexicon_vi.NET.yaml p1 8/8); cờ chỉ do so từng âm tiết “ê, thơ, nét” với một từ — không có lỗi',
    'Câu một, phần máy có mấy bit?':
        'ASR chép “phần máy có máy biết”: mấy/máy khác thanh, bit/biết nhóm bit; câu 7 từ — NOT_VERIFIED bằng tai người',
    'Địa chỉ đuôi 77 viết nhị phân là 0 1 0 0, 1 1 0 1.':
        'ASR chép “0100-1101”: tám chữ số đúng thứ tự (ASR gộp dãy chữ số, nhóm đã biết); 77 khớp',
    'Khi tra bảng, tìm mọi mục khớp rồi chọn mục dài nhất.':
        'ASR chép “Khi tra bản, tìm mỗi mục hấp rồi chọn mục dài nhất”: bảng/bản (âm cuối ng/n), mọi/mỗi, khớp/hấp — nhầm của ASR; câu đủ nghĩa trên màn hình — NOT_VERIFIED bằng tai người',
    'Còn 8 chấm 8 chấm 8 chấm 8 chỉ khớp đường mặc định.':
        'ASR chép “Còn 8.8.8.8 chỉ khắp đường mặc định”: “chấm” được viết thành dấu chấm — đúng địa chỉ; khớp/khắp khác vần',
    'Lỗi thứ nhất, nghĩ bảng ghi cả đường đi.':
        'ASR chép “Lội thứ nhất, nghĩ bản ghi cả đường đi”: lỗi/lội (cặp đã gặp ở TOC L06), bảng/bản âm cuối ng/n — NOT_VERIFIED bằng tai người',
    'So sánh hai giao thức.':
        'câu 5 từ; ASR chép “Sò sánh 2 dâu thức”: so/sò, giao/dâu (nhầm gi/d) — câu ngắn mở đầu bảng so sánh, nội dung đầy đủ trên màn hình — NOT_VERIFIED bằng tai người',
    'Đa số gói UDP vẫn tới nơi, UDP chỉ không bảo đảm, mất thì không tự gửi lại, đến lộn thứ tự thì không tự sắp.':
        'UDP đọc thô (lexicon_vi.NET.yaml: probe p1 7/8, đối chứng 0/8); ở câu này ASR chép “URP” hai lần, độ khớp 0,923 — NOT_VERIFIED bằng tai người',
    'Với dừng chờ, hiệu suất bằng 0 phẩy 0 0 8 chia cho 30 phẩy 0 0 8, xấp xỉ 0 phẩy 0 0 0 2 7.':
        'ASR chép “0.008 chia cho 30.008, sắp xỉ 0.00027”: ba số thập phân đúng từng chữ số; xấp/sắp nhầm x/s',
    'Ba, kiểm ngược, 3751 nhân 0 phẩy 0 0 8 xấp xỉ 30 phẩy 0 0 8 mi li giây.':
        'ASR chép “3751 nhân 0.008 xếp xỉ 30.008 mili giây”: mọi số đúng; xấp/xếp lệch vần',
    'Gói dài 8 nghìn bit, đường 1 tỉ bit mỗi giây, nên thời gian phát là 0 phẩy 0 0 8 mi li giây, còn một lượt đi về là 30 mi li giây.':
        'ASR chép “8.000 bit … 1 tỷ bit … 0,008 ms … 30 ms”: mọi số đúng, “mi li giây” viết tắt ms, tỉ/tỷ cùng từ, nên/nền khác thanh',
    'Khi nghẽn, gói rơi hàng loạt, nên phải rút mạnh để hàng đợi kịp thoát.':
        'ASR chép “Khi nhén, gói trơi … trúc mạnh để hàng đời kịp thoát”: nghẽn/nhén, rơi/trơi, rút/trúc (đổi r → tr như TOC “Rai” → “trai”), đợi/đời — NOT_VERIFIED bằng tai người',
    'Khi êm, tăng chậm để dò dần phần dư, không gây nghẽn đột ngột.':
        'ASR chép “khi em tăng chậm … không gây ngãng đột ngục”: êm/em, nghẽn/ngãng, ngột/ngục — nhầm vần của ASR; “nghẽn” ở các câu khác của L11 chép đúng — NOT_VERIFIED bằng tai người',
    'Lỗi thứ hai, lẫn cửa sổ tắc nghẽn với cửa sổ của bên nhận.':
        'ASR chép “Lội thứ 2, lẫn cửa sổ tắt ngạn với cửa sổ của bên nhận”: lỗi/lội, tắc nghẽn/tắt ngạn — nhầm âm cuối và vần; “cửa sổ tắc nghẽn” chép đúng ở các câu khác của L11 — NOT_VERIFIED bằng tai người',
    'Lỗi thứ nhất, nghĩ DNS chỉ dùng UDP.':
        'DNS đọc “đê en ét” (lexicon_vi.NET.yaml p1 5/8, NOT_VERIFIED); ASR chép “đe an ác”: đủ ba âm tiết; UDP khớp; lỗi/lội — NOT_VERIFIED bằng tai người',
    'Lỗi thứ nhất, nghĩ Diffie–Hellman chống được mọi kẻ gian.':
        'Diffie–Hellman đọc “Đi-phi Hen-man” (lexicon_vi.NET.yaml p1 8/8; ASR không tách m/n nên NOT_VERIFIED); ASR chép “đi phi henman” — đủ bốn âm tiết, chỉ viết liền',
    'Hôm nay ta học mã đối xứng, mã khoá công khai, và trao đổi khoá Diffie–Hellman trên số nhỏ.':
        'Diffie–Hellman đọc “Đi-phi Hen-man” (lexicon NET p1 8/8); ASR chép “DeFi Handman” — đúng bốn âm tiết theo cách viết tiếng Anh, độ khớp 0,9 — NOT_VERIFIED bằng tai người',
    'Năm 1976, Diffie–Hellman chỉ ra cách làm, chỉ bằng lũy thừa và phép chia lấy dư.':
        'Diffie–Hellman đọc “Đi-phi Hen-man” (lexicon NET p1 8/8); ASR chép “đi phi Henman” — đủ âm tiết, viết liền; độ khớp 0,939',
    # ── RBM (2026-10-29): lý do dựa trên bản chép trong out/RBM/<id>/asr_report.md ──
    'Tích của hai quaternion đơn vị vẫn có độ dài 1.':
        'quaternion → “Qua Tân Yên” (nhóm quaternion, PARTIAL); số 1 cuối câu chép “mục”: âm cuối t → c của ASR ở âm tiết cuối câu (cùng hiện tượng “một” → “mục” ở L08, L11) — NOT_VERIFIED bằng tai người',
    'Tổng kết lại, ta nhân quaternion theo bảng i, j, k.':
        'quaternion → “qua tên ương” (nhóm quaternion, PARTIAL); nhân/nhận là nhầm thanh; i, j, k chép “y, di, ca” — tên chữ cái kiểu Việt (SKILL Bước 5); bảng hiện trên màn hình — NOT_VERIFIED bằng tai người',
    'Chỉ góc Euler bị khoá gimbal.':
        'bản chép “Chỉ góc ở le bị khóa gimbal” đúng mọi từ: Euler → “ở le” (probe DMS p1_ten Ơ-le 8/8), độ khớp 0,769 chỉ do cách viết tên — câu 6 từ, ≥ 0,7',
    'Lỗi thứ ba, lấy nghịch đảo của cả ma trận T bằng chuyển vị.':
        'nghịch đảo → “nhiệt đạo”, cả → “cá”: nhầm phụ âm đầu ng/nh và thanh của ASR; “nghịch đảo” chép đúng ở các câu khác của L03 — NOT_VERIFIED bằng tai người',
    'J chính là Jacobian của công thức động học thuận ở bài 4, hàng ứng với x, y, cột ứng với hai khớp.':
        'Jacobian đọc “Gia-cô-biên” (lexicon chung, CS115 L05); ASR chép “gia co biên”: cùng âm; J → “di” là tên chữ cái kiểu Việt; cột/cục là nhầm âm cuối — NOT_VERIFIED bằng tai người',
    'Đi cả bước là đọc độ dốc sai chỗ.':
        'đọc → “độc”, dốc → “chốc”: nhầm thanh và phụ âm đầu của ASR ở câu 8 từ (≥ 0,7); “độ dốc” chép đúng ở các câu khác của L08 — NOT_VERIFIED bằng tai người',
    'Nói cách khác, Gradient Descent là Euler chạy trên dòng chảy xuống dốc, w phẩy bằng âm đạo hàm của f.':
        'Gradient Descent đọc “grê-đi-ần đi-xen” (lexicon chung 6/6); ASR chép “gradient descent”: đúng; Euler → “ơ le”, w → “về kép”, f → “ép” là tên chữ cái kiểu Việt; chảy/chạy, phẩy/phải là nhầm thanh đã gặp ở bảng tham khảo — NOT_VERIFIED bằng tai người',
    'Tốc độ học của Gradient Descent tuân theo cùng một luật.':
        'Descent đọc “đi-xen” (lexicon chung; medium chép “Descent” khi dò) → ASR chép “đi xem”: cùng âm, lệch âm cuối; “một luật” → “mục lực”: âm cuối t → c và lực/luật — NOT_VERIFIED bằng tai người',
    'Đúng ngưỡng 0 phẩy 2, hệ số là âm 1, dãy dao động mãi giữa 1 và âm 1.':
        '“0 phẩy 2” → “không phải 2”: phẩy/phải là nhầm thanh lặp lại ở nhiều câu RBM (bảng tham khảo L07); hệ/hề, dãy/dạy (d/gi), động/đồng là nhầm thanh; các số 0, 2, 1, âm 1 khớp — NOT_VERIFIED bằng tai người',
    'Khớp tốt trong khoảng 0 đến 3 ki-lô-gam chưa nói gì về 10 ki-lô-gam.':
        'ASR viết “ki-lô-gam” thành “kg” (đúng đơn vị, chỉ khác cách viết) nên độ khớp tụt; chưa/chứ là nhầm thanh; các số 0, 3, 10 khớp',
    'Đảo mô hình để sửa số đọc.':
        'đảo → “đạo”, đọc → “độc”: nhầm thanh của ASR ở câu 7 từ (độ khớp 0,714 ≥ 0,7); “sửa số đọc” chép đúng ở câu kế tiếp — NOT_VERIFIED bằng tai người',
    'Bây giờ sửa số đọc, nếu cảm biến báo 5 thì giá trị thật bằng 5 trừ 1 phẩy 03, chia 1 phẩy 98, xấp xỉ 2 phẩy 005 ki-lô-gam.':
        'ASR viết số thành “5,1%3, chia 1,98, sắp xỉ 2,005 kg”: “trừ 1 phẩy 03” bị gộp thành “1%3” (ASR chuẩn hoá số), các chữ số 5, 1, 0, 3, 1, 98, 2, 005 đều có; kg là cách viết của ki-lô-gam; xấp/sắp là nhầm x/s — NOT_VERIFIED bằng tai người',
    'Gọi x gạch và y gạch là trung bình.':
        'gạch → “gạp”: nhầm âm cuối ch/p của ASR; x → “ít” là tên chữ cái kiểu Việt; ký hiệu x gạch, y gạch hiện trên màn hình — NOT_VERIFIED bằng tai người',
    'Nhiễu nằm ở số đọc y, mà bình phương tối thiểu giả định nhiễu ở biến được khớp.':
        'nhiễu → “nhịu”, đọc → “độc”, khớp → “khấp”: nhầm vần và thanh của ASR; “bình phương tối thiểu” chép đúng — NOT_VERIFIED bằng tai người',
    'Lỗi thứ hai, nghĩ máy nào cũng dừng.':
        'ASR chép “Lội thứ hai, nghĩ mấy nào cũng dừng”: lỗi/lội, máy/mấy là nhầm thanh; cùng mẫu “Lỗi thứ …” các bài khác chép đúng — NOT_VERIFIED bằng tai người',
}
GROUP = [
    (lambda r, s: "De Morgan" in s and re.search(r"(^|, )(mo|de|morgan)(,|$)", r),
     "De Morgan đọc “Đơ Mo-gần” (lexicon_vi.DMS.yaml, probe p1_ten 8/8, đối chứng 0/8); ASR chép “đơ mô gần/đơ Morgan”, cùng âm"),
    (lambda r, s: re.search(r"(^|, )p(,|$)", r), P2),
    (lambda r, s: "Fermat" in s and re.search(r"(^|, )(phéc|ma)(,|$)", r),
     "Fermat đọc “Phéc-ma” (lexicon DMS, probe p1_ten 8/8 khi khoá nhận “phét ma”); ASR không phân biệt âm cuối c/t — chép “phét ma”, cùng âm"),
    (lambda r, s: "Cayley" in s and re.search(r"(^|, )(kê|li)(,|$)", r),
     "Cayley đọc “Kê-li” (probe p1_ten 8/8); ASR chép “kê ly”, cùng âm"),
    (lambda r, s: "Euler" in s and re.search(r"(^|, )(ơ|le)(,|$)", r),
     "Euler đọc “Ơ-le” (probe p1_ten 8/8); ASR chép “ơ le/ở Lê/ở lè”, cùng âm hoặc lệch thanh"),
    (lambda r, s: re.search(r"\b(KB|KiB|MB|MiB|GB|TiB)\b", s) and re.fullmatch(r"(ki|lô|mê|ga|ghi|tê|t|ra|byte)(, (ki|lô|mê|ga|ghi|tê|t|ra|byte))*", r),
     "đơn vị đọc theo lexicon_vi.OSY.yaml (KB/KiB → “ki-lô-byte”, MB/MiB → “mê-ga-byte”, GB → “ghi-ga-byte”, TiB → “tê-ra-byte”); ASR chép “kilobyte/megabyte/gigabyte/terabyte/kb” hoặc tách “kg bay”, “tê ra bay” — đúng đơn vị, chỉ khác cách viết; “byte” → “bay/bai” cùng âm (probe p1 CSA)"),
    (lambda r, s: re.fullmatch(r"byte(, byte)*", r),
     "“byte” đọc thô /bai/ — probe audit/csa/probes/p1_thuat_ngu.md: ASR chép “bay” 8/8 (cùng âm), đối chứng 0/8; lexicon foreign_ok"),
    (lambda r, s: re.fullmatch(r"(bit|byte)(, (bit|byte))*", r),
     "“bit” ASR chép “bích/biết” (probe p1 CSA: không cách viết nào phân định âm cuối t/ch) — NOT_VERIFIED bằng tai người; “byte” → “bay” cùng âm"),
    (lambda r, s: "ô-tô-mát" in s and re.search(r"(^|, )ô(,|$)", r),
     "“ô-tô-mát” ASR chép “Automat / Otomac / automatic”: đúng từ mượn, chỉ khác cách viết; chép đúng ở mọi bài TOC có từ này"),
    (lambda r, s: "Turing" in s and re.search(r"(^|, )(tua|rinh)(,|$)", r),
     "Turing đọc “Tua-rinh” (lexicon_vi.TOC.yaml, probe p1+p2 6/8 — tốt nhất trong 6 cách viết); ASR chép “Turing / Turin / tu trinh / tô rinh”: đổi r → tr như “Rai” → “trai” — NOT_VERIFIED bằng tai người"),
    (lambda r, s: "Kleene" in s and re.search(r"(^|, )(cờ|li|ni)(,|$)", r),
     "Kleene đọc “Cờ-li-ni” (probe p1 7/8, đối chứng 0/8); ASR chép “Kalini / Cligny / Coligny”: đủ ba âm k-l-n, khác cách viết"),
    (lambda r, s: "Rice" in s and re.search(r"(^|, )rice(,|$)", r),
     "Rice đọc thô (probe p1 6/8; foreign_ok); ASR chép “Rice/Ricecom” hoặc “trai” (r → tr, đã biết) — NOT_VERIFIED bằng tai người"),
    (lambda r, s: "Sigma" in s and re.search(r"(^|, )xích(,|$)", r),
     "Sigma đọc “xích ma” (lexicon chung); ASR chép “Sít ma”: cùng âm, lệch âm cuối ch/t; chữ Σ hiện trên màn hình"),
    (lambda r, s: re.search(r"\bw\b", s) and re.fullmatch(r"(v, )?kép(, (v, )?kép)*", r),
     "chữ w đọc “vê kép” (luật chung); ASR chép “Vket / V-ket”: cùng âm; chữ w hiện trên màn hình"),
    (lambda r, s: re.search(r"\bsin\b", s) and re.fullmatch(r"sin(, (sin|cos|t|ta|tê))*", r),
     "sin đọc thô “sin” (foreign_ok trong lexicon_vi.RBM.yaml); ASR chép “sinh” — cùng âm, chỉ khác âm cuối n/nh mà tiếng Việt không phân biệt ở âm tiết này; hàm sin hiện trên màn hình"),
    (lambda r, s: "robot" in s and re.fullmatch(r"robot(, robot)*", r),
     "robot đọc thô (foreign_ok lexicon RBM, cùng cách đọc ở mọi bài RBM); ASR chép “rô bốt / trò bốc” — đổi r → tr như TOC “Rai” → “trai” — NOT_VERIFIED bằng tai người"),
    # ── RBM (2026-10-29): nhóm theo lexicon_vi.RBM.yaml và bản chép trong out/RBM/<id>/asr_report.md ──
    (lambda r, s: "quaternion" in s.lower() and re.fullmatch(r"(tơ|ni|ơn)(, (tơ|ni|ơn))*", r),
     "quaternion đọc “qua-tơ-ni-ơn” (lexicon_vi.RBM.yaml, probe p1 + p2: tốt nhất 4/8, PARTIAL); ASR chép “qua tơ niên / qua tơ ni ân / qua tên yên”: cùng bốn âm tiết, lệch vần — NOT_VERIFIED bằng tai người"),
    (lambda r, s: "gimbal" in s and re.fullmatch(r"gim(, gim)*", r),
     "gimbal đọc “gim-bồ” (lexicon RBM, probe p1 7/8); ASR chép “Gimbo / ghim bồ / gimbal”: cùng âm"),
    (lambda r, s: re.search(r"\bcos\b", s) and re.fullmatch(r"(cô|sin)(, (cô|sin))*", r),
     "cos đọc “cô-sin” (lexicon RBM, probe p2: bản chép “cô xin / cosin / cosine” đúng âm), sin đọc thô (foreign_ok, “sinh” cùng âm); hàm hiện trên màn hình"),
    (lambda r, s: re.fullmatch(r"héc(, héc)*", r),
     "Hz đọc “héc” (lexicon RBM p1): ASR không tách âm cuối c/t — chép “hét / H / h”, đối chứng “hét” cũng chép “hét”; các số tần số trong câu khớp — NOT_VERIFIED bằng tai người"),
    (lambda r, s: re.fullmatch(r"radian(, radian)*", r),
     "radian đọc thô (lexicon RBM p1: thô 8/8); ASR chép “ra đi ăn / ra đi an”: cùng ba âm tiết"),
    (lambda r, s: "theta" in s and re.fullmatch(r"(tê|ta)(, (tê|ta))*", r),
     "theta đọc “tê-ta” (lexicon RBM p2 7/8); ASR chép “Teta / tê ta”: cùng âm"),
    (lambda r, s: "Manhattan" in s and re.fullmatch(r"(man|hát|tần)(, (man|hát|tần))*", r),
     "Manhattan đọc “Man-hát-tần” (lexicon chung); ASR chép “mang hát tần / mang hát tầng”: cùng ba âm tiết, lệch âm cuối n/ng"),
    (lambda r, s: re.search(r"\bô\b", s) and re.fullmatch(r"ô(, ô)*", r),
     "từ “ô” (ô lưới) bị ASR viết thành chữ “O / OK / o”: cùng âm, ASR chọn cách viết chữ cái Latinh; nghĩa hiện trên màn hình"),
    (lambda r, s: re.search(r"(^|, )[a-oq-z](,|$)", r),
     "tên chữ cái đọc kiểu Việt, ASR chép nhầm chữ (q→quy, x→ích, k→ca) — nhóm đã biết (SKILL Bước 5); chữ hiện trên màn hình"),
]


COURSE = "DMS"


def flagged(lid):
    rows, rep = [], (ROOT / "out" / COURSE / lid / "asr_report.md").read_text(encoding="utf-8")
    for line in rep.split("## Tham khảo")[0].splitlines():
        c = [x.strip() for x in line.strip().strip("|").split("|")]
        if len(c) == 8 and c[0].isdigit() and c[7] == "—":
            rows.append((c[2], c[5] if c[5] != "—" else ""))
    return rows


args = sys.argv[1:]
COURSE = "DMS"
if args and args[0] == "--course":
    COURSE, args = args[1].upper(), args[2:]
for lid in args:
    tpl = next((ROOT / "audit" / COURSE.lower() / "src").glob(lid + "_*.tpl.yaml"), None)
    p = tpl or next((ROOT / "lessons" / COURSE.lower()).glob(lid + "_*.yaml"))
    sp = lv.load_spec(p)
    have = {s.strip() for sc in sp["scenes"] for st in sc["steps"] for s in lv.sentences(st.get("say", ""))}
    done = {str(x["sentence"]).strip() for x in sp.get("asr_reviewed") or []}
    new = []
    for sent, risk in flagged(lid):
        if sent not in have or sent in done:
            continue
        reason = HAND.get(sent) or "; ".join(dict.fromkeys(t for f, t in GROUP if f(risk, sent)))
        if not reason:
            print("THIẾU LÝ DO", lid, "|", sent, "|", risk)
            continue
        new.append((sent, reason))
    if not new:
        print(lid, "0 mục mới")
        continue
    text = p.read_text(encoding="utf-8")
    lines = "".join(f'  - {{sentence: "{s}", reason: "{r}"}}\n' for s, r in new)
    head = re.search(r"\nasr_reviewed:[ \t]*(#[^\n]*)?\n", text)  # CS115 có dòng chú thích sau khoá
    if head:
        text = text[:head.end()] + lines + text[head.end():]
    elif "\nasr_reviewed: []\n" in text:
        assert text.count("\nasr_reviewed: []\n") == 1, "khung bài phải có đúng một `asr_reviewed: []`"
        text = text.replace("\nasr_reviewed: []\n", "\nasr_reviewed:\n" + lines, 1)
    else:  # bài chưa có khoá (PAR L07–L12): thêm ngay trước `scenes:`
        assert "asr_reviewed" not in text and text.count("\nscenes:\n") == 1, "không tìm được chỗ đặt `asr_reviewed`"
        text = text.replace("\nscenes:\n", "\nasr_reviewed:\n" + lines + "scenes:\n", 1)
    p.write_text(text, encoding="utf-8")
    print(lid, len(new), "mục →", p.relative_to(ROOT))
