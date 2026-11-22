"""AF2/AF4 upgrader cho Stage 9 Batch 2: IRS(14), LLM(15), AGT(13), RLN(14), CVI(13) = 69 bài."""
import sys
from pathlib import Path

ROOT = Path(r"D:\research-video")
sys.path.insert(0, str(ROOT / "audit" / "review"))
sys.path.insert(0, str(ROOT / "audit" / "s9_11"))
import af2_upgrader as up  # noqa: E402
import common  # noqa: E402

COVERS = {
    # IRS (14)
    ("IRS", "L00"): [(1, "example"), (2, "example"), (3, "example")],
    ("IRS", "L01"): [(1, "formula"), (2, "example"), (3, "pitfalls")],
    ("IRS", "L02"): [(1, "formula"), (2, "formula"), (2, "example"), (3, "pitfalls")],
    ("IRS", "L03"): [(1, "formula"), (2, "example"), (3, "pitfalls")],
    ("IRS", "L04"): [(1, "formula"), (1, "example"), (2, "pitfalls"), (3, "check")],
    ("IRS", "L05"): [(1, "formula"), (2, "pitfalls"), (3, "example")],
    ("IRS", "L06"): [(1, "example"), (2, "formula"), (3, "pitfalls")],
    ("IRS", "L07"): [(1, "sym"), (1, "example"), (2, "formula"), (2, "example"), (3, "check"), (3, "practice")],
    ("IRS", "L08"): [(1, "hindsight"), (1, "intuition"), (2, "formula"), (2, "example"), (3, "example")],
    ("IRS", "L09"): [(1, "formula"), (2, "check"), (3, "example")],
    ("IRS", "L10"): [(1, "formula"), (2, "example"), (2, "check"), (3, "online")],
    ("IRS", "L11"): [(1, "example"), (2, "example"), (3, "loop")],
    ("IRS", "L12"): [(1, "example"), (2, "check"), (3, "example"), (4, "quiz")],
    ("IRS", "L13"): [
        (1, "stage1"), (1, "stage2"), (1, "stage3"), (1, "stage4"), (1, "stage5"),
        (2, "check"), (3, "stage5"), (3, "practice"),
    ],
    # LLM (15)
    ("LLM", "L00"): [(1, "example"), (2, "example"), (3, "intuition")],
    ("LLM", "L01"): [(1, 'example'), (2, 'example'), (3, 'check'), (3, 'practice')],
    ("LLM", "L02"): [(1, "example"), (2, "check"), (3, "pitfalls")],
    ("LLM", "L03"): [(1, "sym"), (2, "example"), (3, "pitfalls")],
    ("LLM", "L04"): [(1, "sym"), (2, "example"), (3, "pitfalls")],
    ("LLM", "L05"): [(1, "formula"), (2, "example"), (3, "check"), (4, "check")],
    ("LLM", "L06"): [(1, "example"), (2, "example"), (3, "pitfalls")],
    ("LLM", "L07"): [(1, 'example'), (2, 'example'), (3, 'example'), (3, 'practice')],
    ("LLM", "L08"): [(1, "example"), (2, "example"), (3, "pitfalls")],
    ("LLM", "L09"): [(1, "intuition"), (2, "example"), (3, "pitfalls")],
    ("LLM", "L10"): [(1, "example"), (2, "example"), (3, "pitfalls")],
    ("LLM", "L11"): [(1, "hook"), (1, "pitfalls"), (2, "example"), (3, "example")],
    ("LLM", "L12"): [(1, "intuition"), (2, "example"), (3, "pitfalls")],
    ("LLM", "L13"): [(1, "example"), (2, "example"), (3, "pitfalls")],
    ("LLM", "L14"): [(1, 'stage1'), (1, 'stage2'), (1, 'stage3'), (1, 'stage4'), (1, 'stage5'), (2, 'stage1'), (2, 'stage3'), (2, 'stage4'), (2, 'check'), (3, 'stage5'), (3, 'practice')],
    # AGT (13)
    ("AGT", "L00"): [(1, "sym"), (2, "example"), (3, "pitfalls")],
    ("AGT", "L01"): [(1, "example"), (1, "practice"), (2, "check"), (3, "pitfalls")],
    ("AGT", "L02"): [(1, "sym"), (2, "example"), (3, "check"), (3, "practice")],
    ("AGT", "L03"): [(1, "example"), (2, "practice"), (3, "pitfalls")],
    ("AGT", "L04"): [(1, "example"), (2, "example"), (3, "check"), (3, "practice")],
    ("AGT", "L05"): [(1, "example"), (2, "sym"), (2, "pitfalls"), (3, "pitfalls")],
    ("AGT", "L06"): [(1, "example"), (2, "check"), (3, "pitfalls")],
    ("AGT", "L07"): [(1, "example"), (2, "check"), (3, "practice")],
    ("AGT", "L08"): [(1, "example"), (2, "example"), (3, "pitfalls")],
    ("AGT", "L09"): [(1, "example"), (2, "example"), (3, "pitfalls")],
    ("AGT", "L10"): [(1, "example"), (2, "example"), (3, "pitfalls")],
    ("AGT", "L11"): [(1, "example"), (2, "check"), (3, "practice")],
    ("AGT", "L12"): [
        (1, "stage1"), (1, "stage2"), (1, "stage3"), (1, "stage4"), (1, "stage5"),
        (2, "check"), (3, "stage5"), (3, "practice"),
    ],
    # RLN (14)
    ("RLN", "L00"): [(1, 'sym'), (1, 'intuition'), (2, 'example'), (3, 'formula'), (4, 'check')],
    ("RLN", "L01"): [(1, "sym"), (2, "formula"), (3, "example"), (4, "check")],
    ("RLN", "L02"): [(1, "example"), (2, "formula"), (3, "formula"), (3, "check"), (4, "check")],
    ("RLN", "L03"): [(1, 'formula'), (2, 'formula'), (2, 'example'), (2, 'check'), (3, 'example'), (4, 'check')],
    ("RLN", "L04"): [(1, 'intuition'), (1, 'formula'), (2, 'example'), (3, 'example'), (4, 'check')],
    ("RLN", "L05"): [(1, "formula"), (2, "example"), (3, "pitfalls")],
    ("RLN", "L06"): [(1, 'formula'), (1, 'example'), (2, 'check'), (3, 'formula'), (4, 'pitfalls')],
    ("RLN", "L07"): [(1, "formula"), (2, "example"), (3, "pitfalls")],
    ("RLN", "L08"): [(1, "formula"), (2, "example"), (3, "pitfalls")],
    ("RLN", "L09"): [(1, "example"), (2, "formula"), (3, "pitfalls"), (4, "check")],
    ("RLN", "L10"): [(1, "example"), (2, "formula"), (3, "penalty"), (4, "pitfalls")],
    ("RLN", "L11"): [(1, 'example'), (2, 'check'), (3, 'concept'), (4, 'check'), (4, 'practice')],
    ("RLN", "L12"): [(1, "example"), (2, "example"), (3, "check"), (4, "pitfalls"), (4, "quiz")],
    ("RLN", "L13"): [(1, 'stage1'), (1, 'stage2'), (1, 'stage3'), (1, 'stage4'), (1, 'stage5'), (2, 'check'), (3, 'stage4'), (3, 'stage5'), (3, 'practice')],
    # CVI (13)
    ("CVI", "L00"): [(1, 'formula'), (2, 'formula'), (3, 'example'), (3, 'check'), (4, 'pitfalls')],
    ("CVI", "L01"): [(1, "example"), (2, "formula"), (3, "blur"), (4, "pitfalls")],
    ("CVI", "L02"): [(1, "example"), (2, "formula"), (3, "equalize"), (4, "pitfalls")],
    ("CVI", "L03"): [(1, 'formula'), (2, 'formula'), (3, 'example'), (4, 'check')],
    ("CVI", "L04"): [(1, "formula"), (2, "example"), (3, "example"), (4, "pitfalls")],
    ("CVI", "L05"): [(1, 'intuition'), (2, 'concept'), (3, 'formula'), (4, 'check'), (4, 'practice')],
    ("CVI", "L06"): [(1, 'row'), (2, 'example'), (3, 'formula'), (4, 'check')],
    ("CVI", "L07"): [(1, "formula"), (2, "example"), (3, "example"), (4, "pitfalls")],
    ("CVI", "L08"): [(1, 'formula'), (2, 'nms'), (3, 'example'), (4, 'threshold')],
    ("CVI", "L09"): [(1, "example"), (2, "formula"), (3, "rare"), (4, "pitfalls")],
    ("CVI", "L10"): [(1, 'intuition'), (2, 'formula'), (3, 'example'), (4, 'check'), (4, 'practice')],
    ("CVI", "L11"): [(1, 'example'), (2, 'counterfactual'), (3, 'pitfalls'), (4, 'counterfactual')],
    ("CVI", "L12"): [
        (1, "stage1"), (1, "stage2"), (1, "stage3"), (1, "stage4"), (1, "stage5"), (1, "stage6"),
        (2, "check"), (3, "stage6"), (3, "practice"),
    ],
}

