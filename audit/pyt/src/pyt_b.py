"""Hàm dùng chung cho nửa B của khoá PYT (L12, L13): khoảng trắng không ngắt trong số/đơn vị hiện trên màn hình (tránh dòng gãy giữa '1 099' và '999').
Chỉ đổi phần chữ NGOÀI khối mã (div.code), nên mã/đầu ra trên màn hình và sổ screen_code không đổi."""
import re

_NUM = re.compile(r"(?<=\d) (?=\d{3}(?!\d))")
_UNIT = re.compile(r"(?<=[\d≈]) (?=(?:ms|µs|ns|s|KB|MB|GB|byte|giây|phút|giờ|ngày)\b)")


def _fix(t):
    t = _NUM.sub(" ", t)
    t = _UNIT.sub(" ", t)
    t = t.replace("≈ ", "≈ ")
    return t.replace("--tb=short", '<span style="white-space:nowrap">--tb=short</span>') if "<code>" in t else t


def nbsp_html(h):
    """Áp _fix lên chữ ngoài các khối <div class="code">…</div> (đếm độ sâu thẻ div)."""
    out, i, n = [], 0, len(h)
    key = '<div class="code">'
    while i < n:
        j = h.find(key, i)
        if j < 0:
            out.append(_fix(h[i:]))
            break
        out.append(_fix(h[i:j]))
        depth, k = 0, j
        for m in re.finditer(r"<(/?)div\b", h[j:]):
            depth += -1 if m.group(1) else 1
            if depth == 0:
                k = j + m.end()
                k = h.find(">", k) + 1
                break
        out.append(h[j:k])
        i = k
    return "".join(out)


def nbsp_spec(slug_spec):
    slug, spec = slug_spec
    for sc in spec["scenes"]:
        for st in sc["steps"]:
            st["show"] = nbsp_html(st["show"])
    return slug, spec
