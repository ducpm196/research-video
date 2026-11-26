from contextlib import redirect_stdout
import io
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(r"D:\research-video")
sys.path.insert(0, str(ROOT / "tools"))
import lv  # noqa: E402


def rep(rel: str, old: str, new: str) -> None:
    p = ROOT / rel
    txt = p.read_text(encoding="utf-8")
    if new in txt and old not in txt:
        return
    assert old in txt, f"Missing in {rel}: {old[:110]!r}"
    assert txt.count(old) == 1, f"Non-unique in {rel}: {old[:110]!r}"
    p.write_text(txt.replace(old, new, 1), encoding="utf-8")


def append_recap0(rel: str, extra: str) -> None:
    p = ROOT / rel
    txt = p.read_text(encoding="utf-8")
    if extra.strip() in txt:
        return
    sp = lv.load_spec(p)
    recap = [sc for sc in sp["scenes"] if sc["kind"] == "recap"][0]
    old = recap["steps"][0]["say"]
    assert old in txt and txt.count(old) == 1
    p.write_text(txt.replace(old, old.rstrip() + " " + extra.strip(), 1), encoding="utf-8")


PATCHES = [
    ("lessons/aif/L05_thoa_rang_buoc.yaml", "cho bài toán Sudoku hay xếp thời khoá biểu không trùng giờ.", "cho bài toán xếp ô số hay xếp lịch không trùng giờ."),
    ("lessons/aif/L06_tro_choi_doi_khang.yaml",
     "Điều tuyệt đẹp của cắt tỉa alpha và beta là nó luôn cho ra cùng một kết quả chính xác y hệt cực đại cực tiểu đầy đủ mà không mất mát bất kỳ thông tin tối ưu nào.",
     "Cắt tỉa alpha và beta luôn trả về đáp án y hệt thuật toán cực đại cực tiểu đầy đủ. Ta hoàn toàn không mất bất kỳ thông tin tối ưu nào ở gốc."),
    ("lessons/aif/L07_cay_mo_phong_ngau_nhien.yaml",
     "Tuy vậy ở những trạng thái có thế cờ chiến thuật bén nhạy dễ thua sau một nước sai, mô phỏng ngẫu nhiên thuần tuý có thể bỏ sót đường đi sâu nên ngoài thực tế thường kết hợp thêm mạng nơ-ron.",
     "Tuy vậy với các thế cờ dễ thua chỉ sau một nước sai, mô phỏng ngẫu nhiên thuần tuý có thể bỏ sót nhánh sâu. Ngoài thực tế hệ thống hay ghép thêm mạng nơ-ron."),
    ("lessons/aif/L08_logic_menh_de.yaml",
     "Khi phân tích một tập quy tắc nghiệp vụ hay mạch kiểm tra an toàn phần mềm, phép kiểm mô hình buộc ta rà soát mọi tổ hợp chân trị mà không bỏ sót bất kỳ ngoại lệ ẩn nào.",
     "Khi phân tích quy tắc nghiệp vụ hay mạch kiểm an toàn, phép kiểm mô hình rà soát đủ mọi tổ hợp chân trị. Nhờ vậy ta không bỏ sót ngoại lệ ẩn nào."),
    ("lessons/aif/L08_logic_menh_de.yaml",
     "Trong tình huống số lượng biến lên tới hàng trăm, người ta chuyển từ bảng chân trị thô sang các bộ giải thoả mãn logic hiện đại biết phân tích xung đột và học thêm mệnh đề cắt nhánh tự động.",
     "Khi số biến lên tới hàng trăm, ta chuyển sang các bộ giải thoả mãn logic hiện đại. Chúng biết phân tích xung đột và tự học thêm mệnh đề cắt nhánh."),
    ("lessons/aif/L08_logic_menh_de.yaml",
     "Một lưu ý rất thực tế là chỉ một câu mâu thuẫn lọt vào tập tri thức sẽ làm tập mô hình rỗng và kéo theo mọi câu bất kỳ, nên bước kiểm tra nhất quán luôn phải chạy trước tiên.",
     "Một câu mâu thuẫn lọt vào tri thức sẽ làm tập mô hình rỗng và kéo theo mọi câu bất kỳ. Vì vậy ta luôn phải chạy bước kiểm tra nhất quán trước tiên."),
    ("lessons/aif/L09_suy_dien_tien_lui.yaml",
     "Trong khi đó, suy diễn lùi phù hợp cho bài toán hỏi đáp hay kiểm định quyền truy cập vì nó chỉ chạm tới những nhánh luật có liên quan trực tiếp đến giả thuyết đang đặt ra.",
     "Trong khi đó, suy diễn lùi hợp cho bài toán hỏi đáp hay kiểm định quyền truy cập. Nó chỉ đụng tới những nhánh luật dẫn thẳng về giả thuyết đang xét."),
    ("lessons/aif/L10_lap_ke_hoach.yaml",
     "Trong nhiều hệ robot công nghiệp và điều phối kho hàng tự động, việc mô hình hoá gọn từng thao tác thành tiền điều kiện cùng hai danh sách thêm và xoá giúp tái sử dụng trọn bộ giải tìm kiếm chuẩn.",
     "Trong các hệ robot kho vận, mỗi thao tác được viết gọn thành tiền điều kiện và hiệu ứng thêm xoá. Cách mô tả chung giúp tái sử dụng bộ giải tìm kiếm chuẩn."),
    ("lessons/aif/L10_lap_ke_hoach.yaml",
     "Thay vì phải lập trình tay từng kịch bản riêng rẽ rất dễ gãy khi đổi quy tắc kho, kỹ sư chỉ cần bổ sung một mẫu hành động mới là hệ tìm kiếm tự tìm ra đường đi hợp lệ.",
     "Thay vì viết tay từng kịch bản riêng rất dễ gãy khi đổi quy tắc kho, ta chỉ thêm mẫu hành động mới. Hệ tìm kiếm sẽ tự tìm ra dãy bước hợp lệ."),
    ("lessons/aif/L10_lap_ke_hoach.yaml",
     "Với không gian trạng thái lớn hàng triệu cấu hình, người ta còn xây hàm đánh giá từ việc bỏ qua hiệu ứng xoá để dẫn đường tìm kiếm tiến về đích nhanh hơn mà vẫn giữ chính xác.",
     "Khi không gian đạt hàng triệu cấu hình, ta rút ra hàm đánh giá bằng cách tạm bỏ hiệu ứng xoá. Cách này dẫn đường tìm kiếm về đích nhanh mà vẫn an toàn."),
    ("lessons/aif/L12_lap_gia_tri.yaml",
     "Khi bài toán mở rộng lên không gian trạng thái liên tục hoặc hàng triệu ô không thể chứa vừa một bảng giá trị cố định, phương pháp lặp giá trị chuyển thành nền tảng cho học tăng cường hiện đại.",
     "Khi chuyển sang không gian liên tục hay hàng triệu trạng thái không thể giữ hết bằng bảng, lặp giá trị trở thành nền tảng cho học tăng cường hiện đại."),
    ("lessons/aif/L13_tong_hop.yaml",
     "Ngược lại, khi không gian trạng thái bùng nổ vượt ngưỡng duyệt hết hoặc môi trường thiếu công thức chuyển trạng thái rõ ràng, hãy ghép mô phỏng và hàm ước lượng học được đúng chỗ.",
     "Ngược lại khi không gian bùng nổ vượt ngưỡng duyệt hết hay thiếu mô hình rõ ràng, ta ghép thêm mô phỏng ngẫu nhiên. Hàm ước lượng học được sẽ dẫn đường đúng chỗ."),
]

