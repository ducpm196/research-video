CREATE INDEX idx_k ON Items(k);
SELECT 'total_rows=' || COUNT(*) FROM Items;
SELECT 'idx_exists=' || COUNT(*) FROM sqlite_master WHERE type='index' AND name='idx_k';
SELECT 'range_500_504=' || COUNT(*) FROM Items WHERE k BETWEEN 500 AND 504;
