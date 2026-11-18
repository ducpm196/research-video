import lib2
from lib2 import *
from libj import jstep
from l16 import _spoken  # ghép câu quá ngắn vào câu bên cạnh, giữ focus
from labkit import write_lab, practice_steps, practice_scene

lib2.begin("L32")

# ── Mã chạy THẬT: Python 3 + git thật (vòng đối chiếu kiểu GitOps, trạng thái "cụm" là từ điển trong bộ nhớ: MÔ PHỎNG, không chạy Argo CD hay Kubernetes);
#    kho bí mật Vault 2.2.2 ở chế độ phát triển bằng ảnh Docker chính thức (ghim băm, `docker run --rm`, tự gỡ); bộ đánh giá chính sách quyền kiểu AWS IAM
#    là MÔ PHỎNG bằng Python (không có tài khoản AWS). Đầu ra tất định (commit chỉ in thông điệp, không in mã băm) — đệm ở audit/bnx/progcache/L32.json. ──
VAULT_IMG = "hashicorp/vault@sha256:dfa48c2fa2b0099ccb47681ec5c4804bf5aec9d6879ecfee07ad4b92a5427ad6"

P_DC = prog("DoiChieu", r'''
import json, os, pathlib, subprocess, tempfile

kho = pathlib.Path(tempfile.mkdtemp())
ENV = dict(os.environ, GIT_AUTHOR_NAME="b", GIT_AUTHOR_EMAIL="b@x",
           GIT_COMMITTER_NAME="b", GIT_COMMITTER_EMAIL="b@x")

def git(*a):
    r = subprocess.run(["git", *a], cwd=kho, env=ENV, text=True,
                       capture_output=True, check=True)
    return r.stdout

def mong_muon():                      # trang thai MONG MUON: doc tu HEAD
    tep = git("ls-tree", "--name-only", "HEAD").split()
    return {t[:-5]: json.loads(git("show", "HEAD:" + t)) for t in tep}

cum, cuoi = {}, None                  # trang thai THAT (gia lap), commit da dong bo

def lech():
    mm = mong_muon()
    return sorted({t for t in mm if cum.get(t) != mm[t]} | (set(cum) - set(mm)))

def dong_bo(tu_chua=False, prune=False):
    global cuoi
    mm, viec = mong_muon(), []
    rev = git("rev-parse", "HEAD").strip()
    moi, cuoi = rev != cuoi, rev
    for ten, ch in mm.items():
        if cum.get(ten) != ch and (moi or tu_chua or ten not in cum):
            viec.append(("sua " if ten in cum else "tao ") + ten)
            cum[ten] = dict(ch)
    for ten in sorted(set(cum) - set(mm)):
        if prune:
            viec.append("xoa " + ten)
            del cum[ten]
    return viec

def ghi(ten, noi_dung, thong_diep):
    (kho / (ten + ".json")).write_text(json.dumps(noi_dung, sort_keys=True))
    git("add", "-A")
    git("commit", "-q", "-m", thong_diep)

def buoc(i, mo_ta, **kw):
    viec = dong_bo(**kw)
    print(f"{i}. {mo_ta}: {', '.join(viec) or 'khong viec'} | lech {len(lech())}")

git("init", "-q")
ghi("thanh-toan", {"anh": "v1.4", "ban": 3}, "them thanh-toan")
ghi("so-cai", {"anh": "v2.0", "ban": 2}, "them so-cai")
buoc(1, "commit 1-2")
buoc(2, "khong doi gi")
cum["thanh-toan"]["ban"] = 9
buoc(3, "sua tay ban 3 -> 9")
buoc(4, "bat tu chua", tu_chua=True)
ghi("thanh-toan", {"anh": "v1.5", "ban": 3}, "thanh-toan v1.5")
buoc(5, "commit anh v1.5")
git("revert", "--no-edit", "HEAD")
buoc(6, "git revert")
git("rm", "-q", "so-cai.json")
git("commit", "-q", "-m", "go so-cai")
buoc(7, "xoa so-cai.json trong Git")
buoc(8, "bat prune", prune=True)
for dong in git("log", "--reverse", "--name-status", "--format=%s").split("\n"):
    if dong:
        print(dong.replace("\t", " "))
''', lang="python", timeout=120, claims=["vòng đối chiếu GitOps mô phỏng với git thật: commit đầu tạo 2 dịch vụ; sửa tay không tự chữa khi tắt cờ (lệch 1), bật cờ thì chữa; revert đưa ảnh về bản cũ; xoá tệp trong Git chỉ thành lệch 1 nếu chưa bật prune, bật prune thì xoá"])

P_QM = prog("QuyMo", r'''
import json, pathlib, subprocess, tempfile

dem = 0

def git(kho, *a, vao=None):
    global dem
    dem += 1
    return subprocess.run(["git", *a], cwd=kho, input=vao, text=True,
                          capture_output=True, check=True).stdout

def tao_kho(n):
    kho = pathlib.Path(tempfile.mkdtemp())
    git(kho, "init", "-q")
    for i in range(n):
        (kho / f"u{i}.json").write_text(json.dumps({"ban": 3}))
    git(kho, "add", "-A")
    git(kho, "-c", "user.name=b", "-c", "user.email=b@x", "commit", "-q", "-m", "m")
    return kho

def doc_tung_tep(kho):                       # 1 + n lan goi git
    tep = git(kho, "ls-tree", "--name-only", "HEAD").split()
    return {t: json.loads(git(kho, "show", "HEAD:" + t)) for t in tep}

def doc_mot_lan(kho):                        # 2 lan goi git
    tep = git(kho, "ls-tree", "--name-only", "HEAD").split()
    ra = git(kho, "cat-file", "--batch", vao="".join(f"HEAD:{t}\n" for t in tep))
    dong = ra.split("\n")
    return {t: json.loads(dong[2 * i + 1]) for i, t in enumerate(tep)}

for n in (10, 200):
    kho = tao_kho(n)
    dem = 0
    a = doc_tung_tep(kho)
    lan_a, dem = dem, 0
    b = doc_mot_lan(kho)
    print(n, "ung dung: tung tep", lan_a, "lan goi git, mot lan", dem,
          "| giong nhau:", a == b)
''', lang="python", timeout=300, claims=["đọc trạng thái mong muốn từng tệp tốn 1 + n lần gọi git (11 ở 10 ứng dụng, 201 ở 200); đọc một lần bằng cat-file --batch luôn 2 lần; kết quả giống nhau"])

P_IAM = prog("ChinhSach", r'''
import fnmatch

CHINH_SACH = [
    {"hieu_luc": "Allow", "viec": "s3:Get*", "tai_nguyen": "bao-cao/*"},
    {"hieu_luc": "Deny", "viec": "s3:*", "tai_nguyen": "bao-cao/rieng/*"},
]

def quyet_dinh(viec, tai_nguyen):
    khop = [c["hieu_luc"] for c in CHINH_SACH
            if fnmatch.fnmatch(viec, c["viec"])
            and fnmatch.fnmatch(tai_nguyen, c["tai_nguyen"])]
    if "Deny" in khop:
        return "tu choi (Deny ro rang)"
    if "Allow" in khop:
        return "cho phep"
    return "tu choi (mac dinh)"

for v, t in [("s3:GetObject", "bao-cao/2026/a.csv"),
             ("s3:PutObject", "bao-cao/2026/a.csv"),
             ("s3:GetObject", "bao-cao/rieng/b.csv")]:
    print(v, t, "->", quyet_dinh(v, t))
''', lang="python", claims=["mô phỏng đánh giá chính sách quyền: Allow khớp thì cho phép; không có Allow thì từ chối mặc định; Deny rõ ràng thắng Allow"])

