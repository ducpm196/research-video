"""[BẢN THỬ GIAO DIỆN — pack_dev.py: chỉ ghi HOC_TAP.dev.html, không ghi HOC_TAP.html/md/xem.html]
Trang học trọn lộ trình từ con số 0 tới senior (KHMT · CNTT · AI) — HOC_TAP.html, sinh tự động từ giáo án và video thật.

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
    ("S01", "Chặng 1 · Nền thực hành và lập trình Java từ con số 0", "MASTER cấp 0A (bắt buộc với người chưa từng lập trình)", ["FND", "JVA", "JV2"],
     "Dòng lệnh, tệp, dữ liệu, HTTP, SQL và Git để có chỗ đứng thực hành; rồi Java từ chương trình đầu tiên tới dự án nhiều tệp: biến, rẽ nhánh, vòng lặp, mảng, hàm, lớp, chuỗi, danh sách, ngoại lệ, giao diện, luồng, kiểm thử; kết thúc bằng sổ chuyển khoản nhỏ."),
    ("S02", "Chặng 2 · Nền tảng backend ngân hàng", "MASTER cấp 1A (bắt buộc, học trước INT/ACB)", ["BNK"],
     "Bộ nhớ và luồng của Java, Spring Boot, REST và khoá lũy đẳng, SQL và PL/SQL, Redis, Kafka, SAGA, sổ cái bút toán kép, T24, ISO 8583, đối soát, PIN/HSM."),
    ("S03", "Chặng 3 · Kỹ năng backend theo JD và CV", "Mở rộng cấp 1A — lấp khoảng trống JD và CV (MASTER Mục 8)", ["BNX"],
     "Những chủ đề JD và CV nêu mà kho chưa có bài: Git, OpenAPI, gRPC, JWT và OAuth, mTLS, thủ tục lưu trữ Oracle và SQL Server, Oracle cho khối lượng lớn, Elasticsearch, Couchbase, Kafka nâng cao và RabbitMQ, thanh toán quốc tế và ngoại tệ, ví điện tử và thuế điện tử, triển khai, DDD và Open API; rồi các bài theo CV: đa luồng Java nâng cao, Spring Security và Spring Cloud, JUnit 5 và Mockito, Redis nâng cao, Go, hệ thống cho vay số, Adobe Experience Manager, scikit-learn và ONNX Runtime."),
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
    # Đối chiếu CV (resources/job/PHAM-MINH-DUC-SENIOR-INTEGRATION-CV.md): mỗi dòng CV phải có bài dạy đủ để bị hỏi là trả lời được (đợt LF2, 2026-11-12).
    ("CV — Java đa luồng nâng cao: ExecutorService, CompletableFuture, ForkJoinPool", "hồ sơ CV", ["INT:L01", "BNX:L16"]),
    ("CV — Spring Security, Spring Security OAuth2, Spring Cloud, Consul", "hồ sơ CV", ["BNX:L04", "BNX:L17"]),
    ("CV — kiểm thử tự động: JUnit 5, Mockito", "hồ sơ CV", ["BNX:L18"]),
    ("CV — Redis Cluster, khoá SET NX EX, khử trùng theo mã giao dịch, danh sách đen JWT", "hồ sơ CV", ["BNK:L06", "BNX:L19", "BNX:L03"]),
    ("CV — Go (Golang), Fiber", "hồ sơ CV", ["BNX:L20"]),
    ("CV — hệ thống cho vay: LOS/LMS, chấm điểm tín dụng, thẩm định, ký số + ECM, 2FA, dấu vân tay thiết bị, trường đa trị T24", "hồ sơ CV", ["BNX:L21", "ACB:L04", "ACB:L08"]),
    ("CV — Adobe Experience Manager: OSGi, Sling Models, HTL, JCR", "hồ sơ CV", ["BNX:L22"]),
    ("CV — Scikit-Learn, ONNX Runtime, Isolation Forest (dự án học tập)", "hồ sơ CV", ["BNX:L23", "INT:L05", "CS115:L37"]),
    ("CV — CQRS, DLQ, Kafka, saga, outbox (tích hợp ngân hàng)", "hồ sơ CV", ["EVT:L02", "EVT:L04", "EVT:L05", "BNX:L10", "CLD:L14"]),
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
    # AF2: trong cùng một khoá, bài đứng sau luôn học SAU bài đứng trước theo thứ tự tác giả (cạnh ngầm CHỈ để xếp dãy, không hiện
    # ở "Cần học trước"). Đo bằng audit/review/check_next_refs.py: 551 lời hẹn "Bài sau (bài N)", 93 lệch dãy học → 0 lệch.
    pre = {u: set(v) for u, v in pre.items()}
    for C, c in cur.items():
        ids = [l["id"] for l in c["lessons"]]
        for a, b in zip(ids, ids[1:]):
            pre[f"{C}:{b}"].add(f"{C}:{a}")
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


LAB_RE = re.compile(r"labs/([A-Za-z0-9]+)/(L\d+)")
SHORT = {"S01": "Nền tảng, Java", "S02": "Backend ngân hàng", "S03": "Kỹ năng JD/CV", "S04": "Ôn phỏng vấn", "S05": "Toán và thuật toán",
         "S06": "Máy tính, mạng", "S07": "Kỹ nghệ, CSDL", "S08": "Hệ phân tán", "S09": "AI và học máy", "S10": "Chuyên gia", "S11": "Mở rộng"}


def lab_of(spec):
    """Đường lab của bài: cảnh `kind: practice` có trường `lab: labs/<KHOÁ>/<Lxx>` (hợp đồng ENV.md). Không có → None."""
    for scn in spec.get("scenes") or []:
        if scn.get("kind") == "practice" and scn.get("lab"):
            p = str(scn["lab"]).strip().strip("/")
            assert LAB_RE.fullmatch(p), f"trường lab sai dạng labs/<KHOÁ>/<Lxx>: {p} ({spec.get('id')})"
            return p
    return None


def kind_of(title, spec):
    """Loại bài suy ra từ dữ liệu có sẵn: tiêu đề giáo án mở đầu bằng "Hành trình" / "Tình huống", hoặc loạt (series) của đặc tả ghi "Tình huống chuyên gia"."""
    t = str(title).strip()
    if t.startswith("Hành trình"):
        return "journey"
    if t.startswith("Tình huống") or "Tình huống chuyên gia" in str((spec or {}).get("series") or ""):
        return "case"
    return ""


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
            dur, chaps, q, a, rec, pit, qf, af, lab, sp = 0.0, [], [], [], [], [], [], [], None, None
            if ready:
                j, _ = ffprobe(mp4)
                dur = float(j["format"]["duration"]) if j else 0.0
                chaps = [c for c in (d / "chapters.txt").read_text(encoding="utf-8").splitlines() if c.strip()] if (d / "chapters.txt").exists() else []
                sp = spec_of(l)
                q, a, rec, pit, qf, af = study_bits(sp, d)
                lab = lab_of(sp)
            r = {"uid": uid, "C": C, "id": l["id"], "title": l["title"], "dur": dur, "ready": ready, "stage": k,
                 "obj": [str(o) for o in (l.get("objectives") or [])], "pre": sorted(pre[uid], key=lambda x: (x.split(":")[0], x)),
                 "mp4": rel(mp4), "srt": rel(d / f"{l['id']}.srt"), "pv": rel(d / "preview.html"), "xem": rel(d / "xem.html"),
                 "ch": chaps, "q": q, "a": a, "qf": qf, "af": af, "rec": rec, "pit": pit, "course": cur[C].get("title") or "",
                 "lab": lab, "kind": kind_of(l["title"], sp)}
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


# ───────────────────────── giao diện ─────────────────────────
# Màu: mỗi cặp chữ/nền ≥ 4,5:1 ở cả hai chế độ (đo trong trình duyệt thật ở bước kiểm). Cùng một bộ biến cho "tối theo máy" và "tối do người dùng chọn".
DARK_VARS = ("--bg:#0e1116; --card:#161b22; --fg:#e7eaf0; --mute:#a3acba; --line:#2f3745; --acc:#8fb4ff; --acc-fg:#0b1220; --acc-soft:#1b2a47; --acc-soft-fg:#c9daff; "
             "--ok:#5bd68a; --ok-soft:#14301f; --warn:#f2b266; --warn-soft:#33240f; --row:#1d232d; --hero-a:#18274a; --hero-b:#10151d; "
             "--cont-bg:#1b3a7a; --cont-fg:#ffffff; --cont-mute:#d3defa; --cont-btn:#ffffff; --cont-btn-fg:#0f2a66; --cc-bg:40%; --cc-l:22%; --cc-fgl:86%; --cc-fgs:80%; --shadow:0 1px 2px rgba(0,0,0,.4);")

CSS = """
:root { --bg:#f5f6f8; --card:#ffffff; --fg:#161a22; --mute:#4a5262; --line:#d3d9e3; --acc:#1d4ed8; --acc-fg:#ffffff; --acc-soft:#e6edff; --acc-soft-fg:#1e3a8a;
  --ok:#166534; --ok-soft:#e3f5ea; --warn:#9a3412; --warn-soft:#fff1e6; --row:#eef1f6; --hero-a:#e4edff; --hero-b:#f5f6f8;
  --cont-bg:#1e3a8a; --cont-fg:#ffffff; --cont-mute:#dbe4ff; --cont-btn:#ffffff; --cont-btn-fg:#1e3a8a; --cc-bg:70%; --cc-l:91%; --cc-fgl:22%; --cc-fgs:60%;
  --shadow:0 1px 2px rgba(20,30,50,.08); --nav-h:96px; color-scheme:light; }
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { @@DARK@@ color-scheme:dark; } }
:root[data-theme="dark"] { @@DARK@@ color-scheme:dark; }
* { box-sizing:border-box; }
[hidden] { display:none !important; }
html { -webkit-text-size-adjust:100%; }
@media (prefers-reduced-motion: no-preference) { html { scroll-behavior:smooth; } }
body { background:var(--bg); color:var(--fg); font:16px/1.55 system-ui, "Segoe UI", Roboto, sans-serif; margin:0; overflow-wrap:anywhere; }
.wrap { max-width:1120px; margin:0 auto; padding:0 16px; }
main { padding-bottom:56px; }
h1, h2, h3, h4, p, ul, ol { margin:0; }
a { color:var(--acc); } code { font:.9em ui-monospace, Consolas, monospace; background:var(--row); padding:1px 5px; border-radius:4px; overflow-wrap:anywhere; }
.mute { color:var(--mute); } .ok { color:var(--ok); } .warn { color:var(--warn); }
:focus-visible { outline:3px solid var(--acc); outline-offset:2px; border-radius:4px; }
.sr { position:absolute; width:1px; height:1px; overflow:hidden; clip:rect(0 0 0 0); white-space:nowrap; }
.skip { position:absolute; left:8px; top:-60px; background:var(--acc); color:var(--acc-fg); padding:8px 14px; border-radius:6px; z-index:60; } .skip:focus { top:8px; }

