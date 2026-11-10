"""Sinh curriculum/jva.yaml từ lessons/jva/*.yaml (tiêu đề, mục tiêu) + ví dụ và `fix` viết tay dưới đây.
Chạy: .venv/Scripts/python audit/jva/gen_curriculum.py   (mỗi ví dụ dẫn mã VER JVA:Lxx có dòng rec trong audit/verify_plan_curricula.py;
bộ kiểm thật của khoá là audit/jva/verify_jva.py — chạy javac/java trên mọi chương trình trong bài)"""
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.stdout.reconfigure(encoding="utf-8")

EX = {
    "L00": "Năm lệnh in với 2 và 3: in 5, \"2 + 3\", Tong: 23, Tong: 5, 5 dong — dấu + gặp chuỗi là nối chữ, từ trái sang phải",
    "L01": "Ba lần chi lương 900 000 000 đồng cộng bằng int ra −1 594 967 296 (tràn số, 2 700 000 000 − 2^32); cộng bằng long ra đúng 2 700 000 000",
    "L02": "7 / 2 = 3, 7 % 2 = 1, (double) 7 / 2 = 3.5, −7 / 2 = −3, −7 % 2 = −1 (chia số nguyên của Java cắt về 0)",
    "L03": "Biểu phí minh hoạ ba bậc, thử ba số tiền ở biên; so sánh > với >= đổi bậc đúng ở số tiền biên",
    "L04": "Mười lần cộng 0,1 bằng double ra 0.9999999999999999; vòng lặp tháng viết thang < 12 chỉ chạy 11 tháng thay vì 12 (lệch một)",
    "L05": "Mảng 5 số dư: tổng, lớn nhất và vị trí; truy cập phần tử chỉ số 5 của mảng dài 5 ném ArrayIndexOutOfBoundsException",
    "L06": "Hàm nhận số nguyên không đổi được biến của người gọi; hàm nhận mảng đổi được phần tử của mảng gốc",
    "L07": "Hai tài khoản độc lập; rút quá số dư bị từ chối nên số dư không bao giờ âm",
    "L08": "Hai chuỗi giống chữ tạo riêng: so bằng == ra false, bằng equals ra true; định dạng 1234567 thành 1,234,567",
    "L09": "Integer so bằng ==: 127 ra true, 128 ra false (bộ nhớ đệm −128..127); đếm giao dịch theo loại bằng bản đồ",
    "L10": "Rút quá số dư ném ngoại lệ tự định nghĩa; khối finally chạy cả khi có lỗi lẫn khi không; dấu vết ngăn xếp chỉ đúng dòng gây lỗi",
    "L11": "Hai cách tính phí cài cùng một giao diện chạy qua một vòng lặp; hai bản ghi cùng giá trị thì equals ra true",
    "L12": "Sổ chuyển khoản 3 tài khoản: tổng tiền trước bằng tổng sau; lỗi chép nhầm biến bị bắt ngay bởi phép kiểm bất biến",
}
FIX = {
    "L00": "Biên dịch được chưa chắc chạy đúng: lỗi khi chạy (chia cho 0) chỉ lộ ra lúc chạy",
    "L01": "Không dùng double cho tiền; tổng tiền dùng long theo đơn vị đồng vì int tràn ở 2 147 483 647",
    "L02": "(double)(7 / 2) vẫn ra 3.0 vì phép chia số nguyên đã chạy trước khi ép kiểu",
    "L03": "Ranh giới bậc phí phải ghi rõ “từ” hay “trên”; kiểm ngay tại số biên",
    "L04": "Lệch một vòng là lỗi hay gặp của vòng lặp; đếm trước số lần bằng cuối − đầu + 1 và chọn đúng dấu < hay <=",
    "L05": "Gán b = a không sao chép mảng mà cho hai tên cùng trỏ một mảng",
    "L06": "Java luôn truyền theo giá trị; với mảng và đối tượng, giá trị được truyền là tham chiếu",
    "L07": "Trường để public cho phép phá bất biến; giữ private và kiểm điều kiện trong phương thức",
    "L08": "So nội dung chuỗi bằng equals, không bằng ==; viết hằng chuỗi đứng trước để tránh lỗi giá trị rỗng",
    "L09": "Số đã hộp hoá so bằng equals; không xoá phần tử trong vòng duyệt từng phần tử",
    "L10": "Khối bắt lỗi rỗng nuốt lỗi; bắt đúng loại ngoại lệ cần xử lý",
    "L11": "Ưu tiên giao diện hơn kế thừa sâu; đánh dấu @Override để trình biên dịch bắt sai tên",
    "L12": "Không sửa lỗi bằng cách nuốt ngoại lệ; kiểm bất biến sau mỗi thao tác chứ không chỉ cuối ngày",
}

HEAD = """# Giáo án Khoá JVA · Lập trình Java từ con số 0 (13 bài, 2026-11-08)
# Căn cứ phạm vi: rà soát 2026-11-08 (interview/HANDOVER_INTERVIEW.md Mục 10) — thư viện không có khoá lập trình nhập môn; người học mất gốc
#   vào thẳng BNK L00 (bộ nhớ Java) sẽ hụt. Khoá này dạy lập trình Java từ đầu và đứng trước BNK.
# Bộ kiểm độc lập: audit/jva/verify_jva.py biên dịch và chạy THẬT (javac/java, JDK 22 trên máy) mọi chương trình trong bài, so từng dòng in ra.
# Nguồn: The Java Language Specification (Java SE 21), Javadoc Java SE 21, dev.java/learn; mục cụ thể ghi trong `source` của từng bài.
course: JVA
profile: stem
status: active
lessons:
"""


def main():
    out = [HEAD.rstrip("\n")]
    files = sorted((ROOT / "lessons" / "jva").glob("L*.yaml"))
    prev = None
    for f in files:
        sp = yaml.safe_load(f.read_text(encoding="utf-8"))
        lid = sp["id"]
        title = re.sub(r"^Bài \d+ — ", "", sp["title"])
        block = {"id": lid, "title": title, "spec": f"lessons/jva/{f.name}", "requires": [prev] if prev else [],
                 "objectives": sp["objectives"], "example": f"{EX[lid]} (VER JVA:{lid})", "fix": [FIX[lid]]}
        out.append(yaml.dump([block], allow_unicode=True, sort_keys=False, width=1000).rstrip("\n"))
        prev = lid
    (ROOT / "curriculum" / "jva.yaml").write_text("\n".join(out) + "\n", encoding="utf-8", newline="\n")
    print("ghi curriculum/jva.yaml:", len(files), "bài")


main()
