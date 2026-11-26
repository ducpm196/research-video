import glob
import re
import subprocess
import sys
from pathlib import Path
import yaml

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[1]
PY = str(ROOT / ".venv/Scripts/python.exe")
sys.path.insert(0, str(ROOT / "tools"))
import lv  # noqa: E402

# 1. Remove all remaining `'càng '` in Stage 9 show:/objectives across IRS, AGT, LLM, RLN, CVI
CANG_FIXES = {
    "lessons/irs/L00_do_chat_luong.yaml": [
        ("Vị trí càng xa thì người dùng càng mất công", "Vị trí xa hơn làm người dùng mất công hơn"),
    ],
    "lessons/irs/L01_ndcg.yaml": [
        ("vị trí càng sau, điểm càng bị giảm", "vị trí sau hơn bị giảm điểm nhiều hơn"),
    ],
    "lessons/irs/L02_tf_idf.yaml": [
        ("số càng lớn thì lôgarit càng lớn, nhưng tăng chậm", "khi số lớn hơn thì lôgarit tăng theo nhưng tăng chậm"),
        ("góc càng nhỏ, cosin càng gần 1, càng giống", "góc nhỏ hơn đưa cosin về gần 1, biểu thị mức giống cao hơn"),
    ],
    "lessons/irs/L04_hop_nhat_thu_hang.yaml": [
        ("càng ít văn bản có, từ càng đáng giá", "từ xuất hiện ở ít văn bản hơn mang trọng số cao hơn"),
        ("câu hỏi càng nhiều từ hiếm, điểm càng lớn", "câu hỏi nhiều từ hiếm hơn tạo điểm tổng lớn hơn"),
        ("hạng càng sau, phiếu càng nhỏ.", "hạng đứng sau có trọng số phiếu nhỏ hơn."),
    ],
    "lessons/irs/L05_hoc_xep_hang.yaml": [
        ("nên vị trí càng sau càng bị giảm giá.", "nên vị trí đứng sau bị giảm giá nhiều hơn."),
        ("sai càng xa: mất mát tăng gần như thẳng", "sai lệch lớn hơn: mất mát tăng gần như thẳng"),
        ("đúng càng xa:", "chênh đúng lớn hơn:"),
    ],
    "lessons/irs/L07_phan_ra_ma_tran.yaml": [
        ("Nhích càng nhỏ, con số càng gần $-4$.", "Bước nhích nhỏ hơn đưa con số tiến sát $-4$."),
        ("và sai càng xa phạt càng nặng.", "và sai lệch lớn hơn bị phạt nặng hơn gấp bội."),
    ],
    "lessons/irs/L08_phan_hoi_ngam.yaml": [
        ("(món xuất hiện càng nhiều càng dễ bị chọn)", "(món xuất hiện nhiều hơn dễ bị chọn làm mẫu âm hơn)"),
        ("càng nhỏ càng âm nhiều.", "tiến gần 0 cho giá trị âm sâu hơn."),
    ],
    "lessons/irs/L09_khoi_dong_lanh.yaml": [
        ("càng lớn càng chưa chắc", "giá trị lớn hơn biểu thị độ bất định cao hơn"),
    ],
    "lessons/irs/L10_thien_lech_vi_tri.yaml": [
        ("làm thứ phổ biến càng phổ biến.", "làm món phổ biến lại càng thêm áp đảo — gọi tắt là hiệu ứng giàu thêm giàu."),
    ],
    "lessons/irs/L11_da_dang.yaml": [
        ("Nhận ra vòng phản hồi làm sản phẩm đang dẫn càng dẫn, và sửa bằng dữ liệu khám phá",
         "Nhận ra vòng phản hồi giúp sản phẩm đang dẫn giữ thế áp đảo, và sửa bằng dữ liệu khám phá"),
        ("vì vị trí càng sâu càng ít người nhìn.", "vì vị trí xuống sâu có ít người nhìn thấy hơn."),
        ("hệ càng tin A.", "hệ thống lại dồn thêm điểm cho A."),
    ],
    "lessons/irs/L12_tinh_huong_hai_tang.yaml": [
        ("Càng nhiều mảnh, đuôi chậm càng dày.", "Số mảnh tăng thêm làm phần đuôi chậm dày lên rõ rệt."),
    ],
    "lessons/irs/L13_hanh_trinh_goi_y_video.yaml": [
        ("điểm của video trong phép tính càng cao thì nó càng bị đẩy xuống mạnh.",
         "video có điểm trong phép tính cao hơn bị lực đẩy xuống mạnh hơn."),
    ],
    "lessons/agt/L00_vong_lap_tac_tu.yaml": [
        ("càng nối dài vòng lặp tác tử càng bắt buộc có ngưỡng dừng và kiểm chứng từng bước.",
         "khi nối dài vòng lặp tác tử, ta bắt buộc đặt ngưỡng dừng và kiểm chứng từng bước."),
    ],
    "lessons/agt/L08_chi_phi_do_tre.yaml": [
        ("và lịch sử thì ngày càng dài.", "và kích thước lịch sử liên tục phình lớn."),
        ("chạy càng lâu, nó càng gần tỉ lệ với <b>bình phương</b> số bước.",
         "khi chạy nhiều bước hơn, chi phí tăng tiệm cận với <b>bình phương</b> số bước."),
    ],
    "lessons/llm/L09_can_chinh.yaml": [
        ("Xác suất càng gần 1 thì $-\\ln$ của nó càng gần 0; xác suất càng nhỏ thì $-\\ln$ càng lớn",
         "Khi xác suất tiến gần 1 thì $-\\ln$ tiến về 0; xác suất nhỏ đi làm $-\\ln$ tăng vọt"),
    ],
    "lessons/llm/L12_sinh_co_truy_xuat.yaml": [
        ("càng gần 1 càng cùng hướng, thường là càng gần nghĩa.",
         "giá trị tiến gần 1 biểu thị hai đoạn cùng hướng và thường gần nghĩa hơn."),
    ],
    "lessons/llm/L14_hanh_trinh_mo_rong.yaml": [
        ("câu càng dài càng không tận dụng được tính song song.",
         "chuỗi câu kéo dài làm giảm khả năng tận dụng xử lý song song."),
        ("mô hình càng lớn thì mỗi lần thử càng đắt.",
         "khi kích thước mô hình tăng lên thì chi phí mỗi lần thử trở nên đắt đỏ."),
        ("dữ liệu càng lớn càng dễ trùng với câu kiểm tra",
         "tập dữ liệu lớn hơn dễ xuất hiện câu trùng với tập kiểm tra"),
    ],
    "lessons/rln/L00_loi_nhuan_chiet_khau.yaml": [
        ("$\\gamma$ càng gần 1 thì tác tử nhìn càng xa,",
         "hệ số $\\gamma$ tiến gần 1 giúp tác tử nhìn về tương lai xa hơn,"),
    ],
    "lessons/rln/L02_lap_chinh_sach.yaml": [
        ("$\\gamma$ càng sát 1 nhìn càng xa nhưng", "khi $\\gamma$ tiến sát 1 tác tử nhìn xa hơn nhưng"),
        ("γ càng sát 1 nhìn càng xa nhưng", "khi γ tiến sát 1 tác tử nhìn xa hơn nhưng"),
    ],
    "lessons/rln/L03_ke_cuop_nhieu_tay.yaml": [
        ("$c$ càng lớn càng chịu thử tay chưa chắc.", "hệ số $c$ lớn hơn khuyến khích thử thêm tay chưa chắc."),
        ("Tay càng ít thử thì $Q(a)$ càng có thể lệch xa giá trị thật",
         "Tay ít được thử hơn khiến $Q(a)$ có thể lệch nhiều khỏi giá trị thật"),
        ("rồi khám phá ngày càng thưa", "rồi tần suất khám phá thưa dần theo thời gian"),
    ],
    "lessons/rln/L09_ppo.yaml": [
        ("làm phần thưởng càng xa càng được tính nhẹ.",
         "khiến phần thưởng ở tương lai xa bị giảm trọng số."),
    ],
    "lessons/rln/L10_phan_thuong_tu_nguoi.yaml": [
        ("Xác suất càng gần 1 thì $-\\ln$ càng gần 0.",
         "Khi xác suất tiến gần 1 thì $-\\ln$ tiến về 0."),
        ("Chính sách được tối ưu càng mạnh càng dễ viết những câu “lạ”",
         "Tối ưu chính sách quá mức khiến mô hình dễ sinh những câu “lạ”"),
    ],
    "lessons/rln/L11_khai_thac_phan_thuong.yaml": [
        ("→ càng phổ biến hơn", "→ mức độ phổ biến lại tiếp tục tăng vọt"),
        ("phần thưởng sai mục tiêu càng chạy lâu càng lộ lỗ hổng",
         "khi chạy đủ dài thì phần thưởng sai mục tiêu dễ lộ lỗ hổng nghiêm trọng"),
    ],
    "lessons/rln/L12_danh_gia_ngoai_tuyen.yaml": [
        ("“Nhật ký càng lớn càng đủ”", "“Nhật ký thật lớn là đủ”"),
    ],
    "lessons/rln/L13_hanh_trinh_atari.yaml": [
        ("và vì sao càng về sau, vấn đề lớn nhất lại là <b>đo cho đúng</b>.",
         "và vì sao ở những chặng sau, vấn đề lớn nhất lại là <b>đo cho đúng</b>."),
    ],
    "lessons/cvi/L02_nguong_otsu.yaml": [
        ("càng xa, hai lớp càng tách bạch", "khoảng cách lớn giúp hai lớp tách bạch rõ hơn"),
    ],
    "lessons/cvi/L03_hieu_chuan_camera.yaml": [
        ("Tiêu cự càng lớn, góc nhìn càng hẹp:", "Tiêu cự lớn hơn tạo ra góc nhìn hẹp hơn:"),
    ],
    "lessons/cvi/L06_do_sau_hai_camera.yaml": [
        ("điểm càng gần thì $d$ càng lớn.", "điểm nằm gần camera hơn tạo độ lệch $d$ lớn hơn."),
    ],
    "lessons/cvi/L12_hanh_trinh_imagenet.yaml": [
        ("và vì sao càng về sau, câu hỏi lớn nhất lại là <b>đo cho đúng</b>.",
         "và vì sao ở các chặng sau, câu hỏi lớn nhất lại là <b>đo cho đúng</b>."),
    ],
}

