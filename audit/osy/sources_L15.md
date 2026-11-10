# Nguồn đã đọc nguyên văn cho OSY L15 (bài hành trình: bộ lập lịch CPU của Linux, 2002 → 2024)

Đọc ngày 2026-11-02 bằng curl + trích văn bản (mọi trang trả 200, không trang nào bị chặn). Chỉ trích các câu bài giảng dựa vào (CITED);
mọi con số khác trong bài là phép tính lại (VER: `checks` của bài, `tools/checklib.py` cfs_run / cfs_groups / eevdf_run,
`audit/verify_plan_curricula.py` OSY:L15) hoặc ghi rõ “(số minh hoạ)”. Không nêu tên cá nhân trong lời đọc; tên tác giả chỉ ở `source:`.

Hành trình theo ROADMAP §8.1 mục 3 (O(1) → CFS 2007 → EEVDF 2023), thêm hai chặng có nguồn chính thức: lập lịch theo nhóm 2.6.24 (2008)
và lớp lập lịch mở rộng sched_ext 6.12 (2024).

## [O102] Goals, Design and Implementation of the new ultra-scalable O(1) scheduler — Documentation/sched-design.txt trong nhân Linux
Tải: raw.githubusercontent.com/torvalds/linux/v2.6.12/Documentation/sched-design.txt (7 912 byte; bản v2.6.22 cùng nội dung, 7 916 byte).
Tệp ghi: “This is an edited version of an email Ingo Molnar sent to lkml on 4 Jan 2002. … Last Updated: 18 April 2002.”
- Goal: “fully O(1) scheduling. Are you tired of the recalculation loop blowing the L1 cache away every now and then? Do you think the
  goodness loop is taking a bit too long to finish if there are lots of runnable processes? … wakeup(), schedule(), the timer interrupt are
  all O(1) algorithms. There is no recalculation loop. There is no goodness loop either.”
- “'perfect' SMP scalability. With the new scheduler there is no 'big' runqueue_lock anymore - it's all per-CPU runqueues and locks - two
  tasks on two separate CPUs can wake up, schedule and context-switch completely in parallel, without any interlocking.”
- “The reason is that the timeslice recalculation loop first needs every currently running task to consume its timeslice. But when this
  happens on eg. an 8-way system, then this property starves an increasing number of CPUs from executing any process. … The more CPUs, the
  worse this effect.” “The new scheduler solves this problem by distributing timeslices on a per-CPU basis, without having any global
  synchronization or recalculation.”
- “O(1) RT scheduling. For those RT folks who are paranoid about the O(nr_running) property of the goodness loop and the recalculation loop.”
- Design: “*two*, priority-ordered 'priority arrays' per CPU. There is an 'active' array and an 'expired' array. … If all active tasks are
  used up then we 'switch' the two pointers”. “there is a 64-bit bitmap cache for array indices. Finding the highest priority task is thus a
  matter of two x86 BSFL bit-search instructions.”
- “there is a per-task 'load estimator'. … the best interactive feel is achieved not by 'boosting' interactive tasks, but by 'punishing'
  tasks that want to use more CPU time than there is available.” “there is a 4-entry 'history' ringbuffer of the task's activities during
  the last 4 seconds. … [the size '4' and the interval of 4x 1 seconds was found by lots of experimentation …]”

## [KN23] Kernel Newbies, Linux 2.6.23 (kernelnewbies.org/Linux_2_6_23, 203 702 byte)
- “Linux kernel version 2.6.23 Released 9 October 2007”.
- §2.1: “During the development of Linux 2.5, the 'O(1)' process scheduler (PS) … was merged to replace the one inherited from 2.4. The O(1)
  PS was designed to fix the scalability issues in the 2.4 PS - the performance improvements were so big that the O(1) PS was one of the
  most frequently backported features to 2.4 in commercial Linux distributions.”
- “if a process - or more than one - starts an endless loop and due to those CPU-bound loopers and the PS doesn't assign as much CPU as
  necessary to the already present non-looping processes in charge of implementing the user interfaces … Or worse, in the case of music
  players your music could skip.” “many users reported corner cases and not-so-corner cases where the new PS didn't work as expected.”
