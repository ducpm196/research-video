"""Bản đồ bộ định tuyến cho NET L07–L08 — dùng lại audit/cs112/wgraph_svg.py (vô hướng). Cây đường đi ngắn nhất tô xanh,
lấy từ alg.next_hops (không chọn tay). Chạy → audit/net/fig/rt_*.svg"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools")); sys.path.insert(0, str(ROOT / "audit" / "cs112"))
sys.stdout.reconfigure(encoding="utf-8")
import checklib as alg  # noqa: E402
from wgraph_svg import svg  # noqa: E402

POS = {"S": (60, 165), "A": (300, 55), "B": (300, 275), "C": (560, 55), "D": (800, 165)}
E = [("S", "A", 4), ("S", "B", 1), ("A", "C", 1), ("A", "B", 2), ("B", "C", 5), ("B", "D", 8), ("C", "D", 3)]


def tree_edges(edges, src):
    """Cạnh của cây đường đi ngắn nhất từ src: với mỗi đích t, cạnh (prev(t), t) — suy từ next_hops qua chi phí."""
    g = alg.undirected(edges)
    cost = {src: 0} | {t: c for t, (_, c) in alg.next_hops(g, src).items()}
    out = set()
    for t in g:
        if t == src:
            continue
        for u, w in g[t].items():
            if cost[u] + w == cost[t]:
                out.add((u, t) if (u, t, w) in edges else (t, u)); break
    return out


if __name__ == "__main__":
    fig = ROOT / "audit" / "net" / "fig"; fig.mkdir(parents=True, exist_ok=True)
    tr = tree_edges(E, "S")
    assert tr == {("S", "B"), ("A", "B"), ("A", "C"), ("C", "D")}, tr
    hi = {e: "#059669" for e in tr}
    E2 = [(u, v, 10 if {u, v} == {"S", "B"} else w) for u, v, w in E]
    F = {"rt_map": svg(POS, E, directed=False, mid="n1"),
         "rt_tree": svg(POS, E, directed=False, hi=hi, mid="n2"),
         "rt_quiz": svg(POS, E2, directed=False, mid="n3"),
         # L08: đường thẳng A —1— B —1— C; bản “đứt” tô đỏ liên kết A–B
         "dv_line": svg({"A": (80, 70), "B": (330, 70), "C": (580, 70)}, [("A", "B", 1), ("B", "C", 1)], directed=False,
                        w=660, h=140, mid="n4"),
         "dv_cut": svg({"A": (80, 70), "B": (330, 70), "C": (580, 70)}, [("A", "B", "đứt"), ("B", "C", 1)], directed=False,
                       hi={("A", "B"): "#dc2626"}, w=660, h=140, mid="n5")}
    for k, v in F.items():
        (fig / f"{k}.svg").write_text(v, encoding="utf-8")
    print(len(F), "hình →", fig)
