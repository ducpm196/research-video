# Documents and Vietnamese technical writing

Labels follow SKILL.md section 2; completion follows section 6. Domain labels used here (REQUIRED | OPTIONAL) are registered in SKILL.md section 2.

## Contents
- A. Long documents with source lineage
- B. Vietnamese technical writing (only when the output is Vietnamese)

## A. Long documents with source lineage
Applies to a report, specification, manual or proposal that spans many sections or several pages, or cites sources. Not for short replies, single-section notes or pure format conversion.

**Source rules** (SKILL.md section 8). Sources: prefer primary or direct sources that fit the claim; check freshness for current facts; cross-check disputed, uncertain or high-impact material claims where a second source is available, otherwise say so; sources sharing an origin are not independent; consensus is not verification. A search-engine result list or summary is a lead, not a source: open the page and cite it (URL, retrieval date, revision or `no revision given`); a claim that rests only on a summary stays INFERRED. A claim with neither a fitting source nor an own check is INFERRED and its validity NOT_VERIFIED.

1. **Fix the contract first.** State audience, purpose, committed scope, exclusions, length, format and acceptance criteria (each REQUIRED or OPTIONAL). Ask the person only when a missing answer would change the structure; write every other gap down as an assumption.
2. **Source register.** List every source before using it; a source you could not open is NOT_VERIFIED and may not support a claim. Never invent sources, authors, figures, dates or quotations; quote sparingly and attribute, paraphrase otherwise. Before listing a source as accessed, check it can really be opened (uploaded file, connector or web search).

   `ID | Title / URL | Revision or date | Access (opened / not opened) | Validity (VALID / NOT_VERIFIED) | Used for claims`
3. **Outline with purpose.** For each section write its purpose, the claims it must establish and its dependencies on other sections. Define each term in one place and link to it elsewhere. Reorder until dependencies flow forward.
4. **Claim ledger.** One line per material claim: `Claim | Basis (OBSERVED / CITED / INFERRED) | Source ID | Section | Check`. Mark INFERRED claims as inference in the text, never as fact. Recompute computed figures; do not copy them.
5. **Draft section by section** against each section's purpose. After each section update the ledger and a running glossary. For very long documents keep a short state summary (decisions, glossary, open items).
6. **Consistency pass.** Record each defect and its fix:
   - One term per concept; the glossary matches usage in every section.
   - Every number, total, percentage and date recomputed; units stated once and used the same way.
   - Every cross-reference points to an existing section, table or figure.
   - Each definition appears before first use, and only once.
   - No two sections make contradictory claims; compare ledger entries on the same topic.
   - Every source ID in the text exists in the register; every register entry is used or removed.
   - Headings, numbering, tense and voice follow one convention.
7. **Verify as separate claims.** SEMANTIC: facts match sources, ledger complete, no unsupported claim, numbers recomputed. RENDERING: layout, headings, tables, page breaks, links, fonts in the final file. Evidence for one never supports the other; an unchecked dimension is NOT_VERIFIED, and "verified" is never claimed without naming the dimension. If the final file cannot be rendered, RENDERING is NOT_VERIFIED.
8. **Complete** per SKILL.md section 6; list gaps as PARTIAL. Deliver through the platform's document route when one exists in this session (for example a docs connector: create the doc with headings first, then keep the source register and claim ledger as state files); platform document rules override this step. Without such a route, write the document as a file and deliver it with the session's file-delivery tool (SKILL.md, Runtime notes). Use a format skill only when a Word, PDF, slide or spreadsheet file is requested.

## B. Vietnamese technical writing
Goal: text that reads as natively written, not translated, with terms, code and labels kept exact. Applies only when the output is Vietnamese and technical or professional; reply in the language the person writes in. Excluded: English output, translation fidelity of legal or regulated text, non-technical creative writing.

**Keep exact, never translate:** code, commands, file paths, identifiers, API names, error messages, log lines; product and standard names; every closed and domain label from SKILL.md section 2 (explain it in Vietnamese beside the label, keep the label itself). In hardening or audit reports keep closed labels, field names and file names in English.

