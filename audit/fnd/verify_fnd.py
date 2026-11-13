"""Bộ kiểm độc lập khoá FND: chạy THẬT bằng Git Bash mọi phiên dòng lệnh khai bằng lib.cmd(...) trong audit/fnd/src/lXX.py, trong một thư mục tạm
sạch, rồi so đầu ra từng bước (stdout + stderr gộp) với giá trị bài giảng ghi. Đây là cách kiểm khác hẳn `checks` (Python): chạy chính
các lệnh người học sẽ gõ.
Chạy: .venv/Scripts/python audit/fnd/verify_fnd.py [L00 L01 …]
Ổn định hoá (runner.py): thư mục tạm hiện là C:/Users/ban (đổi chuỗi đường dẫn trong đầu ra); HOME trỏ vào đó; Git dùng tệp cấu hình riêng (tên,
thư điện tử, nhánh mặc định main, autocrlf tắt, không đọc cấu hình hệ thống) và ngày giờ cố định; máy chưa có sqlite3 thì dùng shim audit/fnd/shim."""
import importlib
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "audit" / "fnd"))
sys.path.insert(0, str(ROOT / "audit" / "fnd" / "src"))
sys.stdout.reconfigure(encoding="utf-8")
import lib  # noqa: E402
from runner import norm, run_session  # noqa: E402

ok = fail = 0
want = [a.upper() for a in sys.argv[1:]] or sorted(p.stem.upper() for p in (ROOT / "audit/fnd/src").glob("l*.py"))
for lid in want:
    lib.begin(lid)
    importlib.import_module(lid.lower()).build()
seen = set()
for c in lib.CMDS:
    key = (c["lesson"], c["name"], tuple(c["steps"]), tuple(sorted(c["files"].items())))
    if key in seen:
        continue
    seen.add(key)
    got, err, R = run_session(c["files"], [a for a, _ in c["steps"]])
    msgs = []
    if got is None:
        msgs.append(err)
    else:
        for i, (a, want_out) in enumerate(c["steps"]):
            have = norm(got.get(i, "<<không có đầu ra>>"))
            if have != norm(want_out):
                msgs.append(f"bước {i} `{a.splitlines()[0][:50]}`: mong {norm(want_out)[:200]!r}; thấy {have[:200]!r}")
    good = not msgs
    ok += good
    fail += not good
    print(f"{'PASS' if good else 'FAIL'} {c['lesson']} {c['name']}: " + (f"{len(c['steps'])} bước khớp" if good else " | ".join(msgs)))
    shutil.rmtree(R, ignore_errors=True)
print(f"verify_fnd: {ok}/{ok + fail} PASS")
print("checked_at=" + datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
sys.exit(1 if fail else 0)
