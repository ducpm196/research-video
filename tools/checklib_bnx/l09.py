"""BNX L09 — Couchbase: khoá bản ghi, vBucket (CRC32 mod 1024, giản lược), CAS chống mất cập nhật, hạn sống. Chỉ thư viện chuẩn."""
import zlib
from itertools import permutations


def bnx_crc32(key):
    return zlib.crc32(key.encode())


def bnx_vbucket_of_crc(crc, n=1024):
    """Như thư viện Java chính thức (couchbase-jvm-clients, KeyValueLocator.partitionForKey):
    ((crc32 >> 16) & 0x7fff) & (n - 1), n là lũy thừa của 2. Viết bằng phép chia: (crc // 65536) mod 32768, rồi mod n."""
    return (crc // 65536) % 32768 % n


def bnx_vbucket(key, n=1024):
    return bnx_vbucket_of_crc(bnx_crc32(key), n)


def bnx_cas_story(start=100, cas=7, adds=(("P1", 50), ("P2", 30)), use_cas=True):
    """Cả hai tiến trình đọc cùng (giá trị, CAS) trước, rồi ghi lần lượt. Có CAS: ghi lệch thì bị từ chối, đọc lại rồi ghi.
    Không CAS: ghi đè bằng giá trị tính từ lần đọc cũ. Trả (giá trị cuối, CAS cuối, nhật ký)."""
    v, c = start, cas
    reads = {p: (v, c) for p, _ in adds}
    log = []
    for p, a in adds:
        old_v, old_c = reads[p]
        if use_cas and old_c != c:
            log.append((p, "từ chối"))
            old_v, old_c = v, c  # đọc lại
            log.append((p, "đọc lại", old_v, old_c))
        v, c = old_v + a, c + 1
        log.append((p, "ghi", v, c))
    return v, c, log


def bnx_interleavings(use_cas, start=100, adds=(("P1", 50), ("P2", 30))):
    """Mọi thứ tự của 4 sự kiện (mỗi tiến trình: đọc rồi ghi). Trả (số thứ tự, tập giá trị cuối có thể)."""
    add = dict(adds)
    names = [p for p, _ in adds for _ in range(2)]
    orders = set(permutations(names))
    finals = set()
    for o in orders:
        v, ver, seen = start, 7, {}
        for p in o:
            if p not in seen:
                seen[p] = (v, ver)
                continue
            old, c = seen[p]
            if use_cas and c != ver:
                old = v
            v, ver = old + add[p], ver + 1
        finals.add(v)
    return len(orders), sorted(finals)


def bnx_ttl_after_mutation(ttl, set_expiry_again, preserve_expiry=False):
    """Couchbase (Manage expiration): ghi mà không đặt hạn sống thì hạn sống về 0 (không hết hạn), trừ khi preserve_expiry."""
    if set_expiry_again or preserve_expiry:
        return ttl
    return 0


def bnx_clock_add(h, m, s, seconds):
    t = h * 3600 + m * 60 + s + seconds
    return t // 3600 % 24, t % 3600 // 60, t % 60
