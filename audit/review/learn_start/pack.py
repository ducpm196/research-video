"""Trang học trọn lộ trình từ con số 0 tới senior (KHMT · CNTT · AI) — HOC_TAP.html, sinh tự động từ giáo án và video thật.

Dùng (từ gốc kho):
  .venv/Scripts/python -B audit/review/learn_start/pack.py list                    # các chặng và số bài
  .venv/Scripts/python -B audit/review/learn_start/pack.py check [--decode] [--tsv out.tsv] [--course JVA,BNK]
  .venv/Scripts/python -B audit/review/learn_start/pack.py preview                 # sinh lại preview.html cho bài nào lệch
  .venv/Scripts/python -B audit/review/learn_start/pack.py page                    # sinh HOC_TAP.html + HOC_TAP.md + xem.html, rồi kiểm liên kết

Dãy học (đợt LF1, 2026-11-11): MỘT dãy duy nhất chia chặng theo cấp độ của interview/MASTER_CURRICULUM_INDEX.md và tầng của
curriculum/ROADMAP.md (bảng STAGES dưới đây). Mỗi chặng = bao đóng tiên quyết (requires + requires_ext) của các mục tiêu chặng, bỏ các
bài đã xếp ở chặng trước, sắp tô pô (phá hoà theo `prefer` của curriculum/tracks.yaml rồi số bài). Máy kiểm:
  - mỗi bài đúng một chỗ trong dãy; mọi bài của kho đều có chỗ;
  - MỌI cạnh tiên quyết trỏ về một bài đứng trước trong dãy toàn cục;
  - chặng 1–4 là "đường nhanh phỏng vấn" = đường học tối thiểu của MASTER_INDEX (JVA → BNK → [BNX] → INT → ACB).
Bài có trong giáo án mà chưa có video: hiện "đang soạn", không có liên kết, không vào `check`.

check, cho mỗi bài đã có video:
  - mục giáo án có `spec` trỏ tới tệp có thật; tiêu đề đặc tả = tiêu đề giáo án;
  - out/<KHOÁ>/<id>/: mp4, srt, chapters.txt, build_report.json, preview.html;
  - ffprobe: h264 1920x1080 + aac; |độ dài − timeline| ≤ 0,5 s;
  - (--decode) ffmpeg giải mã trọn, không in lỗi;
  - srt: số thứ tự liên tiếp, đầu < cuối, tăng dần, cuối ≤ độ dài + 0,5 s, chữ không rỗng;
  - chapters: bắt đầu 00:00, tăng dần, < độ dài;
  - build_report.spec_sha256 = lv.spec_digest(đặc tả hiện tại);
  - preview.html trùng từng byte với bản lv.player_html sinh ra từ đặc tả hiện tại (không cũ).
"""
import argparse
import html
import io
import json
import re
import subprocess
import sys
from collections import defaultdict
from contextlib import redirect_stdout
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
import lv  # noqa: E402

FFPROBE = "ffprobe"
FFMPEG = "ffmpeg"


def load_cur():
    cur = {}
    for f in sorted((ROOT / "curriculum").glob("*.yaml")):
        c = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
        if isinstance(c, dict) and c.get("course"):
            cur[str(c["course"])] = c
    return cur


# ───────────────────────── các chặng ─────────────────────────
# (khoá, tên, cấp độ trong MASTER_INDEX / ROADMAP, mục tiêu, lời giới thiệu). Khoá chưa có giáo án (vd BNX trước khi lập) tự bỏ qua.
STAGES = [
    ("S01", "Chặng 1 · Lập trình Java từ con số 0", "MASTER cấp 0A (bắt buộc với người chưa từng lập trình)", ["JVA"],
     "Gõ, biên dịch, chạy chương trình đầu tiên; biến, rẽ nhánh, vòng lặp, mảng, hàm, lớp, chuỗi, danh sách, ngoại lệ, giao diện; kết thúc bằng sổ chuyển khoản nhỏ."),
    ("S02", "Chặng 2 · Nền tảng backend ngân hàng", "MASTER cấp 1A (bắt buộc, học trước INT/ACB)", ["BNK"],
     "Bộ nhớ và luồng của Java, Spring Boot, REST và khoá lũy đẳng, SQL và PL/SQL, Redis, Kafka, SAGA, sổ cái bút toán kép, T24, ISO 8583, đối soát, PIN/HSM."),
    ("S03", "Chặng 3 · Kỹ năng backend theo JD ngân hàng", "Mở rộng cấp 1A — lấp khoảng trống JD (MASTER Mục 8)", ["BNX"],
     "Những chủ đề JD nêu mà kho chưa có bài: Git, OpenAPI, gRPC, JWT và OAuth, mTLS, thủ tục lưu trữ Oracle và SQL Server, Oracle cho khối lượng lớn, Elasticsearch, Couchbase, Kafka nâng cao và RabbitMQ, thanh toán quốc tế và ngoại tệ, ví điện tử và thuế điện tử, triển khai, DDD và Open API."),
    ("S04", "Chặng 4 · Ôn phỏng vấn và tích hợp ngân hàng", "MASTER cấp 3–4 (INT, ACB)", ["INT", "ACB"],
     "Ôn tập theo bộ 100 câu hỏi, đàm phán lương, rồi các tình huống tích hợp T24, NAPAS, ksqlDB, chi lương, sinh trắc học, đối soát ba bên, tín dụng."),
    ("S05", "Chặng 5 · Toán rời rạc, thuật toán, toán cho học máy", "MASTER cấp 0 · ROADMAP T0–T1", ["DMS", "CS112", "CS115:L00-L21", "CS115:L44"],
     "Lôgic, chứng minh, đếm, đồ thị; độ phức tạp, cấu trúc dữ liệu, chia để trị, quy hoạch động, đường đi ngắn nhất; vector, ma trận, đạo hàm, xác suất, thống kê. Có thể học song song với chặng 1–4."),
    ("S06", "Chặng 6 · Máy tính, hệ điều hành, mạng", "MASTER cấp 0 · ROADMAP T1", ["CSA", "OSY", "NET"],
     "Máy tính biểu diễn số và chạy lệnh thế nào, hệ điều hành chia CPU và bộ nhớ ra sao, gói tin đi qua mạng, TCP, DNS, HTTP, TLS."),
    ("S07", "Chặng 7 · Kỹ nghệ phần mềm, cơ sở dữ liệu, DevOps, bảo mật", "MASTER cấp 1B · ROADMAP T2–T3", ["SWF", "SDP", "DBS", "DVO", "WEB", "SEC"],
     "Phần mềm đúng đắn và kiểm thử, mẫu thiết kế, cơ sở dữ liệu từ mô hình quan hệ tới giao dịch và khôi phục, web, DevOps, an toàn thông tin."),
    ("S08", "Chặng 8 · Hệ phân tán, dữ liệu, đám mây, kiến trúc", "MASTER cấp 2 · ROADMAP T3, T5", ["DSY", "EVT", "DEN", "CLD", "CLC", "SAR"],
     "Đồng hồ lôgic, sao chép, đồng thuận, hướng sự kiện, kỹ thuật dữ liệu, container và Kubernetes, đám mây, kiến trúc hệ thống lớn — tầm của kỹ sư senior và kiến trúc sư."),
    ("S09", "Chặng 9 · Trí tuệ nhân tạo và học máy", "ROADMAP T4 (MASTER chưa có tầng AI — bổ sung đợt LF1)", ["CS115", "AIF", "DAN", "DSC", "MLO", "IRS", "LLM", "AGT", "RLN", "CVI"],
     "Phần còn lại của toán cho học máy, nền tảng AI, phân tích và khoa học dữ liệu, MLOps, truy xuất thông tin, mô hình ngôn ngữ lớn, AI agent, học tăng cường, thị giác máy tính."),
    ("S10", "Chặng 10 · Chuyên gia: lý thuyết, ngôn ngữ, song song, con người, nghề nghiệp, sự cố thật", "ROADMAP T1, T2, T7", ["TOC", "PLC", "PAR", "HCI", "SEP", "CAS"],
     "Lý thuyết tính toán, ngôn ngữ lập trình, tính toán song song, tương tác người–máy, đạo đức và pháp lý nghề nghiệp, và mười hai sự cố có thật đọc theo báo cáo điều tra gốc."),
    ("S11", "Chặng 11 · Chuyên ngành mở rộng (tuỳ chọn)", "ROADMAP T0, T5, T6", ["RBM", "ESY", "ROB", "GFX", "BCH"],
     "Toán cho robot, hệ nhúng thời gian thực, robot tự hành, đồ hoạ máy tính, blockchain — học khi nghề của bạn cần."),
]
FAST = {"S01", "S02", "S03", "S04"}

