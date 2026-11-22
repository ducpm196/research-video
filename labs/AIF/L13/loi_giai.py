import math
log10_full = 60 * math.log10(20)
d3 = 20 ** 3
log10_red = log10_full - 3 * math.log10(20)
print(
    f"log10_tree={log10_full:.1f} depth3_nodes={d3} "
    f"log10_reduction={log10_red:.1f}"
)
