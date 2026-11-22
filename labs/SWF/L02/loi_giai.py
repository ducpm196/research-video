a, b, steps, dec = 1071, 462, 0, True
while b > 0:
    nxt = a % b
    dec = dec and (0 <= nxt < b)
    a, b = b, nxt; steps += 1
print(f'gcd={a}')
print(f'steps={steps}')
print(f'strictly_decreasing={int(dec)}')
