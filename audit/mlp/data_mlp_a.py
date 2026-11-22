# -*- coding: utf-8 -*-
"""Đặc tả 7 bài đầu khoá MLP (L00..L06) — Học máy Thực hành trên CPU."""

LESSONS_A = [
    {
        "id": "L00",
        "fname": "L00_du_lieu_bang_chong_ro_ri.yaml",
        "title": "Bài 0 — Dữ liệu bảng & Pipeline chia Train/Val/Test chống rò rỉ",
        "assumes": [],
        "introduces": ["mlp_leakage", "mlp_pipeline"],
        "obj": [
            "Phân tích cấu trúc dữ liệu bảng và chia tách Train/Val/Test phân tầng",
            "Phát hiện sai số rò rỉ dữ liệu khi chuẩn hóa trước lúc chia tập",
            "Cài Pipeline StandardScaler + LogisticRegression bảo đảm khớp chỉ trên Train",
        ],
        "prereq": [
            ("Mảng số học hai chiều (PYT:L09)", "Ma trận X có n hàng mẫu và d cột đặc trưng"),
            ("Mạng đa tầng và lan truyền (CS115:L23)", "Thang đo đặc trưng lớn làm lệch bước tối ưu"),
            ("Bẫy thống kê gộp (MLP)", "Tính trung bình trên toàn bộ dữ liệu gây lộ thông tin tập kiểm tra"),
        ],
        "prereq_say": (
            "Chào bạn đến với khoá học máy thực hành trên dữ liệu bảng và chạy hoàn toàn trên CPU. "
            "Trước hết ta nối kiến thức ma trận hai chiều từ bài trước để tổ chức bảng đặc trưng X và nhãn y. "
            "Thứ hai, ta xử lý bẫy phổ biến nhất khi mới làm thực tế là rò rỉ dữ liệu qua bước chuẩn hóa sớm."
        ),
        "svg_boxes": [("Chia Train / Test", "Tách trước 80% / 20%"), ("Fit trên Train", "Lưu mean & std Train"), ("Transform Test", "Áp nguyên tham số cũ")],
        "svg_say": (
            "Nguyên tắc vàng chống rò rỉ dữ liệu gồm ba bước một chiều không bao giờ đảo ngược. "
            "Bước một tách riêng tập huấn luyện và tập kiểm tra ngay từ đầu. "
            "Bước hai chỉ học trung bình và độ lệch chuẩn trên phần huấn luyện, rồi mới biến đổi tập kiểm tra."
        ),
        "hook_say": (
            "Rò rỉ dữ liệu là khi thông tin phân phối của tập kiểm tra vô tình thấm ngược vào bước huấn luyện mô hình. "
            "Nếu bạn gọi bộ chuẩn hóa trên toàn bộ bảng dữ liệu rồi mới chia đôi, điểm số lúc thử nghiệm sẽ cao giả tạo vì mô hình đã nhìn trộm biên độ tương lai. "
            "Hôm nay ta dùng chuỗi xử lý khép kín để bảo đảm phần kiểm tra hoàn toàn vô hình khi khớp tham số."
        ),
        "hook_txt": "Chia <b>100 mẫu</b> tỉ lệ 80/20 có <code>80 mẫu Train</code> và <code>20 mẫu Test</code>. Khớp <b>Pipeline</b> giữ thống kê Test nằm ngoài lúc <code>fit()</code>, triệt tiêu hoàn toàn <b>rò rỉ dữ liệu</b> (độ lệch = <b>0</b>).",
        "hook_chk": ["80 + 20 == 100", "abs(0.0) < 1e-9"],
        "formula_txt": (
            "<p><b>1. Chuẩn hóa đúng (chỉ từ Train):</b> <code>z = (x - mean_train) / std_train</code>.</p>"
            "<p><b>2. Pipeline:</b> gói chuỗi biến đổi <code>fit_transform(X_train)</code> rồi <code>transform(X_test)</code> tự động trong một đối tượng.</p>"
        ),
        "formula_say": (
            "Trên màn hình là công thức chuẩn hóa đúng nguyên tắc tách biệt hoàn toàn giữa huấn luyện và kiểm tra. "
            "Ta định nghĩa rò rỉ dữ liệu là việc tính trung bình và độ lệch chuẩn bằng dữ liệu gộp chung cả hai tập. "
            "Còn Pipeline là chuỗi xử lý đóng gói hai bước khớp và biến đổi, giúp mọi thước đo chỉ học duy nhất trên phần huấn luyện."
        ),
        "sym_rows": [
            ["<code>train_test_split(X, y, stratify=y)</code>", "Chia giữ nguyên tỉ lệ nhãn ở hai tập, đặt random_state=42"],
            ["<code>StandardScaler()</code>", "Đưa mỗi cột về trung bình 0 và phương sai đơn vị"],
            ["<code>Pipeline([('sc', ...), ('clf', ...)])</code>", "Chuỗi xử lý khép kín fit từ Train và suy luận sang Test"],
            ["<code>mean_</code>", "Thuộc tính lưu vector trung bình cột đã học từ tập Train"],
        ],
        "sym_say": (
            "Bảng trên giải thích từng thành phần viết trong mã nguồn để bạn nhìn vào là đọc hiểu ngay. "
            "Hàm chia tách nhận thêm tham số giữ cân bằng tỉ lệ nhãn và hạt giống bốn hai để kết quả lặp lại y hệt nhau. "
            "Bộ chuẩn hóa đưa cột về cùng thang đo, còn đối tượng Pipeline xâu chuỗi gọn gàng hai bước ấy."
        ),
        "ex_code": (
            "from sklearn.datasets import make_classification\n"
            "from sklearn.model_selection import train_test_split\n"
            "from sklearn.preprocessing import StandardScaler\n"
            "from sklearn.linear_model import LogisticRegression\n"
            "from sklearn.pipeline import Pipeline\n"
            "X, y = make_classification(n_samples=120, n_features=4, random_state=42)\n"
            "X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.25, stratify=y, random_state=42)\n"
            "pipe = Pipeline([('sc', StandardScaler()), ('clf', LogisticRegression(random_state=42))])\n"
            "pipe.fit(X_tr, y_tr)\n"
            "print(f'tr_n={len(X_tr)} te_n={len(X_te)} acc={pipe.score(X_te, y_te):.3f}')\n"
        ),
        "ex_say": (
            "Đoạn mã tạo một trăm hai mươi mẫu chuẩn bằng hạt giống bốn hai, rồi tách chín mươi mẫu huấn luyện và ba mươi mẫu kiểm tra. "
            "Nhờ bọc bộ chuẩn hóa và hồi quy vào cùng một chuỗi khép kín, lời gọi khớp chỉ tiếp xúc đúng phần chín mươi mẫu đầu."
        ),
        "ex_out_say": (
            "Đầu ra chạy thật trên CPU xác nhận kích thước hai tập đúng chuẩn chín mươi và ba mươi. "
            "Độ chính xác kiểm tra phản ánh trung thực năng lực mô hình vì tập kiểm tra chưa từng tham gia bước tính thang đo."
        ),
        "chk_code": (
            "import numpy as np\n"
            "from sklearn.preprocessing import StandardScaler\n"
            "X_tr = np.array([[0.0], [2.0]]); X_te = np.array([[10.0]])\n"
            "sc_ok = StandardScaler().fit(X_tr)\n"
            "sc_leak = StandardScaler().fit(np.vstack([X_tr, X_te]))\n"
            "print(f'ok_mean={sc_ok.mean_[0]:.2f} leak_mean={sc_leak.mean_[0]:.2f}')\n"
        ),
        "chk_say": (
            "Để kiểm chứng tận mắt độ sai lệch khi làm ẩu, ta thử trên tập huấn luyện chỉ gồm hai số không và hai, còn tập kiểm tra chứa giá trị mười. "
            "Ta so sánh trung bình của bộ chuẩn hóa khớp sạch chỉ trên phần huấn luyện với bộ chuẩn hóa gộp chung cả hai tập."
        ),
        "chk_out_say": (
            "Kết quả đối chiếu tách bạch rất rõ giữa hai cách làm. "
            "Bộ sạch cho trung bình bằng một, còn bộ rò rỉ bị kéo vọt lên bốn phẩy không do giá trị mười từ tập kiểm tra đã lọt sang lúc khớp."
        ),
        "quymo": [
            ("120 mẫu thử nghiệm", "Chạy CPU < 20 ms", "Kiểm chứng nhanh quy trình tách sạch"),
            ("100 000 dòng sản xuất", "Lưu mean/std JSON < 1 KB", "Không cần nạp lại toàn tập Train khi suy luận"),
            ("10 triệu dòng dữ liệu lớn", "Rò rỉ ẩn nâng khống điểm Val", "Bọc toàn bộ tiền xử lý trong Pipeline ngay từ đầu"),
        ],
        "quymo_say": (
            "Khi mở rộng quy mô từ trăm dòng thử nghiệm lên trăm nghìn dòng ngoài thực tế, cấu trúc Pipeline phát huy giá trị kép. "
            "Mọi thống kê khớp chỉ gói gọn thành vài tham số nhẹ nên suy luận một dòng mới diễn ra tức thì mà không cần đọc lại dữ liệu cũ."
        ),
        "pitfalls": [
            "<b>Lỗi 1 (-30đ):</b> Gọi <code>StandardScaler().fit_transform(X)</code> trước <code>train_test_split</code>.",
            "<b>Lỗi 2 (-20đ):</b> Quên <code>stratify=y</code> làm một tập thiếu lớp khi mẫu ít hoặc lệch.",
            "<b>Lỗi 3 (-10đ):</b> Gọi lại <code>fit_transform(X_test)</code> thay vì <code>transform(X_test)</code> khi đánh giá.",
        ],
        "pitfalls_say": (
            "Hãy lưu ý ba sai lầm khiến điểm mô hình ngoài thực tế tụt sâu so với lúc thử nghiệm. "
            "Lỗi nặng nhất là gọi chuẩn hóa trước khi chia tập. "
            "Thứ hai là quên giữ nguyên tỉ lệ nhãn, và thứ ba là gọi nhầm lệnh khớp lại trên tập kiểm tra thay vì chỉ biến đổi."
        ),
        "q_text": "<ol><li>Khi tập Train là <code>[0, 2]</code> và Test là <code>[10]</code>, <code>mean_</code> hợp lệ bằng mấy?</li><li>Vì sao gọi <code>fit_transform</code> lên tập Test lại sai?</li></ol>",
        "q_say": "Bạn kiểm tra lại kiến thức bằng hai câu hỏi nhanh sau đây. Câu một, nếu tập huấn luyện là không và hai, tập kiểm tra là mười thì trung bình hợp lệ bằng mấy? Câu hai, vì sao gọi lệnh khớp lên tập kiểm tra lại sai? Bấm tạm dừng và trả lời.",
        "q_ans1": "Bằng <code><b>1.0</b></code> (trung bình của <code>[0, 2]</code>); tuyệt đối không tính phần tử <code>10</code> của Test.",
        "q_ans1_say": "Đáp án câu một: trung bình hợp lệ đúng bằng một, vì chỉ được tính trên hai giá trị không và hai của phần huấn luyện.",
        "q_ans2": "Vì <code>fit_transform</code> học mean và std mới ngay trên tập Test, phá hỏng quy chuẩn so sánh và rò rỉ dữ liệu.",
        "q_ans2_say": "Đáp án câu hai: vì nó tính lại trung bình và độ lệch chuẩn mới trên chính tập kiểm tra, làm hỏng thước đo đồng nhất và gây rò rỉ dữ liệu.",
        "lab_de": (
            "# Lab MLP L00 — Pipeline chống rò rỉ dữ liệu trên dữ liệu bảng\n\n"
            "Viết chương trình Python (chạy bằng `labs/.venv-ml` qua `cham.sh`): "
            "(1) dùng `make_classification(n_samples=120, n_features=4, random_state=42)` chia `test_size=0.25, stratify=y, random_state=42`; "
            "(2) chạy `Pipeline([('sc', StandardScaler()), ('clf', LogisticRegression(random_state=42))])`; "
            "(3) kiểm `mean_` khi không rò rỉ trên `[0.0, 2.0]` vs có rò rỉ với `[10.0]`, in đúng 3 dòng:\n"
            "1. `clean_mean=1.00`\n2. `leak_mean=4.00`\n3. `pipe_test_acc=...`\n\n"
            "Chấm tự động:\n```bash\nbash labs/cham.sh MLP L00 duong_dan/bai_cua_ban.py\n```"
        ),
        "lab_sol": (
            "import numpy as np\n"
            "from sklearn.datasets import make_classification\n"
            "from sklearn.model_selection import train_test_split\n"
            "from sklearn.preprocessing import StandardScaler\n"
            "from sklearn.linear_model import LogisticRegression\n"
            "from sklearn.pipeline import Pipeline\n"
            "X, y = make_classification(n_samples=120, n_features=4, random_state=42)\n"
            "X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.25, stratify=y, random_state=42)\n"
            "pipe = Pipeline([('sc', StandardScaler()), ('clf', LogisticRegression(random_state=42))])\n"
            "pipe.fit(X_tr, y_tr)\n"
            "m_ok = StandardScaler().fit(np.array([[0.0], [2.0]])).mean_[0]\n"
            "m_lk = StandardScaler().fit(np.array([[0.0], [2.0], [10.0]])).mean_[0]\n"
            "print(f'clean_mean={m_ok:.2f}')\n"
            "print(f'leak_mean={m_lk:.2f}')\n"
            "print(f'pipe_test_acc={pipe.score(X_te, y_te):.3f}')\n"
        ),
        "chain": ["Tách Train/Test trước", "Pipeline fit chỉ Train", "0 rò rỉ dữ liệu"],
    },
    {
        "id": "L01",
        "fname": "L01_tien_xu_ly_column_transformer.yaml",
        "title": "Bài 1 — Tiền xử lý cột số, phân loại & dữ liệu khuyết bằng ColumnTransformer",
        "assumes": ["mlp_leakage", "mlp_pipeline"],
        "introduces": [],
        "obj": [
            "Điền giá trị khuyết bằng trung vị SimpleImputer tách biệt theo tập huấn luyện",
            "Mã hóa biến phân loại rời rạc bằng OneHotEncoder bỏ qua nhãn lạ khi suy luận",
            "Ghép ColumnTransformer sạch nối tiếp với bộ phân loại trong một Pipeline duy nhất",
        ],
        "prereq": [
            ("Chuỗi xử lý Pipeline chống rò rỉ (MLP:L00)", "Chỉ học tham số biến đổi trên tập huấn luyện"),
            ("Dữ liệu bảng hỗn hợp thực tế", "Bảng thật vừa có cột số bị thiếu vừa có cột chữ như tỉnh thành"),
            ("Tách nhánh theo cột", "Cột số đi nhánh điền khuyết + chuẩn hóa, cột chữ đi nhánh mã hóa rời rạc"),
        ],
        "prereq_say": (
            "Tiếp nối nguyên tắc tách tập của bài không, bài này giải quyết bảng dữ liệu hỗn hợp ngoài đời thật. "
            "Một bảng giao dịch thường vừa thiếu vài ô số, vừa chứa cột chữ rời rạc như thành phố hay kênh thanh toán. "
            "Ta cần bộ biến đổi theo từng cột để mỗi kiểu dữ liệu đi đúng làn xử lý của nó."
        ),
        "svg_boxes": [("Cột số (NaN)", "SimpleImputer trung vị"), ("Cột phân loại", "OneHotEncoder an toàn"), ("Ghép ColumnTransformer", "Đưa vào mô hình chuẩn")],
        "svg_say": (
            "Sơ đồ chia bảng dữ liệu thành hai nhánh xử lý song song theo đúng kiểu từng cột. "
            "Nhánh cột số điền ô trống bằng trung vị của phần huấn luyện rồi chuẩn hóa thang đo. "
            "Nhánh cột phân loại chuyển chữ thành véc tơ nhị phân và bỏ qua an toàn khi gặp nhãn mới."
        ),
        "hook_say": (
            "Dịch vụ sản xuất rất dễ sập giữa chừng chỉ vì hai tình huống dữ liệu đời thường. "
            "Thứ nhất là một ô tuổi tác bị bỏ trống gây lỗi phép nhân ma trận, thứ hai là hôm nay khách hàng mới chọn một mã tỉnh chưa từng có trong tập huấn luyện. "
            "Hôm nay ta học cách chặn đứng cả hai lỗi đó trong một bộ biến đổi cột gọn sạch."
        ),
        "hook_txt": "Cột số <code>[10, 20, 30, NaN]</code> dùng trung vị Train = <b>20.0</b>. Còn cột nhãn lạ khi gặp giá trị mới dùng <code>handle_unknown='ignore'</code> giữ dịch vụ chạy <b>0 lỗi</b>.",
        "hook_chk": ["(10 + 20 + 30) / 3 == 20.0", "2 + 1 == 3"],
        "formula_txt": (
            "<p><b>1. Trung vị (median):</b> ít bị kéo lệch bởi giá trị ngoại lai hơn trung bình cộng.</p>"
            "<p><b>2. Mã hóa an toàn:</b> từ điển có <code>K</code> nhãn Train → véc tơ độ dài <code>K</code>; nhãn lạ biến thành toàn số <code>0</code>.</p>"
        ),
        "formula_say": (
            "Hai quy tắc toán học trên giúp đường ống tiền xử lý bền vững trước nhiễu và dữ liệu mới. "
            "Trung vị đứng yên khi có một vài giao dịch bất thường cực lớn, không bị kéo lệch như trung bình cộng. "
            "Còn mã hóa mã hóa nhị phân cấu hình bỏ qua nhãn lạ sẽ biến giá trị chưa thấy thành hàng số không thay vì ném ngoại lệ dừng chương trình."
        ),
        "sym_rows": [
            ["<code>SimpleImputer(strategy='median')</code>", "Điền giá trị thiếu bằng trung vị từng cột học từ Train"],
            ["<code>OneHotEncoder(handle_unknown='ignore')</code>", "Mã hóa cột chữ, trả toàn 0 nếu gặp nhãn lạ lúc Test"],
            ["<code>ColumnTransformer([('num', ...), ('cat', ...)])</code>", "Áp các nhánh tiền xử lý khác nhau lên từng nhóm cột"],
        ],
        "sym_say": (
            "Bảng trên liệt kê ba lớp thư viện chính xuất hiện trong đoạn mã xử lý hỗn hợp. "
            "Lớp điền khuyết nhận chiến lược trung vị, bộ mã hóa rời rạc bật cờ bỏ qua nhãn lạ. "
            "Cuối cùng bộ ghép cột định tuyến đúng từng nhóm chỉ số cột vào mỗi nhánh tương ứng."
        ),
        "ex_code": (
            "import numpy as np\n"
            "from sklearn.impute import SimpleImputer\n"
            "from sklearn.preprocessing import OneHotEncoder, StandardScaler\n"
            "from sklearn.compose import ColumnTransformer\n"
            "from sklearn.pipeline import Pipeline\n"
            "X_tr = np.array([[10.0,'hn'],[20.0,'sg'],[30.0,'hn'],[np.nan,'sg']], object)\n"
            "X_te = np.array([[np.nan,'dn']], object)\n"
            "num_p = Pipeline([('imp', SimpleImputer(strategy='median')), ('sc', StandardScaler())])\n"
            "ct = ColumnTransformer([('num', num_p, [0]), ('cat', OneHotEncoder(handle_unknown='ignore'), [1])])\n"
            "ct.fit(X_tr); out = ct.transform(X_te)\n"
            "m = ct.named_transformers_['num']['imp'].statistics_[0]\n"
            "print(f'med={m:.1f} shape={out.shape} cat={out[0,1:].tolist()}')\n"
        ),
        "ex_say": (
            "Đoạn mã minh họa bảng gồm hai cột: cột số có một ô trống và cột thành phố gồm Hà Nội với Sài Gòn. "
            "Ở tập kiểm tra ta đưa vào cả ô số bị trống lẫn mã Đà Nẵng chưa từng xuất hiện lúc huấn luyện."
        ),
        "ex_out_say": (
            "Kết quả chạy thật chứng minh hai cơ chế phòng thủ cùng hoạt động chính xác. "
            "Vì trung vị ba số mười, hai mươi, ba mươi là hai mươi nên ô trống được điền đúng hai mươi, còn mã Đà Nẵng cho ra hai số không an toàn."
        ),
        "chk_code": (
            "import numpy as np\n"
            "from sklearn.impute import SimpleImputer\n"
            "med = SimpleImputer(strategy='median').fit([[10.0], [20.0], [1000.0]]).statistics_[0]\n"
            "mean = SimpleImputer(strategy='mean').fit([[10.0], [20.0], [1000.0]]).statistics_[0]\n"
            "print(f'median={med:.1f} mean={mean:.1f}')\n"
        ),
        "chk_say": (
            "Ở phép kiểm chứng thứ hai, ta cố tình thêm một giá trị ngoại lai một nghìn vào bên cạnh mười và hai mươi. "
            "Ta so sánh kết quả điền khuyết giữa chiến lược trung vị và chiến lược trung bình cộng."
        ),
        "chk_out_say": (
            "Đầu ra xác nhận trung vị giữ vững ở mức hai mươi không hề bị ảnh hưởng, trong khi trung bình cộng nhảy vọt lên hơn ba trăm bốn mươi ba. "
            "Nhờ vậy chiến lược trung vị giúp bảo vệ tốt hơn khi cột số có giá trị đột biến."
        ),
        "quymo": [
            ("Bảng nhỏ 20 cột", "ColumnTransformer < 5 ms", "Dễ bảo trì từng cột số / chữ"),
            ("Bảng 100 cột + API thật", "Nhãn tỉnh/thiết bị mới xuất hiện mỗi tuần", "handle_unknown='ignore' giữ API uptime 100%"),
            ("Lô suy luận 50 000 dòng", "Khớp 1 lần lúc train, xuất sparse matrix", "Giảm bộ nhớ gấp nhiều lần cho cột chữ nhiều hạng mục"),
        ],
        "quymo_say": (
            "Bảng quy mô giải thích tầm quan trọng của hai tham số an toàn trên hệ thống sản xuất dài hạn. "
            "Mỗi tuần có mã chi nhánh hoặc thiết bị mới xuất hiện là chuyện bình thường nên bộ mã hóa bắt buộc phải bật chế độ bỏ qua nhãn lạ."
        ),
        "pitfalls": [
            "<b>Lỗi 1 (-30đ):</b> Gọi <code>fillna(df.median())</code> trên toàn bảng trước khi chia tập Train/Test.",
            "<b>Lỗi 2 (-20đ):</b> Để mặc định <code>handle_unknown='error'</code> khiến API vỡ ngoại lệ khi thấy danh mục mới.",
            "<b>Lỗi 3 (-10đ):</b> Dùng mã hóa nhãn số 1, 2, 3 cho biến danh mục không có thứ tự gây hiểu nhầm 3 > 1.",
        ],
        "pitfalls_say": (
            "Bạn tránh kỹ ba sai lầm rất hay gặp khi tiền xử lý bảng hỗn hợp. "
            "Lỗi một là điền giá trị thiếu trước lúc chia tập gây rò rỉ dữ liệu. "
            "Lỗi hai là quên đặt cờ bỏ qua nhãn lạ và lỗi ba là gán số thứ tự tuỳ tiện cho các nhãn không so sánh lớn bé."
        ),
        "q_text": "<ol><li>Với tập Train là <code>[10, 20, 1000]</code>, nên dùng <code>median</code> hay <code>mean</code> để ít lệch ngoại lai?</li><li><code>OneHotEncoder(handle_unknown='ignore')</code> trả về gì khi gặp nhãn chưa thấy lúc Train?</li></ol>",
        "q_say": "Mời bạn tự kiểm tra hiểu bài qua hai câu hỏi nhanh sau. Câu một, với tập huấn luyện mười, hai mươi và một nghìn, nên chọn trung vị hay trung bình để tránh nhiễu ngoại lai? Câu hai, bộ mã hóa rời rạc đặt cờ bỏ qua sẽ xuất gì khi gặp nhãn mới? Bấm tạm dừng và trả lời.",
        "q_ans1": "Nên dùng <code><b>median</b></code> (= 20.0) thay vì <code>mean</code> (= 343.3) vì ngoại lai kéo lệch trung bình cộng.",
        "q_ans1_say": "Đáp án câu một: chọn trung vị bằng hai mươi để không bị giá trị một nghìn kéo lệch gấp mười mấy lần.",
        "q_ans2": "Trả về véc tơ toàn số <code><b>0</b></code> đúng bằng chiều từ điển lúc Train, không gây sập chương trình.",
        "q_ans2_say": "Đáp án câu hai: nó xuất ra một hàng toàn số không có cùng số chiều đã học và tiếp tục chạy bình thường.",
        "lab_de": (
            "# Lab MLP L01 — ColumnTransformer điền khuyết trung vị & mã hóa bỏ qua nhãn lạ\n\n"
            "Viết chương trình Python (chạy bằng `labs/.venv-ml` qua `cham.sh`): "
            "cho Train `[[10.0,'hn'], [20.0,'sg'], [30.0,'hn'], [np.nan,'sg']]` và Test `[[np.nan,'dn']]`, "
            "dùng `ColumnTransformer` với `SimpleImputer(strategy='median')` cho cột `[0]` và `OneHotEncoder(handle_unknown='ignore')` cho cột `[1]`, "
            "in đúng 3 dòng:\n1. `train_median=20.0`\n2. `test_imputed_val=20.0`\n3. `unknown_ohe_sum=0`\n\n"
            "Chấm tự động:\n```bash\nbash labs/cham.sh MLP L01 duong_dan/bai_cua_ban.py\n```"
        ),
        "lab_sol": (
            "import numpy as np\n"
            "from sklearn.impute import SimpleImputer\n"
            "from sklearn.preprocessing import OneHotEncoder\n"
            "from sklearn.compose import ColumnTransformer\n"
            "X_tr = np.array([[10.0, 'hn'], [20.0, 'sg'], [30.0, 'hn'], [np.nan, 'sg']], dtype=object)\n"
            "X_te = np.array([[np.nan, 'dn']], dtype=object)\n"
            "ct = ColumnTransformer([('num', SimpleImputer(strategy='median'), [0]),\n"
            "                        ('cat', OneHotEncoder(handle_unknown='ignore'), [1])])\n"
            "ct.fit(X_tr); out = ct.transform(X_te)\n"
            "med = ct.named_transformers_['num'].statistics_[0]\n"
            "print(f'train_median={med:.1f}')\n"
            "print(f'test_imputed_val={float(out[0, 0]):.1f}')\n"
            "print(f'unknown_ohe_sum={int(sum(out[0, 1:]))}')\n"
        ),
        "chain": ["SimpleImputer trung vị", "OneHotEncoder an toàn", "ColumnTransformer chuẩn"],
    },
    {
        "id": "L02",
        "fname": "L02_hoi_quy_dieu_chuan_ridge_lasso.yaml",
        "title": "Bài 2 — Hồi quy tuyến tính có điều chuẩn Ridge & Lasso chống quá khớp",
        "assumes": ["mlp_leakage", "mlp_pipeline"],
        "introduces": [],
        "obj": [
            "Phân biệt hình phạt L2 (Ridge co nhỏ trọng số) và L1 (Lasso đưa hệ số về 0)",
            "Đo tác động của alpha lên sai số Train vs Test trên đặc trưng đa cộng tuyến",
            "Chọn mức điều chuẩn giữ sai số kiểm thử thấp và mô hình ổn định",
        ],
        "prereq": [
            ("Đường ống chuẩn hóa và chia tập (MLP:L00)", "Chuẩn hóa trước khi phạt để mọi cột công bằng"),
            ("Bài toán nhiều biến cộng tuyến", "Khi hai cột gần giống hệt nhau, trọng số chưa phạt dễ phình to trái dấu"),
            ("Điều chuẩn L2 và L1", "Phạt bình phương co nhỏ đồng đều; phạt trị tuyệt đối loại bỏ cột nhiễu"),
        ],
        "prereq_say": (
            "Bài hai đưa đường ống chuẩn hóa ở bài không vào xử lý bài toán hồi quy có nhiều cột dữ liệu thừa và tương quan lẫn nhau. "
            "Khi hai cột gần như lặp lại nhau, hồi quy thường rất dễ gán hệ số dương âm cực lớn triệt tiêu lẫn nhau khiến mô hình mất ổn định. "
            "Ta dùng hình phạt điều chuẩn để giữ trọng số gọn gàng."
        ),
        "svg_boxes": [("Ridge (phạt L2)", "Co nhỏ tất cả w, w != 0"), ("Lasso (phạt L1)", "Đẩy w cột nhiễu về đúng 0"), ("Chọn alpha tốt", "Giảm sai số trên tập Test")],
        "svg_say": (
            "Ba khối so sánh trực tiếp hiệu ứng hai loại hình phạt kinh điển trong học máy thực hành. "
            "Hình phạt bình phương co đều trọng số nhưng giữ lại toàn bộ cột. "
            "Còn hình phạt trị tuyệt đối cắt thẳng trọng số của các cột vô ích về đúng bằng không."
        ),
        "hook_say": (
            "Giả sử bạn dự báo giá nhà với hai mươi đặc trưng nhưng thực tế chỉ năm đặc trưng thật sự có tác dụng, còn mười lăm cột kia chỉ là nhiễu. "
            "Nếu chạy hồi quy thường, mô hình sẽ học thuộc cả nhiễu trên tập huấn luyện và dự báo sai nặng khi gặp nhà mới. "
            "Hôm nay ta dùng hai kỹ thuật điều chuẩn để khoá chặt độ lớn trọng số và lọc sạch cột nhiễu."
        ),
        "hook_txt": "Với hệ số phạt <code>alpha = 1.0</code>, <b>Ridge</b> co tổng bình phương trọng số nhỏ lại, còn <b>Lasso</b> cắt thưa bớt cột thừa về đúng <b>0.0</b> sau khi đi qua <code>StandardScaler</code>.",
        "hook_chk": ["0.0 + 0.0 == 0.0", "10.0 > 1.0"],
        "formula_txt": (
            "<p><b>1. Ridge (L2):</b> tối thiểu <code>||y - Xw||^2 + alpha * sum(w_j^2)</code>.</p>"
            "<p><b>2. Lasso (L1):</b> tối thiểu <code>||y - Xw||^2 + alpha * sum(|w_j|)</code> → tạo nghiệm thưa.</p>"
        ),
        "formula_say": (
            "Cả hai hàm mục tiêu đều cộng thêm phần phạt độ lớn trọng số nhân với siêu tham số điều chỉnh. "
            "Ở công thức thứ nhất, hình phạt bình phương kéo mạnh các trọng số quá lớn xuống nhanh. "
            "Ở công thức thứ hai, góc nhọn của hàm trị tuyệt đối khiến nhiều trọng số dừng ngay tại gốc tọa độ bằng không."
        ),
        "sym_rows": [
            ["<code>Ridge(alpha=1.0, random_state=42)</code>", "Hồi quy phạt L2 làm mượt và co nhỏ toàn bộ trọng số"],
            ["<code>Lasso(alpha=0.5, random_state=42)</code>", "Hồi quy phạt L1 tự động đẩy nhiều hệ số về 0"],
            ["<code>coef_</code>", "Mảng trọng số w đã khớp tương ứng với từng cột đặc trưng"],
        ],
        "sym_say": (
            "Bảng ký hiệu nêu hai lớp mô hình và thuộc tính đọc trọng số từ mã thực thi. "
            "Cả hai lớp đều nhận siêu tham số độ mạnh hình phạt và gắn được vào sau bộ chuẩn hóa trong chuỗi xử lý. "
            "Sau khi khớp xong, mảng trọng số cho phép kiểm đếm chính xác bao nhiêu cột bị đẩy về không."
        ),
        "ex_code": (
            "import numpy as np\n"
            "from sklearn.datasets import make_regression\n"
            "from sklearn.preprocessing import StandardScaler\n"
            "from sklearn.pipeline import Pipeline\n"
            "from sklearn.linear_model import Ridge, Lasso\n"
            "X, y = make_regression(n_samples=150, n_features=12, n_informative=4, noise=2.0, random_state=42)\n"
            "r = Pipeline([('sc', StandardScaler()), ('m', Ridge(alpha=10.0, random_state=42))]).fit(X, y)\n"
            "l = Pipeline([('sc', StandardScaler()), ('m', Lasso(alpha=2.0, random_state=42))]).fit(X, y)\n"
            "rz = int(np.sum(np.abs(r['m'].coef_) < 1e-6)); lz = int(np.sum(np.abs(l['m'].coef_) < 1e-6))\n"
            "print(f'ridge_zeros={rz} lasso_zeros={lz} l2_norm={np.linalg.norm(r[\"m\"].coef_):.2f}')\n"
        ),
        "ex_say": (
            "Đoạn mã sinh dữ liệu một trăm năm mươi mẫu gồm mười hai cột nhưng chỉ bốn cột mang thông tin thật. "
            "Ta bọc bộ chuẩn hóa cùng hai mô hình phạt mức mười và hai rồi đếm số hệ số tiến sát không."
        ),
        "ex_out_say": (
            "Kết quả chạy thật chứng minh sự khác biệt căn bản giữa hai loại hình phạt. "
            "Mô hình bình phương không cắt cột nào về không, trong khi mô hình trị tuyệt đối tự động đưa nhiều hệ số nhiễu về đúng không."
        ),
        "chk_code": (
            "import numpy as np\n"
            "from sklearn.datasets import make_regression\n"
            "from sklearn.linear_model import Ridge\n"
            "X, y = make_regression(n_samples=80, n_features=6, noise=3.0, random_state=42)\n"
            "n_low = np.linalg.norm(Ridge(alpha=0.1).fit(X, y).coef_)\n"
            "n_hi = np.linalg.norm(Ridge(alpha=100.0).fit(X, y).coef_)\n"
            "print(f'norm_a01={n_low:.2f} norm_a100={n_hi:.2f} shrunk={int(n_hi < n_low)}')\n"
        ),
        "chk_say": (
            "Để kiểm chứng tác động khi tăng hệ số phạt lên một nghìn lần, ta so sánh chuẩn véc tơ trọng số ở mức không phẩy một và mức một trăm. "
            "Vì mức phạt càng lớn thì chi phí giữ hệ số to càng đắt nên tổng độ lớn trọng số bắt buộc phải co lại."
        ),
        "chk_out_say": (
            "Đầu ra khẳng định tổng độ dài véc tơ trọng số giảm mạnh từ mức cao xuống rất nhỏ khi hệ số phạt tăng lên. "
            "Cờ kiểm tra trả về một đúng như kỳ vọng toán học."
        ),
        "quymo": [
            ("12 đặc trưng có 8 nhiễu", "Lasso đặt alpha vừa phải", "Giữ gọn chỉ vài đặc trưng chính"),
            ("10 000 đặc trưng văn bản", "Rất nhiều cột đa cộng tuyến", "Ridge/L2 giữ ổn định tốc độ huấn luyện"),
            ("Quên chuẩn hóa cột thu nhập (triệu)", "Cột thu nhập bị phạt nhẹ, cột tuổi phạt nặng", "Bắt buộc đặt StandardScaler trước Ridge/Lasso"),
        ],
        "quymo_say": (
            "Bảng quy mô cho thấy tiêu chí chọn loại hình phạt theo hình dạng bảng dữ liệu lớn. "
            "Khi có hàng vạn cột rời rạc tương quan, phạt bình phương chạy ổn định hơn, còn khi muốn lọc ra ít đặc trưng giải thích cho nghiệp vụ thì ưu tiên phạt trị tuyệt đối."
        ),
        "pitfalls": [
            "<b>Lỗi 1 (-30đ):</b> Dùng Ridge hoặc Lasso trên dữ liệu thô chưa đưa qua <code>StandardScaler</code>.",
            "<b>Lỗi 2 (-20đ):</b> Đặt <code>alpha</code> quá lớn khiến cả trọng số cột hữu ích bị ép về 0 gây dưới khớp.",
            "<b>Lỗi 3 (-10đ):</b> Nhầm lẫn rằng <code>Lasso</code> chỉ dùng cho phân loại trong khi nó là mô hình hồi quy.",
        ],
        "pitfalls_say": (
            "Bạn tránh ba cái bẫy sau khi áp dụng điều chuẩn tuyến tính trong bài làm. "
            "Sai lầm nặng nhất là quên chuẩn hóa thang đo làm hình phạt đối xử bất công giữa cột đơn vị nghìn và cột đơn vị một. "
            "Tiếp đến là tăng phạt quá mạnh gây dưới khớp toàn phần, và nhầm tên mô hình sang bài toán phân loại."
        ),
        "q_text": "<ol><li>Mô hình nào (<code>Ridge</code> hay <code>Lasso</code>) đưa hẳn trọng số nhiễu về đúng <code>0</code>?</li><li>Nếu quên chuẩn hóa cột đo bằng mét vs mi-li-mét, điều chuẩn bị lệch ra sao?</li></ol>",
        "q_say": "Hãy tự kiểm tra qua hai câu hỏi chốt bài ngay sau đây. Câu một, mô hình nào tự động đẩy hẳn trọng số cột nhiễu về đúng không? Câu hai, nếu quên chuẩn hóa hai cột lệch đơn vị mét và mi-li-mét thì hình phạt bị sai ở đâu? Bấm tạm dừng và trả lời.",
        "q_ans1": "<b>Lasso</b> (phạt L1 trị tuyệt đối) đẩy hệ số các đặc trưng yếu về đúng <code>0</code>.",
        "q_ans1_say": "Đáp án câu một: mô hình phạt trị tuyệt đối là Lasso mới đưa hẳn hệ số cột dư thừa về đúng không.",
        "q_ans2": "Cột có độ lớn số nhỏ (hoặc lớn khác nhau) chịu mức phạt không đồng đều vì hình phạt tính trực tiếp theo bình phương hoặc trị tuyệt đối của w.",
        "q_ans2_say": "Đáp án câu hai: hình phạt tính thẳng trên giá trị trọng số nên hai cột khác đơn vị sẽ bị phạt nặng nhẹ hoàn toàn mất cân xứng.",
        "lab_de": (
            "# Lab MLP L02 — Hồi quy có điều chuẩn Ridge & Lasso chống quá khớp\n\n"
            "Viết chương trình Python (chạy bằng `labs/.venv-ml` qua `cham.sh`): "
            "dùng `make_regression(n_samples=150, n_features=12, n_informative=4, noise=2.0, random_state=42)`, "
            "xây `Pipeline` có `StandardScaler()` cho `Ridge(alpha=10.0)` và `Lasso(alpha=2.0)`, "
            "kiểm chứng mức co độ dài `||w||` khi tăng alpha từ 0.1 lên 100.0, in đúng 3 dòng:\n"
            "1. `ridge_zero_coefs=...`\n2. `lasso_zero_coefs=...`\n3. `higher_alpha_shrinks=1`\n\n"
            "Chấm tự động:\n```bash\nbash labs/cham.sh MLP L02 duong_dan/bai_cua_ban.py\n```"
        ),
        "lab_sol": (
            "import numpy as np\n"
            "from sklearn.datasets import make_regression\n"
            "from sklearn.preprocessing import StandardScaler\n"
            "from sklearn.pipeline import Pipeline\n"
            "from sklearn.linear_model import Ridge, Lasso\n"
            "X, y = make_regression(n_samples=150, n_features=12, n_informative=4, noise=2.0, random_state=42)\n"
            "r10 = Pipeline([('sc', StandardScaler()), ('m', Ridge(alpha=10.0, random_state=42))]).fit(X, y)\n"
            "r100 = Pipeline([('sc', StandardScaler()), ('m', Ridge(alpha=100.0, random_state=42))]).fit(X, y)\n"
            "l2 = Pipeline([('sc', StandardScaler()), ('m', Lasso(alpha=2.0, random_state=42))]).fit(X, y)\n"
            "rz = int(np.sum(np.abs(r10['m'].coef_) < 1e-6))\n"
            "lz = int(np.sum(np.abs(l2['m'].coef_) < 1e-6))\n"
            "sh = int(np.linalg.norm(r100['m'].coef_) < np.linalg.norm(r10['m'].coef_))\n"
            "print(f'ridge_zero_coefs={rz}')\n"
            "print(f'lasso_zero_coefs={lz}')\n"
            "print(f'higher_alpha_shrinks={sh}')\n"
        ),
        "chain": ["Chuẩn hóa trước khi phạt", "Ridge L2 co mượt", "Lasso L1 chọn cột"],
    },
    {
        "id": "L03",
        "fname": "L03_phan_loai_nguong_pr.yaml",
        "title": "Bài 3 — Phân loại nhị phân, ngưỡng quyết định & cân bằng Precision–Recall",
        "assumes": ["mlp_leakage", "mlp_pipeline"],
        "introduces": [],
        "obj": [
            "Đọc đúng ma trận nhầm lẫn TP, FP, FN, TN và công thức Precision, Recall, F1",
            "Thay đổi ngưỡng phân loại p >= threshold thay vì mặc định 0.50 để đạt mục tiêu nghiệp vụ",
            "So sánh F1 khi giữ ngưỡng 0.50 so với ngưỡng tối ưu chi phí bỏ sót",
        ],
        "prereq": [
            ("Chuỗi phân loại tuyến tính (MLP:L00)", "Hồi quy logistic trả về xác suất p từ 0 đến 1"),
            ("Chi phí sai số bất đối xứng", "Bỏ sót ca bệnh hoặc gian lận đắt hơn gấp nhiều lần báo động nhầm"),
            ("Tách biệt mô hình và ngưỡng", "Thay đổi ngưỡng quyết định không cần huấn luyện lại trọng số"),
        ],
        "prereq_say": (
            "Bài ba chuyển sang bài toán phân loại nhị phân và trả lời câu hỏi quan trọng khi ra quyết định. "
            "Hồi quy logistic thực chất xuất ra một xác suất từ không tới một, còn hàm dự đoán mặc định chỉ là phép cắt ngang tại mức không phẩy năm. "
            "Khi chi phí bỏ sót đắt hơn báo động giả, ta phải dịch ngưỡng cắt cho đúng bài toán."
        ),
        "svg_boxes": [("predict_proba(X)[:, 1]", "Xác suất lớp dương p"), ("So ngưỡng p >= t", "t=0.50 vs t=0.30"), ("Đo P, R, F1", "Đánh đổi báo nhầm & bỏ sót")],
        "svg_say": (
            "Quy trình tách hai khâu rõ ràng giữa dự báo xác suất và ra quyết định nhị phân. "
            "Khâu một đọc xác suất dự báo của lớp dương từ mô hình đã huấn luyện. "
            "Khâu hai thử cắt ở các ngưỡng khác nhau để cân bằng giữa độ chuẩn xác và độ phủ."
        ),
        "hook_say": (
            "Một mô hình sàng lọc rủi ro có xác suất dự báo khá tốt nhưng vẫn làm mất nhiều tiền chỉ vì lập trình viên giữ nguyên hàm dự đoán mặc định cắt ở ngưỡng năm mươi phần trăm. "
            "Khi hạ ngưỡng xuống ba mươi phần trăm, số ca thật bị bỏ sót giảm rõ rệt mà không tốn thêm một giây huấn luyện nào. "
            "Hôm nay ta kiểm soát trực tiếp ngưỡng quyết định và ma trận nhầm lẫn."
        ),
        "hook_txt": "Đọc xác suất <code>p = predict_proba(X)[:, 1]</code> rồi áp ngưỡng tự chọn <code>(p >= t)</code>. Hạ <code>t</code> từ <b>0.50</b> xuống <b>0.30</b> luôn kéo độ phủ <code>Recall</code> tăng hoặc bằng, đổi lại có thể tăng báo nhầm.",
        "hook_chk": ["4 / 5 == 0.8", "2 * 0.8 * 0.6 / (0.8 + 0.6) > 0.68"],
        "formula_txt": (
            "<p><b>1. Precision =</b> <code>TP / (TP + FP)</code> (trong số báo dương, bao nhiêu thật); "
            "<b>Recall =</b> <code>TP / (TP + FN)</code> (trong số dương thật, bắt được bao nhiêu).</p>"
            "<p><b>2. F1 =</b> <code>2 * P * R / (P + R)</code> — trung bình điều hòa kéo về thước đo thấp hơn.</p>"
        ),
        "formula_say": (
            "Hai công thức độ chuẩn xác và độ phủ đặt cạnh nhau để kiểm soát cả hai loại sai sót. "
            "Độ chuẩn xác chia số bắt trúng cho tổng số máy báo động nên phản ánh độ sạch của cảnh báo. "
            "Còn độ phủ chia số bắt trúng cho tổng số ca dương thật nên đo khả năng không bỏ lọt lưới."
        ),
        "sym_rows": [
            ["<code>predict_proba(X)[:, 1]</code>", "Lấy cột xác suất rơi vào lớp 1 từ bộ phân loại"],
            ["<code>confusion_matrix(y, pred)</code>", "Trả ma trận 2x2 [[TN, FP], [FN, TP]] theo thứ tự nhãn"],
            ["<code>precision_score / recall_score / f1_score</code>", "Tính ba độ đo chất lượng từ nhãn thật và nhãn cắt theo ngưỡng"],
        ],
        "sym_say": (
            "Bảng ký hiệu tóm tắt cách lấy xác suất và tính bộ ba độ đo từ thư viện chuẩn. "
            "Cột thứ nhất của mảng xác suất tương ứng với lớp một tức lớp dương tính ta đang quan tâm. "
            "Còn hàm ma trận nhầm lẫn sắp xếp cố định bốn ô đúng âm, giả dương, giả âm và đúng dương."
        ),
        "ex_code": (
            "from sklearn.datasets import make_classification\n"
            "from sklearn.model_selection import train_test_split\n"
            "from sklearn.pipeline import Pipeline\n"
            "from sklearn.preprocessing import StandardScaler\n"
            "from sklearn.linear_model import LogisticRegression\n"
            "from sklearn.metrics import precision_score as P, recall_score as R, f1_score as F1\n"
            "X, y = make_classification(n_samples=240, n_features=6, class_sep=0.6, random_state=42)\n"
            "X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.25, stratify=y, random_state=42)\n"
            "pipe = Pipeline([('s', StandardScaler()), ('c', LogisticRegression(random_state=42))]).fit(X_tr, y_tr)\n"
            "p = pipe.predict_proba(X_te)[:, 1]\n"
            "for t in (0.50, 0.30):\n"
            "    pr = (p >= t).astype(int)\n"
            "    print(f't={t:.2f} P={P(y_te,pr):.3f} R={R(y_te,pr):.3f} F1={F1(y_te,pr):.3f}')\n"
        ),
        "ex_say": (
            "Đoạn mã huấn luyện chuỗi chuẩn hóa cộng hồi quy logistic trên một trăm tám mươi mẫu và chấm thử sáu mươi mẫu kiểm tra. "
            "Sau đó chỉ từ cùng một mảng xác suất đầu ra, ta so sánh bộ ba chỉ số tại hai ngưỡng không phẩy năm và không phẩy ba."
        ),
        "ex_out_say": (
            "Đầu ra chạy thật cho thấy khi giảm ngưỡng xuống không phẩy ba, độ phủ tăng vọt vì ít ca dương bị bỏ sót hơn. "
            "Ngược lại độ chuẩn xác giảm nhẹ do có thêm một số trường hợp ngưỡng ranh giới bị gán nhãn dương."
        ),
        "chk_code": (
            "from sklearn.metrics import confusion_matrix\n"
            "y_true = [0, 0, 1, 1, 1]; p = [0.20, 0.40, 0.35, 0.60, 0.80]\n"
            "tn5, fp5, fn5, tp5 = confusion_matrix(y_true, [int(x >= 0.5) for x in p]).ravel()\n"
            "tn3, fp3, fn3, tp3 = confusion_matrix(y_true, [int(x >= 0.3) for x in p]).ravel()\n"
            "print(f'at50_tp={tp5}_fn={fn5}_fp={fp5} at30_tp={tp3}_fn={fn3}_fp={fp3}')\n"
        ),
        "chk_say": (
            "Để kiểm tay từng ô của ma trận nhầm lẫn, ta xét năm mẫu nhỏ có sẵn xác suất dự báo. "
            "Ở ngưỡng không phẩy năm, điểm không phẩy ba lăm bị xếp vào âm tính giả, còn hạ xuống ngưỡng không phẩy ba thì bắt trúng thêm điểm đó nhưng đồng thời dính thêm một ca báo nhầm tại mức không phẩy bốn."
        ),
        "chk_out_say": (
            "Kết quả chạy kiểm chứng khớp tuyệt đối với phép đếm tay từng ô. "
            "Vì vậy mỗi khi điều chỉnh ngưỡng, số ca đúng dương luôn biến thiên cùng chiều hoặc giữ nguyên, kéo theo đánh đổi rõ giữa bỏ sót và báo nhầm."
        ),
        "quymo": [
            ("Ngưỡng cứng 0.50 mặc định", "Tối ưu độ chính xác 0-1 đối xứng", "Không phù hợp khi bỏ sót đắt hơn báo nhầm"),
            ("Điều chỉnh ngưỡng t trên tập Val", "Chỉnh 1 con số không cần train lại", "Cẩn thận: tuyệt đối không tìm t trên tập Test cuối"),
            ("Chi phí FN = 10 x FP", "Ưa ngưỡng thấp hơn (0.20 - 0.35)", "Giảm tổng thiệt hại tài chính trên thực tế"),
        ],
        "quymo_say": (
            "Bảng quy mô nhấn mạnh một nguyên tắc ranh giới chống rò rỉ dữ liệu khi chọn ngưỡng. "
            "Nếu tìm ngưỡng đẹp nhất trực tiếp trên tập kiểm tra cuối cùng thì vẫn là gian lận ngầm; ngưỡng phải chốt xong trên tập thẩm định trước."
        ),
        "pitfalls": [
            "<b>Lỗi 1 (-30đ):</b> Quét tìm ngưỡng tốt nhất trên tập Test cuối cùng gây rò rỉ gián tiếp.",
            "<b>Lỗi 2 (-20đ):</b> Gọi <code>predict()</code> thay vì <code>predict_proba()</code> làm mất xác suất để dịch ngưỡng.",
            "<b>Lỗi 3 (-10đ):</b> Đọc nhầm vị trí cột xác suất <code>[:, 0]</code> thay vì lớp dương <code>[:, 1]</code>.",
        ],
        "pitfalls_say": (
            "Bạn tránh ba lỗi thường gặp khi làm việc với ngưỡng phân loại sau đây. "
            "Một là tinh chỉnh ngưỡng ngay trên tập kiểm tra cuối, hai là chỉ gọi hàm dự đoán nhãn cứng nên mất xác suất, "
            "và ba là lấy nhầm cột xác suất của lớp không thay vì lớp một."
        ),
        "q_text": "<ol><li>Hạ ngưỡng quyết định từ <code>0.50</code> xuống <code>0.30</code> tác động thế nào tới số ca <code>Recall</code> và <code>FP</code>?</li><li>Có được tìm ngưỡng tối ưu trực tiếp trên tập Test cuối cùng không?</li></ol>",
        "q_say": "Mời bạn dừng hình trả lời hai câu hỏi ôn tập sau. Câu một, khi hạ ngưỡng cắt từ không phẩy năm xuống không phẩy ba thì độ phủ và số ca báo nhầm đổi theo chiều nào? Câu hai, có được chọn ngưỡng tối ưu trực tiếp trên tập kiểm tra cuối không? Bấm tạm dừng và trả lời.",
        "q_ans1": "<b>Recall</b> tăng (hoặc giữ nguyên vì ít <code>FN</code> hơn), đổi lại số ca báo nhầm <code><b>FP</b></code> có xu hướng tăng.",
        "q_ans1_say": "Đáp án câu một: độ phủ tăng lên vì bắt thêm ca dương, nhưng số báo động nhầm cũng có thể tăng lên.",
        "q_ans2": "<b>Không</b> — phải chọn ngưỡng trên tập Validation hoặc từ CV, rồi mới đo một lần cuối trên Test.",
        "q_ans2_say": "Đáp án câu hai: tuyệt đối không, ngưỡng phải được chọn trên tập thẩm định để giữ tập kiểm tra hoàn toàn sạch.",
        "lab_de": (
            "# Lab MLP L03 — Cân bằng ngưỡng Precision–Recall từ xác suất dự báo\n\n"
            "Viết chương trình Python (chạy bằng `labs/.venv-ml` qua `cham.sh`): "
            "huấn luyện `Pipeline` (`StandardScaler` + `LogisticRegression(random_state=42)`) trên `make_classification(n_samples=240, n_features=6, random_state=42)` chia 75/25 `stratify=y, random_state=42`, "
            "tính `Recall` tại ngưỡng `0.50` và `0.30`, in đúng 3 dòng:\n"
            "1. `r_at_50=...`\n2. `r_at_30=...`\n3. `recall_monotone_non_decreasing=1`\n\n"
            "Chấm tự động:\n```bash\nbash labs/cham.sh MLP L03 duong_dan/bai_cua_ban.py\n```"
        ),
        "lab_sol": (
            "from sklearn.datasets import make_classification\n"
            "from sklearn.model_selection import train_test_split\n"
            "from sklearn.pipeline import Pipeline\n"
            "from sklearn.preprocessing import StandardScaler\n"
            "from sklearn.linear_model import LogisticRegression\n"
            "from sklearn.metrics import recall_score\n"
            "X, y = make_classification(n_samples=240, n_features=6, random_state=42)\n"
            "X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.25, stratify=y, random_state=42)\n"
            "pipe = Pipeline([('sc', StandardScaler()), ('clf', LogisticRegression(random_state=42))]).fit(X_tr, y_tr)\n"
            "p = pipe.predict_proba(X_te)[:, 1]\n"
            "r50 = recall_score(y_te, (p >= 0.50).astype(int))\n"
            "r30 = recall_score(y_te, (p >= 0.30).astype(int))\n"
            "print(f'r_at_50={r50:.3f}')\n"
            "print(f'r_at_30={r30:.3f}')\n"
            "print(f'recall_monotone_non_decreasing={int(r30 >= r50)}')\n"
        ),
        "chain": ["Đọc xác suất lớp 1", "Đặt ngưỡng theo chi phí", "Giữ Test sạch khỏi chọn ngưỡng"],
    },
    {
        "id": "L04",
        "fname": "L04_kiem_chung_cheo_gridsearch.yaml",
        "title": "Bài 4 — Kiểm chứng chéo StratifiedKFold & tìm siêu tham số GridSearchCV",
        "assumes": ["mlp_leakage", "mlp_pipeline"],
        "introduces": [],
        "obj": [
            "Chia K phần phân tầng StratifiedKFold giữ nguyên tỉ lệ nhãn dương ở từng nếp",
            "Chạy GridSearchCV bọc quanh Pipeline tránh rò rỉ trong từng vòng chéo",
            "Đọc điểm trung bình và độ lệch chuẩn để không chọn cấu hình ăn may một lần chia",
        ],
        "prereq": [
            ("Rủi ro một lần chia cố định", "Một lần tách ngẫu nhiên nhỏ dễ đánh lừa điểm cao hay thấp do may mắn"),
            ("Chuỗi xử lý khép kín (MLP:L00)", "Đưa toàn bộ biến đổi vào Pipeline trước khi chạy vòng chéo"),
            ("Tìm kiếm lưới siêu tham số", "Thử đều các mức phạt C trên từng nếp và lấy trung bình"),
        ],
        "prereq_say": (
            "Khi tập dữ liệu chỉ có vài trăm tới vài nghìn dòng, một lần chia ngẫu nhiên duy nhất rất dễ cho kết quả may rủi. "
            "Bài bốn hướng dẫn cách kiểm chứng chéo năm nếp phân tầng kết hợp tìm kiếm lưới bọc bên ngoài chuỗi xử lý, "
            "giúp chọn siêu tham số chắc chắn mà không bao giờ gây rò rỉ dữ liệu giữa các nếp."
        ),
        "svg_boxes": [("Chia 5 nếp phân tầng", "Mỗi nếp giữ đúng tỉ lệ y"), ("Lồng Pipeline trong CV", "Fit scaler lại từng nếp"), ("Chọn best_params_", "Chấm 1 lần trên Test")],
        "svg_say": (
            "Luồng thực thi chuẩn mực gồm ba tầng bảo vệ tách biệt nhau. "
            "Tầng một chia phần huấn luyện thành năm nếp giữ nguyên tỉ lệ nhãn. "
            "Tầng hai đặt bộ chuẩn hóa vào trong chuỗi khép kín để lưới tìm kiếm tự khớp lại trên bốn nếp trước khi đo trên nếp thứ năm."
        ),
        "hook_say": (
            "Nhiều bạn hỏi vì sao phải đặt bộ chuẩn hóa bên trong Pipeline trước khi đưa vào hàm tìm kiếm lưới. "
            "Bởi nếu bạn chuẩn hóa toàn bộ tập huấn luyện trước, thì khi chia năm nếp, thông số trung bình của nếp kiểm chứng đã ngầm lọt vào bốn nếp huấn luyện còn lại. "
            "Hôm nay ta cài đặt lưới tìm kiếm lồng chuẩn xác và chạy toàn bộ trên CPU chỉ vài trăm mi-li-giây."
        ),
        "hook_txt": "Với <code>K = 5</code> nếp và lưới <b>4</b> ứng viên <code>C = [0.01, 0.1, 1.0, 10.0]</code>, <code>GridSearchCV</code> chạy đúng <code>5 × 4 = <b>20</b></code> lần khớp độc lập cộng <b>1</b> lần refit cuối.",
        "hook_chk": ["5 * 4 == 20", "20 + 1 == 21"],
        "formula_txt": (
            "<p><b>1. Tên tham số lưới Pipeline:</b> <code>'step_name__param'</code> (hai dấu gạch dưới <code>__</code>), ví dụ <code>'clf__C'</code>.</p>"
            "<p><b>2. Thống kê tổng hợp:</b> đọc <code>mean_test_score</code> kèm <code>std_test_score</code> qua K nếp.</p>"
        ),
        "formula_say": (
            "Quy ước cú pháp quan trọng nhất của lưới tìm kiếm bọc chuỗi khép kín là hai dấu gạch dưới. "
            "Nếu bước mô hình đặt tên tắt là clf, thì khoá tham số trong từ điển tìm kiếm phải viết đúng tên bước, hai dấu gạch dưới, rồi tới tên tham số. "
            "Khi đọc bảng kết quả, luôn nhìn cả điểm trung bình lẫn độ lệch chuẩn qua các nếp."
        ),
        "sym_rows": [
            ["<code>StratifiedKFold(n_splits=5, shuffle=True)</code>", "Chia 5 nếp phân tầng bảo toàn tỉ lệ lớp với random_state=42"],
            ["<code>GridSearchCV(pipe, {'clf__C': [...]})</code>", "Tìm lưới các ứng viên siêu tham số qua kiểm chứng chéo"],
            ["<code>best_score_ / best_params_</code>", "Điểm CV trung bình cao nhất và bộ siêu tham số tương ứng"],
        ],
        "sym_say": (
            "Bảng ký hiệu trình bày ba đối tượng điều phối quá trình tìm siêu tham số chuẩn xác. "
            "Bộ chia phân tầng gắn cờ xáo trộn với hạt giống bốn hai bảo đảm thứ tự mẫu không gây thiên vị nếp đầu nếp cuối. "
            "Còn đối tượng lưới tự động tìm cấu hình tốt nhất rồi huấn luyện lại trên toàn bộ phần huấn luyện."
        ),
        "ex_code": (
            "from sklearn.datasets import make_classification\n"
            "from sklearn.model_selection import train_test_split, StratifiedKFold, GridSearchCV\n"
            "from sklearn.pipeline import Pipeline\n"
            "from sklearn.preprocessing import StandardScaler\n"
            "from sklearn.linear_model import LogisticRegression\n"
            "X, y = make_classification(n_samples=300, n_features=8, random_state=42)\n"
            "X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)\n"
            "pipe = Pipeline([('sc', StandardScaler()), ('clf', LogisticRegression(random_state=42))])\n"
            "cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)\n"
            "gs = GridSearchCV(pipe, {'clf__C': [0.01, 0.1, 1.0, 10.0]}, cv=cv, scoring='f1')\n"
            "gs.fit(X_tr, y_tr)\n"
            "c = gs.best_params_['clf__C']\n"
            "print(f'best_C={c} cv_f1={gs.best_score_:.3f} te_f1={gs.score(X_te, y_te):.3f}')\n"
        ),
        "ex_say": (
            "Đoạn mã chạy lưới tìm kiếm bốn mức phạt C qua năm nếp phân tầng trên hai trăm bốn mươi mẫu huấn luyện. "
            "Sau hai mươi lần khớp nội bộ, nó tự chọn giá trị C tốt nhất, huấn luyện lại một mô hình sạch rồi chấm đúng một lần trên sáu mươi mẫu kiểm tra."
        ),
        "ex_out_say": (
            "Đầu ra xác nhận hệ thống chọn đúng siêu tham số tối ưu nhờ đánh giá chéo đầy đủ năm nếp thay vì đoán mò. "
            "Điểm trên tập kiểm tra độc lập nằm rất sát điểm trung bình kiểm chứng chéo nên không có dấu hiệu học vẹt."
        ),
        "chk_code": (
            "from sklearn.datasets import make_classification\n"
            "from sklearn.model_selection import StratifiedKFold\n"
            "X, y = make_classification(n_samples=100, weights=[0.8, 0.2], random_state=42)\n"
            "cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)\n"
            "cnts = [int(y[te].sum()) for _, te in cv.split(X, y)]\n"
            "print(f'pos_per_fold={cnts} same={int(len(set(cnts)) == 1)}')\n"
        ),
        "chk_say": (
            "Để kiểm chứng bộ chia phân tầng trên tập mất cân bằng hai mươi phần trăm nhãn dương, ta đếm số lượng mẫu dương lọt vào mỗi nếp. "
            "Tổng hai mươi ca dương chia đều năm nếp thì bắt buộc mỗi nếp phải nhận đúng bốn ca dương."
        ),
        "chk_out_say": (
            "Kết quả chạy thật trả về danh sách năm số bốn đều tăm tắp vì cơ chế phân tầng bảo toàn tỉ lệ chính xác qua từng nếp. "
            "Nhờ vậy không có nếp nào bị khuyết lớp thiểu số khi tính điểm."
        ),
        "quymo": [
            ("4 ứng viên x 5 nếp", "20 lần khớp (< 100 ms)", "Gọn nhẹ cho Logistic / Ridge"),
            ("1 000 tổ hợp siêu tham số", "20 000 lần khớp quá chậm", "Chuyển sang RandomizedSearchCV thử 30 điểm ngẫu nhiên"),
            ("Dữ liệu theo ngày tháng", "StratifiedKFold sẽ rò rỉ tương lai", "Phải thay bằng TimeSeriesSplit (sẽ học ở bài L08)"),
        ],
        "quymo_say": (
            "Bảng quy mô giúp bạn biết giới hạn thực tế của phương pháp vét lưới. "
            "Khi số lượng tham số nhân lên vài nghìn tổ hợp, hãy chuyển sang lấy mẫu ngẫu nhiên để giữ thời gian tìm kiếm trong ngưỡng chấp nhận được."
        ),
        "pitfalls": [
            "<b>Lỗi 1 (-30đ):</b> Chuẩn hóa <code>X_tr</code> bằng tay trước khi truyền vào <code>GridSearchCV</code> làm 5 nếp rò rỉ chéo nhau.",
            "<b>Lỗi 2 (-20đ):</b> Dùng khoá một gạch dưới <code>'clf_C'</code> thay vì hai gạch dưới <code>'clf__C'</code> gây ValueError.",
            "<b>Lỗi 3 (-10đ):</b> Đưa cả tập Test vào <code>GridSearchCV.fit(X, y)</code>.",
        ],
        "pitfalls_say": (
            "Ba lỗi kỹ thuật rất dễ mắc khi dùng tìm kiếm lưới trên thực tế gồm những điểm sau. "
            "Một là chuẩn hóa trước bên ngoài khiến các nếp nhìn trộm nhau, hai là gõ thiếu một dấu gạch dưới ở tên tham số, "
            "và ba là quên tách tập kiểm tra trước khi gọi hàm tìm lưới."
        ),
        "q_text": "<ol><li>Với 5 nếp và 4 giá trị <code>C</code>, <code>GridSearchCV</code> chạy bao nhiêu lần khớp (cộng refit)?</li><li>Tên tham số <code>C</code> của bước <code>clf</code> trong Pipeline viết trong lưới là gì?</li></ol>",
        "q_say": "Bạn kiểm tra lại kiến thức vừa học với hai câu hỏi ngắn. Câu một, với năm nếp và bốn mức C thì bộ tìm kiếm chạy bao nhiêu lần khớp tất cả? Câu hai, khoá từ điển để chỉnh tham số C của bước clf viết như thế nào? Bấm tạm dừng và trả lời.",
        "q_ans1": "<code>5 × 4 = <b>20</b></code> lần khớp đánh giá + <b>1</b> lần <code>refit</code> trên toàn tập Train = <b>21</b> lần.",
        "q_ans1_say": "Đáp án câu một: năm nhân bốn bằng hai mươi lần đánh giá cộng thêm một lần huấn luyện lại cuối là hai mốt lần.",
        "q_ans2": "Viết bằng hai dấu gạch dưới: <code><b>'clf__C'</b></code>.",
        "q_ans2_say": "Đáp án câu hai: ghép tên bước và tên tham số bằng hai dấu gạch dưới thành clf hai gạch dưới C.",
        "lab_de": (
            "# Lab MLP L04 — StratifiedKFold + GridSearchCV bọc quanh Pipeline\n\n"
            "Viết chương trình Python (chạy bằng `labs/.venv-ml` qua `cham.sh`): "
            "trên `make_classification(n_samples=300, n_features=8, random_state=42)` chia 80/20 `stratify=y, random_state=42`, "
            "chạy `GridSearchCV` 5-fold (`StratifiedKFold(n_splits=5, shuffle=True, random_state=42)`) cho `{'clf__C': [0.01, 0.1, 1.0, 10.0]}` scoring=`'f1'`, "
            "và kiểm đếm số mẫu dương trên từng fold của `y_train`, in đúng 3 dòng:\n"
            "1. `best_c=...`\n2. `cv_f1=...`\n3. `equal_folds_positive=...` (`1` nếu 5 fold có cùng số lượng dương tuyệt đối, `0` nếu chênh 1 mẫu do tổng số dương của `y_train` không chia hết cho 5)\n\n"
            "Chấm tự động:\n```bash\nbash labs/cham.sh MLP L04 duong_dan/bai_cua_ban.py\n```"
        ),
        "lab_sol": (
            "from sklearn.datasets import make_classification\n"
            "from sklearn.model_selection import train_test_split, StratifiedKFold, GridSearchCV\n"
            "from sklearn.pipeline import Pipeline\n"
            "from sklearn.preprocessing import StandardScaler\n"
            "from sklearn.linear_model import LogisticRegression\n"
            "X, y = make_classification(n_samples=300, n_features=8, random_state=42)\n"
            "X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)\n"
            "pipe = Pipeline([('sc', StandardScaler()), ('clf', LogisticRegression(random_state=42))])\n"
            "cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)\n"
            "gs = GridSearchCV(pipe, {'clf__C': [0.01, 0.1, 1.0, 10.0]}, cv=cv, scoring='f1').fit(X_tr, y_tr)\n"
            "cnts = [int(y_tr[te].sum()) for _, te in cv.split(X_tr, y_tr)]\n"
            "print(f'best_c={gs.best_params_[\"clf__C\"]}')\n"
            "print(f'cv_f1={gs.best_score_:.3f}')\n"
            "print(f'equal_folds_positive={int(len(set(cnts)) == 1)}')\n"
        ),
        "chain": ["Pipeline lồng trong CV", "StratifiedKFold đều lớp", "Ký hiệu __ chuẩn"],
    },
    {
        "id": "L05",
        "fname": "L05_lech_nhan_hieu_chuan_xac_suat.yaml",
        "title": "Bài 5 — Dữ liệu lệch nhãn 2% & hiệu chuẩn xác suất Brier Score",
        "assumes": ["mlp_leakage", "mlp_pipeline"],
        "introduces": [],
        "obj": [
            "Hiểu vì sao Accuracy đánh lừa trên dữ liệu lệch nhãn 98% âm – 2% dương",
            "Dùng trọng số lớp class_weight='balanced' và ưu tiên PR-AUC thay cho Accuracy",
            "Đo độ tin cậy xác suất thực tế bằng Brier score (càng gần 0 càng chuẩn)",
        ],
        "prereq": [
            ("Ma trận nhầm lẫn và độ phủ (MLP:L03)", "Nhìn Recall lớp hiếm thay vì tổng tỉ lệ đúng chung"),
            ("Bài toán thực tế lệch lớp", "Gian lận thẻ hay lỗi máy hiếm khi quá vài phần trăm dữ liệu"),
            ("Hiệu chuẩn xác suất dự báo", "Xác suất máy báo 0.8 phải tương ứng khoảng 80% ca thật"),
        ],
        "prereq_say": (
            "Trên thực tế sản xuất, hai lớp rất ít khi chia đôi năm mươi năm mươi như sách giáo khoa. "
            "Nếu giao dịch gian lận chỉ chiếm hai đến năm phần trăm, một mô hình lười biếng đoán toàn âm tính vẫn đạt độ chính xác chín mươi lăm phần trăm. "
            "Bài năm trang bị cách cân bằng trọng số và đo độ trung thực của xác suất."
        ),
        "svg_boxes": [("Dữ liệu lệch 95/5", "Accuracy 95% nhưng Recall = 0"), ("class_weight='balanced'", "Nhân phạt lớp hiếm x19"), ("PR-AUC & Brier Score", "Đo chất lượng xếp hạng & xác suất")],
        "svg_say": (
            "Sơ đồ chỉ ra ba điểm mấu chốt khi xử lý bảng dữ liệu mất cân bằng nhãn nghiêm trọng. "
            "Đầu tiên ta bỏ qua con số phần trăm đúng tổng thể dễ gây ảo giác. "
            "Sau đó dùng trọng số cân bằng lớp và đánh giá bằng diện tích đường cong chuẩn xác phủ cùng điểm số Brier."
        ),
        "hook_say": (
            "Một hệ thống phát hiện gian lận báo cáo độ chính xác chín mươi tám phần trăm khiến nhóm sản phẩm mừng thầm, cho tới khi kiểm tra lại thấy nó không bắt được ca gian lận nào cả. "
            "Bởi vì đơn giản chín mươi tám phần trăm giao dịch vốn là bình thường. "
            "Hôm nay ta sửa thẳng hàm mất mát bằng trọng số lớp và kiểm định độ trung thực xác suất."
        ),
        "hook_txt": "Trên 100 mẫu có <b>5 lớp dương</b> và <b>95 lớp âm</b>: mô hình đoán toàn 0 đạt <code>Accuracy = <b>95%</b></code> nhưng <code>Recall = <b>0.00</b></code>. Đặt <code>class_weight='balanced'</code> tăng trọng số lớp hiếm gấp <b>19 lần</b>.",
        "hook_chk": ["95 / 100 == 0.95", "95 / 5 == 19.0"],
        "formula_txt": (
            "<p><b>1. Trọng số cân bằng:</b> <code>w_c = N / (2 * N_c)</code> → lớp 5% được nhân phạt cao gấp 19 lần lớp 95%.</p>"
            "<p><b>2. Brier score:</b> <code>mean((p_i - y_i)^2)</code> — đo sai số bình phương giữa xác suất dự báo <code>p</code> và nhãn thật <code>y</code>.</p>"
        ),
        "formula_say": (
            "Hai công thức ngắn trên giải quyết trọn vẹn phần thuật toán và phần đánh giá hiệu chuẩn. "
            "Công thức một tính trọng số lớp tỉ lệ nghịch với tần suất xuất hiện, nên mỗi lỗi bỏ sót ca hiếm bị phạt nặng gấp mười chín lần. "
            "Công thức hai đo trung bình bình phương hiệu giữa xác suất dự báo và nhãn thực tế không một."
        ),
        "sym_rows": [
            ["<code>class_weight='balanced'</code>", "Tự động tăng hệ số phạt cho lớp ít mẫu trong hàm mất mát"],
            ["<code>average_precision_score(y, p)</code>", "Tính diện tích dưới đường cong chuẩn xác – độ phủ PR-AUC"],
            ["<code>brier_score_loss(y, p)</code>", "Đo độ tin cậy xác suất từ 0 (hoàn hảo) tới 1 (sai tuyệt đối)"],
        ],
        "sym_say": (
            "Bảng trên tóm lược ba công cụ thiết yếu cho bài toán lớp hiếm trong thư viện học máy. "
            "Tham số cân bằng trọng số đặt ngay trong bộ phân loại, hàm tính trung bình độ chuẩn xác đo diện tích dưới đường cong chuẩn xác phủ, "
            "và hàm mất mát Brier đánh giá sai lệch xác suất đầu ra."
        ),
        "ex_code": (
            "from sklearn.datasets import make_classification as mk\n"
            "from sklearn.model_selection import train_test_split as sp\n"
            "from sklearn.pipeline import Pipeline as P\n"
            "from sklearn.preprocessing import StandardScaler as SS\n"
            "from sklearn.linear_model import LogisticRegression as LR\n"
            "from sklearn.metrics import recall_score as rc\n"
            "from sklearn.metrics import average_precision_score as ap\n"
            "from sklearn.metrics import brier_score_loss as br\n"
            "X, y = mk(600, n_informative=4, weights=[0.95,0.05], random_state=42)\n"
            "Xa, Xb, ya, yb = sp(X, y, test_size=0.25, stratify=y, random_state=42)\n"
            "c0 = LR(random_state=42); cb = LR(class_weight='balanced', random_state=42)\n"
            "p0 = P([('s', SS()), ('c', c0)]).fit(Xa, ya)\n"
            "pb = P([('s', SS()), ('c', cb)]).fit(Xa, ya); pr = pb.predict_proba(Xb)[:, 1]\n"
            "print(f'raw_rec={rc(yb, p0.predict(Xb)):.3f} bal_rec={rc(yb, pb.predict(Xb)):.3f}')\n"
            "print(f'pr_auc={ap(yb, pr):.3f} brier={br(yb, pr):.3f}')\n"
        ),
        "ex_say": (
            "Đoạn mã tạo sáu trăm mẫu trong đó lớp dương chỉ chiếm năm phần trăm rồi so sánh trực tiếp hai phiên bản mô hình. "
            "Một bản giữ mặc định, còn bản thứ hai bật trọng số cân bằng để ép mô hình chú ý tới nhóm ít mẫu."
        ),
        "ex_out_say": (
            "Đầu ra thực tế cho thấy độ phủ lớp hiếm tăng nhảy vọt ngay khi bật chế độ cân bằng trọng số. "
            "Đồng thời ta ghi nhận điểm diện tích đường cong chuẩn xác phủ và điểm số hiệu chuẩn Brier để theo dõi song song."
        ),
        "chk_code": (
            "from sklearn.metrics import brier_score_loss\n"
            "y = [0, 0, 1, 1]\n"
            "b_good = brier_score_loss(y, [0.1, 0.1, 0.9, 0.9])\n"
            "b_bad = brier_score_loss(y, [0.4, 0.4, 0.4, 0.4])\n"
            "print(f'brier_good={b_good:.4f} brier_bad={b_bad:.4f} better={int(b_good < b_bad)}')\n"
        ),
        "chk_say": (
            "Để kiểm chứng ý nghĩa trực quan của điểm số Brier, ta so sánh dự báo tự tin đúng hướng với dự báo lấp lửng bằng không phẩy bốn trên bốn nhãn thật. "
            "Vì điểm Brier là bình phương sai lệch nên mô hình bám sát sự thật phải có con số nhỏ hơn rõ rệt."
        ),
        "chk_out_say": (
            "Kết quả tính ra không phẩy không một so với không phẩy hai sáu, chứng minh thước đo này phạt rất nặng các xác suất thiếu tự tin hoặc lệch hướng."
        ),
        "quymo": [
            ("Gian lận 2% trên 1 triệu đơn", "Accuracy 98% hoàn toàn vô nghĩa", "Ưu tiên PR-AUC và Recall tại K cảnh báo"),
            ("Dùng class_weight='balanced'", "Xác suất thô bị đẩy cao quanh 0.5", "Cần hiệu chuẩn lại (Platt / Isotonic) trước khi chốt"),
            ("Lệch cực đoan 0.1%", "Thiếu mẫu dương từng fold", "Giữ n_splits <= 5 khi chia phân tầng"),
        ],
        "quymo_say": (
            "Bảng quy mô cảnh báo một tác dụng phụ ít người để ý khi dùng trọng số cân bằng lớp. "
            "Việc nhân trọng số lên mười chín lần làm xác suất đầu ra thô bị đẩy lệch cao hơn tần suất tự nhiên thật, nên cần hiệu chuẩn lại nếu dùng con số xác suất làm đầu vào tính tiền rủi ro."
        ),
        "pitfalls": [
            "<b>Lỗi 1 (-30đ):</b> Chỉ báo cáo <code>Accuracy = 98%</code> trên tập lệch 2% mà không nhìn Precision hay Recall.",
            "<b>Lỗi 2 (-20đ):</b> Dùng thẳng xác suất của mô hình <code>class_weight='balanced'</code> làm xác suất thật mà không hiệu chuẩn.",
            "<b>Lỗi 3 (-10đ):</b> Chỉ nhìn ROC-AUC trên dữ liệu cực lệch vì ROC bị che mờ bởi lượng TN khổng lồ.",
        ],
        "pitfalls_say": (
            "Hãy tránh ba sai lầm kinh điển trong bài toán dữ liệu lệch nhãn sau đây. "
            "Một là khoe độ chính xác tổng thể chín mươi tám phần trăm che mất độ phủ bằng không. "
            "Hai là lấy thẳng xác suất sau cân bằng làm tỉ lệ thật, và ba là chỉ tin một mình chỉ số ROC AUC."
        ),
        "q_text": "<ol><li>Với tập 95% âm và 5% dương, nếu mô hình chỉ đoán toàn 0 thì Accuracy và Recall bằng bao nhiêu?</li><li>Brier score gần 0 hay gần 1 thì xác suất dự báo đáng tin cậy hơn?</li></ol>",
        "q_say": "Bạn dừng hình trả lời hai câu hỏi nhanh trước khi vào bài thực hành. Câu một, trên tập chín mươi lăm phần trăm âm và năm phần trăm dương, đoán toàn không cho độ chính xác và độ phủ bằng mấy? Câu hai, điểm Brier càng gần không hay gần một thì càng tốt? Bấm tạm dừng và trả lời.",
        "q_ans1": "<code>Accuracy = <b>95%</b></code> nhưng <code>Recall = <b>0.00</b></code> — hoàn toàn bỏ lọt toàn bộ lớp dương.",
        "q_ans1_say": "Đáp án câu một: độ chính xác tổng thể tới chín mươi lăm phần trăm nhưng độ phủ đúng bằng không.",
        "q_ans2": "Càng gần <code><b>0</b></code> càng tốt (0.000 là dự báo khớp tuyệt đối từng xác suất).",
        "q_ans2_say": "Đáp án câu hai: càng gần không càng chuẩn xác vì nó đo bình phương sai lệch giữa xác suất và nhãn thật.",
        "lab_de": (
            "# Lab MLP L05 — Xử lý lệch nhãn 5% & đo PR-AUC / Brier Score\n\n"
            "Viết chương trình Python (chạy bằng `labs/.venv-ml` qua `cham.sh`): "
            "trên `make_classification(n_samples=600, weights=[0.95, 0.05], n_informative=4, random_state=42)` chia 75/25 `stratify=y, random_state=42`, "
            "so sánh `LogisticRegression(random_state=42)` thường với `LogisticRegression(class_weight='balanced', random_state=42)` trong `Pipeline`, in đúng 3 dòng:\n"
            "1. `balanced_recall_ge_raw=1`\n2. `balanced_pr_auc=...`\n3. `balanced_brier=...`\n\n"
            "Chấm tự động:\n```bash\nbash labs/cham.sh MLP L05 duong_dan/bai_cua_ban.py\n```"
        ),
        "lab_sol": (
            "from sklearn.datasets import make_classification\n"
            "from sklearn.model_selection import train_test_split\n"
            "from sklearn.pipeline import Pipeline\n"
            "from sklearn.preprocessing import StandardScaler\n"
            "from sklearn.linear_model import LogisticRegression\n"
            "from sklearn.metrics import recall_score, average_precision_score, brier_score_loss\n"
            "X, y = make_classification(n_samples=600, weights=[0.95, 0.05], n_informative=4, random_state=42)\n"
            "X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.25, stratify=y, random_state=42)\n"
            "p0 = Pipeline([('s', StandardScaler()), ('c', LogisticRegression(random_state=42))]).fit(X_tr, y_tr)\n"
            "pb = Pipeline([('s', StandardScaler()), ('c', LogisticRegression(class_weight='balanced', random_state=42))]).fit(X_tr, y_tr)\n"
            "pr = pb.predict_proba(X_te)[:, 1]\n"
            "print(f'balanced_recall_ge_raw={int(recall_score(y_te, pb.predict(X_te)) >= recall_score(y_te, p0.predict(X_te)))}')\n"
            "print(f'balanced_pr_auc={average_precision_score(y_te, pr):.3f}')\n"
            "print(f'balanced_brier={brier_score_loss(y_te, pr):.3f}')\n"
        ),
        "chain": ["Không tin Accuracy khi lệch nhãn", "Dùng balanced + PR-AUC", "Kiểm Brier hiệu chuẩn"],
    },
    {
        "id": "L06",
        "fname": "L06_cay_quyet_dinh_rung_ngau_nhien.yaml",
        "title": "Bài 6 — Cây quyết định, Rừng ngẫu nhiên RandomForest & kiểm soát độ sâu",
        "assumes": ["mlp_leakage"],
        "introduces": [],
        "obj": [
            "Giải thích chia nhánh theo chỉ số bất thuần khiết Gini và giới hạn max_depth",
            "So sánh phương sai của một cây đơn lẻ quá sâu với Rừng ngẫu nhiên nhiều cây",
            "Rút trích feature_importances_ để kiểm tra cây có bám đặc trưng giả mạo không",
        ],
        "prereq": [
            ("Ranh giới phi tuyến dạng bậc thang", "Cây cắt trục tọa độ theo từng ngưỡng x_j <= t mà không cần chuẩn hóa thang đo"),
            ("Quá khớp của cây sâu", "Cây không giới hạn độ sâu thuộc lòng từng điểm nhiễu nên đạt Train 1.000"),
            ("Tập hợp nhiều cây (Bagging)", "Lấy phiếu bầu đa số của nhiều cây độc lập làm giảm mạnh phương sai"),
        ],
        "prereq_say": (
            "Từ mô hình tuyến tính, bài sáu mở sang họ mô hình cây quyết định vốn là xương sống cho dữ liệu bảng. "
            "Khác với hồi quy, một cây quyết định đơn lẻ học thuộc lòng dữ liệu rất nhanh nếu không bị chặn độ sâu. "
            "Giải pháp chuẩn là giới hạn độ sâu kết hợp trồng cả khu rừng ngẫu nhiên nhiều cây lấy phiếu chung."
        ),
        "svg_boxes": [("1 Cây sâu tự do", "Train=1.000 dễ học vẹt"), ("Rừng nhiều cây", "Chia tập con + cột ngẫu nhiên"), ("Bình chọn đa số", "Hạ phương sai trên tập Test")],
        "svg_say": (
            "Ba khối minh họa bước chuyển từ một cây đơn độc sang sức mạnh tập thể của rừng ngẫu nhiên. "
            "Một cây thả tự do sẽ chia vụn tới tận từng mẫu đơn lẻ. "
            "Khi gộp năm mươi cây trồng trên các mẫu rút ngẫu nhiên khác nhau, nhiễu cá biệt bị triệt tiêu đáng kể."
        ),
        "hook_say": (
            "Một cây quyết định không đặt ngưỡng độ sâu đạt điểm tuyệt đối một trăm phần trăm trên tập huấn luyện chỉ trong nháy mắt, nhưng vừa đưa sang dữ liệu mới liền tụt điểm thê thảm. "
            "Hôm nay ta thực nghiệm trực tiếp hiện tượng học vẹt đó và kiểm chứng hiệu quả hạ nhiệt của rừng ngẫu nhiên trên CPU."
        ),
        "hook_txt": "Chỉ số bất thuần khiết <b>Gini</b> đạt <code>0.0</code> khi nút chứa 100% cùng 1 lớp và đạt cực đại <code>0.5</code> khi chia 50/50. Đặt <code>max_depth=4</code> và gộp <b>50 cây</b> giữ ranh giới tổng quát hóa tốt hơn.",
        "hook_chk": ["1 - 0.5**2 - 0.5**2 == 0.5", "1 - 1.0**2 - 0.0**2 == 0.0"],
        "formula_txt": (
            "<p><b>1. Chỉ số Gini:</b> <code>G = 1 - sum(p_k^2)</code> (nút thuần nhất: <code>G = 0</code>; 2 lớp bằng nhau: <code>G = 0,5</code>).</p>"
            "<p><b>2. Rừng ngẫu nhiên:</b> trung bình dự đoán của <code>B</code> cây huấn luyện trên mẫu bootstrap và tập con đặc trưng.</p>"
        ),
        "formula_say": (
            "Mỗi nút trong cây tìm cách cắt làm sao cho tổng chỉ số bất thuần khiết của hai nhánh con giảm nhiều nhất có thể. "
            "Một nút toàn nhãn giống nhau có độ bất thuần khiết bằng không, còn trộn đều năm mươi năm mươi đạt cực đại không phẩy năm. "
            "Rừng ngẫu nhiên chỉ việc lấy trung bình xác suất của toàn bộ cây con để triệt tiêu dao động."
        ),
        "sym_rows": [
            ["<code>DecisionTreeClassifier(max_depth=...)</code>", "Cây quyết định giới hạn chiều sâu tối đa chống học vẹt"],
            ["<code>RandomForestClassifier(n_estimators=50)</code>", "Rừng gồm 50 cây độc lập bỏ phiếu chung kết quả"],
            ["<code>feature_importances_</code>", "Mảng tỉ trọng đóng góp giảm Gini của từng cột đặc trưng"],
        ],
        "sym_say": (
            "Bảng trên tóm tắt hai bộ phân loại họ cây cùng thuộc tính kiểm tra mức độ quan trọng của từng cột. "
            "Tham số chiều sâu tối đa khống chế số tầng rẽ nhánh, còn số cây trong rừng đặt mức năm mươi chạy cực nhanh trên CPU. "
            "Mảng tầm quan trọng đặc trưng luôn có tổng đúng bằng một."
        ),
        "ex_code": (
            "from sklearn.datasets import make_classification\n"
            "from sklearn.model_selection import train_test_split\n"
            "from sklearn.tree import DecisionTreeClassifier as DT\n"
            "from sklearn.ensemble import RandomForestClassifier as RF\n"
            "X, y = make_classification(n_samples=400, n_features=12,\n"
            "                           n_informative=4, random_state=42)\n"
            "X_tr, X_te, y_tr, y_te = train_test_split(\n"
            "    X, y, test_size=0.3, stratify=y, random_state=42)\n"
            "dt = DT(random_state=42).fit(X_tr, y_tr)\n"
            "rf = RF(n_estimators=50, max_depth=6, random_state=42).fit(X_tr, y_tr)\n"
            "print(f'dt_tr={dt.score(X_tr,y_tr):.3f} dt_te={dt.score(X_te,y_te):.3f}')\n"
            "imp = rf.feature_importances_.sum()\n"
            "print(f'rf_tr={rf.score(X_tr,y_tr):.3f} rf_te={rf.score(X_te,y_te):.3f} sum_imp={imp:.2f}')\n"
        ),
        "ex_say": (
            "Đoạn mã huấn luyện song song một cây thả tự do không giới hạn độ sâu và một rừng năm mươi cây giới hạn sáu tầng. "
            "Cả hai chạy trên bộ bốn trăm mẫu có tám cột nhiễu để lộ rõ hiện tượng quá khớp."
        ),
        "ex_out_say": (
            "Đầu ra chạy thật chứng minh cây sâu tự do đạt một trăm phần trăm trên tập huấn luyện nhưng tụt điểm rõ rệt ở tập kiểm tra. "
            "Nhờ gộp nhiều cây có độ sâu vừa phải, rừng ngẫu nhiên giữ khoảng cách huấn luyện và kiểm tra hẹp hơn hẳn."
        ),
        "chk_code": (
            "g_pure = 1.0 - (1.0**2 + 0.0**2)\n"
            "g_mix = 1.0 - (0.5**2 + 0.5**2)\n"
            "print(f'gini_pure={g_pure:.1f} gini_half={g_mix:.1f}')\n"
        ),
        "chk_say": (
            "Phép kiểm chứng thứ hai tính tay trực tiếp công thức độ bất thuần khiết tại hai nút cực trị. "
            "Một nút thuần nhất một trăm phần trăm cùng lớp và một nút chia đôi năm mươi phần trăm."
        ),
        "chk_out_say": (
            "Kết quả ra đúng không và không phẩy năm, vì công thức lấy một trừ tổng bình phương tỉ lệ hai lớp luôn nằm gọn trong đoạn từ không tới không phẩy năm."
        ),
        "quymo": [
            ("Bảng vừa < 100 000 dòng", "RandomForest 50-100 cây CPU < 1 s", "Ổn định, không cần chuẩn hóa thang đo"),
            ("Cột có 10 000 mã ID duy nhất", "Gini ưu tiên chọn nhầm cột ID chia vụn", "Bắt buộc loại bỏ cột ID trước khi trồng rừng"),
            ("Phân biệt rõ ranh giới mượt", "Cây chia bậc thang vuông góc kém mượt", "Kết hợp thử thêm Boosting hoặc hồi quy"),
        ],
        "quymo_say": (
            "Bảng quy mô cảnh báo bẫy đặc trưng mã định danh khi dùng cây quyết định. "
            "Chỉ số giảm bất thuần khiết rất thích các cột có nhiều giá trị rời rạc khác nhau như mã đơn hàng hay số điện thoại, nên phải lọc bỏ mọi cột định danh trước khi huấn luyện."
        ),
        "pitfalls": [
            "<b>Lỗi 1 (-30đ):</b> Để <code>max_depth=None</code> trên một cây đơn lẻ làm nhớ vẹt toàn bộ nhiễu Train.",
            "<b>Lỗi 2 (-20đ):</b> Đưa cột mã giao dịch ID vào huấn luyện vì độ quan trọng Gini thiên vị cột nhiều giá trị.",
            "<b>Lỗi 3 (-10đ):</b> Quên đặt <code>random_state=42</code> làm thứ tự rút mẫu ngẫu nhiên đổi kết quả mỗi lần chạy.",
        ],
        "pitfalls_say": (
            "Bạn tránh kỹ ba sai lầm phổ biến sau với mô hình cây và rừng ngẫu nhiên. "
            "Một là thả cây sâu tự do gây học vẹt tuyệt đối, hai là quên lọc cột mã định danh gây ảo giác quan trọng, "
            "và ba là bỏ trống hạt giống ngẫu nhiên khiến kết quả không tái lập được."
        ),
        "q_text": "<ol><li>Khi nút cây chứa 100% lớp 1 và 0% lớp 0, chỉ số Gini bằng mấy?</li><li>Vì sao Rừng ngẫu nhiên giảm được quá khớp so với một Cây đơn lẻ quá sâu?</li></ol>",
        "q_say": "Mời bạn tự kiểm tra hai câu hỏi ngắn của bài sáu. Câu một, một nút thuần nhất chỉ chứa toàn nhãn một có chỉ số bất thuần khiết bằng mấy? Câu hai, vì sao rừng ngẫu nhiên giảm quá khớp so với một cây đơn lẻ? Bấm tạm dừng và trả lời.",
        "q_ans1": "Bằng <code><b>0.0</b></code> (<code>1 - 1^2 - 0^2 = 0</code>).",
        "q_ans1_say": "Đáp án câu một: bằng không vì toàn bộ mẫu trong nút đều thuộc cùng một lớp.",
        "q_ans2": "Do lấy trung bình phiếu từ nhiều cây huấn luyện trên các tập con bootstrap và nhóm cột ngẫu nhiên, triệt tiêu nhiễu riêng của từng cây.",
        "q_ans2_say": "Đáp án câu hai: nhờ lấy trung bình nhiều cây học trên các phần dữ liệu rút khác nhau nên sai số ngẫu nhiên tự triệt tiêu lẫn nhau.",
        "lab_de": (
            "# Lab MLP L06 — Cây quyết định, Rừng ngẫu nhiên & chỉ số Gini\n\n"
            "Viết chương trình Python (chạy bằng `labs/.venv-ml` qua `cham.sh`): "
            "trên `make_classification(n_samples=400, n_features=12, n_informative=4, random_state=42)` chia 70/30 `stratify=y, random_state=42`, "
            "huấn luyện `DecisionTreeClassifier(random_state=42)` (không giới hạn sâu) và `RandomForestClassifier(n_estimators=50, max_depth=6, random_state=42)`, in đúng 3 dòng:\n"
            "1. `dt_train_acc=1.000`\n2. `rf_test_acc=...`\n3. `importances_sum=1.00`\n\n"
            "Chấm tự động:\n```bash\nbash labs/cham.sh MLP L06 duong_dan/bai_cua_ban.py\n```"
        ),
        "lab_sol": (
            "from sklearn.datasets import make_classification\n"
            "from sklearn.model_selection import train_test_split\n"
            "from sklearn.tree import DecisionTreeClassifier\n"
            "from sklearn.ensemble import RandomForestClassifier\n"
            "X, y = make_classification(n_samples=400, n_features=12, n_informative=4, random_state=42)\n"
            "X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, stratify=y, random_state=42)\n"
            "dt = DecisionTreeClassifier(random_state=42).fit(X_tr, y_tr)\n"
            "rf = RandomForestClassifier(n_estimators=50, max_depth=6, random_state=42).fit(X_tr, y_tr)\n"
            "print(f'dt_train_acc={dt.score(X_tr, y_tr):.3f}')\n"
            "print(f'rf_test_acc={rf.score(X_te, y_te):.3f}')\n"
            "print(f'importances_sum={rf.feature_importances_.sum():.2f}')\n"
        ),
        "chain": ["Cây sâu tự do dễ học vẹt", "RandomForest hạ phương sai", "Gini [0..0.5] & lọc cột ID"],
    },
]
