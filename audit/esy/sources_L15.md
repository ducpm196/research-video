# Nguồn đã đọc nguyên văn cho ESY L15 (bài hành trình: phần mềm trên robot thăm dò sao Hoả, 1997 → 2004 → 2015 → nay)

Đọc ngày 2026-11-02. Chỉ trích các câu bài giảng dựa vào (CITED); mọi con số khác trong bài là phép tính lại (VER, `checks` của bài,
`audit/esy/verify_esy.py` L15a–L15f và `audit/verify_plan_curricula.py` ESY:L15) hoặc ghi rõ “(số minh hoạ)”.
Không nêu tên cá nhân trong lời đọc; tên tác giả chỉ ở `source:` và dòng nguồn trên màn hình.
Tránh trùng bài CAS L04 (khoá CAS chưa soạn, sẽ phân tích sự cố Pathfinder như một sự cố): bài này KHÔNG kể lại dòng thời gian sự cố
chi tiết, mà rút thực hành kỹ thuật theo quy mô nhiệm vụ (một tàu → hai xe nhiệm vụ 3 tháng → nhiệm vụ kéo dài hơn 10 năm → nhiều
nhiệm vụ nhỏ dùng chung một khung phần mềm).

## [GR97] G. Reeves (trưởng nhóm phần mềm bay Mars Pathfinder, JPL), thư “What really happened on Mars? — Authoritative Account”, 15/12/1997
Bản gốc đăng ở trang của M. Jones (research.microsoft.com/~mbj/Mars_Pathfinder/Authoritative_Account.html): curl 403; trang mới
microsoft.com/en-us/research/people/mbj/…: 403 (curl) và 404 (WebFetch); web.archive.org: 429 (bị giới hạn tốc độ, không thử lách).
Đọc bản chép nguyên văn tại https://www.cs.unc.edu/~anderson/teach/comp790/papers/mars_pathfinder_long_version.html (trang môn học
của Đại học North Carolina; curl 200, 20 931 byte; tiêu đề, người gửi Glenn.E.Reeves@jpl.nasa.gov, ngày “Monday, December 15, 1997”).
Khớp từng chữ với bản trên trang Microsoft: NOT_VERIFIED (không đọc được trang đó).
- Phần cứng: “A single CPU controls the spacecraft.” “Wind River ported vxWorks to the RS6000 processor for us for this mission”.
  “The hardware which we used to interface to the 1553 bus (at both ends) was inherited from the Cassini spacecraft. This hardware came
  with a specific paradigm for its usage : the software will schedule activity at an 8 Hz rate.”
- Chu kỳ: sơ đồ “|< ------------- .125 seconds ------------------------>|”; “t1 - bus hardware starts via hardware control on the 8 Hz
  boundary”; “t4 - bc_sched task is awakened to setup transactions for the next cycle”. “The bc_sched and bc_dist tasks check each cycle
  to be sure that the other had completed its execution.”
- Ưu tiên: “The bc_sched task is the highest priority task in the system (except for the vxWorks "tExec" task). The bc_dist is third
  highest (a task controlling the entry and landing is second).” “Science functions, such as imaging, image compression, and the ASI/MET
  task are still lower.”
- Lỗi: “The failure was identified by the spacecraft as a failure of the bc_dist task to complete its execution before the bc_sched task
  started. The reaction to this by the spacecraft was to reset the computer.” “No science or engineering data is lost that has already
  been collected … However, the remainder of the activities for that day were not accomplished until the next day.”
  “The failure turned out to be a case of priority inversion … The higher priority bc_dist task was blocked by the much lower priority
  ASI/MET task that was holding a shared resource. The ASI/MET task had acquired this resource and then been preempted by several of the
  medium priority tasks.” “The resource that caused this problem was a mutual exclusion semaphore used within the select() mechanism”.
  “the bc_sched task determined that the bc_dist task had not completed its cycle (a hard deadline in the system)”.
- Tìm ra: “several debug features … These features were not "fortuitously" left enabled but remain in the software by design. We
  strongly believe in the "test what you fly and fly what you test" philosophy.” “trace/log facility … continues to collect data (in ring
  buffers) until told to stop.” “The bc_sched was already coded so as to stop the trace/log collection and dump the data … for this error.
  So, when we went into the lab to test it we did not have to change the software.” “In less that 18 hours we were able to cause the
  problem to occur.”