# Clean up any leftover `càng` in IRS L10 note cleanly -> replace `"lại càng thêm"` so `re.findall(r'\bcàng\b') == 0`!
CANG_FIXES["lessons/irs/L10_thien_lech_vi_tri.yaml"] = [
    ("làm thứ phổ biến càng phổ biến.", "làm món phổ biến thêm phần áp đảo — gọi tắt là hiệu ứng giàu thêm giàu."),
]

for rel, pairs in CANG_FIXES.items():
    p = ROOT / rel
    s = p.read_text(encoding="utf-8")
    for old, new in pairs:
        if old in s:
            s = s.replace(old, new)
    p.write_text(s, encoding="utf-8")

# Wait — also check curriculum/irs.yaml L11 objective string so curriculum matches lesson L11!
curr_irs = ROOT / "curriculum/irs.yaml"
cs = curr_irs.read_text(encoding="utf-8")
cs = cs.replace(
    "Nhận ra vòng phản hồi làm sản phẩm đang dẫn càng dẫn, và sửa bằng dữ liệu khám phá",
    "Nhận ra vòng phản hồi giúp sản phẩm đang dẫn giữ thế áp đảo, và sửa bằng dữ liệu khám phá",
)
curr_irs.write_text(cs, encoding="utf-8")

# 2. Scene upgrades (`concept` -> `example` for worked procedures, + crisp notes in mapped scenes, + covers sync)
TYPE_CONV = [
    ("lessons/cvi/L05_ransac.yaml", "- id: concept\n  kind: concept\n", "- id: concept\n  kind: example\n"),
    ("lessons/cvi/L08_phat_hien_doi_tuong.yaml", "- id: nms\n  kind: concept\n", "- id: nms\n  kind: example\n"),
    ("lessons/cvi/L11_tinh_huong_loi_tat.yaml", "- id: counterfactual\n  kind: concept\n", "- id: counterfactual\n  kind: example\n"),
]
for rel, old, new in TYPE_CONV:
    p = ROOT / rel
    s = p.read_text(encoding="utf-8")
    if old in s:
        p.write_text(s.replace(old, new), encoding="utf-8")

