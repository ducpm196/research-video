import pathlib

REPS = [
    ('say: "O-ra-cơn"', 'say: "O-rơ-cồ"'),
    ('say: O-ra-cơn', 'say: O-rơ-cồ'),
    ('say: "cây-x-cu-l-đê-bê"', 'say: "ca ét kiu eo đê bê"'),
    ('say: cây-x-cu-l-đê-bê', 'say: ca ét kiu eo đê bê'),
    ('say: "P Lét Cù L"', 'say: "P L ét kiu eo"'),
    ('say: P Lét Cù L', 'say: P L ét kiu eo'),
    ('say: "Pốt-g-rê ét-cu-l"', 'say: "Pốt-g-rê ét kiu eo"'),
    ('say: Pốt-g-rê ét-cu-l', 'say: Pốt-g-rê ét kiu eo'),
    ('say: "ét-cu-l"', 'say: "ét kiu eo"'),
    ('say: ét-cu-l', 'say: ét kiu eo'),
]

for p in sorted(pathlib.Path("tools/registry").glob("lexicon_vi.*.yaml")):
    txt = p.read_text("utf-8")
    new = txt
    for old, rep in REPS:
        new = new.replace(old, rep)
    if new != txt:
        p.write_text(new, "utf-8")
        print("UPDATED:", p.name)