- Sửa: “change the creation flags for the semaphore so as to enable priority inheritance.” “When you change this global variable all of
  the select semaphores created after that point will be created with the new options.” “The priority inheritance option was deliberately
  left out by Wind River in the default selectLib() service for optimum performance.” “We did end up modifying the global variable to
  include the priority inheritance option. This corrected the problem.” “They concluded that the performance impact would be minimal”.
  “We concluded, both by analysis and test, that there was no adverse behavior. We tested the system extensively before we changed the
  software on the spacecraft.”
- Cách vá: “No, we did not use the vxWorks shell to change the software”. “It involves sending the differences between what you have
  onboard and what you want (and have on Earth) to the spacecraft. Custom software on the spacecraft (with a whole bunch of validation)
  modifies the onboard copy.”
- Vì sao không bắt được trước khi phóng: “The problem would only manifest itself when ASI/MET data was being collected and intermediate
  tasks were heavily loaded. Our before launch testing was limited to the "best case" high data rates and science activities. The fact that
  data rates from the surface were higher than anticipated … We did not expect nor test the "better than we could have ever imagined" case.”
  “We did see the problem before landing but could not get it to repeat when we tried to track it down.” “we ran out of time to get the
  lower priority issues completed.”
- Bền vững: “We knew that if this problem occurred we would reset.” “We built in the ability (and tested it) to go through multiple resets
  while we were going through the Martian atmosphere.” “The spacecraft would have even done a 60 day mission on its own”.
- Bài học: “there was no conscious decision to not have the priority inheritance option enabled. We just missed it.” “A good lesson when
  you fly COTS stuff - make sure you know how it works.” “we could not have figured this out **ever** if we did not have the tools to give
  us the insight.” Về bản kể lại: “I think I have had probably 400 people send me copies.” “Dave Wilner did talk to me about this problem
  before he gave his talk. I could not find my notes … So, I winged it and I sure did get it wrong.”

## [MJ97] M. Jones, “What Happened on Mars?”, thư 5/12/1997 (tóm tắt bài nói của Wind River tại IEEE RTSS 1997)
Tải: https://www.cs.cmu.edu/afs/cs/user/raj/www/mars.html (trang của R. Rajkumar, CMU; curl 200, 8 859 byte).
Chỉ dùng để dạy bài học “đọc lịch sử qua bản kể lại”: [MJ97] viết “The JPL engineers fortuitously decided to launch the spacecraft with
this feature still enabled.” và “A short C program was uploaded to the spacecraft, which when interpreted, changed the values of these
variables from FALSE to TRUE.” — [GR97] sửa lại cả hai: tính năng gỡ lỗi để lại “by design”, và “we did not use the vxWorks shell”.
Cũng từ [MJ97]: “It is precisely in such time critical and important situations where correctness is essential, even at some additional
performance cost.” Bài báo nền: “L. Sha, R. Rajkumar, and J. P. Lehoczky, Priority Inheritance Protocols: An Approach to Real-Time
Synchronization. In IEEE Transactions on Computers, vol. 39, pp. 1175-1185, Sep. 1990.”

## [RN05] G. Reeves, T. Neilson (JPL), “The Mars Rover Spirit FLASH Anomaly”, IEEE Aerospace Conference 2005 (IEEEAC paper #1426, Version 5, 2/12/2004)
NTRS: https://ntrs.nasa.gov/citations/20060044140 (API trả bản ghi: “The Mars Rover Spirit FLASH anomaly”, CONFERENCE_PAPER, ngày
xuất bản 2005-03-05, `downloads: []` — NTRS không có tệp toàn văn). Đọc toàn văn bản tác giả tại
https://www.cs.princeton.edu/courses/archive/spr08/cos333/mars.rover.pdf (curl 200, 522 168 byte, 14 trang; dòng bản quyền
“0-7803-8870-4/05/$20.00© 2005 IEEE”). Bản thứ hai corpora.tika.apache.org/…/321622.pdf: curl lỗi kết nối, không đọc.
- §1: “NASA's Mars Exploration Rovers (MER) project landed two rovers, Spirit and Opportunity, on Mars on January 4 and January 25, 2004”.
  “An anomaly occurred on the MER-A vehicle, Spirit, on Sol 18, or January 21, 2004”. “Spirit was finally restored to its normal
  operational state on Sol 32, and nominal science activities resumed on Sol 33.” Chú thích 3: “A sol is a Martian day, 24 hours 37
  minutes long”. **Ghi chú đợt C (2026-11-09):** 24 h 37 min là ngày SAO của sao Hoả (24,6229 h); sol là ngày MẶT TRỜI, trung bình
  24 h 39 min 35,244 s = 24,6597 h (NASA NSSDCA, Mars Fact Sheet, D. R. Williams, truy cập 2026-11-09, no revision given — giá trị
  chuẩn, cũng là định nghĩa “sol” của các nhiệm vụ MER). Bài dùng ≈ 1480 phút, không chép số 24 h 37 min của chú thích này. “The root cause of the anomaly was a design error in the software module that provides file system services. In
  addition, two significant configuration errors detrimentally affected the overall behavior of the system”.
