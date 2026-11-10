"""Sinh curriculum/bnk.yaml từ các bài lessons/bnk/*.yaml (tiêu đề, mục tiêu) + ví dụ và `fix` viết tay bên dưới.
Chạy: .venv/Scripts/python audit/bnk/gen_curriculum.py"""
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.stdout.reconfigure(encoding="utf-8")

EX = {
    "L01": ("Sáu đối tượng, gốc trỏ tới A; sống A, B, C và rác 3 đối tượng, dọn 300 byte (số minh hoạ); cộng 10 lần 0,1 bằng double ra 0.9999999999999999", "VER BNK:L01"),
    "L02": ("Số dư 100, nạp 50 và 30 cùng lúc: 6 cách xen kẽ cho 3 kết quả {130, 150, 180}; 10 000 yêu cầu chờ 0,1 giây với 200 luồng mất 5 giây", "VER BNK:L02"),
    "L03": ("Gọi ghi vết qua proxy mở 2 giao dịch, gọi thẳng this chỉ 1; giao dịch ngoài hỏng thì còn 1 dòng hay 0 dòng", "VER BNK:L03"),
    "L04": ("Số dư 2 000 000, chuyển 500 000, thử 3 lần: không khoá còn 500 000, có khoá còn 1 500 000; UNIQUE giữ 1 dòng", "VER BNK:L04"),
    "L05": ("10 000 000 dòng, mỗi nút 100 lối rẽ: 4 tầng, 5 lần đọc; sqlite báo SCAN hay SEARCH tuỳ chỉ mục và điều kiện", "VER BNK:L05"),
    "L06": ("Hai khoá, 4 cặp thứ tự, 2 cặp ngược nhau gây bế tắc; sắp thứ tự id tăng thì 0 bế tắc (mô phỏng; Oracle không chạy trên máy)", "VER BNK:L06"),
    "L07": ("Độ trễ trung bình 3 ms khi trúng 0,9 (tđệm 1 ms, tcsdl 20 ms); mã chặn khiến ghi cuối là B thay vì A", "VER BNK:L07"),
    "L08": ("6 phân vùng chia cho 3 và 2 bộ đọc; sập ở thông điệp 2: [1,1,2,1,1] hay [1,1,0,1,1] tuỳ thứ tự ghi nhớ", "VER BNK:L08"),
    "L09": ("Bước lỗi i thì nhật ký 2i + 1 dòng; sập giữa lưu và báo: 0 sự kiện không outbox, 1 sự kiện có outbox", "VER BNK:L09"),
    "L10": ("Chuyển 500 000 phí 5 500 (số minh hoạ): ba dòng tổng 0; bút toán đảo đưa số dư về 0, sổ có 6 dòng", "VER BNK:L10"),
    "L11": ("Phản hồi về theo thứ tự 2,0,1,4,3: ghép theo thứ tự đến đúng 0/5, theo mã tương quan 5/5; 44 trên 120 thứ tự không trùng vị trí nào", "VER BNK:L11"),
    "L12": ("Bản tin 0200 trường 2, 3, 4, 11: bản đồ 7020000000000000, dài 62 ký tự; đọc ngược khớp", "VER BNK:L12"),
    "L13": ("Hai sổ 5 mã: 3 khớp, 1 chỉ ngân hàng, 1 chỉ chuyển mạch, 1 lệch tiền (số minh hoạ); 6 mã khác nhau", "VER BNK:L13"),
    "L14": ("Khối PIN định dạng 0 của PIN thử 1234 và thẻ thử: 041225EEEEEEEEEE; đổi số tiền thì MAC đổi; Luhn của số thẻ thử", "VER BNK:L14"),
    "L15": ("Tình huống giả định: gửi 2 lần không khoá bị trừ dư 500 000; đối soát tìm 1 mã chỉ ở ngân hàng; bút toán đảo sửa", "VER BNK:L15"),
}
FIX = {
    "L01": "Rò rỉ bộ nhớ không phải “quên dọn” mà là “vẫn còn tham chiếu”; không dùng double cho tiền",
    "L02": "count += n không nguyên tử; luồng ảo giúp việc chờ, không làm CPU nhanh hơn",
    "L03": "Nhãn @Transactional chỉ có tác dụng khi lời gọi đi qua proxy; gọi this bỏ qua nhãn",
    "L04": "Thử lại sau hết giờ chờ chỉ an toàn khi có khoá lũy đẳng và ràng buộc UNIQUE ở cơ sở dữ liệu",
    "L05": "Có chỉ mục chưa chắc được dùng: bọc cột trong hàm hay bỏ cột đầu làm chỉ mục vô dụng; đọc kế hoạch thực thi",
    "L06": "SELECT thường của Oracle không khoá hàng; bế tắc chặn bằng thứ tự khoá, không bằng may rủi",
    "L07": "Khoá có hạn có thể bị hai người cùng giữ; tính đúng đắn do cơ sở dữ liệu bảo đảm, không do khoá Redis",
    "L08": "Kafka đúng một lần chỉ bao trùm việc trong Kafka; tác dụng phụ bên ngoài vẫn cần khử trùng",
    "L09": "SAGA không cô lập như giao dịch thường; bước bù phải lũy đẳng; ghi kép làm mất sự kiện",
    "L10": "Không sửa hay xoá dòng sổ cái; sửa bằng bút toán đảo; số dư là kết quả suy ra",
    "L11": "Phản hồi không về theo thứ tự gửi; hết giờ chờ là chưa biết, phải truy vấn trước khi gửi lại",
    "L12": "Mỗi mạng thanh toán có đặc tả riêng dù cùng ISO 8583; không ghi nguyên số thẻ vào nhật ký",
    "L13": "Ghép hai sổ theo mã tham chiếu, không theo số tiền; việc sửa sổ phải qua người duyệt",
    "L14": "Khoá không để trong mã nguồn; máy chủ tự kiểm điều kiện sinh trắc học; ranh giới ngưỡng theo văn bản hiện hành",
    "L15": "Chỉ kể sự cố thật của mình, số liệu có nguồn; bài này là tình huống giả định, không phải sự cố có thật",
}

