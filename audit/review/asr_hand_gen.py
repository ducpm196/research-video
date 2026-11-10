"""Sinh khối HAND cho asr_review_dms.py từ out/<C>/Lxx/asr_report.json: mỗi câu gắn cờ chưa xem xét → lý do trích bản chép,
phân loại từng chỗ lệch theo bằng chứng probe đã ghi trong lexicon (KNOWN); chỗ lệch không thuộc nhóm đã biết ghi là
“lệch âm/thanh thuần Việt” và liệt kê nguyên văn để người nghe kiểm. In thêm danh sách câu có chỗ lệch CHƯA phân loại.
Chạy: .venv/Scripts/python audit/review/asr_hand_gen.py <KHOÁ> "<KHOÁ> Lxx–Lyy (ngày)" <tệp khối> → ĐỌC LẠI từng lý do (bộ phân loại chỉ là
bản nháp: một từ trùng khoá KNOWN có thể mang nghĩa khác trong câu) → chèn trước dấu mốc của audit/dms/asr_review_dms.py → áp dụng."""
import json, re, sys
sys.path.insert(0, "tools")
from vi_text import normalize  # noqa: E402  số → chữ trước khi so độ dài bản chép với câu
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
C, label, out = sys.argv[1].upper(), sys.argv[2], Path(sys.argv[3])
KNOWN = {  # từ trong câu (đã chuẩn hoá) → giải thích có dẫn bằng chứng
    "pod": "Pod đọc thô (probe CLD p1: 5/8, ASR viết pốt/phút/pút)",
    "borg": "Borg đọc “Bo-gờ” theo lexicon CLD (probe p3/p4: 7/8, PARTIAL), ASR viết “burger/boga/bò gờ/bog”",
    "container": "container đọc thô (probe CLD p1: 5/8, small viết “cần tên nơi”)",
    "little": "Little đọc thô (probe CLD p1: 5/8, ASR viết “lít tồ”)",
    "cpu": "CPU đọc thô (probe CLD p1: 7/8)",
    "byte": "byte đọc thô, ASR viết “bay/bai/vai” (probe CSA p1: “bay” 8/8)",
    "gb": "GB đọc “ghi-ga-byte” theo lexicon của khoá, ASR viết “GB/gigabyte”",
    "w": "W đọc tên chữ cái “vê đúp”, ASR viết “vê đúc/về đút” (đã chấp nhận ở các khoá trước)",
    "muy": "muy (μ) ASR viết “my/nguy”",
    "phẩy": "“phẩy” của số thập phân, ASR viết dấu phẩy hoặc “phải”",
    **dict.fromkeys(["mi", "li", "crô", "na", "nô"], "tiền tố đơn vị mi-li/mi-crô/na-nô đọc tách âm tiết, ASR viết gộp “mili/micro/nano” hoặc lệch thanh"),
    **dict.fromkeys(["lam", "đa"], "lam-đa (λ), ASR viết “lambda”"),
    "tỉ": "“tỉ” ASR viết chính tả “tỷ” (cùng âm)",
    # “ghi”, “ga” KHÔNG tra từng từ (“ghi” là từ Việt: ghi sự kiện, mô hình ghi); cụm GB nhận ở UNITS
    **{ch: "chữ cái đứng riêng đọc tên kiểu Việt, ASR viết khác" for ch in "abcdefghjklmnopqrstuvwxz"},  # trừ i, y: “y nguyên” là từ Việt,
    **dict.fromkeys(["man", "tần"], "Manhattan đọc “Man-hát-tần” theo lexicon chung, ASR viết “mang hát tân/tầng”"),
    "ét": "Bayes đọc “Bay-ét” theo lexicon chung (probe 3/8, NOT_VERIFIED), ASR viết “bay X/S”",
    **dict.fromkeys(["gam", "ma"], "gam-ma (γ) ASR viết “gamma”"),
    "gram": "n-gram đọc “en-gram” theo lexicon LLM, ASR viết “engram/N-RAM”",
    "kép": "chữ w đọc “vê kép” (luật chung), ASR viết tách chữ",
    "pi": "pi (π) ASR viết “P/π”",
    "sin": "sin đọc thô, ASR viết “sinh” (gần âm)",
    "cos": "cos đọc “cô-sin” theo lexicon RBM/ROB, ASR viết “cô sinh/co sinh”",
    "mét": "đơn vị mét, ASR viết ký hiệu “m”",
    "robot": "robot đọc thô (probe RBM p1: 7/8, r → tr/ro)",
    "ô": "“ô” (ô lưới) ASR viết chữ “O”",
    "mib": "MiB đọc “mê-ga-byte” (quy ước OSY/DEN: cách nói thông dụng, màn hình giữ MiB, câu nêu rõ 2 mũ 20), ASR viết “MB”",
    "mb": "MB đọc “mê-ga-byte” theo lexicon của khoá, ASR viết “MB/megabyte”",
    "html": "HTML đọc “hát tê em eo” theo lexicon WEB, ASR viết “html/HT ML”",
    "get": "GET đọc “gét” theo lexicon WEB, ASR viết “ghét”",
    "post": "POST đọc “pâu-xt” theo lexicon WEB, ASR viết “poster”",
    "cồ": "Merkle đọc “Mơ-cồ” theo lexicon BCH, ASR viết “mơ cổ”",
    **dict.fromkeys(["xim", "xơn"], "Simpson đọc “Xim-xơn” theo lexicon DAN, ASR viết “sim sân”"),
    "alpha": "alpha đọc thô (probe AIF p1: 7/8, bản chép “an pha / ANFA / α”)",
    "beta": "beta đọc “bê-ta”, ASR viết “bê/beta”",
    "devops": "DevOps đọc thô (probe DVO p1: 6/8, NOT_VERIFIED)",
    "logic": "logic đọc “lô-gíc” theo lexicon chung, ASR viết dạng tiếng Anh",
    "web": "web đọc thô (probe NET p2: 8/8), lần này ASR viết sai",
    **dict.fromkeys(["ki", "lô"], "“ki-lô-byte” đọc tách âm tiết, ASR viết “kg” rồi chép “byte” thành “bay/ba”"),
}
UNITS = [  # (cụm âm tiết trong câu đã chuẩn hoá, giải thích) — xét theo thứ tự
    (" ô mê ga ", "ô-mê-ga (ω) đọc tách âm tiết, ASR viết “omega/ω”"),
    (" mê ga bít ", "“mê-ga-bít” đọc tách âm tiết (đã dựng ở NET), ASR viết “megabit”"),
    (" ghi ga bít ", "“ghi-ga-bít” đọc tách âm tiết, NOT_VERIFIED riêng cụm (lexicon SAR)"),
    (" ghi ga byte ", "GB đọc “ghi-ga-byte” theo lexicon của khoá, ASR viết “GB/gigabyte”"),
    (" mê ga byte ", "MB đọc “mê-ga-byte” theo lexicon của khoá, ASR viết “MB/megabyte”"),
    (" ki lô byte ", "KB đọc “ki-lô-byte” theo lexicon của khoá, ASR viết “kilobyte/kg”"),
    (" t ra byte ", "“tê-ra-byte” đọc tách âm tiết (đã dựng ở OSY/NET), ASR viết “TB/terabyte”"),
    (" ra byte ", "“tê-ra-byte” đọc tách âm tiết (đã dựng ở OSY/NET), ASR viết “TB/terabyte”"),
    (" ga bít ", "“ghi-ga-bít / mê-ga-bít” đọc tách âm tiết; mê-ga-bít đã dựng ở NET, ghi-ga-bít NOT_VERIFIED riêng cụm (lexicon SAR)"),
    (" mê ga ", "“mê-ga-…” đọc tách âm tiết (đã dựng ở NET), ASR viết dạng gộp"),
    (" ghi ga ", "GB đọc “ghi-ga-byte” theo lexicon của khoá, ASR viết “GB/gigabyte”"),
    (" ga byte ", "GB đọc “ghi-ga-byte” theo lexicon của khoá, ASR viết “GB/gigabyte”"),
    (" kb ", "KB đọc “ki-lô-byte” theo lexicon của khoá, ASR viết “kilobyte/kg”"),
    (" lô byte ", "KB đọc “ki-lô-byte” theo lexicon của khoá, ASR viết “kilobyte/kg”"),
    (" n gram ", "n-gram đọc “en-gram” theo lexicon LLM, ASR viết “engram/N-RAM”"),
    (" ra đi an ", "ra-đi-an: probe RBM p1 8/8, ASR viết “radian/radiant”"),
    (" t ta ", "tê-ta theo lexicon RBM/ROB, ASR viết “theta/teta”"),
    (" tê ta ", "tê-ta theo lexicon RBM/ROB, ASR viết “theta/teta”"),
    (" xích ma ", "xích-ma (σ) đọc tách âm tiết, ASR viết “sigma”"),
    (" ka pa ", "ka-pa (κ) đọc tách âm tiết, ASR viết “kappa”"),
    (" mi li mét ", "đơn vị mi-li-mét, ASR viết ký hiệu “mm”"),
    (" hát t ", "HTML đọc “hát tê em eo” theo lexicon WEB, ASR viết “html/HT ML”"),
    (" tâu ", "token đọc “tâu-cần” theo lexicon SAR (probe p1 8/8), ASR viết “tô cần”"),
]
LETTER_WORD = {"x": "ích", "c": "xê", "d": "dê", "b": "bê", "g": "giê", "p": "pê", "t": "tê", "v": "vê", "k": "ca"}
# ── Từ mượn / tên riêng (sửa 2026-11-09, đợt đọc kiểm C) ──
# Trước đây mọi chỗ lệch ngoài KNOWN đều bị ghi “lệch âm/thanh thuần Việt”, kể cả Kafka, Redis, NAPAS, Temenos, Spring Boot…
# (memory: “asr_hand_gen mislabels loanwords”). Nay: chỗ lệch có ít nhất một từ KHÔNG thể là âm tiết tiếng Việt → xếp
# “từ mượn/tên riêng”, dẫn luật lexicon của khoá nếu có (đọc theo luật đó) hoặc ghi “đọc thô, không có luật lexicon”.
_VOW = "aàáảãạăằắẳẵặâầấẩẫậeèéẻẽẹêềếểễệiìíỉĩịoòóỏõọôồốổỗộơờớởỡợuùúủũụưừứửữựyỳýỷỹỵ"
_VI_SYL = re.compile(r"^(?:ngh|ng|nh|ch|gh|gi|kh|ph|qu|th|tr|[bcdđghklmnpqrstvx])?[" + _VOW + r"]{1,3}(?:ch|ng|nh|[cmnpt])?$")


