SELECT 'left_all=' || COUNT(*) FROM SV LEFT JOIN Lop ON lop=ma;
SELECT 'left_where_drops_null=' || COUNT(*) FROM SV LEFT JOIN Lop ON lop=ma WHERE Lop.ten='CS';
SELECT 'top_names=' || GROUP_CONCAT(ten, ',') FROM (SELECT ten FROM SV WHERE diem>=7 ORDER BY ten);
