from contextlib import redirect_stdout
import io
from pathlib import Path
import re
import sys

ROOT = Path(r"D:\research-video")
sys.path.insert(0, str(ROOT / "tools"))
import lv  # noqa: E402


def append_recap0(rel: str, extra: str) -> None:
    p = ROOT / rel
    txt = p.read_text(encoding="utf-8")
    sp = lv.load_spec(p)
    recap = [sc for sc in sp["scenes"] if sc["kind"] == "recap"][0]
    old_say = recap["steps"][0]["say"]
    assert old_say in txt, f"Could not locate recap0 say in {rel}"
    assert txt.count(old_say) == 1, f"Non-unique recap0 say in {rel}"
    new_say = old_say.rstrip() + " " + extra.strip()
    p.write_text(txt.replace(old_say, new_say, 1), encoding="utf-8")


EXTRAS = {
    "lessons/cs115/L22_lan_truyen_nguoc.yaml": (
        "Nhờ tích hợp công cụ giải tích tự động này, bạn vừa tránh được lỗi sai số học vừa làm chủ nền tảng của mọi khung mạng sâu hiện đại."
    ),
    "lessons/cs115/L27_knn.yaml": (
        "Hãy nhớ mô hình không có bước huấn luyện tham số nào nhưng gánh nặng chuyển hết sang lúc suy đoán theo từng truy vấn. Khi số chiều đặc trưng tăng lên hàng trăm, mọi cặp điểm đều dần cách đều nhau và làm thước đo mất tác dụng. Vì vậy trước khi đo khoảng cách trên bảng dữ liệu lớn, bạn nên chiếu giảm chiều bằng phân tích thành phần chính của bài 16 hoặc phân tích phân biệt tuyến tính của bài 26. Cuối cùng hãy lưu bảng dữ liệu đã chuẩn hoá thang đo cùng giá trị K tối ưu rút ra từ kiểm định chéo để dùng lâu dài. Quy trình gọn nhưng chặt chẽ này giúp bạn tự tin áp dụng ngay thuật toán láng giềng gần nhất cho mọi bài toán phân loại và hồi quy ban đầu."
    ),
    "lessons/cs115/L28_cay_quyet_dinh.yaml": (
        "Một mẹo thực chiến quan trọng là dùng độ sâu nông từ ba đến năm tầng cho dữ liệu nhiễu hoặc ít mẫu, đồng thời theo dõi sai số ngoài túi trên phần mẫu không được bốc để tinh chỉnh rừng nhanh mà không cần tách thêm tập kiểm định riêng. Hãy cảnh giác với bẫy cây ưu tiên biến có nhiều giá trị rời rạc như mã số định danh khi đo độ lợi thông tin thuần tuý. Nắm vững cả mặt mạnh trực quan lẫn giới hạn này giúp bạn quyết định đúng khi nào nên chọn rừng ngẫu nhiên hay chuyển sang mô hình tăng cường theo chuỗi."
    ),
    "lessons/cs115/L31_nmf.yaml": (
        "Trên thực tế khi phân tích hàng vạn tài liệu hoặc ma trận đánh giá thưa thớt, chọn hạng phân rã nhỏ vừa đủ giúp ép mô hình gom các từ đồng nghĩa thành từng chủ đề cô đọng dễ đặt tên. Hãy luôn chạy thuật toán với nhiều hạt giống khởi tạo khác nhau rồi đối chiếu sai số tái tạo cùng độ ổn định của các chủ đề thu được trước khi chốt kết quả. Thêm một lượng phạt điều chuẩn nhẹ trên các ma trận hệ số còn giúp mỗi mẫu chỉ dùng đúng vài thành phần nổi bật nhất để biểu diễn gọn gàng."
    ),
    "lessons/cs115/L32_tsne.yaml": (
        "Ngoài ra độ bối rối nhỏ khoảng năm chỉ gom cụm rất cục bộ, còn độ bối rối ba mươi tới năm mươi mới cho cái nhìn rộng hơn qua các lân cận trung bình. Hãy luôn thử ít nhất hai hoặc ba giá trị độ bối rối cùng vài hạt giống khởi tạo khác nhau để chắc chắn nhóm cụm bạn thấy là cấu trúc thật chứ không phải ảo ảnh ngẫu nhiên của một lần tối ưu."
    ),
    "lessons/cs115/L34_cnn.yaml": (
        "Khi ghép nhiều lớp liên tiếp trên ảnh màu ba kênh, chiều sâu bản đồ đặc trưng tăng dần trong khi kích thước không gian co nhỏ lại để gom toàn bộ nét cục bộ thành khái niệm toàn cảnh ở tầng phân loại cuối. Đừng quên đặt phần đệm hợp lý nếu muốn giữ nguyên kích thước ảnh qua từng tầng."
    ),
    "lessons/cs115/L35_rnn_lstm.yaml": (
        "Việc hiểu rõ cơ chế duỗi theo thời gian và nút thắt truyền tin tuần tự cũng lý giải vì sao kiến trúc chú ý song song ở bài 41 ra đời sau này lại nhanh chóng vượt qua mạng hồi tiếp trên các chuỗi văn bản dài hàng nghìn từ."
    ),
    "lessons/cs115/L36_boosting.yaml": (
        "Trên dữ liệu dạng bảng có kích thước vừa phải, các biến thể tăng cường gradient hiện đại thường cho độ chính xác vượt trội so với mạng nơ-ron nhiều lớp, miễn là bạn kiểm soát chặt chiều sâu từng cây con và số vòng lặp nối tiếp. Hãy nhớ đừng bao giờ so sánh mù mà luôn chạy kiểm chứng chéo trên cùng cách chia dữ liệu để thấy rõ lợi ích thật."
    ),
    "lessons/cs115/L37_autoencoder.yaml": (
        "Ngoài nén chiều, chuẩn hoá tốt không gian cổ chai còn giúp loại bỏ nhiễu ngẫu nhiên vì mô hình buộc phải giữ lại quy luật chung thay vì từng hạt nhiễu rời rạc. Hãy bắt đầu đo sai số trên tập kiểm định để tìm chiều cổ chai nhỏ nhất mà chất lượng tái tạo vẫn chấp nhận được."
    ),
    "lessons/cs115/L40_umap.yaml": (
        "Từ mặt phẳng trực quan thu được, hãy luôn quay lại kiểm tra chỉ số lân cận trên chính dữ liệu gốc nhiều chiều trước khi ra quyết định phân nhóm khách hàng hay phân tích dữ liệu sinh học. Kết hợp cả trực quan nhanh lẫn thước đo định lượng trên không gian gốc sẽ giữ cho phân tích của bạn vừa rõ ràng vừa khách quan. Tương tự t-SNE của bài 32, hãy chú ý điều chỉnh số láng giềng k khi muốn cân bằng giữa chi tiết cục bộ với cấu trúc liên kết vừa phải của toàn tập dữ liệu lớn."
    ),
    "lessons/cs115/L41_attention.yaml": (
        "Hiểu sâu phép nhân truy vấn khoá và chia căn số chiều hôm nay là chìa khoá trực tiếp để bạn đọc hiểu mọi mô hình ngôn ngữ lớn hiện đại."
    ),
    "lessons/cs115/L43_diffusion.yaml": (
        "Ngoài sinh ảnh nghệ thuật, khung mô hình khuếch tán thêm và khử nhiễu này còn mở rộng rất mạnh sang thiết kế phân tử thuốc mới, tạo âm thanh độ phân giải cao và mô phỏng chuỗi chuyển động ba chiều chân thực. Dù tốc độ sinh chậm do phải lặp nhiều bước giải mã, nhiều phương pháp lấy mẫu gia tốc gần đây đã rút ngắn xuống chỉ còn vài chục bước mà vẫn giữ chất lượng ảnh sắc nét. Hãy tự tay chạy bài thực hành lịch nhiễu tuyến tính hôm nay để cảm nhận trọn vẹn đường đi toán học tuyệt đẹp của cả khoá học."
    ),
}