# 3. Enrich mapped AF2_DO_SCENES steps so each mapped `example`/`check`/`formula`/`stage5` explicitly covers the objective!
ENRICH = {
    "lessons/aif/L14_hanh_trinh_may_choi_co.yaml": (
        "stage5",
        '<p class="note"><b>Chọn đường đi cho bài của bạn:</b> nếu có hàm đánh giá viết tay tốt dùng tìm kiếm (ổn định ngay trên 1 máy); chỉ chuyển sang tự học bằng tự chơi khi trò chưa có hàm đánh giá tốt, luật rõ ràng, mô phỏng rẻ và đủ máy song song.</p>',
        " Khi chọn cho trò chơi của chính mình, dùng tìm kiếm với hàm viết tay nếu đã có tri thức tốt; chỉ chuyển sang tự chơi khi thiếu hàm viết tay tốt, luật rõ và mô phỏng rẻ.",
        2,
    ),
    "lessons/llm/L01_ngram_do_hon_loan.yaml": (
        "check",
        '<p class="note"><b>Quy tắc so sánh mô hình đúng:</b> luôn đo độ hỗn loạn trên cùng tập văn bản kiểm tra chưa từng thấy và phải dùng chung một bộ tách từ tố.</p>',
        " Nhớ quy tắc so sánh mô hình đúng, luôn đo trên cùng tập chưa từng thấy và cùng bộ tách từ tố.",
        2,
    ),
    "lessons/llm/L07_sinh_van_ban.yaml": (
        "example",
        '<p class="note"><b>Chọn cách sinh theo mục đích:</b> cần đáp án chính xác chọn nhiệt độ thấp hay tham lam; cần viết đa dạng sáng tạo chọn lấy mẫu hạt nhân.</p>',
        " Khi chọn cách sinh theo mục đích, hãy dùng nhiệt độ thấp cho câu trả lời chuẩn xác và lấy mẫu hạt nhân khi cần văn phong đa dạng.",
        2,
    ),
    "lessons/llm/L14_hanh_trinh_mo_rong.yaml": (
        "stage5",
        '<p class="note"><b>Quy tắc chia ngân sách quy mô nhỏ–vừa:</b> giữ tỉ lệ khoảng 20 từ tố cho mỗi tham số để huấn luyện tối ưu; nếu có ngưỡng suy luận chặt tại máy chủ hoặc ít dữ liệu sạch thì đổi sang mô hình nhỏ gọn được chưng cất hoặc huấn luyện dài hơn.</p>',
        " Ở quy mô của bạn, chia ngân sách gần tỉ lệ 20 từ tố mỗi tham số; nếu bị trói giới hạn suy luận hoặc thiếu dữ liệu sạch thì rút nhỏ mô hình lại.",
        2,
    ),
    "lessons/rln/L00_loi_nhuan_chiet_khau.yaml": (
        "check",
        '<p class="note"><b>Chọn $\\gamma$ và cạm bẫy cộng hằng số:</b> chọn $\\gamma$ gần 1 để tác tử chịu chờ phần thưởng lớn; trong bài toán kết thúc theo bước, cộng hằng số vào mọi phần thưởng có thể đổi hẳn quyết định thắng sớm hay kéo dài.</p>',
        " Nhớ chọn gam-ma gần 1 để chịu chờ xa, và tránh cộng hằng số vào mọi phần thưởng khi lượt chơi kết thúc được.",
        3,
    ),
    "lessons/rln/L03_ke_cuop_nhieu_tay.yaml": (
        "check",
        '<p class="note"><b>Cập nhật cộng dồn và khám phá:</b> công thức trung bình cộng dồn dùng bước $1/n$ cho môi trường tĩnh, đổi sang bước cố định $\\alpha$ khi phần thưởng trôi theo thời gian; khám phá theo độ bất định giữ tổng mất mát tăng chậm hơn nhiều so với chọn ngẫu nhiên cố định.</p>',
        " Khi phần thưởng thay đổi theo thời gian, dùng bước cố định thay cho 1 chia n; đồng thời khám phá theo độ bất định giảm mất mát dài hạn rõ rệt.",
        2,
    ),
    "lessons/rln/L04_monte_carlo_td.yaml": (
        "check",
        '<p class="note"><b>Chọn tốc độ học và phương pháp:</b> khi kết quả đến muộn hoặc lượt chơi quá dài, ưu tiên cập nhật từng bước TD với tốc độ học vừa phải thay vì chờ hết ván như Monte Carlo.</p>',
        " Với nhiệm vụ mà kết quả đến muộn, chọn cập nhật từng bước với tốc độ học vừa phải sẽ học nhanh hơn chờ hết lượt.",
        2,
    ),
    "lessons/rln/L11_khai_thac_phan_thuong.yaml": (
        "check",
        '<p class="note"><b>Thiết kế phần thưởng an toàn:</b> gắn thưởng trực tiếp với kết quả cuối cùng cần đạt, bổ sung ràng buộc chống lạm dụng và kiểm tra hành vi định tính trước khi phát hành.</p>',
        " Khi thiết kế phần thưởng, gắn thưởng vào kết quả thật, đặt thêm ràng buộc và luôn kiểm tra hành vi thực tế định tính.",
        2,
    ),
    "lessons/rln/L13_hanh_trinh_atari.yaml": (
        "stage5",
        '<p class="note"><b>Quy trình thực tế 1 GPU trong 1 tuần:</b> chạy lặp ít nhất 5 hạt giống ngẫu nhiên, vẽ đường học và báo cả độ trải dài cùng hành động dính thay vì báo điểm cao nhất của 1 lần may mắn.</p>',
        " Ở quy mô 1 GPU trong 1 tuần, giữ quy trình chạy nhiều hạt giống, báo đường học kèm hành động dính chống học vẹt.",
        2,
    ),
    "lessons/cvi/L00_anh_so.yaml": (
        "formula",
        '<p class="note"><b>Số mức màu của kênh:</b> với $b$ bit mỗi kênh, mỗi điểm biểu diễn $2^b$ mức (8 bit cho $2^8 = 256$ mức); ảnh màu sắp thành mảng 3 chiều (hàng, cột, kênh).</p>',
        " Với b bit mỗi kênh ta có 2 mũ b mức độ sáng, ví dụ 8 bit cho 256 mức, và ảnh màu là mảng ba chiều gồm hàng, cột và kênh.",
        2,
    ),
    "lessons/cvi/L03_hieu_chuan_camera.yaml": (
        "formula",
        '<p class="note"><b>Đổi sang điểm ảnh:</b> tiêu cự điểm ảnh $f_x = f_{\\text{mm}} / p_{\\text{mm}}$ (tiêu cự chia cỡ một cảm biến); từ đó tính trực tiếp góc nhìn theo $W$ và $f_x$.</p>',
        " Nhớ đổi tiêu cự mi-li-mét sang điểm ảnh bằng cách chia cho kích thước một cảm biến trên mặt phẳng máy ảnh.",
        2,
    ),
    "lessons/cvi/L05_ransac.yaml": (
        "check",
        '<p class="note"><b>Đánh đổi chi phí:</b> lọc bớt điểm khớp tốt trước làm chi phí kiểm mỗi mẫu giả định nhỏ hẳn đi so với giữ nguyên kho mẫu nhiễu và thử tràn lan.</p>',
        " So với việc thử thêm vô tội vạ, lọc cặp khớp tốt trước giúp cắt giảm đáng kể thời gian kiểm chứng từng giả thuyết.",
        2,
    ),
    "lessons/cvi/L06_do_sau_hai_camera.yaml": (
        "check",
        '<p class="note"><b>Chọn thông số cho bài đo thực tế:</b> tăng khoảng cách hai camera $B$ (chẳng hạn chọn $B \\ge 0{,}46$ m thay vì quá hẹp) kèm dải tìm chênh lệch $d$ khớp cự ly gần–xa cần đo giúp giảm sai số độ sâu.</p>',
        " Để giữ sai số nhỏ trong bài đo thực tế, cần chọn khoảng cách hai camera đủ rộng và đặt dải tìm chênh lệch khớp cự ly đo.",
        2,
    ),
    "lessons/cvi/L10_dich_chuyen_mien.yaml": (
        "check",
        '<p class="note"><b>Quy tắc lập tập kiểm tra:</b> thu đúng theo lát bối cảnh triển khai thật và luôn tách tập theo cụm vị trí đặt camera hoặc theo ngày chụp để tránh rò rỉ khung hình liền kề.</p>',
        " Luôn lập tập kiểm tra theo điều kiện triển khai thật và tách không rò rỉ theo điểm đặt máy quay hoặc theo ngày.",
        2,
    ),
}

