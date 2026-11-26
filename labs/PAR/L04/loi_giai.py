import sys
s = sys.stdin.read().strip() or "4,9,2,8,1,7,3,6"
jobs = [int(x) for x in s.split(",")]
half = len(jobs) // 2
static_ms = max(sum(jobs[:half]), sum(jobs[half:]))
loads = [0, 0]
for j in sorted(jobs, reverse=True):
    i = 0 if loads[0] <= loads[1] else 1
    loads[i] += j
print(f"static_makespan={static_ms} lpt_makespan={max(loads)}")
