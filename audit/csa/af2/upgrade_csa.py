"""Nâng trọn bộ 17 bài CSA (L00–L16) lên chuẩn AF2 theo bảng quyết định BN-08.

- L00–L05: lời giải C thật biên dịch qua GCC 16.2.0 (-std=c11 -Wall -Wextra -Werror)
- L06–L16: mô phỏng định lượng Python tất định (nhãn rõ '(mô phỏng định lượng)' trên đề và bài)
- Mỗi bài thêm cảnh `practice` (kèm mong_doi.txt) + bảng giải mã/quy mô (nếu cần), giữ nguyên phần bài gốc đã duyệt.
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "audit" / "review"))
import af2_kit as ak  # noqa: E402
import af2_upgrader as up  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")


def r3_c_csa():
    rows = [
        ["<code>uint8_t / int8_t</code>", "Số nguyên 8 bit không dấu (0..255) và có dấu (-128..127)"],
        ["<code>(x &gt;&gt; k) &amp; 1U</code>", "Dịch phải k vị trí rồi giữ 1 bit thấp nhất bằng mặt nạ"],
        ["<code>memcpy(&amp;u, &amp;f, 4)</code>", "Chép đúng 4 byte biểu diễn bit IEEE 754 của float sang uint32_t"],
    ]
    return ak.sc(
        "code_read",
        "symbol",
        "Đọc nhanh các ký hiệu bit trong mã thực hành C",
        [
            ak.st_auto(
                ak.table(["viết trong mã C", "đọc là và ý nghĩa"], rows),
                "Trước khi sang phần thực hành bằng mã C, bạn lướt nhanh bảng đọc ba ký hiệu thao tác bít hay gặp. Kiểu tám bít phân biệt rạch ròi không dấu và có dấu, phép dịch kết hợp mặt nạ tách từng bít, còn hàm chép vùng nhớ đọc nguyên dạng bít số thực.",
                clear=True,
            )
        ],
    )


LESSONS = [
    (
        "L00", "c", "1 KiB = 1 024 byte, còn 1 KB = 1 000 byte",
        "# Lab CSA L00 — Hệ đếm nhị phân, thập lục phân và phân biệt KB vs KiB\n\n"
        "Viết chương trình C chuẩn C11 đổi giá trị `47` sang hexa, kiểm tra trạng thái 8 bit tối đa `255` và tính hiệu `1 KiB - 1 KB` theo byte, in đúng 3 dòng:\n"
        "1. `dec=47 hex=0x2F`\n2. `u8_states=256 max=255`\n3. `kib_minus_kb=24`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh CSA L00 duong_dan/bai_cua_ban.c\n```",
        "#include <stdio.h>\n#include <stdint.h>\nint main(void) {\n"
        "    unsigned x = 47;\n    printf(\"dec=%u hex=0x%02X\\n\", x, x);\n"
        "    printf(\"u8_states=%d max=%u\\n\", 1 << 8, UINT8_MAX);\n"
        "    printf(\"kib_minus_kb=%d\\n\", 1024 - 1000);\n    return 0;\n}\n",
        None,
    ),
    (
        "L01", "c", "Biên 8 bit bù 2: từ -128 tới +127",
        "# Lab CSA L01 — Số nguyên không dấu, bù 2 và ranh giới tràn 8 bit\n\n"
        "Viết chương trình C chuẩn C11 chuyển mẫu bit `0xFF` thành `uint8_t` (255) và `int8_t` (-1), kiểm tra giá trị cực tiểu/cực đại bù 2 của 8 bit, in đúng 3 dòng:\n"
        "1. `u8=255 i8=-1`\n2. `i8_min=-128 i8_max=127`\n3. `u8_wrap_127_plus_1=128`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh CSA L01 duong_dan/bai_cua_ban.c\n```",
        "#include <stdio.h>\n#include <stdint.h>\n#include <string.h>\nint main(void) {\n"
        "    uint8_t raw = 0xFF; int8_t s = 0; memcpy(&s, &raw, 1);\n"
        "    printf(\"u8=%u i8=%d\\n\", raw, (int)s);\n"
        "    printf(\"i8_min=%d i8_max=%d\\n\", INT8_MIN, INT8_MAX);\n"
        "    uint8_t v = 127; v = (uint8_t)(v + 1);\n"
        "    printf(\"u8_wrap_127_plus_1=%u\\n\", v);\n    return 0;\n}\n",
        None,
    ),
    (
        "L02", "c", "Kiểm lũy thừa của 2 bằng (x & (x - 1)) == 0 với x > 0",
        "# Lab CSA L02 — Phép toán bit, mặt nạ và kiểm lũy thừa của 2\n\n"
        "Viết chương trình C chuẩn C11 dùng toán tử bit trên `x = 0x5A` (lấy bit 3, bật bit 0, tắt bit 4) và kiểm tra `64` vs `48` có là lũy thừa của 2 không, in đúng 3 dòng:\n"
        "1. `bit3=1 set0=0x5B clr4=0x4A`\n2. `pow2_64=1 pow2_48=0`\n3. `shift_mul=80`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh CSA L02 duong_dan/bai_cua_ban.c\n```",
        "#include <stdio.h>\nstatic int is_pow2(unsigned n) { return n > 0 && (n & (n - 1)) == 0; }\n"
        "int main(void) {\n    unsigned x = 0x5A;\n"
        "    printf(\"bit3=%u set0=0x%02X clr4=0x%02X\\n\", (x >> 3) & 1U, x | 1U, x & ~(1U << 4));\n"
        "    printf(\"pow2_64=%d pow2_48=%d\\n\", is_pow2(64), is_pow2(48));\n"
        "    printf(\"shift_mul=%u\\n\", 5U << 4);\n    return 0;\n}\n",
        None,
    ),
    (
        "L03", "c", "float32: 1 bit dấu, 8 bit mũ lệch 127, 23 bit định trị",
        "# Lab CSA L03 — Giải mã 3 trường IEEE 754 float32 và so sánh gần đúng\n\n"
        "Viết chương trình C chuẩn C11 tách bit dấu, mũ (đã trừ bias 127) và phần định trị hexa của `float x = -6.5f`, đồng thời kiểm tra `fabs(0.1 + 0.2 - 0.3) < 1e-9`, in đúng 3 dòng:\n"
        "1. `sign=1 exp_unbiased=2 mant_hex=0x500000`\n2. `close_03=1`\n3. `hex32=0xC0D00000`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh CSA L03 duong_dan/bai_cua_ban.c\n```",
        "#include <stdio.h>\n#include <stdint.h>\n#include <string.h>\n#include <math.h>\nint main(void) {\n"
        "    float f = -6.5f; uint32_t u = 0; memcpy(&u, &f, 4);\n"
        "    int sign = (int)(u >> 31); int exp = (int)((u >> 23) & 0xFF) - 127;\n"
        "    uint32_t mant = u & 0x7FFFFFU;\n"
        "    printf(\"sign=%d exp_unbiased=%d mant_hex=0x%06X\\n\", sign, exp, mant);\n"
        "    printf(\"close_03=%d\\n\", fabs((0.1 + 0.2) - 0.3) < 1e-9 ? 1 : 0);\n"
        "    printf(\"hex32=0x%08X\\n\", u);\n    return 0;\n}\n",
        r3_c_csa(),
    ),
    (
        "L04", "c", "Cộng số nhỏ trước, kiểm FLT_EPSILON (ngưỡng sai số float 32-bit) để tránh mất độ chính xác",
        "# Lab CSA L04 — Epsilon máy, cộng không kết hợp và kiểm FLT_EPSILON\n\n"
        "Viết chương trình C chuẩn C11 minh họa cộng dấu phẩy động không kết hợp: `(1e16 + 1.0) - 1e16 == 0.0` so với `1.0 + (1e16 - 1e16) == 1.0`, "
        "và kiểm chứng hằng số `FLT_EPSILON` (ngưỡng epsilon máy 32-bit trong `<float.h>`) nhỏ hơn `1e-6`, in đúng 3 dòng:\n"
        "1. `left_assoc=0.0`\n2. `right_assoc=1.0`\n3. `eps_f32_lt_1e6=1`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh CSA L04 duong_dan/bai_cua_ban.c\n```",
        "#include <stdio.h>\n#include <float.h>\nint main(void) {\n"
        "    double big = 1e16;\n"
        "    printf(\"left_assoc=%.1f\\n\", (big + 1.0) - big);\n"
        "    printf(\"right_assoc=%.1f\\n\", 1.0 + (big - big));\n"
        "    printf(\"eps_f32_lt_1e6=%d\\n\", FLT_EPSILON < 1e-6f ? 1 : 0);\n    return 0;\n}\n",
        None,
    ),
    (
        "L05", "c", "Cổng NAND đơn độc tổng hợp được NOT, AND, OR và Half Adder",
        "# Lab CSA L05 — Dựng cổng logic phổ quát NAND và bộ cộng bán phần/toàn phần\n\n"
        "Viết chương trình C chuẩn C11 chỉ dùng hàm `nand(a, b)` để dựng `b_not`, `b_and`, `b_or`, `b_xor`, rồi kiểm tra bộ cộng toàn phần `(a=1, b=1, cin=1)`, in đúng 3 dòng:\n"
        "1. `not1=0 and11=1 or01=1 xor11=0`\n2. `fa_111_sum=1 fa_111_cout=1`\n3. `fa_101_sum=0 fa_101_cout=1`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh CSA L05 duong_dan/bai_cua_ban.c\n```",
        "#include <stdio.h>\nstatic int nand_g(int a, int b) { return !(a & b); }\n"
        "static int g_not(int a) { return nand_g(a, a); }\n"
        "static int g_and(int a, int b) { return g_not(nand_g(a, b)); }\n"
        "static int g_or(int a, int b) { return nand_g(g_not(a), g_not(b)); }\n"
        "static int g_xor(int a, int b) { int t = nand_g(a, b); return nand_g(nand_g(a, t), nand_g(b, t)); }\n"
        "int main(void) {\n"
        "    printf(\"not1=%d and11=%d or01=%d xor11=%d\\n\", g_not(1), g_and(1,1), g_or(0,1), g_xor(1,1));\n"
        "    int s1 = g_xor(g_xor(1,1),1), c1 = g_or(g_and(1,1), g_and(1, g_xor(1,1)));\n"
        "    int s2 = g_xor(g_xor(1,0),1), c2 = g_or(g_and(1,0), g_and(1, g_xor(1,0)));\n"
        "    printf(\"fa_111_sum=%d fa_111_cout=%d\\n\", s1, c1);\n"
        "    printf(\"fa_101_sum=%d fa_101_cout=%d\\n\", s2, c2);\n    return 0;\n}\n",
        None,
    ),
    (
        "L06", "py", "(Mô phỏng định lượng) Bộ cộng nhiều bit, phép trừ và cờ tràn số",
        "# Lab CSA L06 (Mô phỏng phần cứng ALU) — Bộ cộng 8 bit, trừ bằng bù 2 và cờ tràn\n\n"
        "Viết chương trình Python mô phỏng bộ cộng 8 bit phát hiện cả **tràn có dấu (OV)** và **nhớ không dấu (CF)** cho `(100 + 50)` và phép trừ `40 - 15`, in đúng 3 dòng:\n"
        "1. `add_100_50=150 ov_signed=1 cf_unsigned=0`\n2. `sub_40_15=25`\n3. `add_200_100=44 cf_unsigned=1`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh CSA L06 duong_dan/bai_cua_ban.py\n```",
        "def add8(a, b):\n    s = (a + b) & 0xFF\n    cf = int(a + b > 255)\n    sa, sb, ss = (a >> 7) & 1, (b >> 7) & 1, (s >> 7) & 1\n    ov = int(sa == sb and ss != sa)\n    return s, ov, cf\n"
        "s1, ov1, cf1 = add8(100, 50)\n"
        "s2, _, _ = add8(40, ((~15) + 1) & 0xFF)\n"
        "s3, _, cf3 = add8(200, 100)\n"
        "print(f'add_100_50={s1} ov_signed={ov1} cf_unsigned={cf1}')\nprint(f'sub_40_15={s2}')\nprint(f'add_200_100={s3} cf_unsigned={cf3}')\n",
        None,
    ),
    (
        "L07", "py", "(Mô phỏng định lượng) Bộ đếm lệnh vòng lặp trên thanh ghi tập lệnh",
        "# Lab CSA L07 (Mô phỏng ISA nhỏ) — Đếm tổng số lệnh thực thi của vòng lặp\n\n"
        "Viết chương trình Python mô phỏng đoạn hợp ngữ khởi tạo `R1=0, R2=1` (1 lệnh nạp mỗi thanh ghi → 2 lệnh đầu) rồi chạy vòng lặp `while R2 <= 10` (`N=10` lượt, mỗi lượt gồm `ADD` cộng, `ADDI` tăng 1, `BLE` nhảy nếu ≤ = 3 lệnh), in đúng 3 dòng:\n"
        "1. `sum_1_to_10=55`\n2. `loop_iters=10`\n3. `total_dynamic_insts=32`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh CSA L07 duong_dan/bai_cua_ban.py\n```",
        "r1, r2, dyn, iters = 0, 1, 2, 0\n"
        "while r2 <= 10:\n    r1 += r2\n    r2 += 1\n    dyn += 3\n    iters += 1\n"
        "print(f'sum_1_to_10={r1}')\nprint(f'loop_iters={iters}')\nprint(f'total_dynamic_insts={dyn}')\n",
        None,
    ),
    (
        "L08", "py", "(Mô phỏng định lượng) Thời gian CPU = số lệnh IC × CPI / tần số f",
        "# Lab CSA L08 (Mô phỏng hiệu năng CPU) — Tính CPI trung bình và thời gian chạy\n\n"
        "Viết chương trình Python cho chương trình có tổng số lệnh `IC = 1e9` gồm `50%` số học (`CPI = 1`), `30%` tải/lưu (`CPI = 3`), `20%` nhánh (`CPI = 2`) chạy trên CPU `2.0 GHz` (`2e9 Hz`), in đúng 3 dòng:\n"
        "1. `cpi_avg=1.80`\n2. `cpu_time_s=0.900`\n3. `speedup_vs_3ghz_cpi3=1.11`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh CSA L08 duong_dan/bai_cua_ban.py\n```",
        "cpi = 0.50 * 1 + 0.30 * 3 + 0.20 * 2\nt_a = 1e9 * cpi / 2e9\nt_b = 1e9 * 3.0 / 3e9\n"
        "print(f'cpi_avg={cpi:.2f}')\nprint(f'cpu_time_s={t_a:.3f}')\nprint(f'speedup_vs_3ghz_cpi3={t_b / t_a:.2f}')\n",
        None,
    ),
    (
        "L09", "py", "(Mô phỏng định lượng) Số chu kỳ đường ống k tầng và tăng tốc",
        "# Lab CSA L09 (Mô phỏng Pipeline k tầng) — Chu kỳ lý tưởng và độ trễ xung đột\n\n"
        "Viết chương trình Python tính số chu kỳ hoàn thành `N = 100` lệnh trên đường ống `k = 5` tầng (`k + N - 1`), so với thực thi không đường ống (`k * N`) và khi gặp 12 lần dừng 1 chu kỳ (stall), in đúng 3 dòng:\n"
        "1. `cycles_no_pipe=500`\n2. `cycles_pipe_ideal=104 speedup=4.81`\n3. `cycles_with_12_stalls=116`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh CSA L09 duong_dan/bai_cua_ban.py\n```",
        "k, n = 5, 100\nno_p = k * n\nid_p = k + n - 1\n"
        "print(f'cycles_no_pipe={no_p}')\nprint(f'cycles_pipe_ideal={id_p} speedup={no_p / id_p:.2f}')\nprint(f'cycles_with_12_stalls={id_p + 12}')\n",
        None,
    ),
    (
        "L10", "py", "(Mô phỏng định lượng) Phân cấp bộ nhớ và thời gian truy cập trung bình AMAT",
        "# Lab CSA L10 (Mô phỏng phân cấp bộ nhớ) — Tính thời gian truy cập trung bình AMAT\n\n"
        "Viết chương trình Python tính AMAT cho phân cấp L1 (`hit = 1 ns`, tỉ lệ trượt `5%`) → L2 (`hit = 10 ns`, tỉ lệ trượt cục bộ `20%`) → RAM (`100 ns`), in đúng 3 dòng:\n"
        "1. `l2_amat_ns=30.0`\n2. `total_amat_ns=2.50`\n3. `locality_speedup_vs_ram=40.0`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh CSA L10 duong_dan/bai_cua_ban.py\n```",
        "l2_amat = 10.0 + 0.20 * 100.0\ntot = 1.0 + 0.05 * l2_amat\n"
        "print(f'l2_amat_ns={l2_amat:.1f}')\nprint(f'total_amat_ns={tot:.2f}')\nprint(f'locality_speedup_vs_ram={100.0 / tot:.1f}')\n",
        None,
    ),
    (
        "L11", "py", "(Mô phỏng định lượng) Bộ nhớ đệm ánh xạ trực tiếp (Tag/Index/Offset)",
        "# Lab CSA L11 (Mô phỏng Cache ánh xạ trực tiếp) — Tách thẻ (Tag), chỉ số (Index), độ dời (Offset) và đếm trúng/trượt\n\n"
        "Viết chương trình Python mô phỏng cache ánh xạ trực tiếp có `8` dòng (`index` = chỉ số `3 bit`), kích thước khối `16 byte` (`offset` = độ dời `4 bit`, phần còn lại là `tag` = thẻ). Cho chuỗi địa chỉ `[0x00, 0x04, 0x80, 0x08]`, đếm tổng số trượt do xung đột ghi đè lên ngăn đã có dữ liệu (`conflict_at_0x80` = tổng xung đột tại chỉ số 0 khi `0x80` và `0x08` lần lượt đẩy nhau), in đúng 3 dòng:\n"
        "1. `split_0x84=tag:1,idx:0,off:4`\n2. `hits=1 misses=3`\n3. `conflict_at_0x80=2`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh CSA L11 duong_dan/bai_cua_ban.py\n```",
        "def split_a(a): return (a >> 7), ((a >> 4) & 0x7), (a & 0xF)\nt1, i1, o1 = split_a(0x84)\ntags = [None] * 8; hits = misses = conf = 0\n"
        "for a in [0x00, 0x04, 0x80, 0x08]:\n    tg, idx, _ = split_a(a)\n    if tags[idx] == tg: hits += 1\n"
        "    else:\n        if tags[idx] is not None: conf += 1\n        misses += 1; tags[idx] = tg\n"
        "print(f'split_0x84=tag:{t1},idx:{i1},off:{o1}')\nprint(f'hits={hits} misses={misses}')\nprint(f'conflict_at_0x80={conf}')\n",
        None,
    ),
    (
        "L12", "py", "(Mô phỏng định lượng) Cache kết hợp 2 đường và chính sách LRU",
        "# Lab CSA L12 (Mô phỏng Cache 2 đường LRU) — So sánh giảm conflict miss so với ánh xạ trực tiếp\n\n"
        "Viết chương trình Python mô phỏng cache 2-way (mỗi set 2 slot, LRU) giải cùng chuỗi ping-pong hai địa chỉ ánh xạ cùng set `idx = 0`: `[0x00, 0x80, 0x00, 0x80]`, in đúng 3 dòng:\n"
        "1. `direct_mapped_hits=0 misses=4`\n2. `two_way_lru_hits=2 misses=2`\n3. `final_set0_order=0x00,0x80`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh CSA L12 duong_dan/bai_cua_ban.py\n```",
        "seq = [0x00, 0x80, 0x00, 0x80]\ndm = None; dh = dm_m = 0\nfor a in seq:\n    tg = a >> 7\n    if dm == tg: dh += 1\n    else: dm_m += 1; dm = tg\n"
        "lru = []; lh = lm = 0\nfor a in seq:\n    tg = a >> 7\n    if tg in lru: lh += 1; lru.remove(tg); lru.append(tg)\n    else:\n        lm += 1\n        if len(lru) == 2: lru.pop(0)\n        lru.append(tg)\n"
        "print(f'direct_mapped_hits={dh} misses={dm_m}')\nprint(f'two_way_lru_hits={lh} misses={lm}')\nprint('final_set0_order=' + ','.join(f'0x{t<<7:02X}' for t in lru))\n",
        None,
    ),
    (
        "L13", "py", "(Mô phỏng định lượng) Định luật Amdahl và giới hạn tăng tốc song song",
        "# Lab CSA L13 (Mô phỏng Amdahl) — Tính tăng tốc theo số nhân và trần giới hạn\n\n"
        "Viết chương trình Python với phần song song `p = 0.80` (tức phần tuần tự `s = 0.20`), tính hệ số tăng tốc ở `4`, `16` nhân và giới hạn khi `n → ∞`, in đúng 3 dòng:\n"
        "1. `speedup_4=2.50`\n2. `speedup_16=4.00`\n3. `max_limit=5.00`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh CSA L13 duong_dan/bai_cua_ban.py\n```",
        "def amdahl(p, n): return 1.0 / ((1.0 - p) + p / n)\n"
        "print(f'speedup_4={amdahl(0.80, 4):.2f}')\nprint(f'speedup_16={amdahl(0.80, 16):.2f}')\nprint(f'max_limit={1.0 / (1.0 - 0.80):.2f}')\n",
        None,
    ),
    (
        "L14", "py", "(Mô phỏng định lượng) Dịch địa chỉ ảo (VPN), bảng trang và thời gian hiệu dụng TLB (EAT)",
        "# Lab CSA L14 (Mô phỏng bộ nhớ ảo & TLB) — Dịch địa chỉ 4 KB (VPN -> khung vật lý) và tính EAT\n\n"
        "Viết chương trình Python với trang `4 096 byte`, số trang ảo VPN `0x05` ánh xạ vào khung vật lý `0x12`, dịch địa chỉ ảo `0x5ABC` và tính thời gian truy cập hiệu dụng EAT khi `TLB hit = 98%` (TLB 1 ns, RAM 100 ns), in đúng 3 dòng:\n"
        "1. `vpn=0x05 offset=0xABC`\n2. `phys_addr=0x12ABC`\n3. `eat_ns=103.00`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh CSA L14 duong_dan/bai_cua_ban.py\n```",
        "va = 0x5ABC; vpn = va >> 12; off = va & 0xFFF; pfn = 0x12; pa = (pfn << 12) | off\n"
        "eat = 0.98 * (1 + 100) + 0.02 * (1 + 100 + 100)\n"
        "print(f'vpn=0x{vpn:02X} offset=0x{off:03X}')\nprint(f'phys_addr=0x{pa:05X}')\nprint(f'eat_ns={eat:.2f}')\n",
        None,
    ),
    (
        "L15", "py", "(Mô phỏng định lượng) So sánh chi phí CPU giữa Thăm dò, Ngắt và DMA",
        "# Lab CSA L15 (Mô phỏng I/O) — So sánh phần trăm CPU bận giữa Polling, Interrupt và DMA\n\n"
        "Viết chương trình Python tính thời gian CPU tốn mỗi giây trên CPU `1 GHz` khi truyền `1 000 KB/s`: Ngắt từng khối `4 KB` tốn `1 000` chu kỳ/lần so với DMA chỉ báo ngắt 1 lần sau `1 000 KB` (cộng `500` chu kỳ thiết lập), in đúng 3 dòng:\n"
        "1. `irq_cycles_per_s=250000`\n2. `dma_cycles_per_s=1500`\n3. `dma_saved_pct=99.4%`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh CSA L15 duong_dan/bai_cua_ban.py\n```",
        "irq = (1000 // 4) * 1000\ndma = 500 + 1000\n"
        "print(f'irq_cycles_per_s={irq}')\nprint(f'dma_cycles_per_s={dma}')\nprint(f'dma_saved_pct={100 * (irq - dma) / irq:.1f}%')\n",
        None,
    ),
    (
        "L16", "py", "(Mô phỏng định lượng) Hết bữa trưa miễn phí, đa nhân và bài toán Spectre",
        "# Lab CSA L16 (Mô phỏng kiến trúc chuyên gia) — Đa nhân Amdahl và chênh lệch thời gian cache\n\n"
        "Viết chương trình Python tính tăng tốc giới hạn của phần tuần tự `15%` khi mở rộng sang 8 nhân và mô phỏng độ trễ cache hit (`2 ns`) vs miss (`100 ns`) bộc lộ kênh kề, in đúng 3 dòng:\n"
        "1. `speedup_8cores_p85=3.90`\n2. `limit_inf=6.67`\n3. `cache_timing_ratio=50.0x`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh CSA L16 duong_dan/bai_cua_ban.py\n```",
        "s8 = 1.0 / (0.15 + 0.85 / 8.0)\nlim = 1.0 / 0.15\n"
        "print(f'speedup_8cores_p85={s8:.2f}')\nprint(f'limit_inf={lim:.2f}')\nprint(f'cache_timing_ratio={100.0 / 2.0:.1f}x')\n",
        None,
    ),
]

for lid, ext, hint, de_md, sol, extra in LESSONS:
    extras = (extra,) if extra else ()
    ex_s = "example" if lid != "L16" else "timeline"
    chk_s = "verify" if lid != "L16" else "check"
    cov = [(1, ex_s), (2, chk_s), (3, "practice")]
    fp, lo = up.apply_upgrade(
        "CSA", lid,
        de_md=de_md, ext=ext, sol_code=sol, de_hint=hint,
        covers=cov, extra_scenes=extras,
    )
    print(f"OK CSA {lid}: {fp.name} ({len(lo.splitlines())} dòng)")

led_p, nblk = up.sync_course_ledger("CSA", default_lang="python")
print(f"Synced {led_p.relative_to(ROOT)}: {nblk} blocks")

# Đồng bộ ngược template L05
tpl = subprocess.run([ak.VENV_PY, "-B", "audit/review/sync_tpl_from_lesson.py", "csa", "--write"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
print("sync_tpl CSA:", tpl.stdout.strip() or tpl.stderr.strip())