def split_sents(text):
    if hasattr(lv, "split_sentences"):
        return lv.split_sentences(text)
    return [x.strip() for x in re.split(r"(?<=[.!?])\s+", text.strip()) if x.strip()]

for rel, (sid, note_html, note_say, f_val) in ENRICH.items():
    p = ROOT / rel
    txt = p.read_text(encoding="utf-8")
    if note_html[:40] in txt:
        continue
    d = yaml.safe_load(txt)
    sc = next(s for s in d["scenes"] if s["id"] == sid)
    last = sc["steps"][-1]
    old_show = str(last.get("show", ""))
    old_say = str(last.get("say", ""))
    lines = txt.splitlines(keepends=True)

    # Locate the last step inside scene `sid` cleanly by matching unique prefix of old_say
    key_prefix = old_say.strip()[:35]
    say_idx = None
    in_scene = False
    for idx, l in enumerate(lines):
        if l.startswith(f"- id: {sid}"):
            in_scene = True
        elif in_scene and l.startswith("- id: "):
            in_scene = False
        if in_scene and l.lstrip().startswith("say:") and key_prefix in l:
            say_idx = idx
    assert say_idx is not None, f"Could not find step say in {rel} {sid}"

    # Insert note_html right before focus: or say: inside `show:` block
    # Find start of step (`  - ` above say_idx) and end of show (`focus:` or `introduces:` or `say:`)
    show_end = None
    for j in range(say_idx - 1, -1, -1):
        ls = lines[j].lstrip()
        if ls.startswith(("focus:", "introduces:", "notation_note:", "forward_ref:", "pause:", "clear:")):
            show_end = j
        elif ls.startswith("show:"):
            if show_end is None:
                show_end = say_idx
            break
    assert show_end is not None, f"show_end not found in {rel} {sid}"
    # If show was single-line (unlikely here, all read steps were multiline `show: |`), verify
    indent_html = " " * (len(lines[show_end - 1]) - len(lines[show_end - 1].lstrip()))
    lines[show_end - 1] = lines[show_end - 1].rstrip("\n") + "\n" + indent_html + note_html + "\n"

    # Append note_say onto lines[say_idx]
    lines[say_idx] = lines[say_idx].rstrip("\n") + note_say + "\n"

    # Update `focus:` count if present on that step
    n_add = len(split_sents(note_say.strip()))
    # determine block index of newly appended note_html
    new_show = old_show.rstrip() + "\n" + note_html
    # Count top-level blocks via simple parse or lv
    if hasattr(lv, "split_blocks"):
        blk_idx = len(lv.split_blocks(new_show))
    else:
        blk_idx = 2
    for j in range(say_idx - 1, max(-1, say_idx - 25), -1):
        if lines[j].lstrip().startswith("focus:"):
            end = j + 1
            while end < say_idx and lines[end].lstrip().startswith("- "):
                end += 1
            indent_f = " " * (len(lines[end - 1]) - len(lines[end - 1].lstrip()))
            add_f = [f"{indent_f}- {blk_idx}\n"] * n_add
            lines = lines[:end] + add_f + lines[end:]
            break

    p.write_text("".join(lines), encoding="utf-8")

