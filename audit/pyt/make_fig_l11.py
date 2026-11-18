"""Sinh audit/pyt/fig_l11.json: dữ liệu THẬT của lệnh hexbin trong bài L11 (cùng mã P_HEX: rng = default_rng(1), 100000 điểm, gridsize=30).
Chạy bằng labs/.venv-pyt (có numpy, matplotlib): labs/.venv-pyt/Scripts/python -B audit/pyt/make_fig_l11.py
l11.py đọc tệp này và vẽ SVG từ toạ độ ô và số đếm thật (không bịa số)."""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(1)
x = rng.normal(size=100000)
y = rng.normal(size=100000)
fig, ax = plt.subplots()
hb = ax.hexbin(x, y, gridsize=30)
off = hb.get_offsets()
cnt = hb.get_array()
verts = hb.get_paths()[0].vertices
out = {
    "n": 100000, "gridsize": 30, "ncell": int(len(cnt)), "total": int(cnt.sum()), "max": int(cnt.max()),
    "xlim": [float(v) for v in ax.get_xlim()], "ylim": [float(v) for v in ax.get_ylim()],
    "hex": [[float(a), float(b)] for a, b in verts],
    "pts1k": [[round(float(a), 3), round(float(b), 3)] for a, b in zip(x[:1000], y[:1000])],  # 1000 điểm đầu của chính mẫu 100 000 điểm
    "cells": [[round(float(o[0]), 5), round(float(o[1]), 5), int(c)] for o, c in zip(off, cnt)],
}
Path(__file__).with_name("fig_l11.json").write_text(json.dumps(out), encoding="utf-8", newline="\n")
print(out["ncell"], out["total"], out["max"], out["xlim"], out["ylim"], len(out["hex"]))