SH_VAULT = prog("ChayVault", r'''
IMG=''' + VAULT_IMG + r'''
command -v docker >/dev/null || { echo "NOT_VERIFIED: thieu docker" >&2; exit 97; }
docker image inspect $IMG >/dev/null 2>&1 || docker pull -q $IMG >/dev/null 2>&1 || { echo "NOT_VERIFIED: khong co anh Vault" >&2; exit 97; }
cat > in.sh <<'EOF'
export VAULT_ADDR=http://127.0.0.1:8200 VAULT_TOKEN=root
vault server -dev -dev-root-token-id=root >/dev/null 2>&1 &
for i in $(seq 1 30); do vault status >/dev/null 2>&1 && break; sleep 1; done
vault kv put -mount=secret thanh-toan db_pass=abc123 >/dev/null
vault kv put -mount=secret thanh-toan db_pass=xyz789 >/dev/null
echo "ban moi nhat: $(vault kv get -mount=secret -field=db_pass thanh-toan)"
echo "ban 1: $(vault kv get -mount=secret -version=1 -field=db_pass thanh-toan)"
vault policy write chi-doc - >/dev/null <<'P'
path "secret/data/thanh-toan" { capabilities = ["read"] }
P
T=$(vault token create -policy=chi-doc -ttl=4s -field=token)
doc() {
  VAULT_TOKEN=$T vault kv get -mount=secret -field=db_pass \
    thanh-toan 2>&1
}
ghi() {
  VAULT_TOKEN=$T vault kv put -mount=secret thanh-toan \
    db_pass=x 2>&1 | grep -o 'permission denied' | head -1
}
echo "the doc luc 0 giay: $(doc | head -1)"
echo "the ghi luc 0 giay: $(ghi)"
sleep 6
echo "the doc sau 6 giay: $(doc | grep -o 'permission denied' | head -1)"
EOF
tar cf - in.sh | docker run --rm -i --entrypoint sh $IMG -c 'cd /tmp && tar x && sh in.sh'
''', lang="bash", timeout=300,
    claims=["Vault 2.2.2 dev: ghi hai phiên bản, đọc bản mới xyz789 và bản 1 abc123; thẻ chính sách chỉ đọc có hạn 4 giây: đọc được lúc đầu, ghi bị từ chối, sau 6 giây đọc cũng bị từ chối"])

# Application của Argo CD: YAML đọc thật bằng PyYAML khi sinh sổ; trường theo hướng dẫn chính thức (sources_l32.md [ARGOSPEC]); không chạy Argo CD (cần Kubernetes)
YAML_ARGO = r'''
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata: {name: thanh-toan, namespace: argocd}
spec:
  project: default
  source:
    repoURL: https://git.example/bnx.git
    targetRevision: HEAD
    path: manifests
  destination: {server: "https://kubernetes.default.svc", namespace: bnx}
  syncPolicy:
    automated: {prune: true, selfHeal: true}
'''.strip("\n")
lib2.other("apiVersion: argoproj.io/v1alpha1", kind="other", lang="yaml",
           reason="Application của Argo CD: khai nguồn Git, đích là cụm, và chính sách đồng bộ tự động với hai công tắc prune, selfHeal.",
           read_check="Phân tích được bằng YAML (PyYAML safe_load, kiểm khi sinh bài và trong ver/l32.py); tên trường (spec.source.repoURL, targetRevision, path, destination, syncPolicy.automated.prune/selfHeal) "
                      "theo hướng dẫn Argo CD (audit/bnx/sources_l32.md, [ARGOSPEC]); URL kho là giả (git.example); KHÔNG chạy Argo CD: cần cụm Kubernetes.")

# ── Lab (cham.sh, Python): vòng đối chiếu nhỏ với cờ prune ──
LAB_PY = r'''
MONG_MUON = {"a": 2, "b": 1}
THAT = {"a": 5, "c": 1}


def lech():
    return sorted({t for t in MONG_MUON if THAT.get(t) != MONG_MUON[t]} | (set(THAT) - set(MONG_MUON)))


def dong_bo(prune):
    viec = []
    for ten, ban in MONG_MUON.items():
        if THAT.get(ten) != ban:
            viec.append(("sua " if ten in THAT else "tao ") + ten)
            THAT[ten] = ban
    if prune:
        for ten in sorted(set(THAT) - set(MONG_MUON)):
            viec.append("xoa " + ten)
            del THAT[ten]
    return viec


def hien(ds):
    return ", ".join(ds) or "-"


print("lech:", hien(lech()))
print("dong bo (khong prune):", hien(dong_bo(False)), "| lech:", hien(lech()))
print("dong bo (prune):", hien(dong_bo(True)), "| lech:", hien(lech()))
'''
LAB_OUT = """lech: a, b, c
dong bo (khong prune): sua a, tao b | lech: c
dong bo (prune): xoa c | lech: -"""
LAB_DE = """# Lab BNX L32 — Vòng đối chiếu nhỏ: sửa lệch, tạo thiếu, xoá thừa

Trạng thái **mong muốn** (như trong Git, số minh hoạ): `a` có 2 bản sao, `b` có 1. Trạng thái **thật** của cụm (từ điển): `a` có 5 bản sao, `c` có 1 (`c` không còn trong Git).
Số bản sao là giá trị của từng tên: `MONG_MUON = {"a": 2, "b": 1}`, `THAT = {"a": 5, "c": 1}`.

Viết `mau.py`:
1. Hàm `lech()` trả danh sách tên (sắp theo chữ cái) mà trạng thái thật khác mong muốn hoặc chỉ có ở một bên. In `lech: <các tên, cách nhau ", ">` (rỗng thì in `-`).
2. Hàm `dong_bo(prune)`: với mỗi tên trong mong muốn mà thật khác: ghi `sua <tên>` nếu đã có trong thật, `tao <tên>` nếu chưa có, rồi chỉnh trạng thái thật cho khớp. Tên chỉ có ở thật: chỉ khi `prune` là đúng thì ghi `xoa <tên>` và xoá khỏi trạng thái thật.
3. Gọi `dong_bo(False)` rồi `dong_bo(True)`. In mỗi lần `dong bo (khong prune): <việc> | lech: <các tên>` và `dong bo (prune): <việc> | lech: <các tên>`, việc cách nhau ", " (rỗng thì `-`).

Chạy: `python mau.py`. Chấm: `bash labs/cham.sh BNX L32 mau.py`.
"""


