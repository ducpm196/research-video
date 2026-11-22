f1, f2, f3 = lambda x: 2, lambda x: 1 + 1, lambda x: x + 1
is_even = lambda f: all(f(x) % 2 == 0 for x in (0, 1, 2))
has_yes = any(is_even(f) for f in (f1, f2, f3))
has_no = any(not is_even(f) for f in (f1, f2, f3))
same_sem = [f1(x) for x in (0, 1, 2)] == [f2(x) for x in (0, 1, 2)]
applies = has_yes and has_no and same_sem
print(f"has_yes={int(has_yes)} has_no={int(has_no)}",
      f"syn_diff_same_sem={int(same_sem)} rice_applies={int(applies)}")
