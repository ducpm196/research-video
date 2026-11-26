from contextlib import redirect_stdout
import io
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(r"D:\research-video")
sys.path.insert(0, str(ROOT / "tools"))
import lv  # noqa: E402


def rep(rel: str, old: str, new: str, multi: bool = False) -> None:
    p = ROOT / rel
    txt = p.read_text(encoding="utf-8")
    if new in txt and old not in txt:
        return
    assert old in txt, f"Missing in {rel}: {old[:110]!r}"
    if not multi:
        assert txt.count(old) == 1, f"Non-unique in {rel}: {old[:110]!r}"
    p.write_text(txt.replace(old, new) if multi else txt.replace(old, new, 1), encoding="utf-8")


def append_hook(rel: str, extra: str) -> None:
    p = ROOT / rel
    txt = p.read_text(encoding="utf-8")
    if extra.strip() in txt:
        return
    sp = lv.load_spec(p)
    hk = sp["scenes"][0]["steps"][0]
    old_say = hk["say"]
    assert old_say in txt and txt.count(old_say) == 1, f"Hook say match fail in {rel}"
    n_add = len(lv.sentences(extra))
    foc = hk.get("focus")
    if foc is not None:
        # Insert extra focus items right before `say:` inside the hook step block
        last_val = foc[-1]
        old_tail = "\n    say: " + old_say
        if old_tail not in txt:
            # Find focus lines before say
            idx = txt.find(old_say)
            assert idx > 0
            seg = txt[:idx]
            add_lines = "".join(f"    - {repr(last_val)}\n" if isinstance(last_val, str) else f"    - {last_val}\n" for _ in range(n_add))
            pos = seg.rfind("    say:")
            txt = txt[:pos] + add_lines + txt[pos:]
        else:
            add_lines = "".join(f"\n    - {repr(last_val)}" if isinstance(last_val, str) else f"\n    - {last_val}" for _ in range(n_add))
            txt = txt.replace(old_tail, add_lines + old_tail, 1)
    txt = txt.replace(old_say, old_say.rstrip() + " " + extra.strip(), 1)
    p.write_text(txt, encoding="utf-8")


def replace_recap0(rel: str, new_say: str) -> None:
    p = ROOT / rel
    txt = p.read_text(encoding="utf-8")
    if new_say in txt:
        return
    sp = lv.load_spec(p)
    recap = [sc for sc in sp["scenes"] if sc["kind"] == "recap"][0]
    old_say = recap["steps"][0]["say"]
    assert old_say in txt and txt.count(old_say) == 1, f"Recap0 say match fail in {rel}"
    p.write_text(txt.replace(old_say, new_say, 1), encoding="utf-8")


# 1. Fix 3 AIF SVGs (L04, L08, L13)
rep(
    "lessons/aif/L04_tim_kiem_cuc_bo.yaml",
    """      <circle cx="330" cy="250" r="16" fill="#eb6834"/><circle cx="690" cy="140" r="16" fill="#eb6834"/><circle cx="1080" cy="312" r="16" fill="#059669"/>

      <g font-size="25" text-anchor="middle" fill="#1f2937">

      <text x="330" y="205">cực tiểu địa phương: h = 1</text>

      <text x="690" y="105">cao nguyên: mọi láng giềng bằng nhau</text>

      <text x="1080" y="270">lời giải: h = 0</text>

      <text x="160" y="50">xuất phát: h = 17</text></g>""",
    """      <circle cx="330" cy="250" r="16" fill="#eb6834"/><circle cx="690" cy="140" r="16" fill="#eb6834"/><circle cx="1080" cy="312" r="16" fill="#059669"/>

      <g font-size="23" text-anchor="middle" fill="#1f2937">

      <text x="295" y="198">cực tiểu địa phương</text>

      <text x="295" y="224">h = 1</text>

      <text x="720" y="102">cao nguyên: mọi láng giềng bằng nhau</text>

      <text x="1080" y="268">lời giải: h = 0</text>

      <text x="160" y="48">xuất phát: h = 17</text></g>""",
)
rep("lessons/aif/L08_logic_menh_de.yaml", '<svg width="1500" height="340" viewBox="0 0 1500 340">', '<svg width="1500" height="370" viewBox="0 0 1500 370">')
rep(
    "lessons/aif/L13_tong_hop.yaml",
    """      <rect x="1070" y="235" width="320" height="80" rx="10" fill="#d1fae5" stroke="#059669" stroke-width="2"/><text x="1230" y="270">đường → 1–3, cấu hình → 4–5</text><text x="1230" y="302" font-size="21">A*; leo đồi, ràng buộc</text></g>
      <g font-size="22" fill="#6b7280"><text x="420" y="65">chắc</text><text x="920" y="65">không</text></g>""",
    """      <rect x="1050" y="235" width="360" height="80" rx="10" fill="#d1fae5" stroke="#059669" stroke-width="2"/><text x="1230" y="270" font-size="22">1–3: đường · 4–5: cấu hình</text><text x="1230" y="302" font-size="22">A*; leo đồi, ràng buộc</text></g>
      <g font-size="22" text-anchor="middle" fill="#4b5563"><text x="475" y="65">chắc</text><text x="975" y="65">không</text></g>""",
)

