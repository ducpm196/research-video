# Nguồn đã đọc nguyên văn cho SAR L13 (bài hành trình: Twitter từ nguyên khối Ruby tới dịch vụ trên máy ảo Java)

Đọc ngày 2026-11-02 (curl + pdftotext). Chỉ trích các câu bài giảng dựa vào (CITED); mọi con số khác trong bài là phép tính lại (VER,
`checks` của bài và `audit/sar/verify_sar.py` L13) hoặc ghi rõ “(số minh hoạ)”. Không nêu tên cá nhân trong lời đọc; tên tác giả chỉ ở
`source:`.

## Đổi so với ROADMAP §8.1 mục 3 (ứng viên “New Tweets per second record, and how!”, blog kỹ thuật Twitter 2013)
- `blog.twitter.com/2013/new-tweets-per-second-record-and-how` chuyển sang `blog.x.com/...` → **HTTP 403** (curl và WebFetch).
  Bản lưu Wayback Machine: **HTTP 429** liên tục (9 lần thử trong khoảng 20 phút, 2026-11-02); WebFetch không được phép lấy từ
  web.archive.org / archive.ph; chỉ mục Common Crawl trả 504. Planet MySQL (entry 258324) chỉ có đoạn trích ngắn → **bài blog 2013
  KHÔNG đọc được nguyên văn, KHÔNG dạy chi tiết riêng của nó**.
- Thay bằng ba nguồn gốc do chính kỹ sư Twitter viết, đọc được nguyên văn, kể cùng hành trình (và bài [AN14] dẫn đúng URL bài blog 2013
  cho con số kỷ lục):
  [AN14] bài trình bày của trưởng nhóm mã nguồn mở Twitter; [BD14] bài trình bày QCon London 2014 của một kỹ sư nhóm thư viện lõi
  Twitter; [ME13] bài báo “Your Server as a Function” (Twitter, 2013).

## [AN14] C. Aniszczyk (Head of Open Source, Twitter), *Scaling Twitter with Open Source*, bài trình bày (PDF)
Tải: events.static.linuxfound.org/sites/events/files/scalingtwitter_chris_aniszczyk.pdf (curl, 8 694 230 byte, pdftotext -layout).
Slide không ghi ngày; nội dung nhắc “World Cup 2014” và “284M+ Active Users” → trình bày năm 2014 (INFERRED). Trích theo tiêu đề slide:
- “What is the scale of Twitter?”: “500,000,000+ Tweets / Day”, “3,500,000,000+ Tweets / Week”, “6000+ Tweets / Second (steady state)”,
  “However, there are peaks!”
- “Miyazaki 2011 25,088 TPS”; “Miyazaki 2013 … 143,199 TPS https://blog.twitter.com/2013/new-tweets-per-second-record-and-how”.
  (Slide cũng ghi “NYE 2013: 33,338 TPS” — không dùng, vì không đối chiếu được.)
- “sizeof(1 tweet) = 140 characters 200 bytes”.
- “2006: A simple idea... Routing Presentation Logic Storage — MySQL — Monorail (Ruby on Rails)”.
- “2008: Growing Pains … Monorail (Ruby on Rails) MySQL Tweet Store Flock Cache Memcache Redis”.
- “2009+: Crazy Growth” (biểu đồ 250M → 500M, mốc 2006 2009 2010 2013).
- “2010: World Cup Woes” (dẫn blog.twitter.com/2010/2010-world-cup-global-conversation).
- “What was wrong?”: “Fragile monolithic Rails code base: managing raw database and memcache connections to rendering the site and
  presenting the public APIs”; “Throwing machines at the problem: instead of engineering solutions”; “Trapped in an optimization corner:
  trade off readability and flexibility for performance”.
- “Whale Hunting Expeditions”: “We organized archeology digs and whale hunting expeditions to understand large scale failures”.
- “Re-envision the system?”: “We wanted big infra wins: in performance, reliability and efficiency (reduce machines to run Twitter by
  10x)”; “Failure is inevitable in distributed systems: we wanted to isolate failures across our infrastructure”; “Cleaner boundaries
  with related logic in one place: desire for a loosely coupled services oriented model at the systems level”.
- “Ruby VM Reflection”: “Started to evaluate our front end server tier: CPU, RAM and network”; “Rails machines were being pushed to the
  limit: CPU and RAM maxed but not network (200-300 requests/host)”; “Twitter's usage was growing: it was going to take a lot of machines
  to keep up with the growth curve”.
- “JVM (Java) Experimentation”: “Search (Java via Lucene)” (dẫn engineering.twitter.com/2010/10/twitters-new-search-architecture.html);
  “FlockDB: Social Graph (Scala)” (dẫn blog.twitter.com/2010/introducing-flockdb); “...and we liked it, enamored by JVM performance!”
- “The JVM Solution”: “Level of trust with the JVM with previous experience”; “JVM is a mature and world class platform”; “Huge mature
  ecosystem of libraries”; “Polyglot possibilities (Java, Scala, Clojure, etc)”.
- “Decomposing the Monolith”: “Created services based on our core nouns: Tweet service User service Timeline service DM service Social
  Graph service ....”
- “Services: Concurrency is Hard”: “Decomposing the monolith: each team took slightly different approaches to concurrency”; “Different
  failure semantics across teams: no consistent back pressure mechanism”; “Failure domains informed us of the importance of having a
  unified client/server library: deal with failure strategies and load balancing”.
- “Finagle Programming Model”: “Takes care of: service discovery, load balancing, retrying, connection pooling, stats collection,
  distributed tracing”; “Future[T]: modular, composable, async, non-blocking I/O”.
- “Datacenter: Static Partitioning”; “The evils of single tenancy and static partitioning”; “Different jobs... different utilization
  profiles...”; hình “DATACENTER STATIC PARTITIONING 33% 33% 33%”.
