"""Kiểm mọi con số dự định đưa lên màn hình của khoá NET bằng tools/checklib.py VÀ một cách tính độc lập.
Chạy: .venv/Scripts/python audit/net/verify_net.py → PASS/FAIL từng mục."""
import hashlib
import ipaddress
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
import checklib as alg  # noqa: E402

R = []


def ok(name, cond):
    R.append((name, bool(cond)))
    print("PASS" if cond else "FAIL", name)


# L00 đóng gói
ok("L00 1460 + 20 + 20 + 18 = 1518", 1460 + 20 + 20 + 18 == 1518)
ok("L00 hiệu suất 1460/1518 ≈ 96,2%", round(100 * 1460 / 1518, 1) == 96.2)
ok("L00 gói nhỏ 40 B dữ liệu: 40/98 ≈ 40,8% (Ethernet tối thiểu 64 B khung + đệm: xem bài)", round(100 * 40 / (40 + 58), 1) == 40.8)
ok("L00 khung Ethernet tối thiểu 64 B: 46 dữ liệu tối thiểu + 18", 46 + 18 == 64)
# L01 trễ
ok("L01 1500 B ở 100 Mbps: 120 µs", math.isclose(1500 * 8 / 100e6, 120e-6))
ok("L01 1000 km ở 2·10^8 m/s: 5 ms", math.isclose(1000e3 / 2e8, 5e-3))
ok("L01 lưu–chuyển 3 liên kết: 3 × 120 µs + 3 × 5 ms = 15,36 ms", math.isclose(3 * 120e-6 + 3 * 5e-3, 15.36e-3))
ok("L01 ở 1 Gbps: 12 µs truyền, lan truyền vẫn 5 ms", math.isclose(1500 * 8 / 1e9, 12e-6))
ok("L01 quiz 1250 B, 10 Mbps: 1 ms; 300 km cáp quang 2·10^8: 1,5 ms; tổng 2,5 ms",
   math.isclose(1250 * 8 / 10e6, 1e-3) and math.isclose(300e3 / 2e8, 1.5e-3))
# L02 thông lượng
ok("L02 100 Mbps × 50 ms = 625 000 B", 100e6 * 50e-3 / 8 == 625000)
ok("L02 đoạn chậm nhất: min(100, 20, 1000) = 20 Mbps", min(100, 20, 1000) == 20)
ok("L02 tệp 25 MB qua 20 Mbps: 10 s", 25e6 * 8 / 20e6 == 10)
ok("L02 quiz 1 Gbps × 100 ms = 12,5 MB", 1e9 * 0.1 / 8 == 12.5e6)
# L03 CRC
rem, tr = alg.crc_remainder("11010011101100", "1011")
ok("L03 CRC 11010011101100 / 1011 → 100", rem == "100")
ok("L03 bên nhận: từ mã đúng → dư 000", alg.crc_check("11010011101100" + rem, "1011") == "000")
bad = list("11010011101100100"); bad[3] = "1" if bad[3] == "0" else "0"
ok("L03 lật 1 bit → dư khác 000", alg.crc_check("".join(bad), "1011") != "000")


def poly_mod2(a, b):
    """chia đa thức hệ số GF(2) bằng số nguyên (độc lập với crc_remainder)."""
    a, b = int(a, 2), int(b, 2)
    while a.bit_length() >= b.bit_length():
        a ^= b << (a.bit_length() - b.bit_length())
    return a


