cat > gd.csv <<'EOF'
ma,loai,kenh,so_tien
1,rut,atm,500000
2,chuyen,app,1200000
3,thanh_toan,pos,85000
4,chuyen,app,300000
5,nap,quay,5000000
6,rut,atm,2000000
7,chuyen,web,450000
8,thanh_toan,pos,120000
9,chuyen,app,75000
10,rut,atm,1000000
11,nap,app,3000000
12,thanh_toan,web,260000
13,chuyen,app,640000
14,thanh_toan,pos,45000
15,rut,quay,700000
EOF
tail -n +2 gd.csv | wc -l
cut -d, -f2 gd.csv | tail -n +2 | sort | uniq -c
cut -d, -f2 gd.csv | tail -n +2 | sort | uniq -c | sort -rn | head -n 1
cut -d, -f4 gd.csv | tail -n +2 | sort -rn | head -n 3