/* nút */
button, .btn { display:inline-flex; align-items:center; justify-content:center; gap:6px; min-height:36px; background:var(--row); color:var(--fg); border:1px solid var(--line);
  border-radius:8px; padding:5px 14px; font:inherit; font-size:.93rem; font-weight:600; cursor:pointer; text-decoration:none; line-height:1.2; }
button:hover, .btn:hover { border-color:var(--acc); }
button, .btn { white-space:nowrap; }
button.pri, .btn.pri { background:var(--acc); color:var(--acc-fg); border-color:var(--acc); }
button.pri:hover, .btn.pri:hover { filter:brightness(1.08); }
.btn.lab { background:var(--ok-soft); color:var(--ok); border-color:var(--ok); }
.btn.sm { min-height:32px; padding:3px 12px; }
input[type=number] { width:5.2em; font:inherit; padding:4px 6px; border:1px solid var(--line); border-radius:6px; background:var(--card); color:var(--fg); }

/* hero */
.hero { background:linear-gradient(160deg, var(--hero-a), var(--hero-b)); border-bottom:1px solid var(--line); padding:28px 0 26px; }
.hero .wrap { display:grid; gap:18px 28px; grid-template-columns:1fr; }
.eyebrow { font-size:.8rem; font-weight:700; letter-spacing:.08em; text-transform:uppercase; color:var(--acc-soft-fg); background:var(--acc-soft); display:inline-block; padding:2px 10px; border-radius:20px; }
.hero h1 { font-size:clamp(1.65rem, 4.6vw, 2.5rem); line-height:1.15; margin:10px 0 8px; letter-spacing:-.01em; }
.lead { font-size:1.08rem; max-width:40em; } .facts { margin-top:10px; font-size:.93rem; }
.facts span { display:inline-block; margin:2px 14px 2px 0; }
.next { background:var(--cont-bg); color:var(--cont-fg); border-radius:14px; padding:16px 18px; box-shadow:var(--shadow); }
.next .lbl { font-size:.78rem; font-weight:700; letter-spacing:.08em; text-transform:uppercase; color:var(--cont-mute); }
.next h2 { font-size:1.22rem; line-height:1.3; margin:4px 0 4px; }
.next .code { font:700 .9rem ui-monospace, Consolas, monospace; background:rgba(255,255,255,.16); color:var(--cont-fg); padding:1px 8px; border-radius:5px; margin-right:6px; white-space:nowrap; }
.next .sub { color:var(--cont-mute); font-size:.92rem; }
.next .alert { margin-top:8px; background:rgba(0,0,0,.28); color:#fff; border-radius:8px; padding:6px 10px; font-size:.92rem; }
.next .alert a { color:#fff; font-weight:700; }
.next .btns { display:flex; flex-wrap:wrap; gap:8px; margin-top:12px; }
.next .btn.go { background:var(--cont-btn); color:var(--cont-btn-fg); border-color:var(--cont-btn); font-size:1rem; min-height:42px; padding:6px 20px; }
.next .btn.alt { background:transparent; color:var(--cont-fg); border-color:rgba(255,255,255,.55); min-height:42px; }
.next :focus-visible { outline-color:#fff; }
.panel { background:var(--card); border:1px solid var(--line); border-radius:14px; padding:16px; box-shadow:var(--shadow); }
.ringbox { display:flex; align-items:center; gap:16px; }
.ring { width:132px; height:132px; flex:none; } .ring .rt { stroke:var(--line); } .ring .ra { stroke:var(--acc); transition:stroke-dashoffset .5s; }
.ring text { fill:var(--fg); font-family:inherit; text-anchor:middle; } .ring .rp { font-size:26px; font-weight:800; } .ring .rs { font-size:10px; fill:var(--mute); }
.ringtxt b { display:block; font-size:1.5rem; line-height:1.1; font-variant-numeric:tabular-nums; } .ringtxt span { font-size:.9rem; }
.tiles { display:grid; grid-template-columns:repeat(3, 1fr); gap:8px; margin-top:14px; }
.tile { background:var(--row); border-radius:10px; padding:8px 10px; } .tile b { display:block; font-size:1.35rem; line-height:1.2; font-variant-numeric:tabular-nums; } .tile span { font-size:.82rem; color:var(--mute); line-height:1.25; display:block; }
.tile.due b.hot { color:var(--warn); }
.plan { margin-top:12px; font-size:.9rem; } .plan .mute { font-size:.82rem; }
@media (prefers-reduced-motion: reduce) { .ring .ra { transition:none; } }
@media (min-width:900px) { .hero .wrap { grid-template-columns:minmax(0,1.35fr) minmax(0,1fr); align-items:start; } .hero .panel { grid-column:2; grid-row:1 / span 2; } }

/* thanh điều hướng dính */
.top { position:sticky; top:0; z-index:40; background:var(--card); border-bottom:1px solid var(--line); box-shadow:var(--shadow); }
.top .r1 { display:flex; align-items:center; gap:10px; padding:8px 0 4px; }
.top .brand { font-weight:800; white-space:nowrap; display:none; } .top .brand i { font-style:normal; color:var(--acc); }
.sbox { position:relative; flex:1; min-width:0; }
.sbox svg { position:absolute; left:10px; top:50%; transform:translateY(-50%); width:16px; height:16px; stroke:var(--mute); fill:none; stroke-width:2; pointer-events:none; }
input[type=search] { width:100%; min-height:38px; font:inherit; padding:6px 36px 6px 34px; border:1px solid var(--line); border-radius:20px; background:var(--row); color:var(--fg); }
input[type=search]::placeholder { color:var(--mute); opacity:1; }
.kbd { position:absolute; right:10px; top:50%; transform:translateY(-50%); font:600 .72rem ui-monospace, Consolas, monospace; color:var(--mute); border:1px solid var(--line); border-radius:4px; padding:0 5px; display:none; }
.iconbtn { width:38px; min-height:38px; padding:0; border-radius:50%; flex:none; } .iconbtn svg { width:18px; height:18px; stroke:currentColor; fill:none; stroke-width:2; stroke-linecap:round; stroke-linejoin:round; }
.top .tdue { display:none; }
.chips { display:flex; gap:6px; overflow-x:auto; padding:2px 0 8px; scrollbar-width:thin; }
.chip { position:relative; flex:none; display:flex; align-items:center; gap:6px; padding:4px 10px 6px; border:1px solid var(--line); border-radius:8px; background:var(--card); color:var(--fg); text-decoration:none; font-size:.86rem; white-space:nowrap; overflow:hidden; }
.chip b { display:inline-grid; place-items:center; min-width:22px; height:22px; border-radius:50%; background:var(--row); font-size:.78rem; }
.chip .cp { font-style:normal; color:var(--mute); font-size:.78rem; font-variant-numeric:tabular-nums; }
.chip::after { content:""; position:absolute; left:0; bottom:0; height:3px; width:var(--p, 0%); background:var(--ok); }
.chip:hover { border-color:var(--acc); } .chip.on { background:var(--acc-soft); border-color:var(--acc); color:var(--acc-soft-fg); } .chip.on b { background:var(--acc); color:var(--acc-fg); }
.chip.fin b { background:var(--ok); color:var(--bg); }
.chip.misc { border-style:dashed; }
@media (min-width:700px) { .top .brand { display:block; } .sbox { max-width:560px; } .kbd { display:block; } .top .tdue { display:inline-flex; } }

/* tiêu đề phần */
.sec { margin-top:34px; } .sec > h2.st { font-size:1.35rem; margin-bottom:4px; } .sec > .mute { max-width:52em; }
section, details#jd, #review, .les, .sec, #backup { scroll-margin-top:calc(var(--nav-h) + 8px); }

/* ôn hôm nay */
#review { display:none; margin-top:20px; } #review.on { display:block; }
.card { background:var(--card); border:1px solid var(--line); border-radius:12px; padding:14px 18px; box-shadow:var(--shadow); }
#review h3 { font-size:1.15rem; margin-bottom:4px; }
.rcard { border:1px solid var(--line); border-radius:10px; padding:12px 16px; margin:10px 0; background:var(--bg); }
.rcard .btns { display:flex; flex-wrap:wrap; gap:8px; margin-top:10px; }

/* bản đồ lộ trình */
.strip { display:flex; gap:3px; margin:16px 0 6px; align-items:flex-end; padding-top:20px; }
.seg { position:relative; flex:1 1 0; min-width:0; height:30px; background:var(--row); border:1px solid var(--line); border-radius:6px; overflow:hidden; text-decoration:none; color:var(--fg); display:grid; place-items:center; font-size:.78rem; font-weight:700; }
.seg i { position:absolute; left:0; top:0; bottom:0; width:0; background:var(--ok-soft); } .seg span { position:relative; }
.seg.fast { border-top:3px solid var(--acc); } .seg.cur { outline:3px solid var(--acc); outline-offset:1px; z-index:1; }
.seg:hover { border-color:var(--acc); }
.slegend { font-size:.86rem; display:flex; flex-wrap:wrap; gap:6px 16px; margin-bottom:10px; }
.slegend i { display:inline-block; width:12px; height:12px; border-radius:3px; vertical-align:-1px; margin-right:5px; border:1px solid var(--line); }
.tl { list-style:none; padding:0; margin:12px 0 0; position:relative; }
.tl li { position:relative; padding:0 0 12px 46px; }
.tl li::before { content:""; position:absolute; left:15px; top:30px; bottom:-4px; width:3px; background:var(--line); border-radius:2px; }
.tl li:last-child::before { display:none; }
.tl li.fast::before { background:var(--acc); }
.node { position:absolute; left:0; top:6px; width:34px; height:34px; border-radius:50%; display:grid; place-items:center; background:var(--card); border:3px solid var(--line); font-weight:800; font-size:.9rem; z-index:1; }
.tl li.fast .node { border-color:var(--acc); }
.tl li.fin .node { background:var(--ok); border-color:var(--ok); color:var(--bg); } .tl li.fin .node span { display:none; } .tl li.fin .node::after { content:"✓"; }
.tl li.cur .node { background:var(--acc); border-color:var(--acc); color:var(--acc-fg); box-shadow:0 0 0 4px var(--acc-soft); }
a.mcard { display:block; background:var(--card); border:1px solid var(--line); border-radius:12px; padding:12px 16px; text-decoration:none; color:var(--fg); box-shadow:var(--shadow); }
a.mcard:hover { border-color:var(--acc); }
.tl li.cur a.mcard { border-color:var(--acc); border-width:2px; padding:11px 15px; }
.mcard .mt { font-weight:700; font-size:1.02rem; line-height:1.3; } .mcard .lv { font-size:.85rem; color:var(--mute); margin-top:2px; }
.mcard .mm { display:flex; flex-wrap:wrap; gap:4px 14px; font-size:.9rem; margin-top:6px; } .mcard .mm b { font-variant-numeric:tabular-nums; }
.mcard .cs { display:flex; flex-wrap:wrap; gap:5px; margin-top:8px; }
.mcard .mp { display:flex; align-items:center; gap:10px; margin-top:10px; font-size:.85rem; color:var(--mute); font-variant-numeric:tabular-nums; white-space:nowrap; } .mcard .mp .bar { flex:1; }
.tag { display:inline-block; font-size:.74rem; font-weight:700; border-radius:20px; padding:1px 9px; margin-left:6px; vertical-align:2px; white-space:nowrap; }
.tag.fast { background:var(--acc-soft); color:var(--acc-soft-fg); } .tag.here { display:none; background:var(--acc); color:var(--acc-fg); position:static; transform:none; }
.tl li.cur .tag.here { display:inline-block; } .tag.fin { display:none; background:var(--ok-soft); color:var(--ok); } .tl li.fin .tag.fin { display:inline-block; }
.cc { display:inline-block; font-size:.78rem; font-weight:700; border-radius:6px; padding:0 8px; background:hsl(var(--h) var(--cc-bg) var(--cc-l)); color:hsl(var(--h) var(--cc-fgs) var(--cc-fgl)); white-space:nowrap; }
.cc small { font-weight:600; font-size:.78rem; margin-left:3px; }
.bar { height:7px; background:var(--row); border:1px solid var(--line); border-radius:4px; overflow:hidden; } .bar i { display:block; height:100%; background:var(--acc); width:0; }
.bar.full i { background:var(--ok); }
@media (min-width:900px) {
  .tl { display:block; } a.mcard { display:grid; grid-template-columns:minmax(0,1.5fr) minmax(0,1fr) 180px; gap:6px 20px; align-items:center; }
  .mcard .mm { margin-top:2px; } .mcard .cs { margin-top:0; grid-column:2; grid-row:1 / span 2; } .mcard .mp { margin-top:0; grid-column:3; grid-row:1 / span 2; }
  .mcard .mt, .mcard .lv, .mcard .mm { grid-column:1; }
}

/* cách học */
.steps { list-style:none; padding:0; margin:14px 0 0; display:grid; gap:12px; grid-template-columns:repeat(auto-fit, minmax(230px, 1fr)); counter-reset:s; }
.steps li { background:var(--card); border:1px solid var(--line); border-radius:12px; padding:14px 16px; box-shadow:var(--shadow); counter-increment:s; position:relative; }
.steps .ic { font-size:1.6rem; line-height:1; display:block; margin-bottom:6px; }
.steps b { display:block; font-size:1.02rem; margin-bottom:2px; } .steps b::before { content:counter(s) ". "; color:var(--acc); }
.steps p { font-size:.93rem; color:var(--mute); }
.two { display:grid; gap:12px; grid-template-columns:1fr; margin-top:12px; } @media (min-width:800px) { .two { grid-template-columns:1fr 1fr; } }
.tips li { margin:4px 0; font-size:.93rem; } .tips { padding-left:20px; margin-top:6px; }
.machine h3 { font-size:1.05rem; } .reqs { display:flex; flex-wrap:wrap; gap:6px; margin:8px 0; list-style:none; padding:0; }
.reqs li { background:var(--row); border:1px solid var(--line); border-radius:20px; padding:2px 12px; font-size:.9rem; font-weight:600; }
.basis > summary { cursor:pointer; color:var(--mute); font-size:.9rem; margin-top:10px; } .basis p { font-size:.88rem; color:var(--mute); margin-top:6px; }

/* chặng */
.stagebar { display:flex; flex-wrap:wrap; align-items:center; gap:10px 18px; margin:12px 0 0; }
.stagebar label { display:inline-flex; align-items:center; gap:8px; font-size:.93rem; cursor:pointer; min-height:36px; }
.stagebar input { width:18px; height:18px; accent-color:var(--acc); }
section.stage { margin-top:12px; background:var(--card); border:1px solid var(--line); border-radius:14px; box-shadow:var(--shadow); }
section.stage > details > summary { list-style:none; cursor:pointer; display:grid; grid-template-columns:auto minmax(0,1fr); gap:4px 14px; align-items:center; padding:14px 16px; border-radius:14px; }
section.stage > details > summary::-webkit-details-marker, .course > summary::-webkit-details-marker, details.more > summary::-webkit-details-marker { display:none; }
.sn { width:40px; height:40px; border-radius:50%; background:var(--row); display:grid; place-items:center; font-weight:800; border:3px solid var(--line); }
section.stage.fast .sn { border-color:var(--acc); } section.stage.fin .sn { background:var(--ok); border-color:var(--ok); color:var(--bg); }
.sh h2 { font-size:1.12rem; line-height:1.3; } .sh .sm { font-size:.88rem; color:var(--mute); margin-top:2px; }
.sh .sp { display:flex; align-items:center; gap:10px; margin-top:6px; font-size:.85rem; color:var(--mute); font-variant-numeric:tabular-nums; } .sh .sp .bar { flex:1; max-width:340px; }
.chev::after { content:"▸"; display:inline-block; margin-left:8px; transition:transform .15s; color:var(--mute); }
details[open] > summary .chev::after { transform:rotate(90deg); }
.sbody { padding:0 16px 14px; } .sbody .intro { margin:2px 0 10px; font-size:.94rem; } .sbody .lvl { font-size:.85rem; color:var(--mute); margin-bottom:2px; }
.course { margin-top:10px; border:1px solid var(--line); border-radius:10px; overflow:hidden; background:var(--bg); }
.course > summary { list-style:none; cursor:pointer; display:flex; flex-wrap:wrap; align-items:center; gap:4px 10px; padding:9px 12px; background:var(--row); font-weight:600; }
.course > summary .cname { flex:1 1 220px; min-width:0; } .course .cprog { font-size:.85rem; font-weight:400; color:var(--mute); font-variant-numeric:tabular-nums; white-space:nowrap; }
.course .bar { width:90px; }
ol.ls { list-style:none; margin:0; padding:0; }

/* bài học */
.les { display:grid; grid-template-columns:44px minmax(0,1fr) auto; grid-template-areas:"chk main acts" "chk meta more"; column-gap:6px; align-items:center; padding:8px 12px 8px 4px; border-top:1px solid var(--line); background:var(--card); }
.les:first-child { border-top:0; }
.les.hide { display:none; }
.les .chk { grid-area:chk; align-self:start; position:relative; display:grid; place-items:center; width:44px; height:44px; cursor:pointer; }
.les .chk input { position:absolute; inset:0; width:100%; height:100%; margin:0; opacity:0; cursor:pointer; }
.box { width:24px; height:24px; border:2px solid var(--mute); border-radius:7px; display:grid; place-items:center; background:var(--card); }
.les .chk input:checked + .box { background:var(--ok); border-color:var(--ok); } .les .chk input:checked + .box::after { content:"✓"; color:var(--bg); font-weight:800; font-size:.95rem; line-height:1; }
.les .chk input:focus-visible + .box { outline:3px solid var(--acc); outline-offset:2px; }
.les .chk.ph .box { border-style:dashed; border-color:var(--line); }
.les .main { grid-area:main; min-width:0; padding-top:2px; }
.ttl { line-height:1.35; } .ttl .code { display:inline-block; font:700 .8rem ui-monospace, Consolas, monospace; background:var(--row); border:1px solid var(--line); border-radius:5px; padding:0 6px; margin-right:6px; white-space:nowrap; color:var(--fg); }
.ttl .name { font-weight:600; }
.les.done .name { color:var(--mute); font-weight:500; }
.bd { display:inline-block; font-size:.72rem; font-weight:700; border-radius:20px; padding:0 8px; margin-left:6px; vertical-align:1px; white-space:nowrap; background:var(--row); color:var(--mute); border:1px solid var(--line); }
.bd.j { background:var(--acc-soft); color:var(--acc-soft-fg); border-color:transparent; } .bd.c { background:var(--warn-soft); color:var(--warn); border-color:transparent; }
.les .meta { grid-area:meta; display:flex; flex-wrap:wrap; align-items:center; gap:2px 12px; font-size:.84rem; color:var(--mute); min-width:0; padding-bottom:2px; }
.meta .no { font-variant-numeric:tabular-nums; } .meta .dur { font-variant-numeric:tabular-nums; } .meta .dur::before { content:"⏱ "; }
.meta .due.warn { font-weight:700; } .meta .pre a { margin-right:5px; } .meta .labnote { font:.82rem ui-monospace, Consolas, monospace; color:var(--ok); }
.les .acts { grid-area:acts; display:flex; gap:6px; align-items:center; justify-content:flex-end; flex-wrap:wrap; }
.les.pend { background:var(--bg); } .les.pend .box { background:transparent; } .les.pend .name { color:var(--mute); font-weight:500; }
.les.pend .meta .soon { font-style:italic; }
details.more { grid-column:3; grid-row:2; justify-self:end; min-width:0; }
details.more > summary { list-style:none; cursor:pointer; display:inline-flex; align-items:center; gap:4px; min-height:30px; padding:2px 12px; border-radius:20px; border:1px solid var(--line); background:var(--row); color:var(--acc); font-size:.86rem; font-weight:600; }
details.more > summary:hover { border-color:var(--acc); } details.more > summary::after { content:"▾"; }
details.more[open] { grid-column:2 / -1; grid-row:3; justify-self:stretch; padding:8px 0 4px; }
details.more[open] > summary::after { content:"▴"; }
.more .body { margin-top:10px; border-left:3px solid var(--acc-soft); padding:2px 0 4px 14px; font-size:.93rem; }
.more .h { margin:10px 0 2px; font-weight:700; font-size:.92rem; } .more ul, .more ol { margin:4px 0; padding-left:20px; } .more p { margin:4px 0; }
details.ans > summary { cursor:pointer; color:var(--acc); font-weight:600; min-height:32px; margin-top:4px; display:flex; align-items:center; }
.basis > summary { min-height:32px; display:flex; align-items:center; }
.labbox { background:var(--ok-soft); border-radius:8px; padding:8px 12px; margin-top:8px; } .labbox code { background:var(--card); }
img.fr { display:block; width:100%; max-width:640px; height:auto; border:1px solid var(--line); border-radius:6px; margin:6px 0; }
textarea { width:100%; min-height:5.5em; font:inherit; font-size:.92rem; background:var(--card); color:var(--fg); border:1px solid var(--line); border-radius:8px; padding:8px; resize:vertical; }
.alt a { margin-right:12px; }
@media (max-width:640px) {
  .les { grid-template-columns:44px minmax(0,1fr); grid-template-areas:"chk main" "chk acts" "chk meta" "chk more"; padding-right:8px; }
  .les .acts { justify-content:flex-start; margin:4px 0 2px; } details.more { grid-area:more; justify-self:start; }
  details.more[open] { grid-area:more; justify-self:stretch; }
  .btn.sm { min-height:38px; }
  .ring { width:104px; height:104px; } .tiles { grid-template-columns:1fr 1fr; } .tile.due { grid-column:1 / -1; }
}

/* JD */
details#jd { margin-top:34px; background:var(--card); border:1px solid var(--line); border-radius:14px; box-shadow:var(--shadow); }
details#jd > summary { cursor:pointer; list-style:none; padding:14px 16px; font-weight:700; font-size:1.15rem; } details#jd > summary::-webkit-details-marker { display:none; }
details#jd .jdb { padding:0 16px 14px; }
table.jd { width:100%; border-collapse:collapse; margin-top:10px; } table.jd th, table.jd td { text-align:left; vertical-align:top; padding:8px 8px; border-bottom:1px solid var(--line); font-size:.92rem; }
table.jd th { font-size:.8rem; text-transform:uppercase; letter-spacing:.04em; color:var(--mute); } table.jd td.need { white-space:nowrap; }
.pill { display:inline-block; background:var(--row); border:1px solid var(--line); border-radius:20px; padding:0 9px; font-size:.8rem; color:var(--mute); }
table.jd td.refs a { display:inline-block; margin:0 8px 2px 0; white-space:nowrap; }
@media (max-width:700px) { table.jd thead { display:none; } table.jd tr { display:block; padding:8px 0; border-bottom:1px solid var(--line); } table.jd td { display:block; border:0; padding:2px 0; } }

/* sao lưu, chân trang */
#backup { margin-top:34px; } #backup h2 { font-size:1.1rem; } #backup .row { display:flex; flex-wrap:wrap; gap:8px; align-items:center; margin-top:10px; }
.foot { margin-top:26px; font-size:.86rem; color:var(--mute); }
"""
CSS = CSS.replace("@@DARK@@", DARK_VARS)

THEME_JS = """(function(){try{var t=localStorage.getItem("hoc_tap_theme");if(t==="dark"||t==="light")document.documentElement.setAttribute("data-theme",t);}catch(e){}})();"""

ICON_SEARCH = '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/></svg>'
ICON_THEME = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>')


FASTTAG = '<span class="tag fast">Đường nhanh phỏng vấn</span>'


def hue_map(data):
    hs, order = {}, []
    for p in data:
        for r in p["rows"]:
            if r["C"] not in hs:
                hs[r["C"]] = round((len(order) * 137.508) % 360)
                order.append(r["C"])
    return hs


def row_html(r, les):
    esc = html.escape
    uid = r["uid"]
    pre = " ".join(f'<a href="#{anchor(p)}">{esc(p.replace(":", " "))}</a>' for p in r["pre"])
    pre = f'<span class="pre">Cần học trước: {pre}</span>' if pre else ""
    bd = {"journey": '<span class="bd j">Hành trình</span>', "case": '<span class="bd c">Tình huống chuyên gia</span>'}.get(r["kind"], "")
    code = f'<span class="code">{esc(r["C"])} {esc(r["id"])}</span>'
    if not r["ready"]:
        return (f'<li class="les pend" id="{anchor(uid)}" data-uid="{esc(uid)}"><span class="chk ph" aria-hidden="true"><span class="box"></span></span>'
                f'<div class="main"><div class="ttl t">{code}<span class="name">{esc(r["title"])}</span>{bd}<span class="bd">đang soạn</span></div></div>'
                f'<div class="meta"><span class="no">#{r["n"]}</span><span class="soon">chưa có video</span>{pre}</div></li>')
    obj = "".join(f"<li>{esc(o)}</li>" for o in r["obj"])
    ch = "".join(f"<li>{esc(c)}</li>" for c in r["ch"])
    qq = "".join(f"<p>{esc(x)}</p>" for x in r["q"]) + "".join(f'<img class="fr" loading="lazy" src="{esc(x)}" alt="khung câu hỏi trong video">' for x in r["qf"])
    qa = "".join(f"<p>{esc(x)}</p>" for x in r["a"]) + "".join(f'<img class="fr" loading="lazy" src="{esc(x)}" alt="khung đáp án trong video">' for x in r["af"])
    rec = "".join(f"<li>{esc(x)}</li>" for x in r["rec"])
    pit = "".join(f"<li>{esc(x)}</li>" for x in r["pit"])
    label = f'{r["C"]} {r["id"]}'
    lab_btn = lab_note = lab_box = ""
    if r["lab"]:
        m = LAB_RE.fullmatch(r["lab"])
        cham = f'bash labs/cham.sh {m.group(1)} {m.group(2)} tệp'
        lab_btn = f'<a class="btn lab sm" href="{esc(r["lab"])}/de.md" title="Mở đề lab. Chấm: {esc(cham)}" aria-label="Tự làm (lab) bài {esc(label)}">🧪 Tự làm (lab)</a>'
        lab_note = f'<span class="labnote">Chấm: {esc(cham)}</span>'
        lab_box = (f'<div class="labbox"><b>🧪 Tự làm (lab)</b> — đề: <a href="{esc(r["lab"])}/de.md">{esc(r["lab"])}/de.md</a>. '
                   f'Làm trước ở thư mục tạm của bạn, rồi chấm: <code>{esc(cham)}</code>. Môi trường: <a href="labs/ENV.md">labs/ENV.md</a>.</div>')
    return (
        f'<li class="les" id="{anchor(uid)}" data-uid="{esc(uid)}" data-dur="{int(round(r["dur"]))}" data-pre="{esc(" ".join(r["pre"]))}">'
        f'<label class="chk"><input type="checkbox" data-uid="{esc(uid)}" aria-label="Đã học: {esc(label)} · {esc(r["title"])}"><span class="box" aria-hidden="true"></span></label>'
        f'<div class="main"><div class="ttl t">{code}<span class="name">{esc(r["title"])}</span>{bd}</div></div>'
        f'<div class="acts"><a class="btn pri sm go" href="{esc(r["xem"])}" aria-label="Xem video bài {esc(label)}">▶ Xem</a>{lab_btn}</div>'
        f'<div class="meta"><span class="no">#{r["n"]}</span><span class="dur">{mmss(r["dur"])}</span><span class="due"></span>{lab_note}{pre}</div>'
        f'<details class="more"><summary>Tự kiểm<span class="sr"> và ghi chú bài {esc(label)}</span></summary><div class="body">'
        f'{lab_box}'
        f'<p class="h">Học xong bạn làm được:</p><ul>{obj}</ul>'
        f'<p class="h">Tự kiểm (trả lời ra giấy trước, rồi mới mở đáp án):</p><div class="qq">{qq}</div>'
        f'<details class="ans"><summary>Hiện đáp án</summary><div class="qa">{qa}</div></details>'
        f'<p class="h">Chuỗi logic cần mang theo:</p><ul class="rec">{rec}</ul>'
        f'<p class="h">Lỗi hay gặp:</p><ul>{pit}</ul>'
        f'<p class="h">Mục lục video (phút:giây):</p><ul>{ch}</ul>'
        f'<p class="h">Giải thích lại bằng lời của bạn (lưu trong trình duyệt):</p><div class="note" data-uid="{esc(uid)}"></div>'
        f'<p class="h">Mở theo cách khác:</p><p class="alt"><a href="{esc(r["xem"])}">▶ trang xem bài</a><a href="{esc(r["mp4"])}">tệp video</a><a href="{esc(r["pv"])}">duyệt nhanh từng khung</a></p>'
        f'</div></details></li>')


def f1(x):
    return f"{x:.1f}".replace(".", ",")


def short_name(p):
    return SHORT.get(p["k"]) or re.sub(r"^Chặng \d+ · ", "", p["name"])[:18]


def long_name(p):
    return re.sub(r"^Chặng \d+ · ", "", p["name"])


def page_html(data, seq, jd, les):
    esc = html.escape
    ready = [r for r in seq if r["ready"]]
    tot_h = sum(r["dur"] for r in ready) / 3600
    fast = [r for r in ready if r["stage"] in FAST]
    hue = hue_map(data)
    pend_all = len(seq) - len(ready)
    fn = sorted(int(k[1:]) for k in FAST)
    fast_rng = f"{fn[0]}–{fn[-1]}" if len(fn) > 1 else str(fn[0])

    def cc(C, n=None):
        return f'<span class="cc" style="--h:{hue[C]}">{esc(C)}' + (f"<small>{n}</small>" if n is not None else "") + "</span>"
    chips, strip, tl = [], [], []
    for i, p in enumerate(data, 1):
        k = p["k"]
        rr = [r for r in p["rows"] if r["ready"]]
        pend = len(p["rows"]) - len(rr)
        hrs = sum(r["dur"] for r in rr) / 3600
        by = defaultdict(int)
        for r in p["rows"]:
            by[r["C"]] += 1
        isf = k in FAST
        fc = " fast" if isf else ""
        chips.append(f'<a class="chip" href="#{k}" data-k="{k}" aria-label="Chặng {i}: {esc(short_name(p))}"><b>{i}</b><span>{esc(short_name(p))}</span><i class="cp" data-pct="{k}">0%</i></a>')
        strip.append(f'<a class="seg{fc}" href="#{k}" data-k="{k}" title="Chặng {i}: {esc(long_name(p))}"><i data-bar="{k}"></i><span>{i}</span></a>')
        tl.append(
            f'<li class="{"fast" if isf else ""}" data-k="{k}"><span class="node" aria-hidden="true"><span>{i}</span></span>'
            f'<a class="mcard" href="#{k}"><div class="mt">{esc(long_name(p))}'
            f'{FASTTAG if isf else ""}'
            f'<span class="tag here">Bạn đang ở đây</span><span class="tag fin">Đã xong</span></div>'
            f'<div class="lv">{esc(p["level"])}</div>'
            f'<div class="mm"><span><b>{len(rr)}</b> bài{f" (+{pend} đang soạn)" if pend else ""}</span><span><b>{f1(hrs)}</b> giờ video</span></div>'
            f'<div class="cs">{"".join(cc(C, n) for C, n in by.items())}</div>'
            f'<div class="mp"><span data-prog="{k}">0/{len(rr)}</span><div class="bar"><i data-bar="{k}"></i></div></div></a></li>')
    chips.append('<a class="chip misc" href="#jd"><span>Đối chiếu JD/CV</span></a>')
    chips.append('<a class="chip misc" href="#backup"><span>Sao lưu</span></a>')
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
        jr.append(f'<tr><td>{esc(topic)}</td><td class="need"><span class="pill">{esc(need)}</span></td><td class="refs">{" ".join(cells)}</td></tr>')
    # các chặng
    parts = []
    for i, p in enumerate(data, 1):
        k = p["k"]
        rr = [r for r in p["rows"] if r["ready"]]
        pend = len(p["rows"]) - len(rr)
        groups, cur_g = [], None
        for r in p["rows"]:
            if cur_g is None or cur_g[0] != r["C"]:
                cur_g = (r["C"], [])
                groups.append(cur_g)
            cur_g[1].append(r)
        gh = []
        for gi, (C, grs) in enumerate(groups):
            gr = [r for r in grs if r["ready"]]
            ttl = grs[0]["course"]
            gh.append(
                f'<details class="course" open data-g="{k}-{gi}"><summary><span class="cname">{cc(C)} <span>{esc(ttl) if ttl else ""}</span></span>'
                f'<span class="cprog" data-gprog="{k}-{gi}">0/{len(gr)}</span><span class="bar"><i data-gbar="{k}-{gi}"></i></span><span class="chev"></span></summary>'
                f'<ol class="ls">{"".join(row_html(r, les) for r in grs)}</ol></details>')
        isf = k in FAST
        parts.append(
            f'<section class="stage{" fast" if isf else ""}" id="{k}" data-k="{k}"><details><summary><span class="sn">{i}</span>'
            f'<div class="sh"><h2>{esc(long_name(p))}{FASTTAG if isf else ""}<span class="chev"></span></h2>'
            f'<div class="sm">{len(rr)} bài{f" (+{pend} đang soạn)" if pend else ""} · {f1(sum(r["dur"] for r in rr) / 3600)} giờ video</div>'
            f'<div class="sp"><span class="prog" data-prog="{k}">0/{len(rr)}</span><div class="bar"><i data-bar="{k}"></i></div></div></div></summary>'
            f'<div class="sbody"><p class="lvl">{esc(p["level"])}</p><p class="intro">{esc(p["intro"])}</p>{"".join(gh)}</div></details></section>')
    return f"""<!doctype html>
<html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="color-scheme" content="light dark">
<title>Lộ trình học</title>
<script>{THEME_JS}</script>
<style>{CSS}</style></head>
<body>
<a class="skip" href="#map">Bỏ qua tới bản đồ lộ trình</a>
<header class="hero"><div class="wrap">
<div class="intro">
<span class="eyebrow">Lộ trình tự học</span>
<h1>Từ con số 0 tới senior</h1>
<p class="lead">Từ con số 0 tới năng lực nền của kỹ sư senior: công nghệ thông tin, khoa học máy tính, trí tuệ nhân tạo. Học từng bài video, tự kiểm, ôn đúng hạn.</p>
<p class="facts mute"><span><b>{len(ready)}</b> bài có video{f" (+{pend_all} đang soạn)" if pend_all else ""}</span><span><b>{tot_h:.0f}</b> giờ video</span><span><b>{len(data)}</b> chặng</span><span><b>{sum(1 for r in ready if r.get("lab"))}</b> bài có phần Tự làm (lab chạy được)</span><span><b>{len(fast)}</b> bài ({sum(r["dur"] for r in fast) / 3600:.0f} giờ) là đường nhanh phỏng vấn</span></p>
</div>
<div class="next" id="next" aria-live="polite">
<div class="lbl">Học tiếp</div>
<h2><span class="code" id="nx-code"></span><span id="nx-title"></span></h2>
<p class="sub" id="nx-sub"></p>
<p class="alert" id="nx-warn" hidden></p>
<div class="btns"><a class="btn go" id="nx-go" href="#map">▶ Xem bài</a><a class="btn alt" id="nx-open" href="#map">Mở trong danh sách</a></div>
</div>
<div class="panel">
<div class="ringbox">
<svg class="ring" viewBox="0 0 120 120" role="img" id="ring" aria-label="Tiến độ chung"><circle class="rt" cx="60" cy="60" r="52" fill="none" stroke-width="11"/>
<circle class="ra" id="ring-arc" cx="60" cy="60" r="52" fill="none" stroke-width="11" stroke-linecap="round" stroke-dasharray="326.73" stroke-dashoffset="326.73" transform="rotate(-90 60 60)"/>
<text class="rp" id="ring-pct" x="60" y="63">0%</text><text class="rs" x="60" y="80">số bài đã học</text></svg>
<div class="ringtxt"><span class="mute">Đã học</span><b id="d-done">0</b><span class="mute" id="d-donep"></span></div>
</div>
<div class="tiles">
<div class="tile"><b id="d-hrs">0</b><span>giờ video đã học, trên {tot_h:.0f} giờ</span></div>
<div class="tile"><b id="d-streak">0</b><span>ngày liên tục (có học hoặc ôn)</span></div>
<div class="tile due"><b id="d-due">0</b><span>bài cần ôn hôm nay</span><button class="pri sm" id="b-review" style="margin-top:6px">Ôn ngay</button></div>
</div>
<p class="plan">Mỗi ngày học <input type="number" id="c-min" min="10" max="600" step="10" value="60" aria-label="Số phút video mỗi ngày"> phút video → <span id="d-eta"></span>
<span class="mute">(tính cả thời gian dừng làm bài: mỗi phút video ≈ 2,5 phút học thật — ước lượng, không phải số đo).</span></p>
</div>
</div></header>

<nav class="top" aria-label="Điều hướng lộ trình"><div class="wrap">
<div class="r1"><span class="brand"><i>▶</i> Lộ trình</span>
<div class="sbox">{ICON_SEARCH}<input type="search" id="q" aria-label="Tìm bài" placeholder="Tìm bài: tên khoá, mã, từ khoá (Kafka, bế tắc, JVA L05)"><span class="kbd" aria-hidden="true">/</span></div>
<button class="tdue" id="b-review2" aria-label="Mở ôn hôm nay">Ôn: <span id="d-due2">0</span></button>
<button class="iconbtn" id="b-theme" aria-label="Đổi giao diện sáng hoặc tối" title="Đổi sáng/tối">{ICON_THEME}</button></div>
<div class="chips">{"".join(chips)}</div>
<p class="mute" id="qn" style="font-size:.84rem;padding-bottom:4px" aria-live="polite"></p>
</div></nav>

<main class="wrap">
<section id="review" class="card" aria-label="Ôn hôm nay"><h3>Ôn hôm nay</h3>
<p class="mute">Với mỗi bài: đọc câu hỏi, <b>tự trả lời ra giấy hoặc nói thành tiếng</b>, rồi mới mở đáp án và tự chấm thật lòng.
"Quên" đưa bài về ôn lại ngày mai; "nhớ chắc" giãn lịch ôn ra 1 → 3 → 7 → 14 → 30 → 60 → 120 ngày.</p>
<div id="rlist"></div><p><button id="b-close">Đóng</button></p></section>

<div class="sec" id="map"><h2 class="st">Bản đồ {len(data)} chặng</h2>
<p class="mute">Chặng {fast_rng} là <b>đường nhanh phỏng vấn</b> ({len(fast)} bài, {f1(sum(r["dur"] for r in fast) / 3600)} giờ): đúng đường học tối thiểu của MASTER_INDEX.
Chặng 5 có thể học song song từ ngày đầu. Mỗi bài nằm đúng một chỗ, và máy đã kiểm mọi bài cần học trước đứng trước nó.
Tổng {len(ready)} bài có video ({f1(tot_h)} giờ){f", {pend_all} bài đang soạn" if pend_all else ""}.</p>
<div class="strip" role="group" aria-label="Dải tiến độ theo chặng">{"".join(strip)}</div>
<div class="slegend"><span><i style="background:var(--ok-soft);border-color:var(--ok)"></i>phần đã học</span><span><i style="border-top:3px solid var(--acc)"></i>đường nhanh phỏng vấn</span><span><i style="outline:2px solid var(--acc);outline-offset:-1px"></i>chặng bạn đang ở</span></div>
<ol class="tl">{"".join(tl)}</ol></div>

<div class="sec"><h2 class="st">Cách học để kiến thức thành của bạn</h2>
<ol class="steps">
<li><span class="ic" aria-hidden="true">👀</span><b>Trước bài</b><p>Đọc mục tiêu bài và mục "Cần học trước". Chưa vững bài nào trong đó thì quay lại bài đó trước.</p></li>
<li><span class="ic" aria-hidden="true">▶</span><b>Trong bài</b><p>Bấm <i>▶ Xem</i>. Khi video hỏi, dừng (phím cách), trả lời ra giấy rồi mới xem tiếp. Làm lại bằng tay mọi ví dụ có số; bài có mã thì gõ lại và chạy.</p></li>
<li><span class="ic" aria-hidden="true">✍</span><b>Ngay sau bài</b><p>Mở "Tự kiểm", trả lời không nhìn đáp án; viết "Giải thích lại bằng lời của bạn" như đang dạy người khác. Chỗ nào không viết được là chỗ chưa hiểu.</p></li>
<li><span class="ic" aria-hidden="true">🔁</span><b>Đánh dấu và ôn</b><p>Tick "Đã học" khi tự làm lại được mọi mục tiêu. Trang tự lên lịch ôn: ngày mai, rồi giãn dần. Mỗi ngày bấm <i>Ôn ngay</i> trước khi học bài mới.</p></li>
</ol>
<div class="two">
<div class="card"><b>Hai thói quen giúp nhớ lâu</b>
<ul class="tips"><li><b>Trộn bài khi ôn:</b> hàng "Ôn hôm nay" trộn các khoá khác nhau, nên bạn phải tự nhận ra bài nào cần cách giải nào.</li>
<li><b>Sau mỗi chặng:</b> tự làm một dự án nhỏ dùng kiến thức cả chặng. Ví dụ, sau chặng 2–3, viết một API chuyển khoản có khoá lũy đẳng, sổ cái, Kafka, Redis, OpenAPI, Docker và CI.</li></ul>
<details class="basis"><summary>Cơ sở khoa học và giới hạn</summary><p>Hiệu ứng tự kiểm (Roediger &amp; Karpicke, 2006), ôn ngắt quãng (Cepeda và cộng sự, 2006), tổng quan kỹ thuật học
(Dunlosky và cộng sự, 2013). Các kết quả này đo trên người học nói chung; trên chính bạn thì chưa ai đo (NOT_VERIFIED).</p></details></div>
<div class="card machine"><h3>🧪 Chuẩn bị máy</h3>
<p class="mute" style="font-size:.93rem">Bài có nút <b>🧪 Tự làm (lab)</b> cần môi trường thực hành chuẩn của khoá:</p>
<ul class="reqs"><li>Git Bash</li><li>JDK 21</li><li>Python 3.11+</li><li>sqlite3</li></ul>
<p style="font-size:.93rem">Chi tiết, cách kiểm máy và cách chấm lab: <a href="labs/ENV.md">labs/ENV.md</a>. Kiểm nhanh: <code>bash labs/check_env.sh</code></p></div>
</div></div>

<div class="sec"><h2 class="st">Danh sách bài theo chặng</h2>
<p class="mute">Bấm tên chặng để mở; trong chặng, bài xếp theo khoá và theo thứ tự nên học.</p>
<div class="stagebar"><label><input type="checkbox" id="f-todo"> Ẩn bài đã học</label><button class="sm" id="b-all">Mở hết chặng</button><button class="sm" id="b-none">Thu gọn hết</button></div>
{"".join(parts)}</div>

<details id="jd"><summary>Đối chiếu yêu cầu tuyển dụng (JD) và hồ sơ (CV) với bài học</summary><div class="jdb">
<p class="mute">Nguồn: <code>resources/job/JD.md</code> (tin Software Engineer trên acbjobs.com.vn và các tin Backend, Lead) và <code>resources/job/PHAM-MINH-DUC-SENIOR-INTEGRATION-CV.md</code> (các dòng bắt đầu bằng “CV”). Bấm mã bài để nhảy tới bài.</p>
<table class="jd"><thead><tr><th>Yêu cầu</th><th>Mức</th><th>Bài</th></tr></thead><tbody>{"".join(jr)}</tbody></table></div></details>

<div class="card" id="backup"><h2>Sao lưu tiến độ</h2>
<p class="mute">Dấu đã học, lịch ôn và ghi chú chỉ nằm trong trình duyệt này. Xoá dữ liệu trình duyệt là mất. Hãy <b>xuất tệp mỗi tuần</b>, và nhập lại khi đổi máy hay đổi trình duyệt.</p>
<div class="row"><button class="pri" id="b-exp">Xuất tệp sao lưu</button> <label class="btn">Nhập tệp sao lưu <input type="file" id="f-imp" accept="application/json,.json" hidden></label> <span id="imp-msg" role="status"></span></div></div>
<p class="foot">Trang sinh tự động bằng <code>audit/review/learn_start/pack.py page</code> từ giáo án <code>curriculum/*.yaml</code>, đặc tả bài và video thật trong <code>out/</code>; thứ tự chặng theo
<a href="interview/MASTER_CURRICULUM_INDEX.md">MASTER_CURRICULUM_INDEX.md</a>. Mở bằng trình duyệt, không cần mạng.</p>
</main>
<script>
{JS}
</script>
</body></html>
"""


JS = r"""
(function () {
  var KEY = "hoc_tap_v2", OLD = "hoc_tap_done_v1", IV = [1, 3, 7, 14, 30, 60, 120], CIRC = 326.73;
  var S = { v: 2, L: {}, N: {}, A: {}, cfg: { min: 60 } };
  function $(id) { return document.getElementById(id); }
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
  var rows = Array.prototype.slice.call(document.querySelectorAll("li.les[data-dur]"));
  var byUid = {}; rows.forEach(function (tr) { byUid[tr.dataset.uid] = tr; });
  var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  function label(u) { return u.replace(":", " "); }
  function code(tr) { return tr.querySelector(".code").textContent; }
  function name(tr) { return tr.querySelector(".name").textContent; }
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
  function missing(tr) { return (tr.dataset.pre || "").split(" ").filter(function (p) { return p && byUid[p] && !S.L[p]; }); }
  function setAll(sel, attr, val, fn) { document.querySelectorAll(sel).forEach(function (e) { fn ? fn(e) : e.setAttribute(attr, val); }); }
  var curStage = null;
  function paint() {
    var done = 0, sec = 0, tot = 0, t = today();
    rows.forEach(function (tr) {
      var u = tr.dataset.uid, x = S.L[u], b = tr.querySelector("input[type=checkbox]");
      tot += +tr.dataset.dur;
      b.checked = !!x; tr.classList.toggle("done", !!x);
      var du = tr.querySelector(".due");
      if (x) { done++; sec += +tr.dataset.dur; du.textContent = x.due <= t ? "cần ôn" : "ôn ngày " + x.due.split("-").reverse().join("/"); du.className = "due " + (x.due <= t ? "warn" : ""); }
      else { du.textContent = ""; du.className = "due"; }
    });
    var pct = rows.length ? done / rows.length : 0, nd = dueList().length;
    $("d-done").textContent = done + "/" + rows.length;
    $("d-donep").textContent = rows.length ? Math.round(100 * pct) + "% số bài" : "";
    $("d-hrs").textContent = (sec / 3600).toFixed(1).replace(".", ",");
    $("d-due").textContent = nd; $("d-due2").textContent = nd;
    $("d-due").className = nd ? "hot" : "";
    $("d-streak").textContent = streak();
    $("ring-arc").setAttribute("stroke-dashoffset", (CIRC * (1 - pct)).toFixed(2));
    $("ring-pct").textContent = Math.round(100 * pct) + "%";
    $("ring").setAttribute("aria-label", "Tiến độ chung: đã học " + done + " trên " + rows.length + " bài, " + Math.round(100 * pct) + "%");
    // chặng
    var nx = rows.find(function (tr) { return !S.L[tr.dataset.uid]; });
    curStage = nx ? nx.closest("section.stage").dataset.k : null;
    document.querySelectorAll("section.stage").forEach(function (s) {
      var k = s.dataset.k, rr = s.querySelectorAll("li.les[data-dur]"), n = 0;
      rr.forEach(function (tr) { if (S.L[tr.dataset.uid]) n++; });
      var p = rr.length ? 100 * n / rr.length : 0, fin = rr.length > 0 && n === rr.length, txt = "đã học " + n + "/" + rr.length;
      setAll('[data-prog="' + k + '"]', 0, 0, function (e) { e.textContent = txt; });
      setAll('[data-bar="' + k + '"]', 0, 0, function (e) { e.style.width = p + "%"; if (e.parentNode.classList.contains("bar")) e.parentNode.classList.toggle("full", fin); });
      setAll('[data-pct="' + k + '"]', 0, 0, function (e) { e.textContent = Math.round(p) + "%"; e.parentNode.style.setProperty("--p", p + "%"); e.parentNode.classList.toggle("fin", fin); });
      s.classList.toggle("fin", fin);
      var tli = document.querySelector('.tl li[data-k="' + k + '"]'); if (tli) { tli.classList.toggle("fin", fin); tli.classList.toggle("cur", k === curStage); }
      var sg = document.querySelector('.seg[data-k="' + k + '"]'); if (sg) { sg.classList.toggle("cur", k === curStage); sg.setAttribute("aria-label", "Chặng " + k.slice(1) + ": " + txt); }
    });
    document.querySelectorAll("details.course").forEach(function (g) {
      var id = g.dataset.g, rr = g.querySelectorAll("li.les[data-dur]"), n = 0;
      rr.forEach(function (tr) { if (S.L[tr.dataset.uid]) n++; });
      var gp = g.querySelector('[data-gprog]'), gb = g.querySelector('[data-gbar]');
      if (gp) gp.textContent = "đã học " + n + "/" + rr.length;
      if (gb) { gb.style.width = (rr.length ? 100 * n / rr.length : 0) + "%"; gb.parentNode.classList.toggle("full", rr.length > 0 && n === rr.length); }
    });
    // học tiếp
    var wr = $("nx-warn"), go = $("nx-go"), op = $("nx-open");
    if (nx) {
      var miss = missing(nx), st = nx.closest("section.stage");
      $("nx-code").textContent = code(nx); $("nx-title").textContent = name(nx);
      $("nx-sub").textContent = "Bài " + nx.querySelector(".no").textContent.replace("#", "") + " · " + st.querySelector("h2").firstChild.textContent + " · " + "thời lượng " + nx.querySelector(".dur").textContent;
      go.hidden = false; go.setAttribute("href", nx.querySelector("a.go").getAttribute("href")); go.setAttribute("aria-label", "Xem video bài " + code(nx));
      op.hidden = false; op.setAttribute("href", "#" + nx.id);
      if (miss.length) { wr.hidden = false; wr.innerHTML = "Còn thiếu bài cần học trước: " + miss.map(function (m) { return "<a href='#" + byUid[m].id + "'>" + label(m) + "</a>"; }).join(", ") + ". Nên học những bài này trước."; }
      else wr.hidden = true;
    } else {
      $("nx-code").textContent = ""; $("nx-title").textContent = "Bạn đã đánh dấu học hết mọi bài có video";
      $("nx-sub").textContent = "Hãy giữ nhịp ôn hằng ngày."; go.hidden = true; op.hidden = true; wr.hidden = true;
    }
    var min = +(S.cfg.min || 60), left = tot - sec, days = Math.ceil(left / 60 * 2.5 / min);
    $("c-min").value = min;
    $("d-eta").textContent = left > 0 ? "còn khoảng " + days + " ngày học (≈ " + (days / 30).toFixed(1).replace(".", ",") + " tháng)" : "đã xong";
  }
  document.addEventListener("change", function (e) {
    var b = e.target;
    if (b.type === "checkbox" && b.dataset.uid) {
      var u = b.dataset.uid, tr = byUid[u];
      if (b.checked) {
        var miss = missing(tr);
        if (miss.length && !confirm("Bài này cần học trước: " + miss.map(label).join(", ") + ".\nCác bài đó chưa đánh dấu đã học. Vẫn đánh dấu bài này?")) { b.checked = false; return; }
      }
      learn(u, b.checked);
    } else if (b.id === "c-min") { S.cfg.min = Math.max(10, Math.min(600, +b.value || 60)); save(); paint(); }
    else if (b.id === "f-todo") applyFilter();
  });
  document.addEventListener("toggle", function (e) {   // ô ghi chú chỉ tạo khi mở, đỡ nặng trang
    var d = e.target; if (!d.classList || !d.classList.contains("more") || !d.open) return;
    var box = d.querySelector(".note"); if (!box || box.firstChild) return;
    var ta = document.createElement("textarea"), u = box.dataset.uid;
    ta.setAttribute("aria-label", "Giải thích lại bằng lời của bạn");
    ta.placeholder = "Viết như đang giảng cho một người chưa học: bài này giải quyết vấn đề gì, cơ chế ra sao, ví dụ số nào, lỗi nào hay gặp."; ta.value = S.N[u] || "";
    ta.addEventListener("input", function () { if (ta.value.trim()) S.N[u] = ta.value; else delete S.N[u]; save(); });
    box.appendChild(ta);
  }, true);
  function showReview() {
    var R = $("review"), list = $("rlist"), du = dueList();
    list.innerHTML = "";
    if (!du.length) list.innerHTML = "<p class='ok'>Hôm nay không có bài nào đến hạn ôn. Học bài mới, hoặc tự chọn một bài cũ để ôn.</p>";
    du.slice(0, 30).forEach(function (u) {
      var tr = byUid[u], c = document.createElement("div"); c.className = "rcard";
      var q = tr.querySelector(".qq"), a = tr.querySelector(".qa"), rc = tr.querySelector(".rec");
      c.innerHTML = "<b>" + code(tr) + "</b> · " + name(tr)
        + " <span class='mute'>(hộp " + S.L[u].b + ", đã ôn " + (S.L[u].r || 0) + " lần)</span>"
        + "<div class='qq'>" + (q ? q.innerHTML : "") + "</div><details class='ans'><summary>Hiện đáp án và chuỗi logic</summary>"
        + (a ? a.innerHTML : "") + "<p class='h'>Chuỗi logic:</p><ul>" + (rc ? rc.innerHTML : "") + "</ul></details>"
        + "<div class='btns'><button data-g='0'>Quên — ôn lại ngày mai</button><button data-g='1'>Nhớ lơ mơ</button><button class='pri' data-g='2'>Nhớ chắc</button>"
        + " <a class='btn' href='#" + tr.id + "'>Mở bài</a></div>";
      c.querySelectorAll("button[data-g]").forEach(function (bt) { bt.addEventListener("click", function () { grade(u, +bt.dataset.g); c.remove(); if (!list.children.length) showReview(); }); });
      list.appendChild(c);
    });
    if (du.length > 30) list.insertAdjacentHTML("beforeend", "<p class='mute'>Còn " + (du.length - 30) + " bài đến hạn; ôn xong 30 bài này rồi mở lại.</p>");
    R.classList.add("on"); R.scrollIntoView({ behavior: reduce ? "auto" : "smooth" });
  }
  $("b-review").addEventListener("click", showReview);
  $("b-review2").addEventListener("click", showReview);
  $("b-close").addEventListener("click", function () { $("review").classList.remove("on"); });
  // tìm bài + lọc (bỏ dấu để gõ "ket thuc" vẫn ra "kết thúc")
  function fold(s) { return s.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/đ/g, "d"); }
  var all = Array.prototype.slice.call(document.querySelectorAll("li.les"));
  var hay = all.map(function (li) { return fold(li.querySelector(".ttl").textContent + " " + (li.dataset.uid || "").replace(":", " ")); });
  function applyFilter() {
    var v = fold($("q").value.trim()), hideDone = $("f-todo").checked, n = 0, hid = 0;
    all.forEach(function (li, i) {
      var ok = (!v || hay[i].indexOf(v) >= 0), dn = li.classList.contains("done");
      if (ok && hideDone && dn) { ok = false; hid++; }
      li.classList.toggle("hide", !ok); if (ok) n++;
    });
    var on = v || hideDone;
    document.querySelectorAll("details.course").forEach(function (g) {
      var vis = g.querySelectorAll("li.les:not(.hide)").length;
      g.hidden = !!on && !vis; if (v && vis) g.open = true;
    });
    document.querySelectorAll("section.stage").forEach(function (s) {
      var vis = s.querySelectorAll("li.les:not(.hide)").length;
      s.hidden = !!on && !vis; if (v && vis) s.querySelector("details").open = true;
    });
    $("qn").textContent = v ? n + " bài khớp" + (hideDone ? " (đang ẩn bài đã học)" : "") : (hideDone ? "Đang ẩn " + hid + " bài đã học" : "");
  }
  $("q").addEventListener("input", applyFilter);
  $("q").addEventListener("keydown", function (e) { if (e.key === "Escape") { this.value = ""; applyFilter(); this.blur(); } });
  document.addEventListener("keydown", function (e) {
    if (e.key === "/" && !/^(INPUT|TEXTAREA|SELECT)$/.test(document.activeElement.tagName)) { e.preventDefault(); $("q").focus(); }
  });
  var origPaint = paint; paint = function () { origPaint(); applyFilter(); };
  $("b-all").addEventListener("click", function () { document.querySelectorAll("section.stage > details").forEach(function (d) { d.open = true; }); });
  $("b-none").addEventListener("click", function () { document.querySelectorAll("section.stage > details").forEach(function (d) { d.open = false; }); });
  // sáng/tối
  function effTheme() { return document.documentElement.getAttribute("data-theme") || (matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light"); }
  $("b-theme").addEventListener("click", function () {
    var t = effTheme() === "dark" ? "light" : "dark"; document.documentElement.setAttribute("data-theme", t);
    try { localStorage.setItem("hoc_tap_theme", t); } catch (e) {}
  });
  $("b-exp").addEventListener("click", function () {
    var blob = new Blob([JSON.stringify(S, null, 1)], { type: "application/json" }), a = document.createElement("a");
    a.href = URL.createObjectURL(blob); a.download = "hoc_tap_tien_do_" + today() + ".json"; document.body.appendChild(a); a.click(); a.remove();
  });
  $("f-imp").addEventListener("change", function () {
    var f = this.files[0], msg = $("imp-msg"); if (!f) return;
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
  // nhảy tới chặng/bài: mở mọi hộp bao quanh
  function reveal(el) {
    if (el.tagName === "DETAILS") el.open = true;
    if (el.matches && el.matches("section.stage")) el.querySelector("details").open = true;
    for (var d = el.parentElement; d; d = d.parentElement) { if (d.tagName === "DETAILS") d.open = true; if (d.hidden) d.hidden = false; }
    if (el.classList.contains("hide")) el.classList.remove("hide");
  }
  function jump() {
    if (!location.hash || location.hash.length < 2) return;
    var t; try { t = document.querySelector(location.hash); } catch (e) { return; }
    if (t) { reveal(t); t.scrollIntoView(); }
  }
  document.querySelectorAll("a.chip, a.seg, a.mcard").forEach(function (a) {
    a.addEventListener("click", function () { var t = document.getElementById(a.getAttribute("href").slice(1)); if (t) reveal(t); });
  });
  // chip đang xem (scrollspy nhẹ)
  var chips = Array.prototype.slice.call(document.querySelectorAll("a.chip[data-k]")), secs = Array.prototype.slice.call(document.querySelectorAll("section.stage")), tick = false;
  function spy() {
    tick = false; var cur = null, y = (document.querySelector(".top").offsetHeight || 90) + 24;
    secs.forEach(function (s) { if (!s.hidden && s.getBoundingClientRect().top <= y) cur = s.dataset.k; });
    chips.forEach(function (c) { var on = c.dataset.k === cur; c.classList.toggle("on", on); if (on) c.setAttribute("aria-current", "true"); else c.removeAttribute("aria-current"); });
    var on = document.querySelector("a.chip.on"); if (on && on.offsetParent) { var ch = on.parentNode; if (on.offsetLeft < ch.scrollLeft || on.offsetLeft + on.offsetWidth > ch.scrollLeft + ch.clientWidth) ch.scrollLeft = on.offsetLeft - 40; }
  }
  window.addEventListener("scroll", function () { if (!tick) { tick = true; requestAnimationFrame(spy); } }, { passive: true });
  function navh() { var n = document.querySelector(".top"); if (n) document.documentElement.style.setProperty("--nav-h", n.offsetHeight + "px"); }
  window.addEventListener("resize", navh);
  load(); paint(); navh();
  if (location.hash && location.hash.length > 1) jump();
  else if (curStage) { var cs = document.getElementById(curStage); cs.querySelector("details").open = true; }
  spy();
  window.addEventListener("hashchange", jump);
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
    DEV = "--dev" in sys.argv                    # --dev: chỉ ghi HOC_TAP.dev.html, không đụng HOC_TAP.md và xem.html
    OUT = "HOC_TAP.dev.html" if DEV else "HOC_TAP.html"
    (ROOT / OUT).write_text(h, encoding="utf-8")
    md = page_md(data, seq)
    if not DEV:
        (ROOT / "HOC_TAP.md").write_text(md, encoding="utf-8")
    ready = [r for r in seq if r["ready"]]
    wn, wdead, pages = 0, [], []
    for i, r in enumerate(ready):
        w = watch_html(r, ready[i - 1] if i else None, ready[i + 1] if i + 1 < len(ready) else None)
        if not DEV:
            (ROOT / r["xem"]).write_text(w, encoding="utf-8")
        pages.append((r, w, ROOT / r["xem"]))
    for r, w, f in pages:
        c, dd = check_links(w, f.parent)
        wn += c
        wdead += [f"{r['xem']} → {x}" for x in dd]
        wdead += [f"{r['xem']} → HOC_TAP.html#{a}" for a in re.findall(r'HOC_TAP\.html#([^"]+)"', w) if f'id="{a}"' not in h]
    print(f"xem.html{' (không ghi, kiểm trong bộ nhớ)' if DEV else ''}: {len(pages)} trang, {wn} liên kết, chết {len(wdead)}")
    n, dead = check_links(h)
    adead = check_anchors(h)
    dead += wdead + [f"#{a}" for a in adead]
    mdl = re.findall(r"\]\(([^)#]+)\)", md)
    mdead = [x for x in mdl if not (ROOT / x).exists()]
    nq = sum(1 for r in ready if r["q"] and r["a"])
    nf = sum(1 for r in ready if r["qf"] and r["af"])
    nl = sum(1 for r in ready if r["lab"])
    na = len(re.findall(r'href="#', h))
    print(f"{OUT}: {len(seq)} bài ({len(ready)} có video, {len(seq) - len(ready)} đang soạn), {n} liên kết tệp, "
          f"{na} liên kết neo, chết {len(dead)}; tự kiểm đủ câu+đáp án {nq}/{len(ready)}, có khung hình {nf}/{len(ready)}; có lab {nl}; "
          f"{len(h.encode('utf-8')) / 1e6:.2f} MB; HOC_TAP.md: {len(mdl)} liên kết, chết {len(mdead)}")
    for x in dead + mdead:
        print("  chết:", x)
    return 1 if dead or mdead or nq < len(ready) else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["list", "check", "preview", "page"])
    ap.add_argument("--decode", action="store_true")
    ap.add_argument("--dev", action="store_true", help="page: ghi HOC_TAP.dev.html, không đụng HOC_TAP.md/xem.html")
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
