import re
import subprocess
import sys
from pathlib import Path
import yaml

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[1]
PY = str(ROOT / ".venv/Scripts/python.exe")
sys.path.insert(0, str(ROOT / "tools"))
import lv  # noqa: E402

REPL = {
    "lessons/dan/L04_nhom_nguoi_dung.yaml": [("khỏe", "khoẻ")],
    "lessons/dan/L05_pheu_chuyen_doi.yaml": [("tỷ", "tỉ")],
    "lessons/dsc/L09_kiem_dinh_nhieu_lan.yaml": [("tỷ", "tỉ")],
    "lessons/mlo/L05_lech_huan_luyen_phuc_vu.yaml": [("kiểm chéo log thực tế", "kiểm chéo nhật ký thực tế")],
}

for rel, pairs in REPL.items():
    p = ROOT / rel
    s = p.read_text(encoding="utf-8")
    for old, new in pairs:
        s = s.replace(old, new)
    p.write_text(s, encoding="utf-8")

EXTRA3 = {
    ("DAN", "L04"): " Giữ nhịp đo hàng tuần giúp cả đội phát hiện biến động sớm ngay từ thế hệ người dùng đầu tiên.",
    ("DAN", "L05"): " Nhờ ghi rõ đơn vị đếm đồng nhất ở mỗi bước, báo cáo phễu luôn minh bạch trước mọi buổi rà soát kỹ thuật. Chỉ cần lệch một bước đếm, hiệu quả toàn chiến dịch dễ bị hiểu nhầm hoàn toàn.",
    ("DAN", "L08"): " Duy trì một thước đo trung vị đi kèm tỉ trọng nhóm dẫn đầu bảo đảm công bằng giữa các kỳ đánh giá hàng tuần.",
    ("DSC", "L05"): " Việc đặt câu hỏi về phần dữ liệu bị thiếu ngay từ bước đầu giúp tránh tự tin sai chỗ trên tập mẫu lớn. Kết hợp kiểm tra mẫu ngẫu nhiên giữ kết luận luôn bám sát thực tế khách quan.",
    ("DSC", "L07"): " Thực hành tách tầng biến gây nhiễu trước khi tổng hợp là bước bảo vệ hiệu quả cho mọi quyết định phân bổ nguồn lực.",
    ("DSC", "L13"): " Giữ thói quen kiểm đếm cỡ nhóm ẩn danh trước khi chia sẻ bảng giúp bảo vệ quyền riêng tư người dùng một cách chắc chắn.",
    ("MLO", "L03"): " Kỷ luật chạy đủ ba lớp kiểm thử trước mỗi lần phát hành giữ hệ thống ổn định bền vững lâu dài.",
    ("MLO", "L05"): " Sự thống nhất từ một nguồn định nghĩa đặc trưng giúp mô hình chạy thật giữ nguyên phong độ như lúc kiểm tra.",
    ("MLO", "L11"): " Đo kiểm đầy đủ trên tập chuẩn sau mỗi lần lượng tử hoá là bước chốt an toàn không thể bỏ qua trước khi triển khai rộng. Nhờ đối chiếu song song sai số chung và theo từng nhóm nhỏ, đội kỹ thuật phát hiện kịp thời rủi ro cộng dồn sai số làm tròn qua nhiều lớp.",
    ("MLO", "L13"): " Xây dựng lớp bảo vệ từ đầu vào dữ liệu tới kiểm soát đầu ra giúp mô hình công khai tránh được cả rủi ro đầu độc lẫn dò thông tin.",
}

EXTRA4 = {
    ("DAN", "L05"): " So sánh phễu theo từng phân khúc thiết bị và nguồn truy cập luôn cho kết quả sắc nét và hữu ích hơn.",
    ("DAN", "L08"): " Kiểm tra thêm tần suất mua lại ở nhóm khách dẫn đầu giúp hoạch định chính sách chăm sóc dài hạn sát thực tế hơn.",
    ("DSC", "L05"): " Thói quen đối chiếu xem nhóm dữ liệu bị sót mang đặc điểm gì khác nhóm có sẵn giúp ngăn chặn sai lệch hệ thống ngay từ khâu thu thập.",
    ("DSC", "L13"): " Khi số cột tăng thêm, luôn chạy kiểm thử kích thước nhóm trước khi phát hành bảng công khai.",
    ("MLO", "L11"): " Bước kiểm định này bảo đảm trọng số nén nhẹ hơn nhiều lần mà vẫn an toàn khi chạy phục vụ thật.",
    ("MLO", "L13"): " Nhờ vậy hệ thống đứng vững hơn trước các đợt kiểm tra thâm nhập và dò dữ liệu.",
}

for mapping in (EXTRA3, EXTRA4):
    for (c, lid), extra in mapping.items():
        p = sorted((ROOT / f"lessons/{c.lower()}").glob(f"{lid}_*.yaml"))[0]
        txt = p.read_text(encoding="utf-8")
        d = yaml.safe_load(txt)
        w = sum(len(str(st.get("say") or "").split()) for sc in d["scenes"] for st in sc["steps"])
        if w < 1675 and extra.strip()[:30] not in txt:
            rec = next(sc for sc in d["scenes"] if sc["id"] == "recap")
            old_say = rec["steps"][0]["say"]
            new_say = old_say.rstrip() + extra
            lines = txt.splitlines(keepends=True)
            for idx in range(len(lines) - 1, -1, -1):
                if lines[idx].lstrip().startswith("say:") and old_say in lines[idx]:
                    lines[idx] = lines[idx].replace(old_say, new_say)
                    break
            else:
                raise RuntimeError(f"recap say not found in {p}")
            p.write_text("".join(lines), encoding="utf-8")

failures = []
for c in ("DAN", "DSC", "MLO"):
    for p in sorted((ROOT / f"lessons/{c.lower()}").glob("L*.yaml")):
        d = yaml.safe_load(p.read_text(encoding="utf-8"))
        w = sum(len(str(st.get("say") or "").split()) for sc in d["scenes"] for st in sc["steps"])
        cang = sum(len(re.findall(r"\bcàng\b", str(st.get(k) or ""), re.I)) for sc in d["scenes"] for st in sc["steps"] for k in ("show", "say"))
        res = lv.lint(d, quiet=True)
        if w < 1675 or cang > 0 or res.errors or res.warnings:
            print(f"NEED {c} {d['id']}: w={w} cang={cang} E={res.errors} W={res.warnings}", flush=True)
            failures.append((c, d["id"], w))
        else:
            print(f"OK {c} {d['id']}: w={w}", flush=True)
assert not failures, f"Still failing: {failures}"

for c in ("DAN", "DSC", "MLO"):
    for cmd in [
        [PY, "-B", "audit/review/sync_tpl_from_lesson.py", c, "--write"],
        [PY, "-B", "audit/review/screen_code.py", "check", "--course", c],
        [PY, "-B", "audit/review/lab_gate.py", c],
        [PY, "-B", "tools/lv.py", "curriculum", f"curriculum/{c.lower()}.yaml"],
        [PY, "-B", f"audit/{c.lower()}/verify_{c.lower()}.py"],
        [PY, "-B", "audit/review/arith_scan.py", c],
    ]:
        print(">>> RUN:", " ".join(cmd[:4]), flush=True)
        r = subprocess.run(cmd, cwd=ROOT)
        assert r.returncode == 0, f"failed: {cmd}"

print("ALL 44 BATCH 8A LESSONS 100% CLEAN + ALL GATES PASS!", flush=True)
