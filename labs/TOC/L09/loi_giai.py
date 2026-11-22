tape = list('10111'); pos = len(tape) - 1; state = 'C'; steps = 0
while state != 'H':
    sym = '_' if pos < 0 else tape[pos]
    steps += 1
    if sym == '1':
        tape[pos] = '0'; pos -= 1
    else:
        if pos < 0: tape.insert(0, '1')
        else: tape[pos] = '1'
        state = 'H'
print(f"tm_inc={''.join(tape)} steps={steps}")
