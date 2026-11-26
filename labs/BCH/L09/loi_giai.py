import sys
s = sys.stdin.read().strip() or "10 2"
pool, dep = map(int, s.split())
class Vault:
    def __init__(self, pl, safe):
        self.pool, self.safe, self.bal = pl, safe, dep
    def withdraw(self, who):
        if self.bal <= 0 or self.pool < dep: return
        if self.safe: self.bal = 0; self.pool -= dep; who.recv(self)
        else: self.pool -= dep; who.recv(self); self.bal = 0
class Attacker:
    def __init__(self): self.got = 0
    def recv(self, v): self.got += dep; v.withdraw(self)
def run(safe):
    v, a = Vault(pool, safe), Attacker(); v.withdraw(a); return a.got
print(f"unsafe_stolen={run(False)} safe_withdrawn={run(True)}")
