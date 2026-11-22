from pathlib import Path
import re
import sys

ROOT = Path(r"D:\research-video")
sys.path.insert(0, str(ROOT / "tools"))
import lv

# Shorten L25 >170 sentence cleanly into two crisp sentences
p25 = ROOT / "lessons" / "cs115" / "L25_svm.yaml"
t25 = p25.read_text(encoding="utf-8")
old25 = "Điều kiện KKT và điều kiện bù chứng minh chỉ các điểm sát biên gọi là véc-tơ hỗ trợ mới có trọng số an-pha dương, còn mọi điểm nằm xa hoàn toàn không ảnh hưởng đường biên."
new25 = "Điều kiện KKT và điều kiện bù chứng minh chỉ các điểm sát biên gọi là véc-tơ hỗ trợ mới có trọng số an-pha dương. Mọi điểm nằm xa hoàn toàn không ảnh hưởng đường biên."
if old25 in t25:
    p25.write_text(t25.replace(old25, new25, 1), encoding="utf-8")

bad = []
for i in range(22, 44):
    lid = f"L{i:02d}"
    fp = sorted((ROOT / "lessons" / "cs115").glob(f"{lid}_*.yaml"))[0]
    sp = lv.load_spec(fp)
    w = sum(len((st.get("say") or "").split()) for sc in sp["scenes"] for st in sc["steps"])
    for sc in sp["scenes"]:
        for idx, st in enumerate(sc["steps"]):
            say = st.get("say") or ""
            foc = st.get("focus")
            sents = lv.sentences(say)
            if foc is not None and len(foc) != len(sents):
                bad.append(f"{lid}:{sc['id']}#{idx} focus={len(foc)} != sents={len(sents)}")
            for s in sents:
                if len(s) > 170:
                    bad.append(f"{lid}:{sc['id']}#{idx} len={len(s)} >170: {s}")
                if len(s.split()) > 38:
                    bad.append(f"{lid}:{sc['id']}#{idx} words={len(s.split())} >38: {s}")
                if "càng " in s.lower():
                    bad.append(f"{lid}:{sc['id']}#{idx} 'càng ': {s}")
                if re.search(r"[$_^]", s):
                    bad.append(f"{lid}:{sc['id']}#{idx} TeX: {s}")
    if w < 1645:
        bad.append(f"{lid} words={w} < 1645")
    else:
        print(f"OK {lid}: words={w}", flush=True)

for b in bad:
    print("BAD:", b, flush=True)
assert not bad, f"{len(bad)} violations"
print("ALL 22 CS115 STAGE 9 LESSONS CLEAN!", flush=True)
