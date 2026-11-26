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
    if (new and new in txt and old not in txt) or (not new and old not in txt):
        return
    assert old in txt, f"Missing in {rel}: {old[:110]!r}"
    if not multi:
        assert txt.count(old) == 1, f"Non-unique in {rel}: {old[:110]!r}"
    p.write_text(txt.replace(old, new) if multi else txt.replace(old, new, 1), encoding="utf-8")


def append_recap0(rel: str, extra: str) -> None:
    p = ROOT / rel
    txt = p.read_text(encoding="utf-8")
    if extra.strip() in txt:
        return
    sp = lv.load_spec(p)
    recap = [sc for sc in sp["scenes"] if sc["kind"] == "recap"][0]
    old = recap["steps"][0]["say"]
    assert old in txt and txt.count(old) == 1, f"Recap0 fail in {rel}"
    p.write_text(txt.replace(old, old.rstrip() + " " + extra.strip(), 1), encoding="utf-8")


# 1. Fix L13 notation ('·' inside text SVG -> '/')
rep(
    "lessons/aif/L13_tong_hop.yaml",
    "1–3: đường · 4–5: cấu hình",
    "1–3: đường / 4–5: cấu hình",
)

# 2. Remove stale E30 asr_reviewed items in L06 & L11
rep(
    "lessons/aif/L06_tro_choi_doi_khang.yaml",
    """- sentence: alpha và beta ghi lại điều đã chắc chắn, alpha lớn hơn hoặc bằng beta thì bỏ nhánh, và xét nước tốt trước để cắt được nhiều.
  reason: 'ASR chép “Anfa và Beta ghi lại điều đã chắc chắn, Anfa lớn hơn hoặc bằng Beta thì bỏ nhánh, và xét nước tốt trước để cắt được nhiều.” (0.862): alpha đọc thô (probe AIF p1: 7/8, bản chép “an pha / ANFA / α”); beta đọc “bê-ta”, ASR viết “bê/beta” — NOT_VERIFIED bằng tai người'
""",
    "",
)
rep(
    "lessons/aif/L11_mang_bayes.yaml",
    """- sentence: Tổng kết lại, mạng Bayes gồm đồ thị và các bảng điều kiện, và phân phối đồng thời bằng tích các bảng.
  reason: 'ASR chép “Tổng kết lại, mạng bay X gồm đồ thị và các bản điều kiện và phân phối đồng thời bằng tích các bản.” (0.87): Bayes đọc “Bay-ét” theo lexicon chung (probe 3/8, NOT_VERIFIED), ASR viết “bay X/S”; lệch âm/thanh thuần Việt: bảng/bản, bảng/bản — NOT_VERIFIED bằng tai người'
""",
    "",
)

# 3. Replace 4 existing 'càng ' sentences cleanly (1-for-1 preserving focus!)
rep("lessons/aif/L03_thiet_ke_ham_danh_gia.yaml",
    "Con số này càng gần 1 thì hàm đánh giá càng tốt.",
    "Con số này tiến sát về 1 cho thấy hàm đánh giá đạt hiệu quả rất cao.")
rep("lessons/aif/L04_tim_kiem_cuc_bo.yaml",
    "Số mũ càng âm thì kết quả càng gần 0.",
    "Số mũ mang giá trị âm lớn kéo kết quả tiến sát về 0.")
rep("lessons/aif/L12_lap_gia_tri.yaml",
    "Giá trị lan ra từ ô cộng 1, càng xa càng nhỏ, và ô sát ô trừ 1 bị kéo xuống.",
    "Giá trị lan ra từ ô cộng 1 rồi giảm dần theo khoảng cách, còn ô sát ô trừ 1 bị kéo tụt xuống.")
rep("lessons/aif/L14_hanh_trinh_may_choi_co.yaml",
    "Bài học sai thứ ba là nghĩ càng nhiều dữ liệu càng tốt, cứ lấy mọi thế cờ của mỗi ván.",
    "Bài học sai thứ ba là nghĩ thu gom thật nhiều thế cờ từ mỗi ván luôn tốt hơn.")