**Terminology.** Use the established Vietnamese term when one exists and readers know it. Keep the English term when it is the norm in practice (API, commit, pipeline) or a translation would be unclear. On first use give the pair, such as "kiểm chứng độc lập (independent verification)", then use one form consistently. Keep English for a concept with no established Vietnamese equivalent (for example "contract bottleneck") until a source supports a Vietnamese term. Do not invent Vietnamese terms for established English ones. Keep a glossary and apply it across the whole document.

**Natural phrasing.** Write short, direct sentences with the actor and action clear. Avoid long chains of "của", "việc", "sự" that mirror English nominalisation. Prefer active voice; use "được" or "bị" only when the agent is unknown or the benefit or harm nuance matters. Choose one register and address form for the whole document (neutral instructional with "bạn", or impersonal) and do not mix them. Re-express idioms by meaning, never literally.

**Conventions.** Correct diacritics, Unicode NFC; never strip tone marks. Choose one number and date convention (decimal and thousands separators, date order) per document and apply it everywhere; avoid ambiguity such as 1.500 versus 1,500. Sentence case for headings; units and symbols in standard form.

**Glossary header** (state at the top of the glossary):
`Register / address form: ... | Number format: ... | Date format: ...`
`English term | Vietnamese term or "keep English" | First-use form | Notes`

**Verify.** Orthography: text is NFC with no missing or garbled diacritics. Terminology: every glossary term appears in one form only. Phrasing: read for translated-sounding structures. Do not call a term "standard" or "official" without a cited source; otherwise mark it a recommendation. Language quality is a judgment, so label it INFERRED unless a source or a check supports it; an unrun check is NOT_VERIFIED.

**EGW glossary.** Terms of this skill for Vietnamese output; use it as the starting glossary. Header: `Register / address form: impersonal (choose one form per document; do not mix it with "bạn") | Number format: 1,234.56 (comma for thousands, point for decimals) | Date format: YYYY-MM-DD (ISO-8601 UTC)`

| English term | Vietnamese term or "keep English" | First-use form | Notes |
|---|---|---|---|
| Contract bottleneck | keep English | contract bottleneck (điểm nghẽn hợp đồng) | Khái niệm cốt lõi theo Mục 5, giữ nguyên thuật ngữ kỹ thuật |
| Verification record | hồ sơ xác minh | hồ sơ xác minh (verification record) | Mẫu lưu trữ bằng chứng thực nghiệm Mục 3 |
| Closed label sets | tập nhãn đóng | tập nhãn đóng (closed label sets) | 4 tập nhãn phân loại Mục 2 |
| Staleness propagation | lan truyền trạng thái suy thoái | lan truyền trạng thái suy thoái (staleness propagation) | Cơ chế cập nhật DAG khi dependency thay đổi Mục 4 |
| Independent verification | kiểm chứng độc lập | kiểm chứng độc lập (independent verification) | Nguyên tắc kiểm tra Mục 8 |
| Knowledge graph (DAG) | đồ thị tri thức (DAG) | đồ thị tri thức (knowledge graph / verification DAG) | Cấu trúc quan hệ suy luận và kiểm chứng có hướng không chu trình Mục 3, 4 |
| Handover document | tài liệu bàn giao | tài liệu bàn giao (handover.md / handover_<ref>_<ts>.md) | Tài liệu tổng kết trạng thái tác vụ, blocker, việc tiếp theo; mức full của SKILL.md Mục 8 |
| Context independence | tính độc lập ngữ cảnh | tính độc lập ngữ cảnh (context independence) | Nguyên tắc duy trì trạng thái bền vững ngoài session; SKILL.md Runtime notes |
| 5-stage operational lifecycle | chu trình vận hành 5 bước | chu trình vận hành 5 bước (5-stage operational lifecycle) | Quy trình cốt lõi của mức full, SKILL.md Mục 8: Scan, Plan, Execute, Audit, Handover |
| Execution plan | kế hoạch thực thi | kế hoạch thực thi (execution plan: plan_<ref>_<ts>.md) | Kế hoạch hành động chi tiết trước khi thực hiện Mục 8 |
