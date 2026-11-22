CREATE TABLE Logs(id INT, code INT);
WITH RECURSIVE c(x) AS (SELECT 1 UNION ALL SELECT x+1 FROM c WHERE x<1000) INSERT INTO Logs SELECT x, x % 100 FROM c;
SELECT 'row_count=' || COUNT(*) FROM Logs;
SELECT 'plan_uses_scan=' || (1 - EXISTS(SELECT 1 FROM sqlite_master WHERE type='index' AND tbl_name='Logs'));
SELECT 'hits_42=' || COUNT(*) FROM Logs WHERE code = 42;
