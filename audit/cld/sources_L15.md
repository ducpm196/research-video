# Nguồn đã đọc nguyên văn cho CLD L15 (bài hành trình Borg → Omega → Kubernetes)

Đọc ngày 2026-10-31. Chỉ trích các câu bài giảng dựa vào (CITED); mọi con số khác trong bài là phép tính lại (VER, `checks` của bài)
hoặc ghi rõ “minh hoạ”. Không nêu tên cá nhân trong lời đọc; tên tác giả chỉ ở `source:` và trên màn hình nguồn.

## [B15] A. Verma, L. Pedrosa, M. Korupolu, D. Oppenheimer, E. Tune, J. Wilkes. *Large-scale cluster management at Google with Borg.* EuroSys 2015, Bordeaux (doi 10.1145/2741948.2741964)
Tải: static.googleusercontent.com/media/research.google.com/en//pubs/archive/43438.pdf (18 trang).
- Tóm tắt: “runs hundreds of thousands of jobs, from many thousands of different applications, across a number of clusters each with up to tens of thousands of machines.”
- §1: “a set of qualitative observations we have made from operating Borg in production for more than a decade.”
- §2.3: “Our median cell size is about 10 k machines after excluding test cells; some are much larger.”
- §2.6: “help our SREs manage a few tens of thousands of machines per person.”
- §4 (Availability): Borg “automatically reschedules evicted tasks …; reduces correlated failures by spreading tasks of a job across failure domains such as machines, racks, and power domains; limits the allowed rate of task disruptions …; uses declarative desired-state representations and idempotent mutating operations, so that a failed client can harmlessly resubmit any forgotten requests; rate-limits finding new places for tasks from machines that become unreachable, because it cannot distinguish between large-scale machine failure and a network partition; …”
- §4: “already-running tasks continue to run even if the Borgmaster or a task’s Borglet goes down.”
- §4: “Borgmaster uses a combination of techniques that enable it to achieve 99.99% availability in practice … Each cell is independent of the others to minimize the chance of correlated operator errors and failure propagation.”
- §5.2: “98% of the machines in shared Borg cells, 83% across the entire set of machines managed by Borg.” “segregating prod and non-prod work would need 20–30% more machines in the median cell to run our workload.”
- §5.2 (đọc lại 2026-11-09 từ PDF tải về, đợt C): “That’s because prod jobs usually reserve resources to handle rare workload spikes, but don’t use these resources most of the time.” (căn cứ “điểm nghẽn” chặng 1); “we split off a user’s workload into a new cell if they consumed at least 10 TiB of memory (or 100 TiB) … we would need 2–16× as many cells, and 20–150% additional machines.” (căn cứ câu hỏi 2 của bài: tách theo người dùng/đội — KHÔNG dùng con số 20–30% của tách prod/non-prod cho trường hợp này).
- §4 (đọc lại 2026-11-09): “Failures are the norm in large scale systems” (căn cứ “máy hỏng là chuyện hằng ngày”).

