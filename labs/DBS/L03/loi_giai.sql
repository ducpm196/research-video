SELECT 'cnt_all=' || COUNT(*) || ' cnt_col=' || COUNT(lop) FROM SV;
SELECT 'eq_null=' || (SELECT COUNT(*) FROM SV WHERE lop = NULL) || ' is_null=' || COUNT(*) FROM SV WHERE lop IS NULL;
SELECT 'having_ge2_groups=' || COUNT(*) FROM (SELECT lop FROM SV GROUP BY lop HAVING COUNT(*) >= 2);
