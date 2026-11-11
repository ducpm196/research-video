"""BNX L00 — Git: mô hình đối tượng Git viết lại bằng Python thuần (hashlib), không gọi git.
Bộ kiểm audit/bnx/ver/l00.py chạy git THẬT rồi so với các hàm này (đường khác)."""
import datetime as _dt
import hashlib as _hl


def bnx_git_obj(kind, body):
    """Mã đối tượng Git = SHA-1 của "<loại> <độ dài>\\0" + nội dung (40 ký tự thập lục phân)."""
    return _hl.sha1(f"{kind} {len(body)}\0".encode() + body).hexdigest()


def bnx_git_blob(text):
    return bnx_git_obj("blob", text.encode("utf-8"))


def bnx_git_tree(entries):
    """entries: [(tên tệp, mã blob)] — chế độ 100644 (tệp thường), xếp theo tên."""
    body = b"".join(b"100644 " + n.encode() + b"\0" + bytes.fromhex(h) for n, h in sorted(entries))
    return bnx_git_obj("tree", body)


def _epoch(iso):
    return int(_dt.datetime.fromisoformat(iso).timestamp())


def bnx_git_commit(tree, parents, msg, who="An <an@vd.vn>", when="2026-01-05T09:00:00+07:00"):
    tz = when[-6:].replace(":", "")
    sig = f"{who} {_epoch(when)} {tz}"
    head = f"tree {tree}\n" + "".join(f"parent {p}\n" for p in parents) + f"author {sig}\ncommitter {sig}\n\n{msg}\n"
    return bnx_git_obj("commit", head.encode("utf-8"))


def bnx_merge3(base, ours, theirs):
    """Gộp ba chiều cho MỘT dòng: chỉ một bên đổi → lấy bên đổi; hai bên đổi giống nhau → lấy; đổi khác nhau → xung đột."""
    if ours == theirs:
        return ("ok", ours)
    if ours == base:
        return ("ok", theirs)
    if theirs == base:
        return ("ok", ours)
    return ("conflict", None)


def bnx_conflict_file(ours, theirs, ours_name="HEAD", theirs_name="tang"):
    """Tệp sau khi gộp báo xung đột (kiểu mặc định của git: bên mình ở trên, bên nhánh gộp vào ở dưới)."""
    return f"<<<<<<< {ours_name}\n{ours}\n=======\n{theirs}\n>>>>>>> {theirs_name}\n"


def bnx_markers(text):
    return [ln for ln in text.splitlines() if ln.startswith(("<<<<<<<", "=======", ">>>>>>>"))]


def bnx_git_demo():
    """Dựng lại lịch sử của bài (cùng tên, ngày giờ, lời nhắn) bằng Python thuần; trả mọi mã đối tượng."""
    r = {}
    r["blob5500"] = bnx_git_blob("phi=5500\n")
    r["root"] = bnx_git_commit(bnx_git_tree([("phi.txt", r["blob5500"])]), [], "Phí chuyển khoản 5500")
    r["blob6600"] = bnx_git_blob("phi=6600\n")
    r["tree6600"] = bnx_git_tree([("phi.txt", r["blob6600"])])
    r["tang"] = bnx_git_commit(r["tree6600"], [r["root"]], "Tăng phí lên 6600")
    r["giam"] = bnx_git_commit(bnx_git_tree([("phi.txt", bnx_git_blob("phi=4400\n"))]), [r["root"]], "Giảm phí còn 4400")
    r["merge"] = bnx_git_commit(r["tree6600"], [r["giam"], r["tang"]], "Gộp nhánh tang: chốt 6600")
    # nhánh lỗi bí mật (khối pitfall): sau commit gốc, thêm .env rồi xoá
    env_blob = bnx_git_blob("DB_PASS=MatKhau123\n")
    r["blob_env"] = env_blob
    r["secret_add"] = bnx_git_commit(bnx_git_tree([(".env", env_blob), ("phi.txt", r["blob5500"])]), [r["root"]], "Thêm cấu hình kết nối")
    r["secret_rm"] = bnx_git_commit(bnx_git_tree([("phi.txt", r["blob5500"])]), [r["secret_add"]], "Xoá mật khẩu")
    return r


def bnx_is_hex40(h):
    return len(h) == 40 and all(c in "0123456789abcdef" for c in h)


def bnx_hex_bits(n_chars):
    """Mỗi ký tự thập lục phân mang 4 bit (16 = 2⁴ giá trị)."""
    return 4 * n_chars


def bnx_reachable(parents, start):
    """Số commit đi tới được từ start theo cạnh cha (đếm như git rev-list --count)."""
    seen, st = set(), [start]
    while st:
        c = st.pop()
        if c not in seen:
            seen.add(c)
            st.extend(parents.get(c, []))
    return len(seen)
