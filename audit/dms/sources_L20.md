# Nguồn đã đọc nguyên văn cho DMS L20 (bài hành trình: hàm băm từ va chạm MD5 tới rút SHA-1)

Đọc ngày 2026-11-02 (curl + trích văn bản; WebFetch khi trang chặn curl). Chỉ trích các câu bài giảng dựa vào (CITED); mọi con số khác
là phép tính lại (VER, `checks` của bài và `audit/verify_plan_curricula.py` DMS:L20) hoặc ghi rõ “(số minh hoạ)”. Chỉ ở mức khái niệm
phòng thủ: bài KHÔNG trình bày cách dựng va chạm. Không nêu tên cá nhân trong lời đọc; tên tác giả chỉ ở `source:` và màn hình nguồn.

Đổi so với ROADMAP §8.1 mục 3 (Wang và cộng sự 2004–2005 → Stevens và cộng sự 2017): hai bài báo của nhóm Wang KHÔNG đọc được
(eprint.iacr.org/2004/199.pdf trả 403 với curl và WebFetch; bài EUROCRYPT 2005 trên link.springer.com trả trang “Client Challenge”;
web.archive.org trả 429). Chặng MD5 dựa vào RFC 6151 (IETF, 2011, đồng tác giả NIST) — văn bản chính thức tóm tắt các kết quả đó.
Trang shattered.io nay là một trang tin khác (tên miền đã đổi chủ, đọc 2026-11-02); chính tài liệu của Git dẫn bản lưu web.archive.org,
bản lưu đó đang trả 429 → chặng 2017 dựa vào tóm tắt ePrint 2017/190 và blog Google ngày 23/2/2017 của chính nhóm tác giả.

## [RF11] RFC 6151, *Updated Security Considerations for the MD5 Message-Digest and the HMAC-MD5 Algorithms*, IETF, 3/2011
Tải: www.rfc-editor.org/rfc/rfc6151.txt (curl, 14 662 byte). Tác giả: S. Turner (IECA), L. Chen (NIST).
- §1: “MD5 [MD5] is a message digest algorithm that takes as input a message of arbitrary length and produces as output a 128-bit
  "fingerprint" or "message digest" of the input.”
- §1: “Where the MD5 checksum is used inline with the protocol solely to protect against errors, an MD5 checksum is still an acceptable use.”
- §2: “MD5 was published in 1992 as an Informational RFC.”
- §2: “MD5 is no longer acceptable where collision resistance is required such as digital signatures.  It is not urgent to stop using MD5 in
  other ways, such as HMAC-MD5; however, since MD5 must not be used for digital signatures, new protocol designs should not employ HMAC-MD5.”
- §2.1: “The first paper that demonstrated two collision pairs for MD5 was published in 2004 [WFLY2004].  The detailed attack techniques for
  MD5 were published at EUROCRYPT 2005 [WAYU2005].”
- §2.1: “The attacks presented in [KLIM2006] can find MD5 collision in about one minute on a standard notebook PC (Intel Pentium, 1.6GHz).
  [STEV2007] claims that it takes 10 seconds or less on a 2.6Ghz Pentium4 to find collisions.  In [STEV2007], [SLdeW2007], [SSALMOdeW2009],
  and [SLdeW2009], the collision attacks on MD5 were successfully applied to X.509 certificates.”
- §2.1: “the aforementioned results have provided sufficient reason to eliminate MD5 usage in applications where collision resistance is
  required such as digital signatures.”
- §2.2: “the complexity 2^123.4 is still pretty high.” (tiền ảnh — không dạy chi tiết, chỉ dùng ý “kháng tiền ảnh còn vững”)

## [NP] NIST CSRC, *NIST Policy on Hash Functions* (các mục 15/3/2006, 28/9/2012, 5/8/2015, 15/12/2022)
Tải: csrc.nist.gov/projects/hash-functions/nist-policy-on-hash-functions (curl).
- 15/3/2006: “Federal agencies should stop using SHA-1 for digital signatures, digital time stamping and other applications that require
  collision resistance as soon as practical, and must use the SHA-2 family of hash functions for these applications after 2010.”
- 15/3/2006: “Regardless of use, NIST encourages application and protocol designers to use the SHA-2 family of hash functions for all new
  applications and protocols.”
- 5/8/2015: “Federal agencies may use SHA-1 for the following applications: verifying old digital signatures and time stamps, generating and
  verifying hash-based message authentication codes (HMACs), key derivation functions (KDFs), and random bit/number generation.”
- 5/8/2015: “NIST encourages application and protocol designers to implement SHA-256 at a minimum for any applications of hash functions
  requiring interoperability.” … “Currently there is no need to transition applications from SHA-2 to SHA-3.”
