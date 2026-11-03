# PAR L08 — nhóm 32 luồng: mô phỏng từng lượt với “mặt nạ luồng đang làm” và đếm byte của từng đoạn 32 byte (khác `checks`:
# alg.par_warp_passes đếm số nhánh khác nhau, alg.par_transactions đếm tập chỉ số đoạn).
from fractions import Fraction as F
import random


def run_warp(branch_of, body_len):
    """Chạy một nhóm 32 luồng: mỗi lượt chọn nhánh của luồng nhỏ nhất còn chưa xong, bật mặt nạ cho mọi luồng cùng nhánh."""
    pending, steps, useful = set(range(32)), 0, 0
    while pending:
        b = branch_of(min(pending))
        mask = {t for t in pending if branch_of(t) == b}
        steps += body_len[b]; useful += len(mask) * body_len[b]
        pending -= mask
    return steps, F(useful, 32 * steps)


rec("L08a", run_warp(lambda t: t % 2, {0: 10, 1: 10}) == (20, F(1, 2)) and run_warp(lambda t: 0 if t else 1, {0: 10, 1: 10}) == (20, F(1, 2))
    and all(run_warp(lambda t, w=w: ((w * 32 + t) // 32) % 2, {0: 10, 1: 10}) == (10, 1) for w in range(4))
    and run_warp(lambda t: t < 16, {True: 10, False: 10})[0] == 20,
    "mô phỏng mặt nạ: chẵn/lẻ 2 lượt 50%; 1 luồng lạc đàn vẫn 50%; theo số nhóm 1 lượt 100%; t < 16 → 2 lượt")


def bytes_moved(elem_index, offset_bytes=0):
    """Phủ từng byte cần đọc lên lưới đoạn 32 byte; trả (số đoạn, byte chuyển, byte cần)."""
    need = set()
    for t in range(32):
        a = offset_bytes + 4 * elem_index(t)
        need |= set(range(a, a + 4))
    segs = {b // 32 for b in need}
    return len(segs), 32 * len(segs), len(need)


cases = {1: (4, 1), 2: (8, F(1, 2)), 4: (16, F(1, 4)), 32: (32, F(1, 8)), 1024: (32, F(1, 8))}
rec("L08b", all((lambda r: (r[0], F(r[2], r[1])))(bytes_moved(lambda t, s=s: s * t)) == v for s, v in cases.items())
    and (lambda r: (r[0], F(r[2], r[1])))(bytes_moved(lambda t: t, 4)) == (5, F(4, 5)),
    "phủ byte lên đoạn 32 byte: bước 1 → 4 (100%), 2 → 8 (50%), 4 → 16 (25%), 32 và 1024 → 32 (12,5%), lệch 4 byte → 5 (80%)")
rec("L08c", [4 * 5, 100 // 32, 100 % 32] == [20, 3, 4] and 10 ** 12 * F(1, 8) == 125 * 10 ** 9,
    "ôn nền: địa chỉ 20, đoạn 3 dư 4; băng thông có ích 125 tỉ byte/s (ít hơn 8 lần)")
random.seed(8)
same = sum(len({random.random() > 0.5 for _ in range(32)}) == 1 for _ in range(200000))
rec("L08d", same == 0 and abs(2 / 2 ** 32 - 4.656612873e-10) < 1e-18,
    f"dữ liệu ngẫu nhiên: 200 000 nhóm thử, {same} nhóm không phân kỳ; xác suất 2/2^32 ≈ 4,7·10^-10")
