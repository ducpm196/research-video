# Nguồn đã đọc nguyên văn cho PLC L13 (bài hành trình: chuyển sang ngôn ngữ an toàn bộ nhớ, 2019 → 2025)

Đọc ngày 2026-11-02 (curl + trích văn bản bằng script; trang Blogger lấy phần thân trong `<script type='text/template'>`). Chỉ trích
các câu bài giảng dựa vào (CITED); mọi con số khác trong bài là phép tính lại (VER, `checks` của bài và `audit/plc/verify_plc.py` L13)
hoặc ghi rõ “(số minh hoạ)”. Không nêu tên cá nhân trong lời đọc; tên tác giả chỉ ở `source:`. Nội dung an ninh chỉ ở mức khái niệm
phòng thủ: loại lỗi, tỉ lệ, cách phòng — không có mã hay chuỗi khai thác.

Ứng viên ROADMAP §8.1 mục 3: “MSRC 2019; blog bảo mật Google 2022 (Android)”. Đã đọc cả hai, cộng thêm các bài chính thức cùng đội viết
trước và sau đó (2019 Chromium, 2019 và 2021 Android, 2024, 2025) để đủ năm chặng theo quy mô.

## [MS19] MSRC Blog, *A proactive approach to more secure code*, 2019-07-16 (By MSRC Team)
URL: https://msrc.microsoft.com/blog/2019/07/a-proactive-approach-to-more-secure-code/ → chuyển hướng 301 tới
https://www.microsoft.com/en-us/msrc/blog/2019/07/a-proactive-approach-to-more-secure-code (curl, đọc được).
- “Since 2004, the Microsoft Security Response Centre (MSRC) has triaged every reported Microsoft security vulnerability.”
- “the majority of vulnerabilities fixed and with a CVE assigned are caused by developers inadvertently inserting memory corruption bugs into
  their C and C++ code. As Microsoft increases its code base and uses more Open Source Software in its code, this problem isn’t getting
  better, it’s getting worse.”
- Hình 1: “~70% of the vulnerabilities Microsoft assigns a CVE each year continue to be memory safety issues”
- “The developer has a plethora of tools at their disposal: amazingly complex static analysis tools …, fuzzing at scale …, taint analysis,
  and constraint solvers. There is guidance … the Secure Development Lifecycle …, hours of code review, plenty of training”.
- “A language considered safe from memory corruption vulnerabilities removes the onus of software security from the feature developer and
  puts it on the language developer.” “… several languages available that are regarded as “safe” from memory corruption vulnerabilities,
  such as C#.”
- “Rather than providing guidance and tools for addressing flaws, we should strive to prevent the developer from introducing the flaws in
  the first place.”

## [MS19b] MSRC Blog, *We need a safer systems programming language*, 2019-07-18 (By MSRC Team)
URL: https://www.microsoft.com/en-us/msrc/blog/2019/07/we-need-a-safer-systems-programming-language (curl, đọc được).
- “memory safety issues have represented almost the same proportion of vulnerabilities assigned a CVE for over a decade.”
- “Memory safety is a property of programming languages where all memory access is well defined. Most programming languages in use today
  are memory-safe because they use some form of garbage collection.”
- “the root cause of approximately 70% of security vulnerabilities that Microsoft fixes and assigns a CVE … are due to memory safety issues.
  This is despite mitigations including intense code review, training, static analysis, and more.”
- “it is near impossible to write memory-safe code using traditional systems-level programming languages at scale.”
- “Spatial memory safety refers to ensuring that all memory accesses are within bounds of the type that is being accessed.”
- “Temporal memory safety refers to ensuring that pointers still point to valid memory at the time of dereference.”
- “A data race occurs when two or more threads in a single process concurrently access the same memory location, at least one of the
  accesses is for writing, and the threads are not using any exclusive locks”.

## [BH19] M. Miller, *Trends, challenges, and strategic shifts in the software vulnerability mitigation landscape*, BlueHat IL, 2/2019
URL: https://github.com/microsoft/MSRC-Security-Research/raw/master/presentations/2019_02_BlueHatIL/2019_01%20-%20BlueHatIL%20-%20Trends%2C%20challenge%2C%20and%20shifts%20in%20software%20vulnerability%20mitigation.pdf
(PDF 32 trang, pdftotext; liên kết lấy từ [CR19]).
- Biểu đồ “% of memory safety vs. non-memory safety CVEs by patch year”, trục năm 2006 … 2018; chú thích: “~70% of the vulnerabilities
  addressed through a security update each year continue to be memory safety issues”.
- Số từng năm trên biểu đồ KHÔNG trích được dạng văn bản → bài chỉ nói “khoảng 70% mỗi năm, từ 2006 tới 2018”.

