from pathlib import Path
import subprocess
import sys

ROOT = Path(r"D:\research-video")
sys.path.insert(0, str(ROOT / "tools"))
import lv  # noqa: E402


def append_recap0(rel: str, extra: str) -> None:
    p = ROOT / rel
    txt = p.read_text(encoding="utf-8")
    sp = lv.load_spec(p)
    recap = [sc for sc in sp["scenes"] if sc["kind"] == "recap"][0]
    old_say = recap["steps"][0]["say"]
    assert old_say in txt and txt.count(old_say) == 1
    p.write_text(txt.replace(old_say, old_say.rstrip() + " " + extra.strip(), 1), encoding="utf-8")


append_recap0(
    "lessons/cs115/L35_rnn_lstm.yaml",
    "Việc đối chiếu cả hai cơ chế tắt dần và bùng nổ qua bài thực hành sẽ giúp bạn làm chủ chuỗi thời gian.",
)
append_recap0(
    "lessons/cs115/L36_boosting.yaml",
    "Thực hành tính tay hai trọng số AdaBoost và phần dư ngay sau đây để nhớ chắc công thức nền.",
)
append_recap0(
    "lessons/cs115/L43_diffusion.yaml",
    "Cách tách bài toán phức tạp thành nhiều bước khử nhiễu nhỏ là tư duy thiết kế rất đáng học hỏi.",
)

# Check CS115 L22..43 sentences & words before running up_s9_cs115.py
exec(open(ROOT / "scratch" / "check_cs115_s9_sentences.py", encoding="utf-8").read())

PY = str(ROOT / ".venv" / "Scripts" / "python.exe")
for cmd in (
    [PY, "-B", "-u", "audit/s9_11/up_s9_cs115.py"],
    [PY, "-B", "-u", "tools/lv.py", "curriculum", "curriculum/cs115.yaml"],
    [PY, "-B", "-u", "audit/verify_cs115_tex.py"],
    [PY, "-B", "-u", "audit/layout_scan.py", "CS115"],
):
    print(">>> RUN:", " ".join(cmd), flush=True)
    r = subprocess.run(cmd, cwd=ROOT)
    assert r.returncode == 0, f"FAILED: {cmd}"
print("CS115 STAGE 9 COMPLETE PIPELINE PASSED!", flush=True)
