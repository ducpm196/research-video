"""Kiểm độc lập BNX L32 (GitOps và bí mật). Đường khác với tools/checklib_bnx/l32.py:
- CHẠY LẠI THẬT (không đệm) mọi chương trình trên màn hình: Python + git thật (vòng đối chiếu, số lần gọi git), Vault 2.2.2 ở chế độ phát triển trong ảnh Docker chính thức
  (ghim băm; thẻ 4 giây hết hạn sau 6 giây), đầu ra phải bằng từng ký tự đầu ra đã hiện;
- vòng đối chiếu: dựng lại kịch bản bằng git thật nhưng KHÔNG dùng hàm của bài (tự gọi `git log --name-status` giữa các commit) và so với việc đồng bộ in ra;
- đánh giá quyền: so bộ mô phỏng với alg và với bảng chân trị tự viết; YAML Application đọc bằng PyYAML (trường prune, selfHeal, repoURL…);
- cửa sổ lộ: tính tay; lab chạy lại và so mong_doi.txt.
Thiếu docker / ảnh / git → SKIP (rec None: cổng FAIL, NOT_VERIFIED), không PASS lặng lẽ."""
import os
import shutil
import subprocess
import sys
import tempfile
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "audit" / "bnx"))
sys.path.insert(0, str(ROOT / "audit" / "bnx" / "src"))
import checklib as alg  # noqa: E402
import lib2  # noqa: E402
import l32 as src  # noqa: E402

LAB = ROOT / "labs" / "BNX" / "L32"


