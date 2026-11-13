BEGIN { print "ngay,tk,loai,so_tien" }
{ printf "2026-01-%02d,A0%d,%s,%d\n", $1 % 28 + 1, $1 % 3 + 1,
    ($1 % 4 == 0 ? "rut" : "nap"), 1000 * ($1 % 50 + 1) }
