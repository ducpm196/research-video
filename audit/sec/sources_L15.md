# Nguồn đã đọc nguyên văn cho SEC L15 (bài hành trình: HTTPS trở thành mặc định, 2014 → 2028)

Đọc ngày 2026-11-02 (tải bằng curl; PDF trích chữ bằng pdftotext; câu dưới đây chép nguyên văn từ bản trích). Chỉ trích các câu bài giảng
dựa vào (CITED); mọi con số khác trong bài là phép tính lại (VER, `checks` của bài và `audit/sec/verify_sec.py` L15) hoặc ghi rõ
“số minh hoạ”. Không nêu tên cá nhân (kể cả người tìm ra lỗi) trong lời đọc. Heartbleed chỉ dạy ở mức khái niệm phòng thủ: điều kiện
kiểm đúng, vá, thay khoá — KHÔNG có cách dựng yêu cầu khai thác.

## [O14] OpenSSL Security Advisory, *TLS heartbeat read overrun (CVE-2014-0160)*, 07/04/2014
Tải: https://www.openssl.org/news/secadv/20140407.txt
- “A missing bounds check in the handling of the TLS heartbeat extension can be used to reveal up to 64k of memory to a connected client or
  server.”
- “Only 1.0.1 and 1.0.2-beta releases of OpenSSL are affected including 1.0.1f and 1.0.2-beta1.”
- “Affected users should upgrade to OpenSSL 1.0.1g.”

## [D14] Z. Durumeric, J. Kasten, D. Adrian, J. A. Halderman, M. Bailey, F. Li, N. Weaver, J. Amann, J. Beekman, M. Payer, V. Paxson. *The Matter of Heartbleed.* ACM IMC 2014
Tải: https://jhalderm.com/pub/papers/heartbleed-imc14.pdf
- Tóm tắt: “allowed attackers to remotely read protected memory from an estimated 24–55% of popular HTTPS sites.”
- §1: “We estimate that 24–55% of HTTPS servers in the Alexa Top 1 Million were initially vulnerable”.
- §1: “Two days after disclosure, we observed that 11% of HTTPS sites in the Alexa Top 1 Million remained vulnerable”.
- §1: “within the first 24 hours, all but 5 of the Alexa Top 100 sites were patched … patching plateaued after about two weeks, and 3% of HTTPS
  sites in the Alexa Top 1 Million remained vulnerable almost two months after disclosure.”
- §1: “less than a quarter of Alexa Top 1 Million sites replaced certificates in the week following disclosure. Even more worryingly, only 10%
  of the sites that were vulnerable 48 hours after disclosure replaced their certificates within the next month, and of those that did, 14%
  neglected to change the private key, gaining no protection from certificate replacement.”
- §1: “observing a surprisingly high 47% increase in patching by notified operators.”
- §2.2: “On April 7, 2014, the OpenSSL project publicly disclosed the Heartbleed vulnerability … The extension was introduced in February 2012 in
  RFC 6520 [66], added to OpenSSL on December 31, 2011, and released in OpenSSL Version 1.0.1 on March 14, 2012.”
- §2.2: “HeartbeatRequest messages consist of a one-byte type field, a two-byte payload length field, a payload, and at least 16 bytes of random
  padding.”
- §2.3: “by specifying a payload length larger than the amount of data in the HeartbeatRequest message. Because the payload length field is two
  bytes, the peer responds with up to 2^16 bytes (~64 KB) of memory.”
- §2.3: “The OpenSSL patch adds a bounds check that discards the HeartbeatRequest message if the payload length field exceeds the length of the
  payload.”

## [A19] J. Aas, R. Barnes, B. Case, Z. Durumeric, P. Eckersley, A. Flores-López, J. A. Halderman, J. Hoffman-Andrews, J. Kasten, E. Rescorla, S. Schoen, B. Warren. *Let's Encrypt: An Automated Certificate Authority to Encrypt the Entire Web.* ACM CCS 2019
Tải: https://jhalderm.com/pub/papers/letsencrypt-ccs19.pdf (doi 10.1145/3319535.3363192)
- Tóm tắt: “By January 2019, it had issued over 538 million certificates for 223 million domain names.”
- §1: “low adoption of HTTPS posed an even starker risk: as recently as 2015, 55–70% of browser page loads used plaintext HTTP [47].”
- §1: “To obtain and install a certificate, a server operator had to use arcane key generation software and configuration directives, follow
  manual steps to prove control of the domain name, and complete a payment transaction to a CA.”
