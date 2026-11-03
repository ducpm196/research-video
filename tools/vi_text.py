"""Chuẩn hoá văn bản tiếng Việt để so lời đọc kỳ vọng với bản nghe lại (ASR)."""
import re
import unicodedata

DIGITS = ["không", "một", "hai", "ba", "bốn", "năm", "sáu", "bảy", "tám", "chín"]


def _under_1000(n, full):
    h, t, u = n // 100, n // 10 % 10, n % 10
    out = []
    if full or h:
        out += [DIGITS[h], "trăm"]
    if t == 0:
        if u and (full or h):
            out.append("linh")
    elif t == 1:
        out.append("mười")
    else:
        out += [DIGITS[t], "mươi"]
    if u:
        if u == 1 and t >= 2:
            out.append("mốt")
        elif u == 5 and t >= 1:
            out.append("lăm")
        else:
            out.append(DIGITS[u])
    return out


def num_to_words(n):
    """Số nguyên ≥ 0 → chữ tiếng Việt (vd 784 → 'bảy trăm tám mươi bốn'). Từ 10⁹ trở lên đọc theo “tỉ”, lồng nhau:
    2 147 483 648 → 'hai tỉ một trăm bốn mươi bảy triệu …'; 10¹² → 'một nghìn tỉ' (lỗi thật CSA L01 2026-10-28: ASR chép số 2³¹,
    bản cũ chỉ tới “triệu” nên IndexError). Kết quả cho n < 10⁹ không đổi."""
    if n == 0:
        return "không"
    if n >= 10 ** 9:
        hi, lo = divmod(n, 10 ** 9)
        if not lo:
            return num_to_words(hi) + " tỉ"
        rest = " ".join(_full_below_billion(lo))
        return num_to_words(hi) + " tỉ " + rest
    units, groups, parts = ["", "nghìn", "triệu"], [], []
    while n:
        groups.append(n % 1000)
        n //= 1000
    seen_higher = False
    for i in range(len(groups) - 1, -1, -1):
        g = groups[i]
        if g:
            parts += _under_1000(g, full=seen_higher)   # nhóm sau nhóm đầu đọc đủ: 1005 → một nghìn không trăm linh năm
            parts += [units[i]] if units[i] else []
            seen_higher = True
    return " ".join(parts)


def _full_below_billion(n):
    """Phần dưới 10⁹ đứng SAU “tỉ”: mọi nhóm đọc đủ (5 → 'không trăm linh năm'; 7 000 → 'không trăm linh bảy nghìn')."""
    units, groups, parts = ["", "nghìn", "triệu"], [], []
    for _ in range(3):
        groups.append(n % 1000); n //= 1000
    for i in range(2, -1, -1):
        if groups[i]:
            parts += _under_1000(groups[i], full=True) + ([units[i]] if units[i] else [])
    return parts


_OLD_TONE = {"óa": "oá", "òa": "oà", "ỏa": "oả", "õa": "oã", "ọa": "oạ", "óe": "oé", "òe": "oè", "ỏe": "oẻ", "õe": "oẽ",
             "ọe": "oẹ", "úy": "uý", "ùy": "uỳ", "ủy": "uỷ", "ũy": "uỹ", "ụy": "uỵ"}


def normalize(text):
    text = unicodedata.normalize("NFC", text.lower())
    # bỏ dấu kiểu cũ/mới là CÙNG một từ (“xóa” = “xoá”, “hòa” = “hoà”): quy về kiểu mới, chỉ ở cuối âm tiết
    text = re.sub(r"(óa|òa|ỏa|õa|ọa|óe|òe|ỏe|õe|ọe|úy|ùy|ủy|ũy|ụy)(?!\w)", lambda m: _OLD_TONE[m.group(1)], text)
    text = re.sub(r"(?<=\d)[.,](?=\d{3}\b)", "", text)          # 1.000 → 1000
    text = re.sub(r"(?<=\d),(?=\d)", " phẩy ", text)            # 4,47 → 4 phẩy 47
    text = re.sub(r"\d+", lambda m: " " + num_to_words(int(m.group())) + " ", text)
    # ASR viết dấu phẩy trên của đạo hàm (“F' của ba”, L05 2026-10-23) — lời kỳ vọng viết bằng chữ “f phẩy”
    text = re.sub(r"(?<=[a-z])['’′]", " phẩy ", text)
    # ASR viết “29%” cho lời “29 phần trăm” — trước đây “%” bị xoá như dấu câu, câu ngắn bị gắn cờ oan (L26 2026-10-25)
    text = text.replace("%", " phần trăm ")
    text = re.sub(r"(?<![^\W\d_])cm(?![^\W\d_])", " xăng ti mét ", text)   # “19cm” = “19 xăng-ti-mét” (L27)
    text = re.sub(r"[^\w\s]", " ", text)
    # các cách đọc số tương đương được quy về một dạng: tư=bốn, lăm=năm, mốt=một, lẻ=linh, ngàn=nghìn
    syn = {"tư": "bốn", "lăm": "năm", "mốt": "một", "lẻ": "linh", "ngàn": "nghìn", **LETTER_NAMES}
    return " ".join(syn.get(w, w) for w in text.split())


