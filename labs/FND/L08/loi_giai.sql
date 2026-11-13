CREATE TABLE giao_dich (
  id INTEGER PRIMARY KEY, tk INTEGER, so_tien INTEGER);
INSERT INTO giao_dich VALUES
  (1, 1, 800000), (2, 2, -120000), (3, 3, 450000),
  (4, 1, 300000), (5, 2, 500000), (6, 3, -50000),
  (7, 1, -100000), (8, 2, 70000);
SELECT tk, SUM(so_tien) FROM giao_dich GROUP BY tk ORDER BY tk;
SELECT 'tong', SUM(so_tien) FROM giao_dich;
SELECT 'am', COUNT(*) FROM giao_dich WHERE so_tien < 0;
