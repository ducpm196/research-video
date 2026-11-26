import sys
s = sys.stdin.read().strip() or "15 30"
gx, cx = map(int, s.split())
def lookup(env, name):
    while env is not None:
        if name in env["vars"]: return env["vars"][name]
        env = env["parent"]
global_env = {"vars": {"x": gx}, "parent": None}
caller_env = {"vars": {"x": cx}, "parent": global_env}
def call_fn(c_env, dynamic=False):
    local_env = {"vars": {}, "parent": c_env if dynamic else global_env}
    return lookup(local_env, "x")
print(f"static={call_fn(caller_env, False)} dynamic={call_fn(caller_env, True)}")
