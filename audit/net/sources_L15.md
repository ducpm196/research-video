# Nguồn đã đọc nguyên văn cho NET L15 (bài hành trình: kiểm soát tắc nghẽn từ 1986 tới QUIC)

Đọc ngày 2026-11-02 (tải bằng curl, trích chữ bằng pdftotext; câu dưới đây chép nguyên văn từ bản trích). Chỉ trích các câu bài giảng
dựa vào (CITED); mọi con số khác trong bài là phép tính lại (VER, `checks` của bài và `audit/net/verify_net.py` L15) hoặc ghi rõ
“số minh hoạ”. Không nêu tên cá nhân trong lời đọc; tên tác giả chỉ ở `source:` và trên màn hình nguồn.

## [J88] V. Jacobson, M. J. Karels. *Congestion Avoidance and Control.* SIGCOMM '88 (bản sửa nhẹ, tháng 11/1988)
Tải: https://ee.lbl.gov/papers/congavoid.pdf (25 trang). Trang 1 ghi: “This is a very slightly revised version of a paper originally
presented at SIGCOMM '88”.
- Mở đầu (tr. 1): “it is now common to see internet gateways drop 10% of the incoming packets because of local buffer overflows.”
- Mở đầu (tr. 1): “In October of '86, the Internet had the first of what became a series of `congestion collapses'. During this period,
  the data throughput from LBL to UC Berkeley (sites separated by 400 yards and two IMP hops) dropped from 32 Kbps to 40 bps. We were
  fascinated by this sudden factor-of-thousand drop in bandwidth …”
- Mở đầu (tr. 1): “much of the cause lies in transport protocol implementations (not in the protocols themselves)”.
- Tr. 2: “we have put seven new algorithms into the 4BSD TCP: (i) round-trip-time variance estimation (ii) exponential retransmit timer
  backoff (iii) slow-start (iv) more aggressive receiver ack policy (v) dynamic window sizing on congestion (vi) Karn's clamped retransmit
  backoff (vii) fast retransmit”.
- Tr. 2: “By `conservation of packets' we mean that for a connection `in equilibrium' … A new packet isn't put into the network until an old
  packet leaves.”
