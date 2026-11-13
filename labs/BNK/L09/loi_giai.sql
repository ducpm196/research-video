CREATE TABLE but_toan (gd INTEGER, tk TEXT, tien INTEGER);
INSERT INTO but_toan VALUES (1, 'C', -1206600), (1, 'D', 1200000), (1, 'phi', 6600);
INSERT INTO but_toan VALUES (2, 'C', -50000), (2, 'D', 40000);
SELECT gd FROM but_toan GROUP BY gd HAVING SUM(tien) <> 0;
SELECT tk, SUM(tien) FROM but_toan GROUP BY tk ORDER BY tk;