def run(rec):
    if not shutil.which("git") or not shutil.which("docker"):
        rec("L32", None, "thiếu git hoặc docker: NOT_VERIFIED")
    else:
        lib2.verify_programs(rec, "L32")
    P = {q.name: q for q in lib2.PROGRAMS if q.lesson == "L32"}
    out = P["DoiChieu"].out.splitlines()
    rec("L32", out[:8] == ["1. commit 1-2: tao so-cai, tao thanh-toan | lech 0", "2. khong doi gi: khong viec | lech 0", "3. sua tay ban 3 -> 9: khong viec | lech 1",
                           "4. bat tu chua: sua thanh-toan | lech 0", "5. commit anh v1.5: sua thanh-toan | lech 0", "6. git revert: sua thanh-toan | lech 0",
                           "7. xoa so-cai.json trong Git: khong viec | lech 1", "8. bat prune: xoa so-cai | lech 0"], "vòng đối chiếu: 8 bước đúng như đã hiện")
    # tham chiếu thuần theo nội dung (alg) cho các bước đổi nội dung
    v, l = alg.bnx_l32_reconcile({"thanh-toan": {"anh": "v1.4", "ban": 3}, "so-cai": {"anh": "v2.0", "ban": 2}}, {}, False)
    rec("L32", v == ["tao thanh-toan", "tao so-cai"] and l == [], "alg: lần đầu tạo hai dịch vụ, hết lệch")
    v, l = alg.bnx_l32_reconcile({"a": 2}, {"a": 2, "c": 1}, False)
    v2, l2 = alg.bnx_l32_reconcile({"a": 2}, {"a": 2, "c": 1}, True)
    rec("L32", (v, l) == ([], ["c"]) and (v2, l2) == (["xoa c"], []), "alg: thừa chỉ bị xoá khi bật prune (lệch 1 rồi 0)")
    # git thật, đường khác: dựng kịch bản bằng git rồi hỏi git log --name-status (không dùng hàm của bài)
    d = Path(tempfile.mkdtemp())
    env = dict(os.environ, GIT_AUTHOR_NAME="v", GIT_AUTHOR_EMAIL="v@x", GIT_COMMITTER_NAME="v", GIT_COMMITTER_EMAIL="v@x")

    def g(*a):
        return subprocess.run(["git", *a], cwd=d, env=env, text=True, capture_output=True, check=True).stdout
    g("init", "-q")
    (d / "thanh-toan.json").write_text('{"anh": "v1.4", "ban": 3}')
    (d / "so-cai.json").write_text('{"anh": "v2.0", "ban": 2}')
    g("add", "-A")
    g("commit", "-q", "-m", "c1")
    (d / "thanh-toan.json").write_text('{"anh": "v1.5", "ban": 3}')
    g("add", "-A")
    g("commit", "-q", "-m", "c2")
    g("revert", "--no-edit", "HEAD")
    g("rm", "-q", "so-cai.json")
    g("commit", "-q", "-m", "c4")
    cac = [x.replace("\t", " ") for x in g("log", "--reverse", "--name-status", "--format=%s").split("\n") if x]
    rec("L32", cac == ["c1", "A so-cai.json", "A thanh-toan.json", "c2", "M thanh-toan.json", 'Revert "c2"', "M thanh-toan.json", "c4", "D so-cai.json"]
        and out[8:] == ["them thanh-toan", "A thanh-toan.json", "them so-cai", "A so-cai.json", "thanh-toan v1.5", "M thanh-toan.json", 'Revert "thanh-toan v1.5"', "M thanh-toan.json", "go so-cai", "D so-cai.json"],
        "git log --name-status: A, M, M (revert), D khớp việc đồng bộ (tạo, sửa, sửa, xoá)")
    # số lần gọi git
    rec("L32", P["QuyMo"].out.splitlines() == ["10 ung dung: tung tep 11 lan goi git, mot lan 2 | giong nhau: True", "200 ung dung: tung tep 201 lan goi git, mot lan 2 | giong nhau: True"]
        and alg.bnx_l32_git_calls(10) == (11, 2) and alg.bnx_l32_git_calls(200) == (201, 2) and 10000 + 1 == 10001, "số lần gọi git: 11 và 201 (từng tệp), luôn 2 (một lần), kết quả giống nhau")
    # Vault thật
    rec("L32", P["ChayVault"].out.splitlines() == ["ban moi nhat: xyz789", "ban 1: abc123", "the doc luc 0 giay: xyz789", "the ghi luc 0 giay: permission denied", "the doc sau 6 giay: permission denied"],
        "Vault 2.2.2 thật: bản mới xyz789, bản 1 abc123; thẻ chỉ đọc 4 giây: đọc được, ghi bị từ chối, sau 6 giây đọc bị từ chối")
    # đánh giá quyền
    CS = [("Allow", "s3:Get*", "bao-cao/*"), ("Deny", "s3:*", "bao-cao/rieng/*")]
    ca = [("s3:GetObject", "bao-cao/2026/a.csv", "cho phep"), ("s3:PutObject", "bao-cao/2026/a.csv", "tu choi (mac dinh)"), ("s3:GetObject", "bao-cao/rieng/b.csv", "tu choi (Deny ro rang)")]
    rec("L32", all(alg.bnx_l32_decide(CS, v_, t) == kq for v_, t, kq in ca) and P["ChinhSach"].out.splitlines() == [f"{v_} {t} -> {kq}" for v_, t, kq in ca],
        "đánh giá quyền: cho phép / từ chối mặc định / Deny thắng Allow (mô phỏng = alg)")
    CK = [("Allow", "s3:Get*", "kho/*"), ("Deny", "s3:*", "kho/mat/*")]
    rec("L32", alg.bnx_l32_decide(CK, "s3:GetObject", "kho/x") == "cho phep" and alg.bnx_l32_decide(CK, "s3:PutObject", "kho/x") == "tu choi (mac dinh)"
        and alg.bnx_l32_decide(CK, "s3:GetObject", "kho/mat/y") == "tu choi (Deny ro rang)", "quiz câu 2: cho phép, từ chối mặc định, Deny thắng")
    # YAML Application
    try:
        import yaml
        y = yaml.safe_load(src.YAML_ARGO)
        ok = (y["kind"] == "Application" and y["spec"]["syncPolicy"]["automated"] == {"prune": True, "selfHeal": True}
              and y["spec"]["source"]["path"] == "manifests" and "repoURL" in y["spec"]["source"])
        rec("L32", ok, "YAML Application đọc được bằng PyYAML: prune và selfHeal đều true, có repoURL và path")
    except ImportError:
        rec("L32", None, "thiếu PyYAML: NOT_VERIFIED")
    # cửa sổ lộ
    rec("L32", 90 * 24 == 2160 and Fraction(720) / Fraction(1, 4) == 2880 and 30 * 24 == 720 and 15 / 60 == 0.25 and alg.bnx_l32_hours(90) == 2160 and alg.bnx_l32_ratio(720, 0.25) == 2880,
        "cửa sổ lộ: 2 160 giờ so với 1 giờ; quiz: 720 giờ / 0,25 giờ = 2 880 lần")
    # lab
    r = subprocess.run([sys.executable, "-X", "utf8", str(LAB / "loi_giai.py")], capture_output=True, text=True, encoding="utf-8")
    rec("L32", r.returncode == 0 and r.stdout.strip() == (LAB / "mong_doi.txt").read_text(encoding="utf-8").strip(), "lab: loi_giai.py cho đúng mong_doi.txt")
    v, l = alg.bnx_l32_reconcile({"a": 2, "b": 1}, {"a": 5, "c": 1}, False)
    v2, l2 = alg.bnx_l32_reconcile({"a": 2, "b": 1}, {"a": 5, "b": 1, "c": 1}, True)
    rec("L32", v == ["sua a", "tao b"] and l == ["c"] and v2 == ["sua a", "xoa c"] and l2 == [], "lab: sửa a, tạo b rồi còn lệch c; có prune thì xoá c (alg)")
    import fnmatch
    rec("L32", fnmatch.fnmatch("s3:GetObject", "s3:Get*") and not fnmatch.fnmatch("s3:PutObject", "s3:Get*") and fnmatch.fnmatch("bao-cao/rieng/b.csv", "bao-cao/*")
        and fnmatch.fnmatch("bao-cao/rieng/b.csv", "bao-cao/rieng/*"), "dấu * trong chính sách: s3:Get* khớp GetObject không khớp PutObject; bao-cao/* khớp cả bao-cao/rieng/b.csv (cho nên cần Deny riêng)")
    rec("L32", 'path "secret/data/thanh-toan"' in src.SH_VAULT.code and "-mount=secret thanh-toan" in src.SH_VAULT.code, "KV v2: kho secret, bí mật thanh-toan, đường dẫn chính sách secret/data/thanh-toan khớp lệnh ghi hiện trên màn hình")
    # s3:Get* KHÔNG khớp s3:ListBucket (fnmatch của bài); ChinhSach.py hiện đủ đường ra mặc định; bài nói rõ mật khẩu tĩnh còn sống khi thẻ hết hạn
    import fnmatch
    yml = " ".join(next((ROOT / "lessons" / "bnx").glob("L32_*.yaml")).read_text(encoding="utf-8").split())
    rec("L32", not fnmatch.fnmatch("s3:ListBucket", "s3:Get*") and fnmatch.fnmatch("s3:GetObject", "s3:Get*")
        and 'return "tu choi (mac dinh)"' in yml and "không</b> gồm <code>s3:ListBucket</code>" in yml
        and "mật khẩu tĩnh nằm trong kho bí mật vẫn sống sau khi thẻ hết hạn" in yml,
        "s3:Get* không phủ s3:ListBucket; ChinhSach.py hiện cả đường ra mặc định; phân biệt mật khẩu tĩnh với thẻ/bí mật động")
    # R4 SHOULD: màn hình hiện đủ lệnh ghi thử, sleep 6 và lệnh git log đúng thứ tự (mới nhất ở cuối), mỗi khối ≤ 12 dòng
    yml2 = " ".join(next((ROOT / "lessons" / "bnx").glob("L32_*.yaml")).read_text(encoding="utf-8").split())
    ghi_blk = src.SH_VAULT.code.split(chr(10))
    i0 = next(k for k, l in enumerate(ghi_blk) if "ghi() {" in l)
    rec("L32", "sleep 6" in yml2 and "ghi() {" in yml2 and "--reverse" in yml2 and "--name-status" in yml2 and "--format=%s" in yml2 and "head -1" in yml2
        and "sleep 6" in ghi_blk[i0 + 6] and 'git("log", "--reverse", "--name-status", "--format=%s")' in src.P_DC.code
        and "git(\"rm\"" in yml2.replace("&quot;", '"'),
        "màn hình hiện lệnh ghi thử, sleep 6, git rm và đủ lệnh git log --reverse --name-status --format=%s (đúng chữ trong chương trình)")
