# Nguồn đã đọc nguyên văn cho SWF L13 (bài hành trình: kho mã đơn khối của Google)

Đọc ngày 2026-11-02 (curl + trích văn bản bằng script). Chỉ trích các câu bài giảng dựa vào (CITED); mọi con số khác trong bài là phép
tính lại (VER, `checks` của bài và `audit/swf/verify_swf.py` L13) hoặc ghi rõ “(số minh hoạ)”. Không nêu tên cá nhân trong lời đọc; tên tác
giả chỉ ở `source:`.

## Nguồn ứng viên KHÔNG đọc được: R. Potvin, J. Levenberg, *Why Google Stores Billions of Lines of Code in a Single Repository*, CACM 59(7), 2016
- cacm.acm.org/research/why-google-stores-billions-of-lines-of-code-in-a-single-repository/ → 403 (Cloudflare), cả curl lẫn WebFetch;
  dl.acm.org/doi/10.1145/2854146 và /doi/fullHtml/… → 403; m-cacm.acm.org → 403.
- Bản lưu trữ web.archive.org (ảnh chụp 2024-02-29 và 2025-11-12 có tồn tại theo API “available”) → 429 Too Many Requests ở mọi lần thử
  (10 lần trong khoảng 25 phút, cách nhau 150 giây); WebFetch không truy cập được web.archive.org.
- research.google/pubs/why-google-stores-billions-of-lines-of-code-in-a-single-repository/ chỉ có tóm tắt, không có PDF; bản
  pubs/archive/45424.pdf → 404.
- Tóm tắt (đọc được): “Google's monolithic repository provides a common source of truth for tens of thousands of developers around the world.”
- KẾT LUẬN: bài giảng KHÔNG dùng con số nào của bài này. Thay bằng các nguồn chính thức khác của chính Google có ngày tháng: [ET11], [TB11],
  [CM13], [FT16], [TM17], [SE20] (dưới). [SE20] chương 16 xác nhận: “In 2016, we published a (highly cited, much discussed) paper on Google’s
  monorepo approach.” [TM17] dẫn bài này là tài liệu tham khảo [3].

## [ET11] J. Thomas, A. Kumar, *Welcome to the Google Engineering Tools blog!*, Google Engineering Tools Blog, 2011-05-03
Tải: google-engtools.blogspot.com/2011/05/welcome-to-google-engineering-tools.html (trang động) → nội dung qua nguồn Atom chính thức
www.blogger.com/feeds/8477590467225772179/posts/default/2598871672046038394 (published 2011-05-03T09:49:00-07:00).
- “To get a sense of the size and scale of our challenge, take a look at some of these stats from a talk Ashish (Director, Engineering Tools)
  gave last year:” → bài nói năm 2010.
- “5000+ developers across 40+ offices around the world” · “20+ changes per minute; 50% code base changes every month” · “More than 50 million
  test cases executed every day” · “Single-rooted code tree with mixed language code” · “Development on head; all releases from source”.

## [TB11] P. Gupta, M. Ivey, J. Penix, *Testing at the speed and scale of Google*, Google Testing Blog, 2011-06-14
Tải: testing.googleblog.com/2011/06/testing-at-speed-and-scale-of-google.html (curl, 200).
- “As more code is added, each clean run takes much longer and more changes gets crammed into a single run.”
- “The code base receives 20+ code changes per minute and 50% of the files change every month!”
- “we built a continuous integration system that uses dependency analysis to determine all the tests a change transitively affects and then
  runs only those tests for every change.”
- “The gmail_server_tests are broken by the second change, however a typical continuous integration system will only be able to tell that
  either change #2 or change #3 caused this test to fail.”
- Trả lời bình luận của tác giả: “The build rules are defined as per compiler specifications, and then the dependency graph generation is
  automatic.”

## [CM13] H. K. Wright, D. Jasper, M. Klimek, C. Carruth, Z. Wan, *Large-Scale Automated Refactoring Using ClangMR*, ICSM 2013
Tải: static.googleusercontent.com/media/research.google.com/en//pubs/archive/41342.pdf (PDF 4 trang; trang research.google/pubs/pub41342
ghi năm 2013).
- Abstract: “a sample large-scale refactoring effort recently completed which modified over 35,000 function call sites across 100 million
  lines of code.”
- Motivation: “Google maintains a large mixed-language codebase in a single repository, with a significant portion written in C++.”
- “At the time, there were roughly 45,000 callers of SplitStringUsing, and migrating them by hand was infeasible.”
- “A “safe” transformation meets the following criteria: …” (công cụ chỉ đổi chỗ thoả điều kiện an toàn).
- “The initial ClangMR program transformed about 35,000 callers of SplitStringUsing to strings::Split, and these changes were mailed for review
  in 3,100 separate chunks, though not all simultaneously. These were often reviewed quite quickly, with an 80th-percentile review time of just
  over two minutes. The bulk of reviews were completed over two months”.

