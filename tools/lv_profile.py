"""Hồ sơ chuyên ngành (tools/profiles/<tên>.yaml) cho lv.py: phân cảnh hợp lệ và nhãn, phân cảnh bắt buộc, chuẩn độ sâu (E39),
chính sách bằng chứng và luật riêng (E41–E46). Hồ sơ mặc định `stem` giữ đúng hành vi cũ của lv.py.

Bài chọn hồ sơ bằng trường `profile:` của đặc tả; không khai thì lấy `profile:` của lộ trình curriculum/<khoá>.yaml; không có nữa
thì `stem`. Thêm chuyên ngành mới = thêm một tệp YAML ở tools/profiles/ (xem .claude/skills/lecture-video/references/profiles.md)."""
import re
from functools import lru_cache
from pathlib import Path

import yaml

TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parent
PROFILES = TOOLS / "profiles"
DEFAULT_PROFILE = "stem"


@lru_cache(maxsize=None)
def load_profile(name):
    p = PROFILES / f"{name}.yaml"
    if not p.exists():
        raise SystemExit(f"không có hồ sơ chuyên ngành `{name}` (có: {', '.join(available())})")
    prof = yaml.safe_load(p.read_text(encoding="utf-8"))
    prof.setdefault("rules", [])
    prof.setdefault("depth", {})
    return prof


def available():
    return sorted(p.stem for p in PROFILES.glob("*.yaml"))


@lru_cache(maxsize=None)
def _course_profile(course):
    cp = ROOT / "curriculum" / f"{str(course).lower()}.yaml"
    if cp.exists():
        try:
            return (yaml.safe_load(cp.read_text(encoding="utf-8")) or {}).get("profile")
        except yaml.YAMLError:
            return None
    return None


def profile_name(spec):
    return spec.get("profile") or _course_profile(spec.get("course") or "") or DEFAULT_PROFILE


def profile_of(spec):
    return load_profile(profile_name(spec))


def kind_labels(prof):
    """{kind: [nhãn, lớp màu]} cho player.html (cùng dạng hằng KIND cũ)."""
    return {k: [v["label"], v["cls"]] for k, v in prof["kinds"].items()}


def voice_lang(voice):
    """Mã ngôn ngữ của giọng: “en-US-AvaNeural” → en; “vi-VN-…”, “vieneu:…”, “piper:…” → vi (hai bộ sau chỉ có giọng Việt)."""
    v = str(voice or "")
    if ":" in v:
        return "vi"
    m = re.match(r"^([a-z]{2,3})-[A-Z]{2}", v)
    return m.group(1) if m else "vi"


# ─────────────── luật riêng theo hồ sơ (E41–E46) ───────────────
ABSOLUTE_RE = re.compile(r"(?i)(?<!\w)(tốt nhất|số 1|số một thị trường|rẻ nhất|đỉnh nhất|cam kết|bảo đảm 100|100 ?%|"
                         r"không thể thiếu|duy nhất trên thị trường|chắc chắn (?:thành công|hiệu quả|giàu))(?!\w)")
TESTIMONIAL_RE = re.compile(r"(?i)(khách hàng (?:nói|khen|chia sẻ|đánh giá)|hàng nghìn người (?:đã|tin)|5 sao|năm sao|"
                            r"ai dùng cũng (?:khen|thích))")
GUARANTEE_RE = re.compile(r"(?i)(chắc chắn (?:thành công|hiệu quả|được)|đảm bảo (?:thành công|thăng tiến|giàu)|"
                          r"100 ?% (?:thành công|hiệu quả)|bí quyết thành công tuyệt đối)")
QUOTE_RE = re.compile(r"“([^”]{25,})”")


def _texts(spec):
    for si, sc in enumerate(spec.get("scenes") or []):
        for ki, st in enumerate(sc.get("steps") or []):
            yield si, sc, ki, st, f"{sc.get('show', '')}", str(st.get("show", "") or ""), str(st.get("say", "") or "")


