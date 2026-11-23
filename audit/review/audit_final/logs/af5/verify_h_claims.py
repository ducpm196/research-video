"""AF5 — người điều phối tự kiểm lại (chỉ đọc) các phát hiện chính của Mẫu H và đo độ lan toàn kho.
Chạy: .venv/Scripts/python -B audit/review/audit_final/logs/af5/verify_h_claims.py"""
import collections, pathlib, re, sys
import yaml
ROOT = pathlib.Path(__file__).resolve().parents[5]
sys.stdout.reconfigure(encoding="utf-8")
L = {}
for p in sorted((ROOT / "lessons").glob("*/L*.yaml")):
    L[(p.parent.name.upper(), p.name[:3])] = (p, p.read_text(encoding="utf-8"))
def has(c, l, s): return s in L[(c, l)][1]
print("== A. kiểm điểm từng phát hiện (True = đúng như người đọc báo)")
T = [
 ("MLP L04 '20 000 lần khớp' cho 1 000 tổ hợp × 5 nếp", has("MLP","L04","20 000 lần khớp")),
 ("BNK L08 lời 'lỗi ở bước đầu thì nhật ký chỉ một dòng'", has("BNK","L08","lỗi ở bước đầu thì nhật ký chỉ một dòng")),
 ("CPR L06 tiêu đề 'Ba lỗi thường gặp' + lời 'bốn lỗi'", has("CPR","L06","Ba lỗi thường gặp") and has("CPR","L06","bốn lỗi")),
 ("MLP L12 lời 'mười mũ trừ mười lăm' + màn hình max_diff=0.00e+00", has("MLP","L12","mười mũ trừ mười lăm") and has("MLP","L12","max_diff=0.00e+00")),
 ("CPR L04 lời 'nằm ngoài hàm chính'", has("CPR","L04","nằm ngoài hàm chính")),
 ("LNX L03 lời 'đường ống chuẩn để tách riêng luồng'", has("LNX","L03","đường ống chuẩn để tách riêng luồng")),
 ("PLC L03 recap 'độ sâu' khi đổi kết hợp trái/phải", has("PLC","L03","độ sâu của cây") or has("PLC","L03","độ sâu cây")),
 ("AIF L10 '10^{150}' trạng thái", "10^{150}" in L[("AIF","L10")][1]),
 ("PRJ L04 'chấm tự động 100 điểm'", has("PRJ","L04","100 điểm")),
 ("NET L11 de.md gọi nhân đôi là AIMD", "AIMD" in (ROOT/"labs/NET/L11/de.md").read_text(encoding="utf-8") and "gấp đôi" in (ROOT/"labs/NET/L11/de.md").read_text(encoding="utf-8")),
 ("CSA L00 lab là C, bài không có printf/#include", (ROOT/"labs/CSA/L00/loi_giai.c").exists() and not re.search(r"printf|#include", re.sub(r"(?s)- id: practice.*", "", L[("CSA","L00")][1]))),
 ("DBS L01 lab SQL, bài 1 đứng trước bài SQL (L02)", (ROOT/"labs/DBS/L01/loi_giai.sql").exists()),
 ("LNX L06: 'ssh-keygen' ≤ 1 lần, 'authorized_keys' 0 lần", L[("LNX","L06")][1].count("ssh-keygen") <= 2 and "authorized_keys" not in L[("LNX","L06")][1]),
 ("cham.sh chỉ so đầu ra (có diff, không có thang điểm)", "diff" in (ROOT/"labs/cham.sh").read_text(encoding="utf-8") and "điểm" not in (ROOT/"labs/cham.sh").read_text(encoding="utf-8")),
]
for name, ok in T: print(f"  {ok!s:5} {name}")
print("== B. độ lan toàn kho (số tệp bài chứa chuỗi)")
S = ["Hai mức quy mô", "làm tròn 2 chữ số; `!r`", "sắp xếp, cực trị, ghép đôi", "lượng giác, hàm ngược góc", "Bảng này giải thích từng ký hiệu dùng trong lời giải tham khảo",
     "tìm hiểu chủ đề tiếp nối ngay phần vừa học", "đ):", "Ta chạy thực nghiệm này vì cần đo trực tiếp hành vi trên dữ liệu thật", "1 + 1 == 2", "1e-12 < 1e-9",
     "Lời giải tham khảo", "chỉ xem sau khi tự thử"]
for s in S:
    hit = [k for k, (p, t) in L.items() if s in t]
    cc = collections.Counter(k[0] for k in hit)
    print(f"  {len(hit):4} tệp | {s[:60]} | {dict(cc.most_common(6))}")
print("== C. covers và lab")
cov_pr = cov_pr_gen = n_cov = 0; les_cov_pr_gen = 0
tri = collections.Counter(); labext = collections.defaultdict(collections.Counter)
for (c, l), (p, t) in L.items():
    d = yaml.safe_load(t)
    sc = {s.get("id"): s for s in d.get("scenes") or []}
    pr = next((s for s in d["scenes"] if s.get("kind") == "practice"), None)
    gen = bool(pr and any("mở đề" in (st.get("say") or "").lower() or "mở tệp đề" in (st.get("say") or "").lower() or "mở đề thực hành" in (st.get("say") or "").lower() for st in pr["steps"]))
    cv = d.get("covers") or []
    n_cov += len(cv)
    k = sum(1 for x in cv if x.get("scene") == (pr or {}).get("id"))
    cov_pr += k
    if gen and k: cov_pr_gen += k; les_cov_pr_gen += 1
    seq = tuple(sc.get(x.get("scene"), {}).get("kind") for x in cv)
    tri[seq] += 1
    for f in (ROOT / "labs" / c / l).glob("loi_giai.*"): labext[c][f.suffix[1:]] += 1
print(f"  covers tổng {n_cov}; trỏ vào cảnh practice {cov_pr}; trong đó practice kiểu 'mở đề' (không dạy gì) {cov_pr_gen} ở {les_cov_pr_gen} bài")
print("  10 dãy kind của covers hay gặp nhất:", [(" > ".join(map(str, k)), v) for k, v in tri.most_common(10)])
print("  ngôn ngữ lời giải lab theo khoá:")
for c in sorted(labext): print("   ", c, dict(labext[c]))
