"""BNX L01 — OpenAPI: kiểm yêu cầu theo lược đồ chuyển khoản, phân loại thay đổi hợp đồng. Chỉ thư viện chuẩn."""
import re as _re


def _ecma(pattern):
    r"""Mẫu của OpenAPI 3.0 theo kiểu ECMA 262: `$` (không multiline) là HẾT chuỗi. `$` của Python còn khớp trước một \n cuối
    chuỗi, nên đổi `$` ở cuối mẫu thành `\Z` (lỗi người đọc độc lập báo 2026-11-11: "0123456789\n" lọt)."""
    return pattern[:-1] + r"\Z" if pattern.endswith("$") and not pattern.endswith(r"\$") else pattern

# Lược đồ TransferRequest của bài (giống hằng SPEC_YAML ở audit/bnx/src/l01.py; ver/l01.py nạp YAML thật và đối chiếu)
BNX_L01_SCHEMA = {
    "type": "object",
    "required": ["fromAccount", "toAccount", "amount"],
    "properties": {
        "fromAccount": {"type": "string", "pattern": "^[0-9]{10,19}$"},
        "toAccount": {"type": "string", "pattern": "^[0-9]{10,19}$"},
        "amount": {"type": "integer", "minimum": 1},
    },
}

BNX_L01_REQS = [
    {"fromAccount": "0123456789", "toAccount": "9876543210", "amount": 500000},
    {"fromAccount": "0123456789", "toAccount": "9876543210", "amount": 0},
    {"fromAccount": "0123456789", "amount": 500000},
]


def bnx_oas_errors(req, schema=None):
    """Danh sách lỗi của một yêu cầu theo lược đồ (một phần JSON Schema mà OpenAPI 3.0 dùng: required, type, pattern, minimum).
    Mỗi lỗi là "tên_trường: lý do"."""
    s = schema or BNX_L01_SCHEMA
    err = []
    for f in s.get("required", []):
        if f not in req:
            err.append(f + ": thiếu")
    for f, p in s.get("properties", {}).items():
        if f not in req:
            continue
        v, t = req[f], p.get("type")
        if t == "string":
            if not isinstance(v, str):
                err.append(f + ": sai kiểu")
                continue
            if "pattern" in p and not _re.search(_ecma(p["pattern"]), v):
                err.append(f + ": sai dạng")
        elif t == "integer":
            if not isinstance(v, int) or isinstance(v, bool):
                err.append(f + ": sai kiểu")
                continue
            if "minimum" in p and v < p["minimum"]:
                err.append(f + ": nhỏ hơn " + str(p["minimum"]))
    return err


def bnx_oas_status(req, schema=None):
    """Mã trạng thái máy chủ trả khi bật kiểm lược đồ: 400 nếu có lỗi, 201 nếu hợp lệ (bỏ qua trùng khoá)."""
    return 400 if bnx_oas_errors(req, schema) else 201


def bnx_oas_batch():
    """Kết quả ba yêu cầu thử của bài: [(mã trạng thái, [lỗi])]."""
    return [(bnx_oas_status(r), bnx_oas_errors(r)) for r in BNX_L01_REQS]


def bnx_oas_change(old, new, side):
    """Phân loại một thay đổi lược đồ: 'tương thích' hoặc 'phá vỡ'.
    side='request': máy chủ mới phải nhận mọi yêu cầu cũ hợp lệ. side='response': máy khách cũ phải đọc được phản hồi mới.
    old/new: {"required": [...], "properties": {tên: {"type": ...}}}."""
    op, np_ = old.get("properties", {}), new.get("properties", {})
    oreq, nreq = set(old.get("required", [])), set(new.get("required", []))
    for f in op:
        if f not in np_:
            return "phá vỡ"              # xoá trường: bên còn dùng nó bị gãy
        if op[f].get("type") != np_[f].get("type"):
            return "phá vỡ"              # đổi kiểu
    if side == "request" and (nreq - oreq):
        return "phá vỡ"                  # yêu cầu cũ không có trường mới bắt buộc
    if side == "response" and (oreq - nreq):
        return "phá vỡ"                  # máy khách cũ trông vào trường luôn có
    return "tương thích"


def bnx_oas_old_valid_after(new_required, reqs=None):
    """Số yêu cầu cũ hợp lệ (theo lược đồ cũ) còn hợp lệ khi lược đồ yêu cầu thêm các trường bắt buộc new_required."""
    reqs = BNX_L01_REQS if reqs is None else reqs
    s = dict(BNX_L01_SCHEMA, required=BNX_L01_SCHEMA["required"] + list(new_required))
    return sum(1 for r in reqs if not bnx_oas_errors(r) and not bnx_oas_errors(r, s))


def bnx_oas_match(s, pattern="^[0-9]{10,19}$"):
    """Chuỗi có khớp mẫu số tài khoản của lược đồ không (re.search, như JSON Schema: mẫu không tự neo, nên ^…$ là cần)."""
    return isinstance(s, str) and _re.search(_ecma(pattern), s) is not None
