# Nguồn đã đọc nguyên văn cho AGT L12 (bài hành trình: tác tử dùng công cụ, 2022 → 2025)

Đọc ngày 2026-11-02. Trang tóm tắt arXiv tải bằng curl (export.arxiv.org/abs/…), toàn văn tải bản PDF chính thức trên arXiv rồi trích
bằng `pdftotext -layout` (bảng bị xô cột thì đọc lại bằng `pdftotext` không bố cục và đối chiếu với câu trong thân bài). Chỉ trích các
câu bài giảng dựa vào (CITED); mọi con số khác trong bài là phép tính lại (VER: `checks` của bài, `audit/agt/verify_agt.py` L12,
`audit/verify_plan_curricula.py` AGT:L12) hoặc ghi rõ “(số minh hoạ)”. Tên tác giả chỉ ở `source:`; lời đọc gọi tên nhóm và năm.
An ninh (chèn lời nhắc gián tiếp) chỉ ở mức khái niệm phòng thủ, không có chuỗi khai thác.

Thứ tự theo ROADMAP §8.1 mục 3 (ReAct → Toolformer → SWE-bench), thêm hai chặng sau từ nguồn chính thức đọc được: SWE-agent
(NeurIPS 2024, chính nhóm làm SWE-bench) và trang chính thức swebench.com (Verified, Bash Only, tin 2024–2025).

## [RE23] S. Yao và cộng sự, *ReAct: Synergizing Reasoning and Acting in Language Models*, ICLR 2023 (arXiv 2210.03629)
Tải: export.arxiv.org/abs/2210.03629 và arxiv.org/pdf/2210.03629v3. Lịch sử: v1 6/10/2022; v3 10/3/2023, ghi chú tác giả “v3 is the ICLR
camera ready version”. Đầu trang PDF: “Published as a conference paper at ICLR 2023”.
- Tóm tắt: “we explore the use of LLMs to generate both reasoning traces and task-specific actions in an interleaved manner … reasoning traces
  help the model induce, track, and update action plans as well as handle exceptions, while actions allow it to interface with external
  sources, such as knowledge bases or environments, to gather additional information.”
- Tóm tắt: “ReAct overcomes issues of hallucination and error propagation prevalent in chain-of-thought reasoning by interacting with a simple
  Wikipedia API”. “On two interactive decision making benchmarks (ALFWorld and WebShop), ReAct outperforms imitation and reinforcement
  learning methods by an absolute success rate of 34% and 10% respectively, while being prompted with only one or two in-context examples.”
- §3.1 Action Space: “(1) search[entity], which returns the first 5 sentences from the corresponding entity wiki page if it exists, or else
  suggests top-5 similar entities … (2) lookup[string], which would return the next sentence in the page containing string, simulating
  Ctrl+F … (3) finish[answer], which would finish the current task with answer.”
- §3.2: “each trajectory consists of multiple thought-action-observation steps”. “A) ReAct → CoT-SC: when ReAct fails to return an answer
  within given steps, back off to CoT-SC. We set 7 and 5 steps for HotpotQA and FEVER respectively as we find more steps will not improve
  ReAct performance.”
- §3.3: “ReAct outperforms CoT on Fever (60.9 vs. 56.3) and slightly lags behind CoT on HotpotQA (27.4 vs. 29.4).” “we randomly sampled 50
  trajectories with correct and incorrect answers (judged by EM) from ReAct and CoT respectively (thus 200 examples in total)”.
- §3.3 (Bảng 2 và lời): “Hallucination is a serious problem for CoT, resulting in much higher false positive rate than ReAct (14% vs. 6%) in
  success mode, and make up its major failure mode (56%).” “one frequent error pattern specific to ReAct, in which the model repetitively
  generates the previous thoughts and actions”. “Non-informative search, which counts for 23% of the error cases, derails the model
  reasoning and gives it a hard time to recover and reformulate thoughts.”
