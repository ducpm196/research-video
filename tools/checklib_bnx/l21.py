"""BNX L21 — Hệ thống cho vay số: hàm tham chiếu cho `checks:` (chỉ thư viện chuẩn).
Mọi ngưỡng (tỉ lệ nghĩa vụ trả nợ trên thu nhập, điểm duyệt, trọng số thẻ điểm, số hồ sơ trên một thiết bị) là SỐ MINH HOẠ,
không phải chính sách của tổ chức nào. Nhóm nợ theo số ngày quá hạn: Thông tư 31/2024/TT-NHNN Điều 10 (audit/bnx/sources_l21.md [TT31])."""
import hashlib
from fractions import Fraction

_BNX21_FSM = {"NOP": ("CHAM_DIEM",), "CHAM_DIEM": ("THAM_DINH", "TU_CHOI"), "THAM_DINH": ("DUYET", "TU_CHOI", "XET_TAY"),
              "XET_TAY": ("DUYET", "TU_CHOI"), "DUYET": ("DA_KY",), "DA_KY": ("GIAI_NGAN",), "GIAI_NGAN": (), "TU_CHOI": ()}


def bnx_loan_path_ok(path):
    """Dãy trạng thái hồ sơ có hợp lệ không (mỗi bước phải là một cạnh của máy trạng thái). Trả (hợp lệ?, chỉ số bước sai hoặc -1)."""
    for i in range(len(path) - 1):
        if path[i + 1] not in _BNX21_FSM.get(path[i], ()):
            return False, i
    return True, -1


def bnx_dti(income, paying, new):
    """Tỉ lệ nghĩa vụ trả nợ hằng tháng trên thu nhập, dạng phân số chính xác của phần trăm."""
    return Fraction((paying + new) * 100, income)


def bnx_dti_pass(income, paying, new, limit_pct=50):
    """Qua khi tỉ lệ không vượt ngưỡng (so bằng phép nhân chéo, không làm tròn)."""
    return (paying + new) * 100 <= limit_pct * income


def bnx_max_new_payment(income, paying, limit_pct=50):
    """Khoản trả mới lớn nhất (đồng, số nguyên) để tỉ lệ không vượt ngưỡng."""
    return max(0, limit_pct * income // 100 - paying)


def bnx_debt_group(days):
    """Nhóm nợ theo số ngày quá hạn (phần định lượng): dưới 10 → 1; 10–90 → 2; 91–180 → 3; 181–360 → 4; trên 360 → 5."""
    if days < 10:
        return 1
    if days <= 90:
        return 2
    if days <= 180:
        return 3
    if days <= 360:
        return 4
    return 5


def bnx_scorecard(income, group, months):
    """Thẻ điểm minh hoạ ba đặc trưng. Trả (điểm thu nhập, điểm lịch sử trả nợ, điểm thâm niên, tổng)."""
    d1 = 35 if income >= 15_000_000 else 20
    d2 = 25 if group == 1 else 0
    d3 = 20 if months >= 24 else 10
    return d1, d2, d3, d1 + d2 + d3


def bnx_underwrite(income, paying, new, group, months, dti_limit=50, score_limit=70):
    """Bộ máy quyết định minh hoạ: nhóm nợ từ 2 → XET_TAY; tỉ lệ vượt ngưỡng hoặc điểm dưới ngưỡng → TU_CHOI; còn lại DUYET."""
    total = bnx_scorecard(income, group, months)[3]
    if group >= 2:
        return "XET_TAY"
    if not bnx_dti_pass(income, paying, new, dti_limit) or total < score_limit:
        return "TU_CHOI"
    return "DUYET"


def bnx_sha256_hex(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def bnx_hex_diff(a, b):
    """Số vị trí khác nhau giữa hai chuỗi cùng độ dài."""
    return sum(1 for x, y in zip(a, b) if x != y)


def bnx_ofs_fields(msg):
    """Tách phần dữ liệu của bản tin mẫu `ỨNG.DỤNG,TUỲ.CHỌN,NGƯỜI.DÙNG,MÃ,TRƯỜNG:MV:SV=GIÁ TRỊ,…`.
    Trả {tên trường: {(mv, sv): giá trị}}."""
    res = {}
    for part in msg.split(",")[4:]:
        left, _, val = part.partition("=")
        name, mv, sv = left.split(":")
        res.setdefault(name, {})[(int(mv), int(sv))] = val
    return res


def bnx_device_fp(dev):
    """Dấu vân tay thiết bị minh hoạ: 12 ký tự đầu của SHA-256 trên các thuộc tính nối bằng “|” theo thứ tự tên khoá."""
    return hashlib.sha256("|".join(dev[k] for k in sorted(dev)).encode()).hexdigest()[:12]


def bnx_fp_counts(apps):
    """apps: [(mã hồ sơ, giấy tờ, thiết bị)]. Trả {dấu vân tay: số giấy tờ khác nhau}."""
    seen = {}
    for _, doc, dev in apps:
        seen.setdefault(bnx_device_fp(dev), set()).add(doc)
    return {k: len(v) for k, v in seen.items()}


# ── Quy mô (AF2, nhánh B): luật “từ 3 giấy tờ khác nhau trên cùng một dấu vân tay thì gắn cờ” khi số hồ sơ tăng ──
_L21_HE = ["Android 13", "Android 14", "iOS 17", "iOS 18"]
_L21_MAN = ["720x1600", "1080x2400", "1170x2532", "1290x2796", "1440x3200", "1080x1920"]


def bnx_l21_fp_of(i):
    """Dấu vân tay của hồ sơ thứ i trong quần thể minh hoạ: 4 hệ điều hành × 6 cỡ màn hình = 24 tổ hợp, chọn theo SHA-256 của "hs<i>"."""
    h = int(hashlib.sha256(f"hs{i}".encode()).hexdigest(), 16)
    return bnx_device_fp({"he": _L21_HE[h % 4], "man": _L21_MAN[h // 4 % 6], "mui": "UTC+7"})


def bnx_l21_scale(n, nguong=3):
    """(số mã khác nhau, số hồ sơ bị gắn cờ) với n hồ sơ, mỗi hồ sơ một giấy tờ khác nhau; gắn cờ nếu mã có ≥ nguong giấy tờ."""
    dem = {}
    for i in range(n):
        k = bnx_l21_fp_of(i)
        dem[k] = dem.get(k, 0) + 1
    return len(dem), sum(c for c in dem.values() if c >= nguong)


def bnx_l21_reviewers(flagged, per_person):
    """Số người xét tối thiểu một ngày: làm tròn lên."""
    return -(-flagged // per_person)
