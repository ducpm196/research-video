import math
b1 = math.log2(26 ** 8); b2 = math.log2(7776 ** 4)
print(f'bits_8_lower={b1:.1f}')
print(f'bits_4_words={b2:.1f}')
print(f'words_stronger={int(b2 > b1)}')