for rel, o, n in PATCHES:
    rep(rel, o, n)

EXTRAS = {
    "lessons/aif/L00_tac_tu_moi_truong.yaml": "Nhận diện chuẩn năm tiêu chí môi trường giúp bạn chọn ngay thiết kế tác tử vừa đủ đơn giản vừa tin cậy.",
    "lessons/aif/L01_bai_toan_tim_kiem.yaml": "Đừng quên phân biệt rành mạch số cạnh với tổng chi phí đường đi trên đồ thị có trọng số. Tập trung viết đúng hàm mở rộng và lưu dấu đã thăm sẽ giúp mã nguồn chạy gọn trong bài tập ngay sau đây.",
    "lessons/aif/L03_thiet_ke_ham_danh_gia.yaml": "Việc kiểm nghiệm trên tập trạng thái mẫu giúp bạn tự tin rằng thuật toán tìm kiếm luôn chạy nhanh mà không đánh mất đáp số ngắn nhất.",
    "lessons/aif/L04_tim_kiem_cuc_bo.yaml": "Nhớ kiểm tra điều kiện dừng thật kỹ trước khi thoát vòng lặp tìm láng giềng.",
    "lessons/aif/L05_thoa_rang_buoc.yaml": "Ngoài việc phát hiện ngõ cụt sớm, cách sắp xếp thứ tự xét biến thông minh còn cắt giảm bộ nhớ ngăn xếp đáng kể. Trong phần thực hành ngay tới đây, bạn sẽ viết chương trình liệt kê toàn bộ không gian cấu hình trên bản đồ sáu vùng nối tám cạnh. Sau đó chỉ một phép lọc đơn giản mọi ràng buộc cạnh kề sẽ trích xuất ra chính xác mọi nghiệm hợp lệ.",
    "lessons/aif/L06_tro_choi_doi_khang.yaml": "Hãy quan sát kỹ hai tham số cận dưới và cận trên thay đổi ra sao qua từng nút con từ trái sang phải. Nắm vững quy tắc cập nhật cận này giúp bạn giải thích rành mạch vì sao một nút lá không bao giờ cần phải mở. Trong bài tập thực hành liền kề, bạn sẽ tự cài đặt vòng lặp cắt tỉa trên cây ba nhánh mới và đếm đúng tổng số lá đã chạm tới.",
    "lessons/aif/L07_cay_mo_phong_ngau_nhien.yaml": "Cân bằng đúng giữa khám phá nước mới và khai thác nước thắng cao là bí quyết của tìm kiếm cây hiện đại.",
    "lessons/aif/L08_logic_menh_de.yaml": "Một quy trình gọn gàng trong thực hành gồm ba bước nối tiếp là sinh đủ mọi bộ gán, giữ các bộ thoả toàn bộ tri thức rồi kiểm chứng kết luận. Nếu tri thức có ba biến mệnh đề, bảng chân trị chỉ có tám dòng nên một vòng lặp đơn giản giải quyết trọn vẹn trong nháy mắt. Cách làm tuy ngắn nhưng đặt nền móng tư duy cực kỳ chuẩn xác trước khi chuyển sang bộ suy diễn luật tuyến tính ở bài tiếp theo.",
    "lessons/aif/L09_suy_dien_tien_lui.yaml": "Lưu ý thêm rằng suy diễn tiến tìm ra tất cả mệnh đề hệ quả đúng từ tri thức hiện có ngay cả khi ta chưa đặt câu hỏi cụ thể nào. Ngược lại nếu cơ sở dữ liệu chứa hàng nghìn luật phức tạp trong khi người dùng chỉ cần biết một câu kết luận duy nhất có đúng hay không, suy diễn lùi tiết kiệm rất nhiều phép đối chiếu dư thừa. Ngoài dạng luật xác định một kết luận dương, hệ thống logic thực tế dùng thêm phép hợp giải tổng quát để xử lý câu phủ định. Giờ là lúc bạn tự chạy quy trình suy diễn tiến qua bài tập năm luật.",
    "lessons/aif/L10_lap_ke_hoach.yaml": "Cần lưu ý rằng các hành động đảo vị trí khối đòi hỏi kiểm soát chặt xem đỉnh khối đó đã thật sự trống hay chưa trước khi nhấc lên. Việc mã hoá trạng thái bằng bộ cặp đã sắp xếp giúp tránh trùng lặp trạng thái trong tập đã thăm khi chạy tìm kiếm theo chiều rộng. Chính cấu trúc sạch sẽ này bảo đảm chương trình luôn tìm thấy chuỗi thao tác ít bước nhất để đưa chồng khối từ trạng thái đầu về đích.",
    "lessons/aif/L11_mang_bayes.yaml": "Thao tác chuẩn hoá cuối cùng bằng cách chia tổng hai nhánh sẽ trả về xác suất hậu nghiệm chính xác.",
    "lessons/aif/L12_lap_gia_tri.yaml": "Hãy chú ý cập nhật giá trị mới bằng mảng tạm thay vì ghi đè ngay trong vòng lặp nếu muốn đúng bản cập nhật đồng bộ.",
    "lessons/aif/L13_tong_hop.yaml": "Đặt đúng thước đo chi phí và nhớ giới hạn cắt độ sâu luôn là bước bảo vệ hệ thống chạy ổn định ngoài thực tế. Kết thúc phần lý thuyết hôm nay, bạn sẽ dùng công thức lôgarit để tính cỡ cây trò chơi mới gồm hai mươi nhánh ở độ sâu sáu mươi. Bài thực hành nhỏ này chứng minh ngay hiệu quả giảm bớt số bậc khi cắt sâu ba tầng đầu tiên.",
}

for rel, ext in EXTRAS.items():
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
