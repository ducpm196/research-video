# Nguồn đã đọc nguyên văn cho TOC L14 (bài hành trình: khớp biểu thức chính quy, 1968 → 2025)

Đọc ngày 2026-11-02 (urllib/curl + trích văn bản; PDF bằng pdftotext). Chỉ trích các câu bài giảng dựa vào (CITED); mọi con số khác
trong bài là phép tính lại (VER: `checks` của bài, `audit/toc/verify_toc.py` mục L14, `audit/verify_plan_curricula.py` TOC:L14) hoặc ghi
rõ “(số minh hoạ)”. Không nêu tên cá nhân trong lời đọc; tên tác giả chỉ ở `source:`. Bài hậu kiểm năm 2019 ghi “An engineer wrote a
regular expression…” — bài giảng KHÔNG nêu người đó và không quy sự cố về một người (bài hậu kiểm liệt kê 11 nguyên nhân góp phần).

## [TH68] K. Thompson, *Regular expression search algorithm*, Communications of the ACM 11(6), 6/1968, tr. 419–422
Bản ACM (dl.acm.org/doi/10.1145/363347.363387, cả trang tóm tắt lẫn PDF) trả **403** với curl và WebFetch. Liên kết PDF mà [CX07] dẫn
(cs.chalmers.se/~coquand/AUTOMATA/thompson.pdf) trả 404; web.archive.org trả 429. Đã đọc **bản chép quét** của chính bài báo tại
www.oilshell.org/archive/Thompson-1968.pdf (529 788 byte, pdftotext) — đầu trang ghi “Volume 11 / Number 6 / June, 1968 … Communications
of the ACM 419”. Mọi điều bài giảng nói về [TH68] cũng được [CX07] và [CF19] dẫn lại.
- Tóm tắt: “A method for locating specific character strings embedded in character text is described and an implementation of this method
  in the form of a compiler is discussed. The compiler accepts a regular expression as source language and produces an IBM 7094 program as
  object language.”
- The Algorithm: “Previous search algorithms involve backtracking when a partially successful search path fails. This necessitates a lot of
  storage and bookkeeping, and executes slowly. In the regular expression recognition technique described in this paper, each character in
  the text to be searched is examined in sequence against a list of all possible current characters. During this examination a new list of
  all possible next characters is built. When the end of the current list is reached, the new list becomes the current list, the next
  character is obtained, and the process continues.” … “The parallel nature of this algorithm makes it extremely fast.”
- “This compile-search algorithm is incorporated as the context search in a time-sharing text editor.”

## [CX07] R. Cox, *Regular Expression Matching Can Be Simple And Fast (but is slow in Java, Perl, PHP, Python, Ruby, ...)*, 1/2007
Tải: swtch.com/~rsc/regexp/regexp1.html (59 115 byte, HTTP 200).
- Hình đầu: “Notice that Perl requires over sixty seconds to match a 29-character string. The other approach, labeled Thompson NFA … requires
  twenty microseconds to match the string.” “the Thompson NFA handles a 100-character string in under 200 microseconds, while Perl would
  require over 10^15 years.”
- “there are no regular expressions that are pathological for the Thompson NFA implementation.”
- “Thompson chose not to use his algorithm when implementing the text editor ed … (1971), or in its descendant grep … (1973). Instead, these
  venerable Unix tools used recursive backtracking! Backtracking was justifiable because the regular expression syntax was quite limited”.
  “Al Aho's egrep, which first appeared in the Seventh Edition (1979), was the first Unix tool to provide the full regular expression syntax,
  using a precomputed DFA.”
- Quay lui: “One way to simulate perfect guessing is to guess one option, and if that doesn't work, try the other.” “in the worst case, there
  can be exponentially many possible execution paths”. Nhiều trạng thái cùng lúc: “This multi-state approach tries both paths at the same
  time, reading the input only once.” “In an NFA with n nodes, there can only be n reachable states at any step, but there might be 2^n
  paths through the NFA.”
- Dựng NFA: “this technique creates exactly one state per character or metacharacter in the regular expression, excluding parentheses.
  Therefore the number of states in the final NFA is at most equal to the length of the original regular expression.”
- Ví dụ bệnh: “Consider the regular expression a?^n a^n. It matches the string a^n when the a? are chosen not to match any letters … There are
  n such choices to make, a total of 2^n possibilities. Only the very last possibility—choosing zero for all the ?—will lead to a match.
  The backtracking approach thus requires O(2^n) time, so it will not scale much beyond n=25.” “Thompson's algorithm maintains state lists of
  length approximately n … for a total of O(n^2) time.”
- “PCRE stops getting the right answer at n=23, because it aborts the recursive backtracking after a maximum number of steps.”
- “Although not benchmarked here, Java uses a backtracking implementation too.”
- “while examples as dramatic as this one rarely occur in practice, less dramatic ones do occur. Examples include using (.*) (.*) (.*) (.*)
  (.*) to split five space-separated fields”.