- §1 (tr. 2–4): “the sender uses acks as a `clock' to strobe new packets into the network.” “When starting or restarting after a loss, set
  cwnd to one packet. On each ack for new data, increase cwnd by one packet. When sending, send the minimum of the receiver's advertised
  window and cwnd.”
- §1 (tr. 4): “Actually, the slow-start window increase isn't that slow: it takes time R log2 W where R is the round-trip-time and W is the
  window size in packets”.
- Hình 4 (tr. 5): “two seconds is spent on the slow-start so the effective bandwidth of this part of the trace is 16 KBps -- two times better
  than figure 3 … The effective bandwidth without slow-start stays at 7 KBps no matter how long the trace.”
- §3 (tr. 9–10): “On congestion: Wi = dWi-1 (d < 1) I.e., a multiplicative decrease of the window size”; “On no congestion: Wi = Wi-1 + u
  (u ≪ Wmax) where Wmax is the pipesize (the delay-bandwidth product of the path minus protocol overhead …). This is the additive increase /
  multiplicative decrease policy … We used 0.5 and 1”.
- §3 (tr. 10): “The first thought is to use a symmetric, multiplicative increase … This is a mistake. The result will oscillate wildly”.
- Hình 8 (§4): “Trace data from four simultaneous TCP conversations without congestion avoidance … 4,000 of 11,000 packets sent were
  retransmissions (i.e., half the data packets were retransmitted). Since the link data bandwidth is 25 KBps, each of the four conversations
  should have received 6 KBps. Instead, one conversation got 8 KBps, two got 5 KBps, one got 0.5 KBps and 6 KBps has vanished.”
- Phụ lục B: “On a timeout, half the current window size is recorded in ssthresh (this is the multiplicative decrease part of the congestion
  avoidance algorithm), then cwnd is set to 1 packet (this initiates slow-start).”

## [G17] N. Cardwell, Y. Cheng (Google). *TCP BBR congestion control comes to GCP – your Internet just got faster.* Google Cloud Blog, 2017-07-21
Tải: https://cloud.google.com/blog/products/networking/tcp-bbr-congestion-control-comes-to-gcp-your-internet-just-got-faster
(hai tác giả cũng là tác giả bài ACM Queue 2016 — xem “Nguồn ứng viên không đọc được” bên dưới).
- “The internet has largely used loss-based congestion control since the late 1980s, relying only on indications of lost packets as the
  signal to slow down. This worked well for many years, because internet switches’ and routers’ small buffers were well-matched to the low
  bandwidth of internet links.”
- “In shallow buffers, packet loss happens before congestion. … loss-based congestion control can result in abysmal throughput because it
  overreacts, halving the sending rate upon packet loss, even if the packet loss comes from transient traffic bursts”.
- “In deep buffers, congestion happens before packet loss. At the edge of today's internet, loss-based congestion control causes the infamous
  “bufferbloat” problem, by repeatedly filling the deep buffers in many last-mile links and causing seconds of needless queuing delay.”
- “BBR considers how fast the network is delivering data. … it uses recent measurements of the network's delivery rate and round-trip time to
  build an explicit model that includes both the maximum recent bandwidth available to that connection, and its minimum recent round-trip
  delay.”
- “Take, for example, YouTube’s experience with BBR. Here, BBR yielded 4 percent higher network throughput … reducing round-trip time by 33
  percent … BBR provides 11 percent higher mean-time-between-rebuffers.” (so với CUBIC)
- “Consider a typical server-class computer with a 10 Gigabit Ethernet link, sending over a path with a 100 ms round-trip time (say, Chicago to
  Berlin) with a packet loss rate of 1%. In such a case, BBR's throughput is 2700x higher than today's best loss-based congestion control,
  CUBIC (CUBIC gets about 3.3 Mbps, while BBR gets over 9,100 Mbps).”
- “Consider a typical last-mile link with 10 Megabits of bandwidth, a 40 ms round-trip time, and a typical 1000-packet bottleneck buffer. In a
  scenario like this, BBR keeps queuing delay 25x lower than CUBIC (CUBIC has a median round-trip time of 1090 ms, versus just 43 ms for BBR).”
- “A few synthetic microbenchmarks illustrate the nature (though not necessarily the typical magnitude) of the advantages”.

## [B26] N. Cardwell, I. Swett, J. Beshay (biên tập). *BBR Congestion Control*, draft-ietf-ccwg-bbr-06, IETF CCWG, tháng 7/2026
Tải: https://www.ietf.org/archive/id/draft-ietf-ccwg-bbr-06.txt
- Đầu trang: “Intended status: Experimental”.
- §1: “The Internet has traditionally used loss-based congestion control algorithms like Reno ([Jac88], [Jac90], [WS95] [RFC5681]) and CUBIC
  ([HRX08], [RFC9438]). These algorithms worked well for many years because they were sufficiently well-matched to the prevalent range of
  bandwidth-delay products and degrees of buffering in Internet paths.”
- §3: “data volume: the amount of data in flight in the network should ideally match the bandwidth-delay product (BDP) of the path”;
  “If a sender perfectly matches its sending rate to the available bandwidth, but its C.inflight exceeds the BDP, then the sender can
  maintain a large standing queue, increasing network latency and risking packet loss.”
- Định nghĩa: “BBR.bdp: The estimate of the network path's BDP (Bandwidth-Delay Product), computed as: BBR.bdp = BBR.bw * BBR.min_rtt.”

## [Q21] RFC 9000 *QUIC: A UDP-Based Multiplexed and Secure Transport* và RFC 9002 *QUIC Loss Detection and Congestion Control* (IETF, tháng 5/2021)
Tải: https://www.rfc-editor.org/rfc/rfc9000.txt, https://www.rfc-editor.org/rfc/rfc9002.txt
- RFC 9000 §1: “QUIC packets are carried in UDP datagrams [UDP] to better facilitate deployment in existing systems and networks.”
- RFC 9000 §1: “Connection migration uses connection identifiers to allow connections to transfer to a new network path.”
- RFC 9002 §4.2: “TCP conflates transmission order at the sender with delivery order at the receiver, resulting in the retransmission
  ambiguity problem … QUIC's packet number is strictly increasing within a packet number space … When a packet containing ack-eliciting
  frames is detected lost, QUIC includes necessary frames in a new packet with a new packet number, removing ambiguity … Consequently, more
  accurate RTT measurements can be made”.
- RFC 9002 §7: “This document specifies a sender-side congestion controller for QUIC similar to TCP NewReno [RFC6582]. The signals QUIC
  provides for congestion control are generic and are designed to support different sender-side algorithms. A sender can unilaterally choose
  a different algorithm to use, such as CUBIC [RFC8312].” “the chosen controller MUST conform to the congestion control guidelines specified
  in Section 3.1 of [RFC8085].”
- RFC 9002 §7.2: “Endpoints SHOULD use an initial congestion window of ten times the maximum datagram size (max_datagram_size), while limiting
  the window to the larger of 14,720 bytes or twice the maximum datagram size.”
- RFC 9002 §7.3.3: “A sender in congestion avoidance uses an Additive Increase Multiplicative Decrease (AIMD) approach that MUST limit the
  increase to the congestion window to at most one maximum datagram size for each congestion window that is acknowledged.”
- RFC 9002 phụ lục B.1: “kLossReductionFactor: Scaling factor applied to reduce the congestion window when a new loss event is detected.
  Section 7 recommends a value of 0.5.”

## Nguồn ứng viên không đọc được (thay thế, ghi lý do)
- N. Cardwell và cộng sự, *BBR: Congestion-Based Congestion Control*, ACM Queue 14(5), 2016 (queue.acm.org/detail.cfm?id=3022184): curl và
  WebFetch đều bị chặn (Cloudflare “Sorry, you have been blocked”, HTTP 403) ngày 2026-11-02; bản CACM 2017 cũng 403; trang research.google
  chỉ dẫn về ACM Queue. Thay bằng [G17] (bài blog chính thức của hai tác giả BBR, 2017) và [B26] (bản đặc tả IETF do nhóm BBR biên tập).
  Bài giảng KHÔNG dạy con số nào chỉ có trong bài ACM Queue (ví dụ kết quả trên mạng B4).

## Điều KHÔNG dạy (nguồn không ghi)
- “Ba chặng IMP” hay được kể lại: bản [J88] đã đọc ghi “two IMP hops” → bài không nói số chặng.
- “Giảm một nghìn lần” là cách nói tròn của nguồn (“factor-of-thousand”); phép chia 32 000 / 40 = 800 là VER — bài nói “khoảng 800 lần”.
- Năm BBR chạy trên YouTube, tỉ lệ máy chủ Google dùng BBR, so sánh công bằng giữa BBR và CUBIC: [G17] không ghi → không dạy.
- Gói 1500 byte trong phép tính bộ đệm 1000 gói là GIẢ ĐỊNH (số minh hoạ); [G17] chỉ ghi “1000-packet bottleneck buffer”.
- QUIC dùng BBR theo mặc định: RFC 9002 KHÔNG ghi (bộ điều khiển mẫu giống NewReno, cho phép chọn thuật toán khác) → không dạy.
- Tỉ lệ lưu lượng Internet đi qua QUIC: không có nguồn đã đọc → không dạy.

## Đọc kiểm lần ba (đợt C, 2026-11-09)
- [J88] tải lại (curl + pdftotext), kiểm thêm: “opening a window of size W packets will require W/2 packets of buffer capacity at the
  bottleneck” (§1, chú thích hình 2 — nguồn của dòng “bộ đệm 8 gói khi mở cửa sổ 16”); “The system will stabilize only if the traffic
  sources throttle back at least as quickly as the queues are growing” (§3 — nguồn của lý do hệ số giảm). “LBL to UC Berkeley”: một phòng
  thí nghiệm và một trường đại học → bài sửa “hai phòng thí nghiệm” thành “một phòng thí nghiệm với một trường đại học”.
- [G17] đọc lại (WebFetch): CUBIC được gọi là “today's best loss-based congestion control”, KHÔNG phải “phổ biến nhất” → bài sửa thành
  “mà nhóm gọi là tốt nhất lúc đó”. “improved YouTube network throughput by 4 percent on average globally” và “reducing round-trip time by
  33 percent” khớp.
- [B26]: bản nháp (Internet-Draft), “Intended status: Experimental” → bài nói “bản nháp, dự kiến xếp mức thử nghiệm”.
- Chặng 4, nhập nhằng gửi lại: TCP thật không đo bừa — bỏ mẫu đo của đoạn gửi lại (thuật toán Karn, có trong danh sách bảy thuật toán của
  [J88]) hoặc dùng tuỳ chọn dấu thời gian (RFC 7323) → bài nói “đo bừa có thể sai gấp 7 lần, nên TCP phải bỏ mẫu đo này, hoặc dùng thêm dấu
  thời gian”; RFC 9002 §4.2 gọi đây là “retransmission ambiguity problem”.
