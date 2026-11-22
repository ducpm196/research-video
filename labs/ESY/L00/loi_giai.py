budget = 25
used = 6 + 9 + 4 + 2
print(f"used_ms={used} deadline_met={int(used <= budget)} slack={budget - used}ms")
