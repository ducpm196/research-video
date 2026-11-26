import sys
s = sys.stdin.read().strip() or "auth:MIT,fmt:Apache-2.0,csv_fast:GPL-3.0,http:BSD-3-Clause"
deps = [tuple(p.split(":", 1)) for p in s.split(",") if p]
copyleft = [n for n, lic in deps if lic.startswith("GPL")]
print(f"total_deps={len(deps)} closed_app_conflict={copyleft}")
