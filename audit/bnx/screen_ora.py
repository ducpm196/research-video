"""Sinh sổ mã trên màn hình (audit/bnx/screen/lNN.yaml) cho bài BNX có khối Oracle: các khối `oracle` không phải chương trình `prog(...)`
nên lib2.py gen-screen không sinh được. Mỗi bài khai CFG[lid] = danh sách mục; script đọc văn bản khối từ lessons/bnx, CHẠY THẬT
(tiền đề + khối + post) trên bnx-ora qua dbrun.ora rồi ghi expect_stdout đúng như cổng screen_code sẽ so.

Dùng: python -B audit/bnx/screen_ora.py L07 [L38 …]   (cần container bnx-ora đang chạy; ghi audit/bnx/screen/lNN.yaml)
Mục CFG: (khoá "cảnh bước khối", kind, thông số)
    run    : prelude=[khoá khối đứng trước], post=chuỗi, claims=[…]  → kind run, lang oracle, expect_stdout lấy từ lần chạy thật
    output : of=khoá khối run, reason                                 → kind output
    other  : lang, reason, read_check                                 → kind other
Nguồn dùng chung (sources:) chép nguyên văn từ tệp sổ cũ nếu có (ví dụ lời giải lab)."""
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "audit" / "bnx"))
sys.path.insert(0, str(ROOT / "audit" / "review"))
sys.stdout.reconfigure(encoding="utf-8")
import dbrun  # noqa: E402
import screen_code as sc  # noqa: E402


def R(key, **kw):
    return (key, "run", kw)


def O(key, of, reason="Đầu ra thật của khối chạy trên Oracle (sqlplus căn cột bằng tab, giữ nguyên; … là đoạn lược)."):
    return (key, "output", dict(of=of, reason=reason))


def X(key, **kw):
    return (key, "other", kw)


CFG = {}
DROP_SOURCES = {"L07": ("L07_aq_clean",)}   # nguồn của lần soạn cũ (hàng đợi AQ đã chuyển sang L38)

# ── L07 ──
CFG["L07"] = [
    R("formula 0 0", claims=["chỉ khai 1 phân vùng đầu (trước 1/2/2025); INTERVAL 1 tháng"],
      post="SELECT COUNT(*) AS so_phan_vung FROM user_tab_partitions WHERE table_name = 'BNX_L07_GD';"),
    R("formula 1 0", claims=["CONNECT BY ROWNUM <= 3 trên dual cho 3 dòng: 1, 2, 3"]),
    O("formula 1 1", "formula 1 0"),
    R("formula 2 0", prelude=["formula 0 0"], claims=["3 650 dòng", "1 + 11 = 12 phân vùng (Oracle tự tạo 11)"]),
    O("formula 3 0", "formula 2 0"),
    R("formula 4 0", prelude=["formula 0 0", "formula 2 0"], claims=["kế hoạch truy vấn tháng 3: PARTITION RANGE SINGLE, Pstart = Pstop = 3"]),
    R("formula 5 0", claims=["hai dòng JSON hợp lệ: 500 000 qua app, 2 000 000 qua atm"], post="SELECT COUNT(*) AS so_dong FROM bnx_l07_js;"),
    R("formula 6 0", prelude=["formula 5 0"], expect_stderr_contains="ORA-02290: check constraint (BNX.BNX_L07_ISJ) violated",
      claims=["chuỗi thiếu dấu đóng ngoặc bị IS JSON từ chối (ORA-02290)", "chỉ dòng 2, kênh atm, có so_tien > 1 000 000"]),
    O("formula 6 1", "formula 6 0", "Đầu ra thật (lược dòng ERROR/Help của sqlplus)."),
    O("example 1 0", "formula 4 0", "Bảng kế hoạch thật của DBMS_XPLAN.DISPLAY(…, 'BASIC +PARTITION') cho truy vấn tháng 3 (bỏ dòng tiêu đề và Plan hash value)."),
    R("example 3 0", prelude=["formula 0 0", "formula 2 0"], claims=["truy vấn không lọc theo ngày: PARTITION RANGE ALL, Pstart 1, Pstop 1048575"]),
    O("example 3 1", "example 3 0", "Bảng kế hoạch thật."),
    R("check 0 0", prelude=["formula 0 0", "formula 2 0"], claims=["đếm theo điều kiện ngày = 310 = đếm thẳng trong phân vùng chứa 15/3"]),
    O("check 0 1", "check 0 0"),
    R("quymo 0 0", claims=["bảng phân vùng theo tháng nạp 1000 dòng mỗi ngày: cả năm 365000 dòng; riêng phân vùng chứa 15/3/2025 là 31000 dòng (31 ngày × 1000)"]),
    O("quymo 1 0", "quymo 0 0"),
    R("pitfalls 0 0", prelude=["formula 0 0", "formula 2 0"], claims=["TRUNC(ngay, 'MM') = … : PARTITION RANGE ALL, không cắt tỉa"]),
    O("pitfalls 0 1", "pitfalls 0 0", "Hai dòng của bảng kế hoạch thật (phần đầu lược bằng …)."),
    R("pitfalls 1 0", claims=["{kenh:'app'} (tên trường không nháy kép, nháy đơn quanh giá trị): IS JSON mặc định (lỏng) nhận, IS JSON (STRICT) từ chối"]),
    O("pitfalls 1 1", "pitfalls 1 0"),
    R("pitfalls 2 0", prelude=["formula 0 0", "formula 2 0"],
      claims=["bỏ phân vùng tháng 1 rồi ROLLBACK vẫn còn 3 340 dòng: lệnh bỏ phân vùng tự chốt, mất đúng 310 dòng"]),
    O("pitfalls 2 1", "pitfalls 2 0"),
    O("practice 1 0", "src:BNX:LAB_L07", "kết quả mong đợi của lab LAB_L07: đầu ra THẬT của lời giải (chạy như labs/cham.sh)"),
    X("practice 3 0", lang="bash", reason="Lệnh dựng Oracle Free tự làm (không chạy trong cổng: tạo container mới).",
      read_check="Đối chiếu từng cờ với lệnh đã dùng dựng container bnx-ora (audit/bnx/BRIEF.md mục 8): ảnh gvenzl/oracle-free:23-slim, cổng 1521, ORACLE_PASSWORD, APP_USER, APP_USER_PASSWORD, "
                 "kết nối bnx/bnx_pass@//localhost/FREEPDB1 (dịch vụ FREEPDB1 đã dùng ở dbrun.py). Cú pháp bash kiểm bằng bash -n khi viết."),
]


