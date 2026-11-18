"""Sinh lại sổ mã trên màn hình của bài BNX CŨ (L12–L23) mà KHÔNG làm mất các mục viết tay: dùng như `lib2.py gen-screen`, nhưng khối nào
không khớp chương trình `prog(...)` thì lấy lại mục cũ theo `sha` (văn bản khối không đổi) và dịch lại khoá `of:` sang khoá mới.
Dùng: python -B audit/bnx/screen_keep.py L12 [L13 …]   (rồi python -B audit/bnx/screen_fast.py L12). Chạy lặp được (tất định).
Khối mới không khớp mục cũ nào và không khớp chương trình nào được liệt kê "CHƯA KHỚP": thêm `prog(...)` hoặc `lib2.other(...)`."""
import importlib
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "audit" / "bnx"))
import lib2  # noqa: E402
import screen_code as sc  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")


def run(lid):
    outp = ROOT / "audit" / "bnx" / "screen" / f"{lid.lower()}.yaml"
    old = yaml.safe_load(outp.read_text(encoding="utf-8")) if outp.exists() else {}
    old_blocks, old_sources = (old or {}).get("blocks") or {}, (old or {}).get("sources") or {}
    importlib.import_module(lid.lower())
    lib2.gen_screen(lid)  # ghi mục khớp chương trình (và liệt kê chưa khớp)
    new = yaml.safe_load(outp.read_text(encoding="utf-8")) or {}
    blocks, sources = new.get("blocks") or {}, new.get("sources") or {}
    f = next((ROOT / "lessons" / "bnx").glob(f"{lid}_*.yaml"))
    _, allb = sc.blocks_of(f)
    sha2key = {}
    for sid, ti, bi, t in allb:
        sha2key.setdefault(sc.digest(t), f"BNX {lid} {sid} {ti} {bi}")
    by_sha = {}
    for k, v in old_blocks.items():
        by_sha.setdefault(v.get("sha"), (k, v))
    miss = []
    for sid, ti, bi, t in allb:
        k = f"BNX {lid} {sid} {ti} {bi}"
        if k in blocks:
            continue
        h = sc.digest(t)
        if h in by_sha:
            ok, ov = by_sha[h]
            e = dict(ov)
            def _remap(key):
                osha = old_blocks.get(key, {}).get("sha")
                return sha2key.get(osha, key)
            if e.get("of"):
                e["of"] = _remap(e["of"])
            if e.get("prelude_keys"):
                e["prelude_keys"] = [_remap(x) for x in e["prelude_keys"]]
            if isinstance(e.get("files"), dict):   # tên tệp → khoá khối đã ghim (WP4 nhánh A)
                e["files"] = {fn: (_remap(r) if isinstance(r, str) and r.startswith("BNX ") else r) for fn, r in e["files"].items()}
            blocks[k] = e
        else:
            miss.append((k, t.split("\n")[0][:80]))
    for n, v in old_sources.items():
        sources.setdefault(n, v)
    hdr = (f"# Sổ mã trên màn hình bài BNX {lid}: mục khớp chương trình prog() sinh bằng audit/bnx/screen_keep.py (lib2.gen_screen), mục khác giữ từ bản viết tay theo sha.\n")
    outp.write_text(hdr + yaml.safe_dump({"blocks": blocks, "sources": sources}, allow_unicode=True, sort_keys=False, width=200), encoding="utf-8", newline="\n")
    print(f"{lid}: {len(allb)} khối, mục {len(blocks)}, nguồn {len(sources)}, chưa khớp {len(miss)}")
    for k, first in miss:
        print("  CHƯA KHỚP", k, "|", first)
    return not miss


if __name__ == "__main__":
    ok = True
    for a in sys.argv[1:]:
        ok = run(a.upper()) and ok
    sys.exit(0 if ok else 1)
