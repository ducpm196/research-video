import sys
s = sys.stdin.read().strip() or "9.0 12.0"
f_sig, fs = map(float, s.split())
nyq = 2.0 * f_sig
alias = abs(f_sig - round(f_sig / fs) * fs)
print(f"need_fs_gt={nyq:.0f}Hz observed_alias={alias:.0f}Hz")
