SELECT 'row_count=' || COUNT(*) FROM Logs;
SELECT 'plan_uses_scan=' || (1 - EXISTS(SELECT 1 FROM sqlite_master WHERE type='index' AND tbl_name='Logs'));
SELECT 'hits_42=' || COUNT(*) FROM Logs WHERE code = 42;
