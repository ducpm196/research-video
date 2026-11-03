# Nguồn đã đọc nguyên văn cho MLO L14 (bài hành trình: từ nợ kỹ thuật của hệ ML tới nền tảng học máy)

Đọc ngày 2026-11-02 (curl tải PDF chính thức + `pdftotext`, đọc toàn văn). Chỉ trích các câu bài giảng dựa vào (CITED); mọi con số khác
trong bài là phép tính lại (VER, `checks` của bài, `audit/mlo/verify_mlo.py` L14, `audit/verify_plan_curricula.py` MLO:L14) hoặc ghi rõ
“(số minh hoạ)”. Không nêu tên cá nhân trong lời đọc; tên tác giả chỉ ở `source:`.

Đối chiếu ROADMAP §8.1 mục 3 (ứng viên NOT_VERIFIED: Sculley và cộng sự, NeurIPS 2015; Baylor và cộng sự, KDD 2017): cả hai ĐÃ đọc toàn văn.
Thêm chặng đầu và chặng cuối từ bài nhìn lại của chính đội TFX (arXiv 2020), vì bài đó kể lại cả hành trình Sibyl 2007 → TFX 2020.

## [SC15] D. Sculley và cộng sự (Google), *Hidden Technical Debt in Machine Learning Systems*, NIPS 2015 (nay gọi NeurIPS)
Tải: papers.nips.cc/paper_files/paper/2015/file/86df7dcfd896fcaf2674f757a2463eba-Paper.pdf (PDF 9 trang, 165 614 byte).
- Tóm tắt: “Using the software engineering framework of technical debt, we find it is common to incur massive ongoing maintenance costs in
  real-world ML systems.”
- §1: “developing and deploying ML systems is relatively fast and cheap, but maintaining them over time is difficult and expensive.”
- §1: “Not all debt is bad, but all debt needs to be serviced.” “Hidden debt is dangerous because it compounds silently.”
- §2 Entanglement: “If we change the input distribution of values in x1, the importance, weights, or use of the remaining n − 1 features may
  all change. … No inputs are ever really independent. We refer to this here as the CACE principle: Changing Anything Changes Everything.”
- §2 Undeclared Consumers: “Without access controls, some of these consumers may be undeclared, silently using the output of a given model as
  an input to another system.” “In the absence of barriers, engineers will naturally use the most convenient signal at hand, especially when
  working against deadline pressures.”
- §3 Unstable Data Dependencies: “a silent update that corrects the signal will have sudden ramifications for the model.” “One common
  mitigation strategy for unstable data dependencies is to create a versioned copy of a given signal.” “Versioning carries its own costs,
  however, such as potential staleness and the cost to maintain multiple versions of the same signal over time.”
- §3 Underutilized: “Underutilized dependencies can be detected via exhaustive leave-one-feature-out evaluations. These should be run
  regularly to identify and remove unnecessary features.” (ε-Features:) “it is tempting to improve model accuracy even when the accuracy gain
  is very small or when the complexity overhead might be high.”
- §5 (Figure 1): “Only a small fraction of real-world ML systems is composed of the ML code … The required surrounding infrastructure is vast
  and complex.” (Hình là ảnh; nhãn các khối KHÔNG trích được → bài không chép nhãn.)
- §5 Glue Code: “Because a mature system might end up being (at most) 5% machine learning code and (at least) 95% glue code, it may be less
  costly to create a clean native solution rather than re-use a generic package.” “An important strategy for combating glue-code is to wrap
  black-box packages into common API's.”
- §5 Pipeline Jungles: “the resulting system for preparing data in an ML-friendly format may become a jungle of scrapes, joins, and sampling
  steps, often with intermediate files output.”
- §5 Dead Experimental Codepaths: “A famous example of the dangers here was Knight Capital's system losing $465 million in 45 minutes,
  apparently because of unexpected behavior from obsolete experimental codepaths [15].” ([15] = thông cáo của SEC năm 2013.)
  “it is often beneficial to periodically reexamine each experimental branch to see what can be ripped out.”