# ── L38 ──
CFG["L38"] = [
    R("formula 0 0", prelude=["src:BNX:L38_aq_clean"], claims=["tạo kiểu thông điệp, bảng hàng đợi, hàng đợi và bật gửi/nhận"],
      post="SELECT name, TRIM(enqueue_enabled) AS enq, TRIM(dequeue_enabled) AS deq FROM user_queues WHERE name = 'BNX_L38_Q';",
      note="Người dùng bnx được cấp AQ_ADMINISTRATOR_ROLE, AQ_USER_ROLE, EXECUTE ON DBMS_AQ/DBMS_AQADM bằng SYSTEM ngày 2026-11-11 (lệnh ghi ở audit/bnx/ver/l38.py)."),
    R("formula 1 0", prelude=["src:BNX:L38_aq_clean", "formula 0 0"], claims=["gửi 101 rồi hoàn tác, gửi 102 rồi chốt: bảng hàng đợi còn 1 thông điệp"]),
    O("formula 2 0", "formula 1 0"),
    R("formula 3 0", prelude=["src:BNX:L38_aq_clean", "formula 0 0", "formula 1 0"], claims=["nhận đúng 102, 200 000", "sau khi chốt, bảng hàng đợi còn 0"]),
    O("formula 4 0", "formula 3 0", "Đầu ra thật của DBMS_OUTPUT và của câu đếm."),
    R("formula 5 0", claims=["INMEMORY_SIZE = 0 trên Oracle AI Database 26ai Free của bài", "ALTER TABLE … INMEMORY chạy được, user_tables.inmemory = ENABLED"],
      unverified_claims=["bộ nhớ cột làm báo cáo nhanh hơn: không đo (INMEMORY_SIZE = 0; bật cần khởi động lại instance dùng chung, không làm)"]),
    O("formula 6 0", "formula 5 0", "Đầu ra thật (lược dòng gạch dài của cột VALUE)."),
]
SRC = {"L38": {"L38_aq_clean": dict(
    lang="oracle", code=None, reason="Dọn hàng đợi, bảng hàng đợi và kiểu thông điệp của lần chạy trước để khối formula 0 0 chạy lại được (không hiện trên màn hình; bài không nói gì về bước dọn). Chép từ hằng AQ_CLEAN của audit/bnx/src/l38.py.",
    no_claim_reason="chỉ dọn dẹp; bài không nói kết quả nào của bước này")}}