- §2 (đặt lại trễ): “If the FSW determines that a reset is necessary during the FSW initialization process, the FSW delays the actual reset
  until a minimum time period has passed. This process is referred to as a "delayed reset". The intent is to allow sufficient time for
  ground intervention.” “the boot logic … is designed to load and start alternating copies of the FSW with each reset. By design, the time
  period between resets is set to a fifteen minute delay for the first severe error, fifteen minutes for the second, and then one hour for
  the third. This pattern then repeats”.
- §2 Sol 21: “send a hardware command to place Spirit in a "crippled mode". This command tells the FSW "do not use the FLASH file system"”.
  Chú thích 8: “The crippled mode command is one of a few commands that are processed entirely by hardware. The command only sets individual
  bits in a software accessible register that the FSW interrogates during initialization”. “the crippled command only sets volatile
  registers, which revert to the nominal state after the electronics are powered off.”
- §2 Sol 32: “the team manually booted the rover into crippled mode and copied the FSW image into RAM (for insurance). The team then ran a
  sequence that erased small chunks of FLASH at a time, and checked both FSW images … after each chunk.”
- §3 Bảng 1: “FLASH File System … FLASH … 224 Mbytes … Science and engineering data products”.
- §3 Thiết kế: “The MER FSW uses a commercial operating system and capitalizes upon many of the bundled functions and libraries”.
  “When a file is deleted, the only action performed is to change the value of the first letter in the file name to a special value (the
  infamous hex byte code value E5h).” “when a file is deleted, the space in the file system (on FLASH) is freed but the internal data
  structure space is still required. In fact, the space is never released.” “the total size of the file system structure … is not expressed
  by the number of current files but by the sum of the maximum number of files that had ever existed in each subdirectory.”
- §3 Cấu hình: “In the MER configuration, this initial size is 256K bytes.” “when the initial space was exhausted, the DOS Library logic
  made allocation requests in increments of 256K bytes from the free system memory.” “a second parameter can be set to limit the growth to a
  maximum amount of space. This second parameter was also in error; no limit was specified.” Chú thích 12: “The free system memory is > 4
  Mbytes normally”. “By convention, applications are allowed to request memory allocations only during initialization.” “the configuration
  parameter was not set correctly, and the task performing the file system activity was silently suspended.” “The MER architecture includes
  a "software health" function that continuously checks for suspended tasks. When the health monitor function identifies a suspended task,
  it forces a reset”.
- §3 Đặt lại lặp: “each time the software initializes, the FLASH file system is mounted. This caused the re-creation of the RAM resident
  data structures, which, in turn, consumed all of the available memory.” “The cycle then repeated.” Phụ: “the memory allocation failure
  occurred within one of these critical regions. With the task suspended, the access control semaphore was never released”.
  §4 Sol 19: “there was no timeout or other logic to force the continuation of the shutdown actions”.