## [FT16] J. Micco, *Flaky Tests at Google and How We Mitigate Them*, Google Testing Blog, 2016-05-27
Tải: testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html (curl, 200).
- “we see a continual rate of about 1.5% of all test runs reporting a "flaky" result.” “Almost 16% of our tests have some level of flakiness
  associated with them!” “more than 1 in 7 of the tests”.
- “about 84% of the transitions we observe from pass to fail involve a flaky test!”
- “consider that the average project contains 1000 or so individual tests. … If 1.5% of test results are flaky, 15 tests will likely fail”.
- “It is human nature to ignore alarms when there is a history of false signals coming from a system. For example, see this article about
  airline pilots ignoring an alarm on 737s.” “Ignoring legitimate failures at this stage results in the submission of broken code.”
- “We even have a way to denote a test as flaky - causing it to report a failure only if it fails 3 times in a row.” “Imagine a 15 minute
  integration test marked as flaky … The breakage will not be discovered until 3 executions of the test complete, or 45 minutes”.

## [TM17] A. Memon, Z. Gao, B. Nguyen, S. Dhanda, E. Nickell, R. Siemborski, J. Micco, *Taming Google-Scale Continuous Testing*, ICSE-SEIP 2017
Tải: static.googleusercontent.com/media/research.google.com/en//pubs/archive/45861.pdf (PDF 10 trang).
- “Google’s Test Automation Platform (TAP) system, responsible for CI of Google’s vast majority of 2 Billion LOC codebase—structured largely
  as a single monolithic code tree”.
- “In an average day, TAP integrates and tests— at enormous compute cost—more than 13K code projects, requiring 800K builds and 150 Million
  test runs.”
- “A milestone is typically cut every 45 minutes during peak development time”.
- “we report results of studying over 500K CLs, from Feb. 11, to Mar. 11, 2016”.


## [SE20] T. Winters, T. Manshreck, H. Wright (biên tập), *Software Engineering at Google*, O’Reilly, 3/2020 — bản HTML chính thức
Tải: abseil.io/resources/swe-book (trang giới thiệu: “In March, 2020, we published a book titled “Software Engineering at Google””; bản số
miễn phí do chính nhóm tác giả đưa lên abseil.io, giấy phép CC BY-NC-ND 4.0). Các chương đọc: 16 (html/ch16.html), 22 (ch22.html),
9 (ch09.html), 23 (ch23.html).

### Chương 16 — Version Control and Branch Management
- “we find “trunk-based development” as popularized by DevOps (one repository, no dev branches) to be a particularly scalable policy approach”
- Distributed VCS: “most existing tools don’t scale well with 50,000 engineers and tens of millions of commits.”
- Version Control at Google: “At Google, the vast majority of our source is managed in a single repository (monorepo) shared among roughly
  50,000 engineers.” “We rely on an in-house-developed centralized VCS called Piper” … “a globally available VCS storing more than 80 TB of
  content and metadata.” “we’ll regularly handle 60,000 to 70,000 commits to the repository per work day.”
- “it takes perhaps 15 seconds total to create a new client at trunk, add a file, and commit an (unreviewed) change to Piper.”
- “at every level of the file hierarchy, we can find OWNERS files that list the usernames of engineers that are allowed to approve commits
  within that subtree of the repository”.
- One Version: “For every dependency in our repository, there must be only one version of that dependency to choose.”
- (Nearly) No Long-Lived Branches: “development branches should be minimal, or at best be very short lived.” “work should be done in small
  increments against trunk, committed regularly.” “Across the roughly 1,000 teams that work in the Google monorepo, there are only a couple that
  have such a dev branch.” “every job in production needs to be rebuilt and redeployed every six months, maximum.”
- Dev Branches: “When there are multiple branches being developed in isolation for long periods, coordinating merge operations becomes
  significantly more expensive (and possibly riskier) than they would be with trunk-based development.” “The alternative requires a different
  paradigm: trunk-based development, rely heavily on testing and CI, keep the build green, and disable incomplete/untested features at runtime.”
- Monorepos: “In 2016, we published a (highly cited, much discussed) paper on Google’s monorepo approach.” “no, we don’t think the monorepo
  approach as we’ve described it is the perfect answer for everyone.” “What is important is not whether we focus on monorepo; it’s to adhere to
  the One-Version principle to the greatest extent possible”. “Choice violations of the One-Version Rule lead to merge strategy discussions,
  diamond dependencies, lost work, and wasted effort.” “if every project in your organization has the same secrecy, legal, privacy, and security
  requirements, a true monorepo is a fine way to go. Otherwise, aim for the functionality of a monorepo”.
