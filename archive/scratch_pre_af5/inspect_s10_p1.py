from pathlib import Path
import yaml

def find_lines(glob_pat, pat_list):
    for p in sorted(Path("lessons").glob(glob_pat)):
        txt = p.read_text(encoding="utf-8")
        print(f"=== {p.name} ===")
        for kw in pat_list:
            hits = [f"{i}:{l.strip()[:120]}" for i, l in enumerate(txt.splitlines(), 1) if kw in l]
            print(f"  {kw}: {hits[:3]}")

find_lines("hci/L*.yaml", ["px", "O(n)", "10^{-5}", "HTML", "thẻ văn bản"])
find_lines("cas/L05*.yaml", ["check", "{"])
find_lines("cas/L07*.yaml", ["recap", ".*.*=.*"])
find_lines("toc/L14*.yaml", ["{n}", "O(n", "C_4"])