# 4. Fix CVI L00 example to explicitly show 3D (hàng, cột, kênh) indexing + write accurate COVERS in up_s9_llm_rl_cv.py & up_s9_data_ai.py & YAMLs!
NEW_COVERS = {
    ("AIF", "L13"): [(1, "example"), (2, "example"), (3, "pitfalls")],
    ("AIF", "L14"): [(1, "stage1"), (1, "stage2"), (1, "stage3"), (1, "stage4"), (1, "stage5"), (2, "check"), (3, "stage5"), (3, "practice")],
    ("LLM", "L01"): [(1, "example"), (2, "example"), (3, "check"), (3, "practice")],
    ("LLM", "L07"): [(1, "example"), (2, "example"), (3, "example"), (3, "practice")],
    ("LLM", "L14"): [(1, "stage1"), (1, "stage2"), (1, "stage3"), (1, "stage4"), (1, "stage5"), (2, "stage1"), (2, "stage3"), (2, "stage4"), (2, "check"), (3, "stage5"), (3, "practice")],
    ("RLN", "L00"): [(1, "sym"), (1, "intuition"), (2, "example"), (3, "formula"), (4, "check")],
    ("RLN", "L03"): [(1, "formula"), (2, "formula"), (2, "example"), (2, "check"), (3, "example"), (4, "check")],
    ("RLN", "L04"): [(1, "intuition"), (1, "formula"), (2, "example"), (3, "example"), (4, "check")],
    ("RLN", "L06"): [(1, "formula"), (1, "example"), (2, "check"), (3, "formula"), (4, "pitfalls")],
    ("RLN", "L11"): [(1, "example"), (2, "check"), (3, "concept"), (4, "check"), (4, "practice")],
    ("RLN", "L13"): [(1, "stage1"), (1, "stage2"), (1, "stage3"), (1, "stage4"), (1, "stage5"), (2, "check"), (3, "stage4"), (3, "stage5"), (3, "practice")],
    ("CVI", "L00"): [(1, "formula"), (2, "formula"), (3, "example"), (3, "check"), (4, "pitfalls")],
    ("CVI", "L03"): [(1, "formula"), (2, "formula"), (3, "example"), (4, "check")],
    ("CVI", "L05"): [(1, "intuition"), (2, "concept"), (3, "formula"), (4, "check"), (4, "practice")],
    ("CVI", "L06"): [(1, "row"), (2, "example"), (3, "formula"), (4, "check")],
    ("CVI", "L08"): [(1, "formula"), (2, "nms"), (3, "example"), (4, "threshold")],
    ("CVI", "L10"): [(1, "intuition"), (2, "formula"), (3, "example"), (4, "check"), (4, "practice")],
    ("CVI", "L11"): [(1, "example"), (2, "counterfactual"), (3, "pitfalls"), (4, "counterfactual")],
}

