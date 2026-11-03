# Nguồn đã đọc nguyên văn cho CAS L04 (Mars Pathfinder, 1997)

Đọc ngày 2026-11-02. Bản tải để ở thư mục nháp của phiên, không đưa vào kho. Chỉ trích câu bài giảng dựa vào (CITED). Mọi mốc mili giây
là SỐ MINH HOẠ, mô phỏng bằng `alg.cas_inversion_sim` (bài) và mô phỏng theo sự kiện viết riêng (`audit/cas/ver/L04.py`); giáo án CAS:L04.
Cùng nguồn với ESY L15 (`audit/esy/sources_L15.md`) — đã đối chiếu, không mâu thuẫn.

## [GR97] Trưởng nhóm phần mềm bay của tàu, *What really happened on Mars? — Authoritative Account*, thư 15/12/1997
Tải: www.cs.unc.edu/~anderson/teach/comp790/papers/mars_pathfinder_long_version.html (HTTP 200, 20 931 byte; bản chép thư gốc).
- “A single CPU controls the spacecraft.” “The hardware which we used to interface to the 1553 bus … was inherited from the Cassini
  spacecraft. This hardware came with a specific paradigm for its usage : the software will schedule activity at an 8 Hz rate.”
  Sơ đồ chu kỳ: “|< ------------- .125 seconds ------------------------>|”.
- “The bc_sched and bc_dist tasks check each cycle to be sure that the other had completed its execution. The bc_sched task is the highest
  priority task in the system (except for the vxWorks "tExec" task). The bc_dist is third highest … Science functions, such as imaging,
  image compression, and the ASI/MET task are still lower.”
- “Most of the tasks in the system that access the information collected over the 1553 do so via a double buffered shared memory mechanism
  … The exception to this is the ASI/MET task which is delivered its information via an interprocess communication mechanism (IPC).”
- “The failure was identified by the spacecraft as a failure of the bc_dist task to complete its execution before the bc_sched task started.
  The reaction to this by the spacecraft was to reset the computer. … It also terminates the execution of the current ground commanded
  activities. No science or engineering data is lost that has already been collected … However, the remainder of the activities for that day
  were not accomplished until the next day.”
- “The higher priority bc_dist task was blocked by the much lower priority ASI/MET task that was holding a shared resource. The ASI/MET task
  had acquired this resource and then been preempted by several of the medium priority tasks.” “the bc_sched task determined that the bc_dist
  task had not completed its cycle (a hard deadline in the system) and declared the error that initiated the reset.”
- “These features were not "fortuitously" left enabled but remain in the software by design. We strongly believe in the "test what you fly
  and fly what you test" philosophy.” “The bc_sched was already coded so as to stop the trace/log collection and dump the data … for this error.”
- “In less that 18 hours we were able to cause the problem to occur. Once we were able to reproduce the failure the priority inversion
  problem was obvious.”
- “change the creation flags for the semaphore so as to enable priority inheritance. The Wind River folks … supply global configuration
  variables for parameters such as the "options" parameter for the semMCreate used by the select service”. Bốn câu hỏi: “1) … When you change
  this global variable all of the select semaphores created after that point will be created with the new options.” “2) … how will this
  change the behavior of the rest of the system ?” “3) The priority inheritance option was deliberately left out by Wind River in the
  default selectLib() service for optimum performance.” “4) Was there some intrinsic behavior of the select mechanism itself that would
  change …”. “They concluded that the performance impact would be minimal and that the behavior of select() would not change so long as there
  was always only one task waiting for any particular file descriptor. This is true in our system.” “We concluded, both by analysis and test,
  that there was no adverse behavior. We tested the system extensively before we changed the software on the spacecraft.”
- “No, we did not use the vxWorks shell to change the software … It involves sending the differences between what you have onboard and what
  you want … Custom software on the spacecraft (with a whole bunch of validation) modifies the onboard copy.”
- “The problem would only manifest itself when ASI/MET data was being collected and intermediate tasks were heavily loaded. Our before launch
  testing was limited to the "best case" high data rates and science activities. The fact that data rates from the surface were higher than
  anticipated …” “We did see the problem before landing but could not get it to repeat when we tried to track it down.”
- “We knew that if this problem occurred we would reset. … There are a large number of safeguards in the system”.
- “there was no conscious decision to not have the priority inheritance option enabled. We just missed it. There are several other places in
  the flight software where similar protection is required for critical data structures and the semaphores do have priority inversion
  protection. A good lesson when you fly COTS stuff - make sure you know how it works.”

## [MJ97] M. Jones, *What Happened on Mars?*, thư 5/12/1997 (kể lại bài nói ở hội nghị)
Tải: www.cs.cmu.edu/afs/cs/user/raj/www/mars.html (HTTP 200, 8 859 byte).
- “after its July 4th, 1997 landing on the Martian surface … But a few days into the mission, not long after Pathfinder started gathering
  meteorological data, the spacecraft began experiencing total system resets”.
- Các chi tiết bị [GR97] đính chính, bài nêu như ví dụ “tin bản kể lại”: “a watchdog timer would go off” (theo [GR97]: tác vụ lập lịch
  phát hiện trễ hạn); “The JPL engineers fortuitously decided to launch the spacecraft with this feature still enabled” (theo [GR97]: “by
  design”); “A short C program was uploaded to the spacecraft, which when interpreted, changed the values” (theo [GR97]: không dùng shell,
  gửi phần sai khác). [MJ97] ghi “each resulting in losses of data” — [GR97] ghi dữ liệu đã thu không mất → bài theo [GR97].

## Điều KHÔNG dạy
- Số lần khởi động lại, ngày cụ thể của từng lần: không nguồn nào trong hai thư ghi → bài nói “nhiều lần”, “vài ngày sau”.
- Thời gian thật của từng tác vụ (ms): không ghi → mọi mốc là số minh hoạ (giáo án CAS:L04).
- Tên người trong thư (người viết, người dựng công cụ ghi vết…): không nêu; tên hệ điều hành và nhà cung cấp chỉ ở nguồn.