- §6 Configuration Debt: “In a mature system which is being actively developed, the number of lines of configuration can far exceed the
  number of lines of the traditional code.” Nguyên tắc: “Configurations should undergo a full code review and be checked into a repository.”
- §7 Monitoring: “Prediction Bias. In a system that is working as intended, it should usually be the case that the distribution of predicted
  labels is equal to the distribution of observed labels.” “Action Limits … If the system hits a limit for a given action, automated alerts
  should fire and trigger manual intervention or investigation.”
- §8 Process Management Debt: “mature systems may have dozens or hundreds of models running simultaneously”.
- §8 Cultural Debt: “It is important to create team cultures that reward deletion of features, reduction of complexity, improvements in
  reproducibility, stability, and monitoring to the same degree that improvements in accuracy are valued.”
- §9: “Research solutions that provide a tiny accuracy benefit at the cost of massive increases in system complexity are rarely wise
  practice.” “Even the addition of one or two seemingly innocuous data dependencies can slow further progress.”
- Cuối bài: “A short version of this paper was presented at the SE4ML workshop in 2014 in Montreal, Canada.”

## [TX17] D. Baylor và cộng sự (Google), *TFX: A TensorFlow-Based Production-Scale Machine Learning Platform*, KDD 2017, tr. 1387–1395
Tải: storage.googleapis.com/gweb-research2023-media/pubtools/4795.pdf (bản PDF trên trang research.google của bài; ACM DL trả trang HTML
chặn tải, trang kdd.org trả tệp rỗng). DOI 10.1145/3097983.3098021.
- Tóm tắt: “such orchestration is often done ad hoc using glue code and custom scripts developed by individual teams for specific use cases,
  leading to duplicated effort and fragile systems with high technical debt.”
- Tóm tắt: “we were able to standardize the components, simplify the platform configuration, and reduce the time to production from the
  order of months to weeks”.
- Tóm tắt: “Deploying TFX led to reduced custom code, faster experiment cycles, and a 2% increase in app installs resulting from improved
  data and model analysis.”
- §1: “Google Play, a commercial mobile app store with over one billion active users and over one million apps”.
- §2.2: “training data that accidentally includes the label will lead to a good quality model that passes validation, but would not perform
  well in production where the label is not available.”
- §2.2: “Integrating these components ensures consistency across the pipeline and guarantees that the same transformations are applied at
  training and serving, which in turn prevents one form of training-serving skew”.
- §3: “anomalies in the data not an exception, but more the norm.” “Our experience has shown that users tend to switch off data-quality
  checks if they receive a large number of false-negative alerts or if the alerts are hard to understand.” (bài nói “quá nhiều cảnh báo,
  hoặc cảnh báo khó hiểu” — không dịch cụm “false-negative”.)
- §3.2: “TFX exports any data transformations as part of the trained model, which in turn avoids problems with inconsistency.”
- §3.3: “the component relies on a schema that provides a versioned, succinct description of the expected properties of the data.”
  “In some cases the anomalies correspond to a natural evolution of the data, and the appropriate action is to change the schema (rather than
  fix the data).” “we allow anomalies to be filed just like any software bug where they are documented, tracked, and eventually resolved.”
- §4.1: “huge training datasets (O(100B) data points) which may take hours (or days in some cases) of training … This results in a trade-off
  between model quality and model freshness.” Warm-starting: “we initialize (or warm-start) the parameters corresponding to these features
  from the previously trained version of the network and fine tune them”.
- §5.3: “We validate that a model is safe to serve with a simple canary process. We evaluate prediction quality by comparing the model
  quality against a fixed threshold as well as against a baseline model (e.g., the current production model). Any new model failing any of
  these checks is not pushed to serving, and product teams are alerted.”