# Đối chiếu JD (resources/job/JD.md, tin Software Engineer acbjobs.com.vn + tin Backend/Lead) → bài. Mã nào không có trong giáo án: page() báo lỗi.
JD_MAP = [
    ("Java / Spring Boot", "bắt buộc ≥ 2 năm", ["JVA", "BNK:L00-L02"]),
    ("Thiết kế REST API, đặc tả bằng Swagger/OpenAPI", "bắt buộc", ["BNK:L03", "WEB:L06", "SDP:L14", "BNX:L01"]),
    ("gRPC", "kiến thức backend", ["BNX:L02"]),
    ("Giải thuật, tối ưu mã và hệ thống", "bắt buộc", ["CS112:L00-L07", "CS112:L12", "CS112:L18", "CS112:L23", "CS112:L24"]),
    ("Stored Procedure Oracle và MS SQL", "bắt buộc ≥ 3 năm", ["BNK:L05", "BNX:L06"]),
    ("Oracle: SQL, chỉ mục, kế hoạch thực thi, khoá, bế tắc", "lợi thế lớn", ["BNK:L04", "BNK:L05", "DBS:L08", "DBS:L10", "DBS:L13", "DBS:L15"]),
    ("Tính năng Oracle mới: Sharding, Queue, In-Memory, JSON", "mô tả công việc", ["BNX:L07"]),
    ("PostgreSQL, Couchbase, Elasticsearch", "kiến thức backend", ["DBS:L16", "DEN:L03", "DEN:L07", "BNX:L08", "BNX:L09"]),
    ("Queue: Kafka, RabbitMQ, ActiveMQ", "kiến thức backend", ["BNK:L07", "DSY:L14", "EVT:L00-L03", "DEN:L08", "BNX:L10"]),
    ("Cache Redis", "kiến thức backend", ["BNK:L06", "SAR:L04"]),
    ("Microservice/SOA, saga, outbox, lũy đẳng", "kiến thức backend", ["BNK:L08", "CLD:L00", "CLD:L03", "CLD:L04", "CLD:L14", "EVT:L06", "SAR:L09", "DEN:L10"]),
    ("TCP/IP, DNS, SSL/TLS, HTTP", "kiến thức backend", ["NET:L00", "NET:L05", "NET:L09", "NET:L12", "NET:L13", "NET:L14", "SEC:L09"]),
    ("Xác thực và phân quyền: JWT, OAuth 2.0/OIDC, mTLS", "bảo mật dữ liệu", ["SEC:L03-L05", "WEB:L09", "BNX:L03", "BNX:L04", "BNX:L05"]),
    ("Git, Docker, Kubernetes, GitLab CI/CD", "điểm cộng", ["BNX:L00", "CLD:L01", "CLD:L02", "CLD:L05", "CLD:L08", "DVO:L01", "DVO:L03", "DVO:L07", "BNX:L13"]),
    ("Nghiệp vụ: tài khoản, chuyển khoản trong và ngoài ngân hàng", "điểm cộng", ["BNK:L09-L12", "ACB:L00-L08"]),
    ("Nghiệp vụ: thanh toán quốc tế, ngoại tệ", "điểm cộng", ["BNX:L11"]),
    ("Nghiệp vụ: ví điện tử, thuế điện tử", "điểm cộng", ["BNX:L12"]),
    ("Hiệu năng, mở rộng, sẵn sàng cao, bảo mật (Back-end Lead)", "tin Lead", ["SAR:L00-L12", "CLD:L10-L12", "SEC:L11-L14"]),
    ("DDD, API Gateway, Open Banking (Back-end Lead)", "ưu tiên", ["SAR:L03", "BNX:L14"]),
    ("Thiết kế hệ thống thanh toán, xử lý lỗi phân tán", "chuẩn bị phỏng vấn", ["BNK:L14", "SAR:L12", "DSY:L13", "BNX:L15"]),
    ("Agile/Scrum, làm việc nhóm, đọc tài liệu tiếng Anh", "kỹ năng mềm", ["DVO:L00", "DVO:L09", "SEP:L00"]),
    ("Ứng dụng AI (lợi thế của bằng Cử nhân AI)", "lợi thế riêng của ứng viên", ["INT:L05", "AIF:L00", "LLM:L12", "MLO:L06", "MLO:L08"]),
]


def lesson_index(cur):
    les = {f"{C}:{l['id']}": (C, l) for C, c in cur.items() for l in c["lessons"]}
    pre = {u: {f"{C}:{q}" for q in l.get("requires") or []} | {str(q) for q in l.get("requires_ext") or []}
           for u, (C, l) in les.items()}
    return les, pre


def expand(cur, g):
    if ":" not in g:
        return [f"{g}:{l['id']}" for l in cur[g]["lessons"]] if g in cur else []
    C, rng = g.split(":")
    if C not in cur:
        return []
    m = re.fullmatch(r"L(\d+)(?:-L(\d+))?", rng)
    assert m, f"mục tiêu sai dạng: {g}"
    return [f"{C}:L{k:02d}" for k in range(int(m.group(1)), int(m.group(2) or m.group(1)) + 1)]


def stages(cur):
    """[(khoá chặng, tên, cấp, giới thiệu, [(C, l), …])] — bao đóng tiên quyết, sắp tô pô, mỗi bài một chỗ; kiểm mọi cạnh."""
    tr = yaml.safe_load((ROOT / "curriculum" / "tracks.yaml").read_text(encoding="utf-8"))
    prefer = list(tr["prefer"])
    les, pre = lesson_index(cur)
    for C in cur:
        if C not in prefer:
            prefer.append(C)
    key = lambda u: (prefer.index(u.split(":")[0]), int(u.split(":L")[1]))
    placed, out, pos = set(), [], {}
    for k, name, level, goals, intro in STAGES:
        gs = [u for g in goals for u in expand(cur, g)]
        if not gs:
            continue
        need, stack = set(), list(gs)
        while stack:
            u = stack.pop()
            if u in need or u in placed:
                continue
            assert u in les, f"tiên quyết {u} không có trong giáo án"
            need.add(u)
            stack += list(pre[u])
        ind = {u: len(pre[u] & need) for u in need}
        order, ready = [], sorted((u for u in need if ind[u] == 0), key=key)
        while ready:
            u = ready.pop(0)
            order.append(u)
            for v in need:
                if u in pre[v]:
                    ind[v] -= 1
                    if ind[v] == 0:
                        ready.append(v)
            ready.sort(key=key)
        assert len(order) == len(need), f"chu trình tiên quyết trong {k}"
        for u in order:
            pos[u] = len(pos)
        placed |= need
        out.append((k, name, level, intro, [les[u] for u in order]))
    missing = set(les) - placed
    assert not missing, f"bài không có chỗ trong dãy: {sorted(missing)[:10]}"
    bad = [(u, a) for u in les for a in pre[u] if pos[a] >= pos[u]]
    assert not bad, f"thứ tự vi phạm tiên quyết: {bad[:5]}"
    return out


def all_items(cur):
    return {k: items for k, _, _, _, items in stages(cur)}


def odir(C, l):
    return ROOT / "out" / C / l["id"]


