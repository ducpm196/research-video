# Nguồn đã đọc nguyên văn cho CSA L16 (bài hành trình: hết “bữa trưa miễn phí” → đa nhân → Spectre → giảm thiểu)

Đọc ngày 2026-11-02 bằng curl + trích văn bản (HTML → chữ; PDF → `pdftotext`). Chỉ trích các câu bài giảng dựa vào (CITED); mọi con số
khác trong bài là phép tính lại (VER, `checks` của bài và `audit/verify_plan_curricula.py` CSA:L16) hoặc ghi rõ “(số minh hoạ)”.
Không nêu tên cá nhân trong lời đọc; tên tác giả chỉ ở `source:` và dòng nguồn trên màn hình.
Nội dung an ninh chỉ ở mức khái niệm phòng thủ: bài KHÔNG chép đoạn mã khai thác, không nêu tốc độ rò rỉ, không nêu cách luyện sai bộ đoán.

## [HS05] H. Sutter, *The Free Lunch Is Over: A Fundamental Turn Toward Concurrency in Software*, Dr. Dobb's Journal 30(3), 3/2005
Tải: http://www.gotw.ca/publications/concurrency-ddj.htm (trang của chính tác giả; curl 200, 54 200 byte).
Ghi chú trang: “The CPU trends graph last updated August 2009 to include current data and show the trend continues as predicted. The rest of
this article including all text is still original as first posted here in December 2004.”
- Mở đầu: “The major processor manufacturers and architectures, from Intel and AMD to Sparc and PowerPC, have run out of room with most of their
  traditional approaches to boosting CPU performance. Instead of driving clock speeds and straight-line instruction throughput ever higher, they
  are instead turning en masse to hyperthreading and multicore architectures.” “multicore is … coming in 2005 from Intel and AMD.”
  “it’s not much of a stretch to call 2004 the year of multicore.”
- Bữa trưa miễn phí: “Most classes of applications have enjoyed free and regular performance gains for several decades, even without releasing
  new versions or doing anything special”. “We’re used to seeing 500MHz CPUs give way to 1GHz CPUs give way to 2GHz CPUs, and so on. Today
  we’re in the 3GHz range on mainstream computers.”
- Ba nguồn tăng tốc cũ: “Over the past 30 years, CPU designers have achieved performance gains in three main areas … clock speed, execution
  optimization, cache”. Tối ưu thực thi: “including pipelining, branch prediction, executing multiple instructions in the same clock cycle(s),
  and even reordering the instruction stream for out-of-order execution.” “even old applications have always run significantly faster—even
  without being recompiled”.
- Tối ưu có thể đổi nghĩa chương trình: “they’re under so much pressure that they’ll risk changing the meaning of your program, and possibly
  break it, in order to make it run faster.”
- Bức tường: “CPU performance growth as we have known it hit a wall two years ago.” “Around the beginning of 2003, you’ll note a disturbing
  sharp turn in the previous trend toward ever-faster CPU clock speeds.” “several physical issues, notably heat (too much of it and too hard to
  dissipate), power consumption (too high), and current leakage problems.”
- Con số: “On Intel chips, we reached 2GHz a long time ago (August 2001), and according to CPU trends before 2003, now in early 2005 we should
  have the first 10GHz Pentium-family chips.” “We’re at 3.4GHz already”. “in fall 2004 it officially abandoned its 4GHz plans entirely.”
  “Intel is planning to ramp up a little further to 3.73GHz in early 2005”.
- Moore vẫn tiếp tục: “transistor counts continue to explode”.
- Đa nhân: “Myths and Realities: 2 x 3GHz < 6 GHz”. “most multi-threaded applications won’t run twice as fast on a dual-core box.” Lý do:
  “coordination overhead between the cores to ensure cache coherency”; “unless the two cores are running different processes, or different
  threads … that are well-written to run independently and almost never wait for each other, they won’t be well utilized.” “If you’re running a
  single-threaded application, then the application can only make use of one core.”
- Siêu phân luồng: “sometimes cited as offering a 5% to 15% performance boost for reasonably well-written multi-threaded applications, or even
  as much as 40% under ideal conditions”.
- Bộ nhớ đệm: “a cache miss that goes out to main memory often costs 10 to 50 times as much getting the information from the cache”.
  “If an application’s working set fits into cache, we’re golden”. “Cache is king.”
- Hệ quả: “Intel is talking about someday producing 100-core chips; a single-threaded application can exploit at most 1/100 of such a chip’s
  potential throughput.” “‘Oh, performance doesn’t matter so much, computers just keep getting faster’ has always been a naïve statement …
  and for the near future it will almost always be simply wrong.” “3. Efficiency and performance optimization will get more, not less,
  important.”
- Song song có điều kiện: “not all problems are inherently parallelizable and because concurrent programming is hard.” Ví dụ đứa bé: “It is
  indeed an inherently nonparallel problem if the goal is to produce one child. It is actually an ideally parallelizable problem if the goal is
  to produce many children! Knowing the real goals can make all the difference.”
