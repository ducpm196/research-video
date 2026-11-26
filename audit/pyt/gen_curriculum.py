"""Sinh curriculum/pyt.yaml từ lessons/pyt/*.yaml (tiêu đề, mục tiêu) + bảng example/fix/requires_ext dưới đây. Chạy SAU CÙNG (bẫy E37):
.venv/Scripts/python -B audit/pyt/gen_curriculum.py"""
import sys as _sys; from pathlib import Path as _P; _sys.path.insert(0, str(_P(__file__).resolve().parents[1])); import _frozen  # noqa: E402,F401
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.stdout.reconfigure(encoding="utf-8")

HEADER = """# Giáo án Khoá PYT · Python từ con số 0 (14 bài L00–L13, 2026-11-13)
# Căn cứ phạm vi (CITED = nguồn đã dùng khi soạn, tên đủ trong `source` từng bài; mọi trích dẫn tính từ trí nhớ ghi NOT_VERIFIED trong `source`): tài liệu chính thức của Python 3 (Tutorial, Language
#   Reference, Library Reference: dữ liệu, kiểu, luồng điều khiển, hàm, cấu trúc dữ liệu, chuỗi và `re`, `open`, `csv`, `json`, `pathlib`, lớp và `dataclasses`, ngoại lệ, `logging`, `venv`);
#   tài liệu pip (requirements file, pip freeze); tài liệu NumPy, pandas, Matplotlib, pytest (phiên bản ghim ở labs/requirements-py.txt); IEEE 754 (số thực dấu phẩy động); RFC 3629 (UTF-8), RFC 4180 (CSV), RFC 8259 (JSON).
# Vì sao cần: mọi khoá sau (BNX, PLC, SDP, ESY, DSC, AIF, LLM, MLP…) đọc và viết mã Python mà KHÔNG giảng cú pháp; FND dạy dòng lệnh, tệp, CSV/JSON/YAML, HTTP, SQL, Git nhưng không dạy ngôn ngữ lập trình nào.
#   PYT dạy lại từ con số 0 (mỗi khái niệm lập trình được giảng tại chỗ bằng Python, KHÔNG giả định đã học JVA/JV2: khoá sau Java cũng như trước Java đều phải đọc được PYT).
# Thứ tự học: sau FND (requires_ext FND:L04, FND:L05 cho L00; FND:L06 cho L05; FND:L04 cho L08), trước mọi khoá dùng Python.
# Môi trường (hợp đồng lab, labs/ENV.md): Python tối thiểu 3.11 (kho kiểm trên 3.11.9 và 3.13.5); L00–L08 và L12 chỉ cần thư viện chuẩn (L12 cần pytest); L09–L13 cần `pip install -r labs/requirements-py.txt`
#   (numpy 2.4.6, pandas 3.1.1, matplotlib 3.11.2, pytest 9.2.0; kiểm trên labs/.venv-pyt).
# Bộ kiểm độc lập: audit/pyt/verify_pyt.py chạy THẬT mọi chương trình trên Python 3.11 và 3.13 (so từng dòng, hai hạt giống băm), cửa sổ `>>>` bằng code.InteractiveConsole, phiên Git Bash, và phép đo thời gian/bộ nhớ
#   (audit/pyt/measured.json; số thời gian là số minh hoạ trên máy kiểm). Số trong `example` là số minh hoạ chạy thật bằng verify_pyt; chưa gắn mã "VER PYT:Lxx" vì audit/verify_plan_curricula.py chưa có dòng PYT.
# Phát âm: chỉ «Python» đọc được («Phai-thơn», 7/8, đối chứng 0/8; audit/pyt/probes/p1.md); numpy, pandas, matplotlib, pytest (≤ 4/8) không đọc trong lời — chỉ hiện trên màn hình.
"""