- Tham chiếu ngược: “backreferences … The power that backreferences add comes at great cost: in the worst case, the best known
  implementations require exponential search algorithms”. “(cat|dog)\1 matches catcat and dogdog but not catdog nor dogcat.”
- History: “Henry Spencer reimplemented the Eighth Edition library interface from scratch, but using backtracking … It became very widely
  used, eventually serving as the basis for the slow regular expression implementations mentioned earlier: Perl, PCRE, Python, and so on.”
  (Bài giảng không nêu tên người; chỉ nói “một thư viện quay lui phổ biến được chép lại rộng rãi”.)

## [CX10] R. Cox, *Regular Expression Matching in the Wild*, 3/2010
Tải: swtch.com/~rsc/regexp/regexp3.html (57 102 byte, HTTP 200).
- “I spent the summer of 2006 building Code Search … We originally planned to use PCRE … until we realized that it used a backtracking
  algorithm, meaning it is easy to make searches take exponential time or arbitrary stack depth. Since Code Search accepts regular expressions
  from anyone on the Internet, using PCRE would have left it open to easy denial of service attacks.”
- “The result, RE2, provides most of the functionality of PCRE … but it guarantees linear time execution and a fixed stack footprint. RE2 is
  now in widespread use at Google”. “As of March 2010, RE2 is an open source project”.
- “RE2 disallows PCRE features that cannot be implemented efficiently using automata. (The most notable such feature is backreferences.)”
- Summary: “RE2 requires about 10 KB per regexp, in contrast to PCRE's half a KB or so. In exchange for the extra space, RE2 guarantees
  linear-time performance, although the linear-time constant varies by situation.” “It runs at about half the speed for ambiguous regexps with
  small matches, and considerably slower for ambiguous regexps with large matches.”
- “The parser does not use recursive descent, because the recursion depth would be potentially unbounded and might overflow the stack”.

## [CF19] Cloudflare Blog, *Details of the Cloudflare outage on July 2, 2019*, đăng 12/7/2019
Tải: blog.cloudflare.com/details-of-the-cloudflare-outage-on-july-2-2019/ (373 736 byte, HTTP 200). Bài hậu kiểm chính thức của công ty.
- “On July 2, we deployed a new rule in our WAF Managed Rules that caused CPUs to become exhausted on every CPU core that handles
  HTTP/HTTPS traffic on the Cloudflare network worldwide.” “this resulted in our customers … seeing a 502 error page”.
- “the update contained a regular expression that backtracked enormously and exhausted CPU used for HTTP/HTTPS serving.”
- “the real story of how the Cloudflare service went down for 27 minutes is much more complex than “a regular expression went bad”.”
- Dòng thời gian (UTC): “At 13:42 … deployed a minor change to the rules for XSS detection via an automatic process.” “Three minutes later the
  first PagerDuty page went out”. “a leader … told me we had lost 80% of our traffic.” “At 14:00 the WAF was identified as the component
  causing the problem”. “a team member executed the global WAF termination at 14:07 and by 14:09 traffic levels and CPU were back to expected
  levels worldwide.” “At 14:52 … the WAF was re-enabled globally.”
- “In the last 60 days, 476 change requests have been handled for the WAF Managed Rules (averaging one every 3 hours).”
- “This particular change was to be deployed in “simulate” mode … But even in the simulate mode the rules actually need to execute”.
- “The SOP for a rule change specifically allows it to be pushed globally. This is very different from all the software we release … where
  the SOP first pushes software to an internal dogfooding network point of presence … then to a small number of customers … followed by a
  push to numerous customers and finally to the world.”
- Kiểm thử: “What it didn't do was test for runaway CPU utilization by the WAF and examining the log files from previous WAF builds shows that
  no increase in test suite run time was observed”.
- “On average, we hit a p99 of 2.29s for a change to be distributed to every machine worldwide.”
- “The Lua WAF uses PCRE internally, and it uses backtracking for matching and has no mechanism to protect against a runaway expression.”
- What went wrong (11 mục), gồm: “A protection that would have helped prevent excessive CPU use by a regular expression was removed by mistake
  during a refactoring of the WAF weeks prior”; “The regular expression engine being used didn't have complexity guarantees.”; “The test
  suite didn't have a way of identifying excessive CPU consumption.”; “The SOP allowed a non-emergency rule change to go globally into
  production without a staged rollout.”; “The rollback plan required running the complete WAF build twice taking too long.” — và câu dẫn:
  “Getting to a single root cause, while satisfying, may obscure the reality.”
- Sau sự cố: “Re-introduce the excessive CPU usage protection that got removed. (Done)”; “Manually inspecting all 3,868 rules in the WAF
  Managed Rules to find and correct any other instances of possible excessive backtracking.”; “Introduce performance profiling for all rules
  to the test suite.”; “Switching to either the re2 or Rust regex engine which both have run-time guarantees.”; “Changing the SOP to do staged
  rollouts of rules … while retaining the ability to do emergency global deployment for active attacks.”
