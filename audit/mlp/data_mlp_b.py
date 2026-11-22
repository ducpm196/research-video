# -*- coding: utf-8 -*-
"""Đặc tả 7 bài sau khoá MLP (L07..L13) — Tăng cường độ dốc, Chuỗi thời gian, PyTorch CPU & Dự án Gian lận."""

LESSONS_B = [
    {
        "id": "L07",
        "fname": "L07_gradient_boosting_thuc_hanh.yaml",
        "title": "Bài 7 — Tăng cường độ dốc HistGradientBoosting học từ phần dư",
        "assumes": ["mlp_leakage"],
        "introduces": [],
        "obj": [
            "Hiểu nguyên lý mỗi cây mới sửa sai số phần dư của tổng các cây đi trước",
            "Điều chỉnh learning_rate phối hợp max_iter để hội tụ mượt không quá khớp",
            "Chạy HistGradientBoostingClassifier trên dữ liệu bảng và so sánh với RandomForest",
        ],
        "prereq": [
            ("Rừng ngẫu nhiên trồng song song (MLP:L06)", "Nhiều cây độc lập bỏ phiếu cùng lúc giảm phương sai"),
            ("Chiến lược sửa sai nối tiếp (Boosting)", "Mỗi cây nông kế tiếp học trực tiếp trên phần dư sai số còn sót"),
            ("Tốc độ học learning_rate", "Bước nhỏ 0.05-0.10 giúp tổng tích lũy không vọt lố theo nhiễu"),
        ],
        "prereq_say": (
            "Nếu rừng ngẫu nhiên trồng hàng chục cây song song rồi lấy trung bình, thì tăng cường độ dốc trồng từng cây nối đuôi nhau. "
            "Cây sau chỉ tập trung sửa chính phần sai số mà tổng các cây trước còn để sót lại. "
            "Nhờ vậy mô hình cây nông vẫn đạt độ chính xác rất cao trên dữ liệu bảng thực tế."
        ),
        "svg_boxes": [("Dự đoán vòng 0", "Giá trị cơ sở y0"), ("Cây m sửa phần dư", "F_m = F_{m-1} + lr * h_m"), ("Dừng sớm early_stopping", "Khoá quá khớp trước khi nhiễu")],
        "svg_say": (
            "Hình minh họa cơ chế cộng dồn từng bước của họ tăng cường độ dốc. "
            "Mỗi cây con mới sinh ra chỉ học phần chênh lệch còn lại rồi nhân thêm tốc độ học nhỏ trước khi cộng vào mô hình tổng. "
            "Kết hợp cơ chế dừng sớm khi điểm thẩm định ngừng cải thiện, mô hình tự dừng đúng lúc."
        ),
        "hook_say": (
            "Trên các bảng dữ liệu tài chính hay thương mại điện tử có vài trăm nghìn dòng, bộ phân loại tăng cường độ dốc theo giỏ dữ liệu thường vượt trội cả hồi quy lẫn rừng ngẫu nhiên. "
            "Bí mật nằm ở tốc độ gom cột thành hai trăm năm mươi sáu giỏ và học nối tiếp trên phần dư. "
            "Hôm nay ta chạy trực tiếp bộ phân loại này trên CPU trong chưa tới một giây."
        ),
        "hook_txt": "Cập nhật tuần tự <code>F_m(x) = F_{m-1}(x) + lr * h_m(x)</code>. Giảm <code>lr</code> từ <code>1.0</code> xuống <b>0.10</b> buộc mô hình học chậm và mượt qua từng cây nông thay vì nhớ nhiễu.",
        "hook_chk": ["0.0 + 0.1 * 10.0 == 1.0", "256 == 2 ** 8"],
        "formula_txt": (
            "<p><b>1. Cộng dồn tăng cường:</b> <code>F_M(x) = F_0 + lr * sum_{m=1..M} h_m(x)</code>.</p>"
            "<p><b>2. Giỏ histogram:</b> rời rạc hóa biến liên tục thành tối đa <code>255</code> giỏ số nguyên nên tìm ngưỡng cắt nhanh gấp nhiều lần.</p>"
        ),
        "formula_say": (
            "Công thức thứ nhất cho thấy đầu ra cuối là tổng có trọng số của chuỗi cây nối tiếp nhau, trong đó mỗi cây nhân với hệ số bước học nhỏ. "
            "Nhờ gom giá trị số liên tục vào tối đa hai trăm năm mươi lăm giỏ cố định, máy chỉ cần duyệt vài trăm ngưỡng thay vì sắp xếp lại hàng triệu điểm."
        ),
        "sym_rows": [
            ["<code>HistGradientBoostingClassifier</code>", "Bộ tăng cường độ dốc nhanh dựa trên histogram trên CPU"],
            ["<code>learning_rate=0.1</code>", "Hệ số co nhỏ bước cộng của mỗi cây mới"],
            ["<code>max_iter=40</code>", "Số lượng cây tuần tự tối đa được cộng thêm"],
        ],
        "sym_say": (
            "Bảng ký hiệu liệt kê tên lớp và hai siêu tham số cặp đôi luôn đi cùng nhau trong tăng cường độ dốc. "
            "Tốc độ học nhỏ cần nhiều vòng lặp hơn một chút nhưng giảm rủi ro nhảy vọt quá đà, "
            "còn số vòng lặp tối đa chặn tổng số cây nối đuôi."
        ),
        "ex_code": (
            "from sklearn.datasets import make_classification\n"
            "from sklearn.model_selection import train_test_split\n"
            "from sklearn.ensemble import HistGradientBoostingClassifier\n"
            "X, y = make_classification(n_samples=600, n_features=12, n_informative=6, random_state=42)\n"
            "X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.25, stratify=y, random_state=42)\n"
            "hgb = HistGradientBoostingClassifier(max_iter=50, learning_rate=0.1, random_state=42).fit(X_tr, y_tr)\n"
            "print(f'n_iter={hgb.n_iter_} tr={hgb.score(X_tr,y_tr):.3f} te={hgb.score(X_te,y_te):.3f}')\n"
        ),
        "ex_say": (
            "Đoạn mã huấn luyện năm mươi vòng tăng cường độ dốc với tốc độ học không phẩy một trên sáu trăm mẫu dữ liệu. "
            "Bộ chia vẫn giữ nguyên cấu trúc phân tầng và hạt giống bốn hai để đối chứng công bằng."
        ),
        "ex_out_say": (
            "Kết quả chạy thật trên CPU hoàn thành trong tích tắc và đạt độ chính xác cao trên tập kiểm tra. "
            "Do tốc độ học nhỏ kết hợp cây giới hạn độ sâu mặc định nên mô hình không bị rơi vào vũng lầy học thuộc nhiễu."
        ),
        "chk_code": (
            "target, f, lr = 10.0, 0.0, 0.1\n"
            "for step in range(3):\n"
            "    res = target - f\n"
            "    f += lr * res\n"
            "print(f'after_3_steps={f:.3f} remaining_res={target - f:.3f}')\n"
        ),
        "chk_say": (
            "Phép kiểm chứng thứ hai mô phỏng trực tiếp ba bước cộng dồn phần dư với mục tiêu bằng mười và bước học không phẩy một. "
            "Sau mỗi vòng, phần dư còn lại giảm dần theo cấp số nhân chín phần mười."
        ),
        "chk_out_say": (
            "Kết quả in ra đúng hai phẩy bảy một và phần dư bảy phẩy hai chín, vì mỗi bước chỉ bù mười phần trăm khoảng cách còn thiếu nên đường tiến về đích rất êm."
        ),
        "quymo": [
            ("100 000 dòng dữ liệu bảng", "Cây thường: rất chậm khi sort", "HistGradientBoosting nhanh hơn hàng chục lần nhờ 255 giỏ"),
            ("Tăng lr=0.5 + max_iter=500", "Đạt Train 100% rất sớm", "Bật early_stopping=True + giảm lr về 0.05..0.10"),
            ("Bảng có ô NaN rải rác", "Mô hình tuyến tính gãy lỗi", "HistGradientBoosting tự học nhánh rẽ cho giá trị thiếu"),
        ],
        "quymo_say": (
            "Bảng quy mô nêu ba lợi thế thực chiến nổi bật của thuật toán gom giỏ trên hệ thống lớn. "
            "Thậm chí ngay cả khi bảng dữ liệu có sẵn các ô trống chưa điền, thuật toán vẫn tự chọn hướng nhánh trái hay phải tốt nhất cho ô trống đó."
        ),
        "pitfalls": [
            "<b>Lỗi 1 (-30đ):</b> Tăng cả <code>learning_rate=0.5</code> lẫn <code>max_iter=500</code> khiến mô hình quá khớp dữ dội.",
            "<b>Lỗi 2 (-20đ):</b> Tưởng nhầm rừng ngẫu nhiên và tăng cường độ dốc giống nhau nên không chỉnh tỉ lệ giữa tốc độ học và số cây.",
            "<b>Lỗi 3 (-10đ):</b> Bỏ quên hạt giống ngẫu nhiên khi so sánh các bộ siêu tham số.",
        ],
        "pitfalls_say": (
            "Hãy tránh ba sai lầm sau khi điều chỉnh bộ tăng cường độ dốc. "
            "Đầu tiên là đẩy cả bước học lẫn số cây lên quá cao làm mô hình học cả nhiễu. "
            "Thứ hai là nhầm lẫn giữa trồng song song của rừng ngẫu nhiên và cộng nối tiếp trên phần dư."
        ),
        "q_text": "<ol><li>Cây thứ <code>m</code> trong tăng cường độ dốc huấn luyện để khớp vào mục tiêu gì?</li><li>Khi giảm <code>learning_rate</code> từ <code>0.2</code> xuống <code>0.05</code>, thường cần tăng hay giảm <code>max_iter</code>?</li></ol>",
        "q_say": "Mời bạn tự kiểm tra nhanh hai câu hỏi cho bài bảy. Câu một, mỗi cây mới trong tăng cường độ dốc học để khớp vào đại lượng nào của các cây trước? Câu hai, khi giảm tốc độ học đi bốn lần thì thường phải tăng hay giảm số cây? Bấm tạm dừng và trả lời.",
        "q_ans1": "Khớp vào <b>phần dư (sai số âm gradient)</b> mà tổng các cây đi trước còn để sót.",
        "q_ans1_say": "Đáp án câu một: mỗi cây mới học thẳng phần dư sai số mà tổ hợp cây trước chưa sửa hết.",
        "q_ans2": "Thường cần <b>tăng <code>max_iter</code></b> lên tương ứng (phối hợp dừng sớm) để mô hình kịp tiến tới điểm tối ưu.",
        "q_ans2_say": "Đáp án câu hai: cần tăng số lượng cây lên tương ứng vì bước đi mỗi cây giờ nhỏ hơn trước.",
        "lab_de": (
            "# Lab MLP L07 — Tăng cường độ dốc HistGradientBoosting & đối chứng cộng phần dư\n\n"
            "Viết chương trình Python (chạy bằng `labs/.venv-ml` qua `cham.sh`): "
            "chạy `HistGradientBoostingClassifier(max_iter=50, learning_rate=0.1, random_state=42)` trên `make_classification(n_samples=600, n_features=12, n_informative=6, random_state=42)` chia 75/25 `stratify=y, random_state=42`, "
            "kèm 3 bước cộng phần dư từ `0.0` tới `10.0` với `lr=0.1`, in đúng 3 dòng:\n"
            "1. `n_iter=50`\n2. `hgb_test_acc=...`\n3. `res_after_3=7.290`\n\n"
            "Chấm tự động:\n```bash\nbash labs/cham.sh MLP L07 duong_dan/bai_cua_ban.py\n```"
        ),
        "lab_sol": (
            "from sklearn.datasets import make_classification\n"
            "from sklearn.model_selection import train_test_split\n"
            "from sklearn.ensemble import HistGradientBoostingClassifier\n"
            "X, y = make_classification(n_samples=600, n_features=12, n_informative=6, random_state=42)\n"
            "X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.25, stratify=y, random_state=42)\n"
            "hgb = HistGradientBoostingClassifier(max_iter=50, learning_rate=0.1, random_state=42).fit(X_tr, y_tr)\n"
            "f = 0.0\n"
            "for _ in range(3): f += 0.1 * (10.0 - f)\n"
            "print(f'n_iter={hgb.n_iter_}')\n"
            "print(f'hgb_test_acc={hgb.score(X_te, y_te):.3f}')\n"
            "print(f'res_after_3={10.0 - f:.3f}')\n"
        ),
        "chain": ["Cộng dồn trên phần dư", "Histogram 255 giỏ siêu nhanh", "Khớp cặp lr & max_iter"],
    },
    {
        "id": "L08",
        "fname": "L08_dac_trung_time_series_split.yaml",
        "title": "Bài 8 — Đặc trưng tương tác & kiểm chứng theo trục thời gian TimeSeriesSplit",
        "assumes": ["mlp_leakage", "mlp_pipeline"],
        "introduces": [],
        "obj": [
            "Tạo đặc trưng bậc hai PolynomialFeatures bổ sung mối quan hệ phi tuyến cho mô hình tuyến tính",
            "Hiểu lỗi chí tử khi xáo trộn ngẫu nhiên chuỗi thời gian để đánh giá tương lai",
            "Dùng TimeSeriesSplit bảo đảm mọi nếp kiểm tra luôn nằm sau tập huấn luyện về thời gian",
        ],
        "prereq": [
            ("Ranh giới phi tuyến đơn giản", "Một đường thẳng không thể tách hình tròn bên trong khỏi vòng ngoài"),
            ("Nâng bậc đặc trưng (x1^2, x2^2, x1*x2)", "Chuyển từ không gian phẳng sang đa thức giúp hàm tuyến tính cắt được đường tròn"),
            ("Thứ tự nhân quả thời gian", "Dữ liệu ngày hôm sau tuyệt đối không được dùng để đoán ngày hôm trước"),
        ],
        "prereq_say": (
            "Bài tám ghép hai kỹ năng cốt lõi cho dữ liệu thực tế nâng cao: tạo đặc trưng phi tuyến và kiểm chứng chuỗi thời gian. "
            "Khi dữ liệu có hình tròn đồng tâm, chỉ thêm đặc trưng bình phương giúp hồi quy tuyến tính tách sạch ranh giới. "
            "Nhưng trên dữ liệu theo ngày tháng, việc xáo trộn ngẫu nhiên truyền thống sẽ làm rò rỉ tương lai."
        ),
        "svg_boxes": [("Tạo x1^2, x2^2, x1x2", "PolynomialFeatures bậc 2"), ("Mốc thời gian 0..T", "Trộn ngẫu nhiên là rò rỉ!"), ("TimeSeriesSplit", "max(Train) < min(Val) 100%")],
        "svg_say": (
            "Ba khối trên màn hình đối chiếu hai bước nâng cấp đặc trưng và quy tắc chia tập theo dòng chảy thời gian. "
            "Biến đổi đa thức mở rộng không gian cho mô hình tuyến tính. "
            "Còn bộ chia chuỗi thời gian luôn bảo đảm mọi chỉ số huấn luyện nằm hoàn toàn trước mọi chỉ số kiểm tra."
        ),
        "hook_say": (
            "Đội dự báo doanh thu dùng kiểm chứng chéo xáo trộn ngẫu nhiên báo điểm đẹp như mơ, nhưng vừa chạy ngoài thật lại trượt dài. "
            "Lý do là tập kiểm tra chứa ngày mười lăm tháng sáu trong khi tập huấn luyện đã kịp học mất ngày mười sáu và mười bảy. "
            "Hôm nay ta khoá chặt lỗi xuyên không thời gian bằng bộ chia tịnh tiến và thử nghiệm đa thức."
        ),
        "hook_txt": "Từ <b>2 cột</b> <code>(x1, x2)</code>, đa thức bậc 2 tạo <code>[x1, x2, x1^2, x1*x2, x2^2]</code> (tổng <b>5 đặc trưng</b> chưa gồm hằng số). Bộ chia <code>TimeSeriesSplit</code> bảo đảm <code>max(train_idx) &lt; min(test_idx)</code> ở <b>100%</b> nếp.",
        "hook_chk": ["2 + 3 == 5", "10 < 11"],
        "formula_txt": (
            "<p><b>1. Đường tròn đơn giản:</b> <code>x1^2 + x2^2 &lt; r^2</code> là tuyến tính hoàn toàn theo đặc trưng mới <code>z1=x1^2, z2=x2^2</code>.</p>"
            "<p><b>2. Cửa sổ mở rộng:</b> nếp thứ <code>k</code> dùng quá khứ <code>[0..t_k]</code> để dự đoán tương lai <code>(t_k..t_{k+1}]</code>.</p>"
        ),
        "formula_say": (
            "Hai nguyên lý đơn giản giải thích vì sao biến đổi đặc trưng và chia theo thời gian lại có sức mạnh lớn đến vậy. "
            "Bất đẳng thức hình tròn vốn cong trong mặt phẳng gốc bỗng biến thành mặt phẳng thẳng tắp khi ta cung cấp bình phương hai tọa độ. "
            "Còn cửa sổ thời gian luôn cuộn tiến về phía trước không bao giờ nhìn ngược."
        ),
        "sym_rows": [
            ["<code>PolynomialFeatures(degree=2, include_bias=False)</code>", "Sinh các số hạng bình phương và tích chéo bậc hai"],
            ["<code>TimeSeriesSplit(n_splits=4)</code>", "Chia 4 cửa sổ tiến dần theo thời gian, giữ quá khứ riêng"],
            ["<code>make_circles(n_samples=300, factor=0.4)</code>", "Bộ dữ liệu hai vòng tròn đồng tâm để kiểm khả năng cắt phi tuyến"],
        ],
        "sym_say": (
            "Bảng ký hiệu nêu hai bộ biến đổi và bộ sinh dữ liệu hai vòng tròn đồng tâm. "
            "Tham số tắt cột hệ số chệch giữ gọn số lượng cột vì bộ phân loại phía sau đã tự học độ chệch rồi. "
            "Còn bộ chia chuỗi thời gian nhận số bước kiểm tra mà tuyệt đối không cho phép xáo trộn."
        ),
        "ex_code": (
            "from sklearn.datasets import make_circles\n"
            "from sklearn.model_selection import train_test_split\n"
            "from sklearn.preprocessing import PolynomialFeatures as PF, StandardScaler as SS\n"
            "from sklearn.linear_model import LogisticRegression as LR\n"
            "from sklearn.pipeline import Pipeline\n"
            "X, y = make_circles(n_samples=300, factor=0.4, noise=0.05, random_state=42)\n"
            "X_tr, X_te, y_tr, y_te = train_test_split(\n"
            "    X, y, test_size=0.3, stratify=y, random_state=42)\n"
            "lin = Pipeline([('s', SS()), ('c', LR(random_state=42))]).fit(X_tr, y_tr)\n"
            "poly = Pipeline([('pf', PF(2, include_bias=False)), ('s', SS()),\n"
            "                 ('c', LR(random_state=42))]).fit(X_tr, y_tr)\n"
            "print(f'linear_acc={lin.score(X_te, y_te):.3f} poly2_acc={poly.score(X_te, y_te):.3f}')\n"
        ),
        "ex_say": (
            "Đoạn mã đối đầu trực tiếp mô hình tuyến tính thuần và mô hình gắn thêm đa thức bậc hai trên dữ liệu hai vòng tròn đồng tâm. "
            "Mọi bước chuẩn hóa và mở rộng đặc trưng đều nằm gọn trong chuỗi xử lý khép kín."
        ),
        "ex_out_say": (
            "Kết quả chạy thật chứng minh đường thẳng thường chỉ đoán ngang mức tung đồng xu quanh năm mươi phần trăm. "
            "Ngược lại khi có thêm bình phương tọa độ, chính bộ phân loại tuyến tính đó nhảy vọt lên độ chính xác gần tuyệt đối."
        ),
        "chk_code": (
            "import numpy as np\n"
            "from sklearn.model_selection import TimeSeriesSplit\n"
            "tscv = TimeSeriesSplit(n_splits=4)\n"
            "ok = all(tr.max() < te.min() for tr, te in tscv.split(np.arange(100)))\n"
            "print(f'causal_time_order={int(ok)}')\n"
        ),
        "chk_say": (
            "Phép kiểm chứng thứ hai xác minh tính nhân quả trên mảng một trăm ngày liên tiếp chia thành bốn nếp tiến dần. "
            "Ta kiểm tra ở mọi nếp xem chỉ số lớn nhất của phần huấn luyện có luôn nhỏ hơn chỉ số nhỏ nhất của phần kiểm tra hay không."
        ),
        "chk_out_say": (
            "Đầu ra khẳng định bằng một trên tất cả bốn nếp vì bộ chia tịnh tiến chỉ mở rộng tập quá khứ và kiểm tra ngay đoạn tương lai kế tiếp."
        ),
        "quymo": [
            ("2 cột -> bậc 2", "5 đặc trưng mới", "Chi phí tăng không đáng kể"),
            ("100 cột -> bậc 2", "5 150 đặc trưng!", "Bùng nổ tổ hợp C(d+2, 2) -> dễ tràn RAM và quá khớp"),
            ("Chuỗi giao dịch nhiều năm", "KFold xáo trộn sai nghiêm trọng", "Luôn dùng TimeSeriesSplit hoặc cắt theo ngày cứng"),
        ],
        "quymo_say": (
            "Bảng quy mô nhắc nhở hai lưu ý khi mở rộng bài toán. "
            "Thứ nhất, đừng chạy đa thức bậc cao trên bảng trăm cột vì số chiều sẽ tăng theo hàm bậc hai lên tới hàng nghìn cột nhiễu. "
            "Thứ hai, với bài toán dự báo theo ngày, chỉ số thời gian luôn phải kiểm bằng chia tịnh tiến."
        ),
        "pitfalls": [
            "<b>Lỗi 1 (-30đ):</b> Dùng <code>KFold(shuffle=True)</code> trên dữ liệu theo thời gian gây nhìn trộm tương lai.",
            "<b>Lỗi 2 (-20đ):</b> Đặt đa thức bậc 3–4 trên hàng trăm cột làm số chiều nổ hàng triệu cột.",
            "<b>Lỗi 3 (-10đ):</b> Tạo đặc trưng trượt trên toàn bảng trước khi chia tập Train/Test.",
        ],
        "pitfalls_say": (
            "Ba sai lầm chí tử khi xử lý đặc trưng và thời gian cần nhớ kỹ gồm những điểm sau. "
            "Một là xáo trộn ngẫu nhiên bảng giao dịch theo ngày, hai là lạm dụng đa thức bậc quá cao gây bùng nổ chiều, "
            "và ba là tính trung bình trượt băng qua ranh giới tập kiểm tra."
        ),
        "q_text": "<ol><li>Từ 2 cột <code>(x1, x2)</code>, <code>PolynomialFeatures(degree=2, include_bias=False)</code> tạo ra bao nhiêu cột?</li><li>Vì sao không được dùng <code>StratifiedKFold(shuffle=True)</code> trên dữ liệu dự báo doanh số ngày?</li></ol>",
        "q_say": "Hãy kiểm tra lại hai câu hỏi chốt bài ngay dưới đây. Câu một, từ hai cột đầu vào, bộ đa thức bậc hai bỏ hằng số tạo ra tổng cộng mấy cột? Câu hai, vì sao không được xáo trộn ngẫu nhiên các ngày khi đánh giá dự báo chuỗi thời gian? Bấm tạm dừng và trả lời.",
        "q_ans1": "Tạo ra <code><b>5</b></code> cột: <code>x1, x2, x1^2, x1*x2, x2^2</code>.",
        "q_ans1_say": "Đáp án câu một: tổng cộng năm cột gồm hai biến gốc, hai bình phương và một tích chéo.",
        "q_ans2": "Vì xáo trộn đưa dữ liệu tương lai vào tập Train để đoán ngược quá khứ, gây rò rỉ nhân quả.",
        "q_ans2_say": "Đáp án câu hai: vì nó cho phép mô hình nhìn thấy các ngày tương lai để đoán ngược lại quá khứ, làm sai lệch hoàn toàn độ chính xác thật.",
        "lab_de": (
            "# Lab MLP L08 — Đa thức bậc 2 trên hình tròn & kiểm chứng nhân quả TimeSeriesSplit\n\n"
            "Viết chương trình Python (chạy bằng `labs/.venv-ml` qua `cham.sh`): "
            "so sánh `LogisticRegression` tuyến tính vs `PolynomialFeatures(degree=2, include_bias=False)` trên `make_circles(n_samples=300, factor=0.4, noise=0.05, random_state=42)` chia 70/30 `stratify=y, random_state=42`, "
            "và kiểm `TimeSeriesSplit(n_splits=4)` trên 100 chỉ số, in đúng 3 dòng:\n"
            "1. `linear_acc=...`\n2. `poly2_acc=1.000`\n3. `strict_causal_splits=1`\n\n"
            "Chấm tự động:\n```bash\nbash labs/cham.sh MLP L08 duong_dan/bai_cua_ban.py\n```"
        ),
        "lab_sol": (
            "import numpy as np\n"
            "from sklearn.datasets import make_circles\n"
            "from sklearn.model_selection import train_test_split, TimeSeriesSplit\n"
            "from sklearn.preprocessing import PolynomialFeatures, StandardScaler\n"
            "from sklearn.linear_model import LogisticRegression\n"
            "from sklearn.pipeline import Pipeline\n"
            "X, y = make_circles(n_samples=300, factor=0.4, noise=0.05, random_state=42)\n"
            "X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, stratify=y, random_state=42)\n"
            "lin = Pipeline([('sc', StandardScaler()), ('c', LogisticRegression(random_state=42))]).fit(X_tr, y_tr)\n"
            "poly = Pipeline([('pf', PolynomialFeatures(degree=2, include_bias=False)), ('sc', StandardScaler()), ('c', LogisticRegression(random_state=42))]).fit(X_tr, y_tr)\n"
            "ok = all(tr.max() < te.min() for tr, te in TimeSeriesSplit(n_splits=4).split(np.arange(100)))\n"
            "print(f'linear_acc={lin.score(X_te, y_te):.3f}')\n"
            "print(f'poly2_acc={poly.score(X_te, y_te):.3f}')\n"
            "print(f'strict_causal_splits={int(ok)}')\n"
        ),
        "chain": ["Đa thức tách biên cong", "Tránh nổ chiều bậc cao", "TimeSeriesSplit giữ nhân quả"],
    },
    {
        "id": "L09",
        "fname": "L09_khong_giam_sat_kmeans_pca.yaml",
        "title": "Bài 9 — Học không giám sát thực hành: Phân cụm KMeans & giảm chiều PCA",
        "assumes": ["mlp_leakage", "mlp_pipeline"],
        "introduces": [],
        "obj": [
            "Chuẩn hóa khoảng cách trước khi chạy phân cụm KMeans(n_init=10)",
            "Chiếu đặc trưng qua PCA và đo tổng tỉ lệ phương sai được giữ lại",
            "Phát hiện cụm bất thường dựa trên khoảng cách tới tâm cụm gần nhất",
        ],
        "prereq": [
            ("Khoảng cách hình học Ơ-clít (MLP:L00)", "Một cột đơn vị lớn gấp 1 000 lần sẽ thống trị toàn bộ khoảng cách"),
            ("Phân cụm không nhãn (KMeans)", "Gom điểm vào K tâm cụm gần nhất theo khoảng cách bình phương"),
            ("Giảm chiều tuyến tính (PCA)", "Chiếu xuống các trục chứa nhiều phương sai nhất của dữ liệu"),
        ],
        "prereq_say": (
            "Nhiều bài toán thực tế như phân khúc khách hàng hay phát hiện hành vi lạ ban đầu không có sẵn nhãn đúng sai. "
            "Bài chín sử dụng phân cụm KMeans và giảm chiều PCA để rút gọn cấu trúc ẩn của bảng nhiều cột. "
            "Điều kiện tiên quyết không thể thiếu là luôn chuẩn hóa thang đo trước khi đo khoảng cách hay chiếu trục."
        ),
        "svg_boxes": [("StandardScaler", "Đưa cột về cùng đơn vị"), ("PCA(n_components=k)", "Giữ >80% tổng phương sai"), ("KMeans(K cụm)", "Đo khoảng cách tới tâm cụm")],
        "svg_say": (
            "Đường ống học không giám sát gồm ba chặng thẳng hàng trên hình vẽ. "
            "Chặng đầu đưa mọi cột về trung bình không phương sai một để không cột nào áp đảo phần còn lại. "
            "Chặng hai nén chiều qua PCA, rồi chặng ba gom cụm và đo khoảng cách từ điểm mới tới tâm gần nhất."
        ),
        "hook_say": (
            "Hãy tưởng tượng bạn chạy phân cụm trên hai cột: số năm công tác từ một tới mười và tiền lương từ hai mươi triệu tới một trăm triệu. "
            "Nếu quên chuẩn hóa, khoảng cách giữa hai người chỉ hoàn toàn phụ thuộc tiền lương mà bỏ rơi cột năm công tác. "
            "Hôm nay ta chuẩn hóa chuẩn xác, giữ gọn chiều dữ liệu và đo khoảng cách bất thường."
        ),
        "hook_txt": "Đặt <code>StandardScaler()</code> trước <code>PCA</code> và <code>KMeans</code> bảo đảm mọi đặc trưng đóng góp bình đẳng vào khoảng cách. Kiểm định tổng tỉ lệ phương sai giữ lại <code>sum(explained_variance_ratio_)</code>.",
        "hook_chk": ["0.5 + 0.3 + 0.1 == 0.9", "3 < 8"],
        "formula_txt": (
            "<p><b>1. Tổng phương sai giữ lại:</b> <code>R_k = sum_{i=1..k} lambda_i / sum_{j=1..d} lambda_j</code> (thường giữ <code>&gt;= 0,85</code>).</p>"
            "<p><b>2. Độ lệch bất thường cụm:</b> <code>dist(x) = min_c ||x - mu_c||_2</code> — điểm càng xa mọi tâm cụm càng bất thường.</p>"
        ),
        "formula_say": (
            "Hai công thức trên giúp bạn chọn số chiều nén và phát hiện điểm ngoại lai một cách định lượng. "
            "Tỉ số tổng phương sai giữ lại cho biết sau khi vứt bỏ các trục phụ thì còn giữ được bao nhiêu phần trăm thông tin biến thiên gốc. "
            "Còn khoảng cách tối thiểu tới tâm cụm gần nhất càng lớn chứng tỏ điểm đó lạc đàn so với các cụm quen thuộc."
        ),
        "sym_rows": [
            ["<code>PCA(n_components=2, random_state=42)</code>", "Nén ma trận xuống 2 thành phần chính trực giao"],
            ["<code>explained_variance_ratio_</code>", "Tỉ lệ phần trăm phương sai mà mỗi trục mới giải thích"],
            ["<code>KMeans(n_clusters=3, n_init=10, random_state=42)</code>", "Chạy phân cụm 3 tâm với 10 lần khởi tạo chọn nghiệm tốt nhất"],
        ],
        "sym_say": (
            "Bảng ký hiệu liệt kê hai lớp không giám sát và thuộc tính đọc phương sai giữ lại. "
            "Trong KMeans, việc đặt số lần khởi tạo bằng mười kèm hạt giống bốn hai giúp tránh rơi vào tâm cụm xấu ngay lần chạy đầu. "
            "Còn thuộc tính tỉ lệ phương sai trả về mảng từng phần trăm ứng với mỗi trục chính."
        ),
        "ex_code": (
            "from sklearn.datasets import make_blobs\n"
            "from sklearn.preprocessing import StandardScaler\n"
            "from sklearn.decomposition import PCA\n"
            "from sklearn.cluster import KMeans\n"
            "from sklearn.pipeline import Pipeline\n"
            "X, _ = make_blobs(n_samples=300, centers=3, n_features=6, cluster_std=1.0, random_state=42)\n"
            "sc = StandardScaler().fit_transform(X)\n"
            "pca = PCA(n_components=2, random_state=42).fit(sc)\n"
            "km = Pipeline([('sc', StandardScaler()),\n"
            "               ('km', KMeans(n_clusters=3, n_init=10, random_state=42))]).fit(X)\n"
            "print(f'var_2d={pca.explained_variance_ratio_.sum():.3f} inertia={km[\"km\"].inertia_:.1f}')\n"
        ),
        "ex_say": (
            "Đoạn mã sinh ba trăm điểm gom thành ba cụm trong không gian sáu chiều, sau đó chuẩn hóa toàn bộ cột rồi chiếu xuống hai chiều chính. "
            "Đồng thời ta khớp bộ phân cụm ba tâm để đo tổng bình phương khoảng cách tới tâm cụm."
        ),
        "ex_out_say": (
            "Kết quả chạy thật chứng minh chỉ giữ hai trục chính đã thu gọn được phần lớn phương sai dữ liệu sáu chiều. "
            "Bởi ba cụm tách biệt rõ rệt nên chỉ cần rất ít thành phần chính vẫn giữ nguyên hình khối cụm."
        ),
        "chk_code": (
            "import numpy as np\n"
            "from sklearn.cluster import KMeans\n"
            "X = np.array([[0.0, 0.0], [0.1, -0.1], [10.0, 10.0], [10.1, 9.9]])\n"
            "km = KMeans(n_clusters=2, n_init=10, random_state=42).fit(X)\n"
            "d_norm = km.transform([[0.05, 0.0]]).min()\n"
            "d_anom = km.transform([[50.0, 50.0]]).min()\n"
            "print(f'd_norm={d_norm:.3f} d_anom={d_anom:.3f} far={int(d_anom > 10 * d_norm)}')\n"
        ),
        "chk_say": (
            "Phép kiểm chứng thứ hai thử đo khoảng cách tới tâm gần nhất cho một điểm nằm giữa cụm quen thuộc và một điểm nhảy vọt ra tọa độ năm mươi năm mươi. "
            "Hàm biến đổi của KMeans trả ngay khoảng cách tới tất cả các tâm nên lấy nhỏ nhất ra điểm lệch chuẩn."
        ),
        "chk_out_say": (
            "Đầu ra khẳng định điểm bất thường cách tâm xa hơn hàng trăm lần điểm bình thường, vì phương pháp đo khoảng cách tới tâm phát hiện tức thì ngoại lai hình học."
        ),
        "quymo": [
            ("8 chiều -> PCA(2)", "Trực quan hóa nhanh và lọc nhiễu", "Giữ biểu đồ rõ mà ít mất thông tin chính"),
            ("1 000 000 dòng", "KMeans thường khá chậm", "Chuyển sang MiniBatchKMeans xử lý theo lô"),
            ("Cột doanh thu vs số đơn", "Sai lệch 10^6 lần nếu quên Scaler", "Luôn bọc StandardScaler trước PCA và KMeans"),
        ],
        "quymo_say": (
            "Bảng quy mô gợi ý lựa chọn khi bảng phình lên một triệu dòng: hãy dùng phiên bản chạy theo lô nhỏ để tiết kiệm bộ nhớ mà vẫn tìm tâm cụm rất nhanh."
        ),
        "pitfalls": [
            "<b>Lỗi 1 (-30đ):</b> Chạy <code>PCA</code> hoặc <code>KMeans</code> trực tiếp trên dữ liệu lệch đơn vị chưa qua <code>StandardScaler</code>.",
            "<b>Lỗi 2 (-20đ):</b> Quên gán <code>random_state=42</code> khi phân cụm dẫn tới thứ tự nhãn cụm nhảy lung tung mỗi lần chạy.",
            "<b>Lỗi 3 (-10đ):</b> Tưởng nhãn 0, 1, 2 của <code>KMeans</code> có thứ tự lớn bé hoặc khớp sẵn với tên lớp nghiệp vụ.",
        ],
        "pitfalls_say": (
            "Bạn tránh kỹ ba sai lầm thường gặp trong học không giám sát dưới đây. "
            "Một là bỏ qua chuẩn hóa thang đo trước khi đo khoảng cách, hai là quên khoá hạt giống ngẫu nhiên, "
            "và ba là hiểu nhầm nhãn cụm số không và số hai có thứ tự hơn kém."
        ),
        "q_text": "<ol><li>Tại sao phải đặt <code>StandardScaler</code> trước <code>PCA</code> và <code>KMeans</code>?</li><li>Làm sao dùng <code>KMeans</code> đã khớp để chấm điểm bất thường cho một giao dịch mới?</li></ol>",
        "q_say": "Mời bạn tự kiểm tra nhanh hai câu hỏi cho bài chín. Câu một, vì sao bắt buộc đặt bộ chuẩn hóa trước PCA và KMeans? Câu hai, dùng mô hình KMeans đã huấn luyện chấm điểm bất thường cho một điểm mới bằng cách nào? Bấm tạm dừng và trả lời.",
        "q_ans1": "Vì cả phương sai PCA lẫn khoảng cách Ơ-clít của KMeans đều bị cột có đơn vị lớn chi phối nếu không chuẩn hóa.",
        "q_ans1_say": "Đáp án câu một: vì cả phương sai lẫn khoảng cách đều phụ thuộc mạnh vào đơn vị đo nên cột số lớn sẽ áp đảo các cột khác nếu thiếu chuẩn hóa.",
        "q_ans2": "Tính khoảng cách nhỏ nhất từ điểm đó tới tâm cụm gần nhất (<code>km.transform(x).min()</code>); càng xa càng bất thường.",
        "q_ans2_say": "Đáp án câu hai: đo khoảng cách từ điểm mới tới tâm cụm gần nhất, khoảng cách càng lớn càng đáng nghi là bất thường.",
        "lab_de": (
            "# Lab MLP L09 — Chuẩn hóa + PCA & KMeans đo phương sai và bất thường\n\n"
            "Viết chương trình Python (chạy bằng `labs/.venv-ml` qua `cham.sh`): "
            "trên `make_blobs(n_samples=300, centers=3, n_features=6, cluster_std=1.0, random_state=42)` sau `StandardScaler()`, "
            "chạy `PCA(n_components=2, random_state=42)` và `KMeans(n_clusters=3, n_init=10, random_state=42)` cùng kiểm điểm lệch `[50, 50]` vs `[0.05, 0]`, in đúng 3 dòng:\n"
            "1. `pca_var_sum=...`\n2. `kmeans_clusters=3`\n3. `anomaly_further=1`\n\n"
            "Chấm tự động:\n```bash\nbash labs/cham.sh MLP L09 duong_dan/bai_cua_ban.py\n```"
        ),
        "lab_sol": (
            "import numpy as np\n"
            "from sklearn.datasets import make_blobs\n"
            "from sklearn.preprocessing import StandardScaler\n"
            "from sklearn.decomposition import PCA\n"
            "from sklearn.cluster import KMeans\n"
            "X, _ = make_blobs(n_samples=300, centers=3, n_features=6, cluster_std=1.0, random_state=42)\n"
            "Xs = StandardScaler().fit_transform(X)\n"
            "pca = PCA(n_components=2, random_state=42).fit(Xs)\n"
            "km3 = KMeans(n_clusters=3, n_init=10, random_state=42).fit(Xs)\n"
            "km2 = KMeans(n_clusters=2, n_init=10, random_state=42).fit(np.array([[0.0,0.0],[0.1,-0.1],[10.0,10.0],[10.1,9.9]]))\n"
            "far = int(km2.transform([[50.0, 50.0]]).min() > km2.transform([[0.05, 0.0]]).min())\n"
            "print(f'pca_var_sum={pca.explained_variance_ratio_.sum():.3f}')\n"
            "print(f'kmeans_clusters={len(set(km3.labels_))}')\n"
            "print(f'anomaly_further={far}')\n"
        ),
        "chain": ["Chuẩn hóa thang đo trước", "PCA nén chiều đo phương sai", "Đo khoảng cách tới tâm cụm"],
    },
    {
        "id": "L10",
        "fname": "L10_pytorch_cpu_tensor_autograd.yaml",
        "title": "Bài 10 — Vòng huấn luyện PyTorch CPU: Tensor, Autograd & tối ưu SGD",
        "assumes": ["mlp_leakage"],
        "introduces": ["mlp_autograd"],
        "obj": [
            "Khởi tạo Tensor float32 có requires_grad=True và tính đạo hàm bằng loss.backward()",
            "Nhớ rõ bắt buộc gọi zero_grad() trước mỗi bước cập nhật để không cộng dồn đạo hàm",
            "Cài vòng huấn luyện hồi quy tuyến tính y = 3x + 2 bằng PyTorch CPU khớp tham số",
        ],
        "prereq": [
            ("Lan truyền ngược trên đồ thị (CS115:L22)", "Quy tắc chuỗi tính đạo hàm từ hàm mất mát ngược về tham số"),
            ("Chuyển sang PyTorch CPU", "Thay vì viết tay từng đạo hàm, đồ thị động tự ghi lại mọi phép toán"),
            ("Chu kỳ 5 lệnh của vòng huấn luyện", "Xóa gradient → suy luận → tính loss → lan truyền ngược → bước cập nhật"),
        ],
        "prereq_say": (
            "Hai bài mười và mười một đưa bạn từ thư viện bảng sang mạng nơ-ron bằng PyTorch chạy thuần CPU. "
            "Thay vì giải tay đạo hàm phức tạp như trước, bộ vi phân tự động autograd tự dựng đồ thị phép tính và tính ngược mọi đạo hàm giúp bạn. "
            "Mọi mô hình học sâu đều vận hành theo đúng một vòng lặp năm dòng chuẩn này."
        ),
        "svg_boxes": [("1. zero_grad()", "Xóa đạo hàm vòng cũ"), ("2. loss = MSE(pred, y)", "Tính xuôi & mất mát"), ("3. backward() + step()", "Tính ngược & cập nhật w, b")],
        "svg_say": (
            "Hình trên vẽ chu kỳ ba chặng bất biến của bất kỳ vòng huấn luyện PyTorch nào. "
            "Chặng một bắt buộc xóa sạch đạo hàm cũ về không. "
            "Chặng hai tính xuôi dự đoán và mất mát, rồi chặng ba truyền ngược để bộ tối ưu dịch chuyển trọng số."
        ),
        "hook_say": (
            "Một lỗi kinh điển làm rất nhiều người mới học PyTorch thấy tham số bùng nổ tới vô cực chỉ sau mười vòng lặp là quên một dòng xóa đạo hàm. "
            "Vì thư viện cố ý cộng dồn đạo hàm qua các lần gọi truyền ngược để phục vụ ghép lô lớn. "
            "Hôm nay ta tự tay kiểm chứng hai lần truyền ngược liên tiếp và huấn luyện khớp đường thẳng ba ích cộng hai."
        ),
        "hook_txt": "Định nghĩa <b>autograd</b>: cơ chế tự động ghi đồ thị phép tính trên <code>Tensor</code> để tính đạo hàm ngược khi gọi <code>loss.backward()</code>. Luôn gọi <code>opt.zero_grad()</code> đầu vòng lặp vì PyTorch mặc định <b>cộng dồn</b> gradient.",
        "hook_chk": ["3.0 * 2.0 + 2.0 == 8.0", "2.0 + 2.0 == 4.0"],
        "formula_txt": (
            "<p><b>1. Nếu quên <code>zero_grad()</code>:</b> sau 2 lần gọi <code>backward()</code> trên <code>y = x^2</code> tại <code>x=3</code>, <code>x.grad</code> thành <code>6 + 6 = <b>12</b></code> thay vì <code>6</code>.</p>"
            "<p><b>2. Cập nhật SGD:</b> <code>w_new = w - lr * dL/dw</code>.</p>"
        ),
        "formula_say": (
            "Ví dụ toán học cực gọn chứng minh bản chất cộng dồn của đạo hàm trong bộ nhớ tensor. "
            "Đạo hàm của bình phương tại x bằng ba đúng ra chỉ là sáu. "
            "Nếu gọi truyền ngược hai lần liên tiếp mà không xóa giữa chừng, giá trị trong thuộc tính đạo hàm bị cộng thành mười hai."
        ),
        "sym_rows": [
            ["<code>torch.tensor(..., requires_grad=True)</code>", "Tạo Tensor theo dõi mọi phép tính để tính đạo hàm"],
            ["<code>opt = torch.optim.SGD(..., lr=0.1)</code>", "Bộ tối ưu hạ độ dốc ngẫu nhiên với tốc độ học 0.1"],
            ["<code>opt.zero_grad() / loss.backward() / opt.step()</code>", "Bộ ba xóa cũ → lan truyền ngược → bước cập nhật tham số"],
        ],
        "sym_say": (
            "Bảng ký hiệu liệt kê đúng ba phần cốt lõi trong mã nguồn PyTorch CPU. "
            "Cờ theo dõi đạo hàm bật cho các tham số cần học, còn bộ tối ưu giữ nhiệm vụ trừ đạo hàm nhân bước học khỏi trọng số. "
            "Bộ ba lệnh xóa cũ, truyền ngược và cập nhật luôn đứng đúng thứ tự đó."
        ),
        "ex_code": (
            "import torch\n"
            "torch.manual_seed(42)\n"
            "x = torch.linspace(-1, 1, 20).unsqueeze(1)\n"
            "y = 3.0 * x + 2.0\n"
            "layer = torch.nn.Linear(1, 1)\n"
            "opt = torch.optim.SGD(layer.parameters(), lr=0.2)\n"
            "for _ in range(120):\n"
            "    opt.zero_grad()\n"
            "    loss = ((layer(x) - y) ** 2).mean()\n"
            "    loss.backward()\n"
            "    opt.step()\n"
            "print(f'w={layer.weight.item():.3f} b={layer.bias.item():.3f} loss={loss.item():.6f}')\n"
        ),
        "ex_say": (
            "Đoạn mã huấn luyện lớp tuyến tính một đầu vào một đầu ra trên hai mươi điểm thuộc đường thẳng ba ích cộng hai. "
            "Chỉ với một trăm hai mươi vòng hạ độ dốc trên CPU và hạt giống bốn hai, mọi trọng số hội tụ hoàn toàn."
        ),
        "ex_out_say": (
            "Kết quả chạy thật chứng minh trọng số tiến sát ba phẩy không không, độ chệch tiến sát hai phẩy không không và sai số mất mát tiến về không. "
            "Toàn bộ quá trình diễn ra nhanh tức thì trên CPU thuần."
        ),
        "chk_code": (
            "import torch\n"
            "x = torch.tensor(3.0, requires_grad=True)\n"
            "(x ** 2).backward(); g1 = x.grad.item()\n"
            "(x ** 2).backward(); g2_acc = x.grad.item()\n"
            "x.grad.zero_(); (x ** 2).backward(); g_reset = x.grad.item()\n"
            "print(f'g1={g1:.1f} g2_accumulated={g2_acc:.1f} g_after_zero={g_reset:.1f}')\n"
        ),
        "chk_say": (
            "Phép kiểm chứng thứ hai chạy trực tiếp hàm ích bình phương tại ích bằng ba để đo tận mắt hành vi cộng dồn đạo hàm. "
            "Lần đầu gọi truyền ngược, sau đó gọi tiếp lần hai không xóa, rồi mới xóa và gọi lại lần ba."
        ),
        "chk_out_say": (
            "Đầu ra ghi nhận đúng ba con số sáu, mười hai rồi quay lại sáu, vì thiếu bước xóa thì autograd cộng dồn đạo hàm mới vào bộ nhớ đệm đang giữ sẵn."
        ),
        "quymo": [
            ("Mô hình 1 lớp tuyến tính CPU", "120 vòng hết ~15 ms", "Khớp tức thì không cần GPU"),
            ("Huấn luyện batch lớn 4 096 mẫu", "Cộng dồn grad 4 micro-batch rồi mới step()", "Đây chính là lý do PyTorch thiết kế cộng dồn grad mặc định!"),
            ("Quên zero_grad()", "Bước cập nhật phình theo cấp số cộng", "Mất mát nhanh chóng thành NaN"),
        ],
        "quymo_say": (
            "Bảng quy mô giải thích nghịch lý thiết kế rất hay của thư viện: cơ chế mặc định cộng dồn không phải lỗi, mà giúp gom nhiều lô nhỏ khi thiếu bộ nhớ trước khi bước cập nhật."
        ),
        "pitfalls": [
            "<b>Lỗi 1 (-30đ):</b> Quên <code>optimizer.zero_grad()</code> trong vòng huấn luyện làm gradient cộng dồn và bùng nổ.",
            "<b>Lỗi 2 (-20đ):</b> Dùng số nguyên <code>torch.tensor([1, 2])</code> thay vì số thực <code>float32</code> làm autograd từ chối theo dõi.",
            "<b>Lỗi 3 (-10đ):</b> Quên <code>unsqueeze(1)</code> khiến đầu vào 1D <code>(20,)</code> sai chiều cho tầng <code>Linear(1, 1)</code>.",
        ],
        "pitfalls_say": (
            "Bạn tránh kỹ ba lỗi lập trình PyTorch đầu tay sau đây. "
            "Một là quên xóa đạo hàm đầu vòng, hai là truyền nhầm tensor số nguyên vào lớp tính đạo hàm chỉ nhận số thực, "
            "và ba là thiếu một chiều cột khi truyền vào tầng tuyến tính."
        ),
        "q_text": "<ol><li>Tại <code>x = 3</code>, nếu gọi <code>(x**2).backward()</code> hai lần liên tiếp KHÔNG xóa, <code>x.grad</code> bằng mấy?</li><li>Trong 3 lệnh <code>zero_grad / backward / step</code>, lệnh nào bắt buộc đứng đầu hoặc xóa trước vòng mới?</li></ol>",
        "q_say": "Hãy tự kiểm tra qua hai câu hỏi chốt bài mười ngay dưới đây. Câu một, tại ích bằng ba nếu truyền ngược ích bình phương hai lần liên tiếp không xóa thì đạo hàm bằng mấy? Câu hai, trong ba lệnh xóa, truyền ngược và cập nhật, lệnh nào xóa bộ nhớ đệm đạo hàm cũ? Bấm tạm dừng và trả lời.",
        "q_ans1": "Bằng <code>6 + 6 = <b>12.0</b></code> do PyTorch cộng dồn gradient.",
        "q_ans1_say": "Đáp án câu một: bằng mười hai vì đạo hàm đúng sáu bị cộng dồn hai lần liên tiếp.",
        "q_ans2": "<code><b>zero_grad()</b></code> xóa sạch đạo hàm cũ về 0 trước khi gọi <code>backward()</code> tính đạo hàm vòng mới.",
        "q_ans2_say": "Đáp án câu hai: lệnh xóa đạo hàm về không sẽ xóa sạch bộ đệm cũ trước khi tính vòng mới.",
        "lab_de": (
            "# Lab MLP L10 — PyTorch CPU Autograd, zero_grad & khớp hồi quy tuyến tính\n\n"
            "Viết chương trình Python (chạy bằng `labs/.venv-ml` qua `cham.sh`): "
            "(1) kiểm chứng `(x**2).backward()` 2 lần liên tiếp tại `x=3.0` cho `12.0` và sau `zero_()` cho `6.0`; "
            "(2) huấn luyện `torch.nn.Linear(1, 1)` với `torch.manual_seed(42)`, `SGD(lr=0.2)` 120 bước trên `y = 3x + 2`, in đúng 3 dòng:\n"
            "1. `grad_accum=12.0`\n2. `grad_reset=6.0`\n3. `fitted_wb=3.00_2.00`\n\n"
            "Chấm tự động:\n```bash\nbash labs/cham.sh MLP L10 duong_dan/bai_cua_ban.py\n```"
        ),
        "lab_sol": (
            "import torch\n"
            "x0 = torch.tensor(3.0, requires_grad=True)\n"
            "(x0 ** 2).backward(); (x0 ** 2).backward()\n"
            "acc = x0.grad.item()\n"
            "x0.grad.zero_(); (x0 ** 2).backward()\n"
            "rst = x0.grad.item()\n"
            "torch.manual_seed(42)\n"
            "x = torch.linspace(-1, 1, 20).unsqueeze(1); y = 3.0 * x + 2.0\n"
            "m = torch.nn.Linear(1, 1); opt = torch.optim.SGD(m.parameters(), lr=0.2)\n"
            "for _ in range(120):\n"
            "    opt.zero_grad(); loss = ((m(x) - y) ** 2).mean(); loss.backward(); opt.step()\n"
            "print(f'grad_accum={acc:.1f}')\n"
            "print(f'grad_reset={rst:.1f}')\n"
            "print(f'fitted_wb={m.weight.item():.2f}_{m.bias.item():.2f}')\n"
        ),
        "chain": ["Tensor float32 + requires_grad", "zero_grad tránh cộng dồn", "backward + step hội tụ"],
    },
    {
        "id": "L11",
        "fname": "L11_mang_mlp_pytorch_cpu.yaml",
        "title": "Bài 11 — Mạng nơ-ron đa tầng MLP trên PyTorch CPU cho bài toán phi tuyến",
        "assumes": ["mlp_autograd"],
        "introduces": [],
        "obj": [
            "Ghép hai tầng Linear xen giữa hàm kích hoạt phi tuyến ReLU tạo ranh giới cong",
            "Dùng CrossEntropyLoss trên đầu ra logit thô và chế độ model.eval() + torch.no_grad()",
            "Phân tích lỗi đặt nhầm Softmax hai lần trước CrossEntropyLoss làm suy giảm gradient",
        ],
        "prereq": [
            ("Vòng huấn luyện Tensor & Autograd (MLP:L10)", "Bộ khung xóa grad → lan truyền ngược → bước cập nhật"),
            ("Tính tuyến tính bất biến của tầng Linear chồng nhau", "Hai ma trận nhân thẳng không có kích hoạt giữa chỉ ra một ma trận duy nhất"),
            ("Hàm mất mát đa lớp CrossEntropyLoss", "Đã tích hợp sẵn LogSoftmax nên nhận thẳng điểm thô logit"),
        ],
        "prereq_say": (
            "Bài mười một nâng từ một lớp tuyến tính lên mạng đa tầng hoàn chỉnh chạy trên CPU. "
            "Nếu xếp hai tầng tuyến tính nối liền mà quên chèn hàm kích hoạt phi tuyến ở giữa, cả mạng vẫn sụp thành một đường thẳng đơn điệu. "
            "Đồng thời ta tránh bẫy đặt thừa hàm Softmax trước hàm mất mát đa lớp."
        ),
        "svg_boxes": [("Linear(2, 16) + ReLU", "Bẻ cong không gian 16 chiều"), ("Linear(16, 2) -> Logits", "Không đặt Softmax cuối!"), ("eval() + no_grad()", "Suy luận nhanh, không dựng đồ thị")],
        "svg_say": (
            "Kiến trúc mạng gồm một lớp ẩn mười sáu nơ-ron kết hợp hàm ReLU làm gãy khúc không gian, theo sau bởi lớp đầu ra hai điểm thô. "
            "Khi chấm điểm trên tập kiểm tra, luôn bật chế độ đánh giá và tắt theo dõi đạo hàm để tiết kiệm bộ nhớ."
        ),
        "hook_say": (
            "Hai tầng tuyến tính xếp chồng lên nhau mà thiếu kích hoạt phi tuyến sẽ chỉ học được đúng một đường thẳng chia cắt dữ liệu hai lớp, nên hoàn toàn bất lực trước bài toán XOR kinh điển. "
            "Chỉ cần chèn một lớp ReLU ở giữa và giữ đầu ra logit thô, mạng nhỏ trên CPU dễ dàng giải trọn bài toán phi tuyến."
        ),
        "hook_txt": "Mạng <b>2 → 16 → 2</b> xen giữa <code>ReLU()</code> học tách chính xác ranh giới phi tuyến trên CPU. Lớp cuối giữ nguyên <b>logits thô</b> vì <code>CrossEntropyLoss</code> tự áp <code>LogSoftmax</code> bên trong.",
        "hook_chk": ["2 * 16 + 16 + 16 * 2 + 2 == 82", "1 + 1 == 2"],
        "formula_txt": (
            "<p><b>1. Nếu thiếu ReLU:</b> <code>W2 (W1 x + b1) + b2 = (W2 W1) x + (W2 b1 + b2)</code> — vẫn chỉ là một hàm bậc nhất!</p>"
            "<p><b>2. Số tham số mạng 2→16→2:</b> <code>(2*16 + 16) + (16*2 + 2) = 48 + 34 = <b>82</b></code> trọng số.</p>"
        ),
        "formula_say": (
            "Hai công thức chứng minh rõ vai trò sống còn của hàm kích hoạt và cách đếm tham số mạng. "
            "Nhân hai phép biến đổi tuyến tính luôn cho ra một phép biến đổi tuyến tính mới nếu không có hàm phi tuyến chặn giữa. "
            "Mạng nhỏ tám mươi hai trọng số này đủ nhẹ để chạy tức thì trên mọi CPU."
        ),
        "sym_rows": [
            ["<code>nn.Sequential(nn.Linear(2, 16), nn.ReLU(), nn.Linear(16, 2))</code>", "Chuỗi 2 tầng có kích hoạt ReLU bẻ cong biên"],
            ["<code>nn.CrossEntropyLoss()</code>", "Hàm mất mát phân loại nhận trực tiếp logits thô (chưa qua Softmax)"],
            ["<code>with torch.no_grad():</code>", "Tắt autograd khi kiểm thử để tiết kiệm RAM và tăng tốc"],
        ],
        "sym_say": (
            "Bảng ký hiệu giải thích ba công cụ dựng mạng và suy luận sạch trong PyTorch. "
            "Khối xếp tuần tự nối các tầng gọn thành một đối tượng duy nhất. "
            "Còn khối ngữ cảnh tắt đạo hàm loại bỏ hoàn toàn chi phí ghi đồ thị tính toán khi đánh giá."
        ),
        "ex_code": (
            "import torch, torch.nn as nn\n"
            "torch.manual_seed(42)\n"
            "X = torch.tensor([[0.,0.],[0.,1.],[1.,0.],[1.,1.]] * 25)\n"
            "y = torch.tensor([0, 1, 1, 0] * 25)\n"
            "net = nn.Sequential(nn.Linear(2, 16), nn.ReLU(), nn.Linear(16, 2))\n"
            "opt = torch.optim.Adam(net.parameters(), lr=0.05); crit = nn.CrossEntropyLoss()\n"
            "for _ in range(150):\n"
            "    opt.zero_grad(); loss = crit(net(X), y); loss.backward(); opt.step()\n"
            "net.eval()\n"
            "with torch.no_grad(): acc = (net(X[:4]).argmax(1) == y[:4]).float().mean().item()\n"
            "n_par = sum(p.numel() for p in net.parameters())\n"
            "print(f'n_params={n_par} xor_acc={acc:.2f} loss={loss.item():.4f}')\n"
        ),
        "ex_say": (
            "Đoạn mã huấn luyện mạng tám mươi hai trọng số giải bài toán XOR bốn góc đối xứng trên CPU. "
            "Lớp cuối giữ nguyên điểm logit thô truyền thẳng vào hàm mất mát đa lớp, và khi chấm kết quả ta bật chế độ đánh giá kèm ngữ cảnh tắt đạo hàm."
        ),
        "ex_out_say": (
            "Kết quả chạy thật đạt đúng tám mươi hai tham số, độ chính xác tuyệt đối một trăm phần trăm trên bốn góc XOR và mất mát tiến sát không. "
            "Điều này chứng tỏ lớp ReLU đã giúp mạng học gọn đường cắt chéo phi tuyến."
        ),
        "chk_code": (
            "import torch, torch.nn as nn\n"
            "torch.manual_seed(42)\n"
            "X = torch.tensor([[0.,0.],[0.,1.],[1.,0.],[1.,1.]])\n"
            "y = torch.tensor([0, 1, 1, 0])\n"
            "lin = nn.Sequential(nn.Linear(2, 16), nn.Linear(16, 2))\n"
            "opt = torch.optim.SGD(lin.parameters(), lr=0.1); crit = nn.CrossEntropyLoss()\n"
            "for _ in range(200): opt.zero_grad(); l = crit(lin(X), y); l.backward(); opt.step()\n"
            "with torch.no_grad(): acc = (lin(X).argmax(1) == y).float().mean().item()\n"
            "print(f'no_relu_xor_acc={acc:.2f}')\n"
        ),
        "chk_say": (
            "Ở nhánh kiểm chứng đối chứng, ta cố tình rút bỏ hàm kích hoạt ReLU giữa hai lớp tuyến tính rồi huấn luyện hai trăm vòng trên đúng bốn điểm XOR đó. "
            "Vì tích hai ma trận vẫn chỉ là một đường thẳng đơn nên không đường thẳng nào tách nổi bốn góc chéo nhau."
        ),
        "chk_out_say": (
            "Đầu ra ghi nhận độ chính xác chỉ kẹt ở hai mươi lăm phần trăm — còn tệ hơn đoán ngẫu nhiên, chứng minh hàm kích hoạt phi tuyến là bắt buộc cho mạng nhiều lớp."
        ),
        "quymo": [
            ("MLP 2→16→2 (82 tham số)", "CPU ~40 ms cho 150 epoch", "Nhanh gọn thử nghiệm biên phi tuyến"),
            ("Đặt nhầm Softmax trước CrossEntropyLoss", "Áp Softmax 2 lần -> mất tín hiệu grad", "Luôn giữ lớp cuối là Linear trả logit"),
            ("Quên model.eval() lúc phục vụ", "Dropout/BatchNorm vẫn nhảy ngẫu nhiên", "Bắt buộc model.eval() + with torch.no_grad()"),
        ],
        "quymo_say": (
            "Bảng quy mô nhấn mạnh kỷ luật khi đưa mạng PyTorch ra phục vụ người dùng: luôn gọi chế độ đánh giá và tắt đạo hàm, không bao giờ chèn thêm Softmax trước hàm mất mát chéo."
        ),
        "pitfalls": [
            "<b>Lỗi 1 (-30đ):</b> Thêm <code>nn.Softmax(dim=1)</code> vào cuối mạng rồi truyền vào <code>nn.CrossEntropyLoss()</code>.",
            "<b>Lỗi 2 (-20đ):</b> Quên <code>nn.ReLU()</code> giữa các tầng <code>Linear</code> làm mạng sụp thành hàm tuyến tính bậc nhất.",
            "<b>Lỗi 3 (-10đ):</b> Quên <code>model.eval()</code> và <code>with torch.no_grad():</code> lúc suy luận gây rò RAM.",
        ],
        "pitfalls_say": (
            "Ba lỗi kỹ thuật rất phổ biến cần tránh khi viết mạng nơ-ron trong PyTorch là như sau. "
            "Thứ nhất là lồng Softmax kép vào hàm mất mát chéo, thứ hai là thiếu hàm kích hoạt phi tuyến giữa các lớp, "
            "và thứ ba là quên tắt theo dõi đạo hàm khi suy luận."
        ),
        "q_text": "<ol><li>Tại sao hai tầng <code>Linear</code> nối liền KHÔNG có <code>ReLU</code> lại không giải được XOR?</li><li>Mạng dùng <code>nn.CrossEntropyLoss()</code> có nên đặt <code>nn.Softmax</code> ở lớp cuối không?</li></ol>",
        "q_say": "Bạn kiểm tra nhanh hai câu hỏi cho bài mười một nhé. Câu một, vì sao hai lớp tuyến tính nối liền nhau thiếu ReLU lại không giải nổi bài toán XOR? Câu hai, khi dùng hàm mất mát phân loại chéo có nên thêm lớp Softmax cuối mạng không? Bấm tạm dừng và trả lời.",
        "q_ans1": "Vì hợp thành của hai phép biến đổi tuyến tính vẫn chỉ là <b>một phép tuyến tính</b> (một đường thẳng), không tách được hai cặp chéo XOR.",
        "q_ans1_say": "Đáp án câu một: hợp hai phép tuyến tính vẫn chỉ ra một đường thẳng nên không chia nổi bốn góc đối xứng.",
        "q_ans2": "<b>Không</b> — <code>CrossEntropyLoss</code> đã tự tính <code>LogSoftmax</code> bên trong, thêm <code>Softmax</code> sẽ bóp nghẹt gradient.",
        "q_ans2_say": "Đáp án câu hai: không được đặt, vì hàm mất mát đã tự tính lô-ga-rít Softmax bên trong rồi.",
        "lab_de": (
            "# Lab MLP L11 — Mạng MLP 2→16→2 PyTorch CPU giải XOR & đối chứng thiếu ReLU\n\n"
            "Viết chương trình Python (chạy bằng `labs/.venv-ml` qua `cham.sh`): "
            "với `torch.manual_seed(42)`, huấn luyện mạng `Linear(2,16) -> ReLU -> Linear(16,2)` bằng `Adam(lr=0.05)` + `CrossEntropyLoss()` 150 bước trên 100 mẫu XOR "
            "và đối chứng mạng thiếu ReLU (`SGD(lr=0.1)` 200 bước trên 4 mẫu), in đúng 3 dòng:\n"
            "1. `n_params=82`\n2. `mlp_xor_acc=1.00`\n3. `no_relu_xor_acc=0.25`\n\n"
            "Chấm tự động:\n```bash\nbash labs/cham.sh MLP L11 duong_dan/bai_cua_ban.py\n```"
        ),
        "lab_sol": (
            "import torch, torch.nn as nn\n"
            "torch.manual_seed(42)\n"
            "X = torch.tensor([[0.,0.],[0.,1.],[1.,0.],[1.,1.]] * 25)\n"
            "y = torch.tensor([0, 1, 1, 0] * 25)\n"
            "net = nn.Sequential(nn.Linear(2, 16), nn.ReLU(), nn.Linear(16, 2))\n"
            "opt = torch.optim.Adam(net.parameters(), lr=0.05); crit = nn.CrossEntropyLoss()\n"
            "for _ in range(150): opt.zero_grad(); loss = crit(net(X), y); loss.backward(); opt.step()\n"
            "net.eval()\n"
            "with torch.no_grad(): acc_mlp = (net(X[:4]).argmax(1) == y[:4]).float().mean().item()\n"
            "torch.manual_seed(42)\n"
            "lin = nn.Sequential(nn.Linear(2, 16), nn.Linear(16, 2))\n"
            "opt2 = torch.optim.SGD(lin.parameters(), lr=0.1)\n"
            "for _ in range(200): opt2.zero_grad(); l2 = crit(lin(X[:4]), y[:4]); l2.backward(); opt2.step()\n"
            "with torch.no_grad(): acc_lin = (lin(X[:4]).argmax(1) == y[:4]).float().mean().item()\n"
            "print(f'n_params={sum(p.numel() for p in net.parameters())}')\n"
            "print(f'mlp_xor_acc={acc_mlp:.2f}')\n"
            "print(f'no_relu_xor_acc={acc_lin:.2f}')\n"
        ),
        "chain": ["ReLU phá tính tuyến tính", "Giữ logits thô cho CrossEntropy", "eval() + no_grad() lúc chạy"],
    },
    {
        "id": "L12",
        "fname": "L12_dong_goi_suy_luan_cpu.yaml",
        "title": "Bài 12 — Đóng gói trọng số an toàn JSON, bất biến suy luận & đo độ trễ CPU",
        "assumes": ["mlp_leakage", "mlp_pipeline"],
        "introduces": [],
        "obj": [
            "Giải thích rủi ro bảo mật thực thi mã lạ của tệp pickle không tin cậy khi triển khai",
            "Xuất tham số scaler (mean, scale) và trọng số (coef, intercept) ra JSON thuần tất định",
            "Đối chiếu đầu ra suy luận Python thuần khớp tuyệt đối với scikit-learn trong sai số 1e-9",
        ],
        "prereq": [
            ("Rủi ro bảo mật định dạng Pickle", "Nạp tệp pickle cho phép chạy mã Python tuỳ ý lúc giải tuần tự"),
            ("Chuỗi xử lý khép kín (MLP:L00)", "Toàn bộ mô hình tuyến tính chỉ gồm 4 mảng số: mean, scale, coef, intercept"),
            ("Kiểm chứng tương đương toán học", "Dịch vụ Python thuần không cài scikit-learn vẫn tính khớp sai số < 1e-12"),
        ],
        "prereq_say": (
            "Huấn luyện xong một mô hình tốt mới chỉ là nửa chặng đường, nửa sau là triển khai an toàn và nhẹ nhàng vào dịch vụ. "
            "Định dạng pickle quen thuộc tiềm ẩn nguy cơ thực thi mã độc và phụ thuộc cứng phiên bản thư viện lúc huấn luyện. "
            "Bài mười hai hướng dẫn xuất toàn bộ trọng số sang JSON thuần và đối chứng độ chính xác tuyệt đối."
        ),
        "svg_boxes": [("Huấn luyện Pipeline", "Trích mean, scale, w, b"), ("Lưu tệp JSON thuần", "0 mã thực thi, đọc mọi ngôn ngữ"), ("Suy luận sigmoid(z)", "Khớp scikit-learn sai số < 1e-12")],
        "svg_say": (
            "Sơ đồ mô tả quy trình tách rời môi trường huấn luyện nặng nề khỏi dịch vụ phục vụ gọn nhẹ. "
            "Từ chuỗi xử lý đã khớp, ta trích bốn danh sách số thực lưu vào JSON an toàn. "
            "Dịch vụ sản xuất chỉ cần vài dòng tính tích vô hướng và hàm mũ để ra kết quả giống hệt từng chữ số."
        ),
        "hook_say": (
            "Khi cập nhật phiên bản thư viện máy chủ, rất nhiều tệp pickle cũ lập tức báo lỗi không nạp được, chưa kể rủi ro chèn mã thực thi tuỳ ý qua hàm tạo đối tượng. "
            "Nếu xuất mô hình tuyến tính ra đúng bốn trường số JSON, bất kỳ ngôn ngữ nào từ Python tới Go đều suy luận chuẩn xác dưới một phần mười mi-li-giây."
        ),
        "hook_txt": "Đóng gói an toàn <b>4 khoá JSON</b>: <code>mean</code>, <code>scale</code>, <code>coef</code>, <code>intercept</code>. Phép suy luận thuần <code>1 / (1 + exp(-(sum((x - mean)/scale * w) + b)))</code> khớp gốc với độ lệch tối đa <code>&lt; <b>1e-12</b></code>.",
        "hook_chk": ["1.0 / (1.0 + 1.0) == 0.5", "1e-12 < 1e-9"],
        "formula_txt": (
            "<p><b>1. Chuẩn hóa &amp; Logit:</b> <code>z = sum_j ((x_j - mean_j) / scale_j) * w_j + b</code>.</p>"
            "<p><b>2. Xác suất Sigmoid ổn định:</b> <code>p = 1 / (1 + exp(-z))</code> khớp tuyệt đối <code>predict_proba(x)[0, 1]</code>.</p>"
        ),
        "formula_say": (
            "Hai công thức trên là toàn bộ trái tim toán học nằm bên trong đường ống chuẩn hóa kết hợp hồi quy logistic. "
            "Đầu tiên trừ trung bình và chia độ lệch chuẩn từng cột rồi nhân vô hướng với mảng trọng số cộng độ chệch. "
            "Cuối cùng áp hàm sigmoid để biến điểm logit thành xác suất trong khoảng không một."
        ),
        "sym_rows": [
            ["<code>json.dumps({'mean': ..., 'scale': ..., 'coef': ..., 'b': ...})</code>", "Đóng gói tham số thuần dữ liệu, không thực thi mã"],
            ["<code>math.exp(-z)</code>", "Hàm mũ chuẩn thư viện gốc để tính sigmoid không cần thư viện ngoài"],
            ["<code>max_abs_diff &lt; 1e-9</code>", "Bất biến đối chiếu đầu ra suy luận thuần so với scikit-learn"],
        ],
        "sym_say": (
            "Bảng ký hiệu nêu cấu trúc gói JSON thuần dữ liệu và ngưỡng sai số đối chiếu. "
            "Khác với tệp nhị phân pickle, tệp JSON chỉ chứa các số dấu phẩy động đọc hiểu bằng mắt thường. "
            "Hàm đối chứng yêu cầu sai lệch giữa hàm tự viết và thư viện gốc nhỏ hơn một phần tỉ."
        ),
        "ex_code": (
            "import json, math\n"
            "from sklearn.datasets import make_classification\n"
            "from sklearn.preprocessing import StandardScaler as SS\n"
            "from sklearn.linear_model import LogisticRegression as LR\n"
            "from sklearn.pipeline import Pipeline\n"
            "X, y = make_classification(120, n_features=4, random_state=42)\n"
            "p = Pipeline([('s', SS()), ('c', LR(random_state=42))]).fit(X, y)\n"
            "m, s, w, b = [x.tolist() for x in (p['s'].mean_, p['s'].scale_,\n"
            "              p['c'].coef_[0])] + [float(p['c'].intercept_[0])]\n"
            "pkg = json.loads(json.dumps({'m': m, 's': s, 'w': w, 'b': b}))\n"
            "diffs = [abs(1.0 / (1.0 + math.exp(-(sum((v - m0) / s0 * w0\n"
            "  for v, m0, s0, w0 in zip(r, pkg['m'], pkg['s'], pkg['w'])) + pkg['b'])))\n"
            "  - float(pr)) for r, pr in zip(X[:5], p.predict_proba(X[:5])[:, 1])]\n"
            "print(f'max_diff={max(diffs):.2e} match_1e9={int(max(diffs) < 1e-9)}')\n"
        ),
        "ex_say": (
            "Đoạn mã huấn luyện xong mô hình rồi đóng gói ngay bốn thành phần vào chuỗi JSON và nạp lại bằng mô-đun chuẩn. "
            "Trên năm mẫu đầu tiên, ta dùng hàm toán học thuần tính lại xác suất từ bốn danh sách số vừa giải mã để đối chiếu từng con số."
        ),
        "ex_out_say": (
            "Đầu ra chạy thật chứng minh sai lệch tối đa chỉ ở cỡ mười mũ trừ mười lăm hay mười mũ trừ mười sáu. "
            "Bởi phép tính dấu phẩy động hoàn toàn tương đương nên bạn có thể triển khai sang mọi dịch vụ siêu nhẹ mà không mang theo cả cây thư viện huấn luyện."
        ),
        "chk_code": (
            "import json\n"
            "blob = json.dumps({'mean': [1.0, 2.0], 'scale': [0.5, 2.0], 'w': [1.5, -0.5], 'b': 0.2})\n"
            "obj = json.loads(blob)\n"
            "print(f'keys_ok={int(set(obj) == {\"mean\",\"scale\",\"w\",\"b\"})} json_bytes={len(blob)}')\n"
        ),
        "chk_say": (
            "Phép kiểm chứng thứ hai xác minh kích thước gọn nhẹ của gói JSON và cấu trúc đủ bốn khoá bắt buộc. "
            "Chỉ mất vài chục bai cho một mô hình tuyến tính hoàn chỉnh so với hàng chục mê-ga-bai của bộ khung đóng gói nặng."
        ),
        "chk_out_say": (
            "Kết quả in ra bằng một khẳng định đủ cả bốn khoá và tổng dung lượng chỉ sáu mươi chín bai, vì cấu trúc dữ liệu thuần chỉ giữ các con số cốt lõi cần cho phép tính."
        ),
        "quymo": [
            ("Gói JSON trọng số tuyến tính", "~1 KB cho 20 đặc trưng", "An toàn tuyệt đối khỏi lỗ hổng deserialization"),
            ("Tốc độ 1 request đơn lẻ", "~5 micro-giây bằng Python thuần", "Không tốn chi phí khởi tạo mảng sklearn mỗi yêu cầu"),
            ("Mô hình cây / mạng sâu lớn", "Dùng định dạng ONNX / SafeTensors", "Không nhận tệp pickle từ bên ngoài không ký xác thực"),
        ],
        "quymo_say": (
            "Bảng quy mô mở rộng góc nhìn khi chuyển sang các kiến trúc phức tạp hơn như rừng cây hay mạng sâu nhiều tầng. "
            "Với mô hình lớn hãy chọn chuẩn chuyên biệt an toàn như ONNX hay SafeTensors thay vì nạp pickle tuỳ tiện."
        ),
        "pitfalls": [
            "<b>Lỗi 1 (-30đ):</b> Nạp <code>pickle.load()</code> từ nguồn không xác thực cho phép kẻ tấn công chèn <code>__reduce__</code> chạy lệnh hệ thống.",
            "<b>Lỗi 2 (-20đ):</b> Xuất trọng số <code>coef_</code> của mô hình nhưng quên xuất <code>mean_</code> và <code>scale_</code> của <code>StandardScaler</code>.",
            "<b>Lỗi 3 (-10đ):</b> Không viết bài kiểm thử đối chiếu sai số tuyệt đối giữa dịch vụ suy luận và mô hình gốc.",
        ],
        "pitfalls_say": (
            "Ba sai lầm triển khai cần tránh tuyệt đối ở khâu đóng gói gồm những điểm sau. "
            "Một là dùng pickle không kiểm soát nguồn gốc, hai là xuất trọng số mà bỏ quên thông số chuẩn hóa đi kèm, "
            "và ba là thiếu kiểm thử đối chiếu xác suất đầu ra trước lúc phát hành."
        ),
        "q_text": "<ol><li>Vì sao không nên dùng <code>pickle</code> để nạp tệp mô hình từ nguồn ngoài không tin cậy?</li><li>Nếu chỉ xuất trọng số <code>w, b</code> mà quên xuất <code>mean_, scale_</code> thì kết quả suy luận sai thế nào?</li></ol>",
        "q_say": "Mời bạn tự kiểm tra kiến thức triển khai với hai câu hỏi cuối bài mười hai. Câu một, vì sao không nên nạp tệp pickle từ nguồn không tin cậy? Câu hai, nếu chỉ lưu trọng số mà quên lưu trung bình và độ lệch chuẩn thì suy luận bị sai gì? Bấm tạm dừng và trả lời.",
        "q_ans1": "Vì <code>pickle</code> có thể thực thi mã Python tuỳ ý trong quá trình giải tuần tự (lỗ hổng RCE bảo mật).",
        "q_ans1_say": "Đáp án câu một: vì pickle cho phép thực thi mã tuỳ ý ngay trong bước giải mã nên rất nguy hiểm về bảo mật.",
        "q_ans2": "Đầu vào mới sẽ không được chuẩn hóa đúng thang đo lúc Train, khiến tích vô hướng <code>w * x</code> lệch thang đo hoàn toàn.",
        "q_ans2_say": "Đáp án câu hai: đầu vào mới không được đưa về đúng thang đo lúc huấn luyện nên mọi phép nhân trọng số đều sai lệch hoàn toàn.",
        "lab_de": (
            "# Lab MLP L12 — Xuất mô hình JSON an toàn & đối chiếu sai số suy luận thuần\n\n"
            "Viết chương trình Python (chạy bằng `labs/.venv-ml` qua `cham.sh`): "
            "huấn luyện `Pipeline` (`StandardScaler` + `LogisticRegression(random_state=42)`) trên `make_classification(n_samples=120, n_features=4, random_state=42)`, "
            "xuất `mean, scale, w, b` qua `json.loads(json.dumps(...))`, đối chiếu xác suất thuần `1/(1+exp(-z))` trên 5 mẫu đầu so với `predict_proba`, in đúng 3 dòng:\n"
            "1. `json_keys_ok=1`\n2. `match_lt_1e9=1`\n3. `first_prob=...`\n\n"
            "Chấm tự động:\n```bash\nbash labs/cham.sh MLP L12 duong_dan/bai_cua_ban.py\n```"
        ),
        "lab_sol": (
            "import json, math\n"
            "from sklearn.datasets import make_classification\n"
            "from sklearn.preprocessing import StandardScaler\n"
            "from sklearn.linear_model import LogisticRegression\n"
            "from sklearn.pipeline import Pipeline\n"
            "X, y = make_classification(n_samples=120, n_features=4, random_state=42)\n"
            "pipe = Pipeline([('sc', StandardScaler()), ('clf', LogisticRegression(random_state=42))]).fit(X, y)\n"
            "pkg = json.loads(json.dumps({'mean': pipe['sc'].mean_.tolist(), 'scale': pipe['sc'].scale_.tolist(),\n"
            "                             'w': pipe['clf'].coef_[0].tolist(), 'b': float(pipe['clf'].intercept_[0])}))\n"
            "probs, diffs = [], []\n"
            "for row, ref in zip(X[:5], pipe.predict_proba(X[:5])[:, 1]):\n"
            "    z = sum(((v - m) / s) * w for v, m, s, w in zip(row, pkg['mean'], pkg['scale'], pkg['w'])) + pkg['b']\n"
            "    p = 1.0 / (1.0 + math.exp(-z)); probs.append(p); diffs.append(abs(p - float(ref)))\n"
            "print(f'json_keys_ok={int(set(pkg) == {\"mean\", \"scale\", \"w\", \"b\"})}')\n"
            "print(f'match_lt_1e9={int(max(diffs) < 1e-9)}')\n"
            "print(f'first_prob={probs[0]:.6f}')\n"
        ),
        "chain": ["Tránh pickle không tin cậy", "JSON giữ đủ scaler + w + b", "Kiểm khớp < 1e-9"],
    },
    {
        "id": "L13",
        "fname": "L13_tinh_huong_phat_hien_gian_lan.yaml",
        "title": "Bài 13 — Tình huống chuyên gia: Hệ thống phát hiện gian lận từ đầu tới triển khai",
        "assumes": ["mlp_leakage", "mlp_pipeline"],
        "introduces": [],
        "obj": [
            "Tổ chức đường ống đánh giá gian lận 2% bảo toàn thứ tự thời gian không rò rỉ",
            "So sánh điểm PR-AUC và Brier score giữa LogisticRegression và HistGradientBoostingClassifier",
            "Thiết lập ngưỡng cảnh báo tối ưu và kiểm thử suy luận tất định sẵn sàng triển khai",
        ],
        "prereq": [
            ("Tách tập giữ thứ tự thời gian (MLP:L08)", "Chia cắt theo mốc thời gian thực, không xáo trộn tương lai"),
            ("Xử lý lệch nhãn & hiệu chuẩn (MLP:L05)", "Đo PR-AUC và Brier thay cho Accuracy ảo"),
            ("So sánh hai họ mô hình (MLP:L00/L07)", "Tuyến tính có Pipeline chuẩn hóa vs Cây tăng cường độ dốc"),
        ],
        "prereq_say": (
            "Bài mười ba khép lại khoá học máy thực hành bằng một tình huống chuyên gia hoàn chỉnh từ dữ liệu thô tới kiểm thử phát hành. "
            "Bài toán đặt ra là phát hiện giao dịch gian lận chỉ chiếm bốn phần trăm theo dòng thời gian. "
            "Ta ghép mọi hàng rào kỹ thuật đã học: chia tập theo thứ tự thời gian, cân bằng lớp, so sánh hai mô hình và kiểm thử suy luận dưới mức ba mươi giây."
        ),
        "svg_boxes": [("Chia thời gian 75% / 25%", "Quá khứ Train -> Tương lai Test"), ("Pipeline LR vs HistGB", "Đo PR-AUC & Brier Score"), ("Chốt ngưỡng & kiểm CPU", "Tất định, không rò rỉ")],
        "svg_say": (
            "Ba chặng liên hoàn dựng lên khung kiểm nghiệm chuẩn công nghiệp cho hệ thống phòng chống gian lận. "
            "Chặng đầu cắt dữ liệu thẳng theo trục thời gian để tập kiểm tra luôn nằm sau tập huấn luyện. "
            "Chặng hai đối đầu mô hình tuyến tính cân bằng lớp với bộ tăng cường độ dốc trên cùng bộ độ đo chuẩn."
        ),
        "hook_say": (
            "Đây là bài kiểm tra tổng hợp năng lực thiết kế hệ thống học máy từ A tới Z không sót bất kỳ lỗ hổng ngầm nào. "
            "Bỏ qua bất kỳ một trong ba chốt chặn gồm tách theo thời gian, dùng đúng thước đo lớp hiếm và giữ mọi tiền xử lý bên trong chuỗi khép kín sẽ làm dự án sụp đổ ngay khi lên sóng."
        ),
        "hook_txt": "Trên <b>1 000 giao dịch</b> theo dòng thời gian (<b>4% gian lận</b>): tách 750 đầu làm Train, 250 cuối làm Test. Chấm bằng <b>PR-AUC</b> và <b>Brier</b> thay cho Accuracy 96% ảo.",
        "hook_chk": ["750 + 250 == 1000", "1000 * 0.04 == 40.0"],
        "formula_txt": (
            "<p><b>1. Đường cơ sở vô dụng:</b> dự đoán toàn 0 trên 4% gian lận cho <code>Accuracy = <b>96%</b></code> nhưng <code>PR-AUC ≈ <b>0,04</b></code>.</p>"
            "<p><b>2. Bất biến triển khai:</b> thời gian chạy toàn bộ trên CPU <code>&lt;&lt; 30 s</code> và kết quả lặp lại <b>100%</b> với <code>random_state=42</code>.</p>"
        ),
        "formula_say": (
            "Hai bất biến định lượng chốt chặn cho cả hệ thống thực chiến được nêu rõ trên bảng. "
            "Thước đo chuẩn xác phủ ban đầu chỉ bằng không phẩy không bốn cho dự đoán mù, nên mọi mô hình tốt hơn sẽ vọt cao lên rõ rệt so với đường nền đó. "
            "Còn hạt giống cố định bảo đảm đồng nghiệp chạy lại trên máy khác cũng nhận ra đúng từng chữ số."
        ),
        "sym_rows": [
            ["<code>X_tr, X_te = X[:750], X[750:]</code>", "Cắt thẳng theo thứ tự thời gian, không xáo trộn shuffle"],
            ["<code>average_precision_score(y_te, p)</code>", "Thước đo chính PR-AUC không bị nhiễu bởi 96% giao dịch sạch"],
            ["<code>brier_score_loss(y_te, p)</code>", "Đánh giá sai số bình phương xác suất đầu ra"],
        ],
        "sym_say": (
            "Bảng ký hiệu liệt kê đúng ba câu lệnh chủ chốt cho vòng đánh giá cuối cùng. "
            "Phép cắt lát bảy trăm năm mươi mẫu đầu giữ nguyên dòng thời gian thực tế, "
            "còn hai hàm chấm điểm đo chất lượng xếp hạng cảnh báo và mức độ tin cậy của xác suất."
        ),
        "ex_code": (
            "from sklearn.datasets import make_classification\n"
            "from sklearn.pipeline import Pipeline\n"
            "from sklearn.preprocessing import StandardScaler as SS\n"
            "from sklearn.linear_model import LogisticRegression as LR\n"
            "from sklearn.ensemble import HistGradientBoostingClassifier as HGB\n"
            "from sklearn.metrics import average_precision_score as ap, brier_score_loss as br\n"
            "X, y = make_classification(1000, weights=[0.96, 0.04], n_informative=6, random_state=42)\n"
            "X_tr, X_te, y_tr, y_te = X[:750], X[750:], y[:750], y[750:]\n"
            "lr = Pipeline([('s', SS()), ('c', LR(class_weight='balanced', random_state=42))]).fit(X_tr, y_tr)\n"
            "gb = HGB(max_iter=50, learning_rate=0.1, random_state=42).fit(X_tr, y_tr)\n"
            "p_lr, p_gb = lr.predict_proba(X_te)[:, 1], gb.predict_proba(X_te)[:, 1]\n"
            "print(f'lr_pr={ap(y_te,p_lr):.3f} gb_pr={ap(y_te,p_gb):.3f}')\n"
            "print(f'gb_brier={br(y_te,p_gb):.3f} gb_beats_lr={int(ap(y_te,p_gb) > ap(y_te,p_lr))}')\n"
        ),
        "ex_say": (
            "Đoạn mã chạy trọn vẹn tình huống một nghìn giao dịch lệch bốn phần trăm gian lận theo đúng thứ tự thời gian. "
            "Ta đối chiếu trực tiếp chuỗi hồi quy cân bằng lớp với bộ tăng cường độ dốc năm mươi vòng trên cùng tập kiểm tra theo thời gian."
        ),
        "ex_out_say": (
            "Đầu ra chạy thật chứng minh bộ tăng cường độ dốc đạt diện tích đường cong chuẩn xác phủ vượt trội so với hồi quy tuyến tính lẫn đường nền ngẫu nhiên và giữ điểm số Brier cực thấp ngay trên CPU."
        ),
        "chk_code": (
            "from sklearn.datasets import make_classification\n"
            "from sklearn.metrics import average_precision_score\n"
            "_, y = make_classification(n_samples=1000, weights=[0.96, 0.04], n_informative=6, random_state=42)\n"
            "y_te = y[750:]\n"
            "base_pr = average_precision_score(y_te, [0.0] * len(y_te))\n"
            "print(f'test_pos={int(y_te.sum())} zero_baseline_pr={base_pr:.3f}')\n"
        ),
        "chk_say": (
            "Ở phép kiểm chứng đối chứng cuối cùng, ta tính điểm đường nền khi một mô hình ngây thơ trả về toàn số không trên đúng hai trăm năm mươi giao dịch kiểm tra cuối. "
            "So sánh con số đường nền này cho phép chứng minh mô hình huấn luyện thật mang lại giá trị thực sự."
        ),
        "chk_out_say": (
            "Kết quả khẳng định đường nền chỉ loanh quanh tỉ lệ dương tự nhiên khoảng bốn phần trăm, vì không có thông tin phân biệt nào để xếp hạng gian lận lên đầu."
        ),
        "quymo": [
            ("1 000 giao dịch CPU", "Train + Eval vài giây (<= 5 s)", "Lặp lại 100% cùng random_state=42"),
            ("1 000 000 giao dịch thật", "Chia cắt theo ngày + Pipeline + HistGB", "Giữ nguyên PR-AUC và Brier làm cổng CI trước deploy"),
            ("Sau khi lên sản xuất", "Theo dõi độ trôi dữ liệu & trễ ECE/Brier", "Kích hoạt huấn luyện lại khi phân phối lệch quá ngưỡng"),
        ],
        "quymo_say": (
            "Bảng quy mô khép lại toàn bộ vòng đời thực chiến từ tập mẫu nghìn dòng tới vận hành triệu giao dịch. "
            "Nhờ giữ nguyên hai độ đo chuẩn và cổng kiểm tra chống rò rỉ trong quy trình tích hợp liên tục, chất lượng mô hình luôn được bảo vệ lâu dài."
        ),
        "pitfalls": [
            "<b>Lỗi 1 (-30đ):</b> Dùng <code>train_test_split(shuffle=True)</code> cắt ngẫu nhiên giao dịch theo thời gian làm lộ tương lai.",
            "<b>Lỗi 2 (-20đ):</b> Báo cáo độ chính xác 96% làm tiêu chuẩn nghiệm thu trên tập chỉ có 4% gian lận.",
            "<b>Lỗi 3 (-10đ):</b> Không cố định hạt giống ngẫu nhiên khiến kết quả chấm tự động lệch qua từng lần chạy.",
        ],
        "pitfalls_say": (
            "Trước khi bắt tay hoàn thành bài thực hành cuối khoá, bạn rà kỹ ba sai lầm chí tử sau đây. "
            "Một là xáo trộn ngẫu nhiên làm rò rỉ thời gian, hai là lấy độ chính xác tổng thể chín mươi sáu phần trăm làm tiêu chí, "
            "và ba là quên đặt hạt giống cố định."
        ),
        "q_text": "<ol><li>Khi bảng dữ liệu theo ngày có 1 000 dòng, vì sao dùng lát cắt <code>[:750] / [750:]</code> thay vì <code>train_test_split</code> mặc định?</li><li>Trên tập 4% gian lận, dự đoán toàn 0 đạt Accuracy và PR-AUC cỡ bao nhiêu?</li></ol>",
        "q_say": "Mời bạn tự kiểm tra kiến thức tổng kết bằng hai câu hỏi cuối khoá. Câu một, vì sao dùng lát cắt theo thời gian thay cho hàm chia mặc định xáo trộn ngẫu nhiên? Câu hai, đoán toàn không trên tập bốn phần trăm gian lận cho độ chính xác và PR-AUC cỡ bao nhiêu? Bấm tạm dừng và trả lời.",
        "q_ans1": "Vì <code>train_test_split</code> mặc định có <code>shuffle=True</code> sẽ trộn giao dịch tương lai vào Train; cắt tuyến tính giữ nguyên thứ tự thời gian.",
        "q_ans1_say": "Đáp án câu một: vì hàm chia mặc định xáo trộn ngẫu nhiên khiến dữ liệu tương lai lọt vào quá khứ, còn cắt tuần tự bảo toàn tuyệt đối thứ tự thời gian.",
        "q_ans2": "<code>Accuracy ≈ <b>96%</b></code> nhưng <code>PR-AUC ≈ <b>0.04</b></code> (bằng tỉ lệ dương tự nhiên, vô dụng để phát hiện gian lận).",
        "q_ans2_say": "Đáp án câu hai: độ chính xác tới chín mươi sáu phần trăm nhưng diện tích chuẩn xác phủ chỉ vỏn vẹn quanh không phẩy không bốn.",
        "lab_de": (
            "# Lab MLP L13 — Tình huống chuyên gia: Phát hiện gian lận theo thời gian trên CPU\n\n"
            "Viết chương trình Python (chạy bằng `labs/.venv-ml` qua `cham.sh`): "
            "trên `make_classification(n_samples=1000, weights=[0.96, 0.04], n_informative=6, random_state=42)` cắt thời gian `[:750]` Train / `[750:]` Test, "
            "huấn luyện `HistGradientBoostingClassifier(max_iter=50, learning_rate=0.1, random_state=42)` và so sánh `PR-AUC` với đường nền `0.0`, in đúng 3 dòng:\n"
            "1. `test_n=250`\n2. `gb_pr_auc=...`\n3. `beats_baseline=1`\n\n"
            "Chấm tự động:\n```bash\nbash labs/cham.sh MLP L13 duong_dan/bai_cua_ban.py\n```"
        ),
        "lab_sol": (
            "from sklearn.datasets import make_classification\n"
            "from sklearn.ensemble import HistGradientBoostingClassifier\n"
            "from sklearn.metrics import average_precision_score\n"
            "X, y = make_classification(n_samples=1000, weights=[0.96, 0.04], n_informative=6, random_state=42)\n"
            "X_tr, X_te, y_tr, y_te = X[:750], X[750:], y[:750], y[750:]\n"
            "gb = HistGradientBoostingClassifier(max_iter=50, learning_rate=0.1, random_state=42).fit(X_tr, y_tr)\n"
            "p = gb.predict_proba(X_te)[:, 1]\n"
            "pr = average_precision_score(y_te, p)\n"
            "base = average_precision_score(y_te, [0.0] * len(y_te))\n"
            "print(f'test_n={len(y_te)}')\n"
            "print(f'gb_pr_auc={pr:.3f}')\n"
            "print(f'beats_baseline={int(pr > base)}')\n"
        ),
        "chain": ["Cắt thời gian 75/25", "HistGB + PR-AUC + Brier", "Tất định CPU <= 5 s"],
    },
]
