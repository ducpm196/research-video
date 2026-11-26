import sys
s = sys.stdin.read().strip() or "PUSH 12;PUSH 3;PUSH 2;MUL;SUB"
st = []
for ins in s.split(";"):
    if ins.startswith("PUSH"): st.append(int(ins.split()[1]))
    elif ins == "MUL": b, a = st.pop(), st.pop(); st.append(a * b)
    elif ins == "SUB": b, a = st.pop(), st.pop(); st.append(a - b)
print(f"vm_result={st[0]}")
