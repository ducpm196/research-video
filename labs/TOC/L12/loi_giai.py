import sys
s = sys.stdin.read().strip() or "2|1+1|x+1"
e1, e2, e3 = s.split("|")
def ev(expr, x):
    acc = 0
    for term in expr.replace(" ", "").split("+"):
        acc += x if term == "x" else int(term)
    return acc
is_even = lambda ex: all(ev(ex, x) % 2 == 0 for x in (0, 1, 2))
has_yes = any(is_even(ex) for ex in (e1, e2, e3))
has_no = any(not is_even(ex) for ex in (e1, e2, e3))
same_sem = [ev(e1, x) for x in (0, 1, 2)] == [ev(e2, x) for x in (0, 1, 2)]
applies = has_yes and has_no and same_sem
print(f"has_yes={int(has_yes)} has_no={int(has_no)} syn_diff_same_sem={int(same_sem)} rice_applies={int(applies)}")