def build():
    write_lab("BNX", "L32", LAB_DE, "py", LAB_PY, LAB_OUT)
    hook = sc("hook", "hook", "Git ghi 3 bản sao, cụm đang chạy 9: ai đúng?", [
        st("""<p>Git ghi dịch vụ thanh toán chạy <b>3 bản sao</b>, nhưng cụm đang chạy <b>9</b> vì ai đó sửa tay lúc 2 giờ sáng. Mật khẩu tĩnh của cơ sở dữ liệu để trong kho mã sống <b>90 ngày = 2 160 giờ</b>; bí mật động do kho bí mật cấp (tự hết hạn) chỉ sống <b>1 giờ</b> (số minh hoạ).</p>
<div class="box key">Ai đúng: Git hay cụm? Và nếu mật khẩu lộ, kẻ xấu dùng được trong bao lâu?</div>""",
           """Chào bạn, kho mã ghi dịch vụ thanh toán chạy ba bản sao, nhưng cụm đang chạy chín vì ai đó sửa tay lúc hai giờ sáng. Mật khẩu tĩnh sống chín mươi ngày, tức hai nghìn một trăm sáu mươi giờ, còn bí mật động chỉ sống một giờ. Ai đúng, và mật khẩu lộ thì dùng được bao lâu?"""),
        st(table(["câu hỏi", "bài này trả lời"],
                 [["ai giữ cho cụm khớp với điều đã khai", "<b>GitOps</b>: trạng thái mong muốn nằm trong Git; công cụ (Argo CD) chạy <b>vòng đối chiếu</b>"],
                  ["tự xoá và tự chữa có nguy hiểm không", "hai công tắc <code>prune</code>, <code>selfHeal</code>: <b>mặc định tắt</b>"],
                  ["bí mật để đâu", "không để trong Git: kho bí mật (Vault) cấp <b>thẻ có hạn</b>, quyền tối thiểu"],
                  ["hạ tầng đám mây tối thiểu", "mạng ảo (VPC), quyền (IAM), kho đối tượng (S3), cơ sở dữ liệu quản lý sẵn (RDS)"]]),
           """Hôm nay ta trả lời bốn câu: ai giữ cụm khớp với kho mã, hai công tắc tự xoá và tự chữa, bí mật để đâu, và hạ tầng đám mây tối thiểu.""",
           clear=True),
    ], checks=["alg.bnx_l32_hours(90) == 2160"])

    pre = sc("prereq", "prereq", "Trước hết: sáu điều cần hiểu", [
        st(table(["khái niệm", "nghĩa", "ví dụ"],
                 [["① mong muốn và thật", "<b>mong muốn</b>: điều ta khai; <b>thật</b>: điều đang chạy; hai thứ có thể lệch nhau", "khai 3 bản sao, đang chạy 9"],
                  ["② Git", "kho ghi từng lần <b>chốt</b> thay đổi; hoàn tác = thêm một lần chốt đảo ngược", "<code>git revert</code>"],
                  ["③ cụm (cluster)", "nhóm máy chạy ứng dụng đóng gói sẵn; ta chỉ khai &laquo;muốn 3 bản sao&raquo;", "Kubernetes"],
                  ["④ vòng đối chiếu", "lặp đi lặp lại: so sánh, rồi sửa cho khớp", "mỗi 3 phút"],
                  ["⑤ bí mật", "mật khẩu, khoá, mã truy cập: lộ là mất quyền", "mật khẩu cơ sở dữ liệu"],
                  ["⑥ quyền tối thiểu", "chỉ cấp đúng điều cần, mặc định là không được", "chỉ đọc một đường dẫn"]]),
           """Trước hết ta cần hiểu sáu điều. Trạng thái mong muốn và trạng thái thật có thể lệch nhau. Kho mã ghi từng lần chốt, còn cụm chạy ứng dụng. Vòng đối chiếu so sánh rồi sửa. Bí mật lộ là mất quyền, nên quyền tối thiểu là chỉ cấp đúng điều cần.""",
           focus=[0, "1.2", "1.3", "1.4", "1.5", "1.6"]),
    ], checks=["alg.bnx_l32_hours(1) == 24"])

    sym = sc("sym", "symbol", "Giải mã các tên trên màn hình", [
        st(table(["tên", "nghĩa"],
                 [["<code>anh</code>, <code>ban</code>", "trong tệp JSON của bài: phiên bản ảnh và số bản sao của một dịch vụ"],
                  ["<code>prune</code>, <code>selfHeal</code>", "tự xoá thứ không còn trong Git; tự sửa thứ bị sửa tay trong cụm"],
                  ["<code>kv put -mount=secret</code>", "ghi một bí mật vào kho bí mật; mỗi lần ghi là một phiên bản"],
                  ["<code>-ttl=4s</code>", "thời gian sống của thẻ: hết 4 giây thì thẻ vô dụng"],
                  ["<code>capabilities = [&quot;read&quot;]</code>", "chính sách chỉ cho phép đọc"],
                  ["<code>Allow</code>, <code>Deny</code>", "cho phép, từ chối; từ chối rõ ràng thắng cho phép"]]),
           """Bảng này giải mã các tên của bài: ảnh và bản sao, hai công tắc, thẻ sống bốn giây, và từ chối rõ ràng thắng cho phép.""",
           focus=[0, "1.2", "1.3", "1.4", "1.5", "1.6", "1.7"]),
    ], checks=["alg.bnx_l32_decide([('Allow', 's3:Get*', 'a/*')], 's3:GetObject', 'a/x') == 'cho phep'"])

    intu = sc("intuition", "intuition", "Hình dung: vòng đối chiếu và hạ tầng tối thiểu", [
        st(svg(1500, 500,
               txt(750, 40, "GitOps: Git là sự thật; vòng đối chiếu kéo cụm về đúng điều Git khai", 26, "middle", "#1f2937", True),
               box(40, 130, 340, 140, ["kho Git", "trạng thái MONG MUỐN", "mỗi lần chốt = một phiên bản"], C_BLUE, 22, True),
               box(570, 130, 360, 140, ["vòng đối chiếu", "đọc Git, đọc cụm", "so sánh, sửa cho khớp"], C_GREEN, 22, True),
               box(1120, 130, 340, 140, ["cụm", "trạng thái THẬT", "(bài này: từ điển mô phỏng)"], C_AMBER, 22, True),
               arrow(575, 175, 385, 175, "#475569", "đọc", 20), arrow(925, 200, 1115, 200, "#16a34a", "đồng bộ", 20), arrow(1115, 245, 925, 245, "#dc2626", "lệch: sửa tay", 20),
               box(40, 330, 1420, 70, "Mặc định chỉ tạo và sửa theo commit mới; tự xoá (prune) và tự chữa (selfHeal) phải bật riêng", C_PURPLE, 22),
               box(40, 420, 1420, 60, "Bài này MÔ PHỎNG vòng đối chiếu bằng Python và git thật; không chạy Argo CD hay Kubernetes", C_GRAY, 22)),
           """Đây là vòng đối chiếu. Kho mã giữ trạng thái mong muốn, mỗi lần chốt là một phiên bản. Vòng đối chiếu đọc kho mã, đọc cụm, so sánh rồi sửa cho khớp. Tự xoá và tự chữa phải bật riêng."""),
        st(svg(1500, 520,
               txt(750, 40, "Hạ tầng tối thiểu của một backend trên đám mây (sơ đồ khái niệm, không chạy trong bài)", 26, "middle", "#1f2937", True),
               panel(40, 80, 940, 330, "VPC: mạng ảo riêng của ta", C_BLUE, 24),
               box(70, 150, 400, 100, ["mạng con công khai", "cổng vào (bộ cân bằng tải)"], C_AMBER, 22, True),
               box(520, 150, 420, 100, ["mạng con riêng", "ứng dụng backend"], C_GREEN, 22, True),
               box(520, 290, 420, 90, ["RDS: cơ sở dữ liệu quản lý sẵn", "chỉ ứng dụng gọi được"], C_PURPLE, 22, True),
               arrow(475, 200, 515, 200, "#475569"), arrow(730, 255, 730, 285, "#475569"),
               box(1140, 100, 320, 110, ["IAM: quyền", "vai trò của ứng dụng;", "mặc định từ chối"], C_RED, 22, True),
               box(1140, 250, 320, 110, ["S3: kho đối tượng", "tệp báo cáo, bản sao lưu"], C_GRAY, 22, True),
               arrow(1135, 160, 945, 190, "#dc2626", "vai trò", 20), arrow(1135, 300, 945, 235, "#475569", "tệp", 20),
               txt(750, 470, "Mỗi khối trả lời một câu hỏi: ai vào được, ai làm được gì, dữ liệu nằm đâu", 24, "middle", "#1f2937", True)),
           """Hình thứ hai là hạ tầng tối thiểu trên đám mây, trong một mạng ảo riêng. Cổng vào là bộ cân bằng tải, tức một cửa chung chia yêu cầu cho nhiều bản sao. Ứng dụng và cơ sở dữ liệu nằm ở mạng con riêng, còn dịch vụ quản lý quyền gắn vai trò cho ứng dụng.""", introduces=["bnx_bo_can_bang_tai"]),
    ], checks=["alg.bnx_l32_decide([], 's3:GetObject', 'a/x') == 'tu choi (mac dinh)'"])

    form = sc("formula", "formula", "Suy ra từng bước: từ Git tới bí mật", [
        st(table(["viết trong mã", "nghĩa", "ví dụ nhỏ"],
                 [["<code>git(\"ls-tree\", \"--name-only\", \"HEAD\")</code>", "chạy lệnh git thật qua hàm <code>git</code> của bài: liệt kê tên các tệp ở lần chốt mới nhất", "<code>so-cai.json</code>, <code>thanh-toan.json</code>"],
                  ["<code>git(\"show\", \"HEAD:\" + t)</code>", "in nội dung tệp <code>t</code> ở lần chốt mới nhất", "<code>{\"anh\": \"v1.4\", \"ban\": 3}</code>"],
                  ["<code>json.loads(…)</code>", "đổi chuỗi chữ viết theo JSON thành từ điển Python để dùng tiếp", "<code>'{&quot;ban&quot;: 3}'</code> thành <code>{'ban': 3}</code>"],
                  ["<code>{t[:-5]: … for t in tep}</code>", "dựng từ điển bằng vòng lặp; <code>t[:-5]</code> bỏ 5 ký tự cuối (<code>.json</code>) để còn tên dịch vụ", "<code>thanh-toan.json</code> thành <code>thanh-toan</code>"]]),
           """Trước hết ta xem bốn cách viết. Lệnh liệt kê cho tên các tệp ở lần chốt mới nhất, rồi lệnh in cho nội dung từng tệp. Hàm đổi chữ biến chuỗi JSON thành từ điển. Tên tệp bỏ năm ký tự cuối nên còn tên dịch vụ.""", clear=True),
        st("""<p><b>Bước 1. Trạng thái mong muốn nằm trong Git.</b> Mỗi dịch vụ là một tệp JSON; trạng thái mong muốn là nội dung các tệp ở lần chốt mới nhất (<code>HEAD</code>). Nên mọi thay đổi có người chốt, có lịch sử và hoàn tác được.</p>"""
           + P_DC.show_from("def mong_muon", 3, title="DoiChieu.py (trích): đọc trạng thái mong muốn từ HEAD"),
           """Bước một là trạng thái mong muốn nằm trong kho mã. Mỗi dịch vụ là một tệp JSON, nên mọi thay đổi có người chốt, có lịch sử, và hoàn tác được.""", clear=True),
        st(table(["viết trong mã", "nghĩa"],
                 [["<code>global cuoi</code>", "cho phép hàm gán lại biến <code>cuoi</code> nằm ngoài hàm; thiếu dòng này, Python tạo biến mới chỉ trong hàm"],
                  ["<code>moi, cuoi = rev != cuoi, rev</code>", "gán hai biến cùng lúc: <code>moi</code> đúng nếu mã chốt đã đổi; rồi nhớ mã chốt hiện tại vào <code>cuoi</code>"]]),
           """Dòng toàn cục cho phép hàm gán lại biến nằm ngoài hàm, nên mã chốt đã gặp được nhớ lại. Phép gán đồng thời cho biết lần chốt này có mới không.""", clear=True),
        jstep([(("<code>for ten, ch in mm.items():</code>", "duyệt từng cặp của từ điển <code>mm</code>: <code>ten</code> là tên dịch vụ, <code>ch</code> là nội dung mong muốn của nó", "Vòng lặp duyệt từng cặp tên và nội dung."), "tên <code>so-cai</code> đi với <code>{&quot;ban&quot;: 2}</code>", ""),
               (("<code>cum.get(ten) != ch and (moi or tu_chua or ten not in cum)</code>", "<code>cum.get(ten)</code>: nội dung thật của <code>ten</code>, chưa có thì ra <code>None</code>; làm khi thật khác mong muốn <b>và</b> một trong ba điều đúng: lần chốt mới, bật tự chữa, tên chưa có trong cụm", "Sửa khi thật khác mong muốn, và có lần chốt mới, hoặc bật tự chữa, hoặc tên chưa có."), "sửa tay <code>ban</code> 9 khi tắt tự chữa: không việc", ""),
               (("<code>(\"sua \" if ten in cum else \"tao \") + ten</code>", "biểu thức điều kiện: chữ <code>sua </code> nếu <code>ten</code> đã có trong cụm, ngược lại <code>tao </code>; <code>+ ten</code> nối tên vào sau", "Chọn chữ sửa nếu tên đã có, ngược lại chữ tạo."), "ra <code>tao so-cai</code> hoặc <code>sua so-cai</code>", ""),
               (("<code>viec.append(…)</code>, <code>dict(ch)</code>", "<code>append</code>: thêm vào cuối danh sách <code>viec</code>; <code>dict(ch)</code>: chép một bản riêng của từ điển <code>ch</code>", "Thêm vào cuối danh sách, và chép bản riêng."), "", "")],
              intro="Hàm đồng bộ có bốn chỗ mới, nên ta giải trước."),
        st("""<p><b>Bước 2. Vòng đối chiếu.</b> Với mỗi dịch vụ: thật khác mong muốn thì <b>sửa</b> hoặc <b>tạo</b> cho khớp. Chỉ làm khi có commit mới, hoặc khi bật <code>tu_chua</code>.</p>"""
           + P_DC.show_from("def dong_bo", 9, title="DoiChieu.py (trích): tạo và sửa cho khớp"),
           """Bước hai là vòng đối chiếu. Dịch vụ nào thật khác mong muốn thì sửa hoặc tạo, nhưng chỉ khi có lần chốt mới hoặc bật tự chữa, nên sửa tay không bị ghi đè lặng lẽ.""", clear=True),
        jstep([(("<code>for ten in sorted(set(cum) - set(mm)):</code>", "<code>set(…)</code>: tập tên không trùng lặp; phép trừ giữ tên có trong cụm mà không có trong mong muốn; <code>sorted</code> xếp theo chữ cái; rồi duyệt từng tên thừa", "Phép trừ giữ tên chỉ có trong cụm, xếp theo chữ cái."), "<code>{a, c}</code> trừ <code>{a, b}</code> còn <code>{c}</code>", ""),
               (("<code>if prune:</code>, <code>del cum[ten]</code>", "<code>if prune:</code>: chỉ chạy các dòng thụt vào khi <code>prune</code> đúng; <code>del cum[ten]</code>: xoá mục <code>ten</code> khỏi từ điển", "Khối chỉ chạy khi cờ đúng, và lệnh xoá bỏ mục khỏi từ điển."), "", "")],
              intro="Bước tiếp có phép trừ tập hợp."),
        st("""<p><b>Bước 3. Xoá thừa.</b>Thứ có trong cụm mà đã biến khỏi Git chỉ bị xoá khi bật <code>prune</code>, vì xoá nhầm là mất dịch vụ thật.</p>"""
           + P_DC.show_from("for ten in sorted", 5, title="DoiChieu.py (trích): xoá thừa chỉ khi bật prune"),
           """Bước ba là xoá thừa. Thứ có trong cụm mà đã biến khỏi kho mã chỉ bị xoá khi bật cờ tự xoá, vì xoá nhầm là mất dịch vụ thật.""", clear=True),
        st(table(["viết trong khai báo", "nghĩa"],
                 [["<code>apiVersion: argoproj.io/v1alpha1</code>, <code>kind: Application</code>, <code>metadata: {name: …}</code>, <code>spec:</code>, <code>project: default</code>", "tệp YAML: <code>apiVersion</code> là loại và bản của đối tượng; <code>kind</code>: một ứng dụng cần giữ đồng bộ với Git; <code>metadata</code>: tên (ngoặc nhọn gom cặp khoá và giá trị trên một dòng); <code>spec</code>: phần khai chi tiết, thụt vào; <code>project: default</code>: nhóm quản lý mặc định của Argo CD"],
                  ["<code>source: repoURL, targetRevision, path</code>", "nguồn: địa chỉ kho Git, lần chốt cần theo (<code>HEAD</code> là mới nhất), thư mục chứa tệp khai báo"],
                  ["<code>destination: server, namespace</code>", "đích: cụm nào và ngăn riêng nào trong cụm"],
                  ["<code>syncPolicy.automated: {prune, selfHeal}</code>", "đồng bộ tự động, kèm hai công tắc tự xoá và tự chữa"]]),
           """Ta đọc khai báo của công cụ đồng bộ. Phần mở đầu là loại đối tượng, tên và nhóm mặc định, còn phần khai chi tiết thụt vào. Nên nguồn là kho mã và lần chốt, đích là cụm cùng ngăn riêng, và có hai công tắc.""", clear=True),
        st(code(YAML_ARGO, title="Bước 3 (tiếp): Application của Argo CD, bật cả hai công tắc ở dòng cuối (mặc định đều tắt; không chạy: cần Kubernetes)"),
           """Theo hướng dẫn chính thức, mặc định công cụ không xoá và không chữa sửa tay, nhưng ở dòng cuối ta bật cả hai công tắc. Tệp này không chạy trên máy vì cần cụm thật.""", clear=True),
        st(table(["viết trong lệnh", "nghĩa"],
                 [["<code>export VAULT_ADDR=… VAULT_TOKEN=root</code>", "đặt biến môi trường cho các lệnh sau: địa chỉ máy chủ và thẻ đăng nhập; <code>root</code> là thẻ gốc của chế độ thử, không dùng thật"],
                  ["<code>vault server -dev -dev-root-token-id=root … &amp;</code>", "chạy máy chủ ở chế độ thử (dữ liệu trong bộ nhớ, tự mở khoá); dấu <code>&amp;</code> cho chạy nền để lệnh sau chạy tiếp"],
                  ["<code>for i in &#36;(seq 1 30); do … sleep 1; done</code>", "lặp tối đa 30 lần, nghỉ 1 giây, cho tới khi máy chủ báo sẵn sàng"],
                  ["<code>… &gt;/dev/null</code>, <code>echo \"ban 1: &#36;(vault kv get …)\"</code>", "<code>&gt;/dev/null</code> vứt chữ lệnh in ra; <code>&#36;(…)</code> chạy lệnh trong ngoặc rồi dán kết quả vào chuỗi"]]),
           """Hai biến môi trường là địa chỉ máy chủ và thẻ gốc của chế độ thử. Lệnh máy chủ kết thúc bằng dấu và nên chạy nền, rồi vòng lặp chờ tối đa ba mươi giây. Dấu lớn hơn vứt chữ đi, còn dấu đô la ngoặc dán kết quả lệnh vào chuỗi.""", clear=True),
        st("""<p><b>Bước 4. Bí mật không nằm trong Git.</b> Kho bí mật giữ bí mật có <b>phiên bản</b>: mỗi lần <code>kv put</code> ghi thêm một bản; <code>-version=1</code> đọc lại bản đầu.</p>"""
           + SH_VAULT.show_from("export VAULT_ADDR", 7, title="Chạy thật: ghi hai phiên bản rồi đọc (Vault 2.2.2, chế độ phát triển)"),
           """Bước bốn là bí mật không nằm trong kho mã. Ta ghi mật khẩu hai lần vào cùng một mục nên có hai phiên bản.
           Lệnh đọc lấy bản mới nhất, còn cờ phiên bản một lấy lại bản đầu.""", clear=True),
        jstep([(("<code>vault policy write chi-doc - &gt;/dev/null &lt;&lt;'P' … P</code>", "ghi chính sách tên <code>chi-doc</code>; dấu <code>-</code> nghĩa là đọc nội dung từ đầu vào chuẩn; <code>&lt;&lt;'P'</code> mở <b>khối chữ dòng-trong-lệnh</b>: mọi dòng tới dòng chỉ có chữ <code>P</code> được đưa vào lệnh nguyên văn", "Dấu gạch nối đọc nội dung từ đầu vào, và hai dấu nhỏ hơn mở khối chữ nhiều dòng."), "", ""),
               (("<code>T=&#36;(vault token create -policy=chi-doc -ttl=4s -field=token)</code>", "tạo thẻ gắn chính sách <code>chi-doc</code>, sống 4 giây; <code>-field=token</code> chỉ in đúng chữ thẻ; <code>T=&#36;(…)</code> cất chữ đó vào biến <code>T</code>", "Tạo thẻ sống bốn giây, chỉ in chữ thẻ, cất vào biến."), "", ""),
               (("<code>VAULT_TOKEN=&#36;T vault kv get …</code>, <code>doc() { … }</code>", "đặt <code>VAULT_TOKEN</code> chỉ cho riêng lệnh này, nên lệnh dùng thẻ <code>&#36;T</code> thay thẻ gốc; <code>doc() { … }</code> đặt tên cho một nhóm lệnh để gọi lại", "Biến đặt trước lệnh chỉ có tác dụng với lệnh đó, nên thẻ riêng thay thẻ gốc, và hàm đặt tên cho nhóm lệnh."), "", ""),
               (("<code>2&gt;&amp;1 | grep -o 'permission denied' | head -1</code>", "<code>2&gt;&amp;1</code> gộp chữ báo lỗi vào dòng chữ thường; <code>grep -o</code> chỉ in đúng đoạn khớp; <code>head -1</code> giữ dòng đầu", "Gộp chữ báo lỗi vào đầu ra, chỉ giữ đoạn khớp."), "", "")],
              intro="Đoạn lệnh sau có bốn cách viết mới."),
        st("""<p>Chính sách <b>mặc định từ chối</b>; thẻ <b>có hạn</b>: hết hạn là vô dụng, nên lộ cũng chỉ trong một lúc. Kho phiên bản 2 chèn <code>data</code> vào đường dẫn: bí mật <code>thanh-toan</code> của kho <code>secret</code> thành <code>secret/data/thanh-toan</code> trong chính sách.</p>"""
           + SH_VAULT.show_from("vault policy write", 8, title="Chạy thật: chính sách chỉ đọc và thẻ sống 4 giây (Vault 2.2.2, chế độ phát triển)"),
           """Chính sách mặc định từ chối, và ta chỉ mở quyền đọc cho đúng một đường dẫn. Kho phiên bản hai chèn thêm một đoạn vào giữa đường dẫn, nên chính sách phải ghi đoạn ấy. Thẻ chỉ sống bốn giây.""", clear=True),
        st("""<p>Hàm <code>ghi</code> thử ghi bằng chính thẻ chỉ đọc; <code>sleep 6</code> nghỉ 6 giây, quá hạn 4 giây của thẻ, rồi đọc lại.</p>"""
           + SH_VAULT.show_from("ghi() {", 8, title="Chạy thật: thử ghi bằng thẻ chỉ đọc, nghỉ 6 giây rồi đọc lại (kết quả ở phần ví dụ)"),
           """Hàm ghi thử ghi bằng chính thẻ chỉ đọc. Lệnh nghỉ sáu giây nên vượt hạn bốn giây của thẻ, rồi đọc lại. Kết quả ở phần ví dụ.""", clear=True),
        jstep([(("<code>{\"hieu_luc\": \"Allow\", \"viec\": \"s3:Get*\", …}</code>, <code>c[\"viec\"]</code>", "danh sách các từ điển, mỗi từ điển là một quy tắc; <code>c[\"viec\"]</code> lấy giá trị của khoá <code>viec</code> trong quy tắc <code>c</code>", "Mỗi quy tắc là một từ điển trong danh sách."), "", ""),
               (("<code>fnmatch.fnmatch(viec, c[\"viec\"])</code>", "<code>import fnmatch</code> nạp thư viện so khớp; hàm cho đúng khi chữ <code>viec</code> khớp mẫu có dấu <code>*</code>", "Hàm cho đúng khi chữ khớp mẫu có dấu sao."), "<code>s3:GetObject</code> khớp <code>s3:Get*</code>", "")],
              intro="Quy tắc quyền có hai cách viết mới."),
        st("""<p><b>Bước 5. Quyền trên đám mây.</b> Mỗi quy tắc gồm hiệu lực (<code>Allow</code>/<code>Deny</code>), việc và tài nguyên. Dấu <code>*</code> khớp mọi ký tự: <code>s3:Get*</code> là mọi việc có tên bắt đầu bằng <code>Get</code> (<code>GetObject</code>…), <b>không</b> gồm <code>s3:ListBucket</code> (liệt kê tên tệp, cần quy tắc riêng); <code>bao-cao/*</code> là mọi tệp trong thư mục.</p>"""
           + P_IAM.show(lines=(3, 6), title="ChinhSach.py (trích): bảng CHINH_SACH, hai quy tắc"),
           """Bước năm là quyền trên đám mây: mỗi quy tắc có hiệu lực, việc và tài nguyên, dấu sao khớp mọi ký tự còn lại. Nên quy tắc đầu cho phép các việc bắt đầu bằng chữ lấy, còn quy tắc hai từ chối mọi việc trong thư mục riêng.""", clear=True),
        jstep([(("<code>def quyet_dinh(viec, tai_nguyen):</code>", "khai hàm có hai tham số; <code>return \"…\"</code> trả chữ kết quả về chỗ gọi", "Hàm có hai tham số, lệnh trả về đưa kết quả về chỗ gọi."), "", ""),
               (("<code>[c[\"hieu_luc\"] for c in CHINH_SACH if … and …]</code>", "danh sách sinh sẵn: lấy hiệu lực của mỗi quy tắc <code>c</code> mà <b>cả hai</b> điều kiện nối bằng <code>and</code> đều đúng", "Danh sách sinh sẵn lấy hiệu lực của quy tắc thoả cả hai điều kiện."), "", ""),
               (("<code>\"Deny\" in khop</code>", "<code>in</code>: đúng khi chữ <code>Deny</code> có trong danh sách <code>khop</code>", "Phép thuộc đúng khi chữ có trong danh sách."), "", "")],
              intro="Hàm quyết định có ba cách viết mới."),
        st("""<p>Hướng dẫn của AWS: mọi yêu cầu bị từ chối ngầm; chỉ <code>Allow</code> mới mở; <b>Deny rõ ràng thắng Allow</b>. Bài mô phỏng đúng quy tắc ấy.</p>"""
           + P_IAM.show_from("def quyet_dinh", 9, title="ChinhSach.py (trích): mô phỏng, không phải AWS thật"),
           """Theo hướng dẫn chính thức, mọi yêu cầu bị từ chối ngầm, chỉ quy tắc cho phép mới mở được, và từ chối rõ ràng thắng cho phép. Đoạn mã mô phỏng đúng quy tắc ấy, không phải dịch vụ thật.""", clear=True),
        st("""<p><b>Bước 6. Cửa sổ lộ.</b> Bí mật tĩnh lộ thì kẻ xấu dùng tới khi ai đó đổi nó. Thẻ truy cập, hay bí mật động do kho tự tạo, có hạn nên dùng tối đa đến hết hạn. <b>Lưu ý:</b> mật khẩu tĩnh nằm trong kho bí mật vẫn sống sau khi thẻ hết hạn; chỉ bí mật động mới tự hết.</p>"""
           + """$$\\text{cửa sổ lộ} \\le \\text{thời gian sống}: \\quad 90 \\times 24 = \\hl{2\\,160} \\text{ giờ} \\;\\text{so với}\\; \\hlg{1} \\text{ giờ}$$""",
           """Bước sáu là cửa sổ lộ: bí mật tĩnh dùng được tới khi có người đổi, còn thẻ hay bí mật động tối đa đến hết hạn. Nên cửa sổ là chín mươi nhân hai mươi bốn, tức hai nghìn một trăm sáu mươi giờ, so với một giờ.""", clear=True),
    ], checks=["alg.bnx_l32_hours(90) == 2160", "alg.bnx_l32_decide([('Allow', 's3:Get*', 'b/*'), ('Deny', 's3:*', 'b/r/*')], 's3:GetObject', 'b/r/x') == 'tu choi (Deny ro rang)'"])

    ex = sc("example", "example", "Ví dụ chạy thật, từng phép tính", [
        jstep([(("<code>cum[\"thanh-toan\"][\"ban\"] = 9</code>", "giả lập người sửa tay: lấy từ điển của <code>thanh-toan</code> trong cụm, đặt khoá <code>ban</code> bằng 9", "Dòng này giả lập sửa tay số bản sao lên chín."), "", ""),
               (("<code>buoc(4, \"bat tu chua\", tu_chua=True)</code>", "gọi hàm <code>buoc</code> (chạy đồng bộ rồi in một dòng); <code>tu_chua=True</code> đặt riêng đối số tên <code>tu_chua</code> là đúng, bỏ ra thì mặc định sai", "Đối số có tên đặt riêng một tham số, bỏ ra thì lấy mặc định."), "", ""),
               (("<code>git(\"revert\", \"--no-edit\", \"HEAD\")</code>", "chốt thêm một lần <b>đảo ngược</b> lần chốt mới nhất; <code>--no-edit</code>: dùng thông điệp có sẵn, khỏi mở trình soạn", "Lệnh hoàn tác chốt thêm một lần đảo ngược lần chốt mới nhất."), "", "")],
              intro="Kịch bản có ba dòng mới."),
        st(P_DC.show_from("git(\"init\"", 12, title="Chạy thật: DoiChieu.py (Python + git thật; cụm là từ điển)"),
           """Ta chạy thật bằng Python và kho mã thật. Hai lần chốt đầu thêm hai dịch vụ, rồi ta gọi vòng đồng bộ sau mỗi sự kiện, còn cụm chỉ là một từ điển.""", clear=True),
        st(P_DC.out_html("""1. commit 1-2: tao so-cai, tao thanh-toan | lech 0
2. khong doi gi: khong viec | lech 0
3. sua tay ban 3 -> 9: khong viec | lech 1""")
           + """$$① \\; \\text{2 dịch vụ mới} \\Rightarrow \\text{tạo 2}; \\; \\text{giống nhau} \\Rightarrow 0; \\quad ② \\; \\text{sửa tay, tắt tự chữa} \\Rightarrow \\text{lệch } 1$$""",
           """Phép tính thứ nhất, hai dịch vụ mới nên tạo hai, rồi cụm giống Git nên không có việc. Phép tính thứ hai, ai đó sửa tay số bản sao từ ba lên chín. Vì tự chữa tắt, vòng đồng bộ chỉ báo lệch một.""", clear=True),
        st(P_DC.out_html("""4. bat tu chua: sua thanh-toan | lech 0
5. commit anh v1.5: sua thanh-toan | lech 0
6. git revert: sua thanh-toan | lech 0""")
           + """$$③ \\; \\text{tự chữa: } ban: 9 \\to 3; \\quad v1.4 \\to v1.5; \\quad \\text{revert: } v1.5 \\to v1.4$$""",
           """Phép tính thứ ba, bật tự chữa thì vòng sau sửa số bản sao từ chín về ba. Lần chốt đổi ảnh sang bản một chấm năm được sửa theo, và hoàn tác đưa ảnh về bản một chấm bốn.""", clear=True),
        st("""<p>Lệnh <code>git rm</code> gỡ tệp khỏi thư mục và khỏi lần chốt sau; <code>-q</code> cho ít chữ. Rồi ta chốt.</p>"""
           + P_DC.show_from("git(\"rm\"", 4, title="Chạy thật: DoiChieu.py (tiếp): xoá tệp trong Git, rồi bật prune"),
           """Lệnh xoá gỡ tệp sổ cái khỏi thư mục và khỏi lần chốt sau, rồi ta chốt.""", clear=True),
        st(P_DC.out_html("""7. xoa so-cai.json trong Git: khong viec | lech 1
8. bat prune: xoa so-cai | lech 0""")
           + """$$\\text{xoá tệp trong Git, tắt prune} \\Rightarrow \\text{dịch vụ vẫn chạy (lệch 1); bật prune} \\Rightarrow \\text{xoá}$$""",
           """Xoá tệp sổ cái khỏi kho mã mà chưa bật tự xoá thì dịch vụ vẫn chạy, chỉ báo lệch một. Bật tự xoá thì vòng sau mới xoá dịch vụ, nên công tắc mặc định tắt.""", clear=True),
        st(SH_VAULT.out_html("""ban moi nhat: xyz789
ban 1: abc123
the doc luc 0 giay: xyz789
the ghi luc 0 giay: permission denied
the doc sau 6 giay: permission denied""", "Chạy thật: Vault 2.2.2 ở chế độ phát triển (ảnh Docker chính thức)")
           + """$$④ \\; \\text{2 phiên bản}; \\quad \\text{thẻ chỉ đọc: đọc được, ghi bị từ chối, sau } 6 > 4 \\text{ giây: bị từ chối}$$""",
           """Phép tính thứ tư là kho bí mật thật. Hai lần ghi thành hai phiên bản, đọc được cả hai. Thẻ chỉ đọc ghi bị từ chối, và sau sáu giây, quá hạn bốn giây, đọc cũng bị từ chối.""", clear=True),
        st(P_IAM.out_html("""s3:GetObject bao-cao/2026/a.csv -> cho phep
s3:PutObject bao-cao/2026/a.csv -> tu choi (mac dinh)
s3:GetObject bao-cao/rieng/b.csv -> tu choi (Deny ro rang)""", "Chạy thật: bộ mô phỏng đánh giá quyền (không phải AWS)")
           + """$$⑤ \\; \\text{có Allow} \\Rightarrow \\text{cho phép}; \\quad \\text{không Allow} \\Rightarrow \\text{từ chối mặc định}; \\quad \\text{Deny} > \\text{Allow}$$""",
           """Phép tính thứ năm là đánh giá quyền. Đọc tệp báo cáo khớp quy tắc cho phép nên được phép. Ghi vào đó không khớp quy tắc nào nên bị từ chối mặc định. Đọc thư mục riêng khớp cả hai, và từ chối thắng.""", clear=True),
    ], checks=["alg.bnx_l32_decide([('Allow', 's3:Get*', 'a/*')], 's3:PutObject', 'a/x') == 'tu choi (mac dinh)'", "alg.bnx_l32_reconcile({'a': 2, 'b': 1}, {'a': 5, 'c': 1}, False)[0] == ['sua a', 'tao b']"])

    chk = sc("check", "check", "Tự kiểm bằng đường khác: lịch sử của chính Git", [
        jstep([(("<code>git(\"log\", \"--reverse\", \"--name-status\", \"--format=%s\")</code>", "in lịch sử: <code>--reverse</code> lần chốt cũ trước, mới sau; <code>--name-status</code> kèm chữ cái (<code>A</code> thêm, <code>M</code> sửa, <code>D</code> xoá) và tên tệp; <code>--format=%s</code> chỉ in dòng thông điệp", "Lệnh xem lịch sử in lần chốt cũ trước, kèm chữ cái thêm, sửa hay xoá và tên tệp."), "", ""),
               (("<code>.split(\"\\n\")</code>, <code>if dong:</code>, <code>dong.replace(\"\\t\", \" \")</code>", "cắt chuỗi thành các dòng; bỏ dòng rỗng; đổi ký tự tab (<code>\\t</code>) thành dấu cách", "Cắt chuỗi thành các dòng, bỏ dòng rỗng, và đổi ký tự nhảy cột thành dấu cách."), "", "")],
              intro="Vòng in lịch sử có hai chỗ mới, nên ta giải trước."),
        st(P_DC.show_from("for dong in git", 3, title="DoiChieu.py (ba dòng cuối): in lịch sử do chính Git ghi"),
           """Đây là ba dòng cuối của chương trình, in lịch sử do chính Git ghi.""", clear=True),
        st(P_DC.out_html("""them thanh-toan
A thanh-toan.json
them so-cai
A so-cai.json
thanh-toan v1.5
M thanh-toan.json
Revert "thanh-toan v1.5"
M thanh-toan.json
go so-cai
D so-cai.json""", "Chạy thật: đầu ra"),
           """Ta kiểm bằng đường khác: lịch sử do chính Git ghi, không qua mã của ta, ghi tệp nào được thêm, sửa hay xoá.""", clear=True),
        st(table(["lần chốt", "Git ghi", "vòng đồng bộ làm"],
                 [["v1.5", "M thanh-toan.json (sửa)", "sua thanh-toan"], ["revert", "M thanh-toan.json", "sua thanh-toan (về v1.4)"], ["go so-cai", "D so-cai.json (xoá)", "xoa so-cai, chỉ khi bật prune"]]),
           """Lần chốt sửa ảnh ghi chữ M và vòng đồng bộ sửa. Lần hoàn tác cũng ghi chữ M nên sửa về bản cũ, còn lần xoá tệp ghi chữ D nên chỉ xoá khi bật tự xoá.""", clear=True),
    ], checks=["alg.bnx_l32_reconcile({'a': 2}, {'a': 2, 'c': 1}, True)[0] == ['xoa c']"])

    quymo = sc("quymo", "example", "Khi hệ thống lớn dần: số lần gọi Git và cửa sổ lộ", [
        st(P_QM.out_html("""10 ung dung: tung tep 11 lan goi git, mot lan 2 | giong nhau: True
200 ung dung: tung tep 201 lan goi git, mot lan 2 | giong nhau: True""", "Chạy thật: đọc trạng thái mong muốn của n ứng dụng")
           + """$$10 \\to 200 \\;(\\times 20): \\; 11 \\to 201 \\text{ lần gọi (từng tệp)}; \\; 2 \\to \\hlg{2} \\text{ lần (đọc một lần)}$$""",
           """Số đo thật khi số ứng dụng tăng hai mươi lần: đọc từng tệp gọi Git một cộng n lần, từ mười một lên hai trăm linh một, còn đọc một lần luôn hai lần. Với mười nghìn ứng dụng, mỗi lần ba mươi mili giây, số minh hoạ, một vòng mất năm phút, dài hơn chu kỳ ba phút.""", clear=True),
        st(table(["cách giữ bí mật", "cửa sổ lộ tối đa", "với 1, 100, 10 000 dịch vụ"],
                 [["mật khẩu tĩnh, đổi mỗi 90 ngày (số minh hoạ)", "90 × 24 = 2 160 giờ", "đổi tay 1, 100, 10 000 mật khẩu mỗi kỳ"],
                  ["bí mật động có hạn 1 giờ (kho bí mật tự cấp)", "1 giờ", "tự hết hạn: không ai phải đổi tay (mật khẩu tĩnh trong kho vẫn phải đổi tay)"]]),
           """Số thứ hai là cửa sổ lộ, số minh hoạ. Mật khẩu tĩnh đổi mỗi chín mươi ngày có cửa sổ hai nghìn một trăm sáu mươi giờ, và mười nghìn dịch vụ là mười nghìn mật khẩu phải đổi tay. Bí mật động có hạn một giờ thì tự hết hạn.""", clear=True),
        st(table(["cách", "được", "mất", "chọn khi"],
                 [["đồng bộ thủ công, bí mật trong cấu hình", "đơn giản, dễ hiểu", "dễ lệch, mật khẩu sống lâu, khó kiểm toán", "một vài dịch vụ, thử nghiệm"],
                  ["đồng bộ tự động, tắt tự xoá và tự chữa", "mọi thay đổi qua Git; xoá nhầm không mất ngay", "sửa tay vẫn lệch, phải tự xử lý", "môi trường thật, mới áp dụng"],
                  ["bật cả tự xoá và tự chữa, thẻ có hạn", "cụm luôn khớp Git; lộ chỉ trong một lúc", "chữa cháy phải qua Git; xoá nhầm tệp là mất dịch vụ", "đã quen quy trình, có kiểm duyệt thay đổi"]]),
           """Bảng này là các lựa chọn của người làm nghề. Đồng bộ thủ công đơn giản nhưng dễ lệch. Đồng bộ tự động với hai công tắc tắt đưa mọi thay đổi qua kho mã, đổi lại sửa tay vẫn lệch. Bật cả hai thì cụm luôn khớp, đổi lại chữa cháy phải qua kho mã.""",
           focus=[0, "1.2", "1.3", "1.4"], clear=True),
    ], checks=["alg.bnx_l32_git_calls(10) == (11, 2) and alg.bnx_l32_git_calls(200) == (201, 2)", "alg.bnx_l32_hours(90) == 2160 and 10000 + 1 == 10001"])

    pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, theo từng giai đoạn của hệ thống", [
        st("""<div class="box warn"><b>Lỗi 1 (người mới).</b> <b class="red">Để mật khẩu trong kho Git</b> rồi xoá ở lần chốt sau. Lịch sử vẫn giữ nó: ai có bản sao kho đều đọc được. Bí mật phải ra khỏi Git, và bí mật đã lộ phải <b>đổi</b>, không chỉ xoá.</div>
$$\\text{xoá tệp} \\ne \\text{xoá lịch sử}$$""",
           """Lỗi thứ nhất là để mật khẩu trong kho mã rồi xoá ở lần chốt sau. Lịch sử vẫn giữ nó, nên bí mật đã lộ phải đổi chứ không chỉ xoá.""", clear=True),
        st("""<div class="box warn"><b>Lỗi 2 (người đã đi làm, lúc mới dựng).</b> Bật <code>prune</code> ngay từ đầu. Một lần xoá nhầm tệp trong Git thành xoá dịch vụ thật (đã thấy ở bước 7–8). Bật sau khi quen quy trình, và bắt buộc có người duyệt thay đổi.</div>
$$\\text{xoá tệp trong Git} + prune \\Rightarrow \\text{xoá dịch vụ thật}$$""",
           """Lỗi thứ hai, lộ ra lúc mới dựng: bật tự xoá ngay từ đầu, nên một lần xoá nhầm tệp thành xoá dịch vụ thật. Hãy bật sau khi quen quy trình, và bắt buộc có người duyệt.""", clear=True),
        st("""<div class="box warn"><b>Lỗi 3 (người đã đi làm, lúc tải tăng).</b> Vòng đối chiếu <b class="red">gọi Git một lần cho mỗi tệp</b>: 10 ứng dụng 11 lần, 200 ứng dụng 201 lần, 10 000 ứng dụng 10 001 lần mỗi vòng. Đọc một lần (<code>cat-file --batch</code>: nhận cả danh sách tên rồi trả nội dung tất cả) luôn 2 lần.</div>
$$1 + n \\;\\text{so với}\\; 2$$""",
           """Lỗi thứ ba, lộ ra khi tải tăng: vòng đối chiếu gọi Git một lần cho mỗi tệp, nên mười nghìn ứng dụng mất mười nghìn lẻ một lần. Đọc cả danh sách tên một lần luôn chỉ hai lần.""", clear=True),
        st("""<div class="box warn"><b>Lỗi 4 (người đã đi làm, lúc vận hành lâu dài).</b> Bật <code>selfHeal</code> rồi <b class="red">chữa cháy bằng sửa tay</b> giữa sự cố: vài phút sau vòng đối chiếu ghi đè lại. Khi bật tự chữa, chữa cháy cũng phải qua Git (hoặc tạm tắt công tắc có ghi lại). Và thẻ, khoá không bao giờ hết hạn thì không có gì tự thu hồi.</div>
<table class='t'><tr><th>việc</th><th>cách làm đúng</th></tr><tr><td>chữa cháy khi tự chữa đang bật</td><td>chốt vào Git hoặc tạm tắt có ghi chép</td></tr></table>""",
           """Lỗi thứ tư, lộ ra khi vận hành lâu dài: bật tự chữa rồi chữa cháy bằng sửa tay, vài phút sau vòng đối chiếu ghi đè lại. Chữa cháy cũng phải qua kho mã.""", clear=True),
    ], checks=["alg.bnx_l32_git_calls(200)[0] == 201 and 10000 + 1 == 10001"])

    quiz = sc("quiz", "quiz", "Đến lượt bạn", [
        st(table(["câu", "đề"],
                 [["1", "Mật khẩu đổi mỗi 30 ngày, so với thẻ sống 15 phút. Cửa sổ lộ tối đa mỗi cách là bao nhiêu giờ, và gấp nhau mấy lần?"],
                  ["2", "Chính sách: Allow <code>s3:Get*</code> trên <code>kho/*</code>; Deny <code>s3:*</code> trên <code>kho/mat/*</code>. Kết quả của (a) GetObject kho/x, (b) PutObject kho/x, (c) GetObject kho/mat/y?"],
                  ["3", "Quyết định (số minh hoạ): môi trường thật, 40 dịch vụ, đội 6 người. Bật ngay <code>prune</code> và <code>selfHeal</code>, hay bật tự chữa trước, tự xoá sau? Vì sao?"]]),
           """Đến lượt bạn. Câu một: mật khẩu đổi mỗi ba mươi ngày so với thẻ sống mười lăm phút, cửa sổ lộ mỗi cách bao nhiêu giờ, gấp mấy lần? Câu hai: ba phép thử trên chính sách cho phép đọc thư mục kho và từ chối mọi việc trong kho mật. Câu ba: bốn mươi dịch vụ, đội sáu người, bật ngay cả hai công tắc hay tự chữa trước? Hãy dừng lại làm ra giấy.""",
           pause=30),
        st("""<p>Câu 1: 30 ngày = 720 giờ; 15 phút = 0,25 giờ.</p>
$$30 \\times 24 = \\hlg{720} \\text{ giờ}; \\quad 15 : 60 = \\hlg{0{,}25} \\text{ giờ}; \\quad 720 : 0{,}25 = \\hl{2\\,880} \\text{ lần}$$""",
           """Đáp án câu một. Ba mươi ngày là bảy trăm hai mươi giờ, mười lăm phút là không phẩy hai mươi lăm giờ, nên mật khẩu gấp hai nghìn tám trăm tám mươi lần."""),
        st("""<p>Câu 2: (a) có Allow khớp, không Deny: <b>cho phép</b>. (b) không Allow nào khớp <code>s3:Put</code>: <b>từ chối mặc định</b>. (c) Allow khớp nhưng Deny cũng khớp: <b>Deny thắng</b>.</p>""",
           """Đáp án câu hai. Đọc kho x được phép vì khớp quy tắc cho phép. Ghi kho x bị từ chối mặc định vì không khớp quy tắc nào. Đọc kho mật y khớp cả hai, và từ chối thắng."""),
        st(table(["lựa chọn", "được", "mất"],
                 [["bật cả hai ngay", "cụm luôn khớp Git", "xoá nhầm một tệp là mất dịch vụ; đội mới quen, chưa có thói quen duyệt"],
                  ["tự chữa trước, tự xoá sau", "sửa tay bị chặn; xoá nhầm chưa gây mất dịch vụ", "thứ thừa tích tụ, phải dọn tay một thời gian"]]),
           """Đáp án câu ba. Bật cả hai ngay làm cụm luôn khớp, nhưng xoá nhầm một tệp là mất dịch vụ thật khi đội còn mới. Bật tự chữa trước chặn được sửa tay mà chưa mất dịch vụ. Hợp lý là cách thứ hai.""",
           focus=[0, "1.2", "1.3"]),
    ], checks=["alg.bnx_l32_hours(30) == 720 and alg.bnx_l32_ratio(720, 0.25) == 2880",
               "alg.bnx_l32_decide([('Allow', 's3:Get*', 'kho/*'), ('Deny', 's3:*', 'kho/mat/*')], 's3:GetObject', 'kho/mat/y') == 'tu choi (Deny ro rang)'"])

    lab_pr = practice_scene(sc, "Tự làm: vòng đối chiếu nhỏ với cờ tự xoá", practice_steps2(
        st, "BNX", "L32",
        """<p><b>Đề</b>: mong muốn <code>{"a": 2, "b": 1}</code>, thật <code>{"a": 5, "c": 1}</code>. Viết <code>lech()</code> và <code>dong_bo(prune)</code>; gọi <code>dong_bo(False)</code> rồi <code>dong_bo(True)</code> và in từng lần việc đã làm cùng danh sách còn lệch.</p>
<p>Định dạng đầu ra chính xác nằm trong <code>de.md</code>; số liệu <b>khác</b> ví dụ trong bài.</p>""",
        """Bây giờ tới phần bạn tự làm. Trạng thái mong muốn có a bằng hai và b bằng một, trạng thái thật có a bằng năm và c bằng một. Viết hàm tìm chỗ lệch và hàm đồng bộ có cờ tự xoá. Hãy dừng video và tự viết.""",
        LAB_OUT, "mau.py",
        """<div class="box key"><b>Nếu kẹt:</b> lệch = tên có ở mong muốn mà khác thật, cộng tên chỉ có ở thật. Sửa nếu đã có trong thật, tạo nếu chưa; xoá chỉ khi cờ bật.
Lời giải đầy đủ ở <code>labs/BNX/L32/loi_giai.py</code> — chỉ mở sau khi bạn đã thử.</div>""",
        """Nếu kẹt, chỗ lệch gồm tên khác nhau giữa hai bên, cộng tên chỉ có ở thật. Sửa nếu đã có, tạo nếu chưa, và chỉ xoá khi cờ bật. Lời giải đầy đủ nằm trong thư mục thực hành.""", pause=180), "BNX", "L32")

    rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        st(chain("mong muốn nằm trong Git", "vòng đối chiếu kéo cụm về khớp", "tự xoá, tự chữa: bật có chủ ý", "bí mật ngoài Git, thẻ có hạn", "quyền tối thiểu, mặc định từ chối"),
           """Trạng thái mong muốn nằm trong kho mã, vòng đối chiếu kéo cụm về khớp, tự xoá và tự chữa chỉ bật có chủ ý. Bí mật nằm ngoài kho mã, quyền thì tối thiểu."""),
        st("""<div class='box key'><b>Tư duy:</b> một nguồn sự thật (Git) cho điều ta <b>muốn</b>, một nơi riêng (kho bí mật) cho điều ta <b>phải giấu</b>, và quyền chỉ mở khi có lý do. Mọi tự động hoá đều có công tắc an toàn; hãy biết công tắc nào đang bật.
Argo CD, Vault, AWS chỉ là công cụ: vòng đối chiếu, thẻ có hạn và mặc định từ chối mới là thứ mang theo.</div>""",
           """Một nguồn sự thật cho điều ta muốn, một nơi riêng cho điều phải giấu, và quyền chỉ mở khi có lý do. Mọi tự động hoá đều có công tắc an toàn, hãy biết công tắc nào đang bật."""),
        st(table(["Nếu bị hỏi về dòng này trên CV", "ý trả lời"],
                 [["GitOps, Argo CD: bạn hiểu thế nào?", "trạng thái mong muốn nằm trong Git; vòng đối chiếu sửa lệch; <code>prune</code>, <code>selfHeal</code> mặc định tắt vì xoá nhầm tệp thành xoá dịch vụ (bài mô phỏng, không chạy Argo CD)"],
                  ["Quản lý bí mật bằng Vault?", "bí mật không để trong Git; phiên bản, chính sách mặc định từ chối, thẻ có hạn (đo: thẻ 4 giây hết hạn thì đọc bị từ chối); cửa sổ lộ của thẻ và bí mật động ≤ thời gian sống, còn mật khẩu tĩnh phải đổi tay"],
                  ["AWS tối thiểu cho backend?", "VPC (mạng con công khai và riêng), IAM (vai trò, mặc định từ chối, Deny thắng Allow), S3, RDS đặt ở mạng riêng; bài chỉ giảng khái niệm"]]),
           """Nếu người phỏng vấn hỏi về dòng này, có ba câu hay gặp. Kho mã: trạng thái mong muốn nằm trong đó, hai công tắc mặc định tắt. Kho bí mật: thẻ có hạn. Đám mây: quyền mặc định từ chối.""",
           focus=[0, "1.2", "1.3", "1.4"], clear=True),
        st("""<p>Bài sau: <b>hệ cũ</b>: Servlet, JSP, Tomcat và JBoss: vòng đời, biên dịch JSP, WAR.</p>""",
           """Ở bài ba mươi ba, ta tìm hiểu hệ cũ: các chương trình web chạy trong máy chủ ứng dụng, vòng đời và cách biên dịch trang.""",
           forward_ref=True),
    ], checks=["alg.bnx_l32_hours(90) == 2160"])
    scenes = _spoken([hook, pre, sym, intu, form, ex, chk, quymo, pit, quiz, lab_pr, rec])
    return lesson("L32", "gitops_bi_mat_aws_toi_thieu",
                  "Bài 32 — GitOps và bí mật: vòng đối chiếu, Argo CD, Vault và AWS tối thiểu",
                  "curriculum/bnx.yaml L32; audit/bnx/verify_bnx.py L32; audit/bnx/sources_l32.md: hướng dẫn Argo CD (How it works, Automated Sync Policy, Application specification), "
                  "Vault (Dev Server, Policies, Tokens, KV v2, Database secrets engine), AWS (IAM policy evaluation logic, IAM, VPC, S3, RDS), đọc 2026-11-14; "
                  "Vault 2.2.2 chạy thật bằng ảnh Docker chính thức; vòng đối chiếu và đánh giá quyền là mô phỏng Python (git thật, không chạy Argo CD hay AWS)",
                  OBJ32,
                  scenes,
                  covers=COV32)