# Tên chữ cái kiểu Việt mà ASR hay viết thay cho chữ cái (L01: x → “ích/ít”, c → “xê”). Áp dụng cho CẢ HAI phía
# (lời kỳ vọng và lời nghe được), nên chỉ gộp hai cách viết của cùng một âm, không che được từ đọc sai khác hẳn.
# Không gộp từ hay gặp mang nghĩa khác (“xe”, “giác”) để khỏi che lỗi thật. “dê” = tên chữ D (ASR 2026-10-22: “N nhân D” → “n nhân dê”).
LETTER_NAMES = {"ích": "x", "ít": "x", "ich": "x", "bê": "b", "xê": "c", "đê": "d", "dê": "d", "vê": "v", "tê": "t",
                "dét": "z", "giét": "z", "zét": "z", "y": "i"}

# Cách ASR viết tên chữ cái mà cũng là từ thật (“giác”, “giết”, “xe”): chỉ coi là chữ cái khi câu kỳ vọng CÓ chữ đó.
# Lấy từ lời nghe thật của L01 (small + medium, 2026-10-22).
LETTER_HEARD = {"z": {"giác", "giết", "giếp"}, "c": {"xe", "cờ"}, "x": {"dứt"},
                "v": {"về", "vệ"},   # “vê” trong “vê kép” (= w), L02 2026-10-22
                # L03 2026-10-23, đối chứng: audio “Q” và audio viết hẳn “quy” dài bằng nhau (3,264 s); medium chép
                # bản “quy”/“ca” y hệt bản chữ cái thô → TTS đọc tên chữ cái, ASR viết tên chữ cái
                "q": {"quy", "quý"}, "k": {"ca"},
                # L04 2026-10-23 (lambda_probe.py): TTS đọc “lam-đa”; small/medium nghe “5 đã”, “5 đa” (l → n)
                "lam": {"năm", "lâm"}, "đa": {"đã"},
                # L05 2026-10-23 (l05_probe.py): TTS đọc f = “ép”, h = “hát”; bản viết hẳn “ép”, “hát” cho độ dài lệch
                # 0–72 ms và medium chép y hệt bản chữ cái thô (“ép”, “eff”, “F”; “hát”). “ép”, “hát” là từ thật
                # (L04: “bị ép thành”), nên chỉ đổi ở vị trí gióng hàng với chữ f, h
                "f": {"ép", "eff", "app"}, "h": {"hát"},
                # L06 2026-10-24: TTS đọc J = “gi”, giọng Bắc gi = d → ASR chép “di” (asr_L06 khung 19)
                "j": {"di", "gi"},
                # L09–L10 2026-10-24: chữ g (gradient tại bước k, tổng G) — ASR chép “d”, “dê”, “dây” ở 12 khung L10, 3 khung L09
                #   (giọng Bắc: “giê” = “dê”); chỉ đổi ở vị trí gióng hàng với chữ g
                "g": {"d", "dê", "dây", "giê"}}
