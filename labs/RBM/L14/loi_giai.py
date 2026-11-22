f_sig, fs = 9.0, 12.0
nyquist_min = 2.0 * f_sig
k = round(f_sig / fs)
alias = abs(f_sig - k * fs)
print(f"need_fs_gt={nyquist_min:.0f}Hz observed_alias={alias:.0f}Hz")
