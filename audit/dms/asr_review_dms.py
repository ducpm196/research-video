"""Ghi `asr_reviewed` cho câu ASR gắn cờ của khoá DMS — đọc thẳng out/DMS/<id>/asr_report.md (bảng đầu, cột “đã xem xét” = —).
Lý do theo nhóm đã có bằng chứng dò (audit/dms/probes/*.md); câu không thuộc nhóm nào phải có lý do viết tay ở HAND, nếu không
script in “THIẾU LÝ DO” và KHÔNG ghi — câu đó phải sửa lời đọc (câu ngắn) hoặc người nghe lại.
Bài sinh từ mẫu (audit/dms/src/*.tpl.yaml) thì ghi vào MẪU rồi ghép lại, vì mẫu là nguồn duy nhất.
Chạy: .venv/Scripts/python audit/dms/asr_review_dms.py L01 L02 …  (khoá khác: --course CSA L00 L01 …)"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
import lv  # noqa: E402
import yaml  # noqa: E402

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
    # ── Khoá mới: RLN (2026-11-03) ──
    'Bước bốn, chuyển gam-ma nhân G sang vế trái, được G nhân 1 trừ gam-ma bằng 1, rồi chia cho 1 trừ gam-ma, được chia vì gam-ma nhỏ hơn 1.':
        'ASR chép “Bước 4, chuyển gama nhân dây sang với trái, được dây nhân một trừ gama bằng một, rồi chia cho một trừ gama, được chia vì gama nhỏ hơn một.” (0.781): gam-ma (γ) ASR viết “gamma”; lệch âm/thanh thuần Việt: vế/với — NOT_VERIFIED bằng tai người',
    'Bước hai, theo công thức đệ quy, G một bằng r hai cộng gam-ma nhân G hai.':
        'ASR chép “Bước 2, theo công thức đệ quy, dê 1 bằng Adder 2 cộng Gamma Nhân v2.” (0.8): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; gam-ma (γ) ASR viết “gamma” — NOT_VERIFIED bằng tai người',
    'Bước ba, G không bằng r một cộng gam-ma nhân G một.':
        'ASR chép “Bước 3, về không bằng R1 cộng gamma nhân dế 1.” (0.72): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; gam-ma (γ) ASR viết “gamma” — NOT_VERIFIED bằng tai người',
    'Lấy căn hai vế, gam-ma phải lớn hơn căn của 0 phẩy 6, xấp xỉ 0 phẩy 775.':
        'ASR chép “Lấy căn 2 v, gamma phải lớn hơn căn của 0,6, sắp xỉ 0,775.” (0.791): gam-ma (γ) ASR viết “gamma”; “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; lệch âm/thanh thuần Việt: vế (trong “vế gam ma” → “v gamma”), xấp/sắp, không (trong “không phẩy” → “”) — NOT_VERIFIED bằng tai người',
    'Đứng ở A mà luôn bước sang B thì ô A đáng giá 5 phẩy 263.':
        'ASR chép “Đứng ở A mà luôn bước sang B thì OA đáng giá 5,263.” (0.872): “ô” (ô lưới) ASR viết chữ “O”; chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải” — NOT_VERIFIED bằng tai người',
    'Còn nếu mỗi lần tung đồng xu để chọn đi hay ở, thì cũng ô A đó chỉ đáng giá 3 phẩy 448.':
        'ASR chép “Còn nếu mỗi lần tung đồng xu để chọn đi hay ở, thì cũng OA đó chỉ đáng giá 3,448.” (0.906): “ô” (ô lưới) ASR viết chữ “O”; chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải” — NOT_VERIFIED bằng tai người',
    'Còn s phẩy là trạng thái kế tiếp, nơi hành động dẫn tới.':
        'ASR chép “Còn F phải là trạng thái kế tiếp, nơi hành động dẫn tới.” (0.846): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải” — NOT_VERIFIED bằng tai người',
    'Hình vẽ trò chơi hai ô.':
        'ASR chép “Hình vẽ trò chơi 2U.” (0.833): “ô” (ô lưới) ASR viết chữ “O” — NOT_VERIFIED bằng tai người',
    'Bước hai, sau khi tới s phẩy, phần còn lại của trò chơi chỉ phụ thuộc s phẩy, không cần nhớ đã đi đường nào.':
        'ASR chép “Bước 2, sau khi tới F-phẩy, phần còn lại của trò chơi chỉ phụ thuộc F-phẩy, không cần nhớ đã đi đường nào.” (0.92): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Vì vậy kỳ vọng của G t cộng 1 chính là V của s phẩy.':
        'ASR chép “Vì vậy, kỳ vọng của GT cộng 1 chính là V của F phải.” (0.867): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải” — NOT_VERIFIED bằng tai người',
    'Dấu Sigma hoa nghĩa là cộng qua mọi hành động a.':
        'ASR chép “Dấu sigma hoa nghĩa là cộng qua mọi hành động nha.” (0.909): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Với chính sách 1, thay V của B bằng 0 phẩy 9 nhân V của A vào phương trình của A, ta được V của A bằng 1 cộng 0 phẩy 81 nhân V của A.':
        'ASR chép “Với chính sách 1, thay V của B bằng không phải chính nhân V của A vào phương trình qua, ta được V của A bằng một cộng không phải 81 nhân V của A.” (0.88): “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: chín (trong “phẩy chín” → “phải chính”), của (trong “của a” → “qua”) — NOT_VERIFIED bằng tai người',
    'V của A đi từ 1 ở vòng 1, lên 3 phẩy 428 ở vòng 10, và tới 5 phẩy 263 ở vòng 100.':
        'ASR chép “V của AD từ 1 ở vòng 1 lên 3,428 ở vòng 10 và tới 5,263 ở vòng 100.” (0.892): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; lệch âm/thanh thuần Việt: đi (trong “a đi” → “ad”) — NOT_VERIFIED bằng tai người',
    'Lỗi thứ nhất, nói giá trị của ô A mà không nói chính sách nào.':
        'ASR chép “Lỗi thứ nhất, nói giá trị của OA mà không nói chính sách nào.” (0.897): “ô” (ô lưới) ASR viết chữ “O”; chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Cùng ô A, hai chính sách cho 5 phẩy 263 và 3 phẩy 448.':
        'ASR chép “Cùng OA, hai chính sách cho 5,263 và 3,448.” (0.837): “ô” (ô lưới) ASR viết chữ “O”; chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải” — NOT_VERIFIED bằng tai người',
    'Với 10 nghìn trạng thái, riêng ma trận hệ số đã cần 800 triệu byte.':
        'ASR chép “Với 10.000 trạng thái, riêng ma trận hệ số đã cần 800 triệu bay.” (0.938): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Ta được k lớn hơn hoặc bằng lôgarit của 0 phẩy 001 chia cho lôgarit của gam-ma.':
        'ASR chép “Ta được ca lớn hơn hoặc bằng Logarit của 0.001 chi cho Logarit của Gamma.” (0.788): “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; gam-ma (γ) ASR viết “gamma”; lệch âm/thanh thuần Việt: không (trong “không phẩy” → “”), chia/chi — NOT_VERIFIED bằng tai người',
    'Khi gam-ma gần 1, lôgarit của gam-ma xấp xỉ âm của 1 trừ gam-ma, nên k xấp xỉ lôgarit của 1000, tức khoảng 6 phẩy 9, chia cho 1 trừ gam-ma.':
        'ASR chép “Khi gamma gần 1, logarith của gamma sắp sĩ âm của một trừ gamma nên cả sắp sĩ logarith của 1 nghìn tức khoảng 6,9 chia cho một trừ gamma.” (0.676): gam-ma (γ) ASR viết “gamma”; chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: xấp xỉ (trong “gam ma xấp xỉ” → “gamma sắp sĩ”), xấp xỉ (trong “k xấp xỉ” → “cả sắp sĩ”) — NOT_VERIFIED bằng tai người',
    'Cụ thể là c nhân căn của lôgarit t chia cho N.':
        'ASR chép “Cụ thể là xe nhân căn của Logarith Techi cho N.” (0.87): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: chia (trong “t chia” → “techi”) — NOT_VERIFIED bằng tai người',
    'Bước bốn, làm thử với t bằng 12, c bằng 2, và lôgarit của 12 xấp xỉ 2 phẩy 485.':
        'ASR chép “Bước 4, làm thử với T bằng 12, C bằng 2 và Logatrix của 12 sắp xỉ 2,485.” (0.885): “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; lệch âm/thanh thuần Việt: lôgarit/logatrix, xấp/sắp — NOT_VERIFIED bằng tai người',
    'Đen-ta bằng r cộng gam-ma nhân V của s phẩy, trừ V của s.':
        'ASR chép “Đen ta bằng add cộng gamma nhân v của x phải trừ v của x.” (0.774): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; gam-ma (γ) ASR viết “gamma”; “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải” — NOT_VERIFIED bằng tai người',
    'Phần G t cộng 1 chưa biết, nhưng ta đã có ước lượng của nó là V của s phẩy, nên thay vào chỗ G.':
        'ASR chép “Phần GT Cộng 1 chưa biết, nhưng ta đã có ước lượng của nó là V của F phải nên thay vào chỗ G.” (0.92): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải” — NOT_VERIFIED bằng tai người',
    'Ta kiểm bằng ví dụ 6.2 của sách, gồm năm ô A, B, C, D, E, bắt đầu ở C, mỗi bước sang trái hoặc phải với xác suất 0 phẩy 5.':
        'ASR chép “Ta kiểm bằng ví dụ 6.2 của sách gồm 5 OA, B, C, G, E bắt đầu ở C mỗi bước sang trái hoặc phải với xác suốt 0,5.” (0.892): “ô” (ô lưới) ASR viết chữ “O”; chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: suất/suốt — NOT_VERIFIED bằng tai người',
    'Đích dùng ước lượng của chính mình, nên nếu V của s phẩy ban đầu là 0 trong khi giá trị thật là 10, đích chỉ là 1 thay vì 10.':
        'ASR chép “Đích dùng ước lượng của chính mình nên nếu V của F phải ban đầu là không trong khi giá trị thật là 10, đích chỉ là 1 thay vì 10.” (0.935): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải” — NOT_VERIFIED bằng tai người',
    'Ta lấy đúng hành động a phẩy mà robot sẽ làm ở s phẩy, kể cả khi đó là nước chọn bừa.':
        'ASR chép “Ta lấy đúng hành động A phẩy mà robot sẽ làm ở F phẩy, kể cả khi đó là nước chọn bưa.” (0.909): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: bừa/bưa — NOT_VERIFIED bằng tai người',
    'Ta lấy giá trị của hành động tốt nhất ở s phẩy, dù robot có làm hành động đó hay không.':
        'ASR chép “Ta lấy giá trị của hành động tốt nhất ở F, dù robot có làm hành động đó hay không?” (0.927): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải” — NOT_VERIFIED bằng tai người',
    'Phép thử là in giá trị ở ô đích sau khi học, nó phải đúng bằng 0.':
        'ASR chép “Phép thử là yên giá trị ở Odix sau khi học, nó phải đúng bằng không?” (0.848): “ô” (ô lưới) ASR viết chữ “O”; lệch âm/thanh thuần Việt: in/yên, đích (trong “ô đích” → “odix”) — NOT_VERIFIED bằng tai người',
    'Theta cũ là một bản chép tham số được giữ nguyên một thời gian, gọi là mạng mục tiêu.':
        'ASR chép “Teta của là một bản chép tham số được giữ nguyên một thời gian, gọi là mạng mục tiêu.” (0.895): theta đọc “tê-ta” theo lexicon RLN (probe p1: 7/8), ASR viết “teta”; lệch âm/thanh thuần Việt: cũ/của — NOT_VERIFIED bằng tai người',
    'Công thức là y bằng r cộng gam-ma nhân số lớn nhất của Q tính bằng theta cũ.':
        'ASR chép “Công thức là y bằng Adder cộng Gamma nhân số lớn nhất của quy tính bằng Teta cũ.” (0.811): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; gam-ma (γ) ASR viết “gamma”; theta đọc “tê-ta” theo lexicon RLN (probe p1: 7/8), ASR viết “teta” — NOT_VERIFIED bằng tai người',
    'Kết quả trung bình khoảng 0 phẩy 001 mỗi lô.':
        'ASR chép “Các quả trung bình khoảng 0,001 mỗi lô.” (0.778): “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; lệch âm/thanh thuần Việt: kết/các, không (trong “không phẩy” → “”) — NOT_VERIFIED bằng tai người',
    'Phép thử là lô nào có bước kết thúc thì y phải bằng đúng r.':
        'ASR chép “Phép thử là lô nào có bước kết thúc thì y phải bằng đúng error.” (0.933): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Yếu tố thứ nhất là xấp xỉ hàm, dùng mạng nơ-ron thay bảng.':
        'ASR chép “Yếu tố thứ nhất là sắp sĩ hàm dùng mạng Neuron thay bản.” (0.786): lệch âm/thanh thuần Việt: xấp xỉ/sắp sĩ, bảng/bản — NOT_VERIFIED bằng tai người',
    'Điều thứ hai, hàm chữ S này biến một số thực theta thành xác suất, và tại theta bằng 0 nó bằng 0 phẩy 5.':
        'ASR chép “Điều thứ 2, hàm chữ S này biến một số thực Teta thành xác suất, và tại Teta bằng không nó bằng 0,5.” (0.92): theta đọc “tê-ta” theo lexicon RLN (probe p1: 7/8), ASR viết “teta” — NOT_VERIFIED bằng tai người',
    'Lôgarit tự nhiên của nó có đạo hàm đẹp, bằng 1 trừ hàm đó, còn lôgarit của 1 trừ hàm đó có đạo hàm bằng âm hàm đó.':
        'ASR chép “Logatic tự nhiên của nó có đạo hàm đẹp, bằng một trừ hàm đó, còn Logatic của một trừ hàm đó có đạo hàm bằng âm hàm đó.” (0.929): lệch âm/thanh thuần Việt: lôgarit/logatic, lôgarit/logatic — NOT_VERIFIED bằng tai người',
    'Pi của a khi biết s, với tham số theta, là xác suất chọn hành động a.':
        'ASR chép “Pi của A khi biết x với tham số θ là xác xuất chọn hành động A.” (0.941): theta đọc “tê-ta” theo lexicon RLN (probe p1: 7/8), ASR viết “θ” — NOT_VERIFIED bằng tai người',
    'Ví dụ hành động thứ nhất có xác suất bằng hàm chữ S của theta, và ở theta bằng 0 cả hai đều 0 phẩy 5.':
        'ASR chép “Ví dụ hành động thứ nhất có xác sát xuất bằng hàm chữ S của TETA, và ở TETA bằng 0 cả 2 đều 0,5.” (0.868): theta đọc “tê-ta” theo lexicon RLN (probe p1: 7/8), ASR viết “teta”; lệch âm/thanh thuần Việt: suất/sát xuất — NOT_VERIFIED bằng tai người',
    'Nhưng gradient của pi bằng pi nhân gradient của lôgarit pi, theo đạo hàm của lôgarit, nên gradient của J là kỳ vọng của G nhân gradient của lôgarit pi.':
        'ASR chép “Nhưng Gradient của Pi bằng Pi nhân Gradient của Logarith Pi, theo đạo hàm của Logarith, nền Gradient của Yi là kỳ vọng của Giai nhân Gradient của Logarith Pi.” (0.921): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: nên/nền — NOT_VERIFIED bằng tai người',
    'Bước ba, làm thử ngay ở theta bằng 0, gradient của lôgarit pi là 0 phẩy 5 cho hành động một và âm 0 phẩy 5 cho hành động hai, theo phần ôn thứ hai.':
        'ASR chép “Bước 3, làm thử ngay ở Teta bằng 0, Gradient của Logarith P là 0,5 cho hành động 1 và âm 0,5 cho hành động 2, theo phần ôn thứ 2.” (0.933): theta đọc “tê-ta” theo lexicon RLN (probe p1: 7/8), ASR viết “teta”; pi (π) ASR viết “P/π” — NOT_VERIFIED bằng tai người',
    'Cập nhật là theta thay bằng theta cộng an-pha nhân mẫu đó, và sách giáo khoa chuẩn gọi đây là thuật toán gradient chính sách cơ bản, công bố năm 1992.':
        'ASR chép “Cập nhật là Teta thay bằng Teta cộng an pha nhân mẫu đó và sách giáo khoa chuẩn gọi đây là thuộc toán Gradient Chính Sách Cơ Bản, công bố năm 1992.” (0.902): theta đọc “tê-ta” theo lexicon RLN (probe p1: 7/8), ASR viết “teta”; lệch âm/thanh thuần Việt: thuật/thuộc — NOT_VERIFIED bằng tai người',
    'Vậy G trừ b, nhân gradient lôgarit pi, vẫn có cùng kỳ vọng âm 0 phẩy 5.':
        'ASR chép “Vậy dây trừ B nhân Gradient Logaritpy vẫn có cùng kỳ vọng âm 0.5.” (0.889): pi (π) ASR viết “P/π”; “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; lệch âm/thanh thuần Việt: lôgarit (trong “lôgarit pi” → “logaritpy”) — NOT_VERIFIED bằng tai người',
    'Bước một, nếu chọn hành động một thì G bằng 10, gradient lôgarit pi bằng 0 phẩy 5, nên mẫu bằng 5.':
        'ASR chép “Bước 1, nếu chọn hành động 1 thì dế bằng 10, gradient logarith p bằng 0,5 nên mẫu bằng 5.” (0.917): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; pi (π) ASR viết “P/π” — NOT_VERIFIED bằng tai người',
    'Trừ đường cơ sở 11 thì theta mới là âm 0 phẩy 05, đúng hướng.':
        'ASR chép “Trừ đường cơ sở 11 thì Teta mới là âm 0.05, đúng hướng.” (0.903): “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; theta đọc “tê-ta” theo lexicon RLN (probe p1: 7/8), ASR viết “teta” — NOT_VERIFIED bằng tai người',
    'Như bước năm của ví dụ, một lượt chọn hành động một đẩy theta lên 0 phẩy 5, đi sai hướng gấp 10 lần độ lớn bước đúng.':
        'ASR chép “Như bước 5 của ví dụ, một lượt chọn hành động 1 đẩy Teta lên 0,5, đi sai hướng gấp 10 lần độ lớn bước đúng.” (0.964): theta đọc “tê-ta” theo lexicon RLN (probe p1: 7/8), ASR viết “teta” — NOT_VERIFIED bằng tai người',
    'Tổng kết lại, mục tiêu là lợi nhuận kỳ vọng J của theta.':
        'ASR chép “Tổng kết lại, mục tiêu là lợi những kỳ vọng di của TETA.” (0.846): theta đọc “tê-ta” theo lexicon RLN (probe p1: 7/8), ASR viết “teta”; lệch âm/thanh thuần Việt: nhuận/những — NOT_VERIFIED bằng tai người',
    'Mẹo lôgarit biến gradient của J thành kỳ vọng của G nhân gradient lôgarit pi, nên mỗi lượt chơi cho một mẫu không lệch nhưng rất nhiễu.':
        'ASR chép “Mẹo Logarith biến Gradian của di thành kỳ vọng của gia nhân Gradian Logarith P nên mỗi lượt chơi cho một mẫu không lệch nhưng rất nhiễu.” (0.935): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; pi (π) ASR viết “P/π” — NOT_VERIFIED bằng tai người',
    'Nếu đi chắc chắn tới s phẩy thì Q bằng r cộng gam-ma nhân V của s phẩy, ví dụ 5 phẩy 5.':
        'ASR chép “Nếu đi chắc chắn tới f\' thì quy bằng r cộng gamma nhân v của f\', ví dụ 5,5.” (0.851): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; gam-ma (γ) ASR viết “gamma” — NOT_VERIFIED bằng tai người',
    'Ở bài 7, ta sửa chính sách theo G trừ đường cơ sở, nhân gradient lôgarit pi, và đường cơ sở chỉ phụ thuộc trạng thái thì không làm lệch.':
        'ASR chép “Ở bài 7, ta sửa chính sách theo dây trừ đường cơ sở, nhận Gradient Logaritpy và đường cơ sở chỉ phụ thuộc trạng thái thì không làm lịch.” (0.889): pi (π) ASR viết “P/π”; lệch âm/thanh thuần Việt: nhân/nhận, lôgarit (trong “lôgarit pi” → “logaritpy”), lệch/lịch — NOT_VERIFIED bằng tai người',
    'An-pha V là tốc độ học của nhà phê bình, phần sửa bảng giá trị.':
        'ASR chép “An pha với là tốc độ học của nhà phê bình phần sửa bản giá trị.” (0.875): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: bảng/bản — NOT_VERIFIED bằng tai người',
    'Bước hai, giống bài 4, ta thay G bằng đích một bước, r cộng gam-ma nhân V của s phẩy, nên không phải chờ hết lượt.':
        'ASR chép “Bước 2, giống bài 4, ta thay dê bằng đích 1 bước r cộng gamma nhân v của f\' nền không phải chờ hết lượt.” (0.868): gam-ma (γ) ASR viết “gamma”; chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: nên/nền — NOT_VERIFIED bằng tai người',
    'Theta mới bằng 0 cộng 0 phẩy 1 nhân 1 phẩy 5 nhân 0 phẩy 5, bằng 0 phẩy 075, nên xác suất hành động một tăng từ 0 phẩy 5 lên khoảng 0 phẩy 519.':
        'ASR chép “TETA mới bằng không cộng 0,1 nhân 1,5 nhân 0,5, bằng 0,07 năm nên xác xuất hành động 1 tăng từ 0,5 lên khoảng 0,519.” (0.937): “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; theta đọc “tê-ta” theo lexicon RLN (probe p1: 7/8), ASR viết “teta”; lệch âm/thanh thuần Việt: mươi/∅, không (trong “không phẩy” → “”) — NOT_VERIFIED bằng tai người',
    'Kiểm tra thứ nhất dùng định nghĩa, vì đi chắc chắn tới s phẩy nên Q bằng 1 cộng 0 phẩy 9 nhân 5, bằng 5 phẩy 5.':
        'ASR chép “Kiểm tra thứ nhất dùng định nhĩa vì đi chắc chắn tới ếch phải nên quý bằng 1 cộng 0,9 nhân năm, bằng 5,5.” (0.893): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; lệch âm/thanh thuần Việt: nghĩa/nhĩa — NOT_VERIFIED bằng tai người',
    'Bây giờ đến lượt bạn, với gam-ma 0 phẩy 9, an-pha theta 0 phẩy 1, an-pha V 0 phẩy 2, theta bằng 0, và tác tử chọn hành động một.':
        'ASR chép “Bây giờ đến lượt bạn, với gamma 0.9, an pha teta 0.1, an pha v0.2, teta bàn không và tác tử chọn hành động 1.” (0.806): gam-ma (γ) ASR viết “gamma”; “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; theta đọc “tê-ta” theo lexicon RLN (probe p1: 7/8), ASR viết “teta”; lệch âm/thanh thuần Việt: bằng/bàn — NOT_VERIFIED bằng tai người',
    'Câu hai, cũng như vậy nhưng s phẩy là trạng thái kết thúc, đen-ta bằng bao nhiêu?':
        'ASR chép “Câu 2 cũng như vậy nhưng F phải là trạng thái kết thúc đen ta bằng bao nhiêu?” (0.889): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải” — NOT_VERIFIED bằng tai người',
    'Theta mới là 0 cộng 0 phẩy 1 nhân 0 phẩy 5 nhân 0 phẩy 5, bằng 0 phẩy 025.':
        'ASR chép “TETA mới là không cộng không phải 1 nhân, không phải 5 nhân, không phải 5, bằng không phải 0.25.” (0.756): “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; theta đọc “tê-ta” theo lexicon RLN (probe p1: 7/8), ASR viết “teta” — NOT_VERIFIED bằng tai người',
    'Quanh rô bằng 1, nhích tổng cộng 0 phẩy 002 làm mục tiêu đổi 0 phẩy 004, nên độ dốc là 2 và tối ưu còn kéo rô đi.':
        'ASR chép “Quanh row bằng một, nhất tổng cộng 0.002 là mục tiêu đổi 0.004, nền độ dốc là 2 và tối ưu còn kéo row đi.” (0.741): “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; rô (ρ) đọc tách âm tiết, ASR viết “row”; lệch âm/thanh thuần Việt: nhích/nhất, không (trong “không phẩy” → “”), làm/là, nên/nền — NOT_VERIFIED bằng tai người',
    'Hai số đó cộng lại bằng 1, vì xích-ma của âm x bằng 1 trừ xích-ma của x.':
        'ASR chép “Hai số đó cộng lại bằng một, vì sigma của âm ít bằng một trừ sigma cuối.” (0.757): xích-ma (σ) đọc tách âm tiết, ASR viết “sigma”; chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: của (trong “xích ma của x” → “sigma cuối”) — NOT_VERIFIED bằng tai người',
    'Xác suất càng gần 1 thì âm lôgarit càng gần 0.':
        'ASR chép “Sát xuất càng gần 1 thì âm logo đuít càng gần không.” (0.783): lệch âm/thanh thuần Việt: xác/sát, lôgarit/logo đuít — NOT_VERIFIED bằng tai người',
    'Ví dụ w bằng 4, đạo hàm 2w trừ 6 bằng 2, ê-ta bằng 0 phẩy 5, nên w mới bằng 3.':
        'ASR chép “Ví dụ v kép bằng 4, đạo hàm 2 v đúc trừ 6 bằng 2, eta bằng 0.5, nền v kép mới bằng 3.” (0.885): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; lệch âm/thanh thuần Việt: nên/nền — NOT_VERIFIED bằng tai người',
    'D là hiệu hai điểm, r A trừ r B.':
        'ASR chép “V là hiệu 2 điểm, rA-EB.” (0.667): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: trừ (trong “trừ r b” → “eb”) — NOT_VERIFIED bằng tai người',
    'Xác suất người chọn A bằng xích-ma của d, đó là mô hình so sánh cặp.':
        'ASR chép “Sa suốt người chọn A bằng sít ma của G, đó là mô hình so sánh cặp.” (0.765): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: xác suất/sa suốt, xích/sít — NOT_VERIFIED bằng tai người',
    'Bước một, mất mát khi người chọn A là âm lôgarit của xích-ma của d.':
        'ASR chép “Bước 1. Mất mát khi người chọn A là âm logarith của sigma của V.” (0.839): xích-ma (σ) đọc tách âm tiết, ASR viết “sigma”; chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Bước hai, vì d bằng r A trừ r B, tăng r A một đơn vị thì d tăng một, còn tăng r B thì d giảm một.':
        'ASR chép “Bước 2, vì dây bằng rA-rB, tăng rA1 đơn vị thì dây tăng 1, còn tăng rB thì dây giảm 1.” (0.873): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: trừ/∅ — NOT_VERIFIED bằng tai người',
    'Bước một, d bằng 0, xích-ma bằng 0 phẩy 5, mất mát là âm lôgarit của 0 phẩy 5, xấp xỉ 0 phẩy 693, và lực kéo là 1 trừ 0 phẩy 5, bằng 0 phẩy 5.':
        'ASR chép “Bước 1, dê bằng 0, sigma bằng 0,5, mất mát là âm logadric của 0,5, sắp xỉ 0,693 và lực kéo là 1 trừ 0,5 bằng 0,5.” (0.889): xích-ma (σ) đọc tách âm tiết, ASR viết “sigma”; “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; lệch âm/thanh thuần Việt: lôgarit/logadric, xấp/sắp, không (trong “không phẩy” → “”) — NOT_VERIFIED bằng tai người',
    'Xích-ma của 1 xấp xỉ 0 phẩy 731, mất mát xấp xỉ 0 phẩy 313, và lực kéo còn khoảng 0 phẩy 269.':
        'ASR chép “Sít ma của một sắp sĩ không phải 731, mất má sắp sĩ không phải 313 và lực kéo còn khoảng không phải 269.” (0.743): “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; lệch âm/thanh thuần Việt: xích/sít, xấp xỉ/sắp sĩ, mát xấp xỉ/má sắp sĩ — NOT_VERIFIED bằng tai người',
    'Bước ba, r A tăng thêm 0 phẩy 269 thành khoảng 0 phẩy 769, r B giảm thành khoảng âm 0 phẩy 769, nên d xấp xỉ 1 phẩy 538.':
        'ASR chép “Bước 3, R A tăng thêm 0,269 thành khoảng 0,769, R B giảm thành khoảng âm 0,769, nền dề sắp xỉ 1,538.” (0.837): “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: không (trong “không phẩy” → “”), nên xấp (trong “nên d xấp” → “nền dề sắp”) — NOT_VERIFIED bằng tai người',
    'Xích-ma xấp xỉ 0 phẩy 823, và mất mát còn khoảng 0 phẩy 195.':
        'ASR chép “Sigma sắp xỉ 0,823 và mất mát còn khoảng 0,195.” (0.78): xích-ma (σ) đọc tách âm tiết, ASR viết “sigma”; “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; lệch âm/thanh thuần Việt: xấp (trong “xích ma xấp” → “sigma sắp”), không (trong “không phẩy” → “”) — NOT_VERIFIED bằng tai người',
    'Nếu chính sách viết câu đó nhiều hơn mô hình gốc thì tỉ số lớn hơn 1, lôgarit dương, và phần thưởng bị trừ.':
        'ASR chép “Nếu chính sách viết câu đó nhiều hơn mô hình gốc thì tỷ số lớn hơn 1, lo gà trích dương và phần thưởng bị trư.” (0.84): “tỉ” ASR viết chính tả “tỷ” (cùng âm); lệch âm/thanh thuần Việt: lôgarit/lo gà trích, trừ/trư — NOT_VERIFIED bằng tai người',
    'Đáp án như bảng.':
        'ASR chép “Đáp án như bạn.” (0.75): lệch âm/thanh thuần Việt: bảng/bạn — NOT_VERIFIED bằng tai người',
    'Câu một, hiệu d bằng 1 phẩy 5, xích-ma xấp xỉ 0 phẩy 818, mất mát xấp xỉ 0 phẩy 201.':
        'ASR chép “Câu 1, hiệu dê bằng 1,5, sigma sắp xỉ 0,818, mất mát sắp xỉ 0,201.” (0.784): xích-ma (σ) đọc tách âm tiết, ASR viết “sigma”; “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; lệch âm/thanh thuần Việt: xấp (trong “xích ma xấp” → “sigma sắp”), không (trong “không phẩy” → “”), xấp/sắp — NOT_VERIFIED bằng tai người',
    'Mất mát là âm lôgarit của xác suất, với lực kéo 1 trừ xích-ma.':
        'ASR chép “mất mát là âm logo đích của xác sức với lực kéo một trừ sít ma.” (0.774): lệch âm/thanh thuần Việt: lôgarit/logo đích, suất/sức, xích/sít — NOT_VERIFIED bằng tai người',
    # ── PAR L13 dựng lại (2026-11-03) ──
    'Mỗi thẻ đồ hoạ khi ấy chỉ có 3 GB bộ nhớ, nên cả mạng không vừa trong một thẻ.':
        'ASR chép “Mỗi thẻ đồ họa khi ấy chỉ có 3GB bộ nhớ, nên cả mạng không vừa trong một thẻ.” (1.0): GB đọc “ghi-ga-byte” theo lexicon của khoá, ASR viết “GB/gigabyte” — NOT_VERIFIED bằng tai người',
    # ── Khoá mới: CVI L00 ──
    'Nếu lưu thẳng từng điểm ảnh mà không nén, một giờ chiếm khoảng 672 tỉ byte.':
        'ASR chép “Nếu lưu thẳng từng điểm ảnh mà không nén, 1 giờ chiếm khoảng 672 tỷ bay.” (0.9): “tỉ” ASR viết chính tả “tỷ” (cùng âm); byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Một ổ đĩa một nghìn tỉ byte sẽ đầy sau khoảng 89 phút.':
        'ASR chép “Một ổ đĩa 1000 tỷ bay sẽ đầy sau khoảng 89 phút.” (0.867): “tỉ” ASR viết chính tả “tỷ” (cùng âm); byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Đơn vị hai mũ hai mươi byte vì thế hơi lớn hơn một triệu byte.':
        'ASR chép “đơn vị 2 mũ 20 bay vì thế hơi lớn hơn 1 triệu bay.” (0.867): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'W là chiều rộng, tức số cột điểm ảnh, ở đây 1920.':
        'ASR chép “Về đúc là chiều động tức số Cột điểm ảnh ở đây 1.920.” (0.857): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: rộng/động — NOT_VERIFIED bằng tai người',
    'Ảnh là một lưới H hàng, mỗi hàng có W điểm ảnh, nên theo phép nhân có W nhân H điểm ảnh.':
        'ASR chép “Ảnh là một lưới hát hàng, mỗi hàng có ve đúc điểm ảnh, nên theo phép nhân có ve đúc nhân hát điểm ảnh.” (0.87): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Bước hai là đếm số, vì mỗi điểm ảnh có C số, một số cho mỗi kênh, nên cả ảnh có W nhân H nhân C số.':
        'ASR chép “Bước 2 là đếm số, vì mỗi điểm ảnh có xe số, một số cho mỗi kênh, nên cả ảnh có về đúc nhân hát nhân xe số.” (0.945): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Bước ba là đổi ra byte.':
        'ASR chép “Bước 3 là đổi ra bay.” (0.833): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Vậy dung lượng bằng W nhân H nhân C nhân b, chia cho 8, tính bằng byte.':
        'ASR chép “Vậy dung lượng bằng V đúc nhân hát nhân c nhân b, chia cho 8, tính bằng bai.” (0.857): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Làm thử, 72 nhân 8 chia 8 bằng 72 byte, nghĩa là với 8 bit mỗi kênh, số byte đúng bằng số con số.':
        'ASR chép “Làm thử 72 nhân 8 chia 8 bằng 72 bay, nghĩa là với 8 bit mỗi kênh, số bay đúng bằng số con số.” (0.929): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Bước hai, mỗi điểm ảnh có 3 kênh, mỗi kênh 1 byte, nên ta có 2 triệu 73 nghìn 600 nhân 3, bằng 6 triệu 220 nghìn 800 byte.':
        'ASR chép “Bước 2, mỗi điểm ảnh có 3 kinh, mỗi kinh 1 bay nên ta có 2 triệu 73.600 nhân ba bằng 6 triệu 220.800 bay.” (0.889): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: kênh/kinh, kênh/kinh — NOT_VERIFIED bằng tai người',
    'Bước ba, đổi ra đơn vị hai mũ hai mươi byte, ta chia cho 1 triệu 48 nghìn 576, được xấp xỉ 5 phẩy 93 đơn vị cho chỉ một khung ảnh.':
        'ASR chép “Bước 3, đổi ra đơn vị 2 mũ 20 Ba, ta chia cho 1 triệu 48.576 được sắp xỉ 5,93 đơn vị cho chỉ 1 khung ảnh.” (0.95): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: xấp/sắp — NOT_VERIFIED bằng tai người',
    'Dấu bằng lượn sóng đọc là xấp xỉ.':
        'ASR chép “Dấu bằng lượng sóng độc là sắp xỉ.” (0.625): lệch âm/thanh thuần Việt: lượn/lượng, đọc/độc, xấp/sắp — NOT_VERIFIED bằng tai người',
    'Nhân 30 được 186 triệu 624 nghìn byte, tức xấp xỉ 186 phẩy 6 triệu byte mỗi giây.':
        'ASR chép “Nhân 30 được 186,624,000 bai, tức sắp xỉ 186,6 triệu bai mỗi giây.” (0.903): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: xấp/sắp — NOT_VERIFIED bằng tai người',
    'Nhân tiếp 3600 giây được khoảng 672 tỉ byte mỗi giờ, đúng con số ở phần mở đầu.':
        'ASR chép “Nhân tiếp 3600 giây được khoảng 672 tỷ bai mỗi giờ, đúng còn số ở phần mở đầu.” (0.88): “tỉ” ASR viết chính tả “tỷ” (cùng âm); byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: con/còn — NOT_VERIFIED bằng tai người',
    'Kiểm tra thứ nhất, đếm bit thay vì byte.':
        'ASR chép “Kiểm tra thứ nhất, đếm bịt thay vì bay.” (0.778): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: bit/bịt — NOT_VERIFIED bằng tai người',
    'Chia cho 8 được đúng 6 triệu 220 nghìn 800 byte, khớp kết quả cũ.':
        'ASR chép “chia cho 8 được đúng 6.220.800 bai, khớp kết quả cũ.” (0.947): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Kiểm tra thứ hai là hỏi chính máy, tạo một mảng số nguyên 8 bit có hình dạng 1080, 1920, 3, rồi hỏi nó chiếm bao nhiêu byte.':
        'ASR chép “Kiểm tra thứ 2 là hỏi chính máy, tạo một mạng số nguyên 8 biết có hình dạng 1.080, 1.920, 3, rồi hỏi nó chiếm bao nhiêu bay.” (0.921): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: mảng/mạng, bit/biết — NOT_VERIFIED bằng tai người',
    'Máy trả lời 6 triệu 220 nghìn 800, nghĩa là khớp với phép nhân của ta, vì mỗi số 8 bit chiếm đúng một byte.':
        'ASR chép “Máy trả lời 6.220.800, nghĩa là khớp với phép nhân của ta, vì mỗi số 8 biết chiếm đúng một bay.” (0.931): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: bit/biết — NOT_VERIFIED bằng tai người',
    'Câu một, ảnh xám 640 nhân 480, 8 bit, chiếm bao nhiêu byte?':
        'ASR chép “Câu 1, ảnh xám 640 nhân 480, tảm biệt, chiếm bao nhiêu bay?” (0.842): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: tám bit/tảm biệt — NOT_VERIFIED bằng tai người',
    'Câu hai, một mạng nhận dạng ảnh nhận ảnh màu 224 nhân 224, hỏi ảnh đó bao nhiêu byte, và nhỏ hơn khung 1920 nhân 1080 bao nhiêu lần?':
        'ASR chép “Câu 2. Một mạng nhận dạng ảnh nhận ảnh màu 224 nhân 224, hỏi ảnh đó bao nhiêu bay và nhỏ hơn khu 1.920 nhân 1.080 bao nhiêu lần?” (0.957): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: khung/khu — NOT_VERIFIED bằng tai người',
    'Câu ba, camera 3840 nhân 2160, 30 khung mỗi giây, cần lưu một giờ trên ổ một nghìn tỉ byte, lưu thô được không, và bạn làm gì?':
        'ASR chép “Câu ba, camera 3.840 nhân 2.160, 30 khung mỗi giây, cần lưu 1 giờ trên ổ 1.000 tỷ bay, lưu thô được không và bạn làm gì?” (0.949): “tỉ” ASR viết chính tả “tỷ” (cùng âm); byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Câu một, ảnh xám có một kênh, nên dung lượng là 640 nhân 480 nhân 1 nhân 8 chia 8, bằng 307 nghìn 200 byte.':
        'ASR chép “Câu 1, ảnh sám có 1 kênh, nền dung lượng là 640 nhân 480 nhân 1 nhân 8 chi 8 bằng 307.200 bai.” (0.914): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: nên/nền, chia/chi — NOT_VERIFIED bằng tai người',
    'Câu hai, 224 nhân 224 nhân 3 bằng 150 nghìn 528 byte.':
        'ASR chép “Câu 2, 224 nhân 224 nhân 3 bằng 150.528 bài.” (0.963): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Câu ba, một khung là 24 triệu 883 nghìn 200 byte, nên một giờ khoảng 2 phẩy 69 nghìn tỉ byte.':
        'ASR chép “Câu Ba, 1 khung là 24,883.200 bay nên 1 giờ khoảng 2,69.000 tỷ bay.” (0.9): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); “tỉ” ASR viết chính tả “tỷ” (cùng âm) — NOT_VERIFIED bằng tai người',
    'Ổ một nghìn tỉ byte đầy sau khoảng 22 phút, nên lưu thô là không được.':
        'ASR chép “Ổ 1 nghìn tỷ bay đầy sau khoảng 22 phút nên lưu thô là không được.” (0.889): “tỉ” ASR viết chính tả “tỷ” (cùng âm); byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Tổng kết lại, ảnh là một mảng có H hàng, W cột và C kênh.':
        'ASR chép “Tổng kết lại, ảnh là một mạng có hát hàng, về đúc cột và xe kênh.” (0.839): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: mảng/mạng — NOT_VERIFIED bằng tai người',
    'Mỗi số b bit cho 2 mũ b mức, nên dung lượng bằng W nhân H nhân C nhân b chia 8.':
        'ASR chép “Mỗi số b bit cho 2 mũ b mức, nền dung lượng bằng v đút nhân hát nhân c nhân b chi 8.” (0.844): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: nên/nền, chia/chi — NOT_VERIFIED bằng tai người',
    'Một khung 1920 nhân 1080 là 6 triệu 220 nghìn 800 byte, và 30 khung mỗi giây là khoảng 186 phẩy 6 triệu byte.':
        'ASR chép “Một khung 1920 nhân 1080 là 6.220.800 bai và 30 khung mỗi giây là khoảng 186.6 triệu bai.” (0.941): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải” — NOT_VERIFIED bằng tai người',
    # ── Khoá mới: CVI L01 ──
    'Làm thử, G x bằng 30, G y bằng 40, mũi tên kép đọc là suy ra, độ lớn bằng căn của 2500, bằng 50.':
        'ASR chép “Làm thử, gx bằng 30, ge bằng 40, mũi tên kép độc là suy ra, độ lớn bằng căng của 2500 bằng 50.” (0.885): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: i (trong “g i” → “ge”), đọc/độc, căn/căng — NOT_VERIFIED bằng tai người',
    'G x bằng 30 và G y cũng bằng 30, nên theo công thức độ lớn cạnh, ta được căn của 1800, xấp xỉ 42 phẩy 4, và hướng của cạnh nghiêng đúng 45 độ.':
        'ASR chép “GX bằng 30 và GY cũng bằng 30, nên theo công thức độ lớn cạnh, ta được căn của 1800, sắp xỉ 42,4 và hướng của cạnh nghiên đúng 45 độ.” (0.92): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: i (trong “g i” → “gy”), xấp/sắp, nghiêng/nghiên — NOT_VERIFIED bằng tai người',
    'Cách sửa là đệm bằng cách lặp lại điểm ảnh ở mép, hoặc bỏ dải viền khi đo.':
        'ASR chép “Cắt sữa là đềm bằng cách lập lại điểm ảnh ở mép hoặc bỏ giải viền khi đo.” (0.778): lệch âm/thanh thuần Việt: cách sửa/cắt sữa, đệm/đềm, lặp/lập — NOT_VERIFIED bằng tai người',
    # ── Khoá mới: CVI L02 ──
    'Xích ma với chỉ số dưới W và mũ hai là phương sai trong lớp, đo mỗi lớp tự toả rộng bao nhiêu, cộng theo tỉ lệ w.':
        'ASR chép “SITMA với chỉ số dưới V đúc và mũ 2 là phương sai trong lớp, đo mỗi lớp tự tỏa động bao nhiêu, cộng theo tỷ lệ V kép.” (0.828): xích-ma (σ) đọc tách âm tiết, ASR viết “sigma”; chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; “tỉ” ASR viết chính tả “tỷ” (cùng âm); lệch âm/thanh thuần Việt: rộng/động — NOT_VERIFIED bằng tai người',
    'Hai chỉ số B và W lấy từ chữ đầu của hai từ tiếng Anh nghĩa là giữa và trong.':
        'ASR chép “Hai chỉ số B và V đút, lấy từ chữ đầu của hai từ tiếng Anh nghĩa là giữa và trong.” (0.927): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    # ── Khoá mới: CVI L03 ──
    'Điểm 0 phẩy 5, 0 phẩy 25, 2 mét với f bằng 800 và c x bằng 320 cho u bằng 800 nhân 0 phẩy 25 cộng 320, bằng 520.':
        'ASR chép “Điểm 0,5, 0,25, 2m với x bằng 800 và Cx bằng 320 cho u bằng 800 nhân 0,25 cộng 320 bằng 520.” (0.956): đơn vị mét, ASR viết ký hiệu “m”; chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'c x và c y là tâm ảnh, nơi trục nhìn thẳng chạm mặt ảnh, ở đây là 320, 240.':
        'ASR chép “CX và CE là tâm ảnh nơi trục nhìn thẳng chạm mặt ảnh. Ở đây là 320, 240.” (0.941): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: i (trong “c i” → “ce”) — NOT_VERIFIED bằng tai người',
    'Tiêu cự tính bằng điểm ảnh vì ống kính 4 mi-li-mét chia cho bề rộng 0 phẩy 005 mi-li-mét của mỗi điểm cảm biến, bằng 800.':
        'ASR chép “Tiêu cử tính bằng điểm ảnh vì ống kính 4 mm chia cho bề rộng 0,005 mm của mỗi điểm cảm biến bằng 800.” (0.786): đơn vị mi-li-mét, ASR viết ký hiệu “mm”; “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; lệch âm/thanh thuần Việt: cự/cử, không (trong “không phẩy” → “”) — NOT_VERIFIED bằng tai người',
    'Nửa ảnh rộng W chia 2 điểm ảnh và cách lỗ kim f x điểm ảnh, nên theo định nghĩa tang, tang của nửa góc nhìn bằng 320 chia 800, bằng 0 phẩy 4.':
        'ASR chép “Nửa ảnh rộng về đúc chia 2 điểm ảnh và cách lỗ kim fx điểm ảnh nên theo định nhễ tan, tan của nửa gốc nhìn bằng 320 chia 800, bằng 0,4.” (0.857): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: nghĩa tang tang/nhễ tan tan, góc/gốc — NOT_VERIFIED bằng tai người',
    # ── Khoá mới: CVI L04 ──
    'Điểm p có một láng giềng rất gần là b một, và láng giềng thứ hai xa hơn hẳn.':
        'ASR chép “Điểm T có một láng giềng rất gần là B1 và láng giềng thứ hai xa hơn hẳn.” (0.947): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    # ── Khoá mới: CVI L05 ──
    'w là tỉ lệ dữ liệu đúng, gọi là điểm trong, ví dụ 6 trên 8 điểm là 0 phẩy 75.':
        'ASR chép “V kết là tỷ lệ dữ liệu đúng, gọi là điểm trong, ví dụ 6 trên 8 điểm là 0,75.” (0.917): chữ w đọc “vê kép” (luật chung), ASR viết tách chữ; “tỉ” ASR viết chính tả “tỷ” (cùng âm) — NOT_VERIFIED bằng tai người',
    'Lấy lôgarit hai vế và đưa N xuống thành phép nhân, ta được N nhân lôgarit của 1 trừ w mũ s, nhỏ hơn hoặc bằng lôgarit của 1 trừ p.':
        'ASR chép “Lấy log 2v và đưa n xuống thành phép nhân, ta được n nhân log 1 trừ vk mũ x, nhỏ hơn hoặc bằng log 1 trừ P.” (0.8): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: lôgarit/log, vế/v, lôgarit của/log, lôgarit của/log — NOT_VERIFIED bằng tai người',
    'Bước một, với w bằng 0 phẩy 5, bốn điểm mỗi mẫu và độ chắc 0 phẩy 99, như vừa suy ra, cần 72 lần.':
        'ASR chép “Bước 1, với VK bằng 0,5, 4 điểm mỗi mẫu và độ chắc 0,99 như vừa suy ra cần 72 lần.” (0.966): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Vì w nằm ở số mũ, nên lọc đầu vào rẻ hơn thử thêm rất nhiều.':
        'ASR chép “Vì v-cap nằm ở số mũ nên lọc đầu vào rẽ hơn thử thêm rất nhiều.” (0.882): chữ w đọc “vê kép” (luật chung), ASR viết tách chữ; lệch âm/thanh thuần Việt: rẻ/rẽ — NOT_VERIFIED bằng tai người',
    'Một lần bốc thành công với xác suất w mũ s, từ đó N bằng lôgarit của 1 trừ p chia lôgarit của 1 trừ w mũ s, làm tròn lên.':
        'ASR chép “Một lần bốc thành công với sát suốt V kép mũ S, từ đó n bằng logatric của 1 trừ P chia logatric của 1 trừ V kép mũ S, làm tròn lên.” (0.879): lệch âm/thanh thuần Việt: xác suất/sát suốt, lôgarit/logatric, lôgarit/logatric — NOT_VERIFIED bằng tai người',
    # ── Khoá mới: CVI L06 ──
    'Chi phí của d là tổng trị tuyệt đối chênh lệch giữa cửa sổ ở ảnh trái và cửa sổ dời d cột ở ảnh phải, bằng 0 khi khớp hoàn hảo.':
        'ASR chép “Chi phí của dê là tổng trị tuyệt đối trên lệch giữa cửa sổ, ảnh trái và cửa sổ dời dây cột ở ảnh phải bằng không khi khấp hoàn hảo.” (0.889): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: chênh/trên, ở/∅, khớp/khấp — NOT_VERIFIED bằng tai người',
    'Đó là một cực tiểu rõ rệt, vì mọi d khác đều có chi phí từ 120 trở lên.':
        'ASR chép “Đó là một cực tiểu rõ rệt vì mọi giây khác đều có chi phí từ 120 trở lên.” (0.955): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Rút gọn, sai lệch độ sâu xấp xỉ Z bình phương nhân sai lệch của d, chia cho f nhân B.':
        'ASR chép “Rút gọn, sai lệch độ sâu sấp xỉ giác bình phương nhân sai lệch của V, chia cho F nhân B.” (0.952): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    # ── Khoá mới: CVI L07 ──
    'Tiếp theo là lớp gộp 3 nhân 3 bước 2, lúc này j bằng 2, nên r bằng 7 cộng 2 nhân 2, bằng 11.':
        'ASR chép “Tiếp theo là lớp gột 3 nhân 3 bước 2, lúc này dì bằng 2, nền R bằng 7 cộng 2 nhân 2, bằng 11.” (0.885): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: gộp/gột, nên/nền — NOT_VERIFIED bằng tai người',
    'Rồi một lớp 3 nhân 3, j đã là 4, nên r bằng 11 cộng 2 nhân 4, bằng 19.':
        'ASR chép “Rồi một lớp 3 nhân 3, vi đã là 4, nền R bằng 11 cộng 2 nhân 4, bằng 19.” (0.909): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: nên/nền — NOT_VERIFIED bằng tai người',
    'Ta cho một hàng 15 điểm ảnh toàn 0, bật một điểm thành 1, chạy qua ba lớp 3 nhân 3 với mọi trọng số bằng 1, rồi xem ô ra số 4 có khác 0 không.':
        'ASR chép “Ta cho 1 hàng 15 điểm ảnh toàn không, bật 1 điểm thành 1, chạy qua 3 lớp 3 nhân 3 với mọi trọng số bằng 1, rồi xem ODA số 4 có khác không không.” (0.96): “ô” (ô lưới) ASR viết chữ “O”; lệch âm/thanh thuần Việt: ra (trong “ô ra” → “oda”) — NOT_VERIFIED bằng tai người',
    # ── Khoá mới: CVI L08 ──
    'Bên phải, C và D lệch nhau một điểm ảnh, giao bằng 90, hợp bằng 110.':
        'ASR chép “Bên phải, xe và dây lệch nhau một điểm ảnh, giao bằng 90, hợp bằng 110.” (0.947): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Số ô nằm trong cả A lẫn B là 25, số ô nằm trong ít nhất một hộp là 175, khớp tỉ số 25 phần 175 mà không cần công thức.':
        'ASR chép “Số O nằm trong cả A lẫn B là 25, số O nằm trong ít nhất một hộp là 175, khớp tỷ số 25 phần 175 mà không cần công thức.” (0.93): “ô” (ô lưới) ASR viết chữ “O”; “tỉ” ASR viết chính tả “tỷ” (cùng âm) — NOT_VERIFIED bằng tai người',
    'Bảng quét mười ngưỡng.':
        'ASR chép “Bản quét 10 ngưỡng.” (0.75): lệch âm/thanh thuần Việt: bảng/bản — NOT_VERIFIED bằng tai người',
    'Ghép theo điểm cho dãy đúng sai, rồi diện tích dưới đường độ chuẩn xác theo độ phủ là độ chính xác trung bình.':
        'ASR chép “Gép theo điểm cho dạy đúng sai, rồi diện tích dưới đường đồ chuẩn xác theo đồ phủ là đồ chính xác trung bình.” (0.792): lệch âm/thanh thuần Việt: ghép/gép, dãy/dạy, độ/đồ, độ/đồ, độ/đồ — NOT_VERIFIED bằng tai người',
    # ── Khoá mới: CVI L09 ──
    'Loại cuối là nền được giữ đúng là nền.':
        'ASR chép “Loại cuối là nên được giữ đúng là nên.” (0.778): lệch âm/thanh thuần Việt: nền/nên, nền/nên — NOT_VERIFIED bằng tai người',
    'Thay số, 0 phẩy 9 chia 1 phẩy 1, xấp xỉ 0 phẩy 818.':
        'ASR chép “Thay số 0,9 × 1,1 xếp sĩ 0,818.” (0.774): “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; lệch âm/thanh thuần Việt: chia/∅, xấp xỉ không (trong “xấp xỉ không phẩy” → “xếp sĩ”) — NOT_VERIFIED bằng tai người',
    'Giao trên hợp của lớp vết nứt gộp cả tập không bị nền lấn át, nhưng vết dài và to sẽ lấn át vết mảnh.':
        'ASR chép “Giao trên hộp của lớp vết nước gột cả tập không bị nền lấn ác, nhưng vết dài và to sẽ lấn ác vết mảnh.” (0.68): lệch âm/thanh thuần Việt: hợp/hộp, vết nứt gộp/véc nước gột, át/ác, vết/véc, át vết/ác véc — NOT_VERIFIED bằng tai người',
    # ── Khoá mới: CVI L10 ──
    'Điều thứ nhất là trung bình có trọng số, như ở bài 2 ta nhân mỗi lớp với tỉ lệ w của nó.':
        'ASR chép “Điều thứ nhất là trung bình có trọng số, như ở bài hai ta nhân mỗi lớp với tỷ lệ v kết của nó.” (0.917): “tỉ” ASR viết chính tả “tỷ” (cùng âm); chữ w đọc “vê kép” (luật chung), ASR viết tách chữ — NOT_VERIFIED bằng tai người',
    'Điều thứ ba là tăng bao nhiêu phần trăm, từ a lên b thì tăng b trừ a chia a.':
        'ASR chép “Điều thứ 3 là tăng bao nhiêu phần trăm, từ A lên B thì tăng B trữ A chia.” (0.923): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: trừ/trữ — NOT_VERIFIED bằng tai người',
    # ── Khoá mới: CVI L11 ──
    'Theo bảng bốn ô, trên tập thử cùng phân bố, A đúng 950 trên 1000 ảnh, tức 95 phần trăm.':
        'ASR chép “Theo bản 4 ô, trên tập thử cùng phân bố, à đúng 950 trên 1 nghìn ảnh, tức 95%” (0.923): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: bảng/bản — NOT_VERIFIED bằng tai người',
    'Ảnh huấn luyện chụp ở 3 bãi đỗ xe.':
        'ASR chép “Ảnh huấn liền chục ở 3 bãi đổ xe” (0.667): lệch âm/thanh thuần Việt: luyện chụp/liền chục, đỗ/đổ — NOT_VERIFIED bằng tai người',
    # ── Khoá mới: CVI L12 ──
    'Chào bạn, năm 2010, đội thắng cuộc thi nhận dạng ảnh ImageNet sai 28 phẩy 2 phần trăm theo cách tính năm đáp án.':
        'ASR chép “Chào bạn, năm 2010, đội thắng cuộc thi nhận dạng ảnh E-MIC NextSci 28,2% theo cách tính 5 đáp án.” (0.918): lệch âm/thanh thuần Việt: imagenet sai/e mic nextsci — NOT_VERIFIED bằng tai người',
    'Bảng tính lại.':
        'ASR chép “Bạn tính lại.” (0.667): lệch âm/thanh thuần Việt: bảng/bạn — NOT_VERIFIED bằng tai người',
    'Thực hành rút ra là trước khi chọn cách sửa, hãy nhìn lỗi huấn luyện.':
        'ASR chép “Thực hành trúc tra là trước khi chọn các sữa, hãy nhìn lỗi huấn luyện.” (0.733): lệch âm/thanh thuần Việt: rút ra/trúc tra, cách sửa/các sữa — NOT_VERIFIED bằng tai người',
    'Nhóm tác giả ghi rằng học từ đầu trên tập cỡ vừa như ImageNet mà không chính quy hoá mạnh, nó kém mạng có lối tắt cùng cỡ vài điểm phần trăm.':
        'ASR chép “Nhóm tác giả ghi rằng học từ đầu trên tập cỡ vừa như im miệt nét mà không chính quy hóa mạnh, nó kém mạng có lối tắt cùng cỡ vài điểm phần trăm.” (0.941): lệch âm/thanh thuần Việt: i mịt/im miệt — NOT_VERIFIED bằng tai người',
    # ── Khoá mới: IRS L00 ──
    'Ký hiệu y i, với i nhỏ dưới chân, là mức liên quan ở vị trí i, bằng 1 nếu đúng và 0 nếu sai, như hệ A có y 1 bằng 1, y 2 bằng 0.':
        'ASR chép “Ký hiệu y, với y nhỏ dưới chân, là mức liên quan ở vị trí y, bằng một nếu đúng và không nếu sai, như hệ A có y một bằng một, y hai bằng không.” (0.986): lệch âm/thanh thuần Việt: i/∅ — NOT_VERIFIED bằng tai người',
    'Hình cho thấy cơ chế, mười ô là mười kết quả của hệ A, ô xanh có dấu tích là kết quả đúng.':
        'ASR chép “Hình cho thấy cơ chế, 10O là 10 kết quả của hệ A, O xanh có dấu tích là kết quả đúng.” (0.913): “ô” (ô lưới) ASR viết chữ “O” — NOT_VERIFIED bằng tai người',
    'Bước một là đếm, mỗi kết quả đúng góp 1 và kết quả sai góp 0, nên số kết quả đúng trong k dòng đầu bằng tổng các y i.':
        'ASR chép “Bước 1 là đếm mỗi kết quả đúng góp 1 và kết quả sai góp 0, nên số kết quả đúng trong ca dòng đầu bằng tổng cắt EIE.” (0.915): lệch âm/thanh thuần Việt: các i i/cắt eie — NOT_VERIFIED bằng tai người',
    # ── Khoá mới: IRS L01 ──
    'Điều thứ nhất, ở bài 0 ta đếm kết quả đúng trong k dòng đầu bằng tổng các y i, mỗi y i là 0 hoặc 1.':
        'ASR chép “Điều thứ nhất, ở bài không ta đếm kết quả đúng trong ca vòng đầu bằng tổng cắt y, mỗi y là 0 hoặc 1.” (0.885): lệch âm/thanh thuần Việt: dòng/vòng, các i/cắt, i/∅ — NOT_VERIFIED bằng tai người',
    'Hôm nay y i được phép là 0, 1, 2 hoặc 3, tức mức liên quan nhiều bậc.':
        'ASR chép “Hôm nay, khi được phép là 0, 1, 2 hoặc 3 tức mức liên quan nhiều bật.” (0.857): lệch âm/thanh thuần Việt: i i/khi, bậc/bật — NOT_VERIFIED bằng tai người',
    'Bảng giải mã từng ký hiệu, y i là mức liên quan ở vị trí i, từ 0 là không liên quan tới 3 là rất liên quan.':
        'ASR chép “Bản giải mã từng ký hiệu là mức liên quan ở vị trí Y, từ 0 là không liên quan tới 3 là rất liên quan.” (0.926): lệch âm/thanh thuần Việt: bảng/bản, i i/∅ — NOT_VERIFIED bằng tai người',
    'Ba chữ D C G, a còng, k là độ lợi tích lũy có chiết khấu, tức tổng các y i đã nhân chiết khấu ở k dòng đầu.':
        'ASR chép “Ba chữ dcd, a còng, ca là độ lợi tích lụy có chiếc khấu, tức tổng các y đã nhân chiếc khấu ở ca vòng đầu.” (0.764): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: luỹ/luỵ, chiết/chiếc, i/∅, chiết/chiếc, dòng/vòng — NOT_VERIFIED bằng tai người',
    'Thêm chữ n nhỏ ở đầu là bản chuẩn hoá, bằng D C G chia cho bản lý tưởng, nên luôn nằm từ 0 đến 1.':
        'ASR chép “Thêm chữ n nhỏ ở đầu là bản chuẩn hóa, bằng gcg chia cho bản lý tưởng nên luôn nằm từ 0 đến 1.” (0.92): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Hai vị trí đầu giống hệ X, còn mức 1 bây giờ ở vị trí 3, chia lôgarit cơ số 2 của 4 bằng 2, nên được 0 phẩy 5.':
        'ASR chép “Hai vị trí đầu giống hệ ít còn mức một bây giờ ở vị trí 3 chia logatic cơ số 2 của 4 bằng 2 nên được 0,5.” (0.967): lệch âm/thanh thuần Việt: lôgarit/logatic — NOT_VERIFIED bằng tai người',
    'Hệ bỏ sót văn bản tốt mà điểm vẫn gần 1.':
        'ASR chép “Hãy bỏ sóc văn bản tốt mà điểm vẫn gần mục.” (0.727): lệch âm/thanh thuần Việt: hệ/hãy, sót/sóc, một/mục — NOT_VERIFIED bằng tai người',
    'Rồi ta xếp hạng văn bản bằng cosin của góc giữa hai vector.':
        'ASR chép “Rồi ta xếp hạng văn bản bằng cosine của góc giữa hai vector.” (0.923): lệch âm/thanh thuần Việt: cosin/cosine — NOT_VERIFIED bằng tai người',
    # ── Khoá mới: IRS L02 ──
    'Một hệ đơn giản chỉ đếm từ rồi so bằng cosin, và d1 được tới 0 phẩy 632, chỉ vì có chữ máy hai lần dù d1 nói về ổ cứng.':
        'ASR chép “Một hệ đơn giản chỉ đếm từ rồi so bằng cosine và dê một được tới 0,632 chỉ vì có chữ mấy hai lần dù dê một nói về ổ cứng.” (0.917): “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; lệch âm/thanh thuần Việt: cosin/cosine, không (trong “không phẩy” → “”), máy/mấy — NOT_VERIFIED bằng tai người',
    'Cosin của hai vector bằng tích vô hướng chia tích hai độ dài, chỉ phụ thuộc hướng.':
        'ASR chép “Cô xin của hai vector bằng tích vô hướng chia tích 2 độ dài chỉ phụ thuộc hướng.” (0.914): lệch âm/thanh thuần Việt: cosin/cô xin — NOT_VERIFIED bằng tai người',
    'Ba chữ i d f là độ hiếm, bằng lôgarit của N chia d f, từ càng ít văn bản có thì độ hiếm càng lớn.':
        'ASR chép “Ba chữ Y,Y,F là độ hiếm bằng logarith của N,Y,Y,F từ càng ít văn bản có thì độ hiếm càng lớn.” (0.885): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: chia (trong “chia d” → “i i”) — NOT_VERIFIED bằng tai người',
    'Văn bản d3 có thêm từ màn, nên mũi tên nghiêng lên, lệch khoảng 70 độ so với câu hỏi.':
        'ASR chép “Văn bản G3 có thêm từ màn nên mũi tên nghiên lên là khoảng 70 độ so với câu hỏi.” (0.864): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: nghiêng/nghiên, lệch/là — NOT_VERIFIED bằng tai người',
    'Vì vậy ta cần một số bằng 0 khi d f bằng N và lớn dần khi từ hiếm đi, và lôgarit của tỉ số N chia d f làm đúng việc đó.':
        'ASR chép “Vì vậy ta cần một số bằng 0 khi gf bằng n và lớn dần khi từ hiếm đi và logarith của tỷ số n gf làm đúng việc đó.” (0.857): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; “tỉ” ASR viết chính tả “tỷ” (cùng âm); lệch âm/thanh thuần Việt: chia (trong “chia d f” → “gf”) — NOT_VERIFIED bằng tai người',
    'Bước bốn là điểm, văn bản hợp câu hỏi khi hai mũi tên cùng hướng, nên điểm là cosin của góc giữa vector câu hỏi q và vector văn bản d.':
        'ASR chép “Bước 4 là điểm, văn bản hợp câu hỏi khi hai mũi tên cùng hướng, nên điểm là cô sinh của gốc giữa vét tơ câu hỏi quy và vét tơ văn bản d.” (0.925): lệch âm/thanh thuần Việt: cosin/cô sinh, góc/gốc — NOT_VERIFIED bằng tai người',
    'Văn bản d3 thành 0, 0, 0 phẩy 405, 1 phẩy 099.':
        'ASR chép “Văn bản G3 thành 0, 0, 0,405, 1,099.” (0.778): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; lệch âm/thanh thuần Việt: không (trong “không phẩy” → “”) — NOT_VERIFIED bằng tai người',
    'Tích vô hướng của q và d3 chỉ có một cặp khác 0, là 0 phẩy 405 nhân 0 phẩy 405, khoảng 0 phẩy 164.':
        'ASR chép “Tích vô hướng của Quy và G3 chỉ có một cặp khác không là 0,405 nhân 0,405, khoảng 0,164.” (0.879): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; lệch âm/thanh thuần Việt: không (trong “không phẩy” → “”), không (trong “không phẩy” → “”), không (trong “không phẩy” → “”) — NOT_VERIFIED bằng tai người',
    'Chia cho 0 phẩy 405 nhân 1 phẩy 171 được cosin khoảng 0 phẩy 346.':
        'ASR chép “chia cho 0,405 nhân 1,171 được cô sinh khoảng 0,346.” (0.816): “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; lệch âm/thanh thuần Việt: không (trong “không phẩy” → “”), cosin/cô sinh, không (trong “không phẩy” → “”) — NOT_VERIFIED bằng tai người',
    'Bước bốn, với d2, tích vô hướng cũng là 0 phẩy 164, chia cho 0 phẩy 405 nhân 0 phẩy 405 được đúng 1, còn với d1, tích vô hướng bằng 0 nên cosin bằng 0.':
        'ASR chép “Bước 4, với G2, tích vô hướng cũng là 0.164, chia cho 0.405 nhân 0.405 được đúng 1, còn với G1, tích vô hướng bằng không nên cô xin bằng không.” (0.857): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; lệch âm/thanh thuần Việt: không (trong “không phẩy” → “”), không (trong “không phẩy” → “”), không (trong “không phẩy” → “”), cosin/cô xin — NOT_VERIFIED bằng tai người',
    'Phép thử thứ nhất là ghép d1 với chính nó, thành máy ổ máy máy ổ máy.':
        'ASR chép “Phép thử thứ nhất là ghép G1 với chính nó thành mấy ổ mấy mấy ổ mấy.” (0.722): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: máy/mấy, máy máy/mấy mấy, máy/mấy — NOT_VERIFIED bằng tai người',
    'Với câu hỏi máy ổ, d1 có tích vô hướng 1 phẩy 207 và cosin bằng 1.':
        'ASR chép “Với câu hỏi máy ổ, G1 có tích vô hướng 1,207 và coosin bằng 1.” (0.857): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; lệch âm/thanh thuần Việt: cosin/coosin — NOT_VERIFIED bằng tai người',
    'Bản ghép đôi có tích vô hướng gấp đôi, 2 phẩy 414, nhưng cosin vẫn bằng 1, vì tử và mẫu cùng gấp đôi.':
        'ASR chép “Bản kép đôi có tích vô hướng gấp đôi 2,414, nhưng cô sinh vẫn bằng một vì tử và mẫu cùng gấp đôi.” (0.873): “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; lệch âm/thanh thuần Việt: ghép/kép, cosin/cô sinh — NOT_VERIFIED bằng tai người',
    'Phép thử thứ hai đi đường khác, ta bỏ độ hiếm, chỉ dùng vector đếm rồi tính cosin.':
        'ASR chép “Phép thử thứ 2 đi đường khác, ta bỏ độ hiếm, chỉ dùng vector đếm rồi tính cosine.” (0.944): lệch âm/thanh thuần Việt: cosin/cosine — NOT_VERIFIED bằng tai người',
    'Văn bản d2 vẫn được 1 dù tính cách nào.':
        'ASR chép “Văn bản G2 vẫn được một dù tính cách nào?” (0.909): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Văn bản d3 được 0 phẩy 816 khi đếm thô, so với 0 phẩy 346, vì vậy độ hiếm chính là thứ đẩy trang ổ cứng xuống.':
        'ASR chép “Văn bản G3 được 0,816 khi đếm thô so với 0,346, vì vậy độ hiếm chính là thứ đậy trang ổ cứng xuống.” (0.879): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; lệch âm/thanh thuần Việt: không (trong “không phẩy” → “”), không (trong “không phẩy” → “”), đẩy/đậy — NOT_VERIFIED bằng tai người',
    'Lỗi thứ tư cũng của người đã đi làm, là tin rằng cosin chống được nhồi từ khoá.':
        'ASR chép “Lỗi thứ tư cũng của người đã đi làm là tin rằng cô xin chống được nhồi từ khóa.” (0.919): lệch âm/thanh thuần Việt: cosin/cô xin — NOT_VERIFIED bằng tai người',
    'Văn bản pin pin pin pin pin được cosin bằng 1 với câu hỏi pin, hơn hẳn văn bản d3 thật chỉ được 0 phẩy 346.':
        'ASR chép “Văn bản PIN PIN PIN PIN PIN được cố xin bằng một với câu hỏi PIN, hơn hãng văn bản dê ba thật chỉ được 0,346.” (0.885): “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; lệch âm/thanh thuần Việt: cosin/cố xin, hẳn/hãng, không (trong “không phẩy” → “”) — NOT_VERIFIED bằng tai người',
    'Cosin chỉ chống văn bản dài lặp lại chính nó, còn văn bản chỉ gồm từ khoá thì trùng hướng câu hỏi.':
        'ASR chép “Cô xin chỉ chống văn bản dài lập lại chính nó, còn văn bản chỉ gồm từ khóa thì trùng hướng câu hỏi.” (0.889): lệch âm/thanh thuần Việt: cosin/cô xin, lặp/lập — NOT_VERIFIED bằng tai người',
    'Câu hai, tính cosin với d2 và d3, rồi xếp hạng.':
        'ASR chép “Câu 2, tính cô sinh với dê 2 và dê 3, rồi xếp hạng.” (0.889): lệch âm/thanh thuần Việt: cosin/cô sinh — NOT_VERIFIED bằng tai người',
    'Câu hai, vì d3 cùng vector với q nên cosin bằng 1 và d3 đứng đầu.':
        'ASR chép “Câu 2, vì dê 3 cùng vét tơ với quy nên cô xin bằng 1 và dê 3 đứng đầu.” (0.923): lệch âm/thanh thuần Việt: cosin/cô xin — NOT_VERIFIED bằng tai người',
    'Ví dụ d3 thành khoảng 0, 0, 0 phẩy 346, 0 phẩy 938, và tổng bình phương xấp xỉ 1.':
        'ASR chép “Ví dụ G3 thành khoảng 0, 0, 0.346, 0.938 và tổng bình phương sắp xỉ 1.” (0.852): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; lệch âm/thanh thuần Việt: không (trong “không phẩy” → “”), không (trong “không phẩy” → “”), xấp/sắp — NOT_VERIFIED bằng tai người',
    'Khi đó cosin chính là tích vô hướng, chỉ cần nhân từng cặp rồi cộng, rẻ hơn hẳn.':
        'ASR chép “Khi đó cô xin chính là tích vô hướng, chỉ cần nhân từng cặp rồi cộng rẻ hơn hẳn.” (0.919): lệch âm/thanh thuần Việt: cosin/cô xin — NOT_VERIFIED bằng tai người',
    'Sau đó xếp trọng số thành vector cho cả văn bản và câu hỏi, rồi xếp hạng bằng cosin của góc giữa hai vector.':
        'ASR chép “Sau đó xếp trọng số thành vector cho cả văn bản và câu hỏi, rồi xếp hạng bằng cosine của góc giữa hai vector.” (0.958): lệch âm/thanh thuần Việt: cosin/cosine — NOT_VERIFIED bằng tai người',
    # ── Khoá mới: IRS L03 ──
    'Ví dụ cụm gồm bốn điểm trong ngoặc móc nhọn, mũi tên kép nghĩa là suy ra tâm của cụm.':
        'ASR chép “Ví dụ cùng gồm 4 điểm trong hoặc mất nhọn, mũi tình kép nghĩa là suy ra tâm của cùng.” (0.75): lệch âm/thanh thuần Việt: cụm/cùng, ngoặc móc/hoặc mất, tên/tình, cụm/cùng — NOT_VERIFIED bằng tai người',
    'Vì vậy với m bằng 1, độ phủ ở 1 láng giềng là 0 chia 1, bằng 0, ta đã sót.':
        'ASR chép “Vì vậy với em mờ bằng một, độ phủ ở một láng giềng là không chi một, bằng không, ta đã sót.” (0.884): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: chia/chi — NOT_VERIFIED bằng tai người',
    'Bảng cho bốn điểm của cụm B, điểm ở mép trái chỉ cách q 0 phẩy 25, gần hơn mọi điểm của cụm A.':
        'ASR chép “Bảng cho 4 điểm của cục b, điểm ở mép trái chỉ cách quy 0,25, gần hơn mọi điểm của cục ma.” (0.885): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: cụm/cục, cụm (trong “cụm a” → “cục ma”) — NOT_VERIFIED bằng tai người',
    'Tổng kết lại, truy hồi dày dùng vector nhúng dày đặc, so hết thì tốn n phép so.':
        'ASR chép “Tổng kết lại, truy hồi dây dùng vét tơ nhúng dày đặt, so hết thịt tún nở Phép so.” (0.737): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: dày/dây, đặc/đặt, thì tốn (trong “thì tốn n” → “thịt tún nở”) — NOT_VERIFIED bằng tai người',
    # ── Khoá mới: IRS L04 ──
    'Hệ theo vector xếp B đầu với cosin 0 phẩy 83, rồi E, A, C, thang điểm từ 0 tới 1.':
        'ASR chép “Hệ theo vector set B đầu với cô sinh 0,83, rồi E, A, C thang điểm từ 0 tới 1.” (0.894): lệch âm/thanh thuần Việt: xếp/set, cosin/cô sinh — NOT_VERIFIED bằng tai người',
    'Ở bài 2 và bài 3, điểm theo vector là cosin của góc giữa hai vector, luôn từ 0 tới 1, ví dụ 0 phẩy 956.':
        'ASR chép “Ở bài 2 và bài 3, điểm theo vector là cosine của góc giữa 2 vector, luôn từ 0 tới 1, ví dụ 0,956.” (0.931): “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; lệch âm/thanh thuần Việt: cosin/cosine, không (trong “không phẩy” → “”) — NOT_VERIFIED bằng tai người',
    'Bảng giải mã từng ký hiệu, r j của d là hạng của văn bản d trong danh sách thứ j, như A hạng 1 ở danh sách từ khoá và hạng 3 ở danh sách vector.':
        'ASR chép “Bản giải mã từng ký hiệu RY của G là hạng của văn bản G trong danh sách thứ G, như A hạng 1 ở danh sách từ khóa và hạng 3 ở danh sách vector.” (0.849): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: bảng/bản — NOT_VERIFIED bằng tai người',
    'Văn bản E và D chỉ có mặt ở một danh sách, nên chỉ có một lá phiếu và xuống cuối.':
        'ASR chép “Văn bản E và G chỉ có mặt ở một danh sách, nên chỉ có một lá phiếu và xuống cuối.” (0.952): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Ta cộng thêm hằng số k vào mẫu số, và điểm của văn bản d là tổng theo mọi danh sách j của 1 chia k cộng r j của d.':
        'ASR chép “Ta cộng thêm hàng số ca vào mẫu số, và điểm của văn bản dê là tổng theo mọi danh sách dê của một chia ca cộng rj của dê.” (0.935): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: hằng/hàng — NOT_VERIFIED bằng tai người',
    'Điểm của nó là 1 chia 62 cộng 1 chia 61, khoảng 0 phẩy 016129 cộng 0 phẩy 016393, bằng chừng 0 phẩy 03252, lớn hơn A.':
        'ASR chép “Điểm của nó là 1 chia 62 cộng 1 chia 61, khoảng 0.016129 cộng 0.016393 bằng chừng 0.03252, lớn hơn nha.” (0.949): “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Thang từ khoá lớn gấp hàng chục lần thang cosin, nên tổng gần như chỉ là điểm từ khoá, và danh sách vector bị bỏ qua.':
        'ASR chép “Thang từ khóa lớn gấp hàng chục lần thang cosine, nền tổng gần như chỉ là điểm từ khóa và danh sách vector bị bỏ qua.” (0.923): lệch âm/thanh thuần Việt: cosin nên/cosine nền — NOT_VERIFIED bằng tai người',
    'Lỗi thứ hai là bỏ hằng số làm dịu, dùng 1 chia r.':
        'ASR chép “Lỗi thứ 2 là bỏ hàng số làm dịu dùng một chia error.” (0.846): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: hằng/hàng — NOT_VERIFIED bằng tai người',
    'Hệ vector xếp R, S, Q với cosin 0 phẩy 9, 0 phẩy 85 và 0 phẩy 8.':
        'ASR chép “Hệ vét tơ xếp r, x, quỳ với cô sinh 0,9, 0,85 và 0,8.” (0.884): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: cosin/cô sinh — NOT_VERIFIED bằng tai người',
    # ── Khoá mới: IRS L05 ──
    'Bước bốn, đọc hình dáng bằng cách thay vài giá trị của o.':
        'ASR chép “Bước bốn, đọc hình dáng bằng cách thay vài giá trị của.” (0.96): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    # ── Khoá mới: IRS L06 ──
    'Người W chấm 1, 2 và 5.':
        'ASR chép “Người với đúc .1, 2 và 5” (0.714): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: chấm (trong “w chấm” → “với đúc”) — NOT_VERIFIED bằng tai người',
    'Cosin là tích vô hướng chia tích hai độ dài, ở đây 11 chia căn 5 nhân 5, khoảng 0 phẩy 984.':
        'ASR chép “Cô Xin là tích vô hướng chia tích 2 độ dài. Ở đây 11 chia căng 5 nhân năm, khoảng không phải 984.” (0.873): “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; lệch âm/thanh thuần Việt: cosin/cô xin, căn/căng — NOT_VERIFIED bằng tai người',
    'Bài 2 đã dùng chính số này để xếp văn bản theo câu hỏi, cosin càng gần 1 thì hai vector càng cùng hướng.':
        'ASR chép “Bài 2 đã dùng chính số này để xếp văn bản theo câu hỏi, cô xin càng gần 1 thì 2 vét tơ càng cùng hướng.” (0.941): lệch âm/thanh thuần Việt: cosin/cô xin — NOT_VERIFIED bằng tai người',
    'Bảng giải mã ký hiệu, chữ u in đậm là vector hàng điểm của người U, bằng 5, 3, 0, tương tự với v và w.':
        'ASR chép “Bản giải mã ký hiệu, chữ u in đậm là vector hàng điểm của người u bằng 5, 3, 0, tương tự với v và v két.” (0.906): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: bảng/bản — NOT_VERIFIED bằng tai người',
    'Còn cosin của u và v là độ tương tự giữa hai người, nằm từ 0 tới 1 khi mọi điểm không âm.':
        'ASR chép “Còn cosine của U và V là độ tương tự giữa hai người, nằm từ không tới một khi mọi điểm không âm.” (0.957): lệch âm/thanh thuần Việt: cosin/cosine — NOT_VERIFIED bằng tai người',
    'Hình cho thấy cơ chế, U ở bên trái chưa chấm ốp lưng, còn hai láng giềng V và W đã chấm.':
        'ASR chép “Hình cho thấy cơ chế, u ở bên trái chưa chấm óc lưng, còn hai láng dìn V và V đúc đã chấm.” (0.844): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: ốp/óc, giềng/dìn — NOT_VERIFIED bằng tai người',
    'Đường nối dày màu lục nghĩa là U giống V nhiều, độ tương tự 0 phẩy 606, đường mảnh màu xám nghĩa là U giống W ít, chỉ 0 phẩy 344.':
        'ASR chép “Đường nối dày màu lục nghĩa là U giống V nhiều, độ tương tự 0,606, đường mảnh màu xám nghĩa là U giống V đút ít, chỉ 0,344.” (0.904): “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: không (trong “không phẩy” → “”), không (trong “không phẩy” → “”) — NOT_VERIFIED bằng tai người',
    'Vì V nặng ký hơn, dự đoán sẽ gần 4 của V hơn là gần 5 của W.':
        'ASR chép “Vì về nặng ký hơn, dự đoán sẽ gần 4 của về hơn là gần 5 của về đúc.” (0.919): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Bước một là đo độ giống, theo bài 2, hai hàng điểm là hai vector, nên độ giống của hai người là cosin của hai vector đó.':
        'ASR chép “Bước 1 là đo độ giống, theo bài 2, hai hàng điểm là hai vector, nên độ giống của hai người là cosine của hai vector đó.” (0.963): lệch âm/thanh thuần Việt: cosin/cosine — NOT_VERIFIED bằng tai người',
    'Ở đây cả V và W đều đã chấm ốp lưng, nên với k bằng 2 ta lấy cả hai.':
        'ASR chép “Ở đây, cả V và V đúc đều đã chấm óc lưng, nên với ca bằng hai ta lấy cả hai.” (0.878): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: ốp/óc — NOT_VERIFIED bằng tai người',
    'Bước ba, ta làm lại y hệt với W.':
        'ASR chép “Bước 3. Ta làm lại y hợp với Vê Đúc.” (0.737): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: hệt/hợp — NOT_VERIFIED bằng tai người',
    'Chia ra, độ giống của U và W chỉ khoảng 0 phẩy 344, vì W thích ốp lưng mà chê tai nghe, ngược với U.':
        'ASR chép “Chia ra, độ giống của U và Vđúc chỉ khoảng 0,344 vì Vđúc thích óc lưng mà chia tay nghe ngược với U.” (0.786): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; lệch âm/thanh thuần Việt: không (trong “không phẩy” → “”), ốp/óc, chê tai/chia tay — NOT_VERIFIED bằng tai người',
    'Người U đã xem video J, và người xem J cũng hay xem L, M, N.':
        'ASR chép “Người U đã xem video gì và người xem gì cũng hay xem L, M, N.” (0.875): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Gợi ý cho U là hợp của hai nhóm, L, M, N, O, P, Q, trong đó N được nhắc hai lần nên đáng đứng đầu.':
        'ASR chép “gợi ý cho u là hợp của hai nhóm L, M, N, O, T, Q, trong đó N được nhắc hai lần nên đáng đứng đầu.” (0.962): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Số 0 nghĩa là chưa chấm, không phải ghét, nên hãy đếm riêng số ô đã chấm trước khi lấy trung bình.':
        'ASR chép “Số không nghĩa là chưa chấm, không phải ghét, nên hãy đếm riêng số O đã chấm trước khi lấy trung bình.” (0.955): “ô” (ô lưới) ASR viết chữ “O” — NOT_VERIFIED bằng tai người',
    'U và V chỉ cùng chấm tai nghe, nếu tính cosin trên đúng món chung đó thì ra 5 nhân 4 chia 5 nhân 4, bằng 1, tức giống hệt nhau.':
        'ASR chép “U và V chỉ cùng chấm tay nghe, nếu tính cô xin trên đúng món chung đó thì ra 5 nhân 4 chia 5 nhân 4 bằng 1, tức giống hệt nhau.” (0.921): lệch âm/thanh thuần Việt: tai/tay, cosin/cô xin — NOT_VERIFIED bằng tai người',
    'Với một món chung thì cosin luôn bằng 1, nên hãy đòi tối thiểu vài món chung trước khi tin độ giống.':
        'ASR chép “Với một món chung thì cô xin luôn bằng một, nên hãy đòi tối thiểu vài món chung trước khi tinh độ giống.” (0.889): lệch âm/thanh thuần Việt: cosin/cô xin, tin/tinh — NOT_VERIFIED bằng tai người',
    'W chấm trung bình chỉ khoảng 2 phẩy 667 mà chấm ốp lưng 5, cao hơn hẳn thói quen, lệch cộng 2 phẩy 333.':
        'ASR chép “Về đút, chấm trung bình chỉ khoảng 2,667 mà chấm ốc lưng 5, cao hơn hẳn thói quen, lệch cộng 2,333.” (0.862): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; lệch âm/thanh thuần Việt: ốp/ốc — NOT_VERIFIED bằng tai người',
    'Bây giờ đến lượt bạn, ta thay W bằng người X, chưa chấm tai nghe, chấm sạc 4 và chấm ốp lưng 2.':
        'ASR chép “Bây giờ đến lượt bạn, ta thay về đúc bằng người ích chưa chấm tay nghe chấm sạc 4 và chấm óp lưng 2.” (0.851): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: tai/tay, ốp/óp — NOT_VERIFIED bằng tai người',
    'Câu một, tính cosin của u và x, với u bằng 5, 3, 0.':
        'ASR chép “Câu 1, tính coxin của u và x với u bằng 5, 3, 0.” (0.929): lệch âm/thanh thuần Việt: cosin/coxin — NOT_VERIFIED bằng tai người',
    'Tổng kết lại, mỗi hàng điểm là một vector, độ giống của hai người là cosin của hai vector.':
        'ASR chép “Tổng kết lại, mỗi hàng điểm là 1 vector, độ giống của 2 người là cosine của 2 vector.” (0.947): lệch âm/thanh thuần Việt: cosin/cosine — NOT_VERIFIED bằng tai người',
    # ── Khoá mới: IRS L07 ──
    'Khi đó ta chỉ cần gần 25 triệu số, bằng khoảng 1 phần 343 số ô.':
        'ASR chép “Khi đó, ta chỉ cần gần 25 triệu số bằng khoảng 1 phần 343 số ố.” (0.955): “ô” (ô lưới) ASR viết chữ “O” — NOT_VERIFIED bằng tai người',
    'Vì vậy mỗi bước có thêm phần lambda nhân p kéo vector về phía 0.':
        'ASR chép “Vì vậy, mỗi bước có thêm phần Lam đa nhân tê kéo vector về phía không?” (0.848): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: véc tơ/vector — NOT_VERIFIED bằng tai người',
    'Làm thử với lambda bằng 0 phẩy 1, p mới là 1 phẩy 015 và 2 phẩy 03, nhích ít hơn so với khi không phạt.':
        'ASR chép “Làm thử với Lam Da bằng 0,1, về mới là 1,015 và 2,03, nhất ít hơn so với khi không phạt.” (0.828): lam-đa (λ), ASR viết “lambda”; chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; lệch âm/thanh thuần Việt: nhích/nhất — NOT_VERIFIED bằng tai người',
    'Lỗi thứ hai là không chính quy hoá, lambda bằng 0, cho người mới chỉ chấm đúng một phim.':
        'ASR chép “Lỗi thứ hai là không chính quy hóa, làm đa bằng không, cho người mới chỉ chấm đúng một phim.” (0.95): lam-đa (λ), ASR viết “lambda” — NOT_VERIFIED bằng tai người',
    'Câu hai, có phạt lambda 0 phẩy 1, p mới là 2 phẩy 08 và 1 phẩy 09, nhích ít hơn một chút.':
        'ASR chép “Câu 2, có phạt lam đa 0,1, tè mới là 2,08 và 1,09, nhất ít hơn 1 chút.” (0.917): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: nhích/nhất — NOT_VERIFIED bằng tai người',
    # ── Khoá mới: IRS L08 ──
    'Người V xem cả A và B.':
        'ASR chép “Người với xem cả A và B.” (0.857): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Một bài báo năm 2019 của đội gợi ý video chỉ ra điều này, và họ trừ lôgarit của tần suất lọt lô vào điểm lúc huấn luyện.':
        'ASR chép “Một bài báo năm 2019 của đội gợi EVDO chỉ ra điều này và họ trừ Logatic của tần suốt lọc lô vào điểm lúc huấn luyện.” (0.862): lệch âm/thanh thuần Việt: ý video/evdo, lôgarit/logatic, suất lọt/suốt lọc — NOT_VERIFIED bằng tai người',
    'Bảng gom lời cảnh báo của các nhóm tác giả về dữ liệu ngầm.':
        'ASR chép “Bản con lời cảnh báo của các nhóm tác giả về dữ liệu ngâm.” (0.786): lệch âm/thanh thuần Việt: bảng gom/bản con, ngầm/ngâm — NOT_VERIFIED bằng tai người',
    'Theo tần suất thường thì tỉ lệ 81 trên 1, phần của D chỉ 1 chia 82, khoảng 0 phẩy 0122, nhỏ gần ba lần.':
        'ASR chép “Theo từng xuất thường thì tỷ lệ 81 trên 1, phần của G chỉ 1 chia 82, khoảng 0.00122, nhỏ gần 3 lần.” (0.892): Manhattan đọc “Man-hát-tần” theo lexicon chung, ASR viết “mang hát tân/tầng”; “tỉ” ASR viết chính tả “tỷ” (cùng âm); chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải” — NOT_VERIFIED bằng tai người',
    # ── Khoá mới: IRS L09 ──
    'Ba chữ m a x nghĩa là lấy số lớn nhất, và niềm tin ban đầu của mọi sản phẩm mới là Beta 1 1.':
        'ASR chép “Ba chữ M à ít nghĩa là lấy số lớn nhất và niềm tin ban đầu của mọi sản phẩm mới là beta 11.” (0.885): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; beta đọc “bê-ta”, ASR viết “bê/beta”; lệch âm/thanh thuần Việt: một/∅ — NOT_VERIFIED bằng tai người',
    # ── Khoá mới: IRS L10 ──
    'Bước bốn là đo p r bằng hoán đổi ngẫu nhiên, nhóm tác giả năm 2017 đổi chỗ kết quả đứng đầu với kết quả ở một vị trí ngẫu nhiên từ 1 tới 21, suốt 7 ngày.':
        'ASR chép “Bước bốn là đo TER bằng hoán đổi ngẫu nhiên, nhóm tác giả năm 2017 đổi chỗ kết quả đứng đầu với kết quả ở một vị trí ngẫu nhiên từ 1 tới 21, suốt 7 ngày.” (0.966): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Cùng một kết quả, chỉ khác chỗ đứng, nên mức liên quan triệt tiêu, và tỉ số tỉ lệ bấm chính là p j chia p 1.':
        'ASR chép “Cùng một kết quả, chỉ khác chỗ đứng nên mức liên quan trịt tiêu và tỷ số tỷ lệ bấm chính là PGGP1.” (0.784): “tỉ” ASR viết chính tả “tỷ” (cùng âm); chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: triệt/trịt, chia (trong “p j chia p” → “pggp”) — NOT_VERIFIED bằng tai người',
    'Đáp án câu một, D có 40 chia 1000 bằng 0 phẩy 04, chia cho 1 vẫn là 0 phẩy 04.':
        'ASR chép “Đáp án câu 1, về có 40 chia 1.000 bằng 0.04, chia cho 1 vẫn là 0.04.” (0.909): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải” — NOT_VERIFIED bằng tai người',
    # ── Khoá mới: IRS L11 ──
    'Điều thứ hai, ba chữ m a x là lấy số lớn nhất, giữa 0 phẩy 8 và 0 phẩy 1 thì được 0 phẩy 8.':
        'ASR chép “Điều thứ 2, 3 chữ m, ít là lấy số lớn nhất giữa 0,8 và 0,1 thì được 0,8.” (0.98): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Điều thứ ba, ở bài 1, độ lợi ở vị trí i được nhân với chiết khấu 1 chia lôgarit cơ số 2 của i cộng 1, vì vị trí càng sâu càng ít người nhìn.':
        'ASR chép “Điều thứ 3, ở bài 1, đổ lợi ở vị trí y được nhân với chiếc khấu 1 chia logatric cơ số 2 của y cộng 1 vì vị trí càng sâu càng ít người nhìn.” (0.917): lệch âm/thanh thuần Việt: độ/đổ, chiết/chiếc, lôgarit/logatric — NOT_VERIFIED bằng tai người',
    'Bảng giải mã từng ký hiệu, ba chữ r e l viết tắt mức liên quan của ứng viên D với câu hỏi, như của X là 0 phẩy 9.':
        'ASR chép “Bản giải mã từng ký hiệu, 3 chữ R, L viết tắt mức liên quan của ứng viên dê với câu hỏi, như của x là 0,9.” (0.949): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: bảng/bản — NOT_VERIFIED bằng tai người',
    'Y ở xa A nên giữ gần hết điểm liên quan, và được chọn vào ô thứ hai.':
        'ASR chép “Ở xa A nên giữ gần hết điểm liên quan và được chọn vào ô thứ 2.” (0.971): lệch âm/thanh thuần Việt: i/∅ — NOT_VERIFIED bằng tai người',
    'Làm thử với X, lambda bằng 1 cho 0 phẩy 9, lambda bằng 0 cho âm 0 phẩy 8.':
        'ASR chép “Làm thử với x, làm đa bằng một cho 0,9, làm đa bằng không cho âm 0,8.” (0.905): lam-đa (λ), ASR viết “lambda” — NOT_VERIFIED bằng tai người',
    'Ở ô ba, X được 0 phẩy 27 trừ 0 phẩy 56, bằng âm 0 phẩy 29, còn Z được 0 phẩy 18 trừ 0 phẩy 21, bằng âm 0 phẩy 03.':
        'ASR chép “Ở O3, ít được 0,27-0,56 bằng âm 0,29, còn giác được 0,18-0,21 bằng âm 0,03.” (0.95): “ô” (ô lưới) ASR viết chữ “O”; lệch âm/thanh thuần Việt: trừ/∅, trừ/∅ — NOT_VERIFIED bằng tai người',
    'Đáp án câu một, X được 0 phẩy 72 trừ 0 phẩy 16, bằng 0 phẩy 56, cao nhất, nên ô hai chọn X, đúng như phép giải lambda trên 0 phẩy 778.':
        'ASR chép “Đáp án câu một, ít được 0,72 trừ 0,16, bằng 0,56, cao nhất, nên O2 chọn ít, đúng như phép dải lambda trên 0,778.” (0.952): “ô” (ô lưới) ASR viết chữ “O”; “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; lệch âm/thanh thuần Việt: không (trong “không phẩy” → “”) — NOT_VERIFIED bằng tai người',
    # ── Khoá mới: IRS L12 ──
    'Tổng 80 mi li giây, còn 20 mi li giây dự phòng cho xếp lại và cho những lúc chậm.':
        'ASR chép “Tổng 80 mili dây, còn 20 mili dây dự phòng cho xếp lại và cho những lúc chậm.” (0.762): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh — NOT_VERIFIED bằng tai người',
    'B có mô hình tốt hơn ở đầu danh sách, đổi lại mất 7 điểm độ phủ ở tầng đầu.':
        'ASR chép “V có mô hình tốt hơn ở đầu danh sách, đổi lại mất 7 điểm độ phủ ở tân đầu.” (0.9): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: tầng/tân — NOT_VERIFIED bằng tai người',
    # ── Khoá mới: IRS L13 ──
    'Bạn xem J và K, người xem J hay xem L, M, N, người xem K hay xem N, O, P, Q, nên gợi ý hợp các tập đó, và N được nhắc tới hai lần.':
        'ASR chép “Bạn xem G và K, người xem G hay xem L, M, N, người xem K hay xem N, O, T, Quy nên gợi ý hợp các tập đó và N được nhắc tới 2 lần.” (0.917): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Bảng vector của thí nghiệm có 1 triệu video, mỗi video 256 số thực 4 byte, tức khoảng 1 tỉ byte.':
        'ASR chép “Bảng vector của thiến nghiệm có 1 triệu video, mỗi video 256 số thực 4 bay, tức khoảng 1 tỷ bay.” (0.84): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); “tỉ” ASR viết chính tả “tỷ” (cùng âm); lệch âm/thanh thuần Việt: thí/thiến — NOT_VERIFIED bằng tai người',
    'Trọng số sửa thiên lệch luôn có cắt, và chính mức cắt cũng được thử trực tuyến.':
        'ASR chép “Trọng số sử thiên lịch luôn có cắt, và 9 bức cắt cũng được thử trực tuyến.” (0.765): lệch âm/thanh thuần Việt: sửa/sử, lệch/lịch, chính mức/chín bức — NOT_VERIFIED bằng tai người',
    'Bảng vector năm 2016 tính từng video trước, 256 số nhân 4 byte là 1024 byte, nhân 1 triệu video ra 1 tỉ 024 triệu byte, khớp.':
        'ASR chép “Bảng vector năm 2016 tính từng video trước, 256 số nhân 4 bay là 1024 bay, nhân 1 triệu video ra 1 tỷ 024 triệu bay, khớp.” (0.909): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); “tỉ” ASR viết chính tả “tỷ” (cùng âm) — NOT_VERIFIED bằng tai người',
    # ── INT L00-L07 NamMinh (2026-11-07) ──
    'Chào bạn, nhiều bạn băn khoăn liệu chỉ xem vài chục phút video có đủ để trở thành kỹ sư ngân hàng cấp cao và thương lượng mức lương 50 triệu gross hay không.':
        'ASR chép “Chào bạn! Nhiều bạn băng khoang liệu chỉ xem vài chục phút video có đủ để trở thành kỹ sư ngân hàng cấp cao và thương lượng mức lương 50 triệu g-rốt hay không?” (0.917): lệch âm/thanh thuần Việt: băn khoăn/băng khoang, gơ/g — NOT_VERIFIED bằng tai người',
    'Bước một, cổng tích hợp sử dụng lệnh nguyên tử của Redis để tạo khóa phân tán theo mã giao dịch.':
        'ASR chép “Bước 1, cộng tích hợp sử dụng lệnh nguyên tử của Reddit để tạo khóa phân tán theo mã giao dịch.” (0.905): lệch âm/thanh thuần Việt: cổng/cộng, redis/reddit — NOT_VERIFIED bằng tai người',
    'Dữ liệu nạp từ bộ nhớ chính lên bộ nhớ đệm luôn theo từng khối 64 byte.':
        'ASR chép “Giữ liệu nạp từ bộ nhớ chính lên bộ nhớ đệm luôn theo từng khối 64 bay.” (0.947): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Nhưng với luồng ảo trong Java 21, mỗi kết nối chỉ tiêu tốn vài trăm byte.':
        'ASR chép “Nhưng với luận ảo trong Java 21, mỗi kết nối chỉ tiêu tốn vài trăm bay.” (0.889): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: luồng/luận — NOT_VERIFIED bằng tai người',
    'Hạ tầng máy chủ trang bị mười sáu gigabyte bộ nhớ và tám nhân xử lý.':
        'ASR chép “Hạ tầng máy chủ trang bị 16GB bộ nhớ và 8 nhân xử lý.” (0.938): lệch âm/thanh thuần Việt: gigabyte/gb — NOT_VERIFIED bằng tai người',
    'Bước một, nếu dùng luồng truyền thống, mười nghìn luồng sẽ ngốn tới mười gigabyte bộ nhớ ngăn xếp.':
        'ASR chép “Bước 1, nếu dùng luồng truyền thống, 10.000 luồng sẽ ngũn tới 10GB bộ nhớ ngăn xếp.” (0.895): lệch âm/thanh thuần Việt: ngốn/ngũn, gigabyte/gb — NOT_VERIFIED bằng tai người',
    'Bước hai, khi chuyển sang luồng ảo trong Java 21, mười nghìn luồng chỉ tiêu thụ khoảng năm megabyte bộ nhớ.':
        'ASR chép “Bước 2, khi chuyển sang luận ảo trong Java 21, 10.000 lùng chỉ tiêu thụ khoảng 5 MB bộ nhớ.” (0.87): lệch âm/thanh thuần Việt: luồng/luận, luồng/lùng, megabyte/mb — NOT_VERIFIED bằng tai người',
    'Do đó khi có chỉ mục cây nhiều nhánh, việc tìm kiếm đạt độ phức tạp lôgarit và chỉ mất từ ba đến bốn lần đọc đĩa.':
        'ASR chép “Do đó khi có chỉ một cây nhiều nhánh, việc tìm kiếm đạt độ phức tạp logatric và chỉ mất từ 3 đến 4 lần độc đĩa.” (0.889): lệch âm/thanh thuần Việt: mục/một, lôgarit/logatric, đọc/độc — NOT_VERIFIED bằng tai người',
    'Nắm vững nền tảng khoa học máy tính lõi, bạn tự tin làm chủ các hệ thống cao tải và bảo vệ mức lương 50 triệu gross tại ACB.':
        'ASR chép “Nắm vững nền tảng khoa học máy tính lõi, bạn tự tin làm chủ các hệ thống cao tải và bảo vệ mức lương 50 triệu GROP tại ACB.” (0.967): lệch âm/thanh thuần Việt: gross/grop — NOT_VERIFIED bằng tai người',
    'Nguyên nhân bắt nguồn từ cơ chế ủy quyền động của Spring Boot bị vô hiệu hóa khi tự gọi hàm nội bộ.':
        'ASR chép “Nguyên nhân bắt nguồn từ cơ chế ủy quyền động của Springbook bị vô hiệu hóa khi tự gọi hàm nội bộ.” (0.933): lệch âm/thanh thuần Việt: spring boot/springbook — NOT_VERIFIED bằng tai người',
    'Trước tiên ta ôn lại vòng đời của đối tượng trong Spring Boot.':
        'ASR chép “trước tiên ta ôn lại vòng đời của đối tượng trong Spring Book.” (0.923): lệch âm/thanh thuần Việt: boot/book — NOT_VERIFIED bằng tai người',
    'Làm chủ những kỹ thuật tinh hoa này, bạn tự tin gánh vác các hệ thống tài chính lớn và bảo vệ mức lương 50 triệu gross tại ACB.':
        'ASR chép “Làm chủ những kỹ thuật tinh hoa này, bạn tự tin gánh vác các hệ thống tài chính lớn và bảo vệ mức lương 50 triệu g-rốt tại ACB.” (0.97): lệch âm/thanh thuần Việt: gơ/g — NOT_VERIFIED bằng tai người',
    'Toàn bộ bảng dữ liệu tài khoản sẽ bị đóng băng khiến ứng dụng cạn kiệt kết nối.':
        'ASR chép “Toàn bộ bản dữ liệu tai khoản sẽ bị đóng băng khiến ứng dụng càng kỳ kết nối.” (0.778): lệch âm/thanh thuần Việt: bảng/bản, tài/tai, cạn kiệt/càng kỳ — NOT_VERIFIED bằng tai người',
    'Nắm vững những vũ khí phân tán này, bạn tự tin làm chủ hạ tầng thanh toán cốt lõi và khẳng định mức đãi ngộ 50 triệu gross tại ACB.':
        'ASR chép “Nắm vững những vũ khí phân tán này, bạn tự tin làm chủ hạ tầng thanh toán cốt lõi và khẳng định mức đại ngộ 50 triệu g-rốt tại ACB.” (0.941): lệch âm/thanh thuần Việt: đãi/đại, gơ/g — NOT_VERIFIED bằng tai người',
    'Sáu trụ cột tín dụng bán lẻ bao quát trọn vẹn vòng đời một khoản vay số.':
        'ASR chép “Sáu trụ cục tín dụng bán lẻ bao quát trọng vẹn vòng đời một khoảng vây số.” (0.765): lệch âm/thanh thuần Việt: cột/cục, trọn/trọng, khoản vay/khoảng vây — NOT_VERIFIED bằng tai người',
    'Làm chủ nghiệp vụ ngân hàng cốt lõi này, bạn tự tin thể hiện bản lĩnh chuyên gia và khẳng định mức đãi ngộ 50 triệu gross tại ACB.':
        'ASR chép “Làm chủ nghiệp vụ ngân hàng cốt lõi này, bạn tự tin thể hiện bản lĩnh chuyên gia và khẳng định mức đải ngộ 50 triệu g-rốt tại ACB.” (0.939): lệch âm/thanh thuần Việt: đãi/đải, gơ/g — NOT_VERIFIED bằng tai người',
    'Tóm lại, chuỗi logic gồm nền tảng học thuật đại học, kiến trúc đường dẫn kép, suy luận máy học tốc độ cao và định tuyến thông minh.':
        'ASR chép “Tóm lại, chủ lô ghét gồm nền tảng học thuật đại học, kiến trúc đường dẫn kép, suy luận máy học tốc độ cao và định tuyến thông minh.” (0.931): lệch âm/thanh thuần Việt: chuỗi/chủ, gíc/ghét — NOT_VERIFIED bằng tai người',
    'Biến tri thức đỉnh cao thành giá trị bảo vệ hệ thống, bạn tự tin khẳng định vị thế Kỹ sư Cấp cao và xứng đáng với mức lương 50 triệu gross tại ACB.':
        'ASR chép “Biến tri thức đỉnh cao thành giá trị bảo vệ hệ thống, bạn tự tin khẳng định vì thế kỷ sư cấp cao và xính đáng với mức lương 50 triệu g rốt tại ACB.” (0.895): lệch âm/thanh thuần Việt: vị/vì, kỹ/kỷ, xứng/xính, gơ/g — NOT_VERIFIED bằng tai người',
    'Tầng cổng vào chịu trách nhiệm bảo mật và phân luồng.':
        'ASR chép “Tân cổng vào chiều trách nhiệm bảo mật và phân luôn.” (0.727): lệch âm/thanh thuần Việt: tầng/tân, chịu/chiều, luồng/luôn — NOT_VERIFIED bằng tai người',
    'Chi phí trả mức lương năm mươi triệu gross tương đương khoảng bảy trăm năm mươi triệu một năm.':
        'ASR chép “chi phí trả mức lương 50 triệu gờ rốt tương đương khoảng 750 triệu một năm.” (0.95): lệch âm/thanh thuần Việt: gơ/gờ — NOT_VERIFIED bằng tai người',
    # ── ACB L00-L08 NamMinh (2026-11-07) ──
    'Hôm nay ta cùng phân tích toàn cảnh kiến trúc tích hợp ngân hàng, từ Core T24, Cổng NAPAS, điều phối SAGA, tới mức lương 50 triệu gross.':
        'ASR chép “Hôm nay ta cùng phân tích toàn cảnh kiến trúc tích hợp ngân hàng từ Co T-24, cổng Nà Phát, Điều Phối Saga tới mức lương 50 triệu g-rốt.” (0.879): lệch âm/thanh thuần Việt: core/co, napas/nà phát, gross/g rốt — NOT_VERIFIED bằng tai người',
    'Một giây bằng một nghìn mi li giây.':
        'ASR chép “Một dây bằng một nghìn mili dây.” (0.667): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh — NOT_VERIFIED bằng tai người',
    'Bản tin OFS là định dạng giao tiếp chuẩn của Core Banking Temenos T24 qua hàng đợi IBM MQ.':
        'ASR chép “Bản tin OFS là định dạng giao tiếp chuẩn của con banh kiên Temenok T24 qua hàng đợi IBM MQ.” (0.862): lệch âm/thanh thuần Việt: co/con, king te me nót/kiên temenok — NOT_VERIFIED bằng tai người',
    'Chuẩn ISO 8583 là giao thức bản tin tài chính qua cổng chuyển mạch NAPAS.':
        'ASR chép “Chuẩn ISO 8583 là giao thức bản tin tài chính qua cổng chuyển mạch NAPAC.” (0.952): lệch âm/thanh thuần Việt: napas/napac — NOT_VERIFIED bằng tai người',
    'Mô hình SAGA là chuỗi giao dịch phân tán giúp tự động hoàn tiền khi đối tác sập.':
        'ASR chép “Mô hình Saga là chủ giao dịch phân tán giúp tự động hoàn tiền khi đối tách sập.” (0.889): lệch âm/thanh thuần Việt: chuỗi/chủ, tác/tách — NOT_VERIFIED bằng tai người',
    'Số kiểm toán STAN cùng số tham chiếu RRN là hai mã số dùng để đối soát liên ngân hàng.':
        'ASR chép “Số kiểm toán S-Thang cùng số tham chiếu RRN là hai mã số dùng để đối soát liên ngân hàng.” (0.927): lệch âm/thanh thuần Việt: stan/s thang — NOT_VERIFIED bằng tai người',
    'Tầng hai là trung tâm thanh toán kiểm tra khử trùng lặp trong Redis và điều phối trạng thái.':
        'ASR chép “Tần 2 là trung tâm thanh toán kiểm tra khử trùng lập trong reddit và điều phối trạng thái.” (0.842): lệch âm/thanh thuần Việt: tầng/tần, lặp/lập, redis/reddit — NOT_VERIFIED bằng tai người',
    'Tầng ba đóng gói bản tin tài chính ISO 8583 gửi qua socket TCP tới cổng NAPAS.':
        'ASR chép “Tần 3 đóng gói bản tin tài chính EXO 8583 gửi qua socket TCP tới cổng NaPak.” (0.87): lệch âm/thanh thuần Việt: tầng/tần, iso/exo, napas/napak — NOT_VERIFIED bằng tai người',
    'Và tầng bốn giao tiếp với Core Banking Temenos T24 qua hàng đợi IBM MQ.':
        'ASR chép “và tầng 4 giao tiếp với cò banking Temenos T24 qua hạng đợi IBMMQ.” (0.8): lệch âm/thanh thuần Việt: core/cò, hàng/hạng, ibm mq/ibmmq — NOT_VERIFIED bằng tai người',
    'Bước hai, ta đo lường độ trễ toàn trình.':
        'ASR chép “Bước 2. Ta đo lương độ trễ toàn trinh.” (0.778): lệch âm/thanh thuần Việt: lường/lương, trình/trinh — NOT_VERIFIED bằng tai người',
    'Thời gian mạng NAPAS tốn 120 mi li giây.':
        'ASR chép “thời gian mạng nạp phát tốn 120 ms.” (0.696): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; lệch âm/thanh thuần Việt: napas/nạp phát — NOT_VERIFIED bằng tai người',
    'Hạch toán Core T24 tốn 35 mi li giây.':
        'ASR chép “Hạch toán COT-24 tốn 35 mili giây.” (0.769): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; lệch âm/thanh thuần Việt: core (trong “core t” → “cot”) — NOT_VERIFIED bằng tai người',
    'Bước ba, ta thiết lập khoá khử trùng lặp trong Redis.':
        'ASR chép “Bước 3. Ta thiết lập khóa khử trùng lập trong reddit.” (0.818): lệch âm/thanh thuần Việt: lặp/lập, redis/reddit — NOT_VERIFIED bằng tai người',
    'Câu một, khi cổng NAPAS phản hồi hết giờ với bản tin 0200, ta nên xử lý thế nào?':
        'ASR chép “Câu một, khi cổng NAPAC phản hồi hết giờ với bản tin 0200, ta nên xử lý thế nào?” (0.95): lệch âm/thanh thuần Việt: napas/napac — NOT_VERIFIED bằng tai người',
    'Bạn là Chuyên viên chính tại OCB trực tiếp kiến trúc cổng Core T24 và NAPAS, từng phụ trách cho vay tại Mirae Asset, và có bằng Cử nhân AI tại trường UIT.':
        'ASR chép “Bạn là chuyên viên chính tại OCB trực tiếp kiến trúc cổng Cô T-24 và NaPak, từng phụ trách cho vay tại Midday Asset và có bằng cử nhân AI tại trường UIT.” (0.917): lệch âm/thanh thuần Việt: core/cô, napas/napak, mirae/midday — NOT_VERIFIED bằng tai người',
    'Tổng kết lại, hành trang phỏng vấn ACB được gắn kết theo chuỗi logic sau.':
        'ASR chép “Tổng kết lại, hành trang phỏng vấn ACB được gắn kết theo chuỗi lô kia sau.” (0.944): lệch âm/thanh thuần Việt: gíc/kia — NOT_VERIFIED bằng tai người',
    'Nắm vững Core T24 và NAPAS giúp bạn bảo toàn dòng tiền.':
        'ASR chép “Nắm vững Cote 24 và nạp hát giúp bạn bảo toàn dòng tiên.” (0.733): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: core (trong “core t” → “cote”), napas/nạp hát, tiền/tiên — NOT_VERIFIED bằng tai người',
    'Làm chủ Kafka và Oracle đảm bảo hệ thống chịu tải mượt mà.':
        'ASR chép “làm chủ Cupca và Oracle đảm bảo hệ thống chịu tải mượt ma.” (0.846): lệch âm/thanh thuần Việt: kafka/cupca, mà/ma — NOT_VERIFIED bằng tai người',
    'Chào bạn, trong kiến trúc công nghệ ngân hàng, Core Banking Temenos T24 là trái tim nắm giữ toàn bộ số dư và sổ cái.':
        'ASR chép “Chào bạn! Trong kiến trúc công nghệ ngân hàng, co-banking Teminoc T24 là trái tim nắm giữ toàn bộ số dư và số cái.” (0.893): lệch âm/thanh thuần Việt: core/co, temenos/teminoc, sổ/số — NOT_VERIFIED bằng tai người',
    'Mọi giao dịch mở tài khoản, chuyển tiền liên ngân hàng, hay tất toán sổ tiết kiệm đều phải gửi lệnh vào Core T24.':
        'ASR chép “Mọi giao dịch mở tài khoản, chuyển tiền liên ngân hàng hay tách toán sổ tiết kiệm đều phải gửi lệnh vào COTE24.” (0.906): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: tất/tách, core (trong “core t” → “cote”) — NOT_VERIFIED bằng tai người',
    'Hôm nay ta cùng phân tích sâu bản chất kỹ thuật: cấu trúc bản tin OFS XML, cơ chế gửi nhận bất đồng bộ qua IBM MQ, và giải pháp xử lý timeout chuẩn Senior.':
        'ASR chép “Hôm nay ta cùng phân tích sau bản chức kỹ thuật, cấu trúc bản tin OSSXML, cơ chế gửi nhận bất đồng bộ qua IBMMQ và giải pháp xử lý Timeout chuẩn Senior.” (0.853): lệch âm/thanh thuần Việt: sâu/sau, chất/chức, ofs xml/ossxml, ibm mq/ibmmq — NOT_VERIFIED bằng tai người',
    'Hàng đợi tin nhắn đóng vai trò vùng đệm, bảo đảm không làm mất dữ liệu khi Core Banking xử lý chậm.':
        'ASR chép “Hàng đời tin nhắn đóng vai trò vùng đệm, bảo đảm không làm mất dữ liệu khi co ban kiên xử lý chậm.” (0.87): lệch âm/thanh thuần Việt: đợi/đời, banh king/ban kiên — NOT_VERIFIED bằng tai người',
    'Bản tin OFS tuân theo cấu trúc phân cách nghiêm ngặt.':
        'ASR chép “Bản tin OSS Tuân theo cấu trúc phần cách nghiêm ngặt.” (0.818): lệch âm/thanh thuần Việt: ofs/oss, phân/phần — NOT_VERIFIED bằng tai người',
    'Ta kiểm tra tình huống thực tế khi máy chủ Core T24 bị quá tải dẫn tới hết thời gian chờ 3 giây.':
        'ASR chép “Ta kiểm tra tình huống thực tế khi máy chủ Cote 24 bị quá tải dẫn tới hết thời gian chờ 3 giây.” (0.941): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: core (trong “core t” → “cote”) — NOT_VERIFIED bằng tai người',
    'Khi kết nối Core T24 qua IBM MQ, tại sao ta bắt buộc phải dùng mã định danh tương quan thay vì mở hàng đợi riêng cho từng khách hàng?':
        'ASR chép “Khi kết nối có tê 24 qua IBMMQ, tại sao ta bắt buộc phải dùng mã định danh tương quan thay vì mở hàng đợi riêng cho từng khách hàng?” (0.923): lệch âm/thanh thuần Việt: core/có, ibm mq/ibmmq — NOT_VERIFIED bằng tai người',
    'Tóm lại, chuỗi logic tích hợp Core T24 gồm tạo bản tin OFS, gán mã định danh, đẩy vào hàng đợi yêu cầu và nhận kết quả an toàn.':
        'ASR chép “Tóm lại, chủ lô ghiết tích hợp CoT-24 gồm tàu bản tin OFS, gán mã định danh, đẩy vào hàng đời yêu cầu và nhận kết quả an toàn.” (0.841): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: chuỗi/chủ, gíc/ghiết, co (trong “co t” → “cot”), tạo/tàu, đợi/đời — NOT_VERIFIED bằng tai người',
    'Đây chính là năng lực thực chiến giúp bạn khẳng định vị thế Senior chuyên nghiệp và tự tin trước hội đồng ACB.':
        'ASR chép “Đây chính là năng lực thực chiến giúp bạn khẳng định vị thế senior chuyên nghiệp và tự tin trước hội đồng ACB.” (1.0): từ rủi ro xi, ni, ơ cả hai mô hình viết khác (cách viết, không phải âm) — NOT_VERIFIED bằng tai người',
    'Phía sau sự mượt mà đó là cả một hệ sinh thái chuyển mạch liên ngân hàng NAPAS 247 chạy liên tục suốt ngày đêm.':
        'ASR chép “phía sau sự mượt mà đó là cả một hệ sinh thái chuyển mạch liên ngân hàng NAPAC 247 chạy liên tục suốt ngày đêm.” (0.966): lệch âm/thanh thuần Việt: napas/napac — NOT_VERIFIED bằng tai người',
    'Từng giao dịch đều được đóng gói bằng bản tin ISO 8583 nhị phân và gửi qua đường truyền TCP chuyên dụng.':
        'ASR chép “Từng giao dịch đều được đóng gói bằng bản tin ESO 8.583 nhị phân và gửi qua đường truyền TCP chuyên dụng.” (0.964): lệch âm/thanh thuần Việt: iso/eso — NOT_VERIFIED bằng tai người',
    'Hôm nay ta sẽ cùng giải mã toàn diện kiến trúc cổng NAPAS 247.':
        'ASR chép “Hôm nay ta sẽ cùng giải mã toàn diện kiến trúc cổng NaPak 247.” (0.944): lệch âm/thanh thuần Việt: napas/napak — NOT_VERIFIED bằng tai người',
    'Ta cũng nắm vững giải pháp khử trùng lặp đạt chuẩn Senior.':
        'ASR chép “Ta cũng nắm vững giải pháp khử trùng lập đạt chuẩn senior.” (0.917): lệch âm/thanh thuần Việt: lặp/lập — NOT_VERIFIED bằng tai người',
    'Bước bốn, hệ thống cập nhật sổ cái Core Banking và phản hồi kết quả thành công cho người gửi.':
        'ASR chép “Bước 4, hệ thống cập nhật sổ cái co banh kim và phản hồi kết quả thành công cho người gửi” (0.952): lệch âm/thanh thuần Việt: king/kim — NOT_VERIFIED bằng tai người',
    'Tóm lại, chuỗi logic cổng NAPAS gồm đóng gói bản tin, kiểm tra tính toàn vẹn, dịch mã bảo mật phần cứng, khử trùng lặp và đối soát sổ cái.':
        'ASR chép “Tóm lại, chuỗi lô ghét cổng NaPak gồm đóng gói bản tin, kiểm tra tính toàn vẹn, dịch mã bảo mật phần cứng, khử trùng lập và đối xóa sổ cái.” (0.857): lệch âm/thanh thuần Việt: gíc/ghét, pát (trong “na pát” → “napak”), lặp/lập, soát/xoá — NOT_VERIFIED bằng tai người',
    'Nắm vững bản chất này, bạn hoàn toàn làm chủ vị trí Kỹ sư Tích hợp Cấp cao và tự tin thương lượng mức thu nhập 50 triệu gross tại ngân hàng ACB.':
        'ASR chép “Nắm vững bản chất này, bạn hoàn toàn làm chủ vị trí kỹ sư tích hợp cấp cao và tự tin thương lượng mức thu nhập 50 triệu GROT tại ngân hàng ACB.” (0.971): lệch âm/thanh thuần Việt: gross/grot — NOT_VERIFIED bằng tai người',
    'Ta phân tích nền tảng Confluent cây-x-cu-l-đê-bê và Kafka Streams.':
        'ASR chép “Ta phân tích nền tảng cong pha luân Case Cooler DB và CapCash Stream.” (0.533): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: confluent cây cu (trong “confluent cây x cu l” → “cong pha luân case cooler”), kafka streams/capcash stream — NOT_VERIFIED bằng tai người',
    'Bước hai, máy chủ cây-x-cu-l-đê-bê kết hợp luồng giao dịch với bảng hồ sơ khách hàng để chọn kênh gửi tối ưu.':
        'ASR chép “Bước 2, máy chủ Case Cooler DB kết hợp luồn giao dịch với bản hồ sơ khách hàng để chọn kênh gửi tối ưu.” (0.808): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: cây cu (trong “cây x cu l” → “case cooler”), luồng/luồn, bảng/bản — NOT_VERIFIED bằng tai người',
    'Câu lệnh cây-x-cu-l-đê-bê thể hiện sức mạnh xử lý luồng tức thời.':
        'ASR chép “Câu lệnh Case Cooler DB thể hiện sức mạnh xử lý lùng tức thời.” (0.75): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: cây cu (trong “cây x cu l” → “case cooler”), luồng/lùng — NOT_VERIFIED bằng tai người',
    'Trong công nghệ cây-x-cu-l-đê-bê, tại sao bảng hồ sơ người dùng bắt buộc phải được tạo dưới dạng Bảng thay vì dạng Luồng?':
        'ASR chép “Trong công nghệ Case Cooler DB, tại sao bản hồ sơ người dùng bắt buộc phải được tạo dưới dạng bản thay vì dạng luôn?” (0.778): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: cây cu (trong “cây x cu l” → “case cooler”), bảng/bản, bảng/bản, luồng/luôn — NOT_VERIFIED bằng tai người',
    'Tóm lại, chuỗi logic truyền phát gồm bắt biến động dữ liệu, kết hợp luồng qua cây-x-cu-l-đê-bê, phân luồng đa kênh, khử trùng lặp và chuyển phát an toàn.':
        'ASR chép “Tóm lại, chủ lô gít truyền phát gồm bắt biến động dữ liệu, kết hợp luồn qua KSQDB, phân luồn đa kênh, khử trùng lập và chuyển phát an toàn.” (0.738): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: chuỗi/chủ, gíc/gít, luồng/luồn, bê/ksqdb, cây cu (trong “cây x cu l d b” → “ksqdb”), luồng/luồn, lặp/lập — NOT_VERIFIED bằng tai người',
    'Nắm vững giải pháp này, bạn hoàn toàn tự tin tỏa sáng ở vị trí Kỹ sư Tích hợp Cấp cao và chinh phục mức thu nhập 50 triệu gross tại ACB.':
        'ASR chép “Nắm vững giải pháp này, bạn hoàn toàn tự tin tỏa sáng ở vị trí kỹ sư tích hợp cấp cao và chinh phục mức thu nhập 50 triệu GROT tại ACB.” (0.97): lệch âm/thanh thuần Việt: gross/grot — NOT_VERIFIED bằng tai người',
    'Cổng Fiber tiếp nhận và thực thi câu lệnh Khóa Lạc quan trên PostgreSQL.':
        'ASR chép “Cổng Faber tiếp nhận và thực thi câu lệnh khóa lạc quan trên pốc Re-eculer.” (0.8): lệch âm/thanh thuần Việt: fiber/faber, postgresql/pốc re eculer — NOT_VERIFIED bằng tai người',
    'Sau khi khóa thành công, hệ thống gửi bản tin OFS sang Core T24 để đổi quyền sở hữu sổ cái.':
        'ASR chép “Sau khi khóa thành công, hệ thống gửi bản tin OFS sang Corte24 để đổi quyền sở hữu số cái.” (0.902): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: co (trong “co t” → “corte”), sổ/số — NOT_VERIFIED bằng tai người',
    'Lỗi ORA không không không sáu không là sự cố bế tắc khóa kinh điển cần triệt tiêu.':
        'ASR chép “Lỗi OERA-00060 là sự cố bế tắc khóa kinh điển cần triệt tiêu.” (0.788): lệch âm/thanh thuần Việt: ora không không không/oera, không/mươi — NOT_VERIFIED bằng tai người',
    'Ta sử dụng mệnh đề lấy dữ liệu theo mảng kết hợp khóa hàng có thứ tự tăng dần.':
        'ASR chép “Ta sử dụng mình để lấy giữ liệu theo mạng cất hợp khóa hàng có thứ tự tăng dân.” (0.737): lệch âm/thanh thuần Việt: mệnh đề/mình để, mảng kết/mạng cất, dần/dân — NOT_VERIFIED bằng tai người',
    'Tóm lại, chuỗi logic gồm tiếp nhận lô lương, lưu vết hộp thư giao dịch, khóa hàng có thứ tự, cập nhật hàng loạt và tổng hợp sao kê phân tán.':
        'ASR chép “Tóm lại, chủ lô ghiết gồm tiếp nhận lô lương, lưu vết hộp thư giao dịch, khóa hàng có thứ tự, cập nhật hàng loạt và tổng hợp sau kê phân tán.” (0.875): lệch âm/thanh thuần Việt: chuỗi/chủ, gíc/ghiết, vết/véc, sao/sau — NOT_VERIFIED bằng tai người',
    'Nắm vững giải pháp này, bạn hoàn toàn tự tin làm chủ các cổng thanh toán doanh nghiệp lớn và đàm phán mức lương 50 triệu gross tại ACB.':
        'ASR chép “Nắm vững giải pháp này, bạn hoàn toàn tự tin làm chủ các cổng thanh toán doanh nghiệp lớn và đàm phán mức lương 50 triệu g-rốt tại ACB.” (0.97): lệch âm/thanh thuần Việt: gơ/g — NOT_VERIFIED bằng tai người',
    'Kết quả xác nhận trùng khớp hoàn toàn với ảnh lưu trên chíp căn cước.':
        'ASR chép “Kết quả xác nhận trung khấp hoàn toàn với ảnh lưu trên chip căn cứ.” (0.733): lệch âm/thanh thuần Việt: trùng khớp/trung khấp, chíp/chip, cước/cứ — NOT_VERIFIED bằng tai người',
    'Khi điều kiện tiên quyết được thỏa mãn, lệnh trừ tiền mới được phát hành sang Core T24.':
        'ASR chép “Khi điều kiện tiên quyết được thỏa mãn, lệnh trừ tiền mới được phát hành sang Cô Tê 24.” (0.952): lệch âm/thanh thuần Việt: core/cô — NOT_VERIFIED bằng tai người',
    'Tóm lại, chuỗi logic gồm kiểm tra hạn mức, quét khuôn mặt sống, so khớp căn cước công dân, cấp vé một lần và điều phối hạch toán an toàn.':
        'ASR chép “Tóm lại, chủ lô khít gồm kiểm tra hạn mức, quê khu mặt sống, so khấp căn cứ công dân, cấp vẽ một lần và điều phối hạt toán an toàn.” (0.742): lệch âm/thanh thuần Việt: chuỗi/chủ, gíc/khít, quét khuôn/quê khu, khớp/khấp, cước/cứ, vé/vẽ, hạch/hạt — NOT_VERIFIED bằng tai người',
    'Nắm vững giải pháp này, bạn hoàn toàn tự tin dẫn dắt các bài toán chuyển đổi số lớn và đàm phán mức lương 50 triệu gross tại ACB.':
        'ASR chép “Nắm vững giải pháp này, bạn hoàn toàn tự tin dẫn dắt các bài toán chuyển đổi số lớn và đàm phán mức lương 50 triệu g-rốt tại ACB.” (0.97): lệch âm/thanh thuần Việt: gơ/g — NOT_VERIFIED bằng tai người',
    'Cổng thanh toán tiếp nhận bản tin và bóc tách đầu số tài khoản ảo.':
        'ASR chép “Cổng thanh toán tiếp nhận bản tin và bốc tắt đầu số tài khỏa ngảo.” (0.733): lệch âm/thanh thuần Việt: bóc tách/bốc tắt, khoản ảo/khoả ngảo — NOT_VERIFIED bằng tai người',
    'Tỉ lệ cấp vốn khống chế hạn mức tối đa, còn biên độ chênh lệch quy định lãi suất khoản vay.':
        'ASR chép “tỷ lệ cấp vốn không chế hàng mức tối đa còn biên độ chênh lệch quy định lại xuất khoảng vây.” (0.714): “tỉ” ASR viết chính tả “tỷ” (cùng âm); lệch âm/thanh thuần Việt: khống/không, hạn/hàng, lãi/lại, khoản vay/khoảng vây — NOT_VERIFIED bằng tai người',
    'Bạn hoàn toàn xứng đáng với mức đãi ngộ 50 triệu gross tại ACB.':
        'ASR chép “Bạn hoàn toàn xứng đáng với mức đại ngộ 50 triệu G-Rot tại ACB.” (0.839): lệch âm/thanh thuần Việt: đãi/đại, gross/g rot — NOT_VERIFIED bằng tai người',
    # ── BNK L00-L14 NamMinh (2026-11-08) ──
    'Nó cho ra không phẩy chín chín chín, chín chín chín, và còn nhiều chữ chín nữa.':
        'ASR chép “Nó cho ra không phải 999, 999 và còn nhiều chữ 9 nữa.” (0.737): “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; lệch âm/thanh thuần Việt: chín chín/mươi — NOT_VERIFIED bằng tai người',
    'Thêm một đơn vị đo: một ki lô byte bằng một nghìn không trăm hai mươi bốn byte, và một mê ga byte là số đó nhân với chính nó.':
        'ASR chép “Thêm một đơn vị đo, một kilobytes bằng 1024 bytes và một megabyte là số đó nhân với chính nó.” (0.821): KB đọc “ki-lô-byte” theo lexicon của khoá, ASR viết “kilobyte/kg”; byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); MB đọc “mê-ga-byte” theo lexicon của khoá, ASR viết “MB/megabyte” — NOT_VERIFIED bằng tai người',
    'Giả sử mỗi đối tượng chiếm một trăm byte, đây là số minh hoạ, và heap đang có sáu đối tượng từ A đến F.':
        'ASR chép “Giả sử mỗi đối tượng chiếm 100 vai, đây là số minh họa và HIP đang có 6 đối tượng từ A đến F.” (0.92): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: heap/hip — NOT_VERIFIED bằng tai người',
    'Phép tính thứ nhất, tổng bộ nhớ là sáu nhân một trăm, bằng sáu trăm byte.':
        'ASR chép “Phép tính thứ nhất, tổng bộ nhớ là 6 nhân 100 bằng 600 bay.” (0.938): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Phép tính thứ ba, bộ nhớ đang sống là ba nhân một trăm, bằng ba trăm byte.':
        'ASR chép “Phép tính thứ ba, bộ nhớ đang sống là 3 nhân 100, bằng 300 vai.” (0.941): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Phép tính thứ tư, bộ nhớ dọn được là sáu trăm trừ ba trăm, bằng ba trăm byte.':
        'ASR chép “Phép tính thứ 4, bộ nhớ dọn được là 600 trừ 300 bằng 300 bay.” (0.944): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Phép tính thứ năm, dọn được năm nhân một trăm, bằng năm trăm byte.':
        'ASR chép “Phép tính thứ 5, dọn được 5 nhân 100 bằng 500 bay.” (0.929): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'BigDecimal giữ số thập phân nên đúng.':
        'ASR chép “BitDecimon giữ số thập phân nên đúng.” (0.857): lệch âm/thanh thuần Việt: bigdecimal/bitdecimon — NOT_VERIFIED bằng tai người',
    'Câu một, heap có bốn đối tượng, gốc chỉ trỏ tới X, X trỏ tới Y, còn Z trỏ tới W.':
        'ASR chép “Câu 1, hiếp có 4 đối tượng, gốc chỉ trọ tới ít, ít trọ tới y, còn giác trọ tới về đúc.” (0.744): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: heap/hiếp, trỏ/trọ, trỏ/trọ, trỏ/trọ — NOT_VERIFIED bằng tai người',
    'Z và W không có đường từ gốc, nên rác là bốn trừ hai bằng hai.':
        'ASR chép “Giác và vê đúc không có đường từ gốc, nền trác là 4 trừ 2 bằng 2.” (0.788): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: nên rác/nền trác — NOT_VERIFIED bằng tai người',
    'Đáp án câu hai.':
        'ASR chép “Đập án câu 2.” (0.75): lệch âm/thanh thuần Việt: đáp/đập — NOT_VERIFIED bằng tai người',
    'Hai đối tượng rác nhân năm mươi byte, bằng một trăm byte.':
        'ASR chép “2 đối tượng trác nhân 50 bài bằng 100 bài.” (0.75): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: rác/trác — NOT_VERIFIED bằng tai người',
    'Số thực nhị phân dễ viết nhưng lệch.':
        'ASR chép “Số thực nhị phân dễ viết nhân lịch” (0.75): lệch âm/thanh thuần Việt: nhưng lệch/nhân lịch — NOT_VERIFIED bằng tai người',
    'Số nguyên đơn vị nhỏ nhất, hoặc BigDecimal, chính xác.':
        'ASR chép “số nguyên đơn vị nhỏ nhất hoặc bích decimal chính xác.” (0.857): lệch âm/thanh thuần Việt: bigdecimal/bích decimal — NOT_VERIFIED bằng tai người',
    'Tên biến giữ tham chiếu, tham chiếu trỏ tới đối tượng trên heap.':
        'ASR chép “Tên biến dự tham chiếu, tham chiếu trọ tới đối tượng trên hiếp” (0.769): lệch âm/thanh thuần Việt: giữ/dự, trỏ/trọ, heap/hiếp — NOT_VERIFIED bằng tai người',
    'Hãy dùng số nguyên đơn vị nhỏ nhất, hoặc BigDecimal.':
        'ASR chép “Hãy dùng số nguyên đơn vị nhỏ nhất hoặc bích decimal.” (0.857): lệch âm/thanh thuần Việt: bigdecimal/bích decimal — NOT_VERIFIED bằng tai người',
    'Một là hai luồng sửa cùng một số dư thì mất khoản nạp.':
        'ASR chép “Một là hai luồng sữa cùng một số dư thì mất khoảng ngập.” (0.769): lệch âm/thanh thuần Việt: sửa/sữa, khoản nạp/khoảng ngập — NOT_VERIFIED bằng tai người',
    'Luồng ảo là luồng rất nhẹ do Java quản lý.':
        'ASR chép “Lùng ảo là lùng trức nhẹ do gia va quản lý.” (0.727): lệch âm/thanh thuần Việt: luồng/lùng, luồng rất/lùng trức — NOT_VERIFIED bằng tai người',
    'A ghi một trăm năm mươi.':
        'ASR chép “Agi 150” (0.727): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: ghi (trong “a ghi” → “agi”) — NOT_VERIFIED bằng tai người',
    'Nhờ vậy mười nghìn luồng ảo cùng chờ cũng không cạn.':
        'ASR chép “Nhờ vảy mươi nghìn luồng ảo cùng chờ cũng không cản.” (0.727): lệch âm/thanh thuần Việt: vậy mười/vảy mươi, cạn/cản — NOT_VERIFIED bằng tai người',
    'Bước hai, vì thứ tự trong từng luồng được giữ, nên số cách xếp bằng số cách chọn hai ô trong bốn ô cho luồng A.':
        'ASR chép “Bước 2, vì thứ tự trong từng luồng được giữ, nền số cắt xếp bằng số cách chọn 2 ô trong 4 ô cho luồng nga.” (0.885): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: nên/nền, cách/cắt — NOT_VERIFIED bằng tai người',
    'Ta theo dõi cách xen kẽ xấu.':
        'ASR chép “Ta theo dõi cách xem kẻ sấu.” (0.714): lệch âm/thanh thuần Việt: xen kẽ/xem kẻ — NOT_VERIFIED bằng tai người',
    'Phép tính thứ ba, B ghi giá trị mà B đã đọc, một trăm, cộng ba mươi, là một trăm ba mươi, và nó đè lên kết quả của A.':
        'ASR chép “Phép tính thứ 3, B ghi giá trị mà B đã đọc, 100 cộng 30 là 130 và nó đề lên kết quả qua.” (0.915): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: đè/đề, của (trong “của a” → “qua”) — NOT_VERIFIED bằng tai người',
    'Phép tính thứ tư, kết quả đúng là một trăm tám mươi, thực tế còn một trăm ba mươi, nên mất đúng năm mươi, chính là khoản nạp của A.':
        'ASR chép “Phép tính thứ 4 kết quả đúng là 180, thực tế còn 130, nên mất đúng 50, chính là khoảng nạp của ai.” (0.933): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: khoản/khoảng — NOT_VERIFIED bằng tai người',
    'Thực ra nó gồm đọc, cộng và ghi, nên luồng khác chen vào được.':
        'ASR chép “Thực ra nó gồm độc, cộng và ghi nên luôn khác chan vào được.” (0.786): lệch âm/thanh thuần Việt: đọc/độc, luồng/luôn, chen/chan — NOT_VERIFIED bằng tai người',
    'Bây giờ tới phần bạn tự làm bài.':
        'ASR chép “Bây giờ tới phần bạn tự lam bay.” (0.75): lệch âm/thanh thuần Việt: làm bài/lam bay — NOT_VERIFIED bằng tai người',
    'Câu ba, dịch vụ gọi đối tác chậm ba trăm mili giây, hàng nghìn yêu cầu cùng lúc, bạn chọn gì?':
        'ASR chép “Câu 3. Dịch vụ gọi đối tác chậm 300 ms. Hàng nghiên yêu cầu cùng lúc. Bạn chọn gì?” (0.878): lệch âm/thanh thuần Việt: mili (trong “mili giây” → “ms”), nghìn/nghiên — NOT_VERIFIED bằng tai người',
    'Đáp án câu hai.':
        'ASR chép “Đập án câu 2.” (0.75): lệch âm/thanh thuần Việt: đáp/đập — NOT_VERIFIED bằng tai người',
    'Nếu chỉ làm một nửa, sổ sách lệch.':
        'ASR chép “Nếu chỉ là một nửa, sổ sách lịch.” (0.75): lệch âm/thanh thuần Việt: làm/là, lệch/lịch — NOT_VERIFIED bằng tai người',
    'Tiêm phụ thuộc là Spring nối các bean với nhau.':
        'ASR chép “Tim phụ thuộc là Espring nối các binh với nhau.” (0.7): lệch âm/thanh thuần Việt: tiêm/tim, spring/espring, bean/binh — NOT_VERIFIED bằng tai người',
    'Hình cho thấy cách Spring nối các bean.':
        'ASR chép “Hình cho thấy cách spring nổi các binh.” (0.75): lệch âm/thanh thuần Việt: nối/nổi, bean/binh — NOT_VERIFIED bằng tai người',
    'Proxy đứng giữa, rồi mới chuyển lời gọi tới bean thật.':
        'ASR chép “Pharoxy đứng giữa, rồi mới chuyển lời gọi tới binh thật.” (0.818): lệch âm/thanh thuần Việt: proxy/pharoxy, bean/binh — NOT_VERIFIED bằng tai người',
    'Proxy làm ba việc.':
        'ASR chép “Heroxy làm ba việc” (0.75): lệch âm/thanh thuần Việt: proxy/heroxy — NOT_VERIFIED bằng tai người',
    'Nhãn giao dịch thật ra chỉ là lời dặn cho proxy, rằng hãy mở trước và đóng sau.':
        'ASR chép “Nhãn giao dịch thật ra chỉ là lời dặn cho Pocsi rằng hãy mở trước và đóng sau.” (0.944): lệch âm/thanh thuần Việt: proxy/pocsi — NOT_VERIFIED bằng tai người',
    'Bây giờ tới phần bạn tự làm bài.':
        'ASR chép “Bây giờ tới phần bạn tự lam bay.” (0.75): lệch âm/thanh thuần Việt: làm bài/lam bay — NOT_VERIFIED bằng tai người',
    'Đáp án câu hai.':
        'ASR chép “Đập án câu 2.” (0.75): lệch âm/thanh thuần Việt: đáp/đập — NOT_VERIFIED bằng tai người',
    'Proxy đọc nhãn rồi mở và đóng giao dịch.':
        'ASR chép “Herdoxy đọc nhãn đồi mở và đóng giao dịch” (0.778): lệch âm/thanh thuần Việt: proxy/herdoxy, rồi/đồi — NOT_VERIFIED bằng tai người',
    'G E T là đọc, không thay đổi gì.':
        'ASR chép “VE-T là độc, không thay đổi gì.” (0.706): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: đọc/độc — NOT_VERIFIED bằng tai người',
    'P O S T là làm một việc mới, mỗi lần gọi có thể làm thêm.':
        'ASR chép “THT là một việc mới, mỗi lần gọi có thể làm thêm.” (0.786): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: làm/∅ — NOT_VERIFIED bằng tai người',
    'Còn P O S T không lũy đẳng, nên cần khoá nếu muốn thử lại an toàn.':
        'ASR chép “Còn P-RST không lụy đẳng, nên cần khóa nếu muốn thử lại an toàn.” (0.812): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: luỹ/luỵ — NOT_VERIFIED bằng tai người',
    'Bây giờ tới phần bạn tự làm bài.':
        'ASR chép “Bây giờ tới phần bạn tự lam bay.” (0.75): lệch âm/thanh thuần Việt: làm bài/lam bay — NOT_VERIFIED bằng tai người',
    'Đáp án câu hai.':
        'ASR chép “Đập án câu 2.” (0.75): lệch âm/thanh thuần Việt: đáp/đập — NOT_VERIFIED bằng tai người',
    'Truy vấn lấy các dòng thoả điều kiện đặt sau mệnh đề điều kiện.':
        'ASR chép “Truy vấn lấy các dòng thỏa điều kiện đặc sâu mạnh để điều kiện.” (0.714): lệch âm/thanh thuần Việt: đặt sau mệnh đề/đặc sâu mạnh để — NOT_VERIFIED bằng tai người',
    'Quét toàn bảng là đọc từng dòng.':
        'ASR chép “Quét toàn bảng là độc từng dông.” (0.714): lệch âm/thanh thuần Việt: đọc/độc, dòng/dông — NOT_VERIFIED bằng tai người',
    'Số tầng rất ít dù số dòng rất lớn.':
        'ASR chép “số từng trất ít dù số dòng rất lớn.” (0.778): lệch âm/thanh thuần Việt: tầng rất/từng trất — NOT_VERIFIED bằng tai người',
    'Bây giờ tới phần bạn tự làm bài.':
        'ASR chép “Bây giờ tới phần bạn tự lam bay.” (0.75): lệch âm/thanh thuần Việt: làm bài/lam bay — NOT_VERIFIED bằng tai người',
    'Đáp án câu hai.':
        'ASR chép “Đập án câu 2.” (0.75): lệch âm/thanh thuần Việt: đáp/đập — NOT_VERIFIED bằng tai người',
    'Oracle phát hiện chuyện này và trả lỗi O R A không không không sáu không cho một trong hai lệnh.':
        'ASR chép “Oracle phát hiện chuyện này và trả lỗi R.A.00060-1 trong hai lệnh.” (0.811): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: không không không/∅, không cho/mươi — NOT_VERIFIED bằng tai người',
    'Cuối cùng, P L S Q L là ngôn ngữ thủ tục của Oracle, chạy ngay trong cơ sở dữ liệu.':
        'ASR chép “Cuối cùng, PLSQL là ngôn ngữ thủ tục của Oracle, chạy ngay trong cơ sở dữ liệu.” (0.842): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Bây giờ tới phần bạn tự làm bài.':
        'ASR chép “Bây giờ tới phần bạn tự lam bay.” (0.75): lệch âm/thanh thuần Việt: làm bài/lam bay — NOT_VERIFIED bằng tai người',
    'Đáp án câu hai.':
        'ASR chép “Đập án câu 2.” (0.75): lệch âm/thanh thuần Việt: đáp/đập — NOT_VERIFIED bằng tai người',
    'Chào bạn, mỗi lần tra số dư mất hai mươi mili giây ở cơ sở dữ liệu.':
        'ASR chép “Chào bạn, mỗi lần tra số dư mất 20ml dây ở cơ sở giữ liệu.” (0.941): lệch âm/thanh thuần Việt: mili/ml — NOT_VERIFIED bằng tai người',
    'Có bộ đệm với tỉ lệ trúng chín mươi phần trăm, trung bình chỉ còn khoảng ba mili giây.':
        'ASR chép “có bộ đềm với tỷ lệ trúng 90%, trung bình chỉ còn khoảng 3 mg.” (0.811): “tỉ” ASR viết chính tả “tỷ” (cùng âm); lệch âm/thanh thuần Việt: đệm/đềm, mili (trong “mili giây” → “mg”) — NOT_VERIFIED bằng tai người',
    'Không phẩy chín cộng không phẩy một bằng một.':
        'ASR chép “Không phải 9 cộng không phải 1 bằng 1.” (0.778): “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải” — NOT_VERIFIED bằng tai người',
    'Trước tiên, dịch vụ sẽ hỏi Redis trước.':
        'ASR chép “Trước tiên, dịch vụ sẽ hỏi Reddit trước.” (0.875): lệch âm/thanh thuần Việt: redis/reddit — NOT_VERIFIED bằng tai người',
    'Nếu trượt thì hỏi tiếp cơ sở dữ liệu, mất thêm hai mươi mili giây, và đó là mười trong một trăm lần.':
        'ASR chép “Nếu trượt thì hỏi tiếp cơ sở dữ liệu, mất thêm 20 ms và đó là 10 trong 100 lần.” (0.933): lệch âm/thanh thuần Việt: mili (trong “mili giây” → “ms”) — NOT_VERIFIED bằng tai người',
    'Phép tính thứ nhất, với h bằng không phẩy chín, T bằng một cộng không phẩy một nhân hai mươi, là ba mili giây.':
        'ASR chép “Phép tính thứ nhất với hát bằng 0,9, tê bằng 1 cộng 0,1 nân 20 là 3 mg.” (0.894): lệch âm/thanh thuần Việt: nhân/nân, mili (trong “mili giây” → “mg”) — NOT_VERIFIED bằng tai người',
    'Phép tính thứ ba, không có bộ đệm, mọi lần đều hỏi cơ sở dữ liệu, nên T bằng hai mươi mili giây.':
        'ASR chép “Phép tính thứ 3, không có bộ đệm, mọi lần đều hỏi cơ sở dữ liệu, nền tê bằng 20 ms.” (0.889): lệch âm/thanh thuần Việt: nên/nền, mili (trong “mili giây” → “ms”) — NOT_VERIFIED bằng tai người',
    'Phép tính thứ tư, nhanh gấp hai mươi chia ba, xấp xỉ sáu phẩy bảy lần.':
        'ASR chép “Phép tính thứ 4, nhành gấp 23, xắp xị 6,7 lần.” (0.774): lệch âm/thanh thuần Việt: nhanh/nhành, chia/∅, xấp xỉ/xắp xị — NOT_VERIFIED bằng tai người',
    'Cộng lại được ba trăm, nên chia một trăm bằng ba mili giây, khớp công thức.':
        'ASR chép “Cộng lại được 300 nên chia 100 bằng 30 li dây khớp công thức.” (0.941): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh — NOT_VERIFIED bằng tai người',
    'Vì phần trượt tốn nhiều nhất, nên từ không phẩy năm lên không phẩy chín chín, độ trễ giảm từ mười một xuống một phẩy hai mili giây.':
        'ASR chép “Vì phần trượt tốn nhiều nhất, nên từ 0,5 lên 0,99, độ trả giảm từ 11 xuống 1,2 ms.” (0.893): lệch âm/thanh thuần Việt: trễ/trả, mili (trong “mili giây” → “ms”) — NOT_VERIFIED bằng tai người',
    'Bộ đệm có thể chứa dữ liệu đã cũ.':
        'ASR chép “Bộ đềm có thể chứa giữ liệu đã cuốn.” (0.778): lệch âm/thanh thuần Việt: đệm/đềm, cũ/cuốn — NOT_VERIFIED bằng tai người',
    'Bây giờ tới phần bạn tự làm bài.':
        'ASR chép “Bây giờ tới phần bạn tự lam bay.” (0.75): lệch âm/thanh thuần Việt: làm bài/lam bay — NOT_VERIFIED bằng tai người',
    'Câu một, thời gian bộ đệm hai mili giây, cơ sở dữ liệu ba mươi mili giây, tỉ lệ trúng không phẩy tám, độ trễ trung bình là bao nhiêu?':
        'ASR chép “Câu 1, thời gian bộ đệm 2mg, cơ sở giữ liệu 30mg, tỷ lệ trúng 0,8, đồ trẻ trung bình là bao nhiêu?” (0.793): “tỉ” ASR viết chính tả “tỷ” (cùng âm); lệch âm/thanh thuần Việt: mili (trong “mili giây” → “mg”), mili (trong “mili giây tỉ” → “mg tỷ”), độ trễ/đồ trẻ — NOT_VERIFIED bằng tai người',
    'Câu ba, có nên dùng khoá Redis để bảo vệ việc trừ tiền không?':
        'ASR chép “Câu 3, có nên dùng khóa trai đích để bảo vệ việc trư tiền không?” (0.828): lệch âm/thanh thuần Việt: redis/trai đích, trừ/trư — NOT_VERIFIED bằng tai người',
    'Đáp án câu hai.':
        'ASR chép “Đập án câu 2.” (0.75): lệch âm/thanh thuần Việt: đáp/đập — NOT_VERIFIED bằng tai người',
    'Chỉ dùng khoá Redis thì nhanh nhưng có thể trừ trùng.':
        'ASR chép “Chỉ dùng khóa ra đích thì nhanh nhưng có thể trừ trung.” (0.783): lệch âm/thanh thuần Việt: redis/ra đích, trùng/trung — NOT_VERIFIED bằng tai người',
    'Hỏi bộ đệm trước, độ trễ trung bình là thời gian bộ đệm cộng tỉ lệ trượt nhân thời gian cơ sở dữ liệu.':
        'ASR chép “Hỏi bộ đềm trước. Đồ trễ trung bình là thời gian bộ đềm cộng tỷ lệ trực nhân thời gian cơ sở dữ liệu.” (0.792): “tỉ” ASR viết chính tả “tỷ” (cùng âm); lệch âm/thanh thuần Việt: đệm/đềm, độ/đồ, đệm/đềm, trượt/trực — NOT_VERIFIED bằng tai người',
    'Kiểm phép chia dư.':
        'ASR chép “Kiểm phép chi dư.” (0.75): lệch âm/thanh thuần Việt: chia/chi — NOT_VERIFIED bằng tai người',
    'Làm thử, khoá T K một không không một hai lần đều vào phân vùng một.':
        'ASR chép “Làm thử, khóa TK10012 lần đều vào phân vùng 1.” (0.788): lệch âm/thanh thuần Việt: một/mười nghìn, không một/trăm mười — NOT_VERIFIED bằng tai người',
    'Quá số phân vùng thì các bộ đọc thừa ngồi không.':
        'ASR chép “Quả số phân vùng thì các bộ độc thương ngồi không?” (0.727): lệch âm/thanh thuần Việt: quá/quả, đọc thừa/độc thương — NOT_VERIFIED bằng tai người',
    'Lỗi thứ ba, cũng của người đã đi làm, là nghe đúng một lần của Kafka rồi tin mọi tác dụng phụ chỉ xảy ra một lần.':
        'ASR chép “Lỗi thứ ba, cũng của người đã đi làm là nghe đúng một lần của kắp ca rồi tin mọi tác dụng phụ chỉ xảy ra một lần.” (0.964): lệch âm/thanh thuần Việt: cáp/kắp — NOT_VERIFIED bằng tai người',
    'Bây giờ tới phần bạn tự làm bài.':
        'ASR chép “Bây giờ tới phần bạn tự lam bay.” (0.75): lệch âm/thanh thuần Việt: làm bài/lam bay — NOT_VERIFIED bằng tai người',
    'Đáp án câu hai.':
        'ASR chép “Đập án câu 2.” (0.75): lệch âm/thanh thuần Việt: đáp/đập — NOT_VERIFIED bằng tai người',
    'Đừng hỏi Kafka có đúng một lần không.':
        'ASR chép “Đừng hỏi cắp ca có đúng một lần không?” (0.889): lệch âm/thanh thuần Việt: cáp/cắp — NOT_VERIFIED bằng tai người',
    'SAGA là chuỗi giao dịch cục bộ, mỗi bước có bước bù để quay lui.':
        'ASR chép “Saga là chủ giao dịch cục bộ, mỗi bước có bước bù để quay lui.” (0.933): lệch âm/thanh thuần Việt: chuỗi/chủ — NOT_VERIFIED bằng tai người',
    'Rồi một bộ chuyển tiếp đọc bảng Outbox và gửi sang Kafka, kể cả khi dịch vụ đã sập và chạy lại.':
        'ASR chép “Rồi một bộ chuyển tiếp đọc bản Au Bốc và gửi sang Kafka kể cả khi dịch vụ đã sập và chạy lại.” (0.889): lệch âm/thanh thuần Việt: bảng outbox/bản au bốc — NOT_VERIFIED bằng tai người',
    'Không có Outbox thì không sự kiện nào được phát.':
        'ASR chép “Không có áo bốc thì không sự kiện nào được phát.” (0.909): lệch âm/thanh thuần Việt: ao/áo — NOT_VERIFIED bằng tai người',
    'Tưởng SAGA cho tính cô lập như giao dịch thường.':
        'ASR chép “Tưởng Saga cho tính cô lập như giao dịch thương.” (0.9): lệch âm/thanh thuần Việt: thường/thương — NOT_VERIFIED bằng tai người',
    'Lưu cơ sở dữ liệu rồi gửi Kafka thành hai lệnh riêng.':
        'ASR chép “Lưu cơ sở dữ liệu rồi gửi káp ca thành hai lệnh riêng.” (0.923): lệch âm/thanh thuần Việt: cáp/káp — NOT_VERIFIED bằng tai người',
    'Bây giờ tới phần bạn tự làm bài.':
        'ASR chép “Bây giờ tới phần bạn tự lam bay.” (0.75): lệch âm/thanh thuần Việt: làm bài/lam bay — NOT_VERIFIED bằng tai người',
    'Câu hai, bước bù chạy theo thứ tự nào?':
        'ASR chép “Câu 2. Bước buồn chạy theo thứ tử nào” (0.778): lệch âm/thanh thuần Việt: bù/buồn, tự/tử — NOT_VERIFIED bằng tai người',
    'Đáp án câu hai.':
        'ASR chép “Đập án câu 2.” (0.75): lệch âm/thanh thuần Việt: đáp/đập — NOT_VERIFIED bằng tai người',
    'Bây giờ tới phần bạn tự làm bài.':
        'ASR chép “Bây giờ tới phần bạn tự lam bay.” (0.75): lệch âm/thanh thuần Việt: làm bài/lam bay — NOT_VERIFIED bằng tai người',
    'Đáp án câu hai.':
        'ASR chép “Đập án câu 2.” (0.75): lệch âm/thanh thuần Việt: đáp/đập — NOT_VERIFIED bằng tai người',
    'OFS là bản tin dạng chữ để gọi chức năng của lõi từ bên ngoài.':
        'ASR chép “OSS là bản tin dạng chữ để gọi chức năng của lỗi từ bên ngoài.” (0.867): lệch âm/thanh thuần Việt: ofs/oss, lõi/lỗi — NOT_VERIFIED bằng tai người',
    'Bây giờ tới phần bạn tự làm bài.':
        'ASR chép “Bây giờ tới phần bạn tự lam bay.” (0.75): lệch âm/thanh thuần Việt: làm bài/lam bay — NOT_VERIFIED bằng tai người',
    'Đáp án câu hai.':
        'ASR chép “Đập án câu 2.” (0.75): lệch âm/thanh thuần Việt: đáp/đập — NOT_VERIFIED bằng tai người',
    'Lưu ý, mỗi mạng thanh toán có đặc tả riêng, kể cả NAPAS.':
        'ASR chép “Lưu ý, mỗi mạng thanh toán có đặc tả riêng kể cả Na Phát.” (0.929): lệch âm/thanh thuần Việt: pát/phát — NOT_VERIFIED bằng tai người',
    'Thập lục phân có mười sáu chữ số, từ không tới chín rồi A tới F, và mỗi chữ số tương ứng bốn bit.':
        'ASR chép “Thập lục phân có 16 triệu số, từ 0 tới 9 rồi A tới S và mỗi triệu số tương ứng 4 bit.” (0.875): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: chữ/triệu, chữ/triệu — NOT_VERIFIED bằng tai người',
    'D E là một trường dữ liệu, đánh số hai, ba, bốn.':
        'ASR chép “V-E là một trường dữ liệu, đánh số 2, 3, 4.” (0.917): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Cuối cùng, STAN là trường mười một, RRN là trường ba mươi bảy.':
        'ASR chép “Cuối cùng, Xtang là trường 11, RRN là trường 37.” (0.923): lệch âm/thanh thuần Việt: stan/xtang — NOT_VERIFIED bằng tai người',
    'Chỉ bit mười một bật, nên là không không một không, không không không không, tức thập lục phân hai không.':
        'ASR chép “Chỉ biết 11 bật, nên là 0010 0000 tức thập lụt phân 2-0.” (0.667): lệch âm/thanh thuần Việt: bit/biết, không không một không không không không/mười, lục/lụt — NOT_VERIFIED bằng tai người',
    'Kết quả là bảy không hai không, rồi các chữ số không.':
        'ASR chép “Kết quả là 7020, rồi cắt chữ số 0.” (0.769): lệch âm/thanh thuần Việt: không/mươi, các/cắt — NOT_VERIFIED bằng tai người',
    'Cùng chuẩn nhưng mỗi mạng có đặc tả riêng, gồm trường nào dùng, độ dài, bảng mã ký tự.':
        'ASR chép “Cùng chuẩn nhưng mỗi mạng có đặc tả tiên, gồm trường nào dùng, đồ dài, bản mạ ký tự.” (0.789): lệch âm/thanh thuần Việt: riêng/tiên, độ/đồ, bảng mã/bản mạ — NOT_VERIFIED bằng tai người',
    'Bây giờ tới phần bạn tự làm bài.':
        'ASR chép “Bây giờ tới phần bạn tự lam bay.” (0.75): lệch âm/thanh thuần Việt: làm bài/lam bay — NOT_VERIFIED bằng tai người',
    'Khúc đầu có bit ba và bốn bật, nên là không không một một, không không không không, tức ba không.':
        'ASR chép “Khúc đầu có biết 3 và 4 bật, nền là 0011 0000, tức 3 không.” (0.703): lệch âm/thanh thuần Việt: bit/biết, nên/nền, không không/mười, một không không không/∅ — NOT_VERIFIED bằng tai người',
    'Đáp án câu hai.':
        'ASR chép “Đập án câu 2.” (0.75): lệch âm/thanh thuần Việt: đáp/đập — NOT_VERIFIED bằng tai người',
    'Chi tiết của NAPAS nằm trong đặc tả kết nối chính thức của họ.':
        'ASR chép “Chi tiết của NAPAC nằm trong đặc tạ kết nối chính thức của họ.” (0.857): lệch âm/thanh thuần Việt: napas/napac, tả/tạ — NOT_VERIFIED bằng tai người',
    'Lệch tiền là cả hai có nhưng tiền khác.':
        'ASR chép “Lời tiền là cả hai có những tiền khác.” (0.778): lệch âm/thanh thuần Việt: lệch/lời, nhưng/những — NOT_VERIFIED bằng tai người',
    'Chênh lệch là một trăm năm mươi.':
        'ASR chép “Chín lịch là 150.” (0.714): lệch âm/thanh thuần Việt: chênh lệch/chín lịch — NOT_VERIFIED bằng tai người',
    'Bây giờ tới phần bạn tự làm bài.':
        'ASR chép “Bây giờ tới phần bạn tự lam bay.” (0.75): lệch âm/thanh thuần Việt: làm bài/lam bay — NOT_VERIFIED bằng tai người',
    'A hai lệch tiền, hai mươi khác hai mươi lăm.':
        'ASR chép “À hai lệch tiền, hai mươi khác hai mươi lăm.” (0.9): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Đáp án câu hai.':
        'ASR chép “Đập án câu 2.” (0.75): lệch âm/thanh thuần Việt: đáp/đập — NOT_VERIFIED bằng tai người',
    'Không một một một XOR không một không một bằng không không một không.':
        'ASR chép “0111XOA 01001 bằng 01001.” (0.556): lệch âm/thanh thuần Việt: không/∅, một/trăm mười, một không/trăm linh, không/trăm linh, không/∅ — NOT_VERIFIED bằng tai người',
    'MAC là mã xác thực bản tin.':
        'ASR chép “mac là mả sát thực bản tin.” (0.778): lệch âm/thanh thuần Việt: mã xác/mả sát — NOT_VERIFIED bằng tai người',
    'PIN rõ chỉ tồn tại ở hai đầu, trong phần cứng bảo vệ.':
        'ASR chép “Pim rõ chỉ tồn tại ở hai đầu trong phần cứng bảo vệ.” (0.923): lệch âm/thanh thuần Việt: pin/pim — NOT_VERIFIED bằng tai người',
    'Phép tính thứ hai, hai byte đầu XOR với không nên giữ nguyên là không bốn và một hai.':
        'ASR chép “Phép tính thứ 2, hai bay đầu ít OA với không nên giữ nguyên là 04 và 102.” (0.884): lệch âm/thanh thuần Việt: bai/bay, không/∅ — NOT_VERIFIED bằng tai người',
    'Phép tính thứ ba, F F XOR một một cho E E, và lặp lại năm lần ở các byte còn lại.':
        'ASR chép “Phép tính thứ 3 FFXOA11 cho FFXOA11 và lặp lại 5 lần ở các bay còn lại.” (0.698): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: xor một (trong “f f xor một” → “ffxoa mười”) — NOT_VERIFIED bằng tai người',
    'Phép tính thứ tư, ghép lại, khối PIN là không bốn một hai hai năm rồi năm cặp E E.':
        'ASR chép “Phép tính thứ 4, ghép lại, khối pin là 041 225 rồi 5 cặp Ê.” (0.829): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: không/∅ — NOT_VERIFIED bằng tai người',
    'Bây giờ tới phần bạn tự làm bài.':
        'ASR chép “Bây giờ tới phần bạn tự lam bay.” (0.75): lệch âm/thanh thuần Việt: làm bài/lam bay — NOT_VERIFIED bằng tai người',
    'Đáp án câu hai.':
        'ASR chép “Đập án câu 2.” (0.75): lệch âm/thanh thuần Việt: đáp/đập — NOT_VERIFIED bằng tai người',
    'MAC phát hiện bản tin bị sửa.':
        'ASR chép “M à sẽ phát hiện bản tin bị sửa.” (0.778): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Bây giờ tới phần bạn tự làm bài.':
        'ASR chép “Bây giờ tới phần bạn tự lam bay.” (0.75): lệch âm/thanh thuần Việt: làm bài/lam bay — NOT_VERIFIED bằng tai người',
    'Câu ba là bài tập, viết bốn câu S T A R cho một sự cố thật của bạn.':
        'ASR chép “Câu 3 là bài tập, viết 4 câu S T, E R cho một sự cố thật của bạn.” (0.947): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Đáp án câu hai.':
        'ASR chép “Đập án câu 2.” (0.75): lệch âm/thanh thuần Việt: đáp/đập — NOT_VERIFIED bằng tai người',
    'Câu ba là bài của riêng bạn, nên bài này không bịa hộ bạn.':
        'ASR chép “Câu 3 là bài của thiên bản, nên bài này không bị hộ bản.” (0.714): lệch âm/thanh thuần Việt: riêng bạn/thiên bản, bịa/bị, bạn/bản — NOT_VERIFIED bằng tai người',
    # ── INT rà soát nội dung (2026-11-08) ──
    'Mời bạn tính toán gói thu nhập: Với mức lương 50 triệu gross một tháng, lương tháng 13 cố định và thưởng từ 1 đến 4 tháng, gói thu nhập một năm nằm trong khoảng nào?':
        'ASR chép “Mời bạn tính toán gói thu nhập. Với mức lương 50 triệu gờ rốt 1 tháng, lương tháng 13 cố định và thưởng từ 1 đến 4 tháng, gói thu nhập 1 năm nằm trong khoảng nào?” (0.974): lệch âm/thanh thuần Việt: gơ/gờ — NOT_VERIFIED bằng tai người',
    'Bước một, nếu dùng luồng truyền thống, mười nghìn luồng dự trữ tới khoảng mười gigabyte không gian ngăn xếp.':
        'ASR chép “Bước một, nếu dùng luồng truyền thống, 10.000 luồng dự trữ tới khoảng 10GB không gian ngăn xếp.” (0.95): lệch âm/thanh thuần Việt: gigabyte/gb — NOT_VERIFIED bằng tai người',
    'Bước hai, với luồng ảo, nếu giả định mỗi luồng tốn khoảng hai nghìn byte thì mười nghìn luồng cần khoảng hai mươi megabyte trên bộ nhớ động.':
        'ASR chép “Bước 2, với luồng đảo, nếu giả định mỗi luồng tốn khoảng 2.000 bai thì 10.000 luồng cần khoảng 20 MB trên bộ nhớ động.” (0.897): “mê-ga-…” đọc tách âm tiết (đã dựng ở NET), ASR viết dạng gộp; lệch âm/thanh thuần Việt: ảo/đảo, bai (trong “mê ga bai” → “mb”) — NOT_VERIFIED bằng tai người',
    'Khi trình bày trung thực nền tảng này ở mức nguyên mẫu học thuật, bạn có lý do rõ ràng để đề xuất mức lương 50 triệu gross tại ACB.':
        'ASR chép “Khi trình bày trung thực nền tảng này ở mức nguyên mẫu học thuật, bạn có lý do rõ ràng để đề xuất mức lương 50 triệu GROC tại ACB.” (0.968): lệch âm/thanh thuần Việt: gross/groc — NOT_VERIFIED bằng tai người',
    # ── ACB rà soát nội dung (2026-11-08) ──
    'Bạn là Chuyên viên chính trong nhóm tín dụng tại OCB, phối hợp với đội vận hành Core T24 và NAPAS, và đang học Cử nhân AI tại trường UIT.':
        'ASR chép “Bạn là chuyên viên chính trong nhóm tín dụng tại OCB, phối hợp với đội vận hành COTE24 và NAPAC và đang học cử nhân AI tại trường UIT.” (0.923): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: core (trong “core t” → “cote”), napas/napac — NOT_VERIFIED bằng tai người',
    'Hôm nay ta cùng phân tích sâu bản chất kỹ thuật: cấu trúc bản tin OFS, cơ chế gửi nhận bất đồng bộ qua IBM MQ, và giải pháp xử lý timeout chuẩn Senior.':
        'ASR chép “Hôm nay ta cùng phân tích sau bản chất kỹ thuật, cấu trúc bản tin OFS, cơ chế gửi nhận bớt đồng bộ qua eBay MMQ và giải pháp xử lý timeout chuẩn senior.” (0.882): lệch âm/thanh thuần Việt: sâu/sau, bất/bớt, ibm mq/ebay mmq — NOT_VERIFIED bằng tai người',
    'Sau đó là người dùng kết nối, rồi mã giao dịch để trống cho Core tự sinh.':
        'ASR chép “Sau đó là người dùng kết nối, rồi mãi giao dịch để trống cho con tự sinh.” (0.882): lệch âm/thanh thuần Việt: mã/mãi, core/con — NOT_VERIFIED bằng tai người',
    'Mỗi giao dịch được đóng gói theo đặc tả kết nối của NAPAS, có gốc từ chuẩn ISO 8583, và gửi qua đường truyền TCP chuyên dụng.':
        'ASR chép “Mỗi giao dịch được đóng gói theo đặc tạ kết nối của NAPAC, có gốc tự chuẩn ISO 8583 và gửi qua đường truyền t cp chuyên dụng.” (0.907): NAPAS đọc “na pát” theo lexicon INT/ACB, ASR viết “NAPAC” (cùng nhóm với các câu NAPAS đã xem xét 2026-11-07); TCP đọc tên chữ cái, ASR viết “t cp”; lệch âm/thanh thuần Việt: tả/tạ, từ/tự — NOT_VERIFIED bằng tai người',
    'Trường số ba là mã xử lý cho biết loại nghiệp vụ, mã cụ thể cần kiểm với đặc tả kết nối của NAPAS.':
        'ASR chép “Trường số 3 là mã xử lý cho biết loại nhiệp vụ mà cụ thể cần kiểm với đặc tạ kết nối của NAPAC.” (0.833): lệch âm/thanh thuần Việt: nghiệp/nhiệp, mã/mà, tả/tạ, napas/napac — NOT_VERIFIED bằng tai người',
    'Điểm khớp vượt ngưỡng cấu hình nên hệ thống kết luận trùng khớp.':
        'ASR chép “Điểm khắp vượt ngưỡng cấu hình nên hệ thống kết luận trung khắp.” (0.769): lệch âm/thanh thuần Việt: khớp/khắp, trùng khớp/trung khắp — NOT_VERIFIED bằng tai người',
    # ── BNK, DSY, EVT dựng lại sau rà soát toàn bộ (2026-11-08) ──
    'D trỏ tới E, nhưng cả hai không có đường từ gốc.':
        'ASR chép “Ve trỏ tới e, nhưng cả hai không có đường từ gốc.” (0.917): chữ cái D đứng riêng đọc tên kiểu Việt “đê”, ASR viết “Ve”; phần còn lại khớp — NOT_VERIFIED bằng tai người',
    'Còn luồng nền là luồng thật của hệ điều hành, và luồng ảo chạy nhờ trên nó.':
        'ASR chép “Con luôn nên là luôn thật của hệ điều hành, và luôn áo chạy nhờ trên nó.” (0.647): lệch âm/thanh thuần Việt: còn/con, luồng/luôn (cả ba lần), nền/nên, ảo/áo; trật tự từ và số từ khớp đủ, không có dấu hiệu âm thanh cụt — NOT_VERIFIED bằng tai người',
    'Trong kế hoạch của Oracle, hai cách này mang tên khác, ghi trong ngoặc trên màn hình.':
        'ASR chép “Trong kế hoạch của ORACON, hai cách này mang tên khác, ghi trong hoặc trên màn hình.” (0.882): tên riêng tiếng Anh Oracle đọc thô, ASR viết “ORACON”; lệch âm thuần Việt ngoặc/hoặc — NOT_VERIFIED bằng tai người',
    'Oracle có cách quét nhảy qua cột đầu khi cột đầu ít giá trị khác nhau, nhưng thường kém hơn chỉ mục đúng thứ tự.':
        'ASR chép “Oraken có cách quét nhảy qua cột đầu khi cột đầu ít giá trị khác nhau, nhưng thường kém hơn chỉ một đúng thứ tự.” (0.92): tên riêng tiếng Anh Oracle đọc thô, ASR viết “Oraken”; lệch âm thuần Việt mục/một — NOT_VERIFIED bằng tai người',
    'Nhiều mạng gửi bản đồ ở dạng nhị phân tám byte, chứ không phải mười sáu ký tự.':
        'ASR chép “Nhiều mạng gửi bản đồ ở dạng nhì phân tám bay chứ không phải mười sáu ký tự.” (0.889): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch thanh thuần Việt nhị/nhì — NOT_VERIFIED bằng tai người',
    'Ghi xong khi W bản xác nhận, đọc thì hỏi R bản, và nếu R cộng W lớn hơn N thì tập đọc luôn có ít nhất một bản giữ lần ghi đã hoàn tất mới nhất.':
        'ASR chép “Ghi xong khi v-dup bảng xác nhận, đọc thì hỏi R bảng, và nếu R cộng v-dup lớn hơn N thì tập đọc luôn có ít nhất một bảng giữ lần ghi đã hoàn tất mới nhất.” (0.842): W đọc tên chữ cái “vê đúp”, ASR viết “v-dup” (đã chấp nhận ở các khoá trước); lệch thanh thuần Việt bản/bảng (ba lần) — NOT_VERIFIED bằng tai người',
    'Vì vậy bản mới viết trên máy chậm đồng hồ trông cũ hơn.':
        'ASR chép “Vì vậy bạn mới viết trên máy chậm đồng hồ trong củ hơn.” (0.769): lệch thanh thuần Việt bản/bạn, trông/trong, cũ/củ; số từ khớp đủ — NOT_VERIFIED bằng tai người',
    # ── JVA L00–L03 dựng lần đầu (2026-11-08) ──
    'Bên trái là tệp mã nguồn bạn gõ.':
        'ASR chép “Bên trái là tạp mãn nguồn bạng gõ.” (0.625): lệch âm/thanh thuần Việt tệp/tạp, mã/mãn, bạn/bạng; đủ 8 từ, không cụt — NOT_VERIFIED bằng tai người',
    'Lớp tên Chao nhưng lưu trong một tệp tên khác.':
        'ASR chép “Lớp tên trao nhân lưu trong một tạp tên khác.” (0.7): tên lớp Chao (từ Việt) ASR viết “trao”; lệch âm thuần Việt nhưng/nhân, tệp/tạp; đủ từ — NOT_VERIFIED bằng tai người',
    'Kết quả chạy có năm dòng, khớp.':
        'ASR chép “Cứ quả chạy có 5 dòng, khứt.” (0.714): lệch âm thuần Việt kết/cứ, khớp/khứt; số “năm” ASR viết 5 (đúng) — NOT_VERIFIED bằng tai người',
    'Đáp án như sau.':
        'ASR chép “Đáp ản như sau” (0.75): lệch thanh thuần Việt án/ản; câu chuyển ý ngắn, đủ từ — NOT_VERIFIED bằng tai người',
    'Đây là chương trình đầu tiên, nằm trong tệp tên là Chao chấm Java.':
        'ASR chép “Đây là chương trình đầu tiên nằm trong tạp tên là www.chao.java” (0.857): tên tệp Chao chấm Java ASR viết dạng tên tệp “chao.java” (chấm → dấu chấm, “www” là ASR tự thêm); lệch tệp/tạp — NOT_VERIFIED bằng tai người',
    'Sau đó máy ảo Java, viết tắt JVM, nạp tệp mã bai và chạy từng lệnh, rồi kết quả hiện ra màn hình.':
        'ASR chép “Sau đó máy ảo Java viết tắt GVM nạp tẹp mã bay và chạy từng lệnh, rồi kết quả hiện ra màn hình.” (0.87): JVM đọc theo lexicon, ASR viết “GVM”; “mã bai” (bytecode) ASR viết “bay” (cùng nhóm byte → “bay”, probe CSA p1 8/8); lệch tệp/tẹp — NOT_VERIFIED bằng tai người',
    'Trình biên dịch từ chối ngay, và báo rằng lớp Chao phải nằm trong tệp tên Chao chấm Java.':
        'ASR chép “Trình biên dịch từ chối ngay và báo rằng lớp chao phải nằm trong tạp tên chao.java.” (0.919): tên tệp ASR viết “chao.java” (chấm → dấu chấm); lệch tệp/tạp — NOT_VERIFIED bằng tai người',
    'Phép gán tính vế phải rồi ghi đè.':
        'ASR chép “Phép gãng tính vế phải rồi ghi đây.” (0.75): lệch âm/thanh thuần Việt gán/gãng, đè/đây; đủ 8 từ — NOT_VERIFIED bằng tai người',
    'Theo luật của Java, máy bỏ phần tràn, chỉ giữ ba mươi hai ô.':
        'ASR chép “Theo luật của Java, máy bỏ phần tràn chỉ giữ 32 ohm.” (0.929): “ô” (ô nhớ/bit) ASR viết “ohm”; số ba mươi hai ASR viết 32 (đúng) — NOT_VERIFIED bằng tai người',
    'Phép hoặc cũng vậy, vế trái đúng thì dừng.':
        'ASR chép “Phép hoặc cũng vậy, vệ trái đúng thi dưng.” (0.667): lệch thanh thuần Việt vế/vệ, thì/thi, dừng/dưng; đủ từ — NOT_VERIFIED bằng tai người',
    'Dấu chấm than đảo đúng thành sai.':
        'ASR chép “dấu chấm thang đạo đúng thành sai” (0.714): lệch âm/thanh thuần Việt than/thang, đảo/đạo; đủ 7 từ — NOT_VERIFIED bằng tai người',
    'Đáp án dòng một.':
        'ASR chép “Đáp án dòng mục” (0.75): lệch âm thuần Việt một/mục ở cuối câu; đủ từ — NOT_VERIFIED bằng tai người',
    'Dòng hai ép a thành số thực rồi chia.':
        'ASR chép “Dòng 2FA thành số thực rồi chia.” (0.824): “ép a” (ép kiểu biến a) ASR gộp thành “FA”; số hai ASR viết 2 (đúng) — NOT_VERIFIED bằng tai người',
    'Chuỗi rẽ nhánh xếp hạng bạc, vàng hoặc thường.':
        'ASR chép “Chủi trẻ nhánh xếp hạng bạc, vàng hoặc thương” (0.667): lệch âm/thanh thuần Việt chuỗi/chủi, rẽ/trẻ, thường/thương; đủ từ — NOT_VERIFIED bằng tai người',
    'Ví dụ rút tiền.':
        'ASR chép “Ví dụ trúc tiền.” (0.75): lệch âm thuần Việt rút/trúc; câu chuyển ý ngắn, đủ từ — NOT_VERIFIED bằng tai người',
    # ── JVA L04–L12 dựng lần đầu (2026-11-08) ──
    'Tìm phần lặp lại để làm thân vòng lặp.':
        'ASR chép “Tìm phần lập lại để làm thân vòng lập.” (0.778): lệch thanh thuần Việt lặp/lập (hai lần); đủ từ — NOT_VERIFIED bằng tai người',
    'Bước bốn, suy ra vòng lặp duyệt mảng.':
        'ASR chép “Bước bốn, suy ra vòng lập diệt mãn.” (0.625): lệch âm/thanh thuần Việt lặp/lập, duyệt/diệt, mảng/mãn; đủ 8 từ, không cụt — NOT_VERIFIED bằng tai người',
    'Bước ba, sắp xếp.':
        'ASR chép “Bước 3, chắp xếp” (0.75): lệch âm thuần Việt sắp/chắp; số ba ASR viết 3 (đúng); câu đề mục ngắn — NOT_VERIFIED bằng tai người',
    'Với mảng, bản sao là mũi tên tham chiếu, nên hai tên cùng trỏ vào một mảng, và hàm đổi được các ô.':
        'ASR chép “Với mảng, bảng sao là mũi tên tham chiếu, nên hai tên cùng trỏ vào một mảng và hàm đổi được các cô.” (0.913): lệch thanh thuần Việt bản/bảng, ô/cô — NOT_VERIFIED bằng tai người',
    'Cách sửa là để trường riêng tư.':
        'ASR chép “Các sửa là đẩy trường riêng tư.” (0.714): lệch âm/thanh thuần Việt cách/các, để/đẩy; đủ 7 từ — NOT_VERIFIED bằng tai người',
    'Chuỗi là dãy ký tự đánh chỉ số từ không.':
        'ASR chép “Chủy là dạy ký tự đánh chi số tư không?” (0.6): lệch thanh thuần Việt chuỗi/chủy, dãy/dạy, chỉ/chi, từ/tư; đủ 10 từ, không cụt; nội dung (chỉ số bắt đầu từ 0) có trên màn hình — NOT_VERIFIED bằng tai người',
    'Phép tính thứ năm, hàm định dạng với mẫu phần trăm, dấu phẩy, chữ d chèn dấu phân cách hàng nghìn.':
        'ASR chép “Phép tính thứ 5, hàm định dạng với mẫu phần trăm, giấu phẩy, chữ G chàng giấu phân cách hàng nghìn.” (0.905): chữ cái d đọc tên kiểu Việt, ASR viết “G”; lệch dấu/giấu, chèn/chàng — NOT_VERIFIED bằng tai người',
    'Phép nối cũng tạo chuỗi mới, rồi biến s trỏ sang nó.':
        'ASR chép “Phép nối cũng tạo chuỗi mới, rồi biến ép trỏ sang nó.” (0.917): tên biến s đọc tên chữ cái “ét”, ASR viết “ép” — NOT_VERIFIED bằng tai người',
    'Và đừng xoá phần tử trong vòng lặp duyệt.':
        'ASR chép “và đừng xóa phần tử trong vòng lập duy.” (0.778): lệch thanh thuần Việt lặp/lập, duyệt/duy; “xoá/xóa” chỉ khác vị trí dấu — NOT_VERIFIED bằng tai người',
    'Phép tính thứ nhất in bản ghi a.':
        'ASR chép “Phép tính thứ nhất in bản Gia.” (0.8): “ghi a” (bản ghi tên a) ASR gộp thành “Gia”; đủ từ — NOT_VERIFIED bằng tai người',
    'Lệnh ba nằm đúng biên: một triệu không lớn hơn một triệu, nên được chuyển, A về không, C thành hai triệu rưỡi.':
        'ASR chép “Lệnh 3 nằm đúng biên, 1 triệu không lớn hơn 1 triệu nên được chuyển A về 0 sẽ thành 2 triệu rưỡi.” (0.957): tên tài khoản C đọc “xê”, ASR viết “sẽ”; số ASR viết dạng chữ số (đúng) — NOT_VERIFIED bằng tai người',
    # ── CLD, CSA, DBS, DEN dựng lại sau rà soát toàn bộ (2026-11-08) ──
    'Nếu không có cả yêu cầu lẫn giới hạn, bộ xếp lịch coi Pod cần 0 tài nguyên và nhồi quá nhiều Pod vào một nút.':
        'ASR chép “Nếu không có cả yêu cầu lẫn giới hạn, bộ xếp lịch coi pốt cần không tài nguyên và nhồi quá nhiều pốt vào một nút.” (0.923): Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút) — NOT_VERIFIED bằng tai người',
    'Cờ C bật khi có nhớ ra khỏi bit cao nhất, báo tràn số không dấu khi cộng.':
        'ASR chép “CC bật khi có nhớ ra khỏi biết cao nhất, bảo trạng số không giấu khi cộng.” (0.743): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: cờ (trong “cờ c” → “cc”), bit/biết, báo tràn/bảo trạng — NOT_VERIFIED bằng tai người',
    'Bộ nhớ đệm gồm vài tầng, từ vài chục nghìn đến vài chục triệu byte, mất từ một tới vài chục na-nô giây.':
        'ASR chép “Bộ nhớ đệm gồm vài tân, từ vài chục nghiên đến vài chục triệu bai, mất từ một tới vài chục nano-gay.” (0.766): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; lệch âm/thanh thuần Việt: tầng/tân, nghìn/nghiên — NOT_VERIFIED bằng tai người',
    'Cỡ trang tuỳ hệ, thường từ 4 tới 16 ki-lô-byte, bài này lấy 8 ki-lô-byte.':
        'ASR chép “Cở trang tùy hệ, thường từ 4 tới 16 kilobytes, bài này lấy 8 kilobytes.” (0.722): KB đọc “ki-lô-byte” theo lexicon của khoá, ASR viết “kilobyte/kg”; lệch âm/thanh thuần Việt: cỡ/cở — NOT_VERIFIED bằng tai người',
    'Ở hệ cơ sở dữ liệu văn bản mà bài lấy làm ví dụ, một văn bản tối đa 16 MiB, tức 16 nhân 2 mũ 20, bằng 16777216 byte, còn hệ khác có trần khác.':
        'ASR chép “Ở hệ cơ sở dữ liệu văn bản mà bài lấy làm ví dụ, một văn bản tối đa 16 MB, tức 16 nhân 2 mũ 20 bằng 16777216B, còn hệ khác có trần khác.” (0.961): MiB đọc “mê-ga-byte” (quy ước OSY/DEN: cách nói thông dụng, màn hình giữ MiB, câu nêu rõ 2 mũ 20), ASR viết “MB”; byte đọc thô, ASR viết dạng chữ số “16777216B” (đúng giá trị) — NOT_VERIFIED bằng tai người',
    # ── DSY, OSY, SWF dựng lại sau rà soát toàn bộ (2026-11-08) ──
    'Một tỉ địa chỉ, mỗi địa chỉ khoảng 50 byte, tổng cộng 50 ghi-ga-byte, quá tốn nếu chỉ để trả lời đã thấy chưa.':
        'ASR chép “Một tỷ địa chỉ, mỗi địa chỉ khoảng 50 byte, tổng cộng 50 GB. Quá tốn nếu chỉ để trả lời đã thấy chưa.” (0.889): “tỉ” ASR viết chính tả “tỷ” (cùng âm); GB đọc “ghi-ga-byte” theo lexicon của khoá, ASR viết “GB/gigabyte” — NOT_VERIFIED bằng tai người',
    'Phải chép hàng trăm triệu byte, và chương trình bị dời phải dừng trong lúc chép.':
        'ASR chép “Phải chép hàng trăm triệu bay và chương trình bị dời phải dừng trong lúc chép.” (0.938): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Trước vòng i bằng 1, s mới là 0 mà công thức đã cho 1, và nếu tin công thức thì khi dừng nó cho thừa n so với tổng thật.':
        'ASR chép “Trước vòng y bằng 1, f mới là 0 mà công thức đã cho 1, và nếu tin công thức thì khi dừng nó cho thừa n so với tổng thật.” (0.968): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Trong tấn công thật, phần tràn ghi đè địa chỉ mà hàm sẽ quay về khi xong, nên máy nhảy tới các byte do kẻ tấn công đưa vào và chạy chúng như mã.':
        'ASR chép “Trong tấn công thật, phần trang ghi đề địa chỉ mà hàm sẽ quay về khi xong, nên máy nhảy tới các bay do kẻ tấn công đưa vào và chạy chúng như mã.” (0.912): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: tràn/trang, đè/đề — NOT_VERIFIED bằng tai người',
    # ── AIF dựng lại sau rà soát đợt B (2026-11-09) ──
    'Khi cả hai chấp nhận được, A sao dùng hàm trội không mở nhiều nút hơn, trừ chênh lệch nhỏ do cách phá hoà như ở bài 2.':
        'ASR chép “Khi cả hai chấp nhận được, à sao dùng hàm trội không mở nhiều nút hơn, trừ chênh lệch nhỏ do cách phá hòa như ở bài 2.” (0.964): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    # ── BCH dựng lại sau rà soát đợt B (2026-11-09) ──
    'Trên chuỗi chỉ còn vài byte mỗi giao dịch, cộng bằng chứng hay thời hạn phản đối cho cả lô.':
        'ASR chép “Trên chuỗi chỉ còn vài bay mỗi giao dịch, cộng bằng chứng hay thời hạn phản đối cho cả lô.” (0.95): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    # ── CAS dựng lại sau rà soát đợt B (2026-11-09) ──
    'Bước ba, nếu thiếu phép kiểm thì máy vẫn chép 65 nghìn 535 byte.':
        'ASR chép “Bước ba, nếu thiếu phép kiểm thì máy vẫn chép 65.535 bay.” (0.95): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Nhưng từ ô dữ liệu tới cuối bản ghi chỉ có 20 trừ 3, tức 17 byte, nên 65 nghìn 518 byte trả về nằm ngoài bản ghi.':
        'ASR chép “Nhưng từ ô dữ liệu tới cuối bản ghi chỉ có 20 trừ 3, tức 17 bai, nên 65.518 bai trả về nằm ngoài bản ghi.” (0.943): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    # ── CLC dựng lại sau rà soát đợt B (2026-11-09) ──
    'Lưu trữ khối là một ổ đĩa thường gắn vào một máy ảo, sửa từng khối nhỏ với độ trễ thấp, hợp với ổ hệ điều hành và cơ sở dữ liệu tự quản.':
        'ASR chép “Lưu trữ khối là một ổ đĩa thương gắn vào một máy ảo, sự từng khối nhỏ với độ trễ thấp, hợp với ô hệ điều hành và cơ sở dữ liệu tư quản.” (0.882): lệch âm/thanh thuần Việt: thường/thương, sửa/sự, ổ/ô, tự/tư (bản chép “tư quản”; bộ so khớp ghép nhầm cặp “tự/bốn”) — NOT_VERIFIED bằng tai người',
    'Ở chặng bốn, trước năm 2020, kho chưa bảo đảm nhất quán mạnh cho mọi thao tác, và Amazon gọi đó là nhất quán cuối cùng.':
        'ASR chép “Ở chặng 4, trước năm 2020, kho chưa bảo đảm nhất quán mạnh cho mọi thao tác, và Amaro gọi đó là nhất quán cuối cùng.” (0.968): Amazon đọc thô theo lexicon CLC (probe p1: thô 8/8), lần này ASR viết “Amaro” — NOT_VERIFIED bằng tai người',
    # ── ESY dựng lại sau rà soát đợt B (2026-11-09) ──
    'Đèn báo nguồn, bộ ổn áp, cảm biến không được tắt, mỗi thứ tốn từ vài mi-crô-am-pe tới vài mi-li-am-pe, cộng thẳng vào dòng ngủ.':
        'ASR chép “Đen báo nguồn, bộ ổn áp, cảm biến không được tắt, mỗi thứ tốn từ vài microamper tới vài milliamper, cộng thẳng vào dòng ngủ.” (0.786): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; lệch âm/thanh thuần Việt: đèn/đen, am pe (trong “mi crô am pe” → “microamper”), am pe (trong “mi li am pe” → “milliamper”) — NOT_VERIFIED bằng tai người',
    'Lấy số minh hoạ, một đèn nối qua điện trở 1000 ôm ở 3 phẩy 3 vôn đã tốn khoảng 1 phẩy 3 mi-li-am-pe, gấp 130 lần dòng ngủ 10 mi-crô-am-pe.':
        'ASR chép “Lấy số minh họa, một đè nối qua điện trở một nghìn ôm ở 3,3 vôn đã tốn khoảng 1,3 mA, gấp 130 lần dòng ngủ 10 μA.” (0.842): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; lệch âm/thanh thuần Việt: đèn/đè, am pe (trong “mi li am pe” → “ma”), am pe (trong “mi crô am pe” → “μa”) — NOT_VERIFIED bằng tai người',
    'Năm 2014, xe Opportunity, thiết kế cho 3 tháng, đã chạy hơn 10 năm, và nghi phạm hàng đầu của các lần đặt lại là bộ nhớ flash đã mòn.':
        'ASR chép “Năm 2014, xe Opportunity, thiết kế cho 3 tháng, đã chạy hơn 10 năm và nghi phạm hàng đầu của các lần đặt lại là bộ nhớ Falas đã mòn.” (0.971): flash đọc thô theo lexicon ESY (probe p2: thô 6/8, dưới ngưỡng 7/8), ASR viết “Falas” — NOT_VERIFIED bằng tai người',
    # ── GFX dựng lại sau rà soát đợt B (2026-11-09) ──
    'Nhờ cắt ngay tại chính giữa đoạn trước khi chia cho w, toàn bộ nửa đoạn nằm gần hơn mặt gần được loại bỏ.':
        'ASR chép “Nhờ cắt ngay tại chính giữa đoạn trước khi chia cho v két, toàn bộ nửa đoạn nằm gần hơn mặt gần được loại bỏ.” (0.96): chữ w đọc “vê kép” (luật chung), ASR viết tách chữ — NOT_VERIFIED bằng tai người',
    # ── HCI dựng lại sau rà soát đợt B (2026-11-09) ──
    'Bảng này giải mã năm ký hiệu thao tác cơ sở, trong đó bốn giá trị K, P, H, M lấy từ bài báo năm 1980, còn B là cách tính hay dùng về sau.':
        'ASR chép “Bản này giải mã 5 kí hiệu thao tác cơ sở, trong đó 4 giá trị K, T, H, M lấy từ bài báo năm 1980, còn B là cách tính hay dùng về sau.” (0.925): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: bảng/bản, ký/kí — NOT_VERIFIED bằng tai người',
    'Theo điều kiện kích thước, một nút bấm đạt khi cả chiều rộng W lẫn chiều cao H đều lớn hơn hoặc bằng ngưỡng quy định.':
        'ASR chép “Theo điều kiện kích thức, một nút bấm đạt khi cả chiều rộng về đúc lẫn chiều cao hát đều lớn hơn hoặc bằng ngưỡng quy định.” (0.906): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: thước/thức — NOT_VERIFIED bằng tai người',
    # ── LLM dựng lại sau rà soát đợt B (2026-11-09) ──
    'Hôm nay ta học mã hoá cặp byte, cách học các mảnh từ từ dữ liệu mà nhiều mô hình ngôn ngữ lớn dùng để tách văn bản.':
        'ASR chép “Hôm nay ta học mã hóa cặp bay, cách học các mảnh từ từ dữ liệu mà nhiều mô hình ngôn ngữ lớn dùng để tách văn bản.” (0.964): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    # ── MLO dựng lại sau rà soát đợt B (2026-11-09) ──
    'Kho mã giữ mọi phiên bản mãi mãi, một tệp 5 GB sửa 10 lần có thể chiếm tới 50 GB, vì tệp dữ liệu lớn thường nén kém.':
        'ASR chép “Kho mả giữ mọi phiên bản mãi mãi, một tẹp 5GB sửa 10 lần có thể chiếm tới 50GB vì tẹp dữ liệu lớn thường nén kém.” (0.9): lệch âm/thanh thuần Việt: mã/mả, tệp/tẹp, tệp/tẹp — NOT_VERIFIED bằng tai người',
    # ── RBM dựng lại sau rà soát đợt B (2026-11-09) ──
    'Do đó với bài này, mỗi bước Euler đi quá xuống một chút, và các sai lệch nhỏ cộng dồn lại.':
        'ASR chép “Do đó với bài này, mỗi bước ơ lè đi quá xuống một chút và các sai lệch nhỏ cộng dồn lại.” (0.955): Euler đọc “Ơ-le” theo lexicon RBM (mượn probe DMS p1_ten: 8/8), ASR viết “ơ lè” (lệch thanh) — NOT_VERIFIED bằng tai người',
    'W đổi dấu mỗi bước là dấu hiệu hệ số đã âm, tức tốc độ học đã quá 1 chia a.':
        'ASR chép “Về đúc đổi dấu mỗi bước là dấu hiệu hệ số đà âm, tức tốc độ học đã quá một chia.” (0.857): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: đã/đà — NOT_VERIFIED bằng tai người',
    # ── ROB dựng lại sau rà soát đợt B (2026-11-09) ──
    'Vị trí đó có thể đã cũ tới khoảng 50 mi li giây, gồm một chu kỳ chờ và thời gian tính.':
        'ASR chép “vị trí đó có thể đã cụ tới khoảng 50mL, go một chút kỳ chờ và thời gian tính.” (0.773): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; lệch âm/thanh thuần Việt: cũ/cụ, gồm (trong “mi li giây gồm” → “ml go”), chu/chút — NOT_VERIFIED bằng tai người',
    # ── TOC dựng lại sau rà soát đợt B (2026-11-09) ──
    'Trong khoảng 1932 tới 1936, ba mô hình ra đời độc lập là máy Turing, phép tính lam-đa, và các hàm đệ quy.':
        'ASR chép “Trong khoảng 1932-1936, ba mô hình ra đời độc lập là máy tu trinh, phép tính lam đa và các hàm đệ quy.” (0.944): Turing đọc “Tua-rinh” theo lexicon TOC (probe p1+p2: 6/8, dưới ngưỡng 7/8), ASR viết “tu trinh”; “tới” giữa hai năm ASR viết thành gạch nối “1932-1936” — NOT_VERIFIED bằng tai người',
    'Năm 1936, Turing chứng minh một bài toán rất gần với nó là không máy nào giải được.':
        'ASR chép “Năm 1936, Tô Trình chứng minh một bài toán rất gần với nó là không máy nào giải được.” (0.939): Turing đọc “Tua-rinh” theo lexicon TOC (probe p1+p2: 6/8, dưới ngưỡng 7/8), ASR viết “Tô Trình” — NOT_VERIFIED bằng tai người',
    # ── WEB dựng lại sau rà soát đợt B (2026-11-09) ──
    'Giả sử ảnh chính nặng 300 KB, đây là số minh hoạ.':
        'ASR chép “Giả sự ảnh chính nặng 300 kilobyte, đây là số minh họa.” (0.846): KB đọc “ki-lô-byte” theo lexicon của khoá, ASR viết “kilobyte/kg”; lệch âm/thanh thuần Việt: sử/sự — NOT_VERIFIED bằng tai người',
    'Ảnh không chặn lần vẽ đầu, nhưng phần chính chỉ hiện ra khi ảnh tải xong, nên tổng phải tải là 500 cộng 300, bằng 800 KB.':
        'ASR chép “Ấn không chặn lần vẽ đầu, nhưng phần chính chỉ hiện ra khi ảnh tải xong nên tổng phải tải là 500 cộng 300 bằng 800 kg.” (0.933): KB đọc “ki-lô-byte” theo lexicon của khoá, ASR viết “kilobyte/kg”; lệch âm/thanh thuần Việt: ảnh/ấn — NOT_VERIFIED bằng tai người',
    'Ô nhập sai chỉ đổi viền đỏ, trong khi khoảng 5 tới 8 phần trăm nam giới, tuỳ nhóm dân, có rối loạn sắc giác đỏ lục.':
        'ASR chép “Ôn nhập sai chỉ đổi viện đỏ, trong khi khoảng 5 tới 8% nam giới tùy nhóm dân có trối loạn sát giác đỏ lục.” (0.852): lệch âm/thanh thuần Việt: ô/ôn (ô nhập liệu), viền/viện, rối/trối, sắc/sát — NOT_VERIFIED bằng tai người',
    # ── ACB L02 dựng lại sau đọc mẫu độc lập (2026-11-09) ──
    'Bước bốn, Core Banking đã giữ số tiền của khách trước khi bản tin được gửi đi.':
        'ASR chép “Bước 4, coa banh kiên đã giữ số tiền của khách trước khi bản tin được gửi đi.” (0.889): “Core Banking” theo lexicon đọc “co banh king” (BN-0019, cùng kiểu câu cũ của bài: ASR viết “co banh kim”), lần này ASR viết “coa banh kiên” — NOT_VERIFIED bằng tai người',
    # ── INT dựng lại sau đọc kiểm C (2026-11-09) ──
    'SAGA là chuỗi bước mà bước nào lỗi thì chạy bước hoàn tác, Outbox là bảng hộp thư ghi sự kiện cùng lúc với dữ liệu, còn Kafka chuyển sự kiện giữa các dịch vụ.':
        'ASR chép “Saga là chủ bước mà bước nào lỗi thì chạy bước hoàn tác, Outbox là bản hộp thư ghi sự kiện cùng lúc với dữ liệu, còn cao ca chuyển sự kiện giữa các dịch vụ.” (0.901): “kafka” đọc theo luật lexicon (lexicon_vi.INT.yaml: “Cáp-ca”), ASR viết “cao ca”; lệch âm/thanh thuần Việt: chuỗi/chủ, bảng/bản — NOT_VERIFIED bằng tai người',
    'T24 là một phần mềm ngân hàng lõi của hãng Temenos, còn NAPAS là công ty chuyển mạch tiền giữa các ngân hàng Việt Nam.':
        'ASR chép “T-24 là một phần mềm ngân hàng lõi của hãng Temenor, còn Napark là công ty chuyển mặt tiền giữa các ngân hàng Việt Nam.” (0.893): “temenos” đọc theo luật lexicon (lexicon_vi.INT.yaml: “Te-me-nót”), ASR viết “temenor”; “napas” đọc theo luật lexicon (lexicon_vi.INT.yaml: “Na-pát”), ASR viết “napark”; lệch âm/thanh thuần Việt: mạch/mặt — NOT_VERIFIED bằng tai người',
    'Cổng tích hợp dùng lệnh nguyên tử của Redis, tức kiểm tra và đặt khóa trong một bước, để tạo khóa phân tán theo mã đó.':
        'ASR chép “Cộng tích hợp dùng lệnh nguyên tử của Reddit, tức kiểm tra và đặt khóa trong một bước để tạo khóa phân tán theo mã đó.” (0.923): “redis” đọc theo luật lexicon (lexicon_vi.INT.yaml: “Rê-đít”), ASR viết “reddit”; lệch âm/thanh thuần Việt: cổng/cộng — NOT_VERIFIED bằng tai người',
    'Bước hai, khóa Redis có thể mất khi máy chủ bộ nhớ đệm gặp sự cố, nên lớp chặn cuối cùng nằm trong cơ sở dữ liệu, là ràng buộc duy nhất trên cột mã yêu cầu.':
        'ASR chép “Bước 2, khóa rê điếc có thể mất khi máy chủ bộ nhớ đem gặp sự cố nên lớp chặn cuối cùng nằm trong cơ sở dữ liệu là tràng buộc duy nhất trên cột mã yêu cầu.” (0.921): “redis” đọc theo luật lexicon (lexicon_vi.INT.yaml: “Rê-đít”), ASR viết “điếc”; lệch âm/thanh thuần Việt: đệm/đem, ràng/tràng — NOT_VERIFIED bằng tai người',
    'Vì dữ liệu đi theo khối 64 byte, nên một khối chứa được 64 chia 8, bằng 8 biến số nguyên dài nằm cạnh nhau.':
        'ASR chép “Vì dữ liệu đi theo khối 64-B, nên một khối chứa được 64-8 bằng 8 biến số nguyên dài nằm cạnh nhau.” (0.947): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: chia/∅ — NOT_VERIFIED bằng tai người',
    'Cách sửa là đệm thêm byte trống để mỗi biến hay bị ghi nằm ở một khối riêng.':
        'ASR chép “Các sữa là đệm thêm bay trống để mỗi biến hay bị ghi nằm ở một khối riêng.” (0.833): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: cách sửa/các sữa — NOT_VERIFIED bằng tai người',
    'Tầng một chia một nghìn nhánh, tầng hai thành một triệu, tầng ba thành một tỉ nhánh.':
        'ASR chép “Tần 1 chia 1.000 nhánh, tần 2 thành 1 triệu, tần 3 thành 1 tỷ nhánh.” (0.765): “tỉ” ASR viết chính tả “tỷ” (cùng âm); lệch âm/thanh thuần Việt: tầng/tần, tầng/tần, tầng/tần — NOT_VERIFIED bằng tai người',
    'Spring Boot là bộ khung phổ biến để viết dịch vụ Java, còn lớp vỏ ủy quyền là đối tượng bọc quanh đối tượng của bạn để tự mở và đóng giao dịch.':
        'ASR chép “Springbook là bộ khung phổ biến để viết dịch vụ Java, còn lớp vỏ ủy quyền là đối tượng bọc quanh đối tượng của bạn để tự mở và đóng giao dịch.” (0.954): “spring” đọc theo luật lexicon (lexicon_vi.INT.yaml: “S-pring”), ASR viết “springbook” — NOT_VERIFIED bằng tai người',
    'Đáp án chính xác là lựa chọn B vì bộ lọc Bloom là một mảng bit, mỗi tài khoản bật vài bit qua vài hàm băm, nên kiểm tra chỉ cần xem vài bit đó.':
        'ASR chép “Đáp án chính xác là lựa chọn B vì bộ lọc bơ luôn là một mãn bit. Mỗi tài khoản bật vài bit qua vài hàm băm, nên kiểm tra chỉ cần xem vài bit đó.” (0.93): “bloom” đọc theo luật lexicon (lexicon_vi.INT.yaml: “B-lum”), ASR viết “bơ luôn”; lệch âm/thanh thuần Việt: mảng/mãn — NOT_VERIFIED bằng tai người',
    'Hiểm họa ghi kép xảy ra khi dịch vụ vừa ghi cơ sở dữ liệu vừa gửi thông điệp ra ngoài qua Kafka, là hệ thống chuyển sự kiện giữa các dịch vụ.':
        'ASR chép “Hiểm họa ghi kép xảy ra khi dịch vụ vừa ghi cơ sở dữ liệu vừa gửi thông biệp ra ngoài qua Capca là hệ thống chuyển sự kiện giữa các dịch vụ.” (0.939): “kafka” đọc theo luật lexicon (lexicon_vi.INT.yaml: “Cáp-ca”), ASR viết “capca”; lệch âm/thanh thuần Việt: điệp/biệp — NOT_VERIFIED bằng tai người',
    'SAGA là chuỗi giao dịch nhỏ, mỗi bước có sẵn một bước bù trừ làm ngược lại, còn gạch nợ là báo cho bên bán rằng hoá đơn đã được trả.':
        'ASR chép “Saga là chủ giao dịch nhỏ, mỗi bước có sẵn một bước bù trừ làm ngược lại, còn gạch nợ là báo cho bên bán rằng hóa đơn đã được trả.” (0.968): lệch âm/thanh thuần Việt: chuỗi/chủ — NOT_VERIFIED bằng tai người',
    'Công cụ bắt biến động dữ liệu, ví dụ Debezium, đọc nhật ký giao dịch của cơ sở dữ liệu để phát bản tin, và thử lại cho tới khi gửi xong.':
        'ASR chép “Công cụ bắt biến động dữ liệu, ví dụ DBrium, đọc nhật ký giao dịch của cơ sở dữ liệu để phát bản tin và thử lại cho tới khi gửi xong.” (0.969): “debezium” đọc theo luật lexicon (lexicon_vi.INT.yaml: “Đê-bê-di-um”), ASR viết “dbrium” — NOT_VERIFIED bằng tai người',
    'Để hiểu cấu hình trên, ta giải nghĩa vài từ, nhà sản xuất là chương trình gửi tin, còn Broker là máy chủ Kafka lưu tin.':
        'ASR chép “Để hiểu cấu hình trên, ta giải nghĩa vai từ nhà sản xuất là chương trình gửi tin, còn Broker là máy chủ KK Lưu Tin.” (0.923): “kafka” đọc theo luật lexicon (lexicon_vi.INT.yaml: “Cáp-ca”), ASR viết “kk”; lệch âm/thanh thuần Việt: vài/vai — NOT_VERIFIED bằng tai người',
    'Bế tắc là khi mỗi phiên giữ một khóa và chờ khóa mà phiên kia đang giữ, và mã lỗi ORA-00060 là cách Oracle báo đã phát hiện điều đó.':
        'ASR chép “Bế tắc là khi mỗi phiên giữ một khóa và chờ khóa mà phiên kia đang giữ, và mã lỗi R.A.00060 là cách Oracle báo đã phát hiện điều đó.” (0.954): từ mượn/tên riêng “ora” đọc thô (không có luật lexicon), ASR viết “r a” — NOT_VERIFIED bằng tai người',
    'Bước ba, kỹ sư viết bằng PL/SQL, ngôn ngữ lập trình chạy bên trong Oracle, lấy dữ liệu theo từng lô một nghìn dòng trong một vòng lặp và cập nhật đồng loạt từng lô.':
        'ASR chép “Bước 3, kỹ sư viết bằng p lét cụ l, ngôn ngữ lập trình chạy bên trong Oracle, lấy dữ liệu theo từng lô một nghìn dòng trong một vòng lập và cập nhật đồng loạt từng lô.” (0.897): “pl/sql” đọc theo luật lexicon (lexicon_vi.INT.yaml: “P Lét Cù L”), ASR viết “cụ”; chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; “oracle” đọc theo luật lexicon (lexicon_vi.INT.yaml: “O-ra-cơn”), ASR viết “oracle”; lệch âm/thanh thuần Việt: lặp/lập — NOT_VERIFIED bằng tai người',
    'Vì sao xử lý theo lô nhanh hơn, vì câu lệnh cơ sở dữ liệu chạy ở một bộ máy khác với ngôn ngữ PL/SQL.':
        'ASR chép “Vì sao xử lý theo lô nhanh hơn? Vì câu lệnh cơ sở dữ liệu chạy ở một bộ máy khác với ngôn ngữ PLEC cụ EL.” (0.906): “sql” đọc theo luật lexicon (lexicon_vi.INT.yaml: “ét-cu-l”), ASR viết “plec cụ el” — NOT_VERIFIED bằng tai người',
    'Hệ thống phải hạch toán sổ cái ngân hàng lõi, rồi đóng gói bản tin gửi NAPAS, công ty chuyển mạch tiền giữa các ngân hàng.':
        'ASR chép “Hệ thống phải hạch toán sổ cái ngân hàng loại, rồi đóng gói bản tin gửi NAPAC, công ty chuyển mạch tiền giữa các ngân hàng.” (0.923): “napas” đọc theo luật lexicon (lexicon_vi.INT.yaml: “Na-pát”), ASR viết “napac”; lệch âm/thanh thuần Việt: lõi/loại — NOT_VERIFIED bằng tai người',
    'Bài này dùng hệ lõi T24 của hãng Temenos làm ví dụ.':
        'ASR chép “Bài này dùng hệ lõi T24 của hãng Themenot làm ví dụ.” (0.933): “temenos” đọc theo luật lexicon (lexicon_vi.INT.yaml: “Te-me-nót”), ASR viết “themenot” — NOT_VERIFIED bằng tai người',
    'Bản tin OFS là bản tin dạng chữ, các phần cách nhau bằng dấu phẩy, để hệ thống khác ra lệnh cho hệ lõi T24.':
        'ASR chép “Bản tin OS X là bản tin dạng chữ các phần cách nhau bằng dấu phẩy để hệ thống khác ra lệnh cho hệ loại T24.” (0.912): “ofs” đọc theo luật lexicon (lexicon_vi.INT.yaml: “O F S”), ASR viết “os x”; lệch âm/thanh thuần Việt: lõi/loại — NOT_VERIFIED bằng tai người',
    'ISO 8583 là chuẩn quốc tế cho bản tin giao dịch thẻ, và đặc tả của NAPAS thường được mô tả có gốc từ chuẩn này.':
        'ASR chép “ISO 8583 là chuẩn quốc tế cho bản tin giao dịch thẻ và đặt tả của NAPAC thường được mô tả có gốc từ chuẩn này.” (0.938): “napas” đọc theo luật lexicon (lexicon_vi.INT.yaml: “Na-pát”), ASR viết “napac”; lệch âm/thanh thuần Việt: đặc/đặt — NOT_VERIFIED bằng tai người',
    'Ở ngân hàng, một lệnh của HSM dịch khối PIN từ khóa của máy đầu cuối sang khóa vùng dùng với NAPAS, và một lệnh khác dịch giữa hai khóa vùng.':
        'ASR chép “Ở ngân hàng, một lệnh của HSM dịch khối pin từ khóa của máy đầu cuối sang khóa vùng dùng với NAPAC và một lệnh khác dịch giữa hai khóa vùng.” (0.968): “napas” đọc theo luật lexicon (lexicon_vi.INT.yaml: “Na-pát”), ASR viết “napac” — NOT_VERIFIED bằng tai người',
    'Số theo dõi STAN và số tham chiếu RRN mười hai ký tự là căn cứ chính để tra cứu và đối soát giao dịch giữa các ngân hàng thành viên.':
        'ASR chép “Số theo dõi S-Thang và số tham chiếu RRN 12 ký tự là căn cứ chính để tra cứu và đối soát giao dịch giữa các ngân hàng thành viên.” (0.952): “stan” đọc theo luật lexicon (lexicon_vi.INT.yaml: “Ét-tan”), ASR viết “s thang” — NOT_VERIFIED bằng tai người',
    'Khi một danh sách đã hết, phần còn dư của danh sách kia đều là lệch, và ta lặp lại cách này giữa NAPAS với đối tác.':
        'ASR chép “Khi một danh sách đã hết, phần cộng dư của danh sách kia đều là lịch, và ta lặp lại cách này giữa na phát với đối tác.” (0.893): “napas” đọc theo luật lexicon (lexicon_vi.INT.yaml: “Na-pát”), ASR viết “phát”; lệch âm/thanh thuần Việt: còn/cộng, lệch/lịch — NOT_VERIFIED bằng tai người',
    'Tra soát nghĩa là gửi yêu cầu hỏi lại trạng thái thật của giao dịch tới NAPAS hoặc ngân hàng nhận.':
        'ASR chép “Tra xoát nghĩa là gửi yêu cầu hỏi lại trạng thái thực của giao dịch tới NAPAC hoặc ngân hàng nhận.” (0.905): “napas” đọc theo luật lexicon (lexicon_vi.INT.yaml: “Na-pát”), ASR viết “napac”; lệch âm/thanh thuần Việt: thật/thực — NOT_VERIFIED bằng tai người',
    'Rừng cô lập, tức Isolation Forest, là nhiều cây chia dữ liệu ngẫu nhiên, và điểm bất thường bị tách riêng sau rất ít lần chia.':
        'ASR chép “Rừng cô lập, tức isolation forest là nhiều cây chi dữ liệu ngẫu nhiên và điểm bất thường bị tách riêng sau rất ít lần chia.” (0.962): lệch âm/thanh thuần Việt: chia/chi — NOT_VERIFIED bằng tai người',
    'Với độ tương đồng Cosine, hai véc tơ 1, 2 và 2, 3 có tích vô hướng bằng 8, chia cho căn 5 nhân căn 13 được khoảng 0 phẩy 992.':
        'ASR chép “Với độ tương đồng cosine 2 vector 1, 2 và 2, bà có tích vô hướng bằng 8, chia cho căn 5 nhân căn 13 được khoảng 0,992.” (0.899): “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; lệch âm/thanh thuần Việt: véc tơ/vector, ba/bà, không (trong “không phẩy” → “”) — NOT_VERIFIED bằng tai người',
    'Điểm Z cho biết số tiền cách mức trung bình bao nhiêu lần độ lệch chuẩn.':
        'ASR chép “điểm giá cho biết số tiền cách mức trung bình bao nhiêu lần độ lệch chuẩn.” (0.938): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Ví dụ trung bình 2 triệu, độ lệch chuẩn 1 phẩy 5 triệu, giao dịch 30 triệu thì điểm Z xấp xỉ 18 phẩy 67.':
        'ASR chép “Ví dụ trung bình 2 triệu, độ lệch chuẩn 1,5 triệu, giao dịch 30 triệu thì điểm giá sắp xỉ 18,67.” (0.931): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: xấp (trong “z xấp” → “giá sắp”) — NOT_VERIFIED bằng tai người',
    'Hệ thống cần thiết kế là một trung tâm điều phối thanh toán, còn cổng vào chung, gọi là API Gateway, kiểm tra từng yêu cầu rồi mới chuyển vào trong.':
        'ASR chép “Hệ thống cần thiết kế là một trung tâm điều phối thanh toán, còn cổng vào chung, gọi là APYGY, kiểm tra từng yêu cầu rồi mới chuyển vào trong.” (0.951): “gateway” đọc theo luật lexicon (lexicon_vi.INT.yaml: “ghét-oay”), ASR viết “apygy” — NOT_VERIFIED bằng tai người',
    # ── JVA dựng lại sau đọc kiểm C (2026-11-09) ──
    'Trước khi bắt đầu, máy cần có bộ công cụ JDK, bản hai mươi mốt trở lên, có bản tải miễn phí, vì trong đó có sẵn trình biên dịch và máy ảo.':
        'ASR chép “Trước khi bắt đầu, máy cần có bộ công cụ GZK, bản 21 trở lên có bản tại miễn phí vì trong đó có sẵn trình biên dịch và máy ảo.” (0.939): “jdk” đọc theo luật lexicon (lexicon_vi.JVA.yaml: “J D K”), ASR viết “gzk”; lệch âm/thanh thuần Việt: tải/tại — NOT_VERIFIED bằng tai người',
    # ── ACB dựng lại sau đọc kiểm C (2026-11-09) ──
    'Lương gross là lương trước khi trừ thuế và bảo hiểm.':
        'ASR chép “Lương gơ đốc là lương trước khi trừ thuế và bảo hiểm.” (0.917): “gross” đọc theo luật lexicon (lexicon_vi.ACB.yaml: “gơ-rốt”), ASR viết “đốc” — NOT_VERIFIED bằng tai người',
    'Redis là kho dữ liệu nằm trong bộ nhớ, đọc ghi rất nhanh, thường dùng để ghi nhớ mã giao dịch đã xử lý.':
        'ASR chép “Rê đích là kho giữ liệu nằm trong bộ nhớ, độc ghi rất nhanh, thường dùng để ghi nhớ mã giao dịch đã xử lý.” (0.92): “redis” đọc theo luật lexicon (lexicon_vi.ACB.yaml: “Rê-đít”), ASR viết “đích”; lệch âm/thanh thuần Việt: đọc/độc — NOT_VERIFIED bằng tai người',
    'Kafka ở tầng này là hệ thống lưu các sự kiện theo đúng thứ tự để nhiều dịch vụ cùng đọc.':
        'ASR chép “CAPCA ở tầng này là hệ thống lưu các sự kiện theo đúng thứ tự để nhiều dịch vụ cung độc.” (0.857): “kafka” đọc theo luật lexicon (lexicon_vi.ACB.yaml: “Cáp-ca”), ASR viết “capca”; lệch âm/thanh thuần Việt: cùng đọc/cung độc — NOT_VERIFIED bằng tai người',
    'Do Core chưa trả kết quả, cách làm nghiệp dư là báo lỗi thất bại ngay hoặc tự động bấm gửi lại lệnh.':
        'ASR chép “Do còn chưa trả kết quả, cách làm nghiệp dư là báo lỗi thất bại ngay hoặc tự động bấm gửi lại lệnh.” (0.957): “core” đọc theo luật lexicon (lexicon_vi.ACB.yaml: “Co”), ASR viết “còn” — NOT_VERIFIED bằng tai người',
    'Thứ hai là không đặt hạn sống cho bản tin khiến các lệnh cũ ứ đọng và có thể bị hạch toán muộn sang ngày hôm sau.':
        'ASR chép “Thứ hai là không đặt hàng sống cho bản tin khiến các lệnh củ ưu động và có thể bị hạch toán muộn sang ngày hôm sau.” (0.852): lệch âm/thanh thuần Việt: hạn/hàng, cũ ứ đọng/củ ưu động — NOT_VERIFIED bằng tai người',
    'Khi kết nối Core T24 qua IBM MQ, tại sao ta nên dùng mã định danh tương quan thay vì mở hàng đợi riêng cho từng khách hàng?':
        'ASR chép “Khi kết nối COT-24 qua IB-MMQI, tại sao ta nên dùng mã định danh tương quan thay vì mở hàng đợi riêng cho từng khách hàng?” (0.892): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; “core” đọc theo luật lexicon (lexicon_vi.ACB.yaml: “Co”), ASR viết “cot” — NOT_VERIFIED bằng tai người',
    'NAPAS là Công ty Cổ phần Thanh toán Quốc gia Việt Nam, vận hành hệ thống chuyển mạch nối các ngân hàng với nhau.':
        'ASR chép “NAPAC là công ty cổ phần thanh toán quốc gia Việt Nam vận hành hệ thống chuyển mạch nối các ngân hàng với nhau.” (0.958): “napas” đọc theo luật lexicon (lexicon_vi.ACB.yaml: “Na-pát”), ASR viết “napac” — NOT_VERIFIED bằng tai người',
    'Redis là kho dữ liệu khoá giá trị nằm trong bộ nhớ, đọc ghi rất nhanh và nhiều máy chủ cùng dùng chung.':
        'ASR chép “Reddit là kho dữ liệu khóa giá trị nằm trong bộ nhớ, đọc ghi rất nhanh và nhiều máy chủ cùng dùng chung.” (0.957): “redis” đọc theo luật lexicon (lexicon_vi.ACB.yaml: “Rê-đít”), ASR viết “reddit” — NOT_VERIFIED bằng tai người',
    'Tóm lại, chuỗi logic cổng NAPAS gồm khử trùng lặp, giữ tiền trên hệ thống lõi và dịch mã PIN trong phần cứng.':
        'ASR chép “Tóm lại, chuỗi lô ghét cổng NaPak gồm khử trùng lập, giữ tiền trên hệ thống lõi và dịch mã pin trong phần cứng.” (0.857): “logic” đọc theo luật lexicon (lexicon_vi.yaml: “lô-gíc”), ASR viết “ghét”; tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; “napas” đọc theo luật lexicon (lexicon_vi.ACB.yaml: “Na-pát”), ASR viết “napak”; lệch âm/thanh thuần Việt: lặp/lập — NOT_VERIFIED bằng tai người',
    'Còn cây-x-cu-l-đê-bê là công cụ cho phép viết câu lệnh giống SQL để xử lý trực tiếp luồng sự kiện trên Kafka.':
        'ASR chép “Còn CaseCoolerDB là công cụ cho phép viết câu lệnh giống SQL để xử lý trực tiếp luôn sự kiện trên CapCa.” (0.776): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; “kafka” đọc theo luật lexicon (lexicon_vi.ACB.yaml: “Cáp-ca”), ASR viết “capca”; lệch âm/thanh thuần Việt: bê/casecoolerdb, cây cu (trong “cây x cu l d b” → “casecoolerdb”), luồng/luôn — NOT_VERIFIED bằng tai người',
    'Bước ba, Trung tâm thông báo phân loại mức ưu tiên và kiểm tra khóa chống gửi trùng trong Redis, kho dữ liệu nằm trong bộ nhớ.':
        'ASR chép “Bước 3, Trung tâm thông báo phân loại mức ưu tiên và kiểm tra khóa chống gửi trùng trong Reddit, kho dữ liệu nằm trong bộ nhớ.” (0.963): “redis” đọc theo luật lexicon (lexicon_vi.ACB.yaml: “Rê-đít”), ASR viết “reddit” — NOT_VERIFIED bằng tai người',
    'Trong công nghệ cây-x-cu-l-đê-bê, tại sao bảng hồ sơ người dùng nên được tạo dưới dạng Bảng thay vì dạng Luồng?':
        'ASR chép “Trong công nghệ Case Cooler DB, tại sao bản hồ sơ người dùng nên được tạo dưới dạng bản thay vì dạng luôn?” (0.76): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: cây cu (trong “cây x cu l” → “case cooler”), bảng/bản, bảng/bản, luồng/luôn — NOT_VERIFIED bằng tai người',
    'Bước hai, cây-x-cu-l-đê-bê vẫn cho nối hai luồng với nhau, nhưng phải kèm một cửa sổ thời gian, nên hồ sơ khách cập nhật từ lâu sẽ không được ghép với giao dịch mới.':
        'ASR chép “Bước 2, cái schooler DB vẫn cho nối hai lùng với nhau, nhưng phải kè một cửa sổ thời gian, nên hồ sơ khách cập nhật từ lâu sẽ không được ghép với giao dịch mới.” (0.868): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: cây cu (trong “cây x cu l” → “cái schooler”), luồng/lùng, kèm/kè — NOT_VERIFIED bằng tai người',
    'Fiber là một thư viện để viết dịch vụ chạy trên máy chủ, còn PostgreSQL là một hệ quản trị cơ sở dữ liệu quan hệ mã nguồn mở.':
        'ASR chép “Faber là một thư viện để viết dịch vụ chạy trên máy chủ, còn Popre Ecular là một hệ quản trị cơ sở dữ liệu quan hệ mã nguồn mở.” (0.915): “fiber” đọc theo luật lexicon (lexicon_vi.ACB.yaml: “Pha-bơ”), ASR viết “faber”; “postgresql” đọc theo luật lexicon (lexicon_vi.ACB.yaml: “Pốt-g-rê ét-cu-l”), ASR viết “popre ecular” — NOT_VERIFIED bằng tai người',
    'Còn người chỉ xem thì ở cả hai cách đều đọc tự do, vì PostgreSQL giữ nhiều phiên bản của một dòng nên lệnh đọc thường không bị chặn.':
        'ASR chép “Còn người chỉ xem thì ở cả hai cách đều đọc tự do, vì POPGREA S Cooler giữ nhiều phiên bản của một dòng nên lệnh đọc thường không bị chặn.” (0.933): “postgresql” đọc theo luật lexicon (lexicon_vi.ACB.yaml: “Pốt-g-rê ét-cu-l”), ASR viết “popgrea s cooler” — NOT_VERIFIED bằng tai người',
    'Trong Oracle, lỗi này mang mã ORA-00060.':
        'ASR chép “Trong Oracle, lỗi này mang mã ORA00060.” (1.0): từ rủi ro ra, không, không, không, không cả hai mô hình viết khác (cách viết, không phải âm) — NOT_VERIFIED bằng tai người',
    'Lỗi ORA không không không sáu không là sự cố bế tắc khóa kinh điển cần phòng tránh.':
        'ASR chép “Lỗi OERA 00060 là sự cố bế tắc khóa kinh điển cần phòng tránh.” (0.788): từ mượn/tên riêng “ora không không không” đọc thô (không có luật lexicon), ASR viết “oera”; lệch âm/thanh thuần Việt: không/mươi — NOT_VERIFIED bằng tai người',
    'Ta tránh quét cơ sở dữ liệu chính bằng cách đọc dữ liệu đã chép sang Kafka và chia theo đoạn thời gian.':
        'ASR chép “Ta tránh quét cơ sở dữ liệu chính bằng cách đọc dữ liệu đã chép sang CAPCA và chia theo đoạn thời gian.” (0.957): “kafka” đọc theo luật lexicon (lexicon_vi.ACB.yaml: “Cáp-ca”), ASR viết “capca” — NOT_VERIFIED bằng tai người',
    'Thủ tục lưu trữ là đoạn chương trình PL/SQL được lưu và chạy ngay bên trong cơ sở dữ liệu.':
        'ASR chép “Thủ tục lưu trữ là đoạn chương trình P-Led cụ L được lưu và chạy ngay bên trong cơ sở dữ liệu.” (0.913): “pl/sql” đọc theo luật lexicon (lexicon_vi.ACB.yaml: “P Lét Cù L”), ASR viết “led cụ” — NOT_VERIFIED bằng tai người',
    'Mỗi lần mã PL/SQL gọi sang bộ máy SQL là một lần chuyển ngữ cảnh tốn thời gian.':
        'ASR chép “Mỗi lần mã P-LedQ-E-L gọi sang bộ máy S-Cooler là một lần chuyển ngữ cảnh tốn thời gian.” (0.8): “pl/sql” đọc theo luật lexicon (lexicon_vi.ACB.yaml: “P Lét Cù L”), ASR viết “ledq e”; Bayes đọc “Bay-ét” theo lexicon chung (probe 3/8, NOT_VERIFIED), ASR viết “bay X/S”; chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; “sql” đọc theo luật lexicon (lexicon_vi.ACB.yaml: “ét-cu-l”), ASR viết “s cooler” — NOT_VERIFIED bằng tai người',
    'Deepfake là video giả khuôn mặt người thật do trí tuệ nhân tạo tạo ra, còn bộ công cụ phần mềm kiểm tra độ sống giúp phân biệt người thật với ảnh hay video.':
        'ASR chép “Dipfit là video giả khu mặt người thật do trí tuệ nhân tạo tạo ra, còn bộ công cụ phần mềm kiểm tra độ sống giúp phân biệt người thật với ảnh hay video.” (0.941): “deepfake” đọc theo luật lexicon (lexicon_vi.ACB.yaml: “đíp-phếch”), ASR viết “dipfit”; lệch âm/thanh thuần Việt: khuôn/khu — NOT_VERIFIED bằng tai người',
    'Động cơ này chạy theo mô hình SAGA, tức một chuỗi bước giao dịch nhỏ, bước nào hỏng thì chạy bước bù trừ để hoàn tác các bước trước.':
        'ASR chép “Động cơ này chạy theo mô hình Saga, tức một chuỗi bước giao dịch nhỏ, bước nào hỏng thì chạy bước bù trừ để hoàn tác các bước trước.” (1.0): từ rủi ro sa, ga cả hai mô hình viết khác (cách viết, không phải âm) — NOT_VERIFIED bằng tai người',
    'Khi điều kiện tiên quyết được thỏa mãn, lệnh trừ tiền mới được phát hành sang Core Banking.':
        'ASR chép “Khi điều kiện tiên quyết được thỏa mãn, lệnh trừ tiền mới được phát hành sang Coban King.” (0.919): lệch âm/thanh thuần Việt: co banh/coban — NOT_VERIFIED bằng tai người',
    'ERP là phần mềm quản trị doanh nghiệp của đối tác, còn Webhook là việc máy chủ ngân hàng chủ động gọi sang máy chủ đối tác để báo tin.':
        'ASR chép “RRP là phần mềm quản trị doanh nghiệp của đối tác. Còn webhook là việc máy chủ ngân hàng chủ động gọi sang máy chủ đối tác để báo tin.” (0.967): “erp” đọc theo luật lexicon (lexicon_vi.ACB.yaml: “E R P”), ASR viết “rrp” — NOT_VERIFIED bằng tai người',
    'Trong kiến trúc tham chiếu, lệnh này dùng ứng dụng chuyển tiền của Core Banking Temenos T24.':
        'ASR chép “Trong kiến trúc tham chiếu, lệnh này dùng ứng dụng chuyển tiền của co-banking Temenok T24.” (0.9): “core” đọc theo luật lexicon (lexicon_vi.ACB.yaml: “Co”), ASR viết “co”; “temenos” đọc theo luật lexicon (lexicon_vi.ACB.yaml: “Te-me-nót”), ASR viết “temenok” — NOT_VERIFIED bằng tai người',
    'Sau khi sắp xếp, sổ cái có mã 1, 2 và 4, tệp của NAPAS có mã 1, 2, 3 và 4, còn đối tác chỉ có mã 1 và 4.':
        'ASR chép “Sau khi sắp xếp, sổ cái có mã 1, 2 và 4, tẹp của NAPAC có mã 1, 2, 3 và 4, còn đối tác chỉ có mã 1 và 4.” (0.935): “napas” đọc theo luật lexicon (lexicon_vi.ACB.yaml: “Na-pát”), ASR viết “napac”; lệch âm/thanh thuần Việt: tệp/tẹp — NOT_VERIFIED bằng tai người',
    'Mã 3 chỉ có ở NAPAS nên là lệnh treo ghi Có, cần hạch toán bù.':
        'ASR chép “Mã 3 chỉ có ở Na Phát nên là lệnh treo ghi có, cần hạch toán bu.” (0.882): “napas” đọc theo luật lexicon (lexicon_vi.ACB.yaml: “Na-pát”), ASR viết “phát”; lệch âm/thanh thuần Việt: bù/bu — NOT_VERIFIED bằng tai người',
    'Lưu ý, T24 ở đây là kiến trúc tham chiếu rút từ kinh nghiệm làm ở OCB, và Squad Lending là tên nhóm phát triển tín dụng ở đó.':
        'ASR chép “Lưu ý, T-24 ở đây là kiến trúc tham chiếu rút từ kinh nghiệm làm ở OCB và Squawk Landing là tên nhóm phát triển tín dụng ở đó.” (0.938): “lending” đọc theo luật lexicon (lexicon_vi.ACB.yaml: “len-đinh”), ASR viết “squawk landing” — NOT_VERIFIED bằng tai người',
    'LOS là hệ thống tiếp nhận và xét duyệt hồ sơ vay, còn Whitelist lương là danh sách khách nhận lương qua ngân hàng được ưu tiên cấp thấu chi.':
        'ASR chép “ELO-OX là hệ thống tiếp nhận và xét duyệt hồ survey, còn wireless lương là danh sách khách nhận lương qua ngân hàng được ưu tiên cấp thấu chi.” (0.867): “los” đọc theo luật lexicon (lexicon_vi.ACB.yaml: “L O S”), ASR viết “elo ox”; “whitelist” đọc theo luật lexicon (lexicon_vi.ACB.yaml: “oai-lít”), ASR viết “wireless”; lệch âm/thanh thuần Việt: sơ vay/survey — NOT_VERIFIED bằng tai người',
    # ── CS115 dựng lại sau đọc kiểm C (2026-11-09) ──
    'Tử số là 0 phẩy 9 nhân 0 phẩy 01, mẫu số là 0 phẩy 108.':
        'ASR chép “Tự số là không phải chiến nhân 0.01, mẫu số là 0.108.” (0.743): “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; lệch âm/thanh thuần Việt: tử/tự, chín (trong “phẩy chín” → “phải chiến”), không (trong “không phẩy” → “”) — NOT_VERIFIED bằng tai người',
    'Vì vậy cả hai điểm chuyển sang cụm đầu.':
        'ASR chép “Vì vậy, cả 2 điểm chuyển sang cũng đâu.” (0.778): lệch âm/thanh thuần Việt: cụm đầu/cũng đâu — NOT_VERIFIED bằng tai người',
    'Công thức Bayes cho hậu nghiệm có tâm x chia 2, phương sai một nửa, tức tâm 0 phẩy 5 khi x bằng 1.':
        'ASR chép “Công thức bay x cho hậu nghiệm có tâm ích chi 2, phương sai 1 nữa, tức tâm 0,5 khi ích bằng 1.” (0.88): Bayes đọc “Bay-ét” theo lexicon chung (probe 3/8, NOT_VERIFIED), ASR viết “bay X/S”; lệch âm/thanh thuần Việt: chia/chi, nửa/nữa — NOT_VERIFIED bằng tai người',
    # ── CSA dựng lại sau đọc kiểm C (2026-11-09) ──
    'Epsilon là khoảng cách quanh số 1.':
        'ASR chép “FC Long là khoảng cách quanh số 1.” (0.8): “epsilon” đọc theo luật lexicon (lexicon_vi.yaml: “ép-xi-lôn”), ASR viết “fc long” — NOT_VERIFIED bằng tai người',
    'Luật De Morgan nói, không của a và b bằng không a hoặc không b, tức là nói không phải cả hai đều bằng 1 cũng là nói ít nhất một cái bằng 0.':
        'ASR chép “Luật đơ mor gần nói, không của A và B bằng không A hoặc không B, tức là nói không phải cả 2 đều bằng 1 cũng là nói ít nhất 1 cái bằng không.” (0.971): “de morgan” đọc theo luật lexicon (lexicon_vi.CSA.yaml: “Đơ Mo-gần”), ASR viết “mor” — NOT_VERIFIED bằng tai người',
    'Chỉ số gồm 9 bit, vì bộ nhớ đệm 32768 byte chia 64 byte được 512 bằng 2 mũ 9 dòng, nó chỉ phải nhìn vào dòng nào.':
        'ASR chép “Chỉ số gồm 9 biết, vì bộ nhớ đệm 32.768 bai chia 64 bai được 512 bằng 2 mũ chứng dòng, nó chỉ phải nhìn vào dòng nào.” (0.902): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: bit/biết, chín/chứng — NOT_VERIFIED bằng tai người',
    'Một khối là một đoạn 64 byte liền nhau của bộ nhớ, số khối bằng địa chỉ chia lấy phần nguyên cho 64, ví dụ địa chỉ 200 thuộc khối 3.':
        'ASR chép “Một khối là một đoạn 64 bai liền nhau của bộ nhớ, số khối bằng địa chỉ chia lấy phần nguyên cho 64, ví dụ địa chỉ 200 thuộc khối 3.” (0.972): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Giá phải trả là bảng trang phẳng có 2 mũ 20 mục, mỗi mục 4 byte, tức khoảng 4 triệu byte cho mỗi tiến trình, nên máy thật dùng bảng trang nhiều tầng.':
        'ASR chép “Giá phải trả là bản trang phẳng có 2 mũ 20 mục, mỗi mục 4 bay, tức khoảng 4 triệu bay cho mỗi tiến trình, nên máy thật dùng bản trang nhiều tân.” (0.853): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: bảng/bản, bảng/bản, tầng/tân — NOT_VERIFIED bằng tai người',
    # ── DBS dựng lại sau đọc kiểm C (2026-11-09) ──
    'Cộng lại, mỗi lần đọc ngẫu nhiên mất khoảng 8 mi li giây, một số minh hoạ.':
        'ASR chép “Tộng lại, mỗi lần độc ngẫu nhiên mất khoảng 8 mili giây một số minh họa.” (0.788): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; lệch âm/thanh thuần Việt: cộng/tộng, đọc/độc — NOT_VERIFIED bằng tai người',
    'Làm thử với bảng 5 triệu dòng, một số minh hoạ, mỗi trang 8 ki-lô-byte chứa 100 dòng như bài 7.':
        'ASR chép “Làm thử với bảng 5 triệu dòng, một số minh họa, mỗi trang 8 kilobytes chiếu 100 dòng như bài 7.” (0.87): KB đọc “ki-lô-byte” theo lexicon của khoá, ASR viết “kilobyte/kg”; lệch âm/thanh thuần Việt: chứa (trong “ki lô byte chứa” → “kilobytes chiếu”) — NOT_VERIFIED bằng tai người',
    'Dựng lại cả bảng phải ghi 50 nghìn trang, khoảng 0 phẩy 4 GB, còn thêm cột tức thì không ghi trang dữ liệu nào.':
        'ASR chép “Dựng lại cả bản phải ghi 50.000 trang, khoảng 0.4GB, còn thêm cục tức thì không ghi trang dữ liệu nào.” (0.902): “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; lệch âm/thanh thuần Việt: bảng/bản, cột/cục — NOT_VERIFIED bằng tai người',
    # ── DMS dựng lại sau đọc kiểm C (2026-11-09) ──
    'Vì L là bội của p trừ 1, định lý Fermat nhỏ cho x mũ L đồng dư 1 theo mô-đun p.':
        'ASR chép “Vì l là bội của p-1, định lý phát ma nhỏ cho ít mũ l đồng dư 1 theo mô đun p.” (0.936): “fermat” đọc theo luật lexicon (lexicon_vi.DMS.yaml: “Phéc-ma”), ASR viết “phát”; lệch âm/thanh thuần Việt: trừ/∅ — NOT_VERIFIED bằng tai người',
    # ── OSY dựng lại sau đọc kiểm C (2026-11-09) ──
    'Nhưng chọn ô 1 rồi ô 3 hay chọn ô 3 rồi ô 1 vẫn là cùng một cặp, nên mỗi cặp bị đếm 2 lần.':
        'ASR chép “Nhưng chọn O1 rồi O3 hay chọn O3 rồi O1 vẫn là cùng một cặp, nên mỗi cặp bị đếm hai lần.” (0.846): “ô” (ô lưới) ASR viết chữ “O” — NOT_VERIFIED bằng tai người',
    'Cách một, cộng hai bộ đếm ở những dòng mà món đã đặt hoặc lấy xong, 5 với 0, 4 với 1, cho tới 0 với 5, lúc nào cũng được 5, đúng bằng số ô.':
        'ASR chép “Cách 1, cộng 2 bộ đếm ở những dòng mà món đã đặt hoặc lấy xong, 5 với 0, 4 với 1, cho tới 0 với 5, lúc nào cũng được 5, đúng bằng số ố.” (0.972): “ô” (ô lưới) ASR viết chữ “O” — NOT_VERIFIED bằng tai người',
    'Địa chỉ ảo là địa chỉ chương trình tự dùng, như thể nó có riêng một dải liền bắt đầu từ 0, còn địa chỉ vật lý là vị trí thật của byte đó trong bộ nhớ.':
        'ASR chép “Địa chỉ áo là địa chỉ chương trình tự dùng, như thể nó có riêng một giải liền bắt đầu từ không, còn địa chỉ vật lý là vị trí thật của bài đó trong bộ nhớ.” (0.946): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: ảo/áo — NOT_VERIFIED bằng tai người',
    'Bảng hai tầng chia 20 bit số trang thành 10 bit chọn mục trong thư mục và 10 bit chọn mục trong bảng con.':
        'ASR chép “Bảng 2 tần chia 20 biết số trang thành 10 biết chọn mục trong thứ 1 và 10 biết chọn mục trong bảng con.” (0.76): lệch âm/thanh thuần Việt: tầng/tần, bit/biết, bit/biết, thư mục/thứ một, bit/biết — NOT_VERIFIED bằng tai người',
    'Bộ đệm nhỏ mà vẫn hay trúng, vì một trang có 4096 byte, và chương trình thường đọc nhiều byte liền nhau trong cùng một trang trước khi sang trang khác.':
        'ASR chép “Bộ đệm nhỏ mà vẫn hay trúng vì một trang có 4.096 bai và chương trình thường đọc nhiều bai liền nhau trong cùng một trang trước khi sang trang khác.” (0.946): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Về lý thuyết các con trỏ đủ chỉ tới tệp khoảng 4 TiB, dù hệ thống thật còn bị những giới hạn khác chặn thấp hơn.':
        'ASR chép “Về lý thuyết các con trỏ đủ chỉ tới tệ khoảng 4TB, dù hệ thống thật còn bị những giới hạn khác chặn thấp hơn.” (0.923): “tib” đọc theo luật lexicon (lexicon_vi.OSY.yaml: “tê-ra-byte”), ASR viết “tb”; lệch âm/thanh thuần Việt: tệp/tệ — NOT_VERIFIED bằng tai người',
    'Bốn KiB bằng 2 mũ 12, tức 4096 byte, còn MiB và TiB là 2 mũ 20 và 2 mũ 40, ở giữa còn một bậc 2 mũ 30, mỗi bậc gấp 1024 lần bậc trước.':
        'ASR chép “4 kilobyte bằng 2 mũ 12, tức 4096 byte, còn megabyte và terabyte là 2 mũ 20 và 2 mũ 40, ở giữa còn một bật 2 mũ 30, mỗi bật cấp 1024 lần bật trước.” (0.865): “kib” đọc theo luật lexicon (lexicon_vi.OSY.yaml: “ki-lô-byte”), ASR viết “kilobyte”; MiB đọc “mê-ga-byte” (quy ước OSY/DEN: cách nói thông dụng, màn hình giữ MiB, câu nêu rõ 2 mũ 20), ASR viết “MB”; “tib” đọc theo luật lexicon (lexicon_vi.OSY.yaml: “tê-ra-byte”), ASR viết “terabyte”; lệch âm/thanh thuần Việt: bậc/bật, bậc gấp/bật cấp, bậc/bật — NOT_VERIFIED bằng tai người',
    'Đĩa chia thành các khối 4 KiB, và mỗi tệp có một nút chỉ mục ghi kích thước, chủ sở hữu, quyền, thời gian, cùng 15 con trỏ khối.':
        'ASR chép “để chia thành các khối 4 kilobytes và mỗi tệp có một nút chỉ một ghi kích thước, chủ sở hữu, quyền, thời gian cùng 15 con trỏ khối.” (0.9): “kib” đọc theo luật lexicon (lexicon_vi.OSY.yaml: “ki-lô-byte”), ASR viết “kilobytes”; lệch âm/thanh thuần Việt: đĩa/để, mục/một — NOT_VERIFIED bằng tai người',
    'Mỗi con trỏ chỉ là một số dài 4 byte ghi số hiệu của một khối trên đĩa.':
        'ASR chép “Mỗi con trỏ chỉ là một số dài bốn bay ghi số hiệu của một khối trên đĩa.” (0.944): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Ổ đĩa quay gồm các mặt đĩa tròn xếp chồng lên nhau, mỗi mặt có nhiều rãnh là những vòng tròn đồng tâm.':
        'ASR chép “Hổ đĩa quay gồm các mặt đĩa tròn xếp trồng lên nhau, mỗi mặt có nhiều rảnh là những vòng tròn đồng tâm.” (0.87): lệch âm/thanh thuần Việt: ổ/hổ, chồng/trồng, rãnh/rảnh — NOT_VERIFIED bằng tai người',
    'Mỗi tệp ghi 9 bit quyền cơ bản, chia làm ba nhóm, chủ sở hữu, nhóm, và người khác.':
        'ASR chép “Mỗi tập ghi chính biết quyền cơ bản, chia làm ba nhóm, chủ sở hiểu, nhóm và người khác.” (0.789): lệch âm/thanh thuần Việt: tệp/tập, chín bit/chính biết, hữu/hiểu — NOT_VERIFIED bằng tai người',
    # ── PLC dựng lại sau đọc kiểm C (2026-11-09) ──
    'Một ô-tô-mát hữu hạn là một cỗ máy có hữu hạn trạng thái, đọc một ký tự thì đi theo mũi tên mang ký tự đó sang trạng thái kế, như hình vừa xem.':
        'ASR chép “Một Automat hữu hạn là một cổ máy có hữu hạn trạng thái, đọc một ký tự thì đi theo mũi tên mang ký tự đó sang trạng thái kế, như hình vừa xem.” (0.914): “ô” (ô lưới) ASR viết chữ “O”; lệch âm/thanh thuần Việt: tô mát (trong “ô tô mát” → “automat”), cỗ/cổ — NOT_VERIFIED bằng tai người',
    'Người ta đã chứng minh mỗi biểu thức chính quy đổi được thành một ô-tô-mát hữu hạn, và ta ghép mọi mẫu lại thành một ô-tô-mát lớn.':
        'ASR chép “Người ta đã chứng minh mỗi biểu thức chính quy đổi được thành một automatic hữu hạn và ta ghép mọi mẫu lại thành một automatic lớn.” (0.862): “ô” (ô lưới) ASR viết chữ “O”; lệch âm/thanh thuần Việt: tô mát (trong “ô tô mát” → “automatic”), tô mát (trong “ô tô mát” → “automatic”) — NOT_VERIFIED bằng tai người',
    'Kết quả là 1065353216, dù chuẩn C không bảo đảm cách đọc này.':
        'ASR chép “Kết quả là 106535216, dù chuẩn xe không bảo đảm cách độc này.” (0.737): “tỉ” ASR viết chính tả “tỷ” (cùng âm); lệch âm/thanh thuần Việt: không (trong “tỉ không” → “”), triệu ba trăm năm mươi ba/∅, đọc/độc — NOT_VERIFIED bằng tai người',
    # ── SDP dựng lại sau đọc kiểm C (2026-11-09) ──
    'Xét một đơn nặng 2 ki-lô-gam đi 8 ki-lô-mét, với giá là số minh hoạ.':
        'ASR chép “Xét 1 đơn nặng 2 kg đi 8 km, với giá là số minh họa.” (0.765): “ki-lô-byte” đọc tách âm tiết, ASR viết “kg” rồi chép “byte” thành “bay/ba”; gam-ma (γ) ASR viết “gamma”; đơn vị mét, ASR viết ký hiệu “m” — NOT_VERIFIED bằng tai người',
    # ── SWF dựng lại sau đọc kiểm C (2026-11-09) ──
    'Máy như vậy có tên là ô-tô-mát hữu hạn đơn định, trong đó ô-tô-mát nghĩa là máy tự chạy theo luật.':
        'ASR chép “Máy như vậy có tên là Automat Hữu Hạng Đơn Định, trong đó Automat nghĩa là máy tự chạy theo luật.” (0.783): “ô” (ô lưới) ASR viết chữ “O”; lệch âm/thanh thuần Việt: tô mát (trong “ô tô mát” → “automat”), hạn/hạng, tô mát (trong “ô tô mát” → “automat”) — NOT_VERIFIED bằng tai người',
    'Tiếp theo, ta đếm số cách xen kẽ.':
        'ASR chép “Tiếp theo, tà đếm số cách sen kẻ.” (0.75): lệch âm/thanh thuần Việt: ta/tà, kẽ/kẻ — NOT_VERIFIED bằng tai người',
    'Số cách chọn k ô trong n ô gọi là tổ hợp chập k của n, bằng n giai thừa chia cho k giai thừa nhân n trừ k giai thừa.':
        'ASR chép “Số khách chọn KO trong N, O gọi là tổ hợp chập K của N, bằng N giai thừa chi cho K giai thừa nhân N trừ K giai thừa.” (0.852): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; “ô” (ô lưới) ASR viết chữ “O”; lệch âm/thanh thuần Việt: cách/khách, chia/chi — NOT_VERIFIED bằng tai người',
    'Tiếp theo, byte là một ô nhớ nhỏ chứa một số từ 0 tới 255.':
        'ASR chép “Tiếp theo, bay là một ô nhớ nhỏ chứa một số từ 0 tới 255.” (0.947): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Máy lưu chữ bằng cách gán cho mỗi chữ một mã số, mỗi chữ cái tiếng Anh nằm trong một byte, chữ A có mã 65, chữ B có mã 66.':
        'ASR chép “Máy lưu chữ bằng cách gán cho mỗi chữ một mạ số, mỗi chữ cái tiếng Anh nằm trong một bay, chữ A có mạ 65, chữ B có mạ 66.” (0.886): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: mã/mạ, mã/mạ, mã/mạ — NOT_VERIFIED bằng tai người',
    'Trong ngôn ngữ C, chuỗi kết thúc bằng một byte 0 để máy biết chỗ dừng, nên chuỗi 9 chữ cần 10 byte.':
        'ASR chép “Trong ngôn ngữ C, chủ kết thúc bằng một bay không để máy biết chỗ dừng, nền chủ 9 chữ cần 10 bay.” (0.783): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: chuỗi/chủ, nên chuỗi/nền chủ — NOT_VERIFIED bằng tai người',
    # ── TOC dựng lại sau đọc kiểm C (2026-11-09) ──
    'Định lý Kleene, năm 1956, nối ba cách mô tả, gồm biểu thức chính quy, máy không đơn định, và máy đơn định.':
        'ASR chép “Định lý Collini, năm 1956, nối ba cách mô tả, gồm biểu thức chính quy, máy không đơn định và máy đơn định.” (0.966): “kleene” đọc theo luật lexicon (lexicon_vi.TOC.yaml: “Cờ-li-ni”), ASR viết “collini” — NOT_VERIFIED bằng tai người',
    'Vì đi được cả hai chiều, hai định nghĩa cho đúng cùng một lớp NP, và phần ví dụ ngay sau làm điều này bằng số với bài toán tổng tập con.':
        'ASR chép “Vì đi được cả hai chiều, hai định nghĩa cho đúng cùng một lớp NT và phần ví dụ ngay sau làm điều này bằng số với bài toán tổng tập con.” (0.969): “np” đọc theo luật lexicon (lexicon_vi.TOC.yaml: “en-pê”), ASR viết “nt” — NOT_VERIFIED bằng tai người',
    # ── OSY L09 câu dãy chữ số hệ mười sáu (đợt đọc kiểm C, 2026-11-10) ──
    'Ví dụ địa chỉ 0 0 4 0 3 A B C hệ mười sáu, ta tách nó thành 0 0 4 0 0 0 0 0 cộng 3 A B C.':
        'ASR chép “Ví dụ địa chỉ 00403ABC hệ 16, ta tách nó thành 0040000-3ABC.” (0.737): ASR gộp dãy chữ số và chữ cái đọc rời (“không không bốn không ba A B C”) thành một số viết liền, nên bản chép ngắn hơn câu; đủ cả hai địa chỉ và từ “cộng” → “-”; không cụt: tts_speed_scan 2026-11-10 báo 0/51 874 câu < 0,22 s/từ — NOT_VERIFIED bằng tai người',
    # ── BNK dựng lại sau đọc kiểm C (2026-11-09) ──
    'Thêm một đơn vị đo, theo cách tính quen dùng cho bộ nhớ: một ki lô byte bằng một nghìn không trăm hai mươi bốn byte, và một mê ga byte là số đó nhân với chính nó.':
        'ASR chép “Thêm một đơn vị đo, theo cách tính quen dùng cho bộ nhớ, 1 kilobytes bằng 1024 bytes và 1 megabyte là số đó nhân với chính nó.” (0.861): KB đọc “ki-lô-byte” theo lexicon của khoá, ASR viết “kilobyte/kg”; byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); MB đọc “mê-ga-byte” theo lexicon của khoá, ASR viết “MB/megabyte” — NOT_VERIFIED bằng tai người',
    'BigDecimal giữ số thập phân nên đúng, với điều kiện tạo nó từ chuỗi chữ không phẩy một.':
        'ASR chép “Bích decimal giữ số thập phân nên đúng với điều kiện tạo nó từ chủ chữ 0,1.” (0.865): “bigdecimal” đọc theo luật lexicon (lexicon_vi.BNK.yaml: “Bích Đê-xi-mơn”), ASR viết “bích decimal”; lệch âm/thanh thuần Việt: chuỗi/chủ — NOT_VERIFIED bằng tai người',
    'Spring Boot là cách đóng gói và chạy nhanh bộ khung đó.':
        'ASR chép “Springbook là cách đóng gói và chạy nhanh bộ khung đó.” (0.87): “spring” đọc theo luật lexicon (lexicon_vi.BNK.yaml: “S-pring”), ASR viết “springbook” — NOT_VERIFIED bằng tai người',
    'Tiêm phụ thuộc là Spring nối các bean với nhau, thường qua hàm khởi tạo, tức phương thức chạy lúc tạo đối tượng.':
        'ASR chép “Tiêm phụ thuộc là spring nối các binh với nhau, thường qua hàm khởi tạo, tức phương thức chạy lúc tạo đối tượng.” (0.957): lệch âm/thanh thuần Việt: bean/binh — NOT_VERIFIED bằng tai người',
    'REST API là cách một dịch vụ mở chức năng của nó qua các đường dẫn đó.':
        'ASR chép “RECAPI là cách một dịch vụ mở chức năng của nó qua các đường dẫn đó.” (0.909): “rest” đọc theo luật lexicon (lexicon_vi.BNK.yaml: “Rét”), ASR viết “recapi” — NOT_VERIFIED bằng tai người',
    'Phiên là một kết nối đang làm việc với cơ sở dữ liệu, tức phần mềm lưu bảng dữ liệu mà ta hỏi bằng ngôn ngữ SQL.':
        'ASR chép “Phiên là một kết nối đang làm việc với cơ sở dữ liệu, tức phần mềm lưu bản dữ liệu mà ta hỏi bằng ngôn ngữ Eculer.” (0.926): “sql” đọc theo luật lexicon (lexicon_vi.BNK.yaml: “ét-cu-l”), ASR viết “eculer”; lệch âm/thanh thuần Việt: bảng/bản — NOT_VERIFIED bằng tai người',
    'Redis là một kho tên tra cứu và giá trị chạy trong bộ nhớ, hay được dùng làm bộ đệm.':
        'ASR chép “Reddit là một kho tên tra cứu và giá trị chạy trong bộ nhớ, hay được dùng làm bộ đệm.” (0.95): “redis” đọc theo luật lexicon (lexicon_vi.BNK.yaml: “Rê-đít”), ASR viết “reddit” — NOT_VERIFIED bằng tai người',
    'Khoá phân tán là khoá giữ quyền dùng chung giữa nhiều máy chủ, đặt ở một nơi lưu chung như Redis.':
        'ASR chép “Khóa phân tán là khóa giữ quyền dùng chung giữa nhiều máy chủ, đặt ở một nơi lưu chung như Reddit.” (0.952): “redis” đọc theo luật lexicon (lexicon_vi.BNK.yaml: “Rê-đít”), ASR viết “reddit” — NOT_VERIFIED bằng tai người',
    'Kafka là hệ thống chuyển thông điệp.':
        'ASR chép “CAPCA là hệ thống chuyển thông điệp” (0.857): “kafka” đọc theo luật lexicon (lexicon_vi.BNK.yaml: “Cáp-ca”), ASR viết “capca” — NOT_VERIFIED bằng tai người',
    'Sự kiện là một thông điệp báo một việc đã xảy ra, được gửi qua một hệ thống chuyển thông điệp như Kafka, ví dụ lệnh bốn mươi hai đã chuyển xong.':
        'ASR chép “Sự kiện là một thông điệp báo một việc đã xảy ra, được gửi qua một hệ thống chuyển thông điệp như CAPCA, ví dụ lệnh 42 đã chuyển xong.” (0.969): “kafka” đọc theo luật lexicon (lexicon_vi.BNK.yaml: “Cáp-ca”), ASR viết “capca” — NOT_VERIFIED bằng tai người',
    'Lưu ý, mỗi mạng thanh toán có đặc tả riêng, kể cả NAPAS, công ty chuyển mạch thẻ và thanh toán liên ngân hàng của Việt Nam.':
        'ASR chép “Lưu ý, mỗi mạng thanh toán có đặt tải riêng, kể cả NAPAC, công ty chuyển mạch thẻ và thanh toán liên ngân hàng của Việt Nam.” (0.889): “napas” đọc theo luật lexicon (lexicon_vi.BNK.yaml: “Na-pát”), ASR viết “napac”; lệch âm/thanh thuần Việt: đặc tả/đặt tải — NOT_VERIFIED bằng tai người',
    'Một byte là nhóm tám bit, nên viết bằng đúng hai chữ số thập lục phân.':
        'ASR chép “Một by là nhóm 8 bit nên viết bằng đúng 2 chữ số thập lục phân.” (0.938): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Cuối cùng, STAN là trường mười một, mã vết sáu chữ số do bên gửi đánh.':
        'ASR chép “Cuối cùng, Estan là trường 11 mà vết 6 triệu số do bên gửi đánh.” (0.75): “stan” đọc theo luật lexicon (lexicon_vi.BNK.yaml: “Ét-tan”), ASR viết “estan”; lệch âm/thanh thuần Việt: mã vết/mà véc, chữ/triệu — NOT_VERIFIED bằng tai người',
    'Ở Việt Nam, chuyển mạch đó là NAPAS, công ty chuyển mạch thẻ và thanh toán liên ngân hàng.':
        'ASR chép “Ở Việt Nam, chuyển mặt đó là NAPAC, công ty chuyển mặt thẻ và thanh toán liên ngân hàng.” (0.842): “napas” đọc theo luật lexicon (lexicon_vi.BNK.yaml: “Na-pát”), ASR viết “napac”; lệch âm/thanh thuần Việt: mạch/mặt, mạch/mặt — NOT_VERIFIED bằng tai người',
    # ── CAS dựng lại sau đọc kiểm C (2026-11-09) ──
    'Bộ nhớ là một dãy ô liền nhau, mỗi ô 1 byte, và một chương trình đặt nhiều dữ liệu khác nhau sát cạnh nhau.':
        'ASR chép “Bộ nhớ là một dãy ô liền nhau, mỗi ô một bay và một chương trình đặt nhiều dữ liệu khác nhau sát cạnh nhau.” (0.96): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Ví dụ vùng A chiếm từ ô 0 tới ô 19 thì dữ liệu khác bắt đầu ngay từ ô 20.':
        'ASR chép “Ví dụ vùng A chiếm từ O0 tới O19 thì dữ liệu khác bắt đầu ngay từ O20.” (0.87): “ô” (ô lưới) ASR viết chữ “O” — NOT_VERIFIED bằng tai người',
    'Trước hết, ta cần bốn điều, bắt đầu từ cách máy ghi số có dấu bằng n bit, gọi là bù 2.':
        'ASR chép “Trước hết, ta cần 4 điều, bắt đầu từ cách máy ghi số có dấu bằng nBit, gọi là bù 2.” (0.93): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: bit (trong “n bit” → “nbit”) — NOT_VERIFIED bằng tai người',
    # ── CS112 dựng lại sau đọc kiểm C (2026-11-09) ──
    'Lỗi thứ nhất, ép hệ thức 2 nhân T của n chia 2, cộng n lôgarit n, vào trường hợp ba, hay trường hợp hai như bảng vừa học.':
        'ASR chép “Lỗi thứ nhất, ép hệ thức 2 nhân tê của n chi 2, cộng n log n vào trường hợp 3 hay trường hợp 2 như bản vừa học.” (0.897): thuật ngữ Việt hoá viết liền “lôgarit” (= lô-ga-rit), TTS đọc theo chính tả Việt, ASR viết “log”; lệch âm/thanh thuần Việt: chia/chi, bảng/bản — NOT_VERIFIED bằng tai người',
    'Chi phí do việc sắp xếp quyết định, Theta của n lôgarit n, tức số bước tăng cùng cỡ với n nhân lôgarit n.':
        'ASR chép “Chi phí do việc sắp xếp quyết định, theta của n log n tức số bước tăng cùng cỡ với n nhân log n.” (0.88): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; thuật ngữ Việt hoá viết liền “lôgarit” (= lô-ga-rit), TTS đọc theo chính tả Việt, ASR viết “log” — NOT_VERIFIED bằng tai người',
    'Xâu là một dãy ký tự, và xâu con chung của hai xâu là một dãy con có mặt trong cả hai, ví dụ A B C B và B D C B có chung B C B.':
        'ASR chép “Sâu là một dãy ký tự, và sâu con chung của hai sâu là một dãy con có mặt trong cả hai, ví dụ ABCB và BGCB có chung BCB.” (0.932): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Tập mọi điểm thoả hết ràng buộc gọi là miền chấp nhận được, ở đây là một tứ giác có bốn đỉnh O, A, B, C.':
        'ASR chép “Tập mọi điểm thỏa hết tràn buộc gọi là miền chấp nhận được, ở đây là một tứ giác có 4 định nhò A, B, C.” (0.885): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: ràng/tràn, đỉnh (trong “đỉnh o” → “định nhò”) — NOT_VERIFIED bằng tai người',
    'Theo bài 1, Theta của f nghĩa là số bước tăng cùng cỡ với f, bị kẹp giữa hai hằng số nhân f, còn Omega của f nghĩa là ít nhất cỡ f.':
        'ASR chép “Theo bài 1, teta của f nghĩa là số bước tăng cùng cỡ với f, bị kẹp giữa hai hàng số nhân f, còn omega của f nghĩa là ít nhất cỡ f.” (0.939): “theta” đọc theo luật lexicon (lexicon_vi.CS112.yaml: “tê-ta”), ASR viết “teta”; lệch âm/thanh thuần Việt: hằng/hàng — NOT_VERIFIED bằng tai người',
    'Ví dụ n nhân n trừ 1 chia 2 nằm giữa một phần tư và một nửa của n bình phương khi n từ 2 trở lên, nên thuộc Theta của n bình phương.':
        'ASR chép “Ví dụ n nhân n trừ 1 chi 2 nằm giữ 1 phần 4 và 1 nửa của n bình phương khi n từ 2 trở lên, nên thuộc teta của n bình phương.” (0.912): “theta” đọc theo luật lexicon (lexicon_vi.CS112.yaml: “tê-ta”), ASR viết “teta”; lệch âm/thanh thuần Việt: chia/chi, giữa/giữ — NOT_VERIFIED bằng tai người',
    'Nó lấy ra phần tử nhỏ nhất và cập nhật trong Theta của lôgarit n, với 1000 phần tử chỉ khoảng 10 bước.':
        'ASR chép “Nó lấy ra phần tử nhỏ nhất và cập nhật trong teta của logarith n với 1 nghìn phần tử chỉ khoảng 10 bước.” (0.958): “theta” đọc theo luật lexicon (lexicon_vi.CS112.yaml: “tê-ta”), ASR viết “teta” — NOT_VERIFIED bằng tai người',
    'Ở bài 6, đống nhị phân là một cây luôn giữ phần tử nhỏ nhất ở gốc, lấy ra phần tử nhỏ nhất trong Theta của lôgarit n.':
        'ASR chép “Ở bài 6, đóng nhị phân là một cây luôn giữ phần tử nhỏ nhất ở gốc, lấy ra phần tử nhỏ nhất trong teta của logarith n.” (0.929): “theta” đọc theo luật lexicon (lexicon_vi.CS112.yaml: “tê-ta”), ASR viết “teta”; lệch âm/thanh thuần Việt: đống/đóng — NOT_VERIFIED bằng tai người',
    'Ở đây W là sức chứa, và ô hàng i cột c ghi giá trị lớn nhất khi chỉ dùng i món đầu với sức chứa c.':
        'ASR chép “Ở đây về đúc là sức chứa và ô hàng y cột xe ghi giá trị lớn nhất khi chỉ dùng y món đầu với sức chứa xe.” (0.945): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    # ── CVI dựng lại sau đọc kiểm C (2026-11-09) ──
    'Trước hết, ta cần hiểu bit và byte là gì.':
        'ASR chép “Trước hết, ta cần hiểu biết và bay là gì?” (0.8): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: bit/biết — NOT_VERIFIED bằng tai người',
    'Nếu ảnh có thêm một cột, ta trượt bộ lọc sang phải một cột, ô mới là 2, 0, 4, 1, cho 2 trừ 1, bằng 1.':
        'ASR chép “Nếu ảnh có thêm 1 cột, ta trực bộ lọc sang phải 1 cột, ôm mới là 2, 0, 4, 1, cho 2 trừ 1, bằng 1.” (0.926): “ô” (ô lưới) ASR viết chữ “O”; lệch âm/thanh thuần Việt: trượt/trực — NOT_VERIFIED bằng tai người',
    'Đệm P nghĩa là thêm P hàng và P cột số 0 quanh viền ảnh, còn bước nhảy S nghĩa là mỗi lần trượt bộ lọc đi S ô.':
        'ASR chép “Đệm P nghĩa là thêm P hàng và P cột số không quanh viện ảnh, còn bước nhảy S nghĩa là mỗi lần trượt bộ lọc đi SO.” (0.912): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; “ô” (ô lưới) ASR viết chữ “O”; lệch âm/thanh thuần Việt: viền/viện — NOT_VERIFIED bằng tai người',
    # ── DSC dựng lại sau đọc kiểm C (2026-11-09) ──
    'Trong từng cỡ cửa hàng, chi thêm không bán thêm, nhưng gộp cả bốn thì r khoảng 0 phẩy 978, chỉ vì cửa hàng lớn vừa chi nhiều vừa bán nhiều.':
        'ASR chép “Trong từng cửa hàng, chi thêm không bán thêm, nhưng gột cả 4 thì error khoảng 0,978, chỉ vì cửa hàng lớn vừa chi nhiều vừa bán nhiều.” (0.896): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; lệch âm/thanh thuần Việt: cỡ/∅, gộp/gột, không (trong “không phẩy” → “”) — NOT_VERIFIED bằng tai người',
    'Đo một tỉ lệ p trên n người thì kết quả dao động quanh tỉ lệ thật, vì một nhóm người khác sẽ cho con số hơi khác.':
        'ASR chép “Đó 1 tỷ lệ T trên n người thì kết quả giao động quanh tỷ lệ thật vì một nhóm người khác sẽ cho con số hơi khác.” (0.857): “tỉ” ASR viết chính tả “tỷ” (cùng âm); chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: đo/đó — NOT_VERIFIED bằng tai người',
    # ── DSY dựng lại sau đọc kiểm C (2026-11-09) ──
    'Tăng tốc là thời gian cũ chia thời gian mới, tức 1 chia cho tổng đó, và công thức này gọi là định luật Amdahl.':
        'ASR chép “Tăng tốc là thời gian cũ chia thời gian mới, tức mục chia cho tổng đó và công thức này gọi là định luật am đang.” (0.923): “amdahl” đọc theo luật lexicon (lexicon_vi.DSY.yaml: “Am-đan”), ASR viết “đang”; lệch âm/thanh thuần Việt: một/mục — NOT_VERIFIED bằng tai người',
    'Hãy tưởng tượng có m ô, và ta rút ngẫu nhiên m lần, mỗi lần một ô.':
        'ASR chép “Hãy tưởng tượng có mO và ta trúc ngẫu nhiên m lần, mỗi lần một O.” (0.788): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; “ô” (ô lưới) ASR viết chữ “O”; lệch âm/thanh thuần Việt: rút/trúc — NOT_VERIFIED bằng tai người',
    'Đảo lại, D xấp xỉ 256 chia số nhỏ thứ 256, nhưng người ta dùng 255, tức 256 trừ 1.':
        'ASR chép “Đảo lại, về sắp sĩ 256 chia số nhỏ thứ 256, nhưng người ta dùng 255, tức 256 trừ 1.” (0.917): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: xấp xỉ (trong “d xấp xỉ” → “về sắp sĩ”) — NOT_VERIFIED bằng tai người',
    # ── DVO dựng lại sau đọc kiểm C (2026-11-09) ──
    'Dữ liệu trong máy được đếm bằng byte, mỗi chữ cái không dấu chiếm một byte.':
        'ASR chép “Dữ liệu trong máy được đếm bằng bay, mỗi chữ cái không giấu chiếm một bay.” (0.875): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    # ── IRS dựng lại sau đọc kiểm C (2026-11-09) ──
    'Thử lại, e mũ 1 phẩy 099 xấp xỉ 3 phẩy 001, gần đúng bằng 3.':
        'ASR chép “Thử lại, e-mũ 1.099 sắp xỉ 3.001 gần đúng bằng 3.” (0.732): “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; lệch âm/thanh thuần Việt: xấp/sắp — NOT_VERIFIED bằng tai người',
    'Cosin bằng tích vô hướng chia tích hai độ dài, với u và v ở trên là 8 chia 2 phẩy 236 nhân 3 phẩy 742, khoảng 0 phẩy 956.':
        'ASR chép “Cô sinh bằng tích vô hướng chia tích 2 độ dài, với u và v ở trên là 8 chi 2 phẩy 236 nhân 3 phẩy 742, khoảng 0,956.” (0.916): thuật ngữ Việt hoá viết liền “cosin” (= co-sin), TTS đọc theo chính tả Việt, ASR viết “cô sinh”; “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; lệch âm/thanh thuần Việt: chia/chi, không (trong “không phẩy” → “”) — NOT_VERIFIED bằng tai người',
    'Hai mũi tên cùng hướng, như 1, 2, 0 và 2, 4, 0, có góc 0 độ và cosin bằng 1.':
        'ASR chép “2 mũi tên cùng hướng như 1, 2, 0 và 2, 4, 0, có góc không độ và cô xin bằng 1.” (0.93): thuật ngữ Việt hoá viết liền “cosin” (= co-sin), TTS đọc theo chính tả Việt, ASR viết “cô xin” — NOT_VERIFIED bằng tai người',
    'Hai mũi tên vuông góc, như 1, 0 và 0, 1, có góc 90 độ và cosin bằng 0, vì tích vô hướng bằng 0.':
        'ASR chép “Hai mũi tên vung góc như 1, 0 và 0, 1 có góc 90 độ và cô sinh bằng 0, vị tích vô hướng bằng 0.” (0.868): thuật ngữ Việt hoá viết liền “cosin” (= co-sin), TTS đọc theo chính tả Việt, ASR viết “cô sinh”; lệch âm/thanh thuần Việt: vuông/vung, vì/vị — NOT_VERIFIED bằng tai người',
    'Cosin càng gần 1 thì hai vector càng cùng hướng, nên ta sẽ dùng nó để đo văn bản giống câu hỏi tới đâu.':
        'ASR chép “Cô Siên càng gần 1 thì hai vét tơ càng cùng hướng nên ta sẽ dùng nó để đo văn bản giống câu hỏi tới đâu.” (0.941): thuật ngữ Việt hoá viết liền “cosin” (= co-sin), TTS đọc theo chính tả Việt, ASR viết “cô siên” — NOT_VERIFIED bằng tai người',
    'Công thức xếp hạng có bão hoà làm cái lợi của việc lặp từ tăng chậm dần.':
        'ASR chép “Công thức xếp hạn có bảo hòa làm cái lợi của việc lập từ tăng chậm dân.” (0.765): lệch âm/thanh thuần Việt: hạng/hạn, bão/bảo, lặp/lập, dần/dân — NOT_VERIFIED bằng tai người',
    'Cosin của hai vector là tích vô hướng, tức nhân từng cặp thành phần rồi cộng, chia cho tích hai độ dài, và ở đây ba vector đều dài đúng 5.':
        'ASR chép “Cô xuyên của 2 vector là tích vô hướng, tức nhân từng cặp thành phần rồi cộng, chia cho tích 2 độ dài và ở đây 3 vector đều dài đúng 5.” (0.952): thuật ngữ Việt hoá viết liền “cosin” (= co-sin), TTS đọc theo chính tả Việt, ASR viết “cô xuyên” — NOT_VERIFIED bằng tai người',
    'Bình phương khoảng cách là lấy hiệu từng thành phần, bình phương, rồi cộng lại, nên cosin lớn hay khoảng cách nhỏ đều nghĩa là gần.':
        'ASR chép “Bình phương khoảng cách là lấy hiệu từng thành phần, bình phương, rồi cộng lại, nền coxin lớn hay khoảng cách nhỏ đều nghĩa là gân.” (0.885): thuật ngữ Việt hoá viết liền “cosin” (= co-sin), TTS đọc theo chính tả Việt, ASR viết “nền coxin”; lệch âm/thanh thuần Việt: nên (trong “nên cosin” → “nền coxin”), gần/gân — NOT_VERIFIED bằng tai người',
    'Cosin của chúng là 4 nhân 3 cộng 3 nhân 4, chia 5 nhân 5, được 0 phẩy 96, còn bình phương khoảng cách chỉ là 1 cộng 1, bằng 2.':
        'ASR chép “Cô sinh của chúng là 4 nhân 3 cộng 3 nhân 4, chia 5 nhân 5, được 0,96, còn bình phương khoảng cách chỉ là 1 cộng 1 bằng 2.” (0.955): thuật ngữ Việt hoá viết liền “cosin” (= co-sin), TTS đọc theo chính tả Việt, ASR viết “cô sinh” — NOT_VERIFIED bằng tai người',
    'Văn bản ô tô đồ chơi có chung chữ ô tô, nhưng vector 0, 5 chỉ cho cosin 0 phẩy 6 và bình phương khoảng cách tới 20.':
        'ASR chép “Văn bản ô tô đồ chơi có chung chữ ô tô nhưng vector 0 nằm chỉ cho cosine 0,6 và bình phương khoảng cách tới 20.” (0.931): thuật ngữ Việt hoá viết liền “cosin” (= co-sin), TTS đọc theo chính tả Việt, ASR viết “cosine”; lệch âm/thanh thuần Việt: năm/nằm — NOT_VERIFIED bằng tai người',
    'Hệ theo vector xếp B đầu với cosin 0 phẩy 83, rồi E, A, C, thang điểm không bao giờ vượt quá 1.':
        'ASR chép “Hệ theo vét tơ xếp bê đầu với cô sinh 0,83 rồi E, A, C thang điểm không bao giờ vượt quá mục.” (0.906): thuật ngữ Việt hoá viết liền “cosin” (= co-sin), TTS đọc theo chính tả Việt, ASR viết “cô sinh”; lệch âm/thanh thuần Việt: một/mục — NOT_VERIFIED bằng tai người',
    'Hệ theo từ khoá thường dùng công thức xếp hạng có bão hoà.':
        'ASR chép “Hãy theo từ khóa thường dùng công thức xếp hạn có bảo hòa.” (0.769): lệch âm/thanh thuần Việt: hệ/hãy, hạng/hạn, bão/bảo — NOT_VERIFIED bằng tai người',
    'Điều thứ ba là cosin, hệ theo vector dùng nó để đo hai vector có cùng hướng hay không.':
        'ASR chép “Điều thứ ba là cô sinh, hệ theo vét tơ dùng nó để đo hai vét tơ có cùng hướng hay không?” (0.93): thuật ngữ Việt hoá viết liền “cosin” (= co-sin), TTS đọc theo chính tả Việt, ASR viết “cô sinh” — NOT_VERIFIED bằng tai người',
    'Cosin là tích vô hướng, tức nhân từng cặp thành phần rồi cộng, chia cho tích hai độ dài, mỗi độ dài là căn của tổng bình phương.':
        'ASR chép “Cô xuyên là tích vô hướng, tức nhân từng cặp thành phần rồi cộng, chia cho tích 2 độ dài, mỗi độ dài là căn của tổng bình phương.” (0.947): thuật ngữ Việt hoá viết liền “cosin” (= co-sin), TTS đọc theo chính tả Việt, ASR viết “cô xuyên” — NOT_VERIFIED bằng tai người',
    'Hai độ dài là căn 5, khoảng 2 phẩy 236, và căn 14, khoảng 3 phẩy 742, nên cosin xấp xỉ 0 phẩy 956.':
        'ASR chép “2 độ dài là căn 5, khoảng 2,236 và căn 14, khoảng 3,742, nên cô xin sắp xỉ không phải 956.” (0.853): “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; thuật ngữ Việt hoá viết liền “cosin” (= co-sin), TTS đọc theo chính tả Việt, ASR viết “cô xin sắp”; lệch âm/thanh thuần Việt: xấp (trong “cosin xấp” → “cô xin sắp”) — NOT_VERIFIED bằng tai người',
    'Cosin không bao giờ vượt 1, đạt 1 khi hai vector cùng hướng hẳn, và không dưới âm 1, khi hai vector ngược hướng.':
        'ASR chép “Cô xin không bao giờ vượt một, đạt một khi hai vét tơ cùng hướng hẳn và không dưới âm một khi hai vét tơ ngược hướng.” (0.943): thuật ngữ Việt hoá viết liền “cosin” (= co-sin), TTS đọc theo chính tả Việt, ASR viết “cô xin” — NOT_VERIFIED bằng tai người',
    'Vector trọng số của bài 2 không có số âm nên cosin nằm từ 0 tới 1, còn vector nhúng của bài 3 có thể cho cosin âm.':
        'ASR chép “Vét tơ trọng số của bài 2 không có số âm nên cosine nằm từ 0 tới 1, còn vét tơ nhúng của bài 3 có thể cho cosine âm.” (0.933): thuật ngữ Việt hoá viết liền “cosin” (= co-sin), TTS đọc theo chính tả Việt, ASR viết “cosine” — NOT_VERIFIED bằng tai người',
    'Vì vậy lôgarit của 1 bằng 0, còn lôgarit của 2 xấp xỉ 0 phẩy 693 vì e mũ 0 phẩy 693 xấp xỉ 2.':
        'ASR chép “Vì vậy, logarith của 1 bằng không, còn logarith của 2 sắp sĩ 0,693 vì emu 0,693 sắp sĩ 2.” (0.754): “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: xấp xỉ không (trong “xấp xỉ không phẩy” → “sắp sĩ”), mũ không (trong “e mũ không phẩy” → “emu”), xấp xỉ/sắp sĩ — NOT_VERIFIED bằng tai người',
    'Nếu mô hình dành xác suất p cho đáp án đúng, mất mát là âm lôgarit của p.':
        'ASR chép “Nếu mô hình dành xác suất P cho đáp án đúng, mất mát là âm logadric của P.” (0.944): thuật ngữ Việt hoá viết liền “lôgarit” (= lô-ga-rit), TTS đọc theo chính tả Việt, ASR viết “logadric” — NOT_VERIFIED bằng tai người',
    'Con số này đúng là cosin của góc giữa hai vector, nên hai vector cùng hướng như 1, 2 và 2, 4 được 1, còn hai vector vuông góc như 1, 0 và 0, 1 được 0.':
        'ASR chép “Con số này đúng là cô xin của góc giữa 2 vét tơ nên 2 vét tơ cùng hướng như 1, 2 và 2, 4 được 1, còn 2 vét tơ vung góc như 1, 0 và 0, 1 được 0.” (0.938): thuật ngữ Việt hoá viết liền “cosin” (= co-sin), TTS đọc theo chính tả Việt, ASR viết “cô xin”; lệch âm/thanh thuần Việt: vuông/vung — NOT_VERIFIED bằng tai người',
    'Bài 2 đã dùng chính số này để xếp văn bản theo câu hỏi, cosin càng gần 1 thì hai vector càng cùng hướng, bất kể dài hay ngắn.':
        'ASR chép “Bài 2 đã dùng chính số này để xếp văn bản theo câu hỏi, cô xin càng gần 1 thì hai vét tơ càng cùng hướng, bất kể dài hay ngắn.” (0.951): thuật ngữ Việt hoá viết liền “cosin” (= co-sin), TTS đọc theo chính tả Việt, ASR viết “cô xin” — NOT_VERIFIED bằng tai người',
    'Bài 6 cũng đã dùng tích vô hướng để tính cosin, tức độ giống nhau giữa hai người.':
        'ASR chép “Bài 6 cũng đã dùng tích vô hướng để tính cô sinh, tức độ giống nhau giữa hai người.” (0.919): thuật ngữ Việt hoá viết liền “cosin” (= co-sin), TTS đọc theo chính tả Việt, ASR viết “cô sinh” — NOT_VERIFIED bằng tai người',
    'Độ giống ở bài này là số minh hoạ cho sẵn, còn thực tế có thể lấy cosin của hai vector mô tả sản phẩm như ở bài 2, bằng 1 khi hai vector cùng hướng.':
        'ASR chép “Độ giống ở bài này là số minh họa cho sẵn, còn thực tế có thể lấy cosine của hai vector mô tả sản phẩm như ở bài 2, bằng một khi hai vector cùng hướng.” (0.972): thuật ngữ Việt hoá viết liền “cosin” (= co-sin), TTS đọc theo chính tả Việt, ASR viết “cosine” — NOT_VERIFIED bằng tai người',
    # ── MLO dựng lại sau đọc kiểm C (2026-11-09) ──
    'Hàm băm là một quy tắc cố định biến mọi dãy byte thành 256 bit, tức 64 ký tự mười sáu, và bài này chỉ hiện 12 ký tự đầu cho gọn.':
        'ASR chép “Hàm Bâm là một quy tắc cố định biến mọi dãy bay thành 256 bit, tức 64 ký tự 16, và bài này chỉ hiện 12 ký tự đầu cho gọn.” (0.949): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: băm/bâm — NOT_VERIFIED bằng tai người',
    'Mã hoá ký tự là quy tắc đổi chữ thành byte, chữ ã có thể thành 1 hay 2 byte tuỳ quy tắc.':
        'ASR chép “Mã hóa ký tự là quy tắc đổi chữ thành bay, chữ à có thể thành 1 hay 2 bay tuy quy tắc.” (0.826): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: ã/à, tuỳ (trong “byte tuỳ” → “bay tuy”) — NOT_VERIFIED bằng tai người',
    'Kho mã giữ mọi phiên bản mãi mãi, một tệp 5 GB có 10 phiên bản có thể chiếm tới 50 GB, vì tệp dữ liệu lớn thường nén kém.':
        'ASR chép “Khó mã giữ mọi phiên bản mãi mãi, một tệp 5GB có 10 phiên bản có thể chiếm tới 50GB vì tệp dữ liệu lớn thường nán kém.” (0.935): lệch âm/thanh thuần Việt: kho/khó, nén/nán — NOT_VERIFIED bằng tai người',
    'Vì e mũ 0 bằng 1, lôgarit của 1 bằng 0, nên không đổi thì bằng 0.':
        'ASR chép “vì em mũ không bằng 1, lo ga tuyết của 1 bằng 0, nên không đổi thì bằng 0.” (0.833): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; thuật ngữ Việt hoá viết liền “lôgarit” (= lô-ga-rit), TTS đọc theo chính tả Việt, ASR viết “lo ga tuyết” — NOT_VERIFIED bằng tai người',
    'Trước hết ta cần hiểu bit và byte, hai đơn vị đo bộ nhớ.':
        'ASR chép “Trước hết ta cần hiểu biết và bay, hai đơn vị đo bộ nhớ.” (0.857): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: bit/biết — NOT_VERIFIED bằng tai người',
    'Một bit là một chữ số chỉ 0 hoặc 1, đơn vị nhỏ nhất máy lưu, và 8 bit gộp thành 1 byte.':
        'ASR chép “Một biết là một chữ số chỉ 0 hoặc 1 đơn vị nhỏ nhất máy lưu và 8 biết gột thành một bay.” (0.826): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: bit/biết, bit gộp/biết gột — NOT_VERIFIED bằng tai người',
    # ── NET dựng lại sau đọc kiểm C (2026-11-09) ──
    'Khi đó Z chỉ báo vô cùng cho X, còn báo cho Y một cách bình thường, dù đường của Z đi qua X rồi vòng về chính Y.':
        'ASR chép “Khi đó, Jack chỉ báo vô cùng cho ít, còn báo cho y một cách bình thường, dù đường của Jack đi qua ít rồi vòng về chính y.” (0.931): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    # ── RLN dựng lại sau đọc kiểm C (2026-11-09) ──
    'Ví dụ e mũ 2 phẩy 3 xấp xỉ 10, nên lôgarit của 10 khoảng 2 phẩy 3.':
        'ASR chép “Ví dụ E mũ 2,3 xếp xỉ 10, nên logic của 10 khoảng 2,3.” (0.889): thuật ngữ Việt hoá viết liền “lôgarit” (= lô-ga-rit), TTS đọc theo chính tả Việt, ASR viết “logic”; lệch âm/thanh thuần Việt: xấp/xếp — NOT_VERIFIED bằng tai người',
    'Ba tác giả đặt ra công thức này năm 2002 viết căn của 2 nhân lôgarit t chia N.':
        'ASR chép “Ba tác giả đặt ra công thức này năm 2002 viết căng của hai nhân Logatrix T-N.” (0.894): thuật ngữ Việt hoá viết liền “lôgarit” (= lô-ga-rit), TTS đọc theo chính tả Việt, ASR viết “logatrix”; lệch âm/thanh thuần Việt: căn/căng, chia/∅ — NOT_VERIFIED bằng tai người',
    'Tung 4 lần ra ngửa, sấp, ngửa, ngửa thì trung bình là 14 chia 4, bằng 3 phẩy 5, vẫn còn lệch.':
        'ASR chép “Tùng 4 lần tra ngửa, sắp, ngửa, ngửa thì trung bình là 14 chi 4, bằng 3,5 vẫn còn lịch.” (0.783): lệch âm/thanh thuần Việt: tung/tùng, ra/tra, sấp/sắp, chia/chi, lệch/lịch — NOT_VERIFIED bằng tai người',
    'Làm thử với x bằng 2, theta bằng 1, y bằng 4, độ dốc là âm 2 nhân 2, bằng âm 4.':
        'ASR chép “Làm thử với x bằng 2, teta bằng 1, y bằng 4, độ dốc là âm 2 nhân 2, bằng âm 4.” (0.955): “theta” đọc theo luật lexicon (lexicon_vi.RLN.yaml: “tê-ta”), ASR viết “teta” — NOT_VERIFIED bằng tai người',
    'Kiểm bằng cách nhích theta lên 1 phẩy 01, sai số giảm từ 2 xuống 1 phẩy 9602, tức khoảng âm 4 cho mỗi đơn vị.':
        'ASR chép “Kiểm bằng cách nhất θ lên 1,01, sai số giảm từ 2 xuống 1,90602 tức khoảng âm 4 cho mỗi đơn vị.” (0.921): “theta” đọc theo luật lexicon (lexicon_vi.RLN.yaml: “tê-ta”), ASR viết “nhất θ” — NOT_VERIFIED bằng tai người',
    'Hàm này biến mọi số thực thành một số giữa 0 và 1, nên dùng làm xác suất được, và tại theta bằng 0 nó bằng 1 chia 2, tức 0 phẩy 5.':
        'ASR chép “Hàm này biến mọi số thực thành một số giữa 0 và 1 nên dùng làm xa xuất được và tại θ bằng không nó bằng 1 chi 2, tức 0,5.” (0.909): “theta” đọc theo luật lexicon (lexicon_vi.RLN.yaml: “tê-ta”), ASR viết “θ”; lệch âm/thanh thuần Việt: xác/xa, chia/chi — NOT_VERIFIED bằng tai người',
    'Đạo hàm của nó bằng chính nó nhân 1 trừ nó, nên theo quy tắc vừa nêu, lôgarit của hàm chữ S có đạo hàm bằng 1 trừ hàm đó.':
        'ASR chép “Đạo hàm của nó bằng chính nó nhân một trừ nó, nên theo quy tắc vừa nêu, Logatrix của hàm chữ S có đạo hàm bằng một trừ hàm đó.” (0.967): thuật ngữ Việt hoá viết liền “lôgarit” (= lô-ga-rit), TTS đọc theo chính tả Việt, ASR viết “logatrix” — NOT_VERIFIED bằng tai người',
    'Làm thử ở theta bằng 0 với hành động một, gradient của pi là 0 phẩy 25, còn pi là 0 phẩy 5.':
        'ASR chép “Làm thử ở θ bằng không với hành động 1, gradient của pi là 0,25, còn pi là 0,5.” (0.945): tê-ta theo lexicon RBM/ROB, ASR viết “theta/teta” — NOT_VERIFIED bằng tai người',
    'Vậy gradient của J là kỳ vọng của G nhân gradient của lôgarit pi.':
        'ASR chép “Vậy gradient của dì là kỳ vọng của dây nhân gradient của logarithpy.” (0.857): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; pi (π) ASR viết “P/π”; thuật ngữ Việt hoá viết liền “lôgarit” (= lô-ga-rit), TTS đọc theo chính tả Việt, ASR viết “logarithpy” — NOT_VERIFIED bằng tai người',
    'Gradient lôgarit pi là đạo hàm theo theta của lôgarit xác suất, với hai hành động thì của hành động một bằng 1 trừ hàm chữ S của theta, tức 0 phẩy 5 khi theta bằng 0.':
        'ASR chép “Gradient Logarith P là đạo hàm theo Teta của Logarith sát xuất, với hai hành động thì có hành động một bằng một trừ hàm chữ S của Teta, tức 0,5 khi Teta bằng 0.” (0.815): pi (π) ASR viết “P/π”; tê-ta theo lexicon RBM/ROB, ASR viết “theta/teta”; lệch âm/thanh thuần Việt: xác/sát, của/có — NOT_VERIFIED bằng tai người',
    'Lôgarit của 1 bằng 0, lôgarit của 10 xấp xỉ 2 phẩy 303, và âm lôgarit của 0 phẩy 731 xấp xỉ 0 phẩy 313.':
        'ASR chép “Logarith của 1 bằng 0, Logarith của 10 sắp sĩ 2,303 và âm Logarith của 0,731 sắp sĩ 0,313.” (0.788): “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; lệch âm/thanh thuần Việt: xấp xỉ/sắp sĩ, không (trong “không phẩy” → “”), xấp xỉ không (trong “xấp xỉ không phẩy” → “sắp sĩ”) — NOT_VERIFIED bằng tai người',
    'Công thức là w thay bằng w trừ ê-ta nhân đạo hàm, với ê-ta là tốc độ học.':
        'ASR chép “Công thức là v kết thay bằng v kết trừ eta nhân đạo hàm, với eta là tốc độ học.” (0.909): chữ w đọc “vê kép” (luật chung), ASR viết tách chữ — NOT_VERIFIED bằng tai người',
    'Ví dụ hàm w bình phương trừ 6w có đạo hàm 2w trừ 6.':
        'ASR chép “Ví dụ hàm v kép bình phương trừ 6 về đúc có đạo hàm 2 về đúc trừ 6.” (0.833): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    # ── SAR dựng lại sau đọc kiểm C (2026-11-09) ──
    'Bit là một chữ số nhị phân, 0 hoặc 1, còn 1 byte gồm 8 bit, đủ ghi một chữ cái không dấu.':
        'ASR chép “Biết là một chữ số nhị phân, không hoặc một, còn một bai gồm 8 biết, đủ ghi một chữ cái không giấu.” (0.87): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: bit/biết, bit/biết — NOT_VERIFIED bằng tai người',
    'Dung lượng lưu trữ tính bằng byte, còn tốc độ đường truyền tính bằng bit mỗi giây.':
        'ASR chép “Dung lượng lưu trữ tính bằng vai, còn tốc độ đường truyền tính bằng bit mỗi giây.” (0.941): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Đó là vì 2314 phẩy 8 nhân 50 KB là khoảng 115 phẩy 7 MB mỗi giây, nhân 8 để đổi sang bit.':
        'ASR chép “Đó là vì 2.314,8 x 50 kB là khoảng 115,7 MB mỗi giây, nhần 8 để đổi sang bit.” (0.938): lệch âm/thanh thuần Việt: nhân/x, nhân/nhần — NOT_VERIFIED bằng tai người',
    'Có 7 phẩy 3 tê-ra-byte dữ liệu, sao chép 3 bản là 21 phẩy 9 tê-ra-byte, đã gấp 3 con số thô.':
        'ASR chép “Có 7,3 terabyte dữ liệu, sau chép 3 bản là 21,9 terabyte, đã gấp 3 con số thô.” (0.808): “tê-ra-byte” đọc tách âm tiết (đã dựng ở OSY/NET), ASR viết “TB/terabyte”; lệch âm/thanh thuần Việt: sao/sau — NOT_VERIFIED bằng tai người',
    'Mã hoá biến dữ liệu thành dạng chỉ ai có khoá mới đọc được.':
        'ASR chép “Mả hóa biến dữ liệu thanh vàng chị ai có khóa mới đọc được.” (0.714): lệch âm/thanh thuần Việt: mã/mả, thành dạng chỉ/thanh vàng chị — NOT_VERIFIED bằng tai người',
    'Va chạm là khi mã vừa sinh trùng một mã đã có, và mã thứ i trùng một trong i trừ 1 mã trước với xác suất không quá i trừ 1 chia N.':
        'ASR chép “Va chạm là khi mã vừa sinh trùng mục mã đã có và mã thứ y trùng mục trong y trường mục mã trước với sát suất không quá y trường mục chia n.” (0.794): lệch âm/thanh thuần Việt: một/mục, một/mục, trừ một/trường mục, xác/sát, trừ một/trường mục — NOT_VERIFIED bằng tai người',
    # ── SEC dựng lại sau đọc kiểm C (2026-11-09) ──
    'Trước hết, ta cần hiểu cách hệ điều hành ghi quyền trên một tệp.':
        'ASR chép “Trước hết, ta cần hiểu cách thể điều hành di quyền trên một tập.” (0.786): lệch âm/thanh thuần Việt: hệ/thể, ghi/di, tệp/tập — NOT_VERIFIED bằng tai người',
    'Mã hoá đối xứng là hai bên dùng chung một khoá để mã và giải mã, khoá 16 byte dài 16 nhân 8 bằng 128 bit.':
        'ASR chép “Mả hóa đối xứng là hai bên dùng chung một khóa để mã và giải mã. Khóa 16 bay dài 16 nhân 8 bằng 128 bit.” (0.938): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: mã/mả — NOT_VERIFIED bằng tai người',
    'Với chế độ bộ đếm, lật bit nào ở bản mã là lật đúng bit đó ở bản rõ, chẳng hạn lật 2 bit của một byte biến chữ số 9 thành 5, mà người nhận không biết.':
        'ASR chép “Với chế độ bộ đếm, lật biết nào ở bản mã là lật đúng biết đó ở bản rõ, chẳng hạn lật 2 biết của một bài biến chữ số 9 thành 5 mà người nhận không biết.” (0.895): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: bit/biết, bit/biết, bit/biết — NOT_VERIFIED bằng tai người',
    'Cách đơn giản nhất là cộng mã các byte rồi lấy dư khi chia 256, chuyển 100 cho 61, còn chuyển 900 cho 69.':
        'ASR chép “Cách đơn giản nhất là cộng mã các bay rồi lấy dư khi chia 256, chuyển 100 cho 61, còn chuyển 900 cho 69.” (0.971): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Bộ nhớ là một dãy ô, mỗi ô chứa 1 byte và có một số thứ tự gọi là địa chỉ, còn mảng là một dải ô liền nhau.':
        'ASR chép “Bộ nhớ là một giải ô, mỗi ô chứu một bay và có một số thứ tự gọi là địa chỉ, còn mảng là một giải ô liền nhau.” (0.897): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: dãy/giải, chứa/chứu — NOT_VERIFIED bằng tai người',
    'Mảng 16 byte đặt ở địa chỉ 100 chiếm tới ô 100 cộng 16 trừ 1, tức ô 115.':
        'ASR chép “Mảng 16 bay đặt ở địa chỉ 109 tới ô 100 cộng 16-1, tức ô 115.” (0.885): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: chiếm/linh chín, trừ/∅ — NOT_VERIFIED bằng tai người',
    'Vì vậy ghi 20 byte từ ô 100 sẽ tới ô 119, tràn sang 4 ô hàng xóm.':
        'ASR chép “Vì vậy, ghi 20 bay từ ô 100 sẽ tới ô 119 tràn sang 4 ô hàng xóm.” (0.957): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Hệ điều hành chia bộ nhớ thành từng khúc gọi là trang, thường dài 4096 byte, mỗi trang có cờ quyền đọc, ghi và chạy.':
        'ASR chép “Hệ điều hành chi bộ nhớ thành từng khúc gọi là trang, thường dài 4.096 bay, mỗi trang có cờ quyền đọc, ghi và chạy.” (0.935): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: chia/chi — NOT_VERIFIED bằng tai người',
    # ── RBM dựng lại sau đọc kiểm C (2026-11-09) ──
    'Ở đây cos của 180 độ trừ theta 2 bằng âm cos theta 2, vì mũi tên lật sang phía bên kia thì bóng trên trục ngang đổi dấu.':
        'ASR chép “Ở đây cô xin của 180 độ trừ teta 2 bằng âm cô xin teta 2 vì mũi tên lật sang phía bên kia thì bóng trên trục ngang đổ dấu.” (0.886): tê-ta theo lexicon RBM/ROB, ASR viết “theta/teta”; lệch âm/thanh thuần Việt: đổi/đổ — NOT_VERIFIED bằng tai người',
    'Để so sánh, a-tan của một số t là góc nằm giữa âm 90 độ và 90 độ mà sin chia cos bằng t, và với điểm x, y thì sin chia cos chính là y chia x.':
        'ASR chép “Để so sánh, a tan của một số t là góc nằm giữa âm 90 độ và 90 độ mà sinh chia cô sinh bằng t và với điểm í, i thì sinh chia cô sinh chính là í chia í.” (0.837): sin đọc thô, ASR viết “sinh” (gần âm); chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: i/í — NOT_VERIFIED bằng tai người',
    'Ví dụ a-tan của 1 là 45 độ, vì sin và cos của 45 độ cùng bằng 0 phẩy 707.':
        'ASR chép “Ví dụ A tan của một là 45 độ, vì sinh và cô sinh của 45 độ cùng bằng 0.707.” (0.893): sin đọc thô, ASR viết “sinh” (gần âm); “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; lệch âm/thanh thuần Việt: không (trong “không phẩy” → “”) — NOT_VERIFIED bằng tai người',
    'Ví dụ u bình phương có đạo hàm 2 u, và tại u bằng 2, nhích 0 phẩy 001 cho tỉ số 4 phẩy 001, rất gần 2 nhân 2.':
        'ASR chép “Ví dụ u bình phương có đạo hàm 2u và tại u bằng 2, nhất 0.001 cho tỷ số 4.001, rất gần 2x2.” (0.787): “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; “tỉ” ASR viết chính tả “tỷ” (cùng âm); lệch âm/thanh thuần Việt: nhích không (trong “nhích không phẩy” → “nhất”), nhân/x — NOT_VERIFIED bằng tai người',
    'Đạo hàm của sin u là cos u, thử tại u bằng 0 phẩy 5, tỉ số ra 0 phẩy 8773, sát cos của 0 phẩy 5 là 0 phẩy 8776.':
        'ASR chép “Đạo hàm của sinh u là cô sinh u, thử tài u bằng 0,5, tỷ số ra 0,8773, sát cô sinh của 0,5 là 0,8776.” (0.889): sin đọc thô, ASR viết “sinh” (gần âm); “tỉ” ASR viết chính tả “tỷ” (cùng âm); lệch âm/thanh thuần Việt: tại/tài — NOT_VERIFIED bằng tai người',
    'Đạo hàm của cos u là âm sin u, tỉ số ra âm 0 phẩy 4799, sát âm sin của 0 phẩy 5 là âm 0 phẩy 4794.':
        'ASR chép “Đạo hàm của cô sinh u là âm sinh u, tỷ số ra âm 0,4799, sát âm sinh của 0,5 là âm 0,4794.” (0.902): sin đọc thô, ASR viết “sinh” (gần âm); “tỉ” ASR viết chính tả “tỷ” (cùng âm) — NOT_VERIFIED bằng tai người',
    'Hai quy tắc của sin và cos chỉ đúng khi góc đo bằng radian, với 180 độ bằng pi radian, nên 1 độ xấp xỉ 0 phẩy 01745 radian.':
        'ASR chép “Hai quy tác của sinh và cô sinh chỉ đúng khi góc đo bằng radian với 180 độ bằng pi radian nên 1 độ sắp xỉ 0,01745 radian.” (0.897): sin đọc thô, ASR viết “sinh” (gần âm); lệch âm/thanh thuần Việt: tắc/tác, xấp/sắp — NOT_VERIFIED bằng tai người',
    'Theo quy tắc chuỗi vừa ôn, x phẩy bằng đạo hàm riêng của x theo theta 1 nhân theta 1 phẩy, cộng đạo hàm riêng theo theta 2 nhân theta 2 phẩy.':
        'ASR chép “Theo quy tắc chuỗi vừa ôn, ít phải bằng đạo hàm riêng của ít theo Teta 1 nhân Teta 1 phải cộng đạo hàm riêng theo Teta 2 nhân Teta 2 phải.” (0.781): “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; “theta” đọc theo luật lexicon (lexicon_vi.RBM.yaml: “tê-ta”), ASR viết “teta” — NOT_VERIFIED bằng tai người',
    'Lấy ví dụ ô trên bên trái, x bằng L 1 cos theta 1 cộng L 2 cos của theta 1 cộng theta 2, ta giữ theta 2 đứng yên và lấy đạo hàm theo theta 1.':
        'ASR chép “Lấy ví dụ O trên bên trái, ít bằng L1 cos teta 1 cộng L2 cos của teta 1 cộng teta 2, ta giữ teta 2 đứng yên và lấy đạo hàm theo teta 1.” (0.838): “ô” (ô lưới) ASR viết chữ “O”; “theta” đọc theo luật lexicon (lexicon_vi.RBM.yaml: “tê-ta”), ASR viết “teta” — NOT_VERIFIED bằng tai người',
    'Đạo hàm của cos là âm sin, nên ô đó bằng âm L 1 s 1 trừ L 2 s 1 2.':
        'ASR chép “Đạo hàm của cô sinh là âm sinh nên ô đó bằng âm L1S1 trừ L2S12.” (0.87): sin đọc thô, ASR viết “sinh” (gần âm); lệch âm/thanh thuần Việt: một/mười — NOT_VERIFIED bằng tai người',
    'Điều thứ hai, lũy thừa là nhân lặp lại, còn mũ âm nghĩa là chia, nên e mũ âm 1 là 1 chia e.':
        'ASR chép “Điều thứ 2, lũy thừa là nhân lập lại, còn mũ âm nghĩa là chia, nên em mũ âm 1 là mục chia.” (0.851): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: lặp/lập, một/mục — NOT_VERIFIED bằng tai người',
    'Với hệ x phẩy bằng lambda x, trong đó lambda là một hằng số, thay bốn độ dốc vào công thức, ta thấy mỗi bước RK4 nhân x với một hệ số cố định.':
        'ASR chép “Với hệ ích phải bằng lambda ích, trong đó lambda là 1 hàng số, thay 4 độ giúp vào công thức, ta thấy mỗi bước error ca 4 nhân ích với 1 hệ số cố định.” (0.883): “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; “rk4” đọc theo luật lexicon (lexicon_vi.RBM.yaml: “e rờ ca 4”), ASR viết “error”; lệch âm/thanh thuần Việt: hằng/hàng, dốc/giúp — NOT_VERIFIED bằng tai người',
    'Nếu v là vector riêng của A với trị riêng lambda, như phần ôn đầu bài, ta thử x của t bằng e mũ lambda t nhân v.':
        'ASR chép “Nếu ve là vét tơ riêng của A với trị riêng lambda, như phần ôn đầu bài, ta thử ích của tê bằng e mũ lambda tê nhân ve.” (0.935): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Nếu trị riêng lặp mà thiếu vector riêng thì có thêm số hạng t nhân e mũ lambda t, nhưng kết luận vẫn giữ, hệ ổn định khi mọi trị riêng đều có phần thực âm.':
        'ASR chép “Nếu trị riêng lặp mà thiếu vét tơ riêng thì có thêm số hạng tây nhân e mũ lambda tê nhưng kết luận vẫn giữ, hề ổn định khi mọi trị riêng đều có phần thực âm.” (0.947): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: hệ/hề — NOT_VERIFIED bằng tai người',
    'Với trị riêng a cộng trừ b i, e mũ lambda t bằng e mũ a t nhân một tổ hợp của cos và sin của b t, theo công thức Euler, nêu không chứng minh.':
        'ASR chép “Với trị riêng a cộng trừ bi, e mũ lambda t bằng e mũ a t nhân một tổ hợp của cô sinh và sinh của bt, theo công thức ơ le, nèo không chứng minh.” (0.923): sin đọc thô, ASR viết “sinh” (gần âm); lệch âm/thanh thuần Việt: nêu/nèo — NOT_VERIFIED bằng tai người',
    'Vậy hệ liên tục ổn định với mọi a dương, nhưng mô phỏng bằng Euler chỉ ổn định khi bước nhỏ hơn 2 chia a.':
        'ASR chép “Vậy hệ liên tục ổn định với mọi a dương, nhưng mô phỏng bằng ơ le chỉ ổn định khi bước nhỏ hơn hai chia.” (0.98): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Ví dụ nhỏ với 4 mẫu 1, 0, âm 1, 0, tức một dao động cos, C 1 bằng 1 cộng 1, bằng 2, còn S 1 bằng 0.':
        'ASR chép “Ví dụ nhỏ với 4 mẫu 1, 0, âm 1, 0, tức 1 giao động cô sinh C1 bằng 1 cộng 1, bằng 2, còn S1 bằng 0.” (0.967): sin đọc thô, ASR viết “sinh” (gần âm) — NOT_VERIFIED bằng tai người',
    'Cuối cùng chốt B bằng 3, đường ngắn nhất tới B là đi vòng qua A.':
        'ASR chép “Cuối cùng chốt b bằng 3, đường ngắn nhất tới b là đi vòng qua.” (0.968): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Manhattan cũng thoả, vì mỗi bước làm nó giảm nhiều nhất 1.':
        'ASR chép “Mang hát tần cũng thỏa, vì mỗi bước làm nó giảm nhiều nhất một.” (0.929): Manhattan đọc “Man-hát-tần” theo lexicon chung, ASR viết “mang hát tân/tầng” — NOT_VERIFIED bằng tai người',
    'Nếu độ lệch chuẩn nhỏ nhất là 0 phẩy 002 mét, tỉ số thành 10 mũ 8, vượt 2 mũ 24, khi đó nên chọn dạng căn bậc hai như máy bay năm 1972, hoặc dạng U D.':
        'ASR chép “Nếu độ lệch chuẩn nhỏ nhất là 0,002 mét, tỷ số thành 10 mũ 8 vượt 2 mũ 24, khi đó nên chọn dạng căn bật 2 như máy bay năm 1972 hoặc dạng UV.” (0.899): “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; “tỉ” ASR viết chính tả “tỷ” (cùng âm); chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: không (trong “không phẩy” → “”), bậc/bật — NOT_VERIFIED bằng tai người',
    # ── AIF dựng lại sau đọc kiểm C (2026-11-09) ──
    'Bài ba, dùng quá trình quyết định Markov như ở bài 12, gồm trạng thái, hành động có xác suất chuyển, và thưởng, vì hành động không chắc thành công.':
        'ASR chép “Bài 3, dùng quá trình quyết định macCop như ở bài 12, gồm trạng thái, hành động có xác xuất chuyển và thưởng vì hành động không chắc thành công.” (0.968): “markov” đọc theo luật lexicon (lexicon_vi.yaml: “Mác-cốp”), ASR viết “maccop” — NOT_VERIFIED bằng tai người',
    # ── BCH dựng lại sau đọc kiểm C (2026-11-09) ──
    'Vì sao lại là 1 chia p?':
        'ASR chép “Vì sao lại là một chip ấy?” (0.714): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: chia (trong “chia p” → “chip ấy”) — NOT_VERIFIED bằng tai người',
    # ── CLC dựng lại sau đọc kiểm C (2026-11-09) ──
    # ── CLD dựng lại sau đọc kiểm C (2026-11-09) ──
    'Dựng một máy ảo cho mỗi chương trình thì nặng, mỗi máy ảo thường cả GB và khởi động mất hàng chục giây, tuỳ máy.':
        'ASR chép “Dựng một máy ảo cho mỗi chương trình thì nặng, mỗi máy ảo thường cả Gigabyte và khởi động mất hàng chục giây, tùy máy.” (0.96): GB đọc “ghi-ga-byte” theo lexicon của khoá, ASR viết “GB/gigabyte” — NOT_VERIFIED bằng tai người',
    'Hãy đặt yêu cầu theo mức dùng đo được, chẳng hạn phân vị 90, tức mức mà 90 phần trăm số lần đo Pod dùng không vượt quá, và giới hạn cao hơn một chút.':
        'ASR chép “Hãy đặt yêu cầu theo mức dùng đo được, chẳng hạn phân vị 90, tức mức mà 90% số lần đo pốt dùng không vượt quá và giới hạn cao hơn một chút.” (0.973): Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút) — NOT_VERIFIED bằng tai người',
    # ── DAN dựng lại sau đọc kiểm C (2026-11-09) ──
    # ── DEN dựng lại sau đọc kiểm C (2026-11-09) ──
    'Đĩa không đọc từng ô lẻ, mà đọc theo từng đoạn liền nhau gọi là trang, ví dụ mỗi trang 4096 byte, nên muốn lấy một ô 8 byte thì cả trang chứa nó được đọc lên.':
        'ASR chép “Đĩa không đọc từng ô lẻ, mà đọc theo từng đoạn liền nhau gọi là trang, ví dụ mỗi trang 4.096 bay, nền muốn lấy một ô 8 bay thì cả trang chứa nó được đọc lên.” (0.93): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: nên (trong “byte nên” → “bay nền”) — NOT_VERIFIED bằng tai người',
    'Một trang 4096 byte chứa 4096 chia 8, bằng 512 ô.':
        'ASR chép “1 trang 4.096 bài chứa 4.096 chia 8, bằng 512 ô.” (0.962): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Nếu cả 512 ô đều là thứ ta cần thì một lần đọc được 512 ô có ích, còn nếu chỉ 1 ô có ích thì 4088 byte còn lại bị đọc phí.':
        'ASR chép “Nếu cả 512 ô đều là thứ ta cần thì một lần đọc được 512 ô có ít, còn nếu chỉ một ô có ít thì 4.088 bay còn lại bị đọc phí.” (0.978): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Đĩa đọc ghi theo trang, ví dụ mỗi trang 4096 byte, và mỗi nút của cây là một trang, chứa nhiều khoá đã sắp cùng các con trỏ xuống nút con, còn lá chứa bản ghi.':
        'ASR chép “Để đọc ghi theo trang, ví dụ mỗi trang 4096 by và mỗi nút của cây là một trang, chứa nhiều khóa đã sắp cùng các con trỏ xuống nút con, còn lá chứa bản ghi.” (0.952): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: đĩa/để — NOT_VERIFIED bằng tai người',
    'Lỗi thứ nhất, tưởng cây gộp theo nhật ký không khuếch đại ghi, trong khi nó vẫn ghi lại mỗi byte nhiều lần.':
        'ASR chép “Lỗi thứ nhất, tưởng cây gột theo nhật ký không khuết đại ghi, trong khi nó vẫn ghi lại mỗi bay nhiều lần.” (0.87): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: gộp/gột, khuếch/khuết — NOT_VERIFIED bằng tai người',
    'Ở ví dụ trên, mỗi byte bị ghi 6 lần chứ không phải 1.':
        'ASR chép “Ở ví dụ trên, mỗi bay bị ghi 6 lần chứ không phải 1.” (0.929): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Tổng số byte có thể ít hơn cây B, như 6 so với 40 phẩy 96 ở ví dụ, hoặc nhiều hơn, vì cách gộp theo tầng ghi lại nhiều hơn.':
        'ASR chép “Tổng số bài có thể ít hơn cây B, nhiều 6 so với 40,96 ở ví dụ, hoặc nhiều hơn, vì cách gột theo tần ghi lại nhiều hơn.” (0.882): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: như/nhiều, gộp/gột, tầng/tần — NOT_VERIFIED bằng tai người',
    'Trước hết, kho cột rộng là gì.':
        'ASR chép “Trước hết, kho cục động là gì?” (0.714): lệch âm/thanh thuần Việt: cột rộng/cục động — NOT_VERIFIED bằng tai người',
    'Trước hết, ta cần hiểu lôgarit tự nhiên.':
        'ASR chép “Trước hết, ta cần hiểu Logatrix tự nhiên.” (0.875): thuật ngữ Việt hoá viết liền “lôgarit” (= lô-ga-rit), TTS đọc theo chính tả Việt, ASR viết “logatrix” — NOT_VERIFIED bằng tai người',
    'Vì vậy người ta dùng lôgarit để thưởng điểm mà không để số lớn áp đảo.':
        'ASR chép “Vì vậy người ta dùng Logatrix để thưởng điểm mà không để số lớn áp đảo.” (0.938): thuật ngữ Việt hoá viết liền “lôgarit” (= lô-ga-rit), TTS đọc theo chính tả Việt, ASR viết “logatrix” — NOT_VERIFIED bằng tai người',
    'Vậy là không được, vì bảng 2 GB không vừa 1 GB bộ nhớ mỗi máy, nên phải xáo trộn, hoặc lọc bớt cột và dòng của bảng nhỏ trước.':
        'ASR chép “Vậy là không được, vì bảng 2GB không vừa 1GB bộ nhớ mỗi máy nên phải xáo trộn hoặc lọc bớt cột vài dòng của bảng nhỏ trước.” (0.967): lệch âm/thanh thuần Việt: và/vài — NOT_VERIFIED bằng tai người',
    # ── ESY dựng lại sau đọc kiểm C (2026-11-09) ──
    'Trước hết, ta cần hiểu các đơn vị đo bộ nhớ, bắt đầu từ bit, một chữ số chỉ nhận 0 hoặc 1, và 8 bit gộp lại thành một byte.':
        'ASR chép “Trước hết, ta cần hiểu các đơn vị đo bộ nhớ, bắt đầu từ bit, một chữ số chỉ nhận 0 hoặc 1 và 8 bit gột lại thành một bay.” (0.935): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: gộp/gột — NOT_VERIFIED bằng tai người',
    'Máy tính đếm theo lũy thừa của 2, nên một ki-lô-byte là 1024 byte, nên 2 ki-lô-byte là 2048 byte.':
        'ASR chép “Mẫy tính đến theo lũy thừa của 2 nên 1 kilobyte là 1.024 vai nên 2 kilobyte là 2.048 vai.” (0.765): KB đọc “ki-lô-byte” theo lexicon của khoá, ASR viết “kilobyte/kg”; byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: máy/mẫy, đếm/đến — NOT_VERIFIED bằng tai người',
    'Một vi điều khiển phổ biến chỉ có 2 ki-lô-byte bộ nhớ dữ liệu, so với 16 gi-ga-byte, ít hơn tám triệu lần.':
        'ASR chép “Một vi điều khiển phổ biến chỉ có 2 kilobytes bộ nhớ dữ liệu so với 16 GB, ít hơn 8 triệu lần.” (0.846): KB đọc “ki-lô-byte” theo lexicon của khoá, ASR viết “kilobyte/kg”; GB đọc “ghi-ga-byte” theo lexicon của khoá, ASR viết “GB/gigabyte”; lệch âm/thanh thuần Việt: gi (trong “gi ga byte” → “gb”) — NOT_VERIFIED bằng tai người',
    'Bù lại, nó rẻ, tốn rất ít điện, khởi động gần như ngay lập tức, và chương trình nằm riêng trong 32 ki-lô-byte bộ nhớ flash.':
        'ASR chép “Bù lại, nó rẻ, tốn rất ít điện, khởi động gần như ngay lập tức và chương trình nằm riêng trong 32 kg bộ nhớ Phlax.” (0.897): KB đọc “ki-lô-byte” theo lexicon của khoá, ASR viết “kilobyte/kg”; từ mượn/tên riêng “flash” đọc thô (không có luật lexicon), ASR viết “phlax” — NOT_VERIFIED bằng tai người',
    'Vì 16 bằng 2 mũ 4, một chữ số hệ mười sáu đúng bằng 4 bit, và một byte 8 bit viết gọn bằng đúng hai chữ số, từ 0 0 tới F F.':
        'ASR chép “Vì 16 bằng 2 mũ 4, 1 chữ số hệ 16 đúng bằng 4 bit và 1 bai 8 bit viết gọn bằng đúng 2 chữ số từ 00 tới FF.” (0.957): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: không/∅ — NOT_VERIFIED bằng tai người',
    'Năm mẫu cách nhau 1 mi li giây phủ kín 5 mi li giây dội, nên khi đủ 5 mẫu liên tiếp giống nhau, ta coi phím đã hết nảy.':
        'ASR chép “5 mẫu cách nhau 1 mili dây phụ kín 5 mili dây dội, nên khi đủ 5 mẫu liên tiếp giống nhau, ta coi phím đã hết nảy.” (0.793): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; lệch âm/thanh thuần Việt: phủ (trong “mi li giây phủ” → “mili dây phụ”) — NOT_VERIFIED bằng tai người',
    'Với một sóng sin dùng hết thang đo, tỉ số tín hiệu trên nhiễu lượng tử xấp xỉ 6 phẩy 02 nhân n, cộng 1 phẩy 76, tính bằng đề-xi-ben.':
        'ASR chép “Với một sóng sinh dùng hết thang đo, tỷ số tín hiệu trên nhiễu lượng từ sắp xị 6,02n n cộng 1,76 tính bằng deciBand.” (0.758): sin đọc thô, ASR viết “sinh” (gần âm); “tỉ” ASR viết chính tả “tỷ” (cùng âm); lệch âm/thanh thuần Việt: tử xấp xỉ/từ sắp xị, nhân/n, đề xi ben/deciband — NOT_VERIFIED bằng tai người',
    'Bit chẵn lẻ, nếu có, là một bit thêm vào để bên nhận kiểm xem số bit 1 là chẵn hay lẻ.':
        'ASR chép “Biết chẳng lẽ, nếu có, là một biết thêm vào để bên nhận kiểm xem số biết 1 là chẳng hay lẽ.” (0.682): lệch âm/thanh thuần Việt: bit chẵn linh/biết chẳng lẽ, bit/biết, bit/biết, chẵn/chẳng, linh/lẽ — NOT_VERIFIED bằng tai người',
    'Bộ đệm vòng là một mảng chứa các byte chờ gửi, ghi tới cuối mảng thì quay lại đầu.':
        'ASR chép “Bộ đệm vòng là một mạng chứa các bay chờ gửi, vì tới cuối mạng thì quay lại đâu.” (0.737): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: mảng/mạng, ghi/vì, mảng/mạng, đầu/đâu — NOT_VERIFIED bằng tai người',
    'Kiểm bằng đường khác, vì công thức lô-ga-rít rất dễ bấm nhầm, ta cho điện áp đi từng na-nô giây.':
        'ASR chép “Kiểm bằng đường khác, vì công thức Logarith rất dễ bấm nhầm, ta cho điện app đi từng nano dây.” (0.744): “ki-lô-byte” đọc tách âm tiết, ASR viết “kg” rồi chép “byte” thành “bay/ba”; tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; lệch âm/thanh thuần Việt: ga rít (trong “lô ga rít” → “lôgarit”), áp/app — NOT_VERIFIED bằng tai người',
    'Phần sụn thật dài hàng trăm ki-lô-byte, nên người ta tính một bản tóm tắt ngắn của nó, gọi là giá trị băm, rồi ký lên bản tóm tắt đó.':
        'ASR chép “Phân sụng thật dài hàng trăm kilobyte nên người ta tính một bản tóm tắt ngắn của nó gọi là giá trị bâm, rồi ký lên bản tóm tắt đó.” (0.839): KB đọc “ki-lô-byte” theo lexicon của khoá, ASR viết “kilobyte/kg”; lệch âm/thanh thuần Việt: phần sụn/phân sụng, băm/bâm — NOT_VERIFIED bằng tai người',
    'Ở bài 14, ta luôn giữ một đường lui, hai phân vùng 400 cộng bộ nạp 32 là 832 ki-lô-byte, bản mới hỏng thì quay về bản cũ.':
        'ASR chép “Ở bài 14, ta luôn giữ một đường lui, hai phân vùng 400 cộng bộ nạp 32 là 832 kilobytes, bản mới hỏng thì quay về bản cũ.” (0.946): KB đọc “ki-lô-byte” theo lexicon của khoá, ASR viết “kilobyte/kg” — NOT_VERIFIED bằng tai người',
    # ── EVT dựng lại sau đọc kiểm C (2026-11-09) ──
    # ── LLM dựng lại sau đọc kiểm C (2026-11-09) ──
    'Trước hết, ta cần hiểu xác suất là gì.':
        'ASR chép “Trước hết, ta cần hiểu xa suốt là gì?” (0.778): lệch âm/thanh thuần Việt: xác suất/xa suốt — NOT_VERIFIED bằng tai người',
    'Lý do là 2 nhân 2 nhân 2 nhân 2 bằng 16.':
        'ASR chép “Lý do là 2 nhìn 2 nhìn 2 nhìn 2 bằng 16.” (0.769): lệch âm/thanh thuần Việt: nhân/nhìn, nhân/nhìn, nhân/nhìn — NOT_VERIFIED bằng tai người',
    'Thứ hai, máy lưu chữ thành byte, mỗi byte là một ô nhớ nhỏ chứa một số từ 0 tới 255.':
        'ASR chép “Thứ hai, máy lưu chữ thành bay. Mỗi bay là một ô nhớ nhỏ chiếu một số từ 0 tới 255.” (0.88): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: chứa/chiếu — NOT_VERIFIED bằng tai người',
    'Chuẩn lưu chữ phổ biến nhất quy định mỗi chữ cần mấy byte.':
        'ASR chép “chuẩn lưu chữ phổ biến nhất quy định mỗi chữ cần máy bay.” (0.846): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: mấy (trong “mấy byte” → “máy bay”) — NOT_VERIFIED bằng tai người',
    'Chữ a không dấu cần 1 byte, còn chữ ô hay chữ e huyền cần 2 byte.':
        'ASR chép “Chữ A không dấu cần một bay, còn chữ O hay chữ E huyền cần hai bay.” (0.824): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); “ô” (ô lưới) ASR viết chữ “O” — NOT_VERIFIED bằng tai người',
    'Byte là ô nhớ nhỏ nhất, chứa một số từ 0 tới 255.':
        'ASR chép “Bay là ô nhớ nhỏ nhất, chữ một số từ 0 tới 255.” (0.882): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: chứa/chữ — NOT_VERIFIED bằng tai người',
    'Tốc độ đọc ghi trên màn hình là số byte đọc được mỗi giây, ở đây là 10 mũ 12 byte mỗi giây.':
        'ASR chép “Tốc độ độc ghi trên màn hình là số bai độc được mỗi giây, ở đây là 10 mũ, 12 bai mỗi giây.” (0.833): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: đọc/độc, đọc (trong “byte đọc” → “bai độc”) — NOT_VERIFIED bằng tai người',
    'Một mi li giây là một phần nghìn giây.':
        'ASR chép “Một mili dây là một phần nghìn dây.” (0.706): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh — NOT_VERIFIED bằng tai người',
    'Trước hết, ta cần lôgarit tự nhiên.':
        'ASR chép “Trước hết, ta cần Logarets tự nhiên.” (0.857): thuật ngữ Việt hoá viết liền “lôgarit” (= lô-ga-rit), TTS đọc theo chính tả Việt, ASR viết “logarets” — NOT_VERIFIED bằng tai người',
    'Đại lượng này đo độ lệch giữa phân phối đáp án thật và phân phối của mô hình, bằng âm tổng của xác suất thật nhân lôgarit xác suất mô hình.':
        'ASR chép “Đại lượng này đo độ lệch giữa phân phối đáp án thật và phân phối của mô hình, bằng âm tổng của xác suất thật nhân Logatrix xác suất mô hình.” (0.968): thuật ngữ Việt hoá viết liền “lôgarit” (= lô-ga-rit), TTS đọc theo chính tả Việt, ASR viết “logatrix” — NOT_VERIFIED bằng tai người',
    'Mười sáu byte gồm 2 byte trọng số, 2 byte độ dốc, tức mức mất mát đổi khi nhích tham số một chút, và 4 byte bản sao chính xác.':
        'ASR chép “16 bai gồm 2 bai trọng số, 2 bai độ dốc, tức mức mất mát đổi khi nhất tham số một chút và 4 bai bản sao chính xác.” (0.833): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: nhích/nhất — NOT_VERIFIED bằng tai người',
    'Còn 8 byte là hai số mà thuật toán nhớ cho mỗi tham số, trung bình độ dốc và trung bình bình phương độ dốc.':
        'ASR chép “Còn 8 bai là 2 số mà thuộc toán nhớ cho mỗi tham số, Trung Bình Độ Dốc và Trung Bình Bình Phương Độ Dốc.” (0.92): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: thuật/thuộc — NOT_VERIFIED bằng tai người',
    'Nếu ma trận B có r cột, mỗi hàng của tích B nhân A là một tổ hợp của đúng r hàng của A.':
        'ASR chép “Nếu mà trận B có R cục, mỗi hàng của tích B nhân A là một tổ hợp của đúng R hàng qua.” (0.851): gam-ma (γ) ASR viết “gamma”; chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: cột/cục, của (trong “của a” → “qua”) — NOT_VERIFIED bằng tai người',
    'Tổng kết lại, tinh chỉnh toàn bộ tốn khoảng 16 byte mỗi tham số, còn hạng thấp chỉ học r nhân 2 d số.':
        'ASR chép “Tổng kết lại, tinh chỉnh toàn bộ tốn khoảng 16 bay mỗi thăm số, còn hạn thấp chỉ học R nhân 2D số.” (0.88): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: tham/thăm, hạng/hạn — NOT_VERIFIED bằng tai người',
    'Xác suất càng gần 1 thì âm lôgarit của nó càng gần 0, xác suất càng nhỏ thì âm lôgarit càng lớn, và đó là mất mát dùng trong bài.':
        'ASR chép “Sát suốt càng gần 1 thì âm Logatrix của nó càng gần 0, sát suốt càng nhỏ thì âm Logatrix càng lớn, và đó là mất mát dùng trong bài.” (0.8): thuật ngữ Việt hoá viết liền “lôgarit” (= lô-ga-rit), TTS đọc theo chính tả Việt, ASR viết “logatrix”; lệch âm/thanh thuần Việt: xác suất/sát suốt, xác suất/sát suốt — NOT_VERIFIED bằng tai người',
    'Vì sao có căn?':
        'ASR chép “Vì sao có căng?” (0.75): lệch âm/thanh thuần Việt: căn/căng — NOT_VERIFIED bằng tai người',
    'Điều thứ hai là tổng cấp số nhân, gọi S là tổng 1 cộng alpha cộng alpha bình phương, tới alpha mũ k.':
        'ASR chép “Điều thứ 2 là tổng cấp số nhân, gọi X là tổng 1 cộng an pha, cộng an pha bình phương, tới an pha mũ ca.” (0.816): alpha đọc thô (probe AIF p1: 7/8, bản chép “an pha / ANFA / α”) — NOT_VERIFIED bằng tai người',
    'Nhân cả hai vế với alpha, ta được alpha cộng alpha bình phương, tới alpha mũ k cộng 1.':
        'ASR chép “Nhân cả hai với với an pha, ta được an pha cộng an pha bình phương tới an pha mũ ca cộng 1.” (0.667): alpha đọc thô (probe AIF p1: 7/8, bản chép “an pha / ANFA / α”); lệch âm/thanh thuần Việt: vế/∅ — NOT_VERIFIED bằng tai người',
    'Trừ hai dòng thì mọi số hạng ở giữa triệt tiêu, còn S trừ alpha S bằng 1 trừ alpha mũ k cộng 1, nên S bằng 1 trừ alpha mũ k cộng 1, chia 1 trừ alpha.':
        'ASR chép “Trừ hai dòng thì mọi số hạn ở giữa trịt tiêu còn S trừ an pha S bằng một trừ an pha mũ ca cộng mục nên S bằng một trừ an pha mũ ca cộng mục chi một trừ an pha.” (0.725): alpha đọc thô (probe AIF p1: 7/8, bản chép “an pha / ANFA / α”); lệch âm/thanh thuần Việt: hạng/hạn, triệt/trịt, một/mục, một chia/mục chi — NOT_VERIFIED bằng tai người',
    'Cứ thế tới alpha mũ k, và cộng lại chính là tổng cấp số nhân ở trên.':
        'ASR chép “cứ thế tới an pha mũ ca và cộng lại chính là tổng cấp số nhân ở trên.” (0.914): alpha đọc thô (probe AIF p1: 7/8, bản chép “an pha / ANFA / α”) — NOT_VERIFIED bằng tai người',
    'Nửa byte mỗi tham số có thể làm mô hình kém đi ở một số việc như toán hay viết mã, và mức giảm tuỳ mô hình và cách lượng tử hoá.':
        'ASR chép “Nửa bay mỗi tham số có thể làm mô hình kém đi ở một số việc như toán hay viết mã, và mức giảm tùy mô hình và cách lượng tử hóa.” (0.969): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    # ── PAR dựng lại sau đọc kiểm C (2026-11-09) ──
    'Điều thứ hai là định luật Amdahl, và trước hết ta cần hiểu ý chính của nó.':
        'ASR chép “Điều thứ hai là định luật am đang, và trước hết ta cần hiểu ý chính của nó.” (0.944): “amdahl” đọc theo luật lexicon (lexicon_vi.PAR.yaml: “Am-đan”), ASR viết “đang” — NOT_VERIFIED bằng tai người',
    'Vì chương trình hay dùng lại dữ liệu vừa dùng và dữ liệu nằm ngay cạnh nó, gọi là tính cục bộ, bộ nhớ đệm chép cả một dòng 64 byte liền nhau, không chép từng byte.':
        'ASR chép “Vì chương trình hay dùng lại giữ liệu vừa dùng và giữ liệu nằm ngay cạnh nó, gọi là tính cuộc bộ, bộ nhớ đem chép cả 1 dòng 64 bai liền nhau, không chép từng bay.” (0.897): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: cục/cuộc, đệm/đem — NOT_VERIFIED bằng tai người',
    'Một dòng 64 byte chứa được 8 số loại 8 byte, nên đọc 8 số liền nhau chỉ tốn một lần chép dòng thay vì 8 lần.':
        'ASR chép “Một dòng 64 bay chứa được 8 số loại 8 bay, nền đọc 8 số liền nhau chỉ tốn một lần chép dòng thay vị 8 lần.” (0.862): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: nên (trong “byte nên” → “bay nền”), vì/vị — NOT_VERIFIED bằng tai người',
    'Mỗi lượt chỉ dùng x i và y i của chính nó, nên vector hoá được, mỗi phép toán mất 125 lệnh thay vì 1000, ít hơn 8 lần.':
        'ASR chép “Mỗi lượt chỉ dùng ít y và ít y của chính nó nên vẽ tơ hóa được, mỗi phép toán mất 125 lệnh thay vì 1 nghìn, ít hơn 8 lần.” (0.943): lệch âm/thanh thuần Việt: i/x, véc/vẽ — NOT_VERIFIED bằng tai người',
    'Phần thứ hai là dung lượng chia thông lượng, với thông lượng là số byte đường truyền chở được mỗi giây.':
        'ASR chép “Phần thứ hai là dung lượng chia thông lượng, với thông lượng là số bay đường truyền chở được mỗi giây.” (0.952): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8) — NOT_VERIFIED bằng tai người',
    'Gửi 1 GB qua đường 10 GB mỗi giây với độ trễ 1 mi li giây mất 0 phẩy 1 cộng 0 phẩy 001, bằng 0 phẩy 101 giây.':
        'ASR chép “Gửi 1 GB qua đường 10 GB mỗi dây với độ trễ 1 mili dây mất không phải 1 cọng 0.001 bằng 0.100 Linh 1 dây.” (0.78): tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh; “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; lệch âm/thanh thuần Việt: cộng không (trong “cộng không phẩy” → “cọng”), không (trong “không phẩy” → “”) — NOT_VERIFIED bằng tai người',
    # ── SEP dựng lại sau đọc kiểm C (2026-11-09) ──
    # ── WEB dựng lại sau đọc kiểm C (2026-11-09) ──
    'Điều thứ hai, một dãy ngoặc gọi là lồng đúng khi ngoặc mở sau phải đóng trước.':
        'ASR chép “Điều thứ hai, một dãy hoặc gọi là lòng đúng khi hoặc mở sao phải đóng trước.” (0.765): lệch âm/thanh thuần Việt: ngoặc/hoặc, lồng/lòng, ngoặc/hoặc, sau/sao — NOT_VERIFIED bằng tai người',
    'Trình duyệt tải trước liên kết, công cụ quét tự đi theo liên kết, và máy trung gian đứng giữa trình duyệt với máy chủ được phép tự gửi lại GET bất cứ lúc nào.':
        'ASR chép “Trình duyệt tải trước liên kết, công cụ quét tự đi theo liên kết và máy trung gian đứng giữa trình duyệt với máy chủ được phép tự gửi lại ghét bất cứ lúc nào.” (0.971): GET đọc “gét” theo lexicon WEB, ASR viết “ghét” — NOT_VERIFIED bằng tai người',
    'Mã truy cập là một chuỗi ngắn hạn gửi kèm mỗi yêu cầu API, đi cùng mã làm mới, dùng để xin mã truy cập mới khi mã cũ hết hạn.':
        'ASR chép “Mả truy cập là một chuỗi ngắn hàng gửi kè mỗi yêu cầu API, đi cùng mả làm mới, dùng để xin mả truy cập mới khi mả cũ hết hàng.” (0.774): lệch âm/thanh thuần Việt: mã/mả, hạn/hàng, kèm/kè, mã/mả, mã/mả, mã/mả, hạn/hàng — NOT_VERIFIED bằng tai người',
    'Khách hàng dùng điện thoại tầm trung, mạng di động yếu khoảng 200 KB mỗi giây, một số minh hoạ.':
        'ASR chép “Khách hàng dùng điện thoại tầm trung màng di động yếu khoảng 200 kB mỗi giây một số minh họa.” (0.952): lệch âm/thanh thuần Việt: mạng/màng — NOT_VERIFIED bằng tai người',
    'Ô nhập sai chỉ đổi viền đỏ, trong khi khoảng 4 tới 8 phần trăm nam giới, tuỳ nhóm dân, có rối loạn sắc giác đỏ lục.':
        'ASR chép “Ôn nhập sai chỉ đổi viền đỏ, trong khi khoảng 4 tới 8% nam giới, tuyên nhóm dân, có trối loạn sát giác đỏ lụt.” (0.815): “ô” (ô lưới) ASR viết chữ “O”; lệch âm/thanh thuần Việt: tuỳ/tuyên, rối/trối, sắc/sát, lục/lụt — NOT_VERIFIED bằng tai người',
    'Cửa sổ của TCP là lượng byte được gửi đi trước khi phải chờ xác nhận, lúc đầu nhỏ, và mỗi vòng suôn sẻ thì gấp đôi, gọi là khởi động chậm.':
        'ASR chép “Cửa sổ của TCP là lượng bay được gửi đi trước khi phải chờ xác nhận, lúc đầu nhỏ và mỗi vòng xung sẻ thì gấp đôi, gọi là khởi động chậm.” (0.938): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: suôn/xung — NOT_VERIFIED bằng tai người',
    'Làm thử với số minh hoạ, 100 yêu cầu, mỗi tiêu đề 500 byte, và cửa sổ đầu 10 gói, mỗi gói 1460 byte, nhân đôi mỗi vòng theo cách khởi động chậm.':
        'ASR chép “Làm thử với số minh họa, 100 yêu cầu, mỗi tiêu đề 500 by và cửa sổ đầu 10 gói, mỗi gói 1460 by, nhận đôi mỗi vòng theo cách khởi động chậm.” (0.925): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: nhân (trong “byte nhân” → “by nhận”) — NOT_VERIFIED bằng tai người',
    # ── AGT dựng lại sau đọc kiểm C (2026-11-09) ──
    'Đồ thị phụ thuộc có mỗi bước là một nút, tức một ô, và cạnh là mũi tên từ A tới B nếu B cần kết quả của A.':
        'ASR chép “Đồ thì phụ thuộc có mỗi bước là một nút, tức một ô, và cạnh là mũi tên từ A tới B nếu B cần kết quả qua.” (0.912): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: thị/thì, của (trong “của a” → “qua”) — NOT_VERIFIED bằng tai người',
    # ── GFX dựng lại sau đọc kiểm C (2026-11-09) ──
    'Điều thứ hai là hàm cạnh E, một biểu thức bậc nhất tính từ hai đỉnh của cạnh và toạ độ điểm p, cho biết p nằm ở phía nào của cạnh.':
        'ASR chép “Điều thứ hai là hàm cạnh E, một biểu thức bật nhất tính từ hai đỉnh của cạnh và tọa độ điểm T, cho biết T nằm ở phía nào của cạnh.” (0.906): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: bậc/bật — NOT_VERIFIED bằng tai người',
    'Ba hệ số k a, k d và k s từ 0 đến 1 là tỉ lệ ánh sáng môi trường, khuếch tán và bóng sáng mà vật liệu hắt lại.':
        'ASR chép “Ba hệ số Ka, Kj và Ks từ 0 đến 1 là tỷ lệ ánh sáng môi trường, khuết tán và bóng sáng mà vật liệu hát lại.” (0.852): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; “tỉ” ASR viết chính tả “tỷ” (cùng âm); lệch âm/thanh thuần Việt: khuếch/khuết, hắt/hát — NOT_VERIFIED bằng tai người',
    'Còn I a và I l lần lượt là cường độ của ánh sáng môi trường và của nguồn sáng.':
        'ASR chép “Còn YA và YL lần lượt là cường độ của ánh sáng môi trường và của nguồn sáng.” (0.842): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: i (trong “i a” → “ya”), i (trong “i l” → “yl”) — NOT_VERIFIED bằng tai người',
    'Biểu thức là F bằng F không cộng 1 trừ F không nhân với 1 trừ cosin góc tới mũ 5.':
        'ASR chép “Biểu thức là f bằng f không cộng 1 trừ f không nhân với 1 trừ cô sinh góc tới mũ năm.” (0.93): thuật ngữ Việt hoá viết liền “cosin” (= co-sin), TTS đọc theo chính tả Việt, ASR viết “cô sinh” — NOT_VERIFIED bằng tai người',
    # ── HCI dựng lại sau đọc kiểm C (2026-11-09) ──
    'Nhắc lại, thời gian đưa con trỏ tới một nút tăng theo lôgarit cơ số 2 của khoảng cách chia bề rộng cộng 1, nên nút càng xa và càng hẹp thì càng lâu.':
        'ASR chép “Nhắc lại, thời gian đưa con trỏ tới một nút tăng theo logatic cơ số 2 của khoảng cách chia bề động cộng 1, nền nút càng xa và càng hẹp thì càng lâu.” (0.912): thuật ngữ Việt hoá viết liền “lôgarit” (= lô-ga-rit), TTS đọc theo chính tả Việt, ASR viết “logatic”; lệch âm/thanh thuần Việt: rộng/động, nên/nền — NOT_VERIFIED bằng tai người',
    # ── ROB dựng lại sau đọc kiểm C (2026-11-09) ──
    'Điều thứ hai là bước Euler, cách tính dần một đại lượng khi biết tốc độ thay đổi của nó.':
        'ASR chép “Điều thứ 2 là bước ơ lê cách tính dần một đại lượng khi biết tốc độ thay đổi của nó.” (0.952): “euler” đọc theo luật lexicon (lexicon_vi.ROB.yaml: “Ơ-le”), ASR viết “lê” — NOT_VERIFIED bằng tai người',
    'Lý do là mũi tên dài 1 chỉ theo hướng tê-ta có bóng trên trục x dài cô-sin tê-ta, và bóng trên trục y dài sin tê-ta.':
        'ASR chép “Lý do là mũi tên dài một chỉ theo hướng teta có bóng trên trục ít dài cô sinh teta và bóng trên trục y dài sinh teta.” (0.78): tê-ta theo lexicon RBM/ROB, ASR viết “theta/teta”; sin đọc thô, ASR viết “sinh” (gần âm) — NOT_VERIFIED bằng tai người',
    'Ở đây tư thế gồm vị trí x, y cùng hướng đầu xe tê-ta, còn x phẩy là tốc độ thay đổi của x mỗi giây.':
        'ASR chép “Ở đây từ thế gồm vị trí ít, ít cùng hướng đầu xe teta, còn ít phải là tốc độ thay đổi của ít mỗi giây.” (0.83): tê-ta theo lexicon RBM/ROB, ASR viết “theta/teta”; “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; lệch âm/thanh thuần Việt: bốn/từ, i/x — NOT_VERIFIED bằng tai người',
    'Điều thứ hai, ta cần hiểu công thức Bayes, tin sau bằng tin trước nhân khả năng, rồi chuẩn hoá.':
        'ASR chép “Điều thứ 2, ta cần hiểu công thức bay x tin sau bằng tin trước nhân khả năng rồi chuẩn hóa.” (0.952): Bayes đọc “Bay-ét” theo lexicon chung (probe 3/8, NOT_VERIFIED), ASR viết “bay X/S” — NOT_VERIFIED bằng tai người',
    'Xem bộ lọc hạt làm việc với 4 hạt ở ô 1, 2, 4 và 5, mỗi hạt trọng số 0 phẩy 25, khi robot thấy cửa.':
        'ASR chép “Xem bộ lọc hạt làm việc với 4 hạt ở ôm 1, 2, 4 và 5, mỗi hạt trọng số 0,25 khi robot thấy cửa.” (0.966): “ô” (ô lưới) ASR viết chữ “O” — NOT_VERIFIED bằng tai người',
    'Hạt ở ô 2 và ô 5 đứng trước tường, nhân 0 phẩy 1 được 0 phẩy 025, chuẩn hoá còn khoảng 0 phẩy 056.':
        'ASR chép “Hạt ở O2 và O5 đứng trước tường, nhần 0,1 được 0,02 năm, chuẩn hóa còn khoảng 0,056.” (0.836): “ô” (ô lưới) ASR viết chữ “O”; “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; lệch âm/thanh thuần Việt: nhân/nhần, mươi/∅, không (trong “không phẩy” → “”) — NOT_VERIFIED bằng tai người',
    'Đạo hàm của cos là âm sin, thử số cho khoảng âm 0 phẩy 0005, gần bằng 0, đúng là âm sin 0.':
        'ASR chép “Đạo hàm của cô sinh là âm sinh, thử số cho khoảng âm 0.0005, gần bằng không, đúng là âm sinh không.” (0.851): sin đọc thô, ASR viết “sinh” (gần âm); “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải” — NOT_VERIFIED bằng tai người',
    'Còn đạo hàm của s cô-sin tê-ta theo tê-ta là âm s sin tê-ta, đúng như ô hàng một cột ba.':
        'ASR chép “Còn đạo hàm của echo sinh tê ta theo tê ta là âm s sinh tê ta, đúng như ô hàng một cột ba.” (0.857): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; sin đọc thô, ASR viết “sinh” (gần âm); lệch âm/thanh thuần Việt: cô (trong “s cô sin” → “echo sinh”) — NOT_VERIFIED bằng tai người',
    'Điều thứ hai, lôgarit tự nhiên của a là số mũ x sao cho e mũ x bằng a, với e là hằng số khoảng 2 phẩy 718.':
        'ASR chép “Điều thứ 2, Logatrix tự nhiên của A là số mũ ít sao cho E mũ ít bằng A, với E là hàng số khoảng 2,718.” (0.903): thuật ngữ Việt hoá viết liền “lôgarit” (= lô-ga-rit), TTS đọc theo chính tả Việt, ASR viết “logatrix”; “phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”; lệch âm/thanh thuần Việt: hằng/hàng — NOT_VERIFIED bằng tai người',
    'Ô A đã đi 2 và còn ước lượng 3, tổng là 5.':
        'ASR chép “OA đã đi 2 và còn gước lượng 3, tổng là 5.” (0.8): “ô” (ô lưới) ASR viết chữ “O”; chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: ước/gước — NOT_VERIFIED bằng tai người',
    'Ô B mới đi 1 nhưng còn ước lượng 5, tổng là 6, nên A sao mở ô A trước.':
        'ASR chép “OB mới đi một nhưng còn ước lượng 5, tổng là 6, nên A sao mở OA trước?” (0.842): “ô” (ô lưới) ASR viết chữ “O”; chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Ở đây v 0 là tốc độ hiện tại, h là chu kỳ, và ô-mê-ga cũng có một cửa sổ như vậy theo gia tốc góc tối đa.':
        'ASR chép “Ở đây V0 là tốc độ hiện tại, H là chu kỳ và Omega cũng có một cửa sổ như vậy theo gia tốc góc tối đa.” (0.931): ô-mê-ga (ω) đọc tách âm tiết, ASR viết “omega/ω” — NOT_VERIFIED bằng tai người',
    'Tịnh tiến nghĩa là lấy toạ độ điểm đích trừ đi toạ độ của xe, được hai hiệu số theo hai trục là d x và d y.':
        'ASR chép “Tình tiến nghĩa là lấy tọa độ điểm đích trừ đi tọa độ của xe, được hai hiệu số theo hai trục là GX và GY.” (0.852): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: tịnh/tình, i (trong “d i” → “gy”) — NOT_VERIFIED bằng tai người',
    # ── ACB dựng lại sau đọc mẫu D (2026-11-10) ──
    'Kafka là một hàng đợi sự kiện, chương trình này ghi sự kiện vào, chương trình khác đọc ra theo đúng thứ tự, và sự kiện được lưu lại nên đọc lại được.':
        'ASR chép “Cáp K là một hàng đợi sự kiện. Chương trình này ghi sự kiện vào, chương trình khác đọc ra theo đúng thứ tự và sự kiện được lưu lại nên đọc lại được.” (0.971): “kafka” đọc theo luật lexicon (lexicon_vi.ACB.yaml: “Cáp-ca”), ASR viết “k” — NOT_VERIFIED bằng tai người',
    'Công cụ bắt thay đổi dữ liệu đọc nhật ký thay đổi của cơ sở dữ liệu, và biến mỗi dòng mới thành một sự kiện trên Kafka.':
        'ASR chép “Công cụ bắt thay đổi dữ liệu đọc nhật ký thay đổi của cơ sở dữ liệu và biến mỗi dòng mới thành một sự kiện trên Capca.” (0.964): “kafka” đọc theo luật lexicon (lexicon_vi.ACB.yaml: “Cáp-ca”), ASR viết “capca” — NOT_VERIFIED bằng tai người',
    'Core Banking là hệ thống lõi giữ sổ tài khoản của ngân hàng, còn NAPAS là đơn vị chuyển mạch nối các ngân hàng Việt Nam để chuyển tiền liên ngân hàng.':
        'ASR chép “Cò Banking là hệ thống lõi giữ sổ tài khoản của ngân hàng, còn Napark là đơn vị chuyển mạch nối các ngân hàng Việt Nam để chuyển tiền liên ngân hàng.” (0.938): “core” đọc theo luật lexicon (lexicon_vi.ACB.yaml: “Co”), ASR viết “cò”; “napas” đọc theo luật lexicon (lexicon_vi.ACB.yaml: “Na-pát”), ASR viết “napark” — NOT_VERIFIED bằng tai người',
    # ── CLD dựng lại sau đọc mẫu D (2026-11-10) ──
    'Nhưng hình dạng dựng đứng gần công suất thì hệ nào cũng có, và định luật Little thì đúng cho mọi hệ ổn định, bất kể phân phối.':
        'ASR chép “Nhưng hình dạng dựng đứng gần công suất thì hệ nào cũng có, và định luật liết tồ thì đúng cho mọi hệ ổn định, bất kể phân phối.” (0.947): Little đọc thô (probe CLD p1: 5/8, ASR viết “lít tồ”) — NOT_VERIFIED bằng tai người',
    'Tổng kết lại, định luật Little đúng cho mọi hệ ổn định, tức hệ mà hàng đợi không dài mãi.':
        'ASR chép “Tổng kết lại, định luật Licto đúng cho mọi hệ ổn định, tức hệ mà hàng đợi không dài máy.” (0.9): Little đọc thô (probe CLD p1: 5/8, ASR viết “lít tồ”); lệch âm/thanh thuần Việt: mãi/máy — NOT_VERIFIED bằng tai người',
    # ── DEN dựng lại sau đọc mẫu D (2026-11-10) ──
    'Băm nghĩa là dùng một hàm biến khoá của dòng thành một con số, rồi chia số đó cho M lấy phần dư để biết dòng thuộc máy nào, nên cùng khoá thì luôn về cùng một máy.':
        'ASR chép “Băm nghĩa là dùng một hàm biến khóa của dòng thành một con số, rồi chia số đó cho em lấy phần dư để biết dòng thuộc máy nào, nên cùng khóa thi luôn về cùng một máy.” (0.947): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: thì/thi — NOT_VERIFIED bằng tai người',
    # ── DMS dựng lại sau đọc mẫu D (2026-11-10) ──
    'Đó là nhị thức Newton, và các hệ số của khai triển x cộng y mũ n chính là hàng n của tam giác Pascal.':
        'ASR chép “Đó là nhị thức Newton và các hệ số của khai truyện x cộng y mũ n chính là hàng n của tam giác Pascan.” (0.923): từ mượn/tên riêng “pascal” đọc thô (không có luật lexicon), ASR viết “pascan”; lệch âm/thanh thuần Việt: triển/truyện — NOT_VERIFIED bằng tai người',
    # ── HCI dựng lại sau đọc mẫu D (2026-11-10) ──
    'Bài 2 chỉ ra rằng thời gian trỏ T bằng a cộng b nhân lôgarit cơ số 2 của D chia W cộng 1.':
        'ASR chép “Bài 2 chỉ ra rằng thời gian trỏ T bằng A cộng B nhân logarithm cơ số 2 của dây chia về đúc cộng 1.” (0.898): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    'Trong đó D là khoảng cách từ con trỏ tới nút, W là bề rộng nút, còn a và b là hai hằng số đo riêng cho từng thiết bị.':
        'ASR chép “Trong đó dê là khoảng cách từ con trỏ tới nút, V đúc là bề rộng nút, còn A và B là hai hàng số đo riêng cho từng thiết bị.” (0.918): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác; lệch âm/thanh thuần Việt: hằng/hàng — NOT_VERIFIED bằng tai người',
    # ── JVA dựng lại sau đọc mẫu D (2026-11-10) ──
    'Lệnh bốn, C còn hai triệu một trăm nghìn, còn A nhận hai triệu ba trăm nghìn cộng hai trăm nghìn, thành hai triệu rưỡi.':
        'ASR chép “Lệnh 4, sẽ còn 2 triệu 100 nghìn, còn A nhận 2 triệu 300 nghìn cộng 200 nghìn, thành 2 triệu rưỡi.” (0.96): chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác — NOT_VERIFIED bằng tai người',
    # ── SEC dựng lại sau đọc mẫu D (2026-11-10) ──
    'Trước hết, bit là một chữ số nhị phân, 0 hoặc 1, còn một byte gồm 8 bit, chứa một số từ 0 tới 255.':
        'ASR chép “Trước hết, bit là một chữ số nhị phân, không hoặc một, còn một bay gồm 8 bit, chữ một số từ 0 tới 255.” (0.931): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: chứa/chữ — NOT_VERIFIED bằng tai người',
    'Nửa thấp của một byte là 4 bit cuối của nó, một số từ 0 tới 15, còn bỏ bit đầu là đặt bit trái nhất về 0 để số luôn dương.':
        'ASR chép “Nửa thấp của một bai là 4 bit cuối của nó, một số từ 0 tới 15, còn bỏ bit đầu là đặc bit trái nhất về không để số luân dương.” (0.909): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: đặt/đặc, luôn/luân — NOT_VERIFIED bằng tai người',
    'Băm có khoá là một hàm trộn bí mật với dữ liệu, cho ra một dãy byte dài cố định.':
        'ASR chép “Băm có khóa là một hàm trộn bí mật với dữ liệu, trò ra một dãy bay dài cố định.” (0.9): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: cho/trò — NOT_VERIFIED bằng tai người',
    # ── SWF dựng lại sau đọc mẫu D (2026-11-10) ──
    'Trong kiểu tấn công kinh điển được mô tả từ năm 1996, phần tràn ghi đè địa chỉ mà hàm sẽ quay về khi xong, nên máy nhảy tới các byte do kẻ tấn công đưa vào.':
        'ASR chép “Trong kiểu tấn công kinh điển được mô tả từ năm 1996, phần trang ghi đại địa chỉ Mà Hàm sẽ quay về khi xong, nên máy nhảy tới các bài do kẻ tấn công đưa vào.” (0.93): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: tràn/trang, đè/đại — NOT_VERIFIED bằng tai người',
    # ── INT dựng lại sau đọc mẫu D (2026-11-10) ──
    'Ta tìm hiểu cách ra lệnh cho hệ lõi T24 bằng bản tin OFS, một định dạng chữ riêng của hãng Temenos.':
        'ASR chép “Ta tìm hiểu cách tra lệnh cho hệ loại T24 bằng bản tin OFS, một định dạng chữ riêng của hãng Temenor.” (0.88): “temenos” đọc theo luật lexicon (lexicon_vi.INT.yaml: “Te-me-nót”), ASR viết “temenor”; lệch âm/thanh thuần Việt: ra/tra, lõi/loại — NOT_VERIFIED bằng tai người',
    'Ta nắm vững bản tin chuyển mạch theo đặc tả riêng của NAPAS, thường được mô tả có gốc từ chuẩn quốc tế ISO 8583.':
        'ASR chép “Ta nắm vững bản tin chuyển mặt theo đặt tả riêng của NAPAC, thường được mô tả có gốc tự chuẩn quốc tế ISO 8583.” (0.871): “napas” đọc theo luật lexicon (lexicon_vi.INT.yaml: “Na-pát”), ASR viết “napac”; lệch âm/thanh thuần Việt: mạch/mặt, đặc/đặt, từ/tự — NOT_VERIFIED bằng tai người',
    'Redis là phần mềm giữ dữ liệu trong bộ nhớ, rất nhanh, để nhiều máy chủ dùng chung một chỗ ghi khóa.':
        'ASR chép “Rê đích là phần mềm giữ giữ liệu trong bộ nhớ rất nhanh để nhiều máy chủ dùng chung một chỗ ghi khóa.” (0.957): “redis” đọc theo luật lexicon (lexicon_vi.INT.yaml: “Rê-đít”), ASR viết “đích” — NOT_VERIFIED bằng tai người',
    # ── ESY dựng lại sau đọc mẫu D (2026-11-10) ──
    'Giữa một byte, dây dữ liệu chỉ được đổi khi xung nhịp ở 0, nên bên nhận không nhầm bit dữ liệu với bắt đầu hay dừng.':
        'ASR chép “Giữa một bay, giấy giữ liệu chỉ được đổi khi xuân nhịp ở không nên bên nhận không nhằm biết giữ liệu với bắt đầu hay dừng.” (0.815): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: dây (trong “byte dây” → “bay giấy”), xung/xuân, nhầm bit/nhằm biết — NOT_VERIFIED bằng tai người',
    'Sau đó chip trả về 2 byte dữ liệu, và vi điều khiển xác nhận byte đầu.':
        'ASR chép “Sau đó chịp trả về hai bay giữ liệu và video khiển xác nhận bay đầu.” (0.727): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: chip/chịp, vi điều/video — NOT_VERIFIED bằng tai người',
    'Ở byte cuối, vi điều khiển cố ý không xác nhận để báo đã đọc đủ, rồi gửi dừng.':
        'ASR chép “Ở bay cuối, vi điều khiển cô ý không xác nhận để báo đã đọc đủ, rồi gửi dưng.” (0.842): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: cố/cô, dừng/dưng — NOT_VERIFIED bằng tai người',
    'Mỗi byte tốn 9 nhịp, kể cả nhịp xác nhận hay không xác nhận, nên 4 byte là 36 nhịp, chưa kể bắt đầu và dừng.':
        'ASR chép “Mỗi bay tốn chính nhịp, kể cả nhịp xác nhận hay không xác nhận nên 4 bay là 36 nhịp, chưa kể bắt đầu và dưng.” (0.857): byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8); lệch âm/thanh thuần Việt: chín/chính, dừng/dưng — NOT_VERIFIED bằng tai người',
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
    orig = text = p.read_text(encoding="utf-8")
    head = re.search(r"\nasr_reviewed:[ \t]*(#[^\n]*)?\n", text)  # CS115 có dòng chú thích sau khoá
    # thụt lề theo danh sách ĐÃ CÓ: tệp do yaml.dump sinh (BNK/JVA qua gen.py) để mục ở cột 0 — chèn “  - ” vào đó làm vỡ YAML
    # (lỗi thật 2026-11-09/10: JVA L00, ACB L02, BNK L00). Chuỗi viết bằng json.dumps = chuỗi nháy kép YAML hợp lệ, tự thoát “"” và “\”.
    ind = "  "
    if head:
        nxt = re.match(r"([ \t]*)- ", text[head.end():])
        if nxt:
            ind = nxt.group(1)
    q = lambda v: json.dumps(v, ensure_ascii=False)
    lines = "".join(f"{ind}- {{sentence: {q(s)}, reason: {q(r)}}}\n" for s, r in new)
    if head:
        text = text[:head.end()] + lines + text[head.end():]
    elif "\nasr_reviewed: []\n" in text:
        assert text.count("\nasr_reviewed: []\n") == 1, "khung bài phải có đúng một `asr_reviewed: []`"
        text = text.replace("\nasr_reviewed: []\n", "\nasr_reviewed:\n" + lines, 1)
    else:  # bài chưa có khoá (PAR L07–L12): thêm ngay trước `scenes:`
        assert "asr_reviewed" not in text and text.count("\nscenes:\n") == 1, "không tìm được chỗ đặt `asr_reviewed`"
        text = text.replace("\nscenes:\n", "\nasr_reviewed:\n" + lines + "scenes:\n", 1)
    # chặn ghi nếu YAML vỡ hoặc mất mục: phải đọc lại được và có đủ mục cũ + mới
    try:
        got = {str(x["sentence"]).strip() for x in (yaml.safe_load(text) or {}).get("asr_reviewed") or []}
    except yaml.YAMLError as e:
        raise SystemExit(f"DỪNG {lid}: chèn asr_reviewed làm vỡ YAML ({e}); tệp giữ nguyên") from e
    if not (done | {s for s, _ in new}) <= got:
        raise SystemExit(f"DỪNG {lid}: sau khi chèn thiếu mục asr_reviewed; tệp giữ nguyên")
    assert orig != text
    p.write_text(text, encoding="utf-8")
    print(lid, len(new), "mục →", p.relative_to(ROOT))