- Future of Version Control: “Even though Piper has done very well for us, investing in a highly scaling VMR and tools to manage it … could have
  been a better investment.”

### Chương 22 — Large-Scale Changes
- “as a codebase and the number of engineers working in it grows, the largest atomic change possible counterintuitively decreases”.
- “an LSC is any set of changes that are logically related but cannot practically be submitted as a single atomic unit.”
- Testing: “Finding the root cause of a test failure in a change of 25 files is pretty straightforward; finding 1 in a 10,000-file change is
  like the proverbial needle in a haystack.” “Today it is common for a double-digit percentage (10% to 20%) of the changes in a project to be the
  result of LSCs”.
- TAP train: “For each change on the train, run a sample of 1,000 randomly-selected tests.”
- “Google’s codebase had more than 500,000 references to scoped_ptr” … “At the height of the migration process, we were consistently
  generating, testing and committing more than 700 independent changes, touching more than 15,000 files per day.”
- Codebase Insight: “if a change requires more than 500 edits, it’s usually more efficient for an engineer to learn and execute our
  change-generation tools rather than manually execute that edit.”
- Change Management: “At Google, this tool is called Rosie” … “split the large sets of comprehensive changes produced by tooling into smaller
  shards, which can be tested, reviewed, and submitted independently.”
- Sharding: “Rosie takes a large change and shards it based upon project boundaries and ownership rules”; “it caps the number of outstanding
  shards for any given LSC, runs at lower priority”.
- Testing: “the vast majority of shards affect fewer than one thousand tests, out of the millions across our codebase.”
- Policies: “code owners … don’t hold a veto over the broader LSC.” Authorization: “direct all of the code reviews for an LSC to go to a single
  "global approver."”

### Chương 9 — Code Review
- “Only one LGTM is required by default”. “Approval from one of the code owners” … “Google’s codebase is a tree structure with hierarchical
  owners of particular directories.” “a given file is generally owned by the union of the members of all the OWNERS files above it in the
  directory tree.” “When new projects are created … a new OWNERS file is sufficient.” “This ownership mechanism is simple, yet powerful, and has
  scaled well over the past two decades.” “tens of thousands of engineers can operate efficiently on billions of lines of code in a single
  repository.”

### Chương 23 — Continuous Integration
- “TAP is the gateway for almost all changes at Google. Every day it is responsible for handling more than 50,000 unique changes and running
  more than four billion individual test cases.”
- “we typically limit presubmit tests to just those for the project where the change is happening.”
- “Some teams rely on a tool to remove such flaky tests from presubmit temporarily while the flakiness is investigated and fixed.”
  “We also have a system for flake classification, which uses statistics to classify flakes at a Google-wide level”. “After a change has been submitted, we use
  TAP to asynchronously run all potentially affected tests, including larger and slower tests.”
- “we don’t want to run unreliable tests on presubmit”. “Policies that say, “Nobody can commit if our latest CI results aren’t green” are
  probably misguided.”
- Culprit finding: “TAP automatically splits a failing batch up into individual changes and reruns the tests against each change in isolation.”
  “culprit finding tools that an individual developer can use to binary search through a batch of changes”.

## Điều KHÔNG dạy (nguồn không ghi)
- Mọi con số của Potvin & Levenberg 2016 (số tệp, số dòng, số lần gộp, dung lượng, năm chuyển hệ quản lý phiên bản): chưa đọc nguyên văn
  → không dạy. Số “2 tỉ dòng” trong bài lấy từ [TM17], không từ bài CACM.
- Năm Google bắt đầu dùng một kho, tên và năm thay hệ quản lý phiên bản cũ: các nguồn đã đọc không ghi → không dạy.
- “20+ changes per minute” là cận dưới; 28 800 mỗi ngày là phép tính lại giả sử đều suốt 24 giờ (“hơn”), nguồn không ghi số mỗi ngày.
- 32 mốc mỗi ngày: phép tính lại giả sử cả ngày đều 45 phút; [TM17] chỉ ghi 45 phút ở giờ cao điểm.
- 2 phút mỗi phần duyệt: [CM13] chỉ ghi phân vị 80 “just over two minutes”, không ghi tổng giờ duyệt → 103,3 giờ là số minh hoạ.
- Đồ thị 1 thư viện chung + 2 dự án, lô 16 / 8 thay đổi, dự án 1000 thay đổi, công ty 40 kỹ sư, 5 đội, 2 lần gộp mỗi ngày, 15 ngày: số minh hoạ.
- Số lần chia đôi thật mà công cụ tìm lỗi của Google cần: [SE20] chỉ ghi “binary search through a batch of changes”, không ghi số.
- 60 000–70 000 lần gộp mỗi ngày gồm cả “semiautomated processes” — không chia ra người và máy, nên bài không tính “mỗi kỹ sư mấy lần”.

