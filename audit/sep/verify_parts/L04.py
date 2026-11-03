# SEP L04 — kiểm bằng bảng quy tắc mã hoá từ văn bản giấy phép và liệt kê cây phụ thuộc (khác `checks`: đếm chuỗi).
import itertools

RULE = {  # trích nghĩa vụ chính khi PHÂN PHỐI (convey), theo audit/sep/sources_L04.md
    "MIT": {"closed_ok": True, "notices": 1},
    "Apache-2.0": {"closed_ok": True, "notices": 1},     # bản giấy phép + NOTICE nếu có
    "GPL-3.0": {"closed_ok": False, "notices": 1},       # cả tác phẩm theo GPL khi kết hợp thành một chương trình
}


def audit(deps, distributes=True, combined=True):
    blockers = [d for d in deps if distributes and combined and not RULE[d]["closed_ok"]]
    notices = sum(RULE[d]["notices"] for d in deps if RULE[d]["closed_ok"])
    return blockers, notices


rec("L04a", audit(["MIT", "MIT", "Apache-2.0", "GPL-3.0"]) == (["GPL-3.0"], 3),
    "sản phẩm đóng cài máy khách: 1 gói chặn (GPL-3.0), 3 bản thông báo")
rec("L04b", audit(["MIT", "MIT", "Apache-2.0", "GPL-3.0"], distributes=False)[0] == []
    and audit(["MIT", "MIT", "Apache-2.0", "GPL-3.0"], combined=False)[0] == [],
    "chỉ chạy trên máy chủ (không convey) hoặc chỉ là “aggregate”: không gói nào chặn")
tree = {f"d{i}": [f"d{i}.{j}" for j in range(3)] for i in range(4)}
nodes = list(tree) + list(itertools.chain.from_iterable(tree.values()))
rec("L04c", len(nodes) == 16 and len(nodes) - len(tree) == 12, "cây 4 gói trực tiếp × 3 gói con: 16 gói phải kiểm, 12 gián tiếp")
rec("L04d", audit(["MIT"] * 3 + ["Apache-2.0"] * 2 + ["GPL-3.0"]) == (["GPL-3.0"], 5),
    "quiz: 3 MIT + 2 Apache → 5 bản thông báo; GPL-3.0 gọi trực tiếp → chặn mã đóng")
