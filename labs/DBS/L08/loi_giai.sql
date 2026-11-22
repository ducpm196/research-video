CREATE TABLE Items(id INT PRIMARY KEY, k INT);
WITH RECURSIVE c(x) AS (SELECT 1 UNION ALL SELECT x+1 FROM c WHERE x<10000) INSERT INTO Items SELECT x, x FROM c;
CREATE INDEX idx_k ON Items(k);
SELECT 'total_rows=' || COUNT(*) FROM Items;
SELECT 'idx_exists=' || COUNT(*) FROM sqlite_master WHERE type='index' AND name='idx_k';
SELECT 'range_500_504=' || COUNT(*) FROM Items WHERE k BETWEEN 500 AND 504;
