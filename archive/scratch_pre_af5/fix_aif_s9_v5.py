from contextlib import redirect_stdout
import io
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(r"D:\research-video")
sys.path.insert(0, str(ROOT / "tools"))
import lv  # noqa: E402


def append_recap0(lid: str, extra: str) -> None:
    p = sorted((ROOT / "lessons" / "aif").glob(f"{lid}_*.yaml"))[0]
    txt = p.read_text(encoding="utf-8")
    if extra.strip() in txt:
        return
    sp = lv.load_spec(p)
    recap = [sc for sc in sp["scenes"] if sc["kind"] == "recap"][0]
    old = recap["steps"][0]["say"]
    assert old in txt and txt.count(old) == 1
    p.write_text(txt.replace(old, old.rstrip() + " " + extra.strip(), 1), encoding="utf-8")


# Fix L07 UCB lexicon warning
p07 = sorted((ROOT / "lessons" / "aif").glob("L07_*.yaml"))[0]
t07 = p07.read_text(encoding="utf-8")
if "công thức UCB1" in t07:
    p07.write_text(t07.replace("công thức UCB1", "công thức cận trên tin cậy"), encoding="utf-8")

TOP2 = {
    "L05": "Chúc bạn cài đặt thành công bài toán sáu vùng không trùng màu.",
    "L06": "Cắt đúng cận giúp giữ nguyên đáp án tối ưu ở gốc mà rút ngắn mạnh thời gian duyệt cây.",
    "L08": "Hiểu vững logic mệnh đề giúp bạn thiết kế bộ kiểm tra tính đúng đắn tự động cho mọi quy tắc suy luận chặt chẽ.",
    "L09": "Phân biệt rõ chiều dữ liệu tiến và chiều mục tiêu lùi sẽ giúp bạn xử lý đúng mọi hệ luật.",
    "L10": "Hãy đối chiếu kỹ mọi tiền điều kiện trước khi chọn hành động để đạt đích nhanh nhất.",
    "L12": "Cách gán đồng loạt này bảo đảm không giá trị mới nào bị trộn lẫn trong cùng một vòng lặp.",
    "L13": "Việc chọn đúng công cụ từ bản đồ tổng hợp sẽ tiết kiệm rất nhiều công sức khi triển khai ngoài thực tế.",
}
for lid, ext in TOP2.items():
    append_recap0(lid, ext)

TOP3 = {
    "L02": (
        "Hãy nhớ rằng hai hàm đánh giá có cùng điều kiện chấp nhận được vẫn cho hiệu năng rất khác nhau nếu độ chặt ước lượng khác nhau. "
        "Luôn thử nghiệm hàm đánh giá trên một bài toán nhỏ có lời giải biết trước để kiểm chứng cả độ chính xác lẫn số nút mở rộng thực tế. "
        "Thói quen so sánh trực tiếp số trạng thái đã duyệt giúp bạn phát hiện ngay hàm đánh giá nào thực sự tiết kiệm bộ nhớ khi mở rộng quy mô. "
        "Khi bước vào bài thực hành ngay sau đây, hãy đối chiếu thật kỹ cả hai giá trị ước lượng trên cùng một bảng tám ô số."
    ),
    "L03": "Khi hiểu rõ cách nới lỏng từng ràng buộc và cách chọn giá trị lớn nhất của nhiều hàm hợp lệ, bạn luôn có phương pháp bài bản để nâng cấp bộ tìm kiếm.",
    "L06": "Khi luyện tập thêm nhiều cây trò chơi nhỏ, trực giác chọn nhánh đi trước của bạn sẽ sắc bén hơn hẳn.",
    "L08": "Nắm chắc bảng chân trị cùng phép tương đương logic là nền tảng vững vàng để xây dựng mọi hệ lập luận tự động về sau.",
    "L09": "Khi nắm vững hai hướng suy diễn tiến và lùi trên hệ luật chặt chẽ, bạn dễ dàng chọn hướng tiết kiệm bước tính nhất cho từng bài toán.",
    "L10": "Hãy thử tự tay viết thêm một vài kịch bản lập kế hoạch nhỏ để thấy rõ hiệu quả cắt giảm không gian tìm kiếm.",
    "L13": "Từ nền tảng tìm kiếm đến suy diễn và ra quyết định, bạn đã sẵn sàng ghép nối chúng vào bài toán thực tế.",
}

PY = str(ROOT / ".venv" / "Scripts" / "python.exe")
print(">>> RUN: up_s9_data_ai.py AIF", flush=True)
r = subprocess.run([PY, "-B", "-u", "audit/s9_11/up_s9_data_ai.py", "AIF"], cwd=ROOT)
assert r.returncode == 0, "FAILED: up_s9_data_ai.py AIF"

for lid, ext in TOP3.items():
    append_recap0(lid, ext)

bad = []
for i in range(15):
    lid = f"L{i:02d}"
    fp = sorted((ROOT / "lessons" / "aif").glob(f"{lid}_*.yaml"))[0]
    sp = lv.load_spec(fp)
    w = sum(len((st.get("say") or "").split()) for sc in sp["scenes"] for st in sc["steps"])
    with redirect_stdout(io.StringIO()):
        res = lv.lint(sp, quiet=True)
    if res.errors or res.warnings:
        bad.append(f"{lid} E={res.errors} W={res.warnings}")
    if w < 1645:
        bad.append(f"{lid} w={w} (need +{1655-w})")
    for sc in sp["scenes"]:
        for idx, st in enumerate(sc["steps"]):
            say = st.get("say") or ""
            foc = st.get("focus")
            sents = lv.sentences(say)
            if foc is not None and len(foc) != len(sents):
                bad.append(f"{lid}:{sc['id']}#{idx} focus mismatch")
            for s in sents:
                if len(s) > 170: bad.append(f"{lid}:{sc['id']}#{idx} >170: {s}")
                if len(s.split()) > 38: bad.append(f"{lid}:{sc['id']}#{idx} >38w: {s}")
                if "càng " in s.lower(): bad.append(f"{lid}:{sc['id']}#{idx} 'càng ': {s}")
                if re.search(r"[$_^]", s): bad.append(f"{lid}:{sc['id']}#{idx} TeX: {s}")
    print(f"AIF:{lid}: w={w} E={len(res.errors)} W={len(res.warnings)}", flush=True)
for b in bad:
    print("BAD:", b, flush=True)
assert not bad, f"{len(bad)} AIF issues"

for cmd in (
    [PY, "-B", "-u", "audit/review/sync_tpl_from_lesson.py", "AIF", "--write"],
    [PY, "-B", "-u", "audit/review/screen_code.py", "check", "--course", "AIF"],
    [PY, "-B", "-u", "audit/review/lab_gate.py", "AIF"],
    [PY, "-B", "-u", "tools/lv.py", "curriculum", "curriculum/aif.yaml"],
    [PY, "-B", "-u", "audit/aif/verify_aif.py"],
):
    print(">>> RUN:", " ".join(cmd), flush=True)
    r = subprocess.run(cmd, cwd=ROOT)
    assert r.returncode == 0, f"FAILED: {cmd}"
print("AIF STAGE 9 UPGRADE & VERIFY PASSED!", flush=True)
