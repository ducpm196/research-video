cat > gd.csv <<'EOF'
ngay,loai,so_tien
01,luong,12000000
02,an,150000
03,di_lai,60000
05,an,220000
08,mua_sam,900000
10,an,95000
12,di_lai,45000
15,luong,3000000
EOF
# may kiem chua cai sqlite3: dung ban thay the cua kho (hoc vien da cai sqlite3 thi bo qua hai dong nay)
command -v sqlite3 > /dev/null 2>&1 || sqlite3() { cat > q.sql; python "$(dirname "$0")/../../sqlrun.py" q.sql; }
{
  echo "CREATE TABLE gd (ngay TEXT, loai TEXT, so_tien INTEGER);"
  tail -n +2 gd.csv | sed "s/\(.*\),\(.*\),\(.*\)/INSERT INTO gd VALUES ('\1', '\2', \3);/"
  echo "SELECT loai, SUM(so_tien) FROM gd WHERE loai <> 'luong' GROUP BY loai ORDER BY loai;"
  echo "SELECT 'so du', SUM(CASE WHEN loai = 'luong' THEN so_tien ELSE -so_tien END) FROM gd;"
} | sqlite3 :memory: > bao_cao.txt
cat bao_cao.txt
a=$(tail -n 1 bao_cao.txt | cut -d'|' -f2)
b=$(awk -F, 'NR > 1 { if ($2 == "luong") s += $3; else s -= $3 } END { print s }' gd.csv)
[ "$a" = "$b" ] && echo "tong khop: $a" || echo "LECH: $a $b"
git init -q -b main repo
cp bao_cao.txt gd.csv repo/
cd repo
git config user.name "Hoc Vien"
git config user.email "hv@example.com"
git add bao_cao.txt gd.csv
git commit -q -m "bao cao thang 1"
git log --format=%s