DATA = {
    "IRS": [
        ("L00", "Tính P@k, R@k và hạng nghịch đảo trung bình từ danh sách hạng",
         "# Lab IRS L00 — Độ đo truy hồi: độ chuẩn xác, độ phủ và hạng nghịch đảo trung bình\n\n"
         "Kho có `T = 6` tài liệu đúng; hệ A trả kết quả đúng tại vị trí `[2, 4, 7]`, hệ B trả tại `[3, 5, 8]`. "
         "Viết hàm tính `P@k = số đúng trong k đầu / k` và `R@k = số đúng trong k đầu / T` (không gán cứng đáp số), rồi tính hạng nghịch đảo trung bình trên 3 câu hỏi có hạng đúng đầu tiên là `[2, 4, None]` (câu không tìm thấy có hạng nghịch đảo `0`).\n\n"
         "Định dạng đầu ra (2 dòng):\n`A_P5=<1 chữ số> R5=<1 chữ số> R10=<1 chữ số> B_P3=<1 chữ số>`\n`MRR_3=<4 chữ số>`",
         "hits = lambda ranks, k: sum(1 for r in ranks if r <= k)\n"
         "ranks_a, ranks_b, total = [2, 4, 7], [3, 5, 8], 6\n"
         "p5 = hits(ranks_a, 5) / 5\n"
         "r5, r10 = hits(ranks_a, 5) / total, hits(ranks_a, 10) / total\n"
         "p3_b = hits(ranks_b, 3) / 3\n"
         "first_pos = [2, 4, None]\n"
         "mrr = sum(0.0 if p is None else 1.0 / p\n"
         "          for p in first_pos) / len(first_pos)\n"
         "print(f\"A_P5={p5:.1f} R5={r5:.1f} R10={r10:.1f} B_P3={p3_b:.1f}\")\n"
         "print(f\"MRR_3={mrr:.4f}\")"),
        ("L01", "Tính DCG@4 và nDCG@4 không làm tròn giữa chừng",
         "# Lab IRS L01 — Độ lợi tích lũy có chiết khấu và chuẩn hoá (nDCG)\n\n"
         "Tính độ lợi tích lũy có chiết khấu tại 4 vị trí đầu (`DCG@4`) cho dãy mức liên quan `[2, 3, 1, 2]` và bản lý tưởng toàn kho `IDCG@4` cho dãy sắp xếp giảm dần theo công thức `sum(rel / log2(vị trí + 1))` với vị trí đếm từ 1. Không làm tròn trung gian.\n\n"
         "Định dạng đầu ra (1 dòng):\n`DCG=<5 chữ số> IDCG=<5 chữ số> nDCG=<5 chữ số>`",
         "import math\n"
         "dcg = lambda rels: sum(r / math.log2(i + 2) for i, r in enumerate(rels))\n"
         "rels = [2, 3, 1, 2]\n"
         "d = dcg(rels)\n"
         "idcg = dcg(sorted(rels, reverse=True))\n"
         "print(f\"DCG={d:.5f} IDCG={idcg:.5f} nDCG={d/idcg:.5f}\")"),
        ("L02", "Tính TF-IDF theo số văn bản chứa từ df và cosin từ kho 3 câu",
         "# Lab IRS L02 — Mô hình không gian vector: trọng số từ hiếm và cosin\n\n"
         "Cho kho 3 văn bản `docs = ['xe dap nhanh', 'xe dien ben', 'xe dien dep']` với câu hỏi `'xe dien'`. "
         "Viết mã đếm số văn bản chứa mỗi từ (`df`), tính độ hiếm `idf = ln(N / df)` cho mọi từ trong từ vựng `['xe', 'dap', 'nhanh', 'dien', 'ben', 'dep']`, dựng vector TF-IDF (`tf * idf`) của câu hỏi và hai văn bản `'xe dien ben'`, `'xe dien dep'`, rồi tính độ tương tự cosin giữa câu hỏi với từng văn bản đó.\n\n"
         "Định dạng đầu ra (1 dòng):\n`idf_xe=<1 chữ số> idf_dien=<3 chữ số> cos_d2=<3 chữ số> cos_d3=<3 chữ số>`",
         "import math\n"
         "docs = ['xe dap nhanh', 'xe dien ben', 'xe dien dep']\n"
         "vocab = ['xe', 'dap', 'nhanh', 'dien', 'ben', 'dep']\n"
         "df = {w: sum(1 for d in docs if w in d.split()) for w in vocab}\n"
         "idf = {w: math.log(len(docs) / df[w]) for w in vocab}\n"
         "vec = lambda s: [s.split().count(w) * idf[w] for w in vocab]\n"
         "cos = lambda a, b: (\n"
         "    sum(x * y for x, y in zip(a, b)) / (math.hypot(*a) * math.hypot(*b))\n"
         ")\n"
         "vq, vd2, vd3 = vec('xe dien'), vec(docs[1]), vec(docs[2])\n"
         "print(f\"idf_xe={idf['xe']:.1f} idf_dien={idf['dien']:.3f}\",\n"
         "      f\"cos_d2={cos(vq, vd2):.3f} cos_d3={cos(vq, vd3):.3f}\")"),
        ("L03", "Ước lượng số phép so chia cụm tìm láng giềng gần đúng",
         "# Lab IRS L03 — Truy hồi dày và tìm láng giềng gần đúng theo cụm\n\n"
         "Cho kho `2_000_000` vector chia thành `1_000` cụm đều nhau. Khi truy vấn dò `8` cụm có tâm gần nhất, tính tổng số phép so cần thực hiện (gồm bước so với mọi tâm cụm cộng với duyệt các vector trong cụm đã chọn) và hệ số tăng tốc so với duyệt toàn bộ kho.\n\n"
         "Định dạng đầu ra (1 dòng):\n`ivf_ops=<số nguyên> speedup=<1 chữ số>x`",
         "exact = 2_000_000\n"
         "ivf = 1000 + 8 * (exact // 1000)\n"
         "print(f\"ivf_ops={ivf} speedup={exact / ivf:.1f}x\")"),
        ("L04", "Hợp nhất thứ hạng hai danh sách tìm kiếm (k=60)",
         "# Lab IRS L04 — Truy hồi lai và hợp nhất thứ hạng\n\n"
         "Với hằng số `k = 60`, tài liệu A đứng hạng `1` và `4` ở hai danh sách; tài liệu B đứng hạng `2` và `2`. Tính điểm hợp nhất `1/(k + hạng_1) + 1/(k + hạng_2)` cho A, B và xác định bên thắng.\n\n"
         "Định dạng đầu ra (1 dòng):\n`score_A=<5 chữ số> score_B=<5 chữ số> win=<A hoặc B>`",
         "rrf = lambda r1, r2, k=60: 1.0 / (k + r1) + 1.0 / (k + r2)\n"
         "sa, sb = rrf(1, 4), rrf(2, 2)\n"
         "print(f\"score_A={sa:.5f} score_B={sb:.5f} win={'B' if sb > sa else 'A'}\")"),
        ("L05", "Tính mất mát theo cặp và cái giá DCG khi đổi chỗ vị trí đầu",
         "# Lab IRS L05 — Học để xếp hạng: mất mát theo cặp và trọng số vị trí đầu\n\n"
         "Tính mất mát theo cặp `ln(1 + exp(-(s_a - s_b)))` khi hai điểm đúng thứ tự `(s_a=2.5, s_b=1.2)` so với đảo ngược `(1.2, 2.5)`. Sau đó tính độ giảm DCG khi tráo cặp vị trí `(1, 2)` (mức `4` và `2`) so với cặp `(3, 4)` (mức `1` và `0`) trong dãy `[4, 2, 1, 0]`.\n\n"
         "Định dạng đầu ra (2 dòng):\n`loss_ok=<3 chữ số> loss_swap=<3 chữ số>`\n`dcg_drop_12=<3 chữ số> dcg_drop_34=<3 chữ số>`",
         "import math\n"
         "loss_ok = math.log1p(math.exp(-(2.5 - 1.2)))\n"
         "loss_bad = math.log1p(math.exp(-(1.2 - 2.5)))\n"
         "swap12 = (4 - 2) * (1 / math.log2(2) - 1 / math.log2(3))\n"
         "swap34 = (1 - 0) * (1 / math.log2(4) - 1 / math.log2(5))\n"
         "print(f\"loss_ok={loss_ok:.3f} loss_swap={loss_bad:.3f}\")\n"
         "print(f\"dcg_drop_12={swap12:.3f} dcg_drop_34={swap34:.3f}\")"),
        ("L06", "Tính cosin láng giềng theo trọng số điểm chung và dự đoán",
         "# Lab IRS L06 — Lọc cộng tác theo láng giềng và trọng số cosin\n\n"
         "Cho vector điểm chấm `U = (4, 2, 0)` (`0` nghĩa là chưa chấm), `V = (5, 0, 3)`, `W = (1, 3, 5)`. Viết hàm tính độ tương tự cosin trực tiếp `sum(u*v) / (||u||*||v||)` từ hai vector rồi dự đoán điểm món thứ 3 cho `U` theo công thức trung bình có trọng số `(cosUV*r_V3 + cosUW*r_W3) / (cosUV + cosUW)`.\n\n"
         "Định dạng đầu ra (1 dòng):\n`cosUV=<3 chữ số> cosUW=<3 chữ số> pred_u3=<2 chữ số>`",
         "import math\n"
         "cos = lambda a, b: (\n"
         "    sum(x * y for x, y in zip(a, b)) / (math.hypot(*a) * math.hypot(*b))\n"
         ")\n"
         "u, v, w = (4.0, 2.0, 0.0), (5.0, 0.0, 3.0), (1.0, 3.0, 5.0)\n"
         "c_uv, c_uw = cos(u, v), cos(u, w)\n"
         "pred_u3 = (c_uv * v[2] + c_uw * w[2]) / (c_uv + c_uw)\n"
         "print(f\"cosUV={c_uv:.3f} cosUW={c_uw:.3f} pred_u3={pred_u3:.2f}\")"),
        ("L07", "Một bước cập nhật vector tiềm ẩn có và không có chính quy hoá λ",
         "# Lab IRS L07 — Phân rã ma trận bằng dốc ngẫu nhiên (SGD)\n\n"
         "Với `p = [1.5, 0.5]`, `q = [1.0, 2.0]`, điểm thật `r = 4.0`, tốc độ học `eta = 0.2`, tính sai số dự đoán `err = r - dot(p, q)` (với `dot` là tích vô hướng `sum(a*b)`) và áp dụng quy tắc cập nhật `p_i <- p_i + eta * (err * q_i - lam * p_i)` cho hai trường hợp `lam = 0` và `lam = 0.05` (mọi toạ độ làm tròn `round(..., 4)`).\n\n"
         "Định dạng đầu ra (1 dòng):\n`err=<1 chữ số> p_raw=[<4 chữ số>, <4 chữ số>] p_reg=[<4 chữ số>, <4 chữ số>]`",
         "p, q, r, eta = [1.5, 0.5], [1.0, 2.0], 4.0, 0.2\n"
         "err = r - sum(a * b for a, b in zip(p, q))\n"
         "p0 = [round(pi + eta * err * qi, 4) for pi, qi in zip(p, q)]\n"
         "p_reg = [\n"
         "    round(pi + eta * (err * qi - 0.05 * pi), 4) for pi, qi in zip(p, q)\n"
         "]\n"
         "print(f\"err={err:.1f} p_raw={p0} p_reg={p_reg}\")"),
        ("L08", "Lấy mẫu âm theo tần suất mũ 0,75 và bù lôgarit tự nhiên -ln(p)",
         "# Lab IRS L08 — Phản hồi ngầm, lấy mẫu âm mũ 0.75 và bù trừ tần suất\n\n"
         "Với video A xuất hiện `200` lần và B `2` lần, tính xác suất B được lấy làm mẫu âm theo tần suất thô so với tần suất mũ `0.75`, rồi tính hệ số bù lôgarit tự nhiên `-ln(0.01)`.\n\n"
         "Định dạng đầu ra (1 dòng):\n`raw_B=<3 chữ số> pow075_B=<3 chữ số> logq_corr=<3 chữ số>`",
         "import math\n"
         "p_raw = 2.0 / (200.0 + 2.0)\n"
         "p_pow = (2.0 ** 0.75) / (200.0 ** 0.75 + 2.0 ** 0.75)\n"
         "corr = -math.log(0.01)\n"
         "print(f\"raw_B={p_raw:.3f} pow075_B={p_pow:.3f} logq_corr={corr:.3f}\")"),
        ("L09", "Tính trung bình và độ lệch chuẩn phân phối Beta(a, b)",
         "# Lab IRS L09 — Khởi động lạnh với phân phối Beta\n\n"
         "So sánh trung bình và độ lệch chuẩn của phân phối `Beta(1, 1)` (sản phẩm mới chưa có dữ liệu) với `Beta(31, 471)` (sản phẩm cũ có 30 bấm trên 500 hiển thị).\n\n"
         "Định dạng đầu ra (2 dòng):\n`new_mean=<2 chữ số> new_sd=<3 chữ số>`\n`old_mean=<4 chữ số> old_sd=<4 chữ số>`",
         "import math\n"
         "stat = lambda a, b: (\n"
         "    a / (a + b), math.sqrt(a * b / ((a + b) ** 2 * (a + b + 1)))\n"
         ")\n"
         "m1, s1 = stat(1, 1)\n"
         "m2, s2 = stat(31, 471)\n"
         "print(f\"new_mean={m1:.2f} new_sd={s1:.3f}\")\n"
         "print(f\"old_mean={m2:.4f} old_sd={s2:.4f}\")"),
        ("L10", "Khử thiên lệch vị trí bằng trọng số nghịch đảo xu hướng (IPS)",
         "# Lab IRS L10 — Khử thiên lệch vị trí bằng trọng số nghịch đảo xu hướng\n\n"
         "Biết xác suất được nhìn thấy ở vị trí 1 là `0.9` và ở vị trí 4 là `0.25`. Chuẩn hoá tỉ lệ bấm quan sát được `0.045` (ở vị trí 1) và `0.020` (ở vị trí 4) bằng cách chia cho xác suất được nhìn thấy.\n\n"
         "Định dạng đầu ra (1 dòng):\n`ips_rel_pos1=<3 chữ số> ips_rel_pos4=<3 chữ số>`",
         "rel_pos1 = 0.045 / 0.9\n"
         "rel_pos4 = 0.020 / 0.25\n"
         "print(f\"ips_rel_pos1={rel_pos1:.3f} ips_rel_pos4={rel_pos4:.3f}\")"),
        ("L11", "Tính điểm cân bằng liên quan – đa dạng (MMR, λ = 0.6)",
         "# Lab IRS L11 — Cân bằng độ liên quan với độ đa dạng (MMR)\n\n"
         "Theo công thức `lam * liên_quan - (1 - lam) * giống_đã_chọn` với `lam = 0.6`, so sánh ứng viên `X` (liên quan `0.95`, giống `0.85`) với `Y` (liên quan `0.75`, giống `0.15`).\n\n"
         "Định dạng đầu ra (1 dòng):\n`mmr_X=<3 chữ số> mmr_Y=<3 chữ số> pick=<X hoặc Y>`",
         "mmr = lambda rel, sim, l=0.6: l * rel - (1.0 - l) * sim\n"
         "sx, sy = mmr(0.95, 0.85), mmr(0.75, 0.15)\n"
         "print(f\"mmr_X={sx:.3f} mmr_Y={sy:.3f} pick={'Y' if sy > sx else 'X'}\")"),
        ("L12", "Kiểm ngân sách phân vị 99 trong kiến trúc hai tầng và đuôi song song 8 mảnh",
         "# Lab IRS L12 — Thiết kế hệ gợi ý hai tầng trong ngân sách 100 ms\n\n"
         "Tính độ trễ phân vị 99 khi cắt ứng viên từ `1 200` xuống `500` (biết sinh ứng viên tốn `18 ms`, mạng đọc đặc trưng `22 ms`, và tầng xếp hạng tốn `0.06 ms` mỗi ứng viên ở phân vị 99), rồi tính xác suất một yêu cầu gặp đuôi chậm khi chia `8` mảnh song song mà mỗi mảnh chậm `1.5%`.\n\n"
         "Định dạng đầu ra (1 dòng):\n`p99_before=<số nguyên>ms p99_after=<số nguyên>ms tail8=<1 chữ số>%`",
         "t_before = 18 + 1200 * 0.06 + 22\n"
         "t_after = 18 + 500 * 0.06 + 22\n"
         "tail8 = (1.0 - 0.985 ** 8) * 100\n"
         "print(\n"
         "    f\"p99_before={t_before:.0f}ms p99_after={t_after:.0f}ms \"\n"
         "    f\"tail8={tail8:.1f}%\"\n"
         ")"),
        ("L13", "Tính bộ nhớ bảng nhúng (MiB), lượt xem mỗi người và bù tần suất",
         "# Lab IRS L13 — Hành trình gợi ý video: từ 2008 tới hệ hai tầng\n\n"
         "Tính dung lượng (đơn vị `MiB`, biết `1 MiB = 1024^2 = 1 048 576 byte`) của bảng vector `2 triệu` video × `128` số thực 32 bit (`float32`, mỗi số `4 byte`), số lượt xem trung bình mỗi người ở nhóm `18.0 triệu lượt / 1.5 triệu người`, và hệ số bù `-ln(0.05)`.\n\n"
         "Định dạng đầu ra (1 dòng):\n`emb_mib=<1 chữ số> views_u=<1 chữ số> log_corr=<3 chữ số>`",
         "import math\n"
         "mem_mb = 2_000_000 * 128 * 4 / (1024 ** 2)\n"
         "vpu = 18.0 / 1.5\n"
         "print(\n"
         "    f\"emb_mib={mem_mb:.1f} views_u={vpu:.1f} \"\n"
         "    f\"log_corr={-math.log(0.05):.3f}\"\n"
         ")"),
    ],
    "LLM": [
        ("L00", "Đếm cặp từ kế tiếp (bigram) từ 3 câu để tính xác suất chuỗi chính xác",
         "# Lab LLM L00 — Mô hình ngôn ngữ và quy tắc chuỗi\n\n"
         "Từ kho 3 câu `['<s> em hoc toan </s>', '<s> em hoc ly </s>', '<s> anh hoc toan </s>']`, đếm tần suất mọi cặp từ kế tiếp (bigram) và tự tính xác suất chính xác bằng phân số `Fraction` cho câu `'<s> em hoc toan </s>'`.\n\n"
         "Định dạng đầu ra (1 dòng):\n`prob=<phân số> float=<4 chữ số>`",
         "from fractions import Fraction\n"
         "from collections import Counter\n"
         "raw = ('<s> em hoc toan </s>', '<s> em hoc ly </s>', '<s> anh hoc toan </s>')\n"
         "sents = [s.split() for s in raw]\n"
         "uni = Counter(w for s in sents for w in s[:-1])\n"
         "bi = Counter((a, b) for s in sents for a, b in zip(s, s[1:]))\n"
         "target = '<s> em hoc toan </s>'.split()\n"
         "p = Fraction(1, 1)\n"
         "for a, b in zip(target, target[1:]):\n"
         "    p *= Fraction(bi[(a, b)], uni[a])\n"
         "print(f\"prob={p} float={float(p):.4f}\")"),
        ("L01", "Tính độ hỗn loạn và xác suất làm trơn cộng 1 từ số đếm rõ",
         "# Lab LLM L01 — Mô hình n-gram, làm trơn cộng một và độ hỗn loạn\n\n"
         "Một câu `3` bước dự đoán có xác suất `8/27`: tính độ hỗn loạn `(8/27)^(-1/3)`. Sau đó tính xác suất cặp chưa từng gặp khi ngữ cảnh đứng trước đã xuất hiện `3` lần trong kho và bộ từ vựng có `V = 7` từ (làm trơn cộng 1: `(0 + 1) / (3 + 7)`).\n\n"
         "Định dạng đầu ra (1 dòng):\n`perplexity=<3 chữ số> add1_unseen=<3 chữ số>`",
         "p = 8.0 / 27.0\n"
         "ppl = p ** (-1.0 / 3.0)\n"
         "p_unseen_add1 = (0 + 1) / (3 + 7)\n"
         "print(f\"perplexity={ppl:.3f} add1_unseen={p_unseen_add1:.3f}\")"),
        ("L02", "Chạy 2 bước gộp cặp theo đúng quy tắc: hoà tần suất chọn cặp gặp trước",
         "# Lab LLM L02 — Tách từ tố: mã hoá cặp byte (BPE)\n\n"
         "Trên từ điển tần suất `{'s t a r </w>': 7, 's t a r t </w>': 4, 'c a r </w>': 3, 'f a r </w>': 2}`, chạy 2 bước học luật gộp liên tiếp. Quy tắc: chọn cặp liền nhau có tổng tần suất cao nhất; nếu nhiều cặp hoà tần suất thì chọn cặp xuất hiện đầu tiên.\n\n"
         "Định dạng đầu ra (2 dòng):\n`merge1=<a+b> freq=<số nguyên>`\n`merge2=<a+b> freq=<số nguyên>`",
         "from collections import Counter\n"
         "vocab = {\n"
         "    's t a r </w>': 7, 's t a r t </w>': 4,\n"
         "    'c a r </w>': 3, 'f a r </w>': 2,\n"
         "}\n"
         "for step in (1, 2):\n"
         "    pairs = Counter()\n"
         "    for w, f in vocab.items():\n"
         "        syms = w.split()\n"
         "        for a, b in zip(syms, syms[1:]):\n"
         "            pairs[(a, b)] += f\n"
         "    best = max(pairs, key=pairs.__getitem__)\n"
         "    print(f\"merge{step}={best[0]}+{best[1]} freq={pairs[best]}\")\n"
         "    pair_s, merged_s = f\"{best[0]} {best[1]}\", \"\".join(best)\n"
         "    vocab = {w.replace(pair_s, merged_s): f for w, f in vocab.items()}"),
        ("L03", "Tính độ tương tự cosin giữa vector nhúng và kiểm cặp vuông góc",
         "# Lab LLM L03 — Vector nhúng và độ tương tự cosin\n\n"
         "Tính độ tương tự cosin giữa vector `(2, 1, 0)` với `(3, 2, 1)` và với vector vuông góc `(-1, 2, 0)`.\n\n"
         "Định dạng đầu ra (1 dòng):\n`cos_sim=<3 chữ số> cos_orth=<1 chữ số>`",
         "import math\n"
         "cos = lambda u, v: (\n"
         "    sum(a * b for a, b in zip(u, v)) / (math.hypot(*u) * math.hypot(*v))\n"
         ")\n"
         "c1 = cos((2, 1, 0), (3, 2, 1))\n"
         "c2 = cos((2, 1, 0), (-1, 2, 0))\n"
         "print(f\"cos_sim={c1:.3f} cos_orth={c2:.1f}\")"),
        ("L04", "Đếm số ô hợp lệ trong mặt nạ nhân quả tam giác dưới",
         "# Lab LLM L04 — Transformer giải mã và mặt nạ nhân quả\n\n"
         "Tính số cặp `(vị_trí_đọc, vị_trí_nhìn)` hợp lệ `n * (n + 1) // 2` trên tổng `n * n` ô cho chuỗi `n = 6` và `n = 12` từ tố.\n\n"
         "Định dạng đầu ra (2 dòng):\n`n=6 allowed=<hợp lệ>/<tổng>`\n`n=12 allowed=<hợp lệ>/<tổng>`",
         "for n in (6, 12):\n"
         "    allowed = n * (n + 1) // 2\n"
         "    print(f\"n={n} allowed={allowed}/{n * n}\")"),
        ("L05", "Tính dung lượng bộ nhớ đệm khoá–giá trị ở 16 bit (fp16)",
         "# Lab LLM L05 — Chi phí bộ nhớ đệm khoá–giá trị (KV cache)\n\n"
         "Cho mô hình `24` tầng, kích thước ẩn `2 048`, độ dài ngữ cảnh `8 192` từ tố, lưu dạng nửa độ chính xác 16 bit (`2 byte` mỗi số). Tính tổng byte và GiB (`1 GiB = 1024^3 byte`) của bộ nhớ đệm khoá–giá trị cho 1 chuỗi.\n\n"
         "Định dạng đầu ra (1 dòng):\n`kv_bytes=<số nguyên> kv_GiB=<1 chữ số>`",
         "bytes_kv = 2 * 24 * 2048 * 8192 * 2\n"
         "gib_kv = bytes_kv / (1024 ** 3)\n"
         "print(f\"kv_bytes={bytes_kv} kv_GiB={gib_kv:.1f}\")"),
        ("L06", "Tính độ hỗn loạn từ mất mát entropy chéo và ước lượng phép tính C ≈ 6ND",
         "# Lab LLM L06 — Huấn luyện trước: mất mát và quy luật mở rộng\n\n"
         "Tính độ hỗn loạn `exp(1.5)` khi mất mát bằng `1.5` (cơ số e), và ước lượng số phép tính `C ≈ 6 * N * D` cho mô hình `8 tỉ` tham số huấn luyện trên `200 tỉ` từ tố.\n\n"
         "Định dạng đầu ra (1 dòng):\n`ppl=<2 chữ số> flops=<dạng e khoa học 2 chữ số>`",
         "import math\n"
         "ppl = math.exp(1.5)\n"
         "flops = 6 * 8e9 * 2.0e11\n"
         "print(f\"ppl={ppl:.2f} flops={flops:.2e}\")"),
        ("L07", "Tính Softmax theo nhiệt độ và lọc tích lũy top-p động (>= 0.85)",
         "# Lab LLM L07 — Sinh văn bản: nhiệt độ và lấy mẫu hạt nhân top-p\n\n"
         "Cho dãy điểm thô `(3, 1.5, 0)`. Tính phân phối chuẩn hoá mũ (Softmax) ở nhiệt độ `T = 1.0` và `T = 0.6`. Sau đó cộng dồn xác suất lớn nhất ở `T = 1.0` theo danh sách giảm dần cho tới khi tổng `>= 0.85` và in tổng đó.\n\n"
         "Định dạng đầu ra (1 dòng):\n`T1=[<3 số làm tròn 3 chữ số>] T06=[<3 số làm tròn 3 chữ số>] top_p_sum=<3 chữ số>`",
         "import math\n"
         "def sm_raw(logits, t):\n"
         "    exps = [math.exp(z / t) for z in logits]\n"
         "    tot = sum(exps)\n"
         "    return [v / tot for v in exps]\n"
         "r1, r06 = sm_raw((3.0, 1.5, 0.0), 1.0), sm_raw((3.0, 1.5, 0.0), 0.6)\n"
         "acc = 0.0\n"
         "for v in sorted(r1, reverse=True):\n"
         "    acc += v\n"
         "    if acc >= 0.85:\n"
         "        break\n"
         "p1 = [round(v, 3) for v in r1]\n"
         "p06 = [round(v, 3) for v in r06]\n"
         "print(f\"T1={p1} T06={p06} top_p_sum={acc:.3f}\")"),
        ("L08", "Đếm tham số tinh chỉnh toàn bộ vs hạng thấp (LoRA, hạng 16)",
         "# Lab LLM L08 — Tinh chỉnh toàn bộ tham số và tinh chỉnh hạng thấp (LoRA)\n\n"
         "Xét một ma trận vuông `2048 × 2048`: tính tổng tham số khi tinh chỉnh toàn bộ, số tham số khi phân tích thành hai ma trận hạng `r = 16` (`2 * 2048 * 16`), và tỉ lệ phần trăm so với toàn bộ.\n\n"
         "Định dạng đầu ra (1 dòng):\n`full=<số nguyên> lora=<số nguyên> ratio=<2 chữ số>%`",
         "full = 2048 * 2048\n"
         "lora = 2 * 2048 * 16\n"
         "print(f\"full={full} lora={lora} ratio={lora / full * 100:.2f}%\")"),
        ("L09", "Tính xác suất chọn và mất mát mô hình phần thưởng Bradley–Terry",
         "# Lab LLM L09 — Học theo chỉ dẫn và căn chỉnh theo sở thích con người\n\n"
         "Cho chênh lệch điểm phần thưởng `r_A - r_B = 1.5`. Tính xác suất người chấm chọn câu trả lời A qua hàm xích-ma `1 / (1 + exp(-1.5))` và mất mát `-ln(p)`.\n\n"
         "Định dạng đầu ra (1 dòng):\n`bt_prob=<3 chữ số> bt_loss=<3 chữ số>`",
         "import math\n"
         "p = 1.0 / (1.0 + math.exp(-1.5))\n"
         "loss = -math.log(p)\n"
         "print(f\"bt_prob={p:.3f} bt_loss={loss:.3f}\")"),
        ("L10", "Tính biên độ khoảng tin cậy 95% của độ chính xác trên bộ kiểm tra",
         "# Lab LLM L10 — Đánh giá mô hình ngôn ngữ và khoảng tin cậy\n\n"
         "Một bộ kiểm tra có `n = 800` câu độc lập, mô hình trả lời đúng `78%` (`p = 0.78`). Tính biên độ khoảng tin cậy 95% `1.96 * sqrt(p * (1 - p) / n) * 100` (đơn vị điểm phần trăm).\n\n"
         "Định dạng đầu ra (1 dòng):\n`acc=<1 chữ số>% margin_pp=<2 chữ số>`",
         "import math\n"
         "p, n = 0.78, 800\n"
         "me = 1.96 * math.sqrt(p * (1 - p) / n) * 100\n"
         "print(f\"acc={p * 100:.1f}% margin_pp={me:.2f}\")"),
        ("L11", "Tính xác suất biểu quyết đa số 7 lần độc lập bằng phân phối nhị thức",
         "# Lab LLM L11 — Ảo giác, hiệu chuẩn và tự nhất quán\n\n"
         "Giả sử mỗi lần sinh trả lời đúng độc lập với xác suất `p = 0.65`. Dùng tổng nhị thức `k = 4..7` trong 7 lần thử để tính xác suất đáp án đa số đúng.\n\n"
         "Định dạng đầu ra (1 dòng):\n`single=<3 chữ số> maj7_indep=<3 chữ số>`",
         "import math\n"
         "p = 0.65\n"
         "maj7 = sum(\n"
         "    math.comb(7, k) * (p ** k) * ((1 - p) ** (7 - k))\n"
         "    for k in range(4, 8)\n"
         ")\n"
         "print(f\"single={p:.3f} maj7_indep={maj7:.3f}\")"),
        ("L12", "Truy xuất 1 đoạn tốt nhất bằng cosin và tính recall@1 tự động",
         "# Lab LLM L12 — Sinh có truy xuất (RAG): chỉ mục và tìm kiếm\n\n"
         "Cho vector câu hỏi `q = [2, 1, 0]`, hai đoạn văn trong kho `'docA': [3, 2, 1]` và `'docB': [0, 1, 4]`, trong đó nhãn đúng là `'docA'`. Viết mã tìm đoạn có độ tương tự cosin lớn nhất và tự kiểm tra `best == 'docA'` để tính `recall@1` (không gán cứng `1.0`).\n\n"
         "Định dạng đầu ra (1 dòng):\n`top1=<tên đoạn> cos=<3 chữ số> recall_at_1=<1 chữ số>`",
         "import math\n"
         "cos = lambda u, v: (\n"
         "    sum(a * b for a, b in zip(u, v)) / (math.hypot(*u) * math.hypot(*v))\n"
         ")\n"
         "q, relevant = [2, 1, 0], 'docA'\n"
         "docs = {'docA': [3, 2, 1], 'docB': [0, 1, 4]}\n"
         "best = max(docs, key=lambda k: cos(q, docs[k]))\n"
         "r1 = float(best == relevant)\n"
         "print(f\"top1={best} cos={cos(q, docs[best]):.3f} recall_at_1={r1:.1f}\")"),
        ("L13", "Tính hệ số tăng bộ nhớ đệm và phép tính chú ý khi mở rộng 2k -> 24k",
         "# Lab LLM L13 — Ngữ cảnh dài và suy luận hiệu quả\n\n"
         "Khi tăng độ dài ngữ cảnh từ `2 000` (2k) lên `24 000` (24k) từ tố, tính hệ số nhân của bộ nhớ đệm khoá–giá trị (tuyến tính theo `n`) và hệ số nhân của phép tính chú ý (tỉ lệ bậc hai `n^2`).\n\n"
         "Định dạng đầu ra (1 dòng):\n`kv_mult=<số nguyên>x attn_flops_mult=<số nguyên>x`",
         "scale = 24 // 2\n"
         "print(f\"kv_mult={scale}x attn_flops_mult={scale ** 2}x\")"),
        ("L14", "Tính PF-ngày theo quy mô mở rộng (6ND) và tỉ lệ từ tố trên tham số",
         "# Lab LLM L14 — Hành trình mở rộng: từ kiến trúc chú ý tới huấn luyện tối ưu\n\n"
         "Tính hai đại lượng trên một mô hình tham chiếu giả định: (1) đổi tổng phép tính `C = 6 * 90e9 * 4.5e11` sang đơn vị `PF-ngày` (biết `1 PF-ngày = 10^15 * 86 400` phép tính); (2) tính tỉ lệ số từ tố trên mỗi tham số ở cấu hình tối ưu gồm `2.0e12` từ tố và `100e9` tham số.\n\n"
         "Định dạng đầu ra (1 dòng):\n`model_pf_days=<số nguyên> tokens_per_param=<số nguyên>`",
         "flops = 6 * 90e9 * 4.5e11\n"
         "pf_days = flops / (1e15 * 86400)\n"
         "ratio = 2.0e12 / 100e9\n"
         "print(f\"model_pf_days={pf_days:.0f} tokens_per_param={ratio:.0f}\")"),
    ],
    "AGT": [
        ("L00", "Tính độ tin cậy tích lũy của tác tử sau 15 bước độc lập",
         "# Lab AGT L00 — Vòng lặp tác tử: độ tin cậy qua nhiều bước\n\n"
         "So sánh tỉ lệ hoàn thành cả nhiệm vụ `15` bước độc lập khi độ tin cậy mỗi bước đạt `96%` so với `99%`.\n\n"
         "Định dạng đầu ra (1 dòng):\n`task15_at96=<1 chữ số>% task15_at99=<1 chữ số>%`",
         "p96 = 0.96 ** 15 * 100\n"
         "p99 = 0.99 ** 15 * 100\n"
         "print(f\"task15_at96={p96:.1f}% task15_at99={p99:.1f}%\")"),
        ("L01", "Kiểm chứng tham số gọi công cụ trước khi thực thi (loại cả kiểu bool)",
         "# Lab AGT L01 — Gọi công cụ và kiểm tra lược đồ tham số\n\n"
         "Kiểm tra danh sách 5 lời gọi chuyển khoản giả lập `calls = [(750_000, '9876543210'), (True, '9876543210'), (-100, '9876543210'), (250_000, '12345'), (15_000_000, '9876543210')]`. Quy tắc hợp lệ: số tiền `amt` phải là `int` thực sự (loại `bool`) trong khoảng `0 < amt <= 10_000_000` và tài khoản `acc` là chuỗi đúng `10` chữ số.\n\n"
         "Định dạng đầu ra (1 dòng):\n`total_calls=<số> valid_count=<số> idx=<danh sách chỉ số>`",
         "def valid(amt, acc):\n"
         "    ok_a = isinstance(amt, int) and not isinstance(amt, bool)\n"
         "    return ok_a and 0 < amt <= 10_000_000 and len(acc) == 10 and acc.isdigit()\n"
         "calls = [\n"
         "    (750_000, '9876543210'), (True, '9876543210'), (-100, '9876543210'),\n"
         "    (250_000, '12345'), (15_000_000, '9876543210'),\n"
         "]\n"
         "ok = [i for i, c in enumerate(calls) if valid(*c)]\n"
         "print(f\"total_calls={len(calls)} valid_count={len(ok)} idx={ok}\")"),
        ("L02", "Tính đường găng song song trực tiếp trên đồ thị phụ thuộc DAG",
         "# Lab AGT L02 — Lập kế hoạch và phân rã đồ thị phụ thuộc (DAG)\n\n"
         "Cho đồ thị phụ thuộc gồm 5 bước: `tim` (3 s, không phụ thuộc), `docA` (5 s, sau `tim`), `docB` (2 s, sau `tim`), `tonghop` (4 s, sau cả `docA` và `docB`), `kiemtra` (1 s, sau `tonghop`). Viết mã dựng cấu trúc đồ thị phụ thuộc và tính thời gian hoàn thành từng bước để tìm thời gian chạy tuần tự, đường găng song song và thời gian tiết kiệm.\n\n"
         "Định dạng đầu ra (1 dòng):\n`sequential=<số>s critical_path=<số>s saved=<số>s`",
         "dur = {'tim': 3, 'docA': 5, 'docB': 2, 'tonghop': 4, 'kiemtra': 1}\n"
         "deps = {\n"
         "    'tim': [], 'docA': ['tim'], 'docB': ['tim'],\n"
         "    'tonghop': ['docA', 'docB'], 'kiemtra': ['tonghop'],\n"
         "}\n"
         "finish = {}\n"
         "for node in ('tim', 'docA', 'docB', 'tonghop', 'kiemtra'):\n"
         "    prev = max((finish[p] for p in deps[node]), default=0)\n"
         "    finish[node] = dur[node] + prev\n"
         "seq = sum(dur.values())\n"
         "crit = finish['kiemtra']\n"
         "print(f\"sequential={seq}s critical_path={crit}s saved={seq - crit}s\")"),
        ("L03", "Tính số lượt hội thoại tối đa trước khi đầy bộ nhớ ngữ cảnh",
         "# Lab AGT L03 — Bộ nhớ ngắn hạn và ngân sách ngữ cảnh\n\n"
         "Với trần ngữ cảnh `64_000` từ tố, phần lời nhắc hệ thống (system prompt) cố định `4_000` từ tố, mỗi lượt hỏi–đáp thêm `1_500` từ tố. Tính số lượt tối đa và tổng từ tố khi đầy.\n\n"
         "Định dạng đầu ra (1 dòng):\n`max_turns=<số nguyên> full_after=<số nguyên>`",
         "max_turns = (64_000 - 4_000) // 1_500\n"
         "print(f\"max_turns={max_turns} full_after={4000 + max_turns * 1500}\")"),
        ("L04", "Tính độ phủ truy vấn lặp 3 vòng và tự kiểm tra khớp chuỗi trích dẫn",
         "# Lab AGT L04 — Tác tử tìm thông tin: truy vấn lặp và kiểm trích dẫn\n\n"
         "Biết vòng truy vấn đầu phủ `50%`, hai vòng viết lại tiếp theo mỗi vòng tìm thêm `40%` phần còn sót. Đồng thời kiểm tra tự động xem câu trích `'rut ngan 45% thoi gian xu ly'` có tồn tại nguyên văn trong văn bản nguồn `'He thong thanh toan rut ngan 45% thoi gian xu ly.'` hay không.\n\n"
         "Định dạng đầu ra (1 dòng):\n`recall_after_3=<1 chữ số>% matched_quote=<0 hoặc 1>`",
         "miss = 0.50 * (0.60 ** 2)\n"
         "cov = (1.0 - miss) * 100\n"
         "src = 'He thong thanh toan rut ngan 45% thoi gian xu ly.'\n"
         "quote = 'rut ngan 45% thoi gian xu ly'\n"
         "matched = int(quote in src)\n"
         "print(f\"recall_after_3={cov:.1f}% matched_quote={matched}\")"),
        ("L05", "Tính độ tin cậy hậu nghiệm Bayes qua bộ kiểm chứng",
         "# Lab AGT L05 — Tự kiểm tra: tỉ lệ thật sau bộ kiểm chứng\n\n"
         "Biết tỉ lệ nền bộ sinh đúng là `base = 0.55`, bộ kiểm chứng bắt đúng câu đúng với tỉ lệ `TPR = 0.85` và nhận nhầm câu sai với tỉ lệ `FPR = 0.15`. Tính phần trăm câu thật sự đúng trong nhóm được chấp nhận.\n\n"
         "Định dạng đầu ra (1 dòng):\n`accepted_true_pct=<1 chữ số>%`",
         "tp, fp = 0.55 * 0.85, 0.45 * 0.15\n"
         "post = tp / (tp + fp) * 100\n"
         "print(f\"accepted_true_pct={post:.1f}%\")"),
        ("L06", "Đếm số kênh giao tiếp ngang hàng vs qua tác tử điều phối",
         "# Lab AGT L06 — Nhiều tác tử và chi phí giao tiếp\n\n"
         "Với nhóm `8` tác tử, tính số kênh giao tiếp một chiều khi nối trực tiếp mọi cặp ngang hàng so với đi qua 1 tác tử điều phối tập trung.\n\n"
         "Định dạng đầu ra (1 dòng):\n`mesh_channels=<số nguyên> hub_channels=<số nguyên>`",
         "n = 8\n"
         "mesh = n * (n - 1)\n"
         "hub = 2 * (n - 1)\n"
         "print(f\"mesh_channels={mesh} hub_channels={hub}\")"),
        ("L07", "So sánh độ ổn định pass^4 với cơ hội ít nhất một lần pass@4",
         "# Lab AGT L07 — Đánh giá tác tử: ít nhất một lần vs ổn định mọi lần\n\n"
         "Khi mỗi lần chạy độc lập có xác suất thành công `p = 0.75`, tính `pass@4` (ít nhất 1 lần thành công trong 4 lần) và `pass^4` (cả 4 lần đều thành công) theo đơn vị phần trăm.\n\n"
         "Định dạng đầu ra (1 dòng):\n`pass_at_4=<1 chữ số>% pass_pow_4=<1 chữ số>%`",
         "p = 0.75\n"
         "pass_at_4 = (1.0 - (1.0 - p) ** 4) * 100\n"
         "pass_pow_4 = (p ** 4) * 100\n"
         "print(f\"pass_at_4={pass_at_4:.1f}% pass_pow_4={pass_pow_4:.1f}%\")"),
        ("L08", "Tính tổng từ tố (token) tích lũy qua 8 bước khi không dùng bộ nhớ đệm",
         "# Lab AGT L08 — Chi phí từ tố tăng gần bình phương nếu gửi lại lịch sử\n\n"
         "Vòng lặp `8` bước: bước 0 gửi `1 500` từ tố (token), mỗi bước sau lịch sử dài thêm `400` từ tố. Tính kích thước ngữ cảnh cuối, tổng từ tố gửi lại qua 8 bước và hệ số nhân so với bước cuối.\n\n"
         "Định dạng đầu ra (1 dòng):\n`final_ctx=<số> total_input=<số> mult=<2 chữ số>x`",
         "toks = [1500 + 400 * k for k in range(8)]\n"
         "print(\n"
         "    f\"final_ctx={toks[-1]} total_input={sum(toks)} \"\n"
         "    f\"mult={sum(toks) / toks[-1]:.2f}x\"\n"
         ")"),
        ("L09", "Mô phỏng chính sách quyền tối thiểu chống chèn lời nhắc gián tiếp",
         "# Lab AGT L09 — An toàn cho tác tử trước chèn lời nhắc gián tiếp\n\n"
         "Cho bảng chính sách quyền công cụ `policy = {'read_file': 'allow', 'email_ext': 'confirm', 'pay_wire': 'confirm', 'exec_shell': 'deny'}` và danh sách `actions = ['read_file', 'email_ext', 'pay_wire', 'exec_shell']` do trang web lạ kích hoạt. Lọc các hành động tự động chạy (`'allow'`) và kiểm tra trạng thái của `'exec_shell'`.\n\n"
         "Định dạng đầu ra (1 dòng):\n`auto_executed=<danh sách> blocked=<trạng thái>`",
         "policy = {\n"
         "    'read_file': 'allow', 'email_ext': 'confirm',\n"
         "    'pay_wire': 'confirm', 'exec_shell': 'deny',\n"
         "}\n"
         "actions = ['read_file', 'email_ext', 'pay_wire', 'exec_shell']\n"
         "auto_run = [a for a in actions if policy.get(a) == 'allow']\n"
         "print(f\"auto_executed={auto_run} blocked={policy['exec_shell']}\")"),
        ("L10", "Phân loại vết truy vết (trace) theo quy luật ưu tiên Pareto",
         "# Lab AGT L10 — Quan sát vết truy vết và gỡ lỗi theo Pareto\n\n"
         "Cho bảng đếm `60` lần chạy lỗi `errs = {'wrong_tool': 31, 'bad_args': 18, 'early_stop': 7, 'tool_fail': 4}`. Tính tỉ lệ phần trăm của nhóm lỗi lớn nhất `'wrong_tool'` và tổng số ca lỗi.\n\n"
         "Định dạng đầu ra (1 dòng):\n`top_cause_pct=<1 chữ số>% total=<số nguyên>`",
         "errs = {\n"
         "    'wrong_tool': 31, 'bad_args': 18, 'early_stop': 7, 'tool_fail': 4,\n"
         "}\n"
         "tot = sum(errs.values())\n"
         "print(f\"top_cause_pct={errs['wrong_tool'] / tot * 100:.1f}% total={tot}\")"),
        ("L11", "So sánh độ tin cậy quy trình cố định (Workflow) vs tác tử tự chủ",
         "# Lab AGT L11 — Chọn quy trình cố định hay tác tử tự chủ\n\n"
         "Một tác vụ đã biết rõ `5` bước: dùng quy trình cố định có độ tin cậy `97%/bước`, còn giao cho tác tử tự chọn đường chạy trung bình `8` bước với độ tin cậy `94%/bước`. Tính xác suất thành công trọn vẹn của cả hai phương án.\n\n"
         "Định dạng đầu ra (1 dòng):\n`fixed_workflow=<1 chữ số>% autonomous_agent=<1 chữ số>%`",
         "wf = (0.97 ** 5) * 100\n"
         "ag = (0.94 ** 8) * 100\n"
         "print(f\"fixed_workflow={wf:.1f}% autonomous_agent={ag:.1f}%\")"),
        ("L12", "Tính cải thiện định lượng trên bộ chuẩn kiểm thử (benchmark) SWE-bench",
         "# Lab AGT L12 — Hành trình tác tử dùng công cụ 2022–2025\n\n"
         "Tính: (1) số bài giải được ban đầu ở mức `1.96%` trên bộ `2 294` bài (làm tròn thành số nguyên), rồi hệ số tăng khi tiến tới `286` bài cùng bộ; (2) số bài giải được khi đạt `65%` trên bộ SWE-bench Verified (`500` bài).\n\n"
         "Định dạng đầu ra (1 dòng):\n`full_old=<số> full_gain=<1 chữ số>x verified_solved=<số>`",
         "solved_full_old = round(0.0196 * 2294)\n"
         "gain_x = 286 / solved_full_old\n"
         "solved_ver = round(0.65 * 500)\n"
         "print(\n"
         "    f\"full_old={solved_full_old} full_gain={gain_x:.1f}x \"\n"
         "    f\"verified_solved={solved_ver}\"\n"
         ")"),
    ],
    "RLN": [
        ("L00", "Tính tổng chiết khấu vô hạn 1/(1 - γ) và chuỗi phần thưởng hữu hạn",
         "# Lab RLN L00 — Lợi nhuận chiết khấu với hệ số γ = 0.8\n\n"
         "Với hệ số chiết khấu `gamma = 0.8`, tính giới hạn tổng vô hạn `1 / (1 - gamma)` khi mỗi bước đều nhận thưởng `1`, và tính tổng lợi nhuận chiết khấu của chuỗi `[0, 5, 10]` (chú ý bước `t` đếm từ `0`).\n\n"
         "Định dạng đầu ra (1 dòng):\n`G_inf=<1 chữ số> G_0_5_10=<1 chữ số>`",
         "g = 0.8\n"
         "g_inf = 1.0 / (1.0 - g)\n"
         "g_fin = 0 + g * 5.0 + (g ** 2) * 10.0\n"
         "print(f\"G_inf={g_inf:.1f} G_0_5_10={g_fin:.1f}\")"),
        ("L01", "Giải chính xác hệ phương trình tự nhất quán Bellman hai trạng thái",
         "# Lab RLN L01 — Hàm giá trị và phương trình Bellman kỳ vọng\n\n"
         "Cho hai trạng thái chuyển qua lại với `gamma = 0.8`: `V(A) = 2 + 0.8*V(B)` và `V(B) = 0.8*V(A)`. Giải hệ phương trình để tính chính xác `V(A)` và `V(B)`.\n\n"
         "Định dạng đầu ra (1 dòng):\n`V_A=<3 chữ số> V_B=<3 chữ số>`",
         "g = 0.8\n"
         "va = 2.0 / (1.0 - g * g)\n"
         "vb = g * va\n"
         "print(f\"V_A={va:.3f} V_B={vb:.3f}\")"),
        ("L02", "Tính số vòng lặp giá trị cần thiết theo định lý co",
         "# Lab RLN L02 — Tốc độ hội tụ của lặp giá trị\n\n"
         "Theo cận trên tính co `k >= ln(eps) / ln(gamma)`, tính số vòng tối thiểu làm tròn lên để sai số giảm `eps = 0.0001` lần khi hệ số chiết khấu `gamma = 0.85` so với `gamma = 0.95`.\n\n"
         "Định dạng đầu ra (1 dòng):\n`iters_g085=<số nguyên> iters_g095=<số nguyên>`",
         "import math\n"
         "k85 = math.ceil(math.log(0.0001) / math.log(0.85))\n"
         "k95 = math.ceil(math.log(0.0001) / math.log(0.95))\n"
         "print(f\"iters_g085={k85} iters_g095={k95}\")"),
        ("L03", "Tính xác suất chọn tay ε-tham lam và một bước cập nhật cộng dồn Q",
         "# Lab RLN L03 — Khám phá và khai thác: kẻ cướp nhiều tay\n\n"
         "Cho `k = 8` tay và mức khám phá `eps = 0.2`: tính xác suất chọn tay tốt nhất `(1 - eps) + eps / k` và mỗi tay còn lại `eps / k`, cùng giá trị `Q` mới theo công thức cập nhật trung bình cộng dồn `Q_1 = Q_0 + (r - Q_0) / n` sau lần thưởng `r = 2.0` từ `Q_0 = 0.0` tại lần thứ `n = 2`.\n\n"
         "Định dạng đầu ra (1 dòng):\n`p_best=<3 chữ số> p_other=<3 chữ số> q1=<1 chữ số>`",
         "k, eps = 8, 0.2\n"
         "p_best = (1.0 - eps) + eps / k\n"
         "p_other = eps / k\n"
         "q_new = 0.0 + (2.0 - 0.0) / 2\n"
         "print(f\"p_best={p_best:.3f} p_other={p_other:.3f} q1={q_new:.1f}\")"),
        ("L04", "So sánh ước lượng Monte Carlo với một bước sai phân thời gian TD(0)",
         "# Lab RLN L04 — Học từ kinh nghiệm: Monte Carlo và TD(0)\n\n"
         "Tính ước lượng trung bình các lượt chơi `[3.0, 6.0, 9.0]` (Monte Carlo) và kết quả một bước cập nhật sai phân thời gian `V_moi = V + alpha * (r + gamma * V_next - V)` từ `V = 5.0` với `r = 2.0`, `V_next = 8.0`, `gamma = 0.9`, `alpha = 0.25`.\n\n"
         "Định dạng đầu ra (1 dòng):\n`MC=<1 chữ số> TD0=<2 chữ số>`",
         "mc = sum([3.0, 6.0, 9.0]) / 3.0\n"
         "td = 5.0 + 0.25 * (2.0 + 0.9 * 8.0 - 5.0)\n"
         "print(f\"MC={mc:.1f} TD0={td:.2f}\")"),
        ("L05", "So sánh cập nhật ngoài chính sách (Q-learning) với theo chính sách (SARSA)",
         "# Lab RLN L05 — Q-learning (ngoài chính sách) và SARSA (theo chính sách)\n\n"
         "Từ `Q = 1.5`, thưởng `r = -1.0`, `gamma = 0.9`, tốc độ học `alpha = 0.2`: áp dụng quy tắc cập nhật `Q_moi = Q + alpha * (r + gamma * đích - Q)` cho ngoài chính sách (dùng `max Q(s') = 6.0`) và theo chính sách thật vừa chọn (`Q(s', a') = 2.0`).\n\n"
         "Định dạng đầu ra (1 dòng):\n`q_learning=<2 chữ số> sarsa=<2 chữ số>`",
         "ql = 1.5 + 0.2 * (-1.0 + 0.9 * 6.0 - 1.5)\n"
         "sarsa = 1.5 + 0.2 * (-1.0 + 0.9 * 2.0 - 1.5)\n"
         "print(f\"q_learning={ql:.2f} sarsa={sarsa:.2f}\")"),
        ("L06", "Tính mục tiêu hồi quy của mạng Q sâu (DQN) ở bước thường và kết thúc",
         "# Lab RLN L06 — Xấp xỉ hàm và mạng Q sâu (DQN)\n\n"
         "Cho `r = 2.0`, `gamma = 0.95`. Tính mục tiêu hồi quy của mạng Q sâu `r + gamma * max Q_target` ở bước trung gian (trong đó `max Q_target = 8.0` là giá trị cực đại ước lượng từ mạng mục tiêu giữ ổn định) và giá trị khi là bước kết thúc lượt (`y = r`).\n\n"
         "Định dạng đầu ra (1 dòng):\n`dqn_target=<1 chữ số> terminal_target=<1 chữ số>`",
         "y_step = 2.0 + 0.95 * 8.0\n"
         "y_term = 2.0 + 0.0\n"
         "print(f\"dqn_target={y_step:.1f} terminal_target={y_term:.1f}\")"),
        ("L07", "Tính kỳ vọng và phương sai tổng thể (chia N) trước/sau khi trừ đường cơ sở",
         "# Lab RLN L07 — Gradient chính sách REINFORCE và đường cơ sở giảm phương sai\n\n"
         "Với `N = 2` hành động đồng xác suất, mẫu gradient có dạng `g_i = grad_i * (G_i - b)`: hành động 1 có `(G_1 = 8, grad_1 = +0.5)` và hành động 2 có `(G_2 = 14, grad_2 = -0.5)`. Tính kỳ vọng và **phương sai tổng thể** (chia cho `N = len(vals) = 2`) khi chưa trừ đường cơ sở (`b = 0`) so với sau khi trừ đường cơ sở `b = 11`.\n\n"
         "Định dạng đầu ra (1 dòng):\n`mean=<2 chữ số> raw_var=<2 chữ số> bas_var=<2 chữ số>`",
         "vals_raw = [0.5 * 8.0, -0.5 * 14.0]\n"
         "vals_bas = [0.5 * (8.0 - 11.0), -0.5 * (14.0 - 11.0)]\n"
         "var = lambda xs: sum((x - sum(xs) / len(xs)) ** 2 for x in xs) / len(xs)\n"
         "print(\n"
         "    f\"mean={sum(vals_raw) / 2:.2f} raw_var={var(vals_raw):.2f} \"\n"
         "    f\"bas_var={var(vals_bas):.2f}\"\n"
         ")"),
        ("L08", "Tính lợi thế ước lượng A và quyết định hướng cập nhật Diễn viên–Nhà phê bình",
         "# Lab RLN L08 — Diễn viên–nhà phê bình (Actor–Critic) và hàm lợi thế\n\n"
         "Với `r = 2.0`, `gamma = 0.85`, `V(s') = 6.0`, `V(s) = 5.0`, tính lợi thế ước lượng `A = r + gamma * V(s') - V(s)` và xác định xem xác suất hành động này có tăng (`1` nếu `A > 0`) hay không.\n\n"
         "Định dạng đầu ra (1 dòng):\n`advantage=<1 chữ số> increase_prob=<0 hoặc 1>`",
         "adv = 2.0 + 0.85 * 6.0 - 5.0\n"
         "print(f\"advantage={adv:.1f} increase_prob={int(adv > 0)}\")"),
        ("L09", "Tính mục tiêu cắt tỉ số PPO cho cả phía dương và phía âm",
         "# Lab RLN L09 — Tối ưu chính sách gần kề (PPO): cắt tỉ số an toàn\n\n"
         "Áp dụng công thức `min(rho * A, clip(rho, 1 - eps, 1 + eps) * A)` với `eps = 0.2` cho hai trường hợp: lợi thế dương `(rho = 1.4, A = 3.0)` (bị cắt trần) và lợi thế âm `(rho = 0.6, A = -3.0)`.\n\n"
         "Định dạng đầu ra (1 dòng):\n`pos_clipped=<1 chữ số> neg_unclipped=<1 chữ số>`",
         "ppo = lambda rho, A, e=0.2: min(rho * A, max(1 - e, min(1 + e, rho)) * A)\n"
         "print(f\"pos_clipped={ppo(1.4, 3.0):.1f} neg_unclipped={ppo(0.6, -3.0):.1f}\")"),
        ("L10", "Tính mô hình sở thích Bradley–Terry và trừ phạt độ lệch phân phối",
         "# Lab RLN L10 — Học phần thưởng từ sở thích người dùng & phạt độ lệch KL\n\n"
         "Cho hiệu điểm `r_A - r_B = 1.5`: tính xác suất `P(A > B) = 1 / (1 + exp(-1.5))` và mất mát `-ln(P)`. Đồng thời với phần thưởng thô `3.0`, tính điểm sau khi trừ phạt độ lệch Kullback–Leibler (`KL = ln(pi / pi_ref)`) với hệ số `beta = 0.2`, chính sách mới `pi = 0.9` và chính sách gốc tham chiếu `pi_ref = 0.3`.\n\n"
         "Định dạng đầu ra (1 dòng):\n`prob=<3 chữ số> loss=<3 chữ số> kl_adj_r=<3 chữ số>`",
         "import math\n"
         "p = 1.0 / (1.0 + math.exp(-1.5))\n"
         "loss = -math.log(p)\n"
         "pen_r = 3.0 - 0.2 * math.log(0.9 / 0.3)\n"
         "print(f\"prob={p:.3f} loss={loss:.3f} kl_adj_r={pen_r:.3f}\")"),
        ("L11", "Tính điểm quay vòng khai thác lỗ hổng phần thưởng trong 1 200 bước",
         "# Lab RLN L11 — Khai thác phần thưởng\n\n"
         "Trong trò đua thuyền `1 200` bước, hành vi đúng về đích nhận tổng `+150`, còn hành vi quay vòng ăn mốc thưởng `+2` mỗi `6` bước sẽ kiếm được bao nhiêu? Kiểm tra xem phần thưởng khai thác có lớn hơn hành vi đúng (`1` nếu có).\n\n"
         "Định dạng đầu ra (1 dòng):\n`intended=<số> reward_hacked=<số> broken=<0 hoặc 1>`",
         "finish = 150\n"
         "loop_r = (1200 // 6) * 2\n"
         "print(\n"
         "    f\"intended={finish} reward_hacked={loop_r} \"\n"
         "    f\"broken={int(loop_r > finish)}\"\n"
         ")"),
        ("L12", "Tính trọng số 8 bước và số mẫu hiệu dụng (ESS)",
         "# Lab RLN L12 — Đánh giá ngoại tuyến: trọng số quan trọng và số mẫu hiệu dụng\n\n"
         "Cho một nhật ký 5 lượt có dãy trọng số `[2**8, 1, 1, 1, 1]`. Tính trọng số lớn nhất `w8` và số mẫu hiệu dụng `ESS = (sum(w))^2 / sum(w^2)`.\n\n"
         "Định dạng đầu ra (1 dòng):\n`w8=<số nguyên> ESS=<3 chữ số>`",
         "w = [2 ** 8, 1, 1, 1, 1]\n"
         "ess = (sum(w) ** 2) / sum(x * x for x in w)\n"
         "print(f\"w8={w[0]} ESS={ess:.3f}\")"),
        ("L13", "Quy đổi 120 triệu khung 60 Hz ra số ngày và điểm chuẩn hoá trò chơi Breakout",
         "# Lab RLN L13 — Hành trình trò chơi Atari 2013–2020\n\n"
         "Quy đổi `120_000_000` khung hình ở tốc độ `60` khung/giây (`Hz`) ra số ngày chơi liên tục; sau đó tính điểm chuẩn hoá theo mức người chơi `100 * (agent - rand) / (human - rand)` cho trò chơi phá gạch (Breakout) với điểm ngẫu nhiên `1.7`, người chơi `31.8` và tác tử `401.2`.\n\n"
         "Định dạng đầu ra (1 dòng):\n`days=<1 chữ số> breakout_norm=<1 chữ số>%`",
         "days = 120_000_000 / 60 / 86400\n"
         "norm_b = (401.2 - 1.7) / (31.8 - 1.7) * 100\n"
         "print(f\"days={days:.1f} breakout_norm={norm_b:.1f}%\")"),
    ],
    "CVI": [
        ("L00", "Tính dung lượng khung ảnh (MiB) và đổi giá trị mức sáng sRGB sang tuyến tính",
         "# Lab CVI L00 — Ảnh số, đơn vị MiB và độ sáng tuyến tính\n\n"
         "Cho một khung ảnh màu `1280 × 720`, 3 kênh, mỗi kênh 1 byte: tính tổng số byte và đổi sang `MiB` (biết `1 MiB = 1024^2 byte`). Sau đó chuẩn hoá giá trị `sRGB = 96` về `[0, 1]` (`u = s / 255`) và đổi sang độ sáng tuyến tính theo quy tắc sRGB chuẩn (`u / 12.92` nếu `u <= 0.04045`, ngược lại dùng phần hiệu chỉnh gamma `((u + 0.055)/1.055)^2.4`).\n\n"
         "Định dạng đầu ra (1 dòng):\n`bytes=<số nguyên> MiB=<2 chữ số> linear_96=<3 chữ số>`",
         "b_frame = 1280 * 720 * 3\n"
         "mib = b_frame / (1024 ** 2)\n"
         "u = 96 / 255\n"
         "lin96 = u / 12.92 if u <= 0.04045 else ((u + 0.055) / 1.055) ** 2.4\n"
         "print(f\"bytes={b_frame} MiB={mib:.2f} linear_96={lin96:.3f}\")"),
        ("L01", "Tính tích chập Sobel (lật 180 độ) trên cạnh dọc và vùng phẳng thật",
         "# Lab CVI L01 — Lọc ảnh bằng tích chập Sobel S_x\n\n"
         "Viết hàm tính **tích chập** 2D (có lật bộ lọc 180 độ `kx[2 - r][2 - c]`) với bộ lọc Sobel `S_x = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]` trên hai vùng `3 × 3`: (1) vùng cạnh có cột phải bằng `12`, hai cột trái bằng `0`; (2) vùng phẳng toàn số `5` (tính trực tiếp qua hàm, không gán cứng).\n\n"
         "Định dạng đầu ra (1 dòng):\n`sobel_edge_x=<số nguyên> flat_region=<số nguyên>`",
         "conv = lambda k, m: (\n"
         "    sum(k[2 - r][2 - c] * m[r][c] for r in range(3) for c in range(3))\n"
         ")\n"
         "kx = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]\n"
         "e_img = [[0, 0, 12], [0, 0, 12], [0, 0, 12]]\n"
         "f_img = [[5, 5, 5], [5, 5, 5], [5, 5, 5]]\n"
         "print(f\"sobel_edge_x={conv(kx, e_img)} flat_region={conv(kx, f_img)}\")"),
        ("L02", "Vét cạn chọn ngưỡng Otsu nhỏ nhất khi hoà phương sai cực đại",
         "# Lab CVI L02 — Biểu đồ tần suất và ngưỡng Otsu\n\n"
         "Quét mọi ngưỡng `t` nguyên trong đoạn `[9, 49]` trên dãy mức sáng `[8, 8, 10, 44, 46, 50]` để tìm ngưỡng tối đa hoá phương sai giữa hai lớp. Quy ước: nếu nhiều ngưỡng cùng đạt phương sai cực đại thì giữ ngưỡng nhỏ nhất đầu tiên.\n\n"
         "Định dạng đầu ra (1 dòng):\n`best_thr=<số nguyên> between_var=<1 chữ số>`",
         "px = [8, 8, 10, 44, 46, 50]\n"
         "cands = []\n"
         "for t in range(9, 50):\n"
         "    g0, g1 = [x for x in px if x <= t], [x for x in px if x > t]\n"
         "    if g0 and g1:\n"
         "        w = (len(g0) / len(px)) * (len(g1) / len(px))\n"
         "        v = w * (sum(g0) / len(g0) - sum(g1) / len(g1)) ** 2\n"
         "        cands.append((round(v, 9), t))\n"
         "best_v, best_t = min(cands, key=lambda item: (-item[0], item[1]))\n"
         "print(f\"best_thr={best_t} between_var={best_v:.1f}\")"),
        ("L03", "Chiếu một điểm 3D lên mặt phẳng ảnh qua ma trận nội K",
         "# Lab CVI L03 — Mô hình camera lỗ kim và hiệu chuẩn\n\n"
         "Với tiêu cự `f = 600` điểm ảnh, tâm ảnh `(cx=400, cy=300)` và điểm 3D `(X=0.6, Y=0.3, Z=3.0)` m, tính toạ độ điểm ảnh `(u, v)`.\n\n"
         "Định dạng đầu ra (1 dòng):\n`pixel_u=<số nguyên> pixel_v=<số nguyên>`",
         "f, cx, cy = 600.0, 400.0, 300.0\n"
         "X, Y, Z = 0.6, 0.3, 3.0\n"
         "u = f * (X / Z) + cx\n"
         "v = f * (Y / Z) + cy\n"
         "print(f\"pixel_u={u:.0f} pixel_v={v:.0f}\")"),
        ("L04", "Lọc khớp đặc trưng (như SIFT) bằng phép thử tỉ số < 0.8",
         "# Lab CVI L04 — Khớp đặc trưng và phép thử tỉ số\n\n"
         "Kiểm hai cặp khoảng cách mô tả đặc trưng SIFT gần nhất / gần nhì: cặp 1 `(0.24, 0.40)` và cặp 2 `(0.42, 0.50)` qua ngưỡng giữ `tỉ số < 0.8`.\n\n"
         "Định dạng đầu ra (1 dòng):\n`keep_good=<0 hoặc 1> keep_ambiguous=<0 hoặc 1>`",
         "r1, r2 = 0.24 / 0.40, 0.42 / 0.50\n"
         "print(f\"keep_good={int(r1 < 0.8)} keep_ambiguous={int(r2 < 0.8)}\")"),
        ("L05", "Tính số lần bốc mẫu đồng thuận ngẫu nhiên (RANSAC) khi đổi w",
         "# Lab CVI L05 — Ước lượng bền vững với đồng thuận mẫu ngẫu nhiên (RANSAC)\n\n"
         "Với số cặp mỗi mẫu `s = 4` và độ tin cậy `p = 0.99`, tính số lần thử `N = ceil(ln(1 - p) / ln(1 - w^s))` ở hai mức tỉ lệ khớp đúng `w = 0.6` và `w = 0.4`.\n\n"
         "Định dạng đầu ra (1 dòng):\n`n_w60=<số nguyên> n_w40=<số nguyên>`",
         "import math\n"
         "ransac_n = lambda w, s=4, p=0.99: (\n"
         "    math.ceil(math.log(1 - p) / math.log(1 - w ** s))\n"
         ")\n"
         "print(f\"n_w60={ransac_n(0.6)} n_w40={ransac_n(0.4)}\")"),
        ("L06", "Tính chênh lệch và sai số độ sâu khi đo hụt 1 điểm ảnh qua hai camera",
         "# Lab CVI L06 — Tính độ sâu và độ nhạy sai số từ cặp camera song song\n\n"
         "Cho tiêu cự `f = 600` điểm ảnh và khoảng cách hai camera `B = 0.15` m. Với vật ở `Z = 3.0` m và `Z = 9.0` m: tự tính độ chênh lệch lý thuyết `d` tương ứng với mỗi khoảng cách, rồi tính lại độ sâu khi phép đo chênh lệch bị hụt `1` điểm ảnh (`d - 1`) để tìm sai số dương tăng thêm `Z_err - Z`.\n\n"
         "Định dạng đầu ra (1 dòng):\n`Z3=3.0 err3=<2 chữ số>m Z9=9.0 err9=<2 chữ số>m`",
         "f, B = 600.0, 0.15\n"
         "d3, d9 = f * B / 3.0, f * B / 9.0\n"
         "err_at_3 = f * B / (d3 - 1.0) - 3.0\n"
         "err_at_9 = f * B / (d9 - 1.0) - 9.0\n"
         "print(f\"Z3=3.0 err3={err_at_3:.2f}m Z9=9.0 err9={err_at_9:.2f}m\")"),
        ("L07", "Đếm tham số lớp cuối và kiểm tra phép tăng cường giữ/hỏng nhãn",
         "# Lab CVI L07 — Học chuyển giao và bảo toàn nhãn khi tăng cường\n\n"
         "Tính: (1) tổng tham số của lớp tuyến tính cuối `256 -> 12` (có hệ số chặn +12); (2) trên 4 phép tăng cường dữ liệu cho bộ phân loại chữ số bảy đoạn `['shift_2px', 'bright_10', 'h_flip_2', 'rot180_6']`, tự phân tích xem phép nào giữ đúng hay làm hỏng nhãn thật rồi đếm tổng số phép biến đổi làm hỏng nhãn.\n\n"
         "Định dạng đầu ra (1 dòng):\n`head_params=<số nguyên> broken_augs=<số nguyên>`",
         "params = 256 * 12 + 12\n"
         "augs = {\n"
         "    'shift_2px': True, 'bright_10': True,\n"
         "    'h_flip_2': False, 'rot180_6': False,\n"
         "}\n"
         "broken = sum(1 for ok in augs.values() if not ok)\n"
         "print(f\"head_params={params} broken_augs={broken}\")"),
        ("L08", "Tính giao trên hợp (IoU) của hai hộp 2D phục vụ NMS",
         "# Lab CVI L08 — Phát hiện vật thể: giao trên hợp (IoU) và loại bỏ không cực đại (NMS)\n\n"
         "Tính giá trị IoU giữa hộp `(0, 0, 12, 12)` với `(6, 6, 18, 18)` (hai vật lệch nhau) và với `(2, 0, 14, 12)` (cần lọc trùng lặp).\n\n"
         "Định dạng đầu ra (1 dòng):\n`iou_diff=<3 chữ số> iou_nms=<3 chữ số>`",
         "def iou(a, b):\n"
         "    iw = max(0, min(a[2], b[2]) - max(a[0], b[0]))\n"
         "    ih = max(0, min(a[3], b[3]) - max(a[1], b[1]))\n"
         "    inter = iw * ih\n"
         "    ua = (a[2] - a[0]) * (a[3] - a[1]) + (b[2] - b[0]) * (b[3] - b[1]) - inter\n"
         "    return inter / ua\n"
         "print(f\"iou_diff={iou((0, 0, 12, 12), (6, 6, 18, 18)):.3f}\",\n"
         "      f\"iou_nms={iou((0, 0, 12, 12), (2, 0, 14, 12)):.3f}\")"),
        ("L09", "Tính IoU, hệ số chồng lấp Dice và độ chính xác điểm ảnh đánh lừa ở vùng 2%",
         "# Lab CVI L09 — Phân đoạn ảnh: IoU, Dice và bẫy độ chính xác điểm ảnh\n\n"
         "Trên một mặt nạ có `TP = 45, FP = 15, FN = 10`, tính IoU, Dice và xác nhận `Dice >= IoU`. Sau đó trên ảnh `100 × 100` có vật chỉ chiếm `2%` (`200` điểm ảnh), giả sử mô hình đoán toàn nền (`0` vật), tính độ chính xác điểm ảnh tổng thể và IoU thật của lớp vật.\n\n"
         "Định dạng đầu ra (1 dòng):\n`iou=<3 chữ số> dice=<3 chữ số> dice_ge_iou=<0 hoặc 1> acc_all_bg=<2 chữ số> iou_all_bg=<1 chữ số>`",
         "tp, fp, fn = 45, 15, 10\n"
         "iou = tp / (tp + fp + fn)\n"
         "dice = 2 * tp / (2 * tp + fp + fn)\n"
         "total_px, obj_px = 100 * 100, 200\n"
         "acc_bg = (total_px - obj_px) / total_px\n"
         "iou_bg = 0 / obj_px\n"
         "print(f\"iou={iou:.3f} dice={dice:.3f} dice_ge_iou={int(dice >= iou)}\",\n"
         "      f\"acc_all_bg={acc_bg:.2f} iou_all_bg={iou_bg:.1f}\")"),
        ("L10", "Tính độ chính xác theo lát sáng/tối khi dịch chuyển miền triển khai",
         "# Lab CVI L10 — Dịch chuyển miền giữa tập thử và thực tế\n\n"
         "Biết mô hình đúng `92%` ban ngày và `60%` ban đêm. Tính độ chính xác gộp trên tập thử cũ (`80%` ngày / `20%` đêm) và khi triển khai thực tế (`40%` ngày / `60%` đêm).\n\n"
         "Định dạng đầu ra (1 dòng):\n`test_overall=<1 chữ số>% deploy_real=<1 chữ số>%`",
         "acc_old = 0.80 * 0.92 + 0.20 * 0.60\n"
         "acc_dep = 0.40 * 0.92 + 0.60 * 0.60\n"
         "print(f\"test_overall={acc_old * 100:.1f}% deploy_real={acc_dep * 100:.1f}%\")"),
        ("L11", "Mô phỏng trên tập 100 ảnh huấn luyện và 25 ảnh nền tuyết quy luật học lối tắt",
         "# Lab CVI L11 — Học lối tắt trên đặc trưng giả: kiểm thử đổi nền\n\n"
         "Tạo dữ liệu giả lập `train_set`: `100` ảnh bò gồm `90` con đứng trên nền cỏ (`has_grass=True`) và `10` con trên nền khác; tạo thêm `snow_set`: `25` ảnh bò trên nền tuyết (`has_grass=False`). Áp dụng bộ phân loại lối tắt `predict = has_grass` lên từng ảnh để tính tỉ lệ đoán trúng (%) trên cả hai tập.\n\n"
         "Định dạng đầu ra (1 dòng):\n`spur_train=<số nguyên>% counterexample_snow=<số nguyên>%`",
         "tr = [{'has_grass': True}] * 90 + [{'has_grass': False}] * 10\n"
         "sn = [{'has_grass': False}] * 25\n"
         "acc = lambda ds: sum(1 for x in ds if x['has_grass']) / len(ds) * 100\n"
         "print(f\"spur_train={acc(tr):.0f}% counterexample_snow={acc(sn):.0f}%\")"),
        ("L12", "Tính hệ số giảm lỗi từ 2011->2015 và 2011->2017 cùng số ảnh sai trên 50k ảnh",
         "# Lab CVI L12 — Hành trình ImageNet: tỉ lệ lỗi top-5 (năm đáp án đầu) qua các mốc\n\n"
         "Với các mốc tỉ lệ sai trong `5` đáp án đầu (top-5 error) khác: `25.8%` (2011), `3.57%` (2015) và `2.25%` (2017), tính hệ số giảm lỗi từ 2011 tới 2015 và tới 2017, đồng thời tính số ảnh đoán sai trên tập kiểm định `50 000` ảnh tại hai mốc sau.\n\n"
         "Định dạng đầu ra (1 dòng):\n`drop_11_15=<1 chữ số>x drop_11_17=<1 chữ số>x err2015=<số> err2017=<số>`",
         "drop_11_15 = 25.8 / 3.57\n"
         "drop_11_17 = 25.8 / 2.25\n"
         "err_15 = round(0.0357 * 50_000)\n"
         "err_17 = round(0.0225 * 50_000)\n"
         "print(f\"drop_11_15={drop_11_15:.1f}x drop_11_17={drop_11_17:.1f}x\",\n"
         "      f\"err2015={err_15} err2017={err_17}\")"),
    ],
}


def main():
    assert set(COVERS) == {(c, item[0]) for c, lst in DATA.items() for item in lst}
    only = {x.strip().upper() for x in sys.argv[1:] if x.strip()}
    for course, items in DATA.items():
        if only and course not in only:
            continue
        for lid, hint, de_md, sol in items:
            common.upgrade_lesson(
                course, lid, hint, de_md, sol,
                covers=COVERS[(course, lid)],
                force_code=True,
            )
        up.sync_course_ledger(course, default_lang="python")
        for lid, hint, de_md, sol in items:
            common.sync_practice_run_blocks(course, lid, sol)
            print(f"OK {course}:{lid}", flush=True)
    print(f"ALL S9 BATCH-2 ({','.join(only) or 'IRS/LLM/AGT/RLN/CVI'}) PASSED!", flush=True)


if __name__ == "__main__":
    main()