- §4 Results: “On ALFWorld, the best ReAct trial achieves an average success rate of 71%, significantly outperforming the best Act (45%) and
  BUTLER (37%) trials.” “we evaluate on 134 unseen evaluation games”.

## [TF23] T. Schick và cộng sự (Meta AI Research), *Toolformer: Language Models Can Teach Themselves to Use Tools*, arXiv 2302.04761v1, 9/2/2023
Tải: export.arxiv.org/abs/2302.04761 và arxiv.org/pdf/2302.04761v1 (bản arXiv; ghi chú arXiv không nêu hội nghị → bài gọi “năm 2023”).
- Tóm tắt: “They also, paradoxically, struggle with basic functionality, such as arithmetic or factual lookup, where much simpler and smaller
  models excel.” “We introduce Toolformer, a model trained to decide which APIs to call, when to call them, what arguments to pass, and how
  to best incorporate the results into future token prediction. This is done in a self-supervised way, requiring nothing more than a
  handful of demonstrations for each API.” Công cụ: “a calculator, a Q&A system, two different search engines, a translation system, and a
  calendar” (bản tóm tắt trên trang arXiv; trong PDF v1: “a search engine”).
- Hình 1: “Out of 1400 participants, 400 (or [Calculator(400 / 1400) → 0.29] 29%) passed the test.”
- §2 Filtering: “Intuitively, an API call is helpful to M if providing it with both the input and the output of this call makes it easier for
  the model to predict future tokens, compared to not receiving the API call at all, or receiving only its input. Given a filtering threshold
  f, we thus only keep API calls for which L⁻ᵢ − L⁺ᵢ ≥ f holds”.
- §1: “Toolformer, which is based on a pretrained GPT-J model … with 6.7B parameters, achieves much stronger zero-shot results, clearly
  outperforming a much larger GPT-3 model”.
- §4.2.2 + Bảng 4 (đọc lại bằng pdftotext không bố cục: hàng GPT-J 7.5/5.2/9.9; GPT-J + CC 9.6/5.0/9.3; Toolformer (disabled)
  14.8/6.3/15.0; Toolformer 40.4/29.4/44.0; OPT (66B) 6.0/4.9/7.9; GPT-3 (175B) 14.0/10.0/19.8 cho ASDiv/SVAMP/MAWPS): “allowing the model to
  make API calls more than doubles performance for all tasks, and also clearly outperforms the much larger OPT and GPT-3 models. This is
  because across all benchmarks, for 97.9% of all examples the model decides to ask the calculator tool for help.”
- §7 Limitations: “the inability of Toolformer to use tools in a chain (i.e., using the output of one tool as an input for another tool)”;
  “Our current approach also does not allow the LM to use a tool in an interactive way”; “models trained with Toolformer to often be
  sensitive to the exact wording of their input when deciding whether or not to call an API”; “processing more than a million documents
  results in only a few thousand examples of useful calls to the calculator API”; “Toolformer currently does not take into account the
  tool-dependent, computational cost incurred from making an API call.”

## [GR23] K. Greshake và cộng sự, *Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection*, arXiv 2302.12173 (v1 23/2/2023)
Tải: export.arxiv.org/abs/2302.12173 (chỉ đọc tóm tắt; dùng ở mức khái niệm phòng thủ).
- “We argue that LLM-Integrated Applications blur the line between data and instructions.” “adversaries … remotely (without a direct
  interface) exploit LLM-integrated applications by strategically injecting prompts into data likely to be retrieved.” “processing retrieved
  prompts can act as arbitrary code execution, manipulate the application's functionality, and control how and if other APIs are called.”
  “effective mitigations of these emerging threats are currently lacking.”