- §1: “Over the four years since Let's Encrypt launched, the fraction of browser page-loads that take place over HTTPS has approximately
  doubled, to 72–95%, according to telemetry from Google Chrome [47].”
- §2.1: “In 2015, the average price for a one-year single-domain certificate from the five largest CAs was $178”.
- §2.1: StartCom “charged for revocation, which proved to be a source of problems when Heartbleed [37] forced many sites to revoke”.
- §2: “Prior to Let's Encrypt, renewal lapse occurred for about 20% of trusted certificates [36].”
- §2: “To further promote automation, Let's Encrypt limits certificate lifetimes to 90 days, rather than one or multiple years as CAs have
  traditionally offered. Shorter certificate lifetimes potentially enhance security, since they lessen reliance on certificate revocation in
  the event of key compromise”.
- §5.2: “The architecture described here has allowed Let's Encrypt to scale up to issuing more than a million certificates per day at peak”.
- §7: “Since its launch in December 2015, Let's Encrypt has steadily grown to become the largest CA in the Web PKI by certificates issued”.
- §7.5: “few Let's Encrypt renewals (2.9%) occur after the prior certificate has expired. Most renewals occur in the last 30 days before the
  validity period of a certificate expires (64%)”.
- §8.1: “Automation is necessary to have a free CA and free certificates make automation practical.”

## [L15] Let's Encrypt, *Why ninety-day lifetimes for certificates?*, 09/11/2015
Tải: https://letsencrypt.org/2015/11/09/why-90-days/
- “They limit damage from key compromise and mis-issuance. Stolen keys and mis-issued certificates are valid for a shorter period of time.”
- “They encourage automation … If we’re going to move the entire Web to HTTPS, we can’t continue to expect system administrators to manually
  handle renewals.”
- “We recommend that subscribers renew every sixty days. Once automated renewal tools are widely deployed and working well, we may consider
  even shorter lifetimes.”

## [L25] Let's Encrypt, *Decreasing Certificate Lifetimes to 45 Days*, 02/12/2025
Tải: https://letsencrypt.org/2025/12/02/from-90-to-45
- “We currently issue certificates valid for 90 days, which will be cut in half to 45 days by 2028. This change is being made along with the
  rest of the industry, as required by the CA/Browser Forum Baseline Requirements”.
- “We are also reducing the authorization reuse period … It is currently 30 days, which will be reduced to 7 hours by 2028.”
- “February 10, 2027: … issuing 64-day certificates with a 10-day authorization reuse period.” “February 16, 2028: … 45-day certificates with a
  7 hour authorization reuse period.”
- “renewing at a hardcoded interval of 60 days will no longer be sufficient. Acceptable behavior includes renewing certificates at
  approximately two thirds of the way through the current certificate’s lifetime.”
- “Manually renewing certificates is not recommended”; “make sure your systems have sufficient monitoring in place to alert appropriately if
  certificates aren’t renewed when expected.”

## Nguồn ứng viên: mốc tỉ lệ trang tải qua HTTPS
- Không đọc trực tiếp báo cáo minh bạch của Google (trang dựng bằng mã kịch bản). Dùng số do [A19] §1 trích từ đo đạc của trình duyệt Chrome:
  2015 có 55–70% lượt tải trang dùng HTTP không mã hoá; bốn năm sau, 72–95% lượt tải trang qua HTTPS. Bài ghi đúng là “theo bài báo năm 2019”.

## Điều KHÔNG dạy (nguồn không ghi hoặc ngoài phạm vi phòng thủ)
- Cách dựng yêu cầu nhịp tim để đọc bộ nhớ: KHÔNG dạy (luật an ninh). Bài chỉ dạy điều kiện kiểm “độ dài khai báo ≤ độ dài nhận được”.
- “Hai phần ba vòng đời” ở [L25] là điều Let's Encrypt chấp nhận, không phải quy định; 60 trên 90 ngày cũng là hai phần ba — VER.
- Tên người tìm ra lỗi (có trong [O14], [D14]): không đọc trong lời.
- Lỗi Heartbleed bị khai thác trước khi công bố hay không: [D14] bàn riêng, bài không khẳng định.
- Số dư 1 ngày khi đếm 754 ngày từ 14/3/2012 tới 7/4/2014: tính bằng máy (`datetime`), ghi trong `checks`.
