# Nguồn đã đọc nguyên văn cho SDP L17 (bài hành trình: Shopify, từ nguyên khối tới nguyên khối mô-đun hoá)

Đọc ngày 2026-11-02 bằng curl (tách chữ từ HTML của shopify.engineering; nội dung bài nằm trong thẻ `<article>`), đối chiếu bằng
WebFetch cho [UD20]. Chỉ trích các câu bài giảng dựa vào (CITED); mọi con số khác trong bài là phép tính lại (VER, `checks` của bài,
`audit/sdp/verify_sdp.py` L17, `audit/verify_plan_curricula.py` SDP:L17) hoặc ghi rõ “(số minh hoạ)”. Không nêu tên cá nhân trong lời
đọc; tên tác giả chỉ ở `source:`.

Nguồn ứng viên của ROADMAP §8.1 mục 3 (Shopify Engineering 2019 “Deconstructing the Monolith”) ĐỌC ĐƯỢC và khớp; thêm ba bài tiếp nối
chính thức của chính đội Shopify (2020, 2020, 2024) để có chặng “ổn định và tiếp tục phát triển”.

## [DM19] K. Westeinde, *Deconstructing the Monolith: Designing Software that Maximizes Developer Productivity*, Shopify Engineering, 2019-02-21
URL: https://shopify.engineering/deconstructing-monolith-designing-software-maximizes-developer-productivity (curl, 265 084 byte;
`datePublished` 2019-02-21).
- Mở bài: “Shopify is one of the largest Ruby on Rails codebases in existence. It has been worked on for over a decade by more than a
  thousand developers.” “It was initially built as a monolith, meaning that all of these distinct functionalities were built into the same
  codebase with no boundaries between them.”
- “We chose to evolve Shopify into a modular monolith, meaning that we would keep all of the code in one codebase, but ensure that
  boundaries were defined and respected between different components.”
- “the code that handled calculating shipping rates lived alongside the code that handled checkouts, and there was very little stopping
  them from calling each other. Over time, this resulted in extremely high coupling”.
- Lợi ích của nguyên khối: “You’ll only need to maintain one repository … only having to maintain one test and deployment pipeline”;
  “you can call into different components directly, rather than needing to communicate over web service API’s. This means you don’t have to
  worry about API version management and backward compatibility”.
- Điểm nghẽn: “if an application reaches a certain scale or the team building it reaches a certain scale, it will eventually outgrow
  monolithic architecture. This occurred at Shopify in 2016”. “Making a seemingly innocuous change could trigger a cascade of unrelated test
  failures. For example, if the code that calculates our shipping rate called into the code that calculates tax rates, then making changes
  to how we calculate tax rates could affect the outcome of shipping rate calculations”; “tests that were difficult to write, and very slow
  to run on CI.” “a new developer who joined the shipping team … would also need to understand how orders are created, how we process
  payments, and much more since everything was so intertwined.”
- Vi dịch vụ: “We’d have to maintain multiple different test & deployment pipelines and take on infrastructural overhead for each service …
  communicating between services means crossing the network, which adds latency and decreases reliability with every call.” “We wanted a
  solution that increased modularity without increasing the number of deployment units”.
- “a survey was sent out to all the developers working in our core system to identify the main pain points. … we wanted to be
  data-informed when coming up with a solution”. “In early 2017, a small but mighty team was put together to tackle this. The project was
  initially named “Break-Core-Up-Into-Multiple-Pieces”, and eventually evolved into “Componentization”.”
- “our code was organized like a typical Rails application: by software concepts (models, views, controllers). The goal was to re-organize
  it by real-world concepts (like orders, shipping, inventory, and billing)”.
- “We did this by listing every ruby class (around 6000 in total) in a massive spreadsheet and manually labeling which component it belongs
  in. Even though no code changed in this process, it still touched the entire codebase … We achieved this move in one big bang PR built by
  automated scripts.” “Our codebase is well tested, so by running our tests locally and in CI without failures … we were able to ensure that
  nothing was missed.” “we lost a lot of our Git history in Github when file moves were incorrectly tracked as deletions and creations”.
- “Each component defined a clean dedicated interface with domain boundaries expressed through a public API and took exclusive ownership of
  its associated data.”
- Wedge: “We developed a tool called Wedge in-house, which tracks the progress of each component towards its goal of isolation. … we wrote a
  tool to hook into Ruby tracepoints during CI to get a full call graph.” “Cross-component associations are always violating
  componentization”; “Calls are ok only to things that are explicitly public”. “Wedge then computes an overall score as well as lists
  violations per component.”
- “we had a legacy tax engine … Before the efforts described in this post, it would have been an almost impossible task to swap out the old
  system for a new one. However, since we had put so much effort into isolating dependencies, we were able to swap out our tax engine”.
- Kết: “no architecture is often the best architecture in the early days of a system.” “Once the speed at which you can add features and
  functionality begins to slow down, that’s when it’s time to invest in good design.” “Designing a complex system of microservices before you
  have domain expertise is a risky move”.