- Kiểm thử: “latent concurrency bugs that surface only on true multiprocessor systems … many teams whose application worked fine even under
  heavy and extended stress testing … until the day that a customer actually had a real multiprocessor machine”.

## [KO19] P. Kocher và cộng sự (12 tác giả), *Spectre Attacks: Exploiting Speculative Execution*, IEEE S&P 2019 (DOI 10.1109/SP.2019.00002)
Tải: https://spectreattack.com/spectre.pdf (trang chính thức của nhóm tác giả; curl 200, 301 067 byte; PDF tạo 2018-06-01, đúng danh sách
12 tác giả của bản hội nghị). Đối chiếu: arXiv:1801.01203v1 (3/1/2018, 10 tác giả, curl 200). doi.org chuyển tới ieeexplore.ieee.org
document 8835233 — trang IEEE KHÔNG đọc toàn văn; mọi câu dưới đây lấy từ bản tác giả tại spectreattack.com (khớp từng câu nào với bản in IEEE:
NOT_VERIFIED).
- Abstract: “Modern processors use branch prediction and speculative execution to maximize performance.” “When the memory value finally arrives,
  the CPU either discards or commits the speculative computation.” “vulnerable speculative execution capabilities are found in microprocessors
  from Intel, AMD, and ARM that are used in billions of devices.” “sound solutions will require fixes to processor designs as well as updates to
  instruction set architectures (ISAs)”.
- §I: “As this memory is much slower than the CPU, it often takes several hundred clock cycles before the value becomes known. Rather than
  wasting these cycles by idling, the CPU attempts to guess the direction of control flow, saves a checkpoint of its register state, and proceeds
  to speculatively execute the program on the guessed path.” “If the guess was wrong, the CPU discards the incorrect speculative execution by
  reverting the register state back to the stored checkpoint, resulting in performance comparable to idling. However, if the guess was correct,
  the speculative execution results are committed, yielding a significant performance gain”.
- §I: “because CPUs are designed to maintain functional correctness by reverting the results of incorrect speculative executions to their prior
  states, these errors were previously assumed to be safe.”
- §I-B (Variant 1, mức khái niệm): “the CPU discovers its error and reverts any changes made to its nominal microarchitectural state. However,
  changes made to the cache state are not reverted”.
- §I-C: “The Spectre family of attacks is documented under CVE-2017-5753 and CVE-2017-5715.”
- §II-B: “Speculative execution on modern CPUs can run several hundred instructions ahead. The limit is typically governed by the size of the
  reorder buffer in the CPU. For instance, on the Haswell microarchitecture, the reorder buffer has sufficient space for 192 micro-ops”.
- §IV (thí nghiệm): “On a Haswell i7-4650U, the code … works with up to 188 simple instructions inserted … between the ‘if’ statement and the
  line accessing array1/array2, which is just below the 192 micro-ops that fit in the reorder buffer of this processor”.
- §VII-A: “preventing speculative execution would cause a significant degradation in the performance of the processor.” “The safest (but
  slowest) approach to protect conditional branches would be to add such an instruction [lfence] on the two outcomes of every conditional
  branch. However, this amounts to disabling branch prediction and our tests indicate that this would dramatically reduce performance”.
  “An improved approach is to use static analysis … to reduce the number of speculation blocking instructions required”. “for protection,
  updated software binaries and libraries are required. This could be an issue for legacy software.”
- §VII-B: “used by the Google Chrome web browser, is to execute each web site in a separate process”.
- §VII-D: “major browser providers have further degraded the resolution of the JavaScript timer”; “it does not guarantee that attacks are not
  possible.”
- §VII-E (IBRS, STIBP, IBPB): “The performance impact varies from a few percent to a factor of 4 or more, depending on which countermeasures are
  employed, how comprehensively they are applied … and the efficiency of the hardware and microcode implementations.” “Google suggests an
  alternative mechanism … called retpolines”.
- §VIII: “A fundamental assumption underpinning software security techniques is that the processor will faithfully execute program
  instructions, including its safety checks.” “they are only stop-gap measures”. “there are trade-offs between security and performance. The
  vulnerabilities … arise from a long-standing focus in the technology industry on maximizing performance.”

## [LK] The Linux Kernel documentation, *Spectre Side Channels* (admin-guide/hw-vuln/spectre)
Tải: https://docs.kernel.org/admin-guide/hw-vuln/spectre.html (curl 200, 51 905 byte; trang ghi bản tài liệu 7.4.0-rc1; trang không ghi ngày
viết từng đoạn — năm 2019 trong bài lấy từ mã CVE-2019-1125 được liệt kê trên trang).
- “Spectre is a class of side channel attacks that exploit branch prediction and speculative execution on modern CPUs to read memory, possibly
  bypassing access controls.” “most modern high speed processors use branch prediction and speculative execution.”
- Danh sách CPU bị ảnh hưởng gồm “Intel Core, Atom, Pentium, and Xeon processors; AMD Phenom, EPYC, and Zen processors; IBM POWER and zSeries
  processors; Higher end ARM processors; Apple CPUs; Higher end MIPS CPUs; Likely most other high performance CPUs.”