- §5.3: “most bugs cause dramatic changes to model quality metrics that can be caught by using loose thresholds. However, there is a strong
  selection bias here, since more subtle issues may not have drawn our attention.”
- §5.4: “metrics on the entire dataset can fail to reflect the performance on these small slices”.
- §5.5: “no product teams actively requested the validation function when the component was first built, and when the feature was
  explained to them, few activated it.” “encountering a real issue in production which could have been prevented by validation made the
  value of the validation apparent to the teams … we plan to provide a configuration-free validation setup that is enabled by default”.
- §6.1: “we observed latency peaks during the interval when the system was loading a new model”. “setting the threadpool size for
  model-loading operations to 1 or 2 was ideal”. “the 99.9-percentile inference request latency measured during loads was in the range of
  ∼500 to ∼1500 msec. However, with the specification of a separate threadpool, the 99.9-percentile inference request latency during loads
  reduced to a range of ∼75 to ∼150 msec.”
- §7: “The typical training dataset size is hundreds of billions of examples”. “collectively serve thousands of queries per second with a
  strict latency requirement of tens of milliseconds. Due to fresh models being trained daily, the servers have to reload multiple models”.
- §7: “Google Play discovered a few features that were always missing from the logs, but always present in training. The results of an
  online A/B experiment showed that removing this skew improved the app install rate on the main landing page of the app store by 2%.”
- §7: “Training from scratch can take several days to converge to a high-quality model”. “The model validation component tests the new
  model against the production model, preventing issues like accidentally pushing partially-trained models to serving because of system
  failures.”

## [TH20] K. Katsiapis và cộng sự (Google), *Towards ML Engineering: A Brief History Of TensorFlow Extended (TFX)*, arXiv:2010.02013, 2020
Tải: arxiv.org/pdf/2010.02013 (PDF 16 trang, 492 477 byte).
- “We discovered early on from our endeavors to apply ML in production that while ML algorithms are important, they are usually insufficient
  in realizing the successful application of ML in a product [4].” ([4] = bài SE4ML 2014 “high interest credit card of technical debt”.)
- Sibyl (2007 - 2020): “Sibyl [2], founded in 2007, was a platform that enabled massive-scale ML, catered to production use.” “on top of
  “wide” models (linear, logistic, poisson regression and later factorization machines)”. “Sibyl also offered tools for several aspects of
  the ML workflow including Data Ingestion, Data Analysis and Validation, Training (of course), Model Analysis, and Training-Serving Skew
  Detection. All these were packaged as a single integrated product”. “It was in production for ~14 years, and the vast majority of its
  workloads migrated to TFX.”
- TFX (2017 - ?): “While TensorFlow offered flexibility, it lacked a complete end-to-end production system. On the other hand, Sibyl had
  robust end-to-end capabilities, but lacked flexibility.” “in 2017, nearly a decade after the birth of Sibyl, we launched TFX within Google.”
- “In the 3 years since its launch … TFX is used by thousands of users within Alphabet, and it powers hundreds of popular Alphabet products
  … On any given day there are thousands of TFX pipelines running, which are processing exabytes of data and producing tens of thousands of
  models, which in turn are performing hundreds of millions of inferences per second.”
- “the public TFX offering [3] was released in early 2019 and widely adopted in under a year”.
- Rules of ML, “a common evolution”: “Start with simple rules and heuristics, and generate data to learn from”; “Move to simple ML (i.e.,
  simple models) and realize large gains; this is usually the entry point for introduction of ML pipelines”; “Move to ML with more features
  and more advanced models to realize decent gains”; “Move to state-of-the-art ML, manage refinement and complexity (for solutions to the
  problems that are worth it), and realize small gains”; “bearing in mind return on investment (and diminishing returns).”
- “artifacts are first class citizens in ML, on par with the processes that produce and consume them.”
- Data: “setting explicit expectations on the form of the data (including its schema, invariants and value distributions) … can … make the
  data trustworthy enough to train models on”.
