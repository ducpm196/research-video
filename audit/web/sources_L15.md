# Nguồn đã đọc nguyên văn cho WEB L15 (bài hành trình: HTTP từ 1.0 tới 3)

Đọc ngày 2026-11-02 (tải bản .txt chính thức từ rfc-editor.org bằng curl, grep nguyên văn). Chỉ trích các câu bài giảng dựa vào (CITED);
mọi con số khác trong bài là phép tính lại (VER, `checks` của bài và `audit/web/verify_web.py` L15) hoặc ghi rõ “số minh hoạ”.
Không nêu tên cá nhân trong lời đọc; tên biên tập viên chỉ ở `source:`.

## [R96] RFC 1945 *Hypertext Transfer Protocol -- HTTP/1.0* (Informational, tháng 5/1996)
Tải: https://www.rfc-editor.org/rfc/rfc1945.txt
- §1.3: “Except for experimental applications, current practice requires that the connection be established by the client prior to each
  request and closed by the server after sending the response.”
- §1.3: “The default port is TCP 80 [15], but other ports can be used.”

## [R99] RFC 2616 *Hypertext Transfer Protocol -- HTTP/1.1* (Standards Track, tháng 6/1999)
Tải: https://www.rfc-editor.org/rfc/rfc2616.txt
- §8.1.1: “Prior to persistent connections, a separate TCP connection was established to fetch each URL, increasing the load on HTTP servers
  and causing congestion on the Internet. The use of inline images and other associated data often require a client to make multiple
  requests of the same server in a short amount of time.”
- §8.1.1: “HTTP requests and responses can be pipelined on a connection. Pipelining allows a client to make multiple requests without waiting
  for each response”; “Latency on subsequent requests is reduced since there is no time spent in TCP's connection opening handshake.”;
  “HTTP implementations SHOULD implement persistent connections.”
- §8.1.2.2: “A server MUST send its responses to those requests in the same order that the requests were received.”
- §8.1.4: “A single-user client SHOULD NOT maintain more than 2 connections with any server or proxy.”

## [R97] RFC 2068 *Hypertext Transfer Protocol -- HTTP/1.1* (Standards Track, tháng 1/1997) — thêm 2026-11-08 khi đọc kiểm
Tải: https://www.rfc-editor.org/rfc/rfc2068.txt (truy cập 2026-11-08). Bản HTTP/1.1 ĐẦU TIÊN; RFC 2616 (1999) là bản sửa của nó.
Bài cũ tính “1.0 → 1.1 mất 3 năm, 1.1 → 2 mất 16 năm” theo năm của RFC 2616 — sai; đúng là 8 tháng (5/1996 → 1/1997) và 18 năm (1997 → 2015).
- §8.1.1: “HTTP implementations SHOULD implement persistent connections.”
- §8.1.2.2: “A client that supports persistent connections MAY "pipeline" its requests”; “A server MUST send its responses to those
  requests in the same order that the requests were received.”
- §8.1.4: “A single-user client SHOULD maintain AT MOST 2 connections with any server or proxy.”

## [R22a] RFC 9112 *HTTP/1.1* (STD 99, tháng 6/2022)
Tải: https://www.rfc-editor.org/rfc/rfc9112.txt
- §9.4: “Previous revisions of HTTP gave a specific number of connections as a ceiling, but this was found to be impractical for many
  applications. As a result, this specification does not mandate a particular maximum number of connections but, instead, encourages clients
  to be conservative when opening multiple connections.”
- §9.4: “Multiple connections are typically used to avoid the "head-of-line blocking" problem, wherein a request that takes significant
  server-side processing and/or transfers very large content would block subsequent requests on the same connection. However, each connection
  consumes server resources.”

## [R15] RFC 7540 *HTTP/2* (tháng 5/2015) và RFC 7541 *HPACK: Header Compression for HTTP/2* (tháng 5/2015)
Tải: https://www.rfc-editor.org/rfc/rfc7540.txt, https://www.rfc-editor.org/rfc/rfc7541.txt
- RFC 7540 §1: “HTTP/1.0 allowed only one request to be outstanding at a time on a given TCP connection. HTTP/1.1 added request pipelining,
  but this only partially addressed request concurrency and still suffers from head-of-line blocking. Therefore, HTTP/1.0 and HTTP/1.1
  clients that need to make many requests use multiple connections to a server in order to achieve concurrency and thereby reduce latency.”
- RFC 7540 §1: “Furthermore, HTTP header fields are often repetitive and verbose, causing unnecessary network traffic as well as causing the
  initial TCP [TCP] congestion window to quickly fill.”
