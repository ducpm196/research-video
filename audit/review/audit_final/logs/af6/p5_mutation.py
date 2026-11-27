# AF6 probe 5: thử đột biến bộ chấm lab. Với mỗi lab Python có ca_an/:
#   (1) lời giải mẫu phải PASS; (2) "bài làm in cứng" (in nguyên văn mong_doi.txt) phải FAIL.
# Mọi tệp tạm nằm ngoài kho (tempfile). Chỉ đọc kho.
import os, sys, glob, subprocess, tempfile, shutil, collections, time

ROOT = os.path.abspath('.')
BASH = shutil.which('bash') or 'bash'
labs = []
for d in sorted(glob.glob('labs/*/L*')):
    if os.path.isdir(os.path.join(d, 'ca_an')) and os.path.exists(os.path.join(d, 'loi_giai.py')):
        labs.append(d.replace('\\', '/'))
step = int(sys.argv[1]) if len(sys.argv) > 1 else 1
labs = labs[::step]
print('python labs with ca_an tested:', len(labs), 'step', step)
tmp = tempfile.mkdtemp(prefix='af6_mut_')
res = collections.Counter()
bad = []
t0 = time.time()
for d in labs:
    _, c, l = d.split('/')
    exp = open(os.path.join(d, 'mong_doi.txt'), encoding='utf-8').read()
    hard = os.path.join(tmp, f'{c}_{l}_hard.py')
    with open(hard, 'w', encoding='utf-8') as fo:
        fo.write('import sys\nsys.stdout.reconfigure(encoding="utf-8")\nsys.stdout.write(' + repr(exp) + ')\n')
    sol = os.path.join(tmp, f'{c}_{l}_sol.py')
    shutil.copy(os.path.join(d, 'loi_giai.py'), sol)

    def run(path):
        try:
            p = subprocess.run([BASH, ROOT.replace('\\', '/') + '/labs/cham.sh', c, l, path.replace('\\', '/')],
                               cwd=tmp, capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=120)
            return p.returncode, (p.stdout + p.stderr).strip().splitlines()[-1:] or ['']
        except subprocess.TimeoutExpired:
            return 124, ['TIMEOUT']
    rs, ts = run(sol)
    rh, th = run(hard)
    res['sol_pass' if rs == 0 else 'sol_FAIL'] += 1
    res['hard_fail' if rh != 0 else 'hard_PASS'] += 1
    if rs != 0 or rh == 0:
        bad.append((d, rs, ts, rh, th))
print('result', dict(res), 'elapsed_s', int(time.time() - t0))
for b in bad[:60]:
    print('BAD', b)
shutil.rmtree(tmp, ignore_errors=True)
