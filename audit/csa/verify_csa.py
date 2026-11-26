"""Kiểm độc lập mọi khẳng định của khoá CSA (17 bài L00–L16) — tự cài lại không dùng logic trong checklib,
rồi đối chiếu với tools/checklib.py khi có hàm tương ứng.
Chạy: .venv/Scripts/python audit/csa/verify_csa.py"""
import math
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
import checklib as alg  # noqa: E402

R = []


def rec(code, ok, what):
    R.append((code, bool(ok)))
    print(("PASS" if ok else "FAIL"), code, "—", what)


# L00: 0x2F = 47 = 0b101111; 1 KiB vs 1 kB
rec("L00", int("2F", 16) == 47 and bin(47) == "0b101111" and (1 << 10) == 1024 and 10 ** 3 == 1000,
    "0x2F = 47 = 0b101111; 1 KiB = 1024 B != 1 kB = 1000 B")

# L01: bù 2 8 bit: -5 = 11111011; 127 + 1 -> -128
to_u8 = lambda x: x & 0xFF
to_s8 = lambda u: u - 256 if (u & 0x80) else u
rec("L01", format(to_u8(-5), "08b") == "11111011" and to_s8(to_u8(127 + 1)) == -128,
    "bù 2 8-bit: -5 = 11111011; 127 + 1 quay vòng không dấu thành -128")

# L02: phép bit 12 & 11 = 8; x & (x-1) == 0; 13 << 3 = 104
p2 = [x for x in range(1, 65) if (x & (x - 1)) == 0]
rec("L02", (12 & 11) == 8 and p2 == [1, 2, 4, 8, 16, 32, 64] and (13 << 3) == 104,
    "12 & 11 = 8; x&(x-1)==0 đúng mọi luỹ thừa 2 <= 64; 13 << 3 = 104")

# L03: IEEE 754 float32 của 1.0 = 0x3F800000; 0.1 + 0.2
b32 = struct.unpack(">I", struct.pack(">f", 1.0))[0]
rec("L03", b32 == 0x3F800000 and (0.1 + 0.2) != 0.3 and abs((0.1 + 0.2) - 0.3) < 1e-15,
    "float32(1.0) = 0x3F800000; 0.1 + 0.2 = 0.30000000000000004")

# L04: epsilon máy float64 = 2^-52 và triệt tiêu (10^16 + 1) - 10^16 == 0
eps = 1.0
while 1.0 + eps / 2.0 != 1.0:
    eps /= 2.0
rec("L04", eps == 2.0 ** -52 and abs(eps - 2.220446049250313e-16) < 1e-30 and ((1e16 + 1.0) - 1e16) == 0.0,
    f"eps = {eps:.3e} == 2^-52; (10^16 + 1) - 10^16 == 0")

# L05: half adder & NAND completeness (kiểm bảng chân trị + SVG gates)
ha = {(a, b): (a ^ b, a & b) for a in (0, 1) for b in (0, 1)}
nand = lambda a, b: 1 - (a & b)
nand_not = lambda a: nand(a, a)
nand_and = lambda a, b: nand_not(nand(a, b))
nand_or = lambda a, b: nand(nand_not(a), nand_not(b))
nand_xor = lambda a, b: nand(nand(a, nand(a, b)), nand(b, nand(a, b)))
ok_nand = all(nand_xor(a, b) == (a ^ b) and nand_and(a, b) == (a & b) and nand_or(a, b) == (a | b)
              for a in (0, 1) for b in (0, 1))
rec("L05", ha[(1, 1)] == (0, 1) and ha[(1, 0)] == (1, 0) and ok_nand,
    "bộ cộng bán phần + đủ cổng từ NAND (4 trạng thái)")

# L06: bộ cộng 4 bit phần cứng cho 0111 + 0101 = 1100 (12 unsigned, -4 signed -> overflow)
def ripple_add4(a, b):
    c = 0
    s = 0
    for i in range(4):
        ai, bi = (a >> i) & 1, (b >> i) & 1
        si = ai ^ bi ^ c
        ci = (ai & bi) | (c & (ai ^ bi))
        if i == 3:
            c_in_msb, c_out_msb = c, ci
        c = ci
        s |= (si << i)
    return s, (s - 16 if s & 8 else s), (c_in_msb ^ c_out_msb) == 1

u4, s4, ov = ripple_add4(0b0111, 0b0101)
rec("L06", u4 == 12 and s4 == -4 and ov is True,
    "0111 + 0101 = 1100: 12 không dấu, -4 có dấu, tràn có dấu = True")

# L07: mô phỏng vòng lặp 1..10 (3 lệnh khởi tạo + 10*3 = 33 lệnh) so với checklib.run_asm
acc, i, ops = 0, 1, 3  # 3 lệnh khởi tạo (acc=0, i=1, n=10)
while True:
    acc += i
    i += 1
    ops += 2
    ops += 1  # ble jump
    if i > 10:
        break
r_asm, n_asm, _ = alg.run_asm(alg.SUM_1_TO_10)
rec("L07", acc == 55 and ops == 33 and r_asm["r1"] == 55 and n_asm == 33,
    f"tổng 1..10 = {acc}, số lệnh = {ops} (khớp checklib.run_asm steps={n_asm})")

# L08: thời gian CPU = IC * CPI / freq
t_cpu = 1e9 * 1.5 / 2e9
rec("L08", abs(t_cpu - 0.75) < 1e-12, "10^9 * 1.5 / 2 GHz = 0.75 s")