ok("L03 đối chiếu bằng số nguyên GF(2): dư = 0b100", poly_mod2("11010011101100" + "000", "1011") == 0b100)
ok("L03 CRC phát hiện MỌI lỗi 1 bit (17 vị trí)", all(alg.crc_check("".join(c if i != j else ("1" if c == "0" else "0") for i, c in enumerate("11010011101100100")), "1011") != "000" for j in range(17)))
ok("L03 chẵn lẻ: 1011001 có 4 bit 1 → bit chẵn lẻ 0", "1011001".count("1") % 2 == 0)
ok("L03 chẵn lẻ bỏ sót lỗi 2 bit", ("1011001".count("1") + 2) % 2 == 0)
s, c = alg.inet_checksum([0x4500, 0x0073, 0x0000, 0x4000, 0x4011, 0x0000, 0xC0A8, 0x0001, 0xC0A8, 0x00C7])
ok("L03 checksum IPv4 mẫu (Wikipedia): 0xB861", c == 0xB861)
ok("L03 quiz CRC 101110 / 1001 → 011", alg.crc_remainder("101110", "1001")[0] == "011" and poly_mod2("101110000", "1001") == 0b011)
# L04 ALOHA, chuyển mạch
ok("L04 ALOHA thuần max 1/(2e) ≈ 0,184 tại G = 0,5", round(1 / (2 * math.e), 3) == 0.184 and
   max(G / 1000 * math.exp(-2 * G / 1000) for G in range(1, 3000)) <= 1 / (2 * math.e) + 1e-9)
ok("L04 ALOHA chia khe max 1/e ≈ 0,368 tại G = 1", round(1 / math.e, 3) == 0.368)
sw = alg.learn_switch([("A", "B", 1), ("B", "A", 2), ("A", "B", 1), ("C", "A", 1)])
ok("L04 chuyển mạch tự học: tràn, gửi cổng 1, gửi cổng 2, lọc", [a for a, _ in sw] == ["tràn", "gửi cổng 1", "gửi cổng 2", "lọc"])
ok("L04 lùi ngẫu nhiên lần va chạm thứ 3: chọn trong 0..7 (2^3 khả năng)", len(range(2 ** 3)) == 8)
# L05 IPv4
ok("L05 192.168.10.0/26: mạng .0, quảng bá .63, 62 máy", alg.subnet("192.168.10.0/26")[:3] == ("192.168.10.0", "192.168.10.63", 62))
ok("L05 /24 chia /26: 4 mạng con", alg.split_subnets("192.168.10.0/24", 26) == ["192.168.10.0/26", "192.168.10.64/26", "192.168.10.128/26", "192.168.10.192/26"])
ok("L05 2^(32−26) − 2 = 62", 2 ** (32 - 26) - 2 == 62)
ok("L05 192.168.10.77 nằm trong mạng con .64/26", ipaddress.ip_address("192.168.10.77") in ipaddress.ip_network("192.168.10.64/26"))
ok("L05 mặt nạ /26 = 255.255.255.192", str(ipaddress.ip_network("0.0.0.0/26").netmask) == "255.255.255.192")
ok("L05 quiz 10.0.0.0/22: quảng bá 10.0.3.255, 1022 máy", alg.subnet("10.0.0.0/22")[1:3] == ("10.0.3.255", 1022))
ok("L05 /31: 2 địa chỉ, dùng cả hai cho liên kết điểm–điểm (RFC 3021)", ipaddress.ip_network("10.0.0.0/31").num_addresses == 2)
# L06 khớp tiền tố dài nhất
T6 = [("200.23.16.0/20", "A"), ("200.23.24.0/21", "B"), ("0.0.0.0/0", "mặc định")]
ok("L06 200.23.25.7 khớp /20, /21, /0 → B", alg.lpm(T6, "200.23.25.7")[0] == "B" and len(alg.lpm(T6, "200.23.25.7")[2]) == 3)
ok("L06 200.23.18.1 chỉ khớp /20 (và /0) → A", alg.lpm(T6, "200.23.18.1")[0] == "A")
ok("L06 8.8.8.8 → mặc định", alg.lpm(T6, "8.8.8.8")[0] == "mặc định")
ok("L06 gom 4 khối /24 liền nhau 200.23.16–19 thành /22", list(ipaddress.collapse_addresses(
    [ipaddress.ip_network(f"200.23.{i}.0/24") for i in range(16, 20)])) == [ipaddress.ip_network("200.23.16.0/22")])
