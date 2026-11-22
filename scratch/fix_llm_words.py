"""Top up LLM L00..L04, L07..L13 word counts >= 1655w + fix LLM L09 E29, then run full gates on 5 Stage 9 courses."""
from contextlib import redirect_stdout
import io
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(r"D:\research-video")
sys.path.insert(0, str(ROOT / "tools"))
import lv  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")

# Fix E29 'bản gốc' in L09 yaml & fix_s9_5courses_v2.py
l09 = ROOT / "lessons" / "llm" / "L09_can_chinh.yaml"
t09 = l09.read_text(encoding="utf-8")
if "tránh trôi xa bản gốc" in t09:
    l09.write_text(t09.replace("tránh trôi xa bản gốc", "tránh trôi xa mô hình khởi điểm"), encoding="utf-8", newline="\n")

v2p = ROOT / "scratch" / "fix_s9_5courses_v2.py"
tv2 = v2p.read_text(encoding="utf-8")
if "tránh trôi xa bản gốc" in tv2:
    v2p.write_text(tv2.replace("tránh trôi xa bản gốc", "tránh trôi xa mô hình khởi điểm"), encoding="utf-8", newline="\n")

EXTRA = {
    "L00": (
        "Mỗi dự đoán ở bước tiếp theo thực chất là chọn một từ tố hợp lệ trên bảng phân phối xác suất điều kiện theo đúng ngữ cảnh đứng trước. "
        "Khi ghép cả đoạn văn bản dài hàng trăm từ, phép nhân liên tiếp những số nhỏ hơn một đòi hỏi ta chuyển sang tổng lôgarit để tránh tràn số dưới mức biểu diễn. "
        "Nhờ góc nhìn xác suất thuần tuý đó, bạn sẽ không bị nhầm lẫn giữa câu văn trôi chảy hay gặp với câu phát biểu đúng về mặt sự kiện ngoài đời thật."
    ),
    "L01": (
        "Khi một cặp từ mới xuất hiện trong văn bản thử nghiệm chưa từng thấy trong tập huấn luyện, xác suất cả câu lập tức sụp về không và kéo độ hỗn loạn lên vô cực. "
        "Các kỹ thuật làm trơn trích một phần nhỏ xác suất từ cặp quen thuộc chia đều cho cặp vắng mặt, giúp phân phối luôn dương và đo được độ hỗn loạn hữu hạn. "
        "Luôn kiểm soát chặt quy trình tách từ tố và bộ ngữ liệu kiểm thử để hai mô hình so với nhau trên cùng một thước đo công bằng nhất."
    ),
    "L02": (
        "Mỗi lần gộp hai mảnh liền kề có tần suất cao nhất là ta rút ngắn độ dài chuỗi đầu vào thêm một phần, đổi lấy kích thước từ điển tăng thêm một mục mới. "
        "Do thứ tự gộp quy định thẳng cách ghép mảnh về sau, việc lưu đầy đủ danh sách các cặp gộp theo đúng trình tự học được là yêu cầu bắt buộc khi đóng gói bộ tách từ. "
        "Ngoài ra, bạn cũng nên kiểm tra mật độ tách trên chính văn bản tiếng Việt thực tế của dự án trước khi chốt ngưỡng độ dài ngữ cảnh. "
        "Nhờ đo trước số từ tố trung bình cho mỗi câu, ta ước lượng sát chi phí tính toán lẫn thời gian phản hồi thực tế khi hệ thống đi vào phục vụ nhiều người dùng cùng lúc. "
        "Đây là kỹ năng nền tảng giúp bạn làm chủ hoàn toàn mọi đường ống xử lý văn bản đầu vào cho mô hình ngôn ngữ."
    ),
    "L03": (
        "Điểm mạnh lớn nhất của biểu diễn bằng vector đặc là các hướng ngữ nghĩa tương tự hay cùng vai trò ngữ pháp tự nhiên tụ thành từng cụm gần nhau trong không gian nhiều chiều. "
        "Khi tính độ tương tự cô-sin, phép chia cho tích độ dài hai vector loại bỏ ảnh hưởng độ dài và chỉ giữ lại góc mở giữa hai hướng. "
        "Tuy nhiên, vì cách huấn luyện chỉ dựa trên ngữ cảnh xuất hiện xung quanh từ, hai khái niệm đối lập nhau nhưng dùng chung cấu trúc câu thường có góc rất hẹp. "
        "Do đó, bạn cần kiểm tra thêm ngữ cảnh hoặc dùng lớp phân biệt chuyên biệt thay vì tin hoàn toàn vào độ gần về hướng của hai vector đơn lẻ."
    ),
    "L04": (
        "Nhờ cơ chế mặt nạ tam giác chặn mọi liên kết nhìn tới các vị trí đứng sau, toàn bộ chuỗi đầu vào được tính song song trong một lượt khi huấn luyện. "
        "Đồng thời, mã hoá vị trí bổ sung dấu ấn thứ tự rõ ràng để cơ chế tự chú ý phân biệt chính xác ai tác động lên ai trong câu văn hoàn chỉnh."
    ),
    "L07": (
        "Ở mức nhiệt độ thấp dưới một, phép chia làm giãn khoảng cách giữa điểm cao và điểm thấp, dồn xác suất mạnh vào vài lựa chọn đầu bảng khiến câu trả lời an toàn nhưng ít biến đổi. "
        "Khi tăng nhiệt độ lên cao hơn một, đuôi phân phối được nâng lên đáng kể giúp mô hình chọn nhiều từ ít gặp hơn và tăng rủi ro lạc đề hoặc sai sự kiện. "
        "Kết hợp cắt theo hạng k cố định với cắt theo tổng xác suất hạt nhân giúp loại bỏ hàng nghìn từ tố đuôi vô nghĩa mà vẫn giữ được độ linh hoạt ở những chỗ có nhiều đáp án hay. "
        "Hãy thử đo tỷ lệ lặp chữ và độ chính xác theo từng bộ tham số sinh chữ trên tập câu hỏi đại diện trước khi khoá cấu hình cho sản phẩm. "
        "Khả năng cân chỉnh linh hoạt bước chọn từ cuối cùng chính là chìa khoá phân tách rõ rệt giữa công cụ tra cứu chuẩn xác và trợ lý sáng tạo nội dung."
    ),
    "L08": (
        "Thay vì cập nhật toàn bộ hàng tỉ trọng số kèm trạng thái bộ tối ưu khổng lồ, phương pháp hạng thấp đóng băng ma trận gốc và chỉ học hai ma trận hẹp ghép song song vào lớp tuyến tính. "
        "Nhờ kích thước tệp trọng số bổ sung chỉ vài chục mê-ga-byte, một máy chủ duy nhất có thể phục vụ nhiều tác vụ chuyên biệt cùng lúc chỉ bằng cách hoán đổi bộ trọng số nhẹ đi kèm. "
        "Tuy vậy, tinh chỉnh hiệu quả nhất cho dạy cấu trúc trả lời hay văn phong chuyên ngành, còn kiến thức mới biến động hằng ngày vẫn nên tách sang bước truy xuất tài liệu bên ngoài."
    ),
    "L09": (
        "Bước học có giám sát theo chỉ dẫn giúp mô hình hiểu cấu trúc câu hỏi đáp nhưng vẫn chưa phân biệt rành rọt hai phương án cùng đúng ngữ pháp mà khác mức hữu ích hay an toàn. "
        "Chính lúc này dữ liệu so sánh theo cặp của con người phát huy tác dụng, biến cảm nhận chủ quan thành hàm xác suất chênh lệch điểm thưởng rõ ràng để huấn luyện mô hình chấm điểm. "
        "Khi tối ưu chính sách dựa trên mô hình chấm đó, thành phần phạt phân kỳ giữ khoảng cách an toàn với điểm xuất phát để câu văn không trôi vào lối diễn đạt rườm rà lấy lòng bộ chấm. "
        "Cuối cùng, đánh giá chéo trên người dùng thật hoặc bộ đề mù độc lập là bước chốt chặn bắt buộc trước khi phát hành mô hình mới. "
        "Nắm chắc chu trình ba bước này giúp bạn đọc vị nhanh mọi biểu hiện lệch mục tiêu ở các hệ thống trợ lý hội thoại thực tế."
    ),
    "L10": (
        "Một con số phần trăm đúng đơn lẻ trên một tập thử nghiệm nhỏ dễ gây ngộ nhận nếu không tính kèm biên độ sai số thống kê quanh ước lượng mẫu đó. "
        "Khi so hai phiên bản mô hình trên cùng danh sách câu hỏi, phân tích những câu mà một bản làm đúng còn bản kia làm sai cho sức phân biệt nhạy hơn hẳn việc cộng điểm trung bình rời rạc. "
        "Ngoài ra, nguy cơ rò rỉ dữ liệu kiểm tra vào kho huấn luyện lớn đòi hỏi kiểm định độ trùng lặp từng câu hoặc đánh giá trên tập câu hỏi mới thu thập sau thời điểm huấn luyện. "
        "Đầu tư cho bộ đề chuẩn sạch và phép kiểm phù hợp giúp bạn tránh mất thời gian theo đuổi những cải tiến ảo không lặp lại khi đưa vào vận hành. "
        "Đó là kỷ luật cốt lõi giúp các nhóm kỹ thuật đưa ra quyết định nâng cấp mô hình có cơ sở định lượng vững chắc."
    ),
    "L11": (
        "Khi xác suất tự tin mô hình gán cho dự đoán luôn cao hơn tỉ lệ trả lời đúng thật tế ở từng nhóm điểm, hệ thống đang rơi vào trạng thái quá tự tin rất nguy hiểm cho quyết định tự động. "
        "Biểu đồ tin cậy theo các khoảng xác suất và sai số hiệu chuẩn mong đợi cho thấy ngay mức lệch cần chỉnh ở từng ngưỡng tin cậy khác nhau. "
        "Nếu bài toán cho phép phát sinh nhiều lộ trình suy luận độc lập rồi gom chọn đáp án đồng thuận nhất, chất lượng giải bài toán phức tạp tăng rõ rệt khi các nhánh đi theo lối tư duy đa dạng. "
        "Ngược lại, nếu mọi nhánh chỉ lặp đi lặp lại cùng một lỗi tính toán quen thuộc, việc tăng thêm số lần lấy mẫu sẽ chỉ đội chi phí mà không cải thiện được độ chính xác cuối cùng. "
        "Kết hợp đo hiệu chuẩn cùng kiểm tra độ đa dạng nhánh giúp bạn chọn đúng ngưỡng tự động hoá hay chuyển người kiểm duyệt."
    ),
    "L12": (
        "Thay vì nhồi mọi tài liệu vào trọng số mô hình tốn kém, kiến trúc sinh có truy xuất tìm đúng vài đoạn văn liên quan nhất làm ngữ cảnh tức thì ngay tại thời điểm hỏi. "
        "Nhờ vậy, khi chính sách hay số liệu nội bộ thay đổi trong ngày, đội vận hành chỉ cần cập nhật chỉ mục tìm kiếm mà không phải huấn luyện lại toàn bộ mô hình nền tảng. "
        "Tuy nhiên, hệ thống chỉ trả lời đúng khi cả hai khâu hoạt động nhịp nhàng: khâu truy xuất kéo được đúng đoạn chứa câu trả lời, và khâu sinh chữ bám sát đoạn đã kéo để trích dẫn mạch lạc. "
        "Luôn áp dụng lọc quyền truy cập người dùng ngay ở tầng tìm kiếm để mô hình không vô tình trích dẫn nội dung nhạy cảm vượt thẩm quyền. "
        "Phân tách rạch ròi bài kiểm tra từng khâu là thói quen quan trọng nhất để giữ trợ lý tài liệu nội bộ luôn trung thực."
    ),
    "L13": (
        "Từ mô hình bigram đếm bảng thô tới các trợ lý ngôn ngữ dài hàng trăm nghìn từ tố, mọi bước nhảy vọt về năng lực đều đi kèm một bài toán cân bằng mới giữa chất lượng, độ trễ và ngân sách tính toán. "
        "Khi triển khai thực tế, chọn kích thước mô hình gọn phù hợp, lượng tử hoá trọng số hợp lý và quản trị tốt bộ nhớ đệm giúp tiết kiệm hàng chục lần chi phí phần cứng mỗi tháng. "
        "Quan trọng hơn cả là thói quen kiểm chứng lại toàn diện bằng số liệu đo thật mỗi khi thay đổi một tham số hay bật một kỹ thuật tăng tốc mới. "
        "Chỉ những cải tiến giữ vững chất lượng đầu ra xuyên suốt cả độ dài ngữ cảnh lẫn độ chính xác sự kiện mới xứng đáng được đưa lên hệ thống chính thức. "
        "Hãy mang tinh thần đo lường chặt chẽ này qua từng bài thực hành để sẵn sàng bước sang chuyên đề tác tử tự chủ."
    ),
}