## [UD20] P. Müller, *Under Deconstruction: The State of Shopify’s Monolith*, Shopify Engineering, 2020-09-16
URL: https://shopify.engineering/shopify-monolith (curl, 327 003 byte; `datePublished` 2020-09-16; WebFetch đối chiếu).
- “Shopify’s core monolith has over 2.8 million lines of Ruby code and 500,000 commits.”
- “over three years ago, Shopify founded a team to investigate how to make our Rails monoliths more modular.” Tầm nhìn: “Instead of running
  the test suite on the whole application, we can run it on the smaller subset of components affected by a change”; “developers should feel
  like they are working on a much smaller app than they actually are.”
- “We generally stand by the original ideas as described in Deconstructing the Monolith, but almost all of the details have changed.”
- “under continuous development since at least 2006, with hundreds of developers currently adding features.”
- “A single centralized team can’t make change happen by working against the momentum of hundreds of developers adding features.” “making a
  fundamental architecture change to a system that’s being actively worked on is in large part a people problem.”
- Mô hình hành vi (Fogg): “for a behavior to occur, three things need to be in place: Ability, Motivation, and Prompt.”
- “we invested quite a bit of time and energy into developing patterns … We then pushed developers to use these patterns everywhere. In
  hindsight, this strategy didn’t increase developer ability or motivation.” “they lead developers to redefine their problem to fit the
  solution we provided, which degraded the overall state of the monolith.”
- “Currently, the Architecture Guild has ~400 members and 54 documented meetups”. “If I were to start a similar effort again today, I’d
  establish a forum like this from the beginning”.
- “When we started analyzing the graph of dependencies between components, it was very dense, to the point that every component depended on
  over half of all the other components. We also had lots of circular dependencies.” “Changes to any component in a cycle can break all other
  components in the cycle.”
- “almost everything depends on the Shop class. That means that if we want to avoid circular dependencies, the Shop class can depend on
  almost nothing.” “We can make arrows point in different directions, by either moving responsibilities into the component that depends on
  them or applying inversion of control. … This can be done for example through a publish/subscribe mechanism”.
- Lớp: “we think about the components grouped into layers. This allows us to prioritize and focus on cleaning up dependencies across layers
  first.” (platform → supporting → frontend).
- “At first, we solely focused on decoupling components from each other. … it still left us with cohesive parts of the codebase that spanned
  across component boundaries.” “Change Locality: The degree to which code that changes together lives together.” “The number of components
  touched should go down over time.”
- Nguyên lý gói: “Classes that change together are packaged together.” “Depend in the direction of stability.” “Abstractness increases with
  stability.”
- Wedge: “It logged all method calls during test suite execution on CI … We found the results produced were often not useful. Call graph
  logging produces a lot of data … it took over an hour to run, which doesn’t make for a useful feedback cycle.”
- Packwerk: “a new tool called Packwerk to analyze static constant references. … Packwerk runs a full analysis on our largest codebase in a
  few minutes, so we’re able to integrate it with our Pull Request workflow. This allows us to reject changes that break the dependency graph
  or component encapsulation before they get merged into our main branch.”
- “In my experience, all large architecture changes end up in an incomplete state. … So choose an approach based on which intermediary state
  is most useful for your specific situation.”
- “We currently have 37 components in our main monolith, each with public entrypoints covering large parts of its responsibilities. Packwerk
  is used on about a third of the components”. “Total acyclicity is the long term goal, but the more edges we can remove from the graph in the
  short term the easier the system will be to reason about.”
- Tách dịch vụ có lý do: “we split out storefront rendering because it’s a read-only use case with very high throughput … Credit card
  vaulting is a separate service because it processes sensitive data that shouldn’t flow through other parts of the system.” “splitting a
  single monolithic application into a distributed system of services increases the overall complexity considerably.”
- “The long term vision is to have separate, isolated test suites for most of the components of our main monolith.”

## [PW20] M. Ong, *Enforcing Modularity in Rails Apps with Packwerk*, Shopify Engineering, 2020-09 (`datePublished` 2020-09-23; buổi giới thiệu 2020-09-30)
URL: https://shopify.engineering/enforcing-modularity-rails-apps-packwerk (curl, 290 150 byte).
- “Packwerk is an open source static analysis tool used to enforce boundaries between groups of Ruby files we call packages.”
- “The componentization effort was a great first step … but we are still far from a modular codebase—we need walls. Cross-component calls
  are still being made, and Active Record models are shared across domains. There’s no wall imposing those boundaries, just an agreed upon
  social contract that can be easily broken.”
- “Distributing code over multiple machines is a topology change, not an architectural change. … A poorly designed API within the monolith
  will still be a poorly designed API within a service, but now with additional complexities.”
- “There are two violations that Packwerk enforces: dependency and privacy.”
- “If packages depend on each other in a cycle, making a change to one package will create a domino effect and force a change on all
  packages in the cycle.”
