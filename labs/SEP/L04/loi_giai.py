deps = [('auth', 'MIT'), ('fmt', 'Apache-2.0'), ('csv_fast', 'GPL-3.0'), ('http', 'BSD-3-Clause')]
copyleft = [n for n, lic in deps if lic.startswith('GPL')]
print(f"total_deps={len(deps)} closed_app_conflict={copyleft}")