for (c, lid), cov in NEW_COVERS.items():
    p = sorted((ROOT / f"lessons/{c.lower()}").glob(f"{lid}_*.yaml"))[0]
    txt = p.read_text(encoding="utf-8")
    # Replace YAML `covers:` block at EOF cleanly
    cov_lines = ["covers:\n"] + [f"- objective: {o}\n  scene: {s}\n" for o, s in cov]
    idx = txt.find("\ncovers:\n")
    assert idx != -1, f"covers: not found in {p}"
    p.write_text(txt[:idx + 1] + "".join(cov_lines), encoding="utf-8")

# Sync up_s9_data_ai.py COVERS & AIF L09 table hint
dai = ROOT / "audit/s9_11/up_s9_data_ai.py"
ds = dai.read_text(encoding="utf-8")
ds = ds.replace('"L13": [(1, \'example\'), (2, \'sym\'), (3, \'pitfalls\')],',
                '"L13": [(1, \'example\'), (2, \'example\'), (3, \'pitfalls\')],')
ds = ds.replace('derived=<chuỗi cách nhau bằng dấu phẩy>`', 'derived=...`')
dai.write_text(ds, encoding="utf-8")

# Sync up_s9_llm_rl_cv.py COVERS
lrc = ROOT / "audit/s9_11/up_s9_llm_rl_cv.py"
ls = lrc.read_text(encoding="utf-8")
for (c, lid), cov in NEW_COVERS.items():
    if c == "AIF":
        continue
    pat = re.compile(rf'\("{c}", "{lid}"\):\s*\[[^\]]*\]', re.DOTALL)
    rep = f'("{c}", "{lid}"): {[(o, s) for o, s in cov]}'
    ls, n = pat.subn(rep, ls)
    assert n == 1, f"Failed to update {c} {lid} in up_s9_llm_rl_cv.py (n={n})"