for rel, extra in EXTRAS.items():
    append_recap0(rel, extra)

# Verify ALL 22 L22..L43 lessons cleanly
for i in range(22, 44):
    lid = f"L{i:02d}"
    fp = sorted((ROOT / "lessons" / "cs115").glob(f"{lid}_*.yaml"))[0]
    sp = lv.load_spec(fp)
    w = sum(len((st.get("say") or "").split()) for sc in sp["scenes"] for st in sc["steps"])
    for sc in sp["scenes"]:
        for idx, st in enumerate(sc["steps"]):
            say = st.get("say") or ""
            foc = st.get("focus")
            sents = lv.sentences(say)
            if foc is not None:
                assert len(foc) == len(sents), f"{lid}:{sc['id']}#{idx} focus={len(foc)} != sents={len(sents)}"
            for s in sents:
                assert len(s) <= 170, f"{lid}:{sc['id']}#{idx} sent >170 ({len(s)}): {s}"
                assert len(s.split()) <= 38, f"{lid}:{sc['id']}#{idx} sent >38 ({len(s.split())}): {s}"
                assert "càng " not in s.lower(), f"{lid}:{sc['id']}#{idx} 'càng ': {s}"
                assert not re.search(r"[$_^]", s), f"{lid}:{sc['id']}#{idx} TeX in say: {s}"
    assert w >= 1645, f"CS115:{lid} words={w} < 1645"
    print(f"OK {lid}: words={w}", flush=True)
print("ALL 22 CS115 STAGE 9 LESSONS >= 1645w & CLEAN!", flush=True)