- “We also included this in Shopify’s CI pipeline to prevent any new violations from being merged into the main branch of the codebase.”
- “we want to stop the bleeding and prevent new violations from being added to the codebase. … This is done by generating a deprecated
  references list for the package.” “we essentially have a to-do list that can be worked off.”
- “If a constant is not autoloaded, Packwerk ignores it. This ensures that the results produced by Packwerk won’t have any false positives,
  but it can create false negatives.”
- “There was no formal push for the adoption of Packwerk within Shopify.”
- “Currently Packwerk runs in six Rails applications at Shopify, including the core monolith. Within the core codebase, we have 48 packages
  with 30 boundary enforcements within those packages.”

## [PR24] C. Salzberg và cộng sự, *A Packwerk Retrospective*, Rails at Scale 2024-01-26; đăng lại Shopify Engineering 2024-02-07
URL: https://shopify.engineering/a-packwerk-retrospective (curl, 286 072 byte; `datePublished` 2024-02-07; trang ghi “originally posted on
the Rails at Scale blog”); bản gốc https://railsatscale.com/2024-01-26-a-packwerk-retrospective/ (ngày 2024-01-26).
- “In September, 2020, our team at Shopify released a Ruby gem named Packwerk”.
- “Violations can be temporarily “allowed” via todo files (package_todo.yml); this makes it possible to “declare bankruptcy” in a codebase by
  generating a todo file for existing violations and using Packwerk to prevent new ones from creeping in.”
- Kiểm riêng tư: “privacy checks had transformed Packwerk into something it was never intended to be: an API design tool.” “we ended up with
  endless poorly-documented public code that was never meant to be public in the first place.” “privacy checks were removed from Packwerk
  with the release of version 3.0.”
- “developers tend to group code into packages based strongly on semantic clues that in many cases have little relation to how the code
  actually runs.” (ví dụ mô hình “shop billing settings” — chuyển xuống đáy đồ thị).
- “a package that is well-defined according to Packwerk (has no violations left to resolve) may actually crash with name errors when its
  code is executed.”
- Platform Essentials: “We achieved our goal of an isolated base package with zero violations and zero dependencies. … We relied heavily on
  inversion of control … These changes introduced indirection that, while resolving the violations, often made code harder to understand.”
- “we were likely the first Packwerk user to completely work through an entire package todo file, years after its initial release. This
  confirmed our suspicion that the rate at which Packwerk was identifying problems to its users vastly outpaced their capacity to actually
  fix them”.
- “we then attempted to actually run it by booting the monolith with only its code loaded. Unsurprisingly … this did not work.” “With boot
  working, we went a step further and created a CI step to run tests for the package’s code in isolation. This surfaced yet more issues”.
- “our effort to reach full isolation had taken many months of hard work.” “We implemented checks in CI to ensure our progress would never be
  reversed.”
- “Components were created many years ago by sorting thousands of files into a couple dozen buckets, each representing its own domain of
  commerce.” “running Packwerk on the codebase … generated monstrously large todo files for every component. With every new feature added,
  these todo files grew larger.”
- “our solution to this has been to use components as top-level organizational tools for grouping one or more packages … teams can still
  own domains, while individual packages act as the truly modular code units.”
- “running code, more than any metric, will always be the best indicator of real progress.” “Always ask yourself if the violation is an
  error at the developer level, or at the dependency graph level.”
- “We have discussed removing Packwerk from our monolith … Packwerk has however provided value in holding the line against new dependencies at
  the base layer of our application.” “While no longer as central as it once was, Packwerk still plays a role at Shopify”.

## Điều KHÔNG dạy (nguồn không ghi)
- Số dòng mã, số lập trình viên theo từng năm 2006–2016: nguồn chỉ ghi “since at least 2006”, “over a decade”, “more than a thousand
  developers” (2019), “hundreds of developers currently” (2020). Không dạy đường cong tăng trưởng.
- Số thành phần ban đầu năm 2017: [DM19] không ghi; [PR24] chỉ ghi “a couple dozen buckets”. Bài chỉ dùng 37 (năm 2020, [UD20]).
- Thời gian thật để dán nhãn 6000 lớp, thời gian chạy kiểm thử trên CI: không có. “1 phút mỗi lớp”, “5 phút” cho “a few minutes”, đồ thị
  10 miền, nhóm 6 người là SỐ MINH HOẠ.
- 37 thành phần × “over half” chỉ cho CẬN DƯỚI số mũi tên (≥ 19 mỗi thành phần) nếu áp cho 37 — [UD20] không ghi số thành phần lúc bắt đầu
  phân tích; bài ghi rõ là phép tính minh hoạ với 37.
- Số thành phần cụ thể dùng Packwerk: [UD20] ghi “about a third” → bài nói “khoảng một phần ba, cỡ 12”, không nói con số chính xác.
- Ngày phát hành Packwerk 3.0: [PR24] không ghi → không dạy năm của bản 3.0.
- Số vi phạm trong tệp việc cần làm, tốc độ giảm vi phạm: không có → không dạy.
- Kubernetes, vi dịch vụ của công ty khác, Twitter: không thuộc nguồn này.
