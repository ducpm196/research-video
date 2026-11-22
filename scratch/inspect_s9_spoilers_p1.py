import sys
from pathlib import Path

ROOT = Path(r"D:\research-video")
sys.path.insert(0, str(ROOT / "tools"))
import lv

for c, lid, terms in [
    ("llm", "L00", ["bigram", "ngram", "Fraction"]),
    ("llm", "L01", ["perplexity", "V = 6", "add-1"]),
    ("llm", "L02", ["BPE", "</w>", "Byte"]),
    ("llm", "L05", ["KV", "fp16", "GiB"]),
    ("llm", "L06", ["6ND", "flops", "FLOP"]),
    ("llm", "L11", ["ECE", "maj", "nhị thức"]),
    ("llm", "L12", ["RAG", "recall", "cosin"]),
    ("rln", "L06", ["DQN", "max", "terminal"]),
    ("rln", "L08", ["Actor", "Advantage", "A ="]),
    ("rln", "L12", ["ESS", "w =", "importance"]),
    ("rln", "L13", ["Atari", "Hz", "skiing"]),
]:
    fp = sorted((ROOT / "lessons" / c).glob(f"{lid}_*.yaml"))[0]
    sp = lv.load_spec(fp)
    print(f"=== {c.upper()}:{lid} ===")
    for sc in sp["scenes"]:
        if sc["kind"] in ("practice",):
            print("  practice#0:", sc["steps"][0]["show"][:260])
        for idx, st in enumerate(sc["steps"]):
            sh = st.get("show") or ""
            for t in terms:
                if t.lower() in sh.lower() and sc["kind"] not in ("practice",):
                    print(f"  [{sc['id']}#{idx}] matched '{t}': {sh[:180]!r}")
                    break