- Related CVEs: “CVE-2017-5753 Bounds check bypass Spectre variant 1; CVE-2017-5715 Branch target injection Spectre variant 2; CVE-2019-1125
  Spectre v1 swapgs”. Mục BHB: “Further research has found attacks that don’t require unprivileged eBPF.”
- “The Linux kernel provides a sysfs interface to enumerate the current mitigation status of the system for Spectre: whether the system is
  vulnerable, and which mitigations are active.” Tệp: “/sys/devices/system/cpu/vulnerabilities/spectre_v1”, “…/spectre_v2”; giá trị
  ví dụ “‘Not affected’”, “‘Mitigation: None’ Vulnerable, no mitigation”, “‘Mitigation: Retpolines’”, “‘Mitigation: Enhanced IBRS’”.
- “The retpoline mitigation is turned on by default on vulnerable CPUs.” “The above mitigations are turned on by default on vulnerable CPUs.”
  “In general the kernel selects reasonable default mitigations for the current CPU.”
- “Enhanced IBRS is more efficient than retpoline.” “Programs that disable their indirect branch speculation will have more overhead and run
  slower.”
- Mitigation selection guide: “1. Trusted userspace — If all userspace applications are from trusted sources and do not execute externally
  supplied untrusted code, then the mitigations can be disabled.” “2. Protect sensitive programs — For security-sensitive programs that have
  secrets (e.g. crypto keys), protection … can be put in place by disabling indirect branch speculation when the program is running”.
  “3. Sandbox untrusted programs — Untrusted programs that could be a source of attacks can be cordoned off”. “High security mode — All
  Spectre variant 2 mitigations can be forced on at boot time for all programs … This will add overhead”.

## Điều KHÔNG dạy (nguồn không ghi, hoặc ngoài phạm vi phòng thủ)
- Mã khai thác, cách luyện sai bộ đoán rẽ nhánh, tốc độ đọc trộm (KB/s) của [KO19]: không dạy (luật an ninh — chỉ khái niệm phòng thủ).
- Mức giảm hiệu năng cụ thể của từng biện pháp trên một máy cụ thể: [KO19] chỉ ghi khoảng “a few percent to a factor of 4 or more”; [LK] chỉ
  ghi “add overhead / run slower”. Mọi phần trăm khác trong bài (10% ở câu đố) là SỐ MINH HOẠ.
- Lý do vật lý định lượng của bức tường xung nhịp (công suất theo tần số, định luật Dennard): [HS05] chỉ kể “heat, power consumption, current
  leakage” → bài không đưa công thức công suất.
- Số lõi của chip Intel/AMD năm 2005: [HS05] chỉ ghi “dual-core” và “2005”; không dạy số lõi của các năm sau.
- “Dark silicon”, bài giảng Turing 2018 (Hennessy & Patterson): không đọc trong phiên này → không dạy.
- Meltdown: [KO19] mục I-D phân biệt với Spectre; bài chỉ dạy Spectre.
- Số 200 chu kỳ (“several hundred clock cycles”), 4 vi lệnh mỗi chu kỳ, đoán đúng 95%, chương trình 60 giây, tỉ lệ song song 80% / 20%:
  SỐ MINH HOẠ, ghi rõ trên màn hình.

## Đọc lại đợt C (2026-11-09, curl lại cùng hai URL: gotw.ca 54 200 byte, docs.kernel.org 51 905 byte — cùng cỡ với lần đọc 2026-11-02)
- [HS05]: “Intel is planning to ramp up a little further to 3.73GHz in early 2005 … but the clock race really is over, at least for now”
  → 3,73 GHz là KẾ HOẠCH, không phải “thực tế”: hook bài sửa thành “kế hoạch cho đầu 2005 chỉ là 3,73 GHz”; câu trích trên màn hình
  thêm “ít nhất là lúc này”.
- [HS05]: “The initial Intel and AMD designs, both due in 2005” → bài sửa “Intel và AMD ra chip hai lõi năm 2005” thành “hẹn ra trong năm 2005”.
- [HS05]: “although a hyper-threaded CPU has some extra hardware including extra registers, it still has just one cache, one integer math unit,
  one FPU” → khớp ô “vẫn chung một bộ nhớ đệm, một bộ tính số thực”.
- [LK]: “vulnerable kernel code … is annotated on a case by case basis to use nospec accessor macros for bounds clipping” → khớp “nhân hệ
  điều hành cắt chỉ số về trong biên”. “individual user programs can be compiled with return trampolines for indirect branches. This protects
  them from consuming poisoned entries in the branch target buffer” → khớp ghi chú mới về bàn nhún trả về / nhánh gián tiếp.
- Định nghĩa “vi lệnh”, “bộ đệm sắp xếp lại”, “vi mã”, “luồng” thêm ở đợt C là định nghĩa sách giáo khoa (Patterson & Hennessy, Computer
  Organization and Design, chương 4 về thực thi động và vi lệnh), không phải câu trích nguồn.
