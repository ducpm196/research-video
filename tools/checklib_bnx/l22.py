"""BNX L22 — Adobe Experience Manager (JCR, Sling, HTL, OSGi): hàm tham chiếu cho `checks:` (chỉ thư viện chuẩn).
MÔ PHỎNG theo tài liệu (audit/bnx/sources_l22.md), không phải máy chủ AEM. Cách viết ở đây cố ý KHÁC mã hiện trên màn hình
(kho là dict phẳng đường dẫn → thuộc tính; tách đường dẫn bằng cách thử từng tiền tố từ dài tới ngắn)."""

_BNX_L22_REPO = {
    "/content": {},
    "/content/site": {},
    "/content/site/vi": {},
    "/content/site/vi/home": {"jcr:primaryType": "nt:unstructured", "sling:resourceType": "site/components/page",
                              "jcr:title": "Xin chào <script>alert(1)</script>"},
    "/content/site/vi/vay": {"jcr:primaryType": "nt:unstructured", "sling:resourceType": "site/components/page",
                             "jcr:title": "Vay tiêu dùng"},
}
_BNX_L22_SCRIPTS = ("/apps/site/components/page/page.html", "/apps/site/components/page/in.html",
                    "/libs/site/components/page/page.html")
_BNX_L22_NEXT = {"INSTALLED": {"resolve": "RESOLVED", "uninstall": "UNINSTALLED"},
                 "RESOLVED": {"start": "STARTING", "uninstall": "UNINSTALLED"},
                 "STARTING": {"started": "ACTIVE"},
                 "ACTIVE": {"stop": "STOPPING"},
                 "STOPPING": {"stopped": "RESOLVED"},
                 "UNINSTALLED": {}}


def bnx_l22_repo():
    """Kho mẫu của bài: {đường dẫn nút: {thuộc tính: giá trị}}."""
    return {k: dict(v) for k, v in _BNX_L22_REPO.items()}


def bnx_l22_props(path, repo=None):
    """Thuộc tính của nút tại `path`, hoặc None khi không có nút."""
    repo = _BNX_L22_REPO if repo is None else repo
    return dict(repo[path]) if path in repo else None


def bnx_l22_depth(path):
    """Số cấp của một đường dẫn tuyệt đối (/a/b → 2)."""
    return len([p for p in path.split("/") if p])


def bnx_l22_split(url, paths=None):
    """Tách đường dẫn yêu cầu theo Apache Sling “URL decomposition”.
    Trả (đường dẫn tài nguyên, [selector], phần mở rộng hoặc None, hậu tố hoặc None, có tài nguyên?).
    Đường dẫn tài nguyên = tiền tố DÀI NHẤT trùng một nút có thật mà ký tự kế tiếp là dấu chấm hoặc hết chuỗi;
    không có nút nào thì cắt ở dấu chấm đầu tiên (hoặc lấy cả chuỗi)."""
    paths = set(_BNX_L22_REPO) if paths is None else set(paths)
    cut, found = None, False
    for end in range(len(url), 0, -1):
        if (end == len(url) or url[end] == ".") and url[:end] in paths:
            cut, found = end, True
            break
    if cut is None:
        cut = url.index(".") if "." in url else len(url)
    rest = url[cut + 1:]
    slash = rest.find("/")
    mid, suffix = (rest, None) if slash < 0 else (rest[:slash], rest[slash:])
    parts = mid.split(".") if mid else []
    return url[:cut], parts[:-1], (parts[-1] if parts else None), suffix, found


def bnx_l22_script(rtype, selectors, ext, scripts=None):
    """Chọn tệp dựng: tên theo selector (khớp nhiều selector đầu hơn thì ưu tiên hơn) rồi tới tên theo nhãn của kiểu tài nguyên;
    với mỗi tên, tìm ở /apps trước, /libs sau. Phần mở rộng html được lược khỏi tên tệp. Không thấy → None."""
    scripts = _BNX_L22_SCRIPTS if scripts is None else tuple(scripts)
    tail = ".html" if ext == "html" else f".{ext}.html"
    names = []
    k = len(selectors)
    while k > 0:
        names.append("/".join(selectors[:k]))
        k -= 1
    names.append(rtype.rsplit("/", 1)[-1])
    for name in names:
        for root in ("/apps/", "/libs/"):
            cand = f"{root}{rtype}/{name}{tail}"
            if cand in scripts:
                return cand
    return None


def bnx_l22_resolve(url):
    """Cả chuỗi của bài: đường dẫn → nút → sling:resourceType → tệp dựng. Trả (đường dẫn tài nguyên, kiểu, tệp)."""
    path, sels, ext, _, found = bnx_l22_split(url)
    if not found:
        return path, None, None
    rtype = _BNX_L22_REPO[path].get("sling:resourceType")
    return path, rtype, (bnx_l22_script(rtype, sels, ext) if rtype and ext else None)


def bnx_l22_escape(text):
    """Thoát bốn ký tự đặc biệt của HTML (& < > \")."""
    res = []
    for ch in text:
        res.append({"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;"}.get(ch, ch))
    return "".join(res)


def bnx_l22_escaped_count(text):
    """Số ký tự bị thay khi thoát."""
    return sum(1 for ch in text if ch in '&<>"')


def bnx_l22_bundle_trace(needs, available):
    """Dãy trạng thái của một gói khi gọi start. Thiếu gói phụ thuộc → dừng ở INSTALLED."""
    trace = ["INSTALLED"]
    if any(p not in available for p in needs):
        return trace
    for ev in ("resolve", "start", "started"):
        trace.append(_BNX_L22_NEXT[trace[-1]][ev])
    return trace


def bnx_l22_bundle_step(state, event):
    """Một bước của máy trạng thái gói; sự kiện không hợp lệ ở trạng thái đó → None."""
    return _BNX_L22_NEXT.get(state, {}).get(event)


def bnx_l22_serves(state):
    """Gói chỉ cung cấp dịch vụ khi ở ACTIVE."""
    return state == "ACTIVE"


def bnx_l22_scan_cost(rtype, repo=None):
    """Tìm mọi nút có sling:resourceType = rtype khi KHÔNG có chỉ mục: phải đọc mọi nút. Trả (số nút đã đọc, số nút khớp)."""
    repo = _BNX_L22_REPO if repo is None else repo
    read = hit = 0
    for props in repo.values():
        read += 1
        hit += props.get("sling:resourceType") == rtype
    return read, hit
