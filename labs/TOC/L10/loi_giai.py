import sys
s = sys.stdin.read().strip() or "10110"
tbl = {("F", "0"): ("F", "1", "R"), ("F", "1"): ("F", "0", "R"), ("F", "_"): ("H", "_", "S")}
tape = list(s); pos = 0; st = "F"; steps = 0
while st != "H":
    ch = tape[pos] if 0 <= pos < len(tape) else "_"
    st, write, mv = tbl[(st, ch)]
    if 0 <= pos < len(tape): tape[pos] = write
    pos += 1 if mv == "R" else (-1 if mv == "L" else 0)
    steps += 1
print(f"tape_out={''.join(tape)} steps={steps} final_state={st}")