- 15/12/2022: “After 12/31/2030, any FIPS 140 validated cryptographic module that has SHA-1 as an approved algorithm will be moved to the
  historical list.”

## [S3] NIST CSRC, *SHA-3 Project*
Tải: csrc.nist.gov/projects/hash-functions/sha-3-project (curl).
- “In 2004-2005, several cryptographic hash algorithms were successfully attacked, and serious attacks were published against the
  NIST-approved SHA-1. In response, NIST held two public workshops … NIST decided to develop a new cryptographic hash algorithm for
  standardization through a public competition.”
- “NIST announced the SHA-3 Cryptographic Hash Algorithm Competition on November 2, 2007, and ended the competition on October 2, 2012, when
  it announced KECCAK as the winning algorithm to be standardized as the new SHA-3.”
- Danh mục: “FIPS 202, SHA-3 Standard: Permutation-Based Hash and Extendable-Output Functions” (trang không ghi ngày ban hành FIPS 202 →
  bài chỉ nói “chuẩn FIPS 202”, năm 2015 lấy từ mục chính sách 5/8/2015 của [NP], nơi SHA-3 lần đầu được liệt kê là được dùng).

## [ST17] M. Stevens, E. Bursztein, P. Karpman, A. Albertini, Y. Markov, *The first collision for full SHA-1*, CRYPTO 2017 (ePrint 2017/190)
Tải: eprint.iacr.org/2017/190 (trang tóm tắt, curl 200; tệp PDF trả 403 → chỉ dùng tóm tắt).
- “SHA-1 is a widely used 1995 NIST cryptographic hash function standard that was officially deprecated by NIST in 2011 due to fundamental
  security weaknesses demonstrated in various analyses and theoretical attacks.”
- “Despite its deprecation, SHA-1 remains widely used in 2017 for document and TLS certificate signatures, and also in many software such
  as the GIT versioning system for integrity and backup purposes.”
- “finding an actual collision has seemed to be impractical for the past eleven years due to the high complexity and computational cost”
- “the prefix of the colliding messages was carefully chosen so that they allow an attacker to forge two distinct PDF documents with the
  same SHA-1 hash that display different arbitrarily-chosen visual contents.”
- “In total the computational effort spent is equivalent to 2^63.1 calls to SHA-1's compression function, and took approximately 6,500 CPU
  years and 100 GPU years. … it is still more than 100,000 times faster than a brute force search.”
- “Publication info: A minor revision of an IACR publication in CRYPTO 2017”; “2017-02-28: received”.

## [GB17] Google Online Security Blog, *Announcing the first SHA1 collision*, 23/2/2017 (nhóm tác giả CWI + Google)
Tải: security.googleblog.com/2017/02/announcing-first-sha1-collision.html (curl; thân bài nằm trong mã trang, trích bằng script).
- “Nine quintillion (9,223,372,036,854,775,808) SHA1 computations in total”; “6,500 years of CPU computation to complete the attack first
  phase”; “110 years of GPU computation to complete the second phase”. (Lệch nhỏ với [ST17] “100 GPU years” → bài dùng số của bài báo
  [ST17] và nói “khoảng”.)
- “the SHA-1 shattered attack is still more than 100,000 times faster than a brute force attack which remains impractical.”
- “As early as 2014, the Chrome team announced that they would gradually phase out using SHA-1.”
- “it’s more urgent than ever for security practitioners to migrate to safer cryptographic hashes such as SHA-256 and SHA-3. Following
  Google’s vulnerability disclosure policy, we will wait 90 days before releasing code … we’ve added protections for Gmail and GSuite users
  that detects our PDF collision technique. Furthermore, we are providing a free detection system to the public.”

