def lookup(env, name):
    while env is not None:
        if name in env['vars']: return env['vars'][name]
        env = env['parent']
global_env = {'vars': {'x': 15}, 'parent': None}
fn_def_parent = global_env
def call_fn(caller_env, dynamic=False):
    local_env = {'vars': {}, 'parent': caller_env if dynamic else fn_def_parent}
    return lookup(local_env, 'x')
caller_env = {'vars': {'x': 30}, 'parent': global_env}
print(f"static={call_fn(caller_env, False)} dynamic={call_fn(caller_env, True)}")
