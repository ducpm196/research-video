"""(Chuyển từ scratchpad phiên 7f725234 vào kho 2026-11-10 để dùng lại; chạy: .venv/Scripts/python audit/review/interview_sync_video.py [--check])
Copy rebuilt INT/ACB outputs from out/ into interview/video/ under the names the docs link to, then verify by sha256."""
import hashlib, shutil, sys
from pathlib import Path
ROOT = Path("D:/research-video"); V = ROOT / "interview/video"
INT = ["00_overview_roadmap", "01_foundation_cs_java", "02_backend_microservices", "03_distributed_systems_senior",
       "04_banking_domain_t24_napas", "05_uit_ai_banking_multiplier", "06_interview_qa_bank_100", "07_salary_negotiation_50m_gross"]
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
pairs = []
for i, n in enumerate(INT):
    L = f"L{i:02d}"; o = ROOT / "out/INT" / L
    pairs += [(o / f"{L}.mp4", V / f"{n}.mp4"), (o / f"{L}.mp4", V / f"INT_{L}.mp4"),
              (o / f"{L}.srt", V / f"{n}.srt"), (o / f"{L}.srt", V / f"INT_{L}.srt"),
              (o / "chapters.txt", V / f"{n}_chapters.txt"), (o / "chapters.txt", V / f"INT_{L}_chapters.txt"),
              (o / "build_report.json", V / f"{n}_build_report.json")]
for i in range(9):
    L = f"L{i:02d}"; o = ROOT / "out/ACB" / L
    sfx = "" if i == 0 else f"_{L}"
    pairs += [(o / f"{L}.mp4", V / f"{L}.mp4"), (o / f"{L}.srt", V / f"{L}.srt"),
              (o / "chapters.txt", V / f"chapters{sfx}.txt"), (o / "build_report.json", V / f"build_report{sfx}.json")]
dry = "--check" in sys.argv
bad = 0
for src, dst in pairs:
    if not dry and (not dst.exists() or sha(src) != sha(dst)):
        shutil.copyfile(src, dst)
    ok = dst.exists() and sha(src) == sha(dst)
    bad += not ok
    if not ok: print("MISMATCH", dst.name)
print(f"{len(pairs)} pairs, {len(pairs) - bad} identical, {bad} mismatched")
