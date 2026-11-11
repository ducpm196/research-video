"""Kiểm độc lập BNX L00: chạy git THẬT (thư mục tạm, biến môi trường cố định) rồi so với mô hình Python thuần alg.bnx_* .
Đường khác: (1) chạy nguyên văn các khối bash trên màn hình; (2) Python tự điều khiển git từng lệnh; (3) mô hình đối tượng Git
viết lại bằng hashlib (checklib) — ba đường phải cho cùng mã."""
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "audit" / "bnx" / "src"))
sys.path.insert(0, str(ROOT / "audit" / "bnx"))
sys.path.insert(0, str(ROOT / "tools"))
import checklib as alg  # noqa: E402
import l00  # noqa: E402

ENV = dict(os.environ, GIT_AUTHOR_NAME="An", GIT_AUTHOR_EMAIL="an@vd.vn", GIT_COMMITTER_NAME="An", GIT_COMMITTER_EMAIL="an@vd.vn",
           GIT_AUTHOR_DATE="2026-01-05T09:00:00+07:00", GIT_COMMITTER_DATE="2026-01-05T09:00:00+07:00",
           GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1")


class Repo:
    def __init__(self, d=None, init=True):
        self.d = d or tempfile.mkdtemp(prefix="bnx_l00v_")
        if init:
            self.g("init", "-q", "-b", "main")

    def g(self, *a):
        return subprocess.run(["git", *a], cwd=self.d, env=ENV, capture_output=True, text=True, encoding="utf-8")

    def w(self, name, text):
        with open(os.path.join(self.d, name), "w", encoding="utf-8", newline="\n") as f:
            f.write(text)

    def r(self, name):
        with open(os.path.join(self.d, name), encoding="utf-8") as f:
            return f.read()

    def head(self, rev="HEAD"):
        return self.g("rev-parse", rev).stdout.strip()


def bash(*parts):
    with tempfile.TemporaryDirectory() as d:
        Path(d, "k.sh").write_text("\n".join(p.strip("\n") for p in parts) + "\n", encoding="utf-8", newline="\n")
        p = subprocess.run([shutil.which("bash"), "k.sh"], cwd=d, capture_output=True, text=True, encoding="utf-8")
        return p.returncode, p.stdout, p.stderr


def run(rec):
    if not shutil.which("git") or not shutil.which("bash"):
        rec("L00", None, "thiếu git hoặc bash")
        return
    M = alg.bnx_git_demo()

    # (1) khối bash nguyên văn trên màn hình
    rc, so, se = bash(l00.GIT_INIT, l00.GIT_BRANCH, l00.GIT_RESOLVE)
    lines = so.splitlines()
    rec("L00", rc == 0 and lines[0].split()[0] == M["root"] and alg.bnx_is_hex40(lines[0].split()[0]),
        f"bash nguyên văn: commit gốc {lines[0][:12]}… = Python thuần {M['root'][:12]}…, 40 ký tự thập lục phân")
    rec("L00", "CONFLICT (content): Merge conflict in phi.txt" in so
        and alg.bnx_conflict_file("phi=4400", "phi=6600") in so,
        "bash nguyên văn: gộp báo CONFLICT; tệp sau gộp đúng bằng mô hình (HEAD 4400 ở trên, tang 6600 ở dưới)")
    rec("L00", f"parent {M['giam']}" in so and f"parent {M['tang']}" in so and f"tree {M['tree6600']}" in so
        and lines[-1] == M["blob6600"] and M["merge"][:7] in so,
        "bash nguyên văn: commit gộp có tree/2 parent/blob đúng như Python thuần tính")
    rc2, so2, _ = bash(l00.GIT_INIT, l00.GIT_BRANCH, l00.GIT_RESOLVE, l00.GIT_SECRET)
    tail = so2.splitlines()[-5:]
    rec("L00", rc2 == 0 and tail == ["phi.txt", f"{M['secret_rm'][:7]} Xoá mật khẩu", f"{M['secret_add'][:7]} Thêm cấu hình kết nối",
                                     f"{M['root'][:7]} Phí chuyển khoản 5500", "DB_PASS=MatKhau123"],
        f"bash nguyên văn NỐI TIẾP ví dụ (nhánh thu tách từ {M['root'][:7]}): git show {M['secret_add'][:7]}:.env vẫn trả mật khẩu")

    # (2) Python tự điều khiển git, đếm và đọc lại bằng lệnh khác
    R = Repo()
    R.w("phi.txt", "phi=5500\n"); R.g("add", "."); R.g("commit", "-qm", "Phí chuyển khoản 5500")
    R.g("switch", "-qc", "tang"); R.w("phi.txt", "phi=6600\n"); R.g("commit", "-qam", "Tăng phí lên 6600")
    R.g("switch", "-q", "main"); R.w("phi.txt", "phi=4400\n"); R.g("commit", "-qam", "Giảm phí còn 4400")
    base = R.g("merge-base", "main", "tang").stdout.strip()
    m = R.g("merge", "tang")
    txt = R.r("phi.txt")
    marks = alg.bnx_markers(txt)
    rec("L00", base == M["root"] and m.returncode != 0 and len(marks) == 3 and txt == alg.bnx_conflict_file("phi=4400", "phi=6600"),
        f"git merge-base = commit gốc; gộp thoát {m.returncode}; {len(marks)} dấu mốc")
    R.g("add", "phi.txt")
    plain = R.g("diff", "--check")
    chk = R.g("diff", "--cached", "--check")
    rec("L00", plain.returncode == 0 and plain.stdout == "" and chk.returncode != 0 and "leftover conflict marker" in chk.stdout,
        "sau git add: git diff --check im lặng, git diff --cached --check báo “leftover conflict marker” (Lỗi 1)")
    R.w("phi.txt", "phi=6600\n"); R.g("add", "phi.txt"); R.g("commit", "-qm", "Gộp nhánh tang: chốt 6600")
    par = R.g("rev-list", "--parents", "-n", "1", "HEAD").stdout.split()[1:]
    cnt = int(R.g("rev-list", "--count", "HEAD").stdout)
    blob = R.g("hash-object", "phi.txt").stdout.strip()
    rec("L00", R.head() == M["merge"] and par == [M["giam"], M["tang"]] and len(par) == 2 and cnt == 3 + 1 == 4,
        f"commit gộp {R.head()[:7]} có {len(par)} cha, lịch sử {cnt} commit (đếm bằng rev-list)")
    rec("L00", blob == M["blob6600"] == alg.bnx_git_blob("phi=6600\n") and len("phi=6600\n") == 9,
        "git hash-object = SHA-1 tự tính của 'blob 9\\0phi=6600\\n'")
    h = R.head()
    nbits = sum(4 for _ in h)
    rec("L00", nbits == alg.bnx_hex_bits(40) == 160 and int(h, 16) < 2 ** 160 and sum(int(c, 16) * 16 ** i for i, c in enumerate(reversed("ff"))) == 255,
        "40 ký tự × 4 bit = 160 bit; ff = 255 (cộng từng chữ số)")

    # (3) luật gộp ba chiều: 4 ca của bảng + câu 1 quiz, chạy git thật cho từng ca
    def merge_case(a, b):
        X = Repo()
        X.w("phi.txt", "phi=5500\n"); X.g("add", "."); X.g("commit", "-qm", "goc")
        X.g("switch", "-qc", "tang")
        if b != "5500":
            X.w("phi.txt", f"phi={b}\n"); X.g("commit", "-qam", "b")
        else:
            X.w("khac.txt", "x\n"); X.g("add", "."); X.g("commit", "-qm", "b khac tep")
        X.g("switch", "-q", "main")
        if a != "5500":
            X.w("phi.txt", f"phi={a}\n"); X.g("commit", "-qam", "a")
        r = X.g("merge", "-q", "--no-edit", "tang")
        return ("conflict", None) if r.returncode else ("ok", X.r("phi.txt").strip().split("=")[1])
    cases = [("5500", "6600"), ("4400", "5500"), ("6600", "6600"), ("4400", "6600"), ("7700", "5500")]
    got = [merge_case(a, b) for a, b in cases]
    want = [alg.bnx_merge3("5500", a, b) for a, b in cases]
    rec("L00", got == want, f"luật gộp ba chiều: git thật {got} = mô hình")

    # câu 2 quiz: gộp thêm một nhánh có 2 commit riêng vào lịch sử 4 commit
    R.g("switch", "-qc", "them", M["root"])
    R.w("a.txt", "1\n"); R.g("add", "."); R.g("commit", "-qm", "a1")
    R.w("a.txt", "2\n"); R.g("commit", "-qam", "a2")
    R.g("switch", "-q", "main")
    R.g("merge", "-q", "--no-edit", "them")
    cnt2 = int(R.g("rev-list", "--count", "HEAD").stdout)
    np2 = len(R.g("rev-list", "--parents", "-n", "1", "HEAD").stdout.split()) - 1
    rec("L00", cnt2 == 4 + 2 + 1 == 7 and np2 == 2, f"câu 2: sau gộp {cnt2} commit, commit mới {np2} cha")

    # (4) Lỗi 3: ép đẩy lên nhánh chung làm mất commit đồng nghiệp; --force-with-lease từ chối
    srv = tempfile.mkdtemp(prefix="bnx_l00srv_")
    subprocess.run(["git", "init", "-q", "--bare", "-b", "main", srv], env=ENV, capture_output=True)
    A = Repo()
    A.w("phi.txt", "phi=5500\n"); A.g("add", "."); A.g("commit", "-qm", "goc")
    A.g("remote", "add", "origin", srv); A.g("push", "-q", "origin", "main")
    B = Repo(tempfile.mkdtemp(prefix="bnx_l00b_"), init=False)
    subprocess.run(["git", "clone", "-q", srv, B.d], env=ENV, capture_output=True)
    A.w("phi.txt", "phi=6600\n"); A.g("commit", "-qam", "An"); A.g("push", "-q", "origin", "main")
    an = A.head()
    B.w("phi.txt", "phi=4400\n"); B.g("commit", "-qam", "Binh")
    plain = B.g("push", "-q", "origin", "main")
    lease = B.g("push", "-q", "--force-with-lease", "origin", "main")
    srv_after_lease = subprocess.run(["git", "--git-dir", srv, "rev-parse", "main"], env=ENV, capture_output=True, text=True).stdout.strip()
    B2 = Repo(tempfile.mkdtemp(prefix="bnx_l00b2_"), init=False)
    subprocess.run(["git", "clone", "-q", srv, B2.d], env=ENV, capture_output=True)
    force = B.g("push", "-q", "--force", "origin", "main")
    anc = subprocess.run(["git", "--git-dir", srv, "merge-base", "--is-ancestor", an, "main"], env=ENV, capture_output=True)
    rec("L00", plain.returncode != 0 and lease.returncode != 0 and srv_after_lease == an and force.returncode == 0 and anc.returncode == 1,
        "đẩy thường bị từ chối; --force-with-lease bị từ chối (B chưa thấy commit của An); --force thành công và commit của An mất khỏi main trên máy chủ")
    # --force-with-lease sau khi đã lấy về: không còn bảo vệ
    A.g("fetch", "-q"); A.w("phi.txt", "phi=7700\n"); A.g("commit", "-qam", "An 2"); A.g("push", "-q", "--force", "origin", "main")
    an2 = A.head()
    B2.g("fetch", "-q"); B2.w("phi.txt", "phi=3300\n"); B2.g("commit", "-qam", "Binh 2")
    lease2 = B2.g("push", "-q", "--force-with-lease", "origin", "main")
    anc2 = subprocess.run(["git", "--git-dir", srv, "merge-base", "--is-ancestor", an2, "main"], env=ENV, capture_output=True)
    rec("L00", lease2.returncode == 0 and anc2.returncode == 1,
        "đã git fetch rồi thì --force-with-lease vẫn ghi đè, commit mới của An mất khỏi main (điều kiện ở Lỗi 3)")
    for d in (R.d, A.d, B.d, B2.d, srv):
        shutil.rmtree(d, ignore_errors=True)

    # số trong bài
    rec("L00", (4400 - 5500, 6600 - 5500, 6600 - 4400) == (-1100, 1100, 2200), "hiệu phí: âm 1100, 1100, 2200")
