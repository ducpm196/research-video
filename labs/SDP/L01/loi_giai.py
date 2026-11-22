def naive(s): return int(''.join(c for c in s if c.isdigit()) or 0)
def strict(s): return int(s)
raised = 0
try: strict('12a')
except ValueError: raised = 1
print(f'naive_12a={naive("12a")}')
print(f'strict_42={strict("42")}')
print(f'strict_12a_raised={raised}')
