import pathlib, subprocess, sys

LESSONS = [
    ("ACB", "L00"), ("ACB", "L02"), ("ACB", "L03"), ("ACB", "L04"), ("ACB", "L05"),
    ("BCH", "L01"),
    ("BNK", "L03"), ("BNK", "L04"), ("BNK", "L05"), ("BNK", "L08"), ("BNK", "L09"), ("BNK", "L14"),
    ("BNX", "L06"), ("BNX", "L07"), ("BNX", "L08"), ("BNX", "L14"), ("BNX", "L15"), ("BNX", "L24"),
    ("BNX", "L25"), ("BNX", "L28"), ("BNX", "L34"), ("BNX", "L36"), ("BNX", "L37"), ("BNX", "L38"),
    ("DEN", "L02"), ("DMS", "L07"),
    ("FND", "L00"), ("FND", "L07"), ("FND", "L08"), ("FND", "L09"), ("FND", "L10"),
    ("HCI", "L08"),
    ("INT", "L00"), ("INT", "L03"), ("INT", "L06"),
    ("PRJ", "L06"), ("PRJ", "L07"),
    ("RLN", "L10"),
]

bad = []
for c, l in LESSONS:
    mp4 = pathlib.Path("out") / c / l / f"{l}.mp4"
    r = subprocess.run(["ffmpeg", "-v", "error", "-xerror", "-i", str(mp4), "-f", "null", "-"], capture_output=True, text=True)
    if r.returncode != 0 or r.stderr.strip():
        bad.append((c, l, r.returncode, r.stderr.strip()))
        print(f"FAIL {c} {l}: rc={r.returncode} {r.stderr.strip()}")
print(f"DECODE_38: checked={len(LESSONS)} fail={len(bad)}")
sys.exit(1 if bad else 0)