## [CR19] Chromium, *The Rule Of 2* (docs/security/rule-of-2.md)
URL: https://chromium.googlesource.com/chromium/src/+/main/docs/security/rule-of-2.md (`?format=TEXT`, đọc được; bản hiện hành, câu số
liệu ghi mốc “As of March 2019”).
- “The Rule Of 2 is: Pick no more than 2 of — untrustworthy inputs; unsafe implementation language; and high privilege.”
- “When code that handles untrustworthy inputs at high privilege has bugs, the resulting vulnerabilities are typically of Critical or High
  severity.”
- “(As of March 2019, only about 5 of 130 public Critical-severity bugs are not obviously due to memory corruption.)”

## [AQ19] Google Security Blog, *Queue the Hardening Enhancements*, 2019-05-09 (Android Q)
URL: https://security.googleblog.com/2019/05/queue-hardening-enhancements.html (curl, đọc được).
- “Use-after-free (UAF), integer overflows, and out of bounds (OOB) reads/writes comprise 90% of vulnerabilities with OOB being the most
  common.”
- “In Android Q, we moved software codecs out of the main mediacodec service into a constrained sandbox.” “In 2018, approximately 80% of the
  critical/high severity vulnerabilities in media components occurred in software codecs”.
- “Incorrect or missing memory bounds checking on arrays account for about 34% of Android’s userspace vulnerabilities.”
- “By optimizing away a number of unnecessary checks the performance overhead was reduced to less than 1%.” (BoundSan)

## [AR21] Google Security Blog, *Rust in the Android platform*, 2021-04-06
URL: https://security.googleblog.com/2021/04/rust-in-android-platform.html (curl, đọc được).
- “memory safety bugs continue to be a top contributor of stability issues, and consistently represent ~70% of Android’s high severity
  security vulnerabilities.”
- “Memory-safe languages are the most cost-effective means for preventing memory bugs.”
- “Rust provides memory safety guarantees by using a combination of compile-time checks to enforce object lifetime/ownership and runtime
  checks to ensure that memory accesses are valid.”
- “if code is written in C/C++ and parses untrustworthy input, it should be contained within a tightly constrained and unprivileged sandbox.”
  “Sandboxing is expensive: the new processes it requires consume additional overhead and introduce latency due to IPC and additional memory
  usage. Sandboxing doesn’t eliminate vulnerabilities from the code”.
- “rewriting tens of millions of lines of code is simply not feasible.”
- “Most of our memory bugs occur in new or recently modified code, with about 50% being less than a year old.”
- “References and variables are immutable by default”. “Data concurrency - prevents data races.”
- “For the past 18 months we have been adding Rust support to the Android Open Source Project”.

## [AN22] Google Security Blog, *Memory Safe Languages in Android 13*, 2022-12-01
URL: https://security.googleblog.com/2022/12/memory-safe-languages-in-android-13.html (curl, đọc được).
- “For more than a decade, memory safety vulnerabilities have consistently represented more than 65% of vulnerabilities across products”.
- “From 2019 to 2022 the annual number of memory safety vulnerabilities dropped from 223 down to 85.”
- “Android 13 is the first Android release where a majority of new code added to the release is in a memory safe language.”
- “From 2019 to 2022 it has dropped from 76% down to 35% of Android’s total vulnerabilities.”
- “While correlation doesn’t necessarily mean causation … Of course there may be other contributing factors or alternative explanations.”
- “our goal is not to convert existing C/C++ to Rust, but rather to shift development of new code to memory safe languages over time.”
- “In Android 13, about 21% of all new native code (C/C++/Rust) is in Rust. There are approximately 1.5 million total lines of Rust code in
  AOSP”.
- “To date, there have been zero memory safety vulnerabilities discovered in Android’s Rust code.”
- “Historical vulnerability density is greater than 1/kLOC (1 vulnerability per thousand lines of code) in many of Android’s C/C++
  components … it’s likely that using Rust has already prevented hundreds of vulnerabilities from reaching production.”
- “There are exactly two uses of unsafe in the UWB code”.
- “The number of vulnerabilities reported in the bulletin has stayed somewhat steady over the past 4 years at around 20 per month”.
- “In 2022, despite only representing 36% of vulnerabilities in the security bulletin, memory-safety vulnerabilities accounted for 86% of our
  critical severity security vulnerabilities … and 89% of our remotely exploitable vulnerabilities.”
  (Ghi chú: cùng bài ghi 35% ở đoạn trên và 36% ở đoạn này — bài giảng dùng 35% cho tỉ lệ năm, không dùng 36%.)
- “We continue to invest in tools to improve the safety of our C/C++ … Scudo hardened allocator, HWASAN, GWP-ASAN, and KFENCE”.

## [AN24] Google Security Blog, *Eliminating Memory Safety Vulnerabilities at the Source*, 2024-09-25
URL: https://security.googleblog.com/2024/09/eliminating-memory-safety-vulnerabilities-Android.html (curl, đọc được).
- “the percentage of memory safety vulnerabilities in Android dropped from 76% to 24% over 6 years as development shifted to memory safe
  languages.”
