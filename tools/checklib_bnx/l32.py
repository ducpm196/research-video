"""BNX L32 — GitOps và bí mật: mô hình tham chiếu của vòng đối chiếu (tạo, sửa, xoá khi bật prune), đánh giá chính sách quyền (mặc định từ chối, Deny thắng Allow),
số lần gọi Git, cửa sổ lộ của bí mật. Chỉ thư viện chuẩn, không mạng, không Docker. Kiểm độc lập ở audit/bnx/ver/l32.py
(chạy THẬT Python + git, Vault 2.2.2 bằng ảnh Docker chính thức)."""
import fnmatch


def bnx_l32_hours(ngay):
    return ngay * 24


def bnx_l32_ratio(a, b):
    return a / b


def bnx_l32_decide(chinh_sach, viec, tai_nguyen):
    """chinh_sach: danh sách (hiệu lực, mẫu việc, mẫu tài nguyên). Mặc định từ chối; Deny rõ ràng thắng Allow."""
    khop = [h for h, v, t in chinh_sach if fnmatch.fnmatch(viec, v) and fnmatch.fnmatch(tai_nguyen, t)]
    if "Deny" in khop:
        return "tu choi (Deny ro rang)"
    return "cho phep" if "Allow" in khop else "tu choi (mac dinh)"


def bnx_l32_reconcile(mong_muon, that, prune):
    """Một vòng đồng bộ chỉ theo nội dung: (danh sách việc, danh sách còn lệch). Không sửa đối số."""
    that = dict(that)
    viec = []
    for ten, ban in mong_muon.items():
        if that.get(ten) != ban:
            viec.append(("sua " if ten in that else "tao ") + ten)
            that[ten] = ban
    thua = sorted(set(that) - set(mong_muon))
    if prune:
        viec += ["xoa " + t for t in thua]
        for t in thua:
            del that[t]
    lech = sorted({t for t in mong_muon if that.get(t) != mong_muon[t]} | (set(that) - set(mong_muon)))
    return viec, lech


def bnx_l32_git_calls(n):
    """Số lần gọi git để đọc n tệp: từng tệp = 1 (ls-tree) + n (show); một lần = 2 (ls-tree + cat-file --batch)."""
    return n + 1, 2
