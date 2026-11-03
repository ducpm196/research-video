"""Kiểm thử công cụ: lint phải BẮT được từng lỗi cố tình cài trong fixtures/bad_lesson.yaml
và phải SẠCH với mọi bài trong lessons/. Chạy: .venv/Scripts/python tests/test_lint.py"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import lv  # noqa: E402

EXPECT = {
    "E1 assumes không có trong registry": "không có trong tools/registry/symbols.yaml",
    "E2 ký hiệu dùng trước khi giải thích": "dấu tổng Sigma",
    "E3 LaTeX thô trong say": "LaTeX thô",
    "E4 unicode chưa giải thích": "“⊥”",
    "E5 phép tính sai": "phép tính SAI",
    "E6 KaTeX hỏng": "KaTeX:",
    "E7 phụ đề tràn": "phụ đề sẽ tràn",
    "E8 SVG marker": "userSpaceOnUse",
    "E9 thiếu phân cảnh bắt buộc": "thiếu phân cảnh bắt buộc",
}


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    fails = 0
    r = lv.lint(lv.load_spec(ROOT / "tests" / "fixtures" / "bad_lesson.yaml"))
    text = "\n".join(r.errors)
    for name, needle, pool in [("E10 lệnh LaTeX chưa đăng ký", "\\Omega", r.warnings),
                               ("E12 viết lẫn ‖u‖₂ và ‖u‖", "Độ dài vector (chuẩn): viết lẫn", r.errors),
                               ("E13 bước biến đổi không nói lý do", "chưa nói lý do", r.warnings),
                               ("E14 ⇒ trong chữ và ⟹ trong công thức", "“suy ra” vừa gõ ký tự", r.errors),
                               ("E15 dấu phẩy trên u′ chưa giải thích", "dấu phẩy trên", r.errors),
                               ("E16 ký tự ✗ giống chữ X", "giống chữ X", r.errors),
                               ("E18 hai chỉ số dưới x₁₂ chưa giải thích", "hai chỉ số dưới", r.errors),
                               ("E18 kích thước M × N chưa giải thích", "kích thước ma trận M × N", r.errors),
                               ("E19 kích thước gõ bằng \\times", "dùng \\sz{M}{N}", r.errors),
                               ("E22 nhắc bài không có trong lộ trình", "lộ trình không có bài L99", r.errors),
                               ("E22 nhắc bài sau thiếu forward_ref", "chưa có `forward_ref: true`", r.errors),
                               ("E22 nhắc bài sau giữa phần giảng", "nhắc bài sau giữa phần giảng", r.warnings),
                               ("E23 nhắc bài trước nói tắt", "E23 nhắc bài trước mà gần như không nói lại", r.warnings),
                               ("E24 “bài sau” ghi sai số bài", "E24 “bài sau” ghi là bài 7", r.errors),
                               ("E24 “bài sau” không khớp tên bài kế tiếp", "E24 câu về “bài sau” không nhắc cụm nào", r.warnings),
                               ("E25 tiêu đề scene có ký tự LaTeX", "E25 tiêu đề scene có ký tự LaTeX", r.errors),
                               ("E26 check chỉ so hai hằng số", "E26 check chỉ so hai hằng số", r.warnings),
                               ("E27 mã nội bộ hiện cho người học", "E27 mã nội bộ", r.errors),
                               ("E28 phiên âm tên riêng trong lời đọc", "E28 lời đọc gõ phiên âm", r.errors),
                               ("E29 nhắc nguồn người xem không có", "E29 nhắc nguồn người xem không có", r.errors),
                               ("E30 ghi chú xem xét ASR mồ côi", "E30 câu đã xem xét không còn trong bài", r.warnings),
                               ("E31 focus trỏ tới phần không có", "không có phần 3", r.errors),
                               ("E31 focus thiếu mục cho một câu", "E31 `focus` phải là danh sách đúng 2 mục", r.errors),
                               ("E32 step dày chữ thiếu focus", "E32 3 câu nói về khối có 3 phần", r.warnings),
                               ("E32 2 câu trên khối 2 phần thiếu focus", "E32 2 câu nói về khối có 2 phần", r.warnings),
                               ("E32 step không show thiếu focus", "không có `show` mà nói tiếp", r.warnings),
                               ("E33 tên lệnh LaTeX mất dấu \\", "E33 “equiv” trong công thức thiếu dấu", r.errors),
                               ("E34 khoá step lạ", "E34 khoá step `set`", r.errors),
                               ("E35 check hai vế giống hệt", "E35 check có phép so sánh hai vế giống hệt", r.warnings),
                               ("E36 hệ 16 viết liền", "E36 chuỗi hệ 16 “3E200000”", r.warnings),
                               ("E37 khoảng trỏ tới bài không có", "E37 khoảng “bài 99–100”", r.errors),
                               ("E37 bản đồ khoá học bỏ sót bài", "E37 bản đồ khoá học nhắc", r.errors),
                               ("E38 biến thể chính tả", "E38 viết “luỹ”", r.warnings)]:
        ok = any(needle in w for w in pool)
        fails += not ok
        print(f"{'PASS' if ok else 'FAIL'} | bắt được {name}")
    # E29 + domain_terms (CSA L11, 2026-10-28): “dòng 345” là thuật ngữ khi bài khai báo domain_terms: [dòng]; “tài liệu” vẫn bị chặn
    import copy as _cp
    base29 = lv.load_spec(ROOT / "lessons" / "cs115" / "L12_ham_mu_logarit.yaml")
    s29 = _cp.deepcopy(base29); s29["scenes"][0]["steps"][0]["say"] = "Bộ nhớ đệm nhìn vào dòng 345 của nó."
    e_no = any("E29" in e for e in lv.lint(s29, quiet=True).errors)
    s29["domain_terms"] = ["dòng"]
    e_yes = any("E29" in e for e in lv.lint(s29, quiet=True).errors)
    s29["scenes"][0]["steps"][0]["say"] = "Theo tài liệu, bộ nhớ đệm nhìn vào dòng 345."
    e_doc = any("E29" in e for e in lv.lint(s29, quiet=True).errors)
    ok = e_no and not e_yes and e_doc
    fails += not ok
    print(f"{'PASS' if ok else 'FAIL'} | E29 “dòng N” bị chặn mặc định, được phép khi domain_terms: [dòng], “tài liệu” vẫn bị chặn")
    # E39 (depth: full) và E40 (case: journey), 2026-10-31: hai bài mẫu sạch; bỏ hình cơ chế / bỏ ôn nền / đảo năm phải bị chặn
    d39 = lv.load_spec(ROOT / "lessons" / "llm" / "L05_chi_phi_tinh_toan.yaml")
    j40 = lv.load_spec(ROOT / "lessons" / "cld" / "L15_hanh_trinh_borg_kubernetes.yaml")
    clean = not any(("E39" in e or "E40" in e) for e in lv.lint(d39, quiet=True).errors + lv.lint(j40, quiet=True).errors)
    s = _cp.deepcopy(d39)
    for sc in s["scenes"]:
        for st in sc["steps"]:
            st["show"] = str(st.get("show", "")).replace("<svg", "<div").replace("</svg>", "</div>")
    no_svg = any("E39 không có hình cơ chế" in e for e in lv.lint(s, quiet=True).errors)
    s = _cp.deepcopy(d39); s["scenes"] = [sc for sc in s["scenes"] if sc["kind"] != "prereq"]
    no_pre = any("E39" in e and "prereq" in e for e in lv.lint(s, quiet=True).errors)
    s = _cp.deepcopy(j40); next(sc for sc in s["scenes"] if sc["id"] == "stage5")["stage"]["year"] = "2010"
    order = any("E40" in e and "trục thời gian" in e for e in lv.lint(s, quiet=True).errors)
    s = _cp.deepcopy(j40); next(sc for sc in s["scenes"] if sc["id"] == "stage2").pop("checks")
    nochk = any("E40" in e and "checks" in e for e in lv.lint(s, quiet=True).errors)
    for name, ok in [("E39/E40 hai bài mẫu sạch", clean), ("E39 bắt bài thiếu hình cơ chế", no_svg),
                     ("E39 bắt bài thiếu ôn nền", no_pre), ("E40 bắt chặng đảo năm", order), ("E40 bắt chặng không tính lại số", nochk)]:
        fails += not ok
        print(f"{'PASS' if ok else 'FAIL'} | {name}")
    # Hồ sơ chuyên ngành (2026-10-31): mỗi mẫu trong examples/profiles/ lint 0 FAIL; mỗi luật riêng E41–E50 bắt được lỗi cài sẵn
    ex = {p: lv.load_spec(next((ROOT / "examples" / "profiles").glob(f"{p}_L0*.yaml")))
          for p in ("language", "softskill", "humanities", "film", "affiliate")}
    for p_, s_ in ex.items():
        errs = lv.lint(s_, quiet=True).errors
        ok = not errs
        fails += not ok
        print(f"{'PASS' if ok else 'FAIL'} | mẫu hồ sơ {p_} lint 0 FAIL" + ("" if ok else f": {errs[:2]}"))

    def bad(prof, mutate, needle):
        s = _cp.deepcopy(ex[prof]); mutate(s)
        return any(needle in e for e in lv.lint(s, quiet=True).errors)

    def say_(s, sid, txt):
        next(sc for sc in s["scenes"] if sc["id"] == sid)["steps"][0]["say"] += " " + txt
    cases = [
        ("E41 thiếu công bố liên kết", "affiliate", lambda s: s.__setitem__("scenes", [x for x in s["scenes"] if x["kind"] != "disclosure"]), "E41"),
        ("E42 từ tuyệt đối không nguồn", "affiliate", lambda s: say_(s, "compare", "Máy A là loại tốt nhất."), "E42"),
        ("E43 lời khen khách hàng bịa", "affiliate", lambda s: say_(s, "compare", "Khách hàng khen máy A hết lời."), "E43"),
        ("E44 khẳng định không có ngày xem", "affiliate", lambda s: s["claims"][0].pop("checked"), "E44"),
        ("E45 không nói ai không nên mua", "affiliate",
         lambda s: next(x for x in s["scenes"] if x["kind"] == "fit")["steps"][0].update(say="Máy lớn hợp với người đi nhiều ngày.", show="<p>đi nhiều ngày</p>", focus=[1]), "E45"),
        ("E46 hứa kết quả chắc chắn", "softskill", lambda s: say_(s, "model", "Làm vậy chắc chắn thành công."), "E46"),
        ("E47 trích dẫn thiếu tác giả", "humanities", lambda s: s["quotes"][0].pop("author"), "E47"),
        ("E48 ảnh chưa khai giấy phép", "film",
         lambda s: next(x for x in s["scenes"] if x["kind"] == "theme")["steps"][0].update(show="<img src='still.png'>"), "E48"),
        ("E49 tiết lộ nội dung không báo", "film", lambda s: s.__setitem__("spoilers", True), "E49"),
        ("E50 giọng bản ngữ đọc lời tiếng Việt", "language",
         lambda s: next(x for x in s["scenes"] if x["kind"] == "pattern")["steps"][1].update(say="Câu mẫu: I have lived here."), "E50"),
    ]
    for name, prof, mut, needle in cases:
        ok = bad(prof, mut, needle)
        fails += not ok
        print(f"{'PASS' if ok else 'FAIL'} | bắt được {name}")
    # hồ sơ stem giữ y hành vi cũ: nhãn phân cảnh trùng hằng KIND trước 2026-10-31
    ok = lv.kind_labels(lv.load_profile("stem"))["symbol"] == ["Giải mã ký hiệu", "k-symbol"] and lv.profile_name({"course": "CS115"}) == "stem"
    fails += not ok
    print(f"{'PASS' if ok else 'FAIL'} | hồ sơ mặc định stem giữ nhãn và cấu trúc cũ")
    # E12b (L12): viết lẫn \ln/\log hoặc e^/\exp ngoài step notation_note phải bị chặn; trong notation_note thì được phép
    import copy
    base = lv.load_spec(ROOT / "lessons" / "cs115" / "L12_ham_mu_logarit.yaml")
    for name, extra, needle in [("E12 viết lẫn ln và log", r" $\log 2$", "Lôgarit tự nhiên: viết lẫn"),
                                ("E12 viết lẫn e^x và exp", r" $\exp(1)$", "Hàm mũ cơ số e: viết lẫn")]:
        sp_ = copy.deepcopy(base)
        st = next(sc for sc in sp_["scenes"] if sc["id"] == "verify")["steps"][0]
        st["show"] += extra
        errs = "\n".join(lv.lint(sp_).errors)
        ok = needle in errs
        fails += not ok
        print(f"{'PASS' if ok else 'FAIL'} | bắt được {name}")
    ok = not any("viết lẫn" in e for e in lv.lint(base).errors)
    fails += not ok
    print(f"{'PASS' if ok else 'FAIL'} | E12 cho phép ln/log, exp trong step notation_note (L12)")
    # E12c (L13): \text{Var} lẫn với \operatorname{Var} phải bị chặn; \cap chưa giới thiệu phải bị chặn
    base13 = lv.load_spec(ROOT / "lessons" / "cs115" / "L13_xac_suat_roi_rac.yaml")
    sp_ = copy.deepcopy(base13)
    next(sc for sc in sp_["scenes"] if sc["id"] == "quiz")["steps"][1]["show"] += r" $\text{Var}(X)$"
    ok = "Phương sai: viết lẫn" in "\n".join(lv.lint(sp_).errors)
    fails += not ok
    print(f"{'PASS' if ok else 'FAIL'} | bắt được E12 viết lẫn Var (operatorname và text)")
    sp_ = copy.deepcopy(base13)
    next(sc for sc in sp_["scenes"] if sc["id"] == "sym_prob")["steps"][0]["show"] += r" $P(A \cap B)$"
    ok = any("`cap`" in e for e in lv.lint(sp_).errors)
    fails += not ok
    print(f"{'PASS' if ok else 'FAIL'} | bắt được ký hiệu giao (cap) dùng trước khi giải thích")
    ok = not any("viết lẫn" in e or "`cap`" in e for e in lv.lint(base13).errors)
    fails += not ok
    print(f"{'PASS' if ok else 'FAIL'} | L13 gốc không bị báo nhầm (Var, cap)")
    # E11: luật phát âm chỉ khớp nguyên từ (hồi quy lỗi thật 'hai' → 'hây ai' ở L01 v1)
    for src, want in [("hai cộng hai", "hai cộng hai"), ("sai số", "sai số"), ("AI học", "ây ai học"),
                      ("chữ proj", "chữ prô-giéc"), ("projection", "prô-giéc-sần"), ("vector", "véc tơ"),
                      ("vector w và w một", "véc tơ vê kép và vê kép một"), ("wow", "wow")]:
        got = lv.lexicon_apply(src)
        ok = got == want
        fails += not ok
        print(f"{'PASS' if ok else 'FAIL'} | E11 phát âm “{src}” → “{got}” (kỳ vọng “{want}”)")
    # bộ đổi số → chữ dùng cho ASR
    sys.path.insert(0, str(ROOT / "tools"))
    from vi_text import num_to_words, normalize
    # E17: ASR mức từ — lời nghe thật của small/medium ở đối chứng 2026-10-22. Một từ đọc sai (“nghịch lý” thay
    # “nghịch đảo”) cho độ khớp câu 0,917 nên lọt ngưỡng 0,8; mức từ phải bắt được vì CẢ HAI mô hình nghe khác.
    # Ngược lại, câu đúng mà chỉ small nghe nhầm (“cột” → “cục”) thì không được gắn cờ.
    def both(expected, h1, h2):
        e = normalize(lv.lexicon_apply(expected)).split()
        m1 = lv.missed_words(e, normalize(lv.lexicon_apply(h1)).split())
        m2 = lv.missed_words(e, normalize(lv.lexicon_apply(h2)).split())
        return [e[k] for k in sorted(m1 & m2)]
    from vi_text import canon_heard
    for name, got, want in [
            ("E17 “giác” = chữ z khi câu có z", canon_heard(["giác", "vuông"], ["z", "vuông"]), ["z", "vuông"]),
            ("E17 “giết” KHÔNG bị coi là z khi câu không có z", canon_heard(["giết"], ["giữ"]), ["giết"]),
            ("E17 “project” = cách đọc prô-giéc", canon_heard(["chữ", "project"], ["chữ", "prô", "giéc"]), ["chữ", "prô", "giéc"]),
            ("E17 “ab” = hai chữ cái a b khi câu có a b", canon_heard(["còn", "ab", "nhân"], ["còn", "a", "b", "nhân"]),
             ["còn", "a", "b", "nhân"]),
            ("E17 “ad” KHÔNG bị tách khi câu không có a d", canon_heard(["ad"], ["s"]), ["ad"]),
            ("E17 “quy” = chữ Q khi câu có q (L03)", canon_heard(["vậy", "quy", "chuyển", "vị"], ["vậy", "q", "chuyển", "vị"]),
             ["vậy", "q", "chuyển", "vị"]),
            ("E17 “quy tắc” KHÔNG bị coi là chữ q", canon_heard(["quy", "tắc", "q"], ["quy", "tắc", "q"]), ["quy", "tắc", "q"]),
            ("E17 “quy” KHÔNG thành q khi câu không có q", canon_heard(["quy", "tắc"], ["luật", "tắc"]), ["quy", "tắc"]),
            ("E17 “năm đã” = lam-đa khi câu có lambda (L04)", canon_heard(["số", "năm", "đã", "gọi"], ["số", "lam", "đa", "gọi"]),
             ["số", "lam", "đa", "gọi"]),
            ("E17 “năm” KHÔNG thành “lam” khi câu kỳ vọng là số khác", canon_heard(["năm", "bước"], ["bốn", "bước"]), ["năm", "bước"]),
            ("E17 “ép” = chữ f khi câu có f (L05)", canon_heard(["đạo", "hàm", "của", "ép"], ["đạo", "hàm", "của", "f"]),
             ["đạo", "hàm", "của", "f"]),
            ("E17 “ép” KHÔNG thành f khi câu kỳ vọng là từ khác", canon_heard(["bị", "ép", "thành"], ["bị", "nén", "thành"]),
             ["bị", "ép", "thành"]),
            ("E17 “hát” = chữ h khi câu có h (L05)", canon_heard(["cho", "hát", "nhỏ"], ["cho", "h", "nhỏ"]), ["cho", "h", "nhỏ"]),
            ("E17 ASR viết F' = “f phẩy” (L05)", normalize("Vậy F' của ba"), "vậy f phẩy của ba"),
            ("E17 đồng âm giọng Bắc: “da” = “gia” khi gióng hàng (L06)", canon_heard(["da", "cô", "biên", "trong"], ["gia", "cô", "biên", "trong"]),
             ["gia", "cô", "biên", "trong"]),
            ("E17 đồng âm giọng Bắc: “sếp” = “xếp” (L06)", canon_heard(["sếp", "bốn"], ["xếp", "bốn"]), ["xếp", "bốn"]),
            ("E17 KHÔNG coi khác thanh là đồng âm: “giá” ≠ “gia”", canon_heard(["giá", "cô"], ["gia", "cô"]), ["giá", "cô"]),
            ("E17 KHÔNG coi khác nguyên âm là đồng âm: “sắp” ≠ “xấp”", canon_heard(["sắp", "xỉ"], ["xấp", "xỉ"]), ["sắp", "xỉ"]),
            ("E17 “Hexen”/“Jacobin” = cách đọc đã chọn (L06)", canon_heard(["hexen", "là", "jacobin"], ["hết", "sen", "là", "gia", "cô", "biên"]),
             ["hết", "sen", "là", "gia", "cô", "biên"]),
            ("E17 dấu kiểu cũ/mới: xóa = xoá, hòa = hoà", normalize("xóa hòa khỏe thúy"), "xoá hoà khoẻ thuý"),
            ("E17 ASR viết 29% = “29 phần trăm” (L26)", normalize("sai 29%"), "sai hai mươi chín phần trăm"),
            ("E17 ASR viết 19cm = “19 xăng-ti-mét” (L27)", normalize("cao hơn 19cm, đổi sang cm"), normalize("cao hơn 19 xăng-ti-mét, đổi sang xăng-ti-mét"))]:
        ok = got == want
        fails += not ok
        print(f"{'PASS' if ok else 'FAIL'} | {name} (được {got}, kỳ vọng {want})")
    for name, got, want in [
            ("E17 một từ đọc sai bị bắt", both("Ma trận nghịch đảo nhân với A bằng ma trận đơn vị.",
                                               "Ma trận nghịp lý nhân với A bằng ma trận đơn vị.",
                                               "Ma trận nghịch lý nhân với A bằng ma trận đơn vị."), ["đảo"]),
            ("E17 chỉ một mô hình nghe nhầm → không gắn cờ", both("Lấy hàng một của A nhân với cột hai của B.",
                                                                  "Lấy hàng mục của ai nhân với cục 2 của B.",
                                                                  "Lấy hàng một của A nhân với cột hai của B."), []),
            ("E17 tên chữ cái và Vector↔véc tơ không bị coi là sai", both("X chuyển vị nhân vector x.",
                                                                          "Ích chuyển vị nhân Vector ít.",
                                                                          "ít chuyển vị nhân vector x."), [])]:
        ok = got == want
        fails += not ok
        print(f"{'PASS' if ok else 'FAIL'} | {name} (cả hai nghe khác: {got}, kỳ vọng {want})")
    # E21: audio cắt cụt (lỗi thật L05 khung 75: 0,72 s cho 16 từ) phải bị phát hiện; câu bình thường thì không
    import tempfile as _tf, wave as _wave
    with _tf.TemporaryDirectory() as td:
        def mk(sec):
            q = Path(td) / f"{sec}.wav"
            with _wave.open(str(q), "wb") as w:
                w.setnchannels(1); w.setsampwidth(2); w.setframerate(lv.SR); w.writeframes(bytes(2) * int(sec * lv.SR))
            return q
        fr16 = {"tts": "Với hàm vừa rồi, tại điểm 1, 2, grê-đi-ần là véc tơ 8, 3."}
        ok = lv.tts_truncated(fr16, mk(0.72)) and not lv.tts_truncated(fr16, mk(4.2))
    fails += not ok
    print(f"{'PASS' if ok else 'FAIL'} | E21 audio cắt cụt bị phát hiện (0,72 s / 16 từ), câu bình thường không")
    # E20: verify phải thấy audio lỗi thời khi lexicon đổi cách đọc (L05: “gradient” → “grê-đi-ần”, L04 vẫn PASS)
    fa = [{"tts": "véc tơ gờ-ra-đi-ần", "voice": "v", "rate": "-5%"}]
    fb = [{"tts": "véc tơ grê-đi-ần", "voice": "v", "rate": "-5%"}]
    ok = lv.tts_digest(fa) != lv.tts_digest(fb) and lv.tts_digest(fa) == lv.tts_digest([dict(fa[0])])
    fails += not ok
    print(f"{'PASS' if ok else 'FAIL'} | E20 dấu TTS đổi khi lexicon đổi cách đọc, giữ nguyên khi không đổi")
    exp = {15: "mười lăm", 21: "hai mươi mốt", 56: "năm mươi sáu", 105: "một trăm linh năm", 784: "bảy trăm tám mươi bốn",
           1005: "một nghìn không trăm linh năm"}
    bad = {k: num_to_words(k) for k, v in exp.items() if num_to_words(k) != v}
    fails += bool(bad)
    print(f"{'PASS' if not bad else 'FAIL'} | num_to_words {len(exp)} ca {bad or ''}")
    for name, needle in EXPECT.items():
        ok = needle in text
        fails += not ok
        print(f"{'PASS' if ok else 'FAIL'} | bắt được {name}")
    # chữ hai dấu trong công thức → {\char"XXXX} (KaTeX không tự tách dấu); chữ ngoài công thức, chữ một dấu giữ nguyên
    got = lv.katex_safe(r"số $\text{số phòng} + \text{độ}$ $$\text{dốc}$$")
    want = r'số $\text{s{\char"1ED1} phòng} + \text{đ{\char"1ED9}}$ $$\text{d{\char"1ED1}c}$$'
    ok = got == want
    fails += not ok
    print(f"{'PASS' if ok else 'FAIL'} | katex_safe chữ hai dấu trong công thức ({got})")
    import contextlib, io, tempfile
    # lộ trình: bài đứng trước bài cuối đã làm mà thiếu spec phải bị bắt (lỗi thật: L00 bị bỏ sót)
    with tempfile.TemporaryDirectory() as td:
        cp = Path(td) / "cur.yaml"
        cp.write_text("course: T\nlessons:\n  - {id: L00, title: a, requires: []}\n"
                      "  - {id: L01, title: b, requires: [], spec: lessons/cs115/L01_vector_tich_vo_huong_phep_chieu.yaml}\n",
                      encoding="utf-8")
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = lv.cmd_curriculum(str(cp))
    ok = rc == 1 and "L00 chưa có đặc tả" in buf.getvalue()
    fails += not ok
    print(f"{'PASS' if ok else 'FAIL'} | curriculum bắt bài bị bỏ sót (L00 thiếu spec)")
    # Khoá học (CS112 dùng lại số hiệu L00… của CS115): thư mục ra, lộ trình “bài N”, lexicon và sổ ký hiệu phải tách riêng —
    # nếu không, dựng CS112 L00 sẽ ĐÈ out/L00 của CS115, và thêm luật đọc cho CS112 làm video CS115 thành STALE.
    s115, s112 = {"id": "L00"}, {"id": "L00", "course": "CS112"}
    ok = lv.out_dir(s115) == lv.OUT / "CS115" / "L00" and lv.out_dir(s112) == lv.OUT / "CS112" / "L00"
    fails += not ok
    print(f"{'PASS' if ok else 'FAIL'} | khoá học: CS115 → out/CS115/L00, CS112 → out/CS112/L00")
    k115, k112 = lv.lesson_numbers({"id": "L01"})[1], lv.lesson_numbers({"id": "L01", "course": "CS112"})[1]
    ok = k115.get(1, "").startswith("Vector") and k112.get(1, "").startswith("Ký hiệu tiệm cận") and 43 in k115 and 43 not in k112
    fails += not ok
    print(f"{'PASS' if ok else 'FAIL'} | “bài N” tra đúng lộ trình của khoá (CS115 bài 1: “{k115.get(1, '')[:20]}”, CS112 bài 1: “{k112.get(1, '')[:20]}”)")
    base_rules = len(lv.load_yaml(ROOT / "tools" / "registry" / "lexicon_vi.yaml")["rules"])
    ex = ROOT / "tools" / "registry" / "lexicon_vi.CS112.yaml"
    n_ex = len((lv.load_yaml(ex) or {}).get("rules") or []) if ex.exists() else 0
    ok = len(lv.lexicon("CS115")["rules"]) == base_rules and len(lv.lexicon("CS112")["rules"]) == base_rules + n_ex
    fails += not ok
    print(f"{'PASS' if ok else 'FAIL'} | lexicon: CS115 chỉ dùng luật chung ({base_rules}), CS112 thêm {n_ex} luật riêng")
    ok = not any(s["id"] == "bigO" for s in lv.registry("CS115")["symbols"]) and any(s["id"] == "bigO" for s in lv.registry("CS112")["symbols"])
    fails += not ok
    print(f"{'PASS' if ok else 'FAIL'} | sổ ký hiệu: ký hiệu riêng CS112 (O lớn) không lọt vào CS115")
    tpl = (ROOT / "tools" / "templates" / "lesson_template.yaml").read_text(encoding="utf-8")
    with tempfile.TemporaryDirectory() as td:
        tp = Path(td) / "tpl.yaml"
        tp.write_text(tpl.replace("__ID__", "LT").replace("__TITLE__", "t"), encoding="utf-8")
        r = lv.lint(lv.load_spec(tp))
    ok = not r.errors
    fails += not ok
    print(f"{'PASS' if ok else 'FAIL'} | template bài mới lint sạch {r.errors if r.errors else ''}")
    for p in sorted((ROOT / "lessons" / "cs115").glob("*.yaml")) + sorted((ROOT / "lessons" / "cs112").glob("*.yaml")):
        r = lv.lint(lv.load_spec(p))
        ok = not r.errors
        fails += not ok
        print(f"{'PASS' if ok else 'FAIL'} | {p.name} lint sạch ({len(r.errors)} lỗi)")
        for e in r.errors:
            print("     " + e)
    print(f"tests: {fails} FAIL\nchecked_at={lv.now()}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
