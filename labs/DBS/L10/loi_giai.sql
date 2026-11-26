CREATE INDEX idx_sk ON S(k);
SELECT 'joined_rows=' || COUNT(*) FROM R JOIN S ON R.k=S.k;
SELECT 'idx_sk_ok=' || COUNT(*) FROM sqlite_master WHERE name='idx_sk';
SELECT 'sum_v=' || SUM(S.v) FROM R JOIN S ON R.k=S.k;
