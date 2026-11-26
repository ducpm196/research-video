SELECT 'cross_rows=' || COUNT(*) FROM SV CROSS JOIN Lop;
SELECT 'inner_rows=' || COUNT(*) FROM SV JOIN Lop ON lop=ma;
SELECT 'top_cs=' || COALESCE((SELECT SV.ten FROM SV JOIN Lop ON lop=ma WHERE Lop.ten='CS' AND diem>=7 ORDER BY SV.ten LIMIT 1), 'NONE');