ok("L06 quiz 200.23.31.200 → B; 200.23.32.1 → mặc định", alg.lpm(T6, "200.23.31.200")[0] == "B" and alg.lpm(T6, "200.23.32.1")[0] == "mặc định")
# L07 trạng thái liên kết (bản đồ CS112 bài 24, vô hướng)
E7 = [("S", "A", 4), ("S", "B", 1), ("A", "C", 1), ("A", "B", 2), ("B", "C", 5), ("B", "D", 8), ("C", "D", 3)]
G7 = alg.undirected(E7)
ok("L07 bảng chuyển tiếp của S: mọi đích đi qua B; chi phí A3 B1 C4 D7",
   alg.next_hops(G7, "S") == {"A": ("B", 3), "B": ("B", 1), "C": ("B", 4), "D": ("B", 7)})
ok("L07 bảng của D: A qua C (4), B qua C (6), C (3), S qua C (7)",
   alg.next_hops(G7, "D") == {"A": ("C", 4), "B": ("C", 6), "C": ("C", 3), "S": ("C", 7)})
ok("L07 đối chiếu alg.dijkstra (bản có hướng hai chiều)", {v: d for v, d in alg.dijkstra(G7, "S")[0].items()} == {"S": 0, "A": 3, "B": 1, "C": 4, "D": 7})
ok("L07 số thông báo trạng thái liên kết: 5 bộ định tuyến × 7 liên kết... mỗi bộ phát 1 gói, mỗi gói qua 7 liên kết × 2 chiều tối đa", 5 * 7 * 2 == 70)
G7b = alg.undirected([("S", "A", 4), ("S", "B", 1), ("A", "C", 1), ("A", "B", 2), ("B", "C", 5), ("B", "D", 8), ("C", "D", 3)])
G7b["S"]["B"] = G7b["B"]["S"] = 10
ok("L07 quiz: S–B tăng lên 10 → S đi A trực tiếp (4), C qua A (5), B qua A (6), D qua A (8)",
   alg.next_hops(G7b, "S") == {"A": ("A", 4), "B": ("A", 6), "C": ("A", 5), "D": ("A", 8)})