# 2. Polish Unicode exponents in AIF Hai mức quy mô
rep("lessons/aif/L02_a_sao.yaml", "15-puzzle (~10^13 trạng thái)", "bài toán 15 ô (~10¹³ trạng thái)", multi=True)
rep("lessons/aif/L04_tim_kiem_cuc_bo.yaml", "hơn 10^40000 trạng thái", "hơn 10⁴⁰⁰⁰⁰ trạng thái", multi=True)
rep("lessons/aif/L12_lap_gia_tri.yaml", "O(|S|^2|A|)", "O(|S|²|A|)", multi=True)

# 3. Clean hook + recap0 boosts across AIF L00..L13 (each sentence <= 160 chars, <= 34 words, 0 'càng ', 0 TeX)
HOOK_EXTRAS = {
    "lessons/aif/L00_tac_tu_moi_truong.yaml": "Nếu phòng mở rộng thành ba ô hoặc có chướng ngại che tầm nhìn, chỉ hai luật phản xạ thô sẽ lặp vô tận hoặc bỏ sót bụi. Hiểu đúng môi trường là bước đầu chọn đúng kiến trúc tác tử.",
    "lessons/aif/L01_bai_toan_tim_kiem.yaml": "Khi các cạnh bản đồ mang trọng số khác nhau, đường ít bước nhất không chắc là đường tốn ít chi phí nhất. Phân biệt hai tiêu chuẩn này giúp bạn chọn đúng cấu trúc hàng đợi ngay từ đầu.",
    "lessons/aif/L03_thiet_ke_ham_danh_gia.yaml": "Cũng giống như nới lỏng bản đồ đường bộ thành đường chim bay, hàm ước lượng từ bài toán dễ hơn luôn là cận dưới an toàn. Thước đo hệ số nhánh hiệu dụng cho phép ta kiểm chứng mức cắt giảm không gian bằng con số cụ thể.",
    "lessons/aif/L05_thoa_rang_buoc.yaml": "Mấu chốt nằm ở việc xoá ngay các giá trị xung đột ở hàng xóm ngay khi vừa gán xong một biến. Phối hợp thêm thứ tự ưu tiên biến bó hẹp nhất giúp giải nhanh hàng loạt bài toán xếp lịch phức tạp. Hôm nay bạn sẽ thấy bài toán bản đồ giảm từ hàng chục bước thử sai về đúng một mạch thẳng tắp.",
    "lessons/aif/L06_tro_choi_doi_khang.yaml": "Kỹ thuật cắt tỉa không hề làm đổi đáp án tối ưu ở gốc mà chỉ bỏ qua các nhánh vô vọng. Với thứ tự xét nước tốt từ sớm, độ sâu nhìn trước của máy tăng gấp đôi trên cùng ngân sách thời gian. Ta cũng làm rõ điều kiện cắt nhánh chuẩn xác để bạn không bao giờ cắt nhầm nước đi hay.",
    "lessons/aif/L07_cay_mo_phong_ngau_nhien.yaml": "Cơ chế bốn bước chọn, mở rộng, mô phỏng và cập nhật ngược giúp thuật toán tập trung ngân sách đúng vào nhánh triển vọng. Khi hết thời gian tìm kiếm, lựa chọn đi thật dựa trên số lượt ghé thăm thay vì tỉ lệ thắng thô.",
    "lessons/aif/L08_logic_menh_de.yaml": "Ta phân biệt rành mạch giữa bảng gán đúng sai và hệ quả logic trên mọi mô hình thoả mãn tri thức ban đầu. Nắm chắc ngữ nghĩa tập hợp giúp bạn tránh sạch lỗi ngụy biện khẳng định hệ quả hay nhầm chiều kéo theo.",
    "lessons/aif/L09_suy_dien_tien_lui.yaml": "Nhờ giới hạn câu luật về đúng một vế kết luận dương, thời gian suy diễn rút từ hàm mũ xuống tuyến tính theo số luật. Hiểu hai hướng suy diễn còn giúp bạn biết lúc nào hệ chuyên gia nên dẫn từ dữ liệu và lúc nào nên truy ngược mục tiêu.",
    "lessons/aif/L10_lap_ke_hoach.yaml": "Thú vị hơn nữa, giải riêng từng mục tiêu nhỏ rồi ghép lại có thể hỏng dây chuyền vì hành động sau phá mất điều kiện vừa tạo. Ta cần đồ thị trạng thái chuẩn xác cho toàn tổ hợp mục tiêu để tránh bẫy tương tác này.",
    "lessons/aif/L13_tong_hop.yaml": "Khi đặt đúng ba câu hỏi phân loại về tính tất định, đối thủ và đường đi hay cấu hình, bản đồ thuật toán hiện ra rất rành mạch. Quan trọng nhất là thấy cách tìm kiếm cổ điển kết nối tự nhiên với hàm ước lượng học được trong trí tuệ nhân tạo hiện đại.",
}