## [SB24] C. E. Jimenez và cộng sự, *SWE-bench: Can Language Models Resolve Real-World GitHub Issues?*, ICLR 2024 (arXiv 2310.06770)
Tải: export.arxiv.org/abs/2310.06770 và arxiv.org/pdf/2310.06770v3 (v1 10/10/2023; ghi chú arXiv “ICLR 2024”).
- Tóm tắt: “SWE-bench, an evaluation framework consisting of 2,294 software engineering problems drawn from real GitHub issues and
  corresponding pull requests across 12 popular Python repositories.” “The best-performing model, Claude 2, is able to solve a mere 1.96% of
  the issues.” (Bảng 5 của bản v3 ghi 1.97 cho Claude 2 khi thêm Claude 3 Opus; bài dùng 1,96% của tóm tắt và §5, ghi chỗ lệch vào `fix`.)
- §2.1: “producing about 90,000 PRs in total”. “We filter out task instances without at least one test where its status changes from a fail
  to pass (henceforth referred to as fail-to-pass test).” “the original 90,000 PRs are filtered down to the 2,294 task instances”.
- §2.2: “If the patch applies successfully and all of these tests pass we consider the proposed solution to have successfully resolved the
  issue. The metric for our benchmark is the percentage of task instances that are resolved.”
- §2.3: “Continually updatable … evaluate LMs on issues created after their training date”. “Issue descriptions are typically long and
  detailed (195 words on average)”. “40% of instances have at least two fail-to-pass tests … a median of 51 additional tests run to check
  whether prior functionality is properly maintained.” “SWE-bench's reference solutions average editing 1.7 files, 3.0 functions, and 32.8
  lines (added or removed).”
- §2.4: “we create a Lite subset of 300 instances”. §4.1: “codebases consist of many more tokens (438K lines on average) than can typically be
  fit into an LMs context window.”

## [SA24] J. Yang và cộng sự, *SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering*, NeurIPS 2024 (arXiv 2405.15793)
Tải: export.arxiv.org/abs/2405.15793 và arxiv.org/pdf/2405.15793v3 (chân trang 1: “38th Conference on Neural Information Processing Systems
(NeurIPS 2024)”; v1 6/5/2024).
- Tóm tắt: “we posit that LM agents represent a new category of end users with their own needs and abilities, and would benefit from
  specially-built interfaces to the software they use.”
- §1: “it fails to provide simple commands to edit a small file segment, and does not provide any feedback if the user makes an invalid
  edit.” “SWE-agent's ACI instead offers a small set of simple actions for viewing, searching through and editing files. The ACI uses
  guardrails to prevent common mistakes, and an agent receives specific, concise feedback about a command's effects at every turn.”
  “SWE-agent solves 12.47% of the 2,294 SWE-bench test tasks, substantially outperforming the previous best resolve rate of 3.8% by a
  non-interactive, retrieval-augmented system”.
- §3: “we integrate a code linter into the edit function … Invalid edits are discarded, and the agent is asked to try editing the file again.”
  “if no output is generated, a specific message ("Your command ran successfully and did not produce any output") is included”.
  “observations preceding the last 5 are each collapsed into a single line”.
- §4: “we set the per-instance budget to $4; if a run exceeded this budget, existing edits were submitted automatically.”
- §5: “successfully solving 12.47% (286/2,294) of the full SWE-bench test set and 18.00% (54/300) of the Lite split.” Bảng 3 (Lite):
  “edit action 15.0 … w/ linting 18.0”; “No search 15.7 … Iterative 12.0”; “30 lines 14.3 … 100 lines 18.0 … Full file 12.7”.
  “agents tend to look through every match exhaustively … leading to even worse performance than the not having additional search tools”.
- §5.2: “successful instances solved by SWE-agent w/ GPT 4 finish with a median cost of $1.21 and 12 steps compared to a mean of $2.52 and 21
  steps for unsuccessful ones.” “93.0% of resolved instances are submitted before exhausting their cost budget, compared to 69.0% of
  instances overall.”