- RFC 7540 §1: “it allows interleaving of request and response messages on the same connection and uses an efficient coding for HTTP header
  fields. It also allows prioritization of requests”; “The resulting protocol is more friendly to the network because fewer TCP connections
  can be used in comparison to HTTP/1.x.”
- RFC 7541 §1: “In HTTP/1.1 (see [RFC7230]), header fields are not compressed. As web pages have grown to require dozens to hundreds of
  requests, the redundant header fields in these requests unnecessarily consume bandwidth, measurably increasing latency.”
- RFC 7541 §1: “SPDY [SPDY] initially addressed this redundancy by compressing header fields using the DEFLATE [DEFLATE] format … However,
  that approach exposed a security risk as demonstrated by the CRIME (Compression Ratio Info-leak Made Easy) attack”; “The HPACK format is
  intentionally simple and inflexible. Both characteristics reduce the risk of interoperability or security issues due to implementation
  error.”

## [R22b] RFC 9114 *HTTP/3* (tháng 6/2022), RFC 9113 *HTTP/2* (tháng 6/2022), RFC 9110 *HTTP Semantics* (STD 97, tháng 6/2022)
Tải: https://www.rfc-editor.org/rfc/rfc9114.txt, rfc9113.txt, rfc9110.txt
- RFC 9114 §1.1: “Because HTTP/1.1 does not include a multiplexing layer, multiple TCP connections are often used to service requests in
  parallel. However, that has a negative impact on congestion control and network efficiency, since TCP does not share congestion control
  across multiple connections.”
- RFC 9114 §1.1: “HTTP/2 … introduced a binary framing and multiplexing layer to improve latency without modifying the transport layer.
  However, because the parallel nature of HTTP/2's multiplexing is not visible to TCP's loss recovery mechanisms, a lost or reordered packet
  causes all active transactions to experience a stall regardless of whether that transaction was directly impacted by the lost packet.”
- RFC 9114 §1.2: “The QUIC transport protocol incorporates stream multiplexing and per-stream flow control … By providing reliability at the
  stream level and congestion control across the entire connection, QUIC has the capability to improve the performance of HTTP compared to a
  TCP mapping.”
- RFC 9114 §2: “Each request-response pair consumes a single QUIC stream. Streams are independent of each other, so one stream that is blocked
  or suffers packet loss does not prevent progress on other streams.”
- RFC 9114 §3.1: “Connectivity problems (e.g., blocking UDP) can result in a failure to establish a QUIC connection; clients SHOULD attempt to
  use TCP-based versions of HTTP in this case.”
- RFC 9114 §3.1.1: “An HTTP origin can advertise the availability of an equivalent HTTP/3 endpoint via the Alt-Svc HTTP response header field
  … Alt-Svc: h3=":50781"”.
- RFC 9114 §1: “HTTP/3 supports the same semantics over a new transport protocol: QUIC.”
- RFC 9110 Tóm tắt: “This document describes the overall architecture of HTTP, establishes common terminology, and defines aspects of the
  protocol that are shared by all versions.”
- RFC 9113 §5.3.2: “This update to HTTP/2 deprecates the priority signaling defined in RFC 7540 … Though the priority signaling from RFC 7540
  was not widely adopted, the information it provides can still be useful in the absence of better information.”

## Nguồn ứng viên đã thay
- ROADMAP ghi RFC 2616: đã đọc; bản hiện hành là RFC 9112 (2022) — bài dẫn cả hai (2616 cho chặng 1999, 9112 cho giới hạn số kết nối).
- ROADMAP ghi RFC 7540: đã đọc; bản hiện hành RFC 9113 (2022) — dẫn ở chặng cuối (bỏ cơ chế ưu tiên cũ).

## Điều KHÔNG dạy (nguồn không ghi)
- Thời gian bắt tay mã hoá (số vòng của TLS 1.3, 0-RTT của QUIC) — các RFC đã đọc không đếm số vòng → bài chỉ đếm vòng bắt tay giao vận và
  vòng yêu cầu như bài 0, phần mã hoá không tính (ghi rõ trên màn hình).
- Tỉ lệ trang web dùng HTTP/2 hay HTTP/3 — không có nguồn đã đọc → không dạy.
- Trình duyệt mở 6 kết nối mỗi máy chủ — không có trong RFC đã đọc → không dạy (RFC 2616 ghi 2; RFC 9112 bỏ con số cố định).
- Đẩy từ máy chủ (server push) bị trình duyệt bỏ — không có trong RFC đã đọc → không dạy.
- Mọi kích thước tiêu đề (500 byte) và thời gian xử lý (300 ms) trong bài là SỐ MINH HOẠ.
