PRAGMA foreign_keys = ON;
CREATE TABLE SV(mssv TEXT PRIMARY KEY); INSERT INTO SV VALUES ('S1'),('S2');
CREATE TABLE Mon(ma TEXT PRIMARY KEY); INSERT INTO Mon VALUES ('DB'),('OS');
CREATE TABLE DK(mssv TEXT REFERENCES SV(mssv), ma TEXT REFERENCES Mon(ma), diem INT, PRIMARY KEY(mssv, ma));
INSERT OR IGNORE INTO DK VALUES ('S1','DB',8),('S1','OS',9),('S2','DB',7),('S1','DB',10);
SELECT 'enrolled_rows=' || COUNT(*) FROM DK;
SELECT 'dup_enroll_blocked=' || (COUNT(*)=3) FROM DK;
SELECT 'avg_s1=' || printf('%.1f', AVG(diem)) FROM DK WHERE mssv='S1';
