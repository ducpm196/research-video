"""BNX L23 — Từ scikit-learn tới ONNX Runtime, rừng cô lập: hàm tham chiếu cho `checks:` (chỉ thư viện chuẩn).
Công thức độ sâu trung bình c(n), điểm 2^(-h/c(n)), dấu âm và offset_ theo mã nguồn scikit-learn 1.9 (audit/bnx/sources_l23.md [SKIF]).
Mọi số liệu từ lần chạy thật với scikit-learn / skl2onnx / onnxruntime nằm ở audit/bnx/ver/l23.py (cần thư viện ngoài); ở đây chỉ có phần tính được bằng toán."""
import math

_BNX23_EULER = 0.5772156649015329


def bnx_l23_c(n):
    """Độ sâu trung bình để cô lập một điểm trong cây n điểm: 2(ln(n-1) + γ) - 2(n-1)/n; n = 2 → 1; n ≤ 1 → 0."""
    if n <= 1:
        return 0.0
    if n == 2:
        return 1.0
    return 2.0 * (math.log(n - 1) + _BNX23_EULER) - 2.0 * (n - 1) / n


def bnx_l23_score(h, n):
    """Điểm theo kiểu scikit-learn (score_samples): -2^(-h / c(n)); h là độ sâu trung bình của điểm."""
    return -(2.0 ** (-h / bnx_l23_c(n)))


def bnx_l23_depth_from_score(s, n):
    """Độ sâu quy đổi ngược từ điểm âm s: -c(n) * log2(-s)."""
    return -bnx_l23_c(n) * math.log2(-s)


def bnx_l23_decision(score, offset):
    """decision_function = score_samples - offset_ (tài liệu scikit-learn)."""
    return score - offset


def bnx_l23_label(score, offset):
    """Nhãn predict: -1 khi decision_function < 0, ngược lại 1."""
    return -1 if bnx_l23_decision(score, offset) < 0 else 1


def bnx_l23_expected_flags(n, contamination):
    """Số điểm huấn luyện bị gắn -1 khi offset_ là phân vị 100*contamination của n điểm có điểm khác nhau
    (numpy nội suy tuyến tính: chỉ số q*(n-1); điểm NHỎ HƠN HẲN ngưỡng bị gắn)."""
    idx = contamination * (n - 1)
    k = math.floor(idx)
    return k + 1 if idx - k > 1e-9 else k