for lid, ext in EXTRA.items():
    p = sorted((ROOT / "lessons" / "llm").glob(f"{lid}_*.yaml"))[0]
    txt = p.read_text(encoding="utf-8")
    if ext[:40] in txt:
        continue
    sp = lv.load_spec(p)
    recap = [sc for sc in sp["scenes"] if sc["kind"] == "recap"][0]
    old = recap["steps"][0]["say"]
    assert old in txt and txt.count(old) == 1, f"{lid}: unique recap0 failed"
    p.write_text(txt.replace(old, old.rstrip() + " " + ext, 1), encoding="utf-8", newline="\n")

bad = []
for c in ("irs", "agt", "llm", "rln", "cvi"):
    for fp in sorted((ROOT / "lessons" / c).glob("L*.yaml")):
        sp = lv.load_spec(fp)
        lid = sp["id"]
        w = sum(len((st.get("say") or "").split()) for sc in sp["scenes"] for st in sc["steps"])
        with redirect_stdout(io.StringIO()):
            res = lv.lint(sp, quiet=True)
        if res.errors or res.warnings:
            bad.append(f"{c.upper()}:{lid} E={res.errors} W={res.warnings}")
        if w < 1645:
            bad.append(f"{c.upper()}:{lid} w={w} (need +{1655-w})")
        for sc in sp["scenes"]:
            for idx, st in enumerate(sc["steps"]):
                say = st.get("say") or ""
                foc = st.get("focus")
                sents = lv.sentences(say)
                if foc is not None and len(foc) != len(sents):
                    bad.append(f"{c.upper()}:{lid}:{sc['id']}#{idx} focus={len(foc)} != sents={len(sents)}")
                for s in sents:
                    if len(s) > 170: bad.append(f"{c.upper()}:{lid}:{sc['id']}#{idx} >170 ({len(s)}): {s}")
                    if len(s.split()) > 38: bad.append(f"{c.upper()}:{lid}:{sc['id']}#{idx} >38w ({len(s.split())}): {s}")
                    if "càng " in s.lower(): bad.append(f"{c.upper()}:{lid}:{sc['id']}#{idx} 'càng ': {s}")
                    if re.search(r"[$_^]", s): bad.append(f"{c.upper()}:{lid}:{sc['id']}#{idx} TeX: {s}")
        print(f"CHECK {c.upper()}:{lid} w={w} E={len(res.errors)} W={len(res.warnings)}", flush=True)

for b in bad:
    print("BAD:", b, flush=True)
assert not bad, f"{len(bad)} issues across 5 Stage 9 courses"

PY = str(ROOT / ".venv" / "Scripts" / "python.exe")
for c in ("IRS", "AGT", "LLM", "RLN", "CVI"):
    for cmd in (
        [PY, "-B", "audit/review/sync_tpl_from_lesson.py", c, "--write"],
        [PY, "-B", "audit/review/screen_code.py", "check", "--course", c],
        [PY, "-B", "audit/review/lab_gate.py", c],
        [PY, "-B", "tools/lv.py", "curriculum", f"curriculum/{c.lower()}.yaml"],
        [PY, "-B", f"audit/{c.lower()}/verify_{c.lower()}.py"],
    ):
        print(">>> RUN:", " ".join(cmd), flush=True)
        r = subprocess.run(cmd, cwd=ROOT)
        assert r.returncode == 0, f"FAILED: {cmd}"
print("ALL 5 STAGE 9 COURSES (IRS/AGT/LLM/RLN/CVI = 69 LESSONS) PASSED FULL GATES!", flush=True)
