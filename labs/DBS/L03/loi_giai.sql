CREATE TABLE SV(ten TEXT, lop TEXT);
INSERT INTO SV VALUES ('An','K1'),('Binh','K1'),('Chi','K2'),('Dung',NULL);
SELECT 'cnt_all=' || COUNT(*) || ' cnt_col=' || COUNT(lop) FROM SV;
SELECT 'eq_null=' || (SELECT COUNT(*) FROM SV WHERE lop = NULL) || ' is_null=' || COUNT(*) FROM SV WHERE lop IS NULL;
SELECT 'having_ge2_groups=' || COUNT(*) FROM (SELECT lop FROM SV GROUP BY lop HAVING COUNT(*) >= 2);