HEAD = """# Giáo án Khoá BNK · Nền tảng Backend Ngân hàng cho người mất gốc (15 bài, 2026-11-07)
# Căn cứ phạm vi: khoảng trống đã đo ở interview/HANDOVER_INTERVIEW.md Mục 8 (CITED 2026-11-07): thư viện có 628 bài nền (toán, giải thuật, HĐH, mạng, CSDL, hệ phân tán) nhưng
#   không có bài về Spring Boot, PL/SQL và khoá hàng Oracle, luồng ảo Java 21, Redis, ISO 8583, NAPAS, T24. Khoá này lấp đúng các chủ đề phỏng vấn đó, bám 100 câu hỏi ở interview/06.
# Nguồn kiến thức bên ngoài: ghi trong trường `source` của từng bài; Oracle và T24 không có trên máy nên mô phỏng chỉ kiểm logic (NOT_VERIFIED cho cú pháp riêng).
# Thứ tự học: L00–L01 nền Java; L02–L03 dịch vụ web; L04–L06 dữ liệu và bộ đệm; L07–L08 hệ phân tán; L09–L13 nghiệp vụ ngân hàng; L14 tình huống.
course: BNK
profile: stem
status: active
lessons:
"""


def main():
    out = [HEAD.rstrip("\n")]
    files = sorted((ROOT / "lessons" / "bnk").glob("L*.yaml"))
    prev = None
    for f in files:
        sp = yaml.safe_load(f.read_text(encoding="utf-8"))
        lid = sp["id"]
        title = re.sub(r"^Bài \d+ — ", "", sp["title"])
        old = f"L{int(lid[1:]) + 1:02d}"   # EX/FIX viết theo số cũ L01..L15
        ex, ver = EX[old]
        block = {"id": lid, "title": title, "spec": f"lessons/bnk/{f.name}", "requires": [prev] if prev else []}
        if lid == "L00":  # 2026-11-08: người mất gốc học khoá JVA (lập trình Java từ con số 0) trước BNK
            block["requires_ext"] = ["JVA:L12"]
        block.update({"objectives": sp["objectives"], "example": f"{ex} (VER BNK:{lid})", "fix": [FIX[old]]})
        out.append(yaml.dump([block], allow_unicode=True, sort_keys=False, width=1000).rstrip("\n"))
        prev = lid
    (ROOT / "curriculum" / "bnk.yaml").write_text("\n".join(out) + "\n", encoding="utf-8", newline="\n")
    print("ghi curriculum/bnk.yaml:", len(files), "bài")


main()
