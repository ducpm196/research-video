# Nguồn đã đọc nguyên văn cho SEP L10 (tình huống chuyên gia: một gói nhỏ bị gỡ, 3/2016)

Đọc ngày 2026-11-02 (curl, bóc thẻ HTML; câu dưới đây chép nguyên văn). Không nêu tên cá nhân (tác giả gói, người đăng lại gói) trong
bài — bài npm có nêu tên, bài giảng thì không. Tên công ty trong tranh chấp tên gói chỉ dùng như tên gói `kik` trên màn hình.

## [N16a] npm Blog, *kik, left-pad, and npm*, 23/3/2016 (dấu thời gian trang: “March 23rd, 2016 6:21pm”)
Tải: https://blog.npmjs.org/post/141577284765/kik-left-pad-and-npm (200)
- “Earlier this week, many npm users suffered a disruption when a package that many projects depend on — directly or indirectly — was
  unpublished by its author, as part of a dispute over a package name.”
- “In a global namespace for unscoped modules, collisions are inevitable. npm has a package name dispute resolution policy for this reason.”
- “The policy’s overarching goal is this: provide npm users with the package they expect.”
- “Under our dispute policy, an existing package with a disputed name typically remains on the npm registry; the new owner of the name
  publishes their package with a breaking version number.”
- “In this case, though, without warning to developers of dependent projects, [the author] unpublished his kik package and 272 other
  packages. One of those was left-pad.”
- “This impacted many thousands of projects. Shortly after 2:30 PM (Pacific Time) on Tuesday, March 22, we began observing hundreds of
  failures per minute, as dependent projects — and their dependents, and their dependents… — all failed when requesting the
  now-unpublished package.”
- “Within ten minutes, [a community member] stepped in and published a functionally identical version of left-pad. This was possible
  because left-pad is open source, and we allow anyone to use an abandoned package name as long as they don’t use the same version numbers.”
- “[The new] left-pad was published as version 1.0.0, but we continued to observe many errors. This happened because a number of
  dependency chains, including babel and atom, were bringing it in via line-numbers, which explicitly requested 0.0.3.”
- “We conferred with [him] and took the unprecedented step of re-publishing the original 0.0.3. This required relying on a backup, since
  re-publishing isn’t otherwise possible. We announced this plan at 4:05 PM and completed the operation by 4:55 PM.”
- “The duration of the disruption was 2.5 hours.”
- “The other 272 affected modules were adopted by others in the community in a similar time. They either re-published forks of the
  original modules or created “dummy” packages to prevent malicious publishing of modules under their names.”
- “Unrestricted un-publishing caused a lot of pain.” … “we’ve hit an inflection point in the size of the community and how critical npm
  has become to the Node and front-end development communities.”
- “npm needs safeguards to keep anyone from causing so much disruption.”
- “It took us too long to get you this update.”
- “We will make it harder to un-publish a version of a package if doing so would break other packages.”
- “If a package with known dependents is completely unpublished, we’ll replace that package with a placeholder package that prevents
  immediate adoption of that name.”
- “It was abrupt unpublishing, not our resolution policy, that led to yesterday’s disruptions.”

## [N16b] npm Blog, *changes to npm’s unpublish policy*, 29/3/2016 (dấu thời gian trang: “March 29th, 2016 9:57am”)
Tải: https://blog.npmjs.org/post/141905368000/changes-to-npms-unpublish-policy (200)
- “A byproduct of being so interdependent is that a single actor can wreak significant havoc across the ecosystem. If a publisher
  unpublishes a package that others depend upon, this breaks every downstream project that depends upon it, possibly thousands of projects.”
- “If the version is less than 24 hours old, you can unpublish it.” … “If the version is older than 24 hours, then the unpublish will
  fail, with a message to contact support@npmjs.com.”
- “If you contact support, they will check to see if removing that version of your package would break any other installs. If so, we
  will not remove it.”
- “If every version of a package is removed, it will be replaced with a security placeholder package, so that the formerly used name will
  not be susceptible to malicious squatting.”