# L09: pipeline k=5 tầng, n=100 lệnh -> k + n - 1 = 104 chu kỳ; tăng tốc = 500/104
cyc_pipe = 5 + 100 - 1
sp_pipe = (5 * 100) / cyc_pipe
rec("L09", cyc_pipe == 104 and abs(sp_pipe - 4.8076923) < 1e-4,
    f"5 tầng 100 lệnh = {cyc_pipe} chu kỳ, nhanh {sp_pipe:.2f}x")

# L10: AMAT = h_t + m_r * m_p
amat = 1.0 + 0.05 * 100.0
rec("L10", abs(amat - 6.0) < 1e-12, "AMAT = 1 + 0.05 * 100 = 6 chu kỳ")

# L11: cache ánh xạ trực tiếp 32 KiB, dòng 64 B, địa chỉ 32 bit
lines = (32 * 1024) // 64
off_b = int(math.log2(64))
idx_b = int(math.log2(lines))
tag_b = 32 - idx_b - off_b
rec("L11", lines == 512 and (tag_b, idx_b, off_b) == (17, 9, 6),
    f"cache 32KiB/64B: {lines} dòng, 32 bit = {tag_b} tag + {idx_b} idx + {off_b} off")

# L12: mô phỏng cache LRU độc lập so với checklib.cache_hits
def sim_cache_lru(seq, sets, ways):
    tags = [[] for _ in range(sets)]
    hits = 0
    for blk in seq:
        s = blk % sets
        if blk in tags[s]:
            hits += 1
            tags[s].remove(blk)
            tags[s].append(blk)
        else:
            if len(tags[s]) >= ways:
                tags[s].pop(0)
            tags[s].append(blk)
    return hits

seq12 = [0, 4, 0, 4, 8, 0, 4]
h_dm = sim_cache_lru(seq12, 4, 1)
h_2w = sim_cache_lru(seq12, 2, 2)
ok12 = (h_dm == 0 and h_2w == 2
        and alg.cache_hits(seq12, sets=4, ways=1) == 0
        and alg.cache_hits(seq12, sets=2, ways=2) == 2)
rec("L12", ok12, f"dãy {seq12}: DM hits={h_dm}, 2-set 2-way LRU hits={h_2w}")

# L13: định luật Amdahl: p=0.9, n=8 -> 1 / (0.1 + 0.9/8) = 4.70588..., n->inf -> 10
s8 = 1.0 / (0.1 + 0.9 / 8.0)
s_inf = 1.0 / 0.1
amd_sp = alg.par_amdahl(0.9, 8)
rec("L13", abs(s8 - 80 / 17) < 1e-12 and abs(s8 - amd_sp) < 1e-12 and s_inf == 10.0,
    f"Amdahl p=0.9 n=8 -> {s8:.4f}x, max -> {s_inf:.0f}x")

# L14: bộ nhớ ảo 32 bit, trang 4 KiB -> 2^20 mục; TLB 98% (1ns), mem 100ns -> EAT = 0.98*(1+100)+0.02*(1+200) = 103
pte_cnt = (1 << 32) // 4096
eat = 0.98 * (1 + 100) + 0.02 * (1 + 100 + 100)
rec("L14", pte_cnt == (1 << 20) and abs(eat - 103.0) < 1e-12,
    f"32-bit/4KiB = 2^20 mục; EAT = {eat:.1f} ns")

# L15: vào/ra 1000 ngắt/s * 2 us = 0.2% CPU
io_pct = 1000 * 2e-6 * 100.0
rec("L15", abs(io_pct - 0.2) < 1e-12, f"1000 ngắt/s * 2us = {io_pct:.1f}% CPU")

# L16: bữa trưa miễn phí & Spectre (HS05, KO19): xung nhịp, Amdahl 2 lõi, đoán nhánh 95% * 200 chu kỳ
t_2g = 1e9 * 1.5 / 2e9
t_373 = 1e9 * 1.5 / 3.73e9
t_10g = 1e9 * 1.5 / 10e9
s_2c = 1.0 / (0.1 + 0.9 / 2.0)
avg_pen = 0.05 * 200.0
rec("L16", abs(t_2g - 0.75) < 1e-9 and abs(t_373 - 0.4021) < 1e-3 and abs(t_10g - 0.15) < 1e-9
    and abs(s_2c - 20 / 11) < 1e-9 and abs(avg_pen - 10.0) < 1e-9 and 188 < 192,
    f"2GHz={t_2g:.2f}s, 3.73GHz={t_373:.2f}s, 2 lõi={s_2c:.2f}x, phạt nhánh={avg_pen:.0f} chu kỳ")

# ── Kiểm tự động mọi lab (du_lieu.txt + ca_an/) qua cham.sh ──
import subprocess as _subp
from pathlib import Path as _LabPath
_BASH = r"C:\Program Files\Git\bin\bash.exe"
if not _LabPath(_BASH).exists():
    _BASH = "bash"
for _ld in sorted((ROOT / "labs" / "CSA").glob("L*")):
    _rp = _subp.run([_BASH, str(ROOT / "labs" / "cham.sh"), "CSA", _ld.name], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
    rec(f"{_ld.name}:lab", _rp.returncode == 0 and "PASS" in _rp.stdout and "2 ca an" in _rp.stdout, f"cham.sh {_ld.name} (public + 2 ca_an)")

p = sum(ok for _, ok in R)
print(f"{p}/{len(R)} PASS")
sys.exit(0 if p == len(R) else 1)
