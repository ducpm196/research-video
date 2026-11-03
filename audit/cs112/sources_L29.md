# Nguồn đã đọc nguyên văn cho CS112 L29 (bài hành trình: Timsort, 2002 → 2025)

Đọc ngày 2026-11-02 (curl/urllib + trích văn bản; PDF bằng pdftotext; lịch sử commit bằng GitHub API). Chỉ trích các câu bài giảng dựa
vào (CITED); mọi con số khác là phép tính lại (VER: `checks` của bài và `audit/cs112/verify_cs112.py` mục T29a–T29f) hoặc ghi
“(số minh hoạ)”. Không nêu tên cá nhân trong lời đọc; tên tác giả chỉ ở `source:` và trên màn hình nguồn (Munro & Wild là tên phương pháp).
Bài giảng không quy lỗi cho người viết thư viện (pitfall 1).

## [LS02] T. Peters, `Objects/listsort.txt`, CPython — commit đầu 92f81f2e63 ngày 2002-08-01 (“Checking in the doc file for "timsort"”)
Tải: raw.githubusercontent.com/python/cpython/92f81f2e63/Objects/listsort.txt (28 438 byte) và bản thẻ v2.3.7 (31 473 byte); lịch sử commit
qua api.github.com/repos/python/cpython/commits?path=Objects/listsort.txt.
- Intro: “This describes an adaptive, stable, natural mergesort, modestly called timsort … It has supernatural performance on many kinds of
  partially ordered arrays (less than lg(N!) comparisons needed, and as few as N-1), yet as fast as Python's previous highly tuned samplesort
  hybrid on random arrays.”
- “In a nutshell, the main routine marches over the array once, left to right, alternately identifying the next run, then merging it into
  the previous runs "intelligently".”
- Bảng số đo (bản 2.3.7): n = 1048576, \sort timsort 1048575; *sort lg(n!) = 19458756, timsort 19606028.
- Computing minrun: “If N < 64, minrun is N. IOW, binary insertion sort is used for the whole array then”. “Because sortperf.py only tries
  powers of 2, it took a long time to notice that 32 isn't a good choice for the general case! Consider N=2112: >>> divmod(2112, 32) (66, 0)
  … leaving runs of lengths 2048 and 64 to merge at the end … a lot more data movement (O(N) copies just to get 64 elements into place). If
  we take minrun=33 in this case, then we're very likely to end up with 64 runs each of length 33, and then all merges are perfectly
  balanced.” “take the first 6 bits of N, and add 1 if any of the remaining bits are set.”
- The Merge Pattern: “Stability constrains permissible merging patterns … The merging must be done as (A+B)+C or A+(B+C) instead.”
  “maintains two invariants on the stack entries, where A, B and C are the lengths of the three righmost not-yet merged slices: 1. A > B+C
  2. B > C”. “#1 implies that, reading the lengths right to left, the pending-run lengths grow at least as fast as the Fibonacci numbers.
  Therefore the stack can never grow larger than about log_base_phi(N) entries”. “If A <= B+C, the smaller of A and C is merged with B”.
  (Câu bất biến giống hệt ở commit 2002 và bản 2.3.7.)

## [J11] Java: OpenJDK jdk7 `java/util/TimSort.java`; trang dự án JDK 7; ghi chú tương thích Java SE 7 của Oracle
Tải: raw.githubusercontent.com/openjdk/jdk/jdk7-b147/jdk/src/share/classes/java/util/TimSort.java (36 163 byte); openjdk.org/projects/jdk7/;
www.oracle.com/java/technologies/compatibility.html.
- TimSort.java (jdk7): “Copyright 2009 Google Inc.” “This implementation was adapted from Tim Peters's list sort for Python, which is
  described in detail here: http://svn.python.org/projects/python/trunk/Objects/listsort.txt”.
- MIN_MERGE: “This constant should be a power of two. It was 64 in Tim Peter's C implementation, but 32 was empirically determined to work
  better in this implementation.” `private static final int MIN_MERGE = 32;`
- Constructor: “The C version always uses the same stack length (85), but this was measured to be too expensive when sorting "mid-sized"
  arrays (e.g., 100 elements) in Java.” `int stackLen = (len < 120 ? 5 : len < 1542 ? 10 : len < 119151 ? 19 : 40);`
- openjdk.org: “JDK 7 reached General Availability on 28 July 2011.”
- Oracle Compatibility, Area API Utilities: “Synopsis: Updated sort behavior for Arrays and Collections may throw an IllegalArgumentException
  … Description: The sorting algorithm used by java.util.Arrays.sort and (indirectly) by java.util.Collections.sort has been replaced. The new
  sort implementation may throw an IllegalArgumentException if it detects a Comparable that violates the Comparable contract. The previous
  implementation silently ignored such a situation. If the previous behavior is desired, you can use the new system property,
  java.util.Arrays.useLegacyMergeSort, to restore previous mergesort behavior.”

