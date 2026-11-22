inputs = [700, 400]; pay = 850; fee = 20
change = sum(inputs) - pay - fee
print(f"in_sum={sum(inputs)/100:.1f} change={change/100:.1f}")