- “vulnerabilities decay exponentially. They have a half-life. The distribution of vulnerability lifetime follows an exponential
  distribution given an average vulnerability lifetime λ”.
- “5-year-old code has a 3.4x (using lifetimes from the study) to 7.4x (using lifetimes observed in Android and Chromium) lower vulnerability
  density than new code.”
- Chú thích 1: “The code base doubles every 6 years. The average lifetime for vulnerabilities is 2.5 years. It takes 10 years to transition
  to memory safe languages for new code”.
- “The Android team began prioritizing transitioning new development to memory safe languages around 2019.”
- Chú thích 3: “in the slight increase in 2023. … while the percentage of memory safety vulnerabilities continued to drop, the absolute
  number increased slightly.”
- Bốn thế hệ: “1st generation: reactive patching.” “2nd generation: proactive mitigating.” “3rd generation: proactive vulnerability
  discovery.” “The fourth generation: high-assurance prevention”.
- “The Android team has observed that the rollback rate of Rust changes is less than half that of C++.”
- “Interoperability is the new rewrite”; “we do not need to throw away or rewrite all our existing memory-unsafe code.”
- “after removing the now unnecessary sandbox, Chromium's Rust QR code generator is 20 times faster.”

## [AN25] Google, *Rust in Android: move fast and fix things*, 2025-11-13
URL: https://security.googleblog.com/2025/11/rust-in-android-move-fast-fix-things.html (đường dẫn SUY RA theo mẫu của blog; máy chủ
chuyển hướng 301 tới https://blog.google/security/rust-in-android-move-fast-fix-things/ — curl, đọc được).
- “memory safety vulnerabilities falling below 20% of total vulnerabilities for the first time.”
- “we are seeing a 1000x reduction in memory safety vulnerability density compared to Android’s C and C++ code.”
- “With Rust changes having a 4x lower rollback rate and spending 25% less time in code review”; “For medium and large changes, the rollback
  rate of Rust changes in Android is ~4x lower than C++.” “Rust changes of a similar size need about 20% fewer revisions”.
- “We recently avoided shipping our very first Rust-based memory safety vulnerability: a linear buffer overflow in CrabbyAVIF.”
  “Android’s Scudo hardened allocator deterministically rendered this vulnerability non-exploitable due to guard pages”.
- “With roughly 5 million lines of Rust in the Android platform and one potential memory safety vulnerability found (and fixed pre-release),
  our estimated vulnerability density for Rust is 0.2 vuln per 1 million lines (MLOC).”
- “Our historical data for C and C++ shows a density of closer to 1,000 memory safety vulnerabilities per MLOC.”
- “the approximately 4% of code written within unsafe{} blocks.” “simply banning unsafe code is not workable.”
- “Android’s 6.12 Linux kernel is our first kernel with Rust support enabled and our first production Rust driver.”
- “we are adding a new deep dive on unsafe code to our Comprehensive Rust training.”

## Điều KHÔNG dạy (nguồn không ghi hoặc không đọc được)
- Số phần trăm từng năm 2006–2018 của Microsoft: chỉ có trên biểu đồ ảnh [BH19] → chỉ nói “khoảng 70% mỗi năm”.
- Ba lựa chọn của “Rule of 2” trong [AR21] nằm trong ảnh; bài lấy nguyên văn từ [CR19].
- Quan hệ nhân quả: [AN22] tự ghi “correlation doesn’t necessarily mean causation” → bài nói “trùng với”, không nói “vì thế mà”.
- Số lỗ hổng tuyệt đối năm 2024, 2025 của Android: [AN24] ghi 2024 ngoại suy 36 (đang là 27); [AN25] không ghi số tuyệt đối → bài không
  dạy số tuyệt đối 2025, chỉ “dưới 20%”.
- Chi tiết cơ chế lỗi CrabbyAVIF, cách khai thác: không dạy (chỉ “tràn bộ đệm tuyến tính, trang canh làm nó không khai thác được”).
- Microsoft đã chuyển bao nhiêu mã sang ngôn ngữ an toàn sau 2019: hai bài MSRC không ghi số → không dạy.
- “Hàng trăm lỗ hổng đã được ngăn” [AN22] là ước lượng của nguồn; phép nhân 1,5 triệu dòng × 1 lỗ hổng mỗi nghìn dòng = 1500 trong bài
  chỉ là CẬN TRÊN theo mật độ lịch sử (không phải mọi dòng là mã gốc mới thay cho C/C++), ghi rõ trên màn hình.
- NSA/CISA (2022, 2023): không đọc trong phiên này, không dạy (chỉ [AN24] trích một câu của báo cáo CISA — không dùng).