- §4 Sol 21: “The system is not as capable in this configuration since the RAM based file system is 10 times smaller and volatile.”
- §5: “the compressed development schedule (three years from concept to launch)”. “The data product management software limits the number
  of data products to 8192 unique items.” “Lesson--Understand the behavior of any Commercial Off-The-Shelf (COTS) software that is utilized.”
  “Lesson--Enforce the design guidelines. There was a design guideline that prohibited allocation of space from the free system memory
  space after initialization was complete. This guideline was enforced for the JPL-developed software and it should have been enforced for
  the COTS software as well.” “There should have been a formal management of incomplete items that required resolution.” “Lesson--The FSW
  should have included flight telemetry for resources (such as the free system memory space)”. “A post-anomaly review of one operational
  test showed that the memory leak was evident in the data.” “a longer operational test (over 11 sols) was impractical”. “The idea for
  crippled mode originated on the Mars Pathfinder project. Without this capability, the MER mission may well have been lost.” “The lack of
  compaction for deleted files in the directory structures is a fundamental flaw for long duration missions.”
- §6 Vận hành: “Monitor the amount of free memory space in the system. If the remaining space drops to 800 Kbytes or less, then terminate
  all science and engineering activities.” “Aggressively command the deletion of received data products … The data management team has
  reduced the latency for this action from 48 to 24 hours.” “Remove subdirectories when no more data product files exist.”
- §6 Bản phần mềm 4/2004: “Additional logic to remove the directory list structure entries for deleted files. This change "compacts" the
  directory list structure and thus, removes the "high water mark" effect.” “Additional logic to autonomously enter crippled mode when
  multiple resets have occurred.” “Modifications to the shutdown logic to use the alarm clock hardware function as a secondary watchdog.”
- §6 Không làm: “In hindsight, the correct implementation would have been to limit the private memory area used by DOS Library to a fixed
  size.” “However, this change was not incorporated into the new FSW. This was a considered decision that balanced the benefit versus risk”.
  “the change might expose other, unexplored, behavior … The test program … would be challenging, complex, and time consuming.” “The vehicle
  lifetime is limited.”
- §8: “The predominant factor that led to this error was the compressed design schedule.” “a dedicated team that designed a system with
  built-in diagnostic tools, autonomous communication, and robust fault protection.”

## [JPL14a] NASA/JPL news, “Memory Reformat Planned for Opportunity Mars Rover”, 29/8/2014 (cập nhật 8/9/2014)
URL: https://www.jpl.nasa.gov/news/memory-reformat-planned-for-opportunity-mars-rover/ — curl 403; đọc bằng WebFetch (công cụ trả câu
trích theo yêu cầu, không trả toàn văn). Câu “leading suspect” khớp với bản The Register 30/8/2014 (kết quả tìm kiếm).
- “The resets, including a dozen this month, interfere with the rover's planned science activities”.
- “Worn-out cells in the flash memory are the leading suspect in causing these resets,”
- “Reformatting clears the memory while identifying bad cells and flagging them to be avoided.”
- “as critical sequences and flight software are stored elsewhere in other non-volatile memory on the rover”.
- “missions planned to last only three months”. “Spirit worked for six years, and Opportunity is still active.”
- “The project reformatted the flash memory on Spirit five years ago to stop a series of amnesia events”.
- Cập nhật: “NASA's Mars Exploration Rover Opportunity has successfully reformatted its flash memory.” (Sol 3773, 4/9/2014 — theo WebFetch).

## [JPL14b] NASA/JPL news, “Opportunity Working in No-Flash Mode for Now”, 11/12/2014
URL: https://www.jpl.nasa.gov/news/opportunity-working-in-no-flash-mode-for-now/ — curl 403; đọc bằng WebFetch.
- “Data gathered each Martian day is stored in volatile memory, which on Opportunity is random-access memory, or RAM.”
- “That data stored in volatile memory is relayed Earthward before sleep because it is lost when power goes off.”
- “have occurred in only one of the seven banks of flash microchip circuitry on board.” “The team plans to send commands for the rover to
  avoid that entire bank.”
- Người quản lý dự án: “The mission can continue without storing data to flash memory, and instead store data in volatile RAM”.

## [JPL15] NASA/JPL news, “Rover 'Amnesia' Event Follows Latest Memory Reformatting”, 27/3/2015
URL: https://www.jpl.nasa.gov/news/rover-amnesia-event-follows-latest-memory-reformatting/ — curl 403; đọc bằng WebFetch.
- “Opportunity has seven banks of flash memory.” “the team revised the rover's onboard software to avoid use of Bank 7.”
- “After the March 20 reformatting, the rover resumed use of the other six banks.”
- “The amnesia event did not result in any loss of science data.”
- “Only time will tell if we have been successful in mitigating the most serious flash problems.”