META = {
    "L00": dict(requires=[], requires_ext=["FND:L04", "FND:L05"],
                example="0.1 + 0.2 ra 0.30000000000000004; 12 000 000 × 0.072 ra 863 999.9999999999 (cắt phần lẻ mất 1 đồng); lãi 6% một năm cho 3 tháng trên 2 000 000 là 30 000; 10^15 + 0,1 − 10^15 ra 0,125 (số minh hoạ chạy thật bằng verify_pyt)",
                fix=["Số thực dấu phẩy động không biểu diễn chính xác 0,1; tiền đồng lưu bằng số nguyên và làm tròn một lần có quy tắc", "Lệnh nhập luôn trả về chuỗi, phép chia một dấu luôn ra số thực"]),
    "L01": dict(requires=["L00"], requires_ext=[],
                example="tổng 450 000 + 12 000 000 + 800 000 + 30 000 000 + 2 500 000 = 45 750 000 và 1 giao dịch từ 20 triệu trở lên; gửi 10 triệu lãi 0,5% mỗi tháng gấp đôi sau 139 tháng; thời gian vòng lặp tăng theo số lượt (đo ở 10^3, 10^6, 10^7; số minh hoạ)",
                fix=["Thứ tự các nhánh quyết định kết quả; vòng lặp điều kiện phải làm điều kiện tiến dần tới sai", "range dừng trước số cuối: lỗi lệch một"]),
    "L02": dict(requires=["L01"], requires_ext=[],
                example="thuế 10% của 2 000 000 là 200 000, tổng 2 200 000; thuế 8% cho 2 160 000; sửa công thức ở 100 nơi: khả năng bỏ sót ≥ 1 chỗ là 86,7% nếu mỗi chỗ quên 2% (giả định minh hoạ); chi phí một lần gọi hàm đo ở 10^6 và 10^7 lần (số minh hoạ)",
                fix=["Hàm không có return trả None dù đã in kết quả ra màn hình", "Gán vào biến trùng tên biến toàn cục trong hàm làm biến đó thành cục bộ"]),
    "L03": dict(requires=["L02"], requires_ext=[],
                example="đếm tần suất {'chuyen': 3, 'nap': 2, 'rut': 1}; gộp hai nguồn theo mã tài khoản (300 000 + 250 000 = 550 000); tra cứu trong danh sách 10^6 phần tử chậm hơn tập hợp hàng nghìn lần ở máy kiểm, ngoại suy 10^8 (số minh hoạ)",
                fix=["Gán một danh sách cho biến khác không tạo bản sao", "Xoá phần tử khi đang lặp qua chính danh sách làm bỏ sót phần tử"]),
    "L04": dict(requires=["L03"], requires_ext=[],
                example="dòng nhật ký 'GD#A0001 chuyen 500.000 VND' bóc ra mã A0001 và 500000; len('tiền') = 4 nhưng 6 byte UTF-8; mẫu (a+)+b trên chuỗi 25 ký tự mất cỡ giây, gấp đôi mỗi ký tự thêm (đo ở 17, 21, 25 ký tự; số minh hoạ)",
                fix=["Dấu .* tham lam lấy nhiều nhất có thể; thêm ? để lấy ít nhất", "Số kiểu Việt 1.250 máy đọc thành 1,25: bỏ dấu chấm ngăn hàng nghìn trước khi đổi kiểu"]),
    "L05": dict(requires=["L04"], requires_ext=["FND:L06"],
                example="tệp 'tiền mặt' + '2.000.000 đồng' có 24 ký tự nhưng 31 byte; tổng CSV 500 000 + 2 000 000 + 300 000 = 2 800 000; đọc cả tệp 10^6 dòng tốn bộ nhớ gấp hàng nghìn lần đọc từng dòng (đo; số minh hoạ)",
                fix=["Chế độ 'w' xoá tệp; muốn ghi tiếp dùng 'a'", "Luôn ghi encoding=\"utf-8\" khi mở tệp văn bản; ghi xong phải đóng tệp (dùng with)"]),
    "L06": dict(requires=["L05"], requires_ext=[],
                example="TaiKhoan nạp 500 000 vào 1 000 000, rút 2 000 000 bị từ chối, rút 300 000 còn 1 200 000; tiết kiệm lãi 5 phần nghìn cho 2 000 000 là 10 000; 10^6 đối tượng lớp thường chiếm khoảng 190 MB so với 160 MB cho bộ ba giá trị, hơn khoảng 20% (đo bằng tracemalloc, ngoại suy 10^8; số minh hoạ)",
                fix=["Danh sách đặt ở cấp lớp bị mọi đối tượng dùng chung; tạo trong hàm tạo", "Mặc định == chỉ hỏi cùng một đối tượng; so nội dung cần __eq__ hoặc lớp dữ liệu"]),
    "L07": dict(requires=["L06"], requires_ext=[],
                example="rút 250 000 từ 100 000 ném SoDuKhongDu 'thieu 150000'; finally in 'dong giao dich' ở cả hai lần gọi; try gần như miễn phí khi không có lỗi, đắt khi 50% dòng hỏng (đo trên 10^6 chuỗi; số minh hoạ)",
                fix=["except Exception: pass nuốt cả lỗi gõ sai tên biến và làm kết quả sai lặng lẽ", "Khối except bắt rộng đặt trước khối bắt hẹp thì khối hẹp không bao giờ chạy"]),
    "L08": dict(requires=["L07"], requires_ext=["FND:L04"],
                example="giao_dich.py chạy trực tiếp in __name__ = __main__, bị nạp in __name__ = giao_dich; tệp csv.py che bộ csv có sẵn; labs/requirements-py.txt 17 dòng ghim cho 4 thư viện chính; số thư viện phải cài khi thêm từng nhóm là 1, 4, 12, 17 và thời gian nạp riêng từng thư viện (đo; số minh hoạ)",
                fix=["Đặt tên tệp trùng bộ công cụ có sẵn (csv.py, random.py, traceback.py) làm nạp nhầm tệp của mình", "Quên kích hoạt môi trường ảo trước khi pip install làm cài nhầm vào Python hệ thống"]),
    "L09": dict(requires=["L08"], requires_ext=[],
                example="mảng 3×4 tiền: tổng theo trục 0 là [2200 2800 1350 2900], theo trục 1 là [2800 1650 4800], tổng chung 9250; độ lệch chuẩn của [2,4,4,4,5,5,7,9] là 2; cộng 10^6 số: mảng nhanh hơn vòng lặp hàng trăm lần, 10^8 số nguyên 8 byte là 800 MB (đo; số minh hoạ)",
                fix=["Hình dạng (3,4) và (3,) không lan truyền được: so kích thước từ bên phải", "Số nguyên 4 byte tràn không báo lỗi (2 000 000 000 + 2 000 000 000 ra số âm); cắt lát mảng là cái nhìn, không phải bản sao"]),
    "L10": dict(requires=["L09"], requires_ext=[],
                example="bảng 7 giao dịch: nhóm theo loại chuyển 1 450 000 / nạp 3 000 000 / rút 300 000; một ô thiếu làm tổng 4 750 000 chỉ của 6 giao dịch; mean chia 6 hay 7 tuỳ cách xử lý ô thiếu; 10^6 dòng bốn cột chiếm bộ nhớ cỡ trăm MB (cỡ 140 byte mỗi dòng), kiểu category giảm cỡ 7 lần ở cả 10^4 và 10^6 dòng (hệ số gần như không đổi theo số dòng; đo; số minh hoạ)",
                fix=["Nối điều kiện trên bảng bằng & và |, không bằng and/or", "Tổng và trung bình bỏ qua ô thiếu mà không báo; so ô thiếu bằng == luôn sai: dùng isna()"]),
    "L11": dict(requires=["L10"], requires_ext=[],
                example="cột 100 và 103: trục từ 0 cho tỉ lệ 1,03, trục từ 99 cho tỉ lệ nhìn thấy 4,0; kênh A hơn B ở mọi loại (90,0% / 33,3% so 88,9% / 20,0%) nhưng chung 39,0% so 82,0%; vẽ 10^6 điểm chồng thành một đám, tệp vector phình theo số điểm (đo; số minh hoạ)",
                fix=["Cột bắt đầu từ 0; cắt trục làm tỉ lệ nhìn thấy khác tỉ lệ thật", "Gộp mọi nhóm có thể đảo ngược kết luận; thang loga đọc như thang thường là hiểu sai"]),
    "L12": dict(requires=["L11"], requires_ext=[],
                example="phi_chuyen có 7 ca kiểm (2 + 5 ca biên); đổi < thành <= làm đúng 1 ca đỏ (50 000: mong 1 100, nhận 0); chạy 10^4 ca mất từ vài giây tới vài chục giây, chạy tay 30 giây mỗi ca mất cỡ 83 giờ (3,5 ngày) (đo; số minh hoạ)",
                fix=["Ca kiểm không có assert luôn xanh: cố ý làm hỏng mã để thử ca", "Giá trị mong đợi phải đến từ đặc tả hoặc tính tay, không từ công thức của mã"]),
    "L13": dict(requires=["L12"], requires_ext=[],
                example="tổng theo loại của tệp 8 dòng: chuyển 1 450 000, nạp 3 400 000, rút 550 000 (5 400 000); cả tệp 10^8 dòng cần cỡ chục GB bộ nhớ, từng dòng/từng khối không đổi (đo ở 10^3 và 10^6, ngoại suy; số minh hoạ); thang 10 điểm cho dự án nhỏ",
                fix=["Đọc theo khối phải cộng dồn kết quả các khối (gán đè chỉ còn khối cuối)", "Chỉ thống kê gộp được (tổng, đếm, nhỏ nhất, lớn nhất) mới cộng dồn theo khối; trung vị thì không"]),
}

lessons = []
for f in sorted((ROOT / "lessons" / "pyt").glob("L*.yaml")):
    d = yaml.safe_load(f.read_text(encoding="utf-8"))
    lid = d["id"]
    title = d["title"].split("—", 1)[1].strip()
    m = META[lid]
    item = {"id": lid, "title": title, "spec": f"lessons/pyt/{f.name}", "requires": m["requires"]}
    if m["requires_ext"]:
        item["requires_ext"] = m["requires_ext"]
    item["objectives"] = list(d["objectives"])
    item["example"] = m["example"]
    item["fix"] = m["fix"]
    lessons.append(item)
body = yaml.dump({"course": "PYT", "profile": "stem", "status": "active", "lessons": lessons}, allow_unicode=True, sort_keys=False, width=200)
(ROOT / "curriculum" / "pyt.yaml").write_text(HEADER + body, encoding="utf-8", newline="\n")
print("ghi curriculum/pyt.yaml:", len(lessons), "bài")
