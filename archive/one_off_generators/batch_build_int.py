import os
import shutil
import subprocess
import sys
import time

LESSONS = [
    ("L00", "lessons/int/L00_overview_zero_to_senior.yaml", "00_overview_roadmap"),
    ("L01", "lessons/int/L01_foundation_cs_java.yaml", "01_foundation_cs_java"),
    ("L02", "lessons/int/L02_backend_microservices.yaml", "02_backend_microservices"),
    ("L03", "lessons/int/L03_distributed_systems_senior.yaml", "03_distributed_systems_senior"),
    ("L04", "lessons/int/L04_banking_domain_t24_napas.yaml", "04_banking_domain_t24_napas"),
    ("L05", "lessons/int/L05_uit_ai_banking_multiplier.yaml", "05_uit_ai_banking_multiplier"),
    ("L06", "lessons/int/L06_interview_qa_bank_100.yaml", "06_interview_qa_bank_100"),
    ("L07", "lessons/int/L07_salary_negotiation_50m_gross.yaml", "07_salary_negotiation_50m_gross")
]

VENV_PY = r"D:\research-video\.venv\Scripts\python.exe"
DEST_DIR = r"D:\research-video\interview\video"
os.makedirs(DEST_DIR, exist_ok=True)

for lid, spec_path, slug in LESSONS:
    src_dir = os.path.join(r"D:\research-video\out\INT", lid)
    mp4_src = os.path.join(src_dir, f"{lid}.mp4")
    
    # Check if already built and valid
    need_build = True
    if os.path.exists(mp4_src) and os.path.getsize(mp4_src) > 1000000:
        # verify existing
        vcmd = [VENV_PY, "tools/lv.py", "verify", spec_path]
        vres = subprocess.run(vcmd, capture_output=True, text=True)
        if vres.returncode == 0:
            print(f"[CACHE HIT] {lid} already built and verified PASS.")
            need_build = False

    if need_build:
        t0 = time.time()
        print(f"\n=======================================================")
        print(f"BUILDING {lid}: {spec_path} -> {slug}")
        print(f"=======================================================")
        cmd = [VENV_PY, "tools/lv.py", "build", spec_path]
        res = subprocess.run(cmd, capture_output=True, text=True)
        print(res.stdout)
        if res.returncode != 0:
            print(f"[ERROR] Failed to build {lid}: exit code {res.returncode}")
            print(res.stderr)
            sys.exit(1)

        # Verify
        vcmd = [VENV_PY, "tools/lv.py", "verify", spec_path]
        vres = subprocess.run(vcmd, capture_output=True, text=True)
        print(vres.stdout)
        if vres.returncode != 0:
            print(f"[ERROR] Verification failed for {lid}")
            print(vres.stderr)
            sys.exit(1)
        print(f"[DONE] {lid} built in {time.time() - t0:.1f}s")

    # Copy artifacts
    srt_src = os.path.join(src_dir, f"{lid}.srt")
    ch_src = os.path.join(src_dir, "chapters.txt")
    rep_src = os.path.join(src_dir, "build_report.json")

    if os.path.exists(mp4_src):
        shutil.copy2(mp4_src, os.path.join(DEST_DIR, f"{slug}.mp4"))
        shutil.copy2(mp4_src, os.path.join(DEST_DIR, f"INT_{lid}.mp4"))
    if os.path.exists(srt_src):
        shutil.copy2(srt_src, os.path.join(DEST_DIR, f"{slug}.srt"))
        shutil.copy2(srt_src, os.path.join(DEST_DIR, f"INT_{lid}.srt"))
    if os.path.exists(ch_src):
        shutil.copy2(ch_src, os.path.join(DEST_DIR, f"{slug}_chapters.txt"))
        shutil.copy2(ch_src, os.path.join(DEST_DIR, f"INT_{lid}_chapters.txt"))
    if os.path.exists(rep_src):
        shutil.copy2(rep_src, os.path.join(DEST_DIR, f"{slug}_build_report.json"))

    print(f"[COPIED] {lid} -> {slug}.mp4 & INT_{lid}.mp4")

print("\n>>> ALL 8 LESSONS BUILT, VERIFIED, AND DEPLOYED TO interview/video/ SUCCESSFULLY!")
