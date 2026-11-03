# Nguồn đã đọc nguyên văn cho CAS L10 (Google Flu Trends)

Đọc ngày 2026-11-02. Chỉ trích các câu bài giảng dựa vào (CITED). Mô phỏng khớp quá mức (alg.cas_spurious_fit, seed 0, chuỗi 20 tuần
alg.CAS_FLU), sai số phần trăm 2% / 4,2%, các tỉ lệ 52%, 25%, 92,6%, xác suất nhị thức, quiz: SỐ MINH HOẠ hoặc VER (`checks`,
`audit/cas/ver/L10.py`, `audit/verify_plan_curricula.py` CAS:L10).

## [LZ14] D. Lazer, R. Kennedy, G. King, A. Vespignani, *The Parable of Google Flu: Traps in Big Data Analysis*, Science 343, 14/3/2014, tr. 1203–1205
Bản đọc: **bản tác giả** trên trang của đồng tác giả G. King (Harvard): https://gking.harvard.edu/files/gking/files/0314policyforumff.pdf
(HTTP 200, 1 267 036 byte; pdftotext). Trang ghi “www.sciencemag.org SCIENCE VOL 343 14 MARCH 2014 1203”. Bản trên science.org không thử
(trang thường chặn tải tự động); nội dung dạy chỉ lấy từ bản tác giả này.
- “In February 2013, Google Flu Trends (GFT) made headlines … Nature reported that GFT was predicting more than double the proportion of doctor
  visits for influenza-like illness (ILI) than the Centers for Disease Control and Prevention (CDC), which bases its estimates on surveillance
  reports from laboratories across the United States … This happened despite the fact that GFT was built to predict CDC reports.”
- “We explore two issues that contributed to GFT's mistakes-- big data hubris and algorithm dynamics”.
- “"Big data hubris" is the often implicit assumption that big data are a substitute for, rather than a supplement to, traditional data
  collection and analysis.” “quantity of data does not mean that one can ignore foundational issues of measurement and construct validity and
  reliability and dependencies among data”.
- “the methodology was to find the best matches among 50 million search terms to fit 1152 data points”. “GFT developers, in fact, report weeding
  out seasonal search terms unrelated to the flu but strongly correlated to the CDC data, such as those regarding high school basketball … This
  should have been a warning that the big data were overfitting the small number of cases”. “the initial version of GFT was part flu detector,
  part winter detector.”
- “GFT engineers updated the algorithm in 2009, and this model has run ever since, with a few changes announced in October 2013”.
- “GFT also missed by a very large margin in the 2011–2012 flu season and has missed high for 100 out of 108 weeks starting with August 2011”.
  Chú thích hình: “overshot the actual level in 2011–2012 by more than 50%. From 21 August 2011 to 1 September 2013, GFT reported overly high flu
  prevalence 100 out of 108 weeks.” Sai số: “Error [as a percentage {[Non-CDC estimate)(CDC estimate)]/(CDC) estimate)}”.
- “last week's errors predict this week's errors (temporal autocorrelation), and the direction and magnitude of error varies with the time of
  year (seasonality).”
- “a fairly simple projection forward using already available (typically on a 2-week lag) CDC data”. “Even 3-week-old CDC data do a better job of
  projecting current flu prevalence than GFT”.
- “by combining GFT and lagged CDC data, as well as dynamically recalibrating GFT, we can substantially improve on the performance of GFT or the
  CDC alone”.
- “Mean absolute error (MAE) during the out-of-sample period is 0.486 for GFT, 0.311 for lagged CDC, and 0.232 for combined GFT and CDC.”
- “Algorithm dynamics are the changes made by engineers to improve the commercial service and by consumers in using that service.”
- “The most common explanation for GFT's error is a media-stoked panic last flu season … Although this may have been a factor, it cannot explain
  why GFT has been missing high by wide margins for more than 2 years.” “A more likely culprit is changes made by Google's search algorithm
  itself.” “the official Google search blog reported 86 changes in June and July 2012 alone”.
- “GFT has never documented the 45 search terms used, and the examples that have been released appear misleading”.

## Sai sót / bổ sung giáo án
- `example` khớp nguồn (“more than double”, “more than 50%”). Bổ sung `fix`: số MAE 0,486 / 0,311 / 0,232 (CITED) và 52% (VER CAS:L10 cập
  nhật); và ghi rõ bài báo KHÔNG coi “hoảng loạn truyền thông” là nguyên nhân chính.
- `objectives` nói “trôi khái niệm khi hành vi tìm kiếm đổi”: bài báo dùng chữ “algorithm dynamics” (kỹ sư đổi dịch vụ + người dùng đổi cách
  dùng) và “overfitting”; bài giảng dùng đúng hai ý đó, nối với khái niệm trôi khái niệm của khoá MLO.

## Điều KHÔNG dạy
- Danh sách 45 cụm từ (không được công bố), cụm từ “bóng rổ” cụ thể: không dạy ngoài câu của bài báo.
- Số liệu % ILI cụ thể từng tuần: bài không đọc từ hình → chỉ dùng số minh hoạ 2% / 4,2% và chuỗi mô phỏng, ghi rõ.
- Việc Google ngừng dịch vụ (sau năm 2014): không có trong nguồn đã đọc → không nói.