def _is_vi(word):
    """True nếu `word` (chữ thường) có thể là một âm tiết tiếng Việt; số và chữ cái đứng riêng coi như không xét."""
    return word.isdigit() or len(word) == 1 or bool(_VI_SYL.match(word))


def _lexicon_rules(course):
    import yaml as _y
    rules = {}
    for f in (Path("tools/registry/lexicon_vi.yaml"), Path(f"tools/registry/lexicon_vi.{course}.yaml")):
        if f.exists():
            data = _y.safe_load(f.read_text(encoding="utf-8")) or []
            items = data.get("rules", data) if isinstance(data, dict) else data
            for it in items if isinstance(items, list) else []:
                if isinstance(it, dict) and it.get("pat") and it.get("say") is not None:
                    key = re.sub(r"^(?:\\b)+|(?:\\b)+$", "", str(it["pat"]).lower())   # bỏ \b ở hai đầu (KHÔNG dùng strip: cắt mất chữ “b” của Bloom)
                    rules[key] = (str(it["say"]), f.name)
    return rules


LEX = _lexicon_rules(C)


def _loan_note(exp, heard, caption):
    """Giải thích một chỗ lệch là từ mượn/tên riêng; None nếu mọi từ trong chỗ lệch đều có thể là âm tiết Việt."""
    words = exp.split()
    cap = caption.lower()
    word = lambda s, t: re.search(r"(?<!\w)" + re.escape(s) + r"(?!\w)", t) is not None
    # luật lexicon áp cho câu này: mẫu xuất hiện NGUYÊN TỪ trong câu gốc; ưu tiên mẫu dài
    applied = sorted(((re.sub(r"[^\w\s/.-]", "", p), s, f) for p, (s, f) in LEX.items()), key=lambda x: -len(x[0]))
    applied = [(p, s, f) for p, s, f in applied if p and len(p) > 1 and word(p, cap)]
    for plain, say, fname in applied:
        syl = set(re.split(r"[\s-]+", say.lower()))
        # chỗ lệch là chính từ gốc, hoặc là các âm tiết sinh ra từ cách đọc của luật (“đít” của Rê-đít, “pát” của Na-pát)
        if word(plain, exp) or (words and set(words) <= syl):
            return f"“{plain}” đọc theo luật lexicon ({fname}: “{say}”), ASR viết “{heard or '∅'}”", []
    foreign = [w for w in words if not _is_vi(w)]
    if not foreign:
        return None, words
    # chỉ nêu đúng các từ không phải âm tiết Việt (trước đây kéo cả “nên” vào “nên cosin”); từ Việt còn lại trả về cho người gọi
    vi_left = [w for w in words if w not in foreign]
    seg = {w: _vi_segment(w) for w in foreign}
    parts = []
    viet = [w for w in foreign if seg[w]]
    raw = [w for w in foreign if not seg[w]]
    if viet:   # “cosin”, “lôgarit”: thuật ngữ đã Việt hoá, viết liền nhiều âm tiết — TTS đọc theo chính tả Việt, không phải đọc thô
        parts.append("thuật ngữ Việt hoá viết liền " + ", ".join(f"“{w}” (= {seg[w]})" for w in viet)
                     + f", TTS đọc theo chính tả Việt, ASR viết “{heard or '∅'}”")
    if raw:
        parts.append(f"từ mượn/tên riêng “{' '.join(raw)}” đọc thô (không có luật lexicon), ASR viết “{heard or '∅'}”")
    return "; ".join(parts), vi_left


