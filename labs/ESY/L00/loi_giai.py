import sys
s = sys.stdin.read().strip() or "25|6,9,4,2"
b_s, l_s = s.split("|")
budget = int(b_s); used = sum(int(x) for x in l_s.split(","))
print(f"used_ms={used} deadline_met={int(used <= budget)} slack={budget - used}ms")