## [CAV15] S. de Gouw, J. Rot, F. S. de Boer, R. Bubel, R. Hähnle, *OpenJDK's java.utils.Collection.sort() is broken: The good, the bad and the worst case*, CAV 2015
Bản Springer (link.springer.com/chapter/10.1007/978-3-319-21690-4_16 và bản PDF) trả trang “Client Challenge” → đọc bản của tác giả ở kho
CWI: ir.cwi.nl/pub/23709/23709A.pdf (pdftotext, 48 940 ký tự).
- Abstract: “We investigate the correctness of TimSort, which is the main sorting algorithm provided by the Java standard library. … During
  our verification attempt we discovered a bug which causes the implementation to crash. … we derive a bug-free version that does not
  compromise the performance. We formally specify the new version and mechanically verify the absence of this bug with KeY”.
- §1: “It had a bug history, but was reported as fixed as of Java version 8. … we discovered that the fix to the bug mentioned above is in
  fact not working.”
- §2 mergeCollapse (Listing 3), chú thích của mã: “Examines the stack of runs waiting to be merged and merges adjacent runs until the stack
  invariants are reestablished … so the invariants are guaranteed to hold for i < stackSize upon entry to the method.”
- §3: “consider as an example the situation where runLen consists of 120, 80, 25, 20, 30 on entry of mergeCollapse, directly after 30 has
  been added by pushRun. In the first iteration … there will be a merge at 25, since 25 ≤ 20 + 30 and 25 < 30, resulting in … 120, 80, 45,
  30. In the second iteration, it is checked that the invariant is satisfied at 80 and 45 …, which is the case since 80 > 45 + 30 and 45 > 30,
  and mergeCollapse terminates. But notice that the invariant does not hold at 120, since 120 ≤ 80 + 45.”
- §3.1: dãy chặn dưới “b0 = 0, b1 = 16 and b_{i+2} = b_{i+1} + b_i + 1”; “If a.length < 120 we thus have 4 as the minimal choice of the bound,
  for a.length < 1542 it is 9, etc. This shows that the bounds used in OpenJDK … are slightly suboptimal (off by 1). The default value 40 (39
  is safe) is based on the maximum 2^31 − 1 of integers in Java.” “(in a recent update the number 19 was changed to 24, see Sect. 4)”.
- §4.1 bảng: “array size 64 128 160 65536 131072 67108864 1073741824 / required stack size 3 4 5 21 23 41 49 / runLen.length 5 10 10 19 (24)
  40 40 40”. “For the worst case of length 67108864, the declared bound 40 does not suffice … java.lang.ArrayIndexOutOfBoundsException: 40”.
- §5: “The basic idea is to check validity of the invariant on the top 4 elements of runLen …, instead of only the top 3”.
- §6: “two methods (mergeLo and mergeHi) we did not manage despite a considerable effort. Each has over 100 lines of code”. “In total, there
  are 460 lines of specifications, compared to 928 lines of code”. “over 2 million proof steps in total” (bảng: Total 2.211.263).
- §7: “Extensive testing was not able to exhibit the bug. … the smallest counterexample is an array of 67+ million elements (with
  non-primitive type) and a very complex structure.” “the affected sorting implementation was ported to Java from the Python library. It
  turns out that the bug is present in Python as well, ever since the method was introduced. It can be fixed in the same manner”. Chú thích
  11: “As the Python version works with 64bit integer types and uses larger bounds for runLen, it is even more unlikely to occur”.
  “formal specification allowed us to discover that the invariant is not preserved, in an afternoon.” “the OpenJDK implementation of sort()
  is used daily in billions of program runs”.

