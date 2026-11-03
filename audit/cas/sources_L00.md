# Nguồn đã đọc nguyên văn cho CAS L00 (phương pháp hậu kiểm không đổ lỗi)

Đọc ngày 2026-11-02 (urllib + trích văn bản HTML; bản tải để ở thư mục nháp của phiên, không đưa vào kho). Chỉ trích các câu bài giảng
dựa vào (CITED). Mọi con số khác là phép tính lại (VER: `checks` của bài, `audit/cas/verify_cas.py` mục L00,
`audit/verify_plan_curricula.py` CAS:L00) hoặc ghi rõ “(số minh hoạ)”. Không nêu tên người trong bản hậu kiểm mẫu.

## [R00] J. Reason, *Human error: models and management*, BMJ 320(7237):768–770, 18/3/2000
Tải: pmc.ncbi.nlm.nih.gov/articles/PMC1117770/ (HTTP 200, 110 696 byte; bản toàn văn của PubMed Central). Trang bmj.com trả **403**.
- “The human error problem can be viewed in two ways: the person approach and the system approach.”
- “The person approach focuses on the errors of individuals, blaming them for forgetfulness, inattention, or moral weakness”
- “The system approach concentrates on the conditions under which individuals work and tries to build defences to avert errors or mitigate
  their effects”
- Biện pháp của cách nhìn con người: “These methods include poster campaigns that appeal to people's sense of fear, writing another procedure
  (or adding to existing ones), disciplinary measures, threat of litigation, retraining, naming, blaming, and shaming.”
- “Errors are seen as consequences rather than causes”
- “Blaming individuals is emotionally more satisfying than targeting institutions.”
- “Firstly, it is often the best people who make the worst mistakes—error is not the monopoly of an unfortunate few. Secondly, far from being
  random, mishaps tend to fall into recurrent patterns. The same set of circumstances can provoke similar errors, regardless of the people
  involved.”
- “High technology systems have many defensive layers: some are engineered (alarms, physical barriers, automatic shutdowns, etc), others rely
  on people (surgeons, anaesthetists, pilots, control room operators, etc), and yet others depend on procedures and administrative controls.”
- “they are more like slices of Swiss cheese, having many holes—though unlike in the cheese, these holes are continually opening, shutting,
  and shifting their location. The presence of holes in any one “slice” does not normally cause a bad outcome. Usually, this can happen only
  when the holes in many layers momentarily line up to permit a trajectory of accident opportunity”
- “The holes in the defences arise for two reasons: active failures and latent conditions. Nearly all adverse events involve a combination
  of these two sets of factors.”
- “Active failures are the unsafe acts committed by people who are in direct contact with the patient or system. They take a variety of
  forms: slips, lapses, fumbles, mistakes, and procedural violations.” “Active failures have a direct and usually shortlived impact”
- “Latent conditions are the inevitable “resident pathogens” within the system. They arise from decisions made by designers, builders,
  procedure writers, and top level management.” … “(untrustworthy alarms and indicators, unworkable procedures, design and construction
  deficiencies, etc). Latent conditions—as the term suggests—may lie dormant within the system for many years before they combine with
  active failures and local triggers to create an accident opportunity.” (ví dụ “báo động không đáng tin” lấy từ đây.)
- “active failures are like mosquitoes. They can be swatted one by one, but they still keep coming. The best remedies are to create more
  effective defences and to drain the swamps in which they breed. The swamps, in this case, are the ever present latent conditions.”

## [SRE] Google, *Site Reliability Engineering* (O'Reilly 2016; bản web sre.google, “Copyright © 2017 Google, Inc.”)
Chương 15 “Postmortem Culture: Learning from Failure”: sre.google/sre-book/postmortem-culture/ (HTTP 200, 55 113 byte).
- “A postmortem is a written record of an incident, its impact, the actions taken to mitigate or resolve it, the root cause(s), and the
  follow-up actions to prevent the incident from recurring.”
- “For a postmortem to be truly blameless, it must focus on identifying the contributing causes of the incident without indicting any
  individual or team for bad or inappropriate behavior.”
- “You can’t "fix" people, but you can fix systems and processes to better support people making the right choices when designing and
  maintaining complex systems.”
- “An unreviewed postmortem might as well never have existed.”

Phụ lục D “Example Postmortem”: sre.google/sre-book/example-postmortem/ (HTTP 200, 49 719 byte). Đây là **sự cố giả định** do sách dựng
(“discovered in a Delorean’s glove compartment”) — bài nói rõ là bản mẫu, sự cố giả định.
- “Summary : Shakespeare Search down for 66 minutes during period of very high interest in Shakespeare due to discovery of a new sonnet.”
- “Impact : Estimated 1.21B queries lost, no revenue impact.”
- “Root Causes : Cascading failure due to combination of exceptionally high load and a resource leak when searches failed due to terms not
  being in the Shakespeare corpus. … Under normal circumstances, the rate of task failures due to resource leaks is low enough to be unnoticed.”
- “Trigger : Latent bug triggered by sudden increase in traffic.”
- Action Items: 9 việc, loại ghi lần lượt: mitigate, prevent, process, prevent, prevent, prevent, prevent, prevent, other
  → 1 giảm nhẹ, 6 ngăn ngừa, 1 quy trình, 1 khác (bài đếm lại; check example#5).
- “Where we got lucky” (chú thích: “This section is really for near misses”).
- Timeline (“all times UTC”): “14:53 Traffic to Shakespeare search increases by 88x”; “14:54 OUTAGE BEGINS”; “15:01 INCIDENT BEGINS …
  declares incident #465 … names … incident commander”; “15:34 found order-of-magnitude error in whiteboard calculations for instance count
  increase”; “15:36 OUTAGE MITIGATED , updated index replicated to all clusters”; “16:00 OUTAGE ENDS , all traffic balanced across all
  clusters”; “16:30 INCIDENT ENDS , reached exit criterion of 30 minutes’ nominal performance”.

## [CF19] Cloudflare, *Details of the Cloudflare outage on July 2, 2019* (12/7/2019)
blog.cloudflare.com/details-of-the-cloudflare-outage-on-july-2-2019/ (HTTP 200, 373 334 byte). Chỉ dùng một câu ở hook (bài 7 phân tích
sự cố này; số liệu đã đối chiếu với TOC L14):
- “Getting to a single root cause, while satisfying, may obscure the reality.”

## Phép tính của bài (VER, không có trong nguồn)
- 14:54 → 16:00 = 66 phút (khớp “66 minutes”); 14:54 → 15:01 = 7; 14:54 → 15:36 = 42; 16:00 → 16:30 = 30.
- 1,21 tỉ / 66 ≈ 18,3 triệu truy vấn mỗi phút — bài ghi “phép tính của bài, bản mẫu không ghi”.
- Ba lớp độc lập, mỗi lớp lọt 10% → 0,1% ; chung giả định → 10% (số minh hoạ; giáo án CAS:L00).

## Điều KHÔNG dạy (nguồn không ghi hoặc không đọc được)
- J. Allspaw, *Blameless PostMortems and a Just Culture* (Etsy, 2012): etsy.com trả **403**, web.archive.org trả **429** → không trích.
- Hình gốc “Swiss cheese” của bài báo: không chép; bài tự vẽ hình minh hoạ theo lời mô tả đã trích.
- Không gán con số tỉ lệ lọt nào cho một lớp phòng vệ thật: 10% là số minh hoạ.
- Tên người trong bản mẫu (người trực, người chỉ huy…): không nêu.
