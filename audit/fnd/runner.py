"""Chạy một phiên Git Bash trong thư mục tạm sạch (dùng chung cho verify_fnd.py và explore.py). Xem verify_fnd.py về cách ổn định hoá."""
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASH = r"C:\Program Files\Git\bin\bash.exe"
if not Path(BASH).exists():
    BASH = shutil.which("bash") or "bash"
MARK = "\x01@@STEP "


def posix(p):
    p = str(p).replace("\\", "/")
    return "/" + p[0].lower() + p[2:] if len(p) > 1 and p[1] == ":" else p


def norm(s):
    return "\n".join(l.rstrip() for l in s.replace("\r\n", "\n").replace("\r", "\n").strip("\n").split("\n"))


def run_session(files, steps, keep=False):
    """files = {đường dẫn tương đối: nội dung}; steps = [lệnh, …]. Trả (đầu ra từng bước {i: chuỗi} hoặc None, lỗi, thư mục tạm)."""
    R = Path(os.path.realpath(tempfile.mkdtemp(prefix="fnd_")))
    home = R / "Users" / "ban"
    home.mkdir(parents=True)
    for rel, content in files.items():
        p = home / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(content.encode("utf-8"))
    (R / "gitconfig").write_text("[user]\n\tname = Ban Hoc\n\temail = ban@example.com\n[init]\n\tdefaultBranch = main\n[core]\n\tautocrlf = false\n"
                                 "[advice]\n\tdetachedHead = false\n", encoding="utf-8", newline="\n")
    env = dict(os.environ)
    env.update({"HOME": str(home), "USERPROFILE": str(home), "GIT_CONFIG_GLOBAL": str(R / "gitconfig"), "GIT_CONFIG_NOSYSTEM": "1",
                "GIT_AUTHOR_DATE": "2026-01-05T09:00:00+0700", "GIT_COMMITTER_DATE": "2026-01-05T09:00:00+0700",
                "LC_ALL": "C.UTF-8", "PYTHONIOENCODING": "utf-8", "PYTHONUTF8": "1"})
    # Git Bash tương tác có alias ls='ls -F --color=auto --show-control-chars' (/etc/profile.d/aliases.sh) và xếp cột khi ra màn hình;
    # chạy tệp thì không: bắt chước bằng -F (thêm / sau thư mục) và -C -w 80 (xếp cột, bề ngang 80), bỏ màu.
    pre = ['cd "$HOME"', "shopt -s expand_aliases"]
    AL_TTY = "alias ls='ls -F -C -T 0 -w 80 --show-control-chars'"       # lệnh ra màn hình: xếp cột như cửa sổ lệnh thật
    AL_PIPE = "alias ls='ls -F --show-control-chars'"                      # có ống/chuyển hướng: ls tự in mỗi tên một dòng
    if not shutil.which("sqlite3"):
        pre.append(f'export PATH="{posix(ROOT / "audit" / "fnd" / "shim")}:$PATH"')
    body = ["__rc=0"]
    for i, a in enumerate(steps):
        # __rc giữ mã thoát của bước trước (alias và printf sẽ đặt lại $?); ngay trước lệnh khôi phục bằng (exit $__rc)
        al = AL_PIPE if re.search(r"[|>`]|\$\(", a) else AL_TTY
        body.append(f"__rc=$?; {al}; printf '\\001@@STEP {i}\\n'; (exit $__rc)")
        # đường dẫn tuyệt đối người học thấy (C:/Users/ban, /c/Users/ban) → thư mục tạm thật
        body.append(a.replace("/c/Users/ban", posix(home)).replace("C:/Users/ban", str(home).replace("\\", "/")))
    (R / "run.sh").write_text("\n".join(pre + body) + "\n", encoding="utf-8", newline="\n")
    wrap = R / "wrap.sh"          # lớp bao: gộp stderr vào stdout đúng thứ tự
    wrap.write_text(f'exec 2>&1\nsource "{posix(R / "run.sh")}"\n', encoding="utf-8", newline="\n")
    try:
        r = subprocess.run([BASH, str(wrap)], cwd=str(home), env=env, capture_output=True, timeout=180, stdin=subprocess.DEVNULL)
    except subprocess.TimeoutExpired:
        return None, "quá thời gian (180 s)", R
    raw = r.stdout.decode("utf-8", errors="replace")
    forms = {str(R): "C:", str(R).replace("\\", "/"): "C:", posix(R): "/c"}
    if str(R).startswith(os.path.realpath(tempfile.gettempdir())):
        forms["/tmp/" + R.name] = "/c"
    for k in sorted(forms, key=len, reverse=True):
        raw = raw.replace(k, forms[k])
    # bash chạy tệp (không tương tác) in “/đường/dẫn/run.sh: line N: lệnh: …”; cửa sổ lệnh thật in “bash: lệnh: …”
    raw = re.sub(r"(?m)^(?:/c|C:)/run\.sh: line \d+: ", "bash: ", raw)
    got = {}
    for seg in raw.split(MARK)[1:]:
        n, _, rest = seg.partition("\n")
        got[int(n)] = rest
    if not keep:
        pass
    return got, "", R