OBJ32 = ["Dựng vòng đối chiếu giữa trạng thái mong muốn trong Git và trạng thái thật rồi đọc việc phải làm sau mỗi lần chốt",
         "Giải thích hai công tắc tự xoá và tự chữa của đồng bộ tự động và vì sao mặc định tắt",
         "Đọc lệnh và kết quả chạy kho bí mật ở chế độ phát triển: ghi hai phiên bản, đọc lại phiên bản cũ và cấp thẻ chỉ đọc có hạn",
         "Đọc kết quả đánh giá chính sách quyền: mặc định từ chối và từ chối rõ ràng thắng cho phép",
         "Đếm số lần gọi Git của vòng đối chiếu đọc từng tệp và đọc một lần ở 10 và 200 ứng dụng",
         "Tính cửa sổ lộ của bí mật tĩnh và của thẻ có hạn",
         "Mô tả vai trò của mạng ảo riêng, quản lý quyền, kho đối tượng và cơ sở dữ liệu quản lý sẵn trong một backend tối thiểu",
         "Viết vòng đối chiếu nhỏ có cờ tự xoá trên số liệu mới"]
COV32 = [(1, "example"), (2, "formula"), (3, "example"), (4, "example"), (5, "quymo"), (6, "quymo"), (7, "intuition"), (8, "practice")]