lrc.write_text(ls, encoding="utf-8")

# 5. Remove stale IRS L02 patch from finish_stage9_all.py so nobody can re-duplicate it!
fs9 = ROOT / "scratch/finish_stage9_all.py"
fss = fs9.read_text(encoding="utf-8")
fss = re.sub(r'\s*"lessons/irs/L02_tf_idf\.yaml": \[[^\]]*\],', "", fss, flags=re.DOTALL)
fs9.write_text(fss, encoding="utf-8")

# 6. Verify ALL 106 Stage 9 lessons: word count >= 1650, 0 'càng ' in show/say/objectives, 0 lint E/W!
bad = []
for c in ("cs115", "aif", "irs", "agt", "llm", "rln", "cvi"):
    for p in sorted((ROOT / f"lessons/{c}").glob("L*.yaml")):
        if c == "cs115":
            m = re.search(r"L(\d+)_", p.name)
            if not m or int(m.group(1)) < 22:
                continue
        txt = p.read_text(encoding="utf-8")
        d = yaml.safe_load(txt)
        w = sum(len(str(st.get("say") or "").split()) for sc in d["scenes"] for st in sc["steps"])
        cang = sum(
            len(re.findall(r"\bcàng\b", str(st.get(k) or ""), re.I))
            for sc in d["scenes"] for st in sc["steps"] for k in ("show", "say")
        ) + sum(len(re.findall(r"\bcàng\b", str(o), re.I)) for o in d.get("objectives", []))
        res = lv.lint(d, quiet=True)
        if w < 1650 or cang > 0 or res.errors or res.warnings:
            print(f"FAIL {c.upper()} {d['id']}: w={w} cang={cang} E={res.errors} W={res.warnings}", flush=True)
            bad.append((c.upper(), d["id"], w, cang, res.errors, res.warnings))