## [PY15] CPython: commit b808d590a2 ngày 2015-02-25; `Objects/listobject.c` bản 3.4.3 và 3.4.4; Misc/NEWS 3.4.4
GitHub API (commits?path=Objects/listobject.c, 2/2015): “fix merge_collapse to actually maintain the invariant it purports to (closes #23515)
… See de Gouw, Stijn and Rot, Jurriaan and de Boer, Frank S and Bubel, Richard and Hähnle, Reiner "OpenJDK's java.utils.Collection.sort()
is broken: The good, the bad and the worst case"”. So sánh mã: v3.4.3 chỉ xét `p[n-1].len <= p[n].len + p[n+1].len`; v3.4.4 thêm
`|| (n > 1 && p[n-2].len <= p[n-1].len + p[n].len)`. Misc/NEWS: “What's New in Python 3.4.3? Release date: 2015-02-23”; “What's New in
Python 3.4.4? Release date: 2015/12/20”.

## [JDK15] OpenJDK: JDK-8072909; TimSort.java hiện hành
- bugs.openjdk.org/rest/api/2/issue/JDK-8072909 (trang HTML 403 → đọc API JSON chính thức): “summary: TimSort fails with
  ArrayIndexOutOfBoundsException on worst case long arrays”, “created: 2015-02-06”, “resolutiondate: 2015-02-12”, fixVersions “9”
  (releaseDate 2017-09-21).
- raw.githubusercontent.com/openjdk/jdk/master/src/java.base/share/classes/java/util/TimSort.java: `len < 119151 ? 24 : 49`; “The maximum
  value of 49 allows for an array up to length Integer.MAX_VALUE-4, if array is filled by the worst case stack size increasing scenario.”;
  mergeCollapse có thêm `n > 1 && runLen[n-2] <= runLen[n] + runLen[n-1]`; chú thích “Thanks to Stijn de Gouw, … this is fixed”.

## [PS21] CPython: bpo-34561 — commit 5cb4c672d8 ngày 2021-09-06 (“Switch to Munro & Wild "powersort" merge strategy”); changelog 3.11
- docs.python.org/3.11/whatsnew/changelog.html, mục “Python 3.11.0 alpha 1, Release date: 2021-10-05”: “bpo-34561: List sorting now uses the
  merge-ordering strategy from Munro and Wild's powersort(). Unlike the former strategy, this is provably near-optimal in the entropy of the
  distribution of run lengths. Most uses of list.sort() probably won't see a significant time difference, but may see significant
  improvements in cases where the former strategy was exceptionally poor.”
- listsort.txt (main): “The original version of this code used the first thing I made up that didn't obviously suck ;-) It was loosely
  based on invariants involving the Fibonacci sequence. It worked OK, but it was hard to reason about, and was subtle enough that the
  intended invariants weren't actually preserved. Researchers discovered that when trying to complete a computer-generated correctness
  proof. … At least a dozen different approaches were developed”.
- “The "power" of the first run is a small integer, the depth of the node connecting the two runs in an ideal binary merge tree, where power
  1 is the root node”. “The power is the least integer L such that the "midpoint interval" contains a rational number of the form J/2**L.
  The midpoint interval is the semi-closed interval: ((s1 + n1/2)/n, (s2 + n2/2)/n]”. “A key invariant is that powers on the run stack are
  strictly decreasing (starting from the run at the top of the stack).” “Computing an optimal merge sequence can be done in time quadratic in
  the number of runs … and also requires finding & remembering _all_ the runs' lengths … in advance.”

## [MR25] CPython: gh-135551 — commit 2fc68e180f ngày 2025-06-27; listsort.txt (main), mục Computing minrun
- Commit: “New scheme … for picking minimum run lengths. By allowing them to change a little from one run to the next, it's possible to
  arrange for that all merges, at all levels, strongly tend to be as evenly balanced as possible, for randomly ordered data. Meaning the number
  of initial runs is a power of 2, and all merges involve runs whose lengths differ by no more than 1.”
- listsort.txt: “The original code used a cheap heuristic … but "pretty bad" cases still existed.” “with 315 random elements, the old scheme
  uses fixed minrun=40 and produces runs of length 40, except for the last. The new scheme produces a mix of lengths 39 and 40: old: 40 40 40
  40 40 40 40 35 new: 39 39 40 39 39 40 39 40” với cây trộn 78 79 79 79 / 157 158 / 315. “with 32769 elements (that's 2**15 + 1), it uses
  minrun=33 and produces 993 runs … The new scheme instead produces 1024 runs, all with length 32 except for the last one with length 33.”
  “each run would have 315/8 = 39.375 elements … we instead use 39 (the floor) and remember the current leftover fraction 0.375”. “a driver
  that exhaustively verifies the claims above for all list lengths through 2 million.”

## Điều KHÔNG dạy (nguồn không ghi hoặc không đọc được)
- Bản Springer của [CAV15]: không đọc được (Client Challenge) — đọc bản tác giả ở CWI, cùng tên, cùng nội dung hội nghị.
- Năm chính xác Java “bắt đầu dùng” TimSort: chỉ có bản quyền 2009 trong mã và ngày GA của JDK 7 → bài nói “JDK 7 phát hành 28/7/2011”.
- Có hệ thống thật nào từng sập vì lỗi này: nguồn không ghi → không dạy. [CAV15] chỉ nhắc khả năng bị dùng để tấn công từ chối dịch vụ
  (chú thích 12) — bài giảng không đi vào.
- Bản phát hành chính thức nào của ngôn ngữ gốc mang thay đổi năm 2025: commit trên nhánh main, không ghi số bản → bài chỉ nói “commit ngày
  27/6/2025”.
- Ngày phát hành bản 3.11 chính thức: không đọc trong phiên này → chỉ nêu bản thử 3.11.0a1 ngày 5/10/2021.
- “Vài tuần công”, cỡ 10 phần tử, hàng trăm dịch vụ, 8 byte mỗi phần tử trong quiz là SỐ MINH HOẠ.