- Artifact Lineage: “Much like how stack traces are invaluable for identifying root causes of defects in software programs, the lineage of
  all artifacts produced and consumed by an ML pipeline is invaluable for identifying root causes of defects in ML models.”
- Continuous training: “the pipeline detects the presence of new data and automatically schedules the generation of updated models.”
  Backfilling: “rerun the pipeline on existing artifacts but using updated versions of the components”. “TFX was built from the ground up in a
  way that enables continuous learning (and unlearning) … these advanced capabilities also allow it to be used in a “one-shot”,
  discontinuous, fashion.”
- Dependencies: “We have found that taking dependencies requires effort that is super-linear to the number of dependencies.”
- Interoperability: “TFX leverages Apache Beam [13] to execute on Apache Flink [31] and Apache Spark [32] clusters as well as serverless
  offerings like Google Cloud Dataflow [33].” “provides orchestration options on top of Apache Airflow [22], Apache Beam [22], Kubeflow
  Pipelines [22] … MLMD itself works with several relational databases like SQLite [34] and MySQL [35].” “The combination of multiple
  technology stacks can lead to an exponential number of distinct deployment configurations.”
  (Bài đếm 3 bộ chạy × 3 bộ điều phối × 2 cơ sở dữ liệu siêu dữ liệu = 18 tổ hợp từ đúng các tên này — phép đếm là VER, nguồn không ghi “18”.)
- Portability: “maintaining a portable core with environment-specific and device-specific specialization requires effort that is
  super-linear to the number of environments / devices.” Layering: “roughly linear to the number of layers”.
- Where We Are Going (2020): “auto-detecting surprising model behavior on multidimensional slices, facilitating automatic production of Model
  Cards [67, 68] and improving our training-serving skew detection capabilities.” “we will make an effort to distinguish the battle-tested
  from the experimental aspects of our technology”.

## Điều KHÔNG dạy (nguồn không ghi)
- Nhãn các khối trong Hình 1 của [SC15] (ảnh, không trích được chữ): không chép; bài vẽ thanh tỉ lệ 5/95 tính lại.
- Chi tiết sự cố Knight Capital ngoài câu của [SC15] (năm, cơ chế, số lệnh): không đọc thông cáo SEC 2013 trong phiên này → chỉ dạy câu
  “465 triệu USD trong 45 phút, có vẻ do nhánh mã thử nghiệm cũ”, giữ chữ “có vẻ” (“apparently”); tên công ty chỉ trên màn hình.
- “2%” của [TX17]: nguồn ghi “increase in app installs” và “improved the app install rate … by 2%”; không ghi là 2% tương đối hay 2 điểm
  phần trăm của tỉ lệ cài. Bài dùng câu tóm tắt (“tăng 2% lượt cài”) với 1 000 000 lượt cài là SỐ MINH HOẠ; không dạy tỉ lệ cài gốc.
- Thời gian từ “tháng” xuống “tuần” cụ thể bao nhiêu: [TX17] chỉ ghi “from the order of months to weeks” → không đổi ra số.
- Số người, số mô hình của Sibyl; Sibyl dùng ở sản phẩm nào: [TH20] chỉ ghi “one of the most widely used” → không dạy.
- Năm ra đời Rules of ML: [TH20] chỉ dẫn trang web → không dạy năm; bài dạy “chuỗi tiến hoá” như bài học đội tổng kết năm 2020.
- Các mức lợi ích của từng giai đoạn (70% → 78% → 81% → 81,5%), số tuần công, hệ 100 000 dòng, 20 đặc trưng, đội 3 người, 1 000 000 lượt cài:
  SỐ MINH HOẠ, ghi rõ trên màn hình.
- Những gì xảy ra với TFX sau 2020 (phát hành mới, tỉ lệ dùng): không đọc trong phiên này → chặng cuối dừng ở kế hoạch đội viết năm 2020.