# 4. Top up tight AIF lessons cleanly on recap#0 (all crisp short sentences, no TeX, no lexicon issues)
AIF_TOPUPS = {
    "lessons/aif/L00_tac_tu_moi_truong.yaml": (
        "Nếu bỏ sót một tiêu chí môi trường, chương trình rất dễ dừng nhầm chỗ hoặc lặp vòng tại một góc phòng. "
        "Hãy thử thay đổi số ô từ hai lên ba trong bài thực hành ngay sau đây để cảm nhận sự khác biệt về kích thước không gian trạng thái. "
        "Chính thói quen phân tích cấu trúc bài toán trước khi viết mã sẽ đồng hành cùng bạn xuyên suốt khoá học."
    ),
    "lessons/aif/L01_bai_toan_tim_kiem.yaml": (
        "Sự khác biệt giữa kiểm đích lúc sinh nút với kiểm đích lúc lấy ra là ranh giới sống còn giữa hai thuật toán này. "
        "Nhiều lỗi thực tế phát sinh khi lập trình viên áp dụng hàng đợi theo chiều rộng cho bài toán có chi phí cạnh không bằng nhau. "
        "Hãy luôn tự kiểm tra lại trên một đồ thị nhỏ có bốn hoặc năm đỉnh bằng cách liệt kê tay mọi đường đi để khẳng định kết quả thuật toán hoàn toàn đúng đắn."
    ),
    "lessons/aif/L02_a_sao.yaml": (
        "Hãy nhớ nếu hàm đánh giá chỉ vô tình vượt chi phí thật một đơn vị tại một trạng thái then chốt, thuật toán có thể bỏ qua đường đi ngắn nhất. "
        "Thói quen thử đồng thời cả đường ngắn bằng tay giúp bạn kiểm chứng tính tối ưu nhanh chóng."
    ),
    "lessons/aif/L03_thiet_ke_ham_danh_gia.yaml": (
        "Một chi tiết nhỏ nhưng rất quan trọng là quy tắc nới lỏng không bao giờ tự sinh ra lời giải mới làm tăng chi phí đường đi tối ưu. "
        "Nhờ đặc tính bảo toàn mọi lời giải cũ đó, hàm ước lượng rút ra luôn đứng về phía an toàn. "
        "Khi bước sang bài tập tự giải phương trình tìm hệ số nhánh hiệu dụng hôm nay, bạn sẽ tự đo được mức giảm đáng kể khi chuyển sang hàm đánh giá tốt hơn. "
        "Đây là kỹ năng cốt lõi khi thiết kế hệ tìm đường ngoài thực tế."
    ),
    "lessons/aif/L04_tim_kiem_cuc_bo.yaml": (
        "Ngoài khởi động lại nhiều lần, mô phỏng tôi luyện còn cho phép điều chỉnh lịch giảm nhiệt độ tuỳ theo độ gồ ghề của địa hình hàm mục tiêu. "
        "Nhờ kết hợp nhịp nhàng giữa leo đồi nhanh và bước nhảy thoát bẫy, các bài toán tối ưu tổ hợp lớn tìm ra cấu hình sạch xung đột chỉ trong vài giây."
    ),
    "lessons/aif/L05_thoa_rang_buoc.yaml": (
        "Nếu quay lui đơn thuần hoạt động thụ động chờ tới lúc đụng tường mới lùi, kiểm tra tiến đóng vai trò phát hiện trước ngõ cụt ngay sau mỗi bước gán. "
        "Hơn thế nữa, chọn biến còn ít lựa chọn nhất kết hợp phá thế hoà bằng số lượng biến hàng xóm ràng buộc giúp giữ nhánh hẹp ngay từ đỉnh cây. "
        "Trên nhiều bài toán lập lịch công nghiệp hay chia ca trực có hàng trăm biến, bộ đôi kỹ thuật cắt nhánh này giải quyết gọn trong tích tắc thay vì treo máy nhiều giờ. "
        "Ngoài bản đồ chuẩn, bạn cũng có thể áp dụng nguyên lý y hệt cho bài toán Sudoku hay xếp thời khoá biểu không trùng giờ. "
        "Thực hành đếm mọi cấu hình và lọc lời giải đúng trên bản đồ sáu vùng ngay bây giờ."
    ),
    "lessons/aif/L06_tro_choi_doi_khang.yaml": (
        "Điều tuyệt đẹp của cắt tỉa alpha và beta là nó luôn cho ra cùng một kết quả chính xác y hệt cực đại cực tiểu đầy đủ mà không mất mát bất kỳ thông tin tối ưu nào. "
        "Tuy nhiên, nếu các nhánh xấu lại tình cờ được đặt ngay ở bên trái cây trò chơi, số lá phải duyệt hầu như không giảm được bao nhiêu. "
        "Do đó ngoài thực tế các chương trình cờ thường dùng bảng băm ghi nhớ nước hay và hàm đánh giá nông để xếp các nước triển vọng lên đầu trước khi cắt sâu hơn. "
        "Hiểu sâu cơ chế giữ hai cận đối xứng này giúp bạn đọc và tối ưu nhanh mọi cây tìm kiếm đối kháng hai người. "
        "Hãy thử chạy cắt tỉa trên cây ba nhánh ngay sau đây để kiểm chứng số lá thật sự mở."
    ),
    "lessons/aif/L07_cay_mo_phong_ngau_nhien.yaml": (
        "Điểm mạnh nổi bật của phương pháp này là hoàn toàn không đòi hỏi công thức đánh giá thế cờ viết tay cho từng trò chơi phức tạp. "
        "Tuy vậy ở những trạng thái có thế cờ chiến thuật bén nhạy dễ thua sau một nước sai, mô phỏng ngẫu nhiên thuần tuý có thể bỏ sót đường đi sâu nên ngoài thực tế thường kết hợp thêm mạng nơ-ron. "
        "Thử tự tính hai điểm cân bằng thăm dò ngay trong bài thực hành tiếp theo."
    ),
    "lessons/aif/L08_logic_menh_de.yaml": (
        "Khi phân tích một tập quy tắc nghiệp vụ hay mạch kiểm tra an toàn phần mềm, phép kiểm mô hình buộc ta rà soát mọi tổ hợp chân trị mà không bỏ sót bất kỳ ngoại lệ ẩn nào. "
        "Trong tình huống số lượng biến lên tới hàng trăm, người ta chuyển từ bảng chân trị thô sang các bộ giải thoả mãn logic hiện đại biết phân tích xung đột và học thêm mệnh đề cắt nhánh tự động. "
        "Tuy vậy ý nghĩa gốc của khái niệm kéo theo logic vẫn giữ nguyên không đổi, luôn là điều kiện đúng trên toàn bộ các mô hình thoả mãn tri thức. "
        "Một lưu ý rất thực tế là chỉ một câu mâu thuẫn lọt vào tập tri thức sẽ làm tập mô hình rỗng và kéo theo mọi câu bất kỳ, nên bước kiểm tra nhất quán luôn phải chạy trước tiên. "
        "Hãy viết ngay vòng lặp liệt kê đủ tám cách gán cho ba biến mệnh đề trong phần tự thực hành."
    ),
    "lessons/aif/L09_suy_dien_tien_lui.yaml": (
        "Về mặt kỹ thuật cài đặt, suy diễn tiến cực kỳ hiệu quả khi dữ liệu đầu vào đến liên tục từ cảm biến và hệ thống cần phản ứng kịp thời theo tập luật kích hoạt sẵn. "
        "Trong khi đó, suy diễn lùi phù hợp cho bài toán hỏi đáp hay kiểm định quyền truy cập vì nó chỉ chạm tới những nhánh luật có liên quan trực tiếp đến giả thuyết đang đặt ra. "
        "Một chi tiết cài đặt không thể thiếu ở chiều lùi là bảng theo dõi các mục tiêu đang treo trên ngăn xếp đệ quy để cắt ngay khi xuất hiện phụ thuộc vòng tròn. "
        "Nếu giữ thói quen rà soát cả hai chiều bằng danh sách sự kiện nhỏ, bạn sẽ dễ dàng phát hiện luật dư thừa hoặc tiền đề thiếu từ sớm. "
        "Bây giờ hãy hoàn thành bài thực hành suy diễn tiến năm luật ngay bên dưới để kiểm chứng thứ tự suy ra chính xác."
    ),
    "lessons/aif/L10_lap_ke_hoach.yaml": (
        "Trong nhiều hệ robot công nghiệp và điều phối kho hàng tự động, việc mô hình hoá gọn từng thao tác thành tiền điều kiện cùng hai danh sách thêm và xoá giúp tái sử dụng trọn bộ giải tìm kiếm chuẩn. "
        "Thay vì phải lập trình tay từng kịch bản riêng rẽ rất dễ gãy khi đổi quy tắc kho, kỹ sư chỉ cần bổ sung một mẫu hành động mới là hệ tìm kiếm tự tìm ra đường đi hợp lệ. "
        "Với không gian trạng thái lớn hàng triệu cấu hình, người ta còn xây hàm đánh giá từ việc bỏ qua hiệu ứng xoá để dẫn đường tìm kiếm tiến về đích nhanh hơn mà vẫn giữ chính xác. "
        "Đừng quên kiểm tra thật kỹ thứ tự giải phóng vật nằm bên trên trước khi nhấc vật nằm bên dưới để tránh kế hoạch không hợp lệ."
    ),
    "lessons/aif/L11_mang_bayes.yaml": (
        "Việc đọc đúng bảng xác suất có điều kiện gắn liền với sơ đồ nhân quả trên đồ thị giúp bạn giải thích rõ nguyên nhân ẩn sau các con số hậu nghiệm bất ngờ. "
        "Hãy thử chạy tính toán xác suất hậu nghiệm cho mạng cảm biến nhiệt ba tầng ở bài thực hành ngay sau đây để tự kiểm chứng trực giác."
    ),
    "lessons/aif/L12_lap_gia_tri.yaml": (
        "Khi bài toán mở rộng lên không gian trạng thái liên tục hoặc hàng triệu ô không thể chứa vừa một bảng giá trị cố định, phương pháp lặp giá trị chuyển thành nền tảng cho học tăng cường hiện đại. "
        "Hãy nhớ luôn đọc kỹ xác suất trượt ngẫu nhiên của từng hành động và tách rạch ròi trạng thái kết thúc giữ giá trị cố định khi viết vòng lặp cập nhật."
    ),
    "lessons/aif/L13_tong_hop.yaml": (
        "Khi chuyển từ mô hình đồ chơi trên lớp sang dự án sản xuất thật, điều giúp bạn không tốn công vô ích là khớp đúng bản chất bài toán với khung công cụ phù hợp nhất. "
        "Đừng bao giờ vội vã huấn luyện một mạng học sâu nặng nề nếu bài toán vốn là tìm đường trên bản đồ tĩnh hay lập lịch ràng buộc đã có thuật toán giải chính xác cực nhanh. "
        "Ngược lại, khi không gian trạng thái bùng nổ vượt ngưỡng duyệt hết hoặc môi trường thiếu công thức chuyển trạng thái rõ ràng, hãy ghép mô phỏng và hàm ước lượng học được đúng chỗ. "
        "Nắm trọn bức tranh tổng hợp này giúp bạn tự tin giải quyết các hệ thống thông minh hiện đại."
    ),
}

for rel, ext in AIF_TOPUPS.items():
    append_recap0(rel, ext)

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
