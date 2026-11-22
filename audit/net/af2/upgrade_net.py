"""Nâng trọn bộ 16 bài NET (L00–L15) lên chuẩn AF2 theo bảng quyết định BN-08.

- L09 dùng socket TCP thật trên loopback 127.0.0.1; các bài giao thức / định tuyến /
  mật mã đồ chơi kiểm chứng định lượng bằng Python tất định kèm nhãn rõ ràng.
- Giữ nguyên toàn bộ cảnh gốc đã duyệt, gắn `covers`, `practice`, đồng bộ sổ
  `screen_code/NET.yaml` và template `curriculum/net.yaml`.
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "audit" / "review"))
import af2_kit as ak  # noqa: E402
import af2_upgrader as up  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")

LESSONS = [
    (
        "L00", "py", "(Mô phỏng định lượng) Hiệu suất khung Ethernet đầy = 1460 / 1518 = 96.2%",
        "# Lab NET L00 (Mô phỏng đóng gói) — Tính phần đầu và hiệu suất khung Ethernet\n\n"
        "Viết chương trình Python tính tổng phần đầu TCP (`20 B`), IP (`20 B`), Ethernet (`18 B`) "
        "khi chở `1 460 B` dữ liệu và hiệu suất khung đầy `1 518 B`, in đúng 3 dòng:\n"
        "1. `headers_B=58`\n2. `frame_B=1518`\n3. `efficiency_pct=96.2%`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh NET L00 duong_dan/bai_cua_ban.py\n```",
        "hdr = 20 + 20 + 18; frame = 1460 + hdr\n"
        "print(f'headers_B={hdr}')\nprint(f'frame_B={frame}')\n"
        "print(f'efficiency_pct={100 * 1460 / frame:.1f}%')\n",
    ),
    (
        "L01", "py", "(Mô phỏng định lượng) Trễ truyền = L/R, còn trễ lan truyền = d/s",
        "# Lab NET L01 (Mô phỏng trễ mạng) — Phân biệt trễ truyền và trễ lan truyền\n\n"
        "Viết chương trình Python tính trễ truyền gói `1 500 B` trên đường `100 Mbps`, "
        "trễ lan truyền trên `1 000 km` (tốc độ `2e8 m/s`) và tổng 1 chặng, in đúng 3 dòng:\n"
        "1. `tx_us=120.0`\n2. `prop_ms=5.0`\n3. `total_ms=5.12`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh NET L01 duong_dan/bai_cua_ban.py\n```",
        "tx = (1500 * 8) / 100e6\nprop = 1000e3 / 2e8\n"
        "print(f'tx_us={tx * 1e6:.1f}')\nprint(f'prop_ms={prop * 1e3:.1f}')\n"
        "print(f'total_ms={(tx + prop) * 1e3:.2f}')\n",
    ),
    (
        "L02", "py", "(Mô phỏng định lượng) Thông lượng bằng nút thắt cổ chai min(R1, R2)",
        "# Lab NET L02 (Mô phỏng thông lượng & BDP) — Đường ống chậm nhất và dữ liệu đang bay\n\n"
        "Viết chương trình Python tính thông lượng đầu–cuối qua tuyến gồm hai chặng `500 Mbps` và `100 Mbps`, "
        "và lượng dữ liệu đang bay (tích băng thông–trễ BDP) với thời gian một vòng đi–về `RTT = 50 ms`, in đúng 3 dòng:\n"
        "1. `bottleneck_mbps=100`\n2. `bdp_bits=5000000`\n3. `bdp_bytes=625000`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh NET L02 duong_dan/bai_cua_ban.py\n```",
        "bn = min(500, 100); bdp_b = bn * 1_000_000 * 50 // 1000\n"
        "print(f'bottleneck_mbps={bn}')\nprint(f'bdp_bits={bdp_b}')\n"
        "print(f'bdp_bytes={bdp_b // 8}')\n",
    ),
    (
        "L03", "py", "(Mô phỏng định lượng) Phép chia XOR CRC với đa thức sinh 1011",
        "# Lab NET L03 (Mô phỏng phát hiện lỗi) — Chia đa thức XOR tính CRC 3 bit\n\n"
        "Viết chương trình Python cài phép chia XOR CRC với chuỗi `11010011101100` và đa thức sinh `1011`: "
        "tính phần dư bên gửi, khung `17` bit gửi đi và kiểm tra bên nhận chia lại ra `000`, in đúng 3 dòng:\n"
        "1. `crc_rem=100`\n2. `tx_frame_len=17`\n3. `rx_ok=1`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh NET L03 duong_dan/bai_cua_ban.py\n```",
        "def crc_rem(bits, gen='1011'):\n    b = list(bits)\n    for i in range(len(bits) - len(gen) + 1):\n"
        "        if b[i] == '1':\n            for j in range(len(gen)): b[i+j] = '1' if b[i+j] != gen[j] else '0'\n"
        "    return ''.join(b[-(len(gen)-1):])\n"
        "d = '11010011101100'; r = crc_rem(d + '000'); tx = d + r\n"
        "print(f'crc_rem={r}')\nprint(f'tx_frame_len={len(tx)}')\nprint(f'rx_ok={int(crc_rem(tx) == \"000\")}')\n",
    ),
    (
        "L04", "py", "(Mô phỏng định lượng) ALOHA thuần 1/(2e) ≈ 18.4%, chia khe 1/e ≈ 36.8%",
        "# Lab NET L04 (Mô phỏng truy cập đường truyền) — Hiệu suất ALOHA và Switch MAC\n\n"
        "Viết chương trình Python tính hiệu suất tối đa lý thuyết của ALOHA thuần (`1/(2e)`), "
        "ALOHA chia khe (`1/e`) và mô phỏng bảng MAC của Switch (bộ chuyển mạch) học địa chỉ qua 3 khung (2 địa chỉ MAC khác nhau), in đúng 3 dòng:\n"
        "1. `pure_aloha_pct=18.4%`\n2. `slotted_aloha_pct=36.8%`\n3. `switch_mac_entries=2`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh NET L04 duong_dan/bai_cua_ban.py\n```",
        "import math\ntbl = {}\nfor src, port in (('AA:01', 1), ('BB:02', 3), ('AA:01', 1)): tbl[src] = port\n"
        "print(f'pure_aloha_pct={100 / (2 * math.e):.1f}%')\n"
        "print(f'slotted_aloha_pct={100 / math.e:.1f}%')\n"
        "print(f'switch_mac_entries={len(tbl)}')\n",
    ),
    (
        "L05", "py", "(Mô phỏng định lượng) Chia /24 thành bốn mạng /26, mỗi mạng 62 máy",
        "# Lab NET L05 (Mô phỏng IPv4) — Chia mạng con và tính quảng bá\n\n"
        "Viết chương trình Python bằng thư viện chuẩn `ipaddress` phân tích `192.168.10.0/26` "
        "và đếm số mạng `/26` nằm trong `192.168.10.0/24`, in đúng 3 dòng:\n"
        "1. `net=192.168.10.0 bcast=192.168.10.63`\n2. `usable_hosts=62`\n3. `subnets_in_slash24=4`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh NET L05 duong_dan/bai_cua_ban.py\n```",
        "import ipaddress\nn = ipaddress.IPv4Network('192.168.10.0/26')\n"
        "p = ipaddress.IPv4Network('192.168.10.0/24')\n"
        "print(f'net={n.network_address} bcast={n.broadcast_address}')\n"
        "print(f'usable_hosts={n.num_addresses - 2}')\n"
        "print(f'subnets_in_slash24={len(list(p.subnets(new_prefix=26)))}')\n",
    ),
    (
        "L06", "py", "(Mô phỏng định lượng) Khớp tiền tố dài nhất chọn tuyến cụ thể hơn",
        "# Lab NET L06 (Mô phỏng bảng định tuyến) — Khớp tiền tố dài nhất (LPM)\n\n"
        "Viết chương trình Python tra bảng `{10.1.0.0/20: 'A', 10.1.8.0/21: 'B', 0.0.0.0/0: 'DEFAULT'}` "
        "cho hai đích `10.1.10.5` và `8.8.8.8`, và kiểm tra gom 2 mạng `/24` thành `/23`, in đúng 3 dòng:\n"
        "1. `dst_10_1_10_5=B`\n2. `dst_8_8_8_8=DEFAULT`\n3. `collapsed_prefix=192.168.0.0/23`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh NET L06 duong_dan/bai_cua_ban.py\n```",
        "import ipaddress\n"
        "tbl = [(ipaddress.IPv4Network(p), g) for p, g in (('10.1.0.0/20','A'),('10.1.8.0/21','B'),('0.0.0.0/0','DEFAULT'))]\n"
        "def lpm(ip): return max((n.prefixlen, g) for n, g in tbl if ipaddress.IPv4Address(ip) in n)[1]\n"
        "c = list(ipaddress.collapse_addresses([ipaddress.IPv4Network('192.168.0.0/24'), ipaddress.IPv4Network('192.168.1.0/24')]))\n"
        "print(f'dst_10_1_10_5={lpm(\"10.1.10.5\")}')\nprint(f'dst_8_8_8_8={lpm(\"8.8.8.8\")}')\nprint(f'collapsed_prefix={c[0]}')\n",
    ),
    (
        "L07", "py", "(Mô phỏng định lượng) Dijkstra chọn chi phí nhỏ nhất, không phải ít chặng nhất",
        "# Lab NET L07 (Mô phỏng định tuyến trạng thái liên kết) — Dijkstra trên mạng 5 nút\n\n"
        "Viết chương trình Python chạy thuật toán Dijkstra từ nguồn `S` trên đồ thị 5 nút "
        "`(S-A:4, S-B:1, A-B:2, A-C:1, B-C:5, B-D:8, C-D:3)`, in đúng 3 dòng:\n"
        "1. `dist=A:3,B:1,C:4,D:7`\n2. `next_hop_all=B`\n3. `sa_direct_vs_sb_ba=4_vs_3`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh NET L07 duong_dan/bai_cua_ban.py\n```",
        "import heapq\nadj = {k: [] for k in 'SABCD'}\n"
        "for u, v, w in [('S','A',4),('S','B',1),('A','B',2),('A','C',1),('B','C',5),('B','D',8),('C','D',3)]:\n"
        "    adj[u].append((v, w)); adj[v].append((u, w))\n"
        "d = {'S': 0}; nh = {}; pq = [(0, 'S')]\n"
        "while pq:\n    c, u = heapq.heappop(pq)\n    if c > d.get(u, 99): continue\n"
        "    for v, w in adj[u]:\n"
        "        if c + w < d.get(v, 99):\n"
        "            d[v] = c + w; nh[v] = v if u == 'S' else nh[u]\n"
        "            heapq.heappush(pq, (d[v], v))\n"
        "hops = ''.join(sorted({nh[k] for k in 'ABCD'}))\n"
        "print('dist=' + ','.join(f'{k}:{d[k]}' for k in 'ABCD'))\n"
        "print(f'next_hop_all={hops}')\nprint(f'sa_direct_vs_sb_ba=4_vs_{d[\"A\"]}')\n",
    ),
    (
        "L08", "py", "(Mô phỏng định lượng) Tin xấu làm vòng lặp đếm tới vô cùng (=16 ở RIP)",
        "# Lab NET L08 (Mô phỏng Bellman-Ford) — Đếm tới vô cùng khi liên kết A-B đứt\n\n"
        "Viết chương trình Python mô phỏng hai bộ định tuyến B và C trao đổi khoảng cách tới A "
        "sau khi liên kết A-B đứt (bắt đầu `d_B=1, d_C=2`), mỗi vòng lấy `1 + min` từ hàng xóm đến trần RIP `16`, in đúng 3 dòng:\n"
        "1. `after_round1=B:3,C:2`\n2. `rounds_to_reach_16=15`\n3. `final_vals=16,16`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh NET L08 duong_dan/bai_cua_ban.py\n```",
        "b, c = 1, 2; r = 0; hist = []\n"
        "while min(b, c) < 16:\n    r += 1\n    if r % 2 == 1: b = min(16, c + 1)\n    else: c = min(16, b + 1)\n    hist.append((b, c))\n"
        "print(f'after_round1=B:{hist[0][0]},C:{hist[0][1]}')\n"
        "print(f'rounds_to_reach_16={r}')\nprint(f'final_vals={b},{c}')\n",
    ),
    (
        "L09", "py", "Kết nối TCP thực hiện bắt tay ba bước và giữ luồng tin cậy",
        "# Lab NET L09 — TCP socket loopback (kết nối cục bộ) + tính số thứ tự bắt tay ba bước\n\n"
        "Viết chương trình Python mở một máy chủ ổ cắm TCP (`socket.AF_INET` IPv4, `SOCK_STREAM` TCP) thật trên địa chỉ cục bộ loopback `127.0.0.1`, "
        "gửi/nhận thông điệp `PING` ↔ `PONG` và tính `ack` khi client gửi `SYN seq=100`, server gửi `SYN-ACK seq=500`, in đúng 3 dòng:\n"
        "1. `tcp_echo=PONG`\n2. `syn_ack_ack=101`\n3. `final_ack=501`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh NET L09 duong_dan/bai_cua_ban.py\n```",
        "import socket, threading\ns = socket.socket(); s.settimeout(3.0); s.bind(('127.0.0.1', 0)); s.listen(1); p = s.getsockname()[1]\n"
        "def srv():\n    try:\n        c, _ = s.accept(); _ = c.recv(8); c.sendall(b'PONG'); c.close()\n"
        "    finally:\n        s.close()\n"
        "t = threading.Thread(target=srv, daemon=True); t.start()\n"
        "cl = socket.create_connection(('127.0.0.1', p), timeout=3.0); cl.sendall(b'PING'); msg = cl.recv(8).decode(); cl.close(); t.join(timeout=3.0)\n"
        "print(f'tcp_echo={msg}')\nprint(f'syn_ack_ack={100 + 1}')\nprint(f'final_ack={500 + 1}')\n",
    ),
    (
        "L10", "py", "(Mô phỏng định lượng) Cửa sổ W cần >= BDP (tích băng thông–trễ)/gói mới lấp đầy đường truyền",
        "# Lab NET L10 (Mô phỏng cửa sổ trượt) — So sánh dừng–chờ và cửa sổ phủ BDP (tích băng thông–trễ)\n\n"
        "Viết chương trình Python tính hiệu suất dừng–chờ với gói `8 000 bit`, tốc độ `1 Gbps`, `RTT = 30 ms`, "
        "tính số gói BDP (tích băng thông–trễ = `3 750` gói, lưu ý để đạt 100% cần `W >= 3 750`, bài kiểm chứng dùng `W = 3 750`) và hiệu suất khi cửa sổ `W = 1 000` gói, in đúng 3 dòng:\n"
        "1. `stop_wait_eff=0.00027`\n2. `bdp_packets=3750`\n3. `w1000_eff=26.7%`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh NET L10 duong_dan/bai_cua_ban.py\n```",
        "tx = 8000 / 1e9; rtt = 0.030\n"
        "sw = tx / (rtt + tx)\nbdp_pkts = round((1e9 * rtt) / 8000)\n"
        "print(f'stop_wait_eff={sw:.5f}')\nprint(f'bdp_packets={bdp_pkts}')\n"
        "print(f'w1000_eff={100 * 1000 / bdp_pkts:.1f}%')\n",
    ),
    (
        "L11", "py", "(Mô phỏng định lượng) AIMD (tăng cộng – giảm nhân): tăng tuyến tính khi ổn, giảm nửa khi mất gói",
        "# Lab NET L11 (Mô phỏng tắc nghẽn TCP) — Quỹ đạo cửa sổ tắc nghẽn cwnd qua khởi động chậm và AIMD\n\n"
        "Viết chương trình Python mô phỏng cửa sổ tắc nghẽn `cwnd` bắt đầu từ `1`, ngưỡng chuyển pha `ssthresh = 16`: "
        "mô phỏng `6` RTT đầu theo cơ chế AIMD (tăng cộng – giảm nhân: tăng gấp đôi đến ngưỡng 16 rồi tăng cộng lên 17), sau đó gặp mất gói hết giờ chờ `timeout` (đặt `ssthresh = cwnd // 2`, `cwnd = 1`), in đúng 3 dòng:\n"
        "1. `slowstart_trace=1,2,4,8,16`\n2. `aimd_step1=17`\n3. `after_timeout_ssthresh=8 cwnd=1`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh NET L11 duong_dan/bai_cua_ban.py\n```",
        "cw, ss, tr = 1, 16, [1]\nfor _ in range(5): cw = cw * 2 if cw < ss else cw + 1; tr.append(cw)\n"
        "ss_to, cw_to = cw // 2, 1\n"
        "print('slowstart_trace=' + ','.join(map(str, tr[:-1])))\n"
        "print(f'aimd_step1={tr[-1]}')\n"
        "print(f'after_timeout_ssthresh={ss_to} cwnd={cw_to}')\n",
    ),
    (
        "L12", "py", "(Mô phỏng định lượng) HTTP/1.1 keep-alive (kết nối bền) giảm mạnh số vòng RTT so với không bền",
        "# Lab NET L12 (Mô phỏng DNS & HTTP) — Đếm vòng đi về RTT tải trang HTML + 10 đối tượng\n\n"
        "Viết chương trình Python tính số vòng đi về `RTT` cần thiết khi tải 1 trang HTML + 10 ảnh bằng: "
        "HTTP/1.0 không bền (`2 RTT/mục`) và HTTP/1.1 keep-alive (kết nối bền) tuần tự không đường ống, in đúng 3 dòng:\n"
        "1. `http_nonpersistent_rtt=22`\n2. `http_persistent_seq_rtt=12`\n3. `saved_rtt=10`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh NET L12 duong_dan/bai_cua_ban.py\n```",
        "non_p = 2 + 10 * 2\npers = 2 + 10 * 1\n"
        "print(f'http_nonpersistent_rtt={non_p}')\nprint(f'http_persistent_seq_rtt={pers}')\n"
        "print(f'saved_rtt={non_p - pers}')\n",
    ),
    (
        "L13", "py", "(Mô phỏng định lượng) Diffie-Hellman: g^(ab) mod p tính ra cùng khoá chung",
        "# Lab NET L13 (Mô phỏng trao đổi khoá) — Diffie–Hellman trên tham số nhỏ\n\n"
        "Viết chương trình Python tính các thông điệp công khai `A = g^a mod p`, `B = g^b mod p` và khoá bí mật chung "
        "cho `p = 23, g = 5, a = 6, b = 15`, kiểm chứng hai bên thu cùng một giá trị, in đúng 3 dòng:\n"
        "1. `A=8 B=19`\n2. `shared_alice=2 shared_bob=2`\n3. `keys_match=1`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh NET L13 duong_dan/bai_cua_ban.py\n```",
        "p, g, a, b = 23, 5, 6, 15\nA = pow(g, a, p); B = pow(g, b, p)\n"
        "ka = pow(B, a, p); kb = pow(A, b, p)\n"
        "print(f'A={A} B={B}')\nprint(f'shared_alice={ka} shared_bob={kb}')\nprint(f'keys_match={int(ka == kb)}')\n",
    ),
    (
        "L14", "py", "(Mô phỏng định lượng) Ký dùng khoá bí mật d, kiểm chữ ký dùng khoá công khai e",
        "# Lab NET L14 (Mô phỏng chữ ký số) — RSA (hệ khoá công khai) ký/kiểm chữ ký đồ chơi + băm SHA-256\n\n"
        "Viết chương trình Python dùng RSA (hệ khoá công khai đồ chơi) ký giá trị `m = 4` bằng cặp `(n=33, d=7, e=3)` (`sig = m^d mod n`), "
        "kiểm chữ ký bằng `sig^e mod n == m` và kiểm tra độ dài chuẩn `64` ký tự hệ 16 (`hex`) của SHA-256 trên `'TLS'`, in đúng 3 dòng:\n"
        "1. `sig=16 verify=4`\n2. `valid=1`\n3. `sha256_hex_len=64`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh NET L14 duong_dan/bai_cua_ban.py\n```",
        "import hashlib\nn, d, e, m = 33, 7, 3, 4\n"
        "sig = pow(m, d, n); chk = pow(sig, e, n)\n"
        "h = hashlib.sha256(b'TLS').hexdigest()\n"
        "print(f'sig={sig} verify={chk}')\nprint(f'valid={int(chk == m)}')\nprint(f'sha256_hex_len={len(h)}')\n",
    ),
    (
        "L15", "py", "(Mô phỏng định lượng) Bốn chặng kiểm soát tắc nghẽn 1986 → QUIC RFC 9002",
        "# Lab NET L15 (Mô phỏng tắc nghẽn lịch sử) — Con số bốn chặng 1986 đến QUIC\n\n"
        "Viết chương trình Python tính lại các con số then chốt: tỉ lệ sụp đổ năm 1986 (`32000 -> 40 bit/s`), "
        "BDP đường `10 Gbps × 100 ms`, trễ đệm `1000` gói `1500 B` ở `10 Mbps`, và cửa sổ khởi đầu QUIC (`10 × 1200 B`), in đúng 3 dòng:\n"
        "1. `collapse_1986_drop=800x`\n2. `bdp_10g_100ms_MB=125`\n3. `bufferbloat_s=1.2 quic_iw_B=12000`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh NET L15 duong_dan/bai_cua_ban.py\n```",
        "drop = 32000 // 40\nbdp_mb = (10_000_000_000 * 100 // 1000) // (8 * 1_000_000)\n"
        "bloat = (1000 * 1500 * 8) / 10_000_000\n"
        "print(f'collapse_1986_drop={drop}x')\nprint(f'bdp_10g_100ms_MB={bdp_mb}')\n"
        "print(f'bufferbloat_s={bloat:.1f} quic_iw_B={10 * 1200}')\n",
    ),
]

for lid, ext, hint, de_md, sol in LESSONS:
    if lid == "L15":
        cov = [(1, "stage1"), (2, "check"), (3, "practice")]
    elif lid == "L12":
        cov = [(1, "resolve"), (2, "practice")]
    else:
        cov = [(1, "example"), (2, "verify"), (3, "practice")]
    fp, lo = up.apply_upgrade(
        "NET", lid,
        de_md=de_md, ext=ext, sol_code=sol, de_hint=hint, covers=cov,
    )
    print(f"OK NET {lid}: {fp.name} ({len(lo.splitlines())} dòng)")

led_p, nblk = up.sync_course_ledger("NET", default_lang="python")
print(f"Synced {led_p.relative_to(ROOT)}: {nblk} blocks")

tpl = subprocess.run([ak.VENV_PY, "-B", "audit/review/sync_tpl_from_lesson.py", "net", "--write"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
print("sync_tpl NET:", tpl.stdout.strip() or tpl.stderr.strip())
