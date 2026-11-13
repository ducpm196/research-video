CREATE TABLE ngan_hang (ma TEXT, tk TEXT, tien INTEGER);
CREATE TABLE chuyen_mach (ma TEXT, tien INTEGER);
INSERT INTO ngan_hang VALUES ('r8', 'A', -800000), ('r8b', 'A', -800000), ('r8c', 'A', -800000);
INSERT INTO chuyen_mach VALUES ('r8', 800000);
SELECT ma FROM ngan_hang WHERE ma NOT IN (SELECT ma FROM chuyen_mach) ORDER BY ma;
SELECT 3000000 + SUM(tien) FROM ngan_hang;
INSERT INTO ngan_hang SELECT 'dao-' || ma, tk, -tien FROM ngan_hang WHERE ma NOT IN (SELECT ma FROM chuyen_mach);
SELECT 3000000 + SUM(tien) FROM ngan_hang;
