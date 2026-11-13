CREATE TABLE gd (id INTEGER PRIMARY KEY, tk INTEGER, so_tien INTEGER);
INSERT INTO gd (tk, so_tien) VALUES (11, 900000), (12, -200000), (11, -150000), (13, 400000),
                                   (12, 600000), (11, 250000), (13, -100000);
CREATE INDEX i_gd_tk ON gd (tk);
SELECT id, so_tien FROM gd WHERE tk = 11 ORDER BY id;
SELECT COUNT(*) FROM gd WHERE so_tien < 0;
SELECT tk, SUM(so_tien) FROM gd GROUP BY tk ORDER BY tk;