# L08 vectơ khoảng cách
ct = alg.count_to_infinity(6)
ok("L08 đếm tới vô cùng: (1,2) → (3,2) → (3,4) → (5,4) → (5,6)", ct[:5] == [(1, 2), (3, 2), (3, 4), (5, 4), (5, 6)])
ok("L08 tới 16 (vô cùng của RIP) sau 15 vòng", alg.count_to_infinity(20)[15][0] >= 16 or alg.count_to_infinity(20)[16] == (16, 16))
ok("L08 đầu độc ngược: B thấy ∞ ngay vòng 1, C ở vòng 2", alg.count_to_infinity(3, poison=True)[:3] == [(1, 2), (16, 2), (16, 16)])
ok("L08 Bellman-Ford: D_x(y) = min_v (c(x,v) + D_v(y)) — ví dụ min(1 + 4, 5 + 2) = 5", min(1 + 4, 5 + 2) == 5)
ok("L08 quiz min(2 + 3, 1 + 6, 4 + 0) = 4", min(2 + 3, 1 + 6, 4 + 0) == 4)
# L09 TCP/UDP
ok("L09 bắt tay: seq x=100 → ack 101; seq y=300 → ack 301", (100 + 1, 300 + 1) == (101, 301))
ok("L09 đầu UDP 8 B, TCP tối thiểu 20 B", (8, 20) == (8, 20))
ok("L09 sau 500 B dữ liệu từ seq 101: ack 601", 101 + 500 == 601)
ok("L09 cổng 16 bit: 65536 giá trị", 2 ** 16 == 65536)
# L10 dừng–chờ, cửa sổ
u = alg.stop_wait_util(8000, 1e9, 0.030)
ok("L10 dừng–chờ 8000 bit, 1 Gbps, RTT 30 ms: ≈ 0,00027", round(u, 5) == 0.00027)
ok("L10 thông lượng thực ≈ 267 kbps", round(8000 / 0.030008 / 1e3) == 267)
ok("L10 cửa sổ cần để đầy đường: ⌈(RTT + t)/t⌉ = 3751 gói", math.ceil((0.030 + 8e-6) / 8e-6) == 3751)
ok("L10 cửa sổ 100 gói: hiệu suất ≈ 0,027", round(alg.window_util(100, 8000, 1e9, 0.030), 3) == 0.027)
ok("L10 quiz 12000 bit, 10 Mbps, RTT 10 ms: t = 1,2 ms; U = 1,2/11,2 ≈ 0,107", round(alg.stop_wait_util(12000, 10e6, 0.010), 3) == 0.107)
ok("L10 quiz: cửa sổ ⌈11,2/1,2⌉ = 10 gói", math.ceil(11.2 / 1.2) == 10)
# L11 tắc nghẽn
ok("L11 khởi động chậm tới 16 rồi tăng cộng: 1, 2, 4, 8, 16, 17", alg.cwnd_trace(6, 16) == [1, 2, 4, 8, 16, 17])
ok("L11 mất ở cửa sổ 20 (Reno): xuống 10 rồi 11, 12", alg.cwnd_trace(12, 16, loss_at=(8,))[8:12] == [20, 10, 11, 12])
ok("L11 Tahoe: về 1, khởi động chậm tới ngưỡng mới 10", alg.cwnd_trace(14, 16, loss_at=(8,), variant="tahoe")[8:14] == [20, 1, 2, 4, 8, 10])
ok("L11 quiz ngưỡng 8, mất ở cửa sổ 12 (Reno): 1, 2, 4, 8, 9, 10, 11, 12, 6, 7", alg.cwnd_trace(10, 8, loss_at=(7,)) == [1, 2, 4, 8, 9, 10, 11, 12, 6, 7])
# L12 HTTP, DNS
ok("L12 HTTP không bền, 10 đối tượng: 22 RTT", alg.http_rtts(10) == 22 == 2 + 10 * 2)
ok("L12 HTTP bền: 12 RTT; bền + đường ống: 3 RTT", alg.http_rtts(10, True) == 12 and alg.http_rtts(10, True, True) == 3)
ok("L12 phân giải lặp: gốc, TLD, máy chủ có thẩm quyền = 3 lượt hỏi", len(["gốc", "TLD", "thẩm quyền"]) == 3)
ok("L12 quiz 5 đối tượng: không bền 12, bền 7", alg.http_rtts(5) == 12 and alg.http_rtts(5, True) == 7)
# L13 Diffie–Hellman
ok("L13 DH p=23 g=5 a=6 b=15: 8, 19, khoá 2", alg.dh(23, 5, 6, 15) == (8, 19, 2, 2))
ok("L13 đối chiếu bằng tay: 5^6 = 15625 = 679·23 + 8", 5 ** 6 == 15625 and 15625 % 23 == 8)
ok("L13 quiz p=23 g=5 a=4 b=3: gửi 4 và 10, khoá 18", alg.dh(23, 5, 4, 3) == (4, 10, 18, 18))
ok("L13 khoá đối xứng 128 bit: 2^128 ≈ 3,4·10^38", f"{2 ** 128:.1e}" == "3.4e+38")
# L14 băm, chữ ký
ok("L14 RSA n=33 e=3 d=7: ký 4 → 16; kiểm 16^3 mod 33 = 4", alg.rsa_toy(33, 3, 7, 4) == (16, 4))
ok("L14 e·d = 21 ≡ 1 mod φ(33) = 20", (3 * 7) % ((3 - 1) * (11 - 1)) == 1)
ok("L14 SHA-256('abc') bắt đầu ba7816bf", hashlib.sha256(b"abc").hexdigest().startswith("ba7816bf"))
h1, h2 = hashlib.sha256(b"abc").digest(), hashlib.sha256(b"abd").digest()
diff = sum(bin(x ^ y).count("1") for x, y in zip(h1, h2))
ok(f"L14 đổi 1 ký tự abc→abd: {diff}/256 bit đầu ra đổi (gần một nửa)", 100 <= diff <= 156)
ok("L14 quiz: ký 2 → 2^7 mod 33 = 29; kiểm 29^3 mod 33 = 2", alg.rsa_toy(33, 3, 7, 2) == (29, 2))
# L15 hành trình kiểm soát tắc nghẽn (nguồn: audit/net/sources_L15.md) — mỗi số tính hai cách
ok("L15 1986: 32 000 → 40 bit/s giảm 800 lần; nhân ngược 40·800", 32000 / 40 == 800 and 40 * 800 == 32000)
ok("L15 J88 hình 8: 25/4 = 6,25; nhận 8+5+5+0,5 = 18,5; mất 6,5 (nguồn ghi tròn 6)",
   25 / 4 == 6.25 and math.isclose(sum([8, 5, 5, 0.5]), 18.5) and math.isclose(25 - 18.5, 6.5))
