# Nguồn đã đọc nguyên văn cho CAS L07 (Cloudflare, 2/7/2019)

Đọc ngày 2026-11-02 (urllib + trích văn bản HTML; bản tải ở thư mục nháp của phiên). Chỉ trích các câu bài giảng dựa vào (CITED). Khoảng
thời gian và bộ đếm quay lui là phép tính lại (VER: `checks`, `audit/cas/ver/L07.py`, `audit/verify_plan_curricula.py` CAS:L07).
Đã đối chiếu với TOC L14 (`audit/toc/sources_L14.md` [CF19], cùng URL): 13:42 → 14:09 = 27 phút, 80%, 476 thay đổi / 60 ngày, p99 2,29 s,
3868 quy tắc, 4067 bước — không con số nào mâu thuẫn. TOC L14 dạy góc bộ máy khớp (Thompson → RE2); bài này dạy góc hậu kiểm.

## [CF19] Cloudflare Blog, *Details of the Cloudflare outage on July 2, 2019*, đăng 12/7/2019
URL: https://blog.cloudflare.com/details-of-the-cloudflare-outage-on-july-2-2019/ (HTTP 200, 373 334 byte). Bài hậu kiểm chính thức.
- “On July 2, we deployed a new rule in our WAF Managed Rules that caused CPUs to become exhausted on every CPU core that handles HTTP/HTTPS
  traffic on the Cloudflare network worldwide.” … “seeing a 502 error page”.
- Dòng thời gian (UTC): “At 13:31 an engineer on the team had merged a Pull Request containing the change after it was approved.” “At 13:37
  TeamCity built the rules and ran the tests, giving it the green light.” “With the tests passing, TeamCity automatically began deploying the
  change at 13:42.” “Three minutes later the first PagerDuty page went out indicating a fault with the WAF. This was a synthetic test that checks
  the functionality of the WAF … from outside Cloudflare”. “we had lost 80% of our traffic.” “At 14:00 the WAF was identified as the component
  causing the problem and an attack dismissed as a possibility.” “At 14:02 … it was proposed that we use a ‘global terminate’, a mechanism built
  into Cloudflare to disable a single component worldwide.” “with our Access service down we couldn’t authenticate to our internal control
  panel (and once we were back we’d discover that some members of the team had lost access because of a security feature that disables their
  credentials if they don’t use the internal control panel frequently).” “we had to use a bypass mechanism that wasn’t frequently used”.
  “a team member executed the global WAF termination at 14:07 and by 14:09 traffic levels and CPU were back to expected levels worldwide.”
  “we performed both negative tests … and positive tests … in a single city using a subset of traffic”. “At 14:52 … the WAF was re-enabled
  globally.”
- “the real story of how the Cloudflare service went down for 27 minutes is much more complex than “a regular expression went bad”.”
- “The SOP for a rule change specifically allows it to be pushed globally. This is very different from all the software we release at
  Cloudflare where the SOP first pushes software to an internal dogfooding network point of presence (PoP) (which our employees pass through),
  then to a small number of customers in an isolated location, followed by a push to numerous customers and finally to the world.”
- “This particular change was to be deployed in “simulate” mode … But even in the simulate mode the rules actually need to execute”.
- “In the last 60 days, 476 change requests have been handled for the WAF Managed Rules (averaging one every 3 hours).”
- “On average, we hit a p99 of 2.29s for a change to be distributed to every machine worldwide.”
- Kiểm thử: “These HTTP requests are designed to test requests that should be blocked by the WAF … and those that should be let through …
  What it didn't do was test for runaway CPU utilization by the WAF”.
- “Everything that occurred up to the point the rules were deployed was done “correctly”: a pull request was raised, it was approved, CI/CD
  built the code and tested it, a change request was submitted with an SOP detailing rollout and rollback, and the rollout was executed.”