RECAP0_NEW = {
    "lessons/aif/L00_tac_tu_moi_truong.yaml": (
        "Tổng kết lại, tác tử biến tri giác thu từ cảm biến thành hành động qua cơ cấu chấp hành. Ta luôn mô tả bài toán bằng bốn thành phần gồm hiệu năng, môi trường, chấp hành và cảm biến. "
        "Khung phân loại năm chiều giúp nhận diện ngay mức phức tạp của thế giới xung quanh. "
        "Chỉ trong môi trường quan sát đủ, tác tử phản xạ đơn giản mới an toàn. Khi phòng nhiều ô che khuất tầm nhìn, tác tử bắt buộc giữ trạng thái bên trong. "
        "Nắm chắc khung mô hình hoá này là nền tảng vững vàng cho toàn bộ các thuật toán tìm kiếm và lập kế hoạch tiếp theo."
    ),
    "lessons/aif/L01_bai_toan_tim_kiem.yaml": (
        "Tổng kết lại, bài toán tìm kiếm chuẩn hoá vấn đề thành trạng thái đầu, tập hành động, mô hình chuyển, kiểm tra đích và chi phí. "
        "Tìm theo chiều rộng mở theo tầng từ nông tới sâu nên cho đường ít bước nhất, rất hợp khi chi phí đều và kiểm đích ngay lúc sinh nút con. "
        "Ngược lại khi chi phí các cạnh khác nhau, tìm theo chi phí đều dùng hàng đợi ưu tiên và chỉ kiểm đích khi lấy ra mới bảo đảm đường rẻ nhất. "
        "Đừng quên ghi sổ tập đã thăm và xử lý cập nhật chi phí tốt hơn để tránh lặp vô tận. Thực hành ngay trên đồ thị nhỏ giúp bạn khắc sâu thứ tự mở nút."
    ),
    "lessons/aif/L02_a_sao.yaml": (
        "Tổng kết lại, thuật toán A sao cộng chi phí đã đi với ước lượng chi phí còn lại để hướng tìm kiếm về thẳng mục tiêu. "
        "Nếu hàm đánh giá chấp nhận được tức không bao giờ vượt chi phí thật, A sao luôn trả về đường tối ưu khi kiểm đích lúc lấy ra. "
        "Hàm đánh giá gần sát chi phí thực tế mà không vượt ngưỡng sẽ thu gọn mạnh số nút phải mở cả về thời gian lẫn bộ nhớ. "
        "Đừng kết thúc sớm ngay khi vừa chạm đích lần đầu nếu còn nhánh rẻ hơn trong hàng đợi. Bài thực hành trên bảng tám ô số tiếp theo kiểm định trực tiếp quy tắc này."
    ),
    "lessons/aif/L03_thiet_ke_ham_danh_gia.yaml": (
        "Tổng kết lại, bỏ bớt ràng buộc chuyển bước cho ta một bài toán nới lỏng dễ giải hơn. "
        "Vì mọi lời giải gốc đều hợp lệ trong bài nới lỏng, chi phí tối ưu của nó tự động là hàm đánh giá chấp nhận được. "
        "Khi so hai hàm đánh giá, quan hệ trội bắt buộc phải đúng trên mọi trạng thái chứ không chỉ đúng theo trung bình. "
        "Nếu không hàm nào trội hẳn hàm kia, lấy giá trị lớn nhất từng điểm vẫn giữ tính chấp nhận được và trội hơn cả hai. "
        "Cuối cùng hãy dùng phương trình đa thức tính hệ số nhánh hiệu dụng để đo sức cắt tỉa bằng con số rõ ràng."
    ),
    "lessons/aif/L04_tim_kiem_cuc_bo.yaml": (
        "Tổng kết lại, khi chỉ cần cấu hình cuối tốt mà không cần đường đi, tìm kiếm cục bộ chỉ giữ đúng một trạng thái hiện tại. "
        "Nhờ bộ nhớ nhỏ, nó xử lý gọn bài toán hàng vạn biến nhưng dễ kẹt ở cực tiểu địa phương hoặc cao nguyên bằng phẳng. "
        "Hai chiến lược thoát kẹt chính là khởi động lại ngẫu nhiên với số lần chạy kỳ vọng bằng một chia p, và mô phỏng tôi luyện giảm dần nhiệt độ. "
        "Hãy kiểm tra kỹ để bảo đảm vòng duyệt luôn xét hết toàn bộ lân cận trước khi chọn bước tốt nhất."
    ),
    "lessons/aif/L05_thoa_rang_buoc.yaml": (
        "Tổng kết lại, bài toán thoả ràng buộc quy bài toán thực tế về ba thành phần gồm biến, miền giá trị và tập ràng buộc. "
        "Thay vì gán mù toàn bộ biến gây bùng nổ tổ hợp, ta gán từng biến và quay lui ngay tại chỗ khi có vi phạm. "
        "Kiểm tra tiến giúp xoá sớm giá trị xung đột ở các biến hàng xóm để phát hiện miền rỗng và lùi tức thì. "
        "Kết hợp ưu tiên biến còn ít giá trị nhất ép cây tìm kiếm gãy nhánh, giảm đáng kể số lần thử sai. "
        "Hãy nhớ lập đủ danh sách cạnh ràng buộc khi áp dụng vào bài thực hành tô màu sáu vùng hôm nay."
    ),
    "lessons/aif/L06_tro_choi_doi_khang.yaml": (
        "Tổng kết lại, trong trò chơi hai người, bên cực đại chọn nước lớn nhất còn đối thủ cực tiểu chọn nước nhỏ nhất. "
        "Cận alpha ghi điểm tối thiểu chắc chắn của bên cực đại, cận beta ghi điểm tối đa chắc chắn của bên cực tiểu. "
        "Khi alpha lớn hơn hoặc bằng beta, ta cắt bỏ phần nhánh còn lại mà không làm đổi kết quả tối ưu ở gốc. "
        "Xét nước đi mạnh ngay từ đầu quyết định mức cắt tỉa, giúp tìm sâu hơn gấp nhiều lần trên cùng ngân sách. "
        "Thực hành đếm số lá duyệt qua cây ba nhánh sau đây giúp bạn thấy rõ số phép tính tiết kiệm được."
    ),
    "lessons/aif/L07_cay_mo_phong_ngau_nhien.yaml": (
        "Tổng kết lại, tìm kiếm cây mô phỏng ngẫu nhiên đánh giá thế cờ bằng hàng loạt ván chơi thử tới kết thúc thay cho hàm đánh giá tay. "
        "Mỗi vòng gồm bốn bước gồm chọn nhánh trong cây, mở rộng nút mới, mô phỏng tới hết ván và cập nhật ngược lên gốc. "
        "Công thức cận trên tin cậy kết hợp tỉ lệ thắng hiện tại với phần thưởng khám phá để thử lại những nước ít lượt. "
        "Khi hết ngân sách thời gian, nhớ chốt nước đi thật theo số lượt ghé thăm cao nhất chứ không theo tỉ lệ thắng thô."
    ),
    "lessons/aif/L08_logic_menh_de.yaml": (
        "Tổng kết lại, logic mệnh đề biểu diễn tri thức bằng biến chân trị đúng sai và câu ràng buộc chặt chẽ. "
        "Một câu được tri thức kéo theo logic khi và chỉ khi nó đúng ở mọi mô hình thoả mãn toàn bộ tập tri thức. "
        "Phương pháp liệt kê mọi bảng chân trị đầy đủ và chính xác cho ít biến nhưng bùng nổ lũy thừa hai khi số biến lớn. "
        "Nhớ phân biệt rành mạch giữa kéo theo một chiều với tương đương hai chiều để tránh lỗi ngụy biện khẳng định hệ quả."
    ),
    "lessons/aif/L09_suy_dien_tien_lui.yaml": (
        "Tổng kết lại, với các luật chỉ có một kết luận dương, ta thoát bùng nổ bảng chân trị bằng suy diễn theo luật tuyến tính. "
        "Suy diễn tiến xuất phát từ các sự kiện ban đầu, giảm bộ đếm tiền đề và suy ra mọi kết luận mới theo chiều thuận. "
        "Suy diễn lùi đi ngược từ một mục tiêu cho trước, kiểm đệ quy từng điều kiện và giữ sổ chặn vòng tránh lặp vô tận. "
        "Ngoài dạng luật xác định này, các hệ logic tổng quát hơn đòi hỏi kỹ thuật hợp giải mạnh hơn. "
        "Bài thực hành chạy bộ luật tiến ngay sau đây giúp bạn kiểm chứng thứ tự kích hoạt luật chính xác."
    ),
    "lessons/aif/L10_lap_ke_hoach.yaml": (
        "Tổng kết lại, lập kế hoạch mô tả trạng thái bằng tập sự kiện và hành động bằng tiền điều kiện, hiệu ứng thêm và xoá. "
        "Tìm kiếm theo chiều rộng hoặc có chỉ dẫn trên không gian trạng thái giúp tìm ra kế hoạch ngắn nhất tới mục tiêu. "
        "Vì các mục tiêu con thường xung đột chéo và làm hỏng điều kiện của nhau, ta bắt buộc giải đồng thời trên toàn tổ hợp trạng thái. "
        "Cài đặt bộ giải cho bài toán đảo chồng ba khối ngay sau đây minh hoạ rõ cách biểu diễn và cập nhật tập sự kiện."
    ),
    "lessons/aif/L11_mang_bayes.yaml": (
        "Tổng kết lại, mạng Bayes kết hợp đồ thị có hướng không chu trình với bảng xác suất có điều kiện tại từng nút. "
        "Phân phối đồng thời của toàn hệ bằng đúng tích xác suất có điều kiện từng nút theo cha trực tiếp của nó. "
        "Để suy diễn hậu nghiệm khi quan sát bằng chứng, ta cộng dồn qua các biến ẩn chưa biết rồi chuẩn hoá tổng xác suất về một. "
        "Chú ý hiện tượng giải thích loại trừ làm giảm xác suất một nguyên nhân khi nguyên nhân cạnh tranh khác đã lộ rõ."
    ),
    "lessons/aif/L12_lap_gia_tri.yaml": (
        "Tổng kết lại, khi kết quả hành động mang tính ngẫu nhiên, ta mô hình bài toán bằng quá trình quyết định Markov có thưởng và chiết khấu. "
        "Giá trị tối ưu tại mỗi trạng thái thoả phương trình tự nhất quán gắn với hành động tốt nhất. "
        "Lặp giá trị cập nhật bảng nhiều vòng cho tới khi thay đổi đủ nhỏ rồi đọc ra chính sách hành động tối ưu. "
        "Chỉ cần đổi nhẹ mức thưởng từng bước hay chiết khấu, đường đi tối ưu có thể chuyển từ lối tắt rủi ro sang vòng an toàn."
    ),
    "lessons/aif/L13_tong_hop.yaml": (
        "Tổng kết lại, bản đồ công cụ giúp bạn chọn phương pháp đúng ngay từ đầu dựa trên tính tất định, đối thủ và dạng lời giải. "
        "Với bài toán có mô hình rõ và cỡ vừa, hãy dùng thuật toán tìm kiếm, ràng buộc, logic hoặc lặp giá trị có bảo đảm toán học. "
        "Khi cây trạng thái bùng nổ quá ngưỡng hay thiếu mô hình chuyển bước, kết hợp cắt độ sâu, mô phỏng ngẫu nhiên và hàm đánh giá học được. "
        "Sự bổ trợ giữa suy luận cổ điển và học máy tạo nên các hệ trí tuệ nhân tạo mạnh nhất hiện nay."
    ),
}

