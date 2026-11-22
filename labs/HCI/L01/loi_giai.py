import math
n = 6
guesses = math.factorial(n)
matched = int(len(set(range(n))) == n)
print(f"linear_guesses={guesses} matched_2d={matched}")