- “Mesos, Linux and cgroups”: “Apache Mesos: kernel of the data center”; “isolation via Linux cgroups (CPU, RAM, network, FS)”;
  “reshape clusters dynamically based on resources”. “Data Center Computing: Reduce CapEx/OpEx via efficient utilization of HW”.
- “How did it all turn out?”: “Site Success Rate Today”, hình “100% … Off the monorail … 99._% World Cup 2014 … 2006 2010”.
- “Growth Continues Today...”: “284M+ Active Users”, “500M+ Tweets per Day”, “78% Active Users are on Mobile”.
- “Lessons Learned”: “Lesson #2 Incremental change always wins — increase chance of success by making small changes — small changes add up
  with minimized risk — loosely coupled micro services work”. “Lesson #3 "Data center as a computer" is the future direction of
  infrastructure — Efficient use of hardware saves money”.

## [BD14] B. Degenhardt (Twitter), *Lessons Learned in Scaling Twitter*, QCon London 2014 (PDF)
Tải: qconlondon.com/london-2014/dl/qcon-london-2014/slides/BrianDegenhardt_RealTimeSystemsAtTwitter.pdf (curl, 39 370 797 byte).
- Trang mở: “Scalability, actually all Software Engineering can be described in how you divide a problem into components. … a well-divided
  problem is both scalable and manageable.”
- “Lessons Learned: Incrementally Implement SOA; Separate semantics from execution; Use statistics to monitor behavior”.
- “The monorail was our term for a single Rails application running on ruby 1.8.3”.
- “challenges: difficult to scale storage model; any change deploys to all servers; poor concurrency, runtime performance; leaky
  abstractions / tight-coupling”.
- Các hình chuyển dần: Monorail + MySQL → lưu trữ tách riêng “Tweets (gizzard) Users (gizzard) Timelines (redis) Social Graph (gizzard)” →
  “TFE … Monorail … Tweets (Tweetypie) … Users (Gizmoduck) … Timelines (timelineservice)”.
- “Timeline Query Statistics: >240m active users; 300k qps poll-based timelines; @1ms p50 / 4ms p99”.
- “Finagle is an extensible RPC system for the JVM, used to construct high-concurrency servers” — “service discovery, load balancing,
  retrying, thread/connection pooling, stats collection, distributed tracing”.
- “Why Stats Matter: Increased traffic velocity makes individual events less important; More vertical components requires more
  measurement”.
- “Failures are OK: 300,000rps 99.99% success rate 30 failures per second”; “Failure Rate is more informative than individual failures”.
- “Measure the Long Tail: Tail effects are cumulative; This is why request-level concurrency is important”.
- “Zipkin … Distributed Tracing System, Open Source, Modeled after Google's `Dapper' paper”.

## [ME13] M. Eriksen (Twitter), *Your Server as a Function*, bản tiền ấn phẩm ngày 2013-09-27 (PLOS 2013)
Tải: monkey.org/~marius/funsrv.pdf (curl, 163 933 byte; tiêu đề trang: “Your Server as a Function (Preprint) … 2013/9/27”).
- Mục 1: “Servers in a large-scale setting are required to process tens of thousands, if not hundreds of thousands of requests
  concurrently; they need to handle partial failures, adapt to changes in network conditions, and be tolerant of operator errors.”
- Mục 1: “Futures — The results of asynchronous operations are represented by futures which compose to express dependencies between
  operations.” “Services — Systems boundaries are represented by asynchronous functions called services.” “Filters — Application-agnostic
  concerns (e.g. timeouts, retries, authentication) are encapsulated by filters”.
- Mục 1: “Finagle and its accompanying structuring idioms are used throughout the entire Twitter service stack—from frontend web servers to
  backend data systems.” Tài liệu tham khảo [10]: “M. Eriksen and N. Kallen. Finagle. http://twitter.github.com/finagle, Nov. 2010.”
- Mục 4.3: “our frontend web servers—reverse HTTP proxies through which all of our external traffic flows—use a large stack of filters”;
  “It is quite simple to unit test each of these filters in isolation”.
- Mục 4.4: “The tail latencies of most of our servers are governed by minor heap garbage collections. … our large fan-out system amplifies
  such effects as overall request latency is governed by the slowest component; with large request distribution—often 100s of systems—
  encountering minor garbage collection in the request path is common.”

## Điều KHÔNG dạy (nguồn không ghi hoặc chưa đọc được)
- Mọi chi tiết riêng của bài blog 2013 “New Tweets per second record, and how!” (độ trễ, số máy, cách lưu tweet, ngày đăng chính xác):
  KHÔNG đọc được (403/429) → không dạy. Con số 143 199 tweet mỗi giây và tên chương trình truyền hình lấy từ slide [AN14] (“Miyazaki 2013”);
  bài chỉ nói “năm 2013”, không nói ngày.
- Năm cụ thể bắt đầu tách từng dịch vụ, năm tắt hẳn nguyên khối, số máy Rails, số kỹ sư: nguồn không ghi → không dạy. Chặng tách dịch vụ
  ghi “từ 2010”, dựa vào các mốc 2010 trong [AN14] (tìm kiếm Java 2010, FlockDB 2010) và [ME13] (Finagle, 11/2010).
- “NYE 2013: 33,338 TPS” của [AN14]: không đối chiếu được với nguồn khác → không dùng.
- Tỉ lệ thành công đúng của World Cup 2014 (slide ghi “99._%”, bị che một chữ số) → chỉ nói “gần 100%”, không nêu số.
- Mọi số máy, số yêu cầu mỗi giây của hệ người học, thời gian 10 ms mỗi lần gọi, xác suất 1% chậm: SỐ MINH HOẠ, ghi rõ.
