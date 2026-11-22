"""Replace overly long LLM recap extras on L03, L07..L12 with short <=140c sentences, then verify all 69 lessons & run full gates."""
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

REPLACE_MAP = {
    "L03": (
        "Điểm mạnh lớn nhất của biểu diễn bằng vector đặc là các hướng ngữ nghĩa tương tự hay cùng vai trò ngữ pháp tự nhiên tụ thành từng cụm gần nhau trong không gian nhiều chiều. ",
        "Biểu diễn bằng vector đặc gom các từ cùng ngữ cảnh đứng gần nhau thành từng cụm rõ nét trong không gian nhiều chiều. "
        "Cách này phản ánh mượt vai trò ngữ nghĩa mà không cần gán nhãn thủ công từng cặp từ. "
    ),
    "L07": (
        "Ở mức nhiệt độ thấp dưới một, phép chia làm giãn khoảng cách giữa điểm cao và điểm thấp, dồn xác suất mạnh vào vài lựa chọn đầu bảng khiến câu trả lời an toàn nhưng ít biến đổi. "
        "Khi tăng nhiệt độ lên cao hơn một, đuôi phân phối được nâng lên đáng kể giúp mô hình chọn nhiều từ ít gặp hơn và tăng rủi ro lạc đề hoặc sai sự kiện. "
        "Kết hợp cắt theo hạng k cố định với cắt theo tổng xác suất hạt nhân giúp loại bỏ hàng nghìn từ tố đuôi vô nghĩa mà vẫn giữ được độ linh hoạt ở những chỗ có nhiều đáp án hay. "
        "Hãy thử đo tỷ lệ lặp chữ và độ chính xác theo từng bộ tham số sinh chữ trên tập câu hỏi đại diện trước khi khoá cấu hình cho sản phẩm. "
        "Khả năng cân chỉnh linh hoạt bước chọn từ cuối cùng chính là chìa khoá phân tách rõ rệt giữa công cụ tra cứu chuẩn xác và trợ lý sáng tạo nội dung.",
        "Ở nhiệt độ thấp dưới một, xác suất dồn mạnh vào vài lựa chọn đứng đầu nên câu trả lời ổn định nhưng ít đa dạng. "
        "Khi tăng nhiệt độ lên cao hơn một, mô hình dễ chọn thêm nhiều từ hiếm nên giàu biến đổi nhưng cũng dễ lạc đề hơn. "
        "Cắt theo hạng k cố định giúp loại bớt phần đuôi dài vô nghĩa khỏi bảng phân phối. "
        "Kết hợp thêm cắt theo tổng xác suất hạt nhân giúp giữ nhiều nhánh hợp lý ở chỗ có nhiều cách diễn đạt hay. "
        "Bạn nên đo cả tỉ lệ lặp chữ lẫn độ chính xác theo từng bộ tham số trước khi khoá cấu hình. "
        "Bước chọn từ cuối cùng này phân tách rõ công cụ tra cứu chuẩn xác với trợ lý sáng tạo nội dung."
    ),
    "L08": (
        "Thay vì cập nhật toàn bộ hàng tỉ trọng số kèm trạng thái bộ tối ưu khổng lồ, phương pháp hạng thấp đóng băng ma trận gốc và chỉ học hai ma trận hẹp ghép song song vào lớp tuyến tính. "
        "Nhờ kích thước tệp trọng số bổ sung chỉ vài chục mê-ga-byte, một máy chủ duy nhất có thể phục vụ nhiều tác vụ chuyên biệt cùng lúc chỉ bằng cách hoán đổi bộ trọng số nhẹ đi kèm. "
        "Tuy vậy, tinh chỉnh hiệu quả nhất cho dạy cấu trúc trả lời hay văn phong chuyên ngành, còn kiến thức mới biến động hằng ngày vẫn nên tách sang bước truy xuất tài liệu bên ngoài.",
        "Thay vì cập nhật toàn bộ hàng tỉ trọng số, phương pháp hạng thấp giữ nguyên ma trận sẵn có và chỉ học thêm hai ma trận rất hẹp. "
        "Số tham số huấn luyện mới giảm hàng trăm lần nên vừa nhẹ bộ nhớ đồ hoạ vừa tiết kiệm thời gian chạy. "
        "Nhờ tệp trọng số bổ sung gọn nhẹ chỉ vài chục mê-ga-byte, một máy chủ có thể phục vụ nhiều tác vụ riêng. "
        "Khi chuyển yêu cầu, hệ thống chỉ cần đổi bộ ma trận hạng thấp mà vẫn dùng chung phần lõi nặng bên dưới. "
        "Tuy vậy, tinh chỉnh hợp nhất cho việc dạy định dạng và phong cách trả lời. "
        "Dữ kiện mới biến động hằng ngày vẫn nên tách sang bước truy xuất kho tri thức bên ngoài."
    ),
    "L09": (
        "Bước học có giám sát theo chỉ dẫn giúp mô hình hiểu cấu trúc câu hỏi đáp nhưng vẫn chưa phân biệt rành rọt hai phương án cùng đúng ngữ pháp mà khác mức hữu ích hay an toàn. "
        "Chính lúc này dữ liệu so sánh theo cặp của con người phát huy tác dụng, biến cảm nhận chủ quan thành hàm xác suất chênh lệch điểm thưởng rõ ràng để huấn luyện mô hình chấm điểm. "
        "Khi tối ưu chính sách dựa trên mô hình chấm đó, thành phần phạt phân kỳ giữ khoảng cách an toàn với điểm xuất phát để câu văn không trôi vào lối diễn đạt rườm rà lấy lòng bộ chấm. "
        "Cuối cùng, đánh giá chéo trên người dùng thật hoặc bộ đề mù độc lập là bước chốt chặn bắt buộc trước khi phát hành mô hình mới. "
        "Nắm chắc chu trình ba bước này giúp bạn đọc vị nhanh mọi biểu hiện lệch mục tiêu ở các hệ thống trợ lý hội thoại thực tế.",
        "Học có giám sát theo chỉ dẫn giúp mô hình quen cấu trúc hỏi đáp chuẩn xác hơn. "
        "Tuy nhiên, nó vẫn khó phân biệt hai câu trả lời cùng trôi chảy nhưng khác mức hữu ích và an toàn. "
        "Dữ liệu so sánh theo cặp cho phép chuyển đánh giá con người thành độ lệch xác suất rõ ràng. "
        "Mô hình chấm điểm học từ cặp thắng thua này để ước lượng mức độ vừa ý người dùng. "
        "Khi tối ưu theo bộ chấm đó, ràng buộc phạt độ lệch giữ câu trả lời không đi quá xa mô hình ban đầu. "
        "Nhờ vậy hệ thống tránh sa vào lối viết sáo rỗng hay kéo dài câu để câu điểm giả. "
        "Đánh giá độc lập với người dùng thật hoặc bộ đề riêng luôn là bước chốt chặn bắt buộc trước khi phát hành."
    ),
    "L10": (
        "Một con số phần trăm đúng đơn lẻ trên một tập thử nghiệm nhỏ dễ gây ngộ nhận nếu không tính kèm biên độ sai số thống kê quanh ước lượng mẫu đó. "
        "Khi so hai phiên bản mô hình trên cùng danh sách câu hỏi, phân tích những câu mà một bản làm đúng còn bản kia làm sai cho sức phân biệt nhạy hơn hẳn việc cộng điểm trung bình rời rạc. "
        "Ngoài ra, nguy cơ rò rỉ dữ liệu kiểm tra vào kho huấn luyện lớn đòi hỏi kiểm định độ trùng lặp từng câu hoặc đánh giá trên tập câu hỏi mới thu thập sau thời điểm huấn luyện. "
        "Đầu tư cho bộ đề chuẩn sạch và phép kiểm phù hợp giúp bạn tránh mất thời gian theo đuổi những cải tiến ảo không lặp lại khi đưa vào vận hành. "
        "Đó là kỷ luật cốt lõi giúp các nhóm kỹ thuật đưa ra quyết định nâng cấp mô hình có cơ sở định lượng vững chắc.",
        "Một tỉ lệ đúng đơn lẻ trên tập thử nhỏ dễ gây ngộ nhận nếu thiếu biên độ sai số thống kê đi kèm. "
        "Tính thêm khoảng tin cậy 95 phần trăm cho biết độ chênh lệch có lớn hơn dao động ngẫu nhiên hay không. "
        "Khi so hai mô hình trên cùng bộ câu hỏi, tập trung vào nhóm câu bất đồng giúp tăng độ nhạy kiểm định. "
        "Ngoài ra, kho dữ liệu khổng lồ dễ vô tình chứa sẵn đáp án của bộ câu hỏi kiểm tra công khai. "
        "Bạn cần kiểm lọc trùng lặp hoặc tự dựng bộ câu hỏi mới thu thập sau thời điểm huấn luyện. "
        "Kỷ luật kiểm định chặt giúp đội kỹ thuật đầu tư đúng chỗ và tránh theo đuổi những cải tiến ảo."
    ),
    "L11": (
        "Khi xác suất tự tin mô hình gán cho dự đoán luôn cao hơn tỉ lệ trả lời đúng thật tế ở từng nhóm điểm, hệ thống đang rơi vào trạng thái quá tự tin rất nguy hiểm cho quyết định tự động. "
        "Biểu đồ tin cậy theo các khoảng xác suất và sai số hiệu chuẩn mong đợi cho thấy ngay mức lệch cần chỉnh ở từng ngưỡng tin cậy khác nhau. "
        "Nếu bài toán cho phép phát sinh nhiều lộ trình suy luận độc lập rồi gom chọn đáp án đồng thuận nhất, chất lượng giải bài toán phức tạp tăng rõ rệt khi các nhánh đi theo lối tư duy đa dạng. "
        "Ngược lại, nếu mọi nhánh chỉ lặp đi lặp lại cùng một lỗi tính toán quen thuộc, việc tăng thêm số lần lấy mẫu sẽ chỉ đội chi phí mà không cải thiện được độ chính xác cuối cùng. "
        "Kết hợp đo hiệu chuẩn cùng kiểm tra độ đa dạng nhánh giúp bạn chọn đúng ngưỡng tự động hoá hay chuyển người kiểm duyệt.",
        "Nếu mức tự tin mô hình báo ra luôn cao hơn tỉ lệ đúng thật tế, hệ thống đang mắc lỗi quá tự tin. "
        "Sai số hiệu chuẩn mong đợi tổng hợp độ lệch giữa điểm tin cậy và tỉ lệ đúng qua từng nhóm xác suất. "
        "Với bài toán khó, sinh nhiều lộ trình suy luận độc lập rồi chọn đáp án đồng thuận giúp giảm lỗi ngẫu nhiên. "
        "Cách này chỉ hiệu quả khi các nhánh thật sự đa dạng và không lặp lại cùng một lối suy nghĩ sai. "
        "Nếu mọi nhánh vấp chung một chỗ, lấy mẫu thêm chỉ làm tăng chi phí tính toán vô ích. "
        "Đo cả độ hiệu chuẩn lẫn tính đa dạng nhánh giúp bạn đặt đúng ngưỡng chuyển cho người kiểm duyệt."
    ),
    "L12": (
        "Thay vì nhồi mọi tài liệu vào trọng số mô hình tốn kém, kiến trúc sinh có truy xuất tìm đúng vài đoạn văn liên quan nhất làm ngữ cảnh tức thì ngay tại thời điểm hỏi. "
        "Nhờ vậy, khi chính sách hay số liệu nội bộ thay đổi trong ngày, đội vận hành chỉ cần cập nhật chỉ mục tìm kiếm mà không phải huấn luyện lại toàn bộ mô hình nền tảng. "
        "Tuy nhiên, hệ thống chỉ trả lời đúng khi cả hai khâu hoạt động nhịp nhàng, tức là khâu truy xuất kéo được đúng đoạn chứa câu trả lời, và khâu sinh chữ bám sát đoạn đã kéo để trích dẫn mạch lạc. "
        "Luôn áp dụng lọc quyền truy cập người dùng ngay ở tầng tìm kiếm để mô hình không vô tình trích dẫn nội dung nhạy cảm vượt thẩm quyền. "
        "Phân tách rạch ròi bài kiểm tra từng khâu là thói quen quan trọng nhất để giữ trợ lý tài liệu nội bộ luôn trung thực.",
        "Thay vì nhồi mọi thông tin vào trọng số tốn kém, hệ sinh có truy xuất tìm vài đoạn văn liên quan nhất ngay khi hỏi. "
        "Khi quy định nội bộ thay đổi, kỹ sư chỉ cần cập nhật chỉ mục tìm kiếm thay vì huấn luyện lại mô hình. "
        "Tuy nhiên, chất lượng cuối cùng phụ thuộc vào sự phối hợp chặt chẽ giữa cả hai tầng hệ thống. "
        "Tầng truy xuất phải kéo lên được đúng đoạn chứa câu trả lời nằm trong nhóm đầu. "
        "Tầng sinh chữ phải bám sát ngữ cảnh được cấp và trích dẫn nguồn rõ ràng. "
        "Luôn lọc quyền truy cập của người dùng ngay ở bước tìm để chặn rò rỉ dữ liệu mật. "
        "Kiểm tra riêng rẽ từng khâu là thói quen tốt nhất để giữ hệ thống trả lời trung thực."
    ),
    "L13": (
        "Từ mô hình bigram đếm bảng thô tới các trợ lý ngôn ngữ dài hàng trăm nghìn từ tố, mọi bước nhảy vọt về năng lực đều đi kèm một bài toán cân bằng mới giữa chất lượng, độ trễ và ngân sách tính toán. "
        "Khi triển khai thực tế, chọn kích thước mô hình gọn phù hợp, lượng tử hoá trọng số hợp lý và quản trị tốt bộ nhớ đệm giúp tiết kiệm hàng chục lần chi phí phần cứng mỗi tháng. "
        "Quan trọng hơn cả là thói quen kiểm chứng lại toàn diện bằng số liệu đo thật mỗi khi thay đổi một tham số hay bật một kỹ thuật tăng tốc mới. "
        "Chỉ những cải tiến giữ vững chất lượng đầu ra xuyên suốt cả độ dài ngữ cảnh lẫn độ chính xác sự kiện mới xứng đáng được đưa lên hệ thống chính thức. "
        "Hãy mang tinh thần đo lường chặt chẽ này qua từng bài thực hành để sẵn sàng bước sang chuyên đề tác tử tự chủ.",
        "Từ mô hình đếm cặp hai từ đơn giản tới trợ lý xử lý ngữ cảnh dài, mỗi bước tiến đều đòi hỏi bài toán cân bằng mới. "
        "Bạn phải cân đối đồng thời cả chất lượng trả lời, độ trễ phản hồi và ngân sách phần cứng thực tế. "
        "Khi triển khai, chọn cỡ mô hình vừa phải, lượng tử hoá trọng số và quản trị bộ nhớ đệm giúp giảm chi phí vận hành. "
        "Quan trọng hơn cả là thói quen kiểm chứng lại toàn diện bằng số liệu đo thật sau mỗi thay đổi. "
        "Chỉ những tối ưu giữ vững độ chính xác trên cả độ dài ngữ cảnh dài mới nên đưa lên hệ thống thật. "
        "Hãy mang tinh thần đo lường chặt chẽ này qua bài thực hành trước khi sang chuyên đề tác tử tự chủ."
    ),
}

for lid, (old, new) in REPLACE_MAP.items():
    p = sorted((ROOT / "lessons" / "llm").glob(f"{lid}_*.yaml"))[0]
    txt = p.read_text(encoding="utf-8")
    if new in txt:
        continue
    assert old in txt, f"{lid}: old block not found"
    p.write_text(txt.replace(old, new, 1), encoding="utf-8", newline="\n")

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
