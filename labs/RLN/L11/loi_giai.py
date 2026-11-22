finish = 150
loop_r = (1200 // 6) * 2
print(
    f"intended={finish} reward_hacked={loop_r} "
    f"broken={int(loop_r > finish)}"
)
