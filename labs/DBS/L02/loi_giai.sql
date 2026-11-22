CREATE TABLE Lop(ma TEXT, ten TEXT);
INSERT INTO Lop VALUES ('K1','CS'),('K2','AI');
CREATE TABLE SV(ten TEXT, lop TEXT, diem INT);
INSERT INTO SV VALUES ('An','K1',8),('Binh','K1',6),('Chi','K2',9),('Dung',NULL,7);
SELECT 'left_all=' || COUNT(*) FROM SV LEFT JOIN Lop ON lop=ma;
SELECT 'left_where_drops_null=' || COUNT(*) FROM SV LEFT JOIN Lop ON lop=ma WHERE Lop.ten='CS';
SELECT 'top_names=' || GROUP_CONCAT(ten, ',') FROM (SELECT ten FROM SV WHERE diem>=7 ORDER BY ten);