def lint_profile_rules(spec, r, prof):
    rules = set(prof.get("rules") or [])
    scenes = spec.get("scenes") or []
    kinds = [sc.get("kind") for sc in scenes]
    if "disclosure_first" in rules:      # E41: công bố liên kết phải đến TRƯỚC mọi lời giới thiệu sản phẩm
        if "disclosure" not in kinds[:2]:
            r.err("profile", "E41 video tiếp thị liên kết phải có phân cảnh `disclosure` (công bố liên kết) trong 2 phân cảnh đầu")
        if not str((spec.get("affiliate") or {}).get("disclosure", "")).strip():
            r.err("profile", "E41 thiếu `affiliate: {disclosure: \"…\"}` — câu công bố quan hệ liên kết, hoa hồng")
    if "no_absolute_claims" in rules:    # E42: từ tuyệt đối cần nguồn trong `claims`
        claimed = " ".join(str(c.get("text", "")) for c in spec.get("claims") or [])
        for si, sc, ki, st, _, show, say in _texts(spec):
            for m in ABSOLUTE_RE.finditer(show + " " + say):
                if m.group(0).lower() not in claimed.lower():
                    r.err(f"{sc.get('id', si)}.{ki}", f"E42 từ tuyệt đối “{m.group(0)}” không có trong `claims` có nguồn — bỏ, "
                                                      "hoặc nêu tiêu chí đo được kèm nguồn và ngày")
    if "no_fake_testimonial" in rules:   # E43: không có lời khen “của khách hàng” không nguồn
        for si, sc, ki, st, _, show, say in _texts(spec):
            m = TESTIMONIAL_RE.search(show + " " + say)
            if m:
                r.err(f"{sc.get('id', si)}.{ki}", f"E43 “{m.group(0)}”: lời khen/đánh giá của người dùng phải trích được từ nguồn "
                                                  "công khai có ngày (khai trong `claims`), không viết chung chung")
    if "claims_dated" in rules:          # E44: mỗi khẳng định về sản phẩm có nguồn và ngày xem
        for i, c in enumerate(spec.get("claims") or []):
            if not (str(c.get("source", "")).strip() and re.match(r"\d{4}-\d{2}-\d{2}$", str(c.get("checked", "")))):
                r.err(f"claims#{i}", "E44 khẳng định cần `source` và `checked: YYYY-MM-DD` (giá, thông số thay đổi theo thời gian)")
        nums = {n for *_, show, say in _texts(spec) for n in re.findall(r"\d[\d.,]*\s?(?:đ|đồng|k|nghìn|triệu|%|GB|mAh|W|giờ)\b", show)}
        claimed = " ".join(str(c.get("text", "")) for c in spec.get("claims") or [])
        for n in sorted(nums):
            if n.strip() not in claimed:
                r.warn("claims", f"E44 con số sản phẩm “{n.strip()}” trên màn hình chưa có trong `claims` — thêm nguồn hoặc ghi “(minh hoạ)”")
    if "fit_both_ways" in rules:         # E45: luôn nói ai KHÔNG nên mua
        fit = " ".join(say + show for _, sc, _, st, _, show, say in _texts(spec) if sc.get("kind") == "fit")
        if not re.search(r"(?i)không nên|không hợp|không cần", fit):
            r.err("fit", "E45 phân cảnh `fit` phải nêu cả ai KHÔNG nên mua và phương án thay thế")
    if "no_guarantee" in rules:          # E46: kỹ năng mềm không hứa kết quả chắc chắn
        for si, sc, ki, st, _, show, say in _texts(spec):
            m = GUARANTEE_RE.search(show + " " + say)
            if m:
                r.err(f"{sc.get('id', si)}.{ki}", f"E46 hứa kết quả “{m.group(0)}” — nói điều kiện và mức bằng chứng thay vì bảo đảm")
    if "attributed_quotes" in rules:     # E47: trích dẫn trong ngoặc phải có tác giả/nguồn trong `quotes`
        known = " ".join(str(q.get("text", "")) for q in spec.get("quotes") or [])
        for i, q in enumerate(spec.get("quotes") or []):
            if not (str(q.get("author", "")).strip() and str(q.get("work", "")).strip()):
                r.err(f"quotes#{i}", "E47 trích dẫn cần `author` và `work` (tác phẩm, năm; bản dịch nếu có)")
        for si, sc, ki, st, _, show, say in _texts(spec):
            for m in QUOTE_RE.finditer(re.sub(r"<[^>]+>", "", show)):
                if m.group(1).strip(" .…") not in known:
                    r.warn(f"{sc.get('id', si)}.{ki}", f"E47 câu trong ngoặc kép “{m.group(1)[:40]}…” chưa khai trong `quotes` (tác giả, tác phẩm)")
    if "licensed_assets" in rules:       # E48: ảnh/khung phim phải có giấy phép khai trong `assets`
        lic = {str(a.get("file", "")) for a in spec.get("assets") or [] if str(a.get("license", "")).strip()}
        for si, sc, ki, st, _, show, say in _texts(spec):
            for m in re.finditer(r"<img[^>]+src=[\"']([^\"']+)", show):
                if m.group(1) not in lic:
                    r.err(f"{sc.get('id', si)}.{ki}", f"E48 ảnh “{m.group(1)}” chưa khai `assets: [{{file, license, source}}]` — "
                                                      "không dùng khung hình/ảnh có bản quyền khi chưa có quyền")
    if "spoiler_warning" in rules:       # E49: tiết lộ nội dung phải báo trước
        if spec.get("spoilers") and not any(re.search(r"(?i)tiết lộ nội dung|spoiler", show + say)
                                            for _, sc, _, st, _, show, say in _texts(spec) if sc.get("kind") == "hook"):
            r.err("hook", "E49 bài khai `spoilers: true` thì hook phải báo trước “có tiết lộ nội dung”")
    if "target_language_voice" in rules:  # E50: giọng bản ngữ chỉ đổi theo CẢ step, và chỉ ở phân cảnh câu mẫu
        base = voice_lang(spec.get("voice"))
        for si, sc, ki, st, _, show, say in _texts(spec):
            v = st.get("voice")
            if v and voice_lang(v) != base and re.search(r"[àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]", say, re.I):
                r.err(f"{sc.get('id', si)}.{ki}", "E50 step đọc bằng giọng bản ngữ mà lời có chữ tiếng Việt — tách lời giảng tiếng Việt "
                                                  "sang step khác (không trộn hai giọng trong một câu)")