- “Getting to a single root cause, while satisfying, may obscure the reality. Here are the multiple vulnerabilities that converged” — 11 mục,
  gồm: “A protection that would have helped prevent excessive CPU use by a regular expression was removed by mistake during a refactoring of the
  WAF weeks prior”; “The regular expression engine being used didn't have complexity guarantees.”; “The test suite didn't have a way of
  identifying excessive CPU consumption.”; “The SOP allowed a non-emergency rule change to go globally into production without a staged
  rollout.”; “The rollback plan required running the complete WAF build twice taking too long.”; “The first alert for the global traffic drop
  took too long to fire.”; “We had difficulty accessing our own systems because of the outage and the bypass procedure wasn’t well-trained
  on.”; “SREs had lost access to some systems because their credentials had been timed out for security reasons.”
- Sau sự cố: “Re-introduce the excessive CPU usage protection that got removed. (Done)”; “Manually inspecting all 3,868 rules … (Inspection
  complete)”; “Introduce performance profiling for all rules to the test suite. (ETA: July 19)”; “Switching to either the re2 or Rust regex
  engine which both have run-time guarantees. (ETA: July 31)”; “Changing the SOP to do staged rollouts of rules in the same manner used for other
  software at Cloudflare while retaining the ability to do emergency global deployment for active attacks.”
- Phụ lục: “we can safely ignore it and treat the pattern as .*.*=.*”. “(Worse, if the x= was missing, so the string was just 20 x ’s, the
  engine would take 4,067 steps to find the pattern doesn’t match).” Số bước đo bằng “Perl Regexp::Debugger” (theo bài viết).

## Phép tính của bài (VER)
- 27, 3, 18, 5, 43, 6 phút từ các mốc trên.
- Bộ đếm của bài (tổng alg.bt_match qua mọi vị trí bắt đầu, chuỗi n chữ x không có “=”): 26 (n = 2), 638, 3773, 358 853, 2 767 703
  (n = 10, 20, 100, 200); tỉ số n = 200 / n = 100 ≈ 7,7 → bậc n³. Đơn vị KHÁC “steps” của công cụ Perl (4067) — bài nói rõ không so từng số.
- Quiz: 0,8 × 27 = 21,6; 0,01 × 8 = 0,08; 270 lần (số minh hoạ cho bậc 1% lưu lượng); 4 × 15 = 60 phút.

## Điều KHÔNG dạy (nguồn không ghi hoặc bài không cần)
- Tên kỹ sư (“An engineer wrote a regular expression…”; bài viết do một lãnh đạo ký): không nêu, không quy sự cố cho người viết biểu thức.
- Chuỗi tấn công XSS mà quy tắc nhắm tới và toàn văn biểu thức: chỉ dùng lõi `.*.*=.*` như phụ lục.
- Đã đổi bộ máy khớp hay chưa, ngày nào: bài chỉ có kế hoạch (ETA) → bài nói “việc công ty ghi sẽ làm”, không nói “đã đổi”.
- Ý “mỗi yêu cầu đều chạy biểu thức” là suy từ câu “caused CPUs to become exhausted on every CPU core that handles HTTP/HTTPS traffic” và
  câu về chế độ mô phỏng (INFERRED, bài không đưa con số độ dài chuỗi nào).

## Đọc lại đợt C (2026-11-09; curl -L, cùng URL, HTTP 200, 373 518 byte)
- “by design, the WAF doesn’t use this process because of the need to respond rapidly to threats” → khớp câu lời đọc “quy tắc phải nhanh
  để chặn tấn công mới”.
- “The 502 errors were generated by the front line Cloudflare web servers that still had CPU cores available but were unable to reach the
  processes that serve HTTP/HTTPS traffic” → bài thêm giải nghĩa lỗi 502 (“máy tiếp nhận không gọi được phần xử lý phía sau”).
- Bộ máy khớp “run-time guarantees” (re2 / Rust regex) vẫn chỉ là việc có ETA → tổng kết nói “việc công ty ghi sẽ làm”; “thời gian tăng tỉ lệ
  với độ dài chuỗi” là tính chất của bộ khớp không quay lui (INFERRED từ “run-time guarantees”, không phải câu của bài hậu kiểm).
