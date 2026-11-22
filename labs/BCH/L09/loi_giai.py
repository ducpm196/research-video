class Vault:
    def __init__(self, pool, safe):
        self.pool, self.safe, self.bal = pool, safe, 2
    def withdraw(self, who):
        if self.bal <= 0 or self.pool < 2: return
        if self.safe: self.bal = 0; self.pool -= 2; who.recv(self)
        else: self.pool -= 2; who.recv(self); self.bal = 0
class Attacker:
    def __init__(self): self.got = 0
    def recv(self, v): self.got += 2; v.withdraw(self)
def run(safe):
    v, a = Vault(10, safe), Attacker(); v.withdraw(a); return a.got
print(f"unsafe_stolen={run(False)} safe_withdrawn={run(True)}")
