# Nguồn đã đọc nguyên văn cho CAS L09 (Heartbleed, CVE-2014-0160) — CHỈ mức khái niệm phòng thủ

Đọc ngày 2026-11-02 (urllib; văn bản thuần / HTML). Chỉ trích các câu bài giảng dựa vào (CITED). Phép tính (65 535, 65 554, 19, 16 365,
754 ngày, quiz 2 + n ≤ 50) là VER (`checks`, `audit/cas/ver/L09.py`, `audit/verify_plan_curricula.py` CAS:L09). Bài KHÔNG dạy cách dựng
gói hay khai thác: chỉ cấu trúc tin theo đặc tả, điều kiện kiểm đúng (đúng phép kiểm của bản vá), và việc phải làm sau khi vá.

## [RFC] IETF RFC 6520, *TLS and DTLS Heartbeat Extension*, 2/2012
URL: https://www.rfc-editor.org/rfc/rfc6520.txt (HTTP 200, 16 858 byte).
- Mục 4: “struct { HeartbeatMessageType type; uint16 payload_length; opaque payload[HeartbeatMessage.payload_length]; opaque
  padding[padding_length]; } HeartbeatMessage;”
- “The total length of a HeartbeatMessage MUST NOT exceed 2^14 or max_fragment_length when negotiated”.
- “the length of the type field is 1 byte, and the length of the payload_length is 2. Therefore, the padding_length is TLSPlaintext.length -
  payload_length - 3 for TLS … The padding_length MUST be at least 16.”
- “The padding of a received HeartbeatMessage message MUST be ignored.”
- “If the payload_length of a received HeartbeatMessage is too large, the received HeartbeatMessage MUST be discarded silently.”
- “the receiver MUST send a corresponding HeartbeatResponse message carrying an exact copy of the payload of the received HeartbeatRequest.”

## [ADV] OpenSSL Security Advisory [07 Apr 2014], *TLS heartbeat read overrun (CVE-2014-0160)*
URL: https://www.openssl.org/news/secadv/20140407.txt (HTTP 200, 762 byte).
- “A missing bounds check in the handling of the TLS heartbeat extension can be used to reveal up to 64k of memory to a connected client or
  server.” “Only 1.0.1 and 1.0.2-beta releases of OpenSSL are affected including 1.0.1f and 1.0.2-beta1.” “Affected users should upgrade to
  OpenSSL 1.0.1g. Users unable to immediately upgrade can alternatively recompile OpenSSL with -DOPENSSL_NO_HEARTBEATS.”

## [FIX] OpenSSL, commit 96db9023b881d7cd9f379b0c154650d6c108e9a3 “Add heartbeat extension bounds check.” (Date: Sun, 6 Apr 2014)
URL: https://github.com/openssl/openssl/commit/96db9023b881d7cd9f379b0c154650d6c108e9a3.patch (HTTP 200, 4 156 byte).
- t1_lib.c và d1_both.c: “if (1 + 2 + 16 > s->s3->rrec.length) return 0; /* silently discard */” rồi
  “if (1 + 2 + payload + 16 > s->s3->rrec.length) return 0; /* silently discard per RFC 6520 sec. 4 */”.
- Chỉ d1_both.c (DTLS): “unsigned int write_length = 1 /* heartbeat type */ + 2 /* heartbeat length */ + payload + padding; …
  if (write_length > SSL3_RT_MAX_PLAIN_LENGTH) return 0;” → bài nói “với biến thể chạy trên gói tin rời, bản vá kiểm thêm”.
  (Bài chỉ nêu điều kiện bằng lời và số, không chép mã.)

## [HB] Synopsys / Codenomicon, *The Heartbleed Bug*, heartbleed.com
URL: https://heartbleed.com/ (HTTP 200, 24 976 byte).
- “The Heartbleed Bug is a serious vulnerability in the popular OpenSSL cryptographic software library.”
- “OpenSSL is the most popular open source cryptographic library and TLS (transport layer security) implementation used to encrypt traffic on
  the Internet.”
- “The most notable software using OpenSSL are the open source web servers like Apache and nginx. The combined market share of just those two
  out of the active sites on the Internet was over 66% according to Netcraft's April 2014 Web Server Survey.”
- “Bug was introduced to OpenSSL in December 2011 and has been out in the wild since OpenSSL release 1.0.1 on 14th of March 2012. OpenSSL
  1.0.1g released on 7th of April 2014 fixes the bug.”
- “Exploitation of this bug does not leave any trace of anything abnormal happening to the logs.”
- “There is no total of 64 kilobytes limitation to the attack, that limit applies only to a single heartbeat.” (bài chỉ dùng ý “giới hạn là
  cho một lần, lặp lại thì lộ thêm”, không mô tả cách lặp.)
- Khôi phục: “Recovery from this leak requires patching the vulnerability, revocation of the compromised keys and reissuing and
  redistributing new keys.” “After this users can start changing their passwords”. “Some CAs do this for free, some may take a fee.”
- “If this is not possible software developers can recompile OpenSSL with the handshake removed from the code by compile time option
  -DOPENSSL_NO_HEARTBEATS.”

## Sai sót giáo án đã sửa
- `example` cũ: “kiểm đúng: độ dài khai báo + phần đầu ≤ độ dài thật” thiếu phần đệm ít nhất 16 byte → sửa thành đúng điều kiện của RFC
  và bản vá: 1 + 2 + n + 16 ≤ L (VER CAS:L09 cập nhật: bản ghi 20 byte, khai 1 nhận, khai 65 535 → 65 554 bỏ). “gói thật chỉ mang 1 byte” là
  số minh hoạ (nguồn không ghi) → ghi rõ.
- `fix` cũ: “thư viện dùng rộng mà ít người bảo trì” — không nguồn nào đã đọc ghi “ít người bảo trì” → bỏ chi tiết đó; giữ ý “không phải
  đừng dùng mã nguồn mở” với điều nguồn ghi (phổ biến nhất, 14/3/2012 → 7/4/2014).

## Điều KHÔNG dạy
- Cách dựng yêu cầu khai thác, công cụ dò, chi tiết bộ nhớ lộ ra được những gì cụ thể ở máy nào: không dạy.
- Tên người tìm ra lỗi / người viết mã: không nêu (không cần cho bài).
- Số máy chủ bị ảnh hưởng thật: nguồn chỉ có thị phần > 66% của hai máy chủ trang mạng, không phải số trang dính lỗi → bài nói đúng như vậy.
