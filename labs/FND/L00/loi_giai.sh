dat() {
  v=$("$1" --version 2>/dev/null | grep -oE '[0-9.]+' | head -1)
  nho=$(printf '%s\n%s\n' "$2" "$v" | sort -V | head -1)
  if [ "$nho" = "$2" ]; then echo "✔ $1"; else echo "THIEU $1"; fi
}
dat bash 4.0
dat git 2.28
dat javac 21
dat java 21
dat python 3.11
dat sqlite3 3.32