- Phụ lục: “we can safely ignore it and treat the pattern as .*.*=.*”. “It takes 23 steps for this match to happen.” “if the string is
  changed from x=x to x=xx ? This time is takes 33 steps to match. And if the input is x=xxx it takes 45. That's not linear.” “With 20 x's
  after the = the engine takes 555 steps to match! (Worse, if the x= was missing, so the string was just 20 x's, the engine would take 4,067
  steps to find the pattern doesn't match).” “.*.*=.*; … To match x=x takes 90 steps instead of 23. … Matching x= followed by 20 x's takes
  5,353 steps.” (số bước đếm bằng Perl Regexp::Debugger, theo bài viết)
- Bổ sung, đọc lại 2026-11-09 (WebFetch, đợt C): “Everything that occurred up to the point the rules were deployed was done “correctly””
  (căn cứ bài học sai 1: “mọi bước quy trình đều đã làm đúng thủ tục”); “Because of the sensitivity of the situation we performed both
  negative tests … in a single city using a subset of traffic after removing our paying customers’ traffic from that location.” và “At 14:52
  we were 100% satisfied … the WAF was re-enabled globally.” (căn cứ dòng 14:52 “bật lại sau khi thử ở một thành phố”); “Changing the
  catastrophic example .*.*=.*; to .*?.*?=.*?; doesn’t change its run time at all. … x= followed by 20 x’s still takes 5,353 steps.” (căn cứ
  bài học sai 4 “vẫn 5353 bước”); “And the number of steps grows very quickly.” (căn cứ “còn tăng nhanh hơn”).
- “If the original expression is changed to .*?.*?=.*? then matching x=x takes 11 steps … But laziness isn't the total solution …
  Changing the catastrophic example .*.*=.*; to .*?.*?=.*?; doesn't change its run time at all.”
- “The solution to this problem has been known since 1968 when Ken Thompson wrote a paper … The paper describes a mechanism for converting a
  regular expression into an NFA … using an algorithm that executes in time linear in the size of the string being matched against.”
  “Figure 0 has five states starting at 0.” “Each character was processed once so the algorithm was linear in the length of the input string.”

## [R2] google/re2, README.md (nhánh main), phần đầu; wiki “WhyRE2”
Tải: raw.githubusercontent.com/google/re2/main/README.md (11 420 byte). Trang wiki github.com/google/re2/wiki/WhyRE2 ghi: “Russ Cox edited
this page Jul 30, 2025 … “Why RE2” moved to the top of the README.md.” → bài giảng ghi mốc chặng 5 là 2025 (năm phần giới thiệu được đặt ở
đầu README), không khẳng định ngày viết từng câu.
- “RE2 is an efficient, principled regular expression library that has been used in production at Google and many other places since 2006.”
- “Safety is RE2's primary goal.” “designed and implemented with an explicit goal of being able to handle regular expressions from untrusted
  users without risk. One of its primary guarantees is that the match time is linear in the length of the input string.”
- “the parser, the compiler and the execution engines limit their memory usage by working within a configurable budget—failing gracefully
  when exhausted—and they avoid stack overflow by eschewing recursion.”
- “It is not a goal to be faster than all other engines under all circumstances. … more complex expressions may incur larger constant
  factors”. “RE2 is pessimistic where a backtracking engine is optimistic: A backtracking engine tests each alternative sequentially, making it
  fast when the first alternative is common. By contrast RE2 evaluates all alternatives in parallel”.
- “As a matter of principle, RE2 does not support constructs for which only backtracking solutions are known to exist. Thus, backreferences
  and look-around assertions are not supported.”

## Điều KHÔNG dạy (nguồn không ghi hoặc không đọc được)
- Bản ACM của [TH68]: không đọc được (403); chỉ dạy ý trong bản chép quét đã đọc, và ý đó cũng có trong [CX07], [CF19]. Không dạy chi
  tiết mã IBM 7094.
- Số bước Perl trong [CF19] là CITED; bài giảng KHÔNG tự tính lại 23, 33, 45 bằng bộ đếm riêng. Bộ đếm `alg.bt_match` của bài đếm
  “một lần đặt một ký hiệu của mẫu vào một vị trí” — đơn vị khác, chỉ dùng để thấy tốc độ tăng.
- Đa thức k² + 7k + 15 là phép KHỚP do bài dựng từ ba điểm 23, 33, 45 (VER), kiểm bằng điểm thứ tư 555 — nguồn không viết công thức này.
- Cloudflare đã chuyển sang bộ máy nào, ngày nào: bài hậu kiểm chỉ ghi kế hoạch (“ETA: July 31”) → bài giảng chỉ nói “kế hoạch”.
- Tên kỹ sư, tên người viết thư viện quay lui: không nêu.
- Hiệu năng RE2 năm 2025 so với bộ máy khác: README không cho số → không dạy số.