- “The policy still relies on human beings making human decisions with their human brains.” … “it will eventually reach scaling problems”
- “we must balance individual ownership with collective benefit.”
- Ghi chú đầu trang: “Note: as of January 30, 2020, the unpublish policy has been updated.”

## [N26] npm Docs, *Unpublish policy* (bản hiện hành, đọc 2026-11-02)
Tải: https://docs.npmjs.com/policies/unpublish (200)
- “Registry data is immutable, meaning once published, a package cannot change.” … “no other package can ever be published with that
  name at that version. This is true even if that package is unpublished.”
- “For newly created packages, as long as no other packages in the npm Public Registry depend on your package, you can unpublish anytime
  within the first 72 hours after publishing.”
- “Regardless of how long ago a package was published, you can unpublish a package that meets all of the following conditions: no other
  packages in the npm Public Registry depend on it; it had less than 300 downloads over the last week; it has a single owner/maintainer”

## [N26b] npm Docs, *package-lock.json* (CLI v10, đọc 2026-11-02)
Tải: https://docs.npmjs.com/cli/v10/configuring-npm/package-lock-json (200)
- “It describes the exact tree that was generated, such that subsequent installs are able to generate identical trees, regardless of
  intermediate dependency updates.”
- “This file is intended to be committed into source repositories”
- “Describe a single representation of a dependency tree such that teammates, deployments, and continuous integration are guaranteed to
  install exactly the same dependencies.”

## [ACM18] ACM Code of Ethics and Professional Conduct (2018), bản PDF acm.org (xem sources_L00.md)
- 3.6: “Use care when modifying or retiring systems.” … “Leaders should take care when changing or discontinuing support for system
  features on which people still depend.” … “Users should be notified of the risks of continued use of the unsupported system long
  before support ends.”
- 3.7: “Recognize and take special care of systems that become integrated into the infrastructure of society.” … “As the level of
  adoption changes, the ethical responsibilities of the organization or group are likely to change as well.”

## Con số dùng trong bài
- CITED: 272 gói khác + `kik` = 273 gói bị gỡ ([N16a]); “hàng trăm lỗi mỗi phút” từ khoảng 14:30 giờ Thái Bình Dương 22/3/2016;
  bản thay thế trong 10 phút; bản 1.0.0 không khớp vì chuỗi phụ thuộc yêu cầu đúng 0.0.3; công bố kế hoạch 16:05, xong 16:55;
  gián đoạn 2,5 giờ; chính sách mới 24 giờ ([N16b]); chính sách hiện hành 72 giờ, < 300 lượt tải/tuần, một người duy trì ([N26]).
- VER: 14:30 → 16:55 = 145 phút ≈ 2,4 giờ (khớp “2,5 giờ” ở mức làm tròn); 16:05 → 16:55 = 50 phút; 1 + 272 = 273.
- SỐ MINH HOẠ: chuỗi phụ thuộc 3 tầng, mỗi gói dùng 3 gói → 3 + 9 + 27 = 39 gói gián tiếp; dự án của người học 1 phụ thuộc trực tiếp.

## Suy luận của bài (INFERRED, nói rõ là lời khuyên, không gán cho nguồn)
- “Tệp khoá giúp lần cài sau ra cây y hệt, nhưng mã vẫn được tải từ kho” — suy từ [N26b] (tệp mô tả cây phụ thuộc) và [N26]
  (gỡ đăng làm phiên bản không còn trong kho); lời khuyên “bản sao nội bộ” là thực hành của bài, không phải câu của nguồn.

## Điều KHÔNG dạy (nguồn không ghi)
- “left-pad chỉ có 11 dòng” — không có trong [N16a], [N16b]; không dạy (giáo án fix).
- Số dự án bị ảnh hưởng chính xác (nguồn chỉ ghi “many thousands of projects”) và tên các công ty bị ảnh hưởng ngoài hai chuỗi
  babel, atom mà nguồn nêu — không dạy thêm.
- Không bàn đúng sai của tranh chấp nhãn hiệu: nguồn ghi “This incident did not arise because of intellectual property law.”