- “the 'interactivity estimator' - a piece of code used by the PS to try to decide which processes were more 'interactive' … caused more
  problems than it solved. … It was the typical case of an algorithm using statistics to try to predict the future with heuristics, and
  failing at it.”
- “CFS includes the sleep time in the task's fairness metric … This design gets the best of both worlds: fairness and interactivity, but
  without resorting to an interactivity estimator.” “instead of runqueues, it uses a time-ordered rbtree … It also uses nanosecond
  granularity accounting”.
- “CFS is a quite radical rewrite of the Linux PS (~70% of its code is touched) … RSDL patchset weighted 88K, whereas CFS patcheset weights
  290k”. “CFS is also available as a backport for 2.6.22, 2.6.21 and 2.6.20.”

## [CFS] CFS Scheduler — docs.kernel.org/scheduler/sched-design-CFS.html (bản tài liệu 7.4.0-rc1)
- “CFS stands for “Completely Fair Scheduler,” … merged in Linux 2.6.23. … Nowadays, CFS is making room for EEVDF”.
- “80% of CFS’s design can be summed up in a single sentence: CFS basically models an “ideal, precise multi-tasking CPU” on real hardware.”
  “each at 1/nr_running speed. For example: if there are 2 tasks running, then it runs each at 50% physical power”.
- “the virtual runtime of a task is its actual runtime normalized to the total number of running tasks.” “it always tries to run the task
  with the smallest p->se.vruntime value (i.e., the task which executed least so far).”
- §3: “it uses a time-ordered rbtree to build a “timeline” of future task execution, and thus has no “array switch” artifacts”. “CFS picks
  the “leftmost” task from this tree … slowly but surely giving a chance for every task to become the “leftmost task” and thus get on the CPU
  within a deterministic amount of time.”
- §4: “CFS uses nanosecond granularity accounting and does not rely on any jiffies or other HZ detail. … has no heuristics whatsoever. There
  is only one central tunable: /sys/kernel/debug/sched/base_slice_ns”.
- §6: “sched/rt.c … uses 100 runqueues (for all 100 RT priority levels, instead of 140 in the previous scheduler)”. “Scheduling Classes,” an
  extensible hierarchy of scheduler modules.”
- §7: “it may be desirable to first provide fair CPU time to each user on the system and then to each task belonging to a user.”
  Ví dụ: “#Configure the multimedia group to receive twice the CPU bandwidth that of browser group / echo 2048 > multimedia/cpu.shares /
  echo 1024 > browser/cpu.shares”.

## [KN24] Kernel Newbies, Linux 2.6.24 (kernelnewbies.org/Linux_2_6_24)
- “Linux kernel version 2.6.24 Released 24 January 2008”. “2.6.24 includes CPU "group scheduling"”.
- §2.1: “2.6.23's CFS context switching is more than 10% slower than the old task scheduler. With the optimization done in 2.6.24, CFS is now
  even a bit faster than the old task scheduler”.
- “given two users, one running one cpu-bound process and the other two cpu-bound processes, you may want to give 50% of CPU time to the
  first users and his task, and 50% to the other user, which will be shared between his two processes - 25% of CPU time for each.”
- “lets the administrator create arbitrary groups of tasks (ie: "multimedia", "compiling"), set how much CPU time 'priority' you want to
  give that group … The CFS group scheduling feature uses cgroups to control the CPU time that every cgroup can get.”

## [LWN23] LWN.net, “An EEVDF CPU scheduler for Linux”, 9/3/2023 (lwn.net/Articles/925371/, đọc được toàn văn)
- “CFS was merged for the 2.6.23 release in 2007 and has, with numerous ongoing tweaks, handled the job reasonably well ever since. … The
  EEVDF scheduler … offers the possibility of improving on CFS while reducing its dependence on often-fragile heuristics.”
- “Some processes may not need a lot of CPU time but, when they do need that time, they need it quickly. … CFS does not give processes a
  way to express their latency requirements; nice values (priorities) can be used to give a process more CPU time, but that is not the same
  thing.” “running in a realtime class is a privileged operation”.
- “it was described in this 1995 paper by Ion Stoica and Hussein Abdel-Wahab.”
- “If, for example, there are five processes trying to run on a single CPU, each of those processes should get 20% of the available time.”
  “Imagine a time period of one second; … each process should have gotten 200ms of CPU time.”
