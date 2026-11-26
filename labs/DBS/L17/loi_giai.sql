CREATE TABLE Users_New(id INT PRIMARY KEY);
WITH RECURSIVE c(x) AS (SELECT 1 UNION ALL SELECT x+1 FROM c WHERE x < (SELECT shadow_n FROM Cfg)) INSERT INTO Users_New SELECT x FROM c;
SELECT 'batches=' || (total_rows / batch_sz) FROM Cfg;
SELECT 'total_seconds=' || ((total_rows / batch_sz) * sec_tenth / 10) FROM Cfg;
SELECT 'shadow_copied=' || COUNT(*) FROM Users_New;