print(f"CHECKED STAGE 9 TOTAL FAILURES: {len(bad)}", flush=True)
assert not bad, f"Stage 9 issues remain: {bad}"

# 7. Run all Stage 9 non-browser gates (`sync_tpl`, `screen_code`, `lab_gate`, `curriculum`, `verify_*`, `arith_scan`)!
for c in ("CS115", "AIF", "IRS", "AGT", "LLM", "RLN", "CVI"):
    cmds = [
        [PY, "-B", "audit/review/sync_tpl_from_lesson.py", c, "--write"],
        [PY, "-B", "audit/review/screen_code.py", "check", "--course", c],
        [PY, "-B", "audit/review/lab_gate.py", c],
        [PY, "-B", "tools/lv.py", "curriculum", f"curriculum/{c.lower()}.yaml"],
        [PY, "-B", "audit/review/arith_scan.py", c],
    ]
    if c == "CS115":
        cmds.append([PY, "-B", "audit/verify_cs115_tex.py"])
    else:
        cmds.append([PY, "-B", f"audit/{c.lower()}/verify_{c.lower()}.py"])
    for cmd in cmds:
        print(">>> RUN:", " ".join(cmd[:4]), flush=True)
        r = subprocess.run(cmd, cwd=ROOT)
        assert r.returncode == 0, f"failed: {cmd}"

print("STAGE 9 ALL 106 LESSONS V4 FIXES + ALL NON-BROWSER GATES 100% PASS!", flush=True)