- “that difference is called "lag". A process with a positive lag value has not received its fair share”. “a process is deemed to be
  "eligible" if — and only if — its calculated lag is greater than or equal to zero”.
- “This deadline is calculated by adding a process's allocated time slice to its eligible time. A process with a 10ms time slice, and whose
  eligible time is 20ms in the future, will have a virtual deadline that is 30ms in the future.”
- “a process with a lower latency-nice setting … will get a shorter time slice. … the amount of CPU time given to any two processes (with
  the same nice value) will be the same, but the low-latency process will get it in a larger number of shorter slices.”
- “the current patches implement EEVDF as an option alongside CFS, which will enable wider testing without actually replacing the current
  scheduler. The CPU scheduler has to do the right thing for almost any conceivable workload on the wide range of systems supported by the
  kernel”.

## [KN66] Kernel Newbies, Linux 6.6 (kernelnewbies.org/Linux_6.6)
- “Linux 6.6 has been released on Sunday, 29 Oct 2023. Summary: This release replaces the CFS process scheduler with a new one called EEVDF,
  which should provide better latency in general”.
- §1.1: “CFS used heuristics and tunable knobs to attempt to guess which processes needed more attention. Many of these tunables have been
  removed.”

## [EEV] EEVDF Scheduler — docs.kernel.org/scheduler/sched-eevdf.html
- “Similarly to CFS, EEVDF aims to distribute CPU time equally among all runnable tasks with the same priority. … a task with a positive lag
  is owed CPU time, while a negative lag means the task has exceeded its portion. EEVDF picks tasks with lag greater or equal to zero and
  calculates a virtual deadline (VD) for each, selecting the task with the earliest VD to execute next. … this allows latency-sensitive
  tasks with shorter time slices to be prioritized”.
- “This prevents tasks from exploiting the system by sleeping briefly to reset their negative lag”. “tasks can request specific time slices
  using the new sched_setattr() system call”.
- Ghi chú: trang ghi “began transitioning to EEVDF in version 6.6 (as a new option in 2024)” — câu này mơ hồ (6.6 ra 29/10/2023 theo [KN66]);
  bài chỉ dạy “6.6 năm 2023 thay CFS, 6.12 năm 2024 hoàn tất chuyển đổi” theo [KN66] và [KN612].

## [KN612] Kernel Newbies, Linux 6.12 (kernelnewbies.org/Linux_6.12)
- “Linux 6.12 was released on Sunday, 17 Nov 2024 . Summary: … complete support for the EEVDF task scheduler; the ability to write task
  scheduling algorithms using BPF”.
- §1.2: “This replacement has been gradual. This release completes the EEVDF transition”.
- §1.3: “experimentation or even personalization can provide great improvements. This release includes the first pieces of sched_ext, a
  feature that enables to write task scheduler algorithms in BPF, which provides a much faster development iteration”.

## [SCX] Extensible Scheduler Class — docs.kernel.org/scheduler/sched-ext.html
- “sched_ext is a scheduler class whose behavior can be defined by a set of BPF programs - the BPF scheduler.”
- “The BPF scheduler can be turned on and off dynamically anytime. The system integrity is maintained no matter what the BPF scheduler does.
  The default scheduling behavior is restored anytime an error is detected, a runnable task stalls, or on invoking the SysRq key sequence”.
- “when the BPF scheduler is loaded and SCX_OPS_SWITCH_PARTIAL is set in ops->flags, only tasks with the SCHED_EXT policy are scheduled by
  sched_ext”.
- “ABI Instability … no stability guarantees … subject to change without warning between kernel versions.”

- [RTG] The Linux Kernel documentation, Real-Time group scheduling (Documentation/scheduler/sched-rt-group.rst): mặc định
  sched_rt_period_us = 1000000, sched_rt_runtime_us = 950000 → tác vụ thời gian thực dùng tối đa 0,95 s mỗi giây, chừa 0,05 s (5%) cho
  tác vụ thường. Dùng cho câu “vòng lặp lỗi chiếm gần hết CPU” ở phần quyết định (rà 2026-11-08; trước đó bài nói “chiếm hết”).