## [FP] NASA/JPL, F´ (F Prime) — README trên GitHub và trang chính thức fprime.jpl.nasa.gov
Tải: https://raw.githubusercontent.com/nasa/fprime/devel/README.md (curl 200, 5 825 byte); https://fprime.jpl.nasa.gov/overview/ (200,
41 061 byte); https://fprime.jpl.nasa.gov/overview/projects/ (200, 41 838 byte). Trang không ghi ngày viết; bản quyền “© 2025”.
- README: “F´ (F Prime) is a component-driven framework that enables rapid development and deployment of spaceflight and other embedded
  software applications. Originally developed at the Jet Propulsion Laboratory”. “It is tailored but not limited to small-scale spaceflight
  systems such as CubeSats, SmallSats, and instruments.” “An architecture that decomposes flight software into discrete components with
  well-defined interfaces”; “A C++ framework that provides core capabilities such as message queues and threads”; “Testing tools for testing
  flight software at the unit and integration levels.” Tiêu đề: “A Flight-Proven, Multi-Platform, Open-Source Flight Software Framework”.
- Overview: “We now need to support more flight missions than ever before along with a growing variety of processors and operating systems.
  We need to accommodate tighter cost constraints and shorter development schedules”. “greater emphasis on versatility, reusability, and
  portability without sacrificing reliability and performance.” “Supports running with or without an operating system (useful for executing
  on low power/low performance microcontrollers)”. “Component Library … Usable without modification in new software projects”.
- Projects (8 dự án): ISS-RapidScat “Start Date: Sep. 21, 2014 End Date: Nov. 18, 2018”; ASTERIA “OS: Linux … Start Date: Aug. 14, 2017”;
  Mars Helicopter (Ingenuity) “OS: Linux HW Platform: Qualcomm’s Snapdragon 801 Start Date: Jul. 30, 2020”; Lunar Flashlight “OS: VxWorks …
  Dec. 11, 2022”; Near Earth Asteroid Scout “OS: VxWorks … Nov. 16, 2022”; OWLS “OS: -”; CADRE “OS: Linux … Start Date: 2025”; COLDArm
  “OS: -”. → Linux 3, VxWorks 2, không ghi 3 (đếm lại trong `checks`).

## Điều KHÔNG dạy (nguồn không ghi, hoặc không đọc được nguyên văn)
- Số lần tự khởi động lại của Pathfinder, ngày cụ thể của từng lần, thời gian chạy (ms) của từng tác vụ: [GR97] không ghi → mọi mốc ms trong
  ví dụ đảo ngược ưu tiên là SỐ MINH HOẠ (chỉ chu kỳ 0,125 s là CITED).
- Chi tiết “ba khoá loại trừ”, “chương trình C ngắn đổi FALSE thành TRUE”, “kỹ sư cuối cùng ở lại phòng thí nghiệm” chỉ có ở [MJ97] và bị
  [GR97] sửa (hoặc không xác nhận) → không dạy như sự thật; chỉ nêu là ví dụ bản kể lại sai.
- Báo cáo bất thường JPL D-22919 (2004) và báo cáo cuối nhiệm vụ Pathfinder: không đọc → không dạy chi tiết riêng của chúng.
- Số lần đặt lại thực tế của Spirit mỗi sol: [RN05] chỉ ghi mẫu 15–15–60 phút “repeats” và “many reset/reboot cycles” → con số “tối đa
  khoảng 49 lần mỗi sol” trong bài là PHÉP TÍNH TRÊN MẪU (cận trên nếu lặp suốt sol), ghi rõ như vậy, không phải số đo.
- Kích thước một mục thư mục trong bộ nhớ RAM, số tệp trong từng thư mục con: không có → số minh hoạ.
- Nguyên nhân vật lý mòn ô nhớ flash, số lần ghi tối đa: các trang JPL chỉ ghi “worn-out cells … leading suspect” → không dạy cơ chế mòn.
- Ngày F´ được công bố mã nguồn mở, kích thước mã, số nhiệm vụ ngoài 8 dự án liệt kê: không có trên trang đã đọc → không dạy.
- Phần mềm của Curiosity, Perseverance: không đọc nguồn → không dạy.