for rel, ext in HOOK_EXTRAS.items():
    append_hook(rel, ext)
for rel, nsay in RECAP0_NEW.items():
    replace_recap0(rel, nsay)

# Validate AIF L00..L14 cleanly (collect all before failing)
bad = []
for i in range(15):
    lid = f"L{i:02d}"
    fp = sorted((ROOT / "lessons" / "aif").glob(f"{lid}_*.yaml"))[0]
    sp = lv.load_spec(fp)
    w = sum(len((st.get("say") or "").split()) for sc in sp["scenes"] for st in sc["steps"])
    with redirect_stdout(io.StringIO()):
        res = lv.lint(sp, quiet=True)
    if res.errors or res.warnings:
        bad.append(f"{lid} E={res.errors} W={res.warnings}")
    if w < 1645:
        bad.append(f"{lid} w={w} (need +{1655-w})")
    for sc in sp["scenes"]:
        for idx, st in enumerate(sc["steps"]):
            say = st.get("say") or ""
            foc = st.get("focus")
            sents = lv.sentences(say)
            if foc is not None and len(foc) != len(sents):
                bad.append(f"{lid}:{sc['id']}#{idx} focus={len(foc)} != sents={len(sents)}")
            for s in sents:
                if len(s) > 170: bad.append(f"{lid}:{sc['id']}#{idx} >170 ({len(s)}): {s}")
                if len(s.split()) > 38: bad.append(f"{lid}:{sc['id']}#{idx} >38w ({len(s.split())}): {s}")
                if "càng " in s.lower(): bad.append(f"{lid}:{sc['id']}#{idx} 'càng ': {s}")
                if re.search(r"[$_^]", s): bad.append(f"{lid}:{sc['id']}#{idx} TeX: {s}")
    print(f"AIF:{lid}: w={w} E={len(res.errors)} W={len(res.warnings)}", flush=True)
for b in bad:
    print("BAD:", b, flush=True)
assert not bad, f"{len(bad)} AIF issues"

PY = str(ROOT / ".venv" / "Scripts" / "python.exe")
for cmd in (
    [PY, "-B", "-u", "audit/s9_11/up_s9_data_ai.py", "AIF"],
    [PY, "-B", "-u", "tools/lv.py", "curriculum", "curriculum/aif.yaml"],
    [PY, "-B", "-u", "audit/aif/verify_aif.py"],
):
    print(">>> RUN:", " ".join(cmd), flush=True)
    r = subprocess.run(cmd, cwd=ROOT)
    assert r.returncode == 0, f"FAILED: {cmd}"
print("AIF STAGE 9 UPGRADE & VERIFY PASSED!", flush=True)