ok("L15 J88 hình 8: 4000 gửi lại / 7000 gói mới ≈ 0,57 (“khoảng một nửa”)", round(4000 / (11000 - 4000), 2) == 0.57)
_w, _r = 1, 0
while _w < 16:
    _w, _r = 2 * _w, _r + 1
ok("L15 khởi động chậm 1 → 16 gói: 4 vòng (đếm bằng vòng lặp); 4 × 100 ms = 400 ms", (_w, _r) == (16, 4) and _r * 100 == 400)
ok("L15 bộ đệm W/2 khi mở cửa sổ 16: 8 gói; hình 4: 16/7 ≈ 2,3 lần", 16 // 2 == 8 and round(16 / 7, 1) == 2.3)
ok("L15 BDP 10 Gbit/s × 100 ms = 125 MB; đổi trước ra byte: 1,25 GB/s × 0,1", 10e9 * 0.1 / 8 == 125e6 and math.isclose(10e9 / 8 * 0.1, 125e6))
ok("L15 G17: 9100 / 3,3 ≈ 2758 (“2700x”); CUBIC dùng 0,033% đường", round(9100 / 3.3) == 2758 and round(100 * 3.3 / 10000, 3) == 0.033)
ok("L15 đường vào nhà 10 Mbit/s × 40 ms = 50 000 B ≈ 33,3 gói 1500 B (minh hoạ)", 10e6 * 0.04 / 8 == 50000 and round(50000 / 1500, 1) == 33.3)
ok("L15 xả 1000 gói × 1500 B ở 10 Mbit/s = 1,2 s = 1000 × 1,2 ms; vòng ≤ 1240 ms",
   math.isclose(1000 * 1500 * 8 / 10e6, 1.2) and math.isclose(1000 * (1500 * 8 / 10e6), 1.2) and 40 + 1200 == 1240)
ok("L15 G17: trung vị 1090 / 43 ≈ 25,3 (“25x”)", round(1090 / 43, 1) == 25.3)
_iw = lambda mds: min(10 * mds, max(14720, 2 * mds))
ok("L15 RFC 9002 §7.2 cửa sổ đầu: gói 1200 → 12 000 B; gói 1472 → 14 720 B", (_iw(1200), _iw(1472)) == (12000, 14720))
ok("L15 RFC 9002 hệ số giảm 0,5 = J88 d = 0,5: mất ở 20 → 10", 20 * 0.5 == 10)
ok("L15 nhập nhằng gửi lại: 350 ms hay 350 − 300 = 50 ms, sai gấp 7", 350 - 300 == 50 and 350 / 50 == 7)
_sent, _cw, _rounds = 0, 12000, 0
while _sent < 20000:
    _sent, _cw, _rounds = _sent + _cw, 2 * _cw, _rounds + 1
ok("L15 quiz: 20 000 B với cửa sổ đầu 12 000 B, khởi động chậm → 2 vòng; 12 000 B → 1 vòng", _rounds == 2 and 12000 <= _iw(1200))
print(f"\n{sum(c for _, c in R)}/{len(R)} PASS")
