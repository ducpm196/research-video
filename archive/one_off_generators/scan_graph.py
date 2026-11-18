with open(r'resources\job\hub-system-graph.md', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'### `([^`]+)`', text)
print(f'Total services: {len(matches)}')
high_impact = [s for s in set(matches) if any(k in s.lower() for k in ['kstream', 'ksql', 'bio', 'virtual', 'statement', 'recon', 'billing', 'napas', 't24', 'qr', 'transfer', 'card', 'core', 'esb', 'gateway', 'auth'])]
print(f'Total high-impact services: {len(high_impact)}')
for s in sorted(high_impact):
    print(' -', s)