## [GIT] Git, *Documentation/technical/hash-function-transition.adoc* và *Documentation/BreakingChanges.adoc* (nhánh master)
Tải: raw.githubusercontent.com/git/git/master/Documentation/technical/hash-function-transition.adoc, …/BreakingChanges.adoc (curl).
- “At its core, the Git version control system is a content addressable filesystem. It uses the SHA-1 hash function to name content.”
- “On 23 February 2017 the SHAttered attack (https://web.archive.org/web/20260207211148/https://shattered.io/) demonstrated a practical SHA-1
  hash collision.”
- “Git v2.13.0 and later subsequently moved to a hardened SHA-1 implementation by default, which isn't vulnerable to the SHAttered attack,
  but SHA-1 is still weak.”
- “The hash to replace the hardened SHA-1 should be stronger than SHA-1 was: we would like it to be trustworthy and useful in practice for at
  least 10 years.” “1. A 256-bit hash”. “In late 2018 the project picked SHA-256 as its successor hash.”
- Độ dài: “Objects can be named by their 40 hexadecimal digit SHA-1 name or 64 hexadecimal digit SHA-256 name”; “a 32-byte SHA-256
  hash and for SHA-1, it's a 20-byte SHA-1 hash.” (20 byte = 160 bit, 32 byte = 256 bit: VER trong `checks` của bài)
- Goals: “The transition to SHA-256 can be done one local repository at a time.” “a SHA-256 repository stores a bidirectional mapping
  between SHA-256 and SHA-1 object names.” “SHA-256 repositories cannot be read by older versions of Git.”
- BreakingChanges, “== Git 3.0”: “The default hash function for new repositories will be changed from "sha1" to "sha256".” Danh sách:
  “The SHAppening (2015). … 2^57 operations.” “SHAttered (2017). Generation of two valid PDF files with 2^63 operations.”
  “Birthday-Near-Collision (2019). … chosen prefix attacks with 2^68 operations.” “Shambles (2020). … chosen prefix attacks with 2^63
  operations.” “An important requirement for this change is that the ecosystem is ready to support the "sha256" object format.”
  “There is no plan to deprecate the "sha1" object format at this point in time.”

## [NI22] NIST News, *NIST Retires SHA-1 Cryptographic Algorithm*, 15/12/2022
Tải: www.nist.gov/news-events/news/2022/12/nist-retires-sha-1-cryptographic-algorithm (curl).
- “SHA-1 … has been in use since 1995 as part of the Federal Information Processing Standard (FIPS) 180-1.”
- “NIST is announcing that SHA-1 should be phased out by Dec. 31, 2030, in favor of the more secure SHA-2 and SHA-3 groups of algorithms.”
- “We recommend that anyone relying on SHA-1 for security migrate to SHA-2 or SHA-3 as soon as possible”
- “Publish FIPS 180-5 (a revision of FIPS 180) to remove the SHA-1 specification.”
- “All cryptographic modules used in federal encryption must be validated every five years”; “Companies have eight years to submit updated
  modules that no longer use SHA-1.”

## Điều KHÔNG dạy (nguồn không ghi hoặc không đọc được)
- Cách dựng va chạm MD5/SHA-1 (vi sai, khối tin) — ngoài phạm vi phòng thủ, và hai bài báo năm 2004–2005 không đọc được.
- Thời gian tìm va chạm MD5 năm 2004 (“khoảng một giờ” hay được kể lại): [RF11] không ghi → không dạy; chỉ dạy số năm 2006 (một phút)
  và 2007 (≤ 10 giây) mà [RF11] ghi.
- Độ phức tạp tấn công SHA-1 lý thuyết năm 2005 (2^69 hay được kể lại): không đọc được nguồn → không dạy.
- Nội dung trang shattered.io gốc: không đọc được (tên miền đổi chủ, bản lưu 429).
- Năm phát hành Git 3.0: tài liệu Git không ghi ngày → bài nói “Git ghi kế hoạch cho bản 3.0 (đọc ngày 2/11/2026)” (sửa đợt C, 2026-11-09: bỏ “sắp tới”).
  Git 2.13.0: thẻ v2.13.0 do Junio C Hamano ký ngày 2017-05-09T14:26:15Z (api.github.com/repos/git/git/git/tags/074ffb61…, đọc 2026-11-09) —
  khớp nhãn chặng “2017 → 2018” của bài.

## Bổ sung đợt C (đọc 2026-11-09)
- [NI22] (WebFetch, trang nist.gov ở trên): SHA-1 “has reached the end of its useful life” (lời các chuyên gia an ninh của NIST);
  Chris Celi: “Modules that still use SHA-1 after 2030 will not be permitted for purchase by the federal government.” → khớp
  “đã hết tuổi thọ hữu ích” và “sau 2030 … không được mua nữa” ở chặng 5.
- [NP] mục 5/8/2015 (WebFetch): SHA-3 dùng được “for all applications that employ secure hash algorithms”; “SHA-256 at a minimum”
  là cho ứng dụng “requiring interoperability” → bài nay ghi đủ điều kiện “ứng dụng cần tương thích”.
- [GB17] thân bài (curl, tách văn bản bằng Python): “a well-funded attacker can craft a collision … For example, two insurance
  contracts with drastically different terms.” → khớp câu “hai hợp đồng khác điều khoản” ở chặng 3.
- [RF11] §2: “new protocol designs should not employ HMAC-MD5” — bài trước ghi rộng “thiết kế mới không dùng MD5”; nay sửa đúng phạm vi.
- [GIT] hash-function-transition: tiêu chí “2. High quality implementations should be widely available (e.g., in OpenSSL and Apple
  CommonCrypto).” → khớp “có sẵn trong nhiều thư viện” ở chặng 4.
- Tốc độ băm 10⁹ lần mỗi giây, 10 000 tệp, 64 bit cho khử trùng tệp: SỐ MINH HOẠ, ghi rõ trên màn hình.
