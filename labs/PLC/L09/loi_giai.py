def bad(x, lst=[]): lst.append(x); return lst
def good(x, lst=None): lst = [] if lst is None else lst; lst.append(x); return lst
bad(10); r_bad = bad(20)
good(10); r_good = good(20)
print(f"bad={r_bad} good={r_good}")