# Từ ngoại ASR viết theo chính tả gốc trong khi TTS đọc đúng cách đã chọn (lexicon_vi.yaml): coi là cùng một từ.
ASR_ALIASES = {"pythagore": "pi ta go", "pythagoras": "pi ta go", "project": "prô giéc", "projection": "prô giéc sần",
               "smith": "smít", "vét": "véc", "vết": "véc",
               "lambda": "lam đa",
               # L05 2026-10-23 (grad_probe.py): TTS đọc “nơ-ron”, medium chép “neuron”/“Neuro”
               "neuron": "nơ ron", "neuro": "nơ ron",
               # L05 2026-10-23: TTS đọc “Gia-cô-biên” (jh_probe.py), ASR viết theo chính tả gốc “Giacobin”/“Giacobbian”
               "giacobin": "gia cô biên", "giacobian": "gia cô biên", "giacobbian": "gia cô biên",
               # L06 2026-10-24 (asr_L06): ASR viết theo chính tả gốc tiếng Anh khi TTS đọc đúng cách đã chọn
               "jacobian": "gia cô biên", "jacobin": "gia cô biên", "jacobean": "gia cô biên",
               "hessian": "hết sen", "hexen": "hết sen",          # TTS đọc “Hết-sen” (lexicon, h_probe2.py)
               "gradient": "grê đi ần", "gradian": "grê đi ần",   # TTS đọc “grê-đi-ần” (lexicon, grad_probe.py)
               # L09–L10 2026-10-24: TTS đọc theo cách viết Việt hoá trong lexicon (l09_probe*.py, l10_probe*.py); ASR chép
               # đúng chính tả tiếng Anh khi nhận ra tên → coi là cùng từ. Biến thể nghe sai (“neserope”, “rms probe”) KHÔNG đổi.
               "eta": "ê ta", "beta": "bê ta", "adam": "a đam", "momentum": "mô men tum", "epsilon": "ép xi lôn",
               "nesterov": "nê sờ tê rốp", "adagrad": "a đa grát", "rmsprop": "a rờ em ét prốp", "adadelta": "a đa đeo ta",
               "newton": "niu tơn",
               # L11 ASR lượt 1 (out/L11/asr_report.md): TTS đọc “pa-ra-bôn”; small và medium chép “parabon”/“parabola” ở 7 câu
               "parabon": "parabol", "parabola": "parabol",
               # L12 (l12_probe.py): TTS đọc “lôgarit”, medium chép “logarit”/“logarithm”
               "logarit": "lôgarit", "logarith": "lôgarit", "logarithm": "lôgarit",
               # L13–L23 (l13_probe*.py, l20_probe.py, l23_probe.py, ASR L15/L17): TTS đọc theo cách viết Việt hoá; ASR chép đúng
               #   chính tả gốc khi nhận ra từ → coi là cùng từ. Chỉ các cách viết ĐÚNG (không thêm biến thể nghe sai như “bayet”).
               "bernoulli": "bơ nu li", "bayes": "bay ét", "theta": "thê ta", "elipse": "elip", "ellipse": "elip",
               "sigmoid": "xích moi", "softmax": "sóp mác", "logistic": "lô gi xtích", "relu": "re lu", "xavier": "xa vi ê"}   # L11 (l11_probe.py): TTS đọc “Niu-tơn”, medium chép “Newton”


def _north(w):
    """Dạng phát âm giọng Bắc (giọng vi-VN-NamMinhNeural): phụ âm đầu gi = d, x = s. Hai từ cùng dạng thì ASR
    không có cách nào phân biệt qua âm thanh (L06 2026-10-24: “Gia-cô-biên” → “da cô biên” 9 câu, “xếp” → “sếp”)."""
    if w.startswith("gi") and len(w) > 2:
        w = "d" + w[2:]
    elif w.startswith("x"):
        w = "s" + w[1:]
    return w


def canon_heard(heard, expected):
    """Token ASR đã chuẩn hoá → dạng so được với `expected` (đã chuẩn hoá): đổi bí danh từ ngoại, và đổi tên chữ cái
    thành chữ cái CHỈ ở vị trí gióng hàng với đúng chữ cái đó trong câu kỳ vọng (câu có cả “z” và “tam giác” thì
    “giác” của “tam giác” vẫn giữ nguyên)."""
    import difflib
    out = " ".join(ASR_ALIASES.get(w, w) for w in heard).split()
    # các chữ cái đọc rời (“A B”, “b c”) bị ASR viết dính (“ab”, “bc”): tách lại CHỈ khi đúng dãy chữ cái đó có trong câu
    exp_str = " " + " ".join(expected) + " "
    out = " ".join(" ".join(w) if 2 <= len(w) <= 4 and w.isascii() and w.isalpha() and f" {' '.join(w)} " in exp_str
                   else w for w in out).split()
    for op, a1, a2, b1, b2 in difflib.SequenceMatcher(None, expected, out, autojunk=False).get_opcodes():
        if op == "replace":
            for ea, hb in zip(range(a1, a2), range(b1, b2)):
                if out[hb] in LETTER_HEARD.get(expected[ea], ()) or _north(out[hb]) == _north(expected[ea]):
                    out[hb] = expected[ea]
    return out