def ffprobe(mp4):
    r = subprocess.run([FFPROBE, "-v", "error", "-show_entries", "stream=codec_type,codec_name,width,height:format=duration",
                        "-of", "json", str(mp4)], capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode:
        return None, r.stderr.strip()[:200]
    return json.loads(r.stdout), ""


def decode_errors(mp4):
    r = subprocess.run([FFMPEG, "-v", "error", "-xerror", "-i", str(mp4), "-f", "null", "-"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    return (r.returncode, r.stderr.strip()[:300])


TS = re.compile(r"(\d\d):(\d\d):(\d\d),(\d\d\d) --> (\d\d):(\d\d):(\d\d),(\d\d\d)$")


def srt_problems(p, dur):
    probs, blocks = [], [b for b in re.split(r"\n\s*\n", p.read_text(encoding="utf-8-sig").strip()) if b.strip()]
    prev = -1.0
    for i, b in enumerate(blocks, 1):
        ls = b.splitlines()
        if len(ls) < 3 or ls[0].strip() != str(i):
            probs.append(f"srt khối {i} sai dạng")
            break
        m = TS.match(ls[1].strip())
        if not m:
            probs.append(f"srt khối {i} mốc sai dạng")
            break
        g = [int(x) for x in m.groups()]
        a = g[0] * 3600 + g[1] * 60 + g[2] + g[3] / 1000
        e = g[4] * 3600 + g[5] * 60 + g[6] + g[7] / 1000
        if not (a < e and a >= prev):
            probs.append(f"srt khối {i} mốc không tăng")
        if not " ".join(ls[2:]).strip():
            probs.append(f"srt khối {i} rỗng")
        prev = a
        last = e
    if blocks and dur is not None and last > dur + 0.5:
        probs.append(f"srt kết thúc {last:.1f}s > video {dur:.1f}s")
    return len(blocks), probs


def chapter_problems(p, dur):
    probs, prev, n = [], -1, 0
    for ln in p.read_text(encoding="utf-8").splitlines():
        if not ln.strip():
            continue
        m = re.match(r"(\d+):(\d\d)(?::(\d\d))? (.+)$", ln)
        if not m:
            probs.append(f"chapters dòng sai dạng: {ln[:40]}")
            continue
        t = int(m.group(1)) * 60 + int(m.group(2)) if m.group(3) is None else int(m.group(1)) * 3600 + int(m.group(2)) * 60 + int(m.group(3))
        if n == 0 and t != 0:
            probs.append("chapters không bắt đầu 00:00")
        if t <= prev:
            probs.append(f"chapters không tăng ở {ln[:20]}")
        if dur is not None and t >= dur:
            probs.append(f"chapters {ln[:8]} vượt độ dài")
        prev, n = t, n + 1
    return n, probs


def norm_title(s):   # cùng quy ước với audit/review/check_meta.py: bỏ tiền tố "Bài N — " / "Chuyên đề N — "
    return re.sub(r"\s+", " ", re.sub(r"^(Bài|Chuyên đề) \d+( \([^)]*\))? — ", "", str(s))).strip()


def spec_of(l):
    return lv.load_spec(ROOT / l["spec"])


def preview_expected(spec):
    with redirect_stdout(io.StringIO()):
        frames = lv.build_frames(spec)
        total = lv.timeline(spec, frames)
    return lv.player_html(spec, frames, total, capture=False)


def check_one(C, l, decode):
    probs, info = [], {"C": C, "id": l["id"], "title": l["title"]}
    sp = ROOT / str(l.get("spec") or "")
    if not l.get("spec") or not sp.exists():
        return info | {"probs": ["giáo án không trỏ tới đặc tả có thật"]}
    spec = spec_of(l)
    if norm_title(spec.get("title")) != norm_title(l["title"]):
        probs.append(f"tiêu đề đặc tả ≠ giáo án: {spec.get('title')!r}")
    d = odir(C, l)
    mp4, srt, ch, rep, pv = d / f"{l['id']}.mp4", d / f"{l['id']}.srt", d / "chapters.txt", d / "build_report.json", d / "preview.html"
    for p in (mp4, srt, ch, rep):
        if not p.exists():
            probs.append(f"thiếu {p.name}")
    dur = None
    if mp4.exists():
        j, err = ffprobe(mp4)
        if j is None:
            probs.append(f"ffprobe lỗi: {err}")
        else:
            dur = float(j["format"]["duration"])
            st = j["streams"]
            v = [s for s in st if s.get("codec_type") == "video"]
            a = [s for s in st if s.get("codec_type") == "audio"]
            if not (v and v[0].get("codec_name") == "h264" and v[0].get("width") == 1920 and v[0].get("height") == 1080):
                probs.append("luồng hình không phải h264 1920x1080")
            if not (a and a[0].get("codec_name") == "aac"):
                probs.append("không có tiếng aac")
        if decode:
            rc, err = decode_errors(mp4)
            if rc or err:
                probs.append(f"giải mã lỗi rc={rc}: {err[:120]}")
            info["decoded"] = not (rc or err)
    info["dur"] = dur
    if rep.exists():
        b = json.loads(rep.read_text(encoding="utf-8"))
        if b.get("spec_sha256") != lv.spec_digest(spec):
            probs.append("STALE: đặc tả đổi sau lần dựng")
        tl = b.get("timeline_seconds")
        if dur is not None and tl is not None and abs(dur - tl) > 0.5:
            probs.append(f"độ dài {dur:.2f}s lệch timeline {tl:.2f}s")
    if srt.exists():
        info["cues"], ps = srt_problems(srt, dur)
        probs += ps
    if ch.exists():
        info["chapters"], ps = chapter_problems(ch, dur)
        probs += ps
    if not pv.exists():
        probs.append("thiếu preview.html")
    elif pv.read_text(encoding="utf-8") != preview_expected(spec):
        probs.append("preview.html cũ (khác bản sinh từ đặc tả hiện tại)")
    return info | {"probs": probs}


def has_video(C, l):
    return bool(l.get("spec")) and (ROOT / str(l["spec"])).exists() and (odir(C, l) / f"{l['id']}.mp4").exists()


def cmd_list(cur):
    tot = 0
    for k, name, level, intro, items in stages(cur):
        by = defaultdict(list)
        for C, l in items:
            by[C].append(l["id"])
        ready = sum(1 for C, l in items if has_video(C, l))
        tot += len(items)
        print(f"{k} {name}: {len(items)} bài (có video {ready}) · " + " · ".join(f"{C} {len(v)}" for C, v in by.items()))
    print(f"# tổng {tot} bài")


def cmd_check(cur, decode, tsv, only=None):
    rows, bad, pend = [], 0, 0
    for k, items in all_items(cur).items():
        for C, l in items:
            if only and C not in only:
                continue
            if not has_video(C, l):
                pend += 1
                continue
            r = check_one(C, l, decode)
            rows.append(r)
            if r["probs"]:
                bad += 1
                print(f"✗ {C} {l['id']}: " + " | ".join(r["probs"]))
    tot = sum(r.get("dur") or 0 for r in rows)
    print(f"# {len(rows)} bài có video · có vấn đề {bad} · chưa có video {pend} · tổng {tot / 60:.1f} phút"
          + (f" · giải mã trọn {sum(1 for r in rows if r.get('decoded'))}" if decode else ""))
    if tsv:
        Path(tsv).write_text("course\tlesson\tdur\tcues\tchapters\tdecoded\tproblems\n" + "".join(
            f"{r['C']}\t{r['id']}\t{r.get('dur')}\t{r.get('cues')}\t{r.get('chapters')}\t{r.get('decoded')}\t{' | '.join(r['probs'])}\n"
            for r in rows), encoding="utf-8")
    return 1 if bad else 0


def cmd_preview(cur):
    n = 0
    for k, items in all_items(cur).items():
        for C, l in items:
            if not has_video(C, l):
                continue
            spec = spec_of(l)
            pv = odir(C, l) / "preview.html"
            want = preview_expected(spec)
            if not pv.exists() or pv.read_text(encoding="utf-8") != want:
                pv.write_text(want, encoding="utf-8")
                n += 1
                print(f"↻ {C} {l['id']}")
    print(f"# sinh lại {n} preview.html")
    return 0


# ───────────────────────── trang hướng dẫn học ─────────────────────────
def mmss(s):
    s = int(round(s))
    return f"{s // 60}:{s % 60:02d}"


def rel(p):
    return p.relative_to(ROOT).as_posix()


def clean(t):
    return " ".join(str(t or "").split())


def study_bits(spec, d=None):
    """Câu hỏi tự kiểm, đáp án, chuỗi logic, lỗi hay gặp — lấy nguyên lời đọc (`say`) của đặc tả, không chế thêm.
    Thêm khung hình (PNG đã dựng ở out/<KHOÁ>/<id>/frames/) của câu hỏi và từng bước đáp án, vì câu hỏi thường trỏ vào mã, bảng, công
    thức chỉ có trên màn hình. Khung thứ k = câu thứ k của lời đọc (lv.build_frames: mỗi câu một khung); chỉ gắn khi số PNG = số câu."""
    q, a, rec, pit, qf, af = [], [], [], [], [], []
    idx, span = 0, {}
    for si, scn in enumerate(spec.get("scenes") or []):
        for ki, stp in enumerate(scn.get("steps") or []):
            n = len(lv.sentences(stp["say"]))
            span[(si, ki)] = (idx, idx + n)
            idx += n
    pngs = sorted((d / "frames").glob("*.png")) if d is not None and (d / "frames").is_dir() else []
    frames_ok = len(pngs) == idx and idx > 0
    for si, scn in enumerate(spec.get("scenes") or []):
        steps = scn.get("steps") or []
        if scn.get("kind") == "quiz" and not q:
            pi = next((i for i, s in enumerate(steps) if s.get("pause")), 0)
            q = [clean(s.get("say")) for s in steps[:pi + 1]]
            a = [clean(s.get("say")) for s in steps[pi + 1:]]
            if frames_ok:
                qf = [rel(pngs[span[(si, pi)][1] - 1])]
                af = [rel(pngs[span[(si, k)][1] - 1]) for k in range(pi + 1, len(steps))]
        elif scn.get("kind") == "recap":
            rec += [clean(s.get("say")) for s in steps]
        elif scn.get("kind") == "pitfall":
            pit += [clean(s.get("say")) for s in steps]
    return q, a, rec, pit, qf, af


def anchor(uid):
    return "u-" + uid.replace(":", "-")


def build_page(cur):
    les, pre = lesson_index(cur)
    data, seq = [], []
    for k, name, level, intro, items in stages(cur):
        rows = []
        for C, l in items:
            uid = f"{C}:{l['id']}"
            d = odir(C, l)
            mp4 = d / f"{l['id']}.mp4"
            ready = has_video(C, l)
            dur, chaps, q, a, rec, pit, qf, af = 0.0, [], [], [], [], [], [], []
            if ready:
                j, _ = ffprobe(mp4)
                dur = float(j["format"]["duration"]) if j else 0.0
                chaps = [c for c in (d / "chapters.txt").read_text(encoding="utf-8").splitlines() if c.strip()] if (d / "chapters.txt").exists() else []
                q, a, rec, pit, qf, af = study_bits(spec_of(l), d)
            r = {"uid": uid, "C": C, "id": l["id"], "title": l["title"], "dur": dur, "ready": ready, "stage": k,
                 "obj": [str(o) for o in (l.get("objectives") or [])], "pre": sorted(pre[uid], key=lambda x: (x.split(":")[0], x)),
                 "mp4": rel(mp4), "srt": rel(d / f"{l['id']}.srt"), "pv": rel(d / "preview.html"), "xem": rel(d / "xem.html"),
                 "ch": chaps, "q": q, "a": a, "qf": qf, "af": af, "rec": rec, "pit": pit, "course": cur[C].get("title") or ""}
            rows.append(r)
            seq.append(r)
        data.append({"k": k, "name": name, "level": level, "intro": intro, "rows": rows})
    for i, r in enumerate(seq, 1):
        r["n"] = i
    # bảng JD: mọi mã phải có trong giáo án
    jd = []
    for topic, need, refs in JD_MAP:
        uids = []
        for g in refs:
            ex = expand(cur, g)
            if not ex and g.split(":")[0] not in cur:
                uids.append(("?", g))      # khoá chưa có giáo án: hiện "chưa có"
                continue
            for u in ex:
                assert u in les, f"JD_MAP trỏ tới bài không có: {u}"
                uids.append(("ok", u))
        jd.append((topic, need, uids))
    return data, seq, jd


CSS = """
:root { --bg:#fbfaf7; --fg:#1d1d1b; --mute:#5c5a55; --line:#e2dfd8; --acc:#1f5fa8; --row:#f2efe8; --ok:#1e7a3d; --warn:#9a5b00; --card:#ffffff; --badge:#e8eef8; }
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { --bg:#16171a; --fg:#e8e6e1; --mute:#a5a29b; --line:#33353a; --acc:#7fb0ec; --row:#202227; --ok:#6fcf8f; --warn:#e0a84f; --card:#1d1f23; --badge:#24324a; } }
:root[data-theme="dark"] { --bg:#16171a; --fg:#e8e6e1; --mute:#a5a29b; --line:#33353a; --acc:#7fb0ec; --row:#202227; --ok:#6fcf8f; --warn:#e0a84f; --card:#1d1f23; --badge:#24324a; }
* { box-sizing:border-box; }
body { background:var(--bg); color:var(--fg); font:16px/1.55 system-ui, "Segoe UI", sans-serif; margin:0; padding:0 16px 64px; }
main { max-width:1040px; margin:0 auto; }
h1 { font-size:1.7rem; margin:28px 0 4px; } h2 { margin:0; font-size:1.2rem; display:inline; } h3 { font-size:1.05rem; margin:24px 0 8px; }
a { color:var(--acc); } .mute, .sum { color:var(--mute); } .ok { color:var(--ok); } .warn { color:var(--warn); }
.card { background:var(--card); border:1px solid var(--line); border-radius:10px; padding:12px 16px; margin:12px 0; }
.how li { margin:4px 0; }
.dash { display:grid; grid-template-columns:repeat(auto-fit, minmax(170px, 1fr)); gap:10px; }
.dash div { border:1px solid var(--line); border-radius:8px; padding:8px 12px; } .dash b { display:block; font-size:1.35rem; font-variant-numeric:tabular-nums; }
button, .btn { background:var(--row); color:var(--fg); border:1px solid var(--line); border-radius:6px; padding:5px 12px; font:inherit; cursor:pointer; }
button.pri { background:var(--acc); color:var(--bg); border-color:var(--acc); }
input[type=number] { width:5em; font:inherit; } input[type=search] { width:100%; font:inherit; padding:6px 10px; border:1px solid var(--line); border-radius:6px; background:var(--card); color:var(--fg); }
table { width:100%; border-collapse:collapse; } th, td { text-align:left; vertical-align:top; padding:8px 6px; border-bottom:1px solid var(--line); }
table.map td, table.map th, table.jd td, table.jd th { font-size:.94rem; }
tr.course td { background:var(--row); font-weight:600; } tr.done .t { color:var(--mute); } tr.done .t b::after { content:" ✓"; color:var(--ok); }
tr.pend .t { color:var(--mute); } tr.hide { display:none; }
td.n { white-space:nowrap; width:4.8em; } td.d { white-space:nowrap; width:4.5em; font-variant-numeric:tabular-nums; }
td.l { width:12em; } td.l a { display:inline-block; margin:0 8px 4px 0; }
section.stage { border-top:2px solid var(--line); margin-top:28px; padding-top:8px; } section.stage > details > summary { cursor:pointer; padding:6px 0; }
.lvl { font-size:.85rem; color:var(--mute); }
.badge { display:inline-block; font-size:.75rem; background:var(--badge); border-radius:4px; padding:0 6px; margin-left:4px; vertical-align:1px; }
.pre { font-size:.86rem; color:var(--mute); } .pre a { margin-right:6px; }
details.more > summary { cursor:pointer; color:var(--mute); font-size:.92rem; } .h { margin:8px 0 2px; font-weight:600; font-size:.92rem; }
details.more ul, details.more ol { margin:4px 0; padding-left:20px; font-size:.92rem; } details.more p { margin:4px 0; font-size:.92rem; }
details.ans > summary { cursor:pointer; color:var(--acc); font-size:.92rem; }
img.fr { display:block; width:100%; max-width:640px; height:auto; border:1px solid var(--line); border-radius:6px; margin:6px 0; }
textarea { width:100%; min-height:5em; font:inherit; font-size:.92rem; background:var(--card); color:var(--fg); border:1px solid var(--line); border-radius:6px; padding:6px; }
#review { display:none; } #review.on { display:block; }
.rcard { border:1px solid var(--line); border-radius:10px; padding:12px 16px; margin:10px 0; background:var(--card); }
.rcard .btns { display:flex; flex-wrap:wrap; gap:8px; margin-top:8px; }
.bar { height:6px; background:var(--row); border-radius:3px; overflow:hidden; } .bar i { display:block; height:100%; background:var(--ok); width:0; }
@media (max-width:640px) { thead { display:none; } tr { display:block; } td { display:block; border:0; padding:4px 0; width:auto !important; }
  tbody tr { border-bottom:1px solid var(--line); padding:8px 0; } table.map tr, table.jd tr { border-bottom:1px solid var(--line); } }
"""


def row_html(r, les):
    esc = html.escape
    uid = r["uid"]
    fast = ' <span class="badge">đường nhanh</span>' if r["stage"] in FAST else ""
    pre = " ".join(f'<a href="#{anchor(p)}">{esc(p.replace(":", " "))}</a>' for p in r["pre"])
    pre = f'<div class="pre">Cần học trước: {pre}</div>' if pre else ""
    if not r["ready"]:
        return (f'<tr class="pend" id="{anchor(uid)}" data-uid="{esc(uid)}"><td class="n">{r["n"]}</td>'
                f'<td><div class="t"><b>{esc(r["C"])} {esc(r["id"])}</b> · {esc(r["title"])}{fast} <span class="badge">đang soạn</span></div>{pre}</td>'
                f'<td class="d">—</td><td class="l mute">chưa có video</td></tr>')
    obj = "".join(f"<li>{esc(o)}</li>" for o in r["obj"])
    ch = "".join(f"<li>{esc(c)}</li>" for c in r["ch"])
    qq = "".join(f"<p>{esc(x)}</p>" for x in r["q"]) + "".join(f'<img class="fr" loading="lazy" src="{esc(x)}" alt="khung câu hỏi trong video">' for x in r["qf"])
    qa = "".join(f"<p>{esc(x)}</p>" for x in r["a"]) + "".join(f'<img class="fr" loading="lazy" src="{esc(x)}" alt="khung đáp án trong video">' for x in r["af"])
    rec = "".join(f"<li>{esc(x)}</li>" for x in r["rec"])
    pit = "".join(f"<li>{esc(x)}</li>" for x in r["pit"])
    return (
        f'<tr id="{anchor(uid)}" data-uid="{esc(uid)}" data-dur="{int(round(r["dur"]))}" data-pre="{esc(" ".join(r["pre"]))}">'
        f'<td class="n"><label><input type="checkbox" data-uid="{esc(uid)}"> {r["n"]}</label></td>'
        f'<td><div class="t"><b>{esc(r["C"])} {esc(r["id"])}</b> · {esc(r["title"])}{fast} <span class="due"></span></div>{pre}'
        f'<details class="more"><summary>Mục tiêu · mục lục · tự kiểm · chuỗi logic · lỗi hay gặp · ghi chú</summary>'
        f'<p class="h">Học xong bạn làm được:</p><ul>{obj}</ul>'
        f'<p class="h">Mục lục video (phút:giây):</p><ul>{ch}</ul>'
        f'<p class="h">Tự kiểm (trả lời ra giấy trước, rồi mới mở đáp án):</p><div class="qq">{qq}</div>'
        f'<details class="ans"><summary>Hiện đáp án</summary><div class="qa">{qa}</div></details>'
        f'<p class="h">Chuỗi logic cần mang theo:</p><ul class="rec">{rec}</ul>'
        f'<p class="h">Lỗi hay gặp:</p><ul>{pit}</ul>'
        f'<p class="h">Giải thích lại bằng lời của bạn (lưu trong trình duyệt):</p><div class="note" data-uid="{esc(uid)}"></div>'
        f'</details></td>'
        f'<td class="d">{mmss(r["dur"])}</td>'
        f'<td class="l"><a href="{esc(r["xem"])}">▶ xem bài</a> <a href="{esc(r["mp4"])}">tệp video</a> <a href="{esc(r["pv"])}">duyệt nhanh</a></td></tr>')


def page_html(data, seq, jd, les):
    esc = html.escape
    ready = [r for r in seq if r["ready"]]
    tot_h = sum(r["dur"] for r in ready) / 3600
    fast = [r for r in ready if r["stage"] in FAST]
    # bản đồ chặng
    mp = []
    for p in data:
        rr = [r for r in p["rows"] if r["ready"]]
        pend = len(p["rows"]) - len(rr)
        by = defaultdict(int)
        for r in p["rows"]:
            by[r["C"]] += 1
        mp.append(f'<tr><td><a href="#{p["k"]}">{esc(p["name"])}</a><div class="lvl">{esc(p["level"])}</div></td>'
                  f'<td>{esc(" · ".join(f"{C} {n}" for C, n in by.items()))}</td>'
                  f'<td>{len(rr)}{f" (+{pend} đang soạn)" if pend else ""}</td><td>{sum(r["dur"] for r in rr) / 3600:.1f}</td>'
                  f'<td><span class="sp" data-k="{p["k"]}"></span><div class="bar"><i data-k="{p["k"]}"></i></div></td></tr>')
    # bảng JD
    jr = []
    for topic, need, uids in jd:
        cells = []
        for st, u in uids:
            if st == "?":
                cells.append(f'<span class="mute">{esc(u)} (chưa có giáo án)</span>')
                continue
            r = next(x for x in seq if x["uid"] == u)
            lab = esc(u.replace(":", " "))
            cells.append(f'<a href="#{anchor(u)}">{lab}</a>' + ("" if r["ready"] else ' <span class="mute">(đang soạn)</span>'))
        jr.append(f'<tr><td>{esc(topic)}</td><td class="mute">{esc(need)}</td><td>{", ".join(cells)}</td></tr>')
    # các chặng
    parts = []
    for p in data:
        rr = [r for r in p["rows"] if r["ready"]]
        trs, prevC = [], None
        for r in p["rows"]:
            if r["C"] != prevC:
                trs.append(f'<tr class="course"><td colspan="4">Khoá {esc(r["C"])}{(" · " + esc(r["course"])) if r["course"] else ""}</td></tr>')
                prevC = r["C"]
            trs.append(row_html(r, les))
        parts.append(
            f'<section class="stage" id="{p["k"]}" data-k="{p["k"]}"><details{" open" if p["k"] == "S01" else ""}><summary><h2>{esc(p["name"])}</h2> '
            f'<span class="sum">· {len(rr)} bài · {sum(r["dur"] for r in rr) / 3600:.1f} giờ · <span class="prog" data-k="{p["k"]}"></span></span></summary>'
            f'<p class="lvl">{esc(p["level"])}</p><p>{esc(p["intro"])}</p>'
            f'<table><thead><tr><th>Đã học</th><th>Bài</th><th>Dài</th><th>Mở</th></tr></thead><tbody>{"".join(trs)}</tbody></table></details></section>')
    return f"""<!doctype html>
<html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Lộ trình học</title>
<style>{CSS}</style></head>
<body><main>
<h1>Lộ trình học: từ con số 0 tới senior</h1>
<p class="mute">Khoa học máy tính · công nghệ thông tin · trí tuệ nhân tạo · backend ngân hàng. Trang sinh tự động bằng <code>audit/review/learn_start/pack.py page</code>
từ giáo án <code>curriculum/*.yaml</code>, đặc tả bài và video thật trong <code>out/</code>; thứ tự chặng theo
<a href="interview/MASTER_CURRICULUM_INDEX.md">MASTER_CURRICULUM_INDEX.md</a>. Mở bằng trình duyệt, không cần mạng.</p>

<div class="card"><div class="dash">
<div>Đã học<b id="d-done">0</b><span class="mute" id="d-donep"></span></div>
<div>Giờ video đã học<b id="d-hrs">0</b><span class="mute">trên {tot_h:.0f} giờ</span></div>
<div>Cần ôn hôm nay<b id="d-due">0</b><button class="pri" id="b-review">Ôn ngay</button></div>
<div>Ngày học liên tục<b id="d-streak">0</b><span class="mute">ngày có học hoặc ôn</span></div>
</div>
<p id="d-next"></p>
<p>Mỗi ngày học <input type="number" id="c-min" min="10" max="600" step="10" value="60"> phút video → <span id="d-eta"></span>
<span class="mute">(tính cả thời gian dừng làm bài: mỗi phút video ≈ 2,5 phút học thật — ước lượng, không phải số đo).</span></p>
</div>

<section id="review" class="card"><h3>Ôn hôm nay</h3>
<p class="mute">Với mỗi bài: đọc câu hỏi, <b>tự trả lời ra giấy hoặc nói thành tiếng</b>, rồi mới mở đáp án và tự chấm thật lòng.
"Quên" đưa bài về ôn lại ngày mai; "nhớ chắc" giãn lịch ôn ra 1 → 3 → 7 → 14 → 30 → 60 → 120 ngày.</p>
<div id="rlist"></div><p><button id="b-close">Đóng</button></p></section>

<div class="card how"><b>Cách học để kiến thức thành của bạn và nhớ lâu</b>
<ol>
<li><b>Trước bài:</b> đọc mục tiêu bài và mục "Cần học trước". Chưa vững bài nào trong đó thì quay lại bài đó trước.</li>
<li><b>Trong bài:</b> bấm <i>▶ xem bài</i>. Khi video hỏi, dừng (phím cách), trả lời ra giấy rồi mới xem tiếp. Làm lại bằng tay mọi ví dụ có số; bài có mã thì gõ lại và chạy.</li>
<li><b>Ngay sau bài:</b> mở "Tự kiểm", trả lời không nhìn đáp án; viết "Giải thích lại bằng lời của bạn" như đang dạy người khác. Chỗ nào không viết được là chỗ chưa hiểu.</li>
<li><b>Tick "Đã học"</b> khi tự làm lại được mọi mục tiêu. Trang tự lên lịch ôn: ngày mai, rồi giãn dần. Mỗi ngày bấm <i>Ôn ngay</i> trước khi học bài mới.</li>
<li><b>Trộn bài khi ôn:</b> hàng "Ôn hôm nay" trộn các khoá khác nhau. Như vậy bạn phải tự nhận ra bài nào cần cách giải nào.</li>
<li><b>Sau mỗi chặng:</b> tự làm một dự án nhỏ dùng kiến thức cả chặng. Ví dụ, sau chặng 2–3, viết một API chuyển khoản có khoá lũy đẳng, sổ cái, Kafka, Redis, OpenAPI, Docker và CI.</li>
</ol>
<p class="mute">Cơ sở: hiệu ứng tự kiểm (Roediger &amp; Karpicke, 2006), ôn ngắt quãng (Cepeda và cộng sự, 2006), tổng quan kỹ thuật học
(Dunlosky và cộng sự, 2013). Các kết quả này đo trên người học nói chung; trên chính bạn thì chưa ai đo (NOT_VERIFIED).
Tiến độ chỉ lưu trong trình duyệt này: hãy <b>xuất tệp sao lưu</b> định kỳ (cuối trang).</p></div>

<h3>Bản đồ 11 chặng</h3>
<p class="mute">Chặng 1–4 là <b>đường nhanh phỏng vấn</b> ({len(fast)} bài, {sum(r["dur"] for r in fast) / 3600:.1f} giờ): đúng đường học tối thiểu của MASTER_INDEX.
Chặng 5 có thể học song song từ ngày đầu. Mỗi bài nằm đúng một chỗ, và máy đã kiểm mọi bài cần học trước đều đứng trước nó.
Tổng {len(ready)} bài có video ({tot_h:.1f} giờ){f", {len(seq) - len(ready)} bài đang soạn" if len(seq) > len(ready) else ""}.</p>
<table class="map"><thead><tr><th>Chặng</th><th>Khoá (số bài)</th><th>Bài có video</th><th>Giờ</th><th>Tiến độ</th></tr></thead><tbody>{"".join(mp)}</tbody></table>

<h3 id="jd">Đối chiếu yêu cầu tuyển dụng (JD) với bài học</h3>
<p class="mute">Nguồn: <code>resources/job/JD.md</code>, gồm tin Software Engineer trên acbjobs.com.vn và các tin Backend, Lead. Bấm mã bài để nhảy tới bài.</p>
<table class="jd"><thead><tr><th>Yêu cầu</th><th>Mức</th><th>Bài</th></tr></thead><tbody>{"".join(jr)}</tbody></table>

<h3>Tìm bài</h3>
<input type="search" id="q" placeholder="gõ tên khoá, mã bài hay từ khoá, ví dụ: Kafka, bế tắc, đạo hàm, JVA L05">
<p class="mute" id="qn"></p>
{"".join(parts)}

<div class="card" id="backup"><b>Sao lưu tiến độ</b>
<p class="mute">Dấu đã học, lịch ôn và ghi chú chỉ nằm trong trình duyệt này. Xoá dữ liệu trình duyệt là mất. Hãy xuất tệp mỗi tuần, và nhập lại khi đổi máy hay đổi trình duyệt.</p>
<p><button id="b-exp">Xuất tệp sao lưu</button> <label class="btn">Nhập tệp sao lưu <input type="file" id="f-imp" accept="application/json,.json" hidden></label> <span id="imp-msg"></span></p></div>
</main>
<script>
{JS}
</script>
</body></html>
"""


JS = r"""
(function () {
  var KEY = "hoc_tap_v2", OLD = "hoc_tap_done_v1", IV = [1, 3, 7, 14, 30, 60, 120];
  var S = { v: 2, L: {}, N: {}, A: {}, cfg: { min: 60 } };
  function today(off) { var d = new Date(); d.setHours(12, 0, 0, 0); if (off) d.setDate(d.getDate() + off); return d.toISOString().slice(0, 10); }
  function load() {
    try { var x = JSON.parse(localStorage.getItem(KEY) || "null"); if (x && x.v === 2) S = Object.assign(S, x); } catch (e) {}
    S.L = S.L || {}; S.N = S.N || {}; S.A = S.A || {}; S.cfg = S.cfg || { min: 60 };
    if (!S.cfg.mig) {                      // nhận dấu tick của trang cũ (đợt LS1): coi là đã học, ôn từ hôm nay
      try { var o = JSON.parse(localStorage.getItem(OLD) || "{}") || {}; Object.keys(o).forEach(function (u) { if (!S.L[u]) S.L[u] = { t: today(), b: 1, due: today(), r: 0, f: 0 }; }); } catch (e) {}
      S.cfg.mig = 1; save();
    }
  }
  function save() { try { localStorage.setItem(KEY, JSON.stringify(S)); } catch (e) {} }
  function act() { S.A[today()] = 1; }
  var rows = Array.prototype.slice.call(document.querySelectorAll("tr[data-dur]"));
  var byUid = {}; rows.forEach(function (tr) { byUid[tr.dataset.uid] = tr; });
  function label(u) { return u.replace(":", " "); }
  function learn(u, on) {
    if (on) { if (!S.L[u]) S.L[u] = { t: today(), b: 1, due: today(1), r: 0, f: 0 }; act(); }
    else delete S.L[u];
    save(); paint();
  }
  function grade(u, g) {                   // 0 quên · 1 lơ mơ · 2 nhớ chắc
    var x = S.L[u]; if (!x) return;
    if (g === 0) { x.b = 1; x.due = today(1); x.f = (x.f || 0) + 1; }
    else { if (g === 2) x.b = Math.min(x.b + 1, IV.length); x.due = today(IV[x.b - 1]); }
    x.r = (x.r || 0) + 1; x.last = today(); act(); save(); paint();
  }
  function dueList() {
    var t = today();
    return rows.map(function (tr) { return tr.dataset.uid; }).filter(function (u) { return S.L[u] && S.L[u].due <= t; })
      .sort(function (a, b) { return S.L[a].due < S.L[b].due ? -1 : S.L[a].due > S.L[b].due ? 1 : 0; });
  }
  function streak() { var n = 0, i = 0; if (!S.A[today()]) i = 1; while (S.A[today(-(n + i))]) n++; return n; }
  function paint() {
    var done = 0, sec = 0, tot = 0, t = today();
    rows.forEach(function (tr) {
      var u = tr.dataset.uid, x = S.L[u], b = tr.querySelector("input[type=checkbox]");
      tot += +tr.dataset.dur;
      b.checked = !!x; tr.classList.toggle("done", !!x);
      var du = tr.querySelector(".due");
      if (x) { done++; sec += +tr.dataset.dur; du.textContent = x.due <= t ? "· cần ôn" : "· ôn ngày " + x.due.split("-").reverse().join("/"); du.className = "due " + (x.due <= t ? "warn" : "mute"); }
      else du.textContent = "";
    });
    document.getElementById("d-done").textContent = done + "/" + rows.length;
    document.getElementById("d-donep").textContent = rows.length ? Math.round(100 * done / rows.length) + "% số bài" : "";
    document.getElementById("d-hrs").textContent = (sec / 3600).toFixed(1);
    document.getElementById("d-due").textContent = dueList().length;
    document.getElementById("d-streak").textContent = streak();
    document.querySelectorAll("section.stage").forEach(function (s) {
      var k = s.dataset.k, rr = s.querySelectorAll("tr[data-dur]"), n = 0;
      rr.forEach(function (tr) { if (S.L[tr.dataset.uid]) n++; });
      var txt = "đã học " + n + "/" + rr.length;
      s.querySelector(".prog").textContent = txt;
      var sp = document.querySelector('.sp[data-k="' + k + '"]'); if (sp) sp.textContent = txt;
      var bar = document.querySelector('.bar i[data-k="' + k + '"]'); if (bar) bar.style.width = (rr.length ? 100 * n / rr.length : 0) + "%";
    });
    var nx = rows.find(function (tr) { return !S.L[tr.dataset.uid]; }), el = document.getElementById("d-next");
    if (nx) {
      var miss = (nx.dataset.pre || "").split(" ").filter(function (p) { return p && byUid[p] && !S.L[p]; });
      el.innerHTML = "Bài nên học tiếp: <a href='#" + nx.id + "'>" + nx.querySelector(".t b").textContent + " ·" + nx.querySelector(".t").childNodes[1].textContent.replace(/^ ·/, "") + "</a>"
        + (miss.length ? " <span class='warn'>· còn thiếu bài cần học trước: " + miss.map(label).join(", ") + "</span>" : "");
    } else el.textContent = "Bạn đã đánh dấu học hết mọi bài có video. Hãy giữ nhịp ôn hằng ngày.";
    var min = +(S.cfg.min || 60), left = tot - sec, days = Math.ceil(left / 60 * 2.5 / min);
    document.getElementById("c-min").value = min;
    document.getElementById("d-eta").textContent = left > 0 ? "còn khoảng " + days + " ngày học (≈ " + (days / 30).toFixed(1) + " tháng)" : "đã xong";
  }
  document.addEventListener("change", function (e) {
    var b = e.target;
    if (b.type === "checkbox" && b.dataset.uid) {
      var u = b.dataset.uid, tr = byUid[u];
      if (b.checked) {
        var miss = (tr.dataset.pre || "").split(" ").filter(function (p) { return p && byUid[p] && !S.L[p]; });
        if (miss.length && !confirm("Bài này cần học trước: " + miss.map(label).join(", ") + ".\nCác bài đó chưa đánh dấu đã học. Vẫn đánh dấu bài này?")) { b.checked = false; return; }
      }
      learn(u, b.checked);
    } else if (b.id === "c-min") { S.cfg.min = Math.max(10, Math.min(600, +b.value || 60)); save(); paint(); }
  });
  document.addEventListener("toggle", function (e) {   // ô ghi chú chỉ tạo khi mở, đỡ nặng trang
    var d = e.target; if (!d.classList || !d.classList.contains("more") || !d.open) return;
    var box = d.querySelector(".note"); if (!box || box.firstChild) return;
    var ta = document.createElement("textarea"), u = box.dataset.uid;
    ta.placeholder = "Viết như đang giảng cho một người chưa học: bài này giải quyết vấn đề gì, cơ chế ra sao, ví dụ số nào, lỗi nào hay gặp."; ta.value = S.N[u] || "";
    ta.addEventListener("input", function () { if (ta.value.trim()) S.N[u] = ta.value; else delete S.N[u]; save(); });
    box.appendChild(ta);
  }, true);
  function showReview() {
    var R = document.getElementById("review"), list = document.getElementById("rlist"), du = dueList();
    list.innerHTML = "";
    if (!du.length) list.innerHTML = "<p class='ok'>Hôm nay không có bài nào đến hạn ôn. Học bài mới, hoặc tự chọn một bài cũ để ôn.</p>";
    du.slice(0, 30).forEach(function (u) {
      var tr = byUid[u], c = document.createElement("div"); c.className = "rcard";
      var q = tr.querySelector(".qq"), a = tr.querySelector(".qa"), rc = tr.querySelector(".rec");
      c.innerHTML = "<b>" + tr.querySelector(".t b").textContent + "</b> · " + tr.querySelector(".t").childNodes[1].textContent.replace(/^ · /, "")
        + " <span class='mute'>(hộp " + S.L[u].b + ", đã ôn " + (S.L[u].r || 0) + " lần)</span>"
        + "<div class='qq'>" + (q ? q.innerHTML : "") + "</div><details class='ans'><summary>Hiện đáp án và chuỗi logic</summary>"
        + (a ? a.innerHTML : "") + "<p class='h'>Chuỗi logic:</p><ul>" + (rc ? rc.innerHTML : "") + "</ul></details>"
        + "<div class='btns'><button data-g='0'>Quên — ôn lại ngày mai</button><button data-g='1'>Nhớ lơ mơ</button><button class='pri' data-g='2'>Nhớ chắc</button>"
        + " <a href='#" + tr.id + "'>mở bài</a></div>";
      c.querySelectorAll("button[data-g]").forEach(function (bt) { bt.addEventListener("click", function () { grade(u, +bt.dataset.g); c.remove(); if (!list.children.length) showReview(); }); });
      list.appendChild(c);
    });
    if (du.length > 30) list.insertAdjacentHTML("beforeend", "<p class='mute'>Còn " + (du.length - 30) + " bài đến hạn; ôn xong 30 bài này rồi mở lại.</p>");
    R.classList.add("on"); R.scrollIntoView({ behavior: "smooth" });
  }
  document.getElementById("b-review").addEventListener("click", showReview);
  document.getElementById("b-close").addEventListener("click", function () { document.getElementById("review").classList.remove("on"); });
  document.getElementById("q").addEventListener("input", function () {
    var v = this.value.trim().toLowerCase(), n = 0;
    document.querySelectorAll("section.stage").forEach(function (s) {
      var hit = 0;
      s.querySelectorAll("tbody tr").forEach(function (tr) {
        if (tr.classList.contains("course")) return;
        var ok = !v || tr.querySelector(".t").textContent.toLowerCase().indexOf(v) >= 0 || (tr.dataset.uid || "").toLowerCase().replace(":", " ").indexOf(v) >= 0;
        tr.classList.toggle("hide", !ok); if (ok) { hit++; n++; }
      });
      if (v && hit) s.querySelector("details").open = true;
    });
    document.getElementById("qn").textContent = v ? n + " bài khớp" : "";
  });
  document.getElementById("b-exp").addEventListener("click", function () {
    var blob = new Blob([JSON.stringify(S, null, 1)], { type: "application/json" }), a = document.createElement("a");
    a.href = URL.createObjectURL(blob); a.download = "hoc_tap_tien_do_" + today() + ".json"; document.body.appendChild(a); a.click(); a.remove();
  });
  document.getElementById("f-imp").addEventListener("change", function () {
    var f = this.files[0], msg = document.getElementById("imp-msg"); if (!f) return;
    var rd = new FileReader();
    rd.onload = function () {
      try {
        var x = JSON.parse(rd.result);
        if (!x || x.v !== 2 || typeof x.L !== "object") throw new Error("không phải tệp sao lưu của trang này");
        if (!confirm("Thay toàn bộ tiến độ hiện tại bằng tệp này (" + Object.keys(x.L).length + " bài đã học)?")) return;
        S = Object.assign({ v: 2, L: {}, N: {}, A: {}, cfg: { min: 60, mig: 1 } }, x); save(); paint(); msg.textContent = "Đã nhập.";
      } catch (e) { msg.textContent = "Không nhập được: " + e.message; }
    };
    rd.readAsText(f);
  });
  load(); paint();
  if (location.hash) { var t = document.querySelector(location.hash); if (t) { var d = t.closest("details"); if (d) d.open = true; t.scrollIntoView(); } }
  window.addEventListener("hashchange", function () { var t = document.querySelector(location.hash); if (t) { var d = t.closest("section.stage details"); if (d) d.open = true; t.scrollIntoView(); } });
})();
"""


def page_md(data, seq):
    md = ["# Lộ trình học từ con số 0 tới senior (SINH TỰ ĐỘNG bằng `audit/review/learn_start/pack.py page`, không sửa tay)", "",
          "Mở **[HOC_TAP.html](HOC_TAP.html)** trong trình duyệt để có danh sách bấm được, tự kiểm, lịch ôn ngắt quãng và ghi chú.", ""]
    for p in data:
        rr = [r for r in p["rows"] if r["ready"]]
        md += [f"## {p['name']}", "", f"*{p['level']}* — {p['intro']}", "",
               f"{len(rr)} bài có video · {sum(r['dur'] for r in rr) / 3600:.1f} giờ" + (f" · {len(p['rows']) - len(rr)} bài đang soạn" if len(p["rows"]) > len(rr) else ""), "",
               "| # | Bài | Thời lượng | Video |", "|---:|---|---:|---|"]
        md += [f"| {r['n']} | {r['C']} {r['id']} · {r['title'].replace('|', '/')} | {mmss(r['dur']) if r['ready'] else '—'} | "
               + (f"[{r['mp4']}]({r['mp4']})" if r["ready"] else "đang soạn") + " |" for r in p["rows"]]
        md.append("")
    return "\n".join(md)


def check_links(text, base=ROOT):
    hrefs = [h.split("#")[0] for h in re.findall(r'(?:href|src)="([^"#][^"]*)"', text)]
    dead = [h for h in hrefs if not (base / html.unescape(h)).resolve().exists()]
    return len(hrefs), dead


def check_anchors(text):
    ids = set(re.findall(r'id="([^"]+)"', text))
    return [h for h in re.findall(r'href="#([^"]+)"', text) if h not in ids]


def watch_html(r, prev, nxt):
    esc = html.escape
    up = "../../../"

    def link(x, label):
        if not x:
            return f'<span class="mute">{label}: không có</span>'
        return f'<a href="../../{esc(x["C"])}/{esc(x["id"])}/xem.html">{label}: {esc(x["C"])} {esc(x["id"])}</a>'
    chs = []
    for c in r["ch"]:
        m = re.match(r"(\d+):(\d\d)(?::(\d\d))? (.+)$", c)
        if not m:
            continue
        t = int(m.group(1)) * 60 + int(m.group(2)) if m.group(3) is None else int(m.group(1)) * 3600 + int(m.group(2)) * 60 + int(m.group(3))
        chs.append(f'<li><button data-t="{t}">{esc(c.split(" ", 1)[0])}</button> {esc(m.group(4))}</li>')
    obj = "".join(f"<li>{esc(o)}</li>" for o in r["obj"])
    qq = "".join(f"<p>{esc(x)}</p>" for x in r["q"]) + "".join(f'<img class="fr" loading="lazy" src="frames/{esc(Path(x).name)}" alt="khung câu hỏi trong video">' for x in r["qf"])
    qa = "".join(f"<p>{esc(x)}</p>" for x in r["a"]) + "".join(f'<img class="fr" loading="lazy" src="frames/{esc(Path(x).name)}" alt="khung đáp án trong video">' for x in r["af"])
    rec = "".join(f"<li>{esc(x)}</li>" for x in r["rec"])
    return f"""<!doctype html>
<html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(r["C"])} {esc(r["id"])}</title>
<style>
:root {{ --bg:#fbfaf7; --fg:#1d1d1b; --mute:#5c5a55; --line:#e2dfd8; --acc:#1f5fa8; --btn:#ece8df; }}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{ --bg:#16171a; --fg:#e8e6e1; --mute:#a5a29b; --line:#33353a; --acc:#7fb0ec; --btn:#2a2c31; }} }}
:root[data-theme="dark"] {{ --bg:#16171a; --fg:#e8e6e1; --mute:#a5a29b; --line:#33353a; --acc:#7fb0ec; --btn:#2a2c31; }}
body {{ background:var(--bg); color:var(--fg); font:16px/1.5 system-ui, "Segoe UI", sans-serif; margin:0; padding:0 16px 40px; }}
main {{ max-width:1100px; margin:0 auto; }} a {{ color:var(--acc); }} .mute {{ color:var(--mute); }}
h1 {{ font-size:1.3rem; margin:16px 0 8px; }} h2 {{ font-size:1.05rem; }} video {{ width:100%; background:#000; border-radius:6px; }}
.bar {{ display:flex; flex-wrap:wrap; gap:8px 16px; align-items:center; margin:8px 0; }}
button {{ background:var(--btn); color:var(--fg); border:1px solid var(--line); border-radius:6px; padding:4px 10px; font:inherit; cursor:pointer; }}
button.on {{ outline:2px solid var(--acc); }} .cols {{ display:grid; grid-template-columns:1fr 1fr; gap:24px; }}
ul {{ padding-left:20px; }} ul.ch {{ list-style:none; padding:0; }} ul.ch li {{ margin:4px 0; }} ul.ch li.cur {{ font-weight:600; }}
img.fr {{ display:block; width:100%; max-width:720px; height:auto; border:1px solid var(--line); border-radius:6px; margin:6px 0; }}
.self {{ border:1px solid var(--line); border-radius:8px; padding:4px 16px 12px; margin-top:16px; }} details summary {{ cursor:pointer; color:var(--acc); }}
@media (max-width:720px) {{ .cols {{ grid-template-columns:1fr; }} }}
</style></head>
<body><main>
<p class="bar"><a href="{up}HOC_TAP.html#{anchor(r["uid"])}">← trang lộ trình (tick đã học, lịch ôn)</a> {link(prev, "Bài trước")} {link(nxt, "Bài sau")}</p>
<h1>{esc(r["C"])} {esc(r["id"])} · {esc(r["title"])}</h1>
<video id="v" controls preload="metadata" src="{esc(r["id"])}.mp4"></video>
<p class="bar">Tốc độ: <button data-r="0.75">0,75×</button><button data-r="1" class="on">1×</button><button data-r="1.25">1,25×</button><button data-r="1.5">1,5×</button>
<span class="mute">Phím cách: dừng/chạy · ← →: lùi/tiến 5 giây</span></p>
<div class="cols"><section><h2>Mục lục (bấm để nhảy tới)</h2><ul class="ch">{"".join(chs)}</ul></section>
<section><h2>Học xong bạn làm được</h2><ul>{obj}</ul>
<p class="mute">Thời lượng {mmss(r["dur"])} · <a href="preview.html">duyệt nhanh từng khung</a> · <a href="{esc(r["id"])}.srt">phụ đề .srt</a></p></section></div>
<section class="self"><h2>Tự kiểm ngay sau khi xem</h2>
<p class="mute">Đừng xem lại video. Trả lời ra giấy hoặc nói thành tiếng, rồi mới mở đáp án.</p>
{qq}<details><summary>Hiện đáp án</summary>{qa}</details>
<h2>Chuỗi logic cần mang theo</h2><ul>{rec}</ul>
<p class="mute">Làm được hết thì quay lại trang lộ trình, tick "Đã học"; trang sẽ nhắc bạn ôn vào ngày mai, rồi giãn dần.</p></section>
</main>
<script>
(function () {{
  var v = document.getElementById("v");
  document.querySelectorAll("button[data-t]").forEach(function (b) {{
    b.addEventListener("click", function () {{ v.currentTime = +b.dataset.t; v.play(); }});
  }});
  document.querySelectorAll("button[data-r]").forEach(function (b) {{
    b.addEventListener("click", function () {{
      v.playbackRate = +b.dataset.r;
      document.querySelectorAll("button[data-r]").forEach(function (x) {{ x.classList.toggle("on", x === b); }});
    }});
  }});
  var items = Array.prototype.slice.call(document.querySelectorAll("ul.ch li"));
  v.addEventListener("timeupdate", function () {{
    var cur = -1;
    items.forEach(function (li, i) {{ if (+li.querySelector("button").dataset.t <= v.currentTime + 0.25) cur = i; }});
    items.forEach(function (li, i) {{ li.classList.toggle("cur", i === cur); }});
  }});
  document.addEventListener("keydown", function (e) {{
    if (e.target.tagName === "BUTTON" || e.target === v) return;
    if (e.key === " ") {{ e.preventDefault(); v.paused ? v.play() : v.pause(); }}
    else if (e.key === "ArrowRight") v.currentTime += 5;
    else if (e.key === "ArrowLeft") v.currentTime = Math.max(0, v.currentTime - 5);
  }});
}})();
</script>
</body></html>
"""


def cmd_page(cur):
    les, _ = lesson_index(cur)
    data, seq, jd = build_page(cur)
    uids = [r["uid"] for r in seq]
    assert len(uids) == len(set(uids)), "một bài nằm ở hai chỗ: nút bài trước/sau sẽ mơ hồ"
    h = page_html(data, seq, jd, les)
    (ROOT / "HOC_TAP.html").write_text(h, encoding="utf-8")
    (ROOT / "HOC_TAP.md").write_text(page_md(data, seq), encoding="utf-8")
    ready = [r for r in seq if r["ready"]]
    wn, wdead, pages = 0, [], []
    for i, r in enumerate(ready):
        w = watch_html(r, ready[i - 1] if i else None, ready[i + 1] if i + 1 < len(ready) else None)
        f = ROOT / r["xem"]
        f.write_text(w, encoding="utf-8")
        pages.append((r, w, f))
    for r, w, f in pages:            # kiểm sau khi đã ghi đủ mọi trang
        c, dd = check_links(w, f.parent)
        wn += c
        wdead += [f"{r['xem']} → {x}" for x in dd]
        wdead += [f"{r['xem']} → HOC_TAP.html#{a}" for a in re.findall(r'HOC_TAP\.html#([^"]+)"', w) if f'id="{a}"' not in h]
    print(f"xem.html: {len(pages)} trang, {wn} liên kết, chết {len(wdead)}")
    n, dead = check_links(h)
    adead = check_anchors(h)
    dead += wdead + [f"#{a}" for a in adead]
    mdl = re.findall(r"\]\(([^)#]+)\)", (ROOT / "HOC_TAP.md").read_text(encoding="utf-8"))
    mdead = [x for x in mdl if not (ROOT / x).exists()]
    nq = sum(1 for r in ready if r["q"] and r["a"])
    nf = sum(1 for r in ready if r["qf"] and r["af"])
    na = len(re.findall(r'href="#', h))
    print(f"HOC_TAP.html: {len(seq)} bài ({len(ready)} có video, {len(seq) - len(ready)} đang soạn), {n} liên kết tệp, "
          f"{na} liên kết neo, chết {len(dead)}; tự kiểm đủ câu+đáp án {nq}/{len(ready)}, có khung hình {nf}/{len(ready)}; "
          f"{len(h.encode('utf-8')) / 1e6:.2f} MB; HOC_TAP.md: {len(mdl)} liên kết, chết {len(mdead)}")
    for x in dead + mdead:
        print("  chết:", x)
    return 1 if dead or mdead or nq < len(ready) else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["list", "check", "preview", "page"])
    ap.add_argument("--decode", action="store_true")
    ap.add_argument("--tsv")
    ap.add_argument("--course", help="chỉ kiểm các khoá này, phân cách bằng dấu phẩy")
    a = ap.parse_args()
    cur = load_cur()
    if a.cmd == "list":
        return cmd_list(cur)
    if a.cmd == "check":
        return cmd_check(cur, a.decode, a.tsv, set(a.course.split(",")) if a.course else None)
    if a.cmd == "preview":
        return cmd_preview(cur)
    return cmd_page(cur)


if __name__ == "__main__":
    sys.exit(main() or 0)
