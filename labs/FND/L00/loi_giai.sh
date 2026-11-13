for ten in bash git javac java python; do
  if command -v "$ten" >/dev/null; then echo "✔ $ten"
  else echo "THIEU $ten"; fi
done
if python -c "import sqlite3" 2>/dev/null; then echo "✔ sql"
else echo "THIEU sql"; fi