## [Q16] B. Burns, B. Grant, D. Oppenheimer, E. Brewer, J. Wilkes. *Borg, Omega, and Kubernetes — Lessons learned from three container-management systems over a decade.* ACM Queue 14(1), January–February 2016
Tải: static.googleusercontent.com/media/research.google.com/en//pubs/archive/44843.pdf (24 trang).
- “at Google we have been managing Linux containers at scale for more than ten years and built three different container-management systems in that time.”
- Borg “was built to manage both long-running services and batch jobs, which had previously been handled by two separate systems: Babysitter and the Global Work Queue … both predated Linux control groups. Borg shares machines between these two types of applications as a way of increasing resource utilization and thereby reducing costs.”
- “the result was a somewhat heterogeneous, ad-hoc collection of systems that Borg’s users had to configure and interact with, using several different configuration languages and processes.”
- Omega “was driven by a desire to improve the software engineering of the Borg ecosystem … stored the state of the cluster in a centralized Paxos-based transaction-oriented store … using optimistic concurrency control … Many of Omega’s innovations (including multiple schedulers) have since been folded into Borg.” (Omega: EuroSys 2013, tham khảo [6] của bài.)
- Kubernetes “was conceived of and developed in a world where external developers were becoming interested in Linux containers … Kubernetes is open source … state in Kubernetes is accessed exclusively through a domain-specific REST API”.
- “Orchestration is the beginning, not the end … these tools typically picked idiosyncratic APIs, conventions … An undesired side effect was to increase the complexity of deploying applications in the Borg ecosystem.”
- “every Kubernetes object has three basic fields in its description: ObjectMetadata, Specification (or Spec), and Status.”
- “reconciliation controller loop … compares a desired state … against the observed state … and takes actions to converge … when a controller fails or restarts it simply picks up where it left off.”
- THINGS TO AVOID: “Don’t make the container system manage port numbers … Kubernetes would allocate an IP address per pod”; “Don’t just number containers: give them labels … if the application uses range sharding based on the task index, Borg’s restart policy can cause data unavailability, as it takes down adjacent tasks … people encode this information into job names that they decode using regular expressions”; “Be careful with ownership”; “Don’t expose raw state … forcing all store accesses through a centralized API server”.
- Open problems — Configuration: “configuration-management systems tend to invent a domain-specific configuration language that (eventually) becomes Turing complete … We believe the most effective approach is to … maintain a clean separation between computation and data.”

## [K24] Kubernetes Blog, *10 Years of Kubernetes*, 2024-06-06 (kubernetes.io/blog/2024/06/06/10-years-of-kubernetes/)
- “on June 6th, 2014, the first commit of Kubernetes was pushed to GitHub. That first commit with 250 files and 47,501 lines of go, bash and markdown …”
- “over 88,000 contributors from more than 8,000 companies, across 44 countries.”
- “the first prototype (which came about in 2013)”; “Google's Borg system … had adopted Linux containers as they were developed in the mid-2000s.”
- “culminating in a version 1.0 release on July 21st, 2015. Alongside 1.0, Google announced that Kubernetes would be donated to … the Cloud Native Computing Foundation (CNCF).”
- “Despite reaching 1.0, the Kubernetes project was still very challenging to use and understand.”
- “December 2016 - Kubernetes 1.5 introduces runtime pluggability with initial CRI support”; “September 2019 — Custom Resource Definitions go GA in Kubernetes 1.16”; “August 2020 — Kubernetes 1.19 increases the support window for releases to 1 year”; “April 2021 — the Kubernetes release cadence changes from 4 releases per year to 3 releases per year”; “July 2021 — Widely used beta APIs are removed in Kubernetes 1.22”; “May 2022 — Kubernetes 1.24 sees beta APIs become disabled by default to reduce upgrade conflicts and removal of Dockershim, leading to widespread user confusion (we've since improved our communication!)”.

## Đối chiếu lại đợt C (2026-11-09)
- B15, Q16 (PDF tải từ static.googleusercontent.com) và K24 (kubernetes.io) đã mở lại; các câu trích trên khớp văn bản.
- Omega: Q16 không ghi năm; năm 2013 là năm bài báo Omega (EuroSys 2013, tham khảo [6] của Q16) → bài ghi “quanh 2013 / bài báo năm 2013”, không nói Omega ra đời năm 2013.
- K24: “widespread user confusion” gắn với mục 5/2022 (1.24, bỏ Dockershim); 1.22 (gỡ beta API dùng rộng rãi) được gọi là “lessons learned” → bài tách hai ý.
- B15 §4: mỗi ô độc lập là để “minimize the chance of correlated operator errors and failure propagation” → câu hỏi 2 nói đúng lý do này.

## Điều KHÔNG dạy (nguồn không ghi)
- Năm Borg ra đời chính xác: nguồn chỉ ghi “hơn mười năm” tính tới 2015 và “giữa những năm 2000” → bài ghi “giữa thập niên 2000”.
- Bố trí bản sao ở tác vụ kề bên: Q16 chỉ ghi “takes down adjacent tasks”; ví dụ 6 tác vụ, bản sao ở tác vụ kế tiếp là GIẢ ĐỊNH MINH HOẠ, ghi rõ trên màn hình.
- Chính sách “hỗ trợ 3 bản gần nhất”, lệch phiên bản: không có trong K24 → không dạy.