def _vi_segment(word):
    """Tách `word` thành ≥ 2 âm tiết tiếng Việt hợp lệ (ít mảnh nhất), trả “lô-ga-rit”; None nếu không tách được."""
    best = {0: []}
    for i in range(1, len(word) + 1):
        for j in range(max(0, i - 7), i):
            if j in best and _VI_SYL.match(word[j:i]) and (i not in best or len(best[j]) + 1 < len(best[i])):
                best[i] = best[j] + [word[j:i]]
    out = best.get(len(word))
    return "-".join(out) if out and len(out) >= 2 else None
blocks, unknown = [f"    # ── {label} ──"], []
for d in sorted((Path("out") / C).glob("L*")):
    j = d / "asr_report.json"
    if not j.exists():
        continue
    for r in json.loads(j.read_text(encoding="utf-8")):
        if not (r["ratio"] < 0.8 or r["both_missed"]) or r["reviewed"]:
            continue
        if len(normalize(r["heard"]).split()) < 0.7 * len(normalize(r["caption"]).split()):
            print(f"  ⚠ BỎ QUA {d.name} khung {r['frame']}: bản chép ngắn hẳn câu — nghi âm thanh cụt, kiểm bằng tts_speed_scan.py rồi dựng lại")
            continue
        notes, other = [], []
        for df in r["diff"]:
            m = re.match(r"“(.*)” → nghe thành “(.*)”", df)
            exp, heard = m.groups() if m else (df, "")
            toks = exp.split()
            # đơn vị ghép đọc tách âm tiết: nhận theo CỤM trước, rồi bỏ các âm tiết đó khỏi phép tra từng từ
            pad = f" {exp} "
            for cum, note in UNITS:
                if cum in pad:   # mỗi cụm chỉ được giải thích một lần: cắt khỏi chuỗi để cụm ngắn hơn không khớp lại
                    if note not in notes:
                        notes.append(note)
                    pad = pad.replace(cum, " ")
            toks = pad.split()
            # “byte” nằm trong “ghi-ga-byte” (GB) thì không phải lỗi “byte → bay”
            # chuẩn hoá đưa TỪ VIỆT trùng tên chữ cái về chữ cái (lợi “ích” → x, “xê” dịch → c, “dê” → d, “bê” tông → b):
            # nếu câu có từ đó mà không có chữ cái đứng riêng thì đây là lệch âm của một từ, không phải chữ cái
            low = r["caption"].lower()
            for ch, name in LETTER_WORD.items():
                if ch in toks and re.search(rf"(?<!\w){name}(?!\w)", low) and not re.search(rf"(?<!\w){ch}(?!\w)", low):
                    toks = [w for w in toks if w != ch]
                    other.append(f"{name}/{heard or '∅'}")
            # “beta” đọc “bê-ta”; chuẩn hoá đưa “bê” về “b” → không phải chữ cái đứng riêng
            if "b" in toks and "beta" in r["caption"].lower():
                toks = [w for w in toks if w != "b"]
                if KNOWN["beta"] not in notes:
                    notes.append(KNOWN["beta"])
            hits = [KNOWN[w] for w in toks if w in KNOWN and not (w == "byte" and {"ghi", "ga", "gb"} & set(toks))]
            for h in hits:
                if h not in notes:
                    notes.append(h)
            # phần còn lại của cụm lệch (không thuộc nhóm đã biết; “giây” đi cùng đơn vị) → ghi nguyên văn cho người nghe
            rest = [w for w in toks if w not in KNOWN and w != "giây"]
            loan, vi_left = _loan_note(" ".join(rest), heard, r["caption"]) if rest else (None, rest)
            if loan:
                if loan not in notes:
                    notes.append(loan)
                rest = vi_left
            if rest:
                other.append(f"{exp}/{heard or '∅'}" if not hits and len(rest) == len(exp.split()) else f"{' '.join(rest)} (trong “{exp}” → “{heard}”)")
        # câu khớp cả câu nhưng bị gắn cờ vì TỪ RỦI RO cả hai mô hình nghe khác (diff rỗng) → giải thích theo both_missed
        # câu khớp cả câu (diff rỗng): chuẩn hoá tách cách đọc viết tắt (“hát tê em eo”, “ki-lô-byte”) thành chữ cái / âm tiết,
        # nên giải thích theo THUẬT NGỮ có trong câu trước, chỉ khi không có mới dùng từng từ của both_missed
        if not r["diff"]:
            cap = set(re.findall(r"[a-z0-9]+", r["caption"].lower()))
            for term, note in (("html", KNOWN["html"]), ("kb", "KB đọc “ki-lô-byte” theo lexicon của khoá, ASR viết “KB/kilobyte”"),
                               ("gb", KNOWN["gb"]), ("mb", KNOWN["mb"]), ("mib", KNOWN["mib"])):
                if term in cap and note not in notes:
                    notes.append(note)
        for w in (r["both_missed"] if not r["diff"] and not notes else []):
            if w in KNOWN and KNOWN[w] not in notes and not (w == "byte" and {"ghi", "ga"} & set(r["both_missed"])):
                notes.append(KNOWN[w])
        if not notes and not other:
            notes.append("từ rủi ro " + ", ".join(r["both_missed"]) + " cả hai mô hình viết khác (cách viết, không phải âm)")
        if other:
            notes.append("lệch âm/thanh thuần Việt: " + ", ".join(other))
            unknown.append((d.name, r["frame"], other))
        s = r["caption"].strip().replace("'", "\\'")
        reason = (f"ASR chép “{r['heard'].strip()}” ({r['ratio']}): " + "; ".join(notes)
                  + " — NOT_VERIFIED bằng tai người").replace("'", "\\'")
        blocks += [f"    '{s}':", f"        '{reason}',"]
out.write_text("\n".join(blocks) + "\n", encoding="utf-8")
print(f"{len(blocks) // 2} câu → {out}")
for u in unknown:
    print("  chưa phân loại:", *u)
