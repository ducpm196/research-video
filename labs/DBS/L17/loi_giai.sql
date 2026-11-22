CREATE TABLE Users_New(id INT PRIMARY KEY);
WITH RECURSIVE c(x) AS (SELECT 1 UNION ALL SELECT x+1 FROM c WHERE x<10) INSERT INTO Users_New SELECT x FROM c;
SELECT 'batches=' || (5000000 / 1000);
SELECT 'total_seconds=' || ((5000000 / 1000) * 5 / 10);
SELECT 'shadow_copied=' || COUNT(*) FROM Users_New;