## Đọc kiểm lần ba (2026-11-09, WebFetch, truy cập 2026-11-09, no revision given trừ khi ghi)
Mở lại và khớp: [O102] (v2.6.12 sched-design.txt: thư 4/1/2002, “64-bit bitmap cache”, “4-entry 'history' ringbuffer”, KHÔNG có số 140),
[KN23] (9/10/2007, “~70% of its code is touched”, câu “predict the future with heuristics”, nhạc bị vấp), [CFS] (“merged in Linux 2.6.23”,
“no heuristics whatsoever”, “only one central tunable”, “instead of 140 in the previous scheduler”, ví dụ 2048/1024), [KN24] (24/1/2008,
“more than 10% slower”, ví dụ 50%/25%, nhóm “multimedia”, “compiling”), [LWN23] (J. Corbet, 9/3/2023; bài báo 1995 Stoica & Abdel-Wahab;
ví dụ 10 + 20 = 30 ms; “option alongside CFS”), [KN66] (29/10/2023; thay CFS; “Many of these tunables have been removed”), [KN612]
(17/11/2024; “completes the EEVDF transition”; “first pieces of sched_ext”), [SCX] (bật/tắt bất cứ lúc nào; quay về mặc định khi lỗi,
tác vụ treo, SysRq; SCX_OPS_SWITCH_PARTIAL; API “no stability guarantees”), [RTG] (docs.kernel.org/scheduler/sched-rt-group.html:
1000000 / 950000 µs, “0.05s to be used by SCHED_OTHER”).
Sửa bài theo đó: (1) số 140 mức ưu tiên lấy từ [CFS] §6 (bộ lập lịch trước CFS, tức bản 2.6), không phải từ thư 2002 (thư ghi bảng bit
64 bit) → bài ghi “bản 2.6 có 140 mức”; (2) “viết lại khoảng 70% mã” → “sửa tới khoảng 70% mã” (nguồn: “touched”); (3) vòng đệm 4 ô là
thiết kế trong thư 2002 [O102], bài ghi “theo thiết kế năm 2002”; (4) “không có mẹo đoán” là mô tả lúc ra đời [CFS], còn [LWN23]/[KN66]
cho thấy về sau lại phụ thuộc mẹo và tham số chỉnh → bài ghi rõ hai thời điểm.

## Điều KHÔNG dạy (nguồn không ghi)
- Năm hoà vào nhân chính thức và số hiệu bản của bộ lập lịch O(1): [O102] chỉ ghi thư ngày 4/1/2002 và cập nhật 18/4/2002; [KN23] ghi
  “during the development of Linux 2.5”. Bài nói “năm 2002, trong lúc phát triển nhánh 2.5”, không nói ngày ra bản.
- Số máy, số CPU, số tiến trình của một hệ thật ở mỗi chặng: không nguồn nào ghi (ngoài “8-way” làm ví dụ ở [O102]). 1000 tiến trình sẵn
  sàng, 3 tiến trình đều đặn, lát 3 ms và 9 ms, 1 lệnh so sánh mỗi tiến trình là SỐ MINH HOẠ.
- Bảng trọng số theo mức nice (1024, hệ số 1,25…): không đọc trong phiên này → không dạy; chỉ dùng tỉ lệ cpu.shares 2048 / 1024 của [CFS].
- Độ cao cây đỏ đen, chi phí chèn O(log n): tài liệu không ghi số → không dạy con số cụ thể.
- Chi tiết “sleeper fairness”, cơ chế trễ huỷ hàng đợi (deferred dequeue) của EEVDF, latency-nice có được hoà vào nhân hay không: chỉ nêu ý
  “giao diện đặt lát thời gian riêng” như [EEV]; không dạy giá trị mặc định của lát.
- Kết quả đo hiệu năng EEVDF so với CFS: [LWN23] chỉ trích “wins and losses” sơ bộ → không dạy con số.
- Ai dùng sched_ext ở quy mô nào (công ty, số máy): các nguồn chính thức đã đọc không ghi → không dạy.
- Bài báo năm 1995 về EEVDF: không đọc trực tiếp; chỉ nhắc năm theo [EEV] và [LWN23].
- LWN 2007 “Schedulers: the plot thickens” (lwn.net/Articles/230574/) đã tải được nhưng không dùng chi tiết nào.
