"""BNX L08 — Elasticsearch: chỉ mục ngược, định tuyến mảnh, bản sao, làm tươi. Chỉ thư viện chuẩn, không mạng."""
import zlib
from fractions import Fraction
from math import lcm


def bnx_inverted_index(docs):
    """docs: {mã: mô tả}. Trả {từ: [mã đã sắp]} — chỉ mục ngược tách theo dấu cách."""
    idx = {}
    for d, text in docs.items():
        for w in text.split():
            idx.setdefault(w, set()).add(d)
    return {w: sorted(s) for w, s in idx.items()}


def bnx_search_and(docs, *words):
    idx = bnx_inverted_index(docs)
    s = None
    for w in words:
        cur = set(idx.get(w, []))
        s = cur if s is None else s & cur
    return sorted(s or [])


def bnx_shard(h, n_primary):
    """Mảnh = băm(_routing) mod số mảnh chính (công thức chỉ mục tạo từ bản 9.4)."""
    return h % n_primary


def bnx_total_shards(n_primary, n_replica):
    return n_primary * (1 + n_replica)


def bnx_keep_cycle(n_old, n_new):
    """Trên một chu kỳ lcm(n_old, n_new) giá trị băm liên tiếp: (số giữ mảnh, độ dài chu kỳ, tỉ lệ)."""
    c = lcm(n_old, n_new)
    keep = sum(1 for h in range(c) if h % n_old == h % n_new)
    return keep, c, Fraction(keep, c)


def bnx_crc_shard(doc_id, n):
    """Băm minh hoạ (CRC32 của thư viện chuẩn) — KHÔNG phải hàm băm thật của Elasticsearch."""
    return zlib.crc32(doc_id.encode()) % n


def bnx_crc_keep(n_ids, n_old, n_new):
    ids = [f"tx{i}" for i in range(1, n_ids + 1)]
    return sum(bnx_crc_shard(d, n_old) == bnx_crc_shard(d, n_new) for d in ids)


def bnx_split_ok(n_old, factor):
    """Tách mảnh (split) n_old → n_old·factor: mọi giá trị băm có mảnh mới mod n_old = mảnh cũ (mỗi mảnh mới là con của một mảnh cũ)."""
    n_new = n_old * factor
    return all((h % n_new) % n_old == h % n_old for h in range(lcm(n_old, n_new) * 3))


def bnx_refresh_sim(writes, searches, interval=1.0):
    """writes: [(thời điểm ghi, tài liệu)]; searches: [thời điểm tìm]. Làm tươi ở interval, 2·interval, …
    Trả danh sách số tài liệu tìm thấy ở mỗi lần tìm (tài liệu thấy được khi đã qua một lần làm tươi sau lúc ghi)."""
    out = []
    for t in searches:
        last_refresh = (t // interval) * interval
        out.append(sum(1 for tw, _ in writes if tw < last_refresh))
    return out