## [SBV] Trang chính thức SWE-bench (swebench.com: trang chủ, verified.html) và thẻ dữ liệu princeton-nlp/SWE-bench_Verified
Tải: www.swebench.com/ và www.swebench.com/verified.html (curl); huggingface.co/datasets/princeton-nlp/SWE-bench_Verified/raw/main/README.md;
huggingface.co/api/datasets/princeton-nlp/SWE-bench_Verified (createdAt “2024-08-13T15:04:33.000Z”).
Bài của OpenAI “Introducing SWE-bench Verified” (openai.com/index/introducing-swe-bench-verified/) trả 403 với curl và WebFetch;
web.archive.org trả 429 → KHÔNG đọc được, không dạy chi tiết chỉ có ở bài đó (số người chấm, tỉ lệ mẫu bị loại, điểm của từng mô hình).
- Trang chủ, mục News: “Mar 2024 Released SWE-bench Lite.” “Mar 2024 Check out SWE-agent (12.47% on SWE-bench).” “Jun 2024 Docker -ized
  SWE-bench for easier evaluation.” “Aug 2024 SWE-bench x OpenAI = SWE-bench Verified.” “Jul 2025 mini-SWE-agent scores 65% on SWE-bench
  Verified in 100 lines of Python.”
- Trang chủ: “Verified 500 instances A human-filtered subset of SWE-bench.” “Bash Only 500 instances The default Verified view: every model in
  the same mini-SWE-agent environment.”
- verified.html: “Human annotators reviewed each instance to ensure the problem descriptions are clear, the test patches are correct, and the
  tasks are solvable given the available information.” “To make an apples-to-apples comparison of LMs easier, we evaluate all LMs using
  mini-SWE-agent in a minimal bash environment. No tools, no special scaffold structure; just a simple ReAct agent loop.”
- verified.html: “Results of release 1.x and 2.x are not necessarily comparable to each other, as 2.x uses tool calling to invoke actions,
  whereas 1.x parses action from the output strings.” “We do not aim to tune the configuration and setup to reach higher and higher scores.”
- Thẻ dữ liệu: “SWE-bench Verified is a subset of 500 samples from the SWE-bench test set, which have been human-validated for quality.”

## Điều KHÔNG dạy (nguồn không ghi hoặc không đọc được)
- Bài của OpenAI về Verified (403/429): số người chấm, số mẫu đã xem, tỉ lệ mẫu bị loại và lý do, điểm của từng mô hình trên Verified —
  không dạy. Chỉ dạy: 500 mẫu, người chấm xem đề rõ, bản kiểm đúng, giải được (verified.html), ra mắt tháng 8/2024 (trang chủ + ngày tạo thẻ).
- Điểm 65% (7/2025) là trên tập Verified 500 mẫu, còn 1,96% (2023) và 12,47% (2024) là trên tập đầy đủ 2294 mẫu: KHÔNG so trực tiếp,
  không nói “tăng 33 lần”. Bài dạy đúng chỗ này ở phần bài học sai.
- Toolformer: bản arXiv không ghi hội nghị → gọi “năm 2023”; không dạy chi tiết hàm trọng số, ngưỡng s, f của từng công cụ (phụ lục), không
  dạy Bảng 2 (số ví dụ theo ngưỡng — bảng xô cột, không đọc chắc được hàng nào của công cụ nào).
- ReAct, WebShop: tóm tắt ghi “10%”, Bảng 4 cho 40,0 so với 30,1 (Act), 29,1 (IL), 28,7 (IL + RL) → không tính lại con số 10, chỉ dẫn lời.
- Chèn lời nhắc gián tiếp [GR23]: chỉ đọc tóm tắt; không dạy cách tấn công, ví dụ chuỗi chèn hay hệ thống cụ thể bị tấn công.
- Đội ngũ, số người dùng thật của các tác tử này trong sản phẩm: nguồn không ghi. “Quy mô” của bài là quy mô của bài toán và cách đo
  (từ 3 lệnh tra cứu tới 2294 lỗi thật trên mã trung bình 438 nghìn dòng, rồi một môi trường chuẩn dùng chung).
- Giá $4 mỗi bài, $1,21 và $2,52 là của SWE-agent năm 2024 với mô hình lúc đó; không suy ra giá ngày nay.