def clean(out):
    return "\n".join(l.rstrip() for l in out.replace("\r\n", "\n").split("\n")).strip("\n")


def build(lid):
    blocks = {k: t for k, t in sc.all_blocks("BNX").items() if k.split()[1] == lid}
    reg, src_keep = {}, {}
    old = ROOT / "audit" / "bnx" / "screen" / f"{lid.lower()}.yaml"
    keys_cfg = {f"BNX {lid} {k}" for k, _, _ in CFG[lid]}
    if old.exists():
        d0 = yaml.safe_load(old.read_text(encoding="utf-8")) or {}
        src_keep = {k: v for k, v in (d0.get("sources") or {}).items() if k not in DROP_SOURCES.get(lid, ())}
        # chế độ gộp: giữ mục cũ (do lib2.py gen-screen sinh) còn khối thật và không nằm trong CFG
        reg = {k: v for k, v in (d0.get("blocks") or {}).items() if k in blocks and k not in keys_cfg and sc.digest(blocks[k]) == v.get("sha")}
    src_texts = {}
    for name, ent in SRC.get(lid, {}).items():
        ent = dict(ent)
        if ent.get("code") is None:
            import importlib
            sys.path.insert(0, str(ROOT / "audit" / "bnx" / "src"))
            ent["code"] = importlib.import_module(lid.lower()).AQ_CLEAN
        src_texts[name] = ent["code"].strip("\n")
        src_keep[name] = ent
    used = set(reg)
    for key, kind, kw in CFG[lid]:
        full = f"BNX {lid} {key}"
        if full not in blocks:
            raise SystemExit(f"không có khối {full}")
        used.add(full)
        e = {"sha": sc.digest(blocks[full]), "kind": kind}
        if kind == "run":
            e["lang"] = "oracle"
            pre = [k if k.startswith("src:") else f"BNX {lid} {k}" for k in kw.get("prelude", [])]
            if pre:
                e["prelude_keys"] = pre
            if kw.get("claims"):
                e["claims"] = kw["claims"]
            if kw.get("post"):
                e["post"] = kw["post"]
            for kx in ("unverified_claims", "note"):
                if kw.get(kx):
                    e[kx] = kw[kx]
            if kw.get("expect_stderr_contains"):
                e["expect_stderr_contains"] = kw["expect_stderr_contains"]
            def _t(p):
                if p.startswith("src:"):
                    return src_texts[p.split(":", 2)[2]]
                return blocks[p]
            src = "\n".join(x for x in ([_t(p) for p in pre] + [blocks[full], kw.get("post", "")]) if x)
            e["expect_stdout"] = clean(dbrun.ora(src)) + "\n"
        elif kind == "output":
            of = kw["of"]
            e["of"] = of if of.startswith("src:") else f"BNX {lid} {of}"
            e["reason"] = kw["reason"]
        else:
            e["lang"], e["reason"], e["read_check"] = kw["lang"], kw["reason"], kw["read_check"]
        reg[full] = e
    extra = [k for k in blocks if k not in used]
    if extra:
        print("CHƯA KHAI:", *extra, sep="\n  ")
    outp = ROOT / "audit" / "bnx" / "screen" / f"{lid.lower()}.yaml"
    hdr = (f"# Sổ mã trên màn hình bài BNX {lid} (sinh bằng audit/bnx/screen_ora.py {lid}: khối Oracle chạy thật trên bnx-ora, expect_stdout là đầu ra thật).\n"
           "# Người điều phối gộp vào audit/review/screen_code/BNX.yaml (audit/bnx/screen_try.py --merge).\n")
    outp.write_text(hdr + yaml.safe_dump({"blocks": reg, **({"sources": src_keep} if src_keep else {})}, allow_unicode=True, sort_keys=False, width=200),
                    encoding="utf-8", newline="\n")
    print(f"{lid}: {len(reg)} mục, chưa khai {len(extra)}")
    return not extra


if __name__ == "__main__":
    ok = True
    for lid in [a.upper() for a in sys.argv[1:]]:
        ok = build(lid) and ok
    sys.exit(0 if ok else 1)
